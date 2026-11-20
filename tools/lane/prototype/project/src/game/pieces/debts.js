// LEDGER rule piece: Mickey's debt book. Five debts, five lessons (DESIGN 4): a debtor pays what his purse holds
// and the rest stays on the book (2.8.2); squeezing is told on the street, and so is letting a debt go. Pure.
import { RULES } from '../../rules.js';
const P = RULES.prices;
export const TABLE = RULES.game.econ.debts;

// The book as it is inherited.
export function book() {
  return {
    dennis: { owed: P.owedByIvesonPence, st: 'open', paid: 0 },
    wayne: { owed: P.owedByWaynePence, st: 'open', paid: 0 },
    darren: { owed: P.owedByDarrenPence, st: 'open', paid: 0 },
    lee: { owed: P.owedByLeePence, st: 'open', paid: 0 },
    julie: { owed: P.owedByJuliePence, st: 'open', paid: 0 },
  };
}
export const total = (b) => Object.keys(b).reduce((a, id) => a + (b[id].st === 'open' ? b[id].owed : 0), 0);

// Will he pay when asked in talk, without being fronted up? Fear, or goodwill on a small debt.
export function paysWhenAsked(debt, mind, T = TABLE) {
  if (!debt || debt.st !== 'open') return false;
  return mind.fear > T.paysWhenFearAbove || (mind.regard > T.paysWhenRegardAbove && debt.owed <= T.paysOnRegardOnlyWhenOwingAtMostPence);
}
// Collecting. how: 'asked' (he pays willingly), 'squeezed' (he gave way when fronted up or beaten), 'goods'
// (he pays in things: Wayne), 'word' (he pays in what he hears: Darren). He pays what the purse holds and no more;
// the rest stays on the book. Returns the debt after, the money that changes hands (night money: it goes in the
// tin), what else changes hands, and what the street will make of it.
export function collect(id, debt, how, pursePence, T = TABLE) {
  if (!debt || debt.st !== 'open' || debt.owed <= 0) return { debt, pence: 0, goods: 0, word: false, tells: null, said: 'Nothing stands against that name.' };
  const purse = Math.max(0, pursePence == null ? T.pursePence[id] || 0 : pursePence);
  let pence = 0,
    goods = 0,
    word = false;
  if (how === 'goods') goods = Math.min(debt.owed, T.goodsWorthPence[id] || 0);
  else if (how === 'word') {
    word = (T.wordWorthPence[id] || 0) > 0;
    goods = 0;
    pence = 0;
  } else pence = Math.min(debt.owed, purse);
  const off = pence + goods + (word ? Math.min(debt.owed, T.wordWorthPence[id] || 0) : 0),
    left = debt.owed - off,
    after = { owed: left, st: left > 0 ? 'open' : 'paid', paid: (debt.paid || 0) + off };
  const penniless = how === 'squeezed' && purse <= 0;
  return {
    debt: after,
    pence,
    goods,
    word,
    tells: off || penniless ? tells(how === 'squeezed' ? (penniless ? 'shamed' : 'squeezed') : 'paid', T) : null,
    said: penniless
      ? 'There is nothing in the purse. Squeezing gets shame and no money.'
      : left > 0
        ? 'Part paid. The rest stays on the book.'
        : 'Paid. Sheila can cross it through.',
  };
}
// Striking a debt out, for good.
export function strike(debt, T = TABLE) {
  if (!debt || debt.st !== 'open') return { debt, tells: null };
  return { debt: { owed: 0, st: 'forgiven', paid: debt.paid || 0, struck: debt.owed }, tells: tells('struck', T) };
}
// What each outcome is to the street: the kind of act, how it reads (-1 menace to 1 decent), and what it does to
// the debtor's own regard and fear.
export function tells(outcome, T = TABLE) {
  switch (outcome) {
    case 'squeezed':
      return { kind: 'debt_paid', reads: T.squeezedReadsMenace, regard: -T.regardLostWhenSqueezed, fear: T.fearAddedWhenSqueezed, street: 'he squeezed it out of them' };
    case 'shamed':
      return { kind: 'debt_shamed', reads: T.squeezedAPennilessOneReadsMenace, regard: -T.regardLostWhenSqueezed, fear: T.fearAddedWhenSqueezed, street: 'he leaned on somebody with nothing' };
    case 'struck':
      return { kind: 'debt_forgive', reads: T.struckOutReadsDecent, regard: T.regardAddedWhenStruckOut, fear: 0, street: 'he let a debt go' };
    default:
      return { kind: 'debt_paid', reads: T.paidQuietlyReads, regard: 0, fear: 0, street: 'the debt was paid' };
  }
}
// The lesson each debtor is (DESIGN 4), from the data: what a first visit can come to.
export function lesson(id, T = TABLE) {
  const purse = T.pursePence[id] || 0,
    owed = book()[id] ? book()[id].owed : 0;
  if (T.wordWorthPence[id]) return 'pays in what he hears';
  if (T.goodsWorthPence[id]) return 'pays in goods';
  if (purse <= 0) return 'cannot pay: mercy or shame';
  if (purse >= owed) return 'has the money and will not hand it over';
  return 'stands, and has a little';
}
// The book in words for the Ledger: one line a name.
export function lines(b) {
  return Object.keys(b).map((id) => ({ id, st: b[id].st, owed: b[id].owed, paid: b[id].paid || 0 }));
}

export const PIECE = { name: 'debts', fns: { book, total, paysWhenAsked, collect, strike, tells, lesson, lines } };
