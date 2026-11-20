// LEDGER, the whole game: the system "feel". The camera's rows and lens and Tom's turn are in player.js (numbers
// in tune/feel.js); menus by keys and pad, subtitles and prompts are in ui.js. This file holds what joins them to
// the rest: the assists (DESIGN-ADDENDUM A6), sound shown as captions (8.4.1), and the test calls.
import { register, emit, on } from './core.js';
import { G } from '../state.js';
import { ui, $ } from '../ui.js';
import { vaultPlaces, inWater } from '../map.js';
import { camLine, footFeel, cam } from '../player.js';
import { nightF } from '../seeing.js';
import { RULES } from '../rules.js';

const A = RULES.game.feel.assists;
export const ASSISTS = ['assistSee', 'assistSlowFight', 'assistDrive', 'assistLongWalk', 'soundShown'];
const R = { caps: [], last: 0, noise: 0, ran: false, log: [] };

// A short word at the screen's edge for what Tom hears: never a ring, a gauge or what anyone knows (D33).
export function caption(text) {
  R.log.push({ text, t: G.t, shown: !!G.settings.soundShown });
  if (R.log.length > 100) R.log.shift();
  if (!G.settings.soundShown || typeof document === 'undefined') return false;
  if (G.played - R.last < A.captionAtMostEveryRealSeconds && R.caps.some((c) => c.text === text)) return false;
  R.last = G.played;
  const el = document.createElement('div');
  el.textContent = text;
  $('cap').appendChild(el);
  R.caps.push({ el, text, t: A.captionShowsRealSeconds });
  while (R.caps.length > 3) R.caps.shift().el.remove();
  return true;
}
const SFX_WORDS = { glass: 'glass breaks', door: 'a door', force: 'a door forced', crash: 'a crash', shout: 'a shout', horn: 'a car horn', bell: 'the chapel bell', bin: 'a bin rattles', hit: 'a blow lands', thud: 'a body falls', radio: 'the radio' };
function wrapSfx() {
  if (G.hooks.sfxWrapped || !G.hooks.sfx) return;
  const base = G.hooks.sfx;
  G.hooks.sfxWrapped = true;
  G.hooks.sfx = (name) => {
    if (SFX_WORDS[name]) caption('[' + SFX_WORDS[name] + ']');
    return base(name);
  };
}

register({
  id: 'feel',
  fresh: () => ({ hintsAgainAt: -1 }),
  loaded() {
    wrapSfx();
    for (const k of ASSISTS) if (G.settings[k] === undefined) G.settings[k] = false; // every assist is off by default
    ui.hooks.hintsagain = () => {
      G.x.feel.hintsAgainAt = Math.round(G.t);
      emit('hints:again', {});
      const el = $('hintsagain');
      if (el) el.textContent = 'The first hints will show again as each thing is next met.';
    };
  },
  step(dt) {
    for (let i = R.caps.length - 1; i >= 0; i--) {
      const c = R.caps[i];
      c.t -= dt;
      if (c.t <= 0) {
        c.el.remove();
        R.caps.splice(i, 1);
      }
    }
    // his own loud noise, and running feet at night
    const t = G.tom,
      loud = (t.noiseP || 0) >= A.captionLoudFromMetres;
    if (loud && !R.noise) caption('[a loud noise: his own]');
    R.noise = loud;
    const running = !!t.run && !t.inCar && nightF() > 0.5;
    if (running && !R.ran) caption('[his running feet]');
    R.ran = running;
  },
  hook: {
    vaultPlaces,
    inWater,
    camLine,
    footFeel,
    assists: () => Object.fromEntries(ASSISTS.map((k) => [k, !!G.settings[k]])),
    setAssist: (k, on) => {
      if (!ASSISTS.includes(k)) return false;
      G.settings[k] = !!on;
      return true;
    },
    caption,
    captions: () => R.log.slice(),
    camRow: () => ({ back: cam.back, fov: cam.fov, pitch: cam.pitch }),
  },
});
on('noise', (n) => {
  if (n && n.by !== 'tom') caption('[a noise]');
});
