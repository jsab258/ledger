// LEDGER, the whole game: the system "firm". The firm grows (DESIGN 12 the board, 14; A14; parts 1.7.3, 2.15.1 to
// 2.15.3): the chalkboard in the office with a line for each car and driver; a car bought from a man selling one;
// a driver hired; ranks won by being there; accounts; one other firm on the ranks. Run on the board and through
// people, never a screen of numbers. Rules: pieces/rise.js.
import { register, X, write, tell, hourNow, dayNow, P_, emit, on, PLACES } from './core.js';
import { G } from '../state.js';
import { hyp, esc, quid } from '../util.js';
import { act } from '../events.js';
import { pay } from '../money.js';
import { choose, scene, say, panel } from '../ui.js';
import { RULES } from '../rules.js';
import { PIECE as RISE } from './pieces/rise.js';

const T = RULES.game.firm;
const R = RULES.game.rise;
const F = RISE.fns;
const DRIVER = { kevin: 'Kevin Needham', terry: 'Terry Hodgson', julie: 'Julie Kettlewell', stranger: 'a driver who asked at the counter' };

function sync() {
  const x = X('firm'),
    e = G.x.econ;
  e.cars = x.f.cars.length;
  e.drivers = x.f.cars.filter((c) => c.driver).length - (G.x.rivals && G.x.rivals.inspectUntilT ? 1 : 0);
}
function apply(ev) {
  const x = X('firm');
  const r = F.firm(x.f, ev);
  if (r.ok) x.f = r.firm;
  sync();
  return r;
}
// The board in words: every car, driver, rank and account, never a number of standing (ER-FIRM-01).
function boardHTML() {
  const x = X('firm');
  const rows = x.f.cars.map((c, i) => `<tr><td>Car ${['one', 'two', 'three', 'four', 'five', 'six', 'seven'][i] || i + 1}</td><td>${esc(c.driver ? DRIVER[c.driver] || c.driver : 'no driver')}</td><td>${esc(c.rank ? R.ranks[c.rank].name : 'in the yard')}</td></tr>`).join('');
  return `<h2>The board</h2><table class="t"><tr><th>Car</th><th>Driver</th><th>Where</th></tr>${rows}</table><p>Ranks held: ${x.f.ranks.map((r) => esc(R.ranks[r].name)).join('; ')}.</p><p>Accounts: ${x.f.accounts.length ? x.f.accounts.map(esc).join('; ') : 'none yet'}.</p><p>${esc(R.otherFirm.name)} has ${x.otherFirmOnRank ? 'two cars on the north road rank' : 'gone quiet'}.</p><p><button data-act="close">Leave it to Pauline</button></p>`;
}
async function board() {
  const x = X('firm');
  x.boardOpens++;
  const idle = x.f.cars.filter((c) => c.driver);
  const i = await scene(() => choose('', 'The chalkboard: a line for each car and driver, and the week\'s fares.', ['Read it.', 'Put a car on a rank.', 'Hire a driver for a car without one.', 'Leave it to Pauline.']));
  if (i === 0) return panel(boardHTML(), 'board');
  if (i === 1) {
    const cars = idle.map((c) => c.id),
      ranks = Object.keys(R.ranks);
    const c = await scene(() => choose('', 'Which car?', idle.map((q) => (DRIVER[q.driver] || q.driver) + "'s").concat(['None.'])));
    if (c >= cars.length) return;
    const k = await scene(() => choose('', 'Where?', ranks.map((r) => R.ranks[r].name).concat(['Nowhere.'])));
    if (k >= ranks.length) return;
    apply({ what: 'place', car: cars[c], rank: ranks[k] });
    write(`Chalked ${DRIVER[idle[c].driver] || idle[c].driver} onto ${R.ranks[ranks[k]].name}. A car on a rank is the firm's eyes there.`, { how: 'Did it' });
  } else if (i === 2) hire();
}
function hire() {
  const x = X('firm');
  if (!x.f.cars.some((c) => !c.driver)) return tell('Every car has its driver.', '');
  const who = G.x.crew.men.julie.in && !x.f.cars.some((c) => c.driver === 'julie') ? 'julie' : Math.floor(dayNow() / 7) >= T.strangerDriverFromWeek && !x.f.cars.some((c) => c.driver === 'stranger') ? 'stranger' : null;
  if (!who) return tell('Nobody to put in it yet. A driver comes from his own people, or asks at the counter.', '');
  apply({ what: 'hire', who });
  write(`${DRIVER[who][0].toUpperCase() + DRIVER[who].slice(1)} has the spare car now.`, { how: 'Agreed it' });
}
// A car is bought from a man selling one, at the lot on the north road.
async function buyCar() {
  const x = X('firm'),
    cost = RULES.game.econ.prices.usedCar;
  const i = await scene(async () => {
    await say('The man at the lot', `A Sierra, four years old, one owner, a minister. ${quid(cost)} and it is yours today.`);
    return choose('', 'A car for the firm.', ['Buy it.', 'Not today.']);
  });
  if (i !== 0) return;
  if (!pay(cost, true, 'a used car for the firm')) return tell('"Cash from the firm\'s book, friend, or it stays where it is."', 'The man at the lot');
  const r = apply({ what: 'buy car', seller: 'the man at the lot on the north road' });
  act('bought_car', { silent: true, told: ['sheila', 'pauline'] });
  write(`Bought a car for the firm at the lot on the north road: ${quid(cost)}. It is on the board, without a driver.`, { kind: 'money', how: 'Did it' });
  emit('firm.car', { cars: r.firm.cars.length });
}
// An account adds fares to the book (the cold-store shift contract first).
async function account() {
  const x = X('firm'),
    next = R.accounts[x.f.accounts.length];
  if (!next) return;
  const i = await scene(async () => {
    await say('susan', next === R.accounts[0] ? 'The cold-store contract. Cabs for the packing shift, morning and evening, every day, and no excuses. The last firm had excuses.' : `${next[0].toUpperCase() + next.slice(1)}. On account, monthly. The Board expects a firm that turns up.`);
    return choose('susan', 'Can Mickey\'s do it?', ['Yes.', 'Not yet.']);
  });
  if (i !== 0) return;
  apply({ what: 'account', name: next });
  write(`Mickey's has ${next} now. It earns, and it explains money.`, { who: 'susan', how: 'Agreed it' });
  emit('firm.account', { name: next });
}

register({
  id: 'firm',
  fresh: () => ({ f: F.firmFresh(), boardOpens: 0, otherFirmOnRank: true, wonSaid: {} }),
  loaded() {
    sync();
  },
  daily(d) {
    const x = X('firm');
    x.f.unpaidWeeks = G.x.econ.unpaidWeeks;
    const before = x.f.ranks.slice(),
      drivers = x.f.cars.map((c) => c.driver);
    apply({ what: 'day' });
    for (const r of x.f.ranks)
      if (!before.includes(r)) {
        act('took_rank', { rank: R.ranks[r].name, silent: true, told: ['pauline', 'kevin', 'terry'] });
        write(`The firm holds ${R.ranks[r].name} now: a car of his has been there every day.`, { how: 'Pauline says' });
        if (r === 'north') x.otherFirmOnRank = false;
      }
    x.f.cars.forEach((c, i) => {
      if (drivers[i] && !c.driver) write(`${DRIVER[drivers[i]] || drivers[i]} has stopped driving for him: unpaid.`, { how: 'Sheila says' });
    });
    // an account's fares go into the book each day
    const fr = F.firmFares(x.f, G.x.econ.fareShare);
    if (fr.accountFares) {
      const pence = fr.accountFares * RULES.game.econ.firmFareAveragePence;
      G.money.clean += pence;
      G.money.earnedClean += pence;
      G.hooks.flow('world', 'pocket', pence, "the accounts' fares");
      G.money.fares += pence;
      G.money.sinceWash += pence;
    }
  },
  hotspots(out) {
    const t = G.tom,
      x = X('firm');
    if (t.space === 'mickeys') out.push({ k: out.some((o) => o.k === 'T') ? 'G' : 'T', t: 'The board', run: board });
    if (t.space === 'street' && hyp(t.x, t.z, PLACES.lot.x, PLACES.lot.z) < RULES.game.crime.doorWithinMetres + 3 && hourNow() >= 9 && hourNow() < 17) out.push({ k: 'T', t: 'The used-car lot', run: buyCar });
    if (t.space === 'harbour' && (G.x.rise ? G.x.rise.rung : 1) >= T.contractFromRung && G.x.fares.learned.contract_lead && x.f.accounts.length < R.accounts.length && P_('susan') && P_('susan').space === 'harbour') out.push({ k: 'T', t: 'Ask about the account', run: account });
  },
  hook: {
    x: () => X('firm'),
    board: () => X('firm').f,
    boardHTML,
    apply,
    buyCar,
    hire,
    account,
    fares: () => F.firmFares(X('firm').f, G.x.econ.fareShare),
  },
});
on('econ.week', () => sync());
