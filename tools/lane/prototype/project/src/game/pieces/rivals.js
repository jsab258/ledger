// RULE PIECE: rivals (DESIGN 13). Pure. Unreal ports it and passes test/cases/rivals.json.
// Three rivals, each after a different ledger, each knowing only what its own people saw or heard. Each climbs the
// same ladder, never skipping a rung, each rung said to his face or shown on his street. Every pressure has three
// answers and none ends the game. No faction is a number.
import { TUNE as T } from '../tune/rivals.js';

const fresh = () => Object.fromEntries(Object.keys(T.rivals).map((id) => [id, { rung: 0, shown: true, lastT: -1e9, sightings: [], answered: {}, truceUntilT: null }]));
// Something one of a rival's own people saw or heard of him. Anything else never reaches the rival (ER-RIV-01).
function learns(id, r, sighting) {
  const R = T.rivals[id];
  if (!R.eyes.includes(sighting.by)) return { rival: r, took: false, why: 'not one of its people' };
  return { rival: Object.assign({}, r, { sightings: r.sightings.concat([{ by: sighting.by, what: sighting.what, t: sighting.t, e: sighting.e ?? null }]) }), took: true, why: null };
}
// May the rival climb now? One rung at a time, only on fresh sightings, only once the last rung was shown, never under a truce.
function climb(id, r, t) {
  if (r.rung >= T.ladder.length - 1) return { rival: r, climbed: false, why: 'at the sit-down' };
  if (!r.shown) return { rival: r, climbed: false, why: 'the last rung has not been said to his face or shown on his street' };
  if (r.truceUntilT != null && t < r.truceUntilT) return { rival: r, climbed: false, why: 'the truce holds' };
  if (t - r.lastT < T.rungNotSoonerThanGameDays * 1440) return { rival: r, climbed: false, why: 'too soon' };
  const fresh = r.sightings.filter((s) => s.t > r.lastT);
  if (fresh.length < T.climbsOnSightingsAtLeast) return { rival: r, climbed: false, why: 'its people have seen too little' };
  const rung = r.rung + 1;
  return { rival: Object.assign({}, r, { rung, shown: false, lastT: t }), climbed: true, why: null, rung: T.ladder[rung], trace: fresh.map((s) => s.by + ': ' + s.what), show: showFor(id, rung) };
}
// How each rung reaches him: said to his face or shown on his street.
function showFor(id, rung) {
  const R = T.rivals[id];
  return [null, { how: 'said to his face', by: R.eyes[0], line: `${R.called} has been asking who runs Mickey's now.` }, { how: 'shown on his street', line: `A man of ${R.called}'s comes into the office and looks the place over.` }, { how: 'said to his face', line: R.pressure, pressure: true }, { how: 'shown on his street', line: R.second, threat: true }, { how: 'said to his face', line: `${R.called} will sit down with him.`, sitDown: true }][rung];
}
const shown = (r) => Object.assign({}, r, { shown: true });
// A pressure's three answers. None ends the game (ER-RIV-03). s: what he has ({ pocketPence, knows: fact about the rival, crew })
function answer(id, r, choice, s = {}) {
  const R = T.rivals[id];
  if (!T.answers.includes(choice)) return { ok: false, why: 'three answers only' };
  const cost = R.taxPencePerWeek || R.feePence || R.damagePence;
  if (choice === 'pay') return s.pocketPence >= cost ? { ok: true, flow: { from: 'pocket', to: 'world', pence: cost, why: 'paid ' + R.called }, rival: Object.assign({}, r, { answered: Object.assign({}, r.answered, { [r.rung]: 'pay' }) }), then: 'it holds for now, and it will be asked again', gameOver: false } : { ok: false, why: 'he has not got it', gameOver: false };
  if (choice === 'defy') return { ok: true, flow: null, rival: Object.assign({}, r, { answered: Object.assign({}, r.answered, { [r.rung]: 'defy' }) }), then: 'the next rung comes, and his people see he stood', gameOver: false };
  if (!s.knows) return { ok: false, why: 'he knows nothing to counter with', gameOver: false };
  return { ok: true, flow: null, rival: Object.assign({}, r, { rung: Math.max(1, r.rung - 1), shown: true, answered: Object.assign({}, r.answered, { [r.rung]: 'counter' }) }), then: 'it steps back a rung: ' + R.called + ' knows he knows', gameOver: false };
}
// The Fixer sells true reads, a meeting and one truce. A read is only ever what the simulation holds.
function fixer(buy, s) {
  const F = T.fixer;
  if (buy === 'read') return s.pocketPence >= F.readPence ? { ok: true, pence: F.readPence, read: { rung: T.ladder[s.rival.rung], knows: s.rival.sightings.map((x) => x.what) }, true: true } : { ok: false, why: 'he has not got it' };
  if (buy === 'meeting') return s.pocketPence >= F.meetingPence ? { ok: true, pence: F.meetingPence, opens: 'an appointment' } : { ok: false, why: 'he has not got it' };
  if (buy === 'truce') return s.trucesSold >= F.truces ? { ok: false, why: 'one truce only' } : s.pocketPence >= F.trucePence ? { ok: true, pence: F.trucePence, truceUntilT: s.t + F.truceLastsGameDays * 1440 } : { ok: false, why: 'he has not got it' };
  return { ok: false, why: 'he sells three things' };
}
// The sit-down that ends Act II: one head; accept, defy, or counter with what he knows. The answer is a standing
// state of the town, read every week after: under (a share goes up each week, the head stops climbing and keeps
// the other two off him), at war (the head's second move comes again every week, and its men are seen armed),
// held off (the head leaves him be, the other two do not).
function sitDown(choice, s = {}) {
  const S = T.sitDown;
  if (choice === 'accept') return { ok: true, how: 'under', state: 'under ' + s.head, tributePencePerWeek: S.underTributePencePerWeek, headClimbs: false, othersHeldAtRung: S.underOthersHeldAtRung, headThreatEveryGameDays: null, headsMenArmed: false };
  if (choice === 'defy') return { ok: true, how: 'war', state: 'at war with ' + s.head, tributePencePerWeek: 0, headClimbs: false, othersHeldAtRung: null, headThreatEveryGameDays: S.warThreatEveryGameDays, headsMenArmed: true };
  if (choice === 'counter') return s.knows ? { ok: true, how: 'holds', state: 'holds ' + s.head + ' off with what he knows', tributePencePerWeek: 0, headClimbs: false, othersHeldAtRung: null, headThreatEveryGameDays: null, headsMenArmed: false } : { ok: false, why: 'he knows nothing to counter with' };
  return { ok: false, why: 'three answers only' };
}
// What stands between him and a rival after the sit-down. sd: the sit-down as kept; id: the rival asked about.
function standing(sd, id, rung) {
  if (!sd) return { mayClimb: true, why: null };
  if (id === sd.head) return { mayClimb: false, why: sd.how === 'war' ? 'at war: it does not climb, it comes' : 'settled at the sit-down' };
  if (sd.how === 'under' && rung >= sd.othersHeldAtRung) return { mayClimb: false, why: 'he is under ' + sd.headCalled + ', and they know it' };
  return { mayClimb: true, why: null };
}
export const PIECE = { name: 'rivals', fns: { fresh, learns, climb, showFor, shown, answer, fixer, sitDown, standing } };
