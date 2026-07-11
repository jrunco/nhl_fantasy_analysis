
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import seaborn as sns

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



client = NHLClient(debug=False)


# find player and get player_id

#get_player = "Macklin Celebrini"
#get_player = "Connor McDavid"
get_player = "Tyler Toffoli"
#get_player = "Matt Rempe"
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



career_stats = client.stats.player_career_stats(player_id=player_id)  # "8478402" = Connor McDavid

df_nhl_rs_career_stats = pd.DataFrame(career_stats["seasonTotals"])
df_nhl_rs_career_stats = df_nhl_rs_career_stats[df_nhl_rs_career_stats["leagueAbbrev"] == "NHL"]
df_nhl_rs_career_stats = df_nhl_rs_career_stats[df_nhl_rs_career_stats["gameTypeId"] == 2]
df_nhl_rs_career_stats = df_nhl_rs_career_stats.reset_index(drop=True)

#calculate pp_asists and sh_assists and add them to the stats/game below
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



# TODO: add if statement to not add average line if player has played less than 3 years
# TODO: maybe not put rookie season in averages

## make some cool plots
sns.lmplot(data=df_nhl_rs_career_stats, x="season", y="goals")
plt.title("Goals per Season")
plt.xlabel("Season")
plt.xticks(df_nhl_rs_career_stats["season"], df_nhl_rs_career_stats["season_label"])
plt.show()

sns.lmplot(data=df_nhl_rs_career_stats, x="season_label", y="goals", hue="team_names", fit_reg=False, ci=None)
plt.title("Goals per Season")
plt.xlabel("Season")
plt.show()



g = sns.lmplot(data=df_nhl_rs_career_stats, x="season", y="goals", hue="team_names", fit_reg=False, ci=None)#, zorder=100)
g._legend.set_title("Team Names")

plt.axhline(y=np.mean(df_nhl_rs_career_stats["goals"]), color='tab:green', linewidth=2, zorder=10)
#plt.axhline(y=np.mean(df_nhl_rs_career_stats["goals"][1:]), color='tab:green', linewidth=2)

plt.axhline(y=np.mean(df_nhl_rs_career_stats["goals"])+np.std(df_nhl_rs_career_stats["goals"]), color='tab:green', linestyle='--', linewidth=1, zorder=10)
plt.axhline(y=np.mean(df_nhl_rs_career_stats["goals"])-np.std(df_nhl_rs_career_stats["goals"]), color='tab:green', linestyle='--', linewidth=1, zorder=10)
plt.fill_between(df_nhl_rs_career_stats["season"], np.mean(df_nhl_rs_career_stats["goals"])+np.std(df_nhl_rs_career_stats["goals"]),
    np.mean(df_nhl_rs_career_stats["goals"])-np.std(df_nhl_rs_career_stats["goals"]), color="gray", alpha=0.3, zorder=1)

plt.title("Goals per Season")
plt.xlabel("Season")
plt.xticks(df_nhl_rs_career_stats["season"], df_nhl_rs_career_stats["season_label"])
plt.xticks(rotation=45)
plt.show()




fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))

# ax1
sns.scatterplot(data=df_nhl_rs_career_stats, x="season", y="goals_per_game", hue="team_names", ax=ax1)#, zorder=100)

ax1.axhline(y=np.mean(df_nhl_rs_career_stats["goals_per_game"]), color='tab:green', linewidth=2, zorder=10)

ax1.axhline(y=np.mean(df_nhl_rs_career_stats["goals_per_game"])+np.std(df_nhl_rs_career_stats["goals_per_game"]), color='tab:green', linestyle='--', linewidth=1, zorder=10)
ax1.axhline(y=np.mean(df_nhl_rs_career_stats["goals_per_game"])-np.std(df_nhl_rs_career_stats["goals_per_game"]), color='tab:green', linestyle='--', linewidth=1, zorder=10)
ax1.fill_between(df_nhl_rs_career_stats["season"], np.mean(df_nhl_rs_career_stats["goals_per_game"])+np.std(df_nhl_rs_career_stats["goals_per_game"]),
    np.mean(df_nhl_rs_career_stats["goals_per_game"])-np.std(df_nhl_rs_career_stats["goals_per_game"]), color="gray", alpha=0.3, zorder=1)
ax1.set_title("Goals/Game per Season")
ax1.set_xlabel("Season")
ax1.set_xticks(df_nhl_rs_career_stats["season"], df_nhl_rs_career_stats["season_label"])
ax1.tick_params(axis='x', labelrotation=45)

sns.scatterplot(data=df_nhl_rs_career_stats, x="season", y="goals_per_game", hue="team_names", ax=ax2, legend=False)#, zorder=100)

# ax2
ax2.axhline(y=np.mean(df_nhl_rs_career_stats["goals_per_game"]), color='tab:green', linewidth=2, zorder=10)

ax2.axhline(y=np.mean(df_nhl_rs_career_stats["goals_per_game"])+np.std(df_nhl_rs_career_stats["goals_per_game"]), color='tab:green', linestyle='--', linewidth=1, zorder=10)
ax2.axhline(y=np.mean(df_nhl_rs_career_stats["goals_per_game"])-np.std(df_nhl_rs_career_stats["goals_per_game"]), color='tab:green', linestyle='--', linewidth=1, zorder=10)
ax2.fill_between(df_nhl_rs_career_stats["season"], np.mean(df_nhl_rs_career_stats["goals_per_game"])+np.std(df_nhl_rs_career_stats["goals_per_game"]),
    np.mean(df_nhl_rs_career_stats["goals_per_game"])-np.std(df_nhl_rs_career_stats["goals_per_game"]), color="gray", alpha=0.3, zorder=1)
ax2.set_title("Goals/Game per Season")
ax2.set_xlabel("Season")
ax2.set_xticks(df_nhl_rs_career_stats["season"], df_nhl_rs_career_stats["season_label"])
ax2.tick_params(axis='x', labelrotation=45)

plt.show()




fig = Figure(figsize=(7, 4), dpi=100)

plt.subplot(1, 2, 1)
sns.scatterplot(data=df_nhl_rs_career_stats, x="season", y="goals", hue="team_names")
plt.title("Goals per Season")
plt.xlabel("Season")
plt.xticks(df_nhl_rs_career_stats["season"], df_nhl_rs_career_stats["season_label"])

plt.subplot(1, 2, 2)
sns.scatterplot(data=df_nhl_rs_career_stats, x="season", y="goals", hue="team_names")
plt.title("Goals per Season")
plt.xlabel("Season")
plt.xticks(df_nhl_rs_career_stats["season"], df_nhl_rs_career_stats["season_label"])

plt.tight_layout() # Ensures no overlap between plots
plt.show()





## if a player is traded mid-season, the stats are kept in different columns
## for stats/game, that is preferable
## for total season stats, I will need to combine those rows somehow...
for i in range(len(df_nhl_rs_career_stats)):

    #print(i)
    if i+1 == len(df_nhl_rs_career_stats):
        print(i)
        continue
    else:
        if df_nhl_rs_career_stats["season"].values[i] == df_nhl_rs_career_stats["season"].values[i+1]:
            print("yes")


df_nhl_rs_career_stats_season_group = df_nhl_rs_career_stats.groupby('season').sum().reset_index() # this will make the /game stats wrong









## TODO: need to combine data points on years when a player is traded mid season











## for loops are for ...
"""
nhl_rs_career = pd.DataFrame(columns="season", "avgTOI", 'gamesPlayed', "goals", "assists", "points",
    "plusMinus", "powerPlayGoals", "powerPlayAssits", "shorthandedGoals", "shorthandedAssits", "gameWinningGoals",
    "otGoals", "shots", "shootingPctg", "faceoffWinningPctg")
for year in range(len(career_stats)):
    if career_stats["seasonTotals"][year]["leagueAbbrev"] == "NHL" and career_stats["seasonTotals"][year]["gameTypeId"] == 2:

        # get stats
        season = career_stats["seasonTotals"][year]["season"]
        avgTOI = career_stats["seasonTotals"][year]["avgTOI"]
        gamesPlayed = career_stats["seasonTotals"][year]["gamesPlayed"]
        goals = career_stats["seasonTotals"][year]["goals"]
        assists = career_stats["seasonTotals"][year]["assists"]
        points = career_stats["seasonTotals"][year]["points"]
        plusMinus = career_stats["seasonTotals"][year]["plusMinus"]
        powerPlayGoals = career_stats["seasonTotals"][year]["powerPlayGoals"]
        powerPlayAssits = career_stats["seasonTotals"][year]["powerPlayAssits"]
        shorthandedGoals = career_stats["seasonTotals"][year]["shorthandedGoals"]
        shorthandedAssits = career_stats["seasonTotals"][year]["shorthandedAssits"]
        gameWinningGoals = career_stats["seasonTotals"][year]["gameWinningGoals"]
        otGoals = career_stats["seasonTotals"][year]["otGoals"]
        shots = career_stats["seasonTotals"][year]["shots"]
        shootingPctg = career_stats["seasonTotals"][year]["shootingPctg"]
        faceoffWinningPctg = career_stats["seasonTotals"][year]["faceoffWinningPctg"]

        # append to dataframe
        nhl_rs_career
"""



"""
In [22]: career_stats.keys()
Out[22]: dict_keys(['playerId', 'isActive', 'currentTeamId', 'currentTeamAbbrev', 'fullTeamName', 'teamCommonName', 'teamPlaceNameWithPreposition', 'firstName', 'lastName', 'badges', 'teamLogo', 'sweaterNumber', 'position', 'headshot', 'heroImage', 'heightInInches', 'heightInCentimeters', 'weightInPounds', 'weightInKilograms', 'birthDate', 'birthCity', 'birthStateProvince', 'birthCountry', 'shootsCatches', 'draftDetails', 'playerSlug', 'inTop100AllTime', 'inHHOF', 'featuredStats', 'careerTotals', 'shopLink', 'twitterLink', 'watchLink', 'last5Games', 'seasonTotals', 'awards', 'currentTeamRoster'])
"""
