// LEDGER, the whole game: the system "foot". Tom on foot beyond walking: hiding (A1), street manners, stopping and
// ground rules (A10), the watch and the bell (A31), drawing a watcher away (A23), the torch in the hand (A33),
// things thrown in the water (A11), chasing a runner (A3), marks that last and the old doctor (A21).
// The rules themselves are the pure pieces hide_rules, foot_chase and foot_ground; this file joins them to the game.
import { register, emit, on, PLACES, addPlace } from './core.js';
import { G, hour, day } from '../state.js';
import { hyp, clamp, angDiff, hhmm, hourWords } from '../util.js';
import { act, mkEvent, remember } from '../events.js';
import { sub, bubble, ui, tomName, scene, choose } from '../ui.js';
import { PROPS, SHADE, ROOMS, inWater, los, zoneAt, blocked } from '../map.js';
import { perceivers, sense, tomTarget, nightF, noiseRadius } from '../seeing.js';
import { target, frontUp, F } from '../fight.js';
import { goToPoint, release } from '../routines.js';
import { pay } from '../money.js';
import { startTalk } from '../talk.js';
import { RULES } from '../rules.js';
import { lightForTom, glanceSeconds, drawsSecondLook } from './pieces/hide_rules.js';
import { chaseStep } from './pieces/foot_chase.js';
import { standing, trespassStep } from './pieces/foot_ground.js';

const T = RULES.game.foot,
  SCREEN = RULES.game.feel.screen;
const inRect = (x, z, r) => x >= r.x0 && x <= r.x1 && z >= r.z0 && z <= r.z1;
const inShade = (x, z) => SHADE.some((r) => inRect(x, z, r));
const st = () => G.x.foot;
// what a save does not hold
const R = { mann: 0, mannP: null, held: [], tres: null, tresT: 0, tresBy: null, stood: 0, looked: false, run: null, watchUntil: 0, log: [] };
const said = (what, x) => {
  R.log.push(Object.assign({ what, t: G.t }, x || {}));
  if (R.log.length > 200) R.log.shift();
};

// ---------- the places this system adds ----------
addPlace({ id: 'doctor', name: "the old doctor's door", x: T.marks.doctorX, z: T.marks.doctorZ, address: '10 Quay Street', landmark: 'the terrace door with the brass plate gone green, across from the bus shelter', label: 'private', owner: 'the old doctor' });
// The ground labels of the street's own zones (A10). Rooms keep their hours at the door (player.js); a zone not
// named here is public. Other systems add places with labels through core's addPlace: those within their reach
// count as well.
const ZONE_GROUND = {
  "Iveson's yard": { label: 'hours', openFromHour: T.ground.yardPrivateUntilHour, openUntilHour: T.ground.yardPrivateFromHour, owner: 'dennis', name: "Iveson's yard" },
  "Mickey's yard": { label: 'public', name: "Mickey's yard" },
};
export function groundAt(x, z, space) {
  if (space !== 'street') {
    const p = PLACES[space];
    return p && p.room ? p : null;
  }
  for (const id in PLACES) {
    const p = PLACES[id];
    if ((p.label === 'forbidden' || p.label === 'private' || p.label === 'hours') && p.groundMetres && hyp(x, z, p.x, p.z) < p.groundMetres) return p;
  }
  return ZONE_GROUND[zoneAt(x, z)] || { label: 'public', name: zoneAt(x, z) };
}

// ---------- hiding: the light Tom counts at ----------
function wrapLight() {
  if (G.env.footWrapped) return;
  const base = G.env.lightAt;
  G.env.footWrapped = true;
  G.env.lightAt = (x, z, space) => {
    let L = base(x, z, space);
    const t = G.tom;
    if (t.inCar || space !== t.space || Math.abs(x - t.x) > 0.01 || Math.abs(z - t.z) > 0.01) return L;
    const doorway = space === 'street' && inShade(x, z),
      still = t.still || 0;
    // moving through a doorway counts at the street's light: the light just outside it
    if (doorway && still < T.hiding.stillAfterRealSeconds)
      for (const [dx, dz] of [[1.6, 0], [-1.6, 0], [0, 1.6], [0, -1.6]]) if (!inShade(x + dx, z + dz)) L = Math.max(L, base(x + dx, z + dz, space));
    return lightForTom({ light: L, doorway, night: nightF() > 0.5 }, { stillSeconds: still, torchOn: !!t.torchOn });
  };
}
const peopleNear = (m) => G.named.concat(G.crowd).filter((P) => !P.gone && !P.down && P.space === G.tom.space && hyp(P.x, P.z, G.tom.x, G.tom.z) < m);

// ---------- street manners (A10) ----------
const MANNERS = [
  ['nod', 'Nod'],
  ['greeting', 'Good day'],
  ['hard_look', 'A hard look'],
  ['street_shove', 'Shove'],
  ['called_out', 'Call "Oi!"'],
];
const ANSWERS = {
  nod: ['A nod back.', 'Nods.', 'Lifts a hand.'],
  greeting: ['Now then.', 'Morning.', 'All right.', 'How do.'],
  hard_look: ['What?', 'You looking at me?', 'Looks away.'],
  street_shove: ['Hey! Watch it!', 'Get your hands off!', 'What was that for?'],
  called_out: ['What?', 'Me?', 'Who wants to know?'],
};
function mannerTarget(call) {
  const t = G.tom;
  let P = target();
  if (P && hyp(P.x, P.z, t.x, t.z) < T.manners.reachesWithinMetres) return P;
  // further off: the one most nearly straight ahead, within the remark's reach (the call carries further)
  const reach = call ? T.manners.callHeardMetres : T.manners.reachesWithinMetres;
  let best = null,
    bo = 0.5;
  for (const Q of G.named.concat(G.crowd)) {
    if (Q.gone || Q.down || Q.space !== t.space) continue;
    const d = hyp(Q.x, Q.z, t.x, t.z);
    if (d > reach) continue;
    const off = Math.abs(angDiff(G.env.camYaw ? G.env.camYaw() : t.ang, Math.atan2(Q.x - t.x, Q.z - t.z)));
    if (off < bo) {
      bo = off;
      best = Q;
    }
  }
  return best;
}
export function manner(kind, P) {
  const t = G.tom;
  P = P || mannerTarget(kind === 'called_out');
  if (!P) {
    sub('Nobody near enough.', '', 'over', 2);
    return null;
  }
  const d = hyp(P.x, P.z, t.x, t.z);
  if (kind === 'street_shove' && d > T.manners.shoveWithinMetres) {
    sub('Too far off to lay a hand on.', '', 'over', 2);
    return null;
  }
  t.ang = Math.atan2(P.x - t.x, P.z - t.z);
  const E = act(kind, { target: P.id, name: tomName(P), noiseR: kind === 'called_out' ? T.manners.callHeardMetres : 0 });
  // answered in body or voice within a second, and remembered like any act (ER-MANNER-01)
  P.ang = Math.atan2(t.x - P.x, t.z - P.z);
  P.mind.look = Math.max(P.mind.look || 0, 2.5);
  const key = P.id + ':' + kind,
    last = st().greet[key];
  const again = last !== undefined && G.t - last < T.manners.greetingAgainAfterGameMinutes;
  st().greet[key] = G.t;
  const opts = ANSWERS[kind],
    line = again && (kind === 'nod' || kind === 'greeting') ? 'Nods again.' : opts[(P.id.length + Math.floor(G.t / 60)) % opts.length];
  bubble(P, line, 2.5);
  if (kind === 'called_out') {
    // stops a walker for about two seconds and turns him round: the way to stop a witness on her walk
    R.held.push({ P, t: T.manners.callStopsWalkerRealSeconds, was: !!P.hold, route: P.route, moving: P.moving });
    P.hold = true;
    P.moving = false;
    P.stoppedByCall = G.t;
  }
  if (kind === 'street_shove') {
    const k = T.manners.shovePushesMetres / Math.max(0.2, d),
      nx = P.x + (P.x - t.x) * k,
      nz = P.z + (P.z - t.z) * k;
    if (!blocked(nx, nz, 0.3)) {
      P.x = nx;
      P.z = nz;
    }
    P.mind.regard = clamp((P.mind.regard || 0) - 0.08, -1, 1);
  }
  said('manner', { kind, to: P.id, e: E.id, line });
  emit('manner', { kind, P, E });
  return { E, line, to: P.id };
}

// ---------- stopping and blending in (A10) ----------
function seatNear() {
  const t = G.tom;
  if (t.space !== 'street') return null;
  for (const p of PROPS) if ((p.t === 'bench' || p.t === 'busshelter' || p.t === 'shelter') && hyp(p.x, p.z, t.x, t.z) < T.stopping.seatWithinMetres + (p.w || 0) / 2) return p;
  return null;
}
const wallNear = () => {
  const t = G.tom,
    w = T.stopping.wallWithinMetres;
  return blocked(t.x + w, t.z, 0.2) || blocked(t.x - w, t.z, 0.2) || blocked(t.x, t.z + w, 0.2) || blocked(t.x, t.z - w, 0.2);
};
export function stop(how) {
  const t = G.tom;
  if (how === undefined) how = t.stop ? null : seatNear() ? 'sit' : wallNear() ? 'lean' : 'smoke';
  if (how === t.stop) return how;
  t.stop = how || null;
  t.sit = how === 'sit';
  t.belongs = !!how; // a man who is sitting, leaning or smoking has a reason to be there (hide_rules, A10)
  if (how) {
    sub(how === 'sit' ? 'He sits down. A man on a bench is nobody.' : how === 'lean' ? 'He leans on the wall. A man waiting.' : 'He lights a cigarette. A man with a smoke has a reason to stand.', '', 'over', 3);
    if (how === 'smoke' && G.hooks.sfx) G.hooks.sfx('paper');
    act('sat_about', { silent: true });
  }
  said('stop', { how: how || 'up' });
  return how;
}

// ---------- the watch, the clocks and the bell (A31) ----------
const clockNear = () => {
  const t = G.tom;
  if (t.space === 'mickeys' || t.space === 'harbour') return true; // the office clock, the Harbour Board's
  if (t.space !== 'street') return false;
  const cs = PROPS.filter((p) => p.t === 'clock').map((p) => [p.x, p.z]);
  if (ROOMS.harbour) cs.push([ROOMS.harbour.street[0], ROOMS.harbour.street[1]]); // the clock over the Harbour Board
  return cs.some(([x, z]) => hyp(x, z, t.x, t.z) < SCREEN.streetClockReadWithinMetres && los(t.x, t.z, x, z + 0.5));
};
export const timeKnown = () => performance.now() < R.watchUntil || clockNear();
export function watch() {
  R.watchUntil = performance.now() + SCREEN.watchShowsRealSeconds * 1000;
  ui.hudT = 0;
  const h = hour(),
    m = Math.floor((h % 1) * 60);
  sub(`His watch: ${hhmm(h)}. ${m < 8 ? 'Just gone ' + hourWords(h) : m > 52 ? 'Coming up to ' + hourWords(h + 1) : cap(hourWords(h)) + ', and a bit'}.`, '', 'over', SCREEN.watchShowsRealSeconds + 0.5);
  said('watch', { h });
  return hhmm(h);
}
const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);

// ---------- drawing a watcher away (A23) ----------
export function makeNoise() {
  const t = G.tom;
  if (t.space !== 'street') return sub('Not in here.', '', 'over', 2), null;
  const bin = PROPS.find((p) => (p.t === 'bin' || p.t === 'dustbin') && hyp(p.x, p.z, t.x, t.z) < T.noises.binWithinMetres + p.r);
  const yaw = G.env.camYaw ? G.env.camYaw() : t.ang;
  let x = t.x,
    z = t.z,
    reach = T.noises.binRattleHeardMetres,
    what = 'bin';
  if (!bin) {
    what = 'stone';
    reach = T.noises.stoneHeardMetres;
    // the stone lands where it stops: at a wall, or its full throw
    for (let s = 1; s <= T.noises.stoneThrownMetres; s += 0.5) {
      const nx = t.x + Math.sin(yaw) * s,
        nz = t.z + Math.cos(yaw) * s;
      if (blocked(nx, nz, 0.1) && !inWater(nx, nz)) break;
      x = nx;
      z = nz;
    }
  }
  reach = noiseRadius(reach); // the hour and the rain set how far it carries, as for any noise
  const E = mkEvent('noise_made', { x: Math.round(x), z: Math.round(z) });
  const turned = [];
  for (const P of perceivers()) {
    if (P.dead || P.gone || P.down || !P.awake || P.space !== 'street') continue;
    if (hyp(P.x, P.z, x, z) > reach) continue;
    // a head turns to the noise, and he remembers there was a noise; nobody is named by it
    P.alert = { x, z, t: T.noises.headTurnsForRealSeconds };
    remember(P, E, { src: 'heard', who: 'man', sure: 0.15, heat: 0.2 });
    turned.push(P.id);
  }
  if (bin) t.noiseP = Math.max(t.noiseP || 0, T.noises.binRattleHeardMetres);
  if (G.hooks.sfx) G.hooks.sfx(bin ? 'bin' : 'step');
  sub(bin ? 'He rattles the bin lid.' : inWater(x, z) ? 'A stone, into the water.' : 'A stone, off down the street.', '', 'over', 2.2);
  emit('noise', { x, z, reach, what, by: 'tom' });
  said('noise', { what, x, z, reach, turned });
  return { what, x, z, reach, turned };
}

// ---------- the torch in the hand (A33; the jobs builder reads G.tom.torchOn) ----------
export function torch(on) {
  const t = G.tom,
    has = !!(t.torch || (t.items && t.items.torch));
  if (!has) {
    sub('No torch. The ironmonger sells them.', '', 'over', 2.5);
    return false;
  }
  t.torchOn = on === undefined ? !t.torchOn : !!on;
  sub(t.torchOn ? 'Torch on. He can see, and he can be seen.' : 'Torch off.', '', 'over', 2);
  if (G.hooks.sfx) G.hooks.sfx('tick');
  said('torch', { on: t.torchOn });
  return t.torchOn;
}

// ---------- the water's edge (A11): what goes in is gone ----------
const waterNear = () => {
  const t = G.tom,
    w = T.water.edgeWithinMetres;
  if (t.space !== 'street') return false;
  for (let a = 0; a < 8; a++) if (inWater(t.x + Math.sin((a * Math.PI) / 4) * w, t.z + Math.cos((a * Math.PI) / 4) * w)) return true;
  return false;
};
export function throwIn() {
  const t = G.tom,
    thing = t.weapon || (t.carry && t.carry !== 'suitcase' ? t.carry : null);
  if (!thing || !waterNear()) return null;
  if (t.weapon) {
    t.weapon = null;
    t.armed = false;
  } else t.carry = null;
  st().thrown.push({ thing, t: Math.round(G.t) });
  const E = act('threw_in', { thing: 'a ' + thing, noiseR: 6 });
  sub(`The ${thing} goes in. Gone.`, '', 'over', 3);
  emit('thrown', { thing, E });
  said('threw', { thing });
  return thing;
}

// ---------- chasing a runner (A3) ----------
// Anybody may be set running: G.hooks.runner(P, why). He takes a way he knows, at a running man's pace.
export function runner(P, why = 'ran') {
  if (!P || P.gone || P.down || R.run) return false;
  const t = G.tom,
    away = Math.atan2(P.x - t.x, P.z - t.z),
    home = P.homeAt || P.def.home;
  // toward home if it lies away from Tom, else straight away from him
  let gx = P.x + Math.sin(away) * 80,
    gz = P.z + Math.cos(away) * 80;
  if (home && Math.abs(angDiff(away, Math.atan2(home[0] - P.x, home[1] - P.z))) < 1.6) [gx, gz] = home;
  goToPoint(P, gx, gz, T.chase.tomRunsMetresPerSecond * T.chase.runnerSpeedShareOfTomsRun);
  P.fleeing = true;
  R.run = { P, why, s: { t: 0, gap: hyp(P.x, P.z, t.x, t.z), unseen: 0, end: null }, lastGap: null };
  said('runner', { who: P.id, why });
  return true;
}
function endRun(how) {
  const r = R.run,
    P = r.P;
  R.run = null;
  P.fleeing = false;
  if (how === 'lost') {
    P.hold = false;
    release(P);
    sub(`${tomName(P)} is gone. He will be at home, or with a friend.`, '', 'over', 4);
    said('chase', { end: 'lost', who: P.id, secs: r.s.t });
    emit('chase:end', { how: 'lost', P, seconds: r.s.t });
    return;
  }
  // a hand on the collar, then the choice
  P.moving = false;
  P.route = null;
  P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z);
  const E = act('collared', { target: P.id, name: tomName(P) });
  said('chase', { end: 'caught', who: P.id, secs: r.s.t, e: E.id });
  emit('chase:end', { how: 'caught', P, seconds: r.s.t });
  scene(async () => {
    const i = await choose('', `A hand on ${tomName(P)}'s collar. He stops.`, ['Let him go.', 'A word with him.', 'Front him up.']);
    P.hold = false;
    if (i === 0) release(P);
    else if (i === 1) startTalk(P);
    else frontUp(P);
  });
}
function stepRun(dt) {
  const r = R.run;
  if (!r) return;
  const t = G.tom,
    P = r.P;
  if (P.gone || P.down || G.paused) return;
  const gap = hyp(P.x, P.z, t.x, t.z),
    seen = P.space === t.space && gap < 45 && los(t.x, t.z, P.x, P.z),
    behind = Math.abs(angDiff(P.ang, Math.atan2(t.x - P.x, t.z - P.z))) > Math.PI - T.chase.collarBehindHalfAngleRadians;
  // the piece keeps the clock and the rule; the gap is the street's own
  const s = chaseStep({ t: r.s.t, gap, unseen: r.s.unseen }, { dt, runnerSpeed: 0, pursuerSpeed: 0, seen, behind });
  r.s = s;
  if (!P.moving && !s.end && r.s.t > 1.5) s.end = gap <= T.chase.collarWithinMetres * 2 ? 'caught' : null; // he has run out of road
  if (s.end) endRun(s.end);
}

// ---------- marks that last (A21) ----------
export function mark(hurt = 1) {
  const m = st().marks,
    d = 1440;
  if (hurt < T.marks.markedFromHurt) return m;
  m.bruise = Math.max(m.bruise, G.t + T.marks.bruisesLastGameDays * d);
  m.cut = Math.max(m.cut, G.t + T.marks.cutLipLastsGameDays * d);
  m.limp = Math.max(m.limp, G.t + T.marks.limpLastsGameDays * d);
  syncMarks();
  said('marked', { until: m.bruise });
  return m;
}
function syncMarks() {
  const m = st().marks,
    t = G.tom;
  t.marked = G.t < m.bruise || G.t < m.cut; // a give-away while it lasts (seeing reads G.tom.marked)
  t.limp = G.t < m.limp;
}
function remarks() {
  const t = G.tom,
    s = st();
  if (!t.marked || s.remarkDay === day() || t.inCar) return;
  for (const P of G.named) {
    if (P.gone || P.down || P.space !== t.space || hyp(P.x, P.z, t.x, t.z) > T.marks.remarkWithinMetres) continue;
    if (!sense(P, tomTarget()).see) continue;
    s.remarkDay = day();
    bubble(P, ['That eye. Who gave you that?', 'You have been in the wars.', 'Walked into a door, did you?'][day() % 3], 3.5);
    const E = mkEvent('marked_face', {});
    remember(P, E, { src: 'saw', who: 'tom', sure: 1, heat: 0.4, face: 1 });
    E.wit.push(P.id);
    said('remark', { by: P.id });
    return;
  }
}
const atDoctor = () => G.tom.space === 'street' && hyp(G.tom.x, G.tom.z, T.marks.doctorX, T.marks.doctorZ) < T.marks.doctorWithinMetres;
export function doctor() {
  const s = st(),
    m = s.marks;
  if (!G.tom.marked && !G.tom.limp && G.tom.hurt < 0.2) return sub('He looks him over from the step. "Nothing I can stitch. Go home."', 'The old doctor', 'face', 4), false;
  if (!pay(T.marks.doctorPence, false, 'the old doctor, stitches')) return sub('"Six pounds. I do not ask and I do not give credit."', 'The old doctor', 'face', 4), false;
  for (const k of ['bruise', 'cut', 'limp']) if (m[k] > G.t) m[k] = G.t + (m[k] - G.t) * T.marks.doctorHalvesTimeLeft;
  G.tom.hurt = Math.max(0, G.tom.hurt - 0.4);
  s.doctor++;
  s.doctorKnows.push(Math.round(G.t)); // he remembers who came and when
  act('doctor_visit', { silent: true });
  sub('"Sit. Hold still." Six pounds, no questions. He will remember the face he stitched.', 'The old doctor', 'face', 5);
  syncMarks();
  said('doctor', {});
  return true;
}

// ---------- ground rules (A10) ----------
function stepGround(dt) {
  const t = G.tom;
  R.tresT += dt;
  if (R.tresT < 0.25) return;
  const d = R.tresT;
  R.tresT = 0;
  if (t.inCar || G.paused) return;
  const place = groundAt(t.x, t.z, t.space),
    ground = standing(place, hour());
  let by = null;
  if (ground !== 'free') {
    const T0 = tomTarget();
    for (const P of perceivers()) {
      if (P.down || P.gone || hyp(P.x, P.z, t.x, t.z) > T.ground.warnerWithinMetres) continue;
      const s = sense(P, T0);
      if (s.see || s.hear) {
        by = P;
        if (place.owner === P.id) break;
      }
    }
  }
  const r = trespassStep(R.tres, { ground, watched: !!by, dt: d });
  R.tres = r.s;
  if (!r.say) return;
  const who = by || R.tresBy;
  R.tresBy = who;
  const name = who ? tomName(who) : 'A voice';
  if (r.say === 'warn') sub(`Oi. That is private, ${place.name || 'that'}. Out of it.`, name, 'face', 4);
  else if (r.say === 'warnAgain') sub(ground === 'forbidden' ? 'You. Nobody goes in there. Out, now.' : 'I will not tell you again.', name, 'face', 4);
  else {
    const E = act('trespass', { place: place.name || 'private ground' });
    sub(`${name} has gone for the constable.`, '', 'over', 4);
    emit('trespass', { place, by: who, E });
  }
  said('ground', { say: r.say, place: place.name, by: who ? who.id : null, ground });
}

// ---------- the system ----------
register({
  id: 'foot',
  fresh: () => ({ marks: { bruise: 0, cut: 0, limp: 0 }, doctor: 0, doctorKnows: [], greet: {}, thrown: [], remarkDay: -1 }),
  loaded(x) {
    if (!x.marks) x.marks = { bruise: 0, cut: 0, limp: 0 };
    for (const k of ['greet']) if (!x[k]) x[k] = {};
    for (const k of ['thrown', 'doctorKnows']) if (!x[k]) x[k] = [];
    wrapLight();
    ui.hooks.timeKnown = timeKnown;
    G.hooks.footStop = stop;
    G.hooks.runner = runner;
    G.hooks.markTom = mark;
    G.hooks.vaulted = (v) => {
      said('vault', { x: v.xm, z: v.zm });
      emit('vault', v);
    };
    R.run = null;
    R.tres = null;
    R.mann = 0;
    R.held.length = 0;
    const t = G.tom;
    t.stop = null;
    t.torchOn = !!t.torchOn;
    syncMarks();
  },
  step(dt) {
    const t = G.tom;
    if (R.mann > 0) R.mann -= dt;
    for (let i = R.held.length - 1; i >= 0; i--) {
      const h = R.held[i];
      h.t -= dt;
      if (h.t <= 0) {
        if (!h.was) h.P.hold = false;
        R.held.splice(i, 1);
      } else h.P.moving = false;
    }
    // among people a glance at him takes twice as long (seeing reads G.tom.glanceSecs)
    t.amongPeople = peopleNear(T.hiding.amongPeopleWithinMetres).length;
    t.glanceSecs = glanceSeconds(t.amongPeople);
    // a man standing about at night with no reason draws a second look
    if (!t.inCar && t.space === 'street' && (t.still || 0) > 0.5) {
      R.stood += dt;
      if (!R.looked && drawsSecondLook(nightF() > 0.5, t.stop, R.stood, T.stopping.loiterLookAfterRealSeconds)) {
        R.looked = true;
        const T0 = tomTarget();
        for (const P of perceivers())
          if (sense(P, T0).see) {
            P.mind.look = Math.max(P.mind.look || 0, 4);
            said('second look', { by: P.id });
            break;
          }
      }
    } else {
      R.stood = 0;
      R.looked = false;
    }
    stepGround(dt);
    stepRun(dt);
  },
  minute() {
    syncMarks();
    remarks();
  },
  hourly(h) {
    // the chapel bell strikes the hours by day (A31)
    const t = G.tom,
      x = t.inCar ? G.car.x : t.x,
      z = t.inCar ? G.car.z : t.z;
    if (h >= T.time.chapelBellFromHour && h <= T.time.chapelBellUntilHour && t.space === 'street' && hyp(x, z, T.time.chapelX, T.time.chapelZ) < T.time.chapelBellHeardMetres && !G.paused) {
      if (G.hooks.sfx) G.hooks.sfx('bell');
      sub(`The chapel bell: ${hourWords(h)}.`, '', 'over', 3);
      said('bell', { h });
    }
  },
  hotspots(out) {
    const t = G.tom;
    if (F.on) return;
    if (R.mann > 0) MANNERS.forEach(([k, w], i) => out.push({ k: String(i + 1), t: w, run: () => (R.mann = 0, manner(k, R.mannP)) }));
    const seat = !t.stop && seatNear();
    if (seat) out.push({ k: 'B', t: 'Sit down', run: () => stop('sit') });
    else if (t.stop) out.push({ k: 'B', t: 'Get up and go', run: () => stop(null) });
    const thing = t.weapon || (t.carry && t.carry !== 'suitcase' ? t.carry : null);
    if (thing && waterNear() && !out.some((o) => o.k === 'T')) out.push({ k: 'T', t: `Throw the ${thing} in the water`, run: throwIn });
    if (atDoctor() && !out.some((o) => o.k === 'E')) out.push({ k: 'E', t: "Knock at the old doctor's door", run: doctor });
  },
  key(code) {
    const t = G.tom;
    if (code === 'KeyN') return watch(), true;
    if (t.inCar || F.on) return false;
    if (R.mann > 0 && /^Digit[1-5]$/.test(code)) {
      R.mann = 0;
      manner(MANNERS[+code.slice(5) - 1][0], R.mannP);
      return true;
    }
    if (code === 'KeyM') {
      R.mannP = mannerTarget(true);
      if (!R.mannP) return sub('Nobody near enough.', '', 'over', 2), true;
      R.mann = R.mann > 0 ? 0 : T.manners.menuStaysRealSeconds;
      return true;
    }
    if (code === 'KeyB') return stop(), true;
    if (code === 'KeyO') return makeNoise(), true;
    if (code === 'KeyI') return torch(), true;
    return false;
  },
  hook: {
    log: () => R.log.slice(),
    manner: (kind, id) => manner(kind, id ? G.people[id] : undefined),
    manners: () => MANNERS.map((m) => m[0]),
    stop,
    watch,
    timeKnown,
    makeNoise,
    torch,
    throwIn,
    runner: (id, why) => runner(G.people[id], why),
    chase: () => (R.run ? { who: R.run.P.id, t: R.run.s.t, unseen: R.run.s.unseen } : null),
    mark,
    doctor,
    groundAt: (x, z, space = 'street') => {
      const p = groundAt(x, z, space);
      return { name: p.name, label: p.label, standing: standing(p, hour()) };
    },
    trespass: () => R.tres,
    lightForTomNow: () => G.env.lightAt(G.tom.x, G.tom.z, G.tom.space),
    inShade,
    state: () => ({ stop: G.tom.stop, slow: !!G.tom.slow, torchOn: !!G.tom.torchOn, marked: !!G.tom.marked, limp: !!G.tom.limp, among: G.tom.amongPeople, glance: G.tom.glanceSecs, menu: R.mann > 0 }),
  },
});
// a beating marks him: the fight's end tells this system (fightx emits it)
on('fight:end', (e) => {
  if (e && (e.how === 'beaten' || (G.tom.hurt || 0) >= T.marks.markedFromHurt)) mark(Math.max(G.tom.hurt || 0, e.how === 'beaten' ? 1 : 0));
});
