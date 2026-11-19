// ONE SIMULATION IN THE BROWSER, step 3b: the prototype's frozen JavaScript town against the real rules, measured.
//
//   node measure.mjs --brain one-sim.wasm --specs production/specs --prototype tools/lane/prototype/project/src [--json OUT.json]
//
// The numbers in DIFFERENCES.md come from this file. It loads the prototype's own rule files as they stand
// (rules.js, cast.js, routines.js, gossip.js, events.js, clock.js: nothing of them is copied or changed) and the
// real town through the bridge (one-sim-bridge.mjs), and asks both the same questions:
//   M1  where is each of the nine people both casts hold, at the half of every hour of a week?
//   M2  on what minutes do people move?
//   M3  one story, seen by Darren alone on Tuesday at half past twelve: who holds it at the end of each day?
//   M4  (run 3) what the town is told: the bridge's table of the prototype's kinds of act (PROTOTYPE_ACTS) against
//       the prototype's own list and numbers (kinds.js). This one is a check: the table is derived, kinds.js is its home.
// M1 to M3 are measurements, not checks: they fail only if they cannot measure.
import { readFileSync, writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { openTown, PROTOTYPE_TO_CAST, PROTOTYPE_ACTS } from '../wasm/one-sim-bridge.mjs';

const arg = (name, dflt) => { const i = process.argv.indexOf('--' + name); return i > 0 ? process.argv[i + 1] : dflt; };
const brain = arg('brain'), specs = arg('specs'), proto = arg('prototype'), jsonOut = arg('json');
if (!brain || !specs || !proto) { console.error('usage: node measure.mjs --brain one-sim.wasm --specs production/specs --prototype <the prototype\'s src folder>'); process.exit(2); }
const P = (f) => import(pathToFileURL(resolve(proto, f)).href);
const { RULES } = await P('rules.js');
const { CAST } = await P('cast.js');
const util = await P('util.js');
const state = await P('state.js');
const routines = await P('routines.js');
const events = await P('events.js');
const gossip = await P('gossip.js');
const clock = await P('clock.js');
const { KINDS } = await P('kinds.js');

const castJson = readFileSync(specs + '/hook-cast.json', 'utf8');
const real = JSON.parse(castJson.replace(/^﻿/, ''));
const wasm = await WebAssembly.compile(readFileSync(brain));
const areaOfPlace = {};
for (const [area, v] of Object.entries(real.areas)) for (const p of v.places) areaOfPlace[p] = area;
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const out = {};

// ---- M1: the nine people both casts hold, hour by hour ------------------------------------------------
// The prototype's places and the cast file's are different lists. This table says which of the prototype's
// stand for which area of the cast file. It was made BY EYE from the names, for the nine people's places only;
// a prototype place with no line here has no counterpart found by name.
const AREA_OF_PROTOTYPE_PLACE = {
  rank: 'mickeys', mickeys: 'mickeys', caff: 'cafe', fish: 'fish_market', chapel: 'chapel', chapelgate: 'chapel', rita: 'ritas', coin: 'hals',
  boarding: 'boarding_house', market1: 'market', ferry2: 'ferry',
};
const protoArea = (where) => (where === 'home' || where === 'off' ? 'away' : AREA_OF_PROTOTYPE_PLACE[where.split(':')[0]] ?? 'no counterpart: ' + where.split(':')[0]);
{
  const town = await openTown({ wasm, castJson, startMinute: 0, print: () => {} });
  const rows = [];
  let all = 0, allSame = 0;
  const noCounterpart = new Set();
  for (const [pid, rid] of Object.entries(PROTOTYPE_TO_CAST)) {
    const def = CAST.find((c) => c.id === pid);
    const person = { def, override: null };
    let same = 0, bothAway = 0, outVsAway = 0, otherPlace = 0, nowhere = 0;
    for (let d = 0; d < 7; d++) for (let h = 0; h < 24; h++) {
      const a = protoArea(routines.slot(person, h + 0.5, d).where);
      const place = town.placeOf(rid, d * 1440 + h * 60 + 30);
      const b = place === 'off' || place === '' ? 'away' : areaOfPlace[place] ?? place;
      if (a.startsWith('no counterpart')) noCounterpart.add(a.slice(16));
      if (a === b) { same++; if (a === 'away') bothAway++; }
      else if (a === 'away' || b === 'away') outVsAway++;
      else if (a.startsWith('no counterpart')) nowhere++;
      else otherPlace++;
    }
    all += 168; allSame += same;
    rows.push({ prototype: pid, cast: rid, name: def.name, sameOf168: same, ofThoseBothAway: bothAway, outInOneAwayInTheOther: outVsAway, differentPlace: otherPlace, prototypePlaceWithNoCounterpart: nowhere });
  }
  out.M1 = { rows, hours: all, same: allSame, prototypePlacesWithNoCounterpart: [...noCounterpart].sort() };
  console.log(`M1 where the nine people of both casts are, at the half of each hour of a week (9 x 168 = ${all} person-hours; places matched by eye, by name):`);
  console.log(`   the same area, or away in both: ${allSame} of ${all} (${(100 * allSame / all).toFixed(0)}%)`);
  for (const r of rows) console.log(`   ${r.name.padEnd(15)} same ${String(r.sameOf168).padStart(3)} of 168 (away in both ${r.ofThoseBothAway}); out in one and away in the other ${r.outInOneAwayInTheOther}; ` +
    `in different places ${r.differentPlace}; at a prototype place with no counterpart ${r.prototypePlaceWithNoCounterpart}`);
  console.log(`   prototype places of theirs with no counterpart found by name: ${out.M1.prototypePlacesWithNoCounterpart.join(', ')}`);
}

// ---- M2: on what minutes people move ---------------------------------------------------------------------
{
  let whole = 0, other = 0;
  for (const c of CAST) for (const s of c.sched) (Number.isInteger(s[0]) ? whole++ : other++);
  let realRows = 0, realOther = 0;
  for (const p of real.people) for (const list of [p.routine, ...Object.values(p.days || {})]) for (const s of list) { realRows++; if (!Number.isInteger(s[0])) realOther++; }
  out.M2 = { prototype: { people: CAST.length, rows: whole + other, onTheHour: whole, atOtherMinutes: other }, real: { people: real.people.length, rows: realRows, atOtherMinutes: realOther } };
  console.log(`M2 when people move: the prototype's ${CAST.length} people have ${whole + other} routine lines, ${whole} on the hour and ${other} at other minutes; ` +
    `the real cast's ${real.people.length} people have ${realRows}, ${realOther} of them off the hour`);
  console.log(`   the prototype's town talks every ${RULES.ticking.gossipEveryGameMinutes} game minutes between people standing within ${RULES.gossip.withinMetresOnStreet} m of each other ` +
    `(${RULES.gossip.withinMetresIndoors} m indoors); the real town every 6, between people their routines put in the same place that hour (the cast file's talking range: ${real.talk_range_m} m)`);
}

// ---- M3: one story, seen by Darren alone on Tuesday at half past twelve ------------------------------
// The prototype's own town, run with nobody watching him (he is kept off the street, as its own skipTo keeps
// him), on its own clock in steps of one real second (1.33 game minutes), twenty times with twenty fixed seeds.
// The real town, run through the bridge by the minute. Both from Monday 15:36 to the end of Sunday.
const START = RULES.time.weekStartsGameMinute, SEEN = 1440 + 12 * 60 + 30, END = 7 * 1440;
const KIND = 'strike';   // the prototype's kind for "he hit somebody": a crime of violence in its table
async function prototypeWeek(seed) {
  util.R.f = util.rng(seed);
  state.resetState();
  const G = state.G;
  G.story.phase = 'play';
  routines.initPeople();
  clock.initEnv();
  G.tom.space = 'away';
  let E = null;
  const ends = [];
  let nextEnd = 1440;
  const step = 1, perStep = (step * 60) / state.SECS_PER_HOUR;
  for (let guard = 0; G.t < END && guard < 100000; guard++) {
    clock.simStep(step);
    if (!E && G.t >= SEEN) {
      E = events.mkEvent(KIND, { zone: 'Quay Street', name: 'a man' });
      events.remember(G.people.darren, E, { src: 'saw', who: 'tom', sure: 1, heat: Math.min(1, KINDS[KIND].sev + RULES.seeing.heatAddedToSeverity), face: 1 });
    }
    if (G.t >= nextEnd - perStep / 2) {
      const holders = E ? G.named.filter((p) => p.mind.by[E.id]) : [];
      ends.push({ day: nextEnd / 1440 - 1, all: holders.length, nine: holders.filter((p) => PROTOTYPE_TO_CAST[p.id]).length, namesHim: holders.filter((p) => p.mind.by[E.id].who === 'tom').length });
      nextEnd += 1440;
    }
  }
  return ends;
}
{
  const seeds = Array.from({ length: 20 }, (_, i) => 1990 + i);
  const runs = [];
  const t0 = performance.now();
  for (const s of seeds) runs.push(await prototypeWeek(s));
  const protoMs = performance.now() - t0;
  const town = await openTown({ wasm, castJson, startMinute: START, print: () => {} });
  const realEnds = [];
  let done = false;
  for (let t = START; t <= END; t++) {
    town.tick(t, 'mickeys');
    if (!done && t === SEEN) { done = town.saw({ minute: t, who: 'darren', rung: 4, fact: 'strike_d1', area: 'mickeys', words: 'the new owner hit a man on Quay Street', certainty: 1 }); }
    if (t % 1440 === 0 && t > START) {
      const holders = new Set(town.knows().filter((f) => f.topic === 'player.strike_d1').map((f) => f.who));
      const names = town.knows().filter((f) => f.topic === 'player.strike_d1' && f.names).length;
      realEnds.push({ day: t / 1440 - 1, all: holders.size, nine: [...holders].filter((id) => Object.values(PROTOTYPE_TO_CAST).includes(id)).length, namesHim: names });
    }
  }
  const stat = (day, key) => { const v = runs.map((r) => r[day][key]).sort((a, b) => a - b); return { least: v[0], middle: v[Math.floor(v.length / 2)], most: v[v.length - 1] }; };
  out.M3 = { kind: KIND, seenAtMinute: SEEN, seeds: seeds.length, taken: done, prototype: DAYS.map((d, i) => ({ day: d, all: stat(i, 'all'), nine: stat(i, 'nine'), namesHim: stat(i, 'namesHim') })), real: realEnds.map((e) => ({ ...e, day: DAYS[e.day] })),
    prototypeNamed: CAST.length, prototypeWhoCanHear: CAST.filter((c) => !c.police).length, realPeople: real.people.length, prototypeMsPerWeek: Math.round(protoMs / seeds.length) };
  console.log(`M3 one story (he hit a man), seen by Darren alone on Tuesday at 12:30, nobody watching him after: how many hold it at the end of each day`);
  console.log(`   the real town took the sighting: ${done}`);
  console.log(`   day   prototype, of its ${CAST.length} named (least / middle / most of ${seeds.length} seeded weeks)   real rules, of its ${real.people.length}   | of the nine in both: prototype middle, real`);
  DAYS.forEach((d, i) => { const p = out.M3.prototype[i], r = out.M3.real[i]; console.log(`   ${d}   ${String(p.all.least).padStart(2)} / ${String(p.all.middle).padStart(2)} / ${String(p.all.most).padStart(2)}`.padEnd(70) + `${String(r.all).padStart(2)}`.padEnd(28) + `| ${p.nine.middle}, ${r.nine}`); });
  const last = out.M3.prototype[6];
  console.log(`   by the end of Sunday, of those who hold it, those whose copy names him: prototype ${last.namesHim.least} / ${last.namesHim.middle} / ${last.namesHim.most}; real rules ${out.M3.real[6].namesHim} of ${out.M3.real[6].all}`);
  console.log(`   (the prototype's week took ${out.M3.prototypeMsPerWeek} ms a run here)`);
  console.log(`   of the prototype's ${CAST.length} named people, ${out.M3.prototypeWhoCanHear} can hear a story at all: its talk leaves out the ${CAST.length - out.M3.prototypeWhoCanHear} police (${CAST.filter((c) => c.police).map((c) => c.name).join(', ')})`);
}

// ---- M4: what the town is told --------------------------------------------------------------------------
// The bridge's table against the prototype's own list: every kind has a row and no row is left over; a kind told
// as a sighting reads badly in the prototype's own numbers (below 0), since the town keeps every sighting as about
// his hidden life; a kind marked open reads 0 or better. Printed grouped, as DIFFERENCES.md prints it.
let tableFaults = 0;
{
  const kinds = Object.keys(KINDS), rows = Object.keys(PROTOTYPE_ACTS);
  const missing = kinds.filter((k) => !PROTOTYPE_ACTS[k]), left = rows.filter((k) => !KINDS[k]);
  const wrong = kinds.filter((k) => PROTOTYPE_ACTS[k] && ((PROTOTYPE_ACTS[k].tell === 'saw' && !(KINDS[k].val < 0)) || (PROTOTYPE_ACTS[k].tell === 'open' && !(KINDS[k].val >= 0))));
  tableFaults = missing.length + left.length + wrong.length;
  const by = {};
  for (const k of kinds) if (PROTOTYPE_ACTS[k]) (by[PROTOTYPE_ACTS[k].tell] ??= []).push(k);
  out.M4 = { kinds: kinds.length, rows: rows.length, missing, left, wrong, by, crimes: kinds.filter((k) => KINDS[k].crime >= 2), damage: kinds.filter((k) => PROTOTYPE_ACTS[k]?.tell === 'deed') };
  console.log(`M4 what the town is told: the prototype knows ${kinds.length} kinds (kinds.js); the bridge's table has ${rows.length} rows; ` +
    `${missing.length} kinds without a row${missing.length ? ' (' + missing.join(', ') + ')' : ''}, ${left.length} rows without a kind${left.length ? ' (' + left.join(', ') + ')' : ''}, ` +
    `${wrong.length} against the rule (a sighting reads below 0, an open act 0 or better)${wrong.length ? ' (' + wrong.join(', ') + ')' : ''}`);
  for (const tell of ['saw', 'step', 'open', 'none', 'never', 'deed']) if (by[tell]) console.log(`   ${tell.padEnd(5)} ${String(by[tell].length).padStart(2)}: ${by[tell].map((k) => k + (PROTOTYPE_ACTS[k].by ? ' [' + PROTOTYPE_ACTS[k].by + ']' : '')).join(', ')}`);
  console.log(`   the prototype's crimes of violence or worse (crime level 2 and 3): ${out.M4.crimes.join(', ')}; kinds that are damage to a thing: ${out.M4.damage.length ? out.M4.damage.join(', ') : 'none'}`);
  if (tableFaults) console.log('FAIL M4: the table of kinds and the prototype\'s own list disagree');
}
if (jsonOut) writeFileSync(jsonOut, JSON.stringify(out, null, 1));
console.log(tableFaults ? 'one-sim differences: measured, and the table of kinds is WRONG' : 'one-sim differences: measured');
process.exit(tableFaults ? 1 : 0);
