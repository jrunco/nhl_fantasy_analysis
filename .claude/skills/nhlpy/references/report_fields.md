# Report types and their fields

Generated from `client.misc.config()` (NHL stats API, 2025-26). Regenerate with:
`client.misc.config()` -> keys `playerReportData`, `goalieReportData`, `teamReportData`.

For each report: **fields** = what comes back in `data[]`. **resultFilters** = the properties
that are legal in `fact_query` / `factCayenneExp`. **sortKeys** = API-suggested sort properties
(any field in `fields` generally works as a sort property too).

## Skater reports

Call via: `client.stats.skater_stats_with_query_context(report_type=...)`

### `bios`

- **fields**: playerId, skaterFullName, currentTeamAbbrev, shootsCatches, positionCode, birthDate, birthCity, birthStateProvinceCode, birthCountryCode, nationalityCode, height, weight, draftYear, draftRound, draftOverall, firstSeasonForGameType, isInHallOfFameYn, gamesPlayed, goals, assists, points
- **resultFilters**: height, weight, draftYear, draftRound, draftOverall, gamesPlayed, goals, assists, points
- **sortKeys**: skaterFullName

### `faceoffpercentages`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, gamesPlayed, timeOnIcePerGame, totalFaceoffs, evFaceoffs, ppFaceoffs, shFaceoffs, offensiveZoneFaceoffs, neutralZoneFaceoffs, defensiveZoneFaceoffs, faceoffWinPct, evFaceoffPct, ppFaceoffPct, shFaceoffPct, offensiveZoneFaceoffPct, neutralZoneFaceoffPct, defensiveZoneFaceoffPct
- **resultFilters**: gamesPlayed, timeOnIcePerGame, totalFaceoffs, evFaceoffs, ppFaceoffs, shFaceoffs, offensiveZoneFaceoffs, neutralZoneFaceoffs, defensiveZoneFaceoffs, faceoffWinPct, evFaceoffPct, ppFaceoffPct, shFaceoffPct, offensiveZoneFaceoffPct, neutralZoneFaceoffPct, defensiveZoneFaceoffPct
- **sortKeys**: totalFaceoffs

### `faceoffwins`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, positionCode, gamesPlayed, totalFaceoffs, totalFaceoffWins, totalFaceoffLosses, faceoffWinPct, evFaceoffs, evFaceoffsWon, evFaceoffsLost, ppFaceoffs, ppFaceoffsWon, ppFaceoffsLost, shFaceoffs, shFaceoffsWon, shFaceoffsLost, offensiveZoneFaceoffs, offensiveZoneFaceoffWins, offensiveZoneFaceoffLosses, neutralZoneFaceoffs, neutralZoneFaceoffWins, neutralZoneFaceoffLosses, defensiveZoneFaceoffs, defensiveZoneFaceoffWins, defensiveZoneFaceoffLosses
- **resultFilters**: gamesPlayed, totalFaceoffs, totalFaceoffWins, totalFaceoffLosses, faceoffWinPct, evFaceoffs, evFaceoffsWon, evFaceoffsLost, ppFaceoffs, ppFaceoffsWon, ppFaceoffsLost, shFaceoffs, shFaceoffsWon, shFaceoffsLost, offensiveZoneFaceoffs, offensiveZoneFaceoffWins, offensiveZoneFaceoffLosses, neutralZoneFaceoffs, neutralZoneFaceoffWins, neutralZoneFaceoffLosses, defensiveZoneFaceoffs, defensiveZoneFaceoffWins, defensiveZoneFaceoffLosses
- **sortKeys**: totalFaceoffWins, faceoffWinPct

### `goalsForAgainst`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, positionCode, gamesPlayed, goals, assists, points, powerPlayTimeOnIcePerGame, powerPlayGoalFor, shortHandedGoalsAgainst, shortHandedTimeOnIcePerGame, shortHandedGoalsFor, powerPlayGoalsAgainst, evenStrengthTimeOnIcePerGame, evenStrengthGoalsFor, evenStrengthGoalsAgainst, evenStrengthGoalDifference, evenStrengthGoalsForPct
- **resultFilters**: gamesPlayed, goals, assists, points, powerPlayTimeOnIcePerGame, powerPlayGoalFor, shortHandedGoalsAgainst, shortHandedTimeOnIcePerGame, shortHandedGoalsFor, powerPlayGoalsAgainst, evenStrengthTimeOnIcePerGame, evenStrengthGoalsFor, evenStrengthGoalsAgainst, evenStrengthGoalDifference, evenStrengthGoalsForPct
- **sortKeys**: evenStrengthGoalDifference

### `penalties`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, positionCode, gamesPlayed, goals, assists, points, penaltyMinutes, penaltySecondsPerGame, timeOnIcePerGame, penaltyMinutesPerTimeOnIce, penaltiesDrawn, penalties, netPenalties, penaltiesDrawnPer60, penaltiesTakenPer60, netPenaltiesPer60, minorPenalties, majorPenalties, matchPenalties, misconductPenalties, gameMisconductPenalties
- **resultFilters**: gamesPlayed, goals, assists, points, penaltyMinutes, penaltySecondsPerGame, timeOnIcePerGame, penaltyMinutesPerTimeOnIce, penaltiesDrawn, penalties, netPenalties, penaltiesDrawnPer60, penaltiesTakenPer60, netPenaltiesPer60, minorPenalties, majorPenalties, matchPenalties, misconductPenalties, gameMisconductPenalties
- **sortKeys**: penaltyMinutes

### `penaltyShots`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, penaltyShotAttempts, penaltyShotsGoals, penaltyShotsFailed, penaltyShotShootingPct
- **resultFilters**: penaltyShotAttempts, penaltyShotsGoals, penaltyShotsFailed, penaltyShotShootingPct
- **sortKeys**: penaltyShotsGoals

### `penaltykill`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, positionCode, gamesPlayed, shGoals, shAssists, shPrimaryAssists, shSecondaryAssists, shPoints, shIndividualSatFor, shShots, shShootingPct, shGoalsPer60, shPrimaryAssistsPer60, shSecondaryAssistsPer60, shPointsPer60, shIndividualSatForPer60, shShotsPer60, ppGoalsAgainstPer60, shTimeOnIce, shTimeOnIcePerGame, shTimeOnIcePctPerGame
- **resultFilters**: gamesPlayed, shGoals, shAssists, shPrimaryAssists, shSecondaryAssists, shPoints, shIndividualSatFor, shShots, shShootingPct, shGoalsPer60, shPrimaryAssistsPer60, shSecondaryAssistsPer60, shPointsPer60, shIndividualSatForPer60, shShotsPer60, ppGoalsAgainstPer60, shTimeOnIce, shTimeOnIcePerGame, shTimeOnIcePctPerGame
- **sortKeys**: shTimeOnIce

### `percentages`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, gamesPlayed, timeOnIcePerGame5v5, satPercentage, satPercentageAhead, satPercentageTied, satPercentageBehind, satPercentageClose, satRelative, usatPercentage, usatPercentageAhead, usatPercentageTied, usatPercentageBehind, usatPrecentageClose, usatRelative, zoneStartPct5v5, shootingPct5v5, skaterSavePct5v5, skaterShootingPlusSavePct5v5
- **resultFilters**: gamesPlayed, timeOnIcePerGame5v5, satPercentage, satPercentageAhead, satPercentageTied, satPercentageBehind, satPercentageClose, satRelative, usatPercentage, usatPercentageAhead, usatPercentageTied, usatPercentageBehind, usatPrecentageClose, usatRelative, zoneStartPct5v5, shootingPct5v5, skaterSavePct5v5, skaterShootingPlusSavePct5v5
- **sortKeys**: satPercentage

### `powerplay`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, positionCode, gamesPlayed, ppGoals, ppAssists, ppPrimaryAssists, ppSecondaryAssists, ppPoints, ppIndividualSatFor, ppShots, ppShootingPct, ppGoalsPer60, ppPrimaryAssistsPer60, ppSecondaryAssistsPer60, ppPointsPer60, ppIndividualSatForPer60, ppShotsPer60, ppGoalsForPer60, ppTimeOnIce, ppTimeOnIcePerGame, ppTimeOnIcePctPerGame
- **resultFilters**: gamesPlayed, ppGoals, ppAssists, ppPrimaryAssists, ppSecondaryAssists, ppPoints, ppIndividualSatFor, ppShots, ppShootingPct, ppGoalsPer60, ppPrimaryAssistsPer60, ppSecondaryAssistsPer60, ppPointsPer60, ppIndividualSatForPer60, ppShotsPer60, ppGoalsForPer60, ppTimeOnIce, ppTimeOnIcePerGame, ppTimeOnIcePctPerGame
- **sortKeys**: ppTimeOnIce

### `puckPossessions`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, gamesPlayed, timeOnIcePerGame5v5, satPct, usatPct, goalsPct, individualSatForPer60, individualShotsForPer60, onIceShootingPct, offensiveZoneStartRatio, offensiveZoneStartPct, neutralZoneStartPct, defensiveZoneStartPct, faceoffPct5v5
- **resultFilters**: gamesPlayed, timeOnIcePerGame5v5, satPct, usatPct, goalsPct, individualSatForPer60, individualShotsForPer60, onIceShootingPct, offensiveZoneStartRatio, offensiveZoneStartPct, neutralZoneStartPct, defensiveZoneStartPct, faceoffPct5v5
- **sortKeys**: satPct

### `realtime`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, gamesPlayed, timeOnIcePerGame, hits, hitsPer60, blockedShots, blockedShotsPer60, giveaways, giveawaysPer60, takeaways, takeawaysPer60, firstGoals, otGoals, emptyNetGoals, emptyNetAssists, emptyNetPoints, totalShotAttempts, shotAttemptsBlocked, missedShots, missedShotWideOfNet, missedShotOverNet, missedShotGoalpost, missedShotCrossbar, missedShotShort, missedShotFailedBankAttempt
- **resultFilters**: gamesPlayed, timeOnIcePerGame, hits, hitsPer60, blockedShots, blockedShotsPer60, giveaways, giveawaysPer60, takeaways, takeawaysPer60, firstGoals, otGoals, emptyNetGoals, emptyNetAssists, emptyNetPoints, totalShotAttempts, shotAttemptsBlocked, missedShots, missedShotWideOfNet, missedShotOverNet, missedShotGoalpost, missedShotCrossbar, missedShotShort, missedShotFailedBankAttempt
- **sortKeys**: hits

### `scoringRates`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, positionCode, gamesPlayed, timeOnIcePerGame5v5, goals5v5, assists5v5, primaryAssists5v5, secondaryAssists5v5, points5v5, goalsPer605v5, assistsPer605v5, primaryAssistsPer605v5, secondaryAssistsPer605v5, pointsPer605v5, shootingPct5v5, onIceShootingPct5v5, offensiveZoneStartPct5v5, satRelative5v5, satPct, netMinorPenaltiesPer60
- **resultFilters**: gamesPlayed, timeOnIcePerGame5v5, goals5v5, assists5v5, primaryAssists5v5, secondaryAssists5v5, points5v5, goalsPer605v5, assistsPer605v5, primaryAssistsPer605v5, secondaryAssistsPer605v5, pointsPer605v5, shootingPct5v5, onIceShootingPct5v5, offensiveZoneStartPct5v5, satRelative5v5, satPct, netMinorPenaltiesPer60
- **sortKeys**: pointsPer605v5, goalsPer605v5

### `scoringpergame`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, gamesPlayed, goals, assists, totalPrimaryAssists, totalSecondaryAssists, points, shots, penaltyMinutes, hits, blockedShots, timeOnIce, goalsPerGame, assistsPerGame, primaryAssistsPerGame, secondaryAssistsPerGame, pointsPerGame, shotsPerGame, penaltyMinutesPerGame, hitsPerGame, blocksPerGame, timeOnIcePerGame
- **resultFilters**: gamesPlayed, goals, assists, totalPrimaryAssists, totalSecondaryAssists, points, shots, penaltyMinutes, hits, blockedShots, timeOnIce, goalsPerGame, assistsPerGame, primaryAssistsPerGame, secondaryAssistsPerGame, pointsPerGame, shotsPerGame, penaltyMinutesPerGame, hitsPerGame, blocksPerGame, timeOnIcePerGame
- **sortKeys**: pointsPerGame, goalsPerGame

### `shootout`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, shootoutGamesPlayed, shootoutGoals, shootoutShots, shootoutShootingPct, shootoutGameDecidingGoals, careerShootoutGamesPlayed, careerShootoutGoals, careerShootoutShots, careerShootoutShootingPct, careerShootoutGameDecidingGoals
- **resultFilters**: shootoutGamesPlayed, shootoutGoals, shootoutShots, shootoutShootingPct, shootoutGameDecidingGoals, careerShootoutGamesPlayed, careerShootoutGoals, careerShootoutShots, careerShootoutShootingPct, careerShootoutGameDecidingGoals
- **sortKeys**: shootoutGoals

### `shottype`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, gamesPlayed, goals, goalsWrist, goalsSnap, goalsSlap, goalsBackhand, goalsTipIn, goalsDeflected, goalsWrapAround, goalsPoke, goalsCradle, goalsBetweenLegs, goalsBat, shotsOnNetWrist, shotsOnNetSnap, shotsOnNetSlap, shotsOnNetBackhand, shotsOnNetTipIn, shotsOnNetDeflected, shotsOnNetWrapAround, shotsOnNetPoke, shotsOnNetCradle, shotsOnNetBetweenLegs, shotsOnNetBat, shootingPct, shootingPctWrist, shootingPctSnap, shootingPctSlap, shootingPctBackhand, shootingPctTipIn, shootingPctDeflected, shootingPctWrapAround, shootingPctPoke, shootingPctCradle, shootingPctBetweenLegs, shootingPctBat
- **resultFilters**: gamesPlayed, goals, goalsWrist, goalsSnap, goalsSlap, goalsBackhand, goalsTipIn, goalsDeflected, goalsWrapAround, goalsPoke, goalsCradle, goalsBetweenLegs, goalsBat, shotsOnNetWrist, shotsOnNetSnap, shotsOnNetSlap, shotsOnNetBackhand, shotsOnNetTipIn, shotsOnNetDeflected, shotsOnNetWrapAround, shotsOnNetPoke, shotsOnNetCradle, shotsOnNetBetweenLegs, shotsOnNetBat, shootingPct, shootingPctWrist, shootingPctSnap, shootingPctSlap, shootingPctBackhand, shootingPctTipIn, shootingPctDeflected, shootingPctWrapAround, shootingPctPoke, shootingPctCradle, shootingPctBetweenLegs, shootingPctBat
- **sortKeys**: shootingPct, shootingPctBat

### `summary`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, gamesPlayed, goals, assists, points, plusMinus, penaltyMinutes, pointsPerGame, evGoals, evPoints, ppGoals, ppPoints, shGoals, shPoints, otGoals, gameWinningGoals, shots, shootingPct, timeOnIcePerGame, faceoffWinPct
- **resultFilters**: gamesPlayed, goals, assists, points, plusMinus, penaltyMinutes, pointsPerGame, evGoals, evPoints, ppGoals, ppPoints, shGoals, shPoints, otGoals, gameWinningGoals, shots, shootingPct, timeOnIcePerGame, faceoffWinPct
- **sortKeys**: points, goals, assists

### `summaryshooting`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, gamesPlayed, timeOnIcePerGame5v5, satFor, satAgainst, satTotal, satAhead, satTied, satBehind, satClose, satRelative, usatFor, usatAgainst, usatTotal, usatAhead, usatTied, usatBehind, usatClose, usatRelative
- **resultFilters**: gamesPlayed, timeOnIcePerGame5v5, satFor, satAgainst, satTotal, satAhead, satTied, satBehind, satClose, satRelative, usatFor, usatAgainst, usatTotal, usatAhead, usatTied, usatBehind, usatClose, usatRelative
- **sortKeys**: satTotal, usatTotal

### `timeonice`

- **fields**: playerId, skaterFullName, seasonId, teamAbbrevs, shootsCatches, positionCode, gamesPlayed, timeOnIce, evTimeOnIce, ppTimeOnIce, shTimeOnIce, timeOnIcePerGame, evTimeOnIcePerGame, ppTimeOnIcePerGame, shTimeOnIcePerGame, otTimeOnIce, otTimeOnIcePerOtGame, shifts, timeOnIcePerShift, shiftsPerGame
- **resultFilters**: gamesPlayed, timeOnIce, evTimeOnIce, ppTimeOnIce, shTimeOnIce, timeOnIcePerGame, evTimeOnIcePerGame, ppTimeOnIcePerGame, shTimeOnIcePerGame, otTimeOnIce, otTimeOnIcePerOtGame, shifts, timeOnIcePerShift, shiftsPerGame
- **sortKeys**: timeOnIce

## Goalie reports

Call via: `client.stats.goalie_stats_summary(stats_type=...)`

### `advanced`

- **fields**: playerId, goalieFullName, seasonId, teamAbbrevs, shootsCatches, gamesPlayed, gamesStarted, completeGames, incompleteGames, completeGamePct, qualityStart, qualityStartsPct, goalsFor, goalsAgainst, goalsForAverage, goalsAgainstAverage, regulationWins, regulationLosses, shotsAgainstPer60, savePct, timeOnIce
- **resultFilters**: gamesPlayed, gamesStarted, completeGames, incompleteGames, completeGamePct, qualityStart, qualityStartsPct, goalsFor, goalsAgainst, goalsForAverage, goalsAgainstAverage, regulationWins, regulationLosses, shotsAgainstPer60, savePct, timeOnIce
- **sortKeys**: qualityStart, goalsAgainstAverage

### `bios`

- **fields**: playerId, goalieFullName, currentTeamAbbrev, shootsCatches, birthDate, birthCity, birthStateProvinceCode, birthCountryCode, nationalityCode, height, weight, draftYear, draftRound, draftOverall, firstSeasonForGameType, isInHallOfFameYn, gamesPlayed, wins, losses, ties, otLosses, shutouts
- **resultFilters**: height, weight, draftYear, draftRound, draftOverall, gamesPlayed, wins, losses, ties, otLosses, shutouts
- **sortKeys**: goalieFullName

### `daysrest`

- **fields**: playerId, goalieFullName, seasonId, teamAbbrevs, shootsCatches, gamesPlayed, gamesStarted, wins, losses, ties, otLosses, savePct, gamesPlayedDaysRest0, gamesPlayedDaysRest1, gamesPlayedDaysRest2, gamesPlayedDaysRest3, gamesPlayedDaysRest4Plus, savePctDaysRest0, savePctDaysRest1, savePctDaysRest2, savePctDaysRest3, savePctDaysRest4Plus
- **resultFilters**: gamesPlayed, gamesStarted, wins, losses, ties, otLosses, savePct, gamesPlayedDaysRest0, gamesPlayedDaysRest1, gamesPlayedDaysRest2, gamesPlayedDaysRest3, gamesPlayedDaysRest4Plus, savePctDaysRest0, savePctDaysRest1, savePctDaysRest2, savePctDaysRest3, savePctDaysRest4Plus
- **sortKeys**: wins, savePct

### `penaltyShots`

- **fields**: playerId, goalieFullName, seasonId, teamAbbrevs, shootsCatches, gamesPlayed, shotsAgainst, saves, goalsAgainst, savePct, penaltyShotsAgainst, penaltyShotsSaves, penaltyShotsGoalsAgainst, penaltyShotSavePct
- **resultFilters**: gamesPlayed, shotsAgainst, saves, goalsAgainst, savePct, penaltyShotsAgainst, penaltyShotsSaves, penaltyShotsGoalsAgainst, penaltyShotSavePct
- **sortKeys**: penaltyShotsSaves, penaltyShotSavePct

### `savesByStrength`

- **fields**: playerId, goalieFullName, seasonId, teamAbbrevs, shootsCatches, gamesPlayed, gamesStarted, wins, losses, ties, otLosses, shotsAgainst, saves, goalsAgainst, savePct, evShotsAgainst, evSaves, evGoalsAgainst, evSavePct, ppShotsAgainst, ppSaves, ppGoalsAgainst, ppSavePct, shShotsAgainst, shSaves, shGoalsAgainst, shSavePct
- **resultFilters**: gamesPlayed, gamesStarted, wins, losses, ties, otLosses, shotsAgainst, saves, goalsAgainst, savePct, evShotsAgainst, evSaves, evGoalsAgainst, evSavePct, ppShotsAgainst, ppSaves, ppGoalsAgainst, ppSavePct, shShotsAgainst, shSaves, shGoalsAgainst, shSavePct
- **sortKeys**: wins, savePct

### `shootout`

- **fields**: playerId, goalieFullName, seasonId, teamAbbrevs, shootsCatches, gamesPlayed, shootoutWins, shootoutLosses, shootoutShotsAgainst, shootoutGoalsAgainst, shootoutSaves, shootoutSavePct, careerShootoutGamesPlayed, careerShootoutWins, careerShootoutLosses, careerShootoutShotsAgainst, careerShootoutGoalsAllowed, careerShootoutSaves, careerShootoutSavePct
- **resultFilters**: gamesPlayed, shootoutWins, shootoutLosses, shootoutShotsAgainst, shootoutGoalsAgainst, shootoutSaves, shootoutSavePct, careerShootoutGamesPlayed, careerShootoutWins, careerShootoutLosses, careerShootoutShotsAgainst, careerShootoutGoalsAllowed, careerShootoutSaves, careerShootoutSavePct
- **sortKeys**: shootoutWins, shootoutSavePct

### `startedVsRelieved`

- **fields**: playerId, goalieFullName, seasonId, teamAbbrevs, shootsCatches, gamesPlayed, wins, losses, ties, otLosses, savePct, gamesStarted, gamesStartedWins, gamesStartedLosses, gamesStartedTies, gamesStartedOtLosses, gamesStartedShotsAgainst, gamesStartedSaves, gamesStartedGoalsAgainst, gamesStartedSavePct, gamesRelieved, gamesRelievedWins, gamesRelievedLosses, gamesRelievedTies, gamesRelievedOtLosses, gamesRelievedShotsAgainst, gamesRelievedSaves, gamesRelievedGoalsAgainst, gamesRelievedSavePct
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, savePct, gamesStarted, gamesStartedWins, gamesStartedLosses, gamesStartedTies, gamesStartedOtLosses, gamesStartedShotsAgainst, gamesStartedSaves, gamesStartedGoalsAgainst, gamesStartedSavePct, gamesRelieved, gamesRelievedWins, gamesRelievedLosses, gamesRelievedTies, gamesRelievedOtLosses, gamesRelievedShotsAgainst, gamesRelievedSaves, gamesRelievedGoalsAgainst, gamesRelievedSavePct
- **sortKeys**: gamesStarted, gamesStartedSavePct

### `summary`

- **fields**: playerId, goalieFullName, seasonId, teamAbbrevs, shootsCatches, gamesPlayed, gamesStarted, wins, losses, ties, otLosses, shotsAgainst, saves, goalsAgainst, savePct, goalsAgainstAverage, timeOnIce, shutouts, goals, assists, points, penaltyMinutes
- **resultFilters**: gamesPlayed, gamesStarted, wins, losses, ties, otLosses, shotsAgainst, saves, goalsAgainst, savePct, goalsAgainstAverage, timeOnIce, shutouts, goals, assists, points, penaltyMinutes
- **sortKeys**: wins, savePct

## Team reports

Call via: `raw GET en/team/<report> — only 'summary' has a wrapper (client.stats.team_summary)`

### `daysbetweengames`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, daysRest, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsForPerGame, goalsAgainstPerGame, netGoalsPerGame, shotsForPerGame, shotsAgainstPerGame, shotDifferentialPerGame, ppOpportunitiesPerGame, timesShorthandedPerGame, powerPlayPct, penaltyKillPct, faceoffWinPct
- **resultFilters**: daysRest, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsForPerGame, goalsAgainstPerGame, netGoalsPerGame, shotsForPerGame, shotsAgainstPerGame, shotDifferentialPerGame, ppOpportunitiesPerGame, timesShorthandedPerGame, powerPlayPct, penaltyKillPct, faceoffWinPct
- **sortKeys**: teamFullName, daysRest

### `faceoffpercentages`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, totalFaceoffs, evFaceoffs, ppFaceoffs, shFaceoffs, offensiveZoneFaceoffs, neutralZoneFaceoffs, defensiveZoneFaceoffs, faceoffWinPct, evFaceoffPct, ppFaceoffPct, shFaceoffPct, offensiveZoneFaceoffPct, neutralZoneFaceoffPct, defensiveZoneFaceoffPct
- **resultFilters**: gamesPlayed, totalFaceoffs, evFaceoffs, ppFaceoffs, shFaceoffs, offensiveZoneFaceoffs, neutralZoneFaceoffs, defensiveZoneFaceoffs, faceoffWinPct, evFaceoffPct, ppFaceoffPct, shFaceoffPct, offensiveZoneFaceoffPct, neutralZoneFaceoffPct, defensiveZoneFaceoffPct
- **sortKeys**: faceoffWinPct

### `faceoffwins`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, totalFaceoffs, faceoffsWon, faceoffsLost, faceoffWinPct, evFaceoffs, evFaceoffsWon, evFaceoffsLost, ppFaceoffs, ppFaceoffsWon, ppFaceoffsLost, shFaceoffs, shFaceoffsWon, shFaceoffsLost, offensiveZoneFaceoffs, offensiveZoneFaceoffWins, offensiveZoneFaceoffLosses, neutralZoneFaceoffs, neutralZoneFaceoffWins, neutralZoneFaceoffLosses, defensiveZoneFaceoffs, defensiveZoneFaceoffWins, defensiveZoneFaceoffLosses
- **resultFilters**: gamesPlayed, totalFaceoffs, faceoffsWon, faceoffsLost, faceoffWinPct, evFaceoffs, evFaceoffsWon, evFaceoffsLost, ppFaceoffs, ppFaceoffsWon, ppFaceoffsLost, shFaceoffs, shFaceoffsWon, shFaceoffsLost, offensiveZoneFaceoffs, offensiveZoneFaceoffWins, offensiveZoneFaceoffLosses, neutralZoneFaceoffs, neutralZoneFaceoffWins, neutralZoneFaceoffLosses, defensiveZoneFaceoffs, defensiveZoneFaceoffWins, defensiveZoneFaceoffLosses
- **sortKeys**: faceoffsWon, faceoffWinPct

### `goalgames`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, winPctOneGoalGames, winPctTwoGoalGames, winPctThreeGoalGames, winsOneGoalGames, winsTwoGoalGames, winsThreeGoalGames, lossesOneGoalGames, lossesTwoGoalGames, lossesThreeGoalGames, otLossesOneGoalGames
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, winPctOneGoalGames, winPctTwoGoalGames, winPctThreeGoalGames, winsOneGoalGames, winsTwoGoalGames, winsThreeGoalGames, lossesOneGoalGames, lossesTwoGoalGames, lossesThreeGoalGames, otLossesOneGoalGames
- **sortKeys**: winPctOneGoalGames

### `goalsagainstbystrength`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsFor, goalsAgainst, goalsAgainst5On5, goalsAgainst4On4, goalsAgainst3On3, goalsAgainst5On4, goalsAgainst5On3, goalsAgainst4On3, goalsAgainst3On4, goalsAgainst3On5, goalsAgainst4On5, goalsAgainstPenaltyShots, goalsAgainstEmptyNet, goalsAgainstExtraAttacker, goalsAgainstPerGame
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsFor, goalsAgainst, goalsAgainst5On5, goalsAgainst4On4, goalsAgainst3On3, goalsAgainst5On4, goalsAgainst5On3, goalsAgainst4On3, goalsAgainst3On4, goalsAgainst3On5, goalsAgainst4On5, goalsAgainstPenaltyShots, goalsAgainstEmptyNet, goalsAgainstExtraAttacker, goalsAgainstPerGame
- **sortKeys**: goalsAgainst

### `goalsagainstbystrengthgoaliepull`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsFor, goalsAgainstAllPulls, goalsAgainst6On5, goalsAgainst6On4, goalsAgainst6On3, goalsAgainst3On6, goalsAgainst4On6, goalsAgainst5On6, goalsAgainst5On4, goalsAgainst5On3, goalsAgainst4On5, goalsAgainst4On3, goalsAgainst3On4, goalsAgainst3On5, goalsAgainst6On6, goalsAgainst5On5, goalsAgainst4On4, goalsAgainstPerGame
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsFor, goalsAgainstAllPulls, goalsAgainst6On5, goalsAgainst6On4, goalsAgainst6On3, goalsAgainst3On6, goalsAgainst4On6, goalsAgainst5On6, goalsAgainst5On4, goalsAgainst5On3, goalsAgainst4On5, goalsAgainst4On3, goalsAgainst3On4, goalsAgainst3On5, goalsAgainst6On6, goalsAgainst5On5, goalsAgainst4On4, goalsAgainstPerGame
- **sortKeys**: (none)

### `goalsbyperiod`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, evGoalsFor, ppGoalsFor, shGoalsFor, goalsFor, period1GoalsFor, period2GoalsFor, period3GoalsFor, periodOtGoalsFor, goalsAgainst, period1GoalsAgainst, period2GoalsAgainst, period3GoalsAgainst, periodOtGoalsAgainst
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, evGoalsFor, ppGoalsFor, shGoalsFor, goalsFor, period1GoalsFor, period2GoalsFor, period3GoalsFor, periodOtGoalsFor, goalsAgainst, period1GoalsAgainst, period2GoalsAgainst, period3GoalsAgainst, periodOtGoalsAgainst
- **sortKeys**: period1GoalsFor

### `goalsforbystrength`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsFor, goalsAgainst, goalsFor5On5, goalsFor4On4, goalsFor3On3, goalsFor5On4, goalsFor5On3, goalsFor4On3, goalsFor3On4, goalsFor3On5, goalsFor4On5, goalsForPenaltyShots, goalsForEmptyNet, goalsForExtraAttacker, goalsForPerGame
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsFor, goalsAgainst, goalsFor5On5, goalsFor4On4, goalsFor3On3, goalsFor5On4, goalsFor5On3, goalsFor4On3, goalsFor3On4, goalsFor3On5, goalsFor4On5, goalsForPenaltyShots, goalsForEmptyNet, goalsForExtraAttacker, goalsForPerGame
- **sortKeys**: goalsFor

### `goalsforbystrengthgoaliepull`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsForAllPulls, goalsAgainst, goalsFor6On5, goalsFor6On4, goalsFor6On3, goalsFor3On6, goalsFor4On6, goalsFor5On6, goalsFor5On4, goalsFor5On3, goalsFor4On5, goalsFor4On3, goalsFor3On4, goalsFor3On5, goalsFor6On6, goalsFor5On5, goalsFor4On4, goalsForPerGame
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, goalsForAllPulls, goalsAgainst, goalsFor6On5, goalsFor6On4, goalsFor6On3, goalsFor3On6, goalsFor4On6, goalsFor5On6, goalsFor5On4, goalsFor5On3, goalsFor4On5, goalsFor4On3, goalsFor3On4, goalsFor3On5, goalsFor6On6, goalsFor5On5, goalsFor4On4, goalsForPerGame
- **sortKeys**: (none)

### `leadingtrailing`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, pointPct, period1GoalsFor, period1GoalsAgainst, period2GoalsFor, period2GoalsAgainst, winsLeadPeriod1, lossLeadPeriod1, tiesLeadPeriod1, otLossLeadPeriod1, winPctLeadPeriod1, winsLeadPeriod2, lossLeadPeriod2, tiesLeadPeriod2, otLossLeadPeriod2, winPctLeadPeriod2, winsTrailPeriod1, lossTrailPeriod1, tiesTrailPeriod1, otLossTrailPeriod1, winPctTrailPeriod1, winsTrailPeriod2, lossTrailPeriod2, tiesTrailPeriod2, otLossTrailPeriod2, winPctTrailPeriod2
- **resultFilters**: gamesPlayed, pointPct, period1GoalsFor, period1GoalsAgainst, period2GoalsFor, period2GoalsAgainst, winsLeadPeriod1, lossLeadPeriod1, tiesLeadPeriod1, otLossLeadPeriod1, winPctLeadPeriod1, winsLeadPeriod2, lossLeadPeriod2, tiesLeadPeriod2, otLossLeadPeriod2, winPctLeadPeriod2, winsTrailPeriod1, lossTrailPeriod1, tiesTrailPeriod1, otLossTrailPeriod1, winPctTrailPeriod1, winsTrailPeriod2, lossTrailPeriod2, tiesTrailPeriod2, otLossTrailPeriod2, winPctTrailPeriod2
- **sortKeys**: winsLeadPeriod1

### `outshootoutshotby`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, shotsForPerGame, shotsAgainstPerGame, netShotsPerGame, winsOutshootOpponent, lossesOutshootOpponent, tiesOutshootOpponent, otLossesOutshootOpponent, winsOutshotByOpponent, lossesOutshotByOpponent, tiesOutshotByOpponent, otLossesOutshotByOpponent, winsEvenShots, lossesEvenShots, tiesEvenShots, otLossesEvenShots
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, shotsForPerGame, shotsAgainstPerGame, netShotsPerGame, winsOutshootOpponent, lossesOutshootOpponent, tiesOutshootOpponent, otLossesOutshootOpponent, winsOutshotByOpponent, lossesOutshotByOpponent, tiesOutshotByOpponent, otLossesOutshotByOpponent, winsEvenShots, lossesEvenShots, tiesEvenShots, otLossesEvenShots
- **sortKeys**: winsOutshootOpponent

### `penalties`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, penaltyMinutes, penaltySecondsPerGame, totalPenaltiesDrawn, penalties, netPenalties, penaltiesDrawnPer60, penaltiesTakenPer60, netPenaltiesPer60, benchMinorPenalties, minors, majors, matchPenalties, misconducts, gameMisconducts
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, penaltyMinutes, penaltySecondsPerGame, totalPenaltiesDrawn, penalties, netPenalties, penaltiesDrawnPer60, penaltiesTakenPer60, netPenaltiesPer60, benchMinorPenalties, minors, majors, matchPenalties, misconducts, gameMisconducts
- **sortKeys**: penaltyMinutes

### `penaltykill`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointsPct, timesShorthanded, ppGoalsAgainst, shGoalsFor, pkNetGoals, pkTimeOnIcePerGame, timesShorthandedPerGame, ppGoalsAgainstPerGame, shGoalsForPerGame, pkNetGoalsPerGame, penaltyKillPct, penaltyKillNetPct
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointsPct, timesShorthanded, ppGoalsAgainst, shGoalsFor, pkNetGoals, pkTimeOnIcePerGame, timesShorthandedPerGame, ppGoalsAgainstPerGame, shGoalsForPerGame, pkNetGoalsPerGame, penaltyKillPct, penaltyKillNetPct
- **sortKeys**: penaltyKillPct

### `penaltykilltime`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, pointPct, timeOnIceShorthanded, timesShorthanded, shorthandedGoalsAgainst, overallPenaltyKillPct, timeOnIce4v5, timesShorthanded4v5, goalsAgainst4v5, penaltyKillPct4v5, timeOnIce3v5, timesShorthanded3v5, goalsAgainst3v5, penaltyKillPct3v5, timeOnIce3v4, timesShorthanded3v4, goalsAgainst3v4, penaltyKillPct3v4
- **resultFilters**: gamesPlayed, pointPct, timeOnIceShorthanded, timesShorthanded, shorthandedGoalsAgainst, overallPenaltyKillPct, timeOnIce4v5, timesShorthanded4v5, goalsAgainst4v5, penaltyKillPct4v5, timeOnIce3v5, timesShorthanded3v5, goalsAgainst3v5, penaltyKillPct3v5, timeOnIce3v4, timesShorthanded3v4, goalsAgainst3v4, penaltyKillPct3v4
- **sortKeys**: timeOnIceShorthanded

### `percentages`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, points, pointPct, goalsForPct, satPct, satPctAhead, satPctTied, satPctBehind, satPctClose, usatPct, usatPctAhead, usatPctTied, usatPctBehind, usatPctClose, zoneStartPct5v5, shootingPct5v5, savePct5v5, shootingPlusSavePct5v5
- **resultFilters**: gamesPlayed, points, pointPct, goalsForPct, satPct, satPctAhead, satPctTied, satPctBehind, satPctClose, usatPct, usatPctAhead, usatPctTied, usatPctBehind, usatPctClose, zoneStartPct5v5, shootingPct5v5, savePct5v5, shootingPlusSavePct5v5
- **sortKeys**: satPct

### `powerplay`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, ppOpportunities, powerPlayGoalsFor, shGoalsAgainst, ppNetGoals, ppTimeOnIcePerGame, ppOpportunitiesPerGame, ppGoalsPerGame, shGoalsAgainstPerGame, ppNetGoalsPerGame, powerPlayPct, powerPlayNetPct
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, ppOpportunities, powerPlayGoalsFor, shGoalsAgainst, ppNetGoals, ppTimeOnIcePerGame, ppOpportunitiesPerGame, ppGoalsPerGame, shGoalsAgainstPerGame, ppNetGoalsPerGame, powerPlayPct, powerPlayNetPct
- **sortKeys**: powerPlayPct

### `powerplaytime`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, pointPct, timeOnIcePp, ppOpportunities, powerPlayGoalsFor, overallPowerPlayPct, timeOnIce5v4, opportunities5v4, goals5v4, powerPlayPct5v4, timeOnIce5v3, opportunities5v3, goals5v3, powerPlayPct5v3, timeOnIce4v3, opportunities4v3, goals4v3, powerPlayPct4v3
- **resultFilters**: gamesPlayed, pointPct, timeOnIcePp, ppOpportunities, powerPlayGoalsFor, overallPowerPlayPct, timeOnIce5v4, opportunities5v4, goals5v4, powerPlayPct5v4, timeOnIce5v3, opportunities5v3, goals5v3, powerPlayPct5v3, timeOnIce4v3, opportunities4v3, goals4v3, powerPlayPct4v3
- **sortKeys**: timeOnIcePp

### `realtime`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, timeOnIcePerGame5v5, satPct, hits, hitsPer60, blockedShots, blockedShotsPer60, giveaways, giveawaysPer60, takeaways, takeawaysPer60, emptyNetGoals, shots, missedShots, shotAttemptsBlocked, totalShotAttempts
- **resultFilters**: gamesPlayed, timeOnIcePerGame5v5, satPct, hits, hitsPer60, blockedShots, blockedShotsPer60, giveaways, giveawaysPer60, takeaways, takeawaysPer60, emptyNetGoals, shots, missedShots, shotAttemptsBlocked, totalShotAttempts
- **sortKeys**: hits

### `savePercentage`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, shotsAgainst, goalieGoalsAgainst, emptyNetGoalsAgainst, goalsAgainst, saves, savePct, timeOnIce, goalsAgainstAverage, goalsAgainstPerGame, shutouts
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, shotsAgainst, goalieGoalsAgainst, emptyNetGoalsAgainst, goalsAgainst, saves, savePct, timeOnIce, goalsAgainstAverage, goalsAgainstPerGame, shutouts
- **sortKeys**: savePct, shotsAgainst

### `scoretrailfirst`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, scoringFirstGamesPlayed, winsScoringFirst, lossesScoringFirst, tiesScoringFirst, otLossesScoringFirst, winPctScoringFirst, trailingFirstGamesPlayed, winsTrailingFirst, lossesTrailingFirst, tiesTrailingFirst, otLossesTrailingFirst, winPctTrailingFirst
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, scoringFirstGamesPlayed, winsScoringFirst, lossesScoringFirst, tiesScoringFirst, otLossesScoringFirst, winPctScoringFirst, trailingFirstGamesPlayed, winsTrailingFirst, lossesTrailingFirst, tiesTrailingFirst, otLossesTrailingFirst, winPctTrailingFirst
- **sortKeys**: winsScoringFirst

### `shootout`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, shootoutGamesPlayed, shootoutWins, shootoutLosses, shootoutPoints, shootoutWinPct, shootoutGoals, shootoutShots, shootoutShootingPct, shootoutShotsAgainst, shootoutGoalsAgainst, shootoutSaves, shootoutSavePct, shootoutShootingPlusSavePct
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, shootoutGamesPlayed, shootoutWins, shootoutLosses, shootoutPoints, shootoutWinPct, shootoutGoals, shootoutShots, shootoutShootingPct, shootoutShotsAgainst, shootoutGoalsAgainst, shootoutSaves, shootoutSavePct, shootoutShootingPlusSavePct
- **sortKeys**: shootoutWins, shootoutWinPct

### `shottype`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, goalsFor, goalsWrist, goalsSnap, goalsSlap, goalsBackhand, goalsTipIn, goalsDeflected, goalsWrapAround, shotsOnNet, shotsOnNetWrist, shotsOnNetSnap, shotsOnNetSlap, shotsOnNetBackhand, shotsOnNetTipIn, shotsOnNetDeflected, shotsOnNetWrapAround, shootingPct, shootingPctWrist, shootingPctSnap, shootingPctSlap, shootingPctBackhand, shootingPctTipIn, shootingPctDeflected, shootingPctWrapAround
- **resultFilters**: gamesPlayed, goalsFor, goalsWrist, goalsSnap, goalsSlap, goalsBackhand, goalsTipIn, goalsDeflected, goalsWrapAround, shotsOnNet, shotsOnNetWrist, shotsOnNetSnap, shotsOnNetSlap, shotsOnNetBackhand, shotsOnNetTipIn, shotsOnNetDeflected, shotsOnNetWrapAround, shootingPct, shootingPctWrist, shootingPctSnap, shootingPctSlap, shootingPctBackhand, shootingPctTipIn, shootingPctDeflected, shootingPctWrapAround
- **sortKeys**: shotsOnNet, shootingPct

### `summary`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, wins, losses, ties, otLosses, points, pointPct, winsInRegulation, regulationAndOtWins, winsInShootout, goalsFor, goalsAgainst, goalsForPerGame, goalsAgainstPerGame, teamShutouts, powerPlayPct, penaltyKillPct, powerPlayNetPct, penaltyKillNetPct, shotsForPerGame, shotsAgainstPerGame, faceoffWinPct
- **resultFilters**: gamesPlayed, wins, losses, ties, otLosses, points, pointPct, winsInRegulation, regulationAndOtWins, winsInShootout, goalsFor, goalsAgainst, goalsForPerGame, goalsAgainstPerGame, teamShutouts, powerPlayPct, penaltyKillPct, powerPlayNetPct, penaltyKillNetPct, shotsForPerGame, shotsAgainstPerGame, faceoffWinPct
- **sortKeys**: points, wins

### `summaryshooting`

- **fields**: teamId, franchiseId, teamFullName, franchiseName, seasonId, gamesPlayed, shots5v5, satFor, satAgainst, satTotal, satTied, satAhead, satBehind, satClose, usatFor, usatAgainst, usatTotal, usatTied, usatAhead, usatBehind, usatClose
- **resultFilters**: gamesPlayed, shots5v5, satFor, satAgainst, satTotal, satTied, satAhead, satBehind, satClose, usatFor, usatAgainst, usatTotal, usatTied, usatAhead, usatBehind, usatClose
- **sortKeys**: satTotal
