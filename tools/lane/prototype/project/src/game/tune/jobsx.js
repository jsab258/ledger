// The numbers of the system "jobsx" (the job template, DESIGN 4): plain data, imports nothing.
export const TUNE = {
  windowAtLeastGameHours: 2, // no lateness fail inside a shorter window (ER-JOB-04)
  directionsAtLeast: 2, // sources of direction a step (ER-JOB-02)
  approachesAtLeast: 2, // three keys: at least two scripted ways through (ER-JOB-03)
  ledgerLineWordsAtMost: 30,
  setPieceNotTwiceWithinRealMinutes: 30, // law 6
  minding: { paysPencePerGameHour: 300, countsAfterGameMinutes: 20 },
};
export const SCHEDULES = {};
export const PEOPLE = {};
