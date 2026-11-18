// LEDGER. The cab: the radio offer, the pick-up, the drop-off and the fare.
import { G, hour } from './state.js';
import { hyp, rnd, pick, money, clamp, pounds } from './util.js';
import { act } from './events.js';
import { meet } from './ledger.js';
import { SPOTS, DESTS } from './map.js';
import { sub, say, scene, show, $, tomName } from './ui.js';
import { decision } from './talk.js';
import { setMarker } from './render/sync.js';
import { fl } from './work.js';
import { earn } from './money.js';
import { RULES } from './rules.js';

const FARE = RULES.fares;

// ---------- fares ----------
// Where a fare may be waiting: a name the radio says, and the spot on the map.
const PICK = [
  { name: 'the bus stop on Quay Street', spot: 'busstop' },
  { name: 'the ferry landing', spot: 'ferry2' },
  { name: 'the fish dock', spot: 'boxes2' },
  { name: 'the warehouse row', spot: 'row1' },
  { name: 'the station', spot: 'station' },
  { name: 'the market, Copper Row', spot: 'market3' },
  { name: 'the chapel', spot: 'chapelgate' },
  { name: "the corner by Rita's", spot: 'corner' },
  { name: 'the Harbour Office', spot: 'harbourdoor' },
  { name: 'Chapel Lane', spot: 'cl' },
];

// The fare places by name, for the test hook: where fares are picked up and where they ask to go.
export function farePlaces() {
  return {
    pickUps: PICK.map((p) => ({ name: p.name, xMetres: SPOTS[p.spot][0], zMetres: SPOTS[p.spot][1] })),
    destinations: Object.keys(DESTS).map((k) => ({
      name: DESTS[k].n,
      xMetres: DESTS[k].p[0],
      zMetres: DESTS[k].p[1],
    })),
  };
}

export function fareOffer(special) {
  const st = G.story;
  if (st.fare || !G.car.keys) return;
  let f;
  if (special) f = special;
  else {
    const p = pick(PICK),
      dk = pick(Object.keys(DESTS)),
      D = DESTS[dk],
      s = SPOTS[p.spot];
    if (hyp(s[0], s[1], D.p[0], D.p[1]) < FARE.shortestRunMetres) return;
    f = { from: p.name, sx: s[0], sz: s[1], dest: dk, who: null };
  }
  const D = DESTS[f.dest];
  const metres = hyp(f.sx, f.sz, D.p[0], D.p[1]);
  f.pay =
    Math.round((FARE.flagFallPence + metres * FARE.penceAddedPerMetre) / FARE.roundedToPence) *
    FARE.roundedToPence;
  f.st = 'offer';
  f.t = FARE.offerStandsRealSeconds;
  st.fare = f;
  sub(
    `Car wanted, ${f.from} to ${D.n}. ${f.who ? 'Asked for you, love.' : 'Any car.'}`,
    'Pauline, on the radio',
    'over',
    6,
  );
  if (G.hooks.sfx) G.hooks.sfx('radio');
  fareUI();
}

function fareUI() {
  const f = G.story.fare;
  show('fare', !!f);
  if (!f) {
    setMarker(null);
    return;
  }
  const D = DESTS[f.dest];
  $('fare').innerHTML =
    `<div class="h">FARE DOCKET</div>FROM ${f.from}<br>TO ${D.n}<br>FARE ${money(f.pay)}<br><br>` +
    (f.st === 'offer'
      ? '<b>[Y] Take it</b> · ' + Math.ceil(f.t) + 's'
      : f.st === 'pickup'
        ? 'Pick up: pull in beside them and stop.'
        : 'Drop off: pull in at the marker and stop.');
  if (f.st === 'pickup') setMarker(f.sx, f.sz);
  else if (f.st === 'carry') setMarker(D.p[0], D.p[1]);
  else setMarker(null);
}

export function fareAccept() {
  const f = G.story.fare;
  if (!f || f.st !== 'offer') return;
  f.st = 'pickup';
  const P = f.who ? G.people[f.who] : G.people['pax' + Math.floor(rnd(0, 3))];
  f.pid = P.id;
  P.override = null;
  P.hold = true;
  P.route = null;
  P.moving = false;
  P.gone = false;
  P.space = 'street';
  P.x = f.sx;
  P.z = f.sz;
  P.awake = true;
  P.state = 'idle';
  P.inCar = false;
  P.atWindow = false;
  if (!fl().firstFare) {
    fl().firstFare = 1;
    sub(
      "Car two? That you, love? Go on then. Don't take the long way, they notice.",
      'Pauline, on the radio',
      'over',
      6,
    );
  }
  fareUI();
}

export function fareStep(dt) {
  const st = G.story,
    f = st.fare,
    t = G.tom,
    c = G.car;
  if (!f) {
    const onAir = hour() >= FARE.radioFromHour && hour() < FARE.radioUntilHour;
    if (t.inCar && c.keys && onAir && !st.job?.carrying) {
      st.fareCool = (st.fareCool ?? FARE.firstOfferAfterRealSeconds) - dt;
      if (st.fareCool <= 0) {
        st.fareCool = rnd(FARE.nextOfferAfterRealSecondsAtLeast, FARE.nextOfferAfterRealSecondsAtMost);
        fareOffer();
      }
    }
    return;
  }
  if (f.st === 'offer') {
    f.t -= dt;
    if (Math.floor(f.t) !== f.lt) {
      f.lt = Math.floor(f.t);
      fareUI();
    }
    if (f.t <= 0) {
      st.fare = null;
      fareUI();
      sub("Never mind, love. Kevin's got it.", 'Pauline, on the radio', 'over');
      st.fareCool = rnd(FARE.afterAMissedOfferRealSecondsAtLeast, FARE.afterAMissedOfferRealSecondsAtMost);
    }
    return;
  }
  const P = G.people[f.pid],
    D = DESTS[f.dest];
  if (f.st === 'pickup') {
    if (
      t.inCar &&
      Math.abs(c.v) < FARE.stoppedBelowMetresPerSecond &&
      hyp(c.x, c.z, f.sx, f.sz) < FARE.pickUpWithinMetres
    ) {
      f.st = 'carry';
      P.inCar = true;
      P.x = c.x;
      P.z = c.z;
      sub(
        pick([
          `${cap1(D.n)}, please.`,
          `${cap1(D.n)}. Quick as you like.`,
          `You the new owner? ${cap1(D.n)}, then.`,
        ]),
        tomName(P),
      );
      if (!P.anon) meet(P);
      fareUI();
    }
  } else if (f.st === 'carry') {
    P.x = c.x;
    P.z = c.z;
    const stopped = Math.abs(c.v) < FARE.stoppedBelowMetresPerSecond;
    if (t.inCar && stopped && hyp(c.x, c.z, D.p[0], D.p[1]) < FARE.dropOffWithinMetres) fareDone(f, P, D);
  }
}

const cap1 = (s) => s.charAt(0).toUpperCase() + s.slice(1);

async function fareDone(f, P, D) {
  const st = G.story;
  st.fare = null;
  fareUI();
  P.inCar = false;
  P.hold = false;
  const side = G.car.ang;
  P.x = G.car.x + Math.cos(side) * FARE.passengerStepsOutMetres;
  P.z = G.car.z - Math.sin(side) * FARE.passengerStepsOutMetres;
  P.goalKey = '';
  if (P.anon) {
    P.override = { where: 'off', act: 'idle', until: G.t + FARE.passerByWalksOffForGameMinutes };
  }
  let paid = f.pay;
  G.money.fareCount++;
  if (!P.anon) {
    let free = false;
    if (P.id === 'julie' && G.debts.julie.st === 'open') {
      const i = await scene(() =>
        decision('julie', "What do I owe you? Only I'm a bit short till Thursday. Story of my life.", {
          leaveIdx: 0,
          ask: 'whether Julie pays her fare',
          keep: ['How much is on the slate?', 'How long have you owed it?'],
          keepSay: "Nine pounds, since the summer. I've not forgotten it.",
          opts: [
            {
              say: [
                `That's ${pounds(f.pay)}, please.`,
                `${pounds(f.pay).replace(/^./, (m) => m.toUpperCase())} on the meter.`,
              ],
            },
            {
              say: [
                'Call it nothing. And the slate is struck out.',
                "No charge. I'm striking your slate too.",
              ],
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
    if (free) {
      paid = 0;
      act('free_ride', { target: P.id, dest: 'to ' + D.n });
    } else act('fare', { target: P.id, dest: 'to ' + D.n });
    P.mind.fam = clamp(P.mind.fam + FARE.passengerFamiliarityGain, 0, 1);
    P.mind.regard = clamp(P.mind.regard + FARE.passengerRegardGain, -1, 1);
  }
  if (paid) {
    earn(paid);
    G.money.fares += paid;
    G.money.sinceWash += paid;
    sub(`${money(paid)} in the book.`, '', 'over', 2.5);
  }
  st.fareCool = rnd(FARE.afterAFareRealSecondsAtLeast, FARE.afterAFareRealSecondsAtMost);
}
