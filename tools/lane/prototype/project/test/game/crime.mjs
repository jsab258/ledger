// Crime with the hands and the law (parts 1.6.1 to 1.6.3, 1.6.7, 1.6.9, 1.6.11 to 1.6.14, 2.7.6, 3.5.3, 4.11.1;
// 2.6.1 to 2.6.5, 2.6.8 to 2.6.10, 2.5.4, 2.5.5).
import { start } from './lib.mjs';
const t = await start({ port: 8874 });
const C = (fn, ...a) => t.ev(fn, ...a);
// any written scene still open is answered with its first choice, so the game is never left paused
const clear = async () => { for (let i = 0; i < 8 && (await t.ev(() => LEDGER.read().boxOpen)) === 'dialog'; i++) { await t.h.sleep(1600); await t.h.key('KeyE'); await t.h.key('Digit1'); await t.h.sleep(500); } };

// the pockets (ER-POCKET-01): two things under the coat, no more; a search finds exactly what he carries
const p = await C(() => { const c = LEDGER.game.crime; const a = c.take('torch'), b = c.take('crowbar'), d = c.take('cosh'); return { a, b, d, carried: c.carried().map((x) => x.id) }; });
t.ok(p.a && p.b && !p.d && p.carried.length === 2, 'two things under the coat and no more', p);

// a break-in site entered three ways (1.6.1, 3.5.3): key, back way, force; force is loud and shows on the door
const hut = await C(() => { const G = LEDGER.G, c = LEDGER.game.crime; G.tom.space = 'street'; G.tom.x = -101.5; G.tom.z = 28; LEDGER.game.test.pass(0); const prompts0 = LEDGER.prompts().map((q) => q.text); return { prompts0 }; });
t.ok(hut.prompts0.some((q) => /Locked: Iveson's hut/.test(q)) && hut.prompts0.some((q) => /Force the door/.test(q)), 'a locked site offers its lock and the loud way', hut.prompts0);
const cased = await C(() => { const c = LEDGER.game.crime, G = LEDGER.G; G.tom.x = -85; G.tom.z = 30; c.caseNow('hut'); return { cased: c.x().cased, note: G.ledger.notes.filter((n) => /Watched Iveson's hut/.test(n.text)).map((n) => n.text) }; });
t.ok(cased.cased.hut && /gap by the crane/.test(cased.note[0]) && /dog/.test(cased.note[0]), 'casing writes the hours, the key and the way left open in the Ledger (ER-CASE-01)', cased.note);
const force = await C(() => { const c = LEDGER.game.crime, G = LEDGER.G; G.tom.x = -101.5; G.tom.z = 28; const n0 = G.events.length; c.wayIn('hut', 'force'); const E = G.events.slice().reverse().find((q) => q.kind === 'forced_door') || {}; return { kind: E.kind, marks: c.marks(), inside: c.x().inside, noise: G.tom.noiseP, deeds: LEDGER.game.town.x().deeds.length }; });
t.ok(force.kind === 'forced_door' && force.marks.length === 1 && force.inside === 'hut' && force.noise >= 20, 'force is loud, shows on the door, and is damage the town follows', force);

// searching (ER-SEARCH-01, A33): the table time with the torch, twice that in the dark without it
const s1 = await C(() => { const c = LEDGER.game.crime, G = LEDGER.G; G.t = Math.floor(G.t / 1440) * 1440 + 23.5 * 60; G.env.lightAt = () => 0.1; LEDGER.game.test.pass(0); c.x().torchOn = false; c.search('hut', 'tinbox'); const dark = c.doing().left; c.finishDoing(); c.x().torchOn = true; c.search('hut', 'spike'); const lit = c.doing().left; c.finishDoing(); return { dark, lit, tin: G.money.dirty, facts: c.x().facts, bal: LEDGER.game.econ.balances().holds, notes: G.ledger.notes.filter((n) => /tin box|receipt/.test(n.text)).length }; });
t.ok(s1.dark === 4 && s1.lit === 4, 'a drawer takes 2 s by the table and 4 s in the dark; a desk 4 s with the torch', s1);
t.ok(s1.tin === 8000 && s1.facts.iveson_warehouse && s1.bal && s1.notes === 2, "Iveson's eighty pounds is in the tin, the receipt is a fact he holds, every pound balances", s1);

// lifts, the hot mark and the fence (1.6.3, 2.7.6, ER-HAGGLE-01)
const f = await C(async () => { const c = LEDGER.game.crime, G = LEDGER.G; c.x().goods.push({ id: 'watch', name: 'a gold watch', honestPence: 5000, owner: 'hal', takenT: G.t }); return c.x().goods.length; });
await C(() => { LEDGER.game.crime.fence(); });
await t.h.sleep(1500); await t.h.key('Digit2'); await t.h.sleep(1500); await t.h.key('Digit2'); await t.h.sleep(1500); await t.h.key('Digit2'); await t.h.sleep(1500); await t.h.key('Digit1'); await t.h.sleep(1500);
const f2 = await C(() => ({ h: LEDGER.game.crime.x().haggles, tin: LEDGER.G.money.dirty, goods: LEDGER.game.crime.x().goods.length, box: LEDGER.read().boxOpen }));
t.ok(f2.h.length === 1 && f2.h[0].offers <= 3, 'a haggle never takes more than three offers', f2);

// damage by hand (A35) and finding it (A38): heard at the force reach, stays until mended, known to its owner by morning
const dm = await C(() => { const G = LEDGER.G, c = LEDGER.game.crime; G.tom.space = 'street'; G.tom.x = 7.2; G.tom.z = -26; LEDGER.game.test.pass(0); const pr = LEDGER.prompts().find((q) => /Put it in/.test(q.text)); return { pr }; });
t.ok(!!dm.pr, 'at night a window can be put in by hand', dm);
await t.h.key('KeyG');
const dm2 = await C(() => { const c = LEDGER.game.crime; return { damaged: c.x().damaged, marks: c.marks().map((m) => m.untilT), deeds: LEDGER.game.law.x().deeds.length }; });
t.ok(dm2.damaged.ritawin && dm2.marks.includes(null), 'the broken window stays until mended (2.19)', dm2);

// the law: custody by offence (2.6.4), DS Ellis's stages each with its sign (ER-POL-05)
const cu = await C(() => ({ w: LEDGER.game.law.custody('damage'), r: LEDGER.game.law.custody('robbery'), k: LEDGER.game.law.custody('killing') }));
t.ok(cu.w.gameHours === 6 && cu.r.gameHours === 12 && cu.k.gameHours === 22 && !cu.k.gameOver, 'an arrest costs hours, never the game', cu);
const el = await C(() => { const l = LEDGER.game.law; const a = l.ellisEvent('witnessed killing'); const s1 = { stage: a.stage, shown: a.signShown, owed: a.owed }; const b = l.ellisEvent('body'); return { s1, s2: { stage: b.stage, shown: b.signShown } }; });
t.ok(el.s1.stage === 1 && !el.s1.shown && el.s1.owed === 3 && el.s2.stage === 1, 'no stage of police interest is skipped unseen', el);
// her sign: somebody near him says her name; then the next stage may come
const sg = await C(() => { const G = LEDGER.G; LEDGER.goTo('rank'); const P = G.people.ron; Object.assign(P, { override: null, gone: false, space: 'street', awake: true, x: G.tom.x + 2, z: G.tom.z }); LEDGER.game.test.pass(3, false); const e = LEDGER.game.law.ellis(); return { stage: e.stage, signs: LEDGER.game.ledgerx.signs().map((s) => s.kind) }; });
t.ok(sg.signs.includes('ellis') && sg.stage >= 1, "her name in the street's talk is the sign of stage one, and it is in the Ledger", sg);

// bought men (ER-BOUGHT-01)
const bm = await C(() => { const G = LEDGER.G, l = LEDGER.game.law; G.money.clean += 6000; G.hooks.flow('world', 'pocket', 6000, 'test money'); const ok = l.buy('harker'); return { ok, a: l.useBought('harker', 'looks away from a car'), b: l.useBought('harker', 'loses a statement'), bal: LEDGER.game.econ.balances().holds }; });
t.ok(bm.ok && bm.a.does && !bm.b.does && bm.bal, 'a bought officer does only what his limit says, and the payment balances', bm);

// the office searched (ER-SEARCHED-01): never without the sign the evening before
const os = await C(() => { const l = LEDGER.game.law, c = LEDGER.game.crime; c.x().stored.push({ id: 'cosh', name: 'a cosh', unlawful: true }); const x = l.x(); x.ellis = { stage: 2, signShown: true, signShownT: LEDGER.G.t, owed: null }; x.search.noticeT = null; LEDGER.game.test.pass(26 * 60); const noNotice = x.search.done; x.search.noticeT = LEDGER.G.t; LEDGER.game.test.pass(30 * 60); return { noNotice, done: x.search.done, found: x.search.found, stored: c.x().stored.length, charges: x.charges.length }; });
t.ok(!os.noNotice && os.done && os.found.includes('cosh') && os.stored === 0, 'the office is searched only after notice, and finds what is stored there', os);

await clear(); await t.h.sleep(3000); await clear(); // the window was seen and rung in: the morning's officer is answered
// a street on edge (A37): three seen deeds in two days
const ed = await C(() => { const l = LEDGER.game.law, G = LEDGER.G; l.x().deeds = [1, 2, 3].map((i) => ({ street: 'Quay Street', seen: true, t: G.t - i * 300 })); LEDGER.game.test.pass(2); const on = l.x().edge; l.x().deeds = []; LEDGER.game.test.pass(2); return { on, off: l.x().edge }; });
t.ok(ed.on && !ed.off, 'three seen deeds set Quay Street on edge, and it eases', ed);

await clear();
// the yard dog (ER-DOG-01): barks at a stranger out of hours; a scrap quiets it; no verb harms a dog
const dg = await C(() => { const G = LEDGER.G, c = LEDGER.game.crime; G.t = Math.floor(G.t / 1440) * 1440 + 23 * 60; G.tom.space = 'street'; G.tom.x = -98; G.tom.z = 34; c.x().pockets.length = 0; LEDGER.step(0.1); const barks = c.x().barks.length; c.take('scrap'); G.t += 10; LEDGER.step(0.1); return { barks, after: c.x().barks.length, quiet: c.x().dogQuietUntilT > G.t, verbs: LEDGER.prompts().map((q) => q.text).filter((q) => /dog/i.test(q)) }; });
t.ok(dg.barks === 1 && dg.after === 1 && dg.quiet && !dg.verbs.length, 'the dog barks, a scrap quiets it, and no verb touches the dog', dg);
await t.done();
