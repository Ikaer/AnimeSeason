from dataclasses import dataclass
from typing import Optional

@dataclass
class Studio:
    id: Optional[int] = None
    name: Optional[str] = None
