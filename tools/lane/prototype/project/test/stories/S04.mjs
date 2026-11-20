// S04 The outfit's first ask and getting ready (ONE-SHOT-PROMPT.md). From the save S03 leaves (the "fronts" way), three
// ways on their own: he says yes and gets ready; he says no, and no again when asked twice; he walks away and stays
// out of the office.
import { run } from './play.mjs';

await run('S04', { from: 'S03 fronts' }, async (P, t, n, variant) => {
  const go = async (x, z, o = {}) => { const r = await P.walkTo(x, z, Object.assign({ maxSecs: 60 }, o)); if (r < 0) { const m = await P.tom(); t.ok(false, 'he can walk to ' + Math.round(x) + ', ' + Math.round(z), [Math.round(m.x * 10) / 10, Math.round(m.z * 10) / 10, m.space, await P.world(() => [LEDGER.standable(LEDGER.G.tom.x, LEDGER.G.tom.z), window.__S.lastPlan, LEDGER.G.paused, LEDGER.ui.modal, LEDGER.ui.inScene, LEDGER.G.tom.carry, LEDGER.cam.yaw])]); } return r; };
  const local = (lx, lz) => P.world(({ lx, lz }) => { const r = LEDGER.roomOf('mickeys'); return [r.ox + lx, r.oz + lz]; }, { lx, lz });
  let s;
  // G in the office: the locked drawer (when G has two things on it, the game asks which)
  const openDrawer = async () => { await P.tap('KeyG'); await P.frames(20); let d = await P.choice(); if (d && !/^The locked drawer/.test(d.text)) { await P.pick(/drawer/); d = await P.choice(); } return d; };
  await P.cont();
  // 1. at the office, the wait key until Ron comes after dark
  await go(6.2, 36, { near: 0.6 }); await P.face(7.2, 36); await P.secs(0.3);
  await P.use(/Go into Mickey/);
  await P.until(() => LEDGER.G.tom.space === 'mickeys', 5);
  const c0 = await P.clock();
  await P.down('KeyZ');
  const came = await P.until(() => !!document.querySelector('#dialog:not(.hidden)') && /Boss/.test(document.getElementById('dtxt').innerText + ' '), 40);
  await P.secs(0.5);
  const c1 = await P.clock();
  await P.secs(1);
  const c2 = await P.clock();
  await P.up('KeyZ');
  const ron = await P.world(() => { const R = LEDGER.G.people.ron, t = LEDGER.G.tom; return { space: R.space, d: Math.hypot(R.x - t.x, R.z - t.z), hour: (LEDGER.G.t % 1440) / 60 }; });
  t.ok(came >= 0 && ron.space === 'mickeys' && ron.d < 2.2, 'after dark Ron brings the ask in person, at the office: he walks in and up to him', [came, ron]);
  t.ok(ron.hour >= 19.75 || ron.hour < 5, 'it is after dark', ron.hour);
  t.ok(c2 === c1, 'the wait stops when Ron arrives (the wait key still held, the clock stands)', [c0, c1, c2]);
  const lines = await P.readOn();
  const said = lines.join(' ');
  t.ok(/envelope/.test(said) && /ferry landing/.test(said) && /after ten/.test(said) && /shelter under the last lamp/.test(said) && /Harbour Office clock/.test(said) && /dark coat/.test(said), 'the ask: a dark coat and an envelope for the ferry landing after ten, the landing named by its landmark', lines);
  t.ok(lines.every((l) => /^Ron Kirby/i.test(l)), 'it names its giver: Ron says it himself', lines.map((l) => l.slice(0, 12)));
  await P.secs(0.5);
  s = await P.screen();
  if (s.talk && !s.talk.lines.length) { await P.tap('Tab'); await P.frames(12); s = await P.screen(); }
  t.ok(s.talk && /still on\?/.test(s.talk.log.join(' ')) && s.talk.lines.some((l) => /take it|walk it down/.test(l)) && s.talk.lines.some((l) => /Tell them no|Count me out/.test(l)) && s.talk.leave, "the decision is the game's own lines, with Leave offered", s.talk);

  if (variant === 'yes') {
    await P.talkSay(/take it|walk it down/);
    s = await P.screen();
    if (!s.talk.lines.length) { await P.tap('Tab'); await P.frames(12); s = await P.screen(); }
    t.ok(/You'll take it\?/.test(s.talk.log.slice(-1)[0]) && s.talk.lines.some((l) => /^Yes/.test(l)) && s.talk.lines.some((l) => /^No/.test(l)) && s.talk.lines.length >= 3, 'a yes, a no and a line that keeps talking', s.talk.lines);
    await P.talkSay(/^Yes/);
    const after = await P.readOn();
    t.ok(/ten till one/.test(after.join(' ')) && /coat's on the hook/.test(after.join(' ')), 'on a plain yes Ron hands him the envelope and says where the coat is and when the landing is open', after);
    await P.secs(0.5);
    t.ok((await P.world(() => LEDGER.G.tom.carry)) === 'envelope', 'the envelope is in his hand', await P.world(() => LEDGER.G.tom.carry));
    const open = await P.ledger('open');
    t.ok(/The envelope, to the ferry landing, the shelter under the last lamp/.test(open) && /Ron says/.test(open) && /his hand|in his hand/.test(open), 'Open names the job, its giver, the landing by its landmark, and what he carries', open.split('\n').filter((l) => /envelope|carries/i.test(l)));
    await P.ledgerClose();
    // 3. getting ready, with the hands: the coat with its key, the envelope under it, a third thing refused, the crowbar in the drawer
    const hook = await local(1.6, -2.3);
    await go(hook[0], hook[1], { near: 0.5 }); await P.secs(0.3);
    s = await P.screen();
    t.ok(s.prompts.some((p) => /dark coat/.test(p)), 'the hook has a prompt that names the dark coat', s.prompts);
    await P.tap('KeyT'); await P.frames(15); // before the coat is on: nowhere to hide it
    t.ok((await P.screen()).subs.some((x) => /coat is not on him/.test(x)), 'without the coat the envelope cannot be hidden, and a line says why', (await P.screen()).subs);
    await P.use(/dark coat/); await P.secs(0.4);
    await P.tap('KeyC'); await P.secs(0.4);
    t.ok(await P.world(() => LEDGER.G.tom.coat === true), 'the coat goes on with its one key', await P.world(() => [LEDGER.G.tom.hasCoat, LEDGER.G.tom.coat]));
    await P.tap('KeyT'); await P.secs(0.4);
    t.ok((await P.world(() => [LEDGER.G.tom.carry, LEDGER.game.x().crime.pockets.map((p) => p.id)])).join() === ',envelope', 'the envelope goes under the coat', await P.world(() => [LEDGER.G.tom.carry, LEDGER.game.x().crime.pockets]));
    const nail = await local(5.6, 0.3);
    await go(nail[0], nail[1], { near: 0.5 }); await P.secs(0.3);
    s = await P.screen();
    t.ok(s.prompts.some((p) => /crowbar/.test(p)), 'the crowbar on its nail has a prompt', s.prompts);
    await P.tap('KeyT'); await P.secs(0.4);
    if ((await P.screen()).dialog) await P.pick(/crowbar/);
    await P.secs(0.3);
    t.ok((await P.world(() => LEDGER.game.x().crime.pockets.map((p) => p.id))).join() === 'envelope,crowbar', 'two things fit under the coat', await P.world(() => LEDGER.game.x().crime.pockets));
    // the locked drawer: Mickey's cosh is in it; a third thing under the coat is refused
    s = { dialog: await openDrawer() };
    t.ok(s.dialog && /drawer/i.test(s.dialog.text) && /cosh/.test(s.dialog.text), "the locked drawer opens: Mickey's cosh is in it", s.dialog);
    await P.pick(/Take a cosh/); await P.secs(0.4);
    s = await P.screen();
    t.ok(s.subs.some((x) => /Two things under the coat is all it hides/.test(x)) && (await P.world(() => LEDGER.game.x().crime.pockets.length)) === 2, 'the third thing is refused, with a line saying why', s.subs);
    await P.secs(1);
    await openDrawer();
    await P.pick(/Put away a crowbar/); await P.secs(0.4);
    s = { dialog: await openDrawer() };
    t.ok(s.dialog && /In it: a cosh, a crowbar/.test(s.dialog.text), 'the drawer keeps the crowbar', s.dialog);
    await P.pick(/Shut/); await P.secs(0.3);
    const open2 = await P.ledger('open');
    t.ok(/He carries the envelope under his coat/.test(open2), 'Open says in words what he carries', open2.split('\n').filter((l) => /carries/i.test(l)));
    await P.ledgerClose();
    t.note('ready', await P.world(() => [LEDGER.G.tom.coat, LEDGER.game.x().crime.pockets.map((p) => p.id), LEDGER.game.x().crime.stored.map((p) => p.id)]));
  }

  if (variant === 'no') {
    await P.talkSay(/Tell them no|Count me out/);
    s = await P.screen();
    t.ok(/You want me to tell them no\?/.test(s.talk.log.slice(-1)[0]), 'no is asked about', s.talk.log.slice(-2));
    await P.talkSay(/^Yes/);
    s = await P.screen();
    t.ok(/for certain\?/.test(s.talk.log.slice(-1)[0]) && (await P.world(() => LEDGER.game.outfit.x().ask1)) !== 'no', 'and asked a second time before it is taken', s.talk.log.slice(-2));
    await P.talkSay(/^Yes/);
    const after = await P.readOn();
    t.ok(/I tell them no/.test(after.join(' ')), 'on the second yes it is a no, and Ron says he will tell them', after);
    await P.secs(0.5);
    const day = await P.ledger('day book');
    t.ok(/Said no to Ron Kirby, and no again/.test(day), 'the Ledger has it', day.split('\n').filter((l) => /Ron Kirby/.test(l)).slice(0, 3));
    await P.ledgerClose();
    t.ok((await P.world(() => LEDGER.G.tom.carry)) !== 'envelope', 'no envelope is in his hand', 0);
    t.note('no', await P.world(() => LEDGER.game.outfit.x().ask1));
  }

  if (variant === 'away') {
    await P.click('#tbye');
    const after = await P.readOn();
    t.ok(/on the rank/.test(after.join(' ')), 'he walks away from it: Ron says he will be on the rank', after);
    await P.secs(0.5);
    const mat = await local(-4.2, 3.2);
    await go(mat[0], mat[1], { near: 0.6 });
    await P.use(/Leave/);
    await P.until(() => LEDGER.G.tom.space === 'street', 5);
    await go(7.3, 22);
    const w0 = await P.clock();
    await P.hold('KeyZ', 6); // he stays out of the office: an hour and more goes by on the wait key
    t.ok((await P.clock()) - w0 > 50, 'the wait key passes the time out on the street', (await P.clock()) - w0);
    await go(6.2, 36, { near: 0.6 }); await P.face(7.2, 36); await P.secs(0.3);
    await P.use(/Go into Mickey/);
    await P.until(() => LEDGER.G.tom.space === 'mickeys', 5);
    await P.secs(1.5);
    s = await P.screen();
    t.ok(s.subs.some((x) => /left it in my drawer|It is in the drawer/.test(x)), "staying away, Ron has left the envelope with Sheila's word", s.subs);
    const day = await P.ledger('day book');
    t.ok(/left the envelope with Sheila/.test(day) && /unanswered/.test(day), 'the ask ends unanswered, written in the Ledger', day.split('\n').filter((l) => /envelope/.test(l)).slice(0, 2));
    await P.ledgerClose();
    s = { dialog: await openDrawer() };
    t.ok(s.dialog && /the envelope/.test(s.dialog.text), 'the envelope is in the drawer', s.dialog);
    await P.pick(/Shut/); await P.secs(0.3);
    t.note('away', await P.world(() => LEDGER.game.outfit.x().ask1));
  }
  t.ok(await P.save(t.first ? 'S04 ' + variant : null), 'the game saves', 0);
}, ['yes', 'no', 'away']);
