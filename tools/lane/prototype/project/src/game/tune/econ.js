// The numbers of the system "econ" (money, debts and what things cost): plain data, imports nothing.
// Units in the names, as rules.js. Money is in pence. First values, to be tuned by play (DESIGN 9).
export const TUNE = {
  startsWithPocketPence: 2350,
  rentPence: 1800,
  rentDueDayIndex: 4, // Friday
  rentLateFromHour: 18,
  washedSafelyPence: 1000, // the fare book can hide ten pounds
  washedSafelyShareOfFares: 0.8, // plus this share of the fares really driven since the last wash
  frontAddsWashPencePerWeek: 4000, // each front raises what can be washed (A15)
  driverWagePencePerWeek: 6500,
  carRunningPencePerWeek: 1200,
  fareFlagFallPence: 80,
  farePencePerMetre: 0.9,
  fareRoundedToPence: 10,
  firmDrivesWithoutHimFaresPerCarPerDay: 6, // the lazy path: the book fills slowly without him
  firmFareAveragePence: 190,
  firmFareShareToTheBook: 0.35, // what is left for the book after the driver's share and the petrol
  roundWordsToPence: 50,
  // the five debts of Mickey's book (DESIGN 4): what is owed and what the purse really holds
  debts: {
    darren: { owedPence: 2200, pursePence: 1000, paysIn: 'words' },
    wayne: { owedPence: 3000, pursePence: 600, paysIn: 'goods', goodsWorthPence: 3400 },
    lee: { owedPence: 1500, pursePence: 1500, paysIn: 'stands' },
    julie: { owedPence: 900, pursePence: 60, paysIn: 'cannot' },
    dennis: { owedPence: 8000, pursePence: 9500, paysIn: 'money', hasYardHand: true },
  },
  squeezedRegardLost: 0.2,
  squeezedFearGained: 0.15,
  hardLookHoldsGameMinutes: 30, // a shove pays only on top of a hard look given this lately
  sheilaFinishesWithoutAFareAfterGameMinutes: 300,
  darrenStaysAfterGameMinutes: 20,
  firstNightStagingEndsAtGameMinute: 240, // four in the morning of the Tuesday: nobody is kept standing past it
  afterADeedLookWithinMetres: 14,
  afterADeedLookRealSeconds: 3,
  gathersNoNearerThanMetres: 3.2,
  gathersForRealSeconds: 7,
  forgivenRegardGained: 0.25,
  // prices of the shops' lists (A21), in pence
  prices: { cigarettes: 150, paper: 20, meal: 180, tea: 20, crowbar: 650, torch: 420, keyCut: 150, scrap: 30, decentJacket: 3200, goodOvercoat: 7800, secondHandCoat: 900, scarf: 250, hat: 400, barber: 300, stitches: 1500, usedCar: 65000, solicitorRetainer: 12000, respray: 9000 },
  fencePaysShareOfHonestPrice: 0.4,
  haggleOffersAtMost: 3,
  haggleSecondOfferAddsShare: 0.12,
  haggleThirdOfferAddsShare: 0.05,
  haggleHotGoodsCutShare: 0.25,
  haggleLikedAddsShare: 0.05,
  hotMarkFadesOverGameDays: 7,
  hotMarkFadesBeyondMetres: 300,
  crewCutShareOfTake: 0.25, // a man on a night job (A40)
  paidShortBelowShareOfCut: 0.9,
  paidShortLoyaltyLost: 0.2,
  paidFairLoyaltyGained: 0.05,
};
export const SCHEDULES = {};
export const PEOPLE = {};
