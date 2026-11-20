// LEDGER, the whole game: the system "cars". The car in the town (DESIGN 5; addendum A2, A12, A14, A22, A24, A27, A32):
// what a hit does and the choice after it, the ambulance, a cab that will not drive on, the horn, the patrol car and
// its stops and chases, tails by car, riding as a passenger, paint, taking a parked car, the other firm.
// The rules are the pure piece pieces/car_rules.js; the numbers are tune/cars.js. This file plays them.
import { register, emit, on, X } from './core.js';
import { G, hour } from '../state.js';
import { RULES } from '../rules.js';
import { hyp, clamp, inRect, money, pounds } from '../util.js';
import { act, logLine } from '../events.js';
import { note } from '../ledger.js';
import { sub, say, scene, fade, choose, tomName } from '../ui.js';
import { pay } from '../money.js';
import { advanceTo } from '../work.js';
import { PAVE, SPOTS, EXITS } from '../map.js';
import { keys, cam, snapCam } from '../player.js';
import { endTalk } from '../talk.js';
import { S as SYNC } from '../render/sync.js';
import { restyleCar } from '../render/cars.js';
import { addActor, removeActor, driveActor, autoDrive, exitPoint, footClear } from '../drive.js';
import { PIECE as CAR } from './pieces/car_rules.js';
import { PIECE as FR } from './pieces/fare_rules.js';
import { ROADS_F, PLACES_F, JUNCTIONS_F } from './fares_data.js';

const C = CAR.fns;
const T = () => RULES.game.cars;
const x = () => X('cars');
const mph = (v) => Math.abs(v) / T().metresPerSecondPerMph;
const HOME = { x: 4.1, z: 37.4, ang: 0 }; // the rank, where the firm puts a fetched cab
const FIRM_PAINT = '#1d2a5c';
const PAINTS = ['#5a5a52', '#6a3a22', '#2a3f34', '#7a6a2a'];
const cap1 = (s) => s.charAt(0).toUpperCase() + s.slice(1);
const los = (ax, az, bx, bz) => G.env.los(ax, az, bx, bz);

// what the game is doing with cars that a save does not hold (meshes, a chase in hand)
const RT = { patrol: null, amb: null, van: null, mirror: null, standing: null, takenCar: null, crumbs: [], hornT: 0, hornDown: false, lastRealHit: -99, real: 0 };

const fresh = () => ({
  offRoadUntil: 0, // the cab will not drive on until this game minute
  deadAt: null, // where it was left, until the firm fetches it
  paint: FIRM_PAINT,
  sign: true, // the roof sign: it makes the car the firm's
  plate: 0,
  have: 'cab', // 'cab' or 'taken' (a parked car he has taken)
  standing: null, // where the firm's cab stands while he drives a taken car
  cabDmg: 0,
  taken: null, // { at, name, reported }
  hit: null, // the person just hit, until the choice is made: { pid, t, real, mph, aimed, kind, x, z }
  amb: null, // an ambulance called: { pid, calledAt, arrivesAt, x, z }
  lastHit: null, // { t, hitAndRun }: what the firm's name is paying for
  wanted: null, // { until, why }: the car is described, and a police car that sees it gives chase
  plateNoted: 0,
  stops: 0,
  stop: null, // a stop or a chase in hand: { st: 'flash' | 'chase', why, t, unseen, slow }
  seen: [], // every deed done from the car, with how the car looked: { e, paint, sign, plate }
  lastE: 0,
  auto: null, // he is being driven: { pts, i, to, who }
  ride: null,
  hits: [],
});

// ---------- roads: the lanes a driver keeps to (Britain drives on the left) ----------
export function lanePoints(legs, lane = 1.9) {
  const pts = [];
  for (const l of legs) {
    const R = ROADS_F[l.road],
      off = l.heads === 'south' ? lane : l.heads === 'north' ? -lane : l.heads === 'east' ? -lane : lane;
    pts.push(R.axis === 'z' ? [R.at + off, l.to.z] : [l.to.x, R.at + off]);
  }
  return pts;
}
const routePoints = (from, to) => lanePoints(FR.fns.legs(ROADS_F, from, to));

// ---------- a hit, and the choice put at once (ER-DRIVE-03 to 05, 10) ----------
function carHit(P, hitMph, aimed, H) {
  const s = x();
  RT.lastRealHit = RT.real;
  s.hits.push({ t: Math.round(G.t), who: P.id, mph: Math.round(hitMph), aimed: !!aimed, kind: H.kind });
  if (s.hits.length > 40) s.hits.shift();
  emit('carhit', { who: P.id, mph: hitMph, aimed: !!aimed, kind: H.kind });
  if (H.attack) act('car_aimed', P.anon ? { name: P.def.desc, noiseR: 30 } : { target: P.id, noiseR: 30 });
  if (H.kind === 'clip' && !aimed) return; // a bruise and a mouthful: no more comes of it than the telling
  s.hit = { pid: P.id, t: G.t, real: 0, mph: hitMph, aimed: !!aimed, kind: H.kind, x: P.x, z: P.z, days: H.hospitalDays || 0 };
  // said within two seconds, with both answers on the keys (the prompts follow in the same frame)
  sub(`${tomName(P)} is in the road and not getting up. Stop and help [Y], or drive off [G].`, '', 'over', 7);
}
function help() {
  const s = x(),
    h = s.hit,
    t = G.tom;
  if (!h) return;
  const P = G.people[h.pid];
  s.hit = null;
  G.car.v = 0;
  if (t.inCar) {
    const [ex, ez] = exitPoint();
    t.inCar = false;
    t.x = ex;
    t.z = ez;
    t.v = 0;
  }
  // his face beside the cab, seen by everyone who stopped to look (A22)
  act('hit_helped', P.anon ? { name: P.def.desc } : { target: P.id });
  const r = C.afterHit(T(), 'help');
  s.lastHit = { t: G.t, hitAndRun: false };
  s.amb = { pid: h.pid, calledAt: null, arrivesAt: null, x: h.x, z: h.z, since: G.t, days: h.days, helped: true };
  sub(`You stop and get out. ${tomName(P)} is hurt badly, and alive. Somebody must ring: the phone box on Chapel Lane corner, the office, or a neighbour.`, '', 'over', 8);
  note(`Knocked ${P.anon ? P.def.desc : P.def.name} down with the cab, and stopped. People saw him beside the car.`, 'note', 'hit:' + Math.round(h.t), { who: P.anon ? undefined : P.id, how: 'Was there' });
  logLine('Stopped to help after a hit: ' + r.costsGameMinutes + ' game minutes, the firm pays for ' + r.firmDays + ' days', 'car');
  emit('carhit:answer', { who: h.pid, choice: 'help' });
}
function driveOff() {
  const s = x(),
    h = s.hit;
  if (!h) return;
  const P = G.people[h.pid];
  s.hit = null;
  act('hit_run', P.anon ? { name: P.def.desc, noiseR: 30 } : { target: P.id, noiseR: 30 });
  const r = C.afterHit(T(), 'off');
  s.lastHit = { t: G.t, hitAndRun: true };
  s.wanted = { until: G.t + r.firmDays * 1440, why: 'a hit-and-run', since: G.t };
  // somebody always rings for the person in the road: a car never kills, and nobody is left lying
  s.amb = { pid: h.pid, calledAt: null, arrivesAt: null, x: h.x, z: h.z, since: G.t, days: h.days, helped: false };
  sub(s.sign ? "You drive on. Behind you somebody is shouting the name on the roof." : 'You drive on. Behind you somebody is shouting the colour of the car.', '', 'over', 6);
  note(`Knocked ${P.anon ? P.def.desc : P.def.name} down with the cab and drove on. The car will be described.`, 'note', 'hit:' + Math.round(h.t), { who: P.anon ? undefined : P.id, how: 'Was there' });
  emit('carhit:answer', { who: h.pid, choice: 'off' });
  emit('police:reported', { E: null, by: 'the street', why: 'a hit-and-run' });
}
function hitStep(dt) {
  const s = x(),
    h = s.hit,
    t = G.tom,
    c = G.car;
  if (!h) return;
  h.real += dt;
  const d = hyp(t.inCar ? c.x : t.x, t.inCar ? c.z : t.z, h.x, h.z);
  if (!t.inCar && d < T().drivesOffBeyondMetres) return help(); // he got out beside them: that is stopping
  if (d > T().drivesOffBeyondMetres * 2 || (h.real > T().choiceStandsRealSeconds && d > T().drivesOffBeyondMetres)) driveOff();
}

// ---------- the ambulance (A22; ER-AMB-01) ----------
function ring(how) {
  const a = x().amb;
  if (!a || a.calledAt != null) return false;
  a.calledAt = G.t;
  a.arrivesAt = C.ambulance(T(), G.t);
  a.how = how;
  sub(how === 'neighbour' ? 'Somebody has run to the phone box. An ambulance is coming.' : 'The ambulance is coming. Ten minutes, they say.', '', 'over', 5);
  return true;
}
function ambStep(dt) {
  const s = x(),
    a = s.amb,
    t = G.tom;
  if (!a) return;
  const P = G.people[a.pid];
  if (!P) return (s.amb = null);
  if (a.calledAt == null) {
    // a neighbour rings if he does not: anybody awake on the street near enough
    if (G.t - a.since >= T().neighbourRingsAfterGameMinutes) {
      const near = G.named.concat(G.crowd).some((Q) => Q !== P && !Q.gone && !Q.down && Q.space === 'street' && hyp(Q.x, Q.z, a.x, a.z) < T().neighbourRingsWithinMetres);
      if (near || G.t - a.since >= T().neighbourRingsAfterGameMinutes * 4) ring('neighbour');
    }
    return;
  }
  if (!RT.amb && t.space === 'street') {
    // it comes in along the road from the edge of the map, timed to its minute
    const from = hyp(a.x, a.z, EXITS.N[0], EXITS.N[1]) < 140 ? [1.9, a.z - 80] : a.x < 0 ? [a.x - 80, 46.2] : [a.x + 80, 49.8];
    RT.amb = addActor('van', '#e8e6de', { ambulance: true }, clamp(from[0], -124, 156), clamp(from[1], -204, 50), 0);
    if (RT.amb) RT.amb.to = routePoints({ x: RT.amb.x, z: RT.amb.z }, { x: a.x, z: a.z });
  }
  if (RT.amb && G.t < a.arrivesAt) {
    const pts = RT.amb.to,
      p = pts[RT.amb.i || 0] || [a.x, a.z];
    if (driveActor(RT.amb, p[0], p[1], 13, dt, false) < 4) RT.amb.i = (RT.amb.i || 0) + 1;
    if (RT.amb.car.lamp) RT.amb.car.lamp.color.setRGB(0.2, 0.5, (RT.real * 4) % 2 < 1 ? 3 : 0.6);
  }
  if (G.t >= a.arrivesAt) {
    // there at its minute, every time: the hurt person goes to hospital for the days the hurt sets
    P.down = false;
    P.downT = 0;
    P.gone = true;
    P.hold = false;
    P.override = { where: 'off', act: 'idle', until: G.t + Math.max(0.25, a.days) * 1440 };
    s.amb = null;
    a.arrivedAt = G.t;
    s.lastAmb = a;
    if (hyp(t.x, t.z, a.x, a.z) < 60 && t.space === 'street') sub(`The ambulance takes ${tomName(P)} to the Infirmary.${a.days ? ' ' + cap1(a.days === 1 ? 'a day' : a.days + ' days') + ', they say.' : ''}`, '', 'over', 5);
    logLine(`Ambulance arrived for ${P.def.name} ${Math.round(G.t - a.calledAt)} game minutes after the call`, 'car');
    if (RT.amb) {
      const v = RT.amb;
      RT.amb = null;
      RT.gone = (RT.gone || []).concat([{ v, t: 6 }]);
    }
  }
}

// ---------- a cab that will not drive on (ER-DRIVE-01), fetched and mended ----------
function carDead(what, hitMph) {
  const s = x();
  if (s.have === 'taken') {
    // a taken car wrecked: he walks, and it stays where it stopped
    leaveTaken(true);
    return;
  }
  s.offRoadUntil = G.t + T().offTheRoadGameMinutes;
  s.deadAt = { x: G.car.x, z: G.car.z, t: G.t };
  act('car_dead', { noiseR: 40 });
  note(`Wrecked the cab on ${what} at about ${Math.round(hitMph)} miles an hour. The firm fetches it, and it is off the road a day.`, 'note', 'cardead:' + Math.floor(G.t / 1440));
}
function deadStep() {
  const s = x(),
    t = G.tom,
    c = G.car;
  if (s.deadAt && !t.inCar && (hyp(t.x, t.z, c.x, c.z) > 30 || t.space !== 'street' || G.t - s.deadAt.t > 60)) {
    s.deadAt = null;
    c.x = HOME.x;
    c.z = HOME.z;
    c.ang = HOME.ang;
    c.v = 0;
    if (t.space === 'street') sub('Kevin has towed the cab back to the yard. Tomorrow, he says, if the parts come.', '', 'over', 5);
  }
}

// ---------- the horn (A32) ----------
function horn(long) {
  const t = G.tom,
    c = G.car,
    reach = C.hornReach(T(), hour(), G.weather.rain),
    heard = [];
  if (G.hooks.sfx) G.hooks.sfx('horn');
  for (const P of G.named.concat(G.crowd)) {
    if (P.gone || P.dead || P.inCar) continue;
    const px = P.space === 'street' ? P.x : P.def && P.home ? P.home[0] : null,
      d = P.space === 'street' ? hyp(P.x, P.z, c.x, c.z) : 999;
    void px;
    if (!C.hornHeard(T(), hour(), G.weather.rain, d)) continue;
    heard.push(P.id);
    if (P.awake !== false) P.alert = { x: c.x, z: c.z, t: 3 }; // a head turns, like any noise
    // somebody in the road ahead steps aside
    const fx = Math.sin(c.ang),
      fz = Math.cos(c.ang),
      rx = P.x - c.x,
      rz = P.z - c.z,
      f = rx * fx + rz * fz,
      side = rx * fz - rz * fx;
    if (f > 0 && f < T().hornStepsAsideWithinMetres && Math.abs(side) < 1.6 && !P.down && !P.hold) {
      const k = side >= 0 ? 1 : -1,
        nx = P.x + fz * k * 1.6,
        nz = P.z - fx * k * 1.6;
      if (footClear(nx, nz, 0.35)) {
        P.x = nx;
        P.z = nz;
      }
    }
  }
  // a toot outside a door brings out a fare he is waiting for
  const f = G.story.fare;
  let fareOut = null;
  if (f && f.st === 'pickup') {
    const d = hyp(c.x, c.z, f.sx, f.sz),
      secs = C.hornBringsOut(T(), d);
    if (secs != null) {
      fareOut = secs;
      f.px = c.x;
      f.pz = c.z; // they come to the car: he need only be stopped
      f.hornAt = RT.real;
      const P = G.people[f.pid];
      if (P) sub('Coming!', tomName(P), 'face', 2.5);
    }
  }
  // a long blast in a quiet street at night is remembered as a noise, and draws a look from lit windows
  const night = hour() >= T().hornNightFromHour || hour() < T().hornNightUntilHour;
  if (long && night) act('horn_night', { noiseR: reach });
  else t.noiseP = Math.max(t.noiseP || 0, Math.min(reach, 40));
  return { reachMetres: Math.round(reach), heard, fareOutInRealSeconds: fareOut, remembered: !!(long && night) };
}

// ---------- the patrol car, stops and chases (A12; ER-TRAFFIC-01, 02; ER-POL-04) ----------
const LOOP = [
  [1.9, -196], [1.9, 38], [6, 46.2], [150, 46.2], [152, 49.8], [-118, 49.8], [-120, 46.2], [-8, 46.2], [-1.9, 40], [-1.9, -196], [1.9, -200],
];
function patrolStep(dt) {
  const s = x(),
    t = G.tom,
    c = G.car;
  if (!RT.patrol) {
    if (!SYNC.cab) return;
    RT.patrol = addActor('saloon', '#e9e7df', { police: true }, LOOP[3][0] - 40, LOOP[3][1], Math.PI / 2);
    if (!RT.patrol) return;
    RT.patrol.i = 3;
  }
  const v = RT.patrol,
    st = s.stop,
    d = hyp(v.x, v.z, c.x, c.z),
    sees = t.inCar && t.space === 'street' && d <= T().patrolSeesWithinMetres && los(v.x, v.z, c.x, c.z);
  if (v.car.lamp) v.car.lamp.color.setRGB(0.2, 0.5, st ? ((RT.real * 5) % 2 < 1 ? 3.2 : 0.5) : 0.9);
  if (!st) {
    // his round of the Hook, by day and by night
    const p = LOOP[v.i % LOOP.length];
    if (driveActor(v, p[0], p[1], T().patrolCruiseMetresPerSecond, dt, false) < 4) {
      v.i = (v.i + 1) % LOOP.length;
      const q = LOOP[v.i];
      if (hyp(v.x, v.z, q[0], q[1]) < 8) {
        // the turn at the end of a road: round on the spot, out of anybody's way
        v.x = q[0];
        v.z = q[1];
        v.i = (v.i + 1) % LOOP.length;
        const n = LOOP[v.i];
        v.ang = Math.atan2(n[0] - v.x, n[1] - v.z);
      }
    }
    if (!t.inCar || G.paused) return;
    // a stop starts only on a reckless act an officer saw; ordinary driving is never stopped
    const onPave = Math.abs(c.v) > 3 && PAVE.some((r) => inRect(c.x, c.z, r)),
      did = { hitAPerson: RT.real - RT.lastRealHit < 4, onThePavement: onPave, redLightAtSpeed: false, mph: mph(c.v) },
      r = C.stop(T(), did, { inLineOfSight: sees, metres: d });
    let why = r.stop ? r.why : null;
    if (!why && sees && s.wanted && s.wanted.until > G.t && s.have === 'cab') why = 'the car is described';
    if (!why && sees && s.have === 'taken' && s.taken && s.taken.reported) why = 'a car reported taken';
    if (why) {
      s.stop = { st: 'flash', why, t: 0, unseen: 0, slow: 0, el: 0 };
      s.stops++;
      RT.crumbs = [];
      if (G.hooks.sfx) G.hooks.sfx('shout');
      sub('A blue lamp in the mirror, and two notes on a horn. He wants you to pull over.', '', 'over', 6);
    }
    return;
  }
  // he comes after the cab the way the cab went: never through a wall
  st.t += dt;
  crumb();
  const target = RT.crumbs.length ? RT.crumbs[0] : [c.x, c.z];
  if (hyp(v.x, v.z, target[0], target[1]) < 5 && RT.crumbs.length) RT.crumbs.shift();
  const close = d < 9;
  driveActor(v, target[0], target[1], st.st === 'chase' ? T().patrolTopMetresPerSecond : Math.min(T().patrolTopMetresPerSecond, Math.abs(c.v) + 3), dt, close && Math.abs(c.v) < 1);
  const slow = Math.abs(c.v) < T().stopPulledOverBelowMetresPerSecond;
  if (st.st === 'flash') {
    st.slow = slow ? st.slow + dt : 0;
    if (slow && st.slow > 1.2 && d < 30) return pulledOver();
    if (!t.inCar) return pulledOver(); // he has got out and stood: the same
    if (st.t > T().stopRefusedAfterRealSeconds) {
      st.st = 'chase';
      st.el = 0;
      act('stop_refused', { noiseR: 40 });
      sub('You do not stop. The lamp stays in the mirror, and now he is after you.', '', 'over', 5);
    }
    return;
  }
  // the chase: always over within 90 seconds, always lost by breaking sight
  st.el += dt;
  st.unseen = sees ? 0 : st.unseen + dt;
  st.slow = Math.abs(c.v) < T().chaseCaughtBelowMetresPerSecond || !t.inCar ? st.slow + dt : 0;
  const tx = t.inCar ? c.x : t.x,
    tz = t.inCar ? c.z : t.z,
    out = C.chase(T(), { metresApart: hyp(v.x, v.z, tx, tz), slowSeconds: st.slow, unseenSeconds: st.unseen, elapsedSeconds: st.el });
  if (out === 'caught') takenIn(T().custodyHoursForDrivingOff, st.why + ', and not stopping');
  else if (out === 'lost') {
    s.stop = null;
    s.plateNoted = 1;
    if (!s.wanted || s.wanted.until < G.t + 2880) s.wanted = { until: G.t + 2880, why: 'failing to stop', since: G.t };
    RT.lastChase = { out: 'lost', seconds: Math.round(st.el) };
    sub(s.sign ? 'You have lost him. He has the plate, and the name on the roof.' : 'You have lost him. He has the plate.', '', 'over', 5);
    note('Drove off from a patrol car and lost it. They have the plate.', 'note', 'chase:' + Math.floor(G.t / 60));
  }
}
function crumb() {
  const c = G.car,
    t = G.tom,
    px = t.inCar ? c.x : t.x,
    pz = t.inCar ? c.z : t.z,
    last = RT.crumbs[RT.crumbs.length - 1];
  if (!last || hyp(last[0], last[1], px, pz) > 3) RT.crumbs.push([px, pz]);
  if (RT.crumbs.length > 200) RT.crumbs.shift();
}
function pulledOver() {
  const s = x(),
    st = s.stop;
  if (!st || st.busy) return;
  st.busy = true;
  s.plateNoted = 1;
  const carrying = (G.x.fares && G.x.fares.carrying) || (G.story.job && G.story.job.carrying ? 'a bag that is not his' : null) || (G.tom.weapon ? 'a ' + G.tom.weapon : null);
  const cause = st.why === 'a hit' || st.why === 'the car is described' || st.why === 'a car reported taken';
  scene(async () => {
    await say('A patrol constable', `Engine off. ${st.why === 'speed' ? 'Do you know what this road is marked at?' : st.why === 'the pavement' ? 'The pavement is for feet.' : st.why === 'a hit' ? 'Out of the car. There is somebody lying in the road back there.' : st.why === 'the car is described' ? 'Out of the car. This car has been described to us.' : st.why === 'a car reported taken' ? 'Out of the car. This is not your car, is it.' : 'A word.'}`);
    if (cause) {
      s.stop = null;
      await takenIn(st.why === 'a car reported taken' ? 6 : st.why === 'a hit' ? 8 : 6, st.why, true);
      return;
    }
    await say('A patrol constable', `He walks round the car and writes the plate in his book.${carrying ? ' He looks at the back seat, and has no cause to look harder. This time.' : ''}`);
    await say('A patrol constable', 'A caution. I know the car now. Mind how you go.');
    act('stop_taken', { silent: false });
    advanceTo(G.t + T().stopTakesGameMinutes, false);
    s.stop = null;
    RT.lastStop = { why: st.why, gameMinutes: T().stopTakesGameMinutes };
    note('Pulled over by the patrol car for ' + st.why + '. A caution, and the plate is in his book.', 'note', 'stop:' + Math.floor(G.t / 60));
  });
}
// Taken in: hours lost, never the game, and never twice for one deed (ER-POL-03).
async function takenIn(hours, why, inScene) {
  const s = x(),
    t = G.tom;
  s.stop = null;
  s.wanted = null; // he is never taken twice for the one deed
  RT.lastChase = { out: 'caught', why };
  const run = async () => {
    await fade(true, `They take you in for ${why}.\n${cap1(hours === 6 ? 'six' : hours === 8 ? 'eight' : String(hours))} hours, a duty solicitor, and a caution written down.\nThe street saw you go.`);
    if (s.have === 'taken') leaveTaken(true);
    t.inCar = false;
    G.car.v = 0;
    advanceTo(G.t + hours * 60);
    t.space = 'street';
    t.x = SPOTS.door[0] - 1;
    t.z = SPOTS.door[1];
    G.car.x = HOME.x;
    G.car.z = HOME.z;
    G.car.ang = HOME.ang;
    if (G.hooks.leaveRoom && t.space !== 'street') G.hooks.leaveRoom();
    await fade(false);
  };
  if (inScene) await run();
  else await scene(run);
  emit('arrest', { E: null, hours, outcome: 'cautioned', why });
  note(`Taken in for ${why}: ${hours} hours lost, and a caution.`, 'note', 'takenin:' + Math.floor(G.t / 60));
  if (G.hooks.save) G.hooks.save();
}

// ---------- tails by car (A2; ER-TAIL-01 to 03) ----------
function tailStart(what, f) {
  if (RT.van) removeActor(RT.van.v);
  const from = { x: 1.9, z: -22 },
    to = { x: 62, z: 46.2 },
    pts = routePoints(from, to),
    v = addActor('van', '#dcdad2', { lettering: ['JENSEN & SON', 'FISH'] }, from.x, from.z, 0);
  if (!v) return null;
  RT.van = { v, pts, i: 0, s: { doubt: 0, made: false }, look: 6, n: 0, slowT: 0, arrived: false, learned: false, shows: [], fareId: f ? f.id : null, name: 'the white van', place: 'the fish dock' };
  return RT.van;
}
function tailStep(dt) {
  const k = RT.van;
  if (!k) return;
  const c = G.car,
    v = k.v,
    t = G.tom,
    d = hyp(v.x, v.z, c.x, c.z);
  if (k.arrived) {
    // he has stopped where he was going: seeing him there is what the tail learns
    if (!k.learned && !k.s.made && d < T().tailArrivesWithinMetres * 2 && los(v.x, v.z, t.inCar ? c.x : t.x, t.inCar ? c.z : t.z)) learn(k);
    k.gone = (k.gone || 0) + dt;
    if (k.gone > 120 && d > 60) {
      removeActor(v);
      RT.van = null;
    }
    return;
  }
  k.slowT -= dt;
  const p = k.pts[k.i];
  const left = driveActor(v, p[0], p[1], k.s.made ? 12 : k.slowT > 0 ? 3.5 : 7, dt, false);
  let corner = false;
  if (left < 4) {
    k.i++;
    corner = true;
    if (k.i >= k.pts.length) {
      k.arrived = true;
      v.v = 0;
      v.parked = true;
      return;
    }
  }
  // he looks in his mirror on a rhythm, and at every corner; only then can he catch the car behind (no hidden distance)
  k.look -= dt;
  if (k.look <= 0 || corner) {
    k.n++;
    k.look = T().tailLooksEveryRealSecondsAtLeast + ((k.n * 37) % 9);
    const r = C.tail(T(), k.s, { looks: true, inSight: t.inCar && los(v.x, v.z, c.x, c.z), metres: d, roofSign: x().sign });
    k.s = { doubt: r.doubt, made: r.made };
    if (r.shows) k.shows.push({ shows: r.shows, metres: Math.round(d), real: Math.round(RT.real) });
    if (r.shows === 'doubt') {
      k.slowT = 3; // the doubt shows first: his brake lights, a change of pace
      sub('The van slows. His brake lights: he is looking in his mirror. Hang back.', '', 'over', 5);
    } else if (r.shows === 'made') {
      act('tail_made', { name: k.name });
      sub('The van pulls away hard. He has made the cab.', '', 'over', 5);
      note(`Followed ${k.name} in the cab and was seen doing it. Whoever drives it knows a Mickey's car was behind him.`, 'note', 'tail:' + Math.floor(G.t / 60));
      emit('rival:move', { rival: 'jensen', kind: 'saw', what: 'a cab of his followed our van' });
    }
  }
}
function learn(k) {
  k.learned = true;
  // what a tail learns is in the Ledger within a game minute (ER-TAIL-03)
  note(`${cap1(k.name)} goes from Rita's corner to ${k.place}, and stands by the boxes there.`, 'note', 'tail:learned:' + Math.floor(G.t / 1440), { how: 'Followed it' });
  sub('The van pulls in by the fish boxes and stops. That is where it goes.', '', 'over', 5);
}
function tailEnd(f) {
  const k = RT.van;
  if (!k || k.fareId !== f.id) return null;
  if (k.s.made) return 'made by the van';
  if (!k.learned) learn(k); // losing sight is not failing: she knows where he will be, and now so does Tom
  return 'followed the van';
}

// ---------- a car in the mirror (being tailed) ----------
function mirrorStart(f) {
  const c = G.car;
  if (RT.mirror) removeActor(RT.mirror.v);
  const v = addActor('saloon', '#6f7274', {}, c.x - Math.sin(c.ang) * 22, c.z - Math.cos(c.ang) * 22, c.ang);
  if (!v) return null;
  RT.mirror = { v, crumbs: [], unseen: 0, lost: false, fareId: f ? f.id : null, t: 0 };
  return RT.mirror;
}
function mirrorStep(dt) {
  const m = RT.mirror;
  if (!m || m.lost) return;
  const c = G.car,
    v = m.v,
    F = RULES.game.fares,
    last = m.crumbs[m.crumbs.length - 1];
  m.t += dt;
  if (!last || hyp(last[0], last[1], c.x, c.z) > 3) m.crumbs.push([c.x, c.z]);
  // he keeps his distance along the way the cab went
  let along = 0;
  for (let i = m.crumbs.length - 1; i > 0; i--) along += hyp(m.crumbs[i][0], m.crumbs[i][1], m.crumbs[i - 1][0], m.crumbs[i - 1][1]);
  const d = hyp(v.x, v.z, c.x, c.z),
    tgt = m.crumbs[0] || [c.x, c.z];
  driveActor(v, tgt[0], tgt[1], 9, dt, along < F.mirrorFollowsAtMetres);
  if (hyp(v.x, v.z, tgt[0], tgt[1]) < 4 && m.crumbs.length > 1) m.crumbs.shift();
  m.unseen = los(v.x, v.z, c.x, c.z) ? 0 : m.unseen + dt;
  if (m.unseen > F.mirrorLostAfterUnseenRealSeconds || d > F.mirrorLostBeyondMetres) {
    m.lost = true;
    removeActor(v);
    sub('The grey saloon is gone from the mirror.', '', 'over', 4);
  }
}
function mirrorEnd(f, P) {
  const m = RT.mirror;
  if (!m || m.fareId !== f.id) return null;
  RT.mirror = null;
  if (m.lost) return 'lost the saloon';
  removeActor(m.v);
  sub('The grey saloon rolls past the door, slowly, and on. Somebody knows this address now, and which firm brought him.', '', 'over', 7);
  note(`A grey saloon followed the cab to ${P.anon ? 'a fare' : P.def.name}'s door. Whoever sent it knows the address, and the name on the roof.`, 'note', 'mirror:' + Math.floor(G.t / 60));
  emit('rival:move', { rival: null, kind: 'saw', what: 'followed his cab to a door' });
  return 'followed to the door';
}

// ---------- riding as a passenger (A24; ER-RIDE-01) ----------
const RIDE_TO = ['rank', 'station', 'ferry', 'fishdock', 'row', 'chapel', 'boarding', 'infirmary', 'market'];
async function ride(driver, toKey, skip) {
  const s = x(),
    t = G.tom,
    c = G.car,
    p = PLACES_F[toKey],
    from = { x: t.x, z: t.z },
    legs = FR.fns.legs(ROADS_F, from, { x: p.p[0], z: p.p[1] }),
    metres = FR.fns.metres(legs),
    mins = C.rideGameMinutes(T(), metres, RULES.time.realSecondsPerGameHour);
  if (skip) {
    await fade(true, `${driver} runs you to ${p.n}.`);
    advanceTo(G.t + mins, false);
    t.x = p.p[0] + (Math.abs(p.p[0]) < 8 ? (p.p[0] >= 0 ? 3 : -3) : 0);
    t.z = p.p[1] + (Math.abs(p.p[0]) < 8 ? 0 : p.p[1] < 48 ? -3.6 : 3.6);
    snapCam();
    await fade(false);
    s.lastRide = { to: toKey, gameMinutes: mins, skipped: true };
    return mins;
  }
  // he is driven: the car comes to him, he gets in the back, and the driver keeps to the lanes and brakes for people
  s.ride = { home: { x: c.x, z: c.z, ang: c.ang }, to: toKey, who: driver, t0: G.t, mins };
  const on = FR.fns.onRoad(ROADS_F, from),
    R = ROADS_F[on.id],
    start = R.axis === 'z' ? [R.at + (legs[0] && legs[0].heads === 'north' ? -1.9 : 1.9), on.along] : [on.along, R.at + (legs[0] && legs[0].heads === 'west' ? 1.9 : -1.9)];
  c.x = start[0];
  c.z = start[1];
  c.ang = legs[0] ? { north: Math.PI, south: 0, east: Math.PI / 2, west: -Math.PI / 2 }[legs[0].heads] : 0;
  c.v = 0;
  restyleCar(SYNC.cab, '#6a1f24', true);
  t.inCar = true;
  s.auto = { pts: lanePoints(legs), i: 0, to: toKey, who: driver, said: 0 };
  sub(`${p.n}. ${FR.fns.words(legs, JUNCTIONS_F, cap1(p.landmark))}`, driver, 'face', 7);
  return mins;
}
function rideStep(dt) {
  const s = x(),
    a = s.auto,
    t = G.tom,
    c = G.car;
  if (!a) return;
  if (!t.inCar) return rideOver(false);
  a.t = (a.t || 0) + dt;
  if (a.said === 0 && a.t > 8) {
    a.said = 1;
    sub(a.who.startsWith('Kevin') ? 'Quiet today. It is always quiet now. Your uncle would have had us on the ferry rank.' : 'Nights you see who is about. I say nothing. I just see it.', a.who, 'face', 6);
  }
  if (autoDrive(a.pts, a, T().rideCruiseMetresPerSecond, dt)) rideOver(true);
}
function rideOver(arrived, skipped) {
  const s = x(),
    t = G.tom,
    c = G.car,
    a = s.auto,
    r = s.ride;
  if (!a) return;
  s.auto = null;
  if (skipped) {
    // the rest of the drive passes on the clock: exactly its drive time (ER-RIDE-01)
    const left = r.t0 + r.mins - G.t;
    if (left > 0) advanceTo(G.t + left, false);
    const p = PLACES_F[a.to].p;
    c.x = p[0];
    c.z = p[1];
  }
  if (t.inCar) {
    const [ex, ez] = exitPoint();
    t.inCar = false;
    t.x = ex;
    t.z = ez;
  }
  s.lastRide = { to: a.to, gameMinutes: G.t - r.t0, skipped: !!skipped };
  // the driver pulls away; Tom's own car is where he left it
  c.x = r.home.x;
  c.z = r.home.z;
  c.ang = r.home.ang;
  c.v = 0;
  s.ride = null;
  restyleCar(SYNC.cab, s.paint, s.sign);
  snapCam();
  if (arrived || skipped) sub(`${a.who.split(' ')[0]} drops you at ${PLACES_F[a.to].n} and pulls away.`, '', 'over', 4);
}

// ---------- paint (A24; ER-PAINT-01) ----------
const look = () => ({ paint: x().paint, sign: x().sign, plate: x().plate });
function respray() {
  const s = x();
  s.plate++;
  s.paint = PAINTS[s.plate % PAINTS.length];
  s.sign = false;
  s.offRoadUntil = Math.max(s.offRoadUntil, G.t + T().resprayTakesGameMinutes);
  s.wanted = null; // the car that was described is not this car any more
  restyleCar(SYNC.cab, s.paint, s.sign);
  act('car_repaint', { silent: true, told: ['shaun'] });
  note("Shaun Hewson has the car in his shed: a new colour, other plates, the roof sign off. Nobody who saw the old paint will name this car.", 'note', 'paint:' + s.plate, { who: 'shaun', how: 'Paid for it' });
}
function signBack() {
  const s = x();
  s.sign = true;
  s.paint = FIRM_PAINT;
  restyleCar(SYNC.cab, s.paint, s.sign);
}
// does a deed seen from the car name the car as it stands now?
function named(eventId) {
  const r = x().seen.find((q) => q.e === eventId);
  if (!r) return { names: false, firm: false, seen: false };
  return Object.assign({ seen: true }, C.names(r, look()));
}

// ---------- taking a parked car (A27; ER-TAKE-01) ----------
function parkedNear() {
  const t = G.tom;
  for (const v of SYNC.traffic) {
    if (!v.parked || !v.car.g.visible || v === RT.standing) continue;
    if (hyp(t.x, t.z, v.x, v.z) < T().takeWithinMetres) return v;
  }
  return null;
}
function forceStart(v) {
  const s = x();
  if (s.have === 'taken' || RT.forcing) return;
  const r = C.take(T(), { occupied: !v.parked }, G.t);
  if (!r.can) return sub('Somebody is in it.', '', 'over', 3);
  RT.forcing = { v, t: r.seconds };
  G.tom.noiseP = Math.max(G.tom.noiseP || 0, r.loudMetres);
  if (G.hooks.sfx) G.hooks.sfx('crash');
  sub('The quarter-light goes in with a crack the whole street can hear. Six seconds to the ignition.', '', 'over', 5);
}
function forceStep(dt) {
  const f = RT.forcing,
    t = G.tom;
  if (!f) return;
  if (hyp(t.x, t.z, f.v.x, f.v.z) > T().takeWithinMetres + 1 || t.inCar) {
    RT.forcing = null;
    return sub('You leave it, with its window in.', '', 'over', 3);
  }
  f.t -= dt;
  t.noiseP = Math.max(t.noiseP || 0, T().takeForceNoiseMetres * 0.6);
  if (f.t <= 0) {
    RT.forcing = null;
    takeCar(f.v);
  }
}
const KIND_NAME = { saloon: 'a saloon', hatch: 'a hatchback', van: 'a van', flatbed: 'a flatbed lorry' };
function takeCar(v) {
  const s = x(),
    c = G.car,
    t = G.tom,
    name = KIND_NAME[v.car.kind] || 'a parked car';
  act('car_taken', { noiseR: T().takeForceNoiseMetres, name });
  // the firm's cab stays where it stands; he drives the other
  s.standing = { x: c.x, z: c.z, ang: c.ang };
  s.cabDmg = c.dmg;
  RT.standing = addActor('saloon', s.paint, { cab: true }, c.x, c.z, c.ang, true);
  if (RT.standing) restyleCar(RT.standing.car, s.paint, s.sign);
  RT.takenCar = v;
  v.car.g.visible = false;
  const i = SYNC.traffic.indexOf(v);
  if (i >= 0) SYNC.traffic.splice(i, 1);
  c.x = v.x;
  c.z = v.z;
  c.ang = v.car.g.rotation.y;
  c.v = 0;
  c.dmg = 0;
  s.have = 'taken';
  s.taken = { at: G.t, name, reported: false, color: '#' + v.car.body.color.getHexString() };
  restyleCar(SYNC.cab, s.taken.color, false);
  t.inCar = true;
  sub(`It catches. ${cap1(name)}, no sign on the roof: not the firm's, which is the point. Its owner will find it gone.`, '', 'over', 6);
  note(`Took ${name} by force. No roof sign, so nobody will call it Mickey's. Its owner will report it when he finds it gone.`, 'note', 'took:' + Math.floor(G.t / 60));
}
// leave the taken car where it stands; the firm's cab is his car again
function leaveTaken(walk) {
  const s = x(),
    c = G.car,
    t = G.tom;
  if (s.have !== 'taken') return;
  const v = RT.takenCar;
  if (v) {
    v.x = c.x;
    v.z = c.z;
    v.car.g.position.set(c.x, 0, c.z);
    v.car.g.rotation.y = c.ang;
    v.car.g.visible = true;
    v.left = true;
    if (!SYNC.traffic.includes(v)) SYNC.traffic.push(v);
  }
  if (walk && t.inCar) {
    const [ex, ez] = exitPoint();
    t.inCar = false;
    t.x = ex;
    t.z = ez;
  }
  const st = s.standing || HOME;
  c.x = st.x;
  c.z = st.z;
  c.ang = st.ang;
  c.v = 0;
  c.dmg = s.cabDmg || 0;
  s.have = 'cab';
  s.standing = null;
  removeActor(RT.standing);
  RT.standing = null;
  RT.takenCar = null;
  restyleCar(SYNC.cab, s.paint, s.sign);
}

// ---------- the firm's name and the other firm (A14; ER-DRIVE-10) ----------
function faresLostShare() {
  const h = x().lastHit;
  return h ? C.faresLost(T(), (G.t - h.t) / 1440, h.hitAndRun) : 0;
}

register({
  id: 'cars',
  fresh,
  loaded(s) {
    const f = fresh();
    for (const k in f) if (s[k] === undefined) s[k] = f[k];
    // a save holds no chase, no ride and no taken car's body: he is on his feet with the firm's cab
    s.stop = null;
    s.auto = null;
    s.ride = null;
    if (s.have === 'taken') {
      const st = s.standing || HOME;
      G.car.x = st.x;
      G.car.z = st.z;
      G.car.ang = st.ang;
      G.car.dmg = s.cabDmg || 0;
      s.have = 'cab';
      s.standing = null;
    }
    for (const k of ['patrol', 'amb', 'standing']) {
      if (RT[k]) removeActor(RT[k]);
      RT[k] = null;
    }
    if (RT.van) removeActor(RT.van.v);
    if (RT.mirror) removeActor(RT.mirror.v);
    RT.van = RT.mirror = RT.forcing = null;
    RT.crumbs = [];
    if (SYNC.cab) restyleCar(SYNC.cab, s.paint, s.sign);
    Object.assign(G.hooks, { carHit, carDead, faresLostShare, tailStart, tailEnd, mirrorStart, mirrorEnd, carNamed: named, carLook: look });
  },
  step(dt) {
    const s = x(),
      t = G.tom;
    RT.real += dt;
    if (!G.hooks.carHit) Object.assign(G.hooks, { carHit, carDead, faresLostShare, tailStart, tailEnd, mirrorStart, mirrorEnd, carNamed: named, carLook: look });
    hitStep(dt);
    ambStep(dt);
    deadStep();
    patrolStep(dt);
    tailStep(dt);
    mirrorStep(dt);
    rideStep(dt);
    forceStep(dt);
    for (const g of RT.gone || []) {
      g.t -= dt;
      driveActor(g.v, g.v.x + Math.sin(g.v.ang) * 30, g.v.z + Math.cos(g.v.ang) * 30, 11, dt, false);
      if (g.t <= 0) removeActor(g.v);
    }
    if (RT.gone) RT.gone = RT.gone.filter((g) => g.t > 0);
    // the horn: a toot on the press, a long blast if it is held
    if (t.inCar && keys.KeyH) {
      RT.hornT += dt;
      if (RT.hornT > T().hornLongBlastRealSeconds && !RT.hornLong) {
        RT.hornLong = true;
        horn(true);
      }
    } else {
      RT.hornT = 0;
      RT.hornLong = false;
    }
    // looking back through the rear window while B is held (A24)
    if (t.inCar && keys.KeyB) {
      cam.yaw = G.car.ang + Math.PI;
      cam.idle = 0.6;
      s.lookingBack = 1;
    } else s.lookingBack = 0;
    // every deed done from the car is kept with how the car looked then (ER-EYES-10, ER-PAINT-01)
    for (let i = G.events.length - 1; i >= 0; i--) {
      const E = G.events[i];
      if (E.id <= s.lastE) break;
      if (E.car) s.seen.push(Object.assign({ e: E.id }, look()));
    }
    if (G.events.length) s.lastE = G.events[G.events.length - 1].id;
    if (s.seen.length > 300) s.seen.splice(0, 100);
  },
  minute() {
    const s = x();
    // the owner finds it gone, and reports it (ER-TAKE-01)
    if (s.taken && !s.taken.reported && C.take(T(), { occupied: false, takenAtMinute: s.taken.at }, G.t).reported) {
      s.taken.reported = true;
      s.taken.reportedAt = G.t;
      logLine(`The owner of ${s.taken.name} found it gone and reported it`, 'car');
      emit('police:reported', { E: null, by: 'the owner', why: 'a car taken' });
    }
    if (s.wanted && s.wanted.until <= G.t) s.wanted = null;
  },
  hourly(h) {
    const s = x(),
      c = G.car;
    // dents are mended overnight at the yard (A24)
    if (h === T().dentsMendedAtHour && s.have === 'cab' && hyp(c.x, c.z, HOME.x, HOME.z) < 45 && c.dmg > 0 && !G.tom.inCar && s.offRoadUntil <= G.t + 60) {
      c.dmg = 0;
      logLine('The cab was mended overnight at the yard', 'car');
    }
  },
  carPrompts(out) {
    const s = x();
    if (s.hit) {
      out.push({ k: 'Y', t: 'Stop and help', run: help });
      out.push({ k: 'G', t: 'Drive off', run: driveOff });
    }
    if (s.auto) out.push({ k: 'G', t: 'Skip the ride', run: () => rideOver(false, true) });
    if (s.stop && s.stop.st === 'flash') out.push({ k: '!', t: 'Pull over and stop, or keep driving' });
    else if (!G.story.fare && !s.hit && !s.auto) out.push({ k: 'H', t: 'Horn' });
  },
  hotspots(out) {
    const s = x(),
      t = G.tom;
    if (t.space !== 'street') {
      if (s.amb && s.amb.calledAt == null && t.space === 'mickeys') out.push({ k: 'E', t: 'Ring for an ambulance', run: () => ring('office') });
      return;
    }
    if (s.amb && s.amb.calledAt == null && hyp(t.x, t.z, 7.3, -13.2) < T().phoneReachMetres + 1) out.push({ k: 'E', t: 'Ring for an ambulance', run: () => ring('phone box') });
    if (s.hit && hyp(t.x, t.z, s.hit.x, s.hit.z) < 4) out.push({ k: 'E', t: 'See to them', run: help });
    if (s.have === 'taken' && RT.standing && hyp(t.x, t.z, RT.standing.x, RT.standing.z) < 3.4) out.push({ k: 'G', t: "Get in Mickey's cab", run: () => { leaveTaken(false); t.inCar = true; } });
    else if (s.have === 'cab' && !RT.forcing) {
      const v = parkedNear();
      if (v && hyp(t.x, t.z, G.car.x, G.car.z) > 3.2) out.push({ k: 'G', t: 'Force the car door (loud)', run: () => forceStart(v) });
    }
  },
  key(code) {
    if (code === 'KeyH' && G.tom.inCar && !x().auto) {
      horn(false);
      return true;
    }
    return false;
  },
  matters(P, a) {
    const s = x();
    if ((P.id === 'kevin' || P.id === 'terry') && !G.story.fare && !G.tom.inCar && !s.auto)
      a.push({
        key: 'ride',
        direct: true,
        ask: 'whether to be driven somewhere',
        raise: 'Want running anywhere, boss? Say where and I will take you.',
        opts: [
          {
            agree: 1,
            q: 'Shall I run you somewhere?',
            yes: ['Yes. Run me somewhere.', 'Yes. Drive me.'],
            no: ['No. I will walk.', 'No. Not now.'],
            keep: ['How long does it take?', 'Is the car all right?'],
            keepSay: 'Minutes, anywhere on the Hook. She pulls to the left, same as ever. Shall I run you somewhere?',
            noSay: 'Right you are.',
            take: async () => {
              endTalk();
              await scene(async () => {
                const names = RIDE_TO.map((k) => cap1(PLACES_F[k].n)),
                  i = await choose(P.id, 'Where to?', names.concat(['Nowhere. Leave it.']));
                if (i < 0 || i >= RIDE_TO.length) return;
                const j = await choose(P.id, `${cap1(PLACES_F[RIDE_TO[i]].n)}. Get in.`, ['Ride along', 'Skip the ride']);
                await ride(P.def.name, RIDE_TO[i], j === 1);
              });
            },
          },
        ],
      });
    if (P.id === 'shaun' && s.have === 'cab') {
      if (s.sign)
        a.push({
          key: 'paint',
          direct: true,
          ask: 'whether to have the car repainted so it is not known',
          raise: `I could make that cab not look like a cab. New colour, other plates, sign off the roof. ${cap1(pounds(T().resprayCostsPence))}, and she is in my shed ten hours.`,
          opts: [
            {
              agree: 1,
              q: `${cap1(pounds(T().resprayCostsPence))}. Do I paint her?`,
              yes: ['Yes. Paint it.', 'Yes. Sign off, new colour.'],
              no: ['No. Leave it as it is.', 'No. Not yet.'],
              keep: ['Who would know it after?', 'What colour?'],
              keepSay: 'Nobody who saw the old paint. Whatever I have most of. Do I paint her?',
              noSay: 'She will keep.',
              take: () => {
                if (!pay(T().resprayCostsPence, false, 'a respray at Hewson\'s shed')) return 'Paint costs money, pal. Come back with it.';
                respray();
                return 'Leave the keys. Ten hours. You never brought her here.';
              },
            },
          ],
        });
      else
        a.push({
          key: 'signback',
          direct: true,
          ask: "whether to make the car a Mickey's cab again",
          raise: 'Want the sign back on, and the blue? No charge for putting right.',
          opts: [
            {
              agree: 1,
              q: 'Blue again, sign on?',
              yes: ['Yes. Make it a cab again.', 'Yes. Put the sign back.'],
              no: ['No. Leave it plain.', 'No. Not yet.'],
              keep: ['Will folk know it again?', 'How long?'],
              keepSay: 'They will know a Mickey\'s cab when they see one. An hour. Blue again?',
              noSay: 'Plain it stays.',
              take: () => {
                signBack();
                return 'There. She is a cab again.';
              },
            },
          ],
        });
    }
  },
  hook: {
    state: () => x(),
    runtime: () => ({ patrol: RT.patrol ? { x: RT.patrol.x, z: RT.patrol.z } : null, van: RT.van ? { x: RT.van.v.x, z: RT.van.v.z, s: RT.van.s, shows: RT.van.shows, arrived: RT.van.arrived, learned: RT.van.learned } : null, mirror: RT.mirror ? { x: RT.mirror.v.x, z: RT.mirror.v.z, lost: RT.mirror.lost } : null, lastChase: RT.lastChase || null, lastStop: RT.lastStop || null, forcing: !!RT.forcing }),
    rules: C,
    tune: T,
    // stage a hit on this person at this speed (the test's way of driving into somebody)
    hit(pid, hitMph, aimed) {
      const P = G.people[pid],
        H = C.hurt(T(), hitMph, !!aimed, null);
      if (!P) return null;
      if (H.down) {
        P.down = true;
        P.hurt = clamp((P.hurt || 0) + H.hurt, 0, Math.max(P.hurt || 0, T().hurtAtMost));
        P.downT = G.t + (H.downGameMinutes || 20);
        act('knocked', { target: P.anon ? undefined : P.id, name: P.def.name, noiseR: 30 });
        carHit(P, hitMph, !!aimed, H);
      }
      return { rule: H, hurt: P.hurt, dead: !!P.dead, choicePut: !!x().hit };
    },
    help,
    driveOff,
    ring,
    horn,
    // put the cab into something at this speed (what one hit does)
    crash(hitMph) {
      const c = G.car,
        r = C.damage(T(), hitMph, c.dmg);
      c.dmg = r.damage;
      if (r.stage === 'dead') carDead('a lamp post', hitMph);
      return r;
    },
    faresLostShare,
    respray,
    signBack,
    named,
    look,
    takeNearest() {
      const v = parkedNear();
      if (!v) return null;
      takeCar(v);
      return x().taken;
    },
    forceNearest() {
      const v = parkedNear();
      if (v) forceStart(v);
      return !!RT.forcing;
    },
    leaveTaken: () => leaveTaken(true),
    parked: () => SYNC.traffic.filter((v) => v.parked).map((v) => ({ x: v.x, z: v.z, kind: v.car.kind })),
    tailStart: () => !!tailStart('van', null),
    mirrorStart: () => !!mirrorStart(null),
    ride: (who, to, skip) => ride(who, to, skip),
    rideSkip: () => rideOver(false, true),
    // have the patrol car beside the cab and looking (for a test of what it stops him for)
    patrolAt(px, pz) {
      if (!RT.patrol) patrolStep(0.01);
      if (!RT.patrol) return null;
      RT.patrol.x = px;
      RT.patrol.z = pz;
      RT.patrol.car.g.position.set(px, 0, pz);
      return { x: px, z: pz };
    },
    wanted(why) {
      x().wanted = { until: G.t + 1440, why: why || 'a hit-and-run', since: G.t };
    },
  },
});
void on;
void money;
