// One light field for both the picture and the rules. The same numbers draw the lamp pools on the ground
// and decide how far away Tom can be seen. Pure maths, baked once into a grid.
import { clamp, hyp, inRect } from './util.js';
import { BOUNDS, LAMPS, GLOWS, SHADE, los } from './map.js';
import { hour } from './state.js';
import { nightF } from './seeing.js';
import { RULES } from './rules.js';
const LIGHTS = RULES.light;

const LIGHT = RULES.light;
export const CELL = LIGHT.gridCellMetres;
export const GW = Math.ceil((BOUNDS.x1 - BOUNDS.x0) / CELL),
  GH = Math.ceil((BOUNDS.z1 - BOUNDS.z0) / CELL);
// channels: 0 sodium lamps, 1 always-on glows, 2 late shop windows, 3 early-closing windows
export const field = [0, 1, 2, 3].map(() => new Float32Array(GW * GH));
export const FERRY = LAMPS.find((l) => l.ferry);
const chan = (g) =>
  g.until >= LIGHTS.allNightChannelFromUntilHour ? 1 : g.until > LIGHTS.lateChannelAboveUntilHour ? 2 : 3;
let baked = false;

export function bake() {
  if (baked) return;
  baked = true;
  const srcs = LAMPS.map((l) => ({ x: l.x, z: l.z, r: l.r, c: 0, k: l.dim ? LIGHT.dimLampTimes : 1 })).concat(
    GLOWS.map((g) => ({ x: g.x, z: g.z, r: g.r, c: chan(g), k: LIGHT.shopGlowTimes })),
  );
  for (const s of srcs) {
    const x0 = Math.max(0, Math.floor((s.x - s.r - BOUNDS.x0) / CELL)),
      x1 = Math.min(GW - 1, Math.ceil((s.x + s.r - BOUNDS.x0) / CELL));
    const z0 = Math.max(0, Math.floor((s.z - s.r - BOUNDS.z0) / CELL)),
      z1 = Math.min(GH - 1, Math.ceil((s.z + s.r - BOUNDS.z0) / CELL));
    const f = field[s.c];
    for (let j = z0; j <= z1; j++)
      for (let i = x0; i <= x1; i++) {
        const wx = BOUNDS.x0 + (i + 0.5) * CELL,
          wz = BOUNDS.z0 + (j + 0.5) * CELL,
          d = hyp(wx, wz, s.x, s.z);
        if (d >= s.r) continue;
        let v = s.k * Math.pow(1 - d / s.r, LIGHT.falloffPower) * LIGHT.lampFullStrength;
        if (d > LIGHT.wallShadowBeyondMetres && !los(s.x, s.z, wx, wz)) v *= LIGHT.behindAWallTimes;
        for (const sh of SHADE)
          if (inRect(wx, wz, sh)) {
            v *= LIGHT.underCoverTimes;
            break;
          }
        const idx = j * GW + i;
        f[idx] = Math.min(1, f[idx] + v);
      }
  }
}
function sample(c, x, z) {
  const fx = (x - BOUNDS.x0) / CELL - 0.5,
    fz = (z - BOUNDS.z0) / CELL - 0.5;
  const i = clamp(Math.floor(fx), 0, GW - 2),
    j = clamp(Math.floor(fz), 0, GH - 2),
    u = clamp(fx - i, 0, 1),
    v = clamp(fz - j, 0, 1),
    f = field[c],
    k = j * GW + i;
  return (f[k] * (1 - u) + f[k + 1] * u) * (1 - v) + (f[k + GW] * (1 - u) + f[k + GW + 1] * u) * v;
}
// What is switched on at this hour. The same values go to the shaders as uniforms.
export function lightState(h = hour()) {
  const n = nightF(h);
  const span = LIGHT.lampsFullWhenNightAbove - LIGHT.lampsStrikeWhenNightAbove;
  const on = clamp((n - LIGHT.lampsStrikeWhenNightAbove) / span, 0, 1); // lamps strike as dusk comes down
  const lateEvening = h >= LIGHT.lateWindowsFromHour && h < LIGHT.lateWindowsUntilHour;
  const late = lateEvening || h < LIGHT.lateWindowsAgainAfterMidnightUntilHour ? 1 : 0;
  const early = h >= LIGHT.earlyWindowsFromHour && h < LIGHT.earlyWindowsUntilHour ? 1 : 0;
  const ferry = h >= LIGHT.ferryLandingDarkFromHour || h < LIGHT.ferryLandingDarkUntilHour ? 0 : 1; // the landing goes dark after the last ferry
  const day = LIGHT.daylightAtNight + (1 - LIGHT.daylightAtNight) * (1 - n);
  return { n, on, late: late * on, early: early * on, ferry, day };
}
export function lightAt(x, z, space) {
  if (space && space !== 'street') return LIGHT.indoors;
  if (!baked) bake();
  const s = lightState();
  let lamp = sample(0, x, z);
  if (!s.ferry && FERRY) {
    const d = hyp(x, z, FERRY.x, FERRY.z);
    if (d < FERRY.r)
      lamp = Math.max(0, lamp - Math.pow(1 - d / FERRY.r, LIGHT.falloffPower) * LIGHT.lampFullStrength);
  }
  const v = s.day + s.on * (lamp + sample(1, x, z)) + s.late * sample(2, x, z) + s.early * sample(3, x, z);
  return clamp(v, 0, 1);
}
export const lightWord = (L) =>
  L < LIGHTS.wordDarkBelowLight
    ? 'IN THE DARK'
    : L < LIGHTS.wordHalfLitBelowLight
      ? 'HALF LIT'
      : 'IN THE LIGHT';
