// LEDGER, the whole game: the system "fares". Fares with stories (DESIGN 5; his direction of 19 Nov; parts 3.4.1 to
// 3.4.3, 1.2.7): few and chosen, each a person with something going on, about half with one wrinkle (the talker, the
// parcel, the tail, the runner, the wait, the hurry, the face), each feeding the crime. No meter, no ratings; a fare
// ends at the door; no two fares in a week alike. Pauline gives the way by landmark and says it again on a key.
import { register, X, write, tell, hourNow, dayNow, P_, emit, on, PLACES } from './core.js';
import { G } from '../state.js';
import { hyp, quid } from '../util.js';
import { act } from '../events.js';
import { earn } from '../money.js';
import { choose, scene, say, sub } from '../ui.js';
import { SPOTS, DESTS } from '../map.js';
import { RULES } from '../rules.js';
import { FARES } from './tune/fares.js';
import { PIECE as JOBS } from './pieces/jobs.js';
import { take } from './crime.js';
import { startChase } from './foot.js';
import { know } from './way.js';

const T = RULES.game.fares;
const S = { cur: null };
const week = () => Math.floor(dayNow() / 7);
const evening = (h = hourNow()) => h >= T.eveningFromHour;
const inHours = (f, h) => (h >= f.hours[0] && h < f.hours[1]) || (f.hours[1] > 24 && h < f.hours[1] - 24);

// The next fare Pauline has: one that fits the hour and the state, and has not been driven this week.
function next() {
  const x = X('fares'),
    h = hourNow(),
    d = dayNow(),
    rung = G.x.rise ? G.x.rise.rung : 1;
  const today = x.log.filter((l) => l.day === d);
  if (today.filter((l) => l.evening === evening()).length >= (evening() ? T.eveningFaresAtMost : T.dayFaresAtMost)) return null; // few and chosen
  const f = FARES.find((q) => inHours(q, h) && (!q.days || q.days.includes(d % 7)) && (!q.fromRung || rung >= q.fromRung) && !x.log.some((l) => l.id === q.id && l.week === week()) && (!q.who || (P_(q.who) && !P_(q.who).dead && !P_(q.who).gone)) && JOBS.fns.mayStage(q.wrinkle, x.log.filter((l) => l.wrinkle !== 'none' && l.wrinkle !== 'talker').map((l) => ({ kind: l.wrinkle, playedSeconds: l.played })), G.played));
  if (!f) return null;
  const s = SPOTS[f.spot];
  x.log.push({ id: f.id, wrinkle: f.wrinkle, week: week(), day: d, evening: evening(), played: G.played, st: 'offered' });
  return { id: f.id, from: f.from, sx: s[0], sz: s[1], dest: f.to, who: f.who };
}
const spec = (f) => (f && f.id ? FARES.find((q) => q.id === f.id) : null);
const logOf = (id) => X('fares').log.filter((l) => l.id === id).slice(-1)[0];
const nameOf = (P) => (P.anon ? 'The fare' : P.def.name);

function pickup({ f, P }) {
  const F_ = spec(f);
  if (!F_) return;
  S.cur = { id: F_.id, t: 0, said: 0, pid: P.id, deadline: F_.wrinkle === 'hurry' ? G.played + T.hurryRealSeconds : null };
  logOf(F_.id).st = 'carrying';
  // the radio is the guide: Pauline gives the way by landmark (ER-DRIVE-09); R says it again
  sub(F_.way, 'Pauline, on the radio', 'face', 10);
  know(DESTS[F_.to] ? Object.keys(PLACES).find((id) => hyp(PLACES[id].x, PLACES[id].z, DESTS[F_.to].p[0], DESTS[F_.to].p[1]) < 14) || 'mickeys' : 'mickeys', 'Pauline said');
}
// What the fare has to say, in the back, while he drives.
function rideStep(dt) {
  const c = S.cur,
    f = G.story.fare;
  if (!c || !f || f.st !== 'carry') return;
  const F_ = spec(f),
    P = P_(c.pid);
  c.t += dt;
  const due = [T.talkerSpeaksAfterRealSeconds, T.talkerSecondLineAfterRealSeconds];
  if (c.said < F_.lines.length && c.said < due.length && c.t >= due[c.said] && !G.paused) {
    sub(F_.lines[c.said], nameOf(P), '', 6);
    c.said++;
    if (c.said === 1 && F_.wrinkle === 'parcel') parcelAsk(F_, P);
    if (c.said === 1 && F_.ask === 'fire') fireAsk(F_, P);
  }
}
async function parcelAsk(F_, P) {
  const i = await scene(() => choose('', `"Take this round to the green door behind the pawn shop for me. After you drop me. No questions, and there is eight pounds in it."`, ['Take it.', 'No.']));
  logOf(F_.id).choice = i === 0 ? 'took' : 'refused';
  if (i !== 0) return;
  if (!take('parcel', { name: 'a parcel in brown paper', unlawful: true })) return;
  act('took_parcel', { silent: true });
  write("A fare gave him a parcel for the green door behind Rita's: eight pounds when it is handed in. It is under his coat until then.", { key: 'parcel' + week(), how: 'Agreed it' });
  X('fares').parcel = { t: G.t };
}
async function fireAsk(F_, P) {
  const i = await scene(() => choose('alison', 'Did he ever say what he saw, the night of the fire?', ['"He never said. I hardly knew him."', '"What does the street say he saw?"', 'Say nothing, and drive.']));
  logOf(F_.id).choice = ['honest', 'asked', 'silent'][i];
  if (i === 1) {
    await scene(() => say('alison', 'The street says a lamp went over. The street always says a lamp went over. I think your uncle knew whose lamp.'));
    write('Alison Sedman, of the Mail, thinks Mickey knew who started the warehouse fire. The street says a lamp went over.', { who: 'alison', how: 'Alison said', key: 'firestreet' });
  } else if (i === 2) act('drove_quiet', { silent: true, told: ['alison'] });
  emit('fares.alison', { answer: ['honest', 'asked', 'silent'][i] });
}
// The fare's ending, by its wrinkle. Returns what he is paid (the fare itself is always the game's own).
async function drop(f, P, D) {
  const F_ = spec(f),
    c = S.cur;
  S.cur = null;
  if (!F_) return null;
  const x = X('fares'),
    L = logOf(F_.id);
  L.st = 'done';
  if (F_.learn) {
    x.learned[F_.learn.fact] = Math.round(G.t);
    write(F_.learn.text, { key: 'fare:' + F_.learn.fact, who: F_.who || undefined, how: (F_.who ? P.def.name : 'A fare') + ' said, in the cab' });
    if (F_.learn.place) know(F_.learn.place, 'a fare said');
    emit('fares.learned', { fact: F_.learn.fact });
  }
  if (F_.wrinkle === 'hurry') {
    const made = G.played <= c.deadline;
    L.made = made;
    if (made) sub('"You have saved me a night in this town." A handful of change over the fare.', nameOf(P), '', 5);
    else sub('"That was my boat." He counts the fare out to the penny.', nameOf(P), '', 5);
    return { paid: f.pay + (made ? T.hurryTipPence : 0) };
  }
  if (F_.wrinkle === 'runner') {
    // out of the door without paying: a chase on foot, or let him go
    P.x = G.car.x + T.runnerBoltsMetres;
    P.z = G.car.z + T.runnerBoltsMetres;
    P.anonRunner = true;
    x.runner = { pid: P.id, pay: f.pay };
    sub('The back door is open and he is gone, running. [F] to get out after him.', '', 'over', 6);
    startChase(P.id, { why: 'runner' });
    return { paid: 0, noFareAct: true };
  }
  if (F_.wrinkle === 'wait') {
    x.waiting = { pid: P.id, untilPlayed: G.played + T.waitRealSeconds, x: G.car.x, z: G.car.z, pay: f.pay };
    P.override = { where: 'off', act: 'idle', until: G.t + 30 };
    sub('He is out and through the door before the cab has stopped rocking. The engine is running.', '', 'over', 6);
    return { paid: 0, noFareAct: true };
  }
  if (F_.wrinkle === 'tail') return { paid: f.pay };
  return null;
}
function waitStep() {
  const x = X('fares'),
    w = x.waiting;
  if (!w || G.paused) return;
  const near = hyp(G.car.x, G.car.z, w.x, w.z) < T.waitWithinMetres && G.tom.inCar;
  if (!near) {
    x.waiting = null;
    logOf('wait').choice = 'left';
    tell('He drives off. Whoever comes out of that door will be looking for a cab that is not there.', '');
    write('Left the man at the Harbour Office to find his own way. Whatever he was doing in there, the cab was not part of it.', { how: 'Did it' });
    return;
  }
  if (G.played < w.untilPlayed) return;
  x.waiting = null;
  logOf('wait').choice = 'waited';
  act('waited_for', { place: 'the Harbour Office' });
  earn(w.pay, false, 'a fare');
  G.money.fares += w.pay;
  G.money.sinceWash += w.pay;
  earn(T.waitPaysPence, true, 'for keeping the engine running');
  sub('"Go. Not fast." He has something under his coat that he did not have before. Six pounds over the fare, folded small.', 'The fare', '', 7);
  write('Kept the engine running outside the Harbour Office while a fare was in and out with something under his coat. Six pounds for it, in the tin. Anybody watching saw a Mickey\'s cab wait.', { how: 'Did it' });
}
function parcelHotspot(out) {
  const x = X('fares'),
    t = G.tom,
    p = PLACES.ritaside;
  if (!x.parcel || t.inCar || hyp(t.x, t.z, p.x, p.z) > RULES.game.crime.doorWithinMetres) return;
  out.push({ k: 'E', t: 'Hand the parcel in at the green door', run: () => {
    const i = G.x.crime.pockets.findIndex((q) => q.id === 'parcel');
    if (i >= 0) G.x.crime.pockets.splice(i, 1);
    x.parcel = null;
    earn(T.parcelPaysPence, true, 'a parcel taken round for a fare');
    act('drop', { zone: "Rita's side door", told: ['wayne'] });
    write(`Handed the parcel in at Rita's side door. ${quid(T.parcelPaysPence)} in the tin, and Wayne Harrison saw who brought it.`, { how: 'Did it', who: 'wayne' });
  } });
}

register({
  id: 'fares',
  fresh: () => ({ log: [], learned: {}, parcel: null, runner: null, waiting: null }),
  loaded() {
    G.hooks.fareNext = next;
    G.hooks.fareDrop = drop;
    S.cur = null;
  },
  step(dt) {
    rideStep(dt);
    waitStep();
  },
  key(code) {
    // Pauline says the way again on a key (ER-DRIVE-09)
    if (code !== 'KeyR' || !G.tom.inCar || !G.story.fare) return false;
    const F_ = spec(G.story.fare);
    // before the pick-up it is the way to the fare; after, the way to where the fare is going
    if (F_) sub(G.story.fare.st === 'pickup' && F_.toPickUp ? F_.toPickUp : F_.way, 'Pauline, on the radio', 'face', 10);
    if (F_ && G.hooks.sfx) G.hooks.sfx('radio');
    return !!F_;
  },
  hotspots(out) {
    parcelHotspot(out);
  },
  hook: {
    x: () => X('fares'),
    list: () => FARES.map((f) => ({ id: f.id, who: f.who, wrinkle: f.wrinkle, hours: f.hours, way: f.way })),
    next,
    current: () => S.cur,
    // every fare's words alone are enough to arrive: its way names the destination's landmark words (ER-DRIVE-09)
    wayFaults: () => FARES.filter((f) => !f.way || f.way.split(' ').length < 8 || !DESTS[f.to] || !SPOTS[f.spot]).map((f) => f.id),
  },
});
on('fare.pickup', pickup);
// the runner: caught, he pays or is let go; lost, the fare is lost and it is written down
on('foot.chase', async ({ id, st, why }) => {
  const x = X('fares');
  if (why !== 'runner' || !x.runner) return;
  const r = x.runner;
  x.runner = null;
  const P = P_(id);
  if (st === 'caught') {
    const i = await scene(() => choose('', 'He is bent double, getting his breath. "All right. All right."', ['Have the fare off him.', 'Let him go.']));
    logOf('runner').choice = i === 0 ? 'paid' : 'let go';
    if (i === 0) {
      earn(r.pay, false, 'a fare');
      G.money.fares += r.pay;
      G.money.sinceWash += r.pay;
      act('runner_paid', {});
    } else act('runner_let_go', {});
    if (P) P.hold = false;
  } else {
    logOf('runner').choice = 'lost';
    write('A fare ran without paying, and got away. Nothing in the book for that one.', { how: 'Did it' });
  }
});
