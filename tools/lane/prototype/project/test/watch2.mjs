// The lane's round 2 (18 Nov): the carry under watch. A constable walks his beat between the pick-up and the
// drop; he sees with the town's own eyes; seen with the bag he calls out; standing is a search (the bag is
// taken), running is a chase he gives up when Tom is out of his sight long enough. Plus the evening to-do that
// sends a newcomer to Ron for the first night's offer.
import fs from 'fs';
import { launch } from './harness.mjs';

let bad = 0;
const ok = (cond, what) => {
  console.log((cond ? 'ok   ' : 'FAIL ') + what);
  if (!cond) bad++;
};

const sc = fs.readFileSync('src/scenes.js', 'utf8');
ok(/Ron Kirby is waiting at the cab rank/.test(sc) && /ask1obj/.test(sc), 'the evening to-do names Ron at the rank once the first offer is due');

let h = await launch({ port: 8798, quality: 'low' });
let errs = [];
// take the Monday bag at 23:00 on Monday; returns where the constable stands and how
const takeBag = () =>
  h.ev(() => {
    const G = LEDGER.G;
    G.t = 23 * 60;
    G.story.flags.ask1 = 'yes';
    G.story.job = { n: 1, st: 'pickup', day: 0 };
    LEDGER.job.goToPickUp();
    const p = LEDGER.prompts().find((x) => /holdall/.test(x.text));
    if (!p) return { prompt: false, prompts: LEDGER.prompts().map((x) => x.text) };
    LEDGER.press(p.key);
    return { prompt: true, job: LEDGER.job.read() };
  });
// put Tom d metres in front of the constable (on his line of sight), or behind him
const place = (d, behind) =>
  h.ev(
    ([d, behind]) => {
      const G = LEDGER.G,
        P = G.people.pc,
        t = G.tom;
      P.route = null;
      P.moving = false;
      const a = P.ang + (behind ? Math.PI : 0);
      t.x = P.x + Math.sin(a) * d;
      t.z = P.z + Math.cos(a) * d;
      t.ang = a;
      return { tom: [t.x, t.z], pc: [P.x, P.z] };
    },
    [d, behind],
  );
const stepFor = (secs) =>
  h.ev(async (secs) => {
    for (let k = 0; k < secs * 4; k++) LEDGER.step(0.25);
    return LEDGER.job.read();
  }, secs);
try {
  // 1. the beat starts at the pick-up
  await h.newWeek();
  const a = await takeBag();
  ok(a.prompt && a.job.state === 'carrying' && a.job.watch && a.job.watch.state === 'beat', 'taking the bag starts the constable\'s beat: ' + JSON.stringify(a.job && a.job.watch));
  // 2. behind him in the dark, eight metres: not seen
  await place(8, true);
  const b = await stepFor(1);
  ok(b.watch.state === 'beat', 'eight metres behind him he does not see Tom: ' + b.watch.state);
  // 3. in front, 1.5 m, standing still: called out to, then searched; the bag is taken
  await place(1.5, false);
  const c1 = await stepFor(0.5);
  ok(c1.watch.state === 'challenge' || c1.watch.state === 'over', 'in front of him he calls out: ' + c1.watch.state);
  const c2 = await stepFor(2);
  const c3 = await h.ev(() => ({
    flag: LEDGER.G.story.flags.job1,
    carry: LEDGER.G.tom.carry,
    taken: (LEDGER.G.events || []).some((e) => e.kind === 'bag_taken'),
  }));
  ok(c2.state === 'lost' && c2.watch.how === 'searched' && c3.flag === 'lost' && !c3.carry && c3.taken, 'standing still he searches and takes the bag: ' + JSON.stringify([c2.state, c2.watch.how, c3]));
  // 4. a fresh page and week: called out to, Tom runs out of his sight; he gives up and Tom keeps the bag
  errs = errs.concat(h.errors);
  await h.close();
  h = await launch({ port: 8799, quality: 'low' });
  await h.newWeek();
  await takeBag();
  // in the dark he sees about four metres (the town's own eyes); three metres in front he calls out
  await place(3, false);
  const d1 = await stepFor(0.5);
  ok(d1.watch.state === 'challenge', 'three metres in front he calls out: ' + d1.watch.state);
  const d2 = await h.ev(() => {
    const G = LEDGER.G,
      P = G.people.pc,
      t = G.tom;
    // away and round a corner: somewhere he cannot see from where he stands, 30 to 60 m off
    for (let r = 30; r <= 60; r += 5)
      for (let k = 0; k < 24; k++) {
        const x = P.x + Math.sin(k / 4) * r,
          z = P.z + Math.cos(k / 4) * r;
        if (!G.env.los(P.x, P.z, x, z)) {
          LEDGER.goTo({ xMetres: x, zMetres: z });
          return { x, z, r };
        }
      }
    return null;
  });
  ok(!!d2, 'found a spot out of his sight: ' + JSON.stringify(d2));
  const d3 = await stepFor(1);
  ok(d3.watch.state === 'chase', 'Tom gone from where he stood: a chase: ' + d3.watch.state);
  // keep Tom out of sight (he stays put; the constable walks to where he last saw him)
  const d4 = await stepFor(10);
  const d5 = await h.ev(() => ({ ran: LEDGER.G.story.flags.ranBeat, carry: LEDGER.G.tom.carry }));
  ok(
    (d4.state === 'carrying' && d4.watch.how === 'lost him' && d5.ran === 1 && d5.carry === 'bag') ||
      (d4.state === 'lost' && d4.watch.how === 'caught running'),
    'the chase ends: lost him (still carrying) or caught: ' + JSON.stringify([d4.state, d4.watch, d5]),
  );
  // 5. the drop still works after an escape
  if (d4.state === 'carrying') {
    await h.ev(() => LEDGER.job.goToDrop());
    const p = await h.ev(() => LEDGER.prompts().map((x) => x.text));
    ok(p.includes('Knock'), 'after the escape the drop still takes the bag: ' + JSON.stringify(p));
  }
  errs = errs.concat(h.errors);
  ok(errs.length === 0, 'no page errors' + (errs.length ? ': ' + errs.join(' | ') : ''));
} finally {
  await h.close();
}
console.log(bad ? `FAIL: ${bad} of the round's checks` : 'PASS');
process.exit(bad ? 1 : 0);
