// Arcade driving and light traffic. Britain drives on the left.
import { G, hour } from './state.js';
import { hyp, clamp, rnd, pick, chance, angDiff } from './util.js';
import { blocked, ROUTES, BUS_STOPS, POSTS, whatBlocks } from './map.js';
import { act } from './events.js';
import { sub, tomName } from './ui.js';
import { AT_ONCE, atOnce } from './talk_lines.js';
import { nightF } from './seeing.js';
import { buildCar, carLights } from './render/cars.js';
import { S } from './render/sync.js';
import { RULES } from './rules.js';
const TRAFFIC = RULES.traffic;
const DRIVING = RULES.driving;
// the one-shot (20 Nov): the car's rules are the pure piece game/pieces/car_rules.js, its numbers game/tune/cars.js
import { PIECE as CAR_RULES } from './game/pieces/car_rules.js';
const CR = CAR_RULES.fns;
const CT = () => RULES.game.cars;
const MPH = (v) => Math.abs(v) / CT().metresPerSecondPerMph;
const carX = () => (G.x && G.x.cars) || {};
// the scene the traffic is built into, for the cars the whole game adds (a patrol car, an ambulance, a van to follow)
export const trafficScene = () => T.scene;

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
const CAB = { steer: 0, jam: 0, wedged: false, boxed: null };
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
  })),
});
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
  if (carX().auto && t.inCar) return; // he is being driven (game/cars.js moves the cab)
  if (!t.inCar) {
    c.v *= Math.max(0, 1 - dt * DRIVING.rollsToAStopPerSecond);
    c.braking = false;
    CAB.steer = 0;
    CAB.jam = 0;
    CAB.wedged = false;
    CAB.boxed = null;
    return;
  }
  // a cab that will not drive on (a hit at about 35 mph, DESIGN 5) does not answer the pedals: he gets out and walks
  const dead = carX().offRoadUntil > G.t && carX().have !== 'taken';
  if (dead) {
    inp = { x: 0, kx: 0, y: 0, hb: true };
    if (!CAB.deadSaid || G.t - CAB.deadSaid > 20) {
      CAB.deadSaid = G.t;
      sub('It will not start. The firm fetches it; it is off the road until tomorrow. [F] Get out.', '', 'over', 5);
    }
  }
  const thr = inp.y,
    hb = inp.hb;
  // somebody dead ahead while he keeps his foot down: a car aimed at a man is an attack (DESIGN 5)
  {
    let ahead = false;
    if (thr > 0.5 && c.v > 2) {
      const ax = Math.sin(c.ang),
        az = Math.cos(c.ang);
      for (const P of G.named.concat(G.crowd)) {
        if (P.gone || P.down || P.dead || P.space !== 'street' || P.inCar) continue;
        const rx = P.x - c.x,
          rz = P.z - c.z,
          f = rx * ax + rz * az;
        if (f > 1 && f < 14 && Math.abs(rx * az - rz * ax) < 1.2) {
          ahead = true;
          break;
        }
      }
    }
    CAB.aim = ahead ? (CAB.aim || 0) + dt : 0;
  }
  // round 6: on keys the steering eases to full lock and centres itself; a stick (pad, touch) is used as it is
  {
    const want = inp.kx || 0,
      per =
        want === 0 ? DRIVING.keysCentreRealSeconds : DRIVING.keysTurnToFullLockRealSeconds,
      step = dt / per;
    CAB.steer += clamp(want - CAB.steer, -step, step);
  }
  const st = clamp(CAB.steer + (inp.x || 0), -1, 1);
  c.braking = (thr < 0 && c.v > DRIVING.brakeLightsAboveMetresPerSecond) || hb;
  if (thr > 0)
    c.v +=
      (c.v < 0
        ? DRIVING.pullAwayFromReverseMetresPerSecondSquared
        : DRIVING.accelerationMetresPerSecondSquared) *
      dt *
      thr;
  else if (thr < 0)
    c.v +=
      (c.v > DRIVING.brakesAboveMetresPerSecond
        ? -DRIVING.brakingMetresPerSecondSquared
        : -DRIVING.reverseAccelerationMetresPerSecondSquared) *
      dt *
      -thr;
  c.v -= c.v * (hb ? DRIVING.handbrakeDragPerSecond : DRIVING.dragPerSecond) * dt;
  c.v = clamp(
    c.v,
    -DRIVING.reverseTopMetresPerSecond,
    (carX().have === 'taken' ? DRIVING.topMetresPerSecond : CT().topMetresPerSecond) * (1 - c.dmg * DRIVING.damageSlowsByShare),
  );
  const grip = clamp(Math.abs(c.v) / DRIVING.fullSteeringFromMetresPerSecond, 0, 1) * Math.sign(c.v || 1);
  const ang0 = c.ang;
  c.ang -=
    st *
    grip *
    (hb ? DRIVING.handbrakeTurnRadiansPerSecond : DRIVING.turnRadiansPerSecond) *
    dt *
    (1 -
      clamp(
        (Math.abs(c.v) - DRIVING.steeringEasesAboveMetresPerSecond) /
          DRIVING.steeringEasesOverMetresPerSecond,
        0,
        DRIVING.steeringEasesByAtMostShare,
      ));
  // round 6: the cab never swings itself into something solid (that is how a car gets wedged on a pole or a wall)
  if (c.ang !== ang0 && poseHit(c.x, c.z, c.ang) && !poseHit(c.x, c.z, ang0)) c.ang = ang0;
  const fx = Math.sin(c.ang),
    fz = Math.cos(c.ang),
    nx = c.x + fx * c.v * dt,
    nz = c.z + fz * c.v * dt;
  let hit = c.v !== 0 && poseHit(nx, nz, c.ang),
    crawl = false;
  // round 6: never stranded (ER-DRIVE-01).
  if (hit && poseHit(c.x, c.z, c.ang)) {
    // Something is already in the cab's own space (a car that rolled into it, a save from before the posts were
    // solid). It may always move the way that leads out soonest, at a crawl, and never deeper in.
    const out = wayOut(c);
    if (!CAB.wedged && out.any) sub(AT_ONCE.jam.wedged, '', 'over', DRIVING.crashLineShowsRealSeconds);
    CAB.wedged = true;
    if (c.v > 0 ? out.ahead : out.back) {
      hit = false;
      crawl = true;
      c.v = clamp(c.v, -DRIVING.wedgedCrawlsMetresPerSecond, DRIVING.wedgedCrawlsMetresPerSecond);
    } else {
      c.v = 0; // not a clear way: it does not move, and nothing is damaged
      if (!out.any && !CAB.boxed) CAB.boxed = [c.x, c.z];
    }
  } else if (hit) {
    // Standing clear, but no room to roll either way: boxed in.
    if (
      !CAB.boxed &&
      playAlong(c, 1, DRIVING.boxedInLooksMetres) + playAlong(c, -1, DRIVING.boxedInLooksMetres) <
        DRIVING.boxedInBelowMetresOfPlay
    )
      CAB.boxed = [c.x, c.z];
  } else if (c.v !== 0) CAB.wedged = false;
  if (CAB.boxed) {
    // He has tried for a moment and it has not got anywhere: the cab is worked clear onto the nearest open ground.
    if (hyp(c.x, c.z, CAB.boxed[0], CAB.boxed[1]) > DRIVING.boxedInBelowMetresOfPlay) {
      CAB.boxed = null;
      CAB.jam = 0;
    } else if (Math.abs(thr) > DRIVING.workedClearThrottleAbove) {
      CAB.jam += dt;
      if (CAB.jam > DRIVING.workedClearAfterRealSeconds && workClear(c)) {
        CAB.boxed = null;
        CAB.jam = 0;
        CAB.wedged = false;
        hit = false;
        crawl = true; // it has just been put down: no step this frame
        sub(AT_ONCE.jam.clear, '', 'over', DRIVING.crashLineShowsRealSeconds);
      }
    }
  }
  if (hit) {
    const sp = Math.abs(c.v);
    if (sp > DRIVING.crashAboveMetresPerSecond && T.crashCool <= 0) {
      T.crashCool = DRIVING.crashCountedEveryRealSeconds;
      const what = hitWhat(c, dt),
        worst = c.dmg >= DRIVING.damageAtMost,
        // the one-shot: what one hit does goes by its closing speed (dented, crumpled, will not drive on)
        hitRule = CR.damage(CT(), MPH(sp), c.dmg);
      c.dmg = hitRule.stage === 'none' ? Math.min(DRIVING.damageAtMost, c.dmg + 1) : hitRule.damage;
      const car2 = /car|bus/.test(what);
      act(car2 && hitRule.stage !== 'dented' ? 'car_rammed' : 'crash', { noiseR: DRIVING.crashNoiseCarriesMetres, name: car2 ? what : undefined });
      if (G.hooks.sfx) G.hooks.sfx('crash');
      if (G.hooks.shake) G.hooks.shake(0.5);
      // round 6: said in words at once, with what it has done to the car (ER-CORE-02, ER-DRIVE-08)
      if (hitRule.stage === 'dead') {
        sub(`The cab hits ${what} hard. The front is stove in and the engine has stopped: it will not drive on. [F] Get out.`, '', 'over', DRIVING.crashLineShowsRealSeconds + 2);
        if (G.hooks.carDead) G.hooks.carDead(what, MPH(sp));
      } else
      sub(
        atOnce(worst ? AT_ONCE.crash.again : AT_ONCE.crash['dent' + c.dmg] || AT_ONCE.crash.again, { what }),
        '',
        'over',
        DRIVING.crashLineShowsRealSeconds,
      );
      if (hitRule.stage === 'dead') {
        c.v = 0;
        t.x = c.x;
        t.z = c.z;
        return;
      }
    }
    c.v = -c.v * DRIVING.bouncesBackShare;
  } else if (!crawl || CAB.wedged) {
    c.x = c.x + fx * c.v * dt;
    c.z = c.z + fz * c.v * dt;
  }
  // people in the road
  for (const P of G.named.concat(G.crowd)) {
    if (P.gone || P.down || P.dead || P.space !== 'street' || P.inCar) continue;
    const d = hyp(P.x, P.z, c.x + fx * 1.7 * Math.sign(c.v || 1), c.z + fz * 1.7 * Math.sign(c.v || 1));
    if (d > DRIVING.hitsAPersonWithinMetres) continue;
    if (Math.abs(c.v) > DRIVING.knocksDownAboveMetresPerSecond) {
      // the one-shot: the hurt goes by speed and aim, and a car never kills (canon; pieces/car_rules.js hurt)
      const mph = MPH(c.v),
        aimed = (CAB.aim || 0) > 0.7,
        H = CR.hurt(CT(), mph, aimed, null);
      P.down = true;
      P.hurt = clamp((P.hurt || 0) + H.hurt, 0, Math.max(P.hurt || 0, CT().hurtAtMost));
      P.downT = G.t + Math.max(DRIVING.runDownStaysDownGameMinutes, H.downGameMinutes || 0);
      P.carHurt = H.kind;
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
      c.v *= DRIVING.slowsToShareAfterHitting;
      if (G.hooks.sfx) G.hooks.sfx('hit');
      if (!P.anon) {
        P.mind.regard = clamp(P.mind.regard - DRIVING.regardLostWhenRunDown, -1, 1);
      }
      // then the choice, put at once: stop and help, or drive off (ER-DRIVE-05; game/cars.js)
      if (G.hooks.carHit) G.hooks.carHit(P, mph, aimed, H);
    } else {
      c.v = 0;
      const a = Math.atan2(P.x - c.x, P.z - c.z) + 1.2;
      const px = P.x + Math.sin(a) * 0.5,
        pz = P.z + Math.cos(a) * 0.5;
      if (!blocked(px, pz)) {
        P.x = px;
        P.z = pz;
      }
    }
  }
  t.x = c.x;
  t.z = c.z;
  t.ang = c.ang;
  t.v = Math.abs(c.v);
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
export function exitPoint() {
  const c = G.car,
    R = DRIVING.exitBodyRadiusMetres;
  for (const [s, k] of [
    [1, 0],
    [-1, 0],
    [1, 1.2],
    [-1, 1.2],
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
          // the one-shot (canon: only the player's car can strike anybody): with somebody this near, he stands on it
          const f = (P.x - v.x) * fx + (P.z - v.z) * fz;
          if (f < 1.6 + (v.v * v.v) / (2 * TRAFFIC.brakingMetresPerSecondSquared)) v.v = 0;
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

// ---------- the one-shot (20 Nov): cars the whole game drives itself ----------
// A patrol car, an ambulance, a van to follow, a car in the mirror, a car left standing. Each is solid like any car
// in the road, is moved by game/cars.js, and its driver always brakes for people (canon).
export function addActor(kind, color, o, x, z, ang, parked) {
  if (!T.scene) return null;
  const car = buildCar(kind, color, Object.assign({ driver: !parked }, o || {}));
  T.scene.add(car.g);
  const v = { car, x, z, ang, v: 0, r: 1.2, actor: true, parked: !!parked };
  car.g.position.set(x, 0, z);
  car.g.rotation.y = ang;
  carLights(car, false, false);
  S.traffic.push(v);
  return v;
}
export function removeActor(v) {
  if (!v) return;
  if (T.scene) T.scene.remove(v.car.g);
  const i = S.traffic.indexOf(v);
  if (i >= 0) S.traffic.splice(i, 1);
}
// Drive an actor towards a point at up to `top`. Returns the metres still to go. brake: stand still.
export function driveActor(v, tx, tz, top, dt, brake) {
  const dx = tx - v.x,
    dz = tz - v.z,
    d = Math.hypot(dx, dz),
    want = Math.atan2(dx, dz),
    fx = Math.sin(v.ang),
    fz = Math.cos(v.ang);
  if (d > 0.5) v.ang += clamp(angDiff(v.ang, want), -2.4 * dt, 2.4 * dt);
  let sp = brake ? 0 : Math.min(top, Math.max(1.5, d * 1.2)) * (Math.abs(angDiff(v.ang, want)) > 0.5 ? 0.5 : 1);
  // always brakes for people, and for Tom on foot
  const near = (x, z) => {
    const rx = x - v.x,
      rz = z - v.z,
      f = rx * fx + rz * fz;
    return f > 0 && f < 2.2 + v.v * 0.9 && Math.abs(rx * fz - rz * fx) < 1.5;
  };
  const t = G.tom;
  if (!t.inCar && t.space === 'street' && near(t.x, t.z)) sp = 0;
  if (sp > 0)
    for (const P of G.named.concat(G.crowd)) {
      if (P.gone || P.space !== 'street' || P.inCar) continue;
      if (Math.abs(P.x - v.x) < 14 && Math.abs(P.z - v.z) < 14 && near(P.x, P.z)) {
        sp = 0;
        if ((P.x - v.x) * fx + (P.z - v.z) * fz < 1.6 + (v.v * v.v) / (2 * TRAFFIC.brakingMetresPerSecondSquared)) v.v = 0;
        break;
      }
    }
  v.v += clamp(sp - v.v, -TRAFFIC.brakingMetresPerSecondSquared * dt, 5 * dt);
  v.x += Math.sin(v.ang) * v.v * dt;
  v.z += Math.cos(v.ang) * v.v * dt;
  v.car.g.position.set(v.x, 0, v.z);
  v.car.g.rotation.y = v.ang;
  for (const w of v.car.wheels) w.rotation.x += (v.v * dt) / 0.35;
  carLights(v.car, nightF() > 0.25, sp < v.v - 0.5);
  v.car.g.visible = t.space === 'street';
  return d;
}
// The cab driven for him (riding with Kevin, Terry or a crewman; the scripted driver of the tests): along the points,
// braking for people. Returns true when it has arrived.
export function autoDrive(pts, st, top, dt) {
  const c = G.car,
    p = pts[st.i];
  if (!p) return true;
  const v = { x: c.x, z: c.z, ang: c.ang, v: c.v, car: S.cab };
  const d = driveActor(v, p[0], p[1], top, dt, false);
  c.x = v.x;
  c.z = v.z;
  c.ang = v.ang;
  c.v = v.v;
  const t = G.tom;
  t.x = c.x;
  t.z = c.z;
  t.ang = c.ang;
  if (d < (st.i === pts.length - 1 ? 1.2 : 3.5)) st.i++;
  if (st.i >= pts.length) {
    c.v = 0;
    return true;
  }
  return false;
}
