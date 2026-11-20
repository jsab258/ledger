// The numbers of the system "feel" (camera and control faults measured on 20 Nov, and the screen's small rules):
// plain data, imports nothing. Bands are from the driving sheet's game set and the melee sheet.
export const TUNE = {
  fightCameraMetres: 4.4, // band 3.5 to 5.0 (measured 5.2)
  cabCameraBackMetres: 5.8, // band 5 to 6.5 (measured 8.5)
  cabCameraUpMetres: 1.8, // band 1.6 to 2.0 (measured 3.4)
  cabCameraTargetHeightMetres: 1.35,
  cabViewAcrossAtRestDegrees: 62.5, // band 60 to 65 (measured 87, never widening)
  cabViewAcrossAt30MphDegrees: 67, // band 64 to 70
  cabViewWidensUpToMetresPerSecond: 13.4, // 30 mph
  viewEasesPerSecond: 3,
  onFootViewUpDownDegrees: 56, // the street lens as built (his 86 degrees across at 16:9)
  // Tom no longer reverses his way in one frame while his body takes 0.28 s to turn: his pace falls while he turns
  turnSlowsAboveRadians: 1.2,
  turnSlowestShare: 0.12,
  subtitleClearsAfterRealSecondsAtMost: 9, // a subtitle that never clears is cleared
  promptLiftsOverSubtitle: true,
  doorPromptWithinMetres: 2.2, // a door gives its prompt from anywhere in reach, not one exact spot
  hintAfterStandingStillRealSeconds: 4,
  hintsNotTwoWithinRealSeconds: 12,
  nudgeAfterStandingAboutRealSeconds: 60,
  useKeyRestsAfterASceneRealSeconds: 0.6,
  firstHintAfterRealSeconds: 3,
  secondHintAfterRealSeconds: 25,
  arrivesAtXMetres: -44,
  arrivesAtZMetres: 55,
  arrivesFacingRadians: 1.45, // looking east, up the quay
  // the camera comes in front of a vehicle that would hide Tom or the cab (drive.js vehicleAt, player.js)
  cameraAndVehicles: {
    carRoofMetres: 1.8,
    busRoofMetres: 3.4,
    grownMetres: 0.15,
    carLengthMetres: 4.2,
    carWidthMetres: 1.7,
    cabHalfLengthMetres: 2.35,
    cabHalfWidthMetres: 1.0,
    armClearOfOwnCabMetres: 2.6, // the arm's first stretch is over the cab itself
  },
};
export const SCHEDULES = {};
export const PEOPLE = {};
