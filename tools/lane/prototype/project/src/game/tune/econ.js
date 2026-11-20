// The numbers of the system "econ" (money, debts, flows) and of the rule pieces money, debts, fights and talk:
// plain data, imports nothing. Units in the names, as rules.js. The older numbers of the same rules stay where
// they were, in rules.js (money, prices, ladder, talk); the pieces read both.
export const TUNE = {
  money: {
    // 2.7.4 rent and running costs. The firm's own drivers bring fares in whether he drives or not (DESIGN 5: the
    // lazy path), and their wages go out of the same takings; what is left over reaches his pocket at the week's count.
    runningCostsPence: 950, // the garage's petrol account and the radio, taken from the pocket
    runningCostsDueDayIndex: 3, // Thursday
    runningCostsDueHour: 12,
    driverTakesPerWorkingDayPence: 700, // one driver, one shift, into the fare book
    driverWagePerWeekPence: 3300,
    driversAtTheStart: 2,
    driverWorkingDaysPerWeek: 5,
    wagesPaidDayIndex: 4, // Friday
    wagesPaidHour: 9,
    weekCountDayIndex: 5, // Saturday: what the firm made after wages reaches his pocket
    weekCountHour: 10,
    firmFaresCountForTheWashShare: 0.25, // how much of the drivers' takings the book can also hide night money behind
    weekLengthDays: 7,
    // ER-MONEY-03's two scripted weeks
    faresAloneWeekFaresPerDay: 3,
    faresAloneWeekFarePence: 210,
    faresAloneWeekDrivingDays: 4, // Tuesday to Friday morning
    // the inspection reads every week the books went off, and every fare written for an hour he was elsewhere
    booksHoldWithOffWeeksAtMost: 0,
    booksThinWithOffWeeksAtMost: 2,
    booksThinWithLiesAtMost: 2,
    alibiFareMinutesEitherSide: 30, // a fare's hour in the book covers him this long either side
    owesInWordsFromPence: 1, // "nothing owed" below this
  },
  flows: {
    keepsLines: 400, // the last lines kept one by one; older ones are kept as sums, so the total is never lost
  },
  debts: {
    // What is in each debtor's purse when Tom comes for it (canon: nobody pays more than the purse holds).
    // Darren pays in what he hears, Wayne in goods, Lee stands, Julie cannot pay, Dennis has the money.
    pursePence: { darren: 300, wayne: 500, lee: 400, julie: 0, dennis: 8000 },
    goodsWorthPence: { wayne: 2500 }, // goods from the pawn's back room, taken against the debt at their fence worth
    wordWorthPence: { darren: 400 }, // what one true piece of news takes off his debt
    paysWhenFearAbove: 0.45,
    paysWhenRegardAbove: 0.35,
    paysOnRegardOnlyWhenOwingAtMostPence: 1500,
    // what each outcome is to the street (the kinds table's own scale: -1 menace to 1 decent)
    squeezedReadsMenace: -0.5,
    paidQuietlyReads: -0.1,
    struckOutReadsDecent: 0.6,
    squeezedAPennilessOneReadsMenace: -0.8, // Julie: shame
    regardLostWhenSqueezed: 0.2,
    regardAddedWhenStruckOut: 0.35,
    fearAddedWhenSqueezed: 0.15,
  },
  fights: {
    rungCount: 8,
    mostEndByRung: 4,
    // the seven slots (0 precursor, 1 draw, 2 act, 3 victim, 4 actor, 5 flight, 6 aftermath) each rung shows the street
    slotCount: 7,
    fairFightTomWinsShareAtLeast: 0.35, // a fair one-on-one is roughly even
    fairFightTomWinsShareAtMost: 0.65,
    patientWinsShareAtLeast: 0.55, // ER-FIGHT-07
    masherWinsShareAtMost: 0.3,
    twoOnOneTomWinsShareAtMost: 0.25, // two against one is deadly
    threeOnOneTomWinsShareAtMost: 0.08, // three is a beating
    simulatedFights: 10000, // ER-FIGHT-05
    simStepRealSeconds: 0.05,
    simEndsAfterRealSeconds: 90,
    fallKillsWithinRealSecondsOfABlow: 3,
    fallAgainstHardEdgeChance: 0.04, // a man put down within reach of a kerb, wall or step lands on it this often
    fallOnHardEdgeKillsChance: 0.12, // and then, rarely, it kills (ruling 30 Oct)
    hardEdgeNearChance: 0.5, // how often the simulated ground has a kerb, wall or step in reach
    knockOutRealSecondsAtLeast: 10, // C7
    knockOutRealSecondsAtMost: 30,
    readableBlowRealSecondsAtLeast: 0.45, // C5, ER-FIGHT-02
    readableBlowRealSecondsAtMost: 0.8,
    jabBandRealSeconds: [0.25, 0.4], // C2
    heavyBandRealSeconds: [0.63, 0.85],
    heavyMissBandRealSeconds: [0.7, 0.9],
    hitStopJabBandRealSeconds: [0.025, 0.05], // C3
    hitStopHeavyBandRealSeconds: [0.06, 0.12],
    lightReactionBandRealSeconds: [0.5, 0.7], // C4
    heavyReactionBandRealSeconds: [0.9, 1.3],
    jabsToEmptyBand: [6, 10], // C11
    heaviesToEmptyBand: [3, 4],
    emptyToFullBandRealSeconds: [4, 8],
    swingGapBandRealSecondsAtLeast: 0.4, // C8
    chairBlowsBand: [1, 3], // C12
    brickBlowsBand: [2, 5],
    heaviesToPutAManDownBand: [3, 6], // C15
    patientReadsTellShare: 0.85, // the scripted patient fighter guards or slips this share of the blows he can read
    masherGuardsShare: 0, // the mashing one never does
    plainReadsTellShare: 0.2, // an ordinary player on a first evening
    counterAfterBlockDamageTimes: 1.5,
    guardHeldAfterAReactionRealSeconds: 0.4, // a man who has just been hit keeps his hands up this much longer
    swingsAgainAfterAReactionRealSeconds: 0.25, // out of a reaction he swings again this soon
    guardUpStopsLightChance: 0.85, // with his guard up a jab mostly lands on his arms, and the jabber is left open
    guardUpStopsHeavyChance: 0.45,
    tiredBlowDamageTimes: 0.5, // out of breath: half the blow, and slower
    tiredBlowSlowerTimes: 1.6,
    readingHarderPerExtraManShare: 0.5, // each man more makes each blow this much harder to read
    patientJabsAboveBreath: 0.6,
    patientJabsPerRealSecond: 0.6,
    plainBlowsPerRealSecond: 1.6,
    plainHeavyShare: 0.3,
    watchersKeepMetres: 3,
    // weapon tiers: 0 fists, 1 things to hand, 2 carried, 3 firearms; what the town makes of a blow rises by tier
    tierCrimeLevel: [2, 2, 3, 4],
    tierReadsMenace: [-0.5, -0.6, -0.8, -1],
    conditionWordsAtHurt: [0.2, 0.45, 0.7, 0.95],
  },
  talk: {
    liveReplyHeardWithinRealSeconds: 2, // ER-TALK-01: or the written line plays
    liveReplyDroppedAfterRealSeconds: 8, // slower than this it is dropped with a brush-off
    ownLineAgainAfterDays: 1, // ER-TALK-02
    sharedLineAgainAfterDays: 7,
    closingLinesEachAtLeast: 3,
    sceneWithoutChoiceRealSecondsAtMost: 60, // ER-TALK-06
    notAPlainYesLines: 170, // ER-TALK-03's count
    reportKeepsLines: 60, // ER-TALK-07: the reports kept in the save
    suggestedLinesAtMost: 3,
  },
};
export const SCHEDULES = {}; // { personId: rows } in the shape of RULES.schedules
export const PEOPLE = {}; // { personId: numbers } in the shape of RULES.people
