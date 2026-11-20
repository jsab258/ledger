// Rule piece: the beat constable's challenge, the search and the chase (DESIGN section 8, addendum A3, A13). Pure.
import { TUNE } from '../tune/law.js';
const BT = TUNE.beat;
// Does he have cause to challenge? tom: { night, carrying, running, bloodied, weaponInHand, trespass }
export function cause(tom) {
  const why = [];
  if (tom.night && tom.carrying) why.push('carrying at night');
  if (tom.running) why.push('running');
  if (tom.bloodied) why.push('bloodied');
  if (tom.weaponInHand) why.push('a weapon in his hand');
  if (tom.trespass) why.push('where he should not be');
  return { cause: why.length > 0, why };
}
// ER-POL-02: he may challenge only after he has been heard or seen for 3 s, and he calls out before he acts.
export function mayChallenge(heardForRealSeconds, calledOut) {
  return { callOut: heardForRealSeconds >= BT.noChallengeBeforeRealSeconds, act: !!calledOut && heardForRealSeconds >= BT.noChallengeBeforeRealSeconds };
}
// A search finds exactly what is under the coat and in the hand, and he keeps it (ER-POCKET-01's other half).
export function search(carried, inHand) {
  const found = [...(carried || [])];
  if (inHand) found.push(inHand);
  return { found, kept: found.slice(), left: [] };
}
// The third answer, a word (A13). officer: 'pc' | 'pashby' | ...; hasCause; offeredNote
export function word(officer, hasCause, offeredNote, pashbyUsed) {
  if (offeredNote) {
    if (officer === 'pashby' && pashbyUsed < TUNE.bought.pashbyLooksAwayTimesANight) return { ends: 'looks away', crime: false };
    if (officer === 'pashby') return { ends: 'search', crime: false };
    return { ends: 'arrest', crime: true }; // offered to an honest one, it is a crime he saw
  }
  return hasCause ? { ends: 'search', crime: false } : { ends: 'talked round', crime: false };
}
function rng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
// One seeded chase, stepped at a tenth of a second. The seed picks how often a corner breaks the line of sight and
// for how long. It always ends, caught or lost, within 90 real seconds (ER-POL-04, ER-PURSUE-01); a runner unseen
// for 7 s or 70 m clear has lost him.
export function chase(seed, runnerMps, startGapMetres) {
  const r = rng(seed), dt = 0.1;
  let gap = startGapMetres, t = 0, unseen = 0, hidden = 0;
  const cornerEvery = 4 + r() * 10, cornerHides = 1 + r() * 8;
  let nextCorner = cornerEvery;
  while (t < BT.chaseEndsWithinRealSeconds) {
    t += dt;
    const stumble = r() < 0.01 ? 0.5 : 1;
    gap += (runnerMps * stumble - BT.chaseMetresPerSecond * (hidden > 0 ? 0.6 : 1)) * dt;
    if (t >= nextCorner && runnerMps > 0) {
      hidden = cornerHides;
      nextCorner = t + cornerEvery;
    }
    if (hidden > 0) {
      hidden -= dt;
      unseen += dt;
    } else unseen = 0;
    if (gap <= BT.catchesWithinMetres) return { end: 'caught', how: 'a hand on his collar', seconds: Math.round(t * 10) / 10 };
    if (unseen >= BT.losesHimAfterRealSecondsUnseen) return { end: 'lost', how: 'unseen', seconds: Math.round(t * 10) / 10 };
    if (gap >= BT.losesHimBeyondMetres) return { end: 'lost', how: 'distance', seconds: Math.round(t * 10) / 10 };
  }
  return { end: 'lost', how: 'gave up', seconds: BT.chaseEndsWithinRealSeconds }; // never past 90 s
}
// many seeded chases: every one ends inside the limit
export function chases(n, runnerMps) {
  let caught = 0, lost = 0, longest = 0;
  for (let i = 1; i <= n; i++) {
    const c = chase(1990 + i, runnerMps, 8 + (i % 7));
    if (c.end === 'caught') caught++;
    else lost++;
    longest = Math.max(longest, c.seconds);
  }
  return { caught, lost, longest, allEndInTime: longest <= BT.chaseEndsWithinRealSeconds };
}
export const PIECE = { name: 'police_beat', fns: { cause, mayChallenge, search, word, chase, chases } };
