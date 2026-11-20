// Third-person chase camera on a sprung arm. No other view exists: the game this feeds is third person only.
//
// The camera has two halves. step() is the camera's own motion and runs once per physics step with the fixed
// 1/120 s, so the same drive gives the same camera numbers on every run: an arm that swings behind the
// direction of travel (so the camera lags a turn a little), a look that leans into the corner, a position that
// follows its place on that arm late (the lag), a height above the road, and a horizontal field of view that
// opens with speed. apply() draws it: it blends the last two steps for a smooth picture and adds shake from
// speed, rough ground and impacts, which is cosmetic and never reaches telemetry.
//
// It follows anything with a position, a heading and a speed: the car, or the person on foot.
import { clamp, clamp01, lerp, angDiff, smoothstep, vnoise, MPH } from './util.js';
import { atan, cos, exp, sin, tan } from './dmath.js';

// Views. 0: the chase view. 1 (key C): the same camera closer and lower. FOOT: behind the person on foot.
// Factors on the tuning settings; fov is added in degrees.
const VIEWS = [{ dist: 1, height: 1, fov: 0, lookH: 0.95, swing: 1 }, { dist: 0.66, height: 0.62, fov: 6, lookH: 0.82, swing: 1.3 }];
const FOOT = { dist: 0.74, height: 1.2, fov: 0, lookH: 1.02, swing: 1.5 }, VW = { dist: 1, height: 1, fov: 0, lookH: 1, swing: 1 };
// Vertical field of view for the renderer from a horizontal one. On a screen much taller than wide the lens
// stops at 100 degrees, so a phone held upright shows a little less width than the setting says.
export const verticalFov = (hfov, aspect) => Math.min(100, 2 * atan(tan(hfov * Math.PI / 360) / aspect) * 180 / Math.PI);
// Fixed vertical lens for the menu's orbit view, widened on a tall, narrow screen.
export const fitFov = (fov, aspect) => (aspect >= 1.3 ? fov : Math.min(104, 2 * atan(tan(fov * Math.PI / 360) * 1.3 / aspect) * 180 / Math.PI));

const PUSH = [0, 0];
const FREE_HOLD = 1.5;     // seconds without the right stick before the free look swings back behind the car
const SHAKE_FROM = 50, SHAKE_FULL = 95;   // mph: the light speed shake starts at the first and is whole at the second

export class ChaseCam {
  // p: the tuning settings (camDist, camHeight, camLag, camFovRest, camFovSpeed, camFovMph, camFovRate, camSwing).
  // world: { base(x, z): road height, ground(x, z): height with kerbs,
  //          blocked(ax, az, bx, bz): how far along the line from a to b something solid is, 0..1, or -1 }.
  constructor(p, world) {
    this.p = p; this.world = world; this.mode = 0; this.footK = 0; this.shake = true;      // footK: 0 following the car .. 1 following the person on foot
    this.yaw = 0; this.yawV = 0; this.look = 0; this.back = 0; this.clip = 1; this.kick = 0; this.fov = p.camFovRest;
    this.free = 0; this.freeP = 0; this.idle = 9;                        // free look: yaw and pitch offsets, time since the stick moved
    this.px = 0; this.py = 0; this.pz = 0; this.ty = 0;                  // camera position after the last step, and the height it looks at
    this.q = { x: 0, y: 0, z: 0, fov: 0, yaw: 0, look: 0, back: 0, ty: 0, freeP: 0 };   // the same after the step before, for drawing
    this.rough = 0; this.t = 0; this.roll = 0; this.vel = { x: 0, y: 0, z: 0 }; this.fwd = { x: 0, y: 0, z: 1 }; this.lx = 0; this.ly = 0; this.lz = 0; this.drawn = false;
  }
  // the view in use: the chase view, or a blend of it and the on-foot view while someone gets in or out
  get view() {
    const a = VIEWS[this.mode], k = this.footK; if (!(k > 0)) return a;
    VW.dist = lerp(a.dist, FOOT.dist, k); VW.height = lerp(a.height, FOOT.height, k); VW.fov = lerp(a.fov, FOOT.fov, k); VW.lookH = lerp(a.lookH, FOOT.lookH, k); VW.swing = lerp(a.swing, FOOT.swing, k); return VW;
  }
  // Rest pose straight behind the car (or the person). Every scripted drive starts from this.
  reset(veh) {
    const p = this.p, V = this.view, h = veh.heading, x = veh.pos[0], z = veh.pos[2];
    this.yaw = h; this.yawV = 0; this.look = 0; this.back = 0; this.clip = 1; this.kick = 0; this.free = 0; this.freeP = 0; this.idle = 9;
    this.fov = p.camFovRest + V.fov;
    this.px = x - sin(h) * p.camDist * V.dist; this.pz = z - cos(h) * p.camDist * V.dist;
    this.py = Math.max(this.world.ground(this.px, this.pz) + 0.5, this.world.base(x, z) + p.camHeight * V.height);
    this.ty = this.world.base(x, z) + V.lookH;
    this.save(); this.drawn = false; this.roll = 0; this.rough = 0;
  }
  save() { const q = this.q; q.x = this.px; q.y = this.py; q.z = this.pz; q.fov = this.fov; q.yaw = this.yaw + this.free; q.look = this.look; q.back = this.back; q.ty = this.ty; q.freeP = this.freeP; }

  // One fixed step. veh: what the camera follows, after its own step. lookBack: the look-behind button is held.
  // lookX, lookY: the right stick (-1..1), for the free look. Scripted drives pass none of these.
  step(dt, veh, lookBack, lookX = 0, lookY = 0) {
    const p = this.p, V = this.view, W = this.world, sp = Math.abs(veh.speed);
    this.save();
    // the arm swings to sit behind the direction of travel, a little wide of the nose in a slide. Because it is a
    // sprung arm, the camera trails a turn slightly instead of being bolted to the car.
    const slip = clamp(veh.bodySlip, -0.7, 0.7) * smoothstep(2, 8, sp) * (veh.speed < 0 ? -1 : 1);
    this.back += ((lookBack ? 1 : 0) - this.back) * Math.min(1, dt * 14);
    const err = angDiff(veh.heading + slip * 0.62, this.yaw);
    // On foot the camera swings round behind the walker, but only slowly when they walk toward it: a stick that
    // moves "where it points, seen from the camera" must not have the camera spin under it.
    const w = lerp(p.camSwing * 0.48, p.camSwing, clamp01(sp / 18)) * V.swing * (this.footK > 0 ? lerp(1, 0.22 + 0.78 * clamp01((cos(err) + 0.35) / 1.35), this.footK) : 1);
    this.yawV += (w * w * err - 2 * w * this.yawV) * dt; this.yaw += this.yawV * dt;
    // free look: the right stick swings the camera round the car; left alone for a moment, it comes back behind
    if (lookX !== 0 || lookY !== 0) { this.idle = 0; this.free = clamp(this.free - lookX * 2.6 * dt, -Math.PI, Math.PI); this.freeP = clamp(this.freeP + lookY * 1.2 * dt, -0.35, 0.5); }
    else { this.idle += dt; if (this.idle > FREE_HOLD) { const k = Math.min(1, dt * 5); this.free -= this.free * k; this.freeP -= this.freeP * k; if (Math.abs(this.free) < 1e-4) this.free = 0; if (Math.abs(this.freeP) < 1e-4) this.freeP = 0; } }
    // look into the corner: aim ahead of the car toward where it is turning
    const lk = clamp(veh.yawRate * 0.17 + veh.steer * 0.3, -0.24, 0.24) * smoothstep(1, 6, sp);
    this.look += (lk - this.look) * Math.min(1, dt * 4.5);
    // where the camera wants to be: on the arm, behind the centre of mass
    const dist = p.camDist * V.dist * lerp(1, 0.86, this.back);
    const yaw = this.yaw + this.free + this.back * Math.PI, sx = sin(yaw), sz = cos(yaw), tx = veh.pos[0], tz = veh.pos[2];
    let cx = tx - sx * dist, cz = tz - sz * dist;
    // Keep the camera out of walls, cars and posts (the world answers with a margin already added). The arm is
    // tested where it is now and where it will be a fifth of a second on, so it starts to shorten before anything
    // cuts in; it shortens quickly but as a move, not a jump, and eases back out slowly.
    const AH = 0.2, yawA = yaw + this.yawV * AH - lookX * 2.6 * AH, txA = tx + (veh.vel ? veh.vel[0] : 0) * AH, tzA = tz + (veh.vel ? veh.vel[2] : 0) * AH;
    const hit = W.blocked(tx, tz, cx, cz), hitA = W.blocked(txA, tzA, txA - sin(yawA) * dist, tzA - cos(yawA) * dist);
    const first = hit >= 0 && hitA >= 0 ? Math.min(hit, hitA) : hit >= 0 ? hit : hitA, want = first >= 0 ? clamp(first - 0.02, 0.18, 1) : 1;
    this.clip += (want - this.clip) * Math.min(1, dt * (want < this.clip ? 14 : 3));
    cx = tx - sx * dist * this.clip; cz = tz - sz * dist * this.clip;
    // position lag: the camera follows that point late, so it trails by about speed x lag. With the arm shortened by
    // something solid the lag fades out: next to a wall the camera stays on the arm's end, which is known to be clear.
    // While the arm is still being pulled in, the camera keeps up with its end: trailing it by the full lag would
    // leave the camera out where the thing that is cutting in is about to be.
    const lagT = p.camLag * smoothstep(0.55, 0.98, this.clip) * (want < this.clip - 0.004 ? 0.25 : 1), k = lagT > 0.001 ? 1 - exp(-dt / lagT) : 1;
    let nx = this.px + (cx - this.px) * k, nz = this.pz + (cz - this.pz) * k;
    if (W.push) { W.push(nx, nz, PUSH); nx = PUSH[0]; nz = PUSH[1]; }      // out of the margin of anything it has drifted beside
    // A camera that follows late cuts corners. Where that would take it through something, it follows less late:
    // it takes the place nearest its own between there and the arm's end from which the car is still in clear view.
    if (W.blocked(tx, tz, nx, nz) >= 0) {
      let lo = 0, hi = 1;
      for (let i = 0; i < 6; i++) { const m = (lo + hi) * 0.5; if (W.blocked(tx, tz, nx + (cx - nx) * m, nz + (cz - nz) * m) >= 0) lo = m; else hi = m; }
      nx += (cx - nx) * hi; nz += (cz - nz) * hi;
      // the arm's end itself is still behind something that cut in faster than the arm shortens: stop in front of it
      const h = W.blocked(tx, tz, nx, nz); if (h >= 0) { const f = Math.max(0.1, h - 0.02); nx = tx + (nx - tx) * f; nz = tz + (nz - tz) * f; }
    }
    // lamp posts and sign posts: the camera steps round them. It meets a post edge-on, so this is a nudge, not a jump.
    if (W.push) { W.push(nx, nz, PUSH); nx = PUSH[0]; nz = PUSH[1]; }
    this.px = nx; this.pz = nz;
    // height: over the road, not over the body, so kerbs and bumps under the car do not reach the camera
    // An ordinary car under the camera, or about to be: the camera sits above its roof (see camworld.js).
    const roof = W.over ? W.over(this.px, this.pz, 1.1) : 0, floorY = W.base(this.px, this.pz);
    const yT = Math.max(W.ground(this.px, this.pz) + 0.5, W.base(tx, tz) + p.camHeight * V.height + (1 - this.clip) * 0.9 + this.freeP * dist * 0.6, roof > 0 ? floorY + roof + 0.45 : -1e9);
    this.py += (yT - this.py) * Math.min(1, dt * 7);
    if (W.over) { const r0 = W.over(this.px, this.pz, 0.2); if (r0 > 0 && this.py < floorY + r0 + 0.3) this.py = floorY + r0 + 0.3; }   // a car that arrived faster than that
    // the point it looks at follows the body's height only slowly and partly: a small, damped follow
    const tyT = W.base(tx, tz) + V.lookH + clamp(veh.pos[1] - W.base(tx, tz) - (veh.rideH || 0), -0.25, 0.6) * 0.35;
    this.ty += (tyT - this.ty) * Math.min(1, dt * 3);
    // field of view (horizontal): a straight line from rest to camFovMph, plus a short punch on impacts
    this.kick *= exp(-dt * 6.5);
    const fT = p.camFovRest + (p.camFovSpeed - p.camFovRest) * clamp01(sp * MPH / p.camFovMph) + V.fov + (this.shake ? this.kick * 30 : 0);
    this.fov += (fT - this.fov) * Math.min(1, dt * p.camFovRate);
  }

  // Draw. cam3: the three.js camera. alpha: how far between the last two steps this frame falls. fdt: frame time,
  // used only for the shake and for the camera speed the rain streaks need. o: the drawn origin of what is followed.
  apply(cam3, alpha, fdt, o, veh) {
    const q = this.q, sp = Math.abs(veh.speed);
    this.t += fdt;
    const x = lerp(q.x, this.px, alpha), y = lerp(q.y, this.py, alpha), z = lerp(q.z, this.pz, alpha), ty = lerp(q.ty, this.ty, alpha);
    const back = lerp(q.back, this.back, alpha), yaw = lerp(q.yaw, this.yaw + this.free, alpha) + back * Math.PI, look = lerp(q.look, this.look, alpha), freeP = lerp(q.freeP, this.freeP, alpha);
    // shake rotates the view a little rather than moving it: rough ground, impacts, and a light tremor at speed
    let r = 0; const ws = veh.wheels || [];
    for (const W of ws) r += Math.min(1.5, Math.abs(W.sdot)); r = r * 0.25 + (ws.length && ws[0].surf === 2 ? 0.25 * clamp01(sp / 12) : 0);
    this.rough += (r - this.rough) * Math.min(1, fdt * (r > this.rough ? 20 : 5));
    const speedShake = smoothstep(SHAKE_FROM, SHAKE_FULL, sp * MPH) * 0.0042;
    const amp = this.shake ? clamp(this.rough * 0.011 + this.kick + speedShake, 0, 0.06) : 0;
    const n1 = vnoise(this.t * 31, 1.7) - 0.5, n2 = vnoise(this.t * 37, 9.2) - 0.5, n3 = vnoise(this.t * 29, 4.4) - 0.5;
    const fv = verticalFov(lerp(q.fov, this.fov, alpha), cam3.aspect); if (Math.abs(cam3.fov - fv) > 0.005) { cam3.fov = fv; cam3.updateProjectionMatrix(); }
    const nx = x, ny = y + n2 * amp * 1.5, nz = z;
    if (fdt > 0 && this.drawn) { this.vel.x = (nx - this.lx) / fdt; this.vel.y = (ny - this.ly) / fdt; this.vel.z = (nz - this.lz) / fdt; } else { this.vel.x = this.vel.y = this.vel.z = 0; }
    this.lx = nx; this.ly = ny; this.lz = nz; this.drawn = true;
    cam3.position.set(nx, ny, nz);
    const a = yaw + look * (1 - 2 * back), lx = sin(a), lz = cos(a);
    cam3.up.set(0, 1, 0); cam3.lookAt(o[0] + lx * 2.2 + n1 * amp * 6, ty - freeP * 1.2 + n3 * amp * 5, o[2] + lz * 2.2);
    this.roll += (clamp((veh.accLat || 0) / 9.81, -1.2, 1.2) * -0.013 * (1 - 2 * back) - this.roll) * Math.min(1, fdt * 5);
    cam3.rotateZ(this.roll + n1 * amp * 0.6);
    this.fwd.x = lx; this.fwd.z = lz;
  }
  // A jolt sized by the impact speed (m/s).
  impact(v) { this.kick = Math.min(0.05, this.kick + v * 0.0035); }
  toggle() { this.mode = (this.mode + 1) % VIEWS.length; }
}
