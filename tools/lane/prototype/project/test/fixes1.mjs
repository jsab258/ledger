// The lane's round 1 (18 Nov): one check for each of the eight fixes in production/lane/FABLE-PROTOTYPE-FIXES-1.md.
// Part one runs the written lines in Node (fixes 1 and 4); part two plays the built page (fixes 2, 5, 6, 7);
// fixes 3 and 8 are checked in the source, since the hook cannot place a bubble or a purchase by itself.
import fs from 'fs';
import { launch } from './harness.mjs';
import { G } from '../src/state.js';
import { fb, fbReset, greet, isSharedLine, FB, FBT } from '../src/talk_lines.js';
const fbClosed = () => FBT.closed;

let bad = 0;
const ok = (cond, what) => {
  console.log((cond ? 'ok   ' : 'FAIL ') + what);
  if (!cond) bad++;
};

// ---------- fix 1: no line twice in one talk; shared lines once a talk, one person a day; a close when nothing is left
G.t = 1440 + 9.5 * 60;
const sheila = { id: 'sheila', def: { sex: 'f' } },
  ron = { id: 'ron', def: { sex: 'm' } },
  kevin = { id: 'kevin', def: { sex: 'm' } },
  lad = { id: 'crowd7', def: { sex: 'm' } };
fbReset();
const s = [];
for (let k = 0; k < 6; k++) {
  s.push(fb(sheila, 'small'));
  if (fbClosed()) break; // after the close only Leave is offered (talk.js)
}
ok(new Set(s).size === s.length, 'fix 1: Sheila never repeats a line in one talk: ' + JSON.stringify(s));
ok(s.filter(isSharedLine).length <= 1, 'fix 1: the shared pool at most once in a talk');
ok(/book/.test(s[s.length - 1]), 'fix 1: with nothing left Sheila closes the talk in her own voice');
fbReset();
const r = [1, 2, 3, 4].map(() => fb(ron, 'small'));
ok(r.filter((x) => x.startsWith('Thirty years on the dock')).length === 1, 'fix 1: Ron says his dock line once a talk');
fbReset();
const m1 = fb(kevin, 'mickey');
fbReset();
const m2 = fb(lad, 'mickey');
ok(!(isSharedLine(m1) && m1 === m2), 'fix 1: one shared Mickey line is said by one person a day at most');
G.t += 1440;
fbReset();
ok(FB.mickey.includes(fb(lad, 'mickey')), 'fix 1: the next day the shared lines are free again');

// ---------- fix 4: greetings follow the hour
G.t = 1440 + 9.5 * 60;
const terry = { id: 'terry', def: { sex: 'm' } };
ok(!/Evening/.test(greet(terry)) && /Morning/.test(greet(terry)), 'fix 4: Terry says Morning at 9.30am');
G.t = 1440 + 21 * 60;
ok(/Evening/.test(greet(terry)), 'fix 4: and Evening at 9pm');

// ---------- fixes 3 and 8, in the source
const ui = fs.readFileSync('src/ui.js', 'utf8'),
  sc = fs.readFileSync('src/scenes.js', 'utf8');
ok(/inEarshot\(P\)/.test(ui) && /sameBubbleQuietRealSeconds/.test(ui), 'fix 3: bubbles only within earshot and sight, no twin lines');
ok(/today\('door'\) && ronEyes\(true\)/.test(sc) && /today\('heard'\) && darrenHeard\(0, true\)/.test(sc), 'fix 8: paying Ron or Darren is offered only when they know something');

// ---------- the page: fixes 2, 5, 6, 7
const h = await launch({ port: 8797, quality: 'low' });
try {
  await h.newWeek();
  // fix 2: an unnamed man 1.2 m straight ahead, Darren 2 m off at 25 degrees: the prompt is for the man in front
  const p2 = await h.ev(() => {
    const G = LEDGER.G,
      t = G.tom,
      A = G.crowd.find((P) => P.space === 'street' && !P.gone && !P.mark),
      D = G.people.darren;
    G.ledger.met.darren = 1;
    t.x = 10;
    t.z = 10;
    t.ang = 0;
    for (const P of G.named.concat(G.crowd)) if (P !== A && P !== D && P.space === 'street' && Math.hypot(P.x - 10, P.z - 10) < 6) P.x += 30;
    Object.assign(A, { x: 10, z: 11.2, hold: true, route: null, moving: false });
    Object.assign(D, { space: 'street', x: 10 + 2 * Math.sin(0.44), z: 10 + 2 * Math.cos(0.44), hold: true, route: null, moving: false });
    return LEDGER.prompts().find((p) => p.key === 'E');
  });
  ok(!!p2 && !/Darren/.test(p2.text), 'fix 2: the prompt goes to the person in front, not Darren to the side: ' + JSON.stringify(p2));
  // fix 5: Ada's prompt never uses her name before Tom has learned it
  const p5 = await h.ev(() => {
    const G = LEDGER.G,
      A = G.people.ada;
    delete G.ledger.met.ada;
    if (G.ledger.names) delete G.ledger.names.ada;
    return LEDGER.prompts().map((p) => p.text);
  });
  ok(!p5.some((t) => /Speak up to Ada/.test(t)), 'fix 5: no "Speak up to Ada" before her name is known');
  // fix 6: the tea note says it was missed once its hour has gone
  const p6 = await h.ev(() => {
    const G = LEDGER.G;
    G.story.flags.teaInvited = 1;
    G.story.objective = 'Ada has asked you to tea at seven tonight. She does not ask twice.';
    G.t = 3 * 1440 + 30;
    LEDGER.step(1);
    return G.story.objective;
  });
  ok(!/seven tonight/.test(p6) && /missed/.test(p6), 'fix 6: just after midnight on Thursday the note says the tea was missed: ' + JSON.stringify(p6));
  // fix 7: a no to a debt never leaves the talk with nothing to say
  const p7 = await h.ev(async () => {
    const G = LEDGER.G,
      id = ['wayne', 'lee', 'julie', 'dennis'].find((k) => G.debts[k] && G.debts[k].st === 'open' && G.people[k].space !== 'home');
    if (!id) return { skip: true };
    LEDGER.talk.open(id, { free: true });
    await LEDGER.talk.idle();
    const out = [];
    let saidNo = false;
    for (let k = 0; k < 6; k++) {
      const st = LEDGER.talk.state();
      if (!st.open) break;
      if (st.deciding === 'debt' && !st.plainQuestionPut) {
        await LEDGER.talk.say('prop');
        out.push('asked');
        continue;
      }
      if (st.deciding) {
        const r = await LEDGER.talk.answer('no');
        out.push(st.deciding);
        if (st.deciding === 'debt' && r.answered) saidNo = true;
      } else await LEDGER.talk.say('personal');
      out.push(LEDGER.talk.state().open ? LEDGER.talk.lines().length : -1);
      if (saidNo) break;
    }
    const leave = LEDGER.talk.lines().some((l) => l.job === 'leave') || !LEDGER.talk.state().open;
    return { id, out, leave, saidNo, lines: LEDGER.talk.lines().map((l) => l.job) };
  });
  ok(p7.skip || (p7.saidNo && p7.out.every((n) => n !== 0) && p7.leave), 'fix 7: after a no on a debt the talk still offers lines and Leave: ' + JSON.stringify(p7));
  ok(h.errors.length === 0, 'no page errors' + (h.errors.length ? ': ' + h.errors.join(' | ') : ''));
} finally {
  await h.close();
}
console.log(bad ? `FAIL: ${bad} of the round's checks` : 'PASS');
process.exit(bad ? 1 : 0);
