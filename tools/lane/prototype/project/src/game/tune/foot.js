// The numbers of the system "foot": moving, hiding, manners, stopping, ground rules, chases on foot, marks.
// Plain data, imports nothing. Units in the names, as rules.js. First values, to be tuned by play.
export const TUNE = {
  moving: {
    slowWalkShare: 0.5, // A1: walking slowly halves the pace
    slowWalkFootstepReachShare: 0.5, // and halves his footsteps' reach
    limpWalkShare: 0.8,
    vaultTakesRealSeconds: 0.8, // A26 (to measure)
    vaultReachMetres: 2.6,
    vaultRiseMetres: 0.55,
    pursuerVaultTakesRealSeconds: 1.4, // a pursuer vaults the same places, slower
  },
  hiding: {
    // A1. The light scale is DESIGN 2's: daylight 1, a lamp 0.7, an unlit street 0.25, a doorway 0.12.
    doorwayLight: 0.12,
    stillAfterRealSeconds: 0.6, // standing this long in shadow is hiding
    stillInDoorwayByDayLightTimes: 0.6,
    torchLight: 0.7, // A33: a lit torch makes him count as lit at lamp value
    shapeAtMetres: 35,
    markAtMetres: 18,
    faceAtMetres: 8,
    knownAtMetres: 25,
    stillInDoorwayShapeOnlyBeyondMetres: 8,
    glanceRealSeconds: 0.35,
    glanceAmongPeopleTimes: 2,
    amongPeopleAtLeast: 3,
    amongPeopleWithinMetres: 2,
  },
  manners: {
    menuStaysRealSeconds: 4,
    reachesWithinMetres: 7, // a remark is said within 7 m (DESIGN 11)
    answeredWithinRealSeconds: 1,
    callStopsWalkerRealSeconds: 2,
    callHeardMetres: 18,
    shovePushesMetres: 0.7,
    shoveWithinMetres: 1.6,
    greetingAgainAfterGameMinutes: 60,
  },
  stopping: {
    seatWithinMetres: 2.2,
    wallWithinMetres: 0.9,
    loiterLookAfterRealSeconds: 20, // a man standing about at night with no reason draws a second look
  },
  ground: {
    warnAgainAfterRealSeconds: 8,
    actsAfterRealSeconds: 20, // within half a minute at worst (DESIGN 4, lead)
    warnerWithinMetres: 30,
    privateRoomsShutFromHour: 22,
    privateRoomsShutUntilHour: 6,
    yardPrivateFromHour: 19,
    yardPrivateUntilHour: 7,
  },
  noises: {
    stoneThrownMetres: 12,
    stoneHeardMetres: 14,
    binRattleHeardMetres: 18,
    binWithinMetres: 1.6,
    headTurnsForRealSeconds: 5,
    walksToLookShare: 0.4, // of those who heard and are not at work
  },
  time: {
    chapelBellFromHour: 7,
    chapelBellUntilHour: 21,
    chapelBellHeardMetres: 260,
    chapelX: -14,
    chapelZ: -67,
  },
  chase: {
    // A3
    runnerSpeedShareOfTomsRun: 0.95,
    collarWithinMetres: 1,
    collarBehindHalfAngleRadians: 1.9,
    lostUnseenRealSeconds: 7,
    lostBeyondMetres: 70,
    endsWithinRealSeconds: 90,
    constableLooksRoundGameMinutes: 60,
    tomRunsMetresPerSecond: 5.2,
  },
  marks: {
    // A21
    bruisesLastGameDays: 3,
    cutLipLastsGameDays: 3,
    limpLastsGameDays: 1,
    markedFromHurt: 0.45,
    remarkWithinMetres: 5,
    doctorPence: 600,
    doctorHalvesTimeLeft: 0.5,
    doctorX: -7.3,
    doctorZ: 24.5,
    doctorWithinMetres: 2.4,
  },
  water: {
    edgeWithinMetres: 3.2, // near enough to throw a thing in
    climbsOutWithinRealSeconds: 60,
    climbsOutAfterRealSeconds: 14,
  },
};
export const SCHEDULES = {};
export const PEOPLE = {};
