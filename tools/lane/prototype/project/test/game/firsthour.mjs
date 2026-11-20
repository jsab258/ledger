// The first hour as DESIGN 15 stages it (part 7.1; ER-FIRST-01 to 03): the ferry shot of at most 20 s that any key
// skips, control at the landing with the suitcase, a to-do that moves with every beat, a hint only when he stands
// still, Sheila's walk-round ending at the radio with a first fare, the debt book at the things themselves, Darren's
// debt standing there, and Ron's ask after dark. Timings are the game's own clock and the machine's.
import { launch, sleep } from '../harness.mjs';
import { drive } from './spine_drive.mjs';
const h = await launch({ port: 8864, quality: 'low' });
const { L, check, clear, read, until, faults, ok } = drive(h);
try {
  // --- the shot and first control (ER-FIRST-01, 02)
  await sleep(800);
  const t0 = Date.now();
  await h.page.click('[data-act="new"]');
  await sleep(2500);
  const shot = await L(() => document.body.innerText);
  check('the ferry comes in under a grey sky, on Monday 15 October 1990', /ferry comes in under a grey sky/.test(shot) && /15 October 1990/.test(shot));
  check('the shot is at most 20 s by its own number', (await L(() => LEDGER.rules.game.acts.ferryShotAtMostRealSeconds)) <= 20);
  await h.key('Space');
  let ctl = false;
  for (let i = 0; i < 200 && !ctl; i++) { await sleep(100); ctl = await L(() => { const r = LEDGER.read(); return r.phase === 'play' && !r.paused; }); }
  const secs = (Date.now() - t0) / 1000;
  check('any key skips it, and control comes within 20 s of New (aim), 90 s at worst (ER-FIRST-01)', ctl && secs < 20, secs.toFixed(1) + ' s');
  await L(() => { window.LEDGER_MANUAL = true; LEDGER.step(0.5); });
  let r = await read();
  check('he stands on the ferry landing with his suitcase', /ferry/.test(r.tom.zone || '') || r.tom.zMetres > 50, JSON.stringify([r.tom.zone, r.tom.xMetres, r.tom.zMetres]));
  check('the suitcase is in his hand', await L(() => LEDGER.G.tom.carry === 'suitcase'));
  check('the to-do names the way by landmark, no marker', /quay/i.test(r.toDo) && /blue sign/.test(r.toDo), r.toDo);
  // --- a hint only on hesitation, once (ER-FIRST-03)
  check('no hint while he has not hesitated', !(await L(() => LEDGER.G.story.flags.hintWalk)));
  await L(() => { LEDGER.G.tom.still = 4.5; }); await h.step(1.5);
  check('standing still four seconds brings the walking hint', !!(await L(() => LEDGER.G.story.flags.hintWalk)));
  const subs1 = await L(() => document.getElementById('subs').textContent);
  await L(() => { LEDGER.G.tom.still = 9; }); await h.step(1.5);
  check('the hint is given once', (await L(() => document.getElementById('subs').textContent.split('W, A, S, D').length - 1)) <= 1, subs1);
  // --- up the quay to Quay Street: the to-do moves with every beat
  await L(() => LEDGER.goTo("Mickey's Cars (street door)")); await h.step(1.2); await clear();
  r = await read();
  check('on Quay Street the to-do moves on to the door', /go in/.test(r.toDo), r.toDo);
  await L(() => LEDGER.goInside("Mickey's Cars")); await h.step(1.2); await clear();
  r = await read();
  check("inside Mickey's it moves on to Sheila", /Sheila Dunn/.test(r.toDo), r.toDo);
  // --- Sheila's walk-round: six lines of hers, ending at the radio with a fare and no car
  await L(() => { const G = LEDGER.G, P = G.people.sheila, t = G.tom; t.x = P.x; t.z = P.z + 1.9; t.ang = Math.PI; }); await h.step(0.5);
  await L(() => LEDGER.press('E')); await h.step(0.3);
  const tour = await clear();
  const hers = tour.filter((x) => /^Sheila|bookkeeper/i.test(x)).length;
  check('the walk-round is short: six lines of hers and Pauline at the radio', tour.length <= 8 && tour.some((x) => /a fare and no car/.test(x)), tour.length + ' lines, hers ' + hers);
  const words = tour.join(' ').split(/\s+/).length;
  check('the scene reads in under 60 s (ER-FIRST-02)', words / 3 < 60, words + ' words');
  r = await read();
  const fare = await L(() => LEDGER.fare.read());
  check('the first verb is offered at once: car two, a fare to the chapel house', (await L(() => LEDGER.G.car.keys)) && fare && /chapel/i.test(fare.toPlace || ''), JSON.stringify(fare));
  check('the to-do says where the car is and where the fare goes', /car two/i.test(r.toDo) && /chapel/i.test(r.toDo), r.toDo);
  check('nothing needs the car: Sheila will go on if he comes back', /go back to Sheila/.test(r.toDo));
  // --- drive it
  await L(() => LEDGER.goOutside()); await h.step(0.5); await clear();
  await L(() => LEDGER.cab.getIn()); await h.step(0.3);
  await L(() => LEDGER.fare.accept()); await h.step(0.5);
  await L(() => LEDGER.fare.pickUp()); await h.step(1);
  await L(() => { LEDGER.fare.dropOff(); }); await h.step(2); await clear();
  check('the first fare goes in the book', (await L(() => LEDGER.G.money.fareCount)) === 1);
  await L(() => LEDGER.cab.getOut()); await h.step(2);
  r = await read();
  check('the to-do moves on: back to Sheila', /Sheila has the rest/.test(r.toDo), r.toDo);
  // --- back at the office: the things themselves, the debt book, five names, 156 pounds, rent on Friday
  await L(() => LEDGER.goInside("Mickey's Cars")); await h.step(1); await clear();
  await L(() => { const G = LEDGER.G, P = G.people.sheila, t = G.tom; t.x = P.x; t.z = P.z + 1.9; t.ang = Math.PI; }); await h.step(2.5);
  await clear(); // Pauline, at the radio beside them, says her piece first
  await L(() => LEDGER.press('E')); await h.step(0.3);
  const end = await clear();
  check("Sheila finishes at the things themselves: the fare book, Mickey's debt book, the door, the flat", end.some((x) => /fare book/.test(x)) && end.some((x) => /debt book/.test(x) && /hundred and fifty-six/.test(x)) && end.some((x) => /rent's Friday/.test(x)), end.length + ' lines');
  const book = await L(() => LEDGER.ledger.book().map((e) => e.what));
  check('the Ledger holds the five names and the sum', book.some((w) => /£156\.00/.test(w) && /Iveson/.test(w) && /Kettlewell/.test(w)));
  r = await read();
  check("the to-do moves on to Darren's twenty-two pounds, standing there", /Darren Milner/.test(r.toDo) && /£22/.test(r.toDo), r.toDo);
  // --- Darren: Mickey's debt book, never a bookmaker
  await L(() => LEDGER.goOutside()); await h.step(0.5);
  await L(() => { LEDGER.G.story.flags.metDarren = 0; const G = LEDGER.G, P = G.people.darren, t = G.tom; P.space = 'street'; P.gone = false; P.x = t.x + 1.5; P.z = t.z; }); await h.step(2.5);
  const dar = await clear();
  check("Darren's debt reads as money Mickey lent, not a bet", dar.some((x) => /Mickey's debt book/.test(x) && /lent/.test(x)) && !dar.some((x) => /owe the book/.test(x)), dar.join(' / ').slice(0, 160));
  check('his debt is open to be fronted up', (await L(() => LEDGER.G.debts.darren.st)) === 'open');
  // --- after dark Ron has the outfit's first ask
  for (let i = 0; i < 400 && (await read()).hour < 17.6; i++) { await h.step(4); await clear(); }
  await h.step(3); await clear();
  check('after dark Ron has a word: the first ask', (await L(() => LEDGER.G.people.ron.mark)) === '!' || !!(await L(() => LEDGER.G.story.flags.ask1)), JSON.stringify(await L(() => [LEDGER.G.people.ron.mark, LEDGER.G.story.flags.ask1, LEDGER.read().clock])));
  const played = (await read()).realSecondsPlayed;
  check('all of it inside the first minutes of play', played < 20 * 60, Math.round(played) + ' s played');
  const b = await L(() => LEDGER.game.ledgerx.budget());
  check('something new at least every three minutes so far (ER-CORE-05)', b.longestNothingNewRealSeconds <= 180, JSON.stringify(b));
  const f = await faults();
  check('no system fault', f.length === 0, f.slice(0, 3).join(' | '));
  check('no page error', h.errors.length === 0, [...new Set(h.errors)].slice(0, 3).join(' | '));
} catch (e) { check('the test ran to its end', false, String(e.stack || e).slice(0, 700)); }
await h.close();
console.log(ok() ? 'PASS' : 'FAIL');
process.exit(ok() ? 0 : 1);
