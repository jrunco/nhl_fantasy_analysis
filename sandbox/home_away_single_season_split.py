
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


player_game_stats = client.stats.player_game_log(player_id=player_id, season_id=season, game_type="2")#, report_type="summary")

df_player_game_stats = pd.DataFrame(data=player_game_stats)

df_player_game_stats["powerPlayAssists"] = df_player_game_stats["powerPlayPoints"] - df_player_game_stats["powerPlayGoals"]
df_player_game_stats["shorthandedAssists"] = df_player_game_stats["shorthandedPoints"] - df_player_game_stats["shorthandedGoals"]




### side project -- make converting toi from mm:ss --> float a function that i can use in multiple places

def toi_string_to_float(df, str_param_name, float_param_name):

    # convert avgToi from a string to a float
    minutes = np.zeros(len(df))
    seconds = np.zeros(len(df))
    for i in range(len(df)):
        minutes[i], seconds[i] = map(int, df[str_param_name].values[i].split(":"))
    df[float_param_name] = minutes + (seconds / 60.)

    return df

df_player_game_stats = toi_string_to_float(df_player_game_stats, "toi", "toi_float")


### side project -- get home/road splits

df_player_game_stats_home = df_player_game_stats[df_player_game_stats["homeRoadFlag"] == "H"]
df_player_game_stats_road = df_player_game_stats[df_player_game_stats["homeRoadFlag"] == "R"]
'''
print("Average TOI:", np.mean(df_player_game_stats["toi_float"]))
print("Average TOI at home:", np.mean(df_player_game_stats_home["toi_float"]))
print("Average TOI on road:", np.mean(df_player_game_stats_road["toi_float"]))

print("Total Goals:", sum(df_player_game_stats["goals"]))
print("Total Goals at home:", sum(df_player_game_stats_home["goals"]))
print("Total Goals on road:", sum(df_player_game_stats_road["goals"]))

print("Total Goals/game:", round(sum(df_player_game_stats["goals"])/len(df_player_game_stats), 2))
print("Total Goals/game at home:", round(sum(df_player_game_stats_home["goals"])/len(df_player_game_stats_home), 2))
print("Total Goals/game on road:", round(sum(df_player_game_stats_road["goals"])/len(df_player_game_stats_road), 2))

#print(df_player_game_stats.to_string(index=False))
'''

# make total game stat per game and per 60
df_player_game_stats_points_per_game = round(sum(df_player_game_stats["points"])/len(df_player_game_stats), 2)
df_player_game_stats_points_per_60min = round((sum(df_player_game_stats["points"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
df_player_game_stats_goals_per_game = round(sum(df_player_game_stats["goals"])/len(df_player_game_stats), 2)
df_player_game_stats_goals_per_60min = round((sum(df_player_game_stats["goals"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
df_player_game_stats_assists_per_game = round(sum(df_player_game_stats["assists"])/len(df_player_game_stats), 2)
df_player_game_stats_assists_per_60min = round((sum(df_player_game_stats["assists"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
df_player_game_stats_shots_per_game = round(sum(df_player_game_stats["shots"])/len(df_player_game_stats), 2)
df_player_game_stats_shots_per_60min = round((sum(df_player_game_stats["shots"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
df_player_game_stats_pm_per_game = round(sum(df_player_game_stats["plusMinus"])/len(df_player_game_stats), 2)
df_player_game_stats_pm_per_60min = round((sum(df_player_game_stats["plusMinus"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
df_player_game_stats_pp_points_per_game = round(sum(df_player_game_stats["powerPlayPoints"])/len(df_player_game_stats), 2)
df_player_game_stats_pp_points_per_60min = round((sum(df_player_game_stats["powerPlayPoints"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
df_player_game_stats_pp_goals_per_game = round(sum(df_player_game_stats["powerPlayGoals"])/len(df_player_game_stats), 2)
df_player_game_stats_pp_goals_per_60min = round((sum(df_player_game_stats["powerPlayGoals"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
df_player_game_stats_pp_assists_per_game = round(sum(df_player_game_stats["powerPlayAssists"])/len(df_player_game_stats), 2)
df_player_game_stats_pp_assists_per_60min = round((sum(df_player_game_stats["powerPlayAssists"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
df_player_game_stats_shooting_percentage = round(sum(df_player_game_stats["goals"])/sum(df_player_game_stats["shots"])*100., 2)


# make home game stat per game and per 60
df_player_game_stats_home_points_per_game = round(sum(df_player_game_stats_home["points"])/len(df_player_game_stats_home), 2)
df_player_game_stats_home_points_per_60min = round((sum(df_player_game_stats_home["points"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
df_player_game_stats_home_goals_per_game = round(sum(df_player_game_stats_home["goals"])/len(df_player_game_stats_home), 2)
df_player_game_stats_home_goals_per_60min = round((sum(df_player_game_stats_home["goals"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
df_player_game_stats_home_assists_per_game = round(sum(df_player_game_stats_home["assists"])/len(df_player_game_stats_home), 2)
df_player_game_stats_home_assists_per_60min = round((sum(df_player_game_stats_home["assists"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
df_player_game_stats_home_shots_per_game = round(sum(df_player_game_stats_home["shots"])/len(df_player_game_stats_home), 2)
df_player_game_stats_home_shots_per_60min = round((sum(df_player_game_stats_home["shots"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
df_player_game_stats_home_pm_per_game = round(sum(df_player_game_stats_home["plusMinus"])/len(df_player_game_stats_home), 2)
df_player_game_stats_home_pm_per_60min = round((sum(df_player_game_stats_home["plusMinus"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
df_player_game_stats_home_pp_points_per_game = round(sum(df_player_game_stats_home["powerPlayPoints"])/len(df_player_game_stats_home), 2)
df_player_game_stats_home_pp_points_per_60min = round((sum(df_player_game_stats_home["powerPlayPoints"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
df_player_game_stats_home_pp_goals_per_game = round(sum(df_player_game_stats_home["powerPlayGoals"])/len(df_player_game_stats_home), 2)
df_player_game_stats_home_pp_goals_per_60min = round((sum(df_player_game_stats_home["powerPlayGoals"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
df_player_game_stats_home_pp_assists_per_game = round(sum(df_player_game_stats_home["powerPlayAssists"])/len(df_player_game_stats_home), 2)
df_player_game_stats_home_pp_assists_per_60min = round((sum(df_player_game_stats_home["powerPlayAssists"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
df_player_game_stats_home_shooting_percentage = round(sum(df_player_game_stats_home["goals"])/sum(df_player_game_stats_home["shots"])*100., 2)


# make road game stat per game and per 60
df_player_game_stats_road_points_per_game = round(sum(df_player_game_stats_road["points"])/len(df_player_game_stats_road), 2)
df_player_game_stats_road_points_per_60min = round((sum(df_player_game_stats_road["points"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
df_player_game_stats_road_goals_per_game = round(sum(df_player_game_stats_road["goals"])/len(df_player_game_stats_road), 2)
df_player_game_stats_road_goals_per_60min = round((sum(df_player_game_stats_road["goals"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
df_player_game_stats_road_assists_per_game = round(sum(df_player_game_stats_road["assists"])/len(df_player_game_stats_road), 2)
df_player_game_stats_road_assists_per_60min = round((sum(df_player_game_stats_road["assists"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
df_player_game_stats_road_shots_per_game = round(sum(df_player_game_stats_road["shots"])/len(df_player_game_stats_road), 2)
df_player_game_stats_road_shots_per_60min = round((sum(df_player_game_stats_road["shots"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
df_player_game_stats_road_pm_per_game = round(sum(df_player_game_stats_road["plusMinus"])/len(df_player_game_stats_road), 2)
df_player_game_stats_road_pm_per_60min = round((sum(df_player_game_stats_road["plusMinus"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
df_player_game_stats_road_pp_points_per_game = round(sum(df_player_game_stats_road["powerPlayPoints"])/len(df_player_game_stats_road), 2)
df_player_game_stats_road_pp_points_per_60min = round((sum(df_player_game_stats_road["powerPlayPoints"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
df_player_game_stats_road_pp_goals_per_game = round(sum(df_player_game_stats_road["powerPlayGoals"])/len(df_player_game_stats_road), 2)
df_player_game_stats_road_pp_goals_per_60min = round((sum(df_player_game_stats_road["powerPlayGoals"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
df_player_game_stats_road_pp_assists_per_game = round(sum(df_player_game_stats_road["powerPlayAssists"])/len(df_player_game_stats_road), 2)
df_player_game_stats_road_pp_assists_per_60min = round((sum(df_player_game_stats_road["powerPlayAssists"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
df_player_game_stats_road_shooting_percentage = round(sum(df_player_game_stats_road["goals"])/sum(df_player_game_stats_road["shots"])*100., 2)







table = PrettyTable(['Stat', 'All Games', "Home Games", "Away Games"])
table.title = "Home vs. Road Stat Split"
table.add_row(['# of games', len(df_player_game_stats), len(df_player_game_stats_home), len(df_player_game_stats_road)])
table.add_row(['Average TOI [minutes]', round(np.mean(df_player_game_stats["toi_float"]), 2), round(np.mean(df_player_game_stats_home["toi_float"]), 2), round(np.mean(df_player_game_stats_road["toi_float"]), 2)])
table.add_row(['Average # of Shifts', round(np.mean(df_player_game_stats["shifts"]), 2), round(np.mean(df_player_game_stats_home["shifts"]), 2), round(np.mean(df_player_game_stats_road["shifts"]), 2)])
table.add_divider()
table.add_row(['Total Points', sum(df_player_game_stats["points"]), sum(df_player_game_stats_home["points"]), sum(df_player_game_stats_road["points"])])
table.add_row(['Total Points per Game', df_player_game_stats_points_per_game, df_player_game_stats_home_points_per_game, df_player_game_stats_road_points_per_game])
table.add_row(['Total Points per 60 minutes', df_player_game_stats_points_per_60min, df_player_game_stats_home_points_per_60min, df_player_game_stats_road_points_per_60min])
table.add_divider()
table.add_row(['Total Goals', sum(df_player_game_stats["goals"]), sum(df_player_game_stats_home["goals"]), sum(df_player_game_stats_road["goals"])])
table.add_row(['Total Goals per Game', df_player_game_stats_goals_per_game, df_player_game_stats_home_goals_per_game, df_player_game_stats_road_goals_per_game])
table.add_row(['Total Goals per 60 minutes', df_player_game_stats_goals_per_60min, df_player_game_stats_home_goals_per_60min, df_player_game_stats_road_goals_per_60min])
table.add_divider()
table.add_row(['Total Assists', sum(df_player_game_stats["assists"]), sum(df_player_game_stats_home["assists"]), sum(df_player_game_stats_road["assists"])])
table.add_row(['Total Assists per Game', df_player_game_stats_assists_per_game, df_player_game_stats_home_assists_per_game, df_player_game_stats_road_assists_per_game])
table.add_row(['Total Assists per 60 minutes', df_player_game_stats_assists_per_60min, df_player_game_stats_home_assists_per_60min, df_player_game_stats_road_assists_per_60min])
table.add_divider()
table.add_row(['Total PP Points', sum(df_player_game_stats["powerPlayPoints"]), sum(df_player_game_stats_home["powerPlayPoints"]), sum(df_player_game_stats_road["powerPlayPoints"])])
table.add_row(['Total PP Points per Game', df_player_game_stats_pp_points_per_game, df_player_game_stats_home_pp_points_per_game, df_player_game_stats_road_pp_points_per_game])
table.add_row(['Total PP Points per 60 minutes', df_player_game_stats_pp_points_per_60min, df_player_game_stats_home_pp_points_per_60min, df_player_game_stats_road_pp_points_per_60min])
table.add_divider()
table.add_row(['Total PP Goals', sum(df_player_game_stats["powerPlayGoals"]), sum(df_player_game_stats_home["powerPlayGoals"]), sum(df_player_game_stats_road["powerPlayGoals"])])
table.add_row(['Total PP Goals per Game', df_player_game_stats_pp_goals_per_game, df_player_game_stats_home_pp_goals_per_game, df_player_game_stats_road_pp_goals_per_game])
table.add_row(['Total PP Goals per 60 minutes', df_player_game_stats_pp_goals_per_60min, df_player_game_stats_home_pp_goals_per_60min, df_player_game_stats_road_pp_goals_per_60min])
table.add_divider()
table.add_row(['Total PP Assists', sum(df_player_game_stats["powerPlayAssists"]), sum(df_player_game_stats_home["powerPlayAssists"]), sum(df_player_game_stats_road["powerPlayAssists"])])
table.add_row(['Total PP Assists per Game', df_player_game_stats_pp_assists_per_game, df_player_game_stats_home_pp_assists_per_game, df_player_game_stats_road_pp_assists_per_game])
table.add_row(['Total PP Assists per 60 minutes', df_player_game_stats_pp_assists_per_60min, df_player_game_stats_home_pp_assists_per_60min, df_player_game_stats_road_pp_assists_per_60min])
table.add_divider()
table.add_row(['Total Shots', sum(df_player_game_stats["shots"]), sum(df_player_game_stats_home["shots"]), sum(df_player_game_stats_road["shots"])])
table.add_row(['Total Shots per Game', df_player_game_stats_shots_per_game, df_player_game_stats_home_shots_per_game, df_player_game_stats_road_shots_per_game])
table.add_row(['Total Shots per 60 minutes', df_player_game_stats_shots_per_60min, df_player_game_stats_home_shots_per_60min, df_player_game_stats_road_shots_per_60min])
table.add_row(['Total Shooting %', df_player_game_stats_shooting_percentage, df_player_game_stats_home_shooting_percentage, df_player_game_stats_road_shooting_percentage])
#table.set_style(DOUBLE_BORDER)
print(table)






def home_away_split(player_id, season_id):

    client = NHLClient(debug=False)

    # find player and get player_id
    #get_player = player_name
    #position = "forwards" # dict_keys(['forwards', 'defensemen', 'goalies'])
    season = season_id

    """
    ''' this probably isn't needed in the jupyter notebook where i already know the player id'''
    # Get all current teams
    teams = client.teams.teams()
    for team in teams:
        roster = client.teams.team_roster(team_abbr=team["abbr"], season=season_id)
        for position in roster:
            for player in roster[position]:
                #print(player["firstName"]["default"] + " " + player["lastName"]["default"])
                if player["firstName"]["default"] + " " + player["lastName"]["default"] == get_player:
                    print(player["firstName"]["default"] + " " + player["lastName"]["default"])
                    print(player["id"])
                    player_id = player["id"]
    """
    player_id = str(player_id)
    player_game_stats = client.stats.player_game_log(player_id=str(player_id), season_id=season, game_type="2")

    df_player_game_stats = pd.DataFrame(data=player_game_stats)
    df_player_game_stats["powerPlayAssists"] = df_player_game_stats["powerPlayPoints"] - df_player_game_stats["powerPlayGoals"]
    df_player_game_stats["shorthandedAssists"] = df_player_game_stats["shorthandedPoints"] - df_player_game_stats["shorthandedGoals"]

    df_player_game_stats = toi_string_to_float(df_player_game_stats, "toi", "toi_float")

    df_player_game_stats_home = df_player_game_stats[df_player_game_stats["homeRoadFlag"] == "H"]
    df_player_game_stats_road = df_player_game_stats[df_player_game_stats["homeRoadFlag"] == "R"]

    df_player_game_stats_points_per_game = round(sum(df_player_game_stats["points"])/len(df_player_game_stats), 2)
    df_player_game_stats_points_per_60min = round((sum(df_player_game_stats["points"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
    df_player_game_stats_goals_per_game = round(sum(df_player_game_stats["goals"])/len(df_player_game_stats), 2)
    df_player_game_stats_goals_per_60min = round((sum(df_player_game_stats["goals"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
    df_player_game_stats_assists_per_game = round(sum(df_player_game_stats["assists"])/len(df_player_game_stats), 2)
    df_player_game_stats_assists_per_60min = round((sum(df_player_game_stats["assists"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
    df_player_game_stats_shots_per_game = round(sum(df_player_game_stats["shots"])/len(df_player_game_stats), 2)
    df_player_game_stats_shots_per_60min = round((sum(df_player_game_stats["shots"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
    df_player_game_stats_pm_per_game = round(sum(df_player_game_stats["plusMinus"])/len(df_player_game_stats), 2)
    df_player_game_stats_pm_per_60min = round((sum(df_player_game_stats["plusMinus"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
    df_player_game_stats_pp_points_per_game = round(sum(df_player_game_stats["powerPlayPoints"])/len(df_player_game_stats), 2)
    df_player_game_stats_pp_points_per_60min = round((sum(df_player_game_stats["powerPlayPoints"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
    df_player_game_stats_pp_goals_per_game = round(sum(df_player_game_stats["powerPlayGoals"])/len(df_player_game_stats), 2)
    df_player_game_stats_pp_goals_per_60min = round((sum(df_player_game_stats["powerPlayGoals"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
    df_player_game_stats_pp_assists_per_game = round(sum(df_player_game_stats["powerPlayAssists"])/len(df_player_game_stats), 2)
    df_player_game_stats_pp_assists_per_60min = round((sum(df_player_game_stats["powerPlayAssists"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2)
    df_player_game_stats_shooting_percentage = round(sum(df_player_game_stats["goals"])/sum(df_player_game_stats["shots"])*100., 2)

    # make home game stat per game and per 60
    df_player_game_stats_home_points_per_game = round(sum(df_player_game_stats_home["points"])/len(df_player_game_stats_home), 2)
    df_player_game_stats_home_points_per_60min = round((sum(df_player_game_stats_home["points"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
    df_player_game_stats_home_goals_per_game = round(sum(df_player_game_stats_home["goals"])/len(df_player_game_stats_home), 2)
    df_player_game_stats_home_goals_per_60min = round((sum(df_player_game_stats_home["goals"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
    df_player_game_stats_home_assists_per_game = round(sum(df_player_game_stats_home["assists"])/len(df_player_game_stats_home), 2)
    df_player_game_stats_home_assists_per_60min = round((sum(df_player_game_stats_home["assists"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
    df_player_game_stats_home_shots_per_game = round(sum(df_player_game_stats_home["shots"])/len(df_player_game_stats_home), 2)
    df_player_game_stats_home_shots_per_60min = round((sum(df_player_game_stats_home["shots"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
    df_player_game_stats_home_pm_per_game = round(sum(df_player_game_stats_home["plusMinus"])/len(df_player_game_stats_home), 2)
    df_player_game_stats_home_pm_per_60min = round((sum(df_player_game_stats_home["plusMinus"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
    df_player_game_stats_home_pp_points_per_game = round(sum(df_player_game_stats_home["powerPlayPoints"])/len(df_player_game_stats_home), 2)
    df_player_game_stats_home_pp_points_per_60min = round((sum(df_player_game_stats_home["powerPlayPoints"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
    df_player_game_stats_home_pp_goals_per_game = round(sum(df_player_game_stats_home["powerPlayGoals"])/len(df_player_game_stats_home), 2)
    df_player_game_stats_home_pp_goals_per_60min = round((sum(df_player_game_stats_home["powerPlayGoals"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
    df_player_game_stats_home_pp_assists_per_game = round(sum(df_player_game_stats_home["powerPlayAssists"])/len(df_player_game_stats_home), 2)
    df_player_game_stats_home_pp_assists_per_60min = round((sum(df_player_game_stats_home["powerPlayAssists"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2)
    df_player_game_stats_home_shooting_percentage = round(sum(df_player_game_stats_home["goals"])/sum(df_player_game_stats_home["shots"])*100., 2)

    # make road game stat per game and per 60
    df_player_game_stats_road_points_per_game = round(sum(df_player_game_stats_road["points"])/len(df_player_game_stats_road), 2)
    df_player_game_stats_road_points_per_60min = round((sum(df_player_game_stats_road["points"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
    df_player_game_stats_road_goals_per_game = round(sum(df_player_game_stats_road["goals"])/len(df_player_game_stats_road), 2)
    df_player_game_stats_road_goals_per_60min = round((sum(df_player_game_stats_road["goals"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
    df_player_game_stats_road_assists_per_game = round(sum(df_player_game_stats_road["assists"])/len(df_player_game_stats_road), 2)
    df_player_game_stats_road_assists_per_60min = round((sum(df_player_game_stats_road["assists"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
    df_player_game_stats_road_shots_per_game = round(sum(df_player_game_stats_road["shots"])/len(df_player_game_stats_road), 2)
    df_player_game_stats_road_shots_per_60min = round((sum(df_player_game_stats_road["shots"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
    df_player_game_stats_road_pm_per_game = round(sum(df_player_game_stats_road["plusMinus"])/len(df_player_game_stats_road), 2)
    df_player_game_stats_road_pm_per_60min = round((sum(df_player_game_stats_road["plusMinus"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
    df_player_game_stats_road_pp_points_per_game = round(sum(df_player_game_stats_road["powerPlayPoints"])/len(df_player_game_stats_road), 2)
    df_player_game_stats_road_pp_points_per_60min = round((sum(df_player_game_stats_road["powerPlayPoints"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
    df_player_game_stats_road_pp_goals_per_game = round(sum(df_player_game_stats_road["powerPlayGoals"])/len(df_player_game_stats_road), 2)
    df_player_game_stats_road_pp_goals_per_60min = round((sum(df_player_game_stats_road["powerPlayGoals"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
    df_player_game_stats_road_pp_assists_per_game = round(sum(df_player_game_stats_road["powerPlayAssists"])/len(df_player_game_stats_road), 2)
    df_player_game_stats_road_pp_assists_per_60min = round((sum(df_player_game_stats_road["powerPlayAssists"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)
    df_player_game_stats_road_shooting_percentage = round(sum(df_player_game_stats_road["goals"])/sum(df_player_game_stats_road["shots"])*100., 2)


    table = PrettyTable(['Stat', 'All Games', "Home Games", "Away Games"])
    table.title = "Home vs. Road Stat Split"
    table.add_row(['# of games', len(df_player_game_stats), len(df_player_game_stats_home), len(df_player_game_stats_road)])
    table.add_row(['Average TOI [minutes]', round(np.mean(df_player_game_stats["toi_float"]), 2), round(np.mean(df_player_game_stats_home["toi_float"]), 2), round(np.mean(df_player_game_stats_road["toi_float"]), 2)])
    table.add_row(['Average # of Shifts', round(np.mean(df_player_game_stats["shifts"]), 2), round(np.mean(df_player_game_stats_home["shifts"]), 2), round(np.mean(df_player_game_stats_road["shifts"]), 2)])
    table.add_divider()
    table.add_row(['Total Points', sum(df_player_game_stats["points"]), sum(df_player_game_stats_home["points"]), sum(df_player_game_stats_road["points"])])
    table.add_row(['Total Points per Game', df_player_game_stats_points_per_game, df_player_game_stats_home_points_per_game, df_player_game_stats_road_points_per_game])
    table.add_row(['Total Points per 60 minutes', df_player_game_stats_points_per_60min, df_player_game_stats_home_points_per_60min, df_player_game_stats_road_points_per_60min])
    table.add_divider()
    table.add_row(['Total Goals', sum(df_player_game_stats["goals"]), sum(df_player_game_stats_home["goals"]), sum(df_player_game_stats_road["goals"])])
    table.add_row(['Total Goals per Game', df_player_game_stats_goals_per_game, df_player_game_stats_home_goals_per_game, df_player_game_stats_road_goals_per_game])
    table.add_row(['Total Goals per 60 minutes', df_player_game_stats_goals_per_60min, df_player_game_stats_home_goals_per_60min, df_player_game_stats_road_goals_per_60min])
    table.add_divider()
    table.add_row(['Total Assists', sum(df_player_game_stats["assists"]), sum(df_player_game_stats_home["assists"]), sum(df_player_game_stats_road["assists"])])
    table.add_row(['Total Assists per Game', df_player_game_stats_assists_per_game, df_player_game_stats_home_assists_per_game, df_player_game_stats_road_assists_per_game])
    table.add_row(['Total Assists per 60 minutes', df_player_game_stats_assists_per_60min, df_player_game_stats_home_assists_per_60min, df_player_game_stats_road_assists_per_60min])
    table.add_divider()
    table.add_row(['Total PP Points', sum(df_player_game_stats["powerPlayPoints"]), sum(df_player_game_stats_home["powerPlayPoints"]), sum(df_player_game_stats_road["powerPlayPoints"])])
    table.add_row(['Total PP Points per Game', df_player_game_stats_pp_points_per_game, df_player_game_stats_home_pp_points_per_game, df_player_game_stats_road_pp_points_per_game])
    table.add_row(['Total PP Points per 60 minutes', df_player_game_stats_pp_points_per_60min, df_player_game_stats_home_pp_points_per_60min, df_player_game_stats_road_pp_points_per_60min])
    table.add_divider()
    table.add_row(['Total PP Goals', sum(df_player_game_stats["powerPlayGoals"]), sum(df_player_game_stats_home["powerPlayGoals"]), sum(df_player_game_stats_road["powerPlayGoals"])])
    table.add_row(['Total PP Goals per Game', df_player_game_stats_pp_goals_per_game, df_player_game_stats_home_pp_goals_per_game, df_player_game_stats_road_pp_goals_per_game])
    table.add_row(['Total PP Goals per 60 minutes', df_player_game_stats_pp_goals_per_60min, df_player_game_stats_home_pp_goals_per_60min, df_player_game_stats_road_pp_goals_per_60min])
    table.add_divider()
    table.add_row(['Total PP Assists', sum(df_player_game_stats["powerPlayAssists"]), sum(df_player_game_stats_home["powerPlayAssists"]), sum(df_player_game_stats_road["powerPlayAssists"])])
    table.add_row(['Total PP Assists per Game', df_player_game_stats_pp_assists_per_game, df_player_game_stats_home_pp_assists_per_game, df_player_game_stats_road_pp_assists_per_game])
    table.add_row(['Total PP Assists per 60 minutes', df_player_game_stats_pp_assists_per_60min, df_player_game_stats_home_pp_assists_per_60min, df_player_game_stats_road_pp_assists_per_60min])
    table.add_divider()
    table.add_row(['Total Shots', sum(df_player_game_stats["shots"]), sum(df_player_game_stats_home["shots"]), sum(df_player_game_stats_road["shots"])])
    table.add_row(['Total Shots per Game', df_player_game_stats_shots_per_game, df_player_game_stats_home_shots_per_game, df_player_game_stats_road_shots_per_game])
    table.add_row(['Total Shots per 60 minutes', df_player_game_stats_shots_per_60min, df_player_game_stats_home_shots_per_60min, df_player_game_stats_road_shots_per_60min])
    table.add_row(['Total Shooting %', df_player_game_stats_shooting_percentage, df_player_game_stats_home_shooting_percentage, df_player_game_stats_road_shooting_percentage])
    #table.set_style(DOUBLE_BORDER)
    print(table)



id = find_player_id("Will Smith", "20252026")

home_away_split(id, "20252026")



'''
t = PrettyTable(['Stat', 'All Games', "Home Games", "Away Games"])
t.title = "Home vs. Road Stat Split"
t.add_row(['# of games', len(df_player_game_stats), len(df_player_game_stats_home), len(df_player_game_stats_road)])
t.add_row(['Average TOI [minutes]', round(np.mean(df_player_game_stats["toi_float"]), 2), round(np.mean(df_player_game_stats_home["toi_float"]), 2), round(np.mean(df_player_game_stats_road["toi_float"]), 2)])
t.add_row(['Average # of Shifts', round(np.mean(df_player_game_stats["shifts"]), 2), round(np.mean(df_player_game_stats_home["shifts"]), 2), round(np.mean(df_player_game_stats_road["shifts"]), 2)])
t.add_divider()
### add points
t.add_row(['Total Goals', sum(df_player_game_stats["goals"]), sum(df_player_game_stats_home["goals"]), sum(df_player_game_stats_road["goals"])])
t.add_row(['Goals per Game', round(sum(df_player_game_stats["goals"])/len(df_player_game_stats), 2), round(sum(df_player_game_stats_home["goals"])/len(df_player_game_stats_home), 2), round(sum(df_player_game_stats_road["goals"])/len(df_player_game_stats_road), 2)])
t.add_row(['Goals per 60 minutes', round((sum(df_player_game_stats["goals"])/len(df_player_game_stats))/np.mean(df_player_game_stats["toi_float"]) * 60., 2),
    round((sum(df_player_game_stats_home["goals"])/len(df_player_game_stats_home))/np.mean(df_player_game_stats_home["toi_float"]) * 60., 2),
    round((sum(df_player_game_stats_road["goals"])/len(df_player_game_stats_road))/np.mean(df_player_game_stats_road["toi_float"]) * 60., 2)])
t.add_divider()
t.add_row(['Total Assists', sum(df_player_game_stats["assists"]), sum(df_player_game_stats_home["assists"]), sum(df_player_game_stats_road["assists"])])
t.add_row(['Assists per Game', round(sum(df_player_game_stats["assists"])/len(df_player_game_stats), 2), round(sum(df_player_game_stats_home["assists"])/len(df_player_game_stats_home), 2), round(sum(df_player_game_stats_road["assists"])/len(df_player_game_stats_road), 2)])
### add shots, shooting percentage
### add plus/minus
### add pp and sh stats
#t.set_style(DOUBLE_BORDER)
print(t)
'''



# end script
