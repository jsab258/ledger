// Deterministic maths for everything the scripted drives measure.
//
// JavaScript's + - * / and Math.sqrt give the same bits on every machine, but Math.sin, Math.cos, Math.atan,
// Math.exp and friends are only "approximated": two browsers, or a browser and Node, may differ in the last
// bit. A last bit is enough to change a telemetry digit after a few thousand steps. So the car, the camera,
// the drive scripts and the analysis use these versions instead, which are built from + - * / and sqrt alone.
// The same drive then gives the same numbers in every browser, on every processor, and in Node.
// The polynomials are the classic fdlibm ones (Sun Microsystems, freely usable); accuracy is about 1e-16.
export const PI = 3.141592653589793, TAU = 6.283185307179586, HALF_PI = 1.5707963267948966;

const S1 = -1.66666666666666324348e-01, S2 = 8.33333333332248946124e-03, S3 = -1.98412698298579493134e-04, S4 = 2.75573137070700676789e-06, S5 = -2.50507602534068634195e-08, S6 = 1.58969099521155010221e-10;
const C1 = 4.16666666666666019037e-02, C2 = -1.38888888888741095749e-03, C3 = 2.48015872894767294178e-05, C4 = -2.75573143513906633035e-07, C5 = 2.08757232129817482790e-09, C6 = -1.13596475577881948265e-11;
const ksin = (x, y) => { const z = x * x, w = z * z, r = S2 + z * (S3 + z * S4) + z * w * (S5 + z * S6), v = z * x; return x - ((z * (0.5 * y - v * r) - y) - v * S1); };
const kcos = (x, y) => { const z = x * x, w = z * z, r = z * (C1 + z * (C2 + z * C3)) + w * w * (C4 + z * (C5 + z * C6)), hz = 0.5 * z, a = 1 - hz; return a + (((1 - a) - hz) + (z * r - x * y)); };
// x = n * pi/2 + (y0 + y1), with pi/2 split in three parts so the subtraction stays exact
const P1 = 1.57079632673412561417e+00, P1T = 6.07710050650619224932e-11, P2 = 6.07710050630396597660e-11, P2T = 2.02226624879595063154e-21;
let rn = 0, r0 = 0, r1 = 0;
function reduce(x) {
  const n = Math.round(x * 0.63661977236758134308), r = x - n * P1;
  let w = n * P1T, y = r - w;
  // one more term when a lot cancelled (x close to a multiple of pi/2)
  if (Math.abs(y) < Math.abs(x) * 1.2e-5) { const t = r; w = n * P2; const r2 = t - w; w = n * P2T - ((t - r2) - w); y = r2 - w; r0 = y; r1 = (r2 - y) - w; }
  else { r0 = y; r1 = (r - y) - w; }
  rn = ((n % 4) + 4) % 4;
}
export function sin(x) {
  if (x !== x || x - x !== 0) return NaN;
  if (x > -0.7853981633974483 && x < 0.7853981633974483) return ksin(x, 0);
  reduce(x);
  return rn === 0 ? ksin(r0, r1) : rn === 1 ? kcos(r0, r1) : rn === 2 ? -ksin(r0, r1) : -kcos(r0, r1);
}
export function cos(x) {
  if (x !== x || x - x !== 0) return NaN;
  if (x > -0.7853981633974483 && x < 0.7853981633974483) return kcos(x, 0);
  reduce(x);
  return rn === 0 ? kcos(r0, r1) : rn === 1 ? -ksin(r0, r1) : rn === 2 ? -kcos(r0, r1) : ksin(r0, r1);
}
export const tan = (x) => sin(x) / cos(x);

const AHI = [4.63647609000806093515e-01, 7.85398163397448278999e-01, 9.82793723247329054082e-01, 1.57079632679489655800e+00];
const ALO = [2.26987774529616870924e-17, 3.06161699786838301793e-17, 1.39033110312309984516e-17, 6.12323399573676603587e-17];
const A0 = 3.33333333333329318027e-01, A1 = -1.99999999998764832476e-01, A2 = 1.42857142725034663711e-01, A3 = -1.11111104054623557880e-01, A4 = 9.09088713343650656196e-02, A5 = -7.69187620504482999495e-02, A6 = 6.66107313738753120669e-02, A7 = -5.83357013379057348645e-02, A8 = 4.97687799461593236017e-02, A9 = -3.65315727442169155270e-02, A10 = 1.62858201153657823623e-02;
export function atan(x) {
  if (x !== x) return NaN;
  const neg = x < 0; let a = neg ? -x : x, id;
  if (a > 1e19) return neg ? -HALF_PI : HALF_PI;
  if (a < 0.4375) { if (a < 7.5e-9) return x; id = -1; }
  else if (a < 1.1875) { if (a < 0.6875) { id = 0; a = (2 * a - 1) / (2 + a); } else { id = 1; a = (a - 1) / (a + 1); } }
  else if (a < 2.4375) { id = 2; a = (a - 1.5) / (1 + 1.5 * a); } else { id = 3; a = -1 / a; }
  const z = a * a, w = z * z, s1 = z * (A0 + w * (A2 + w * (A4 + w * (A6 + w * (A8 + w * A10))))), s2 = w * (A1 + w * (A3 + w * (A5 + w * (A7 + w * A9))));
  if (id < 0) { const r = a - a * (s1 + s2); return neg ? -r : r; }
  const r = AHI[id] - ((a * (s1 + s2) - ALO[id]) - a);
  return neg ? -r : r;
}
export function atan2(y, x) {
  if (x === 0) return y > 0 ? HALF_PI : y < 0 ? -HALF_PI : 0;
  const a = atan(y / x);
  return x > 0 ? a : y >= 0 ? a + PI : a - PI;
}
export const asin = (x) => atan2(x, Math.sqrt((1 - x) * (1 + x)));

// exact powers of two by repeated doubling
const P2TAB = new Float64Array(2200); { let p = 1; for (let k = 0; k <= 1023; k++) { P2TAB[1100 + k] = p; p *= 2; } p = 1; for (let k = 0; k >= -1074; k--) { P2TAB[1100 + k] = p; p *= 0.5; } }
const LN2HI = 6.93147180369123816490e-01, LN2LO = 1.90821492927058770002e-10, INVLN2 = 1.44269504088896338700e+00;
const E1 = 1.66666666666666019037e-01, E2 = -2.77777777770155933842e-03, E3 = 6.61375632143793436117e-05, E4 = -1.65339022054652515390e-06, E5 = 4.13813679705723846039e-08;
export function exp(x) {
  if (x !== x) return NaN; if (x > 709.78) return Infinity; if (x < -745.2) return 0;
  let hi = x, lo = 0, k = 0;
  if (x > 0.34657359027997264 || x < -0.34657359027997264) { k = Math.floor(INVLN2 * x + 0.5); hi = x - k * LN2HI; lo = k * LN2LO; }
  const r = hi - lo, xx = r * r, c = r - xx * (E1 + xx * (E2 + xx * (E3 + xx * (E4 + xx * E5)))), y = 1 + (r * c / (2 - c) - lo + hi);
  if (k === 0) return y;
  return k > -1000 ? y * P2TAB[1100 + k] : y * P2TAB[1100 + k + 1000] * P2TAB[100];
}
const L1 = 6.666666666666735130e-01, L2 = 3.999999999940941908e-01, L3 = 2.857142874366239149e-01, L4 = 2.222219843214978396e-01, L5 = 1.818357216161805012e-01, L6 = 1.531383769920937332e-01, L7 = 1.479819860511658591e-01;
export function ln(x) {
  if (!(x > 0)) return x === 0 ? -Infinity : NaN; if (x === Infinity) return x;
  let k = 0, m = x;
  while (m >= 1.4142135623730951) { m *= 0.5; k++; } while (m < 0.7071067811865476) { m *= 2; k--; }     // exact scalings
  const f = m - 1, s = f / (2 + f), z = s * s, w = z * z, t1 = w * (L2 + w * (L4 + w * L6)), t2 = z * (L1 + w * (L3 + w * (L5 + w * L7))), R = t2 + t1, hfsq = 0.5 * f * f;
  return k * LN2HI - ((hfsq - (s * (hfsq + R) + k * LN2LO)) - f);
}
// x to the power y for x >= 0
export const pow = (x, y) => (x <= 0 ? (y === 0 ? 1 : 0) : exp(y * ln(x)));
export const hypot = (x, y) => Math.sqrt(x * x + y * y);
export const hypot3 = (x, y, z) => Math.sqrt(x * x + y * y + z * z);
export const hypot4 = (x, y, z, w) => Math.sqrt(x * x + y * y + z * z + w * w);
