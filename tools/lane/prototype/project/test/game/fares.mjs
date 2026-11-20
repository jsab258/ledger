// The one-shot (20 Nov 2026): fares, to his words of 19 Nov. Few and chosen, each a person with something going on,
// each feeding the night; a dull one given to a driver in one press; no meter, no countdown, no marker; the way by
// Pauline's landmarks, always right and said again on a key (ER-DRIVE-09); no wrinkle twice running and no fare
// twice in a week (ER-JOB-06); never two minutes without a person or a decision (ER-CORE-08).
import { launch } from '../harness.mjs';

let bad = 0;
const ok = (cond, what) => {
  console.log((cond ? 'ok   ' : 'FAIL ') + what);
  if (!cond) bad++;
};
const h = await launch({ port: 8830, quality: 'low', seed: 1990 });
const L = (fn, ...a) => h.ev(fn, ...a);
await h.newWeek();
await L(() => {
  const G = LEDGER.G;
  G.story.flags.tour = 1;
  G.car.keys = true;
  window.__subs = () => LEDGER.ui.subs.map((s) => (s.el.textContent || '').trim());
  window.__mark = () => new Set(LEDGER.ui.subs);
  window.__since = (m) => LEDGER.ui.subs.filter((s) => !m.has(s)).map((s) => (s.el.textContent || '').trim());
  window.__docket = () => document.getElementById('fare').textContent;
  // pull in at a place and stand still
  window.__pull = (p) => {
    G.car.x = p[0];
    G.car.z = p[1];
    G.car.v = 0;
  };
});
ok(await L(() => LEDGER.cab.getIn()), 'Tom is at the wheel of car two');

// ---- the first fare of the game: the priest's house, by Pauline's landmarks (DESIGN 15, minute 2:30) ----
ok((await L(() => LEDGER.game.fares.next())) === 'priest', "the first fare Pauline has is the priest's house");
let r = await L(() => {
  const m = __mark();
  const o = LEDGER.game.fares.offer('priest');
  return { o, said: __since(m), docket: __docket(), prompts: LEDGER.prompts() };
});
ok(r.o && r.o.state === 'offer', 'Pauline calls it on the radio');
ok(r.said.some((s) => /Pauline/.test(s) && /Mrs Cronin/.test(s)), 'the call names the person and why her: ' + r.said.join(' | ').slice(0, 120));
ok(!/\d+\s*s\b/.test(r.docket) && !/meter/i.test(r.docket), 'no countdown and no meter on the slip: ' + r.docket.slice(0, 90));
ok(r.prompts.some((p) => p.key === 'Y') && r.prompts.some((p) => p.key === 'G' && /Give it to/.test(p.text)), 'one press takes it, one press gives it to a driver');
r = await L(() => {
  const m = __mark();
  LEDGER.press('Y');
  return { f: LEDGER.game.fares.read(), said: __since(m), marker: LEDGER.G.story.fare && 1 };
});
ok(r.f.state === 'pickup', 'Y takes the fare');
ok(r.said.some((s) => /Pauline/.test(s) && /shelter/.test(s)), 'Pauline gives the way to the pick-up by its landmark: ' + r.said.join(' | ').slice(0, 160));
r = await L(() => {
  const P = LEDGER.game.fares.places();
  __pull(P.busstop.p);
  const m = __mark();
  LEDGER.step(0.5);
  const a = LEDGER.game.fares.read(), s1 = __since(m);
  const m2 = __mark();
  LEDGER.step(8);
  return { a, s1, s2: __since(m2), way: LEDGER.game.fares.read().way };
});
ok(r.a.state === 'carry', 'pulled in beside her, she gets in');
ok(r.s1.some((s) => /priest's house/.test(s)), 'she says where to, in her own words');
ok(r.s2.some((s) => /Pauline/.test(s) && /slippers on the step/.test(s)), 'then Pauline gives the way by landmark: ' + (r.way || ''));
ok(!/\d+ ?(m|metres|yards)\b/.test(r.way || ''), 'the way has no distances in it, only roads and landmarks');
r = await L(() => {
  const m = __mark();
  LEDGER.press('KeyR');
  return __since(m);
});
ok(r.some((s) => /Again, love/.test(s) && /slippers/.test(s)), 'R has Pauline say the way again');
r = await L(() => {
  const m = __mark();
  LEDGER.step(20);
  return __since(m);
});
ok(r.some((s) => /I keep Father Walsh's door/.test(s)), 'on the way she talks: a person with something going on');
r = await L(async () => {
  const G = LEDGER.G, P = LEDGER.game.fares.places(), before = { clean: G.money.clean, fares: G.money.fares, n: G.money.fareCount };
  __pull(P.priest.p);
  LEDGER.step(0.5);
  await new Promise((res) => setTimeout(res, 50));
  return { fare: LEDGER.game.fares.read(), paid: G.money.clean - before.clean, book: G.money.fares - before.fares, n: G.money.fareCount - before.n, notes: G.ledger.notes.map((n) => n.text), log: LEDGER.game.fares.state().log.slice(-1)[0], faults: LEDGER.game.faults.length };
});
ok(r.fare === null && r.paid > 0 && r.paid === r.book && r.n === 1, `at the door she pays and it goes in the book (${r.paid}p)`);
ok(r.notes.some((n) => /keeps the priest's door/.test(n)), 'what the fare was worth to the night is in the Ledger');
ok(r.log && r.log.id === 'priest' && r.log.gives === 'eyes', 'the fare log holds it: ' + JSON.stringify(r.log));

// ---- the scripted driver: the legs the words are made from take him to every door (ER-DRIVE-09) ----
r = await L(() => {
  const P = LEDGER.game.fares.places(), starts = [{ x: 4.1, z: 37.4 }, { x: 3.2, z: -200 }, { x: -118, z: 49.6 }, { x: 150, z: 46.6 }, { x: -50, z: -18.5 }], out = [];
  for (const k in P) for (const s of starts) {
    const d = LEDGER.game.fares.drive(k, s);
    if (d.endsMetresFromTheDoor > 6 || !d.words.includes(P[k].landmark)) out.push(k + ' from ' + JSON.stringify(s) + ': ' + d.endsMetresFromTheDoor + ' m');
  }
  return { n: Object.keys(P).length * starts.length, out };
});
ok(r.out.length === 0, `a driver with only Pauline's words reaches all ${r.n} doors within 6 m: ${r.out.slice(0, 3).join('; ')}`);
// and the cab really driven along them, by the driver who brakes for people
r = await L(() => {
  const G = LEDGER.G, w = LEDGER.game.fares.way('ritaside', { x: G.car.x, z: G.car.z });
  return w;
});
ok(r.legs.length >= 1 && /Rita's side door/.test(r.words), 'the way to a side door is said: ' + r.words);

// ---- a dull one, given to a driver in one press ----
r = await L(() => {
  const G = LEDGER.G;
  G.t = 1440 + 10 * 60; // Tuesday, ten in the morning
  const before = { clean: G.money.clean, fares: G.money.fares };
  const o = LEDGER.game.fares.offer('albert_inf');
  LEDGER.press('G');
  return { o, fare: LEDGER.game.fares.read(), pocket: G.money.clean - before.clean, book: G.money.fares - before.fares, done: LEDGER.game.fares.state().done.includes('albert_inf') };
});
ok(r.o && r.fare === null && r.done, 'G gives the fare to Kevin: it is gone from the radio and will not come again this week');
ok(r.book > 0 && r.pocket > 0 && r.pocket < r.book / 4, `it still goes in the book (${r.book}p), and little of it to his pocket (${r.pocket}p)`);

// ---- a wrinkle is one decision, put on the keys while he drives: the talker ----
const ride = async (id, answer, steps = 60) =>
  L(async (id, answer, steps) => {
    const G = LEDGER.G, P = LEDGER.game.fares.places(), F = LEDGER.game.fares, list = F.list().find((f) => f.id === id);
    const key = (name) => Object.keys(P).find((k) => P[k].n === name);
    F.offer(id);
    F.accept();
    __pull(P[key(list.from)].p);
    LEDGER.step(0.5);
    const m = __mark();
    let asked = -1, prompts = null, gap = 0, worst = 0, last = __subs().length, seen = new Set(LEDGER.ui.subs);
    for (let i = 0; i < steps; i++) {
      LEDGER.step(1);
      const fresh = LEDGER.ui.subs.some((s) => !seen.has(s));
      if (fresh) { gap = 0; seen = new Set(LEDGER.ui.subs); } else gap++;
      worst = Math.max(worst, gap);
      const f = F.read();
      if (f && f.ask === 'open' && asked < 0) {
        asked = i;
        prompts = LEDGER.prompts();
        if (answer !== null) F.answer(answer);
      }
    }
    void last;
    const before = { clean: G.money.clean, dirty: G.money.dirty, t: G.t };
    __pull(P[key(list.to)].p);
    LEDGER.step(0.5);
    await new Promise((res) => setTimeout(res, 30));
    return { asked, prompts, worstQuietSeconds: worst, said: __since(m), paid: G.money.clean - before.clean, after: F.state().after && F.state().after.kind, carrying: F.state().carrying, log: F.state().log.slice(-1)[0], fare: F.read(), notes: G.ledger.notes.map((n) => n.text), to: P[key(list.to)].p };
  }, id, answer, steps);
r = await ride('talker_dock', true, 45);
ok(r.asked >= 0 && r.asked < 45, `the talker's question comes while he drives, ${r.asked} s in`);
ok(r.prompts && r.prompts.some((p) => p.key === 'Y' && p.text === 'Ask him who') && r.prompts.some((p) => p.key === 'G' && p.text === 'Let it lie'), 'the answer is on two keys, in plain words');
ok(r.notes.some((n) => /Lee Drewery drives it/.test(n)), 'asking learns a true thing about somebody, written in the Ledger');
ok(r.paid > 0 && r.fare === null, 'and the fare is paid at the door');
ok(r.worstQuietSeconds < 40, `never 40 s in a fare with nobody speaking (longest ${r.worstQuietSeconds} s; ER-CORE-08)`);
r = await L(() => ({ next: LEDGER.game.fares.next(), last: LEDGER.game.fares.state().lastWrinkle, list: LEDGER.game.fares.list() }));
ok(r.last === 'talker' && (r.list.find((f) => f.id === r.next) || {}).wrinkle !== 'talker', `no wrinkle twice running: after a talker comes ${r.next}`);

// ---- the parcel: a risk taken on, carried, and paid into the tin ----
r = await ride('parcel_rita', true, 30);
ok(r.after === 'parcel' && /parcel/.test(r.carrying || ''), 'yes to the parcel: it is in the cab and it is not his (a search would find it)');
let p = await L(() => {
  const G = LEDGER.G, P = LEDGER.game.fares.places(), d0 = G.money.dirty, n = G.events.length;
  __pull(P.ritaside.p);
  LEDGER.step(0.5);
  return { tin: G.money.dirty - d0, carrying: LEDGER.game.fares.state().carrying, kinds: G.events.slice(n).map((e) => e.kind) };
});
ok(p.tin === 200 && p.carrying === null && p.kinds.includes('fare_parcel'), `left at Rita's side door: £2 in the tin, and a deed the street could have seen (${p.kinds})`);

// ---- the hurry: a promise kept is told, and so is one broken ----
r = await ride('hurry_ferry', true, 20);
ok(r.log.outcome === 'promised and made it' && r.said.some((s) => /You said you would, and you did/.test(s)), 'promised and in time: he says so, and tips: ' + r.log.outcome);
await L(() => { LEDGER.G.t += 1440; });
r = await ride('peter_stock', true, 90);
ok(r.log.outcome === 'promised and late', 'promised and late: ' + r.log.outcome);

// ---- the runner: out of the door without paying; nothing fails, it is a face to know again ----
await L(() => { LEDGER.G.t = 2 * 1440 + 22 * 60; });
r = await ride('runner_night', null, 15);
ok(r.paid === 0 && r.after === 'runner', 'the runner pays nothing and is off');
p = await L(() => {
  const G = LEDGER.G;
  __pull([150, 46.6]); // he drives on and lets him go
  for (let i = 0; i < 30; i++) LEDGER.step(1);
  return { after: LEDGER.game.fares.state().after, log: LEDGER.game.fares.state().log.slice(-1)[0], notes: G.ledger.notes.map((n) => n.text) };
});
ok(p.after === null && p.log.after === 'got away' && p.notes.some((n) => /ran from the cab/.test(n)), 'let go, he is gone within the minute and the Ledger has him: ' + p.log.after);

// ---- the wait: paid for the forgetting ----
await L(() => { LEDGER.G.t = 3 * 1440 + 20 * 60; });
r = await ride('wait_row', true, 40);
ok(r.after === 'wait', 'yes to "keep the engine running": he waits');
p = await L(() => {
  const G = LEDGER.G, d0 = G.money.dirty, n = G.events.length;
  for (let i = 0; i < 26; i++) LEDGER.step(1);
  return { tin: G.money.dirty - d0, kinds: G.events.slice(n).map((e) => e.kind), after: LEDGER.game.fares.state().after };
});
ok(p.tin === 300 && p.kinds.includes('fare_wait') && p.after === null, 'two minutes on, three pounds for the tin, and a cab seen waiting on the row');

// ---- the edge is soft: out of the Hook and back, as time passed and money paid ----
await L(() => { LEDGER.G.t = 4 * 1440 + 11 * 60; });
const t0 = await L(() => LEDGER.G.t);
r = await ride('edge_fairview', false, 30);
await h.sleep(4000);
p = await L(() => ({ t: LEDGER.G.t, paused: LEDGER.G.paused, fare: LEDGER.game.fares.read(), log: LEDGER.game.fares.state().log.slice(-1)[0] }));
ok(p.t - t0 >= 40 && p.log.outcome === 'out of the Hook and back' && r.paid >= 450, `forty minutes pass and the fare is paid (${Math.round(p.t - t0)} game minutes, ${r.paid}p)`);

// ---- a week of fares: none twice, no wrinkle twice running, few a day ----
r = await L(() => {
  const G = LEDGER.G, F = LEDGER.game.fares, s = F.state(), list = F.list(), seen = [], bad = [];
  s.done = []; s.lastWrinkle = null; s.week = 0; s.day = -1;
  G.story.flags.firstFareDone = 1;
  let perDay = {}, evening = {};
  for (let t = 1440 * 7 + 5 * 60; t < 1440 * 14; t += 20) {
    G.t = t;
    const id = F.next();
    if (!id) continue;
    const f = list.find((q) => q.id === id), d = Math.floor(t / 1440);
    if (seen.includes(id)) bad.push('twice: ' + id);
    if (f.wrinkle && f.wrinkle === s.lastWrinkle) bad.push('wrinkle twice running: ' + id);
    seen.push(id);
    s.done.push(id); s.lastWrinkle = f.wrinkle; s.offeredToday++;
    perDay[d] = (perDay[d] || 0) + 1;
    if ((t % 1440) / 60 >= 17) { s.eveningOffered++; evening[d] = (evening[d] || 0) + 1; }
  }
  return { n: seen.length, of: list.length, bad, most: Math.max(...Object.values(perDay)), mostEvening: Math.max(0, ...Object.values(evening)), wrinkles: [...new Set(list.map((f) => f.wrinkle).filter(Boolean))] };
});
ok(r.bad.length === 0 && r.n >= 20, `a week offers ${r.n} of the ${r.of} written fares, none twice, no wrinkle twice running ${r.bad.join('; ')}`);
ok(r.most <= 6 && r.mostEvening <= 3, `few and chosen: at most ${r.most} a day, ${r.mostEvening} an evening`);
ok(['talker', 'parcel', 'tail', 'runner', 'wait', 'hurry', 'face'].every((w) => r.wrinkles.includes(w)), 'all seven wrinkles are written: ' + r.wrinkles.join(', '));
r = await L(() => {
  const G = LEDGER.G, F = LEDGER.game.fares, s = F.state();
  s.done = []; s.lastWrinkle = null; s.day = -1;
  G.x.rise = Object.assign(G.x.rise || {}, { rung: 2 });
  const ids = [];
  for (let t = 1440 * 14 + 5 * 60; t < 1440 * 15; t += 20) {
    G.t = t;
    const id = F.next();
    if (id) { ids.push(id); s.done.push(id); s.offeredToday++; s.lastWrinkle = F.list().find((q) => q.id === id).wrinkle; }
  }
  G.x.rise.rung = 1;
  return { ids, plain: ids.filter((id) => !F.list().find((q) => q.id === id).wrinkle) };
});
ok(r.ids.length <= 3 && r.ids.length >= 1 && r.plain.length === 0, `the grind is where he starts, not where he stays: at rung 2 a day offers ${r.ids.join(', ')}, none plain`);

// ---- every place a fare names has an address and a landmark (ER-WAY-02) ----
r = await L(() => Object.entries(LEDGER.game.fares.places()).filter(([, p]) => !p.address || !p.landmark || !p.n).map(([k]) => k));
ok(r.length === 0, 'every place a fare names has an address and a landmark ' + r.join(','));
r = await L(() => ({ faults: LEDGER.game.faults, errors: 0 }));
ok(r.faults.length === 0, 'no fault in any system: ' + r.faults.slice(0, 2).join(' | '));
ok(h.errors.length === 0, 'no page errors: ' + h.errors.slice(0, 2).join(' | '));
await h.close();
console.log(bad ? 'FAIL' : 'PASS');
process.exit(bad ? 1 : 0);
