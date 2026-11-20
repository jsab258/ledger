// REACHING THE WITNESS FIRST, and FINDING AN UNSEEN DEED, played through (parts 1.4.5, 2.5.5; ruling 3 Oct; A38).
// One: a window put in with a witness by; he walks up to her on her way and presses E; a threat stops the call,
// never the street's talk; by morning no statement is on record and nobody comes for him.
// Two: a window put in with nobody about; the first named person whose own day brings them past it finds it,
// holds only the aftermath, and rings the police; an officer comes to the spot, and no arrest follows.
// Set by hand: who stands where, and the hour. The rest is key presses and game time.
import { start } from './lib.mjs';
const t = await start({ port: 8882 });
const C = (fn, ...a) => t.ev(fn, ...a);
const subs = () => t.h.page.evaluate(() => [...document.querySelectorAll('#subs .s')].map((e) => e.textContent));
const stepFor = async (secs, until) => { let said = []; for (let s = 0; s < secs; s += 0.5) { await t.h.step(0.5); for (const l of await subs()) if (!said.includes(l)) said.push(l); if (until && (await C(until))) return { s: s + 0.5, said }; } return { s: secs, said }; };
const walkTo = async (id, secs = 25) => {
  // he goes after her on foot at a run: Shift and W held, the view turned towards her as the mouse would turn it
  for (let s = 0; s < secs; s += 0.25) {
    const d = await C((id) => { const G = LEDGER.G, P = G.people[id], T = G.tom; LEDGER.cam.yaw = Math.atan2(P.x - T.x, P.z - T.z); dispatchEvent(new KeyboardEvent('keydown', { code: 'ShiftLeft', key: 'Shift' })); dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyW', key: 'w' })); LEDGER.step(0.25); return Math.hypot(P.x - T.x, P.z - T.z); }, id);
    if (d < 1.8) break;
  }
  await C(() => { dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyW', key: 'w' })); dispatchEvent(new KeyboardEvent('keyup', { code: 'ShiftLeft', key: 'Shift' })); LEDGER.step(0.1); });
};

// ---- one: reached first ----
const who = await C(() => {
  const G = LEDGER.G;
  G.t = Math.floor(G.t / 1440) * 1440 + 23 * 60;
  LEDGER.goTo({ xMetres: -7.2, zMetres: -33.4 });
  const P = ['grace', 'lily', 'susan', 'peter', 'sylvia', 'alison'].map((id) => G.people[id]).find((p) => p && p.def.upright && !p.def.nostmt && !p.dead && (p.def.nerve ?? 0.5) < 0.7);
  Object.assign(P, { override: { where: 'pave', act: 'idle' }, gone: false, space: 'street', awake: true, x: -5.0, z: -31.4, route: null, hold: true, moving: false });
  P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z);
  P.mind.fam = 1;
  for (const Q of G.named) if (Q !== P && !Q.def.police) { Q.override = { where: 'off', act: 'idle' }; Q.gone = true; Q.space = 'off'; Q.route = null; } // an empty street but for her
  G.money.clean += 5000; G.hooks.flow('world', 'pocket', 5000, 'test money');
  LEDGER.step(0.2);
  return { id: P.id, nerve: P.def.nerve, fear: P.mind.fear, money: G.money.clean };
});
await t.h.key('KeyG');
const go = await stepFor(20, () => LEDGER.game.walks.live().some((w) => w.st === 'going'));
t.ok(go.s <= 12, 'she means to tell and is going', go.s);
await stepFor(24, () => LEDGER.game.walks.x().walks[0].moving); // she stands, then sets off up the street
await stepFor(2);
await walkTo(who.id);
const pr = await C(() => LEDGER.prompts());
t.ok(pr.some((q) => q.key === 'E'), 'beside her on her way, E is offered', pr);
await t.h.key('KeyE'); await t.h.sleep(700);
const sc = await C(() => LEDGER.written.read());
if (!sc.open) console.log('dbg', JSON.stringify(await C((id) => ({ rd: LEDGER.read().boxOpen, talk: LEDGER.talk.state(), w: LEDGER.game.walks.x().walks, d: Math.hypot(LEDGER.G.people[id].x - LEDGER.G.tom.x, LEDGER.G.people[id].z - LEDGER.G.tom.z) }), who.id)), JSON.stringify(pr));
t.ok(sc.open && sc.speakerPersonId === who.id && /ring them/.test(sc.text) && sc.choices.length === 5, 'she stops and says what she saw; five answers: talk round, pay, threaten, put it right, step aside', sc);
const iThreat = sc.choices.findIndex((c) => /what happens to people who talk/.test(c));
await t.h.key('Digit' + (iThreat + 1)); await t.h.sleep(900);
const sc2 = await C(() => LEDGER.written.read());
if (sc2.open) { await t.h.key('KeyE'); await t.h.sleep(600); await t.h.key('KeyE'); await t.h.sleep(600); }
const after = await C((id) => { const G = LEDGER.G, P = G.people[id], x = LEDGER.game.walks.x(), E = G.events.find((e) => e.kind === 'window_in'), th = G.events.find((e) => e.kind === 'threat'); return { st: x.walks.find((w) => w.who === id).st, others: x.walks.filter((w) => w.who !== id).map((w) => w.who), reached: x.reached, fear: P.mind.fear, regard: P.mind.regard, threat: th && { target: th.target, hers: !!P.mind.by[th.id] }, arrest: G.story.arrest, stmt: E.stmt, e: E.id, notes: G.ledger.notes.filter((n) => /Stopped .* on the way to the phone box/.test(n.text)).map((n) => n.text), box: LEDGER.written.read().open }; }, who.id);
t.ok(after.st === 'stopped' && after.reached[0].choice === 'threaten' && after.reached[0].stopped && after.fear >= 0.5, 'the threat frightens her off the call', after);
t.ok(after.threat && after.threat.target === who.id && after.threat.hers, 'the threat is itself a thing done to her, which she holds and the street may hear', after.threat);
t.ok(after.notes.length === 1 && /The street will still hear of it/.test(after.notes[0]), 'the Ledger says the call was stopped and the talk was not', after.notes);
// she turns away from the phone box, and by ten next morning nothing is on record
const away = await stepFor(20);
const morn = await C((id) => { const G = LEDGER.G, P = G.people[id]; const d0 = Math.hypot(P.x - 6, P.z + 11.2); LEDGER.game.test.pass((24 + 10) * 60 - (G.t % 1440)); const E = G.events.find((e) => e.kind === 'window_in'); return { d0, arrest: G.story.arrest, stmt: E.stmt, statements: LEDGER.game.walks.x().statements, spot: LEDGER.game.law.x().spot, hour: (G.t % 1440) / 60, given: P.mind.stmtGiven, knows: !!P.mind.by[E.id] }; }, who.id);
t.ok(morn.d0 > 5, 'she did not go on to the phone box', morn.d0);
t.ok(!morn.arrest && !morn.stmt.length && !morn.statements.length && !morn.given && morn.knows, 'by ten next morning there is no statement and nobody has come for him; she still knows what she saw', morn);

// (the beat constable may have stopped a man with a suitcase at midnight: he has a word, and is let go)
for (let i = 0; i < 6 && (await C(() => LEDGER.written.read().open)); i++) { const w = await C(() => LEDGER.written.read()); await t.h.key(w.waitsForAChoice ? 'Digit3' : 'KeyE'); await t.h.sleep(700); }
// ---- two: an unseen deed is found by whoever really passes ----
const un = await C(() => {
  const G = LEDGER.G;
  G.t = Math.floor(G.t / 1440) * 1440 + 23.5 * 60;
  for (const Q of G.named) Q.override = null; // the town goes back to its own days
  LEDGER.goTo({ xMetres: -101.5, zMetres: 28 });
  LEDGER.game.crime.x().dogQuietUntilT = G.t + 600; // the yard dog has had its scrap
  LEDGER.step(0.2);
  return { prompts: LEDGER.prompts(), box: LEDGER.read().boxOpen, pc: [LEDGER.G.people.pc.x, LEDGER.G.people.pc.z], law: { w: LEDGER.game.law.x().watched, sp: LEDGER.game.law.x().spot, ch: LEDGER.game.law.x().challenges, back: LEDGER.game.law.x().backAtTheSpot } };
});
t.ok(un.prompts.some((q) => /Force the door/.test(q.text) && q.key === 'G'), "Iveson's hut on the quay at half past eleven, nobody about: the loud way in is offered", un);
await t.h.key('KeyG');
const d1 = await C(() => { const G = LEDGER.G, E = G.events.slice().reverse().find((e) => e.kind === 'forced_door'); return { e: E.id, wit: E.wit, traces: LEDGER.game.traces.open(), walks: LEDGER.game.walks.live().filter((w) => w.e === E.id).length }; });
t.ok(d1.e && !d1.wit.some((id) => !/^(yardlad|c\d+)$/.test(id)) && d1.traces.some((q) => q.kind === 'door') && !d1.walks, 'nobody who could name him saw it; the forced door is there to be found', d1);
// he goes home; the night passes; the town's own mornings bring people past
const fd = await C(async (e) => {
  const G = LEDGER.G;
  LEDGER.game.crime.x().inside = null; LEDGER.goTo({ xMetres: -5.4, zMetres: 27.5 });
  let found = null;
  for (let i = 0; i < 16 * 12 && !found; i++) { LEDGER.game.test.pass(5, false); found = LEDGER.game.traces.x().list.find((q) => q.e === e).found; }
  const P = found && G.people[found.by];
  return { found, hour: (G.t % 1440) / 60, real: !!P && !P.anon, name: P && P.def.name, d: P && Math.hypot(P.x - -101.5, P.z - 28), space: P && P.space, mem: P && P.mind.by[e] && { who: P.mind.by[e].who, sure: P.mind.by[e].sure, aftermath: P.mind.by[e].aftermath }, walk: LEDGER.game.walks.x().walks.find((w) => w.e === e) };
}, d1.e);
t.ok(fd.found && fd.real && (fd.d < 16 || fd.space === 'hut'), 'a named person whose own day brought them past it found it: nobody made up, no roll', fd);
t.ok(fd.mem && fd.mem.who === 'man' && fd.mem.aftermath === 1, 'the finder holds only the aftermath: somebody did this, not who', fd.mem);
t.ok(fd.walk && fd.walk.who === fd.found.by && fd.walk.aftermath, 'and sets off to ring the police as a witness would', fd.walk);
const rep = await C((e) => { const G = LEDGER.G; for (let i = 0; i < 90 && LEDGER.game.walks.live().length; i++) LEDGER.game.test.pass(5, false); const law = LEDGER.game.law.x(); return { st: LEDGER.game.walks.x().walks.find((w) => w.e === e).st, watched: law.watched.filter((w) => w.e === e).length, arrest: G.story.arrest, stmts: LEDGER.game.walks.x().statements.filter((s) => s.e === e) }; }, d1.e);
t.ok(rep.st === 'told' && rep.watched === 1 && !(rep.arrest && rep.arrest.e === d1.e) && rep.stmts.length === 1 && !rep.stmts[0].arrest, 'the report brings an officer to the spot and no arrest: nobody named him (ER-POL-01)', rep);
await t.done();
