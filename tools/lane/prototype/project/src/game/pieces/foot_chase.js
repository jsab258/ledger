// Rule piece: a chase on foot, either way round (DESIGN 8 the beat; DESIGN-ADDENDUM A3).
// Pure. A chase is stepped in fixed steps; it ends caught (the hand on the collar within 1 m from behind), or lost
// (the one fleeing unseen for 7 s, or 70 m clear), and always within 90 real seconds.
import { TUNE } from '../tune/foot.js';
const C = TUNE.chase;

// One step. s: { t, gap (metres between them), unseen (seconds the runner has been out of sight) }.
// i: { dt, runnerSpeed, pursuerSpeed, seen (bool: the pursuer has a line of sight), behind (bool) }.
export function chaseStep(s, i, c = C) {
  const gap = Math.max(0, s.gap + (i.runnerSpeed - i.pursuerSpeed) * i.dt),
    unseen = i.seen ? 0 : s.unseen + i.dt,
    t = s.t + i.dt;
  let end = null;
  if (gap <= c.collarWithinMetres && i.behind !== false) end = 'caught';
  else if (unseen >= c.lostUnseenRealSeconds || gap >= c.lostBeyondMetres) end = 'lost';
  else if (t >= c.endsWithinRealSeconds) end = 'lost'; // the runner is winded or gone to ground: it always ends
  return { t, gap, unseen, end };
}
// A whole seeded chase. The runner runs at 95% of Tom's run; a pursuer on a direct line keeps his pace and cuts
// each corner; a lagging one loses ground and sight at every corner. line: 'direct' | 'slow'.
export function chase(o, c = C) {
  let seed = o.seed >>> 0;
  const rnd = () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const run = o.tomRun || c.tomRunsMetresPerSecond,
    runner = run * c.runnerSpeedShareOfTomsRun,
    pursuer = o.line === 'direct' ? run : run * (o.slowShare || 0.8);
  let s = { t: 0, gap: o.startGap, unseen: 0, end: null },
    nextCorner = 4 + rnd() * 6;
  const dt = 0.1;
  let hidden = 0;
  while (!s.end) {
    if (s.t >= nextCorner) {
      nextCorner += 5 + rnd() * 7;
      hidden = o.line === 'direct' ? 0.6 + rnd() * 0.8 : 1.5 + rnd() * 2.5 + s.gap / 8;
      s.gap = Math.max(0, s.gap + (o.line === 'direct' ? -(1 + rnd() * 2) : 1.5 + rnd() * 2.5));
    }
    const seen = hidden <= 0 && s.gap < 45;
    hidden -= dt;
    s = chaseStep(s, { dt, runnerSpeed: runner, pursuerSpeed: pursuer, seen, behind: true }, c);
  }
  return { end: s.end, seconds: Math.round(s.t * 10) / 10, gap: Math.round(s.gap * 10) / 10 };
}
// How many of n seeded chases end each way, and the longest.
export function chases(o, c = C) {
  const out = { caught: 0, lost: 0, longestSeconds: 0 };
  for (let i = 0; i < o.n; i++) {
    const r = chase({ seed: o.seed + i * 7919, startGap: o.startGap, line: o.line, slowShare: o.slowShare }, c);
    out[r.end]++;
    out.longestSeconds = Math.max(out.longestSeconds, r.seconds);
  }
  return out;
}
export const PIECE = { name: 'foot_chase', fns: { chaseStep, chase, chases } };
