// The numbers of the system "fightx" (fights above the feel layer; DESIGN 7, A29): plain data, imports nothing.
export const TUNE = {
  rungs: ['stare', 'square up', 'threaten', 'shove or grab', 'strike', 'weapon out', 'weapon used', 'kill'],
  mostConfrontationsEndByRung: 4,
  // odds: what each side's count does to the fight (two against one is deadly, three is a beating)
  swingAtOnceAtMost: 2,
  swingsApartRealSeconds: 0.4,
  tellRealSecondsAtLeast: 0.45,
  tellRealSecondsAtMost: 0.8,
  jabLandsRealSeconds: 0.3,
  heavyLandsRealSeconds: 0.7,
  slipTakesRealSeconds: 0.3,
  counterWindowRealSeconds: 0.35, // the first part of his recovery after a slip or a block
  grabHoldsRealSeconds: 2,
  // hurt each blow does, of a body that goes down at 1
  hurt: { jab: 0.09, heavy: 0.24, counter: 0.24, weaponBlunt: 0.42, weaponBlade: 0.5, blockedFist: 0.01, blockedHeavy: 0.06 },
  blockedHeavyStaggersRealSeconds: 0.25,
  // breath, not a bar: mashing empties him in a few jabs, back in a few seconds
  breathEmptyAfterFastJabs: 8,
  fastJabWithinRealSeconds: 0.55,
  breathBackRealSeconds: 6,
  emptyBlowsSlowerTimes: 1.6,
  // nerve: a man gives way when the pressure on him passes his nerve
  nervePressurePerRung: 0.12,
  nervePressurePerExtraManAgainst: 0.22,
  nervePressurePerHurt: 0.5,
  nervePressureWeaponShown: 0.3,
  nerveWatchedStandsLongerBy: 0.15,
  nerveCorneredStandsLongerBy: 0.2,
  // the fall rule: fists never kill; a fall against a kerb, wall or step within 3 s of a blow can, rarely
  fallKillsWithinRealSecondsOfABlow: 3,
  fallKillChance: 0.02,
  hardSurfaces: ['kerb', 'wall', 'step'],
  knockedOutRealSecondsAtLeast: 10,
  knockedOutRealSecondsAtMost: 30,
  watchersKeepMetres: 3,
  // things to hand break
  breaksAfterBlows: { chair: 2, brick: 3, 'dustbin lid': 4, 'wheel brace': 9999, bottle: 1, plank: 3 },
  carriedUnderTheCoatAtMost: 2,
  // fighter types (A29): how each behaves in the simulated fight
  types: {
    boxer: { guards: 0.7, rushes: 0.2, takes: 1, keepsDistance: false },
    brawler: { guards: 0.1, rushes: 0.8, takes: 1, keepsDistance: false },
    'big man': { guards: 0.3, rushes: 0.3, takes: 1.6, keepsDistance: false },
    knife: { guards: 0.2, rushes: 0.55, takes: 0.9, keepsDistance: true },
  },
  // the simulated fight of the rule tests: a patient fighter reads this share of tells; how often the other man's blow is heavy
  sim: { patientReadsShare: 0.52, hisBlowHeavyShare: 0.45, hisSwingBase: 0.35, mashingTakesTimes: 0.62, emptyTakesTimes: 1.2, emptyRestsShare: 0.25, exchangesAtMost: 400 },
  streetPlaces: ['wall', 'doorway', 'railings', 'car bonnet', 'steps', 'kerb', 'quay edge'],
  beatenBackInControlRealSecondsAtMost: 60,
  kinds: { sparred: [0.1, 0.2, 0], searched_man: [0.5, -0.5, 1], quiet_blow: [0.7, -0.7, 2] },
  quietBlowWithinMetres: 1.4,
  quietBlowFromBehindAboveRadians: 2,
  quietBlowDownGameMinutes: 25, // 10 to 30 real seconds at the game's clock
  searchManWithinMetres: 1.6,
  sparRounds: 3,
  sparFromHour: 17,
  sparUntilHour: 22,
  // who is what kind of fighter in the written fights (A29): no two fights running use the same mix
  typeOf: { lee: 'brawler', dennis: 'big man', wayne: 'knife', ron: 'boxer', kevin: 'brawler', terry: 'boxer', darren: 'brawler', norman: 'big man', shaun: 'brawler' },
  slowerFightsAssistTellTimes: 1.25, // A6
  fightCameraMetres: 4.4, // band 3.5 to 5.0 (the feel measure of 20 Nov found 5.2)
  refusesToLayHandsOnAge: 60, // QUESTIONS 2: the prototype's standing rule
};
export const SCHEDULES = {};
export const PEOPLE = {};
