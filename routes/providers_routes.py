from flask import Blueprint, request, redirect, url_for, flash, current_app
import os
import json
from typing import Dict, List, Optional
from db.anime_db_storage import get_anime_db_storage
from models.MY.anime_provider import AnimeProvider
from models.MY.season_anime_provider_url import SeasonAnimeProviderUrl

provider_bp = Blueprint('provider_bp', __name__)

def get_provider_id_from_url(url: str, providers: List[AnimeProvider]) -> Optional[int]:
    for provider in providers:
        if url.startswith(provider.url):
            return provider.id
    return None

@provider_bp.route('/add_provider_url', methods=['POST'])
def add_provider_url() -> None:
    anime_db_storage = get_anime_db_storage()
    
    anime_id = str(request.form['anime_id'])
    provider_url = request.form['provider_url']

    providers = anime_db_storage.load_providers()
    provider_id = get_provider_id_from_url(provider_url, providers)
    if provider_id is None:
        flash('Provider not recognized from URL.')
        return redirect(url_for('main_bp.index'))
    
    anime_providers = anime_db_storage.load_anime_providers()
    if anime_id not in anime_providers:
        anime_providers[anime_id] = []
        
    # Prevent duplicate URLs for the same provider
    for entry in anime_providers[anime_id]:
        if entry.provider_id == provider_id:
            entry.url = provider_url
            break
    else:
        anime_providers[anime_id].append(SeasonAnimeProviderUrl(provider_id=provider_id, anime_id=int(anime_id), url=provider_url, season='', year=0))
    anime_db_storage.save_anime_providers(anime_providers)
    flash('Provider URL added.')
    return redirect(url_for('main_bp.index'))
