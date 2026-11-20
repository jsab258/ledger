// The rule pieces' own test cases, under Node, no browser. A piece is src/game/pieces/<name>.js exporting
// PIECE = { name, fns: { fnName: fn } }: pure functions of their arguments (plain data in, plain data out, no clock,
// no random numbers but a seed handed in). Its cases are test/cases/<name>.json:
//   { "piece": "<name>", "cases": [ { "id": "...", "rule": "ER-...", "fn": "fnName", "in": [args], "out": expected } ] }
// "out" is compared deeply; a number within 1e-9. A case may give "outHas" instead: every key of it must match.
// A case may give "outBand" as well or instead: { key: [least, most] }, for a result that is a measure.
// Unreal ports the piece and passes the same cases. Usage: node test/pieces.mjs [name ...]
import fs from 'fs';
import path from 'path';
import url from 'url';
const here = path.dirname(url.fileURLToPath(import.meta.url));
const want = process.argv.slice(2);
const same = (a, b) => {
  if (typeof a === 'number' && typeof b === 'number') return Math.abs(a - b) < 1e-9;
  if (a === null || b === null || typeof a !== 'object' || typeof b !== 'object') return a === b;
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  const ka = Object.keys(a), kb = Object.keys(b);
  return ka.length === kb.length && ka.every((k) => same(a[k], b[k]));
};
const has = (got, part) => {
  if (part === null || typeof part !== 'object') return same(got, part);
  if (got === null || typeof got !== 'object') return false;
  return Object.keys(part).every((k) => has(got[k], part[k]));
};
let pass = 0, fail = 0, pieces = 0;
for (const f of fs.readdirSync(path.join(here, 'cases')).filter((f) => f.endsWith('.json')).sort()) {
  const set = JSON.parse(fs.readFileSync(path.join(here, 'cases', f), 'utf8'));
  if (want.length && !want.includes(set.piece)) continue;
  const mod = await import(url.pathToFileURL(path.join(here, '..', 'src', 'game', 'pieces', set.piece + '.js')));
  pieces++;
  let p = 0, bad = 0;
  for (const c of set.cases) {
    const fn = mod.PIECE.fns[c.fn];
    let got, err = null;
    try { got = fn(...JSON.parse(JSON.stringify(c.in))); } catch (e) { err = e; }
    const band = (g, b) => Object.keys(b).every((k) => typeof g[k] === 'number' && g[k] >= b[k][0] && g[k] <= b[k][1]);
    const ok = !err && fn && ('outBand' in c ? band(got, c.outBand) && (!('outHas' in c) || has(got, c.outHas)) : 'outHas' in c ? has(got, c.outHas) : same(got === undefined ? null : JSON.parse(JSON.stringify(got)), c.out));
    if (ok) p++;
    else { bad++; console.log(`FAIL ${set.piece} ${c.id}${c.rule ? ' (' + c.rule + ')' : ''}: ${err ? err.message : 'got ' + JSON.stringify(got)}`); }
  }
  console.log(`${bad ? 'FAIL' : 'ok  '} ${set.piece}: ${p} of ${set.cases.length} cases`);
  pass += p; fail += bad;
}
console.log(`PIECES ${pieces}, CASES ${pass + fail}, FAILED ${fail}`);
console.log(fail || !pieces ? 'FAIL' : 'PASS');
process.exit(fail || !pieces ? 1 : 0);
