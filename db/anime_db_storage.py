import os
import json
from typing import Any, Type, TypeVar, Callable, Dict, List
from models.MAL.response.season.node import Node
from models.MY.anime_provider import AnimeProvider
from models.MY.season_anime_provider_url import SeasonAnimeProviderUrl
from dataclasses import asdict

class AnimeDbStorage:
    def __init__(self, db_folder: str):
        self.db_folder = db_folder

    def get_path(self, filename: str) -> str:
        return os.path.join(self.db_folder, filename)

    def load_consolidated_anime(self) -> Dict[str, Node]:
        """Load the consolidated anime dictionary from file as Node objects."""
        consolidated_file = self.get_path("anime_seasons_mal.json")
        if os.path.exists(consolidated_file):
            with open(consolidated_file, 'r', encoding='utf-8') as f:
                raw_dict = json.load(f)
            return {k: Node(**v) for k, v in raw_dict.items()}
        return {}

    def get_anime_list_from_consolidated(self, year: int, season: str) -> List[Dict[str, Any]]:
        """Get a list of anime for a given year and season, including provider info."""
        
        anime_dict = self.load_consolidated_anime()
        providers_path = self.get_path('provider.json')
        anime_providers_path = self.get_path('anime_providers.json')
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

    def get_years(self) -> List[int]:
        """Extract available years from anime JSON files in the DB folder."""
        files: List[str] = os.listdir(self.db_folder)
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


    def save_consolidated_anime(self, anime_dict: dict) -> None:
        consolidated_file = self.get_path("anime_seasons_mal.json")
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(anime_dict, f, ensure_ascii=False, indent=2)

    def load_providers(self) -> List[AnimeProvider]:
        provider_file = self.get_path('provider.json')
        with open(provider_file, 'r', encoding='utf-8') as f:
            providers_raw = json.load(f)
        return [AnimeProvider(**provider) for provider in providers_raw]

    def load_anime_providers(self) -> Dict[str, List[SeasonAnimeProviderUrl]]:
        anime_providers_file = self.get_path('anime_providers.json')
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

    def save_anime_providers(self, data: Dict[str, List[SeasonAnimeProviderUrl]]) -> None:
        anime_providers_file = self.get_path('anime_providers.json')
        serializable = {
            anime_id: [link.__dict__ for link in links]
            for anime_id, links in data.items()
        }
        with open(anime_providers_file, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)

    # Add other DB_FOLDER related methods here as needed

# Singleton instance
_anime_db_storage: AnimeDbStorage | None = None

def init_anime_db_storage(db_folder: str) -> None:
    global _anime_db_storage
    _anime_db_storage = AnimeDbStorage(db_folder)

def get_anime_db_storage() -> AnimeDbStorage:
    if _anime_db_storage is None:
        raise RuntimeError("AnimeDbStorage has not been initialized. Call init_anime_db_storage(db_folder) first.")
    return _anime_db_storage
