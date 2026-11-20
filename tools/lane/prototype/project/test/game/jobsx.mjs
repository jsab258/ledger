// The one-shot: the job template at work (parts 3.5.6, 3.5.7, 3.5.1, 3.5.2, 2.8.2, 2.9.1, 2.9.2, 7.14).
// ER-JOB-02, 03, 04, 05, 06, 07 and ER-REACH-01, through the game's test hook.
import { launch } from '../harness.mjs';
let bad = 0;
const ok = (c, what) => { console.log((c ? 'ok   ' : 'FAIL ') + what); if (!c) bad++; };
const h = await launch({ port: 8830, quality: 'low' });
try {
  await h.newWeek();
  const J = () => h.ev(() => LEDGER.game.jobsx);
  // --- the data: the six laws ---
  const d = await h.ev(() => {
    const X = LEDGER.game.jobsx, specs = X.specs();
    return { faults: X.check(), n: specs.length, families: [...new Set(specs.map((s) => s.family))], channels: [...new Set(specs.map((s) => s.channel.kind))],
      approaches: specs.map((s) => s.approaches.length), noMarkers: specs.every((s) => s.steps.every((st) => LEDGER.game.crime.places()[st.place].landmark)),
      words: specs.flatMap((s) => s.steps.flatMap((st) => Object.values(st.outcomes).map((o) => o.line.split(/\s+/).length))) };
  });
  ok(d.faults.length === 0, 'every job passes the laws as data (ER-JOB-02, 03, 05, ER-REACH-01): ' + JSON.stringify(d.faults.slice(0, 4)));
  ok(d.n >= 10 && ['carry', 'collection', 'break-in', 'lift', 'tail', 'minding', 'damage'].every((f) => d.families.includes(f)), d.n + ' jobs across the families: ' + d.families.join(', '));
  ok(['counter', 'street', 'message', 'phone', 'car'].every((c) => d.channels.includes(c)), 'every channel of A17 is used: ' + d.channels.join(', '));
  ok(d.approaches.every((n) => n >= 3), 'three keys to every lock');
  const avg = d.words.reduce((a, b) => a + b, 0) / d.words.length;
  ok(avg > 16 && avg < 28, 'Ledger lines of about 22 words (mean ' + avg.toFixed(1) + ')');
  // --- every outcome of every job reached by a script, each leaving a Ledger line (ER-JOB-05) ---
  const all = await h.ev(() => {
    const X = LEDGER.game.jobsx, G = LEDGER.G, out = [];
    for (const s of X.specs()) for (const r of X.routes(s.id)) {
      const notes0 = G.ledger.notes.length, sent0 = X.sent().length;
      X.start(s.id);
      let okAll = true;
      for (const [step, o] of r.path) okAll = X.finish(s.id, step, o) && okAll;
      const run = X.run(s.id), lines = G.ledger.notes.slice(notes0).map((n) => n.text);
      const want = r.path.map(([step, o]) => s.steps.find((x) => x.id === step).outcomes[o].line);
      out.push({ id: s.id, route: r.path.map((p) => p.join('/')).join(' > '), ok: okAll && run.st === r.ends && want.every((w) => lines.includes(w)), ended: X.sent().slice(sent0).some((e) => e.name === 'job:end' && e.job === s.id) });
    }
    return out;
  });
  const badR = all.filter((r) => !r.ok || !r.ended);
  ok(all.length > 30 && badR.length === 0, all.length + ' routes through ' + d.n + ' jobs each reach their end with a Ledger line a step: ' + JSON.stringify(badR.slice(0, 3)));
  ok((await h.ev(() => LEDGER.game.faults.length)) === 0, 'no system fault: ' + JSON.stringify(await h.ev(() => LEDGER.game.faults.slice(0, 2))));
  // --- offered by a person, on a state (law 1) ---
  const off = await h.ev(() => {
    const X = LEDGER.game.jobsx, G = LEDGER.G, S = X.state();
    S.runs = {}; S.lastOffer = {}; S.variety = []; S.arrangement = null;
    G.t = 4 * 1440 + 19 * 60;
    const before = X.offerFor('ron');
    G.story.flags.tour = 1; G.story.flags.ask1 = 'yes'; G.story.flags.metRon = 1;
    return { before, after: X.offerFor('ron'), sheila: X.offerFor('sheila'), due: X.due() };
  });
  ok(off.before === null && off.after === 'ask_fri', 'Ron offers the Friday envelope only once the office is his and the arrangement stands: ' + JSON.stringify(off));
  // Ron's offer, taken in talk: walk up, E, yes
  const took = await h.ev(async () => {
    const G = LEDGER.G, R = G.people.ron, X = LEDGER.game.jobsx;
    R.space = 'street'; R.gone = false; R.x = 6.2; R.z = 38.5; R.route = null; R.moving = false;
    LEDGER.goTo({ xMetres: 5.2, zMetres: 39.6 });
    G.tom.ang = Math.atan2(R.x - G.tom.x, R.z - G.tom.z);
    LEDGER.step(0.3);
    const p = LEDGER.prompts();
    LEDGER.press('E');
    LEDGER.step(0.2);
    let w = LEDGER.written.read();
    for (let i = 0; i < 6 && w.open && !w.waitsForAChoice; i++) w = await LEDGER.written.next();
    const asked = w.text, choices = w.choices;
    if (w.waitsForAChoice) await LEDGER.written.choose(0);
    LEDGER.step(0.3);
    return { p, asked, choices, run: X.run('ask_fri'), carried: LEDGER.game.crime.carried(), todo: G.story.objective, paused: G.paused };
  });
  ok(took.run && took.run.st === 'taken' && took.carried.coat.includes('the envelope'), 'said yes to Ron: the job is taken and the envelope is under the coat: ' + JSON.stringify([took.asked && took.asked.slice(0, 40), took.run && took.run.st, took.carried]));
  ok(/Harbour Board/.test(took.todo) && !took.paused, 'the to-do names the place by its landmark: ' + took.todo);
  // --- windows, not minutes: early at the door there is a "wait until" (ER-JOB-04) ---
  const win = await h.ev(async () => {
    const G = LEDGER.G, pl = LEDGER.game.crime.places().j_harbour;
    LEDGER.goTo({ xMetres: pl.x, zMetres: pl.z + 1.2 });
    LEDGER.step(0.2);
    const early = LEDGER.prompts().map((p) => p.text);
    LEDGER.press('T');
    for (let i = 0; i < 400 && (G.t % 1440) / 60 < 22; i++) { LEDGER.step(0.5); await new Promise((r) => setTimeout(r, 0)); }
    LEDGER.goTo({ xMetres: pl.x, zMetres: pl.z + 1.2 });
    LEDGER.step(0.5);
    return { early, hourAfter: (G.t % 1440) / 60, now: LEDGER.prompts().map((p) => p.text), paused: G.paused };
  });
  ok(win.early.some((t) => /Wait here until/.test(t)) && !win.early.some((t) => /hand over/.test(t)), 'early at the door: a wait is offered, not a failure: ' + JSON.stringify(win.early));
  ok(win.hourAfter >= 22 && win.now.some((t) => /hand over/.test(t)), 'the wait ends inside the window and the hand-over is on offer: ' + win.hourAfter.toFixed(2) + ' ' + JSON.stringify(win.now));
  // --- 3.5.1 the carry: three routes each finish ---
  const routes = await h.ev(() => {
    const G = LEDGER.G, X = LEDGER.game.jobsx, spec = X.specs().find((s) => s.id === 'ask_fri'), res = [];
    for (const route of spec.routes) {
      X.start('ask_fri');
      G.t = 4 * 1440 + 23 * 60;
      const tin0 = G.money.dirty;
      let clear = true;
      for (const [x, z] of route) { LEDGER.goTo({ xMetres: x, zMetres: z }); LEDGER.step(0.3); clear = clear && LEDGER.isClearOnFoot(x, z); }
      const p = LEDGER.prompts().find((q) => /hand over/.test(q.text));
      if (p) LEDGER.press(p.key);
      LEDGER.step(0.3);
      res.push({ clear, prompt: !!p, st: X.run('ask_fri').st, paid: G.money.dirty - tin0 });
    }
    return res;
  });
  ok(routes.length === 3 && routes.every((r) => r.st === 'done' && r.paid === 7000), 'the carry finishes by each of its three routes and pays the tin: ' + JSON.stringify(routes));
  // --- steps settle by the clock while he is away (ER-JOB-07), and a failure continues (law 4) ---
  const late = await h.ev(() => {
    const G = LEDGER.G, X = LEDGER.game.jobsx;
    G.t = 4 * 1440 + 19 * 60; X.start('ask_fri');
    G.t = 5 * 1440 + 2 * 60; X.settleAll();
    const r = X.run('ask_fri');
    return { st: r.st, outcome: r.outcome, line: r.lines[r.lines.length - 1].line, dropped: G.events.some((e) => e.kind === 'job_dropped'), phase: G.story.phase };
  });
  ok(late.st === 'failed' && late.outcome === 'late' && late.dropped && late.phase === 'play', 'a missed window ends the job as late, Ron hears, and play goes on: ' + JSON.stringify(late));
  // --- 7.14 no set piece twice in thirty minutes (ER-JOB-06) ---
  const vr = await h.ev(() => {
    const X = LEDGER.game.jobsx, S = X.state();
    S.variety = []; X.start('ask_fri');
    const blocked = !X.varietyOk('ask_sun'), other = X.varietyOk('brk_hut');
    LEDGER.G.played += 1900;
    return { blocked, other, later: X.varietyOk('ask_sun'), faults: X.variety() };
  });
  ok(vr.blocked && vr.other && vr.later && vr.faults.length === 0, 'the same set piece is not offered again inside thirty minutes; another is: ' + JSON.stringify(vr));
  // --- 2.9.2 keeping or ending the arrangement ---
  const arr = await h.ev(() => {
    const X = LEDGER.game.jobsx, S = X.state();
    S.arrangement = null; S.runs = {};
    X.start('ask_sun'); const kept = X.arrangement();
    S.arrangement = null; S.runs = {};
    X.refuse('ask_sun'); const ended = X.arrangement();
    return { kept, ended, sent: X.sent().filter((e) => e.name === 'jobs:arrangement').slice(-2).map((e) => e.arrangement) };
  });
  ok(arr.kept === 'kept' && arr.ended === 'ended' && arr.sent.join() === 'kept,ended', 'the last ask keeps or ends the arrangement, and says so: ' + JSON.stringify(arr));
  // --- 2.8.2 a debtor pays what his purse holds; the rest stays on the book ---
  const debt = await h.ev(() => {
    const G = LEDGER.G, X = LEDGER.game.jobsx;
    G.t = 1 * 1440 + 12 * 60; LEDGER.step(0.2);
    X.start('col_wayne');
    const tin0 = G.money.dirty;
    G.hooks.yielded(G.people.wayne, { type: 'debt' }, 4);
    const w = Object.assign({}, G.debts.wayne), paidW = G.money.dirty - tin0;
    for (let i = 0; i < 30; i++) LEDGER.step(0.5);
    const tin1 = G.money.dirty;
    G.hooks.yielded(G.people.lee, { type: 'debt' }, 1);
    const l1 = Object.assign({}, G.debts.lee), paidL1 = G.money.dirty - tin1;
    G.hooks.yielded(G.people.lee, { type: 'debt' }, 4);
    const l2 = Object.assign({}, G.debts.lee);
    G.hooks.yielded(G.people.julie, { type: 'debt' }, 4);
    return { w, paidW, run: X.run('col_wayne'), l1, paidL1, l2, julie: G.debts.julie, flows: G.money.earnedDirty };
  });
  ok(debt.paidW === 900 && debt.w.owed === 2100 && debt.w.st === 'open', "Wayne pays the nine pounds in his purse and twenty-one stays on the book: " + JSON.stringify([debt.paidW, debt.w]));
  ok(debt.run.st === 'done' && debt.run.outcome === 'part', 'the collection ends as part paid, with its line: ' + JSON.stringify([debt.run.st, debt.run.outcome]));
  ok(debt.paidL1 === 750 && debt.l1.owed === 750 && debt.l2.st === 'paid' && debt.l2.owed === 0, 'below a threat Lee parts with half his purse; threatened, the rest: ' + JSON.stringify([debt.paidL1, debt.l1, debt.l2]));
  ok(debt.julie.st === 'open' && debt.julie.owed === 900, 'Julie cannot pay: nothing comes however far it goes');
  // --- every change saved: a run comes back from a save as it was ---
  const sv = await h.ev(() => {
    const G = LEDGER.G, X = LEDGER.game.jobsx;
    X.state().runs = {}; X.start('brk_pawn'); X.finish('brk_pawn', 'in', 'loud');
    const before = JSON.stringify(X.run('brk_pawn'));
    LEDGER.saveNow(false);
    const json = localStorage.getItem('ledger.save.v' + G.v);
    X.state().runs = {};
    LEDGER.restore(json);
    return { same: JSON.stringify(LEDGER.game.jobsx.run('brk_pawn')) === before, cur: LEDGER.game.jobsx.run('brk_pawn').cur };
  });
  ok(sv.same && sv.cur === 'cupboard', 'a job half done is the same job after save and load: ' + JSON.stringify(sv));
  ok((await h.ev(() => LEDGER.game.faults.length)) === 0, 'no system fault at the end: ' + JSON.stringify(await h.ev(() => LEDGER.game.faults.slice(0, 2))));
  ok(h.errors.length === 0, 'no page errors: ' + h.errors.slice(0, 2).join(' | '));
} catch (e) {
  console.log('TEST FAIL', e.stack || e); bad++;
}
await h.close();
console.log(bad ? 'FAIL' : 'PASS');
process.exit(bad ? 1 : 0);
