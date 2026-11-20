// LEDGER, the whole game: the system "econ". Money by the week (running costs, the drivers' takings and wages, the
// week's count), the flows book's check (no money from nowhere), the debts' rules for whoever collects, the alibi
// fare, the book's record for the inspection, and reports of talk lines. The rules themselves are the rule pieces
// (game/pieces/money.js, flows.js, debts.js, talk.js); this file holds the game to them.
import { register, emit, ensureX } from './core.js';
import { G, day } from '../state.js';
import { RULES } from '../rules.js';
import { clamp, money, DAYS } from '../util.js';
import { pay, earn, flowsBook, weekRow, washCap, wash } from '../money.js';
import { act, logLine } from '../events.js';
import { note } from '../ledger.js';
import { sub, scene } from '../ui.js';
import { KINDS } from '../kinds.js';
import * as M from './pieces/money.js';
import * as FLOWS from './pieces/flows.js';
import * as DEBTS from './pieces/debts.js';
import * as TALK from './pieces/talk.js';
import { talking } from '../talk.js';

const T = RULES.game.econ.money;
const WEEK = DAYS.length;
const X = () => ensureX().econ;
const drivers = () => {
  // the rise's fleet, once it exists (G.x.firm.drivers); until then Mickey's two (Kevin days, Terry nights)
  const f = G.x && G.x.firm && G.x.firm.drivers;
  if (Array.isArray(f)) return f.length;
  if (typeof f === 'number') return f;
  return ['kevin', 'terry'].filter((id) => G.people[id] && !G.people[id].dead).length;
};
const weekOf = (d) => Math.floor(d / WEEK);
const key = (what, d) => what + ':' + weekOf(d);
const says = (text) => sub(text, 'Sheila Dunn', 'face', RULES.game.econ.says.lineShowsRealSeconds);

// ---------- the week's money ----------
function runningCosts(d) {
  const x = X();
  if (x.done[key('costs', d)]) return;
  x.done[key('costs', d)] = 1;
  if (pay(T.runningCostsPence, true, 'running costs', 'sheila')) {
    note(`The garage's petrol account and the radio: ${money(T.runningCostsPence)} paid out of his pocket, as every Thursday.`, 'money', key('costs', d), { who: 'sheila', how: 'Sheila says' });
    says(`The garage and the radio, same as every Thursday. ${money(T.runningCostsPence)}, out of your pocket.`);
  } else {
    x.owed.push({ what: 'the garage and the radio', pence: T.runningCostsPence, since: Math.round(G.t) });
    act('costs_unpaid', { silent: true, told: ['sheila'] });
    note(`The garage's petrol account and the radio want ${money(T.runningCostsPence)} and he has not got it. Sheila is holding them off.`, 'money', key('costs', d), { who: 'sheila', how: 'Sheila says' });
    says(`The garage wants its ${money(T.runningCostsPence)} and you haven't got it. I'll hold them off. Not for long.`);
  }
}
function driversDay(d) {
  // the firm drives without him (DESIGN 5): each working driver's shift goes into the fare book
  const x = X();
  if (d % WEEK >= T.driverWorkingDaysPerWeek) return;
  const took = drivers() * T.driverTakesPerWorkingDayPence;
  x.firmTakings += took;
  x.firmFaresSinceWash = (x.firmFaresSinceWash || 0) + took;
  x.firmDays += drivers();
}
function wages(d) {
  const x = X();
  if (x.done[key('wages', d)]) return;
  x.done[key('wages', d)] = 1;
  const n = drivers(),
    due = n * T.driverWagePerWeekPence,
    fromTakings = Math.min(due, x.firmTakings),
    short = due - fromTakings;
  x.firmTakings -= fromTakings;
  x.wagesPaid = { week: weekOf(d), due, short: 0 };
  if (!short) return;
  if (pay(short, true, 'wages', 'sheila')) {
    note(`The cars did not cover the drivers this week. ${money(short)} of their wages came out of his pocket.`, 'money', key('wages', d), { who: 'sheila', how: 'Sheila says' });
    says(`The cars didn't cover the drivers this week. ${money(short)} of it has come out of your pocket.`);
  } else {
    x.wagesPaid.short = short;
    x.owed.push({ what: "the drivers' wages", pence: short, since: Math.round(G.t) });
    act('wages_short', { silent: true, told: ['sheila', 'kevin', 'terry'].filter((id) => G.people[id]) });
    emit('wages:short', { pence: short, week: weekOf(d) });
    note(`The drivers were paid ${money(short)} short this week. They know it.`, 'money', key('wages', d), { who: 'sheila', how: 'Sheila says' });
    says(`I've paid the drivers ${money(short)} short. They know whose fault that is.`);
  }
}
function weekCount(d) {
  const x = X();
  if (x.done[key('count', d)]) return;
  x.done[key('count', d)] = 1;
  const left = x.firmTakings;
  x.firmTakings = 0;
  x.firmDays = 0;
  if (left > 0) {
    earn(left, false, "the firm's week after wages", 'sheila');
    note(`The week's count: after the drivers' wages the cars left ${money(left)} for his pocket.`, 'money', key('count', d), { who: 'sheila', how: 'Sheila says' });
    says(`The week's count. After wages the cars left you ${money(left)}. Don't spend it twice.`);
  }
  weekRow(x); // the week has its row for the inspection even when nothing went wrong
}
// what he still owes from weeks before, paid when he can (Sheila raises it: see matters)
function payOwed(i) {
  const x = X(),
    o = x.owed[i];
  if (!o) return 'Nothing stands.';
  if (!pay(o.pence, true, o.what, 'sheila')) return `That's not ${money(o.pence)}. I can count.`;
  x.owed.splice(i, 1);
  return 'Paid. I shall say so if anybody asks.';
}
// What he has and what is owed by Friday, in words (ER-MONEY-02).
export function moneyWords() {
  const x = X(),
    d = day(),
    f = G.story.flags,
    due = [];
  if (!f.rent && weekOf(d) === 0) due.push({ what: 'the rent', pence: RULES.money.rentPence });
  if (!x.done[key('costs', d)] && d % WEEK <= T.runningCostsDueDayIndex) due.push({ what: 'the garage and the radio', pence: T.runningCostsPence });
  for (const o of x.owed) due.push({ what: o.what, pence: o.pence });
  return M.moneyInWords({ clean: G.money.clean, dirty: G.money.dirty }, due);
}

// ---------- the flows check ----------
function checkFlows() {
  const x = flowsBook(),
    c = FLOWS.check(x.book, { clean: G.money.clean, dirty: G.money.dirty });
  if (c.ok) return true;
  // something moved money without saying why. It is written down as that, so the sum holds from here, and counted.
  for (const [pot, v] of [
    ['pocket', c.pocketUnexplained],
    ['tin', c.tinUnexplained],
  ]) {
    if (!v) continue;
    const f = v > 0 ? { from: 'world', to: pot, pence: v, why: 'unexplained (a fault)' } : { from: pot, to: 'world', pence: -v, why: 'unexplained (a fault)' };
    const r = FLOWS.add(x.book, f);
    if (r.ok) x.book = r.book;
    x.unexplained += Math.abs(v);
  }
  console.error('GAME FAULT econ: money moved with no flow: pocket ' + c.pocketUnexplained + ', tin ' + c.tinUnexplained);
  return false;
}

// ---------- debts, for whoever collects ----------
// how: 'asked' | 'squeezed' | 'goods' | 'word'. The debtor pays what the purse holds and the rest stays on the book.
export function debtCollect(P, how = 'squeezed') {
  const d = G.debts[P.id];
  if (!d || d.st !== 'open') return { pence: 0, goods: 0, word: false, said: 'Nothing stands against that name.' };
  const x = X(),
    purse = x.purses[P.id] == null ? undefined : x.purses[P.id],
    r = DEBTS.collect(P.id, { owed: d.owed, st: d.st, paid: d.paid || 0 }, how, purse);
  d.owed = r.debt.owed;
  d.st = r.debt.st;
  d.paid = r.debt.paid;
  if (r.pence) {
    earn(r.pence, true, 'a debt on the book', P.id);
    x.purses[P.id] = Math.max(0, (purse == null ? RULES.game.econ.debts.pursePence[P.id] || 0 : purse) - r.pence);
  }
  if (r.goods) {
    G.tom.items = G.tom.items || {};
    G.tom.items.goods = (G.tom.items.goods || 0) + r.goods; // carried, hot, to be fenced (the jobs builder's lifts)
    emit('goods', { from: P.id, worthPence: r.goods, hot: true });
  }
  if (r.tells) {
    const kind = r.goods ? 'debt_goods' : r.word ? 'debt_word' : r.tells.kind === 'debt_shamed' ? 'debt_shamed' : r.debt.st === 'paid' ? 'debt_paid' : 'debt_part';
    act(kind, { target: P.id });
    P.mind.regard = clamp(P.mind.regard + r.tells.regard, -1, 1);
    P.mind.fear = clamp(P.mind.fear + r.tells.fear, 0, 1);
  }
  return r;
}
export function debtForgive(P) {
  const d = G.debts[P.id];
  if (!d || d.st !== 'open') return null;
  const r = DEBTS.strike({ owed: d.owed, st: d.st, paid: d.paid || 0 });
  d.owed = 0;
  d.st = 'forgiven';
  act('debt_forgive', { target: P.id });
  P.mind.regard = clamp(P.mind.regard + r.tells.regard, -1, 1);
  return r;
}

// ---------- the alibi fare ----------
// A fare written in the book for an hour he was somewhere else. It covers that hour if nobody saw him elsewhere;
// either way it is a lie in the book, and the inspection reads it.
export function alibiFare(bookMinute) {
  const x = X(),
    W = RULES.game.econ.money.alibiFareMinutesEitherSide,
    seen = G.events.filter((E) => Math.abs(E.t - bookMinute) <= W && E.wit && E.wit.length && !KINDS[E.kind].noself).map((E) => ({ minute: Math.round(E.t), place: E.zone || 'the street' })),
    r = M.alibiFare(bookMinute, false, seen);
  x.alibis.push({ minute: Math.round(bookMinute), holds: r.holds, written: Math.round(G.t) });
  const row = weekRow(x);
  row.lies++;
  if (!r.holds) row.liesBroken++;
  act('alibi_fare', { silent: true, told: ['sheila'] });
  return r;
}
const DAY = RULES.game.econ.says.minutesInADay,
  HOUR = RULES.game.econ.says.minutesInAnHour;
// the night just gone: from ten the evening before to five this morning
const lastNight = () => {
  const base = (day() - 1) * DAY;
  return { from: base + RULES.game.econ.says.nightStartsAtHour * HOUR, to: base + DAY + RULES.game.econ.says.nightEndsAtHour * HOUR };
};
function nightDeed() {
  const n = lastNight(),
    x = X();
  if (x.alibis.some((a) => a.minute >= n.from && a.minute <= n.to)) return null;
  return G.events.find((E) => E.t >= n.from && E.t <= n.to && KINDS[E.kind].crime >= 1 && !KINDS[E.kind].noself) || null;
}
// The book as the inspector will find it.
export const bookReads = () => M.bookReads((X().weeks || []).map((w) => ({ booksOffPence: w.booksOffPence, lies: w.lies, liesBroken: w.liesBroken })));

// ---------- reports of lines (ER-TALK-07) ----------
// talk.js keeps the last line anybody said in G.x.econ.lastLine. F9 reports it, in a talk or from the pause screen.
export function reportLine(from, why) {
  const x = X(),
    l = x.lastLine;
  const r = TALK.report(x.reports, l ? { line: l.text, who: l.who, minute: G.t, from, live: !!l.live, why } : null);
  if (!r.ok) return false;
  x.reports = r.list;
  logLine(`Reported a line of ${l.who}: ${l.text.slice(0, RULES.game.econ.says.logKeepsCharacters)}`, 'report');
  return true;
}
let keyBound = false;
function bindReportKey() {
  if (keyBound || typeof window === 'undefined') return;
  keyBound = true;
  window.addEventListener(
    'keydown',
    (e) => {
      if (e.code !== 'F9' || G.story.phase !== 'play') return;
      e.preventDefault();
      const ok = reportLine(talking() ? 'talk' : 'pause');
      if (G.hooks.reported) G.hooks.reported(ok);
      else sub(ok ? 'That line is reported. It is kept with this game for the people who make it.' : 'There is no line to report yet.', '', 'over', RULES.game.econ.says.lineShowsRealSeconds);
    },
    true,
  );
}

register({
  id: 'econ',
  fresh: () => ({
    book: null, // the flows book, opened when first needed
    unexplained: 0, // pence that moved with no flow: must stay nothing
    weeks: [], // the fare book's record, a row a week, for the inspection
    done: {}, // what has been settled, by week
    owed: [], // what he could not pay when it fell due
    firmTakings: 0, // what the firm's own drivers have brought in since the last count
    firmFaresSinceWash: 0,
    firmDays: 0,
    purses: {}, // what is left in each debtor's purse
    alibis: [],
    reports: [],
    lastLine: null,
    inTalk: false,
    wagesPaid: null,
  }),
  loaded(x) {
    for (const k of ['weeks', 'owed', 'alibis', 'reports']) if (!Array.isArray(x[k])) x[k] = [];
    for (const k of ['done', 'purses']) if (!x[k] || typeof x[k] !== 'object') x[k] = {};
    for (const k of ['unexplained', 'firmTakings', 'firmFaresSinceWash', 'firmDays']) if (typeof x[k] !== 'number') x[k] = 0;
    flowsBook();
    checkFlows();
    bindReportKey();
    Object.assign(G.hooks, { debtCollect, debtForgive, moneyWords, bookReads, alibiFare, reportLine, washCap });
  },
  minute() {
    checkFlows();
  },
  hourly(h, d) {
    const wd = d % WEEK;
    if (h === RULES.game.econ.says.driversBookedAtHour) driversDay(d);
    if (wd === T.runningCostsDueDayIndex && h === T.runningCostsDueHour) runningCosts(d);
    if (wd === T.wagesPaidDayIndex && h === T.wagesPaidHour) wages(d);
    if (wd === T.weekCountDayIndex && h === T.weekCountHour) weekCount(d);
  },
  matters(P, a) {
    if (P.id !== 'sheila') return;
    const x = X();
    if (x.owed.length) {
      const o = x.owed[0];
      a.push({
        key: 'owed',
        direct: true,
        ask: `whether to pay ${o.what} now`,
        raise: `${o.what.charAt(0).toUpperCase() + o.what.slice(1)}: ${money(o.pence)} still stands. Have you got it?`,
        opts: [
          {
            agree: 1,
            q: `${money(o.pence)}. Have you got it?`,
            yes: ['Yes. Pay it.', "Yes. Here's the money."],
            no: ['No. Not today.', 'No. Hold them off.'],
            keep: ['What happens if it waits?', 'Who is asking for it?'],
            keepSay: `It waits, and they talk. ${money(o.pence)}. Have you got it?`,
            noSay: "Then I hold them off another day. I can't do that for ever.",
            take: () => payOwed(0),
          },
        ],
      });
    }
    const E = nightDeed();
    if (E && G.money.fareCount > 0)
      a.push({
        key: 'alibi',
        ask: 'whether to have a fare written in the book for last night',
        raise: 'The book has an empty line for last night, if you were ever going to want one filled.',
        keep: ['What would it say?', 'Who would read it?'],
        keepSay: 'A fare, a time, an address. Anybody who ever opens this book reads it, and I am the one who wrote it.',
        opts: [
          {
            say: ['Write me a fare for last night.', 'Put a fare in for last night.'],
            q: "A fare you never drove, in my hand. Once it's in ink it's in ink. You're sure?",
            yes: ['Yes. Write it.', 'Yes. Put it in.'],
            no: ['No. Leave the line empty.', 'No. Forget I asked.'],
            keep: ['What if somebody saw me elsewhere?', 'Would you stand by it?'],
            keepSay: "Then the book says one thing and they say another, and I'm the one asked which. A fare you never drove. You're sure?",
            take: () => {
              const r = alibiFare(E.t);
              G.people.sheila.mind.regard = clamp(G.people.sheila.mind.regard - RULES.game.econ.says.alibiCostsSheilaRegard, -1, 1);
              note('A fare is in the book for an hour he was somewhere else. Sheila wrote it. Somebody may one day have to hold it up.', 'money', 'alibi:' + Math.round(E.t), { who: 'sheila', how: 'Sheila wrote it' });
              return r.holds ? "It's in. Remember what it says, because I shall." : "It's in. And if anybody saw you that night, it's a lie with my writing on it.";
            },
          },
        ],
      });
  },
  hook: {
    check: () => FLOWS.check(flowsBook().book, { clean: G.money.clean, dirty: G.money.dirty }),
    totals: () => FLOWS.totals(flowsBook().book),
    words: () => moneyWords(),
    bookReads: () => bookReads(),
    state: () => JSON.parse(JSON.stringify(X())),
    pay: (p, cleanOnly, why) => pay(p, cleanOnly, why),
    earn: (p, dirty, why) => earn(p, dirty, why),
    collect: (id, how) => debtCollect(G.people[id], how),
    forgive: (id) => debtForgive(G.people[id]),
    alibi: (minute) => alibiFare(minute),
    report: (from, why) => reportLine(from, why),
    washCap: () => washCap(),
    wash: () => scene(wash), // Sheila's count, as the talk's own decision runs it
    weekCosts: () => M.weekCosts(drivers()),
  },
});
