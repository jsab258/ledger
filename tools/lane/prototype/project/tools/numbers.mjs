// Numbers and the rules table.
//   node tools/numbers.mjs left             every number still written outside src/rules.js, file by file, and a
//                                           pass or fail against tools/numbers_kept.json (the count that may stay)
//   node tools/numbers.mjs list <file>      the numbers in one file, in order, each with its place in the line
//   node tools/numbers.mjs apply <names>    move numbers into src/rules.js under the names given (see below)
// A names file: "@file src/x.js", "@alias section NAME" (the const the file reads that section through),
// "@section section" (the section for bare names), "@default -i" (what unlisted numbers are), then one line
// per number: "<index> <name>" or "<index> section.name", or a reason to leave it where it is:
//   -u a unit conversion (60 minutes, 1440 minutes in a day)   -i an index, a count of things, plain arithmetic
//   -t text and layout                                         -g a place on the map
//   -c how the camera and the controls feel                    -a how people and things look
// The value written into rules.js is the number's own text, so a move cannot change a value.
import fs from 'fs';
import * as acorn from 'acorn';

const TRIVIAL = new Set(['0', '1', '2']);
export const RULE_FILES = ['seeing', 'gossip', 'events', 'ledger', 'money', 'fares', 'jobs', 'police', 'routines', 'talk', 'talk_lines', 'scenes', 'work', 'fight', 'clock', 'kinds', 'cast', 'measures', 'light', 'state', 'player', 'drive'].map((f) => `src/${f}.js`);

export function literals(src) {
  const ast = acorn.parse(src, { ecmaVersion: 'latest', sourceType: 'module', locations: true });
  const out = [];
  let lastImportEnd = 0;
  (function walk(n) {
    if (!n || typeof n.type !== 'string') return;
    if (n.type === 'ImportDeclaration') lastImportEnd = Math.max(lastImportEnd, n.end);
    if (n.type === 'Literal' && typeof n.value === 'number' && !TRIVIAL.has(n.raw)) out.push({ start: n.start, end: n.end, raw: n.raw, line: n.loc.start.line });
    for (const k in n) {
      const v = n[k];
      if (Array.isArray(v)) v.forEach(walk);
      else if (v && typeof v.type === 'string') walk(v);
    }
  })(ast);
  out.sort((a, b) => a.start - b.start);
  return { out, lastImportEnd };
}
const flat = (s) => s.replace(/\s+/g, ' ');

const [, , mode, arg] = process.argv;
if (mode === 'list') {
  const src = fs.readFileSync(arg, 'utf8'), { out } = literals(src);
  out.forEach((l, i) => console.log(`${i} ${flat(src.slice(Math.max(0, l.start - 46), l.start)).slice(-44)}«${l.raw}»${flat(src.slice(l.end, l.end + 30)).slice(0, 26)}`));
} else if (mode === 'apply') {
  const { RULES } = await import('../src/rules.js');
  const spec = fs.readFileSync(arg, 'utf8').split('\n').map((x) => x.trim()).filter((x) => x && !x.startsWith('#'));
  let file = null, section = null, dflt = '-i';
  const alias = {}, named = new Map();
  for (const line of spec) {
    const [a, b, c] = line.split(/\s+/);
    if (a === '@file') file = b;
    else if (a === '@alias') alias[b] = c;
    else if (a === '@section') section = b;
    else if (a === '@default') dflt = b;
    else named.set(+a, b);
  }
  let src = fs.readFileSync(file, 'utf8');
  const { out, lastImportEnd } = literals(src);
  const add = [], kept = {}, usedSec = new Set(), seen = {};
  const edits = [];
  out.forEach((l, i) => {
    const n = named.get(i) || dflt;
    if (n.startsWith('-')) return void (kept[n.slice(1) || 'i'] = (kept[n.slice(1) || 'i'] || 0) + 1);
    const [sec, name] = n.includes('.') ? n.split('.') : [section, n];
    if (!sec || !alias[sec]) throw new Error(`no section or alias for #${i} ${n}`);
    const key = sec + '.' + name, have = RULES[sec] && RULES[sec][name];
    if (seen[key] !== undefined && seen[key] !== l.raw) throw new Error(`${key} given two values: ${seen[key]} and ${l.raw} (#${i})`);
    if (have !== undefined && Number(l.raw) !== have) throw new Error(`${key} is already ${have} in rules.js, not ${l.raw} (#${i})`);
    if (have === undefined && seen[key] === undefined) add.push({ sec, name, raw: l.raw });
    seen[key] = l.raw;
    usedSec.add(sec);
    edits.push({ start: l.start, end: l.end, text: `${alias[sec]}.${name}` });
  });
  for (const e of edits.sort((a, b) => b.start - a.start)) src = src.slice(0, e.start) + e.text + src.slice(e.end);
  let head = '';
  if (!/import \{[^}]*\bRULES\b[^}]*\} from '\.\/rules\.js'/.test(src)) head += `\nimport { RULES } from './rules.js';`;
  for (const sec of usedSec) if (!new RegExp(`\\b${alias[sec]} = RULES\\.${sec}\\b`).test(src)) head += `\nconst ${alias[sec]} = RULES.${sec};`;
  src = src.slice(0, lastImportEnd) + head + src.slice(lastImportEnd);
  fs.writeFileSync(file, src);
  let rules = fs.readFileSync('src/rules.js', 'utf8');
  for (const a of add) {
    const at = rules.indexOf(`\n  ${a.sec}: {`);
    if (at < 0) {
      const end = rules.lastIndexOf('\n};');
      rules = rules.slice(0, end) + `\n\n  ${a.sec}: {\n    ${a.name}: ${a.raw},\n  },` + rules.slice(end);
    } else {
      const close = rules.indexOf('\n  },', at);
      rules = rules.slice(0, close) + `\n    ${a.name}: ${a.raw},` + rules.slice(close);
    }
  }
  fs.writeFileSync('src/rules.js', rules);
  const K = fs.existsSync('tools/numbers_kept.json') ? JSON.parse(fs.readFileSync('tools/numbers_kept.json', 'utf8')) : {};
  K[file] = kept;
  fs.writeFileSync('tools/numbers_kept.json', JSON.stringify(K, null, 1) + '\n');
  console.log(`${file}: ${edits.length} numbers now read from rules.js (${add.length} new names), ${Object.entries(kept).map(([k, v]) => v + ' kept -' + k).join(', ') || 'none kept'}`);
} else if (mode === 'left') {
  const K = JSON.parse(fs.readFileSync('tools/numbers_kept.json', 'utf8'));
  const WHY = { u: 'unit conversions', i: 'indexes, counts and plain arithmetic', t: 'text and layout', g: 'places on the map', c: 'camera and controls', a: 'how people and things look' };
  let bad = 0;
  for (const f of RULE_FILES) {
    const src = fs.readFileSync(f, 'utf8'), { out } = literals(src);
    const allowed = Object.values(K[f] || {}).reduce((a, b) => a + b, 0);
    const why = Object.entries(K[f] || {}).map(([k, v]) => `${v} ${WHY[k] || k}`).join(', ');
    const ok = out.length === allowed;
    if (!ok) bad++;
    console.log(`${ok ? 'ok  ' : 'FAIL'} ${f.padEnd(22)} ${String(out.length).padStart(4)} left${why ? ' (' + why + ')' : ''}${ok ? '' : ' | the record allows ' + allowed}`);
    if (process.argv.includes('--show') || !ok) out.forEach((l) => console.log(`       ${l.line}: ${flat(src.slice(Math.max(0, l.start - 40), l.end + 24))}`));
  }
  console.log(bad ? 'FAIL: numbers outside src/rules.js that the record does not allow' : 'PASS: every number outside src/rules.js is one the record allows');
  process.exit(bad ? 1 : 0);
} else console.log('usage: node tools/numbers.mjs left [--show] | list <file> | apply <names file>');
