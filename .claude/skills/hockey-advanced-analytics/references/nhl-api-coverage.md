# Can this metric be generated from NHL data via `nhlpy`?

Cross-checked against the `nhlpy` skill (stats report fields + live play-by-play schema, verified 2026-07-16). Three tiers: **query it**, **build it from play-by-play**, **can't get it without a model or external data**.

## Tier 1 — directly queryable (stats API reports)

| Metric | Report (skater unless noted) | Fields |
|---|---|---|
| Corsi = **SAT**, Fenwick = **USAT** (NHL's names) | `summaryshooting`, `percentages`, `puckPossessions`; team `percentages` | `satFor/Against/Total`, `satPct`, `usat*`, all 5v5 |
| Relative Corsi/Fenwick | `percentages`, `summaryshooting` | `satRelative`, `usatRelative` |
| Score-state splits | same reports | `satPctAhead/Tied/Behind/Close` — raw material for score adjustment; the NHL does **not** publish a score-adjusted composite, the weighting is yours |
| On-ice GF/GA, GF% | `goalsForAgainst` | `evenStrengthGoalsFor/Against`, `evenStrengthGoalsForPct` |
| Zone starts | `puckPossessions`, `scoringRates`, `percentages` | `offensiveZoneStartPct`, `zoneStartPct5v5` |
| PDO (unnamed) | `percentages`; team `percentages` | `skaterShootingPlusSavePct5v5` / `shootingPlusSavePct5v5` |
| On-ice shooting % | `puckPossessions`, `scoringRates` | `onIceShootingPct` |
| Attempt components | `realtime`, `shottype` | `totalShotAttempts`, `missedShots*`, `blockedShots` |
| Goalie Sv% by strength | goalie `savesByStrength`, `advanced` | `evSavePct`, `ppSavePct`, `shSavePct`, quality starts |
| Goalie rest splits | goalie `daysrest` | `savePctDaysRest0..4Plus` — direct feature for a starting-goalie model |
| Rest/home/recency (pregame model inputs) | schedule, standings, team `summary` | `daysRest` on team summary |

## Tier 2 — derivable, pipeline work required (play-by-play ± shift charts)

Play-by-play events (`client.game_center.play_by_play`) carry `xCoord`, `yCoord`, `zoneCode`, `shotType`, `situationCode`, running score, and timestamps. That is enough to build:

- **war-on-ice scoring chances / high-danger chances** — zone point values from coordinates; rush (+1, ≤4s after neutral/D-zone event) and rebound (+1, ≤3s after a shot) tags from event-sequence time deltas. *Team-level* needs pbp only.
- **D-zone giveaways** (MoneyPuck pregame-model feature) — giveaway events carry `zoneCode`.
- **xG model features** — distance, angle, shot type, time/speed since last event, preceding event type, strength, empty net (from `situationCode`): all reconstructable.

**The catch — on-ice attribution:** pbp events do **not** list who was on the ice (verified live). Any *player* on-ice version of a custom metric (HDCF% for a skater, on-ice SC%) requires joining `shift_chart_data` timestamps to event timestamps. Doable, but it's a real data-engineering step, and the stats-API 10000-row cap + per-game `isGame=True` escape hatch (see nhlpy skill footguns) apply to bulk pulls.

**Bulk history cost:** training data means pbp for every game — ~1,300+ calls per season with ~0.5s sleeps. Budget hours, not minutes, and cache locally.

## Tier 3 — genuine gaps (not generate-able from the NHL API)

1. **Everything xG-denominated.** The NHL API exposes **no expected-goals field anywhere** — no xGF%, ixG, xGA. Consequently GSAx, expected Sv%, probability-based danger tiers (<8/8–20/≥20%), flurry-adjusted xG, shooting-talent-adjusted xG, Created xG, xRebounds, xFreezes, and the Deserve-to-Win-O'Meter all require **training your own model first** (Tier 2 gives you the features; the model is a project, not a query). Any "xG from nhlpy" claim is wrong.
2. **Arena-adjusted coordinates.** Raw pbp x/y has well-documented per-rink recording bias. MoneyPuck ships arena-adjusted coords in its shot files; from NHL data you must implement the adjustment yourself or accept the bias.
3. **MoneyPuck's specific numbers.** Their gradient-boosting xG, Bayesian shooting talent, and win models are proprietary trained artifacts — reproducible in kind from pbp, never in value. Don't mix a homegrown xG with quoted MoneyPuck figures.
4. **WAR (Evolving Hockey) / GSVA (Luszczyszyn).** External proprietary models; not derivable and not downloadable from the NHL.
5. **Historical model-validation baselines** (log loss ~0.65–0.66, favorite wins ~60–64%) — reference facts from MoneyPuck, not data you can pull.

**Practical rule:** counting/possession/split stats → query the stats API (Tier 1). Location- or sequence-based chance metrics → build from pbp (Tier 2). Anything with "expected" in the name → own model or MoneyPuck's licensed data (Tier 3).
