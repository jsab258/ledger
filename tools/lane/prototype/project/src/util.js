// Small shared helpers. No rendering imports here so the simulation can run in Node tests.
export const TAU = Math.PI * 2;
export const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
export const lerp = (a, b, t) => a + (b - a) * t;
export const smooth = (a, b, x) => {
  const t = clamp((x - a) / (b - a), 0, 1);
  return t * t * (3 - 2 * t);
};
export const hyp = (ax, az, bx, bz) => Math.hypot(ax - bx, az - bz);
export function angDiff(a, b) {
  let d = (b - a) % TAU;
  if (d > Math.PI) d -= TAU;
  if (d < -Math.PI) d += TAU;
  return d;
}
export function rng(seed) {
  let s = seed >>> 0;
  return function () {
    s |= 0;
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export const R = { f: Math.random }; // swappable for deterministic tests
export const rnd = (a = 1, b) => (b === undefined ? R.f() * a : a + R.f() * (b - a));
export const pick = (arr) => arr[Math.floor(R.f() * arr.length) % arr.length];
export const chance = (p) => R.f() < p;
// Segment vs axis-aligned rect {x0,z0,x1,z1}
export function segRect(ax, az, bx, bz, r) {
  let t0 = 0,
    t1 = 1;
  const dx = bx - ax,
    dz = bz - az;
  const p = [-dx, dx, -dz, dz],
    q = [ax - r.x0, r.x1 - ax, az - r.z0, r.z1 - az];
  for (let i = 0; i < 4; i++) {
    if (p[i] === 0) {
      if (q[i] < 0) return false;
    } else {
      const t = q[i] / p[i];
      if (p[i] < 0) {
        if (t > t1) return false;
        if (t > t0) t0 = t;
      } else {
        if (t < t0) return false;
        if (t < t1) t1 = t;
      }
    }
  }
  return true;
}
export const inRect = (x, z, r, m = 0) => x >= r.x0 - m && x <= r.x1 + m && z >= r.z0 - m && z <= r.z1 + m;
export function money(p) {
  p = Math.round(p);
  const neg = p < 0;
  p = Math.abs(p);
  return (neg ? '-' : '') + '£' + Math.floor(p / 100) + '.' + String(p % 100).padStart(2, '0');
}
export const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
export const DAYS3 = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
export function hhmm(h) {
  h = ((h % 24) + 24) % 24;
  const m = Math.floor((h % 1) * 60);
  return String(Math.floor(h)).padStart(2, '0') + ':' + String(m).padStart(2, '0');
}
export function hourWords(h) {
  h = Math.floor(((h % 24) + 24) % 24);
  if (h < 5)
    return [
      'midnight',
      'one in the morning',
      'two in the morning',
      'three in the morning',
      'four in the morning',
    ][h];
  if (h < 12) return ['five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven'][h - 5] + ' in the morning';
  if (h === 12) return 'dinner time';
  if (h < 18) return ['one', 'two', 'three', 'four', 'five'][h - 13] + ' in the afternoon';
  return ['six', 'seven', 'eight', 'nine', 'ten', 'eleven'][h - 18] + ' at night';
}
export const esc = (s) =>
  String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
export const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
export function listAnd(a) {
  return a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
}

// money as he would say it: "twenty-two pounds", "eight pounds fifty"
const ONES = [
    'nought',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten',
    'eleven',
    'twelve',
    'thirteen',
    'fourteen',
    'fifteen',
    'sixteen',
    'seventeen',
    'eighteen',
    'nineteen',
  ],
  TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
const numWords = (n) =>
  n < 20
    ? ONES[n]
    : n < 100
      ? TENS[Math.floor(n / 10)] + (n % 10 ? '-' + ONES[n % 10] : '')
      : n < 1000
        ? ONES[Math.floor(n / 100)] + ' hundred' + (n % 100 ? ' and ' + numWords(n % 100) : '')
        : String(n);
export function pounds(p) {
  p = Math.round(Math.abs(p));
  const l = Math.floor(p / 100),
    d = p % 100;
  if (!l) return numWords(d) + ' pence';
  return numWords(l) + (l === 1 ? ' pound' : ' pounds') + (d ? ' ' + numWords(d) : '');
}

// ---------- how the Ledger writes things ----------
// Money "£18.00" or "80p". Times "6.30pm". Dates "Fri 19 Oct". Monday is 15 October 1990.
export function quid(pence) {
  pence = Math.round(pence);
  const neg = pence < 0 ? '-' : '';
  pence = Math.abs(pence);
  if (pence < 100) return neg + pence + 'p';
  return neg + '£' + Math.floor(pence / 100) + '.' + String(pence % 100).padStart(2, '0');
}
export function clockText(gameMinutes) {
  const m = Math.floor(((gameMinutes % 1440) + 1440) % 1440),
    h = Math.floor(m / 60),
    mm = m % 60;
  return (h % 12 === 0 ? 12 : h % 12) + '.' + String(mm).padStart(2, '0') + (h < 12 ? 'am' : 'pm');
}
export function dateText(gameMinutes) {
  const d = Math.floor(gameMinutes / 1440);
  return DAYS3[((d % 7) + 7) % 7] + ' ' + (15 + d) + ' Oct';
}
export const countWords = (text) => String(text).trim().split(/\s+/).filter(Boolean).length;
// Keep whole sentences while they fit in n words; a first sentence that is too long is cut at n words.
export function clipWords(text, n) {
  text = String(text).trim();
  if (countWords(text) <= n) return text;
  let out = '';
  for (const s of text.match(/[^.!?]+[.!?]*/g) || [text]) {
    if (countWords(out + s) > n) break;
    out += s;
  }
  if (out.trim()) return out.trim();
  return (
    text
      .split(/\s+/)
      .slice(0, n)
      .join(' ')
      .replace(/[,;:]$/, '') + '.'
  );
}
