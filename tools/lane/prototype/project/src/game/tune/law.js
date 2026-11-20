// The numbers of the system "law": witnesses who walk to tell, and the police. Plain data, imports nothing.
// Units in the names, as rules.js. First values, to be tuned by play (DESIGN sections 2 and 8, addendum A3, A13, A36 to A38).
export const TUNE = {
  walk: {
    setsOffAfterRealSeconds: 4, // a witness who means to tell stands a moment, then goes
    lastsAtLeastRealSeconds: 30, // ER-EYES-04, when the walk starts in his sight
    longerWalksAssistTimes: 1.5, // the "longer walks" assist (A6)
    arrivesWithinMetres: 2.6,
    landsAnywayAfterGameMinutes: 150, // a walk nobody could follow still ends: she rang from somewhere
    friendWithinMetres: 45, // a friend this near on the street is who she tells first
    startsInSightWithinMetres: 40,
    nightIsFromHour: 21,
    nightIsUntilHour: 6,
  },
  stop: {
    talkedRoundAboveRegard: 0, // she can be talked round only if she does not think badly of him
    payBasePence: 500,
    payMorePencePerCrimeLevel: 500,
    paidOnlyIfVenalAtLeast: 0.3,
    threatWorksIfNerveBelow: 0.75,
    threatFearAdded: 0.6,
    threatRegardLost: 0.3,
    helpRegardAdded: 0.25, // walking her home, carrying her bag: a decent act the street may see
    helpStopsIfRegardThenAbove: 0.1,
  },
  reaction: {
    lookWithinMetres: 14, // ER-EYES-09: people this near a seen deed look
    lookForRealSeconds: 4,
    gatherForRealSeconds: 9, // one of them comes nearer, then drifts back
    gatherStopsShortMetres: 3,
    quietForGameMinutes: 60, // witnesses talk quieter for a game hour (ruling 23 Sep)
    quietTalkTimes: 0.5,
  },
  edge: {
    seenDeedsNeeded: 3, // A37: three seen deeds on one street
    withinGameMinutes: 2880, // within two game days
    easesGameMinutesAfterTheLast: 2880, // it eases as the talk cools; the memories stay
    setsOffSoonerTimes: 0.5, // witnesses set off to tell sooner
    constableVisitsTimes: 2, // and the constable walks it more often
  },
  custody: {
    windowGameHours: 6, // damage, a threat, a shove: the least
    windowOwnedUpGameHours: 2, // owns up: two hours and a caution
    woundingGameHours: 8,
    robberyGameHours: 12,
    killingGameHours: 22, // and then bail
    ranAddsGameHours: 2,
    underRealSeconds: 120, // ER-POL-03
  },
  stages: {
    nextStageNotBeforeGameMinutes: 30, // a stage's sign is shown this long before the next stage can begin
    manhuntSignBeforeArrestGameMinutes: 60, // ER-POL-05
    ellisTalkFromDayIndex: 3, // from day 4 for talk
    ellisTalkNeedsDayPeople: 3, // once three people of his day world pass talk of his nights
    caseStrengthPerStatement: 1,
    caseStrengthPerCharge: 2,
    caseStrengthPerOfficeFind: 2,
  },
  beat: {
    fromHour: 21.5,
    untilHour: 4.5,
    walkMetresPerSecond: 1.1,
    turnsWithinMetres: 2.5,
    heardWithinMetres: 30, // his boots are heard, or he is seen, from here
    seesWithinMetres: 22,
    noChallengeBeforeRealSeconds: 3, // ER-POL-02: heard or seen 3 s before he can challenge
    callsOutWithinMetres: 14,
    actsAfterCallingRealSeconds: 2.5, // he calls out, then walks up
    speaksWithinMetres: 3,
    chaseMetresPerSecond: 3.3,
    catchesWithinMetres: 1.5,
    losesHimAfterRealSecondsUnseen: 7,
    losesHimBeyondMetres: 70,
    chaseEndsWithinRealSeconds: 90, // ER-POL-04
    looksRoundAfterLosingGameMinutes: 60, // A3: he walks to where he last saw him and looks round about a game hour
    restsBetweenChallengesGameMinutes: 45,
    points: [
      [4.5, -60],
      [4.5, 30],
      [-30, 52],
      [30, 52],
    ], // Quay Street top to bottom, then along the quay
    carryingAtNightIsCause: true,
  },
  spot: {
    officerComesWithinGameMinutes: 20, // A36: a reported deed brings an officer to its spot
    officerStaysGameMinutes: 40,
    watchedUntilHour: 6, // the spot is watched ground until morning
    watchedWithinMetres: 16,
    ellisAfterABodyAtHour: 9,
  },
  bought: {
    pashbyPricePence: 2000, // PC Pashby looks away from a car
    pashbyLooksAwayTimesANight: 1,
    thwaitePricePence: 5000, // Sergeant Thwaite loses a statement, once
    thwaiteLosesStatements: 1,
    colleagueSeesWithinMetres: 25,
  },
  office: {
    noticeAtHour: 18, // ER-SEARCHED-01: the sign the evening before
    searchAtHour: 9,
    searchTakesGameHours: 2,
  },
  armed: {
    gunCallArrivesGameMinutes: 25, // dial 2: armed officers come from the station for gun calls, slowly
    warCarArrivesGameMinutes: 10, // dial 3: armed cars
    warStopSearchEveryGameMinutes: 180, // stop and search on the street
    warStopSearchFromHour: 8,
    warStopSearchUntilHour: 23,
    warArmedOfficersAtMost: 4, // guns stay rare, on their side too
  },
  find: {
    seenWithinMetres: 7, // A38: a routine that passes this near, in sight of what was left, finds it
    steppedOnWithinMetres: 3,
  },
  missing: {
    noticedAfterGameHours: 24, // a man who stops keeping his routine becomes the town's question
    askedAgainEveryGameHours: 48,
  },
  // People the real town's cast holds (BRIDGE.md): for these the town decides who goes to the police once it runs.
  townCast: ['sheila', 'ron', 'darren', 'alison', 'walsh', 'ada', 'june', 'rita', 'hal'],
};
export const SCHEDULES = {
  pashby: [{ fromHour: 0, place: 'off' }],
  thwaite: [{ fromHour: 0, place: 'off' }],
};
export const PEOPLE = {
  pashby: { ageYears: 44, nerveZeroToOne: 0.6, venalZeroToOne: 0.85, talkativeZeroToOne: 0.4, discretionZeroToOne: 0.7 },
  thwaite: { ageYears: 52, nerveZeroToOne: 0.8, venalZeroToOne: 0.7, talkativeZeroToOne: 0.3, discretionZeroToOne: 0.85 },
};
