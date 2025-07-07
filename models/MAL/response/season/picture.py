from dataclasses import dataclass
from typing import Optional

@dataclass
class Picture:
    medium: Optional[str] = None
    large: Optional[str] = None
