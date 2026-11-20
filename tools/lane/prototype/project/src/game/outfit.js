// LEDGER, the whole game: the system "outfit". The old firm's claim on him (ONE-SHOT-PROMPT 4 at 7:00, 14, 36; stories
// S04 on): after dark Ron brings the first ask in person at the office, a dark coat and an envelope for the ferry
// landing after ten. Yes, no (asked twice), or stay away: staying away, Ron leaves the envelope with Sheila's word and
// the ask ends unanswered. Getting ready is done with the hands: the coat from its hook, two things under it, the rest
// in the locked drawer. The carry itself is game/carry.js.
import { register, X, write, P_, dayNow, hourNow } from './core.js';
import { G } from '../state.js';
import { sub, ui, say, scene } from '../ui.js';
import { RULES } from '../rules.js';
import { ROOMS, roomPos } from '../map.js';
import { hyp, angDiff } from '../util.js';
import { decision } from '../talk.js';
import { stopWaiting } from '../player.js';
import { take, has } from './crime.js';
import { walkInOffice } from './hour1.js';
import { carriedWords } from './ledgerx.js';

const T = RULES.game.outfit;
const fl = () => G.story.flags;
const dark = () => hourNow() >= T.ronComesFromHour || hourNow() < 5;
export const LANDING_WORDS = 'the ferry landing, the shelter under the last lamp past the Harbour Office clock';

const KEEP = ['What is in the envelope?', 'Who are they, Ron?'];
const SPEC = () => ({
  leaveIdx: 2,
  ask: 'whether he will take the envelope to the ferry landing tonight',
  keep: KEEP,
  keepSay: "You don't ask, boss. Mickey never asked. It's an envelope and a walk. Do I tell them it's still on?",
  opts: [
    {
      agree: 1,
      say: ["I'll take it. Tell them it's on.", "All right. I'll walk it down."],
      q: "You'll take it? Once I tell them it's on, it's on.",
      yes: ["Yes. Tell them it's on.", "Yes. I'll take it."],
      no: ['No. Hold off a minute.', "No. I'll think on it."],
      keep: KEEP,
      keepSay: "Mickey took it every Monday for nine years. So. You'll take it?",
    },
    {
      refuse: 1,
      say: ["Tell them no. I'm not doing it.", "I'm not carrying it. Count me out."],
      q: 'You want me to tell them no?',
      q2: "They count a no, boss. Mickey never gave them one. No, for certain?",
      yes: ['Yes. Tell them no.', "Yes. I'm sure."],
      no: ['No. Hold off a minute.', "No. I'll think on it."],
      keep: KEEP,
      keepSay: 'Nine years and never a no out of this office. You want me to tell them no?',
    },
  ],
});
async function ask() {
  const x = X('outfit'),
    R = P_('ron');
  x.asking = true;
  try {
    await scene(async () => {
      if (!x.put) {
        await say('ron', "Boss. Got a minute? It's a thing of Mickey's that didn't die with him.");
        await say('ron', "An envelope goes down to the ferry landing of a Monday night, after ten. A man waits by the shelter under the last lamp, past the Harbour Office clock. Mickey walked it every week for nine years, in that dark coat on the hook.");
        x.put = Math.round(G.t);
        write("Ron Kirby's ask, from the men behind the landing: an envelope to the ferry landing, the shelter under the last lamp, after ten.", { key: 'ask1-put', who: 'ron', how: 'Ron says' });
      }
      const i = await decision('ron', x.ask1 === 'put' ? "They'll want an answer, boss. Do I tell them it's still on?" : "So. Do I tell them it's still on?", SPEC());
      if (i === 0) {
        x.ask1 = 'yes';
        x.takenT = Math.round(G.t);
        fl().ask1 = 'yes';
        G.tom.carry = 'envelope';
        await say('ron', "Then it's on. Here. Don't open it. The coat's on the hook in the back room: it goes on before you go out, and that goes under it.");
        await say('ron', "The landing's open from ten till one. Three ways down and you'll see them yourself: the quay under the lamps, the yard and the lane behind the warehouses, or the cab. The constable walks the quay.");
        write('Said yes to Ron Kirby. The envelope is in his hand, for ' + LANDING_WORDS + ', between ten and one.', { key: 'ask1-yes', who: 'ron', how: 'He did it' });
      } else if (i === 1) {
        x.ask1 = 'no';
        fl().ask1 = 'no';
        await say('ron', "Then I tell them no. First no that office has given them in nine years. They'll count it, boss.");
        write('Said no to Ron Kirby, and no again when he asked twice. The envelope does not go to the landing tonight by his hand.', { key: 'ask1-no', who: 'ron', how: 'He did it' });
      } else {
        x.ask1 = 'put';
        x.leftT = Math.round(G.t);
        await say('ron', "Think quick, boss. I'll be on the rank. They want it at the landing after ten, whoever takes it.");
      }
    });
  } finally {
    x.asking = false;
    // Ron goes back out to the rank
    if (R) {
      R.busy = false;
      R.space = 'street';
      R.x = ROOMS.mickeys.street[0] - 0.8;
      R.z = ROOMS.mickeys.street[1] + 1.6;
      R.goalKey = null;
    }
  }
}
// Ron comes in off the rank and walks up to him
function ronComes(x, dt) {
  const t = G.tom,
    R = P_('ron');
  if (!R || R.dead) return;
  if (!x.coming || R.space !== 'mickeys') {
    x.coming = Math.round(G.t);
    R.busy = true;
    R.gone = false;
    R.awake = true;
    R.space = 'mickeys';
    [R.x, R.z] = roomPos('mickeys', ROOMS.mickeys.mat[0], ROOMS.mickeys.mat[1] - 0.6);
    stopWaiting(); // a wait always stops for a man at the door
    if (G.hooks.sfx) G.hooks.sfx('door');
  }
  const r = ROOMS.mickeys,
    lx = t.x - r.ox,
    lz = t.z - r.oz,
    d = hyp(R.x, R.z, t.x, t.z);
  if (d > T.ronStandsAtMetres + 0.3) {
    const k = (d - T.ronStandsAtMetres) / d;
    walkInOffice(R, [R.x - r.ox + (lx - (R.x - r.ox)) * k, R.z - r.oz + (lz - (R.z - r.oz)) * k], dt);
    return;
  }
  R.moving = false;
  R.ang += angDiff(R.ang, Math.atan2(t.x - R.x, t.z - R.z)) * Math.min(1, dt * 6);
  if (!ui.modal && !x.asking) ask();
}

register({
  id: 'outfit',
  fresh: () => ({ ask1: null, put: 0, coming: 0, soughtT: 0, leftT: 0, takenT: 0, told: false, seeded: false, crowbar: 'nail' }),
  loaded(x) {
    fl().ask1 = fl().ask1 || 'outfit'; // the first ask is this system's: the older bag run is never offered
    if (!x.seeded) {
      x.seeded = true;
      const c = G.x.crime;
      if (c && !c.stored.some((s) => s.id === 'cosh')) c.stored.push({ id: 'cosh', name: 'a cosh', unlawful: true }); // Mickey's, in his drawer
    }
    const R = P_('ron');
    if (R && x.asking) x.asking = false;
    G.hooks.closedWhy = (key) => (key === 'carry1' ? { done: 'Handed over at the landing', police: 'Taken by the constable', late: 'The landing shut' }[X('outfit').envelope] || 'Over' : key === 'carrying' ? 'Put down' : null);
    G.hooks.openRows2 = (o) => {
      const t = G.tom,
        y = X('outfit');
      if (y.ask1 === 'yes' && !y.envelope) o.push({ key: 'carry1', who: 'ron', what: 'The envelope, to ' + LANDING_WORDS, day: 'Tonight, ten till one', how: 'Ron says' });
      if (y.ask1 === 'put') o.push({ key: 'ask1', who: 'ron', what: 'Ron Kirby wants an answer: the envelope for the ferry landing. He is on the rank', day: 'Tonight', how: 'Ron says' });
      if (t.carry || (G.x.crime && G.x.crime.pockets.length)) o.push({ key: 'carrying', who: null, what: 'He carries ' + carriedWords(), how: 'His own pockets' });
    };
  },
  step(dt) {
    if (G.paused || G.story.phase !== 'play') return;
    const x = X('outfit'),
      t = G.tom,
      book = X('book');
    // 7:00 after dark, once Sheila has shown him the debt book, Ron brings the ask in person at the office
    // (the debt book first: he comes once Darren's twenty-two pounds has been dealt with one way or another, or a while
    // after the book was shown)
    const due = book.shown && (book.darren || G.t - book.shown > T.ronComesAfterTheBookGameMinutes);
    if (dayNow() <= 1 && (dayNow() === 0 ? dark() : hourNow() < T.landingShutsHour) && due && (x.ask1 === null || x.ask1 === 'put')) {
      if (t.space === 'mickeys' && !x.asking && x.ask1 === null) ronComes(x, dt);
      else if (t.space !== 'mickeys') {
        // he has gone out before Ron reached him: Ron goes back to the rank and comes in again when he is back
        const R = P_('ron');
        if (R && x.coming && !x.put && R.busy && R.space === 'mickeys') {
          R.busy = false;
          R.space = 'street';
          R.x = ROOMS.mickeys.street[0] - 0.8;
          R.z = ROOMS.mickeys.street[1] + 1.6;
          R.goalKey = null;
          x.coming = 0;
        }
        // he is not there: Ron waits on the rank; after long enough the ask ends unanswered
        if (!x.soughtT) x.soughtT = G.t;
        if (G.t - Math.max(x.soughtT, x.leftT || 0) > T.ronWaitsForAnAnswerGameMinutes && (x.ask1 === 'put' || x.coming === 0)) {
          x.ask1 = 'left';
          x.envelope = 'sheila';
          const c = G.x.crime;
          if (c) c.stored.push({ id: 'envelope', name: 'the envelope', unlawful: true });
        }
      } else x.soughtT = 0;
    }
    // staying away: Ron left the envelope with Sheila's word; he learns it when he is next in the office
    if (x.ask1 === 'left' && !x.told && t.space === 'mickeys' && !ui.modal) {
      x.told = true;
      const S = P_('sheila'),
        here = S && S.space === 'mickeys' && !S.gone;
      if (here) sub("Ron was in with something for the landing and you were not here. He has left it in my drawer. I have said nothing and I know nothing.", 'Sheila Dunn', 'face', 8);
      else sub("A note on the counter, in Sheila's hand: Ron came. You were out. It is in the drawer. I know nothing about it. S.D.", '', 'over', 8);
      write("Ron's ask for the landing went unanswered: he was out. Ron left the envelope with Sheila; it is in the drawer.", { key: 'ask1-left', who: 'ron', how: here ? 'Sheila says' : "Sheila's note" });
    }
  },
  beatFor(P) {
    const x = X('outfit');
    if (P.id === 'ron' && x.ask1 === 'put' && !x.asking) return () => ask(); // he answers Ron on the rank
    return null;
  },
  hotspots(out) {
    const t = G.tom,
      x = X('outfit');
    if (t.carry === 'envelope' && !t.inCar)
      out.push({
        k: 'T',
        t: 'Put the envelope under the coat',
        run: () => {
          if (!t.coat) return sub('Nowhere to hide it: the dark coat is not on him.', '', 'over', 4);
          if (take('envelope')) {
            t.carry = null;
            sub('The envelope goes under the coat, flat against his ribs.', '', 'over', 3.5);
          }
        },
      });
    if (t.space === 'mickeys' && x.ask1 === 'yes' && !t.hasCoat && !out.some((o) => /dark coat/.test(o.t))) {
      const [hx, hz] = roomPos('mickeys', 1.1, -3.2);
      if (hyp(t.x, t.z, hx, hz) < 1.5)
        out.push({
          k: 'E',
          t: 'Take the dark coat from its hook',
          run: () => {
            t.hasCoat = true;
            sub("Mickey's dark coat, off its hook. C puts it on.", '', 'over', 4);
          },
        });
    }
    if (t.space === 'mickeys' && x.crowbar === 'nail') {
      const [nx, nz] = roomPos('mickeys', T.nailByTheYardDoor[0], T.nailByTheYardDoor[1]);
      if (hyp(t.x, t.z, nx, nz) < RULES.game.hour1.thingWithinMetres)
        out.push({
          k: 'T',
          t: 'Take the crowbar from the nail by the yard door',
          run: () => {
            if (take('crowbar')) {
              x.crowbar = 'taken';
              sub("Mickey's crowbar, off its nail. Under the coat with it.", '', 'over', 3.5);
            }
          },
        });
    }
  },
  hook: { x: () => X('outfit'), landingWords: LANDING_WORDS, has },
});
