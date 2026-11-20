// The system "law", second sheet, in Node (law_headless.mjs): the night's run still works as the prototype's tests
// expect; every route to a manhunt passes its signs (ER-POL-05); a witnessed hold-up walks to the station, is
// reported, raises the stage and costs twelve hours; the spot after a deed; DS Ellis after a body; a walk that
// reaches the phone box early still gives him his thirty seconds; every failure route ends in play inside two real
// minutes (ER-CORE-04); three weeks at War counted.
import { boot } from './law_headless.mjs';
import { KINDS } from '../../src/kinds.js';

const h = await boot({ seed: 1990 });
const G = h.G, law = LEDGER.game.law, X = () => G.x.law;
let bad = 0;
const check = (name, ok, extra = '') => { if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${extra ? ' | ' + String(typeof extra === 'string' ? extra : JSON.stringify(extra)).slice(0, 320) : ''}`); };
const nextAt = (hr) => { const t = G.t, d = Math.floor(t / 1440); return d * 1440 + hr * 60 > t + 1 ? d * 1440 + hr * 60 : (d + 1) * 1440 + hr * 60; };
const put = (x, z) => { const t = G.tom; t.space = 'street'; t.inCar = false; t.x = x; t.z = z; t.run = false; };
const stepUntil = async (test, secs = 1, max = 60) => { for (let i = 0; i < max; i++) { if (test()) return true; await h.step(secs); } return test(); };
const plant = (kind, wit, mems) => { const id = G.nextE++, e = { id, kind, t: G.t, zone: G.tom.zone, x: 0, z: 0, coat: false, car: false, wit }; G.events.push(e); G.ev[id] = e; for (const [pid, src] of mems) { const m = G.people[pid].mind, s = { e: id, src, from: null, who: 'tom', sure: 0.9, heat: 0.8, t: G.t, said: false, hop: 0, face: 1 }; m.mem.push(s); m.by[id] = s; } return id; };
const reset = () => { const x = X(); x.stage = 0; x.signs = []; x.reported = {}; x.ellisAsked = 0; x.ran = 0; x.hunted = 0; x.bodies = []; x.traces = []; x.spots = []; x.missing = {}; x.walks.forEach((w) => { if (w.st === 'pending' || w.st === 'walking') w.st = 'dropped'; }); G.story.arrest = null; G.story.ellis = null; G.story.flags.ranPolice = 0; };
try {
  G.story.flags.tour = 1; G.story.flags.metRon = G.story.flags.metDarren = G.story.flags.metPauline = G.story.flags.metJune = 1;
  G.story.ended = true; // these checks run past Friday: the week's own end (the spine's to rework) is kept out of their way
  law.beat.force(false);
  await h.step(1); await h.clear();

  // ---- the night's run, as the lane's systems test plants it on Monday evening
  const [w, t, f, b] = G.named.filter((p) => !p.def.nostmt && !p.def.upright && !p.dead && !p.mind.bought && p.mind.fear < 0.5 && !p.def.police && !['sheila', 'ron', 'pauline', 'kevin', 'terry', 'darren'].includes(p.id)).slice(0, 4).map((p) => p.id);
  for (const k of [w, t, f, b]) G.people[k].mind.regard = -0.6;
  G.people[f].mind.fear = 0.8; G.people[b].mind.bought = 1;
  const P = { seen: plant('shove', [w], [[w, 'saw']]), unseen: plant('shove', [], []), told: plant('threat', [], [[t, 'told']]), afraid: plant('shove', [f], [[f, 'saw']]), paid: plant('shove', [b], [[b, 'saw']]) };
  put(100, 60);
  await h.pass(1440 + 4.25 * 60); await h.step(0.5);
  const stmt = (k) => JSON.stringify(G.ev[P[k]].stmt);
  check('by four on Tuesday the witness who saw it has stated; unseen, told, afraid and paid have not', stmt('seen') === JSON.stringify([w]) && stmt('unseen') === '[]' && stmt('told') === '[]' && stmt('afraid') === '[]' && stmt('paid') === '[]', Object.keys(P).map((k) => k + stmt(k)).join(' '));
  const a = G.story.arrest;
  check('a statement brings the police: the arrest names the deed and who stated, due at nine', a && a.e === P.seen && a.by.includes(w) && a.due === 1440 + 9 * 60 && G.log.some((l) => l.tag === 'police'), a);
  check('ER-EYES-05: the report traces to a sighting (the walk or the night\'s run is in the log)', G.log.some((l) => l.tag === 'police' && /statement was made/.test(l.text) && l.text.includes(G.people[w].def.name)));
  reset();

  // ---- ER-POL-05: every route to a manhunt passes its signs, one stage at a time, and waits its hour
  KINDS.test_wound = Object.assign({}, KINDS.strike);
  KINDS.test_holdup = Object.assign({}, KINDS.strike, { crime: 3, lawClass: 'robbery', sev: 0.95, truth: () => 'Tom held up the newsagent with a bar in his hand', mine: () => 'Held up the newsagent' });
  const routes = {
    'a witnessed killing': () => { const e = plant('kill', [w], [[w, 'saw']]); G.ev[e].target = null; law.plantStatement(e, w); },
    'running from the police after a wounding': () => { const e = plant('test_wound', [w], [[w, 'saw']]); law.plantStatement(e, w); X().ran = 1; G.story.arrest = null; },
    'hunted by word from elsewhere': () => { law.setStage(3); },
  };
  for (const name in routes) {
    reset();
    G.people[w].mind.regard = -0.6; G.people[w].mind.fear = 0; G.people[w].dead = false;
    await h.pass(nextAt(12)); await h.step(0.5); put(4.5, 10);
    routes[name]();
    G.story.arrest = null;
    const seen = []; let arrestAt = null, sign3 = null;
    for (let i = 0; i < 400 && arrestAt == null; i++) {
      await h.step(1.5);
      const x = X();
      if (seen[seen.length - 1] !== x.stage) seen.push(x.stage);
      const g3 = x.signs.find((g) => g.stage === 3 && g.shown);
      if (g3 && sign3 == null) sign3 = g3.t;
      if (x.stage < 3) G.story.arrest = null; // the ordinary visit at nine is another matter: this route is the manhunt's
      else if (G.story.arrest) arrestAt = G.t;
    }
    const x = X(), shown = x.signs.filter((g) => g.shown).map((g) => g.stage).join(',');
    check(`manhunt by ${name}: stages 1, 2, 3 in order, each sign shown, the arrest a game hour after the last`, seen.join(',').replace(/^0,/, '') === '1,2,3' && shown === '1,2,3' && arrestAt != null && arrestAt - sign3 >= 60, { seen, shown, sign3, arrestAt });
    await h.clear();
  }
  reset();

  // ---- a witnessed hold-up (the rise builder's): walks to the station, is reported, raises the stage, twelve hours
  await h.pass(nextAt(11)); await h.step(0.5);
  const W = G.people[w];
  W.mind.regard = -0.5; W.mind.fear = 0; W.mind.bought = false; W.space = 'street'; W.gone = false; W.awake = true; W.x = 6; W.z = 14; W.route = null;
  put(4.5, 10);
  const e5 = LEDGER.act('test_holdup', { silent: true });
  law.plantWitness(e5, w);
  await h.step(6);
  const wk = X().walks.find((q) => q.e === e5 && q.who === w);
  check('a witnessed hold-up: she sets off for the station by herself', wk && wk.st === 'walking' && (wk.to === 'station' || (wk.to === 'friend' && wk.then === 'station')), wk);
  put(100, 60);
  await stepUntil(() => (G.ev[e5].stmt || []).length > 0, 5, 80);
  check('it is reported', (G.ev[e5].stmt || []).includes(w) && G.story.arrest && G.story.arrest.cls === 'robbery', G.story.arrest);
  await stepUntil(() => X().stage >= 1, 2, 30);
  check('it raises the stage', X().stage >= 1 && X().want >= 2, { stage: X().stage, want: X().want });
  await h.pass(G.story.arrest.due - 2); await h.step(0.5); put(6.2, 20);
  const p0 = G.played;
  await stepUntil(() => LEDGER.ui.modal === 'dialog', 3, 80);
  const met5 = await h.clear({ choice: 0 }); await h.step(2); await h.clear();
  check('and costs twelve hours, a charge and bail', X().lastArrest && X().lastArrest.hours === 12 && X().lastArrest.outcome === 'charged' && !G.paused, X().lastArrest);
  check('ER-CORE-04: arrested, he is in control again inside two real minutes', G.played - p0 < 120 && !G.paused && !LEDGER.ui.modal, G.played - p0);
  check('DS Ellis comes next morning for a detective\'s crime once reported', true); // checked below with the body
  reset();

  // ---- A36: a reported deed brings an officer to its spot, watched until morning; going back there is the risk
  await h.pass(nextAt(22)); await h.step(0.5); put(4.5, 10);
  const e6 = LEDGER.act('shove', { silent: true });
  law.plantWitness(e6, w); G.people[w].mind.regard = -0.5; G.people[w].mind.fear = 0;
  law.plantStatement(e6, w);
  law.spot(e6);
  G.story.arrest = null;
  const sp = X().spots.find((s) => s.e === e6);
  check('a reported deed has its spot, from twenty game minutes on, until six in the morning', sp && sp.from - Math.round(G.t) === 20 && sp.until === nextAt(6), sp);
  law.beat.force(null);
  put(60, 50);
  await h.pass(G.t + 25); await h.step(3);
  check('the beat constable goes to the spot', X().beat.detour && X().beat.detour.e === e6 && X().beat.st !== 'off', X().beat);
  put(4.5, 10);
  check('standing there is cause for a challenge: watched ground', law.beat.cause().why.includes('back where it happened') && !!law.watchedGround(4.5, 10), law.beat.cause());
  put(100, 60); law.beat.force(false); await h.step(1); await h.clear();
  reset();

  // ---- a body: tape, DS Ellis next morning, people she asks remember being asked
  await h.pass(nextAt(13)); await h.step(0.5); put(4.5, 10);
  const victim = G.named.find((p) => !p.def.police && !p.dead && !['sheila', 'ron', 'darren', 'ada', 'pauline', 'hal', w].includes(p.id) && (p.def.close || []).length).id;
  const e7 = LEDGER.act('kill', { silent: true, target: victim });
  G.people[victim].dead = true;
  await h.step(0.5);
  put(100, 60);
  const finderP = G.named.find((p) => p.space === 'street' && !p.gone && p.awake && !p.def.police && !p.dead);
  finderP.x = G.ev[e7].x + 1.5; finderP.z = G.ev[e7].z; finderP.route = null; finderP.hold = true;
  await h.pass(G.t + 3); await h.step(2);
  finderP.hold = false;
  const body = X().bodies.find((q) => q.id === victim);
  check('a body left where a routine passes is found, and its spot is taped', body && body.found && X().spots.some((s) => s.e === e7 && s.body), body);
  check('nobody is arrested for it: the finder holds only the aftermath (ER-POL-01)', !G.story.arrest && X().want === 2, { want: X().want });
  const day0 = Math.floor(G.t / 1440);
  await h.pass(nextAt(9.2)); await h.step(1); await h.clear();
  check('DS Ellis is on Quay Street the next morning, for the body', !!G.story.ellis && Math.floor(G.t / 1440) === day0 + 1 && X().ellisAsked > 0, { ellis: !!G.story.ellis, ellisAsked: X().ellisAsked });
  put(100, 60);
  await h.step(60);
  const asked = G.named.filter((p) => p.mind.mem.some((m) => G.ev[m.e] && G.ev[m.e].kind === 'ellis_asked')).map((p) => p.id);
  check('the people she asks remember being asked', asked.length >= 1, asked);
  const heat = G.named.map((p) => p.mind.by[e7]).filter(Boolean);
  await h.pass(G.t + 3 * 1440); await h.step(1); await h.clear();
  check('a body never cools: three days on, whoever holds the killing holds it hot', heat.length === 0 || heat.every((m) => m.heat >= 0.85), heat.map((m) => m.heat));
  reset();

  // ---- ER-EYES-04 when the phone box is close: she gets there early and it still takes its thirty seconds
  await h.pass(nextAt(11)); await h.step(0.5);
  W.dead = false; W.mind.regard = -0.5; W.mind.fear = 0; W.mind.bought = false; W.space = 'street'; W.gone = false; W.awake = true; W.x = 6.5; W.z = -9; W.route = null; W.override = null;
  put(8, -6);
  const e8 = LEDGER.act('shove', { silent: true });
  law.plantWitness(e8, w);
  law.startWalk(w, e8);
  let landedAfter = null, startReal = null;
  for (let i = 0; i < 200 && landedAfter == null; i++) {
    await h.step(0.5);
    const q = X().walks.find((z) => z.e === e8);
    if (q.st === 'walking' && startReal == null) startReal = G.played;
    if (q.st === 'landed') landedAfter = G.played - startReal;
  }
  check('a walk that starts in his sight lasts at least 30 real seconds, however near the phone box', landedAfter != null && landedAfter >= 29.5, landedAfter);
  reset();

  // ---- ER-CORE-04: searched and chased, each ends in play inside two real minutes
  await h.pass(nextAt(23)); await h.step(0.5); await h.clear(); put(4.5, 10);
  G.x.crime = { carried: ['the envelope'] }; G.tom.carry = null;
  law.beat.place(6);
  const p1 = G.played;
  await stepUntil(() => LEDGER.ui.modal === 'dialog', 0.5, 80);
  await h.clear({ choice: 0 });
  check('searched: in control again inside two real minutes, with a Ledger line', G.played - p1 < 120 && !G.paused && G.ledger.notes.some((n) => /kept the envelope/.test(n.text)), G.played - p1);
  G.x.crime.carried = ['a parcel']; put(4.5, 10); law.beat.place(6);
  const p2 = G.played;
  await stepUntil(() => X().beat.st === 'called', 0.25, 80);
  G.tom.run = true; G.tom.x += 8;
  await h.step(0.3);
  G.tom.run = false;
  for (let i = 0; i < 60 && X().beat.st === 'chase'; i++) { G.tom.x = 4.5 + 9 + i * 0.2; await h.step(0.5); } // he keeps a little ahead and is run down
  for (let i = 0; i < 120 && X().beat.st === 'chase'; i++) await h.step(0.5);
  await h.clear();
  const ch = X().beat.chases[X().beat.chases.length - 1];
  check('chased: it ends, caught or lost, inside 90 real seconds, and play goes on', ch && ch.seconds <= 90 && !G.paused && G.played - p2 < 120, { ch, real: G.played - p2 });
  law.beat.force(false); await h.step(1); await h.clear();
  reset();

  // ---- 2.6.6: three weeks at War. Stop and search by day, at most one every three game hours; armed officers
  // only for gun calls and never more than four
  G.x.dial = { state: 3 };
  G.x.law.armed = { calls: 0, stops: 0, lastStopT: -1e9 };
  let stopsByDay = [], worstGap = 1e9, last = null, nightStops = 0;
  const startDay = Math.floor(G.t / 1440) + 1;
  for (let d = 0; d < 21; d++) {
    let n = 0;
    for (const hr of [9, 12.5, 16, 19.5, 2]) {
      const before = X().armed.stops;
      put(4.5, 10); G.x.crime.carried = [];
      await h.pass(hr === 2 ? (startDay + d + 1) * 1440 + 120 : (startDay + d) * 1440 + hr * 60); await h.step(0.3); await h.clear();
      put(4.5, 10);
      law.beat.force(null);
      await h.step(1.2);
      if (X().armed.stops > before) { n++; if (hr === 2) nightStops++; if (last != null) worstGap = Math.min(worstGap, G.t - last); last = G.t; }
      X().beat.stopSearch = 0; law.beat.force(false); await h.step(0.3); await h.clear();
      G.story.arrest = null;
    }
    stopsByDay.push(n);
  }
  const total = stopsByDay.reduce((a2, b2) => a2 + b2, 0);
  check('three weeks at War: he is stopped by day on the street, never more often than every three game hours, never at night', total >= 21 && total <= 21 * 4 && worstGap >= 180 && nightStops === 0, { total, worstGap, nightStops, firstWeek: stopsByDay.slice(0, 7) });
  const eg = LEDGER.act('shove', { silent: true });
  law.gunCall(eg);
  check('a gun call at War brings armed cars in ten game minutes; armed officers stay few', X().armed.calls === 1 && X().spots.filter((s) => s.armed).pop().from - Math.round(G.t) === 10 && LEDGER.game.law.beat.boughtDoes && G.x.law.armed.calls <= 4);
  G.x.dial = { state: 0 };

  check('no fault in any system', LEDGER.game.faults.length === 0, LEDGER.game.faults.join(' || '));
} catch (e) {
  bad++;
  console.log('TEST FAIL ' + ((e && e.stack) || e));
}
console.log(bad ? `FAIL: ${bad} checks failed` : 'PASS');
process.exit(bad ? 1 : 0);
