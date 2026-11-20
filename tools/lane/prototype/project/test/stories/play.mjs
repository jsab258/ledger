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
const SAVES = path.resolve(process.env.LEDGER_STORY_SAVES || 'story-saves');
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
    now: 10000000, seq: 0, timers: [], frames: [], frameNo: 0, on: false, sounds: [], heard: [], log: [], keys: {}, mouseDown: false, pad: null, subsSeen: {}, subsLog: [], headsSeen: {}, eachs: {},
    yield: () => new Promise((r) => { yieldRes = r; ch.port2.postMessage(0); }),
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
      S.now += 1000 / 60;
      S.frameNo++;
      S.fireDue();
      const fs = S.frames; S.frames = [];
      for (const f of fs) { try { f.fn(S.now); } catch (e) { console.error('frame threw: ' + ((e && e.stack) || e)); } }
      // the record every story shares: each subtitle the first time it is on screen (with the real seconds played), and
      // whose head has turned to him on the street
      if (window.LEDGER && LEDGER.G && LEDGER.G.story.phase === 'play' && S.frameNo % 3 === 0) {
        for (const e of document.querySelectorAll('#subs .s')) { const s = e.innerText.trim(); if (s && !S.subsSeen[s]) { S.subsSeen[s] = 1; S.subsLog.push({ s, at: Math.round(LEDGER.G.played * 100) / 100, t: Math.round(LEDGER.G.t * 10) / 10 }); } }
        if (S.frameNo % 15 === 0) for (const Q of LEDGER.G.named.concat(LEDGER.G.crowd)) if (!Q.gone && Q.mind && Q.mind.look > 0 && (Q.space === 'street' || Q.win)) S.headsSeen[Q.id] = 1;
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
    talk: vis(document.getElementById('talk')) ? { who: txt('twho'), log: list('#tlog > *'), lines: list('#tlines > *'), hint: txt('thint'), ai: txt('tai'), acts: list('#tacts > *'), slip: txt('tslip') } : null,
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
    async hold(code, secs) { await P.down(code); await P.secs(secs); await P.up(code); await P.frames(2); },
    type: async (text) => { await page.evaluate((t) => { const el = document.activeElement; if (el && el.tagName === 'INPUT') { for (const c of t) { el.value += c; el.dispatchEvent(new InputEvent('input', { data: c, bubbles: true })); } } }, text); await P.frames(6); },
    click: async (sel) => { await page.evaluate((s) => { const e = document.querySelector(s); if (e) e.click(); }, sel); await P.frames(4); },
    look: (dx, dy = 0) => page.evaluate(({ dx, dy }) => window.__S.look(dx, dy), { dx, dy }),
    // ----- what a player meets -----
    screen: () => page.evaluate(SCREEN),
    // every subtitle met so far, in order, each with the real seconds of play when it first showed
    subsLog: () => page.evaluate(() => window.__S.subsLog.slice()),
    heads: () => page.evaluate(() => Object.keys(window.__S.headsSeen)),
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
        if (t.space === 'street' && !opt.straight && hyp(t.x, t.z, x, z) > 14 && !LEDGER.map.clear(t.x, t.z, x, z)) {
          const a = M.nearNode(t.x, t.z), b = M.nearNode(x, z);
          pts = M.path(a, b).map((i) => [M.NODES[i].x, M.NODES[i].z]).concat([[x, z]]);
          while (pts.length > 1 && hyp(t.x, t.z, pts[1][0], pts[1][1]) < hyp(pts[0][0], pts[0][1], pts[1][0], pts[1][1])) pts.shift(); // never walk back to a first node behind him
        }
        let stuck = 0, lx = t.x, lz = t.z, side = 0, sideT = 0, tries = 0;
        const angd = (a, b) => { let d = b - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return d; };
        const done = await S.run(max, () => hyp(t.x, t.z, x, z) <= near || (opt.until && (0, eval)('(' + opt.until + ')')()), () => {
          while (pts.length > 1 && hyp(t.x, t.z, pts[0][0], pts[0][1]) < 2.2) pts.shift();
          const p = pts[0], want = Math.atan2(p[0] - t.x, p[1] - t.z);
          const off = angd(LEDGER.cam.yaw, want);
          // the mouse turns the view at most about 200 degrees a second
          const sens = 0.0028 * (G.settings.sens || 1), step = Math.max(-0.058, Math.min(0.058, off));
          if (Math.abs(off) > 0.01) S.look(-step / sens);
          if (Math.abs(off) < 0.9) S.kd('KeyW'); else S.ku('KeyW');
          if (opt.run) S.kd('ShiftLeft');
          if (opt.slow) S.kd('KeyZ');
          // held against something: step round it, as a player does
          // (first one way for a second and a half; if that did not free him, the other way for longer)
          if (S.frameNo % 30 === 0) { const d = hyp(t.x, t.z, lx, lz); stuck = d < 0.25 ? stuck + 1 : 0; lx = t.x; lz = t.z; if (stuck >= 2 && !sideT) { side = side > 0 ? -1 : 1; tries++; sideT = 60 + 45 * tries; stuck = 0; } }
          if (sideT > 0) { sideT--; S.kd(side > 0 ? 'KeyD' : 'KeyA'); S.ku('KeyW'); if (!sideT) { S.ku('KeyD'); S.ku('KeyA'); } }
        });
        S.ku('KeyW'); S.ku('ShiftLeft'); S.ku('KeyZ'); S.ku('KeyA'); S.ku('KeyD'); S.lookEnd();
        return done;
      }, { x, z, opt: Object.assign({}, opt, { until: opt.until ? opt.until.toString() : null }) });
      await P.frames(2);
      return r < 0 ? -1 : r / FPS;
    },
    // turn the view (mouse) to face a point
    async face(x, z) {
      await page.evaluate(async ({ x, z }) => {
        const S = window.__S, t = LEDGER.G.tom;
        const angd = (a, b) => { let d = b - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return d; };
        await S.run(120, () => Math.abs(angd(LEDGER.cam.yaw, Math.atan2(x - t.x, z - t.z))) < 0.02, () => { const off = angd(LEDGER.cam.yaw, Math.atan2(x - t.x, z - t.z)); S.look(-Math.max(-0.058, Math.min(0.058, off)) / (0.0028 * (LEDGER.G.settings.sens || 1))); });
        S.lookEnd();
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
    close: async () => { await browser.close(); srv.close(); },
  };
  return P;
}

// A story: play(P, t) is run twice from the same start; both runs must meet the same things (rule 6).
// t.ok(cond, what, got) marks one "must happen"; t.note(what, value) adds to the record that both runs must share.
export async function run(id, o, play) {
  const digests = [], fails = [];
  const runs = process.env.LEDGER_STORY_ONCE ? 1 : 2;
  for (let n = 1; n <= runs; n++) {
    const P = await open(Object.assign({}, o, { port: (o.port || 8950) + n }));
    const t = {
      ok(cond, what, got) {
        if (cond) { if (n === 1) console.log('ok   ' + what); } else { fails.push(what); console.log('TEST FAIL run ' + n + ': ' + what + (got !== undefined ? ' | got ' + JSON.stringify(got).slice(0, 600) : '')); }
        return !!cond;
      },
      note: (what, v) => P.note(what, v),
    };
    try {
      await play(P, t, n);
    } catch (e) {
      fails.push('threw');
      console.log('TEST FAIL run ' + n + ': the story stopped: ' + String((e && e.stack) || e).slice(0, 900));
    }
    const faults = await P.page.evaluate(() => (window.LEDGER && LEDGER.game ? LEDGER.game.faults.slice(0, 5) : ['no game'])).catch(() => ['page gone']);
    t.ok(!faults.length, 'no fault inside any system', faults);
    t.ok(!P.errors.length, 'no page error', P.errors.slice(0, 3));
    digests.push(P.digest());
    if (process.env.LEDGER_STORY_REC) fs.writeFileSync(path.join(SAVES, id + '.run' + n + '.rec.json'), JSON.stringify(P.rec, null, 1));
    await P.close();
  }
  if (runs === 2) {
    if (digests[0] === digests[1]) console.log('ok   the same keys gave the same result twice (' + digests[0] + ')');
    else { fails.push('twice'); console.log('TEST FAIL the two runs differ: ' + digests.join(' and ')); }
  }
  console.log(fails.length ? 'FAIL ' + id + ' (' + fails.length + ')' : 'PASS ' + id);
  process.exit(fails.length ? 1 : 0);
}
