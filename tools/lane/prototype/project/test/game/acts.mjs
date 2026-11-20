// The acts (parts 3.1.1, 3.1.2, 3.1.3, 7.4, 7.9, 7.11): Act I closes and play goes on; Act II's beats fire on states
// and on quiet, never on a day; a wait stops for what the town has for him; the sit-down; the inspection week one
// morning at a time; and the books open. Played through the test hook, the game stepped by hand.
import { launch } from '../harness.mjs';
import { drive } from './spine_drive.mjs';
const h = await launch({ port: 8861, quality: 'low' });
const { L, check, clear, read, until, pastIntros, faults, passTo, ok } = drive(h);
try {
  await h.newWeek();
  await pastIntros();
  check('a new game is in Act I', (await L(() => LEDGER.game.acts.read().act)) === 1);
  // --- Act I closes on Sheila's answer, and play goes on (no end of the game there)
  await L(() => { LEDGER.endWeek('take'); });
  check('the close of Act I is shown', await until(() => LEDGER.read().boxOpen === 'end', 60));
  const html = await L(() => document.getElementById('book').textContent);
  check('the close gives Tom\'s reading and a way on', /The end of Act I/.test(html) && /Carry on/.test(html) && /The street calls him/.test(html));
  await h.page.click('[data-act="carryon"]');
  await h.step(0.5);
  let r = await read();
  check('after the close he is in control again, the same game', r.phase === 'play' && !r.paused && r.weekEnded, JSON.stringify({ phase: r.phase, paused: r.paused }));
  check('Sheila has her answer, and with nothing grown it is still Act I', await L(() => { const s = LEDGER.game.acts.read(); return s.answered && s.act === 1; }));
  // --- Act II opens on a state: the business has grown
  await L(() => { LEDGER.G.money.fareCount = 10; });
  await h.step(2);
  check('ten fares driven: Act II opens', (await L(() => LEDGER.game.acts.read().act)) === 2);
  const pend = await L(() => LEDGER.game.acts.read().pending);
  check('its first beat waits with a person, not a marker or the clock', pend && pend.id === 'opens' && pend.giver === 'sheila', JSON.stringify(pend));
  check('the giver has a word for him (her mark is up)', await until(() => LEDGER.G.people.sheila.mark === '!', 6));
  // through the person: go up to Sheila and press E
  await L(() => LEDGER.goInside("Mickey's Cars")); await h.step(0.5);
  await L(() => { const G = LEDGER.G, P = G.people.sheila, t = G.tom; t.x = P.x; t.z = P.z + 1.9; t.ang = Math.PI; }); await h.step(0.5);
  await L(() => LEDGER.press('E')); await h.step(0.3);
  const opens = await clear();
  check('Sheila opens Act II in her own words', opens.some((x) => /two cars and a tin/.test(x)) && (await L(() => LEDGER.game.acts.read().fired.includes('opens'))), opens.slice(0, 2).join(' / '));
  await L(() => LEDGER.goOutside()); await h.step(0.5);
  // --- no beat fires on a day alone; three quiet days bring the next one, and the wait stops for it (ER-JOB-04)
  const t0 = (await read()).gameMinute;
  await passTo(t0 + 1440);
  await clear();
  check('one quiet day: no new beat', (await L(() => LEDGER.game.acts.read().fired.length)) === 1 && !(await L(() => LEDGER.game.acts.read().pending)));
  await passTo(t0 + 8 * 1440);
  r = await read();
  const s2 = await L(() => LEDGER.game.acts.read());
  check('quiet days bring the next beat by itself (no dead weeks)', (s2.pending && s2.pending.id === 'rival_first') || s2.fired.includes('rival_first'), JSON.stringify(s2.pending));
  check('the wait stopped for it, days short of what was asked', r.gameMinute < t0 + 5 * 1440, `stopped after ${Math.round((r.gameMinute - t0) / 1440 * 10) / 10} days`);
  // left alone, it reaches him as a message taken at the office
  await L(() => LEDGER.goOutside());
  for (let i = 0; i < 40 && !(await L(() => LEDGER.game.acts.read().fired.includes('rival_first'))); i++) { await h.step(8); await clear(); }
  check('a beat nobody collects reaches him as a message', await L(() => LEDGER.game.acts.read().fired.includes('rival_first')));
  // every beat by script
  for (const id of ['ellis_joins', 'collision', 'squeeze']) {
    await L((id) => { LEDGER.game.acts.fire(id, id === 'ellis_joins' ? 'alison' : id === 'squeeze' ? 'sheila' : 'ron'); }, id);
    await h.step(0.3);
    const said = await clear((w) => (/looking at Tom/.test(w.text) ? 1 : 0));
    check(`beat ${id} plays and is written in the Ledger`, said.length >= 2 && (await L((id) => LEDGER.game.acts.read().fired.includes(id), id)), String(said.length));
  }
  check('the collision left a choice he made', (await L(() => LEDGER.game.acts.read().collision)) === 'stayed');
  // --- the sit-down: called by a person, taken at his own cab, asked twice, three answers
  await L(() => { LEDGER.game.acts.fire('sitdown_called', 'ron'); }); await h.step(0.3);
  const called = await clear();
  const head = await L(() => LEDGER.game.acts.read().called.head);
  check('the Fixer brokers a sit-down with one head', called.some((x) => /Garbutt/.test(x)) && ['widow', 'agar', 'cammack'].includes(head), head);
  await L(() => { const G = LEDGER.G, t = G.tom; LEDGER.goOutside(); t.x = G.car.x + 2.6; t.z = G.car.z; }); await h.step(0.5);
  const pr = await L(() => LEDGER.prompts());
  check('beside his cab the prompt offers the sit-down', pr.some((p) => /Sit down with/.test(p.text)), JSON.stringify(pr) + JSON.stringify(await L(() => { const r = LEDGER.read(), G = LEDGER.G; return [r.paused, r.pausedBecause, r.boxOpen, G.tom.space, G.tom.inCar, G.tom.x, G.tom.z, G.car.x, G.car.z, r.clock, LEDGER.F && LEDGER.F.on]; })));
  await L(() => LEDGER.press('E')); await h.step(0.3);
  let asked = 0;
  const sat = await clear((w) => { if (/Well\?/.test(w.text)) return 1; if (/cannot be unsaid/.test(w.text)) { asked++; return asked === 1 ? 1 : 0; } return 0; });
  const sd = await L(() => LEDGER.game.acts.read().sitDown);
  check('three answers were offered', sat.filter((x) => /^ {2}> /.test(x)).length >= 2 && sat.some((x) => /Well\?/.test(x)));
  check('what cannot be undone asked twice, and a no there took nothing', asked === 2 && sd && sd.answer === 'defy', JSON.stringify(sd) + ' asked ' + asked);
  check('the sit-down opens Act III', (await L(() => LEDGER.game.acts.read().act)) === 3);
  // --- Act III: the letter, then one deciding step each morning
  const d0 = (await read()).dayIndex;
  await passTo((d0 + 1) * 1440 + 8.2 * 60);
  await h.step(3);
  const letter = await clear();
  check('a courteous letter from Customs and Excise opens the week', letter.some((x) => /Customs and Excise/.test(x)) && (await L(() => !!LEDGER.game.acts.read().a3)), letter[0]);
  const grades = [];
  for (let m = 0; m < 6 && (await L(() => !LEDGER.game.endings.read().ended)); m++) {
    const st = await L(() => LEDGER.game.acts.read().a3);
    if (st.grades.length >= 5) break;
    const d = (await read()).dayIndex;
    const day = Math.max(st.startDay, st.lastDay === d ? d + 1 : (await read()).hour >= 13 ? d + 1 : d);
    if (m === 1) {
      // a morning he does not turn up for: it is asked for in writing, never a failure of the game
      await passTo(day * 1440 + 13.2 * 60); await h.step(3); await clear();
      const a = await L(() => LEDGER.game.acts.read().a3);
      check('a morning missed is put in writing by Sheila, and costs a day', a.writings === 1 && a.grades.length === grades.length, JSON.stringify(a));
      continue;
    }
    await passTo(day * 1440 + 9.1 * 60);
    await L(() => LEDGER.goInside("Mickey's Cars")); await h.step(2.5);
    const said = await clear((w) => (/If it is to hand/.test(w.text) ? 0 : /He can still reach/.test(w.text) ? w.choices.length - 1 : /statement/.test(w.text) ? 1 : 0));
    const a = await L(() => LEDGER.game.acts.read().a3);
    if (a.grades.length > grades.length) grades.push(a.grades[a.grades.length - 1]);
    if (m === 0) check('the inspector asks for one set of records and answers in his manner', said.some((x) => /should like to see/.test(x)) && said.some((x) => /Thank you|make a note|both know/.test(x)), said.join(' / ').slice(0, 200));
    await L(() => LEDGER.goOutside());
  }
  check('five mornings, one deciding step each', grades.length === 5, grades.join(','));
  // --- then the books open: an ending as a state, the credits, and the town again
  check('the books open and the close is reached', await until(() => !!LEDGER.game.endings.read().ended, 30));
  await h.step(1); await h.key('Space'); await h.step(1);
  check('the credits come after the close', await until(() => LEDGER.read().boxOpen === 'credits-end', 40));
  const e = await L(() => LEDGER.game.endings.read().ended);
  check('the ending is one of three shown, and Tom\'s reading had predicted its state', ['The Kingdom', 'The Straight Life', 'Burn Both'].includes(e.shown) && e.predicted === e.state, JSON.stringify(e));
  const t1 = Date.now();
  await h.page.click('[data-act="afterend"]'); await h.step(0.5);
  r = await read();
  check('after the credits he walks the town within 10 s (ER-AFTER-01)', r.phase === 'play' && !r.paused && Date.now() - t1 < 10000);
  await h.step(5);
  check('no new main beat after the ending', !(await L(() => LEDGER.game.acts.read().pending)));
  check('no game-over screen anywhere on the way (ER-CORE-04)', !(await L(() => /game over/i.test(document.body.textContent))));
  const f = await faults();
  check('no system fault', f.length === 0, f.slice(0, 3).join(' | '));
  check('no page error', h.errors.length === 0, [...new Set(h.errors)].slice(0, 3).join(' | '));
} catch (e) { check('the test ran to its end', false, String(e.stack || e).slice(0, 700)); }
await h.close();
console.log(ok() ? 'PASS' : 'FAIL');
process.exit(ok() ? 0 : 1);
