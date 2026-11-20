// The endings (parts 3.1.4, 3.1.5, 6.2.5, 7.15): every ending by a scripted route, a hunted man's included
// (ER-END-01); the signs shown before the close agree with the ending, and Tom's reading predicts it (ER-END-02, 03);
// after the credits he walks the town within 10 s, or quits to the title (ER-AFTER-01).
import { launch } from '../harness.mjs';
import { drive } from './spine_drive.mjs';
const h = await launch({ port: 8862, quality: 'low' });
const { L, check, read, until, pastIntros, faults, ok } = drive(h);
try {
  await h.newWeek();
  await pastIntros();
  const quiet = await L(() => LEDGER.game.endings.reading());
  check('with no sign given, his reading says nothing has come due', quiet.quiet && /Nothing has come due/.test(quiet.text.join(' ')), JSON.stringify(quiet.text));
  const WANT = { both: ['both', 'The Kingdom'], kingdom: ['kingdom', 'The Kingdom'], quiet: ['quiet', 'The Straight Life'], straight: ['straight', 'The Straight Life'], burn: ['burn', 'Burn Both'], hunted: ['burn', 'Burn Both'] };
  const seen = new Set();
  for (const name of Object.keys(WANT)) {
    await L((name) => { const s = LEDGER.game.x().endings; s.ended = null; s.signs = {}; s.after = 0; LEDGER.G.story.phase = 'play'; LEDGER.game.endings.route(name); }, name);
    await until(() => !!LEDGER.game.endings.read().ended, 20);
    await h.step(1.5); await h.key('Space'); await h.step(1);
    const up = await until(() => LEDGER.read().boxOpen === 'credits-end', 40);
    const s = await L(() => LEDGER.game.endings.read());
    const e = s.ended || {};
    seen.add(e.shown);
    check(`route ${name}: ends as ${WANT[name][1]} (${WANT[name][0]})`, up && e.state === WANT[name][0] && e.shown === WANT[name][1], JSON.stringify(e));
    check(`route ${name}: every deciding cost had shown its sign, and his reading predicted the state`, e.predicted === e.state && Object.keys(s.signs).length >= 1, JSON.stringify(Object.keys(s.signs)));
    const body = await L(() => document.getElementById('book').textContent);
    check(`route ${name}: the close names the ending and gives both ways on`, body.includes(WANT[name][1]) && /Walk the town/.test(body) && /Quit to the title/.test(body));
    const t1 = Date.now();
    await h.page.click('[data-act="afterend"]'); await h.step(0.4);
    const r = await read();
    check(`route ${name}: control back in the town within 10 s`, r.phase === 'play' && !r.paused && Date.now() - t1 < 10000, JSON.stringify({ phase: r.phase, paused: r.paused }));
  }
  check('three endings are shown, no more', seen.size === 3, [...seen].join(', '));
  check('the Ledger\'s last page says the story is told', await L(() => LEDGER.ledger.book().some((e) => /The story is told/.test(e.what))));
  check('the Open part carries Tom\'s reading', await L(() => { LEDGER.ledger.open('open'); const t = document.getElementById('lmain').textContent; LEDGER.ledger.close(); return /How things stand/.test(t); }));
  check('no number of standing or heat in the reading (ER-RISE-01)', !/\d/.test((await L(() => LEDGER.game.endings.reading().text.join(' ')))));
  const f = await faults();
  check('no system fault', f.length === 0, f.slice(0, 3).join(' | '));
  check('no page error', h.errors.length === 0, [...new Set(h.errors)].slice(0, 3).join(' | '));
} catch (e) { check('the test ran to its end', false, String(e.stack || e).slice(0, 700)); }
await h.close();
console.log(ok() ? 'PASS' : 'FAIL');
process.exit(ok() ? 0 : 1);
