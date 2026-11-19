// LEDGER. The night jobs: the bag, the parcel, the scrapyard. Where the drop doors are and what they pay.
import { G, day, hour } from './state.js';
import { money, quid } from './util.js';
import { act, seed, logLine } from './events.js';
import { statements } from './police.js';
import { note, meet } from './ledger.js';
import { KINDS } from './kinds.js';
import { SPOTS, ROOMS, zoneAt } from './map.js';
import { sub, say, scene, $ } from './ui.js';
import { fl, tomAt } from './work.js';
import { hyp } from './util.js';
import { sense, tomTarget } from './seeing.js';
import { goToPoint } from './routines.js';
import { pay, earn } from './money.js';
import { RULES } from './rules.js';

const JOB = RULES.jobs;

// ---------- night jobs ----------
export const JOBS = {
  1: {
    name: 'the Monday bag',
    from: 'shelter',
    fromZ: 'the ferry landing',
    to: 'coinback',
    toZ: "Metcalfe's back door",
    pay: JOB.mondayBagPayPence,
    after: JOB.mondayBagFromHour,
  },
  2: {
    name: 'the Tuesday parcel',
    from: 'smoke1',
    fromZ: 'the smoke house door',
    to: 'ritaside',
    toZ: "Rita's side door",
    pay: JOB.tuesdayParcelPayPence,
    after: JOB.tuesdayParcelFromHour,
  },
};

export function startJob(n) {
  G.story.job = { n, st: 'pickup', day: day() };
}

export function jobHotspots(out) {
  const j = G.story.job,
    t = G.tom;
  if (!j || j.st === 'done' || t.inCar) return;
  const J = JOBS[j.n];
  if (!J) return;
  const h = hour(),
    ready = h >= J.after || h < JOB.doorsShutAtHour;
  if (j.st === 'pickup') {
    const s = SPOTS[J.from];
    if (tomAt(s[0], s[1], JOB.pickUpWithinMetres) && ready)
      out.push({
        k: 'E',
        t: 'Take the holdall',
        run: () => {
          j.st = 'carry';
          j.carrying = true;
          t.carry = 'bag';
          act('pickup', { zone: J.fromZ });
          startBeat(j, J);
          sub(
            j.n === 1
              ? 'A cheap holdall under the bench. Heavier than it looks.'
              : 'A parcel in sacking behind the door. Tied tight, and heavier than it looks.',
            '',
            'over',
          );
        },
      });
  } else if (j.st === 'carry') {
    const s = SPOTS[J.to];
    if (tomAt(s[0], s[1], JOB.dropWithinMetres)) out.push({ k: 'E', t: 'Knock', run: () => deliver(j, J) });
  }
}

async function deliver(j, J) {
  const t = G.tom,
    who = j.n === 1 ? 'hal' : 'wayne';
  const dropped = act('drop', { zone: J.toZ, told: [who], noiseR: JOB.knockNoiseMetres });
  t.carry = null;
  endBeat(j, null);
  j.st = 'done';
  j.carrying = false;
  earn(J.pay, true);
  fl()['job' + j.n] = 'done';
  await scene(async () => {
    if (j.n === 1) {
      await say('hal', "You're not Mickey.");
      await say(
        'hal',
        t.coat ? 'Coat fits, though.' : "No coat. He always wore the coat. Somebody'll have seen your face.",
      );
      await say('hal', 'Sixty. Count it somewhere else.');
    } else {
      await say('wayne', "Nice one. Rita's not to know I was stood here, you following?");
      await say('wayne', "Forty. And if you ever need something that isn't in the window, ask.");
    }
  });
  meet(G.people[who]);
  note(`${quid(J.pay)} in the tin for ${J.name}.`, 'money', null, { how: 'Counted it', ev: dropped.id });
}

export function jobClock() {
  // not turning up is an answer as well
  const st = G.story,
    j = st.job;
  if (!j || j.st === 'done' || j.st === 'missed' || j.st === 'lost') return;
  if (
    JOBS[j.n] &&
    day() > j.day &&
    hour() >= JOB.missedFromHourNextDay &&
    hour() < JOB.missedUntilHourNextDay
  ) {
    if (j.st === 'carry') {
      G.tom.carry = null;
      fl().keptBag = 1;
    }
    j.st = 'missed';
    fl()['job' + j.n] = 'noshow';
    seed('no_show', ['ron', j.n === 1 ? 'hal' : 'wayne']);
    logLine('Tom never turned up for ' + JOBS[j.n].name, 'job');
  }
}

// ---------- the carry under watch (lane round 2, 18 Nov) ----------
// The night carry is no longer a walk: a constable walks his beat between the pick-up and the drop. He sees
// by the town's own eyes (light, line of sight, where he faces), so Ron's advice holds: keep out from under
// the lamps, wait for him to turn. Seen with the bag, he calls out: stand and be searched (the bag is taken,
// he has your face), or run (a chase; out of his sight long enough and he gives up).
const W = RULES.jobs;
const beatPts = (J) => {
  const a = SPOTS[J.from],
    b = SPOTS[J.to],
    f = W.beatStartsAlongTheWayFraction;
  return [
    [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f],
    [b[0] + (a[0] - b[0]) * W.beatEndsShortOfTheDropFraction, b[1] + (a[1] - b[1]) * W.beatEndsShortOfTheDropFraction],
  ];
};
export function startBeat(j, J) {
  if (G.story.arrest && !G.story.arrest.violent) return; // the constable is already about something else
  const P = G.people.pc;
  if (!P || P.dead) return;
  const pts = beatPts(J);
  j.watch = { st: 'beat', leg: 1, t: 0, lost: 0, ct: 0, seenAt: null };
  P.override = null;
  P.gone = false;
  P.space = 'street';
  P.awake = true;
  P.x = pts[0][0];
  P.z = pts[0][1];
  P.route = null;
  goToPoint(P, pts[1][0], pts[1][1], W.beatWalkMetresPerSecond);
  logLine('A constable walked his beat between ' + J.fromZ + ' and ' + J.toZ, 'police');
  sub(
    'Footsteps on the wet. A constable is walking his beat along your way. Keep out of the light.',
    '',
    'over',
    W.subtitleRealSeconds,
  );
}
function endBeat(j, how) {
  const w = j.watch;
  if (!w || w.st === 'over') return;
  w.st = 'over';
  w.how = how || 'job over';
  const P = G.people.pc;
  if (!P) return;
  P.mark = null;
  P.hurry = 1;
  P.hold = false;
  P.override = { where: 'off', act: 'idle' };
  P.goalKey = '';
}
export function watchStep(dt) {
  const j = G.story.job;
  if (!j || !j.watch || j.watch.st === 'over' || G.paused) return;
  const w = j.watch,
    J = JOBS[j.n],
    P = G.people.pc,
    t = G.tom;
  if (!P || P.dead || P.gone || (G.story.arrest && !G.story.arrest.violent)) return endBeat(j, 'called away');
  if (j.st !== 'carry') return endBeat(j, w.st === 'search' ? w.how : 'job over'); // a save made mid-search
  w.t += dt;
  // where he would look for Tom: on foot, the cab, or the street door of the room he went into (as policeStep)
  const tx = t.space === 'street' ? (t.inCar ? G.car.x : t.x) : ROOMS[t.space] ? ROOMS[t.space].street[0] : t.x,
    tz = t.space === 'street' ? (t.inCar ? G.car.z : t.z) : ROOMS[t.space] ? ROOMS[t.space].street[1] : t.z;
  const d = hyp(P.x, P.z, tx, tz),
    seeable = t.space === 'street';
  if (w.st === 'beat') {
    if (w.t > W.beatLastsAtMostRealSeconds) return endBeat(j, 'beat over');
    // back and forth along the way
    const pts = beatPts(J),
      to = pts[w.leg];
    if (hyp(P.x, P.z, to[0], to[1]) < W.beatTurnsWithinMetres) {
      w.leg = 1 - w.leg;
      const nx = pts[w.leg];
      goToPoint(P, nx[0], nx[1], W.beatWalkMetresPerSecond);
    } else if (!P.route) goToPoint(P, to[0], to[1], W.beatWalkMetresPerSecond); // stopped short: walk on
    const s = t.carry && !t.inCar ? sense(P, tomTarget()) : { see: false };
    if (s.see && d < W.challengesWithinMetres) {
      w.st = 'challenge';
      w.ct = 0;
      w.seenAt = { x: t.x, z: t.z, c: s.c };
      P.mark = '!';
      P.ang = Math.atan2(t.x - P.x, t.z - P.z);
      goToPoint(P, t.x, t.z, W.beatWalkMetresPerSecond);
      sub('"You. With the bag. Stop there a minute." Stand and let him look, or run [Shift].', 'PC Ibbotson', 'over', W.subtitleRealSeconds);
      logLine('The constable called out to Tom with the bag', 'police');
    }
    return;
  }
  if (w.st === 'challenge') {
    w.ct += dt;
    if (w.ct > W.challengeHoldsRealSeconds) {
      w.ct2 = (w.ct2 || 0) + dt;
      if (w.ct2 > W.challengeFollowsEveryRealSeconds) {
        w.ct2 = 0;
        goToPoint(P, t.x, t.z, W.beatWalkMetresPerSecond);
      }
    }
    const moved = w.seenAt ? hyp(tx, tz, w.seenAt.x, w.seenAt.z) : 0;
    if (d < W.searchesWithinMetres && seeable && !t.inCar) return caught(j, J, P, false);
    if (w.ct > W.challengeLastsAtMostRealSeconds || !seeable || t.inCar || t.run || moved > W.startsChaseWhenTomMovesMetres || d > W.challengesWithinMetres + W.chaseIfFurtherByMetres) {
      w.st = 'chase';
      w.ct = 0;
      w.lost = 0;
      w.look = 0;
      sub('"Oi! Stop!" A whistle behind you.', 'PC Ibbotson', 'over', W.subtitleRealSeconds);
      logLine('Tom ran from the constable with the bag', 'police');
      t.noiseP = Math.max(t.noiseP, RULES.police.runningNoiseMetres);
    }
    return;
  }
  if (w.st === 'chase') {
    w.ct += dt;
    w.look -= dt;
    const los = seeable && d < RULES.police.seesHimWithinMetres && G.env.los(P.x, P.z, tx, tz);
    w.lost = los ? 0 : w.lost + dt;
    if (w.look <= 0) {
      w.look = RULES.police.looksAgainWhenChasingEveryRealSeconds;
      if (los) goToPoint(P, tx, tz, RULES.police.chasingMetresPerSecond);
    }
    if (d < RULES.police.catchesWithinMetres && seeable && !t.inCar) return caught(j, J, P, true);
    if (
      w.lost > RULES.police.losesHimAfterRealSecondsUnseen ||
      d > RULES.police.losesHimBeyondMetres ||
      w.ct > RULES.police.chaseLastsAtMostRealSeconds
    ) {
      act('ran_police', { zone: zoneAt(t.x, t.z), noiseR: RULES.police.runningNoiseMetres });
      fl().ranBeat = (fl().ranBeat || 0) + 1;
      endBeat(j, 'lost him');
      sub('You have lost him. He saw a man with a bag. Whether he saw your face, you will find out.', '', 'over', W.subtitleRealSeconds);
      note('Ran from a constable with the bag on ' + zoneAt(t.x, t.z) + '. Lost him.', 'police', null, { how: 'Did it' });
    }
  }
}
async function caught(j, J, P, ran) {
  const t = G.tom,
    w = j.watch;
  const E = act('bag_taken', { zone: zoneAt(t.x, t.z), what: J.name, told: ['pc'], noiseR: ran ? RULES.police.runningNoiseMetres : 0 });
  t.carry = null;
  j.carrying = false;
  j.st = 'lost';
  fl()['job' + j.n] = 'lost';
  w.st = 'search';
  w.how = ran ? 'caught running' : 'searched';
  P.route = null;
  P.hold = true;
  await scene(async () => {
    await say('pc', ran ? 'Nobody runs from me with an empty bag. Let\'s see it.' : "Let's have a look, then.");
    await say(
      'pc',
      j.n === 1
        ? "Well. That's not your washing. I'll keep this. Name? I'll be writing it down, son."
        : "Heavy, for a parcel. I'll keep this. Name? I'll be writing it down, son.",
    );
  });
  endBeat(j, w.how);
  note(`The constable took ${J.name} on the way to ${J.toZ}. He wrote the name down.`, 'police', null, {
    how: 'Did it',
    ev: E.id,
  });
}
