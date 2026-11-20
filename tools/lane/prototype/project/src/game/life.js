// LEDGER, the whole game: the system "life". The town's days (DESIGN 2 and 6; A18 to A20, A38; parts 2.1.2, 2.1.4,
// 2.1.6, 2.4.2, 2.4.5, 2.5.5, 2.16, 2.19, 3.7, 7.5, 7.12, 7.14): the calendar and who it puts on the street, the
// paper twice a week, street happenings placed by state, bodies and the missing, and play time booked by activity.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on, tomXZ } from './core.js';
import { G } from '../state.js';
import { hyp, esc, DAYS } from '../util.js';
import { act, remember } from '../events.js';
import { attached } from '../seeing.js';
import { KINDS } from '../kinds.js';
import { choose, scene, panel } from '../ui.js';
import { RULES } from '../rules.js';
import { PIECE as LIFE } from './pieces/life.js';
import { PIECE as EYES } from './pieces/eyes.js';
import { ellisEvent } from './law.js';

const T = RULES.game.life;
const L = LIFE.fns;
const S = { act: 'foot' };

// ---- the calendar (A20): what today is, and what it does to who is out ----
export const today = () => L.calendar(dayNow());
function crowd(base) {
  const h = hourNow(),
    w = G.weather.kind;
  const plain = L.crowd(h, 'dry', 0, 100) || 1;
  return Math.max(base ? 1 : 0, Math.round((base * L.crowd(h, w, dayNow(), 100)) / plain));
}
// ---- the paper (A19): twice a week; every printed line traces to what Alison saw or was told ----
function printPaper(d) {
  const x = X('life'),
    A = P_('alison');
  if (!A || x.papers[d]) return;
  const holds = A.mind.mem.filter((m) => KINDS[G.ev[m.e].kind] && !KINDS[G.ev[m.e].kind].priv && !KINDS[G.ev[m.e].kind].word && (KINDS[G.ev[m.e].kind].sev >= 0.3) && !x.printed[m.e]).map((m) => ({ words: KINDS[G.ev[m.e].kind].truth(G.ev[m.e]), src: m.src === 'told' ? 'told by ' + (m.from || 'somebody') : m.src === 'heard' ? 'heard it' : 'saw it', e: m.e, sure: m.sure, namesHim: attached(m) }));
  const p = L.paper(holds, d);
  if (!p.out) return;
  x.papers[d] = { lines: p.lines, t: Math.round(G.t) };
  for (const l of p.lines) {
    x.printed[l.e] = d;
    // the paper is a way news spreads beyond the routines' meetings, at the strength she wrote it
    for (const id of T.paperReaders) {
      const P = P_(id);
      if (P && !P.dead && !P.mind.by[l.e]) remember(P, G.ev[l.e], { src: 'told', from: 'alison', who: /\bTom\b/.test(l.text) ? 'tom' : 'man', sure: l.sure * T.paperStrengthTimes, heat: KINDS[G.ev[l.e].kind].sev, hop: 2 });
    }
  }
  if (p.lines.length) emit('life.paper', { day: d, lines: p.lines });
}
function readPaper() {
  const x = X('life'),
    d = Object.keys(x.papers).map(Number).sort((a, b) => b - a)[0];
  const p = x.papers[d];
  x.read[d] = true;
  panel(`<h2>The paper, ${DAYS[d % 7]}</h2><p>The local page.</p>${p.lines.length ? p.lines.map((l) => `<p>${esc(l.text)}.</p>`).join('') : '<p>Tides, a jumble sale at the chapel hall, and the Harbour Board minutes.</p>'}<p><button data-act="close">Fold it</button></p>`, 'paper');
  for (const l of p.lines) if (/Tom|Mickey's/.test(l.text)) write(`The paper has it: ${l.text}.`, { key: 'paper:' + l.e, who: 'alison', how: 'Read it in the paper' });
}
// ---- street happenings (A18): placed by the town's state and the hour, never by dice ----
function states() {
  const h = hourNow(),
    c = today();
  const out = (id) => {
    const P = P_(id);
    return !!P && !P.gone && !P.dead && P.space === 'street';
  };
  return { grocerOpen: h >= 8 && h < 18 && c.weekday !== 6, darrenOut: out('darren'), evening: h >= 18, noraHome: !!P_('nora') && P_('nora').space === 'home', marketDay: c.weekday === T.marketDayWeekday, ferryHour: h >= 15 && h < 22.5, normanOnRow: out('norman'), night: h >= 22 || h < 5, sylviaHome: !!P_('sylvia') && P_('sylvia').space !== 'street' };
}
function placeHappenings() {
  const x = X('life');
  if (x.live) {
    if (G.t - x.live.t > 90) x.live = null; // it drifts away if nobody takes it up
    return;
  }
  const s = Object.assign(states(), { hour: hourNow(), playedSeconds: G.played, dayIndex: dayNow() });
  const [tx, tz] = tomXZ();
  for (const h of T.happenings) {
    const r = L.happening(h, s, x.happened);
    if (!r.place || hyp(tx, tz, h.at[0], h.at[1]) > 70) continue;
    x.live = { id: h.id, t: G.t, by: r.by };
    x.happened.push({ id: h.id, street: h.street, playedSeconds: G.played, dayIndex: dayNow(), by: r.by, taken: null });
    return;
  }
}
async function happening(h) {
  const x = X('life');
  const i = await scene(() => choose('', h.text, h.choices.map((c) => c[0])));
  const c = h.choices[i];
  act(c[1], { what: h.id === 'shoplifter' ? 'a shoplifter at Hook Stores' : h.id === 'row' ? "the row on Nora Cronin's step" : h.id === 'van' ? 'a van stuck in the back lane' : h.id === 'lostman' ? 'a lost man off the ferry' : h.id === 'dogloose' ? 'a dog loose on the quay' : 'a lodger locked out', target: h.who && G.people[h.who] && !G.people[h.who].anon ? h.who : undefined });
  write(c[2], { how: 'Did it', who: h.who && G.people[h.who] && !G.people[h.who].anon ? h.who : undefined });
  const log = x.happened[x.happened.length - 1];
  log.taken = c[1];
  if (h.returns && c[1] !== 'walked_past') x.returns.push({ id: h.id, dueT: G.t + T.happeningReturnsAfterGameDays * 1440, text: h.returns });
  x.live = null;
  emit('life.happening', { id: h.id, taken: c[1] });
}
// ---- bodies and the missing (2.16): a body is never wiped; a missing routine becomes the town's question ----
function bodies(d) {
  const x = X('life');
  for (const b of x.bodies) {
    if (b.found || b.asked) continue;
    // lying where a routine passes it is found by whoever really passes (game/traces.js); never found, he is missed
    if (d - Math.floor(b.t / 1440) >= T.missingAskedAfterGameDays) {
      b.asked = Math.round(G.t);
      ellisEvent('talk');
      write(`People are asking where ${b.name} has got to. Nobody has seen ${b.sex === 'f' ? 'her' : 'him'} since ${DAYS[Math.floor(b.t / 1440) % 7]}.`, { key: 'missing:' + b.id, how: 'The street says' });
    }
  }
}

register({
  id: 'life',
  fresh: () => ({ papers: {}, printed: {}, read: {}, happened: [], live: null, returns: [], bodies: [], booked: { foot: 0, driving: 0, talk: 0, jobs: 0, fights: 0, ledger: 0, waiting: 0 }, lastNewPlayed: 0, calSaid: -1 }),
  loaded() {
    G.hooks.crowd = crowd;
  },
  step(dt) {
    // play time booked by activity (ER-CORE-06): what the hour budget is measured from
    const x = X('life'),
      t = G.tom,
      modal = G.hooks.modal ? G.hooks.modal() : null;
    const k = G.fast > 1 ? 'waiting' : modal === 'talk' || modal === 'dialog' ? 'talk' : modal === 'ledger' || modal ? 'ledger' : G.hooks.fighting && G.hooks.fighting() ? 'fights' : t.inCar ? 'driving' : G.x.crime.inside || (G.story.job && G.story.job.carrying) ? 'jobs' : 'foot';
    x.booked[k] += dt;
  },
  minute(m) {
    if (m % T.happeningCheckedEveryGameMinutes === 0) placeHappenings();
    const x = X('life');
    for (const r of x.returns)
      if (!r.done && G.t >= r.dueT && G.tom.space === 'street' && !G.paused) {
        r.done = true; // a stranger he helped turns up days later with a small favour (A18)
        tell(r.text, '', 8);
        write(r.text, { how: 'A man he once helped said' });
      }
  },
  hourly(h, d) {
    const x = X('life'),
      c = L.calendar(d);
    if (h === 6 && c.paperOut) printPaper(d);
    if (h === 7 && x.calSaid !== d && c.is.length) {
      x.calSaid = d;
      write(`${DAYS[c.weekday]}: ${c.is.join('; ')}.`, { key: 'cal:' + d, how: 'The day it is' });
    }
    if (h === 7) bodies(d);
  },
  hotspots(out) {
    const x = X('life'),
      t = G.tom;
    if (x.live && t.space === 'street') {
      const h = T.happenings.find((q) => q.id === x.live.id);
      if (hyp(t.x, t.z, h.at[0], h.at[1]) < T.happeningWithinMetres) out.push({ k: 'T', t: 'See what is going on', run: () => happening(h) });
    }
    const days = Object.keys(x.papers);
    if (days.length && ['news', 'caff', 'mickeys'].includes(t.space) && !x.read[Math.max(...days.map(Number))]) out.push({ k: 'G', t: 'Read the local page', run: readPaper });
  },
  hook: {
    x: () => X('life'),
    today,
    crowd,
    states,
    printPaper,
    placeHappenings,
    happening: (id) => happening(T.happenings.find((q) => q.id === id)),
    budget: () => L.budget(X('life').booked),
    hot: (kind, days) => L.hot(kind, days),
  },
});
on('traces.found', (f) => {
  const b = f.kind === 'body' && X('life').bodies.find((q) => q.id === f.e);
  if (!b || b.found) return;
  b.found = { by: f.by, t: Math.round(G.t) };
  write(`They have found ${b.name} at ${b.zone}. ${P_(f.by) ? P_(f.by).def.name + ' came on him' : 'Somebody came on him'}.`, { key: 'body:' + b.id, how: 'The street says' });
});
on('act', (E) => {
  if (E.kind !== 'kill') return;
  const P = G.people[E.target];
  X('life').bodies.push({ id: E.id, name: E.name || 'a man', sex: P ? P.def.sex : 'm', zone: E.zone, t: G.t, hidden: false, found: null, asked: null });
});
