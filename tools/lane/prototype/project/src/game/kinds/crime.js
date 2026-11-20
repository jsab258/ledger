// New kinds of act for the system "crime": the same fields as kinds.js (sev, val, crime, truth, mine and the flags).
import { TUNE as T } from '../tune/crime.js';
const K = (id, truth, mine, o = {}) => Object.assign({ sev: T.kinds[id][0], val: T.kinds[id][1], crime: T.kinds[id][2], truth, mine }, o);
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  // damage by hand (A35): the deed the real town's week follows (damage: 1; game/town.js)
  window_in: K('window_in', (e) => `Tom put ${e.thing || 'a window'} in on ${e.zone}`, (e) => `Put ${e.thing || 'a window'} in`, { loud: 1, damage: 1 }),
  forced_door: K('forced_door', (e) => `Tom forced ${e.thing || 'a door'} on ${e.zone}`, (e) => `Forced ${e.thing || 'a door'}`, { loud: 1, damage: 1 }),
  car_taken: K('car_taken', (e) => `Tom broke into ${e.thing || 'a parked car'} on ${e.zone} and drove it off`, (e) => `Took ${e.thing || 'a parked car'}`, { loud: 1, damage: 1 }),
  broke_in: K('broke_in', (e) => `Tom was inside ${e.place || 'a place'} after hours`, (e) => `Was inside ${e.place || 'a place'} after hours`),
  searched: K('searched', (e) => `Tom went through ${e.thing || 'the drawers'} at ${e.place || e.zone}`, (e) => `Went through ${e.thing || 'the drawers'} at ${e.place || e.zone}`),
  lifted: K('lifted', (e) => `Tom took ${e.thing || 'goods'} from ${e.place || e.zone}`, (e) => `Took ${e.thing || 'goods'} from ${e.place || e.zone}`),
  pocket: K('pocket', (e) => `Tom had his hand in ${n(e)}'s pocket on ${e.zone}`, (e) => `Was felt at ${n(e)}'s pocket`, { grudge: 1 }),
  fenced: K('fenced', (e) => `Tom sold ${e.thing || 'goods'} in Rita's back room`, (e) => `Sold ${e.thing || 'goods'} at Rita's`),
  sold_back: K('sold_back', (e) => `Tom tried to sell ${n(e)} their own goods`, (e) => `Tried to sell ${n(e)} their own goods`, { grudge: 1 }),
  cased: K('cased', (e) => `Tom stood a long while watching ${e.place || 'a place'}`, (e) => `Watched ${e.place || 'a place'}`),
  threw_in: K('threw_in', (e) => `Tom threw ${e.thing || 'something'} into the water off ${e.zone}`, (e) => `Threw ${e.thing || 'something'} in the water`),
  washed: K('washed', () => 'Tom put a coat through a service wash at the Washeteria', () => 'Washed the coat at the Washeteria', { town: { tell: 'open' } }),
  dog_barked: K('dog_barked', (e) => `The dog in ${e.place || 'the yard'} barked at somebody in the night`, (e) => `Set the dog off at ${e.place || 'the yard'}`, { loud: 1, noself: true }),
  holdup: K('holdup', (e) => `Tom held up ${e.place || 'a shop'} with a ${e.weapon || 'weapon'} in his hand`, (e) => `Held up ${e.place || 'a shop'}`, { loud: 1, grudge: 1 }),
  torch_seen: K('torch_seen', (e) => `A torch was moving about inside ${e.place || 'a place'} after hours`, (e) => `Showed a light inside ${e.place || 'a place'}`, { noself: true }),
};
