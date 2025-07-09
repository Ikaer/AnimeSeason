import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from mal.mal_auth import MALAuth
from mal.mal_api import fetch_seasonal_anime, MalUnauthorizedException
import configparser
from requests_oauthlib import OAuth2Session
import secrets
import base64
from datetime import datetime
import dataclasses
import requests

from add_provider_url_route import provider_bp

import logging
logging.basicConfig(level=logging.DEBUG)

# === CONFIGURATION ===
config = configparser.ConfigParser()
config.read('config.ini')
DB_FOLDER = config['Paths']['anime_db_path']
CLIENT_ID = config['ApiKey']['mal']
REDIRECT_URI = config['ApiKey'].get('redirect_uri', None)
AUTH_URL = 'https://myanimelist.net/v1/oauth2/authorize'
TOKEN_URL = 'https://myanimelist.net/v1/oauth2/token'

os.makedirs(DB_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

SEASONS = ['winter', 'spring', 'summer', 'fall']

CONSOLIDATED_FILE = os.path.join(DB_FOLDER, "anime_seasons_mal.json")

# Register the provider blueprint
app.register_blueprint(provider_bp)

# Helper to load the consolidated anime dict
def load_consolidated_anime():
    if os.path.exists(CONSOLIDATED_FILE):
        with open(CONSOLIDATED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Helper to save the consolidated anime dict
def save_consolidated_anime(anime_dict):
    with open(CONSOLIDATED_FILE, 'w', encoding='utf-8') as f:
        json.dump(anime_dict, f, ensure_ascii=False, indent=2)

# Helper to upsert anime from a season fetch
# anime_season is AnimeSeasonResponse (dataclass)
def upsert_anime_season(anime_season):
    anime_dict = load_consolidated_anime()
    for anime_data in anime_season.data:
        node = anime_data.node
        # Convert dataclass to dict
        node_dict = dataclasses.asdict(node)
        anime_dict[str(node.id)] = node_dict
    save_consolidated_anime(anime_dict)

# Helper to get anime list for a year/season from consolidated file
def get_anime_list_from_consolidated(year, season):
    anime_dict = load_consolidated_anime()
    # Load provider info
    providers_path = os.path.join(DB_FOLDER, 'provider.json')
    anime_providers_path = os.path.join(DB_FOLDER, 'anime_providers.json')
    with open(providers_path, 'r', encoding='utf-8') as f:
        providers = {str(p['id']): p for p in json.load(f)}
    if os.path.exists(anime_providers_path):
        with open(anime_providers_path, 'r', encoding='utf-8') as f:
            anime_providers = json.load(f)
    else:
        anime_providers = {}
    result = []
    for anime in anime_dict.values():
        start_season = anime.get('start_season', {})
        if start_season.get('year') == year and start_season.get('season') == season:
            anime_id = str(anime['id'])
            # Attach provider info if available
            provider_entries = []
            for entry in anime_providers.get(anime_id, []):
                provider = providers.get(str(entry['provider_id']))
                if provider:
                    provider_entry = provider.copy()
                    provider_entry['url'] = entry['url']
                    provider_entries.append(provider_entry)
            anime['providers'] = provider_entries
            result.append(anime)
    return result

# Helper to get available years (scan files or hardcode)
def get_years():
    files = os.listdir(DB_FOLDER)
    years = set()
    for f in files:
        if f.startswith('anime_') and f.endswith('.json'):
            parts = f.split('_')
            if len(parts) >= 3:
                try:
                    years.add(int(parts[1]))
                except ValueError:
                    pass
    if not years:
        years = {2025}
    return sorted(years, reverse=True)

def get_json_path(year, season):
    return os.path.join(DB_FOLDER, f"anime_{year}_{season}.json")

def load_anime_list(year:int, season):
    json_path = get_json_path(year, season)
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_anime_list(year, season, anime_season):
    json_path = get_json_path(year, season)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json.loads(json.dumps(anime_season, default=lambda o: o.__dict__)), f, ensure_ascii=False, indent=2)

# Helper to check MAL token validity before fetching
def is_mal_token_valid(token):
    """Check if the MAL token is valid by making a lightweight API call."""
    try:
        headers = {"Authorization": f"Bearer {token['access_token'] if isinstance(token, dict) else token}"}
        resp = requests.get("https://api.myanimelist.net/v2/users/@me", headers=headers)
        if resp.status_code == 401:
            return False
        resp.raise_for_status()
        return True
    except Exception:
        return False

# === ROUTES ===
@app.route('/', methods=['GET', 'POST'])
def index():
    years = get_years()
    selected_year = int(request.values.get('year', years[0]))
    # Determine current season if not provided
    season_param = request.values.get('season')
    if season_param:
        selected_season = season_param
    else:
        month = datetime.now().month
        if month in [12, 1, 2]:
            selected_season = 'winter'
        elif month in [3, 4, 5]:
            selected_season = 'spring'
        elif month in [6, 7, 8]:
            selected_season = 'summer'
        else:
            selected_season = 'fall'
    # Use consolidated file
    anime_list = get_anime_list_from_consolidated(selected_year, selected_season)
    has_file = bool(anime_list)
    return render_template('index.html',
        years=years,
        seasons=SEASONS,
        selected_year=selected_year,
        selected_season=selected_season,
        anime_list=anime_list,
        has_file=has_file
    )

@app.route('/mal/fetch', methods=['POST'])
def mal_fetch():
    year = int(request.form['year'])
    season = request.form['season']
    # Use token from session or file
    token = session.get('mal_token')
    if not token:
        try:
            with open('mal_token.json', 'r', encoding='utf-8') as f:
                token = json.load(f)
        except Exception:
            token = None
    # Check token validity before proceeding
    if not token or not is_mal_token_valid(token):
        flash('Your MAL session has expired or is invalid. Please log in again.')
        return redirect(url_for('mal_login'))
    fields = (
        "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users," \
        "nsfw,genres,media_type,status,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures," \
        "background,related_anime,studios"
    )
    try:
        anime_season = fetch_seasonal_anime(token, year, season, limit=100, fields=fields, sort="anime_score")
    except MalUnauthorizedException:
        flash('Your MAL session has expired or is invalid. Please log in again.')
        return redirect(url_for('mal_login'))
    upsert_anime_season(anime_season)
    flash(f"Fetched and upserted anime list for {season} {year} into consolidated file.")
    return redirect(url_for('index', year=year, season=season))

@app.route('/mal/login')
def mal_login():
    # Start OAuth2 flow for MAL
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('utf-8')
    while len(code_verifier) < 43:
        code_verifier += "A"  # pad if needed
    session['mal_code_verifier'] = code_verifier
    print(f"[LOGIN] Generated code_verifier: \"{repr(code_verifier)}\"")
    print(f"[LOGIN] Redirect URI: \"{repr(REDIRECT_URI)}\"")
    print(f"[LOGIN] Client ID: \"{repr(CLIENT_ID)}\"")
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    auth_url, state = oauth.authorization_url(
        AUTH_URL,
        code_challenge=code_verifier,
        code_challenge_method='plain'
    )
    session['mal_oauth_state'] = state
    return redirect(auth_url)

@app.route('/mal/callback')
def mal_callback():
    code = request.args.get('code')
    code_verifier = session.get('mal_code_verifier')
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    
    print(f"[TOKEN] Generated code_verifier: \"{repr(code_verifier)}\"")
    print(f"[TOKEN] Redirect URI: \"{repr(REDIRECT_URI)}\"")
    print(f"[TOKEN] Client ID: \"{repr(CLIENT_ID)}\"")
    print(f"[TOKEN] Received code: {code}")
    token = oauth.fetch_token(
        TOKEN_URL,
        code=code,
        include_client_id=True,
        code_verifier=code_verifier
    )
    # Save token to file (single user)
    with open('mal_token.json', 'w', encoding='utf-8') as f:
        json.dump(token, f)
    session['mal_token'] = token
    flash('MAL authentication successful.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=12345)
