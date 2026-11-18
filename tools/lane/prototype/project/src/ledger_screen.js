// LEDGER. The Ledger screen, the slip beside a talk, and the Noted line. It shows only what Tom believes.
import { RULES } from './rules.js';
import { activeAsk, askMark, askSkip } from './measures.js';
import { book, syncOpen, moneyNow, knownNames } from './ledger.js';
import { G, day, hour } from './state.js';
import { money, hhmm, DAYS3, esc, cap, listAnd, quid, clockText, dateText } from './util.js';
import { KINDS, whenTxt } from './kinds.js';
import { BLD, ROADS, SETTS, WATER, LAMPS } from './map.js';
import { tomName } from './ui.js';

const LED = RULES.ledger;

const nm = (id) =>
  id === 'anon' ? 'passers-by' : id === 'someone' ? 'a passer-by' : G.people[id] ? tomName(G.people[id]) : id;

export const low = (x) => x.replace(/^(The|A|An) /, (m) => m.toLowerCase());

const nmIn = (id) => low(nm(id)); // a name or a description, for the middle of a sentence

const tag = (x) => String(x).replace(/\{\{(\w+)\}\}/g, (m, id) => cap(nm(id)));

export const real = (id) => (id === 'someone' ? 'a passer-by' : G.people[id] ? G.people[id].def.name : id);

export const stamp = (t) => `${DAYS3[Math.floor(t / 1440) % 7]} ${hhmm((t % 1440) / 60)}`;

export const gkey = (E) => E.kind + ':' + Math.floor((E.t - 300) / 1440) + ':' + (E.target || '');

const BASIS = {
  saw: 'saw me, and I saw them look',
  window: 'was at a window',
  said: 'said it to my face',
  there: 'was there',
  asked: 'told me when I asked',
  bought: 'according to what I paid for',
  talking: 'was talking',
};

function groups() {
  // Tom's own acts, merged by kind and night
  const g = new Map();
  for (const a of G.ledger.acts) {
    const E = G.ev[a.e];
    if (!E) continue;
    const k = gkey(E);
    if (!g.has(k)) g.set(k, { E, zones: new Set(), seen: {}, t: E.t });
    const x = g.get(k);
    x.zones.add(E.zone);
    for (const id in a.seen) {
      const s = a.seen[id];
      if (!x.seen[id] || s.t > x.seen[id].t) x.seen[id] = s;
    }
  }
  return [...g.values()].sort((a, b) => b.t - a.t);
}

// ---------- Tom's beliefs, by person and by event ----------
const SURE = {
  said: 'sure',
  there: 'sure',
  bought: 'thinks so',
  asked: 'thinks so',
  saw: 'thinks so',
  window: 'thinks so',
  talking: 'guesses',
};

export const her = (id) => {
  const P = G.people[id];
  return !P || id === 'anon' ? 'them' : P.def.sex === 'f' ? 'her' : 'him';
};

export function how(id, x) {
  // how he came to think it
  const w = whenTxt(x.t),
    o = her(id),
    by = x.from ? cap(nm(x.from)) : null;
  switch (x.b) {
    case 'window':
      return `saw ${o} at ${o === 'them' ? 'a' : o === 'her' ? 'her' : 'his'} window, ${w}`;
    case 'saw':
      return `saw ${o} looking, ${w}`;
    case 'talking':
      return `saw ${o} with ${o === 'them' ? 'their heads' : o === 'her' ? 'her head' : 'his head'} together with somebody, eyes on me, ${w}`;
    case 'said':
      return `${o === 'them' ? 'they' : o === 'her' ? 'she' : 'he'} said it to my face, ${w}`;
    case 'there':
      return `${o === 'them' ? 'they were' : o === 'her' ? 'she was' : 'he was'} there`;
    default:
      return by
        ? `${by} said ${o === 'them' ? 'they' : o === 'her' ? 'she' : 'he'} had heard`
        : `I was told, ${w}`;
  }
}

const mineOf = (g) =>
  KINDS[g.E.kind].mine(
    Object.assign(
      {},
      g.E,
      { zone: listAnd([...g.zones]) },
      g.E.target && G.people[g.E.target] ? { name: nmIn(g.E.target) } : null,
    ),
  );

function beliefsOf(id) {
  const out = [];
  for (const g of groups()) {
    const x = g.seen[id];
    if (x)
      out.push({
        t: x.t,
        text: mineOf(g),
        how: how(id, x),
        sure: SURE[x.b] || 'guesses',
        when: whenTxt(g.E.t),
      });
  }
  return out.sort((a, b) => b.t - a.t);
}

// the one line shown when Tom comes to believe something new
export function believedLine(E, P, b) {
  const K = E && KINDS[E.kind];
  if (!K || E.kind === 'inherit' || E.kind === 'good_word' || E.kind === 'ellis_asked') return null;
  let t = K.mine(Object.assign({}, E, E.target && G.people[E.target] ? { name: nmIn(E.target) } : null));
  if (E.kind === 'patched') t = 'Were patched up in the caff kitchen';
  t = t
    .replace(/^./, (c) => c.toLowerCase())
    .replace(/^was /, 'were ')
    .replace(/\bmyself\b/g, 'yourself')
    .replace(/\bmy\b/g, 'your')
    .replace(/\bme\b/g, 'you')
    .replace(/\bI am\b/g, 'you are')
    .replace(/\bI\b/g, 'you');
  const who = !P || P.anon ? 'somebody passing' : nmIn(P.id),
    sure = b === 'said' || b === 'there';
  return `Noted in the Ledger: ${who} ${sure ? 'knows' : b === 'talking' || b === 'asked' || b === 'bought' ? 'may have heard' : 'may have seen'} that you ${t}.`;
}

// ---------- the slip beside a talk, and what the suggest call is told ----------
const liveOf = (id) =>
  book()
    .entries.filter((e) => e.who === id && !e.struck && !e.closed)
    .sort((x, y) => y.t - x.t || y.id - x.id);
const sureWords = (e) => (e.sure ? ' ' + cap(e.sure) + '.' : '');
const dot = (x) => String(x).replace(/[.\s]+$/, '') + '.';

// Folded, the slip is its heading and nothing else. Unfolded: two or three lines of what Tom believes this
// person knows, and anything open between them. Only his beliefs.
export function slipHTML(P, unfolded) {
  const id = P.anon ? 'anon' : P.id,
    head = `<b>FROM THE LEDGER · F2 ${unfolded ? 'FOLDS' : 'UNFOLDS'}</b>`;
  if (!unfolded) return head;
  const mine = liveOf(id),
    b = mine.filter((e) => e.kind === 'belief' || e.kind === 'call').slice(0, 3),
    o = mine.filter((e) => e.kind === 'open').slice(0, 2);
  return (
    head +
    (b.length
      ? b
          .map((e) => `<div>${esc(dot(e.what))} <small>${esc(dot(e.how))}${esc(sureWords(e))}</small></div>`)
          .join('')
      : '<div>Nothing written about this one yet.</div>') +
    o.map((e) => `<div>Open: ${esc(dot(e.what))}${e.day ? ' ' + esc(dot(e.day)) : ''}</div>`).join('')
  );
}

// the same, as plain sentences: all the suggest call is ever told
export function tomKnows(P) {
  const id = P.anon ? 'anon' : P.id,
    out = [];
  for (const e of liveOf(id).slice(0, 7)) {
    if (e.kind === 'belief')
      out.push(
        `He ${e.sure === 'a guess' ? 'guesses' : e.sure ? 'thinks' : 'is sure'} this person ${e.what.replace(/^Knows: /, 'knows that he ')} (${e.how}).`,
      );
    else if (e.kind === 'open')
      out.push('Open between them: ' + dot(e.what) + (e.day ? ' ' + dot(e.day) : ''));
    else if (e.kind === 'call') out.push(`This person ${e.what.replace(/^Calls Tom/, 'has called him')}.`);
  }
  const kn = Object.keys(G.ledger.names || {})
    .filter((k) => G.people[k] && k !== P.id)
    .map((k) => G.people[k].def.name);
  if (kn.length)
    out.push(
      'People he knows by name: ' + kn.slice(0, 12).join(', ') + '. His late uncle was Mickey Suddaby.',
    );
  return out;
}

// =====================================================================================================
// The Ledger screen test. Four parts: People, Day book, Open, Money. Words only: no percentages, bars,
// colours or icons. L opens it anywhere and L or Esc closes it; Q and E change part; it opens on the part
// last used. Up and Down move along the entries, Left and Right turn the page, a typed letter jumps in People,
// and "/" then a letter jumps to any letter (E, L and Q are keys of their own).
// =====================================================================================================
export const PARTS = ['people', 'daybook', 'open', 'money'];
const PART_NAME = { people: 'People', daybook: 'Day book', open: 'Open', money: 'Money' };
export const LS = { part: 'people', person: null, dayIdx: null, cur: 0, rows: [], said: '', jump: false };

const when = (t) => dateText(t) + ', ' + clockText(t);
const heading = (id) => {
  if (id === 'anon') return { name: 'Passers-by', was: null, sort: 'passers-by' };
  const P = G.people[id],
    desc = cap(P.def.desc || 'somebody');
  if (knownNames()[id]) return { name: P.def.name, was: desc, sort: P.def.name.toLowerCase() };
  return { name: desc, was: null, sort: desc.replace(/^(The|A|An) /, '').toLowerCase() };
};

export function peoplePages() {
  const last = {};
  for (const e of book().entries) if (e.who) last[e.who] = Math.max(last[e.who] || 0, e.t);
  for (const id in knownNames()) if (!(id in last)) last[id] = 0;
  for (const id in G.ledger.met || {}) if (!(id in last)) last[id] = 0;
  return Object.keys(last)
    .filter((id) => id === 'anon' || G.people[id])
    .sort((x, y) => last[y] - last[x] || heading(x).sort.localeCompare(heading(y).sort));
}

function sourceText(e) {
  const E = G.ev[e.ev];
  if (!E) return 'No source event.';
  const told = /says$|^Heard it|^Said it|asked$|^Passed along|^Overheard/.test(e.how || '');
  const kind =
    E.kind !== 'word'
      ? 'his own act'
      : told
        ? E.by && G.people[E.by]
          ? 'said by ' + nmIn(E.by)
          : 'said to him'
        : 'noticed';
  return `Source: event ${E.id}, ${kind}, ${when(E.t)}, ${E.zone}.`;
}

function rowHTML(r, i) {
  const cur = i === LS.cur ? ' cur' : '';
  if (r.sum)
    return `<div class="le${cur}" data-row="${i}"><div class="lt sum"><span>${esc(r.what)}</span><b>${quid(r.amountPence)}</b></div><div class="lh">${esc(dot(r.how))}</div></div>`;
  const e = r.entry,
    what = esc(dot(r.what || e.what)) + (e.day ? ' ' + esc(dot(e.day)) : ''),
    cls = (r.sub ? ' sub' : '') + (e.closed ? ' ruled' : '');
  return (
    `<div class="le${cur}${cls}" data-row="${i}"><div class="lw">${when(e.t)} · ${esc(e.place || '')}</div>` +
    `<div class="lt">${e.struck ? '<s>' + what + '</s>' : what}</div>` +
    `<div class="lh">${esc(dot(e.how))}${esc(sureWords(e))} ${esc(sourceText(e))}</div>` +
    (e.struck
      ? `<div class="ls">Struck through ${dateText(e.struck.t)}: ${esc(dot(e.struck.why))}</div>`
      : '') +
    (e.closed ? `<div class="ls">Closed ${dateText(e.closed.t)}: ${esc(dot(e.closed.why))}</div>` : '') +
    '</div>'
  );
}
const newest = (x, y) => y.t - x.t || y.id - x.id;

function buildRows() {
  const B = book(),
    rows = [];
  if (LS.part === 'people') {
    const pages = peoplePages();
    if (!pages.includes(LS.person)) LS.person = pages[0] || null;
    if (LS.person)
      for (const e of B.entries.filter((x) => x.who === LS.person).sort(newest)) rows.push({ entry: e });
  } else if (LS.part === 'daybook') {
    if (LS.dayIdx == null || LS.dayIdx > day()) LS.dayIdx = day();
    const mine = B.entries
      .filter((e) => Math.floor(e.t / 1440) === LS.dayIdx && !['belief', 'open', 'unseen'].includes(e.kind))
      .sort(newest);
    for (const e of mine) {
      rows.push({ entry: e });
      if (e.kind !== 'did') continue;
      for (const x of B.entries
        .filter((y) => y.ev === e.ev && (y.kind === 'unseen' || y.kind === 'belief'))
        .sort((p, q) => p.id - q.id))
        rows.push({ entry: x, sub: true, what: x.kind === 'belief' ? cap(nm(x.who)) + ' knows' : x.what });
    }
  } else if (LS.part === 'open') {
    const all = B.entries.filter((e) => e.kind === 'open');
    for (const e of all.filter((x) => !x.closed && !x.struck).sort(newest)) rows.push({ entry: e });
    for (const e of all
      .filter((x) => x.closed || x.struck)
      .sort((x, y) => (y.closed || y.struck).t - (x.closed || x.struck).t))
      rows.push({ entry: e });
  } else {
    for (const m of moneyNow()) rows.push(m);
    for (const e of B.entries.filter((x) => x.kind === 'money').sort(newest)) rows.push({ entry: e });
  }
  LS.rows = rows;
  LS.cur = Math.max(0, Math.min(LS.cur, rows.length - 1));
  return rows;
}

// The week so far, in five lines at most: a line a day, the two acts of that day that matter most.
function weekSoFar() {
  const B = book(),
    lines = [];
  for (let d = Math.max(0, day() - (LED.weekSoFarLinesAtMost - 1)); d <= day(); d++) {
    const top = B.entries
      .filter((e) => e.kind === 'did' && Math.floor(e.t / 1440) === d && G.ev[e.ev])
      .sort((x, y) => KINDS[G.ev[y.ev].kind].sev - KINDS[G.ev[x.ev].kind].sev)
      .slice(0, 2)
      .map((e) => dot(e.what));
    lines.push(`${dateText(d * 1440)}: ${top.length ? top.join(' ') : 'Nothing written.'}`);
  }
  return lines;
}

export function ledgerHTML() {
  syncOpen();
  const rows = buildRows(),
    ask = activeAsk();
  const tabs = PARTS.map(
    (k) => `<button class="${k === LS.part ? 'on' : ''}" data-part="${k}">${PART_NAME[k]}</button>`,
  ).join('');
  let side = '',
    main = '';
  if (LS.part === 'people') {
    const pages = peoplePages(),
      letters = [...new Set(pages.map((id) => heading(id).sort[0].toUpperCase()))].sort();
    side =
      `<div class="lidx">${letters.map((c) => `<u data-letter="${c}">${c}</u>`).join(' ') || ''}</div>` +
      (letters.length ? '<div class="was">/ then a letter jumps there</div>' : '') +
      pages
        .map(
          (id) =>
            `<button class="lpg${id === LS.person ? ' on' : ''}" data-page="${id}">${esc(heading(id).name)}</button>`,
        )
        .join('');
    if (LS.person) {
      const h = heading(LS.person);
      main =
        `<h2>${esc(h.name)}</h2>` +
        (h.was
          ? `<div class="was"><s>${esc(h.was)}</s></div>`
          : '<div class="was">No name learned yet.</div>');
    } else
      main =
        '<div class="lh">Nobody yet. A page is opened for each person Tom meets or catches looking.</div>';
  } else if (LS.part === 'daybook') {
    const days = [];
    for (let d = day(); d >= 0; d--) days.push(d);
    side = days
      .map(
        (d) =>
          `<button class="lpg${d === LS.dayIdx ? ' on' : ''}" data-page="${d}">${dateText(d * 1440)}</button>`,
      )
      .join('');
    main = `<div class="week"><b>The week so far</b><br>${weekSoFar().map(esc).join('<br>')}</div><h2>${dateText(LS.dayIdx * 1440)}</h2>`;
  } else if (LS.part === 'open') {
    main =
      '<h2>Waiting on Tom</h2><div class="was">A day is written only where somebody said one. Closed lines are ruled off and stay.</div>';
  } else {
    main = '<h2>Money</h2><div class="was">Pounds and pence. Only sums Tom knows.</div>';
  }
  main += rows.map(rowHTML).join('') || '<div class="lh">Nothing written here yet.</div>';
  if (LS.part === 'open')
    main +=
      '<h2 style="margin-top:14px">The Hook</h2><canvas id="lmap" width="980" height="620" style="max-width:100%;border:1.5px solid #111"></canvas>';
  const askLine = ask
    ? `<div class="lask"><b>Playtest ask:</b> ${esc(ask.question)} Put the cursor on the entry and press Enter (pad: A). Backspace gives up.${LS.said ? ' <b>' + esc(LS.said) + '</b>' : ''}</div>`
    : LS.said
      ? `<div class="lask"><b>${esc(LS.said)}</b></div>`
      : '';
  return (
    `<h1>THE LEDGER</h1><div class="ltabs"><span class="k">Q</span>${tabs}<span class="k">E</span><span style="flex:1"></span><button data-close="1">Close</button></div>${askLine}` +
    `<div class="lbody">${side ? `<div class="lside">${side}</div>` : ''}<div class="lmain" id="lmain">${main}</div></div>` +
    `<div class="lfoot"><span>Only what Tom believes, from what he saw and heard. Eyes he did not notice are not in here.</span><span>Up, Down: entries. Left, Right: page.${LS.part === 'people' ? ' A letter: jump.' : ''} L or Esc: close.</span></div>`
  );
}

// Keys and pad buttons while the Ledger is open. Returns 'close' when it should shut, true when used.
export function ledgerInput(code, device = 'keyboard') {
  const step = (n) => {
    LS.cur = Math.max(0, Math.min(LS.cur + n, LS.rows.length - 1));
  };
  const page = (n) => {
    if (LS.part === 'people') {
      const pages = peoplePages(),
        i = pages.indexOf(LS.person);
      LS.person = pages[Math.max(0, Math.min(i + n, pages.length - 1))] || null;
    } else if (LS.part === 'daybook') LS.dayIdx = Math.max(0, Math.min(LS.dayIdx - n, day()));
    LS.cur = 0;
  };
  // "/" and then a letter jumps to that letter in People: any letter, E, L and Q among them, which by
  // themselves change part or close the book. Esc, or any other key, lets the jump go.
  if (LS.jump) {
    LS.jump = false;
    LS.said = '';
    if (/^Key[A-Z]$/.test(code)) {
      if (!jumpTo(code.slice(3))) LS.said = 'Nobody under ' + code.slice(3) + ' yet.';
      return true;
    }
    if (code === 'Escape' || code === 'Slash') return true;
  }
  if (code === 'KeyL' || code === 'Escape') return 'close';
  LS.said = '';
  if (code === 'Slash' || code === 'NumpadDivide') {
    if (LS.part !== 'people') LS.part = 'people';
    LS.jump = true;
    LS.said = 'Jump to which letter?';
    return true;
  }
  if (code === 'KeyQ' || code === 'KeyE') {
    LS.part = PARTS[(PARTS.indexOf(LS.part) + (code === 'KeyE' ? 1 : PARTS.length - 1)) % PARTS.length];
    LS.cur = 0;
  } else if (code === 'ArrowDown') step(1);
  else if (code === 'ArrowUp') step(-1);
  else if (code === 'ArrowRight') page(1);
  else if (code === 'ArrowLeft') page(-1);
  else if (code === 'Enter') {
    const r = LS.rows[LS.cur],
      res = r ? askMark(r, device) : null;
    if (res === 'found') LS.said = 'That is the one. Thank you.';
    else if (res === 'wrong') LS.said = 'Not that one.';
  } else if (code === 'Backspace') {
    if (activeAsk()) {
      askSkip(device);
      LS.said = 'Left unanswered.';
    }
  } else if (/^Key[A-Z]$/.test(code) && LS.part === 'people') jumpTo(code.slice(3));
  else return false;
  return true;
}
// A typed letter in People: the first page under that letter, A to Z.
export function jumpTo(letter) {
  const hit = peoplePages()
    .map((id) => ({ id, s: heading(id).sort }))
    .sort((x, y) => x.s.localeCompare(y.s))
    .find((x) => x.s[0] === letter.toLowerCase());
  if (hit) {
    LS.person = hit.id;
    LS.cur = 0;
  }
  return !!hit;
}
export function ledgerClick(target, device = 'keyboard') {
  const part = target.closest('[data-part]'),
    pg = target.closest('[data-page]'),
    let_ = target.closest('[data-letter]'),
    row = target.closest('[data-row]');
  if (target.closest('[data-close]')) return 'close';
  LS.said = '';
  if (part) {
    LS.part = part.dataset.part;
    LS.cur = 0;
  } else if (pg) {
    if (LS.part === 'people') LS.person = pg.dataset.page;
    else LS.dayIdx = +pg.dataset.page;
    LS.cur = 0;
  } else if (let_) jumpTo(let_.dataset.letter);
  else if (row) {
    const i = +row.dataset.row;
    if (i === LS.cur && activeAsk()) return ledgerInput('Enter', device); // a second tap on the entry marks it
    LS.cur = i;
  } else return false;
  return true;
}
// What the hook reads: the rows on screen, in plain values.
export function ledgerRows() {
  return buildRows().map((r, i) =>
    r.sum
      ? { row: i, sum: r.sum, what: r.what, amountPence: r.amountPence, how: r.how }
      : {
          row: i,
          entryId: r.entry.id,
          kind: r.entry.kind,
          who: r.entry.who,
          whenGameMinute: r.entry.t,
          when: when(r.entry.t),
          place: r.entry.place,
          what: r.what || r.entry.what,
          day: r.entry.day || null,
          how: r.entry.how,
          sure: r.entry.sure || 'sure',
          sourceEvent: r.entry.ev,
          struckThrough: r.entry.struck ? { day: dateText(r.entry.struck.t), why: r.entry.struck.why } : null,
          closed: r.entry.closed ? { day: dateText(r.entry.closed.t), why: r.entry.closed.why } : null,
        },
  );
}

export function drawMap(cv) {
  if (!cv) return;
  const x = cv.getContext('2d'),
    W = cv.width,
    H = cv.height,
    KEYW = 262,
    x0 = -128,
    x1 = 160,
    z0 = -226,
    z1 = 100,
    s = Math.min((W - KEYW) / (z1 - z0), H / (x1 - x0)),
    MW = (z1 - z0) * s;
  // drawn on its side: north to the left, so the long street fits the page. The crowded street is numbered, with the key beside it.
  const px = (wx, wz) => [(wz - z0) * s, (x1 - wx) * s],
    HAND = '"Patrick Hand", "Comic Sans MS", cursive';
  x.fillStyle = '#e4dcc4';
  x.fillRect(0, 0, W, H);
  x.save();
  x.beginPath();
  x.rect(0, 0, MW, H);
  x.clip();
  x.fillStyle = '#b9c4c4';
  for (const w of WATER) {
    const [a, b] = px(Math.min(x1, w.x1), Math.max(z0, w.z0)),
      [c, d] = px(Math.max(x0, w.x0), Math.min(z1, w.z1));
    x.fillRect(a, b, c - a, d - b);
  }
  const rect = (r, col) => {
    const [a, b] = px(r.x1, r.z0),
      [c, d] = px(r.x0, r.z1);
    x.fillStyle = col;
    x.fillRect(a, b, c - a, d - b);
  };
  SETTS.forEach((r) => rect(r, '#d2c9ad'));
  ROADS.forEach((r) => rect(r, '#f4efdf'));
  for (const b of BLD) {
    rect(b, b.burnt ? '#5a4a40' : b.enter ? '#9a8a66' : '#bfb596');
  }
  x.fillStyle = '#c8641a';
  for (const l of LAMPS) {
    const [a, b] = px(l.x, l.z);
    x.beginPath();
    x.arc(a, b, 2, 0, 7);
    x.fill();
  }
  x.textAlign = 'center';
  const lab = (t, wx, wz, rot) => {
    const [a, b] = px(wx, wz);
    x.save();
    x.translate(a, b);
    if (rot) x.rotate(rot);
    x.fillText(t, 0, 4);
    x.restore();
  };
  x.fillStyle = '#28357a';
  x.font = '14px ' + HAND;
  for (const [t, wx, wz] of [
    ["Iveson's yard", -104, 31],
    ['ferry', -55, 72],
    ['fish dock', 89, 74],
    ['warehouse row', 71, 14],
    ['school', -95, -21],
    ['market', -27, -160],
    ['bank', 15, -139],
    ['video', 15, -157],
    ['market hall', -28, -206],
  ])
    lab(t, wx, wz);
  lab('station', 27, -216, -Math.PI / 2);
  x.fillStyle = '#efe7d0';
  lab('No 4', 119, 31.5);
  x.font = '15px ' + HAND;
  x.fillStyle = '#111';
  lab('Q U A Y   S T R E E T', 0, -12);
  lab('the quay', -70, 48, -Math.PI / 2);
  lab('Chapel Lane', -45, -18.5, -Math.PI / 2);
  lab('back lane', 29.5, 6);
  lab('C O P P E R   R O W', 0, -168);
  lab('the Cut', 60, -107, -Math.PI / 2);
  lab('T H E   H U M B E R', 20, 84, -Math.PI / 2);
  x.font = 'bold 13px ' + HAND;
  x.fillStyle = '#14204f';
  MAPKEY.forEach(([, wx, wz], i) => lab(String(i + 1), wx, wz));
  const t = G.tom,
    [a, b] = px(
      t.inCar ? G.car.x : t.space === 'street' ? t.x : 0,
      t.inCar ? G.car.z : t.space === 'street' ? t.z : 0,
    );
  if (t.space === 'street' || t.inCar) {
    x.strokeStyle = '#9a1c1c';
    x.lineWidth = 2.5;
    x.beginPath();
    x.moveTo(a - 6, b - 6);
    x.lineTo(a + 6, b + 6);
    x.moveTo(a + 6, b - 6);
    x.lineTo(a - 6, b + 6);
    x.stroke();
  }
  x.restore();
  // the key
  x.strokeStyle = 'rgba(40,53,122,.35)';
  x.lineWidth = 1;
  x.beginPath();
  x.moveTo(MW + 0.5, 0);
  x.lineTo(MW + 0.5, H);
  x.stroke();
  x.textAlign = 'left';
  x.fillStyle = '#111';
  x.font = '15px ' + HAND;
  x.fillText('Quay Street, by number', MW + 20, 24);
  const lh = Math.min(22, (H - 150) / MAPKEY.length);
  x.font = '15px ' + HAND;
  MAPKEY.forEach(([n], i) => {
    const yy = 50 + i * lh;
    x.fillStyle = '#14204f';
    x.textAlign = 'right';
    x.fillText(String(i + 1), MW + 34, yy);
    x.textAlign = 'left';
    x.fillStyle = '#1f2a5a';
    x.fillText(n, MW + 44, yy);
  });
  let ky = 50 + MAPKEY.length * lh + 14;
  x.font = '14px ' + HAND;
  x.fillStyle = '#444';
  x.strokeStyle = '#9a1c1c';
  x.lineWidth = 2.5;
  x.beginPath();
  x.moveTo(MW + 20, ky - 10);
  x.lineTo(MW + 30, ky);
  x.moveTo(MW + 30, ky - 10);
  x.lineTo(MW + 20, ky);
  x.stroke();
  x.fillText('where you stand', MW + 44, ky);
  ky += 22;
  x.fillStyle = '#c8641a';
  x.beginPath();
  x.arc(MW + 25, ky - 5, 3, 0, 7);
  x.fill();
  x.fillStyle = '#444';
  x.fillText('a street lamp. Light is where', MW + 44, ky);
  ky += 18;
  x.fillText('you are seen.', MW + 44, ky);
  ky += 24;
  x.fillText('North is to the left.', MW + 20, ky);
}

const MAPKEY = [
  ["Mickey's Cars", 14, 36],
  ["Laverack's, fish", 14, 26.8],
  ['the Washeteria', 14, 18.4],
  ['Hook Stores', 14, 10],
  ['empty, to let', 14, 1.6],
  ['the Golden River', 14, -6.8],
  ["Rita's", 14, -29],
  ['the chandlery', 14, -37],
  ['Regent House', 14, -46.5],
  ['the old laundry', 16, -62],
  ["Ada's", -14, 32],
  ["Peart's, papers", -14, 7.3],
  ["the ironmonger's", -14, 0],
  ['the Copper Kettle', -14, -7.3],
  ["Rinaldi's caff", -14, -29],
  ["Metcalfe's, coins", -14, -36],
  ['the chapel', -27, -67.5],
  ['the Ship, boarded', -14, -84.5],
  ['the Harbour Office', -29, 36],
];
