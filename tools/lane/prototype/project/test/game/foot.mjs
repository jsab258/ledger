// The whole game, system "foot": hiding, manners, stopping, ground rules, the watch, noises, the torch, vaulting,
// the water's edge, chasing a runner, marks. Each check names its experience rule.
import { launch } from '../harness.mjs';
let bad = 0;
const ok = (c, what) => {
  console.log((c ? 'ok   ' : 'FAIL ') + what);
  if (!c) bad++;
};
const h = await launch({ port: 8840, quality: 'low' });
try {
  await h.newWeek();
  const L = (fn, ...a) => h.ev(fn, ...a);
  // a clear stretch of Quay Street, by day, nobody's scene in the way
  await L(() => {
    const G = LEDGER.G;
    window.__run = (s) => { for (let i = 0; i < s * 60; i++) LEDGER.tick(1 / 60); };
    window.__put = (x, z, a = 0) => { const t = G.tom; t.inCar = false; t.space = 'street'; t.x = x; t.z = z; t.ang = a; t.v = 0; t.carry = null; };
    window.__man = (id, x, z, ang) => { const P = G.people[id]; P.gone = false; P.space = 'street'; P.x = x; P.z = z; P.ang = ang; P.hold = true; P.route = null; P.moving = false; P.awake = true; P.down = false; return P; };
    window.__key = (code, up) => dispatchEvent(new KeyboardEvent(up ? 'keyup' : 'keydown', { code }));
    G.story.flags.tour = 1; G.story.flags.metRon = 1; G.story.flags.metDarren = 1; G.story.flags.metJune = 1;
  });

  // ---- manners (ER-MANNER-01): each answered within 1 s and remembered like any act
  const man = await L(() => {
    const G = LEDGER.G, out = [];
    G.t = 1 * 1440 + 11 * 60;
    __put(0, -40, 0);
    const P = __man('albert', 0, -37.5, Math.PI);
    for (const k of LEDGER.game.foot.manners()) {
      if (k === 'street_shove') { P.x = 0; P.z = -38.8; }
      const n0 = G.events.length, r = LEDGER.game.foot.manner(k, 'albert');
      const bub = LEDGER.ui.bubs.find((b) => b.P === P);
      const E = G.events[G.events.length - 1];
      out.push({ k, made: G.events.length === n0 + 1 && E.kind === k, answered: !!bub && !!r, remembered: !!P.mind.by[E.id], faces: Math.abs(Math.atan2(G.tom.x - P.x, G.tom.z - P.z) - P.ang) < 0.01 });
    }
    return out;
  });
  for (const m of man) ok(m.made && m.answered && m.remembered && m.faces, `ER-MANNER-01 ${m.k}: an act, answered in voice and body at once, and kept in the other's memory`);
  const oi = await L(() => {
    const G = LEDGER.G, P = G.people.albert;
    P.hold = false; P.moving = true;
    LEDGER.game.foot.manner('called_out', 'albert');
    const held0 = P.hold;
    __run(1.5); const mid = P.hold;
    __run(1.0); return { held0, mid, after: P.hold };
  });
  ok(oi.held0 && oi.mid && !oi.after, 'A10 the call "Oi!" stops a walker for about 2 s, then lets him go (held at once, held at 1.5 s, free by 2.5 s)');
  const menu = await L(() => {
    __put(0, -40, 0); __man('albert', 0, -37.5, Math.PI); LEDGER.cam.yaw = 0;
    __key('KeyM'); __run(0.3);
    const p = LEDGER.prompts().map((x) => x.key + ' ' + x.text);
    const n0 = LEDGER.G.events.length; __key('Digit1'); __run(0.2);
    return { p, made: LEDGER.G.events.length - n0, kind: LEDGER.G.events[LEDGER.G.events.length - 1].kind };
  });
  ok(menu.p.filter((x) => /^[1-5] /.test(x)).length === 5 && menu.made === 1 && menu.kind === 'nod', 'A10 one key [M] brings the five manners as prompts, and a digit picks one (' + menu.p.filter((x) => /^[1-5] /.test(x)).join(', ') + ')');

  // ---- stopping (ER-STOP-01) and the second look
  const stop = await L(() => {
    const G = LEDGER.G, f = LEDGER.game.foot;
    __put(-6.3, -62, 1.57);
    const prompt = LEDGER.prompts().map((x) => x.text);
    __key('KeyB'); __run(0.2); const a = f.state().stop, sit = !!G.tom.sit, belongs = !!G.tom.belongs;
    __key('KeyW'); __run(0.4); __key('KeyW', true); const b = f.state().stop;
    __put(0, -40, 0); __key('KeyB'); __run(0.2); const c = f.state().stop; f.stop(null);
    return { prompt, a, sit, belongs, b, c };
  });
  ok(stop.prompt.includes('Sit down') && stop.a === 'sit' && stop.sit && stop.belongs && stop.b === null && stop.c === 'smoke', `ER-STOP-01 [B] by the bench sits him (${stop.a}), a step gets him up, and on open ground he lights a cigarette (${stop.c}); a stopped man is marked as belonging`);
  const look = await L(() => {
    const G = LEDGER.G, f = LEDGER.game.foot;
    G.t = 1 * 1440 + 23.5 * 60; __put(0, -40, 0);
    const P = __man('albert', 0, -34, Math.PI); P.mind.look = 0;
    __run(22); const stoodLook = f.log().some((l) => l.what === 'second look');
    __put(0.5, -40, 0); __run(0.2); f.stop('smoke'); const n = f.log().filter((l) => l.what === 'second look').length;
    __run(24); const smokeLook = f.log().filter((l) => l.what === 'second look').length > n; f.stop(null);
    return { stoodLook, smokeLook };
  });
  ok(look.stoodLook && !look.smokeLook, 'A10 standing about at night for 20 s draws a second look; smoking there draws none');

  // ---- the watch and the clocks (ER-TIME-01)
  const time = await L(() => {
    const G = LEDGER.G, f = LEDGER.game.foot;
    G.t = 1 * 1440 + 11 * 60; __put(0, -40, 0); LEDGER.ui.hudT = 0;
    __run(2.6); const before = { known: f.timeKnown(), hud: document.getElementById('dtime').textContent };
    __key('KeyN'); __run(0.3);
    const during = { known: f.timeKnown(), hud: document.getElementById('dtime').textContent, sub: LEDGER.ui.subs.map((s) => s.el.textContent).join('|') };
    __put(-14, -170, 0); __run(0.3); const byClock = f.timeKnown();
    return { before, during, byClock };
  });
  ok(!time.before.known && time.before.hud === '' && time.during.known && /^\d\d:\d\d$/.test(time.during.hud) && /His watch/.test(time.during.sub) && time.byClock, `ER-TIME-01 no screen clock ("${time.before.hud}"); [N] raises the watch and the hour shows at once ("${time.during.hud}"); a street clock in sight tells it too`);
  await h.sleep(2300);
  ok(await L(() => { __put(0, -40, 0); return !LEDGER.game.foot.timeKnown(); }), 'ER-TIME-01 the watch goes down again after 2 s');

  // ---- drawing a watcher away (A23): inside its reach a head turns, outside nothing
  const noise = await L(() => {
    const G = LEDGER.G, f = LEDGER.game.foot;
    G.t = 1 * 1440 + 23 * 60; G.weather.rain = 0;
    __put(0, -40, 0); LEDGER.cam.yaw = 0;
    const near = __man('albert', 2, -26, 0), far = __man('lily', 2, 40, 0);
    near.alert = far.alert = null;
    const r = f.makeNoise();
    return { r, near: !!near.alert, far: !!far.alert, nearRemembers: near.mind.mem.some((m) => G.ev[m.e].kind === 'noise_made'), farRemembers: far.mind.mem.some((m) => G.ev[m.e].kind === 'noise_made'), dNear: Math.hypot(2 - r.x, -26 - r.z), dFar: Math.hypot(2 - r.x, 40 - r.z) };
  });
  ok(noise.r.what === 'stone' && noise.near && !noise.far && noise.nearRemembers && !noise.farRemembers && noise.dNear < noise.r.reach && noise.dFar > noise.r.reach, `A23 a thrown stone (reach ${noise.r.reach.toFixed(1)} m at night): a man ${noise.dNear.toFixed(1)} m from where it lands turns his head and remembers a noise; one at ${noise.dFar.toFixed(0)} m does nothing`);

  // ---- hiding (ER-HIDE-01, 02) and the torch (A33)
  const hide = await L(() => {
    const G = LEDGER.G, f = LEDGER.game.foot;
    G.t = 1 * 1440 + 23.5 * 60;
    __put(7.7, 1.5, 0); const sh = f.inShade(7.7, 1.5);
    G.tom.still = 0; const moving = f.lightForTomNow();
    G.tom.still = 2; const still = f.lightForTomNow();
    G.tom.items.torch = 1; f.torch(true); const lit = f.lightForTomNow(); f.torch(false); const off = f.lightForTomNow();
    return { sh, moving, still, lit, off };
  });
  ok(hide.sh && hide.still <= 0.12 + 1e-9 && hide.moving > hide.still && hide.off === hide.still, `ER-HIDE-01, 02 in the doorway by the ladder at night: standing still he counts at ${hide.still.toFixed(2)} (the doorway's light), moving through at ${hide.moving.toFixed(2)} (the street's); only the move keys are used`);
  ok(Math.abs(hide.lit - 0.7) < 1e-9, 'A33 a lit torch makes him count as lit at lamp value 0.7, and off again when it is switched off');

  // ---- walking slowly (A1)
  const slow = await L(() => {
    const G = LEDGER.G;
    G.t = 1 * 1440 + 11 * 60; __put(0, -60, 0); LEDGER.cam.yaw = 0;
    __key('KeyW'); __run(1.5); const z0 = G.tom.z; __run(1); const walk = G.tom.z - z0;
    __key('KeyZ'); __run(0.5); const z1 = G.tom.z; __run(1); const slowly = G.tom.z - z1, flag = LEDGER.game.foot.state().slow, fast = G.fast;
    __key('KeyZ', true); __key('KeyW', true); __run(0.3);
    return { walk, slowly, flag, fast };
  });
  ok(slow.flag && slow.fast === 1 && Math.abs(slow.slowly / slow.walk - 0.5) < 0.08, `A1 [Z] held while walking halves his pace (${slow.walk.toFixed(2)} m/s to ${slow.slowly.toFixed(2)} m/s) and does not pass the time`);

  // ---- vaulting (ER-VAULT-01): every set place, and nothing else
  const vault = await L(() => {
    const G = LEDGER.G, out = { places: 0, over: 0, fails: [] };
    G.t = 1 * 1440 + 11 * 60;
    const places = LEDGER.game.feel.vaultPlaces();
    for (const p of places) {
      // run at it from each of four sides; one clear run-up that carries him over is enough
      let done = false, tried = 0;
      for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const sx = p.x - dx * 2.2, sz = p.z - dz * 2.2;
        if (LEDGER.isBlocked(sx, sz) || LEDGER.isBlocked(p.x + dx * 1.6, p.z + dz * 1.6)) continue;
        tried++;
        __put(sx, sz, Math.atan2(dx, dz)); LEDGER.cam.yaw = Math.atan2(dx, dz); G.tom.hurt = 0;
        __key('ShiftLeft'); __key('KeyW'); __run(2.2); __key('KeyW', true); __key('ShiftLeft', true); __run(0.2);
        const far = (G.tom.x - p.x) * dx + (G.tom.z - p.z) * dz;
        if (far > 0.3 && !LEDGER.isBlocked(G.tom.x, G.tom.z)) { done = true; break; }
      }
      if (tried) { out.places++; if (done) out.over++; else out.fails.push(p.kind + ' ' + p.x.toFixed(0) + ',' + p.z.toFixed(0)); }
    }
    // not anywhere else: the school wall and a lamp post stop him
    __put(-95, -1.5, Math.PI); LEDGER.cam.yaw = Math.PI; __key('ShiftLeft'); __key('KeyW'); __run(2); __key('KeyW', true); __key('ShiftLeft', true); __run(0.2);
    out.school = G.tom.z > -3.6;
    // walking (not running) at a set place does not vault
    const w = places.find((p) => p.kind === 'dustbin');
    __put(w.x, w.z + 2, Math.PI); LEDGER.cam.yaw = Math.PI; __key('KeyW'); __run(2); __key('KeyW', true); __run(0.2);
    out.walkStops = G.tom.z > w.z;
    out.all = places.length;
    return out;
  });
  ok(vault.places >= 6 && vault.over === vault.places, `ER-VAULT-01 every set place with a clear run-up is vaulted at a run (${vault.over} of ${vault.places}; ${vault.all} set places${vault.fails.length ? '; not over: ' + vault.fails.join(' | ') : ''})`);
  ok(vault.school && vault.walkStops, 'ER-VAULT-01 nothing else can be vaulted (the school wall stops a running man) and walking at a set place does not vault');

  // ---- the water's edge (ER-WATER-01 on foot; A11 things thrown in are gone)
  const water = await L(() => {
    const G = LEDGER.G, f = LEDGER.game.foot;
    let wet = 0;
    for (const x of [-100, -40, 10, 60, 120]) {
      __put(x, 58, 0); LEDGER.cam.yaw = 0; __key('ShiftLeft'); __key('KeyW'); __run(3); __key('KeyW', true); __key('ShiftLeft', true); __run(0.1);
      if (LEDGER.game.feel.inWater(G.tom.x, G.tom.z)) wet++;
    }
    G.tom.weapon = 'flick knife';
    const prompt = LEDGER.prompts().map((x) => x.text).find((x) => /water/.test(x)), n0 = G.events.length;
    const thing = f.throwIn();
    return { wet, prompt, thing, weapon: G.tom.weapon, made: G.events.length - n0, kind: G.events[G.events.length - 1].kind, z: G.tom.z };
  });
  ok(water.wet === 0, 'ER-WATER-01 running at the quay edge at five places: he never goes in');
  ok(/Throw the flick knife/.test(water.prompt || '') && water.thing === 'flick knife' && water.weapon === null && water.kind === 'threw_in', 'A11 at the edge a carried weapon can be thrown in; it is gone, and the throw is an act the town can see');

  // ---- ground rules (ER-GROUND-01): the warnings come in order
  const ground = await L(() => {
    const G = LEDGER.G, f = LEDGER.game.foot, out = {};
    G.t = 1 * 1440 + 23 * 60;
    out.dayLabel = f.groundAt(-100, 28).label; out.night = f.groundAt(-100, 28).standing; out.street = f.groundAt(0, -40).standing;
    G.t = 1 * 1440 + 11 * 60; out.day = f.groundAt(-100, 28).standing; G.t = 1 * 1440 + 23 * 60;
    __put(-98, 22, 0); __man('dennis', -98, 27, Math.PI);
    const n0 = f.log().length; __run(0.6);
    const says = () => f.log().slice(n0).filter((l) => l.what === 'ground').map((l) => l.say);
    out.first = says().join(','); __run(8.5); out.second = says().join(','); const e0 = G.events.length; __run(12.5); out.third = says().join(',');
    out.act = G.events.slice(e0).some((E) => E.kind === 'trespass');
    __put(0, -40, 0); __run(0.6); out.reset = f.trespass();
    __put(-98, 22, 0); G.people.dennis.gone = true; G.people.dennis.space = 'away'; for (const id in G.people) if (id !== 'dennis' && Math.hypot(G.people[id].x + 98, G.people[id].z - 22) < 40) G.people[id].gone = true;
    const n1 = f.log().length; __run(3); out.unwatched = f.log().slice(n1).filter((l) => l.what === 'ground').length;
    return out;
  });
  ok(ground.dayLabel === 'hours' && ground.day === 'free' && ground.night === 'private' && ground.street === 'free', "ER-GROUND-01 the ground carries a label: Iveson's yard is open by hours (free by day, private at night), the street is public");
  ok(ground.first === 'warn' && ground.second === 'warn,warnAgain' && ground.third === 'warn,warnAgain,act' && ground.act && ground.reset === null, `ER-GROUND-01 in the yard at night in the owner's sight: warned, warned again, then he acts within half a minute (${ground.third}); leaving resets the warnings, the sighting is kept`);
  ok(ground.unwatched === 0, 'ER-GROUND-01 with nobody to see or hear him, nobody warns');

  // ---- chasing a runner (ER-PURSUE-01, 02)
  const chase = await L(() => {
    const G = LEDGER.G, f = LEDGER.game.foot, out = {};
    G.t = 1 * 1440 + 11 * 60;
    for (const id in G.people) { G.people[id].gone = false; }
    // a lagging pursuer: Tom stands still, the runner goes
    __put(0, -40, 0); const P = __man('wayne', 0, -36, 0);
    out.started = f.runner('wayne', 'test');
    let secs = 0; while (f.chase() && secs < 95) { __run(1); secs++; }
    out.lostIn = secs; out.lost = f.log().some((l) => l.what === 'chase' && l.end === 'lost');
    // a direct pursuer: Tom runs straight after him
    __put(0, -40, 0); __man('wayne', 0, -37.5, 0); G.people.wayne.hold = false; LEDGER.cam.yaw = 0;
    f.runner('wayne', 'test'); __key('ShiftLeft'); __key('KeyW');
    secs = 0; while (f.chase() && secs < 95) { __run(0.5); secs += 0.5; }
    __key('KeyW', true); __key('ShiftLeft', true);
    out.caughtIn = secs; out.caught = f.log().some((l) => l.what === 'chase' && l.end === 'caught');
    out.choice = [...document.querySelectorAll('#dopts .opt')].map((o) => o.textContent.replace(/^\d/, ''));
    out.modal = LEDGER.ui.modal;
    return out;
  });
  ok(chase.started && chase.lost && chase.lostIn <= 90, `ER-PURSUE-01, 02 a runner nobody follows is lost within 90 s (${chase.lostIn} s: out of sight 7 s or 70 m clear)`);
  ok(chase.caught && chase.caughtIn <= 90, `ER-PURSUE-02 run down on a direct line he is caught: a hand on his collar (${chase.caughtIn} s)`);
  await h.sleep(1500);
  const choice = await L(() => ({ opts: [...document.querySelectorAll('#dopts .opt')].map((o) => o.textContent.replace(/^\d/, '')), modal: LEDGER.ui.modal }));
  ok(choice.opts.length === 3 && /Let him go/.test(choice.opts[0]), 'A3 then the choice is put: let go, a word, or front him up (' + choice.opts.join(' / ') + ')');
  await L(() => { dispatchEvent(new KeyboardEvent('keydown', { code: 'Digit1' })); __run(0.3); });

  // ---- marks that last (ER-MARK-01) and the old doctor
  const marks = await L(() => {
    const G = LEDGER.G, f = LEDGER.game.foot, out = {};
    G.t = 2 * 1440 + 10 * 60; G.money.clean = 2000;
    f.mark(1); __run(0.2);
    out.at0 = f.state(); G.tom.hurt = 0;
    __put(0, -60, 0); LEDGER.cam.yaw = 0; __key('ShiftLeft'); __key('KeyW'); __run(1.5); out.runs = G.tom.run; __key('KeyW', true); __key('ShiftLeft', true); __run(0.3);
    __put(-6.6, 24.5, -1.57); out.doorPrompt = LEDGER.prompts().map((x) => x.text).find((x) => /doctor/.test(x));
    const m0 = Object.assign({}, G.x.foot.marks), p0 = G.money.clean + G.money.dirty;
    out.treated = f.doctor(); out.paid = p0 - (G.money.clean + G.money.dirty); out.halved = (G.x.foot.marks.bruise - G.t) / (m0.bruise - G.t);
    G.t += 1 * 1440 - 100; __run(1.2); out.afterDay = f.state();
    G.t += 2 * 1440; __run(1.2); out.after3 = f.state();
    return out;
  });
  ok(marks.at0.marked && marks.at0.limp && !marks.runs, 'ER-MARK-01 a beaten Tom is marked (a give-away the town can catch) and limps: a limping man does not run');
  ok(/doctor/.test(marks.doorPrompt || '') && marks.treated && marks.paid === 600 && Math.abs(marks.halved - 0.5) < 0.01, `A21 the old doctor's door on Quay Street: stitched for six pounds, no questions, and the marks' time left is halved`);
  ok(!marks.afterDay.limp && !marks.after3.marked, 'ER-MARK-01 the marks fade on the clock (the limp first, then the bruises)');

  const faults = await L(() => LEDGER.game.faults.slice());
  ok(faults.length === 0, 'no fault inside any system' + (faults.length ? ': ' + faults[0] : ''));
  ok(h.errors.length === 0, 'no page errors' + (h.errors.length ? ': ' + h.errors[0] : ''));
} catch (e) {
  console.log('FAIL TEST FAIL ' + (e.stack || e));
  bad++;
}
await h.close();
console.log(bad ? `foot: ${bad} FAIL` : 'PASS');
process.exit(bad ? 1 : 0);
