// The numbers of the system "way" (finding the way, DESIGN-ADDENDUM A9): plain data, imports nothing.
export const TUNE = {
  lostNudgeAfterRealSeconds: 90, // ER-WAY-03: Tom's own line, once per goal, never inside 90 s
  lostOfferAfterRealSeconds: 180, // then the next person he passes offers the way
  lostOfferWithinMetres: 5,
  progressCountsMetres: 6, // getting this much nearer the goal is progress, and starts the count again
  arrivedWithinMetres: 9,
  goalFromToDoCheckedEveryRealSeconds: 2,
  nearWordsWithinMetres: 30, // "just along from here"
};
export const SCHEDULES = {};
export const PEOPLE = {};
