from flask import Blueprint, request, redirect, url_for, flash, session, current_app, render_template
from db.anime_db_storage import get_anime_db_storage
from mal.mal_api import fetch_seasonal_anime, MalUnauthorizedException
import json
import os
import base64
import secrets
from requests_oauthlib import OAuth2Session
from models.MAL.response.season.anime_season_response import AnimeSeasonResponse
from models.MAL.response.season.node import Node

mal_bp = Blueprint('mal_bp', __name__)

def is_mal_token_valid(token):
    import requests
    try:
        headers = {"Authorization": f"Bearer {token['access_token'] if isinstance(token, dict) else token}"}
        resp = requests.get("https://api.myanimelist.net/v2/users/@me", headers=headers)
        if resp.status_code == 401:
            return False
        resp.raise_for_status()
        return True
    except Exception:
        return False

def upsert_anime_season(anime_season: AnimeSeasonResponse) -> None:
    """
    Upsert anime season data into the consolidated anime dictionary.
    """
    anime_db_storage = get_anime_db_storage()
    anime_dict = anime_db_storage.load_consolidated_anime()
    for anime_data in anime_season.data:
        node = anime_data.node
        anime_dict[str(node.id)] = node
    anime_db_storage.save_consolidated_anime(anime_dict)


@mal_bp.route('/mal/fetch', methods=['POST'])
def mal_fetch():
    year = int(request.form['year'])
    season = request.form['season']
    token = session.get('mal_token')
    if not token:
        try:
            with open('mal_token.json', 'r', encoding='utf-8') as f:
                token = json.load(f)
        except Exception:
            token = None
    if not token or not is_mal_token_valid(token):
        flash('Your MAL session has expired or is invalid. Please log in again.')
        return redirect(url_for('mal_bp.mal_login'))
    fields = (
        "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users," \
        "nsfw,genres,media_type,status,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures," \
        "background,related_anime,studios"
    )
    try:
        anime_season = fetch_seasonal_anime(token, year, season, limit=100, fields=fields, sort="anime_score")
    except MalUnauthorizedException:
        flash('Your MAL session has expired or is invalid. Please log in again.')
        return redirect(url_for('mal_bp.mal_login'))
    upsert_anime_season(anime_season)
    flash(f"Fetched and upserted anime list for {season} {year} into consolidated file.")
    return redirect(url_for('main_bp.index', year=year, season=season))

@mal_bp.route('/mal/login')
def mal_login():
    config = current_app.config
    CLIENT_ID = config['CLIENT_ID']
    REDIRECT_URI = config['REDIRECT_URI']
    AUTH_URL = config['AUTH_URL']
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('utf-8')
    while len(code_verifier) < 43:
        code_verifier += "A"
    session['mal_code_verifier'] = code_verifier
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    auth_url, state = oauth.authorization_url(
        AUTH_URL,
        code_challenge=code_verifier,
        code_challenge_method='plain'
    )
    session['mal_oauth_state'] = state
    return redirect(auth_url)

@mal_bp.route('/mal/callback')
def mal_callback():
    config = current_app.config
    CLIENT_ID = config['CLIENT_ID']
    REDIRECT_URI = config['REDIRECT_URI']
    TOKEN_URL = config['TOKEN_URL']
    code = request.args.get('code')
    code_verifier = session.get('mal_code_verifier')
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = oauth.fetch_token(
        TOKEN_URL,
        code=code,
        include_client_id=True,
        code_verifier=code_verifier
    )
    with open('mal_token.json', 'w', encoding='utf-8') as f:
        json.dump(token, f)
    session['mal_token'] = token
    flash('MAL authentication successful.')
    return redirect(url_for('main_bp.index'))

