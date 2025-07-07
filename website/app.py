import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from animecore.mal_auth import MALAuth
from animecore.mal_api import fetch_seasonal_anime
import configparser

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
app.secret_key = 'replace-this-with-a-random-secret-key'

SEASONS = ['winter', 'spring', 'summer', 'fall']

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

def load_anime_list(year, season):
    json_path = get_json_path(year, season)
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_anime_list(year, season, anime_season):
    json_path = get_json_path(year, season)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json.loads(json.dumps(anime_season, default=lambda o: o.__dict__)), f, ensure_ascii=False, indent=2)

# === ROUTES ===
@app.route('/', methods=['GET', 'POST'])
def index():
    years = get_years()
    selected_year = int(request.values.get('year', years[0]))
    selected_season = request.values.get('season', SEASONS[0])
    anime_list = load_anime_list(selected_year, selected_season)
    has_file = anime_list is not None
    return render_template('index.html',
        years=years,
        seasons=SEASONS,
        selected_year=selected_year,
        selected_season=selected_season,
        anime_list=anime_list['data'] if anime_list else [],
        has_file=has_file
    )

@app.route('/fetch', methods=['POST'])
def fetch():
    year = int(request.form['year'])
    season = request.form['season']
    # Authenticate and fetch from MAL
    mal = MALAuth(CLIENT_ID, REDIRECT_URI, AUTH_URL, TOKEN_URL)
    token = mal.authenticate()
    fields = (
        "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users," \
        "nsfw,genres,media_type,status,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures," \
        "background,related_anime,studios"
    )
    anime_season = fetch_seasonal_anime(token, year, season, limit=100, fields=fields, sort="anime_score")
    save_anime_list(year, season, anime_season)
    flash(f"Fetched and saved anime list for {season} {year}.")
    return redirect(url_for('index', year=year, season=season))

if __name__ == '__main__':
    app.run(debug=True)
