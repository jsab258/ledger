// LEDGER rule piece: crew (DESIGN section 12, DESIGN-ADDENDUM A16 and A40). Pure.
// A man: { id, role, can: [verbs], nerve, loyalty, ceiling, brittle, wear, owedPence, signed, fate }.
import { TUNE as C } from '../tune/crew.js';

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const round = (v) => Math.round(v * 1000) / 1000;

// Recruiting, by one of two roads. ctx: { needMet, hookHeld, nerve }
function recruit(id, road, ctx) {
  const def = C.recruits[id];
  if (!def) return { ok: false, why: 'Nobody the firm can use.' };
  if (road === 'need' && !ctx.needMet) return { ok: false, why: 'Not yet. What he needs has not been met.' };
  if (road === 'hook' && !ctx.hookHeld) return { ok: false, why: 'There is nothing to hold over him.' };
  if (road !== 'need' && road !== 'hook') return { ok: false, why: 'A man comes by a need or by a hook.' };
  const k = road === 'need' ? C.byNeed : C.byHook;
  return {
    ok: true,
    why: '',
    man: { id, role: def.role, use: def.use, can: def.can.slice(), road, nerve: ctx.nerve ?? 0.5, loyalty: k.loyaltyStarts, ceiling: k.loyaltyCeiling, brittle: k.brittle, wear: 0, owedPence: 0, signed: null, fate: null, withTom: false, post: null },
  };
}
// An order in the field. ctx: { act, near, hasMark, carrying, canDrive }. Answered at once; a man who cannot says why (ER-CREW-01).
function order(man, verb, ctx) {
  const no = (say) => ({ ok: false, say });
  if (!man || man.fate) return no('He is not the firm\'s any more.');
  if (!C.orderWords[verb]) return no('That is not an order.');
  if (verb === 'thats_all') return { ok: true, say: 'Right you are.' };
  if (!ctx.near) return no('He is too far off to hear it.');
  if (!man.can.includes(verb))
    return no({ with_me: "I'm needed here, boss.", fetch_him: "That's not for me to do.", lean_on: "I don't lay hands on people. Never have.", drive: "I don't drive.", take_this: "I can't leave the desk.", wait_here: 'I can\'t stop here.', watch_that: "I'd not see a thing from where I sit." }[verb]);
  if ((verb === 'fetch_him' || verb === 'lean_on') && !ctx.hasMark) return no('Who? Show me him first.');
  if (verb === 'take_this' && !ctx.carrying) return no("You've nothing in your hands, boss.");
  if (verb === 'lean_on' && man.loyalty < 0.4) return no('Not for what you pay me.');
  return { ok: true, say: { with_me: 'Behind you.', wait_here: "I'll be here.", watch_that: "I'll watch it.", fetch_him: "I'll bring him.", take_this: "It'll be in the drawer.", drive: "I'll bring her round.", lean_on: "He'll listen." }[verb] };
}
// A sent verb (D56), from Act II, each through a named man. ctx: { act, target }
function send(man, verb, ctx) {
  const v = C.sent[verb];
  const no = (say) => ({ ok: false, say, asksTwice: false });
  if (!v) return no('That is not a thing he can send a man to do.');
  if ((ctx.act || 1) < C.sentFromAct) return no('Not yet. He has nobody who would go.');
  if (!man || man.fate) return no('He is not the firm\'s any more.');
  if (!ctx.target) return no('Who? It needs a name.');
  if (man.nerve - (man.wear || 0) < v.nerveNeeded) return no("I've not the stomach for that. Ask somebody else.");
  if (man.loyalty < v.loyaltyNeeded) return no("That's more than I owe you.");
  // ER-CREW-04 and ER-CORE-03: what cannot be undone asks twice, and is never done unless told
  return { ok: true, say: 'Leave it with me.', asksTwice: !!v.cannotBeUndone, chain: chain(verb, man.id, ctx.target) };
}
// The chain the town can trace: who told whom, who did what to whom, and who now knows.
function chain(verb, manId, target) {
  return {
    links: [
      { from: 'tom', to: manId, how: 'told him' },
      { from: manId, to: target, how: C.sent[verb] ? C.sent[verb].words : verb },
    ],
    knows: [manId, target],
    accompliceKnows: true,
  };
}
// What happens to a man moves his loyalty (never over its ceiling) and wears his nerve.
function strain(man, what) {
  const m = Object.assign({}, man);
  m.loyalty = round(clamp(m.loyalty + (C.loyalty[what] || 0), 0, m.ceiling));
  m.wear = round(clamp((m.wear || 0) + (C.nerveWornBy[what] || 0), 0, 1));
  if (what === 'paidFair' || what === 'steadied') m.signed = null;
  return m;
}
const low = (m) => m.loyalty < C.signBelowLoyalty || (m.wear || 0) > m.nerve - C.signAboveWear;
const gone = (m) => m.loyalty < C.breaksBelowLoyalty || (m.wear || 0) > m.nerve + C.breaksWhenWearOverNerveBy;
// One look at a man (once a game day). The sign always comes first (ER-CREW-03): a man who has shown none cannot break.
function look(man) {
  const m = Object.assign({}, man);
  if (m.fate) return { man: m, sign: null, broke: null };
  if (!low(m) && !gone(m)) {
    m.signed = null;
    return { man: m, sign: null, broke: null };
  }
  if (!m.signed) {
    m.signed = m.owedPence > 0 ? 'asks_cut' : m.wear > m.nerve - C.signAboveWear ? 'not_at_post' : 'looks_away';
    return { man: m, sign: m.signed, broke: null };
  }
  if (gone(m)) {
    // past his nerve he talks to the police; short of loyalty he goes to whoever pays
    const to = (m.wear || 0) > m.nerve + C.breaksWhenWearOverNerveBy ? 'police' : 'rival';
    m.fate = to === 'police' ? 'frightened' : 'poached';
    return { man: m, sign: m.signed, broke: to };
  }
  return { man: m, sign: m.signed, broke: null };
}
// Pay (A40). A cut is agreed before the job and paid from the tin.
const cut = (takePence) => Math.max(C.nightCutPence, Math.round(takePence * C.nightCutShare));
function settle(man, agreedPence, paidPence, late) {
  const short = paidPence < agreedPence;
  let m = strain(man, short ? 'paidShort' : late ? 'paidLate' : 'paidFair');
  m.owedPence = Math.max(0, agreedPence - paidPence);
  return { man: m, short, flow: { from: 'the tin', to: man.id, pence: paidPence, why: 'his cut' } };
}
// Odds (DESIGN section 7): a fair one-on-one is even, two against one is deadly, three is a beating. A man at his side is one more man.
function odds(tomSide, otherSide) {
  const d = tomSide - otherSide;
  if (d >= 1) return { reads: 'theirs to lose', tomWinsShare: C.oddsTomWinsShare.oneUp };
  if (d === 0) return { reads: 'a fair fight', tomWinsShare: C.oddsTomWinsShare.even };
  if (d === -1) return { reads: 'deadly', tomWinsShare: C.oddsTomWinsShare.oneDown };
  return { reads: 'a beating', tomWinsShare: C.oddsTomWinsShare.twoDown };
}
// Where a follower should stand: about two metres behind Tom, never in the doorway or lane Tom faces (ER-CREW-02).
function followPoint(tx, tz, tang, dist) {
  const d = dist ?? C.followsAtMetres;
  return { x: round(tx - Math.sin(tang) * d + Math.cos(tang) * 0.6), z: round(tz - Math.cos(tang) * d - Math.sin(tang) * 0.6) };
}
export const PIECE = { name: 'crew_rules', fns: { recruit, order, send, chain, strain, look, cut, settle, odds, followPoint } };
