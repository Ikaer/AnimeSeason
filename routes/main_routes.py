from flask import Blueprint, render_template, request, current_app
from datetime import datetime
from typing import Any, Dict, List
import os
import json

from constants import SEASONS
from db.anime_db_storage import get_anime_db_storage  # Use the shared seasons constant

main_bp = Blueprint('main_bp', __name__)

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
    """Render the main page with anime list for the selected year and season."""
    anime_db_storage = get_anime_db_storage()
    years: List[int] = anime_db_storage.get_years()
    selected_year: int = int(request.values.get('year', years[0]))
    selected_season: str = request.values.get('season') or get_current_season()
    anime_list: List[Dict[str, Any]] = anime_db_storage.get_anime_list_from_consolidated(selected_year, selected_season)
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