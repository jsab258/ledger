// New kinds of act for the system "law": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/law.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
const n = (e) => e.name || 'an officer';
export const KINDS_ADD = {
  searched_by: K('searched_by', (e) => `A constable stopped Tom on ${e.zone} and went through his pockets`, (e) => `Was searched on ${e.zone}`, { loud: 1 }),
  talked_round: K('talked_round', (e) => `Tom talked a constable round on ${e.zone}`, (e) => `Talked the constable round on ${e.zone}`, { town: { tell: 'open' } }),
  paid_quiet: K('paid_quiet', (e) => `Tom put money in ${e.name || 'a witness'}'s hand to keep quiet`, (e) => `Paid ${e.name || 'a witness'} to keep quiet`, { priv: 1 }),
  paid_officer: K('paid_officer', (e) => `Tom put money in ${n(e)}'s hand`, (e) => `Paid ${n(e)}`, { priv: 1 }),
  stopped_car: K('stopped_car', (e) => `The police pulled Mickey's cab over on ${e.zone}`, (e) => `Was pulled over on ${e.zone}`, { loud: 1 }),
  drove_off_police: K('drove_off_police', (e) => `A Mickey's cab would not stop for the police on ${e.zone}`, (e) => `Drove off from the police on ${e.zone}`, { loud: 1 }),
  office_searched: K('office_searched', () => "The police went through Mickey's office", () => 'The office was searched', { noself: true }),
};
