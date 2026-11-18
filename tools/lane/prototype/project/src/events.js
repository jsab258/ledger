// LEDGER. Events and memories: what Tom does becomes an event; each witness keeps a memory of it.
import { clamp } from './util.js';
import { G, tally } from './state.js';
import { KINDS } from './kinds.js';
import { tomTarget, sense, attached, knowsWho, perceivers, witness } from './seeing.js';
import { ledgerSelf, ledgerSeen } from './ledger.js';
import { RULES } from './rules.js';

export const NONE = { see: false, hear: false, c: 0, d: 999 };

const MEM = RULES.memory;

// How well someone knows you decides whether they can name you.
const RANK = { man: 0, coat: 1, cab: 1, owner: 2, tom: 3 };

// ---------- events and memory ----------
export function mkEvent(kind, x = {}) {
  const t = G.tom,
    id = G.nextE++;
  const E = Object.assign(
    {
      id,
      kind,
      t: G.t,
      zone: x.zone || t.zone,
      x: Math.round(t.inCar ? G.car.x : t.x),
      z: Math.round(t.inCar ? G.car.z : t.z),
      coat: !!t.coat,
      car: !!t.inCar,
      wit: [],
    },
    x,
  );
  delete E.silent;
  delete E.told;
  delete E.noiseR;
  G.events.push(E);
  G.ev[id] = E;
  return E;
}

export function logLine(text, tag = 'ev') {
  G.log.push({ t: Math.round(G.t), tag, text });
  if (G.log.length > MEM.logKeepsLines) G.log.splice(0, 100);
  if (G.onLog) G.onLog(text, tag);
}

export function link(P) {
  const m = P.mind;
  for (const r of m.mem) {
    if (r.who === 'coat' && m.knowsCoat) {
      r.who = 'owner';
      r.sure *= MEM.coatLinkedToHimSureTimes;
      r.linked = 1;
      feel(P, r);
    } else if (r.who === 'cab' && m.knowsCab) {
      r.who = 'owner';
      r.sure *= MEM.cabLinkedToHimSureTimes;
      r.linked = 1;
      feel(P, r);
    } else if (
      r.who === 'man' &&
      r.src !== 'told' &&
      r.src !== 'heard' &&
      knowsWho(P) &&
      (r.face > MEM.strangerLinkedAboveFace ||
        (r.sure > MEM.strangerLinkedAboveSure && m.fam > MEM.strangerLinkedAboveFamiliarity))
    ) {
      r.who = r.face > MEM.linkedAsTomAboveFace ? 'tom' : 'owner';
      r.linked = 1;
      feel(P, r);
    }
  }
}

export function feel(P, r) {
  const E = G.ev[r.e],
    k = KINDS[E.kind],
    w = r.src === 'told' ? MEM.regardPerToldAct : MEM.regardPerSeenAct;
  const minds = P.def.upright && k.val < 0 ? MEM.uprightMindsBadActsTimes : 1;
  P.mind.regard = clamp(P.mind.regard + k.val * w * r.sure * minds, -1, 1);
  if (k.crime >= MEM.seriousCrimeFromLevel) {
    const fright = r.src === 'told' ? MEM.fearFromSeriousCrimeTold : MEM.fearFromSeriousCrimeSeen;
    P.mind.fear = clamp(P.mind.fear + fright * (MEM.fearNerveBase - P.def.nerve), 0, 1);
  }
}

export function remember(P, E, m) {
  const mind = P.mind;
  let r = mind.by[E.id];
  if (r) {
    const was = attached(r);
    if (RANK[m.who] > RANK[r.who]) r.who = m.who;
    r.sure = Math.max(r.sure, m.sure);
    r.heat = Math.min(1, Math.max(r.heat, m.heat) + MEM.heatAddedWhenSeenAgain);
    if (m.src === 'saw' && r.src === 'told') r.src = 'saw';
    if (!was && attached(r)) feel(P, r);
    return r;
  }
  r = {
    e: E.id,
    src: m.src,
    from: m.from || null,
    who: m.who,
    sure: m.sure,
    heat: m.heat,
    t: G.t,
    said: false,
    hop: m.hop || 0,
    face: m.face || 0,
  };
  mind.mem.push(r);
  mind.by[E.id] = r;
  if (E.kind === 'inherit') mind.inh = 1;
  if (attached(r)) {
    feel(P, r);
    if (E.coat && (E.kind === 'coat_day' || m.src !== 'told')) mind.knowsCoat = 1;
    if (E.kind === 'cab_drive' || E.kind === 'fare' || E.kind === 'free_ride') mind.knowsCab = 1;
  }
  link(P);
  return r;
}

// A discrete act by Tom, witnessed by whoever can see or hear it right now.
export function act(kind, x = {}) {
  const k = KINDS[kind];
  if (x.noiseR) G.tom.noiseP = Math.max(G.tom.noiseP, x.noiseR);
  const told = x.told || [],
    silent = x.silent;
  const E = mkEvent(kind, x);
  const T = tomTarget();
  if (E.target) {
    const P = G.people[E.target];
    if (P) {
      E.name = E.name || P.def.name;
      partyTo(P, E);
    }
  }
  for (const id of told) {
    const P = G.people[id];
    if (P) partyTo(P, E);
  }
  if (!silent) {
    for (const P of perceivers()) {
      if (P.id === E.target || told.includes(P.id)) continue;
      const s = sense(P, T);
      if (s.see) witness(P, E, s, T);
      else if (s.hear && k.loud && !s.asleep) {
        tally('heard');
        remember(P, E, { src: 'heard', who: 'man', sure: MEM.heardSure, heat: MEM.heardHeat });
        P.alert = { x: T.x, z: T.z, t: MEM.alertLastsRealSeconds };
      } else if (s.hear && s.asleep && k.loud) P.wake = 1;
    }
  }
  if (!k.noself) ledgerSelf(E);
  logLine(k.truth(E) + (E.wit.length ? '. Seen by ' + E.wit.length : ''), 'act');
  return E;
}

function partyTo(P, E) {
  const who = knowsWho(P) || P.mind.fam > MEM.partyNamesHimAboveFamiliarity ? 'tom' : 'man';
  const heat = clamp(KINDS[E.kind].sev + MEM.heatAddedToSeverity, 0, 1);
  remember(P, E, { src: 'self', who, sure: 1, heat, face: MEM.partyFace });
  P.mind.fam = clamp(P.mind.fam + MEM.partyFamiliarityGain, 0, 1);
  if (!E.party) E.party = [];
  E.party.push(P.id);
  if (!KINDS[E.kind].noself) ledgerSeen(E, P, 'there');
}

// A story that starts with other people (the inheritance, Ellis asking, a good word).
export function seed(kind, ids, x = {}) {
  const E = mkEvent(kind, Object.assign({ zone: 'Quay Street' }, x));
  for (const id of ids) {
    const P = G.people[id];
    if (P)
      remember(P, E, {
        src: 'self',
        who: 'tom',
        sure: 1,
        heat: clamp(KINDS[kind].sev + MEM.heatAddedToSeverity, 0, 1),
      });
  }
  return E;
}

// ---------- the Ledger: only what Tom himself has seen and heard ----------
export const BR = { talking: 0, window: 1, saw: 2, bought: 3, asked: 3, there: 4, said: 5 };

export function newMind() {
  return { fam: 0, regard: 0, fear: 0, mem: [], by: {}, attn: 0, look: 0 };
}
