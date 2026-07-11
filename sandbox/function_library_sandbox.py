
import numpy as np
import pandas as pd

import seaborn as sns
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
        print("Skater not found: error in defining player name or season")
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


def get_stats_by_season(player_id):

    client = NHLClient(debug=False)

    # define player
    career_stats = client.stats.player_career_stats(player_id=player_id)  # "8478402" = Connor McDavid

    # set up dataframe
    df_nhl_rs_career_stats = pd.DataFrame(career_stats["seasonTotals"])
    df_nhl_rs_career_stats = df_nhl_rs_career_stats[df_nhl_rs_career_stats["leagueAbbrev"] == "NHL"]
    df_nhl_rs_career_stats = df_nhl_rs_career_stats[df_nhl_rs_career_stats["gameTypeId"] == 2]
    df_nhl_rs_career_stats = df_nhl_rs_career_stats.reset_index(drop=True)

    # calculate pp_asists and sh_assists and add them to the stats/game below
    df_nhl_rs_career_stats["powerPlayAssists"] = df_nhl_rs_career_stats["powerPlayPoints"] - df_nhl_rs_career_stats["powerPlayGoals"]
    df_nhl_rs_career_stats["shorthandedAssists"] = df_nhl_rs_career_stats["shorthandedPoints"] - df_nhl_rs_career_stats["shorthandedGoals"]

    # calculate even strength stats
    df_nhl_rs_career_stats["even_strength_goals"] = df_nhl_rs_career_stats["goals"] - (df_nhl_rs_career_stats["powerPlayGoals"] + df_nhl_rs_career_stats["shorthandedGoals"])
    df_nhl_rs_career_stats["even_strength_assists"] = df_nhl_rs_career_stats["assists"] - (df_nhl_rs_career_stats["powerPlayAssists"] + df_nhl_rs_career_stats["shorthandedAssists"])
    df_nhl_rs_career_stats["even_strength_points"] = df_nhl_rs_career_stats["points"] - (df_nhl_rs_career_stats["powerPlayPoints"] + df_nhl_rs_career_stats["shorthandedPoints"])

    ## get stats/game
    df_nhl_rs_career_stats["assists_per_game"] = df_nhl_rs_career_stats["assists"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["goals_per_game"] = df_nhl_rs_career_stats["goals"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["points_per_game"] = df_nhl_rs_career_stats["points"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["powerPlayGoals_per_game"] = df_nhl_rs_career_stats["powerPlayGoals"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["powerPlayAssists_per_game"] = df_nhl_rs_career_stats["powerPlayAssists"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["powerPlayPoints_per_game"] = df_nhl_rs_career_stats["powerPlayPoints"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["shorthandedGoals_per_game"] = df_nhl_rs_career_stats["shorthandedGoals"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["shorthandedAssists_per_game"] = df_nhl_rs_career_stats["shorthandedAssists"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["shorthandedPoints_per_game"] = df_nhl_rs_career_stats["shorthandedPoints"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["even_strength_goals_per_game"] = df_nhl_rs_career_stats["even_strength_goals"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["even_strength_assists_per_game"] = df_nhl_rs_career_stats["even_strength_assists"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["even_strength_points_per_game"] = df_nhl_rs_career_stats["even_strength_points"]/df_nhl_rs_career_stats["gamesPlayed"]
    df_nhl_rs_career_stats["shots_per_game"] = df_nhl_rs_career_stats["shots"]/df_nhl_rs_career_stats["gamesPlayed"]

    # define season start
    df_nhl_rs_career_stats["season_label"] = df_nhl_rs_career_stats['season']
    df_nhl_rs_career_stats['season_label'] = df_nhl_rs_career_stats['season_label'].astype('string')
    df_nhl_rs_career_stats["season_label"] = df_nhl_rs_career_stats['season_label'].str[:4]

    # get team name
    teams = pd.DataFrame(df_nhl_rs_career_stats["teamName"]) # df_nhl_rs_career_stats['teamCommonName'] gives just the team name (e.g., sharks)
    # might have to do for loop...
    team_names = []
    for i in range(len(teams)):
        team_names.append(teams["teamName"][i]["default"])
    team_names = np.array(team_names)
    df_nhl_rs_career_stats["team_names"] = team_names

    df_nhl_rs_career_stats = df_nhl_rs_career_stats.drop(columns=['teamName', 'teamCommonName', 'teamPlaceNameWithPreposition'])

    # convert avgToi from a string to a float
    minutes = np.zeros(len(df_nhl_rs_career_stats))
    seconds = np.zeros(len(df_nhl_rs_career_stats))
    for i in range(len(df_nhl_rs_career_stats)):
        minutes[i], seconds[i] = map(int, df_nhl_rs_career_stats["avgToi"].values[i].split(":"))
    df_nhl_rs_career_stats["avgToi_float"] = minutes + (seconds / 60.)

    return df_nhl_rs_career_stats


def plot_stat_per_game(ax, ax_str, df, include_avg, stat, title, ylabel):

    if ax_str == "ax1":
        sns.scatterplot(data=df, x="season", y=stat, s=200, hue="team_names", ax=ax, zorder=100)
    else:
        sns.scatterplot(data=df, x="season", y=stat, s=200, hue="team_names", ax=ax, legend=False, zorder=100)
    #sns._legend.set_title("Team Names")

    if include_avg:
        ax.axhline(y=np.mean(df[stat]), color='tab:green', linewidth=8, zorder=10)
        #plt.axhline(y=np.mean(df["goals"][1:]), color='tab:green', linewidth=2) # this would exclude their rookie season from the average

        ax.axhline(y=np.mean(df[stat])+np.std(df[stat]), color='tab:green', linestyle='--', linewidth=4, zorder=10)
        ax.axhline(y=np.mean(df[stat])-np.std(df[stat]), color='tab:green', linestyle='--', linewidth=4, zorder=10)
        ax.fill_between(df["season"], np.mean(df[stat])+np.std(df[stat]),
            np.mean(df[stat])-np.std(df[stat]), color="gray", alpha=0.3, zorder=1)

    ax.set_title(title)
    ax.set_xlabel("Season")
    ax.set_ylabel(ylabel)
    ax.set_xticks(df["season"], df["season_label"])
    ax.tick_params(axis='x', labelrotation=45)
    if ax_str == "ax1":
        # simple legend
        #ax.legend(frameon=False)

        # fancier legend. need plt.subplots adjust for this one
        #ax.legend(loc='upper center', frameon=False, bbox_to_anchor(0.5, 1.02), ncols=4)
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncols=2, mode="expand", borderaxespad=1.)
    #plt.subplots_adjust(top=0.90)
    #plt.show()
"""
def plot_stat_per_game(df, stat, title, ylabel):

    g = sns.lmplot(data=df, x="season", y=stat, hue="team_names", fit_reg=False, ci=None)#, zorder=100)
    g._legend.set_title("Team Names")

    plt.axhline(y=np.mean(df[stat]), color='tab:green', linewidth=2, zorder=10)
    #plt.axhline(y=np.mean(df["goals"][1:]), color='tab:green', linewidth=2) # this would exclude their rookie season from the average

    plt.axhline(y=np.mean(df[stat])+np.std(df[stat]), color='tab:green', linestyle='--', linewidth=1, zorder=10)
    plt.axhline(y=np.mean(df[stat])-np.std(df[stat]), color='tab:green', linestyle='--', linewidth=1, zorder=10)
    plt.fill_between(df["season"], np.mean(df[stat])+np.std(df[stat]),
        np.mean(df[stat])-np.std(df[stat]), color="gray", alpha=0.3, zorder=1)

    plt.title(title)
    plt.xlabel("Season")
    plt.ylabel(ylabel)
    plt.xticks(df["season"], df["season_label"])
    plt.xticks(rotation=45)
    #plt.show()
"""
