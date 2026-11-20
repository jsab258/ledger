// RULE PIECE: debts (DESIGN 4, collections). Pure. Unreal ports it and passes test/cases/debts.json.
// A debtor pays what his purse holds and the rest stays on the book. Squeezing is told on the street; so is letting go.
import { TUNE as T } from '../tune/econ.js';

const book = () => Object.fromEntries(Object.entries(T.debts).map(([id, d]) => [id, { owed: d.owedPence, purse: d.pursePence, st: 'open', paid: 0 }]));
// how: 'ask' (take what he offers), 'squeeze' (fronted up and he gave way), 'forgive' (struck out), 'goods', 'words'
function collect(debt, how) {
  if (debt.st !== 'open' && debt.st !== 'part') return { debt, got: 0, kind: null, told: null, why: 'nothing open on this line' };
  if (how === 'forgive') return { debt: Object.assign({}, debt, { st: 'forgiven' }), got: 0, kind: null, told: 'let it go', why: null };
  if (how === 'words') return { debt: Object.assign({}, debt, { st: debt.st }), got: 0, kind: 'words', told: null, why: null };
  const got = Math.min(debt.purse, debt.owed);
  if (got <= 0) return { debt, got: 0, kind: null, told: how === 'squeeze' ? 'squeezed' : null, why: 'the purse is empty' };
  const left = debt.owed - got;
  const d = Object.assign({}, debt, { owed: left, purse: debt.purse - got, paid: debt.paid + got, st: left ? 'part' : 'paid' });
  return { debt: d, got, kind: how === 'goods' ? 'goods' : 'money', told: how === 'squeeze' ? 'squeezed' : null, why: null };
}
// What each of the five does when Tom comes for it: five debts, five lessons. Scripted, never rolled.
// approach: 'ask' | 'front' (the ladder's lower rungs) | 'night' (come back for it) | 'lean' (what he knows)
function answer(id, approach, s = {}) {
  const d = T.debts[id];
  if (!d) return { does: 'nothing', why: 'no such debt' };
  if (id === 'darren') return approach === 'front' ? { does: 'pays part', how: 'squeeze' } : { does: 'offers what he hears', how: 'words' };
  if (id === 'wayne') return approach === 'front' ? { does: 'pays part', how: 'squeeze' } : { does: 'offers goods from the back room', how: 'goods' };
  if (id === 'lee') return approach === 'ask' ? { does: 'refuses', how: null } : s.crewBeside ? { does: 'pays', how: 'squeeze' } : { does: 'stands', how: 'fight' };
  if (id === 'julie') return approach === 'front' ? { does: 'pays the little she has', how: 'squeeze', shame: true } : { does: 'cannot pay', how: null, mercy: true };
  // dennis: three keys (DESIGN 15, minute 47): front up his yard hand, the hut at night, or what he bought out of the burned warehouse
  if (approach === 'front') return s.yardHandDown ? { does: 'pays', how: 'squeeze' } : { does: 'sets his yard hand on him', how: 'fight' };
  if (approach === 'night') return { does: 'the hut holds it', how: 'break-in' };
  if (approach === 'lean') return s.knowsWarehouse ? { does: 'pays', how: 'ask' } : { does: 'laughs', how: null };
  return { does: 'refuses', how: null };
}
const regardAfter = (regard, told) => Math.max(-1, Math.min(1, regard + (told === 'squeezed' ? -T.squeezedRegardLost : told === 'let it go' ? T.forgivenRegardGained : 0)));
const totalOwed = (b) => Object.values(b).reduce((a, d) => a + (d.st === 'open' || d.st === 'part' ? d.owed : 0), 0);
export const PIECE = { name: 'debts', fns: { book, collect, answer, regardAfter, totalOwed } };
