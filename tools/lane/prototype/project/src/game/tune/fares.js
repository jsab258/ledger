// The numbers of the system "fares": plain data, imports nothing. Units in the names, as rules.js.
export const TUNE = {
  // few and chosen (his words, 19 Nov): the grind is where he starts, not where he stays
  offersADayAtRungOne: 6,
  offersADayFromRungTwo: 3,
  eveningFromHour: 17,
  eveningOffersAtMost: 3,
  firstOfferAfterRealSeconds: 6,
  nextOfferAfterRealSecondsAtLeast: 35,
  nextOfferAfterRealSecondsAtMost: 70,
  offerStandsRealSeconds: 26,
  // a fare is a few minutes and ends at the door
  longestFareRealSeconds: 150,
  somethingEveryRealSeconds: 40, // ER-CORE-08: never 2 minutes without a decision, a person or a sighting
  leftHereBeforeJunctionMetres: 34,
  // money
  tipPence: 50,
  bigTipPence: 150,
  parcelPaysPence: 200,
  waitPaysPence: 300,
  edgeFarePence: 450,
  edgeTakesGameMinutes: 40,
  driverShareToThePocket: 0.1, // a fare a driver takes fills the book; little of it reaches Tom's pocket
  driverFareEveryGameMinutes: 150,
  driverFarePence: 170,
  // the hurry
  hurryRealSeconds: 75,
  // the wait
  waitRealSeconds: 22,
  // the runner (A3's rule)
  runnerLostAfterUnseenRealSeconds: 7,
  runnerLostBeyondMetres: 70,
  runnerCaughtWithinMetres: 1.3,
  runnerRunsMetresPerSecond: 4.4,
  // the car in the mirror
  mirrorFollowsAtMetres: 16,
  mirrorLostAfterUnseenRealSeconds: 7,
  mirrorLostBeyondMetres: 70,
};
export const SCHEDULES = {};
export const PEOPLE = {};
