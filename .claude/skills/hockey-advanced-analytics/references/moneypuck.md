# MoneyPuck: model internals and data access

Source: moneypuck.com/about.htm + data.htm (fetched 2026-07-16). Built by Peter Tanner (@pr_tanner); Python on AWS.

## Expected goals model

- **Training:** 800k+ shots / 50k+ goals, 2007-08 → 2014-15 regular season + playoffs (games with location data). Holdout validation on 2015-16: top 15% of shots by predicted probability produced >50% of goals.
- **Algorithm:** gradient boosting.
- **15 features** incl.: shot distance, shot angle, shot type (slap/wrist/backhand/…), ice coordinates, time since last event, **speed from previous event** (distance between shot and prior event ÷ elapsed time — a signature feature), rebound angle change, preceding event type, opponent skaters on ice, man-advantage state, powerplay elapsed time, empty-net status.
- Highest-xG shots: rebounds close to the net with large angle change. Blocked shots get xG = 0.

## Pregame win-probability model

Trained 2017-18 → 2023-24; rebuilt Jan 2025. Three weighted components:

| Component | Weight | Inputs |
|---|---|---|
| Scoring chances | 54% | shooting-talent-adjusted xG, goals, attempts, SOG, D-zone giveaways, all strengths |
| Goaltending | 29% | current goalies' multi-season GSAx/60 and Sv% |
| Ability to win | 17% | win % with recency weighting; OT/SO games treated as ties |

Per-game adjustments: home ice (~54% baseline win rate), rest differential (~4% impact).

**Validation (favorite win % / log loss):** 2024-25: 60.4% / 0.658 · 2023-24: 61.1% / 0.661 · 2022-23: 60.6% / 0.656 · 2021-22: 64.1% / 0.648 · 2020-21: 60.1% / 0.6596. Use these as the calibration ceiling for any NHL game-prediction model you build.

## Other models

- **Live in-game:** score + time remaining over historical outcomes; penalty handling = blend of win prob if PP scores vs doesn't; pregame weight decays as game progresses.
- **Playoff odds / season simulator:** 100,000 simulations of remaining schedule using pregame probabilities; distant-game team strength regresses toward the mean.
- **Starting goalie prediction:** trained 2017-18 → 2024-25 (COVID excluded). 10 features: days rest, previous game result, TOI last 10 games, career TOI, age, 2-yr GSAx, 2-yr Sv%, home/away, healthy goalies on roster, playoff importance.
- **Deserve-to-Win-O'Meter / flurry / shooting-talent adjustments:** see `metrics.md`.

## Downloadable data (data.htm)

Datasets, 2007-08 → current season (current updated nightly):

- **Season summaries** (CSV, one row per entity-season): `skaters.csv`, `goalies.csv`, `lines.csv`, `teams.csv` under `moneypuck.com/moneypuck/playerData/seasonSummary/{year}/regular/` (also playoff variants).
- **Game-by-game**: per-season ZIPs by player type; bulk all-seasons files.
- **Careers + bios**: per-player CSVs, searchable by name.
- **Shot database**: 1,840,218 shots, 2007-08 → 2024-25, **124 attributes per shot** (xG, arena-adjusted coordinates, etc.): `peter-tanner.com/moneypuck/downloads/shots_{year}.zip` and a combined `shots_2007-2023.zip`.
- **Data dictionaries**: downloadable CSVs documenting all columns (one general, one for the 124 shot attributes).

### Licensing gate — respect it

Verified 2026-07-16: automated (non-browser) requests to the moneypuck.com CSV paths are 302-redirected to `moneypuck.com/data_license.htm`, which says scraping impacts their bandwidth costs and asks you to email **moneypuck.com@gmail.com** for a data license agreement. So:

- Manual download via a browser from moneypuck.com/data.htm is the intended free path.
- Do NOT script around the redirect (UA spoofing etc.). For programmatic/bulk use, get the license or use the `nhlpy` skill against the NHL's own APIs and compute metrics from `metrics.md` definitions.
- The `shots_{year}.zip` files on peter-tanner.com responded 200 to direct requests at time of writing, but the same license expectation reasonably applies — download once manually, cache locally.

## Interpretation notes specific to MoneyPuck numbers

- Their xG differs from Evolving Hockey / Natural Stat Trick / HockeyViz — never mix models in one comparison.
- Prefer their flurry-adjusted and shooting-talent-adjusted series for prediction; raw xG for description.
- "Score adjusted" columns already correct for score-state shooting bias.

## Further reading linked from the site

- Gradient boosting, Bayes' theorem (Wikipedia); log loss explainer (dratings.com/explaining-log-loss)
- Tanner's VanHAC talk: hockeygraphsdotcom.files.wordpress.com/2016/10/5-tanner-vanhac-expectations-for-expected-goals.ppt
- Namita Nandakumar on simulation subtleties: hockey-graphs.com/2018/12/19/some-people-were-wrong-on-twitter/
