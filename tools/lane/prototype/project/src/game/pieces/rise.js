// RULE PIECE: the rise (DESIGN 14), the escalation dial (DESIGN 7), the firm (A14), fronts and rounds (A15) and
// hold-ups (A41). Pure. Unreal ports it and passes test/cases/rise.json. He rises in position, never in numbers:
// no rung, standing or heat is ever a number on screen.
import { TUNE as T } from '../tune/rise.js';
import { TUNE as E } from '../tune/econ.js';

// Which rung his holdings make. h: { cars, recruits, answeredSheila, fronts, rounds, contract, nightDesk, menAtTheGate, brief }
function rung(h) {
  let r = 1;
  if (h.answeredSheila && h.cars >= T.rung2.cars && h.recruits >= T.rung2.recruits) r = 2;
  if (r === 2 && h.cars >= T.rung3.cars && h.fronts >= T.rung3.fronts && h.rounds >= T.rung3.rounds && h.contract && h.nightDesk) r = 3;
  if (r === 3 && h.fronts >= T.rung4.fronts && h.rounds >= T.rung4.rounds && h.menAtTheGate && h.brief) r = 4;
  return { rung: r, name: T.rungs[r].name, opens: T.rungs.slice(1, r + 1).flatMap((x) => x.opens), office: T.office[r] };
}
// A step never goes back: the rung he has reached is the highest he ever held.
const reached = (was, now) => Math.max(was, now);
// What a person calls him: the gate is knowing, not liking; never above the rung's own name; never back.
function calls(p, rungNow) {
  let n = !p.knowsHim ? 1 : Math.min(rungNow + (p.close ? 1 : 0), p.close ? 4 : 3, rungNow >= 4 && p.close ? 4 : 3);
  if (p.id === 'sheila' && !p.trusts) n = Math.min(n, 1); // Sheila withholds his name until she trusts him
  n = Math.max(n, p.calledBefore || 0);
  return { level: n, name: T.names[n] };
}
// Access as soft keys: a door opens on any one of its keys.
const door = (d, has) => {
  const key = (d.keys || []).find((k) => (k === 'rung' ? has.rung >= d.rung : k === 'dress' ? has.outfit >= d.outfit : !!has[k]));
  return { opens: !!key, by: key || null, wants: key ? null : d.keys };
};
// The dial: a fact in the town's memory. It never moves on a deed nobody saw or heard.
function dial(state, ev) {
  const s = Object.assign({ at: 0, top: 0, quietSinceT: null, who: null }, state);
  if (ev.what === 'quiet') {
    const floor = s.top > 0 ? T.dialNeverBelowAfterRising : 0;
    if (s.at > floor && s.quietSinceT != null && ev.t - s.quietSinceT >= T.dialFallsAfterQuietGameDays * 1440) return Object.assign(s, { at: s.at - 1, quietSinceT: ev.t });
    return s;
  }
  if (!ev.seenOrHeard) return s; // ER-FIGHT-08
  const to = ev.what === 'gun seen' ? 1 : ev.what === 'shot heard' ? 2 : ev.what === 'crew armed' || ev.what === 'second shooting' ? 3 : s.at;
  if (to > s.at) return Object.assign(s, { at: Math.min(to, s.at + (ev.what === 'shot heard' && s.at === 0 ? 2 : 1)), top: Math.max(s.top, to), quietSinceT: ev.t, who: s.who || ev.by || null });
  return Object.assign(s, { quietSinceT: ev.t });
}
const dialMeans = (at) => ({ name: T.dial[at], rivalsTopMenCarry: at >= 1, armedOfficersForGunCalls: at >= 2, armedCars: at >= 3 ? T.armedCarsAtWar : 0, stopAndSearch: at >= 3, shotCanKill: at >= 3, carriersPerSideAtMost: at >= 3 ? T.carriersPerSideAtWar : at >= 1 ? 1 : 0, nightFaresShare: at >= 3 ? T.warNightFaresShare : 1 });
// A gun reaches him only through a person (bought, stolen, taken) or once, found at Mickey's.
const gun = (how, s = {}) => (['bought', 'stolen', 'taken'].includes(how) && s.from ? { has: true, through: s.from } : how === 'found' && !s.foundBefore ? { has: true, through: "Mickey's" } : { has: false, through: null });
// The firm: a bought car joins the board; a rank is won by days there; accounts add fares to the book.
function firm(f, ev) {
  const s = JSON.parse(JSON.stringify(f));
  if (ev.what === 'buy car') {
    if (!ev.seller) return { firm: s, ok: false, why: 'a car is bought from a man selling one' };
    s.cars.push({ id: 'car' + (s.cars.length + 1), driver: null, rank: null, from: ev.seller });
    return { firm: s, ok: true, board: s.cars.map((c) => c.id) };
  }
  if (ev.what === 'hire') {
    const c = s.cars.find((x) => !x.driver);
    if (!c) return { firm: s, ok: false, why: 'no car without a driver' };
    c.driver = ev.who;
    return { firm: s, ok: true };
  }
  if (ev.what === 'place') {
    const c = s.cars.find((x) => x.id === ev.car);
    if (!c || !T.ranks[ev.rank]) return { firm: s, ok: false, why: 'no such car or rank' };
    c.rank = ev.rank;
    return { firm: s, ok: true };
  }
  if (ev.what === 'day') {
    for (const c of s.cars) if (c.driver && c.rank && !T.ranks[c.rank].his && !s.ranks.includes(c.rank)) {
      s.rankDays[c.rank] = (s.rankDays[c.rank] || 0) + 1;
      if (s.rankDays[c.rank] >= T.ranks[c.rank].daysToWin) s.ranks.push(c.rank);
    }
    for (const c of s.cars) if (c.driver && s.unpaidWeeks >= T.driversLeaveUnpaidAfterWeeks) c.driver = null;
    return { firm: s, ok: true };
  }
  if (ev.what === 'account') {
    if (!T.accounts.includes(ev.name) || s.accounts.includes(ev.name)) return { firm: s, ok: false, why: 'no such account, or held already' };
    s.accounts.push(ev.name);
    return { firm: s, ok: true };
  }
  return { firm: s, ok: false, why: 'the board does not do that' };
}
const firmFresh = () => ({ cars: [{ id: 'car1', driver: 'kevin', rank: 'mickeys' }, { id: 'car2', driver: 'terry', rank: 'mickeys' }], ranks: ['mickeys'], rankDays: {}, accounts: [], unpaidWeeks: 0 });
// What the firm's day brings the book, with the other firm taking fares after a drive-off (and giving them back).
const firmFares = (f, hitAndRunFareShare = 1) => ({ carsOut: f.cars.filter((c) => c.driver).length, accountFares: f.accounts.length * T.accountFaresPerDay, share: hitAndRunFareShare, toOtherFirm: Math.round((1 - hitAndRunFareShare) * 100) / 100 });
// Fronts and rounds: money and trouble reach him only through the named man; short if the man is.
function front(id, s) {
  const F = T.fronts[id];
  if (!F) return { ok: false, why: 'no such front' };
  if (!s.held) return { ok: false, why: 'not his' };
  const pence = Math.round(T.frontPaysPencePerWeek * (s.manShort ? 0.5 : 1));
  return { ok: true, through: F.man, pence, washAddsPence: E.frontAddsWashPencePerWeek, trouble: s.trouble ? { reaches: 'through ' + F.man, what: s.trouble } : null, screen: null };
}
// Hold-ups (A41): rare and late, loud, always witnessed, never a game over.
function holdupMay(s) {
  if (s.rung < T.holdupFromRung) return { may: false, why: 'not before the rise has begun' };
  if (!s.weaponOut) return { may: false, why: 'only with a weapon out, on the held key' };
  if (s.gun && !s.gunThrough) return { may: false, why: 'a gun reaches him only through a person' };
  if (!T.holdupTargets.includes(s.target)) return { may: false, why: 'only places with a till and people with a purse' };
  if (s.keeper && (s.keeper.age >= 60 || s.keeper.priest)) return { may: false, why: 'nobody under the content rule' };
  if ((s.heldUpBefore || []).includes(s.target)) return { may: false, why: 'never the same place twice' };
  if (s.thisWeek >= T.holdupOneAWeekThenShopsShut && s.streetOnEdge) return { may: false, why: 'every shop on the street has shut early' };
  return { may: true, why: null, rung: 6 };
}
function holdup(s, input) {
  const till = s.tillPence;
  const base = { witnesses: ['keeper'].concat(s.inside || []), atFaceDistance: true, loud: 'shout', reported: !T.holdupNeverReports.includes(s.target), toldTo: T.holdupNeverReports.includes(s.target) ? 'their own people: a rival hears of it' : 'the police, at once', offence: 'robbery', ellisStagePlus: 1, dial: s.gun ? 'gun seen' : null, shopRefusesHimForGood: true, streetServesColdGameDays: T.streetServesColdGameDays, gameOver: false };
  if (input === 'go') return Object.assign(base, { outcome: 'walked away', take: 0, flow: null });
  if (s.keeperNerve >= 0.7 && input !== 'threaten again') return Object.assign(base, { outcome: 'the keeper stands: a fight on the ladder', take: 0, flow: null });
  if (s.keeperNerve >= 0.5 && input === 'wait' && !s.waited) return Object.assign(base, { outcome: 'stalls', take: 0, flow: null });
  return Object.assign(base, { outcome: 'given', take: till, seconds: input === 'threaten again' ? T.holdupThreatenedRealSeconds : T.holdupTillGivenRealSeconds, worseInEveryMemory: input === 'threaten again', flow: till > 0 ? { from: 'world', to: 'tin', pence: till, why: 'taken from the till at ' + s.target } : null, notesHotGameDays: T.holdupNotesHotGameDays });
}
const till = (hour) => (hour < 12 ? T.tillPenceByHour.morning : hour < 16 ? T.tillPenceByHour.afternoon : T.tillPenceByHour.evening);
export const PIECE = { name: 'rise', fns: { rung, reached, calls, door, dial, dialMeans, gun, firm, firmFresh, firmFares, front, holdupMay, holdup, till } };
