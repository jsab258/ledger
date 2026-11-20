// The bridge to the real town code (the one-shot, 20 Nov 2026; step 4a). A seeded week, stepped by hand.
// What it holds: the town opens and runs; how well a witness sees him is the real rule's; a crime seen reaches the
// police by the real rule and brings a constable; the week's deed is followed; the town travels in the save; a save
// from before the swap loads; without the simulation file the game still runs; every reaction prints its chain.
import { launch } from '../harness.mjs';
let failed = 0;
const check = (name, ok, detail = '') => { console.log((ok ? 'ok   ' : 'TEST FAIL ') + name + (ok ? '' : ' ' + detail)); if (!ok) failed++; };
const h = await launch({ port: 8941, seed: 19901015 });
await h.newWeek();
const T = () => h.ev(() => ({ live: LEDGER.game.town.live(), why: LEDGER.game.town.why(), people: LEDGER.game.town.people().length, failed: LEDGER.game.town.failed(), refusals: LEDGER.game.town.refusals.slice(), faults: LEDGER.game.faults.slice() }));
let t = await T();
check('the real town is running from the first step', t.live && t.people === 41, JSON.stringify(t));

// ---- how well a witness sees him: the port's own rule, through the door ----
const r = await h.ev(() => { const g = LEDGER.game.town; return { near: g.rung(5, 1, 0.9, false, true), nearStranger: g.rung(5, 1, 0, false, true), mid: g.rung(15, 1, 0, false, true), midMark: g.rung(15, 1, 0, true, true), far: g.rung(30, 1, 0, false, true), dark: g.rung(15, 0.12, 0, true, true), lit: g.rung(15, 0.7, 0, true, true), back: g.rung(5, 1, 0, false, false), backMark: g.rung(5, 1, 0, true, false), backKnown: g.rung(5, 1, 0.9, false, false), foot3am: g.audible(25, 15), footNoon: g.audible(25, 45) }; });
check('recognised close by somebody who knows him, a face by a stranger (the ladder, 2.2.2)', r.near === 4 && r.nearStranger === 3, JSON.stringify(r));
check('a mark at 15 m with the coat, a silhouette without; a silhouette at 30 m (2.2.3)', r.midMark === 2 && r.mid <= 1 && r.far === 1, JSON.stringify(r));
check('a dark doorway catches less than a lamp at the same distance (ER-HIDE-01, the light scale)', r.dark < r.lit, JSON.stringify(r));
check('with his back turned a stranger catches no face, a mark still; somebody who knows him knows his back (A1, the real rule)', r.back === 1 && r.backMark === 2 && r.backKnown === 4, JSON.stringify(r));
check('a footstep carries about 3.6 m at three in the morning and nothing at noon (2.2.4)', Math.abs(r.foot3am - 3.6) < 0.2 && r.footNoon === 0, JSON.stringify(r));

// ---- a crime seen: two witnesses, one of the cast (June) and one the cast file lacks (Grace) ----
const stand = (ids) => h.ev((ids) => { const G = LEDGER.G, t = G.tom; if (t.inCar) t.inCar = false; t.space = 'street'; t.x = 0; t.z = 0; t.ang = 0; t.coat = false; t.v = 0; G.t = Math.max(G.t, 1 * 1440 + 11 * 60); let i = 0; for (const id of ids) { const P = G.people[id]; P.space = 'street'; P.gone = false; P.awake = true; P.dead = false; P.hold = true; P.route = null; P.moving = false; P.x = -1.5 + 3 * i++; P.z = 4; P.ang = Math.atan2(t.x - P.x, t.z - P.z); P.mind.fam = 0.9; P.mind.inh = 1; P.mind.fear = 0; P.mind.regard = 0; } LEDGER.step(0.2); }, ids);
await stand(['june', 'grace']);
const c1 = await h.ev(() => { const g = LEDGER.game.town; const e = g.act('weapon_used', { target: 'lee', zone: 'Quay Street' }); return { e, crimes: g.crimes(), stmt: LEDGER.G.ev[e].stmt, wit: LEDGER.G.ev[e].wit, mem: ['june', 'grace'].map((id) => { const m = LEDGER.G.people[id].mind.by[e]; return m && { who: m.who, rung: m.rung, sure: m.sure }; }) }; });
const crime = c1.crimes.find((c) => c.topic.endsWith('_e' + c1.e));
check('a wounding seen by two is told to the town as a crime (decision 5)', !!crime && crime.offence === 3 && crime.witnesses.length >= 2, JSON.stringify(c1));
check('both witnesses recognised him, by the real rule (rung 4, sure)', c1.mem.every((m) => m && m.rung === 4 && m.who === 'tom' && m.sure === 1), JSON.stringify(c1.mem));
check("the prototype's old statement rule is retired for it", Array.isArray(c1.stmt) && c1.stmt.length === 0, JSON.stringify(c1.stmt));
// the next morning: nine, the witnesses go; ten, a constable
await h.ev(() => { for (const id of ['june', 'grace']) LEDGER.G.people[id].hold = false; LEDGER.G.tom.space = 'away'; });
const until = async (minute) => { for (let i = 0; i < 400; i++) { const now = await h.ev(() => LEDGER.G.t); if (now >= minute) return; await h.ev((m) => { const G = LEDGER.G; for (let k = 0; k < 40 && G.t < m; k++) LEDGER.simStep(1.5); }, minute); } };
await until(2 * 1440 + 9 * 60 + 5);
const c2 = await h.ev((e) => ({ crimes: LEDGER.game.town.crimes(), stmt: LEDGER.G.ev[e].stmt, x: LEDGER.G.x.town }), c1.e);
const cr2 = c2.crimes.find((c) => c.topic.endsWith('_e' + c1.e));
check('at nine next morning both went to the police, by the real rule (WouldReport)', ['june', 'grace'].every((id) => Number.isInteger(cr2.witnesses.find((w) => w.id === id).went)) && c2.stmt.includes('june') && c2.stmt.includes('grace'), JSON.stringify(cr2) + JSON.stringify(c2.stmt));
check('DS Ellis comes the same morning for the wounding (the real nine o\'clock)', (c2.x.ellis || []).some((v) => /Wounding/.test(v.why)), JSON.stringify(c2.x.ellis));
await until(3 * 1440 + 10 * 60 + 5);
const c3 = await h.ev(() => ({ x: LEDGER.G.x.town, arrest: LEDGER.G.story.arrest, held: LEDGER.game.town.held() }));
check('at ten the day after, a constable comes for him (TakeIn), and the game has an arrest to play', (c3.x.taken || []).length === 1 && c3.x.taken[0].e === c1.e, JSON.stringify(c3.x.taken) + JSON.stringify(c3.arrest));
const re = await h.ev(() => LEDGER.game.town.reactions());
check('every reaction prints a chain that ends at somebody who saw it (ER-EYES-05)', re.length >= 3 && re.every((x) => x.ok), JSON.stringify(re.filter((x) => !x.ok)).slice(0, 600));

// ---- a frightened witness does not go (reaching the witness first) ----
await h.ev(() => { LEDGER.G.story.arrest = null; LEDGER.G.tom.space = 'street'; });
await stand(['brenda']);
const f1 = await h.ev(() => { const e = LEDGER.game.town.act('weapon_used', { target: 'lee', zone: 'Quay Street' }); LEDGER.G.people.brenda.mind.fear = 0.9; LEDGER.G.people.brenda.hold = false; LEDGER.G.tom.space = 'away'; return e; });
await until(5 * 1440 + 9 * 60 + 5);
const f2 = await h.ev((e) => LEDGER.game.town.crimes().find((c) => c.topic.endsWith('_e' + e)), f1);
check('a witness frightened before nine never goes; the memory stays', f2.witnesses.filter((w) => w.id === 'brenda').every((w) => w.never && !Number.isInteger(w.went)), JSON.stringify(f2));

// ---- the same deed, different people: each person's temper (2.14) ----
const tp = await h.ev(() => { const g = LEDGER.game.town; return { timid: g.wouldReportAs(0.2, 0.5, 3, false), steady: g.wouldReportAs(0.8, 0.5, 3, false), friend: g.wouldReportAs(0.8, 0.9, 3, false), victimSoft: g.wouldReportAs(0.8, 0.9, 2, true), victimHard: g.wouldReportAs(0.8, 0.1, 2, true) }; });
check('a timid witness and a friend stay away, a steady one goes; a victim settles or does not (2.14)', !tp.timid && tp.steady && !tp.friend && !tp.victimSoft && tp.victimHard, JSON.stringify(tp));

// ---- the week's one deed: a thing damaged, followed by the real rules ----
await h.ev(() => { LEDGER.G.tom.space = 'street'; });
await stand(['june']);
const d1 = await h.ev(() => { const g = LEDGER.game.town; const e = g.act('crash', { zone: 'Quay Street' }); LEDGER.G.people.june.hold = false; LEDGER.G.tom.space = 'away'; return { e, deed: g.deed(), tell: g.tellOf('crash') }; });
check('damage is the week\'s deed in the real town, with its witness (decision 6)', d1.tell === 'deed' && d1.deed && d1.deed.witnesses.some((w) => w.id === 'june'), JSON.stringify(d1));

// ---- the town travels in the save ----
const s1 = await h.ev(() => { const before = JSON.stringify(LEDGER.game.town.save()); LEDGER.saveNow(false); const json = localStorage.getItem('ledger.save.v4'); const mems = Object.values(LEDGER.G.people).reduce((n, P) => n + (P.mind ? P.mind.mem.length : 0), 0); const ok = LEDGER.restore(json); return { ok, mems, memsAfter: Object.values(LEDGER.G.people).reduce((n, P) => n + (P.mind ? P.mind.mem.length : 0), 0), same: before === JSON.stringify(LEDGER.game.town.save()), why: LEDGER.game.town.why(), live: LEDGER.game.town.live(), json }; });
check('saved and loaded, the town is the same to the last character and every memory is kept (ER-EYES-07)', s1.ok && s1.live && s1.same && s1.mems === s1.memsAfter && /saved town/.test(s1.why), JSON.stringify({ ...s1, json: undefined }));
await until(6 * 1440 + 12 * 60);
t = await T();
check('it plays on after the load', t.live && !t.refusals.length && !t.faults.length, JSON.stringify(t));

// ---- a reload gives the same next hour for the town (ER-SAVE-01), at three moments ----
let sameHour = 0;
for (const at of [6 * 1440 + 13 * 60 + 17, 6 * 1440 + 20 * 60 + 2, 7 * 1440 + 3 * 60 + 41]) {
  await until(at);
  const r1 = await h.ev(() => { LEDGER.G.tom.space = 'away'; LEDGER.saveNow(false); const json = localStorage.getItem('ledger.save.v4'); const t0 = LEDGER.G.t; while (LEDGER.G.t < t0 + 60) LEDGER.simStep(1.5); const a = JSON.stringify(LEDGER.game.town.save().texts); LEDGER.restore(json); LEDGER.G.tom.space = 'away'; while (LEDGER.G.t < t0 + 60) LEDGER.simStep(1.5); const b = JSON.stringify(LEDGER.game.town.save().texts); return { same: a === b, n: a.length }; });
  if (r1.same) sameHour++;
}
check('saved at three odd moments and loaded, the town plays the same next hour each time (ER-SAVE-01)', sameHour === 3, String(sameHour));

// ---- a save from before the swap ----
const o1 = await h.ev((json) => { const o = JSON.parse(json); delete o.x; const ok = LEDGER.restore(JSON.stringify(o)); return { ok, live: LEDGER.game.town.live(), why: LEDGER.game.town.why(), old: LEDGER.G.x.town.old }; }, s1.json);
check('a save from before the real town loads: a fresh town at its clock, told what its people saw', o1.ok && o1.live && /before the real town/.test(o1.why) && o1.old && o1.old.fed >= 1, JSON.stringify(o1));
await until(7 * 1440 + 6 * 60);

// ---- without the simulation file the game still runs ----
const n1 = await h.ev(() => { LEDGER.game.town.drop(); for (let i = 0; i < 80; i++) LEDGER.simStep(1.5); return { live: LEDGER.game.town.live(), faults: LEDGER.game.faults.slice(), t: LEDGER.G.t }; });
check('with the real town gone the street runs on the old rules, with no fault', !n1.live && !n1.faults.length, JSON.stringify(n1));
t = await T();
check('no call was refused and no system faulted in the whole run', !t.refusals.length && !t.faults.length, JSON.stringify(t));
check('no page errors', h.errors.length === 0, h.errors.slice(0, 3).join(' | '));
await h.close();
console.log(failed ? 'FAIL' : 'PASS');
process.exit(failed ? 1 : 0);
