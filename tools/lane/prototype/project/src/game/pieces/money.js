// RULE PIECE: money (DESIGN 9). Pure: plain data in, plain data out. Unreal ports it and passes test/cases/money.json.
// Every pound is a flow between two named pots, so no money comes from nowhere (ER-MONEY-01):
//   pots: 'world' (everybody else), 'pocket' (clean money on him and in the fare book), 'tin' (night money)
import { TUNE as T } from '../tune/econ.js';

const fresh = () => ({ pocket: T.startsWithPocketPence, tin: 0, sinceWash: 0, booksOff: 0, flows: [{ from: 'world', to: 'pocket', pence: T.startsWithPocketPence, why: 'what he came with' }] });
// One movement of money. Refused, with the reason and nothing changed, when the pot does not hold it.
function post(book, flow) {
  const { from, to, pence, why } = flow;
  if (!(pence > 0) || Math.round(pence) !== pence) return { ok: false, why: 'not a whole sum of pence', book };
  if (from === to || !['world', 'pocket', 'tin'].includes(from) || !['world', 'pocket', 'tin'].includes(to)) return { ok: false, why: 'no such pots', book };
  if (!why) return { ok: false, why: 'every flow says what it was for', book };
  if (from !== 'world' && book[from] < pence) return { ok: false, why: 'the ' + from + ' does not hold it', book };
  const b = Object.assign({}, book, { flows: book.flows.concat([{ from, to, pence, why }]) });
  if (from !== 'world') b[from] -= pence;
  if (to !== 'world') b[to] += pence;
  return { ok: true, why: null, book: b };
}
// ER-MONEY-01: each pot equals the sum of its flows.
function balances(book) {
  const sum = { pocket: 0, tin: 0 };
  for (const f of book.flows) {
    if (f.to in sum) sum[f.to] += f.pence;
    if (f.from in sum) sum[f.from] -= f.pence;
  }
  return { pocket: sum.pocket, tin: sum.tin, holds: sum.pocket === book.pocket && sum.tin === book.tin };
}
// What the fare book can hide: ten pounds, plus a share of the fares really driven since the last wash, plus the fronts.
const washCap = (sinceWashPence, fronts = 0) => T.washedSafelyPence + Math.round(sinceWashPence * T.washedSafelyShareOfFares) + fronts * T.frontAddsWashPencePerWeek;
// The count with Sheila. She warns before a wash puts the books off (ER-MONEY-04): ask first with confirm false.
function wash(book, pence, fronts = 0, confirm = false) {
  const amt = Math.min(pence, book.tin),
    cap = washCap(book.sinceWash, fronts),
    over = Math.max(0, amt - cap);
  if (amt <= 0) return { done: false, warn: false, over: 0, cap, book };
  if (over > 0 && !confirm) return { done: false, warn: true, over, cap, book };
  const r = post(book, { from: 'tin', to: 'pocket', pence: amt, why: 'put through the fare book' });
  const b = Object.assign({}, r.book, { sinceWash: 0, booksOff: book.booksOff + over });
  return { done: true, warn: over > 0, over, cap, book: b };
}
const fare = (metres) => Math.round((T.fareFlagFallPence + metres * T.farePencePerMetre) / T.fareRoundedToPence) * T.fareRoundedToPence;
// The week's running costs: rent, each driver's wage, each car's upkeep.
const weekCosts = (cars, drivers) => T.rentPence + drivers * T.driverWagePencePerWeek + cars * T.carRunningPencePerWeek;
// What the firm's own drivers bring the book in a day without him (the lazy path).
const firmDay = (carsOnTheRoad, fareShare = 1) => Math.round(carsOnTheRoad * T.firmDrivesWithoutHimFaresPerCarPerDay * T.firmFareAveragePence * T.firmFareShareToTheBook * fareShare);
const rentState = (dayIndex, hour, paid) => (paid ? 'paid' : dayIndex < T.rentDueDayIndex ? 'not yet due' : dayIndex === T.rentDueDayIndex && hour < T.rentLateFromHour ? 'due today' : 'late');
// Money in words, never to the penny (ER-MONEY-02): "about twenty-three pounds fifty".
const ONES = ['nought', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
const TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
function number(n) {
  if (n < 20) return ONES[n];
  if (n < 100) return TENS[Math.floor(n / 10)] + (n % 10 ? '-' + ONES[n % 10] : '');
  if (n < 1000) return ONES[Math.floor(n / 100)] + ' hundred' + (n % 100 ? ' and ' + number(n % 100) : '');
  return number(Math.floor(n / 1000)) + ' thousand' + (n % 1000 ? (n % 1000 < 100 ? ' and ' : ' ') + number(n % 1000) : '');
}
function words(pence) {
  const p = Math.round(pence / T.roundWordsToPence) * T.roundWordsToPence;
  if (p === 0) return pence > 0 ? 'a few pence' : 'nothing';
  const pounds = Math.floor(p / 100),
    rest = p % 100;
  const exact = p === pence ? '' : 'about ';
  if (!pounds) return exact + number(rest) + ' pence';
  return exact + number(pounds) + (pounds === 1 ? ' pound' : ' pounds') + (rest ? ' ' + number(rest) : '');
}
export const PIECE = { name: 'money', fns: { fresh, post, balances, washCap, wash, fare, weekCosts, firmDay, rentState, words } };
