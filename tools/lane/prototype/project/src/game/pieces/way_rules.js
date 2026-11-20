// Rule piece: finding the way without markers (DESIGN section 4 "Guidance", DESIGN-ADDENDUM A9).
// Pure: plain data in, plain data out. Unreal ports this and passes test/cases/way_rules.json.
//
// place:  { id, name, address, landmark, label, known: 'all' | 'locals' | [personIds], owner?, x, z }
// person: { id, local: bool, keeper: bool, police: bool, haunts: [placeIds] }

// Does this person know the way to this place? Shopkeepers and the constable always do (A9).
function knows(person, place) {
  if (!person || !place) return false;
  if (person.keeper || person.police) return true;
  if (place.owner === person.id) return true;
  if ((person.haunts || []).includes(place.id)) return true;
  if (place.known === 'all') return true;
  if (place.known === 'locals') return !!person.local;
  return Array.isArray(place.known) && place.known.includes(person.id);
}
const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
// What is said when asked. Only an address and a landmark, never a distance in numbers or a compass point.
function answer(person, place) {
  if (!knows(person, place)) return { knows: false, text: 'No idea. Try the caff.' };
  return { knows: true, text: cap(place.name) + '? ' + cap(place.address) + '. ' + cap(place.landmark) + '.' };
}
// Tom's own line when he is lost: the landmark again, once.
function ownLine(place) {
  return cap(place.name) + ': ' + place.landmark + '.';
}
// The lost rule, one step. st: { goal, best, since, nudged, offered } (best: nearest he has been, since: real
// seconds without progress). Returns the new state and what fires: null | 'nudge' | 'offer' | 'arrived'.
// t: { nudgeAfter, offerAfter, progress, arrived }
function lostStep(st, goalId, dist, dt, someoneNear, t) {
  if (!goalId) return { st: { goal: null, best: 0, since: 0, nudged: false, offered: false }, fires: null };
  if (!st || st.goal !== goalId) st = { goal: goalId, best: dist, since: 0, nudged: false, offered: false };
  else st = Object.assign({}, st);
  if (dist <= t.arrived) return { st: Object.assign(st, { since: 0, best: dist }), fires: 'arrived' };
  if (dist < st.best - t.progress) {
    st.best = dist;
    st.since = 0;
    return { st, fires: null };
  }
  st.since += dt;
  if (!st.nudged && st.since >= t.nudgeAfter) {
    st.nudged = true;
    return { st, fires: 'nudge' };
  }
  if (st.nudged && !st.offered && st.since >= t.offerAfter && someoneNear) {
    st.offered = true;
    return { st, fires: 'offer' };
  }
  return { st, fires: null };
}
// ER-WAY-02: what a place lacks, as a list of words (empty when it has an address, a landmark and a label).
function lacks(place) {
  const out = [];
  if (!place.address) out.push('address');
  if (!place.landmark) out.push('landmark');
  if (!['public', 'hours', 'private', 'forbidden'].includes(place.label)) out.push('label');
  if (place.label === 'hours' && !(place.openUntilHour > place.openFromHour)) out.push('hours');
  return out;
}
// A10 ground rules: may he be here now without a warning? h: hour of the day.
function ground(place, h) {
  if (place.label === 'public') return 'free';
  if (place.label === 'hours') return h >= place.openFromHour && h < place.openUntilHour ? 'free' : 'private';
  return place.label;
}

export const PIECE = { name: 'way_rules', fns: { knows, answer, ownLine, lostStep, lacks, ground } };
