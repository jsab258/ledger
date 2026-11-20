// The numbers of the system "rise" (the four rungs, access as soft keys, property that reacts): plain data.
// DESIGN section 14. First values.
export const TUNE = {
  // What each rung is called, what he holds, what opens, and what must be true to stand on it.
  rungs: [
    null,
    {
      called: 'the new owner',
      name: 'The nephew',
      holds: ['two cars', 'two drivers', 'Ron at the door', 'Sheila at the book', "Mickey's debt book", 'the Monday run'],
      opens: ['the street', 'the rank', 'the landing'],
      needs: {},
      changes: [],
    },
    {
      called: 'Nowak',
      name: 'The firm is his',
      holds: ['his answer to Sheila', 'a third car', 'a first recruit'],
      opens: ["Mickey's locked office and the real book, on trust", "Rita's back room"],
      needs: { tookItOn: true, carsAtLeast: 3, recruitsAtLeast: 1 },
      changes: [
        'People who know him say Nowak, not the new owner.',
        "The door in the back room stands open and Mickey's desk is his.",
        'A third cab stands on the rank.',
        "Rita's back room lets him in.",
      ],
    },
    {
      called: 'Tom',
      name: "The Hook's firm",
      holds: ['five cars', 'a night desk', 'a first front', 'a first round', 'the cold-store shift contract'],
      opens: ['the dock gate', "the Harbour Board's counter", 'a solicitor'],
      needs: { carsAtLeast: 5, nightDesk: true, frontsAtLeast: 1, roundsAtLeast: 1, coldStore: true },
      changes: [
        'People who know him say Tom.',
        'His cabs pass him in the street.',
        'The office has a night desk and a second telephone.',
        'The man on the dock gate lifts the bar for him.',
        'Shopkeepers hold the door.',
      ],
    },
    {
      called: 'Tom',
      calledByAFew: 'Tommy',
      name: "The port's man",
      holds: ['fronts and rounds across the Hook', 'men at the dock gate, the cold store and the landing', 'a brief on call'],
      opens: ['the sit-down', 'people step aside'],
      needs: { frontsAtLeast: 3, roundsAtLeast: 2, postsAtLeast: 3, solicitor: true },
      changes: [
        'Two or three people say Tommy.',
        'People step aside on the pavement.',
        'His men stand at the dock gate, the cold store and the landing.',
        "The flat above the office is his, not Mickey's.",
      ],
    },
  ],
  // Doors as soft keys: standing (the rung), dress (0 as he arrived, 1 a decent jacket, 2 a good overcoat),
  // or instead an introduction by a named person, or an appointment the Fixer brokers.
  doors: {
    mickeysOffice: { name: "Mickey's locked office", standingRung: 2, dress: 0, introducedBy: ['sheila'] },
    ritasBackRoom: { name: "Rita's back room", standingRung: 2, dress: 0, introducedBy: ['wayne', 'rita'] },
    dockGate: { name: 'the dock gate', standingRung: 3, dress: 0, introducedBy: ['lee', 'ron'] },
    harbourCounter: { name: "the Harbour Board's counter", standingRung: 3, dress: 1, introducedBy: ['susan'], appointment: true },
    solicitor: { name: "a solicitor's office", standingRung: 3, dress: 1, introducedBy: [], appointment: true },
    sitDown: { name: 'the sit-down', standingRung: 4, dress: 2, introducedBy: [], appointment: true },
  },
  nameHeardWithinGameHours: 20,
  nameSaidWithinMetres: 9,
  // property that reacts: the office and the flat, by rung
  officeByRung: [null, "Mickey's, as he left it", 'his desk, the back door open', 'a night desk and a second telephone', 'a full room, the board chalked to the edge'],
  flatByRung: [null, "Mickey's flat, shut up", "Mickey's flat, shut up", 'aired, a bed made', "his own, nothing of Mickey's left on the walls"],
};
export const SCHEDULES = {};
export const PEOPLE = {};
