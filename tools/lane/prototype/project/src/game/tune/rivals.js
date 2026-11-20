// The numbers of the system "rivals" (DESIGN section 13): plain data. First values.
export const TUNE = {
  rungNames: ['unknown to them', 'noticed', 'a visit', 'pressure', 'a threat', 'a sit-down'],
  rivals: {
    jensen: {
      head: 'jensen', called: 'the Widow', after: 'his people', eyes: ['lee', 'kevin'], man: 'gary',
      pressure: 'a tax on his drivers at the dock gate', threat: 'his least loyal man offered a place',
      payPence: 1500, payRisesTimes: 1.5,
    },
    agar: {
      head: 'agar', called: 'Mr Agar', after: 'his clean money', eyes: ['susan'], man: 'clive',
      pressure: "a solicitor's letter about the private-hire licence", threat: 'an inspection of the cars',
      payPence: 4000, payRisesTimes: 1.25,
    },
    cammack: {
      head: 'cammack', called: 'Cammack', after: 'his cover', eyes: ['rita'], man: 'dean',
      pressure: 'trouble on Quay Street that brings the police', threat: 'a window put in, with his name said loud',
      payPence: 2500, payRisesTimes: 2,
    },
  },
  startsFromAct: 2,
  gameDaysBetweenRungsAtLeast: 3,
  gameDaysBetweenRungsIfTheRunEnded: 2,
  shownOnTheStreetAfterGameHours: 24, // a rung nobody said to his face is shown on his street by then
  paidHoldsGameDays: 7,
  defiedComesSoonerByGameDays: 1,
  counteredStepsBackRungs: 1,
  counteredHoldsGameDays: 10,
  // what defying each pressure costs, carried by people
  defyTaxFaresTimes: 0.8,
  defyTaxGameDays: 7,
  defyLetterBringsInspectionInGameDays: 5,
  defyTroubleSeenDeeds: 2,
  // the Fixer
  fixerReadPence: 1000,
  fixerMeetingPence: 2500,
  fixerTrucePence: 6000,
  fixerTruceGameDays: 14,
  fixerAt: 'caff:s2',
  fixerFromHour: 14,
  fixerUntilHour: 16.5,
  manWaitsAt: 'pave',
  headWaitsAt: 'rank2',
};
export const SCHEDULES = {
  garbutt: [{ fromHour: 0, place: 'off' }],
  agar: [{ fromHour: 0, place: 'off' }],
  jensen: [{ fromHour: 0, place: 'off' }],
  cammack: [{ fromHour: 0, place: 'off' }],
  gary: [{ fromHour: 0, place: 'off' }],
  clive: [{ fromHour: 0, place: 'off' }],
  dean: [{ fromHour: 0, place: 'off' }],
};
export const PEOPLE = {
  garbutt: { ageYears: 48, nerveZeroToOne: 0.8, venalZeroToOne: 0.9, talkativeZeroToOne: 0.5, discretionZeroToOne: 0.85 },
  agar: { ageYears: 61, nerveZeroToOne: 0.85, venalZeroToOne: 0.3, talkativeZeroToOne: 0.3, discretionZeroToOne: 0.95 },
  jensen: { ageYears: 52, nerveZeroToOne: 0.95, venalZeroToOne: 0.4, talkativeZeroToOne: 0.25, discretionZeroToOne: 0.9 },
  cammack: { ageYears: 29, nerveZeroToOne: 0.75, venalZeroToOne: 0.6, talkativeZeroToOne: 0.8, discretionZeroToOne: 0.2 },
  gary: { ageYears: 38, nerveZeroToOne: 0.7, venalZeroToOne: 0.5, talkativeZeroToOne: 0.3, discretionZeroToOne: 0.7 },
  clive: { ageYears: 44, nerveZeroToOne: 0.35, venalZeroToOne: 0.4, talkativeZeroToOne: 0.4, discretionZeroToOne: 0.8 },
  dean: { ageYears: 22, nerveZeroToOne: 0.55, venalZeroToOne: 0.6, talkativeZeroToOne: 0.8, discretionZeroToOne: 0.15 },
};
