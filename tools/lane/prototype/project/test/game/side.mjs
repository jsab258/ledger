// MEN AT HIS SIDE, in a fight, played (part 1.7.4, A16). Ron is told "with me" by key. Tom fronts up one of two
// lads by key, and it comes to blows. Ron takes the second man: that lad fights Ron and never swings at Tom while
// Ron stands. The same fight without Ron: both lads come at Tom. Set by hand: who stands where, and the hour.
import { start } from './lib.mjs';
const C = (t, fn, ...a) => t.ev(fn, ...a);
async function fight(t, withRon) {
  const subsSeen = [];
  const subs = async () => { for (const l of await t.h.page.evaluate(() => [...document.querySelectorAll('#subs .s')].map((e) => e.textContent))) if (!subsSeen.includes(l)) subsSeen.push(l); };
  await C(t, (withRon) => {
    const G = LEDGER.G;
    G.t = Math.floor(G.t / 1440) * 1440 + 19 * 60; // seven in the evening: the lads are out by the video shop
    G.tom.carry = null;
    for (const Q of G.named) if (Q.id !== 'ron') { Q.override = { where: 'off', act: 'idle' }; Q.gone = true; Q.space = 'off'; Q.route = null; }
    LEDGER.game.test.pass(2, false);
    const lads = G.crowd.filter((p) => p.lad && !p.gone).slice(0, 2);
    LEDGER.goTo({ xMetres: lads[0].x - 1.6, zMetres: lads[0].z });
    LEDGER.cam.yaw = Math.atan2(lads[0].x - G.tom.x, lads[0].z - G.tom.z); G.tom.ang = LEDGER.cam.yaw;
    const R = G.people.ron;
    if (withRon) Object.assign(R, { override: null, gone: false, space: 'street', awake: true, hold: false, route: null, x: G.tom.x - 1.5, z: G.tom.z + 1 });
    else Object.assign(R, { override: { where: 'off', act: 'idle' }, gone: true, space: 'off' });
    LEDGER.step(0.2);
  }, withRon);
  if (withRon) { await t.h.key('Digit1'); await t.h.step(0.5); }
  const side = await C(t, () => ({ with: LEDGER.game.crew.man('ron').with, side: LEDGER.game.crew.sideMen() }));
  // Q fronts the lad up, and again climbs the ladder until it is blows
  for (let i = 0; i < 8; i++) { await t.h.key('KeyQ'); await t.h.step(0.8); const f = await C(t, () => LEDGER.game.crew.fight()); if (f.on && f.foes.length >= 2 && f.foes.some((q) => q.st !== 'idle')) break; }
  const f0 = await C(t, () => LEDGER.game.crew.fight());
  // blows: J at the nearest man, in steps, for up to forty seconds; what each lad does is recorded
  let heldSeen = null, heldSwung = 0, tomHurt0 = await C(t, () => LEDGER.G.tom.hurt), swingsAtTom = {};
  for (let s = 0; s < 40; s += 0.25) {
    await t.h.key('KeyJ'); await t.h.step(0.25); await subs();
    const f = await C(t, () => LEDGER.game.crew.fight());
    for (const q of f.foes) { if (q.heldBy) { heldSeen = q.id; if (q.st === 'windup' || q.st === 'strike') heldSwung++; } else if (q.st === 'windup' || q.st === 'strike') swingsAtTom[q.id] = (swingsAtTom[q.id] || 0) + 1; }
    if (!f.on) break;
  }
  const end = await C(t, () => ({ f: LEDGER.game.crew.fight(), side: LEDGER.game.crew.x().sideFights, ron: { down: !!LEDGER.G.people.ron.down, knows: LEDGER.game.crew.man('ron').knows }, hurt: LEDGER.G.tom.hurt }));
  return { side, f0, heldSeen, heldSwung, swingsAtTom, end, subsSeen, tomHurt0 };
}
let t = await start({ port: 8884 });
const a = await fight(t, true);
t.ok(a.side.with && a.side.side.includes('ron'), 'digit 1 beside Ron: he is with him', a.side);
t.ok(a.f0.on && a.f0.foes.length === 2, 'Q fronts up one lad and his mate comes in: two against Tom and Ron', a.f0);
t.ok(a.heldSeen && a.subsSeen.some((l) => /Ron.* takes the second man/.test(l)), 'Ron takes the second man, and the screen says so', { held: a.heldSeen, subs: a.subsSeen.slice(-5) });
t.ok(a.heldSwung === 0 && !a.swingsAtTom[a.heldSeen], 'the man Ron has never swings at Tom while Ron stands', { heldSwung: a.heldSwung, atTom: a.swingsAtTom, held: a.heldSeen });
t.ok(a.end.side.length >= 1 || a.end.f.foes.some((q) => q.heldBy) || !a.end.f.on, 'their own fight goes on to an end: one of the two goes down, or the lads run', a.end);
t.ok(a.end.ron.knows >= 1, 'Ron was in it, and knows what it was about', a.end.ron);
const faults = await t.h.page.evaluate(() => LEDGER.game.faults.slice(0, 5));
t.ok(!faults.length, 'no fault inside any system (first fight)', faults);
await t.h.close();
// the same evening without Ron: both lads come at Tom
const t2 = await start({ port: 8885 });
const b = await fight(t2, false);
t2.ok(b.f0.on && b.f0.foes.length === 2 && !b.heldSeen && Object.keys(b.swingsAtTom).length === 2, 'alone, both lads swing at Tom: two against one', { atTom: b.swingsAtTom, f0: b.f0 });
t2.ok(Object.keys(a.swingsAtTom).length <= 1, 'with Ron there, only one man ever swung at Tom', a.swingsAtTom);
await t2.done();
