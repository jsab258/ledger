// LEDGER rule piece: the flows ledger. No money from nowhere (2.7.7, ER-MONEY-01): every pound in the pocket or
// the tin traces through a sum of flows, each with a named other side and a reason. Pure.
// A flow: { from, to, pence, dirty, why, who? }. The pots are 'pocket' and 'tin'; anything else is the world, and
// the world's side must be named by `why` (a fare, a debt paid, rent) and may name a person in `who`.
import { RULES } from '../../rules.js';
export const TABLE = RULES.game.econ.flows;
const POTS = ['pocket', 'tin'];

// A flow is sound when it moves a whole, positive sum between two different sides, one of them a pot, with a reason.
export function sound(f) {
  if (!f || typeof f !== 'object') return { ok: false, why: 'not a flow' };
  if (!Number.isInteger(f.pence) || f.pence <= 0) return { ok: false, why: 'the sum must be whole pence above nothing' };
  if (!f.from || !f.to || f.from === f.to) return { ok: false, why: 'it needs two different sides' };
  if (!POTS.includes(f.from) && !POTS.includes(f.to)) return { ok: false, why: 'neither side is his pocket or the tin' };
  if (!f.why || !String(f.why).trim()) return { ok: false, why: 'money from nowhere: no reason given' };
  return { ok: true, why: '' };
}
// A book: { start: { pocket, tin }, sums: { 'from>to|why': pence }, lines: [flows, the newest last], count }.
export function open(startPocket, startTin) {
  return { start: { pocket: startPocket, tin: startTin || 0 }, sums: {}, lines: [], count: 0 };
}
// Add one flow. An unsound flow is refused and the book comes back unchanged, with why.
export function add(book, f, T = TABLE) {
  const s = sound(f);
  if (!s.ok) return { book, ok: false, why: s.why };
  const key = f.from + '>' + f.to + '|' + f.why;
  const sums = Object.assign({}, book.sums);
  sums[key] = (sums[key] || 0) + f.pence;
  const lines = book.lines.concat([f]).slice(-T.keepsLines);
  return { book: { start: book.start, sums, lines, count: book.count + 1 }, ok: true, why: '' };
}
// What the pots must hold by the book.
export function balance(book) {
  const b = { pocket: book.start.pocket, tin: book.start.tin };
  for (const key in book.sums) {
    const [sides] = key.split('|'),
      [from, to] = sides.split('>');
    if (from in b) b[from] -= book.sums[key];
    if (to in b) b[to] += book.sums[key];
  }
  return b;
}
// The check: the pots against the book. ok only when both agree to the penny.
export function check(book, pots) {
  const b = balance(book),
    pocket = Math.round(pots.clean - b.pocket),
    tin = Math.round(pots.dirty - b.tin);
  return { ok: pocket === 0 && tin === 0, pocketUnexplained: pocket, tinUnexplained: tin };
}
// Where the money came from and went, largest first: for the Ledger's money page and the end screen.
export function totals(book) {
  const inn = {},
    out = {};
  for (const key in book.sums) {
    const [sides, why] = key.split('|'),
      [from, to] = sides.split('>');
    if (POTS.includes(from) && POTS.includes(to)) continue;
    if (POTS.includes(to)) inn[why] = (inn[why] || 0) + book.sums[key];
    else out[why] = (out[why] || 0) + book.sums[key];
  }
  const list = (o) => Object.keys(o).sort((a, b) => o[b] - o[a] || (a < b ? -1 : 1)).map((why) => ({ why, pence: o[why] }));
  return { in: list(inn), out: list(out), washed: Object.keys(book.sums).filter((k) => k.startsWith('tin>pocket|')).reduce((a, k) => a + book.sums[k], 0) };
}

export const PIECE = { name: 'flows', fns: { sound, open, add, balance, check, totals } };
