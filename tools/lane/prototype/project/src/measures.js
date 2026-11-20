// LEDGER. The Ledger screen test: what is measured, and the scripted "find the fact" asks.
// Everything here is a playtest instrument. It is saved with the week, shown on the Measures screen, exported
// as one JSON file and returned by the test hook as LEDGER.measures().
import { G } from './state.js';
import { RULES } from './rules.js';
import { book, bookFaults } from './ledger.js';
const ASKING = RULES.asks;

const LED = RULES.ledger;
const nowMs = () => (typeof performance !== 'undefined' ? performance.now() : 0);

export function M() {
  if (!G.measures)
    G.measures = {
      version: 1,
      visits: [],
      noted: [],
      asks: [],
      talks: 0,
      talksWithSlipUnfolded: 0,
      tab: { firstPressAtRealSecondsPlayed: null },
    };
  return G.measures;
}

// ---------- Ledger visits ----------
let visit = null;
export function visitStart(device, from, part) {
  const m = M();
  visit = {
    atRealSecondsPlayed: Math.round(G.played),
    atGameMinute: Math.round(G.t),
    device,
    openedFrom: from || 'play',
    part,
    t0: nowMs(),
  };
  // a Noted line is "followed" when the Ledger is opened within a minute of it
  for (const n of m.noted)
    if (
      n.followedByOpen == null &&
      G.played - n.atRealSecondsPlayed <= LED.notedCountsAsFollowedWithinRealSeconds
    )
      n.followedByOpen = true;
  const a = activeAsk();
  if (a && a.openedAtMs == null) {
    a.openedAtMs = nowMs();
    a.realSecondsFromAskToOpen = round1((a.openedAtMs - a.shownAtMs) / 1000);
  }
}
export function visitEnd() {
  if (!visit) return;
  const m = M();
  m.visits.push({
    atRealSecondsPlayed: visit.atRealSecondsPlayed,
    atGameMinute: visit.atGameMinute,
    device: visit.device,
    openedFrom: visit.openedFrom,
    openedOnPart: visit.part,
    realSecondsOpen: round1((nowMs() - visit.t0) / 1000),
  });
  visit = null;
}

// ---------- the Noted line ----------
export function notedShown(things) {
  const m = M();
  for (const n of m.noted) if (n.followedByOpen == null) n.followedByOpen = false; // the one before was not followed
  m.noted.push({
    atRealSecondsPlayed: Math.round(G.played),
    atGameMinute: Math.round(G.t),
    things,
    followedByOpen: null,
  });
}

// ---------- talks ----------
export function talkEnded(slipWasUnfolded) {
  const m = M();
  m.talks++;
  if (slipWasUnfolded) m.talksWithSlipUnfolded++;
}
export function tabPressed() {
  const m = M();
  if (m.tab.firstPressAtRealSecondsPlayed == null) m.tab.firstPressAtRealSecondsPlayed = Math.round(G.played);
}

// ---------- scripted "find the fact" asks ----------
// At a set moment the player is asked to find one fact in the Ledger and mark it. We time from the Ledger
// opening to the right entry, note whether it was found, and keep keyboard and pad apart.
const isLive = (e) => !e.struck && !e.closed;
export const ASKS = [
  {
    id: 'bus',
    fromGameMinute: 1440 + ASKING.busAskFromHour * 60, // Tue 9.30am
    question: 'Who saw Tom get off the bus on Monday?',
    where: 'People, or the Day book under Monday',
    target: (row) =>
      row.entry &&
      row.entry.kind === 'belief' &&
      G.ev[row.entry.ev] &&
      G.ev[row.entry.ev].kind === 'arrive' &&
      isLive(row.entry),
  },
  {
    id: 'rent',
    fromGameMinute: 2 * 1440 + ASKING.rentAskFromHour * 60, // Wed 12 noon
    question: 'What rent is due, and on what day?',
    where: 'Open',
    target: (row) => row.entry && row.entry.kind === 'open' && row.entry.key === 'rent',
  },
  {
    id: 'call',
    fromGameMinute: ASKING.callAskDayIndex * 1440 + ASKING.callAskFromHour * 60, // Thu 10am
    question: 'What does Ron Kirby call Tom now?',
    where: "People, on Ron Kirby's page",
    target: (row) => row.entry && row.entry.kind === 'call' && row.entry.who === 'ron' && isLive(row.entry),
  },
  {
    id: 'tin',
    fromGameMinute: ASKING.tinAskDayIndex * 1440 + ASKING.tinAskFromHour * 60, // Fri 9am
    question: 'How much is in the tin?',
    where: 'Money',
    target: (row) => row.sum === 'tin',
  },
];

export const activeAsk = () => M().asks.find((a) => a.state === 'asked') || null;

// Called on a slow tick while he is free to act. Puts the next ask on screen when its moment has come.
export function askTick(canAsk) {
  const m = M();
  if (G.settings.asks === false || activeAsk() || !canAsk) return null;
  for (const A of ASKS) {
    if (m.asks.find((a) => a.id === A.id) || G.t < A.fromGameMinute) continue;
    const rec = {
      id: A.id,
      question: A.question,
      askedAtGameMinute: Math.round(G.t),
      askedAtRealSecondsPlayed: Math.round(G.played),
    };
    const exists = A.id === 'tin' ? G.story.flags.tour : book().entries.some((e) => A.target({ entry: e }));
    if (!exists) {
      // the fact is not in his Ledger this week (he never did or heard the thing): logged, not asked
      Object.assign(rec, { state: 'not asked', why: 'no such entry in the Ledger this week' });
      m.asks.push(rec);
      continue;
    }
    Object.assign(rec, { state: 'asked', shownAtMs: nowMs(), openedAtMs: null, wrongMarks: 0 });
    m.asks.push(rec);
    return rec;
  }
  return null;
}

// He has put the cursor on a row and marked it.
export function askMark(row, device) {
  const a = activeAsk();
  if (!a) return null;
  const A = ASKS.find((x) => x.id === a.id);
  if (A.target(row)) {
    Object.assign(a, {
      state: 'answered',
      found: true,
      device,
      realSecondsFromOpenToEntry: a.openedAtMs == null ? null : round1((nowMs() - a.openedAtMs) / 1000),
    });
    delete a.shownAtMs;
    delete a.openedAtMs;
    return 'found';
  }
  a.wrongMarks++;
  return 'wrong';
}
export function askSkip(device) {
  const a = activeAsk();
  if (!a) return;
  Object.assign(a, {
    state: 'answered',
    found: false,
    device: device || 'keyboard',
    realSecondsFromOpenToEntry: null,
    gaveUpAfterRealSeconds: round1((nowMs() - a.shownAtMs) / 1000),
  });
  delete a.shownAtMs;
  delete a.openedAtMs;
}
export const askFor = (id) => ASKS.find((x) => x.id === id);

// ---------- the summary ----------
const round1 = (x) => Math.round(x * 10) / 10;
const round2 = (x) => Math.round(x * 100) / 100;
const median = (xs) => {
  if (!xs.length) return null;
  const s = xs.slice().sort((a, b) => a - b),
    i = Math.floor(s.length / 2);
  return round1(s.length % 2 ? s[i] : (s[i - 1] + s[i]) / 2);
};
const share = (a, b) => (b > 0 ? round2(a / b) : null);

export function measures() {
  const m = M(),
    st = G.stats,
    hours = G.played / 3600,
    faults = bookFaults();
  const byDevice = (dev) => {
    const xs = m.asks.filter((a) => a.state === 'answered' && a.device === dev);
    return {
      asked: xs.length,
      found: xs.filter((a) => a.found).length,
      medianRealSecondsFromOpenToEntry: median(
        xs
          .filter((a) => a.found && a.realSecondsFromOpenToEntry != null)
          .map((a) => a.realSecondsFromOpenToEntry),
      ),
    };
  };
  const notedDone = m.noted.filter(
    (n) =>
      n.followedByOpen != null ||
      G.played - n.atRealSecondsPlayed > LED.notedCountsAsFollowedWithinRealSeconds,
  );
  const said = st.linesSaid || 0,
    typed = st.typed || 0,
    tabOpens = st.linesOpened || 0,
    firstTab = m.tab.firstPressAtRealSecondsPlayed;
  return {
    about:
      'LEDGER loop prototype: Ledger screen test measures. Times are real seconds; money is pence; game time is minutes since Monday 00:00.',
    weekEnded: !!G.story.ended,
    // the whole game (parts 7.5, 7.6): play time booked by activity, and the count of tense and retellable moments
    hourBudget: G.hooks.budget ? G.hooks.budget() : null,
    tension: G.hooks.tension ? G.hooks.tension() : null,
    act: (G.x && G.x.acts && G.x.acts.act) || 1,
    realSecondsPlayed: Math.round(G.played),
    gameMinute: Math.round(G.t),
    ledgerOpens: m.visits.length,
    ledgerOpensPerHourOfPlay: hours > 0 ? round1(m.visits.length / hours) : null,
    medianRealSecondsOpenPerVisit: median(m.visits.map((v) => v.realSecondsOpen)),
    findTheFact: {
      keyboard: byDevice('keyboard'),
      pad: byDevice('pad'),
      hook: byDevice('hook'),
      asks: m.asks.map((a) => Object.assign({}, a)),
    },
    talks: m.talks,
    shareOfTalksWithTheSlipUnfolded: share(m.talksWithSlipUnfolded, m.talks),
    notedLinesShown: m.noted.length,
    shareOfNotedLinesFollowedByAnOpenWithin60Seconds: share(
      notedDone.filter((n) => n.followedByOpen).length,
      notedDone.length,
    ),
    tabPressedInTheFirstHour: firstTab != null && firstTab <= LED.firstHourRealSeconds,
    firstTabAtRealSecondsPlayed: firstTab,
    tabOpens,
    linesSaidFromSuggestions: said,
    linesSaidPerTabOpen: tabOpens > 0 ? round2(said / tabOpens) : null,
    turnsTyped: typed,
    shareOfTurnsFromSuggestions: share(said, said + typed),
    entries: faults.entries,
    entriesStruckThroughThisWeek: faults.entriesStruckThrough,
    entriesRuledOffAsClosed: faults.entriesClosed,
    entriesWithNoSourceEvent: faults.entriesWithNoSourceEvent,
    entriesOverTheWordLimit: faults.entriesOverTheWordLimit,
    visits: m.visits.slice(),
    noted: m.noted.slice(),
  };
}
