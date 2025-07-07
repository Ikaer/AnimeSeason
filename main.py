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

# === CONFIGURATION ===
config = configparser.ConfigParser()
config.read('config.ini')
CSV_DIR = config['Paths']['anime_db_path']
CLIENT_ID = config['ApiKey']['mal']
REDIRECT_URI = config['ApiKey'].get('redirect_uri', None)  # Optional, can be omitted
AUTH_URL = 'https://myanimelist.net/v1/oauth2/authorize'
TOKEN_URL = 'https://myanimelist.net/v1/oauth2/token'

os.makedirs(CSV_DIR, exist_ok=True)

# === FETCH SEASONAL ANIME ===
def fetch_seasonal_anime(token, year, season, limit=100):
    """Fetch seasonal anime from MAL API using OAuth2 token."""
    url = f"https://api.myanimelist.net/v2/anime/season/{year}/{season}?limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()['data']

# === SAVE TO CSV ===
def save_to_csv(anime_list, filename):
    """Save anime data to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "title", "media_type", "start_date"])
        for anime in anime_list:
            node = anime['node']
            writer.writerow([
                node.get('id'),
                node.get('title'),
                node.get('media_type'),
                node.get('start_date'),
            ])
    print(f"Saved {len(anime_list)} anime to {filename}")

# === MAIN ===
if __name__ == "__main__":
    # 1. Authenticate and get OAuth2 token (with refresh support)
    mal = MALAuth(CLIENT_ID, REDIRECT_URI, AUTH_URL, TOKEN_URL)
    token = mal.authenticate()
    # 2. Fetch anime for current season (example: 2025, summer)
    year = 2025
    season = 'summer'  # spring, summer, fall, winter
    anime_list = fetch_seasonal_anime(token, year, season)
    # 3. Save to CSV in configured directory
    csv_path = os.path.join(CSV_DIR, f"anime_{year}_{season}.csv")
    save_to_csv(anime_list, csv_path)
