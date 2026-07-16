---
name: nhlpy
description: Expert use of the nhl-api-py (`nhlpy`) library for NHL data — stats reports, the query builder, EDGE tracking data, schedules, standings, play-by-play. Use whenever pulling NHL data, building a QueryContext/cayenneExp, choosing a report_type, or debugging BadRequestException / truncated result sets from the NHL stats API.
---

# nhlpy (nhl-api-py) expert usage

`pip install nhl-api-py`, imports as `nhlpy`. Version documented here: **3.3.0**.

```python
from nhlpy import NHLClient
client = NHLClient(timeout=60)            # default timeout=10 is too tight for big pulls — see below
                                          # debug=True logs every URL; use it when a query misbehaves
```

Everything hangs off that one client: `client.stats`, `client.edge`, `client.schedule`,
`client.standings`, `client.teams`, `client.players`, `client.game_center`, `client.misc`,
`client.helpers`. Full method list: `references/api_surface.md`.

## The one thing to understand: two different APIs

nhlpy wraps two unrelated NHL backends, and almost every mistake comes from confusing them.

| | **Web API** (`api-web.nhle.com`) | **Stats API** (`api.nhle.com/stats/rest`) |
|---|---|---|
| Powers | schedule, standings, rosters, game_center, EDGE | the stats reports |
| Shape | fixed endpoints, nested JSON | one report engine + a query language |
| Identified by | `team_abbr` ("TOR"), `player_id` | `franchise_id` (int), `playerId` |
| Filtering | none — you get the whole payload | Cayenne expressions |

**`team_abbr` and `franchise_id` are not interchangeable, and `franchise_id` is not `teamId`.**
Get the mapping from `client.teams.teams()`, which returns dicts carrying `abbr`, `franchise_id`,
conference, and division together. That call is the bridge between the two worlds.

## The stats report engine

This is where the library's real power is, and it's the part people underuse. There are **50 report
types** (18 skater, 8 goalie, 24 team). Each is the same query engine pointed at a different column
set. `report_type="summary"` is the boring default; `scoringRates`, `puckPossessions`, `realtime`,
`timeonice`, `powerplay`, `shottype` are where the interesting fantasy signal lives.

Every report field, its legal filter properties, and its sort keys: **`references/report_fields.md`**
(generated from the API's own `client.misc.config()`). Consult it before inventing a field name.

Three knobs, and they are *not* the same thing:

- **`cayenneExp`** — *which rows exist.* Built by `QueryBuilder` from filter objects. Season, game
  type, position, franchise, nationality, draft, etc.
- **`fact_query`** (`factCayenneExp`) — *which rows survive, by their stats.* `gamesPlayed>=40`,
  `shots>=100`. Applied after aggregation. Defaults to `gamesPlayed>=1`.
- **`aggregate`** — `True` collapses a multi-season range into one row per player (career-in-range
  totals). `False` gives one row per player per season.

### Canonical skater query

```python
from nhlpy.api.query.builder import QueryBuilder
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.game_type import GameTypeQuery
from nhlpy.api.query.filters.position import PositionQuery, PositionTypes

ctx = QueryBuilder().build(filters=[
    SeasonQuery(season_start="20242025", season_end="20242025"),
    GameTypeQuery(game_type="2"),                        # 1=pre, 2=regular, 3=playoffs
    PositionQuery(position=PositionTypes.ALL_FORWARDS),  # F expands to (L or R or C)
])
assert ctx.is_valid(), ctx.errors        # ALWAYS check — build() collects errors, it does not raise

ctx.fact_query = "gamesPlayed>=40"       # only way to set it; build() ignores fact_query entirely

res = client.stats.skater_stats_with_query_context(
    report_type="scoringRates",
    query_context=ctx,
    aggregate=False,
    limit=-1,                            # see below
)
rows, n = res["data"], res["total"]
```

Note `ctx.fact_query = ...` is a **post-build mutation**. `QueryBuilder.build()` accepts no
`fact_query` argument even though `QueryContext.__init__` takes one — assigning to the attribute
afterward is the supported path, not a hack.

### `limit=-1` returns everything in one call

The default `limit=25` silently truncates. `limit=-1` returns the full result set in a single
request (a full season of skater summaries = 920 rows, one call, well under a second). Prefer it
over hand-rolled pagination loops.

**Pair it with a raised timeout.** `NHLClient` defaults to `timeout=10`, and the wider reports are
much slower than `summary` — a `limit=-1` pull of `scoringRates` for one season reliably blows
through 10s and dies with `httpx.ReadTimeout` (an httpx error, *not* an `NHLApiException`, so a
`try/except NHLApiException` will not catch it). `NHLClient(timeout=60)` fixes it.

## Footguns — all four verified against the live API

**1. `total` is capped at 10000, and rows silently truncate there.** This is the dangerous one.
A season of *per-game* skater rows is ~47,000; ask for them in one query and you get exactly 10000
back, with `total` reporting `10000` as though that were the true count. No exception, no warning.
Chunk by franchise (~1,476 rows per team-season — safely under the cap) and concatenate:

```python
for team in client.teams.teams():
    ctx = QueryBuilder().build(filters=[
        FranchiseQuery(franchise_id=team["franchise_id"]),
        SeasonQuery(season_start=season, season_end=season),
        GameTypeQuery(game_type="2"),
    ])
    ...
```
Rule of thumb: if a result comes back as exactly 10000 rows, it is truncated. Never trust it.

**2. A filter that renders empty corrupts the whole query.** `StatusQuery()` with its defaults
(`is_active=False, is_hall_of_fame=False`) emits `""`, which `build()` joins into
`"seasonId >= 20242025 and  and gameTypeId=2"`. `is_valid()` returns **True**, then the API rejects
it with `BadRequestException: Encountered unexpected token: "and"`. Either pass
`StatusQuery(is_active=True)` or omit the filter — never include it in its default state. If you get
that token error, print `ctx.query_str` and look for a doubled `and`.

**3. `is_valid()` is weaker than it looks.** Most filters' `validate()` is a hardcoded `return True`
— only `DecisionQuery` genuinely validates. A wrong franchise id or a misspelled nationality code
passes validation and fails (or silently returns nothing) at the API.

**4. Per-game rows need the escape hatch.** `skater_stats_with_query_context` hardcodes
`isGame=False`, so it can only ever return season aggregates. Per-game rows require a raw call (below).

## The escape hatch

Only `en/team/summary` is wrapped (`client.stats.team_summary`); the other 23 team reports and
`isGame=True` have no wrapper. Reuse the client's HTTP layer rather than reaching for `requests` —
you keep the error handling and the `QueryContext` you already built:

```python
import json
from nhlpy.http_client import Endpoint

res = client.stats.client.get(
    endpoint=Endpoint.API_STATS,
    resource="en/team/realtime",          # any report from references/report_fields.md
    query_params={
        "isAggregate": False,
        "isGame": True,                   # True -> one row per player per game (gameId, gameDate)
        "start": 0, "limit": -1,
        "factCayenneExp": ctx.fact_query,
        "cayenneExp": ctx.query_str,
        "sort": json.dumps([{"property": "hits", "direction": "DESC"}]),
    },
).json()
```

Goalies have no `goalie_stats_with_query_context`. Feed the built query in through
`default_cayenne_exp` instead — it accepts the same string:

```python
client.stats.goalie_stats_summary(
    start_season="20242025", stats_type="advanced",
    default_cayenne_exp=ctx.query_str, limit=-1,
)
```

## Filters

All live in `nhlpy.api.query.filters.*`. Constructor arg → emitted Cayenne property:

| Filter | Arg | Emits | Notes |
|---|---|---|---|
| `SeasonQuery` | `season_start`, `season_end` | `seasonId >= / <=` | `"20242025"` format; same value both sides for one season |
| `GameTypeQuery` | `game_type` | `gameTypeId` | `"1"` pre, `"2"` regular, `"3"` playoffs |
| `FranchiseQuery` | `franchise_id` | `franchiseId` | from `client.teams.teams()`, **not** an abbr |
| `OpponentQuery` | `opponent_franchise_id` | `opponentFranchiseId` | |
| `PositionQuery` | `position` | `positionCode` | `PositionTypes` enum; `ALL_FORWARDS` → OR-group |
| `NationalityQuery` | `nation_code` | `nationalityCode` | codes from `client.misc.countries()` |
| `DraftQuery` | `year`, `draft_round` | `draftYear`, `draftRound` | round optional |
| `ShootCatchesQuery` | `shoot_catch` | `shootsCatches` | `"L"` / `"R"` |
| `HomeRoadQuery` | `home_road` | `homeRoad` | `"H"` / `"R"` |
| `ExperienceQuery` | `is_rookie` | `isRookie` | |
| `StatusQuery` | `is_active`, `is_hall_of_fame` | `active` / `isInHallOfFame` | see footgun 2 |
| `DecisionQuery` | `decision` | `decision` | `"W"`/`"L"`/`"O"`; goalies; raises on bad input |

Filters are ANDed. There is no OR across filters and no NOT — for either, write the `cayenneExp`
string yourself and pass it as `default_cayenne_exp`, or assign to `ctx.query_str`.

## EDGE (puck/player tracking)

`client.edge.*` — the modern tracking data: shot speed, skating speed, bursts, distance skated,
zone-time %, shot locations. Skater, goalie, and team variants of each, plus `*_landing` for
league-wide leaders. All take `(player_id | team_id, season=None, game_type=2)` and default to the
current season when `season` is omitted. Values come back as `{"imperial": ..., "metric": ...}` —
pick a unit explicitly.

This is a different dataset from the stats reports, not a different view of it. Zone-time and
skating-speed data exist nowhere else in the library.

## Rate limiting

No auth, no documented quota, but 429s are real and surface as `RateLimitExceededException`.
The `client.helpers.*` convenience methods (`all_players`, `game_ids_by_season`,
`all_players_summary_statistics`) make ~32 calls each and take an `api_sleep_rate` for this reason.
When looping over teams or games yourself, sleep ~0.5s between calls. Catch
`nhlpy.http_client.NHLApiException` (base) or its subclasses: `ResourceNotFoundException`,
`RateLimitExceededException`, `BadRequestException`, `ServerErrorException`, `UnauthorizedException`.

## Picking the right call

- One player, everything about them → `client.stats.player_career_stats(player_id)` (bio, career
  totals, `seasonTotals`, `last5Games`, awards).
- One player, game by game → `client.stats.player_game_log(player_id, season_id, game_type)`.
- Many players, filtered/ranked → the query-context path. This is the workhorse.
- Anything about a single game → `client.game_center.*`. `play_by_play` gives ~340 events with
  x/y ice coordinates; `shift_chart_data` gives ~740 shifts. Both are rich and underused.
- Tracking metrics (speed, distance, zone time) → `client.edge.*`.
- "What does this stat abbreviation mean?" → `client.misc.glossary()` (~321 entries).
