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
