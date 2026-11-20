// LEDGER, the whole game: the system "ledgerx". What the one-shot adds to Tom's notebook and to knowing where he
// stands (DESIGN 10, A5, A19, A31; parts 6.1.5, 6.2.5, 6.10, 6.5): the watch, the chapel bell, what he carries in
// words, letters and papers in hand, and Tom's reading, built only from signs he was shown.
import { register, X, write, tell, hourNow, dayNow, on } from './core.js';
import { G } from '../state.js';
import { esc, hourWords, DAYS } from '../util.js';
import { panel, closePanel, ui , showWatch } from '../ui.js';
import { RULES } from '../rules.js';
import { PIECE as STORY } from './pieces/story.js';
import { PIECE as LIFE } from './pieces/life.js';
import { inWords } from './econ.js';

const T = RULES.game.ledgerx;

// A sign he was shown (DESIGN 16): kept for good, and what his reading is built from.
export function sign(kind, text) {
  const x = X('ledgerx');
  if (!x.signs.some((s) => s.kind === kind && s.text === text)) x.signs.push({ kind, text, t: Math.round(G.t) });
  write(text, { key: 'sign:' + kind + ':' + text.slice(0, 40), how: 'Saw it himself' });
}
export const signsShown = () => [...new Set(X('ledgerx').signs.map((s) => s.kind))];
// Tom's reading: how things stand as he sees them, on request and at each act's end.
export function reading() {
  return STORY.fns.reading(signsShown());
}
// A letter or a paper in hand (A19): opens as a page and goes into the Ledger.
export function letter(id, from, title, body) {
  const x = X('ledgerx');
  if (!x.letters.find((l) => l.id === id)) {
    x.letters.push({ id, from, title, body, t: Math.round(G.t), read: false });
    write(`A letter from ${from}: ${title}.`, { key: 'letter:' + id, how: 'Read it' });
  }
  return id;
}
export function openLetter(id) {
  const l = X('ledgerx').letters.find((q) => q.id === id);
  if (!l) return false;
  l.read = true;
  panel(`<h2>${esc(l.title)}</h2><p><i></i>From ${esc(l.from)}</p>${l.body.split('\n').map((p) => `<p>${esc(p)}</p>`).join('')}<p><button data-act="close">Put it away</button></p>`.replace('<i></i>', ''), 'letter');
  return true;
}
// What he carries, in words (A5): two things under the coat, one in the hand.
export function carriedWords() {
  const t = G.tom,
    c = (G.x.crime && G.x.crime.pockets) || [];
  const hand = t.carry === 'bag' ? 'a holdall in his hand' : t.carry === 'suitcase' ? 'his suitcase in his hand' : t.carry ? t.carry + ' in his hand' : null;
  const under = c.map((i) => i.name);
  return [hand, under.length ? under.join(' and ') + ' under his coat' : null].filter(Boolean).join('; ') || 'nothing but his keys';
}
function readingHTML() {
  const r = reading(),
    w = inWords();
  return `<h2>How things stand, as he sees them</h2>${r.lines.map((l) => `<p>${esc(l)}</p>`).join('')}<p>${esc(w.rent)} In his pocket: ${esc(w.pocket)}. In the tin: ${esc(w.tin)}. ${esc(w.hide)}</p><p>On him: ${esc(carriedWords())}.</p><p><button data-act="close">Shut the book</button></p>`;
}

register({
  id: 'ledgerx',
  fresh: () => ({ signs: [], letters: [], watchT: -1e9, bellHour: -1, hints: {} }),
  loaded() {
    ui.hooks.close = () => closePanel(); // a panel's own button to put it away
  },
  hourly(h) {
    // the chapel bell strikes the hours by day (A31); it is a sound, shown in words only with "sound shown" on
    if (LIFE.fns.time({ hour: h, minute: 0 }).bell && G.settings.soundShown && G.tom.space === 'street') tell(`[the chapel bell: ${hourWords(h)}]`, '');
    // heard in the mix, by its strokes, wherever he is in the Hook (louder near the chapel)
    if (LIFE.fns.time({ hour: h, minute: 0 }).bell && G.hooks.sfx) G.hooks.sfx('bell:' + (h % 12 || 12), G.tom.space === 'street' ? 0.5 : 0.2);
    X('ledgerx').bellHour = h;
  },
  key(code) {
    if (code === 'KeyN') {
      // the watch: a glance at his wrist, the hour for two seconds, no screen clock (ER-TIME-01)
      X('ledgerx').watchT = G.played;
      showWatch(hourNow(), `${hourWords(hourNow())}, ${DAYS[dayNow() % 7]}`, T.watchShowsRealSeconds);
      if (G.hooks.sfx) G.hooks.sfx('cloth', 0.05);
      return true;
    }
    if (code === 'Period') {
      panel(readingHTML(), 'reading');
      return true;
    }
    return false;
  },
  hotspots(out) {
    const x = X('ledgerx'),
      unread = x.letters.find((l) => !l.read);
    if (unread && G.tom.space === 'mickeys') out.push({ k: 'E', t: 'Open the letter from ' + unread.from, run: () => openLetter(unread.id) });
  },
  hook: {
    reading,
    readingHTML,
    sign,
    signs: () => X('ledgerx').signs,
    letter,
    openLetter,
    letters: () => X('ledgerx').letters,
    carriedWords,
    watch: () => ({ hour: hourNow(), words: hourWords(hourNow()), screenClock: false }),
  },
});
on('act.end', (e) => write('How things stand at the end of Act ' + e.act + ': ' + reading().lines.join(' '), { key: 'reading:act' + e.act, how: 'His own reading' }));
