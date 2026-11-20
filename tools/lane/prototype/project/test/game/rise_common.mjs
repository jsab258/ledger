// Shared by the rise's in-game tests (crew, rivals, rise, firm, dial, holdup): open the built page, start a new game,
// and step it by hand through the test hook. Each test runs on its own port.
import { launch } from '../harness.mjs';
export async function open(port, seed = 1990) {
  const h = await launch({ port, seed, quality: 'low' });
  await h.newWeek();
  let bad = 0;
  const ok = (cond, what, more) => {
    console.log((cond ? 'ok   ' : 'FAIL ') + what + (cond || more === undefined ? '' : ' :: ' + JSON.stringify(more)));
    if (!cond) bad++;
  };
  const done = async () => {
    const faults = await h.ev(() => LEDGER.game.faults.slice());
    ok(faults.length === 0, 'no fault in any system of the whole game', faults.slice(0, 3));
    ok(h.errors.length === 0, 'no page error', h.errors.slice(0, 3));
    // ER-RISE-01: no number of standing, loyalty or heat is ever on screen
    const words = await h.ev(() => document.body.innerText);
    ok(!/\b(loyalty|standing|heat|nerve|rung)\b\s*[:=]?\s*\d/i.test(words), 'ER-RISE-01 no number of standing, loyalty or heat on screen');
    await h.close();
    console.log(bad ? 'TEST FAIL' : 'PASS');
    process.exit(bad ? 1 : 0);
  };
  // the game clock moved on by game hours, in steps, with every system's hours and days run
  const hours = (n) => h.ev((n) => { const end = LEDGER.G.t + n * 60; let g = 0; while (LEDGER.G.t < end && g++ < 4000) { LEDGER.G.paused = false; LEDGER.step(2); } return LEDGER.G.t; }, n);
  return { h, ok, done, hours };
}
