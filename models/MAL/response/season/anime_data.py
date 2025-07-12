from dataclasses import dataclass

from dataclasses_json import dataclass_json
from .node import Node

@dataclass_json
@dataclass
class AnimeData:
    node: Node
