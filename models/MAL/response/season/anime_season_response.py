from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json
from .anime_data import AnimeData
from .paging import Paging

@dataclass_json
@dataclass
class AnimeSeasonResponse:
    data: List[AnimeData]
    paging: Optional[Paging] = None
