// Rule piece: ground rules and trespass (DESIGN 4 break-ins; DESIGN-ADDENDUM A10).
// Pure. Every place carries a label: public, hours (open by hours, private out of them), private, forbidden.
// Private: the owner or a neighbour warns, warns again, then calls or acts within half a minute. Forbidden skips
// the first warning. The warnings reset when he leaves; the sighting is kept for good (the caller's business).
import { TUNE } from '../tune/foot.js';
const GR = TUNE.ground;

// What the ground is to him now: 'free' | 'private' | 'forbidden'.
export function standing(place, hour) {
  if (!place || place.label === 'public') return 'free';
  if (place.label === 'forbidden') return 'forbidden';
  if (place.label === 'private') return 'private';
  if (place.label === 'hours') {
    const a = place.openFromHour == null ? 0 : place.openFromHour,
      b = place.openUntilHour == null ? 24 : place.openUntilHour,
      open = a <= b ? hour >= a && hour < b : hour >= a || hour < b;
    return open ? 'free' : 'private';
  }
  return 'free';
}
// One step of the warnings. s: { stage (1 warned, 2 warned again, 3 acted), since (seconds since the first
// warning) } or null. i: { ground ('free'|'private'|'forbidden'), watched (somebody who minds can see or hear him),
// dt }. Gives { s, say: null | 'warn' | 'warnAgain' | 'act' }.
export function trespassStep(s, i, g = GR) {
  if (i.ground === 'free') return { s: null, say: null };
  if (!s) {
    if (!i.watched) return { s: null, say: null };
    return i.ground === 'forbidden'
      ? { s: { stage: 2, since: g.warnAgainAfterRealSeconds }, say: 'warnAgain' }
      : { s: { stage: 1, since: 0 }, say: 'warn' };
  }
  const since = s.since + i.dt;
  if (s.stage === 1 && since >= g.warnAgainAfterRealSeconds) return { s: { stage: 2, since }, say: 'warnAgain' };
  if (s.stage === 2 && since >= g.actsAfterRealSeconds) return { s: { stage: 3, since }, say: 'act' };
  return { s: { stage: s.stage, since }, say: null };
}
export const PIECE = { name: 'foot_ground', fns: { standing, trespassStep } };
