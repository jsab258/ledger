// The way system (6.9, DESIGN-ADDENDUM A9): ER-WAY-02 every place has an address, a landmark and a label, and stands
// on open ground; people asked give the way by landmark if they know it; ER-WAY-03 the nudge when lost fires once
// per goal and never inside 90 s; after three minutes the next person he passes offers the way.
import { launch } from '../harness.mjs';
let bad = 0;
const ok = (c, m) => { console.log((c ? 'ok   ' : 'TEST FAIL ') + m); if (!c) bad++; };
const h = await launch({ port: 8830, quality: 'low', seed: 1990 });
try {
  await h.newWeek();
  const r = await h.ev(() => {
    const W = LEDGER.game.way, ps = W.places();
    const needed = ['mickeys', 'rank', 'yard', 'regent', 'caff', 'ritas', 'coin', 'adas', 'chapel', 'priesthouse', 'landing', 'shelter', 'quay', 'smokehouse', 'fishdock', 'coldstore', 'warehouserow', 'no4', 'scrapyard', 'hut', 'customs', 'harbour', 'phonebox_qs', 'phonebox_quay', 'launderette', 'newsagent', 'ironmonger', 'outfitter', 'solicitor', 'carlot', 'ferryrank', 'stationrank', 'dockgate', 'boxing', 'doctor', 'station_police', 'west_road', 'north_road'];
    return {
      n: ps.length,
      lacks: W.lacks(),
      missing: needed.filter((id) => !ps.some((p) => p.id === id)),
      inWall: ps.filter((p) => LEDGER.isBlocked(p.x, p.z) && !p.room).map((p) => p.id),
      offMap: ps.filter((p) => p.x < -130 || p.x > 162 || p.z < -226 || p.z > 112).map((p) => p.id),
      keeper: W.directions('shelter', 'k_news'),
      june: W.directions('doctor', 'june'),
      ron: W.directions('doctor', 'ron'),
      words: [W.placeByWords('a holdall under the bench in the landing shelter'), W.placeByWords("Find Mickey's. The letter says Quay Street"), W.placeByWords('nothing here')],
      hook: typeof LEDGER.G.hooks.wayTo === 'function' && /shelter/.test(LEDGER.G.hooks.wayTo('shelter')),
    };
  });
  ok(r.n >= 55, 'places on the list: ' + r.n);
  ok(r.missing.length === 0, 'every place the game names is there' + (r.missing.length ? ', missing ' + r.missing : ''));
  ok(r.lacks.length === 0, 'ER-WAY-02: every place has an address, a landmark and a label ' + JSON.stringify(r.lacks));
  ok(r.offMap.length === 0, 'every place is on the map ' + r.offMap);
  ok(r.inWall.length === 0, 'street places stand on open ground (inside something solid: ' + r.inWall + ')');
  ok(/bench/.test(r.keeper) && !/\d+ m\b|north|south|east of here/.test(r.keeper), 'a shopkeeper gives the way by landmark: ' + r.keeper);
  ok(/No idea/.test(r.june) && /bell pull/.test(r.ron), 'an incomer says no idea, Ron knows the old doctor: ' + r.june + ' | ' + r.ron);
  ok(r.words[0] === 'shelter' && r.words[1] === 'mickeys' && r.words[2] === null, 'a line of words names its place: ' + r.words);
  ok(r.hook, 'G.hooks.wayTo is there for the other systems');
  // lost: stand still on Copper Row with the chapel as the goal
  await h.ev(() => { LEDGER.goTo && 0; const G = LEDGER.G; G.tom.x = 150; G.tom.z = 48; G.tom.space = 'street'; LEDGER.game.way.setGoal('chapel', 'test'); });
  await h.step(88);
  const a = await h.ev(() => LEDGER.game.way.state());
  ok(a.nudges.length === 0, 'ER-WAY-03: no nudge inside 90 s (' + Math.round(a.lost.since) + ' s without progress)');
  await h.step(6);
  const b = await h.ev(() => ({ s: LEDGER.game.way.state(), sub: document.getElementById('sub') ? document.getElementById('sub').textContent : '' }));
  ok(b.s.nudges.length === 1 && b.s.nudges[0].kind === 'nudge', 'the nudge fires once after 90 s: ' + JSON.stringify(b.s.nudges));
  await h.step(60);
  const c = await h.ev(() => LEDGER.game.way.state());
  ok(c.nudges.length === 1, 'ER-WAY-03: and only once for the goal (nobody near): ' + c.nudges.length);
  // somebody passes within 5 m after three minutes: the way is offered
  await h.step(40);
  await h.ev(() => { const G = LEDGER.G, A = G.crowd.find((P) => P.space === 'street' && !P.gone); Object.assign(A, { x: 151.5, z: 48, hold: true, route: null, moving: false }); });
  await h.step(3);
  const d = await h.ev(() => ({ s: LEDGER.game.way.state(), told: LEDGER.G.hooks.placeKnown('chapel'), led: LEDGER.G.ledger.notes.some((n) => /chapel/i.test(n.text || '')) }));
  ok(d.s.nudges.length === 2 && d.s.nudges[1].kind === 'offer', 'after three minutes the next person within 5 m offers the way: ' + JSON.stringify(d.s.nudges));
  ok(d.told, 'and the place is now one Tom has been told of (for the paper map)');
  // walking toward it counts as progress: no further nudge, and arriving clears a set goal
  await h.ev(() => { const G = LEDGER.G; G.tom.x = -12; G.tom.z = -66; });
  await h.step(3);
  const e = await h.ev(() => ({ s: LEDGER.game.way.state(), f: LEDGER.game.faults.slice() }));
  ok(e.s.goal === null, 'arriving ends the goal');
  ok(e.f.length === 0, 'no faults in the game systems ' + e.f.join(' | '));
  ok(h.errors.length === 0, 'no page errors' + (h.errors.length ? ': ' + h.errors.join(' | ') : ''));
} finally {
  await h.close();
}
console.log(bad ? `FAIL: ${bad} checks` : 'PASS');
process.exit(bad ? 1 : 0);
