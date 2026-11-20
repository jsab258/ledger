// LEDGER rule piece: the job template (DESIGN 4; parts 3.5.6, 3.5.7). Pure: plain data in, plain data out.
// A job is a small graph of saved states. Four job states and five step states; every change is a new run object
// the game saves. Nothing here knows the clock but the minute handed in, and nothing is rolled.
//
// A spec (authored, never rolled):
//   { id, name, family, setPiece, giver, channel: { kind, place }, offer, pay: { pence, dirty },
//     approaches: [ { id, needsTalk, needsFight, needsCar } ],            (law 2: three keys to every lock)
//     steps: [ { id, verb, place, who: [ids], act, window: { fromHour, untilHour }, lastDayOffset,
//                directions: [ 'the giver', 'the Ledger', ... ],            (ER-JOB-02: two or more)
//                outcomes: { name: { line, next, fail } } } ] }             (next: a step id, 'done' or 'failed')
// A run: { id, st, takenAt, endedAt, outcome, cur, steps: { stepId: { st, outcome, at } }, lines: [ { t, step, line } ] }
export const JOB_STATES = ['offered', 'taken', 'done', 'failed'];
export const STEP_STATES = ['asleep', 'open', 'done', 'failed', 'skipped'];
export const CHANNELS = ['counter', 'street', 'message', 'phone', 'car'];
const words = (s) => String(s).trim().split(/\s+/).filter(Boolean).length;
const copy = (o) => JSON.parse(JSON.stringify(o));
const stepOf = (spec, id) => spec.steps.find((s) => s.id === id);

function newRun(spec, t) {
  const steps = {};
  for (const s of spec.steps) steps[s.id] = { st: 'asleep', outcome: null, at: null };
  return { id: spec.id, st: 'offered', offeredAt: t, takenAt: null, endedAt: null, outcome: null, cur: null, steps, lines: [] };
}
// Taking a job opens its first step. Refusing ends it as failed with the outcome 'refused' (law 4: failure continues).
function take(run, spec, t) {
  const r = copy(run);
  if (r.st !== 'offered') return { run: r, ok: false, why: 'not on offer' };
  r.st = 'taken';
  r.takenAt = t;
  r.cur = spec.steps[0].id;
  r.steps[r.cur] = { st: 'open', outcome: null, at: t };
  return { run: r, ok: true, events: [{ name: 'job:step', job: r.id, step: r.cur, state: 'open' }] };
}
function refuse(run, spec, t, line) {
  const r = copy(run);
  if (r.st !== 'offered') return { run: r, ok: false, why: 'not on offer' };
  r.st = 'failed';
  r.outcome = 'refused';
  r.endedAt = t;
  r.lines.push({ t, step: null, line: line || 'Said no to ' + spec.name + '. It will be passed on, and somebody will count it.' });
  return { run: r, ok: true, events: [{ name: 'job:end', job: r.id, outcome: 'refused' }] };
}
// A step ends one of its authored ways. The line goes in the Ledger; the next step opens, or the job ends.
function resolve(run, spec, stepId, outcome, t) {
  const r = copy(run),
    S = stepOf(spec, stepId);
  if (r.st !== 'taken') return { run: r, ok: false, why: 'the job is not live' };
  if (!S || r.cur !== stepId || r.steps[stepId].st !== 'open') return { run: r, ok: false, why: 'that step is not open' };
  const O = S.outcomes[outcome];
  if (!O) return { run: r, ok: false, why: 'no such outcome' };
  r.steps[stepId] = { st: O.fail ? 'failed' : 'done', outcome, at: t };
  r.lines.push({ t, step: stepId, line: O.line });
  const events = [{ name: 'job:step', job: r.id, step: stepId, state: r.steps[stepId].st, outcome }];
  if (O.next === 'done' || O.next === 'failed') {
    r.st = O.next;
    r.outcome = outcome;
    r.endedAt = t;
    r.cur = null;
    events.push({ name: 'job:end', job: r.id, outcome });
  } else {
    r.cur = O.next;
    r.steps[O.next] = { st: 'open', outcome: null, at: t };
    events.push({ name: 'job:step', job: r.id, step: O.next, state: 'open' });
  }
  return { run: r, ok: true, line: O.line, events };
}
// The tester's skip (ER-JOB-07): the step is marked skipped and the job moves on by the outcome named (or its first).
function skip(run, spec, stepId, t, outcome) {
  const S = stepOf(spec, stepId);
  if (!S) return { run: copy(run), ok: false, why: 'no such step' };
  const name = outcome || Object.keys(S.outcomes)[0];
  const res = resolve(run, spec, stepId, name, t);
  if (res.ok) res.run.steps[stepId].st = 'skipped';
  return res;
}
// Windows, not minutes (law 3). minute: game minutes since Monday 00:00. A window may run past midnight.
// Returns { state: 'early' | 'open' | 'late', waitUntil } where waitUntil is the minute the window next opens.
function windowAt(step, minute) {
  const w = step.window;
  if (!w) return { state: 'open', waitUntil: minute };
  const dayStart = Math.floor(minute / 1440) * 1440,
    h = (minute - dayStart) / 60,
    wraps = w.untilHour <= w.fromHour;
  const inside = wraps ? h >= w.fromHour || h < w.untilHour : h >= w.fromHour && h < w.untilHour;
  if (inside) return { state: 'open', waitUntil: minute };
  const next = h < w.fromHour ? dayStart + w.fromHour * 60 : dayStart + 1440 + w.fromHour * 60;
  return { state: !wraps && h >= w.untilHour ? 'late' : 'early', waitUntil: next };
}
// Steps sleep while he is away and settle by the clock (ER-JOB-07): an open step whose last day has passed ends
// by its 'late' outcome if it has one, else its job fails as 'no show'.
function settle(run, spec, minute) {
  if (run.st !== 'taken' || !run.cur) return { run: copy(run), ok: false, why: 'nothing to settle' };
  // the days are counted from when this step opened (the first step: from when the job was taken)
  const S = stepOf(spec, run.cur),
    opened = run.steps[run.cur].at === null || run.steps[run.cur].at === undefined ? run.takenAt : run.steps[run.cur].at,
    takenDay = Math.floor(opened / 1440),
    last = S.lastDayOffset === undefined ? 1 : S.lastDayOffset,
    w = S.window || { fromHour: 0, untilHour: 24 },
    wraps = w.untilHour <= w.fromHour,
    deadline = (takenDay + last + (wraps ? 1 : 0)) * 1440 + w.untilHour * 60;
  if (minute < deadline) return { run: copy(run), ok: false, why: 'still inside its window' };
  if (S.outcomes.late) return resolve(run, spec, S.id, 'late', minute);
  const r = copy(run);
  r.steps[S.id] = { st: 'failed', outcome: 'no show', at: minute };
  r.st = 'failed';
  r.outcome = 'no show';
  r.endedAt = minute;
  r.cur = null;
  const line = 'Never turned up for ' + spec.name + '. Whoever asked will have counted it.';
  r.lines.push({ t: minute, step: S.id, line });
  return {
    run: r,
    ok: true,
    line,
    events: [
      { name: 'job:step', job: r.id, step: S.id, state: 'failed', outcome: 'no show' },
      { name: 'job:end', job: r.id, outcome: 'no show' },
    ],
  };
}
// The six laws as data checks. places: { id: { landmark, address } }. people: a list of known ids. Returns faults.
function check(spec, places, people) {
  const f = [],
    bad = (rule, what) => f.push(rule + ': ' + spec.id + ': ' + what);
  if (!spec.giver || (people && !people.includes(spec.giver))) bad('ER-REACH-01', 'no giver the game knows');
  if (!spec.channel || !CHANNELS.includes(spec.channel.kind)) bad('ER-REACH-01', 'no channel');
  else if (!spec.channel.place || !places[spec.channel.place]) bad('ER-REACH-01', 'the channel names no place');
  if (!spec.offer || !words(spec.offer)) bad('LAW-1', 'no offer in words');
  const A = spec.approaches || [];
  if (A.length < 2) bad('ER-JOB-03', 'fewer than two approaches');
  for (const need of ['needsTalk', 'needsFight', 'needsCar'])
    if (A.length && A.every((a) => a[need])) bad('ER-JOB-03', 'every approach ' + need);
  if (!spec.setPiece) bad('ER-JOB-06', 'no set piece named');
  if (!spec.steps || !spec.steps.length) bad('LAW-5', 'no steps');
  const ids = (spec.steps || []).map((s) => s.id),
    reached = new Set(ids.slice(0, 1));
  let ends = 0;
  for (const S of spec.steps || []) {
    if (!places[S.place]) bad('ER-JOB-01', S.id + ' names no known place');
    else if (!places[S.place].landmark) bad('ER-JOB-01', S.id + ': its place has no landmark');
    if (!S.directions || S.directions.length < 2) bad('ER-JOB-02', S.id + ' has fewer than two sources of direction');
    if (!S.act) bad('LAW-5', S.id + ' has no act the town can perceive');
    if (S.window) {
      const len = (S.window.untilHour - S.window.fromHour + 24) % 24 || 24;
      if (len < 2) bad('ER-JOB-04', S.id + ': a window under two game hours');
    }
    const outs = Object.keys(S.outcomes || {});
    if (!outs.length) bad('ER-JOB-05', S.id + ' has no outcome');
    if (S.decides && outs.filter((o) => o !== 'late').length < 2) bad('LAW-4', S.id + ' decides with fewer than two outcomes');
    for (const o of outs) {
      const O = S.outcomes[o],
        n = words(O.line || '');
      if (n < 8 || n > 34) bad('ER-JOB-05', S.id + '/' + o + ': a Ledger line of ' + n + ' words (about 22 wanted)');
      if (/—/.test(O.line || '')) bad('WORDS', S.id + '/' + o + ': a long dash');
      if (O.next === 'done' || O.next === 'failed') ends++;
      else if (!ids.includes(O.next)) bad('ER-JOB-05', S.id + '/' + o + ' leads nowhere');
      else reached.add(O.next);
    }
  }
  for (const id of ids) if (!reached.has(id)) bad('ER-JOB-05', id + ' can never be reached');
  if (!ends) bad('ER-JOB-05', 'no outcome ends the job');
  return f;
}
// Every route through a job, as lists of [step, outcome], for the scripts that reach every outcome (ER-JOB-05).
function routes(spec) {
  const out = [];
  const walk = (id, path, seen) => {
    const S = stepOf(spec, id);
    for (const o of Object.keys(S.outcomes)) {
      const O = S.outcomes[o],
        p = path.concat([[id, o]]);
      if (O.next === 'done' || O.next === 'failed') out.push({ path: p, ends: O.next, outcome: o });
      else if (!seen.includes(O.next)) walk(O.next, p, seen.concat(id));
    }
  };
  walk(spec.steps[0].id, [], []);
  return out;
}
// No set piece twice in thirty real minutes (law 6, ER-JOB-06). log: [ { piece, atRealSeconds } ].
function varietyOk(log, piece, nowRealSeconds, gapRealSeconds) {
  return !log.some((l) => l.piece === piece && nowRealSeconds - l.atRealSeconds < gapRealSeconds);
}
function varietyFaults(log, gapRealSeconds) {
  const f = [];
  for (let i = 0; i < log.length; i++)
    for (let j = i + 1; j < log.length; j++)
      if (log[i].piece === log[j].piece && Math.abs(log[j].atRealSeconds - log[i].atRealSeconds) < gapRealSeconds)
        f.push(log[i].piece + ' twice within ' + Math.round(Math.abs(log[j].atRealSeconds - log[i].atRealSeconds)) + ' s');
  return f;
}
export const PIECE = {
  name: 'job_template',
  fns: { newRun, take, refuse, resolve, skip, windowAt, settle, check, routes, varietyOk, varietyFaults },
};
