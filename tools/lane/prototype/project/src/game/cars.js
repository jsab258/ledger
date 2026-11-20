// LEDGER, the whole game: the system "cars". The car in the town (DESIGN 5; A24, A27, A32; parts 1.2.4, 1.2.5,
// 1.2.8 to 1.2.11, 1.5.3, 4.1.4): a hit hurts and never kills and the choice is put at once; from about 35 mph in
// one hit the car will not drive on; the horn; looking back; being driven; repairs and paint; taking a parked car;
// reckless driving in the patrol car's sight; the soft edge. The rules are pieces/law.js and pieces/life.js.
import { register, X, write, tell, hourNow, dayNow, P_, emit, on, PLACES, tomXZ } from './core.js';
import { G } from '../state.js';
import { hyp } from '../util.js';
import { act } from '../events.js';
import { pay } from '../money.js';
import { advanceTo } from '../work.js';
import { choose, scene, say } from '../ui.js';
import { blocked } from '../map.js';
import { RULES } from '../rules.js';
import { PIECE as LAW } from './pieces/law.js';
import { PIECE as LIFE } from './pieces/life.js';
import { PIECE as EYES } from './pieces/eyes.js';
import { setFareShare } from './econ.js';

const T = RULES.game.cars;
const S = { pave: 0, tick: 0, hornT: -99 };
const raining = () => G.weather.rain > RULES.weather.rainingAboveRain;
const firmCar = () => !X('cars').taken && !X('cars').resprayed;

// ---- cars and people (1.2.5): the choice, put within 2 s; neither answer ends the game ----
async function hit({ P, speed }) {
  const x = X('cars');
  const h = LAW.fns.carHit(speed, false);
  if (!h.choiceWithinSeconds) return; // a clip at walking pace: a mouthful, and forgiven
  P.hurtKind = h.hurt;
  const name = P.anon ? P.def.desc : P.def.name;
  const i = await scene(() => choose('', `${name[0].toUpperCase() + name.slice(1)} is down in the road, and not getting up. The engine is still running.`, ['Stop and help.', 'Drive off.']));
  const r = LAW.fns.afterHit(i === 0 ? 'stop and help' : 'drive off');
  x.hits.push({ who: P.id, hurt: h.hurt, choice: i === 0 ? 'stopped' : 'drove off', speed: Math.round(speed * 10) / 10, t: Math.round(G.t) });
  if (i === 0) {
    G.car.v = 0;
    act('hit_stopped', { target: P.anon ? undefined : P.id, name: P.def.name });
    // help is a call from the nearest phone box or a neighbour who rings; the ambulance comes in ten game minutes (A22)
    const amb = LAW.fns.ambulance(G.t);
    x.ambulance = { who: P.id, arrivesT: amb.arrivesT, calledT: G.t };
    advanceTo(G.t + T.helpTakesGameMinutes, false);
    write(`Knocked ${name} down with the cab, and stopped. The ambulance took ${P.def.sex === 'f' ? 'her' : 'him'}: ${h.hurt}. Everybody who stopped to look saw his face beside the cab.`, { who: P.anon ? undefined : P.id, how: 'Did it' });
    hospital(P, h);
  } else {
    act('hit_and_run', { target: P.anon ? undefined : P.id, name: P.def.name, noiseR: RULES.game.foot.reachMetres.cab });
    // the firm's name pays: people ring the other firm for a while (ER-DRIVE-10)
    if (firmCar()) setFareShare(r.firmFaresShare, G.t + r.forGameDays * 1440);
    x.hitAndRun = { t: G.t, untilT: G.t + r.forGameDays * 1440 };
    write(`Drove off from ${name} lying in the road. It is a hit-and-run now: the car will be described, and the firm's name with it.`, { how: 'Did it' });
    emit('cars.reckless', { why: 'hit', x: G.car.x, z: G.car.z });
    hospital(P, h);
  }
}
function hospital(P, h) {
  if (!h.hospitalDays) return;
  X('cars').inHospital[P.id] = { untilT: G.t + h.hospitalDays * 1440 };
  P.override = { where: 'off', act: 'idle', until: G.t + h.hospitalDays * 1440 };
  P.down = false;
  P.gone = true;
}
// ---- crashes (1.2.4): damage in stages by closing speed; from about 35 mph it will not drive on ----
function crash({ speed }) {
  const x = X('cars'),
    r = LIFE.fns.crash(speed * T.mphPerMetrePerSecond);
  x.crashes.push({ mph: Math.round(speed * T.mphPerMetrePerSecond), stage: r.stage, t: Math.round(G.t) });
  if (!r.drives && !x.wrecked) {
    x.wrecked = { t: G.t, backT: (dayNow() + 1) * 1440 + T.carFetchedBackAtHour * 60 };
    tell('The front is in. It will not drive on. He can get out [F]; the firm will fetch it, and it is off the road till tomorrow.', '', 8);
    write('Put the cab into something hard enough that it would not drive on. The firm fetched it; a day off the road.', { how: 'Did it' });
  }
}
// ---- the horn (A32) ----
function horn() {
  const t = G.tom,
    x = X('cars'),
    [cx, cz] = tomXZ();
  const listeners = G.named.concat(G.crowd).filter((P) => !P.gone && !P.dead && P.space === 'street').map((P) => ({ id: P.id, metres: hyp(P.x, P.z, cx, cz) }));
  const f = G.story.fare;
  const r = EYES.fns.horn({ hour: hourNow(), rain: raining(), listeners, fareMetres: f && f.st === 'pickup' ? hyp(f.sx, f.sz, cx, cz) : null });
  for (const id of r.heardBy) {
    const P = G.people[id];
    if (P && P.awake) {
      P.alert = { x: cx, z: cz, t: RULES.game.foot.noiseHoldsAWatcherRealSeconds };
      if (hyp(P.x, P.z, cx, cz) < 8 && P.moving) P.pauseT = 1; // people in the road step aside
    }
  }
  const night = hourNow() >= RULES.game.foot.nightFromHour || hourNow() < RULES.game.foot.nightUntilHour;
  if (night) act('horn_night', { silent: true, told: r.heardBy.filter((id) => G.people[id] && !G.people[id].anon && G.people[id].awake).slice(0, 6) });
  x.horns.push({ heard: r.heardBy.length, fare: r.fareComesOutWithinSeconds, night, t: Math.round(G.t) });
  if (r.fareComesOutWithinSeconds && f) {
    f.hornT = G.played;
    tell('A door opens down the street. The fare is coming out.', '');
  }
  if (G.hooks.sfx) G.hooks.sfx('radio');
  S.hornT = G.played;
  return r;
}
// ---- riding as a passenger (A24): he says where, by landmark; skipping passes exactly the drive's time ----
async function rideWith(D) {
  const names = T.ridePlaces.map((id) => PLACES[id].name);
  const i = await scene(() => choose(D.id, 'Where to, boss?', names.concat(['Never mind.'])));
  if (i >= T.ridePlaces.length) return;
  const p = PLACES[T.ridePlaces[i]],
    [x0, z0] = tomXZ();
  const r = LIFE.fns.ride(hyp(x0, z0, p.x, p.z) * 1.3, T.rideMetresPerSecond, RULES.time.realSecondsPerGameHour);
  const t0 = G.t;
  advanceTo(G.t + r.gameMinutes, true);
  const t = G.tom;
  t.space = 'street';
  t.inCar = false;
  let px = p.x,
    pz = p.z + 2.5;
  for (let k = 0; k < 12 && blocked(px, pz); k++) pz += 0.7;
  t.x = px;
  t.z = pz;
  if (G.hooks.snapCam) G.hooks.snapCam();
  act('rode', { target: D.id, dest: 'to ' + p.name, silent: true, told: [D.id] });
  X('cars').rides.push({ by: D.id, to: p.id, gameMinutes: Math.round((G.t - t0) * 100) / 100, wanted: r.gameMinutes });
  tell(`${D.def.name} drops him at ${p.name} and pulls away.`, '');
}
// ---- repairs, plates and paint (A24): Shaun Hewson's paint makes a car not look like a cab ----
async function respray() {
  const x = X('cars');
  if (x.resprayed) return tell('"It has had its coat. Any more and it will not close its doors."', 'shaun');
  const cost = RULES.game.econ.prices.respray;
  const i = await scene(() => choose('shaun', `"Sign off, new colour, nobody the wiser. ${cost / 100} pounds, and I never saw it."`, ['Do it.', 'Not today.']));
  if (i !== 0) return;
  if (!pay(cost, false, 'a respray at Shaun Hewson\'s lock-up')) return tell('"Come back with the money."', 'shaun');
  x.resprayed = { t: G.t, paint: 'dark blue' };
  act('resprayed', { silent: true, told: ['shaun'] });
  write("Shaun Hewson resprayed car two dark blue and took the roof sign off. Nobody who saw the white cab will know this car.", { who: 'shaun', how: 'Did it' });
}
// A sighting of a deed done from the car names the car, unless the paint has changed since (ER-PAINT-01).
export const carNamed = (sightingT) => LIFE.fns.named({ sawCar: true, paint: X('cars').resprayed && sightingT < X('cars').resprayed.t ? 'white' : X('cars').resprayed ? 'dark blue' : 'white', plate: 'E412' }, { paint: X('cars').resprayed ? 'dark blue' : 'white', plate: 'E412', roofSign: !X('cars').resprayed });
// ---- taking a parked car (A27): only parked cars, never one with somebody in it; loud; about 6 s ----
function takeHotspot(out) {
  const t = G.tom,
    x = X('cars');
  if (t.inCar || t.space !== 'street' || x.taken) return;
  for (const c of RULES.game.crime.parked) {
    if (x.takenBefore[c.id] || hyp(t.x, t.z, c.at[0], c.at[1]) > T.takeCarWithinMetres) continue;
    const r = EYES.fns.takeCar({ parked: true, someoneInIt: false, plate: c.name });
    out.push({ k: 'G', t: 'Break into ' + c.name + ' (loud)', run: () => {
      const Ev = act('car_taken', { thing: c.name, noiseR: EYES.fns.reach(r.noise, hourNow(), raining()) });
      x.taken = { id: c.id, name: c.name, owner: c.owner, t: G.t, e: Ev.id, home: [G.car.x, G.car.z, G.car.ang] };
      x.takenBefore[c.id] = Math.round(G.t);
      Object.assign(G.car, { x: c.at[0], z: c.at[1], v: 0, keys: true });
      t.inCar = true;
      write(`Took ${c.name}. No roof sign: it is not the firm's car, which is the point. Its owner will report it when he finds it gone.`, { how: 'Did it', ev: Ev.id });
      emit('crime.damage', { e: Ev.id, owner: c.owner, thing: c.name, place: c.id });
    } });
    return;
  }
}
function leaveTaken() {
  const x = X('cars');
  if (!x.taken || G.tom.inCar) return;
  // left where he got out; the firm's own car is where he left it
  x.left.push({ id: x.taken.id, x: Math.round(G.car.x), z: Math.round(G.car.z), t: Math.round(G.t) });
  Object.assign(G.car, { x: x.taken.home[0], z: x.taken.home[1], ang: x.taken.home[2], v: 0 });
  x.taken = null;
}

register({
  id: 'cars',
  fresh: () => ({ hits: [], crashes: [], horns: [], rides: [], wrecked: null, resprayed: null, taken: null, takenBefore: {}, left: [], inHospital: {}, ambulance: null, hitAndRun: null, edge: [] }),
  step(dt) {
    if (G.paused) return;
    const t = G.tom,
      c = G.car,
      x = X('cars');
    if (x.wrecked) {
      if (G.t >= x.wrecked.backT) {
        x.wrecked = null;
        c.dmg = 0;
        Object.assign(c, { x: 4.1, z: 37.4, ang: 0, v: 0 }); // fetched, mended, back on the rank
      } else if (t.inCar) c.v = 0;
    }
    leaveTaken();
    if (!t.inCar) return void (S.pave = 0);
    // the soft edge (4.1.4): a car at the map's edge has gone by the west or north road and comes back as time passed
    S.tick += dt;
    if (S.tick < T.recklessCheckedEveryRealSeconds) return;
    S.tick = 0;
    const zone = G.env.zone(c.x, c.z);
    const onPave = /pavement/i.test(zone) || (Math.abs(c.x) > 4.6 && Math.abs(c.x) < 7 && c.z < 40 && c.z > -90 && Math.abs(c.v) > 3);
    S.pave = onPave ? S.pave + T.recklessCheckedEveryRealSeconds : 0;
    if (S.pave >= T.pavementCountsAfterRealSeconds) {
      S.pave = 0;
      emit('cars.reckless', { why: 'pavement', x: c.x, z: c.z });
    } else if (Math.abs(c.v) > RULES.game.law.speedLimitMetresPerSecond * RULES.game.law.recklessFarOverSpeedShare) emit('cars.reckless', { why: 'speed', x: c.x, z: c.z });
  },
  hourly(h) {
    const c = G.car;
    if (h === T.dentMendedOvernightAtHour && c.dmg > 0 && !G.tom.inCar && !X('cars').wrecked) c.dmg = 0; // a dent stays until the firm mends it at the yard overnight
    const x = X('cars');
    for (const id in x.inHospital)
      if (G.t >= x.inHospital[id].untilT) {
        delete x.inHospital[id];
        const P = G.people[id];
        if (P) {
          P.gone = false;
          P.override = null;
        }
      }
  },
  key(code) {
    if (code !== 'KeyH' || !G.tom.inCar) return false;
    horn();
    return true;
  },
  carPrompts(out) {
    if (X('cars').wrecked) out.push({ k: 'F', t: 'Get out: it will not drive on' });
  },
  hotspots(out) {
    const t = G.tom;
    takeHotspot(out);
    if (t.space !== 'street') return;
    for (const id of ['kevin', 'terry']) {
      const D = P_(id);
      if (D && !D.gone && D.space === 'street' && hyp(D.x, D.z, t.x, t.z) < RULES.tom.talksWithinMetres && hyp(D.x, D.z, 6.2, 38.5) < 8) {
        out.push({ k: 'T', t: 'Have ' + D.def.name.split(' ')[0] + ' drive him', run: () => rideWith(D) });
        break;
      }
    }
    const sh = P_('shaun');
    if (sh && !sh.gone && sh.space === 'street' && hyp(sh.x, sh.z, t.x, t.z) < RULES.tom.talksWithinMetres && (G.x.rise ? G.x.rise.rung : 1) >= 2) out.push({ k: 'T', t: 'Ask Shaun about paint', run: respray });
  },
  hook: {
    x: () => X('cars'),
    hit: (id, speed) => hit({ P: G.people[id], speed }),
    crash: (speed) => crash({ speed }),
    horn,
    rideWith: (id) => rideWith(G.people[id]),
    respray,
    carNamed,
    carHit: (speed, aimed) => LAW.fns.carHit(speed, aimed),
  },
});
on('cars.hit', hit);
on('cars.crash', crash);
