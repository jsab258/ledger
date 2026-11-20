// The numbers of the system "law" (police; DESIGN 8, A12, A13, A36, A37): plain data, imports nothing.
export const TUNE = {
  // what an arrest costs in game hours, never the game
  custodyGameHours: { damage: 6, damageOwnedUp: 2, assault: 6, wounding: 8, robbery: 12, killing: 22 },
  arrestRealSecondsAtMost: 120,
  oneCaseAddsGameHours: 2, // once the street crimes and the fire are one case
  announcesBeforeChallengeRealSeconds: 3,
  challengesWithinMetres: 14,
  stages: ['nothing', 'asking round', 'investigating', 'a manhunt'],
  stageSigns: ['', 'her name in the street talk', 'an officer at his door', 'a car on the street and his description said aloud'],
  ellisFromDayIndex: 3, // day 4
  ellisTalkNeedsDayPeople: 3, // three people of his day world passing talk of his nights
  manhuntSignShowsGameHoursBeforeArrest: 1,
  officeSearchNoticeGameHours: 12, // the evening before
  // traffic (A12)
  patrolCars: 1,
  patrolCarsAtWar: 3,
  stopRealSecondsAtMost: 120,
  recklessFarOverSpeedShare: 1.6,
  speedLimitMetresPerSecond: 13.4, // 30 mph
  // bought men (A13)
  bought: {
    harker: { name: 'PC Harker', pricePence: 5000, limit: 'looks away from a car', uses: 99 },
    pollitt: { name: 'DC Pollitt', pricePence: 15000, limit: 'loses a statement', uses: 1 },
  },
  // a street on edge (A37)
  edgeDeeds: 3,
  edgeWithinGameDays: 2,
  edgeEasesAfterGameDays: 3,
  edgeWalkStartsSoonerTimes: 0.5,
  edgeBeatVisitsTimes: 2,
  // police after a deed (A36)
  officerAtTheSpotWithinGameMinutes: 20,
  spotWatchedUntilHour: 7,
  officerToTheSpotMetresPerSecond: 1.6,
  officerStaysAtTheSpotGameMinutes: 60,
  watchedGroundWithinMetres: 24,
  ellisNextMorningAtHour: 9,
  // the beat
  beatFromHour: 21,
  beatUntilHour: 5,
  beatWalkMetresPerSecond: 1.5,
  searchFindsEverythingCarried: true,
  // charges
  cautionForFirst: ['damage'],
  bailForKillingIsRare: true,
  // hit and run (ER-DRIVE-10)
  hitAndRunCostsFirmGameDays: 5,
  hitAndRunFareShare: 0.6,
  ambulanceArrivesGameMinutes: 10, // A22
  hospitalDaysByHurt: { bruise: 0, 'broken leg': 14, badly: 30 },
  carHurtAtMetresPerSecond: { bruise: 0, 'broken leg': 6.7, badly: 13.4 }, // 15 mph and 30 mph
  carForgivenBelowMetresPerSecond: 2.2, // a clip at walking pace
  // each kind: [how newsworthy 0..1, how it reads -1 menace..+1 decent, crime level 0..3]
  kinds: { searched_by: [0.4, -0.2, 0], talked_round: [0.1, 0, 0], paid_officer: [0.6, -0.6, 1], paid_quiet: [0.5, -0.4, 0], stopped_car: [0.35, -0.2, 0], drove_off_police: [0.6, -0.5, 1], office_searched: [0.6, -0.4, 0] },
  beatEnds: [[5.6, 30], [5.6, -40]], // the beat along Quay Street's east pavement
  beatHeardWithinMetres: 22,
  challengeWithinMetres: 12,
  challengeAgainAfterGameMinutes: 45,
  searchWithinMetres: 2.5,
  constableRunsMetresPerSecond: 5.2,
  patrolSeesWithinMetres: 45,
  patrolLoopRealSeconds: 240,
  patrolLoop: [[3.2, 30], [3.2, -80], [3.2, -190], [3.2, -80], [3.2, 30], [80, 46.6], [-40, 46.6]],
  carChaseFollowsMetresBehind: 28,
  carChaseCaughtBelowMetresPerSecond: 2,
  carChaseCaughtAfterRealSeconds: 3,
  signHeardWithinMetres: 8,
  robberyStatementNextDayAtHour: 9,
};
export const SCHEDULES = {};
export const PEOPLE = {};
