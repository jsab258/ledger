// The story player (the one-shot's giant prompt, 20 Nov 2026).
//
// A play story is played here the way its rules say (ONE-SHOT-PROMPT.md, "How every story is played and judged"):
//   1. Played, never set: from New game, or from a save the game itself made in another story (Continue).
//   2. Real inputs: keys, mouse look and pad go in as browser input events; no test call moves Tom, a person, a
//      car or the clock. Every frame is simulated, at 60 frames a second on a clock the test owns; a timer fires
//      only when that clock reaches it, so nothing is skipped by the harness.
//   3. Judged by what a player meets: the words on screen (read from the page as drawn), the sound mix (the names
//      and loudness the game's audio was asked to play), and the world as rendered (where a body is, how it moves).
//   6. Twice the same: every story's record of what was met is digested, and run() plays it twice and compares.
//   8. A story ends by saving through the pause menu; the browser's save is kept under the story's name.
//
// The player's own knowledge used here: where Tom stands and which way the camera looks (he sees both), and the
// town's street map (a player learns it; the walking graph stands in for that).
import puppeteer from 'puppeteer-core';
import http from 'http';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

const TYPES = { '.js': 'text/javascript', '.html': 'text/html', '.jpg': 'image/jpeg', '.txt': 'text/plain', '.json': 'application/json', '.md': 'text/plain', '.wasm': 'application/wasm', '.mjs': 'text/javascript' };
const SAVES = path.resolve(process.env.LEDGER_STORY_SAVES || '../story-saves') // beside the work folder: a rebuild leaves the saves alone;
export const FPS = 60;

// Runs in the page before its own code: a seeded Math.random and a strict clock.
function CLOCK(seed) {
  const st = { s: seed >>> 0 };
  Math.random = function () {
    st.s = (st.s + 0x6d2b79f5) | 0;
    let t = Math.imul(st.s ^ (st.s >>> 15), 1 | st.s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const nativeTimeout = window.setTimeout.bind(window);
  const ch = new MessageChannel();
  let yieldRes = null;
  ch.port1.onmessage = () => { const r = yieldRes; yieldRes = null; if (r) r(); };
  const S = (window.__S = {
    now: 10000000, seq: 0, timers: [], frames: [], frameNo: 0, on: false, sounds: [], heard: [], log: [], keys: {}, mouseDown: false, pad: null, subsSeen: {}, subsLog: [], headsSeen: {}, notedSeen: {}, notedLog: [], eachs: {},
    yield: () => new Promise((r) => { yieldRes = r; ch.port2.postMessage(0); }),
    // The same start for every run: chance set to its seed, and the clock put on one fixed reading (the loading took
    // its own number of frames on the machine's time; timers already waiting keep their distance). From here the clock
    // is the fixed reading plus whole frames, so a timer falls due on the same frame in every run, to the last bit.
    reseed: (n) => { st.s = n >>> 0; const d = 20000000 - S.now; for (const t of S.timers) t.due += d; S.now = 20000000; S.base = 20000000; S.since = 0; },
    nativeTimeout,
    install() {
      if (S.on) return;
      S.on = true;
      performance.now = () => S.now;
      Date.now = () => 656000000000 + Math.floor(S.now);
      window.setTimeout = (fn, ms, ...a) => { const id = ++S.seq; S.timers.push({ id, due: S.now + Math.max(0, +ms || 0), fn, a }); return id; };
      window.clearTimeout = (id) => { const i = S.timers.findIndex((t) => t.id === id); if (i >= 0) S.timers.splice(i, 1); };
      window.setInterval = (fn, ms, ...a) => { const id = ++S.seq; S.timers.push({ id, due: S.now + Math.max(1, +ms || 0), fn, a, every: Math.max(1, +ms || 0) }); return id; };
      window.clearInterval = window.clearTimeout;
    },
    fireDue() {
      for (let guard = 0; guard < 10000; guard++) {
        let best = -1;
        for (let i = 0; i < S.timers.length; i++) if (S.timers[i].due <= S.now && (best < 0 || S.timers[i].due < S.timers[best].due || (S.timers[i].due === S.timers[best].due && S.timers[i].id < S.timers[best].id))) best = i;
        if (best < 0) return;
        const t = S.timers[best];
        if (t.every) t.due += t.every; else S.timers.splice(best, 1);
        try { t.fn(...t.a); } catch (e) { console.error('timer threw: ' + ((e && e.stack) || e)); }
      }
    },
    // one frame of 1/60 s: timers that are due, then the game's frame, then the page's own promises
    async frame() {
      if (S.base) { S.since++; S.now = S.base + (S.since * 1000) / 60; } else S.now += 1000 / 60;
      S.frameNo++;
      S.fireDue();
      const fs = S.frames; S.frames = [];
      for (const f of fs) { try { f.fn(S.now); } catch (e) { console.error('frame threw: ' + ((e && e.stack) || e)); } }
      // the record every story shares: each subtitle the first time it is on screen (with the real seconds played), and
      // whose head has turned to him on the street
      if (window.LEDGER && LEDGER.G && LEDGER.G.story.phase === 'play' && S.frameNo % 3 === 0) {
        for (const e of document.querySelectorAll('#subs .s')) { const s = e.innerText.trim(); if (s && !S.subsSeen[s]) { S.subsSeen[s] = 1; S.subsLog.push({ s, at: Math.round(LEDGER.G.played * 100) / 100, t: Math.round(LEDGER.G.t * 10) / 10 }); } }
        if (S.frameNo % 15 === 0) for (const Q of LEDGER.G.named.concat(LEDGER.G.crowd)) if (!Q.gone && Q.mind && Q.mind.look > 0 && (Q.space === 'street' || Q.win)) S.headsSeen[Q.id] = 1;
        { const nd = document.getElementById('noted'); if (nd && nd.classList.contains('on')) { const s = nd.innerText.trim(); if (s && !S.notedSeen[s]) { S.notedSeen[s] = 1; S.notedLog.push({ s, at: Math.round(LEDGER.G.played * 100) / 100 }); } } }
      }
      for (const k in S.eachs) { try { S.eachs[k](); } catch (e) { console.error('story watcher threw: ' + ((e && e.stack) || e)); } }
      await S.yield();
    },
    // run frames until n are done or until() says so (checked every frame); bot() may press keys each frame
    async run(n, until, bot) {
      for (let i = 0; i < n; i++) {
        if (bot) bot(i);
        await S.frame();
        if (until && until()) return i + 1;
      }
      return until ? -1 : n;
    },
    kd(code, key) { if (S.keys[code]) return; S.keys[code] = true; const t = document.activeElement && document.activeElement !== document.body ? document.activeElement : window; t.dispatchEvent(new KeyboardEvent('keydown', { code, key: key || (code.startsWith('Key') ? code.slice(3).toLowerCase() : code), bubbles: true, cancelable: true })); },
    ku(code) { if (!S.keys[code]) return; S.keys[code] = false; const t = document.activeElement && document.activeElement !== document.body ? document.activeElement : window; t.dispatchEvent(new KeyboardEvent('keyup', { code, bubbles: true, cancelable: true })); },
    allUp() { for (const k in S.keys) if (S.keys[k]) S.ku(k); },
    // mouse look: the middle button held on the picture, then moves (the game turns the camera on a drag)
    look(dxPixels, dyPixels = 0) {
      const cv = document.getElementById('c');
      if (!S.mouseDown) { cv.dispatchEvent(new MouseEvent('mousedown', { button: 1, bubbles: true })); S.mouseDown = true; }
      window.dispatchEvent(new MouseEvent('mousemove', { movementX: dxPixels, movementY: dyPixels, bubbles: true }));
    },
    lookEnd() { if (S.mouseDown) { window.dispatchEvent(new MouseEvent('mouseup', { button: 1, bubbles: true })); S.mouseDown = false; } },
  });
  // The way a player picks through a room or round a parked car: the shortest clear way on a fine grid of the ground
  // he can stand on. Returns corner points, or null when there is no way.
  S.plan = (ax, az, bx, bz, tight) => {
    // a little clear of everything, as a walking man keeps (and, when there is no such way, as tight as it takes)
    const m = tight ? 0 : 0.2, C = 0.3;
    const ok = (x, z) => LEDGER.standable(x, z) && (!m || (LEDGER.standable(x + m, z) && LEDGER.standable(x - m, z) && LEDGER.standable(x, z + m) && LEDGER.standable(x, z - m)));
    const clear = (x0, z0, x1, z1) => { const n = Math.ceil(Math.hypot(x1 - x0, z1 - z0) / 0.15); for (let i = 1; i <= n; i++) if (!ok(x0 + ((x1 - x0) * i) / n, z0 + ((z1 - z0) * i) / n)) return false; return true; };
    if (clear(ax, az, bx, bz)) return [[bx, bz]];
    const pad = 9, x0 = Math.min(ax, bx) - pad, z0 = Math.min(az, bz) - pad, W = Math.ceil((Math.abs(ax - bx) + 2 * pad) / C), H = Math.ceil((Math.abs(az - bz) + 2 * pad) / C);
    if (W * H > 250000) return null;
    const id = (i, j) => j * W + i, ci = (x) => Math.round((x - x0) / C), cj = (z) => Math.round((z - z0) / C);
    const free = new Int8Array(W * H); // 0 unknown, 1 free, 2 solid
    const isFree = (i, j) => { if (i < 0 || j < 0 || i >= W || j >= H) return false; const k = id(i, j); if (!free[k]) free[k] = ok(x0 + i * C, z0 + j * C) ? 1 : 2; return free[k] === 1; };
    let si = ci(ax), sj = cj(az), gi = ci(bx), gj = cj(bz);
    // standing against something: the plan starts from the nearest clear spot beside him
    if (!isFree(si, sj)) { let best = null; for (let r = 1; r < 5 && !best; r++) for (let di = -r; di <= r; di++) for (let dj = -r; dj <= r; dj++) if (!best && isFree(si + di, sj + dj)) best = [si + di, sj + dj]; if (!best) return null; [si, sj] = best; }
    if (!isFree(gi, gj)) { let best = null; for (let r = 1; r < 8 && !best; r++) for (let di = -r; di <= r; di++) for (let dj = -r; dj <= r; dj++) if (!best && isFree(gi + di, gj + dj)) best = [gi + di, gj + dj]; if (!best) return null; [gi, gj] = best; }
    const g = new Float32Array(W * H).fill(1e9), from = new Int32Array(W * H).fill(-1), open = [[0, si, sj]];
    g[id(si, sj)] = 0;
    let found = false;
    for (let guard = 0; open.length && guard < 400000; guard++) {
      let b = 0; for (let k = 1; k < open.length; k++) if (open[k][0] < open[b][0]) b = k;
      const [, i, j] = open.splice(b, 1)[0];
      if (i === gi && j === gj) { found = true; break; }
      for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]) {
        const ni = i + di, nj = j + dj;
        if (!isFree(ni, nj) || (di && dj && (!isFree(i + di, j) || !isFree(i, j + dj)))) continue;
        const ng = g[id(i, j)] + (di && dj ? 1.414 : 1);
        if (ng < g[id(ni, nj)]) { g[id(ni, nj)] = ng; from[id(ni, nj)] = id(i, j); open.push([ng + Math.hypot(ni - gi, nj - gj), ni, nj]); }
      }
    }
    if (!found) return null;
    let pts = [], k = id(gi, gj);
    while (k >= 0) { pts.unshift([x0 + (k % W) * C, z0 + Math.floor(k / W) * C]); k = from[k]; }
    // only the corners: from each point, the furthest one that can be walked to straight
    const out = []; let at = 0;
    while (at < pts.length - 1) { let far = at + 1; for (let m = pts.length - 1; m > at + 1; m--) if (clear(pts[at][0], pts[at][1], pts[m][0], pts[m][1])) { far = m; break; } out.push(pts[far]); at = far; }
    if (clear(out[out.length - 1][0], out[out.length - 1][1], bx, bz)) out.push([bx, bz]);
    return out;
  };
  { const plan0 = S.plan; S.plan = (ax, az, bx, bz) => plan0(ax, az, bx, bz, false) || plan0(ax, az, bx, bz, true); }
  // can he walk straight from here to there, a little clear of everything?
  S.clearWay = (ax, az, bx, bz) => { const m = 0.2, ok = (x, z) => LEDGER.standable(x, z) && LEDGER.standable(x + m, z) && LEDGER.standable(x - m, z) && LEDGER.standable(x, z + m) && LEDGER.standable(x, z - m); const n = Math.ceil(Math.hypot(bx - ax, bz - az) / 0.15); for (let i = 1; i <= n; i++) if (!ok(ax + ((bx - ax) * i) / n, az + ((bz - az) * i) / n)) return false; return true; };
  window.requestAnimationFrame = (fn) => { const id = ++S.seq; S.frames.push({ id, fn }); return id; };
  window.cancelAnimationFrame = (id) => { S.frames = S.frames.filter((f) => f.id !== id); };
  // a pad the test owns (the game reads navigator.getGamepads each frame)
  const realPads = navigator.getGamepads ? navigator.getGamepads.bind(navigator) : () => [];
  navigator.getGamepads = () => (S.pad ? [S.pad] : realPads());
  S.padOn = () => { S.pad = { id: 'story pad (standard)', index: 0, connected: true, mapping: 'standard', timestamp: 0, axes: [0, 0, 0, 0], buttons: Array.from({ length: 17 }, () => ({ pressed: false, touched: false, value: 0 })) }; };
  S.padBtn = (i, v) => { S.pad.buttons[i] = { pressed: v > 0.5, touched: v > 0, value: v }; S.pad.timestamp = S.now; };
  S.padAxis = (i, v) => { S.pad.axes[i] = v; S.pad.timestamp = S.now; };
}

// What is on the screen now, read from the page as it is drawn (only what is visible counts).
function SCREEN() {
  const vis = (e) => { if (!e) return false; const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05) return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && (e.offsetParent !== null || cs.position === 'fixed'); };
  const txt = (id) => { const e = document.getElementById(id); return e && vis(e) ? e.innerText.trim() : ''; };
  const list = (sel) => [...document.querySelectorAll(sel)].filter(vis).map((e) => e.innerText.trim()).filter(Boolean);
  return {
    subs: list('#subs .s'),
    prompts: list('#prompt > div'),
    bubbles: list('#bubbles > *'),
    dialog: vis(document.getElementById('dialog')) ? { who: txt('dwho'), text: txt('dtxt'), opts: list('#dopts > *') } : null,
    talk: vis(document.getElementById('talk')) ? { who: txt('twho'), log: list('#tlog > *'), lines: list('#tlines > *'), hint: txt('thint'), ai: txt('tai'), acts: list('#tacts > *'), slip: txt('tslip'), leave: vis(document.getElementById('tbye')) } : null,
    panel: txt('panel'),
    book: txt('book'),
    ledger: txt('lbook'),
    title: vis(document.getElementById('title')) ? list('#tmenu button') : null,
    fade: txt('fade'),
    obj: txt('obj'),
    news: txt('news'),
    hud: [...document.querySelectorAll('#hud > *')].filter(vis).map((e) => e.id).filter(Boolean),
  };
}

export async function open(o = {}) {
  const root = path.resolve(o.dist || 'dist'), port = (o.port || 8950) + (+process.env.LEDGER_PORT_SHIFT || 0), W = o.width || 1280, H = o.height || 720;
  const srv = http.createServer((q, r) => {
    const f = path.join(root, decodeURIComponent(q.url.split('?')[0]));
    fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); r.end(d); } });
  }).listen(port);
  const browser = await puppeteer.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', `--window-size=${W},${H}`] });
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H });
  const errors = [];
  page.on('console', (m) => { const t = m.text(); if ((m.type() === 'error' || m.type() === 'warning') && !/404|GPU stall|fonts.g|ERR_|Automatic fallback|GroupMarker|WebGL/.test(t)) errors.push(t.slice(0, 500)); });
  page.on('pageerror', (e) => errors.push('PAGEERR ' + String(e.stack || e).slice(0, 900)));
  await page.evaluateOnNewDocument(CLOCK, o.seed == null ? 20261120 : o.seed);
  const store = Object.assign({}, o.from ? JSON.parse(fs.readFileSync(path.join(SAVES, o.from + '.json'), 'utf8')) : {});
  await page.evaluateOnNewDocument((store, render, settings) => {
    if (!sessionStorage.getItem('story.booted')) {
      sessionStorage.setItem('story.booted', '1');
      for (const k in store) localStorage.setItem(k, store[k]);
      const s0 = JSON.parse(localStorage.getItem('ledger.settings') || '{}');
      localStorage.setItem('ledger.settings', JSON.stringify(Object.assign({ quality: 'low', autoRes: false, vol: 0 }, s0, settings)));
    }
    window.LEDGER_NORENDER = !render;
    window.resizeTo = (w, h) => window.__resizeWindow(w, h);
    window.LEDGER_STORY = true; // the page knows only that frames are stepped (it shows no loading wait on real time)
  }, store, !!o.render, o.settings || {});
  await (page._pw || page).exposeFunction('__resizeWindow', async (w, h) => { await page.setViewport({ width: w, height: h }); P.W = w; P.H = h; });
  await page.goto(`http://localhost:${port}/index.html`);
  // the page loads on the machine's time (files, the town code); frames are ours from the first
  for (let i = 0; i < 3000; i++) {
    const ready = await page.evaluate(async () => { for (let k = 0; k < 5; k++) await window.__S.frame(); return !!(window.LEDGER && document.getElementById('load').classList.contains('hidden')); });
    if (ready) break;
    await new Promise((r) => setTimeout(r, 50));
    if (errors.length && i > 40) throw new Error('the page did not start: ' + errors.slice(0, 3).join(' | '));
    if (i === 2999) throw new Error('the page never finished loading');
  }
  await page.evaluate(() => window.__S.install());
  const SEED = o.seed == null ? 20261120 : o.seed;
  const rec = []; // the record of what was met, in order: the digest of a run
  const P = {
    page, browser, errors, rec, W, H,
    ev: (fn, ...a) => page.evaluate(fn, ...a),
    // ----- time -----
    frames: (n) => page.evaluate((n) => window.__S.run(n), n),
    secs: (s) => P.frames(Math.round(s * FPS)),
    // run until the page-side test fn (given as a function and its arguments) is true; returns real seconds taken, or -1
    async until(fn, maxSecs = 30, ...a) {
      const n = await page.evaluate(({ src, n, a }) => { const f = (0, eval)('(' + src + ')'); return window.__S.run(n, () => f(...a)); }, { src: fn.toString(), n: Math.round(maxSecs * FPS), a });
      return n < 0 ? -1 : n / FPS;
    },
    // ----- inputs -----
    down: (code) => page.evaluate((c) => window.__S.kd(c), code),
    up: (code) => page.evaluate((c) => window.__S.ku(c), code),
    async tap(code, holdFrames = 4) { await P.down(code); await P.frames(holdFrames); await P.up(code); await P.frames(2); },
    // the use key on the thing ahead; when two things share the key the game asks which, and the one wanted is picked
    async use(rx, code = 'KeyE') {
      await P.tap(code);
      await P.frames(20);
      if ((await P.screen()).dialog) await P.choice();
      const s = await P.screen();
      if (s.dialog && s.dialog.opts.length) {
        const i = s.dialog.opts.findIndex((o) => rx.test(o));
        await P.tap('Digit' + ((i < 0 ? s.dialog.opts.length - 1 : i) + 1));
        await P.frames(10);
        return i >= 0;
      }
      return true;
    },
    // pick one of a written choice's lines by its words (the digit keys)
    // a written choice once its words are all out and its lines are offered (the words come a letter at a time)
    async choice() {
      await P.until(() => !document.querySelector('#dialog:not(.hidden)') || document.querySelectorAll('#dopts .opt').length > 0, 4);
      return (await P.screen()).dialog;
    },
    async pick(rx) {
      await P.choice();
      const s = await P.screen();
      if (!s.dialog || !s.dialog.opts.length) return false;
      const i = s.dialog.opts.findIndex((o) => rx.test(o));
      if (i < 0) return false;
      await P.tap('Digit' + (i + 1));
      await P.frames(12);
      return true;
    },
    // in a talk: say one of his suggested lines, chosen by its words (Tab shows them; Up, Down and Enter choose)
    async talkSay(rx) {
      let s = await P.screen();
      if (!s.talk) return false;
      if (!s.talk.lines.length) { await P.tap('Tab'); await P.frames(12); s = await P.screen(); }
      const lines = s.talk.lines, i = lines.findIndex((l) => rx.test(l));
      if (i < 0) return false;
      const sel = await page.evaluate(() => [...document.querySelectorAll('#tlines > *')].findIndex((e) => e.classList.contains('on')));
      for (let k = 0; k < (i - Math.max(0, sel) + lines.length) % lines.length; k++) await P.tap('ArrowDown');
      const n0 = await page.evaluate(() => document.querySelectorAll('#tlog > *').length);
      await P.tap('Enter');
      await P.until((n0) => document.querySelectorAll('#tlog > *').length >= n0 + 2, 6, n0);
      await P.frames(20);
      return true;
    },
    // in a talk: type his own words and say them
    async talkType(text) {
      await page.evaluate(() => document.getElementById('tin').focus());
      await P.type(text);
      const n0 = await page.evaluate(() => document.querySelectorAll('#tlog > *').length);
      await P.tap('Enter');
      await P.until((n0) => document.querySelectorAll('#tlog > *').length >= n0 + 2, 9, n0);
      await P.frames(20);
    },
    // read a written line on (E) until none is up; returns the lines read
    async readOn(max = 12) {
      const out = [];
      for (let k = 0; k < max; k++) {
        const s = await P.screen();
        if (!s.dialog) break;
        if (s.dialog.opts.length) break;
        out.push((s.dialog.who ? s.dialog.who + ': ' : '') + s.dialog.text);
        await P.tap('KeyE'); await P.frames(30);
      }
      return out;
    },
    async hold(code, secs) { await P.down(code); await P.secs(secs); await P.up(code); await P.frames(2); },
    type: async (text) => { await page.evaluate((t) => { const el = document.activeElement; if (el && el.tagName === 'INPUT') { for (const c of t) { el.value += c; el.dispatchEvent(new InputEvent('input', { data: c, bubbles: true })); } } }, text); await P.frames(6); },
    click: async (sel) => { await page.evaluate((s) => { const e = document.querySelector(s); if (e) e.click(); }, sel); await P.frames(4); },
    look: (dx, dy = 0) => page.evaluate(({ dx, dy }) => window.__S.look(dx, dy), { dx, dy }),
    // ----- what a player meets -----
    screen: () => page.evaluate(SCREEN),
    // every subtitle met so far, in order, each with the real seconds of play when it first showed
    subsLog: () => page.evaluate(() => window.__S.subsLog.slice()),
    heads: () => page.evaluate(() => Object.keys(window.__S.headsSeen)),
    headsReset: () => page.evaluate(() => { window.__S.headsSeen = {}; }),
    // the low belief line: every text it has shown
    beliefs: () => page.evaluate(() => window.__S.notedLog.slice()),
    // save from the pause menu and keep the browser's store under a name
    async save(name) { await P.tap('Escape'); await P.frames(18); await P.click('[data-act="save"]'); await P.frames(30); const ok = /Saved/.test((await P.screen()).book); await P.tap('Escape'); await P.frames(18); if ((await P.screen()).book) { await P.tap('Escape'); await P.frames(18); } if (name) await P.keep(name); return ok; },
    // open the Ledger on one of its pages (L, then E to turn the pages); returns the page's words
    async ledger(part) { await P.tap('KeyL'); await P.frames(20); for (let k = 0; k < 5; k++) { const on = await page.evaluate(() => { const b = document.querySelector('#lbook button.on'); return b ? b.innerText.trim().toLowerCase() : ''; }); if (on === part.toLowerCase()) break; await P.tap('KeyE'); await P.frames(15); } return (await P.screen()).ledger; },
    ledgerClose: async () => { await P.tap('KeyL'); await P.frames(20); },
    world: (fn, ...a) => page.evaluate(fn, ...a),
    tom: () => page.evaluate(() => { const t = LEDGER.G.tom; return { x: t.x, z: t.z, ang: t.ang, space: t.space, inCar: !!t.inCar, room: LEDGER.ui.roomName || null, run: !!t.run }; }),
    clock: () => page.evaluate(() => LEDGER.G.t), // game minutes (the watch's own value), for timing a story's steps
    played: () => page.evaluate(() => LEDGER.G.played),
    note(what, v) { rec.push([what, v]); },
    shot: async (file) => { await page.evaluate(() => { window.LEDGER_NORENDER = false; }); await P.frames(3); await page.screenshot({ path: file }); await page.evaluate(() => { window.LEDGER_NORENDER = true; }); },
    // ----- walking by keys and mouse look, at a player's pace -----
    // Walk to a point on the street (metres): the camera is turned by mouse moves towards the next corner of the way
    // and W is held. run: Shift held. Returns seconds taken, or -1 when not there in maxSecs.
    async walkTo(x, z, opt = {}) {
      const r = await page.evaluate(async ({ x, z, opt }) => {
        const S = window.__S, G = LEDGER.G, M = LEDGER.map;
        const t = G.tom, near = opt.near == null ? 1.2 : opt.near, max = Math.round((opt.maxSecs || 120) * 60);
        const hyp = (ax, az, bx, bz) => Math.hypot(ax - bx, az - bz);
        let pts = [[x, z]];
        if (t.space === 'street' && !opt.straight && hyp(t.x, t.z, x, z) > 45) {
          const a = M.nearNode(t.x, t.z), b = M.nearNode(x, z);
          pts = M.path(a, b).map((i) => [M.NODES[i].x, M.NODES[i].z]).concat([[x, z]]);
          while (pts.length > 1 && hyp(t.x, t.z, pts[1][0], pts[1][1]) < hyp(pts[0][0], pts[0][1], pts[1][0], pts[1][1])) pts.shift(); // never walk back to a first node behind him
        }
        // each leg is walked by the clear way round what stands in it
        const legs = pts; pts = [];
        const replan = () => { const leg = legs[0]; const way = S.plan(t.x, t.z, leg[0], leg[1]); pts = way || [leg]; S.lastPlan = { from: [Math.round(t.x * 10) / 10, Math.round(t.z * 10) / 10], way: way ? way.map((p) => [Math.round(p[0] * 10) / 10, Math.round(p[1] * 10) / 10]) : 'no way found' }; };
        replan();
        let stuck = 0, lx = t.x, lz = t.z, side = 0, sideT = 0, tries = 0;
        const angd = (a, b) => { let d = b - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return d; };
        let held = 0; // the game stopped under him (a box has opened): after a second and a half the walk is given up
        const done = await S.run(max, () => held > 90 || hyp(t.x, t.z, x, z) <= near || (opt.until && (0, eval)('(' + opt.until + ')')()), () => {
          if (G.paused) { held++; return; }
          held = 0;
          // a corner is done with when he stands on it, or can already walk straight to the one after it
          while (pts.length > 1 && (hyp(t.x, t.z, pts[0][0], pts[0][1]) < 0.2 || (S.frameNo % 4 === 0 && hyp(t.x, t.z, pts[0][0], pts[0][1]) < 1.5 && S.clearWay(t.x, t.z, pts[1][0], pts[1][1])))) pts.shift();
          if (legs.length > 1 && hyp(t.x, t.z, legs[0][0], legs[0][1]) < 2.2) { legs.shift(); replan(); }
          const p = pts[0], want = Math.atan2(p[0] - t.x, p[1] - t.z);
          if (t.space !== 'street') {
            // in a room the view is fixed, so he is steered as a player steers there: by the four move keys, eight ways
            const yaw = LEDGER.cam.yaw, dx = Math.sin(want), dz = Math.cos(want);
            const f = dx * Math.sin(yaw) + dz * Math.cos(yaw), r = dx * -Math.cos(yaw) + dz * Math.sin(yaw);
            const set = (code, on) => (on ? S.kd(code) : S.ku(code));
            set('KeyW', f > 0.38); set('KeyS', f < -0.38); set('KeyD', r > 0.38); set('KeyA', r < -0.38);
            if (opt.slow) S.kd('KeyZ');
            if (S.frameNo % 30 === 0) { const d = hyp(t.x, t.z, lx, lz); stuck = d < 0.2 ? stuck + 1 : 0; lx = t.x; lz = t.z; if (stuck >= 2) { stuck = 0; replan(); } }
            return;
          }
          const off = angd(LEDGER.cam.yaw, want);
          // the mouse turns the view at most about 200 degrees a second
          const sens = 0.0028 * (G.settings.sens || 1), step = Math.max(-0.058, Math.min(0.058, off));
          if (Math.abs(off) > 0.01) S.look(-step / sens);
          if (Math.abs(off) < 0.9) S.kd('KeyW'); else S.ku('KeyW');
          if (opt.run) S.kd('ShiftLeft');
          if (opt.slow) S.kd('KeyZ');
          // held against something: step round it, as a player does
          // (first one way for a second and a half; if that did not free him, the other way for longer)
          if (S.frameNo % 30 === 0) { const d = hyp(t.x, t.z, lx, lz); stuck = d < 0.25 ? stuck + 1 : 0; lx = t.x; lz = t.z; if (stuck >= 2 && !sideT) { side = side > 0 ? -1 : 1; tries++; sideT = 30 + 20 * tries; stuck = 0; replan(); } }
          if (sideT > 0) { sideT--; S.kd(side > 0 ? 'KeyD' : 'KeyA'); S.ku('KeyW'); if (!sideT) { S.ku('KeyD'); S.ku('KeyA'); } }
        });
        S.ku('KeyW'); S.ku('KeyS'); S.ku('ShiftLeft'); S.ku('KeyZ'); S.ku('KeyA'); S.ku('KeyD'); S.lookEnd();
        return held > 90 ? -1 : done;
      }, { x, z, opt: Object.assign({}, opt, { until: opt.until ? opt.until.toString() : null }) });
      await P.frames(2);
      return r < 0 ? -1 : r / FPS;
    },
    // ----- driving by the keys: W and S, A and D, as a careful player drives -----
    // Drive through the points in order and stop at the last. He slows for bends, brakes for anybody or anything in his
    // way, and backs off a kerb he has run onto. Returns seconds taken, or -1.
    async drive(pts, opt = {}) {
      const r = await page.evaluate(async ({ pts, opt }) => {
        const S = window.__S, G = LEDGER.G, c = G.car;
        const hyp = (ax, az, bx, bz) => Math.hypot(ax - bx, az - bz);
        const angd = (a, b) => { let d = b - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return d; };
        const set = (code, on) => (on ? S.kd(code) : S.ku(code));
        let i = 0, stuck = 0, lx = c.x, lz = c.z, back = 0, stopped = 0, waited = 0, edge = 0, prev = [c.x, c.z]; let lastAng = c.ang;
        const top = opt.speed || 8.5, max = Math.round((opt.maxSecs || 120) * 60);
        const blocker = () => {
          const fx = Math.sin(c.ang), fz = Math.cos(c.ang), reach = 4 + (c.v * c.v) / 12;
          const inWay = (x, z, half) => { const dx = x - c.x, dz = z - c.z, f = dx * fx + dz * fz, l = Math.abs(dx * fz - dz * fx); return f > 1.5 && f < reach + half && l < 1.25 + half * 0.4; };
          for (const Q of G.named.concat(G.crowd)) if (!Q.gone && !Q.inCar && Q.space === 'street' && inWay(Q.x, Q.z, 0.3)) return 'person ' + Q.id;
          for (const v of LEDGER.streetThings().cars) if (!(v.parked && opt.besideParked) && inWay(v.xMetres, v.zMetres, v.lengthMetres / 2)) return v.parked ? 'parked car' : 'car';
          return null;
        };
        S.driveDbg = null;
        const n = await S.run(max, () => i >= pts.length || (opt.until && (0, eval)('(' + opt.until + ')')()), () => {
          if (!G.tom.inCar) { i = pts.length; return; }
          const p = pts[i], last = i === pts.length - 1, d = hyp(c.x, c.z, p[0], p[1]);
          if (last && d < (opt.stopWithin || 3)) {
            set('KeyW', false); set('KeyA', false); set('KeyD', false);
            // (the automatic takes a brake held at a standstill for reverse: stopped, he holds it on the handbrake)
            set('KeyS', c.v > 0.25); set('Space', Math.abs(c.v) <= 0.25);
            if (Math.abs(c.v) <= 0.25) { set('KeyS', false); if (++stopped > 20) { set('Space', false); i++; } }
            return;
          }
          if (!last && d < 4.5) { prev = p; i++; return; }
          // he aims a few car lengths ahead along the lane, not at the far end of it: so he keeps his lane
          let aim = p;
          { const sx = p[0] - prev[0], sz = p[1] - prev[1], L = Math.hypot(sx, sz); if (L > 12) { const u = Math.max(0, Math.min(1, ((c.x - prev[0]) * sx + (c.z - prev[1]) * sz) / (L * L))), a = Math.min(1, u + 9 / L); aim = [prev[0] + sx * a, prev[1] + sz * a]; } }
          const err = angd(c.ang, Math.atan2(aim[0] - c.x, aim[1] - c.z));
          if (back > 0) { // backing off something: the wheel turned the other way
            back--;
            set('Space', false); set('KeyW', false); set('KeyS', true); set('KeyA', err < -0.1); set('KeyD', err > 0.1);
            if (!back) set('KeyS', false);
            return;
          }
          // somebody or something in his way: he waits; if it does not move in a few seconds he edges round it
          const b = edge > 0 ? null : blocker();
          if (edge > 0) edge--;
          if (b && Math.abs(c.v) < 0.5) { if (++waited > 240) { waited = 0; edge = 240; } } else if (!b) waited = Math.max(0, waited - 1);
          const want = b ? 0 : Math.min(edge > 0 ? 3 : top, last ? Math.max(2.2, d * 0.7) : 99, Math.abs(err) > 1.0 ? 3 : Math.abs(err) > 0.35 ? 5 : 99, !last && d < 12 && pts[i + 1] && Math.abs(angd(Math.atan2(p[0] - c.x, p[1] - c.z), Math.atan2(pts[i + 1][0] - p[0], pts[i + 1][1] - p[1]))) > 0.6 ? 5 : 99);
          // he steers to where the car will be pointing in a third of a second, not where it points now (no weaving)
          { const yr = angd(lastAng, c.ang) * 60; lastAng = c.ang; const e2 = err - yr * 0.3; set('KeyA', e2 > 0.05); set('KeyD', e2 < -0.05); }
          set('KeyW', want > 0 && c.v < want - 0.3); set('KeyS', c.v > want + 1.2 || (want === 0 && c.v > 0.3));
          set('Space', want === 0 && Math.abs(c.v) <= 0.3); // waiting: on the handbrake, never on a held brake
          if (S.frameNo % 60 === 0) { const moved = hyp(c.x, c.z, lx, lz); lx = c.x; lz = c.z; stuck = moved < 0.3 && want > 0 ? stuck + 1 : 0; if (stuck >= 2) { stuck = 0; back = 80; } S.driveDbg = { leg: i, blocker: b, want: Math.round(want * 10) / 10, err: Math.round(err * 100) / 100, edge, waited }; }
        });
        for (const k of ['KeyW', 'KeyS', 'KeyA', 'KeyD', 'Space']) S.ku(k);
        return n;
      }, { pts, opt: Object.assign({}, opt, { until: opt.until ? opt.until.toString() : null }) });
      await P.frames(2);
      return r < 0 ? -1 : r / FPS;
    },
    car: () => page.evaluate(() => { const c = LEDGER.G.car; return { x: Math.round(c.x * 10) / 10, z: Math.round(c.z * 10) / 10, ang: Math.round(c.ang * 100) / 100, v: Math.round(c.v * 10) / 10, dmg: c.dmg, dbg: window.__S.driveDbg }; }),
    // New game from the title. The page's loading ran on the machine's time, so chance is set to its seed here: the same
    // keys from here on give the same game. The town's own code is waited for before a frame is played against it.
    async newGame() {
      await page.evaluate((n) => { window.__S.reseed(n); window.__S.frameNo = 0; }, SEED); // (the count of frames too: the loading took its own number)
      await P.click('[data-act="new"]');
      if ((await P.screen()).title) await P.click('[data-act="new"]'); // it asks twice when it would replace a saved game
      await page.evaluate(() => (LEDGER.game.town.ready ? LEDGER.game.town.ready() : null));
      await P.frames(2);
    },
    // Continue from the title (the save the store was started with)
    async cont() {
      await page.evaluate((n) => { window.__S.reseed(n); window.__S.frameNo = 0; }, SEED); // (the count of frames too: the loading took its own number)
      await P.click('[data-act="cont"]');
      await page.evaluate(() => (LEDGER.game.town.ready ? LEDGER.game.town.ready() : null));
      const ok = await P.until(() => LEDGER.G.story.phase === 'play' && !LEDGER.G.paused && !document.getElementById('hud').classList.contains('hidden'), 20);
      await page.evaluate(() => LEDGER.game.town.ready && LEDGER.game.town.ready());
      await P.frames(10);
      return ok;
    },
    // turn the view (mouse) to face a point
    async face(x, z) {
      await page.evaluate(async ({ x, z }) => {
        const S = window.__S, t = LEDGER.G.tom;
        const angd = (a, b) => { let d = b - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return d; };
        await S.run(120, () => Math.abs(angd(LEDGER.cam.yaw, Math.atan2(x - t.x, z - t.z))) < 0.02, () => { const off = angd(LEDGER.cam.yaw, Math.atan2(x - t.x, z - t.z)); S.look(-Math.max(-0.058, Math.min(0.058, off)) / (0.0028 * (LEDGER.G.settings.sens || 1))); });
        S.lookEnd();
        // his body turns when he steps: a touch of forward, as a player gives it
        S.kd('KeyW'); await S.run(40, () => Math.abs(angd(t.ang, LEDGER.cam.yaw)) < 0.2); S.ku('KeyW'); await S.run(10);
      }, { x, z });
    },
    // ----- saves -----
    // The browser's own store after the game saved: kept under the story's name for the stories that start from it.
    async keep(name) {
      const store = await page.evaluate(() => { const o = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); o[k] = localStorage.getItem(k); } return o; });
      fs.mkdirSync(SAVES, { recursive: true });
      fs.writeFileSync(path.join(SAVES, name + '.json'), JSON.stringify(store));
    },
    digest: () => crypto.createHash('sha256').update(JSON.stringify(rec)).digest('hex').slice(0, 16),
    // a trace of the world once a second (for finding where two runs part ways): LEDGER_STORY_TRACE=1
    traceOn: () => page.evaluate(() => { const S = window.__S; S.h = []; S.eachs.h = () => { if (S.frameNo % 60 || !window.LEDGER || LEDGER.G.story.phase !== 'play') return; const G = LEDGER.G; const h = (a) => { let x = 0; for (const v of a) x = (x * 31 + Math.round(v * 100)) | 0; return x; }; S.h.push([S.frameNo, Math.round(G.t * 1000), h([G.tom.x, G.tom.z, G.car.x, G.car.z]), h(G.named.flatMap((Q) => [Q.x, Q.z])), h(G.crowd.flatMap((Q) => [Q.x, Q.z])), h(LEDGER.streetThings().cars.flatMap((c) => [c.xMetres, c.zMetres])), Math.round(G.played * 100)]); }; }),
    trace: () => page.evaluate(() => window.__S.h || []),
    close: async () => { await browser.close(); srv.close(); },
  };
  return P;
}

// A story: play(P, t) is run twice from the same start; both runs must meet the same things (rule 6).
// t.ok(cond, what, got) marks one "must happen"; t.note(what, value) adds to the record that both runs must share.
export async function run(id, o, play, variants = ['']) {
  const fails = [];
  const twice = !process.env.LEDGER_STORY_ONCE;
  let port = (o.port || 8950);
  for (const variant of variants) {
    if (process.env.LEDGER_STORY_ONLY && variant !== process.env.LEDGER_STORY_ONLY) continue; // one way alone, when mending it
    const digests = [], recs = [];
    for (let n = 1; n <= (twice ? 2 : 1); n++) {
      const P = await open(Object.assign({}, o, { port: ++port, from: typeof o.from === 'function' ? o.from(variant) : o.from }));
      const tag = (variant ? variant + ', ' : '') + 'run ' + n;
      if (process.env.LEDGER_STORY_TRACE) await P.traceOn();
      const t = {
        variant, first: n === 1,
        ok(cond, what, got) {
          if (cond) { if (n === 1) console.log('ok   ' + (variant ? '[' + variant + '] ' : '') + what); } else { fails.push(what); console.log('TEST FAIL ' + tag + ': ' + what + (got !== undefined ? ' | got ' + JSON.stringify(got).slice(0, 600) : '')); }
          return !!cond;
        },
        note: (what, v) => P.note(what, v),
      };
      try {
        await play(P, t, n, variant);
      } catch (e) {
        fails.push('threw');
        console.log('TEST FAIL ' + tag + ': the story stopped: ' + String((e && e.stack) || e).slice(0, 900));
      }
      // the checkers' watchers (23 Nov 2026, after round 1 of the proof): checks the stories never made
      try { await watchers(P, t); } catch (e) { t.ok(false, 'watch: the watchers could run', String(e).slice(0, 200)); }
      const faults = await P.page.evaluate(() => (window.LEDGER && LEDGER.game ? LEDGER.game.faults.slice(0, 5) : ['no game'])).catch(() => ['page gone']);
      t.ok(!faults.length, 'no fault inside any system', faults);
      t.ok(!P.errors.length, 'no page error', P.errors.slice(0, 3));
      digests.push(P.digest()); recs.push(JSON.stringify(P.rec));
      if (process.env.LEDGER_STORY_TRACE) { fs.mkdirSync(SAVES, { recursive: true }); fs.writeFileSync(path.join(SAVES, id + (variant ? '.' + variant : '') + '.run' + n + '.trace.json'), JSON.stringify(await P.trace().catch(() => []))); }
      if (process.env.LEDGER_STORY_REC) { fs.mkdirSync(SAVES, { recursive: true }); fs.writeFileSync(path.join(SAVES, id + (variant ? '.' + variant : '') + '.run' + n + '.rec.json'), JSON.stringify(P.rec, null, 1)); }
      await P.close();
    }
    if (twice) {
      if (digests[0] === digests[1]) console.log('ok   ' + (variant ? '[' + variant + '] ' : '') + 'the same keys gave the same result twice (' + digests[0] + ')');
      else { fails.push('twice'); console.log('TEST FAIL ' + (variant ? '[' + variant + '] ' : '') + 'the two runs differ: ' + digests.join(' and ') + ' | run 1 ' + recs[0].slice(0, 700) + ' | run 2 ' + recs[1].slice(0, 700)); }
    }
  }
  console.log(fails.length ? id + ' FAIL (' + fails.length + ')' : id + ' PASS');
  process.exit(fails.length ? 1 : 0);
}

// ---- the checkers' watchers: run at the end of every story's play, in the same page ----
// 1. a save and reload give back the same game: debts, the Ledger, money, the story's flags and what people remember,
//    compared as the game holds them (round 1: a save that dropped the debt book, or what witnesses saw, passed every story).
// 2. nobody says the same line of five words or more twice in one story, and no two people share one (round 1: every
//    list giving its first line passed every story).
async function watchers(P, t) {
  const live = await P.page.evaluate(() => !!(window.LEDGER && LEDGER.G && LEDGER.G.story && LEDGER.G.story.phase === 'play')).catch(() => false);
  if (!live) return;
  const said = {};
  for (const x of await P.subsLog()) {
    const m = /^([A-Z][A-Z .,'-]+?)\s*"(.+)"\s*$/.exec(String(x.s || ''));
    if (!m) continue;
    const who = m[1].trim(), line = m[2].trim();
    if ((line.match(/[A-Za-z']+/g) || []).length < 5) continue;
    (said[line] = said[line] || []).push(who);
  }
  const rep = Object.entries(said).filter(([, w]) => w.length > 1).map(([l, w]) => w.join(' + ') + ': ' + l.slice(0, 80));
  t.ok(!rep.length, 'watch: no line of five words or more said twice, by one person or by two', rep.slice(0, 6));
  const snap = () => P.page.evaluate(() => {
    const G = LEDGER.G, j = (o) => JSON.stringify(o === undefined ? null : o);
    const mem = {};
    for (const id in G.minds || {}) { const M = G.minds[id]; if (M && Array.isArray(M.mem)) mem[id] = M.mem.map((m) => [m.e, m.src]).sort().join(';'); }
    return { debts: j(G.debts), ledger: j(G.ledger), pocket: j(G.money && G.money.clean), tin: j(G.money && G.money.dirty), flags: j(G.story && G.story.flags), memory: j(mem) };
  });
  const a = await snap();
  const text = await P.page.evaluate(() => LEDGER.saveText());
  await P.page.evaluate((s) => LEDGER.restore(s), text);
  await P.frames(30);
  const b = await snap();
  const diff = Object.keys(a).filter((k) => a[k] !== b[k]);
  t.ok(!diff.length, 'watch: a save and reload give back the same game (debts, Ledger, money, flags, memories)', diff.map((k) => k + ': ' + a[k].slice(0, 90) + ' | after: ' + b[k].slice(0, 90)));
}
