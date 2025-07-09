import requests
from models.MAL.response.season.anime_season_response import AnimeSeasonResponse
import json
import dataclasses

class MalUnauthorizedException(Exception):
    pass

def parse_anime_season_response(data):
    # Helper to recursively convert dicts to dataclasses
    def from_dict(cls, d):
        if isinstance(d, list):
            return [from_dict(cls.__args__[0], i) for i in d]
        if not isinstance(d, dict):
            return d
        if not dataclasses.is_dataclass(cls):
            return d
        fieldtypes = {f.name: f.type for f in cls.__dataclass_fields__.values()}
        return cls(**{k: from_dict(fieldtypes[k], v) for k, v in d.items() if k in fieldtypes})
    return from_dict(AnimeSeasonResponse, data)

def fetch_seasonal_anime(token, year, season, limit=100, offset=0, sort=None, fields=None, nsfw=None):
    """
    Fetch seasonal anime from MAL API using OAuth2 token and return as dataclasses.
    """
    url = f"https://api.myanimelist.net/v2/anime/season/{year}/{season}"
    params = {"limit": limit, "offset": offset}
    if sort:
        params["sort"] = sort
    if fields:
        params["fields"] = fields
    if nsfw is not None:
        params["nsfw"] = str(nsfw).lower()
    headers = {"Authorization": f"Bearer {token['access_token'] if isinstance(token, dict) else token}"}
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 401:
        raise MalUnauthorizedException("Unauthorized: Invalid or expired MAL token.")
    resp.raise_for_status()
    data = resp.json()
    return parse_anime_season_response(data)
