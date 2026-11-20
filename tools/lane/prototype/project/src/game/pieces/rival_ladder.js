// LEDGER rule piece: the three rivals' ladders, pressures and answers, and the Fixer (DESIGN section 13). Pure.
// A rival's state: { rung 0..5, shown (the rung he stands on has been said or shown), since (game minute of the
// last move), holdUntil, used: [sighting keys], paid (times), settled }.
import { TUNE as V } from '../tune/rivals.js';

const DAY = 1440;
const key = (s) => s.by + ':' + s.e;
// ER-RIV-01 and 02. ctx: { t, act, runEnded, sightings: [{ by, e, t }] } where each sighting is something one of
// this rival's own people saw or heard of him. No sighting, no move; no rung skipped; the last rung first said or shown.
function canAdvance(id, r, ctx) {
  const def = V.rivals[id],
    no = (why) => ({ ok: false, why, from: null });
  if (!def) return no('no such rival');
  if ((ctx.act || 1) < V.startsFromAct && !ctx.runEnded) return no('too early: the business has not grown');
  if (r.settled) return no('settled at the sit-down');
  if (r.rung >= 5) return no('at the top of the ladder');
  if (r.rung > 0 && !r.shown) return no('the last rung has not yet been said or shown');
  if (ctx.t < (r.holdUntil || 0)) return no('held off for now');
  const gap = (ctx.runEnded ? V.gameDaysBetweenRungsIfTheRunEnded : V.gameDaysBetweenRungsAtLeast) * DAY;
  if (r.rung > 0 && ctx.t - (r.since || 0) < gap) return no('too soon after the last');
  const mine = (ctx.sightings || []).filter((s) => def.eyes.includes(s.by)).sort((a, b) => b.t - a.t);
  if (!mine.length) return no('none of its people has seen or heard anything of him');
  const fresh = mine.find((s) => !(r.used || []).includes(key(s)));
  if (r.rung === 0 && !fresh) return no('nothing new has reached it');
  return { ok: true, why: '', from: fresh || mine[0] };
}
function advance(id, r, ctx) {
  const c = canAdvance(id, r, ctx);
  if (!c.ok) return { rival: r, move: null, why: c.why };
  const n = Object.assign({}, r, { rung: r.rung + 1, shown: false, since: ctx.t, used: (r.used || []).concat(key(c.from)) });
  return { rival: n, move: { rival: id, rung: n.rung, kind: V.rungNames[n.rung], from: c.from }, why: '' };
}
const pressure = (id, rung) => (rung === 3 ? V.rivals[id].pressure : rung === 4 ? V.rivals[id].threat : null);
const price = (id, r) => Math.round(V.rivals[id].payPence * Math.pow(V.rivals[id].payRisesTimes, r.paid || 0));
// ER-RIV-03: every pressure has three answers and none ends the game.
// ctx: { t, moneyPence, knows: [facts he holds about this rival] }
function answer(id, r, how, ctx) {
  const def = V.rivals[id];
  if (r.rung < 3 || r.rung > 4) return { ok: false, why: 'There is nothing to answer yet.', rival: r, effects: [], endsTheGame: false };
  const n = Object.assign({}, r);
  if (how === 'pay') {
    const p = price(id, r);
    if ((ctx.moneyPence || 0) < p) return { ok: false, why: 'He has not got it.', rival: r, effects: [], endsTheGame: false };
    n.paid = (r.paid || 0) + 1;
    n.holdUntil = ctx.t + V.paidHoldsGameDays * DAY;
    n.answered = 'pay';
    return { ok: true, why: '', rival: n, effects: [{ what: 'pays', pence: p, to: def.head }, { what: 'the street hears he paid', by: def.eyes[0] }], endsTheGame: false };
  }
  if (how === 'defy') {
    n.since = (r.since || 0) - V.defiedComesSoonerByGameDays * DAY;
    n.answered = 'defy';
    const cost =
      id === 'jensen'
        ? { what: r.rung === 3 ? 'his drivers are taxed at the gate anyway: fewer fares' : 'his least loyal man is offered a place', times: V.defyTaxFaresTimes, days: V.defyTaxGameDays }
        : id === 'agar'
          ? { what: r.rung === 3 ? 'the letter is followed by an inspection of the cars' : 'a car is taken off the road', days: V.defyLetterBringsInspectionInGameDays }
          : { what: r.rung === 3 ? 'trouble on Quay Street that the police put down to him' : 'the office window goes in', seenDeeds: V.defyTroubleSeenDeeds };
    return { ok: true, why: '', rival: n, effects: [cost, { what: 'the street hears he stood', by: def.eyes[0] }], endsTheGame: false };
  }
  if (how === 'counter') {
    const fact = (ctx.knows || [])[0];
    if (!fact) return { ok: false, why: 'He has nothing on them to counter with.', rival: r, effects: [], endsTheGame: false };
    n.rung = Math.max(1, r.rung - V.counteredStepsBackRungs);
    n.shown = true;
    n.holdUntil = ctx.t + V.counteredHoldsGameDays * DAY;
    n.answered = 'counter';
    return { ok: true, why: '', rival: n, effects: [{ what: 'steps back a rung', with: fact }], endsTheGame: false };
  }
  return { ok: false, why: 'Pay, defy, or counter with what he knows.', rival: r, effects: [], endsTheGame: false };
}
// The sit-down (rung 5), three answers; it settles that rival and never ends the game.
function sitDown(id, r, how, ctx) {
  if (r.rung < 5) return { ok: false, why: 'There is no sit-down yet.', rival: r, endsTheGame: false };
  if (how === 'counter' && !(ctx.knows || []).length) return { ok: false, why: 'He has nothing on them to counter with.', rival: r, endsTheGame: false };
  if (!['accept', 'defy', 'counter'].includes(how)) return { ok: false, why: 'Accept, defy, or counter with what he knows.', rival: r, endsTheGame: false };
  return { ok: true, why: '', rival: Object.assign({}, r, { settled: how, shown: true }), endsTheGame: false };
}
// The Fixer sells true reads, a meeting and one truce. A read is made only from the rival's own state.
function fixer(what, state, ctx) {
  const f = state.fixer || {},
    no = (why) => ({ ok: false, why, pence: 0 });
  const p = what === 'read' ? V.fixerReadPence : what === 'meeting' ? V.fixerMeetingPence : what === 'truce' ? V.fixerTrucePence : -1;
  if (p < 0) return no('He sells a read, a meeting and one truce.');
  if ((ctx.moneyPence || 0) < p) return no('He does not work on account.');
  if (what === 'truce' && f.truceUsed) return no('One truce. He said one.');
  const r = state[ctx.rival];
  if (!r) return no('Which of them?');
  if (what === 'read')
    return { ok: true, why: '', pence: p, read: { rival: ctx.rival, rung: r.rung, standsAt: V.rungNames[r.rung], through: V.rivals[ctx.rival].eyes, after: V.rivals[ctx.rival].after, next: r.rung < 5 ? V.rungNames[r.rung + 1] : 'nothing: it is settled at the table' } };
  if (what === 'meeting') return { ok: true, why: '', pence: p, appointment: 'sitDown' };
  return { ok: true, why: '', pence: p, holdUntil: ctx.t + V.fixerTruceGameDays * DAY, truceUsed: true };
}
export const PIECE = { name: 'rival_ladder', fns: { canAdvance, advance, pressure, price, answer, sitDown, fixer } };
