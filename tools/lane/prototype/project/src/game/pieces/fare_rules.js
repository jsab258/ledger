// LEDGER rule piece: fares. Pure: plain data in, plain data out. Ported to Unreal with the same cases
// (test/cases/fare_rules.json). `t` is game/tune/fares.js; `r` is rules.js fares (flag fall and distance).

// What a fare pays: 80p plus distance (DESIGN 5). No meter: the price is what Pauline quoted.
const pay = (r, metres) => Math.round((r.flagFallPence + metres * r.penceAddedPerMetre) / r.roundedToPence) * r.roundedToPence;

// Which fare Pauline calls next. Few and chosen (his words, 19 Nov; ER-JOB-06, ER-CORE-08):
//   never a fare already driven or handed on this week; never the same wrinkle twice running; from rung 2 only fares
//   with a wrinkle or a face (the drivers take the rest); so many a day and no more; a fare only in its own hours and
//   on its own state. The list's order is the author's order: the first that fits is called.
// fares: [{ id, wrinkle|null, fromHour, untilHour, fromDay?, untilDay?, needs?: [flag], not?: [flag], rungFrom?, rungUntil? }]
// s: { day, hour, rung, doneThisWeek: [id], lastWrinkle, offeredToday, eveningOffered, flags: {} }
function next(t, fares, s) {
  const cap = s.rung >= 2 ? t.offersADayFromRungTwo : t.offersADayAtRungOne;
  if (s.offeredToday >= cap) return null;
  if (s.hour >= t.eveningFromHour && s.eveningOffered >= t.eveningOffersAtMost) return null;
  for (const f of fares) {
    if (s.doneThisWeek.includes(f.id)) continue;
    const inHours = f.fromHour <= f.untilHour ? s.hour >= f.fromHour && s.hour < f.untilHour : s.hour >= f.fromHour || s.hour < f.untilHour;
    if (!inHours) continue;
    if (f.fromDay != null && s.day < f.fromDay) continue;
    if (f.untilDay != null && s.day > f.untilDay) continue;
    if (f.rungFrom != null && s.rung < f.rungFrom) continue;
    if (f.rungUntil != null && s.rung > f.rungUntil) continue;
    if (s.rung >= 2 && !f.wrinkle) continue;
    if (f.wrinkle && f.wrinkle === s.lastWrinkle) continue;
    if ((f.needs || []).some((k) => !s.flags[k])) continue;
    if ((f.not || []).some((k) => s.flags[k])) continue;
    return f.id;
  }
  return null;
}

// The way, from the three roads of the Hook. roads: { id: { axis: 'x'|'z', at, from, to, name } } (axis is the one the
// road runs along). A place is put on its nearest road; the way goes by the junctions. Each leg: the road, the way he
// heads on it, where it ends, and the turn he makes there. The words Pauline says are made from the legs and nothing
// else, so a driver who follows the words arrives (ER-DRIVE-09).
function onRoad(roads, p) {
  let best = null;
  for (const id in roads) {
    const R = roads[id],
      along = R.axis === 'x' ? p.x : p.z,
      off = Math.abs((R.axis === 'x' ? p.z : p.x) - R.at),
      over = along < R.from ? R.from - along : along > R.to ? along - R.to : 0,
      d = off + over;
    if (!best || d < best.d) best = { id, d, along: Math.min(R.to, Math.max(R.from, along)) };
  }
  return best;
}
const pointOn = (R, along) => (R.axis === 'x' ? { x: along, z: R.at } : { x: R.at, z: along });
function cross(roads, a, b) {
  const A = roads[a], B = roads[b];
  if (A.axis === B.axis) return null;
  const alongA = B.at, alongB = A.at;
  if (alongA < A.from - 6 || alongA > A.to + 6 || alongB < B.from - 6 || alongB > B.to + 6) return null;
  return { alongA, alongB };
}
const heading = (R, from, to) => (R.axis === 'x' ? (to > from ? 'east' : 'west') : to > from ? 'south' : 'north');
// +z is south and +x is east, seen from above with north up: turning from north to east is a right turn
const ORDER = ['north', 'east', 'south', 'west'];
const turn = (h0, h1) => ((ORDER.indexOf(h1) - ORDER.indexOf(h0) + 4) % 4 === 1 ? 'right' : 'left');
function legs(roads, from, to) {
  const a = onRoad(roads, from), b = onRoad(roads, to);
  const chain = [a.id];
  if (a.id !== b.id) {
    if (cross(roads, a.id, b.id)) chain.push(b.id);
    else {
      const via = Object.keys(roads).find((m) => m !== a.id && m !== b.id && cross(roads, a.id, m) && cross(roads, m, b.id));
      if (!via) return [];
      chain.push(via, b.id);
    }
  }
  const out = [];
  let at = a.along;
  for (let i = 0; i < chain.length; i++) {
    const R = roads[chain[i]];
    let end, next = null;
    if (i < chain.length - 1) {
      const c = cross(roads, chain[i], chain[i + 1]);
      end = c.alongA;
      next = c.alongB;
    } else end = b.along;
    if (Math.abs(end - at) > 0.5 || i === chain.length - 1)
      out.push({ road: chain[i], name: R.name, heads: heading(R, at, end), to: pointOn(R, end), turn: null, metres: Math.round(Math.abs(end - at)) });
    at = next;
  }
  for (let i = 0; i < out.length - 1; i++) out[i].turn = turn(out[i].heads, out[i + 1].heads);
  return out;
}
const metres = (ls) => ls.reduce((n, l) => n + l.metres, 0);
// Pauline's words: by road and landmark, never a number of metres. junctions: { 'roadA>roadB': 'the landmark' }.
function words(ls, junctions, place) {
  const s = [];
  for (let i = 0; i < ls.length; i++) {
    const l = ls[i];
    if (!i) s.push(`${l.heads === 'north' ? 'Up' : l.heads === 'south' ? 'Down' : 'Along'} ${l.name}${l.road === 'qs' ? '' : ', ' + l.heads}`);
    if (l.turn) s.push(`${l.turn} at ${junctions[l.road + '>' + ls[i + 1].road] || ls[i + 1].name} ${ls[i + 1].heads === 'north' ? 'and up' : ls[i + 1].heads === 'south' ? 'and down' : ls[i + 1].road === 'quay' ? 'along' : 'into'} ${ls[i + 1].name}`);
  }
  return s.map((x) => x.charAt(0).toUpperCase() + x.slice(1)).join('. ') + '. ' + place + '.';
}
// What the fare in the back says a junction before: "Left here." (A9). Null when no turn is near.
function leftHere(t, ls, pos) {
  for (const l of ls) {
    if (!l.turn) continue;
    const d = Math.abs(pos.x - l.to.x) + Math.abs(pos.z - l.to.z);
    if (d <= t.leftHereBeforeJunctionMetres) return { turn: l.turn, key: l.road + '>' + l.turn };
  }
  return null;
}
export const PIECE = { name: 'fare_rules', fns: { pay, next, onRoad, legs, metres, words, leftHere, turn } };
