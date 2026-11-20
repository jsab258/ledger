// The numbers of the system "fightx": reading and answering blows (DESIGN-ADDENDUM A29), fighter types, the
// quiet blow (A23), the weapon on a held input, the water in a fight (A11). First values; the melee sheet's bands
// (production/research/lane/FEEL-TARGETS-MELEE-2026-11-18.md) are the targets where it gives them.
export const TUNE = {
  defend: {
    slipSideMetres: 0.75, // a step and a duck to the side
    slipRealSeconds: 0.3, // A29 (to measure against the melee sheet)
    counterWindowRealSeconds: 0.55, // the first part of the other man's recovery after a slip or a block
    counterHitStopRealSeconds: 0.1,
    guardLetsHeavyStaggerRealSeconds: 0.18, // a blocked heavy blow staggers him a little
    weaponBreaksGuardShare: 0.75, // a swung weapon mostly comes through a guard
    breathSlowsFromStamina: 0.5, // below this his blows start slower
    breathSlowsWindUpByShareAtEmpty: 0.5,
    breathHeardBelowStamina: 0.35,
    breathHeardAtMostEveryRealSeconds: 2.5,
  },
  hold: {
    // the grab at rung 4: holds a man about 2 s
    reachMetres: 1.35,
    lastsRealSeconds: 2,
    pushMetres: 1.3,
    pushIntoPlaceHurts: 0.3,
    pushStaggerRealSeconds: 1.1,
    coolDownRealSeconds: 2.5,
  },
  types: {
    // every fight's men are one of a few kinds, so authored fights differ
    boxerGuardChanceTimes: 1.6,
    boxerWaitsTimes: 1.15,
    brawlerHeavyChance: 0.65,
    brawlerWaitsTimes: 0.6,
    bigManHurtTimes: 0.6, // slow to drop
    bigManWindUpTimes: 1.2,
    knifeStandsOffAddedMetres: 0.5,
    knifeDamageTimes: 1.5,
  },
  quiet: {
    // A23: from behind, on a man who has not seen him
    reachMetres: 1.3,
    behindHalfAngleRadians: 1.0,
    fistOutRealSeconds: 20, // 10 to 30 s (the melee sheet's figure for a fist)
    coshOutRealSeconds: 30, // LEDGER's own first value
    noiseMetres: 4,
    shapeSure: 0.2,
  },
  weapon: {
    heldToDrawRealSeconds: 0.4, // ER-FIGHT-08: a weapon comes out only on a held input
  },
  ends: {
    stepInAfterRealSeconds: 28, // people step in to a long fist fight
    stepInWatchersAtLeast: 3,
    stepInWithinMetres: 14,
  },
  water: {
    climbsOutAfterRealSeconds: 14, // A11: out within a minute, soaked, alive
  },
  tiers: { fists: 0, toHand: 1, carried: 2, firearm: 3 },
  sim: {
    // the duel model the pieces test ER-DEFEND-01 and ER-FIGHT-07 with (numbers of rules.js ladder, copied as first values)
    lightHurts: 0.14,
    heavyHurts: 0.3,
    foeLightHurts: 0.12,
    foeHeavyHurts: 0.24,
    blockLetsThrough: 0.25,
    openTimes: 1.5,
    lightCost: 0.11,
    heavyCost: 0.24,
    tooTiredBelow: 0.12,
    staminaBackPerSecond: 0.22,
    foeGuardStopsLight: 0.3,
    foeHeavyChance: 0.35,
  },
};
export const SCHEDULES = {};
export const PEOPLE = {};
