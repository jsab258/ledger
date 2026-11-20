// The numbers of the systems "back" (it comes back: ONE-SHOT-PROMPT 2 and the first hour at 13:00; story S06) and
// "count" (the count with Sheila: part 26). Plain data, imports nothing.
export const TUNE = {
  litAbove: 0.3, // he is lit above this light value
  seenLitWithinMetres: 60, // under a lamp he is made out from far along the quay
  seenDarkWithinMetres: 12, // in the dark only from close by
  passesAfterGameMinutes: 60, // nobody carries it on the same hour it happened
  roadFromHour: 7.05, // the morning's road: the outfit's man to Ron, Ron to Darren
  roadUntilHour: 21,
  courierComesFrom: [[3.4, 45.5], [-30, 44], [40, 43.5], [-3.2, 4]], // up from the quay end of Quay Street, or the first of these Tom cannot see
  tellsWithinMetres: 2.2,
  headsTogetherRealSeconds: 5,
  headsSeenWithinMetres: 30,
  saysWithinMetres: 4.5,
  lookWithinMetres: 9,
  lookHeldRealSeconds: 3.2,
  backTurnedRealSeconds: 4,
  heldGameMinutes: 45, // a man sent to the rank or the pavement for this stays that long, and is sent again while it is still to do
  // the count
  countFromHour: 7.5,
  countUntilHour: 18,
  countWithinMetres: 2.7,
  smallerSumPence: 500,
  overWashingCostsSheilaRegard: 0.12,
};
