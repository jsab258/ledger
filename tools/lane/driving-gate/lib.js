// Pure measures the gate uses. No browser here, so they are tested on made-up rows (lib.test.js).
'use strict';

// Steering smoothness. rows: [{t, v}] at a fixed step (v: steering input -1..1, or yaw rate in rad/s).
// Looks at the series as a player sees it, one value per 60 Hz frame.
// Returns the biggest frame-to-frame change, the frames taken from 10% to 90% of the move, and whether either
// counts as a snap or a jerk by the limits below.
const FRAME = 1 / 60;
const LIMITS = {
  snapFrames: 2,        // input reaching 90% of its move from 10% in this many frames or fewer is a snap
  yawStep: 0.15,        // rad/s change in yaw rate within one frame (about 9 rad/s2); a smooth step-steer is near 0.04
  yawStepRatio: 3,      // ... and it must stand out: this many times the typical change while the yaw is building
};

function perFrame(rows) {
  if (!rows.length) return [];
  const out = [rows[0]]; let next = rows[0].t + FRAME - 2e-4;   // tolerance: times are rounded to 4 places
  for (const r of rows) if (r.t >= next) { out.push(r); next = r.t + FRAME - 2e-4; }
  return out;
}

function rise(frames) {
  // frames from leaving 10% to reaching 90% of the largest move away from the first value
  if (frames.length < 2) return null;
  const v0 = frames[0].v; let peak = 0;
  for (const f of frames) if (Math.abs(f.v - v0) > Math.abs(peak)) peak = f.v - v0;
  if (Math.abs(peak) < 1e-6) return null;
  let a = -1, b = -1;
  for (let i = 0; i < frames.length; i++) {
    const k = (frames[i].v - v0) / peak;
    if (a < 0 && k >= 0.1) a = i;
    if (a >= 0 && k >= 0.9) { b = i; break; }
  }
  return a >= 0 && b >= 0 ? b - a : null;
}

function steps(frames) {
  const d = [];
  for (let i = 1; i < frames.length; i++) d.push(Math.abs(frames[i].v - frames[i - 1].v));
  return d;
}
function median(a) { if (!a.length) return 0; const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; }

function inputSmooth(rows) {
  const f = perFrame(rows), r = rise(f), d = steps(f), max = d.length ? Math.max(...d) : 0;
  return { riseFrames: r, maxStep: +max.toFixed(3), snap: r !== null && r <= LIMITS.snapFrames };
}

function yawSmooth(rows) {
  const f = perFrame(rows), d = steps(f), max = d.length ? Math.max(...d) : 0;
  const moving = d.filter((x) => x > 0.005).sort((a, b) => a - b); moving.pop();   // the typical change, leaving out the largest
  const typ = median(moving);
  const jerk = max > LIMITS.yawStep && (typ === 0 || max > LIMITS.yawStepRatio * typ);
  return { maxStep: +max.toFixed(3), typicalStep: +typ.toFixed(3), jerk };
}

// Steering moves: the press, the release and the switch from one side to the other, each judged on its own.
// rows: [{t, v}] (any fixed step; looked at once per 60 Hz frame). events: [{t, label}] in time order: the moment
// a key or stick changed. Each event's window runs to the next event. For each one: the value just before (from),
// where it settles (to, the mean of the window's last 3 frames), the time from 10% to 90% of that move (linear
// between frames), and the biggest change in one frame. A move under minMove is not timed (only its steps).
// Pass: the 10-90% time is at least minRise (about 0.1 s) and no frame changes it by more than maxStep.
const MOVE = {
  minRise: 0.1,         // seconds from 10% to 90% of a move
  riseSlack: 0.005,     // measuring tolerance on that time
  steerStep: 0.15,      // most a steering value (1 = full lock) may change in one 60 Hz frame; a ramp that just
                        // meets 0.1 s for a full press changes about 0.13 a frame
  yawStep: 0.15,        // most the yaw rate may change in one frame, rad/s
  minMove: { steer: 0.05, yaw: 0.1 },
};

function judgeMoves(rows, events, { maxStep, minMove, minRise = MOVE.minRise } = {}) {
  const f = perFrame(rows), out = [];
  for (let e = 0; e < events.length; e++) {
    const t0 = events[e].t, t1 = e + 1 < events.length ? events[e + 1].t : Infinity;
    let bi = -1; for (let i = 0; i < f.length; i++) { if (f[i].t < t0 - 1e-9) bi = i; else break; }
    const win = f.filter((r) => r.t >= t0 - 1e-9 && r.t < t1 - 1e-9);
    if (!win.length) { out.push({ label: events[e].label, empty: true }); continue; }
    const before = bi >= 0 ? f[bi] : win[0], seq = [before, ...win.filter((r) => r !== before)];
    const v0 = before.v, tail = win.slice(-3), v1 = tail.reduce((a, r) => a + r.v, 0) / tail.length, move = v1 - v0;
    let step = 0, stepAt = 0; for (let i = 1; i < seq.length; i++) { const d = Math.abs(seq[i].v - seq[i - 1].v); if (d > step) { step = d; stepAt = seq[i].t - t0; } }
    let rise = null, done = false;
    if (Math.abs(move) >= minMove) {
      const at = (k) => { for (let i = 1; i < seq.length; i++) { const a = (seq[i - 1].v - v0) / move, b = (seq[i].v - v0) / move;
        if (b >= k) return a >= k ? seq[i - 1].t : seq[i - 1].t + (seq[i].t - seq[i - 1].t) * (k - a) / (b - a); } return null; };
      const ta = at(0.1), tb = at(0.9);
      if (ta !== null && tb !== null) { rise = +(tb - ta).toFixed(3); done = true; }
    }
    const snap = done && rise < minRise - MOVE.riseSlack, jump = step > maxStep;
    out.push({ label: events[e].label, from: +v0.toFixed(3), to: +v1.toFixed(3), riseS: rise, maxStep: +step.toFixed(3), stepAt: +stepAt.toFixed(3), snap, jump, pass: !snap && !jump });
  }
  return out;
}
const judgeSteer = (rows, events) => judgeMoves(rows, events, { maxStep: MOVE.steerStep, minMove: MOVE.minMove.steer });
const judgeYaw = (rows, events) => judgeMoves(rows, events, { maxStep: MOVE.yawStep, minMove: MOVE.minMove.yaw });

// Damage in words: a message counts only if it was shown at or after the hit, within `within` seconds, and
// speaks of damage or what to do about it. toasts: [{t, text}].
const DAMAGE_WORDS = /damag|dent|crumpl|wreck|broken|smash|will not drive|won't drive|repair/i;
function damageTold(toasts, hitT, within = 3) {
  return toasts.filter((m) => m.t >= hitT - 1e-6 && m.t <= hitT + within && DAMAGE_WORDS.test(m.text));
}

// Stranded: after the player has stopped, does anything they do move them within `within` seconds?
// rows: [{t, x, z, wx, wz, walker, act}] where act is true while the player is pressing something that should
// move them (throttle, reverse, walk). Returns each stop and how long until they had moved `dist` metres, or null.
function strandedStops(rows, { within = 5, dist = 0.5, stopMph = 0.5 } = {}) {
  const stops = []; let moving = false;
  for (let i = 0; i < rows.length; i++) {
    const r = rows[i];
    if (Math.abs(r.speed) > 3) moving = true;
    if (moving && Math.abs(r.speed) < stopMph) {
      moving = false;
      const p0 = where(r); let moved = null;
      for (let j = i + 1; j < rows.length && rows[j].t - r.t <= within; j++) {
        const p = where(rows[j]);
        if (Math.hypot(p[0] - p0[0], p[1] - p0[1]) >= dist) { moved = +(rows[j].t - r.t).toFixed(2); break; }
      }
      const tried = rows.some((q) => q.t > r.t && q.t - r.t <= within && q.act);
      stops.push({ t: +r.t.toFixed(2), movedAfter: moved, tried, stranded: tried && moved === null });
    }
  }
  return stops;
}
function where(r) { return r.walker && r.walker !== 'drive' ? [r.wx, r.wz] : [r.x, r.z]; }

// Unresponsive: the longest stretch in seconds during which the player pressed something (act) and neither the
// car nor the person moved at all (less than 5 cm per second of pressing).
function longestDeadInput(rows) {
  let best = 0, start = null, p0 = null;
  for (const r of rows) {
    if (!r.act) { start = null; continue; }
    const p = where(r);
    if (start === null) { start = r.t; p0 = p; continue; }
    const span = r.t - start;
    if (Math.hypot(p[0] - p0[0], p[1] - p0[1]) > 0.05 * Math.max(1, span)) { start = r.t; p0 = p; continue; }
    best = Math.max(best, span);
  }
  return +best.toFixed(2);
}

// A picture filled mostly by one flat colour (the camera inside a wall shows one surface). hist: counts of
// pixels per quantised colour. Returns the largest colour's share.
function flatShare(hist) {
  let total = 0, top = 0;
  for (const k in hist) { total += hist[k]; if (hist[k] > top) top = hist[k]; }
  return total ? top / total : 0;
}

module.exports = { LIMITS, MOVE, judgeMoves, judgeSteer, judgeYaw, damageTold, DAMAGE_WORDS, perFrame, inputSmooth, yawSmooth, strandedStops, longestDeadInput, flatShare };
