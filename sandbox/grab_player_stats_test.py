

import numpy as np
import pandas as pd

#from nhlpy import NHLClient


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



client = NHLClient(debug=True)

filters = [
    GameTypeQuery(game_type="2"),
    #DraftQuery(year="2020", draft_round="2"),
    SeasonQuery(season_start="20252026", season_end="20252026"),
    FranchiseQuery(franchise_id="1"),
    #PositionQuery(position=PositionTypes.ALL_FORWARDS)
]

query_builder = QueryBuilder()
query_context: QueryContext = query_builder.build(filters=filters)

data = client.stats.skater_stats_with_query_context(
    #report_type='summary',
    #report_type='bios',
    report_type='realtime',
    query_context=query_context,
    aggregate=True,
    start=0,
    limit=None
)




# Basic usage
client = NHLClient()

# Get all teams
teams = client.teams.teams()

# Find a specific team
for team in teams:
    if team['abbr'] == 'SJS':
        print(f"Team: {team['name']}")
        print(f"Division: {team['division']['name']}")
        print(f"Franchise ID: {team['franchise_id']}")
        break

# Get that team's roster
roster = client.teams.team_roster(team_abbr="SJS", season="20252026")
print(f"Forwards: {len(roster['forwards'])}")
print(f"Defensemen: {len(roster['defensemen'])}")
print(f"Goalies: {len(roster['goalies'])}")

"""
for key, value in roster.items():
    print(f"Key: {key}, Value: {value}")
    print(" ")

for value in roster.items():
    print(f"Value: {value}")
    print(" ")
"""

print(roster["forwards"][0])

# roster.keys() == dict_keys(['forwards', 'defensemen', 'goalies'])
#roster_keys = roster.keys()
roster_keys = ['forwards', 'defensemen', 'goalies']
for i in range(len(roster_keys)):
    for j in range(len(roster[roster_keys[i]])):
        #print(roster[roster_keys[i]][j])
        print(roster[roster_keys[i]][j]['id'])
        print(roster[roster_keys[i]][j]['firstName'])
        print(roster[roster_keys[i]][j]['lastName'])
        print(" ")



# get player game log
"""
game_type (int): The type of games to retrieve:
            1: Preseason
            2: Regular season
            3: Playoffs
"""

# celebrini: 8484801
# smith: 8484227
# it does accurately take into account games played. len(celebrini) is 82; len(smith) is 69
mack = client.stats.player_game_log(player_id="8484801", season_id="20252026", game_type="2")

print(mack[0])
print(mack[0]["goals"])
"""
{'gameId': 2025021308, 'teamAbbrev': 'SJS', 'homeRoadFlag': 'R', 'gameDate': '2026-04-16', 'goals': 1, 'assists': 2, 'commonName': {'default': 'Sharks'},
'opponentCommonName': {'default': 'Jets'}, 'points': 3, 'plusMinus': 2, 'powerPlayGoals': 0, 'powerPlayPoints': 1, 'gameWinningGoals': 0, 'otGoals': 0,
'shots': 3, 'shifts': 16, 'shorthandedGoals': 0, 'shorthandedPoints': 0, 'opponentAbbrev': 'WPG', 'pim': 0, 'toi': '14:41'}
"""

mack_goals = 0
mack_assists = 0
mack_plusMinus = 0
mack_powerPlayGoals = 0
mack_powerPlayAssists = 0
mack_powerPlayPoints = 0
mack_gameWinningGoals = 0
mack_shots = 0
mack_shorthandedGoals = 0
mack_shorthandedAssists = 0
mack_shorthandedPoints = 0
mack_pim = 0
for i in range(len(mack)):
    mack_goals += mack[i]["goals"]
    mack_assists += mack[i]["assists"]
    mack_plusMinus += mack[i]["plusMinus"]
    mack_powerPlayGoals += mack[i]["powerPlayGoals"]
    mack_powerPlayAssists += mack[i]["powerPlayPoints"] - mack[i]["powerPlayGoals"]
    mack_powerPlayPoints += mack[i]["powerPlayPoints"]
    mack_gameWinningGoals += mack[i]["gameWinningGoals"]
    mack_shots += mack[i]["shots"]
    mack_shorthandedGoals += mack[i]["shorthandedGoals"]
    mack_shorthandedAssists += mack[i]["shorthandedPoints"] - mack[i]["shorthandedGoals"]
    mack_shorthandedPoints += mack[i]["shorthandedPoints"]
    mack_pim += mack[i]["pim"]
print(mack_goals)
print(mack_assists)
print(mack_goals+mack_assists)

fantasy_points = mack_goals * fantasy_goals + mack_assists * fantasy_assists ### ...............

#names = np.array([])
#arrays = np.array([])
#df_mack = pd.DataFrame(data=[])



## this does not work
"""
# Filter by player
skater_stats = client.stats.skater_stats_summary(
    start_season="20232024",
    end_season="20232024",
    player_id="8484801" # Macklin celebrini
    #franchise_id="10"  # Toronto Maple Leafs
)
"""



### misc stats
#misc = client.misc.Misc()
glossary = client.misc.glossary()

config = client.misc.config()


for i in range(len(glossary)):
    #print("Full name: ", glossary[i]["fullName"], glossary[i]["abbreviation"], glossary[i]["definition"])
    print("Full name: ", glossary[i]["fullName"])
    print("Abbreviation: ", glossary[i]["abbreviation"])
    print("Definition: ", glossary[i]["definition"])
    print(" ")


# Find specific stats definitions
stat_terms = ["BENCH", "BKS", "A", "ENA", "EV GA"]
for term in stat_terms:
    for entry in glossary:
        if entry['abbreviation'].upper() == term:
            print(f"{term}: {entry['definition']}")
            continue




### this method only returns the first 25 players ....
### adding limit = None only gives 50 players ....




""" test code from corey """

p = client.stats.player_career_stats(player_id="8481528")


# To get a single players season data its not as easy as you would think,
# you were correct on the game log.  That being said maybe the NHL released some new APIs to dig into, but for now.

# For this you can swap the season_id to any previous season, and it works mid season.

games = client.stats.player_game_log(player_id="8478402", season_id="20252026", game_type=2)

totals = {
      "goals": sum(g["goals"] for g in games),
      "assists": sum(g["assists"] for g in games),
      "points": sum(g["points"] for g in games),
      "shots": sum(g["shots"] for g in games),
   }







def load_summary_statistics_for_skaters(season_start, season_end, limit: int = 100):
    from nhlpy.api.query.builder import QueryBuilder, QueryContext
    from nhlpy.api.query.filters.season import SeasonQuery
    from nhlpy.api.query.filters.game_type import GameTypeQuery

    filters = [
    SeasonQuery(season_start=season_start, season_end=season_end),
    GameTypeQuery(game_type="2"),

    ]
    context: QueryContext = QueryBuilder().build(filters=filters)
    all_data = []
    start = 0

    client = NHLClient(debug=False)

    while True:
        response = client.stats.skater_stats_with_query_context(
            report_type='summary',
            #report_type='realtime',
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


test_skater_query = load_summary_statistics_for_skaters("20252026", "20252026")





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

test_faceoffwins_query = load_faceoffwins_statistics_for_skaters("20252026", "20252026")




def load_faceoffpercentages_statistics_for_skaters(season_start, season_end, limit: int = 100):

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
            report_type='faceoffpercentages',
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

test_faceoffpercentages_query = load_faceoffpercentages_statistics_for_skaters("20252026", "20252026")



def load_scoringRates_statistics_for_skaters(season_start, season_end, limit: int = 100):

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
            report_type='scoringRates',
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

test_scoringRates_query = load_scoringRates_statistics_for_skaters("20252026", "20252026")



def load_scoringpergame_statistics_for_skaters(season_start, season_end, limit: int = 100):

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
            report_type='scoringpergame',
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

test_scoringpergame_query = load_scoringpergame_statistics_for_skaters("20252026", "20252026")









### nhl edge stats

# Get comprehensive EDGE statistics for a skater
edge_test = client.edge.skater_detail(player_id='8484801', season='20252026')







#### new idea to get all stats
"""
from nhlpy.stats import PlayerStats # no module called player stats

season = "20252026"
player_name = "Macklin Celebrini"

# fetch player stats for the season
stats = PlayerStats(season=season)

found = False
for player_stat in stats:
    if player_stat.full_name.lower() == player_name.lower():
"""



from nhlpy import NHLClient

# Initialize client
client = NHLClient()

# Search for player ID (in case you don't already know it)
#players = client.search_player("Macklin Celebrini") # this does not exist

# Grab the first match (you may want to verify ID in real usage)
player_id = "8484801"

# Get player stats for 2025-2026 season
stats = client.player.stats( # this does not exist
    player_id=player_id,
    season="20252026",
    stats_type="season",
    game_type="2"
)

# Extract regular season stats
regular_season = stats["regularSeason"]#["subSeason"]

# Pull desired fields
data = {
    "goals": regular_season.get("goals"),
    "assists": regular_season.get("assists"),
    "powerPlayGoals": regular_season.get("powerPlayGoals"),
    "powerPlayPoints": regular_season.get("powerPlayPoints"),
    "plusMinus": regular_season.get("plusMinus"),
    "shortHandedGoals": regular_season.get("shortHandedGoals"),
    "shortHandedPoints": regular_season.get("shortHandedPoints"),
    "hits": regular_season.get("hits"),
    "blockedShots": regular_season.get("blockedShots"),
    "penaltyMinutes": regular_season.get("penaltyMinutes"),
    "faceOffWins": regular_season.get("faceOffWins"),
    "faceOffLosses": regular_season.get("faceOffLosses"),
}

# Print results
for stat, value in data.items():
    print(f"{stat}: {value}")






player_id = 8484145 # Macklin Celebrini (verify if needed)

# Fetch stats for the 2025–2026 season
stats = client.stats.player_stats( # this does not exist
    player_id=player_id,
    season="20252026"
)

# Locate regular season stats
regular_season = next(
    s for s in stats["stats"]
    if s["type"]["displayName"] == "statsSingleSeason"
)

season_stats = regular_season["splits"][0]["stat"]

# Extract stats
goals = season_stats.get("goals", 0)
assists = season_stats.get("assists", 0)
hits = season_stats.get("hits", 0)
blocks = season_stats.get("blocked", 0)
pim = season_stats.get("pim", 0)

print(f"Goals: {goals}")
print(f"Assists: {assists}")
print(f"Hits: {hits}")
print(f"Blocked Shots: {blocks}")
print(f"Penalty Minutes: {pim}")










# end
