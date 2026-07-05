import numpy as np
import pandas as pd

#from nhlpy import NHLClient

"""
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
"""
# my custom functions
from function_library import load_summary_statistics_for_skaters
from function_library import load_realtime_statistics_for_skaters
from function_library import load_faceoffwins_statistics_for_skaters
from function_library import skater_single_season_fantasy_points

"""
#### fantasy points ####
fantasy_goals = 6.0
fantasy_assists = 4.0
fantasy_plusminus = 1.5
fantasy_pp_goals = 2.0
fantasy_pp_assists = 2.0
fantasy_sh_goals = 3.0
fantasy_sh_assists = 1.0
fantasy_game_winning_goals = 1.0
fantasy_shots = 0.75
fantasy_hits = 0.4
fantasy_blocks = 1.25
fantasy_fowins = 0.15
fantasy_folosses = -0.15
fantasy_pims = 0.0
"""


skater_single_season_fantasy_points(
    "Macklin Celebrini",
    #"Morgan Geekie",
    "20252026",
    6.0,
    4.0,
    1.5,
    2.0,
    2.0,
    3.0,
    1.0,
    1.0,
    0.75,
    0.4,
    1.25,
    0.15,
    -0.15,
    0.0,
    )



## not a function
"""
start_season = "20252026"
end_season = "20252026"

skater_summary_query = load_summary_statistics_for_skaters(start_season, end_season)
skater_realtime_query = load_realtime_statistics_for_skaters(start_season, end_season)
skater_faceoffwins_query = load_faceoffwins_statistics_for_skaters(start_season, end_season)

skater_to_grab = "Macklin Celebrin"
#skater_to_grab = "Connor McDavid"

name_grabbed = "N/A"
for i in range(len(skater_summary_query)):
    if skater_summary_query[i]["skaterFullName"] == skater_to_grab:
        name_grabbed = skater_summary_query[i]["skaterFullName"]
        season_gamesPlayed = skater_summary_query[i]["gamesPlayed"]
        season_goals = skater_summary_query[i]["goals"]
        season_assists = skater_summary_query[i]["assists"]
        season_plusMinus = skater_summary_query[i]["plusMinus"]
        season_ppGoals = skater_summary_query[i]["ppGoals"]
        season_ppAssists = skater_summary_query[i]["ppPoints"] - skater_summary_query[i]["ppGoals"]
        season_shGoals = skater_summary_query[i]["shGoals"]
        season_shAssists = skater_summary_query[i]["shPoints"] - skater_summary_query[i]["shGoals"]
        season_gameWinningGoals = skater_summary_query[i]["gameWinningGoals"]
        season_shots = skater_summary_query[i]["shots"]
        season_penaltyMinutes = skater_summary_query[i]["penaltyMinutes"]

for i in range(len(skater_realtime_query)):
    if skater_realtime_query[i]["skaterFullName"] == skater_to_grab:
        #name_grabbed = skater_realtime_query[i]["skaterFullName"]
        season_blockedShots = skater_realtime_query[i]["blockedShots"]
        season_hits = skater_realtime_query[i]["hits"]

for i in range(len(skater_faceoffwins_query)):
    if skater_faceoffwins_query[i]["skaterFullName"] == skater_to_grab:
        #name_grabbed = skater_faceoffwins_query[i]["skaterFullName"]
        season_totalFaceoffWins = skater_faceoffwins_query[i]["totalFaceoffWins"]
        season_totalFaceoffLosses = skater_faceoffwins_query[i]["totalFaceoffLosses"]

if name_grabbed == "N/A":
    print("Skater not found == user spell more gooder")
else:
    tot_fantasy_points = (season_goals*fantasy_goals
        + season_assists*fantasy_assists
        + season_plusMinus*fantasy_plusminus
        + season_ppGoals*fantasy_pp_goals
        + season_ppAssists*fantasy_pp_assists
        + season_shGoals*fantasy_sh_goals
        + season_shAssists*fantasy_sh_assists
        + season_gameWinningGoals*fantasy_game_winning_goals
        + season_shots*fantasy_shots
        + season_hits*fantasy_hits
        + season_blockedShots*fantasy_blocks
        + season_totalFaceoffWins*fantasy_fowins
        + season_totalFaceoffLosses*fantasy_folosses
        + season_penaltyMinutes*fantasy_pims
        )
        #season_goals*fantasy_goals +
        #season_goals*fantasy_goals +
    print("%s fantasy points = %s" % (name_grabbed, tot_fantasy_points))
"""


"""
report_type = summary

{'assists': 90,
 'evGoals': 34,
 'evPoints': 82,
 'faceoffWinPct': 0.49512,
 'gameWinningGoals': 4,
 'gamesPlayed': 82,
 'goals': 48,
 'lastName': 'McDavid',
 'otGoals': 1,
 'penaltyMinutes': 44,
 'playerId': 8478402,
 'plusMinus': 17,
 'points': 138,
 'pointsPerGame': 1.68292,
 'positionCode': 'C',
 'ppGoals': 13,
 'ppPoints': 54,
 'shGoals': 1,
 'shPoints': 2,
 'shootingPct': 0.15686,
 'shootsCatches': 'L',
 'shots': 306,
 'skaterFullName': 'Connor McDavid',
 'timeOnIcePerGame': 1379.1219}
"""

"""
report_type = realtime
{'blockedShots': 39,
 'blockedShotsPer60': 2.14,
 'emptyNetAssists': 0,
 'emptyNetGoals': 0,
 'emptyNetPoints': 0,
 'firstGoals': 0,
 'gamesPlayed': 82,
 'giveaways': 63,
 'giveawaysPer60': 3.47,
 'hits': 413,
 'hitsPer60': 22.75,
 'lastName': 'Trenin',
 'missedShotCrossbar': 0,
 'missedShotFailedBankAttempt': 5,
 'missedShotGoalpost': 4,
 'missedShotOverNet': 5,
 'missedShotShort': 3,
 'missedShotWideOfNet': 43,
 'missedShots': 60,
 'otGoals': 0,
 'playerId': 8478508,
 'positionCode': 'C',
 'shootsCatches': 'L',
 'shotAttemptsBlocked': 33,
 'skaterFullName': 'Yakov Trenin',
 'takeaways': 24,
 'takeawaysPer60': 1.32,
 'timeOnIcePerGame': 796.9,
 'totalShotAttempts': 191}
"""
