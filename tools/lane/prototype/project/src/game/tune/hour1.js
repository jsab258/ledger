// The numbers of the system "hour1": the first hour as staged (ONE-SHOT-PROMPT, section 4). Plain data, imports nothing.
export const TUNE = {
  ferryShotRealSeconds: 20, // one shot, skippable (Escape)
  arrivesAtXMetres: -55, // the foot of the gangway, on the pontoon
  arrivesAtZMetres: 73.5,
  arrivesFacingRadians: 3.14159, // looking up the gangway to the quay
  passingLineWithinMetres: 9, // a line in passing is said once, the first time he comes this near in sight
  headsTurnWithinMetres: 14, // people on the quay turn their heads as he passes
  headTurnLastsRealSeconds: 2.5,
  sheilaWalksMetresPerSecond: 1.5,
  sheilaSpeaksWhenHeIsWithinMetres: 2.6,
  thingWithinMetres: 1.2,
  stairClimbRealSeconds: 1.2,
  staysAfterHisLineGameMinutes: 120, // the people of the first afternoon stay put a while after their line
  stagingEndsAfterGameMinutes: 440, // or when Sheila's walk-round is done, whichever is first
  voiceLoudness: 0.6, // a spoken line in the mix, 0 to 1
  voiceFarLoudness: 0.3, // a line in passing from across the street
};
export const SCHEDULES = {};
export const PEOPLE = {};
