// Opens a saved copy of the published page in headless Chromium. Read-only: the file is served, never written.
// Google Fonts are blocked (the cloud cannot reach them and the page would wait). A recorder is put into the
// page that keeps one row of state per drawn frame, read from window.QR (the page's own test object).
'use strict';
const http = require('http');
const fs = require('fs');
const { chromium } = require('playwright');

function serve(file) {
  const body = fs.readFileSync(file);
  const srv = http.createServer((req, res) => {
    if (req.url === '/' || req.url.startsWith('/index.html')) { res.writeHead(200, { 'content-type': 'text/html' }); res.end(body); }
    else { res.writeHead(404); res.end(); }
  });
  return new Promise((ok) => srv.listen(0, '127.0.0.1', () => ok(srv)));
}

// A standard-mapping pad the test drives through window.__pad (axes and button values).
const PAD_INIT = `(() => {
  const pad = { id: 'Gate pad (standard)', index: 0, connected: true, mapping: 'standard', timestamp: 0,
    axes: [0, 0, 0, 0], buttons: Array.from({ length: 17 }, () => ({ pressed: false, touched: false, value: 0 })) };
  window.__pad = pad;
  window.__setPad = (axes, btn) => { if (axes) axes.forEach((v, i) => { pad.axes[i] = v; });
    if (btn) for (const k in btn) { const v = btn[k]; pad.buttons[k] = { pressed: v > 0.5, touched: v > 0, value: v }; }
    pad.timestamp = performance.now(); };
  navigator.getGamepads = () => [pad, null, null, null];
})();`;

// One row per frame: game time, speed, yaw rate, steering in and out, damage, who is driving, camera, toast.
const RECORDER = `(() => {
  window.__rows = []; window.__errs = [];
  function row() {
    const Q = window.QR; if (!Q || !Q.car) return;
    const c = Q.car, d = Q.sim.player.dmg, cam = Q.cam, t = document.getElementById('toast');
    window.__rows.push({ wall: performance.now(), t: Q.sim.time, mode: Q.mode, speed: c.speed * 2.23694, yaw: c.yawRate || 0,
      steerIn: Q.input.k.steer, steerOut: c.ctl.steer, wheel: c.steer, thr: c.ctl.throttle, brk: c.ctl.brake,
      x: c.pos[0], z: c.pos[2], dead: d.dead, worst: d.worst, points: d.points, power: d.power, walker: Q.walker.state,
      toast: t && t.classList.contains('on') ? t.textContent : '', dev: Q.input.device });
  }
  function tick() { try { row(); } catch (e) {} requestAnimationFrame(tick); }
  requestAnimationFrame(tick);
})();`;

async function open(file, { pad = false } = {}) {
  const srv = await serve(file);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 960, height: 540 }, deviceScaleFactor: 1 });
  await ctx.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
  if (pad) await ctx.addInitScript(PAD_INIT);
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push('uncaught: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.goto('http://127.0.0.1:' + srv.address().port + '/', { waitUntil: 'load', timeout: 60000 });
  await page.waitForFunction(() => window.QR && window.QR.car, null, { timeout: 60000 });
  await page.evaluate(RECORDER);
  const close = async () => { await browser.close(); srv.close(); };
  return { page, errors, close };
}

module.exports = { open };
