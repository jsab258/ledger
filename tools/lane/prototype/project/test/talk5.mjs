// The lane's round 5 (18 Nov): talk that does not repeat across talks and people, small talk that answers the question,
// and a debtor who stands (Lee, courted by Cammack's lads). Part one runs the written lines in Node; part two plays the
// built page for Lee's ladder.
import { launch } from './harness.mjs';
import { G } from '../src/state.js';
import { fb, fbReset, FBQ, FB, FBT, streetOf, topicOf } from '../src/talk_lines.js';
import { RULES } from '../src/rules.js';

let bad = 0;
const ok = (cond, what) => {
  console.log((cond ? 'ok   ' : 'FAIL ') + what);
  if (!cond) bad++;
};
const D = 1440;
const person = (id, name, sex = 'm', z = 0) => ({ id, def: { name, sex }, space: 'street', x: 0, z });
G.story = {}; // an older save's story: nothing heard yet
G.t = D + 9.5 * 60;
const ron = person('ron', 'Ron Kirby'),
  pauline = person('pauline', 'Pauline Kitching', 'f'),
  brenda = person('brenda', 'Brenda Laverack', 'f'),
  grace = person('grace', 'Grace Rinaldi', 'f'),
  walsh = person('walsh', 'Father Walsh'),
  wayneCopper = person('wayne', 'Wayne Harrison', 'm', -150);

// Ron's own line: once a day, across talks
const talk = (P, key, text, n = 4) => {
  fbReset();
  const out = [];
  for (let k = 0; k < n && !FBT.closed; k++) out.push(fb(P, key, text));
  return out;
};
const dock = (xs) => xs.filter((x) => x.startsWith('Thirty years on the dock')).length;
const t1 = talk(ron, 'small'),
  t2 = talk(ron, 'small');
ok(dock(t1) === 1 && dock(t2) === 0, "Ron's dock line once a day across talks: " + JSON.stringify([t1, t2]));
G.t += D;
ok(dock(talk(ron, 'small')) === 1, '... and again the next day');

// a shared line: once a week on each street, whoever says it first
G.t = 10 * D + 15 * 60;
G.story.heard = { own: {}, st: {} };
const p1 = talk(pauline, 'small'),
  sharedSaid = p1.filter((x) => FB.small.includes(x));
ok(sharedSaid.length === 1, 'Pauline gives one shared small-talk line: ' + JSON.stringify(p1));
G.t += 2 * D;
const b1 = talk(brenda, 'small');
ok(!b1.includes(sharedSaid[0]), 'two days on, Brenda on the same street does not repeat it: ' + JSON.stringify(b1));
const onCopper = () => Object.assign(G.tom, { space: 'street', z: -150 }),
  onHook = () => Object.assign(G.tom, { space: 'street', z: 0 });
onCopper();
const sc = streetOf(wayneCopper);
onHook();
ok(sc === 'Copper Row' && streetOf(brenda) === 'the Hook', 'Copper Row and the Hook are two streets (where Tom stands)');
G.tom.space = 'mickeys';
G.tom.z = -500;
ok(streetOf(pauline) === 'the Hook', "inside Mickey's the street is the one its door lets out on");
onHook();
// every shared small-talk line said on the Hook today: nobody there has one left, but over the bridge they are free
G.story.heard.st = { 'the Hook': Object.fromEntries(FB.small.map((x) => [x, Math.floor(G.t / D)])) };
const b2 = talk(brenda, 'small');
onCopper();
const w1 = talk(wayneCopper, 'small');
onHook();
ok(!b2.some((x) => FB.small.includes(x)), 'on the Hook the shared lines are spent: ' + JSON.stringify(b2));
ok(w1.some((x) => FB.small.includes(x)), 'over the bridge Copper Row keeps its own count: ' + JSON.stringify(w1));
// across a whole week of talks on the Hook, no shared line is heard twice
G.t = 20 * D + 10 * 60;
G.story.heard = { own: {}, st: {} };
const cast = ['pauline', 'brenda', 'kevin', 'terry', 'lily', 'rita', 'sylvia', 'dennis', 'albert', 'nora'].map((id) =>
  person(id, id[0].toUpperCase() + id.slice(1)),
);
const heardShared = [];
const qs = ["I'm still finding my feet here.", 'Do you get many strangers down here?', "Where's good for a cup of tea round here?", 'What do people do round here of a Sunday?'];
for (let d = 0; d < 6; d++) {
  for (const P of cast) {
    fbReset();
    for (const q of qs) {
      if (FBT.closed) break;
      const x = fb(P, 'small', q);
      if (FB.small.includes(x) || Object.values(FBQ).flat().includes(x)) heardShared.push(x);
    }
  }
  G.t += D;
}
ok(new Set(heardShared).size === heardShared.length, `a week on the Hook: ${heardShared.length} shared lines, none twice`);

// small talk answers the question asked
G.t = 40 * D + 11 * 60;
G.story.heard = { own: {}, st: {} };
ok(topicOf("Where's good for a cup of tea round here?") === 'tea', 'the tea question is read as tea');
fbReset();
const tea = fb(brenda, 'small', "Where's good for a cup of tea round here?");
ok(FBQ.tea.includes(tea), 'Brenda answers the tea question about tea: ' + tea);
fbReset();
const rt = fb(ron, 'small', "Where's good for a cup of tea round here?");
ok(/Grace/.test(rt), 'Ron answers it in his own words: ' + rt);
G.story.heard = { own: {}, st: {} };
fbReset();
const gt = fb(grace, 'small', "Where's good for a cup of tea round here?");
ok(!/Grace/.test(gt), 'Grace never recommends herself by name: ' + gt);
fbReset();
const ws = fb(walsh, 'small', 'What do people do round here of a Sunday?');
ok(!/Walsh/.test(ws), 'nor the priest: ' + ws);
fbReset();
ok(!FBQ.tea.includes(fb(brenda, 'nothing', "Where's good for a cup of tea round here?")), 'a non-small-talk answer is not turned into a topic');
// the question is answered before ordinary small talk, even by people with their own small talk (the review's fault)
G.story.heard = { own: {}, st: {} };
fbReset();
const rs = fb(ron, 'small', 'What do people do round here of a Sunday?');
ok(FBQ.sunday.includes(rs), 'Ron answers the Sunday question, not with his dock line: ' + rs);
// a second question in the same talk is answered in his own words (the street's stock is one line a talk)
const r2 = fb(ron, 'small', 'Do you get many strangers down here?');
ok(/suitcase/.test(r2), 'and the strangers question after it, in his own words: ' + r2);
// the working replies keep a day's rule: a refusal never closes a talk because the street used it last week
G.story.heard = { own: {}, st: {} };
const okLines = [];
for (let d = 0; d < 3; d++) {
  for (const P of cast.slice(0, 3)) {
    fbReset();
    okLines.push(fb(P, 'ok'));
  }
  G.t += D;
}
ok(okLines.filter((x) => FB.ok.includes(x)).length >= 3, 'agreeing replies come back day after day: ' + JSON.stringify(okLines));
const ellis = person('ellis', 'DS Carol Ellis', 'f');
fbReset();
ok(!FBQ.lived.includes(fb(ellis, 'small', 'Have you always lived round here?')), 'the detective never claims a lifetime on the street');

// saved with the week
const json = JSON.stringify(G.story);
ok(JSON.parse(json).heard && Object.keys(JSON.parse(json).heard.st).length >= 1, 'what was said is saved with the story');
ok(RULES.talk.sharedLineAgainOnStreetAfterDays === 7 && RULES.talk.ownLineAgainAfterDays === 1, 'the rules table holds the day counts');

// ---------- the page: Lee stands when fronted up (Cammack's lads behind him), and it comes to blows at the shove
const h = await launch({ port: 8799, quality: 'low' });
try {
  await h.newWeek();
  const lee = (backed) =>
    h.ev((backed) => {
      const G = LEDGER.G, t = G.tom, F = LEDGER.F;
      if (F.on) LEDGER.fight.end();
      for (const Q of G.named.concat(G.crowd)) Q.space = 'elsewhere';
      const P = G.named.find((p) => p.id === 'lee');
      t.space = 'street'; t.hurt = 0; t.weapon = null; t.armed = false;
      P.space = 'street'; P.down = false; P.hurt = 0; P.gone = false; P.mind.fear = 0; P.mind.mem = [];
      P.x = t.x + Math.sin(t.ang) * 1.2; P.z = t.z + Math.cos(t.ang) * 1.2;
      P.def.backed = backed;
      LEDGER.fight.frontUp(P, null);
      const rungs = [];
      for (let i = 0; i < 4 && F.on && F.rung < 4 && !F.yielded; i++) {
        LEDGER.fight.climb();
        rungs.push({ rung: F.rung, yielded: !!F.yielded, why: F.standWhy || '' });
      }
      const out = { rungs, fight: F.foes.length > 0, last: F.last };
      LEDGER.fight.end();
      P.def.backed = 1;
      return out;
    }, backed);
  const a = await lee(1);
  ok(a.rungs.some((r) => r.why === 'backed') && !a.rungs.some((r) => r.yielded), "Lee stands, and says Cammack's lot are behind him: " + JSON.stringify(a.rungs));
  ok(a.fight, 'at the shove it comes to blows');
  const b = await lee(0);
  ok(b.rungs.some((r) => r.yielded), 'control: without the backing Lee gives way: ' + JSON.stringify(b.rungs));
} finally {
  await h.close();
}
console.log(bad ? `talk5: ${bad} FAIL` : 'PASS');
process.exit(bad ? 1 : 0);
