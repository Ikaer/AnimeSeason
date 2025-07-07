The main goal:
Provide an UI that let choose a season 


Now we will need to manage our own json file for the season which will be "anime_2025_summer_providers.json". We dont directly write into the MAL json, because we want to be able to update whenever we want as the "source of truth".
The idea would be to have an UI that let met pick a provider and fill an URL for an anime season, and it would go in this new file.
So we would start by loading #file:anime_2025_summer.json, load "anime_2025_summer_providers.json", then creates a list of #sym:SeasonComputedAnime  that would take an anime from MAL and if it exists the provider info I previously entered and then presents that in an UI.
THe UI would then let me enter the provider info for the one missing and update the file "anime_2025_summer_providers.json" behind the scene.

Can you make a plan on what we should to make that happened ?