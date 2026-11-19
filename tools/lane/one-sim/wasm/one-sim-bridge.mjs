// ONE SIMULATION IN THE BROWSER: the plain bridge for the prototype (step 3a, 19 November 2026).
//
// The prototype keeps its own clock (game minutes since Monday 00:00), its own street, its own
// money, debts, jobs, fights and talk. This module is the one place where that clock meets the
// town: the game's own town rules, compiled for the browser (one-sim.wasm, loaded by one-sim.mjs).
// BRIDGE.md says in plain words what the prototype calls and what it reads back.
//
//   import { openTown } from './one-sim-bridge.mjs';
//   const town = await openTown({ wasm, castJson, startMinute: G.t });           // a new week
//   const town = await openTown({ wasm, castJson, saved: G.town });              // a saved week
//   for (const hour of town.tick(G.t, area)) { ... }                             // every simulation step
//   G.town = town.save();                                                        // whenever the prototype saves
//
// NO TOWN RULE LIVES HERE. The bridge only turns the prototype's minutes into the calls the
// packaged game makes (CrimeProbe.cpp ClockHours and its clock tick), in the same order:
//   for each whole hour the clock has crossed: the talk of the hour before, up to its last minute;
//   then the hour's scheduled steps (TownWeek::RunHour); and after them the talk up to now.
// It remembers two things the game also keeps outside the town (CrimeProbe.cpp ConstableHour):
// that he is held, and until when.
import { loadOneSim, NightAnswer, WeekAnswer, Offence } from './one-sim.mjs';

export { NightAnswer, WeekAnswer, Offence };

/// The version of the saved object below. A save from a later version is refused.
export const BRIDGE_SAVE_VERSION = 1;

/// The prototype's ids for the people who are in both casts, and the real cast's ids for them
/// (production/specs/hook-cast.json). Six carry the same full name on both sides; June, Rita and
/// Hal carry a surname only in the prototype (June Suddaby, Rita Welburn, Hal Metcalfe). The
/// other people of the prototype have no certain match: DIFFERENCES.md lists them.
export const PROTOTYPE_TO_CAST = Object.freeze({
  sheila: 'lena', ron: 'rocco', darren: 'sam', alison: 'noor', walsh: 'emil', ada: 'ada', june: 'june', rita: 'rita', hal: 'hal',
});
export const CAST_TO_PROTOTYPE = Object.freeze(Object.fromEntries(Object.entries(PROTOTYPE_TO_CAST).map(([p, c]) => [c, p])));

/// How well a witness saw the man, as the town counts it (Rumor::OriginRung, Sighting.h).
export const Rung = Object.freeze({ Someone: 0, Silhouette: 1, Mark: 2, Face: 3, Recognised: 4 });

/// The thirteen answers of one game hour, by name. The same thirteen, in the same order and
/// words, as the C# Core's TownWeekHour golden rows (one_sim.cpp os_hour).
export const HOUR_FIELDS = Object.freeze(['found', 'went', 'ellis', 'taken', 'invite', 'ron', 'tea', 'held', 'asks', 'outfit', 'stories', 'ellisFirst', 'takenFirst']);

const MIN_PER_DAY = 1440;
const unEsc = (s) => s.replace(/~/g, ' ').replace(/\^/g, '\n').replace(/!/g, '|');   // the golden table's escaping, undone
// A mark of the cast file's text (FNV-1a, 32 bits): a save made with one cast is not loaded into another.
function castMark(text) {
  let h = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  return h.toString(16).padStart(8, '0');
}
const clockOf = (minute) => {
  const m = Math.floor(minute), day = Math.floor(m / MIN_PER_DAY), rest = m - day * MIN_PER_DAY;
  return [day, Math.floor(rest / 60), rest % 60];
};

/// One hour's raw row (thirteen fields joined by '|') as an object the prototype can read.
export function readHour(row, day, hour) {
  const f = row.split('|');
  if (f.length !== HOUR_FIELDS.length) throw new Error(`one-sim bridge: an hour came back with ${f.length} fields, not ${HOUR_FIELDS.length}`);
  const list = (s) => (s === '-' ? [] : s.split(','));
  const asks = unEsc(f[8]).split(';');   // next night; the nights answered so far; "stands" or why it ended
  return {
    day, hour, minute: day * MIN_PER_DAY + hour * 60, row,
    found: list(f[0]).map((x) => { const at = x.lastIndexOf('@'); return { who: x.slice(0, at), atMinute: Number(x.slice(at + 1)) }; }),   // who came by and found the damage
    went: list(f[1]),                           // who went to the police this morning
    ellis: f[2] === '-' ? null : f[2],          // why DS Ellis came, or null: she did not
    taken: f[3] === '-' ? null : f[3],          // how his arrest will end (Cautioned, Charged, BailedToReturn), or null: nobody came for him
    invite: f[4] === '1',                       // Ada asked him in for tea
    ron: f[5] === '1',                          // Ron brought the envelope
    tea: f[6],                                  // the tea's state, in the rules' own word
    held: f[7] === '1',                         // he is in the cells this hour
    asks: {
      nextNight: Number(asks[0]),
      nights: Object.fromEntries((asks[1] || '').split(',').filter(Boolean).map((kv) => kv.split('='))),
      ended: asks[2] === 'stands' ? null : asks[2],
    },
    outfit: list(f[9]),                         // what the outfit's man holds about him
    stories: Number(f[10]),                     // how many stories the town holds, everyone's counted
    ellisFirst: unEsc(f[11]),                   // "never", or "day N, for <why>"
    takenFirst: unEsc(f[12]),                   // "no", or "day N, <how it ended>"
  };
}

/// Opens the town. One of: a new week (startMinute, the prototype's clock at the start), or a
/// saved one (saved, what save() returned). `wasm` is the bytes of one-sim.wasm or a compiled
/// module; `castJson` the cast file's text. `talk` is 'by the minute' (the packaged game's way,
/// the default) or 'by the hour' (the reference week's way: the town's talk runs only as each
/// hour ends and before something he does; the tests use it to hold the bridge to the C# rows).
export async function openTown({ wasm, castJson, startMinute = 0, saved = null, talk = 'by the minute', print } = {}) {
  if (typeof castJson !== 'string' || !castJson) throw new Error('one-sim bridge: no cast file text was given');
  if (talk !== 'by the minute' && talk !== 'by the hour') throw new Error(`one-sim bridge: talk is 'by the minute' or 'by the hour', not ${JSON.stringify(talk)}`);
  const sim = await loadOneSim(wasm, print ? { print } : undefined);
  const mark = castMark(castJson);
  let at, nextHour, held = null;

  if (saved) {
    // Everything is checked before anything is loaded: a save this build cannot read changes nothing.
    if (typeof saved !== 'object' || saved.kind !== 'one-sim town') throw new Error('one-sim bridge: this is not a saved town');
    if (!(saved.v >= 1) || saved.v > BRIDGE_SAVE_VERSION) throw new Error(`one-sim bridge: the saved town is version ${saved.v}, this build reads ${BRIDGE_SAVE_VERSION}`);
    if (saved.cast !== mark) throw new Error('one-sim bridge: the saved town was made with another cast file');
    const t = saved.texts;
    if (!t || typeof t.agents !== 'string' || typeof t.town !== 'string' || typeof t.week !== 'string' || !t.memories || typeof t.memories !== 'object'
        || !Number.isFinite(saved.at) || !Number.isInteger(saved.nextHour) || saved.at < 0) throw new Error('one-sim bridge: the saved town is not whole');
    let week;
    try { week = JSON.parse(t.week); } catch (e) { throw new Error('one-sim bridge: the saved town is not whole'); }
    sim.newTown(castJson);
    sim.loadAgents(t.agents);
    for (const person of sim.people()) if (typeof t.memories[person] === 'string') sim.loadMemory(person, t.memories[person]);
    sim.loadTown(t.town);
    sim.loadWeek(week);
    talk = saved.talk === 'by the hour' ? 'by the hour' : 'by the minute';
    at = saved.at;
    nextHour = saved.nextHour;
    const until = sim.heldUntil(...clockOf(at));
    if (until >= 0) held = { until };
  } else {
    if (!Number.isFinite(startMinute) || startMinute < 0) throw new Error('one-sim bridge: the week starts at a minute from Monday 00:00, zero or later');
    sim.newTown(castJson);
    at = Math.floor(startMinute);
    nextHour = Math.ceil(startMinute / 60);       // an hour that begins exactly at the start is the first one run
    sim.age(...clockOf(at));                      // the town's talk aged to the start, as a week's first hour does
  }

  // Before something he does that the town is told of: the talk up to the minute before, as the
  // reference week runs it. The clock must have been ticked to that minute first, so that an hour
  // that has begun has had its steps before he acts in it.
  const before = (minute) => {
    if (!Number.isFinite(minute) || minute < 0) throw new Error('one-sim bridge: he does things at a minute from Monday 00:00, zero or later');
    const m = Math.floor(minute);
    if (m < at) throw new Error(`one-sim bridge: that minute (${m}) is before the town's clock (${at})`);
    if (Math.floor(m / 60) >= nextHour) throw new Error(`one-sim bridge: tick the clock to minute ${m} before he acts at it`);
    if (m >= 1) sim.roundsTo(...clockOf(m - 1));
    at = m;
    return clockOf(m);
  };
  // "Held" is the game's to keep, not the town's: taken from each hour's own answer, with the release time asked of the custody.
  const noteHeld = (event) => {
    if (!event.held) { held = null; return; }
    const until = sim.heldUntil(event.day, event.hour, 0);
    held = { until: until >= 0 ? until : event.minute + 60 };
  };

  const town = {
    sim,                                           // the loader's own object, for anything not wrapped here
    talk: () => talk,
    now: () => at,
    /// He is in the cells: { until: the minute he is let out }, or null. Kept here, as the game keeps it.
    held: () => (held ? { ...held } : null),

    /// EVERY SIMULATION STEP: the prototype's clock now (game minutes since Monday 00:00, fractions
    /// welcome) and the area he stands in (for ten o'clock's constable). Returns the hours that
    /// began since the last call, oldest first, each as readHour gives it; most calls return none.
    tick(nowMinute, area = 'mickeys') {
      if (!Number.isFinite(nowMinute)) throw new Error('one-sim bridge: the clock is not a number');
      const now = Math.floor(nowMinute);
      if (now < at) throw new Error(`one-sim bridge: the clock went back (${now} after ${at}); open the town again from its save`);
      const hours = [];
      for (; nextHour * 60 <= now; nextHour++) {
        const day = Math.floor(nextHour / 24), hod = nextHour - day * 24;
        if (talk === 'by the minute' && nextHour * 60 >= 1) sim.roundsTo(...clockOf(nextHour * 60 - 1));   // the hour before's talk first
        const event = readHour(sim.hour(day, hod, area), day, hod);
        noteHeld(event);
        event.heldUntil = held ? held.until : null;
        hours.push(event);
      }
      if (now > at) {
        if (talk === 'by the minute') sim.roundsTo(...clockOf(now));   // the town's talk as its minutes pass
        at = now;
        if (held && now >= held.until) held = null;
      }
      return hours;
    },

    // ---- reading the town ----
    people: () => sim.people(),
    /// Where the town's routine puts someone at a minute: a place id of the cast file. Takes the
    /// prototype's id or the cast's.
    placeOf(person, minute = at) { const [day, hour] = clockOf(minute); return sim.placeOf(PROTOTYPE_TO_CAST[person] ?? person, day, hour); },
    /// The Ledger's facts: who knows what, and how (saw it or was told, from whom, how well the first witness saw him).
    knows: () => sim.knows(),
    /// The week's pieces as the game's save writes them: asks, police, tea, damage, arrests, hours, week.
    state: () => JSON.parse(sim.state()),

    // ---- what he does, when he does it (minute: the prototype's clock at that moment) ----
    /// Damage done, and who saw it: witnesses is [{ id, rung }], ids of the prototype or the cast.
    deed({ minute, area, thing, said, witnesses = [], fact, words, certainty = 1 }) {
      const [day, hour, min] = before(minute);
      sim.deed(day, hour, min, area, thing, said, witnesses.map((w) => `${PROTOTYPE_TO_CAST[w.id] ?? w.id}:${w.rung}`).join(','), fact, words, certainty);
    },
    /// Something seen that is no damage: one person saw it themselves, at this rung. True if the town took it.
    saw({ minute, who, rung = -1, fact, area, words, certainty = 1 }) {
      const [day, hour, min] = before(minute);
      return sim.witness(PROTOTYPE_TO_CAST[who] ?? who, fact, area, words, day, hour, min, certainty, rung);
    },
    /// His answer to a night's ask (NightAnswer). True if it was taken.
    answerAsk(askDay, what, minute) { const [day, hour, min] = before(minute); return sim.answerAsk(askDay, what, day, hour, min); },
    asksOn: (day) => sim.asksOn(day),
    askDelivered: (day) => sim.askDelivered(day),
    /// A minute he spends at Ada's tea.
    teaDay: () => sim.teaDay(),
    teaMinute(minute) { sim.teaWithHer(...clockOf(minute)); },
    /// The week's end: its day, whether Sheila asks now, her question put, his answer (WeekAnswer).
    weekDay: () => sim.weekDay(),
    weekAsksNow(minute, atOffice = true) { return sim.weekAsksNow(...clockOf(minute), atOffice); },
    weekAsk(minute) { return sim.weekAsk(...clockOf(minute)); },
    weekGive(answer, minute) { const [day, hour, min] = before(minute); return sim.weekGive(answer, day, hour, min); },

    // ---- the save ----
    /// The town as one plain object for the prototype's save: the same texts the packaged game
    /// writes to its save folder (the town's talk, each person's memory, the week's pieces and
    /// the few lines beside them), with the bridge's own place in the week.
    save() {
      const memories = {};
      for (const person of sim.people()) memories[person] = sim.saveMemory(person);
      return {
        kind: 'one-sim town', v: BRIDGE_SAVE_VERSION, cast: mark, at, nextHour, talk,
        texts: { agents: sim.saveAgents(), town: sim.saveTown(), week: sim.saveWeek(), memories },
      };
    },
  };
  return town;
}
