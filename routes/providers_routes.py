from flask import Blueprint, request, redirect, url_for, flash, current_app
import os
import json

provider_bp = Blueprint('provider_bp', __name__)

def get_db_folder():
    # Use the same DB_FOLDER as in app.py
    return current_app.config.get('DB_FOLDER') or getattr(current_app, 'DB_FOLDER', None) or 'AnimeSeasonDb'

def load_providers():
    db_folder = get_db_folder()
    provider_file = os.path.join(db_folder, 'provider.json')
    with open(provider_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_anime_providers():
    db_folder = get_db_folder()
    anime_providers_file = os.path.join(db_folder, 'anime_providers.json')
    if os.path.exists(anime_providers_file):
        with open(anime_providers_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_anime_providers(data):
    db_folder = get_db_folder()
    anime_providers_file = os.path.join(db_folder, 'anime_providers.json')
    with open(anime_providers_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_provider_id_from_url(url, providers):
    for provider in providers:
        if url.startswith(provider['url']):
            return provider['id']
    return None

@provider_bp.route('/add_provider_url', methods=['POST'])
def add_provider_url():
    anime_id = str(request.form['anime_id'])
    provider_url = request.form['provider_url']
    providers = load_providers()
    provider_id = get_provider_id_from_url(provider_url, providers)
    if not provider_id:
        flash('Provider not recognized from URL.')
        return redirect(url_for('main_bp.index'))
    anime_providers = load_anime_providers()
    if anime_id not in anime_providers:
        anime_providers[anime_id] = []
    # Prevent duplicate URLs for the same provider
    for entry in anime_providers[anime_id]:
        if entry['provider_id'] == provider_id:
            entry['url'] = provider_url
            break
    else:
        anime_providers[anime_id].append({'provider_id': provider_id, 'url': provider_url})
    save_anime_providers(anime_providers)
    flash('Provider URL added.')
    return redirect(url_for('main_bp.index'))
