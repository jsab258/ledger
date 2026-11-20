// LEDGER, the whole game: the system "way". Finding the way without markers (DESIGN 4 guidance, A9; parts 6.9, 6.3,
// 2.2.6's labels): every place has an address and a landmark; people asked give it by landmark if they know it;
// the paper map marks only places he has been or been told of; lost, his own line notes the landmark again, once.
import { register, addPlace, PLACES, X, write, tell, tomXZ, hourNow, here, on } from './core.js';
import { G } from '../state.js';
import { hyp, esc } from '../util.js';
import { panel } from '../ui.js';
import { RULES } from '../rules.js';
import { PLACE_LIST, STREETS } from './tune/way.js';
import { PIECE as LIFE } from './pieces/life.js';

const T = RULES.game.way;
for (const p of PLACE_LIST) addPlace(p);

// He has been there or been told of it: it goes on his paper map, and the line into the Ledger once.
export function know(id, how = 'been there') {
  const x = X('way'),
    p = PLACES[id];
  if (!p || x.known[id]) return false;
  x.known[id] = { how, t: Math.round(G.t) };
  return true;
}
// A job, a fare or a letter names a place: the address and the landmark are said, written, and become the goal.
export function direct(id, by) {
  const p = PLACES[id];
  if (!p) return null;
  know(id, 'told by ' + by);
  const x = X('way');
  x.goal = { id, by, sinceT: G.t, best: null, noProgress: 0, nudged: false, offered: false };
  return `${p.name}: ${p.landmark} (${p.address})`;
}
export const goalDone = () => (X('way').goal = null);
export const landmark = (id) => (PLACES[id] ? PLACES[id].landmark : '');
// Asked the way (A9): shopkeepers and the constable always know; others if the place is in their own day.
export function askWay(P, placeId) {
  const place = PLACES[placeId];
  if (!place) return null;
  const r = LIFE.fns.askWay({ keeper: !!P.keeper || /^k_/.test(P.id), police: !!P.def.police, knows: P.def.local === false ? [] : Object.keys(PLACES) }, place);
  if (r.knows) know(placeId, 'told by ' + P.def.name);
  return r.says;
}
function mapHTML() {
  const x = X('way');
  const rows = Object.keys(x.known)
    .map((id) => PLACES[id])
    .sort((a, b) => b.z - a.z)
    .map((p) => `<tr><td><b>${esc(p.name)}</b></td><td>${esc(p.address)}</td><td>${esc(p.landmark)}</td><td>${esc(x.known[p.id].how)}</td></tr>`)
    .join('');
  return `<h2>The Hook, on paper</h2><p>Only the places he has been or been told of. The river is to the south; Quay Street runs north from the quay to the bridge and Copper Row.</p><table class="t"><tr><th>Place</th><th>Address</th><th>Look for</th><th>How he knows</th></tr>${rows}</table><p>${STREETS.map((s) => esc(s.name)).join(' · ')}</p><p><button data-act="close">Fold it up</button></p>`;
}

register({
  id: 'way',
  fresh: () => ({ known: { mickeys: { how: 'the letter said', t: 0 } }, goal: null }),
  step(dt) {
    const x = X('way'),
      t = G.tom;
    if (G.paused) return;
    const [tx, tz] = tomXZ();
    // being at a place puts it on his map
    if (t.space !== 'street') {
      const here_ = PLACE_LIST.find((p) => p.room === t.space);
      if (here_) know(here_.id);
    } else for (const p of PLACE_LIST) if (!x.known[p.id] && !p.room && hyp(tx, tz, p.x, p.z) < T.reachedWithinMetres) know(p.id);
    const g = x.goal;
    if (!g) return;
    const p = PLACES[g.id],
      d = t.space === p.room ? 0 : hyp(tx, tz, p.x, p.z);
    if (d < T.reachedWithinMetres) return void goalDone();
    if (g.best === null || d < g.best - 1) {
      g.best = d;
      g.noProgress = 0;
    } else g.noProgress += dt;
    const r = LIFE.fns.lost({ secondsNoProgress: g.noProgress, nudged: g.nudged, offered: g.offered });
    if (r.nudge) {
      g.nudged = true; // once per goal, never inside 90 s (ER-WAY-03)
      tell(`${p.name}. ${p.landmark[0].toUpperCase() + p.landmark.slice(1)}.`, '', RULES.game.feel.subtitleClearsAfterRealSecondsAtMost);
    } else if (r.offer) {
      const who = G.named.find((P) => here(P, RULES.game.ledgerx.lostOfferWithinMetres) && !P.def.police);
      if (who) {
        g.offered = true;
        tell(`"You look lost. ${askWay(who, g.id)}"`, who.def.name);
      }
    }
  },
  key(code) {
    if (code !== 'Comma' || G.tom.inCar) return false;
    panel(mapHTML(), 'map'); // opening it pauses nothing in the town's rules, but he stands still to read it
    return true;
  },
  hook: {
    places: () => PLACE_LIST.map((p) => ({ id: p.id, name: p.name, address: p.address, landmark: p.landmark, label: p.label, x: p.x, z: p.z })),
    known: () => Object.keys(X('way').known),
    direct,
    goal: () => X('way').goal,
    mapHTML,
    askWay: (personId, placeId) => askWay(G.people[personId], placeId),
    // ER-WAY-02: every place has an address, a landmark and a label
    faults: () => PLACE_LIST.filter((p) => !p.address || !p.landmark || !['public', 'hours', 'private', 'forbidden'].includes(p.label)).map((p) => p.id),
    hourNow,
  },
});
on('way.ask', ({ P, place }) => tell('"' + askWay(P, place) + '"', P.anon ? P.def.desc : P.def.name));
