// LEDGER rule piece: Act III, the inspection week (DESIGN 16). Pure.
// The inspector brings one item each morning; Tom produces it or asks for it in writing. Each morning is one
// deciding step, graded by what the books hold. B, the books:
//   booksOffPence (night money put through beyond what the fares could hide), overWashes (how many times),
//   alibiFares (fares written for hours he was elsewhere), wagesOwedPence, faresDriven
// T: game/tune/acts.js.
import { TUNE } from '../tune/acts.js';
export const ITEMS = [
  { id: 'farebook', name: 'the fare book for the quarter' },
  { id: 'takings', name: 'the takings against the fares' },
  { id: 'carlog', name: "the cars' log, hour by hour" },
  { id: 'wages', name: 'the wage sheets' },
  { id: 'paidin', name: 'the paying-in book from the bank' },
];
const b = (B) => Object.assign({ booksOffPence: 0, overWashes: 0, alibiFares: 0, wagesOwedPence: 0, faresDriven: 0 }, B);
// 'holds' | 'thin' | 'fails' for one item.
export function gradeItem(itemId, B0, T) {
  const B = b(B0);
  switch (itemId) {
    case 'farebook':
      return B.faresDriven > 0 ? 'holds' : 'thin'; // a firm whose owner never drove: the book is honest and bare
    case 'takings':
      return B.booksOffPence <= T.booksOffHoldsAtMostPence ? 'holds' : B.booksOffPence <= T.booksOffThinAtMostPence ? 'thin' : 'fails';
    case 'carlog':
      return B.alibiFares >= T.alibiFaresFailFrom ? 'fails' : B.alibiFares >= T.alibiFaresThinFrom ? 'thin' : 'holds';
    case 'wages':
      return B.wagesOwedPence >= T.wagesOwedFailFromPence ? 'fails' : 'holds';
    case 'paidin':
      return B.overWashes >= 2 ? 'fails' : B.overWashes === 1 ? 'thin' : 'holds';
  }
  return 'holds';
}
// One morning. answer: 'produce' | 'writing'. In writing puts the item off a day; it is allowed a set number of
// times, after which the inspector takes the item as it stands and notes the delay (one step worse, never better).
export function morning(itemId, answer, B, writingsSoFar, T) {
  const g = gradeItem(itemId, B, T);
  if (answer === 'writing') {
    if (writingsSoFar < T.inWritingAllowedTimes) return { grade: null, putOff: true, manner: 'patient' };
    const worse = g === 'holds' ? 'thin' : 'fails';
    return { grade: worse, putOff: false, manner: worse === 'fails' ? 'cold' : 'careful' };
  }
  return { grade: g, putOff: false, manner: g === 'holds' ? 'courteous' : g === 'thin' ? 'careful' : 'cold' };
}
// The week's result from the grades given. The sign comes before it decides: the manner after each grade.
export function result(grades, T) {
  const fails = grades.filter((g) => g === 'fails').length,
    thins = grades.filter((g) => g === 'thin').length;
  const sunk = fails + Math.floor(thins / T.thinsThatCountAsAFail) >= T.failsThatSinkTheBooks;
  return { booksHold: !sunk, fails, thins, manner: sunk ? 'cold' : fails || thins ? 'careful' : 'courteous' };
}
// Where the lie holds: what Sheila says if she trusts him. The items, safest first.
export function whereItHolds(B, T) {
  const rank = { holds: 0, thin: 1, fails: 2 };
  return ITEMS.map((i) => ({ id: i.id, grade: gradeItem(i.id, B, T) })).sort((x, y) => rank[x.grade] - rank[y.grade]);
}
export const PIECE = {
  name: 'act_inspection',
  fns: {
    gradeItem: (i, B) => gradeItem(i, B, TUNE),
    morning: (i, a, B, n) => morning(i, a, B, n, TUNE),
    result: (g) => result(g, TUNE),
    whereItHolds: (B) => whereItHolds(B, TUNE),
    itemIds: () => ITEMS.map((i) => i.id),
  },
};
