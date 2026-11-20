// New kinds of act for the system "fares": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/fares.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
export const KINDS_ADD = {
  waited_for: K('waited_for', (e) => `A Mickey's cab sat with its engine running outside ${e.place || 'the Harbour Office'} while a man was in and out`, (e) => `Kept the engine running outside ${e.place || 'the Harbour Office'}`),
  took_parcel: K('took_parcel', () => "Tom took a parcel round for a fare, no questions", () => 'Took a parcel round for a fare'),
  runner_let_go: K('runner_let_go', (e) => `Tom ran a fare-dodger down on ${e.zone} and let him go`, () => 'Let the runner go', { town: { tell: 'open' } }),
  runner_paid: K('runner_paid', (e) => `Tom ran a fare-dodger down on ${e.zone} and had the fare off him`, () => 'Had the fare off the runner'),
  drove_quiet: K('drove_quiet', () => 'Tom told the reporter nothing', () => 'Told the reporter nothing', { town: { tell: 'open' } }),
};
