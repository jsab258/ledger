// Build the game: bundle src/main.js into dist/ledger.js, and copy the page and the art beside it.
//   npm run build        the published build (minified)
//   npm run build:dev    the same, not minified, with a source map
import { build } from 'esbuild';
import fs from 'fs';
import path from 'path';

const dev = process.argv.includes('--dev');
// The real town (the one-shot, 20 Nov 2026): the loader, the bridge and the cast file sit beside the source in onesim/.
// build.py puts them there in its work folder. Run straight from the repository, they are fetched from the one-sim folder.
if (!fs.existsSync('onesim/one-sim-bridge.mjs')) {
  const from = path.join('..', '..', 'one-sim', 'wasm'), cast = path.join('..', '..', '..', '..', 'production', 'specs', 'hook-cast.json');
  if (!fs.existsSync(path.join(from, 'one-sim-bridge.mjs')) || !fs.existsSync(cast))
    throw new Error('onesim/ is missing: build with tools/lane/prototype/build.py, or from inside the repository');
  fs.mkdirSync('onesim', { recursive: true });
  for (const f of ['one-sim.mjs', 'one-sim-bridge.mjs']) fs.copyFileSync(path.join(from, f), path.join('onesim', f));
  fs.writeFileSync('onesim/cast.mjs', '// production/specs/hook-cast.json as text.\nexport const CAST_JSON = ' + JSON.stringify(fs.readFileSync(cast, 'utf8').replace(/^\uFEFF/, '')) + ';\n');
}
fs.mkdirSync('dist', { recursive: true });
await build({
  entryPoints: ['src/main.js'],
  bundle: true,
  format: 'iife',
  minify: !dev,
  sourcemap: dev,
  outfile: 'dist/ledger.js',
  logLevel: 'warning',
});
fs.copyFileSync('src/index.html', 'dist/index.html');
for (const f of fs.readdirSync('assets')) {
  if (/^(people(_lo)?\.jpg|people\.txt|tx_(road|plaza|wood|plaster|stone)_[dn]\.jpg|one-sim\.wasm|ONE-SIM-CREDITS\.md)$/.test(f))
    fs.copyFileSync(path.join('assets', f), path.join('dist', f));
}
const size = (f) => (fs.statSync(f).size / 1024).toFixed(0) + ' KB';
console.log('built dist/ledger.js', size('dist/ledger.js'), '| dist/index.html', size('dist/index.html'));
