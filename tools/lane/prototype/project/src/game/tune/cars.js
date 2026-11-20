// The numbers of the system "cars": plain data, imports nothing. Units in the names, as rules.js.
export const TUNE = {
  metresPerSecondPerMph: 0.44704,
  // the cab (the prototype's own; the driving study's car replaces it later). Round 6's cab topped out at 32 mph,
  // so a single hit at 35 mph could never be made in play: the top is raised to 37 mph and nothing else is changed.
  topMetresPerSecond: 16.6,
  // damage by closing speed in one hit (DESIGN 5; the driving study, round 3)
  forgivenBelowMph: 10, // ER-DRIVE-08: a touch under 10 mph does nothing
  crumplesFromMph: 20,
  willNotDriveOnFromMph: 35,
  dentAddsDamage: 1,
  crumpleAddsDamage: 2,
  damageAtMost: 4,
  offTheRoadGameMinutes: 1440, // the firm fetches it; a day off the road
  dentsMendedAtHour: 5, // overnight, at the yard
  // people (canon: a car hurts, never kills)
  knocksDownAboveMph: 7,
  clipBelowMph: 12,
  brokenLegFromMph: 25,
  hurtPerMph: 0.018,
  hurtAtMost: 0.95, // below 1: nobody dies of a car
  aimedIsAnAttackFromMph: 12,
  downGameMinutesPerMph: 1.2,
  hospitalDaysBrokenLeg: 6,
  hospitalDaysBadly: 2,
  choicePutWithinRealSeconds: 2, // ER-DRIVE-05
  choiceStandsRealSeconds: 14, // no answer by then is driving off, if he has moved away; staying is stopping
  drivesOffBeyondMetres: 25,
  helpCostsGameMinutes: 14,
  // the firm's name after a drive-off (ER-DRIVE-10)
  driveOffCostsFirmGameDays: 5,
  driveOffFaresLostShareAtFirst: 0.6,
  helpedFaresLostShareAtFirst: 0.15,
  helpedCostsFirmGameDays: 2,
  // the ambulance (A22)
  ambulanceArrivesGameMinutes: 10,
  phoneReachMetres: 3,
  neighbourRingsWithinMetres: 30,
  neighbourRingsAfterGameMinutes: 3,
  // the horn (A32)
  hornReachByDayMetres: 60,
  hornReachByNightMetres: 95,
  hornNightFromHour: 22,
  hornNightUntilHour: 6,
  hornRainCutsShare: 0.3,
  hornBringsFareOutWithinMetres: 15,
  hornFareOutRealSeconds: 6,
  hornLongBlastRealSeconds: 1.2,
  hornStepsAsideWithinMetres: 14,
  // the patrol car and stops (A12)
  patrolSeesWithinMetres: 60,
  farOverTheLimitMph: 33, // the town's band tops at about 30; ordinary fast driving is not stopped
  stopTakesGameMinutes: 6,
  stopPulledOverBelowMetresPerSecond: 0.6,
  stopRefusedAfterRealSeconds: 9,
  chaseLostAfterUnseenRealSeconds: 7,
  chaseLostBeyondMetres: 110,
  chaseEndsByRealSeconds: 85, // ER-POL-04: always over within 90
  chaseCaughtWithinMetres: 7,
  chaseCaughtBelowMetresPerSecond: 1.5,
  chaseCaughtAfterRealSeconds: 2.5,
  patrolTopMetresPerSecond: 15.2,
  patrolCruiseMetresPerSecond: 7,
  custodyHoursForDrivingOff: 6,
  // tails by car (A2)
  tailLooksEveryRealSecondsAtLeast: 8,
  tailLooksEveryRealSecondsAtMost: 16,
  tailMarkWithinMetres: 22, // the car is the mark; nearer than this at a look is caught
  tailRoofSignTimes: 1.5, // the firm's lit sign makes it worse
  tailArrivesWithinMetres: 14,
  // riding (A24)
  rideCruiseMetresPerSecond: 8.5,
  // taking a parked car (A27)
  takeForceRealSeconds: 6,
  takeForceNoiseMetres: 40,
  takeWithinMetres: 3.2,
  ownerFindsItGoneAfterGameMinutes: 180,
  // paint (A24)
  resprayCostsPence: 2500,
  resprayTakesGameMinutes: 600,
  // traffic (4.5.1): how hard a driver brakes for a person
  trafficBrakesMetresPerSecondSquared: 14,
};
export const SCHEDULES = {
  nev: [{ fromHour: 0, place: 'off' }],
};
export const PEOPLE = {
  // Neville Stather, who has the other minicab firm on the Hook (A14: a business, never a rival)
  nev: { ageYears: 47, nerveZeroToOne: 0.4, venalZeroToOne: 0.5, talkativeZeroToOne: 0.6, discretionZeroToOne: 0.4 },
};
