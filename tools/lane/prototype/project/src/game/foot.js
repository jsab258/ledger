// LEDGER, the whole game: the system "foot". On foot under watch (A1 to A3, A10, A21, A23, A26; parts 1.1.5 to 1.1.8,
// 1.4.7, 1.4.8, 1.5.2, 2.2.6, 1.3.11): hiding without a stealth mode, walking slowly, street manners, stopping and
// blending in, a thrown stone, vaulting set places, tails, running a man down, trespass by the ground's label, and
// the marks a beating leaves. The rules are pieces/eyes.js; nothing on screen says "hidden".
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on, PLACES } from './core.js';
import { G } from '../state.js';
import { hyp, angDiff, clamp } from '../util.js';
import { act } from '../events.js';
import { choose, scene, bubble } from '../ui.js';
import { goToPoint, send } from '../routines.js';
import { RULES } from '../rules.js';
import { PIECE as EYES } from './pieces/eyes.js';
import { VAULTS, PLACE_LIST } from './tune/way.js';
import { target as aimedAt } from '../fight.js';

const T = RULES.game.foot;
const E = EYES.fns;
const S = { tail: null, chase: null, tres: null, vaultT: 0 };

// ---- being seen (A1): the prototype's clarity, cut by what a man in a street can really do ----
function seen(P, Tg, c, d, e) {
  const t = G.tom,
    x = X('foot');
  if (Tg.inCar || Tg.space !== 'street') return { see: true, c };
  const still = t.still > T.stillAfterRealSeconds && !x.torch;
  if (still && Tg.light <= T.stillInDoorwayLightAtMost) {
    // standing still in shadow is the hiding: a shape at most, and nothing at all from any distance
    if (d > T.stillShapeOnlyBeyondMetres) return { see: d < RULES.seeing.rangeInBlackMetres + T.stillUnseenBeyondShareOfRange * RULES.seeing.rangeAddedByFullLightMetres * Tg.light, c: Math.min(c, T.stillShapeClarityAtMost) };
  }
  // his back to the watcher: no face, the coat still shows
  const toWatcher = Math.atan2(e.x - Tg.x, e.z - Tg.z);
  if (Math.abs(angDiff(t.ang, toWatcher)) > T.backTurnedAboveRadians) c = Math.min(c, T.backTurnedClarityAtMost);
  if (x.scarf) c = Math.min(c, T.scarfClarityAtMost);
  // among people: a group of three or more within 2 m, and a glance takes twice as long
  let near = 0;
  for (const Q of G.named.concat(G.crowd)) if (Q !== P && !Q.gone && Q.space === 'street' && hyp(Q.x, Q.z, Tg.x, Tg.z) < T.amongPeopleWithinMetres) near++;
  if (near >= T.amongPeopleAtLeast) c *= T.amongPeopleClarityTimes;
  return { see: true, c };
}
function target(Tg) {
  const t = G.tom,
    x = X('foot');
  if (x.torch && !t.inCar) Tg.light = Math.max(Tg.light, T.torchLight); // a lit torch lights him like a lamp (A33)
  if (t.slow && !t.inCar && !t.run) Tg.noiseR *= T.slowWalkHalvesFootsteps; // walking slowly halves his footsteps
  if (!t.inCar && marked().bruised) Tg.marked = true; // a face that has been hit is a face people place (A21, ER-MARK-01)
}
export const marked = () => E.marks(dayNow() - X('foot').beatenDay);
export const setTorch = (on_) => (X('foot').torch = !!on_);

// ---- street manners (A10): one key, a short list; each is an act, answered within a second ----
async function manners() {
  const P = aimedAt();
  if (!P) return tell('Nobody near enough.', '');
  const list = ['A nod.', 'Good day.', 'A hard look.', '"Oi!"', 'Ask the way.', 'Never mind.'];
  const i = await scene(() => choose('', 'To ' + (P.anon ? P.def.desc : P.def.name) + ':', list));
  const kinds = ['nod', 'greet', 'hard_look', 'called_out'];
  if (i < 4) {
    const m = E.manner(['nod', 'greeting', 'hard look', 'oi'][i]);
    const Ev = act(kinds[i], P.anon ? { name: P.def.desc } : { target: P.id, noiseR: i === 3 ? T.reachMetres.shout : 0 });
    X('foot').manners.push({ kind: kinds[i], to: P.id, e: Ev.id, t: Math.round(G.t) });
    P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z);
    if (i === 3) {
      P.pauseT = m.stopsSeconds; // stops a walker for about 2 s and turns him round
      emit('foot.oi', P);
    }
    bubble(P, ['A nod back.', P.mind.regard < -0.2 ? 'Is it.' : hourNow() < 12 ? 'Morning.' : hourNow() < 18 ? 'Afternoon.' : 'Evening.', P.def.nerve > 0.6 ? 'Help you?' : '...', 'What?'][i], RULES.game.feel.hintAfterStandingStillRealSeconds);
  } else if (i === 4) {
    const g = G.x.way.goal;
    if (!g) return tell('He has nowhere he is looking for.', '');
    emit('way.ask', { P, place: g.id });
  }
}
// ---- stopping and blending in (A10): sit, lean, smoke: a man who belongs draws no second look ----
function stop() {
  const x = X('foot'),
    t = G.tom;
  if (t.inCar) return false;
  x.belongs = !x.belongs;
  tell(x.belongs ? (t.space !== 'street' ? 'He stands easy by the wall and lights a cigarette, like a man who is meant to be here.' : t.light <= T.stillInDoorwayLightAtMost ? 'He leans in the doorway and lights a cigarette, like a man waiting for somebody.' : 'He sits on the step and lights a cigarette. A man with a reason to be there.') : 'He treads it out and moves on.', '');
  return true;
}
// ---- a thrown stone or a rattled bin (A23): a watcher inside its reach turns to it and remembers a noise ----
function stone() {
  const t = G.tom;
  if (t.inCar || t.space !== 'street') return false;
  const bin = false,
    what = bin ? 'bin' : 'stone',
    ax = t.x + Math.sin(t.ang) * T.reachMetres.stone,
    az = t.z + Math.cos(t.ang) * T.reachMetres.stone;
  const turned = [];
  for (const P of G.named.concat(G.crowd)) {
    if (P.gone || P.space !== 'street' || P.dead) continue;
    const r = E.drawn(hyp(P.x, P.z, ax, az), what, hourNow(), G.weather.rain > RULES.weather.rainingAboveRain);
    if (r.turns) {
      P.alert = { x: ax, z: az, t: r.forSeconds };
      P.ang = Math.atan2(ax - P.x, az - P.z);
      turned.push(P.id);
    }
  }
  act('noise_made', { silent: true });
  X('foot').stones.push({ t: Math.round(G.t), turned });
  tell(turned.length ? 'A stone skitters down the street. A head turns to it.' : 'A stone skitters down the street. Nobody near enough to hear.', '');
  return true;
}
// ---- vaulting (A26): set places only, running ----
function vaultStep(dt) {
  const t = G.tom;
  if (S.vaultT > 0) {
    S.vaultT -= dt;
    return;
  }
  if (t.inCar || t.space !== 'street' || !t.run) return;
  for (const v of VAULTS) {
    for (const [a, b] of [[v.at, v.to], [v.to, v.at]]) {
      if (hyp(t.x, t.z, a[0], a[1]) > T.vaultWithinMetres) continue;
      const toward = Math.abs(angDiff(t.ang, Math.atan2(b[0] - a[0], b[1] - a[1]))) < 1;
      const r = E.vault({ setPlace: true, heightMetres: v.heightMetres, running: t.run });
      if (!toward || !r.vaults) continue;
      t.x = b[0];
      t.z = b[1];
      S.vaultT = r.seconds;
      X('foot').vaults.push({ id: v.id, t: Math.round(G.t) });
      t.noiseP = Math.max(t.noiseP, T.reachMetres.run);
      return;
    }
  }
}
// ---- tails (A2): the target looks back on a rhythm; made only after a doubt; what is learned goes in the Ledger ----
export function startTail(id, learns, o = {}) {
  S.tail = { id, learns, st: { doubt: 0, ended: null }, lookIn: T.targetLooksBackEveryRealSecondsAtLeast, by: o.by || null };
  X('foot').tail = { id, learns };
  return true;
}
function tailEvent(ev) {
  const tl = S.tail;
  if (!tl) return null;
  const before = tl.st.doubt;
  tl.st = E.tail(tl.st, ev);
  const P = P_(tl.id);
  if (tl.st.doubt && !before && P) {
    P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z);
    P.pauseT = 1.5;
    tell(`${P.def.name} looks back, and holds it a moment too long.`, '');
  }
  if (tl.st.ended) {
    const x = X('foot');
    if (tl.st.ended === 'arrived') write(`Followed ${P ? P.def.name : tl.id}: ${tl.st.learned}.`, { key: 'tail:' + tl.id + ':' + Math.round(G.t), who: tl.id, how: 'Saw it himself' });
    else if (tl.st.ended === 'made' && P) {
      act('followed', { target: tl.id, silent: true, told: [tl.id] });
      tell('"You following me?"', P.def.name);
      write(`${P.def.name} made him on the tail.`, { who: tl.id, how: 'Said to his face' });
    }
    x.tails.push({ id: tl.id, ended: tl.st.ended, learned: tl.st.learned || null, doubtFirst: !!tl.st.doubt || tl.st.ended !== 'made', t: Math.round(G.t) });
    emit('foot.tail', { id: tl.id, ended: tl.st.ended, learned: tl.st.learned || null });
    x.tail = null;
    S.tail = null;
  }
  return tl.st;
}
function tailStep(dt) {
  const tl = S.tail;
  if (!tl) return;
  const P = P_(tl.id),
    t = G.tom;
  if (!P || P.gone || P.dead) return;
  tl.lookIn -= dt;
  if (tl.lookIn > 0) return;
  tl.lookIn = T.targetLooksBackEveryRealSecondsAtLeast + (T.targetLooksBackEveryRealSecondsAtMost - T.targetLooksBackEveryRealSecondsAtLeast) * (1 - (P.def.nerve ?? 0.5));
  const d = hyp(P.x, P.z, t.x, t.z);
  const r = E.caught({ metres: d, light: t.light, knowsHim: P.mind.fam > RULES.naming.familiarityAtLeastOnceMet, lineOfSight: G.env.los(P.x, P.z, t.x, t.z) && P.space === t.space, coat: t.coat, still: t.still > 1, inDoorway: t.light <= T.stillInDoorwayLightAtMost, peopleNear: 0, inCar: t.inCar });
  tailEvent({ rung: r.rung });
}
// ---- running a man down (A3): caught by a hand on the collar, lost by 7 s unseen or 70 m, over within 90 s ----
export function startChase(id, o = {}) {
  const P = P_(id);
  if (!P) return false;
  S.chase = { id, seconds: 0, unseen: 0, why: o.why || '' };
  P.override = null;
  P.hold = false;
  P.hurry = 1;
  const away = Math.atan2(P.x - G.tom.x, P.z - G.tom.z);
  goToPoint(P, P.x + Math.sin(away) * T.lostBeyondMetres, P.z + Math.cos(away) * T.lostBeyondMetres, RULES.tom.runningMetresPerSecond * T.runnerSpeedShareOfToms);
  return true;
}
function chaseStep(dt) {
  const c = S.chase;
  if (!c) return;
  const P = P_(c.id),
    t = G.tom;
  c.seconds += dt;
  const d = hyp(P.x, P.z, t.x, t.z),
    los = P.space === t.space && G.env.los(P.x, P.z, t.x, t.z);
  c.unseen = los ? 0 : c.unseen + dt;
  const r = E.chase({ metres: d, unseenSeconds: c.unseen, seconds: c.seconds });
  if (r.st === 'on') {
    if (!P.route) startChaseLeg(P);
    return;
  }
  S.chase = null;
  P.hurry = 0;
  P.route = null;
  X('foot').chases.push({ id: c.id, st: r.st, seconds: Math.round(c.seconds), t: Math.round(G.t) });
  if (r.st === 'caught') {
    P.hold = true;
    act('collared', { target: c.id });
    tell('A hand on his collar. He stops.', '');
  } else {
    send(P, 'home', 'idle', G.t + 120); // he goes home or to a friend, where he can be found later
    tell(`${P.def.name} is gone. He will be somewhere he knows.`, '');
    write(`Lost ${P.def.name} on foot. He will have gone home.`, { who: c.id, how: 'Saw it himself' });
  }
  emit('foot.chase', { id: c.id, st: r.st, why: c.why });
}
function startChaseLeg(P) {
  const away = Math.atan2(P.x - G.tom.x, P.z - G.tom.z);
  goToPoint(P, P.x + Math.sin(away) * T.markAtMetres, P.z + Math.cos(away) * T.markAtMetres, RULES.tom.runningMetresPerSecond * T.runnerSpeedShareOfToms);
}
// ---- ground rules (A10): public, open by hours, private, forbidden; the warnings come in order ----
function trespassStep(dt) {
  const t = G.tom;
  if (t.inCar) return void (S.tres = null);
  const p = PLACE_LIST.find((q) => (q.room ? q.room === t.space : t.space === 'street' && hyp(t.x, t.z, q.x, q.z) < RULES.game.way.reachedWithinMetres) && q.label !== 'public');
  // his own office and the flat over it are his at every hour
  if (!p || p.room === 'mickeys' || p.room === 'flat' || (G.x.crime && G.x.crime.allowed && G.x.crime.allowed[p.id])) return void (S.tres = null);
  const owner = P_(p.owner),
    ownerHere = owner && here(owner, T.shapeAtMetres);
  const r0 = E.trespass(p, hourNow(), 0);
  if (r0.stage === 'free' || !ownerHere) return void (S.tres = null);
  if (!S.tres || S.tres.id !== p.id) S.tres = { id: p.id, seconds: 0, stage: '' };
  S.tres.seconds += dt;
  const r = E.trespass(p, hourNow(), S.tres.seconds);
  if (r.stage === S.tres.stage) return;
  S.tres.stage = r.stage;
  X('foot').warnings.push({ place: p.id, stage: r.stage, t: Math.round(G.t) });
  if (r.stage === 'warns') tell('"We are shut. Out you go."', owner.def.name);
  else if (r.stage === 'warns again') tell('"I will not tell you again."', owner.def.name);
  else {
    act('trespass', { place: p.name, told: [owner.id] }); // the warnings reset; the sighting is kept for good
    tell('"Right. I am fetching somebody."', owner.def.name);
    emit('foot.trespass', { place: p.id, owner: owner.id });
    S.tres = null;
  }
}

register({
  id: 'foot',
  fresh: () => ({ torch: false, scarf: false, belongs: false, beatenDay: -99, manners: [], stones: [], vaults: [], tails: [], chases: [], warnings: [], tail: null }),
  loaded() {
    G.hooks.seen = seen;
    G.hooks.target = target;
    G.hooks.limp = () => (marked().limp ? T.limpRunsAtShare : 1); // a limp for a day: he cannot run as he did
    S.tail = S.chase = S.tres = null;
  },
  step(dt) {
    if (G.paused) return;
    const t = G.tom;
    if (X('foot').belongs && (t.v > 0.2 || t.inCar)) X('foot').belongs = false;
    vaultStep(dt);
    tailStep(dt);
    chaseStep(dt);
    trespassStep(dt);
  },
  key(code) {
    if (G.tom.inCar) return false;
    if (code === 'KeyM') return manners(), true;
    if (code === 'KeyB') return stop();
    if (code === 'KeyO') return stone();
    return false;
  },
  hook: {
    seen: (personId) => {
      const P = P_(personId),
        t = G.tom;
      return E.caught({ metres: hyp(P.x, P.z, t.x, t.z), light: t.light, knowsHim: P.mind.fam > 0.5, coat: t.coat, still: t.still > 1, inDoorway: t.light <= T.stillInDoorwayLightAtMost });
    },
    startTail,
    tailEvent,
    tailState: () => (S.tail ? S.tail.st : null),
    startChase,
    chaseState: () => S.chase,
    marked,
    stone,
    stop,
    vaults: () => VAULTS,
    x: () => X('foot'),
  },
});
on('fight.beaten', () => {
  X('foot').beatenDay = dayNow();
  tell('A split lip, and one eye closing. It will show for three days, and the leg will not run properly before tomorrow.', '', 8);
  write('Beaten. The face will show it for three days: people will place him by it. The leg is bad until tomorrow.', { key: 'marks' + dayNow(), how: 'Felt it' });
}); // bruises and a cut lip for three game days, a limp for one (A21)
