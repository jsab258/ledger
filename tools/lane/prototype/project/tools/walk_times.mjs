// How long every walk in every schedule takes, against the time its row has.
// For each person and each row of their week it works out the way they walk (the game's own paths), and the
// game minutes it takes twice: with Tom away (nobody in his sight, so everybody at the quicker pace) and with
// Tom standing at the rank (within routines.fullyStepsWithinMetres of him they walk at their real pace).
// A row must leave room for the walk and a margin; rows that do not are listed.
//   node tools/walk_times.mjs            the rows that are too short (none: PASS)
//   node tools/walk_times.mjs --all      every walk
//   node tools/walk_times.mjs <id>       one person's walks
import { RULES } from '../src/rules.js';
import { CAST } from '../src/cast.js';
import { SPOTS, ROOMS, EXITS, WINDOWS, NODES, nearNode, path, roomPos } from '../src/map.js';

const W = RULES.routines, MARGIN = 1.25, REAL_SECONDS_PER_GAME_MINUTE = RULES.time.realSecondsPerGameHour / 60;
const tom = SPOTS.rank;
const hyp = (ax, az, bx, bz) => Math.hypot(ax - bx, az - bz);
const homePoint = (d) => {
  const w = WINDOWS[d.id];
  return w ? [w[0] + Math.sin(w[2]) * 0.9, w[1] + Math.cos(w[2]) * 0.9] : SPOTS[d.homeSpot || 'chapelgate'];
};
const exitOf = (d) => EXITS[d.exit || (['susan', 'lee', 'norman'].includes(d.id) ? 'E' : d.id === 'dennis' ? 'W' : 'N')];
// where a place is entered from the street, and how far the walk goes on indoors
function point(d, where) {
  if (where === 'home') return { p: homePoint(d), inside: 0 };
  if (where === 'off') return { p: exitOf(d), inside: 0 };
  const i = where.indexOf(':');
  if (i > 0) {
    const r = ROOMS[where.slice(0, i)], s = r.spots[where.slice(i + 1)] || [0, 0, 0];
    return { p: r.street, inside: Math.hypot(s[0] - r.mat[0], s[1] - r.mat[1]) };
  }
  return { p: SPOTS[where] || SPOTS.pave, inside: 0 };
}
function way(a, b) {
  const pts = [a];
  if (hyp(a[0], a[1], b[0], b[1]) > W.takesThePathsBeyondMetres) for (const n of path(nearNode(a[0], a[1]), nearNode(b[0], b[1]))) pts.push([NODES[n].x, NODES[n].z]);
  pts.push(b);
  return pts;
}
function walk(d, from, to) {
  const A = point(d, from), B = point(d, to), pts = way(A.p, B.p);
  const v = d.frail ? W.frailMetresPerSecond : d.age > W.slowerAboveAgeYears ? W.over60MetresPerSecond : W.walkingMetresPerSecond;
  const quick = v * W.paceOutOfHisSightTimes;
  let metres = 0, inSight = 0;
  for (let i = 1; i < pts.length; i++) {
    const [ax, az] = pts[i - 1], [bx, bz] = pts[i], L = hyp(ax, az, bx, bz), n = Math.max(1, Math.ceil(L));
    for (let k = 0; k < n; k++) {
      const x = ax + ((bx - ax) * (k + 0.5)) / n, z = az + ((bz - az) * (k + 0.5)) / n;
      metres += L / n;
      if (hyp(x, z, tom[0], tom[1]) < W.fullyStepsWithinMetres) inSight += L / n;
    }
  }
  const indoors = A.inside + B.inside;
  const away = (metres + indoors) / quick / REAL_SECONDS_PER_GAME_MINUTE;
  const rank = (inSight / v + (metres - inSight + indoors) / quick) / REAL_SECONDS_PER_GAME_MINUTE;
  return { metres: Math.round(metres + indoors), inSight: Math.round(inSight), away, rank };
}
// a person's rows on one day, in order, as the game picks them (a row for that day wins over an every-day row)
function rowsOn(id, day) {
  const rows = RULES.schedules[id].filter((r) => !r.onDayIndexes || r.onDayIndexes.includes(day % 7));
  return rows
    .map((r, i) => ({ ...r, i }))
    .sort((a, b) => a.fromHour - b.fromHour || (a.onDayIndexes ? 1 : 0) - (b.onDayIndexes ? 1 : 0))
    .filter((r, i, all) => !(all[i + 1] && all[i + 1].fromHour === r.fromHour));
}
const only = process.argv.find((a, i) => i > 1 && !a.startsWith('--')), all = process.argv.includes('--all');
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
let bad = 0, walks = 0;
const seen = new Set();
for (const d of CAST) {
  if (d.police || (only && d.id !== only)) continue;
  for (let day = 0; day < 5; day++) {
    const today = rowsOn(d.id, day), next = rowsOn(d.id, day + 1);
    const yesterday = rowsOn(d.id, day + 6);
    for (let i = 0; i < today.length; i++) {
      const r = today[i], prev = i ? today[i - 1] : yesterday[yesterday.length - 1];
      if (prev.place === r.place) continue; // the same place: no walk (a new thing to do there, at most)
      const until = i + 1 < today.length ? today[i + 1].fromHour : 24 + next[0].fromHour + (next[0].place === r.place && next[1] ? next[1].fromHour : 0);
      const slot = (until - r.fromHour) * 60, w = walk(d, prev.place, r.place);
      const key = `${d.id}|${prev.place}|${r.place}|${r.fromHour}|${until}`;
      const short = w.away * MARGIN > slot || w.rank * MARGIN > slot;
      if (seen.has(key)) continue;
      seen.add(key);
      walks++;
      if (short) bad++;
      if (short || all || only)
        console.log(`${short ? 'SHORT' : 'ok   '} ${d.id.padEnd(8)} ${DAYS[day]} ${String(r.fromHour).padStart(5)} ${(prev.place + ' -> ' + r.place).padEnd(44)} ${String(w.metres).padStart(4)} m (${String(w.inSight).padStart(3)} in his sight)  needs ${String(Math.round(w.away)).padStart(3)} away, ${String(Math.round(w.rank)).padStart(3)} at the rank | has ${Math.round(slot)} game minutes`);
    }
  }
}
console.log(bad ? `${bad} of ${walks} walks have too little time (the walk and a quarter again)` : `PASS: all ${walks} walks fit their rows, with Tom away and with Tom at the rank, with a quarter to spare`);
process.exit(bad ? 1 : 0);
