// Rule piece: street happenings and where they are placed (DESIGN-ADDENDUM A18). Authored, never rolled: a
// happening is placed by a named state and the hour. ER-HAPPEN-01. Pure.
//
// spec: { id, street, fromHour, untilHour, needs: [factName], notIf: [factName], weather: 'dry' | 'wet' | undefined }
// state: { hour, day, wet: bool, facts: { name: true }, log: [{ id, street, t (real seconds played), day }] }
// t: { quietRealSeconds (none twice in 30 min), sameStreetDays (none twice in a week on one street), gapRealSeconds }
function whyNot(spec, st, now, t) {
  if (st.hour < spec.fromHour || st.hour >= spec.untilHour) return 'the hour';
  if (spec.weather === 'dry' && st.wet) return 'the weather';
  if (spec.weather === 'wet' && !st.wet) return 'the weather';
  for (const n of spec.needs || []) if (!st.facts[n]) return 'needs ' + n;
  for (const n of spec.notIf || []) if (st.facts[n]) return 'not while ' + n;
  const last = st.log.length ? st.log[st.log.length - 1] : null;
  if (last && now - last.t < t.gapRealSeconds) return 'one just happened';
  for (const l of st.log) {
    if (l.id === spec.id && now - l.t < t.quietRealSeconds) return 'the same one inside thirty minutes';
    if (l.id === spec.id && l.street === spec.street && st.day - l.day < t.sameStreetDays) return 'the same one on this street this week';
  }
  return null;
}
// The one to place now: the first in the written order whose state holds, starting from the day's place in the
// list so the week varies without dice. Returns { id, because } or null.
function place(specs, st, now, t) {
  const n = specs.length;
  for (let i = 0; i < n; i++) {
    const s = specs[(i + st.day) % n];
    if (!whyNot(s, st, now, t)) return { id: s.id, because: (s.needs || []).concat(['hour ' + Math.floor(st.hour)]).join(', ') };
  }
  return null;
}
// A stranger Tom helped turns up days later with a small favour, carried by the same memory as any deed.
function favourDue(helped, day, t) {
  return helped.filter((h) => !h.returned && day - h.day >= t.favourAfterDays && day - h.day <= t.favourWithinDays).map((h) => h.id);
}
export const PIECE = { name: 'life_happen', fns: { whyNot, place, favourDue } };
