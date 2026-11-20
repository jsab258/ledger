// LEDGER, the whole game: hold-ups of shops and people (DESIGN-ADDENDUM A41; part 1.6.15). A system of its own,
// state under G.x.holdup. Rare and late, loud, always witnessed, never a game over. Rules: pieces/holdup_rules.js.
import { register, emit } from './core.js';
import { G } from '../state.js';
import { act } from '../events.js';
import { sub } from '../ui.js';
import { note } from '../ledger.js';
import { target, setOn } from '../fight.js';
import { earn } from '../money.js';
import { send } from '../routines.js';
import { nameLevel } from '../gossip.js';
import { PIECE } from './pieces/holdup_rules.js';
import { TUNE as D } from './tune/dial.js';
import { P_, X, knowers, rungNow, zoneOf, near } from './rise_util.js';

const R = PIECE.fns;
const st = () => X('holdup');
const HOUSES = ['home', 'ada', 'boarding'];

function targetInfo(P) {
  const t = G.tom;
  if (!P) return { kind: 'none' };
  if (P.inCar) return { kind: 'car' };
  if (HOUSES.includes(t.space)) return { kind: 'house' };
  const d = P.def || {};
  return { kind: P.keeper ? 'shop' : 'person', open: !!P.keeper && P.space === t.space, sex: d.sex, age: d.age, priest: P.id === 'walsh' };
}
function watchersOf(P) {
  const t = G.tom;
  let n = 0;
  for (const Q of G.named.concat(G.crowd))
    if (Q !== P && !Q.gone && !Q.dead && !Q.down && Q.space === t.space && Math.hypot(Q.x - t.x, Q.z - t.z) < 12) n++;
  return n;
}
const purse = (P) => (P.keeper ? R.till(Math.floor(G.t / 1440)) : Math.round(D.holdUpPursePence * (0.6 + ((P.def && P.def.venal) || 0.4))));
const SAY = {
  gives: ['All right. All right. Take it. Take it and go.', "It's all there is. I've seen your face, mind."],
  runs: ['He is off down the street before the words are out.'],
  shouts: ['THIEF! He has a knife! Somebody!'],
  stands: ['No. Put it away, or use it.'],
};
// The hold-up itself. Returns what happened, or why it did not (ER-HOLDUP-01: each refusal is said).
export function holdUp(P) {
  const t = G.tom,
    x = st();
  const ctx = { rung: rungNow(), weapon: t.weapon, shown: !!t.armed, target: targetInfo(P) };
  if (!P) return { ok: false, why: 'Nobody is in front of him.' };
  const c = R.can(ctx);
  if (!c.ok) {
    sub(c.why, '', 'over', 4);
    return c;
  }
  if (x.banned[P.id] && P.keeper && false) return c;
  const watchers = watchersOf(P),
    covered = !!t.coat,
    how = R.outcome({ nerve: (P.def && P.def.nerve) ?? 0.5 }, { watchers, weapon: t.weapon }),
    E = act('holdup', { target: P.id, name: P.def && P.def.name, weapon: t.weapon, noiseR: how === 'shouts' ? D.holdUpShoutCarriesMetres : D.holdUpNoiseCarriesMetres });
  // ER-HOLDUP-02: the mark always holds it, at the face rung, or at the mark rung when his face was covered
  const w = R.witness(covered),
    m = P.mind && P.mind.by && P.mind.by[E.id];
  if (m && covered) {
    m.who = 'coat';
    m.sure = w.sure;
    m.face = 0.1;
  }
  const took = R.take(purse(P), how);
  if (took) earn(took, true, 'a hold-up');
  sub(SAY[how][E.id % SAY[how].length], how === 'runs' ? '' : P.anon ? P.def.desc : P.def.name.split(' ')[0], how === 'shouts' ? 'face' : '', 4);
  if (how === 'stands') setOn([P]);
  else if (how !== 'gives' && !P.anon) send(P, 'phone', 'idle', G.t + 90);
  const street = zoneOf(P) || t.zone;
  const rec = { t: Math.round(G.t), e: E.id, mark: P.id, street, how, took, covered, rung: w.rung, watchers, reached: false, reported: null, ellisDue: null, trace: R.aftermath({ t: Math.round(G.t), mark: P.id, street }) };
  x.list.push(rec);
  x.edge[street] = rec.t + D.holdUpStreetOnEdgeGameDays * 1440;
  x.faresDownUntil = rec.t + D.holdUpFaresFallGameDays * 1440;
  if (P.keeper) x.banned[P.id] = true;
  note(`Held up ${P.anon ? P.def.desc : P.def.name} on ${street} with the ${t.weapon}. ${took ? 'Took what was there.' : 'Got nothing.'} ${covered ? 'Collar up; he saw the coat.' : 'He saw his face.'}`, 'note', 'holdup' + E.id, { how: 'Did it', ev: E.id });
  if (G.hooks.dialTell) G.hooks.dialTell(R.dialEvent(t.weapon, knowers(E).length).type, E);
  emit('holdup', rec);
  emit('deed', { E });
  emit('street:edge', { zone: street, until: x.edge[street], deeds: D.holdUpCountsAsSeenDeedsOnItsStreet, by: P.id });
  if (G.hooks.save) G.hooks.save();
  return { ok: true, how, took, rec };
}
// The mark was reached before the phone (talked round, paid or threatened): no report; the street's talk stands.
function reached(markId) {
  for (const r of st().list)
    if (r.mark === markId && !r.reported) {
      r.reached = true;
      r.trace = R.aftermath({ t: r.t, mark: r.mark, street: r.street, reached: true });
    }
}

register({
  id: 'holdup',
  fresh: () => ({ list: [], edge: {}, faresDownUntil: 0, cool: {}, banned: {} }),
  loaded() {
    G.hooks.streetOnEdge = (zone) => (st().edge[zone] || 0) > G.t;
    G.hooks.holdupReached = reached;
    G.hooks.holdupFaresTimes = () => (st().faresDownUntil > G.t ? D.holdUpFaresTimes : 1);
  },
  minute(tm) {
    const x = st();
    for (const r of x.list) {
      const M = P_(r.mark);
      // the walk ends: the report is made, unless he was reached first (or a keeper's own statement at his counter)
      if (!r.reported && !r.reached && tm >= r.t + 30 && !(M && M.dead)) {
        r.reported = tm;
        r.ellisDue = (Math.floor(r.t / 1440) + 1) * 1440 + D.holdUpEllisComesAtHour * 60;
        emit('police:reported', { E: G.ev[r.e], by: r.mark, crime: 'robbery', hours: D.holdUpArrestCostsGameHours, ellisAt: r.ellisDue, street: r.street });
      }
      if (r.ellisDue && tm >= r.ellisDue && !r.ellisCame) {
        r.ellisCame = tm;
        emit('ellis:due', { why: 'a robbery reported', street: r.street, E: G.ev[r.e], by: r.mark });
        note(`DS Ellis is on ${r.street} this morning, asking about the hold-up.`, 'police', 'holdupellis' + r.e, { how: 'Seen on the street' });
      }
    }
  },
  hourly() {
    // a cooler name: people who had come to call him Tom, and now hold the hold-up, say Mr Nowak for a week
    const x = st();
    for (const r of x.list) {
      if (G.t > r.t + D.holdUpNameCoolsGameDays * 1440) continue;
      const E = G.ev[r.e];
      if (!E) continue;
      for (const id of knowers(E)) {
        const Q = P_(id);
        if (Q && !Q.anon && !x.cool[id] && (nameLevel(Q) >= 2 || id === r.mark)) x.cool[id] = { until: r.t + D.holdUpNameCoolsGameDays * 1440, said: false, from: r.mark, e: r.e };
      }
    }
  },
  step() {
    if (G.paused || G.tom.inCar) return;
    const x = st();
    for (const id in x.cool) {
      const c = x.cool[id],
        Q = P_(id);
      if (c.said || c.until < G.t || !Q || !near(Q, 6)) continue;
      c.said = true;
      sub(id === c.from ? 'Not you. Out.' : 'Mr Nowak.', Q.def.name.split(' ')[0], 'face', 4);
      note(`${Q.def.name} would not use his name after the hold-up.`, 'note', 'cool' + id + c.e, { who: id, how: 'Said to his face', ev: c.e });
    }
  },
  hotspots(out) {
    const t = G.tom;
    if (t.inCar || !t.armed || !R.tier(t.weapon)) return;
    const P = target();
    if (P && Math.hypot(P.x - t.x, P.z - t.z) < D.holdUpWithinMetres) out.push({ k: 'H', t: P.keeper ? 'Demand the till' : 'Demand his money', run: () => holdUp(P) });
  },
  key(code) {
    const t = G.tom;
    if (code !== 'KeyH' || t.inCar || !t.armed || !R.tier(t.weapon)) return false;
    const P = target();
    if (!P || Math.hypot(P.x - t.x, P.z - t.z) >= D.holdUpWithinMetres) return false;
    holdUp(P);
    return true;
  },
  hook: {
    // stage(targetId, { weapon, covered, shown }): puts Tom beside the mark with the weapon out and does it
    stage(id, o = {}) {
      const P = P_(id),
        t = G.tom;
      if (!P) return { ok: false, why: 'nobody of that name' };
      if (o.weapon !== undefined) t.weapon = o.weapon;
      t.armed = o.shown !== false && !!t.weapon;
      if (o.covered !== undefined) {
        t.hasCoat = t.hasCoat || o.covered;
        t.coat = !!o.covered;
      }
      if (!P.keeper || o.move) {
        t.space = P.space === 'home' || P.space === 'away' ? t.space : P.space;
        t.x = P.x + 1.2;
        t.z = P.z;
      }
      return holdUp(P);
    },
    reached,
    list: () => st().list,
    chain: (i = 0) => {
      const r = st().list[i];
      return r ? r.trace.map((s) => `${s.what} (through ${s.by})`) : [];
    },
    onEdge: (zone) => (st().edge[zone] || 0) > G.t,
    cool: () => st().cool,
    can: (id) => PIECE.fns.can({ rung: rungNow(), weapon: G.tom.weapon, shown: !!G.tom.armed, target: targetInfo(P_(id)) }),
  },
});
