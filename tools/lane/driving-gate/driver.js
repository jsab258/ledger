// What runs inside the page. Keys and the pad reach the game through its own listeners and its own Input object.
//
// Two ways of advancing the world:
//
// 1. window.__pump(frames): the page's REAL frame loop. page.js catches every requestAnimationFrame callback
//    before the page loads; in pump mode the gate calls those callbacks itself with timestamps 1/60 s apart, so
//    the page's own loop (OS in the bundle) runs exactly as on a 60 Hz screen: it polls the pad, takes button
//    presses, sets the slip and driver-aid flags, steps Input.step and the world at 1/120 s, and moves the camera.
//    Only drawing is skipped (renderer.render is a no-op while pumping), because software graphics here take
//    about 235 ms a frame. Steering is measured this way.
//
// 2. window.__go(seconds): the gate's own copy of that loop, used for the long scenarios (crashes, wedges, spam)
//    because it is simpler to stop between steps. The page exposes no step that reads input (QR.run takes the
//    input from a function, QR.stepWorld takes it ready-made), so the copy rebuilds it. Where it differs from the
//    page's loop (OS):
//      - it polls the pad and takes button presses once per 1/60 s frame, as the page does, then runs two steps;
//      - gear up and down flags (page variables B1 and H1, not exposed) are always false; the runs use the
//        automatic gearbox, which ignores them;
//      - the look-back button and right-stick look are not passed to the camera (QR.run cannot pass them);
//      - the demo driver and QR.script paths are not copied (the gate never uses them).
'use strict';

const DRIVER = `(() => {
  const Q = window.QR, STEP = 1 / 120;
  Q.hold = true;                          // the page's own loop stops stepping the world; it still polls and takes keys
  window.__log = [];                      // rows: one per step (copy) or per frame (pump)
  window.__hits = [];                     // the player's impacts: game time, kind, closing mph, stage
  window.__toasts = [];                   // every message shown, with the game time of the step that showed it
  window.__pedLog = [];                   // while a person is watched: contact with the car, per step
  window.__watch = null;                  // index of the person watched
  const el = document.getElementById('toast');
  // takeRecords() is read every step, so each message gets the time of the step that set it (a plain observer
  // would only report after the whole batch of steps had run). Messages set between batches (keys the page's
  // own loop handled, such as Backspace or R) reach the observer's callback; the world is held then, so the
  // game time is still right.
  const obs = new MutationObserver((recs) => { if (recs.length) window.__toasts.push({ t: Q.sim.time, text: el.textContent }); });
  obs.observe(el, { childList: true, characterData: true, subtree: true });
  let lastHit = Q.sim.player.lastHit || null;
  function di() {
    if (Q.walker.state !== 'drive') return null;            // on foot the walker reads keys or stick itself
    const c = Q.car; Q.input.spin = Math.max(c.wheels[0].slipRatio, c.wheels[1].slipRatio); Q.input.foot = !c.assists;
    const o = Q.input.step(STEP); o.up = false; o.down = false; return o;
  }
  function rec(tag) {
    if (obs.takeRecords().length) window.__toasts.push({ t: Q.sim.time, text: el.textContent });
    const lh = Q.sim.player.lastHit;
    if (lh && lh !== lastHit) { lastHit = lh; if (Q.mode !== 'menu') window.__hits.push({ t: lh.t, kind: lh.kind, mph: +lh.mph.toFixed(1), st: lh.st }); }
    const c = Q.car, d = Q.sim.player.dmg, cam = Q.cam, W = Q.walker;
    const sx = W.state === 'drive' ? c.pos[0] : W.x, sz = W.state === 'drive' ? c.pos[2] : W.z;
    // camera inside something: the line from what it follows to where it stands crosses a solid well short of it
    const arm = Math.hypot(cam.px - sx, cam.pz - sz), f = arm > 0.3 ? cam.world.blocked(sx, sz, cam.px, cam.pz) : -1;
    window.__log.push({ tag, t: +Q.sim.time.toFixed(4), mode: Q.mode, speed: c.speed * 2.23694, yaw: c.yawRate || 0,
      steerIn: Q.input.out.steer, steerCar: c.ctl.steer, x: c.pos[0], z: c.pos[2], wx: W.x, wz: W.z, walker: W.state,
      act: Q.mode !== 'menu' && !!(Q.input.down.thr || Q.input.down.brk || Q.input.raw.thr > 0.1 || Q.input.raw.brk > 0.1 || (W.state === 'foot' && Math.hypot(Q.input.raw.moveX, Q.input.raw.moveY) > 0.2)),
      dead: d.dead, worst: d.worst, points: d.points, camIn: f >= 0 ? +(arm * (1 - f)).toFixed(2) : 0, dev: Q.input.device, toast: el.classList.contains('on') ? el.textContent : '' });
    if (window.__watch !== null) {
      const peds = Q.sim.traffic.peds;
      const touched = []; peds.forEach((p, i) => { if (p.moving === 2) touched.push(i); });
      const p = peds[window.__watch];
      window.__pedLog.push({ t: Q.sim.time, touched, state: p.state, x: p.x, z: p.z, gap: +(Math.hypot(p.x - c.pos[0], p.z - c.pos[2])).toFixed(2), speed: c.speed * 2.23694 });
    }
  }
  window.__go = (sec, tag) => {
    const frames = Math.round(sec * 60);
    for (let i = 0; i < frames; i++) {
      Q.input.poll(); Q.handle(Q.input.take());
      for (let k = 0; k < 2; k++) { if (Q.mode !== 'menu') Q.run(1, di); rec(tag); }
    }
    return Q.sim.time;
  };
  // the page's real frame loop, driven at 60 Hz with drawing skipped
  const R = window.__raf, rr = Q.core.renderer, realRender = rr.render;
  window.__pumpOn = () => { R.manual = true; };                // then wait until the pending frames are caught
  window.__pumpReady = () => R.q.length > 0;
  window.__pump = (frames, tag) => {
    Q.hold = false; rr.render = () => {};
    try { for (let i = 0; i < frames; i++) { R.last += 1000 / 60; for (const cb of R.q.splice(0)) cb(R.last); rec(tag); } }
    finally { Q.hold = true; rr.render = realRender; }
    return Q.sim.time;
  };
  window.__pumpOff = () => { Q.hold = true; R.release(); };
  // put the car somewhere, standing, facing heading h (0 = +z), mended, and the camera behind it (set-up only,
  // never used to recover from a crash)
  window.__place = (x, z, h) => {
    Q.sim.player.dmg.reset(); Q.pcar.repair(); Q.car.reset(x, z, h); Q.sim.proxy.sync(); Q.walker.seat(); Q.cam.reset(Q.car);
  };
  // how far a straight line runs from x, z on heading h before something solid in the page's camera collision
  // world (metres, up to L). That world holds walls, buildings, lamps, posts and bollards, and moving bodies 1.6 m
  // or taller; parked cars and traffic (1.4 m) are not in it.
  window.__clear = (x, z, h, L) => { const f = Q.cam.world.blocked(x, z, x + Math.sin(h) * L, z + Math.cos(h) * L); return f < 0 ? L : f * L; };
  window.__state = () => { const c = Q.car, d = Q.sim.player.dmg; return { t: Q.sim.time, x: c.pos[0], z: c.pos[2], speed: c.speed * 2.23694,
    heading: Math.atan2(c.R ? c.R[6] : 0, c.R ? c.R[8] : 1), dead: d.dead, worst: d.worst, points: d.points, power: d.power, walker: Q.walker.state, mode: Q.mode }; };
})();`;

module.exports = { DRIVER };
