// The same week, exactly. One full scripted week (week_bot.mjs) is played with a fixed seed on a clock the
// test owns, and everything the save holds at the end (events, memories, money, debts, the Ledger's entries,
// the measures) is compared, part by part, with the record in test/golden/week.json.
// A change that is meant to alter nothing (moving a number into rules.js, renaming, tidying) must leave this
// test passing. A change that is meant to alter the week must say so and write a new record.
//   node test/same_week.mjs                 compare dist/ with test/golden/week.json
//   node test/same_week.mjs --write         play the week and write the record
//   DIST=<folder> GOLDEN=<file> SEED=<n>    another build, another record, another seed
import fs from 'fs';
import crypto from 'crypto';
import { launch } from './harness.mjs';
import { playWeek } from './week_bot.mjs';

const DIST = process.env.DIST || 'dist', GOLDEN = process.env.GOLDEN || 'test/golden/week.json', write = process.argv.includes('--write');
const old = fs.existsSync(GOLDEN) ? JSON.parse(fs.readFileSync(GOLDEN, 'utf8')) : null;
const SEED = +(process.env.SEED || (old && old.seed) || 19901015);
const sha = (x) => crypto.createHash('sha256').update(typeof x === 'string' ? x : JSON.stringify(x)).digest('hex').slice(0, 20);

const h = await launch({ port: +(process.env.PORT || 8851), dist: DIST, seed: SEED, width: 1280, height: 720 });
const lines = [];
const r = await playWeek(h, { log: (...a) => lines.push(a.join(' ')), outDir: 'out/same_week' });
const text = await h.ev(() => LEDGER.saveText());
const gossip = await h.ev(() => (LEDGER.gossip ? LEDGER.gossip() : null)); // the gossip table of this same week
const errors = h.errors.slice();
await h.close();
const save = JSON.parse(text);
const parts = {};
// the one-shot: `at` is the wall clock at the save, no part of the week. Since the real town's code opens off the
// clock, the test's own clock can stand a few seconds apart between two runs (one waiting timer taken early or
// late), with every part of the week the same; so `at` is left out of the record.
for (const k of Object.keys(save).sort()) if (k !== 'at') parts[k] = sha(save[k]);
const now = {
  seed: SEED,
  ended: !!r.ended,
  whole: sha(parts),
  parts,
  counts: {
    events: (save.events || []).length,
    storiesPassedOn: (save.transfers || []).length,
    ledgerEntries: r.book ? r.book.length : null,
    pocketPence: save.money && save.money.clean,
    tinPence: save.money && save.money.dirty,
    ledgerOpens: r.measures && r.measures.ledgerOpens,
    notedLinesShown: r.measures && r.measures.notedLinesShown,
    talks: r.measures && r.measures.talks,
    gameMinute: save.t,
  },
};
fs.mkdirSync('out/same_week', { recursive: true });
fs.writeFileSync('out/same_week/save.json', JSON.stringify(save, null, 1));
fs.writeFileSync('out/same_week/log.txt', lines.join('\n'));
if (gossip) fs.writeFileSync(process.env.GOSSIP_OUT || 'out/same_week/gossip.json', JSON.stringify(gossip, null, 1));
console.log(`seed ${SEED} | ${DIST} | week ended: ${now.ended} | whole ${now.whole} | ${JSON.stringify(now.counts)}`);
if (r.failed || errors.length) console.log('the script failed:', r.failed || '', errors.slice(0, 3).join(' | '));
if (write) {
  fs.writeFileSync(GOLDEN, JSON.stringify(now, null, 1) + '\n');
  console.log('wrote', GOLDEN);
  process.exit(r.failed || errors.length || !now.ended ? 1 : 0);
}
if (!old) { console.log('no record at', GOLDEN, '(run with --write)'); process.exit(1); }
const differ = Object.keys({ ...old.parts, ...parts }).filter((k) => old.parts[k] !== parts[k]);
if (differ.length) console.log('DIFFERENT in:', differ.join(', '), '| record', JSON.stringify(old.counts));
const ok = !differ.length && old.whole === now.whole && now.ended && !r.failed && !errors.length;
console.log(ok ? 'PASS: the same week, part for part (' + Object.keys(parts).length + ' parts)' : 'FAIL');
process.exit(ok ? 0 : 1);
