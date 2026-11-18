// Two rules of the Ledger, pass or fail.
// 1. "Nobody saw" never disappears. It is written only once an act has gone two game minutes with no watcher
//    Tom knows of; if a watcher turns up after that it is struck through with the reason; if one turns up
//    before, it is never written. No entry, once in the book, is ever taken out.
// 2. In People, "/" and then a letter jumps to that letter, E, L and Q among them (keys of their own otherwise).
import { launch } from './harness.mjs';
import { driver } from './week_bot.mjs';

const h = await launch({ port: 8898, seed: +(process.env.SEED || 1990) });
const { L, clear } = driver(h, { log: () => {} });
let bad = 0;
const check = (name, ok, extra = '') => { if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${extra ? ' | ' + String(extra).slice(0, 300) : ''}`); };
const book = () => L(() => LEDGER.ledger.book().map((e) => ({ id: e.id, kind: e.kind, ev: e.ev, what: e.what, struck: e.struck || null })));
const WAIT = await L(() => LEDGER.rules.ledger.unseenHeldAfterGameMinutes);
const gameMinutes = (n) => h.step((n * 45) / 60); // 45 real seconds to a game hour
try {
  await h.newWeek(); await clear();
  await L(() => { const f = LEDGER.G.story.flags; f.tour = 1; f.metRon = f.metDarren = 1; LEDGER.G.tom.hasCoat = true; });
  // Tuesday at four in the afternoon the chapel is empty: he sits in a pew, and nobody is there to see it
  await L((t) => LEDGER.passTime(t), 1440 + 16 * 60); await clear();
  const pew = await L(() => Object.keys(LEDGER.insidePlaces).find((k) => /pew|chapel/i.test(k)));
  const before = await book();
  await L((p) => LEDGER.goInside(p), pew); await h.step(0.4);
  const ev1 = await L(() => LEDGER.ledger.act('chapel')); // the act itself, without the sitting that follows it in play
  const act = (await book()).find((e) => e.kind === 'did' && e.ev === ev1) || null;
  check('an act of his own is written down', !!act, act ? act.what : 'no act came');
  const watchers = await L((ev) => LEDGER.ledger.book().filter((e) => e.kind === 'belief' && e.ev === ev).length, act.ev);
  const now1 = await book();
  check('"Nobody saw" is not written at once', !now1.some((e) => e.kind === 'unseen' && e.ev === act.ev) && (await L(() => LEDGER.ledger.waiting().length)) > 0, `watchers known: ${watchers}`);
  await gameMinutes(WAIT + 0.5);
  const now2 = await book(), unseen = now2.find((e) => e.kind === 'unseen' && e.ev === act.ev);
  check(`after ${WAIT} game minutes with no watcher it is written`, watchers === 0 ? !!unseen && !unseen.struck : !unseen, unseen ? unseen.what : 'not written');
  await L((ev) => LEDGER.ledger.learn(ev, 'ron'), act.ev);
  const now3 = await book(), still = now3.find((e) => unseen && e.id === unseen.id);
  check('a watcher turns up later: the line stays, struck through with the reason', !!still && !!still.struck && /ron|kirby|man|knows/i.test(still.struck.why || ''), still ? JSON.stringify(still.struck) : 'the line is gone');
  // a second act, and this time the watcher is known before the wait is over
  await L((t) => LEDGER.passTime(t), 2 * 1440 + 16 * 60); await clear(); // Wednesday, the same pew
  await L((p) => LEDGER.goInside(p), pew); await h.step(0.4);
  const ev2 = await L(() => { const id = LEDGER.ledger.act('chapel'); LEDGER.ledger.learn(id, 'darren'); return id; });
  const act2 = (await book()).find((e) => e.kind === 'did' && e.ev === ev2) || null;
  if (act2) {
    await gameMinutes(WAIT + 1);
    const now4 = await book();
    check('a watcher known before the wait is over: "Nobody saw" is never written', !now4.some((e) => e.kind === 'unseen' && e.ev === act2.ev), act2.what);
  } else check('a second act came to test the early watcher', false);
  const end = await book();
  const gone = now1.concat(now2, now3).filter((e) => !end.some((x) => x.id === e.id));
  check('no entry that was ever in the book has been taken out', gone.length === 0, gone.map((e) => e.what).join(' | '));

  // the People index
  await L(() => { const G = LEDGER.G; for (const id of ['lee', 'ellis', 'sheila', 'ron']) { G.ledger.met[id] = 1; LEDGER.ledger.learn(G.events[0].id, id); } if (G.ledger.names) for (const id of ['lee', 'ellis', 'sheila', 'ron']) G.ledger.names[id] = 1; });
  const open = await L(() => LEDGER.ledger.open('people', 'keyboard'));
  const names = await L(() => LEDGER.ledger.pages().map((p) => p.heading));
  let r = await L(() => { LEDGER.ledger.key('Slash', 'keyboard'); return LEDGER.ledger.read(); });
  check('"/" asks for a letter', r.open && /letter/i.test(r.said || ''), r.said);
  r = await L(() => { LEDGER.ledger.key('KeyL', 'keyboard'); return LEDGER.ledger.read(); });
  check('"/" then L jumps to the first page under L and the book stays open', r.open && r.part === 'people' && r.person === 'darren', `page ${r.person} (the lad on the pavement, before Lee) | pages: ${names.join(', ')}`);
  r = await L(() => { LEDGER.ledger.key('Slash', 'keyboard'); LEDGER.ledger.key('KeyS', 'keyboard'); return LEDGER.ledger.read(); });
  check('"/" then S jumps to Sheila', r.open && r.person === 'sheila', `page ${r.person}`);
  r = await L(() => { LEDGER.ledger.key('Slash', 'keyboard'); LEDGER.ledger.key('KeyE', 'keyboard'); return LEDGER.ledger.read(); });
  check('"/" then E looks under E and does not change part', r.open && r.part === 'people' && /under E/.test(r.said || ''), `${r.part} | ${r.said}`);
  r = await L(() => { LEDGER.ledger.key('Slash', 'keyboard'); LEDGER.ledger.key('KeyQ', 'keyboard'); return LEDGER.ledger.read(); });
  check('"/" then Q looks under Q and does not change part', r.open && r.part === 'people' && /under Q/.test(r.said || ''), `${r.part} | ${r.said}`);
  r = await L(() => { LEDGER.ledger.key('Slash', 'keyboard'); LEDGER.ledger.key('Escape', 'keyboard'); return LEDGER.ledger.read(); });
  check('Esc lets the jump go without closing the book', r.open && !r.said);
  r = await L(() => { LEDGER.ledger.key('KeyE', 'keyboard'); return LEDGER.ledger.read(); });
  check('E by itself still changes part', r.open && r.part !== 'people', r.part);
  await L(() => LEDGER.ui.hooks.ledgerKey && 0);
  await h.key('KeyL'); await h.step(0.2);
  check('L by itself still closes the book', !(await L(() => LEDGER.ledger.read().open)) || open.open === false);
} catch (e) { bad++; console.log('TEST FAIL', String(e.stack || e).slice(0, 700)); }
if (h.errors.length) { bad++; console.log(' errors', [...new Set(h.errors)].slice(0, 4).join('\n  ')); }
await h.close();
console.log(bad ? 'FAIL' : 'PASS');
process.exit(bad ? 1 : 0);
