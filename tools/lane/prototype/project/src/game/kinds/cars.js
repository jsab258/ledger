// New kinds of act for the system "cars": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/cars.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  hit_stopped: K('hit_stopped', (e) => `Tom knocked ${n(e)} down with the cab on ${e.zone}, and stopped and stayed with them`, (e) => `Stopped for ${n(e)} after the knock`, { town: { tell: 'open' } }),
  hit_and_run: K('hit_and_run', (e) => `A Mickey's cab knocked ${n(e)} down on ${e.zone} and never stopped`, (e) => `Drove off after knocking ${n(e)} down`, { grudge: 1, loud: 1, forever: 1 }),
  horn_night: K('horn_night', (e) => `Somebody leaned on a car horn on ${e.zone} in the night`, (e) => `Sounded the horn on ${e.zone} at night`, { loud: 1, noself: true }),
  rode: K('rode', (e) => `Tom was driven ${e.dest || 'across town'} by ${n(e)}`, (e) => `Was driven ${e.dest || 'across town'} by ${n(e)}`, { town: { tell: 'open' } }),
  resprayed: K('resprayed', () => "Shaun Hewson has had one of Mickey's cars in his lock-up, and it came out another colour", () => 'Had the car resprayed', { priv: 1 }),
};
