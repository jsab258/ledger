// The numbers of the system "rise" (DESIGN 14, with the dial of DESIGN 7, the firm of A14, fronts of A15 and
// hold-ups of A41): plain data, imports nothing.
export const TUNE = {
  rungs: [
    null,
    { name: 'the nephew', called: 'the new owner', opens: ['the street', 'the rank', 'the landing'] },
    { name: 'the firm is his', called: 'Nowak', opens: ["Mickey's locked office and the real book (on trust)", "Rita's back room"] },
    { name: "the Hook's firm", called: 'Tom', opens: ['the dock gate', "the Harbour Board's counter", 'a solicitor'] },
    { name: "the port's man", called: 'Tom to most, Tommy to two or three', opens: ['the sit-down', 'people step aside'] },
  ],
  rung2: { cars: 3, recruits: 1, answeredSheila: true },
  rung3: { cars: 5, fronts: 1, rounds: 1, contract: true, nightDesk: true },
  rung4: { fronts: 3, rounds: 2, menAtTheGate: true, brief: true },
  names: ['', 'the new owner', 'Nowak', 'Tom', 'Tommy'],
  nameHeardWithinGameDays: 1,
  // the escalation dial (ruling 18 Nov)
  dial: ['Fists', 'Shown', 'Fired', 'War'],
  dialFallsAfterQuietGameDays: 14,
  dialNeverBelowAfterRising: 1,
  carriersPerSideAtWar: 3,
  deathsAnActAtMost: 4,
  warNightFaresShare: 0.6,
  armedCarsAtWar: 2,
  // the firm (A14)
  ranks: { mickeys: { name: "the rank outside Mickey's", his: true }, ferry: { name: 'the ferry rank', daysToWin: 5 }, north: { name: 'the north road rank', daysToWin: 8 } },
  accounts: ['the cold-store shift contract', "the Harbour Board's late men", "a solicitor's office"],
  accountFaresPerDay: 4,
  otherFirm: { name: 'Portside Cars', cars: 2, owner: 'Len Wardle' },
  boardRealSecondsADayAtMost: 60,
  driversLeaveUnpaidAfterWeeks: 1,
  // fronts and rounds (A15)
  fronts: { laund: { name: 'the Washeteria', man: 'k_laund', sharePence: 30000 }, caff: { name: "Rinaldi's", man: 'grace', sharePence: 45000 }, unit: { name: 'the empty unit on Chapel Lane', man: 'shaun', sharePence: 20000 } },
  frontPaysPencePerWeek: 2500,
  roundPaysPencePerWeek: 4000,
  // hold-ups (A41)
  holdupFromRung: 2,
  holdupTillGivenRealSeconds: 8,
  holdupThreatenedRealSeconds: 4,
  holdupOneAWeekThenShopsShut: 1,
  holdupNotesHotGameDays: 7,
  holdupTargets: ['grocer', 'news', 'iron', 'tearoom', 'laund', 'fish', 'rita', 'chandler', 'harbour', 'takings'],
  holdupNeverReports: ['rita'],
  tillPenceByHour: { morning: 1500, afternoon: 4200, evening: 6500 },
  streetServesColdGameDays: 7,
  // property that reacts (2.12.5)
  office: [null, 'as Mickey left it: one desk, the cot, his photograph', 'a second desk, the back room open', 'a night desk, a board full of chalk, new chairs', 'a brief on the phone, men waiting on the bench'],
};
export const SCHEDULES = {};
export const PEOPLE = {};
