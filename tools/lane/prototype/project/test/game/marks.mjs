// MARKS THAT LAST, in play (part 1.3.11, A21, ER-MARK-01). After a beating his face shows it for three game days:
// the same watcher at the same distance places him more surely; a man who knows him remarks on the face (never
// on a coat he is not wearing); he cannot run as he did for a day. Then it fades.
// Set by hand: who stands where, and that the fight was lost (the fight system's own event). The deeds watched
// are test acts; what is measured is what the watcher catches, the words on screen, and his speed by the keys.
import { start } from './lib.mjs';
const t = await start({ port: 8883 });
const C = (fn, ...a) => t.ev(fn, ...a);
const subs = () => t.h.page.evaluate(() => [...document.querySelectorAll('#subs .s')].map((e) => e.textContent));
const runFor = (secs) => C((secs) => { const T = LEDGER.G.tom; LEDGER.cam.yaw = 0; const z0 = T.z, x0 = T.x; dispatchEvent(new KeyboardEvent('keydown', { code: 'ShiftLeft', key: 'Shift' })); dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyW', key: 'w' })); LEDGER.step(secs); dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyW', key: 'w' })); dispatchEvent(new KeyboardEvent('keyup', { code: 'ShiftLeft', key: 'Shift' })); LEDGER.step(0.3); return Math.hypot(T.x - x0, T.z - z0); }, secs);
const place = () => C(() => {
  const G = LEDGER.G;
  G.t = Math.floor(G.t / 1440) * 1440 + 13 * 60; // one in the afternoon
  G.tom.carry = null;
  LEDGER.goTo({ xMetres: 3.0, zMetres: -40 });
  for (const Q of G.named) if (!['lily', 'peter'].includes(Q.id)) { Q.override = { where: 'off', act: 'idle' }; Q.gone = true; Q.space = 'off'; Q.route = null; }
  const P = G.people.lily;
  Object.assign(P, { override: { where: 'pave', act: 'idle' }, gone: false, space: 'street', awake: true, x: 3.0, z: -49, route: null, hold: true, moving: false, ang: 0 });
  P.mind.fam = 0.45; P.mind.regard = 0; P.mind.fear = 0;
  LEDGER.step(0.2);
});
const seenDoing = () => C(() => { const G = LEDGER.G, E = LEDGER.game.test.act('shove', { name: 'a man' }), m = G.people.lily.mind.by[E.id]; return m ? { face: m.face, sure: m.sure, who: m.who } : null; });

await place();
const before = await seenDoing();
const d0 = await runFor(3);
await place();
// the fight is lost
await C(() => LEDGER.game.emit('fight.beaten', {}));
await t.h.step(0.5);
const said = await subs();
const m1 = await C(() => ({ m: LEDGER.game.foot.marked(), notes: LEDGER.G.ledger.notes.filter((n) => /The face will show it/.test(n.text)).length }));
t.ok(m1.m.bruised && m1.m.limp && m1.notes === 1 && said.some((l) => /split lip/.test(l)), 'he is told what the beating left, on screen and in the Ledger', { m1, said });
const after = await seenDoing();
t.ok(before && after && after.face > before.face * 1.3 && after.sure >= before.sure, 'the same watcher at the same nine metres places a marked face more surely (ER-MARK-01)', { before, after });
const d1 = await runFor(3);
t.ok(d1 < d0 * 0.85 && d1 > d0 * 0.5, 'with the limp he runs slower by the keys', { d0, d1 });
// a man who knows him and has nothing against him remarks on the face as he passes, never on a coat he does not wear
await C(() => { const G = LEDGER.G; G.people.lily.gone = true; G.people.lily.space = 'off'; G.people.lily.override = { where: 'off', act: 'idle' }; LEDGER.goTo({ xMetres: 3.0, zMetres: -40 }); const P = G.people.peter; Object.assign(P, { override: { where: 'pave', act: 'idle' }, gone: false, space: 'street', awake: true, x: 4.5, z: -41, route: null, hold: true, moving: false }); P.mind.fam = 0.9; P.mind.regard = 0; P.mind.fear = 0; G.tom.coat = false; });
let greet = [];
for (let i = 0; i < 60 && !greet.some((l) => /at your face|coat again/.test(l)); i++) { await C(() => LEDGER.game.test.pass(1, false)); await t.h.step(1.5); greet = greet.concat(await subs()); }
t.ok(greet.some((l) => /Somebody has been at your face/.test(l)) && !greet.some((l) => /That coat again/.test(l)), 'the remark is on his face, since that is what is there to remark on', greet.slice(-4));
// the limp goes in a day, the bruises in three
const fade = await C(() => { const f = LEDGER.game.foot; LEDGER.game.test.pass(1440); const a = f.marked(); LEDGER.game.test.pass(2 * 1440); return { day1: a, day3: f.marked() }; });
t.ok(fade.day1.bruised && !fade.day1.limp && !fade.day3.bruised, 'the limp lasts a day and the bruises three', fade);
await place();
const d2 = await runFor(3);
const healed = await seenDoing();
t.ok(d2 > d0 * 0.9 && healed.face < after.face * 0.8, 'healed, he runs as before and is placed no more easily than any man', { d0, d2, healed });
await t.done();
