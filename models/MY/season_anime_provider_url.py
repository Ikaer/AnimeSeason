from dataclasses import dataclass

@dataclass
class SeasonAnimeProviderUrl:
    provider_id: int
    anime_id: int
    url: str
    season: str  # e.g., 'spring', 'summer', 'fall', 'winter'
    year: int
