# Complete nhlpy API surface (nhl-api-py 3.3.0)

Every public method on `NHLClient`. Game type: `1`=preseason, `2`=regular, `3`=playoffs.
Season format is `"20242025"`. `team_abbr` is `"TOR"`; `franchise_id` is an int from
`client.teams.teams()` and is **not** the same as `teamId`.

```python
NHLClient(debug=False, timeout=10, ssl_verify=True, follow_redirects=True)
```
`follow_redirects=True` matters: every `/now` endpoint 302s to today's data.

## client.stats

| Method | Returns |
|---|---|
| `player_career_stats(player_id)` | Bio + career totals + `seasonTotals` + `last5Games` + awards |
| `player_game_log(player_id, season_id, game_type)` | `list[dict]`, one row per game |
| `skater_stats_with_query_context(query_context, report_type, sort_expr=None, aggregate=False, start=0, limit=25)` | `{"data": [...], "total": n}`. The workhorse. 18 report types. |
| `skater_stats_summary(start_season, end_season, franchise_id=None, game_type_id=2, aggregate=False, sort_expr=None, start=0, limit=25, fact_cayenne_exp="gamesPlayed>=1", default_cayenne_exp=None)` | `list[dict]`. Convenience wrapper; no QueryContext needed. |
| `goalie_stats_summary(start_season, end_season=None, stats_type="summary", game_type_id=2, franchise_id=None, aggregate=False, sort_expr=None, start=0, limit=25, fact_cayenne_exp=None, default_cayenne_exp=None)` | `list[dict]`. 8 goalie report types. No QueryContext variant — pass `default_cayenne_exp=ctx.query_str`. |
| `team_summary(start_season, end_season, game_type_id=2, is_game=False, is_aggregate=False, sort_expr=None, start=0, limit=50, fact_cayenne_exp="gamesPlayed>1", default_cayenne_exp=None)` | `list[dict]`. Only `en/team/summary`; the other 23 team reports need a raw call. |
| `gametypes_per_season_directory_by_team(team_abbr)` | Which game types a team played each season |

Report types — full field lists in `report_fields.md`:

- **skater** (`report_type=`): `summary`, `bios`, `faceoffpercentages`, `faceoffwins`,
  `goalsForAgainst`, `realtime`, `penalties`, `penaltykill`, `penaltyShots`, `powerplay`,
  `puckPossessions`, `summaryshooting`, `percentages`, `scoringRates`, `scoringpergame`,
  `shootout`, `shottype`, `timeonice`
- **goalie** (`stats_type=`): `summary`, `advanced`, `bios`, `daysrest`, `penaltyShots`,
  `savesByStrength`, `shootout`, `startedVsRelieved`
- **team** (raw call only, except `summary`): `summary`, `realtime`, `penalties`, `penaltykill`,
  `penaltykilltime`, `powerplay`, `powerplaytime`, `percentages`, `shottype`, `shootout`,
  `faceoffpercentages`, `faceoffwins`, `goalsbyperiod`, `goalgames`, `goalsforbystrength`,
  `goalsagainstbystrength`, `goalsforbystrengthgoaliepull`, `goalsagainstbystrengthgoaliepull`,
  `savePercentage`, `scoretrailfirst`, `leadingtrailing`, `outshootoutshotby`,
  `daysbetweengames`, `summaryshooting`

`sort_expr` is `[{"property": "points", "direction": "DESC"}, ...]`. Directions: `ASC`, `DESC`,
`ASC_CI` (case-insensitive, for name fields). Omit it and the library picks a sensible per-report
default (`SortingOptions.get_default_sorting_for_report`).

## client.edge

All take `(player_id | team_id, season=None, game_type=2)`; `season=None` → current season.
Measurements are `{"imperial": ..., "metric": ...}`.

- **Skater**: `skater_detail`, `skater_shot_speed_detail`, `skater_skating_speed_detail`,
  `skater_shot_location_detail`, `skater_skating_distance_detail`, `skater_comparison`,
  `skater_zone_time`, `skater_landing(season, game_type)`, `cat_skater_detail`
- **Goalie**: `goalie_detail`, `goalie_shot_location_detail`, `goalie_5v5_detail`,
  `goalie_comparison`, `goalie_save_percentage_detail`, `goalie_landing(season, game_type)`,
  `cat_goalie_detail`
- **Team** (`team_id`, not abbr): `team_detail`, `team_skating_distance_detail`,
  `team_zone_time_details`, `team_shot_location_detail`, `team_shot_speed_detail`,
  `team_skating_speed_detail`, `team_landing(season, game_type)`

`*_landing` = league-wide leaderboards. `cat_*` = "Catch All Tracking", a condensed summary.

## client.game_center

All take `game_id` (e.g. `"2023020280"`), from any schedule endpoint.

| Method | Content |
|---|---|
| `boxscore(game_id)` | Team totals + `playerByGameStats` per position |
| `play_by_play(game_id)` | `plays[]` (~340), each with `typeDescKey`, `timeInPeriod`, `details.xCoord/yCoord`; plus `rosterSpots` |
| `shift_chart_data(game_id, excludes=["eventDetails"])` | `data[]` (~740 shifts) with start time + duration |
| `match_up(game_id)` | Landing page: scoring by period, three stars, penalties, `teamGameStats` |
| `game_story(game_id)` | Post-game recap payload |
| `season_series_matchup(game_id)` | Head-to-head record, linescore, game report links |
| `daily_scores(date=None)` | All games + scores for a date, with prev/next date links |

`play_by_play` x/y coordinates are the basis for any shot-location or xG work.

## client.schedule

- `daily_schedule(date=None)` — flattened single day (`YYYY-MM-DD`; raises `ValueError` on bad format)
- `weekly_schedule(date=None)` — 7-day `gameWeek`
- `team_season_schedule(team_abbr, season)` — full season, `{"games": [...]}`
- `team_monthly_schedule(team_abbr, month=None)` — `list[dict]`, month is `"2024-01"`
- `team_weekly_schedule(team_abbr, date=None)` — `list[dict]`
- `calendar_schedule(date)` — calendar view + all 32 teams
- `playoff_carousel(season)` — series up to the current round
- `playoff_series_schedule(season, series)` — `series` is `"a"`–`"h"` R1, `"i"`–`"l"` R2, `"m"`–`"n"` CF, `"o"` SCF
- `playoff_bracket(year)` — `year` is `"2024"`, not a season

## client.standings

- `league_standings(date=None, season=None)` — `season` wins if both are given; it's resolved to
  that season's final date via the manifest, so this gives **end-of-season** standings. Raises
  `ValueError` on an unknown season. Neither arg → today.
- `season_standing_manifest()` — every season with `standingsStart`/`standingsEnd` and rule flags
  (`tiesInUse`, `wildcardInUse`, `pointForOTlossInUse`, …). Use it before comparing across eras.

## client.teams

- `teams(date="now")` — **the abbr ↔ franchise_id bridge.** Each dict: `name`, `common_name`,
  `abbr`, `logo`, `franchise_id`, `conference{abbr,name}`, `division{abbr,name}`. Built from the
  standings endpoint, so during preseason `"now"` can resolve to *last* season — pass an explicit
  in-season date (e.g. `"2024-10-04"`) when it matters.
- `team_roster(team_abbr, season)` — `{"forwards": [...], "defensemen": [...], "goalies": [...]}`
- `franchises()` — all franchises, including defunct

## client.players

- `players_by_team(team_abbr, season)` — same payload as `team_roster`
- `prospects_by_team(team_abbr)` — prospect pool by position

## client.misc

- `config()` — **the source of truth for report fields.** `playerReportData` / `goalieReportData` /
  `teamReportData`, each report mapping to `displayItems` (returned fields), `resultFilters` (legal
  `fact_query` properties), `sortKeys`. `report_fields.md` is a dump of this.
- `glossary()` — ~321 stat definitions
- `countries()` — codes for `NationalityQuery`
- `season_specific_rules_and_info()` — ~108 seasons, games played, rule flags
- `draft_year_and_rounds()` — rounds per draft year

## client.helpers

Convenience loops. Each makes ~32 calls; all take `api_sleep_rate` to avoid 429s.

- `all_players(season, api_sleep_rate=0.5)` — every rostered player, names flattened, `team` added
- `game_ids_by_season(season, game_types=None, api_sleep_rate=1)` — ~2,600 ids for a full season
- `all_players_summary_statistics(season, api_sleep_rate=1)` — rosters joined to summary stats on
  `playerId`. Slow. Rows with no roster match are still included (bare stats dict, no `team`).

## Exceptions — `nhlpy.http_client`

`NHLApiException` (base, has `.status_code` and `.error_code`) → `ResourceNotFoundException` (404),
`RateLimitExceededException` (429), `BadRequestException` (400 — a malformed `cayenneExp` lands
here), `UnauthorizedException` (401), `ServerErrorException` (5xx — an invalid `report_type` lands
here, not a 404).

## Raw access

`client.<any>.client.get(endpoint, resource, query_params)` with
`Endpoint.API_WEB_V1` / `Endpoint.API_STATS` / `Endpoint.API_CORE` reaches anything unwrapped while
keeping the library's error handling.
