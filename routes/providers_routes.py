from flask import Blueprint, request, redirect, url_for, flash, current_app
import os
import json
from typing import Dict, List, Optional
from models.MY.anime_provider import AnimeProvider
from models.MY.season_anime_provider_url import SeasonAnimeProviderUrl

provider_bp = Blueprint('provider_bp', __name__)

def get_db_folder() -> str:
    """
    Get the DB_FOLDER from Flask current_app config. Raises RuntimeError if not set or empty.
    """
    db_folder = current_app.config.get('DB_FOLDER')
    if not db_folder:
        raise RuntimeError("DB_FOLDER is not set in Flask config.")
    return db_folder

def load_providers() -> List[AnimeProvider]:
    db_folder = get_db_folder()
    provider_file = os.path.join(db_folder, 'provider.json')
    with open(provider_file, 'r', encoding='utf-8') as f:
        providers_raw = json.load(f)
    return [AnimeProvider(**provider) for provider in providers_raw]

def load_anime_providers() -> Dict[str, List[SeasonAnimeProviderUrl]]:
    db_folder = get_db_folder()
    anime_providers_file = os.path.join(db_folder, 'anime_providers.json')
    if os.path.exists(anime_providers_file):
        with open(anime_providers_file, 'r', encoding='utf-8') as f:
            anime_providers_raw = json.load(f)
        return {
            anime_id: [SeasonAnimeProviderUrl(
                provider_id=link['provider_id'],
                anime_id=int(anime_id),
                url=link['url'],
                season=link.get('season', ''),
                year=link.get('year', 0)
            ) for link in links]
            for anime_id, links in anime_providers_raw.items()
        }
    return {}

def save_anime_providers(data: Dict[str, List[SeasonAnimeProviderUrl]]) -> None:
    db_folder = get_db_folder()
    anime_providers_file = os.path.join(db_folder, 'anime_providers.json')
    serializable = {
        anime_id: [link.__dict__ for link in links]
        for anime_id, links in data.items()
    }
    with open(anime_providers_file, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

def get_provider_id_from_url(url: str, providers: List[AnimeProvider]) -> Optional[int]:
    for provider in providers:
        if url.startswith(provider.url):
            return provider.id
    return None

@provider_bp.route('/add_provider_url', methods=['POST'])
def add_provider_url() -> None:
    anime_id = str(request.form['anime_id'])
    provider_url = request.form['provider_url']
    providers = load_providers()
    provider_id = get_provider_id_from_url(provider_url, providers)
    if provider_id is None:
        flash('Provider not recognized from URL.')
        return redirect(url_for('main_bp.index'))
    anime_providers = load_anime_providers()
    if anime_id not in anime_providers:
        anime_providers[anime_id] = []
    # Prevent duplicate URLs for the same provider
    for entry in anime_providers[anime_id]:
        if entry.provider_id == provider_id:
            entry.url = provider_url
            break
    else:
        anime_providers[anime_id].append(SeasonAnimeProviderUrl(provider_id=provider_id, anime_id=int(anime_id), url=provider_url, season='', year=0))
    save_anime_providers(anime_providers)
    flash('Provider URL added.')
    return redirect(url_for('main_bp.index'))
