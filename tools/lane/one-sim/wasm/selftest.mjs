// ONE SIMULATION IN THE BROWSER: the checks checked (19 November 2026).
//
//   node selftest.mjs --brain one-sim.wasm --check one-sim-check.wasm --golden TABLE.txt --specs production/specs
//
// A check that cannot fail proves nothing. The accepting case comes first (the true table
// passes); then the table is spoiled in four small ways and each must be caught, by the
// check it belongs to and by no more rows than were spoiled.
import { readFileSync } from 'node:fs';
import { runChecks } from './checks.mjs';

const arg = (name) => { const i = process.argv.indexOf('--' + name); return i > 0 ? process.argv[i + 1] : undefined; };
const brainBytes = readFileSync(arg('brain')), checkBytes = readFileSync(arg('check')), specs = arg('specs');
const tableText = readFileSync(arg('golden'), 'utf8');
const dataText = {};
for (const name of ['hook-cast.json', 'quay-cast.json', 'town-news.json']) dataText[name] = readFileSync(specs + '/' + name, 'utf8');

let pass = 0, fail = 0;
const ok = (what, cond) => { if (cond) pass++; else fail++; console.log(`  ${cond ? 'ok  ' : 'FAIL'} ${what}`); };

console.log('[1] ACCEPTING CASE: the table as the C# Core wrote it');
const good = await runChecks({ brainBytes, checkBytes, tableText, dataText });
ok('every check passes', good.failed === 0);

console.log('[2] FOUR SPOILED ROWS MUST BE CAUGHT, EACH BY ITS OWN CHECK');
const lines = tableText.split('\n');
const spoil = (prefix, change) => {
  const i = lines.findIndex((l) => l.startsWith(prefix));
  if (i < 0) throw new Error('no row starts with ' + prefix);
  const cr = lines[i].endsWith('\r') ? '\r' : '';
  const f = lines[i].replace(/\r$/, '').split('|');
  change(f);
  lines[i] = f.join('|') + cr;
};
spoil('MotionFactor|4|', (f) => { f[f.length - 1] = '0.123'; });                 // a single rule's number
spoil('CastPlaceOf|hook-cast.json|', (f) => { f[f.length - 1] = 'nowhere_at_all'; });   // a routine's place
spoil('TownWeekHour|days|1|12|', (f) => { f[f.length - 1] = 'yes~wrong'; });      // an hour of a scripted week
lines.push('NoSuchRule|1|2');                                                     // a rule this build cannot answer
const bad = await runChecks({ brainBytes, checkBytes, tableText: lines.join('\n'), dataText });
ok('T1 sees exactly the three wrong answers', bad.T1.mismatch === 3);
ok('T1 sees the one row nobody can answer', bad.T1.unknown === 1);
ok('T2 (routines through the bridge) sees the one wrong place', bad.T2.bad === 1);
ok('T3 (the week through the bridge) sees the one wrong hour', bad.T3.bad === 1);
ok('T4 (same town twice) is untouched by a spoiled table', bad.T4.first === good.T4.first && bad.T4.second === good.T4.second);
ok('and the run as a whole fails', bad.failed >= 3);

console.log(`one-sim selftest: passed=${pass}/${pass + fail} failed=${fail}`);
process.exit(fail ? 4 : 0);
