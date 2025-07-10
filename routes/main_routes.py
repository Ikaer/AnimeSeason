from flask import Blueprint, render_template, request, current_app
from datetime import datetime
import os
import json

main_bp = Blueprint('main_bp', __name__)

# Helper to load the consolidated anime dict
def load_consolidated_anime():
    db_folder = current_app.config['DB_FOLDER']
    consolidated_file = os.path.join(db_folder, "anime_seasons_mal.json")
    if os.path.exists(consolidated_file):
        with open(consolidated_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_anime_list_from_consolidated(year, season):
    db_folder = current_app.config['DB_FOLDER']
    anime_dict = load_consolidated_anime()
    providers_path = os.path.join(db_folder, 'provider.json')
    anime_providers_path = os.path.join(db_folder, 'anime_providers.json')
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

def get_years():
    db_folder = current_app.config['DB_FOLDER']
    files = os.listdir(db_folder)
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

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    years = get_years()
    selected_year = int(request.values.get('year', years[0]))
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
    anime_list = get_anime_list_from_consolidated(selected_year, selected_season)
    has_file = bool(anime_list)
    return render_template('index.html',
        years=years,
        seasons=['winter', 'spring', 'summer', 'fall'],
        selected_year=selected_year,
        selected_season=selected_season,
        anime_list=anime_list,
        has_file=has_file
    )
