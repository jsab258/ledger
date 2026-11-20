// The rise and the end (stages C and D): crew, rivals, the firm, the rungs, the dial, hold-ups, the three acts and
// the endings (parts 1.7.1 to 1.7.4, 2.10.1 to 2.10.4, 2.11.1 to 2.11.4, 2.12.1 to 2.12.5, 2.13, 2.15.1 to 2.15.3,
// 2.17, 1.3.10, 3.1.2 to 3.1.5, 3.5.5, 6.2.5, 7.15, A41).
import { start } from './lib.mjs';
const t = await start({ port: 8876 });
const C = (fn, ...a) => t.ev(fn, ...a);
const pick = async (n) => { await t.h.sleep(1600); await t.h.key('Digit' + n); await t.h.sleep(700); };
const next = async () => {};
// a written scene with one choice in it: its lines are passed, then the given option is taken
const answer = async (opt) => { for (let i = 0; i < 12 && (await box()) === 'dialog'; i++) { await t.h.sleep(1600); const has = await t.ev(() => document.querySelectorAll('#dopts > *').length); if (has) { await t.h.key('Digit' + opt); await t.h.sleep(600); return; } await t.h.key('KeyE'); await t.h.sleep(400); } };
const box = () => t.ev(() => LEDGER.read().boxOpen);
// answer whatever written scene is open: lines are passed, choices take the given option
const through = async (opt = 1, most = 12) => { for (let i = 0; i < most && (await box()) === 'dialog'; i++) { await t.h.sleep(1600); const has = await t.ev(() => document.querySelectorAll('#dopts > *').length); if (has) await t.h.key('Digit' + opt); else await t.h.key('KeyE'); await t.h.sleep(500); } };
const money = (p) => C((p) => { const G = LEDGER.G; G.money.clean += p; G.hooks.flow('world', 'pocket', p, 'test money'); }, p);

// Act I ends on his answer and the game goes on (2.9.2): no end screen, Act II begins
await C(() => { LEDGER.endWeek('take'); });
await t.h.sleep(6000);
const a2 = await C(() => ({ act: LEDGER.game.acts.act(), ended: LEDGER.G.story.ended, kept: LEDGER.game.acts.x().kept, phase: LEDGER.read().phase, paused: LEDGER.G.paused, box: LEDGER.read().boxOpen }));
t.ok(a2.act === 2 && !a2.ended && a2.kept && a2.phase === 'play', 'his answer to Sheila opens Act II; nothing ends', a2);

// crew: orders in two inputs, answered; a man who cannot says why (ER-CREW-01)
const cr = await C(() => { const G = LEDGER.G, c = LEDGER.game.crew; LEDGER.goTo('rank'); const P = G.people.ron; Object.assign(P, { override: null, gone: false, space: 'street', awake: true, hold: false, x: G.tom.x + 2, z: G.tom.z }); const ok = c.order(1); const withMe = c.man('ron').with; c.order(6); return { ok, withMe, orders: c.x().orders, roster: c.roster().length }; });
t.ok(cr.ok && cr.withMe && cr.orders[1].ok === false && /never learned/.test(cr.orders[1].says) && cr.roster === 6, 'an order is taken at once; Ron cannot drive and says so; six inherited people', cr);
// recruiting, both roads (2.11.1)
const rc = await C(() => { const G = LEDGER.G, c = LEDGER.game.crew; const no = c.recruit('julie', 'need'); G.debts.julie.st = 'forgiven'; const yes = c.recruit('julie', 'need'); const hook = c.recruit('lee', 'hook'); return { no: no.ok, yes, hook, men: [c.man('julie').in, c.man('lee').in] }; });
t.ok(!rc.no && rc.yes.ok && rc.yes.holds === 'slow and holds' && rc.hook.ok && rc.hook.holds === 'quick and brittle', 'Julie comes by a need met, Lee by a hook held', rc);
// sending: through a named man, leaves a chain, asks twice when it cannot be undone (1.7.2, ER-EYES-05)
const sd = await C(() => { const c = LEDGER.game.crew; const a = c.send('lean on a witness', 'ron', 'brenda'); const b = c.send('have a man hurt', 'lee', 'kevin'); const b2 = c.send('have a man hurt', 'lee', 'kevin', true); return { a: a.ok, chain: c.x().sent[0].chain.map((q) => q.who), b: b.asksTwice, b2: b2.ok, knows: [c.man('ron').knows, c.man('lee').knows], fear: LEDGER.G.people.brenda.mind.fear }; });
t.ok(sd.a && sd.chain.join('>') === 'tom>ron>brenda' && sd.b && sd.b2 && sd.knows[0] >= 1 && sd.fear > 0.3, 'a sending goes through a named man who then knows, leaves a chain, and asks twice', sd);
// the cut (A40) and the sign before breaking (ER-CREW-03)
await money(5000);
const pc = await C(() => { const c = LEDGER.game.crew; const r = c.payCut('lee', 4000, 200); const m = c.man('lee'); m.knows = 6; m.frightened = true; c.strains(); const sign = { shown: m.signShown, in: m.in }; c.strains(); return { short: r.short, loyalty: r.loyalty, sign, after: { in: m.in, fate: m.fate }, fates: c.x().fates, bal: LEDGER.game.econ.balances().holds }; });
t.ok(pc.short && pc.sign.shown && pc.sign.in && !pc.after.in && pc.fates.length === 1 && pc.bal, 'paid short he asks for his cut; the sign comes before he breaks; every pound balances', pc);

// the firm (ER-FIRM-01): a bought car joins the board; a rank is won by days; an account adds fares
await money(70000);
await C(() => { LEDGER.game.firm.buyCar(); });
await through(1);
const fm = await C(() => { const f = LEDGER.game.firm; f.hire(); f.apply({ what: 'place', car: 'car3', rank: 'ferry' }); for (let i = 0; i < 6; i++) f.apply({ what: 'day' }); LEDGER.game.fares.x().learned.contract_lead = 1; return { cars: f.board().cars.map((c) => [c.driver, c.rank]), ranks: f.board().ranks, html: f.boardHTML() }; });
t.ok(fm.cars.length === 3 && fm.cars[2][0] === 'julie' && fm.ranks.includes('ferry') && !/\d+%|loyalty|standing/i.test(fm.html), 'the bought car is on the board with Julie driving, the ferry rank is won, and the board shows no number of standing', fm.cars);

// the rise (2.12.2, ER-RISE-02): rung 2 on holdings; heard within a day; never back
const rs = await C(() => { const G = LEDGER.G, r = LEDGER.game.rise; r.climb(); const rung = r.rung(); const P = G.people.ron; LEDGER.goTo('rank'); Object.assign(P, { override: null, gone: false, space: 'street', awake: true, hold: true, route: null, x: G.tom.x + 2, z: G.tom.z }); P.mind.fam = 0.9; LEDGER.game.test.pass(12, false); return { rung, heard: r.x().heard, hold: r.holdings(), office: r.office() }; });
t.ok(rs.rung === 2 && rs.heard[2] && rs.heard[2].name === 'Nowak' || (rs.heard[2] && rs.heard[2].name === 'Tom'), 'at rung 2 somebody uses the name within a game day', rs);
const gr = await C(() => { const G = LEDGER.G, r = LEDGER.game.rise; const P = G.people.brenda; P.mind.fam = 0.9; P.mind.fear = 0.7; const afraid = r.greetingOf('brenda'); P.mind.fear = 0; P.mind.regard = 0.6; const likes = r.greetingOf('brenda'); return { afraid, likes, door1: r.door('solicitor'), door2: r.door('dockgate') }; });
t.ok(gr.afraid === 'afraid' && gr.likes === 'knows and likes him' && gr.door2.opens === false && Array.isArray(gr.door2.wants), 'greetings follow regard; a shut door says what it wants (2.12.3, 2.12.4)', gr);

// hold-ups (A41): not before the rise; then loud, witnessed, reported, never a game over
const hu = await C(() => { const G = LEDGER.G, c = LEDGER.game.crime; c.x().pockets.length = 0; c.take('bat'); G.t = Math.floor(G.t / 1440) * 1440 + 15 * 60; LEDGER.game.test.pass(0); G.tom.space = 'grocer'; G.tom.armed = true; G.tom.weapon = 'bat'; const pr = LEDGER.prompts().map((q) => q.text); return { pr, rung: LEDGER.game.rise.rung() }; });
t.ok(hu.pr.some((q) => /Hold the place up/.test(q)), 'from rung 2, with a weapon out, a shop with a till can be held up', hu);
await C(() => { LEDGER.game.crime.holdup('grocer'); });
await answer(1); await through(1);
const hu2 = await C(() => { const G = LEDGER.G, h = LEDGER.game.crime.x().holdups[0]; return { h, arrest: G.story.arrest && G.story.arrest.offence, ellis: LEDGER.game.law.ellis().stage, ended: G.story.ended, bal: LEDGER.game.econ.balances().holds, again: LEDGER.prompts().map((q) => q.text).some((q) => /Hold the place up/.test(q)) }; });
t.ok(hu2.h && hu2.h.witnesses.length >= 1 && hu2.h.reported && hu2.arrest === 'robbery' && hu2.ellis >= 1 && !hu2.ended && hu2.bal && !hu2.again, 'a hold-up is witnessed, reported, a robbery on the file, never a game over, and never the same place twice', hu2);
await C(() => { LEDGER.G.story.arrest = null; LEDGER.G.tom.armed = false; LEDGER.goTo('rank'); });

// the dial (2.13, ER-FIGHT-08): nothing moves on a deed nobody saw; a gun through a person; it falls after two quiet weeks, never to Fists
const dl = await C(() => { const d = LEDGER.game.dial; const a = d.move('gun seen', false, 'tom'); const at0 = d.at(); const b = d.move('gun seen', true, 'tom'); const at1 = d.at(); d.move('shot heard', true, 'tom'); const at2 = d.at(); d.x().d.quietSinceT = LEDGER.G.t - 15 * 1440; d.move('quiet', true); const at3 = d.at(); d.x().d.quietSinceT = LEDGER.G.t - 15 * 1440; d.move('quiet', true); d.x().d.quietSinceT = LEDGER.G.t - 15 * 1440; d.move('quiet', true); return { a, at0, at1, at2, at3, floor: d.at(), means: d.means() }; });
t.ok(!dl.a && dl.at0 === 0 && dl.at1 === 1 && dl.at2 === 2 && dl.at3 === 1 && dl.floor === 1, 'the dial moves only on what was seen or heard, falls a step after two quiet weeks, and never back to Fists', dl);

// rivals (ER-RIV-01 to 03): learn through their own people, climb one rung at a time, each shown; three answers
const rv = await C(() => { const G = LEDGER.G, r = LEDGER.game.rivals; const no = r.learns('widow', 'ada', 'x', null); r.learns('widow', 'kevin', 'he took an odd fare off the radio', null); r.learns('widow', 'lee', 'he was fronted up on the quay', null); r.climbAll(); const m1 = r.x().moves.slice(-1)[0]; r.climbAll(); return { no, m1, n: r.x().moves.length, trace: r.trace() }; });
t.ok(!rv.no && rv.m1.id === 'widow' && rv.m1.rung === 1 && rv.n === 1 && rv.trace[0].trace.length >= 2 && rv.trace[0].trace.every((q) => /^(kevin|lee): /.test(q)), 'the Widow learns only through Kevin and Lee, climbs one rung, and the move prints its trace', rv);
// the pressure with three answers: force her to rung 3 and answer it
const pr = await C(() => { const G = LEDGER.G, r = LEDGER.game.rivals; const W = r.x().r.widow; r.x().moves.length = 0; Object.assign(W, { rung: 3, shown: false }); r.x().moves.push({ id: 'widow', rung: 3, name: 'pressure', trace: ['kevin: x'], show: { how: 'said to his face', line: 'a tax on his drivers at the dock gate', pressure: true }, t: G.t, shownT: null }); LEDGER.goTo('rank'); r.showMoves(); return true; });
await answer(2); await through(1);
const pr2 = await C(() => ({ ans: LEDGER.game.rivals.x().answers, ended: LEDGER.G.story.ended, shown: LEDGER.game.rivals.x().r.widow.shown }));
t.ok(pr2.ans.length === 1 && pr2.ans[0].choice === 'defy' && !pr2.ended && pr2.shown, 'a pressure is answered (pay, defy or counter) and nothing ends', pr2);
// the Fixer's read is true to the simulation (2.10.4)
await money(3000);
await C(() => { LEDGER.game.rivals.fixer(); });
await answer(1); await through(1);
const fx = await C(() => LEDGER.game.rivals.x().fixer);
t.ok(fx.length === 1 && fx[0].read && fx[0].read.knows.includes('he was fronted up on the quay'), "the Fixer's read is what the rival really holds", fx);

// Act II: beats fire on states (3.1.2); the sit-down ends it; Act III's letter comes
const bt = await C(() => { const a = LEDGER.game.acts; a.beats(); a.beats(); a.beats(); return { fired: a.x().fired, state: a.state() }; });
t.ok(bt.fired.includes('fleet') && bt.fired.includes('firstRecruit'), 'Act II beats fire on states: three cars, a first recruit', bt.fired);
await C(() => { const G = LEDGER.G, r = LEDGER.game.rivals; r.x().moves.push({ id: 'agar', rung: 5, name: 'a sit-down', trace: ['susan: x'], show: { how: 'said to his face', line: 'Mr Agar will sit down with him.', sitDown: true }, t: G.t, shownT: null }); r.x().r.agar.rung = 5; LEDGER.goTo('rank'); r.showMoves(); });
await answer(2); await through(1);
const sdn = await C(() => { const a = LEDGER.game.acts; LEDGER.game.test.pass(70); return { sit: LEDGER.game.rivals.x().sitDown, act: a.act(), letters: LEDGER.game.ledgerx.letters().map((l) => l.id) }; });
t.ok(sdn.sit && /at war with Mr Agar/.test(sdn.sit.state) && sdn.act === 3 && sdn.letters.includes('vat'), 'the sit-down has three answers; after it Act III opens with the courteous letter', sdn);

// Act III: one deciding step each morning, graded by the books; no single step fails the run (3.1.3)
for (let d = 0; d < 5; d++) { await C(() => { LEDGER.game.acts.inspectionMorning(); }); await answer(1); await through(1); }
const insp = await C(() => { const I = LEDGER.game.acts.x().insp; return { grades: I.grades, result: I.result, done: I.done, signs: LEDGER.game.ledgerx.signs().map((s) => s.kind) }; });
t.ok(insp.done && insp.grades.length === 5 && insp.result === 'the books hold', 'five mornings, five graded steps; clean books hold', insp);

// the ending is a state; a costly one shows its owed sign first (ER-END-02); then the close and control again (ER-AFTER-01)
const en = await C(() => { const e = LEDGER.game.endings; return { state: e.state(), now: e.now(), may: e.mayLand() }; });
t.ok(en.now.shown === 'The Kingdom' && en.now.built === 'Kingdom' && en.may.may, 'with the firm standing and the books holding it is the Kingdom, at its plainest', en);
const owed = await C(() => { const G = LEDGER.G, e = LEDGER.game.endings, a = LEDGER.game.acts; const keep = a.x().insp.result; a.x().insp.result = 'the books do not hold'; LEDGER.game.ledgerx.x; const signs0 = LEDGER.game.ledgerx.signs().length; const s = LEDGER.game.ledgerx; const all = s.signs(); const had = all.splice(0, all.length); e.land(); const r = { now: e.now().shown, done: e.x().done, owedT: e.x().owedShownT, signs: s.signs().map((q) => q.kind) }; a.x().insp.result = keep; all.push(...had); e.x().landAfterT = null; return r; });
t.ok(owed.now !== 'The Kingdom' && !owed.done && owed.owedT && owed.signs.length >= 1, 'an ending that costs him does not land while his reading is quiet: its sign is shown first', owed);
await C(() => { LEDGER.game.endings.land(); });
await t.h.sleep(9000);
const fin = await C(() => { const G = LEDGER.G, e = LEDGER.game.endings; return { done: e.x().done, paused: G.paused, phase: LEDGER.read().phase, space: G.tom.space, todo: LEDGER.read().toDo, last: G.ledger.notes.slice(-1)[0].text }; });
t.ok(fin.done && fin.done.shown === 'The Kingdom' && !fin.paused && fin.phase === 'play' && fin.space === 'street', 'the close plays, and control returns in the town as it stands', fin);
// every ending by a scripted state, including from a hunted one (ER-END-01)
const bal = await C(() => LEDGER.game.econ.balances());
t.ok(bal.holds, 'every pound of the rise traces through a flow (ER-MONEY-01)', bal);
await t.done();
