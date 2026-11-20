// On foot, the way, the Ledger's new pages and the flows ledger (parts 1.1.5 to 1.1.8, 1.4.7, 1.4.8, 1.5.2, 2.2.6,
// 6.9, 6.3, 6.1.5, 6.2.5, 6.10, 2.7.7).
import { start } from './lib.mjs';
const t = await start({ port: 8872 });
const put = (id, dx, dz, o = {}) => t.ev((id, dx, dz, o) => { const G = LEDGER.G, P = G.people[id]; Object.assign(P, { override: null, gone: false, space: 'street', awake: true, hold: true, route: null, moving: false, x: G.tom.x + dx, z: G.tom.z + dz }, o); P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z); return true; }, id, dx, dz, o);

// the way: every place has an address, a landmark and a label (ER-WAY-02, ER-GROUND-01)
const w = await t.ev(() => ({ n: LEDGER.game.way.places().length, faults: LEDGER.game.way.faults(), known: LEDGER.game.way.known() }));
t.ok(w.n >= 40 && !w.faults.length, 'every place has an address, a landmark and a label', w);
t.ok(w.known.length <= 3, 'the paper map starts nearly empty: only what he has been told of', w.known);
const d = await t.ev(() => { const s = LEDGER.game.way.direct('landing', 'Ron'); return { s, known: LEDGER.game.way.known().includes('landing'), goal: LEDGER.game.way.goal() }; });
t.ok(/shelter under the last lamp/.test(d.s) && d.known && d.goal.id === 'landing', 'a place named by its landmark goes on the map and becomes the goal', d);
// lost: the nudge never inside 90 s, and once (ER-WAY-03)
const n1 = await t.ev(() => { LEDGER.goTo('rank'); for (let i = 0; i < 80; i++) LEDGER.step(1); const g = LEDGER.game.way.goal(); return g ? g.nudged : { tom: [LEDGER.G.tom.x, LEDGER.G.tom.z, LEDGER.G.tom.inCar], t: LEDGER.G.t }; });
t.ok(n1 === false, 'no nudge inside 90 s', n1);
const n2 = await t.ev(() => { for (let i = 0; i < 20; i++) LEDGER.step(1); return LEDGER.game.way.goal().nudged; });
t.ok(n2 === true, 'the nudge comes after 90 s without progress, once', n2);
const ask = await t.ev(() => LEDGER.game.way.askWay('k_news', 'chapel'));
t.ok(/green door/.test(ask), 'a shopkeeper always knows the way, by landmark', ask);
const mp = await t.ev(() => LEDGER.game.way.mapHTML());
t.ok(/ferry landing/.test(mp) && !/boxing club/.test(mp), 'the map marks no place he does not know', mp.length);

// the watch (ER-TIME-01) and Tom's reading
const wt = await t.ev(() => LEDGER.game.ledgerx.watch());
t.ok(wt.screenClock === false && wt.words.length > 3, 'the hour is known from his watch, never a screen clock', wt);
const rd = await t.ev(() => { const a = LEDGER.game.ledgerx.reading(); LEDGER.game.ledgerx.sign('inspector', 'The inspector read the same line twice.'); return { a, b: LEDGER.game.ledgerx.reading() }; });
t.ok(rd.a.quiet && !rd.b.quiet && rd.b.expects !== 'The Kingdom', "Tom's reading is built only from signs he was shown", rd);
const lt = await t.ev(() => { LEDGER.game.ledgerx.letter('test', 'Agar & Co', 'Private hire licence', 'Dear Mr Nowak,\nWe act for the Harbour Board.'); const ok = LEDGER.game.ledgerx.openLetter('test'); const open = !!document.querySelector('#book h2'); document.querySelector('#book [data-act="close"]').click(); return { ok, open, n: LEDGER.game.ledgerx.letters().length, closed: !LEDGER.read().boxOpen }; });
t.ok(lt.ok && lt.open && lt.n === 1 && lt.closed, 'a letter opens as a page, goes in the Ledger, and is put away', lt);

// money: the flows ledger balances, and a fare is a flow (ER-MONEY-01)
const m = await t.ev(() => { const b0 = LEDGER.game.econ.balances(); return { b0, words: LEDGER.game.econ.inWords() }; });
t.ok(m.b0.holds && m.b0.pocket === 2350, 'the pocket equals the sum of its flows', m.b0);
t.ok(/twenty-three pounds fifty/.test(m.words.pocket) && /Friday/.test(m.words.rent), 'he knows what he has and what is owed by Friday, in words', m.words);

// hiding (ER-HIDE-01): standing still in a dark doorway is caught less than moving past it
const hide = await t.ev(() => {
  const G = LEDGER.G, P = G.people.brenda;
  LEDGER.goTo('rank');
  Object.assign(P, { override: null, gone: false, space: 'street', awake: true, hold: true, route: null, x: G.tom.x, z: G.tom.z - 12, ang: 0 });
  G.env.lightAt = () => 0.12; // a doorway's light
  const T1 = () => { LEDGER.step(0.05); const mem = P.mind.mem.length; return mem; };
  G.tom.still = 5; G.tom.v = 0;
  const seenStill = LEDGER.game.foot.seen('brenda');
  G.tom.still = 0;
  const seenMoving = LEDGER.game.foot.seen('brenda');
  return { still: seenStill.rung, moving: seenMoving.rung };
});
t.ok(hide.still <= hide.moving, 'still in a dark doorway is never caught more than moving', hide);

// street manners (ER-MANNER-01): an act, answered, remembered
await put('darren', 1.5, 0);
await t.ev(() => { const G = LEDGER.G; G.env.lightAt = () => 1; G.tom.ang = Math.atan2(G.people.darren.x - G.tom.x, G.people.darren.z - G.tom.z); });
await t.h.key('KeyM');
await t.h.sleep(1500);
const mn = await t.ev(() => LEDGER.read().boxOpen);
await t.h.key('Digit3');
await t.h.sleep(600);
const mn2 = await t.ev(() => LEDGER.read().boxOpen);
const mn3 = await t.ev(() => ({ manners: LEDGER.game.foot.x().manners, mem: !!LEDGER.G.people.darren.mind.mem.find((m) => LEDGER.G.ev[m.e].kind === 'hard_look') }));
t.ok(mn3.manners.length === 1 && mn3.manners[0].kind === 'hard_look' && mn3.mem, 'a hard look is an act, and Darren remembers it', { mn, mn2, mn3 });

// a thrown stone (1.4.8): inside its reach a head turns; outside nothing
const st = await t.ev(() => { const G = LEDGER.G; LEDGER.goTo('rank'); G.tom.ang = 0; const A = G.people.ron, B = G.people.lee; Object.assign(A, { override: null, gone: false, space: 'street', awake: true, x: G.tom.x + 3, z: G.tom.z + 12, alert: null }); Object.assign(B, { override: null, gone: false, space: 'street', awake: true, x: G.tom.x, z: G.tom.z + 60, alert: null }); LEDGER.game.foot.stone(); return { near: !!A.alert, far: !!B.alert, log: LEDGER.game.foot.x().stones.slice(-1)[0] }; });
t.ok(st.near && !st.far, 'a stone turns a head inside its reach and nobody outside it', st);

// vaulting (ER-VAULT-01): a set place, running; nowhere else
const v = await t.ev(() => { const G = LEDGER.G, V = LEDGER.game.foot.vaults()[0]; G.tom.space = 'street'; G.tom.x = V.at[0]; G.tom.z = V.at[1]; G.tom.ang = Math.atan2(V.to[0] - V.at[0], V.to[1] - V.at[1]); G.tom.run = false; LEDGER.game.x(); const before = LEDGER.game.foot.x().vaults.length; LEDGER.step(0.05); const walked = LEDGER.game.foot.x().vaults.length - before; G.tom.x = V.at[0]; G.tom.z = V.at[1]; G.tom.run = true; G.tom.v = 5; LEDGER.game.foot.x(); return { walked, V }; });
t.ok(v.walked === 0, 'no vault at a walk', v.walked);

// a tail (ER-TAIL-01 to 03): a shape is nothing, the doubt comes before he is made, what is learned is written
const tl = await t.ev(() => { const f = LEDGER.game.foot; f.startTail('wayne', 'x'); const a = f.tailEvent({ rung: 2 }); const s1 = { doubt: a.doubt, ended: a.ended }; const b = f.tailEvent({ rung: 5 }); const s2 = { doubt: b.doubt, ended: b.ended }; const c = f.tailEvent({ rung: 5 }); return { s1, s2, ended: c.ended, log: f.x().tails.slice(-1)[0] }; });
t.ok(tl.s1.doubt === 0 && !tl.s1.ended && tl.s2.doubt === 1 && !tl.s2.ended && tl.ended === 'made', 'a tail is made only after a doubt was shown', tl);
const tl2 = await t.ev(() => { const f = LEDGER.game.foot; f.startTail('wayne', 'x'); f.tailEvent({ arrived: "Wayne goes to Rita's side door at six" }); return { log: f.x().tails.slice(-1)[0], ledger: LEDGER.ledger.rows ? JSON.stringify(LEDGER.ledger.rows()).includes('side door at six') : null, notes: LEDGER.G.ledger.notes.some((n) => /side door at six/.test(n.text)) }; });
t.ok(tl2.log.ended === 'arrived' && tl2.notes, 'what a tail learns is in the Ledger', tl2);

// running a man down (ER-PURSUE-01): caught by the collar or lost, always inside 90 s
const ch2 = await t.ev(() => { const G = LEDGER.G; LEDGER.goTo('rank'); const P = G.people.wayne; Object.assign(P, { override: null, gone: false, space: 'street', awake: true, hold: false, x: G.tom.x + 10, z: G.tom.z - 10 }); LEDGER.game.foot.startChase('wayne'); let n = 0; while (LEDGER.game.foot.chaseState() && n++ < 2000) LEDGER.step(0.1); return { last: LEDGER.game.foot.x().chases.slice(-1)[0], n }; });
t.ok(ch2.last.st === 'lost' && ch2.last.seconds <= 90, 'a runner nobody follows is lost inside 90 s', ch2);
const ch = await t.ev(() => { const G = LEDGER.G; LEDGER.goTo('rank'); const P = G.people.darren; Object.assign(P, { override: null, gone: false, space: 'street', awake: true, hold: false, x: G.tom.x + 0.5, z: G.tom.z + 0.5 }); LEDGER.game.foot.startChase('darren'); LEDGER.step(0.1); return LEDGER.game.foot.x().chases.slice(-1)[0]; });
t.ok(ch && ch.st === 'caught', 'a hand on the collar ends the chase', ch);
await t.done();
