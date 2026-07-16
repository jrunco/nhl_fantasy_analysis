---
name: hockey-advanced-analytics
description: Expert knowledge of advanced hockey analytics — Corsi, Fenwick, expected goals (xG), scoring/high-danger chances, GSAx, shooting talent, MoneyPuck's models and data. Use whenever interpreting, computing, or explaining NHL advanced stats, evaluating skaters/goalies/teams beyond boxscore stats, building fantasy models on shot quality, or working with MoneyPuck data.
---

# Advanced hockey analytics expert

Sources: Brett Marshall's "Hockey Analytics for Beginners" (Medium, 2022) and MoneyPuck.com (about + glossary + data pages). Full definitions/formulas: `references/metrics.md`. MoneyPuck model internals and data access: `references/moneypuck.md`.

## The metric hierarchy (weakest → strongest signal)

1. **Goals (GF%)** — what actually happened. Tiny samples, heavily luck-driven; teammate/competition quality inflates or deflates it without reflecting individual skill.
2. **Corsi (CF%)** — all shot attempts (on goal + missed + blocked). Volume proxy for possession. Treats a point shot and a slot chance identically.
3. **Fenwick (FF%)** — Corsi minus blocked shots. Basis for xG models (blocked shots have no reliable location, xG = 0).
4. **Scoring / high-danger chances (SCF%, HDCF%)** — location-weighted attempts (war-on-ice zone system; rush/rebound modifiers).
5. **Expected goals (xGF%)** — probability each unblocked attempt becomes a goal, from shot location, type, angle, distance, preceding event, etc. The single best public metric; public models are ~77–80% accurate and xG predicts future scoring better than Corsi.

For all rate metrics: **>50% good, <50% bad**, and the actual-vs-expected gap is the story (e.g., Kaprizov 2021-22: 48.99 xGF but 74 GF at 5v5 — finishing talent, not shot volume).

## Interpretation rules (apply every time)

- **Filter to 5v5 / even strength** unless the question is specifically about special teams. Mixed-strength aggregates are misleading; state the strength situation when quoting a number.
- **Sample size first.** Small samples of xG/Corsi are noise. Say so instead of drawing conclusions from a handful of games.
- **Actual vs expected gap = talent or luck.** Persistent over-performance across seasons ⇒ shooting talent (MoneyPuck models this with a Bayesian adjustment). One-season spikes ⇒ mostly variance, expect regression.
- **Context adjusts everything:** teammates, competition, zone starts, score state (trailing teams shoot more — use score-adjusted metrics), home/away.
- **Danger tiers (MoneyPuck):** low <8% xG (~75% of shots, ~33% of goals), medium 8–20% (~20% of shots, ~33% of goals), high ≥20% (~5% of shots, ~33% of goals). High-danger volume is the repeatable skill to hunt for.
- **Flurry adjustment:** in rapid shot sequences, later shots only exist because earlier ones missed. Flurry-adjusted xG (discounted by P(no goal yet), max 1.0 per flurry) is more repeatable and predictive than raw xG — prefer it for player evaluation.

## Evaluating by role

- **Skaters:** on-ice xGF% (with relative-to-team), individual xG (ixG) vs actual goals for finishing, Created xG (non-rebound xG + xG of expected rebounds — credits rebound generation; flatters D, deflates rebound-feeding C).
- **Goalies:** save % is nearly useless without shot-quality context. Use **GSAx = xGA − actual GA** (per 60 or per season). Rules of thumb: >10/season good starter, 0–10 average/backup, <0 poor. Check start volume and team defense before judging. Igor Shesterkin 2021-22: +37.18 in 53 GP (elite); Grubauer same year: −31.53 (league worst).
- **Teams / game outcomes:** Deserve-to-Win-O'Meter logic — re-simulate the game's shots with average goaltending; the >50% team historically wins ~64% of the time. MoneyPuck pregame model weights: scoring chances 54%, goaltending 29%, win-ability 17%; home ice ≈54% baseline; rest diff ≈4%. A well-calibrated NHL pregame model's favorite wins only ~60–64% (log loss ~0.65–0.66) — hockey is high-variance; never present single-game predictions as confident.

## Common pitfalls to flag

- Quoting Corsi as if it measures shot quality — it doesn't.
- Comparing xG numbers across different models (MoneyPuck, Evolving Hockey, Natural Stat Trick, HockeyViz all differ in features/training data). Name the model.
- Ignoring empty-net situations (excluded from GF/GA and handled specially in simulations).
- Treating xG as exact — it's built on scrutinized public play-by-play location data; model error is real.
- Judging goalies on raw Sv% or W-L.

## Data

MoneyPuck publishes CSVs (skaters/goalies/lines/teams per season, game-by-game zips, 1.84M-shot database 2007→present with 124 attributes + data dictionaries) — see `references/moneypuck.md` for layout **and the licensing gate**: automated scraping of moneypuck.com redirects to a license notice; manual browser download from moneypuck.com/data.htm is the intended path, and bulk/programmatic use requires emailing them for a data license. For raw NHL data, prefer the `nhlpy` skill instead.

**Which of these metrics can be generated from the NHL API (`nhlpy`)?** See `references/nhl-api-coverage.md`. Short version: Corsi/Fenwick (NHL calls them SAT/USAT), on-ice GF%, zone starts, PDO, score-state splits are direct queries; scoring/high-danger chances are buildable from play-by-play coordinates (player-level needs a shift-chart join — pbp has no on-ice lists); **nothing xG-denominated exists in the NHL API** — xG, GSAx, danger tiers, flurry/talent adjustments all require training your own model or licensing MoneyPuck's data.
