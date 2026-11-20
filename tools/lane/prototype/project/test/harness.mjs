// Shared test harness: serves dist/, opens the game in headless Chrome, and returns helpers.
// Usage: const h = await launch({ quality: 'low', width: 640, height: 400, port: 8790 });
import puppeteer from 'puppeteer-core';
import http from 'http';
import fs from 'fs';
import path from 'path';

const TYPES = { '.js': 'text/javascript', '.html': 'text/html', '.jpg': 'image/jpeg', '.txt': 'text/plain', '.json': 'application/json', '.md': 'text/plain' };
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function launch(o = {}) {
  const root = path.resolve(o.dist || 'dist'), port = (o.port || 8790) + (+process.env.LEDGER_PORT_SHIFT || 0), // the shift lets two authors test at once W = o.width || 640, H = o.height || 400;
  const srv = http.createServer((q, r) => {
    const f = path.join(root, decodeURIComponent(q.url.split('?')[0]));
    fs.readFile(f, (e, d) => {
      if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); r.end(d); }
    });
  }).listen(port);
  const browser = await puppeteer.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', `--window-size=${W},${H}`] });
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H });
  const errors = [];
  page.on('console', (m) => { const t = m.text(); if ((m.type() === 'error' || m.type() === 'warning') && !/404|GPU stall|fonts.g|ERR_|Automatic fallback|GroupMarker/.test(t)) errors.push(t.slice(0, 500)); });
  page.on('pageerror', (e) => errors.push('PAGEERR ' + String(e.stack || e).slice(0, 900)));
  const virtual = o.seed != null; // a seeded, stepped run: same seed, same week, whatever the machine's speed
  if (virtual) await page.evaluateOnNewDocument(VIRTUAL, o.seed);
  if (o.before) await page.evaluateOnNewDocument(o.before); // a test may stand in for the host before the page loads
  await page.evaluateOnNewDocument((q, store, render) => {
    localStorage.setItem('ledger.settings', JSON.stringify(Object.assign({ quality: q, autoRes: false, vol: 0 }, store.settings || {})));
    for (const k in store) if (k !== 'settings') localStorage.setItem(k, store[k]);
    window.LEDGER_NORENDER = !render;
  }, o.quality || 'low', o.store || {}, !!o.render);
  await page.goto(`http://localhost:${port}/index.html`);
  if (virtual) {
    // no frames run by themselves here, so the page is asked from outside until it has loaded
    for (let i = 0; i < 1800 && !(await page.evaluate(() => !!(window.LEDGER && document.getElementById('load').classList.contains('hidden')))); i++) await sleep(100);
  } else await page.waitForFunction('window.LEDGER && document.getElementById("load").classList.contains("hidden")', { timeout: 180000 });
  if (virtual) {
    await sleep(400);
    await page.evaluate((n) => { window.__V.install(); window.__V.reseed(n); }, o.seed);
  }
  const settle = () => (virtual ? page.evaluate(() => window.__V.drain()) : null);
  const ev = async (fn, ...a) => {
    const r = await page.evaluate(fn, ...a);
    await settle();
    return r;
  };
  // wait a while: real time in a plain run; in a seeded run, that many milliseconds of frames on the game's own clock
  const nap = async (ms) => {
    if (!virtual) return sleep(ms);
    await page.evaluate((ms) => window.__V.runFor(ms), ms);
    await settle();
  };
  const h = {
    page, browser, errors, ev, sleep: nap, virtual, settle,
    key: async (code) => { await ev((c) => { dispatchEvent(new KeyboardEvent('keydown', { code: c, key: c.startsWith('Key') ? c.slice(3).toLowerCase() : c })); dispatchEvent(new KeyboardEvent('keyup', { code: c })); }, code); await sleep(60); },
    step: (secs) => ev((s, v) => { LEDGER.step(s); if (v) { window.__V.now += Math.round(s * 1000); window.__V.frame(); } }, secs, virtual),
    shot: async (file, wait = 1500) => { await ev(() => { window.LEDGER_NORENDER = false; }); await sleep(wait); await page.screenshot({ path: file }); await ev(() => { window.LEDGER_NORENDER = true; }); },
    // start a new week and get past the opening letter, with the game stepped by hand from then on
    newWeek: async () => {
      await nap(800); await page.click('[data-act="new"]'); await settle(); await nap(3500);
      await page.mouse.click(W / 2, H / 2); await settle(); await nap(1500); await page.mouse.click(W / 2, H / 2 + 10); await settle(); await nap(2500);
      await ev(() => { window.LEDGER_MANUAL = true; LEDGER.step(1); });
    },
    close: async () => { await browser.close(); srv.close(); },
  };
  return h;
}

// Runs in the page before any of its own code. Math.random becomes a seeded generator (the game's own random
// numbers come from it), and __V holds a clock the test owns: once installed, timers fire in the order they are
// due without waiting on the machine, frames run only when the test asks, and "now" moves only with them.
function VIRTUAL(seed) {
  const st = { s: seed >>> 0 };
  Math.random = function () {
    st.s |= 0;
    st.s = (st.s + 0x6d2b79f5) | 0;
    let t = Math.imul(st.s ^ (st.s >>> 15), 1 | st.s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const nativeTimeout = window.setTimeout.bind(window);
  const V = (window.__V = {
    now: 0, seq: 0, timers: [], frames: [], waiters: [], pumping: false, fired: 0,
    reseed(n) { st.s = n >>> 0; },
    // Frames belong to the test from the first moment, so the street behind the title never runs on the machine's time.
    frames0() {
      window.requestAnimationFrame = (fn) => { const id = ++V.seq; V.frames.push({ id, fn }); return id; };
      window.cancelAnimationFrame = (id) => { V.frames = V.frames.filter((f) => f.id !== id); };
    },
    install() {
      V.now = 10000000; // a fixed start, later than any real time so far, so every run reads the same clock
      performance.now = () => V.now;
      Date.now = () => 656000000000 + V.now;
      window.setTimeout = (fn, ms, ...a) => { const id = ++V.seq; V.timers.push({ id, due: V.now + Math.max(0, +ms || 0), fn, a }); V.kick(); return id; };
      window.clearTimeout = (id) => { const i = V.timers.findIndex((t) => t.id === id); if (i >= 0) V.timers.splice(i, 1); };
      window.setInterval = () => ++V.seq; // nothing in the game's rules runs on an interval
      window.clearInterval = () => {};
    },
    kick() { if (!V.pumping) { V.pumping = true; nativeTimeout(V.pump, 0); } },
    pump() {
      V.pumping = false;
      let best = -1;
      for (let i = 0; i < V.timers.length; i++) if (best < 0 || V.timers[i].due < V.timers[best].due || (V.timers[i].due === V.timers[best].due && V.timers[i].id < V.timers[best].id)) best = i;
      if (best >= 0) {
        const t = V.timers.splice(best, 1)[0];
        if (t.due > V.now) V.now = t.due;
        V.fired++;
        try { t.fn(...t.a); } catch (e) { console.error('timer threw: ' + ((e && e.stack) || e)); }
      }
      if (V.timers.length && V.fired < 2e6) V.kick();
      else if (!V.pumping) { const w = V.waiters; V.waiters = []; for (const r of w) r(); }
    },
    drain() { return new Promise((res) => { if (!V.timers.length && !V.pumping) res(); else { V.waiters.push(res); V.kick(); } }); },
    frame() { const fs = V.frames; V.frames = []; for (const f of fs) { try { f.fn(V.now); } catch (e) { console.error('frame threw: ' + ((e && e.stack) || e)); } } },
    runFor(ms, each = 50) { for (let t = 0; t < ms; t += each) { V.now += each; V.frame(); } },
  });
  V.frames0();
}
