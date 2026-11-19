// ONE SIMULATION IN THE BROWSER: the checks, run under Node (first slice, 19 November 2026).
//
//   node test_one_sim.mjs --brain one-sim.wasm --check one-sim-check.wasm \
//        --golden TABLE.txt --specs production/specs [--json OUT.json]
//   --bridge-only (then no --check): only the checks that go through the front door, T2 to T5.
//
// The checks are in checks.mjs (the same file a real web page runs, see browser_test.py).
// This wrapper reads the files, runs them, and adds the download sizes.
import { readFileSync, writeFileSync } from 'node:fs';
import { gzipSync, brotliCompressSync, constants as z } from 'node:zlib';
import { runChecks } from './checks.mjs';

const arg = (name, dflt) => { const i = process.argv.indexOf('--' + name); return i > 0 ? process.argv[i + 1] : dflt; };
const brainPath = arg('brain'), checkPath = arg('check'), goldenPath = arg('golden'), specs = arg('specs'), jsonOut = arg('json');
const bridgeOnly = process.argv.includes('--bridge-only');   // T2 to T5 only: no check build needed
if (!brainPath || (!checkPath && !bridgeOnly) || !goldenPath || !specs) {
  console.error('usage: node test_one_sim.mjs --brain one-sim.wasm --check one-sim-check.wasm --golden TABLE.txt --specs production/specs');
  process.exit(2);
}
const brainBytes = readFileSync(brainPath), checkBytes = bridgeOnly ? null : readFileSync(checkPath);
const dataText = {};
for (const name of ['hook-cast.json', 'quay-cast.json', 'town-news.json']) dataText[name] = readFileSync(specs + '/' + name, 'utf8');

const report = await runChecks({ brainBytes, checkBytes, tableText: readFileSync(goldenPath, 'utf8'), dataText, log: (t) => console.log(t) });

const size = (b) => ({ raw: b.length, gzip: gzipSync(b, { level: 9 }).length, brotli: brotliCompressSync(b, { params: { [z.BROTLI_PARAM_QUALITY]: 11 } }).length });
report.size = { brain: size(brainBytes), check: checkBytes ? size(checkBytes) : null, loader: size(readFileSync(new URL('./one-sim.mjs', import.meta.url))) };
console.log(`info size: the brain ${report.size.brain.raw} bytes, ${report.size.brain.gzip} gzip, ${report.size.brain.brotli} Brotli; its loader ${report.size.loader.raw} bytes, ${report.size.loader.gzip} gzip` + (checkBytes ? `; the check build ${report.size.check.raw} bytes (never shipped)` : ''));
if (jsonOut) writeFileSync(jsonOut, JSON.stringify(report, null, 1));
console.log(report.failed ? `one-sim tests: ${report.failed} FAILED` : 'one-sim tests: all passed');
process.exit(report.failed ? 1 : 0);
