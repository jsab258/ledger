// LEDGER, the whole game: the system "town". THE BRIDGE TO THE GAME'S REAL TOWN CODE (way A, his decision):
// the game's own C++ town rules, compiled for the browser (tools/lane/one-sim), run inside this page. This file
// holds no town rule. It hands the town the clock each step, tells it what he was seen doing, and hands back
// what each hour did. What changed for the player is in production/lane/ONE-SHOT-SIM-DIFFERENCES.md.
//
//   every step        town.tick(G.t, area): the hours that began come back and are given out as 'town.hour'
//   a sighting        seeing.js witness() -> G.hooks.sighted: one call a witness, at the rung his memory supports
//   damage            the week's one deed (the first act of a kind marked damage), with everyone who saw it
//   what people know  the nine people of both casts are told by the real town's talk, never by gossip.js
//   the police        who went to the police over the damage, DS Ellis's mornings, the arrest and its hours
//   the save          the town travels in the save as G.x.town.saved; a save from before it opens a fresh town
import { register, emit, on } from './core.js';
import { G } from '../state.js';
import { clamp } from '../util.js';
import { KINDS } from '../kinds.js';
import { remember, logLine } from '../events.js';
import { RULES } from '../rules.js';
import { AREA_OF_ROOM, AREA_OF_ZONE } from './tune/town.js';
import wasmBytes from './sim/one-sim.wasm';
import castJson from './sim/hook-cast.txt';
import { openTown, openTownFromOldSave, PROTOTYPE_TO_CAST, CAST_TO_PROTOTYPE, PROTOTYPE_ACTS, NightAnswer, WeekAnswer } from './sim/one-sim-bridge.mjs';

const T = RULES.game.town;
const S = { town: null, opening: null, queue: [], fault: null, gen: 0, lost: null, hours: 0 };
const X = () => G.x.town;

export const townReady = () => S.opening || Promise.resolve(!!S.town);
export const townOpen = () => !!S.town;
export const inRealCast = (id) => !!PROTOTYPE_TO_CAST[id];
export { NightAnswer, WeekAnswer };

// Where he stands, as an area of the cast file.
export function areaNow(x, z, space) {
  const t = G.tom;
  space = space || t.space;
  if (AREA_OF_ROOM[space]) return AREA_OF_ROOM[space];
  x = x === undefined ? (t.inCar ? G.car.x : t.x) : x;
  z = z === undefined ? (t.inCar ? G.car.z : t.z) : z;
  const zone = G.env.zone(x, z);
  if (AREA_OF_ZONE[zone]) return AREA_OF_ZONE[zone];
  if (z > T.quayStreetMickeysAboveZMetres) return 'mickeys';
  if (z > T.quayStreetBusStopAboveZMetres) return 'bus_stop';
  if (z > T.quayStreetNewsagentAboveZMetres) return 'newsagent';
  if (z > T.quayStreetRitasAboveZMetres) return 'ritas';
  return 'chapel';
}
const rungOf = (m) =>
  m.who === 'tom' || m.who === 'owner' ? T.rungRecognised : m.who === 'coat' || m.who === 'cab' ? T.rungMark : (m.face || 0) > T.faceRungAboveFaceScore ? T.rungFace : T.rungSilhouette;
const factOf = (E) => E.kind + '_e' + E.id;
const wordsOf = (E) => KINDS[E.kind].truth(E);

function open(gen, make) {
  S.town = null;
  S.fault = null;
  S.opening = make()
    .then((r) => {
      if (gen !== S.gen) return false;
      S.town = r.town || r;
      if (r.lost) S.lost = r.lost; // a save from before the town: what the player loses, in plain lines
      for (const h of r.hours || []) hour(h);
      const q = S.queue;
      S.queue = [];
      for (const fn of q) run(fn);
      return true;
    })
    .catch((e) => {
      S.fault = String((e && e.message) || e);
      console.error('GAME FAULT town: ' + S.fault);
      return false;
    });
  return S.opening;
}
// Everything told to the town goes through here: before the town is open it waits its turn; a refusal is kept and shown.
function run(fn) {
  if (!S.town) return void S.queue.push(fn);
  try {
    sync();
    return fn(S.town);
  } catch (e) {
    X().refused.push(String((e && e.message) || e).slice(0, 200));
    if (X().refused.length > 40) X().refused.shift();
    return undefined;
  }
}
function sync() {
  if (!S.town || G.t < S.town.now()) return;
  const hours = S.town.tick(G.t, areaNow());
  for (const h of hours) hour(h);
}
// One hour of the real town, as the game's own hour gives it.
function hour(h) {
  const x = X();
  S.hours++;
  for (const f of h.found) x.found.push({ who: CAST_TO_PROTOTYPE[f.who] || f.who, t: f.atMinute });
  for (const w of h.went) {
    x.went.push({ who: CAST_TO_PROTOTYPE[w] || w, t: h.minute });
    logLine((CAST_TO_PROTOTYPE[w] || w) + ' went to the police about the damage', 'police');
  }
  if (h.ellis) x.ellis = { why: h.ellis, t: h.minute, shown: false };
  if (h.taken) x.taken = { how: h.taken, t: h.minute, until: h.heldUntil, shown: false };
  x.asks = h.asks;
  x.tea = h.tea;
  x.stories = h.stories;
  x.last = { day: h.day, hour: h.hour, ellisFirst: h.ellisFirst, takenFirst: h.takenFirst };
  emit('town.hour', h);
  told();
}
// What the real town's talk has passed to the people of both casts becomes their memory here: a telling, from whom,
// how many tellings from the one who saw it. gossip.js no longer passes anything between two people of the real cast.
function told() {
  if (!S.town) return;
  const x = X();
  for (const k of S.town.knows()) {
    const m = /^player\.([a-z0-9_]+)_e(\d+)$/.exec(k.topic);
    const id = CAST_TO_PROTOTYPE[k.who];
    if (!m || !id || k.saw) continue;
    const P = G.people[id],
      E = G.ev[+m[2]];
    if (!P || !E || P.mind.by[E.id]) continue;
    const from = CAST_TO_PROTOTYPE[k.from] || null;
    remember(P, E, {
      src: 'told',
      from,
      who: k.names ? 'tom' : 'man',
      sure: clamp(k.sure, 0, 1),
      heat: clamp(KINDS[E.kind].sev * T.toldHeatShareOfSeverity + T.toldHeatAdded, 0, 1),
      hop: k.hops,
    });
    x.chains.push({ who: id, e: E.id, from: k.from, hops: k.hops, t: Math.round(G.t) });
    if (x.chains.length > 400) x.chains.shift();
  }
}
// A witness saw him: told to the town once a witness and event, and again only if he was then seen better.
function sighted(P, E, r) {
  const how = (PROTOTYPE_ACTS[E.kind] || KINDS[E.kind].town || {}).tell || (KINDS[E.kind].damage ? 'deed' : KINDS[E.kind].val < 0 ? 'saw' : 'open');
  if (how !== 'saw' || !inRealCast(P.id) || r.src !== 'saw') return;
  const x = X(),
    key = E.id + ':' + P.id,
    rung = rungOf(r);
  if (x.fed[key] >= rung) return;
  x.fed[key] = rung;
  const what = { minute: G.t, who: P.id, rung, fact: factOf(E), area: areaNow(E.x, E.z, 'street'), words: wordsOf(E), certainty: clamp(r.sure, T.certaintyAtLeast, 1) };
  run((town) => town.saw(what));
}
// An act is over: if it damaged a thing, it is the week's deed (the first), with everyone who saw it done.
function acted(E) {
  const k = KINDS[E.kind];
  if (!k.damage) return;
  const x = X();
  // a passer-by of the crowd is nobody of the cast: the town is told only of people it can name (they are dropped by the bridge too)
  const wit = (E.wit || []).filter((id) => G.people[id] && !G.people[id].anon).map((id) => ({ id, rung: rungOf(G.people[id].mind.by[E.id] || { who: 'man' }) }));
  const what = { minute: G.t, area: areaNow(E.x, E.z, 'street'), thing: E.thing || 'a window', said: (E.thing || 'a window') + ' was damaged', witnesses: wit, fact: factOf(E), words: wordsOf(E) };
  run((town) => {
    if (town.deedHeld()) {
      // the real week follows one deed: a further piece of damage becomes talk, one telling a witness
      for (const w of wit) if (inRealCast(w.id)) town.saw({ minute: G.t, who: w.id, rung: w.rung, fact: what.fact, area: what.area, words: what.words });
      x.deeds.push({ e: E.id, deed: false });
    } else {
      const r = town.deed(what);
      x.deeds.push({ e: E.id, deed: true, taken: r.taken.map((w) => w.id), dropped: r.dropped.map((w) => w.id) });
    }
  });
}

register({
  id: 'town',
  fresh: () => ({ saved: null, fed: {}, found: [], went: [], ellis: null, taken: null, asks: null, tea: null, stories: 0, last: null, deeds: [], chains: [], refused: [], answered: {} }),
  loaded(x) {
    const gen = ++S.gen;
    S.queue = [];
    S.lost = null;
    G.hooks.sighted = sighted;
    G.hooks.acted = (E) => emit('act', E); // every system may hear of an act: on('act', fn)
    G.hooks.townPair = (A, B) => inRealCast(A.id) && inRealCast(B.id); // gossip.js leaves these to the real town
    G.hooks.townEllis = () => (S.town || S.opening ? !!(x.ellis && !x.ellis.shown && G.t - x.ellis.t < T.ellisComesWithinGameHoursOfTheTownSayingSo * 60) : null);
    G.hooks.townEllisShown = () => x.ellis && (x.ellis.shown = true);
    G.hooks.beforeSave = () => {
      if (S.town && gen === S.gen) {
        sync();
        x.saved = S.town.save();
      }
    };
    const wasm = wasmBytes;
    if (x.saved) open(gen, () => openTown({ wasm, castJson, saved: x.saved }));
    else if (G.events.length > 1 && G.t > RULES.time.weekStartsGameMinute + 1)
      // a save from before the town was the real one: a fresh town at its clock, told what its people saw with their own eyes
      open(gen, () =>
        openTownFromOldSave({ wasm, castJson, old: { t: G.t, minds: G.minds, events: G.events }, areaOf: (E) => areaNow(E.x, E.z, 'street'), wordsOf: (E) => (KINDS[E.kind] ? wordsOf(E) : 'he was seen') }),
      );
    else open(gen, () => openTown({ wasm, castJson, startMinute: Math.floor(G.t) }));
  },
  step() {
    if (S.town) sync();
  },
  hook: {
    ready: () => townReady(),
    open: () => !!S.town,
    fault: () => S.fault,
    lost: () => S.lost,
    hoursRun: () => S.hours,
    knows: () => (S.town ? S.town.knows() : []),
    state: () => (S.town ? S.town.state() : null),
    now: () => (S.town ? S.town.now() : null),
    areaNow: () => areaNow(),
    placeOf: (id, minute) => (S.town ? S.town.placeOf(id, minute) : null),
    deedHeld: () => (S.town ? S.town.deedHeld() : null),
    x: () => X(),
    // ER-EYES-05: the chain of sightings and tellings by which somebody holds a story, back to the one who saw it
    chain(personId, eventId) {
      const out = [];
      let id = personId;
      for (let i = 0; i < 12 && id; i++) {
        const P = G.people[id],
          m = P && P.mind.by[eventId];
        if (!m) break;
        out.push({ who: id, how: m.src, from: m.from || null });
        if (m.src !== 'told') break;
        id = m.from;
      }
      return out;
    },
  },
});

// His answers reach the town's own week (the asks, the tea, the week's end), so its own stories of them are right.
export function townAnswerAsk(askDay, answer) {
  const x = X();
  if (x.answered['ask' + askDay]) return;
  x.answered['ask' + askDay] = answer;
  run((town) => town.answerAsk(askDay, answer, G.t));
}
export function townTeaMinute() {
  run((town) => town.teaMinute(G.t));
}
export function townWeekGive(answer) {
  run((town) => {
    if (town.weekAsksNow(G.t) && town.weekAsk(G.t)) town.weekGive(answer, G.t);
  });
}
on('act', acted);
