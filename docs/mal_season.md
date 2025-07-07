# MyAnimeList API v2 — Section: Anime Season

## Endpoint
GET /anime/season/{year}/{season}


- **Purpose:** Retrieve a list of anime for a specific season and year.

## Parameters

| Name     | Type     | Required | Description                                                         |
|----------|----------|----------|---------------------------------------------------------------------|
| year     | integer  | Yes      | The year of the season (e.g., 2024)                                 |
| season   | string   | Yes      | The season name: `winter`, `spring`, `summer`, or `fall`            |
| sort     | string   | No       | Sorting order (valid values not detailed in snippet)                 |
| limit    | integer  | No       | Default: 100. Max: 500. Number of anime to return                   |
| offset   | integer  | No       | Default: 0. Offset for pagination                                   |
| fields   | string   | No       | Comma-separated list of fields to include in the response           |

sort:
anime_score	Descending
anime_num_list_users	Descending

## Season Mapping

| Season  | Months                        |
|---------|-------------------------------|
| winter  | January, February, March      |
| spring  | April, May, June              |
| summer  | July, August, September       |
| fall    | October, November, December   |

## Example Request
curl 'https://api.myanimelist.net/v2/anime/season/2017/summer?limit=4'
-H 'Authorization: Bearer YOUR_TOKEN'



## Notes

- The endpoint supports pagination via `limit` and `offset`.
- You can customize the response using the `fields` parameter (e.g., `fields=id,title,synopsis`).
- Only the specified fields will be returned to reduce payload size.
- By default, some APIs don’t return NSFW content. You can control this with the `nsfw` parameter (`true` or `false`).
- Make sure to provide a valid OAuth2 Bearer token in the `Authorization` header.

## Error Codes

| Status Code | Error Code     | Description                                      |
|-------------|---------------|--------------------------------------------------|
| 400         | -             | Invalid Parameters                               |
| 401         | invalid_token | Expired or invalid access tokens                 |
| 403         | -             | Forbidden (e.g., DoS detected)                   |
| 404         | -             | Not Found                                        |


## Output Object Structure

The response object for this endpoint is a JSON object containing a list of anime for the specified season and year. Below is a breakdown of the available fields in the output object.

### Top-Level Fields

| Field      | Type    | Description                                      |
|------------|---------|--------------------------------------------------|
| data       | array   | List of anime objects for the season             |
| paging     | object  | Pagination info (next/previous URLs)             |

---

### `data` Array

Each element in the `data` array is an object with the following structure:

| Field   | Type   | Description                     |
|---------|--------|---------------------------------|
| node    | object | Main anime data (see below)     |

#### Example

### `node` Object — All Available Fields

| Field                   | Type      | Description                                                |
|-------------------------|-----------|------------------------------------------------------------|
| id                      | integer   | Anime ID                                                   |
| title                   | string    | Anime title                                                |
| main_picture            | object    | URLs for medium/large images                               |
| alternative_titles      | object    | Synonyms, English, Japanese titles                         |
| start_date              | string    | Airing start date (YYYY-MM-DD)                             |
| end_date                | string    | Airing end date (YYYY-MM-DD)                               |
| synopsis                | string    | Synopsis                                                   |
| mean                    | float     | Mean score                                                 |
| rank                    | integer   | Ranking                                                    |
| popularity              | integer   | Popularity ranking                                         |
| num_list_users          | integer   | Number of users with this anime on their list              |
| num_scoring_users       | integer   | Number of users who scored this anime                      |
| nsfw                    | string    | NSFW status (`white`, `gray`, `black`)                     |
| genres                  | array     | List of genres (id, name)                                  |
| created_at              | string    | Creation timestamp                                         |
| updated_at              | string    | Last update timestamp                                      |
| media_type              | string    | Type (tv, ova, movie, special, ona, music)                 |
| status                  | string    | Airing status (finished_airing, currently_airing, etc.)    |
| my_list_status          | object    | User's list status (if authenticated)                      |
| num_episodes            | integer   | Total number of episodes                                   |
| start_season            | object    | Season/year when anime started                             |
| broadcast               | object    | Broadcast day/time                                         |
| source                  | string    | Original source (manga, novel, etc.)                       |
| average_episode_duration| integer   | Average episode duration (seconds)                         |
| rating                  | string    | Age rating (G, PG, PG-13, R, R+, Rx)                      |
| pictures                | array     | Additional images                                          |
| background              | string    | Background information                                     |
| related_anime           | array     | Related anime (id, title, relation_type)                   |
| studios                 | array     | Studios (id, name)                                         |

**Note:**  
- Fields returned depend on the `fields` query parameter.
- Some fields (like `my_list_status`) require user authentication.
- Not all fields are always present for every anime.


## Sub-object Structures (Flat Reference)

---

// main_picture
{
"medium": "string", // URL to medium-sized image
"large": "string" // URL to large-sized image
}

// alternative_titles
{
"synonyms": ["string"], // List of alternative titles
"en": "string", // English title
"ja": "string" // Japanese title
}

// genres (array of objects)
[
{
"id": integer,
"name": "string"
}
]

// my_list_status (requires authentication)
{
"status": "string", // "watching", "completed", etc.
"score": integer, // User's score
"num_episodes_watched": integer, // Episodes watched
"is_rewatching": boolean, // Rewatching flag
"updated_at": "string", // ISO8601 timestamp
"start_date": "string", // (optional) Start date (YYYY-MM-DD)
"finish_date": "string", // (optional) Finish date (YYYY-MM-DD)
"priority": integer, // (optional) User priority
"num_times_rewatched": integer, // (optional) Times rewatched
"rewatch_value": integer, // (optional) Rewatch value
"tags": ["string"], // (optional) Tags
"comments": "string" // (optional) Comments
}

// start_season
{
"year": integer,
"season": "string" // "winter", "spring", "summer", "fall"
}

// broadcast
{
"day_of_the_week": "string", // e.g. "Monday"
"start_time": "string" // e.g. "18:00"
}

// pictures (array of objects)
[
{
"medium": "string", // URL
"large": "string" // URL
}
]

// related_anime (array of objects)
[
{
"id": integer,
"title": "string",
"relation_type": "string", // e.g. "sequel", "prequel"
"relation_type_formatted": "string" // Human-readable label
}
]

// studios (array of objects)
[
{
"id": integer,
"name": "string"
}
]

text

---

- All sub-objects are shown in a single, continuous code block for **easy copy-paste**.
- Arrays are shown with a single sample object for clarity.
- Optional fields are indicated in comments.



### `paging` Object

| Field     | Type    | Description                              |
|-----------|---------|------------------------------------------|
| next      | string  | URL for the next page of results         |
| previous  | string  | URL for the previous page of results     |

---

## References

- [MyAnimeList API v2 Documentation](https://myanimelist.net/apiconfig/references/api/v2#operation/anime_season_year_season_get)
