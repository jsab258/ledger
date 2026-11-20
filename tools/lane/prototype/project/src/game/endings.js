// LEDGER, the whole game: the system "endings" (parts 3.1.4, 3.1.5, 6.2.5, 7.15; DESIGN 16, addendum A7).
// The endings are states, never picked from a list. Every cost that decides shows its sign before it decides; Tom's
// reading is built only from the signs he was given. After the close and the credits, play goes on in the town.
import { register, emit, on, X } from './core.js';
import { G, setPaused } from '../state.js';
import { RULES } from '../rules.js';
import { KINDS, NAMES } from '../kinds.js';
import { ui, sub, fade, panel, closePanel, say, scene } from '../ui.js';
import { note } from '../ledger.js';
import { attached } from '../seeing.js';
import { townLevel } from '../gossip.js';
import { esc } from '../util.js';
import { ending, signsFor, reading, SIGNS, SHOWN } from './pieces/ending_state.js';

const T = () => RULES.game.endings,
  TA = () => RULES.game.acts;
const st = () => X('endings');
const xs = (id) => (G.x && G.x[id]) || {};

// A sign shown to Tom: once, in the world's words, and written in the Ledger.
export function showSign(id, quiet) {
  const s = st();
  if (s.signs[id] !== undefined || !SIGNS[id]) return false;
  s.signs[id] = Math.round(G.t);
  if (id === 'friend_act') delete s.signs.friend_gone;
  if (id === 'friend_gone') delete s.signs.friend_act;
  note(SIGNS[id], 'note', 'sign_' + id + (id.startsWith('friend') ? '_' + Math.round(G.t) : ''), { how: 'Tom saw it' });
  if (!quiet && G.story.phase === 'play') sub(SIGNS[id], '', 'over', T().signShownRealSeconds);
  return true;
}
export const signsShown = () => Object.keys(st().signs);

// What the close reads, from the game as it stands. over: what Act III settled (booksHold, handedOver, traded).
export function inputsNow(over = {}) {
  const f = G.story.flags,
    law = xs('law'),
    kase = law.case || {},
    life = xs('life');
  const killed = G.events.some((E) => KINDS[E.kind] && KINDS[E.kind].crime >= T().killingCrimeLevel);
  const hunted = (law.stage || 0) >= 3;
  let tellers = 0;
  for (const P of G.named || [])
    if (P.mind && P.mind.mem.some((m) => attached(m) && m.src === 'told' && G.ev[m.e] && KINDS[G.ev[m.e].kind].crime >= T().seriousCrimeFromLevel)) tellers++;
  const friend = life.friend,
    fp = G.people[(friend && friend.who) || 'alison'];
  const friendHolds = friend && friend.holds !== undefined ? !!friend.holds : !!(fp && !fp.dead && fp.mind.regard > TA().friendHoldsAboveRegard);
  return Object.assign(
    {
      woundDown: f.choice === 'wind',
      booksHold: true,
      caseSinksFirm: (kase.strength || 0) >= TA().caseSinksTheFirmFromStrength,
      handedOver: false,
      friendHolds,
      streetFact: tellers >= TA().streetHoldsItAsFactFromPeople,
      hunted,
      huntedForKilling: hunted && killed,
    },
    over,
  );
}
// The signs the world owes him now: shown as each cost arises, long before the books open.
function watch() {
  if (st().ended) return;
  const I = inputsNow(st().over || {}),
    acts = xs('acts');
  for (const id of signsFor(I)) {
    if (id.startsWith('friend') && (acts.act || 1) < 3) continue; // the friendship is read at the close's week
    if ((id === 'inspector_cold' || id === 'sheila_line') && (acts.act || 1) < 3) continue;
    showSign(id);
  }
}
export function readingNow() {
  const r = reading(signsShown());
  const m = G.money,
    lv = NAMES[townLevel()] || 'nothing yet';
  const stands = [`The street calls him ${lv}.`];
  if (m.booksOff > 0) stands.push('The fare book has had more through it than it could hide.');
  if (r.quiet) stands.push('Nothing has come due yet, as far as he can tell.');
  return Object.assign(r, { stands, text: stands.concat(r.lines) });
}
export const readingHTML = () => `<h2 style="margin-top:14px">How things stand</h2><div class="was">Tom's own reading, from what he has been shown and told.</div>${readingNow().text.map((l) => `<div class="lh">${esc(l)}</div>`).join('')}`;

const CLOSE = {
  both: ["Mickey's is still on Quay Street, and the books stood.", 'One person in this town still asks him in without wanting anything.', 'Nobody on the street can say for certain what he is. They call him Tom.'],
  kingdom: ["Mickey's is still on Quay Street, and the books stood.", 'People are civil to him. Doors open. Nobody sits down.', 'The port does not move without him, and he eats alone.'],
  quiet: ['The sign over the office has somebody else to answer for it now.', 'He walked away clean, and one door on this street is still open to him.', 'On the quay, nobody steps aside. He does not need them to.'],
  straight: ['There is no business at the close. The cars are sold or somebody else drives them.', 'One friendship held. It cost the rest.', 'He is a man with a room and a name people say quietly.'],
  burn: ["The office is dark and the rank is somebody else's.", 'Nobody on this street does anything for him unasked.', 'What Mickey left him is gone, and so is what he might have had instead.'],
};
// The close: a short walk through the town as it now stands, the credits, then the town again (A7).
export async function runEnding(over = {}) {
  const s = st();
  if (s.ended) return s.ended;
  s.over = over;
  const I = inputsNow(over);
  for (const id of signsFor(I)) showSign(id, true); // nothing decides unshown (ER-END-02)
  const e = ending(I),
    r = reading(signsShown());
  s.ended = { state: e.state, shown: e.shown, turn: e.turn, t: Math.round(G.t), predicted: r.predicts, inputs: I };
  G.story.flags.ending = e.state;
  emit('ending', { state: e.state, shown: e.shown, turn: e.turn });
  note(`How it ended: ${e.shown}. ${CLOSE[e.state][0]}`, 'note', 'ending', { how: 'Tom saw it' });
  note('The story is told. The town goes on as it stands, and Tom can walk it for as long as he likes.', 'note', 'afterending', { how: 'Tom knows' });
  if (G.hooks.save) G.hooks.save();
  setPaused(true, 'the ending');
  await fade(true, `${e.shown.toUpperCase()}\n\n${CLOSE[e.state].join('\n\n')}\n\nThe street calls him ${NAMES[townLevel()] || 'nothing at all'}.`);
  await new Promise((res) => {
    s.closeDone = res;
    ui.hooks.endclose = res;
    setTimeoutSafe(res, T().closeLineRealSeconds * CLOSE[e.state].length * 1000);
    addEventListener('keydown', res, { once: true });
    addEventListener('pointerdown', res, { once: true });
  });
  G.story.phase = 'end';
  panel(creditsEndHTML(e), 'credits-end');
  await fade(false);
  return s.ended;
}
const setTimeoutSafe = (fn, ms) => setTimeout(fn, ms);
function creditsEndHTML(e) {
  return `<div class="masthead">LEDGER</div><h1>${esc(e.shown)}</h1><p>${CLOSE[e.state].map(esc).join(' ')}</p>
  <h2>Credits</h2><p>A game by Jafar. Design, town, words and code built with Claude. Figures: Quaternius (CC0). Ground and wall pictures: Poly Haven (CC0). three.js (MIT). Built with esbuild (MIT). The town simulation is the game's own C++ town code compiled for the browser; the notices of the library pieces inside it are kept in its credits file, beside the page's source.</p>
  <p>Britain, 1990. Every person, firm and place in Meridian is invented.</p>
  <div class="row"><button class="btn" data-act="afterend">Walk the town as it now stands</button><button class="btn alt" data-act="totitle">Quit to the title</button></div>`;
}
// After the credits: control back in the town at the ending's state (ER-AFTER-01). No new main beats.
export function afterEnding() {
  const s = st();
  if (!s.ended) return false;
  closePanel();
  G.story.phase = 'play';
  s.after = 1;
  setPaused(false, 'after the ending: the town as it stands');
  fade(false);
  sub('The town as it now stands. Nothing more is owed.', '', 'over', 5);
  return true;
}

register({
  id: 'endings',
  fresh: () => ({ signs: {}, ended: null, after: 0, over: null }),
  loaded(s) {
    if (!s.signs) s.signs = {};
    ui.hooks.afterend = afterEnding;
    G.hooks.reading = readingNow;
    G.hooks.readingHTML = readingHTML;
  },
  minute(t) {
    if (t % 10 === 0) watch();
  },
  hook: {
    read: () => JSON.parse(JSON.stringify(st())),
    reading: () => readingNow(),
    inputs: (over) => inputsNow(over || {}),
    showSign: (id) => showSign(id, true),
    // a scripted route to each ending (ER-END-01): the inputs are set as the world would set them, the signs are
    // shown, and the close runs. name: one of the five states, or 'hunted' (a hunted man's end).
    async route(name) {
      const R = {
        both: { booksHold: true, friendHolds: true, streetFact: false },
        kingdom: { booksHold: true, friendHolds: false },
        quiet: { handedOver: true, friendHolds: true, hunted: false, huntedForKilling: false },
        straight: { booksHold: false, friendHolds: true, huntedForKilling: false },
        burn: { booksHold: false, friendHolds: false },
        hunted: { hunted: true, huntedForKilling: true, friendHolds: true },
      }[name];
      if (!R) return null;
      const base = { woundDown: false, caseSinksFirm: false, handedOver: false, streetFact: false, hunted: false, huntedForKilling: false };
      const p = runEnding(Object.assign(base, R));
      const s = st();
      for (let i = 0; i < 200 && !s.closeDone; i++) await new Promise((r) => setTimeout(r, 10));
      if (s.closeDone) s.closeDone();
      return p;
    },
    after: () => afterEnding(),
    shown: () => SHOWN,
  },
});
void on;
void say;
void scene;
