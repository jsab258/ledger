// Advances the simulation: clock, weather, people, witnesses, gossip, fading.
import { clamp, lerp, rnd, pick } from './util.js';
import { G, hour, SECS_PER_HOUR } from './state.js';
import { stepPeople } from './routines.js';
import { perceiveTick } from './seeing.js';
import { gossipTick, decay } from './gossip.js';
import { los, zoneAt } from './map.js';
import { lightAt, bake } from './light.js';
import { RULES } from './rules.js';

const WX = RULES.weather,
  TICK = RULES.ticking;
const acc = { g: 0, d: 0 };
export function initEnv(camYaw) {
  bake();
  G.env.los = los;
  G.env.lightAt = lightAt;
  G.env.zone = zoneAt;
  if (camYaw) G.env.camYaw = camYaw;
}
export function setWeather(kind) {
  G.weather.kind = kind;
  G.weather.next = G.t + rnd(WX.changesAfterGameMinutesAtLeast, WX.changesAfterGameMinutesAtMost);
}
function weatherStep(dm) {
  const w = G.weather;
  if (G.t >= w.next) {
    const h = hour(),
      opts =
        h < WX.nightWeatherBeforeHour || h > WX.nightWeatherAfterHour
          ? ['mist', 'drizzle', 'drizzle', 'rain', 'dry', 'heavy']
          : ['drizzle', 'drizzle', 'rain', 'dry', 'dry', 'heavy', 'rain'];
    setWeather(pick(opts.filter((k) => k !== w.kind)));
  }
  const aim = WX[w.kind] || WX.drizzle,
    k = clamp(dm / WX.settlesOverGameMinutes, 0, 1);
  w.rain = lerp(w.rain, aim.rain, k);
  w.mist = lerp(w.mist, aim.mist, k);
  const change =
    w.rain > WX.rainingAboveRain
      ? dm * WX.streetWetsPerGameMinuteOfFullRain * w.rain
      : -dm * WX.streetDriesPerGameMinute;
  w.wet = clamp(w.wet + change, WX.streetNeverDrierThan, 1);
}
// dt: seconds of simulated time (already multiplied when the player is passing the time).
export function simStep(dt) {
  const dm = (dt * 60) / SECS_PER_HOUR;
  G.t += dm;
  const t = G.tom;
  t.zone = zoneAt(t.inCar ? G.car.x : t.x, t.inCar ? G.car.z : t.z);
  weatherStep(dm);
  stepPeople(dt);
  perceiveTick(dt);
  acc.g += dm;
  if (acc.g >= TICK.gossipEveryGameMinutes) {
    acc.g = 0;
    gossipTick();
  }
  acc.d += dm;
  if (acc.d >= TICK.memoriesFadeEveryGameMinutes) {
    decay(acc.d);
    acc.d = 0;
  }
}
// Skip a stretch of time with nobody watching Tom (sleeping, custody): routines and gossip still run.
export function skipTo(tEnd, hidden = true) {
  const t = G.tom,
    sp = spaceBeforeHiding();
  if (hidden) t.space = 'away';
  HIDING.depth++;
  let guard = 0;
  try {
    while (G.t < tEnd && guard++ < 20000)
      simStep(Math.min(TICK.longestSkipStepRealSeconds, ((tEnd - G.t) * SECS_PER_HOUR) / 60 + 0.01));
  } finally {
    HIDING.depth--;
    t.space = sp;
  }
}
// The one-shot (the clumsy run's fault): time passed unseen puts Tom 'away' for its length. One such stretch begun
// inside another, or a scene that read where he stood in the middle of one, could leave him 'away' for good: on
// the street, unseen, unable to walk. Where he really stood is kept here, and play never goes on with him 'away'.
export const HIDING = { depth: 0, was: 'street' };
export function spaceBeforeHiding() {
  const t = G.tom;
  if (t.space !== 'away') HIDING.was = t.space;
  return HIDING.was;
}
export function neverLeftAway() {
  const t = G.tom;
  if (t.space === 'away' && HIDING.depth === 0) t.space = HIDING.was || 'street';
  else if (t.space !== 'away') HIDING.was = t.space;
}
