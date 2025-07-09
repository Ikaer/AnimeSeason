# Step1:
## On MAL fetch to get season animes:
### Consolidate the json files fetch on MAL api
actually we have on file per season and year. I would prefer to have only one big file, which will be fill/upsert on the fly when asking MAL for a season. 
Reason: The information of start year/season is already integrated in the mal response so no need to be a part of the filename too, also some anime season span can span for two season (25 episodes instead of 12).

### Get current season and season before
because of anime spanning on multiple season, when we ask a season, we need to ask the season before to be sure to also have anime currently airing but started at previous season.


### Change on the "/" from the flask app
#### Add a airing status dropdown
Add a status dropdown to select the airing status (default on "currently_airing"), filter the list on this status.

#### Implicitely add previous season when "currently_airing" selected.
If filter is "currently_airing", the previous season (in addition to the one asked) must be taken into account.

#### List returned by the "/" endpoint
The list returned by the "/" endpoint should be a list of #sym:SeasonComputedAnime, which will be concatenation of information from MAL file and #file:anime_providers.json file (my information about the provider for the anime season).

# Step2
Now we will need to manage our own json file for the season which will be "anime_providers.json" (cf #sym:SeasonAnimeProviderUrl ).

We dont directly write into the MAL json, because we want to be able to update whenever we want as the "source of truth".

The idea would be to have an UI that let met pick a provider and fill an URL for an anime season, and the update would go into this file (note: an anime can have multiple providers, so the UI should let me add multiple providers for the same anime).


