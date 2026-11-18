// Shared test harness: serves dist/, opens the game in headless Chrome, and returns helpers.
// Usage: const h = await launch({ quality: 'low', width: 640, height: 400, port: 8790 });
import puppeteer from 'puppeteer-core';
import http from 'http';
import fs from 'fs';
import path from 'path';

const TYPES = { '.js': 'text/javascript', '.html': 'text/html', '.jpg': 'image/jpeg', '.txt': 'text/plain', '.json': 'application/json', '.md': 'text/plain' };
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function launch(o = {}) {
  const root = path.resolve(o.dist || 'dist'), port = o.port || 8790, W = o.width || 640, H = o.height || 400;
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
  if (o.before) await page.evaluateOnNewDocument(o.before); // a test may stand in for the host before the page loads
  await page.evaluateOnNewDocument((q, store, render) => {
    localStorage.setItem('ledger.settings', JSON.stringify(Object.assign({ quality: q, autoRes: false, vol: 0 }, store.settings || {})));
    for (const k in store) if (k !== 'settings') localStorage.setItem(k, store[k]);
    window.LEDGER_NORENDER = !render;
  }, o.quality || 'low', o.store || {}, !!o.render);
  await page.goto(`http://localhost:${port}/index.html`);
  await page.waitForFunction('window.LEDGER && document.getElementById("load").classList.contains("hidden")', { timeout: 180000 });
  const ev = (fn, ...a) => page.evaluate(fn, ...a);
  const h = {
    page, browser, errors, ev, sleep,
    key: async (code) => { await ev((c) => { dispatchEvent(new KeyboardEvent('keydown', { code: c, key: c.startsWith('Key') ? c.slice(3).toLowerCase() : c })); dispatchEvent(new KeyboardEvent('keyup', { code: c })); }, code); await sleep(60); },
    step: (secs) => ev((s) => LEDGER.step(s), secs),
    shot: async (file, wait = 1500) => { await ev(() => { window.LEDGER_NORENDER = false; }); await sleep(wait); await page.screenshot({ path: file }); await ev(() => { window.LEDGER_NORENDER = true; }); },
    // start a new week and get past the opening letter, with the game stepped by hand from then on
    newWeek: async () => {
      await sleep(800); await page.click('[data-act="new"]'); await sleep(3500);
      await page.mouse.click(W / 2, H / 2); await sleep(1500); await page.mouse.click(W / 2, H / 2 + 10); await sleep(2500);
      await ev(() => { window.LEDGER_MANUAL = true; LEDGER.step(1); });
    },
    close: async () => { await browser.close(); srv.close(); },
  };
  return h;
}
