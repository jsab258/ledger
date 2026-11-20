// Arcade driving and light traffic. Britain drives on the left.
import { G, hour } from './state.js';
import { hyp, clamp, rnd, pick, chance, angDiff } from './util.js';
import { blocked, ROUTES, BUS_STOPS, POSTS, whatBlocks , ROADS } from './map.js';
import { act } from './events.js';
import { sub, tomName } from './ui.js';
import { AT_ONCE, atOnce } from './talk_lines.js';
import { nightF } from './seeing.js';
import { buildCar, carLights } from './render/cars.js';
import { S } from './render/sync.js';
import { RULES } from './rules.js';
import * as QR from './qr/cab.js';
const TRAFFIC = RULES.traffic;
const DRIVING = RULES.driving;

const T = {
  list: [],
  spawn: TRAFFIC.firstCarAfterRealSeconds,
  bus: TRAFFIC.firstBusAfterRealSeconds,
  crashCool: 0,
  scene: null,
};
const KINDS_ = [
  ['saloon', '#5a5a52'],
  ['hatch', '#7a2a22'],
  ['hatch', '#c8c2a8'],
  ['saloon', '#2a3f34'],
  ['van', '#d8d4c8'],
  ['saloon', '#3a2a4a'],
  ['hatch', '#8a6a1a'],
  ['flatbed', '#3a4a5a'],
];
export function initTraffic(scene) {
  T.scene = scene;
  T.list = [];
}
// round 6: a lamp post (the column, not a wall bracket) stands in the way of the cab
const postAt = (x, z, r) => {
  for (const l of POSTS) if (hyp(x, z, l.x, l.z) < r + DRIVING.lampPostRadiusMetres) return true;
  return false;
};
// the car, van or bus standing at this spot, if one is (round 6: split out of solidAt so a crash can name it)
function trafficAt(x, z, r, self, parkedOnly) {
  for (const v of S.traffic) {
    if (v === self || !v.car.g.visible || (parkedOnly && !v.parked)) continue;
    if (hyp(x, z, v.x, v.z) < r + v.r) return v;
    if (v.car.len > 5) {
      const a = v.car.g.rotation.y;
      for (const k of [-1, 1])
        if (
          hyp(x, z, v.x + Math.sin(a) * k * v.car.len * 0.3, v.z + Math.cos(a) * k * v.car.len * 0.3) <
          r + v.r
        )
          return v;
    }
  }
  return null;
}
function solidAt(x, z, r, self, parkedOnly) {
  if (blocked(x, z, r)) return true;
  if (postAt(x, z, r)) return true;
  return !!trafficAt(x, z, r, self, parkedOnly);
}
// The cab Tom drives.
// Round 6 (the gate): what the cab is doing that a save does not hold: the eased steering, a jam being timed.
const CAB = { steer: 0, jam: 0, wedged: false, boxed: null, last: null };
// for the test hook: the eased steering, whether the cab is wedged, and whether it stands clear of everything solid
export const cabFeel = () => ({
  steerMinusOneToOne: CAB.steer,
  wedged: CAB.wedged,
  standsClear: !poseHit(G.car.x, G.car.z, G.car.ang),
  standsClearOfFixedThings: !poseHit(G.car.x, G.car.z, G.car.ang, true), // walls, posts, parked cars: not a car in the road
});
// for the test hook: what stands on the street besides the map's own things
export const streetThings = () => ({
  lampPosts: POSTS.map((l) => ({ xMetres: l.x, zMetres: l.z, radiusMetres: DRIVING.lampPostRadiusMetres })),
  cars: S.traffic.map((v) => ({
    xMetres: v.x,
    zMetres: v.z,
    facingRadians: v.car.g.rotation.y,
    lengthMetres: v.car.len,
    widthMetres: v.car.wid,
    parked: !!v.parked,
    bus: !!v.bus,
    speedMetresPerSecond: v.v || v.sp || 0,
  })),
});
// The one-shot (the clumsy run's fault): a vehicle standing or passing between the camera and Tom hides him. The
// camera comes in front of any vehicle its arm crosses below the vehicle's roof (player.js).
export function vehicleAt(x, z, y) {
  const K = RULES.game.feel.cameraAndVehicles;
  for (const v of S.traffic) {
    if (y >= (v.bus ? K.busRoofMetres : K.carRoofMetres)) continue;
    const dx = x - v.x,
      dz = z - v.z,
      len = (v.car.len || K.carLengthMetres) / 2 + K.grownMetres;
    if (Math.abs(dx) > len || Math.abs(dz) > len) continue;
    const a = v.car.g.rotation.y,
      along = dx * Math.sin(a) + dz * Math.cos(a),
      across = dx * Math.cos(a) - dz * Math.sin(a);
    if (Math.abs(along) < len && Math.abs(across) < (v.car.wid || K.carWidthMetres) / 2 + K.grownMetres) return true;
  }
  // his own cab, when he is on foot beside it
  if (!G.tom.inCar && y < K.carRoofMetres) {
    const c = G.car,
      dx = x - c.x,
      dz = z - c.z,
      along = dx * Math.sin(c.ang) + dz * Math.cos(c.ang),
      across = dx * Math.cos(c.ang) - dz * Math.sin(c.ang);
    if (Math.abs(along) < K.cabHalfLengthMetres && Math.abs(across) < K.cabHalfWidthMetres) return true;
  }
  return false;
}
const AXLES = [1.55, 0, -1.55];
// would the cab, standing here at this heading, be in something solid?
function poseHit(x, z, ang, fixedOnly) {
  const fx = Math.sin(ang),
    fz = Math.cos(ang);
  for (const k of AXLES)
    if (solidAt(x + fx * k, z + fz * k, DRIVING.cabHalfWidthMetres, null, fixedOnly)) return true;
  // a post is thin enough to slip between two of the three circles: the two gaps are looked at as well
  for (const k of AXLES)
    if (k && postAt(x + (fx * k) / 2, z + (fz * k) / 2, DRIVING.cabHalfWidthMetres)) return true;
  return false;
}
// how far the cab could roll along its own line, this way (dir 1 ahead, -1 back), before meeting something
function playAlong(c, dir, most) {
  const fx = Math.sin(c.ang) * dir,
    fz = Math.cos(c.ang) * dir,
    e = DRIVING.wedgedLooksEveryMetres;
  let d = 0;
  while (d + e <= most && !poseHit(c.x + fx * (d + e), c.z + fz * (d + e), c.ang)) d += e;
  return d;
}
// How far along its own line, this way (1 ahead, -1 back), a wedged cab would first stand clear (Infinity: not in reach)
function clearAlong(c, dir) {
  const fx = Math.sin(c.ang) * dir,
    fz = Math.cos(c.ang) * dir;
  for (let d = DRIVING.wedgedLooksEveryMetres; d <= DRIVING.wedgedLooksMetres; d += DRIVING.wedgedLooksEveryMetres)
    if (!poseHit(c.x + fx * d, c.z + fz * d, c.ang)) return d;
  return Infinity;
}
// Which ways a wedged cab may move: the way that leads out soonest, and the other way too when it is about as
// near (a post at its middle). Never the long way, which would be through to the far side of a wall.
function wayOut(c) {
  const back = clearAlong(c, -1),
    ahead = clearAlong(c, 1),
    near = Math.min(back, ahead) + DRIVING.wedgedEitherWayWithinMetres;
  return {
    back: back < Infinity && back <= near,
    ahead: ahead < Infinity && ahead <= near,
    any: back < Infinity || ahead < Infinity,
  };
}
// A cab with no room either way is put on the nearest ground where it stands clear and has room to roll.
function workClear(c) {
  const room = (x, z, a) => {
    if (poseHit(x, z, a)) return false;
    const q = { x, z, ang: a };
    return (
      playAlong(q, 1, DRIVING.workedClearNeedsMetresOfPlay) + playAlong(q, -1, DRIVING.workedClearNeedsMetresOfPlay) >=
      DRIVING.workedClearNeedsMetresOfPlay
    );
  };
  for (let r = 1; r <= DRIVING.workedClearSearchMetres; r++)
    for (let k = 0; k < DRIVING.looksRoundInDirections; k++) {
      const a = (k * 2 * Math.PI) / DRIVING.looksRoundInDirections,
        x = c.x - Math.sin(c.ang + a) * r,
        z = c.z - Math.cos(c.ang + a) * r;
      for (const turn of [0, Math.PI / 2, -Math.PI / 2, Math.PI])
        if (room(x, z, c.ang + turn)) {
          c.x = x;
          c.z = z;
          c.ang += turn;
          c.v = 0;
          return true;
        }
    }
  return false;
}
// what the cab has just met, in plain words, for the line on screen
function hitWhat(c, dt) {
  const fx = Math.sin(c.ang),
    fz = Math.cos(c.ang),
    dir = Math.sign(c.v || 1),
    r = DRIVING.cabHalfWidthMetres,
    reach = dir * (Math.abs(c.v) * dt + DRIVING.wedgedLooksEveryMetres);
  for (const k of [AXLES[0] * dir, 0, -AXLES[0] * dir, (AXLES[0] * dir) / 2, (-AXLES[0] * dir) / 2]) {
    const x = c.x + fx * (k + reach),
      z = c.z + fz * (k + reach),
      v = trafficAt(x, z, r, null);
    if (v) return v.parked ? 'a parked car' : v.bus ? 'the bus' : 'a car in the road';
    if (postAt(x, z, r)) return 'a lamp post';
    const w = whatBlocks(x, z, r);
    if (w) return w;
  }
  return 'something';
}
export function stepCar(dt, inp) {
  const c = G.car,
    t = G.tom;
  T.crashCool -= dt;
  if (!t.inCar) {
    // left standing: held on its brakes
    c.v *= Math.max(0, 1 - dt * DRIVING.rollsToAStopPerSecond);
    c.braking = false;
    CAB.steer = 0;
    CAB.jam = 0;
    CAB.wedged = false;
    CAB.boxed = null;
    QR.park();
    return;
  }
  // The car is the driving study's (qr/cab.js). It is sat where the game's car stands whenever the game has moved
  // the car itself (getting in, a load, a car fetched back or worked clear).
  if (!QR.CAB.live || !CAB.last || hyp(c.x, c.z, CAB.last[0], CAB.last[1]) > 0.02 || Math.abs(c.ang - CAB.last[2]) > 0.001) QR.seat(c);
  else if (Math.abs(c.v - CAB.last[3]) > 1e-6) QR.setSpeed(c, c.v); // the game itself has changed its speed (a wreck rolling to rest, a test's own run-up)
  const thr = inp.y,
    hb = inp.hb,
    cars = G.x && G.x.cars,
    dead = !!(cars && cars.wrecked && G.played - cars.wrecked.played > RULES.game.cars.wreckRollsOnRealSeconds),
    x0 = c.x,
    z0 = c.z,
    a0 = c.ang;
  CAB.steer = -QR.CAB.k.steer; // the eased wheel, for the picture and the tests (positive to the right, as before)
  c.braking = (thr < 0 && c.v > DRIVING.brakeLightsAboveMetresPerSecond) || hb;
  const near = [];
  for (const v of S.traffic) if (v.car.g.visible && hyp(v.x, v.z, c.x, c.z) < 12) near.push(v);
  QR.stepCab(dt, dead ? { kx: inp.kx, x: inp.x, y: -0.4, hb: false } : inp, dead ? 0 : 1 - c.dmg * DRIVING.damageSlowsByShare, near);
  QR.read(c);
  // never inside the town: water, the edge of the map, anything the solver did not hold (a rare deep overlap)
  if (deepIn(c)) {
    c.x = x0;
    c.z = z0;
    c.ang = a0;
    c.v = 0;
    QR.seat(c);
  }
  // a crash, said in words at once with what it has done to the car (ER-CORE-02, ER-DRIVE-08)
  for (const h of QR.CAB.hits) {
    if (h.v <= DRIVING.crashAboveMetresPerSecond || T.crashCool > 0) continue;
    T.crashCool = DRIVING.crashCountedEveryRealSeconds;
    const what = h.kind === 'post' ? 'a lamp post' : h.kind === 'parked' ? 'a parked car' : h.kind === 'car' ? 'a car in the road' : whatBlocks(h.x, h.z, 0.6) || hitWhat(c, dt),
      worst = c.dmg >= DRIVING.damageAtMost;
    c.dmg = Math.min(DRIVING.damageAtMost, c.dmg + 1);
    act('crash', { noiseR: DRIVING.crashNoiseCarriesMetres });
    if (G.hooks.emit) G.hooks.emit('cars.crash', { speed: h.v, what }); // the whole game: from about 35 mph it will not drive on (game/cars.js)
    if (G.hooks.sfx) G.hooks.sfx('crash');
    if (G.hooks.shake) G.hooks.shake(0.5);
    sub(atOnce(worst ? AT_ONCE.crash.again : AT_ONCE.crash['dent' + c.dmg] || AT_ONCE.crash.again, { what }), '', 'over', DRIVING.crashLineShowsRealSeconds);
  }
  // never stranded (ER-DRIVE-01, the cab fix of 20 Nov): pressing and not moving, with no room to roll either way,
  // the cab is worked clear onto the nearest open ground
  if (!dead && Math.abs(thr) > DRIVING.workedClearThrottleAbove && Math.abs(c.v) < 0.3) {
    if (!CAB.boxed) CAB.boxed = [c.x, c.z];
    CAB.jam += dt;
    if (hyp(c.x, c.z, CAB.boxed[0], CAB.boxed[1]) > DRIVING.boxedInBelowMetresOfPlay) {
      CAB.boxed = null;
      CAB.jam = 0;
    } else if (CAB.jam > DRIVING.workedClearAfterRealSeconds * 3 && playAlong(c, 1, DRIVING.boxedInLooksMetres) + playAlong(c, -1, DRIVING.boxedInLooksMetres) < DRIVING.boxedInBelowMetresOfPlay && workClear(c)) {
      CAB.boxed = null;
      CAB.jam = 0;
      QR.seat(c);
      sub(AT_ONCE.jam.clear, '', 'over', DRIVING.crashLineShowsRealSeconds);
    }
  } else if (Math.abs(c.v) > 0.6) {
    CAB.boxed = null;
    CAB.jam = 0;
  }
  const fx = Math.sin(c.ang),
    fz = Math.cos(c.ang),
    vWas = c.v;
  // people in the road
  for (const P of G.named.concat(G.crowd)) {
    if (P.gone || P.down || P.dead || P.space !== 'street' || P.inCar) continue;
    // against the whole car, nose, tail and flanks (the study's car turns in its own length: a flank can meet a man too)
    const pdx = P.x - c.x,
      pdz = P.z - c.z,
      pf = pdx * fx + pdz * fz,
      pl = pdx * fz - pdz * fx,
      d = hyp(P.x, P.z, c.x + fx * 1.7 * Math.sign(c.v || 1), c.z + fz * 1.7 * Math.sign(c.v || 1)),
      flank = Math.abs(pl) < DRIVING.cabHalfWidthMetres + 0.3 && pf > -2.25 && pf < 2.35 && Math.abs(c.v) > 0.05;
    if (d > DRIVING.hitsAPersonWithinMetres && !flank) continue;
    if (Math.abs(c.v) > DRIVING.knocksDownAboveMetresPerSecond) {
      P.down = true;
      P.hurt = clamp(
        (P.hurt || 0) + Math.abs(c.v) * DRIVING.hurtPerMetrePerSecond,
        0,
        DRIVING.runDownHurtAtMost,
      );
      P.downT = G.t + DRIVING.runDownStaysDownGameMinutes;
      P.route = null;
      P.moving = false;
      act('knocked', {
        target: P.anon ? undefined : P.id,
        name: P.def.name,
        noiseR: DRIVING.runDownNoiseCarriesMetres,
      });
      // round 6: said in words at once, by the name Tom knows them by. A car hurts and never kills.
      sub(
        atOnce(
          Math.abs(c.v) < DRIVING.runDownIsAClipBelowMetresPerSecond ? AT_ONCE.knocked.clip : AT_ONCE.knocked.hard,
          { t: tomName(P) },
        ),
        '',
        'over',
        DRIVING.runDownLineShowsRealSeconds,
      );
      if (G.hooks.emit) G.hooks.emit('cars.hit', { P, speed: Math.abs(c.v) }); // the whole game: the choice is put at once (game/cars.js)
      c.v *= DRIVING.slowsToShareAfterHitting;
      if (G.hooks.sfx) G.hooks.sfx('hit');
      if (!P.anon) {
        P.mind.regard = clamp(P.mind.regard - DRIVING.regardLostWhenRunDown, -1, 1);
      }
    } else {
      c.v = 0;
      // he steps out from the side of the car, clear of it
      const side = pl >= 0 ? 1 : -1,
        out = Math.max(0.5, DRIVING.cabHalfWidthMetres + 0.45 - Math.abs(pl));
      const px = P.x + fz * side * out,
        pz = P.z - fx * side * out;
      if (!blocked(px, pz)) {
        P.x = px;
        P.z = pz;
      }
    }
  }
  if (c.v !== vWas) QR.slowTo(vWas ? c.v / vWas : 0); // somebody in the road stopped or slowed it
  CAB.last = [c.x, c.z, c.ang, c.v];
  t.x = c.x;
  t.z = c.z;
  t.ang = c.ang;
  t.v = Math.abs(c.v);
}
// is the middle line of the cab well inside something (water and the map's edge count)?
function deepIn(c) {
  const fx = Math.sin(c.ang),
    fz = Math.cos(c.ang);
  for (const k of AXLES) if (blocked(c.x + fx * k, c.z + fz * k, 0.25)) return true;
  return false;
}
export function nearCar(d = DRIVING.nearTheCabWithinMetres) {
  return hyp(G.tom.x, G.tom.z, G.car.x, G.car.z) < d;
}
// Round 6 (the gate): what stops a man on foot besides the map: lamp posts, parked cars, cars in the road. A step
// is refused only when it takes him deeper into one of them, so he can always walk out of anything he finds
// himself inside. (ox, oz): where he stands now.
const carDepth = (v, x, z, rad) => {
  const a = v.car.g.rotation.y,
    sn = Math.sin(a),
    cs = Math.cos(a),
    dx = x - v.x,
    dz = z - v.z;
  return Math.min(
    v.car.len / 2 + rad - Math.abs(dx * sn + dz * cs),
    v.car.wid / 2 + rad - Math.abs(dx * cs - dz * sn),
  );
};
export function footSolid(x, z, ox, oz, rad) {
  for (const l of POSTS) {
    const d = hyp(x, z, l.x, l.z);
    if (d < rad + DRIVING.lampPostRadiusMetres && d < hyp(ox, oz, l.x, l.z)) return true;
  }
  for (const v of S.traffic) {
    if (!v.car.g.visible) continue;
    const pen = carDepth(v, x, z, rad);
    if (pen > 0 && pen > carDepth(v, ox, oz, rad)) return true;
  }
  return false;
}
// is this spot clear ground for a man: not in the map's solids, a post or a car
export function footClear(x, z, rad) {
  if (blocked(x, z, rad)) return false;
  for (const l of POSTS) if (hyp(x, z, l.x, l.z) < rad + DRIVING.lampPostRadiusMetres) return false;
  for (const v of S.traffic) if (v.car.g.visible && carDepth(v, x, z, rad) > 0) return false;
  return true;
}
// the nearest clear ground to a spot, looked for in widening rings (null when there is none in reach)
export function clearGround(x, z, rad, most, step, ok = () => true) {
  for (let r = step; r <= most; r += step)
    for (let k = 0; k < DRIVING.looksRoundInDirections; k++) {
      const a = (k * 2 * Math.PI) / DRIVING.looksRoundInDirections,
        px = x + Math.sin(a) * r,
        pz = z + Math.cos(a) * r;
      if (footClear(px, pz, rad) && ok(px, pz)) return [px, pz];
    }
  return null;
}
// which side of the car is nearer a pavement: 1 its right, -1 its left
function nearerKerb(c) {
  const d = (s) => {
    for (let k = 1.55; k < 9; k += 0.5) {
      const x = c.x + -Math.cos(c.ang) * s * k,
        z = c.z + Math.sin(c.ang) * s * k;
      if (!ROADS.some((r) => x > r.x0 && x < r.x1 && z > r.z0 && z < r.z1)) return k;
    }
    return 99;
  };
  return d(1) <= d(-1) ? 1 : -1;
}
export function exitPoint() {
  const c = G.car,
    R = DRIVING.exitBodyRadiusMetres;
  // the one-shot: he gets out on the kerb side when that door is clear, by the road side when it is not
  const sideX = (s) => c.x + -Math.cos(c.ang) * s * 1.55,
    sideZ = (s) => c.z + Math.sin(c.ang) * s * 1.55,
    onRoad = (x, z) => ROADS.some((r) => x > r.x0 && x < r.x1 && z > r.z0 && z < r.z1),
    kerb = onRoad(sideX(1), sideZ(1)) && !onRoad(sideX(-1), sideZ(-1)) ? -1 : !onRoad(sideX(1), sideZ(1)) && onRoad(sideX(-1), sideZ(-1)) ? 1 : nearerKerb(c);
  for (const [s, k] of [
    [kerb, 0],
    [-kerb, 0],
    [kerb, 1.2],
    [-kerb, 1.2],
    [0, -3.2],
  ]) {
    const x = c.x + -Math.cos(c.ang) * s * 1.55 + Math.sin(c.ang) * (s ? k : -3.2),
      z = c.z + Math.sin(c.ang) * s * 1.55 + Math.cos(c.ang) * (s ? k : -3.2);
    if (footClear(x, z, R)) return [x, z];
  }
  // round 6 (ER-DRIVE-07): a blocked door never traps him. No door has clear ground: he climbs out to the nearest
  // clear ground beside the cab instead of into whatever is against it.
  const offCab = (px, pz) => {
    for (const k of AXLES)
      if (hyp(px, pz, c.x + Math.sin(c.ang) * k, c.z + Math.cos(c.ang) * k) < RULES.tom.cabBodyRadiusMetres + R)
        return false;
    return true;
  };
  return (
    clearGround(c.x, c.z, R, DRIVING.exitSearchMetres, DRIVING.exitSearchStepMetres, offCab) || [c.x + 2, c.z]
  );
}

// Other people's cars, and the corporation bus.
function spawn(kind, color, route, o = {}) {
  const pts = ROUTES[route];
  const car = buildCar(kind, color, Object.assign({ driver: true }, o));
  T.scene.add(car.g);
  const v = {
    car,
    route,
    pts,
    i: 0,
    x: pts[0][0],
    z: pts[0][1],
    v: kind === 'bus' ? TRAFFIC.busStartsMetresPerSecond : TRAFFIC.carStartsMetresPerSecond,
    max:
      kind === 'bus'
        ? TRAFFIC.busTopMetresPerSecond
        : rnd(TRAFFIC.carTopMetresPerSecondAtLeast, TRAFFIC.carTopMetresPerSecondAtMost),
    r: kind === 'bus' ? 1.5 : 1.2,
    stop: 0,
    bus: kind === 'bus',
  };
  v.ang = Math.atan2(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]);
  car.g.position.set(v.x, 0, v.z);
  car.g.rotation.y = v.ang;
  for (const o2 of S.traffic)
    if (!o2.parked && hyp(o2.x, o2.z, v.x, v.z) < TRAFFIC.spawnClearMetres) {
      T.scene.remove(car.g);
      return null;
    }
  S.traffic.push(v);
  T.list.push(v);
  return v;
}
export function spawnBusLeaving() {
  const v = spawn('bus', '#1f3f7a', 'E', { blind: '14 STATION' });
  if (v) {
    v.i = 3;
    v.x = -1.9;
    v.z = 14;
    v.ang = Math.PI;
  }
}
export function stepTraffic(dt) {
  const t = G.tom,
    h = hour(),
    n = nightF(),
    want =
      h < TRAFFIC.noCarsBeforeHour
        ? 0
        : h < TRAFFIC.fewCarsBeforeHour
          ? 1
          : h < TRAFFIC.dayCarsBeforeHour
            ? TRAFFIC.carsByDay
            : h < TRAFFIC.eveningCarsBeforeHour
              ? 2
              : 1;
  T.spawn -= dt;
  T.bus -= dt;
  if (T.spawn <= 0) {
    T.spawn = rnd(TRAFFIC.nextCarAfterRealSecondsAtLeast, TRAFFIC.nextCarAfterRealSecondsAtMost);
    if (T.list.filter((v) => !v.bus).length < want) {
      const k = pick(KINDS_);
      spawn(k[0], k[1], pick(['A', 'B', 'C', 'D', 'E', 'F', 'C', 'D']));
    }
  }
  if (T.bus <= 0) {
    T.bus = rnd(TRAFFIC.nextBusAfterRealSecondsAtLeast, TRAFFIC.nextBusAfterRealSecondsAtMost);
    if (h >= TRAFFIC.busesFromHour && h < TRAFFIC.busesUntilHour && !T.list.some((v) => v.bus))
      spawn('bus', '#1f3f7a', chance(0.5) ? 'E' : 'B', { blind: chance(0.5) ? '14 STATION' : '14 QUAY ST' });
  }
  for (let k = T.list.length - 1; k >= 0; k--) {
    const v = T.list[k],
      tgt = v.pts[v.i + 1];
    if (!tgt) {
      T.scene.remove(v.car.g);
      T.list.splice(k, 1);
      S.traffic.splice(S.traffic.indexOf(v), 1);
      continue;
    }
    const dx = tgt[0] - v.x,
      dz = tgt[1] - v.z,
      d = Math.hypot(dx, dz),
      want2 = Math.atan2(dx, dz);
    v.ang += clamp(
      angDiff(v.ang, want2),
      -TRAFFIC.turnRadiansPerSecond * dt,
      TRAFFIC.turnRadiansPerSecond * dt,
    );
    let sp =
      v.max *
      (Math.abs(angDiff(v.ang, want2)) > TRAFFIC.slowsWhenTurningAboveRadians
        ? TRAFFIC.turningSpeedShare
        : 1);
    // stop for anything ahead: Tom, his car, people, another vehicle
    const fx = Math.sin(v.ang),
      fz = Math.cos(v.ang),
      ahead = (x, z, r) => {
        const rx = x - v.x,
          rz = z - v.z,
          f = rx * fx + rz * fz,
          s = Math.abs(rx * fz - rz * fx);
        return (
          f > 0 && f < TRAFFIC.looksAheadMetres + v.v * TRAFFIC.looksAheadAddedPerMetrePerSecond && s < r
        );
      };
    let block =
      (!t.inCar && t.space === 'street' && ahead(t.x, t.z, TRAFFIC.stopsForTomWithinMetres)) ||
      ahead(G.car.x, G.car.z, TRAFFIC.stopsForTheCabWithinMetres);
    if (!block)
      for (const o of S.traffic) {
        if (o === v || o.parked) continue;
        if (ahead(o.x, o.z, TRAFFIC.stopsForACarWithinMetres)) {
          block = true;
          break;
        }
      }
    if (!block)
      for (const P of G.named.concat(G.crowd)) {
        if (P.gone || P.space !== 'street' || P.inCar) continue;
        if (
          Math.abs(P.x - v.x) < TRAFFIC.looksForPeopleWithinMetres &&
          Math.abs(P.z - v.z) < TRAFFIC.looksForPeopleWithinMetres &&
          ahead(P.x, P.z, TRAFFIC.stopsForAPersonWithinMetres)
        ) {
          block = true;
          break;
        }
      }
    if (v.bus && BUS_STOPS[v.route]) {
      const bs = BUS_STOPS[v.route],
        ds = hyp(v.x, v.z, bs[0], bs[1]);
      if (!v.stopped && ds < TRAFFIC.busStopWithinMetres) {
        v.stopped = true;
        v.stop = TRAFFIC.busWaitsRealSeconds;
      }
    }
    if (v.stop > 0) {
      v.stop -= dt;
      sp = 0;
    }
    if (block) sp = 0;
    v.v += clamp(
      sp - v.v,
      -TRAFFIC.brakingMetresPerSecondSquared * dt,
      TRAFFIC.accelerationMetresPerSecondSquared * dt,
    );
    v.x += fx * v.v * dt;
    v.z += fz * v.v * dt;
    if (d < 2.2) v.i++;
    v.car.g.position.set(v.x, 0, v.z);
    v.car.g.rotation.y = v.ang;
    for (const w of v.car.wheels) w.rotation.x += (v.v * dt) / 0.35;
    carLights(v.car, n > 0.25, sp < v.v - 0.5);
    v.car.g.visible = t.space === 'street';
  }
}
export function clearTraffic() {
  for (const v of T.list) {
    T.scene.remove(v.car.g);
    const i = S.traffic.indexOf(v);
    if (i >= 0) S.traffic.splice(i, 1);
  }
  T.list = [];
}
