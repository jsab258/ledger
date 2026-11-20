// LEDGER rule piece: the endings as states (DESIGN 16; QUESTIONS 1 to the recommended answer: the five built states
// kept underneath, three endings shown, each with a better and a plainer way to turn out). Pure.
// I, what the close reads:
//   woundDown (he told Sheila he was winding it down), booksHold (the inspection), caseSinksFirm (Ellis's case is
//   strong enough to take the firm), handedOver (a crewman took it over, on his offer), friendHolds (one friendship
//   still counts him), streetFact (the street holds his rackets as fact), hunted (a manhunt), huntedForKilling
// Out: state (one of the five built states), shown (one of three), turn 'better' | 'plainer'.
export const STATES = ['both', 'kingdom', 'quiet', 'straight', 'burn'];
export const SHOWN = { both: 'The Kingdom', kingdom: 'The Kingdom', quiet: 'The Straight Life', straight: 'The Straight Life', burn: 'Burn Both' };
const n = (I) => {
  const o = Object.assign({ woundDown: false, booksHold: true, caseSinksFirm: false, handedOver: false, friendHolds: false, streetFact: false, hunted: false, huntedForKilling: false }, I);
  if (o.huntedForKilling) o.hunted = true;
  return o;
};
export function ending(I0) {
  const I = n(I0);
  const business = !I.woundDown && !I.handedOver && I.booksHold && !I.caseSinksFirm && !I.hunted;
  let state;
  if (business) state = I.friendHolds && !I.streetFact ? 'both' : 'kingdom';
  else if (I.friendHolds && !I.huntedForKilling) state = (I.handedOver || I.woundDown) && !I.hunted && !I.caseSinksFirm ? 'quiet' : 'straight';
  else state = 'burn';
  return { state, shown: SHOWN[state], turn: state === 'both' || state === 'quiet' ? 'better' : 'plainer' };
}
// Every cost that decides the ending shows its sign before it decides (D58; the ending signs of 30 Sep). The signs
// a state of the world gives Tom, each a thing he sees or is told.
export const SIGNS = {
  inspector_cold: "The inspector's manner has gone cold: the books have stopped standing.",
  sheila_line: 'Sheila has said it plainly: the true books have crossed the line.',
  ellis_tells: 'DS Ellis no longer asks. She tells: the case will take the firm.',
  manhunt: 'A police car on the street and his description said aloud: they are hunting him.',
  manhunt_killing: 'They are hunting him for a killing.',
  successor_took: 'The offer to take the firm over was made, and he said yes.',
  wound_down: 'He told Sheila he was winding it down.',
  friend_act: 'A friend did something for him, unasked: that friendship still counts him.',
  friend_gone: 'The one friend has stopped calling. Nobody does anything for him unasked.',
  overheard_fact: 'He has overheard his rackets told as plain fact on the street.',
};
export function signsFor(I0) {
  const I = n(I0),
    s = [];
  if (!I.booksHold) s.push('inspector_cold', 'sheila_line');
  if (I.caseSinksFirm) s.push('ellis_tells');
  if (I.huntedForKilling) s.push('manhunt', 'manhunt_killing');
  else if (I.hunted) s.push('manhunt');
  if (I.handedOver) s.push('successor_took');
  if (I.woundDown) s.push('wound_down');
  s.push(I.friendHolds ? 'friend_act' : 'friend_gone');
  if (I.streetFact) s.push('overheard_fact');
  return s;
}
// Tom's reading (DESIGN 10, 16): how things stand as he sees them, built only from signs he was given. It predicts
// the ending the state gives (ER-END-02, ER-END-03). quiet: he has been given no sign of a cost.
export function reading(signs) {
  const has = (k) => signs.includes(k);
  const I = {
    booksHold: !has('inspector_cold') && !has('sheila_line'),
    caseSinksFirm: has('ellis_tells'),
    hunted: has('manhunt'),
    huntedForKilling: has('manhunt_killing'),
    handedOver: has('successor_took'),
    woundDown: has('wound_down'),
    friendHolds: has('friend_act') && !has('friend_gone'),
    streetFact: has('overheard_fact'),
  };
  const e = ending(I);
  const costs = signs.filter((k) => k !== 'friend_act');
  return { predicts: e.state, shown: e.shown, turn: e.turn, quiet: costs.length === 0, lines: signs.map((k) => SIGNS[k]).filter(Boolean) };
}
// The balance sweep (ER-END-02): over every state of the world, the reading built from the signs that state gives
// predicts the ending that state gets, and no ending but the one with nothing lost lands on a quiet reading.
export function sweep() {
  const keys = ['woundDown', 'booksHold', 'caseSinksFirm', 'handedOver', 'friendHolds', 'streetFact', 'hunted', 'huntedForKilling'];
  let cases = 0,
    wrong = 0,
    quietLoss = 0;
  const seen = {};
  for (let m = 0; m < 1 << keys.length; m++) {
    const I = {};
    keys.forEach((k, i) => (I[k] = !!(m & (1 << i))));
    const e = ending(I),
      r = reading(signsFor(I));
    cases++;
    seen[e.state] = (seen[e.state] || 0) + 1;
    if (r.predicts !== e.state) wrong++;
    if (r.quiet && e.state !== 'both') quietLoss++;
  }
  return { cases, wrong, quietLoss, statesReached: STATES.filter((s) => seen[s]).length };
}
export const PIECE = { name: 'ending_state', fns: { ending, signsFor, reading, sweep, shownOf: (s) => SHOWN[s] } };
