// The player's car: one rigid body, four quarter-car suspension corners with a vertical tyre spring and
// hub mass, anti-roll bars, a combined-slip Magic Formula tyre with relaxation lengths, engine, clutch,
// five-speed gearbox, open front differential and unassisted brakes. SI units throughout.
// Car axes: +X left, +Y up, +Z forward. World: Y up. One physics step is 1/120 s; inside it the body, hubs,
// tyres and driveline are integrated in 4 sub-steps (480 Hz). Nothing in here reads a clock or a random number:
// the same inputs from the same reset state give the same numbers every time.
import { clamp, clamp01, smoothstep, sign, approach, table, lerp, G, DEG } from './util.js';
import { groundY, baseY, hillSlope, surfaceType, puddleAt, env, SURF } from './world.js'; // LEDGER: the Hook answers for the study's town (qr/world.js); nothing else in this file is changed
import { atan, atan2, cos, exp, hypot, hypot3, hypot4, pow, sin, tan } from './dmath.js';

export const SUB = 4;
const DISC = [-0.24, -0.16, -0.08, 0, 0.08, 0.16, 0.24];
const KMAX = 1.6, TMAX = 1.4, RHO_AIR = 1.225, RPM = 9.549296585513721;
export const worldGround = { y: groundY, base: baseY, slopeZ: hillSlope, type: surfaceType, puddle: puddleAt, wet: () => env.wet };

function solveB(C, E) {
  const target = tan(Math.PI / (2 * C));
  let lo = 0.01, hi = 80;
  for (let i = 0; i < 60; i++) { const B = (lo + hi) / 2; if (B - E * (B - atan(B)) - target > 0) hi = B; else lo = B; }
  return (lo + hi) / 2;
}
// Body outline used for collisions and ground contact, in the body-origin frame
// (origin on the ground under the middle of the wheelbase at ride height).
export const BODY = { halfW: 0.82, zFront: 2.02, zRear: -1.94, yLow: 0.2, yTop: 1.4 };
const HULL = [
  [0.74, 0.24, 1.96], [-0.74, 0.24, 1.96], [0.74, 0.24, -1.88], [-0.74, 0.24, -1.88], [0.8, 0.21, 0.3], [-0.8, 0.21, 0.3],
  [0.7, 0.86, 1.62], [-0.7, 0.86, 1.62], [0.56, 1.39, 0.5], [-0.56, 1.39, 0.5], [0.56, 1.37, -0.95], [-0.56, 1.37, -0.95], [0.7, 0.93, -1.82], [-0.7, 0.93, -1.82],
];

export class Vehicle {
  constructor(p, ground = worldGround) {
    this.p = p; this.g = ground;
    this.pos = new Float64Array(3); this.vel = new Float64Array(3); this.q = new Float64Array([0, 0, 0, 1]); this.w = new Float64Array(3);
    this.R = new Float64Array(9);
    this.wheels = [];
    for (let i = 0; i < 4; i++) this.wheels.push({ i, front: i < 2, left: (i & 1) === 0, lx: 0, ly0: 0, lz: 0, F0: 0, s: 0, sPrev: 0, u: 0, defl: 0, omega: 0, ang: 0, kap: 0, tana: 0, steer: 0, tq: 0, a: 0, Fz: 0, Fx: 0, Fy: 0, vlong: 0, vlat: 0, slipAngle: 0, slipRatio: 0, rho: 0, surf: 0, puddle: 0, onGround: false, cx: 0, cy: 0, cz: 0, sdot: 0, brakeT: 0, grip: 1, hit: 0 });
    this.eng = { w: 90, thr: 0, cut: 0, torque: 0, load: 0 };
    this.gear = 1; this.gearSel = 1; this.shiftT = 0; this.shiftTo = 1; this.clutch = 0; this.clutchLocked = false; this.autoT = 0;
    this.steer = 0; this.steerN = 0; this.hand = 0; this.steerBias = 0; this.auto = false; this.assists = 0; this.powerScale = 1; this.usefulLock = 0; this.betaF = 0;
    this.ctl = { steer: 0, throttle: 0, brake: 0, handbrake: 0, analog: false, shiftUp: false, shiftDown: false };
    this.tc = 0; this.esc = [0, 0, 0, 0]; this.escCut = 0; this.escActive = 0; this.tcActive = 0; this.brk = 0; this.hbk = 0;
    this.abs = [1, 1, 1, 1]; this.absActive = 0; this.hbT = 0;        // anti-lock: share of the brake each wheel is given; time since the handbrake was last on
    this.speed = 0; this.rpm = 850; this.yawRate = 0; this.accLong = 0; this.accLat = 0; this.bodySlip = 0; this.groundHit = 0; this.kerbHit = 0;
    this.shiftEvent = 0; this.limiterEvent = 0;
    this.prev = { pos: new Float64Array(3), q: new Float64Array([0, 0, 0, 1]), s: [0, 0, 0, 0], steer: [0, 0, 0, 0], ang: [0, 0, 0, 0] };
    this._pen = new Float64Array(7); this._pv = new Float64Array(3);
    this.derive(); this.reset(0, 0, 0);
  }

  // Recompute everything that depends on the tuning numbers. Call after any parameter change.
  derive() {
    const p = this.p, d = (this.d = this.d || {});
    d.m = p.mass + p.driverMass; d.invM = 1 / d.m;
    d.L = p.wheelbase; const fw = p.frontWeight / 100;
    d.a = d.L * (1 - fw); d.b = d.L * fw; d.zcg = d.L * (fw - 0.5);
    d.F0f = d.m * G * fw / 2; d.F0r = d.m * G * (1 - fw) / 2;
    d.SQ = DISC.map((x) => Math.sqrt(p.tyreRadius * p.tyreRadius - x * x));
    for (const W of this.wheels) {
      W.F0 = W.front ? d.F0f : d.F0r;
      W.lx = (W.left ? 1 : -1) * (W.front ? p.trackF : p.trackR) / 2;
      W.lz = W.front ? d.a : -d.b;
      W.ly0 = p.tyreRadius - W.F0 / p.tyreRate - p.cgHeight;
    }
    d.Bdry = solveB(p.shapeC, p.shapeE); d.Bwet = solveB(p.wetShapeC, p.shapeE);
    d.tanAp = tan(p.peakSlipAngle * DEG);
    d.tq = [[0, p.tq1000 * 0.5], [500, p.tq1000 * 0.8]];
    for (const r of [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]) d.tq.push([r, p['tq' + r]]);
    d.tq.push([7000, p.tq6500 * 0.55], [7600, 0]);
    d.maxTq = Math.max(...d.tq.map((t) => t[1]));
    d.ratios = [-p.gR, 0, p.g1, p.g2, p.g3, p.g4, p.g5];
    // Full lock as a road-wheel angle: the mean of the two front wheels (the bicycle-model angle).
    d.lock = p.maxSteer * DEG;
    d.hull = HULL.map((h) => [h[0], h[1] - p.cgHeight, h[2] - d.zcg]);
    return d;
  }

  reset(x, z, heading, speed = 0) {
    const p = this.p, d = this.d, g = this.g;
    const sl = g.slopeZ(z), pitch = -atan(sl * cos(heading));   // nose up when facing uphill
    // yaw then pitch about the car's left axis
    const cy = cos(heading / 2), sy = sin(heading / 2), cp = cos(pitch / 2), sp = sin(pitch / 2);
    this.q[0] = cy * sp; this.q[1] = sy * cp; this.q[2] = -sy * sp; this.q[3] = cy * cp;
    this.updateAxes();
    const R = this.R;
    this.pos[0] = x + R[6] * d.zcg; this.pos[2] = z + R[8] * d.zcg;
    this.pos[1] = g.base(this.pos[0], this.pos[2]) + p.cgHeight * R[4] + 0.02;
    this.vel[0] = R[6] * speed; this.vel[1] = R[7] * speed; this.vel[2] = R[8] * speed;
    this.w.fill(0);
    for (const W of this.wheels) { W.s = 0; W.sPrev = 0; W.u = this.vel[0] * R[3] + this.vel[1] * R[4] + this.vel[2] * R[5]; W.defl = W.F0 / p.tyreRate; W.omega = speed / p.tyreRadius; W.kap = 0; W.tana = 0; W.steer = 0; W.Fz = W.F0; }
    this.steer = 0; this.steerN = 0; this.hand = 0; this.brk = 0; this.hbk = 0; this.eng.w = Math.max(p.idleRpm / RPM, 0); this.eng.thr = 0; this.eng.cut = 0;
    this.shiftT = 0; this.clutch = 0; this.clutchLocked = false;
    if (speed > 3) { let gsel = 1; for (let k = 1; k <= 5; k++) if (speed / p.tyreRadius * d.ratios[k + 1] * p.finalDrive * RPM > 1700) gsel = k; this.gear = this.gearSel = gsel; this.eng.w = speed / p.tyreRadius * d.ratios[gsel + 1] * p.finalDrive; this.clutch = 1; this.clutchLocked = true; }
    else if (this.gearSel < 1 || this.gear < 1) { this.gear = this.gearSel = 1; }
    this.speed = speed; this.snapshot();
  }

  // The reset state for scripted drives: every piece of state the car carries is set, so nothing from an
  // earlier drive (gear, shift timers, driver aids, filtered values, damage) can leak into the next one.
  hardReset(x, z, heading) {
    const c = this.ctl, e = this.esc;
    this.gear = this.gearSel = 1; this.shiftTo = 1; this.shiftFrom = 1; this.autoT = 0; this.shiftEvent = 0; this.limiterEvent = 0;
    this.tc = 0; this.escCut = 0; e[0] = e[1] = e[2] = e[3] = 0; this.tcActive = this.escActive = 0;
    this.abs[0] = this.abs[1] = this.abs[2] = this.abs[3] = 1; this.absActive = 0; this.hbT = 0;
    this.steerBias = 0; this.powerScale = 1;
    c.steer = c.throttle = c.brake = c.handbrake = 0; c.shiftUp = c.shiftDown = false;
    this.eng.torque = 0; this.eng.load = 0; this.thrEff = 0; this.clutchTq = 0;
    this.accLong = this.accLat = 0; this.yawRate = 0; this.bodySlip = 0; this.groundHit = 0; this.kerbHit = 0; this.usefulLock = 0; this.betaF = 0;
    for (const W of this.wheels) { W.ang = 0; W.tq = 0; W.a = 0; W.Fx = W.Fy = 0; W.vlong = W.vlat = 0; W.slipAngle = W.slipRatio = 0; W.rho = 0; W.surf = 0; W.puddle = 0; W.onGround = true; W.sdot = 0; W.brakeT = 0; W.grip = 1; W.hit = 0; W.cx = W.cy = W.cz = 0; }
    this.reset(x, z, heading, 0);
    this.rpm = this.eng.w * RPM;
  }

  updateAxes() {
    const q = this.q, R = this.R, x = q[0], y = q[1], z = q[2], w = q[3];
    const xx = x * x, yy = y * y, zz = z * z, xy = x * y, xz = x * z, yz = y * z, wx = w * x, wy = w * y, wz = w * z;
    R[0] = 1 - 2 * (yy + zz); R[1] = 2 * (xy + wz); R[2] = 2 * (xz - wy);
    R[3] = 2 * (xy - wz); R[4] = 1 - 2 * (xx + zz); R[5] = 2 * (yz + wx);
    R[6] = 2 * (xz + wy); R[7] = 2 * (yz - wx); R[8] = 1 - 2 * (xx + yy);
  }
  snapshot() {
    const pr = this.prev; pr.pos.set(this.pos); pr.q.set(this.q);
    for (let i = 0; i < 4; i++) { const W = this.wheels[i]; pr.s[i] = W.s; pr.steer[i] = W.steer; pr.ang[i] = W.ang; }
  }
  get heading() { return atan2(this.R[6], this.R[8]); }
  get rideH() { return this.p.cgHeight; }      // height of the centre of mass above the road at rest
  frontOmega() { return (this.wheels[0].omega + this.wheels[1].omega) * 0.5; }
  // World position of the body origin (ground point under the middle of the wheelbase).
  origin(out) { const R = this.R, p = this.p, d = this.d; out[0] = this.pos[0] - R[3] * p.cgHeight - R[6] * d.zcg; out[1] = this.pos[1] - R[4] * p.cgHeight - R[7] * d.zcg; out[2] = this.pos[2] - R[5] * p.cgHeight - R[8] * d.zcg; return out; }

  engineTorque(rpm, thr) {
    const p = this.p, fr = p.engineBrake0 + p.engineBrake1 * rpm / 1000;
    return thr * (table(this.d.tq, rpm) * this.powerScale * p.engineScale + fr) - fr;
  }

  requestShift(to) {
    const p = this.p, d = this.d;
    if (this.shiftT > 0 || to === this.gearSel || to < -1 || to > 5) return false;
    if (to === -1 && this.speed > 1.5) return false;
    if (to >= 2 && this.speed < -1.5) return false;
    if (to >= 1 && to < this.gearSel && Math.abs(this.frontOmega()) * d.ratios[to + 1] * p.finalDrive * RPM > p.limiterRpm + 250) return false;
    this.shiftFrom = this.gearSel; this.shiftTo = to; this.gearSel = to;
    this.shiftT = this.gear === 0 || to === 0 ? p.shiftTime * 0.55 : p.shiftTime;
    this.gear = 0; this.clutchLocked = false; this.shiftEvent = to === 0 ? 0.5 : 1;
    return true;
  }

  // One 120 Hz step. ctl: steer -1..1 as a share of full lock (+ left), throttle, brake, handbrake 0..1,
  // shiftUp/shiftDown edges.
  step(dt) {
    const p = this.p, d = this.d, c = this.ctl, R = this.R, eng = this.eng;
    this.snapshot();
    const v0x = this.vel[0], v0y = this.vel[1], v0z = this.vel[2];
    this.updateSteering(dt);

    // ---- gearbox
    if (this.shiftT > 0) { this.shiftT -= dt; if (this.shiftT <= 0) { this.gear = this.shiftTo; this.shiftT = 0; } }
    else {
      if (c.shiftUp) this.requestShift(this.gearSel + 1); else if (c.shiftDown) this.requestShift(this.gearSel - 1);
      else if (this.auto) this.autoShift(dt);
    }
    c.shiftUp = c.shiftDown = false;
    const ratio = d.ratios[this.gear + 1] * p.finalDrive;
    const rpmIn = ratio * this.frontOmega() * RPM;
    this.rpm = eng.w * RPM;

    // ---- clutch
    let ct = 0;
    if (ratio !== 0 && this.shiftT <= 0) {
      if (this.clutchLocked && rpmIn < p.idleRpm + 20) this.clutchLocked = false;
      if (this.clutchLocked) ct = 1;
      else {
        if (rpmIn > this.rpm) ct = smoothstep(p.idleRpm - 50, p.idleRpm + 250, rpmIn);
        else { const lo = p.idleRpm + 150 + 1500 * c.throttle; ct = smoothstep(lo, lo + 700, this.rpm); }
        if (Math.abs(this.rpm - rpmIn) < 50 && rpmIn > p.idleRpm + 120 && this.clutch > 0.4) this.clutchLocked = true;
      }
    }
    this.clutch = approach(this.clutch, ct, dt / (ct > this.clutch ? 0.14 : 0.05));

    // ---- driver aids ("mild" by default since round three)
    this.updateAssists(dt);

    // ---- throttle
    let thr = c.throttle * (1 - this.tc) * (1 - this.escCut);
    if (this.shiftT > 0 && this.shiftFrom !== 0 && this.shiftTo !== 0) {
      if (this.shiftTo > this.shiftFrom) thr = 0;                                    // lift for the upshift
      else { const tgt = Math.abs(this.frontOmega()) * d.ratios[this.shiftTo + 1] * p.finalDrive * RPM; thr = clamp((tgt - this.rpm) / 1200, 0, 0.85); }   // blip on the way down
    }
    eng.thr += (thr - eng.thr) * (p.throttleLag > 0.001 ? 1 - exp(-dt / p.throttleLag) : 1);
    const idleThr = clamp(0.115 + (p.idleRpm - this.rpm) * 0.003, 0, 0.75);
    let thrEff = Math.max(eng.thr, idleThr);
    if (this.rpm > p.limiterRpm) { eng.cut = 0.05; this.limiterEvent = 1; }
    if (eng.cut > 0) { eng.cut -= dt; thrEff = 0; }
    eng.load = thrEff;
    this.thrEff = thrEff;

    // ---- brakes (anti-lock only as one of the driver aids)
    // brake pressure follows the pedal with a short lag (servo and hydraulics)
    this.brk += (c.brake - this.brk) * (p.brakeLag > 0.001 ? 1 - exp(-dt / p.brakeLag) : 1);
    this.hbk += (c.handbrake - this.hbk) * (p.handbrakeLag > 0.001 ? 1 - exp(-dt / p.handbrakeLag) : 1);   // the lever and cable take a moment too
    const bf = this.brk * p.brakeTorque * (p.brakeBias / 100) * 0.5, br = this.brk * p.brakeTorque * (1 - p.brakeBias / 100) * 0.5, hb = this.hbk * p.handbrakeTorque * 0.5;
    const ws = this.wheels;
    const ab = this.abs;
    ws[0].brakeT = bf * ab[0] + this.esc[0]; ws[1].brakeT = bf * ab[1] + this.esc[1]; ws[2].brakeT = br * ab[2] + hb + this.esc[2]; ws[3].brakeT = br * ab[3] + hb + this.esc[3];

    this.kerbHit = 0;
    const h = dt / SUB;
    for (let i = 0; i < SUB; i++) this.substep(h, ratio);
    this.groundContacts(dt);

    // ---- derived values for the camera, sound and telemetry
    this.speed = this.vel[0] * R[6] + this.vel[1] * R[7] + this.vel[2] * R[8];
    const ax = (this.vel[0] - v0x) / dt, ay = (this.vel[1] - v0y) / dt, az = (this.vel[2] - v0z) / dt;
    this.accLong += ((ax * R[6] + ay * R[7] + az * R[8]) - this.accLong) * 0.25;
    this.accLat += ((ax * R[0] + ay * R[1] + az * R[2]) - this.accLat) * 0.25;
    this.yawRate = this.w[0] * R[3] + this.w[1] * R[4] + this.w[2] * R[5];
    const vl = this.vel[0] * R[0] + this.vel[1] * R[1] + this.vel[2] * R[2];
    this.bodySlip = hypot(vl, this.speed) > 1.5 ? atan2(vl, Math.abs(this.speed)) : 0;   // angle between where the car points and where it goes (90 deg when broadside)
    this.rpm = eng.w * RPM;
  }

  autoShift(dt) {
    const p = this.p, d = this.d, g = this.gearSel;
    this.autoT -= dt;
    if (this.autoT > 0 || g < 1) return;
    const thr = this.ctl.throttle, perRatio = Math.abs(this.frontOmega()) * p.finalDrive * RPM;
    const upAt = lerp(2500, Math.min(p.autoShiftRpm, p.limiterRpm - 150), pow(thr, 1.4)), now = perRatio * d.ratios[g + 1];
    if (g < 5 && now > upAt && this.clutchLocked) { if (this.requestShift(g + 1)) this.autoT = 0.55; return; }
    if (g > 1) {
      const down = perRatio * d.ratios[g];
      const kick = thr > 0.92 && down < p.limiterRpm * 0.8 && now < p.limiterRpm * 0.55;
      // foot hard down a long way under the power: straight to the gear that pulls, not one gear at a time
      if (kick && g > 2 && perRatio * d.ratios[g - 1] < p.limiterRpm * 0.7) { if (this.requestShift(g - 2)) this.autoT = 0.55; return; }
      if ((now < lerp(1250, 2500, thr) && down < upAt - 450) || kick) { if (this.requestShift(g - 1)) this.autoT = 0.55; }
    }
  }

  // Help for hand input (keys or a stick). Scripted drives do not use it. s is the driver's input (-1..1, + left),
  // analog says it comes from a stick. The hands keep their own idea of the wheel angle they want (this.hand):
  // full input asks only for the lock that is still useful at this speed, the front tyres are not steered far past
  // peak slip, with the input released in a slide the wheels follow the direction of travel, and the angle moves
  // no faster than builds cornering force at a set rate (quicker when unwinding or catching a slide).
  // The car's own steering then follows a command late, so the hands lead it: the command returned asks for more
  // than is wanted by handLead times the gap between what is wanted and where the wheels are.
  handSteer(s, analog, dt) {
    const p = this.p, d = this.d, R = this.R, v = this.vel, w = this.w;
    // velocity of the front axle centre in the car frame
    const rx = R[6] * d.a, ry = R[7] * d.a, rz = R[8] * d.a;
    const fx = v[0] + (w[1] * rz - w[2] * ry), fy = v[1] + (w[2] * rx - w[0] * rz), fz = v[2] + (w[0] * ry - w[1] * rx);
    const fwd = fx * R[6] + fy * R[7] + fz * R[8], lat = fx * R[0] + fy * R[1] + fz * R[2];
    const lock = d.lock, win = p.slipWindow * p.peakSlipAngle * DEG, blend = smoothstep(3, 9, fwd);
    const v2 = Math.max(fwd * fwd, 1), K = 0.0028;
    // lock that is still useful at this speed: geometry for about 1 g plus the slip window
    const useful = p.steerReach >= 0.5 ? lerp(lock, clamp(atan(d.L * 9.5 / v2) + win, 5 * DEG, lock), blend) : lock;
    this.usefulLock = useful;
    let target = s * useful;
    const betaF = atan2(lat, Math.max(fwd, 0.5));
    this.betaF = betaF;
    if (blend > 0) {
      let tl;
      if (Math.abs(s) < 0.02) { const e = Math.abs(betaF) - 2.5 * DEG; tl = e > 0 ? sign(betaF) * e * p.selfAlign : 0; }
      else tl = clamp(target, betaF - win, betaF + win);
      target = lerp(target, clamp(tl, -lock, lock), blend);
    }
    let rate = p.steerOnset * G * d.L * (1 + K * v2) / v2;                    // rad/s for the chosen lateral-g onset
    const slide = smoothstep(3 * DEG, 10 * DEG, Math.abs(this.bodySlip));
    if (target * this.hand < 0 || Math.abs(target) < Math.abs(this.hand)) rate *= 2.2;   // unwinding is quicker than winding on
    rate *= 1 + 3 * slide;                                                     // and catching a slide quicker still
    if (analog) rate *= 2.5;
    rate = clamp(rate, 9 * DEG, 190 * DEG);
    this.hand = approach(this.hand, target, rate * dt);
    const ask = this.hand / lock, sN = this.steerN;
    // never lead by more than brings the wheels onto the wanted angle within one step (no overshoot)
    const gain = 1 - exp(-(sN === 0 || (ask - sN) * sN > 0 ? p.steerSpeed : p.steerReturn) * dt), lead = Math.min(p.handLead, 1 / gain - 1);
    return clamp(ask + (ask - sN) * lead, -1, 1);
  }

  // The car's own steering smoothing, applied to every input (keys, controller and scripts alike): the road wheels
  // follow the command with a first-order response, quicker toward lock than back toward centre, and never faster
  // than steerRateMax. Then the angle is split onto the two front wheels (Ackermann).
  updateSteering(dt) {
    const p = this.p, d = this.d, cmd = clamp(this.ctl.steer, -1, 1);
    let s = this.steerN;
    // moving toward centre (also on the way through it to the other side) follows the return speed;
    // winding lock on follows the steering speed and is capped at the fastest steering movement
    const away = s === 0 || (cmd - s) * s > 0;
    let ds = (cmd - s) * (1 - exp(-(away ? p.steerSpeed : p.steerReturn) * dt));
    if (away) { const cap = p.steerRateMax * dt; if (ds > cap) ds = cap; else if (ds < -cap) ds = -cap; }
    else if ((s + ds) * s < 0) ds = -s;                                   // do not overshoot centre inside one step
    s += ds; if (Math.abs(s) < 1e-9 && cmd === 0) s = 0;
    this.steerN = s; this.steer = s * d.lock;
    // Ackermann split onto the two front wheels, plus any pull from crash damage.
    const st = this.steer, a = Math.abs(st), ws = this.wheels;
    let inn = a, out = a;
    if (a > 1e-4) { const Rt = d.L / tan(a), k = p.ackermann / 100; inn = lerp(a, atan(d.L / (Rt - p.trackF / 2)), k); out = lerp(a, atan(d.L / (Rt + p.trackF / 2)), k); }
    ws[0].steer = (st > 0 ? inn : -out) + this.steerBias; ws[1].steer = (st > 0 ? out : -inn) + this.steerBias;
  }

  // Driver aids. "Mild" is the default since round three; "none" leaves the bare car.
  //  - traction control trims the throttle when a driven wheel spins up;
  //  - anti-lock eases the brake on a wheel that is about to lock, so the tyres stay near their peak grip and the
  //    front ones still steer. It stands back in a big slide, where a locked wheel stops the car soonest;
  //  - a stability nudge brakes one wheel when an axle slides well past its peak. A pulled handbrake is the driver
  //    asking for a slide, so the nudge waits until that slide is over.
  updateAssists(dt) {
    const p = this.p, d = this.d, ws = this.wheels, e = this.esc, ab = this.abs;
    if (!this.assists) { this.tc = 0; this.escCut = 0; e[0] = e[1] = e[2] = e[3] = 0; ab[0] = ab[1] = ab[2] = ab[3] = 1; this.tcActive = this.escActive = this.absActive = 0; this.hbT = 0; return; }
    // traction control: trim the throttle when a driven wheel spins up
    const k = Math.max(ws[0].kap, ws[1].kap), tcT = clamp((k - p.peakSlipRatio * p.tcSlip) / 0.32, 0, p.tcCut);
    this.tc += (tcT - this.tc) * Math.min(1, dt * (tcT > this.tc ? 22 : 9));
    this.tcActive = this.tc > 0.05 ? 1 : 0;
    // anti-lock: each wheel gets less of the brake the further its slip runs past the slip it should hold
    this.absActive = 0;
    const hold = p.peakSlipRatio * p.absSlip, band = p.peakSlipRatio * p.absBand, straight = 1 - smoothstep(p.absAngle * DEG, p.absAngle * 1.6 * DEG, Math.abs(this.bodySlip));
    for (let i = 0; i < 4; i++) {
      const W = ws[i]; let t = 1;
      if (straight > 0 && this.brk > 0.02 && W.onGround && Math.abs(W.vlong) > 1.5) {
        const slip = W.vlong > 0 ? -W.kap : W.kap;                       // how much slower than the road the tyre is turning
        if (slip > hold) { t = lerp(1, clamp(1 - (slip - hold) / band, 0.03, 1), straight); this.absActive = 1; }
      }
      ab[i] += (t - ab[i]) * Math.min(1, dt * (t < ab[i] ? 90 : 16));
    }
    // the handbrake asks for a slide: no stability nudge until a moment after it is let go
    if (this.hbk > 0.08) this.hbT = p.escHold; else if (this.hbT > 0) this.hbT -= dt;
    // stability: brake one wheel to pull the car straight when an axle is well past its peak slip
    let cut = 0; e[0] = e[1] = e[2] = e[3] = 0; this.escActive = 0;
    if (this.speed > 7 && this.hbT <= 0 && p.escGain > 0) {
      const R = this.R, v = this.vel;
      const yr = this.yawRate, vlatR = (v[0] * R[0] + v[1] * R[1] + v[2] * R[2]) - yr * d.b;
      const aR = atan2(-vlatR, this.speed), lim = p.peakSlipAngle * DEG;
      const over = Math.abs(aR) - lim * 0.85;
      if (over > 0) {   // rear sliding: brake the outside front wheel
        const outer = aR > 0 ? 1 : 0;   // rear slip to the left of travel = car rotating left = outside wheel is the right one
        e[outer] = Math.min(900, over * 9000) * p.escGain; cut = Math.min(0.5, over * 4 * p.escGain); this.escActive = 1;
      } else {
        const aF = Math.abs(atan(ws[0].tana) + atan(ws[1].tana)) * 0.5;
        if (aF > lim * 1.15 && Math.abs(this.steer) > 2 * DEG) { const inner = this.steer > 0 ? 2 : 3; e[inner] = Math.min(350, (aF - lim * 1.15) * 5000) * p.escGain; cut = Math.min(0.35, (aF - lim * 1.15) * 3 * p.escGain); this.escActive = 1; }
      }
    }
    this.escCut += (cut - this.escCut) * Math.min(1, dt * 12);
  }

  substep(dt, ratio) {
    const p = this.p, d = this.d, g = this.g, pos = this.pos, vel = this.vel, w = this.w, ws = this.wheels, eng = this.eng, P = this._pen;
    this.updateAxes();
    const R = this.R, axx = R[0], axy = R[1], axz = R[2], ayx = R[3], ayy = R[4], ayz = R[5], azx = R[6], azy = R[7], azz = R[8];
    let Fx = 0, Fy = -d.m * G, Fz = 0, Tx = 0, Ty = 0, Tz = 0;
    // aerodynamic drag and a little lift
    const sp = hypot3(vel[0], vel[1], vel[2]), vf = vel[0] * azx + vel[1] * azy + vel[2] * azz;
    const kd = 0.5 * RHO_AIR * p.cdA * sp; Fx -= kd * vel[0]; Fy -= kd * vel[1]; Fz -= kd * vel[2];
    Fy += 0.5 * RHO_AIR * p.liftA * vf * vf;
    const wet = g.wet(), R0 = p.tyreRadius, upright = ayy > 0.35;
    const B = wet ? d.Bwet : d.Bdry, C = wet ? p.wetShapeC : p.shapeC, E = p.shapeE;
    const baseGrip = wet === 0 ? 1 : wet === 1 ? p.wetGrip : p.heavyGrip, hbGrip = 1 - (1 - p.handbrakeGrip) * this.hbk, hbDrag = 1 - (1 - p.handbrakeDrag) * this.hbk;
    ws[0].sPrev = ws[0].s; ws[1].sPrev = ws[1].s; ws[2].sPrev = ws[2].s; ws[3].sPrev = ws[3].s;

    for (let i = 0; i < 4; i++) {
      const W = ws[i], lx = W.lx, lz = W.lz, ly = W.ly0 + W.s;
      const rx = axx * lx + ayx * ly + azx * lz, ry = axy * lx + ayy * ly + azy * lz, rz = axz * lx + ayz * ly + azz * lz;
      const cx = pos[0] + rx, cy = pos[1] + ry, cz = pos[2] + rz;
      W.cx = cx; W.cy = cy; W.cz = cz;
      const vpx = vel[0] + (w[1] * rz - w[2] * ry), vpy = vel[1] + (w[2] * rx - w[0] * rz), vpz = vel[2] + (w[0] * ry - w[1] * rx);
      const vMount = vpx * ayx + vpy * ayy + vpz * ayz;
      const cs = cos(W.steer), sn = sin(W.steer);
      const fwx = axx * sn + azx * cs, fwy = axy * sn + azy * cs, fwz = axz * sn + azz * cs;
      const hl = hypot(fwx, fwz);
      let defl = 0, nx = 0, ny = 1, nz = 0, fhx = 0, fhz = 1;
      if (upright && hl > 0.2) {
        fhx = fwx / hl; fhz = fwz / hl;
        // The tyre as a rigid disc rolling over the ground profile: deepest penetration of seven samples.
        let best = -1e9, bj = 3;
        for (let j = 0; j < 7; j++) { const dd = DISC[j], pen = g.y(cx + fhx * dd, cz + fhz * dd) - (cy - d.SQ[j]); P[j] = pen; if (pen > best) { best = pen; bj = j; } }
        let ds = DISC[bj];
        if (bj > 0 && bj < 6) { const a = P[bj - 1], b = P[bj], c2 = P[bj + 1], den = a - 2 * b + c2; if (den < -1e-9) { const off = clamp(0.5 * (a - c2) / den, -0.5, 0.5); ds += off * 0.08; best = b - 0.25 * (a - c2) * off; } }
        if (best > 0) {
          defl = best;
          const sq = Math.sqrt(Math.max(1e-6, R0 * R0 - ds * ds));
          nx = -fhx * ds / R0; ny = sq / R0; nz = -fhz * ds / R0;
          const lat = -g.slopeZ(cz) * -fhx;     // side slope: terrain normal (0,1,-dH/dz) projected on the wheel's side axis (fhz,0,-fhx)
          nx += lat * fhz; nz += lat * -fhx;
          const nl = 1 / hypot3(nx, ny, nz); nx *= nl; ny *= nl; nz *= nl;
        }
      }
      const ddefl = (defl - W.defl) / dt; W.defl = defl;
      let Ft = defl > 0 ? p.tyreRate * defl + 450 * ddefl : 0;
      if (Ft < 0) Ft = 0; else if (Ft > 32000) Ft = 32000;

      // ---- suspension: spring, bump stop, droop stop, damper, anti-roll bar
      const sdot = W.u - vMount; W.sdot = sdot;
      let Fs = W.F0 + (W.front ? p.springF : p.springR) * W.s;
      const over = W.s - p.bumpTravel; if (over > 0) Fs += p.bumpStopRate * over * (1 + over * 45);
      const under = -p.droopTravel - W.s; if (under > 0) Fs -= 160000 * under;
      const cb = W.front ? p.bumpF : p.bumpR, cr = W.front ? p.reboundF : p.reboundR;
      let Fd = sdot > 0 ? cb * sdot : cr * sdot;
      if (sdot > 1) Fd = cb * (1 + 0.4 * (sdot - 1)); else if (sdot < -1) Fd = -cr * (1 - 0.4 * (sdot + 1));   // dampers blow off at high shaft speed
      Fs += Fd + (W.front ? p.arbF : p.arbR) * (W.sPrev - ws[i ^ 1].sPrev);
      const nAy = nx * ayx + ny * ayy + nz * ayz;
      // hub: its own mass between the tyre spring and the suspension
      W.u += dt * (Ft * nAy - Fs) / (W.front ? p.unsprungF : p.unsprungR);
      W.s += dt * (W.u - vMount);
      const sMax = p.bumpTravel + 0.04, sMin = -p.droopTravel - 0.025;
      if (W.s > sMax) { W.s = sMax; if (W.u > vMount) W.u = vMount; if (Ft * nAy > Fs) Fs = Ft * nAy; }
      else if (W.s < sMin) { W.s = sMin; if (W.u < vMount) W.u = vMount; }
      if (Math.abs(sdot) > this.kerbHit) this.kerbHit = Math.abs(sdot);

      // force on the body: suspension along the strut, plus the part of the tyre normal force the strut cannot take
      let bx = ayx * Fs, by = ayy * Fs, bz = ayz * Fs;
      if (Ft > 0) { bx += Ft * (nx - nAy * ayx); by += Ft * (ny - nAy * ayy); bz += Ft * (nz - nAy * ayz); }
      Fx += bx; Fy += by; Fz += bz;
      Tx += ry * bz - rz * by; Ty += rz * bx - rx * bz; Tz += rx * by - ry * bx;

      // ---- tyre forces in the contact patch
      W.Fz = Ft; W.onGround = Ft > 0; W.tq = 0; W.a = dt / p.wheelInertia;
      if (Ft > 0) {
        const rl = R0 - defl, rcx = rx - nx * rl, rcy = ry - ny * rl, rcz = rz - nz * rl;
        const vcx = vel[0] + (w[1] * rcz - w[2] * rcy), vcy = vel[1] + (w[2] * rcx - w[0] * rcz), vcz = vel[2] + (w[0] * rcy - w[1] * rcx);
        const fd = fwx * nx + fwy * ny + fwz * nz;
        let tfx = fwx - nx * fd, tfy = fwy - ny * fd, tfz = fwz - nz * fd; const tl = 1 / hypot3(tfx, tfy, tfz); tfx *= tl; tfy *= tl; tfz *= tl;
        const tsx = ny * tfz - nz * tfy, tsy = nz * tfx - nx * tfz, tsz = nx * tfy - ny * tfx;
        const vlong = vcx * tfx + vcy * tfy + vcz * tfz, vlat = vcx * tsx + vcy * tsy + vcz * tsz, av = Math.abs(vlong);
        const Re = R0 - defl * 0.35, vsx = W.omega * Re - vlong;
        // Slip builds up over a relaxation length. Near standstill (ground speed and wheel speed both under about
        // 0.25 m/s) what a tyre stores is only its elastic give: the stored slip is held to its value at peak grip
        // and the relaxation length is cut short. Without this a wheel locked to a stop keeps the slip it had while
        // sliding, and that pushes the stopped car back by a hand's width before it comes to rest. What is left
        // after a hard stop is the body rocking back on its springs, about 3 cm at the centre of mass.
        const vq = Math.max(hypot(vlong, vlat), Math.abs(W.omega) * Re), low = 1 - smoothstep(0.04, 0.25, vq), cut = 1 - 0.85 * low;
        const kLim = KMAX - (KMAX - p.peakSlipRatio) * low, tLim = TMAX - (TMAX - d.tanAp) * low;
        // Lengthways slip is measured against the speed of the road under the tyre in any direction, not only along
        // the wheel. For a rolling tyre the two are the same. For a car sliding sideways with its wheels locked the
        // old measure froze as the car swung through broadside, and the tyres pushed the wrong way for a moment.
        W.kap += dt * (vsx - hypot(vlong, vlat) * W.kap) / (p.relaxLong * cut); if (W.kap > kLim) W.kap = kLim; else if (W.kap < -kLim) W.kap = -kLim;
        W.tana += dt * (-vlat - av * W.tana) / (p.relaxLat * cut); if (W.tana > tLim) W.tana = tLim; else if (W.tana < -tLim) W.tana = -tLim;
        // grip available here: weather, surface, standing water, load sensitivity
        const type = g.type(cx, cz), pud = type === SURF.PAVEMENT ? 0 : g.puddle(cx, cz);
        let mu = baseGrip * (type === SURF.COBBLE ? p.cobbleGrip * (wet ? 0.9 : 1) : type === SURF.PAVEMENT ? 0.93 : 1);
        if (pud > 0) mu *= 1 - pud * p.puddleLoss * (0.55 + 0.9 * clamp01(sp / 30));
        mu *= clamp(1 - p.loadSens * (Ft / p.nominalLoad - 1), 0.6, 1.25);
        W.surf = type; W.puddle = pud; W.grip = mu;
        const sxn = W.kap / p.peakSlipRatio, syn = W.tana / d.tanAp, rho = hypot(sxn, syn);
        let Fxt = 0, Fyt = 0;
        // A rolling tyre grips less sideways than lengthways (muLat against muLong). A wheel that is locked while the
        // road slides under it is just a block of rubber: it grips the same in every direction (lockGrip = 1).
        const lock = p.lockGrip > 0 ? p.lockGrip * (1 - clamp01(Math.abs(W.omega) * Re / (0.25 * hypot(vlong, vlat) + 0.3))) : 0;
        const muY = p.muLat + (p.muLong - p.muLat) * lock;
        if (rho > 1e-7) { const x = B * rho, f = Ft * mu * sin(C * atan(x - E * (x - atan(x)))) / rho; Fxt = p.muLong * f * sxn; Fyt = muY * f * syn; }
        if (i > 1 && this.hbk > 0) { Fyt *= hbGrip; Fxt *= hbDrag; }        // handbrake on: the rear tyres keep only part of their grip, sideways and lengthways
        // near standstill the slip definitions lose meaning: add velocity damping so the car settles and holds on a slope
        const ls = 1 - smoothstep(1.2, 4.5, av);
        if (ls > 0) {
          let dxf = 9000 * vsx * ls, dyf = -9000 * vlat * ls;
          Fxt += dxf; Fyt += dyf;
          const lim = mu * Ft, mag = hypot(Fxt / p.muLong, Fyt / muY);
          if (mag > lim) { const k = lim / mag; Fxt *= k; Fyt *= k; } else W.a = dt / (p.wheelInertia + dt * 9000 * ls * Re * Re);
        }
        // rolling resistance and the drag of standing water act on the car, not through wheel torque
        const drag = (p.rollRes * (type === SURF.COBBLE ? 1.6 : 1) * Ft + pud * 0.55 * vlong * vlong) * clamp(vlong * 2, -1, 1);
        const flx = Fxt - drag;
        const cfx = tfx * flx + tsx * Fyt, cfy = tfy * flx + tsy * Fyt, cfz = tfz * flx + tsz * Fyt;
        Fx += cfx; Fy += cfy; Fz += cfz;
        Tx += rcy * cfz - rcz * cfy; Ty += rcz * cfx - rcx * cfz; Tz += rcx * cfy - rcy * cfx;
        W.tq = -Fxt * Re; W.Fx = Fxt; W.Fy = Fyt; W.vlong = vlong; W.vlat = vlat; W.rho = rho;
        W.slipAngle = atan(W.tana); W.slipRatio = W.kap;
        W.use = hypot(Fxt / p.muLong, Fyt / muY) / (mu * Ft);            // the share of this tyre's grip in use (the squeal listens to it)
      } else { W.kap *= 0.92; W.tana *= 0.92; W.Fx = W.Fy = 0; W.rho = 0; W.slipAngle = 0; W.slipRatio = 0; W.puddle = 0; W.use = 0; }
    }

    // ---- driveline: engine, clutch (implicit stick-slip), gearbox, open front differential
    const rpm = eng.w * RPM, Te = this.engineTorque(rpm, this.thrEff);
    eng.torque = Te;
    const w0 = ws[0], w1 = ws[1], ae = dt / p.engineInertia;
    let o0 = w0.omega + w0.a * w0.tq, o1 = w1.omega + w1.a * w1.tq, wE = eng.w + ae * Te;
    if (ratio !== 0 && this.clutch > 0.001) {
      const K = ae + p.driveEff * ratio * ratio * (w0.a + w1.a) * 0.25, cap = p.clutchTorque * this.clutch;
      const Tc = clamp((wE - ratio * (o0 + o1) * 0.5) / K, -cap, cap);
      wE -= ae * Tc; const tw = p.driveEff * ratio * Tc * 0.5; o0 += w0.a * tw; o1 += w1.a * tw;
      this.clutchTq = Tc;
    } else this.clutchTq = 0;
    eng.w = wE < 40 ? 40 : wE;
    w0.omega = o0; w1.omega = o1; ws[2].omega += ws[2].a * ws[2].tq; ws[3].omega += ws[3].a * ws[3].tq;
    for (let i = 0; i < 4; i++) {
      const W = ws[i], dw = W.a * W.brakeT;
      if (dw > 0) { if (Math.abs(W.omega) <= dw) W.omega = 0; else W.omega -= sign(W.omega) * dw; }
      W.ang += W.omega * dt;
    }

    // ---- integrate the body
    vel[0] += dt * Fx * d.invM; vel[1] += dt * Fy * d.invM; vel[2] += dt * Fz * d.invM;
    const Ix = p.inertiaPitch, Iy = p.inertiaYaw, Iz = p.inertiaRoll;
    let wbx = w[0] * axx + w[1] * axy + w[2] * axz, wby = w[0] * ayx + w[1] * ayy + w[2] * ayz, wbz = w[0] * azx + w[1] * azy + w[2] * azz;
    const tbx = Tx * axx + Ty * axy + Tz * axz, tby = Tx * ayx + Ty * ayy + Tz * ayz, tbz = Tx * azx + Ty * azy + Tz * azz;
    const gx = wby * wbz * (Iz - Iy), gy = wbz * wbx * (Ix - Iz), gz = wbx * wby * (Iy - Ix);
    wbx += dt * (tbx - gx) / Ix; wby += dt * (tby - gy) / Iy; wbz += dt * (tbz - gz) / Iz;
    w[0] = axx * wbx + ayx * wby + azx * wbz; w[1] = axy * wbx + ayy * wby + azy * wbz; w[2] = axz * wbx + ayz * wby + azz * wbz;
    pos[0] += vel[0] * dt; pos[1] += vel[1] * dt; pos[2] += vel[2] * dt;
    const q = this.q, hx = w[0] * dt * 0.5, hy = w[1] * dt * 0.5, hz = w[2] * dt * 0.5, qx = q[0], qy = q[1], qz = q[2], qw = q[3];
    let nqx = qx + hx * qw + hy * qz - hz * qy, nqy = qy + hy * qw + hz * qx - hx * qz, nqz = qz + hz * qw + hx * qy - hy * qx, nqw = qw - hx * qx - hy * qy - hz * qz;
    const ql = 1 / hypot4(nqx, nqy, nqz, nqw); q[0] = nqx * ql; q[1] = nqy * ql; q[2] = nqz * ql; q[3] = nqw * ql;
  }

  // ---- impulses (collisions) -------------------------------------------------------------
  // Effective inverse mass at offset r (from the centre of mass) along unit direction n.
  invMassAt(rx, ry, rz, nx, ny, nz) {
    const R = this.R, p = this.p;
    const cx = ry * nz - rz * ny, cy = rz * nx - rx * nz, cz = rx * ny - ry * nx;
    const bx = cx * R[0] + cy * R[1] + cz * R[2], by = cx * R[3] + cy * R[4] + cz * R[5], bz = cx * R[6] + cy * R[7] + cz * R[8];
    return this.d.invM + bx * bx / p.inertiaPitch + by * by / p.inertiaYaw + bz * bz / p.inertiaRoll;
  }
  applyImpulse(rx, ry, rz, jx, jy, jz) {
    const R = this.R, p = this.p, v = this.vel, w = this.w, im = this.d.invM;
    v[0] += jx * im; v[1] += jy * im; v[2] += jz * im;
    const lx = ry * jz - rz * jy, ly = rz * jx - rx * jz, lz = rx * jy - ry * jx;
    const bx = (lx * R[0] + ly * R[1] + lz * R[2]) / p.inertiaPitch, by = (lx * R[3] + ly * R[4] + lz * R[5]) / p.inertiaYaw, bz = (lx * R[6] + ly * R[7] + lz * R[8]) / p.inertiaRoll;
    w[0] += R[0] * bx + R[3] * by + R[6] * bz; w[1] += R[1] * bx + R[4] * by + R[7] * bz; w[2] += R[2] * bx + R[5] * by + R[8] * bz;
  }
  pointVel(rx, ry, rz, out) { const v = this.vel, w = this.w; out[0] = v[0] + (w[1] * rz - w[2] * ry); out[1] = v[1] + (w[2] * rx - w[0] * rz); out[2] = v[2] + (w[0] * ry - w[1] * rx); return out; }

  // Body shell against the ground: only matters when the car bottoms out, lands badly or rolls over.
  groundContacts(dt) {
    const d = this.d, g = this.g, pos = this.pos, pv = this._pv;
    this.updateAxes(); const R = this.R;
    let hit = 0;
    for (let k = 0; k < d.hull.length; k++) {
      const h = d.hull[k];
      const rx = R[0] * h[0] + R[3] * h[1] + R[6] * h[2], ry = R[1] * h[0] + R[4] * h[1] + R[7] * h[2], rz = R[2] * h[0] + R[5] * h[1] + R[8] * h[2];
      const px = pos[0] + rx, py = pos[1] + ry, pz = pos[2] + rz;
      const pen = g.y(px, pz) - py;
      if (pen <= 0) continue;
      const sl = g.slopeZ(pz), nl = 1 / hypot(1, sl), nx = 0, ny = nl, nz = -sl * nl;
      this.pointVel(rx, ry, rz, pv);
      const vn = pv[0] * nx + pv[1] * ny + pv[2] * nz, bias = Math.min(pen, 0.2) * 0.25 / dt;
      if (vn > bias) continue;
      const jn = (bias - vn) / this.invMassAt(rx, ry, rz, nx, ny, nz);
      this.applyImpulse(rx, ry, rz, nx * jn, ny * jn, nz * jn);
      let tx = pv[0] - vn * nx, ty = pv[1] - vn * ny, tz = pv[2] - vn * nz; const tl = hypot3(tx, ty, tz);
      if (tl > 0.05) { tx /= tl; ty /= tl; tz /= tl; const jt = Math.min(0.55 * jn, tl / this.invMassAt(rx, ry, rz, tx, ty, tz)); this.applyImpulse(rx, ry, rz, -tx * jt, -ty * jt, -tz * jt); }
      if (jn > hit) hit = jn;
    }
    this.groundHit = hit;
  }
}
