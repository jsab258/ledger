// LEDGER, the whole game: the system "walks". THE WALK (DESIGN 2, part 1.4.5, ER-EYES-04): a witness who means to
// tell sets off for the phone box and is seen going. No phone in any pocket in 1990: the walk is the timer, and
// until it ends nothing is on record. Tom can reach them first: talk them round, pay, threaten, put it right, or
// let them go. A threat can stop a report to the police, never the street's talk (ruling 3 Oct). Every statement
// the police hold now comes from a walk that ended; the old nightly batch only sends the late ones off at eight.
// Rules: pieces/eyes.js (walk, reached) and pieces/law.js (mayArrest).
import { register, X, write, tell, emit, on, inView } from './core.js';
import { G } from '../state.js';
import { hyp, clamp, quid } from '../util.js';
import { act, logLine } from '../events.js';
import { pay } from '../money.js';
import { choose, scene, say, tomName } from '../ui.js';
import { goToPoint, resolve, gameMinPerSec } from '../routines.js';
import { KINDS } from '../kinds.js';
import { tomNotices, attached } from '../seeing.js';
import { wouldTell, statementMade } from '../police.js';
import { ROOMS, SPOTS, freeSpot } from '../map.js';
import { RULES } from '../rules.js';
import { PIECE as EYES } from './pieces/eyes.js';
import { PIECE as LAW } from './pieces/law.js';

const W = RULES.game.foot.walk;
const PHONE = () => SPOTS.phone;
const live = (w) => w.st === 'means' || w.st === 'going' || w.st === 'calling';
const walkOf = (P) => X('walks').walks.find((w) => w.who === P.id && live(w)) || null;
const spare = (P) => {
  // back to their own day
  P.hold = false;
  P.hurry = 1;
  P.route = null;
  P.goalKey = '';
  P.mark = null;
};

// Somebody saw a crime plainly and means to tell: the surest first, a second a while after, never more.
function plan(E, ids, atT) {
  const x = X('walks');
  const sure = (id) => (G.people[id].mind.by[E.id] || {}).sure || 0;
  ids = ids.filter((id) => !x.walks.some((w) => w.who === id && w.e === E.id)).sort((a, b) => sure(b) - sure(a)).slice(0, W.walkersAtMostADeed);
  ids.forEach((who, i) => x.walks.push({ n: x.n++, who, e: E.id, st: 'means', atT: atT + i * W.nextWitnessAfterGameMinutes, asked: false }));
  if (x.walks.length > 60) x.walks.splice(0, x.walks.length - 60);
  return ids;
}
// Somebody who found what was left (game/traces.js), or whom the real town's own rules send over the week's damage.
export function walkFor(E, P, o = {}) {
  const x = X('walks');
  if (x.walks.some((w) => w.who === P.id && w.e === E.id)) return null;
  const r = EYES.fns.walk({ metres: 0, inHisSight: false, onEdge: !!(G.x.law && G.x.law.edge) });
  const w = { n: x.n++, who: P.id, e: E.id, st: 'means', atT: G.t + r.startsAfterSeconds * gameMinPerSec(), asked: false, aftermath: o.aftermath || null, town: !!o.town };
  x.walks.push(w);
  return w;
}
function setOff(w) {
  const P = G.people[w.who],
    E = G.ev[w.e];
  const quiet = P && (P.mind.fear >= RULES.police.noStatementIfFearAtLeast || P.mind.bought);
  if (!P || P.dead || !E || (w.aftermath || w.town ? quiet : !wouldTell(P, E))) return void (w.st = 'stayed'); // frightened, paid or warmed to him since
  if (P.fight || P.down || P.busy || P.chat) return; // not this minute
  if (P.space !== 'street' || P.gone) {
    // out of the door: no witness tells from an armchair
    const door = ROOMS[P.space] ? ROOMS[P.space].street : null,
      h = door || [resolve(P, 'home').x, resolve(P, 'home').z],
      f = freeSpot(h[0], h[1]) || h;
    Object.assign(P, { space: 'street', gone: false, awake: true, atWindow: false, x: f[0], z: f[1], override: null });
  }
  const ph = PHONE(),
    seen = tomNotices(P) || inView(P, 40);
  const r = EYES.fns.walk({ metres: hyp(P.x, P.z, ph[0], ph[1]), inHisSight: seen, onEdge: !!(G.x.law && G.x.law.edge) });
  Object.assign(w, { st: 'going', startedPlayed: G.played, startedT: G.t, standsUntil: G.played + r.standsFirstSeconds, dueT: G.t + r.lastsSeconds * gameMinPerSec(), moving: false, seenGoing: false, inSight: seen });
  P.route = null;
  P.hold = true;
  P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z); // a look at him first
  logLine(P.def.name + ' set off for the phone box about: ' + KINDS[E.kind].truth(E), 'police');
  emit('walks.setoff', { who: P.id, e: E.id });
}
function seenGoing(w, P) {
  if (w.seenGoing || !(tomNotices(P) || inView(P))) return;
  w.seenGoing = true;
  const E = G.ev[w.e];
  tell(w.moving ? `${tomName(P)} is walking fast up Quay Street and not looking round. The phone box is that way.` : `${tomName(P)} has stopped dead, looking straight at him. Then at the phone box up the street.`, '', 7);
  write(`${tomName(P)} ${w.aftermath ? 'found it' : 'saw it'} (${KINDS[E.kind].mine(E).toLowerCase()}) and set off for the phone box. Until that call is made, nothing is on record.`, { key: 'walk' + w.n, who: P.id, how: 'Saw it himself', ev: E.id });
}
function told(w) {
  const P = G.people[w.who],
    E = G.ev[w.e],
    x = X('walks');
  w.st = 'told';
  w.toldT = Math.round(G.t);
  spare(P);
  P.mind.stmtGiven = 1;
  // ER-POL-01: no arrest without a named statement, and never twice for one deed
  const may = LAW.fns.mayArrest({ takenFor: !!(G.x.law && G.x.law.takenFor[E.id]), officerSaw: false, statements: [{ namesHim: !w.aftermath && attached(P.mind.by[E.id] || {}), signed: true }] });
  x.statements.push({ who: P.id, e: E.id, t: w.toldT, arrest: may.may, why: may.why });
  if (may.may) statementMade(E, P.id);
  if (w.seenGoing) write(`${tomName(P)} made the call. It is on record now: ${KINDS[E.kind].mine(E).toLowerCase()}.`, { key: 'walktold' + w.n, who: P.id, how: 'Saw it himself', ev: E.id });
  emit('walks.told', { who: P.id, e: E.id, arrest: may.may, aftermath: !!w.aftermath });
}
// He reaches the witness first (E beside them): one go at each witness.
async function reach(w) {
  const P = G.people[w.who],
    E = G.ev[w.e],
    k = KINDS[E.kind],
    x = X('walks'),
    name = tomName(P);
  const was = { route: P.route, hold: P.hold };
  P.route = null;
  P.hold = true;
  const s = { regard: P.mind.regard, nerve: P.def.nerve == null ? 0.5 : P.def.nerve, venal: P.def.venal || 0, upright: !!P.def.upright, crime: k.crime, damage: !!k.damage, askedBefore: w.asked, pocketPence: G.money.clean + G.money.dirty };
  const price = W.payPenceByCrime[clamp(k.crime, 1, 3)];
  const opts = [['talk round', `Talk ${name} round.`]];
  if (price) opts.push(['pay', `Put ${quid(price)} in ${name}'s hand.`]);
  opts.push(['threaten', 'Say what happens to people who talk.']);
  if (k.damage) opts.push(['put it right', `Offer ${quid(W.putRightPence)} for the mending.`]);
  opts.push(['let go', 'Step aside.']);
  const what = k.truth(E).replace(/^Tom /, 'you ').replace(/^A man /, 'a man ');
  const i = await scene(() => choose(P.id, w.asked ? '"I have said all I am saying to you."' : w.aftermath ? `"Somebody has been at it in the night: ${w.aftermath}. I am going to ring the police."` : `"I saw it. I saw ${/^you /.test(what) ? what : 'what you did'}. I am going to ring them."`, opts.map((o) => o[1])));
  const choice = opts[i][0];
  const r = EYES.fns.reached(choice, s);
  w.asked = true;
  w.answer = choice;
  if (r.costPence) pay(r.costPence, false, choice === 'pay' ? 'paid a witness to keep quiet' : 'paid for the mending');
  if (r.bought) P.mind.bought = 1;
  if (r.fearTo != null) P.mind.fear = Math.max(P.mind.fear, r.fearTo);
  if (r.regardBy) P.mind.regard = clamp(P.mind.regard + r.regardBy, -1, 1);
  if (r.makesAnAct) act(r.makesAnAct, { target: P.id }); // a thing done to them, seen by whoever is about: the street hears of it
  if (r.bought) act('paid_quiet', { target: P.id, silent: true });
  x.reached.push({ who: P.id, e: E.id, choice, stopped: r.stops, t: Math.round(G.t) });
  const LINES = {
    'talk round': r.stops ? (w.aftermath ? '"...Aye. Well. Maybe it is none of mine. But I saw it, and I will not forget I saw it."' : '"...Aye. Well. Nobody was hurt. But I saw it, and I will not forget I saw it."') : '"No. You do not get to talk me out of what I saw."',
    pay: r.stops ? '"I never saw a thing." The money is gone into a pocket.' : r.short ? '"With what? You have not got it."' : '"Put that away. Now I have two things to tell them."',
    threaten: r.stops ? 'Not a word. A step back, and then another, and away home the other way.' : '"Is that right. I will tell them that and all."',
    'put it right': r.stops ? '"See that it is mended, then. I will be looking."' : r.short ? '"With what? You have not got it."' : '"It is past mending with money."',
    'let go': 'A long look, and on up the street.',
  };
  await scene(() => say(choice === 'threaten' && r.stops ? '' : choice === 'let go' ? '' : P.id, LINES[choice]));
  if (r.stops) {
    w.st = 'stopped';
    spare(P);
    write(`Stopped ${name} on the way to the phone box (${choice === 'pay' ? 'money' : choice === 'threaten' ? 'a threat' : choice === 'put it right' ? 'paid for the mending' : 'talked round'}). No call was made. ${r.streetStillTalks ? 'The street will still hear of it.' : ''}`, { key: 'walkstop' + w.n, who: P.id, how: 'Did it', ev: E.id });
    emit('walks.stopped', { who: P.id, e: E.id, how: choice, aftermath: !!w.aftermath });
  } else {
    if (r.sooner) P.hurry = 1.5;
    P.hold = was.hold;
    w.moving = false; // she picks her way up again
    if (r.sooner) w.standsUntil = G.played;
  }
}

register({
  id: 'walks',
  fresh: () => ({ n: 1, walks: [], statements: [], reached: [] }),
  loaded() {
    G.hooks.morningWalk = (E, ids) => {
      E.stmt = [];
      const d = Math.floor(G.t / 1440) * 1440 + W.morningWalkAtHour * 60;
      plan(E, ids, d > G.t ? d : d + 1440);
    };
    G.hooks.walkBeat = (P) => {
      const w = walkOf(P);
      return w && (w.st !== 'means' || G.t >= w.atT) ? () => reach(w) : null;
    };
  },
  step(dt) {
    if (G.paused) return;
    const x = X('walks'),
      ph = PHONE();
    for (const w of x.walks) {
      if (!live(w)) continue;
      const P = G.people[w.who];
      if (!P || P.dead) {
        w.st = 'off';
        continue;
      }
      if (w.st === 'means') {
        if (G.t >= w.atT) setOff(w);
        continue;
      }
      seenGoing(w, P);
      const d = hyp(P.x, P.z, ph[0], ph[1]);
      const far = G.tom.space !== 'street' || hyp(P.x, P.z, G.tom.x, G.tom.z) > 45;
      if (w.st === 'going') {
        if (G.played >= w.standsUntil && (!w.moving || (!P.route && d > W.arrivesWithinMetres))) {
          w.moving = true;
          goToPoint(P, ph[0], ph[1], W.metresPerSecond * (P.hurry > 1 ? 1.4 : 1));
        }
        if (d <= W.arrivesWithinMetres || (far && G.t >= w.dueT)) {
          if (far) Object.assign(P, { x: ph[0], z: ph[1] });
          w.st = 'calling';
          w.callUntilT = Math.max(G.t, w.dueT - W.phoneCallRealSeconds * gameMinPerSec()) + W.phoneCallRealSeconds * gameMinPerSec();
          P.route = null;
          P.hold = true;
          P.ang = ph[2] || 0;
          if (tomNotices(P) || inView(P)) tell(`${tomName(P)} is in the phone box, the door pulled to.`, '', 5);
        }
      } else if (w.st === 'calling' && G.t >= w.callUntilT) told(w);
    }
  },
  hook: {
    x: () => X('walks'),
    live: () => X('walks').walks.filter(live).map((w) => ({ who: w.who, st: w.st, e: w.e, dueT: w.dueT, startedPlayed: w.startedPlayed, seenGoing: w.seenGoing })),
  },
});
// every plainly seen crime: whoever means to tell sets off, after a moment in which he can see them make their mind up
on('act', (E) => {
  const k = KINDS[E.kind];
  if (!k || k.crime < 1 || E.stmt !== undefined) return;
  const ids = [...new Set([...(E.wit || []), ...(E.party || [])])].filter((id) => G.people[id] && !G.people[id].anon && wouldTell(G.people[id], E));
  if (!ids.length) return; // nobody means to tell now; somebody who places him later goes in the morning (police.js nightly)
  E.stmt = [];
  const r = EYES.fns.walk({ metres: 0, inHisSight: false, onEdge: !!(G.x.law && G.x.law.edge) });
  plan(E, ids, G.t + r.startsAfterSeconds * gameMinPerSec());
});
// the real town's rules send somebody to the police over the week's damage: that is a walk too, unless he already
// stopped that person, or the walk is under way or over
on('town.went', ({ who, e }) => {
  const P = G.people[who],
    E = G.ev[e],
    x = X('walks');
  if (!P || !E || P.anon) return;
  const mine = x.walks.find((w) => w.who === who && w.e === e);
  if (mine) return; // going, told, or stopped by him: his reaching them stands
  E.stmt = E.stmt || [];
  walkFor(E, P, { town: true });
});
