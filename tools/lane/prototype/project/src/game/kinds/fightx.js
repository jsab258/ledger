// New kinds of act for the system "fightx": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/fightx.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  sparred: K('sparred', () => 'Tom went a few rounds with the gloves on at the boxing club', () => 'Sparred at the boxing club', { town: { tell: 'open' } }),
  searched_man: K('searched_man', (e) => `Tom went through ${n(e)}'s pockets while he was down on ${e.zone}`, (e) => `Went through ${n(e)}'s pockets`, { grudge: 1 }),
  quiet_blow: K('quiet_blow', (e) => `Tom struck ${n(e)} from behind on ${e.zone}`, (e) => `Put ${n(e)} down from behind`, { grudge: 1 }),
};
