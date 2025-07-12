from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Studio:
    id: Optional[int] = None
    name: Optional[str] = None
