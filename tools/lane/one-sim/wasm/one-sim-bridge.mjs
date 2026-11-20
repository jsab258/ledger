// ONE SIMULATION IN THE BROWSER: the plain bridge for the prototype (step 3a, 19 November 2026;
// run 3 the same day: the fresh review's fixes, and the way in for a save from before the swap).
//
// The prototype keeps its own clock (game minutes since Monday 00:00), its own street, its own
// money, debts, jobs, fights and talk. This module is the one place where that clock meets the
// town: the game's own town rules, compiled for the browser (one-sim.wasm, loaded by one-sim.mjs).
// BRIDGE.md says in plain words what the prototype calls and what it reads back.
//
//   import { openTown } from './one-sim-bridge.mjs';
//   const town = await openTown({ wasm, castJson, startMinute: G.t });           // a new week
//   const town = await openTown({ wasm, castJson, saved: G.town });              // a saved week
//   const { town } = await openTownFromOldSave({ wasm, castJson, old });         // a save from before the swap
//   for (const hour of town.tick(G.t, area)) { ... }                             // every simulation step
//   G.town = town.save();                                                        // whenever the prototype saves
//
// NO TOWN RULE LIVES HERE. The bridge only turns the prototype's minutes into the calls the
// packaged game makes (CrimeProbe.cpp ClockHours and its clock tick), in the same order:
//   for each whole hour the clock has crossed: the talk of the hour before, up to its last minute;
//   then the hour's scheduled steps (TownWeek::RunHour); and after them the talk up to now.
// It remembers two things the game also keeps outside the town (CrimeProbe.cpp ConstableHour):
// that he is held, and until when.
//
// What the bridge does add is refusals. A call the town would take in silence and that would
// leave it wrong (an act out of turn, a second deed, an area or a story name it does not know, a
// save whose pieces do not fit) is refused here with its reason, and nothing is changed.
import { loadOneSim, loadOneSimNow, NightAnswer, WeekAnswer, Offence } from './one-sim.mjs';

export { NightAnswer, WeekAnswer, Offence };

/// The version of the saved object below. A save from a later version is refused.
export const BRIDGE_SAVE_VERSION = 2;   // 2 (the one-shot, 20 Nov 2026): the crimes told to the town and the reports still to make travel with it

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

/// STORY NAMES THE TOWN'S OWN RULES USE. A story is "player.<fact>". The rules file stories of
/// their own under these names and read them back by name: the answers to the night's asks
/// (Arrangement.h, "outfit_d"), the arrest seen (PoliceFile.h, "taken_d"), DS Ellis asking
/// ("police_d"), the week's end ("week_d"), a threat to a witness (Silence.h, "threat_"), and the
/// two plain facts of him (Gossip.h PlainFactOfHim, "name" and "arrived"). A sighting or a deed
/// handed in under one of them would be taken for the rule's own story, so it is refused.
export const TOWN_OWN_FACTS = Object.freeze({ starts: ['outfit_d', 'taken_d', 'police_d', 'week_d', 'threat_'], whole: ['name', 'arrived'] });

const MIN_PER_DAY = 1440;
/// The longest jump of the clock one tick will follow: a year. A wilder number is a fault in the caller, and is
/// refused before the page is left running hours by the million.
const LONGEST_JUMP_MINUTES = 366 * MIN_PER_DAY;
/// The last minute a town can live to. The town's own save keeps how far its talk has run only below
/// 600 million minutes (TownRounds.h, TownHours FromValue: about 1,140 years); past it a saved town
/// would come back with its talk started over. No clock is followed that far.
const LAST_MINUTE = 6e8 - 1;
const ROUND_MINUTES = 6;   // TownRounds.h MinutesBetweenRounds: read here only to check a save against the town's own record
const unEsc = (s) => s.replace(/~/g, ' ').replace(/\^/g, '\n').replace(/!/g, '|');   // the golden table's escaping, undone
const clockOf = (minute) => {
  const m = Math.floor(minute), day = Math.floor(m / MIN_PER_DAY), rest = m - day * MIN_PER_DAY;
  return [day, Math.floor(rest / 60), rest % 60];
};
const plain = (x) => x !== null && typeof x === 'object' && !Array.isArray(x);
const quote = (x) => { try { return String(JSON.stringify(typeof x === 'string' ? x.slice(0, 60) : x)).slice(0, 70); } catch (e) { return typeof x; } };

// The cast file as the page reads it: its areas, each with its places. The town reads the file
// itself (one_sim.cpp os_town_new); this second reading only serves the bridge's own checks.
function areasOf(castJson) {
  let cast;
  try { cast = JSON.parse(castJson.replace(/^﻿/, '')); }
  catch (e) { throw new Error(`one-sim bridge: the town read the cast file, but the page cannot read it as JSON (${String(e.message).slice(0, 80)})`); }
  const areas = new Map();
  if (plain(cast) && plain(cast.areas)) for (const [id, a] of Object.entries(cast.areas)) areas.set(id, plain(a) && Array.isArray(a.places) ? a.places.map(String) : []);
  return areas;
}
// A MARK OF WHAT A SAVE RESTS ON IN THE CAST FILE: who is in the town, and its areas with their
// places (FNV-1a, 32 bits, over the sorted names). Not the file's text: a byte-order mark, the
// line endings of a Windows checkout, the spacing, the notes, the routines and the ties may all
// change and the save still loads, as the packaged game's does (its save holds no cast at all).
function castMark(people, areas) {
  const text = 'people:' + [...people].sort().join(',') + '|areas:' + [...areas.keys()].sort().map((a) => a + '=' + [...areas.get(a)].sort().join('+')).join(',');
  let h = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  return h.toString(16).padStart(8, '0');
}

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
export async function openTown(options = {}) {
  refuseBeforeLoading(options);
  const sim = await loadOneSim(options.wasm, options.print ? { print: options.print } : undefined);
  return openTownWith(sim, options);
}
/// The same without waiting (the one-shot of 20 November 2026): `module` is one-sim.wasm already
/// compiled (WebAssembly.compile, once, when the page starts).
export function openTownNow(options = {}) {
  refuseBeforeLoading(options);
  return openTownWith(loadOneSimNow(options.module, options.print ? { print: options.print } : undefined), options);
}
// What can be refused before the simulation is loaded at all, each with its reason.
function refuseBeforeLoading(options) {
  if (!plain(options)) throw new Error('one-sim bridge: openTown takes { wasm, castJson, startMinute } or { wasm, castJson, saved }');
  const { castJson, saved } = options;
  const talk = options.talk ?? 'by the minute';
  if (typeof castJson !== 'string' || !castJson) throw new Error('one-sim bridge: no cast file text was given');
  if (talk !== 'by the minute' && talk !== 'by the hour') throw new Error(`one-sim bridge: talk is 'by the minute' or 'by the hour', not ${quote(talk)}`);
  // A saved week that is asked for and is not there must never turn into a new week at minute zero without a
  // word: the next tick would then play every hour since Monday over a week the player has already lived.
  const wantsSaved = 'saved' in options;
  if (wantsSaved && (saved === null || saved === undefined)) throw new Error('one-sim bridge: no saved town was given. A save from before the swap has none: open it with openTownFromOldSave');
  if (wantsSaved && 'startMinute' in options) throw new Error('one-sim bridge: a saved town keeps its own clock; give saved or startMinute, not both');
}
function openTownWith(sim, options) {
  refuseBeforeLoading(options);
  const { castJson, startMinute = 0, saved } = options;
  let talk = options.talk ?? 'by the minute';
  const wantsSaved = 'saved' in options;
  // Each town has a module of its own, so a town that is refused below is simply dropped: nothing of it is left behind.
  sim.newTown(castJson);                          // throws "cast not read: ..." with the town's own reason
  const people = sim.people(), inCast = new Set(people);
  const areas = areasOf(castJson);
  const mark = castMark(people, areas);
  let at, nextHour, held = null;
  // CRIMES THAT ARE NO DAMAGE TO THE WEEK'S ONE THING (the one-shot, 20 Nov 2026): each with the witnesses who may yet go
  // to the police over it, and whether he has been taken for it. The rules asked are the port's own (WouldReport, Report,
  // TakeIn); the timetable below is the deed's own (TownWeek.h NineReports and TenConstable), followed here for these.
  let crimes = [];

  // The town's own record of how far its talk has run: the first round not yet run, in minutes, or -1 before any.
  const townRound = () => { const m = /"hours":\{"next":-?\d+,"round":(-?\d+)\}/.exec(sim.state()); return m ? Number(m[1]) : null; };

  if (wantsSaved) {
    // Everything that can be checked is checked before anything is loaded, each refusal with its reason.
    if (!plain(saved) || saved.kind !== 'one-sim town') throw new Error('one-sim bridge: this is not a saved town');
    if (!Number.isInteger(saved.v) || saved.v < 1 || saved.v > BRIDGE_SAVE_VERSION) throw new Error(`one-sim bridge: the saved town is version ${quote(saved.v)}, this build reads ${BRIDGE_SAVE_VERSION}`);
    if (saved.talk !== 'by the minute' && saved.talk !== 'by the hour') throw new Error(`one-sim bridge: the saved town is not whole: its way of talking reads ${quote(saved.talk)}`);
    const t = saved.texts;
    // The talk and the week's pieces must each be a JSON object's text. (They are not parsed here: the town code
    // reads its own texts, and writes numbers a JavaScript reader would refuse. Its own reader would take a week's
    // text that is no object as a fresh week, which for a save is a loss nobody is told of: refused here instead.)
    const objectText = (x) => typeof x === 'string' && x.trimStart().startsWith('{') && x.trimEnd().endsWith('}');
    if (!plain(t) || !objectText(t.agents) || !objectText(t.town) || typeof t.week !== 'string' || !plain(t.memories)) throw new Error('one-sim bridge: the saved town is not whole');
    // The people first, by name: a save made with other people says who, which a mark alone could not.
    const savedPeople = Object.keys(t.memories);
    const gone = savedPeople.filter((p) => !inCast.has(p)), fresh = people.filter((p) => !(p in t.memories));
    if (gone.length && fresh.length || saved.cast !== mark && (gone.length || fresh.length))
      throw new Error('one-sim bridge: the saved town was made with another cast file' + (gone.length ? `; in the save and not in the cast: ${gone.slice(0, 6).join(', ')}` : '')
        + (fresh.length ? `; in the cast and not in the save: ${fresh.slice(0, 6).join(', ')}` : ''));
    if (gone.length) throw new Error(`one-sim bridge: the saved town is not whole: it holds a memory for ${gone.slice(0, 6).join(', ')}, who is not in its cast`);
    if (fresh.length) throw new Error(`one-sim bridge: the saved town is not whole: no memory for ${fresh.slice(0, 6).join(', ')}`);
    const noText = people.filter((p) => typeof t.memories[p] !== 'string');
    if (noText.length) throw new Error(`one-sim bridge: the saved town is not whole: the memory of ${noText.slice(0, 6).join(', ')} is no text`);
    if (saved.cast !== mark) throw new Error('one-sim bridge: the saved town was made with another cast file: its areas or places are not the same');
    // Each piece must be the piece it says it is. The town's own readers take a text that holds nothing (an empty
    // object, a memory with no heading) as a town that knows nothing, which for a save is a loss nobody is told of.
    const wrongMemory = people.filter((p) => t.memories[p] !== `# Memory: ${p}` && !t.memories[p].startsWith(`# Memory: ${p}\n`));
    if (wrongMemory.length) throw new Error(`one-sim bridge: the saved town is not whole: the memory kept for ${wrongMemory.slice(0, 6).join(', ')} is not that person's memory`);
    const noTalk = people.filter((p) => !t.agents.includes(`"id":${JSON.stringify(p)}`));
    if (noTalk.length) throw new Error(`one-sim bridge: the saved town is not whole: its talk does not hold ${noTalk.slice(0, 6).join(', ')}`);
    if (!/"hours"\s*:\s*\{/.test(t.town)) throw new Error('one-sim bridge: the saved town is not whole: its week does not say how far the talk has run');
    // Its place in the week: a whole minute, and the next hour due the one that follows it (or the minute's own
    // hour, for a town saved on the stroke of an hour before that hour ran).
    if (!Number.isInteger(saved.at) || saved.at < 0 || saved.at > LAST_MINUTE || !Number.isInteger(saved.nextHour)) throw new Error('one-sim bridge: the saved town is not whole: its clock is no whole minute of a week');
    const hourNow = Math.floor(saved.at / 60), unrun = saved.at % 60 === 0 && saved.nextHour === hourNow;
    if (saved.nextHour !== hourNow + 1 && !unrun) throw new Error(`one-sim bridge: the saved town's clock does not fit itself (minute ${saved.at}, next hour ${saved.nextHour})`);
    let week;
    try { week = JSON.parse(t.week); } catch (e) { throw new Error('one-sim bridge: the saved town is not whole'); }
    if (!plain(week) || typeof week.deedTopic !== 'string' || !Number.isInteger(week.deedDay) || week.deedDay < -1 || !Number.isInteger(week.deedAt) || week.deedAt < -1
        || typeof week.ellisFirst !== 'string' || typeof week.takenFirst !== 'string' || !Array.isArray(week.witnesses)
        || week.witnesses.some((w) => !Array.isArray(w) || w.length !== 2 || typeof w[0] !== 'string' || !Number.isInteger(w[1])))
      throw new Error('one-sim bridge: the saved town is not whole: the lines beside its week (the deed, who saw it, her first visit, his first arrest) do not read');
    sim.loadAgents(t.agents);
    for (const person of people) sim.loadMemory(person, t.memories[person]);
    sim.loadTown(t.town);
    sim.loadWeek(week);
    // And the clock against the town's own record, now that the town has read its texts: its talk cannot have run
    // past the saved minute, nor stopped short of the last hour said to have run. (A clock moved back would play
    // hours over a town that has lived them; a clock moved on would skip hours it never had.)
    const round = townRound();
    const last = Math.floor(saved.at / ROUND_MINUTES) * ROUND_MINUTES + ROUND_MINUTES;
    if (round === null || round > last || (round >= 0 && (unrun || round < (saved.nextHour - 1) * 60 + ROUND_MINUTES)) || round < -1)
      throw new Error(`one-sim bridge: the saved town's clock does not fit the town (minute ${saved.at}, next hour ${saved.nextHour}; the town's own talk has run to ${round === null ? 'no minute it can name' : 'minute ' + (round - ROUND_MINUTES)})`);
    if (saved.crimes !== undefined) {
      if (!Array.isArray(saved.crimes) || saved.crimes.some((c) => !plain(c) || typeof c.topic !== 'string' || !Number.isInteger(c.offence) || !Number.isFinite(c.minute) || !Array.isArray(c.witnesses)))
        throw new Error('one-sim bridge: the saved town is not whole: its list of crimes does not read');
      crimes = JSON.parse(JSON.stringify(saved.crimes));
    }
    talk = saved.talk;
    at = saved.at;
    nextHour = saved.nextHour;
    const until = sim.heldUntil(...clockOf(at));
    if (until >= 0) held = { until };
  } else {
    if (!Number.isFinite(startMinute) || startMinute < 0 || startMinute > LAST_MINUTE) throw new Error('one-sim bridge: the week starts at a minute from Monday 00:00, zero or later');
    at = Math.floor(startMinute);
    nextHour = Math.ceil(startMinute / 60);       // an hour that begins exactly at the start is the first one run
    sim.age(...clockOf(at));                      // the town's talk aged to the start, as a week's first hour does
  }

  // IN TURN: he does things at the clock's minute or later, inside an hour that has already had its steps. The clock
  // must have been ticked to that minute first. Nothing is changed by the check.
  const inTurn = (minute) => {
    if (!Number.isFinite(minute) || minute < 0) throw new Error('one-sim bridge: he does things at a minute from Monday 00:00, zero or later');
    const m = Math.floor(minute);
    if (m < at) throw new Error(`one-sim bridge: that minute (${m}) is before the town's clock (${at})`);
    if (Math.floor(m / 60) >= nextHour) throw new Error(`one-sim bridge: tick the clock to minute ${m} before he acts at it`);
    return m;
  };
  // Before something he does that the town is told of: the talk up to the minute before, as the reference week runs it.
  const before = (minute) => {
    const m = inTurn(minute);
    if (m >= 1) sim.roundsTo(...clockOf(m - 1));
    at = m;
    return clockOf(m);
  };
  const knownArea = (area) => typeof area === 'string' && (areas.size === 0 ? area !== '' : areas.has(area));   // a cast file that names no areas takes any
  const needArea = (area, what) => {
    if (!knownArea(area)) throw new Error(`one-sim bridge: ${what} ${quote(area)} is no area of the cast file` + (areas.size ? ` (its areas: ${[...areas.keys()].join(', ')})` : ''));
  };
  const needFact = (fact) => {
    if (typeof fact !== 'string' || !/^[A-Za-z0-9_]{1,80}$/.test(fact)) throw new Error(`one-sim bridge: a story's name is letters, digits and underscores, not ${quote(fact)}`);
    if (TOWN_OWN_FACTS.whole.includes(fact) || TOWN_OWN_FACTS.starts.some((p) => fact.startsWith(p))) throw new Error(`one-sim bridge: the story name ${quote(fact)} is one the town's own rules use; pick another`);
  };
  // Text, and not empty: the town keeps no damage for a thing with no name or nothing said of it, and would still
  // keep the deed's story, so that the witness went to the police over damage nobody could ever find.
  const needText = (x, what) => { if (typeof x !== 'string' || x.trim() === '') throw new Error(`one-sim bridge: ${what} is text with something in it, not ${quote(x)}`); };
  const needSure = (x) => { if (!(typeof x === 'number' && x > 0 && x <= 1)) throw new Error(`one-sim bridge: how sure a witness is runs from just above 0 to 1, not ${quote(x)}`); };
  const needRung = (x) => { if (!Number.isInteger(x) || x < -1 || x > 4) throw new Error(`one-sim bridge: how well a witness saw him is 0 to 4 (Rung), or -1 for a thing known, not ${quote(x)}`); };
  const castId = (id) => (typeof id !== 'string' ? null : Object.prototype.hasOwnProperty.call(PROTOTYPE_TO_CAST, id) ? PROTOTYPE_TO_CAST[id] : id);
  // The week's deed as the town itself holds it (the same lines the save carries), or null: none yet.
  const deedHeld = () => {
    const w = JSON.parse(sim.saveWeek());
    return w.deedDay >= 0 && w.deedTopic ? { topic: w.deedTopic, day: w.deedDay, minute: w.deedAt, witnesses: w.witnesses.map(([id, rung]) => ({ id, rung })) } : null;
  };
  // "Held" is the game's to keep, not the town's: taken from each hour's own answer, with the release time asked of the custody.
  const noteHeld = (event) => {
    if (!event.held) { held = null; return; }
    const until = sim.heldUntil(event.day, event.hour, 0);
    held = { until: until >= 0 ? until : event.minute + 60 };
  };

  // The morning a crime is first reported: nine on the day after its night (a crime before six is the night before's),
  // as TownWeek's Aftermath::FirstReportMorning has it for the deed.
  const firstReportDay = (minute) => { const d = Math.floor(minute / MIN_PER_DAY); return minute - d * MIN_PER_DAY < 6 * 60 ? d : d + 1; };
  const nineReportsForCrimes = (day) => {
    const went = [];
    for (const c of crimes) {
      if (day < firstReportDay(c.minute)) continue;
      for (const w of c.witnesses) {
        if (w.went || w.never) continue;
        const would = w.host ? sim.wouldReportAs(w.nerve, w.loyalty, c.offence, !!w.victim) : sim.wouldReport(w.id, c.offence, !!w.victim, c.topic);
        if (!would) continue;
        if (sim.policeReport(w.host ? 'host:' + w.id : w.id, c.topic, c.offence, w.rung, day)) {
          w.went = day;
          went.push({ who: w.id, host: !!w.host, topic: c.topic, offence: c.offence, statement: w.rung >= 4 });
        }
      }
    }
    return went;
  };
  // Ten o'clock, nobody come for the damage and he is not held: a constable for the oldest crime with a statement
  // (a witness who recognised him) of a kind a man is taken for (PoliceFile Arrestable: damage, and from wounding up).
  const ARRESTABLE = (o) => o === Offence.Damage || o >= Offence.Wounding;
  const END = { [Offence.Damage]: 'Charged', [Offence.Wounding]: 'Charged', [Offence.Robbery]: 'Charged', [Offence.Killing]: 'BailedToReturn' };
  const tenConstableForCrimes = (day) => {
    for (const c of crimes) {
      if (c.taken || !ARRESTABLE(c.offence)) continue;
      if (!c.witnesses.some((w) => Number.isInteger(w.went) && w.went < day && w.rung >= 4)) continue;   // a statement of an earlier day, as the deed's
      if (!sim.takeIn(c.topic, day, 10, 0)) continue;
      c.taken = day;
      return { topic: c.topic, offence: c.offence, end: END[c.offence] ?? 'Charged' };
    }
    return null;
  };

  const town = {
    sim,                                           // the loader's own object: for reading and for the tests. Acts go through the calls below.
    talk: () => talk,
    now: () => at,
    /// He is in the cells: { until: the minute he is let out }, or null. Kept here, as the game keeps it.
    held: () => (held ? { ...held } : null),
    /// The areas of the cast file, by name. Empty for a cast file that names none.
    areas: () => [...areas.keys()],

    /// EVERY SIMULATION STEP: the prototype's clock now (game minutes since Monday 00:00, fractions
    /// welcome) and the area he stands in (for ten o'clock's constable). Returns the hours that
    /// began since the last call, oldest first, each as readHour gives it; most calls return none.
    /// HANDLE THE WHOLE LIST BEFORE MOVING THE CLOCK AGAIN: a clock skip started from inside the
    /// loop over these hours would hand later hours to the page before the rest of this list.
    tick(nowMinute, area = 'mickeys') {
      if (!Number.isFinite(nowMinute)) throw new Error('one-sim bridge: the clock is not a number');
      const now = Math.floor(nowMinute);
      if (now < at) throw new Error(`one-sim bridge: the clock went back (${now} after ${at}); open the town again from its save`);
      if (now - at > LONGEST_JUMP_MINUTES) throw new Error(`one-sim bridge: the clock jumped more than a year (${at} to ${now})`);
      if (now > LAST_MINUTE) throw new Error(`one-sim bridge: the clock is past the last minute a town can be saved at (${LAST_MINUTE})`);
      needArea(area, 'where he stands:');
      const hours = [];
      for (; nextHour * 60 <= now; nextHour++) {
        const day = Math.floor(nextHour / 24), hod = nextHour - day * 24;
        if (talk === 'by the minute' && nextHour * 60 >= 1) sim.roundsTo(...clockOf(nextHour * 60 - 1));   // the hour before's talk first
        const wentForCrimes = hod === 9 ? nineReportsForCrimes(day) : [];   // before nine's own steps, so DS Ellis hears of a wounding the same morning
        const event = readHour(sim.hour(day, hod, area), day, hod);
        event.crimeWent = wentForCrimes;          // [{ who, topic, offence, statement }]: who went to the police over a crime that is no damage to the week's thing
        event.takenFor = null;                    // the crime's topic, when the constable came for one of those
        if (hod === 10 && !event.taken && !event.held) {
          const c = tenConstableForCrimes(day);
          if (c) { event.taken = c.end; event.takenFor = c.topic; event.takenOffence = c.offence; event.held = true; }
        } else if (hod === 10 && event.taken) event.takenFor = deedHeld()?.topic ?? null;
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
    placeOf(person, minute = at) { const [day, hour] = clockOf(minute); return sim.placeOf(castId(person) ?? '', day, hour); },
    /// The Ledger's facts: who knows what, and how (saw it or was told, from whom, how well the first witness saw him).
    knows: () => sim.knows(),
    /// The week's pieces as the game's save writes them: asks, police, tea, damage, arrests, hours, week.
    state: () => JSON.parse(sim.state()),
    /// The week's one deed as the town holds it: { topic, day, minute, witnesses: [{ id, rung }] }, or null.
    deedHeld,

    // ---- what he does, when he does it (minute: the prototype's clock at that moment) ----
    /// DAMAGE DONE, and who saw it: witnesses is [{ id, rung }], ids of the prototype or the cast.
    /// THE TOWN FOLLOWS ONE DEED: the rules keep one deed's story and its witnesses (TownWeek.h
    /// Deed), and a second would replace the first, witnesses and all, so that nobody went to the
    /// police for the first. A second deed is therefore refused; tell the town of it with saw(),
    /// one call a witness, and it becomes talk. Returns { taken, dropped }: the witnesses the
    /// town took, by the cast's ids, and the ones it does not know (most of the prototype's
    /// people have no match in the cast), each with why.
    deed(what = {}) {
      if (!plain(what)) throw new Error(`one-sim bridge: a deed is { minute, area, thing, said, witnesses, fact, words }, not ${quote(what)}`);
      const { minute, area, thing, said, witnesses = [], fact, words, certainty = 1 } = what;
      inTurn(minute);
      needArea(area, 'the deed\'s place');
      needText(thing, 'the thing damaged'); needText(said, 'what is said of the damage'); needText(words, 'the story\'s words');
      needFact(fact); needSure(certainty);
      if (!Array.isArray(witnesses)) throw new Error('one-sim bridge: witnesses is a list of { id, rung }');
      const taken = [], dropped = [], seen = new Set();
      for (const w of witnesses) {
        const id = castId(w?.id);
        if (id === null) throw new Error(`one-sim bridge: a witness is { id, rung }, not ${quote(w)}`);
        needRung(w.rung);
        if (!inCast.has(id)) dropped.push({ id: w.id, why: 'not in the cast' });
        else if (seen.has(id)) dropped.push({ id: w.id, why: 'named twice' });
        else { seen.add(id); taken.push({ id, rung: w.rung }); }
      }
      const first = deedHeld();
      if (first) throw new Error(`one-sim bridge: the town follows one deed and already holds ${first.topic} (day ${first.day + 1}); a second would wipe out who saw the first. Tell the town of this one with saw()`);
      const [day, hour, min] = before(minute);
      sim.deed(day, hour, min, area, thing, said, taken.map((w) => `${w.id}:${w.rung}`).join(','), fact, words, certainty);
      return { taken, dropped };
    },
    /// Something seen that is no damage: one person saw it themselves, at this rung. True if the town took it,
    /// false if the witness is nobody of the cast. It becomes talk; it is never a statement to the police.
    saw(what = {}) {
      if (!plain(what)) throw new Error(`one-sim bridge: a sighting is { minute, who, rung, fact, area, words }, not ${quote(what)}`);
      const { minute, who, rung = -1, fact, area, words, certainty = 1 } = what;
      inTurn(minute);
      needArea(area, 'the sighting\'s place');
      needFact(fact); needText(words, 'the story\'s words'); needSure(certainty); needRung(rung);
      const id = castId(who);
      if (id === null) throw new Error(`one-sim bridge: who saw it is an id, not ${quote(who)}`);
      if (!inCast.has(id)) return false;
      const [day, hour, min] = before(minute);
      return sim.witness(id, fact, area, words, day, hour, min, certainty, rung);
    },
    // ---- added by the one-shot of 20 November 2026 (step 4, the swap) ----
    /// Whether the town has this person (the prototype's id or the cast's), and the cast's id for them.
    covers: (id) => inCast.has(castId(id)),
    castId,
    /// How well a witness sees him, by the port's own rule (Perception::IdRung): the distance in metres, the light on
    /// him (0 to 1), how well the witness knows him (0 to 1), whether he carries a mark (the coat, the cab) and whether
    /// his face is toward the witness. 0 someone, 1 a silhouette, 2 a mark, 3 a face, 4 recognised.
    rung: (metres, light, familiarity, mark, faceToward = true) => sim.idRung(metres, light, familiarity, !!mark, !!faceToward),
    /// One person's temper as the town holds it: { nerve, loyalty }, or null.
    temper: (id) => sim.temper(castId(id) ?? ''),
    /// An OPEN act seen (a fare driven, a debt struck out, the rent paid): as saw(), but not kept as about his hidden life.
    sawOpen(what = {}) {
      if (!plain(what)) throw new Error(`one-sim bridge: a sighting is { minute, who, rung, fact, area, words }, not ${quote(what)}`);
      const { minute, who, rung = -1, fact, area, words, certainty = 1 } = what;
      inTurn(minute);
      needArea(area, 'the sighting\'s place');
      needFact(fact); needText(words, 'the story\'s words'); needSure(certainty); needRung(rung);
      const id = castId(who);
      if (id === null) throw new Error(`one-sim bridge: who saw it is an id, not ${quote(who)}`);
      if (!inCast.has(id)) return false;
      const [day, hour, min] = before(minute);
      return sim.witnessOpen(id, fact, area, words, day, hour, min, certainty, rung);
    },
    /// A CRIME SEEN THAT IS NOT THE WEEK'S ONE DEED: a blow, a wounding, a robbery, a killing, or a further piece of
    /// damage. offence is an Offence. witnesses is [{ id, rung, victim?, sure?, nerve?, loyalty? }]. Somebody of the cast
    /// holds the story first-hand at once (the mill's own Witness) and passes it on as any story. Somebody the cast does
    /// not have (a host's own person: give their nerve and their goodwill toward him, 0 to 1) holds nothing in the town,
    /// but may still go to the police. From nine on the morning after, each witness goes if the port's own rule says
    /// they would (WouldReport), and the report is filed in the town's own police file (Report). At ten on a later day a
    /// constable comes for a crime with a statement, if it is of a kind a man is taken for (TakeIn). Each hour's answer
    /// then says so (crimeWent, taken, takenFor). Returns { told, queued, dropped }.
    crime(what = {}) {
      if (!plain(what)) throw new Error(`one-sim bridge: a crime is { minute, area, offence, fact, words, witnesses }, not ${quote(what)}`);
      const { minute, area, offence, fact, words, witnesses = [] } = what;
      inTurn(minute);
      needArea(area, 'the crime\'s place');
      needFact(fact); needText(words, 'the story\'s words');
      if (!Number.isInteger(offence) || offence < Offence.Suspicious || offence > Offence.Killing) throw new Error(`one-sim bridge: an offence is 0 to 5 (Offence), not ${quote(offence)}`);
      if (!Array.isArray(witnesses)) throw new Error('one-sim bridge: witnesses is a list of { id, rung }');
      const topic = 'player.' + fact;
      if (crimes.some((c) => c.topic === topic)) throw new Error(`one-sim bridge: the town already holds a crime under the name ${quote(fact)}`);
      const list = [], told = [], dropped = [], seen = new Set();
      for (const w of witnesses) {
        if (!plain(w) || typeof w.id !== 'string' || !w.id) throw new Error(`one-sim bridge: a witness is { id, rung }, not ${quote(w)}`);
        needRung(w.rung);
        const id = castId(w.id), host = !inCast.has(id);
        if (seen.has(id)) { dropped.push({ id: w.id, why: 'named twice' }); continue; }
        seen.add(id);
        if (host && !(typeof w.nerve === 'number' && w.nerve >= 0 && w.nerve <= 1 && typeof w.loyalty === 'number' && w.loyalty >= 0 && w.loyalty <= 1)) {
          dropped.push({ id: w.id, why: 'not in the cast, and no nerve and goodwill given for them' });
          continue;
        }
        const sure = w.sure === undefined ? 1 : w.sure;
        needSure(sure);
        list.push(host ? { id, host: true, rung: w.rung, victim: !!w.victim, nerve: w.nerve, loyalty: w.loyalty, never: !!w.never }
                       : { id, rung: w.rung, victim: !!w.victim, sure, never: !!w.never });
      }
      const [day, hour, min] = before(minute);
      for (const w of list) if (!w.host && w.rung >= 0 && sim.witness(w.id, fact, area, words, day, hour, min, w.sure, w.rung)) told.push(w.id);
      crimes.push({ topic, offence, minute: at, area, witnesses: list });
      return { told, queued: list.map((w) => w.id), dropped };
    },
    /// The crimes told so far, each with who has gone to the police over it and whether he was taken for it (a copy).
    crimes: () => JSON.parse(JSON.stringify(crimes)),
    /// A witness of a crime talked round, paid or frightened before going: they will not go (the game's own decision;
    /// the town's rule for a silenced witness of the deed is Silence.h, not behind the door). True if it changed anything.
    quiet(fact, who) {
      const c = crimes.find((x) => x.topic === 'player.' + fact), id = castId(who);
      const w = c && c.witnesses.find((x) => x.id === id && !Number.isInteger(x.went));
      if (!w || w.never) return false;
      w.never = true;
      return true;
    },

    /// His answer to a night's ask (NightAnswer). True if it was taken.
    answerAsk(askDay, what, minute) { const [day, hour, min] = before(minute); return sim.answerAsk(askDay, what, day, hour, min); },
    asksOn: (day) => sim.asksOn(day),
    askDelivered: (day) => sim.askDelivered(day),
    /// A minute he spends at Ada's tea. In turn, as every act: not before the clock, not in an hour still to run.
    teaDay: () => sim.teaDay(),
    teaMinute(minute) { const m = inTurn(minute); at = m; sim.teaWithHer(...clockOf(m)); },
    /// The week's end: its day, whether Sheila asks now, her question put, his answer (WeekAnswer).
    /// The question "does she ask now" is in turn too, but moves no clock: it may be asked of a later minute of the hour.
    weekDay: () => sim.weekDay(),
    weekAsksNow(minute, atOffice = true) { return sim.weekAsksNow(...clockOf(inTurn(minute)), atOffice); },
    weekAsk(minute) { const m = inTurn(minute); const asked = sim.weekAsk(...clockOf(m)); if (asked) at = m; return asked; },
    weekGive(answer, minute) { const [day, hour, min] = before(minute); return sim.weekGive(answer, day, hour, min); },

    // ---- the save ----
    /// The town as one plain object for the prototype's save: the same texts the packaged game
    /// writes to its save folder (the town's talk, each person's memory, the week's pieces and
    /// the few lines beside them), with the bridge's own place in the week.
    save() {
      const memories = {};
      for (const person of people) memories[person] = sim.saveMemory(person);
      return {
        kind: 'one-sim town', v: BRIDGE_SAVE_VERSION, cast: mark, at, nextHour, talk, crimes: JSON.parse(JSON.stringify(crimes)),
        texts: { agents: sim.saveAgents(), town: sim.saveTown(), week: sim.saveWeek(), memories },
      };
    },
  };
  return town;
}

// =====================================================================================================
// A SAVE FROM BEFORE THE SWAP (the prototype's own town in it, no town of the game's).
// The prototype has kept every older save loading (its CHANGELOG, its test/oldsave.mjs), so the swap
// must too. Such a save opens a FRESH town at the save's clock, and what its people saw him do
// with their own eyes is told to that town at that minute, each as a sighting at the rung their
// old memory supports. What they were only told is not carried: the town's own talk passes the
// stories on again from those who saw them.
// =====================================================================================================

/// WHAT THE TOWN IS TOLD OF EACH KIND OF ACT THE PROTOTYPE KNOWS (its kinds.js: 52 kinds of act
/// and "word", a thing he was told). One home for the table: DIFFERENCES.md prints it, and
/// `one-sim.sh differences` checks it against the prototype's own list and numbers.
///   saw    a sighting, through town.saw, under this name with the event's number after it. The
///          town keeps every sighting as about his hidden life, which fits an act that reads badly.
///   step   the real rules make this story themselves when their own step or call runs (named
///          in `by`); telling it again would have the town hold it twice.
///   open   an open or decent act. The door has no call for a story that is not about his hidden
///          life, so it has no home in the town yet and stays the prototype's own.
///   none   the real rules have their own plain fact for it, which is not behind the door.
///   never  never passed on in the prototype either.
/// None is damage to a thing: the prototype has no deed of the kind the real week follows.
const saw = (note) => (note ? { tell: 'saw', note } : { tell: 'saw' });
const step = (by) => ({ tell: 'step', by });
const open_ = (note) => (note ? { tell: 'open', note } : { tell: 'open' });
export const PROTOTYPE_ACTS = Object.freeze({
  inherit: { tell: 'none', note: 'who he is: the rules\' plain fact "player.name"' },
  arrive: { tell: 'none', note: 'his arrival: the rules\' plain fact "player.arrived"' },
  night_out: saw(), coat_day: saw(), ran: saw(), parcel: saw(), pickup: saw(), drop: saw(),
  cab_drive: open_(), cab_night: saw(), fare: open_(), free_ride: open_(),
  job_yes: step('answerAsk: the envelope handed over'), job_no: step('answerAsk: a no'), no_show: step('six o\'clock: a night away passed'),
  tea: step('teaMinute, and eleven\'s close'), tea_late: step('teaMinute, and eleven\'s close'), tea_snub: step('eleven\'s close'),
  chapel: open_(), talk_ellis: saw(), talk_press: saw(), asked_fire: open_(),
  stare: saw(), squareup: saw(), threat: saw(), shove: saw(),
  strike: saw('violence: talk only, never a statement'), weapon_out: saw('violence: talk only, never a statement'),
  weapon_used: saw('violence: talk only, never a statement'), kill: saw('violence: talk only, never a statement'),
  set_on: saw(), beaten: open_(), patched: open_(),
  debt_paid: saw(), debt_forgive: open_(), paid_info: saw(), bribe_try: saw(), lied: saw(),
  good_word: open_('a story that starts with other people'),
  arrested: step('ten o\'clock\'s constable: who saw him taken'),
  ran_police: saw('only if the prototype keeps its chase'), bag_taken: saw('only if the prototype keeps its own constable'),
  ellis_asked: step('nine o\'clock\'s DS Ellis: whom she asked'),
  wash: { tell: 'never', note: 'private in the prototype: nobody passes it on' },
  rent_paid: open_(), rent_late: saw(),
  knocked: saw('violence: talk only, never a statement'), crash: saw('the nearest thing to damage; a sighting until he rules otherwise'),
  noise: { tell: 'never', note: 'somebody heard, nobody seen: in the game a noise alone is no story about him' },
  choice_wind: step('weekGive'), choice_take: step('weekGive'), choice_silent: step('the week\'s end closed unanswered, or weekGive'),
  word: { tell: 'never', note: 'not an act: something he was told' },
});

/// THE RUNG AN OLD MEMORY SUPPORTS. The prototype kept, for each memory, whom the witness took
/// him for (who) and a face score. Read here as: "tom" or "owner" (they tie it to him):
/// recognised; "coat" or "cab" (a thing of his, not him): a mark; "man" with a face score above
/// 0.2, the prototype's own line for placing him later: a face; any other "man": a silhouette.
/// This is the bridge's reading of the prototype's memory, not a town rule; step 4 may hand in another.
export function oldMemoryRung(memory) {
  if (memory.who === 'tom' || memory.who === 'owner') return Rung.Recognised;
  if (memory.who === 'coat' || memory.who === 'cab') return Rung.Mark;
  if (memory.who !== 'man') return -1;                       // none of the prototype's five words: no rung can be read
  return typeof memory.face === 'number' && memory.face > 0.2 ? Rung.Face : Rung.Silhouette;
}

/// Opens a fresh town at an old save's clock and tells it what the old save's people saw.
/// `old` is the prototype's save as an object (its t, minds and events are read; nothing is
/// changed in it). `areaOf(event)` gives the cast file's area for an old event (the table from
/// the prototype's map is step 4's; the default is the game's own fallback, "mickeys").
/// `wordsOf(event)` gives the story's words (the prototype's own sentence for the act).
/// Returns { town, hours, fed, dropped, lost }: the town; the hours its first tick ran (to be
/// handled like any tick's); each memory told to the town; each one left out, with why; and in
/// plain lines what the player loses.
export async function openTownFromOldSave(options = {}) {
  refuseOldBeforeLoading(options);
  const sim = await loadOneSim(options.wasm, options.print ? { print: options.print } : undefined);
  return openTownFromOldSaveWith(sim, options);
}
function refuseOldBeforeLoading(options) {
  const old = plain(options) ? options.old : null;
  if (!plain(old) || !Number.isFinite(old.t) || old.t < 0 || !plain(old.minds) || !Array.isArray(old.events)) throw new Error('one-sim bridge: this is not a prototype save (no clock, minds or events)');
  if (plain(old.town)) throw new Error('one-sim bridge: this save holds a town already; open it with openTown({ saved })');
}
/// The same without waiting: `module` is one-sim.wasm already compiled.
export function openTownFromOldSaveNow(options = {}) {
  refuseOldBeforeLoading(options);
  return openTownFromOldSaveWith(loadOneSimNow(options.module, options.print ? { print: options.print } : undefined), options);
}
function openTownFromOldSaveWith(sim, { castJson, old, acts = PROTOTYPE_ACTS, rungOf = oldMemoryRung,
    areaOf = () => 'mickeys', wordsOf = (event) => `he was seen (${event.kind})`, talk } = {}) {
  if (!plain(old) || !Number.isFinite(old.t) || old.t < 0 || !plain(old.minds) || !Array.isArray(old.events)) throw new Error('one-sim bridge: this is not a prototype save (no clock, minds or events)');
  if (plain(old.town)) throw new Error('one-sim bridge: this save holds a town already; open it with openTown({ saved })');
  const town = openTownWith(sim, { castJson, startMinute: old.t, ...(talk ? { talk } : {}) });
  const hours = town.tick(old.t, town.areas().length && !town.areas().includes('mickeys') ? town.areas()[0] : 'mickeys');
  const minute = town.now(), inCast = new Set(town.people()), known = town.areas();
  const events = new Map();
  for (const e of old.events) if (plain(e) && Number.isInteger(e.id)) events.set(e.id, e);

  // Every first-hand memory, oldest event first, then by person: the same save always gives the same town.
  const all = [], unread = [];
  for (const [person, mind] of Object.entries(old.minds)) {
    if (!plain(mind) || !Array.isArray(mind.mem)) continue;
    for (const memory of mind.mem) {
      if (plain(memory)) all.push({ person, memory, event: events.get(memory.e) });
      else unread.push({ who: person, kind: null, event: null, why: 'not a memory at all' });
    }
  }
  all.sort((a, b) => ((a.event?.t ?? 0) - (b.event?.t ?? 0)) || ((a.memory.e ?? 0) - (b.memory.e ?? 0)) || (a.person < b.person ? -1 : a.person > b.person ? 1 : 0));

  const fed = [], dropped = [...unread], deedWitnesses = new Map();
  const drop = (x, why) => dropped.push({ who: x.person, kind: x.event?.kind ?? null, event: x.memory.e ?? null, why });
  const sightings = [];
  for (const x of all) {
    const { person, memory, event } = x;
    const id = Object.prototype.hasOwnProperty.call(PROTOTYPE_TO_CAST, person) ? PROTOTYPE_TO_CAST[person] : person;
    if (!event || typeof event.kind !== 'string') { drop(x, 'its event is not in the save'); continue; }
    const act = Object.prototype.hasOwnProperty.call(acts, event.kind) ? acts[event.kind] : null;
    if (!act) { drop(x, 'a kind of act the table does not know'); continue; }
    if (act.tell !== 'saw' && act.tell !== 'deed') { drop(x, act.tell === 'step' ? 'the town makes this story itself, and starts it afresh' : act.tell === 'open' ? 'an open act: no call for it yet'
      : act.tell === 'none' ? 'a plain fact of him: not behind the door' : 'never passed on'); continue; }
    if (memory.src === 'told') { drop(x, 'only told: the town\'s own talk passes it on again'); continue; }
    if (memory.src === 'heard') { drop(x, 'only heard: a noise alone is no story about him'); continue; }
    if (memory.src !== 'saw' && memory.src !== 'self') { drop(x, 'not first-hand'); continue; }
    if (!inCast.has(id)) { drop(x, 'not in the cast'); continue; }
    const sure = typeof memory.sure === 'number' ? Math.min(1, memory.sure) : NaN;
    if (!(sure > 0)) { drop(x, 'no certainty kept'); continue; }
    const rung = rungOf(memory, old.minds[person]);
    if (!Number.isInteger(rung) || rung < 0 || rung > 4) { drop(x, 'no rung could be read'); continue; }
    if (!/^[A-Za-z0-9_]{1,60}$/.test(event.kind)) { drop(x, 'a kind of act the table does not know'); continue; }
    const area = areaOf(event);
    if (typeof area !== 'string' || (known.length ? !known.includes(area) : area === '')) { drop(x, 'no area of the cast for where it happened'); continue; }
    const said = wordsOf(event);
    const one = { who: id, kind: event.kind, event: event.id, rung, sure, fact: `${event.kind}_e${event.id}`, as: 'saw' };
    if (act.tell === 'deed') { if (!deedWitnesses.has(event.id)) deedWitnesses.set(event.id, []); deedWitnesses.get(event.id).push(one); }
    sightings.push({ one, event, area, words: typeof said === 'string' && said ? said : `he was seen (${event.kind})` });
  }
  // The town follows one deed: the oldest damage with a witness is it, and any later one is told as sightings.
  const theDeed = [...deedWitnesses.keys()].sort((a, b) => (events.get(a).t ?? 0) - (events.get(b).t ?? 0) || a - b)[0];
  if (theDeed !== undefined) {
    const event = events.get(theDeed), list = deedWitnesses.get(theDeed);
    const { area, words } = sightings.find((s) => s.event === event);
    const thing = acts[event.kind].thing;
    town.deed({ minute, area, thing: typeof thing === 'string' ? thing : event.kind, said: words, fact: list[0].fact, words,
      witnesses: list.map((w) => ({ id: w.who, rung: w.rung })), certainty: Math.max(...list.map((w) => w.sure)) });
    for (const w of list) { w.as = 'deed'; fed.push(w); }
  }
  for (const { one, area, words } of sightings) {
    if (one.as === 'deed') continue;
    if (town.saw({ minute, who: one.who, rung: one.rung, fact: one.fact, area, words, certainty: one.sure })) fed.push(one);
    else dropped.push({ who: one.who, kind: one.kind, event: one.event, why: 'the town did not take it' });
  }

  // What the player loses, in plain lines, counted from this very save.
  const count = (why) => dropped.filter((d) => d.why.startsWith(why)).length;
  const lost = [];
  const strangers = [...new Set(dropped.filter((d) => d.why === 'not in the cast').map((d) => d.who))];
  if (strangers.length) lost.push(`${count('not in the cast')} thing(s) seen by ${strangers.length} of the old cast who are not in the real cast (${strangers.slice(0, 8).join(', ')}${strangers.length > 8 ? ', ...' : ''})`);
  if (count('only told')) lost.push(`${count('only told')} thing(s) people had only been told: the new town's own talk starts from those who saw`);
  if (count('the town makes')) lost.push(`${count('the town makes')} memory(ies) of the asks, the tea, an arrest, DS Ellis or the week's end: the real week starts these afresh at the save's clock`);
  if (count('no area of the cast')) lost.push(`${count('no area of the cast')} thing(s) seen where the real street has no area`);
  if (count('an open act') + count('a plain fact')) lost.push(`${count('an open act') + count('a plain fact')} memory(ies) of open or decent acts, which the town cannot be told yet`);
  const start = Math.floor(old.t), teaDay = town.teaDay();
  if (teaDay >= 0 && start > teaDay * MIN_PER_DAY + 10 * 60) lost.push('Ada\'s tea: she asks at ten on its day, which has passed, so this week has no tea');
  const firstAsk = Number(town.state().asks?.first);
  if (Number.isInteger(firstAsk) && start > firstAsk * MIN_PER_DAY + 20 * 60) lost.push('Ron\'s asks: the ask nights already past are held as never delivered and his answers to them are not carried; Ron comes again on the next ask night');
  lost.push('what each person thinks of him and what the street calls him stay the prototype\'s own (DIFFERENCES.md, section 6)');
  return { town, hours, fed, dropped, lost };
}
