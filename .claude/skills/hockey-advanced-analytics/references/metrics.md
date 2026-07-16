# Metric definitions, formulas, thresholds

Compiled from "Hockey Analytics for Beginners" (Brett Marshall, Medium, Aug 2022) and the MoneyPuck glossary. Prefixes used league-wide: `F`/`A` = For/Against while on ice, `i` = individual, `x` = expected, `60` = per 60 minutes of ice time.

## Shot attempt taxonomy

| Term | Includes | Excludes |
|---|---|---|
| Corsi (shot attempt) | goals, shots on goal, misses, posts, **blocked shots** | — |
| Fenwick (unblocked attempt) | goals, shots on goal, misses, posts | blocked shots |
| Shot on goal | goals, saved shots | misses, blocks |

Named by Tim Barnes after Jim Corsi (Sabres goalie coach). Fenwick matters because xG models score unblocked attempts only — a blocked shot has xG = 0.

## Corsi / Fenwick

- `CF% = CF / (CF + CA) × 100` (Fenwick identical with FF/FA)
- Threshold: >50% good, <50% poor.
- On-ice vs off-ice vs **relative** (`on-ice − off-ice`): positive relative means the team is better with the player on the ice.
- Caveat: all attempts weighted equally — no shot quality.

## Scoring chances (war-on-ice zone system)

Attempt from an area where goals are more likely (attacking zone only). Point values by zone: outer (yellow) = 1, mid (purple) = 2, slot/inner (aqua) = 3. Modifiers: **rush attempt +1** (within 4s of a neutral/defensive-zone turnover, pass, or hit), **rebound +1** (within 3s of a blocked/missed/saved shot), **blocked −1**.

- **Scoring chance** = total ≥ 2 points → SCF, SCA, SCF%.
- **High-danger chance** = total ≥ 3 points → HDCF, HDCA, HDCF%, iHDCF, HDGF/HDGA, HDSv%.
- Threshold: >50% good.

## MoneyPuck danger tiers (probability-based alternative)

| Tier | xG per shot | Share of shots | Share of goals |
|---|---|---|---|
| Low danger | <8% | ~75% | ~33% |
| Medium danger | 8–20% | ~20% | ~33% |
| High danger | ≥20% | ~5% | ~33% |

## Goals For / Against

GF = goals scored by player's team while on ice; GA = against while on ice; empty-net goals excluded. `GF% = GF/(GF+GA) × 100`; >50% good. Caveat: teammate quality and competition level distort it heavily.

## Expected goals (xG)

The statistical chance of an unblocked shot becoming a goal. Core idea: not all shots are equal. Expressions: xGF, xGA, ixG, `xGF% = xGF/(xGF+xGA) × 100`. Players >50% xGF% are typically among a team's better performers. Public models ~76.7–79.9% accurate; xG beats Corsi at predicting future scoring (Sprigings, hockey-graphs 2015).

Typical model inputs: shot location, distance, angle, shot type, shooter/goalie identity, time since last event, preceding event type, strength state.

Seven public models (know which one your number comes from — they disagree):
Dawson Sprigings; Corsica (Manny Perry); Evolving Hockey (Josh & Luke Younggren, methodology at rpubs.com/evolvingwild/395136); HockeyViz (Micah Blake McCurry); Natural Stat Trick (Brad Timmins); MoneyPuck (Peter Tanner); Top Down Hockey (Patrick Bacon).

Caveats: values come from models, not the eye; built on public play-by-play whose location data has documented accuracy problems (Krzywicki, hockeyanalytics.com).

Worked example (Eriksson Ek vs LAK, Jan 26 2021): xGF 1.20, xGA 0.21 → xGF% 85.1%.

## Goalie metrics

- **Expected goals against (xGA)** — sum of xG of unblocked attempts faced.
- **Expected save %** — Sv% an average NHL goalie posts against that shot diet.
- **GSAx / GSAE (goals saved above expected)** = `xGA − actual GA`. 0 = as expected. Season rules of thumb: >10 good starter, 0–10 average/backup, <0 poor. Always check start volume and team defense.
  - 2021-22 extremes: Shesterkin +37.18 (53 GP, best); Grubauer −31.53 (55 GP, worst).
- **Save % above expected** = actual Sv% − expected Sv%.
- **% of xG saved above average** = GSAx / xGA.
- **Expected rebounds / expected freezes** — rebounds an average goalie would surrender / pucks they'd freeze, vs actual.

## MoneyPuck derived metrics

- **Flurry-adjusted xG** = `P(no goal yet in flurry) × raw xG`; a flurry caps at 1.0 total. More repeatable and predictive than raw xG.
- **Shooting talent above average** — Bayesian estimate of a shooter's goals-vs-xG skill from career actual/expected ratios.
- **Shooting-talent-adjusted xG** = `xG × (1 + shooting talent above average)`.
- **Expected rebounds (shooter side)** — P(shot generates a rebound), modeled like xG.
- **xG of xRebounds** = `P(rebound) × xG of the potential rebound shot`.
- **Created xG** = xG from non-rebound shots + xG of xRebounds. Credits the shot that created the rebound, not the tap-in — flatters defensemen, deflates rebound-feeding centers.
- **Score-adjusted** — reweights attempts to remove score-state bias (trailing teams shoot more); credits away teams and teams with big leads more fairly.
- **Deserve-to-Win-O'Meter** — re-simulates a game's shot list with league-average goaltending on both sides (flurry shots after a simulated goal dropped; empty-net shots excluded unless score implied a pulled goalie), including OT/SO. Team above 50% historically won 64% of the actual games.

## Related frameworks (for further evaluation)

- **WAR (Wins Above Replacement)** — evolving-hockey.com
- **GSVA (Game Score Value Added)** — Dom Luszczyszyn, The Athletic

## Analyst habits from the source material

- Use 5v5 for consistency; models score EV/PP/PK separately.
- Marshall's stated view: xG is "the single best advanced metric"; analytics complement, not replace, watching the game.
