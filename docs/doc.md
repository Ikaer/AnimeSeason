# General purpose.
Create an application that allows me to track new animes each season in a sheet.

# Language/Stack
We are using python (i'm new to it).

# First version
- ask the MAL (MyAnimeList) API for the seasonal anime.
- ideally using the main_auth (my account and not the api key), but I'm not sure how to implement this oauth2 flow.
- put them into a csv which will works as database for us.


# documentation of mal API
https://myanimelist.net/apiconfig/references/api/v2

## Auth
### main_auth
Security Scheme Type	OAuth2
implicit OAuth Flow	
Authorization URL: https://myanimelist.net/v1/oauth2/authorize
Scopes:
write:users - The API client can see and modify basic profile information and users' list data, post information to MyAnimelist on behalf of users.

### client_auth
When user login is not required, the X-MAL-CLIENT-ID request header can be used to authenticate the client by setting your API client ID.

Security Scheme Type	API Key
Header parameter name:	X-MAL-CLIENT-ID

## Our interests:
What specifically interest us is this endpoint:
https://myanimelist.net/apiconfig/references/api/v2#operation/anime_season_year_season_get 
ex:
curl 'https://api.myanimelist.net/v2/anime/season/2017/summer?limit=100' \
-H 'Authorization: Bearer YOUR_TOKEN'

