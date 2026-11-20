// Shared by the spine's tests (acts, endings, ledgerx, firsthour): small helpers over the test hook.
export function drive(h) {
  const L = (fn, ...a) => h.ev(fn, ...a);
  let ok = true;
  const check = (name, pass, detail = '') => {
    console.log(`${pass ? 'ok  ' : 'TEST FAIL'} ${name}${pass || !detail ? '' : ' | ' + detail}`);
    if (!pass) ok = false;
    return pass;
  };
  // read a written scene to its end; pick(w) gives the choice to take (default the first)
  const clear = async (pick = () => 0, max = 120) => {
    const said = [];
    let idle = 0;
    for (let i = 0; i < max && idle < 4; i++) {
      const w = await L(() => LEDGER.written.read());
      if (!w.open && (await L(() => LEDGER.read().boxOpen)) === 'talk') {
        await L(() => LEDGER.talk.leave()); // a talk left open would hold the game for good
        await h.step(0.2);
        continue;
      }
      if (!w.open) {
        idle++;
        await h.step(0.25);
        continue;
      }
      idle = 0;
      said.push((w.speaker || '') + ': ' + w.text);
      if (w.choices) {
        let n = pick(w);
        if (typeof n === 'string') n = Math.max(0, w.choices.findIndex((c) => c.includes(n)));
        said.push('  > ' + w.choices[n]);
        await L((n) => LEDGER.written.choose(n), n);
      } else await L(() => LEDGER.written.next());
      await h.step(0.1);
    }
    return said;
  };
  const read = () => L(() => LEDGER.read());
  // step until fn() in the page is true (or give up)
  const until = async (fn, secs = 40, each = 0.5) => {
    for (let t = 0; t < secs; t += each) {
      if (await L(fn)) return true;
      await h.step(each);
      await new Promise((r) => setTimeout(r, 20));
    }
    return !!(await L(fn));
  };
  const pastIntros = () =>
    L(() => {
      const G = LEDGER.G;
      Object.assign(G.story.flags, { tour1: 1, tour: 1, metRon: 1, metDarren: 1, metPauline: 1, metJune: 1, metSylvia: 1, metWalsh: 1, ask1: 'no', unpacked: 1, adaSaw: 1, fh: 'done' });
      G.story.lastSleepDay = 99;
      G.car.keys = true;
      G.tom.carry = null;
    });
  const faults = () => L(() => LEDGER.game.faults.slice());
  const passTo = async (gameMinute) => {
    await L((t) => { LEDGER.passTime(t, ''); }, gameMinute);
    await until(() => !LEDGER.read().paused || LEDGER.read().boxOpen === 'dialog', 60);
  };
  return { L, check, clear, read, until, pastIntros, faults, passTo, ok: () => ok };
}
