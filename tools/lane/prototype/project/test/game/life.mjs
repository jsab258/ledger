// The life system: the calendar (2.1.6, ER-CAL-01 and 02), who is out (2.1.2, 2.1.4, ER-NIGHT-03), lines by regard,
// rung and situation (2.12.4, 3.6.4, ER-TALK-02), the paper and letters (2.4.5, 6.10, ER-PAPER-01), happenings (3.7,
// ER-HAPPEN-01), side stories (3.3), calls (3.2.7, 3.2.5), the boxing club (7.16, ER-PASTIME-01), town marks (2.19),
// teaching (6.5, ER-FIRST-03) and always something to do (7.12, ER-CORE-07).
import { launch } from '../harness.mjs';
import { GREET_BY, CROWD_LINES, CALENDAR_LINES, OWN_STREET, allNewLines } from '../../src/game/life_lines.js';
import fs from 'fs';
let bad = 0;
const ok = (c, m) => { console.log((c ? 'ok   ' : 'TEST FAIL ') + m); if (!c) bad++; };

// ---------- the written lines, with no browser: the content gate and the counts ----------
// canon's content rule: no alcohol, no gambling, no children; nothing later than 1990; no em-dashes
const BANNED = /\b(beer|ale|lager|pint|pints|whisky|gin|rum|drunk|drink|drinks|drinking|boozer?|bar|wine|sober|hangover|bet|bets|betting|bookie|bookies|bookmaker|wager|odds|gamble|gambling|casino|lottery|raffle|bingo|pools|fruit machine|kid|kids|child|children|boy|boys|girl|girls|baby|babies|toddler|pram|schoolboy|schoolgirl|pupil|pupils|mobile|internet|email|text me|website|euro|euros)\b/i;
const lines = allNewLines();
// and every written word of the happenings, stories, calls, shops and places: the source's own lines, comments left out
const SRC = ['life.js', 'life_happenings.js', 'life_stories.js', 'life_people.js', 'shops.js', 'way.js', 'way_places.js', 'kinds/life.js', 'kinds/shops.js', 'cast/life.js', 'tune/shops.js'];
const texts = lines.concat(SRC.flatMap((f) => fs.readFileSync(new URL('../../src/game/' + f, import.meta.url), 'utf8').split('\n').filter((l) => !/^\s*\/\//.test(l)).map((l) => l.replace(/\/\/.*$/, ''))));
const hits = texts.filter((t) => BANNED.test(t));
ok(hits.length === 0, `ER-CAL-02 and the content rule: ${texts.length} written lines, none with drink, gambling, children or anything later than 1990 ${JSON.stringify(hits.slice(0, 5))}`);
ok(texts.every((t) => !/[—–]/.test(t)), 'no em-dashes in any line');
const few = [];
for (const sit in CROWD_LINES) for (const k of ['om', 'ow', 'ym', 'yw']) if ((CROWD_LINES[sit][k] || []).length < 6) few.push(sit + '/' + k);
ok(few.length === 0, '3.6.4: at least 6 lines per situation per kind of speaker (' + Object.keys(CROWD_LINES).length + ' situations, 4 kinds) ' + few);
const thin = [];
for (const kind in GREET_BY) for (const r of ['nephew', 'owner', 'firm', 'port']) if ((GREET_BY[kind][r] || []).length < 3) thin.push(kind + '/' + r);
ok(thin.length === 0 && Object.keys(GREET_BY).length === 5, '2.12.4: greetings for afraid, angry, likes, his appearance and neutral, at each of the four rungs ' + thin);
ok(['nephew', 'owner', 'firm', 'port'].every((r, i, a) => a.every((q) => q === r || GREET_BY.likes[r].join('|') !== GREET_BY.likes[q].join('|'))), 'ER-RISE-03: the same regard is said differently at each rung');
ok(Object.values(CALENDAR_LINES).every((l) => l.length >= 6), 'each calendar day has at least 6 lines for the street');
const long = lines.filter((l) => l.split(/\s+/).length > 12);
ok(long.length === 0, 'street lines stay short (about seven words, never over twelve) ' + JSON.stringify(long.slice(0, 3)));
const own = Object.entries(OWN_STREET);
ok(own.every(([, l]) => l.length >= 8 && new Set(l).size === l.length), `3.2.3: ${own.length} regulars who had no street lines of their own now have ${own[0][1].length} each (thirty is the target)`);

// ---------- in the game ----------
const h = await launch({ port: 8832, quality: 'low', seed: 1990 });
const at = (d, hr) => h.ev((d, hr) => { LEDGER.G.t = d * 1440 + hr * 60; LEDGER.step(0.1); }, d, hr);
const drain = async (pick = () => 0) => { for (let i = 0; i < 14; i++) { const w = await h.ev(() => LEDGER.written.read()); if (!w.open) return; if (w.choices) await h.ev((n) => LEDGER.written.choose(n), pick(w)); else await h.ev(() => LEDGER.written.next()); await h.sleep(120); } };
try {
  await h.newWeek();
  await h.ev(() => { LEDGER.G.story.flags.tour = 1; LEDGER.G.car.keys = true; LEDGER.G.money.clean = 5000; });
  const cnt = await h.ev(() => ({ hap: LEDGER.game.life.happenings(), st: LEDGER.game.life.stories() }));
  ok(cnt.hap.length >= 6 && cnt.hap.every((s) => s.choices >= 2 && s.fromHour < s.untilHour && Array.isArray(s.needs)), `3.7: ${cnt.hap.length} authored happenings, each with a choice and a named state`);
  ok(cnt.st.length >= 6 && cnt.st.every((s) => s.steps.length >= 3 && s.steps.length <= 5), `3.3: ${cnt.st.length} side stories of three to five steps: ` + cnt.st.map((s) => s.id + ' ' + s.steps.length).join(', '));
  // the calendar
  const cal = await h.ev(() => { const L = LEDGER.game.life; return { d0: L.date(0), k3: L.dayKind(3), k21: L.dayKind(21), k27: L.dayKind(27), hook: LEDGER.G.hooks.calendar() }; });
  ok(cal.d0.weekday === 'Monday' && cal.d0.dayOfMonth === 15 && cal.d0.month === 'October' && cal.k3.market && cal.k21.bonfire && cal.k27.remembrance && cal.hook.weekday, 'A20: Monday 15 October 1990, market Thursday, Bonfire Night and Remembrance Sunday on their days');
  await at(6, 10);
  const sun = await h.ev(() => { const L = LEDGER.game.life; LEDGER.G.x.life.calendar.moved = []; L.calendarHour(10, 6); return { moved: LEDGER.G.x.life.calendar.moved, nora: LEDGER.G.people.nora.override }; });
  ok(sun.moved.filter((m) => m.to === 'chapel').length >= 3 && sun.nora && /chapelgate|bench|grave/.test(sun.nora.where), 'ER-CAL-01: on Sunday morning the churchgoers are sent to the chapel: ' + sun.moved.map((m) => m.who + '>' + m.to).join(' '));
  await at(21, 19.2);
  const bon = await h.ev(() => { const L = LEDGER.game.life; LEDGER.G.x.life.calendar.moved = []; L.calendarHour(19, 21); return LEDGER.G.x.life.calendar.moved; });
  ok(bon.filter((m) => m.to === 'quay').length >= 5 && !bon.some((m) => m.who === 'ada'), 'ER-CAL-01: on Bonfire Night the street goes down to the quay, and Ada stays at her window (' + bon.length + ' moved)');
  // who is out: the same hour dry, in drizzle and in rain; and by the day
  const cr = await h.ev(() => {
    const L = LEDGER.game.life, G = LEDGER.G, out = {};
    const tgt = (d, hr, rain) => { G.t = d * 1440 + hr * 60; G.weather.rain = rain; return L.crowdTarget(); };
    out.dry = tgt(1, 12, 0); out.drizzle = tgt(1, 12, 0.3); out.rain = tgt(1, 12, 0.8); out.rain2 = tgt(1, 12, 0.8);
    out.market = tgt(3, 11, 0); out.wed = tgt(2, 11, 0); out.match = tgt(5, 14.5, 0); out.sat = tgt(5, 11, 0); out.night = tgt(1, 3, 0);
    G.t = 1 * 1440 + 12 * 60; G.weather.rain = 0.8; G.weather.next = 1e9; G.tom.space = 'away';
    return out;
  });
  ok(cr.dry > cr.drizzle && cr.drizzle > cr.rain && cr.rain === cr.rain2, `ER-NIGHT-03: the same hour dry ${cr.dry}, drizzle ${cr.drizzle}, rain ${cr.rain}, and the same every time`);
  ok(cr.market < cr.wed && cr.match > cr.sat && cr.night === 0, `2.1.2, A20: market day empties the Hook (${cr.market} against ${cr.wed}), the match fills it (${cr.match} against ${cr.sat}), nobody at three in the morning`);
  await h.step(20);
  const thin2 = await h.ev(() => { const L = LEDGER.game.life; L.thinCrowd(); const r = { out: L.crowdOut(), want: L.crowdTarget(), ages: LEDGER.G.crowd.concat(LEDGER.G.named).filter((P) => !(P.def.age >= 18)).map((P) => P.id) }; LEDGER.G.weather.rain = 0; LEDGER.G.tom.space = 'street'; return r; });
  ok(thin2.out <= thin2.want, `2.1.4: in rain the walkers out (${thin2.out}) are no more than the rule allows (${thin2.want})`);
  ok(thin2.ages.length === 0, 'canon: nobody in the cast or the crowd is under eighteen ' + thin2.ages);
  // greetings by regard and rung
  await at(1, 11);
  const gr = await h.ev(() => {
    const G = LEDGER.G, L = LEDGER.game.life, t = G.tom, R = G.people.ron, K = G.people.kevin;
    t.space = 'street'; t.x = 40; t.z = 47; t.inCar = false;
    for (const P of G.named.concat(G.crowd)) if (P !== R && P !== K && P.space === 'street' && Math.hypot(P.x - 40, P.z - 47) < 9) P.space = 'off';
    const put = (P, dx) => { Object.assign(P, { space: 'street', x: 40 + dx, z: 49, hold: true, route: null, moving: false, gone: false, dead: false }); P.mind.look = 1; P.mind.fam = 1; };
    put(R, 2); R.mind.regard = 0.6; R.mind.fear = 0; K.space = 'off';
    G.x.life.lines = []; G.x.life.said = {};
    for (let i = 0; i < 4; i++) L.greetStep(0.1);
    const ron = G.x.life.lines.slice();
    R.space = 'off'; put(K, -2); K.mind.regard = -0.7; K.mind.fear = 0; G.x.rise = Object.assign(G.x.rise || {}, { rung: 3 });
    G.x.life.lines = [];
    L.greetStep(0.1);
    const kev = G.x.life.lines.slice();
    G.x.rise.rung = 1; K.hold = false; R.hold = false;
    return { ron, kev, bubs: LEDGER.ui.bubs.map((b) => b.text) };
  });
  ok(gr.ron.length >= 3 && gr.ron[0].kind === 'likes' && gr.ron[0].rung === 'nephew', '2.12.4: a man who likes him greets him so, at rung one: ' + JSON.stringify(gr.ron[0]));
  ok(gr.kev.length === 1 && gr.kev[0].kind === 'angry' && gr.kev[0].rung === 'firm', 'ER-RISE-03: an angry man at rung three says it as to the firm: ' + JSON.stringify(gr.kev[0]) + ' ' + JSON.stringify(gr.bubs));
  // the paper
  const pp = await h.ev(() => {
    const G = LEDGER.G, L = LEDGER.game.life;
    const e1 = LEDGER.ledger.act('strike', { silent: true, told: ['alison'], name: 'a man on the quay' });
    const before = L.alisonKnows();
    const ed = L.printEdition(1), again = L.printEdition(4);
    const readers = G.named.filter((P) => P.id !== 'alison' && P.mind.by[e1] && P.mind.by[e1].src === 'told' && P.mind.by[e1].from === 'alison').map((P) => P.id);
    return { e1, ed, again: again.lines.length, readers, knows: before.map((k) => k.e) };
  });
  ok(pp.ed.lines.length >= 1 && pp.ed.traced && pp.ed.lines.every((l) => pp.knows.includes(l.e)), 'ER-PAPER-01: every printed line traces to what Alison saw or was told: ' + JSON.stringify(pp.ed.lines.map((l) => l.text)));
  ok(pp.readers.length >= 3 && pp.again === 0, `the paper carries it beyond the routines' meetings (${pp.readers.length} readers hold it as told by the paper), and prints it once`);
  await h.ev(() => { LEDGER.game.life.readPaper(); }); await h.sleep(200); await drain();
  const pn = await h.ev(() => LEDGER.G.ledger.notes.filter((n) => /In the paper/.test(n.text || '')).length);
  ok(pn >= 1, 'read, it goes into the Ledger');
  // letters
  const lt = await h.ev(() => { const L = LEDGER.game.life; const a = L.postLetter('solicitor'), b = L.postLetter('solicitor'); LEDGER.goInside && 0; LEDGER.G.hooks.enterRoom('mickeys', true); return { a, b, prompts: LEDGER.prompts() }; });
  ok(lt.a && !lt.b && lt.prompts.some((p) => /Read the post/.test(p.text)), 'a letter waits at the office, once, with a prompt to read it: ' + JSON.stringify(lt.prompts.map((p) => p.text)));
  await h.ev(() => LEDGER.press('G')); await h.sleep(200);
  const l1 = await h.ev(() => LEDGER.written.read());
  await drain();
  const l2 = await h.ev(() => ({ notes: LEDGER.G.ledger.notes.filter((n) => /solicitor/i.test(n.text || '')).length, st: LEDGER.G.x.life.letters, again: LEDGER.game.life.postLetter('solicitor') }));
  ok(l1.open && /solicitor/i.test(l1.text) && l2.notes >= 1 && l2.st.waiting.length === 0 && l2.st.read.solicitor && !l2.again, '6.10: the letter opens as a page, goes into the Ledger, and does not come twice');
  await h.ev(() => LEDGER.G.hooks.leaveRoom());
  // town marks
  const mk = await h.ev(() => { const L = LEDGER.game.life; L.townMark('forced_door', 'hut', 'tom'); L.townMark('broken_window', 'ritas', 'tom'); const a = L.marksNow().length; LEDGER.saveNow(); LEDGER.restore(localStorage.getItem('ledger.save.v4')); const b = LEDGER.game.life.marksNow().length; LEDGER.G.t += 1500; const c = LEDGER.game.life.marksNow().map((m) => m.kind); LEDGER.G.t += 1500; return { a, b, c, d: LEDGER.game.life.marksNow().length }; });
  ok(mk.a === 2 && mk.b === 2 && mk.c.join() === 'broken_window' && mk.d === 0, '2.19: a forced door shows for a day and a broken window for two, across save and load: ' + JSON.stringify(mk));
  // a happening, placed by its state
  await at(8, 10); // Tuesday of week two, ten in the morning
  await h.ev(() => { const G = LEDGER.G, t = G.tom; G.story.flags.tour = 1; t.space = 'street'; t.inCar = false; t.x = 5.6; t.z = 30; G.x.life.happen.log = []; G.x.life.happen.active = null; });
  await h.step(7);
  const hp = await h.ev(() => { const x = LEDGER.G.x.life.happen; return { active: x.active, place: x.placements[x.placements.length - 1], why: LEDGER.game.life.happenWhyNot('row') }; });
  ok(hp.active && hp.active.id === 'shoplifter' && /grocerOpen/.test(hp.place.because), 'ER-HAPPEN-01: the shoplifter is placed because the grocer is open, at that hour: ' + JSON.stringify(hp.place));
  ok(hp.why === 'the hour' || /needs/.test(hp.why), 'and the row on the step is not, for a named reason: ' + hp.why);
  const ev0 = await h.ev(() => LEDGER.G.events.length);
  const pr = await h.ev(() => { const a = LEDGER.G.x.life.happen.active, t = LEDGER.G.tom; t.x = a.x + 1; t.z = a.z + 1; return LEDGER.prompts(); });
  ok(pr.some((p) => p.key === 'E' && /Step in/.test(p.text)), 'beside it, a prompt with the hands: ' + JSON.stringify(pr.map((p) => p.text)));
  await h.ev(() => LEDGER.press('E')); await h.sleep(200);
  const hw = await h.ev(() => LEDGER.written.read());
  ok(hw.open && hw.choices && hw.choices.length === 3, 'a choice: ' + JSON.stringify(hw.choices));
  await drain();
  const ha = await h.ev((n) => { const G = LEDGER.G, x = G.x.life.happen; return { kinds: G.events.slice(n).map((E) => E.kind), active: x.active, place: x.placements[x.placements.length - 1], note: G.ledger.notes.some((q) => /Hook Stores/.test(q.text || '')), again: LEDGER.game.life.happenWhyNot('shoplifter') }; }, ev0);
  ok(ha.kinds.includes('good_turn') && !ha.active && ha.note, 'he stepped in: the town has an act to know and the Ledger a line: ' + ha.kinds);
  ok(ha.place.tookRealSeconds < 120 && /thirty minutes|one just happened/.test(ha.again), `A18: under two minutes (${ha.place.tookRealSeconds} s), and not again inside thirty minutes: ${ha.again}`);
  const fv = await h.ev(() => { const G = LEDGER.G, d = Math.floor(G.t / 1440); G.x.life.happen.helped.push({ id: 'van', day: d - 3, returned: false }); LEDGER.game.life.favourStep(d, 11); return { f: G.x.life.favours, hook: G.hooks.favour('lift') }; });
  ok(fv.f.lift != null && fv.hook, 'a stranger he helped comes back days later with a small favour');
  // a side story, end to end: the plate off the bench
  await at(8, 11);
  const story = [];
  for (let s = 0; s < 4; s++) {
    const o = await h.ev(() => { const o = LEDGER.game.life.storyOpen('bench'); if (o) { const t = LEDGER.G.tom; t.space = 'street'; t.x = o.x + 0.8; t.z = o.z + 0.8; } return { o, pr: LEDGER.prompts().map((p) => p.text) }; });
    story.push(o.o && o.pr.includes(o.o.prompt));
    await h.ev(() => LEDGER.press('E')); await h.sleep(200); await drain();
  }
  const sb = await h.ev(() => { const G = LEDGER.G; return { st: G.x.life.stories.bench, ev: G.events.filter((E) => E.kind === 'story_end').length, walsh: G.people.walsh.mind.mem.some((m) => G.ev[m.e] && G.ev[m.e].kind === 'story_end'), note: G.ledger.notes.some((n) => /plate is back/.test(n.text || '')) }; });
  ok(story.every(Boolean) && sb.st.done && sb.ev === 1 && sb.walsh && sb.note, '3.3: the bench plate story is found on foot in four steps and ends in something the town knows (Father Walsh holds it)');
  // calling on Philip Danby
  await at(9, 13);
  const c1 = await h.ev(() => { const G = LEDGER.G, L = LEDGER.game.life; const before = L.canCall('danby'); G.story.flags.met_danby = 1; return { before, now: L.canCall('danby') }; });
  ok(!c1.before.ok && c1.now.ok, 'A39: no call before they have met; at one in the afternoon, at home, he can be called on');
  const night = await h.ev(() => { LEDGER.G.t = 9 * 1440 + 23 * 60; const r = LEDGER.game.life.canCall('danby'); LEDGER.G.t = 9 * 1440 + 13 * 60; return r; });
  ok(!night.ok, 'A39: not at eleven at night: ' + night.why);
  const visit = async () => { const t0 = await h.ev(() => LEDGER.G.played); h.ev(() => { LEDGER.game.life.call('danby'); }); await h.sleep(250); const seen = []; for (let i = 0; i < 10; i++) { const w = await h.ev(() => LEDGER.written.read()); if (!w.open) break; seen.push(w.text + ' ' + (w.choices || []).join(' ')); if (w.choices) await h.ev(() => LEDGER.written.choose(0)); else await h.ev(() => LEDGER.written.next()); await h.sleep(120); } return { seen, t0 }; };
  const v1 = await visit();
  const v2 = await visit();
  const c2 = await h.ev(() => ({ calls: LEDGER.G.x.life.calls.danby, friend: LEDGER.G.hooks.friend() }));
  ok(v1.seen.length >= 2 && v1.seen.length <= 6 && v1.seen.every((s) => !/\d+\s*(\/|%|points?)/.test(s)), 'A39: a short scene, no score shown (' + v1.seen.length + ' lines)');
  ok(c2.calls.length === 2 && !c2.calls[0].cool && c2.calls[1].cool && /again/i.test(v2.seen[0] || ''), 'A39: a second call inside the day draws a cooler answer: ' + (v2.seen[0] || ''));
  const c3 = await h.ev(() => { const c = LEDGER.G.x.life.calls; c.danby = [{ honest: true }, { honest: true }, { honest: true }]; c.last.danby = -9999; return LEDGER.game.life.canCall('danby'); });
  await visit();
  const c4 = await h.ev(() => LEDGER.G.hooks.friend());
  ok(c3.ok && c4.who === 'danby' && c4.holds, '3.2.5: after honest visits the friendship holds, readable by the endings as G.x.life.friend: ' + JSON.stringify(c4));
  // the boxing club: no stakes
  const m0 = await h.ev(() => { LEDGER.G.t = 9 * 1440 + 18 * 60; return { m: LEDGER.G.money.clean + LEDGER.G.money.dirty, open: LEDGER.game.life.boxingOpen(), sun: LEDGER.game.life.boxingOpen(18, 6) }; });
  h.ev(() => { LEDGER.game.life.club(); }); await h.sleep(250);
  const box = []; for (let i = 0; i < 14; i++) { const w = await h.ev(() => LEDGER.written.read()); if (!w.open) break; box.push(w.text + ' ' + (w.choices || []).join(' ')); if (w.choices) await h.ev(() => LEDGER.written.choose(0)); else await h.ev(() => LEDGER.written.next()); await h.sleep(120); }
  const bx = await h.ev(() => ({ m: LEDGER.G.money.clean + LEDGER.G.money.dirty, b: LEDGER.G.x.life.boxing, ev: LEDGER.G.events[LEDGER.G.events.length - 1].kind }));
  ok(m0.open && !m0.sun && bx.b.bouts === 1 && bx.ev === 'spar', '7.16: three rounds with the gloves on at the boxing club, shut on Sunday');
  ok(bx.m === m0.m && box.every((t) => !/£|\bpence\b|stake|wager|prize|purse/i.test(t)), 'ER-PASTIME-01: no money moves and no stake is spoken of');
  // teaching
  const hn = await h.ev(() => { const L = LEDGER.game.life; LEDGER.G.x.life.hints = { shown: {}, lastAt: null }; const a = L.hint('t1', 'A hint.'), b = L.hint('t1', 'A hint.'), c = L.hint('t2', 'Another.'); LEDGER.G.played += 13; const d = L.hint('t2', 'Another.'); return [a, b, c, d]; });
  ok(hn[0] && !hn[1] && !hn[2] && hn[3], 'ER-FIRST-03: each hint once, never two within 12 s: ' + hn);
  // always something to do: 20 daytime moments
  const idle = await h.ev(() => {
    const G = LEDGER.G, L = LEDGER.game.life, t = G.tom, out = [];
    G.story.flags.tour = 1; G.car.keys = true; G.story.fare = null;
    const spots = [[6, 34], [0, 10], [-4, -28], [4, -44], [10, 46]];
    for (let i = 0; i < 20; i++) { G.t = (8 + (i % 4)) * 1440 + (9 + (i * 2) % 9) * 60; LEDGER.step(0.2); t.space = 'street'; t.inCar = false; [t.x, t.z] = spots[i % 5]; const r = L.somethingToDo(); out.push({ strict: r.ok, any: r.withTalk.ok, first: r.first && r.first.kind }); }
    return out;
  });
  const strict = idle.filter((r) => r.strict).length, any = idle.filter((r) => r.any).length;
  ok(any >= 18, `ER-CORE-07: at 20 daytime moments on Quay Street, something to do within 30 s at ${any} (a fare, a debt, a word, a happening or a story at ${strict}; counting anybody to talk to, ${any})`);
  console.log('     idle probe, first thing in reach: ' + idle.map((r) => r.first || '-').join(' '));
  // the whole of it survives save and load
  const sv = await h.ev(() => { const a = JSON.stringify(LEDGER.G.x.life); LEDGER.saveNow(); LEDGER.restore(localStorage.getItem('ledger.save.v4')); return { same: JSON.stringify(LEDGER.G.x.life) === a, f: LEDGER.game.faults.slice() }; });
  ok(sv.same, 'the town\'s days survive save and load');
  ok(sv.f.length === 0, 'no faults in the game systems ' + sv.f.join(' | '));
  ok(h.errors.length === 0, 'no page errors' + (h.errors.length ? ': ' + h.errors.join(' | ') : ''));
} finally {
  await h.close();
}
console.log(bad ? `FAIL: ${bad} checks` : 'PASS');
process.exit(bad ? 1 : 0);
