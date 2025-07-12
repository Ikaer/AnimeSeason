from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Broadcast:
    day_of_the_week: Optional[str] = None
    start_time: Optional[str] = None
