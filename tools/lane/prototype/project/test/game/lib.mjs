// The whole game's in-game tests: one seeded page, the game stepped by hand through its hook. Each test prints
// "ok" or "TEST FAIL" lines and ends with PASS or FAIL (the rule of run_proto_tests.py).
import { launch } from '../harness.mjs';

export async function start(o = {}) {
  const h = await launch(Object.assign({ seed: 20261120, quality: 'low', width: 640, height: 400, port: 8870 }, o));
  await h.newWeek();
  await h.page.evaluate(() => LEDGER.game.town.ready());
  await h.settle();
  // these tests were written with Tom starting at the foot of the office stair; he arrives at the ferry landing now
  if (!o.atLanding) await h.page.evaluate(() => { LEDGER.goTo({ xMetres: -5.4, zMetres: 27.5 }); LEDGER.G.tom.ang = 0.6; });
  let bad = 0;
  const t = {
    h,
    ev: h.ev,
    ok(cond, what, got) {
      if (cond) console.log('ok   ' + what);
      else {
        bad++;
        console.log('TEST FAIL ' + what + (got !== undefined ? ' | got ' + JSON.stringify(got) : ''));
      }
      return !!cond;
    },
    // game minutes pass with Tom out of the way (asleep, as a skip) or where he stands
    pass: (minutes, hidden = true) => h.ev((m, hid) => LEDGER.game.test.pass(m, hid), minutes, hidden),
    async done() {
      const faults = await h.page.evaluate(() => LEDGER.game.faults.slice(0, 5));
      t.ok(!faults.length, 'no fault inside any system', faults);
      t.ok(!h.errors.length, 'no page error', h.errors.slice(0, 3));
      console.log(bad ? 'FAIL' : 'PASS');
      await h.close();
      process.exit(bad ? 1 : 0);
    },
  };
  return t;
}
