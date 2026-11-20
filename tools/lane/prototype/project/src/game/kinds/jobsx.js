// New kinds of act for the system "jobsx": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/jobsx.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  minded: K('minded', (e) => `Tom stood with ${n(e)} at ${e.place || e.zone}`, (e) => `Stood with ${n(e)} at ${e.place || e.zone}`),
  side_done: K('side_done', (e) => `Tom did ${n(e)} a turn: ${e.what || 'a small thing'}`, (e) => `Did ${n(e)} a turn`, { town: { tell: 'open' } }),
  side_bad: K('side_bad', (e) => `Tom left ${n(e)} to it: ${e.what || 'a small thing'}`, (e) => `Left ${n(e)} to it`),
};
