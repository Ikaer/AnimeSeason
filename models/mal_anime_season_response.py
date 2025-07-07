from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class MainPicture:
    medium: Optional[str] = None
    large: Optional[str] = None

@dataclass
class AlternativeTitles:
    synonyms: List[str] = field(default_factory=list)
    en: Optional[str] = None
    ja: Optional[str] = None

@dataclass
class Genre:
    id: Optional[int] = None
    name: Optional[str] = None

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

@dataclass
class StartSeason:
    year: Optional[int] = None
    season: Optional[str] = None

@dataclass
class Broadcast:
    day_of_the_week: Optional[str] = None
    start_time: Optional[str] = None

@dataclass
class Picture:
    medium: Optional[str] = None
    large: Optional[str] = None

@dataclass
class RelatedAnime:
    id: Optional[int] = None
    title: Optional[str] = None
    relation_type: Optional[str] = None
    relation_type_formatted: Optional[str] = None

@dataclass
class Studio:
    id: Optional[int] = None
    name: Optional[str] = None

@dataclass
class Node:
    id: int
    title: str
    main_picture: Optional[MainPicture] = None
    alternative_titles: Optional[AlternativeTitles] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    synopsis: Optional[str] = None
    mean: Optional[float] = None
    rank: Optional[int] = None
    popularity: Optional[int] = None
    num_list_users: Optional[int] = None
    num_scoring_users: Optional[int] = None
    nsfw: Optional[str] = None
    genres: List[Genre] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    media_type: Optional[str] = None
    status: Optional[str] = None
    my_list_status: Optional[MyListStatus] = None
    num_episodes: Optional[int] = None
    start_season: Optional[StartSeason] = None
    broadcast: Optional[Broadcast] = None
    source: Optional[str] = None
    average_episode_duration: Optional[int] = None
    rating: Optional[str] = None
    pictures: List[Picture] = field(default_factory=list)
    background: Optional[str] = None
    related_anime: List[RelatedAnime] = field(default_factory=list)
    studios: List[Studio] = field(default_factory=list)

@dataclass
class AnimeData:
    node: Node

@dataclass
class Paging:
    next: Optional[str] = None
    previous: Optional[str] = None

@dataclass
class AnimeSeasonResponse:
    data: List[AnimeData]
    paging: Optional[Paging] = None
