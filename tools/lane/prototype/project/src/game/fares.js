// LEDGER, the whole game: the system "fares". Few and chosen: the rules are pieces/fare_rules.js, the fares are
// fares_data.js, the play is ../fares.js. This file is the system's own part: its saved state, the prompts at the
// wheel, the drivers who fill the book without him, the places a fare names, and the test calls.
import { register, addPlace, X } from './core.js';
import { G, hour } from '../state.js';
import { RULES } from '../rules.js';
import { hyp } from '../util.js';
import { FARES, PLACES_F, ROADS_F, JUNCTIONS_F } from './fares_data.js';
import { PIECE as FR } from './pieces/fare_rules.js';
import { freshFares, farePrompts, fareWayAgain, fareNext, fareOffer, fareAccept, fareAnswer, fareHand, bookByDriver, wayTo } from '../fares.js';

const T = () => RULES.game.fares;
for (const k in PLACES_F) {
  const p = PLACES_F[k];
  addPlace({ id: 'f_' + k, name: p.n, x: p.p[0], z: p.p[1], address: p.address, landmark: p.landmark, label: 'public' });
}

// the scripted driver (ER-DRIVE-09): he has only the legs Pauline's words are made from, and drives them
function waypoints(legs, lane = 1.9) {
  const pts = [];
  for (const l of legs) {
    const R = ROADS_F[l.road];
    // Britain drives on the left: the lane is to the left of the way he heads
    const off = l.heads === 'south' ? lane : l.heads === 'north' ? -lane : l.heads === 'east' ? -lane : lane;
    pts.push(R.axis === 'z' ? [R.at + off, l.to.z] : [l.to.x, R.at + off]);
  }
  return pts;
}

register({
  id: 'fares',
  fresh: freshFares,
  loaded(x) {
    const f = freshFares();
    for (const k in f) if (x[k] === undefined) x[k] = f[k];
  },
  carPrompts(out) {
    farePrompts(out);
  },
  key(code) {
    if (code === 'KeyR' && G.tom.inCar && G.story.fare && G.story.fare.st !== 'offer' && G.story.fare.ask !== 'open') return fareWayAgain();
    return false;
  },
  // the firm drives without him: Kevin by day and Terry by night put fares in the book whether he drives or not
  minute(t) {
    const s = X('fares'),
      h = hour();
    if (h >= 3 && h < 7) return;
    if (t % T().driverFareEveryGameMinutes === 0 && !(G.people[h >= 7 && h < 19 ? 'kevin' : 'terry'] || {}).dead) bookByDriver(T().driverFarePence);
    void s;
  },
  hook: {
    list: () => FARES.map((f) => ({ id: f.id, wrinkle: f.wrinkle, gives: f.gives, from: PLACES_F[f.from].n, to: PLACES_F[f.to].n, who: f.who || f.pax.desc })),
    places: () => PLACES_F,
    state: () => X('fares'),
    next: fareNext,
    // have Pauline call this fare now (Tom needs the keys)
    offer(id) {
      G.story.fare = null;
      fareOffer({ id });
      return G.story.fare ? { id: G.story.fare.id, state: G.story.fare.st, payPence: G.story.fare.pay } : null;
    },
    accept: fareAccept,
    hand: fareHand,
    answer: fareAnswer,
    wayAgain: fareWayAgain,
    way(placeKey, from) {
      const w = wayTo(placeKey, from);
      return { words: w.words, legs: w.legs, waypoints: waypoints(w.legs), metres: FR.fns.metres(w.legs) };
    },
    // A driver who has nothing but the way's legs. Puts the cab through them and says how near the door he ends.
    drive(placeKey, from) {
      const w = wayTo(placeKey, from),
        pts = waypoints(w.legs),
        end = pts[pts.length - 1],
        p = PLACES_F[placeKey].p;
      return { legs: w.legs.length, words: w.words, endsMetresFromTheDoor: Math.round(hyp(end[0], end[1], p[0], p[1]) * 10) / 10, waypoints: pts };
    },
    read() {
      const f = G.story.fare;
      return f ? { id: f.id || null, state: f.st, ask: f.ask || null, way: f.way || null, hurryLeft: f.hurry ?? null, payPence: f.pay, pid: f.pid || null } : null;
    },
    junctions: () => JUNCTIONS_F,
  },
});
