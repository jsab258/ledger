// Rule piece: hiding and keeping out of sight (DESIGN 2 "In the moment"; DESIGN-ADDENDUM A1, A10, A33).
// Pure: plain data in, plain data out. The numbers are the tuning table's (game/tune/foot.js hiding), handed in
// or defaulted here so Unreal can port the piece with the same cases.
import { TUNE } from '../tune/foot.js';
const H = TUNE.hiding;

// The light Tom counts at. where: { light (0..1, the place's own light), doorway (bool), night (bool) },
// he: { stillSeconds, torchOn }. Standing still in a doorway counts at the doorway's light; moving through it at
// the street's; a lit torch makes him count as lit at lamp value.
export function lightForTom(where, he, h = H) {
  let L = where.light;
  if (where.doorway && he.stillSeconds >= h.stillAfterRealSeconds)
    L = where.night ? Math.min(L, h.doorwayLight) : L * h.stillInDoorwayByDayLightTimes;
  if (he.torchOn) L = Math.max(L, h.torchLight);
  return Math.max(0, Math.min(1, L));
}
// The rung a watcher can reach: 0 nothing, 1 a shape, 2 a mark, 3 a face, 4 recognition.
// w: { metres, light (what lightForTom gave), lineOfSight, facing, knowsHim, backTurned, markOnHim, stillInDoorway }.
export function rungCaught(w, h = H) {
  if (!w.lineOfSight || !w.facing) return 0;
  const reach = (m) => m * Math.max(w.light, 0); // light scales every distance
  let rung = 0;
  if (w.metres <= reach(h.shapeAtMetres)) rung = 1;
  if (w.markOnHim && w.metres <= reach(h.markAtMetres)) rung = 2;
  if (!w.backTurned && w.metres <= reach(h.faceAtMetres)) rung = 3;
  if (!w.backTurned && w.knowsHim && w.metres <= reach(h.knownAtMetres)) rung = 4;
  // a still figure in a doorway is a shape at most beyond 8 m
  if (w.stillInDoorway && w.metres > h.stillInDoorwayShapeOnlyBeyondMetres) rung = Math.min(rung, 1);
  return rung;
}
// How long a glance at him takes: twice as long among three or more people within 2 m.
export function glanceSeconds(peopleWithinTwoMetres, h = H) {
  return h.glanceRealSeconds * (peopleWithinTwoMetres >= h.amongPeopleAtLeast ? h.glanceAmongPeopleTimes : 1);
}
// His footstep's reach: walking slowly halves it.
export function footstepReach(baseMetres, slow, share = 0.5) {
  return slow ? baseMetres * share : baseMetres;
}
// A10: a seated or smoking man who belongs is caught as a shape like anyone, and never more than a walking one.
export function rungCaughtStopped(w, stoppedAs, h = H) {
  const walking = rungCaught(w, h);
  return stoppedAs ? Math.min(walking, rungCaught(Object.assign({}, w, { stillInDoorway: false }), h)) : walking;
}
// Does a man standing about draw a second look? Only at night, with no reason (not sitting, leaning or smoking).
export function drawsSecondLook(night, stoppedAs, stoodSeconds, afterSeconds) {
  return !!night && !stoppedAs && stoodSeconds >= afterSeconds;
}
export const PIECE = { name: 'hide_rules', fns: { lightForTom, rungCaught, glanceSeconds, footstepReach, rungCaughtStopped, drawsSecondLook } };
