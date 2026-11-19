// LEDGER. Gossip: how a memory passes from one person to the next, fades, comes back to Tom, and what the street calls him.
import { hyp, chance } from './util.js';
import { G, tally } from './state.js';
import { KINDS, NAMES } from './kinds.js';
import { attached, tomNotices } from './seeing.js';
import { logLine, remember } from './events.js';
import { ledgerSeen, ledgerTalking } from './ledger.js';
import { RULES } from './rules.js';

const GOS = RULES.gossip,
  NAME = RULES.naming;

// ---------- it spreads ----------
export function aff(A, B) {
  let a = GOS.affinityBase;
  if ((A.def.close && A.def.close.includes(B.id)) || (B.def.close && B.def.close.includes(A.id)))
    a += GOS.closeFriendsAdded;
  const teller = GOS.tellerTalkBase + (A.def.talk ?? GOS.talkativeIfNotSet);
  const listener = GOS.listenerTalkBase + GOS.listenerTalkShare * (B.def.talk ?? GOS.talkativeIfNotSet);
  return a * teller * listener;
}

function pickStory(A, B) {
  let best = null,
    bs = 0;
  for (const m of A.mind.mem) {
    if (m.heat < GOS.notWorthTellingBelowHeat || B.mind.by[m.e]) continue;
    const E = G.ev[m.e],
      k = KINDS[E.kind];
    if (k.priv || (E.party && E.party.includes(B.id)) || E.target === B.id) continue;
    const sc = m.heat * (GOS.storyScoreSeverityBase + k.sev) * (attached(m) ? 1 : GOS.storyNotAboutHimTimes);
    if (sc > bs) {
      bs = sc;
      best = m;
    }
  }
  if (!best || chance(A.def.discretion ?? GOS.discretionIfNotSet)) return null;
  return best;
}

export function tell(A, B, m, place) {
  const E = G.ev[m.e];
  remember(B, E, {
    src: 'told',
    from: A.anon ? 'someone' : A.id,
    who: m.who,
    sure: m.sure * GOS.toldSureTimes,
    heat: m.heat * GOS.toldHeatTimes,
    hop: m.hop + 1,
  });
  m.heat = Math.min(1, m.heat + GOS.tellerHeatAdded);
  G.transfers.push({
    a: A.anon ? 'someone' : A.id,
    b: B.id,
    e: E.id,
    t: Math.round(G.t),
    z: place || A.place || '',
  });
  A.chat = { with: B.id, t: GOS.talkPoseRealSeconds };
  B.chat = { with: A.id, t: GOS.talkPoseRealSeconds };
  if (attached(m)) {
    const seenA = !A.anon && tomNotices(A),
      seenB = tomNotices(B);
    if ((seenA || seenB) && hyp(A.x, A.z, G.tom.x, G.tom.z) < GOS.tomCatchesThemWithinMetres) {
      A.mind.look = B.mind.look = GOS.lookAtHimRealSeconds;
      ledgerTalking(A, B);
    }
  }
  logLine(`${A.anon ? 'A passer-by' : A.def.name} told ${B.def.name}: ${KINDS[E.kind].truth(E)}`, 'told');
}

export function gossipTick() {
  const ps = G.named.filter(
    (p) => p.awake && !p.gone && !p.dead && !p.down && p.space !== 'home' && !p.def.police,
  );
  for (let i = 0; i < ps.length; i++) {
    const A = ps[i];
    for (let j = i + 1; j < ps.length; j++) {
      const B = ps[j];
      const reach = A.space === 'street' ? GOS.withinMetresOnStreet : GOS.withinMetresIndoors;
      if (A.space !== B.space || hyp(A.x, A.z, B.x, B.z) > reach) continue;
      if (A.moving && B.moving) continue;
      tally('met', A.id < B.id ? A.id + ' + ' + B.id : B.id + ' + ' + A.id); // counted for the gossip table only
      if (!chance(GOS.chanceTimesAffinity * aff(A, B))) continue;
      const m = pickStory(A, B) || null;
      if (m) tell(A, B, m);
      else {
        const m2 = pickStory(B, A);
        if (m2) tell(B, A, m2);
      }
    }
  }
  // passers-by carry what they saw to the first named person they stand near
  for (const C of G.crowd) {
    if (!C.mind.mem.length || C.gone) continue;
    for (const B of ps) {
      if (B.space !== C.space || hyp(C.x, C.z, B.x, B.z) > GOS.passerByWithinMetres) continue;
      const m = C.mind.mem.find((r) => !B.mind.by[r.e] && r.heat > GOS.passerByTellsAboveHeat);
      if (m && chance(GOS.passerByChance)) {
        tell(C, B, m);
        m.heat = 0;
        break;
      }
    }
  }
}

export function decay(dtMin) {
  const f = Math.exp(-dtMin / GOS.heatFadeGameMinutes);
  for (const P of G.named)
    for (const m of P.mind.mem) {
      const fl = KINDS[G.ev[m.e].kind].forever ? GOS.neverForgottenHeat : 0;
      m.heat = Math.max(fl, m.heat * f);
    }
}

// ---------- it comes back ----------
export function comeback(P) {
  const mind = P.mind;
  if ((mind.coolSay || 0) > G.t) return null;
  let best = null,
    bs = 0;
  for (const m of mind.mem) {
    if (m.said || m.heat < GOS.saysItAboveHeat || !attached(m)) continue;
    const E = G.ev[m.e],
      k = KINDS[E.kind];
    if (E.kind === 'inherit' || k.priv) continue;
    if (m.src === 'self' && !(k.grudge && G.t - m.t > GOS.grudgeSpokenAfterGameMinutes)) continue;
    const sc = m.heat * (GOS.saysScoreSeverityBase + k.sev);
    if (sc > bs) {
      bs = sc;
      best = m;
    }
  }
  return best;
}

export function markSaid(P, m) {
  m.said = true;
  P.mind.coolSay = G.t + GOS.nextRemarkAfterGameMinutes;
  G.stats.comebacks++;
  const E = G.ev[m.e];
  ledgerSeen(
    E,
    P,
    'said',
    m.src === 'told' && m.from && m.from !== 'someone' && P.mind.regard > GOS.namesTheTellerAboveRegard
      ? m.from
      : null,
  );
}

// ---------- what the town calls him ----------
export function knowScore(P) {
  const m = P.mind,
    kinds = new Set();
  for (const r of m.mem) if (attached(r) && G.ev[r.e].kind !== 'inherit') kinds.add(G.ev[r.e].kind);
  return (
    (m.inh ? NAME.knowsOfInheritance : 0) +
    Math.min(kinds.size, NAME.kindsCountedAtMost) * NAME.perKindOfActKnown +
    m.fam * NAME.perFamiliarity
  );
}

// The gate is knowing, not liking.
export function nameLevel(P) {
  const k = knowScore(P);
  if (k >= NAME.levelFourFromScore) return 4;
  if (k >= NAME.levelThreeFromScore) return 3;
  if (k >= NAME.levelTwoFromScore) return 2;
  return k >= NAME.levelOneFromScore ? 1 : 0;
}

export function callName(P) {
  if (P.id === 'sheila') return G.story.flags.sheilaNamed ? 'Tom' : 'new management';
  return NAMES[nameLevel(P)];
}

export function townLevel() {
  const loc = G.named.filter((p) => p.def.local !== false && !p.dead);
  if (!loc.length) return 0;
  const lv = loc.map(nameLevel);
  for (let L = 4; L >= 1; L--)
    if (lv.filter((v) => v >= L).length >= loc.length * NAME.townLevelNeedsShareOfLocals) return L;
  return lv.some((v) => v >= 1) ? 1 : 0;
}

export function loudness() {
  let L = 0;
  for (const P of G.named)
    for (const m of P.mind.mem) {
      if (!attached(m)) continue;
      const k = KINDS[G.ev[m.e].kind];
      if (k.val < 0) L += m.heat * k.sev * -k.val * (m.who === 'tom' ? 1 : NAME.notNamedLoudnessTimes);
    }
  return L;
}

// How hard a name he carries: used by the fighting ladder. Power comes through reputation, not fists.
export function menaceTo(P) {
  let v = 0;
  for (const m of P.mind.mem) {
    if (!attached(m)) continue;
    const k = KINDS[G.ev[m.e].kind];
    if (k.crime >= 1 && k.val < NAME.menaceCountsWhenValueBelow)
      v += NAME.menacePerCrimeKnown * m.sure * (k.crime >= 2 ? NAME.menaceSeriousCrimeTimes : 1);
  }
  return Math.min(NAME.menaceAtMost, v);
}
