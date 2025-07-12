from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class MyListStatus:
    status: Optional[str] = None
    score: Optional[int] = None
    num_episodes_watched: Optional[int] = None
    is_rewatching: Optional[bool] = None
    updated_at: Optional[str] = None
    start_date: Optional[str] = None
    finish_date: Optional[str] = None
    priority: Optional[int] = None
    num_times_rewatched: Optional[int] = None
    rewatch_value: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    comments: Optional[str] = None
