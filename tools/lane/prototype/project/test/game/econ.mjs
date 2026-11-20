// The one-shot, system econ: money by the week through the rule pieces, in the built page.
// 2.7.1 to 2.7.4 and 2.7.7; ER-MONEY-01 (no money from nowhere), 02 (in words), 03 (doing nothing misses Friday's
// rent), 04 (Sheila warns before the books go off); 2.8.2 (a debtor pays what the purse holds).
import { launch } from '../harness.mjs';
let bad = 0;
const ok = (c, what) => { console.log((c ? 'ok   ' : 'FAIL ') + what); if (!c) bad++; };
const h = await launch({ port: 8931, seed: 1990 });
await h.newWeek();
const E = (fn, ...a) => h.ev(fn, ...a);

// the book opens with the pocket he arrived with, and agrees with it
let s = await E(() => ({ check: LEDGER.game.econ.check(), m: { ...LEDGER.G.money }, sys: LEDGER.game.systems().includes('econ') }));
ok(s.sys && s.check.ok && s.m.clean === 2350 && s.m.dirty === 0, 'a new game: the flows book opens at £23.50 and agrees with the pocket ' + JSON.stringify(s.check));

// ER-MONEY-01: earning and paying each leave a flow with a reason; the book still agrees
s = await E(() => {
  const e = LEDGER.game.econ;
  e.earn(210, false, 'a fare');
  e.earn(6000, true, 'the Monday bag');
  const paid = e.pay(800, false, 'a cosh'), refused = e.pay(999999, false, 'the moon');
  return { paid, refused, check: e.check(), m: { ...LEDGER.G.money }, totals: e.totals() };
});
ok(s.paid && !s.refused && s.check.ok && s.m.clean === 2560 && s.m.dirty === 5200, 'ER-MONEY-01 earn, pay (night money first) and a refused payment: the book agrees ' + JSON.stringify(s.m.clean + '/' + s.m.dirty));
ok(s.totals.in.some((r) => r.why === 'the Monday bag' && r.pence === 6000) && s.totals.out.some((r) => r.why === 'a cosh' && r.pence === 800), '2.7.7 every pound has its reason in the book ' + JSON.stringify(s.totals));

// a pound from nowhere is seen within a game minute, counted, and written down as what it is
s = await E(() => { LEDGER.G.money.clean += 100; return 1; });
await h.step(2);
s = await E(() => ({ un: LEDGER.game.econ.state().unexplained, check: LEDGER.game.econ.check(), faults: LEDGER.game.faults.length }));
ok(s.un === 100 && s.check.ok, 'ER-MONEY-01 a pound put in the pocket with no flow is caught and counted (unexplained ' + s.un + 'p)');
await E(() => { LEDGER.game.x().econ.unexplained = 0; });

// ER-MONEY-02: in words
s = await E(() => LEDGER.game.econ.words());
ok(/pounds/.test(s.has) && /by Friday/.test(s.owes) && !/\d/.test(s.has + s.owes + s.short), 'ER-MONEY-02 what he has and owes by Friday, in words and no figures: ' + s.has + ' ' + s.owes + ' ' + s.short);

// ER-MONEY-04: the warning comes before anything goes through; "only what the book will hide" keeps the books right
s = await E(() => ({ cap: LEDGER.game.econ.washCap(), tin: LEDGER.G.money.dirty }));
ok(s.tin > s.cap, 'the tin (' + s.tin + ') is over what the book will hide (' + s.cap + ')');
s = await E(() => ({ has: typeof LEDGER.game.econ.wash === 'function' }));
if (s.has) {
  await E(() => { window.__w = LEDGER.game.econ.wash(); });
  await h.sleep(300);
  let r = await E(() => LEDGER.written.read());
  ok(r.open && r.waitsForAChoice && /can't hide/.test(r.text) && r.choices && r.choices.length === 3, 'ER-MONEY-04 Sheila says what the book will hide and what is over, before anything goes through: ' + (r.text || '').slice(0, 90));
  const mid = await E(() => ({ ...LEDGER.G.money }));
  ok(mid.dirty === 5200, 'nothing has gone through while she waits for his answer');
  await E(() => LEDGER.written.choose(0));
  for (let i = 0; i < 6; i++) { r = await E(() => LEDGER.written.read()); if (!r.open) break; await E(() => LEDGER.written.next()); }
  s = await E(() => ({ m: { ...LEDGER.G.money }, check: LEDGER.game.econ.check(), cap: LEDGER.game.econ.washCap() }));
  ok(s.m.booksOff === 0 && s.m.dirty > 0 && s.m.washed > 0 && s.check.ok, '"Only what the book will hide": ' + s.m.washed + 'p through, ' + s.m.dirty + 'p stays in the tin, the books still add up');
  // all of it asks twice, and then the week's row carries it for the inspection
  await E(() => { LEDGER.game.econ.earn(3000, true, 'a night job'); window.__w = LEDGER.game.econ.wash(); });
  await h.sleep(300);
  await E(() => LEDGER.written.choose(1));
  r = await E(() => LEDGER.written.read());
  ok(r.open && r.waitsForAChoice && /sure/i.test(r.text), 'ER-CORE-03 "All of it" asks twice: ' + (r.text || '').slice(0, 80));
  await E(() => LEDGER.written.choose(0));
  for (let i = 0; i < 6; i++) { r = await E(() => LEDGER.written.read()); if (!r.open) break; await E(() => LEDGER.written.next()); }
  s = await E(() => ({ m: { ...LEDGER.G.money }, reads: LEDGER.game.econ.bookReads(), check: LEDGER.game.econ.check() }));
  ok(s.m.booksOff > 0 && s.m.dirty === 0 && s.reads.state === 'thin' && s.check.ok, 'all of it: the books are off by ' + s.m.booksOff + 'p and the inspection will read "' + s.reads.words + '"');
} else ok(false, 'the wash could not be reached from the test hook');

// 2.8.2: a debtor pays what the purse holds, the rest stays on the book
s = await E(() => {
  const before = LEDGER.G.money.dirty, r = LEDGER.game.econ.collect('lee', 'squeezed');
  return { r, lee: { ...LEDGER.G.debts.lee }, got: LEDGER.G.money.dirty - before, check: LEDGER.game.econ.check() };
});
ok(s.r.pence === 400 && s.lee.owed === 1100 && s.lee.st === 'open' && s.got === 400 && s.check.ok, '2.8.2 Lee squeezed pays the four pounds in his purse; eleven stay on the book');
s = await E(() => { const r = LEDGER.game.econ.collect('lee', 'squeezed'); return { r, lee: { ...LEDGER.G.debts.lee } }; });
ok(s.r.pence === 0 && s.lee.owed === 1100, '... and a second squeeze the same day finds the purse empty');
s = await E(() => { const r = LEDGER.game.econ.collect('julie', 'squeezed'); const ev = LEDGER.G.events[LEDGER.G.events.length - 1]; return { r, kind: ev.kind, julie: { ...LEDGER.G.debts.julie } }; });
ok(s.r.pence === 0 && s.kind === 'debt_shamed' && s.julie.owed === 900, 'Julie squeezed: no money, and the street is told he leaned on somebody with nothing');
s = await E(() => { LEDGER.game.econ.forgive('julie'); return { julie: { ...LEDGER.G.debts.julie }, kind: LEDGER.G.events[LEDGER.G.events.length - 1].kind }; });
ok(s.julie.st === 'forgiven' && s.kind === 'debt_forgive', 'struck out: the debt is gone for good and the street is told');

// 2.7.4 and ER-MONEY-03 in the game: a week of doing nothing. Running costs on Thursday, no rent by Friday six.
await h.close();
const g = await launch({ port: 8932, seed: 1990 });
await g.newWeek();
const at = (d, hh) => d * 1440 + hh * 60;
await g.ev((t) => LEDGER.passTime(t, ''), at(3, 13));
await g.sleep(400);
s = await g.ev(() => ({ m: { ...LEDGER.G.money }, x: LEDGER.game.econ.state(), check: LEDGER.game.econ.check(), t: LEDGER.G.t, faults: LEDGER.game.faults.slice(0, 3) }));
ok(s.t >= at(3, 13) - 1 && s.m.clean === 2350 - 950 && s.check.ok, '2.7.4 Thursday noon: the garage and the radio take £9.50 from the pocket (pocket ' + s.m.clean + 'p at minute ' + Math.round(s.t) + ')');
ok(s.x.firmTakings === 2 * 700 * 3, 'the firm drives without him: three days of two drivers in the book (' + s.x.firmTakings + 'p)');
await g.ev((t) => LEDGER.passTime(t, ''), at(4, 18.5));
await g.sleep(400);
s = await g.ev(() => ({ m: { ...LEDGER.G.money }, f: { rent: LEDGER.G.story.flags.rent, late: LEDGER.G.story.flags.rentLate }, x: LEDGER.game.econ.state() }));
ok(s.m.clean < 1800 && !s.f.rent, 'ER-MONEY-03 a week of doing nothing: £' + (s.m.clean / 100).toFixed(2) + ' on Friday at half past six, the rent of £18 cannot be met');
ok(s.x.wagesPaid && s.x.wagesPaid.short === 0, 'the drivers were paid from their own takings on Friday morning');
if (!(await g.ev(() => LEDGER.G.story.ended))) {
  await g.ev((t) => LEDGER.passTime(t, ''), at(5, 10.5));
  await g.sleep(400);
  s = await g.ev(() => ({ m: { ...LEDGER.G.money }, check: LEDGER.game.econ.check(), x: LEDGER.game.econ.state() }));
  ok(s.check.ok && s.x.unexplained === 0, "Saturday's count: what the cars left after wages reaches the pocket (" + s.m.clean + 'p), and the book agrees');
}
s = await g.ev(() => ({ faults: LEDGER.game.faults.slice(0, 5) }));
ok(s.faults.length === 0, 'no fault in any system: ' + JSON.stringify(s.faults));
ok(g.errors.filter((e) => !/unexplained|no flow/.test(e)).length === 0, 'no page errors: ' + JSON.stringify(g.errors.slice(0, 3)));
await g.close();
console.log(bad ? 'TEST FAIL (' + bad + ')' : 'PASS');
process.exit(bad ? 1 : 0);
