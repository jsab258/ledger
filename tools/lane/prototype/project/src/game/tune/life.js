// The numbers of the system "life" (the town's days; DESIGN 2 and 6, A18 to A20): plain data, imports nothing.
export const TUNE = {
  firstDay: { weekday: 0, dayOfMonth: 15, month: 10, year: 1990 }, // Monday 15 October 1990
  marketDayWeekday: 3, // Thursday, in Copper Row: it empties the Hook's shops
  matchWeekday: 5, // Saturday: the street fills at three and five
  matchFillsAtHours: [15, 17],
  sundayWeekday: 6, // shops shut, the chapel busy
  bonfireNight: { dayOfMonth: 5, month: 11 }, // a display on the quay, adults only
  remembranceSunday: { dayOfMonth: 11, month: 11 },
  paperWeekdays: [1, 4], // the paper comes out twice a week: Tuesday and Friday
  // how many of the crowd are out, by hour of the day (share of the crowd's most), dry weather
  crowdShareByHour: [0.03, 0.02, 0.02, 0.02, 0.05, 0.15, 0.35, 0.6, 0.85, 0.9, 0.85, 0.9, 1, 0.9, 0.8, 0.85, 0.95, 1, 0.8, 0.6, 0.45, 0.35, 0.2, 0.08],
  weatherOutShare: { dry: 1, drizzle: 0.75, rain: 0.45, heavy: 0.25, mist: 0.8 },
  marketDayHookShare: 0.6,
  matchHourShare: 1.4,
  sundayShare: 0.55,
  // how long a deed stays hot in talk, by kind (game days); a body never cools; the memory itself is for good
  coolsAfterGameDays: { manners: 1, sighting: 1, debt: 2, damage: 3, theft: 4, violence: 5, weapon: 6, holdup: 7, killing: null },
  // street happenings (A18)
  happeningNotTwiceWithinRealMinutes: 30,
  happeningNotTwiceAWeekOnOneStreet: 7,
  happeningLastsAtMostRealSeconds: 120,
  happeningReturnsAfterGameDays: 3,
  somethingNewAtLeastEveryRealMinutes: 5,
  idleProbeWithinRealSeconds: 30,
  waitShareAtMost: 0.1,
  talkShareAtMost: 0.3,
  drivingShareAtMost: 0.25,
  hourBudgetShares: { foot: 0.25, driving: 0.22, talk: 0.19, jobs: 0.17, fights: 0.08, ledger: 0.06, waiting: 0.03 },
};
export const SCHEDULES = {};
export const PEOPLE = {};
