// LEDGER, the whole game (the one-shot of 20 Nov 2026). The core every system plugs into.
//
// A system is one file under src/game/ that calls register({ id, ... }) once, when it is imported from
// game/index.js. Its saved state lives under G.x[id] and nowhere else. A system may give any of:
//   fresh()            the system's saved state for a new game (plain data only: it goes into the save)
//   loaded(x)          after a new game or a loaded save, with its own state (bring an older shape up to date here)
//   step(dt)           every simulation step, dt in real seconds at normal speed (already multiplied when time is passed)
//   minute(t)          once each new game minute (t: whole game minutes since Monday 00:00)
//   hourly(h, d)       once each new game hour (h 0..23, d the day index, Monday of week one is 0)
//   daily(d)           once at each midnight
//   hotspots(out)      on foot: push prompts { k: 'E', t: 'Words', run } for what is in reach
//   carPrompts(out)    at the wheel: the same
//   beatFor(P)         a written scene waiting with this person, or null (the first system to answer wins)
//   matters(P, a)      push what is open between Tom and this person onto a (the talk's decisions, as scenes.js mattersFor)
//   key(code)          a key press nobody else took: return true if it was this system's
//   hook               an object of test calls, shown as LEDGER.game.<id>
// Systems speak to each other only through on() and emit(), or through each other's exported functions.
import { G } from '../state.js';
import { advanceTo } from '../work.js';
import { act } from '../events.js';
import { note } from '../ledger.js';
import { pay } from '../money.js';
import { sub, ui } from '../ui.js';
import { F } from '../fight.js';
import { hyp } from '../util.js';

export const SYSTEMS = [];
export const FAULTS = []; // a fault inside one system never stops the game; every one is kept here, and tests assert none
const LISTEN = {};
const MINUTES_A_TEST_STEP = 20; // a test's skip of time gives the systems their minutes as it goes
let lastMin = -1;

export function register(sys) {
  if (SYSTEMS.some((s) => s.id === sys.id)) throw new Error('two systems called ' + sys.id);
  SYSTEMS.push(sys);
  return sys;
}
export function on(name, fn) {
  (LISTEN[name] || (LISTEN[name] = [])).push(fn);
}
export function emit(name, payload) {
  for (const fn of LISTEN[name] || []) guard('on ' + name, () => fn(payload));
}
function guard(what, fn) {
  try {
    return fn();
  } catch (e) {
    const line = what + ': ' + ((e && e.stack) || e);
    if (FAULTS.length < 200) FAULTS.push(line);
    console.error('GAME FAULT ' + line);
    return undefined;
  }
}
// The saved state of the whole game. An older save (before the one-shot) has none: it gets a fresh one and loads.
export function ensureX() {
  if (!G.x) G.x = { v: 1 };
  for (const s of SYSTEMS) if (s.fresh && G.x[s.id] === undefined) G.x[s.id] = s.fresh();
  return G.x;
}
export const X = (id) => ensureX()[id];
const each = (name, ...a) => {
  for (const s of SYSTEMS) if (s[name]) guard(s.id + '.' + name, () => s[name](...a));
};
// ---- a spoken line is not said twice (the consequence checker's rule: five words or more, never again) ----
// A line of five words or more is said once in a week. When every long line of a list has been said, a short one
// of the list is used (a short greeting may come again, as it does in a street). The said lines are saved.
const wordsIn = (l) => (String(l).match(/[A-Za-z']+/g) || []).length;
export function freshLine(list, fallback) {
  const x = ensureX();
  const said = (x.feel.said = x.feel.said || {});
  const lines = Array.isArray(list) ? list : [list];
  const unused = lines.filter((l) => wordsIn(l) < SAID_ONCE_FROM_WORDS || !said[l]);
  const long = unused.filter((l) => wordsIn(l) >= SAID_ONCE_FROM_WORDS);
  // a fresh long line first, most of the time; else any line still allowed; else the fallback (a short one)
  const from = long.length && Math.random() < SAID_LONG_SHARE ? long : unused;
  const l = from.length ? from[Math.floor(Math.random() * from.length)] : fallback || '';
  if (l && wordsIn(l) >= SAID_ONCE_FROM_WORDS) said[l] = 1;
  return l;
}
const SAID_ONCE_FROM_WORDS = 5,
  SAID_LONG_SHARE = 0.6;
// After a new game starts or a save is loaded.
export function gameLoaded() {
  ensureX();
  lastMin = Math.floor(G.t);
  G.hooks.emit = emit;
  G.hooks.modal = () => ui.modal;
  G.hooks.pay = (pence, why) => pay(pence, false, why);
  G.hooks.fighting = () => F.on; // the older files tell the systems of a thing through this (a beating, a fare's steps)
  for (const s of SYSTEMS) if (s.loaded) guard(s.id + '.loaded', () => s.loaded(G.x[s.id]));
  emit('loaded');
}
export function gameStep(dt) {
  ensureX();
  each('step', dt);
  const m = Math.floor(G.t);
  if (lastMin < 0 || m < lastMin) lastMin = m;
  let n = 0;
  // every minute is given once, also across a skip of time (capped: a skip of days gives its hours and days, and the
  // minutes of its last two hours)
  if (m - lastMin > 180) {
    for (let t = lastMin + 1; t <= m - 120; t++) {
      if (t % 60 === 0) each('hourly', Math.floor((t % 1440) / 60), Math.floor(t / 1440));
      if (t % 1440 === 0) each('daily', Math.floor(t / 1440));
    }
    lastMin = m - 120;
  }
  while (lastMin < m && n++ < 400) {
    lastMin++;
    each('minute', lastMin);
    if (lastMin % 60 === 0) each('hourly', Math.floor((lastMin % 1440) / 60), Math.floor(lastMin / 1440));
    if (lastMin % 1440 === 0) each('daily', Math.floor(lastMin / 1440));
  }
}
export function gameHotspots(out) {
  each('hotspots', out);
  return out;
}
export function gameCarPrompts(out) {
  each('carPrompts', out);
  return out;
}
export function gameBeatFor(P) {
  for (const s of SYSTEMS)
    if (s.beatFor) {
      const b = guard(s.id + '.beatFor', () => s.beatFor(P));
      if (b) return b;
    }
  return null;
}
export function gameMatters(P, a) {
  each('matters', P, a);
  return a;
}
export function gameKey(code) {
  for (const s of SYSTEMS) if (s.key && guard(s.id + '.key', () => s.key(code))) return true;
  return false;
}
export function gameHook() {
  const o = {
    faults: FAULTS,
    systems: () => SYSTEMS.map((s) => s.id),
    x: () => ensureX(),
    emit,
    places: PLACES,
    // test calls every system's tests share
    test: {
      act: (kind, o = {}) => act(kind, o), // he does a thing now, where he stands, seen by whoever can see it
      // game minutes pass: with Tom out of the way (as a sleep or the cells), or where he stands
      pass(minutes, hidden = true) {
        const end = G.t + minutes;
        while (G.t < end) {
          advanceTo(Math.min(end, G.t + MINUTES_A_TEST_STEP), hidden);
          gameStep(0);
        }
        return G.t;
      },
    },
  };
  for (const s of SYSTEMS) if (s.hook) o[s.id] = s.hook;
  return o;
}

// ---------- places ----------
// Every place a job, a fare, a letter or a person names (DESIGN-ADDENDUM A9, A10): an address, a landmark and a
// ground label. label: 'public' | 'hours' (open by hours, private out of them) | 'private' | 'forbidden'.
export const PLACES = {};
export function addPlace(p) {
  // { id, name, x, z, address, landmark, label, openFromHour?, openUntilHour?, owner?, room? }
  if (!p.id || !p.name || !p.address || !p.landmark || !p.label) throw new Error('a place needs id, name, address, landmark and label: ' + JSON.stringify(p));
  PLACES[p.id] = p;
  return p;
}

// ---------- small things every system uses ----------
export const hourNow = () => (G.t % 1440) / 60;
export const dayNow = () => Math.floor(G.t / 1440);
export const P_ = (id) => G.people[id];
// A line in Tom's Ledger: only what he saw, heard or was told. o: { kind, key (written once), who, how, ev }
export const write = (text, o = {}) => note(text, o.kind || 'note', o.key, { who: o.who, how: o.how, ev: o.ev });
// Words on screen, low: what somebody says, or what he notices.
export const tell = (text, who = '', secs) => sub(text, who, who ? '' : 'over', secs);
export const tomXZ = () => (G.tom.inCar ? [G.car.x, G.car.z] : [G.tom.x, G.tom.z]);
export const tomNear = (x, z, r) => G.tom.space === 'street' && hyp(tomXZ()[0], tomXZ()[1], x, z) <= r;
// Is this person here with him, awake and able to answer?
export const here = (P, r) => !!P && !P.dead && !P.gone && P.awake !== false && P.space === G.tom.space && hyp(P.x, P.z, G.tom.x, G.tom.z) <= r;
