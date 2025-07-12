from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class StartSeason:
    year: Optional[int] = None
    season: Optional[str] = None
