// The numbers of the system "town": plain data, imports nothing. Units in the names, as rules.js.
export const TUNE = {
  // how the prototype's memory of a sighting reads as the real town's rung (BRIDGE.md, "the bridge's reading")
  faceRungAboveFaceScore: 0.2,
  rungRecognised: 4,
  rungFace: 3,
  rungMark: 2,
  rungSilhouette: 1,
  certaintyAtLeast: 0.05, // the town refuses a certainty of nought
  toldHeatShareOfSeverity: 0.8, // a story the town passed to somebody is this hot in the prototype's show of it
  toldHeatAdded: 0.1,
  readsTheTownEveryGameMinutes: 6, // the town's own round
  ellisComesWithinGameHoursOfTheTownSayingSo: 30,
  quayStreetMickeysAboveZMetres: 24,
  quayStreetBusStopAboveZMetres: 14,
  quayStreetNewsagentAboveZMetres: -15,
  quayStreetRitasAboveZMetres: -50,
};
// Where he stands, as the real town's cast file names areas: the prototype's rooms and street zones (step 4's table).
export const AREA_OF_ROOM = {
  mickeys: 'mickeys', caff: 'cafe', fish: 'fish_market', laund: 'laundry', rita: 'ritas', coin: 'hals', news: 'newsagent',
  boarding: 'boarding_house', chapel: 'chapel', harbour: 'harbour_office', ada: 'adas', grocer: 'bus_stop', tangs: 'kiosk',
  iron: 'newsagent', tearoom: 'kiosk', chandler: 'ritas',
};
export const AREA_OF_ZONE = {
  "Mickey's yard": 'mickeys', 'the back lane': 'mickeys', 'the west alley': 'hals', 'the ferry landing': 'ferry',
  'the fish dock': 'fish_dock', 'the warehouse row': 'warehouses', "Iveson's yard": 'repair_yard', 'the quay': 'quay',
  'Chapel Lane': 'flats', 'the bridge': 'market', 'Copper Row': 'market', 'the market end': 'laundry',
  'Quay Street, the quay end': 'mickeys',
};
export const SCHEDULES = {}; // { personId: rows } in the shape of RULES.schedules
export const PEOPLE = {}; // { personId: numbers } in the shape of RULES.people
