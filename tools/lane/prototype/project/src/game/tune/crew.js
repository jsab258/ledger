// The numbers of the system "crew" (DESIGN section 12, DESIGN-ADDENDUM A16 and A40): plain data. First values.
export const TUNE = {
  // Inherited: named residents who act on orders. loyalty and its ceiling 0..1; nerve comes from each person's own card.
  inherited: {
    ron: { role: 'the door and the rank', can: ['with_me', 'wait_here', 'watch_that', 'fetch_him', 'take_this', 'lean_on'], loyaltyStarts: 0.7, loyaltyCeiling: 0.95 },
    sheila: { role: 'the book', can: ['wait_here', 'watch_that'], loyaltyStarts: 0.5, loyaltyCeiling: 0.9 },
    pauline: { role: 'the radio', can: ['watch_that'], loyaltyStarts: 0.6, loyaltyCeiling: 0.85 },
    kevin: { role: 'car one, days', can: ['with_me', 'wait_here', 'watch_that', 'take_this', 'drive'], loyaltyStarts: 0.45, loyaltyCeiling: 0.7 },
    terry: { role: 'car two, nights', can: ['with_me', 'wait_here', 'watch_that', 'take_this', 'drive'], loyaltyStarts: 0.6, loyaltyCeiling: 0.85 },
    darren: { role: 'messages, and what he hears', can: ['with_me', 'wait_here', 'watch_that', 'fetch_him', 'take_this'], loyaltyStarts: 0.4, loyaltyCeiling: 0.65 },
  },
  // Recruits from the regulars. need: slow and holds; hook: quick and brittle.
  recruits: {
    julie: { use: 'a driver', role: 'a third car', need: 'Laid off since June. She wants work, and she can drive.', hook: 'She owes the book nine pounds.', can: ['with_me', 'wait_here', 'watch_that', 'take_this', 'drive'] },
    megginson: { use: 'locks', role: 'every lock on the street', need: 'His shop wants a regular order: the firm has its keys cut with him.', hook: 'He cut a key once for a door that was not the customer\'s.', can: ['with_me', 'wait_here', 'watch_that', 'take_this'] },
    lee: { use: 'fists', role: 'the dock gate', need: 'The foreman never picks him. He wants a wage that does not hang on a nod.', hook: 'He owes the book fifteen pounds.', can: ['with_me', 'wait_here', 'watch_that', 'fetch_him', 'take_this', 'lean_on'] },
    norman: { use: 'nights on the warehouse row', role: 'the cold store', need: 'A lift home at six every morning, and somebody to say good morning.', hook: 'He was asleep in the hut the night No. 4 burned.', can: ['wait_here', 'watch_that'] },
    karen: { use: 'a view of the ferry', role: 'the landing', need: 'Her hours at the ferry kiosk were cut. She wants the rank to send her custom.', hook: 'She saw who met the last ferry, and said nothing.', can: ['wait_here', 'watch_that', 'take_this'] },
    shaun: { use: 'paint', role: 'a cab that does not look like a cab', need: 'Signs are dying. He wants the firm\'s cars to letter and keep lettered.', hook: 'He painted out a name for cash and knows whose it was.', can: ['with_me', 'wait_here', 'watch_that', 'take_this'] },
  },
  byNeed: { loyaltyStarts: 0.6, loyaltyCeiling: 0.9, brittle: false },
  byHook: { loyaltyStarts: 0.45, loyaltyCeiling: 0.55, brittle: true },
  // orders in the field, each on one digit (two inputs at most: face the man, press the digit)
  orders: { with_me: 'Digit1', wait_here: 'Digit2', watch_that: 'Digit3', fetch_him: 'Digit4', take_this: 'Digit5', drive: 'Digit6', lean_on: 'Digit7', thats_all: 'Digit8', mark_him: 'Digit9' },
  orderWords: { with_me: 'With me.', wait_here: 'Wait here.', watch_that: 'Watch that.', fetch_him: 'Fetch him.', take_this: 'Take this to the office.', drive: 'Bring the car.', lean_on: 'Lean on him.', thats_all: "That's all." },
  orderReachMetres: 7,
  // the eight sent verbs, in his order (D56), from Act II; nerve each asks of the man, and whether it can be undone
  sent: {
    hurt: { words: 'have him hurt', nerveNeeded: 0.6, loyaltyNeeded: 0.5, cannotBeUndone: true, violent: true },
    plan: { words: 'point a plan at him', nerveNeeded: 0.4, loyaltyNeeded: 0.45, cannotBeUndone: false, violent: false },
    frame: { words: 'put it about that it was him', nerveNeeded: 0.45, loyaltyNeeded: 0.55, cannotBeUndone: true, violent: false },
    lean_witness: { words: 'lean on her to change what she says', nerveNeeded: 0.5, loyaltyNeeded: 0.5, cannotBeUndone: false, violent: true },
    body: { words: 'move it where nobody walks', nerveNeeded: 0.75, loyaltyNeeded: 0.7, cannotBeUndone: true, violent: false },
    discipline: { words: 'dock him, and let the others see it', nerveNeeded: 0.5, loyaltyNeeded: 0.55, cannotBeUndone: false, violent: true },
    property: { words: 'send men at his place', nerveNeeded: 0.55, loyaltyNeeded: 0.5, cannotBeUndone: true, violent: true },
    vouch: { words: 'have him speak for Tom', nerveNeeded: 0.2, loyaltyNeeded: 0.4, cannotBeUndone: false, violent: false },
  },
  sentFromAct: 2,
  sentSettlesAfterGameHours: 6,
  // strain: what moves loyalty and what wears nerve
  loyalty: { paidFair: 0.06, paidShort: -0.14, paidLate: -0.07, stoodBy: 0.08, sentViolent: -0.05, rivalOffer: -0.1, policeAsked: -0.08, quietWeek: 0.02, steadied: 0.1 },
  nerveWornBy: { sentViolent: 0.12, sawViolence: 0.08, policeAsked: 0.15, rivalThreat: 0.12, quietWeek: -0.05 },
  signBelowLoyalty: 0.35,
  signAboveWear: 0.3, // wear above (nerve - this margin... see the piece) shows a sign
  breaksBelowLoyalty: 0.25,
  breaksWhenWearOverNerveBy: 0.1,
  // pay (A40)
  nightCutPence: 1000,
  nightCutShare: 0.3,
  driverWeekPence: 4500,
  wagesDayIndex: 4, // Friday
  unpaidWeeksBeforeADriverLeaves: 2,
  // men at his side (A16)
  followsAtMetres: 2,
  followerLagsAtMostRealSeconds: 10,
  followerCatchesUpBeyondMetres: 14,
  // odds (DESIGN section 7): how a fight reads by numbers on each side
  oddsTomWinsShare: { even: 0.5, oneDown: 0.15, twoDown: 0.03, oneUp: 0.8 },
  // the board
  boardAtRoom: 'mickeys',
  boardAt: [-5.9, -3.2],
  boardWithinMetres: 1.6,
  boardTakesRealSecondsADayAtMost: 60,
  rankEyesWithinMetres: 30,
  alibiWithinMetres: 45,
};
export const SCHEDULES = {
  megginson: [
    { fromHour: 0, place: 'off' },
    { fromHour: 8.5, place: 'corner', doing: 'idle' },
    { fromHour: 12.5, place: 'caff:s1', doing: 'sit' },
    { fromHour: 13.5, place: 'corner', doing: 'idle' },
    { fromHour: 17.5, place: 'off' },
  ],
  karen: [
    { fromHour: 0, place: 'off' },
    { fromHour: 7, place: 'ferry2', doing: 'idle' },
    { fromHour: 13, place: 'caff:s1', doing: 'sit' },
    { fromHour: 14, place: 'ferry2', doing: 'idle' },
    { fromHour: 22.75, place: 'off' },
  ],
};
export const PEOPLE = {
  megginson: { ageYears: 51, nerveZeroToOne: 0.45, venalZeroToOne: 0.5, talkativeZeroToOne: 0.4, discretionZeroToOne: 0.7 },
  karen: { ageYears: 34, nerveZeroToOne: 0.5, venalZeroToOne: 0.45, talkativeZeroToOne: 0.6, discretionZeroToOne: 0.5 },
};
