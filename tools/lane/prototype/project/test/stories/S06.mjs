// S06 It comes back, and the count (ONE-SHOT-PROMPT.md). From each save S05 leaves (Tuesday morning in the flat):
// out into Quay Street; Darren says it to his face, by the road it really travelled; somebody else holds a look; the
// Ledger is offered and opened; the count with Sheila; then Escape, save, quit to the title, Continue.
import { run } from './play.mjs';

await run('S06', { from: (v) => 'S05 home ' + v }, async (P, t, n, variant) => {
  const go = async (x, z, o = {}) => { const r = await P.walkTo(x, z, Object.assign({ maxSecs: 90 }, o)); if (r < 0 && !o.until) { const m = await P.tom(); t.ok(false, 'he can walk to ' + Math.round(x) + ', ' + Math.round(z), [Math.round(m.x * 10) / 10, Math.round(m.z * 10) / 10, m.space]); } return r; };
  const local = (room, lx, lz) => P.world(({ room, lx, lz }) => { const r = LEDGER.roomOf(room); return [r.ox + lx, r.oz + lz]; }, { room, lx, lz });
  let s;
  await P.cont();
  const start = await P.world(() => ({ day: Math.floor(LEDGER.G.t / 1440), hour: (LEDGER.G.t % 1440) / 60, space: LEDGER.G.tom.space, things: LEDGER.game.back.x().things.map((q) => q.what) }));
  t.ok(start.day === 1 && start.hour >= 6.9 && start.hour < 8 && start.space === 'flat', 'Tuesday morning, in the flat over the office', start);
  const made = variant !== 'quay';
  t.ok(made ? start.things.includes('made') : start.things.includes('missed'), 'what happened last night is the branch that was played', start.things);
  const T0 = await P.clock();

  // ----- 1. down the stair, out of the front door, into Quay Street -----
  const mat = await local('flat', -3.6, 3.0);
  await go(mat[0], mat[1] - 0.4, { near: 0.8 });
  await P.use(/Down the stair/); await P.until(() => LEDGER.G.tom.space === 'mickeys', 5);
  const door = await local('mickeys', -4.2, 3.2);
  await go(door[0], door[1], { near: 0.6 });
  await P.use(/Leave/); await P.until(() => LEDGER.G.tom.space === 'street', 5);
  // watch for bodies: two heads together where he can see them, looks held, a back turned
  await P.headsReset();
  await P.world(() => { const S = window.__S; S.together = {}; S.eachs.tg = () => { if (S.frameNo % 10) return; const m = LEDGER.G.tom; for (const Q of LEDGER.G.named.concat(LEDGER.G.crowd)) if (Q.chat && !Q.gone && Q.space === m.space && Math.hypot(Q.x - m.x, Q.z - m.z) < 30 && LEDGER.map.clear(m.x, m.z, Q.x, Q.z)) S.together[[Q.id, Q.chat.with].sort().join('+')] = Math.round(LEDGER.G.t); }; });
  const said = () => [...document.querySelectorAll('#subs .s')].some((e) => /^DARREN MILNER/.test(e.innerText) && /chief/.test(e.innerText) && /landing|Ibbotson/.test(e.innerText));
  // along the street: up past the rank and the pavement where Darren stands of a morning, and back, until it is said
  let heard = -1;
  for (let k = 0; k < 40 && heard < 0; k++) {
    for (const [x, z] of [[7.6, 33], [7.6, 30.5], [7.6, 37.5]]) { await P.walkTo(x, z, { maxSecs: 30, until: said }); if (await P.world(said)) { heard = 1; break; } await P.until(said, 6); if (await P.world(said)) { heard = 1; break; } }
    if ((await P.clock()) - T0 > 1440) break;
  }
  const line = ((await P.subsLog()).filter((x) => /^DARREN MILNER/.test(x.s) && /chief/.test(x.s)).pop() || { s: '' }).s;
  const took = (await P.clock()) - T0;
  t.ok(heard > 0 && took < 1440, 'Darren says it to his face within one game day', [Math.round(took), line]);
  const chain = await P.world(() => LEDGER.game.back.chain());
  const knewRun = chain.some((c) => c.what === 'ran' && c.knows.includes('Darren Milner'));
  const knewSearch = chain.some((c) => c.what === 'searched' && c.knows.includes('Darren Milner'));
  const want = variant === 'quay' ? (knewSearch ? /Ibbotson had your coat open.*no envelope came/ : /the landing stood waiting and no envelope came/) : variant === 'runs' && knewRun ? /You ran from Ibbotson and still made the landing/ : /So you carried it.*the landing got its envelope/;
  t.ok(want.test(line), 'what he says matches the branch (' + variant + ')', line);
  t.ok(variant === 'runs' || !/ran/.test(line), 'he never mentions a run that did not happen', line);
  t.ok(variant !== 'runs' || knewRun || !/ran/.test(line), 'and speaks of the run only if somebody who saw it carried it to him', [knewRun, line]);
  // the printed chain: somebody who saw it, and every meeting that carried it to Darren, in order and before he spoke
  const mine = chain.filter((c) => c.knows.includes('Darren Milner'));
  t.ok(mine.length > 0 && mine.every((c) => c.saw.length > 0 && !c.saw.includes('Darren Milner') && c.told.length >= 2 && /told Ron Kirby at the rank/.test(c.told[0]) && /Ron Kirby told Darren Milner on the pavement/.test(c.told[1])), 'Darren was not there: the printed chain shows who saw it and the two meetings that brought it to him', chain);
  await P.secs(7.5);
  // ----- bodies -----
  await go(7.6, 37.2, { near: 1.2, maxSecs: 30 }); await P.secs(4.5);
  const heads = await P.heads();
  const tog = await P.world(() => window.__S.together);
  t.ok(heads.some((h) => h !== 'darren'), 'at least one other person holds a look too long', heads);
  const avoided = await P.world(() => LEDGER.game.back.x().avoided);
  t.ok(heads.length >= 2 && (Object.keys(tog).length > 0 || avoided.length > 0), 'who knows shows in bodies: looks held, and two heads together or a back turned', [heads, tog, avoided]);
  t.ok(made || avoided.length > 0, 'when it went badly, a man who knows turns his back on him', avoided);
  // ----- 2. the Ledger, offered now, opened -----
  s = await P.screen();
  t.ok(s.prompts.some((p) => /^L\s*The Ledger/.test(p)), 'the Ledger is offered', s.prompts);
  await P.ledger('people');
  // his page for one person: / and a letter jumps to that letter, Down goes on through the names
  const pageOf = async (letter, rx) => { await P.tap('Slash'); await P.frames(6); await P.tap('Key' + letter); await P.frames(12); for (let k = 0; k < 30; k++) { const s = (await P.screen()).ledger; if (rx.test(s)) return s; await P.tap('ArrowDown'); await P.frames(10); } return (await P.screen()).ledger; };
  let people = await pageOf('D', /Darren Milner knows he/);
  t.ok(/Darren Milner knows he/.test(people) && /Said to his face\. Sure\./.test(people), 'People: what Darren knows, said to his face, sure', people.split('\n').filter((l) => /Darren|Said to his face/.test(l)).slice(0, 4));
  people = await pageOf('R', /looked at him a moment too long/);
  t.ok(/looked at him a moment too long/.test(people) && /Saw him looking\. Thinks so\./.test(people), 'People: the one seen looking is "thinks so"', people.split('\n').filter((l) => /looked|Saw him looking/.test(l)).slice(0, 4));
  await P.ledgerClose();
  await P.secs(0.5);
  t.ok(!(await P.screen()).prompts.some((p) => /^L\s*The Ledger/.test(p)), 'once opened, the offer is gone', (await P.screen()).prompts);

  // ----- 3. the count with Sheila -----
  await P.until(() => { const S = LEDGER.G.people.sheila; return S.space === 'mickeys' && !S.moving && (LEDGER.G.t % 1440) / 60 >= 7.55; }, 120);
  await go(7.9, 36.2, { near: 0.9 }); await P.face(7.2, 36); await P.secs(0.3);
  await P.use(/Mickey|office|door/i); await P.until(() => LEDGER.G.tom.space === 'mickeys', 5);
  const sh = await P.world(() => { const S = LEDGER.G.people.sheila; return [S.x, S.z]; });
  await go(sh[0] - 1.3, sh[1] + 1.5, { near: 0.7 }); await P.secs(0.3);
  const before = await P.world(() => ({ tin: LEDGER.G.money.dirty, washed: LEDGER.G.money.washed, fares: LEDGER.G.money.fares, room: LEDGER.game.count.room(), pocket: LEDGER.G.money.clean, since: LEDGER.G.money.sinceWash }));
  const moneyBefore = await P.ledger('money'); await P.ledgerClose();
  s = await P.screen();
  t.ok(s.prompts.some((p) => /count|Which/i.test(p)), 'at her desk the count has its prompt', s.prompts);
  const c0 = await P.played();
  await P.tap('KeyE'); await P.frames(20);
  let d = await P.choice();
  if (d && !/^The count\./.test(d.text)) { await P.pick(/count/i); d = await P.choice(); }
  t.ok(d && /The book can hide ten pounds and four fifths of the fares really driven/.test(d.text) && d.opts.some((o) => /All of it/.test(o)), 'Sheila says what the book can hide: ten pounds and four fifths of the fares really driven', d);
  t.ok(before.room === 1000 + Math.round(before.since * 0.8), 'the limit is £10 plus 80% of the fares since the last wash', before);
  await P.pick(/All of it/);
  let moved;
  if (before.tin > before.room) {
    d = await P.choice();
    t.ok(d && /That's more than the book will stand, love\. You sure\?/.test(d.text), 'asked for the whole tin, she says the books would be off before she does it', d);
    t.ok((await P.world(() => LEDGER.G.money.dirty)) === before.tin, 'and nothing has moved yet', 0);
    await P.pick(/What the book will stand/);
    moved = before.room;
  } else {
    moved = before.tin;
    t.note('whole tin inside the limit', [before.tin, before.room]);
  }
  const done = await P.readOn();
  t.ok(/out of the tin, and .* more in the fare book/.test(done.join(' ')), 'inside the limit she does it, and says the sum in words', done);
  await P.until(() => !LEDGER.G.paused && !LEDGER.ui.modal, 10);
  t.ok((await P.played()) - c0 <= 20, 'the count takes twenty seconds or less', (await P.played()) - c0);
  const after = await P.world(() => ({ tin: LEDGER.G.money.dirty, washed: LEDGER.G.money.washed, pocket: LEDGER.G.money.clean, off: LEDGER.G.money.booksOff, bal: LEDGER.game.econ.balances() }));
  t.ok(before.tin - after.tin === moved && after.washed - before.washed === moved && after.off === 0, 'the tin and the fare book move by the same sum', [before, after, moved]);
  t.ok(after.bal.holds !== false && after.bal.pocket === after.bal.pocketByFlows && after.bal.tin === after.bal.tinByFlows, 'the flows ledger balances', after.bal);
  const moneyAfter = await P.ledger('money'); await P.ledgerClose();
  const tinWords = (m) => (m.match(/The tin (has about £[\d.]+ in it|is empty)/) || [''])[0], bookWords = (m) => (m.match(/£[\d.]+ (of fares )?in the fare book this week[^.]*\./) || [''])[0];
  t.ok(tinWords(moneyBefore) !== tinWords(moneyAfter) && bookWords(moneyBefore) !== bookWords(moneyAfter) && /put through from the tin/.test(moneyAfter), 'Money says both in words, before and after', [tinWords(moneyBefore), bookWords(moneyBefore), tinWords(moneyAfter), bookWords(moneyAfter)]);
  const day = await P.ledger('day book');
  t.ok(/The count: .* out of the tin and into the fare book/.test(day), 'the count has its Ledger line', day.split('\n').filter((l) => /count/i.test(l)).slice(0, 2));
  await P.ledgerClose();
  // once a day
  await P.secs(0.6);
  t.ok(!(await P.screen()).prompts.some((p) => /The count/.test(p)), 'the count is once a day', (await P.screen()).prompts);

  // ----- 4. Escape, save, quit to the title, Continue -----
  const snap = () => P.world(() => { const G = LEDGER.G; const h = (s) => { let x = 0; for (let i = 0; i < s.length; i++) x = (x * 31 + s.charCodeAt(i)) | 0; return x; }; return { t: Math.floor(G.t), x: Math.round(G.tom.x * 10) / 10, z: Math.round(G.tom.z * 10) / 10, space: G.tom.space, notes: G.ledger.notes.length, ledger: h(JSON.stringify(G.ledger.notes.map((q) => [q.t, q.text || q.key]))), minds: h(JSON.stringify(G.named.map((Q) => [Q.id, Q.mind.mem.map((m) => [m.e, m.src, m.who])]))), back: h(JSON.stringify(G.x.back.things)), money: [G.money.clean, G.money.dirty, G.money.washed] }; });
  await P.tap('Escape'); await P.frames(18);
  const s0 = await snap();
  await P.click('[data-act="save"]'); await P.frames(30);
  t.ok(/Saved/.test((await P.screen()).book), 'Escape, and the game saves', (await P.screen()).book.slice(0, 80));
  if (!(await P.world(() => !!document.querySelector('[data-act="quit"]')))) { await P.tap('Escape'); await P.frames(18); await P.tap('Escape'); await P.frames(18); }
  await P.click('[data-act="quit"]'); await P.frames(40);
  s = await P.screen();
  t.ok(s.title && s.title.some((b) => /continue/i.test(b)), 'quit to the title: Continue is offered', s.title);
  if (t.first && variant === 'cab') await P.keep('S06 count');
  await P.cont();
  const s1 = await snap();
  t.ok(s1.space === s0.space && Math.abs(s1.x - s0.x) < 0.3 && Math.abs(s1.z - s0.z) < 0.3 && s1.t - s0.t >= 0 && s1.t - s0.t <= 1, 'after Continue he stands where he was, at the same game minute', [s0, s1]);
  t.ok(s1.notes === s0.notes && s1.ledger === s0.ledger && s1.minds === s0.minds && s1.back === s0.back && s1.money.join() === s0.money.join(), 'and every memory and Ledger line is as before', [s0, s1]);
  t.note(variant, [line, chain.map((c) => [c.what, c.saw, c.told.length]), heads.sort(), moved]);
  t.note('played seconds', Math.round(await P.played()));
}, ['quay', 'cab', 'dark', 'runs']);
