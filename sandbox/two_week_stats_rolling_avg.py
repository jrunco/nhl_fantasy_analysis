
import numpy as np
import pandas as pd

from tabulate import tabulate
from prettytable import PrettyTable, DOUBLE_BORDER


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



'''
- change mean to median and add in bootstraped median uncertainty
'''




def find_player_id(player_name, season):

    client = NHLClient(debug=False)

    # find player and get player_id
    get_player = player_name
    #position = "forwards" # dict_keys(['forwards', 'defensemen', 'goalies'])
    season = season

    # Get all current teams
    teams = client.teams.teams()
    for team in teams:

        roster = client.teams.team_roster(team_abbr=team["abbr"], season="20252026")
        for position in roster:
            for player in roster[position]:
                if player["firstName"]["default"] + " " + player["lastName"]["default"] == get_player:
                    player_id = player["id"]

    return player_id






client = NHLClient(debug=False)


# find player and get player_id

get_player = "Will Smith"
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

df_player_game_stats = pd.DataFrame(data=player_game_stats)

df_player_game_stats["powerPlayAssists"] = df_player_game_stats["powerPlayPoints"] - df_player_game_stats["powerPlayGoals"]
df_player_game_stats["shorthandedAssists"] = df_player_game_stats["shorthandedPoints"] - df_player_game_stats["shorthandedGoals"]






# end script
