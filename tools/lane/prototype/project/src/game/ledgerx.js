// LEDGER, the whole game: the system "ledgerx", the Ledger's whole-game parts (6.3 the paper map, 2.12.1 the name
// ladder heard, 7.5 the hour budget, 7.6 tense and retellable moments, 7.12's count of new things).
import { register, on, X, PLACES } from './core.js';
import { G, day } from '../state.js';
import { RULES } from '../rules.js';
import { KINDS, NAMES } from '../kinds.js';
import { ui, sub, tomName } from '../ui.js';
import { note, knownNames } from '../ledger.js';
import { townLevel } from '../gossip.js';
import { F } from '../fight.js';
import { hyp } from '../util.js';

const T = () => RULES.game.ledgerx;
const st = () => X('ledgerx');

// ---------- the paper map: only places he has been or been told of (DESIGN 10; ER: no unknown place marked) ----------
// The map's own labels, each with where it is. Core's PLACES join them, so every system's places follow one rule.
export const MAP_LABELS = {
  quaystreet: ['Q U A Y   S T R E E T', 0, -12],
  quay: ['the quay', -70, 48],
  ferry: ['ferry', -55, 72],
  humber: ['T H E   H U M B E R', 20, 84],
  iveson: ["Iveson's yard", -104, 31],
  fishdock: ['fish dock', 89, 74],
  warehouserow: ['warehouse row', 71, 14],
  no4: ['No 4', 119, 31.5],
  school: ['school', -95, -21],
  chapellane: ['Chapel Lane', -45, -18.5],
  backlane: ['back lane', 29.5, 6],
  copperrow: ['C O P P E R   R O W', 0, -168],
  market: ['market', -27, -160],
  bank: ['bank', 15, -139],
  video: ['video', 15, -157],
  markethall: ['market hall', -28, -206],
  station: ['station', 27, -216],
  cut: ['the Cut', 60, -107],
};
export function tell(key) {
  // somebody told him of a place (a job, a fare, a letter, a person asked the way)
  const k = st().known;
  if (k[key] === undefined) k[key] = Math.round(G.t);
}
export const knowsPlace = (key) => st().known[key] !== undefined;
function learnPlaces() {
  const t = G.tom,
    x = t.inCar ? G.car.x : t.x,
    z = t.inCar ? G.car.z : t.z,
    k = st().known,
    r = T().placeKnownWithinMetres;
  if (t.space === 'away') return;
  const before = Object.keys(k).length;
  if (t.space === 'street' || t.inCar) {
    for (const id in MAP_LABELS) if (k[id] === undefined && hyp(x, z, MAP_LABELS[id][1], MAP_LABELS[id][2]) < r * (MAP_LABELS[id][0].includes('   ') ? 2.5 : 1)) k[id] = Math.round(G.t);
    for (const id in PLACES) if (k[id] === undefined && hyp(x, z, PLACES[id].x, PLACES[id].z) < r) k[id] = Math.round(G.t);
  } else if (k['room:' + t.space] === undefined) k['room:' + t.space] = Math.round(G.t);
  if (Object.keys(k).length > before) somethingNew('place');
}

// ---------- the name ladder (ER-RISE-02): each step heard within a game day, and it never goes back ----------
function nameTick() {
  const s = st().name,
    lv = Math.max(s.level, townLevel());
  if (lv > s.level) {
    s.level = lv;
    s.reachedAt[lv] = Math.round(G.t);
  }
  if (s.level <= 1 || s.heardAt[s.level] !== undefined || G.paused || ui.modal || F.on) return;
  // said to his face in passing by somebody who knows who he is: at once if anybody is near, and by the day's end at the latest
  const t = G.tom,
    due = G.t - s.reachedAt[s.level] > T().nameHeardWithinGameHours * 60 - 120;
  let best = null;
  for (const P of G.named || []) {
    if (P.dead || P.gone || P.space !== t.space || P.id === 'sheila' || !knownNames()[P.id]) continue;
    const d = hyp(P.x, P.z, t.x, t.z);
    if (d < T().nameSaidWithinMetres && (!best || d < best.d)) best = { P, d };
  }
  if (!best && !due) return;
  const name = NAMES[s.level];
  s.heardAt[s.level] = Math.round(G.t);
  if (best) sub(`Now then, ${name}.`, tomName(best.P), 'face', 5);
  else sub(`Somebody across the street calls it: "${name}!"`, '', 'over', 5);
  note(`People have started calling him ${name}.`, 'note', 'name' + s.level, { who: best ? best.P.id : undefined, how: 'Said to his face' });
  somethingNew('name');
}
export const nameLevelHeld = () => st().name.level;

// ---------- the hour budget (DESIGN 1; ER-CORE-05, 06): play time booked by activity ----------
// Called once a frame by the main loop, also while a talk or a panel holds the game.
export function budgetTick(dt) {
  if (G.story.phase !== 'play' || !G.x) return;
  const b = st().budget,
    t = G.tom,
    m = ui.modal;
  if (m === 'pause' || m === 'settings' || m === 'how' || m === 'notes' || m === 'credits' || m === 'files' || m === 'playtest') return; // not play
  const k = m === 'talk' || m === 'dialog' ? 'talk' : m === 'ledger' ? 'ledger' : G.fast > 1 || G.pauseWhy === 'passing time' ? 'waiting' : G.paused ? 'watching' : F.on ? 'fight' : t.inCar ? 'driving' : G.story.job && G.story.job.carrying ? 'hands' : (t.still || 0) > 6 ? 'waiting' : 'foot';
  b[k] = (b[k] || 0) + dt;
  b.all = (b.all || 0) + dt;
  b.sinceNew = (b.sinceNew || 0) + dt;
  if (b.sinceNew > (b.longestNothingNew || 0)) b.longestNothingNew = b.sinceNew;
}
// Something new for the player: a place, a person, a kind of deed, a scene, a step up.
export function somethingNew(what) {
  const b = st().budget;
  b.sinceNew = 0;
  b.news = (b.news || 0) + 1;
  st().newLog.push({ t: Math.round(G.t), s: Math.round(b.all || 0), what });
  if (st().newLog.length > 400) st().newLog.splice(0, 100);
}
export function budget() {
  const b = st().budget,
    all = b.all || 0,
    sh = (k) => (all ? Math.round(((b[k] || 0) / all) * 1000) / 1000 : 0);
  const shares = { foot: sh('foot'), driving: sh('driving'), talk: sh('talk'), hands: sh('hands'), fight: sh('fight'), ledger: sh('ledger'), waiting: sh('waiting'), watching: sh('watching') };
  return {
    realSecondsPlayed: Math.round(all),
    shares,
    newThings: b.news || 0,
    longestNothingNewRealSeconds: Math.round(b.longestNothingNew || 0),
    talkUnder30: shares.talk < T().talkShareAtMost,
    waitingUnder10: shares.waiting < T().waitingShareAtMost,
    neverFiveMinutesWithNothingNew: (b.longestNothingNew || 0) <= T().nothingNewAtMostRealSeconds,
  };
}
// ---------- tension (DESIGN 3; ER-TENS-01, 02): counted from what happened, for the playtester ----------
// A tense moment: a deed somebody saw or heard, a crime, a challenge, a fight, a choice put to him. A retellable one:
// he chose, a named person was part of it, and it came back later (somebody said it to his face).
export function tension() {
  const src = {},
    add = (k) => (src[k] = (src[k] || 0) + 1);
  let retell = 0;
  for (const E of G.events) {
    const k = KINDS[E.kind];
    if (!k || k.noself) continue;
    const seen = E.wit && E.wit.length;
    if (k.crime >= 2) add('odds');
    else if (/police|search|arrest|challenge/.test(E.kind)) add('law');
    else if (/pickup|drop|parcel|carry|bag/.test(E.kind)) add('load');
    else if (k.loud && seen) add('ears');
    else if (seen) add('eyes');
    else if (/job_|debt_|choice_|sitdown|collision|tea/.test(E.kind)) add('choice');
    const named = (E.wit || []).concat(E.party || []).some((id) => G.people[id] && !G.people[id].anon);
    const back = (G.named || []).some((P) => P.mind && P.mind.by && P.mind.by[E.id] && P.mind.by[E.id].said);
    if (named && back && (seen || E.party)) retell++;
  }
  const total = Object.values(src).reduce((a, b) => a + b, 0),
    half = (st().budget.all || 0) / T().tenseWindowRealSeconds || 1;
  const top = Math.max(0, ...Object.values(src));
  return { tenseMoments: total, sources: src, perHalfHour: Math.round((total / Math.max(half, 0.2)) * 10) / 10, kindsOfSource: Object.keys(src).length, largestShare: total ? Math.round((top / total) * 100) / 100 : 0, retellable: retell };
}

register({
  id: 'ledgerx',
  fresh: () => ({ known: { quaystreet: 0, ferry: 0, quay: 0, humber: 0 }, name: { level: 1, reachedAt: {}, heardAt: {} }, budget: {}, newLog: [], met: 0, kinds: {} }),
  loaded(s) {
    if (!s.known) s.known = {};
    if (!s.budget) s.budget = {};
    if (!s.newLog) s.newLog = [];
    if (!s.kinds) s.kinds = {};
    G.hooks.knowsPlace = knowsPlace;
    G.hooks.tellPlace = tell;
    G.hooks.budget = budget;
    G.hooks.tension = tension;
    G.hooks.mapLabels = () => MAP_LABELS;
  },
  minute(t) {
    learnPlaces();
    const s = st();
    const met = Object.keys(G.ledger.met || {}).length;
    if (met > s.met) {
      s.met = met;
      somethingNew('person');
    }
    for (let i = G.events.length - 1; i >= 0 && i > G.events.length - 6; i--) {
      const k = G.events[i].kind;
      if (!s.kinds[k]) {
        s.kinds[k] = 1;
        somethingNew('deed:' + k);
      }
    }
    if (t % 5 === 0) nameTick();
  },
  hook: {
    read: () => JSON.parse(JSON.stringify(st())),
    known: () => Object.keys(st().known),
    tell: (k) => tell(k),
    budget: () => budget(),
    tension: () => tension(),
    setLevel(n) {
      const s = st().name;
      s.level = n;
      s.reachedAt[n] = Math.round(G.t);
      return s;
    },
    name: () => JSON.parse(JSON.stringify(st().name)),
    labels: () => MAP_LABELS,
  },
});
on('act', () => somethingNew('act'));
on('acts:beat', () => somethingNew('beat'));
on('job:step', () => somethingNew('job'));
on('rise:rung', () => somethingNew('rung'));
void day;
