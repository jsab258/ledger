// The numbers of the system "crime" (the verbs of jobs done with the hands): plain data, imports nothing.
// Units in the names, as rules.js. First values, to be tuned by play (DESIGN 4, DESIGN-ADDENDUM A2, A4, A5, A23, A30, A33 to A35).
export const TUNE = {
  // A4 searching: a time and a noise by container; twice as long in a dark room without the torch (A33)
  search: {
    drawerRealSeconds: 2,
    deskRealSeconds: 4,
    wardrobeRealSeconds: 5,
    crateRealSeconds: 5,
    cupboardRealSeconds: 3,
    drawerNoiseMetres: 2,
    deskNoiseMetres: 3,
    wardrobeNoiseMetres: 4,
    crateNoiseMetres: 6,
    cupboardNoiseMetres: 3,
    forcedCupboardNoiseMetres: 10,
    darkBelowLight: 0.3,
    darkWithoutTorchTimes: 2,
    stopsWhenTomMovesMetres: 0.8,
    reachWithinMetres: 2.6,
  },
  // getting in: a key lent or copied, a back way a routine leaves open, or force
  entry: {
    forceRealSeconds: 3,
    forceNoiseMetres: 42, // the loudest thing in a quiet street, before the hour and the rain scale it
    forceMarkLastsGameMinutes: 1440,
    doorWithinMetres: 2.4,
    insideWithinMetres: 4.5,
    keyCopyPence: 150,
    ownerWarnsWithinMetres: 14,
    secondWarningAfterRealSeconds: 9,
    actsAfterRealSeconds: 24,
  },
  // A5 coat, pockets and storage
  pockets: { underTheCoatAtMost: 2, inTheHandAtMost: 1, drawerWithinMetres: 1.6 },
  // lifts and the hot mark: fades with value and distance while the owner never forgets
  hot: {
    cheapBelowPence: 1000,
    dearFromPence: 5000,
    cheapFadesPerGameDay: 0.5,
    middlingFadesPerGameDay: 0.25,
    dearFadesPerGameDay: 0.1,
    offTheOwnersStreetTimes: 0.5,
    coldBelow: 0.15,
  },
  // fencing at Rita's back room, and A30's haggle of three offers at most
  fence: {
    shareOfHonestPrice: 0.4,
    hotCutsOfferByShare: 0.3,
    ceilingShareOfHonestPrice: 0.5,
    eachAskClosesShareOfGap: 0.5,
    offersAtMost: 3,
    holdsWhenRegardBelow: -0.2,
    ritaPursePence: 6000,
    walkingAwayCostsRegard: 0.05,
  },
  // A34 lifting from a pocket: fixed limits, never dice
  pocket: {
    holdRealSeconds: 2,
    headTurnsAtRealSeconds: 0.8,
    crowdAtLeastPeople: 3,
    crowdWithinMetres: 5,
    poorLightBelow: 0.5,
    besideWithinMetres: 1.3,
    attentiveFacingWithinRadians: 1.1,
    missedAtHour: 7,
  },
  // A35 damage by hand
  damage: {
    takesRealSeconds: 1.2,
    noiseMetres: 42,
    mendedAfterGameMinutes: 2880,
    ownerKnowsAtHour: 7,
    withinMetres: 2.6,
  },
  // A2 tailing on foot
  tail: {
    looksBackEveryRealSecondsCalm: 32,
    looksBackEveryRealSecondsWary: 20,
    waryAtOrBelowNerve: 0.45,
    lookLastsRealSeconds: 1.4,
    shapeBeyondMetres: 18,
    faceWithinMetres: 8,
    followsWithinMetres: 60,
    arrivesAfterStillRealSeconds: 4,
  },
  // minding: stood with somebody, seen at their shoulder
  mind: { standsWithinMetres: 4, countsAfterRealSeconds: 30 },
  // A23 casing: watching a place learns its hours, who holds the key and which way is left open
  casing: {
    fromAtLeastMetres: 10,
    fromAtMostMetres: 45,
    hoursAfterRealSeconds: 8,
    keyHolderAfterRealSeconds: 16,
    openWayAfterRealSeconds: 24,
    stopsWhenTomMovesMetres: 1.5,
  },
  // getting rid of things
  rid: { waterFromZ: 60.4, waterWithinMetres: 2.2, launderettePence: 100, privateWithinMetres: 12 },
  // 4.11.1 yard dogs: never hurt, by any verb
  dogs: {
    barksWithinMetres: 9,
    barkNoiseMetres: 30,
    ownerLooksWithinRealSeconds: 20,
    scrapQuietsForGameMinutes: 45,
    scrapPence: 30,
    barksAgainAfterRealSeconds: 14,
  },
  // collections: a debtor pays what his purse holds and the rest stays on the book
  debts: {
    pursePence: { darren: 400, wayne: 900, lee: 1500, julie: 0, dennis: 8000 },
    shareOfPurseBelowAThreat: 0.5,
    darrenWordWorthPence: 700,
    wayneGoodsWorthPence: 2600,
    julieWorksOffPencePerShift: 300,
  },
  goods: {
    clockPence: 2600,
    cameraPence: 4500,
    radioPence: 1800,
    cashboxPence: 8000,
    crateOfTinsPence: 1200,
  },
};
export const SCHEDULES = {};
export const PEOPLE = {};
