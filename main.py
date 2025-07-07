"""
AnimeSeason - Track new animes each season in a CSV sheet.

- Authenticates with MyAnimeList (MAL) using OAuth2 (main_auth).
- Fetches seasonal anime data from MAL API.
- Saves the results to a CSV file.

Instructions:
1. Register your app at https://myanimelist.net/apiconfig/application to get CLIENT_ID and CLIENT_SECRET.
2. Fill in your credentials below.
3. Run this script and follow the printed instructions for OAuth2 authentication.
"""

import requests
import configparser
import csv
import os
import urllib.parse
from mal_auth import MALAuth
from mal_api import fetch_seasonal_anime
from models.anime_season import AnimeSeasonResponse, AnimeData, Node
import json

# === CONFIGURATION ===
config = configparser.ConfigParser()
config.read('config.ini')
DB_FOLDER = config['Paths']['anime_db_path']
CLIENT_ID = config['ApiKey']['mal']
REDIRECT_URI = config['ApiKey'].get('redirect_uri', None)  # Optional, can be omitted
AUTH_URL = 'https://myanimelist.net/v1/oauth2/authorize'
TOKEN_URL = 'https://myanimelist.net/v1/oauth2/token'

os.makedirs(DB_FOLDER, exist_ok=True)

# === PARSE JSON TO DATACLASSES ===
def parse_anime_season_response(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Helper to recursively convert dicts to dataclasses
    def from_dict(cls, d):
        if isinstance(d, list):
            return [from_dict(cls.__args__[0], i) for i in d]
        if not isinstance(d, dict):
            return d
        fieldtypes = {f.name: f.type for f in cls.__dataclass_fields__.values()}
        return cls(**{k: from_dict(fieldtypes[k], v) for k, v in d.items() if k in fieldtypes})
    return from_dict(AnimeSeasonResponse, data)

# === SAVE TO CSV ===
def save_to_csv(anime_data_list, filename):
    """Save anime data (as dataclasses) to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "title", "media_type", "start_date"])
        for anime_data in anime_data_list:
            node = anime_data.node
            writer.writerow([
                node.id,
                node.title,
                node.media_type,
                node.start_date,
            ])
    print(f"Saved {len(anime_data_list)} anime to {filename}")

# === MAIN ===
if __name__ == "__main__":
    # 1. Authenticate and get OAuth2 token (with refresh support)
    mal = MALAuth(CLIENT_ID, REDIRECT_URI, AUTH_URL, TOKEN_URL)
    token = mal.authenticate()
    # 2. Fetch anime for current season (example: 2025, summer)
    year = 2025
    season = 'summer'  # spring, summer, fall, winter
    fields = (
        "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,"
        "nsfw,genres,media_type,status,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,"
        "background,related_anime,studios"
    )
    anime_season = fetch_seasonal_anime(token, year, season, limit=100, fields=fields, sort="anime_score")
    # 3. Save JSON response
    json_path = os.path.join(DB_FOLDER, f"anime_{year}_{season}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json.loads(json.dumps(anime_season, default=lambda o: o.__dict__)), f, ensure_ascii=False, indent=2)
    # 4. Save to CSV in configured directory
    # csv_path = os.path.join(DB_FOLDER, f"anime_{year}_{season}.csv")
    # save_to_csv(anime_season.data, csv_path)
