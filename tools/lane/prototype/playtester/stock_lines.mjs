// The game's stock talk lines, read from the readable source, so the playtester can tell a person's own
// line from a line anyone would say. Prints one JSON object:
//   generic:  lines any person may say (FB pools, BYES, the default greeting 'Aye?', street barks)
//   own:      person id -> that person's own lines (GREET, FBOWN)
// Usage: node stock_lines.mjs <project/src folder>
// Written by the cloud lane, 18 Nov 2026. Reads the source; changes nothing in the game.
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';

const src = path.resolve(process.argv[2] || path.join(path.dirname(new URL(import.meta.url).pathname), '..', 'project', 'src'));

// a top-level `const NAME = {...}` or `[...]` literal in a source file, evaluated on its own
function literal(file, name) {
  const text = fs.readFileSync(path.join(src, file), 'utf8');
  const at = text.search(new RegExp('(?:export\\s+)?const\\s+' + name + '\\s*=\\s*[\\[{]'));
  if (at < 0) throw new Error(name + ' not found in ' + file);
  let i = text.indexOf('=', at) + 1;
  while (/\s/.test(text[i])) i++;
  const open = text[i], close = open === '{' ? '}' : ']';
  let depth = 0, q = null;
  for (let j = i; j < text.length; j++) {
    const c = text[j];
    if (q) {
      if (c === '\\') { j++; continue; }
      if (c === q) q = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { q = c; continue; }
    if (c === open) depth++;
    else if (c === close && --depth === 0) return Function('return (' + text.slice(i, j + 1) + ')')();
  }
  throw new Error(name + ': unbalanced literal in ' + file);
}

const flat = (o) => (Array.isArray(o) ? o.flatMap(flat) : o && typeof o === 'object' ? Object.values(o).flatMap(flat) : typeof o === 'string' ? [o] : []);

const lines = await import(pathToFileURL(path.join(src, 'talk_lines.js')).href);
const cast = await import(pathToFileURL(path.join(src, 'cast.js')).href);
const FBOWN = literal('talk_lines.js', 'FBOWN');
const BYES = literal('talk.js', 'BYES');

const own = {};
for (const [id, v] of Object.entries(lines.GREET)) own[id] = (own[id] || []).concat(flat(v));
for (const [id, v] of Object.entries(FBOWN)) own[id] = (own[id] || []).concat(flat(v));
const keeperBarks = {};
for (const k of cast.KEEPERS) if (k.bark) keeperBarks[k.id] = flat(k.bark);

console.log(
  JSON.stringify({
    generic: Array.from(new Set(flat(lines.FB).concat(BYES, ['Aye?'], flat(cast.BARKS)))),
    own,
    keeperBarks,
    cast: cast.CAST.map((c) => ({ id: c.id, name: c.name, sex: c.sex, age: c.age, role: c.role, desc: c.desc })),
    keepers: cast.KEEPERS.map((k) => ({ id: k.id, desc: k.desc, sex: k.sex })),
  }),
);
