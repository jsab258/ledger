// New kinds of act for the system "foot": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/foot.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  nod: K('nod', (e) => `Tom gave ${n(e)} a nod on ${e.zone}`, (e) => `Nodded to ${n(e)}`, { town: { tell: 'open' } }),
  greet: K('greet', (e) => `Tom passed the time of day with ${n(e)} on ${e.zone}`, (e) => `Said good day to ${n(e)}`, { town: { tell: 'open' } }),
  hard_look: K('hard_look', (e) => `Tom gave ${n(e)} a hard look on ${e.zone}`, (e) => `Gave ${n(e)} a hard look`, { grudge: 1 }),
  called_out: K('called_out', (e) => `Tom shouted after ${n(e)} on ${e.zone}`, (e) => `Called after ${n(e)}`, { loud: 1 }),
  trespass: K('trespass', (e) => `Tom was where he had no business, at ${e.place || e.zone}`, (e) => `Was caught where he should not be, at ${e.place || e.zone}`),
  noise_made: K('noise_made', (e) => `Somebody threw something on ${e.zone}`, (e) => `Made a noise on ${e.zone} to turn a head`, { loud: 1, noself: true }),
  followed: K('followed', (e) => `Tom was following ${n(e)} along ${e.zone}`, (e) => `Was made following ${n(e)}`, { grudge: 1 }),
  collared: K('collared', (e) => `Tom ran ${n(e)} down and took him by the collar on ${e.zone}`, (e) => `Ran ${n(e)} down`, { grudge: 1, loud: 1 }),
};
