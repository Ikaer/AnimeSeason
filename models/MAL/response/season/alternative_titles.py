from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class AlternativeTitles:
    synonyms: List[str] = field(default_factory=list)
    en: Optional[str] = None
    ja: Optional[str] = None
