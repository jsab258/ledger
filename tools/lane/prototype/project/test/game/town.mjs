// The bridge (4a): the game's real town code runs in the page, is told what he is seen doing, gives back each
// hour's doings, and travels in the save.
import { start } from './lib.mjs';
const t = await start({ port: 8871 });
const r0 = await t.ev(() => ({ open: LEDGER.game.town.open(), fault: LEDGER.game.town.fault(), now: LEDGER.game.town.now(), t: LEDGER.G.t }));
t.ok(r0.open && !r0.fault, 'the real town is open in the page', r0);
t.ok(Math.abs(r0.now - Math.floor(r0.t)) <= 1, "the town's clock is the game's clock", r0);

// a blow in plain sight of Darren (of both casts) and Lee (the prototype's only): the town takes Darren's sighting
const a = await t.ev(() => {
  const G = LEDGER.G;
  LEDGER.goTo('rank');
  for (const id of ['darren', 'ron']) { const P = G.people[id]; P.override = null; P.gone = false; P.space = 'street'; P.awake = true; P.x = G.tom.x + 2; P.z = G.tom.z + (id === 'ron' ? 1 : -1); P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z); P.hold = true; P.mind.fam = 0.9; }
  G.tom.light = 1;
  const E = LEDGER.game.test.act('strike', { target: 'lee' });
  return { e: E.id, wit: E.wit, fed: LEDGER.game.town.x().fed, refused: LEDGER.game.town.x().refused };
});
t.ok(a.wit.includes('darren'), 'Darren saw the blow', a);
t.ok(Object.keys(a.fed).some((k) => k.endsWith(':darren')), "Darren's sighting was told to the real town", a);
t.ok(!a.refused.length, 'the town refused nothing', a.refused);

await t.pass(6 * 60);
const k = await t.ev((e) => LEDGER.game.town.knows().filter((x) => x.topic === 'player.strike_e' + e), a.e);
t.ok(k.some((x) => x.who === 'sam' && x.saw), 'the town holds it as seen by Darren (sam in the cast file)', k.slice(0, 2));
t.ok(k.length > 1, 'the real talk passed it on within six game hours', k.length);

// damage: the week's one deed, with a witness of both casts; next morning at nine she goes to the police
const d = await t.ev(() => {
  const G = LEDGER.G;
  const P = G.people.ada; P.override = null; P.gone = false; P.space = 'street'; P.awake = true; P.x = G.tom.x - 2; P.z = G.tom.z; P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z); P.hold = true; P.mind.fam = 0.9;
  const E = LEDGER.game.test.act('window_in', { thing: "the pawn shop's window", noiseR: 30 });
  return { e: E.id, wit: E.wit, deeds: LEDGER.game.town.x().deeds, held: LEDGER.game.town.deedHeld(), refused: LEDGER.game.town.x().refused };
});
t.ok(d.deeds.length === 1 && d.deeds[0].deed && d.held, 'a window put in is the deed the real week follows', d);
t.ok(d.deeds[0] && d.deeds[0].taken.includes('ada'), 'Ada is its witness in the real town', d.deeds);
const save1 = await t.ev(() => { LEDGER.saveNow(false); return LEDGER.saveText().length; });
t.ok(save1 > 1000, 'the save holds the town', save1);
await t.pass(22 * 60);
const w = await t.ev(() => ({ went: LEDGER.game.town.x().went, found: LEDGER.game.town.x().found.length, day: LEDGER.G.t / 1440 }));
t.ok(w.went.some((x) => x.who === 'ada'), 'Ada went to the police at nine the morning after', w);
t.ok(w.found >= 1, 'people whose routines pass it found the damage (A38)', w.found);

// the save: load it, and the town plays on from where it was
const back = await t.ev(async () => {
  const json = LEDGER.saveText();
  const stories = LEDGER.game.town.x().stories, now = LEDGER.game.town.now();
  LEDGER.restore(json);
  await LEDGER.game.town.ready();
  return { open: LEDGER.game.town.open(), fault: LEDGER.game.town.fault(), now0: now, now1: LEDGER.game.town.now(), stories, held: !!LEDGER.game.town.deedHeld() };
});
t.ok(back.open && !back.fault && back.now0 === back.now1 && back.held, 'a loaded save carries the town on, the deed still held', back);
await t.pass(3 * 60);
const on = await t.ev(() => ({ hours: LEDGER.game.town.hoursRun(), refused: LEDGER.game.town.x().refused }));
t.ok(on.hours > 20 && !on.refused.length, 'the hours keep coming after the load, nothing refused', on);

// ER-EYES-05: somebody told by the real town can print the chain back to the one who saw
const ch = await t.ev((e) => { const G = LEDGER.G; const who = Object.keys(G.people).find((id) => G.people[id].mind && G.people[id].mind.by[e] && G.people[id].mind.by[e].src === 'told'); return who ? { who, chain: LEDGER.game.town.chain(who, e) } : null; }, a.e);
t.ok(ch && ch.chain.length >= 1, 'a telling prints its chain (ER-EYES-05)', ch);
await t.done();
