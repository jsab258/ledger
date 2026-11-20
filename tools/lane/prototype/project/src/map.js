// Meridian: the Hook around Quay Street, and a slice of Copper Row over the bridge.
// Axes: +x east, +z south. Angles: 0 faces +z (south), increasing towards +x (east).
// Britain drives on the left: southbound traffic keeps to the east lane.
import { hyp, inRect, segRect } from './util.js';

export const BOUNDS = { x0: -130, z0: -226, x1: 162, z1: 112 };
const R = (x0, z0, x1, z1, o = {}) =>
  Object.assign(
    { x0: Math.min(x0, x1), z0: Math.min(z0, z1), x1: Math.max(x0, x1), z1: Math.max(z0, z1) },
    o,
  );

// ---------- ground ----------
export const ROADS = [
  // asphalt carriageways
  R(-5, -208, 5, 44, { n: 'qs' }),
  R(-128, 44, 160, 52, { n: 'quay' }),
  R(-78, -22, 27, -15, { n: 'chapel' }),
];
export const SETTS = [
  // cobbles and setts
  R(27, -25, 32, 44, { n: 'backlane' }),
  R(-24, -57, -20, -25, { n: 'alley' }),
  R(-128, 52, 160, 62, { n: 'apron' }),
  R(20, 31, 27, 41, { n: 'yard' }),
  R(-46, -198, -8, -126, { n: 'market' }),
  R(8, -90, 30, -72, { n: 'marketedge' }),
  R(60, 62, 70, 98, { n: 'pier' }),
  R(-120, 18, -80, 41, { n: 'scrap' }),
  R(-16, -208, 16, -198, { n: 'forecourt' }),
  R(-20, -77, -8, -58, { n: 'chapelyard' }),
];
export const PAVE = [
  // raised flagstone pavements (y 0.12)
  R(5, -208, 8, -22),
  R(-8, -208, -5, -22),
  R(5, -15, 8, 41),
  R(-8, -15, -5, 41),
  R(-128, 41, -8, 44),
  R(8, 41, 27, 44),
  R(32, 41, 160, 44),
  R(-78, -25, -8, -22),
  R(8, -25, 27, -22),
  R(-78, -15, -8, -12),
  R(8, -15, 27, -12),
  R(-8, 41, -5, 44),
  R(5, 41, 8, 44),
];
export const WATER = [R(-130, 62, 162, 112, { n: 'river' }), R(-130, -118, 162, -96, { n: 'cut' })];
export const DECKS = [
  R(60, 62, 70, 98),
  R(-58, 62, -52, 78),
  R(-5, -122, 5, -92),
  R(-8, -122, -5, -92),
  R(5, -122, 8, -92),
];
export const ZONES = [
  R(20, 31, 27, 41, { n: "Mickey's yard" }),
  R(27, -25, 32, 44, { n: 'the back lane' }),
  R(-24, -57, -20, -25, { n: 'the west alley' }),
  R(-66, 52, -40, 82, { n: 'the ferry landing' }),
  R(40, 52, 104, 100, { n: 'the fish dock' }),
  R(32, 20, 160, 52, { n: 'the warehouse row' }),
  R(-122, 16, -78, 43, { n: "Iveson's yard" }),
  R(-130, 41, 162, 62, { n: 'the quay' }),
  R(-80, -25, 27, -12, { n: 'Chapel Lane' }),
  R(-10, -122, 10, -92, { n: 'the bridge' }),
  R(-60, -226, 60, -122, { n: 'Copper Row' }),
  R(-10, -92, 32, -70, { n: 'the market end' }),
  R(-8, 10, 8, 41, { n: 'Quay Street, the quay end' }),
  R(-8, -92, 8, 41, { n: 'Quay Street' }),
];
export function zoneAt(x, z) {
  for (const r of ZONES) if (inRect(x, z, r)) return r.n;
  return 'the Hook';
}

// ---------- buildings ----------
// face: which side fronts the street (W,E,N,S). st: storeys. k: look. sign: fascia text.
export const BLD = [];
const B = (id, x0, z0, x1, z1, o = {}) => {
  const b = Object.assign(R(x0, z0, x1, z1), { id, st: 2, face: 'W', k: 'house', brick: 'soot' }, o);
  BLD.push(b);
  return b;
};
// East parade, six bays, Mickey's at the quay end
B('mickeys', 8, 31, 20, 41, {
  k: 'shop',
  sign: "MICKEY'S CARS",
  sub: 'MINICABS · MERIDIAN 51266',
  fb: '#1d2a5c',
  ff: '#f3e9c6',
  font: 'cab',
  enter: 'mickeys',
});
B('fish', 8, 22.6, 20, 31, {
  k: 'shop',
  sign: 'LAVERACK',
  sub: 'WET FISH · CRAB · KIPPERS',
  fb: '#e8e2d0',
  ff: '#1f4a6b',
  font: 'slab',
  enter: 'fish',
});
B('laund', 8, 14.2, 20, 22.6, {
  k: 'shop',
  sign: 'WASHETERIA',
  sub: 'SERVICE WASH · OPEN 8 TILL 8',
  fb: '#2b8f9c',
  ff: '#fff6da',
  font: 'round',
  enter: 'laund',
});
B('grocer', 8, 5.8, 20, 14.2, {
  k: 'shop',
  sign: 'HOOK STORES',
  sub: 'GROCER & PROVISIONS',
  fb: '#5a1f1a',
  ff: '#e9c96a',
  font: 'serif',
  enter: 'grocer',
});
B('empty', 8, -2.6, 20, 5.8, {
  k: 'shop',
  sign: '',
  sub: '',
  fb: '#6f6a5e',
  ff: '#3a352c',
  font: 'serif',
  tolet: 1,
});
B('tangs', 8, -11, 20, -2.6, {
  k: 'shop',
  sign: 'GOLDEN RIVER',
  sub: 'CHINESE MEALS TO TAKE AWAY',
  fb: '#a4161a',
  ff: '#f6d55c',
  font: 'slab',
  enter: 'tangs',
  late: 1,
});
// West block: plain terraced houses opposite Mickey's, shops opposite the north half
B('h1', -20, 35, -8, 41, { face: 'E' });
B('ada', -20, 29, -8, 35, { face: 'E', enter: 'ada', door: '#2f5d50' });
B('h3', -20, 23, -8, 29, { face: 'E' });
B('h4', -20, 17, -8, 23, { face: 'E' });
B('h5', -20, 11, -8, 17, { face: 'E' });
B('news', -20, 3.7, -8, 11, {
  face: 'E',
  k: 'shop',
  sign: 'R. PEART',
  sub: 'NEWSAGENT & TOBACCONIST',
  fb: '#123c2c',
  ff: '#e7d9a8',
  font: 'serif',
  enter: 'news',
});
B('iron', -20, -3.7, -8, 3.7, {
  face: 'E',
  k: 'shop',
  sign: 'HOOK IRONMONGERY',
  sub: 'TOOLS · PARAFFIN · KEYS CUT',
  fb: '#27262b',
  ff: '#d9d2c0',
  font: 'slab',
  enter: 'iron',
});
B('tearoom', -20, -11, -8, -3.7, {
  face: 'E',
  k: 'shop',
  sign: 'The Copper Kettle',
  sub: 'TEAS · LIGHT LUNCHES',
  fb: '#7b3f2a',
  ff: '#f2e3c4',
  font: 'script',
  enter: 'tearoom',
});
// North of Chapel Lane, east side
B('rita', 8, -33, 20, -25, {
  k: 'shop',
  sign: "RITA'S",
  sub: 'PAWNBROKER · LOANS · UNREDEEMED PLEDGES',
  fb: '#161616',
  ff: '#d8b24a',
  font: 'serif',
  enter: 'rita',
  late: 1,
});
B('chandler', 8, -41, 20, -33, {
  k: 'shop',
  sign: 'CHANDLERY',
  sub: 'ROPE · PAINT · OILSKINS',
  fb: '#1e3f66',
  ff: '#efe6cf',
  font: 'slab',
  enter: 'chandler',
});
B('boarding', 8, -52, 20, -41, {
  st: 3,
  k: 'hotel',
  sign: 'REGENT HOUSE',
  sub: 'BED & BOARD · VACANCIES',
  enter: 'boarding',
  brick: 'red',
});
B('laundry', 8, -72, 24, -52, { st: 3, k: 'works', sign: 'MERIDIAN STEAM LAUNDRY', brick: 'red', shut: 1 });
// North of Chapel Lane, west side
B('caff', -20, -33, -8, -25, {
  face: 'E',
  k: 'shop',
  sign: "Rinaldi's",
  sub: 'CAFE · BREAKFASTS · TEAS',
  fb: '#e6dcc3',
  ff: '#9a1c1c',
  font: 'script',
  enter: 'caff',
});
B('coin', -20, -39, -8, -33, {
  face: 'E',
  k: 'shop',
  sign: 'H. METCALFE',
  sub: 'COINS & MEDALS',
  fb: '#3b3a36',
  ff: '#b9ae8e',
  font: 'serif',
  enter: 'coin',
});
B('h6', -20, -45, -8, -39, { face: 'E' });
B('h7', -20, -51, -8, -45, { face: 'E' });
B('h8', -20, -57, -8, -51, { face: 'E' });
B('chapel', -34, -77, -20, -58, { face: 'E', k: 'chapel', st: 2, brick: 'red', enter: 'chapel' });
B('ship', -20, -90, -8, -79, { face: 'E', k: 'pub', sign: 'THE SHIP', brick: 'soot', shut: 1 });
// The quay front, north side, west of Quay Street
B('harbour', -36, 31, -22, 41, {
  face: 'S',
  k: 'office',
  sign: 'HARBOUR OFFICE',
  sub: 'CUSTOM HOUSE',
  brick: 'red',
  enter: 'harbour',
});
B('smoke', -58, 31, -40, 41, { face: 'S', k: 'works', sign: 'SMOKE HOUSE', shut: 1 });
B('netstore', -76, 31, -60, 41, { face: 'S', k: 'works', sign: 'NET STORE', shut: 1 });
B('scrapcabin', -93, 21, -85, 27, { face: 'S', k: 'cabin', st: 1 });
// The warehouse row
B('wh1', 36, 22, 58, 41, { face: 'S', k: 'ware', st: 3, sign: 'No 1', brick: 'red' });
B('wh2', 60, 22, 82, 41, { face: 'S', k: 'ware', st: 3, sign: 'No 2' });
B('wh3', 84, 22, 106, 41, { face: 'S', k: 'ware', st: 3, sign: 'No 3', brick: 'red' });
B('wh4', 108, 22, 130, 41, { face: 'S', k: 'ware', st: 3, sign: 'No 4', burnt: 1 });
B('wh5', 132, 22, 154, 41, { face: 'S', k: 'ware', st: 3, sign: 'No 5' });
B('fishshed', 78, 55.6, 100, 61.6, { face: 'N', k: 'shed', st: 1, sign: 'JENSEN & SON · FISH MERCHANTS' });
B('ferryhut', -67, 55.6, -59, 60.6, { face: 'N', k: 'cabin', st: 1, sign: 'MERIDIAN FERRY · BOOKINGS' });
// Chapel Lane
B('cl1', -75, -12, -62, -3, { face: 'N' });
B('cl2', -62, -12, -49, -3, { face: 'N' });
B('cl3', -49, -12, -36, -3, { face: 'N' });
B('cl4', -36, -12, -24, -3, { face: 'N' });
B('cn1', -75, -34, -62, -25, { face: 'S' });
B('cn2', -62, -34, -49, -25, { face: 'S' });
B('cn3', -49, -34, -36, -25, { face: 'S' });
B('cn4', -36, -34, -24, -25, { face: 'S' });
B('school', -108, -38, -82, -4, {
  face: 'E',
  k: 'school',
  st: 2,
  brick: 'red',
  sign: 'MERIDIAN BOARD SCHOOL 1894',
  shut: 1,
});
B('garages', 32, -12, 40, 20, { face: 'W', k: 'garages', st: 1 });
B('yards', 20, -11, 27, 31, { k: 'yards', st: 1 });
B('ritayard', 20, -33, 27, -25, { k: 'yards', st: 1 });
B('backeast', 32, 20, 36, 41, { k: 'yards', st: 1 });
// Copper Row over the bridge
B('bank', 8, -150, 22, -128, { st: 3, k: 'bank', sign: 'HUMBER & DISTRICT BANK', brick: 'stone' });
B('video', 8, -164, 22, -150, {
  k: 'shop',
  sign: 'DC VIDEO & SOUND',
  sub: 'FILMS TO RENT · CAR STEREO',
  fb: '#111',
  ff: '#ff4fa3',
  font: 'round',
  late: 1,
});
B('cr3', 8, -178, 22, -164, {
  k: 'shop',
  sign: 'COPPER ROW BAKERY',
  sub: 'BREAD · PIES · FANCIES',
  fb: '#e9e2cc',
  ff: '#6a3b1c',
  font: 'serif',
});
B('cr4', 8, -196, 22, -178, {
  st: 3,
  k: 'shop',
  sign: 'DRAPERS',
  sub: 'WOOLS · HABERDASHERY',
  fb: '#2d2a4a',
  ff: '#e7dfc8',
  font: 'serif',
});
B('hall', -46, -214, -10, -198, { face: 'S', st: 2, k: 'hall', sign: 'MARKET HALL', brick: 'red' });
B('station', 10, -224, 44, -208, { face: 'S', st: 2, k: 'hall', sign: 'MERIDIAN TOWN', brick: 'stone' });
B('cw1', -60, -150, -46, -126, {
  face: 'E',
  st: 3,
  k: 'works',
  sign: 'CORN EXCHANGE',
  brick: 'stone',
  shut: 1,
});
B('cw2', -60, -198, -46, -150, { face: 'E', st: 2, k: 'house' });

// Walls and fences (block movement and sight). Gaps are the yard's two exits.
export const WALLS = [
  R(26.6, 31, 27, 34.4),
  R(26.6, 37.6, 27, 41),
  R(20, 40.6, 21.9, 41),
  R(23.7, 40.6, 27, 41),
  R(20, 31, 27, 31.4), // Mickey's yard
  R(-120, 40.6, -104, 41),
  R(-96, 40.6, -80, 41),
  R(-120.4, 18, -120, 41),
  R(-120, 18, -80, 18.4),
  R(-80.4, 18, -80, 41), // Iveson's yard
  R(-108, -4, -82, -3.6),
  R(-82, -38, -81.6, -4), // school wall
  R(-24.4, -57, -24, -34),
  R(-24, -57.4, -20, -57),
  R(-50, 58.9, -44, 59.3), // west alley end
];
export const PROPS = []; // small solid things: {x,z,r}
const P = (t, x, z, o = {}) => {
  const p = Object.assign({ t, x, z, r: 0.45 }, o);
  PROPS.push(p);
  return p;
};
P('phonebox', 7.3, -13.2, { r: 0.6 });
P('pillarbox', -6.5, 3.2, { r: 0.35 });
P('busshelter', -6.9, 20, { r: 0.2, w: 3.6 });
P('ranksign', 5.7, 41.2, { r: 0.12 });
P('belisha', 5.5, 13, { r: 0.12 });
P('belisha', -5.5, 13, { r: 0.12 });
P('bin', 7.5, 14.4, { r: 0.3 });
P('bin', -7.4, -26.4, { r: 0.3 });
P('skip', 30.7, 12, { r: 1.1, hand: 'brick' });
P('dustbin', 27.8, 30.2, { r: 0.35, hand: 'dustbin lid' });
P('dustbin', 27.8, -6, { r: 0.35, hand: 'dustbin lid' });
P('dustbin', -23.2, -40, { r: 0.35, hand: 'dustbin lid' });
P('boxes', 50, 57.5, { r: 1.2, hand: 'cargo hook' });
P('boxes', 55, 58.5, { r: 1.2 });
P('boxes', 73, 56, { r: 1.2 });
P('nets', 44, 57, { r: 1.4 });
P('nets', 40, 59.5, { r: 1.2 });
P('boxes', 64, 70, { r: 1.0 });
P('nets', 66, 84, { r: 1.1 });
P('bollard', 20, 61, { r: 0.3 });
P('bollard', 0, 61, { r: 0.3 });
P('bollard', -30, 61, { r: 0.3 });
P('bollard', 110, 61, { r: 0.3 });
P('bollard', 140, 61, { r: 0.3 });
P('crane', -18, 59.2, { r: 2 });
P('crane', 112, 59.2, { r: 2 });
P('crane', 142, 59.2, { r: 2 });
P('hut', 37.6, 57.4, { r: 1.3 });
P('brazier', 40.6, 56.8, { r: 0.4 });
P('shelter', -47, 58.2, { r: 0 });
P('scrap', -112, 26, { r: 3.2, hand: 'wheel brace' });
P('scrap', -103, 34, { r: 2.6 });
P('scrap', -88, 34, { r: 2.2, hand: 'brick' });
P('scrapcar', -110, 36, { r: 1.6 });
P('stall', -38, -140, { r: 1.5 });
P('stall', -30, -140, { r: 1.5 });
P('stall', -22, -140, { r: 1.5 });
P('stall', -38, -152, { r: 1.5 });
P('stall', -30, -152, { r: 1.5 });
P('stall', -22, -152, { r: 1.5 });
P('stall', -38, -166, { r: 1.5 });
P('stall', -26, -166, { r: 1.5 });
P('stall', 13, -80, { r: 1.5 });
P('stall', 21, -80, { r: 1.5 });
P('clock', -14, -176, { r: 0.6 });
P('ladder', 7.4, 2.4, { r: 0.3 });
P('bench', -7.45, -62, { r: 0.4, w: 2 });
P('cross', -14, -67, { r: 0.4 });
P('bin', 6.8, -160, { r: 0.3 });
P('busstop', 6.2, -140, { r: 0.1 });
P('cctv', 8.2, -139, { r: 0 });
P('chair', -6.9, -31, { r: 0.3, hand: 'chair' });

// Sodium street lamps. r: pool radius. k: 1 column lamp, 2 wall bracket, 3 small white light.
export const LAMPS = [];
const L = (x, z, r = 13, k = 1, o = {}) => LAMPS.push(Object.assign({ x, z, r, k }, o));
[
  [5.7, 38],
  [-5.7, 22],
  [5.7, 6],
  [-5.7, -9],
  [5.7, -30],
  [-5.7, -48],
  [5.7, -66],
  [-5.7, -85],
].forEach(([x, z]) => L(x, z));
[-102, -66, -28, 16, 52, 88, 124, 152].forEach((x) => L(x, 43.2));
L(-40, -13.6);
L(-68, -13.6);
L(14, -13.6, 11);
L(29.5, 4, 6.5, 2, { dim: 1 });
L(5.7, -100, 12);
L(-5.7, -114, 12);
[
  [5.7, -134],
  [-5.7, -150],
  [5.7, -168],
  [-5.7, -186],
  [-28, -146, 12],
  [-28, -172, 12],
  [0, -203, 12],
].forEach(([x, z, r]) => L(x, z, r || 13));
L(-48, 58.2, 10, 1, { ferry: 1 });
L(66, 60, 9, 1);
L(-100, 30, 7, 2, { dim: 1 });
// Other light at night: lit windows, the phone box, a brazier. until: hour it goes dark (wraps past midnight).
export const GLOWS = [
  { x: 6.6, z: -29, r: 7, col: 'w', until: 24.6, id: 'rita' },
  { x: 6.6, z: -6.8, r: 8, col: 'w', until: 23.5, id: 'tangs' },
  { x: 7.3, z: -13.2, r: 3, col: 'w', until: 30 },
  { x: 6.8, z: -46.5, r: 4.5, col: 'o', until: 30 },
  { x: -28.5, z: 42.6, r: 5, col: 'w', until: 30 },
  { x: 40.6, z: 56.8, r: 5.5, col: 'f', until: 30, id: 'brazier' },
  { x: 6.6, z: 36, r: 5.5, col: 'w', until: 30, id: 'mickeys' },
  { x: 6.8, z: -157, r: 7, col: 'p', until: 23.8 },
  { x: -6.6, z: 7.3, r: 4, col: 'w', until: 19 },
  { x: 6.6, z: 18.4, r: 5, col: 'w', until: 20 },
];
// Places where lamp light does not reach: doorways, the alley mouth, under the fish shed.
export const SHADE = [
  R(7.2, -0.5, 8.2, 3.5),
  R(7.2, 14.6, 8.2, 16),
  R(-8.2, 16, -7.2, 18),
  R(-8.2, -53, -7.2, -50),
  R(7.2, -70, 8.2, -55),
  R(26, 41, 33, 44),
  R(-24.5, -27, -19.5, -24),
  R(78, 55.6, 100, 61.6),
  R(-8.2, -88, -7.2, -80),
  R(19.5, 41, 24, 43),
  R(-78, 41, -60, 42.2),
  R(33, 41, 36, 44),
];

// ---------- interiors ----------
// Each is a small set off the map with its back wall to the north; the camera looks in from the south.
// spots: [x, z, ang] in room coordinates. mat: where you stand to leave. street: where the door lets out, and the way you face.
export const ROOMS = {
  mickeys: {
    name: "Mickey's Cars",
    w: 13.6,
    d: 8,
    k: 'office',
    wall: '#b9b294',
    floor: 'lino',
    street: [7.2, 36, -1.57],
    mat: [-4.2, 3.5],
    exit2: { mat: [6.3, 1.6], street: [20.9, 36, 1.57], label: 'the yard' },
    spots: {
      pauline: [-3.6, -3.1, 0],
      sheila: [4.1, -2.9, 0],
      chair: [4.1, -1.0, 3.14],
      bench1: [-6.1, -0.9, 1.57],
      bench2: [-6.1, 0.4, 1.57],
      june: [-1.4, 1.2, -0.8],
      kevin: [-1.6, 2.4, 2.4],
      door: [5.4, -3.1, 3.14],
      hook: [1.5, -3.2, 3.14],
      photo: [-1.2, -3.1, 3.14],
      cot: [5.9, -0.6, -1.57],
      ron: [-5, 2.6, 1.2],
    },
  },
  caff: {
    name: "Rinaldi's",
    w: 10.4,
    d: 7.2,
    k: 'caff',
    wall: '#d9cfae',
    floor: 'check',
    street: [-7.2, -29, 1.57],
    mat: [-4, 3.1],
    spots: {
      grace: [2.2, -3.0, 0],
      s1: [-3.7, -1.6, 1.57],
      s2: [-2.3, -1.6, -1.57],
      s3: [-3.7, 0.9, 1.57],
      s4: [-2.3, 0.9, -1.57],
      s5: [-0.3, 1.2, 1.57],
      s6: [1.1, 1.2, -1.57],
      s7: [2.9, 1.2, 1.57],
      s8: [4.3, 1.2, -1.57],
      till: [1.0, -1.3, 3.14],
      kitchen: [4.3, -2.9, 0.4],
    },
  },
  fish: {
    name: "Laverack's",
    w: 8,
    d: 6,
    k: 'fish',
    wall: '#e4eef0',
    floor: 'tile',
    street: [7.2, 26.8, -1.57],
    mat: [0, 2.6],
    spots: { brenda: [-0.4, -2.2, 0], q1: [-0.6, 0.0, 3.14], q2: [0.8, 0.7, 3.14], q3: [-2.0, 0.9, 3.14] },
  },
  laund: {
    name: 'the Washeteria',
    w: 8,
    d: 6,
    k: 'laund',
    wall: '#cfe3e1',
    floor: 'lino',
    street: [7.2, 18.4, -1.57],
    mat: [0, 2.6],
    spots: { b1: [-2.6, 0.6, 3.14], b2: [-1.4, 0.6, 3.14], k: [2.6, -1.6, 0] },
  },
  grocer: {
    name: 'Hook Stores',
    w: 8,
    d: 6,
    k: 'grocer',
    wall: '#d8cfb4',
    floor: 'boards',
    street: [7.2, 10, -1.57],
    mat: [0, 2.6],
    spots: { k: [2.2, -2.1, 0], q1: [1.6, 0.0, 3.14] },
  },
  tangs: {
    name: 'the Golden River',
    w: 8,
    d: 6,
    k: 'takeaway',
    wall: '#e9d9b0',
    floor: 'lino',
    street: [7.2, -6.8, -1.57],
    mat: [0, 2.6],
    spots: { peter: [-1.0, -2.2, 0], lily: [1.6, -2.2, 0], q1: [-0.8, 0.0, 3.14], q2: [1.2, 0.8, 3.14] },
  },
  news: {
    name: "Peart's",
    w: 7,
    d: 6,
    k: 'news',
    wall: '#c9c2a3',
    floor: 'boards',
    street: [-7.2, 7.3, 1.57],
    mat: [0, 2.6],
    spots: { k: [1.6, -2.1, 0], q1: [1.2, 0.0, 3.14] },
  },
  iron: {
    name: "the ironmonger's",
    w: 7,
    d: 6,
    k: 'iron',
    wall: '#b8b3a3',
    floor: 'boards',
    street: [-7.2, 0, 1.57],
    mat: [0, 2.6],
    spots: { k: [-1.6, -2.1, 0] },
  },
  tearoom: {
    name: 'the Copper Kettle',
    w: 8,
    d: 6,
    k: 'tearoom',
    wall: '#e7d6c4',
    floor: 'carpet',
    street: [-7.2, -7.3, 1.57],
    mat: [0, 2.6],
    spots: {
      k: [2.6, -2.2, 0],
      s1: [-2.6, -0.6, 1.57],
      s2: [-1.2, -0.6, -1.57],
      s3: [0.6, 0.9, 1.57],
      s4: [2.0, 0.9, -1.57],
    },
  },
  rita: {
    name: "Rita's",
    w: 8,
    d: 6,
    k: 'pawn',
    wall: '#8f8a78',
    floor: 'boards',
    street: [7.2, -29, -1.57],
    mat: [0, 2.6],
    spots: { rita: [-0.6, -2.2, 0], wayne: [3.0, -2.0, -0.6], q1: [-0.6, 0.0, 3.14] },
  },
  chandler: {
    name: 'the chandlery',
    w: 8,
    d: 6,
    k: 'chandler',
    wall: '#aeb6ba',
    floor: 'boards',
    street: [7.2, -37, -1.57],
    mat: [0, 2.6],
    spots: { k: [2.2, -2.1, 0] },
  },
  boarding: {
    name: 'Regent House',
    w: 11,
    d: 7,
    k: 'boarding',
    wall: '#b9a58c',
    floor: 'carpet',
    street: [7.2, -46.5, -1.57],
    mat: [-3.6, 3.0],
    spots: {
      sylvia: [-3.4, -2.4, 0],
      bed: [3.6, -2.0, 1.57],
      chair: [-0.6, 0.4, 2.2],
      june: [-1.6, -0.6, 1.0],
      bag: [2.2, -2.8, 0],
    },
  },
  coin: {
    name: "Metcalfe's",
    w: 6.4,
    d: 5.2,
    k: 'coin',
    wall: '#7f7a6c',
    floor: 'boards',
    street: [-7.2, -36, 1.57],
    mat: [0, 2.2],
    spots: { hal: [0.2, -1.8, 0] },
  },
  chapel: {
    name: 'the chapel',
    w: 10,
    d: 13,
    k: 'chapel',
    wall: '#d6cdb8',
    floor: 'tile',
    street: [-18.6, -67, 1.57],
    mat: [0, 6.0],
    spots: {
      walsh: [0, -4.6, 0],
      nora: [-2.6, 2.4, 3.14],
      p1: [-2.6, 0.2, 3.14],
      p2: [2.6, 0.2, 3.14],
      p3: [2.6, 2.4, 3.14],
      p4: [-2.6, -1.8, 3.14],
      p5: [2.6, -1.8, 3.14],
      tom: [1.4, 4.2, 3.14],
    },
  },
  harbour: {
    name: 'the Harbour Office',
    w: 9,
    d: 6,
    k: 'harbour',
    wall: '#bfc3b4',
    floor: 'lino',
    street: [-28.5, 41.9, 0],
    mat: [0, 2.6],
    spots: { susan: [1.8, -2.1, 0], q1: [1.4, 0.0, 3.14] },
  },
  ada: {
    name: "Ada's front room",
    w: 7,
    d: 6,
    k: 'parlour',
    wall: '#a9b59c',
    floor: 'carpet',
    street: [-7.2, 32, 1.57],
    mat: [0, 2.6],
    locked: 1,
    spots: { ada: [-1.4, -1.0, 1.2], tom: [0.9, -0.8, -1.2] },
  },
  // the one-shot: the flat over Mickey's, up the stair from the office (it has no street door of its own)
  flat: {
    name: "the flat over Mickey's",
    w: 11,
    d: 7,
    k: 'boarding',
    wall: '#b3a892',
    floor: 'carpet',
    street: [7.2, 36, -1.57],
    mat: [-3.6, 3.0],
    locked: 1,
    upFrom: 'mickeys',
    stair: [5.2, 3.5], // where the stair stands in the office, in the office's own metres
    spots: { sylvia: [-3.4, -2.4, 0], june: [-1.6, -0.6, 1.0], bed: [3.6, -2.0, 1.57], chair: [-0.6, 0.4, 2.2], bag: [2.2, -2.8, 0] },
  },
};
let ri = 0;
for (const id in ROOMS) {
  const r = ROOMS[id];
  r.id = id;
  r.ox = 1000 + 60 * ri++;
  r.oz = 1000;
}
// Things inside rooms that Tom can use: the room, the spot in the room's own metres, and how near he must be.
// The game's prompts and the test hook both read this table.
export const INSIDE = {
  coatHook: { name: "the coat hook at Mickey's", room: 'mickeys', x: 1.1, z: -3.2, within: 1.3 },
  photograph: { name: "the photograph at Mickey's", room: 'mickeys', x: -1.2, z: -3.1, within: 1.2 },
  backDoor: { name: "the door in Mickey's back room", room: 'mickeys', x: 5.4, z: -3.0, within: 1.2 },
  cot: { name: "the cot at Mickey's", room: 'mickeys', x: 5.6, z: -2.0, within: 1.4 },
  bed: { name: 'the bed at Regent House', room: 'boarding', x: 3.6, z: -2.0, within: 1.6 },
  flatBed: { name: "the bed in the flat over Mickey's", room: 'flat', x: 3.6, z: -2.0, within: 1.6 },
  stair: { name: "the stair to the flat at Mickey's", room: 'mickeys', x: 5.2, z: 3.5, within: 1.0 },
  caffCounter: { name: "the counter at Rinaldi's", room: 'caff', x: 1.0, z: -1.2, within: 1.5 },
  paperCounter: { name: "the counter at Peart's", room: 'news', x: 1.2, z: 0, within: 2 },
  chipCounter: { name: 'the counter at the Golden River', room: 'tangs', x: 0, z: -0.4, within: 2 },
  chapelPew: { name: 'the back pew in the chapel', room: 'chapel', x: 1.4, z: 4.2, within: 1.6 },
};
export const roomPos = (id, lx, lz) => {
  const r = ROOMS[id];
  return [r.ox + lx, r.oz + lz];
};
export function roomAt(x) {
  if (x < 900) return null;
  const i = Math.round((x - 1000) / 60);
  return Object.values(ROOMS)[i] || null;
}

// ---------- named spots on the street ----------
export const SPOTS = {
  rank: [6.2, 38.5, -1.9],
  rank2: [6.5, 35.6, -1.2],
  door: [7.0, 34.6, -1.57],
  pave: [6.0, 28.5, -2.2],
  adawin: [-8, 32, 1.57],
  adadoor: [-7.2, 30.6, 1.57],
  busstop: [-5.9, 20.6, 1.57],
  infirmary: [-116, 53.2, 3.14], // the pavement outside the Infirmary's door
  junepass: [-6.0, 14.6, 1.57], // where June Suddaby is met on the first afternoon, clear of the bus shelter
  bus2: [-5.9, 19.2, 1.57],
  bus3: [-5.8, 22.6, 1.4],
  phone: [6.0, -11.2, 2.6],
  nets: [45.4, 55.6, 2.4],
  boxes: [51.4, 56.2, 0.6],
  boxes2: [56.6, 57.2, 3.3],
  pier: [65, 72, 0.4],
  ferry: [-55, 60.5, 2.8],
  ferry2: [-42.4, 56.6, -1.75],
  shelter: [-47, 58.2, 3.14],
  pontoon: [-55, 74, 0],
  hut: [39.6, 55.3, 3.14],
  row1: [70, 42.6, 0],
  row2: [118, 42.6, 0],
  row3: [146, 42.6, 0.3],
  fire: [119, 43, 3.14],
  scrap: [-98, 30, 0.6],
  scrapgate: [-100, 42.4, 0],
  scraplad: [-101.5, 27.2, 0.8],
  coinback: [-21, -36, 1.57],
  ritaside: [13, -23.6, 3.14],
  yard: [23.4, 36, 1.2],
  yardgate: [28.4, 36, -1.57],
  ladder: [6.6, 2.4, 1.57],
  market1: [-34, -146, 0.4],
  market2: [-26, -158, 2.0],
  market3: [-30, -134, 3.1],
  marketedge: [16, -77, 3.0],
  station: [3, -203, 3.14],
  bank: [6.4, -139, -1.57],
  video: [6.4, -157, -1.57],
  chapelgate: [-7, -66, 1.57],
  grave: [-13, -70, 2.6],
  bench: [-6.2, -62.6, 1.57],
  corner: [6.4, -24, -2.4],
  corner2: [-6.4, -24, 2.4],
  laundrygate: [6.6, -62, -1.57],
  schoolgate: [-80, -18, -1.57],
  qn: [6.4, -84, 3.14],
  cl: [-44, -23.4, 0],
  clhome: [-42, -13.4, 3.14],
  mam: [-56, -13.4, 3.14],
  smoke1: [-46, 42.4, 0],
  harbourdoor: [-28.5, 42.4, 0],
  zebra: [6.2, 13.6, -1.57],
  quaycorner: [9, 42.6, 0.4],
  cam1: [-14, -176, 0],
  lads1: [4.8, -155, -1.2],
  lads2: [6.6, -153.6, -2.0],
  lads3: [-30, 56, 1],
  lads4: [-28.4, 57, -1.4],
};
// Windows people watch from when they are at home. [x, z, ang, height]
export const WINDOWS = {
  ada: [-8, 32, 1.57, 4.3],
  albert: [-8, 26, 1.57, 4.3],
  julie: [-8, 20, 1.57, 4.3],
  brenda: [8, 26.8, -1.57, 4.4],
  peter: [8, -6.8, -1.57, 4.4],
  lily: [8, -5.4, -1.57, 4.4],
  rita: [8, -29, -1.57, 4.4],
  sylvia: [8, -44, -1.57, 1.7],
  june: [8, -48.5, -1.57, 4.4],
  grace: [-8, -29, 1.57, 4.4],
  hal: [-8, -36, 1.57, 4.4],
  ron: [-42, -12, 3.14, 4.3],
  darren: [-56, -12, 3.14, 4.3],
};
export const EXITS = { N: [2.2, -214], W: [-126, 47], E: [158, 47] };

// ---------- collision, sight lines, heights ----------
const solid = BLD.concat(WALLS);
const water = (x, z) => {
  for (const w of WATER)
    if (inRect(x, z, w)) {
      for (const d of DECKS) if (inRect(x, z, d)) return false;
      return true;
    }
  return false;
};
export function blocked(x, z, rad = 0.35) {
  if (x > 900) {
    const rm = roomAt(x);
    if (!rm) return true;
    return roomBlocked(rm, x - rm.ox, z - rm.oz, rad);
  }
  if (x < BOUNDS.x0 + 1 || x > BOUNDS.x1 - 1 || z < BOUNDS.z0 + 1 || z > BOUNDS.z1 - 1) return true;
  for (const b of solid)
    if (x > b.x0 - rad && x < b.x1 + rad && z > b.z0 - rad && z < b.z1 + rad) return true;
  for (const p of PROPS) {
    if (!p.r) continue;
    if (p.w) {
      if (Math.abs(x - p.x) < p.r + rad && Math.abs(z - p.z) < p.w / 2 + rad) return true;
    } else if (hyp(x, z, p.x, p.z) < p.r + rad) return true;
  }
  return water(x, z);
}
// Round 6 (the gate): the lamp columns that stand on the ground (wall brackets hang clear). They are solid for the
// cab and for Tom on foot only (drive.js): the town's own walks and the fight's knock-backs are left as they were.
export const POSTS = LAMPS.filter((l) => l.k === 1);
// What a crash is told as: the plain name of whatever blocked() meets at this spot (null when nothing does).
const PROP_WORDS = {
  phonebox: 'the phone box',
  pillarbox: 'the pillar box',
  busshelter: 'the bus shelter',
  ranksign: 'the rank sign',
  belisha: 'a crossing beacon',
  bin: 'a litter bin',
  skip: 'a skip',
  dustbin: 'a dustbin',
  boxes: 'a stack of fish boxes',
  nets: 'a heap of nets',
  bollard: 'a bollard',
  crane: 'a crane leg',
  hut: 'the hut',
  brazier: 'the brazier',
  scrap: 'a heap of scrap',
  scrapcar: 'a scrap car',
  stall: 'a market stall',
  clock: 'the clock',
  ladder: 'a ladder',
  bench: 'a bench',
  cross: 'the cross',
  busstop: 'the bus stop',
  chair: 'a chair',
};
export function whatBlocks(x, z, rad = 0.35) {
  if (x > 900) return 'a wall';
  if (x < BOUNDS.x0 + 1 || x > BOUNDS.x1 - 1 || z < BOUNDS.z0 + 1 || z > BOUNDS.z1 - 1)
    return 'the end of the road';
  for (const p of PROPS) {
    if (!p.r) continue;
    if (p.w ? Math.abs(x - p.x) < p.r + rad && Math.abs(z - p.z) < p.w / 2 + rad : hyp(x, z, p.x, p.z) < p.r + rad)
      return PROP_WORDS[p.t] || 'something';
  }
  for (const b of solid)
    if (x > b.x0 - rad && x < b.x1 + rad && z > b.z0 - rad && z < b.z1 + rad) return 'a wall';
  return water(x, z) ? 'the quay edge' : null;
}
// The big things on the street that can hide a man or the cab from the camera: scrap heaps, crane legs, stalls,
// the hut (every prop at least 1.3 m across; the camera treats them as 3 m high).
const BIG = PROPS.filter((p) => p.r >= 1.3);
export function bigThingAt(x, z) {
  for (const p of BIG) if (hyp(x, z, p.x, p.z) < p.r) return true;
  return false;
}
// The one-shot (the machine checks' fault at the ferry landing and on Quay Street): the thin and the roofed things
// that can stand between the camera and Tom: a lamp post, the ferry shelter, the bus shelter. The camera comes in
// front of them as it does for a big thing. Heights in metres, as the town draws them (render/town.js).
const CAM_POST_WITHIN = 0.32,
  CAM_POST_HIGH = 6.5,
  CAM_SHELTER_HIGH = 2.5;
const SHELTERS = PROPS.filter((p) => p.t === 'shelter' || p.t === 'busshelter').map((p) =>
  p.t === 'shelter' ? { x0: p.x - 3.2, x1: p.x + 3.2, z0: p.z - 1.45, z1: p.z + 0.95 } : { x0: p.x - 0.2, x1: p.x + 1.4, z0: p.z - (p.w || 3.6) / 2 - 0.1, z1: p.z + (p.w || 3.6) / 2 + 0.1 },
);
export function thinThingAt(x, z, y) {
  if (y < CAM_POST_HIGH) for (const l of POSTS) if (Math.abs(x - l.x) < CAM_POST_WITHIN && Math.abs(z - l.z) < CAM_POST_WITHIN && hyp(x, z, l.x, l.z) < CAM_POST_WITHIN) return true;
  if (y < CAM_SHELTER_HIGH) for (const r of SHELTERS) if (x > r.x0 && x < r.x1 && z > r.z0 && z < r.z1) return true;
  return false;
}
// Tall walls inside rooms that can hide a man from the camera: room id -> rects in room coordinates, filled by
// the interior builder beside FURN (the low furniture is in FURN only).
export const TALL = {};
// The walls of a room that can come between Tom and the camera, in room coordinates, each grown by `grow`: the
// two side walls and any partition. The back wall is behind him and the fourth wall is away.
const camWalls = {};
export function cameraWalls(r, grow) {
  const key = r.id + ':' + grow;
  if (!camWalls[key]) {
    const hw = r.w / 2,
      hd = r.d / 2;
    camWalls[key] = [
      { x0: -hw - 0.15, x1: -hw, z0: -hd - 0.15, z1: hd + 0.85 },
      { x0: hw, x1: hw + 0.15, z0: -hd - 0.15, z1: hd + 0.85 },
    ]
      .concat(TALL[r.id] || [])
      .map((w) => ({ x0: w.x0 - grow, x1: w.x1 + grow, z0: w.z0 - grow, z1: w.z1 + grow }));
  }
  return camWalls[key];
}
// does the straight line between two spots in a room cross one of those walls?
export function roomSightBlocked(r, ax, az, bx, bz, grow) {
  for (const w of cameraWalls(r, grow)) if (segRect(ax - r.ox, az - r.oz, bx - r.ox, bz - r.oz, w)) return true;
  return false;
}
export const FURN = {}; // room id -> solid rects in room coordinates, filled by the interior builder
function roomBlocked(rm, lx, lz, rad) {
  if (lx < -rm.w / 2 + rad || lx > rm.w / 2 - rad || lz < -rm.d / 2 + rad || lz > rm.d / 2 + 0.2) return true;
  for (const f of FURN[rm.id] || [])
    if (lx > f.x0 - rad && lx < f.x1 + rad && lz > f.z0 - rad && lz < f.z1 + rad) return true;
  return false;
}
export function los(ax, az, bx, bz) {
  if (ax > 900 || bx > 900) return true;
  const x0 = Math.min(ax, bx),
    x1 = Math.max(ax, bx),
    z0 = Math.min(az, bz),
    z1 = Math.max(az, bz);
  for (const b of solid) {
    if (b.x1 < x0 || b.x0 > x1 || b.z1 < z0 || b.z0 > z1) continue;
    if (b.st === 1 && b.k === 'yards') {
      /* low walls still hide a man */
    }
    if (segRect(ax, az, bx, bz, b)) return false;
  }
  return true;
}
export function groundY(x, z) {
  if (x > 900) return 0;
  for (const p of PAVE) if (inRect(x, z, p)) return 0.12;
  return 0;
}
// Push a point out of solid things (used when placing people and cars).
export function freeSpot(x, z) {
  if (!blocked(x, z, 0.4)) return [x, z];
  for (let r = 0.6; r < 6; r += 0.6)
    for (let a = 0; a < 6.28; a += 0.7) {
      const nx = x + Math.sin(a) * r,
        nz = z + Math.cos(a) * r;
      if (!blocked(nx, nz, 0.4)) return [nx, nz];
    }
  return [x, z];
}

// ---------- walking graph ----------
export const NODES = [];
const EDG = [];
const node = (x, z) => {
  NODES.push({ x, z, e: [] });
  return NODES.length - 1;
};
const link = (a, b) => {
  if (a === b || NODES[a].e.includes(b)) return;
  NODES[a].e.push(b);
  NODES[b].e.push(a);
  EDG.push([a, b]);
};
function line(x0, z0, x1, z1, step = 8) {
  const n = Math.max(1, Math.round(hyp(x0, z0, x1, z1) / step));
  const ids = [];
  for (let i = 0; i <= n; i++) {
    ids.push(node(x0 + ((x1 - x0) * i) / n, z0 + ((z1 - z0) * i) / n));
    if (i) link(ids[i - 1], ids[i]);
  }
  return ids;
}
export function nearNode(x, z) {
  let b = 0,
    bd = 1e9;
  for (let i = 0; i < NODES.length; i++) {
    const d = hyp(x, z, NODES[i].x, NODES[i].z);
    if (d < bd) {
      bd = d;
      b = i;
    }
  }
  return b;
}
const join = (ax, az, bx, bz) => link(nearNode(ax, az), nearNode(bx, bz));
line(6.4, 42.6, 6.4, -206, 7);
line(-6.4, 42.6, -6.4, -206, 7); // Quay Street and Copper Row pavements
line(-124, 42.6, -9, 42.6, 9);
line(9, 42.6, 156, 42.6, 9); // the quay, north pavement
line(-124, 54.2, 156, 54.2, 10); // the apron
line(-76, -23.4, -9, -23.4, 8);
line(9, -23.4, 29.5, -23.4, 7);
line(-76, -13.4, -9, -13.4, 8);
line(9, -13.4, 26, -13.4, 6);
line(29.5, 42.6, 29.5, -23.4, 7);
line(-22, -25, -22, -55, 6); // back lane, west alley
line(65, 63, 65, 95, 8);
line(-55, 62.5, -55, 76, 6); // pier, pontoon
line(-40, -130, -12, -130, 9);
line(-40, -146, -12, -146, 9);
line(-40, -159, -12, -159, 9);
line(-40, -174, -12, -174, 9);
line(-12, -130, -12, -192, 8);
line(-42, -130, -42, -192, 8);
line(10, -76, 26, -76, 6);
// cross links
[
  [6.4, 42.6, -6.4, 42.6],
  [6.4, 42.6, 9, 42.6],
  [-6.4, 42.6, -9, 42.6],
  [6.4, 28, -6.4, 28],
  [6.4, 13, -6.4, 13],
  [6.4, -6, -6.4, -6],
  [6.4, -13.4, -6.4, -13.4],
  [6.4, -23.4, -6.4, -23.4],
  [6.4, -13.4, 9, -13.4],
  [6.4, -23.4, 9, -23.4],
  [-6.4, -13.4, -9, -13.4],
  [-6.4, -23.4, -9, -23.4],
  [6.4, -37, -6.4, -37],
  [6.4, -62, -6.4, -62],
  [6.4, -86, -6.4, -86],
  [6.4, -128, -6.4, -128],
  [6.4, -160, -6.4, -160],
  [6.4, -200, -6.4, -200],
  [-6.4, -130, -12, -130],
  [-6.4, -146, -12, -146],
  [-6.4, -174, -12, -174],
  [6.4, -76, 10, -76],
  [29.5, 42.6, 29.5, 54.2],
  [29.5, 42.6, 27, 42.6],
  [29.5, 42.6, 36, 42.6],
  [-48, 42.6, -48, 54.2],
  [-55, 54.2, -55, 62.5],
  [6.4, 42.6, 6, 54.2],
  [-6.4, 42.6, -6, 54.2],
  [65, 54.2, 65, 63],
  [46, 42.6, 46, 54.2],
  [90, 42.6, 90, 54.2],
  [120, 42.6, 120, 54.2],
  [-100, 42.6, -100, 54.2],
  [-22, -25, -22, -23.4],
  [-76, -23.4, -76, -13.4],
  [-40, -23.4, -40, -13.4],
  [29.5, -23.4, 26, -13.4],
].forEach((a) => join(...a));
// the yard and its two exits, Iveson's yard, the chapel yard (anchors are looked up before the new nodes exist)
{
  const aLane = nearNode(29.5, 36),
    aQuay = nearNode(22.8, 42.6),
    aScrap = nearNode(-100, 42.6),
    aChap = nearNode(-6.4, -66),
    aFerry = nearNode(-48, 54.2),
    aAlley = nearNode(-22, -25),
    aCl = nearNode(-22, -23.4);
  const y = node(23.4, 36),
    g = node(27.6, 36),
    p = node(22.8, 41.2),
    yd = node(21, 36);
  link(y, g);
  link(g, aLane);
  link(y, p);
  link(p, aQuay);
  link(y, yd);
  const sg = node(-100, 40.8),
    s1 = node(-99, 31),
    s2 = node(-106, 31);
  link(sg, aScrap);
  link(sg, s1);
  link(s1, s2);
  const c1 = node(-9, -67),
    c2 = node(-14, -68),
    c3 = node(-18.6, -67);
  link(c1, aChap);
  link(c1, c2);
  link(c1, c3);
  link(c2, c3);
  const f1 = node(-44, 56.4);
  link(f1, aFerry);
  link(aAlley, nearNode(-26, -23.4));
}
// stitch together nodes that sit on top of one another where lines meet
for (let i = 0; i < NODES.length; i++)
  for (let j = i + 1; j < NODES.length; j++)
    if (hyp(NODES[i].x, NODES[i].z, NODES[j].x, NODES[j].z) < 2.6) link(i, j);
export function spotNode(x, z) {
  return nearNode(x, z);
}
export function path(a, b) {
  // A* over the walking graph
  if (a === b) return [a];
  const open = [a],
    came = {},
    g = { [a]: 0 },
    f = { [a]: 0 },
    T = NODES[b];
  const closed = new Set();
  while (open.length) {
    let bi = 0;
    for (let i = 1; i < open.length; i++) if (f[open[i]] < f[open[bi]]) bi = i;
    const cur = open.splice(bi, 1)[0];
    if (cur === b) {
      const out = [b];
      let c = b;
      while (came[c] !== undefined) {
        c = came[c];
        out.unshift(c);
      }
      return out;
    }
    closed.add(cur);
    for (const nb of NODES[cur].e) {
      if (closed.has(nb)) continue;
      const ng = g[cur] + hyp(NODES[cur].x, NODES[cur].z, NODES[nb].x, NODES[nb].z);
      if (g[nb] === undefined || ng < g[nb]) {
        g[nb] = ng;
        f[nb] = ng + hyp(NODES[nb].x, NODES[nb].z, T.x, T.z);
        came[nb] = cur;
        if (!open.includes(nb)) open.push(nb);
      }
    }
  }
  return [a, b];
}

// ---------- traffic ----------
export const ROUTES = {
  A: [
    [1.9, -214],
    [1.9, 40],
    [3.5, 45],
    [9, 46.2],
    [160, 46.2],
  ],
  B: [
    [1.9, -214],
    [1.9, 42],
    [0.5, 48],
    [-5, 49.8],
    [-128, 49.8],
  ],
  C: [
    [-128, 46.2],
    [160, 46.2],
  ],
  D: [
    [160, 49.8],
    [-128, 49.8],
  ],
  E: [
    [-128, 46.2],
    [-8, 46.2],
    [-3, 44.5],
    [-1.9, 40],
    [-1.9, -214],
  ],
  F: [
    [160, 49.8],
    [4, 49.8],
    [-0.5, 47],
    [-1.9, 41],
    [-1.9, -214],
  ],
};
export const BUS_STOPS = { E: [-1.9, 20], B: [1.9, -138] };
export const DESTS = {
  station: { n: 'the station', p: [3.2, -200] },
  ferry: { n: 'the ferry landing', p: [-48, 46.6] },
  fishdock: { n: 'the fish dock', p: [70, 46.6] },
  row: { n: 'the warehouse row', p: [120, 46.6] },
  market: { n: 'Copper Row market', p: [3.2, -150] },
  infirmary: { n: 'the Infirmary', p: [-118, 49.6] },
  dockroad: { n: 'Dock Road', p: [150, 46.6] },
  chapel: { n: 'the chapel', p: [-3.2, -66] },
  boarding: { n: 'Regent House', p: [3.2, -46] },
  quayst: { n: 'Quay Street', p: [3.2, 6] },
  harbour: { n: 'the Harbour Office', p: [-28, 46.6] },
  school: { n: 'Chapel Lane', p: [-50, -18.5] },
};
