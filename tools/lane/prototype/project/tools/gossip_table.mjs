// The gossip before and after a change, as a table. Reads two files written by test/same_week.mjs
// (GOSSIP_OUT=<file>): the same seeded week on two builds.
//   node tools/gossip_table.mjs out/gossip_before.json out/gossip_after.json
import fs from 'fs';
const [, , a, b] = process.argv;
const A = JSON.parse(fs.readFileSync(a, 'utf8')), B = JSON.parse(fs.readFileSync(b, 'utf8'));
const days = Math.max(A.length, B.length), row = (d, k) => (d ? d[k] : '');
const out = [];
out.push('| Day | Sightings | Stories passed on | Furthest story (tellings) | Pairs of named people who met |');
out.push('| --- | --- | --- | --- | --- |');
const tot = { s: [0, 0], p: [0, 0], f: [0, 0] };
for (let i = 0; i < days; i++) {
  const x = A[i], y = B[i];
  out.push(`| ${(x || y).date} | ${row(x, 'sightings')} then ${row(y, 'sightings')} | ${row(x, 'storiesPassedOn')} then ${row(y, 'storiesPassedOn')} | ${row(x, 'furthestStoryTellings')} then ${row(y, 'furthestStoryTellings')} | ${x ? x.pairsWhoMet.length : ''} then ${y ? y.pairsWhoMet.length : ''} |`);
  [x, y].forEach((d, k) => { if (d) { tot.s[k] += d.sightings; tot.p[k] += d.storiesPassedOn; tot.f[k] = Math.max(tot.f[k], d.furthestStoryTellings); } });
}
const all = (D) => new Set(D.flatMap((d) => d.pairsWhoMet));
const pa = all(A), pb = all(B);
out.push(`| The week | ${tot.s[0]} then ${tot.s[1]} | ${tot.p[0]} then ${tot.p[1]} | ${tot.f[0]} then ${tot.f[1]} | ${pa.size} then ${pb.size} |`);
const gained = [...pb].filter((p) => !pa.has(p)).sort(), lost = [...pa].filter((p) => !pb.has(p)).sort();
out.push('');
out.push(`Met in the week after, not before (${gained.length}): ${gained.join('; ') || 'none'}.`);
out.push('');
out.push(`Met in the week before, not after (${lost.length}): ${lost.join('; ') || 'none'}.`);
console.log(out.join('\n'));
