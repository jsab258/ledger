// ONE SIMULATION IN THE BROWSER: the breaker (run 3, 19 November 2026).
//
//   node breaker.mjs --brain one-sim.wasm --specs production/specs [--json OUT.json]
//
// Tries to make the bridge misbehave, the way a careless page or a spoiled save would: bad calls,
// ticks out of order, saves with pieces wrong. Each try names what a sound bridge does (refuses
// with a reason, or answers a stated thing) and is marked "held" or "NOT HELD". After every refused
// call the town must be as it was: its save is compared before and after.
// A measurement kept beside the checks (one-sim.sh breaker); T11 and T12 are the gate. What this
// run found is recorded in PROGRESS.md.
import { readFileSync, writeFileSync } from 'node:fs';
import { openTown, openTownFromOldSave, NightAnswer, WeekAnswer } from './one-sim-bridge.mjs';

const arg = (name) => { const i = process.argv.indexOf('--' + name); return i > 0 ? process.argv[i + 1] : undefined; };
if (!arg('brain') || !arg('specs')) { console.error('usage: node breaker.mjs --brain one-sim.wasm --specs production/specs [--json OUT.json]'); process.exit(2); }
const wasm = await WebAssembly.compile(readFileSync(arg('brain')));
const cast = readFileSync(arg('specs') + '/hook-cast.json', 'utf8'), quay = readFileSync(arg('specs') + '/quay-cast.json', 'utf8');
const quiet = () => {};
const open = (more = {}) => openTown({ wasm, castJson: cast, startMinute: 936, print: quiet, ...more });   // Monday 15:36
const TUE = 1440 + 12 * 60 + 30;
const windowDeed = (minute, more = {}) => ({ minute, area: 'ritas', thing: 'rita_window', said: "somebody put Rita's window in", witnesses: [{ id: 'darren', rung: 4 }],
  fact: 'window_d1', words: "the new owner put Rita's window in", ...more });
const sighting = (minute, more = {}) => ({ minute, who: 'ron', rung: 3, fact: 'seen_d1', area: 'mickeys', words: 'Ron saw him on the rank', ...more });

const rows = [], brief = process.argv.includes('--brief');   // --brief: only what did not hold, and the count
let group = '';
const note = (what, held, detail) => { rows.push({ group, what, held, detail }); if (!held || !brief) console.log(`  ${held ? 'held    ' : 'NOT HELD'} ${what}${detail ? ': ' + detail : ''}`); };
const say = (line) => { if (!brief) console.log(line); };
/// Must be refused, with these words in the reason; and if a town is given, it must be unchanged after.
async function refused(what, fn, word, town) {
  const was = town ? JSON.stringify(town.save()) : null;
  try { const got = await fn(); note(what, false, `taken, and answered ${String(JSON.stringify(got)).slice(0, 80)}`); }
  catch (e) {
    const msg = String(e && e.message);
    if (!msg.startsWith('one-sim bridge:') && !msg.includes('cast not read') && !msg.includes('not a whole') && !msg.includes('version')) note(what, false, `fell over instead of refusing: ${msg.slice(0, 120)}`);
    else if (word && !msg.includes(word)) note(what, false, `refused, but with other words: ${msg.slice(0, 120)}`);
    else if (town && JSON.stringify(town.save()) !== was) note(what, false, 'refused, but the town was changed by it');
    else note(what, true, msg.replace('one-sim bridge: ', '').slice(0, 96));
  }
}
/// Must answer, and the answer must be this.
async function answers(what, fn, good, say = (x) => String(JSON.stringify(x)).slice(0, 96)) {
  try { const got = await fn(); note(what, !!good(got), say(got)); }
  catch (e) { note(what, false, `fell over: ${String(e && e.message).slice(0, 120)}`); }
}

// ------------------------------------------------------------------------------------------------
group = 'opening'; say('[1] OPENING THE TOWN');
await refused('no arguments at all', () => openTown(), 'no cast file');
await refused('a list for its arguments', () => openTown([1, 2]), 'openTown takes');
await refused('a cast file that is a number', () => openTown({ wasm, castJson: 41 }), 'no cast file');
await refused('a cast file that is a list', () => openTown({ wasm, castJson: '[1,2,3]' }), 'cast not read');
await refused('a way of talking it does not know', () => open({ talk: 'now and then' }), 'talk is');
for (const [what, m] of [['no number', NaN], ['a minus', -1], ['no end', Infinity], ['text', '936'], ['past the last minute a town can be saved at', 6e8], ['nothing (null)', null]])
  await refused(`a start minute that is ${what}`, () => open({ startMinute: m }), 'week starts');
await answers('a start a thousand years on is taken (the town can live that long) and ticks', async () => { const t = await open({ startMinute: 1000 * 366 * 1440 + 30 }); return [t.tick(1000 * 366 * 1440 + 90).length, t.save().at]; }, (g) => g[0] === 1);
await refused('a saved town asked for and not there (undefined)', () => openTown({ wasm, castJson: cast, saved: undefined }), 'no saved town');
await refused('a saved town asked for and not there (null)', () => openTown({ wasm, castJson: cast, saved: null }), 'no saved town');
try { await openTown({ wasm: new Uint8Array([1, 2, 3, 4]), castJson: cast }); note('bytes that are no simulation file', false, 'taken'); }
catch (e) { note('bytes that are no simulation file', true, 'the browser itself refuses them: ' + String(e.message).slice(0, 60)); }
await answers('the quay cast, which names no areas, opens and ticks with any area', async () => { const t = await openTown({ wasm, castJson: quay, startMinute: 0, print: quiet }); return t.tick(180, 'anywhere').length; }, (n) => n === 4);

// ------------------------------------------------------------------------------------------------
group = 'the clock'; say('[2] THE CLOCK, OUT OF ORDER');
{
  const t = await open();
  await answers('the same minute ticked three times runs no hour twice', () => [t.tick(960).length, t.tick(960).length, t.tick(960.9).length], (g) => g.join() === '1,0,0');
  await answers('a clock that falls back inside its minute is followed', () => t.tick(960.1).length, (n) => n === 0);
  await refused('a clock one minute back', () => t.tick(959), 'went back', t);
  for (const [what, v] of [['text', '1000'], ['nothing', undefined], ['null', null], ['a list', [1000]], ['no number', NaN], ['minus infinity', -Infinity]]) await refused(`a clock that is ${what}`, () => t.tick(v), '', t);
  await refused('a jump of a year and a minute', () => t.tick(960 + 366 * 1440 + 1), 'more than a year', t);
  for (const [what, a] of [['an empty name', ''], ['a number', 7], ['null', null], ['a list', ['mickeys']], ["the prototype's own street name", 'Quay Street'], ['a place, not an area', 'mickeys_rank']])
    await refused(`a tick where he stands in ${what}`, () => t.tick(961, a), 'no area', t);
  await answers('a tick called again from inside the handling of its own hours gives each hour once', () => {
    const seen = [];
    for (const h of t.tick(1200)) { seen.push(h.hour); for (const inner of t.tick(1320)) seen.push(inner.hour); }   // the page skips the clock on from inside its loop
    return seen;
  }, (g) => [...g].sort((a, b) => a - b).join() === '17,18,19,20,21,22' && new Set(g).size === g.length, (g) => `hours came as ${g.join(', ')} (each once; the later ones first, as BRIDGE.md warns)`);
  await answers('a jump of exactly a year is followed', () => t.tick(1320 + 366 * 1440).length, (n) => n === 366 * 24);
}
{
  const t = await open();
  await answers('an hour is crossed on its stroke, not before', () => [t.tick(959.999).length, t.tick(960).length], (g) => g.join() === '0,1');
  await refused('an act at a minute the clock has passed', () => t.saw(sighting(940)), 'before the town', t);
  await refused('an act in an hour not yet run', () => t.saw(sighting(1021)), 'tick the clock', t);
  await answers('an act later in the hour that has run, then the clock at that minute', () => { const ok = t.saw(sighting(1010)); return [ok, t.now(), t.tick(1010).length]; }, (g) => g.join() === 'true,1010,0');
  await refused('then the clock before that act', () => t.tick(1005), 'went back', t);
}

// ------------------------------------------------------------------------------------------------
group = 'bad calls'; say('[3] BAD CALLS');
{
  const t = await open();
  t.tick(TUE);
  await refused('a deed with no arguments', () => t.deed(), '', t);
  await refused('a deed that is null', () => t.deed(null), '', t);
  for (const [what, more] of [['no place', { area: undefined }], ['no thing', { thing: undefined }], ['words that are a number', { words: 5 }], ['no story name', { fact: undefined }],
    ['a story name with a bar and a comma in it', { fact: 'x|y,z' }], ['a story name with a line break', { fact: 'a\nb' }], ['a story name 2,000 letters long', { fact: 'a'.repeat(2000) }],
    ["a story name the town's own rules use (the week's end)", { fact: 'week_d6' }], ["a story name the town's own rules use (his name)", { fact: 'name' }],
    ['witnesses that are text', { witnesses: 'darren:4' }], ['a witness that is null', { witnesses: [null] }], ['a witness whose id is a number', { witnesses: [{ id: 7, rung: 4 }] }],
    ['a witness at rung 9', { witnesses: [{ id: 'darren', rung: 9 }] }], ['a witness at rung 1.5', { witnesses: [{ id: 'darren', rung: 1.5 }] }], ['a witness whose rung is text', { witnesses: [{ id: 'darren', rung: '4' }] }],
    ['a certainty of nought', { certainty: 0 }], ['a certainty of two', { certainty: 2 }], ['a certainty that is no number', { certainty: NaN }], ['a certainty that is text', { certainty: '1' }],
    ['a minute that is no number', { minute: NaN }], ['a minute that is text', { minute: String(TUE) }],
    ['a thing with no name', { thing: '' }], ['a thing named with spaces only', { thing: '   ' }], ['nothing said of the damage', { said: '' }], ['a story with no words', { words: '' }]])
    await refused(`a deed with ${what}`, () => t.deed(windowDeed(TUE, more)), '', t);
  await answers("a deed seen by ids that are JavaScript's own words takes nobody, and such an id has no place and sees nothing", async () => {
    const o = await open(); o.tick(TUE);
    const got = o.deed(windowDeed(TUE, { witnesses: [{ id: 'constructor', rung: 4 }, { id: '__proto__', rung: 4 }, { id: 'toString', rung: 1 }] }));
    return [got.taken.length, got.dropped.length, o.placeOf('constructor'), o.placeOf('toString'), o.saw(sighting(TUE, { who: 'hasOwnProperty' }))];
  }, (g) => g.join('|') === '0|3|||false');
  await answers('a deed whose witness id tries to smuggle in a second witness is taken with nobody seeing it', () => t.deed(windowDeed(TUE, { witnesses: [{ id: 'sam:4,rita', rung: 4 }] })),
    (g) => g.taken.length === 0 && g.dropped.length === 1 && t.deedHeld().witnesses.length === 0);
  await refused('a second deed', () => t.deed(windowDeed(TUE, { fact: 'window2_d1' })), 'one deed', t);
  for (const [what, more] of [['nobody', { who: undefined }], ['a number for who saw it', { who: 12 }], ['rung 5', { rung: 5 }], ['no words', { words: undefined }], ['empty words', { words: '' }], ['no place', { area: null }],
    ["a story name of the town's own", { fact: 'taken_d1' }], ['a certainty below nought', { certainty: -0.5 }]])
    await refused(`a sighting with ${what}`, () => t.saw(sighting(TUE, more)), '', t);
  await answers('a sighting by somebody the cast does not have is answered false and changes nothing', () => { const was = JSON.stringify(t.save()); return [t.saw(sighting(TUE, { who: 'pauline' })), JSON.stringify(t.save()) === was]; }, (g) => g.join() === 'false,true');
  await answers('odd and long words are carried whole', () => {
    const words = 'é|~^\n"\\\u{1F600}'.repeat(500);
    t.saw(sighting(TUE, { fact: 'odd_d1', words }));
    return t.knows().find((f) => f.topic === 'player.odd_d1').said === words;
  }, (g) => g === true);
  for (const [what, a] of [['an answer outside the list', [0, 9, TUE]], ['a night that is no number', [NaN, NightAnswer.Did, TUE]], ['a night before the first', [-1, NightAnswer.Did, TUE]]])
    await answers(`an answer to the ask with ${what} is not taken and changes nothing`, () => { const was = JSON.stringify(t.save().texts.town); return [t.answerAsk(...a), JSON.stringify(t.save().texts.town) === was]; }, (g) => g.join() === 'false,true');
  await refused('an answer to the ask at a minute that is no number', () => t.answerAsk(0, NightAnswer.Did, NaN), 'he does things', t);
  await refused("a minute at Ada's tea that is no number", () => t.teaMinute(NaN), 'he does things', t);
  await refused("a minute at Ada's tea a day ahead", () => t.teaMinute(TUE + 1440), 'tick the clock', t);
  await refused("Sheila's question a day ahead", () => t.weekAsk(TUE + 1440), 'tick the clock', t);
  await answers("Sheila's question on a Tuesday is not taken and changes nothing", () => { const was = JSON.stringify(t.save()); return [t.weekAsk(TUE), JSON.stringify(t.save()) === was]; }, (g) => g.join() === 'false,true');
  await answers('an answer to a question she has not asked is not taken', () => [t.weekGive(WeekAnswer.TakeOver, TUE), t.weekGive(7, TUE), t.weekGive(NaN, TUE)], (g) => g.join() === 'false,false,false');
  await answers('where somebody is, asked oddly, answers a place or nothing', () => [t.placeOf(undefined), t.placeOf('ron', NaN), t.placeOf('ron', -5), t.placeOf('ron', 1e15), t.placeOf(7)], (g) => g.every((v) => typeof v === 'string'));
  await answers('after all of that the town still plays on to the arrest', () => { const hs = t.tick(3 * 1440 + 11 * 60); return [hs.filter((e) => e.went.length).length, hs.filter((e) => e.taken).length]; }, (g) => g.join() === '0,0',
    (g) => `statements at ${g[0]} hour(s), arrests at ${g[1]}: nobody saw the deed (its only witness was the smuggled id), so nobody went`);
}
{
  const a = await open(), b = await open();
  a.tick(TUE); a.deed(windowDeed(TUE));
  await answers('two towns open at once do not touch each other', () => [a.deedHeld() !== null, b.deedHeld(), b.now()], (g) => g[0] === true && g[1] === null && g[2] === 936);
}

// ------------------------------------------------------------------------------------------------
group = 'saves'; say('[4] SPOILED SAVES');
{
  const t = await open();
  t.tick(TUE); t.deed(windowDeed(TUE)); t.tick(2 * 1440 + 10 * 60 + 12);
  const good = JSON.parse(JSON.stringify(t.save()));
  const load = (saved, more = {}) => openTown({ wasm, castJson: cast, saved, print: quiet, ...more });
  const copy = () => JSON.parse(JSON.stringify(good));
  await answers('the save itself loads, and saves again the same', async () => JSON.stringify((await load(copy())).save()) === JSON.stringify(good), (g) => g === true);
  for (const key of ['kind', 'v', 'cast', 'at', 'nextHour', 'talk', 'texts']) await refused(`a save without its "${key}"`, () => { const s = copy(); delete s[key]; return load(s); }, '');
  for (const key of ['agents', 'town', 'week', 'memories']) await refused(`a save without its texts' "${key}"`, () => { const s = copy(); delete s.texts[key]; return load(s); }, '');
  for (const [what, v] of [['text', JSON.stringify(good)], ['a list', [good]], ['a number', 7], ['true', true]]) await refused(`a save that is ${what}`, () => load(v), 'not a saved town');
  for (const v of [0, -1, 1.5, '1', NaN, 99]) await refused(`a save of version ${JSON.stringify(v)}`, () => load({ ...copy(), v }), v === 1.5 || v === '1' ? '' : 'version');
  for (const [what, change] of [['next hour 0', { nextHour: 0 }], ['next hour 100 on', { nextHour: good.nextHour + 100 }], ['next hour as text', { nextHour: String(good.nextHour) }], ['a minute with a fraction', { at: good.at + 0.5 }],
    ['a minus minute', { at: -5, nextHour: 0 }], ['minute 10 to the 12th', { at: 1e12, nextHour: Math.floor(1e12 / 60) + 1 }], ['its clock ten hours back, next hour in step', { at: good.at - 600, nextHour: good.nextHour - 10 }],
    ['its clock a hundred hours on, next hour in step', { at: good.at + 6000, nextHour: good.nextHour + 100 }], ['its clock one hour on, next hour in step', { at: good.at + 60, nextHour: good.nextHour + 1 }],
    ['a way of talking it does not know', { talk: 'now and then' }], ['another cast mark', { cast: '00000000' }]])
    await refused(`a save with ${what}`, () => load({ ...copy(), ...change }), '');
  const texts = (change) => ({ ...copy(), texts: { ...copy().texts, ...change } });
  for (const [what, change] of [['its talk an empty object', { agents: '{}' }], ['its talk cut short', { agents: good.texts.agents.slice(0, 300) }], ['its talk cut short, braces closed', { agents: good.texts.agents.slice(0, 300) + '}' }],
    ['its talk with one person taken out', { agents: good.texts.agents.replace('"id":"sam"', '"id":"sam_gone"') }],
    ["its week's pieces an empty object", { town: '{}' }], ["its week's pieces a list", { town: '[]' }], ["its week's pieces from a later version", { town: good.texts.town.replace('"version":2', '"version":99') }],
    ["its week's pieces without the hours talked", { town: good.texts.town.replace(/"hours":\{[^}]*\},/, '') }],
    ['its lines beside the week no JSON', { week: 'not json' }], ['its lines beside the week a list', { week: '[]' }], ['its lines beside the week null', { week: 'null' }],
    ['every memory gone', { memories: {} }], ['one memory gone', { memories: (() => { const m = { ...good.texts.memories }; delete m.sam; return m; })() }], ['one memory a number', { memories: { ...good.texts.memories, sam: 7 } }],
    ['a memory for somebody not in the cast', { memories: { ...good.texts.memories, pauline: '# Memory: pauline\n' } }],
    ["two people's memories changed over", { memories: { ...good.texts.memories, sam: good.texts.memories.rita, rita: good.texts.memories.sam } }],
    ['a memory that is no memory text', { memories: { ...good.texts.memories, sam: 'hello' } }]])
    await refused(`a save with ${what}`, () => load(texts(change)), '');
  const weekWith = (change) => texts({ week: JSON.stringify({ ...JSON.parse(good.texts.week), ...change }) });
  for (const [what, change] of [["its deed's witnesses spoiled", { witnesses: [[1, 2], 'x', null, ['sam', 4]] }], ["its deed's witnesses text", { witnesses: 'sam:4' }], ["its deed's day text", { deedDay: 'Tuesday' }],
    ["its deed's minute a fraction", { deedAt: 2190.5 }], ['her first visit a number', { ellisFirst: 3 }]])
    await refused(`a save with ${what}`, () => load(weekWith(change)), 'do not read');
  await refused('a save loaded with the quay cast', () => openTown({ wasm, castJson: quay, saved: copy(), print: quiet }), 'another cast');
  await answers('a save loaded with the cast file as Windows writes it (a byte-order mark, CRLF) plays on the same', async () => {
    const a = await load(copy()), b = await load(copy(), { castJson: '﻿' + cast.replace(/\r?\n/g, '\r\n') });
    a.tick(4 * 1440); b.tick(4 * 1440);
    return JSON.stringify(a.save()) === JSON.stringify(b.save());
  }, (g) => g === true);
  await answers('a save made by the hour keeps its way of talking after the load', async () => {
    const h = await open({ talk: 'by the hour' }); h.tick(TUE);
    return (await load(JSON.parse(JSON.stringify(h.save())))).talk();
  }, (g) => g === 'by the hour');
  await answers('the town that made the save is untouched by all of the above', () => JSON.stringify(t.save()) === JSON.stringify(good), (g) => g === true);
}

// ------------------------------------------------------------------------------------------------
group = 'old saves'; say('[5] SAVES FROM BEFORE THE SWAP');
{
  const oldOpen = (old, more = {}) => openTownFromOldSave({ wasm, castJson: cast, old, print: quiet, ...more });
  const mem = (e, src, who, sure, face) => ({ e, src, from: null, who, sure, heat: 0.6, t: 100, said: false, hop: 0, face });
  const base = { v: 7, t: 2 * 1440 + 14 * 60, events: [{ id: 1, kind: 'strike', t: 2000, zone: 'Quay Street', wit: ['darren'] }], minds: { darren: { fam: 0.7, mem: [mem(1, 'saw', 'tom', 0.9, 0.5)] } } };
  for (const [what, old] of [['nothing', undefined], ['null', null], ['text', JSON.stringify(base)], ['a list', []], ['no clock', { ...base, t: undefined }], ['a minus clock', { ...base, t: -3 }],
    ['minds that are a list', { ...base, minds: [] }], ['events that are an object', { ...base, events: {} }]])
    await refused(`an old save that is ${what}`, () => oldOpen(old), 'not a prototype save');
  await answers('an old save whose minds and events are full of odd things opens, tells what it can and names the rest', async () => {
    const odd = { ...base, events: [...base.events, null, 7, { id: 'x', kind: 'strike' }, { id: 2, kind: 5 }, { id: 3, kind: '__proto__', t: 5 }, { id: 4, kind: 'strike', t: 'soon' }],
      minds: { darren: { mem: [mem(1, 'saw', 'tom', 0.9, 0.5), null, 5, mem(2, 'saw', 'tom', 1, 1), mem(3, 'saw', 'tom', 1, 1), mem(4, 'saw', 'tom', NaN, 1), mem(1, 'dreamt', 'tom', 1, 1)] },
        rita: null, hal: { mem: 'x' }, __proto__: { mem: [] }, ron: { mem: [{ e: 1, src: 'saw', who: {}, sure: '0.9', face: 'x' }] } } };
    const r = await oldOpen(odd);
    return [r.fed.length, r.dropped.length, r.town.knows().filter((f) => f.saw).length];
  }, (g) => g[0] === 1 && g[2] === 1, (g) => `${g[0]} told, ${g[1]} left out with a reason, ${g[2]} first-hand in the town`);
  await answers('an old save with ten thousand memories opens (the time is a measurement, not a limit)', async () => {
    const events = [], mems = [];
    for (let i = 0; i < 10000; i++) { events.push({ id: i, kind: i % 2 ? 'strike' : 'ran', t: i, zone: 'Quay Street' }); mems.push(mem(i, 'saw', 'tom', 0.9, 0.5)); }
    const t0 = performance.now();
    const r = await oldOpen({ ...base, events, minds: { darren: { mem: mems } } });
    return [r.fed.length, Math.round(performance.now() - t0), JSON.stringify(r.town.save()).length];
  }, (g) => g[0] === 10000, (g) => `${g[0]} told in ${g[1]} ms; the town's save is then ${g[2]} characters`);
  await refused('an old save past the last minute a town can be saved at', () => oldOpen({ ...base, t: 7e8 }), 'week starts');
}

// ------------------------------------------------------------------------------------------------
// The checks on a save must never refuse a sound one. A town is saved at each of these moments, loaded into a fresh
// module from the save's text, and both are played on to the same later minute: they must end as the same town.
group = 'awkward moments'; say('[6] A SOUND SAVE AT AN AWKWARD MOMENT LOADS AND PLAYS ON THE SAME');
{
  const WED = 2 * 1440, SUN = 6 * 1440;
  const moments = [
    ['just opened on the stroke of an hour, before that hour ran', { startMinute: 960 }, () => {}, 2000],
    ['just opened inside an hour, never ticked', { startMinute: 936 }, () => {}, 2000],
    ['just opened at minute nought', { startMinute: 0 }, () => {}, 1000],
    ['opened inside an hour and ticked on inside it', {}, (t) => { t.tick(950.5); }, 2000],
    ['on the stroke of an hour, after it ran', {}, (t) => { t.tick(1200); }, 2500],
    ['one minute before an hour', {}, (t) => { t.tick(1199); }, 2500],
    ['right after a deed, before the next tick', {}, (t) => { t.tick(TUE); t.deed(windowDeed(TUE)); }, 3 * 1440 + 700],
    ['right after a sighting later in the hour than the clock', {}, (t) => { t.tick(TUE); t.saw(sighting(TUE + 20)); }, 3 * 1440],
    ["after a no to Ron's ask", {}, (t) => { t.tick(21 * 60 + 30); t.answerAsk(0, NightAnswer.Refused, 21 * 60 + 30); }, 3 * 1440],
    ["in the middle of Ada's tea", {}, (t) => { t.tick(WED + 21 * 60); for (let m = 0; m < 25; m++) { t.tick(WED + 21 * 60 + m); t.teaMinute(WED + 21 * 60 + m); } }, 4 * 1440],
    ['while he is held in the cells', {}, (t) => { t.tick(TUE); t.deed(windowDeed(TUE)); t.tick(3 * 1440 + 11 * 60 + 7); if (!t.held()) throw new Error('he is not held'); }, 4 * 1440 + 600],
    ["after Sheila's question, before his answer", { startMinute: SUN + 9 * 60 }, (t) => { t.tick(SUN + 10 * 60 + 30); if (!t.weekAsk(SUN + 10 * 60 + 30)) throw new Error('she did not ask'); }, 7 * 1440 + 300],
    ['after his answer at the week\'s end', { startMinute: SUN + 9 * 60 }, (t) => { t.tick(SUN + 10 * 60 + 30); t.weekAsk(SUN + 10 * 60 + 30); t.tick(SUN + 10 * 60 + 40); t.weekGive(WeekAnswer.WindDown, SUN + 10 * 60 + 40); }, 7 * 1440 + 300],
    ['after a thirty-day jump', {}, (t) => { t.tick(30 * 1440 + 5); }, 31 * 1440],
    ['a town made from an old save, right after it opened', 'old', () => {}, 4 * 1440],
  ];
  for (const talk of ['by the minute', 'by the hour']) for (const [what, how, play, until] of moments) {
    await answers(`saved ${what} (talk ${talk})`, async () => {
      const make = async () => (how === 'old'
        ? (await openTownFromOldSave({ wasm, castJson: cast, talk, print: quiet, old: { t: 2 * 1440 + 14 * 60, events: [{ id: 1, kind: 'strike', t: 2000 }], minds: { darren: { mem: [{ e: 1, src: 'saw', who: 'tom', sure: 0.9, face: 0.5 }] } } } })).town
        : open({ talk, ...how }));
      const straight = await make(), saved = await make();
      play(straight); play(saved);
      const text = JSON.stringify(saved.save());
      const loaded = await openTown({ wasm, castJson: cast, saved: JSON.parse(text), print: quiet });
      const again = JSON.stringify(loaded.save()) === text;
      const a = straight.tick(until).map((e) => e.row).join('\n'), b = loaded.tick(until).map((e) => e.row).join('\n');
      return [again, a === b, JSON.stringify(straight.save()) === JSON.stringify(loaded.save())];
    }, (g) => g.join() === 'true,true,true', (g) => `saves again the same: ${g[0]}; the same hours after: ${g[1]}; the same town at the end: ${g[2]}`);
  }
}

const notHeld = rows.filter((r) => !r.held);
if (arg('json')) writeFileSync(arg('json'), JSON.stringify({ tries: rows.length, held: rows.length - notHeld.length, notHeld, byGroup: Object.fromEntries([...new Set(rows.map((r) => r.group))].map((g) => [g, rows.filter((r) => r.group === g).length])) }, null, 1));
const groups = [...new Set(rows.map((r) => r.group))].map((g) => `${g} ${rows.filter((r) => r.group === g).length}`).join(', ');
console.log(`${notHeld.length ? 'FAIL' : 'ok  '} breaker: ${rows.length} tries to make the bridge misbehave (${groups}): ${rows.length - notHeld.length} held, ${notHeld.length} NOT HELD`);
process.exit(notHeld.length ? 1 : 0);
