// LEDGER, the whole game: the system "econ". Money's glue (DESIGN 9; parts 2.7.1 to 2.7.4, 2.7.7): the flows ledger
// (no money from nowhere), the week's rent and wages from the fare book, and what the firm's own drivers bring the
// book without him. The rules are the piece pieces/money.js; the pocket and the tin stay the prototype's G.money.
import { register, X, write, tell, dayNow, hourNow, emit, FAULTS } from './core.js';
import { G } from '../state.js';
import { pay, earn } from '../money.js';
import { RULES } from '../rules.js';
import { PIECE as MONEY } from './pieces/money.js';

const T = RULES.game.econ;
const M = MONEY.fns;

function flow(from, to, pence, why) {
  const x = X('econ');
  x.flows.push({ from, to, pence, why, t: Math.round(G.t) });
  if (x.flows.length > 600) x.old += x.flows.splice(0, 200).length;
  if (to !== 'world') x.sum[to] += pence;
  if (from !== 'world') x.sum[from] -= pence;
}
// ER-MONEY-01: the pocket and the tin each equal the sum of their flows.
export function balances() {
  const x = X('econ'),
    m = G.money;
  return { pocket: m.clean, tin: m.dirty, pocketByFlows: x.sum.pocket, tinByFlows: x.sum.tin, holds: m.clean === x.sum.pocket && m.dirty === x.sum.tin };
}
// Money in words, for the Ledger and for anybody who asks him (ER-MONEY-02).
export function inWords() {
  const m = G.money,
    d = dayNow();
  const rent = M.rentState(d % 7, hourNow(), !!G.story.flags.rent || X('econ').rentPaidWeek === Math.floor(d / 7));
  return {
    pocket: M.words(m.clean),
    tin: M.words(m.dirty),
    rent: rent === 'paid' ? 'The rent is paid.' : rent === 'late' ? `The rent is late: ${M.words(T.rentPence)}.` : `Rent is ${M.words(T.rentPence)}, due Friday by six.`,
    hide: `The fare book can hide ${M.words(M.washCap(m.sinceWash, X('econ').fronts))}.`,
  };
}
export const fareShare = () => X('econ').fareShare;
export const setFareShare = (share, untilT) => Object.assign(X('econ'), { fareShare: share, fareShareUntilT: untilT });
export const washRoom = () => M.washCap(G.money.sinceWash, X('econ').fronts);

register({
  id: 'econ',
  fresh: () => ({ flows: [], old: 0, sum: { pocket: G.money.clean, tin: G.money.dirty }, fronts: 0, fareShare: 1, fareShareUntilT: null, cars: 2, drivers: 2, unpaidWeeks: 0, rentPaidWeek: -1, wagesWeek: 0, firmDays: {} }),
  loaded(x) {
    // a save from before the flows ledger, or a new game: the ledger opens on what he holds now
    if (!x.flows.length && !x.old) {
      x.sum = { pocket: 0, tin: 0 };
      if (G.money.clean) flow('world', 'pocket', G.money.clean, 'what he came with');
      if (G.money.dirty) flow('world', 'tin', G.money.dirty, 'what was in the tin');
    }
    G.hooks.flow = flow;
  },
  minute() {
    const b = balances();
    if (!b.holds && !X('econ').faulted) {
      X('econ').faulted = true;
      FAULTS.push(`econ: money from nowhere (pocket ${b.pocket} against ${b.pocketByFlows} by flows, tin ${b.tin} against ${b.tinByFlows})`);
    }
    const x = X('econ');
    if (x.fareShareUntilT != null && G.t >= x.fareShareUntilT) {
      x.fareShare = 1; // the talk has faded: people ring Mickey's again
      x.fareShareUntilT = null;
      tell('The radio is busy again. People have stopped ringing the other firm.', '');
    }
  },
  hourly(h, d) {
    const x = X('econ');
    // the firm drives without him: at the end of each day its own drivers' fares go into the book (the lazy path)
    if (h === 23 && !x.firmDays[d]) {
      x.firmDays[d] = 1;
      const pence = M.firmDay(x.drivers, x.fareShare);
      if (pence > 0) {
        earn(pence, false, "the firm's own fares");
        tell(`Eleven at night. The firm's other car pays in its day's fares: £${(pence / 100).toFixed(2)} into the pocket, and into the fare book.`, '');
        G.money.fares += pence;
        G.money.sinceWash += pence;
      }
    }
    // Monday morning from the second week: the drivers' wages and the cars' upkeep come out of the fare book
    const week = Math.floor(d / 7);
    if (d % 7 === 0 && h === 8 && week >= 1 && x.wagesWeek < week) {
      x.wagesWeek = week;
      const due = M.weekCosts(x.cars, x.drivers) - T.rentPence;
      if (pay(due, true, "the week's wages and upkeep")) {
        x.unpaidWeeks = 0;
        write(`Sheila paid the drivers and the garage out of the book: ${M.words(due)}.`, { kind: 'money', key: 'wages' + week, who: 'sheila', how: 'Sheila says' });
      } else {
        x.unpaidWeeks++;
        write(`The book could not pay the drivers this week: ${M.words(due)} owed. Sheila says they will not drive for nothing for long.`, { kind: 'money', key: 'wages' + week, who: 'sheila', how: 'Sheila says' });
        tell('"There is not enough in the book for wages. They will not drive for nothing, Mr Nowak."', 'sheila');
      }
      emit('econ.week', { week, unpaid: x.unpaidWeeks });
    }
  },
  hook: {
    balances,
    flows: () => X('econ').flows,
    inWords,
    washRoom,
    weekCosts: () => M.weekCosts(X('econ').cars, X('econ').drivers),
    x: () => X('econ'),
    fareShare,
  },
});
