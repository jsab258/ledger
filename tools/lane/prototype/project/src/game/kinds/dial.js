// New kinds of act for the system "dial": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/dial.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
export const KINDS_ADD = {
  gun_shown: K('gun_shown', (e) => `Tom had a gun in his hand on ${e.zone}`, (e) => `Showed the gun on ${e.zone}`, { loud: 1, grudge: 1, forever: 1 }),
  shot_fired: K('shot_fired', (e) => `A shot was fired on ${e.zone}`, (e) => `Fired a shot on ${e.zone}`, { loud: 1, forever: 1 }),
  armed_crew: K('armed_crew', () => "Tom's men are carrying now, and everybody knows who brought the guns in", () => 'Armed his men', { forever: 1 }),
};
