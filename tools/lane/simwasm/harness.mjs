// Fallback check: JavaScript rules held to the C# Core's golden rows.
// Usage: node tools/lane/simwasm/harness.mjs OUT.json   (OUT.json from export_golden.py)
//
// Each rule declares how its answer is compared: 'number' (agreement to 1e-9,
// as the C++ port) or 'text' (exact; bits "0"/"1", ids, words). Nothing is
// guessed from the value. A rule with no rows in the table fails: a JavaScript
// rule may only be used if the table checks it.
// Constants are not trusted by hand: CONSTANT_PINS below check each one
// against rows that sit exactly on it, so a drifted constant fails here.
import { readFileSync } from 'node:fs';

const golden = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const Walk = 4.0, Run = 7.0, Fov = 120, Acuity = 60;   // Feel.cs Locomotion, Perception.cs
const clamp = (v, lo, hi) => v < lo ? lo : v > hi ? hi : v;

const rules = {
  MotionFactor: { kind: 'number', fn: ([s]) => { s = +s; if (s <= 0.05) return 0.5; if (s >= Run) return 2.0;
    return s <= Walk ? 0.5 + 0.5 * (s - 0.05) / (Walk - 0.05) : 1.0 + 1.0 * (s - Walk) / (Run - Walk); } },
  ConeWeight:   { kind: 'number', fn: ([d]) => { const a = Math.abs(+d); return a <= Acuity / 2 ? 1.0 : a <= Fov / 2 ? 0.35 : 0.0; } },
  LightFactor:  { kind: 'number', fn: ([l]) => clamp(0.12 + 0.88 * Math.pow(clamp(+l, 0, 1), 0.78), 0.12, 1.0) },
};

// rule, args, expected answer that only holds if the constant is right
const CONSTANT_PINS = [
  ['Walk',   'MotionFactor', ['4'], '1'],   ['Run',    'MotionFactor', ['7'], '2'],
  ['Acuity', 'ConeWeight', ['30'], '1'],    ['Acuity', 'ConeWeight', ['30.1'], '0.35'],
  ['Fov',    'ConeWeight', ['60'], '0.35'], ['Fov',    'ConeWeight', ['60.1'], '0'],
];

let pass = 0, fail = 0;
for (const [name, rule, args, want] of CONSTANT_PINS) {
  const row = (golden[rule] ?? []).find(r => r.args.join('|') === args.join('|'));
  if (!row || row.expected !== want) { fail++; console.log('CONSTANT PIN FAILED', name, rule, args, row?.expected); }
}
for (const [name, { kind, fn }] of Object.entries(rules)) {
  const rows = golden[name] ?? [];
  if (rows.length === 0) { fail++; console.log('NO ROWS IN TABLE', name); continue; }
  for (const row of rows) {
    const got = fn(row.args);
    const ok = kind === 'number' ? Math.abs(got - Number(row.expected)) <= 1e-9 : String(got) === row.expected;
    if (ok) pass++; else { fail++; console.log('FAIL', name, row.args, got, row.expected); }
  }
}
console.log(`rows checked=${pass + fail} pass=${pass} fail=${fail} rulesInTable=${Object.keys(golden).length} portedHere=${Object.keys(rules).length}`);
process.exit(fail ? 1 : 0);
