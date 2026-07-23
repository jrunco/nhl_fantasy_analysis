
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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


def toi_string_to_float(df, str_param_name, float_param_name):

    # convert avgToi from a string to a float
    minutes = np.zeros(len(df))
    seconds = np.zeros(len(df))
    for i in range(len(df)):
        minutes[i], seconds[i] = map(int, df[str_param_name].values[i].split(":"))
    df[float_param_name] = minutes + (seconds / 60.)

    return df


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
        print(" ")
        print("# of games played = %s" % (season_gamesPlayed))
        print("Fantasy points per game = %s" % ((tot_fantasy_points/season_gamesPlayed)))
        print(" ")
        print(" ")
        table = PrettyTable(['Stat Name', 'Total Stats', 'Fantasy Points', 'Stats / Game', 'Fantasy Points / Game'])
        table.title = "Fantasy Points Breakdown by Stat"
        table.add_row(['Goals', season_goals, round((season_goals*fantasy_goals), 2), round(season_goals/season_gamesPlayed, 2), round((season_goals*fantasy_goals)/season_gamesPlayed, 2)])
        table.add_row(['Assists', season_assists, round((season_assists*fantasy_assists), 2), round(season_assists/season_gamesPlayed, 2), round((season_assists*fantasy_assists)/season_gamesPlayed, 2)])
        table.add_row(['Plus/Minus', season_plusMinus, round((season_plusMinus*fantasy_plusminus), 2), round(season_plusMinus/season_gamesPlayed, 2), round((season_plusMinus*fantasy_plusminus)/season_gamesPlayed, 2)])
        table.add_row(['Bonus for PP Goals', season_ppGoals, round((season_ppGoals*fantasy_pp_goals), 2), round(season_ppGoals/season_gamesPlayed, 2), round((season_ppGoals*fantasy_pp_goals)/season_gamesPlayed, 2)])
        table.add_row(['Bonus for PP Assists', season_ppAssists, round((season_ppAssists*fantasy_pp_assists), 2), round(season_ppAssists/season_gamesPlayed, 2), round((season_ppAssists*fantasy_pp_assists)/season_gamesPlayed, 2)])
        table.add_row(['Bonus for SH Goals', season_shGoals, round((season_shGoals*fantasy_sh_goals), 2), round(season_shGoals/season_gamesPlayed, 2), round((season_shGoals*fantasy_sh_goals)/season_gamesPlayed, 2)])
        table.add_row(['Bonus for SH Assists', season_shAssists, round((season_shAssists*fantasy_sh_assists), 2), round(season_shAssists/season_gamesPlayed, 2), round((season_shAssists*fantasy_sh_assists)/season_gamesPlayed, 2)])
        table.add_row(['Bonus for Game Winning Goals', season_gameWinningGoals, round((season_gameWinningGoals*fantasy_game_winning_goals), 2), round(season_gameWinningGoals/season_gamesPlayed, 2), round((season_gameWinningGoals*fantasy_game_winning_goals)/season_gamesPlayed, 2)])
        table.add_row(['Shots', season_shots, round((season_shots*fantasy_shots), 2), round(season_shots/season_gamesPlayed, 2), round((season_shots*fantasy_shots)/season_gamesPlayed, 2)])
        table.add_row(['Hits', season_hits, round((season_hits*fantasy_hits), 2), round(season_hits/season_gamesPlayed, 2), round((season_hits*fantasy_hits)/season_gamesPlayed, 2)])
        table.add_row(['Blocks', season_blockedShots, round((season_blockedShots*fantasy_blocks), 2), round(season_blockedShots/season_gamesPlayed, 2), round((season_blockedShots*fantasy_blocks)/season_gamesPlayed, 2)])
        table.add_row(['Face-offs', (season_totalFaceoffWins-season_totalFaceoffLosses), round(((season_totalFaceoffWins*fantasy_fowins)+(season_totalFaceoffLosses*fantasy_folosses)), 2), round((season_totalFaceoffWins-season_totalFaceoffLosses)/season_gamesPlayed, 2), round(((season_totalFaceoffWins*fantasy_fowins)+(season_totalFaceoffLosses*fantasy_folosses))/season_gamesPlayed, 2)])
        table.add_row(['PIMs', season_penaltyMinutes, round((season_penaltyMinutes*fantasy_pims), 2), round(season_penaltyMinutes/season_gamesPlayed, 2), round((season_penaltyMinutes*fantasy_pims)/season_gamesPlayed, 2)])
        #table.add_divider()
        #table.set_style(DOUBLE_BORDER)
        print(table)

    return tot_fantasy_points


def get_stats_by_season(player_id, path_to_team_images):

    path_to_images = path_to_team_images

    images = {
        "Anaheim Ducks": path_to_images+"anaheim_ducks.png",
        "Boston Bruins": path_to_images+"boston_bruins.png",
        "Buffalo Sabres": path_to_images+"buffalo_sabres.png",
        "Calgary Flames": path_to_images+"calgary_flames.png",
        "Carolina Hurricanes": path_to_images+"carolina_hurricanes.png",
        "Chicago Blackhawks": path_to_images+"chicago_blackhawks.png",
        "Colorado Avalanche": path_to_images+"colorado_avalanche.png",
        "Columbus Blue Jackets": path_to_images+"columbus_blue_jackets.png",
        "Dallas Stars": path_to_images+"dallas_stars.png",
        "Detroit Red Wings": path_to_images+"detroit_red_wings.png",
        "Edmonton Oilers": path_to_images+"edmonton_oilers.png",
        "Florida Panthers": path_to_images+"florida_panthers.png",
        "Los Angeles Kings": path_to_images+"los_angeles_kings.png",
        "Minnesota Wild": path_to_images+"minnesota_wild.png",
        "Montréal Canadiens": path_to_images+"montreal_canadiens.png",
        "Nashville Predators": path_to_images+"nashville_predators.png",
        "New Jersey Devils": path_to_images+"new_jersey_devils.png",
        "New York Islanders": path_to_images+"new_york_islanders.png",
        "New York Rangers": path_to_images+"new_york_rangers.png",
        "Ottawa Senators": path_to_images+"ottawa_senators.png",
        "Philadelphia Flyers": path_to_images+"philadelphia_flyers.png",
        "Pittsburgh Penguins": path_to_images+"pittsburgh_penguins.png",
        "San Jose Sharks": path_to_images+"san_jose_sharks.png",
        "Seattle Kraken": path_to_images+"seattle_kraken.png",
        "St. Louis Blues": path_to_images+"st_louis_blues.png",
        "Tampa Bay Lightning": path_to_images+"tampa_bay_lightning.png",
        "Toronto Maple Leafs": path_to_images+"toronto_maple_leafs.png",
        "Utah Mammoth": path_to_images+"utah_mammoth.png",
        "Vancouver Canucks": path_to_images+"vancouver_canucks.png",
        "Vegas Golden Knights": path_to_images+"vegas_golden_knights.png",
        "Washington Capitals": path_to_images+"washington_capitals.png",
        "Winnipeg Jets": path_to_images+"winnipeg_jets.png"
    }

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

    # set up data to plot images
    df_nhl_rs_career_stats["team_img"] = df_nhl_rs_career_stats["team_names"].map(images)
    df_nhl_rs_career_stats["season_plot"] = df_nhl_rs_career_stats["season"].astype(str).str[:4].astype(int)

    return df_nhl_rs_career_stats


def plot_stat_per_game(ax, ax_str, df, include_avg, stat, title, ylabel):

    for x, y, path in zip(df["season_plot"], df[stat], df["team_img"]):
        try:
            # Load image array
            img_array = plt.imread(path)

            # Wrap image in OffsetImage. Use 'zoom' to scale its visual size.
            img_box = OffsetImage(img_array, zoom=0.05)

            # Position the box at the specific (x, y) data point
            ab = AnnotationBbox(img_box, (x, y), frameon=False, zorder=100)

            # Add the custom marker to your plot
            ax.add_artist(ab)
        except FileNotFoundError:
            print(f"Warning: {path} not found. Skipping point ({x}, {y}).")

    if include_avg:
        ax.axhline(y=np.mean(df[stat]), color='tab:green', linewidth=8, zorder=10)
        #plt.axhline(y=np.mean(df["goals"][1:]), color='tab:green', linewidth=2) # this would exclude their rookie season from the average

        ax.axhline(y=np.mean(df[stat])+np.std(df[stat]), color='tab:green', linestyle='--', linewidth=4, zorder=10)
        ax.axhline(y=np.mean(df[stat])-np.std(df[stat]), color='tab:green', linestyle='--', linewidth=4, zorder=10)
        ax.fill_between(df["season_plot"], np.mean(df[stat])+np.std(df[stat]),
            np.mean(df[stat])-np.std(df[stat]), color="gray", alpha=0.3, zorder=1)

    # set xlim and ylim
    xmin, xmax = min(df["season_plot"]), max(df["season_plot"])
    ymin, ymax = min(df[stat]), max(df[stat])
    x_pad = (xmax - xmin) * 0.1
    y_pad = (ymax - ymin) * 0.1
    ax.set_xlim(xmin - x_pad, xmax + x_pad)
    ax.set_ylim(ymin - y_pad, ymax + y_pad)

    ax.set_title(title)
    ax.set_xlabel("Season")
    ax.set_ylabel(ylabel)
    #ax.set_xticks(df["season"], df["season_label"])
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(True, alpha=0.3)


"""
def plot_stat_per_game_no_team_pics(ax, ax_str, df, include_avg, stat, title, ylabel):

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


def home_away_split(player_id, season_id):

    client = NHLClient(debug=False)

    season = season_id

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
