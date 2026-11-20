// New kinds of act for the system "life": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/life.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
export const KINDS_ADD = {
  helped: K('helped', (e) => `Tom stopped to help on ${e.zone}: ${e.what || 'a small thing'}`, (e) => `Stopped to help: ${e.what || 'a small thing'}`, { town: { tell: 'open' } }),
  stepped_in: K('stepped_in', (e) => `Tom stepped in on ${e.zone}: ${e.what || 'a small thing'}`, (e) => `Stepped in: ${e.what || 'a small thing'}`, { town: { tell: 'open' } }),
  walked_past: K('walked_past', (e) => `Tom walked past ${e.what || 'somebody in trouble'} on ${e.zone}`, (e) => `Walked past ${e.what || 'somebody in trouble'}`),
  body_hidden: K('body_hidden', (e) => `Tom put a body in the water off ${e.zone}`, (e) => `Put ${e.name || 'the body'} in the water`, { forever: 1 }),
};
