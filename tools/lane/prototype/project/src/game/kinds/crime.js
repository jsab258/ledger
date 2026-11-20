// New kinds of act of the system "crime". town: what the real town is told of it ('deed': a thing damaged, the one
// kind the real town takes to the police; 'saw': a sighting of his hidden life; 'open': an open, decent act).
const n = (e) => e.name || 'someone';
const K = (sev, val, crime, truth, mine, o = {}) => Object.assign({ sev, val, crime, truth, mine }, o);
export const KINDS_ADD = {
  break_in: K(0.8, -0.7, 2, (e) => `Tom forced the door of ${e.what || 'a place'} on ${e.zone}`, (e) => `Forced the door of ${e.what || 'a place'}`, { loud: 1, town: 'deed' }),
  let_in: K(0.45, -0.35, 1, (e) => `Tom let himself into ${e.what || 'a place'} on ${e.zone} when nobody was there`, (e) => `Let myself into ${e.what || 'a place'}`, { town: 'saw' }),
  searched_place: K(0.5, -0.45, 1, (e) => `Tom went through ${e.what || 'somebody\'s things'} on ${e.zone}`, (e) => `Went through ${e.what || 'the place'}`, { town: 'saw' }),
  forced_cupboard: K(0.6, -0.5, 2, (e) => `Tom broke open ${e.what || 'a cupboard'} on ${e.zone}`, (e) => `Broke open ${e.what || 'a cupboard'}`, { loud: 1, town: 'deed' }),
  took_goods: K(0.6, -0.55, 2, (e) => `Tom carried ${e.what || 'goods'} out of ${e.from || 'a place'} on ${e.zone}`, (e) => `Took ${e.what || 'goods'} from ${e.from || 'the place'}`, { town: 'saw' }),
  pocket_felt: K(0.65, -0.6, 2, (e) => `Tom had his hand in ${n(e)}'s pocket on ${e.zone}`, (e) => `${n(e)} felt a hand in the pocket`, { grudge: 1, town: 'saw' }),
  pocket_lift: K(0.3, -0.4, 2, (e) => `Tom lifted ${e.what || 'something'} from ${n(e)}'s pocket on ${e.zone}`, (e) => `Lifted ${e.what || 'something'} from ${n(e)}'s pocket`, { town: 'saw' }),
  key_missed: K(0.4, -0.3, 1, (e) => `${n(e)} found ${e.what || 'a key'} gone by morning`, (e) => `${n(e)} has missed ${e.what || 'the key'}`, { noself: true, town: null }),
  damage_thing: K(0.75, -0.65, 2, (e) => `Tom smashed ${e.what || 'a window'} on ${e.zone}`, (e) => `Smashed ${e.what || 'a window'}`, { loud: 1, grudge: 1, town: 'deed' }),
  damage_found: K(0.5, -0.3, 0, (e) => `${n(e)} found ${e.what || 'the damage'} in the morning`, (e) => `${n(e)} has found ${e.what || 'the damage'}`, { noself: true, town: null }),
  tailed: K(0.35, -0.3, 0, (e) => `Tom was following ${n(e)} along ${e.zone}`, (e) => `${n(e)} caught me following`, { town: 'saw' }),
  stood_with: K(0.3, 0, 0, (e) => `Tom stood with ${n(e)} on ${e.zone}`, (e) => `Stood with ${n(e)} on ${e.zone}`, { town: 'open' }),
  cased: K(0.25, -0.2, 0, (e) => `Tom stood a long while watching ${e.what || 'a place'} on ${e.zone}`, (e) => `Watched ${e.what || 'a place'} a while`, { town: 'saw' }),
  threw_in: K(0.45, -0.4, 0, (e) => `Tom threw ${e.what || 'something'} into the water off ${e.zone}`, (e) => `Threw ${e.what || 'it'} in the water`, { town: 'saw' }),
  coat_washed: K(0.3, -0.15, 0, (e) => `Tom had a coat washed at the Washeteria`, () => 'Had the coat washed at the Washeteria', { town: 'open' }),
  washed_up: K(0.2, -0.2, 0, (e) => `Tom was washing blood off on ${e.zone}`, () => 'Washed the blood off', { town: 'saw' }),
  trespass: K(0.4, -0.3, 1, (e) => `Tom was where he had no business, at ${e.what || 'a yard'} on ${e.zone}`, (e) => `Warned off ${e.what || 'the yard'}`, { town: 'saw' }),
  fenced: K(0.4, -0.3, 1, (e) => `Tom sold ${e.what || 'goods'} in Rita's back room`, (e) => `Sold ${e.what || 'goods'} to Rita`, { priv: 1, town: 'saw' }),
  fed_dog: K(0.1, 0.1, 0, (e) => `Tom gave the yard dog a scrap on ${e.zone}`, () => 'Gave the yard dog a scrap', { town: 'open' }),
  debt_kind: K(0.4, 0.3, 0, (e) => `Tom let ${n(e)} pay what was owed another way`, (e) => `Let ${n(e)} pay another way`, { town: 'open' }),
};
