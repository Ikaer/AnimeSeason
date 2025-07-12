from dataclasses import dataclass

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class AnimeProvider:
    name: str
    id: int
    logo: str
    url: str
