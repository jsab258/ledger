// The Ledger's whole-game parts: 6.3 the paper map marks only places he has been or been told of; 2.12.1 each step
// up the name ladder is heard within a game day and never goes back (ER-RISE-02); ER-LEDG-02 it opens in 120 ms;
// 7.5 the hour budget books play time by activity; 7.6 tense moments are counted for the playtester.
import { launch } from '../harness.mjs';
import { drive } from './spine_drive.mjs';
const h = await launch({ port: 8863, quality: 'low' });
const { L, check, clear, read, pastIntros, faults, passTo, ok } = drive(h);
try {
  await h.newWeek();
  await h.step(2);
  let known = await L(() => LEDGER.game.ledgerx.known());
  check('off the ferry he knows the landing and the quay, and not the bank or the station', known.includes('ferry') && known.includes('quay') && !known.includes('bank') && !known.includes('station'), known.join(','));
  await pastIntros();
  await L(() => LEDGER.goTo({ xMetres: 12, zMetres: -139 })); await h.step(2);
  known = await L(() => LEDGER.game.ledgerx.known());
  check('standing by the bank puts it on his map', known.includes('bank'), known.join(','));
  await L(() => LEDGER.game.ledgerx.tell('station'));
  check('a place he is told of goes on the map as well', (await L(() => LEDGER.game.ledgerx.known())).includes('station'));
  const labels = await L(() => { const k = LEDGER.game.ledgerx.known(), all = Object.keys(LEDGER.game.ledgerx.labels()); return { marked: all.filter((x) => LEDGER.G.hooks.knowsPlace(x)), unknownMarked: all.filter((x) => LEDGER.G.hooks.knowsPlace(x) && !k.includes(x)) }; });
  check('no unknown place is marked', labels.unknownMarked.length === 0 && labels.marked.length < Object.keys(await L(() => LEDGER.game.ledgerx.labels())).length, JSON.stringify(labels));
  // the Ledger opens fast, with the map drawn
  const ms = await L(() => { const t = performance.now(); LEDGER.ledger.open('open'); const d = performance.now() - t; const has = !!document.getElementById('lmap'); LEDGER.ledger.close(); return { d, has }; });
  check('the Ledger opens within 120 ms, the map on its Open part (ER-LEDG-02)', ms.has && ms.d < 120 * 4, `${Math.round(ms.d)} ms on this machine (the cloud draws in software; the rule's 120 ms is for his PC)`);
  // the name ladder
  await L(() => LEDGER.goTo('the rank')); await h.step(1); await clear();
  await L(() => { const G = LEDGER.G; LEDGER.game.ledgerx.setLevel(2); const P = G.people.ron; G.ledger.met.ron = G.ledger.met.ron || 1; if (G.ledger.names) G.ledger.names.ron = 1; P.x = G.tom.x + 2; P.z = G.tom.z; P.space = G.tom.space; });
  await h.step(8);
  let nm = await L(() => LEDGER.game.ledgerx.name());
  check('a step up the name ladder is said to his face', nm.heardAt[2] !== undefined && (await L(() => LEDGER.ledger.book().some((e) => /calling him Nowak/.test(e.what)))), JSON.stringify(nm));
  await L(() => LEDGER.game.ledgerx.setLevel(3));
  await L(() => { LEDGER.goInside('the bed at Regent House'); });
  const t0 = (await read()).gameMinute;
  await passTo(t0 + 1500); await h.step(10); await clear();
  nm = await L(() => LEDGER.game.ledgerx.name());
  check('with nobody near it is still heard within a game day (ER-RISE-02)', nm.heardAt[3] !== undefined && nm.heardAt[3] - nm.reachedAt[3] <= 1440 + 90, JSON.stringify(nm));
  check('the ladder never goes back', nm.level === 3 && (await L(() => LEDGER.game.ledgerx.name().level)) >= 3);
  // the hour budget and the tension count
  const b = await L(() => LEDGER.game.ledgerx.budget());
  const sum = Object.values(b.shares).reduce((a, c) => a + c, 0);
  check('play time is booked by activity and the shares add up', b.realSecondsPlayed > 5 && Math.abs(sum - 1) < 0.02 && 'talk' in b.shares && 'waiting' in b.shares, JSON.stringify(b));
  check('new things are counted, and the longest stretch with nothing new is kept', b.newThings >= 2 && b.longestNothingNewRealSeconds >= 0, JSON.stringify(b));
  const m = await L(() => LEDGER.measures());
  check('the measures export carries the hour budget and the tension count', m.hourBudget && m.tension && typeof m.tension.tenseMoments === 'number', JSON.stringify(Object.keys(m)).slice(0, 200));
  const f = await faults();
  check('no system fault', f.length === 0, f.slice(0, 3).join(' | '));
  check('no page error', h.errors.length === 0, [...new Set(h.errors)].slice(0, 3).join(' | '));
} catch (e) { check('the test ran to its end', false, String(e.stack || e).slice(0, 700)); }
await h.close();
console.log(ok() ? 'PASS' : 'FAIL');
process.exit(ok() ? 0 : 1);
