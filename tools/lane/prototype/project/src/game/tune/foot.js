// The numbers of the system "foot" (being seen and heard, hiding, tails, chases, vaulting; DESIGN 2, A1 to A3, A23,
// A26, A32 to A34): plain data, imports nothing. First values, LEDGER's own.
export const TUNE = {
  // how far a watcher catches each rung in full light
  shapeAtMetres: 35,
  markAtMetres: 18,
  faceAtMetres: 8,
  recognisedAtMetres: 25, // only by somebody who knows him
  light: { daylight: 1, lamp: 0.7, unlit: 0.25, doorway: 0.12 },
  glanceRealSeconds: 0.35,
  knowingRealSeconds: 1.2,
  cueBeforeKnowingRealSecondsAtLeast: 0.8, // ER-EYES-03
  runningNoticedTimesFaster: 2,
  amongPeopleAtLeast: 3, // a group this size within amongPeopleWithinMetres doubles the glance
  amongPeopleWithinMetres: 2,
  amongPeopleGlanceTimes: 2,
  stillShapeOnlyBeyondMetres: 8, // a still figure in a doorway is a shape at most beyond this
  torchLightsHimAs: 0.7,
  // noise: how far each act carries by day in the dry; hourTimes and rainTimes scale it
  reachMetres: { footstep: 0, run: 14, slowWalk: 0, forcedDoor: 40, brokenGlass: 45, drawer: 2, forcedCupboard: 10, stone: 12, bin: 20, bark: 30, horn: 60, shout: 35, cab: 44, shot: 177, knock: 8, search: 2 },
  nightFootstepMetres: 3.6, // a footstep at three in the morning
  slowWalkHalvesFootsteps: 0.5,
  nightFromHour: 22,
  nightUntilHour: 5,
  nightReachTimes: 2,
  rainReachTimes: 0.6,
  hornFareComesWithinMetres: 15,
  hornFareComesWithinRealSeconds: 10,
  // tails (A2)
  targetLooksBackEveryRealSecondsAtLeast: 20,
  targetLooksBackEveryRealSecondsAtMost: 40,
  cabBehindTwiceIsADoubt: 2,
  // chases (A3, DESIGN 8)
  runnerSpeedShareOfToms: 0.95,
  collarWithinMetres: 1,
  lostAfterUnseenRealSeconds: 7,
  lostBeyondMetres: 70,
  chaseEndsWithinRealSeconds: 90,
  constableLooksRoundGameMinutes: 60,
  constableLooksRoundRealSecondsAtMost: 30,
  // vaulting (A26)
  vaultUnderMetres: 1.2,
  vaultTakesRealSeconds: 0.8,
  pursuerVaultTakesRealSeconds: 1.3,
  vaultNeedsRunning: true,
  // searching (A4, A33)
  searchRealSeconds: { drawer: 2, desk: 4, wardrobe: 5, till: 3, cupboard: 4, coat: 2, bag: 2, man: 3, shed: 5 },
  searchInTheDarkTimes: 2,
  // lifting from a pocket (A34)
  liftHoldRealSeconds: 2,
  liftCrowdAtLeast: 3,
  liftGoodLightAbove: 0.5,
  headTurnsBeforeFeltRealSeconds: 0.8,
  // taking a parked car (A27)
  takeCarRealSeconds: 6,
  // casing (A23)
  casingLearnsAfterGameMinutes: 30,
  // drawing a watcher away
  noiseHoldsAWatcherRealSeconds: 8,
  oiStopsAWalkerRealSeconds: 2,
  mannersAnsweredWithinRealSeconds: 1,
  // wardrobe and marks (A21)
  bruisesLastGameDays: 3,
  limpLastsGameDays: 1,
  barberLastsGameDays: 7,
  markedCaughtAtMetres: 18,
  // on-foot feel faults found on 20 Nov (the body takes this long to turn, so the way he moves eases with it)
  turnEasesOverRealSeconds: 0.28,
  // trespass (A10): warn, warn again, then act, within half a minute at worst
  trespassSecondWarningAfterRealSeconds: 8,
  trespassActsAfterRealSeconds: 20,
  trespassWorstRealSeconds: 30,
  hintAfterStandingStillRealSeconds: 4,
};
export const SCHEDULES = {};
export const PEOPLE = {};
