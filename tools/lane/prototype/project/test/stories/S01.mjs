// S01 Off the ferry (ONE-SHOT-PROMPT.md). Played by keys from New game; judged by the screen, the mix and the bodies.
import { run, FPS } from './play.mjs';

const subsNow = (P) => P.screen().then((s) => s.subs);
// run for secs, collecting every distinct subtitle line that was on screen and when (real seconds from the start of the watch)
async function watch(P, secs, each = 0.25) {
  const seen = [];
  for (let t = 0; t < secs; t += each) {
    await P.secs(each);
    for (const s of await subsNow(P)) if (!seen.some((x) => x.s === s)) seen.push({ s, at: t + each });
  }
  return seen;
}
const HINT = /W A S D|Quay Street is up the quay|E uses what/;

await run('S01', {}, async (P, t, n) => {
  // walk by keys to a point; a walk that does not arrive is a failed step, said with where he got to
  const go = async (x, z, o = {}) => { const r = await P.walkTo(x, z, Object.assign({ maxSecs: 60 }, o)); if (r < 0) { const m = await P.tom(); t.ok(false, 'he can walk to ' + x + ', ' + z, [Math.round(m.x * 10) / 10, Math.round(m.z * 10) / 10, m.space]); } return r; };
  // ---- 1. New game; nothing pressed for 25 s (run 1), or Escape during the ferry shot (run 2) ----
  let s = await P.screen();
  t.ok(s.title && s.title.some((b) => /new game/i.test(b)) && s.title.some((b) => /quit/i.test(b)), 'the title offers New game and Quit', s.title);
  await P.click('[data-act="new"]');
  const ctl = () => { const G = LEDGER.G; return G.story.phase === 'play' && !G.paused && G.tom.space === 'street' && !document.getElementById('hud').classList.contains('hidden'); };
  let shot;
  if (n === 1) {
    shot = await P.until(ctl, 40);
    t.ok(shot > 18 && shot < 22, 'the ferry shot lasts about 20 real seconds and ends by itself', shot);
    const idle = await watch(P, 25 - shot);
  } else {
    await P.secs(3);
    await P.tap('Escape');
    shot = await P.until(ctl, 5);
    t.ok(shot >= 0 && shot < 0.5, 'Escape ends the ferry shot at once', shot);
    s = await P.screen();
    t.ok(!s.panel && !s.book, 'the skip does not open the pause menu', s.book);
  }
  const tom0 = await P.tom();
  const carry = await P.world(() => LEDGER.G.tom.carry);
  t.ok(carry === 'suitcase' && tom0.space === 'street', 'Tom is under control at the gangway, suitcase in hand', { carry, tom0 });
  s = await P.screen();
  t.ok(s.hud.every((id) => ['bubbles', 'subs', 'prompt', 'noted', 'watch'].includes(id)), 'the screen shows no clock, money figure, meter or to-do slip', s.hud);

  // ---- 2. down the gangway and up the quay; no hint while he moves; standing still brings one ----
  const before = (await subsNow(P)).filter((x) => HINT.test(x));
  await P.down('KeyW');
  const moving = await watch(P, 6);
  await P.up('KeyW');
  t.ok(!moving.some((x) => HINT.test(x.s) && !before.includes(x.s)), 'no hint shows while he moves', moving);
  const turned0 = await P.world(() => LEDGER.G.named.concat(LEDGER.G.crowd).filter((Q) => Q.space === 'street' && !Q.gone && Q.mind.look > 0).map((Q) => Q.id));
  let tw = await P.walkTo(-40, 43.5, { maxSecs: 60 });
  t.ok(tw > 0, 'he walks up the gangway onto the quay', await P.tom());
  // he stands: one hint at about 4 s, and no second inside 12 s
  const seenBefore = (await subsNow(P)).filter((x) => HINT.test(x));
  const stand = await watch(P, 5);
  const fresh = stand.filter((x) => HINT.test(x.s) && !seenBefore.includes(x.s));
  t.ok(fresh.length === 1 && fresh[0].at >= 3.5 && fresh[0].at <= 4.8, 'standing still for 4 real seconds brings one first hint, once', { fresh, seenBefore });
  const more = await watch(P, 10.5);
  t.ok(!more.some((x) => HINT.test(x.s) && !seenBefore.includes(x.s) && !fresh.some((f) => f.s === x.s)), 'no second hint inside 12 real seconds', more);

  // ---- 3. into Quay Street past Ron, Darren, Ada's window and June: each a line in passing, with its audio ----
  for (const [x, z] of [[-2, 43], [7.3, 41], [7.3, 31.5], [-4.6, 31], [-4.4, 18.5]]) {
    await go(x, z);
    await P.secs(1.5);
  }
  await P.secs(3);
  const heads = new Set(turned0.concat(await P.heads()));
  const said = {};
  for (const x of await P.subsLog()) for (const who of ['Darren', 'Ron', 'woman at a window', 'June']) if (x.s.toUpperCase().startsWith(who.toUpperCase()) || x.s.toUpperCase().startsWith('A ' + who.toUpperCase())) said[who] = said[who] || { line: x.s, played: x.at };
  t.ok(heads.size >= 2, 'people on the quay turn their heads as he passes (at least two bodies)', [...heads]);
  for (const who of ['Darren', 'Ron', 'woman at a window', 'June']) t.ok(!!said[who], who + ' says a line in passing, shown as a subtitle', Object.keys(said));
  t.ok(said.Ron && /boss/.test(said.Ron.line), 'Ron calls him "boss"', said.Ron);
  const mix = await P.world(() => LEDGER.mix.filter((m) => m.n === 'voice').map((m) => [m.who, m.loud]));
  for (const who of ['Darren Milner', 'Ron Kirby', 'A woman at a window', 'June Suddaby']) t.ok(mix.some((m) => m[0] === who && m[1] >= 0.3), who + "'s line is in the sound mix with its loudness", mix.slice(0, 12));
  const lastSaid = Math.max(...Object.values(said).map((v) => v.played));
  // the first run stands idle on purpose (25 s at the start, 16 s for the hints); the second run is the player's pace
  t.ok(lastSaid < (n === 1 ? 150 : 100), 'the four lines in passing are heard by about 1:30 of play', lastSaid);
  t.note('who spoke in passing', Object.keys(said).sort());

  // ---- 4. talk to Darren by keyboard: the AI notice, Tab, a suggested line, a typed line, Leave ----
  const dar = await P.world(() => { const D = LEDGER.G.people.darren; return [D.x, D.z]; });
  await go(dar[0] - 1.2, dar[1], { near: 1.0 });
  await P.face(dar[0], dar[1]);
  await P.secs(0.4);
  s = await P.screen();
  t.ok(s.prompts.some((p) => /Darren/.test(p)), 'the prompt names Darren, ahead and in view', s.prompts);
  const subBox = await P.world(() => { const r = (e) => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; }; return { subs: [...document.querySelectorAll('#subs .s')].map(r), prompts: [...document.querySelectorAll('#prompt > div')].map(r) }; });
  const hit = (a, b) => a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3];
  t.ok(!subBox.subs.some((a) => subBox.prompts.some((b) => hit(a, b))), 'no prompt sits over a subtitle', subBox);
  const clock0 = await P.clock(), pos0 = await P.tom();
  await P.tap('KeyE');
  await P.secs(0.5);
  s = await P.screen();
  t.ok(s.talk && /written by an AI/i.test(s.talk.log.join(' ')), 'the AI notice shows before the first talk', s.talk);
  t.ok(!!s.talk, 'E opens a talk with Darren', s);
  t.ok(s.talk && s.talk.leave, 'Leave is offered', s.talk);
  await P.tap('Tab');
  await P.secs(0.3);
  s = await P.screen();
  t.ok(s.talk && s.talk.lines.length >= 2, 'Tab shows suggested lines', s.talk);
  await P.tap('Enter'); // the first of them
  const r1 = await P.until(() => document.querySelectorAll('#tlog > *').length >= 2, 9);
  t.ok(r1 >= 0 && r1 <= 2.2, 'a reply is heard within 2 real seconds or a written line plays', r1);
  await P.world(() => document.getElementById('tin').focus());
  await P.type('What do you hear about the fish dock');
  const posT = await P.tom();
  t.ok(Math.hypot(posT.x - pos0.x, posT.z - pos0.z) < 0.01, 'typing never moves Tom', [pos0, posT]);
  const logN = await P.world(() => document.querySelectorAll('#tlog > *').length);
  await P.tap('Enter');
  const r2 = await P.until((n0) => document.querySelectorAll('#tlog > *').length >= n0 + 2, 9, logN);
  t.ok(r2 >= 0 && r2 <= 2.2, 'the typed line is answered within 2 real seconds or by a written line', r2);
  // a line can be reported from the talk screen
  await P.click('[data-act="report"]');
  await P.secs(0.3);
  s = await P.screen();
  t.ok(/line reported/i.test(JSON.stringify(s)), 'a line can be reported from the talk screen, and "line reported" shows', s.talk);
  t.ok(Math.abs((await P.clock()) - clock0) < 0.01, 'in talk the clock on the watch does not move', [clock0, await P.clock()]);
  await P.click('#tbye');
  await P.secs(0.6);
  s = await P.screen();
  t.ok(!s.talk, 'Leave ends the talk', s.talk);
  // ... and from the pause menu
  await P.tap('Escape'); await P.secs(0.3);
  await P.click('[data-act="reportline"]'); await P.secs(0.3);
  s = await P.screen();
  t.ok(/line reported/i.test(JSON.stringify(s)), 'a line can be reported from the pause menu', s.book.slice(0, 300));
  await P.tap('Escape'); await P.secs(0.4);
  // the notice never shows again
  await P.tap('KeyE'); await P.secs(0.6);
  s = await P.screen();
  t.ok(!!s.talk && !/written by an AI/i.test(s.talk.log.join(' ')), 'the AI notice never shows again', s.talk);
  await P.click('#tbye'); await P.secs(0.6);

  // ---- 7 (played here, while Darren is still on the pavement to talk to). The window at each of the four layout sizes,
  // from the settings, and back ----
  const layout = () => P.world(() => {
    const vis = (e) => { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05) return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
    const W = innerWidth, H = innerHeight, out = { W, H, small: [], off: [], over: [] };
    const texts = [...document.querySelectorAll('#hud *, #dialog *, #talk *, #panel *, #ledgerp *')].filter((e) => vis(e) && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()));
    for (const e of texts) {
      let p = e, shown = true;
      while (p && p !== document.body) { if (!vis(p)) shown = false; p = p.parentElement; }
      if (!shown) continue;
      const fs = parseFloat(getComputedStyle(e).fontSize), r = e.getBoundingClientRect();
      if (fs < 24) out.small.push([e.id || e.className || e.tagName, fs]);
      // inside a scrolling page a line may be scrolled out; the page itself must be on the screen
      const sc = e.closest('.book');
      const b = sc ? sc.getBoundingClientRect() : r;
      if (b.left < -1 || b.top < -1 || b.right > W + 1 || b.bottom > H + 1) out.off.push([e.id || e.className || e.tagName, Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]);
    }
    const blocks = ['#subs .s', '#prompt > div', '#noted.on', '#watch.on'].flatMap((q) => [...document.querySelectorAll(q)].filter(vis).map((e) => [q, e.getBoundingClientRect()]));
    for (let i = 0; i < blocks.length; i++) for (let j = i + 1; j < blocks.length; j++) { const a = blocks[i][1], b = blocks[j][1]; if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) out.over.push([blocks[i][0], blocks[j][0]]); }
    out.small = out.small.slice(0, 6); out.off = out.off.slice(0, 6);
    return out;
  });
  for (const size of ['1600 x 900', '1920 x 1080', '1000 x 600', '1280 x 720']) {
    await P.tap('Escape'); await P.secs(0.3);
    await P.click('[data-act="settings"]'); await P.secs(0.3);
    await P.world((size) => { const el = document.querySelector('[data-set="layout"]'); el.value = size; el.dispatchEvent(new Event('change', { bubbles: true })); }, size);
    await P.secs(0.5);
    const inSettings = await layout();
    const [w, h] = size.split(' x ').map(Number);
    t.ok(inSettings.W === w && inSettings.H === h, 'the settings change the window to ' + size, [inSettings.W, inSettings.H]);
    t.ok(!inSettings.small.length && !inSettings.off.length, size + ': the settings page keeps its words on the screen, none under 24 units', inSettings);
    await P.tap('Escape'); await P.secs(0.3);
    if ((await P.screen()).book) { await P.tap('Escape'); await P.secs(0.3); }
    // a line on screen with a prompt: talk to Sheila, then leave
    const sh = await P.world(() => { const S = LEDGER.G.people.darren; return [S.x, S.z]; });
    await go(sh[0] - 1.2, sh[1], { near: 1.0 });
    await P.face(sh[0], sh[1]); await P.secs(0.3);
    const onFoot = await layout();
    t.ok(!onFoot.small.length && !onFoot.off.length && !onFoot.over.length, size + ': on foot no words overlap or leave the screen, none under 24 units', onFoot);
    await P.tap('KeyE'); await P.secs(0.8);
    await P.tap('Tab'); await P.secs(0.3);
    const inTalk = await layout();
    t.ok(!!(await P.screen()).talk && !inTalk.small.length && !inTalk.off.length, size + ': in talk no words leave the screen, none under 24 units', inTalk);
    await P.click('#tbye'); await P.secs(0.6);
    await P.tap('KeyL'); await P.secs(0.4);
    const inLedger = await layout();
    t.ok(!inLedger.small.length && !inLedger.off.length, size + ': the Ledger keeps its words on the screen, none under 24 units', inLedger);
    await P.tap('KeyL'); await P.secs(0.4);
  }

  // ---- 5. a whole talk with June by pad alone: walk up, talk, a suggested line, her decision, leave ----
  const jn = await P.world(() => { const J = LEDGER.G.people.june; return [J.x, J.z]; });
  await go(jn[0] + 4, jn[1] + 1.5, { near: 1.2 });
  await P.world(() => window.__S.padOn());
  const padPress = async (i) => { await P.world((i) => window.__S.padBtn(i, 1), i); await P.frames(4); await P.world((i) => window.__S.padBtn(i, 0), i); await P.frames(8); };
  const padGot = await P.world(async ({ x, z }) => {
    const S = window.__S, t = LEDGER.G.tom;
    const angd = (a, b) => { let d = b - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return d; };
    const n = await S.run(900, () => Math.hypot(t.x - x, t.z - z) < 1.5, () => { const off = angd(LEDGER.cam.yaw, Math.atan2(x - t.x, z - t.z)); S.padAxis(2, -Math.max(-1, Math.min(1, off * 2))); S.padAxis(1, Math.abs(off) < 0.5 ? -1 : 0); });
    S.padAxis(1, 0); S.padAxis(2, 0);
    return n;
  }, { x: jn[0], z: jn[1] });
  await P.frames(20);
  s = await P.screen();
  t.ok(padGot > 0 && s.prompts.some((p) => /June/.test(p)), 'by the pad stick he walks up to June, and the prompt names her', { padGot, p: s.prompts });
  t.ok(s.prompts.every((p) => !/^E\b/.test(p)), 'prompts name the pad buttons while the pad is in the hands', s.prompts);
  await padPress(0);
  await P.secs(0.6);
  s = await P.screen();
  t.ok(!!s.talk && s.talk.lines.length >= 2, 'on the pad a talk opens with suggested lines shown at once', s.talk);
  const sayByPad = async (rx) => {
    const lines = (await P.screen()).talk.lines;
    const i = lines.findIndex((l) => rx.test(l));
    if (i < 0) return false;
    const sel = await P.world(() => [...document.querySelectorAll('#tlines > *')].findIndex((e) => e.classList.contains('on') || e.classList.contains('sel')));
    for (let k = 0; k < (i - Math.max(0, sel) + lines.length) % lines.length; k++) await padPress(13);
    const n0 = await P.world(() => document.querySelectorAll('#tlog > *').length);
    await padPress(0);
    await P.until((n0) => document.querySelectorAll('#tlog > *').length >= n0 + 2 && !document.getElementById('talk').classList.contains('busy'), 9, n0);
    await P.secs(0.4);
    return true;
  };
  let raised = /never saw me/i.test((await P.screen()).talk.log.join(' '));
  for (let k = 0; k < 3 && !raised; k++) { await sayByPad(/./); raised = /never saw me/i.test((await P.screen()).talk.log.join(' ')); }
  t.ok(raised, 'June puts her decision in the talk: a yes, a no and a line that keeps talking', (await P.screen()).talk);
  s = await P.screen();
  t.ok(s.talk.lines.some((l) => /^.?.?.?Yes/.test(l)) && s.talk.lines.some((l) => /^.?.?.?No/.test(l)) && s.talk.lines.length >= 3, 'the decision is offered as the game\'s own lines', s.talk.lines);
  await sayByPad(/Why would she ask|What is it between/);
  s = await P.screen();
  t.ok(/Yes or no/i.test(s.talk.log.slice(-2).join(' ')), 'the line that keeps talking keeps the decision open', s.talk);
  await sayByPad(/Yes/);
  s = await P.screen();
  t.ok(/only thing I'll ever ask/i.test(s.talk.log.join(' ')), 'a plain yes, by pad, is taken', s.talk.log.slice(-3));
  await padPress(1);
  await P.secs(0.8);
  s = await P.screen();
  t.ok(!s.talk, 'the talk with June is finished by pad buttons only', s.talk);
  await padPress(8); await P.secs(0.4);
  s = await P.screen();
  if (!/never saw June/i.test(s.ledger)) { for (let k = 0; k < 5 && !/never saw June/i.test(s.ledger); k++) { await padPress(5); await P.secs(0.3); s = await P.screen(); } }
  t.ok(/never saw June/i.test(s.ledger), 'the promise is on the Ledger page he opens (by pad)', s.ledger.slice(0, 500));
  await padPress(8); await P.secs(0.4);
  await P.world(() => { window.__S.pad = null; });
  await P.tap('KeyN'); await P.secs(0.3); // back on the keys

  // ---- 6. Mickey's office: the door, Sheila's walk-round at the things themselves, the stair, the yard door ----
  const cam = await P.world(() => {
    // every sixth frame: is the camera inside a wall, and are his feet in the frame? (kept by the page, read at the end)
    const S = window.__S, T3 = LEDGER.THREE, v = new T3.Vector3();
    S.cam = { n: 0, wall: 0, feetOut: 0, where: [], feet: [] };
    // and where Sheila stands at the moment each of her lines first shows
    S.sheila = [];
    S.eachs.sheila = () => { for (const e of document.querySelectorAll('#subs .s')) { const s = e.innerText.trim(); if (/^SHEILA DUNN[A-Z]/.test(s) && !S.sheila.some((x) => x.line === s)) { const Q = LEDGER.G.people.sheila, r = LEDGER.roomOf('mickeys'); S.sheila.push({ line: s, at: [Math.round((Q.x - r.ox) * 10) / 10, Math.round((Q.z - r.oz) * 10) / 10], moving: !!Q.moving }); } } };
    S.eachs.cam = () => {
      const G = LEDGER.G, t = G.tom, c = LEDGER.camera;
      if (S.frameNo % 6 || G.story.phase !== 'play' || G.paused || t.inCar) return;
      S.cam.n++;
      c.updateMatrixWorld(); c.matrixWorldInverse.copy(c.matrixWorld).invert();
      if (t.space === 'street') {
        const inside = LEDGER.cameraInside(); if (inside) { S.cam.wall++; if (S.cam.where.length < 5) S.cam.where.push([Math.round(c.position.x * 10) / 10, Math.round(c.position.z * 10) / 10, inside]); }
        v.set(t.x, t.y || 0, t.z).project(c);
        if (Math.abs(v.x) > 1 || Math.abs(v.y) > 1 || v.z > 1) { S.cam.feetOut++; if (S.cam.feet.length < 5) S.cam.feet.push([Math.round(t.x * 10) / 10, Math.round(t.z * 10) / 10, Math.round(v.x * 100) / 100, Math.round(v.y * 100) / 100]); }
      } else {
        const r = LEDGER.rules && Object.values(LEDGER.G.env && LEDGER.G.env.rooms || {}).find((q) => q.id === t.space);
        const R = r || (LEDGER.roomOf ? LEDGER.roomOf(t.space) : null);
        if (R && c.position.z - R.oz <= R.d / 2 && (Math.abs(c.position.x - R.ox) > R.w / 2 + 0.05 || c.position.z - R.oz < -R.d / 2 - 0.05)) { S.cam.wall++; if (S.cam.where.length < 5) S.cam.where.push([Math.round((c.position.x - R.ox) * 10) / 10, Math.round((c.position.z - R.oz) * 10) / 10, t.space]); }
      }
    };
    return true;
  });
  await go(6.2, 36, { near: 0.6 });
  await P.face(7.2, 36);
  await P.secs(0.4);
  s = await P.screen();
  t.ok(s.prompts.some((p) => /Mickey/.test(p)), "the prompt names Mickey's door", s.prompts);
  let stop = await P.played();
  await P.use(/Mickey/);
  await P.until(() => LEDGER.G.tom.space === 'mickeys' && !LEDGER.G.paused, 6);
  t.ok((await P.tom()).space === 'mickeys' && (await P.played()) - stop < 5, 'the door opens with the use key and he walks in, no stop over 5 real seconds', await P.tom());
  // follow Sheila: she walks to each thing and says its line there
  const lines = [];
  const things = await P.world(() => LEDGER.game.hour1.round.map((r) => r.thing));
  for (let i = 0; i < 6; i++) {
    let got = null;
    for (let k = 0; k < 60 && !got; k++) {
      const sh = await P.world(() => { const S = LEDGER.G.people.sheila, r = LEDGER.roomOf('mickeys'); return { x: S.x, z: S.z, moving: !!S.moving, lx: S.x - r.ox, lz: S.z - r.oz }; });
      const me = await P.tom();
      if (Math.hypot(me.x - sh.x, me.z - sh.z) > 2.0) await P.walkTo(sh.x, sh.z, { maxSecs: 1.5, near: 1.7 });
      else await P.secs(0.3);
      const subs = await subsNow(P);
      const line = subs.find((x) => /^SHEILA DUNN[A-Z]/.test(x) && !/^SHEILA DUNN"/.test(x) && !lines.some((l) => l.line === x));
      if (line) got = { line, at: [Math.round(sh.lx * 10) / 10, Math.round(sh.lz * 10) / 10], moving: sh.moving };
    }
    if (!got) break;
    lines.push(got);
    await P.secs(1.5);
  }
  const want = await P.world(() => LEDGER.game.hour1.round.map((r) => r.at));
  const told = await P.world(() => window.__S.sheila);
  for (const l of lines) { const m = told.find((x) => x.line === l.line); if (m) { l.at = m.at; l.moving = m.moving; } }
  t.ok(lines.length === 6, 'Sheila says her six lines', { lines: lines.map((l) => l.line.slice(0, 40)), diag: await P.world(() => { const S = LEDGER.G.people.sheila; return [LEDGER.game.hour1.x().round, S.space, Math.round(S.x), Math.round(S.z), !!S.gone, !!S.busy, S.override, LEDGER.G.t, LEDGER.G.tom.x, LEDGER.G.tom.z]; }) });
  t.ok(lines.length === 6 && lines.every((l, i) => Math.hypot(l.at[0] - want[i][0], l.at[1] - want[i][1]) < 0.7 && !l.moving), 'each line is said standing at the thing it is about (' + things.join(', ') + ')', lines.map((l) => l.at));
  t.ok(new Set(lines.map((l) => l.at.join())).size === 6, 'she walks with him from thing to thing', lines.map((l) => l.at));
  t.ok(lines.every((l) => !/Tom|Nowak/.test(l.line)), 'she does not use his name', 0);
  const pl = await P.until(() => [...document.querySelectorAll('#subs .s')].some((e) => /PAULINE/i.test(e.textContent) && /no car/.test(e.textContent)), 12);
  t.ok(pl >= 0, 'Pauline at the radio has a fare and no car', await subsNow(P));
  t.note('the walk-round', lines.map((l) => l.line));
  // the stair to the flat and back, then out by the yard door and in again
  const stair = await P.world(() => { const r = LEDGER.roomOf('mickeys'), st = LEDGER.roomOf('flat').stair; return [r.ox + st[0] - 0.5, r.oz + st[1] - 0.4]; });
  await go(stair[0], stair[1], { near: 0.5 });
  await P.secs(0.4);
  s = await P.screen();
  t.ok(s.prompts.some((p) => /stair/.test(p)), 'the stair has a prompt that names it', s.prompts);
  stop = await P.played();
  await P.use(/stair/);
  await P.until(() => LEDGER.G.tom.space === 'flat' && !LEDGER.G.paused, 6);
  t.ok((await P.tom()).space === 'flat' && (await P.played()) - stop < 5, 'the stair is climbed to the flat with no stop over 5 real seconds', await P.tom());
  await P.secs(1);
  s = await P.screen();
  t.ok(s.prompts.some((p) => /stair/i.test(p)), 'the way back down has a prompt', s.prompts);
  await P.use(/stair/);
  await P.until(() => LEDGER.G.tom.space === 'mickeys' && !LEDGER.G.paused, 6);
  const yd = await P.world(() => { const r = LEDGER.roomOf('mickeys'); return [r.ox + r.exit2.mat[0], r.oz + r.exit2.mat[1]]; });
  await go(yd[0], yd[1], { near: 0.8 });
  await P.secs(0.4);
  s = await P.screen();
  t.ok(s.prompts.some((p) => /yard/.test(p)), 'the yard door has a prompt that names it', s.prompts);
  await P.use(/yard/);
  await P.until(() => LEDGER.G.tom.space === 'street', 6);
  await P.secs(1);
  s = await P.screen();
  t.ok((await P.tom()).space === 'street' && s.prompts.some((p) => /Mickey/.test(p)), "out in the yard the back door of Mickey's has its prompt", s.prompts);
  await P.use(/Mickey/);
  await P.until(() => LEDGER.G.tom.space === 'mickeys', 6);
  t.ok((await P.tom()).space === 'mickeys', 'and back in by the yard door', await P.tom());
  const camSeen = await P.world(() => window.__S.cam);
  t.ok(camSeen.n > 200 && camSeen.wall === 0, 'the camera never shows the inside of a wall, on the street, in the office or on the stair', camSeen);
  t.ok(camSeen.feetOut === 0, 'the camera keeps his feet in frame on the street', camSeen);

  // ---- the save this story leaves: at the radio, made by the game (Save on the pause menu) ----
  const rd = await P.world(() => { const r = LEDGER.roomOf('mickeys'); return [r.ox - 2.4, r.oz - 0.9]; });
  await go(rd[0], rd[1], { near: 0.8 });
  await P.tap('Escape'); await P.secs(0.3);
  await P.click('[data-act="save"]'); await P.secs(0.5);
  s = await P.screen();
  t.ok(/Saved/.test(s.book), 'Save on the pause menu saves, and says so', s.book.slice(-80));
  await P.tap('Escape'); await P.secs(0.3);
  await P.keep(n === 1 ? 'S01' : 'S01-run2');
  t.note('the Ledger after the first minutes', await P.world(() => LEDGER.G.ledger.notes.map((x) => x.text || x.t || x)));
});
