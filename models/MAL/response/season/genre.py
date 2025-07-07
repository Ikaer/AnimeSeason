from dataclasses import dataclass
from typing import Optional

@dataclass
class Genre:
    id: Optional[int] = None
    name: Optional[str] = None
