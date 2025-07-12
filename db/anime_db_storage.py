import os
import json
from typing import Dict, List
from models.MAL.response.season.node import Node
from models.MY.anime_provider import AnimeProvider
from models.MY.season_anime_provider_url import SeasonAnimeProviderUrl, SeasonAnimeProviderUrlUI
from models.MY.season_computed_anime import SeasonComputedAnime
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
            # Use Node.from_dict for proper nested deserialization
            return {k: Node.from_dict(v) for k, v in raw_dict.items()}
        return {}

    def get_anime_list_from_consolidated(self, year: int, season: str) -> List[SeasonComputedAnime]:
        """
        Get a list of SeasonComputedAnime for a given year and season, including provider info.
        Also includes anime from the previous season that are still airing.
        """
        anime_dict = self.load_consolidated_anime()
        anime_providers = self.load_anime_providers()
        providers = self.load_providers()

        def build_ui_provider_urls(anime_id: str) -> List[SeasonAnimeProviderUrlUI]:
            provider_urls = anime_providers.get(anime_id, [])
            ui_provider_urls: List[SeasonAnimeProviderUrlUI] = []
            for provider_url in provider_urls:
                provider = next((p for p in providers if p.id == provider_url.provider_id), None)
                if provider:
                    ui_provider_urls.append(SeasonAnimeProviderUrlUI(provider=provider, url=provider_url.url))
            return ui_provider_urls

        result: List[SeasonComputedAnime] = []

        filtered_anime: List[Node] = []
        prev_year, prev_season = self.get_previous_season(year, season)
        # we want animer from the current season (whatever status they have) and also from the previous season that are still airing
        for anime in anime_dict.values():
            if anime.start_season and anime.start_season.year and anime.start_season.season:
                anime_year = anime.start_season.year
                anime_season = anime.start_season.season
                anime_status = anime.status               
                if (anime_year == year and anime_season == season) or (
                    anime_year == prev_year and anime_season == prev_season and anime_status == "currently_airing"
                ):
                    filtered_anime.append(anime)

        # Now convert filtered nodes to SeasonComputedAnime while avoiding duplicates
        seen_ids = set()
        for node in filtered_anime:
            if node.id not in seen_ids:
                seen_ids.add(node.id)
                ui_provider_urls = build_ui_provider_urls(str(node.id))
                result.append(SeasonComputedAnime.from_node(node, ui_provider_urls))
                
        return result


    @staticmethod
    def get_previous_season(year: int, season: str) -> tuple[int, str]:
        """Return the previous season and year using standard anime convention."""
        seasons = ["winter", "spring", "summer", "fall"]
        season = season.lower()
        if season not in seasons:
            raise ValueError(f"Unknown season: {season}")
        idx = seasons.index(season)
        if idx == 0:
            return year - 1, seasons[-1]
        return year, seasons[idx - 1]

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
