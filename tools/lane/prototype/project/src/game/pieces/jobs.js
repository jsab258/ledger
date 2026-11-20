// RULE PIECE: jobs (DESIGN 4). Pure. Unreal ports it and passes test/cases/jobs.json.
// A job is a small graph of saved states: four job states (offered, taken, done, failed) and five step states
// (waiting, open, done, failed, skipped). Offered by a person on a state; three keys to every lock; windows, not
// minutes; failure continues; authored, never rolled.
import { TUNE as T } from '../tune/jobsx.js';

// A job's spec is checked once, when written (the six laws and ER-JOB-01 to 05, ER-REACH-01). Returns the faults.
function validate(spec) {
  const bad = [];
  if (!spec.id || !spec.name) bad.push('no id or name');
  if (!spec.giver) bad.push('law 1: offered by a person');
  if (!spec.channel || !spec.channelPlace) bad.push('ER-REACH-01: a channel that names a place');
  const ways = spec.approaches || [];
  if (ways.length < T.approachesAtLeast) bad.push('ER-JOB-03: at least two approaches');
  if (!ways.some((w) => !w.needsTalk && !w.needsFight && !w.needsCar)) bad.push('ER-JOB-03: one approach needs no talk, fight or car');
  for (const s of spec.steps || []) {
    if (!s.landmark) bad.push('ER-JOB-01: step ' + s.id + ' names no landmark');
    if ((s.directions || []).length < T.directionsAtLeast) bad.push('ER-JOB-02: step ' + s.id + ' has under two sources of direction');
    if (s.window && s.window.untilT - s.window.fromT < T.windowAtLeastGameHours * 60) bad.push('ER-JOB-04: step ' + s.id + ' has a window under two game hours');
    if (!s.line) bad.push('step ' + s.id + ' has no Ledger line');
    else if (s.line.split(/\s+/).length > T.ledgerLineWordsAtMost) bad.push('step ' + s.id + ' has a Ledger line too long');
    if (s.decides && (s.outcomes || []).length < 2) bad.push('step ' + s.id + ' decides with under two outcomes');
  }
  if (!(spec.steps || []).length) bad.push('no steps');
  if (!spec.failLine) bad.push('law 4: failure continues, with a line the town can talk about');
  return bad;
}
const start = (spec, t) => ({ id: spec.id, st: 'offered', offeredT: t, step: 0, steps: spec.steps.map((s) => ({ id: s.id, st: 'waiting', outcome: null })), lines: [] });
// One event on a job: 'take', 'refuse', 'open' (the step's place reached), 'done' (with an outcome), 'fail', 'skip'
// (the tester's skip, ER-JOB-07), 'clock' (the window closed with the step not done). Returns the new job and the
// Ledger line it leaves, if any. Nothing restarts.
function advance(spec, job, ev) {
  const j = JSON.parse(JSON.stringify(job));
  const line = (text) => {
    j.lines.push(text);
    return { job: j, line: text };
  };
  if (j.st === 'done' || j.st === 'failed') return { job: j, line: null };
  if (ev.what === 'refuse' && j.st === 'offered') {
    j.st = 'failed';
    j.how = 'refused';
    return line(spec.refuseLine || spec.failLine);
  }
  if (ev.what === 'take' && j.st === 'offered') {
    j.st = 'taken';
    j.steps[0].st = 'open';
    return line(spec.takeLine || 'Took it on: ' + spec.name + '.');
  }
  if (j.st !== 'taken') return { job: j, line: null };
  const s = j.steps[j.step],
    S = spec.steps[j.step];
  if (ev.what === 'clock') {
    if (!S.window || ev.t <= S.window.untilT || s.st === 'done') return { job: j, line: null };
    s.st = 'failed';
    j.st = 'failed';
    j.how = 'late';
    return line(S.lateLine || spec.failLine);
  }
  if (ev.what === 'fail') {
    s.st = 'failed';
    j.st = 'failed';
    j.how = ev.how || 'failed';
    return line(ev.line || spec.failLine);
  }
  if (ev.what === 'done' || ev.what === 'skip') {
    if (ev.what === 'done' && S.decides && !(S.outcomes || []).includes(ev.outcome)) return { job: j, line: null };
    s.st = ev.what === 'skip' ? 'skipped' : 'done';
    s.outcome = ev.outcome || (S.outcomes ? S.outcomes[0] : null);
    const text = (S.outcomeLines && S.outcomeLines[s.outcome]) || S.line;
    if (j.step + 1 < j.steps.length) {
      j.step++;
      j.steps[j.step].st = 'open';
    } else {
      j.st = 'done';
      j.how = s.outcome || 'done';
    }
    return line(text);
  }
  return { job: j, line: null };
}
// Windows, not minutes: is he in time, early (with a "wait until"), or late?
const timing = (window, t) => (!window ? { st: 'open', waitUntilT: null } : t < window.fromT ? { st: 'early', waitUntilT: window.fromT } : t <= window.untilT ? { st: 'open', waitUntilT: null } : { st: 'late', waitUntilT: null });
// Law 6: no set piece twice in thirty minutes of play. log: [{ kind, playedSeconds }]
const mayStage = (kind, log, playedSeconds) => !log.some((l) => l.kind === kind && playedSeconds - l.playedSeconds < T.setPieceNotTwiceWithinRealMinutes * 60);
// Minding: standing with somebody is recorded as "stood with" and pays by the hour once it has lasted.
const minding = (gameMinutes) => ({ counts: gameMinutes >= T.minding.countsAfterGameMinutes, pence: gameMinutes >= T.minding.countsAfterGameMinutes ? Math.round((gameMinutes / 60) * T.minding.paysPencePerGameHour) : 0, fact: 'stood with' });
export const PIECE = { name: 'jobs', fns: { validate, start, advance, timing, mayStage, minding } };
