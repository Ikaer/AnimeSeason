from dataclasses import dataclass
from typing import Optional

@dataclass
class RelatedAnime:
    id: Optional[int] = None
    title: Optional[str] = None
    relation_type: Optional[str] = None
    relation_type_formatted: Optional[str] = None
