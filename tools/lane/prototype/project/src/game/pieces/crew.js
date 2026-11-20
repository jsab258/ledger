// RULE PIECE: crew (DESIGN 12, A16, A40). Pure. Unreal ports it and passes test/cases/crew.json.
// His power is people. Crew act on orders; an accomplice is the risk, not the alibi; the sign comes before the break.
import { TUNE as T } from '../tune/crew.js';
import { TUNE as E } from '../tune/econ.js';

// An order in the field: two inputs at most, answered within a second; a man who cannot do it says why (ER-CREW-01).
function order(what, man, s = {}) {
  if (!T.orders.includes(what)) return { ok: false, says: 'no such order', inputs: 0 };
  if (!man || man.gone) return { ok: false, says: 'nobody there to tell', inputs: 2 };
  if (what === 'drive' && !man.drives) return { ok: false, says: '"I never learned, boss."', inputs: 2 };
  if (what === 'lean on him' && man.nerve < 0.4) return { ok: false, says: '"Not me. Get Ron."', inputs: 2 };
  if (what === 'take this there' && !s.thing) return { ok: false, says: '"Take what?"', inputs: 2 };
  return { ok: true, says: 'a nod', inputs: 2, answeredWithinSeconds: T.orderAnsweredWithinRealSeconds, alwaysBrakesForPeople: what === 'drive', undoable: true };
}
// A sent verb (Act II): each goes through a named man and leaves a chain the town can trace; the accomplice knows.
function send(verb, through, target, s = {}) {
  if (!T.verbs.includes(verb)) return { ok: false, why: 'not one of the eight' };
  if (!through) return { ok: false, why: 'every sending goes through a named man' };
  if (T.verbsCannotBeUndone.includes(verb) && !s.toldTwice) return { ok: false, why: 'asks twice: this cannot be undone', asksTwice: true };
  return { ok: true, why: null, chain: [{ who: 'tom', how: 'gave the order' }, { who: through, how: 'did it' }].concat(target ? [{ who: target, how: 'it was done to' }] : []), knows: [through], line: `${through} was sent: ${verb}${target ? ', ' + target : ''}.`, shownAtLength: false };
}
// Recruiting (the two roads): meet a need (slow, holds) or spend a hook (quick, brittle).
function recruit(id, road, s = {}) {
  const m = T.men[id];
  if (!m || m.inherited) return { ok: false, why: 'not a recruit' };
  if (road === 'need') return s.needMet ? { ok: true, loyalty: T.needRoadLoyaltyStart, ceiling: m.loyaltyCeiling, brings: m.use, holds: 'slow and holds' } : { ok: false, why: 'his need is not met: ' + (m.need || 'none he will name') };
  if (road === 'hook') return s.hookHeld ? { ok: true, loyalty: T.hookRoadLoyaltyStart, ceiling: Math.min(m.loyaltyCeiling, T.hookRoadLoyaltyCeiling), brings: m.use, holds: 'quick and brittle' } : { ok: false, why: 'he holds no hook on him' };
  return { ok: false, why: 'two roads only' };
}
// How near a man is to breaking: the load of what he knows against his nerve. The sign comes first (ER-CREW-03).
function strain(man, s = {}) {
  const load = (s.knows || 0) * T.loadPerThingHeKnows + (s.frightened ? T.loadWhenFrightened : 0) + (s.arrested ? T.loadWhenArrested : 0) - man.loyalty * T.loadEasedByLoyalty;
  const share = load / man.nerve;
  const shows = share >= T.signAtShareOfNerve;
  const breaks = share >= 1 && !!s.signShown; // never before his sign has been shown
  return { load: Math.round(load * 1000) / 1000, sign: shows ? T.signs[s.paidShort ? 1 : s.arrested ? 2 : 0] : null, breaks, to: breaks ? (s.arrested ? 'talks to the police' : s.rivalNear ? 'talks to a rival' : 'frightened off') : null };
}
// Crew pay and the cut (A40): paid short his loyalty falls and he asks for it first.
function pay(man, takePence, paidPence) {
  const cut = Math.round(takePence * E.crewCutShareOfTake);
  const short = paidPence < cut * E.paidShortBelowShareOfCut;
  const loyalty = Math.max(0, Math.min(man.loyaltyCeiling ?? 1, man.loyalty + (short ? -E.paidShortLoyaltyLost : E.paidFairLoyaltyGained)));
  return { cut, short, loyalty: Math.round(loyalty * 1000) / 1000, asksFirst: short ? 'he asks for his cut' : null, flow: { from: 'tin', to: 'world', pence: paidPence, why: 'the cut, to ' + (man.name || 'his man') } };
}
// A man at his side (A16): one more man in the odds, a witness seen with him, never in the doorway.
const atSide = (men) => ({ hisSide: 1 + men.length, seenWith: men.map((m) => m.id), blocksDoor: false, lagsAtMostSeconds: T.lagsAtMostRealSeconds });
// Crew never do what cannot be undone unless told (ER-CREW-04).
const mayDo = (act, told) => !['kill', 'weapon used', 'burn'].includes(act) || told === act;
// Every fate is reached by a state, never a roll.
function fate(man, s) {
  if (s.killed) return 'killed';
  if (s.arrested && s.broke) return 'talks to the police';
  if (s.arrested) return 'arrested';
  if (s.broke && s.rivalNear) return 'talks to a rival';
  if (s.broke) return 'frightened off';
  if (s.rivalOffer && man.loyalty < 0.4) return 'poached';
  return 'holds';
}
export const PIECE = { name: 'crew', fns: { order, send, recruit, strain, pay, atSide, mayDo, fate } };
