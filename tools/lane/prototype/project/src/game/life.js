// LEDGER, the whole game: the system "life". The town's days: the calendar (A20), who is out by hour, weather and
// day (2.1.2, 2.1.4), the paper and letters (A19), street happenings (A18), side stories (3.3), calling on people
// (A39), the boxing club (A28), lasting marks on the town (2.19), greetings by regard and rung (2.12.4), always
// something to do (ER-CORE-07) and teaching by hints (ER-FIRST-03). Every rule is a pure piece under pieces/.
import { register, PLACES, X, emit, on } from './core.js';
import { G, day, hour } from '../state.js';
import { RULES } from '../rules.js';
import { PIECE as CALP } from './pieces/calendar_days.js';
import { PIECE as CROWDP } from './pieces/life_crowd.js';
import { PIECE as PAPERP } from './pieces/paper_lines.js';
import { PIECE as RULESP } from './pieces/life_rules.js';
import { say, scene, sub, bubble } from '../ui.js';
import { remember } from '../events.js';
import { note } from '../ledger.js';
import { send } from '../routines.js';
import { callName } from '../gossip.js';
import { KINDS } from '../kinds.js';
import { DAYS } from '../util.js';
import { GREET_BY, CROWD_LINES, CALENDAR_LINES, OWN_STREET, speakerKind, allNewLines } from './life_lines.js';
import { happenStep, happenHotspots, happenHook, favourStep } from './life_happenings.js';
import { storyHotspots, storyHook, storyThings } from './life_stories.js';
import { peopleHotspots, peopleHook, peopleBeat } from './life_people.js';

const T = RULES.game.life;
const CAL = CALP.fns,
  CR = CROWDP.fns,
  LR = RULESP.fns;
const C = RULES.crowd;
const WINDOWS = [
  { untilHour: C.smallHoursUntilHour, walkers: 0 },
  { untilHour: C.dawnUntilHour, walkers: C.walkersAtDawn },
  { untilHour: C.earlyUntilHour, walkers: C.walkersEarly },
  { untilHour: C.dayUntilHour, walkers: C.walkersByDay },
  { untilHour: C.eveningUntilHour, walkers: C.walkersInTheEvening },
  { untilHour: C.lateUntilHour, walkers: C.walkersLate },
  { untilHour: 24, walkers: 0 },
];
// who keeps which calendar habit (first values; the regular cards settle it)
const HABIT = {
  churchgoer: ['nora', 'albert', 'sylvia', 'danby', 'brenda', 'grace'],
  trader: ['nora', 'lily', 'albert', 'julie'],
  follows: ['kevin', 'lee', 'wayne', 'shaun'],
  shopkeeper: ['grace', 'rita', 'hal', 'peter', 'lily', 'brenda', 'sheila', 'pauline'],
  stayIn: ['ada', 'calvert', 'sheila', 'pauline', 'ron', 'terry', 'ellis', 'pc', 'alison', 'june', 'susan', 'norman'],
};
const habitOf = (id) => ({ id, churchgoer: HABIT.churchgoer.includes(id), trader: HABIT.trader.includes(id), follows: HABIT.follows.includes(id), shopkeeper: HABIT.shopkeeper.includes(id), stayIn: HABIT.stayIn.includes(id) });
const SPOT_FOR = { chapel: ['chapelgate', 'bench', 'grave'], market: ['market1', 'market2', 'market3'], quay: ['quaycorner', 'harbourdoor', 'smoke1', 'lads3', 'lads4'] };
let crowdT = 0,
  greetT = 0,
  calT = 0,
  bumpT = 0;

export const today = () => CAL.dayKind(day());
export const calendarNow = () => CAL.changes(day(), hour(), T.calendar);
export function crowdTarget() {
  return CR.crowdCount(hour(), G.weather.rain, CAL.crowdShare(day(), hour(), T.calendar), WINDOWS, T.crowd);
}
// ---------- the calendar moves people (ER-CAL-01) ----------
function calendarHour(h, d) {
  const x = X('life');
  let n = 0;
  for (const P of G.named || []) {
    if (!P || P.dead || P.gone || P.hold || P.override) continue;
    const where = CAL.placeFor(habitOf(P.id), d, h + 0.5, T.calendar);
    if (!where) continue;
    const until = (d * 24 + h + 1) * 60;
    if (where === 'off') send(P, 'off', 'idle', until);
    else {
      const spots = SPOT_FOR[where];
      send(P, spots[n++ % spots.length], 'idle', until);
    }
    x.calendar.moved.push({ d, h, who: P.id, to: where });
  }
  if (x.calendar.moved.length > 300) x.calendar.moved.splice(0, 100);
}
// ---------- who is out (2.1.2, 2.1.4): never more walkers than the hour, the weather and the day allow ----------
function thinCrowd() {
  const want = crowdTarget(),
    t = G.tom;
  let out = 0;
  for (const P of G.crowd || []) {
    if (!/^w\d+$/.test(P.id) || P.gone || P.space !== 'street') continue;
    out++;
    if (out <= want || P.hold || P.borrowed || P.pax || P.mark) continue;
    const d = Math.hypot(P.x - (t.inCar ? G.car.x : t.x), P.z - (t.inCar ? G.car.z : t.z));
    if (d < T.crowd.thinOnlyBeyondMetres && t.space === 'street') continue; // nobody vanishes in his sight
    P.gone = true;
    P.space = 'off';
    P.route = null;
    P.moving = false;
    out--;
  }
  X('life').crowd = { want, out, hour: Math.floor(hour()), rain: Math.round(G.weather.rain * 100) / 100 };
}
// ---------- the paper (A19, ER-PAPER-01) ----------
function alisonKnows() {
  const A = G.people.alison,
    x = X('life');
  if (!A || !A.mind) return [];
  return A.mind.mem
    .map((m) => {
      const E = G.ev[m.e],
        k = E && KINDS[E.kind];
      if (!E || !k || k.priv || E.kind === 'inherit') return null;
      return { e: E.id, kind: E.kind, src: m.src, sure: m.sure, named: m.who === 'tom' || m.who === 'owner', crime: k.crime || 0, sev: k.sev || 0, words: k.truth(E), t: E.t, printed: !!x.paper.printed[E.id] };
    })
    .filter(Boolean);
}
export function printEdition(d = day()) {
  const x = X('life'),
    knows = alisonKnows();
  const lines = PAPERP.fns.edition(knows, T.paper.linesAnEdition, T.paper);
  const ed = { day: d, lines, traced: PAPERP.fns.traces(lines, knows), read: false };
  for (const l of lines) x.paper.printed[l.e] = d;
  x.paper.editions.push(ed);
  if (x.paper.editions.length > 20) x.paper.editions.shift();
  // people of the Hook who read the local page take each line at the strength she wrote it (no dice: the day picks)
  const A = G.people.alison;
  const readers = (G.named || []).filter((P) => P.def.local !== false && !P.dead && P.id !== 'alison');
  for (let i = 0; i < Math.min(T.paper.readersAnEdition, readers.length); i++) {
    const P = readers[(d * 3 + i * 5) % readers.length];
    for (const l of lines) {
      const E = G.ev[l.e];
      if (!E || P.mind.by[E.id]) continue;
      remember(P, E, { src: 'told', from: A ? 'alison' : null, who: l.names ? 'tom' : 'man', sure: PAPERP.fns.readerSure(l, T.paper), heat: 0.5, hop: 1 });
      ed.readers = (ed.readers || 0) + 1;
    }
  }
  emit('paper', ed);
  return ed;
}
export async function readPaper() {
  const x = X('life'),
    ed = x.paper.editions[x.paper.editions.length - 1];
  await scene(async () => {
    if (!ed) return say('', 'The Evening Mail. Last week\'s, gone soft at the fold. Nothing in it he needs.');
    const dt = CAL.dateOf(ed.day);
    await say('', `THE EVENING MAIL. ${dt.weekday} ${dt.dayOfMonth} ${dt.month} 1990. The local page.`);
    if (!ed.lines.length) await say('', 'Harbour Board to meet on dredging. Steam laundry site still unsold. Nothing about Quay Street.');
    for (const l of ed.lines) await say('', l.text);
  });
  if (ed && !ed.read) {
    ed.read = true;
    for (const l of ed.lines) note('In the paper: ' + l.text, 'paper', 'paper' + ed.day + '_' + l.e, { who: 'alison', how: 'Read it in the Evening Mail', ev: l.e });
  }
}
// ---------- letters (6.10): each opens as a page and goes into the Ledger ----------
const LETTERS = {
  mickey: { from: 'Mickey Suddaby', title: "Mickey's letter", body: ['Tom. If you are reading this then I am not there to explain it.', "The office is yours. Sheila knows where everything is. Ron knows where everybody is.", 'Do not sell the cars. Do not believe the debt book. Your uncle, M.'] },
  solicitor: { from: 'Pym and Tasker, solicitors', title: "A solicitor's letter", body: ['Dear Mr Nowak. We act for a client with an interest in private hire in the borough.', 'We are instructed to ask for sight of your operator\'s licence and the insurance of each vehicle, within fourteen days.', 'Yours faithfully.'] },
  vat: { from: 'H.M. Customs and Excise', title: 'A letter from Customs and Excise', body: ['Dear Sir. An officer will call at your premises on Monday to examine the records of the business for value added tax.', 'Please have ready the fare book, the purchase invoices and the bank statements for the period.', 'You may be represented. Yours faithfully.'] },
  rent: { from: 'Mrs S. Rennison', title: 'A note under the door', body: ['Mr Nowak. Friday means Friday. S. Rennison.'] },
};
// A letter arrives at the office and waits there; reading it opens it as a page and writes it in the Ledger.
export function postLetter(spec) {
  const l = typeof spec === 'string' ? Object.assign({ id: spec }, LETTERS[spec]) : spec;
  if (!l || !l.id || !l.body) return false;
  const x = X('life');
  if (x.letters.read[l.id] || x.letters.waiting.some((w) => w.id === l.id)) return false;
  x.letters.waiting.push({ id: l.id, from: l.from || '', title: l.title || 'A letter', body: l.body, t: Math.round(G.t) });
  return true;
}
export async function letter(spec) {
  // open it now, in the hand (the giver is there, or it is read at the office)
  const l = typeof spec === 'string' ? Object.assign({ id: spec }, LETTERS[spec] || X('life').letters.waiting.find((w) => w.id === spec)) : spec;
  if (!l || !l.body) return false;
  const x = X('life');
  await scene(async () => {
    await say('', `${l.title || 'A letter'}${l.from ? ', from ' + l.from : ''}.`);
    for (const line of l.body) await say('', line);
  });
  x.letters.waiting = x.letters.waiting.filter((w) => w.id !== l.id);
  if (!x.letters.read[l.id]) {
    x.letters.read[l.id] = Math.round(G.t);
    note(`${l.title || 'A letter'}${l.from ? ' from ' + l.from : ''}: ${l.body.join(' ')}`.slice(0, 400), 'letter', 'letter_' + l.id, { how: 'Read it' });
    emit('letter:read', { id: l.id });
  }
  return true;
}
// ---------- lasting marks on the town (2.19) ----------
export function townMark(kind, place, by) {
  const x = X('life'),
    p = typeof place === 'string' ? PLACES[place] : place;
  if (!p || !T.marks.lastsGameMinutes[kind]) return null;
  const m = { id: x.marks.next++, kind, place: typeof place === 'string' ? place : null, x: p.x, z: p.z, name: p.name || 'a door', t: Math.round(G.t), by: by || null };
  x.marks.list.push(m);
  return m;
}
export const marksNow = () => LR.marksAlive(X('life').marks.list, G.t, T.marks.lastsGameMinutes);
const MARK_WORDS = { forced_door: 'The door of {n} still shows where it was forced.', broken_window: 'A board over a window at {n}. The glass is still in the gutter.', tape: 'Police tape across {n}.', boarded: '{n}: boarded up.', blood: 'A dark stain on the flags by {n}.', paint: 'Fresh paint over something on the wall at {n}.' };
function marksStep() {
  const t = G.tom,
    x = X('life');
  if (t.space !== 'street' || t.inCar) return;
  for (const m of marksNow()) {
    if (x.marks.seen[m.id] === day() || Math.hypot(t.x - m.x, t.z - m.z) > 7) continue;
    x.marks.seen[m.id] = day();
    sub(MARK_WORDS[m.kind].replace('{n}', m.name), '', 'over', 4);
    return;
  }
}
// ---------- teaching (ER-FIRST-03) ----------
export function hint(id, text) {
  const x = X('life');
  const r = LR.hint(x.hints, id, G.played, G.settings.hints !== false, T.hints);
  x.hints = r.st;
  if (r.show) {
    x.hintLog.push({ id, at: Math.round(G.played * 10) / 10 });
    sub(text, '', 'over', 6);
  }
  return r.show;
}
// ---------- always something to do (ER-CORE-07) ----------
export function somethingToDo() {
  const t = G.tom,
    px = t.inCar ? G.car.x : t.x,
    pz = t.inCar ? G.car.z : t.z,
    things = [];
  const here = t.space === 'street' ? [px, pz] : (() => {
    const p = Object.values(PLACES).find((q) => q.room === t.space);
    return p ? [p.x, p.z] : [px, pz];
  })();
  const dist = (P) => {
    if (P.space === 'street') return Math.hypot(P.x - here[0], P.z - here[1]);
    if (P.space === t.space) return 2;
    const p = Object.values(PLACES).find((q) => q.room && q.room === P.space);
    return p ? Math.hypot(p.x - here[0], p.z - here[1]) + 4 : null;
  };
  for (const id in G.debts || {}) {
    const P = G.people[id];
    if (!P || P.dead || G.debts[id].st !== 'open' || !(G.ledger.notes || []).some((n) => n.key === 'debts')) continue;
    const d = dist(P);
    if (d != null) things.push({ kind: 'debt', id, metres: Math.round(d) });
  }
  if (G.car.keys && !G.story.fare) things.push({ kind: 'fare', id: 'radio', metres: Math.round(Math.hypot(G.car.x - here[0], G.car.z - here[1])) });
  for (const P of G.named || []) {
    if (P.dead || P.gone) continue;
    const word = P.mark || P.pendingAsk || (G.hooks.pending && G.hooks.pending(P));
    if (!word) continue;
    const d = dist(P);
    if (d != null) things.push({ kind: 'word', id: P.id, metres: Math.round(d) });
  }
  const hp = X('life').happen.active;
  if (hp) things.push({ kind: 'happening', id: hp.id, metres: Math.round(Math.hypot(hp.x - here[0], hp.z - here[1])) });
  for (const s of storyThings()) things.push({ kind: 'story', id: s.id, metres: Math.round(Math.hypot(s.x - here[0], s.z - here[1])) });
  // anybody named within reach can be spoken to: a person with a word for him when he asks (DESIGN 11)
  for (const P of G.named || []) {
    if (P.dead || P.gone || P.space === 'home' || P.space === 'off') continue;
    const d = dist(P);
    if (d != null && !things.some((x) => x.id === P.id)) things.push({ kind: 'talk', id: P.id, metres: Math.round(d) });
  }
  const strict = things.filter((x) => x.kind !== 'talk');
  const r = LR.somethingToDo(strict, !!t.inCar, T.todo);
  return Object.assign(r, { things, withTalk: LR.somethingToDo(things, !!t.inCar, T.todo) });
}
// ---------- greetings by regard and rung, and the crowd's lines by situation (2.12.4, 3.6.4) ----------
function saidToday(P, line) {
  const x = X('life'),
    k = P.id + '|' + line,
    d = day();
  if (x.said[k] === d) return true;
  x.said[k] = d;
  return false;
}
function pickLine(P, pool) {
  // the first line of the pool this person has not said today, starting from the day's place (no dice)
  for (let i = 0; i < pool.length; i++) {
    const line = pool[(i + day() + (P.id ? P.id.length : 0)) % pool.length];
    if (!saidToday(P, line)) return line;
  }
  return null;
}
function greetStep(dt) {
  greetT -= dt;
  bumpT -= dt;
  const t = G.tom;
  if (t.inCar || t.space !== 'street' || G.paused) return;
  const rung = LR.greetingRung((G.x.rise && G.x.rise.rung) || 1);
  // a bump: a walker within half a metre while he is moving
  if (bumpT <= 0 && t.v > 1)
    for (const P of G.crowd || []) {
      if (P.gone || P.space !== 'street' || P.lad || P.hold) continue;
      if (Math.hypot(P.x - t.x, P.z - t.z) < 0.55) {
        const line = pickLine(P, CROWD_LINES.bump[speakerKind(P)]);
        if (line) bubble(P, line, 3);
        bumpT = 8;
        X('life').lines.push({ sit: 'bump', by: P.id, at: Math.round(G.played) });
        return;
      }
    }
  if (greetT > 0) return;
  for (const P of G.named || []) {
    if (P.dead || P.gone || P.space !== 'street' || P.talking || P.hold) continue;
    const d = Math.hypot(P.x - t.x, P.z - t.z);
    if (d > T.greet.saidWithinMetres || d < 1 || !(P.mind.look > 0)) continue;
    const m = P.mind;
    const kind = LR.greetingKind({ knowsHim: m.fam > 0.15 || !!m.inh, fear: m.fear, regard: m.regard, marked: (t.hurt || 0) > 0.35 }, T.greet);
    const own = kind === 'neutral' && OWN_STREET[P.id] ? OWN_STREET[P.id] : null;
    const line = pickLine(P, own || GREET_BY[kind][rung]);
    if (!line) continue;
    bubble(P, line.replace('{name}', callName(P) || ''), 3.5);
    greetT = T.greet.everyRealSeconds;
    X('life').lines.push({ sit: 'greet', kind, rung, by: P.id, at: Math.round(G.played) });
    return;
  }
  // rain, and the calendar's days, from the crowd
  const cal = today(),
    rain = G.weather.rain >= T.crowd.rainFromRain;
  const pool = cal.bonfire && calendarNow().quayDisplay ? 'bonfire' : cal.remembrance ? 'remembrance' : cal.match && calendarNow().streetFull ? 'match' : cal.market && calendarNow().marketBusy ? 'market' : cal.sunday ? 'sunday' : null;
  for (const P of G.crowd || []) {
    if (P.gone || P.space !== 'street' || P.lad || P.pax) continue;
    if (Math.hypot(P.x - t.x, P.z - t.z) > T.greet.saidWithinMetres) continue;
    const line = pool && !rain ? pickLine({ id: 'street' }, CALENDAR_LINES[pool]) : rain ? pickLine(P, CROWD_LINES.rain[speakerKind(P)]) : null;
    if (!line) continue;
    bubble(P, line, 3.5);
    greetT = CR.chatterEverySeconds(G.weather.rain, T.crowd);
    X('life').lines.push({ sit: pool && !rain ? pool : 'rain', by: P.id, at: Math.round(G.played) });
    return;
  }
}

register({
  id: 'life',
  fresh: () => ({
    calendar: { moved: [] },
    crowd: null,
    paper: { editions: [], printed: {} },
    letters: { waiting: [], read: {} },
    marks: { list: [], next: 1, seen: {} },
    hints: { shown: {}, lastAt: null },
    hintLog: [],
    happen: { active: null, log: [], helped: [], placements: [] },
    stories: {},
    calls: { alison: [], danby: [], last: {} },
    friend: { who: null, holds: false, word: 'slight' },
    boxing: { bouts: 0, met: [] },
    favours: {},
    said: {},
    lines: [],
  }),
  loaded(x) {
    const f = this.fresh();
    for (const k in f) if (x[k] === undefined) x[k] = f[k];
    G.hooks.townMark = townMark;
    G.hooks.townMarks = marksNow;
    G.hooks.letter = letter;
    G.hooks.postLetter = postLetter;
    G.hooks.hint = hint;
    G.hooks.calendar = () => Object.assign({}, today(), calendarNow(), CAL.dateOf(day()));
    G.hooks.somethingToDo = somethingToDo;
    G.hooks.readPaper = readPaper;
    G.hooks.favour = (id) => !!X('life').favours[id];
    G.hooks.friend = () => Object.assign({}, X('life').friend);
  },
  step(dt) {
    if (G.story.phase !== 'play') return;
    crowdT += dt;
    if (crowdT >= T.crowd.thinCheckedEveryRealSeconds) {
      crowdT = 0;
      thinCrowd();
    }
    if (G.paused) return;
    calT += dt;
    if (calT > 1) {
      calT = 0;
      marksStep();
      // hesitation at the very start: one hint, then the rest piece by piece on first need
      const t = G.tom;
      if (G.played > T.hints.hesitatesAfterRealSeconds && G.played < 60 && (t.still || 0) > T.hints.hesitatesAfterRealSeconds) hint('walk', 'Walk with W A S D or the left stick. Look with the mouse or the right stick.');
    }
    greetStep(dt);
    happenStep(dt);
  },
  hourly(h, d) {
    calendarHour(h, d);
    const k = CAL.dayKind(d);
    if (k.paper && h === Math.floor(T.paper.outAtHour)) printEdition(d);
    favourStep(d, h);
    if (X('life').lines.length > 300) X('life').lines.splice(0, 100);
  },
  daily(d) {
    const x = X('life');
    for (const k in x.said) if (x.said[k] < d - 7) delete x.said[k];
    x.marks.list = x.marks.list.filter((m) => G.t - m.t < 30 * 1440);
  },
  hotspots(out) {
    const t = G.tom,
      x = X('life');
    if (t.space === 'mickeys' && x.letters.waiting.length) {
      const l = x.letters.waiting[0];
      out.push({ k: 'G', t: 'Read the post: ' + l.title.toLowerCase(), run: () => letter(l) });
    }
    if ((t.space === 'caff' || t.space === 'news') && x.paper.editions.length && !x.paper.editions[x.paper.editions.length - 1].read) {
      // the paper lies on the counter (the shop's own counter stays on its own prompt)
      hint('paper', 'The Evening Mail comes out on Tuesday and Friday. What it prints about you, people will have read.');
    }
    happenHotspots(out);
    storyHotspots(out);
    peopleHotspots(out);
  },
  beatFor: (P) => peopleBeat(P),
  hook: Object.assign(
    {
      date: (d = day()) => CAL.dateOf(d),
      dayKind: (d = day()) => CAL.dayKind(d),
      calendar: (d = day(), h = hour()) => CAL.changes(d, h, T.calendar),
      calendarHour,
      crowdTarget,
      crowdOut: () => (G.crowd || []).filter((P) => /^w\d+$/.test(P.id) && !P.gone && P.space === 'street').length,
      thinCrowd,
      printEdition,
      alisonKnows,
      readPaper,
      postLetter,
      letter,
      townMark,
      marksNow,
      hint,
      somethingToDo,
      state: () => JSON.parse(JSON.stringify(X('life'))),
      lines: allNewLines,
      greetStep: (dt) => {
        greetT = 0;
        bumpT = 0;
        greetStep(dt);
      },
    },
    happenHook,
    storyHook,
    peopleHook,
  ),
});
on('paper:bought', () => readPaper());
void DAYS;
