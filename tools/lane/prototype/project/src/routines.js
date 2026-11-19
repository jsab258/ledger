// People as agents: routines, walking, windows, the anonymous crowd. No rendering here.
import { hyp, clamp, rnd, pick, chance, angDiff } from './util.js';
import { G, day, hour, SECS_PER_HOUR } from './state.js';
import { CAST, KEEPERS } from './cast.js';
import { NODES, nearNode, path, SPOTS, ROOMS, WINDOWS, EXITS, roomPos, zoneAt } from './map.js';
import { newMind } from './events.js';
import { RULES } from './rules.js';
const CROWD = RULES.crowd;

const WALK = RULES.routines;

const HAIRS = [
  '#2a1a10',
  '#4a3020',
  '#6a4a2a',
  '#8a6a3a',
  '#1a1a1a',
  '#9a958a',
  '#c9c4ba',
  '#7a3b22',
  '#b98a4a',
];
const TOPS_M = [
  ['donkey', '#20242c', '#3a4250'],
  ['carcoat', '#6a5a40', '#2a2a2a'],
  ['anorak', '#2f4a6a', '#c8c0a8'],
  ['shell', '#5a2a7a', '#e0c020'],
  ['shell', '#1a6a5a', '#e04a8a'],
  ['jumper', '#5a3a2a', '#5a3a2a'],
  ['leather', '#2a2420', '#111'],
  ['duffel', '#4a4636', '#222'],
  ['denim', '#48689a', '#ddd'],
  ['overcoat', '#3a3a3e', '#222'],
  ['bomber', '#2a3a30', '#c85a1a'],
];
const TOPS_F = [
  ['mac', '#9a8a6a', '#2a2a2a'],
  ['cardigan', '#7a5a8a', '#e8e0d0'],
  ['anorak', '#a03a4a', '#e8e0d0'],
  ['shell', '#c03a8a', '#3ac0c0'],
  ['overcoat', '#5a4a3a', '#2a2a2a'],
  ['blouse', '#3a5a6a', '#e8e0d0'],
  ['denim', '#5a7aa8', '#eee'],
  ['jumper', '#8a3a3a', '#8a3a3a'],
  ['carcoat', '#4a5a48', '#222'],
];
export function randomLook(sex, older) {
  const m = sex === 'm',
    top = pick(m ? TOPS_M : TOPS_F);
  const hair = older
    ? pick(m ? ['balding', 'flatcap', 'short', 'woolly'] : ['set', 'headscarf', 'bun', 'rainhood'])
    : pick(
        m
          ? ['short', 'short', 'mullet', 'quiff', 'woolly', 'flatcap']
          : ['perm', 'perm', 'bob', 'long', 'set'],
      );
  return {
    h: m ? rnd(1.66, 1.88) : rnd(1.52, 1.72),
    b: rnd(0.15, 0.9),
    skin: chance(0.85) ? Math.floor(rnd(0, 3)) : Math.floor(rnd(3, 7)),
    hair: [hair, older ? pick(['#9a958a', '#c9c4ba', '#6a655a']) : pick(HAIRS)],
    top,
    bot: [
      m ? pick(['trousers', 'jeans', 'jeans', 'trackies']) : pick(['skirt', 'trousers', 'jeans']),
      pick(['#2a2a30', '#3a4560', '#3a3530', '#22222a', '#4a4a52']),
    ],
    x: chance(0.2) ? ['glasses'] : chance(0.2) ? ['bag'] : [],
  };
}

function mkPerson(id, def) {
  const mind = G.minds[id] || (G.minds[id] = newMind());
  mind.by = {};
  for (const m of mind.mem) mind.by[m.e] = m;
  mind.attn = 0;
  mind.look = 0;
  const P = {
    id,
    def,
    x: 0,
    z: 0,
    ang: 0,
    space: 'off',
    awake: true,
    gone: true,
    moving: false,
    state: 'idle',
    mind,
    route: null,
    goalKey: '',
    anim: {},
    v: 0,
  };
  const w = WINDOWS[id];
  if (w) P.win = { x: w[0], z: w[1], ang: w[2], y: w[3] };
  return P;
}
export function initPeople() {
  G.people = {};
  G.named = [];
  G.crowd = [];
  G.keepers = [];
  for (const def of CAST) {
    const P = mkPerson(def.id, def);
    P.dead = !!(G.story.flags.dead && G.story.flags.dead[def.id]);
    G.people[def.id] = P;
    G.named.push(P);
  }
  for (const k of KEEPERS) {
    const P = mkPerson(k.id, {
      id: k.id,
      name: k.desc,
      desc: k.desc,
      sex: k.sex,
      look: randomLook(k.sex, true),
      talk: CROWD.keeperTalkativeZeroToOne,
      nerve: CROWD.keeperNerveZeroToOne,
      voice: 'plain',
      bark: k.bark,
      age: CROWD.keeperAgeYears,
    });
    P.anon = true;
    P.keeper = k;
    G.people[k.id] = P;
    G.crowd.push(P);
    G.keepers.push(P);
    delete G.minds[k.id];
  }
  for (let i = 0; i < CROWD.walkersAtMost; i++) {
    const sex = chance(0.5) ? 'm' : 'f',
      old = chance(CROWD.walkerIsOldChance);
    const P = mkPerson('c' + i, {
      id: 'c' + i,
      name: 'a passer-by',
      desc: sex === 'm' ? 'a man' : 'a woman',
      sex,
      look: randomLook(sex, old),
      talk: CROWD.walkerTalkativeZeroToOne,
      nerve: rnd(CROWD.walkerNerveAtLeast, CROWD.walkerNerveAtMost),
      voice: 'plain',
      age: old ? CROWD.oldWalkerAgeYears : CROWD.walkerAgeYears,
      old,
    });
    P.anon = true;
    P.walker = true;
    G.crowd.push(P);
    delete G.minds['c' + i];
  }
  for (let i = 0; i < CROWD.ladsCount; i++) {
    const P = mkPerson('lad' + i, {
      id: 'lad' + i,
      name: "one of Cammack's lads",
      desc: 'a lad in a shell suit',
      sex: 'm',
      look: {
        h: rnd(1.76, 1.86),
        b: rnd(0.4, 0.7),
        skin: i,
        hair: [pick(['short', 'mullet']), pick(HAIRS)],
        top: ['shell', ['#7a1a8a', '#1a4aa0', '#0a7a6a'][i], ['#e8e020', '#e84a9a', '#f0f0f0'][i]],
        bot: ['trackies', '#1a1a2a'],
        x: [],
      },
      talk: CROWD.ladTalkativeZeroToOne,
      nerve: CROWD.ladNerveZeroToOne,
      voice: 'plain',
      age: CROWD.ladAgeYears,
      lad: 1,
    });
    P.anon = true;
    P.lad = true;
    G.crowd.push(P);
    delete G.minds['lad' + i];
  }
  for (let i = 0; i < CROWD.faresCount; i++) {
    const sex = i === 1 ? 'f' : 'm';
    const P = mkPerson('pax' + i, {
      id: 'pax' + i,
      name: 'a fare',
      desc: sex === 'm' ? 'a man with a bag' : 'a woman in a headscarf',
      sex,
      look: randomLook(sex, i === 1),
      talk: CROWD.fareTalkativeZeroToOne,
      nerve: CROWD.fareNerveZeroToOne,
      voice: 'plain',
      age: CROWD.fareAgeYears,
      sched: [],
    });
    P.anon = true;
    P.pax = true;
    G.people[P.id] = P;
    G.crowd.push(P);
    delete G.minds[P.id];
  }
  {
    const P = mkPerson('yardlad', {
      id: 'yardlad',
      name: "Iveson's yard lad",
      desc: 'a big lad in overalls',
      sex: 'm',
      exit: 'W',
      look: {
        h: 1.9,
        b: 0.9,
        skin: 1,
        hair: ['short', '#3a2a1a'],
        top: ['overall', '#3a4a5a', '#2a2a2a'],
        bot: ['trousers', '#3a4a5a'],
        x: [],
      },
      talk: CROWD.yardLadTalkativeZeroToOne,
      nerve: CROWD.yardLadNerveZeroToOne,
      voice: 'plain',
      age: CROWD.yardLadAgeYears,
      sched: [
        [0, 'off'],
        [CROWD.yardLadWorksFromHour, 'scraplad', 'work'],
        [CROWD.yardLadWorksUntilHour, 'off'],
      ],
    });
    P.anon = true;
    P.yardLad = true;
    G.people[P.id] = P;
    G.crowd.push(P);
    delete G.minds[P.id];
  }
  for (const P of G.named) placeNow(P);
  for (const P of G.crowd) placeNow(P);
}

// ---------- routines ----------
export function slot(P, h = hour(), d = day()) {
  if (P.override && (P.override.until === undefined || G.t < P.override.until)) return P.override;
  if (P.override) P.override = null;
  let best = null,
    bd = null;
  for (const s of P.def.sched || []) {
    if (s[0] > h) continue;
    if (s[3]) {
      if (s[3].includes(d % 7) && (!bd || s[0] >= bd[0])) bd = s;
    } else if (!best || s[0] >= best[0]) best = s;
  }
  const s = bd && (!best || bd[0] >= best[0]) ? bd : best;
  return s ? { where: s[1], act: s[2] || 'idle' } : { where: 'off', act: 'idle' };
}
function homePoint(P) {
  if (P.win) {
    const w = P.win;
    return [w.x + Math.sin(w.ang) * 0.9, w.z + Math.cos(w.ang) * 0.9, w.ang];
  }
  return SPOTS[P.def.homeSpot || 'chapelgate'];
}
const exitOf = (P) =>
  EXITS[P.def.exit || (['susan', 'lee', 'norman'].includes(P.id) ? 'E' : P.id === 'dennis' ? 'W' : 'N')];
// Resolve a place name to somewhere to stand.
export function resolve(P, where) {
  if (where === 'home') {
    const h = homePoint(P);
    return { kind: 'home', x: h[0], z: h[1], ang: h[2] };
  }
  if (where === 'off') {
    const e = exitOf(P);
    return { kind: 'off', x: e[0], z: e[1], ang: 0 };
  }
  const i = where.indexOf(':');
  if (i > 0) {
    const rid = where.slice(0, i),
      r = ROOMS[rid],
      s = r.spots[where.slice(i + 1)] || [0, 0, 0];
    const [wx, wz] = roomPos(rid, s[0], s[1]);
    return { kind: 'room', room: rid, x: wx, z: wz, ang: s[2], door: r.street };
  }
  const s = SPOTS[where] || SPOTS.pave;
  return { kind: 'street', x: s[0], z: s[1], ang: s[2] };
}
function placeNow(P) {
  // put someone where their routine says, with no walking (start, load, after sleep)
  if (P.dead) {
    P.gone = true;
    P.space = 'off';
    return;
  }
  if (P.keeper) {
    const r = ROOMS[P.keeper.room],
      s = r.spots[P.keeper.spot];
    const [x, z] = roomPos(r.id, s[0], s[1]);
    const open = hour() >= WALK.shopsOpenFromHour && hour() < WALK.shopsShutAtHour;
    P.x = x;
    P.z = z;
    P.ang = s[2];
    P.space = open ? r.id : 'off';
    P.gone = !open;
    P.state = 'work';
    return;
  }
  if (P.walker) {
    respawnWalker(P, true);
    return;
  }
  if (P.lad) {
    ladRoutine(P, true);
    return;
  }
  const sl = slot(P),
    g = resolve(P, sl.where);
  P.goalKey = sl.where + '|' + sl.act;
  P.route = null;
  P.moving = false;
  P.state = sl.act;
  P.x = g.x;
  P.z = g.z;
  P.ang = g.ang || 0;
  applyArrive(P, g, sl.act);
}
export function placeAll() {
  for (const P of G.named) placeNow(P);
  for (const P of G.crowd) placeNow(P);
}
// ---------- every walk, written down ----------
// When a named person sets off for a place, and when they get there (or turn for somewhere else first). This is
// what LEDGER.check.arrivals() reads. It is not saved.
export const TRIPS = [];
function tripEnds(P, how, g) {
  const T = P.trip;
  if (!T) return;
  P.trip = null;
  T.ended = how; // 'arrived', 'placed' (put there with no walking, as after sleep) or 'turned' (set off for another place)
  T.endedGameMinute = G.t;
  T.endX = P.x;
  T.endZ = P.z;
  T.endSpace = P.space;
  if (how === 'turned') T.turnedFor = g;
  TRIPS.push(T);
  if (TRIPS.length > 3000) TRIPS.splice(0, 500);
}
function tripStarts(P, g, legs, cameFrom) {
  tripEnds(P, 'turned', g);
  if (!P.def || P.anon || P.walker || P.lad) return;
  let metres = 0,
    px = P.x,
    pz = P.z;
  for (const leg of legs || []) {
    if (leg.x == null || leg.inRoom) continue;
    const d = Math.hypot(leg.x - px, leg.z - pz);
    if (d < 400) metres += d; // a step through a door into a room is not a walk along the street
    px = leg.x;
    pz = leg.z;
  }
  P.trip = {
    personId: P.id,
    goal: g,
    setOffGameMinute: G.t,
    fromX: P.x,
    fromZ: P.z,
    fromSpace: cameFrom,
    streetMetres: metres,
  };
}

function applyArrive(P, g, act) {
  tripEnds(P, P.moving ? 'arrived' : 'placed');
  P.gone = g.kind === 'off';
  P.space = g.kind === 'room' ? g.room : g.kind === 'home' ? 'home' : g.kind === 'off' ? 'off' : 'street';
  P.awake = act !== 'sleep';
  P.atWindow = g.kind === 'home' && act === 'window';
  P.winLit = false;
  P.state = act;
  P.moving = false;
  P.place = g.kind === 'room' ? ROOMS[g.room].name : g.kind === 'street' ? zoneAt(P.x, P.z) : '';
}

function planTo(P, g, act) {
  // legs: walk street path, then door transitions
  const legs = [],
    cameFrom = P.space;
  let sx = P.x,
    sz = P.z;
  if (P.space !== 'street') {
    if (P.space === 'home') {
      const h = homePoint(P);
      P.x = sx = h[0];
      P.z = sz = h[1];
      P.space = 'street';
      P.awake = true;
      P.atWindow = false;
    } else if (P.space === 'off') {
      const e = exitOf(P);
      P.x = sx = e[0] + rnd(-1, 1);
      P.z = sz = e[1];
      P.space = 'street';
      P.gone = false;
    } else {
      const r = ROOMS[P.space];
      if (g.kind === 'room' && g.room === P.space) {
        P.route = { legs: [{ x: g.x, z: g.z }], g, act };
        tripStarts(P, g, [], cameFrom);
        P.moving = true;
        return;
      }
      const [mx, mz] = roomPos(r.id, r.mat[0], r.mat[1]);
      legs.push({ x: mx, z: mz }, { warp: r.street, space: 'street' });
      sx = r.street[0];
      sz = r.street[1];
    }
  }
  const tx = g.kind === 'room' ? g.door[0] : g.x,
    tz = g.kind === 'room' ? g.door[1] : g.z;
  if (hyp(sx, sz, tx, tz) > WALK.takesThePathsBeyondMetres) {
    const a = nearNode(sx, sz),
      b = nearNode(tx, tz),
      off = P.lane ?? (P.lane = rnd(-WALK.laneOffsetAtMostMetres, WALK.laneOffsetAtMostMetres)),
      ns = path(a, b);
    while (
      ns.length > 1 &&
      hyp(sx, sz, NODES[ns[1]].x, NODES[ns[1]].z) <=
        hyp(NODES[ns[0]].x, NODES[ns[0]].z, NODES[ns[1]].x, NODES[ns[1]].z) + WALK.pathEndSlackMetres
    )
      ns.shift(); // never walk back to a node behind you
    while (
      ns.length > 1 &&
      hyp(tx, tz, NODES[ns[ns.length - 2]].x, NODES[ns[ns.length - 2]].z) <=
        hyp(
          NODES[ns[ns.length - 1]].x,
          NODES[ns[ns.length - 1]].z,
          NODES[ns[ns.length - 2]].x,
          NODES[ns[ns.length - 2]].z,
        ) +
          WALK.pathEndSlackMetres
    )
      ns.pop();
    for (const n of ns)
      legs.push({ x: NODES[n].x + off * WALK.laneOffsetScale, z: NODES[n].z + off * WALK.laneOffsetScale });
  }
  legs.push({ x: tx, z: tz });
  if (g.kind === 'room') {
    const r = ROOMS[g.room];
    const [mx, mz] = roomPos(r.id, r.mat[0], r.mat[1]);
    legs.push({ warp: [mx, mz], space: g.room }, { x: g.x, z: g.z });
  }
  P.route = { legs, g, act };
  tripStarts(P, g, legs, cameFrom);
  P.moving = true;
  P.atWindow = false;
  P.gone = false;
  P.awake = true;
}

export function stepPerson(P, dt, near) {
  if (P.dead || P.down || P.busy) return;
  if (P.chat) {
    P.chat.t -= dt;
    if (P.chat.t <= 0) P.chat = null;
  }
  if (P.alert) {
    P.alert.t -= dt;
    if (P.alert.t <= 0) P.alert = null;
  }
  if (P.pauseT > 0) {
    P.pauseT -= dt;
    if (P.moving && !P.fight) return;
  } // a pause in the walk while they look
  if (P.keeper) {
    const open = hour() >= WALK.shopsOpenFromHour && hour() < WALK.shopsShutAtHour;
    if (open === P.gone) placeNow(P);
    return;
  }
  if (P.walker) return stepWalker(P, dt, near);
  if (P.lad) return ladRoutine(P, false, dt, near);
  const sl = slot(P),
    key = sl.where + '|' + sl.act;
  if (key !== P.goalKey && !P.hold) {
    P.goalKey = key;
    const g = resolve(P, sl.where);
    const here = !P.route && ((g.kind === 'home' && P.space === 'home') || (g.kind === 'off' && P.gone));
    if (here) applyArrive(P, g, sl.act);
    else planTo(P, g, sl.act);
  }
  if (P.space === 'home') {
    // light sleepers come to the window when the street wakes them
    if (P.wake) {
      P.wake = 0;
      if (!P.awake || !P.atWindow) {
        P.awake = true;
        P.atWindow = !!P.win;
        P.winLit = true;
        P.winT = G.t + WALK.windowLightStaysGameMinutes;
      }
    }
    if (P.alert && P.awake && P.win && !P.atWindow) {
      P.atWindow = true;
      P.winT = G.t + WALK.atWindowStaysGameMinutes;
    }
    if (P.winT && G.t > P.winT) {
      P.winT = 0;
      const s2 = slot(P);
      P.awake = s2.act !== 'sleep';
      P.atWindow = s2.act === 'window';
      P.winLit = false;
    }
    return;
  }
  walkRoute(P, dt, near);
  if (!P.moving && P.space !== 'off') {
    if (P.chat && G.people[P.chat.with]) {
      const o = G.people[P.chat.with];
      turn(P, Math.atan2(o.x - P.x, o.z - P.z), dt, WALK.turnsToTalkerRadiansPerSecond);
    } else if (P.alert)
      turn(P, Math.atan2(P.alert.x - P.x, P.alert.z - P.z), dt, WALK.turnsToAlertRadiansPerSecond);
    else if (P.route === null && P.homeAng !== undefined)
      turn(P, P.homeAng, dt, WALK.turnsHomeRadiansPerSecond);
  }
}
function turn(P, a, dt, k) {
  P.ang += clamp(angDiff(P.ang, a), -k * dt, k * dt);
}
function walkRoute(P, dt, near) {
  const rt = P.route;
  if (!rt) {
    P.v = 0;
    return;
  }
  let leg = rt.legs[0];
  while (leg && leg.warp) {
    P.x = leg.warp[0];
    P.z = leg.warp[1];
    P.space = leg.space;
    rt.legs.shift();
    leg = rt.legs[0];
  }
  if (!leg) {
    const g = rt.g;
    P.route = null;
    P.x = g.x;
    P.z = g.z;
    P.homeAng = g.ang || 0;
    P.v = 0;
    applyArrive(P, g, rt.act);
    if (g.kind === 'street' || g.kind === 'room') P.ang = g.ang || 0;
    return;
  }
  const pace = P.def.frail
    ? WALK.frailMetresPerSecond
    : P.def.age > WALK.slowerAboveAgeYears
      ? WALK.over60MetresPerSecond
      : WALK.walkingMetresPerSecond;
  const sp = pace * (P.hurry || 1) * (near ? 1 : WALK.paceOutOfHisSightTimes);
  let budget = sp * dt;
  while (leg && !leg.warp && budget > 0) {
    const dx = leg.x - P.x,
      dz = leg.z - P.z,
      d = Math.hypot(dx, dz);
    if (d <= budget + WALK.arrivesWithinMetres) {
      P.x = leg.x;
      P.z = leg.z;
      budget -= d;
      rt.legs.shift();
      leg = rt.legs[0];
      if (near) break;
    } else {
      P.x += (dx / d) * budget;
      P.z += (dz / d) * budget;
      turn(
        P,
        Math.atan2(dx, dz),
        Math.min(dt, WALK.turnStepAtMostRealSeconds),
        WALK.walkingTurnRadiansPerSecond,
      );
      budget = 0;
    }
  }
  P.v = sp;
  P.moving = true;
}

// ---------- the anonymous crowd ----------
function crowdTarget() {
  const h = hour();
  return h < CROWD.smallHoursUntilHour
    ? 1
    : h < CROWD.dawnUntilHour
      ? CROWD.walkersAtDawn
      : h < CROWD.earlyUntilHour
        ? CROWD.walkersEarly
        : h < CROWD.dayUntilHour
          ? CROWD.walkersByDay
          : h < CROWD.eveningUntilHour
            ? CROWD.walkersInTheEvening
            : h < CROWD.lateUntilHour
              ? CROWD.walkersLate
              : 2;
}
function randomNode() {
  for (let i = 0; i < 20; i++) {
    const n = Math.floor(rnd(0, NODES.length));
    const N = NODES[n];
    if (N.z > -205 && Math.abs(N.x) < 125) return n;
  }
  return 0;
}
function respawnWalker(P, anywhere) {
  const idx = +P.id.slice(1);
  if (idx >= crowdTarget()) {
    P.gone = true;
    P.space = 'off';
    P.route = null;
    P.moving = false;
    return;
  }
  const a = anywhere ? randomNode() : nearNode(...pick(Object.values(EXITS))),
    b = randomNode();
  P.x = NODES[a].x;
  P.z = NODES[a].z;
  P.space = 'street';
  P.gone = false;
  P.awake = true;
  P.lane = rnd(-CROWD.walkerLaneOffsetAtMostMetres, CROWD.walkerLaneOffsetAtMostMetres);
  P.route = {
    legs: path(a, b).map((n) => ({
      x: NODES[n].x + P.lane * WALK.laneOffsetScale,
      z: NODES[n].z + P.lane * WALK.laneOffsetScale,
    })),
    g: { kind: 'street', x: NODES[b].x, z: NODES[b].z, ang: rnd(0, 6.28) },
    act: 'idle',
  };
  P.moving = true;
  P.waitT = 0;
  P.mind.mem = [];
  P.mind.by = {};
  P.mind.fam = 0;
}
function stepWalker(P, dt, near) {
  if (P.gone) {
    if (chance(dt * CROWD.walkerComesBackChancePerRealSecond) && +P.id.slice(1) < crowdTarget())
      respawnWalker(P, false);
    return;
  }
  if (P.route) {
    walkRoute(P, dt, near);
    return;
  }
  P.waitT += dt;
  if (P.alert) turn(P, Math.atan2(P.alert.x - P.x, P.alert.z - P.z), dt, WALK.turnsToAlertRadiansPerSecond);
  if (
    P.waitT >
    (P.waitFor || (P.waitFor = rnd(CROWD.walkerWaitsRealSecondsAtLeast, CROWD.walkerWaitsRealSecondsAtMost)))
  ) {
    P.waitFor = 0;
    P.waitT = 0;
    if (+P.id.slice(1) >= crowdTarget() || chance(CROWD.walkerLeavesChance)) {
      const e = pick(Object.values(EXITS));
      const a = nearNode(P.x, P.z),
        b = nearNode(e[0], e[1]);
      P.route = {
        legs: path(a, b).map((n) => ({ x: NODES[n].x, z: NODES[n].z })),
        g: { kind: 'off', x: e[0], z: e[1] },
        act: 'idle',
      };
    } else {
      const a = nearNode(P.x, P.z),
        b = randomNode();
      P.route = {
        legs: path(a, b).map((n) => ({
          x: NODES[n].x + P.lane * WALK.laneOffsetScale,
          z: NODES[n].z + P.lane * WALK.laneOffsetScale,
        })),
        g: { kind: 'street', x: NODES[b].x, z: NODES[b].z, ang: rnd(0, 6.28) },
        act: 'idle',
      };
    }
    P.moving = true;
  }
}
// Cammack's lads stand about outside the video shop in the evening, and drift onto the quay late.
function ladRoutine(P, init, dt, near) {
  const i = +P.id.slice(3),
    h = hour();
  const where =
    h >= CROWD.ladsOutFromHour && h < CROWD.ladsMoveOnAtHour
      ? i < 2
        ? ['lads1', 'lads2'][i]
        : 'video'
      : (h >= CROWD.ladsMoveOnAtHour || h < CROWD.ladsLateUntilHour) && i < 2 && [0, 2, 3].includes(day() % 7)
        ? ['lads3', 'lads4'][i]
        : 'off';
  if (P.fightT) return;
  if (init || where !== P.goalKey) {
    P.goalKey = where;
    const g = resolve(P, where);
    if (init || (g.kind === 'off' && P.gone)) {
      P.x = g.x;
      P.z = g.z;
      P.ang = g.ang || 0;
      P.route = null;
      applyArrive(P, g, 'smoke');
    } else planTo(P, g, 'smoke');
  }
  if (dt) {
    walkRoute(P, dt, near);
    if (!P.moving && P.alert)
      turn(P, Math.atan2(P.alert.x - P.x, P.alert.z - P.z), dt, WALK.turnsToAlertRadiansPerSecond);
  }
}
export function stepPeople(dt) {
  const t = G.tom,
    cx = t.inCar ? G.car.x : t.x,
    cz = t.inCar ? G.car.z : t.z;
  for (const P of G.named)
    stepPerson(P, dt, P.space === t.space && hyp(P.x, P.z, cx, cz) < WALK.fullyStepsWithinMetres);
  for (const P of G.crowd)
    stepPerson(P, dt, P.space === t.space && hyp(P.x, P.z, cx, cz) < WALK.fullyStepsWithinMetres);
}
// Walk someone to an arbitrary point on the street (police, Ellis). They hold there until released.
export function goToPoint(P, x, z, speed = WALK.walkingMetresPerSecond) {
  P.hold = true;
  P.hurry = speed / WALK.walkingMetresPerSecond;
  planTo(P, { kind: 'street', x, z, ang: P.ang }, 'idle');
}
// Send someone somewhere for the story; they walk there and stay until released.
export function send(P, where, act = 'idle', untilT) {
  P.override = { where, act, until: untilT };
  P.hold = false;
  P.hurry = 1;
}
export function release(P) {
  P.override = null;
}
export function isNear(P, d = WALK.besideTomWithinMetres) {
  const t = G.tom;
  return P.space === t.space && !P.gone && hyp(P.x, P.z, t.x, t.z) < d;
}
export const gameMinPerSec = () => 60 / SECS_PER_HOUR;
