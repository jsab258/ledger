// The driving study's car (Quay Run, round 3) in LEDGER's town. The study's vehicle.js asks its world for the road
// under each tyre; this file answers for the Hook: level ground (the prototype's town is flat), tarmac in the streets
// and setts on the quay, and the weather's one wetness value as the study's dry, wet and heavy rain.
import { G } from '../state.js';

export const SURF = { TARMAC: 0, PAVEMENT: 1, COBBLE: 2 };
export const env = { wet: 0, tod: 1 };
export const groundY = () => 0;
export const baseY = () => 0;
export const hillSlope = () => 0;
export const surfaceType = (x, z) => (z > 41.5 && z < 62 ? SURF.COBBLE : SURF.TARMAC);
export const puddleAt = () => 0;
// called once a step by the cab: rain above a drizzle is the study's wet road, a downpour its heavy rain
export function weatherNow() {
  const r = (G.weather && G.weather.rain) || 0,
    w = (G.weather && G.weather.wet) || 0;
  env.wet = r > 0.7 ? 2 : r > 0.15 || w > 0.4 ? 1 : 0;
}
