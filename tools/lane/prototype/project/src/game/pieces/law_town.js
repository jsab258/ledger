// Rule piece: a street on edge (A37), finding an unseen deed (A38), bodies and the missing (DESIGN section 7),
// the dial's police (DESIGN section 7), bought men (A13). Pure.
import { TUNE } from '../tune/law.js';
const E = TUNE.edge, A = TUNE.armed, M = TUNE.missing, B = TUNE.bought;
// seenDeedTimes: game minutes of the seen deeds on one street. On edge while three fall inside two game days and the
// last is not older than the easing time.
export function onEdge(seenDeedTimes, now) {
  const ts = seenDeedTimes.filter((t) => t <= now).sort((a, b) => a - b);
  let edge = false, since = null;
  for (let i = E.seenDeedsNeeded - 1; i < ts.length; i++) {
    if (ts[i] - ts[i - E.seenDeedsNeeded + 1] <= E.withinGameMinutes && now - ts[i] <= E.easesGameMinutesAfterTheLast) {
      edge = true;
      since = ts[i];
    }
  }
  return { edge, since, setsOffTimes: edge ? E.setsOffSoonerTimes : 1, constableTimes: edge ? E.constableVisitsTimes : 1 };
}
// deed: { trace: bool, hidden: bool, sunk: bool, t }; passes: [{ who, t }] the routines that pass its spot.
// The first passer after the deed finds it and holds only the aftermath. Nothing is found by chance.
export function finder(deed, passes) {
  if (!deed.trace || deed.hidden || deed.sunk) return null;
  const p = passes.filter((x) => x.t >= deed.t).sort((a, b) => a.t - b.t || (a.who < b.who ? -1 : 1))[0];
  return p ? { who: p.who, t: p.t, holds: ['aftermath'] } : null;
}
// A body never cools; a man who stops keeping his routine becomes the town's question before anyone finds him.
export function missingAsked(man, now) {
  if (!man.goneSince || man.found) return { asked: false, cools: false, times: 0 };
  const hours = (now - man.goneSince) / 60;
  return { asked: hours >= M.noticedAfterGameHours, cools: false, times: hours < M.noticedAfterGameHours ? 0 : 1 + Math.floor((hours - M.noticedAfterGameHours) / M.askedAgainEveryGameHours) };
}
// The dial's police. dial 0 to 3; call: 'gun' | 'other'.
export function response(dial, call) {
  if (dial >= 3) return { armed: call === 'gun', armedCars: true, stopAndSearch: true, arrivesGameMinutes: call === 'gun' ? A.warCarArrivesGameMinutes : null, armedOfficersAtMost: A.warArmedOfficersAtMost };
  if (dial >= 2 && call === 'gun') return { armed: true, armedCars: false, stopAndSearch: false, arrivesGameMinutes: A.gunCallArrivesGameMinutes, armedOfficersAtMost: 2 };
  return { armed: false, armedCars: false, stopAndSearch: false, arrivesGameMinutes: null, armedOfficersAtMost: 0 };
}
// A bought officer does only what his limit says (ER-BOUGHT-01). who: 'pashby' | 'thwaite' | anyone else (honest).
// ask: 'car' (look away from a car) | 'statement' (lose a statement) | anything else. used: times already used.
export function boughtDoes(who, paid, ask, used) {
  if (who === 'pashby') return { does: !!paid && ask === 'car' && used < B.pashbyLooksAwayTimesANight, crime: false };
  if (who === 'thwaite') return { does: !!paid && ask === 'statement' && used < B.thwaiteLosesStatements, crime: false };
  return { does: false, crime: true }; // a note offered to an honest officer is a crime he saw
}
export const PIECE = { name: 'law_town', fns: { onEdge, finder, missingAsked, response, boughtDoes } };
