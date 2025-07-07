from dataclasses import dataclass, field
from typing import Optional, List
from models.anime_season import Node, MainPicture, Genre, MyListStatus, StartSeason, Studio

@dataclass
class MyAnimeInfo:
    id: int
    title: str
    main_picture: Optional[MainPicture] = None
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
    media_type: Optional[str] = None
    status: Optional[str] = None
    my_list_status: Optional[MyListStatus] = None
    num_episodes: Optional[int] = None
    start_season: Optional[StartSeason] = None
    source: Optional[str] = None
    rating: Optional[str] = None
    studios: List[Studio] = field(default_factory=list)
    english_title: Optional[str] = None

    @classmethod
    def from_node(cls, node: Node):
        english_title = None
        if node.alternative_titles and node.alternative_titles.en:
            english_title = node.alternative_titles.en
        return cls(
            id=node.id,
            title=node.title,
            main_picture=node.main_picture,
            start_date=node.start_date,
            end_date=node.end_date,
            synopsis=node.synopsis,
            mean=node.mean,
            rank=node.rank,
            popularity=node.popularity,
            num_list_users=node.num_list_users,
            num_scoring_users=node.num_scoring_users,
            nsfw=node.nsfw,
            genres=node.genres,
            media_type=node.media_type,
            status=node.status,
            my_list_status=node.my_list_status,
            num_episodes=node.num_episodes,
            start_season=node.start_season,
            source=node.source,
            rating=node.rating,
            studios=node.studios,
            english_title=english_title
        )
