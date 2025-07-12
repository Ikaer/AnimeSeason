from flask import Blueprint, request, redirect, url_for, flash, session
from db.anime_db_storage import get_anime_db_storage
from mal.mal_api import fetch_seasonal_anime, MalUnauthorizedException
from mal.mal_auth import get_mal_auth
from models.MAL.response.season.anime_season_response import AnimeSeasonResponse
from models.MAL.response.season.node import Node

mal_bp = Blueprint('mal_bp', __name__)



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
    mal_auth = get_mal_auth();

    year = int(request.form['year'])
    season = request.form['season']
    token = session.get('mal_token')
    if not token:
        try:
            token = mal_auth.load_token()
        except Exception:
            token = None
    if not token or not mal_auth.is_mal_token_valid(token):
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
    mal_auth = get_mal_auth()
    auth_url, state, code_verifier = mal_auth.authorize()
    session['mal_code_verifier'] = code_verifier
    session['mal_oauth_state'] = state
    return redirect(auth_url)

@mal_bp.route('/mal/callback')
def mal_callback():
    mal_auth = get_mal_auth()

    code = request.args.get('code')
    returned_state = request.args.get('state')

    original_state = session.get('mal_oauth_state')
    code_verifier = session.get('mal_code_verifier')

    token = mal_auth.get_token(code, returned_state, original_state, code_verifier)

    mal_auth.save_token(token)

    session['mal_token'] = token
    flash('MAL authentication successful.')
    return redirect(url_for('main_bp.index'))

