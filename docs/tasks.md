### Get current season and season before
on MAL anime fetch, because of anime spanning on multiple season, when we ask a season, we also need to ask the season before to be sure to also have anime currently airing but started at previous season.


### Change on the "/" from the flask app
#### Add a airing status dropdown
Add a status dropdown to select the airing status (default on "currently_airing"), filter the list on this status.

#### Implicitely add previous season when "currently_airing" selected.
If filter is "currently_airing", the previous season (in addition to the one asked) must be taken into account.

#### List returned by the "/" endpoint
The list returned by the "/" endpoint should be a list of #sym:SeasonComputedAnime, which will be concatenation of information from MAL file and #file:anime_providers.json file (my information about the provider for the anime season).
