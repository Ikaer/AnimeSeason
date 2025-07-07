from dataclasses import dataclass
from typing import List, Optional
from .anime_data import AnimeData
from .paging import Paging

@dataclass
class AnimeSeasonResponse:
    data: List[AnimeData]
    paging: Optional[Paging] = None
