// LEDGER. The night jobs: the bag, the parcel, the scrapyard. Where the drop doors are and what they pay.
import { G, day, hour } from './state.js';
import { money, quid } from './util.js';
import { act, seed, logLine } from './events.js';
import { statements } from './police.js';
import { note, meet } from './ledger.js';
import { KINDS } from './kinds.js';
import { SPOTS } from './map.js';
import { sub, say, scene, $ } from './ui.js';
import { fl, tomAt } from './work.js';
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
          sub(
            j.n === 1
              ? 'A cheap holdall under the bench. Heavier than it looks.'
              : 'A parcel in sacking behind the door. It clinks.',
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
  if (!j || j.st === 'done' || j.st === 'missed') return;
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
