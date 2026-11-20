// S05 The carry past the constable (ONE-SHOT-PROMPT.md). From the save S04 leaves on yes (Monday night, the envelope
// under the coat), four ways on their own: the lit quay, stood and searched; the yard and the dark side of the quay,
// walking slowly; the cab; and the lit quay again, running when the constable calls.
import { run } from './play.mjs';

await run('S05', { from: 'S04 yes' }, async (P, t, n, variant) => {
  const go = async (x, z, o = {}) => { const r = await P.walkTo(x, z, Object.assign({ maxSecs: 90 }, o)); if (r < 0 && !o.until) { const m = await P.tom(); t.ok(false, 'he can walk to ' + Math.round(x) + ', ' + Math.round(z), [Math.round(m.x * 10) / 10, Math.round(m.z * 10) / 10, m.space]); } return r; };
  const local = (room, lx, lz) => P.world(({ room, lx, lz }) => { const r = LEDGER.roomOf(room); return [r.ox + lx, r.oz + lz]; }, { room, lx, lz });
  const called = () => !!document.querySelector('#dialog:not(.hidden)') || [...document.querySelectorAll('#subs .s')].some((e) => /^THE CONSTABLE/.test(e.innerText));
  const pc = () => P.world(() => { const Q = LEDGER.G.people.pc; return { x: Q.x, z: Q.z, gone: !!Q.gone, d: Math.hypot(Q.x - LEDGER.G.tom.x, Q.z - LEDGER.G.tom.z) }; });
  const man = () => P.world(() => LEDGER.game.carry.at());
  const callsSoFar = async () => (await P.subsLog()).filter((x) => /^THE CONSTABLE/.test(x.s));
  let s;
  await P.cont();
  const start = await P.world(() => ({ hour: (LEDGER.G.t % 1440) / 60, coat: LEDGER.G.tom.coat, pockets: LEDGER.game.x().crime.pockets.map((p) => p.id), open: LEDGER.game.carry.landingOpen() }));
  t.ok(start.coat && start.pockets.join() === 'envelope' && start.open, 'Monday night: the coat on, the envelope under it, the landing open', start);
  const T0 = await P.played();

  // ----- the ways out of the office -----
  const outFront = async () => { const m = await local('mickeys', -4.2, 3.2); await go(m[0], m[1], { near: 0.6 }); await P.use(/Leave/); await P.until(() => LEDGER.G.tom.space === 'street', 5); };
  const outYard = async () => { const m = await local('mickeys', 6.3, 1.5); await go(m[0], m[1], { near: 0.7 }); await P.use(/yard/); await P.until(() => LEDGER.G.tom.space === 'street', 5); };
  // home by the yard, up the stair, to bed; the night is skipped and the game saves
  const homeAndSleep = async (name) => {
    await go(25, 42.5); await go(22.4, 36.6, { near: 0.8 }); await P.face(20.9, 36); await P.secs(0.3);
    s = await P.screen();
    t.ok(s.prompts.some((p) => /Back door of Mickey/.test(p)), 'he comes home by the yard: the back door has its prompt', s.prompts);
    await P.use(/Back door/); await P.until(() => LEDGER.G.tom.space === 'mickeys', 5);
    const st = await P.world(() => { const r = LEDGER.roomOf('mickeys'), q = LEDGER.roomOf('flat').stair; return [r.ox + q[0] - 0.5, r.oz + q[1] - 0.4]; });
    await go(st[0], st[1], { near: 0.5 }); await P.secs(0.3);
    await P.use(/stair/); await P.until(() => LEDGER.G.tom.space === 'flat', 5);
    const bed = await local('flat', 2.6, -1.2);
    await go(bed[0], bed[1], { near: 0.6 }); await P.secs(0.3);
    s = await P.screen();
    t.ok(s.prompts.some((p) => /bed/i.test(p)), 'the bed in the flat has its prompt', s.prompts);
    const before = await P.clock();
    await P.use(/bed/);
    await P.pick(/Sleep till morning/);
    const woke = await P.until(() => !LEDGER.G.paused && (LEDGER.G.t % 1440) / 60 >= 6.9 && (LEDGER.G.t % 1440) / 60 < 8 && !document.getElementById('fade').classList.contains('on'), 30);
    const after = await P.clock();
    t.ok(woke >= 0 && Math.floor(after / 1440) === 1 && after - before > 180, 'sleeping skips the night: it is Tuesday morning', [before, after, woke]);
    await P.secs(0.6);
    t.ok((await P.subsLog()).some((x) => /^Saved\./.test(x.s)), 'the game saves, and a save note shows', (await P.subsLog()).slice(-3));
    t.ok(await P.world(() => { try { return JSON.parse(localStorage.getItem('ledger.save.v4')).t >= 1440 + 6.9 * 60; } catch (e) { return false; } }), 'the save holds the morning', 0);
    if (t.first) await P.keep(name);
  };
  // the hand-over at the landing
  const handOver = async (label) => {
    const at = await man();
    const r = await go(at[0] + 1.2, at[1] - 0.6, { near: 0.9, slow: label === 'dark' });
    await P.face(at[0], at[1]);
    const said = await P.until(() => [...document.querySelectorAll('#subs .s')].some((e) => /Mickey's\?/.test(e.innerText)), 4);
    t.ok(said >= 0, 'at the landing a man in the dark says "Mickey\'s?"', (await P.screen()).subs);
    s = await P.screen();
    t.ok(s.prompts.some((p) => /Hand the envelope/.test(p)), 'the hand-over has its prompt', s.prompts);
    await P.use(/Hand the envelope/);
    await P.secs(0.8);
    const lines = (await P.subsLog()).map((x) => x.s);
    t.ok(lines.some((x) => /fifteen|15 pounds/.test(x) && /that's yours/.test(x)) && (await P.world(() => LEDGER.game.x().crime.pockets.length)) === 0, 'the hand-over plays and his cut comes back', lines.slice(-2));
    const money = await P.ledger('money');
    t.ok(/The tin has about £15 in it/.test(money), 'the cut is in the Money page in words, under the tin', money.split('\n').slice(8, 10));
    await P.ledgerClose();
    const day = await P.ledger('day book');
    t.ok(/Handed the envelope to the man at the ferry landing/.test(day) && /His cut of the first envelope: £15/.test(day), 'the hand-over and the cut each have their Ledger line', day.split('\n').filter((l) => /envelope/i.test(l)).slice(0, 3));
    await P.ledgerClose();
  };
  // walk the lit quay westward until the constable calls out (he is on his beat between Quay Street and the landing)
  const meetConstable = async () => {
    await outFront();
    await P.world(() => { const S = window.__S; S.pcSeen = null; S.eachs.pc = () => { if (S.pcSeen) return; const Q = LEDGER.G.people.pc, t = LEDGER.G.tom; if (!Q.gone && Q.space === 'street' && Math.hypot(Q.x - t.x, Q.z - t.z) < 35 && LEDGER.map.clear(t.x, t.z, Q.x, Q.z) && LEDGER.G.env.lightAt(Q.x, Q.z, 'street') > 0.3) S.pcSeen = LEDGER.G.played; }; });
    let got = -1;
    for (const [x, z] of [[6.4, 42.8], [-20, 43.2], [-44, 43.2], [-8, 43.2], [-44, 43.2], [6.4, 42.8]]) {
      got = await P.walkTo(x, z, { maxSecs: 70, until: called });
      if (await P.world(called)) break;
    }
    await P.until(() => !!document.querySelector('#dialog:not(.hidden)'), 4);
    const at = await P.played();
    const heard = await P.world(() => ({ steps: LEDGER.mix.filter((m) => m.n === 'steps' && m.who === 'the constable').map((m) => m.at), seen: window.__S.pcSeen, shout: LEDGER.mix.filter((m) => m.n === 'shout').map((m) => m.at).pop() }));
    const firstSign = Math.min(heard.steps.length ? heard.steps[0] : 1e9, heard.seen || 1e9);
    const calls = await callsSoFar();
    t.ok(calls.length >= 1 && !!(await P.screen()).dialog, 'the constable, on his beat on the quay, calls out', [calls, await pc()]);
    t.ok(calls.length && calls[calls.length - 1].at - firstSign >= 3, 'he is heard (his boots) or seen at least 3 real seconds before he challenges', [firstSign, calls.map((c) => c.at), heard.steps.slice(0, 3)]);
    t.ok(heard.shout && calls.length && at - calls[calls.length - 1].at >= 1, 'he calls out before he acts', [heard.shout, calls.map((c) => c.at), at]);
    const d = await P.choice();
    t.ok(d && ['Stand', 'Run', 'word'].every((w) => d.opts.some((o) => o.includes(w))), 'the challenge has its three answers: stand, run, a word', d);
    return at;
  };

  if (variant === 'quay') {
    const at = await meetConstable();
    await P.pick(/Stand and be searched/);
    const kept = await P.readOn();
    t.ok(/keep the envelope/.test(kept.join(' ')), 'stood and searched, the constable finds what is under the coat and keeps the envelope', kept);
    await P.secs(1);
    const back = await P.until(() => !LEDGER.G.paused && !LEDGER.ui.modal, 20);
    t.ok(back >= 0 && (await P.played()) - at < 120, 'control returns within 2 real minutes', (await P.played()) - at);
    t.ok((await P.world(() => [LEDGER.game.x().crime.pockets.length, LEDGER.G.tom.coat])).join() === '0,true', 'exactly the envelope is gone; the coat is his still', await P.world(() => LEDGER.game.x().crime.pockets));
    const day = await P.ledger('day book');
    t.ok(/Searched by the constable/.test(day) && /The constable has the envelope\. The landing is missed/.test(day), 'the search and the failed ask each have their Ledger line; the ask goes on as a state', day.split('\n').filter((l) => /constable/i.test(l)).slice(0, 3));
    await P.ledgerClose();
    const open = await P.ledger('open');
    t.ok(/Taken by the constable/.test(open), 'Open shows what became of the job', open.split('\n').filter((l) => /envelope|constable/i.test(l)).slice(0, 3));
    await P.ledgerClose();
    const at2 = await man();
    await go(at2[0] + 1.2, at2[1] - 0.6, { near: 1.2 });
    await P.secs(1.5);
    s = await P.screen();
    t.ok(!s.prompts.some((p) => /Hand the envelope/.test(p)) && !s.subs.some((x) => /Mickey's\?/.test(x)), 'at the landing there is nothing to hand over: it is missed', [s.prompts, s.subs]);
    await homeAndSleep('S05 home quay');
    t.note('quay', await P.world(() => [LEDGER.game.carry.x().envelope, LEDGER.G.money.dirty]));
  }

  if (variant === 'cab') {
    await outFront();
    const c0 = await P.car();
    await go(c0.x + 1.5, c0.z - 0.8, { near: 0.5 }); await P.secs(0.3);
    await P.use(/car two/); await P.until(() => LEDGER.G.tom.inCar, 4);
    const at = await man();
    const d0 = await P.played();
    const r = await P.drive([[3.6, 42.5], [0, 49.6], [-25, 49.8], [at[0] + 3, 51]], { maxSecs: 60, stopWithin: 2.5, speed: 8 });
    const took = (await P.played()) - d0;
    t.ok(r >= 0 && took < 30, 'the cab is the quickest way down', took);
    await P.headsReset();
    const calls0 = (await callsSoFar()).length;
    await P.secs(5);
    t.ok((await P.heads()).length === 0 && (await callsSoFar()).length === calls0 && !(await P.screen()).dialog, 'waiting with its sign lit, the cab draws no look and no challenge', [await P.heads(), await pc()]);
    await P.use(/Get out/); await P.until(() => !LEDGER.G.tom.inCar, 4);
    await handOver('cab');
    const beliefs = await P.beliefs();
    t.ok(beliefs.some((b) => /Mickey's cab/.test(b.s) && /landing/.test(b.s)), "whoever sees it at the landing has seen the firm's car: the low line says so", beliefs.slice(-2));
    const day = await P.ledger('day book');
    t.ok(/Took the cab to the landing/.test(day) && /Mickey's name on its roof/.test(day), 'and the Ledger has it', day.split('\n').filter((l) => /cab/i.test(l)).slice(0, 2));
    await P.ledgerClose();
    const c1 = await P.car();
    await go(c1.x - 1.6, c1.z + 0.6, { near: 0.9 }); await P.secs(0.3);
    await P.use(/car two/); await P.until(() => LEDGER.G.tom.inCar, 4);
    await P.drive([[-60, 50], [-66, 48], [-58, 46.6], [-12, 46.6], [-3.2, 42], [-3.2, 30], [0, 22], [3.4, 26], [4.1, 36.5]], { maxSecs: 90, stopWithin: 2, speed: 8 });
    await P.use(/Get out/); await P.until(() => !LEDGER.G.tom.inCar, 4);
    await go(7.3, 41.5);
    await homeAndSleep('S05 home cab');
    t.note('cab', await P.world(() => [LEDGER.game.carry.x().envelope, LEDGER.G.money.dirty, (LEDGER.game.carry.x().cabSeenBy || []).length > 0]));
  }

  if (variant === 'dark') {
    await outYard();
    // out of the yard at a walk (his ordinary footsteps), then slowly along the dark side of the quay by the water
    await P.world(() => { const S = window.__S; S.minPc = 99; S.lit = 0; S.eachs.dk = () => { const Q = LEDGER.G.people.pc, t = LEDGER.G.tom; if (!Q.gone && Q.space === 'street') S.minPc = Math.min(S.minPc, Math.hypot(Q.x - t.x, Q.z - t.z)); if (t.space === 'street' && t.light > 0.5) S.lit++; }; });
    const m0 = await P.world(() => LEDGER.mix.length);
    await go(24.5, 39); await go(26, 44);
    const normal = await P.world((m0) => LEDGER.mix.slice(m0).filter((m) => m.n === 'step').map((m) => m.loud), m0);
    const m1 = await P.world(() => LEDGER.mix.length);
    const w0 = await P.played();
    await go(26, 56.5, { slow: true });
    const at = await man();
    await go(at[0] + 14, 56.8, { slow: true, maxSecs: 150 });
    const slow = await P.world((m1) => LEDGER.mix.slice(m1).filter((m) => m.n === 'step').map((m) => m.loud), m1);
    const med = (a) => a.slice().sort((x, y) => x - y)[Math.floor(a.length / 2)];
    t.ok(normal.length > 3 && slow.length > 5 && Math.abs(med(slow) / med(normal) - 0.5) < 0.08, 'walking slowly (Z held) his footsteps carry half as far, and are heard half as loud', [med(normal), med(slow), normal.length, slow.length]);
    t.ok(Math.abs(med(normal) * 10 - 3.6) < 0.5, 'in the small hours a normal footstep carries about 3.6 m', med(normal) * 10);
    await handOver('dark');
    const took = (await P.played()) - w0;
    const seen = await P.world(() => [window.__S.minPc, window.__S.lit]);
    t.ok((await callsSoFar()).length === 0, 'by the dark way he is not challenged: the constable never has sight of him', [seen, await pc()]);
    t.ok(took > 45, 'the dark way is the slower one', took);
    await homeAndSleep('S05 home dark');
    t.note('dark', await P.world(() => [LEDGER.game.carry.x().envelope, LEDGER.G.money.dirty]));
  }

  if (variant === 'runs') {
    const at = await meetConstable();
    const where = await P.tom();
    await P.pick(/Run/);
    await P.secs(0.2);
    // he runs: back along the quay, into Mickey's yard and up the lane behind it
    const c0 = await P.played();
    await P.world(() => { const S = window.__S; S.ch = { last: null, n: 0 }; S.eachs.ch = () => { const x = LEDGER.game.law.x ? LEDGER.game.law.x() : LEDGER.game.x().law; S.ch.n = x.chases.length; S.ch.last = x.chases[x.chases.length - 1] || null; }; });
    const over = () => window.__S.ch && window.__S.ch.n > 0;
    for (const [x, z] of [[24, 43], [25, 36], [29, 27], [29, 20]]) { await P.walkTo(x, z, { run: true, maxSecs: 40, until: over }); if (await P.world(over)) break; }
    if (!(await P.world(over))) await P.until(over, 60);
    const chase = await P.world(() => window.__S.ch.last);
    const secs = (await P.played()) - c0;
    t.ok(chase && secs <= 90, 'the chase ends within 90 real seconds', [chase, secs]);
    t.ok(chase && chase.st === 'lost', 'it is lost once he is out of sight for 7 seconds (or 70 m)', chase);
    const lostAt = await P.tom();
    const day = await P.ledger('day book');
    t.ok(/Ran from the constable/.test(day), 'the run has its Ledger line', day.split('\n').filter((l) => /constable/i.test(l)).slice(0, 2));
    await P.ledgerClose();
    // the constable walks to the last place he saw him and looks round there
    const spot = await P.world(() => { const x = LEDGER.game.x().law; const w = x.watched[x.watched.length - 1]; return w ? [w.x, w.z] : null; });
    const came = await P.until((sx, sz) => { const Q = LEDGER.G.people.pc; return Math.hypot(Q.x - sx, Q.z - sz) < 8; }, 60, spot ? spot[0] : 0, spot ? spot[1] : 0);
    t.ok(spot && came >= 0, 'the constable walks to the last place he saw him', [spot, await pc()]);
    await P.secs(6);
    const still = await pc();
    t.ok(spot && Math.hypot(still.x - spot[0], still.z - spot[1]) < 12, 'and looks round there', [spot, still]);
    // walking back past that spot within the hour brings a fresh call
    const n0 = (await callsSoFar()).length;
    await P.walkTo(spot[0], spot[1], { maxSecs: 60, near: 4, until: called });
    await P.until(() => !!document.querySelector('#dialog:not(.hidden)'), 6);
    const again = await callsSoFar();
    t.ok(again.length > n0 && /Stop there/.test(again[again.length - 1].s), 'walking back past that spot brings a fresh call', again.slice(-2));
    await P.pick(/Run/);
    await P.world(() => { window.__S.ch.n0 = window.__S.ch.n; });
    const over2 = () => window.__S.ch.n > window.__S.ch.n0;
    for (const [x, z] of [[25, 36], [29, 27], [29, 12]]) { await P.walkTo(x, z, { run: true, maxSecs: 40, until: over2 }); if (await P.world(over2)) break; }
    if (!(await P.world(over2))) await P.until(over2, 60);
    const chase2 = await P.world(() => window.__S.ch.last);
    t.ok(chase2 && chase2.st === 'lost' && chase2.seconds <= 90, 'run from again, he is lost again inside 90 seconds', chase2);
    // then round by the dark side of the quay to the landing, while the constable stands about the yard
    await go(29, 30); await go(27, 44); await go(27, 56.5, { slow: true });
    const at2 = await man();
    await go(at2[0] + 14, 56.8, { maxSecs: 150 });
    await handOver('runs');
    await homeAndSleep('S05 home runs');
    t.note('runs', await P.world(() => [LEDGER.game.carry.x().envelope, LEDGER.G.money.dirty, LEDGER.game.x().law.chases.map((c) => c.st)]));
  }
  t.note('played seconds', Math.round((await P.played()) - T0));
}, ['quay', 'cab', 'dark', 'runs']);
