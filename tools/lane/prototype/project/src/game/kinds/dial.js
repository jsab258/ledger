// New kinds of act of the system "dial": a gun shown, a gun fired, a hold-up (DESIGN 7, ADDENDUM A41).
// sev 0..1 newsworthy, val -1 menace..1 decent, crime 0..4; town: what the real town is told of it.
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  gun_shown: {
    sev: 0.95, val: -0.9, crime: 3, loud: 1, forever: 1, grudge: 1, town: 'saw',
    truth: (e) => `Tom showed a gun${e.target ? ' to ' + n(e) : ''} on ${e.zone}`,
    mine: (e) => `Showed the gun${e.target ? ' to ' + n(e) : ''}`,
  },
  gun_fired: {
    sev: 1, val: -1, crime: 4, loud: 1, forever: 1, grudge: 1, town: 'saw',
    truth: (e) => `Tom fired a gun on ${e.zone}${e.target ? ' at ' + n(e) : ''}`,
    mine: (e) => `Fired the gun on ${e.zone}`,
  },
  gun_got: {
    sev: 0.8, val: -0.7, crime: 2, town: 'saw',
    truth: (e) => `Tom got hold of a gun${e.target ? ' through ' + n(e) : ''}`,
    mine: (e) => `Got a gun${e.target ? ' through ' + n(e) : ''}`,
  },
  holdup: {
    sev: 0.95, val: -0.95, crime: 3, loud: 1, forever: 1, grudge: 1, town: 'saw',
    truth: (e) => `Tom held up ${n(e)} with a ${e.weapon || 'weapon'} on ${e.zone}`,
    mine: (e) => `Held up ${n(e)} with the ${e.weapon || 'weapon'}`,
  },
};
