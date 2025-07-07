from dataclasses import dataclass
from typing import Optional

@dataclass
class Broadcast:
    day_of_the_week: Optional[str] = None
    start_time: Optional[str] = None
