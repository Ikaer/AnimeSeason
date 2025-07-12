from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Paging:
    next: Optional[str] = None
    previous: Optional[str] = None
