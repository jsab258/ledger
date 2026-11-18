// LEDGER. Every rule's number, in one table. The game reads its numbers from here and nowhere else, and the
// test hook shows the same table as LEDGER.rules.
//
// Units are in the names: Metres, Radians, Pence, GameMinutes (minutes of the game's clock), RealSeconds
// (seconds of play at normal speed), Hour (hour of the game's day, 17.25 is quarter past five), Share (0 to 1).
// Light is 0 (black) to 1 (full daylight). Clarity is how well a watcher has him, 0 to 1.
export const RULES = {
  time: {
    weekStartsGameMinute: 936, // Monday 3.36pm, off the bus
    realSecondsPerGameHour: 45,
    duskStartsHour: 17.25,
    nightFullHour: 18.75,
    dawnStartsHour: 6.25,
    dayFullHour: 7.75,
    smallHoursFromHour: 23.5, // from here until smallHoursUntilHour, simply being out is worth remarking
    smallHoursUntilHour: 5,
  },

  seeing: {
    // how far he can be seen: rangeInBlackMetres + rangeAddedByFullLightMetres * light ^ lightCurvePower
    rangeInBlackMetres: 4,
    rangeAddedByFullLightMetres: 44,
    lightCurvePower: 1.2,
    rainCutsRangeByShare: 0.3,
    mistAtNightCutsRangeByShare: 0.22,
    headlampsSeenFromMetres: 34,
    indoorsSeenFromMetres: 14,
    viewHalfAngleRadians: 1.08,
    windowViewHalfAngleRadians: 1.35,
    closeByMetres: 3, // this near, a watcher catches him almost side-on
    closeByViewHalfAngleRadians: 1.9,
    leastClarity: 0.05,
    // attention fills while he is in view; when it reaches 1 the watcher takes it in
    attentionPerRealSecond: 0.45,
    attentionPerRealSecondPerClarity: 1.4,
    attentionFasterWhenRemarkableTimes: 1.5,
    attentionFadesPerRealSecond: 0.4,
    plainSightingEveryGameMinutes: 20,
    // knowing who it is
    knowsHimAboveFamiliarity: 0.5,
    faceBase: 0.35,
    facePerClarity: 0.65,
    coatAtNightFaceTimes: 0.4,
    coatHidesWhenNightAbove: 0.5,
    inCabCloseAndLitFaceTimes: 0.6,
    inCabOtherwiseFaceTimes: 0.1,
    inCabCloseMetres: 10,
    inCabLitAboveLight: 0.3,
    namesHimAboveFace: 0.36, // "that was Tom Nowak"
    placesHimAboveFace: 0.2, // "that was the new owner"
    // how sure a witness is: (sureBase + surePerClarity * clarity), times sureIfNotNamedTimes unless they named him
    sureBase: 0.35,
    surePerClarity: 0.65,
    sureIfNotNamedTimes: 0.85,
    heatAddedToSeverity: 0.3,
    familiarityPerWitnessedAct: 0.02,
    familiarityPerWitnessedActIfKnown: 0.05,
    familiarityPerPlainSighting: 0.012,
    familiarityPerPlainSightingPerClarity: 0.02,
    familiarityPerPlainSightingIfKnown: 0.02,
    familiarityPerPlainSightingIfKnownPerClarity: 0.03,
    strangerFamiliarityStopsAt: 0.6,
    // remarkable simply by being seen
    coatByDayWhenNightBelow: 0.35,
    runningAtNightWhenNightAbove: 0.7,
    runningFasterThanMetresPerSecond: 3,
    sameSightingLastsGameHours: 2, // one ongoing act in one street is one event for this long
  },

  noise: {
    // how far a sound carries: its base radius, times the hour, less rain
    standingMetres: 0.5,
    walkingMetres: 5,
    runningMetres: 12,
    cabIdlingMetres: 8,
    cabAddedAtSpeedMetres: 22,
    cabFullNoiseAtMetresPerSecond: 12,
    stillBelowMetresPerSecond: 0.2,
    noonTimes: 0.5, // 10am to 4pm
    noonFromHour: 10,
    noonUntilHour: 16,
    deadOfNightTimes: 2, // midnight to 5am
    deadOfNightUntilHour: 5,
    earlyTimes: 1.5, // 5am to 7am
    earlyUntilHour: 7,
    lateEveningTimes: 1.3, // from 10pm
    lateEveningFromHour: 22,
    otherwiseTimes: 0.8,
    rainCutsByShare: 0.6,
    throughAWindowTimes: 0.7,
    burstFadesMetresPerRealSecond: 8,
    wakesASleeperAboveMetres: 9,
    remarkedInSmallHoursAboveMetres: 7,
    sameNoiseRemarkedEveryGameMinutes: 90,
    heardSure: 0.25,
    heardHeat: 0.3,
    alertLastsRealSeconds: 3,
  },

  // what a memory does to the person who holds it
  memory: {
    logKeepsLines: 600,
    coatLinkedToHimSureTimes: 0.7, // "the man in the coat was the new owner": less sure than seeing his face
    cabLinkedToHimSureTimes: 0.6,
    strangerLinkedAboveFace: 0.2,
    strangerLinkedAboveSure: 0.6,
    strangerLinkedAboveFamiliarity: 0.55,
    linkedAsTomAboveFace: 0.36,
    regardPerSeenAct: 0.26, // times the act's value and how sure they are
    regardPerToldAct: 0.15,
    uprightMindsBadActsTimes: 1.4,
    fearFromSeriousCrimeSeen: 0.18, // times (fearNerveBase - nerve)
    fearFromSeriousCrimeTold: 0.07,
    fearNerveBase: 1.2,
    seriousCrimeFromLevel: 2,
    heatAddedWhenSeenAgain: 0.08,
    heardSure: 0.3,
    heardHeat: 0.3,
    alertLastsRealSeconds: 4,
    partyNamesHimAboveFamiliarity: 0.15,
    partyFace: 0.9,
    partyFamiliarityGain: 0.12,
    heatAddedToSeverity: 0.3,
  },

  gossip: {
    // how readily two people talk: (base, plus closeFriendsAdded), times how talkative each is
    affinityBase: 0.42,
    closeFriendsAdded: 0.38,
    tellerTalkBase: 0.4,
    talkativeIfNotSet: 0.6,
    listenerTalkBase: 0.6,
    listenerTalkShare: 0.4,
    chanceTimesAffinity: 0.9,
    withinMetresOnStreet: 4.8,
    withinMetresIndoors: 8,
    notWorthTellingBelowHeat: 0.12,
    storyScoreSeverityBase: 0.4,
    storyNotAboutHimTimes: 0.6,
    discretionIfNotSet: 0.25,
    toldSureTimes: 0.8, // each telling is less sure
    toldHeatTimes: 0.92,
    tellerHeatAdded: 0.12,
    talkPoseRealSeconds: 5,
    tomCatchesThemWithinMetres: 18,
    lookAtHimRealSeconds: 4,
    passerByWithinMetres: 3.2,
    passerByTellsAboveHeat: 0.2,
    passerByChance: 0.35,
    heatFadeGameMinutes: 1700,
    neverForgottenHeat: 0.6,
    // it comes back: when someone says it to his face
    saysItAboveHeat: 0.12,
    grudgeSpokenAfterGameMinutes: 240,
    saysScoreSeverityBase: 0.3,
    nextRemarkAfterGameMinutes: 40,
    namesTheTellerAboveRegard: 0.1,
  },

  // what the street calls him: how well it knows him, not how much it likes him
  naming: {
    knowsOfInheritance: 0.25,
    perKindOfActKnown: 0.09,
    kindsCountedAtMost: 6,
    perFamiliarity: 0.4,
    levelOneFromScore: 0.2, // "the new owner"
    levelTwoFromScore: 0.5, // "Nowak"
    levelThreeFromScore: 0.8, // "Tom"
    levelFourFromScore: 1.05, // "Tommy"
    townLevelNeedsShareOfLocals: 0.4,
    notNamedLoudnessTimes: 0.6,
    menacePerCrimeKnown: 0.12,
    menaceSeriousCrimeTimes: 1.6,
    menaceCountsWhenValueBelow: -0.5,
    menaceAtMost: 0.45,
  },

  police: {
    // a statement needs someone who saw him plainly, is not frightened or bought, and has not warmed to him
    statementNeedsSureAtLeast: 0.55,
    noStatementIfFearAtLeast: 0.5,
    uprightStaysQuietAboveRegard: 0.05,
    othersStayQuietAboveRegard: -0.15,
    violentFromCrimeLevel: 2,
    comesNextDayAtHour: 9,
    arrivesAtXMetres: 6.4, // the top of Quay Street
    arrivesAtZMetres: -86,
    walkingMetresPerSecond: 1.25,
    chasingMetresPerSecond: 3.3,
    chaseHurry: 3.2,
    looksAgainEveryRealSeconds: 2,
    looksAgainWhenChasingEveryRealSeconds: 0.6,
    speaksWithinMetres: 3.2,
    catchesWithinMetres: 1.5,
    seesHimWithinMetres: 40,
    losesHimAfterRealSecondsUnseen: 7,
    losesHimBeyondMetres: 70,
    chaseLastsAtMostRealSeconds: 60,
    runningNoiseMetres: 22,
    heldGameHours: 4,
    heldGameHoursIfViolent: 5,
    heldGameHoursAddedIfHeRan: 2,
    briefBillPence: 2500,
    briefBillPenceIfHeRan: 4000,
    releasedAtXMetres: -5.6,
    releasedAtZMetres: 22,
    // DS Ellis asks along the street when the talk about him is loud enough
    ellisFirstDayIndex: 3, // Thursday (Monday is 0)
    ellisLastDayIndex: 4,
    ellisFromHour: 10,
    ellisUntilHour: 13,
    ellisComesAtLoudness: 2.2,
    ellisAsksPeopleAtMost: 5,
    ellisWalkingMetresPerSecond: 1.3,
    ellisStopsWithinMetres: 2.6,
    ellisAsksForRealSeconds: 5,
    ellisLeavesAfterRealSecondsLooking: 60,
    ellisSeeksHimWithinMetres: 70,
    ellisSpeaksWithinMetres: 3,
    askedMemoryHeat: 0.9,
  },

  money: {
    startsWithPocketPence: 2350,
    washedSafelyPence: 1000, // the fare book hides this much, plus washedSafelyShareOfFares of fares taken since
    washedSafelyShareOfFares: 0.8,
    overWashingCostsSheilaRegard: 0.12,
    bookFarePence: 180, // how Sheila counts fares when the book stops adding up
    bookFaresAtLeast: 3,
    rentPence: 1800,
    rentDueDayIndex: 4, // Friday
    rentLateFromHour: 18, // "Friday, by six"
  },

  // what things cost and what is owed, in pence
  prices: {
    ronWatchesTheDoorPence: 500,
    darrenSaysWhatHeHeardPence: 300,
    darrenPutsAGoodWordAboutPence: 500,
    scrapyardCollectionPayPence: 10000,
    eveningPaperPence: 20,
    chipsPence: 45,
    coshPence: 800,
    flickKnifePence: 1200,
    owedByIvesonPence: 8000,
    owedByLeePence: 1500,
    owedByDarrenPence: 2200,
    owedByJuliePence: 900,
    owedByWaynePence: 3000,
  },

  jobs: {
    mondayBagPayPence: 6000,
    mondayBagFromHour: 22.5,
    tuesdayParcelPayPence: 4000,
    tuesdayParcelFromHour: 22,
    doorsShutAtHour: 4,
    pickUpWithinMetres: 2.4,
    dropWithinMetres: 2.6,
    knockNoiseMetres: 9,
    missedFromHourNextDay: 3.5,
    missedUntilHourNextDay: 12,
  },

  fares: {
    flagFallPence: 80,
    penceAddedPerMetre: 0.9,
    roundedToPence: 10,
    shortestRunMetres: 60,
    offerStandsRealSeconds: 26,
    radioFromHour: 7,
    radioUntilHour: 23.2,
    firstOfferAfterRealSeconds: 9,
    nextOfferAfterRealSecondsAtLeast: 16,
    nextOfferAfterRealSecondsAtMost: 34,
    afterAMissedOfferRealSecondsAtLeast: 20,
    afterAMissedOfferRealSecondsAtMost: 40,
    afterAFareRealSecondsAtLeast: 14,
    afterAFareRealSecondsAtMost: 30,
    stoppedBelowMetresPerSecond: 0.8,
    pickUpWithinMetres: 6,
    dropOffWithinMetres: 7,
    passengerStepsOutMetres: 1.6,
    passerByWalksOffForGameMinutes: 30,
    passengerFamiliarityGain: 0.15,
    passengerRegardGain: 0.08,
  },

  // the light on the ground: the same value the picture's corners and the seeing rule use
  light: {
    indoors: 0.85,
    daylightAtNight: 0.07, // what is left of the sky in the dead of night
    lampFullStrength: 0.95,
    dimLampTimes: 0.55,
    shopGlowTimes: 0.8,
    falloffPower: 1.5, // strength falls as (1 - distance / radius) ^ falloffPower
    behindAWallTimes: 0.06,
    wallShadowBeyondMetres: 1.5,
    underCoverTimes: 0.12,
    lampsStrikeWhenNightAbove: 0.3,
    lampsFullWhenNightAbove: 0.55,
    lateWindowsFromHour: 16.5, // Rita's window, the takeaway, the video shop
    lateWindowsUntilHour: 23.6,
    lateWindowsAgainAfterMidnightUntilHour: 0.6,
    earlyWindowsFromHour: 15.5,
    earlyWindowsUntilHour: 19.5,
    ferryLandingDarkFromHour: 23, // the landing goes dark after the last ferry
    ferryLandingDarkUntilHour: 5,
    gridCellMetres: 0.75,
  },

  weather: {
    // each kind of weather: how hard it rains and how thick the mist is, 0 to 1
    dry: { rain: 0, mist: 0.15 },
    drizzle: { rain: 0.28, mist: 0.35 },
    rain: { rain: 0.6, mist: 0.3 },
    heavy: { rain: 1, mist: 0.22 },
    mist: { rain: 0.06, mist: 0.9 },
    changesAfterGameMinutesAtLeast: 100,
    changesAfterGameMinutesAtMost: 240,
    settlesOverGameMinutes: 25,
    nightWeatherBeforeHour: 7,
    nightWeatherAfterHour: 20,
    streetWetsPerGameMinuteOfFullRain: 0.02,
    streetDriesPerGameMinute: 0.0012,
    streetNeverDrierThan: 0.45,
    rainingAboveRain: 0.1,
  },

  ticking: {
    gossipEveryGameMinutes: 4,
    memoriesFadeEveryGameMinutes: 10,
    longestSkipStepRealSeconds: 6,
    longestSleepStepRealSeconds: 5,
  },

  rest: {
    morningAtHour: 7.5,
    eveningAtHour: 18,
    lastFerryAtHour: 22.25,
    nightCountsUntilHour: 5, // before this, "the morning" is the same day's
    eveningOfferedUntilHour: 17.5,
    ferryOfferedUntilHour: 22,
    sleepHealsHurtBy: 0.35,
    deadOnHisFeetFromHour: 4.4, // out all night: he gets as far as his bed
    deadOnHisFeetUntilHour: 5.2,
    wakesAfterCollapseAtHour: 9,
    collapseHealsHurtBy: 0.25,
    teaAtTheCaffPence: 20,
    teaAtTheCaffGameMinutes: 25,
    chapelGameMinutes: 20,
    caffFamiliarityGain: 0.06,
    weekEndsUnansweredOnDayIndex: 5, // Saturday
    weekEndsUnansweredAtHour: 2,
  },

  beaten: {
    shareOfTheTinTaken: 0.5,
    plastersPence: 800,
    hurtAfterwards: 0.55,
    outForAtLeastGameMinutes: 90,
    outForGameHoursByDay: 2,
    nightBeforeHour: 6,
    nightAfterHour: 17,
    comesRoundAtHour: 7,
  },

  // the Ledger screen test
  ledger: {
    entryWordsAtMost: 22,
    unseenHeldAfterGameMinutes: 2, // "nobody saw" counts as a belief he held once this long has passed unseen
    weekSoFarLinesAtMost: 5,
    notedLineShowsRealSeconds: 4,
    notedLineAtMostEveryRealSeconds: 10,
    notedCountsAsFollowedWithinRealSeconds: 60,
    firstHourRealSeconds: 3600,
  },

  routines: {
    walkingMetresPerSecond: 1.35,
    over60MetresPerSecond: 1.1,
    frailMetresPerSecond: 0.95,
    // Out of Tom's sight the town runs at the clock's pace: people cover ground this many times faster, so
    // that routines keep time. Near him they walk at a natural pace and fall behind their hours.
    paceOutOfHisSightTimes: 3.2,
  },

  // what a watcher's body does, so that he can read it
  watching: {
    lookAfterWitnessRealSeconds: 2.5,
    lookAddedPerSeverityRealSeconds: 5,
    lookAtKnownManRealSeconds: 1.9,
    lookAtStrangerRealSeconds: 1.1,
    looksOnlyWithinMetres: 22,
    bodyReactsWithinMetres: 26,
    pauseInWalkRealSeconds: 0.9,
    pauseAddedPerSeverityRealSeconds: 1.6,
    pauseAgainAfterRealSeconds: 20, // one person pauses once for one act, and not again for this long
    stepBackRealSeconds: 3.4,
    stepBackIfNerveBelow: 0.62,
    stepBackWhenNightAbove: 0.5,
    glanceWhileTalkingRealSeconds: 2.6,
  },

  // what Tom himself can notice: only this goes in his Ledger
  noticing: {
    furthestMetres: 34,
    mustFaceBeyondMetres: 2.5,
    facingHalfAngleRadians: 0.9,
    darkWindowHidesBeyondMetres: 9,
    darkFigureHidesBeyondMetres: 7,
    darkBelowLight: 0.2,
  },
};
