// The lane's round 6 (19 Nov 2026), "The gate": can a build be proved safe before the player touches it?
// One check for each thing the publish gate found, on the built page, with real key events and the game stepped by
// hand at 1/60 s. Each check asserts the experience rule's own words and numbers (DESIGN sections 5, 17 and 19):
//   steering eased on keys (ER-DRIVE-02) · lamp posts and parked cars solid · a crash and a run-down told in words
//   at once (ER-CORE-02) · a touch under 10 mph forgiven (ER-DRIVE-08) · a car hurts and never kills ·
//   never stranded (ER-DRIVE-01, ER-CORE-01) · out of the cab onto clear ground (ER-DRIVE-07) ·
//   the camera never behind a wall indoors (ER-CAM-01) · a pad walks, drives and uses (ER-INPUT-03) ·
//   the prompt names the person ahead (ER-INPUT-02) · walking eased, an early press counts (ER-INPUT-01) ·
//   Continue never leaves him stuck (ER-SAVE-02) · typing never moves Tom and the clock stops in talk (ER-TALK-05)
import { launch } from './harness.mjs';
import { RULES } from '../src/rules.js';
import { AT_ONCE } from '../src/talk_lines.js';

let bad = 0;
const ok = (cond, what) => {
  console.log((cond ? 'ok   ' : 'FAIL ') + what);
  if (!cond) bad++;
};
const D = RULES.driving,
  TOM = RULES.tom,
  MPH = 2.237;
const rx = (line) => new RegExp(line.replace(/[.*+?^$()|[\]\\]/g, '\\$&').replace(/\{\w+\}/g, '.+?'));
const CRASH = Object.values(AT_ONCE.crash).map(rx),
  KNOCKED = Object.values(AT_ONCE.knocked).map(rx);
const said = (lines, pats) => lines.find((l) => pats.some((p) => p.test(l))) || null;

// a pretend pad, in the page before its own code runs
const PAD = () => {
  const pad = { id: 'Test pad (standard)', index: 0, connected: true, mapping: 'standard', timestamp: 0, axes: [0, 0, 0, 0], buttons: Array.from({ length: 17 }, () => ({ pressed: false, touched: false, value: 0 })) };
  window.__pad = pad;
  navigator.getGamepads = () => [pad, null, null, null];
};
const h = await launch({ port: 8806, quality: 'low', before: PAD });
const L = (fn, ...a) => h.ev(fn, ...a);

// the test's own hands in the page: keys as the keyboard sends them, the game stepped at 1/60 s
const HANDS = () => {
  const dt = 1 / 60;
  window.__h = {
    dt,
    down: (c) => dispatchEvent(new KeyboardEvent('keydown', { code: c })),
    up: (c) => dispatchEvent(new KeyboardEvent('keyup', { code: c })),
    subs: () => LEDGER.ui.subs.map((s) => (s.el.textContent || '').trim()),
    // the subtitles put up since `mark` (a line said twice is two lines; the page's own frames are not running here)
    mark: () => new Set(LEDGER.ui.subs),
    since: (mark) => LEDGER.ui.subs.filter((s) => !mark.has(s)).map((s) => (s.el.textContent || '').trim()),
    people: () => LEDGER.G.named.concat(LEDGER.G.crowd).filter((p) => !p.gone && !p.dead && p.space === 'street' && !p.inCar),
    // nobody standing within `m` metres of the straight line between two spots
    quiet(ax, az, bx, bz, m) {
      const dx = bx - ax, dz = bz - az, L2 = dx * dx + dz * dz || 1;
      return this.people().every((p) => { const k = Math.max(0, Math.min(1, ((p.x - ax) * dx + (p.z - az) * dz) / L2)); return Math.hypot(p.x - ax - dx * k, p.z - az - dz * k) > m; });
    },
    // a stretch of open ground running east: [x, z], clear `len` metres ahead and `wide` either side, nobody near
    open(len, wide, m = 8) {
      for (let z = 46; z <= 56; z += 1) for (let x = -110; x <= 140; x += 3) {
        let free = true;
        for (let d = -3; d <= len && free; d += 0.5) for (let w = -wide; w <= wide && free; w += 0.45) if (!LEDGER.isClearOnFoot(x + d, z + w)) free = false;
        if (free && this.quiet(x - 3, z, x + len, z, m)) return [x, z];
      }
      return null;
    },
    busy: () => !!(LEDGER.G.paused || LEDGER.ui.modal),
    clear: (x, z) => LEDGER.isClearOnFoot(x, z),
    // a straight run-up to a spot: [x, z, heading, metres], clear of everything but the target (null: none)
    runUp(tx, tz, want, stop) {
      const b = (x, z) => !LEDGER.isClearOnFoot(x, z);
      let best = null;
      for (let k = 0; k < 24; k++) {
        const a = (k * Math.PI) / 12, sx = Math.sin(a), sz = Math.cos(a);
        let d = stop;
        for (; d <= want + 1.6; d += 0.5) {
          const px = tx - sx * d, pz = tz - sz * d;
          if (b(px, pz) || b(px + sz * 0.9, pz - sx * 0.9) || b(px - sz * 0.9, pz + sx * 0.9)) break;
        }
        d -= 2.1;
        if (d >= 7 && this.quiet(tx - sx * d, tz - sz * d, tx, tz, 9) && (!best || Math.abs(d - want) < Math.abs(best[3] - want))) best = [tx - sx * d, tz - sz * d, a, d];
      }
      return best;
    },
    // put Tom in the cab at a spot (test setup)
    cabAt(x, z, a, v = 0) {
      const G = LEDGER.G, c = G.car;
      LEDGER.goOutside();
      c.keys = true; G.tom.inCar = true; c.x = x; c.z = z; c.ang = a; c.v = v;
      G.tom.x = x; G.tom.z = z;
    },
    // drive at a spot at a held speed until something stops the cab; then let go and watch the words
    crash(tx, tz, v, keep) {
      const G = LEDGER.G, c = G.car, before = this.mark();
      if (!keep) c.dmg = 0;
      const d0 = c.dmg, e0 = G.events.length;
      let t = 0, closest = 1e9, hit = null;
      this.down('KeyW');
      while (t < 8) {
        if (this.busy()) { this.up('KeyW'); return { interrupted: LEDGER.ui.modal || 'paused' }; }
        c.v = v; LEDGER.tick(dt); t += dt;
        closest = Math.min(closest, Math.hypot(c.x - tx, c.z - tz));
        if (c.dmg > d0 || c.v < v - 2) { hit = t; break; }
      }
      this.up('KeyW');
      return { hit, closest, dmg: c.dmg - d0, lines: this.since(before), kinds: G.events.slice(e0).map((e) => e.kind), v: c.v };
    },
    // hold a key and say how long until the cab (or Tom) has moved this far
    freeIn(key, metres, secs = 5) {
      const G = LEDGER.G, c = G.car, tm = G.tom, at = () => (tm.inCar ? [c.x, c.z] : [tm.x, tm.z]), [x0, z0] = at();
      let t = 0, free = null;
      this.down(key);
      while (t < secs) {
        LEDGER.tick(dt); t += dt;
        const [x, z] = at();
        if (Math.hypot(x - x0, z - z0) >= metres) { free = t; break; }
      }
      this.up(key);
      return free;
    },
  };
};
// finish any written scene or talk that started by itself, so a check starts in free play
const freePlay = async () => {
  for (let i = 0; i < 40; i++) {
    const s = await L(async () => {
      const w = LEDGER.written.read();
      if (w.open) { if (w.choices && w.choices.length) await LEDGER.written.choose(0); else await LEDGER.written.next(); return 'scene'; }
      if (LEDGER.ui.modal === 'talk') { await LEDGER.talk.leave(); return 'talk'; }
      if (LEDGER.ui.modal) { LEDGER.press('Escape'); return 'box'; }
      if (LEDGER.G.paused) { LEDGER.tick(0.2); return LEDGER.G.paused ? 'paused' : null; }
      return null;
    });
    if (!s) return;
    await L(() => { for (let k = 0; k < 12; k++) LEDGER.tick(1 / 60); });
  }
};
// run a check; if a scene opened in the middle of it, finish the scene and try again
const tryIt = async (fn, ...a) => {
  let r = null;
  for (let i = 0; i < 5; i++) {
    await freePlay();
    r = await L(fn, ...a);
    if (!r || !r.interrupted) return r;
  }
  return r;
};

try {
  await h.newWeek();
  await L(() => { window.LEDGER_MANUAL = true; LEDGER.G.paused = false; });
  await L(HANDS);
  await freePlay();
  const things = await L(() => LEDGER.streetThings());
  const posts = things.lampPosts, parked = things.cars.filter((c) => c.parked);
  ok(posts.length >= 20 && parked.length >= 5, `the street has ${posts.length} lamp posts and ${parked.length} parked cars`);

  // ---------- 1. steering on keys is eased (ER-DRIVE-02) ----------
  {
    const r = await tryIt(() => {
      const H = __h, c = LEDGER.G.car, V = 9;
      const at = H.open(8, 4);
      if (!at) return { none: true };
      const X = at[0] + 4, Z = at[1];
      H.cabAt(X, Z, Math.PI / 2, V);
      // the speed is held and the cab is kept on its spot, so the turn rate shows the steering and nothing else
      const series = (secs) => { const out = []; let t = 0; while (t < secs - 1e-9) { if (H.busy()) return null; c.v = V; c.x = X; c.z = Z; const a0 = c.ang; LEDGER.tick(H.dt); t += H.dt; out.push([-(c.ang - a0) / H.dt, LEDGER.cabFeel().steerMinusOneToOne]); } return out; };
      const base = series(0.2);
      H.down('KeyD'); const press = series(0.6); H.up('KeyD');
      const release = series(1.0);
      c.ang = Math.PI / 2;
      H.down('KeyA'); const heldA = series(0.6); H.up('KeyA'); H.down('KeyD'); const sw = series(0.9); H.up('KeyD');
      if (!base || !press || !release || !heldA || !sw) return { interrupted: 'a box' };
      return { base, press, release, heldA, sw };
    });
    if (!r || r.none || r.interrupted) ok(false, 'steering: no clear line to drive along, or a box kept opening: not reached');
    else {
      const dt = 1 / 60, full = r.press[r.press.length - 1][0];
      const rise = (s, from, to) => { const sh = s.map((x) => (x[0] - from) / (to - from)); const i10 = sh.findIndex((v) => v >= 0.1), i90 = sh.findIndex((v) => v >= 0.9); const steps = sh.map((v, i) => Math.abs(v - (i ? sh[i - 1] : 0))); return { rise: (i90 - i10) * dt, step: Math.max(...steps), i90 }; };
      const lockAt = (r.press.findIndex((x) => x[1] >= 0.999) + 1) * dt, centreAt = (r.release.findIndex((x) => Math.abs(x[1]) <= 0.001) + 1) * dt;
      const p = rise(r.press, 0, full), rel = rise(r.release, full, 0), s = rise(r.sw, -full, full);
      ok(full > 1, `at 9 m/s full lock turns the cab ${full.toFixed(2)} rad/s`);
      ok(lockAt >= 0.2 - 1e-6 && lockAt <= 0.35 + 1e-6, `D pressed: the steering eases to full lock in ${lockAt.toFixed(3)} s (rule: 0.2 to 0.35 s)`);
      ok(p.rise >= 0.1 && p.step <= 0.2, `... the turn builds over ${p.rise.toFixed(3)} s from 10% to 90%, no frame moves it more than ${(p.step * 100).toFixed(0)}% (gate: at least 0.1 s, at most 20%)`);
      ok(centreAt >= 0.4 - 1e-6 && centreAt <= 0.9 + 1e-6, `D let go: it centres itself in ${centreAt.toFixed(3)} s (rule: 0.4 to 0.9 s)`);
      ok(rel.rise >= 0.1 && rel.step <= 0.2, `... the turn falls away over ${rel.rise.toFixed(3)} s, biggest frame step ${(rel.step * 100).toFixed(0)}%`);
      ok(s.rise >= 0.1 && s.step <= 0.2, `A to D in one frame: the swing takes ${s.rise.toFixed(3)} s from 10% to 90%, biggest frame step ${(s.step * 100).toFixed(0)}%`);
      ok(Math.abs(r.base[r.base.length - 1][0]) < 1e-9, 'no key: the cab runs straight');
    }
  }

  // ---------- 2. lamp posts are solid for the cab; a crash is told in words at once; it always backs out ----------
  const crashAt = async (label, tx, tz, r0, speeds, word) => {
    const got = [];
    for (const v of speeds) {
      const r = await tryIt(([tx, tz, r0, v, cool]) => {
        const H = __h, c = LEDGER.G.car;
        // let the last crash's count run out first, somewhere out of the way, then find the run-up as things stand now
        H.cabAt(-120, 100, 0, 0);
        for (let i = 0; i < Math.ceil((cool + 0.4) * 60); i++) { if (H.busy()) return { interrupted: 1 }; c.v = 0; c.x = -120; c.z = 100; LEDGER.tick(H.dt); }
        const ap = H.runUp(tx, tz, 14, r0 + 2.6);
        if (!ap) return { none: true };
        H.cabAt(ap[0], ap[1], ap[2], v);
        const out = H.crash(tx, tz, v);
        if (out.interrupted) return out;
        out.free = H.freeIn('KeyS', 1, 5); out.clear = LEDGER.cabFeel().standsClear;
        return out;
      }, [tx, tz, r0, v, D.crashCountedEveryRealSeconds]);
      // no clear run-up now, or somebody walked into it: this one is not judged; another target is tried
      if (!r || r.none || r.interrupted || r.hit === null || r.closest > r0 + 3.4 || r.kinds.includes('knocked')) return false;
      got.push([v, r]);
    }
    for (const [v, r] of got) {
      const mph = (v * MPH).toFixed(0);
      ok(r.closest > Math.max(0.5, r0), `${label} at ${mph} mph: it stops the cab (the cab's middle came no nearer than ${r.closest.toFixed(2)} m)`);
      if (v < D.crashAboveMetresPerSecond) ok(r.dmg === 0 && !said(r.lines, CRASH) && !r.kinds.includes('crash'), `... a touch under 10 mph is forgiven: no damage, no word, nothing for the town to tell (ER-DRIVE-08)`);
      else {
        const line = said(r.lines, CRASH);
        ok(r.dmg === 1 && !!line && (!word || line.includes(word)), `... told in words the same frame, naming it: "${line}"`);
      }
      ok(r.free !== null && r.free <= 5 && r.clear, `... and it backs out: 1 m clear ${r.free === null ? 'never' : 'in ' + r.free.toFixed(2) + ' s'} of holding S (rule: within 5 s)`);
    }
    return true;
  };
  {
    let n = 0;
    for (const p of posts.slice().reverse()) { if (n >= 2) break; if (await crashAt(`a lamp post at (${p.xMetres}, ${p.zMetres})`, p.xMetres, p.zMetres, p.radiusMetres, n ? [9, 14.3] : [4.4, 9, 14.3], 'a lamp post')) n++; }
    ok(n === 2, 'two lamp posts had a clear run-up for the cab (10, 20 and 32 mph, the cab\'s top speed; 35 and 50 mph cannot be reached in this cab)');
    let m = 0;
    for (const c of parked) { if (m >= 1) break; if (await crashAt(`a parked car at (${c.xMetres}, ${c.zMetres})`, c.xMetres, c.zMetres, 1.5, [9], 'a parked car')) m++; }
    ok(m === 1, 'a parked car had a clear run-up for the cab');
  }
  // a wall, and the whole run of damage: each crash says what it has done to the car, and the car is slower for it
  {
    const r = await tryIt(([top, share, cool]) => {
      const H = __h, c = LEDGER.G.car;
      let line = null;
      for (let x = -110; x <= 140 && !line; x += 3) for (let z = -200; z <= 60 && !line; z += 3) for (let k = 0; k < 4 && !line; k++) {
        const a = (k * Math.PI) / 2; let d = 0, free = H.clear(x, z);
        for (; free && d < 30; d += 0.5) { const px = x + Math.sin(a) * (d + 2.4), pz = z + Math.cos(a) * (d + 2.4); if (LEDGER.isBlocked(px, pz)) break; if (!H.clear(px, pz) || !H.clear(px + Math.cos(a) * 0.9, pz - Math.sin(a) * 0.9) || !H.clear(px - Math.cos(a) * 0.9, pz + Math.sin(a) * 0.9)) free = false; }
        if (free && d >= 12 && d <= 28 && Math.abs(x + Math.sin(a) * (d + 2.4)) < 100 && z + Math.cos(a) * (d + 2.4) > -200 && z + Math.cos(a) * (d + 2.4) < 40 && H.quiet(x, z, x + Math.sin(a) * d, z + Math.cos(a) * d, 6) && H.clear(x - Math.sin(a) * 3, z - Math.cos(a) * 3)) line = [x, z, a, d];
      }
      if (!line) return { none: true };
      const out = [];
      c.dmg = 0;
      for (let i = 0; i < 6; i++) {
        H.cabAt(line[0], line[1], line[2], 0);
        for (let k = 0; k < Math.ceil((cool + 0.5) * 60); k++) { if (H.busy()) return { interrupted: 1 }; c.v = 0; LEDGER.tick(H.dt); }
        H.cabAt(line[0], line[1], line[2], 9);
        const r = H.crash(line[0] + Math.sin(line[2]) * 40, line[1] + Math.cos(line[2]) * 40, 9, true);
        if (r.interrupted) return r;
        // the top speed now: hold W on a long reverse-free run is not needed, the rule is read from the car itself
        r.dmgNow = c.dmg; r.free = H.freeIn('KeyS', 1, 5); out.push(r);
      }
      return { out, line };
    }, [D.topMetresPerSecond, D.damageSlowsByShare, D.crashCountedEveryRealSeconds]);
    if (!r || r.none || r.interrupted) ok(false, 'a wall: no clear run at a wall found, or a box kept opening: not reached');
    else {
      const keys = ['dent1', 'dent2', 'dent3', 'dent4', 'again', 'again'];
      const mine = r.out.map((x) => said(x.lines, CRASH));
      const each = r.out.map((x, i) => !!mine[i] && rx(AT_ONCE.crash[keys[i]]).test(mine[i]) && !mine[i].includes('something'));
      ok(each.every(Boolean), `six crashes into the same thing: each is told at once, names it and says what it did to the car (${mine.join(' | ')})`);
      ok(r.out.map((x) => x.dmgNow).join() === '1,2,3,4,4,4', `damage goes 1, 2, 3, 4 and stays at ${D.damageAtMost}: the cab always drives on (each point takes ${D.damageSlowsByShare * 100}% off its top speed, and the line says slower)`);
      ok(r.out.every((x) => x.free !== null && x.free <= 5), `after every one of them it backs out within 5 s (${r.out.map((x) => (x.free === null ? 'never' : x.free.toFixed(2))).join(', ')} s)`);
    }
  }

  // ---------- 3. never stranded: wedged on a post, boxed in, swung at a wall; out of the cab onto clear ground ----------
  {
    const p = posts[0];
    for (const keys of [['KeyS', 'KeyW'], ['KeyW', 'KeyS']]) {
      const r = await tryIt(([posts, keys]) => {
        const H = __h, c = LEDGER.G.car;
        let p = null, ap = null;
        for (const q of posts) { ap = H.runUp(q.xMetres, q.zMetres, 10, 3); if (ap) { p = q; break; } }
        if (!ap) return { none: true };
        // as an old save might leave it: the post inside the cab's own body, beside its middle
        H.cabAt(p.xMetres + Math.cos(ap[2]) * 0.5, p.zMetres - Math.sin(ap[2]) * 0.5, ap[2], 0);
        c.dmg = 0;
        const before = H.mark(), wedged = !LEDGER.cabFeel().standsClear, x0 = c.x, z0 = c.z;
        let t = 0, free = null;
        for (const key of keys) { H.down(key); for (let i = 0; i < 150 && free === null; i++) { LEDGER.tick(H.dt); t += H.dt; if (Math.hypot(c.x - x0, c.z - z0) >= 1) free = t; } H.up(key); }
        for (const key of keys) { H.down(key); for (let i = 0; i < 240 && !LEDGER.cabFeel().standsClear; i++) LEDGER.tick(H.dt); H.up(key); }
        return { wedged, free, clear: LEDGER.cabFeel().standsClear, dmg: c.dmg, lines: H.since(before) };
      }, [posts, keys]);
      const names = keys.map((k) => k.slice(3)).join(' then ');
      if (!r || r.none || r.interrupted) { ok(false, 'wedged on a post: no lamp post with a clear run-up: not reached'); continue; }
      ok(r.wedged && r.free !== null && r.free <= 5 && r.clear && r.dmg === 0 && r.lines.includes(AT_ONCE.jam.wedged), `a cab with a lamp post in its own body, ${names} held in turn: it crawls out the clear way (1 m in ${r.free !== null ? r.free.toFixed(2) : 'never'} s), is told ("${AT_ONCE.jam.wedged}") and takes no damage`);
    }
    // boxed in: the cab deep inside a building, no way out along its own line
    const b = await tryIt(() => {
      const H = __h, c = LEDGER.G.car;
      let spot = null;
      for (let x = -100; x <= 140 && !spot; x += 2) for (let z = -200; z <= 40 && !spot; z += 2) {
        let deep = LEDGER.isBlocked(x, z);
        for (let dx = -11; dx <= 11 && deep; dx += 1) for (let dz = -11; dz <= 11 && deep; dz += 1) if (!LEDGER.isBlocked(x + dx, z + dz)) deep = false;
        if (deep) spot = [x, z];
      }
      if (!spot) return { none: true };
      H.cabAt(spot[0], spot[1], 0, 0);
      const before = H.mark();
      let t = 0; H.down('KeyW');
      while (t < 5 && !LEDGER.cabFeel().standsClear) { LEDGER.tick(H.dt); t += H.dt; }
      H.up('KeyW');
      const clear = LEDGER.cabFeel().standsClear, lines = H.since(before);
      const free = H.freeIn('KeyW', 1, 5) ?? H.freeIn('KeyS', 1, 5);
      const moved = Math.hypot(c.x - spot[0], c.z - spot[1]);
      // and out of the cab from inside a building: F puts him on clear ground
      H.cabAt(spot[0], spot[1], 0, 0);
      const e = LEDGER.cabExitPoint();
      LEDGER.press('F');
      const tm = LEDGER.G.tom, out = !tm.inCar && H.clear(tm.x, tm.z);
      const walk = out ? H.freeIn('KeyW', 0.5, 5) ?? H.freeIn('KeyS', 0.5, 5) ?? H.freeIn('KeyA', 0.5, 5) ?? H.freeIn('KeyD', 0.5, 5) : null;
      return { t, clear, lines, free, moved, exit: e, out, walk };
    });
    if (!b || b.none) ok(false, 'boxed in: nowhere solid for 11 m all round was found: not reached');
    else {
      ok(b.clear && b.t <= 5 && b.lines.includes(AT_ONCE.jam.clear), `a cab with no way out along its own line (put 11 m deep in something solid), W held: worked clear onto open ground in ${b.t.toFixed(2)} s and told ("${AT_ONCE.jam.clear}")`);
      ok(b.free !== null && b.free <= 5, `... and it drives on from there (1 m in ${b.free === null ? 'never' : b.free.toFixed(2) + ' s'})`);
      ok(b.out && b.walk !== null && b.walk <= 5, `F with every door against a wall: Tom is put on clear ground and walks away (0.5 m in ${b.walk === null ? 'never' : b.walk.toFixed(2) + ' s'}; ER-DRIVE-07: a blocked door never traps him)`);
    }
    // A clumsy minute: full throttle and the wheel thrown about among walls, posts and parked cars; when the cab
    // has got nowhere for a second and a half the driver backs up, as anyone would. The cab never puts its own body
    // into a wall, a post or a parked car, and it is never 5 s without moving a metre.
    const m = await tryIt(() => {
      const H = __h, c = LEDGER.G.car, tm = LEDGER.G.tom;
      H.cabAt(4.1, 20, 0, 0); c.dmg = 0;
      let seed = 12345; const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
      let t = 0, inSolid = 0, dist = 0, lx = c.x, lz = c.z, th = 'KeyW', st = null, next = 0, first = null, esc = null, stops = 0, worst = 0, never = 0; const e0 = LEDGER.G.events.length, W = [];
      H.down(th);
      const set = (k) => { if (k !== th) { H.up(th); th = k; H.down(th); } };
      while (t < 60) {
        if (H.busy()) { H.up(th); if (st) H.up(st); return { interrupted: 1 }; }
        if (t >= next) { if (st) H.up(st); const q = rnd(); st = q < 0.4 ? 'KeyA' : q < 0.8 ? 'KeyD' : null; if (st) H.down(st); next = t + 0.3 + rnd() * 1.2; }
        const recent = W.filter((p) => p[0] >= t - 1.5);
        if (esc) {
          // the rule's own way out: S for 2.5 s, then W for 2.5 s; free when the cab is a metre from where it stopped
          const gone = Math.hypot(c.x - esc.x, c.z - esc.z);
          if (gone >= 1) { worst = Math.max(worst, t - esc.t); esc = null; set('KeyW'); W.length = 0; }
          else if (t - esc.t > 5) { never++; esc = null; set('KeyW'); W.length = 0; }
          else set(t - esc.t < 2.5 ? 'KeyS' : 'KeyW');
        } else if (t > 1.5 && recent.length > 60 && Math.max(...recent.map((p) => Math.hypot(p[1] - c.x, p[2] - c.z))) < 0.5) { esc = { t, x: c.x, z: c.z }; stops++; set('KeyS'); }
        LEDGER.tick(H.dt); t += H.dt;
        if (!LEDGER.cabFeel().standsClearOfFixedThings) { inSolid++; if (!first) first = [+t.toFixed(2), +c.x.toFixed(1), +c.z.toFixed(1)]; }
        dist += Math.hypot(c.x - lx, c.z - lz); lx = c.x; lz = c.z;
        W.push([t, c.x, c.z]); while (W.length && W[0][0] < t - 5) W.shift();
      }
      H.up(th); if (st) H.up(st);
      return { inSolid, first, stops, worst, never, dist, crashes: LEDGER.G.events.slice(e0).filter((e) => e.kind === 'crash').length, inCar: tm.inCar };
    });
    if (!m || m.interrupted) ok(false, 'the clumsy minute: a box kept opening: not reached');
    else {
      ok(m.inSolid === 0, `a clumsy minute at the wheel (${m.dist.toFixed(0)} m, ${m.crashes} crashes): the cab's body was in a wall, a post or a parked car on ${m.inSolid} frames${m.first ? ' (first at ' + JSON.stringify(m.first) + ')' : ''}`);
      ok(m.never === 0 && m.dist > 30, `... it came to a stop ${m.stops} times and each time S then W had it a metre away within 5 s (slowest ${m.worst.toFixed(2)} s; never: ${m.never})`);
    }
  }

  // ---------- 4. on foot: lamp posts and parked cars are solid, and nothing drawn can trap him ----------
  {
    const r = await tryIt(([posts, parked, rad]) => {
      const H = __h, G = LEDGER.G, t = G.tom, out = [];
      LEDGER.goOutside(); if (t.inCar) { G.car.v = 0; LEDGER.cab.getOut(); }
      G.car.x = -120; G.car.z = 100; // the cab out of the way (test setup)
      const walkAt = (px, pz, pr, kind) => {
        for (let k = 0; k < 16; k++) {
          const a = (k * Math.PI) / 8, sx = Math.sin(a), sz = Math.cos(a), st = pr + 2.5;
          let free = true;
          for (let d = pr + 0.6; d <= st; d += 0.25) if (!H.clear(px - sx * d, pz - sz * d)) { free = false; break; }
          if (!free) continue;
          t.x = px - sx * st; t.z = pz - sz * st; t.v = 0; LEDGER.cam.yaw = a;
          let s = 0, closest = 1e9; H.down('KeyW');
          while (s < 2.5) { if (H.busy()) { H.up('KeyW'); return { interrupted: 1 }; } LEDGER.tick(H.dt); s += H.dt; closest = Math.min(closest, Math.hypot(t.x - px, t.z - pz)); }
          H.up('KeyW');
          return { kind, closest, walked: closest < st - 0.5 };
        }
        return null;
      };
      for (const p of posts) { const r = walkAt(p.xMetres, p.zMetres, p.radiusMetres, 'post'); if (r && r.interrupted) return r; if (r) out.push(r); }
      for (const c of parked) { const r = walkAt(c.xMetres, c.zMetres, 1.5, 'car'); if (r && r.interrupted) return r; if (r) out.push(r); }
      // inside a parked car (as if it had been put down on him): every way he can walk leads out
      const c = parked[0]; const esc = [];
      for (const key of ['KeyW', 'KeyS', 'KeyA', 'KeyD']) { t.x = c.xMetres + 0.2; t.z = c.zMetres + 0.1; LEDGER.cam.yaw = 0.3; esc.push(H.freeIn(key, 1.6, 5)); }
      const clearAfter = H.clear(t.x, t.z);
      return { out, esc, clearAfter };
    }, [posts, parked, TOM.bodyRadiusMetres]);
    if (!r || r.interrupted) ok(false, 'on foot: a box kept opening: not reached');
    else {
      const p = r.out.filter((x) => x.kind === 'post'), c = r.out.filter((x) => x.kind === 'car');
      ok(p.length >= 20 && p.every((x) => x.walked && x.closest >= D.lampPostRadiusMetres + TOM.bodyRadiusMetres - 0.02), `Tom walked at ${p.length} lamp posts and none let him through (nearest he came to a post's middle: ${Math.min(...p.map((x) => x.closest)).toFixed(2)} m)`);
      ok(c.length >= 5 && c.every((x) => x.walked && x.closest >= 0.85), `Tom walked at ${c.length} parked cars and none let him through (nearest to a car's middle: ${Math.min(...c.map((x) => x.closest)).toFixed(2)} m)`);
      ok(r.esc.every((x) => x !== null && x <= 5), `put inside a parked car, he walks out by W, S, A or D (${r.esc.map((x) => (x === null ? 'never' : x.toFixed(2))).join(', ')} s; never stuck)`);
    }
  }

  // ---------- 5. a person knocked down: told at once, by the name Tom knows, hurt and never killed ----------
  {
    for (const v of [4, 6.7, 13.4]) {
      const r = await tryIt(([v]) => {
        const H = __h, G = LEDGER.G, c = G.car;
        const P = G.named.find((p) => !p.gone && !p.dead && !p.down && p.space === 'street' && !p.inCar);
        const at = H.open(16, 1.2);
        if (!P || !at) return { none: true };
        // test setup: one person stood on open ground and held still, the cab 12 m back at a held speed
        const was = [P.x, P.z];
        P.x = at[0] + 12; P.z = at[1]; P.route = null; P.moving = false;
        H.cabAt(at[0], at[1], Math.PI / 2, v); c.dmg = 0;
        const before = H.mark(), e0 = G.events.length, shown = LEDGER.people().find((q) => q.personId === P.id);
        let t = 0; H.down('KeyW');
        while (t < 6 && !P.down) { if (H.busy()) { H.up('KeyW'); P.x = was[0]; P.z = was[1]; return { interrupted: 1 }; } c.v = v; P.x = at[0] + 12; P.z = at[1]; P.route = null; P.moving = false; LEDGER.tick(H.dt); t += H.dt; }
        H.up('KeyW');
        const lines = H.since(before), others = H.people().filter((q) => q.down && q !== P).length;
        for (let i = 0; i < 90; i++) LEDGER.tick(H.dt);
        const r = { name: P.def.name, shown: shown ? shown.shownAs : null, down: !!P.down, dead: !!P.dead, hurt: P.hurt || 0, lines, others, kinds: G.events.slice(e0).map((e) => e.kind), deaths: Object.keys(G.story.flags.dead || {}).length };
        P.down = false; P.hurt = 0; P.downT = 0; P.goalKey = ''; P.x = was[0]; P.z = was[1]; // put back on their feet for the next check
        return r;
      }, [v]);
      const mph = (v * MPH).toFixed(0);
      if (!r || r.none || r.interrupted) { ok(false, `a person hit at ${mph} mph: no open ground for it, or a box kept opening: not reached`); continue; }
      const line = said(r.lines, KNOCKED), want = v < D.runDownIsAClipBelowMetresPerSecond ? rx(AT_ONCE.knocked.clip) : rx(AT_ONCE.knocked.hard);
      ok(r.down && !!line && want.test(line), `a person hit at ${mph} mph is told on screen the same frame: "${line}"`);
      ok(!r.dead && r.deaths === 0 && r.hurt > 0 && r.hurt <= D.runDownHurtAtMost && Math.abs(r.hurt - Math.min(D.runDownHurtAtMost, v * D.hurtPerMetrePerSecond)) < 0.03, `... hurt ${r.hurt.toFixed(2)} of 1 (it scales with the speed), and alive: a car hurts and never kills`);
      ok(!!r.shown && !!line && line.startsWith(r.shown), `... named as Tom knows them ("${r.shown}"; the name is ${r.name})`);
    }
    // three people standing together, driven through: every one of them is told
    const g = await tryIt(() => {
      const H = __h, G = LEDGER.G, c = G.car;
      const three = G.named.filter((p) => !p.gone && !p.dead && !p.down && p.space === 'street' && !p.inCar).slice(0, 3);
      if (three.length < 3) return { none: true };
      const at = H.open(20, 1.5);
      if (!at) return { none: true };
      const spot = [at[0] + 12, at[1]];
      three.forEach((P, i) => { P.x = spot[0] + i * 0.9; P.z = spot[1] + (i - 1) * 0.5; P.route = null; P.moving = false; P.space = 'street'; });
      H.cabAt(spot[0] - 12, spot[1], Math.PI / 2, 9);
      let t = 0; H.down('KeyW');
      while (t < 4) { if (H.busy()) { H.up('KeyW'); return { interrupted: 1 }; } c.v = Math.max(c.v, 9); for (const P of three) { P.route = null; P.moving = false; } LEDGER.tick(H.dt); t += H.dt; }
      H.up('KeyW');
      const lines = LEDGER.ui.subs.map((s) => s.el.textContent);
      const shown = three.map((P) => LEDGER.people().find((q) => q.personId === P.id).shownAs);
      const r = { down: three.map((P) => !!P.down), dead: three.map((P) => !!P.dead), shown, lines };
      for (const P of three) { P.down = false; P.hurt = 0; P.downT = 0; P.goalKey = ''; }
      return r;
    });
    if (!g || g.none || g.interrupted) ok(false, 'three people driven through: not reached');
    else ok(g.down.every(Boolean) && !g.dead.some(Boolean) && g.shown.every((n) => g.lines.some((l) => l.startsWith(n) && KNOCKED.some((p) => p.test(l)))), `three people standing together, driven through: all three go down, none is killed, and each is named on screen (${g.lines.join(' | ')})`);
  }

  // ---------- 6. the prompt names the person ahead and in view (ER-INPUT-02) ----------
  {
    const r = await tryIt(([held]) => {
      const H = __h, G = LEDGER.G, t = G.tom;
      LEDGER.goOutside(); if (t.inCar) { G.car.v = 0; LEDGER.cab.getOut(); }
      const named = G.named.find((p) => !p.gone && !p.dead && !p.down && p.space === 'street'), anon = G.crowd.find((p) => !p.gone && !p.dead && !p.down && p.space === 'street' && !p.mark);
      if (!named || !anon) return { none: true };
      let spot = null;
      for (let x = -100; x <= 140 && !spot; x += 5) for (let z = 44; z <= 58 && !spot; z += 2) { let free = true; for (let dx = -3; dx <= 3 && free; dx++) for (let dz = -1; dz <= 5 && free; dz++) if (!H.clear(x + dx, z + dz)) free = false; if (free && G.named.concat(G.crowd).every((p) => p === named || p === anon || p.space !== 'street' || Math.hypot(p.x - x, p.z - z) > 8)) spot = [x, z]; }
      if (!spot) return { none: true };
      const hold = (P, x, z) => { P.x = x; P.z = z; P.route = null; P.moving = false; P.ang = Math.atan2(spot[0] - x, spot[1] - z); };
      const put = (x, z, ang) => { t.x = x; t.z = z; t.ang = ang; t.v = 0; };
      const talkTo = () => (LEDGER.prompts().find((p) => p.key === 'E') || {}).text || null;
      // the playtester's fault: a stranger straight ahead at 2.0 m, a named man 1.7 m away and 21 degrees off
      const off = (21 * Math.PI) / 180;
      hold(anon, spot[0], spot[1] + 2.0); hold(named, spot[0] + Math.sin(off) * 1.7, spot[1] + Math.cos(off) * 1.7);
      put(spot[0], spot[1], 0);
      const ahead = talkTo();
      // facing the named man instead: he is the one
      put(spot[0] + 20, spot[1], 0); talkTo(); put(spot[0], spot[1], off);
      const other = talkTo();
      // two people about equally ahead: the first choice is held for a moment, then gives way
      const second = named;
      hold(anon, spot[0] - 0.25, spot[1] + 2.0); hold(second, spot[0] + 0.62, spot[1] + 2.0);
      put(spot[0] + 20, spot[1], 0); talkTo(); put(spot[0], spot[1], 0);
      const first = talkTo(); // anon is nearer the middle: his
      const names = [];
      // Tom turns a little toward the second person, a step at a time, as a mouse would
      t.ang = 0.09; let tt = 0;
      while (tt < 0.5) { for (const P of [anon, second]) { P.route = null; P.moving = false; } hold(anon, spot[0] - 0.25, spot[1] + 2.0); hold(second, spot[0] + 0.62, spot[1] + 2.0); LEDGER.tick(H.dt); tt += H.dt; t.ang = 0.09; t.x = spot[0]; t.z = spot[1]; names.push([+tt.toFixed(3), talkTo()]); }
      const changedAt = (names.find((n) => n[1] !== first) || [null])[0];
      return { ahead, other, first, changedAt, last: names[names.length - 1][1], anonName: LEDGER.G.crowd.indexOf(anon), named: named.def.name };
    }, [RULES.ladder.targetHeldRealSeconds]);
    if (!r || r.none || r.interrupted) ok(false, 'the prompt: no clear ground or people for it: not reached');
    else {
      ok(/^Speak to /.test(r.ahead || ''), `a stranger straight ahead at 2.0 m, a named man 1.7 m away and 21 degrees off: the prompt is "${r.ahead}" (the person ahead, not the nearer one)`);
      ok(/^Talk to /.test(r.other || ''), `Tom turned to face the named man: "${r.other}"`);
      if (!r.none2) ok(r.changedAt !== null && r.changedAt >= RULES.ladder.targetHeldRealSeconds - 0.02 && r.last !== r.first, `two people about equally ahead: the first choice is held ${r.changedAt === null ? 'for ever' : r.changedAt.toFixed(2) + ' s'} before the prompt changes (rule: held 0.2 s, so it does not flicker)`);
    }
  }

  // ---------- 7. on foot: walking is eased and a press a moment early still counts (ER-INPUT-01) ----------
  {
    const r = await tryIt(([reach]) => {
      const H = __h, G = LEDGER.G, t = G.tom;
      LEDGER.goOutside(); if (t.inCar) { G.car.v = 0; LEDGER.cab.getOut(); }
      let spot = null;
      for (let x = -100; x <= 140 && !spot; x += 5) for (let z = 44; z <= 58 && !spot; z += 2) { let free = true; for (let d = -1; d <= 14 && free; d += 0.5) if (!H.clear(x + d, z) ) free = false; if (free && G.named.concat(G.crowd).every((p) => p.space !== 'street' || Math.hypot(p.x - x, p.z - z) > 16)) spot = [x, z]; }
      if (!spot) return { none: true };
      t.x = spot[0]; t.z = spot[1]; t.v = 0; LEDGER.cam.yaw = Math.PI / 2;
      for (let i = 0; i < 30; i++) LEDGER.tick(H.dt);
      const steps = []; let px = t.x;
      H.down('KeyW');
      for (let i = 0; i < 24; i++) { LEDGER.tick(H.dt); steps.push((t.x - px) / H.dt); px = t.x; }
      H.up('KeyW');
      const stop = [];
      for (let i = 0; i < 18; i++) { LEDGER.tick(H.dt); stop.push((t.x - px) / H.dt); px = t.x; }
      // an early press: F one frame before the cab comes into reach
      const c = G.car; c.keys = true; c.x = spot[0] + 11; c.z = spot[1]; c.ang = 0; c.v = 0;
      t.x = c.x - reach - 0.02; t.z = c.z; LEDGER.cam.yaw = Math.PI / 2;
      for (let i = 0; i < 20; i++) LEDGER.tick(H.dt);
      t.x = c.x - reach - 0.02; t.z = c.z;
      const inReach = Math.hypot(t.x - c.x, t.z - c.z) < reach;
      H.down('KeyD'); H.up('KeyD'); // nothing: just to show keys are live
      H.down('KeyW'); H.down('KeyF'); H.up('KeyF');
      const at0 = t.inCar; let got = null;
      for (let i = 0; i < 12 && got === null; i++) { LEDGER.tick(H.dt); if (t.inCar) got = (i + 1) * H.dt; }
      H.up('KeyW');
      if (t.inCar) { c.v = 0; LEDGER.cab.getOut(); }
      return { steps, stop, inReach, at0, got };
    }, [TOM.cabWithinMetres]);
    if (!r || r.none || r.interrupted) ok(false, 'walking: no clear ground for it: not reached');
    else {
      const full = TOM.walkingMetresPerSecond, at = (r.steps.findIndex((v) => v >= full * 0.98) + 1) / 60, stopAt = (r.stop.findIndex((v) => v <= 0.001) + 1) / 60;
      ok(r.steps[0] < full * 0.25 && at > 0.05 && at <= TOM.reachesPaceInRealSeconds + 0.03, `W pressed: his first step is ${(r.steps[0] / full * 100).toFixed(0)}% of his pace and he is at full pace in ${at.toFixed(2)} s (eased, and well inside 100 ms to answer)`);
      ok(r.stop[0] > 0 && r.stop[0] < full && stopAt > 0.03 && stopAt <= TOM.stopsInRealSeconds + 0.03, `W let go: he stops over ${stopAt.toFixed(2)} s, not dead on the frame`);
      ok(!r.inReach && !r.at0 && r.got !== null && r.got <= TOM.earlyPressCountsRealSeconds + 1e-6, `F pressed a moment before the cab is in reach: it is taken ${r.got === null ? 'never' : r.got.toFixed(3) + ' s'} later, when it is (a press 100 ms early still counts)`);
    }
  }

  // ---------- 8. a pad walks, looks, drives and uses (ER-INPUT-03) ----------
  {
    const r = await tryIt(([walk]) => {
      const H = __h, G = LEDGER.G, t = G.tom, c = G.car, pad = window.__pad;
      const rest = () => { pad.axes = [0, 0, 0, 0]; for (const b of pad.buttons) { b.pressed = false; b.value = 0; } LEDGER.padStep(); };
      const tap = (i) => { pad.buttons[i].pressed = true; pad.buttons[i].value = 1; LEDGER.padStep(); pad.buttons[i].pressed = false; pad.buttons[i].value = 0; LEDGER.padStep(); };
      const run = (secs) => { let s = 0; while (s < secs) { LEDGER.padStep(); LEDGER.tick(H.dt); s += H.dt; } };
      LEDGER.goOutside(); if (t.inCar) { c.v = 0; LEDGER.cab.getOut(); }
      let spot = null;
      for (let x = -100; x <= 140 && !spot; x += 5) for (let z = 44; z <= 58 && !spot; z += 2) { let free = true; for (let d = -2; d <= 40 && free; d += 0.5) if (!H.clear(x + d, z) || !H.clear(x + d, z + 1) || !H.clear(x + d, z - 1)) free = false; if (free && G.named.concat(G.crowd).every((p) => p.space !== 'street' || Math.abs(p.z - z) > 3 || p.x < x - 4)) spot = [x, z]; }
      if (!spot) return { none: true };
      rest(); c.x = spot[0] - 60; c.z = spot[1] + 30;
      const carried = t.carry; t.carry = null; // test setup: the suitcase put down (a man carrying cannot run)
      t.x = spot[0]; t.z = spot[1]; LEDGER.cam.yaw = Math.PI / 2; LEDGER.cam.pitch = 0.3;
      const x0 = t.x; pad.axes[1] = -1; run(2); const walked = t.x - x0;
      const x1 = t.x; pad.axes[1] = -0.6; run(1); const half = t.x - x1;
      const x2 = t.x; pad.axes[1] = -1; pad.buttons[7].pressed = true; pad.buttons[7].value = 1; run(1); const ran = t.x - x2;
      rest(); run(0.3); t.carry = carried;
      const yaw0 = LEDGER.cam.yaw; pad.axes[2] = 1; run(0.5); const turned = yaw0 - LEDGER.cam.yaw; rest();
      const keyboardPrompt = document.getElementById('prompt').textContent;
      // the cab by pad: Y gets in, the right trigger drives, the stick steers by as much as it is pushed
      c.keys = true; c.x = spot[0]; c.z = spot[1]; c.ang = Math.PI / 2; c.v = 0; c.dmg = 0; t.x = c.x; t.z = c.z + 1.6; t.v = 0;
      run(0.3); const prompt = document.getElementById('prompt').textContent;
      tap(3); const inCab = t.inCar;
      const cx = c.x; pad.buttons[7].pressed = true; pad.buttons[7].value = 1; run(2.5); const drove = c.x - cx, speed = c.v;
      const turn = (ax) => { c.x = spot[0]; c.z = spot[1]; c.ang = Math.PI / 2; pad.axes[0] = ax; LEDGER.padStep(); c.v = 9; const a0 = c.ang; LEDGER.tick(H.dt); const first = -(c.ang - a0) / H.dt; pad.axes[0] = 0; LEDGER.padStep(); return first; };
      const fullTurn = turn(1), halfTurn = turn(0.59);
      rest(); pad.buttons[6].pressed = true; pad.buttons[6].value = 1; c.v = 6; run(1.2); const braked = c.v; rest();
      c.v = 0; tap(3); const outAgain = !t.inCar;
      // Menu pauses and carries on
      tap(9); const paused = LEDGER.read().boxOpen === 'pause' && LEDGER.read().paused; tap(9); const resumed = !LEDGER.read().boxOpen && !LEDGER.read().paused;
      // A takes a door, as E does
      const door = Object.entries(LEDGER.places).find(([n, p]) => p.kind === 'door' && /Regent/.test(n));
      LEDGER.goTo(door[0]); run(0.3); tap(0); run(0.5); const indoors = LEDGER.read().tom.indoorsRoomId;
      LEDGER.goOutside(); rest();
      // back on the keys, the prompts show the keys again
      t.x = c.x; t.z = c.z + 1.6; H.down('KeyD'); H.up('KeyD'); run(0.3); const keysAgain = document.getElementById('prompt').textContent;
      return { walked, half, ran, turned, prompt, inCab, drove, speed, fullTurn, halfTurn, braked, outAgain, paused, resumed, indoors, keysAgain };
    }, [TOM.walkingMetresPerSecond]);
    if (!r || r.none || r.interrupted) ok(false, 'the pad: no clear ground for it: not reached');
    else {
      ok(r.walked > TOM.walkingMetresPerSecond * 1.7, `left stick full forward for 2 s: Tom walks ${r.walked.toFixed(2)} m`);
      ok(r.half > 0.3 && r.half < TOM.walkingMetresPerSecond * 0.75, `... the stick is analogue: at about half he walks ${r.half.toFixed(2)} m in a second`);
      ok(r.ran > TOM.walkingMetresPerSecond * 1.5, `... with the right trigger held he runs (${r.ran.toFixed(2)} m in a second)`);
      ok(r.turned > 0.8, `right stick: the camera turns (${r.turned.toFixed(2)} rad in half a second)`);
      ok(/Y\s*Get in the cab/.test(r.prompt), `with the pad in hand the prompt names its button: "${r.prompt.trim()}"`);
      ok(r.inCab && r.drove > 5, `Y gets him into the cab and the right trigger drives it (${r.drove.toFixed(1)} m in 2.5 s, ${(r.speed * MPH).toFixed(0)} mph)`);
      ok(r.fullTurn > 1 && Math.abs(r.halfTurn / r.fullTurn - 0.5) < 0.05, `the stick steers by as much as it is pushed, at once (full ${r.fullTurn.toFixed(2)} rad/s, half ${r.halfTurn.toFixed(2)}): the pad is analogue`);
      ok(r.braked < 1, `the left trigger brakes (from 6 m/s to ${r.braked.toFixed(1)} in 1.2 s)`);
      ok(r.outAgain && r.paused && r.resumed, 'Y gets him out again; Menu pauses and carries on');
      ok(r.indoors === 'boarding', `A at a door goes in, as E does (${r.indoors})`);
      ok(/F\s*Get in the cab/.test(r.keysAgain), `a key pressed: the prompts show the keys again ("${r.keysAgain.trim()}")`);
    }
  }

  // ---------- 9. indoors the camera never goes behind a wall (ER-CAM-01) ----------
  {
    await freePlay();
    const r = await L(async () => {
      const T = LEDGER.THREE, out = [];
      const ray = () => { const c = LEDGER.cam, from = new T.Vector3(c.tx, c.ty, c.tz), to = LEDGER.camera.position.clone(), d = from.distanceTo(to); const rc = new T.Raycaster(from, to.clone().sub(from).normalize(), 0, d); const objs = []; LEDGER.scene.traverse((o) => { if ((o.isMesh || o.isInstancedMesh) && !o.isSkinnedMesh && o.visible) objs.push(o); }); const hit = rc.intersectObjects(objs, false).find((x) => x.object.material && !(x.object.material.transparent && x.object.material.opacity < 0.5)); return { dist: d, hit: hit ? hit.distance : null }; };
      const frames = (ms) => new Promise((res) => setTimeout(res, ms));
      for (const room of ['boarding', 'mickeys']) {
        LEDGER.goInside(room);
        const t = LEDGER.G.tom, x0 = t.x, z0 = t.z;
        // find the room's own middle from where the door mat is: walk the room's width with the collision map
        let west = x0, east = x0; while (!LEDGER.isBlocked(west - 0.1, z0) && x0 - west < 20) west -= 0.1; while (!LEDGER.isBlocked(east + 0.1, z0) && east - x0 < 20) east += 0.1;
        const spots = [[west + 0.05, z0], [east - 0.05, z0]];
        // both sides of every partition the room has: where a step sideways is blocked in mid-room
        for (let x = west + 0.6; x < east - 0.6; x += 0.1) for (const dz of [-2, -3.5]) if (!LEDGER.isBlocked(x, z0 + dz) && LEDGER.isBlocked(x + 0.45, z0 + dz) && !LEDGER.isBlocked(x + 1.2, z0 + dz)) { spots.push([x, z0 + dz], [x + 1.2, z0 + dz]); }
        for (const [x, z] of spots) for (const yaw of [Math.PI - 0.7, Math.PI, Math.PI + 0.7]) {
          t.x = x; t.z = z; LEDGER.cam.yaw = yaw; LEDGER.cam.pitch = 0.62; LEDGER.cam.snap = true;
          window.LEDGER_NORENDER = false; await frames(450); const r = ray(); window.LEDGER_NORENDER = true;
          out.push({ room, x: +(x - x0).toFixed(1), z: +(z - z0).toFixed(1), asked: +(yaw - Math.PI).toFixed(2), got: +(LEDGER.cam.yaw - Math.PI).toFixed(2), dist: r.dist, hit: r.hit });
        }
      }
      LEDGER.goOutside();
      return out;
    });
    // at the wheel beside the biggest scrap heap, the camera on the heap's side: it comes in front of the heap
    const y = await L(async () => {
      const T = LEDGER.THREE, G = LEDGER.G, c = G.car, out = [];
      const frames = (ms) => new Promise((res) => setTimeout(res, ms));
      LEDGER.goOutside(); c.keys = true; G.tom.inCar = true; c.v = 0;
      const heap = [-112, 26, 3.2];
      for (let k = 0; k < 8; k++) {
        const a = (k * Math.PI) / 4, x = heap[0] + Math.sin(a) * (heap[2] + 2.9), z = heap[1] + Math.cos(a) * (heap[2] + 2.9);
        if (!LEDGER.isClearOnFoot(x, z)) continue;
        c.x = x; c.z = z; c.ang = a; G.tom.x = x; G.tom.z = z; LEDGER.cam.yaw = a; LEDGER.cam.idle = 0; LEDGER.cam.snap = true;
        if (!LEDGER.cabFeel().standsClear) continue;
        window.LEDGER_NORENDER = false; await frames(450);
        const cm = LEDGER.cam, from = new T.Vector3(cm.tx, cm.ty, cm.tz), to = LEDGER.camera.position.clone(), d = from.distanceTo(to);
        const rc = new T.Raycaster(from, to.clone().sub(from).normalize(), 0, d), objs = [];
        LEDGER.scene.traverse((o) => { if ((o.isMesh || o.isInstancedMesh) && !o.isSkinnedMesh && o.visible) objs.push(o); });
        const hit = rc.intersectObjects(objs, false).find((h) => h.object.material && !(h.object.material.transparent && h.object.material.opacity < 0.5));
        window.LEDGER_NORENDER = true;
        out.push({ k, dist: +d.toFixed(2), hit: hit ? +hit.distance.toFixed(2) : null });
      }
      G.tom.inCar = false; G.tom.x = 4; G.tom.z = 30;
      return out;
    });
    const hid = y.filter((x) => x.hit !== null && x.hit > 2.7 && x.hit < x.dist - 0.3);
    ok(y.length >= 3 && hid.length === 0 && y.some((x) => x.dist < 5), `at the wheel beside the biggest scrap heap, the camera on the heap's side (${y.length} places): it comes in front of the heap, nothing solid between the cab and the camera${hid.length ? ' | hidden: ' + JSON.stringify(hid) : ''}`);
    const blocked = r.filter((x) => x.hit !== null && x.hit > 0.45 && x.hit < x.dist - 0.3);
    ok(r.length >= 12 && blocked.length === 0, `indoors at Regent House and Mickey's, Tom against each side wall and each side of the partition, the camera pushed hard left, straight and hard right (${r.length} views): nothing solid between him and the camera in ${r.length - blocked.length} of them${blocked.length ? ' | hidden: ' + JSON.stringify(blocked.slice(0, 3)) : ''}`);
    ok(r.some((x) => Math.abs(x.asked) > 0.5 && Math.abs(x.got) < Math.abs(x.asked) - 0.1), 'against a wall the camera gives way: it swings back behind him instead of going through the wall');
    ok(r.some((x) => Math.abs(x.asked) > 0.5 && Math.abs(x.got - x.asked) < 0.02), 'in open floor it stays where the player put it');
  }

  // ---------- 10. Continue after a save made at the wheel; typing never moves Tom; Esc pauses in the cab ----------
  {
    await freePlay();
    const r = await L(async () => {
      const H = __h, G = LEDGER.G, t = G.tom, c = G.car;
      H.cabAt(4.1, 20, 0, 0); for (let i = 0; i < 10; i++) LEDGER.tick(H.dt);
      // Esc pauses at the wheel, and again carries on
      H.down('Escape'); H.up('Escape'); const p1 = LEDGER.read(); H.down('Escape'); H.up('Escape'); const p2 = LEDGER.read();
      const text = LEDGER.saveText();
      LEDGER.restore(text);
      await new Promise((res) => setTimeout(res, 300));
      window.LEDGER_MANUAL = true; G.paused = false;
      const t2 = LEDGER.G.tom, c2 = LEDGER.G.car;
      const at = { inCar: t2.inCar, clear: H.clear(t2.x, t2.z), fromCab: Math.hypot(t2.x - c2.x, t2.z - c2.z) };
      const walk = H.freeIn('KeyW', 1, 5) ?? H.freeIn('KeyS', 1, 5);
      return { paused: p1.paused && p1.boxOpen === 'pause', resumed: !p2.paused && !p2.boxOpen, at, walk };
    });
    ok(r.paused && r.resumed, 'Esc pauses at the wheel and Esc carries on (ER-SAVE-02)');
    const twice = await L(() => {
      __h.down('Escape'); __h.up('Escape');
      const b = document.querySelector('#book [data-act="finish"]'), was = b.textContent;
      b.click();
      const r = { was, now: b.textContent, phase: LEDGER.G.story.phase, box: LEDGER.read().boxOpen, ended: LEDGER.read().weekEnded };
      __h.down('Escape'); __h.up('Escape');
      return r;
    });
    ok(twice.box === 'pause' && twice.phase === 'play' && !twice.ended && /^Sure\? Press again/.test(twice.now), `on the pause screen, "${twice.was}" pressed once only asks ("${twice.now}"): nothing that cannot be undone is one press from Carry on`);
    ok(!r.at.inCar && r.at.clear && r.at.fromCab > TOM.cabBodyRadiusMetres && r.at.fromCab < 4 && r.walk !== null && r.walk <= 5, `a week saved at the wheel and continued: Tom stands at the cab's door (${r.at.fromCab.toFixed(2)} m from its middle), on clear ground, and walks off (1 m in ${r.walk === null ? 'never' : r.walk.toFixed(2) + ' s'})`);
    await freePlay();
    const t = await L(async () => {
      const H = __h, G = LEDGER.G, tm = G.tom;
      const P = G.named.find((p) => !p.gone && !p.down && !p.dead && p.space === 'street' && !p.inCar);
      LEDGER.talk.open(P.id, { free: true });
      for (let i = 0; i < 20; i++) LEDGER.tick(H.dt);
      const open = LEDGER.talk.state().open, x0 = tm.x, z0 = tm.z, m0 = G.t, inp = document.getElementById('tin');
      if (inp) inp.focus();
      for (const c of ['KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyF', 'KeyE', 'KeyQ', 'KeyC']) { const e = new KeyboardEvent('keydown', { code: c, bubbles: true }); (inp || window).dispatchEvent(e); for (let i = 0; i < 12; i++) LEDGER.tick(H.dt); (inp || window).dispatchEvent(new KeyboardEvent('keyup', { code: c, bubbles: true })); }
      const r = { open, still: LEDGER.talk.state().open, moved: Math.hypot(tm.x - x0, tm.z - z0), minutes: G.t - m0, inCar: tm.inCar, fight: !!LEDGER.F.on };
      await LEDGER.talk.leave();
      return r;
    });
    ok(t.open && t.still && t.moved === 0 && t.minutes === 0 && !t.inCar && !t.fight, `in a talk, W A S D F E Q C typed into the box: Tom moved ${t.moved.toFixed(2)} m and the clock moved ${t.minutes.toFixed(2)} minutes (ER-TALK-05)`);
  }
  ok(h.errors.length === 0, 'no page errors' + (h.errors.length ? ': ' + h.errors.slice(0, 3).join(' | ') : ''));
} catch (e) {
  ok(false, 'TEST FAIL ' + String(e.stack || e).slice(0, 700));
} finally {
  await h.close();
}
console.log(bad ? `gate6: ${bad} FAIL` : 'PASS');
process.exit(bad ? 1 : 0);
