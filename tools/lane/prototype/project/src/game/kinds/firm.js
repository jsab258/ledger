// New kinds of act for the system "firm": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/firm.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
export const KINDS_ADD = {
  bought_car: K('bought_car', () => "Mickey's has another car on the road", () => 'Bought another car for the firm', { town: { tell: 'open' } }),
  took_rank: K('took_rank', (e) => `Mickey's cars stand on ${e.rank || 'another rank'} now`, (e) => `The firm holds ${e.rank || 'another rank'}`, { town: { tell: 'open' } }),
};
