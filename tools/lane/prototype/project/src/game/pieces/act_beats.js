// LEDGER rule piece: the acts and Act II's beats (DESIGN 16). Pure: plain data in, plain data out.
// Beats fire on states, never on days. S, the state it reads (every field has a default):
//   act 1..3, answered (Sheila has her Sunday answer), choice 'wind' | 'take' | 'silent',
//   rung 1..4, rivalRungs { widow, agar, cammack } each 0..5, lawStage 0..3, seenCrimes (count),
//   friendHolds, arrangement 'kept' | 'ended' | null, faresDriven, nightMoneyEarnedPence, crewRecruits,
//   fired [beat ids, in order], quietDays (game days since the last beat fired), sitDown null | { head, answer }
// T, the numbers: game/tune/acts.js.
import { TUNE } from '../tune/acts.js';
const d = (S) =>
  Object.assign(
    { act: 1, answered: false, choice: null, rung: 1, rivalRungs: {}, lawStage: 0, seenCrimes: 0, friendHolds: false, arrangement: null, faresDriven: 0, nightMoneyEarnedPence: 0, crewRecruits: 0, fired: [], quietDays: 0, sitDown: null },
    S,
  );
const rungs = (S) => ['widow', 'agar', 'cammack'].map((k) => (S.rivalRungs && S.rivalRungs[k]) || 0);
const sum = (a) => a.reduce((x, y) => x + y, 0);

// Act II's beats, in the order they are tried. giver: who brings it (the first living one; else a message at the office).
export const BEATS = [
  { id: 'opens', giver: ['sheila', 'pauline'], test: () => true },
  { id: 'rival_first', giver: ['ron', 'darren'], test: (S) => Math.max(...rungs(S)) >= 1 },
  { id: 'ellis_joins', giver: ['alison', 'darren'], test: (S, T) => S.lawStage >= 1 && S.seenCrimes >= T.ellisJoinsAtSeenCrimes },
  { id: 'collision', giver: ['ron', 'darren'], test: (S) => S.fired.length >= 3 || (S.friendHolds && S.arrangement === 'kept') },
  { id: 'squeeze', giver: ['sheila', 'pauline'], test: (S, T) => sum(rungs(S)) >= T.squeezeAtRivalRungsInAll || rungs(S).filter((r) => r >= 3).length >= 2 },
  { id: 'sitdown_called', giver: ['ron', 'darren'], test: (S, T) => S.fired.includes('collision') && ((S.rung >= T.sitDownAtRung && Math.max(...rungs(S)) >= T.sitDownAtRivalRung) || S.fired.length >= T.sitDownAfterBeats) },
];

// Which act the state is in. Act II opens when the business has grown (any one of four signs), once Sheila has her
// answer; winding it down opens it as well (the ground is open and the rivals come sooner), and so does a quiet
// stretch after her answer (no dead weeks). Act III opens when the sit-down has been answered.
export function actOf(S0, T) {
  const S = d(S0);
  if (S.sitDown && S.sitDown.answer) return 3;
  if (!S.answered) return 1;
  const grown =
    S.rung >= T.opensAtRung ||
    S.faresDriven >= T.opensAtFaresDriven ||
    S.nightMoneyEarnedPence >= T.opensAtNightMoneyEarnedPence ||
    S.crewRecruits >= T.opensAtCrewRecruits ||
    S.choice === 'wind' ||
    S.quietDays >= T.quietDaysBeforeTheNextBeatComes;
  return grown || S.act >= 2 ? 2 : 1;
}
// The next beat due in Act II, or null. A beat whose state holds fires; when nothing has fired for the quiet days,
// the next unfired beat comes by itself (no dead weeks, DESIGN 16 and part 7.4): quiet is a state too.
export function nextBeat(S0, T) {
  const S = d(S0);
  if (actOf(S, T) !== 2 || S.sitDown) return null;
  const left = BEATS.filter((b) => !S.fired.includes(b.id));
  if (!left.length) return null;
  const due = left.find((b) => b.test(S, T));
  if (due) return { id: due.id, giver: due.giver, why: 'state' };
  if (S.quietDays >= T.quietDaysBeforeTheNextBeatComes) return { id: left[0].id, giver: left[0].giver, why: 'quiet' };
  return null;
}
// The head he sits down with: the rival furthest up their ladder against him (ties: the Widow, Agar, Cammack).
export function sitDownHead(S0) {
  const r = rungs(d(S0)),
    i = r.indexOf(Math.max(...r));
  return ['widow', 'agar', 'cammack'][i < 0 ? 0 : i];
}
// Every beat is reachable: from any state, firing what is due and letting quiet days pass ends at the sit-down call.
export function reachable(S0, T) {
  let S = d(S0);
  S.answered = true;
  S.act = 2;
  const order = [];
  for (let i = 0; i < 60 && order.length < BEATS.length; i++) {
    const b = nextBeat(S, T);
    if (b) {
      order.push(b.id + ':' + b.why);
      S = Object.assign({}, S, { fired: S.fired.concat(b.id), quietDays: 0 });
    } else S = Object.assign({}, S, { quietDays: S.quietDays + 1 });
  }
  return order;
}
export const PIECE = {
  name: 'act_beats',
  fns: {
    actOf: (S) => actOf(S, TUNE),
    nextBeat: (S) => nextBeat(S, TUNE),
    sitDownHead,
    reachable: (S) => reachable(S, TUNE),
    beatIds: () => BEATS.map((b) => b.id),
  },
};
