// The numbers of the system "shops" (spending, ADDENDUM A21, A30): plain data, imports nothing. Prices are first
// values for 1990 in pence (the period's price research is owed).
export const TUNE = {
  haggle: {
    openingShare: 0.4, // Rita's back room fences at about 0.4 of an honest price (DESIGN 4, lead)
    hotCutsShare: 0.5,
    regardAddsShare: 0.25,
    risePerAskShare: 0.06,
    topShare: 0.6,
    callsBack: true,
    honestShopRefusesAboveHot: 0.35,
  },
  // each shop: its room on the map, its counter list, the week's stock, its float, what it buys
  shops: {
    newsagent: { place: 'newsagent', room: 'news', keeper: 'k_news', pursePence: 4000, sells: { 'the paper': 20, 'twenty Mariners': 150, 'a box of matches': 8 }, stock: { 'the paper': 40, 'twenty Mariners': 30, 'a box of matches': 30 }, buys: [] },
    caff: { place: 'caff', room: 'caff', keeper: 'grace', sundayOpen: true, pursePence: 6000, sells: { 'a tea': 20, 'a dinner': 180, 'a bacon sandwich': 70 }, stock: { 'a tea': 200, 'a dinner': 40, 'a bacon sandwich': 40 }, buys: [] },
    ironmonger: { place: 'ironmonger', room: 'iron', keeper: 'k_iron', pursePence: 9000, sells: { 'a crowbar': 650, 'a torch': 320, 'a key cut': 90, 'a padlock': 280 }, stock: { 'a crowbar': 2, 'a torch': 4, 'a key cut': 20, 'a padlock': 3 }, buys: [] },
    secondhand: { place: 'ritas', room: 'rita', keeper: 'rita', fence: true, pursePence: 12000, sells: { 'a second-hand coat': 800, 'a dark donkey jacket': 1400, 'a flat cap': 250, 'a scarf': 150 }, stock: { 'a second-hand coat': 2, 'a dark donkey jacket': 1, 'a flat cap': 3, 'a scarf': 4 }, buys: ['goods', 'jewellery', 'tools', 'electrical'] },
    outfitter: { place: 'outfitter', room: null, keeper: null, pursePence: 20000, sells: { 'a decent jacket': 3500, 'a good overcoat': 9500, 'a hat': 600, 'a scarf': 350 }, stock: { 'a decent jacket': 2, 'a good overcoat': 1, 'a hat': 3, 'a scarf': 4 }, buys: [] },
    barber: { place: 'barber', room: null, keeper: null, pursePence: 3000, sells: { 'a haircut': 300 }, stock: { 'a haircut': 30 }, buys: [] },
    solicitor: { place: 'solicitor', room: null, keeper: null, pursePence: 0, sells: { 'a brief on call': 4000 }, stock: { 'a brief on call': 1 }, buys: [] },
    launderette: { place: 'launderette', room: 'laund', keeper: 'k_laund', pursePence: 2000, sells: { 'a service wash': 100 }, stock: { 'a service wash': 30 }, buys: [] },
    doctor: { place: 'doctor', room: null, keeper: 'calvert', sundayOpen: true, alwaysOpen: true, pursePence: 0, sells: { 'stitches, no questions': 1000 }, stock: { 'stitches, no questions': 10 }, buys: [] },
    coin: { place: 'coin', room: 'coin', keeper: 'hal', pursePence: 15000, sells: {}, stock: {}, buys: ['coins', 'jewellery'] },
  },
  doorWithinMetres: 2.6, // a shop with no room on the map is used at its door
  counterWithinMetres: 2.4,
  // what each bought thing is: a coat he can wear, a thing for the pocket, or something used up on the spot
  items: {
    'a second-hand coat': { coat: 'secondhand' },
    'a dark donkey jacket': { coat: 'dark' },
    'a decent jacket': { coat: 'jacket' },
    'a good overcoat': { coat: 'overcoat' },
    'a flat cap': { wear: 'hat' },
    'a hat': { wear: 'hat' },
    'a scarf': { wear: 'scarf' },
    'a crowbar': { pocket: 'crowbar' },
    'a torch': { pocket: 'torch' },
    'a key cut': { pocket: 'cut key', needs: 'a key to copy' },
    'a padlock': { pocket: 'padlock' },
    'twenty Mariners': { pocket: 'cigarettes' },
    'a box of matches': { pocket: 'matches' },
    'the paper': { read: 'paper' },
    'a tea': { sit: true },
    'a dinner': { sit: true, mends: 0.15 },
    'a bacon sandwich': { mends: 0.05 },
    'a haircut': { barber: true },
    'a brief on call': { flag: 'brief' },
    'a service wash': { wash: true },
    'stitches, no questions': { stitches: true },
  },
  barberLastsDays: 7,
  washTakesGameMinutes: 50,
};
export const SCHEDULES = {};
export const PEOPLE = {};
