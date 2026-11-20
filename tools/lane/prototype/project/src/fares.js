// LEDGER. Fares: few and chosen, each a person with something going on, each feeding the night (cover, eyes, an
// alibi, a risk). Pauline calls them; Tom takes one, or gives it to a driver in one press. No meter, no ratings, no
// long empty drives: a fare is a few minutes and ends at the door. (His words, 19 Nov: "This is not a taxi sim game".)
// The fares themselves are written in game/fares_data.js; the rules that pick one, price it and give the way are
// the pure piece game/pieces/fare_rules.js. This file plays them.
import { G, hour, day } from './state.js';
import { hyp, clamp, pounds, money } from './util.js';
import { act, logLine } from './events.js';
import { meet, note } from './ledger.js';
import { DESTS } from './map.js';
import { sub, say, scene, show, $, tomName, fade, choose } from './ui.js';
import { decision } from './talk.js';
import { setMarker } from './render/sync.js';
import { fl, advanceTo } from './work.js';
import { earn } from './money.js';
import { goToPoint } from './routines.js';
import { RULES } from './rules.js';
import { X, emit } from './game/core.js';
import { FARES, PLACES_F, ROADS_F, JUNCTIONS_F } from './game/fares_data.js';
import { PIECE as FR } from './game/pieces/fare_rules.js';

const FARE = RULES.fares;
const TF = () => RULES.game.fares;
const R = FR.fns;
const RADIO = 'Pauline, on the radio';

// every place a fare names is a destination the map knows by a key (the test hook reads fares by these)
for (const k in PLACES_F) {
  const p = PLACES_F[k];
  if (!p.dest) {
    p.dest = 'f_' + k;
    DESTS[p.dest] = { n: p.n, p: p.p };
  }
}
const FARE_BY_ID = Object.fromEntries(FARES.map((f) => [f.id, f]));
const placeOfDest = (dk) => Object.values(PLACES_F).find((p) => p.dest === dk) || null;

// ---------- the state the save holds (G.x.fares; see game/fares.js) ----------
export const freshFares = () => ({
  week: 0,
  done: [], // fares driven or handed on this week: none comes twice in a week
  lastWrinkle: null, // no wrinkle twice running
  day: -1,
  offeredToday: 0,
  eveningOffered: 0,
  flags: {}, // what fares have turned up: coldstoreKnown, julieDrives, shaunPaintKnown ...
  carrying: null, // a thing in the cab that is not his (a search finds it)
  after: null, // what a fare left behind it: a parcel to deliver, a man to wait for, a runner
  log: [], // every fare offered, with what was chosen and how it ended (the playtester's log)
  book: 0, // pence the drivers have put in the fare book without him
  lostToOtherFirm: 0,
  lost: 0, // the running share of calls that have gone to the other firm
});
const S = () => X('fares');
const rung = () => (G.x && G.x.rise && G.x.rise.rung) || 1;
const carOff = () => !!(G.x && G.x.cars && G.x.cars.offRoadUntil > G.t);
const driverOn = () => (hour() >= 7 && hour() < 19 ? 'kevin' : 'terry');
const first = (id) => (G.people[id] ? G.people[id].def.name.split(' ')[0] : 'Kevin');
function flagsNow() {
  const f = fl(),
    s = S();
  return Object.assign({}, s.flags, {
    tour: !!f.tour,
    first: !!f.firstFareDone,
    ellisAbout: !!G.story.ellis || !!f.ellisAsking || ((G.x && G.x.law && G.x.law.stage) || 0) >= 1 || day() >= 3,
  });
}
function rollDay() {
  const s = S(),
    d = day();
  if (s.day !== d) {
    s.day = d;
    s.offeredToday = 0;
    s.eveningOffered = 0;
    const w = Math.floor(d / 7);
    if (w !== s.week) {
      s.week = w;
      s.done = []; // a new week: the town's people go where they go again
    }
  }
}

// ---------- the way: by road and landmark, and always right (ER-DRIVE-09) ----------
const carAt = () => ({ x: G.car.x, z: G.car.z });
export function wayTo(placeKey, from = carAt()) {
  const p = PLACES_F[placeKey];
  if (!p) return null;
  const legs = R.legs(ROADS_F, from, { x: p.p[0], z: p.p[1] });
  return { legs, words: R.words(legs, JUNCTIONS_F, cap1(p.n) + ': ' + p.landmark), place: p };
}
function sayWay(f, again) {
  const key = f.st === 'carry' ? f.toKey : f.fromKey;
  if (!key) return;
  const w = wayTo(key);
  f.legs = w.legs;
  f.way = w.words;
  sub((again ? 'Again, love. ' : '') + w.words, RADIO, 'over', 9);
}
export function fareWayAgain() {
  const f = G.story.fare;
  if (!f || f.st === 'offer' || !G.tom.inCar) return false;
  sayWay(f, true);
  return true;
}

// The fare places by name, for the test hook: where fares are picked up and where they ask to go.
export function farePlaces() {
  return {
    pickUps: Object.values(PLACES_F).map((p) => ({ name: p.n, xMetres: p.p[0], zMetres: p.p[1] })),
    destinations: Object.keys(DESTS).map((k) => ({ name: DESTS[k].n, xMetres: DESTS[k].p[0], zMetres: DESTS[k].p[1] })),
  };
}
// where the fare stands waiting: on the pavement beside where the cab pulls in
function kerb(p) {
  const on = R.onRoad(ROADS_F, { x: p[0], z: p[1] });
  if (on.id === 'qs') return [p[0] >= 0 ? 6.3 : -6.3, p[1]];
  if (on.id === 'quay') return [p[0], p[1] < 48 ? 42.8 : 53.2];
  return [p[0], p[1] < -18.5 ? -23.3 : -13.6];
}

// ---------- the offer ----------
// Which fare Pauline would call now (null: nothing worth his while). The rule is the piece's.
export function fareNext() {
  rollDay();
  const s = S();
  return R.next(TF(), FARES, {
    day: day(),
    hour: hour(),
    rung: rung(),
    doneThisWeek: s.done,
    lastWrinkle: s.lastWrinkle,
    offeredToday: s.offeredToday,
    eveningOffered: s.eveningOffered,
    flags: flagsNow(),
  });
}
export function fareOffer(special) {
  const st = G.story;
  if (st.fare || !G.car.keys) return;
  let f;
  if (special && special.id && FARE_BY_ID[special.id]) f = fromData(FARE_BY_ID[special.id]);
  else if (special) {
    // a fare the story asks for outright (June's lift to the station): no wrinkle, the old shape
    f = Object.assign({ data: null }, special);
    f.toKey = Object.keys(PLACES_F).find((k) => PLACES_F[k].dest === f.dest) || null;
  } else {
    if (carOff()) return sub("You've no car, love. It's at the yard till it's mended. Kevin has the fares.", RADIO, 'over', 6);
    const id = fareNext();
    if (!id) {
      const s = S();
      if (!s.nothingSaid || G.t - s.nothingSaid > 30) {
        s.nothingSaid = G.t;
        sub(
          rung() >= 2
            ? `Nothing that needs you, love. ${first(driverOn())} has the ordinary ones.`
            : `Nothing just now, love. ${first(driverOn())} has the last one.`,
          RADIO,
          'over',
          5,
        );
      }
      return;
    }
    // after a drive-off people ring the other firm for a while (A14; ER-DRIVE-10)
    const lost = G.hooks.faresLostShare ? G.hooks.faresLostShare() : 0,
      s = S();
    s.lost = (s.lost || 0) + lost;
    if (s.lost >= 1) {
      s.lost -= 1;
      s.lostToOtherFirm++;
      s.offeredToday++;
      s.done.push(id);
      s.log.push({ id, t: Math.round(G.t), wrinkle: FARE_BY_ID[id].wrinkle, choice: 'rang the other firm', outcome: 'lost' });
      return sub("That one rang Stather's instead, love. People are saying things about our cars.", RADIO, 'over', 6);
    }
    f = fromData(FARE_BY_ID[id]);
  }
  const D = DESTS[f.dest];
  const metres = f.data ? R.metres(R.legs(ROADS_F, { x: f.sx, z: f.sz }, { x: D.p[0], z: D.p[1] })) : hyp(f.sx, f.sz, D.p[0], D.p[1]);
  f.pay = f.data && PLACES_F[f.toKey].edge ? TF().edgeFarePence : R.pay(FARE, metres);
  f.st = 'offer';
  f.t = TF().offerStandsRealSeconds;
  f.real = 0;
  st.fare = f;
  if (f.data) {
    const s = S();
    s.offeredToday++;
    if (hour() >= TF().eveningFromHour) s.eveningOffered++;
    sub(f.data.call, RADIO, 'over', 8);
  } else sub(`Car wanted, ${f.from} to ${D.n}. ${f.who ? 'Asked for you, love.' : 'Any car.'}`, RADIO, 'over', 6);
  if (G.hooks.sfx) G.hooks.sfx('radio');
  fareUI();
}
function fromData(d) {
  const a = PLACES_F[d.from],
    b = PLACES_F[d.to],
    [kx, kz] = kerb(a.p);
  return { id: d.id, data: d, from: a.n, fromKey: d.from, toKey: d.to, sx: kx, sz: kz, px: a.p[0], pz: a.p[1], dest: b.dest, who: d.who || null, ask: null, rideI: 0, rideT: 5, said: {} };
}

function fareUI() {
  const f = G.story.fare;
  show('fare', !!f);
  setMarker(null); // no marker in the world: the way is Pauline's words and the landmarks
  if (!f) return;
  const D = DESTS[f.dest],
    to = f.toKey ? PLACES_F[f.toKey] : null,
    from = f.fromKey ? PLACES_F[f.fromKey] : null,
    who = f.data ? cap1(f.data.who ? G.people[f.data.who].def.name : f.data.pax.desc) + '<br>' : '';
  $('fare').innerHTML =
    `<div class="h">${f.st === 'offer' ? 'PAULINE HAS ONE' : 'THE FARE'}</div>${who}FROM ${f.from}<br>TO ${D.n}<br>QUOTED ${money(f.pay)}<br><br>` +
    (f.st === 'offer'
      ? `<b>[Y] Take it</b><br>[G] Give it to ${first(driverOn())}`
      : f.st === 'pickup'
        ? `${from ? cap1(from.landmark) + '.<br>' : ''}Pull in beside them and stop.<br>[R] The way again`
        : `${to ? cap1(to.landmark) + '.<br>' : ''}Pull in and stop at the door.<br>[R] The way again`);
}

export function fareAccept() {
  const f = G.story.fare;
  if (!f || f.st !== 'offer') return;
  f.st = 'pickup';
  const P = f.who ? G.people[f.who] : paxFor(f);
  f.pid = P.id;
  P.override = null;
  P.hold = true;
  P.route = null;
  P.moving = false;
  P.gone = false;
  P.dead = false;
  P.down = false;
  P.space = 'street';
  P.x = f.sx;
  P.z = f.sz;
  P.awake = true;
  P.state = 'idle';
  P.inCar = false;
  P.atWindow = false;
  if (!fl().firstFare) {
    fl().firstFare = 1;
    sub("Car two? That you, love? Go on then. Don't take the long way, they notice.", RADIO, 'over', 5);
  }
  if (f.fromKey) sayWay(f);
  fareUI();
}
function paxFor(f) {
  const want = f.data && f.data.pax ? f.data.pax.sex : null,
    ids = want === 'f' ? ['pax1'] : want === 'm' ? ['pax0', 'pax2'] : ['pax0', 'pax1', 'pax2'],
    busy = S().after && S().after.pid,
    id = ids.find((i) => G.people[i] && i !== busy) || ids[0],
    P = G.people[id];
  if (f.data && f.data.pax) P.def.desc = f.data.pax.desc;
  return P;
}
// One press gives the fare on the radio to the driver on shift: it still goes in the book, and he keeps his hands free.
export function fareHand() {
  const f = G.story.fare,
    s = S();
  if (!f || f.st !== 'offer') return false;
  const drv = driverOn();
  G.story.fare = null;
  fareUI();
  if (f.data) {
    s.done.push(f.id);
    s.log.push({ id: f.id, t: Math.round(G.t), wrinkle: f.data.wrinkle, choice: 'handed to ' + drv, outcome: 'in the book' });
  }
  bookByDriver(f.pay);
  sub(`${first(drv)}'s got it, love. It goes in the book all the same.`, RADIO, 'over', 4);
  G.story.fareCool = TF().nextOfferAfterRealSecondsAtLeast;
  return true;
}
// A fare a driver takes fills the book (room to wash behind); little of it reaches Tom's pocket.
export function bookByDriver(pence) {
  const m = G.money,
    s = S();
  m.fares += pence;
  m.sinceWash += pence;
  s.book += pence;
  const own = Math.round(pence * TF().driverShareToThePocket);
  if (own > 0) earn(own, false, 'a driver\'s fare, the owner\'s share');
}

// ---------- the one decision of a fare, put on the keys while he drives ----------
function ask(f) {
  f.ask = 'open';
  f.askT = 0;
  const P = G.people[f.pid];
  sub(f.data.ask.say, tomName(P), 'face', 9);
}
export function fareAnswer(yes) {
  const f = G.story.fare;
  if (!f || f.ask !== 'open') return false;
  const d = f.data,
    P = G.people[f.pid],
    o = (yes ? d.yes : d.no) || {};
  f.ask = yes ? 'yes' : 'no';
  f.o = o;
  sub(yes ? d.ask.yesSay : d.ask.noSay, tomName(P), 'face', 6);
  for (const id in o.regard || {}) {
    const Q = G.people[id];
    if (Q && Q.mind) Q.mind.regard = clamp(Q.mind.regard + o.regard[id], -1, 1);
  }
  if (o.flag) S().flags[o.flag] = 1;
  if (o.ledger) note(o.ledger, 'note', 'fare:' + d.id + ':said', { who: d.who || undefined, how: 'Said in the cab' });
  if (o.tail && G.hooks.tailStart) G.hooks.tailStart('van', f);
  emit('fare:answer', { id: d.id, yes });
  return true;
}
// what the keys can do for a fare right now, for the prompts at the wheel
export function farePrompts(out) {
  const f = G.story.fare;
  if (!f) return;
  if (f.st === 'offer') out.push({ k: 'G', t: 'Give it to ' + first(driverOn()), run: fareHand });
  else if (f.ask === 'open' && f.data) {
    out.push({ k: 'Y', t: f.data.ask.yes, run: () => fareAnswer(true) });
    out.push({ k: 'G', t: f.data.ask.no, run: () => fareAnswer(false) });
  } else out.push({ k: 'R', t: 'The way again', run: fareWayAgain });
}

// ---------- the ride ----------
export function fareStep(dt) {
  const st = G.story,
    f = st.fare,
    t = G.tom,
    c = G.car;
  afterStep(dt);
  if (!f) {
    const onAir = hour() >= FARE.radioFromHour && hour() < FARE.radioUntilHour;
    if (t.inCar && c.keys && onAir && !st.job?.carrying && !carOff() && !S().after) {
      st.fareCool = (st.fareCool ?? TF().firstOfferAfterRealSeconds) - dt;
      if (st.fareCool <= 0) {
        st.fareCool = TF().nextOfferAfterRealSecondsAtLeast + ((G.t * 7) % 1) * (TF().nextOfferAfterRealSecondsAtMost - TF().nextOfferAfterRealSecondsAtLeast);
        if (fareNext()) fareOffer();
      }
    }
    return;
  }
  f.real += dt;
  if (f.st === 'offer') {
    f.t -= dt;
    if (f.t <= 0) {
      // nobody answered: the driver on shift takes it, as if he had been given it
      const who = first(driverOn());
      fareHand();
      sub(`Never mind, love. ${who}'s got it.`, RADIO, 'over');
    }
    return;
  }
  const P = G.people[f.pid],
    D = DESTS[f.dest],
    stopped = Math.abs(c.v) < FARE.stoppedBelowMetresPerSecond;
  if (f.st === 'pickup') {
    const px = f.px ?? f.sx,
      pz = f.pz ?? f.sz;
    if (t.inCar && stopped && Math.min(hyp(c.x, c.z, f.sx, f.sz), hyp(c.x, c.z, px, pz)) < FARE.pickUpWithinMetres) {
      f.st = 'carry';
      f.t0 = f.real;
      P.inCar = true;
      P.x = c.x;
      P.z = c.z;
      sub(f.data ? f.data.in : `${cap1(D.n)}, please.`, tomName(P), 'face', 6);
      if (!P.anon) meet(P);
      if (f.data && f.data.wrinkle === 'hurry') {
        f.hurry = TF().hurryRealSeconds;
        ask(f);
      }
      if (f.data && f.data.yes && f.data.yes.mirror !== undefined && G.hooks.mirrorStart) G.hooks.mirrorStart(f);
      if (f.toKey) {
        const w = wayTo(f.toKey);
        f.legs = w.legs;
        f.way = w.words;
        f.wayT = 6.5; // Pauline gives the way once he is moving, after the fare has spoken
      }
      fareUI();
    }
    return;
  }
  // carrying
  P.x = c.x;
  P.z = c.z;
  if (f.hurry !== undefined) f.hurry -= dt;
  if (f.wayT !== undefined && (f.wayT -= dt) <= 0) {
    f.wayT = undefined;
    sub(f.way, RADIO, 'over', 9);
  }
  if (f.data) {
    // the fare talks, then asks: never two minutes without a person, a decision or a sighting (ER-CORE-08)
    f.rideT -= dt;
    if (f.rideT <= 0 && f.ask !== 'open') {
      const lines = f.data.ride || [];
      if (f.rideI < lines.length) {
        sub(lines[f.rideI++], tomName(P), 'face', 7);
        f.rideT = 9;
      } else if (f.data.ask && !f.ask) ask(f);
      else f.rideT = 99;
    }
    // a junction before the turn: "Left here." (A9)
    if (f.legs && Math.abs(c.v) > 2) {
      const lh = R.leftHere(TF(), f.legs, { x: c.x, z: c.z });
      if (lh && !f.said[lh.key]) {
        f.said[lh.key] = 1;
        sub(cap1(lh.turn) + ' here.', tomName(P), 'face', 3);
      }
    }
  }
  const edge = f.toKey && PLACES_F[f.toKey].edge;
  if (t.inCar && stopped && hyp(c.x, c.z, D.p[0], D.p[1]) < FARE.dropOffWithinMetres + (edge ? 4 : 0)) fareDone(f, P, D);
}

const cap1 = (s) => s.charAt(0).toUpperCase() + s.slice(1);

async function fareDone(f, P, D) {
  const st = G.story,
    s = S(),
    d = f.data,
    T = TF();
  st.fare = null;
  fareUI();
  if (f.ask === 'open') f.ask = 'no'; // an ask left unanswered at the door is a no, said by silence
  const o = f.o || {};
  P.inCar = false;
  P.hold = false;
  const side = G.car.ang;
  P.x = G.car.x + Math.cos(side) * FARE.passengerStepsOutMetres;
  P.z = G.car.z - Math.sin(side) * FARE.passengerStepsOutMetres;
  P.goalKey = '';
  if (P.anon) P.override = { where: 'off', act: 'idle', until: G.t + FARE.passerByWalksOffForGameMinutes };
  let paid = f.pay,
    outcome = 'paid';
  if (G.hooks.mirrorEnd) outcome = G.hooks.mirrorEnd(f, P) || outcome;
  if (G.hooks.tailEnd) outcome = G.hooks.tailEnd(f, P) || outcome;
  // the soft edge (DESIGN 5): a fare that leaves the Hook comes back as time passed and money paid
  if (d && PLACES_F[f.toKey].edge) {
    await scene(async () => {
      await fade(true, `Out of the Hook, to ${D.n.replace(/^the \w+ road, for /, '')}, and back again.\n${T.edgeTakesGameMinutes} minutes, and the time is in the book.`);
      P.override = { where: 'off', act: 'idle' };
      P.gone = true;
      advanceTo(G.t + T.edgeTakesGameMinutes, false);
      G.car.ang += Math.PI;
      G.car.v = 0;
      await fade(false);
    });
    outcome = 'out of the Hook and back';
  }
  if (d && d.wrinkle === 'runner') {
    // out of the door without paying: get out and run him down, or let him go
    paid = 0;
    outcome = 'ran';
    s.after = { kind: 'runner', id: d.id, pid: P.id, pay: f.pay, t: 0, unseen: 0 };
    P.hold = true;
    P.override = null;
    const away = [P.x + (P.x < G.car.x ? -60 : 60), P.z + (P.z < 0 ? 30 : -30)];
    goToPoint(P, away[0], away[1], T.runnerRunsMetresPerSecond);
    sub('The door bangs. He is out and running, and the fare with him. [F] Get out and go after him, or let him go.', '', 'over', 7);
  }
  if (d && d.wrinkle === 'hurry') {
    const made = f.hurry > 0;
    if (f.ask === 'yes') {
      act(made ? 'fare_kept_word' : 'fare_late', P.anon ? { name: P.def.desc } : { target: P.id });
      if (made) paid += T.bigTipPence;
      sub(made ? 'You said you would, and you did. Keep that.' : 'You promised. I shall say so, where I am asked.', tomName(P), 'face', 5);
      outcome = made ? 'promised and made it' : 'promised and late';
    } else {
      if (made) paid += T.tipPence;
      sub(made ? 'Made it. Good man.' : 'Too late. Well. You never promised.', tomName(P), 'face', 4);
      outcome = made ? 'made it' : 'late';
    }
  }
  if (d && d.wrinkle === 'wait') {
    if (f.ask === 'yes') {
      s.after = { kind: 'wait', id: d.id, pid: P.id, t: T.waitRealSeconds, x: G.car.x, z: G.car.z };
      P.override = { where: 'off', act: 'idle', until: G.t + 20 };
      outcome = 'waiting';
    } else outcome = 'drove off';
  }
  if (o.parcel) {
    s.after = { kind: 'parcel', id: d.id, to: o.parcel, since: G.t };
    s.carrying = 'a parcel that is not his';
    const w = wayTo(o.parcel);
    sub(`The parcel is on the back seat. ${w.words}`, '', 'over', 9);
    outcome = 'carrying a parcel';
  }
  if (o.tip) paid += T.tipPence;
  let free = !!o.free;
  if (!P.anon && !d) {
    // the story's own fares (the old shape): Julie's slate and June's goodbye
    if (P.id === 'julie' && G.debts.julie.st === 'open') {
      const i = await scene(() =>
        decision('julie', "What do I owe you? Only I'm a bit short till Thursday. Story of my life.", {
          leaveIdx: 0,
          ask: 'whether Julie pays her fare',
          keep: ['How much is on the slate?', 'How long have you owed it?'],
          keepSay: "Nine pounds, since the summer. I've not forgotten it.",
          opts: [
            { say: [`That's ${pounds(f.pay)}, please.`, `${cap1(pounds(f.pay))}, as Pauline said.`] },
            {
              say: ['Call it nothing. And the slate is struck out.', "No charge. I'm striking your slate too."],
              q: 'You mean it? Nothing, and the slate gone?',
              yes: ['Yes. Nothing owed.', "Yes. It's struck out."],
              no: ['No. Let me think.', 'No. Not the slate.'],
              keep: ['How much is on the slate?', 'How long have you owed it?'],
              keepSay: 'Nine pounds, since the summer. You said nothing owed. You mean it?',
            },
          ],
        }),
      );
      if (i === 1) {
        free = true;
        G.debts.julie.st = 'forgiven';
        act('debt_forgive', { target: 'julie' });
      }
    }
    if (P.id === 'june')
      await scene(async () => {
        await say('june', 'Thank you for the lift. I meant what I said. I want nothing from it.');
        await say('june', 'But whatever you turn that office into, do it with your eyes open. He never did.');
        fl().juneGone = 1;
        P.override = { where: 'off', act: 'idle' };
      });
  }
  if (!P.anon) {
    if (free) {
      paid = 0;
      act('free_ride', { target: P.id, dest: 'to ' + D.n });
    } else act('fare', { target: P.id, dest: 'to ' + D.n });
    P.mind.fam = clamp(P.mind.fam + FARE.passengerFamiliarityGain, 0, 1);
    P.mind.regard = clamp(P.mind.regard + FARE.passengerRegardGain, -1, 1);
    if (P.def.sched && P.def.sched.length <= 1) P.override = { where: 'off', act: 'idle' }; // somebody with no week on the street goes about their day
  }
  G.money.fareCount++;
  fl().firstFareDone = 1;
  if (paid) {
    earn(paid, false, 'a fare');
    G.money.fares += paid;
    G.money.sinceWash += paid;
    sub(`${money(paid)} in the book.`, '', 'over', 2.5);
  }
  if (d) {
    s.done.push(d.id);
    s.lastWrinkle = d.wrinkle;
    if (d.flag) s.flags[d.flag] = 1;
    // what the fare was worth to the night goes in the Ledger, in his own words
    note(d.ledger, 'note', 'fare:' + d.id, { who: d.who || undefined, how: 'Heard in the cab' });
    s.log.push({ id: d.id, t: Math.round(G.t), wrinkle: d.wrinkle, gives: d.gives, choice: f.ask || 'none', outcome, paidPence: paid, realSeconds: Math.round(f.real) });
    if (s.log.length > 120) s.log.splice(0, 40);
    logLine(`Fare ${d.id}: ${d.wrinkle || 'plain'}, ${outcome}, ${money(paid)}`, 'fare');
  }
  emit('fare:done', { id: d ? d.id : null, who: P.id, paidPence: paid, wrinkle: d ? d.wrinkle : null, gives: d ? d.gives : null, outcome });
  st.fareCool = TF().nextOfferAfterRealSecondsAtLeast;
  if (G.hooks.save) G.hooks.save();
}

// ---------- what a fare leaves behind it ----------
function afterStep(dt) {
  const s = S(),
    a = s.after,
    t = G.tom,
    c = G.car,
    T = TF();
  if (!a) return;
  if (a.kind === 'parcel') {
    const p = PLACES_F[a.to].p,
      here = t.inCar ? Math.abs(c.v) < FARE.stoppedBelowMetresPerSecond && hyp(c.x, c.z, p[0], p[1]) < FARE.dropOffWithinMetres : hyp(t.x, t.z, p[0], p[1]) < 4;
    if (here && !G.paused) {
      s.after = null;
      s.carrying = null;
      act('fare_parcel', { dest: PLACES_F[a.to].n, noiseR: 2 });
      earn(T.parcelPaysPence, true, 'a parcel carried for a fare');
      sub(`The side door opens a hand's width and the parcel is gone. ${money(T.parcelPaysPence)}, folded, for the tin.`, '', 'over', 6);
      note(`Left a fare's parcel at ${PLACES_F[a.to].n}. ${cap1(pounds(T.parcelPaysPence))} for the tin, and no name given.`, 'note', 'parcel:' + a.id + ':' + Math.floor(G.t / 1440));
      log(a.id, 'parcel delivered');
    }
  } else if (a.kind === 'wait') {
    const d = hyp(c.x, c.z, a.x, a.z);
    if (d > RULES.game.cars.drivesOffBeyondMetres) {
      s.after = null;
      sub('You pull away. He will come out to an empty kerb, and remember the firm.', '', 'over', 5);
      log(a.id, 'left him there');
      return;
    }
    a.t -= dt;
    if (a.t <= 0 && !G.paused) {
      s.after = null;
      act('fare_wait', { noiseR: 6 });
      earn(T.waitPaysPence, true, 'kept the engine running for a fare');
      sub(`He is back at the window. "That will do. You were never here." ${cap1(pounds(T.waitPaysPence))}, for the tin.`, '', 'over', 7);
      note('Kept the engine running for a fare who wanted it forgotten. He paid for the forgetting.', 'note', 'wait:' + a.id + ':' + Math.floor(G.t / 1440));
      log(a.id, 'waited and was paid');
    }
  } else if (a.kind === 'runner') {
    const P = G.people[a.pid];
    if (!P) return (s.after = null);
    a.t += dt;
    const tx = t.inCar ? c.x : t.x,
      tz = t.inCar ? c.z : t.z,
      d = hyp(tx, tz, P.x, P.z),
      seen = G.env.los(tx, tz, P.x, P.z);
    a.unseen = seen ? 0 : a.unseen + dt;
    if (!t.inCar && d < T.runnerCaughtWithinMetres && !G.paused) {
      s.after = null;
      P.route = null;
      P.moving = false;
      scene(async () => {
        const i = await choose(P.id, 'All right! All right. Get off me.', ['Take the fare off him', 'Let him go']);
        if (i === 0) {
          earn(a.pay, false, 'a fare, taken off a runner');
          G.money.fares += a.pay;
          G.money.sinceWash += a.pay;
          act('fare_collared', { name: P.def.desc });
          await say(P.id, `Here. ${cap1(pounds(a.pay))}. You are worse than your uncle.`);
          log(a.id, 'caught and paid');
        } else {
          await say(P.id, 'You what? Right. Ta. I will not forget that.');
          log(a.id, 'caught and let go');
        }
        P.hold = false;
        P.override = { where: 'off', act: 'idle' };
      });
    } else if (a.unseen > T.runnerLostAfterUnseenRealSeconds || d > T.runnerLostBeyondMetres || a.t > 85) {
      s.after = null;
      P.hold = false;
      P.override = { where: 'off', act: 'idle' };
      sub('He is gone. A fare short, and a face to know again.', '', 'over', 5);
      log(a.id, 'got away');
    }
  }
}
function log(id, outcome) {
  const s = S(),
    e = s.log.slice().reverse().find((x) => x.id === id);
  if (e) e.after = outcome;
  logLine(`Fare ${id}: ${outcome}`, 'fare');
}
