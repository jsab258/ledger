// LEDGER, the whole game: the system "way". Finding the way with no markers (DESIGN section 4, ADDENDUM A9):
// every place has an address and a landmark; people asked the way give it by landmark if they know it; a lost
// Tom notes the landmark again once, and after three minutes the next person he passes offers the way.
import { register, PLACES, X } from './core.js';
import './way_places.js';
import { G } from '../state.js';
import { RULES } from '../rules.js';
import { PIECE } from './pieces/way_rules.js';
import { sub, bubble } from '../ui.js';
import { note } from '../ledger.js';
import { ROOMS } from '../map.js';

const T = RULES.game.way;
const R = PIECE.fns;
let goalT = 0;

// the person as the rule sees them
const asPerson = (P) => ({
  id: P.id,
  local: P.def ? P.def.local !== false && !P.anon : false,
  keeper: /^k_/.test(P.id || ''),
  police: P.id === 'pc' || P.id === 'ellis' || !!(P.def && P.def.police),
  haunts: P.def && P.def.sched ? hauntsOf(P) : [],
});
const HAUNT = {};
function hauntsOf(P) {
  if (HAUNT[P.id]) return HAUNT[P.id];
  const out = new Set();
  for (const row of P.def.sched || []) {
    const where = String(row[1] || '');
    const room = where.split(':')[0];
    for (const id in PLACES) if (PLACES[id].room === room || id === where) out.add(id);
  }
  return (HAUNT[P.id] = [...out]);
}
export function placeByWords(text) {
  // the place a line of words names, longest name first (so "the ferry landing" beats "the ferry")
  const s = ' ' + String(text || '').toLowerCase() + ' ';
  let best = null,
    len = 0;
  for (const id in PLACES) {
    const p = PLACES[id];
    for (const n of [p.name].concat(p.also || [])) {
      const k = n.toLowerCase();
      if (k.length > len && s.includes(k)) {
        best = p;
        len = k.length;
      }
    }
  }
  return best;
}
const tomXZ = () => {
  const t = G.tom;
  if (t.inCar) return [G.car.x, G.car.z];
  const r = ROOMS[t.space];
  return r && r.street ? [r.street[0], r.street[1]] : [t.x, t.z];
};
export const distTo = (p) => {
  const [x, z] = tomXZ();
  return Math.hypot(p.x - x, p.z - z);
};
// The way to a place, as a person who knows it would say it. Others call this as G.hooks.wayTo(placeId).
export function directions(placeId, P) {
  const p = PLACES[placeId];
  if (!p) return null;
  return P ? R.answer(asPerson(P), p).text : R.answer({ keeper: true }, p).text;
}
export function setGoal(placeId, why) {
  const w = X('way');
  if (placeId && !PLACES[placeId]) return false;
  if (w.goal !== placeId) Object.assign(w, { goal: placeId || null, why: why || null, lost: null, fixed: !!placeId });
  return true;
}
function goalNow() {
  const w = X('way');
  if (w.fixed && w.goal) return w.goal;
  // else the place the to-do names (the Open list's line): nothing Tom has not been told
  const p = placeByWords(G.story.objective || '');
  return p ? p.id : null;
}
function learn(placeId, how, who) {
  const w = X('way');
  if (w.told[placeId]) return;
  w.told[placeId] = Math.round(G.t);
  const p = PLACES[placeId];
  note(`${p.name}: ${p.address}. ${p.landmark[0].toUpperCase() + p.landmark.slice(1)}.`, 'place', 'place_' + placeId, {
    who: who || undefined,
    how: how || 'Told the way',
  });
}

register({
  id: 'way',
  fresh: () => ({ goal: null, why: null, fixed: false, lost: null, told: {}, been: {}, nudges: [] }),
  loaded(w) {
    if (!w.told) w.told = {};
    if (!w.been) w.been = {};
    if (!w.nudges) w.nudges = [];
    G.hooks.wayTo = directions;
    G.hooks.wayGoal = setGoal;
    G.hooks.placeByWords = (t) => {
      const p = placeByWords(t);
      return p ? p.id : null;
    };
    G.hooks.placeKnown = (id) => !!(X('way').told[id] || X('way').been[id]);
  },
  step(dt) {
    if (G.paused || G.story.phase !== 'play') return;
    const w = X('way');
    // places he has been: within reach of the door or the spot (the paper map marks these, 6.3)
    goalT += dt;
    if (goalT < 0.5) return;
    const step = goalT;
    goalT = 0;
    for (const id in PLACES) if (!w.been[id] && distTo(PLACES[id]) < T.arrivedWithinMetres) w.been[id] = Math.round(G.t);
    const gid = goalNow();
    if (!gid) {
      w.lost = null;
      return;
    }
    const p = PLACES[gid];
    const near = G.tom.inCar ? null : nearestPerson();
    const r = R.lostStep(w.lost || {}, gid, distTo(p), step, !!near, {
      nudgeAfter: T.lostNudgeAfterRealSeconds,
      offerAfter: T.lostOfferAfterRealSeconds,
      progress: T.progressCountsMetres,
      arrived: T.arrivedWithinMetres,
    });
    w.lost = r.st;
    if (r.fires === 'arrived') {
      if (w.fixed) Object.assign(w, { goal: null, fixed: false, why: null });
    } else if (r.fires === 'nudge') {
      w.nudges.push({ t: Math.round(G.played), goal: gid, kind: 'nudge' });
      sub(R.ownLine(p), '', 'over', 6);
      learn(gid, 'Worked it out');
    } else if (r.fires === 'offer' && near) {
      w.nudges.push({ t: Math.round(G.played), goal: gid, kind: 'offer', by: near.id });
      const a = R.answer(asPerson(near), p);
      bubble(near, a.knows ? 'Lost, are you? ' + a.text : 'You look lost. ' + a.text, 7);
      if (a.knows) learn(gid, 'Told the way', near.anon ? undefined : near.id);
    }
  },
  // asked in a talk: the person gives the way by landmark if they know it (A9)
  matters(P, a) {
    const gid = goalNow();
    if (!gid || P.anon) return;
    const p = PLACES[gid];
    if (distTo(p) < T.arrivedWithinMetres) return;
    a.push({
      key: 'way_' + gid,
      direct: true,
      ask: 'the way to ' + p.name,
      raise: 'You look like a man looking for somewhere. Is it ' + p.name + '?',
      opts: [
        {
          agree: 1,
          q: 'Do you want the way, or not?',
          yes: ['Yes. Which way is it?', 'Yes. Where do I go?'],
          no: ["No. I'll find it.", 'No. Never mind.'],
          keep: ['Is it far?', 'Do you know it?'],
          keepSay: "It's a small place, the Hook. Nothing's far. Do you want the way, or not?",
          noSay: 'Suit yourself.',
          take: () => {
            const r = R.answer(asPerson(P), p);
            if (r.knows) learn(gid, 'Told the way', P.id);
            return r.text;
          },
        },
      ],
    });
  },
  hook: {
    places: () => Object.values(PLACES).map((p) => Object.assign({}, p)),
    lacks: () => Object.values(PLACES).map((p) => ({ id: p.id, lacks: R.lacks(p) })).filter((r) => r.lacks.length),
    directions: (id, personId) => directions(id, personId ? G.people[personId] : null),
    knows: (personId, id) => R.knows(asPerson(G.people[personId]), PLACES[id]),
    setGoal,
    goal: () => goalNow(),
    state: () => JSON.parse(JSON.stringify(X('way'))),
    placeByWords: (t) => (placeByWords(t) || {}).id || null,
    ground: (id, h) => R.ground(PLACES[id], h),
    distTo: (id) => distTo(PLACES[id]),
  },
});

function nearestPerson() {
  const t = G.tom;
  if (t.space !== 'street') return null;
  let best = null,
    bd = T.lostOfferWithinMetres;
  for (const P of (G.named || []).concat(G.crowd || [])) {
    if (!P || P.dead || P.gone || P.space !== 'street') continue;
    const d = Math.hypot(P.x - t.x, P.z - t.z);
    if (d < bd) {
      bd = d;
      best = P;
    }
  }
  return best;
}
