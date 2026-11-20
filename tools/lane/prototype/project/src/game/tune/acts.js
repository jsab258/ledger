// The numbers of the system "acts" (the story's spine): plain data, imports nothing. Units in the names, as rules.js.
export const TUNE = {
  // the first hour (DESIGN 15)
  ferryShotAtMostRealSeconds: 20,
  hintAfterStandingStillRealSeconds: 4,
  hintsAtLeastApartRealSeconds: 12,
  sceneAtMostRealSeconds: 60,
  controlWithinRealSeconds: 90, // ER-FIRST-01 (the aim is 20)
  arrivesGameMinute: 940, // Monday, twenty to four, off the ferry
  // Act I: Sheila's question on Sunday, her day off
  sheilaAsksOnDayIndex: 6,
  sheilaAsksFromHour: 10,
  unansweredOnDayIndex: 7, // Monday of week two, in the small hours: saying nothing is an answer as well
  unansweredAtHour: 2,
  // Act II opens when the business has grown: any one of these, once Sheila has her answer
  opensAtRung: 2,
  opensAtFaresDriven: 10,
  opensAtNightMoneyEarnedPence: 10000,
  opensAtCrewRecruits: 1,
  // no dead weeks: this many quiet game days and the next beat comes to him by itself
  quietDaysBeforeTheNextBeatComes: 3,
  beatWaitsForHimGameHours: 6, // then it reaches him as a message taken at the office
  ellisJoinsAtSeenCrimes: 2,
  squeezeAtRivalRungsInAll: 6,
  sitDownAtRung: 3,
  sitDownAtRivalRung: 4,
  sitDownAfterBeats: 5,
  // Act III: the inspection week
  letterToFirstMorningGameDays: 1,
  inspectorFromHour: 9,
  inspectorUntilHour: 13,
  mornings: 5,
  inWritingAllowedTimes: 2,
  booksOffHoldsAtMostPence: 0,
  booksOffThinAtMostPence: 4000,
  alibiFaresThinFrom: 1,
  alibiFaresFailFrom: 3,
  wagesOwedFailFromPence: 1,
  failsThatSinkTheBooks: 2,
  thinsThatCountAsAFail: 3,
  lastDayReachesAtMost: 3,
  // the ending
  streetHoldsItAsFactFromPeople: 6,
  caseSinksTheFirmFromStrength: 0.7,
  friendHoldsAboveRegard: 0.25,
  controlBackWithinRealSeconds: 10,
  // tension (DESIGN 3)
  tenseMomentsPerHalfHourAtLeast: 12,
  retellableWithinGameHours: 30,
};
export const SCHEDULES = {};
export const PEOPLE = {};
