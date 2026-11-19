// Run a WebAssembly (WASI) program under Node, the same engine family (V8) as Chrome and Edge.
// Usage: node run_wasi.mjs PROGRAM.wasm [--dir GUEST=HOST ...] [--quiet] [-- args...]
// Each --dir lets the program read one folder: inside the program it is named GUEST.
// The port's golden test opens "production/specs/<cast file>" and the table path it is given.
import { readFileSync } from 'node:fs';
import { WASI } from 'node:wasi';

const argv = process.argv.slice(2);
const prog = argv.shift();
const preopens = {};
let quiet = false;
const args = [];
while (argv.length) {
  const a = argv.shift();
  if (a === '--dir') { const [g, h] = argv.shift().split('='); preopens[g] = h; }
  else if (a === '--quiet') quiet = true;
  else if (a === '--') { args.push(...argv); break; }
  else args.push(a);
}
if (!prog) { console.error('usage: node run_wasi.mjs PROGRAM.wasm [--dir GUEST=HOST ...] [-- args...]'); process.exit(2); }
const wasi = new WASI({ version: 'preview1', args: [prog, ...args], env: {}, preopens, returnOnExit: true });
const t0 = performance.now();
const mod = await WebAssembly.compile(readFileSync(prog));
const inst = await WebAssembly.instantiate(mod, wasi.getImportObject());
const t1 = performance.now();
const code = wasi.start(inst);
const t2 = performance.now();
if (!quiet) console.error(`[run_wasi] compile+instantiate ${(t1 - t0).toFixed(0)} ms, run ${(t2 - t1).toFixed(0)} ms, exit ${code}`);
process.exit(code ?? 0);
