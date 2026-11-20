// LEDGER. The Ledger's records: only what Tom himself believes, from what he saw and heard.
import { G, day } from './state.js';
import { RULES } from './rules.js';
import { ROOMS } from './map.js';
import { clipWords, countWords, quid } from './util.js';
import { KINDS } from './kinds.js';
import { eye, attached } from './seeing.js';
import { feel, BR, mkEvent } from './events.js';
import { callName } from './gossip.js';
const NAME = RULES.naming;

export function ledgerSelf(E) {
  if (!G.ledger.acts.find((a) => a.e === E.id)) G.ledger.acts.push({ e: E.id, t: Math.round(G.t), seen: {} });
  bookAct(E);
}

export function ledgerSeen(E, P, basis, from) {
  let a = G.ledger.acts.find((x) => x.e === E.id);
  if (!a) {
    a = { e: E.id, t: Math.round(G.t), seen: {}, other: 1 };
    G.ledger.acts.push(a);
  }
  const id = P.anon ? 'anon' : P.id,
    old = a.seen[id];
  const b = basis === 'saw' && eye(P) && eye(P).win ? 'window' : basis;
  if (!old || BR[b] > BR[old.b]) {
    a.seen[id] = {
      b,
      t: Math.round(G.t),
      from: from || (old && old.from) || null,
      n: (old ? old.n : 0) + (P.anon ? 1 : 0),
    };
    G.ledgerNew = (G.ledgerNew || 0) + 1;
    bookBelief(E, P, b, from);
    if (!old && G.hooks.believed) G.hooks.believed(E, P, b, from);
  } else if (P.anon) old.n++;
}

export function ledgerTalking(A, B) {
  const names = [A, B].filter((p) => !p.anon).map((p) => p.id);
  const key = names.sort().join('+') + ':' + day();
  if (G.ledger.notes.find((n) => n.key === key)) return;
  G.ledger.notes.push({ t: Math.round(G.t), kind: 'talking', key, ids: names, zone: G.tom.zone });
  const pair = [A, B].filter((p) => !p.anon);
  for (const p of pair)
    entry({
      kind: 'note',
      who: p.id,
      what:
        pair.length > 1
          ? `Heads together with ${lowerFirst(shownAs(pair[0] === p ? pair[1].id : pair[0].id))}, eyes on Tom`
          : 'Head together with a passer-by, eyes on Tom',
      how: 'Saw it',
      sure: 'a guess',
    });
  A.glanceT = B.glanceT = RULES.watching.glanceWhileTalkingRealSeconds;
  G.ledgerNew = (G.ledgerNew || 0) + 1;
}

// A note in his own hand. x may give { who, how, sure, ev }: whose page it also goes on, how he knows, and the
// event it came from (without one, the note itself is logged as something he was told or noticed).
export function note(text, kind = 'note', key, x = {}) {
  if (key && G.ledger.notes.find((n) => n.key === key)) return false;
  G.ledger.notes.push({ t: Math.round(G.t), kind, text, key });
  entry({
    kind: kind === 'money' ? 'money' : 'note',
    who: x.who,
    what: text.replace(/\{\{(\w+)\}\}/g, (m, id) => upperFirst(shownAs(id))),
    how: x.how,
    sure: x.sure,
    ev: x.ev,
    by: x.who,
  });
  G.ledgerNew = (G.ledgerNew || 0) + 1;
  return true;
}

export function meet(P) {
  if (G.ledger.met[P.id]) return;
  G.ledger.met[P.id] = 1;
  P.mind.fam = Math.max(P.mind.fam, NAME.familiarityAtLeastOnceMet);
  for (const r of P.mind.mem)
    if (r.who === 'man' && r.src === 'saw' && r.sure > NAME.knownAsTomAboveSureness) {
      r.who = 'tom';
      r.linked = 1;
      feel(P, r);
    }
}

// names: the street's description of someone stands until Tom hears their name
export const knownNames = () => G.ledger.names || (G.ledger.names = Object.assign({}, G.ledger.met));

export const heardNames = () => G.ledger.heard || (G.ledger.heard = {});

export function hearName(P, text) {
  // P has just said this to Tom: their own name is learned, anyone else named has been heard of
  if (!text) return;
  const kn = knownNames(),
    hd = heardNames();
  for (const Q of G.named) {
    if (kn[Q.id] && hd[Q.id]) continue;
    const w = Q.def.name.split(' ');
    if (!w.some((x) => x.length > 2 && new RegExp('\\b' + x + '\\b').test(text))) continue;
    hd[Q.id] = 1;
    if (Q === P && !kn[Q.id]) {
      kn[Q.id] = 1;
      bookName(Q, P.id);
      if (G.hooks.nameLearned) G.hooks.nameLearned(Q);
    }
  }
}

export function learnName(id, by) {
  const kn = knownNames(),
    Q = G.people[id];
  if (!Q || kn[id]) return;
  kn[id] = 1;
  heardNames()[id] = 1;
  bookName(Q, by);
  if (G.hooks.nameLearned) G.hooks.nameLearned(Q);
}

export function heardCall(P) {
  const c = callName(P);
  if (c && G.ledger.calls[P.id] !== c) {
    G.ledger.calls[P.id] = c;
    bookCall(P, c);
  }
  return c;
}

// ---------- the truth, for the end screen ----------
export function truthTable() {
  const rows = [];
  for (const E of G.events) {
    const k = KINDS[E.kind];
    const saw = [],
      heard = [],
      unnamed = [];
    for (const P of G.named) {
      const m = P.mind.by[E.id];
      if (!m) continue;
      if (!attached(m)) {
        unnamed.push(P.id);
        continue;
      }
      (m.src === 'told' ? heard : saw).push(P.id);
    }
    if (!saw.length && !heard.length && !unnamed.length && k.noself) continue;
    const led = G.ledger.acts.find((a) => a.e === E.id);
    rows.push({ E, k, saw, heard, unnamed, believed: led ? Object.keys(led.seen) : [], led });
  }
  return rows;
}

// =====================================================================================================
// The book: every line of the Ledger as an entry. This is the Ledger screen test of November 1990's
// prototype round: each entry says when, what (22 words at most), how Tom knows, how sure he is (in words,
// and only when he is not sure), and the event it came from. A wrong belief is struck through with the day
// and the reason and is never deleted. A closed line in "Open" is ruled off and is never removed.
// =====================================================================================================
const LED = RULES.ledger;

export function book() {
  const L = G.ledger;
  if (!L.book) {
    L.book = { n: 1, entries: [] };
    migrateOldLedger();
  }
  if (L.book.waiting && L.book.waiting.length && !settling) settleUnseen(L.book);
  return L.book;
}

// "Nobody saw" is written only once an act has gone unseen, so far as Tom knows, for
// ledger.unseenHeldAfterGameMinutes. Until then the act waits here. Once written the line is never taken out:
// if a watcher turns up later it is struck through with the day and the reason.
let settling = false;
function settleUnseen(B) {
  settling = true;
  try {
    const due = B.waiting.filter((w) => G.t - w.t >= LED.unseenHeldAfterGameMinutes);
    if (due.length) B.waiting = B.waiting.filter((w) => !due.includes(w));
    for (const w of due) {
      if (B.entries.some((e) => e.kind === 'belief' && e.ev === w.ev)) continue; // somebody saw: nothing to write
      entry({
        kind: 'unseen',
        key: 'unseen:' + w.ev,
        what: 'Nobody saw',
        how: 'Saw nobody',
        sure: 'thinks so',
        ev: w.ev,
        t: w.t,
        place: w.place,
      });
    }
  } finally {
    settling = false;
  }
}

// Something Tom was told, read or noticed: logged as an event so the entry has a source.
export function wordEvent(text, by) {
  const E = mkEvent('word', { text: clipWords(text, LED.entryWordsAtMost), by: by || null });
  return E;
}

const placeNow = () => {
  const t = G.tom;
  return t.space && ROOMS[t.space] ? ROOMS[t.space].name : t.zone;
};

// Write one entry. o: { kind, who, what, how, sure, ev, key, day, amountPence, t, place }
//   kind: 'did' his own act | 'unseen' nobody saw it, so far as he knows | 'belief' what somebody knows |
//         'call' what somebody calls him | 'name' a name learned | 'note' | 'open' something waiting | 'money'
//   key:  entries with a key are kept one live at a time: a new one strikes the old through
export function entry(o) {
  const B = book();
  const what = clipWords(o.what, LED.entryWordsAtMost);
  let ev = o.ev;
  if (ev == null || !G.ev[ev]) ev = wordEvent(what, o.by).id; // no entry without a source event
  if (o.key) {
    const old = B.entries.find((e) => e.key === o.key && !e.struck && !e.closed);
    if (old) {
      if (old.what === what && old.how === o.how && (old.sure || null) === (o.sure || null)) return old;
      if (o.amend) {
        // the same belief, better founded: the line is brought up to date, and what it said before is kept
        (old.was || (old.was = [])).push({ t: old.t, how: old.how, sure: old.sure || null });
        Object.assign(old, { t: o.t ?? Math.round(G.t), how: o.how, sure: o.sure || null, ev });
        return old;
      }
      strike(old, o.why || 'no longer so');
    }
  }
  const e = {
    id: B.n++,
    kind: o.kind,
    t: o.t ?? Math.round(G.t),
    place: o.place ?? placeNow(),
    who: o.who || null,
    what,
    how: o.how || 'Saw it',
    sure: o.sure || null,
    ev,
  };
  if (o.key) e.key = o.key;
  if (o.day) e.day = o.day;
  if (o.amountPence != null) e.amountPence = o.amountPence;
  B.entries.push(e);
  G.ledgerNew = (G.ledgerNew || 0) + 1;
  return e;
}

// A wrong belief: struck through with the day and the reason. Never deleted.
export function strike(e, why) {
  if (!e || e.struck) return;
  e.struck = { t: Math.round(G.t), why: clipWords(why, LED.entryWordsAtMost) };
  G.stats.struck = (G.stats.struck || 0) + 1;
}

// A line in "Open" that is settled: ruled off, with the day and how it ended. Never removed.
export function closeEntry(e, why) {
  if (!e || e.closed) return;
  e.closed = { t: Math.round(G.t), why: clipWords(why || 'Settled', LED.entryWordsAtMost) };
}

const lowerFirst = (x) => x.replace(/^./, (c) => c.toLowerCase());
const upperFirst = (x) => x.replace(/^./, (c) => c.toUpperCase());
const shownAs = (id) => {
  const P = G.people[id];
  if (!P) return id === 'anon' ? 'a passer-by' : 'somebody';
  return knownNames()[id] ? P.def.name : P.def.desc || 'somebody';
};
const firstName = (id) => (knownNames()[id] && G.people[id] ? G.people[id].def.name.split(' ')[0] : null);

// How he came to think it, and how sure that makes him. Sureness is said in words, and only when he is unsure.
function grounds(P, basis, from) {
  const id = P.anon ? 'anon' : P.id,
    name = firstName(id),
    they = P.anon ? 'They' : P.def.sex === 'f' ? 'She' : 'He';
  switch (basis) {
    case 'said':
      return { how: (name || they) + ' says', sure: null };
    case 'there':
      return { how: 'Was there', sure: null };
    case 'saw':
      return { how: 'Saw it', sure: 'thinks so' };
    case 'window':
      return { how: 'Saw it: at the window', sure: 'thinks so' };
    case 'asked':
    case 'bought':
      return { how: (from && firstName(from) ? firstName(from) : 'Somebody') + ' says', sure: 'thinks so' };
    default:
      return { how: 'Saw them talking', sure: 'a guess' };
  }
}

const mineOf = (E) => {
  const P = E.target && G.people[E.target];
  return KINDS[E.kind].mine(P ? Object.assign({}, E, { name: lowerFirst(shownAs(E.target)) }) : E);
};

// His own act goes in the day book. That nobody saw it is written later, if it stays so (see settleUnseen).
function bookAct(E) {
  const B = book();
  if (B.entries.find((e) => e.kind === 'did' && e.ev === E.id)) return;
  entry({ kind: 'did', what: mineOf(E), how: 'Did it', ev: E.id, t: Math.round(E.t), place: E.zone });
  (B.waiting || (B.waiting = [])).push({ ev: E.id, t: Math.round(E.t), place: E.zone }); // "Nobody saw", if it stays so
}

// What somebody knows of an act: one line on their page, brought up to date when he learns more.
function bookBelief(E, P, basis, from) {
  const id = P.anon ? 'anon' : P.id,
    g = grounds(P, basis, from);
  bookAct(E);
  entry({
    kind: 'belief',
    who: id,
    key: 'belief:' + E.id + ':' + id,
    what: 'Knows: ' + lowerFirst(mineOf(E)),
    how: g.how,
    sure: g.sure,
    ev: E.id,
    amend: true,
  });
  const B = book(),
    none = B.entries.find((e) => e.key === 'unseen:' + E.id && !e.struck);
  // Seen before "Nobody saw" was written: it is not written. Learned after: it was a wrong belief, and the line
  // stays, struck through with the day and the reason. A line once written is never taken out.
  if (B.waiting) B.waiting = B.waiting.filter((w) => w.ev !== E.id);
  if (none) strike(none, upperFirst(shownAs(id)) + (basis === 'talking' ? ' may have heard' : ' knows'));
}

// What somebody calls him. A new name strikes the old one through.
function bookCall(P, c) {
  entry({
    kind: 'call',
    who: P.id,
    key: 'call:' + P.id,
    what: `Calls Tom '${c}'`,
    how: 'Heard it',
    why: `Now calls Tom '${c}'`,
    by: P.id,
  });
}

function bookName(Q, by) {
  if (book().entries.find((e) => e.kind === 'name' && e.who === Q.id)) return;
  const she = Q.def.sex === 'f' ? 'She' : 'He';
  entry({
    kind: 'name',
    who: Q.id,
    what: 'Name: ' + Q.def.name,
    how: by && by !== Q.id && firstName(by) ? firstName(by) + ' says' : she + ' says',
    by: by || Q.id,
  });
}

// ---------- Open: what is waiting on him ----------
// A day is given only if somebody said it to him. Each item has a key; when the game no longer lists it, its
// line is ruled off with the reason.
export function openNow() {
  const f = G.story.flags,
    o = [],
    m = G.money,
    kn = knownNames();
  const nm = (id) => upperFirst(shownAs(id));
  if (f.ask1 === 'think')
    o.push({
      key: 'ask1',
      who: 'ron',
      what: `${nm('ron')} wants an answer about the Monday bag`,
      day: 'Tonight, before the last ferry',
      how: 'Ron says',
    });
  const j = G.story.job;
  if (j && j.st !== 'done' && j.st !== 'missed' && j.st !== 'lost')
    o.push({
      key: 'job' + j.n,
      who: 'ron',
      what:
        j.n === 1
          ? "The Monday bag: ferry landing shelter to Metcalfe's back door"
          : "The Tuesday parcel: smoke house door to Rita's side door",
      day: j.n === 1 ? 'Tonight, after the last ferry, 10.30pm' : 'Tonight, after 10pm',
      how: 'Ron says',
    });
  if (f.teaInvited && !f.tea)
    o.push({
      key: 'tea',
      who: 'ada',
      what: `Tea with ${lowerFirst(nm('ada'))}, her door opposite Mickey's`,
      day: 'Wed, 7pm',
      how: 'Passed along the street',
    });
  if (f.ask2 === 'yes' && !f.job3)
    o.push({
      key: 'job3',
      who: kn.dennis ? 'dennis' : null,
      what: `Collect ${quid(RULES.prices.owedByIvesonPence)} from Iveson at the scrapyard, west end of the quay`,
      day: 'Tonight, 7pm',
      how: 'Ron says',
    });
  if (f.alison && f.alisonAns == null)
    o.push({
      key: 'alison',
      who: 'alison',
      what: `${nm('alison')} asked about the warehouse fire. No answer given yet`,
      how: 'She asked',
    });
  if (f.tour && !f.rent)
    o.push({
      key: 'rent',
      who: 'sheila',
      what: `Rent, ${quid(RULES.money.rentPence)}, on the office and the flat over it`,
      day: f.rentBySix ? 'Fri, by 6pm' : 'Fri',
      how: 'Sheila says',
    });
  if (f.tour && !f.choice)
    o.push({
      key: 'choice',
      who: 'sheila',
      what: `${nm('sheila')}'s question: wind it down, or take it all on`,
      day: f.sheilaAsked ? 'Today' : null,
      how: 'Sheila says',
    });
  if (m.dirty > 0 && f.tour)
    o.push({
      key: 'tin',
      who: 'sheila',
      what: `Money in the tin that never came off a meter. ${nm('sheila')} can put it through the fare book`,
      how: 'Counted it',
    });
  if (G.hooks.openRows) G.hooks.openRows(o); // the whole game's systems add what is open with them (debts: game/book.js)
  if (f.oweAgar > 0)
    o.push({
      key: 'agar',
      who: null,
      what: `Agar & Co want ${quid(f.oweAgar)} for a brief nobody asked for`,
      how: "Agar's clerk says",
    });
  if (f.tour && !(G.x && G.x.book)) // the one-shot: the debts are the debt book's own rows now (game/book.js), written when Sheila has shown it

    for (const id in G.debts) {
      const x = G.debts[id];
      if (x.st === 'open')
        o.push({
          key: 'debt:' + id,
          who: kn[id] ? id : null,
          what: `${G.people[id].def.name} owes the book ${quid(x.owed)}`,
          how: "Mickey's book",
        });
    }
  return o;
}

function closedWhy(key) {
  const f = G.story.flags,
    j = G.story.job;
  if (key === 'ask1') return f.ask1 === 'yes' ? 'Said yes' : f.ask1 === 'no' ? 'Said no' : 'The time passed';
  if (key === 'job1' || key === 'job2') {
    const st = f[key];
    return st === 'done'
      ? 'Delivered'
      : st === 'lost'
        ? 'The bag was taken'
        : j && j.st === 'missed'
          ? 'Never turned up'
          : 'Over';
  }
  if (key === 'tea') return f.tea === 'snub' ? 'Never went' : f.tea === 'late' ? 'Went late' : 'Went';
  if (key === 'job3') return 'Done';
  if (key === 'alison') return 'Answered';
  if (key === 'rent') return 'Paid';
  if (key === 'choice') return 'Answered';
  if (key === 'tin') return 'Nothing left in the tin';
  if (key === 'agar') return 'Paid';
  if (key.startsWith('debt:')) {
    const d = G.debts[key.slice(5)];
    return d && d.st === 'forgiven' ? 'Struck out of the book' : 'Paid';
  }
  return 'Settled';
}

export function syncOpen() {
  if (G.story.phase !== 'play') return;
  const B = book(),
    now = openNow(),
    keys = new Set(now.map((x) => x.key));
  for (const x of now) {
    const live = B.entries.find((e) => e.kind === 'open' && e.key === x.key && !e.closed && !e.struck);
    if (!live)
      entry({
        kind: 'open',
        key: x.key,
        who: x.who,
        what: x.what,
        how: x.how,
        day: x.day || undefined,
        by: x.who,
      });
    else if (live.what !== x.what) {
      // the sum or the terms have changed: the old line is struck through and the new one written under it
      strike(live, 'Changed');
      entry({
        kind: 'open',
        key: x.key,
        who: x.who,
        what: x.what,
        how: x.how,
        day: x.day || undefined,
        by: x.who,
      });
    } else {
      if (x.day && live.day !== x.day) live.day = x.day;
      if (x.who && !live.who) live.who = x.who;
    }
  }
  for (const e of B.entries)
    if (e.kind === 'open' && !e.closed && !e.struck && !keys.has(e.key)) closeEntry(e, closedWhy(e.key));
}

// ---------- Money: pounds and pence, only sums Tom knows ----------
export function moneyNow() {
  const m = G.money,
    f = G.story.flags,
    o = [];
  o.push({ sum: 'pocket', what: 'In his pocket', amountPence: m.clean, how: 'Counted it' });
  if (f.tour || m.dirty > 0)
    o.push({ sum: 'tin', what: 'In the tin, never off a meter', amountPence: m.dirty, how: 'Counted it' });
  if (m.fareCount > 0)
    o.push({
      sum: 'fares',
      what: `Fares taken this week (${m.fareCount})`,
      amountPence: m.fares,
      how: 'The fare book',
    });
  if (m.washed > 0)
    o.push({
      sum: 'washed',
      what: 'Put through the fare book so far',
      amountPence: m.washed,
      how: 'Sheila says',
    });
  if (m.booksOff > 0)
    o.push({ sum: 'off', what: 'More than the book can hide', amountPence: m.booksOff, how: 'Sheila says' });
  if (f.tour && (!G.x || !G.x.book || G.x.book.shown)) {
    let owed = 0;
    for (const id in G.debts) if (G.debts[id].st === 'open') owed += G.debts[id].owed;
    o.push({ sum: 'owed', what: "Owed to Mickey's book, all told", amountPence: owed, how: "Mickey's book" });
    if (!f.rent)
      o.push({ sum: 'rent', what: 'Rent due', amountPence: RULES.money.rentPence, how: 'Sheila says' });
  }
  if (f.oweAgar > 0)
    o.push({ sum: 'agar', what: 'Owed to Agar & Co', amountPence: f.oweAgar, how: "Agar's clerk says" });
  return o;
}

// ---------- saves from before the book ----------
function migrateOldLedger() {
  const L = G.ledger;
  for (const a of L.acts || []) {
    const E = G.ev[a.e];
    if (!E || !KINDS[E.kind]) continue;
    if (!KINDS[E.kind].noself) bookAct(E);
    for (const id in a.seen) {
      const P = id === 'anon' ? { anon: true, def: {} } : G.people[id];
      if (P) bookBelief(E, P, a.seen[id].b, a.seen[id].from);
    }
  }
  for (const n of L.notes || [])
    if (n.text)
      entry({
        kind: n.kind === 'money' ? 'money' : 'note',
        what: n.text.replace(/\{\{(\w+)\}\}/g, (m, id) => upperFirst(shownAs(id))),
        how: 'Written before',
        t: n.t,
      });
  for (const id in L.calls || {}) if (G.people[id]) bookCall(G.people[id], L.calls[id]);
  for (const id in L.names || L.met || {}) if (G.people[id]) bookName(G.people[id]);
}

// The checks the measures need: every entry has a source event, and no entry runs past the word limit.
export function bookFaults() {
  const B = book();
  return {
    entries: B.entries.length,
    entriesWithNoSourceEvent: B.entries.filter((e) => e.ev == null || !G.ev[e.ev]).length,
    entriesOverTheWordLimit: B.entries.filter((e) => countWords(e.what) > LED.entryWordsAtMost).length,
    entriesStruckThrough: B.entries.filter((e) => e.struck).length,
    entriesClosed: B.entries.filter((e) => e.closed).length,
  };
}
