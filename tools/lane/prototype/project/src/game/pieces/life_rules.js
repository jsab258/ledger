// Rule piece: small rules of the town's days. Pure.
//
// A39 calling on people: only where and when the person's routine allows; a second call inside the gap is cooler.
function canCall(routinePlace, homePlaces, hour, t) {
  if (!homePlaces.includes(routinePlace)) return { ok: false, why: 'not in' };
  if (hour < t.callsFromHour || hour >= t.callsUntilHour) return { ok: false, why: 'not at this hour' };
  return { ok: true, why: null };
}
function callWarmth(lastCallMinute, nowMinute, t) {
  if (lastCallMinute == null) return 'warm';
  return nowMinute - lastCallMinute < t.coolerInsideGameMinutes ? 'cool' : 'warm';
}
// The friendship that can hold (3.2.5): built from visits and the honesty in them. No score is shown; the state is
// counted in words. visits: [{ honest: bool, cool: bool }]
function friendship(visits, broken, t) {
  const good = visits.filter((v) => v.honest && !v.cool).length, lies = visits.filter((v) => !v.honest).length;
  if (broken || lies >= t.liesThatEndIt) return { holds: false, word: 'over' };
  if (good >= t.visitsToHold) return { holds: true, word: 'holds' };
  return { holds: false, word: good ? 'warming' : 'slight' };
}
// 2.19 lasting marks on the town: each kind stays its set time. marks: [{ id, kind, place, t }]. Never wiped by
// save or skipped time: only the clock ends one, or mending.
function marksAlive(marks, nowMinute, lasts) {
  return marks.filter((m) => !m.mended && nowMinute - m.t < (lasts[m.kind] || 0));
}
// ER-FIRST-03 teaching: a hint shows only the first time, on first need or hesitation, never two within 12 s.
// st: { shown: { id: true }, lastAt: real seconds }. Returns { show, st }.
function hint(st, id, nowSeconds, hintsOn, t) {
  if (!hintsOn || st.shown[id]) return { show: false, st };
  if (st.lastAt != null && nowSeconds - st.lastAt < t.hintsApartRealSeconds) return { show: false, st };
  return { show: true, st: { shown: Object.assign({}, st.shown, { [id]: true }), lastAt: nowSeconds } };
}
// ER-CORE-07 always something to do: of the things on offer, the nearest within reach in 30 real seconds.
// things: [{ kind: 'fare' | 'debt' | 'word' | 'happening' | 'story', id, metres }]
function somethingToDo(things, inCab, t) {
  const reach = (inCab ? t.cabMetresPerSecond : t.walkMetresPerSecond) * t.withinRealSeconds;
  const near = things.filter((x) => x.metres <= reach).sort((a, b) => a.metres - b.metres);
  return { ok: near.length > 0, first: near[0] || null, reachMetres: reach };
}
// 2.12.4 greetings by regard: which kind of greeting a person gives. Afraid, angry, likes him, his appearance,
// neutral; and how formal by the rung he has reached (heard, never shown as a number).
function greetingKind(p, t) {
  if (!p.knowsHim) return p.marked ? 'appearance' : 'neutral';
  if (p.fear >= t.afraidFromFear) return 'afraid';
  if (p.regard <= t.angryBelowRegard) return 'angry';
  if (p.marked) return 'appearance';
  if (p.regard >= t.likesFromRegard) return 'likes';
  return 'neutral';
}
function greetingRung(rung) {
  return rung >= 4 ? 'port' : rung >= 3 ? 'firm' : rung >= 2 ? 'owner' : 'nephew';
}
export const PIECE = { name: 'life_rules', fns: { canCall, callWarmth, friendship, marksAlive, hint, somethingToDo, greetingKind, greetingRung } };
