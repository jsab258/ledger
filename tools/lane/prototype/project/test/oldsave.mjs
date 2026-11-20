// A save written by an older build must load in this one, with its Ledger rebuilt into the new book.
// OLD=<folder holding an older build of the page> node test/oldsave.mjs   (default: dist_old)
import puppeteer from 'puppeteer-core';
import http from 'http'; import fs from 'fs'; import path from 'path';
const serve = (dir, port) => http.createServer((q, r) => { const f = path.join(path.resolve(dir), decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { 'content-type': f.endsWith('.js') ? 'text/javascript' : f.endsWith('.html') ? 'text/html' : 'application/octet-stream' }); r.end(d); } }); }).listen(port);
const s1 = serve(process.env.OLD || 'dist_old', 8781), s2 = serve('dist', 8782);
const b = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--window-size=1000,600'] });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms)); const log = (...a) => console.log(...a);
const open = async (url, pre) => { const p = await b.newPage(); await p.setViewport({ width: 1000, height: 600 }); const errs = []; p.on('console', (m) => { const t = m.text(); if ((m.type() === 'error' || m.type() === 'warning') && !/404|GPU stall|fonts.g|ERR_|Automatic fallback|GroupMarker/.test(t)) errs.push(t.slice(0, 300)); }); p.on('pageerror', (e) => errs.push('PAGEERR ' + String(e.stack || e).slice(0, 500))); await p.evaluateOnNewDocument((pre) => { localStorage.setItem('ledger.settings', JSON.stringify({ quality: 'low', autoRes: false, vol: 0 })); window.LEDGER_NORENDER = true; for (const k in pre || {}) localStorage.setItem(k, pre[k]); }, pre); await p.goto(url); await p.waitForFunction('window.LEDGER && document.getElementById("load").classList.contains("hidden")', { timeout: 180000 }); return { p, errs, ev: (fn, ...a) => p.evaluate(fn, ...a) }; };
try {
  const A = await open('http://localhost:8781/index.html'); const key = async (c) => { await A.ev((c) => { dispatchEvent(new KeyboardEvent('keydown', { code: c })); dispatchEvent(new KeyboardEvent('keyup', { code: c })); }, c); await sleep(100); };
  await A.p.click('[data-act="new"]'); await sleep(3500); await A.p.mouse.click(500, 300); await sleep(1500); await A.p.mouse.click(500, 310); await sleep(2500);
  await A.ev(() => { window.LEDGER_MANUAL = true; LEDGER.step(1); });
  const flush = async () => { for (let i = 0; i < 50; i++) { await A.ev(() => LEDGER.step(0.2)); if ((await A.ev(() => LEDGER.ui.modal)) !== 'dialog') { await sleep(150); await A.ev(() => LEDGER.step(0.3)); if ((await A.ev(() => LEDGER.ui.modal)) !== 'dialog') return; continue; } await key('KeyE'); await A.ev(() => LEDGER.step(0.1)); await key('KeyE'); await key('Digit1'); } };
  const tp = (x, z) => A.ev((x, z) => { const t = LEDGER.G.tom; t.x = x; t.z = z; }, x, z);
  await tp(6.2, 30); await A.ev(() => LEDGER.step(1)); await flush(); await tp(6.3, 36.9); await A.ev(() => LEDGER.step(1)); await flush();
  await A.ev(() => { const t = LEDGER.G.tom; t.x = 7.0; t.z = 36; t.ang = 1.57; LEDGER.step(0.5); }); await key('KeyE'); await A.ev(() => LEDGER.step(1)); await flush();
  await A.ev(() => { const t = LEDGER.G.tom, P = LEDGER.G.people.sheila; t.x = P.x; t.z = P.z + 1.9; t.ang = Math.PI; LEDGER.step(0.5); }); await key('KeyE'); await A.ev(() => LEDGER.step(0.3)); await flush();
  await A.ev(() => { LEDGER.leaveRoom(); LEDGER.G.t = 17.4 * 60; LEDGER.step(1); }); await tp(6.3, 36.9); await A.ev(() => LEDGER.step(1)); await key('KeyE'); await A.ev(() => LEDGER.step(0.5)); await flush();
  log('old build:', await A.ev(() => JSON.stringify({ tour: LEDGER.G.story.flags.tour, ask1: LEDGER.G.story.flags.ask1, met: Object.keys(LEDGER.G.ledger.met), names: LEDGER.G.ledger.names || null, t: Math.round(LEDGER.G.t) })));
  await A.ev(() => LEDGER.saveNow(true)); await sleep(500);
  const store = await A.ev(() => { const o = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k.startsWith('ledger.save')) o[k] = localStorage.getItem(k); } return o; });
  log('old save keys:', Object.keys(store).join(','), 'bytes', Object.values(store).reduce((a, v) => a + v.length, 0), 'old errors', A.errs.length);
  const B = await open('http://localhost:8782/index.html', store); const k2 = async (c) => { await B.ev((c) => { dispatchEvent(new KeyboardEvent('keydown', { code: c })); dispatchEvent(new KeyboardEvent('keyup', { code: c })); }, c); await sleep(120); };
  await sleep(800); log('title offers:', await B.ev(() => [...document.querySelectorAll('#tmenu [data-act]')].map((x) => x.textContent).join(' | ')));
  await B.ev(() => { window.LEDGER_MANUAL = true; document.querySelector('#tmenu [data-act="cont"]').click(); }); await sleep(3500); await B.ev(() => LEDGER.step(1));
  log('new build after Continue:', await B.ev(() => JSON.stringify({ phase: LEDGER.G.story.phase, ask1: LEDGER.G.story.flags.ask1, job: LEDGER.G.story.job, t: Math.round(LEDGER.G.t), eyes: !!LEDGER.G.settings.eyes })));
  await B.ev(() => { LEDGER.talk.open('ron', { free: true }); }); await sleep(300);
  log('talk head (a name from the old save):', await B.ev(() => document.getElementById('twho').textContent), '| names now:', await B.ev(() => Object.keys(LEDGER.G.ledger.names).join(',')));
  await B.ev(() => LEDGER.talk.key('Tab')); log('lines:', await B.ev(() => LEDGER.talk.lines().map((l) => `[${l.job}] ${l.text}`).join(' / '))); await B.ev(() => LEDGER.talk.leave()); await B.ev(() => LEDGER.step(1.5));
  // the old save has no book: it is rebuilt from the old Ledger on first open, and every entry has a source event
  const led = await B.ev(() => { LEDGER.ledger.open('people'); const r = { part: LEDGER.ledger.read().part, faults: LEDGER.ledger.faults(), first: LEDGER.ledger.book().slice(0, 4).map((e) => e.what) }; LEDGER.ledger.close(); return r; });
  log('the Ledger, rebuilt from the old save:', JSON.stringify(led).slice(0, 700));
  await B.ev(() => LEDGER.step(20)); await B.ev(() => LEDGER.saveNow(true)); log('saved again; report says:', (await B.ev(() => LEDGER.reportText())).split('\n').slice(5, 7).join(' // ').slice(0, 300));
  // the one-shot (20 Nov 2026): an old save has no real town in it. It opens a fresh one at the save's clock, told what its people saw.
  const tw = await B.ev(() => ({ live: LEDGER.game.town.live(), why: LEDGER.game.town.why(), old: LEDGER.G.x.town.old || null, faults: LEDGER.game.faults.length, refusals: LEDGER.game.town.refusals.length }));
  log('the real town after an old save:', JSON.stringify(tw).slice(0, 900));
  const townOk = tw.live && /before the real town/.test(tw.why) && !tw.faults && !tw.refusals;
  log('ERRORS new build', B.errs.length, B.errs.slice(0, 4).join('\n'));
  const phase = await B.ev(() => LEDGER.G.story.phase);
  log(phase === 'play' && !B.errs.length && led.faults.entries > 0 && led.faults.entriesWithNoSourceEvent === 0 && townOk ? 'PASS' : 'FAIL');
} catch (e) { log('TEST FAIL', String(e.stack || e).slice(0, 600)); }
await b.close(); s1.close(); s2.close();
