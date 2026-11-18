// LEDGER. The state of one week: everything the save file holds, the settings, and the pause book.
import { RULES } from './rules.js';
const WEATHER = RULES.weather;

// The one mutable game state. Everything the save file holds lives under G.
export const VERSION = 4;
export const START_T = RULES.time.weekStartsGameMinute; // Monday 3.36pm, off the bus
export const SECS_PER_HOUR = RULES.time.realSecondsPerGameHour; // real seconds per game hour at normal speed

export function freshState() {
  return {
    v: VERSION,
    t: START_T, // game minutes since Monday 00:00 (15 Oct 1990)
    played: 0, // real seconds played
    weather: {
      kind: 'drizzle',
      rain: WEATHER.startsRain,
      mist: WEATHER.startsMist,
      wet: WEATHER.startsWet,
      next: START_T + WEATHER.firstChangeAfterGameMinutes,
    },
    tom: {
      x: -5.4,
      z: 21,
      y: 0.12,
      ang: 0,
      space: 'street',
      v: 0,
      run: false,
      coat: false,
      hasCoat: false,
      inCar: false,
      carry: 'suitcase',
      hurt: 0,
      weapon: null,
      armed: false,
      items: {},
      noiseP: 0,
      light: 1,
      zone: 'Quay Street',
      still: 0,
    },
    car: { x: 4.1, z: 37.4, ang: 0, v: 0, lights: false, keys: false, dmg: 0 },
    minds: {}, // personId -> mind (persisted part of each person)
    events: [],
    ev: {},
    sightIdx: {},
    transfers: [],
    nextE: 1,
    ledger: { acts: [], notes: [], calls: {}, met: {} },
    log: [],
    money: {
      clean: RULES.money.startsWithPocketPence,
      dirty: 0,
      fares: 0,
      fareCount: 0,
      washed: 0,
      sinceWash: 0,
      booksOff: 0,
      earnedClean: 0,
      earnedDirty: 0,
      spent: 0,
    },
    debts: {
      dennis: { owed: RULES.prices.owedByIvesonPence, st: 'open' },
      lee: { owed: RULES.prices.owedByLeePence, st: 'open' },
      darren: { owed: RULES.prices.owedByDarrenPence, st: 'open' },
      julie: { owed: RULES.prices.owedByJuliePence, st: 'open' },
      wayne: { owed: RULES.prices.owedByWaynePence, st: 'open' },
    },
    story: {
      phase: 'title',
      flags: {},
      job: null,
      fare: null,
      police: null,
      ellis: null,
      choice: null,
      ended: false,
      talkNotice: false,
      lastSleepDay: -1,
      objective: '',
    },
    stats: { talks: 0, live: 0, fallback: 0, comebacks: 0, fights: 0, seenTicks: 0 },
    measures: null, // the Ledger screen test: see measures.js
  };
}

// Runtime container. Non-persisted fields (people objects, env hooks, hud lists) hang off here too.
export const G = Object.assign(freshState(), {
  people: {},
  named: [],
  crowd: [],
  env: { los: () => true, lightAt: () => 1, zone: () => 'Quay Street', camYaw: () => 0 },
  watch: [],
  paused: false,
  fast: 1,
  hooks: {},
  settings: {
    quality: 'high',
    autoRes: true,
    healthBar: false,
    vol: 0.8,
    music: 0.6,
    sens: 1,
    invertY: false,
    touch: false,
    hints: true,
    bloom: true,
    liveTalk: true,
    asks: true, // the playtest's find-the-fact asks
    truthView: true, // the end screen's truth beside the Ledger (a playtest view)
    slipOpen: false, // the slip beside a talk starts folded; F2 unfolds it and the choice is remembered
    ledgerPart: 'people', // the Ledger opens on the part last used
  },
});

export function resetState() {
  const f = freshState();
  for (const k of Object.keys(f)) G[k] = f[k];
  TALLY.days = [];
}

// ---------- the gossip table ----------
// Counts for LEDGER.gossip(): per day, how often someone saw Tom do a thing, how often he was only heard, and
// which named people stood within talking distance of each other. Counting only: nothing reads these back,
// no random number is drawn for them, and they are kept while the page is open, not saved with the week.
export const TALLY = { days: [] };
export function tally(what, pair) {
  const d = Math.floor(G.t / 1440),
    row = TALLY.days[d] || (TALLY.days[d] = { sightings: 0, heard: 0, met: {} });
  if (what === 'met') row.met[pair] = (row.met[pair] || 0) + 1;
  else row[what]++;
}
export const day = () => Math.floor(G.t / 1440);
export const hour = () => (G.t % 1440) / 60;

// ---------- pausing ----------
// The game is paused and resumed in one place, and every pause and every resume is written down with the game
// time and its reason. A pause that never ends can then be found: see LEDGER.pauses() and LEDGER.check.nights().
export const PAUSE = { log: [], busy: 0, faults: 0, since: 0, stillHeld: () => false };
export function setPaused(on, reason) {
  on = !!on;
  if (G.paused === on) {
    if (on) G.pauseWhy = reason; // a second reason for the same pause: the latest one is the one that must end it
    return;
  }
  G.paused = on;
  G.pauseWhy = on ? reason : null;
  PAUSE.since = typeof performance !== 'undefined' ? performance.now() : 0;
  PAUSE.log.push({
    paused: on,
    reason,
    gameMinute: Math.round(G.t * 10) / 10,
    dayIndex: day(),
    hour: Math.round(hour() * 100) / 100,
    realSecondsPlayed: Math.round(G.played * 10) / 10,
    atRealMs: Math.round(PAUSE.since),
  });
  if (PAUSE.log.length > 500) PAUSE.log.splice(0, 100);
}
// A stretch of code that holds the game paused while it works (sleep, custody, a fade). Whatever happens inside,
// the pause ends: an error can no longer leave the game stopped.
export async function pausedWhile(reason, fn) {
  setPaused(true, reason);
  PAUSE.busy++;
  try {
    return await fn();
  } finally {
    PAUSE.busy--;
    setPaused(PAUSE.stillHeld(), reason + ': done');
  }
}
