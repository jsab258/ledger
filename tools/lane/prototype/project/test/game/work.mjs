// The cab in the town, fares with stories, shops, the written jobs, the town's days and the boxing club
// (parts 1.2.4, 1.2.5, 1.2.8 to 1.2.11, 3.4.1 to 3.4.3, 2.7.5, 2.7.8, 1.6.10, 3.5.3 to 3.5.7, 3.3, 2.1.6, 2.4.5,
// 3.7, 2.16, 7.16, 2.18).
import { start } from './lib.mjs';
const t = await start({ port: 8875 });
const C = (fn, ...a) => t.ev(fn, ...a);
const pick = async (n) => { await t.h.sleep(1600); await t.h.key('Digit' + n); await t.h.sleep(700); };
// any written scene still open is answered with its first choice, so the game is never left paused
const clear = async () => { for (let i = 0; i < 8 && (await t.ev(() => LEDGER.read().boxOpen)) === 'dialog'; i++) { await t.h.sleep(1600); await t.h.key('KeyE'); await t.h.key('Digit1'); await t.h.sleep(500); } };

// the job specs are sound by the job rule (ER-JOB-01 to 05, ER-REACH-01), and the fares' ways are whole
const sp = await C(() => ({ faults: LEDGER.game.jobsx.specFaults(), n: LEDGER.game.jobsx.specs().length, ways: LEDGER.game.fares.wayFaults(), fares: LEDGER.game.fares.list().length, wr: [...new Set(LEDGER.game.fares.list().map((f) => f.wrinkle))] }));
t.ok(!sp.faults.length && sp.n >= 11, 'every written job has a giver, a channel, three keys and landmarks', sp.faults);
t.ok(!sp.ways.length && sp.fares >= 14 && ['talker', 'parcel', 'tail', 'runner', 'wait', 'hurry', 'face'].every((w) => sp.wr.includes(w)), 'fourteen written fares, all seven wrinkles, each with its way by landmark', sp);

// fares: few and chosen, none twice in a week (ER-JOB-06, his direction)
const fr = await C(() => { const G = LEDGER.G, f = LEDGER.game.fares; G.t = 1 * 1440 + 18 * 60; const got = []; for (let i = 0; i < 6; i++) { const n = f.next(); got.push(n ? n.id : null); G.played += 2000; } return { got, log: f.x().log.length }; });
t.ok(fr.got.filter(Boolean).length === 3 && new Set(fr.got.filter(Boolean)).size === 3 && fr.got[3] === null, 'three fares an evening at most, no two alike', fr.got);

// a hit: the choice is put at once, both answers play on, nobody dies (ER-DRIVE-03, 05, 10)
await C(() => { const G = LEDGER.G; G.t = 2 * 1440 + 11 * 60; LEDGER.game.test.pass(0); LEDGER.cab.getIn(); const P = G.people.nora; Object.assign(P, { override: null, gone: false, space: 'street', awake: true, x: G.car.x + 3, z: G.car.z }); LEDGER.game.cars.hit('nora', 9); });
await pick(1);
const h1 = await C(() => ({ hits: LEDGER.game.cars.x().hits, share: LEDGER.game.econ.fareShare(), hosp: Object.keys(LEDGER.game.cars.x().inHospital), dead: !!LEDGER.G.people.nora.dead, ended: LEDGER.G.story.ended }));
t.ok(h1.hits[0].choice === 'stopped' && h1.share === 1 && !h1.dead && !h1.ended && h1.hosp.includes('nora'), 'stop and help: the ambulance takes her, nobody dies, the firm keeps its fares', h1);
await C(() => { const G = LEDGER.G; const P = G.people.albert; Object.assign(P, { override: null, gone: false, space: 'street', awake: true }); LEDGER.game.cars.hit('albert', 14); });
await pick(2);
await clear();
const h2 = await C(() => ({ hit: LEDGER.game.cars.x().hits[1], share: LEDGER.game.econ.fareShare(), kinds: LEDGER.G.events.slice(-6).map((e) => e.kind), dead: !!LEDGER.G.people.albert.dead }));
t.ok(h2.hit.choice === 'drove off' && h2.share < 1 && h2.kinds.includes('hit_and_run') && !h2.dead, 'drive off: a hit-and-run, the firm loses fares for a while, nobody dies', h2);
const fb = await C(() => { const G = LEDGER.G; const x = LEDGER.game.econ.x(); const until = x.fareShareUntilT; LEDGER.game.test.pass(until - G.t + 5); return LEDGER.game.econ.fareShare(); });
t.ok(fb === 1, 'the fares come back as the talk fades (2.15.3)', fb);

await clear(); await t.h.sleep(3000); await clear(); // somebody saw the hit-and-run and rang: the morning's officer is answered (he goes with him)
// crashes (ER-DRIVE-01): from about 35 mph it will not drive on, says so, and comes back next day
const cr = await C(() => { const c = LEDGER.game.cars; c.crash(4); const a = !!c.x().wrecked; c.crash(16); const b = c.x().wrecked; const stages = c.x().crashes.map((q) => q.stage); LEDGER.game.test.pass(26 * 60); return { a, b: !!b, stages, back: !c.x().wrecked }; });
t.ok(!cr.a && cr.b && cr.stages[1] === 'will not drive on' && cr.back, 'a hard hit takes the car off the road for a day; a touch is forgiven', cr);

// the horn (A32): heard inside its reach only
const hn = await C(() => { const G = LEDGER.G; LEDGER.cab.getIn(); const A = G.people.ron, B = G.people.lee; Object.assign(A, { override: null, gone: false, space: 'street', awake: true, x: G.car.x + 20, z: G.car.z, alert: null }); Object.assign(B, { override: null, gone: false, space: 'street', awake: true, x: G.car.x, z: G.car.z - 200, alert: null }); LEDGER.game.cars.horn(); const r = { near: !!A.alert, far: !!B.alert }; LEDGER.cab.getOut(); return r; });
t.ok(hn.near && !hn.far, 'the horn turns heads inside its reach and nobody outside it', hn);

// shops (ER-SPEND-01, ER-COAT-01): sells only its list, by its hours; a new coat is a new mark
const sh = await C(() => { const G = LEDGER.G, s = LEDGER.game.shops; G.t = 3 * 1440 + 10 * 60; LEDGER.game.test.pass(0); G.money.clean += 9000; G.hooks.flow('world', 'pocket', 9000, 'test money'); const a = s.buy('iron', 'torch'), b = s.buy('iron', 'goodOvercoat'), c = s.buy('chandler', 'decentJacket'); G.t += 12 * 60; const d = s.buy('iron', 'crowbar'); return { a: a.ok, b: b.why, c: c.ok, d: d.why, outfit: s.outfit(), has: LEDGER.game.crime.has('torch'), bal: LEDGER.game.econ.balances().holds }; });
t.ok(sh.a && sh.b === 'not on its list' && sh.c && sh.d === 'shut' && sh.outfit === 'a decent jacket' && sh.has && sh.bal, 'a shop sells only its list, by its hours, and every purchase balances', sh);

// a written job end to end by its events: the hut (ER-JOB-05), with the tester's skip on another (ER-JOB-07)
const jb = await C(() => { const j = LEDGER.game.jobsx, c = LEDGER.game.crime, G = LEDGER.G; j.start('hut'); const st0 = j.job('hut').st; G.tom.space = 'street'; G.tom.x = -101.5; G.tom.z = 28; c.wayIn('hut', 'force'); const step1 = j.job('hut').step; c.search('hut', 'tinbox'); c.finishDoing(); const done = j.job('hut'); j.start('damage_portside'); j.skip('damage_portside'); return { st0, step1, st: done.st, lines: done.lines.length, skipped: j.job('damage_portside').st, todo: LEDGER.read().toDo }; });
t.ok(jb.st0 === 'taken' && jb.step1 === 1 && jb.st === 'done' && jb.lines >= 3 && jb.skipped === 'done', 'a job runs from its giver to its last step by what the hands do, each step a Ledger line', jb);
const jr = await C(() => { const j = LEDGER.game.jobsx; j.start('lift_coin'); j.event('lift_coin', { what: 'fail', how: 'caught' }); const a = j.job('lift_coin'); return { st: a.st, how: a.how, lines: a.lines.length }; });
t.ok(jr.st === 'failed' && jr.lines === 2, 'a failed job ends in a line the town can talk about; nothing restarts', jr);

// minding (1.6.5): standing with somebody is recorded as stood with
await clear();
const md = await C(() => { const j = LEDGER.game.jobsx, G = LEDGER.G; G.story.arrest = null; G.t = (Math.floor(G.t / 1440) + 1) * 1440 + 18 * 60; LEDGER.game.test.pass(0); j.start('mind_ron'); G.tom.space = 'street'; G.tom.x = 16; G.tom.z = -38; for (let i = 0; i < 20 && j.job('mind_ron').st === 'taken'; i++) LEDGER.step(1); return { st: j.job('mind_ron').st, kinds: G.events.slice(-4).map((e) => e.kind), dbg: [G.paused, G.pauseWhy, G.tom.inCar, j.job('mind_ron').mindT, LEDGER.read().boxOpen, G.t / 1440] }; });
await clear();
const md2 = await C(() => { const j = LEDGER.game.jobsx, G = LEDGER.G; for (let i = 0; i < 60 && j.job('mind_ron').st === 'taken'; i++) LEDGER.step(1); return { st: j.job('mind_ron').st, minded: G.events.some((e) => e.kind === 'minded'), paused: G.pauseWhy }; });
t.ok(md2.st === 'done' && md2.minded, 'minding is recorded as "stood with"', [md, md2]);

// the calendar (ER-CAL-01) and the paper (ER-PAPER-01)
const cal = await C(() => { const l = LEDGER.game.life, G = LEDGER.G; const t0 = G.t; G.t = 3 * 1440 + 12 * 60; const thu = l.crowd(10); G.t = 2 * 1440 + 12 * 60; const wed = l.crowd(10); G.t = t0; return { thu, wed, today: l.today() }; });
t.ok(cal.thu < cal.wed, 'market day empties the Hook: fewer walkers on Thursday at noon than on Wednesday', cal);
const pp = await C(() => { const G = LEDGER.G, l = LEDGER.game.life; let d = Math.floor(G.t / 1440) + 1; while (!(d % 7 === 1 || d % 7 === 4) || l.x().papers[d]) d++; G.t = d * 1440 + 5 * 60; const E = G.events.find((e) => e.kind === 'hit_and_run'); const A = G.people.alison; if (!A.mind.by[E.id]) { const m = { e: E.id, src: 'told', from: 'grace', who: 'man', sure: 0.7, heat: 0.8, t: G.t, said: false, hop: 1, face: 0 }; A.mind.mem.push(m); A.mind.by[E.id] = m; } A.mind.by[E.id].sure = 0.7; l.printPaper(d); const p = l.x().papers[d]; return { lines: p ? p.lines : null, readers: ['k_news', 'grace', 'sheila'].every((id) => !!G.people[id].mind.by[E.id]) }; });
t.ok(pp.lines && pp.lines.length >= 1 && pp.lines.every((l) => l.from && l.e) && pp.readers, 'every printed line traces to what Alison saw or was told, and the paper spreads it', pp);

// a street happening is placed by its state, never a roll (ER-HAPPEN-01), and takes a choice with the hands
await clear();
const hp = await C(() => { const G = LEDGER.G, l = LEDGER.game.life; G.story.arrest = null; l.x().live = null; l.x().happened = []; let d = Math.floor(G.t / 1440) + 1; while (d % 7 !== 3) d++; G.t = d * 1440 + 9 * 60; G.tom.space = 'street'; G.tom.inCar = false; G.tom.x = 29.5; G.tom.z = 8; l.placeHappenings(); return { live: l.x().live, states: l.states().marketDay, dbg: [G.t / 1440, l.x().happened.slice(-3), G.tom.x, G.tom.z, G.played] }; });
t.ok(hp.live && hp.live.by.length >= 1, 'a street happening is placed by its named states, never a roll', hp);
await C((id) => { LEDGER.game.life.happening(id); }, hp.live.id);
await pick(1);
await clear();
const hp2 = await C(() => ({ log: LEDGER.game.life.x().happened.slice(-1)[0], returns: LEDGER.game.life.x().returns.length }));
t.ok(['helped', 'stepped_in'].includes(hp2.log.taken), 'the choice with the hands is taken and remembered', hp2);

// the boxing club (ER-PASTIME-01): no stakes anywhere
await clear();
const bal0 = await C(() => LEDGER.G.money.clean + LEDGER.G.money.dirty);
await C(() => { LEDGER.game.fightx.spar(); });
await t.h.sleep(1600); await t.h.key('KeyE'); await pick(2); await pick(2); await pick(2); await t.h.sleep(1600); await t.h.key('KeyE'); await t.h.sleep(800); await clear();
const sp2 = await C((b) => ({ spars: LEDGER.game.fightx.x().spars, same: LEDGER.G.money.clean + LEDGER.G.money.dirty === b, box: LEDGER.read().boxOpen }), bal0);
t.ok(sp2.spars.length === 1 && sp2.spars[0].stakes === 0 && !sp2.spars[0].dies && sp2.same, 'sparring: gloves on, nobody hurt, no money moves', sp2);

// play time is booked by activity (7.5)
const bd = await C(() => LEDGER.game.life.budget());
t.ok(bd.share && typeof bd.share.foot === 'number', 'play time is booked by activity against the hour budget', bd);
const bal = await C(() => LEDGER.game.econ.balances());
t.ok(bal.holds, 'after all of it, every pound still traces through a flow (ER-MONEY-01)', bal);
await t.done();
