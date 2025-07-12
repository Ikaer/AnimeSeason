from dataclasses import dataclass

from dataclasses_json import dataclass_json

from models.MY.anime_provider import AnimeProvider

@dataclass_json
@dataclass
class SeasonAnimeProviderUrl:
    provider_id: int
    anime_id: int
    url: str
    season: str  # e.g., 'spring', 'summer', 'fall', 'winter'
    year: int


@dataclass_json
@dataclass
class SeasonAnimeProviderUrlUI:
    provider: AnimeProvider
    url: str