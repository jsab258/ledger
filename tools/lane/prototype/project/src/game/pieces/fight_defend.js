// Rule piece: reading and answering a blow (DESIGN 7 Feel; DESIGN-ADDENDUM A29). Pure.
// What one incoming blow does to Tom, by what he was doing when it landed, and whether it opens the counter.
import { TUNE } from '../tune/fightx.js';
const S = TUNE.sim,
  D = TUNE.defend;

// blow: { heavy, weapon (the other man swings a weapon), hurts (its full hurt) }
// tom: { doing: 'idle' | 'guard' | 'slip' | 'open' (just missed) | 'windup', facing (bool) }
// Gives { hurt, staggered, counterOpens }.
export function blowLands(blow, tom, s = S, d = D) {
  if (tom.doing === 'slip') return { hurt: 0, staggered: false, counterOpens: true };
  if (tom.doing === 'guard' && tom.facing !== false) {
    if (blow.weapon) return { hurt: blow.hurts * d.weaponBreaksGuardShare, staggered: true, counterOpens: false };
    return { hurt: blow.hurts * s.blockLetsThrough, staggered: !!blow.heavy, counterOpens: !blow.heavy };
  }
  return { hurt: blow.hurts * (tom.doing === 'open' ? s.openTimes : 1), staggered: true, counterOpens: false };
}
// A counter only lands after a slip or a block: a jab inside the window is a heavy blow at a jab's speed.
export function jabIs(secondsSinceCounterOpened, d = D) {
  return secondsSinceCounterOpened != null && secondsSinceCounterOpened >= 0 && secondsSinceCounterOpened <= d.counterWindowRealSeconds ? 'counter' : 'jab';
}
// How much slower a blow starts when he is out of breath (stamina 0..1).
export function windUpTimes(stamina, d = D) {
  return stamina >= d.breathSlowsFromStamina ? 1 : 1 + (d.breathSlowsWindUpByShareAtEmpty * (d.breathSlowsFromStamina - stamina)) / d.breathSlowsFromStamina;
}
// A fair one-on-one, in exchanges. policy: 'reader' (guards or slips on the tell, counters, jabs when it is safe),
// 'masher' (throws heavy blows without stopping). Seeded. Gives { won, exchanges }.
export function duel(o, s = S, d = D) {
  let seed = o.seed >>> 0;
  const rnd = () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  let tom = 0,
    foe = 0,
    stam = 1,
    n = 0;
  while (tom < 1 && foe < 1 && n < 400) {
    n++;
    // the other man's blow of this exchange, readable before it lands
    const heavy = rnd() < s.foeHeavyChance,
      blow = { heavy, weapon: false, hurts: heavy ? s.foeHeavyHurts : s.foeLightHurts };
    if (o.policy === 'reader') {
      // he reads it: slips the heavy ones, guards the jabs, and answers inside the window
      const r = blowLands(blow, { doing: heavy ? 'slip' : 'guard', facing: true }, s, d);
      tom += r.hurt;
      if (r.counterOpens && stam >= s.tooTiredBelow) {
        foe += s.heavyHurts; // the counter is never stopped by his guard
        stam -= s.lightCost;
      } else if (stam > 0.5 && rnd() > s.foeGuardStopsLight) {
        foe += s.lightHurts;
        stam -= s.lightCost;
      }
      stam = Math.min(1, stam + s.staminaBackPerSecond * 1.6);
    } else {
      // he mashes: every exchange a heavy blow if he has the breath, and he is open when the answer comes
      let open = 'windup';
      if (stam >= s.tooTiredBelow) {
        stam -= s.heavyCost;
        if (rnd() > s.foeGuardStopsLight * 1.5) foe += s.heavyHurts * (1 / windUpTimes(stam, d));
        else open = 'open';
      } else open = 'open';
      tom += blowLands(blow, { doing: open }, s, d).hurt;
      stam = Math.min(1, stam + s.staminaBackPerSecond * 0.8);
    }
  }
  return { won: foe >= 1 && tom < 1, exchanges: n };
}
export function duels(o, s = S, d = D) {
  let won = 0;
  for (let i = 0; i < o.n; i++) if (duel({ seed: o.seed + i * 104729, policy: o.policy }, s, d).won) won++;
  return { won, of: o.n };
}
export const PIECE = { name: 'fight_defend', fns: { blowLands, jabIs, windUpTimes, duel, duels } };
