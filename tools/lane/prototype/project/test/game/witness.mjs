// THE WALK, played through (parts 1.4.5, 2.6.10; ER-EYES-04, ER-POL-01, A36). A window is put in by key with a
// witness close by. She is seen to stop, then to go; the walk lasts thirty real seconds in his sight; nothing is on
// record until the call ends; then an officer walks to the spot, and a man who goes back there is challenged.
// Set by hand: only who stands where and the hour. Everything after is key presses and game time.
import { start } from './lib.mjs';
const t = await start({ port: 8881 });
const C = (fn, ...a) => t.ev(fn, ...a);
const subs = () => t.h.page.evaluate(() => [...document.querySelectorAll('#subs .s')].map((e) => e.textContent));
const stepFor = async (secs, until) => { let said = []; for (let s = 0; s < secs; s += 0.5) { await t.h.step(0.5); for (const l of await subs()) if (!said.includes(l)) said.push(l); if (until && (await C(until))) return { s: s + 0.5, said }; } return { s: secs, said }; };

// the scene: eleven at night by the pawn shop window, a woman who knows him two metres off, looking his way
const who = await C(() => {
  const G = LEDGER.G;
  G.t = Math.floor(G.t / 1440) * 1440 + 23 * 60;
  LEDGER.goTo({ xMetres: 7.2, zMetres: -26.4 });
  const P = ['nora', 'grace', 'lily', 'susan', 'peter'].map((id) => G.people[id]).find((p) => p && p.def.upright && !p.def.nostmt && !p.dead);
  Object.assign(P, { override: { where: 'pave', act: 'idle' }, gone: false, space: 'street', awake: true, x: 5.2, z: -24.2, route: null, hold: true, moving: false });
  P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z);
  P.mind.fam = 1;
  LEDGER.step(0.2);
  return { id: P.id, name: P.def.name, prompts: LEDGER.prompts().map((q) => q.text), stmt0: !!G.story.arrest };
});
t.ok(who.prompts.some((q) => /Put it in/.test(q)), 'at night the window can be put in by hand', who);
await t.h.key('KeyG');
const d0 = await C((id) => { const G = LEDGER.G, E = G.events.slice().reverse().find((e) => e.kind === 'window_in'); const m = G.people[id].mind.by[E.id]; return { e: E.id, saw: m && m.src, names: m && m.who, walks: LEDGER.game.walks.live(), arrest: G.story.arrest, stmt: E.stmt }; }, who.id);
t.ok(d0.saw === 'saw' && (d0.names === 'tom' || d0.names === 'owner'), 'she saw it plainly and knows whose face that was', d0);
t.ok(d0.walks.length === 1 && d0.walks[0].who === who.id && d0.walks[0].st === 'means' && !d0.arrest, 'she means to tell, and nothing is on record yet', d0);

// she stands a moment, then goes: he is told so by what he sees, and it is in the Ledger as an open thing
const go = await stepFor(20, () => LEDGER.game.walks.live().some((w) => w.st === 'going'));
const g1 = await C((id) => { const P = LEDGER.G.people[id]; return { x: P.x, z: P.z, live: LEDGER.game.walks.live(), notes: LEDGER.G.ledger.notes.filter((n) => /phone box/.test(n.text)).map((n) => n.text) }; }, who.id);
t.ok(go.s <= 12 && g1.live[0].st === 'going', 'within a few seconds she has made her mind up', { s: go.s, live: g1.live });
const more = await stepFor(8);
const seen = go.said.concat(more.said);
t.ok(seen.some((l) => /phone box/.test(l)), 'he sees her stop and look at the phone box: words on screen, no meter', seen);
// the walk: she moves towards the phone box, and it takes at least thirty real seconds from setting off
const P0 = await C((id) => ({ x: LEDGER.G.people[id].x, z: LEDGER.G.people[id].z }), who.id);
const walk = await stepFor(120, () => !LEDGER.game.walks.live().length);
const end = await C((id, e) => { const G = LEDGER.G, P = G.people[id], x = LEDGER.game.walks.x(), w = x.walks.find((q) => q.e === e); return { st: w.st, x: P.x, z: P.z, phone: [6.0, -11.2], arrest: G.story.arrest, stmt: G.ev[e].stmt, statements: x.statements, given: P.mind.stmtGiven, spot: LEDGER.game.law.x().spot, watched: LEDGER.game.law.x().watched.length }; }, who.id, d0.e);
const took = go.s - 0 + 8 + walk.s - go.s; // seconds from her setting off to the end of the call
t.ok(end.st === 'told' && 8 + walk.s >= 30, 'the walk in his sight lasts at least thirty real seconds (ER-EYES-04)', { secondsAfterSettingOff: 8 + walk.s, st: end.st, took });
t.ok(Math.hypot(end.x - 6.0, end.z + 11.2) < 4 && Math.hypot(P0.x - 6.0, P0.z + 11.2) > 8, 'she walked to the phone box herself', { from: P0, to: [end.x, end.z] });
t.ok(end.arrest && end.arrest.e === d0.e && end.arrest.by.includes(who.id) && end.stmt.includes(who.id) && end.given === 1, 'only now is it on record: a named statement, and an officer due in the morning (ER-POL-01)', end);
t.ok(end.arrest.due > (await C(() => LEDGER.G.t)) + 170, 'the arrest is hours off, never at once', end.arrest);

// police after a deed (A36): an officer walks to the spot inside twenty game minutes and stands there
t.ok(end.spot && end.spot.e === d0.e && end.watched === 1, 'the call sends an officer to the spot, and the ground is watched', end);
await C(() => { LEDGER.goTo({ xMetres: 3.0, zMetres: -50 }); LEDGER.G.tom.ang = Math.PI; }); // he steps well back up the street to watch
const pc0 = await C(() => { const P = LEDGER.G.people.pc; return { x: P.x, z: P.z, gone: P.gone, space: P.space }; });
const arr = await stepFor(40, () => LEDGER.game.law.x().spot && LEDGER.game.law.x().spot.st === 'there');
const pc1 = await C(() => { const P = LEDGER.G.people.pc, sp = LEDGER.game.law.x().spot; return { x: P.x, z: P.z, gone: P.gone, space: P.space, st: sp && sp.st, d: sp && Math.hypot(P.x - sp.x, P.z - sp.z), notes: LEDGER.G.ledger.notes.filter((n) => /constable at the spot/i.test(n.text)).length }; });
t.ok(pc1.st === 'there' && pc1.d < 4 && !pc1.gone && pc1.space === 'street' && arr.s <= 20, 'the constable has come down the street himself and stands at the spot inside twenty game minutes or so', { arr: arr.s, pc0, pc1 });
// going back there is the risk: he walks back to the window, the officer sees him and stops him
await C(() => { LEDGER.goTo({ xMetres: 6.2, zMetres: -33 }); LEDGER.G.tom.ang = 0; });
const back = await stepFor(12, () => LEDGER.written.read().open);
const ch = await C(() => LEDGER.written.read());
t.ok(ch.open && ch.speakerPersonId === 'pc' && /Back for another look/.test(ch.text) && ch.choices.length === 3, 'back at the watched spot he is challenged, with three answers', ch);
t.ok(back.said.concat(arr.said).some((l) => /constable/i.test(l)), 'he could read the officer at the spot from what was on screen', back.said.concat(arr.said));
await t.h.key('Digit1'); await t.h.sleep(800);
const ch2 = await C(() => ({ w: LEDGER.written.read(), ch: LEDGER.game.law.x().challenges.slice(-1)[0] }));
t.ok(ch2.ch && ch2.ch.result === 'searched', 'he stands and is searched', ch2);
await t.done();
