// The numbers of the system "life" (the town's days): plain data, imports nothing. Units in the names.
export const TUNE = {
  calendar: {
    // DESIGN-ADDENDUM A20; first values (the hours of 1990 research are owed, DESIGN section 2)
    sundayServiceFromHour: 9.5,
    sundayServiceUntilHour: 11.5,
    marketFromHour: 8,
    marketUntilHour: 15,
    matchStreetFullHours: [14.25, 16.75], // towards three, and coming away at five
    matchStreetFullForHours: 1,
    matchAwayFromHour: 14.5,
    matchAwayUntilHour: 17,
    bonfireFromHour: 19,
    bonfireUntilHour: 21,
    remembranceFromHour: 10.25,
    remembranceUntilHour: 11.75,
    weekdayShare: 0.85,
    matchCrowdShare: 1,
    bonfireCrowdShare: 1,
    marketDayHookShare: 0.55,
    sundayShare: 0.45,
    sundayServiceShare: 0.6,
    footballClub: 'Meridian Town', // invented; the brand bible still owes the club's name
    paperName: 'the Evening Mail', // as the prototype has it; the brand bible owes the paper's name
  },
  crowd: {
    walkersAtMost: 16,
    drizzleFromRain: 0.2,
    rainFromRain: 0.55,
    drizzleShare: 0.75,
    rainShare: 0.45,
    streetTalkEveryRealSeconds: 45, // DESIGN 11: everyday street talk at most every 45 s
    youngestCrowdAgeYears: 18, // canon: no children anywhere
    thinCheckedEveryRealSeconds: 3,
    thinOnlyBeyondMetres: 45, // nobody vanishes in his sight
  },
  paper: {
    linesAnEdition: 3,
    printsFromNewsworthy: 0.45,
    printsFromSure: 0.3,
    saidFromSure: 0.6,
    namesFromSure: 0.85,
    neverNamesFromCrime: 9, // she names him whenever she saw it herself; a lawyer's caution is the rival Agar's lever
    readerSureOfFact: 0.8,
    readerSureOfSaid: 0.5,
    readerSureOfRumour: 0.25,
    outAtHour: 15, // the Evening Mail is on the counters from three
    pricePence: 20,
    readersAnEdition: 6, // people of the Hook who read the local page that day
  },
  happenings: {
    quietRealSeconds: 1800, // none twice in 30 minutes
    sameStreetDays: 7, // none twice in a week on one street
    gapRealSeconds: 240, // one at a time, and a breath between
    checkedEveryRealSeconds: 5,
    startsWithinMetres: 38, // placed where he can come upon it
    endsAfterRealSeconds: 110, // each takes under two minutes
    favourAfterDays: 2,
    favourWithinDays: 9,
  },
  calls: {
    callsFromHour: 9,
    callsUntilHour: 21.5,
    coolerInsideGameMinutes: 1440, // a second call inside a day is "you again"
    visitsToHold: 3,
    liesThatEndIt: 2,
    visitTakesGameMinutes: 25,
  },
  marks: {
    // how long each mark stays on the town, in game minutes (2.19; a forced door "shows for a day", DESIGN 4)
    lastsGameMinutes: { forced_door: 1440, broken_window: 2880, tape: 4320, boarded: 10080, blood: 720, paint: 10080 },
  },
  hints: { hintsApartRealSeconds: 12, hesitatesAfterRealSeconds: 4 },
  todo: { withinRealSeconds: 30, walkMetresPerSecond: 3.2, cabMetresPerSecond: 9 },
  greet: { afraidFromFear: 0.5, angryBelowRegard: -0.35, likesFromRegard: 0.3, saidWithinMetres: 7, everyRealSeconds: 20 },
  boxing: { boutRounds: 3, clubFeePence: 50, trainsFromHour: 17, trainsUntilHour: 21.5 },
  stories: { foundWithinMetres: 3.2 },
};
// Philip Danby, a teacher by trade with the school shut (canon): at home on Chapel Lane, the tea room, the chapel
// hall of an evening. Dr Calvert, the retired doctor on the terrace side (ADDENDUM A21).
export const SCHEDULES = {
  danby: [
    { fromHour: 0, place: 'home' },
    { fromHour: 10, place: 'tearoom:t1', doing: 'sit' },
    { fromHour: 12, place: 'home' },
    { fromHour: 14.5, place: 'bench', doing: 'sit' },
    { fromHour: 16.5, place: 'home' },
  ],
  calvert: [{ fromHour: 0, place: 'home' }],
};
export const PEOPLE = {
  danby: { ageYears: 36, nerveZeroToOne: 0.45, venalZeroToOne: 0.05, talkativeZeroToOne: 0.55, discretionZeroToOne: 0.7 },
  calvert: { ageYears: 71, nerveZeroToOne: 0.8, venalZeroToOne: 0.5, talkativeZeroToOne: 0.2, discretionZeroToOne: 0.9 },
};
