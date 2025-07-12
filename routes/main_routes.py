from flask import Blueprint, render_template, request, current_app
from datetime import datetime
from typing import Any, Dict, List
import os
import json

from constants import SEASONS  # Use the shared seasons constant

main_bp = Blueprint('main_bp', __name__)

def load_consolidated_anime() -> Dict[str, Any]:
    """Load the consolidated anime dictionary from file."""
    db_folder: str = current_app.config['DB_FOLDER']
    consolidated_file: str = os.path.join(db_folder, "anime_seasons_mal.json")
    if os.path.exists(consolidated_file):
        with open(consolidated_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_anime_list_from_consolidated(year: int, season: str) -> List[Dict[str, Any]]:
    """Get a list of anime for a given year and season, including provider info."""
    db_folder: str = current_app.config['DB_FOLDER']
    anime_dict: Dict[str, Any] = load_consolidated_anime()
    providers_path: str = os.path.join(db_folder, 'provider.json')
    anime_providers_path: str = os.path.join(db_folder, 'anime_providers.json')
    with open(providers_path, 'r', encoding='utf-8') as f:
        providers: Dict[str, Any] = {str(p['id']): p for p in json.load(f)}
    if os.path.exists(anime_providers_path):
        with open(anime_providers_path, 'r', encoding='utf-8') as f:
            anime_providers: Dict[str, Any] = json.load(f)
    else:
        anime_providers = {}
    result: List[Dict[str, Any]] = []
    for anime in anime_dict.values():
        start_season: Dict[str, Any] = anime.get('start_season', {})
        if start_season.get('year') == year and start_season.get('season') == season:
            anime_id: str = str(anime['id'])
            provider_entries: List[Dict[str, Any]] = []
            for entry in anime_providers.get(anime_id, []):
                provider = providers.get(str(entry['provider_id']))
                if provider:
                    provider_entry = provider.copy()
                    provider_entry['url'] = entry['url']
                    provider_entries.append(provider_entry)
            anime['providers'] = provider_entries
            result.append(anime)
    return result

def get_years() -> List[int]:
    """Extract available years from anime JSON files in the DB folder."""
    db_folder: str = current_app.config['DB_FOLDER']
    files: List[str] = os.listdir(db_folder)
    years: set[int] = set()
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

def get_current_season() -> str:
    """Determine the current anime season based on the month."""
    month: int = datetime.now().month
    if month in [12, 1, 2]:
        return SEASONS[0]  # 'winter'
    elif month in [3, 4, 5]:
        return SEASONS[1]  # 'spring'
    elif month in [6, 7, 8]:
        return SEASONS[2]  # 'summer'
    return SEASONS[3]      # 'fall'

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    years: List[int] = get_years()
    selected_year: int = int(request.values.get('year', years[0]))
    selected_season: str = request.values.get('season') or get_current_season()
    anime_list: List[Dict[str, Any]] = get_anime_list_from_consolidated(selected_year, selected_season)
    has_file: bool = bool(anime_list)
    return render_template(
        'index.html',
        years=years,
        seasons=SEASONS,
        selected_year=selected_year,
        selected_season=selected_season,
        anime_list=anime_list,
        has_file=has_file
    )