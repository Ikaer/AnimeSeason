from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class RelatedAnime:
    id: Optional[int] = None
    title: Optional[str] = None
    relation_type: Optional[str] = None
    relation_type_formatted: Optional[str] = None
