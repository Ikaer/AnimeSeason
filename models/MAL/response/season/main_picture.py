from dataclasses import dataclass
from typing import Optional

@dataclass
class MainPicture:
    medium: Optional[str] = None
    large: Optional[str] = None
