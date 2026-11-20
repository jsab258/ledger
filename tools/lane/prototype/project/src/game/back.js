// LEDGER, the whole game: the system "back". It comes back (ONE-SHOT-PROMPT 2 "It comes back", the first hour at
// 13:00, story S06): what he did on the first carry is said to his face the next day by Darren, and only by the road
// it really travelled. A thing is known by the people who saw it. It passes when two of them stand together, heads
// together, in a place: the outfit's man goes to Ron at the rank in the morning, Ron walks over to Darren on the
// pavement, and Darren says it to Tom. Nobody who was not there knows without such a meeting, and the chain can be
// printed (the hook's chain()). Who knows shows in bodies: two heads together, a look held too long, a back turned.
import { register, X, P_, hourNow, dayNow, inView } from './core.js';
import { G } from '../state.js';
import { sub, ui } from '../ui.js';
import { RULES } from '../rules.js';
import { SPOTS } from '../map.js';
import { hyp } from '../util.js';
import { note } from '../ledger.js';
import { send, goToPoint } from '../routines.js';

const T = RULES.game.back;
const O = RULES.game.outfit;
const courier = () => G.people[O.landingManIs];
const nameOf = (id) => (id === O.landingManIs ? "the outfit's man" : G.people[id] ? G.people[id].def.name : id);
const clock = (t) => { const h = Math.floor((t % 1440) / 60), m = Math.floor(t % 60); return `${['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][Math.floor(t / 1440) % 7]} ${h}:${String(m).padStart(2, '0')}`; };

// Who can see Tom now: named people (not the police) and the outfit's man, on the street, awake, with a clear line.
// Under a lamp he is seen from far along the quay; in the dark only from close by.
function whoSees() {
  const t = G.tom,
    out = [];
  if (t.space !== 'street') return out;
  const M = courier();
  for (const P of G.named.concat(M ? [M] : [])) {
    if (!P || P.gone || P.dead || P.space !== 'street' || P.awake === false || (P.def && P.def.police)) continue;
    const d = hyp(P.x, P.z, t.x, t.z);
    if (d > (t.light > T.litAbove ? T.seenLitWithinMetres : T.seenDarkWithinMetres)) continue;
    if (G.env.los && !G.env.los(P.x, P.z, t.x, t.z)) continue;
    if (!out.includes(P.id)) out.push(P.id);
  }
  return out;
}
// Something has happened that the outfit's people will talk of. what: 'made' | 'missed' | 'searched' | 'ran'.
export function happened(what, saw) {
  const x = X('back');
  if (x.things.some((th) => th.what === what && dayNow() * 1440 - th.t < 1440 && G.t - th.t < 600)) return null;
  const th = { id: x.things.length + 1, what, t: Math.round(G.t), knows: {}, chain: [], saidBy: {}, looked: {} };
  for (const id of saw || whoSees()) th.knows[id] = { how: 'saw', t: th.t };
  x.things.push(th);
  return th;
}
// One tells the other, standing together: every thing the teller knows and the hearer does not.
function pass(A, B, place) {
  const x = X('back');
  let n = 0;
  for (const th of x.things) {
    if (!th.knows[A.id] || th.knows[B.id]) continue;
    th.knows[B.id] = { how: 'told', from: A.id, t: Math.round(G.t), at: place };
    th.chain.push({ a: A.id, b: B.id, t: Math.round(G.t), at: place });
    G.transfers.push({ a: A.id, b: B.id, e: 'back' + th.id, t: Math.round(G.t), z: place });
    n++;
  }
  if (n) {
    A.chat = { with: B.id, t: T.headsTogetherRealSeconds };
    B.chat = { with: A.id, t: T.headsTogetherRealSeconds };
    A.ang = Math.atan2(B.x - A.x, B.z - A.z);
    B.ang = Math.atan2(A.x - B.x, A.z - B.z);
    // if he is where he can see it, it goes in the Ledger as a guess: two heads together
    if (inView(A, T.headsSeenWithinMetres) && !B.anon && B.def) note(`${nameOf(A.id) === "the outfit's man" ? 'A man he half knows from the landing' : A.def.name} and ${B.def.name}, heads together ${place}. About last night, he guesses.`, 'note', 'heads-' + A.id + '-' + B.id + '-' + dayNow(), { who: B.id, how: 'Saw it', sure: 'a guess' });
  }
  return n;
}
const pending = (a, b) => X('back').things.some((th) => th.knows[a] && !th.knows[b]);
const together = (A, B, d) => A && B && !A.gone && !B.gone && A.space === 'street' && B.space === 'street' && hyp(A.x, A.z, B.x, B.z) < d;

// Keep a man at a spot while there is something for him to do there (sent again when the last sending has run out).
const keep = (P, where) => { if (!(P.override && P.override.where === where && G.t < P.override.until - 5)) send(P, where, 'idle', G.t + T.heldGameMinutes); };
// The morning's road: the outfit's man to Ron at the rank, Ron to Darren on the pavement. Each walks it.
function road(x) {
  const M = courier(),
    R = P_('ron'),
    D = P_('darren'),
    h = hourNow();
  if (!M || !R || !D) return;
  const due = x.things.some((th) => G.t - th.t > T.passesAfterGameMinutes) && h >= T.roadFromHour && h < T.roadUntilHour;
  if (!due) return;
  // (their overrides carry an end time: the first night's staging in game/book.js lets go only of its own, which have none)
  // Darren is about early too: he wants to hear how the night went
  if (x.things.some((th) => !th.knows.darren)) keep(D, 'pave');
  if (pending(M.id, 'ron')) {
    // Ron is at the rank early: he is waiting to hear how the night went
    keep(R, 'rank');
    const atRank = R.space === 'street' && !R.moving && hyp(R.x, R.z, SPOTS.rank[0], SPOTS.rank[1]) < 3;
    if (!x.courierOut && atRank) {
      // he comes up from the quay; never put down where Tom could watch him appear
      const from = T.courierComesFrom.find(([sx, sz]) => G.tom.space !== 'street' || !G.env.los(G.tom.x, G.tom.z, sx, sz) || hyp(G.tom.x, G.tom.z, sx, sz) > 60);
      if (from) {
        Object.assign(M, { override: null, gone: false, space: 'street', x: from[0], z: from[1], awake: true, state: 'idle', inCar: false, route: null, moving: false });
        x.courierOut = true;
      }
    }
    if (x.courierOut && atRank) {
      if (together(M, R, T.tellsWithinMetres)) {
        M.route = null;
        M.moving = false;
        pass(M, R, 'at the rank');
        x.courierLeavesAt = G.played + T.headsTogetherRealSeconds;
      } else if (!M.route || !M.moving) goToPoint(M, R.x + 0.9, R.z + 0.9);
    }
    return;
  }
  if (x.courierOut && G.played >= (x.courierLeavesAt || 0)) {
    x.courierOut = false;
    M.hold = false;
    M.override = { where: 'off', act: 'idle', until: G.t + 600 };
    M.goalKey = '';
  }
  if (pending('ron', 'darren')) {
    if (R.chat) return; // still hearing it
    keep(D, 'pave');
    const dAt = D.space === 'street' && !D.moving && hyp(D.x, D.z, SPOTS.pave[0], SPOTS.pave[1]) < 3;
    if (!dAt) return;
    if (together(R, D, T.tellsWithinMetres)) {
      R.route = null;
      R.moving = false;
      pass(R, D, "on the pavement outside Mickey's");
      x.ronBackAt = G.played + T.headsTogetherRealSeconds;
    } else if (!R.route || !R.moving) {
      R.override = null;
      goToPoint(R, D.x + 0.8, D.z + 0.9);
    }
    return;
  }
  if (x.ronBackAt && G.played >= x.ronBackAt) {
    x.ronBackAt = 0;
    R.hold = false;
    send(R, 'rank', 'idle', G.t + 120);
  }
  // Darren keeps to the pavement until he has said it
  const unsaid = x.things.some((th) => th.knows.darren && !th.saidBy.darren);
  if (unsaid) keep(D, 'pave');
}
// What Darren says, from what he really knows.
function darrenLine(kn) {
  const has = (w) => kn.some((th) => th.what === w);
  if (has('made') && has('ran')) return ['You ran from Ibbotson and still made the landing. Their man saw the lot from the shelter. Ron near enough smiled, chief.', 'ran from the constable and still made the landing'];
  if (has('made')) return ["So you carried it. Ron had it off their man first thing: the landing got its envelope. Mickey's lad after all, chief.", 'made the landing with the envelope'];
  if (has('searched')) return ['Ibbotson had your coat open on the quay, I hear. Their man watched it from the shelter, and no envelope came. They count that, chief.', 'was searched on the quay and lost the envelope to the constable'];
  if (has('ran')) return ['You ran from Ibbotson, I hear, and the landing stood waiting. No envelope. They count that, chief.', 'ran from the constable and never reached the landing'];
  return ["Ron says the landing stood waiting and no envelope came. They don't like waiting, chief. They count it.", 'never reached the landing with the envelope'];
}
function faces(x) {
  const t = G.tom;
  if (ui.modal || t.inCar || G.story.phase !== 'play') return;
  // Darren says it to his face, once
  const D = P_('darren'),
    kn = x.things.filter((th) => th.knows.darren && !th.saidBy.darren);
  if (D && kn.length && !D.chat && !D.moving && inView(D, T.saysWithinMetres) && !ui.subs.length) {
    const [line, what] = darrenLine(x.things.filter((th) => th.knows.darren && G.t - th.t < 2880));
    for (const th of kn) th.saidBy.darren = Math.round(G.t);
    x.saidT = G.t;
    D.ang = Math.atan2(t.x - D.x, t.z - D.z);
    D.mind.look = T.lookHeldRealSeconds;
    sub(line, D.def.name, 'face', 7);
    if (G.hooks.sfx) G.hooks.sfx('face');
    G.stats.comebacks++;
    note(`Darren Milner knows he ${what}. He said so to his face, outside Mickey's; he had it from Ron.`, 'note', 'back-darren-' + dayNow(), { who: 'darren', how: 'Said to his face', sure: 'sure' });
    if (!x.opened) {
      x.offer = true; // the Ledger is offered now: there is something in it worth reading
      x.offerAt = G.stats.ledgerOpens || 0;
    }
    return;
  }
  // anybody else who knows holds a look a moment too long, the first time he comes by; if it went badly, then turns away
  for (const P of G.named) {
    if (P.id === 'darren' || P.def.police || P.chat) continue;
    const th = x.things.find((q) => q.knows[P.id] && !q.looked[P.id]);
    if (!th || !inView(P, T.lookWithinMetres)) continue;
    for (const q of x.things) if (q.knows[P.id]) q.looked[P.id] = Math.round(G.t);
    P.mind.look = T.lookHeldRealSeconds;
    P.alert = { x: t.x, z: t.z, t: T.lookHeldRealSeconds };
    const bad = x.things.some((q) => q.knows[P.id] && (q.what === 'missed' || q.what === 'searched'));
    if (bad) x.turn = { id: P.id, at: G.played + T.lookHeldRealSeconds };
    note(`${P.def.name} looked at him a moment too long${bad ? ', then turned his back' : ''}. He knows about last night, Tom thinks.`, 'note', 'back-look-' + P.id + '-' + dayNow(), { who: P.id, how: 'Saw him looking', sure: 'thinks so' });
    break;
  }
  if (x.turn && G.played >= x.turn.at) {
    const P = P_(x.turn.id);
    if (P) P.alert = { x: P.x - (t.x - P.x), z: P.z - (t.z - P.z), t: T.backTurnedRealSeconds };
    x.avoided = (x.avoided || []).concat([x.turn.id]);
    x.turn = null;
  }
}

G.hooks.happened = (what) => happened(what);

register({
  id: 'back',
  fresh: () => ({ things: [], courierOut: false, courierLeavesAt: 0, ronBackAt: 0, saidT: 0, offer: false, offerAt: 0, opened: false, turn: null, avoided: [] }),
  step() {
    const x = X('back');
    // the offer stands until he has opened the Ledger after it was made (the count of openings is the game's own)
    if (x.offer && (G.stats.ledgerOpens || 0) > x.offerAt) {
      x.opened = true;
      x.offer = false;
    }
    if (G.paused || G.story.phase !== 'play') return;
    if (!x.things.length) return;
    road(x);
    faces(x);
  },
  hotspots(out) {
    const x = X('back');
    if (x.offer && !G.tom.inCar) out.push({ k: 'L', t: 'The Ledger: what he knows, and how sure', run: () => ui.hooks.ledger && ui.hooks.ledger('keyboard') });
  },
  hook: {
    x: () => X('back'),
    whoSees,
    // the printed chain: who saw it, and each meeting that carried it on
    chain: (what) =>
      X('back')
        .things.filter((th) => !what || th.what === what)
        .map((th) => ({
          what: th.what,
          at: clock(th.t),
          saw: Object.keys(th.knows).filter((id) => th.knows[id].how === 'saw').map(nameOf),
          told: th.chain.map((c) => `${nameOf(c.a)} told ${nameOf(c.b)} ${c.at}, ${clock(c.t)}`),
          knows: Object.keys(th.knows).map(nameOf),
          said: Object.keys(th.saidBy).map(nameOf),
        })),
  },
});
