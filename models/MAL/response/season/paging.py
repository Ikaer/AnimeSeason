from dataclasses import dataclass
from typing import Optional

@dataclass
class Paging:
    next: Optional[str] = None
    previous: Optional[str] = None
