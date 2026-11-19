// Build the game: bundle src/main.js into dist/ledger.js, and copy the page and the art beside it.
//   npm run build        the published build (minified)
//   npm run build:dev    the same, not minified, with a source map
import { build } from 'esbuild';
import fs from 'fs';
import path from 'path';

const dev = process.argv.includes('--dev');
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
  if (/^(people(_lo)?\.jpg|people\.txt|tx_(road|plaza|wood|plaster|stone)_[dn]\.jpg)$/.test(f))
    fs.copyFileSync(path.join('assets', f), path.join('dist', f));
}
const size = (f) => (fs.statSync(f).size / 1024).toFixed(0) + ' KB';
console.log('built dist/ledger.js', size('dist/ledger.js'), '| dist/index.html', size('dist/index.html'));
