// The numbers of the system "feel": the camera's arm by Tom's state, the lens, the turn, the screen's manners.
// Plain data, imports nothing. Units in the names, as rules.js.
export const TUNE = {
  camera: {
    // one arm, read from rows by Tom's state (DESIGN 17). "Back" is level distance behind the look point when the
    // player has not zoomed (the wheel scales every row alike).
    wheelNeutralMetres: 5.4, // the wheel's own value at which a row is used as written
    streetBackMetres: 3.1, // his ruling: 3.1 m back, feet in frame
    runBackMetres: 3.5,
    fightBackMetres: 4.3, // melee sheet C10: 3.5 to 5.0, both men's feet and the watchers
    fightBackAtLeastMetres: 3.6,
    fightBackAtMostMetres: 4.9,
    carBackMetres: 5.8, // driving sheet M10: 5 to 6.5 behind
    carHeightMetres: 1.8, // driving sheet M10: 1.6 to 2.0 up
    carLookHeightMetres: 1.35,
    carPitchSettlesRadiansPerSecond: 1.6,
    carPitchSettlesAfterIdleRealSeconds: 1.2,
    armBlendsPerSecond: 5, // a change of row is blended in well under a second
    // the lens. On foot the upright angle is fixed (86 degrees across on a 16:9 screen, his ruling); at the wheel
    // the angle across is set, and widens with speed (driving sheet M10: 60 to 65 at rest, 64 to 70 at 30 mph).
    footUprightFovDegrees: 56,
    carAcrossFovAtRestDegrees: 62.5,
    carAcrossFovAt30MphDegrees: 67,
    carAcrossFovAtMostDegrees: 69.5,
    thirtyMphMetresPerSecond: 13.41,
    fovBlendsPerSecond: 4,
    // the line from Tom to the camera is tested against the street's own solid shapes (awnings, shelters, the
    // landing's roof), as the publish gate tests it
    lineTestedEveryRealSeconds: 0.08,
    lineIgnoresNearerThanMetresOnFoot: 0.7,
    lineIgnoresNearerThanMetresAtTheWheel: 2.7,
    lineKeepsOffMetres: 0.35,
    lineLetsOutMetresPerSecond: 3.5,
    lineAtLeastMetres: 0.9,
  },
  turn: {
    // Tom's way and his body turn together: a reversal swings him round in about a quarter of a second, and his
    // feet wait for his body (found by the feel numbers: his way reversed in one frame, his body in 0.28 s)
    reversalOverRadians: 2.2,
    turnsRadiansPerSecondOnReversal: 12.5,
    stepsOffOnlyWithinRadians: 1.25, // he moves his way once his body is within this of it
    reversalSlowsToShare: 0.25,
  },
  screen: {
    promptRidesAboveSubtitlesByPixels: 10,
    promptRestsAtPixels: 168,
    subtitleLastsAtMostRealSeconds: 12, // by the wall clock, whatever the game's steps did
    doorPromptWithinMetres: 2.6, // a door gives its prompt anywhere within reach of it, not on one spot
    watchShowsRealSeconds: 2,
    streetClockReadWithinMetres: 30,
  },
  assists: {
    // DESIGN-ADDENDUM A6: each changes only its own thing
    slowFightTellTimes: 1.25,
    slowFightSwingersAtMost: 1,
    longWalkTimes: 1.5,
    captionShowsRealSeconds: 2.5,
    captionLoudFromMetres: 9,
    captionAtMostEveryRealSeconds: 1.5,
  },
};
export const SCHEDULES = {};
export const PEOPLE = {};
