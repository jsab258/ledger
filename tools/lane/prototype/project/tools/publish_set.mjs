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

// what the checks found, this round
const RES = 'Results of the checks';
put(RES, 'RESULTS.md', 'RESULTS.md', 'RESULTS.md', 'Both arrivals checks, the nights check, the same-week proof, the gossip table.');
const result = (from, name, what) => { if (fs.existsSync(from)) put(RES, from, 'results/' + name, 'results/' + name, what); };
result('out/arrivals.json', 'arrivals.json', 'LEDGER.check.arrivals() over 26 game hours: Tom away, and Tom at the rank.');
result('out/nights.json', 'nights.json', 'LEDGER.check.nights(): Tuesday and Wednesday nights, every pause and its resume.');
result('out/gossip_before.json', 'gossip_before.json', 'The gossip of the seeded week before the retiming, day by day.');
result('out/gossip_after.json', 'gossip_after.json', 'The gossip of the same seeded week after the retiming.');

const SRC = 'The source, one file per part (src/)';
for (const f of ls('src', /\.js$/)) put(SRC, `src/${f}`, `src/${f}`, `source/src/${f}`, firstLine(`src/${f}`));
put(SRC, 'src/index.html', 'src/index.html', 'source/src/index.html', 'The page and its styles.');
const REN = 'The source: rendering (src/render/)';
for (const f of ls('src/render', /\.js$/))
  if (f !== 'viewer.js')
    put(REN, `src/render/${f}`, `src/render/${f}`, `source/src/render/${f}`, firstLine(`src/render/${f}`));

// The whole game (the one-shot, 20 Nov 2026): its systems, their numbers, kinds and people, and the rule pieces.
const GAME = 'The source: the whole game (src/game/)';
for (const dir of ['src/game', 'src/game/pieces', 'src/game/tune', 'src/game/kinds', 'src/game/cast'])
  if (fs.existsSync(dir)) for (const f of ls(dir, /\.js$/)) put(GAME, `${dir}/${f}`, `${dir}/${f}`, `source/${dir}/${f}`, firstLine(`${dir}/${f}`));
// The real town: the loader, the bridge and the cast file sit in onesim/ (written there by the build); the town's
// rules themselves are the game's own code, compiled into one-sim.wasm, which is beside the page with its credits.
const TOWN = "The real town (onesim/): the game's own town code, compiled for the browser";
if (fs.existsSync('onesim'))
  for (const f of ls('onesim', /\.mjs$/)) put(TOWN, `onesim/${f}`, `onesim/${f}`, `source/onesim/${f}`, firstLine(`onesim/${f}`) || 'The cast file, as text.');
if (fs.existsSync('dist/one-sim.wasm')) put(TOWN, 'dist/one-sim.wasm', 'one-sim.wasm', 'one-sim.wasm', "The town's rules: LEDGER's own C++ town code, compiled (made by tools/lane/one-sim).", false);
if (fs.existsSync('dist/ONE-SIM-CREDITS.md')) put(TOWN, 'dist/ONE-SIM-CREDITS.md', 'ONE-SIM-CREDITS.md', 'ONE-SIM-CREDITS.md', 'Credits and licence notices for the library pieces inside one-sim.wasm.');

const BLD = 'The build';
put(BLD, 'package.json', 'package.json', 'source/package.json', 'three pinned at 0.187.0; the build and test commands.');
put(BLD, 'package-lock.json', 'package-lock.json', 'source/package-lock.json', 'Every package at its exact version.');
put(BLD, 'tools/build.mjs', 'tools/build.mjs', 'source/tools/build.mjs', firstLine('tools/build.mjs'));
put(BLD, 'tools/publish_set.mjs', 'tools/publish_set.mjs', 'source/tools/publish_set.mjs', firstLine('tools/publish_set.mjs'));
put(BLD, 'tools/pack_people.mjs', 'tools/pack_people.mjs', 'source/tools/pack_people.mjs', firstLine('tools/pack_people.mjs'));
for (const t of ['numbers.mjs', 'walk_times.mjs', 'gossip_table.mjs'])
  put(BLD, `tools/${t}`, `tools/${t}`, `source/tools/${t}`, firstLine(`tools/${t}`));
put(BLD, 'tools/numbers_kept.json', 'tools/numbers_kept.json', 'source/tools/numbers_kept.json', 'How many numbers may stay outside rules.js in each file, and why.');
put(BLD, '.prettierrc.json', '.prettierrc.json', 'source/prettierrc.json', 'Formatting rules (kept as .prettierrc.json).');
put(BLD, '.eslintrc.json', '.eslintrc.json', 'source/eslintrc.json', 'Lint rules (kept as .eslintrc.json).');

const TST = 'The tests (test/)';
// every test the project has, the lane's rounds included (fixes1 to gate6), so the page's list names each one
const TESTS = (process.env.TESTS || 'harness fixes1 watch2 melee3 melee4 talk5 gate6 week_bot week same_week arrivals nights town ledger_rules layout files talk oldsave eyes').split(' ');
for (const t of TESTS)
  if (fs.existsSync(`test/${t}.mjs`))
    put(TST, `test/${t}.mjs`, `test/${t}.mjs`, `source/test/${t}.mjs`, firstLine(`test/${t}.mjs`));

if (fs.existsSync('test/pieces.mjs')) put(TST, 'test/pieces.mjs', 'test/pieces.mjs', 'source/test/pieces.mjs', firstLine('test/pieces.mjs'));
if (fs.existsSync('test/game')) for (const f of ls('test/game', /\.mjs$/)) put(TST, `test/game/${f}`, `test/game/${f}`, `source/test/game/${f}`, firstLine(`test/game/${f}`));
if (fs.existsSync('test/cases')) for (const f of ls('test/cases', /\.json$/)) put(TST, `test/cases/${f}`, `test/cases/${f}`, `source/test/cases/${f}`, 'Test cases of the rule piece of the same name: inputs and expected outputs.');
put(TST, 'test/golden/week.json', 'test/golden/week.json', 'source/test/golden/week.json', 'The record of the seeded week: what test/same_week.mjs compares with.');
put(TST, 'test/golden/week_published_18nov.json', 'test/golden/week_published_18nov.json', 'source/test/golden/week_published_18nov.json', 'The same record for the page as published on 18 Nov, before the numbers were moved.');

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
