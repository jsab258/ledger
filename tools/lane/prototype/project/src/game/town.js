// LEDGER, the whole game: the system "town". The bridge from this prototype to the game's real town code.
//
// The town's rules are not written here. They are the game's own C++ town code (ue-probe/Source/LedgerProbe/Public),
// compiled for the browser as one-sim.wasm and reached through tools/lane/one-sim/wasm/one-sim-bridge.mjs. This file
// only carries things across: the clock in, each hour's doings out, what he does and who saw it in, and who knows
// what back into the prototype's own minds, so the Ledger, the come-backs and the name ladder go on working.
// What changes for the player is written in production/lane/ONE-SHOT-SIM-DIFFERENCES.md.
import { register, emit, FAULTS } from './core.js';
import { G } from '../state.js';
import { KINDS } from '../kinds.js';
import { RULES } from '../rules.js';
import { clamp, hyp, angDiff } from '../util.js';
import { remember, logLine, act } from '../events.js';
import { nightF, knowsWho } from '../seeing.js';
import {
  openTownNow,
  openTownFromOldSaveNow,
  PROTOTYPE_ACTS,
  CAST_TO_PROTOTYPE,
  NightAnswer,
  WeekAnswer,
} from '../../onesim/one-sim-bridge.mjs';
import { CAST_JSON } from '../../onesim/cast.mjs';
import { mindOfRung, rungOfMind, offenceOf, faceToward, hostLoyalty } from './pieces/witness_mind.js';
import { shown, hasMark } from './pieces/giveaways.js';

const TUNE = RULES.game.town;
const MEM = RULES.memory,
  GOS = RULES.gossip;

// What is not saved: the compiled simulation, the open town, and what went wrong.
const T = {
  module: null, // one-sim.wasm, compiled once when the page starts
  failed: null, // why the simulation could not be loaded, in plain words
  town: null, // the open town (the bridge's object), or null: the prototype's own rules are running
  ticking: false,
  queue: [], // things he did while an hour was being handled: told once it has been
  refusals: [], // calls the bridge refused, with its reason (a fault of this file: tests assert none)
  lastRead: -1,
  lastAsks: null,
  hours: 0,
  said: false,
};
const x = () => (G.x && G.x.town) || null;
const proto = (castId) => (CAST_TO_PROTOTYPE[castId] ? CAST_TO_PROTOTYPE[castId] : G.people[castId] ? castId : null);
const refuse = (what, e) => {
  const line = what + ': ' + ((e && e.message) || e);
  if (T.refusals.length < 200) T.refusals.push(line);
  logLine('The town did not take ' + line, 'town');
};

// ---------- loading the simulation file, once, when the page starts ----------
function fetchModule() {
  if (typeof fetch !== 'function' || typeof WebAssembly !== 'object' || typeof window === 'undefined') {
    T.failed = 'this is not a page';
    return;
  }
  fetch('one-sim.wasm')
    .then((r) => {
      if (!r.ok) throw new Error('one-sim.wasm is not beside the page (' + r.status + ')');
      return r.arrayBuffer();
    })
    .then((b) => WebAssembly.compile(b))
    .then((m) => {
      const have = WebAssembly.Module.exports(m).map((e) => e.name);
      for (const need of ['os_id_rung', 'os_witness_open', 'os_would_report_as'])
        if (!have.includes(need)) throw new Error('one-sim.wasm is an older build without ' + need);
      T.module = m;
    })
    .catch((e) => {
      T.failed = String((e && e.message) || e);
    });
}
fetchModule();

// ---------- where things are, in the cast file's words ----------
export function areaAtPoint(px, pz, space) {
  if (space && TUNE.areaOfRoom[space]) return TUNE.areaOfRoom[space];
  let best = 'mickeys',
    bd = 1e9;
  for (const id in TUNE.areaAt) {
    const d = hyp(px, pz, TUNE.areaAt[id][0], TUNE.areaAt[id][1]);
    if (d < bd) {
      bd = d;
      best = id;
    }
  }
  return best;
}
function tomArea() {
  const t = G.tom;
  return areaAtPoint(t.inCar ? G.car.x : t.x, t.inCar ? G.car.z : t.z, t.inCar ? null : t.space);
}
const areaOfEvent = (E) => areaAtPoint(E.x, E.z, null);
const factOf = (E) => 'p_' + E.kind + '_e' + E.id;
// the story name back to the prototype's event: "player.p_strike_e12", "player.strike_e12" (a save from before the
// swap), "player.p_window_e7h" (the same deed, seen by people the cast file lacks)
function eventOfTopic(topic) {
  const m = /^player\.(?:p_)?[A-Za-z0-9_]+?_e(\d+)h?$/.exec(topic);
  return m ? G.ev[+m[1]] || null : null;
}
// what the town is told of a kind: 'deed' (a thing damaged), 'crime' (the police file has a name for it), 'saw'
// (a sighting of his hidden life), 'open' (an open, decent act), or null (nothing)
function tellOf(kindId) {
  const k = KINDS[kindId];
  if (!k) return null;
  let tell;
  if (k.town !== undefined) tell = k.town;
  else {
    const a = PROTOTYPE_ACTS[kindId];
    tell = a && (a.tell === 'saw' || a.tell === 'open') ? a.tell : null;
  }
  if (tell === null) return null;
  const off = offenceOf(kindId, k, TUNE);
  if (tell === 'deed' || (off === 1 && tell !== 'open')) return 'deed';
  if (off >= 2 && tell !== 'open') return 'crime';
  return tell;
}
export const townLive = () => !!T.town;
export const townCovers = (id) => !!T.town && T.town.covers(id);

// ---------- how well a witness sees him: the real rule ----------
// Returns { who, face, sure, rung } for a witness P who has him in view at d metres (the prototype's own geometry
// has already said that he is in view), or null when the real town is not running.
export function townIdentify(P, d, Tt) {
  if (!T.town) return null;
  const t = G.tom;
  const tx = Tt.x,
    tz = Tt.z;
  const eyeX = P.space === 'home' && P.win ? P.win.x : P.x,
    eyeZ = P.space === 'home' && P.win ? P.win.z : P.z;
  const off = angDiff(t.inCar ? G.car.ang : t.ang, Math.atan2(eyeX - tx, eyeZ - tz));
  const night = nightF();
  const toward = faceToward(
    { offRadians: off, inCar: !!Tt.inCar, metres: d, light: Tt.light, coat: !!Tt.coat, night },
    TUNE,
  );
  const fx = G.x || {};
  const list = shown({
    run: t.run && !t.inCar,
    coat: !!Tt.coat,
    blood: !!(t.blood || (fx.foot && fx.foot.blood)),
    dirt: !!t.dirt,
    armed: !!t.armed,
    wrongClothes: !!t.wrongClothes,
    marks: !!(t.marks || (fx.foot && fx.foot.marks && fx.foot.marks.length)),
    inCar: !!Tt.inCar,
    carry: t.carry === 'bag',
  });
  // How well this witness knows the figure in front of them is the host's to say. The real rule recognises a man by
  // more than his face, so the two things that hide who he is are given as a lower familiarity: the runner's coat
  // with its collar up after dark, and sitting in the cab (the prototype's own numbers, kept).
  const SEE = RULES.seeing;
  let fam = clamp(P.mind.fam, 0, 1);
  if (Tt.coat && night > SEE.coatHidesWhenNightAbove) fam *= SEE.coatAtNightFaceTimes;
  if (Tt.inCar)
    fam *= d < SEE.inCabCloseMetres && Tt.light > SEE.inCabLitAboveLight ? SEE.inCabCloseAndLitFaceTimes : SEE.inCabOtherwiseFaceTimes;
  const rung = T.town.rung(d, clamp(Tt.light, 0, 1), clamp(fam, 0, 1), hasMark(list), toward);
  const m = mindOfRung(rung, { knowsWho: knowsWho(P), inCar: !!Tt.inCar, coat: !!Tt.coat }, TUNE);
  m.shows = list;
  return m;
}

// ---------- opening the town ----------
function open() {
  const s = x();
  T.town = null;
  T.queue = [];
  T.lastRead = -1;
  if (!s) return;
  s.live = false;
  if (!T.module) {
    s.why = T.failed || 'the simulation file is still loading';
    return;
  }
  try {
    if (s.saved) {
      T.town = openTownNow({ module: T.module, castJson: CAST_JSON, saved: s.saved });
      if (T.town.now() > Math.floor(G.t)) throw new Error('the saved town is ahead of the saved clock');
      s.why = 'a saved town';
    } else if (G.events.some((E) => E.kind !== 'inherit' && E.kind !== 'arrive') && !s.opened) {
      // a save from before the swap: a fresh town at its clock, told what its people saw with their own eyes
      const r = openTownFromOldSaveNow({
        module: T.module,
        castJson: CAST_JSON,
        old: { t: G.t, minds: G.minds, events: G.events },
        areaOf: areaOfEvent,
        wordsOf: (E) => (KINDS[E.kind] ? KINDS[E.kind].truth(E) : 'he was seen'),
      });
      T.town = r.town;
      s.old = { fed: r.fed.length, dropped: r.dropped.length, lost: r.lost };
      s.why = 'a save from before the real town: a fresh town at its clock';
      logLine(
        `A week saved before the real town: ${r.fed.length} things its people saw were told to the new town, ${r.dropped.length} could not be. ` +
          r.lost.join('. '),
        'town',
      );
    } else {
      T.town = openTownNow({ module: T.module, castJson: CAST_JSON, startMinute: G.t });
      s.why = 'a new town';
    }
  } catch (e) {
    // a town that cannot be opened from its save is opened afresh at the clock, and the log says so
    const why = String((e && e.message) || e);
    try {
      T.town = openTownNow({ module: T.module, castJson: CAST_JSON, startMinute: G.t });
      s.why = 'a fresh town at the clock: ' + why;
      logLine('The saved town could not be read (' + why + '). A fresh town starts at this hour.', 'town');
    } catch (e2) {
      T.town = null;
      s.why = String((e2 && e2.message) || e2);
    }
  }
  s.live = !!T.town;
  s.opened = s.opened || (T.town ? Math.floor(G.t) : 0);
  s.saved = null; // the open town is the truth now; it is written into the save when the game saves
  if (T.town && !T.said) {
    T.said = true;
    logLine("The town's own rules are running: " + T.town.people().length + ' people, ' + s.why + '.', 'town');
  }
}
function saidFailure() {
  const s = x();
  if (!s || s.saidFail || !T.failed) return;
  s.saidFail = 1;
  s.why = T.failed;
  logLine(
    "The town's own rules could not be loaded (" + T.failed + "). The street runs on this prototype's own rules.",
    'town',
  );
}

// ---------- the save ----------
// Called by saving.js before the week is written: the town travels in the save as one plain object.
export function townSave() {
  const s = x();
  if (!s) return;
  if (T.town) {
    try {
      s.saved = T.town.save();
    } catch (e) {
      refuse('a save', e);
    }
  }
}
// After the week has been written the open town stays the truth.
export function townSaved() {
  const s = x();
  if (s && T.town) s.saved = null;
}

// ---------- every simulation step: the clock in, the hours out ----------
export function townTick() {
  if (G.story.phase !== 'play' && G.story.phase !== 'end') return;
  const s = x();
  if (!s) return;
  if (!T.town) {
    if (T.module && !s.live && !s.gaveUp) {
      open();
      if (!T.town) s.gaveUp = 1;
    } else if (T.failed) saidFailure();
    if (!T.town) return;
  }
  if (T.ticking) return; // a clock skip started from inside an hour's handling: the outer call finishes first
  T.ticking = true;
  let hours = [];
  try {
    hours = T.town.tick(G.t, tomArea());
  } catch (e) {
    refuse('the clock', e);
    T.ticking = false;
    T.town = null;
    s.saved = null;
    s.opened = 0;
    s.gaveUp = 0;
    open(); // the town is opened afresh at the clock rather than left wrong
    return;
  }
  for (const h of hours) onHour(h);
  T.ticking = false;
  while (T.queue.length) T.queue.shift()();
  const m = Math.floor(G.t);
  if (m - T.lastRead >= TUNE.mindsReadFromTownEveryGameMinutes || hours.length) {
    T.lastRead = m;
    quietTheFrightened();
    readMinds();
  }
}
const inTurn = (fn) => {
  if (T.ticking) T.queue.push(fn);
  else fn();
};

// ---------- what each hour did ----------
function onHour(h) {
  const s = x();
  T.hours++;
  T.lastAsks = h.asks;
  s.last = { day: h.day, hour: h.hour, stories: h.stories, ellisFirst: h.ellisFirst, takenFirst: h.takenFirst };
  const st = G.story,
    deed = s.deed ? G.ev[s.deed] : null;
  // who came by and found the damage: they hold the aftermath only, never him (A38)
  for (const f of h.found) {
    const id = proto(f.who);
    s.found = s.found || [];
    s.found.push({ who: f.who, t: f.atMinute });
    if (!id || !deed) continue;
    const P = G.people[id];
    if (P && !P.mind.by[deed.id]) {
      remember(P, deed, { src: 'found', who: 'man', sure: TUNE.finderSure, heat: TUNE.finderHeat });
      logLine(`${P.def.name} came by and found it: ${KINDS[deed.kind].truth(deed)}`, 'town');
    }
  }
  // who went to the police this morning (the week's deed, and the crimes that are no damage to it)
  const went = h.went.map((who) => ({ who, E: deed })).concat(
    (h.crimeWent || []).map((w) => ({ who: w.who, E: eventOfTopic(w.topic), statement: w.statement })),
  );
  for (const w of went) {
    const id = proto(w.who) || w.who,
      P = G.people[id];
    s.went = s.went || [];
    s.went.push({ who: id, e: w.E ? w.E.id : null, day: h.day });
    if (w.E) {
      w.E.stmt = w.E.stmt || [];
      if (!w.E.stmt.includes(id)) w.E.stmt.push(id);
    }
    if (P) P.mind.stmtGiven = 1;
    logLine(
      `${P ? P.def.name : 'Somebody (' + w.who + ')'} went to the police` +
        (w.E ? ': ' + KINDS[w.E.kind].truth(w.E) : ''),
      'police',
    );
    emit('police:reported', { E: w.E, by: id, town: true });
  }
  // DS Ellis on the street, asking: the real rule's reason. The prototype's own detective walks it.
  if (h.ellis) {
    s.ellis = s.ellis || [];
    s.ellis.push({ day: h.day, why: h.ellis });
    st.flags.forceEllis = 1;
    st.ellisDays = st.ellisDays || {};
    st.ellisDays[h.day] = 0;
    logLine('DS Ellis is asking on the street. The reason: ' + h.ellis, 'police');
  }
  // a constable for him at ten: the prototype's own constable walks down and the arrest plays as it does
  if (h.taken) {
    const E = h.takenFor ? eventOfTopic(h.takenFor) : deed;
    s.taken = s.taken || [];
    s.taken.push({ day: h.day, end: h.taken, e: E ? E.id : null, until: h.heldUntil });
    if (!st.arrest)
      st.arrest = {
        e: E ? E.id : null,
        violent: !!(E && KINDS[E.kind].crime >= RULES.police.violentFromCrimeLevel),
        due: G.t,
        by: E && E.stmt ? E.stmt.slice() : [],
        town: { end: h.taken, until: h.heldUntil, hours: h.heldUntil ? Math.round((h.heldUntil - h.minute) / 60) : null },
      };
    logLine('A constable has come for him. It will end: ' + h.taken, 'police');
  }
  if (h.invite) {
    s.invite = h.day;
    logLine("By the town's own week, Ada asks him in for tea today.", 'town');
  }
  if (h.ron) {
    s.ron = h.day;
    logLine("By the town's own week, Ron has the envelope tonight.", 'town');
  }
  emit('town:hour', h);
}

// A witness of a crime who is frightened or bought before nine does not go (DESIGN 2: reaching the witness first).
function quietTheFrightened() {
  if (!T.town) return;
  for (const c of T.town.crimes()) {
    for (const w of c.witnesses) {
      if (w.never || Number.isInteger(w.went)) continue;
      const P = G.people[proto(w.id) || w.id];
      if (!P) continue;
      if (P.mind.fear >= TUNE.noReportIfFearAtLeast || P.mind.bought || P.mind.quiet || P.dead) {
        if (T.town.quiet(c.topic.replace(/^player\./, ''), w.id)) logLine(`${P.def.name} will not go to the police.`, 'town');
      }
    }
  }
}

// ---------- who knows what: from the town into the prototype's own minds ----------
// The people the cast file has hold what the town says they hold. A story the town has passed to one of them
// becomes a memory in their mind here, so they can say it to his face, the Ledger can learn of it, and the street's
// name for him climbs, all by the code that did those things before.
const OWN = { outfit: ['job_yes', 'job_no', 'no_show'], taken: ['arrested'], police: ['ellis_asked'] };
function ownEvent(topic) {
  // the town's own stories of a day (an ask answered, an arrest seen, the detective asking), by the prototype's event
  const m = /^player\.(outfit|taken|police)_d(\d+)/.exec(topic);
  if (!m) return null;
  const kinds = OWN[m[1]],
    d = +m[2];
  for (let i = G.events.length - 1; i >= 0; i--) {
    const E = G.events[i],
      ed = Math.floor((E.t - 6 * 60) / 1440); // a deed before six is the night before's
    if (kinds.includes(E.kind) && (ed === d || Math.floor(E.t / 1440) === d)) return E;
  }
  return null;
}
function readMinds() {
  if (!T.town) return;
  let facts;
  try {
    facts = T.town.knows();
  } catch (e) {
    return refuse('reading who knows what', e);
  }
  const s = x();
  s.heldByTown = facts.length;
  for (const f of facts) {
    const id = proto(f.who);
    if (!id) continue;
    const P = G.people[id];
    if (!P || P.dead) continue;
    const E = eventOfTopic(f.topic) || ownEvent(f.topic);
    if (!E || P.mind.by[E.id]) continue;
    const k = KINDS[E.kind];
    if (!k) continue;
    const from = f.saw ? null : proto(f.from) || 'someone';
    const m = mindOfRung(f.rung < 0 ? 4 : f.rung, { knowsWho: knowsWho(P), inCar: !!E.car, coat: !!E.coat }, TUNE);
    remember(P, E, {
      src: f.saw ? 'saw' : 'told',
      from,
      who: f.names && knowsWho(P) ? 'tom' : m.who,
      sure: clamp(Number.isFinite(f.sure) ? f.sure : m.sure, 0.05, 1),
      heat: clamp(k.sev + MEM.heatAddedToSeverity, 0, 1) * Math.pow(GOS.toldHeatTimes, f.hops),
      hop: f.hops,
      face: m.face,
      rung: f.rung,
      town: 1,
    });
    if (!f.saw) {
      G.transfers.push({ a: from, b: id, e: E.id, t: Math.round(G.t), z: 'the town', town: 1, hops: f.hops });
      logLine(`${P.def.name} has heard, ${f.hops} telling${f.hops === 1 ? '' : 's'} from ${from === 'someone' ? 'somebody who saw it' : G.people[from].def.name}: ${k.truth(E)}`, 'told');
    }
  }
}

// ---------- what he does: told to the town ----------
// One person newly holds something first-hand (they saw it, or were part of it). Called by events.js remember().
export function townSaw(P, E, r) {
  if (!T.town || E._acting || r.town || P.anon) return;
  const tell = tellOf(E.kind);
  if (tell !== 'saw' && tell !== 'open') return;
  if (!T.town.covers(P.id)) return; // somebody the cast file lacks: the prototype's own talk carries it
  const what = {
    minute: G.t,
    who: P.id,
    rung: rungOfMind(r),
    fact: factOf(E),
    area: areaOfEvent(E),
    words: KINDS[E.kind].truth(E),
    certainty: clamp(r.sure, 0.05, 1),
  };
  inTurn(() => {
    try {
      if (tell === 'open') T.town.sawOpen(what);
      else T.town.saw(what);
    } catch (e) {
      refuse('a sighting (' + E.kind + ')', e);
    }
  });
}
// A discrete act of his is over and its witnesses are known. Called by events.js act().
export function townAct(E) {
  if (!T.town) return;
  const tell = tellOf(E.kind),
    k = KINDS[E.kind];
  if (OWN_KINDS.includes(E.kind) || E.kind.startsWith('choice_')) answerOwn(E);
  if (!tell) return;
  const ids = [...new Set([...(E.wit || []), ...(E.party || [])])];
  const wits = [];
  for (const id of ids) {
    const P = G.people[id];
    if (!P || P.anon) continue;
    const r = P.mind.by[E.id];
    if (!r || (r.src !== 'saw' && r.src !== 'self')) continue;
    wits.push({ P, r, cast: T.town.covers(id) });
  }
  const area = areaOfEvent(E),
    words = k.truth(E),
    fact = factOf(E),
    s = x();
  if (tell === 'saw' || tell === 'open') {
    for (const w of wits) townSaw(w.P, E, w.r);
    return;
  }
  const off = tell === 'deed' ? 1 : offenceOf(E.kind, k, TUNE);
  const asWitness = (w) =>
    w.cast
      ? { id: w.P.id, rung: rungOfMind(w.r), victim: w.P.id === E.target, sure: clamp(w.r.sure, 0.05, 1), never: !!w.P.def.nostmt }
      : {
          id: w.P.id,
          rung: rungOfMind(w.r),
          victim: w.P.id === E.target,
          nerve: w.P.def.nerve == null ? TUNE.nerveIfNotSet : w.P.def.nerve,
          loyalty: hostLoyalty(w.P.mind.regard || 0, TUNE),
          never: !!w.P.def.nostmt,
        };
  inTurn(() => {
    try {
      if (tell === 'deed' && !T.town.deedHeld()) {
        // the week's one deed: the real rules follow it (who finds it, who goes to the police, the constable)
        T.town.deed({
          minute: G.t,
          area,
          thing: k.thing || E.thing || 'the ' + E.kind.replace(/_/g, ' '),
          said: words,
          fact,
          words,
          witnesses: wits.filter((w) => w.cast).map((w) => ({ id: w.P.id, rung: rungOfMind(w.r) })),
          certainty: 1,
        });
        s.deed = E.id;
        const host = wits.filter((w) => !w.cast);
        if (host.length)
          T.town.crime({ minute: G.t, area, offence: 1, fact: fact + 'h', words, witnesses: host.map(asWitness) });
      } else if (wits.length) {
        T.town.crime({ minute: G.t, area, offence: off, fact, words, witnesses: wits.map(asWitness) });
      }
      s.told = (s.told || 0) + 1;
    } catch (e) {
      refuse('a deed (' + E.kind + ')', e);
    }
  });
}
// The acts the town makes its own story of: his answer to a night's ask, the tea, the week's end.
const OWN_KINDS = ['job_yes', 'job_no', 'no_show', 'drop', 'tea', 'tea_late'];
// A story that starts with other people (events.js seed): only the town's own kinds are passed on from here.
export function townOwn(E) {
  if (T.town && (OWN_KINDS.includes(E.kind) || E.kind.startsWith('choice_'))) answerOwn(E);
}
function answerOwn(E) {
  const s = x();
  const a = T.lastAsks;
  inTurn(() => {
    try {
      if (E.kind === 'job_yes' || E.kind === 'job_no' || E.kind === 'no_show') {
        const night = a && Number.isInteger(a.nextNight) ? a.nextNight : Math.floor((G.t - 360) / 1440);
        const what = E.kind === 'job_no' ? NightAnswer.Refused : E.kind === 'no_show' ? NightAnswer.NoShow : null;
        if (what !== null && night >= 0) s.asked = T.town.answerAsk(night, what, G.t) ? night : s.asked;
        else if (E.kind === 'job_yes') s.agreed = night; // the envelope handed over is told when it is (the drop)
      } else if (E.kind === 'drop' && Number.isInteger(s.agreed)) {
        if (T.town.answerAsk(s.agreed, NightAnswer.Did, G.t)) s.asked = s.agreed;
        s.agreed = null;
      } else if (E.kind === 'tea' || E.kind === 'tea_late') T.town.teaMinute(G.t);
      else if (E.kind.startsWith('choice_')) {
        const ans = E.kind === 'choice_wind' ? WeekAnswer.WindDown : E.kind === 'choice_take' ? WeekAnswer.TakeOver : WeekAnswer.WontSay;
        if (T.town.weekAsksNow(G.t, true) && T.town.weekAsk(G.t)) s.weekGiven = T.town.weekGive(ans, G.t);
        else s.weekGiven = false; // the town's own week asks on its last day: an answer before it is the prototype's alone
      }
    } catch (e) {
      refuse('his answer (' + E.kind + ')', e);
    }
  });
}

// ---------- where the town's routine puts somebody (the table of places) ----------
export function townPlace(id, minute = G.t) {
  if (!T.town || !T.town.covers(id)) return null;
  const place = T.town.placeOf(id, minute);
  return { place, spot: TUNE.spotOfPlace[place] || (place === 'off' ? 'off' : null) };
}

// ---------- every reaction prints its chain (ER-EYES-05: no all-knowing town) ----------
// How this person came to hold this event: a list of steps back to somebody who saw it, heard it or was part of it.
export function chainOf(personId, eventId, seen = {}) {
  const P = G.people[personId],
    E = G.ev[eventId];
  if (!P || !E) return [{ who: personId, how: 'unknown' }];
  const m = P.mind.by[eventId];
  if (!m) return [{ who: personId, how: 'holds nothing of it' }];
  const step = { who: personId, how: m.src, as: m.who, rung: rungOfMind(m), t: Math.round(m.t) };
  if (m.src !== 'told') return [step];
  step.from = m.from;
  if (m.town) {
    step.tellings = m.hop;
    return [step, { who: m.from, how: 'saw', rung: m.rung, note: "first witness, by the town's own talk" }];
  }
  if (!m.from || m.from === 'someone' || seen[m.from]) return [step, { who: m.from || 'someone', how: 'a passer-by who saw it' }];
  seen[personId] = 1;
  return [step].concat(chainOf(m.from, eventId, seen));
}
const rooted = (chain) => {
  const last = chain[chain.length - 1];
  return ['saw', 'self', 'heard', 'found', 'a passer-by who saw it'].includes(last.how);
};
// Every reaction so far by a neighbour or the police, each with its chain: a remark to his face, a statement, DS
// Ellis's visit, an arrest. ok is false for a reaction that traces to nobody.
export function reactions() {
  const out = [],
    s = x() || {};
  for (const P of G.named)
    for (const m of P.mind.mem)
      if (m.said) {
        const chain = chainOf(P.id, m.e);
        out.push({ kind: 'said to his face', who: P.id, e: m.e, chain, ok: rooted(chain) });
      }
  for (const w of s.went || []) {
    const chain = w.e ? chainOf(w.who, w.e) : [];
    out.push({ kind: 'went to the police', who: w.who, e: w.e, chain, ok: !w.e || !G.people[w.who] || rooted(chain) });
  }
  for (const v of s.ellis || []) out.push({ kind: 'DS Ellis came', why: v.why, day: v.day, chain: [{ how: "the town's police file and talk", why: v.why }], ok: !!v.why });
  for (const a of s.taken || []) {
    const E = a.e ? G.ev[a.e] : null,
      by = E && E.stmt ? E.stmt : [];
    out.push({ kind: 'a constable came', e: a.e, by, chain: by.flatMap((id) => (G.people[id] ? chainOf(id, a.e) : [{ who: id, how: 'saw' }])), ok: by.length > 0 || !E });
  }
  return out;
}

register({
  id: 'town',
  fresh: () => ({ live: false, why: '', saved: null, opened: 0, deed: null, told: 0 }),
  loaded() {
    T.said = false;
    open();
  },
  hook: {
    live: () => !!T.town,
    why: () => (x() ? x().why : ''),
    ready: () => !!T.module,
    failed: () => T.failed,
    refusals: T.refusals,
    faults: FAULTS,
    hours: () => T.hours,
    people: () => (T.town ? T.town.people() : []),
    covers: (id) => townCovers(id),
    knows: () => (T.town ? T.town.knows() : []),
    state: () => (T.town ? T.town.state() : null),
    crimes: () => (T.town ? T.town.crimes() : []),
    deed: () => (T.town ? T.town.deedHeld() : null),
    held: () => (T.town ? T.town.held() : null),
    area: tomArea,
    areaAt: areaAtPoint,
    place: townPlace,
    temper: (id) => (T.town ? T.town.temper(id) : null),
    rung: (metres, light, fam, mark, face) => (T.town ? T.town.rung(metres, light, fam, mark, face) : null),
    wouldReportAs: (nerve, loyalty, offence, victim) => (T.town ? T.town.sim.wouldReportAs(nerve, loyalty, offence, victim) : null),
    audible: (loud, ambient) => (T.town ? T.town.sim.audibleRadius(loud, ambient, false) : null),
    save: () => (T.town ? T.town.save() : null),
    act: (kind, o) => act(kind, o || {}).id, // for a test: he does a thing, here and now
    chain: chainOf,
    reactions,
    tellOf,
    read: readMinds,
    reopen: open,
    // for a test: run as if the simulation file could not be loaded
    drop() {
      T.town = null;
      if (x()) {
        x().live = false;
        x().gaveUp = 1;
      }
    },
  },
});
