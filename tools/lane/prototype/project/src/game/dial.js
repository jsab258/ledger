// LEDGER, the whole game: the system "dial". The escalation dial (ruling 18 Nov; DESIGN 7; parts 1.3.10, 2.13,
// 2.6.6): the game starts with no gun in the Hook. Guns come only through people. The dial is a fact in the town's
// memory, not a meter: Fists, Shown, Fired, War. It never moves on a deed nobody saw or heard; it falls one step
// only after two quiet game weeks, and never back to Fists. Guns stay rare. Rules: pieces/rise.js.
import { register, X, write, tell, hourNow, P_, emit, on } from './core.js';
import { G } from '../state.js';
import { hyp, quid } from '../util.js';
import { act } from '../events.js';
import { pay } from '../money.js';
import { choose, scene, say } from '../ui.js';
import { RULES } from '../rules.js';
import { PIECE as RISE } from './pieces/rise.js';
import { PIECE as EYES } from './pieces/eyes.js';
import { has, take } from './crime.js';
import { ellisEvent } from './law.js';
import { setFareShare } from './econ.js';

const T = RULES.game.dial;
const R = RISE.fns;
const NAMES = RULES.game.rise.dial;

function move(what, seenOrHeard, by) {
  const x = X('dial'),
    before = x.d.at;
  x.d = R.dial(x.d, { what, seenOrHeard, t: G.t, by });
  if (x.d.at === before) return false;
  const means = R.dialMeans(x.d.at);
  x.log.push({ at: x.d.at, what, t: Math.round(G.t) });
  write(x.d.at > before ? `The town knows there ${x.d.at === 1 ? 'is a gun on the Hook' : x.d.at === 2 ? 'has been shooting on the Hook' : 'are armed men on both sides now'}. ${x.d.who === 'tom' ? 'It remembers who brought it in.' : ''}` : 'Two quiet weeks. The street has stopped looking over its shoulder quite so much.', { key: 'dial:' + x.d.at + ':' + Math.round(G.t), how: 'The street says' });
  if (x.d.at > before && x.d.at >= 2) ellisEvent('detective crime reported');
  if (x.d.at === 3) setFareShare(means.nightFaresShare, null); // night fares fall while it lasts
  if (before === 3 && x.d.at < 3) setFareShare(1, null);
  emit('dial.moved', { at: x.d.at, means });
  return true;
}
export const dialAt = () => X('dial').d.at;
// A gun reaches him only through a person, or once, found at Mickey's (DESIGN 7).
async function gunAt(how, from) {
  const x = X('dial');
  const r = R.gun(how, { from, foundBefore: x.foundAtMickeys });
  if (!r.has) return false;
  if (how === 'bought' && !pay(T.gunPricePence, false, 'a revolver, from ' + from)) return tell('"Come back with the money."', ''), false;
  if (!take('gun')) return false;
  if (how === 'found') x.foundAtMickeys = true;
  x.gunThrough = r.through;
  write(`A revolver, ${how === 'found' ? "found in the bottom drawer of Mickey's locked office" : 'bought from ' + from + ' for ' + quid(T.gunPricePence)}. Nobody carries one on the Hook. Not yet.`, { how: 'Did it', key: 'gun' });
  return true;
}
// Firing: heard to about 177 m by day. Whoever hears it keeps it for good.
function fire() {
  const t = G.tom,
    x = X('dial');
  const reach = EYES.fns.reach('shot', hourNow(), G.weather.rain > RULES.weather.rainingAboveRain);
  const heard = G.named.filter((P) => !P.gone && !P.dead && hyp(P.x, P.z, t.x, t.z) <= reach).map((P) => P.id);
  act('shot_fired', { noiseR: reach, told: heard.slice(0, 12) });
  x.shots.push({ heard: heard.length, reach, t: Math.round(G.t) });
  move(x.shots.length > 1 ? 'second shooting' : 'shot heard', heard.length > 0, 'tom');
  return { heard: heard.length, reach };
}

register({
  id: 'dial',
  fresh: () => ({ d: { at: 0, top: 0, quietSinceT: null, who: null }, log: [], shots: [], gunThrough: null, foundAtMickeys: false, armedCrew: false }),
  hourly(h) {
    if (h % T.quietCheckedEveryGameHours === 0) move('quiet', true);
  },
  hotspots(out) {
    const t = G.tom,
      x = X('dial'),
      rung = G.x.rise ? G.x.rise.rung : 1;
    if (t.space === 'mickeys' && rung >= T.mickeysGunFromRung && !x.foundAtMickeys && !has('gun')) out.push({ k: 'G', t: "The bottom drawer of Mickey's desk", run: async () => {
      const i = await scene(() => choose('', 'Under the real book, wrapped in a duster: a revolver, old, oiled, loaded. Mickey never fired it. Everything changes if this goes out of this room.', ['Take it.', 'Leave it where it is.']));
      if (i === 0) gunAt('found');
      else x.leftIt = true;
    } });
    if (t.armed && has('gun') && t.space === 'street') out.push({ k: 'G', t: 'Fire it', run: fire });
  },
  hook: {
    x: () => X('dial'),
    at: dialAt,
    name: () => NAMES[dialAt()],
    means: () => R.dialMeans(dialAt()),
    move,
    gunAt,
    fire,
    armCrew: () => {
      X('dial').armedCrew = true;
      act('armed_crew', { silent: true, told: ['ron', 'lee'].filter((id) => P_(id)) });
      return move('crew armed', true, 'tom');
    },
  },
});
// a gun seen is news across town: a weapon out that is a gun, in anybody's sight
on('act', (E) => {
  if (E.kind === 'weapon_out' && E.weapon === 'gun') move('gun seen', (E.wit || []).length + (E.party || []).length > 0, 'tom');
  if (E.kind === 'holdup' && E.weapon === 'gun') move('gun seen', true, 'tom');
});
on('crime.holdup', ({ gun }) => {
  if (gun) move('gun seen', true, 'tom');
});
