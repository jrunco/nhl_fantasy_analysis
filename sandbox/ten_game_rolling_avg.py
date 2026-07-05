
import numpy as np
import pandas as pd

from nhlpy.nhl_client import NHLClient

from nhlpy.api.query.builder import QueryBuilder, QueryContext
from nhlpy.api.query.filters.draft import DraftQuery
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.game_type import GameTypeQuery
from nhlpy.api.query.filters.position import PositionQuery, PositionTypes
from nhlpy.api.query.filters.franchise import FranchiseQuery
from nhlpy.api.query.filters.shoot_catch import ShootCatchesQuery
from nhlpy.api.query.filters.status import StatusQuery
from nhlpy.api.query.filters.opponent import OpponentQuery
from nhlpy.api.query.filters.home_road import HomeRoadQuery
from nhlpy.api.query.filters.experience import ExperienceQuery
from nhlpy.api.query.filters.decision import DecisionQuery


#### fantasy points ####
fantasy_goals = 6.0
fantasy_assists = 4.0
fantasy_plusminus = 1.5
fantasy_pp_goals = 2.0
fantasy_pp_assists = 2.0
fantasy_sh_goals = 4.0
fantasy_sh_assists = 1.0
fantasy_game_winning_goals = 1.0
fantasy_shots = 0.75
fantasy_hits = 0.4
fantasy_blocks = 1.25
fantasy_fowins = 0.15
fantasy_folosses = -0.15
fantasy_pims = 0.0



client = NHLClient(debug=True)


# find player and get player_id

get_player = "Macklin Celebrini"
#position = "forwards" # dict_keys(['forwards', 'defensemen', 'goalies'])
season = "20252026"

# Get all current teams
teams = client.teams.teams()

for team in teams:

    roster = client.teams.team_roster(team_abbr=team["abbr"], season="20252026")

    for position in roster:

        for player in roster[position]:

            #print(player["firstName"]["default"] + " " + player["lastName"]["default"])
            if player["firstName"]["default"] + " " + player["lastName"]["default"] == get_player:
                print(player["firstName"]["default"] + " " + player["lastName"]["default"])
                print(player["id"])
                player_id = player["id"]


player_game_stats = client.stats.player_game_log(player_id=player_id, season_id=season, game_type="2")
















# end script
