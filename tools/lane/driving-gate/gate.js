// The clumsy-player gate. Usage: node gate.js <saved page.html> <out folder for report and pictures>
// Plays the page like a newcomer, keyboard first, then a simulated standard pad, and checks the invariants in
// README.md after each scenario. Writes report.json and a few pictures to the out folder (never to the repo).
'use strict';
const fs = require('fs');
const path = require('path');
const { open } = require('./page.js');
const { DRIVER } = require('./driver.js');
const L = require('./lib.js');

const [file, out] = process.argv.slice(2);
if (!file || !out) { console.error('usage: node gate.js <page.html> <out folder>'); process.exit(2); }
fs.mkdirSync(out, { recursive: true });

const fails = [];       // { inv, scenario, what, steps }
const notes = [];       // facts worth reporting that are not failures
const fail = (inv, scenario, what, steps) => fails.push({ inv, scenario, what, steps: steps.slice() });

async function session(pad, body) {
  const s = await open(file, { pad });
  const { page } = s;
  await page.setViewportSize({ width: 480, height: 270 });
  await page.evaluate(() => window.QR.applySetting('gfx', 0));
  await page.click('#b-drive');
  await page.evaluate(DRIVER);
  const steps = [];
  const g = {
    page, steps,
    go: (sec, tag) => page.evaluate(([a, b]) => window.__go(a, b), [sec, tag || '']),
    state: () => page.evaluate(() => window.__state()),
    place: (x, z, h) => { steps.length = 0; steps.push(`placed at ${x.toFixed(1)},${z.toFixed(1)} facing ${(h * 180 / Math.PI).toFixed(0)} deg`); return page.evaluate(([a, b, c]) => window.__place(a, b, c), [x, z, h]); },
    down: async (k) => { steps.push('hold ' + k); await page.keyboard.down(k); },
    up: async (k) => { steps.push('release ' + k); await page.keyboard.up(k); },
    tap: async (k) => { steps.push('tap ' + k); await page.keyboard.down(k); await g.go(0.05); await page.keyboard.up(k); },
    pad: async (axes, btn, label) => { steps.push('pad ' + (label || JSON.stringify({ axes, btn }))); await page.evaluate(([a, b]) => window.__setPad(a, b), [axes, btn]); },
    log: (from) => page.evaluate((t) => window.__log.filter((r) => r.t >= t), from),
    hits: (from) => page.evaluate((t) => window.__hits.filter((h) => h.t >= t), from),
    toasts: (from) => page.evaluate((t) => [...new Set(window.__toasts.filter((h) => h.t >= t - 0.01).map((h) => h.text).concat(window.__log.filter((r) => r.t >= t && r.toast).map((r) => r.toast)))], from),
    shot: async (name) => { await page.waitForTimeout(900); const p = path.join(out, name + '.png'); await page.screenshot({ path: p }); return p; },
  };
  try { await body(g); } finally {
    const all = await page.evaluate(() => window.__log);
    s.rows = all; await s.close();
  }
  return s;
}

// Drive from a standing start at the keys (or pad) until speed >= mph, then let go and roll until a hit or stop.
async function runInto(g, mph, usePad) {
  const t0 = (await g.state()).t;
  if (usePad) await g.pad(null, { 7: 1 }, 'throttle trigger full'); else await g.down('KeyW');
  for (let i = 0; i < 100; i++) { await g.go(0.1); const s = await g.state(); if (s.speed >= mph || (await g.hits(t0)).length) break; }
  if (usePad) await g.pad(null, { 7: 0 }, 'throttle trigger off'); else await g.up('KeyW');
  for (let i = 0; i < 80; i++) { await g.go(0.1); const s = await g.state(); if (Math.abs(s.speed) < 0.3 && (await g.hits(t0)).length) break; }
  await g.go(0.5);
  return { hits: await g.hits(t0), state: await g.state(), t0 };
}

// After a stop: can the player move again? Reverse, then forward, then on foot; then reset, then repair.
async function recover(g, usePad, scenario) {
  const res = {};
  const moved = async (fn) => { const a = await g.state(); await fn(); const b = await g.state(); return +Math.hypot(b.x - a.x, b.z - a.z).toFixed(2); };
  const t0 = (await g.state()).t;
  if (usePad) { await g.pad(null, { 6: 1 }, 'brake trigger (reverse)'); res.reverse = await moved(() => g.go(2.5)); await g.pad(null, { 6: 0 }, 'brake off'); }
  else { await g.down('KeyS'); res.reverse = await moved(() => g.go(2.5)); await g.up('KeyS'); }
  if (usePad) { await g.pad(null, { 7: 1 }, 'throttle'); res.forward = await moved(() => g.go(2)); await g.pad(null, { 7: 0 }, 'throttle off'); }
  else { await g.down('KeyW'); res.forward = await moved(() => g.go(2)); await g.up('KeyW'); }
  const toasts = await g.toasts(t0 - 6);
  res.toasts = [...new Set(toasts)];
  const s = await g.state();
  res.dead = s.dead; res.worst = s.worst; res.points = s.points;
  res.carMoves = res.reverse > 0.5 || res.forward > 0.5;
  if (!res.carMoves) {
    const steps = g.steps.slice();
    // what a newcomer can do without a hidden key: get out and walk
    if (usePad) { await g.pad(null, { 3: 1 }, 'Y (get out)'); await g.go(0.1); await g.pad(null, { 3: 0 }, 'Y up'); } else await g.tap('KeyF');
    await g.go(2);
    const w0 = await g.page.evaluate(() => [window.QR.walker.x, window.QR.walker.z, window.QR.walker.state]);
    if (usePad) { await g.pad([0, -1], null, 'left stick up'); await g.go(1.5); await g.pad([0, 0], null, 'stick centre'); }
    else { await g.down('KeyW'); await g.go(1.5); await g.up('KeyW'); }
    const w1 = await g.page.evaluate(() => [window.QR.walker.x, window.QR.walker.z, window.QR.walker.state]);
    res.onFoot = w0[2] === 'foot' ? +Math.hypot(w1[0] - w0[0], w1[1] - w0[1]).toFixed(2) : 0;
    // back in and try the hidden keys
    await g.place(s.x, s.z, s.heading);   // put the walker back in the seat where the car is; damage kept below
    await g.page.evaluate(([dead, pts, worst]) => { const d = window.QR.sim.player.dmg; d.dead = dead; d.points = pts; d.worst = worst; if (dead) d.power = 0; }, [s.dead, s.points, s.worst]);
    if (usePad) { await g.pad(null, { 8: 1 }, 'Back/Select (reset)'); await g.go(0.1); await g.pad(null, { 8: 0 }, 'Back up'); } else await g.tap('Backspace');
    if (usePad) { await g.pad(null, { 7: 1 }, 'throttle'); res.afterReset = await moved(() => g.go(2)); await g.pad(null, { 7: 0 }, 'throttle off'); }
    else { await g.down('KeyW'); res.afterReset = await moved(() => g.go(2)); await g.up('KeyW'); }
    await g.tap('KeyR');
    await g.down('KeyW'); res.afterRepair = await moved(() => g.go(2)); await g.up('KeyW');
    res.needs = res.afterReset > 0.5 ? 'Backspace (reset)' : res.afterRepair > 0.5 ? 'R (repair)' : 'nothing worked';
    res.toldWhat = res.toasts.some((t) => /R repairs/.test(t));
    const stepsTxt = steps.concat(['then: hold S 2.5 s, hold W 2 s']);
    fail(1, scenario, `car will not move under reverse or throttle (moved ${res.reverse} m and ${res.forward} m); recovery needs ${res.needs}${usePad ? ' (the pad has no repair button; R is on the keyboard only)' : ''}; on foot moved ${res.onFoot} m`, stepsTxt);
    if (!res.toldWhat || usePad) fail(2, scenario, `the car will not drive on; the screen ${res.toldWhat ? 'says "R repairs it" for about 3 s and then nothing' : 'says nothing'}${usePad ? ', and R is not on the pad' : ''}`, stepsTxt);
  }
  return res;
}

// Find straight lines that end in something solid, with room to reach each speed on the way.
async function findTargets(g) {
  return g.page.evaluate(() => {
    const pts = [];
    for (let z = 40; z >= -90; z -= 10) pts.push([-1.65, z]);
    for (const b of window.QR.sim.traffic.parked.slice(0, 19)) { const p = window.QR.sim.traffic.bodies[b] || b; if (p && p.x !== undefined) pts.push([p.x + Math.cos(p.yaw) * 0, p.z]); }
    const want = { 10: [10, 20], 20: [22, 40], 30: [40, 60], 40: [62, 95] }, found = {};
    for (const [x, z] of pts) {
      let room = 99; for (let a = 0; a < 360; a += 30) room = Math.min(room, window.__clear(x, z, a * Math.PI / 180, 10));
      if (room < 2.2) continue;
      for (let a = 0; a < 360; a += 2) {
        const h = a * Math.PI / 180, d = window.__clear(x, z, h, 120);
        // the run must stay clear a car's half width either side
        const sx = Math.cos(h) * 0.9, sz = -Math.sin(h) * 0.9;
        const dl = window.__clear(x + sx, z + sz, h, 120), dr = window.__clear(x - sx, z - sz, h, 120);
        if (Math.min(dl, dr) < d - 1.5) continue;
        for (const v in want) if (d >= want[v][0] && d <= want[v][1]) (found[v] = found[v] || []).push({ x, z, h, d: +d.toFixed(1) });
      }
    }
    for (const v in found) { const f = found[v]; found[v] = [f[0], f[Math.floor(f.length / 3)], f[Math.floor(2 * f.length / 3)], f[f.length - 1]].filter(Boolean); }
    return found;
  });
}

function steerCheck(all, inv, scenario, label, steps) {
  let n = all.length; for (let i = 1; i < all.length; i++) if (all[i - 1].speed - all[i].speed > 1.5) { n = i - 1; break; }
  const rows = all.slice(0, n);
  if (!rows.length || Math.abs(rows[0].speed) < 20) return { label, notReached: true };
  const sIn = L.inputSmooth(rows.map((r) => ({ t: r.t, v: r.steerIn })));
  const sCar = L.inputSmooth(rows.map((r) => ({ t: r.t, v: r.steerCar })));
  const y = L.yawSmooth(rows.map((r) => ({ t: r.t, v: r.yaw })));
  const m = { label, input: sIn, carSteer: sCar, yaw: y, seconds: +(rows[rows.length - 1].t - rows[0].t).toFixed(2), startMph: +rows[0].speed.toFixed(1) };
  if (sIn.snap || sCar.snap) fail(inv, scenario, `${label}: steering reaches 90% within ${sCar.snap ? sCar.riseFrames : sIn.riseFrames} frame(s)`, steps);
  if (y.jerk) fail(inv, scenario, `${label}: yaw rate jumps ${y.maxStep} rad/s in one frame (typical ${y.typicalStep})`, steps);
  return m;
}

(async () => {
  const report = { page: path.basename(file), when: new Date().toISOString(), keyboard: {}, pad: {} };
  const errs = [];

  // ---------------- keyboard
  const K = await session(false, async (g) => {
    const R = report.keyboard;
    // start driving from the menu with W
    await g.go(0.3); await g.down('KeyW'); await g.go(3); await g.up('KeyW');
    R.start = await g.state(); if (R.start.speed < 5) fail(1, 'start', 'W for 3 s does not get the car moving', g.steps);
    const T = await findTargets(g); R.targets = Object.fromEntries(Object.entries(T).map(([k, v]) => [k, v.length]));
    // crashes at about 10, 20, 30 and 40 mph, several targets each
    R.crashes = [];
    for (const v of [10, 20, 30, 40]) for (const tg of (T[v] || []).slice(0, 3)) {
      await g.place(tg.x, tg.z, tg.h); await g.go(0.6);
      const r = await runInto(g, v, false);
      const first = r.hits[0];
      const c = { target: v, line: tg.d, hit: first ? first.kind : 'nothing', mph: first ? first.mph : 0, stage: r.state.worst, dead: r.state.dead };
      if (first) {
        const steps = g.steps.slice();
        if (v >= 30 && !R['shot' + v]) R['shot' + v] = await g.shot('kb-crash-' + v + '-' + first.kind);
        c.recover = await recover(g, false, `crash ${v} mph into ${first.kind}`);
        if (first.st >= 1) {
          const told = c.recover.toasts.length > 0;
          if (!told) fail(2, `crash ${v} mph into ${first.kind}`, `damage stage "${['none', 'dented', 'crumpled', 'will not drive on'][first.st]}" at ${first.mph} mph closing: no words on screen; only the body shows it`, steps);
        }
      }
      R.crashes.push(c);
    }
    // a run of 20 mph hits adds up to "will not drive on"
    const t20 = (T[20] || [])[0];
    if (t20) {
      const seq = []; await g.place(t20.x, t20.z, t20.h);
      const steps0 = [];
      for (let i = 0; i < 4; i++) {
        await g.page.evaluate(([x, z, h]) => { const Q = window.QR; Q.car.reset(x, z, h); Q.sim.proxy.sync(); Q.cam.reset(Q.car); }, [t20.x, t20.z, t20.h]);
        g.steps.push('car put back at the start of the same line (damage kept)'); await g.go(0.6);
        const r = await runInto(g, 20, false); seq.push({ mph: r.hits[0] ? r.hits[0].mph : 0, st: r.hits[0] ? r.hits[0].st : 0, points: r.state.points, dead: r.state.dead });
        steps0.push(...g.steps); if (r.state.dead) break;
      }
      R.smallHits = seq; R.smallHitsRecover = await recover(g, false, 'repeated 20 mph hits');
    }
    // the owner's complaint (a): one hit on a pole. Poles are thin; aim at the narrowest target found.
    // steering on keys at 30 mph on the long road
    await g.place(-1.65, 40, Math.PI); await g.down('KeyW');
    for (let i = 0; i < 60; i++) { await g.go(0.1); if ((await g.state()).speed >= 30) break; } await g.up('KeyW');
    const ts = (await g.state()).t; const st = g.steps.slice();
    for (let i = 0; i < 3; i++) { await g.tap('KeyA'); await g.go(0.25); }
    await g.down('KeyA'); await g.go(0.5); await g.up('KeyA'); await g.go(0.5);
    await g.down('KeyD'); await g.go(0.5); await g.up('KeyD'); await g.go(0.5);
    const rows = await g.log(ts);
    R.steer = steerCheck(rows, 3, 'keyboard steering at 30 mph', 'taps and holds of A and D', g.steps);
    R.steerTrace = rows.filter((r, i) => i % 2 === 0 && r.t < ts + 2.5).map((r) => [+(r.t - ts).toFixed(3), +r.speed.toFixed(1), +r.steerIn.toFixed(3), +r.steerCar.toFixed(3), +r.yaw.toFixed(3)]);
    // get out and back in
    await g.down('Space'); await g.down('KeyS'); await g.go(3); await g.up('KeyS'); await g.up('Space');
    const t1 = (await g.state()).t;
    await g.tap('KeyF'); await g.go(2.5); const out1 = await g.state();
    await g.tap('KeyF'); await g.go(2.5); const in1 = await g.state();
    await g.down('KeyW'); await g.go(1.5); await g.up('KeyW'); const go1 = await g.state();
    R.outIn = { out: out1.walker, backIn: in1.walker, moved: +Math.hypot(go1.x - in1.x, go1.z - in1.z).toFixed(2), toasts: await g.toasts(t1) };
    if (out1.walker !== 'foot' || in1.walker !== 'drive' || R.outIn.moved < 0.5) fail(1, 'get out and back in', JSON.stringify(R.outIn), g.steps);
    // getting out while moving
    await g.down('KeyW'); await g.go(3); await g.tap('KeyF'); await g.up('KeyW'); const t2 = (await g.state()).t; await g.go(1);
    R.outWhileMoving = { walker: (await g.state()).walker, toasts: await g.toasts(t2 - 0.1) };
    // wedge: nose into the wall beside the start at full lock, then try to get away
    await g.place(-1.65, 37.7, Math.PI * 1.5 + 0.5); await g.down('KeyW'); await g.down('KeyA'); await g.go(4); await g.up('KeyA'); await g.up('KeyW');
    const wedgeShot = await g.shot('kb-wedge'); R.wedgeShot = wedgeShot;
    R.wedge = await recover(g, false, 'wedged nose-first into the wall at full lock');
    // spam: random keys for 10 s of game time
    let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    const keys = ['KeyW', 'KeyA', 'KeyS', 'KeyD', 'Space', 'KeyF', 'KeyR', 'Backspace', 'KeyC', 'Enter', 'KeyP', 'Escape', 'ArrowUp', 'ArrowLeft'];
    const ts3 = (await g.state()).t; g.steps.length = 0; g.steps.push('random keys, seed 7, 10 s');
    for (let i = 0; i < 60; i++) { const k = keys[Math.floor(rnd() * keys.length)]; await g.page.keyboard.down(k); await g.go(0.03 + rnd() * 0.2); await g.page.keyboard.up(k); }
    let s3 = await g.state(); if (s3.mode === 'menu') { await g.tap('Escape'); s3 = await g.state(); }
    if (s3.walker === 'foot') { await g.tap('KeyF'); await g.go(2.5); }
    R.spam = { modeAfter: s3.mode, walker: (await g.state()).walker };
    R.spamRecover = await recover(g, false, 'after random keys');
    R.spamDeadInput = L.longestDeadInput(await g.log(ts3));
    // pause and resume
    const a = await g.state(); await g.tap('Escape'); await g.down('KeyW'); await g.go(2); await g.up('KeyW');
    const b = await g.state(); await g.tap('Escape'); await g.down('KeyW'); await g.go(2); await g.up('KeyW'); const c = await g.state();
    R.pause = { modeWhilePaused: b.mode, movedWhilePaused: +Math.hypot(b.x - a.x, b.z - a.z).toFixed(2), modeAfter: c.mode, movedAfter: +Math.hypot(c.x - b.x, c.z - b.z).toFixed(2) };
    if (b.mode !== 'menu' || R.pause.movedWhilePaused > 0.1 || c.mode !== 'drive' || R.pause.movedAfter < 0.5) fail(6, 'pause and resume (Esc)', JSON.stringify(R.pause), g.steps);
    // pedestrian: drive at one at about 10 mph
    const ped = await g.page.evaluate(() => { const p = window.QR.sim.traffic.peds.find((q) => q.state === 'walk'); return p ? { x: p.x, z: p.z, i: window.QR.sim.traffic.peds.indexOf(p), nx: p.nx, nz: p.nz } : null; });
    if (ped) {
      await g.page.evaluate((i) => { const p = window.QR.sim.traffic.peds[i]; p.pause = 99; p.speed = 0; }, ped.i);
      g.steps.push('stopped one walker in place'); const hx = -ped.nx, hz = -ped.nz;  // come at them across the pavement line
      let best = null; for (let a2 = 0; a2 < 360; a2 += 10) { const h = a2 * Math.PI / 180, x = ped.x - Math.sin(h) * 9, z = ped.z - Math.cos(h) * 9; const cl = await g.page.evaluate(([x0, z0, hh]) => window.__clear(x0, z0, hh, 8.5), [x, z, h]); if (cl >= 8.4) { best = { x, z, h }; break; } }
      if (best) {
        await g.place(best.x, best.z, best.h); await g.go(0.5); const tp = (await g.state()).t;
        await g.down('KeyW'); for (let i = 0; i < 40; i++) { await g.go(0.1); if ((await g.state()).speed > 12) break; } await g.up('KeyW'); await g.go(2);
        const after = await g.page.evaluate((i) => { const p = window.QR.sim.traffic.peds[i]; const o = {}; for (const k in p) if (typeof p[k] !== 'object') o[k] = p[k]; return o; }, ped.i);
        R.ped = { start: ped, after: { state: after.state, x: +after.x.toFixed(2), z: +after.z.toFixed(2) }, movedBy: +Math.hypot(after.x - ped.x, after.z - ped.z).toFixed(2), hits: await g.hits(tp), toasts: await g.toasts(tp), hx, hz };
      } else R.ped = { reached: false };
    }
  });
  errs.push(...K.errors.map((e) => 'keyboard: ' + e));
  report.keyboard.camWorst = Math.max(...K.rows.map((r) => r.camIn));
  report.keyboard.camInside = K.rows.filter((r) => r.camIn > 0.5).length;
  report.keyboard.deadInput = L.longestDeadInput(K.rows);

  // ---------------- simulated pad
  const P = await session(true, async (g) => {
    const R = report.pad;
    await g.go(0.3); await g.pad(null, { 7: 1 }, 'throttle'); await g.go(3); await g.pad(null, { 7: 0 }, 'throttle off');
    R.start = await g.state(); if (R.start.speed < 5) fail(1, 'pad start', 'throttle trigger for 3 s does not get the car moving', g.steps);
    R.device = (await g.log(0)).slice(-1)[0].dev;
    const T = await findTargets(g);
    R.crashes = [];
    for (const v of [20, 40]) for (const tg of (T[v] || []).slice(0, 2)) {
      await g.place(tg.x, tg.z, tg.h); await g.go(0.6);
      const r = await runInto(g, v, true); const first = r.hits[0];
      const c = { target: v, hit: first ? first.kind : 'nothing', mph: first ? first.mph : 0, dead: r.state.dead };
      if (first) c.recover = await recover(g, true, `pad: crash ${v} mph into ${first.kind}`);
      R.crashes.push(c);
    }
    // steering at 30 mph: small and large stick, a quick thumb (5 frames) and an instant step
    R.steer = [];
    for (const [amt, ramp] of [[0.25, 0.08], [0.6, 0.08], [1, 0.08], [1, 0]]) {
      await g.place(-1.65, 40, Math.PI); await g.pad(null, { 7: 1 }, 'throttle');
      for (let i = 0; i < 60; i++) { await g.go(0.1); if ((await g.state()).speed >= 30) break; } await g.pad(null, { 7: 0.35 }, 'part throttle');
      const ts = (await g.state()).t;
      if (ramp) for (let k = 1; k <= 5; k++) { await g.pad([-amt * k / 5, 0], null, `stick ${(-amt * k / 5).toFixed(2)}`); await g.go(ramp / 5); }
      else await g.pad([-amt, 0], null, `stick ${-amt} at once`);
      await g.go(0.5); await g.pad([0, 0], null, 'stick centre'); await g.go(0.5); await g.pad(null, { 7: 0 }, 'throttle off');
      R.steer.push(steerCheck(await g.log(ts), 4, 'pad steering at 30 mph', `stick ${amt} over ${ramp * 1000} ms`, g.steps));
    }
    // pause and resume with Start (button 9)
    const a = await g.state(); await g.pad(null, { 9: 1 }, 'Start'); await g.go(0.1); await g.pad(null, { 9: 0 }, 'Start up');
    await g.pad(null, { 7: 1 }, 'throttle'); await g.go(1.5); await g.pad(null, { 7: 0 }, 'off'); const b = await g.state();
    await g.pad(null, { 9: 1 }, 'Start'); await g.go(0.1); await g.pad(null, { 9: 0 }, 'Start up');
    await g.pad(null, { 7: 1 }, 'throttle'); await g.go(1.5); await g.pad(null, { 7: 0 }, 'off'); const c = await g.state();
    R.pause = { modeWhilePaused: b.mode, movedWhilePaused: +Math.hypot(b.x - a.x, b.z - a.z).toFixed(2), modeAfter: c.mode, movedAfter: +Math.hypot(c.x - b.x, c.z - b.z).toFixed(2) };
    if (b.mode !== 'menu' || c.mode !== 'drive' || R.pause.movedAfter < 0.5) fail(6, 'pad pause and resume (Start)', JSON.stringify(R.pause), g.steps);
    // button spam
    let seed = 11; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    g.steps.length = 0; g.steps.push('random pad buttons and stick, seed 11, 10 s');
    for (let i = 0; i < 60; i++) { const bt = Math.floor(rnd() * 16); await g.pad([rnd() * 2 - 1, rnd() * 2 - 1], { [bt]: 1 }); await g.go(0.03 + rnd() * 0.2); await g.pad([0, 0], { [bt]: 0 }); }
    for (let i = 0; i < 17; i++) await g.pad(null, { [i]: 0 });
    let s3 = await g.state(); if (s3.mode === 'menu') { await g.pad(null, { 9: 1 }); await g.go(0.1); await g.pad(null, { 9: 0 }); }
    s3 = await g.state(); if (s3.walker === 'foot') { await g.pad(null, { 3: 1 }); await g.go(0.1); await g.pad(null, { 3: 0 }); await g.go(2.5); }
    R.spam = await g.state(); R.spamRecover = await recover(g, true, 'pad: after random buttons');
  });
  errs.push(...P.errors.map((e) => 'pad: ' + e));
  report.pad.camWorst = Math.max(...P.rows.map((r) => r.camIn));
  report.pad.deadInput = L.longestDeadInput(P.rows);

  // ---------------- invariants over the whole run
  for (const [name, s] of [['keyboard', K], ['pad', P]]) {
    const stops = L.strandedStops(s.rows);
    report[name].stops = { count: stops.length, stranded: stops.filter((x) => x.stranded).length };
    if (report[name].camWorst > 0.5) fail(5, name, `camera stood ${report[name].camWorst} m inside something solid (seen on ${s.rows.filter((r) => r.camIn > 0.5).length} steps)`, []);
    if (report[name].deadInput > 3) notes.push(`${name}: longest stretch of pressing with nothing moving: ${report[name].deadInput} s (each one is a stranded car above)`);
  }
  // pictures: flat-colour share
  report.pictures = {};
  const { chromium } = require('playwright');
  const br = await chromium.launch(); const pg = await br.newPage();
  for (const f of fs.readdirSync(out).filter((x) => x.endsWith('.png'))) {
    const b64 = fs.readFileSync(path.join(out, f)).toString('base64');
    const hist = await pg.evaluate(async (d) => { const im = new Image(); im.src = 'data:image/png;base64,' + d; await im.decode(); const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const x = c.getContext('2d'); x.drawImage(im, 0, 0); const px = x.getImageData(0, 0, c.width, c.height).data, h = {}; for (let i = 0; i < px.length; i += 4) { const k = (px[i] >> 4) + ',' + (px[i + 1] >> 4) + ',' + (px[i + 2] >> 4); h[k] = (h[k] || 0) + 1; } return h; }, b64);
    const share = L.flatShare(hist); report.pictures[f] = +share.toFixed(2);
    if (share > 0.6) fail(5, 'picture ' + f, `one flat colour fills ${Math.round(share * 100)}% of the frame`, []);
  }
  await br.close();
  // page errors (the blocked font requests are expected and left out)
  const real = errs.filter((e) => !/Failed to load resource: net::ERR_FAILED/.test(e));
  report.errors = real; report.blockedFontErrors = errs.length - real.length;
  for (const e of real) fail(6, 'page', e, []);
  report.fails = fails; report.notes = notes;
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 1));
  const by = {}; for (const f of fails) by[f.inv] = (by[f.inv] || 0) + 1;
  console.log('invariant failures by number:', JSON.stringify(by));
  for (const f of fails) console.log(`#${f.inv} ${f.scenario}: ${f.what}`);
  console.log('report:', path.join(out, 'report.json'));
  process.exitCode = fails.length ? 1 : 0;
})().catch((e) => { console.error(e); process.exit(3); });
