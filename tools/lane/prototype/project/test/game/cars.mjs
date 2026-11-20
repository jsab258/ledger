// The one-shot (20 Nov 2026): the car in the town. A hit hurts and never kills, and the choice is put at once, stop
// and help or drive off (ER-DRIVE-03, 05, 10); the ambulance comes at its minute (ER-AMB-01); a cab that will not
// drive on says so and can be left (ER-DRIVE-01); the horn (A32); the patrol car stops only what it saw and never
// ordinary driving (ER-TRAFFIC-01, 02); a chase always ends and is lost by breaking sight (ER-POL-04); a tail is
// never lost on a hidden distance and the doubt comes first (ER-TAIL-01 to 03); a skipped ride passes its drive time
// (ER-RIDE-01); after a respray the old sightings do not name the car (ER-PAINT-01); a taken car is reported once its
// owner finds it gone (ER-TAKE-01).
import { launch } from '../harness.mjs';

let bad = 0;
const ok = (cond, what) => {
  console.log((cond ? 'ok   ' : 'FAIL ') + what);
  if (!cond) bad++;
};
const h = await launch({ port: 8831, quality: 'low', seed: 1990 });
const L = (fn, ...a) => h.ev(fn, ...a);
await h.newWeek();
await L(() => {
  const G = LEDGER.G;
  G.story.flags.tour = 1;
  G.car.keys = true;
  G.t = 1440 + 11 * 60; // Tuesday, eleven in the morning
  window.__mark = () => new Set(LEDGER.ui.subs);
  window.__since = (m) => LEDGER.ui.subs.filter((s) => !m.has(s)).map((s) => (s.el.textContent || '').trim());
  window.__pull = (x, z, ang) => { G.car.x = x; G.car.z = z; G.car.v = 0; if (ang !== undefined) G.car.ang = ang; };
  // a patrol car that is somewhere else entirely, unless a check wants it
  window.__patrolAway = () => LEDGER.game.cars.patrolAt(150, 46.2);
});
ok(await L(() => LEDGER.cab.getIn()), 'Tom is at the wheel');

// ---- what one hit does to the car: 10, 20, 35 and 50 mph (ER-DRIVE-01, 08) ----
let r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars, out = {};
  for (const mph of [5, 10, 20]) { G.car.dmg = 0; out[mph] = Object.assign({}, C.crash(mph), { dmg: G.car.dmg }); }
  return out;
});
ok(r[5].stage === 'none' && r[5].dmg === 0, 'a touch at 5 mph is forgiven');
ok(r[10].stage === 'dented' && r[20].stage === 'crumpled' && r[20].dmg === 2 && r[10].drives && r[20].drives, 'dented at 10, crumpled at 20, and it still drives');
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars, m = __mark();
  __patrolAway();
  __pull(60, 46.2, Math.PI / 2);
  G.car.dmg = 0;
  const hit = C.crash(35), st = C.state(), x0 = G.car.x;
  // he tries to drive it: it does not answer
  dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyW' }));
  for (let i = 0; i < 120; i++) LEDGER.tick(1 / 60);
  dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyW' }));
  const moved = Math.abs(G.car.x - x0), said = __since(m);
  const out = LEDGER.cab.getOut();
  return { hit, off: st.offRoadUntil - G.t, moved, said, out, next: LEDGER.game.fares.next(), kinds: G.events.slice(-3).map((e) => e.kind) };
});
ok(r.hit.stage === 'dead' && !r.hit.drives && r.off > 1400, 'at 35 mph in one hit it will not drive on, and is off the road a day');
ok(r.moved < 0.5 && r.said.some((s) => /will not start|off the road/.test(s)), 'it says so at once and does not answer the pedals: ' + (r.said[0] || '').slice(0, 80));
ok(r.out, 'and he can always get out and walk (ER-DRIVE-01)');
r = await L(() => {
  const G = LEDGER.G;
  G.tom.x = -40; G.tom.z = 42.6; // he walks away
  LEDGER.step(1);
  const fetched = { x: G.car.x, z: G.car.z, dead: LEDGER.game.cars.state().deadAt };
  // next day: back on the road, mended
  G.t += 1441;
  LEDGER.step(1);
  const st = LEDGER.game.cars.state();
  return { fetched, back: st.offRoadUntil <= G.t };
});
ok(r.fetched.dead === null && Math.hypot(r.fetched.x - 4.1, r.fetched.z - 37.4) < 1 && r.back, 'the firm fetches it to the rank, and a day later it drives again');

// ---- a hit: the hurt scales, nobody dies, and the choice is put at once (ER-DRIVE-03, 05) ----
await L(() => { LEDGER.G.car.dmg = 0; LEDGER.cab.getIn(); __pull(30, 46.2, Math.PI / 2); __patrolAway(); });
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars, out = [];
  for (const [mph, aimed] of [[5, false], [15, false], [30, false], [50, false], [50, true]]) {
    const P = G.people.pax2;
    P.gone = false; P.down = false; P.dead = false; P.hurt = 0; P.space = 'street'; P.x = 36; P.z = 46.2;
    C.state().hit = null;
    const m = __mark(), q = C.hit('pax2', mph, aimed);
    LEDGER.tick(1 / 60);
    out.push({ mph, aimed, kind: q.rule.kind, hurt: q.hurt, dead: q.dead || !!P.dead, put: q.choicePut, said: __since(m), prompts: LEDGER.prompts() });
  }
  return out;
});
ok(r[0].kind === 'none' && !r[0].put, 'at 5 mph nobody is knocked down');
ok(r[1].hurt < r[2].hurt && r[2].hurt < r[3].hurt, `the hurt scales with speed: ${r.map((q) => q.hurt.toFixed(2)).join(', ')}`);
ok(r.every((q) => !q.dead && q.hurt < 1), 'nobody dies, at 50 mph or aimed (canon)');
ok(r[1].put && r[1].said.some((s) => /Stop and help.*drive off/i.test(s)), 'the choice is put in the same frame, in words: ' + (r[1].said.slice(-1)[0] || '').slice(0, 90));
ok(r[1].prompts.some((p) => p.key === 'Y' && p.text === 'Stop and help') && r[1].prompts.some((p) => p.key === 'G' && p.text === 'Drive off'), 'both answers are on the keys');
ok(r[4].said.length >= 0 && (await L(() => LEDGER.G.events.some((e) => e.kind === 'car_aimed'))), 'a car aimed at a man is an attack the town can tell of');

// stop and help: his face beside the cab, the ambulance at its minute, the person in hospital, the game goes on
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars, P = G.people.pax2;
  P.gone = false; P.down = false; P.hurt = 0; P.x = 36; P.z = 46.2; C.state().hit = null; C.state().amb = null;
  C.hit('pax2', 30, false);
  LEDGER.press('Y');
  const st = C.state(), a = { inCar: G.tom.inCar, amb: !!st.amb, hitGone: st.hit === null, kinds: G.events.slice(-2).map((e) => e.kind) };
  // he rings from the phone box on the corner
  G.tom.x = 7.3; G.tom.z = -12;
  const pr = LEDGER.prompts();
  LEDGER.press('E');
  const called = st.amb && st.amb.calledAt, due = st.amb && st.amb.arrivesAt;
  let at = null;
  for (let i = 0; i < 200 && at === null; i++) { LEDGER.step(0.25); if (!C.state().amb) at = G.t; }
  return { a, pr, called, due, at, gone: P.gone, down: P.down, dead: !!P.dead, paused: G.paused, ended: G.story.ended, last: C.state().lastAmb, share: C.faresLostShare() };
});
ok(!r.a.inCar && r.a.amb && r.a.hitGone && r.a.kinds.includes('hit_helped'), 'Y: he stops and gets out, and is seen beside the cab');
ok(r.pr.some((p) => /Ring for an ambulance/.test(p.text)), 'the phone box offers the call');
ok(r.due - r.called === 10 && r.at !== null && r.at - r.called >= 10 && r.at - r.called < 10.6, `the ambulance is there ten game minutes after the call (${(r.at - r.called).toFixed(2)})`);
ok(r.gone && !r.down && !r.dead && !r.ended, 'the person goes to hospital alive, and the game goes on');
ok(r.share > 0 && r.share <= 0.15, `stopping still costs the firm's name a little (${r.share})`);

// drive off: a hit-and-run. The car is described, the firm pays in fares for five days, a patrol car that sees it stops it
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars, P = G.people.pax0;
  LEDGER.cab.getIn(); __pull(30, 46.2, Math.PI / 2); __patrolAway();
  P.gone = false; P.down = false; P.hurt = 0; P.space = 'street'; P.x = 36; P.z = 46.2; C.state().hit = null;
  C.hit('pax0', 30, false);
  LEDGER.press('G');
  const st = C.state();
  const day0 = C.faresLostShare();
  const t0 = G.t;
  G.t = t0 + 2.5 * 1440; const day2 = C.faresLostShare();
  G.t = t0 + 5 * 1440; const day5 = C.faresLostShare();
  G.t = t0;
  return { kinds: G.events.slice(-2).map((e) => e.kind), wanted: st.wanted && st.wanted.why, amb: !!st.amb, day0, day2, day5, ended: G.story.ended, notes: G.ledger.notes.slice(-1)[0].text };
});
ok(r.kinds.includes('hit_run') && r.wanted === 'a hit-and-run' && !r.ended, 'G: a hit-and-run. The car is described and the game goes on');
ok(r.amb, 'somebody still rings for the person in the road');
ok(r.day0 === 0.6 && r.day2 === 0.3 && r.day5 === 0, `the firm's name pays in fares for five days, fading: ${r.day0}, ${r.day2}, ${r.day5} (ER-DRIVE-10)`);
r = await L(() => {
  const G = LEDGER.G, F = LEDGER.game.fares, m = __mark();
  G.story.fare = null; F.state().lost = 0; F.state().after = null;
  let lost = 0, got = 0;
  for (let i = 0; i < 5; i++) {
    G.story.fare = null;
    LEDGER.fare.call();
    if (G.story.fare) { got++; F.hand(); } else lost++;
  }
  return { lost, got, said: __since(m), to: F.state().lostToOtherFirm };
});
ok(r.to >= 2 && r.said.some((s) => /Stather's/.test(s)), `meanwhile people ring the other firm: ${r.to} of 5 calls went to Stather's (A14)`);
// the patrol car sees the described car: a stop; he does not pull over: a chase, which ends
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars;
  G.story.fare = null;
  __pull(60, 46.2, Math.PI / 2);
  C.patrolAt(40, 46.2);
  const m = __mark();
  LEDGER.tick(1 / 60);
  LEDGER.tick(1 / 60);
  const st = C.state().stop && Object.assign({}, C.state().stop);
  return { st, said: __since(m) };
});
ok(r.st && r.st.st === 'flash' && r.st.why === 'the car is described', 'a patrol car that sees the described car starts a stop');
ok(r.said.some((s) => /blue lamp/.test(s)), 'it announces itself: a lamp and a horn before anything else (ER-POL-02)');
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars;
  // he keeps driving east, flat out, then turns up out of sight
  let secs = 0, phase = null;
  dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyW' }));
  for (let i = 0; i < 100 * 60 && C.state().stop; i++) {
    LEDGER.tick(1 / 60);
    secs += 1 / 60;
    if (C.state().stop && C.state().stop.st === 'chase' && !phase) phase = secs;
    if (G.car.x > 140) { G.car.x = 60; } // round again: the quay is long enough to keep running on
  }
  dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyW' }));
  return { secs, phase, last: C.runtime().lastChase, ended: G.story.ended, kinds: G.events.slice(-4).map((e) => e.kind) };
});
ok(r.phase !== null && r.kinds.includes('stop_refused'), `not pulling over becomes a chase after ${r.phase && r.phase.toFixed(1)} s`);
ok(r.last && r.secs < 100, `the chase ends, ${r.last && r.last.out}, ${r.secs.toFixed(0)} s after the lamp (ER-POL-04: within 90 s of the chase)`);
ok(!r.ended, 'and the game goes on');

// ---- the patrol car never stops ordinary driving, and stops speed only when it sees it (ER-TRAFFIC-01, 02) ----
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars, st = C.state();
  st.wanted = null; st.stop = null;
  __pull(-60, 46.2, Math.PI / 2);
  let stops0 = st.stops;
  // 40 real seconds of lawful driving with the patrol car right behind
  for (let i = 0; i < 40 * 30; i++) {
    C.patrolAt(G.car.x - 14, 46.2);
    G.car.v = 12; // about 27 mph
    G.car.x += 12 / 30; if (G.car.x > 140) G.car.x = -60;
    G.car.z = 46.2;
    LEDGER.tick(1 / 30);
    G.car.v = 12;
  }
  const lawful = st.stops - stops0;
  // far over the limit, unseen (the patrol car is the other side of the town)
  __patrolAway(); __pull(-60, 46.2, Math.PI / 2);
  stops0 = st.stops;
  for (let i = 0; i < 60; i++) { G.car.v = 16; LEDGER.tick(1 / 30); }
  const unseen = st.stops - stops0;
  // the same in its sight
  st.stop = null; __pull(-60, 46.2, Math.PI / 2); C.patrolAt(-80, 46.2);
  G.car.v = 16; LEDGER.tick(1 / 60);
  const seen = st.stop && st.stop.why;
  return { lawful, unseen, seen };
});
ok(r.lawful === 0, 'forty seconds at 27 mph with a patrol car behind: never stopped');
ok(r.unseen === 0 && r.seen === 'speed', 'far over the limit: nothing unseen, a stop when the patrol car sees it');
// pull over: a caution, the plate noted, minutes lost and no more
r = await L(async () => {
  const G = LEDGER.G, C = LEDGER.game.cars, t0 = G.t;
  G.car.v = 0;
  C.patrolAt(G.car.x - 10, 46.2);
  for (let i = 0; i < 120; i++) { G.car.v = 0; LEDGER.tick(1 / 60); }
  return { modal: LEDGER.ui.modal, who: document.getElementById('dwho').textContent, t0 };
});
ok(r.modal === 'dialog' && /patrol constable/.test(r.who), 'pulled over: a patrol constable at the window');
for (let i = 0; i < 6; i++) { await L(() => { const d = document.getElementById('dialog'); d.click(); dispatchEvent(new KeyboardEvent('keydown', { code: 'Space' })); }); await h.sleep(700); }
r = await L((t0) => {
  const G = LEDGER.G, st = LEDGER.game.cars.state();
  return { stop: st.stop, plate: st.plateNoted, mins: G.t - t0, last: LEDGER.game.cars.runtime().lastStop, modal: LEDGER.ui.modal, paused: G.paused };
}, r.t0);
ok(r.stop === null && r.plate === 1 && r.last && r.mins < 30, `a caution and the plate in his book; ${r.mins.toFixed(0)} game minutes lost (ER-TRAFFIC-01: under 2 real minutes) ` + JSON.stringify(r.modal));

// ---- the horn (A32) ----
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars;
  LEDGER.cab.getIn();
  __pull(1.9, 0, 0);
  const near = G.people.pax0, far = G.people.pax1;
  for (const P of [near, far]) { P.gone = false; P.down = false; P.space = 'street'; P.awake = true; P.alert = null; P.hold = true; }
  near.x = 6.3; near.z = 30; far.x = 6.3; far.z = -150;
  G.t = Math.floor(G.t / 1440) * 1440 + 14 * 60;
  const day = C.horn(false);
  const a = { nearAlert: !!near.alert, farAlert: !!far.alert };
  // a fare waiting inside 15 m comes to the car on a toot
  LEDGER.game.fares.state().done = [];
  G.story.fare = null;
  LEDGER.game.fares.offer('albert_inf'); LEDGER.game.fares.accept();
  const P = LEDGER.game.fares.places().busstop.p;
  __pull(P[0], P[1] + 12, 0);
  const toot = C.horn(false);
  let secs = 0;
  while (secs < 12 && LEDGER.game.fares.read().state !== 'carry') { LEDGER.step(0.5); secs += 0.5; }
  const f = LEDGER.game.fares.read().state;
  G.story.fare = null;
  // a long blast at night is remembered
  G.t = Math.floor(G.t / 1440) * 1440 + 23.5 * 60;
  const n = G.events.length;
  const night = C.horn(true);
  return { day, a, toot, secs, f, night, kinds: G.events.slice(n).map((e) => e.kind) };
});
ok(r.day.reachMetres === Math.round(60 * (1 - 0.3 * 0)) || r.day.reachMetres <= 60, `the horn by day reaches ${r.day.reachMetres} m`);
ok(r.a.nearAlert && !r.a.farAlert && r.day.heard.includes('pax0') && !r.day.heard.includes('pax1'), 'everybody inside its reach hears it and turns; nobody outside does');
ok(r.toot.fareOutInRealSeconds !== null && r.f === 'carry' && r.secs <= 10, `a toot within 15 m brings the fare out and in within 10 s (${r.secs} s)`);
ok(r.night.remembered && r.kinds.includes('horn_night') && r.night.reachMetres > r.day.reachMetres, `a long blast at night carries further (${r.night.reachMetres} m) and is remembered as a noise`);

// ---- tailing by car (A2) ----
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars;
  G.t = Math.floor(G.t / 1440) * 1440 + 11 * 60;
  LEDGER.cab.getIn(); __patrolAway();
  C.state().sign = false; // no roof sign: the reach is the plain 22 m
  C.tailStart();
  // he hangs well back, 45 m behind the van along its own way, the whole run
  const trail = [];
  let made = false, secs = 0;
  while (secs < 120 && !C.runtime().van.arrived) {
    const v = C.runtime().van;
    trail.push([v.x, v.z]);
    const back = trail[Math.max(0, trail.length - 1 - 160)];
    __pull(back[0], back[1]);
    LEDGER.tick(1 / 30); secs += 1 / 30;
    if (C.runtime().van.s.made) made = true;
  }
  const v = C.runtime().van;
  // he comes up to where it has stopped
  __pull(v.x - 12, v.z); LEDGER.step(0.5);
  return { made, shows: C.runtime().van.shows, arrived: v.arrived, learned: C.runtime().van.learned, secs, notes: G.ledger.notes.map((n) => n.text) };
});
ok(r.arrived && !r.made, `hanging well back the whole way he is never made, at any distance (${r.secs.toFixed(0)} s; ER-TAIL-01) ` + JSON.stringify(r.shows));
ok(r.learned && r.notes.some((n) => /goes from Rita's corner to the fish dock/.test(n)), 'what the tail learned is in the Ledger at once (ER-TAIL-03)');
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars;
  C.state().sign = true;
  C.tailStart();
  let secs = 0;
  // on his bumper, with the firm's sign lit
  while (secs < 90 && !C.runtime().van.s.made && !C.runtime().van.arrived) {
    const v = C.runtime().van;
    __pull(v.x, v.z - 8 > -200 ? v.z - 8 : v.z, 0);
    if (Math.abs(v.z - 46.2) < 2) __pull(v.x - 8, v.z, Math.PI / 2);
    LEDGER.tick(1 / 30); secs += 1 / 30;
  }
  C.state().sign = true;
  return { shows: C.runtime().van.shows, made: C.runtime().van.s.made, kinds: G.events.slice(-2).map((e) => e.kind) };
});
ok(r.made && r.shows.length >= 2 && r.shows[0].shows === 'doubt' && r.shows[r.shows.length - 1].shows === 'made', 'on his bumper he is made, and the doubt showed first: ' + JSON.stringify(r.shows) + ' (ER-TAIL-02)');
ok(r.kinds.includes('tail_made'), 'being made is a thing the town can tell');

// ---- riding as a passenger (A24; ER-RIDE-01) ----
r = await L(async () => {
  const G = LEDGER.G, C = LEDGER.game.cars;
  LEDGER.cab.getOut();
  G.tom.x = 6.3; G.tom.z = 36;
  const t0 = G.t, home = { x: G.car.x, z: G.car.z };
  const mins = await C.ride('Kevin Needham', 'station', true);
  return { mins, passed: G.t - t0, z: G.tom.z, car: Math.hypot(G.car.x - home.x, G.car.z - home.z), last: C.state().lastRide };
});
await h.sleep(1500);
ok(Math.abs(r.passed - r.mins) < 0.2 && r.mins > 5, `a skipped ride passes its drive time and no more: ${r.mins.toFixed(1)} game minutes (${r.passed.toFixed(1)} passed)`);
ok(r.z < -190 && r.car < 1, 'he is set down at the station, and his own car is where he left it');
r = await L(async () => {
  const G = LEDGER.G, C = LEDGER.game.cars;
  G.tom.x = 6.3; G.tom.z = -190;
  await C.ride('Kevin Needham', 'boarding', false);
  const a = { inCar: G.tom.inCar, auto: !!C.state().auto, prompts: LEDGER.prompts() };
  let secs = 0;
  while (secs < 60 && C.state().auto) { LEDGER.tick(1 / 30); secs += 1 / 30; }
  return { a, secs, z: G.tom.z, x: G.tom.x, inCar: G.tom.inCar };
});
ok(r.a.inCar && r.a.auto && r.a.prompts.some((p) => /Skip the ride/.test(p.text)), 'riding along: he is driven, and can skip the rest');
ok(!r.inCar && Math.abs(r.z + 46) < 12 && r.secs < 40, `the driver gets him to Regent House in ${r.secs.toFixed(0)} s`);

// ---- paint (A24; ER-PAINT-01) ----
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars;
  LEDGER.cab.getIn(); __pull(60, 46.2, Math.PI / 2);
  const id = LEDGER.ledger.act('crash', {});
  LEDGER.tick(1 / 60);
  const before = C.named(id);
  C.respray();
  const after = C.named(id);
  LEDGER.tick(1 / 60);
  const id2 = LEDGER.ledger.act('crash', {});
  LEDGER.tick(1 / 60);
  const fresh = C.named(id2), look = C.look();
  C.signBack(); C.state().offRoadUntil = 0;
  return { before, after, fresh, look };
});
ok(r.before.names && r.before.firm, "a deed done from the cab names the car, and the roof sign makes it the firm's (ER-EYES-10)");
ok(!r.after.names && !r.look.sign, 'after the respray a witness of the old paint does not name this car');
ok(r.fresh.names && !r.fresh.firm, "and a new sighting names the plain car, not the firm's");

// ---- taking a parked car (A27; ER-TAKE-01) ----
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars;
  LEDGER.cab.getOut();
  const p = C.parked()[0];
  G.tom.x = p.x + 2.2; G.tom.z = p.z;
  LEDGER.tick(1 / 60);
  const pr = LEDGER.prompts(), n = G.events.length, m = __mark();
  LEDGER.press('G');
  const forcing = C.runtime().forcing, noise = G.tom.noiseP;
  let secs = 0;
  while (secs < 8 && C.state().have !== 'taken') { LEDGER.tick(1 / 30); secs += 1 / 30; }
  const st = C.state();
  return { pr, forcing, noise, secs, have: st.have, inCar: G.tom.inCar, kinds: G.events.slice(n).map((e) => e.kind), said: __since(m), look: C.look(), taken: st.taken, at: G.t };
});
ok(r.pr.some((p) => p.key === 'G' && /Force the car door \(loud\)/.test(p.text)), 'a parked car offers one thing: force the door, and it says it is loud');
ok(r.forcing && r.noise >= 24 && Math.abs(r.secs - 6) < 0.5, `it is loud (${r.noise} m) and takes about six seconds (${r.secs.toFixed(1)} s), with no game to play`);
ok(r.have === 'taken' && r.inCar && r.kinds.includes('car_taken'), 'then he is driving it, and it is a deed with its witnesses');
r = await L(() => {
  const G = LEDGER.G, C = LEDGER.game.cars, st = C.state();
  const id = LEDGER.ledger.act('crash', {});
  LEDGER.tick(1 / 60);
  const named = C.named(id);
  LEDGER.step(1);
  const early = st.taken.reported;
  G.t = st.taken.at + 181;
  LEDGER.step(1);
  const late = st.taken.reported;
  // the patrol car sees it
  __pull(60, 46.2, Math.PI / 2); C.patrolAt(40, 46.2);
  st.stop = null;
  LEDGER.tick(1 / 60); LEDGER.tick(1 / 60);
  const why = st.stop && st.stop.why;
  st.stop = null;
  C.leaveTaken();
  return { named, early, late, why, have: st.have, home: Math.hypot(G.car.x - 60, G.car.z - 46.2) > 5 };
});
ok(r.named.names && !r.named.firm, "a deed from the taken car is not the firm's: no sign on its roof");
ok(!r.early && r.late, 'its owner reports it once he finds it gone, three game hours on, never before');
ok(r.why === 'a car reported taken' && r.have === 'cab', 'a patrol car that sees a reported car stops it; left, he has his own cab again');

// ---- traffic: only the player's car can strike anybody (4.5.1) ----
r = await L(() => {
  const G = LEDGER.G;
  LEDGER.cab.getOut(); G.tom.x = 6.3; G.tom.z = 36;
  G.t = Math.floor(G.t / 1440) * 1440 + 12 * 60;
  let contacts = 0, crossings = 0, minGap = 99;
  const P = G.people.pax1;
  P.gone = false; P.down = false; P.space = 'street'; P.hold = true;
  for (let i = 0; i < 40 * 30; i++) {
    LEDGER.tick(1 / 30);
    const cars = LEDGER.streetThings().cars.filter((c) => !c.parked);
    if (i % 90 === 0 && cars.length) {
      // somebody steps into the road ahead of a moving car
      const c = cars[(i / 90) % cars.length | 0], d = 6 + ((i / 90) % 5);
      P.x = c.xMetres + Math.sin(c.facingRadians) * d;
      P.z = c.zMetres + Math.cos(c.facingRadians) * d;
      crossings++;
    }
    for (const c of cars) {
      const g = Math.hypot(c.xMetres - P.x, c.zMetres - P.z);
      minGap = Math.min(minGap, g);
      if (g < 0.9) contacts++;
    }
  }
  return { contacts, crossings, minGap, down: !!P.down, hurt: P.hurt || 0 };
});
ok(r.crossings >= 5 && r.contacts === 0 && !r.down, `${r.crossings} times somebody steps out ahead of a car in the road: every driver stops (nearest ${r.minGap.toFixed(1)} m)`);

r = await L(() => LEDGER.game.faults);
ok(r.length === 0, 'no fault in any system: ' + r.slice(0, 2).join(' | '));
ok(h.errors.length === 0, 'no page errors: ' + h.errors.slice(0, 2).join(' | '));
await h.close();
console.log(bad ? 'FAIL' : 'PASS');
process.exit(bad ? 1 : 0);
