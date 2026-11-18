// LEDGER. The working day: passing time, sleep, being beaten, and the one step that runs fares, jobs and police.
import { G, day, hour, SECS_PER_HOUR, pausedWhile } from './state.js';
import { hyp, money, quid } from './util.js';
import { seed } from './events.js';
import { RULES } from './rules.js';

const REST = RULES.rest,
  BEAT = RULES.beaten;

import { note, meet, learnName } from './ledger.js';

import { simStep } from './clock.js';
import { placeAll } from './routines.js';
import { ROOMS, roomPos } from './map.js';
import { say, choose, scene, fade, $ } from './ui.js';
import { setInside } from './render/effects.js';
import { fareStep } from './fares.js';
import { policeStep, ellisStep } from './police.js';

export const fl = () => G.story.flags;

export const tomAt = (x, z, r = 2) => hyp(G.tom.x, G.tom.z, x, z) < r;

// ---------- passing the time ----------
export function advanceTo(tEnd, hidden = true) {
  const t = G.tom,
    sp = t.space;
  if (hidden) t.space = 'away';
  let guard = 0;
  while (G.t < tEnd && guard++ < 30000) {
    simStep(Math.min(RULES.ticking.longestSleepStepRealSeconds, ((tEnd - G.t) * SECS_PER_HOUR) / 60 + 0.01));
    if (G.hooks.clock) G.hooks.clock();
  }
  t.space = sp;
}

export async function rest(where) {
  const h = hour(),
    d = day(),
    opts = [],
    T = [];
  const add = (label, t) => {
    opts.push(label);
    T.push(t);
  };
  const night = h < REST.nightCountsUntilHour;
  const morning = (night ? d : d + 1) * 1440 + REST.morningAtHour * 60;
  if (!night && h < REST.eveningOfferedUntilHour)
    add("Rest till this evening, six o'clock.", d * 1440 + REST.eveningAtHour * 60);
  if (!night && h < REST.ferryOfferedUntilHour)
    add('Wait for the last ferry, quarter past ten.', d * 1440 + REST.lastFerryAtHour * 60);
  add(!night && h < 19 ? 'Sleep through to the morning.' : 'Sleep till morning.', morning);
  opts.push('Not now.');
  const i = await scene(() =>
    choose(
      '',
      where === 'bed'
        ? 'Your room at Regent House. One suitcase, one bed, a sink.'
        : 'The cot in the back room. Mickey slept here more nights than not.',
      opts,
    ),
  );
  if (i >= T.length) return;
  await passTime(T[i], T[i] === morning ? 'Morning comes up grey over the Humber.' : '');
}

export async function passTime(tEnd, text = '') {
  await pausedWhile('passing time', async () => {
    await fade(true, text);
    const before = day();
    advanceTo(tEnd);
    if (day() !== before || hour() < 9) wake();
    G.tom.still = 0;
    if (G.hooks.save) G.hooks.save();
    await fade(false);
  });
}

function wake() {
  const t = G.tom;
  t.hurt = Math.max(0, t.hurt - REST.sleepHealsHurtBy);
  t.puff = 0;
  G.story.lastSleepDay = day();
  if (t.space === 'boarding') fl().unpacked = 1;
}

// ---------- beaten down: Grace's kitchen ----------
export async function beaten(foes) {
  await pausedWhile("beaten: Grace's kitchen", async () => {
    const t = G.tom,
      m = G.money;
    const lost = t.carry === 'bag';
    if (lost) {
      t.carry = null;
      if (G.story.job) {
        G.story.job.st = 'missed';
        G.story.job.carrying = false;
        fl()['job' + G.story.job.n] = 'lost';
      }
    }
    const took = Math.round(m.dirty * BEAT.shareOfTheTinTaken);
    m.dirty -= took;
    await fade(true, 'The pavement comes up to meet you.\n\nSomebody gets an arm under yours.');
    const h = hour(),
      early = h < BEAT.nightBeforeHour,
      late = h > BEAT.nightAfterHour;
    const next =
      (late ? day() + 1 : day()) * 1440 +
      (early || late ? BEAT.comesRoundAtHour : h + BEAT.outForGameHoursByDay) * 60;
    advanceTo(Math.max(next, G.t + BEAT.outForAtLeastGameMinutes));
    const [x, z] = roomPos('caff', ...ROOMS.caff.spots.kitchen);
    t.space = 'caff';
    t.x = x;
    t.z = z;
    t.ang = 3.14;
    t.hurt = BEAT.hurtAfterwards;
    t.inCar = false;
    setInside(ROOMS.caff);
    placeAll();
    const cost = Math.min(m.clean, BEAT.plastersPence);
    m.clean -= cost;
    m.spent += cost;
    const patched = seed('patched', ['grace']);
    meet(G.people.grace);
    await fade(false);
    learnName('grace');
    await scene(async () => {
      await say('grace', "Sit down before you fall down. Tea's on.");
      await say('grace', "I've seen worse come off a trawler. Not much worse. Hold that on your eye.");
      await say(
        'grace',
        (lost ? "There was no bag with you, if you're looking for one. " : '') +
          (took ? 'And your pockets were lighter than they should be. ' : '') +
          'Leave something on the counter for the plasters. Then go out the front like a customer.',
      );
    });
    note(
      `Came round in Grace Rinaldi's kitchen. ${quid(cost)} for plasters${took ? ', ' + quid(took) + ' gone from the tin' : ''}. The breakfast tables saw.`,
      'hurt',
      null,
      { who: 'grace', ev: patched.id },
    );
    if (G.hooks.save) G.hooks.save();
  });
}

export function workStep(dt) {
  fareStep(dt);
  policeStep(dt);
  ellisStep(dt);
}
