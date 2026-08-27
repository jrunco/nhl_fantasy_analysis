import numpy as np
import pandas as pd
from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns

from tabulate import tabulate
from prettytable import PrettyTable, TableStyle

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

# custom functions from this repo
from utils.function_library import find_player_id
from utils.function_library import toi_string_to_float
from utils.function_library import load_summary_statistics_for_skaters
from utils.function_library import load_realtime_statistics_for_skaters
from utils.function_library import load_faceoffwins_statistics_for_skaters
from utils.function_library import skater_single_season_fantasy_points
from utils.function_library import get_stats_by_season
from utils.function_library import plot_stat_per_game
from utils.function_library import home_away_split

from matplotlib import rc
plt.rcParams.update({'font.size':22})


fp_goals = 6.0
fp_assists = 4.0
fp_plusminus = 1.5
fp_pp_goals = 2.0
fp_pp_assists = 2.0
fp_sh_goals = 4.0
fp_sh_assists = 1.0
fp_game_winning_goals = 1.0
fp_shots = 0.75
fp_hits = 0.40
fp_blocks = 1.25
fp_fowins = 0.15
fp_folosses = -0.15
fp_pims = 0.0

season = "20252026"
start_season = "20252026"
end_season = "20252026"

skater1_name = "Tyler Toffoli"
skater1_id = find_player_id(skater1_name, season)

skater2_name = "Will Smith"
skater2_id = find_player_id(skater2_name, season)


# grab all stats
skater_summary_query = load_summary_statistics_for_skaters(start_season, end_season)
skater_realtime_query = load_realtime_statistics_for_skaters(start_season, end_season)
skater_faceoffwins_query = load_faceoffwins_statistics_for_skaters(start_season, end_season)

skater1_name_grabbed = "N/A"
skater2_name_grabbed = "N/A"
for i in range(len(skater_summary_query)):
    if skater_summary_query[i]["skaterFullName"] == skater1_name:
        skater1_name_grabbed = skater_summary_query[i]["skaterFullName"]
        skater1_season_gamesPlayed = skater_summary_query[i]["gamesPlayed"]
        skater1_season_goals = skater_summary_query[i]["goals"]
        skater1_season_assists = skater_summary_query[i]["assists"]
        skater1_season_plusMinus = skater_summary_query[i]["plusMinus"]
        skater1_season_ppGoals = skater_summary_query[i]["ppGoals"]
        skater1_season_ppAssists = skater_summary_query[i]["ppPoints"] - skater_summary_query[i]["ppGoals"]
        skater1_season_shGoals = skater_summary_query[i]["shGoals"]
        skater1_season_shAssists = skater_summary_query[i]["shPoints"] - skater_summary_query[i]["shGoals"]
        skater1_season_gameWinningGoals = skater_summary_query[i]["gameWinningGoals"]
        skater1_season_shots = skater_summary_query[i]["shots"]
        skater1_season_penaltyMinutes = skater_summary_query[i]["penaltyMinutes"]
    elif skater_summary_query[i]["skaterFullName"] == skater2_name:
        skater2_name_grabbed = skater_summary_query[i]["skaterFullName"]
        skater2_season_gamesPlayed = skater_summary_query[i]["gamesPlayed"]
        skater2_season_goals = skater_summary_query[i]["goals"]
        skater2_season_assists = skater_summary_query[i]["assists"]
        skater2_season_plusMinus = skater_summary_query[i]["plusMinus"]
        skater2_season_ppGoals = skater_summary_query[i]["ppGoals"]
        skater2_season_ppAssists = skater_summary_query[i]["ppPoints"] - skater_summary_query[i]["ppGoals"]
        skater2_season_shGoals = skater_summary_query[i]["shGoals"]
        skater2_season_shAssists = skater_summary_query[i]["shPoints"] - skater_summary_query[i]["shGoals"]
        skater2_season_gameWinningGoals = skater_summary_query[i]["gameWinningGoals"]
        skater2_season_shots = skater_summary_query[i]["shots"]
        skater2_season_penaltyMinutes = skater_summary_query[i]["penaltyMinutes"]

for i in range(len(skater_realtime_query)):
    if skater_realtime_query[i]["skaterFullName"] == skater1_name:
        #skater1_name_grabbed = skater_realtime_query[i]["skaterFullName"]
        skater1_season_blockedShots = skater_realtime_query[i]["blockedShots"]
        skater1_season_hits = skater_realtime_query[i]["hits"]
    elif skater_realtime_query[i]["skaterFullName"] == skater2_name:
        #skater2_name_grabbed = skater_realtime_query[i]["skaterFullName"]
        skater2_season_blockedShots = skater_realtime_query[i]["blockedShots"]
        skater2_season_hits = skater_realtime_query[i]["hits"]

for i in range(len(skater_faceoffwins_query)):
    if skater_faceoffwins_query[i]["skaterFullName"] == skater1_name:
        #skater1_name_grabbed = skater_faceoffwins_query[i]["skaterFullName"]
        skater1_season_totalFaceoffWins = skater_faceoffwins_query[i]["totalFaceoffWins"]
        skater1_season_totalFaceoffLosses = skater_faceoffwins_query[i]["totalFaceoffLosses"]
    elif skater_faceoffwins_query[i]["skaterFullName"] == skater2_name:
        #skater1_name_grabbed = skater_faceoffwins_query[i]["skaterFullName"]
        skater2_season_totalFaceoffWins = skater_faceoffwins_query[i]["totalFaceoffWins"]
        skater2_season_totalFaceoffLosses = skater_faceoffwins_query[i]["totalFaceoffLosses"]

if skater1_name_grabbed == "N/A":
    print("Skater 1 not found: error in defining player name or season")
elif skater2_name_grabbed == "N/A":
    print("Skater 2 not found: error in defining player name or season")
else:
    skater1_tot_fantasy_points = (skater1_season_goals*fp_goals
        + skater1_season_assists*fp_assists
        + skater1_season_plusMinus*fp_plusminus
        + skater1_season_ppGoals*fp_pp_goals
        + skater1_season_ppAssists*fp_pp_assists
        + skater1_season_shGoals*fp_sh_goals
        + skater1_season_shAssists*fp_sh_assists
        + skater1_season_gameWinningGoals*fp_game_winning_goals
        + skater1_season_shots*fp_shots
        + skater1_season_hits*fp_hits
        + skater1_season_blockedShots*fp_blocks
        + skater1_season_totalFaceoffWins*fp_fowins
        + skater1_season_totalFaceoffLosses*fp_folosses
        + skater1_season_penaltyMinutes*fp_pims
        )
    skater2_tot_fantasy_points = (skater2_season_goals*fp_goals
        + skater2_season_assists*fp_assists
        + skater2_season_plusMinus*fp_plusminus
        + skater2_season_ppGoals*fp_pp_goals
        + skater2_season_ppAssists*fp_pp_assists
        + skater2_season_shGoals*fp_sh_goals
        + skater2_season_shAssists*fp_sh_assists
        + skater2_season_gameWinningGoals*fp_game_winning_goals
        + skater2_season_shots*fp_shots
        + skater2_season_hits*fp_hits
        + skater2_season_blockedShots*fp_blocks
        + skater2_season_totalFaceoffWins*fp_fowins
        + skater2_season_totalFaceoffLosses*fp_folosses
        + skater2_season_penaltyMinutes*fp_pims
        )


# TODO
# try to find a way to highlight which stat is better (probably choose stat #/game over total stat #)
# try an if statement for each group of rows (goals, assists, etc. to highlight the better player's column)
# table columns cannot repeat names
# can grab timeOnIcePerGame from the load_summary_statistics_for_skaters() to get stat/60 minutes

table = PrettyTable(['Category', '%s' % (skater1_name), '%s' % (skater2_name)])#, 'Stats / Game', 'Fantasy Points / Game'])
table.title = "Goals"
if skater1_season_goals/skater1_season_gamesPlayed == skater2_season_goals/skater2_season_gamesPlayed:
    table.add_row(['Total Goals (Fantasy Points)', "%s (%s)" % (skater1_season_goals, round((skater1_season_goals*fp_goals), 2)), "%s (%s)" % (skater2_season_goals, round((skater2_season_goals*fp_goals), 2))])
    table.add_row(['Goals/Game (Fantasy Points / Game)', "%s (%s)" % (round(skater1_season_goals/skater1_season_gamesPlayed, 2), round((skater1_season_goals*fp_goals)/skater1_season_gamesPlayed, 2)), "%s (%s)" % (round(skater2_season_goals/skater2_season_gamesPlayed, 2), round((skater2_season_goals*fp_goals)/skater2_season_gamesPlayed, 2))])
elif()
table.add_row(['Total Goals (Fantasy Points)', "%s (%s)" % (skater1_season_goals, round((skater1_season_goals*fp_goals), 2)), "%s (%s)" % (skater2_season_goals, round((skater2_season_goals*fp_goals), 2))])
table.add_row(['Goals/Game (Fantasy Points / Game)', "%s (%s)" % (round(skater1_season_goals/skater1_season_gamesPlayed, 2), round((skater1_season_goals*fp_goals)/skater1_season_gamesPlayed, 2)), "%s (%s)" % (round(skater2_season_goals/skater2_season_gamesPlayed, 2), round((skater2_season_goals*fp_goals)/skater2_season_gamesPlayed, 2))])
#table.add_divider()
#table.add_row(['Total Goals (Fantasy Points) per game', round((skater1_season_goals*fp_goals), 2), round((skater2_season_goals*fp_goals), 2)])
print(table)





table = PrettyTable(['Category', '%s' % (skater1_name), '%s' % (skater2_name)])#, 'Stats / Game', 'Fantasy Points / Game'])
table.title = "Goals"
table.add_row(['Total Goals (Fantasy Points)', "%s (%s)" % (skater1_season_goals, round((skater1_season_goals*fp_goals), 2)), "%s (%s)" % (skater2_season_goals, round((skater2_season_goals*fp_goals), 2))])
table.add_row(['Total Goals (Fantasy Points)', "%s (%s)" % (skater1_season_goals, round((skater1_season_goals*fp_goals), 2)), "%s (%s)" % (skater2_season_goals, round((skater2_season_goals*fp_goals), 2))])
#table.add_divider()
#table.add_row(['Total Goals (Fantasy Points) per game', round((skater1_season_goals*fp_goals), 2), round((skater2_season_goals*fp_goals), 2)])
print(table)

'''
table = PrettyTable(['Category', '%s' % (skater1_name), 'Stat Total', '# of Fantasy Points', '%s' % (skater2_name), 'Stat Total', '# of Fantasy Points'])#, 'Stats / Game', 'Fantasy Points / Game'])
table.title = "Fantasy Points Breakdown by Stat"
table.add_row(['Goals', 0, skater1_season_goals, round((skater1_season_goals*fp_goals), 2), 0, skater2_season_goals, round((skater2_season_goals*fp_goals), 2)])
print(table)
'''
### i can do stats per game and fantasy points per game for each of these because i know the number of games played
'''
table = PrettyTable(['Category', '%s' % (skater_name), 'Stat Total', '# of Fantasy Points', '%s' % (skater2_name), 'Stat Total', '# of Fantasy Points'])#, 'Stats / Game', 'Fantasy Points / Game'])
table.title = "Fantasy Points Breakdown by Stat"
table.add_row(['Goals', season_goals, round((season_goals*fantasy_goals), 2), round(season_goals/season_gamesPlayed, 2), round((season_goals*fantasy_goals)/season_gamesPlayed, 2)])
print(table)
'''

# i can use the game_log function to get some stats like goals, assists, etc. over a specified date range within a season
# i cannot use the game_log function to get other stats like hits, blocks, etc. over a specified date range within a season


"""
tot_fp = skater_single_season_fantasy_points(skater_name,
    season,
    fp_goals,
    fp_assists,
    fp_plusminus,
    fp_pp_goals,
    fp_pp_asists,
    fp_sh_goals,
    fp_sh_assists,
    fp_game_winning_goals,
    fp_shots,
    fp_hits,
    fp_blocks,
    fp_fowins,
    fp_folosses,
    fp_pims,
    )

tot_fp2 = skater_single_season_fantasy_points(skater2_name,
    season,
    fp_goals,
    fp_assists,
    fp_plusminus,
    fp_pp_goals,
    fp_pp_asists,
    fp_sh_goals,
    fp_sh_assists,
    fp_game_winning_goals,
    fp_shots,
    fp_hits,
    fp_blocks,
    fp_fowins,
    fp_folosses,
    fp_pims,
    )



table = PrettyTable(['Category', '%s' % (skater_name), 'Stat Total', '# of Fantasy Points', '%s' % (skater2_name), 'Stat Total', '# of Fantasy Points'])#, 'Stats / Game', 'Fantasy Points / Game'])
table.title = "Fantasy Points Breakdown by Stat"
table.add_row(['Goals', season_goals, round((season_goals*fantasy_goals), 2), round(season_goals/season_gamesPlayed, 2), round((season_goals*fantasy_goals)/season_gamesPlayed, 2)])
print(table)
"""
