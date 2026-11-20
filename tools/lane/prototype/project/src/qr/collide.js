// Collision in the ground plane. Shapes are oriented boxes and circles; the response is impulse based
// with restitution and friction, so cars are shoved and spun rather than simply stopped.
import { clamp } from './util.js';

export const M = { n: 0, nx: 0, nz: 0, px: [0, 0], pz: [0, 0], depth: [0, 0] };
const cA = [0, 0, 0, 0], cB = [0, 0, 0, 0];

function clip(out, inp, nx, nz, off) {
  let n = 0;
  const d0 = nx * inp[0] + nz * inp[1] - off, d1 = nx * inp[2] + nz * inp[3] - off;
  if (d0 <= 0) { out[0] = inp[0]; out[1] = inp[1]; n++; }
  if (d1 <= 0) { out[n * 2] = inp[2]; out[n * 2 + 1] = inp[3]; n++; }
  if (d0 * d1 < 0) { const t = d0 / (d0 - d1); out[n * 2] = inp[0] + t * (inp[2] - inp[0]); out[n * 2 + 1] = inp[1] + t * (inp[3] - inp[1]); n++; }
  return n;
}
// Box against box. Boxes: {x, z, ux, uz, hu, vx, vz, hv}. Normal points from A to B. Returns the contact count.
export function boxBox(A, B) {
  M.n = 0;
  const dx = B.x - A.x, dz = B.z - A.z;
  const dAu = dx * A.ux + dz * A.uz, dAv = dx * A.vx + dz * A.vz, dBu = dx * B.ux + dz * B.uz, dBv = dx * B.vx + dz * B.vz;
  const a00 = Math.abs(A.ux * B.ux + A.uz * B.uz), a01 = Math.abs(A.ux * B.vx + A.uz * B.vz), a10 = Math.abs(A.vx * B.ux + A.vz * B.uz), a11 = Math.abs(A.vx * B.vx + A.vz * B.vz);
  const fAu = Math.abs(dAu) - A.hu - (a00 * B.hu + a01 * B.hv); if (fAu > 0) return 0;
  const fAv = Math.abs(dAv) - A.hv - (a10 * B.hu + a11 * B.hv); if (fAv > 0) return 0;
  const fBu = Math.abs(dBu) - B.hu - (a00 * A.hu + a10 * A.hv); if (fBu > 0) return 0;
  const fBv = Math.abs(dBv) - B.hv - (a01 * A.hu + a11 * A.hv); if (fBv > 0) return 0;
  let axis = 0, sep = fAu, nx = dAu > 0 ? A.ux : -A.ux, nz = dAu > 0 ? A.uz : -A.uz;
  if (fAv > 0.95 * sep + 0.01 * A.hv) { axis = 1; sep = fAv; nx = dAv > 0 ? A.vx : -A.vx; nz = dAv > 0 ? A.vz : -A.vz; }
  if (fBu > 0.95 * sep + 0.01 * B.hu) { axis = 2; sep = fBu; nx = dBu > 0 ? B.ux : -B.ux; nz = dBu > 0 ? B.uz : -B.uz; }
  if (fBv > 0.95 * sep + 0.01 * B.hv) { axis = 3; sep = fBv; nx = dBv > 0 ? B.vx : -B.vx; nz = dBv > 0 ? B.vz : -B.vz; }
  let fnx, fnz, front, snx, snz, neg, pos, I;
  if (axis === 0) { fnx = nx; fnz = nz; front = A.x * fnx + A.z * fnz + A.hu; snx = A.vx; snz = A.vz; const s = A.x * snx + A.z * snz; neg = -s + A.hv; pos = s + A.hv; I = B; }
  else if (axis === 1) { fnx = nx; fnz = nz; front = A.x * fnx + A.z * fnz + A.hv; snx = A.ux; snz = A.uz; const s = A.x * snx + A.z * snz; neg = -s + A.hu; pos = s + A.hu; I = B; }
  else if (axis === 2) { fnx = -nx; fnz = -nz; front = B.x * fnx + B.z * fnz + B.hu; snx = B.vx; snz = B.vz; const s = B.x * snx + B.z * snz; neg = -s + B.hv; pos = s + B.hv; I = A; }
  else { fnx = -nx; fnz = -nz; front = B.x * fnx + B.z * fnz + B.hv; snx = B.ux; snz = B.uz; const s = B.x * snx + B.z * snz; neg = -s + B.hu; pos = s + B.hu; I = A; }
  // incident edge: the face of I that most faces the reference face
  const nu = -(fnx * I.ux + fnz * I.uz), nv = -(fnx * I.vx + fnz * I.vz);
  let e0u, e0v, e1u, e1v;
  if (Math.abs(nu) > Math.abs(nv)) { if (nu > 0) { e0u = I.hu; e0v = -I.hv; e1u = I.hu; e1v = I.hv; } else { e0u = -I.hu; e0v = I.hv; e1u = -I.hu; e1v = -I.hv; } }
  else if (nv > 0) { e0u = I.hu; e0v = I.hv; e1u = -I.hu; e1v = I.hv; } else { e0u = -I.hu; e0v = -I.hv; e1u = I.hu; e1v = -I.hv; }
  cA[0] = I.x + I.ux * e0u + I.vx * e0v; cA[1] = I.z + I.uz * e0u + I.vz * e0v; cA[2] = I.x + I.ux * e1u + I.vx * e1v; cA[3] = I.z + I.uz * e1u + I.vz * e1v;
  if (clip(cB, cA, -snx, -snz, neg) < 2) return 0;
  if (clip(cA, cB, snx, snz, pos) < 2) return 0;
  let n = 0;
  for (let i = 0; i < 2; i++) {
    const px = cA[i * 2], pz = cA[i * 2 + 1], s = fnx * px + fnz * pz - front;
    if (s <= 0) { M.px[n] = px - s * fnx * 0.5; M.pz[n] = pz - s * fnz * 0.5; M.depth[n] = -s; n++; }
  }
  M.n = n; M.nx = nx; M.nz = nz;
  return n;
}
// Box A against a circle. Normal points from the box to the circle.
export function boxCircle(A, cx, cz, r) {
  M.n = 0;
  const dx = cx - A.x, dz = cz - A.z, lu = dx * A.ux + dz * A.uz, lv = dx * A.vx + dz * A.vz;
  const qu = clamp(lu, -A.hu, A.hu), qv = clamp(lv, -A.hv, A.hv), du = lu - qu, dv = lv - qv, d2 = du * du + dv * dv;
  if (d2 > r * r) return 0;
  let nu, nv, depth;
  if (d2 > 1e-10) { const d = Math.sqrt(d2); nu = du / d; nv = dv / d; depth = r - d; }
  else { const pu = A.hu - Math.abs(lu), pv = A.hv - Math.abs(lv); if (pu < pv) { nu = lu > 0 ? 1 : -1; nv = 0; depth = pu + r; } else { nu = 0; nv = lv > 0 ? 1 : -1; depth = pv + r; } }
  M.nx = A.ux * nu + A.vx * nv; M.nz = A.uz * nu + A.vz * nv;
  M.px[0] = cx - M.nx * (r - depth * 0.5); M.pz[0] = cz - M.nz * (r - depth * 0.5); M.depth[0] = depth; M.n = 1;
  return 1;
}

// A light planar rigid body: parked cars, crashed traffic and loose crates.
export class Body2D {
  constructor(x, z, yaw, hw, hl, mass, h = 1.3) {
    this.x = x; this.z = z; this.yaw = yaw; this.hw = hw; this.hl = hl; this.h = h; this.vx = 0; this.vz = 0; this.wy = 0;
    this.mass = mass; this.invM = 1 / mass; this.invI = 1 / (mass * (hw * hw + hl * hl) / 3 * 1.15);
    this.awake = false; this.kin = false; this.braked = true; this.muLat = 7.5; this.muLong = 6.5; this.rest = 0; this.hit = 0; this.kind = 'car';
    this.box = { x: 0, z: 0, ux: 1, uz: 0, hu: hw, vx: 0, vz: 1, hv: hl };
    this.sync();
  }
  sync() { const b = this.box, s = Math.sin(this.yaw), c = Math.cos(this.yaw); b.x = this.x; b.z = this.z; b.ux = c; b.uz = -s; b.vx = s; b.vz = c; b.hu = this.hw; b.hv = this.hl; return b; }
  velAt(px, pz, out) { const rx = px - this.x, rz = pz - this.z; out[0] = this.vx + this.wy * rz; out[1] = 0; out[2] = this.vz - this.wy * rx; return out; }
  invMassAt(px, pz, nx, nz) { const c = (pz - this.z) * nx - (px - this.x) * nz; return this.invM + c * c * this.invI; }
  impulse(px, pz, jx, jz) { this.vx += jx * this.invM; this.vz += jz * this.invM; this.wy += ((pz - this.z) * jx - (px - this.x) * jz) * this.invI; this.awake = true; this.rest = 0; }
  // Slide to a stop on tyres: strong sideways scrub, wheels braked or in gear.
  integrate(dt) {
    if (!this.awake || this.kin) return;
    const s = Math.sin(this.yaw), c = Math.cos(this.yaw);
    let vf = this.vx * s + this.vz * c, vl = this.vx * c - this.vz * s;
    const al = this.muLat * dt, af = (this.braked ? this.muLong : 0.35) * dt;
    vl = Math.abs(vl) <= al ? 0 : vl - Math.sign(vl) * al; vf = Math.abs(vf) <= af ? 0 : vf - Math.sign(vf) * af;
    this.vx = vf * s + vl * c; this.vz = vf * c - vl * s;
    const aw = 5.5 * dt; this.wy = Math.abs(this.wy) <= aw ? 0 : this.wy - Math.sign(this.wy) * aw;
    this.x += this.vx * dt; this.z += this.vz * dt; this.yaw += this.wy * dt;
    if (Math.abs(this.vx) + Math.abs(this.vz) < 0.03 && Math.abs(this.wy) < 0.03) { this.rest += dt; if (this.rest > 0.4) { this.awake = false; this.vx = this.vz = this.wy = 0; } } else this.rest = 0;
    this.sync();
  }
}

// Adapter so the player's 3D car can share the same solver. yc is the contact height in world space.
const pv = [0, 0, 0], pw = [0, 0, 0];
export class CarProxy {
  constructor(veh) { this.v = veh; this.box = { x: 0, z: 0, ux: 1, uz: 0, hu: 0.82, vx: 0, vz: 1, hv: 1.98 }; this.yc = 0; this.o = [0, 0, 0]; }
  sync() {
    const v = this.v, R = v.R, b = this.box; v.updateAxes(); v.origin(this.o);
    let fx = R[6], fz = R[8]; const l = Math.hypot(fx, fz) || 1; fx /= l; fz /= l;
    b.vx = fx; b.vz = fz; b.ux = fz; b.uz = -fx; b.x = this.o[0] + fx * 0.04; b.z = this.o[2] + fz * 0.04;
    return b;
  }
  velAt(px, pz, out) { const v = this.v; return v.pointVel(px - v.pos[0], this.yc - v.pos[1], pz - v.pos[2], out); }
  invMassAt(px, pz, nx, nz) { const v = this.v; return v.invMassAt(px - v.pos[0], this.yc - v.pos[1], pz - v.pos[2], nx, 0, nz); }
  impulse(px, pz, jx, jz) { const v = this.v; v.applyImpulse(px - v.pos[0], this.yc - v.pos[1], pz - v.pos[2], jx, 0, jz); }
}

export const HIT = { jn: 0, vn: 0, vt: 0, px: 0, pz: 0, nx: 0, nz: 0, depth: 0 };
// Resolve the current manifold M between A and B (B may be null for a fixed obstacle).
// The manifold normal points from A to B. Fills HIT with what happened to A.
// cap limits the normal impulse this step (a crumple zone: the stop is spread over a few steps); maxCorr limits push-out per step.
export function resolve(A, B, rest, mu, moveA, moveB, cap = 1e12, maxCorr = 1, rebound = 0) {
  const n = M.n; if (!n) return 0;
  const nx = -M.nx, nz = -M.nz, tx = -nz, tz = nx;   // n: direction that pushes A away
  let jsum = 0, vn0 = 0, vtMax = 0, sx = 0, sz = 0, dmax = 0;
  const acc = [0, 0], tgt = [0, 0], capK = cap / n;
  for (let k = 0; k < n; k++) {
    A.velAt(M.px[k], M.pz[k], pv); let vn = pv[0] * nx + pv[2] * nz;
    if (B) { B.velAt(M.px[k], M.pz[k], pw); vn -= pw[0] * nx + pw[2] * nz; }
    tgt[k] = Math.max(rebound, vn < -1.2 ? -rest * vn : 0); if (-vn > vn0) vn0 = -vn;
    sx += M.px[k]; sz += M.pz[k]; if (M.depth[k] > dmax) dmax = M.depth[k];
  }
  for (let it = 0; it < 4; it++) for (let k = 0; k < n; k++) {
    const px = M.px[k], pz = M.pz[k];
    A.velAt(px, pz, pv); let vx = pv[0], vz = pv[2];
    if (B) { B.velAt(px, pz, pw); vx -= pw[0]; vz -= pw[2]; }
    const vn = vx * nx + vz * nz;
    const K = A.invMassAt(px, pz, nx, nz) + (B ? B.invMassAt(px, pz, nx, nz) : 0);
    let dj = (tgt[k] - vn) / K; const old = acc[k]; acc[k] = Math.min(capK, Math.max(0, old + dj)); dj = acc[k] - old;
    if (dj !== 0) { A.impulse(px, pz, nx * dj, nz * dj); if (B) B.impulse(px, pz, -nx * dj, -nz * dj); }
    // friction along the surface
    A.velAt(px, pz, pv); vx = pv[0]; vz = pv[2];
    if (B) { B.velAt(px, pz, pw); vx -= pw[0]; vz -= pw[2]; }
    const vt = vx * tx + vz * tz; if (Math.abs(vt) > vtMax) vtMax = Math.abs(vt);
    const Kt = A.invMassAt(px, pz, tx, tz) + (B ? B.invMassAt(px, pz, tx, tz) : 0);
    const jt = clamp(-vt / Kt, -mu * Math.abs(dj), mu * Math.abs(dj));
    if (jt !== 0) { A.impulse(px, pz, tx * jt, tz * jt); if (B) B.impulse(px, pz, -tx * jt, -tz * jt); }
  }
  for (let k = 0; k < n; k++) jsum += acc[k];
  // push the shapes apart
  const corr = Math.min(maxCorr, Math.max(0, dmax - 0.004) * 0.85);
  if (corr > 0) {
    if (B && moveB) { const wa = A.invMassAt(sx / n, sz / n, nx, nz), wb = B.invMassAt(sx / n, sz / n, nx, nz), f = wa / (wa + wb); moveA(nx * corr * f, nz * corr * f); moveB(-nx * corr * (1 - f), -nz * corr * (1 - f)); }
    else moveA(nx * corr, nz * corr);
  }
  HIT.jn = jsum; HIT.vn = vn0; HIT.vt = vtMax; HIT.px = sx / n; HIT.pz = sz / n; HIT.nx = nx; HIT.nz = nz; HIT.depth = dmax;
  return jsum;
}
