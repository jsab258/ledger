// S03 The debt book and Darren's £22 (ONE-SHOT-PROMPT.md). First the save S02 leaves is played to the debt book and
// the Ledger ("book"); then, from the save that leaves, the three ways with Darren, each on its own.
import { run } from './play.mjs';

const words = (s) => s.trim().split(/\s+/).length;

await run('S03', { from: (v) => (v === 'book' ? 'S02' : 'S03 book') }, async (P, t, n, variant) => {
  const go = async (x, z, o = {}) => { const r = await P.walkTo(x, z, Object.assign({ maxSecs: 60 }, o)); if (r < 0) { const m = await P.tom(); t.ok(false, 'he can walk to ' + Math.round(x) + ', ' + Math.round(z), [Math.round(m.x * 10) / 10, Math.round(m.z * 10) / 10, m.space]); } return r; };
  let s;
  await P.cont();

  if (variant === 'book') {
    // ---- 1. Sheila finishes the walk-round: the fare book, the locked door, the flat, the debt book ----
    t.ok((await P.tom()).space === 'mickeys', 'he is back at the office', await P.tom());
    await P.world(() => { const S = window.__S; S.sheila = []; S.eachs.sheila = () => { for (const e of document.querySelectorAll('#subs .s')) { const s = e.innerText.trim(); if (/^SHEILA DUNN[A-Z]/.test(s) && !S.sheila.some((x) => x.line === s)) { const Q = LEDGER.G.people.sheila, r = LEDGER.roomOf('mickeys'); S.sheila.push({ line: s, at: [Math.round((Q.x - r.ox) * 10) / 10, Math.round((Q.z - r.oz) * 10) / 10], moving: !!Q.moving }); } } }; });
    for (let k = 0; k < 70; k++) {
      if ((await P.screen()).book) break;
      const sh = await P.world(() => { const S = LEDGER.G.people.sheila; return [S.x, S.z, S.space]; });
      const me = await P.tom();
      if (sh[2] === 'mickeys' && Math.hypot(me.x - sh[0], me.z - sh[1]) > 2.0) await P.walkTo(sh[0], sh[1], { maxSecs: 1.5, near: 1.7 }); else await P.secs(0.3);
    }
    const told = await P.world(() => window.__S.sheila);
    const want = await P.world(() => LEDGER.game.book.finish);
    t.ok(told.length === 4, 'Sheila finishes with four lines: ' + want.map((w) => w.thing).join(', '), told.map((x) => x.line.slice(0, 50)));
    t.ok(told.length === 4 && told.every((l, i) => Math.hypot(l.at[0] - want[i].at[0], l.at[1] - want[i].at[1]) < 0.7 && !l.moving), 'each said standing at the thing itself', told.map((x) => x.at));
    t.ok(told[0] && /two pounds thirty/i.test(told[0].line) && /fare book/i.test(told[0].line), 'at the fare book she names the fare he drove', told[0]);
    const last = told[3] ? told[3].line : '';
    t.ok(/five names/i.test(last) && /hundred and fifty-six pounds/i.test(last) && /eighteen pounds, Friday/i.test(last), 'she says five names, £156 in all, and the rent of £18 due on Friday', last);
    t.ok(told.every((l) => !/Tom|Nowak/.test(l.line)), 'still without his name', 0);
    s = await P.screen();
    const page = s.book;
    t.ok(/debt book/i.test(page) && ['Darren Milner £22', 'Wayne Harrison £30', 'Lee Drewery £15', 'Julie Kettlewell £9', 'Dennis Iveson £80'].every((x) => page.includes(x)) && /£156 in all/.test(page) && /£18/.test(page) && /Friday/.test(page), 'she shows the debt book as a page: the five names and sums, £156 in all, the rent on Friday', page);
    await P.click('[data-act="close"]'); await P.secs(0.4);
    t.ok(!(await P.screen()).book && !(await P.world(() => LEDGER.G.paused)), 'the book shuts and he has control', await P.screen());
    const choiceAt = await P.played();
    t.ok(choiceAt < 20 * 60, 'the choice over Darren comes well inside 20 minutes of play (about 5:30 on the straight way)', choiceAt);

    // ---- 2. the Ledger: Open, People, the Day book and Money ----
    const frames = await P.world(async () => { const S = window.__S; S.kd('KeyL'); const n = await S.run(30, () => !document.getElementById('ledgerp').classList.contains('hidden') && document.getElementById('lbook').innerText.length > 20); S.ku('KeyL'); return n; });
    t.ok(frames > 0 && frames <= 7, 'the Ledger opens within 120 ms of the key', frames * 16.7);
    await P.tap('KeyL'); await P.frames(15);
    const open = await P.ledger('open');
    const debtLines = open.split('\n').filter((l) => /owes £/.test(l));
    t.ok(new Set(debtLines).size === 5 && debtLines.every((l) => /Find (him|her) (at|in) /.test(l)) && /Darren Milner owes £22/.test(open) && /the rank outside Mickey's/.test(open) && /west end of the quay/.test(open) && /behind Rinaldi's caff/.test(open) && /fish dock/.test(open) && /by the bus stop/.test(open), 'Open lists each debt with its person and a landmark', debtLines);
    t.ok(/Rent, £18/.test(open), 'and the rent', open.slice(0, 300));
    await P.ledgerClose();
    const money = await P.ledger('money');
    t.ok(/£25\.80 in his pocket/.test(money) && /£2\.30 of fares in the fare book/.test(money) && /Rent, £18, Friday/.test(money) && /Darren owes £22/.test(money), 'Money says in words what he has (£23.50 and the fare) and what is owed by Friday', money.slice(0, 500));
    await P.ledgerClose();
    const day = await P.ledger('day book');
    t.ok(/Father Walsh/.test(day) && /debt book/i.test(day), 'the Day book has the fare and the debt book', day.slice(0, 400));
    await P.ledgerClose();
    // any person found in three inputs: L, the People page, the person
    await P.tap('KeyL'); await P.frames(15);
    let inputs = 1;
    for (; inputs < 3 && !/Darren Milner/.test((await P.screen()).ledger); inputs++) { await P.tap('KeyE'); await P.frames(15); }
    s = await P.screen();
    t.ok(/Darren Milner/.test(s.ledger) && inputs <= 3, 'a person is found in the Ledger in three inputs', [inputs, s.ledger.slice(0, 200)]);
    await P.tap('KeyL'); await P.frames(15);
    if ((await P.screen()).ledger) await P.ledgerClose();
    t.ok(await P.save(t.first ? 'S03 book' : null), 'the game saves (the save the three ways with Darren start from)', 0);
    t.note('the debt book page', page.replace(/\s+/g, ' '));
    t.note('Open', debtLines);
    return;
  }

  // ---- 3. out to Darren, who owes £22 and is standing right there ----
  const mat = await P.world(() => { const r = LEDGER.roomOf('mickeys'); return [r.ox + r.mat[0], r.oz + r.mat[1] - 0.3]; });
  await go(mat[0], mat[1], { near: 0.6 });
  await P.use(/Leave/);
  await P.until(() => LEDGER.G.tom.space === 'street', 5);
  const dar = await P.world(() => { const D = LEDGER.G.people.darren; return [D.x, D.z, D.space]; });
  t.ok(dar[2] === 'street' && Math.hypot(dar[0] - 6, dar[1] - 28.5) < 3, 'Darren is on the pavement by the rank', dar);
  await go(dar[0] + 0.2, dar[1] + 1.3, { near: 0.5 });
  await P.face(dar[0], dar[1]); await P.secs(0.4);
  await P.headsReset();
  // people within sight: who moves nearer and back again in the next seconds (read off their bodies)
  const watchCrowd = () => P.world(() => { const S = window.__S, G = LEDGER.G; S.near = {}; S.eachs.near = () => { if (S.frameNo % 12) return; for (const Q of G.named.concat(G.crowd)) { if (Q.gone || Q.space !== 'street' || Q.id === 'darren') continue; const d = Math.hypot(Q.x - G.tom.x, Q.z - G.tom.z); if (d < 16) (S.near[Q.id] = S.near[Q.id] || []).push(Math.round(d * 10) / 10); } }; });
  const gathered = () => P.world(() => Object.entries(window.__S.near).filter(([, a]) => { const i = a.indexOf(Math.min(...a)); return a.length > 8 && a[0] - a[i] > 0.8 && a[a.length - 1] - a[i] > 0.6; }).map(([id, a]) => [id, a[0], Math.min(...a), a[a.length - 1]]));

  if (variant === 'fronts') {
    await watchCrowd();
    await P.tap('KeyM'); await P.frames(15);
    s = await P.screen();
    t.ok(s.dialog && ['nod', 'Good day', 'hard look', 'Oi', 'shove'].every((w) => s.dialog.opts.some((o) => o.includes(w))), 'M offers the street manners: a nod, a greeting, a hard look, a call and a shove', s.dialog);
    const t0 = await P.played();
    await P.pick(/hard look/);
    const ans = await P.until(() => [...document.querySelectorAll('#subs .s')].some((e) => /DARREN/i.test(e.innerText) && /twenty-two/.test(e.innerText)), 3);
    t.ok(ans >= 0 && ans <= 1, 'the hard look is answered within a second, in his voice', ans);
    await P.secs(1.5);
    await P.tap('KeyM'); await P.frames(15);
    await P.pick(/shove/);
    const paid = await P.until(() => [...document.querySelectorAll('#subs .s')].some((e) => /DARREN/i.test(e.innerText) && /Ten pounds/.test(e.innerText)), 3);
    t.ok(paid >= 0, 'shoved, Darren pays what his purse holds: ten pounds', (await P.screen()).subs);
    await P.secs(9);
    const heads = await P.heads();
    t.ok(heads.filter((id) => id !== 'darren').length >= 1, 'somebody sees it: at least one person within sight turns', heads);
    const g = await gathered();
    t.ok(g.length >= 1, 'after the shove one of them gathers and drifts back', [g, await P.world(() => LEDGER.game.book.x().gathered)]);
    const open = await P.ledger('open');
    t.ok(/Darren Milner owes £12/.test(open), 'the rest stays on the book: £12', open.split('\n').filter((l) => /Darren/.test(l)));
    const struck = await P.world(() => [...document.querySelectorAll('#lbook s')].map((e) => e.innerText));
    t.ok(struck.some((x) => /Darren Milner owes £22/.test(x)), 'the old sum is struck through, not removed', struck);
    await P.ledgerClose();
    const money = await P.ledger('money');
    t.ok(/The tin has about £10 in it/.test(money) && /Darren still owes £12/.test(money), 'Money says it in words: the tin, and Darren still owes £12', money.slice(0, 400));
    await P.ledgerClose();
    const day = await P.ledger('day book');
    const line = day.split('\n').find((l) => /Fronted up Darren Milner/.test(l)) || '';
    t.ok(words(line) >= 14 && words(line) <= 34, 'the Day book gets a line of about 22 words', [words(line), line]);
    await P.ledgerClose();
    t.note('fronted', [await P.world(() => [LEDGER.G.debts.darren.owed, LEDGER.G.money.dirty]), line]);
  }

  if (variant === 'takes' || variant === 'strikes') {
    await P.use(/Talk to Darren/);
    await P.secs(0.8);
    s = await P.screen();
    t.ok(!!s.talk, 'he talks to Darren', s.prompts);
    // Darren puts it himself: he has not got it, but he could pay in what he hears
    let raised = /pay it in what I hear/i.test(s.talk.log.join(' '));
    for (let k = 0; k < 2 && !raised; k++) { await P.talkSay(/Hello|Evening|Darren|minute/i); raised = /pay it in what I hear/i.test((await P.screen()).talk.log.join(' ')); }
    s = await P.screen();
    if (!s.talk.lines.length) { await P.tap('Tab'); await P.frames(12); s = await P.screen(); }
    t.ok(raised, 'Darren offers to pay in what he hears', s.talk.log);
    t.ok(s.talk.lines.some((l) => /what you hear/i.test(l)) && s.talk.lines.some((l) => /striking it out|dies with Mickey/.test(l)) && s.talk.lines.some((l) => /come for|want it paid/.test(l)) && s.talk.leave, 'his ways with it are offered as lines: take what he hears, come for the money, strike it out; and Leave', s.talk.lines);
  }

  if (variant === 'takes') {
    await P.talkSay(/what you hear/i);
    s = await P.screen();
    if (!s.talk.lines.length) { await P.tap('Tab'); await P.frames(12); s = await P.screen(); }
    t.ok(/Yeah or no/.test(s.talk.log.slice(-1)[0]) && s.talk.lines.some((l) => /^Yes/.test(l)) && s.talk.lines.some((l) => /^No/.test(l)) && s.talk.lines.length >= 3 && s.talk.leave, "the decision is the game's own lines: a yes, a no and a line that keeps talking, with Leave offered", s.talk.lines);
    await P.talkSay(/What do you hear|worth twenty-two/);
    s = await P.screen();
    t.ok(/Yeah or no/.test(s.talk.log.slice(-1)[0]) && (await P.world(() => LEDGER.G.debts.darren.st)) === 'open', 'the line that keeps talking decides nothing', s.talk.log.slice(-2));
    await P.talkType('well, maybe, I suppose so');
    s = await P.screen();
    t.ok((await P.world(() => LEDGER.G.debts.darren.st)) === 'open', 'anything short of a plain yes is not taken', s.talk.log.slice(-2));
    await P.talkSay(/^Yes/);
    s = await P.screen();
    t.ok(/Iveson/.test(s.talk.log.join(' ')) && /hut in his yard/.test(s.talk.log.join(' ')), 'on a plain yes he pays in what he hears: Iveson, the tin in the hut in his yard', s.talk.log.slice(-2));
    await P.click('#tbye'); await P.secs(0.6);
    const day = await P.ledger('day book');
    const tip = day.split('\n').find((l) => /Darren, for his £22/.test(l)) || '';
    t.ok(/yard hut/.test(tip) && /leaves at six/.test(tip), 'the tip is a line in the Ledger', tip);
    t.ok(words(tip) >= 14 && words(tip) <= 30, 'of about 22 words', words(tip));
    await P.ledgerClose();
    const open = await P.ledger('open');
    t.ok(!open.split('\n').some((l) => /Darren Milner owes/.test(l) && !/Closed|closed/.test(l)) || /Darren/.test(open), 'the debt is no longer open', open.split('\n').filter((l) => /Darren/.test(l)));
    await P.ledgerClose();
    const money = await P.ledger('money');
    t.ok(!/Darren (still )?owes/.test(money) && /Wayne owes £30/.test(money), 'Money no longer counts Darren among what is owed', money.slice(0, 400));
    await P.ledgerClose();
    t.note('taken', [await P.world(() => [LEDGER.G.debts.darren.st, LEDGER.G.money.dirty]), tip]);
  }

  if (variant === 'strikes') {
    // his own line: striking it out. It asks twice.
    const said = await P.talkSay(/striking it out|dies with Mickey/);
    s = await P.screen();
    t.ok(said && /Struck out\? For good\?/.test(s.talk.log.slice(-1)[0]), 'striking the debt out is asked about', s.talk.log.slice(-2));
    await P.talkSay(/^Yes/);
    s = await P.screen();
    t.ok(/cannot be put back/.test(s.talk.log.slice(-1)[0]) && /sure\?/.test(s.talk.log.slice(-1)[0]) && (await P.world(() => LEDGER.G.debts.darren.st)) === 'open', 'and asked a second time before anything is done', s.talk.log.slice(-2));
    await P.talkSay(/^Yes/);
    s = await P.screen();
    t.ok((await P.world(() => LEDGER.G.debts.darren.st)) === 'forgiven' && /Ta|forget that/.test(s.talk.log.slice(-1)[0]), 'on the second yes it is struck out, and Darren says so', s.talk.log.slice(-2));
    await P.click('#tbye'); await P.secs(0.6);
    const open = await P.ledger('open');
    const struck = await P.world(() => [...document.querySelectorAll('#lbook s')].map((e) => e.innerText));
    t.ok(struck.some((x) => /Darren Milner owes £22/.test(x)), 'the Ledger shows it struck through, never removed', [struck, open.split('\n').filter((l) => /Darren/.test(l))]);
    await P.ledgerClose();
    const day = await P.ledger('day book');
    const line = day.split('\n').find((l) => /Struck Darren Milner's £22 out/.test(l)) || '';
    t.ok(words(line) >= 14 && words(line) <= 34, 'the Day book gets a line of about 22 words', [words(line), line]);
    await P.ledgerClose();
    // the book itself, at Sheila's desk: struck through in Mickey's own pages
    await go(6.2, 36, { near: 0.6 }); await P.face(7.2, 36); await P.secs(0.3);
    await P.use(/Go into Mickey/); await P.until(() => LEDGER.G.tom.space === 'mickeys', 5);
    const desk = await P.world(() => { const r = LEDGER.roomOf('mickeys'); return [r.ox + 3.4, r.oz - 0.3]; });
    await go(desk[0], desk[1], { near: 0.5 }); await P.secs(0.3);
    await P.tap('KeyG'); await P.frames(20);
    if ((await P.screen()).dialog) await P.pick(/debt book/);
    const inBook = await P.world(() => [...document.querySelectorAll('#book s')].map((e) => e.innerText));
    t.ok(inBook.some((x) => /Darren Milner £22/.test(x)) && /struck out/.test((await P.screen()).book), "in Mickey's debt book the line is struck through and still there", [inBook, (await P.screen()).book.slice(0, 300)]);
    await P.click('[data-act="close"]'); await P.secs(0.3);
    t.note('struck', [await P.world(() => LEDGER.G.debts.darren.st), line]);
  }

  // whichever way: Tom comes to believe something new, and the low line says so
  const beliefs = await P.beliefs();
  t.ok(beliefs.length >= 1, 'the low belief line shows when Tom comes to believe something new', beliefs);
  t.ok(await P.save(t.first ? 'S03 ' + variant : null), 'the game saves', 0);
}, ['book', 'fronts', 'takes', 'strikes']);
