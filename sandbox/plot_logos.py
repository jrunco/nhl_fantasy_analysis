

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


#from matplotlib import rc
#plt.rcParams.update({'font.size':22})

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



skater_name = "Tyler Toffoli"
season = "20252026"
skater_id = find_player_id(skater_name, season)

df_skater_career_stats = get_stats_by_season(skater_id, "/home/jordan/nhl_fantasy_analysis/nhl_team_logos/")
print(df_skater_career_stats["team_names"])

"""
for i in range(len(df_skater_career_stats)):
    if df_skater_career_stats["team_names"].values[i] == "Montréal Canadiens":
        print("Montréal Canadiens")
"""






import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# 1. Define data points and matching image files
#x_coords = [2, 5, 8]
#y_coords = [3, 7, 4]
#image_paths = ["/home/jordan/nhl_fantasy_analysis/nhl_team_logos/san_jose_sharks.png",
#    "/home/jordan/nhl_fantasy_analysis/nhl_team_logos/vancouver_canucks.png",
#    "/home/jordan/nhl_fantasy_analysis/nhl_team_logos/winnipeg_jets.png"] # Replace with your image paths

# 2. Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# 3. Loop through data and plot custom image markers
for x, y, path in zip(df_skater_career_stats["season_plot"], df_skater_career_stats["even_strength_points"], df_skater_career_stats["team_img"]):
    try:
        # Load image array
        img_array = plt.imread(path)

        # Wrap image in OffsetImage. Use 'zoom' to scale its visual size.
        img_box = OffsetImage(img_array, zoom=0.05)

        # Position the box at the specific (x, y) data point
        ab = AnnotationBbox(img_box, (x, y), frameon=False)

        # Add the custom marker to your plot
        ax.add_artist(ab)
    except FileNotFoundError:
        print(f"Warning: {path} not found. Skipping point ({x}, {y}).")

# 4. Format plot boundaries and labels
xmin, xmax = min(df_skater_career_stats["season_plot"]), max(df_skater_career_stats["season_plot"])
ymin, ymax = min(df_skater_career_stats["even_strength_points"]), max(df_skater_career_stats["even_strength_points"])
x_pad = (xmax - xmin) * 0.1
y_pad = (ymax - ymin) * 0.1
ax.set_xlim(xmin - x_pad, xmax + x_pad)
ax.set_ylim(ymin - y_pad, ymax + y_pad)
#ax.set_xlim(min(df_skater_career_stats["season_plot"]) - 2, max(df_skater_career_stats["season_plot"]) + 2)
#ax.set_ylim(min(df_skater_career_stats["even_strength_points"]) - 2, max(df_skater_career_stats["even_strength_points"]) + 2)
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.grid(True, alpha=0.3)

plt.show()









# end script
