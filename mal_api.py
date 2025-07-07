import requests

def fetch_seasonal_anime(token, year, season, limit=100, offset=0, sort=None, fields=None, nsfw=None):
    """
    Fetch seasonal anime from MAL API using OAuth2 token.
    Parameters:
        token (str): OAuth2 access token
        year (int): Year of the season
        season (str): 'winter', 'spring', 'summer', 'fall'
        limit (int): Number of results (max 500)
        offset (int): Offset for pagination
        sort (str): Sorting order (if supported)
        fields (str): Comma-separated list of fields to include
        nsfw (bool): Include NSFW content (True/False)
    Returns:
        dict: API response JSON
    """
    url = f"https://api.myanimelist.net/v2/anime/season/{year}/{season}"
    params = {"limit": limit, "offset": offset}
    if sort:
        params["sort"] = sort
    if fields:
        params["fields"] = fields
    if nsfw is not None:
        params["nsfw"] = str(nsfw).lower()
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()
