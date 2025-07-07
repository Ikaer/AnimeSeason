from dataclasses import dataclass
from typing import Optional

@dataclass
class StartSeason:
    year: Optional[int] = None
    season: Optional[str] = None
