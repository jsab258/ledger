// LEDGER drives the driving study's car (his ruling of 17 Nov: "His driving study tunes to the sheet; the game adopts
// it"). This is the cab and every car Tom drives: the study's round 3 vehicle (vehicle.js, params.js, collide.js,
// unchanged), stepped at its own 120 steps a second, with the study's hand-steering help, automatic gearbox, mild
// driver aids and its way of going into reverse (the brake held at a standstill). What LEDGER keeps of its own: the
// town it collides with, and the two cab fixes of 20 Nov (keys ease to lock and centre at LEDGER's rates, so the
// wheel never jerks on a release; a car that is boxed in or dead on a pole is never left stranded: drive.js).
import { G } from '../state.js';
import { RULES } from '../rules.js';
import { BLD, WALLS, PROPS, POSTS } from '../map.js';
import { Vehicle } from './vehicle.js';
import { defaultParams } from './params.js';
import { boxBox, boxCircle, resolve, M, HIT, CarProxy } from './collide.js';
import { weatherNow } from './world.js';
import { clamp, approach } from './util.js';

const DRIVING = RULES.driving;
export const STEP = 1 / 120;
const P = defaultParams();
const REST = { wall: 0.14, post: 0.08, car: 0.12 },
  FRIC = { wall: 0.42, post: 0.45, car: 0.45 };
const SOLID = BLD.concat(WALLS).map((b) => ({ cx: (b.x0 + b.x1) / 2, cz: (b.z0 + b.z1) / 2, hx: (b.x1 - b.x0) / 2, hz: (b.z1 - b.z0) / 2, x0: b.x0, x1: b.x1, z0: b.z0, z1: b.z1 }));
const sbox = { x: 0, z: 0, ux: 1, uz: 0, hu: 0, vx: 0, vz: 1, hv: 0 };

export const CAB = {
  veh: new Vehicle(P),
  proxy: null,
  acc: 0,
  k: { steer: 0, thr: 0, brk: 0, hb: 0 },
  revT: 0,
  touch: 9,
  crushV: 0,
  hits: [], // what this frame's steps met: { v: closing metres a second, kind, x, z }
  live: false,
  o: [0, 0, 0],
};
CAB.veh.auto = true;
CAB.veh.assists = 1;
CAB.proxy = new CarProxy(CAB.veh);
const move = (dx, dz) => {
  CAB.veh.pos[0] += dx;
  CAB.veh.pos[2] += dz;
};

// Put the study's car where the game's car stands (getting in, a load, a car put down somewhere by the game).
export function seat(c) {
  const v = CAB.veh;
  v.hardReset(c.x, c.z, c.ang);
  v.auto = true;
  v.assists = 1;
  CAB.k.steer = CAB.k.thr = CAB.k.brk = CAB.k.hb = 0;
  CAB.acc = 0;
  CAB.revT = 0;
  CAB.touch = 9;
  CAB.crushV = 0;
  CAB.live = true;
}
// The game's car from the study's: where the middle of the wheelbase is, the heading, the speed along the car.
export function read(c) {
  const v = CAB.veh;
  v.origin(CAB.o);
  c.x = CAB.o[0];
  c.z = CAB.o[2];
  c.ang = v.heading;
  c.v = v.speed;
}
// the study's Sim.drive: hand-steering help, and the automatic's reverse on a held brake at a standstill
function drive(inp, dt) {
  const car = CAB.veh,
    c = car.ctl;
  c.steer = car.handSteer(inp.steer, !!inp.analog, dt);
  c.handbrake = inp.handbrake || 0;
  let thr = inp.throttle,
    brk = inp.brake;
  const v = car.speed;
  if (car.gearSel === -1) {
    if (thr > 0.3 && v > -0.8) car.requestShift(1);
    else {
      const t = thr;
      thr = brk;
      brk = t;
    }
    CAB.revT = 0;
  } else {
    if (car.gearSel === 0 && car.shiftT <= 0) car.requestShift(1);
    if (brk > 0.5 && thr < 0.05 && Math.abs(v) < 0.5) {
      CAB.revT += dt;
      if (CAB.revT > 0.4) {
        car.requestShift(-1);
        CAB.revT = 0;
      }
    } else CAB.revT = 0;
  }
  c.throttle = thr;
  c.brake = brk;
}
function note(kind) {
  if (HIT.vn > 0.3) {
    if (CAB.touch > 0.2) CAB.hits.push({ v: HIT.vn, kind, x: HIT.px, z: HIT.pz });
    CAB.touch = 0;
  }
  if (HIT.vn > CAB.crushV) CAB.crushV = HIT.vn;
  CAB.touching = true;
}
// The study's collideCar, against the Hook: buildings and walls as boxes, lamp columns and street furniture as
// posts, the other cars standing or moving in the street as round bodies that do not give.
function collide(dt, traffic) {
  const px = CAB.proxy,
    cap = CAB.veh.d.m * Math.max(40 * 9.81, (CAB.crushV * CAB.crushV) / 0.9) * dt;
  let b = px.sync();
  px.yc = 0.46;
  const reb = (k) => (CAB.crushV > 2 ? REST[k] * CAB.crushV : 0);
  for (const s of SOLID) {
    if (s.x1 < b.x - 2.6 || s.x0 > b.x + 2.6 || s.z1 < b.z - 2.6 || s.z0 > b.z + 2.6) continue;
    sbox.x = s.cx;
    sbox.z = s.cz;
    sbox.hu = s.hx;
    sbox.hv = s.hz;
    if (!boxBox(b, sbox)) continue;
    resolve(px, null, REST.wall, FRIC.wall, move, null, cap, 0.012, reb('wall'));
    note('wall');
    b = px.sync();
  }
  for (const l of POSTS) {
    if (Math.abs(l.x - b.x) > 3 || Math.abs(l.z - b.z) > 3) continue;
    if (!boxCircle(b, l.x, l.z, DRIVING.lampPostRadiusMetres)) continue;
    resolve(px, null, REST.post, FRIC.post, move, null, cap, 0.012, reb('post'));
    note('post');
    b = px.sync();
  }
  for (const p of PROPS) {
    if (!p.r || Math.abs(p.x - b.x) > 5 || Math.abs(p.z - b.z) > 5) continue;
    let n;
    if (p.w) {
      sbox.x = p.x;
      sbox.z = p.z;
      sbox.hu = p.r;
      sbox.hv = p.w / 2;
      n = boxBox(b, sbox);
    } else n = boxCircle(b, p.x, p.z, p.r);
    if (!n) continue;
    resolve(px, null, REST.post, FRIC.post, move, null, cap, 0.012, reb('post'));
    note('prop');
    b = px.sync();
  }
  for (const t of traffic) {
    if (Math.abs(t.x - b.x) > 6 || Math.abs(t.z - b.z) > 6) continue;
    if (!boxCircle(b, t.x, t.z, t.r)) continue;
    resolve(px, null, REST.car, FRIC.car, move, null, cap, 0.02, CAB.crushV > 2 ? 0.1 * CAB.crushV : 0);
    note(t.parked ? 'parked' : 'car');
    b = px.sync();
  }
}
// One frame of the game: the steps the study's car is owed. inp: { kx: keys -1..1 (+ right), x: stick -1..1 (+ right),
// y: -1 brake .. 1 throttle, hb }. power: 0..1 (damage). traffic: [{x, z, r, parked}] near enough to matter.
export function stepCab(dt, inp, power, traffic) {
  const v = CAB.veh,
    k = CAB.k;
  CAB.hits.length = 0;
  weatherNow();
  v.powerScale = power;
  CAB.acc = Math.min(CAB.acc + dt, 14 * STEP);
  const stick = Math.abs(inp.x || 0) > 0.02,
    thrIn = Math.max(0, inp.y || 0),
    brkIn = Math.max(0, -(inp.y || 0)),
    analogPedals = inp.analogPedals;
  while (CAB.acc >= STEP) {
    CAB.acc -= STEP;
    // keys are not a wheel: they ease to full lock and centre themselves, at LEDGER's rates (the cab fix of 20 Nov);
    // a stick is used as it is. In the study's frame, steering is positive to the left.
    const want = -(inp.kx || 0);
    k.steer = approach(k.steer, want, STEP / (want === 0 || k.steer * want < 0 ? DRIVING.keysCentreRealSeconds : DRIVING.keysTurnToFullLockRealSeconds));
    // keys are not pedals either (the study's rates): they ramp, and a held brake key stops short of locking
    const thr = analogPedals ? thrIn : thrIn > 0 ? 1 : 0,
      brk = analogPedals ? brkIn : brkIn > 0 ? P.keyBrakeMax : 0;
    k.thr = analogPedals ? thr : approach(k.thr, thr, STEP * (thr > k.thr ? P.keyThrottleIn : P.keyThrottleOut));
    k.brk = analogPedals ? brk : approach(k.brk, brk, STEP * (brk > k.brk ? P.keyBrakeIn : P.keyBrakeOut));
    k.hb = approach(k.hb, inp.hb ? 1 : 0, STEP * 9);
    drive({ steer: stick ? clamp(-(inp.x || 0), -1, 1) : k.steer, analog: stick, throttle: k.thr, brake: k.brk, handbrake: k.hb }, STEP);
    v.step(STEP);
    CAB.touch += STEP;
    if (!CAB.touching) CAB.crushV *= 0.85;
    CAB.touching = false;
    collide(STEP, traffic);
  }
}
// Left standing: held on its brakes (the study's park()).
export function park() {
  CAB.live = false;
}
// Somebody in the road: the car is slowed to this share of its speed (0 stops it).
export function slowTo(share) {
  const v = CAB.veh;
  v.vel[0] *= share;
  v.vel[2] *= share;
  for (const W of v.wheels) W.omega *= share;
}
// The game has set the car's speed itself: the study's car takes it up, in a gear that suits it.
export function setSpeed(c, speed) {
  const v = CAB.veh;
  v.reset(c.x, c.z, c.ang, Math.max(0, speed));
  if (speed < 0) {
    v.vel[0] = Math.sin(c.ang) * speed;
    v.vel[2] = Math.cos(c.ang) * speed;
  }
  v.speed = speed;
}
