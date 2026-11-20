// The numbers of the system "firm" (fleet, drivers, ranks, accounts, fronts and rounds): plain data.
// DESIGN sections 12 and 14, DESIGN-ADDENDUM A14 and A15. First values; the 1990 prices are owed to research.
export const TUNE = {
  carNames: ['car one', 'car two', 'car three', 'car four', 'car five', 'car six'],
  carPricePence: 18000,
  carSeller: 'dennis', // a runner out of the yard; the lot on the north road is still to be put in the atlas
  carsAtMost: 6,
  strangerDriverFromCars: 4, // from the fourth car a stranger asks at the counter for a job
  nightDeskFromCars: 4,
  ranks: {
    mickeys: { name: "the rank outside Mickey's", spot: 'rank', held: true },
    ferry: { name: 'the ferry rank', spot: 'ferry2', held: false, wonAfterGameDaysThere: 5, heldBy: 'the other firm' },
    station: { name: 'the station rank', spot: 'station', held: false, wonAfterGameDaysThere: 7, heldBy: 'the other firm' },
  },
  accounts: {
    coldstore: { name: 'the cold-store shift contract', via: 'norman', needsCars: 3, needsRung: 2, cleanPenceAGameDay: 900, needs: [] },
    harbour: { name: "the Harbour Board's late men", via: 'susan', needsCars: 4, needsRung: 3, cleanPenceAGameDay: 700, needs: ['coldstore'] },
    solicitor: { name: "a solicitor's office", via: 'garbutt', needsCars: 4, needsRung: 3, cleanPenceAGameDay: 500, needs: ['harbour'], needsDress: 1 },
  },
  fareShareOfACarADayPence: 600, // what a car and its driver bring the book in a day without him
  // fronts: a share of a real business on the street, each run by a named man
  fronts: {
    launderette: { name: 'the launderette', keeper: 'k_laund', pricePence: 9000, washExtraPenceAWeek: 4000, cleanPenceAWeek: 1200 },
    caff: { name: "Rinaldi's", keeper: 'grace', pricePence: 14000, washExtraPenceAWeek: 5000, cleanPenceAWeek: 1500 },
    unit: { name: 'the empty unit on the parade', keeper: 'shaun', pricePence: 20000, washExtraPenceAWeek: 7000, cleanPenceAWeek: 800 },
  },
  frontByFavourNeedsRegardAbove: 0.3,
  frontByPressureNeedsFearAbove: 0.4,
  // rounds: payments collected on a day by one of his men
  rounds: {
    quay: { name: 'the quay stalls', nightPenceAWeek: 2500, collectedOnDayIndex: 5 },
    parade: { name: 'the parade shops', nightPenceAWeek: 4000, collectedOnDayIndex: 5 },
  },
  shortManBelowLoyalty: 0.4,
  shortManKeepsShare: 0.3,
  weekSettlesOnDayIndex: 5, // Saturday morning the men bring it
  weekSettlesAtHour: 10,
};
export const SCHEDULES = {};
export const PEOPLE = {};
