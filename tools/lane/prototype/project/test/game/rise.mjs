// The rise (DESIGN section 14; parts 2.12.2, 2.12.3, 2.12.5, 7.7): rungs from holdings, heard within a day, never back.
import { open } from './rise_common.mjs';
const { h, ok, done, hours } = await open(8871);
const a = await h.ev(() => ({ rung: LEDGER.game.rise.rung(), called: LEDGER.game.rise.called(), hold: LEDGER.game.rise.holdings(), miss: LEDGER.game.rise.missing() }));
ok(a.rung === 1 && a.called === 'the new owner', 'a new game starts on rung 1, the new owner', a);
ok(a.hold.cars === 2 && a.hold.recruits === 0, 'he holds two cars and no recruit', a.hold);
ok(a.miss.includes('his answer to Sheila') && a.miss.includes('more cars') && a.miss.includes('a recruit'), 'what rung 2 still wants is read from what he holds', a.miss);
// rung 2 by holdings only: his answer, a third car, a first recruit
const b = await h.ev(() => {
  const G = LEDGER.G, g = LEDGER.game;
  const r0 = g.rise.check();
  G.story.flags.choice = 'take';
  const r1 = g.rise.check();
  g.firm.buy('car', { free: true });
  const r2 = g.rise.check();
  g.crew.recruit('julie', 'need');
  const r3 = g.rise.check();
  return { r0, r1, r2, r3, due: g.rise.due(), state: g.rise.state(), acc: g.rise.access('mickeysOffice'), gate: g.rise.access('dockGate') };
});
ok(b.r0 === 1 && b.r1 === 1 && b.r2 === 1 && b.r3 === 2, 'rung 2 lands only with his answer, a third car and a first recruit', b);
ok(b.acc.open && !b.gate.open, "rung 2 opens Mickey's office and not the dock gate (2.12.3)", [b.acc, b.gate]);
ok(/back door open/.test(b.state.office), 'the office reacts to the rung (2.12.5)', b.state.office);
await hours(24);
const c = await h.ev(() => ({ heard: LEDGER.game.rise.heard(), at: LEDGER.game.rise.state().at, notes: LEDGER.G.ledger.notes.filter((n) => /^called|^rung/.test(n.key || '')).map((n) => n.text) }));
ok(c.heard[2] && c.heard[2] - c.at[2] <= 1440, 'ER-RISE-02 the step up is heard within a game day', c);
ok(c.notes.some((t) => /Nowak/.test(t)), 'the Ledger keeps who called him Nowak', c.notes);
const d = await h.ev(() => {
  const g = LEDGER.game;
  g.firm.state().cars.pop();
  const r = g.rise.check();
  g.rise.introduce('lee');
  return { r, gate: g.rise.access('dockGate'), diff13: g.rise.differences(1, 3), diff34: g.rise.differences(3, 4) };
});
ok(d.r === 2, 'ER-RISE-02 a step never goes back when a holding is lost', d.r);
ok(d.gate.open && d.gate.by === 'an introduction', 'an introduction is a soft key to the dock gate (2.12.3)', d.gate);
ok(d.diff13.length >= 3 && d.diff34.length >= 3, 'ER-RISE-03 each rung changes at least three things a newcomer can point to', [d.diff13.length, d.diff34.length]);
// rungs 3 and 4 by test call, each landing as in play, saved and loaded
const e = await h.ev(() => {
  const g = LEDGER.game;
  const r = g.rise.set(4);
  const txt = LEDGER.saveText();
  return { r, st: g.rise.state(), sit: g.rise.access('sitDown'), saved: JSON.parse(txt).x.rise.rung };
});
ok(e.r === 4 && e.st.at[3] && e.st.at[4], 'set(4) climbs one rung at a time', e.st.at);
ok(!e.sit.open && e.sit.missing.includes('dress'), 'the sit-down wants a good overcoat as well as standing, or an appointment', e.sit);
ok(e.saved === 4, 'the rung is in the save');
await done();
