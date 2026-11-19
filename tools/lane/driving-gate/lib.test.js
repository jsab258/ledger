'use strict';
const test = require('node:test');
const assert = require('node:assert');
const L = require('./lib.js');

const series = (n, f, dt = 1 / 120) => Array.from({ length: n }, (_, i) => ({ t: i * dt, v: f(i * dt) }));

test('a ramp at 6 per second is not a snap', () => {
  const r = L.inputSmooth(series(60, (t) => Math.min(1, Math.max(0, (t - 0.05) * 6))));
  assert.strictEqual(r.snap, false);
  assert.ok(r.riseFrames >= 7, 'rise ' + r.riseFrames);
});

test('full lock within one frame is a snap', () => {
  const r = L.inputSmooth(series(60, (t) => (t >= 0.1 ? 1 : 0)));
  assert.strictEqual(r.snap, true);
  assert.ok(r.maxStep > 0.9);
});

test('a smooth first-order yaw build is not a jerk', () => {
  const r = L.yawSmooth(series(120, (t) => 0.5 * (1 - Math.exp(-t / 0.18))));
  assert.strictEqual(r.jerk, false);
});

test('a sudden yaw-rate jump is a jerk', () => {
  const r = L.yawSmooth(series(120, (t) => (t < 0.3 ? 0.02 * t : 0.4 + 0.02 * t)));
  assert.strictEqual(r.jerk, true);
});

const row = (t, speed, x, act = false, walker = 'drive') => ({ t, speed, x, z: 0, wx: 0, wz: 0, walker, act });

test('a car that stops and moves off again under throttle is not stranded', () => {
  const rows = [];
  for (let i = 0; i <= 100; i++) rows.push(row(i * 0.1, i < 20 ? 20 : i < 30 ? 0 : 5, i < 20 ? i : i < 30 ? 20 : 20 + (i - 30) * 0.2, i >= 25));
  const s = L.strandedStops(rows);
  assert.strictEqual(s.length, 1);
  assert.strictEqual(s[0].stranded, false);
  assert.ok(s[0].movedAfter > 0);
});

test('a car that will not move while the player presses throttle is stranded', () => {
  const rows = [];
  for (let i = 0; i <= 100; i++) rows.push(row(i * 0.1, i < 20 ? 20 : 0, i < 20 ? i : 20, i >= 20));
  const s = L.strandedStops(rows);
  assert.strictEqual(s[0].stranded, true);
  assert.ok(L.longestDeadInput(rows) >= 7);
});

test('walking away counts as moving', () => {
  const rows = [];
  for (let i = 0; i <= 60; i++) rows.push(i < 10 ? row(i * 0.1, 20, i) : { ...row(i * 0.1, 0, 10, i > 20, 'foot'), wx: i > 20 ? (i - 20) * 0.15 : 0 });
  assert.strictEqual(L.strandedStops(rows)[0].stranded, false);
});

test('flat share finds a one-colour frame', () => {
  assert.ok(L.flatShare({ a: 95, b: 5 }) > 0.9);
  assert.ok(L.flatShare({ a: 30, b: 30, c: 40 }) < 0.5);
});

// Steering series that press, release and reverse. A keyboard-style ramp toward a target at `rate` per second.
function keySeries(plan, rateIn, rateOut, dt = 1 / 120) {
  // plan: [[t, target]] the key target from time t; returns rows and the events
  const rows = [], end = plan[plan.length - 1][0] + 0.6; let v = 0, p = 0;
  for (let t = 0; t <= end + 1e-9; t += dt) {
    while (p + 1 < plan.length && t >= plan[p + 1][0] - 1e-9) p++;
    const want = t >= plan[0][0] - 1e-9 ? plan[p][1] : 0;
    if (want !== 0 && v * want >= 0) v = v + Math.sign(want - v) * Math.min(Math.abs(want - v), rateIn * dt);
    else v = v + Math.sign(0 - v) * Math.min(Math.abs(v), rateOut * dt);
    rows.push({ t: +t.toFixed(6), v });
  }
  return rows;
}
const PLAN = [[0.2, 1], [0.8, 0], [1.4, 1], [2.0, -1], [2.8, 0]];
const EVENTS = [{ t: 0.2, label: 'press A' }, { t: 0.8, label: 'release A' }, { t: 1.4, label: 'press A again' }, { t: 2.0, label: 'A to D' }, { t: 2.8, label: 'release D' }];

test('a key ramp at 6 per second in and out passes the press, the release and A to D', () => {
  const r = L.judgeSteer(keySeries(PLAN, 6, 6), EVENTS);
  assert.strictEqual(r.length, 5);
  for (const m of r) assert.ok(m.pass, JSON.stringify(m));
  assert.ok(r[0].riseS >= 0.12 && r[0].riseS <= 0.14, 'press rise ' + r[0].riseS);
  assert.ok(r[3].riseS > 0.2, 'A to D crosses the whole range ' + r[3].riseS);
});

test('a smooth press with a snap back on release fails the release only', () => {
  const r = L.judgeSteer(keySeries(PLAN, 6, 60), EVENTS);
  assert.strictEqual(r[0].pass, true);
  assert.strictEqual(r[1].pass, false, JSON.stringify(r[1]));
  assert.ok(r[1].snap && r[1].jump);
});

test('a two-frame ramp is caught as a snap, though it is not instant', () => {
  const r = L.judgeSteer(keySeries([[0.2, 1], [0.8, 0]], 30, 30), [{ t: 0.2, label: 'press' }, { t: 0.8, label: 'release' }]);
  assert.strictEqual(r[0].snap, true, JSON.stringify(r[0]));
  assert.strictEqual(r[1].snap, true);
});

test('swapping A for D in one frame fails A to D', () => {
  const rows = keySeries([[0.2, 1], [0.8, -1]], 6, 6).map((x) => ({ ...x }));
  for (const x of rows) if (x.t >= 0.8) x.v = -1;      // the swap jumps straight to the other side
  const r = L.judgeSteer(rows, [{ t: 0.2, label: 'press A' }, { t: 0.8, label: 'A to D' }]);
  assert.strictEqual(r[0].pass, true);
  assert.strictEqual(r[1].pass, false);
  assert.ok(r[1].maxStep >= 1.9);
});

test('a yaw rate that drops in one frame on release is a jump; a smooth decay is not', () => {
  const smooth = series(120, (t) => (t < 0.4 ? 0.5 * (1 - Math.exp(-t / 0.18)) : 0.5 * (1 - Math.exp(-0.4 / 0.18)) * Math.exp(-(t - 0.4) / 0.18)));
  const snap = series(120, (t) => (t < 0.4 ? 0.5 * (1 - Math.exp(-t / 0.18)) : 0.02));
  const ev = [{ t: 0, label: 'press' }, { t: 0.4, label: 'release' }];
  assert.ok(L.judgeYaw(smooth, ev).every((m) => m.pass), JSON.stringify(L.judgeYaw(smooth, ev)));
  const j = L.judgeYaw(snap, ev);
  assert.strictEqual(j[0].pass, true);
  assert.strictEqual(j[1].jump, true);
});

test('damage told counts only damage words shown after the hit', () => {
  const toasts = [{ t: 9, text: 'The car will not drive on. R repairs it.' }, { t: 10.2, text: 'Back on the road' }, { t: 10.5, text: 'Headlamps: on' }];
  assert.strictEqual(L.damageTold(toasts, 10).length, 0, 'an older message or an unrelated one does not count');
  assert.strictEqual(L.damageTold(toasts.concat([{ t: 10.1, text: 'The car will not drive on. R repairs it.' }]), 10).length, 1);
});
