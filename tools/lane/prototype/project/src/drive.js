// Arcade driving and light traffic. Britain drives on the left.
import { G, hour } from './state.js';
import { hyp, clamp, rnd, pick, chance, angDiff } from './util.js';
import { blocked, ROUTES, BUS_STOPS } from './map.js';
import { act } from './events.js';
import { nightF } from './seeing.js';
import { buildCar, carLights } from './render/cars.js';
import { S } from './render/sync.js';
import { RULES } from './rules.js';
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
function solidAt(x, z, r, self) {
  if (blocked(x, z, r)) return true;
  for (const v of S.traffic) {
    if (v === self || !v.car.g.visible) continue;
    if (hyp(x, z, v.x, v.z) < r + v.r) return true;
    if (v.car.len > 5) {
      const a = v.car.g.rotation.y;
      for (const k of [-1, 1])
        if (
          hyp(x, z, v.x + Math.sin(a) * k * v.car.len * 0.3, v.z + Math.cos(a) * k * v.car.len * 0.3) <
          r + v.r
        )
          return true;
    }
  }
  return false;
}
// The cab Tom drives.
export function stepCar(dt, inp) {
  const c = G.car,
    t = G.tom;
  T.crashCool -= dt;
  if (!t.inCar) {
    c.v *= Math.max(0, 1 - dt * DRIVING.rollsToAStopPerSecond);
    c.braking = false;
    return;
  }
  const thr = inp.y,
    st = inp.x,
    hb = inp.hb;
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
    DRIVING.topMetresPerSecond * (1 - c.dmg * DRIVING.damageSlowsByShare),
  );
  const grip = clamp(Math.abs(c.v) / DRIVING.fullSteeringFromMetresPerSecond, 0, 1) * Math.sign(c.v || 1);
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
  const fx = Math.sin(c.ang),
    fz = Math.cos(c.ang),
    nx = c.x + fx * c.v * dt,
    nz = c.z + fz * c.v * dt;
  let hit = false;
  for (const k of [1.55, 0, -1.55])
    if (solidAt(nx + fx * k, nz + fz * k, DRIVING.cabHalfWidthMetres, null)) {
      hit = true;
      break;
    }
  if (hit) {
    const sp = Math.abs(c.v);
    c.v = -c.v * DRIVING.bouncesBackShare;
    if (sp > DRIVING.crashAboveMetresPerSecond && T.crashCool <= 0) {
      T.crashCool = DRIVING.crashCountedEveryRealSeconds;
      c.dmg = Math.min(DRIVING.damageAtMost, c.dmg + 1);
      act('crash', { noiseR: DRIVING.crashNoiseCarriesMetres });
      if (G.hooks.sfx) G.hooks.sfx('crash');
      if (G.hooks.shake) G.hooks.shake(0.5);
    }
  } else {
    c.x = nx;
    c.z = nz;
  }
  // people in the road
  for (const P of G.named.concat(G.crowd)) {
    if (P.gone || P.down || P.dead || P.space !== 'street' || P.inCar) continue;
    const d = hyp(P.x, P.z, c.x + fx * 1.7 * Math.sign(c.v || 1), c.z + fz * 1.7 * Math.sign(c.v || 1));
    if (d > DRIVING.hitsAPersonWithinMetres) continue;
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
      c.v *= DRIVING.slowsToShareAfterHitting;
      if (G.hooks.sfx) G.hooks.sfx('hit');
      if (!P.anon) {
        P.mind.regard = clamp(P.mind.regard - DRIVING.regardLostWhenRunDown, -1, 1);
      }
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
export function exitPoint() {
  const c = G.car;
  for (const [s, k] of [
    [1, 0],
    [-1, 0],
    [1, 1.2],
    [-1, 1.2],
    [0, -3.2],
  ]) {
    const x = c.x + -Math.cos(c.ang) * s * 1.55 + Math.sin(c.ang) * (s ? k : -3.2),
      z = c.z + Math.sin(c.ang) * s * 1.55 + Math.cos(c.ang) * (s ? k : -3.2);
    if (!blocked(x, z, 0.35)) return [x, z];
  }
  return [c.x + 2, c.z];
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
