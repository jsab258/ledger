// The numbers and the sites of the system "crime" (jobs with the hands: DESIGN 4; A4, A5, A23, A27, A33 to A35, A41).
export const TUNE = {
  // each kind: [how newsworthy 0..1, how it reads -1 menace..+1 decent, crime level 0..3]
  kinds: {
    window_in: [0.6, -0.5, 1], forced_door: [0.6, -0.55, 1], car_taken: [0.65, -0.6, 1], broke_in: [0.55, -0.6, 1], searched: [0.5, -0.5, 1],
    lifted: [0.55, -0.6, 1], pocket: [0.5, -0.6, 1], fenced: [0.3, -0.3, 1], sold_back: [0.45, -0.5, 1], cased: [0.2, -0.2, 0],
    threw_in: [0.3, -0.3, 0], washed: [0.1, 0, 0], dog_barked: [0.2, -0.1, 0], holdup: [0.95, -1, 2], torch_seen: [0.35, -0.3, 0],
  },
  underTheCoatAtMost: 2,
  darkAboveUnlitBy: 0.1, // a room counts as dark for a search under the unlit street's light plus this
  doorWithinMetres: 2.4,
  containerWithinMetres: 2.2,
  casingWithinMetres: 18,
  casingOfferedAfterStandingRealSeconds: 1.5,
  casingStandsRealSeconds: 4,
  liftWithinMetres: 1.2,
  liftFromBehindAboveRadians: 1.6,
  damageShowsGameDays: 1, // force shows on the door for a day
  dogQuietForGameMinutes: 30,
  dogBarksWithinMetres: 14,
  waterWithinMetres: 4,
  quayEdgeZMetres: 61,
  // what things are, for a search by a constable or of the office
  things: {
    envelope: { name: 'the envelope', unlawful: true }, cosh: { name: 'a cosh', unlawful: true, weapon: 'blunt' }, knife: { name: 'a knife', unlawful: true, weapon: 'blade' },
    bat: { name: 'a bat', unlawful: false, weapon: 'blunt' }, crowbar: { name: 'a crowbar', unlawful: false, tool: true }, torch: { name: 'a torch', unlawful: false },
    scrap: { name: 'a scrap of fish', unlawful: false }, gun: { name: 'a revolver', unlawful: true, weapon: 'gun' }, hutkey: { name: "the key to Iveson's hut", unlawful: false, key: 'hut' },
    safekey: { name: "the key to Rita's safe", unlawful: false, key: 'ritasafe' }, sidekey: { name: "a key to Rita's side door", unlawful: false, key: 'rita' }, susanletter: { name: 'a letter on Harbour Board paper', unlawful: false },
    tillnotes: { name: 'a roll of till notes', unlawful: true },
  },
  // break-in sites (3.5.3): each entered three ways (a key, a back way a routine leaves open, or force)
  sites: {
    hut: {
      place: 'hut', name: "Iveson's hut", door: [-101.5, 27.2], key: 'hut', keyFrom: 'lifted from Dennis, or cut by Ian Megginson from a look at it',
      backWay: { what: 'the gap by the crane, before the lad chains it', fromHour: 7.5, untilHour: 17.2 }, dog: true,
      containers: [{ id: 'tinbox', name: 'the tin box under the bench', kind: 'drawer', holds: { pence: 8000, why: "Iveson's tin box" }, line: "Found Iveson's tin box in the hut: eighty pounds, the sum he owes Mickey's book." },
        { id: 'spike', name: 'the receipts on the spike', kind: 'desk', fact: 'iveson_warehouse', line: 'A receipt on the spike: Iveson bought forty tons of scrap out of the burned warehouse, the week before it burned.' }],
    },
    rita: {
      place: 'rita', room: 'rita', name: "Rita's back room", door: [13, -23.6], key: 'rita', keyFrom: 'lent by Wayne, or cut by Ian Megginson',
      backWay: { what: 'the side door Wayne leaves on the latch until six', fromHour: 17.5, untilHour: 18 }, dog: false,
      containers: [{ id: 'ledgerdrawer', name: 'the drawer under the counter', kind: 'drawer', fact: 'rita_book', line: "Rita's own book: who pawns what, and who never comes back for it. Cammack's lads are in it every week." },
        { id: 'safe', name: 'the safe', kind: 'cupboard', needsKey: 'ritasafe', goods: { id: 'rings', name: 'a tray of rings', honestPence: 30000, owner: 'rita' }, line: 'The safe: a tray of rings.' },
        { id: 'shelf', name: 'the back shelf', kind: 'cupboard', goods: { id: 'clock', name: 'a carriage clock', honestPence: 5000, owner: 'rita' }, line: 'A carriage clock off the back shelf.' }],
    },
    harbourback: {
      place: 'harbourback', room: 'harbour', name: "the Harbour Board's back office", door: [-28.5, 42.4], key: 'harbour', keyFrom: 'a clerk who owes him, from Act II',
      backWay: { what: 'the cleaner props the yard door at six in the morning', fromHour: 6, untilHour: 6.6 }, dog: false, fromRung: 2,
      containers: [{ id: 'cabinet', name: 'the filing cabinet', kind: 'cupboard', fact: 'agar_licence', line: "The licence file: Agar's firm wrote the complaint against Mickey's themselves, on the Board's paper." }],
    },
  },
  // things worth lifting from a pocket (A34): authored, one a person
  pockets: { dennis: 'hutkey', wayne: 'safekey', susan: 'susanletter' },
  // windows and things a job or a pressure can ask him to damage (A35)
  damage: [
    { id: 'ritawin', thing: "the pawn shop's window", at: [7.2, -27.5], owner: 'rita' },
    { id: 'coinwin', thing: "Metcalfe's window", at: [-7.2, -34.5], owner: 'hal' },
    { id: 'portside', thing: "a Portside Cars windscreen", at: [6.5, -196], owner: 'the other firm' },
    { id: 'cammackvan', thing: "the lights of Cammack's van", at: [-34, -146], owner: 'cammack' },
  ],
  // parked cars that can be taken (A27): never one with somebody in it
  parked: [
    { id: 'cortina', name: 'the blue Cortina', at: [-3.6, -52], owner: 'sylvia' },
    { id: 'escort', name: 'the brown Escort van', at: [3.6, -128], owner: 'k_grocer' },
  ],
};
export const SCHEDULES = {};
export const PEOPLE = {};
