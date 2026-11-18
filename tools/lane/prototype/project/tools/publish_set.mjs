// Gather what is published: the page, the art, the documents, the measures from the last full-week run,
// the source under source/, and files.json (read by the game's "Source and files" screen).
//   npm run publish-set            writes site/
//   node tools/publish_set.mjs out writes out/
// Run after `npm run build` and `node test/week.mjs`. Files are overwritten, never deleted.
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { NOTES } from '../src/design_notes_text.js';

const OUT = process.argv[2] || 'site';
const TODAY = process.env.PUBLISHED || new Date().toISOString().slice(0, 10);
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const firstLine = (f) => {
  const m = fs.readFileSync(f, 'utf8').match(/^\s*(?:\/\/|#|<!--)\s*(.+)/);
  return m ? m[1].replace(/^LEDGER[.:]\s*/, '').replace(/-->\s*$/, '').trim() : '';
};
const groups = [];
const put = (group, from, as, to, what, text = true) => {
  const dest = path.join(OUT, to);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(from, dest);
  let g = groups.find((x) => x.name === group);
  if (!g) groups.push((g = { name: group, files: [] }));
  g.files.push({ path: to.split(path.sep).join('/'), as, what, bytes: fs.statSync(dest).size, text });
};
const ls = (dir, re) =>
  fs
    .readdirSync(dir)
    .filter((f) => re.test(f))
    .sort();

// the design notes as a document, from the text the game shows
fs.writeFileSync(
  'DESIGN_NOTES.md',
  '# LEDGER loop prototype: design notes\n\nChoices made without asking, as instructed. Anything marked invented is mine and not canon.\nWritten from `src/design_notes_text.js`, the same text the game shows under Design notes.\n\n' +
    NOTES.map((n) => `## ${n[0]}\n\n${n[1].replace(/\n/g, '\n\n')}\n`).join('\n'),
);

// the build notes, with this publication's checksums at the foot
const sums = { ledger: sha('dist/ledger.js'), index: sha('dist/index.html') };
fs.mkdirSync(OUT, { recursive: true });
const buildPublished = path.join(OUT, '.BUILD.tmp');
fs.writeFileSync(
  buildPublished,
  fs.readFileSync('BUILD.md', 'utf8') +
    `\n## This publication\n\nPublished ${TODAY}.\n\n    ${sums.ledger}  dist/ledger.js\n    ${sums.index}  dist/index.html\n`,
);

const READ = 'Read first';
put(READ, 'README.md', 'README.md', 'README.md', 'What this is, and the source file by file.');
put(READ, 'CHANGELOG.md', 'CHANGELOG.md', 'CHANGELOG.md', 'What changed, item by item, with the date.');
put(READ, 'NOT_DONE.md', 'NOT_DONE.md', 'NOT_DONE.md', 'What could not be done, and why.');
put(READ, buildPublished, 'BUILD.md', 'BUILD.md', 'The build command, the pinned versions, the checksums.');
fs.unlinkSync(buildPublished);
put(READ, 'DESIGN_NOTES.md', 'DESIGN_NOTES.md', 'DESIGN_NOTES.md', 'Every choice made without asking.');
put(
  READ,
  'out/measures.json',
  'measures.json',
  'measures.json',
  'The measures from one full week, played by a script through the test hook.',
);

const SRC = 'The source, one file per part (src/)';
for (const f of ls('src', /\.js$/)) put(SRC, `src/${f}`, `src/${f}`, `source/src/${f}`, firstLine(`src/${f}`));
put(SRC, 'src/index.html', 'src/index.html', 'source/src/index.html', 'The page and its styles.');
const REN = 'The source: rendering (src/render/)';
for (const f of ls('src/render', /\.js$/))
  if (f !== 'viewer.js')
    put(REN, `src/render/${f}`, `src/render/${f}`, `source/src/render/${f}`, firstLine(`src/render/${f}`));

const BLD = 'The build';
put(BLD, 'package.json', 'package.json', 'source/package.json', 'three pinned at 0.187.0; the build and test commands.');
put(BLD, 'package-lock.json', 'package-lock.json', 'source/package-lock.json', 'Every package at its exact version.');
put(BLD, 'tools/build.mjs', 'tools/build.mjs', 'source/tools/build.mjs', firstLine('tools/build.mjs'));
put(BLD, 'tools/publish_set.mjs', 'tools/publish_set.mjs', 'source/tools/publish_set.mjs', firstLine('tools/publish_set.mjs'));
put(BLD, 'tools/pack_people.mjs', 'tools/pack_people.mjs', 'source/tools/pack_people.mjs', firstLine('tools/pack_people.mjs'));
put(BLD, '.prettierrc.json', '.prettierrc.json', 'source/prettierrc.json', 'Formatting rules (kept as .prettierrc.json).');
put(BLD, '.eslintrc.json', '.eslintrc.json', 'source/eslintrc.json', 'Lint rules (kept as .eslintrc.json).');

const TST = 'The tests (test/)';
const TESTS = (process.env.TESTS || 'harness week nights layout files talk oldsave eyes').split(' ');
for (const t of TESTS)
  if (fs.existsSync(`test/${t}.mjs`))
    put(TST, `test/${t}.mjs`, `test/${t}.mjs`, `source/test/${t}.mjs`, firstLine(`test/${t}.mjs`));

const PAGE = 'The built page (dist/)';
put(PAGE, 'dist/index.html', 'dist/index.html', 'index.html', 'The page, copied from src/index.html.');
put(PAGE, 'dist/ledger.js', 'dist/ledger.js', 'ledger.js', 'The game, built from src/ by npm run build.', false);
const ART = 'The art (assets/), copied unchanged by the build';
for (const f of ls('assets', /^(people(_lo)?\.jpg|people\.txt|tx_(road|plaza|wood|plaster|stone)_[dn]\.jpg)$/))
  put(ART, `assets/${f}`, `assets/${f}`, f, f === 'people.txt' ? 'The rigged figures and their animations, packed.' : 'Picture.', false);

fs.writeFileSync(
  path.join(OUT, 'files.json'),
  JSON.stringify(
    {
      published: TODAY,
      buildCommand: 'npm run build',
      dependencies: { three: '0.187.0', esbuild: '0.28.2' },
      ledgerJsSha256: sums.ledger,
      indexHtmlSha256: sums.index,
      groups,
    },
    null,
    1,
  ) + '\n',
);
const n = groups.reduce((a, g) => a + g.files.length, 0);
console.log(`wrote ${OUT}/: ${n} files listed in files.json, ledger.js ${sums.ledger.slice(0, 16)}...`);
