// New kinds of act of the system "fightx". Fields as kinds.js.
const n = (e) => e.name || 'a man';
export const KINDS_ADD = {
  quiet_blow: { sev: 0.75, val: -0.85, crime: 3, grudge: 1, town: 'saw', truth: (e) => `Tom Nowak knocked ${n(e)} out from behind`, mine: (e) => `Put ${n(e)} out from behind. He never saw who` },
  weapon_drawn: { sev: 0.6, val: -0.7, crime: 2, town: 'saw', truth: (e) => `Tom Nowak had a ${e.weapon || 'weapon'} out in the street`, mine: (e) => `Had the ${e.weapon || 'weapon'} out in the open` },
  put_in_water: { sev: 0.6, val: -0.5, crime: 2, loud: 1, town: 'saw', truth: (e) => `Tom Nowak put ${n(e)} in the water off the quay`, mine: (e) => `Put ${n(e)} in the water. He climbed out, soaked` },
  searched_man: { sev: 0.5, val: -0.6, crime: 2, town: 'saw', truth: (e) => `Tom Nowak went through ${n(e)}'s pockets while he lay there`, mine: (e) => `Went through ${n(e)}'s pockets` },
  stepped_in: { sev: 0.3, val: -0.2, crime: 0, noself: true, town: 'open', truth: () => 'People stepped in and stopped a fight Tom Nowak was in', mine: () => 'People stepped in and stopped it' },
};
