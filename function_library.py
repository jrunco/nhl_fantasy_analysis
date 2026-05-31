
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



def load_summary_statistics_for_skaters(season_start, season_end, limit: int = 100):
    #from nhlpy.api.query.builder import QueryBuilder, QueryContext
    #from nhlpy.api.query.filters.season import SeasonQuery
    #from nhlpy.api.query.filters.game_type import GameTypeQuery

    filters = [
    SeasonQuery(season_start=season_start, season_end=season_end),
    GameTypeQuery(game_type="2"),
    #OpponentQuery(opponent_franchise_id="2"),
    ]
    context: QueryContext = QueryBuilder().build(filters=filters)
    all_data = []
    start = 0

    client = NHLClient(debug=False)

    while True:
        response = client.stats.skater_stats_with_query_context(
            report_type='summary',
            query_context=context,
            aggregate=True,
            limit=limit,
            start=start
        )

        total = response['total']
        batch_data = response['data']
        all_data.extend(batch_data)

        if len(all_data) >= total:
            break

        start += limit

    return all_data


def load_realtime_statistics_for_skaters(season_start, season_end, limit: int = 100):

    filters = [
    SeasonQuery(season_start=season_start, season_end=season_end),
    GameTypeQuery(game_type="2"),
    #OpponentQuery(opponent_franchise_id="2"),
    ]
    context: QueryContext = QueryBuilder().build(filters=filters)
    all_data = []
    start = 0

    client = NHLClient(debug=False)

    while True:
        response = client.stats.skater_stats_with_query_context(
            report_type='realtime',
            query_context=context,
            aggregate=True,
            limit=limit,
            start=start
        )

        total = response['total']
        batch_data = response['data']
        all_data.extend(batch_data)

        if len(all_data) >= total:
            break

        start += limit

    return all_data


def load_faceoffwins_statistics_for_skaters(season_start, season_end, limit: int = 100):

    filters = [
    SeasonQuery(season_start=season_start, season_end=season_end),
    GameTypeQuery(game_type="2"),
    #OpponentQuery(opponent_franchise_id="2"),
    ]
    context: QueryContext = QueryBuilder().build(filters=filters)
    all_data = []
    start = 0

    client = NHLClient(debug=False)

    while True:
        response = client.stats.skater_stats_with_query_context(
            report_type='faceoffwins',
            query_context=context,
            aggregate=True,
            limit=limit,
            start=start
        )

        total = response['total']
        batch_data = response['data']
        all_data.extend(batch_data)

        if len(all_data) >= total:
            break

        start += limit

    return all_data


def skater_single_season_fantasy_points(skater_name,
    season,
    fantasy_points_goals,
    fantasy_points_assists,
    fantasy_points_plusminus,
    fantasy_points_pp_goals,
    fantasy_points_pp_asists,
    fantasy_points_sh_goals,
    fantasy_points_sh_assists,
    fantasy_points_game_winning_goals,
    fantasy_points_shots,
    fantasy_points_hits,
    fantasy_points_blocks,
    fantasy_points_fowins,
    fantasy_points_folosses,
    fantasy_points_pims,
    ):

    skater_to_grab = skater_name

    start_season = season
    end_season = season

    fantasy_goals = float(fantasy_points_goals)
    fantasy_assists = float(fantasy_points_assists)
    fantasy_plusminus = float(fantasy_points_plusminus)
    fantasy_pp_goals = float(fantasy_points_pp_goals)
    fantasy_pp_assists = float(fantasy_points_pp_asists)
    fantasy_sh_goals = float(fantasy_points_sh_goals)
    fantasy_sh_assists = float(fantasy_points_sh_assists)
    fantasy_game_winning_goals = float(fantasy_points_game_winning_goals)
    fantasy_shots = float(fantasy_points_shots)
    fantasy_hits = float(fantasy_points_hits)
    fantasy_blocks = float(fantasy_points_blocks)
    fantasy_fowins = float(fantasy_points_fowins)
    fantasy_folosses = float(fantasy_points_folosses)
    fantasy_pims = float(fantasy_points_pims)

    # do an initial query to see if player name exists

    skater_summary_query = load_summary_statistics_for_skaters(start_season, end_season)
    skater_realtime_query = load_realtime_statistics_for_skaters(start_season, end_season)
    skater_faceoffwins_query = load_faceoffwins_statistics_for_skaters(start_season, end_season)

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
        print("%s fantasy points = %s" % (name_grabbed, tot_fantasy_points))
    return tot_fantasy_points
