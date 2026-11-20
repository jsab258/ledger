// The shops system (2.7.5, 2.7.8, 1.6.10; DESIGN-ADDENDUM A21, A30): ER-SPEND-01 every shop sells only its list, by
// its hours, from its stock and purse; ER-HAGGLE-01 a haggle is three offers at most and shows only the prices
// spoken; ER-COAT-01 a new coat leaves a witness of the old one with a shape; the wardrobe survives save and load.
import { launch } from '../harness.mjs';
let bad = 0;
const ok = (c, m) => { console.log((c ? 'ok   ' : 'TEST FAIL ') + m); if (!c) bad++; };
const h = await launch({ port: 8831, quality: 'low', seed: 1990 });
const at = (d, hr) => h.ev((d, hr) => { LEDGER.G.t = d * 1440 + hr * 60; LEDGER.step(0.1); }, d, hr);
const total = () => h.ev(() => LEDGER.G.money.clean + LEDGER.G.money.dirty);
try {
  await h.newWeek();
  await h.ev(() => { LEDGER.G.money.clean = 20000; });
  await at(1, 11); // Tuesday, eleven
  const r = await h.ev(() => {
    const S = LEDGER.game.shops, l = S.list();
    return { n: l.length, noPlace: l.filter((s) => !LEDGER.game.way.places().some((p) => p.id === s.place)).map((s) => s.id), wrong: S.buy('ironmonger', 'a good overcoat'), open: l.filter((s) => s.open).map((s) => s.id) };
  });
  ok(r.n >= 9 && r.noPlace.length === 0, `shops: ${r.n}, each at a place on the list ${r.noPlace}`);
  ok(r.wrong.ok === false && r.wrong.why === 'not sold here', 'ER-SPEND-01: a shop sells only its list: ' + JSON.stringify(r.wrong));
  const m0 = await total();
  const b = await h.ev(() => ({ r: LEDGER.game.shops.buy('ironmonger', 'a torch'), items: Object.assign({}, LEDGER.G.tom.items) }));
  ok(b.r.ok && b.r.pricePence === 320 && b.items.torch === 1 && m0 - (await total()) === 320, 'a torch at the ironmonger: in the pocket, and the money down by exactly its price: ' + JSON.stringify(b.r));
  const c = await h.ev(() => [LEDGER.game.shops.buy('ironmonger', 'a crowbar'), LEDGER.game.shops.buy('ironmonger', 'a crowbar'), LEDGER.game.shops.buy('ironmonger', 'a crowbar')]);
  ok(c[0].ok && c[1].ok && !c[2].ok && c[2].why === 'none left this week', 'ER-SPEND-01: only from its stock: the third crowbar is refused: ' + c[2].why);
  const rs = await h.ev(() => { LEDGER.game.shops.restockNow(1); return LEDGER.game.shops.buy('ironmonger', 'a crowbar'); });
  ok(rs.ok, 'the weekly restock brings the crowbars back');
  const key = await h.ev(() => LEDGER.game.shops.buy('ironmonger', 'a key cut'));
  ok(!key.ok && key.why === 'nothing to copy', 'a key is cut only from a key: ' + key.why);
  await at(1, 22);
  const shut = await h.ev(() => ({ r: LEDGER.game.shops.buy('ironmonger', 'a torch'), doc: LEDGER.game.shops.open('doctor') }));
  ok(!shut.r.ok && shut.r.why === 'shut' && shut.doc, 'ER-SPEND-01: only by its hours: shut at ten at night; the old doctor answers his bell at any hour');
  await at(6, 11); // Sunday
  const sun = await h.ev(() => ({ iron: LEDGER.game.shops.open('ironmonger'), caff: LEDGER.game.shops.open('caff') }));
  ok(!sun.iron && sun.caff, 'ER-CAL-01: shops shut on Sunday, the caff open');
  await at(8, 11);
  const poor = await h.ev(() => { const m = LEDGER.G.money, keep = m.clean; m.clean = 100; m.dirty = 0; const r = LEDGER.game.shops.buy('outfitter', 'a decent jacket'); m.clean = keep; return r; });
  ok(!poor.ok && poor.why === 'not enough money', 'no tick: ' + poor.why);
  // ER-COAT-01: Albert tied a deed to the coat; a new night coat leaves him with a shape
  const coat = await h.ev(() => {
    const G = LEDGER.G, A = G.people.albert, t = G.tom;
    t.hasCoat = true; t.coat = true;
    const id = LEDGER.ledger.act('night_out', { silent: true });
    const E = G.ev[id];
    const mem = { e: id, src: 'saw', from: null, who: 'coat', sure: 0.8, heat: 0.5, t: G.t, said: false, hop: 0, face: 0 };
    A.mind.mem.push(mem); A.mind.by[id] = mem; A.mind.knowsCoat = 1;
    t.coat = false;
    const r = LEDGER.game.shops.buy('secondhand', 'a dark donkey jacket');
    return { r, who: A.mind.by[id].who, knows: A.mind.knowsCoat, sure: A.mind.by[id].sure, dress: LEDGER.game.shops.dress(), w: LEDGER.game.shops.state().wardrobe, coatEv: !!E.coat };
  });
  ok(coat.r.ok && coat.who === 'man' && coat.knows === 0 && coat.sure < 0.8, 'ER-COAT-01: after a new coat the witness of the old one holds a shape, not a mark: ' + JSON.stringify({ who: coat.who, sure: coat.sure }));
  ok(coat.w.owned.dark === 1 && coat.w.night === 'dark', 'the donkey jacket is his night coat now');
  const jk = await h.ev(() => ({ r: LEDGER.game.shops.buy('outfitter', 'a decent jacket'), d: LEDGER.game.shops.dress(), hook: LEDGER.G.hooks.dress().standing }));
  ok(jk.r.ok && jk.d.dayCoat === 'jacket' && jk.d.standing === 1 && jk.hook === 1, 'a decent jacket changes how he stands with strangers, read by others as G.hooks.dress()');
  const hs = await h.ev(() => { LEDGER.game.shops.buy('outfitter', 'a hat'); LEDGER.game.shops.buy('outfitter', 'a scarf'); const x = LEDGER.G.x.shops.wardrobe; x.up = true; LEDGER.G.t = 8 * 1440 + 23 * 60; const night = LEDGER.game.shops.dress(); LEDGER.G.t = 8 * 1440 + 12 * 60; const noon = LEDGER.game.shops.dress(); x.up = false; return { night, noon }; });
  ok(hs.night.catchCap === 2 && hs.noon.catchCap === 4 && hs.noon.drawsALook, 'scarf up and hat down break the face rung at night, and by day draw a look');
  // the haggle (A30)
  await at(8, 11);
  const hg = await h.ev(() => {
    const S = LEDGER.game.shops, goods = { id: 'g1', name: 'a carriage clock', kind: 'goods', honestPence: 4000, hot: 0.5 };
    const not = S.startHaggle('coin', { id: 'g2', name: 'a drill', kind: 'tools', honestPence: 3000, hot: 0 });
    const again = S.startHaggle('coin', { id: 'g2', name: 'a drill', kind: 'tools', honestPence: 3000, hot: 0 });
    let hh = S.startHaggle('secondhand', goods); const first = JSON.parse(JSON.stringify(hh)); let asks = 0;
    while (!hh.done && asks < 10) { hh = S.haggle(hh, 'more'); asks++; }
    let h2 = S.startHaggle('secondhand', goods); h2 = S.haggle(h2, 'more'); h2 = S.haggle(h2, 'take');
    const purse0 = S.list().find((s) => s.id === 'secondhand').pursePence, d0 = LEDGER.G.money.dirty;
    S.settle('secondhand', goods, h2);
    return { not, again, first, asks, ended: hh, h2, purse: purse0 - S.list().find((s) => s.id === 'secondhand').pursePence, dirty: LEDGER.G.money.dirty - d0, ev: LEDGER.G.events[LEDGER.G.events.length - 1].kind };
  });
  ok(hg.not.refused === 'not my line' && hg.again.refused === 'told you no', 'a shop refuses what is not its line, and remembers: ' + hg.not.refused + ' / ' + hg.again.refused);
  ok(hg.first.offers.length === 3 && hg.first.offers[0] < hg.first.offers[2] && hg.first.offers[0] < 4000 * 0.4, 'the fence opens under 0.4 for warm goods and has three offers: ' + hg.first.offers);
  ok(hg.asks === 3 && hg.ended.done && !hg.ended.sold, 'ER-HAGGLE-01: asking for more a third time ends it: never more than three offers');
  ok(hg.h2.sold && hg.purse === hg.h2.pricePence && hg.dirty === hg.h2.pricePence && hg.ev === 'fenced', 'sold at the second offer: out of her purse, into the tin, and an act the town can know: ' + hg.h2.pricePence);
  // at the counter, with the hands: the prompt, the written choice
  const cn = await h.ev(() => { LEDGER.game.shops.goInto('newsagent'); return LEDGER.prompts(); });
  ok(cn.some((p) => p.key === 'G' && /counter/i.test(p.text)), 'in the shop, a prompt for the counter: ' + JSON.stringify(cn));
  await h.ev(() => LEDGER.press('G'));
  await h.sleep(300);
  const w1 = await h.ev(() => LEDGER.written.read());
  ok(w1.open && w1.choices && w1.choices.some((c) => /Mariners/.test(c)) && w1.choices.every((c) => !/[%]|\d+\/\d+/.test(c)), 'the counter offers its list with prices in words and pence only: ' + JSON.stringify(w1.choices));
  const m1 = await total();
  await h.ev(() => LEDGER.written.choose(1)); await h.sleep(200);
  for (let i = 0; i < 6; i++) { const w = await h.ev(() => LEDGER.written.read()); if (!w.open) break; if (w.choices) await h.ev((n) => LEDGER.written.choose(n), w.choices.length - 1); else await h.ev(() => LEDGER.written.next()); await h.sleep(150); }
  ok(m1 - (await total()) === 150, 'twenty Mariners bought at the counter: ' + (m1 - (await total())) + 'p');
  // save and load
  const sv = await h.ev(() => { const a = JSON.stringify(LEDGER.G.x.shops); LEDGER.saveNow(); const j = localStorage.getItem('ledger.save.v4'); LEDGER.restore(j); return { same: JSON.stringify(LEDGER.G.x.shops) === a, dress: LEDGER.game.shops.dress().dayCoat, f: LEDGER.game.faults.slice() }; });
  ok(sv.same && sv.dress === 'jacket', 'the shops, the purses and the wardrobe survive save and load');
  ok(sv.f.length === 0, 'no faults in the game systems ' + sv.f.join(' | '));
  ok(h.errors.length === 0, 'no page errors' + (h.errors.length ? ': ' + h.errors.join(' | ') : ''));
} finally {
  await h.close();
}
console.log(bad ? `FAIL: ${bad} checks` : 'PASS');
process.exit(bad ? 1 : 0);
