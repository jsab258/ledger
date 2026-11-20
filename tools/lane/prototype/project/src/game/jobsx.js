// LEDGER, the whole game: the system "jobsx". The job template in play (DESIGN 4; A17; parts 3.5.3, 3.5.4, 3.5.6,
// 3.5.7, 1.6.5, 3.3): every job is offered by a person on a state through a channel that names a place, has three
// keys, windows instead of minutes, failure that continues, a Ledger line a step, and a tester's skip. The rule is
// the piece pieces/jobs.js; the jobs themselves are written in tune/jobsx.js and checked against it when loaded.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on, PLACES, tomXZ } from './core.js';
import { G } from '../state.js';
import { hyp } from '../util.js';
import { act } from '../events.js';
import { earn } from '../money.js';
import { choose, scene, say } from '../ui.js';
import { RULES } from '../rules.js';
import { JOBS } from './tune/jobsx.js';
import { PIECE as JOB } from './pieces/jobs.js';
import { direct, goalDone } from './way.js';
import { startTail } from './foot.js';

const T = RULES.game.jobsx;
const J = JOB.fns;
const SPEC = Object.fromEntries(JOBS.map((j) => [j.id, j]));
// The spec as the piece reads it: each step's window is put on the town's clock when the step opens.
const forPiece = (s, job) => Object.assign({}, s, { steps: s.steps.map((st, i) => Object.assign({}, st, { window: job && job.windows && job.windows[i] ? job.windows[i] : undefined })) });
export const SPEC_FAULTS = JOBS.flatMap((s) => J.validate(Object.assign({}, s, { steps: s.steps.map((st) => Object.assign({}, st, { window: st.window ? { fromT: st.window.fromHour * 60, untilT: st.window.untilHour * 60 } : undefined })) })).map((f) => s.id + ': ' + f));

// The states that offer a job. Offered by a person, on a state, never by a marker or the clock alone (law 1).
const WHEN = {
  night2: () => dayNow() >= 1 && !!G.story.flags.tour,
  wayneOwes: () => dayNow() >= 1 && G.debts.wayne.st !== 'open' ,
  rung2: () => (G.x.rise ? G.x.rise.rung : 1) >= 2,
  julieFriend: () => G.debts.julie.st === 'forgiven',
  fencedOnce: () => G.x.crime.haggles.some((h) => h.done === 'sold'),
  otherFirmTaking: () => G.x.econ.fareShare < 1 || (G.x.firm && G.x.firm.otherFirmOnRank),
  adaTea: () => ['yes', 'late'].includes(G.story.flags.tea),
  metWalsh: () => !!G.ledger.met.walsh && dayNow() >= 2,
  metGrace: () => !!G.ledger.met.grace && dayNow() >= 1,
  metNorman: () => !!G.ledger.met.norman,
};
const openStep = (job) => (job.st === 'taken' ? SPEC[job.id].steps[job.step] : null);
function objective(job) {
  const st = openStep(job);
  if (!st) return;
  const p = PLACES[st.place];
  direct(st.place, P_(SPEC[job.id].giver) ? P_(SPEC[job.id].giver).def.name : 'the giver');
  G.story.objective = `${SPEC[job.id].name}: ${p ? p.name + ', ' : ''}${st.landmark}.`;
}
function apply(id, ev) {
  const x = X('jobsx'),
    job = x.jobs[id];
  if (!job) return null;
  const spec = SPEC[id];
  const r = J.advance(forPiece(spec, job), job, ev);
  const before = job.step,
    wasSt = job.st;
  Object.assign(job, r.job, { windows: job.windows, mindT: job.mindT });
  if (r.line) write(r.line, { key: 'job:' + id + ':' + job.lines.length, who: spec.giver, how: ev.what === 'take' ? 'Agreed it' : 'Did it' });
  if (job.st === 'taken' && (job.step !== before || wasSt !== 'taken')) {
    const st = spec.steps[job.step];
    if (st.window) {
      // windows, not minutes: the next window of at least two game hours on the town's clock
      const d = hourNow() < st.window.untilHour ? dayNow() : dayNow() + 1;
      job.windows[job.step] = { fromT: d * 1440 + st.window.fromHour * 60, untilT: d * 1440 + st.window.untilHour * 60 };
    }
    objective(job);
  }
  if (r.line && (ev.what === 'done' || ev.what === 'skip')) {
    const st = spec.steps[before];
    if (st.goods) G.x.crime.goods.push(Object.assign({ takenT: G.t, from: st.place }, st.goods));
    if (st.good) act('side_done', { target: spec.giver, what: spec.name, silent: true, told: [spec.giver] });
  }
  if (job.st === 'done' || job.st === 'failed') {
    goalDone();
    if (job.st === 'failed' && spec.family === 'side' && job.how !== 'refused') act('side_bad', { target: spec.giver, what: spec.name, silent: true, told: [spec.giver] });
    if (/job|hut|Rita|door|Coverdale|Portside|medals|lamp|lead|till|dog/.test(G.story.objective || '') && (G.story.objective || '').startsWith(spec.name)) G.story.objective = '';
    emit('jobs.ended', { id, st: job.st, how: job.how, family: spec.family });
  }
  return r;
}
// The offer: said by the giver, at the channel's place; taken or refused, each with its line (ER-JOB-05).
async function offer(spec) {
  const x = X('jobsx');
  x.jobs[spec.id] = Object.assign(J.start(spec, G.t), { windows: {}, mindT: 0 });
  const i = await scene(async () => {
    await say(spec.giver, spec.offer);
    return choose(spec.giver, spec.family === 'side' ? 'Would you?' : 'Well?', ['Yes.', 'No.']);
  });
  apply(spec.id, { what: i === 0 ? 'take' : 'refuse' });
  x.offered[spec.id] = Math.round(G.t);
}
// A message taken at the office when the giver cannot find him (A17): written down, naming the giver and the place.
function messages() {
  const x = X('jobsx');
  for (const spec of JOBS) {
    if (x.jobs[spec.id] || x.messaged[spec.id] || !WHEN[spec.when]()) continue;
    x.due[spec.id] = x.due[spec.id] || Math.round(G.t);
    if (G.t - x.due[spec.id] > 240) {
      x.messaged[spec.id] = Math.round(G.t);
      const giver = P_(spec.giver);
      write(`${spec.channel === 'a message' ? 'Sheila' : 'Pauline'} took a message: ${giver.def.name} wants a word, at ${spec.channelPlace}.`, { key: 'msg:' + spec.id, who: spec.giver, how: 'A message at the office' });
    }
  }
}
function stepWatch(dt) {
  const x = X('jobsx'),
    t = G.tom,
    [tx, tz] = tomXZ();
  for (const id in x.jobs) {
    const job = x.jobs[id];
    const st = openStep(job);
    if (!st) continue;
    const p = PLACES[st.place],
      at = p && (p.room ? t.space === p.room : false || hyp(tx, tz, p.x, p.z) < (st.mind ? T.mindingWithinMetres : T.stepWithinMetres));
    const w = job.windows[job.step];
    if (w && G.t > w.untilT) {
      apply(id, { what: 'clock', t: G.t });
      continue;
    }
    if (!at) continue;
    const timing = J.timing(w || null, G.t);
    if (timing.st === 'early') {
      if (!job.toldEarly) {
        job.toldEarly = true;
        tell('Too early. It can be waited for [Z].', '');
      }
      continue;
    }
    if (st.tail && !G.x.foot.tail && !job.tailed) {
      job.tailed = true;
      startTail(st.tail.id, st.tail.learns);
      tell('There she goes. Not close.', '');
    } else if (st.mind) {
      // minding (1.6.5): being seen at somebody's shoulder; the town's eyes record who stood with whom
      job.mindT = (job.mindT || 0) + (dt * 60) / RULES.time.realSecondsPerGameHour * (G.fast || 1);
      if (job.mindT >= st.mind.minutes) {
        const m = J.minding(job.mindT);
        act('minded', { target: st.mind.with, place: p.name });
        if (SPEC[id].family === 'minding' && m.pence) earn(m.pence, false, 'minding: ' + SPEC[id].name);
        apply(id, { what: 'done' });
      }
    } else if (st.near) apply(id, { what: 'done' });
  }
}

register({
  id: 'jobsx',
  fresh: () => ({ jobs: {}, offered: {}, messaged: {}, due: {} }),
  step(dt) {
    if (!G.paused) stepWatch(dt);
  },
  hourly() {
    messages();
  },
  // a job waiting with its giver is a written scene with that person (the first thing they say)
  beatFor(P) {
    const x = X('jobsx');
    const spec = JOBS.find((s) => s.giver === P.id && !x.jobs[s.id] && WHEN[s.when]());
    return spec ? () => offer(spec) : null;
  },
  hook: {
    x: () => X('jobsx'),
    specs: () => JOBS.map((s) => ({ id: s.id, family: s.family, giver: s.giver, channel: s.channel, channelPlace: s.channelPlace, approaches: s.approaches.length, steps: s.steps.length })),
    specFaults: () => SPEC_FAULTS,
    when: (id) => WHEN[SPEC[id].when](),
    offer: (id) => offer(SPEC[id]),
    start: (id) => {
      X('jobsx').jobs[id] = Object.assign(J.start(SPEC[id], G.t), { windows: {}, mindT: 0 });
      return apply(id, { what: 'take' });
    },
    event: (id, ev) => apply(id, ev),
    skip: (id) => apply(id, { what: 'skip' }), // the tester's skip (ER-JOB-07)
    job: (id) => X('jobsx').jobs[id],
  },
});
// what the hands did reaches the job that was waiting on it
const evDone = (name) => {
  const x = X('jobsx');
  for (const id in x.jobs) {
    const st = openStep(x.jobs[id]);
    if (st && st.ev === name) apply(id, { what: 'done' });
  }
};
on('crime.entered', (e) => evDone('crime.entered:' + (e.site === 'ritaside' ? 'rita' : e.site)));
on('crime.found', (e) => evDone('crime.found:' + e.site + ':' + e.c));
on('crime.damage', (e) => evDone('crime.damage:' + e.place));
on('foot.tail', (e) => evDone('foot.tail:' + e.id + ':' + e.ended));
