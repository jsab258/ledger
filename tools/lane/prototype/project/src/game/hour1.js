// LEDGER, the whole game: the system "hour1". The first hour as staged (ONE-SHOT-PROMPT, section 4): hands first, and
// the speeches spread across the things they are about. This file holds the staging only: who says what in passing,
// Sheila's walk-round at the things themselves, the stair to the flat. Every later beat of the hour belongs to the
// system that owns it (fares, econ, law, crime); this one hands on to them by state.
import { register, X, write, P_, hourNow, dayNow } from './core.js';
import { G } from '../state.js';
import { sub, ui } from '../ui.js';
import { RULES } from '../rules.js';
import { ROOMS, roomPos } from '../map.js';
import { meet, hearName, heardNames, learnName } from '../ledger.js';
import { hyp, angDiff } from '../util.js';
import { enterRoom } from '../player.js';
import { send, release, placeAll } from '../routines.js';
import { hint } from './feel.js';
import { fareOffer, fareAccept } from '../fares.js';
import { FARES } from './tune/fares.js';

const T = RULES.game.hour1;
const fl = () => G.story.flags;

// ---- 1:30 Quay Street: each a line in passing, said once, the first time he comes near in sight ----
const PASSING = {
  darren: { who: 'Darren Milner', line: "You'll be the nephew. Darren Milner. One suitcase, I said to Ron, that'll be him.", flag: 'metDarren' },
  ron: { who: 'Ron Kirby', line: "Afternoon, boss. Ron Kirby. I do the door and the rank, same as I did for Mickey.", flag: 'metRon' },
  ada: { who: 'A woman at a window', line: "So you're what he left it to. Well. You've his walk.", flag: 'metAda', window: true },
  june: { who: 'June Suddaby', line: "You're the nephew. June Suddaby, his daughter. I want nothing out of that office, so don't look worried.", flag: 'metJune' },
};
const STAGED = { darren: 'pave', ron: 'rank', june: 'junepass', walsh: 'infirmary' }; // (Father Walsh is visiting at the Infirmary until his fare is driven)
const posOf = (P) => (P.space === 'home' && P.win ? [P.win.x, P.win.z] : [P.x, P.z]);
function passing(x) {
  const t = G.tom;
  {
    const W = P_('walsh');
    if (W && W.override && W.override.where === 'infirmary' && (G.money.fareCount > 0 || dayNow() > 0)) release(W);
  }
  for (const id of ['ron', 'june']) { // (Darren is held on the pavement by the debt book's own rule: game/book.js)
    const P = P_(id);
    if (P && P.override && P.override.where === STAGED[id] && (x.round > 6 || G.t > RULES.time.weekStartsGameMinute + T.stagingEndsAfterGameMinutes)) release(P);
  }
  if (t.space !== 'street' || t.inCar) return;
  for (const id in PASSING) {
    if (x.passed[id]) continue;
    const P = P_(id),
      d = PASSING[id];
    if (!P || P.gone || P.dead) continue;
    if (!(P.space === 'street' || (d.window && P.space === 'home' && P.win))) continue;
    const [px, pz] = posOf(P);
    if (hyp(px, pz, t.x, t.z) > T.passingLineWithinMetres) continue;
    if (P.space === 'street' && G.env && G.env.los && !G.env.los(t.x, t.z, px, pz)) continue;
    x.passed[id] = Math.round(G.played * 10) / 10;
    x.passedT = x.passedT || {};
    x.passedT[id] = G.t;
    meet(P);
    fl()[d.flag] = 1;
    P.mind.look = Math.max(P.mind.look || 0, T.headTurnLastsRealSeconds + 1.5);
    hearName(P, d.line); // he has the name once they have said it
    if (heardNames()[P.id]) learnName(P.id);
    sub(d.line, d.who, 'face', 6);
    write(d.who + ' spoke to him as he came up Quay Street: "' + d.line + '"', { key: 'passing-' + id, who: id, how: 'said to his face' });
    return; // one at a time: no two lines on top of each other
  }
}
// 0:20 people on the quay look: a head turns as he passes (the figure's head follows mind.look)
function headsTurn(x) {
  const t = G.tom;
  if (t.space !== 'street' || t.inCar || x.round > 0) return;
  for (const P of G.named.concat(G.crowd)) {
    if (P.gone || P.dead || P.space !== 'street' || x.turned[P.id]) continue;
    if (hyp(P.x, P.z, t.x, t.z) > T.headsTurnWithinMetres) continue;
    if (G.env && G.env.los && !G.env.los(t.x, t.z, P.x, P.z)) continue;
    x.turned[P.id] = 1;
    P.mind.look = Math.max(P.mind.look || 0, T.headTurnLastsRealSeconds);
  }
}

// ---- 1:45 Sheila's walk-round: six lines, each said at the thing it is about, walking with him ----
// Places in the office's own metres. She walks to the thing, waits there for him, says its line when he is beside her.
const ROUND = [
  { at: [1.6, 0.6], thing: 'the counter', line: "You'll be the nephew. Sheila Dunn. I kept your uncle's books thirty-one years. Come round, I'll show you what he left." },
  { at: [3.4, -0.8], thing: 'the fare book', line: "The fare book. Every fare Pauline calls goes in it. That's the clean money, such as it is." },
  { at: [5.7, -2.3], thing: "the locked door of Mickey's inner office", line: "That door stays shut. His own office. You'll see inside when I've decided what you are." },
  { at: [4.4, 2.5], thing: 'the stair to the flat', line: "The flat's up there, his things still in it. Yours now. The rent on all of it is eighteen pounds, Friday." },
  { at: [5.3, 0.9], thing: 'the yard door', line: "The yard, through there. Two ways out of this building. Your uncle liked a choice." },
  { at: [-1.7, -1.2], thing: 'the radio', line: "The radio. Nobody in this building can help overhearing it. Remember that before you say anything near it." },
];
const DOORWAY = [0.5, 1.5]; // the gap in the partition between the front office and the back room, in the office's own metres
const PAULINE_FARE = "I've Father Walsh wanting the priest's house, by the chapel, and no car in. Car two's on the rank, love. Keys are on the hook.";
// Walk somebody across the office to a place in its own metres, by the doorway in the partition. True when there.
export function walkInOffice(S, at, dt) {
  const r = ROOMS.mickeys;
  const sideNow = S.x - r.ox < DOORWAY[0] ? -1 : 1,
    sideGoal = at[0] < DOORWAY[0] ? -1 : 1,
    via = sideNow !== sideGoal ? [DOORWAY[0] + sideGoal * 0.5, DOORWAY[1]] : at;
  if (sideNow !== sideGoal && Math.abs(S.z - r.oz - DOORWAY[1]) > 0.5) via[0] = DOORWAY[0] + sideNow * 0.7; // first to the doorway on her own side
  const [gx, gz] = roomPos('mickeys', via[0], via[1]),
    d = hyp(S.x, S.z, gx, gz);
  if (via !== at && d <= 0.15) {
    S.x += sideGoal * 0.2; // through the doorway
    return false;
  }
  if (d > 0.15) {
    const step = Math.min(d, T.sheilaWalksMetresPerSecond * dt);
    S.ang = Math.atan2(gx - S.x, gz - S.z);
    S.x += ((gx - S.x) / d) * step;
    S.z += ((gz - S.z) / d) * step;
    S.moving = true;
    S.act = 'walk';
    return false;
  }
  S.moving = false;
  S.act = 'idle';
  return true;
}
function walkRound(x, dt) {
  const t = G.tom,
    S = P_('sheila');
  if (!S || S.dead) return;
  if (x.round === 0) {
    // it begins the moment he first walks into the office with her in it
    if (t.space !== 'mickeys' || S.space !== 'mickeys') return;
    x.round = 1;
    x.said = 0;
    meet(S);
    release(S); // nothing else places her while she shows him round
  }
  if (x.round > ROUND.length) return;
  if (t.space !== 'mickeys') return; // she waits where she is while he is out
  S.busy = true; // hers to walk while the round lasts (her routine takes her back after)
  const stop = ROUND[x.round - 1];
  if (!walkInOffice(S, stop.at, dt)) return;
  S.ang += angDiff(S.ang, Math.atan2(t.x - S.x, t.z - S.z)) * Math.min(1, dt * 6);
  x.waitT = x.said < x.round ? (x.waitT || 0) + dt : 0;
  if (x.said < x.round && (x.round === 1 || x.waitT > T.sheilaCallsHimOnAfterRealSeconds || hyp(S.x, S.z, t.x, t.z) <= T.sheilaSpeaksWhenHeIsWithinMetres) && !ui.modal && !ui.subs.some((s) => s.t > s.secs - 1.2)) {
    x.waitT = 0;
    x.said = x.round;
    x.saidAt = G.played;
    sub(stop.line, 'Sheila Dunn', 'face', 6.5);
    write('Sheila Dunn, at ' + stop.thing + ': "' + stop.line + '"', { key: 'round-' + x.round, who: 'sheila', how: 'said to his face' });
  } else if (x.said === x.round && G.played - x.saidAt > 3.2) {
    x.round++;
    if (x.round > ROUND.length) endOfRound(x, S);
  }
}
function endOfRound(x, S) {
  S.busy = false;
  S.goalKey = null;
  send(S, 'mickeys:sheila', 'work'); // she sits on at her desk on the first night until she has shown him the debt book (game/book.js)
  fl().tour = 1;
  fl().unpacked = 1;
  fl().metPauline = 1;
  const Pa = P_('pauline');
  if (Pa) meet(Pa);
  G.car.keys = true;
  if (G.tom.carry === 'suitcase') G.tom.carry = null;
  sub(PAULINE_FARE, 'Pauline Kitching, at the radio', 'face', 8);
  if (G.hooks.sfx) G.hooks.sfx('radio');
  write("Pauline Kitching has a fare and no car: Father Walsh, for the priest's house by the chapel. Car two is on the rank outside Mickey's; its keys were on the hook.", { key: 'first-fare-offered', who: 'pauline', how: 'said to his face' });
  G.story.objective = "Car two is on the rank outside Mickey's. Father Walsh wants the priest's house, by the chapel.";
  X('feel').firstFareSaid = true;
  G.story.fareCool = 0;
}

register({
  id: 'hour1',
  fresh: () => ({ passed: {}, turned: {}, round: 0, said: 0, saidAt: 0 }),
  loaded(x) {
    // the first hour's people stand where the staging has them on the Monday afternoon (their routines take over after)
    if (dayNow() === 0 && hourNow() < 17 && G.t < RULES.time.weekStartsGameMinute + 5 && !x.staged) {
      x.staged = 1;
      for (const id in STAGED) if (P_(id)) send(P_(id), STAGED[id], 'idle');
      placeAll(); // they are standing there when the ferry comes in
      fl().metSylvia = 1; // Regent House is not his: the flat over the office is
    }
  },
  step(dt) {
    if (G.paused || G.story.phase !== 'play') return;
    const x = X('hour1');
    if (dayNow() === 0) {
      headsTurn(x);
      passing(x);
      // standing still on the quay before he has found the street: the way, by its landmark, once
      if (!x.round && G.tom.space === 'street' && G.tom.still > RULES.game.feel.hintAfterStandingStillRealSeconds && G.tom.z > 44) hint('way', 'Quay Street is up the quay to the east, past the Harbour Office clock. Mickey\'s is at the quay end, under the blue sign.');
    }
    walkRound(x, dt);
    // 2:30 the first verb with the hands: he sits in car two and the fare Pauline gave at the radio is his
    if (G.tom.inCar && x.round > ROUND.length && !x.fare1 && G.hooks.fareNext) {
      if (!G.story.fare) {
        const nx = G.hooks.fareNext();
        if (nx) fareOffer(nx, true);
      }
      const f = G.story.fare;
      if (f && f.st === 'offer') {
        x.fare1 = Math.round(G.played * 10) / 10;
        fl().firstFare = 1;
        fareAccept();
        const F_ = FARES.find((q) => q.id === f.id);
        if (f.who) learnName(f.who); // Pauline has said who it is
        sub((F_ && F_.toPickUp) || 'He is waiting, love.', 'Pauline, on the radio', 'face', 10);
        if (G.hooks.sfx) G.hooks.sfx('radio');
      }
    }
  },
  hotspots(out) {
    const t = G.tom;
    if (t.space === 'mickeys') {
      const st = ROOMS.flat.stair,
        [sx, sz] = roomPos('mickeys', st[0], st[1]);
      if (hyp(t.x, t.z, sx, sz) < T.thingWithinMetres)
        out.push({
          k: 'E',
          t: 'Up the stair to the flat',
          run: () => {
            enterRoom('flat', true);
            if (G.hooks.sfx) G.hooks.sfx('stair');
          },
        });
    }
  },
  matters(P, a) {
    const x = X('hour1');
    if (P.id === 'june' && !x.june)
      a.push({
        key: 'juneQuiet',
        direct: true,
        ask: "whether to keep it to himself that June has been by",
        raise: "One thing. If Sheila asks, you never saw me on this street. Will you do that?",
        opts: [
          {
            agree: 1,
            q: "You never saw me. Yes or no?",
            yes: ['Yes. I never saw you.', 'Yes.'],
            no: ['No.', "No. I won't lie to her."],
            keep: ['Why would she ask?', 'What is it between you two?'],
            keepSay: "Thirty-one years of her knowing best, that's what. Yes or no?",
            noSay: "Please yourself. You're his nephew all right.",
            take: () => {
              x.june = 'yes';
              write('Promised June Suddaby: if Sheila asks, he never saw June on Quay Street.', { kind: 'promise', key: 'june-quiet', who: 'june', how: 'said to her face' });
              return "Good. That's the only thing I'll ever ask of that office.";
            },
          },
        ],
      });
  },
  hook: { x: () => X('hour1'), round: ROUND, passing: PASSING },
});
