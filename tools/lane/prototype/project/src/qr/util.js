// Small maths helpers shared by the simulation (no rendering dependencies).
export const PI = Math.PI, TAU = Math.PI * 2, DEG = Math.PI / 180, RAD = 180 / Math.PI;
export const MPH = 2.2369362920544, G = 9.81;
export const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
export const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
export const lerp = (a, b, t) => a + (b - a) * t;
export const sign = (v) => (v > 0 ? 1 : v < 0 ? -1 : 0);
export const smoothstep = (a, b, x) => { const t = clamp01((x - a) / (b - a)); return t * t * (3 - 2 * t); };
export const hyp = Math.hypot;
export const sq = (x) => x * x;
// Move a toward b by at most d.
export const approach = (a, b, d) => (a < b ? Math.min(a + d, b) : Math.max(a - d, b));
// Frame-rate independent exponential smoothing factor.
export const damp = (rate, dt) => 1 - Math.exp(-rate * dt);
export function angDiff(a, b) { let d = (a - b) % TAU; if (d > PI) d -= TAU; else if (d < -PI) d += TAU; return d; }

// Deterministic random (mulberry32) so the town is the same on every load.
export function rng(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export function hash2(ix, iz) {
  let h = Math.imul(ix | 0, 374761393) + Math.imul(iz | 0, 668265263);
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}
// Smooth value noise in 2D, range 0..1.
export function vnoise(x, z) {
  const ix = Math.floor(x), iz = Math.floor(z);
  let fx = x - ix, fz = z - iz;
  fx = fx * fx * (3 - 2 * fx); fz = fz * fz * (3 - 2 * fz);
  const a = hash2(ix, iz), b = hash2(ix + 1, iz), c = hash2(ix, iz + 1), d = hash2(ix + 1, iz + 1);
  return a + (b - a) * fx + (c - a) * fz + (a - b - c + d) * fx * fz;
}
export function fbm(x, z, oct = 4) {
  let s = 0, a = 0.5, f = 1, n = 0;
  for (let i = 0; i < oct; i++) { s += a * vnoise(x * f, z * f); n += a; a *= 0.5; f *= 2.03; }
  return s / n;
}
// Piecewise-linear table lookup: pts = [[x0,y0],[x1,y1],...] sorted by x.
export function table(pts, x) {
  const n = pts.length;
  if (x <= pts[0][0]) return pts[0][1];
  if (x >= pts[n - 1][0]) return pts[n - 1][1];
  for (let i = 1; i < n; i++) if (x < pts[i][0]) { const p = pts[i - 1], q = pts[i]; return p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0]); }
  return pts[n - 1][1];
}
