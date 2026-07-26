
import os
import json
import math
import time

import numpy as np
import pandas as pd

import seaborn as sns

from sqlalchemy import create_engine, text

from nhlpy.nhl_client import NHLClient
from nhlpy.http_client import ResourceNotFoundException

from nhlpy.api.query.builder import QueryBuilder, QueryContext
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.game_type import GameTypeQuery



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


# =====================================================================================
# Expected-goals shot data: pull play-by-play (cached in postgres) and derive shot rows
# =====================================================================================
#
# Two layers:
#   1. Raw pbp payloads are cached one-row-per-game in nhl.game_pbp_raw (JSONB). This is
#      the source of truth so games are never re-pulled and any future feature (e.g. the
#      on-ice / shift-chart join) can be derived from cache without touching the API.
#   2. build_shot_dataframe() derives one row per unblocked shot (SOG / goal / missed —
#      i.e. Fenwick; blocked shots are excluded since they carry no reliable location).
#
# FUTURE ITERATION: "who was on the ice" is not in play-by-play. Adding on-ice skater IDs
# (for on-ice xGF%, HDCF%, etc.) requires joining shift_chart_data timestamps to event
# timestamps. Deliberately skipped here — this pass is shot-level only.

SHOT_EVENTS = ("shot-on-goal", "goal", "missed-shot")  # unblocked (Fenwick); blocked excluded
NET_X = 89.0  # goal line x-coordinate; shots are mirrored to a single net via abs(x)


def build_shot_dataframe(season, num_games=None, game_numbers=None, game_type="02",
                         sleep=0.5, debug=False):
    """One row per unblocked shot for a set of games in `season`.

    season      : full season id, e.g. "20232024".
    num_games   : pull the first `num_games` games (#0001 up). None -> whole regular
                  season via the roster helper (slow: ~32 API calls just to enumerate).
    game_numbers: explicit iterable of game numbers (1-based) to pull, e.g. an
                  evenly-spaced sample from sample_game_numbers(). Overrides num_games.
    game_type   : "02" regular season (default), "01" pre, "03" playoffs.
    sleep       : seconds between live API pulls (rate-limit courtesy); skipped on cache hits.

    Play-by-play is cached in postgres (nhl.game_pbp_raw); cached games are read from the
    db and never re-pulled. Returns a pandas DataFrame ready for xG feature work.
    """
    client = NHLClient(debug=debug)
    engine = _pg_engine()
    _ensure_pbp_cache_table(engine)

    game_ids = _resolve_game_ids(season, num_games, game_numbers, game_type, client)

    rows = []
    for game_id in game_ids:
        pbp, from_cache = _get_game_pbp(game_id, client, engine)
        if pbp is None:
            if debug:
                print(f"skip {game_id}: not found")
            continue
        rows.extend(_extract_shot_rows(pbp))
        if debug:
            print(f"{game_id}: {'cache' if from_cache else 'api'} ({len(pbp.get('plays', []))} events)")
        if not from_cache:
            time.sleep(sleep)

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(["game_id", "game_seconds"]).reset_index(drop=True)
    return df


# ------------------------------------------------------------------------------------- #
# helpers
# ------------------------------------------------------------------------------------- #

def _pg_engine():
    """SQLAlchemy engine for the local NHL postgres. Config via env, defaults to the
    local docker postgres (localhost:5432, db=postgres, user=postgres)."""
    host = os.environ.get("NHL_PG_HOST", "localhost")
    port = os.environ.get("NHL_PG_PORT", "5432")
    user = os.environ.get("NHL_PG_USER", "postgres")
    pwd = os.environ.get("NHL_PG_PASSWORD", "password")
    db = os.environ.get("NHL_PG_DB", "postgres")
    return create_engine(f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}")


def _ensure_pbp_cache_table(engine):
    """Create the nhl schema and raw-pbp cache table if they don't already exist."""
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS nhl"))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS nhl.game_pbp_raw (
                game_id    BIGINT PRIMARY KEY,
                season     INTEGER,
                game_type  INTEGER,
                game_date  DATE,
                payload    JSONB NOT NULL,
                pulled_at  TIMESTAMPTZ NOT NULL DEFAULT now()
            )
        """))


def _get_game_pbp(game_id, client, engine):
    """Return (payload_dict, from_cache). Reads nhl.game_pbp_raw first; on a miss pulls
    the pbp from the API and caches it. Returns (None, False) if the game doesn't exist."""
    with engine.connect() as conn:
        cached = conn.execute(
            text("SELECT payload FROM nhl.game_pbp_raw WHERE game_id = :g"),
            {"g": int(game_id)},
        ).scalar()
    if cached is not None:
        return cached, True

    try:
        pbp = client.game_center.play_by_play(game_id=game_id)
    except ResourceNotFoundException:
        return None, False

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO nhl.game_pbp_raw (game_id, season, game_type, game_date, payload)
                VALUES (:g, :s, :t, :d, CAST(:p AS JSONB))
                ON CONFLICT (game_id) DO NOTHING
            """),
            {
                "g": int(game_id),
                "s": pbp.get("season"),
                "t": pbp.get("gameType"),
                "d": pbp.get("gameDate"),
                "p": json.dumps(pbp),
            },
        )
    return pbp, False


def sample_game_numbers(n, total_games=1344):
    """`n` evenly-spaced game numbers across a season's 1..total_games range (systematic
    sample). Because the NHL schedule interleaves all teams chronologically, an even
    spread over game number gives a representative sample across months, teams and arenas."""
    return sorted(set(int(round(x)) for x in np.linspace(1, total_games, n)))


def _resolve_game_ids(season, num_games, game_numbers, game_type, client):
    """Game ids from the deterministic NHL scheme {startYear}{game_type}{gameNo:04d}, so
    no API call is needed. Priority: explicit game_numbers -> first num_games -> (slower)
    full-season roster enumeration when both are None."""
    start_year = season[:4]
    if game_numbers is not None:
        return [f"{start_year}{game_type}{int(n):04d}" for n in game_numbers]
    if num_games is None:
        return client.helpers.game_ids_by_season(season=season, game_types=[int(game_type)])
    return [f"{start_year}{game_type}{n:04d}" for n in range(1, num_games + 1)]


def _extract_shot_rows(pbp):
    """Derive one dict per unblocked shot from a raw pbp payload, with descriptive game
    context, xG features (distance/angle/shot type/preceding event), strength/score state."""
    home = pbp["homeTeam"]
    away = pbp["awayTeam"]
    id_to_abbr = {home["id"]: home["abbrev"], away["id"]: away["abbrev"]}
    names = {rs["playerId"]: f'{rs["firstName"]["default"]} {rs["lastName"]["default"]}'
             for rs in pbp.get("rosterSpots", [])}

    game_ctx = {
        "game_id": pbp["id"],
        "season": pbp["season"],
        "game_date": pbp.get("gameDate"),
        "venue": pbp.get("venue", {}).get("default"),
        "venue_location": pbp.get("venueLocation", {}).get("default"),
        "home_team": home["abbrev"],
        "away_team": away["abbrev"],
    }

    plays = sorted(pbp.get("plays", []), key=lambda p: p.get("sortOrder", 0))
    rows = []
    prev = None
    home_score = away_score = 0  # running score *before* the current event
    for play in plays:
        etype = play.get("typeDescKey")
        d = play.get("details", {}) or {}
        secs = _game_seconds(play)

        if etype in SHOT_EVENTS:
            owner = d.get("eventOwnerTeamId")
            is_home = owner == home["id"]
            x, y = d.get("xCoord"), d.get("yCoord")
            dist, angle = _shot_distance_angle(x, y)
            shooter = d.get("shootingPlayerId") or d.get("scoringPlayerId")
            strength, is_en, shooter_sk, opp_sk = _parse_situation(play.get("situationCode"), is_home)
            prev_type = prev.get("typeDescKey") if prev else None
            prev_secs = _game_seconds(prev) if prev else None
            dt = (secs - prev_secs) if (secs is not None and prev_secs is not None) else None
            prev_owner = (prev.get("details", {}) or {}).get("eventOwnerTeamId") if prev else None
            prev_zone = (prev.get("details", {}) or {}).get("zoneCode") if prev else None

            rows.append({
                **game_ctx,
                "shooting_team": id_to_abbr.get(owner),
                "opponent_team": away["abbrev"] if is_home else home["abbrev"],
                "is_home_shot": is_home,
                "event_id": play.get("eventId"),
                "period": play.get("periodDescriptor", {}).get("number"),
                "time_in_period": play.get("timeInPeriod"),
                "game_seconds": secs,
                "event_type": etype,
                "is_goal": int(etype == "goal"),               # model label
                "x_coord": x,
                "y_coord": y,
                "zone_code": d.get("zoneCode"),
                "shot_type": d.get("shotType"),
                "shot_distance": dist,
                "shot_angle": angle,
                "shooter_id": shooter,
                "shooter_name": names.get(shooter),
                "goalie_id": d.get("goalieInNetId"),
                "goalie_name": names.get(d.get("goalieInNetId")),
                "situation_code": play.get("situationCode"),
                "strength_state": strength,                    # shooter perspective, e.g. "5v5"
                "shooter_skaters": shooter_sk,
                "opponent_skaters": opp_sk,
                "is_empty_net": is_en,                         # opponent net empty
                "home_score": home_score,
                "away_score": away_score,
                "shooter_score": home_score if is_home else away_score,
                "opponent_score": away_score if is_home else home_score,
                "prev_event_type": prev_type,
                "prev_event_zone": prev_zone,
                "seconds_since_prev": dt,
                "is_rebound": int(prev_type in SHOT_EVENTS and prev_owner == owner
                                  and dt is not None and dt <= 3),
                "is_rush": int(prev_zone in ("N", "D") and dt is not None and dt <= 4),
            })

        if etype == "goal":  # update running score *after* recording the shot row
            if d.get("eventOwnerTeamId") == home["id"]:
                home_score += 1
            else:
                away_score += 1
        prev = play

    return rows


def _shot_distance_angle(x, y):
    """Distance (ft) and absolute angle (deg) to the attacking net. Shots are mirrored to
    a single net via abs(x); angle 0 = straight on. Coordinates are raw (un-arena-adjusted)."""
    if x is None or y is None:
        return None, None
    dx = NET_X - abs(x)
    dist = math.hypot(dx, y)
    angle = math.degrees(math.atan2(abs(y), dx)) if dx != 0 else 90.0
    return round(dist, 2), round(angle, 2)


def _parse_situation(situation_code, is_home):
    """(strength_state, is_empty_net, shooter_skaters, opp_skaters) from a 4-char
    situationCode [awayGoalie][awaySkaters][homeSkaters][homeGoalie], shooter perspective."""
    if not situation_code or len(situation_code) != 4:
        return None, None, None, None
    away_g, away_sk, home_sk, home_g = (int(c) for c in situation_code)
    if is_home:
        shooter_sk, opp_sk, opp_goalie = home_sk, away_sk, away_g
    else:
        shooter_sk, opp_sk, opp_goalie = away_sk, home_sk, home_g
    return f"{shooter_sk}v{opp_sk}", int(opp_goalie == 0), shooter_sk, opp_sk


def _game_seconds(play):
    """Absolute elapsed game seconds from a play's period + MM:SS timeInPeriod."""
    if not play:
        return None
    tip = play.get("timeInPeriod")
    period = play.get("periodDescriptor", {}).get("number")
    if tip is None or period is None:
        return None
    mm, ss = (int(v) for v in tip.split(":"))
    return (period - 1) * 1200 + mm * 60 + ss
