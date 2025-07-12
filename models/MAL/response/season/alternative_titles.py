from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class AlternativeTitles:
    synonyms: List[str] = field(default_factory=list)
    en: Optional[str] = None
    ja: Optional[str] = None
