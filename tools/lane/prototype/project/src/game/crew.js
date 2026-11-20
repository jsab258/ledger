// LEDGER, the whole game: the system "crew". His power is people (DESIGN 12; A16, A40; parts 1.7.1, 1.7.2, 1.7.4,
// 2.11.1 to 2.11.4): inherited men and recruits by a need or a hook; orders in two inputs; a man at his side; the
// eight sent verbs, each through a named man who then knows; nerve, loyalty and the sign before a man breaks; the
// cut. Rules: pieces/crew.js. No loyalty or nerve is ever a number on screen.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on } from './core.js';
import { G } from '../state.js';
import { hyp, clamp, quid } from '../util.js';
import { act, seed } from '../events.js';
import { pay } from '../money.js';
import { choose, scene, say, bubble } from '../ui.js';
import { goToPoint } from '../routines.js';
import { RULES } from '../rules.js';
import { PIECE as CREW } from './pieces/crew.js';
import { target as aimedAt } from '../fight.js';
import { ellisEvent } from './law.js';

const T = RULES.game.crew;
const C = CREW.fns;
const nameOf = (id) => (T.men[id] ? T.men[id].name : id);
const man = (id) => X('crew').men[id];
export const inCrew = (id) => !!(man(id) && man(id).in);
export const withHim = () => Object.keys(X('crew').men).filter((id) => man(id).in && man(id).with && P_(id) && here(P_(id), T.orderWithinMetres * 2));
export const recruits = () => Object.keys(X('crew').men).filter((id) => man(id).in && !T.men[id].inherited);

// ---- recruiting (2.11.1): meet a need, slow and holding; or spend a hook, quick and brittle ----
const NEED = { julie: () => G.debts.julie.st === 'forgiven' || (G.x.fares && G.x.fares.learned.julie_drives), norman: () => !!(G.x.jobsx.jobs.side_norman_dog && G.x.jobsx.jobs.side_norman_dog.st === 'done'), shaun: () => !!(G.x.cars && G.x.cars.resprayed), ian: () => !!X('crew').ianPaid };
const HOOK = { lee: () => G.debts.lee.st === 'open' || G.debts.lee.st === 'part', karen: () => false };
export function recruit(id, road) {
  const x = X('crew'),
    m = x.men[id];
  if (!m || m.in) return { ok: false, why: 'already his, or nobody' };
  const r = C.recruit(id, road, { needMet: NEED[id] ? !!NEED[id]() : false, hookHeld: HOOK[id] ? !!HOOK[id]() : false });
  if (!r.ok) return r;
  Object.assign(m, { in: true, loyalty: r.loyalty, ceiling: r.ceiling, road });
  write(`${nameOf(id)} works for him now: ${r.brings}. ${road === 'need' ? 'Taken on for what was needed, which holds.' : 'Taken on by what he had over him, which is brittle.'}`, { who: P_(id) ? id : undefined, how: 'Agreed it' });
  emit('crew.recruited', { id, road });
  return r;
}
// ---- orders in the field (1.7.1): two inputs at most, answered in voice or body within a second ----
function giveOrder(n) {
  const x = X('crew'),
    t = G.tom;
  const near = T.rosterOrder.filter((id) => inCrew(id) && P_(id) && here(P_(id), T.orderWithinMetres));
  const aimed = aimedAt();
  const id = aimed && inCrew(aimed.id) ? aimed.id : near[0];
  if (!id) return false;
  const what = T.orders[n - 1],
    P = P_(id),
    m = man(id);
  const tgt = aimed && aimed.id !== id && !aimed.anon ? aimed : null;
  const r = C.order(what, { nerve: T.men[id].nerve, drives: ['kevin', 'terry', 'julie'].includes(id), gone: P.gone }, { thing: G.x.crime.pockets[0] });
  x.orders.push({ what, to: id, ok: r.ok, says: r.says, t: Math.round(G.t) });
  P.ang = Math.atan2(t.x - P.x, t.z - P.z);
  bubble(P, r.ok ? ['Right, boss.', 'Aye.', 'On it.'][n % 3] : r.says.replace(/"/g, ''), RULES.game.feel.hintAfterStandingStillRealSeconds);
  if (!r.ok) return true;
  if (what === 'with me') Object.assign(m, { with: true, post: null }), Object.assign(P, { override: null, hold: false });
  else if (what === 'wait here') Object.assign(m, { with: false }), Object.assign(P, { hold: true, route: null });
  else if (what === 'watch that') Object.assign(m, { with: false, post: { x: Math.round(P.x), z: Math.round(P.z), sinceT: G.t, zone: G.env.zone(P.x, P.z) } }), Object.assign(P, { hold: true, route: null });
  else if (what === 'fetch him' && tgt) Object.assign(m, { with: false, fetch: tgt.id }), goToPoint(P, tgt.x, tgt.z);
  else if (what === 'take this there') {
    const it = G.x.crime.pockets.shift();
    m.carrying = it;
    m.knows++;
    write(`Gave ${nameOf(id)} ${it.name} to take round. He knows what it is now.`, { who: id, how: 'Did it' });
  } else if (what === 'drive') emit('crew.drive', { id });
  else if (what === 'lean on him' && tgt) lean(id, tgt);
  return true;
}
function lean(id, tgt) {
  const m = man(id);
  tgt.mind.fear = clamp(tgt.mind.fear + T.fearFromLeaning, 0, 1);
  m.knows++;
  act('leaned', { target: tgt.id, through: nameOf(id), silent: true, told: [id, tgt.id] });
  X('crew').sent.push({ verb: 'lean on him', through: id, target: tgt.id, chain: [{ who: 'tom', how: 'gave the order' }, { who: id, how: 'did it' }, { who: tgt.id, how: 'it was done to' }], t: Math.round(G.t) });
}
// ---- a man at his side (A16): follows at about 2 m, never in a doorway, one more man in the odds ----
function sideStep() {
  const t = G.tom,
    x = X('crew');
  for (const id in x.men) {
    const m = x.men[id],
      P = P_(id);
    if (!m.in || !P || P.gone || P.dead) continue;
    if (m.with && t.space === 'street' && P.space === 'street' && !P.fight) {
      const d = hyp(P.x, P.z, t.x, t.z);
      if (d > T.followsFartherThanMetres && (!P.route || d > T.orderWithinMetres)) goToPoint(P, t.x - Math.sin(t.ang) * T.followsAtMetres, t.z - Math.cos(t.ang) * T.followsAtMetres, d > T.orderWithinMetres ? RULES.tom.runningMetresPerSecond : undefined);
      if (d > 40) Object.assign(P, { x: t.x - Math.sin(t.ang) * T.followsAtMetres, z: t.z - Math.cos(t.ang) * T.followsAtMetres, route: null }); // never lags more than a few seconds, never fails the job
      if (!m.seenWithT || G.t - m.seenWithT > 120) {
        m.seenWithT = G.t;
        act('stood_with', { name: nameOf(id), silent: false }); // "Tom and Ron were at the gate" is a sighting
      }
    }
    if (m.fetch) {
      const Q = P_(m.fetch);
      if (Q && hyp(P.x, P.z, Q.x, Q.z) < 3) {
        goToPoint(Q, t.x + 1.5, t.z);
        m.fetch = null;
        m.with = true;
      }
    }
  }
}
// ---- sending (1.7.2): the eight verbs, each through a named man; what cannot be undone asks twice ----
export function sendNow(verb, through, target, toldTwice) {
  const x = X('crew'),
    m = man(through);
  if (!m || !m.in) return { ok: false, why: 'not one of his' };
  const r = C.send(verb, nameOf(through), target ? (T.men[target] ? nameOf(target) : P_(target) ? P_(target).def.name : target) : null, { toldTwice });
  if (!r.ok) return r;
  m.knows++; // the accomplice is the risk, not the alibi
  const P = target ? P_(target) : null;
  if (verb === 'have a man hurt' && P) {
    P.hurt = T.hurtFromSending;
    P.down = true;
    P.downT = G.t + 600;
    P.mind.fear = clamp(P.mind.fear + T.fearFromLeaning, 0, 1);
  } else if (verb === 'lean on a witness' && P) P.mind.fear = clamp(P.mind.fear + T.fearFromLeaning * 1.5, 0, 1);
  else if (verb === 'move or hide a body') {
    const b = G.x.life.bodies.find((q) => !q.found && !q.hidden);
    if (b) b.hidden = true;
  } else if (verb === 'dock, expel or beat one of his own' && man(target)) {
    man(target).loyalty = clamp(man(target).loyalty - 0.3, 0, 1);
    if (man(target).loyalty <= 0.15) Object.assign(man(target), { in: false, fate: 'expelled' });
  } else if (verb === 'send men at a rival property') emit('crew.struck', { rival: target, through });
  else if (verb === 'have someone vouch for him') x.vouched[target || 'the Harbour Board'] = through;
  else if (verb === 'frame someone' && P) x.framed = { who: target, through, t: Math.round(G.t) };
  else if (verb === 'point a plan at a person' && P) x.planned = { who: target, through };
  const Ev = seed('sent', [through].concat(P ? [target] : []).filter((id) => G.people[id]), { through: nameOf(through), verb, name: P ? P.def.name : target || '' });
  x.sent.push({ verb, through, target: target || null, chain: [{ who: 'tom', how: 'gave the order' }, { who: through, how: 'did it' }].concat(target ? [{ who: target, how: 'it was done to' }] : []), e: Ev.id, t: Math.round(G.t) });
  write(r.line[0].toUpperCase() + r.line.slice(1) + ' He knows, now.', { who: G.people[through] ? through : undefined, how: 'Gave the order', ev: Ev.id });
  emit('crew.sent', { verb, through, target });
  return r;
}
async function sendScene() {
  const mine = T.rosterOrder.filter((id) => inCrew(id) && !['sheila', 'pauline'].includes(id));
  const v = await scene(() => choose('', 'Send a man. To do what?', T.verbs.map((q) => q[0].toUpperCase() + q.slice(1) + '.').concat(['Nothing.'])));
  if (v >= T.verbs.length) return;
  const verb = T.verbs[v];
  const w = await scene(() => choose('', 'Through whom?', mine.map(nameOf).concat(['Nobody.'])));
  if (w >= mine.length) return;
  const near = G.named.filter((P) => !P.def.police && P.id !== mine[w] && !P.dead).slice(0, 7);
  const rivals = ['widow', 'agar', 'cammack'];
  const tl = verb === 'send men at a rival property' ? rivals : verb === 'dock, expel or beat one of his own' ? mine.filter((id) => id !== mine[w]) : verb === 'move or hide a body' || verb === 'have someone vouch for him' ? [null] : near.map((P) => P.id);
  let target = tl[0];
  if (tl.length > 1) {
    const k = await scene(() => choose('', 'Who?', tl.map((id) => (T.men[id] ? nameOf(id) : G.people[id] ? G.people[id].def.name : RULES.game.rivals.rivals[id].called)).concat(['Nobody.'])));
    if (k >= tl.length) return;
    target = tl[k];
  }
  let r = sendNow(verb, mine[w], target, false);
  if (r.asksTwice) {
    const sure = await scene(() => choose('', 'This cannot be undone. Send him?', ['Yes. Send him.', 'No.']));
    if (sure !== 0) return;
    r = sendNow(verb, mine[w], target, true);
  }
  if (!r.ok) tell(r.why, '');
}
// ---- nerve, loyalty and breaking (2.11.2, 2.11.3): the sign always comes first ----
function strains() {
  const x = X('crew');
  for (const id in x.men) {
    const m = x.men[id];
    if (!m.in) continue;
    const s = C.strain({ nerve: T.men[id].nerve, loyalty: m.loyalty }, { knows: m.knows, frightened: m.frightened, arrested: m.arrested, signShown: m.signShown, paidShort: m.paidShort, rivalNear: !!(G.x.rivals && Object.values(G.x.rivals.r).some((r) => r.rung >= 2)) });
    if (s.breaks) {
      const fate = C.fate({ loyalty: m.loyalty }, { broke: true, arrested: m.arrested, rivalNear: s.to === 'talks to a rival' });
      Object.assign(m, { in: false, with: false, fate });
      x.fates.push({ id, fate, signShownT: m.signShownT, t: Math.round(G.t) });
      write(`${nameOf(id)} has gone: ${fate}. The sign was there to read.`, { who: G.people[id] ? id : undefined, how: 'Found out' });
      if (fate === 'talks to the police') ellisEvent('detective crime reported');
      emit('crew.broke', { id, fate, knows: m.knows });
    } else if (s.sign && !m.signShown) {
      m.signShown = true;
      m.signShownT = Math.round(G.t);
      m.sign = s.sign;
      tell(`${nameOf(id)}: ${s.sign}.`, '', 7);
      write(`Something is wrong with ${nameOf(id)}: ${s.sign}.`, { who: G.people[id] ? id : undefined, how: 'Saw it himself' });
    }
  }
}
// ---- the cut (A40) ----
export function payCut(id, takePence, paidPence) {
  const m = man(id);
  if (!m) return null;
  if (paidPence > 0 && !pay(paidPence, false, 'the cut, to ' + nameOf(id))) paidPence = 0;
  const r = C.pay({ name: nameOf(id), loyalty: m.loyalty, loyaltyCeiling: m.ceiling ?? T.men[id].loyaltyCeiling }, takePence, paidPence);
  m.loyalty = r.loyalty;
  m.paidShort = r.short;
  X('crew').cuts.push({ id, take: takePence, cut: r.cut, paid: paidPence, short: r.short, t: Math.round(G.t) });
  if (r.short) {
    tell(`"About my cut, boss. It was ${quid(r.cut)} we said."`, nameOf(id));
    write(`${nameOf(id)} was paid short of his cut, and asked for it.`, { who: G.people[id] ? id : undefined, how: 'Said to his face' });
  }
  return r;
}

register({
  id: 'crew',
  fresh: () => ({ men: Object.fromEntries(Object.entries(T.men).map(([id, m]) => [id, { in: !!m.inherited, loyalty: m.loyalty, knows: 0, signShown: false, with: false, post: null, fate: 'holds' }])), orders: [], sent: [], fates: [], cuts: [], vouched: {}, framed: null, planned: null, ianPaid: false }),
  step() {
    if (!G.paused) sideStep();
  },
  hourly(h) {
    if (h % 6 === 0) strains();
  },
  key(code) {
    const m = /^Digit([1-7])$/.exec(code);
    if (!m || G.tom.inCar) return false;
    return giveOrder(+m[1]);
  },
  hotspots(out) {
    const t = G.tom,
      x = X('crew');
    const P = aimedAt();
    if (P && !P.anon && x.men[P.id] && !x.men[P.id].in && hyp(P.x, P.z, t.x, t.z) < RULES.tom.talksWithinMetres) {
      const road = NEED[P.id] && NEED[P.id]() ? 'need' : HOOK[P.id] && HOOK[P.id]() ? 'hook' : null;
      if (road) out.push({ k: 'G', t: road === 'need' ? `Offer ${P.def.name.split(' ')[0]} work` : `Tell ${P.def.name.split(' ')[0]} how he can pay it off`, run: () => recruit(P.id, road) });
    }
    if (t.space === 'iron' && !x.men.ian.in) out.push({ k: 'G', t: x.ianPaid ? 'Offer Ian Megginson work' : "Pay Ian Megginson's rent arrears (twenty pounds)", run: () => {
      if (!x.ianPaid) {
        if (!pay(T.ianRentPence, false, "Ian Megginson's rent arrears")) return tell('He has not got it on him.', '');
        x.ianPaid = true;
        return write("Paid Ian Megginson's rent arrears at the ironmonger's. He cuts keys there, and knows every lock on the street.", { how: 'Did it' });
      }
      recruit('ian', 'need');
    } });
    if (t.space === 'mickeys' && (G.x.acts ? G.x.acts.act : 1) >= 2 && !out.some((o) => o.t === 'Send a man')) out.push({ k: 'T', t: 'Send a man', run: sendScene });
  },
  hook: {
    x: () => X('crew'),
    roster: () => Object.keys(X('crew').men).filter(inCrew).map((id) => ({ id, name: nameOf(id), use: T.men[id].use, with: !!man(id).with })),
    recruit,
    order: giveOrder,
    send: sendNow,
    strains,
    payCut,
    withHim,
    // ER-RISE-01: nothing of loyalty or nerve is a number on screen: the hook is the only place they are read
    man: (id) => man(id),
  },
});
on('law.arrested', () => {
  for (const id of withHim()) man(id).arrested = true;
});
