// The numbers of the system "dial" (the escalation dial, firearms and hold-ups): plain data, imports nothing.
// DESIGN section 7 and DESIGN-ADDENDUM A41. First values, to be tuned by play.
export const TUNE = {
  stateNames: ['Fists', 'Shown', 'Fired', 'War'],
  fallsOneStepAfterQuietGameDays: 14,
  neverFallsBelowState: 1, // once raised it never goes back to Fists
  shotHeardByDayMetres: 177,
  shotHeardAtNightTimes: 2,
  shotHeardInFullRainTimes: 0.6,
  nightFromHour: 21,
  nightUntilHour: 6,
  namedCarriersPerSideByState: [0, 1, 1, 3],
  deathsAnActAtMost: 3,
  shotKillsFromState: 3, // only at War can a shot kill
  shotKillsWhenRollBelowShare: 0.25,
  warIncidentsAGameWeekAtMost: 2,
  gunPricePence: 12000,
  gunBoughtFromRung: 2,
  gunFoundAtMickeysFromRung: 2,
  gunAimsWithinMetres: 14,
  drawAsksTwiceWithinRealSeconds: 1.5,
  watchersRunSoonerTimesByState: [1, 1, 1.25, 1.6],
  witnessesReportMoreTimesByState: [1, 1, 1.2, 1.5],
  nightFaresTimesByState: [1, 1, 0.9, 0.6],
  // hold-ups (A41)
  holdUpFromRung: 2,
  holdUpWithinMetres: 3,
  holdUpWeapons: { 'flick knife': 'blade', knife: 'blade', bat: 'bat', 'wheel brace': 'bat', revolver: 'gun' },
  holdUpTomSparesFromAgeYears: 60,
  holdUpNoiseCarriesMetres: 18,
  holdUpShoutCarriesMetres: 40,
  holdUpNerveAddedPerWatcher: 0.08,
  holdUpNerveAddedAtMost: 0.24,
  holdUpPressureByWeapon: { blade: 0.55, bat: 0.5, gun: 0.9 },
  holdUpShopTillPence: 4200,
  holdUpShopTillSaturdayPence: 9600,
  holdUpPursePence: 650,
  holdUpArrestCostsGameHours: 12,
  holdUpCountsAsSeenDeedsOnItsStreet: 3,
  holdUpStreetOnEdgeGameDays: 2,
  holdUpTalkCoolsAfterGameDays: 7,
  holdUpFaresFallGameDays: 7,
  holdUpFaresTimes: 0.6,
  holdUpNameCoolsGameDays: 7,
  holdUpEllisComesAtHour: 9,
  holdUpMarkWalksAfterRealSeconds: 20,
};
export const SCHEDULES = {};
export const PEOPLE = {};
