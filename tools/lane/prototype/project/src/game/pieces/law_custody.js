// Rule piece: what an arrest costs (DESIGN section 8, addendum A13). Hours, never the game. Pure.
import { TUNE } from '../tune/law.js';
const C = TUNE.custody;
// The class of a deed for the cells: 'window' (damage, a threat, a shove), 'wounding', 'robbery', 'killing'.
// kind: { crime 0..4, lawClass?, kills? } as the kinds table gives it.
export function deedClass(kind) {
  if (!kind) return 'window';
  if (kind.lawClass) return kind.lawClass;
  if (kind.kills) return 'killing';
  if (kind.crime >= 4) return 'killing';
  if (kind.crime >= 3) return 'robbery';
  if (kind.crime >= 2) return 'wounding';
  return 'window';
}
// hours in the cells and how it ends. ownedUp only counts for the least class.
export function custody(cls, ownedUp, ran) {
  let hours = { window: C.windowGameHours, wounding: C.woundingGameHours, robbery: C.robberyGameHours, killing: C.killingGameHours }[cls];
  let outcome = cls === 'window' ? 'released' : 'charged';
  if (cls === 'window' && ownedUp) {
    hours = C.windowOwnedUpGameHours;
    outcome = 'cautioned';
  }
  if (ran) hours += C.ranAddsGameHours;
  return { hours, outcome, bail: cls !== 'window', solicitorPence: 0, coatKept: true };
}
// ER-POL-01: an arrest needs a signed statement from someone who knew it was him, or an officer who saw it.
// ER-POL-03: never twice for one deed.
export function mayArrest(deed) {
  if (deed.takenAlready) return { ok: false, why: 'already taken for this deed' };
  if (deed.officerSaw) return { ok: true, why: 'an officer saw it' };
  const named = (deed.statements || []).filter((s) => s.knewItWasHim);
  if (named.length) return { ok: true, why: 'a statement from ' + named[0].by };
  return { ok: false, why: 'talk alone brings questions, never an arrest' };
}
export const PIECE = { name: 'law_custody', fns: { deedClass, custody, mayArrest } };
