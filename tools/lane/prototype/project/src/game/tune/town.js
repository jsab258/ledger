// The numbers of the system "town" (the bridge to the real town code): plain data, imports nothing.
// Units in the names, as rules.js. None of these is a town rule: the rules are the game's own C++ code, compiled.
export const TUNE = {
  // how often the people the cast file has are brought up to date from the town's own talk (its rounds are 6 minutes)
  mindsReadFromTownEveryGameMinutes: 6,
  // The real rule (Perception::IdRung) gives a rung; the prototype's minds keep "who" and a face score. Rung to mind:
  faceScoreAtRung: [0, 0.05, 0.12, 0.5, 0.9], // someone, a silhouette, a mark, a face, recognised
  sureAtRung: [0.25, 0.4, 0.55, 0.8, 1], // a witness is only as sure as what they caught (ruling 30 Sep)
  // his face is toward a witness when the witness stands within this angle of the way he faces
  faceTowardHalfAngleRadians: 1.75,
  // in the cab his face can be caught only close and lit (the prototype's rule, kept: the real rule has no car)
  inCabFaceWithinMetres: 6,
  inCabFaceAboveLight: 0.5,
  // the runner's coat, collar up, hides the face once night is this far on (0 day to 1 night)
  coatHidesFaceWhenNightAbove: 0.45,
  // what the town is told of each of the prototype's kinds that is a crime (Offence: 0 suspicious, 1 damage, 2 assault,
  // 3 wounding, 4 robbery, 5 killing). A new kind may carry its own offence; else its crime level decides.
  offenceOfKind: { strike: 2, weapon_used: 3, kill: 5, knocked: 3, crash: 1 },
  offenceOfCrimeLevel: [0, 0, 2, 3, 5],
  // somebody the cast file does not have: the goodwill the real rule is asked with is this plus regard times the share
  hostLoyaltyBase: 0.5,
  hostLoyaltyPerRegard: 0.5,
  nerveIfNotSet: 0.5,
  // a witness this frightened, or bought, does not go to the police (a threat stops a report, never the street's talk)
  noReportIfFearAtLeast: 0.5,
  // a finder of damage they did not see done holds only the aftermath: this sure, never tied to him
  finderSure: 0.2,
  finderHeat: 0.5,
  // cooling by kind (DESIGN 2: talk cools, memory does not): game days until a story's heat in talk has halved.
  // A lead, 1 to 7 days by how grave the kind is; a killing never cools. The memory itself is never removed.
  coolsHalfInGameDaysByCrimeLevel: [1, 2, 4, 7, 7],
  coolsHalfInGameDaysIfDecent: 1.5,
  // where the nine people of both casts stand: false, by the prototype's own week (the story's scenes are staged on
  // it); true, by the real town's routine wherever the place has a spot on this map (ONE-SHOT-SIM-DIFFERENCES.md)
  nineStandByTheTownsRoutine: false,
  // the cast file's areas, each by a point on the prototype's map (metres), for "where he stands" and where a deed was
  areaAt: {
    mickeys: [7, 37],
    adas: [-8, 32],
    fish_market: [7.2, 26.8],
    bus_stop: [-5.9, 20.6],
    laundry: [7.2, 18.4],
    newsagent: [-7.2, 7.3],
    kiosk: [6, -11.2],
    cafe: [-7.2, -29],
    ritas: [7.2, -29],
    hals: [-7.2, -36],
    boarding_house: [7.2, -46.5],
    chapel: [-18.6, -67],
    market: [-30, -146],
    quay: [9, 46],
    quay_landing: [-47, 58],
    ferry: [-55, 62],
    harbour_office: [-28.5, 42],
    docks: [-70, 46],
    customs: [-40, 46],
    fish_dock: [52, 58],
    repair_yard: [66, 70],
    warehouses: [118, 42.6],
  },
  // rooms of the prototype's map that are inside an area of the cast file
  areaOfRoom: {
    mickeys: 'mickeys',
    ada: 'adas',
    fish: 'fish_market',
    laund: 'laundry',
    news: 'newsagent',
    caff: 'cafe',
    rita: 'ritas',
    coin: 'hals',
    boarding: 'boarding_house',
    chapel: 'chapel',
    harbour: 'harbour_office',
  },
  // the cast file's places, each by a spot of the prototype's map (routines.js resolve), where it has one
  spotOfPlace: {
    mickeys_office: 'mickeys:desk',
    mickeys_rank: 'rank',
    fish_counter: 'fish:queue',
    fish_front: 'pave',
    ritas_counter: 'rita:counter',
    ritas_step: 'ritaside',
    kiosk: 'phone',
    laundry_front: 'laundrygate',
    laundry_counter: 'laund:queue',
    quay_landing: 'shelter',
    quay: 'quaycorner',
    adas_step: 'adadoor',
    cafe: 'caff:table',
    cafe_front: 'corner2',
    pension_counter: 'news:queue',
    hals_shop: 'coin:counter',
    bus_stop: 'busstop',
    fish_dock: 'boxes',
    repair_yard: 'pier',
    harbour_office: 'harbourdoor',
    ferry_stop: 'ferry',
    warehouse_row: 'row1',
    chapel: 'chapelgate',
    chapel_hall: 'bench',
    market: 'market1',
    boarding_house: 'boarding:hall',
  },
};
export const SCHEDULES = {};
export const PEOPLE = {};
