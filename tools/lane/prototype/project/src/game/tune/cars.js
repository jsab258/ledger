// The numbers of the system "cars" (DESIGN 5; A24, A27, A32): plain data, imports nothing.
export const TUNE = {
  kinds: { hit_stopped: [0.5, 0.2, 0], hit_and_run: [0.9, -0.9, 2], horn_night: [0.15, -0.1, 0], rode: [0.02, 0, 0], resprayed: [0.2, -0.1, 0] },
  mphPerMetrePerSecond: 2.237,
  choicePutAfterRealSeconds: 1.8, // inside the two seconds the rule gives (ER-DRIVE-05), counted from the last person knocked
  wreckRollsOnRealSeconds: 1.2,
  wreckSlowsEachStepTimes: 0.8,
  hornLongAfterRealSeconds: 1.2,
  pavementCountsAfterRealSeconds: 1.5,
  recklessCheckedEveryRealSeconds: 0.5,
  helpTakesGameMinutes: 12,
  carFetchedBackAtHour: 8,
  dentMendedOvernightAtHour: 6,
  rideMetresPerSecond: 9,
  ridePlaces: ['landing', 'chapel', 'market', 'station', 'fishdock', 'boarding', 'scrap', 'harbour', 'lot'],
  takeCarWithinMetres: 2.6,
  ramDamageAboveMetresPerSecond: 4.5,
};
export const SCHEDULES = {};
export const PEOPLE = {};
