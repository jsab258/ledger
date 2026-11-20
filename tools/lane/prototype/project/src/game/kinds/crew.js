// New kinds of act for the system "crew": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/crew.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  sent: K('sent', (e) => `${e.through || 'One of Tom\'s men'} did it on Tom's word: ${e.verb || 'a job'}${e.name ? ', ' + e.name : ''}`, (e) => `Sent ${e.through || 'a man'}: ${e.verb || 'a job'}${e.name ? ', ' + e.name : ''}`, { priv: 1 }),
  leaned: K('leaned', (e) => `${e.through || 'One of Tom\'s men'} leaned on ${n(e)} for Tom`, (e) => `Had ${e.through || 'a man'} lean on ${n(e)}`, { grudge: 1 }),
  stood_with: K('stood_with', (e) => `Tom and ${n(e)} were together on ${e.zone}`, (e) => `Was seen with ${n(e)} on ${e.zone}`),
};
