from dataclasses import dataclass, field
from typing import List, Optional
from .main_picture import MainPicture
from .alternative_titles import AlternativeTitles
from .genre import Genre
from .my_list_status import MyListStatus
from .start_season import StartSeason
from .broadcast import Broadcast
from .picture import Picture
from .related_anime import RelatedAnime
from .studio import Studio

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
