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
    tag: '',
    go: (sec, tag) => page.evaluate(([a, b]) => window.__go(a, b), [sec, tag || g.tag]),
    state: () => page.evaluate(() => window.__state()),
    place: (x, z, h) => { steps.length = 0; steps.push(`placed at ${x.toFixed(1)},${z.toFixed(1)} facing ${(h * 180 / Math.PI).toFixed(0)} deg`); return page.evaluate(([a, b, c]) => window.__place(a, b, c), [x, z, h]); },
    down: async (k) => { steps.push('hold ' + k); await page.keyboard.down(k); },
    up: async (k) => { steps.push('release ' + k); await page.keyboard.up(k); },
    tap: async (k) => { steps.push('tap ' + k); await page.keyboard.down(k); await g.go(0.05); await page.keyboard.up(k); },
    pad: async (axes, btn, label) => { steps.push('pad ' + (label || JSON.stringify({ axes, btn }))); await page.evaluate(([a, b]) => window.__setPad(a, b), [axes, btn]); },
    log: (from) => page.evaluate((t) => window.__log.filter((r) => r.t >= t), from),
    hits: (from) => page.evaluate((t) => window.__hits.filter((h) => h.t >= t), from),
    toasts: (from) => page.evaluate((t) => [...new Set(window.__toasts.filter((h) => h.t >= t - 0.01).map((h) => h.text).concat(window.__log.filter((r) => r.t >= t && r.toast).map((r) => r.toast)))], from),
    toastsAt: (from) => page.evaluate((t) => window.__toasts.filter((m) => m.t >= t - 1e-6), from),
    pumpOn: async () => { await page.evaluate(() => window.__pumpOn()); await page.waitForFunction(() => window.__pumpReady(), null, { timeout: 10000 }); await page.waitForTimeout(400); },
    pump: (frames, tag) => page.evaluate(([a, b]) => window.__pump(a, b), [frames, tag || g.tag]),
    pumpOff: () => page.evaluate(() => window.__pumpOff()),
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

// Names for what the car hit (the page's own collision kinds).
const KIND = { wall: 'wall', chain: 'chain', bollard: 'bollard', lamp: 'lamp post', post: 'post', parked: 'parked car', ai: 'traffic', police: 'police car', crate: 'crate' };
const named = (k) => KIND[k] || k;

// After a stop: can the player move again? Reverse, then forward. If neither moves the car, what a newcomer can
// do: get out and walk; then Backspace (pad: Back) on the car exactly as the crash left it, get back in with F
// (pad: Y), throttle; then R and throttle. Nothing is mended or moved by the gate.
async function recover(g, usePad, scenario, hitT) {
  const res = {};
  const moved = async (fn) => { const a = await g.state(); await fn(); const b = await g.state(); return +Math.hypot(b.x - a.x, b.z - a.z).toFixed(2); };
  const throttle = async (sec) => { if (usePad) { await g.pad(null, { 7: 1 }, 'throttle'); const m = await moved(() => g.go(sec)); await g.pad(null, { 7: 0 }, 'throttle off'); return m; }
    await g.down('KeyW'); const m = await moved(() => g.go(sec)); await g.up('KeyW'); return m; };
  const tS = (await g.state()).t;
  if (hitT === undefined) hitT = tS;
  if (usePad) { await g.pad(null, { 6: 1 }, 'brake trigger (reverse)'); res.reverse = await moved(() => g.go(2.5)); await g.pad(null, { 6: 0 }, 'brake off'); }
  else { await g.down('KeyS'); res.reverse = await moved(() => g.go(2.5)); await g.up('KeyS'); }
  res.forward = await throttle(2);
  const s = await g.state();
  res.dead = s.dead; res.worst = s.worst; res.points = s.points; res.power = +s.power.toFixed(2);
  res.toasts = (await g.toastsAt(hitT)).map((m) => `${(m.t - hitT).toFixed(2)} s: ${m.text}`);
  res.carMoves = res.reverse > 0.5 || res.forward > 0.5;
  if (!res.carMoves) {
    const steps = g.steps.slice();
    // 1. get out and walk
    if (usePad) { await g.pad(null, { 3: 1 }, 'Y (get out)'); await g.go(0.1); await g.pad(null, { 3: 0 }, 'Y up'); } else await g.tap('KeyF');
    await g.go(2);
    const w0 = await g.page.evaluate(() => [window.QR.walker.x, window.QR.walker.z, window.QR.walker.state]);
    if (usePad) { await g.pad([0, -1], null, 'left stick up'); await g.go(1.5); await g.pad([0, 0], null, 'stick centre'); }
    else { await g.down('KeyW'); await g.go(1.5); await g.up('KeyW'); }
    const w1 = await g.page.evaluate(() => [window.QR.walker.x, window.QR.walker.z, window.QR.walker.state]);
    res.onFoot = w0[2] === 'foot' ? +Math.hypot(w1[0] - w0[0], w1[1] - w0[1]).toFixed(2) : 0;
    // 2. Backspace on the car as the crash left it, from where the player stands, then back in
    const tB = (await g.state()).t;
    if (usePad) { await g.pad(null, { 8: 1 }, 'Back/Select (reset)'); await g.go(0.1); await g.pad(null, { 8: 0 }, 'Back up'); } else await g.tap('Backspace');
    await g.go(0.5);
    if ((await g.state()).walker !== 'drive') {
      if (usePad) { await g.pad(null, { 3: 1 }, 'Y (get in)'); await g.go(0.1); await g.pad(null, { 3: 0 }, 'Y up'); } else await g.tap('KeyF');
      await g.go(3);
    }
    const sB = await g.state();
    res.backIn = sB.walker;
    if (sB.walker !== 'drive') { await g.page.evaluate(() => window.QR.walker.seat()); g.steps.push('(could not get back in; seated by the test, damage untouched)'); }
    res.afterReset = await throttle(2);
    const sB2 = await g.state();
    res.deadAfterReset = sB2.dead; res.powerAfterReset = +sB2.power.toFixed(2);
    res.resetToasts = (await g.toastsAt(tB)).map((m) => `${(m.t - tB).toFixed(2)} s: ${m.text}`);
    // 3. R repairs
    const tR = (await g.state()).t;
    await g.tap('KeyR');
    res.afterRepair = await throttle(2);
    res.repairToasts = (await g.toastsAt(tR)).map((m) => m.text);
    res.needs = res.afterReset > 0.5 ? 'Backspace (reset)' : res.afterRepair > 0.5 ? 'R (repair)' : 'nothing worked';
    const all = await g.toastsAt(hitT);
    res.toldWhat = all.some((m) => /R repairs|repair/i.test(m.text) && m.t < tR);
    const stepsTxt = steps.concat(['then: hold S 2.5 s, hold W 2 s']);
    fail(1, scenario, `car will not move under reverse or throttle (moved ${res.reverse} m and ${res.forward} m); on foot moved ${res.onFoot} m; Backspace on the wrecked car then throttle moved ${res.afterReset} m (still dead: ${res.deadAfterReset}); recovery needs ${res.needs}${usePad ? ' (the pad has no repair button; R is on the keyboard only)' : ''}`, stepsTxt);
    if (!res.toldWhat || usePad) fail(2, scenario, `the car will not drive on; the screen ${res.toldWhat ? 'says "R repairs it" for a moment after the hit and then nothing' : 'never says what to do'}; after Backspace it says ${JSON.stringify(res.resetToasts.map((x) => x.replace(/^[^:]*: /, '')))}${usePad ? ', and R is not on the pad' : ''}`, stepsTxt);
  }
  return res;
}

// Crash lines, each aimed at a named kind of thing. Static things (walls, lamp posts, bollards) are found with
// the page's camera collision world: a straight run that ends in something solid, with room either side. A thin
// end (the line just beside it, 0.6 m either way, runs on past it) is left out here.
// Parked cars are not in that world (too low), so lines at them are aimed from their own positions, and every
// line is checked against parked cars and traffic in the way. What was really hit is read from the page's hit.
async function findTargets(g) {
  return g.page.evaluate(() => {
    const Q = window.QR, C = window.__clear, bodies = Q.sim.traffic.bodies.filter((b) => b.kind === 'parked' || b.kind === 'ai' || b.kind === 'police');
    const want = { 10: [10, 20], 20: [22, 40], 30: [40, 62], 40: [62, 95] };
    const inWay = (x, z, h, d, skip) => bodies.some((b) => { if (b === skip) return false; const dx = b.x - x, dz = b.z - z, along = dx * Math.sin(h) + dz * Math.cos(h), side = Math.abs(dx * Math.cos(h) - dz * Math.sin(h));
      return along > -1 && along < d + 1 && side < 0.9 + Math.max(b.hw, b.hl) + 0.3; });
    const roomAt = (x, z) => { let r = 99; for (let a = 0; a < 360; a += 30) r = Math.min(r, C(x, z, a * Math.PI / 180, 10)); return r; };
    const pts = []; for (let x = -70; x <= 70; x += 5) for (let z = -185; z <= 75; z += 5) pts.push([x, z]);
    const found = { pole: {}, wall: {}, parked: {} };
    for (const [x, z] of pts) {
      if (roomAt(x, z) < 2.2) continue;
      for (let a = 0; a < 360; a += 3) {
        const h = a * Math.PI / 180, d = C(x, z, h, 120);
        let v = null; for (const k in want) if (d >= want[k][0] && d <= want[k][1]) v = k; if (!v) continue;
        const sx = Math.cos(h), sz = -Math.sin(h);
        const dl = C(x + sx * 0.9, z + sz * 0.9, h, 120), dr = C(x - sx * 0.9, z - sz * 0.9, h, 120);
        if (Math.min(dl, dr) < d - 1.5 || inWay(x, z, h, d, null)) continue;
        const nl = C(x + sx * 0.6, z + sz * 0.6, h, 120), nr = C(x - sx * 0.6, z - sz * 0.6, h, 120);
        if (nl > d + 1.5 && nr > d + 1.5) continue;     // thin ends are aimed at below, from the poles themselves
        (found.wall[v] = found.wall[v] || []).push({ x, z, h, d: +d.toFixed(1), aim: 'wall' });
      }
    }
    // lamp posts: the page's camera world leaves them out, so they are found from the page's lamp light table
    // (QR.U.uLampTex: x, height, z of each lamp head). The post stands about 1.35 m from the head, away from the
    // road, on the side where a wall is nearest. Lines run along the road through the post, at each speed's
    // distance, clear of walls (0.9 m either side), of other posts and of cars.
    const lt = Q.U.uLampTex && Q.U.uLampTex.value && Q.U.uLampTex.value.image && Q.U.uLampTex.value.image.data, poles = [];
    if (lt) for (let i = 0; i + 3 < lt.length; i += 4) {
      const hx = lt[i], hz = lt[i + 2]; let best = null;
      for (const [ux, uz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const w = C(hx, hz, Math.atan2(ux, uz), 15); if (!best || w < best.w) best = { w, ux, uz }; }
      poles.push([hx + best.ux * 1.35, hz + best.uz * 1.35, best.ux, best.uz]);
    }
    for (const [px, pz, ux, uz] of poles) for (const sgn of [1, -1]) {
      const dx = -uz * sgn, dz = ux * sgn, h = Math.atan2(dx, dz);          // along the road
      for (const k in want) {
        const d = (want[k][0] + want[k][1]) / 2, x = px - dx * d, z = pz - dz * d, sx = Math.cos(h), sz = -Math.sin(h);
        if (Math.min(C(x, z, h, d), C(x + sx * 0.9, z + sz * 0.9, h, d - 0.5), C(x - sx * 0.9, z - sz * 0.9, h, d - 0.5)) < d - 0.6) continue;
        if (poles.some(([qx, qz]) => { if (qx === px && qz === pz) return false; const ex = qx - x, ez = qz - z, al = ex * dx + ez * dz, sd = Math.abs(ex * dz - ez * dx); return al > -1 && al < d && sd < 1.2; })) continue;
        if (inWay(x, z, h, d, null)) continue;
        (found.pole[k] = found.pole[k] || []).push({ x, z, h, d: +d.toFixed(1), aim: 'lamp post' });
      }
    }
    found.poleCount = poles.length;
    // parked cars: from 8 sides, the run must be clear of statics and other cars up to the car's body
    for (const b of Q.sim.traffic.parked) {
      for (let a = 0; a < 360; a += 45) {
        const h = b.yaw + a * Math.PI / 180, ext = Math.abs(Math.cos(a * Math.PI / 180)) * b.hl + Math.abs(Math.sin(a * Math.PI / 180)) * b.hw;
        for (const k in want) {
          const d = (want[k][0] + want[k][1]) / 2, D = d + ext, x = b.x - Math.sin(h) * D, z = b.z - Math.cos(h) * D;
          if (roomAt(x, z) < 2.2) continue;
          const sx = Math.cos(h), sz = -Math.sin(h);
          if (Math.min(C(x, z, h, d), C(x + sx * 0.9, z + sz * 0.9, h, d), C(x - sx * 0.9, z - sz * 0.9, h, d)) < d - 0.01 || inWay(x, z, h, d - 0.5, b)) continue;
          (found.parked[k] = found.parked[k] || []).push({ x, z, h, d: +d.toFixed(1), aim: 'parked car' });
        }
      }
    }
    const spread = (f) => (f ? [f[0], f[Math.floor(f.length / 2)], f[f.length - 1]].filter((x, i, arr) => x && arr.indexOf(x) === i) : []);
    const out = { poles: found.poleCount };
    for (const k in want) out[k] = { pole: spread(found.pole[k]), wall: spread(found.wall[k]), parked: spread(found.parked[k]) };
    return out;
  });
}
// For one speed, up to n lines mixing the kinds: a pole, a parked car, a wall, then more of each.
function pickLines(T, v, n) {
  const t = T[v] || { pole: [], wall: [], parked: [] }, out = [];
  for (let i = 0; out.length < n && i < 3; i++) for (const k of ['pole', 'parked', 'wall']) if (out.length < n && t[k][i]) out.push(t[k][i]);
  return out;
}

// Steering on the page's real frame loop at a steady speed. moves: [[label, action, seconds]]; action is a
// function that changes keys or stick. Speed is held by a hold() called every 3 frames.
async function steerRun(g, moves, hold) {
  await g.pumpOn();
  const events = [];
  for (const [label, act, sec] of moves) {
    const t = (await g.state()).t; if (act) { await act(); events.push({ t, label }); }
    const n = Math.round(sec * 20);
    for (let i = 0; i < n; i++) { await g.pump(3); await hold(); }
  }
  await g.pumpOff();
  return events;
}
function steerJudge(rows, events, inv, scenario, label, steps, { judgeInput = true } = {}) {
  let n = rows.length; for (let i = 1; i < rows.length; i++) if (rows[i - 1].speed - rows[i].speed > 1.5) { n = i - 1; break; }
  const r = rows.slice(0, n);
  if (!r.length || Math.abs(r[0].speed) < 20) { fail(inv, scenario, `${label}: not reached (not at speed, or a collision cut the run short)`, steps); return { label, notReached: true }; }
  const sp = r.map((x) => x.speed);
  const m = { label, speedMph: [+Math.min(...sp).toFixed(1), +Math.max(...sp).toFixed(1)], seconds: +(r[r.length - 1].t - r[0].t).toFixed(2), cutShort: n < rows.length,
    input: L.judgeSteer(r.map((x) => ({ t: x.t, v: x.steerIn })), events), carSteer: L.judgeSteer(r.map((x) => ({ t: x.t, v: x.steerCar })), events), yaw: L.judgeYaw(r.map((x) => ({ t: x.t, v: x.yaw })), events) };
  const judged = r[r.length - 1].t;
  for (const [what, list, on] of [['input', m.input, judgeInput], ['car steering', m.carSteer, true], ['yaw rate', m.yaw, true]]) {
    if (!on) continue;
    for (const e of list) {
      if (e.empty || e.pass) continue;
      const ev = events.find((x) => x.label === e.label); if (ev && ev.t > judged) continue;
      const why = [e.snap ? `10-90% in ${e.riseS} s (under 0.1 s)` : '', e.jump ? `${e.maxStep}${what === 'yaw rate' ? ' rad/s' : ' of full lock'} in one frame, ${e.stepAt} s after the change (limit ${what === 'yaw rate' ? L.MOVE.yawStep : L.MOVE.steerStep})` : ''].filter(Boolean).join(' and ');
      fail(inv, scenario, `${label}, ${e.label}: ${what} goes from ${e.from} to ${e.to} with ${why}`, steps);
    }
  }
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
    const T = await findTargets(g);
    R.targets = Object.fromEntries(Object.entries(T).map(([k, v]) => [k, typeof v === 'number' ? v : Object.fromEntries(Object.entries(v).map(([q, l]) => [q, l.length]))]));
    // crashes at about 10, 20, 30 and 40 mph, lines aimed at a pole, a parked car and a wall at each speed
    R.crashes = [];
    for (const v of [10, 20, 30, 40]) for (const tg of pickLines(T, v, 3)) {
      g.tag = `keyboard crash ${v} mph at ${tg.aim}`; await g.place(tg.x, tg.z, tg.h); await g.go(0.6);
      const r = await runInto(g, v, false);
      const first = r.hits[0];
      const c = { target: v, aimedAt: tg.aim, line: tg.d, hit: first ? named(first.kind) : 'nothing', mph: first ? first.mph : 0, stage: r.state.worst, dead: r.state.dead };
      if (first) {
        const steps = g.steps.slice(), sc = `crash ${v} mph into ${named(first.kind)}`;
        const told = L.damageTold(await g.toastsAt(first.t), first.t);
        c.damageWords = told.map((m) => m.text);
        if (v >= 30 && !R['shot' + v]) R['shot' + v] = await g.shot('kb-crash-' + v + '-' + first.kind);
        c.recover = await recover(g, false, sc, first.t);
        if (first.st >= 1 && !told.length) fail(2, sc, `damage stage "${['none', 'dented', 'crumpled', 'will not drive on'][first.st]}" at ${first.mph} mph closing: no words about damage on screen within 3 s of the hit; only the body shows it`, steps);
      }
      R.crashes.push(c);
    }
    R.hitKinds = {}; for (const c of R.crashes) R.hitKinds[c.hit] = (R.hitKinds[c.hit] || 0) + 1;
    // a run of 20 mph hits adds up to "will not drive on"
    const t20 = (T[20] && (T[20].wall[0] || T[20].pole[0])) || null;
    if (t20) {
      g.tag = 'repeated 20 mph hits'; const seq = []; await g.place(t20.x, t20.z, t20.h);
      const steps0 = [];
      for (let i = 0; i < 4; i++) {
        await g.page.evaluate(([x, z, h]) => { const Q = window.QR; Q.car.reset(x, z, h); Q.sim.proxy.sync(); Q.cam.reset(Q.car); }, [t20.x, t20.z, t20.h]);
        g.steps.push('car put back at the start of the same line (damage kept)'); await g.go(0.6);
        const r = await runInto(g, 20, false); seq.push({ mph: r.hits[0] ? r.hits[0].mph : 0, st: r.hits[0] ? r.hits[0].st : 0, points: r.state.points, dead: r.state.dead });
        steps0.push(...g.steps); if (r.state.dead) break;
      }
      R.smallHits = seq; const lh = await g.hits(0); R.smallHitsRecover = await recover(g, false, 'repeated 20 mph hits', lh.length ? lh[lh.length - 1].t : undefined);
    }
    // steering on keys at about 30 mph on the long road, on the page's real frame loop: press, release, press
    // again, switch A to D, switch D to A, release. W is pressed and let go every 3 frames to hold the speed.
    g.tag = 'keyboard steering'; await g.place(-1.65, 40, Math.PI); await g.down('KeyW');
    for (let i = 0; i < 60; i++) { await g.go(0.1); if ((await g.state()).speed >= 30) break; } await g.up('KeyW');
    g.steps.push('then, on the page\'s own frame loop at 60 Hz, W pressed or let go every 3 frames to hold 30 mph');
    const ts = (await g.state()).t; let wDown = false;
    const holdKb = async () => { const sp = (await g.state()).speed; const want = sp < 30; if (want !== wDown) { wDown = want; if (want) await g.page.keyboard.down('KeyW'); else await g.page.keyboard.up('KeyW'); } };
    const ev = await steerRun(g, [
      ['settle', null, 0.3],
      ['press A', () => g.down('KeyA'), 0.35], ['release A', () => g.up('KeyA'), 0.5],
      ['press D', () => g.down('KeyD'), 0.7], ['release D', () => g.up('KeyD'), 0.5],
      ['press A', () => g.down('KeyA'), 0.35], ['A to D', async () => { await g.up('KeyA'); await g.down('KeyD'); }, 0.7],
      ['D to A', async () => { await g.up('KeyD'); await g.down('KeyA'); }, 0.35], ['release A', () => g.up('KeyA'), 0.5],
    ], holdKb);
    if (wDown) await g.page.keyboard.up('KeyW');
    const rows = await g.log(ts);
    R.steer = steerJudge(rows, ev, 3, 'keyboard steering at 30 mph', 'A and D', g.steps);
    R.steerEvents = ev.map((e) => ({ label: e.label, at: +(e.t - ts).toFixed(3) }));
    R.steerTrace = rows.map((r) => [+(r.t - ts).toFixed(3), +r.speed.toFixed(1), +r.steerIn.toFixed(3), +r.steerCar.toFixed(3), +r.yaw.toFixed(3)]);
    // get out and back in (W held 5 s afterwards, the never-stranded limit)
    g.tag = 'get out and back in';
    await g.down('Space'); await g.down('KeyS'); await g.go(3); await g.up('KeyS'); await g.up('Space');
    const t1 = (await g.state()).t;
    await g.tap('KeyF'); await g.go(2.5); const out1 = await g.state();
    await g.tap('KeyF'); await g.go(2.5); const in1 = await g.state();
    await g.down('KeyW'); await g.go(5); await g.up('KeyW'); const go1 = await g.state();
    R.outIn = { out: out1.walker, backIn: in1.walker, moved: +Math.hypot(go1.x - in1.x, go1.z - in1.z).toFixed(2), toasts: await g.toasts(t1) };
    if (out1.walker !== 'foot' || in1.walker !== 'drive' || R.outIn.moved < 0.5) fail(1, 'get out and back in', JSON.stringify(R.outIn), g.steps);
    // getting out while moving
    await g.down('KeyW'); await g.go(3); await g.tap('KeyF'); await g.up('KeyW'); const t2 = (await g.state()).t; await g.go(1);
    R.outWhileMoving = { walker: (await g.state()).walker, toasts: await g.toasts(t2 - 0.1) };
    g.tag = 'wedge';
    // wedge: nose into the wall beside the start at full lock, then try to get away
    await g.place(-1.65, 37.7, Math.PI * 1.5 + 0.5); await g.down('KeyW'); await g.down('KeyA'); await g.go(4); await g.up('KeyA'); await g.up('KeyW');
    const wedgeShot = await g.shot('kb-wedge'); R.wedgeShot = wedgeShot;
    R.wedge = await recover(g, false, 'wedged nose-first into the wall at full lock');
    // spam: random keys for 10 s of game time
    let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    const keys = ['KeyW', 'KeyA', 'KeyS', 'KeyD', 'Space', 'KeyF', 'KeyR', 'Backspace', 'KeyC', 'Enter', 'KeyP', 'Escape', 'ArrowUp', 'ArrowLeft'];
    g.tag = 'random keys'; const ts3 = (await g.state()).t; g.steps.length = 0; g.steps.push('random keys, seed 7, 10 s');
    for (let i = 0; i < 60; i++) { const k = keys[Math.floor(rnd() * keys.length)]; await g.page.keyboard.down(k); await g.go(0.03 + rnd() * 0.2); await g.page.keyboard.up(k); }
    let s3 = await g.state(); if (s3.mode === 'menu') { await g.tap('Escape'); s3 = await g.state(); }
    await g.go(2.5); if ((await g.state()).walker !== 'drive') { await g.tap('KeyF'); await g.go(3); }   // a newcomer gets back in first
    R.spam = { modeAfter: s3.mode, walker: (await g.state()).walker };
    R.spamRecover = await recover(g, false, 'after random keys');
    R.spamDeadInput = L.longestDeadInput(await g.log(ts3));
    // pause and resume
    g.tag = 'pause'; const a = await g.state(); await g.tap('Escape'); await g.down('KeyW'); await g.go(2); await g.up('KeyW');
    const b = await g.state(); await g.tap('Escape'); await g.down('KeyW'); await g.go(2); await g.up('KeyW'); const c = await g.state();
    R.pause = { modeWhilePaused: b.mode, movedWhilePaused: +Math.hypot(b.x - a.x, b.z - a.z).toFixed(2), modeAfter: c.mode, movedAfter: +Math.hypot(c.x - b.x, c.z - b.z).toFixed(2) };
    if (b.mode !== 'menu' || R.pause.movedWhilePaused > 0.1 || c.mode !== 'drive' || R.pause.movedAfter < 0.5) fail(6, 'pause and resume (Esc)', JSON.stringify(R.pause), g.steps);
    // pedestrian: hold one walker still and drive at them at about 12 mph; up to 16 walkers until one is touched.
    // Rule: a person hit is hurt, never killed, and the hit is told on screen. No person touched: not reached.
    g.tag = 'pedestrian'; R.ped = { tries: [] };
    const cands = await g.page.evaluate(() => window.QR.sim.traffic.peds.map((p, i) => ({ i, x: p.x, z: p.z, state: p.state })).filter((p) => p.state === 'walk').slice(0, 16));
    for (const pd of cands) {
      const tr = { person: pd.i, at: [+pd.x.toFixed(1), +pd.z.toFixed(1)] };
      const best = await g.page.evaluate(([i]) => {
        const Q = window.QR, p = Q.sim.traffic.peds[i], C = window.__clear, roomAt = (x, z) => { let r = 99; for (let a = 0; a < 360; a += 30) r = Math.min(r, C(x, z, a * Math.PI / 180, 10)); return r; }, cars = Q.sim.traffic.bodies.filter((b) => b.kind !== 'crate');
        for (let a = 0; a < 360; a += 10) {
          const h = a * Math.PI / 180, x = p.x - Math.sin(h) * 10, z = p.z - Math.cos(h) * 10, sx = Math.cos(h), sz = -Math.sin(h);
          if (Math.min(C(x, z, h, 10.3), C(x + sx * 0.9, z + sz * 0.9, h, 10), C(x - sx * 0.9, z - sz * 0.9, h, 10)) < 9.95 || roomAt(x, z) < 1.5) continue;
          if (cars.some((b) => { const dx = b.x - x, dz = b.z - z, al = dx * Math.sin(h) + dz * Math.cos(h), sd = Math.abs(dx * Math.cos(h) - dz * Math.sin(h)); return al > -2 && al < 11 && sd < 0.9 + Math.max(b.hw, b.hl); })) continue;
          return { x, z, h };
        }
        return null;
      }, [pd.i]);
      if (!best) { tr.result = 'no clear run'; R.ped.tries.push(tr); continue; }
      await g.place(best.x, best.z, best.h);
      await g.page.evaluate((i) => { const p = window.QR.sim.traffic.peds[i]; p.pause = 99; p.speed = 0; window.__watch = i; window.__pedLog = []; }, pd.i);
      g.steps.push(`held walker ${pd.i} still at ${pd.x.toFixed(1)},${pd.z.toFixed(1)}; drove straight at them from 10 m`);
      await g.go(0.3); const tp = (await g.state()).t;
      await g.down('KeyW'); for (let i = 0; i < 40; i++) { await g.go(0.1); if ((await g.state()).speed > 12) break; } await g.up('KeyW'); await g.go(2.5);
      const pl = await g.page.evaluate(() => { const l = window.__pedLog; window.__watch = null; return l; });
      const hitRow = pl.find((r) => r.touched.includes(pd.i));
      const others = [...new Set(pl.flatMap((r) => r.touched).filter((i) => i !== pd.i))];
      const after = await g.page.evaluate((i) => { const p = window.QR.sim.traffic.peds[i]; const o = {}; for (const k in p) if (typeof p[k] !== 'object') o[k] = p[k]; return o; }, pd.i);
      tr.closest = Math.min(...pl.map((r) => r.gap)); tr.othersTouched = others.length;
      if (!hitRow) { tr.result = 'missed'; R.ped.tries.push(tr); continue; }
      const toasts = (await g.toastsAt(hitRow.t)).filter((m) => m.t <= hitRow.t + 3);
      const hurt = !['walk', 'wait', 'cross'].includes(after.state) || !!(after.hurt || after.down || after.injured);
      const killed = after.state === 'dead' || !!(after.dead || after.killed);
      Object.assign(tr, { result: 'hit', mph: +hitRow.speed.toFixed(1), stateAfter: after.state, hurt, killed, toasts: toasts.map((m) => m.text), hitsLogged: (await g.hits(tp)).map((h) => named(h.kind)) });
      R.ped.tries.push(tr); R.ped.hit = tr;
      const steps = g.steps.slice();
      const why = [!hurt ? `not hurt (still "${after.state}"; the car pushes them aside and they carry on)` : '', killed ? 'killed' : '', !toasts.length ? 'nothing on screen within 3 s of the hit' : ''].filter(Boolean);
      if (why.length) fail(7, 'a person hit by the car', `hit at ${tr.mph} mph: ${why.join('; ')}${others.length ? `; ${others.length} other people touched on the way` : ''}`, steps);
      break;
    }
    if (!R.ped.hit) fail(7, 'a person hit by the car', `not reached: no person was touched in ${R.ped.tries.length} tries (${R.ped.tries.map((t) => t.result).join(', ')})`, g.steps);
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
    for (const v of [20, 40]) for (const tg of pickLines(T, v, 2)) {
      g.tag = `pad crash ${v} mph at ${tg.aim}`; await g.place(tg.x, tg.z, tg.h); await g.go(0.6);
      const r = await runInto(g, v, true); const first = r.hits[0];
      const c = { target: v, aimedAt: tg.aim, line: tg.d, hit: first ? named(first.kind) : 'nothing', mph: first ? first.mph : 0, stage: r.state.worst, dead: r.state.dead };
      if (first) {
        const steps = g.steps.slice(), sc = `pad: crash ${v} mph into ${named(first.kind)}`;
        const told = L.damageTold(await g.toastsAt(first.t), first.t); c.damageWords = told.map((m) => m.text);
        c.recover = await recover(g, true, sc, first.t);
        if (first.st >= 1 && !told.length) fail(2, sc, `damage stage "${['none', 'dented', 'crumpled', 'will not drive on'][first.st]}" at ${first.mph} mph closing: no words about damage on screen within 3 s of the hit`, steps);
      }
      R.crashes.push(c);
    }
    // steering at 30 mph on the page's real frame loop: small, middle and full stick, each pushed over 5 frames
    // (80 ms), let go (the stick springs back at once), pushed the other way, swung left to right, let go
    R.steer = [];
    for (const amt of [0.25, 0.6, 1]) {
      g.tag = `pad steering ${amt}`; await g.place(-1.65, 40, Math.PI); await g.pad(null, { 7: 1 }, 'throttle');
      for (let i = 0; i < 60; i++) { await g.go(0.1); if ((await g.state()).speed >= 30) break; }
      g.steps.push('then, on the page\'s own frame loop at 60 Hz, throttle trigger eased every 3 frames to hold 30 mph');
      const ts = (await g.state()).t;
      const holdPad = async () => { const sp = (await g.state()).speed; await g.page.evaluate((v) => window.__setPad(null, { 7: v }), Math.max(0, Math.min(1, 0.3 + 0.08 * (30 - sp)))); };
      const sweep = async (from, to) => { for (let k = 1; k <= 5; k++) { await g.page.evaluate((v) => window.__setPad([v, 0], null), from + (to - from) * k / 5); await g.pump(1); } g.steps.push(`stick ${from} to ${to} over 80 ms`); };
      const ev = await steerRun(g, [
        ['settle', null, 0.3],
        ['push left', () => sweep(0, -amt), 0.35], ['let go', () => g.pad([0, 0], null, 'stick released'), 0.5],
        ['push right', () => sweep(0, amt), 0.7], ['let go', () => g.pad([0, 0], null, 'stick released'), 0.5],
        ['push left', () => sweep(0, -amt), 0.35], ['left to right', () => sweep(-amt, amt), 0.7], ['let go', () => g.pad([0, 0], null, 'stick released'), 0.5],
      ], holdPad);
      await g.pad(null, { 7: 0 }, 'throttle off');
      R.steer.push(steerJudge(await g.log(ts), ev, 4, 'pad steering at 30 mph', `stick ${amt}`, g.steps, { judgeInput: false }));
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
    g.tag = 'pad random buttons'; g.steps.length = 0; g.steps.push('random pad buttons and stick, seed 11, 10 s');
    for (let i = 0; i < 60; i++) { const bt = Math.floor(rnd() * 16); await g.pad([rnd() * 2 - 1, rnd() * 2 - 1], { [bt]: 1 }); await g.go(0.03 + rnd() * 0.2); await g.pad([0, 0], { [bt]: 0 }); }
    for (let i = 0; i < 17; i++) await g.pad(null, { [i]: 0 });
    let s3 = await g.state(); if (s3.mode === 'menu') { await g.pad(null, { 9: 1 }); await g.go(0.1); await g.pad(null, { 9: 0 }); }
    await g.go(2.5); s3 = await g.state(); if (s3.walker !== 'drive') { await g.pad(null, { 3: 1 }); await g.go(0.1); await g.pad(null, { 3: 0 }); await g.go(3); }
    R.spam = await g.state(); R.spamRecover = await recover(g, true, 'pad: after random buttons');
  });
  errs.push(...P.errors.map((e) => 'pad: ' + e));
  report.pad.camWorst = Math.max(...P.rows.map((r) => r.camIn));
  report.pad.deadInput = L.longestDeadInput(P.rows);

  // ---------------- invariants over the whole run
  for (const [name, s] of [['keyboard', K], ['pad', P]]) {
    const stops = L.strandedStops(s.rows);
    report[name].stops = { count: stops.length, stranded: stops.filter((x) => x.stranded).length };
    if (report[name].stops.stranded > 0) fail(1, name + ' whole run', `${report[name].stops.stranded} of ${stops.length} stops left the player pressing to move and not moving 0.5 m within 5 s (${stops.filter((x) => x.stranded).map((x) => { const row = s.rows.find((q) => q.t >= x.t - 1e-3); return `${x.t} s in ${row && row.tag ? row.tag : 'set-up'}`; }).join('; ')})`, []);
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
