// Rule piece: the four stages of police interest, each with its sign (DESIGN section 8, ER-POL-05). Pure.
// 0 nothing; 1 asking round (her name in the street's talk); 2 investigating (an officer at his door);
// 3 a manhunt (a car on the street and his description). No stage is skipped unseen.
import { TUNE } from '../tune/law.js';
const S = TUNE.stages;
// what the facts ask for. f: { ellisAsked, statements, worstClass ('window'...), ranFromPolice, body, hunted }
export function wanted(f) {
  if (f.hunted || (f.worstClass === 'killing' && f.statements > 0) || (f.ranFromPolice && (f.worstClass === 'wounding' || f.worstClass === 'robbery'))) return 3;
  if (f.statements > 0 || f.body) return 2;
  if (f.ellisAsked) return 1;
  return 0;
}
// One step at a time. st: { stage, signs: [{ stage, t, shown }] }; returns the stage to enter now, or the same stage.
export function advance(st, want, now) {
  if (want <= st.stage) return st.stage;
  const last = st.signs.filter((s) => s.stage === st.stage).pop();
  if (st.stage > 0 && (!last || !last.shown)) return st.stage; // its sign has not been shown yet
  if (st.stage > 0 && now - last.t < S.nextStageNotBeforeGameMinutes) return st.stage;
  return st.stage + 1;
}
// A manhunt's arrest cannot land until its sign has been up a game hour. Other arrests need a statement (law_custody).
export function manhuntMayArrest(st, now) {
  const sign = st.signs.filter((s) => s.stage === 3 && s.shown).pop();
  return !!sign && st.stage === 3 && now - sign.t >= S.manhuntSignBeforeArrestGameMinutes;
}
// Ellis comes for talk from day 4 once three people of his day world pass talk of his nights; for a body; for a
// detective's crime once reported.
export function ellisComes(f) {
  if (f.body) return 'a body';
  if (f.reportedClass === 'wounding' || f.reportedClass === 'robbery' || f.reportedClass === 'killing') return 'a crime reported';
  if (f.dayIndex >= S.ellisTalkFromDayIndex && f.dayPeopleTalking >= S.ellisTalkNeedsDayPeople) return 'the talk';
  return null;
}
// the case she builds, read at the ending
export function caseStrength(c) {
  return (c.statements || 0) * S.caseStrengthPerStatement + (c.charges || 0) * S.caseStrengthPerCharge + (c.officeFinds || 0) * S.caseStrengthPerOfficeFind;
}
export const PIECE = { name: 'law_stages', fns: { wanted, advance, manhuntMayArrest, ellisComes, caseStrength } };
