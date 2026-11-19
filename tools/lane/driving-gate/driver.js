// What runs inside the page. Keys and the pad reach the game through its own listeners and its own Input
// object; this only advances the world in fixed 1/120 s steps the way the page's frame loop does (poll, take
// button presses, ramp the keys, step), because software graphics here draw about 4 frames a second and a
// real-time run would take many minutes. The page's own test hooks (window.QR.hold, window.QR.run) are used.
'use strict';

const DRIVER = `(() => {
  const Q = window.QR, STEP = 1 / 120;
  Q.hold = true;                          // the page's own loop stops stepping the world; it still draws and reads keys
  window.__log = [];                      // rows: one per step
  window.__hits = [];                     // the player's impacts: game time, kind, closing mph, stage
  window.__toasts = [];                   // every message shown, with game time
  const el = document.getElementById('toast');
  new MutationObserver(() => { window.__toasts.push({ t: Q.sim.time, text: el.textContent }); })
    .observe(el, { childList: true, characterData: true, subtree: true });
  function di() {
    if (Q.walker.state !== 'drive') return null;            // on foot the walker reads keys or stick itself
    const c = Q.car; Q.input.spin = Math.max(c.wheels[0].slipRatio, c.wheels[1].slipRatio); Q.input.foot = !c.assists;
    const o = Q.input.step(STEP); o.up = false; o.down = false; return o;
  }
  window.__go = (sec, tag) => {
    const n = Math.round(sec / STEP);
    for (let i = 0; i < n; i++) {
      Q.input.poll(); Q.handle(Q.input.take());
      const paused = Q.mode === 'menu';
      if (!paused) Q.run(1, di);
      for (const e of Q.sim.events) if (e.type === 'hit' && e.car === Q.sim.player && !paused) window.__hits.push({ t: Q.sim.time, kind: e.kind, mph: +e.mph.toFixed(1), st: e.st });
      const c = Q.car, d = Q.sim.player.dmg, cam = Q.cam, W = Q.walker;
      const sx = W.state === 'drive' ? c.pos[0] : W.x, sz = W.state === 'drive' ? c.pos[2] : W.z;
      // camera inside something: the line from what it follows to where it stands crosses a solid well short of it
      const arm = Math.hypot(cam.px - sx, cam.pz - sz), f = arm > 0.3 ? cam.world.blocked(sx, sz, cam.px, cam.pz) : -1;
      window.__log.push({ tag, t: +Q.sim.time.toFixed(4), mode: Q.mode, speed: c.speed * 2.23694, yaw: c.yawRate || 0,
        steerIn: Q.input.out.steer, steerCar: c.ctl.steer, x: c.pos[0], z: c.pos[2], wx: W.x, wz: W.z, walker: W.state,
        act: Q.mode !== 'menu' && !!(Q.input.down.thr || Q.input.down.brk || Q.input.raw.thr > 0.1 || Q.input.raw.brk > 0.1 || (W.state === 'foot' && Math.hypot(Q.input.raw.moveX, Q.input.raw.moveY) > 0.2)),
        dead: d.dead, worst: d.worst, points: d.points, camIn: f >= 0 ? +(arm * (1 - f)).toFixed(2) : 0, dev: Q.input.device, toast: el.classList.contains('on') ? el.textContent : '' });
    }
    return Q.sim.time;
  };
  // put the car somewhere, standing, facing heading h (0 = +z), mended, and the camera behind it
  window.__place = (x, z, h) => {
    Q.sim.player.dmg.reset(); Q.pcar.repair(); Q.car.reset(x, z, h); Q.sim.proxy.sync(); Q.walker.seat(); Q.cam.reset(Q.car);
  };
  // how far a straight line runs from x, z on heading h before something solid (metres, up to L)
  window.__clear = (x, z, h, L) => { const f = Q.cam.world.blocked(x, z, x + Math.sin(h) * L, z + Math.cos(h) * L); return f < 0 ? L : f * L; };
  window.__state = () => { const c = Q.car, d = Q.sim.player.dmg; return { t: Q.sim.time, x: c.pos[0], z: c.pos[2], speed: c.speed * 2.23694,
    heading: Math.atan2(c.R ? c.R[6] : 0, c.R ? c.R[8] : 1), dead: d.dead, worst: d.worst, points: d.points, power: d.power, walker: Q.walker.state, mode: Q.mode }; };
})();`;

module.exports = { DRIVER };
