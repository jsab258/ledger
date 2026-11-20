// LEDGER rule piece: money. The two pots (the pocket, clean; the tin, night money), earning and paying, the wash
// at the count with Sheila, the week's rent, running costs and wages, the alibi fare, the inspection's reading of
// the book, and money in words. DESIGN section 9; ER-MONEY-01 to 04. Pure: plain data in, plain data out.
// Every function takes the numbers table last (default: the one tuning table), so a port hands in its own copy.
import { RULES } from '../../rules.js';

const OLD = RULES.money; // the prototype's own numbers (rules.js)
const NEW = RULES.game.econ.money; // the one-shot's (game/tune/econ.js)
export const TABLE = Object.assign({}, OLD, NEW);

const ONES = ['nought', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
const TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
const HUNDRED = ONES.length * (TENS.length / 2), // 100, said without writing it
  THOUSAND = HUNDRED * TENS.length;
function words(n) {
  n = Math.floor(n);
  if (n < ONES.length) return ONES[n];
  if (n < HUNDRED) return TENS[Math.floor(n / TENS.length)] + (n % TENS.length ? '-' + ONES[n % TENS.length] : '');
  if (n < THOUSAND) return ONES[Math.floor(n / HUNDRED)] + ' hundred' + (n % HUNDRED ? ' and ' + words(n % HUNDRED) : '');
  return words(Math.floor(n / THOUSAND)) + ' thousand' + (n % THOUSAND ? (n % THOUSAND < HUNDRED ? ' and ' : ' ') + words(n % THOUSAND) : '');
}
// "eighteen pounds", "twenty-three pounds fifty", "eighty pence", "nothing"
export function sumInWords(pence) {
  pence = Math.round(Math.abs(pence));
  const l = Math.floor(pence / HUNDRED),
    d = pence % HUNDRED;
  if (!pence) return 'nothing';
  if (!l) return words(d) + ' pence';
  return words(l) + (l === 1 ? ' pound' : ' pounds') + (d ? ' ' + words(d) : '');
}

// Paying. Night money goes first unless the thing must be paid clean (rent, wages, a shop that gives a receipt).
// Returns the pots after, whether it was paid, and the flows it made.
export function pay(pots, pence, cleanOnly, why) {
  pence = Math.round(pence);
  const out = { ok: false, pots: { clean: pots.clean, dirty: pots.dirty }, flows: [] };
  if (!(pence > 0)) return Object.assign(out, { ok: pence === 0 });
  if (cleanOnly ? pots.clean < pence : pots.clean + pots.dirty < pence) return out;
  const fromTin = cleanOnly ? 0 : Math.min(pots.dirty, pence),
    fromPocket = pence - fromTin;
  out.ok = true;
  out.pots.dirty -= fromTin;
  out.pots.clean -= fromPocket;
  if (fromTin) out.flows.push({ from: 'tin', to: 'world', pence: fromTin, dirty: true, why: why || 'paid' });
  if (fromPocket) out.flows.push({ from: 'pocket', to: 'world', pence: fromPocket, dirty: false, why: why || 'paid' });
  return out;
}
export function earn(pots, pence, dirty, why) {
  pence = Math.round(pence);
  const out = { pots: { clean: pots.clean, dirty: pots.dirty }, flows: [] };
  if (!(pence > 0)) return out;
  if (dirty) out.pots.dirty += pence;
  else out.pots.clean += pence;
  out.flows.push({ from: 'world', to: dirty ? 'tin' : 'pocket', pence, dirty: !!dirty, why: why || 'earned' });
  return out;
}

// The wash. The fare book hides a fixed sum plus a share of the fares really driven since the last wash, plus a
// share of what the firm's own drivers took, plus what his fronts add (DESIGN 9; ADDENDUM A15).
export function washCap(sinceWashPence, firmFaresPence, frontsExtraPence, T = TABLE) {
  return Math.round(
    T.washedSafelyPence +
      (sinceWashPence || 0) * T.washedSafelyShareOfFares +
      (firmFaresPence || 0) * T.firmFaresCountForTheWashShare +
      (frontsExtraPence || 0),
  );
}
// ER-MONEY-04: what Sheila says before anything goes through. over > 0 means the books would go off.
export function washWarning(tinPence, capPence) {
  const over = Math.max(0, Math.round(tinPence - capPence));
  return {
    over,
    warns: over > 0,
    words:
      tinPence <= 0
        ? 'There is nothing in the tin to put through.'
        : over > 0
          ? `The book will hide ${sumInWords(capPence)}. Put it all through and it is ${sumInWords(over)} over: the books will not add up.`
          : `It fits behind the fares. ${cap(sumInWords(tinPence))} will go through clean.`,
  };
}
// Putting the tin through. all: the whole tin (the books go off by what is over); otherwise only what fits.
export function wash(pots, capPence, all) {
  const tin = Math.max(0, pots.dirty),
    amt = all ? tin : Math.min(tin, Math.max(0, capPence)),
    over = Math.max(0, amt - Math.max(0, capPence));
  return {
    pots: { clean: pots.clean + amt, dirty: pots.dirty - amt },
    washed: amt,
    booksOffAdded: over,
    left: tin - amt,
    flows: amt ? [{ from: 'tin', to: 'pocket', pence: amt, dirty: false, why: over ? 'the wash, over what the book hides' : 'the wash' }] : [],
  };
}

// The week's fixed costs (2.7.4): what falls due, when, and from which pot.
export function weekCosts(drivers, T = TABLE) {
  return [
    { what: 'running costs', pence: T.runningCostsPence, dayIndex: T.runningCostsDueDayIndex, hour: T.runningCostsDueHour, cleanOnly: true, to: 'the garage and the radio' },
    { what: 'wages', pence: drivers * T.driverWagePerWeekPence, dayIndex: T.wagesPaidDayIndex, hour: T.wagesPaidHour, cleanOnly: true, to: 'the drivers', fromTakings: true },
    { what: 'rent', pence: T.rentPence, dayIndex: T.rentDueDayIndex, hour: T.rentLateFromHour, cleanOnly: true, to: 'Mrs Rennison' },
  ];
}
// What the firm's own drivers bring in over a week, the wages out of it, and what is left for his pocket at the
// count. A short week (a driver gone, a car off the road) gives less; wages are met first from the takings and
// any shortfall comes from his pocket.
export function firmWeek(drivers, workingDaysEach, T = TABLE) {
  const takings = Math.round(drivers * workingDaysEach * T.driverTakesPerWorkingDayPence),
    wages = drivers * T.driverWagePerWeekPence;
  return { takings, wages, toPocket: Math.max(0, takings - wages), shortFromPocket: Math.max(0, wages - takings) };
}
// One scripted week of clean money (ER-MONEY-03). plan: { faresPerDay: [Mon..Sun counts], farePence, paysRent }.
// Returns the pocket where it matters, and whether Friday's rent was met when it fell due.
export function scriptedWeek(plan, T = TABLE) {
  let pocket = T.startsWithPocketPence;
  const lines = [];
  let rentPaid = false,
    costsPaid = false;
  const firm = firmWeek(T.driversAtTheStart, T.driverWorkingDaysPerWeek, T);
  for (let d = 0; d < T.weekLengthDays; d++) {
    const fares = (plan.faresPerDay && plan.faresPerDay[d]) || 0;
    if (d === T.runningCostsDueDayIndex) {
      costsPaid = pocket >= T.runningCostsPence;
      if (costsPaid) pocket -= T.runningCostsPence;
      lines.push({ day: d, what: 'running costs', paid: costsPaid, pocket });
    }
    if (d === T.wagesPaidDayIndex && firm.shortFromPocket) {
      pocket -= Math.min(pocket, firm.shortFromPocket);
      lines.push({ day: d, what: 'wages short', pocket });
    }
    if (fares) {
      pocket += fares * (plan.farePence || 0);
      lines.push({ day: d, what: 'fares', count: fares, pocket });
    }
    if (d === T.rentDueDayIndex) {
      rentPaid = plan.paysRent !== false && pocket >= T.rentPence;
      if (rentPaid) pocket -= T.rentPence;
      lines.push({ day: d, what: 'rent', paid: rentPaid, pocket });
    }
    if (d === T.weekCountDayIndex) {
      pocket += firm.toPocket;
      lines.push({ day: d, what: 'the firm after wages', pocket });
    }
  }
  return { rentPaid, costsPaid, pocketAtEnd: pocket, lines };
}

// The alibi fare (DESIGN 9, new): a fare written in the book for an hour he was somewhere else is a lie in the
// book. bookMinute: the hour written; seenElsewhere: [{ minute, place }] where he really was and was seen.
export function alibiFare(bookMinute, driven, seenElsewhere, T = TABLE) {
  if (driven) return { lie: false, holds: true, why: 'he drove it', needsSomeoneToHoldItUp: false };
  const clash = (seenElsewhere || []).find((s) => Math.abs(s.minute - bookMinute) <= T.alibiFareMinutesEitherSide);
  return {
    lie: true,
    holds: !clash,
    why: clash ? 'somebody saw him at ' + clash.place + ' at that hour' : 'nobody can say where he was',
    needsSomeoneToHoldItUp: true,
  };
}
// What the inspector finds (Act III). weeks: [{ booksOffPence, lies, liesBroken }]. The state is in words.
export function bookReads(weeks, T = TABLE) {
  const off = weeks.filter((w) => (w.booksOffPence || 0) > 0).length,
    lies = weeks.reduce((a, w) => a + (w.lies || 0), 0),
    broken = weeks.reduce((a, w) => a + (w.liesBroken || 0), 0),
    offPence = weeks.reduce((a, w) => a + (w.booksOffPence || 0), 0);
  const state =
    off <= T.booksHoldWithOffWeeksAtMost && !broken && lies <= T.booksThinWithLiesAtMost
      ? 'hold'
      : off <= T.booksThinWithOffWeeksAtMost && !broken
        ? 'thin'
        : 'off';
  return {
    state,
    weeksOff: off,
    offPence,
    lies,
    liesBroken: broken,
    words:
      state === 'hold'
        ? 'The books add up, week on week.'
        : state === 'thin'
          ? `The books hold if nobody leans on them: ${off === 1 ? 'one week does' : words(off) + ' weeks do'} not add up.`
          : 'The books do not stand.',
  };
}
// ER-MONEY-02: what he has and what is owed by Friday, in words. due: [{ what, pence, paid }].
export function moneyInWords(pots, due, T = TABLE) {
  const owed = (due || []).filter((d) => !d.paid && d.pence >= T.owesInWordsFromPence);
  const total = owed.reduce((a, d) => a + d.pence, 0);
  const short = Math.max(0, total - pots.clean);
  return {
    has: `${cap(sumInWords(pots.clean))} in his pocket${pots.dirty > 0 ? ', and ' + sumInWords(pots.dirty) + ' in the tin that he cannot explain' : ''}.`,
    owes: owed.length ? `${cap(sumInWords(total))} to find by Friday: ${owed.map((d) => d.what + ' ' + sumInWords(d.pence)).join(', ')}.` : 'Nothing owed this week.',
    short: owed.length ? (short ? `He is ${sumInWords(short)} short of it.` : 'He has it.') : '',
    shortPence: short,
  };
}
const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);

export const PIECE = {
  name: 'money',
  fns: { sumInWords, pay, earn, washCap, washWarning, wash, weekCosts, firmWeek, scriptedWeek, alibiFare, bookReads, moneyInWords },
};
