// LEDGER, the whole game: the places jobs with the hands go to (the system "crime"). Authored data, nothing rolled.
// Each break-in site can be entered three ways (DESIGN 4): a key lent, copied or lifted; a back way its owner's
// routine leaves open; or force, which is loud, shows on the door for a day and is a crime. No new interiors: a
// door, and what is inside it within reach of the door.
import { SPOTS } from '../map.js';
import { addPlace } from './core.js';
import { TUNE } from './tune/crime.js';

const G_ = TUNE.goods;

// ---------- places, by address and landmark (A9) ----------
const P = (id, name, xz, address, landmark, label, x = {}) =>
  addPlace(Object.assign({ id, name, x: xz[0], z: xz[1], address, landmark, label }, x));
P('j_office', "the counter at Mickey's", SPOTS.door, '1 Quay Street', 'under the blue sign at the quay end', 'hours', { openFromHour: 6, openUntilHour: 24, owner: 'sheila', room: 'mickeys' });
P('j_rank', "the rank outside Mickey's", SPOTS.rank, 'Quay Street, the quay end', "the kerb outside Mickey's, where Ron stands", 'public');
P('j_carpark', 'where car two stands', SPOTS.rank2, 'Quay Street, the quay end', "the kerb outside Mickey's", 'public');
P('j_landing', 'the shelter on the ferry landing', SPOTS.shelter, 'the Ferry Landing, West Quay', 'the bench in the shelter, under the landing lamp', 'public');
P('j_coinback', "Metcalfe's back door", SPOTS.coinback, 'the alley off Chapel Lane', 'the coin shop, round the back, the door with no number', 'private', { owner: 'hal' });
P('j_ritaside', "Rita's side door", SPOTS.ritaside, 'Chapel Lane', "the side of Rita's, under her lit window", 'private', { owner: 'rita' });
P('j_smoke', 'the smoke house door', SPOTS.smoke1, 'West Quay', 'the SMOKE HOUSE sign, the door facing the water', 'private');
P('j_harbour', "the Harbour Board's side door", SPOTS.harbourdoor, 'West Quay', 'the Harbour Board, under its clock, the door facing the water', 'hours', { openFromHour: 8, openUntilHour: 17 });
P('j_hut', "Iveson's cabin", [-89, 28.4], "Iveson's scrapyard, West Quay", 'the cabin inside the scrapyard gate, at the west end of the quay', 'private', { owner: 'dennis' });
P('j_scrapgate', 'the scrapyard gate', SPOTS.scrapgate, 'West Quay, the west end', 'the gate with the heaps behind it', 'hours', { openFromHour: 7.5, openUntilHour: 21.6, owner: 'dennis' });
P('j_unit', 'unit 2 on the warehouse row', [70, 44.2], '2 Warehouse Row, East Quay', "the first unit past the watchman's hut, the green doors", 'private', { owner: 'norman' });
P('j_watchhut', "the watchman's hut", SPOTS.hut, 'East Quay', 'the hut with the stove pipe, by the net racks', 'public');
P('j_fishdock', 'the fish dock', SPOTS.boxes2, 'East Quay', 'the stacked fish boxes by the pier', 'public');
P('j_caff', "Rinaldi's", [-7.2, -29], 'Quay Street', 'the caff with the steamed-up window, across from Rita\'s', 'hours', { openFromHour: 6.5, openUntilHour: 17.5, room: 'caff' });
P('j_laund', 'the Washeteria', [7.2, 18.4], 'Quay Street', 'the launderette, three doors up from Mickey\'s', 'hours', { openFromHour: 8, openUntilHour: 20, room: 'laund' });
P('j_phone', 'the phone box', SPOTS.phone, 'Quay Street', 'the phone box by the pillar box, halfway up the street', 'public');
P('j_yard', "Mickey's yard", SPOTS.yard, "behind Mickey's, Quay Street", 'through the office and out the back, the yard with two gates', 'private', { owner: 'sheila' });
P('j_quayedge', 'the quay edge', [44, 59.6], 'East Quay', 'the edge by the net racks, past the bollards', 'public');
P('j_chips', 'the Golden River', [7.2, -6.8], 'Quay Street', 'the chip shop with the lit window', 'hours', { openFromHour: 11.5, openUntilHour: 23.5, room: 'tangs' });
P('j_iron', "the ironmonger's", [-7.2, 0], 'Quay Street', 'the ironmonger, keys cut while you wait', 'hours', { openFromHour: 8.5, openUntilHour: 17.5, room: 'iron' });

// ---------- break-in sites ----------
// containers: kind is one of the search table's; holds: what is found (the thing sought, sometimes something nobody
// asked for), each once. goods: lifted things with an honest price; paper: a line for the Ledger.
export const SITES = {
  hut: {
    id: 'hut',
    name: "Iveson's cabin",
    place: 'j_hut',
    door: [-89, 28.4],
    owner: 'dennis',
    ownerAt: 'scrap', // his routine's name for being here: the hours come from his week (ER-CASE-01)
    street: 'the quay',
    key: { holder: 'dennis', thing: 'the cabin key' },
    backWay: { fromHour: 11, untilHour: 15.1, words: 'the side window, left on the latch while he is at his dinner' },
    containers: [
      { id: 'desk', kind: 'desk', name: 'the desk', holds: { thing: 'the cash box', goods: { honestPence: G_.cashboxPence, cash: true } } },
      {
        id: 'drawer',
        kind: 'drawer',
        name: 'the drawer under the kettle',
        holds: {
          thing: 'a receipt in a brown envelope',
          paper: "A receipt in Iveson's cabin: scrap lead and copper pipe bought for cash, five weeks back, 'from No. 4, as seen'. No name on it.",
        },
      },
    ],
    dog: { x: -99, z: 40.4, name: "Iveson's yard dog" },
    watchFrom: 'across the road from the scrapyard gate',
    window: { thing: "the cabin's window", at: [-90.6, 28.4] },
  },
  pawn: {
    id: 'pawn',
    name: "Rita's back room",
    place: 'j_ritaside',
    door: [13, -23.6],
    owner: 'rita',
    ownerAt: 'rita:rita',
    street: 'Quay Street',
    key: { holder: 'wayne', thing: 'the side door key' },
    backWay: { fromHour: 19.4, untilHour: 21, words: 'the side door, on the snib from when Wayne goes home till Rita cashes up' },
    containers: [
      { id: 'shelf', kind: 'wardrobe', name: 'the shelves of unredeemed pledges', holds: { thing: 'a carriage clock', goods: { honestPence: G_.clockPence } } },
      { id: 'cupboard', kind: 'cupboard', forced: true, name: 'the locked cupboard', holds: { thing: 'a camera in its case', goods: { honestPence: G_.cameraPence } } },
      {
        id: 'tin',
        kind: 'drawer',
        name: 'the biscuit tin of tickets',
        holds: { thing: 'a pawn ticket', paper: "A pawn ticket in Rita's back room: one gold watch, pledged by 'M. Suddaby', never redeemed. Dated the week of the fire." },
      },
    ],
    watchFrom: 'the corner of Chapel Lane',
    window: { thing: "Rita's side window", at: [11.4, -23.6] },
  },
  unit: {
    id: 'unit',
    name: 'unit 2 on the warehouse row',
    place: 'j_unit',
    door: [70, 44.2],
    owner: 'norman',
    ownerAt: 'row1',
    street: 'the warehouse row',
    key: { holder: 'norman', thing: 'the unit key' },
    backWay: { fromHour: 5.5, untilHour: 8, words: 'the loading hatch, unbolted between the watchman going off and the day men coming on' },
    containers: [
      { id: 'crate', kind: 'crate', name: 'the crates by the door', holds: { thing: 'a crate of tinned salmon', goods: { honestPence: G_.crateOfTinsPence }, hand: true } },
      { id: 'desk', kind: 'desk', name: "the foreman's desk", holds: { thing: 'a transistor radio', goods: { honestPence: G_.radioPence } } },
      {
        id: 'drawer',
        kind: 'drawer',
        name: 'the desk drawer',
        holds: { thing: 'a sheaf of delivery notes', paper: "Delivery notes in unit 2: three loads signed for at No. 4 the week before it burned, by a hand that is not the foreman's." },
      },
    ],
    watchFrom: "the net racks by the watchman's hut",
    window: { thing: 'the office window of unit 2', at: [72.4, 44.2] },
  },
};

// Things that can be damaged by hand (A35), besides each site's window: a windscreen, a van's lights, a shop's sign.
export const BREAKABLES = [
  { id: 'hutwin', thing: "the window of Iveson's cabin", at: SITES.hut.window.at, owner: 'dennis', zone: 'the quay' },
  { id: 'pawnwin', thing: "Rita's side window", at: SITES.pawn.window.at, owner: 'rita', zone: 'Chapel Lane' },
  { id: 'unitwin', thing: 'the office window of unit 2', at: SITES.unit.window.at, owner: 'norman', zone: 'the warehouse row' },
  { id: 'scrapcar', thing: "the windscreen of Iveson's pick-up", at: [-108.6, 37.4], owner: 'dennis', zone: 'the quay' },
  { id: 'coinsign', thing: "the sign over Metcalfe's", at: [-8.2, -36], owner: 'hal', zone: 'Quay Street' },
  { id: 'fishvan', thing: "the lights of Laverack's van", at: [52.6, 54.2], owner: 'brenda', zone: 'the quay' },
];

// What is worth lifting from whose pocket (A34: authored, one thing each).
export const POCKETS = {
  dennis: { thing: 'the cabin key', key: 'hut' },
  wayne: { thing: 'the side door key', key: 'pawn' },
  norman: { thing: 'the unit key', key: 'unit' },
  hal: { thing: 'a folded letter', paper: "A letter out of Metcalfe's pocket: 'The Monday arrangement stands whoever sits in the office. K.G.'" },
};
