
import numpy as np
import pandas as pd

from tabulate import tabulate
from prettytable import PrettyTable, DOUBLE_BORDER

import matplotlib.pyplot as plt

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

df_player_game_stats = pd.DataFrame(data=player_game_stats)

df_player_game_stats["powerPlayAssists"] = df_player_game_stats["powerPlayPoints"] - df_player_game_stats["powerPlayGoals"]
df_player_game_stats["shorthandedAssists"] = df_player_game_stats["shorthandedPoints"] - df_player_game_stats["shorthandedGoals"]


df_player_game_stats_reverse = df_player_game_stats.iloc[::-1]
df_player_game_stats_reverse["gameDate"] = pd.to_datetime(df_player_game_stats_reverse['gameDate'])


df_rolling_avs = df_player_game_stats_reverse.set_index('gameDate')
'''
df_rolling_avs['goals_rolling_mean'] = df_rolling_avs['goals'].rolling(window='14D').mean()
df_rolling_avs['assists_rolling_mean'] = df_rolling_avs['assists'].rolling(window='14D').mean()

#df_rolling_avs['points_rolling_mean'] = df_rolling_avs['points'].rolling(window='14D', center=True, min_periods=1).mean().resample('7D').asfreq('D')
df_rolling_avs['points_rolling_mean'] = df_rolling_avs['points'].rolling(window='14D', center=True, min_periods=1).mean().resample('7D').last()

#df_rolling_avs_7D_resample = df_rolling_avs.iloc[13::7].to_frame()

plt.scatter(df_rolling_avs.index, df_rolling_avs['points_rolling_mean'])
plt.show()


for i in range(len(df_rolling_avs)):
    print(df_rolling_avs.index[i], df_rolling_avs['points'].values[i])
'''

df_rolling_avs_daily = df_rolling_avs.resample('1D').asfreq()
df_rolling_avs_daily['points_rolling_mean'] = df_rolling_avs_daily['points'].rolling(window='14D', center=False, min_periods=1).mean().resample('7D').last()


for i in range(len(df_rolling_avs_daily)):
    print(df_rolling_avs_daily.index[i], df_rolling_avs_daily['points'].values[i], df_rolling_avs_daily['points_rolling_mean'].values[i])


plt.scatter(df_rolling_avs_daily.index, df_rolling_avs_daily['points_rolling_mean'])
plt.show()



## this only makes 10 data points
#df_rolling_avs['points_rolling_mean'] = df_rolling_avs['points'].rolling(window=14).mean()
#df_rolling_avs['points_rolling_mean'] = df_rolling_avs['points'].rolling(window=14, step=7).mean()



"""
'''new attempt '''
df_player_game_stats.columns
"""
"""
''' old attempt '''
########## aaaaahhhhhhhhhhhhhhhhh it stores them the opposite way
dates = pd.date_range(start=df_player_game_stats['gameDate'].iloc[-1], end=df_player_game_stats['gameDate'].iloc[0], freq="D")

reversed_df_player_game_stats = df_player_game_stats[::-1].reset_index(drop=True)
dates = pd.date_range(start=reversed_df_player_game_stats['gameDate'].iloc[0], end=reversed_df_player_game_stats['gameDate'].iloc[-1], freq="D")

df_dates = pd.DataFrame(index=dates)

reversed_df_player_game_stats_all_dates = pd.concat([df_dates, reversed_df_player_game_stats], axis=1)


reversed_df_player_game_stats_date_index = reversed_df_player_game_stats_all_dates[['gameDate', 'goals', 'assists']]
reversed_df_player_game_stats_date_index = reversed_df_player_game_stats_date_index.set_index('gameDate').sort_index()

df_clean = reversed_df_player_game_stats_date_index[reversed_df_player_game_stats_date_index.index.notnull()]

df_clean['rolling_avg_3d'] = df_clean['goals'].rolling(window='3D').mean()



reversed_df_player_game_stats_date_index = reversed_df_player_game_stats_all_dates[['gameDate', 'goals', 'assists']]
reversed_df_player_game_stats_date_index = reversed_df_player_game_stats_date_index.set_index('gameDate')

df_clean = reversed_df_player_game_stats_date_index[reversed_df_player_game_stats_date_index.index.notnull()]

"""



## irregular sampling might be causing errors?

# 2. Resample to the overlap frequency (1 week) using the weekly mean
# 'W' handles the 1-week step/overlap interval
weekly_resampled = df.resample("W").mean()

# 3. Apply a rolling window of 2 periods (2 weeks total)
# window=2 over weekly resampled data sums up to a 14-day window
two_week_rolling_avg = weekly_resampled.rolling(window=2).mean()




# test
df_player_game_stats['gameDate'] = pd.to_datetime(df_player_game_stats['gameDate'])





"""
In [4]: df_player_game_stats["gameDate"]
Out[4]:
0     2026-04-16
1     2026-04-15
2     2026-04-13
3     2026-04-11
4     2026-04-09
         ...
77    2025-10-18
78    2025-10-17
79    2025-10-14
80    2025-10-11
81    2025-10-09
Name: gameDate, Length: 82, dtype: str
"""



# end script
