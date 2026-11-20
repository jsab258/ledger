// RULE PIECE: talk cools by kind, memory does not (DESIGN 2; part 2.4.2). Pure. Unreal ports this and passes
// test/cases/cooling.json. It replaces the single half-life for how hot a story is in talk; nothing is ever removed
// from anybody's memory, and a killing never cools.
//
// heat 0 to 1: how ready somebody is to tell it. kind: { crime 0..4, val -1..1, forever }.
export function halfLifeGameDays(kind, T) {
  if (kind.forever) return null; // never cools
  if (kind.val > 0) return T.coolsHalfInGameDaysIfDecent;
  return T.coolsHalfInGameDaysByCrimeLevel[Math.max(0, Math.min(4, kind.crime | 0))];
}
export function heatAfter(heat, kind, gameMinutes, T, floor = 0) {
  const half = halfLifeGameDays(kind, T);
  if (half === null) return heat;
  return Math.max(floor, heat * Math.pow(0.5, gameMinutes / (half * 1440)));
}
// Whether a story is still talk (worth telling): at or above the line the gossip rule uses.
export function stillTalk(heat, line) {
  return heat >= line;
}
export const PIECE = { name: 'cooling', fns: { halfLifeGameDays, heatAfter, stillTalk } };
