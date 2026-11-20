// LEDGER rule piece: the firm's growth, the board, fronts and rounds (DESIGN 12, 14; ADDENDUM A14, A15). Pure.
// firm: { cars: [{ id, driver, rank, off }], ranks: { id: { held, days } }, accounts: { id: true }, fronts: { id: { man } },
//         rounds: { id: { man } }, unpaid: { driverId: weeks } }
import { TUNE as F } from '../tune/firm.js';

function buyCar(firm, moneyPence) {
  if (firm.cars.length >= F.carsAtMost) return { ok: false, why: 'The yard will not hold another.' };
  if (moneyPence < F.carPricePence) return { ok: false, why: 'He has not got it.' };
  const id = F.carNames[firm.cars.length];
  return { ok: true, why: '', pence: F.carPricePence, car: { id, driver: null, rank: null, off: false } };
}
// A car joins the board and the ranks only once somebody drives it.
function crew(firm, carId, driverId) {
  if (firm.cars.some((c) => c.driver === driverId && c.id !== carId)) return { ok: false, why: 'He is on another car.' };
  const cars = firm.cars.map((c) => (c.id === carId ? Object.assign({}, c, { driver: driverId, rank: c.rank || 'mickeys' }) : c));
  return { ok: cars.some((c) => c.id === carId), why: '', cars };
}
function place(firm, carId, rankId) {
  if (!F.ranks[rankId]) return { ok: false, why: 'No such rank.' };
  const car = firm.cars.find((c) => c.id === carId);
  if (!car || !car.driver) return { ok: false, why: 'Nobody is driving it.' };
  return { ok: true, why: '', cars: firm.cars.map((c) => (c.id === carId ? Object.assign({}, c, { rank: rankId }) : c)) };
}
// A day ends: a rank is won by being there with a car on the board enough days.
function rankDay(firm) {
  const ranks = {},
    won = [];
  for (const id in F.ranks) {
    const r = Object.assign({ held: !!F.ranks[id].held, days: 0 }, firm.ranks[id]);
    if (!r.held && firm.cars.some((c) => c.rank === id && c.driver && !c.off)) {
      r.days++;
      if (r.days >= F.ranks[id].wonAfterGameDaysThere) {
        r.held = true;
        won.push(id);
      }
    }
    ranks[id] = r;
  }
  return { ranks, won };
}
// An account: by a named person, on standing, cars and what is already held. have: { rung, dress, met: [ids] }
function account(firm, id, have) {
  const a = F.accounts[id];
  if (!a) return { ok: false, why: 'No such account.' };
  if (firm.accounts[id]) return { ok: false, why: 'He has it already.' };
  if (!(have.met || []).includes(a.via)) return { ok: false, why: 'It needs a word with the right person first.' };
  if ((have.rung || 1) < a.needsRung) return { ok: false, why: 'They do not know his name well enough yet.' };
  if (firm.cars.filter((c) => c.driver).length < a.needsCars) return { ok: false, why: 'He has not the cars to cover it.' };
  if (a.needs.some((n) => !firm.accounts[n])) return { ok: false, why: 'One contract at a time. They ask who else trusts him.' };
  if ((have.dress || 0) < (a.needsDress || 0)) return { ok: false, why: 'Not dressed like that.' };
  return { ok: true, why: '', name: a.name };
}
// What the book takes in a day without him: each crewed car's share, and each account's fares (ER-FIRM-01: an account adds fares to the book).
function dayFares(firm, timesByRank) {
  let p = 0;
  const flows = [];
  for (const c of firm.cars)
    if (c.driver && !c.off && c.driver !== 'tom') {
      const amt = Math.round(F.fareShareOfACarADayPence * ((timesByRank || {})[c.rank] ?? 1));
      p += amt;
      flows.push({ from: 'fares', to: 'the fare book', pence: amt, why: c.id + ', ' + c.driver });
    }
  for (const id in firm.accounts)
    if (firm.accounts[id]) {
      p += F.accounts[id].cleanPenceAGameDay;
      flows.push({ from: F.accounts[id].name, to: 'the fare book', pence: F.accounts[id].cleanPenceAGameDay, why: 'account fares' });
    }
  return { pence: p, flows };
}
// The board, as chalked: words only, never a number (ER-FIRM-01, ER-RISE-01). names: { driverId: 'Kevin' }
function board(firm, names) {
  const lines = [];
  for (const c of firm.cars) {
    const who = c.driver === 'tom' ? 'himself' : c.driver ? (names || {})[c.driver] || c.driver : 'nobody';
    lines.push(cap(c.id) + ': ' + who + (c.off ? ', off the road' : c.driver ? ', ' + F.ranks[c.rank || 'mickeys'].name : ', standing in the yard'));
  }
  for (const id in F.ranks) {
    const r = firm.ranks[id] || {};
    lines.push(cap(F.ranks[id].name) + ': ' + (r.held || F.ranks[id].held ? 'ours' : r.days ? 'worked, not yet ours' : F.ranks[id].heldBy));
  }
  for (const id in firm.accounts) if (firm.accounts[id]) lines.push('Account: ' + F.accounts[id].name);
  for (const id in firm.fronts) lines.push('Front: ' + F.fronts[id].name + ', through ' + ((names || {})[firm.fronts[id].man] || firm.fronts[id].man));
  for (const id in firm.rounds) lines.push('Round: ' + F.rounds[id].name + ', collected by ' + ((names || {})[firm.rounds[id].man] || firm.rounds[id].man));
  return lines;
}
const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
// A front: got by money, a favour or pressure, and always given a man. keeper: { regard, fear }
function front(firm, id, how, ctx) {
  const f = F.fronts[id];
  if (!f) return { ok: false, why: 'No such business.' };
  if (firm.fronts[id]) return { ok: false, why: 'He has a share already.' };
  if (!ctx.man) return { ok: false, why: 'It needs one of his people put in it.' };
  if (ctx.streetOnEdge) return { ok: false, why: 'Not this week. The street is frightened of him.' };
  if (how === 'money') {
    if ((ctx.moneyPence || 0) < f.pricePence) return { ok: false, why: 'He has not got it.' };
    return { ok: true, why: '', pence: f.pricePence, front: { man: ctx.man, how } };
  }
  if (how === 'favour') {
    if ((ctx.keeper || {}).regard > F.frontByFavourNeedsRegardAbove) return { ok: true, why: '', pence: 0, front: { man: ctx.man, how } };
    return { ok: false, why: 'She owes him nothing.' };
  }
  if (how === 'pressure') {
    if ((ctx.keeper || {}).fear > F.frontByPressureNeedsFearAbove) return { ok: true, why: '', pence: 0, front: { man: ctx.man, how }, seen: true };
    return { ok: false, why: 'Not frightened enough to sign, and now it is known he asked.' };
  }
  return { ok: false, why: 'By money, a favour or pressure.' };
}
// The week's money from fronts and rounds, each through its man: short if the man is (ER-FRONT-01).
// men: { id: { loyalty, fate } }
function week(firm, men) {
  const flows = [],
    trouble = [];
  let washExtra = 0;
  const through = (kind, id, name, pence, dirty) => {
    const slot = firm[kind][id],
      m = (men || {})[slot.man];
    if (!m || m.fate) {
      trouble.push({ at: name, through: slot.man, what: 'nobody brought it: his man is gone' });
      return false;
    }
    const short = m.loyalty < F.shortManBelowLoyalty;
    const got = short ? Math.round(pence * (1 - F.shortManKeepsShare)) : pence;
    flows.push({ from: name, to: dirty ? 'the tin' : 'the fare book', pence: got, why: 'brought by ' + slot.man, through: slot.man });
    if (short) trouble.push({ at: name, through: slot.man, what: 'it came short' });
    return true;
  };
  for (const id in firm.fronts) if (through('fronts', id, F.fronts[id].name, F.fronts[id].cleanPenceAWeek, false)) washExtra += F.fronts[id].washExtraPenceAWeek;
  for (const id in firm.rounds) through('rounds', id, F.rounds[id].name, F.rounds[id].nightPenceAWeek, true);
  return { flows, trouble, washExtraPence: washExtra };
}
// Wages on Friday; an unpaid driver leaves after the set weeks (A14).
function wages(firm, wagePence, moneyPence) {
  const drivers = firm.cars.map((c) => c.driver).filter((d) => d && d !== 'tom');
  const due = drivers.length * wagePence,
    unpaid = Object.assign({}, firm.unpaid),
    left = [];
  let paid = 0;
  for (const d of drivers) {
    if (moneyPence - paid >= wagePence) {
      paid += wagePence;
      delete unpaid[d];
    } else {
      unpaid[d] = (unpaid[d] || 0) + 1;
      if (unpaid[d] >= 2) left.push(d);
    }
  }
  return { due, paid, unpaid, left };
}
export const PIECE = { name: 'firm_rules', fns: { buyCar, crew, place, rankDay, account, dayFares, board, front, week, wages } };
