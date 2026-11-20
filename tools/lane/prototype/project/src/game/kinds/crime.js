// New kinds of act for the system "crime": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/crime.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  // damage by hand (A35): the deed the real town's week follows (damage: 1; game/town.js)
  window_in: K('window_in', (e) => `Tom put ${e.thing || 'a window'} in on ${e.zone}`, (e) => `Put ${e.thing || 'a window'} in`, { loud: 1, damage: 1 }),
};
