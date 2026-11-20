// New kinds of act of the system "law". Each: { sev, val, crime, truth: (E) => words, mine: (E) => words, ...flags as kinds.js,
// town: 'deed' | 'saw' | 'open' | null } (what the real town is told of it). sev 0..1 newsworthy, val -1 menace..1 decent,
// crime 0..4. Imports nothing but may read E.
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  law_paid_witness: {
    sev: 0.5, val: -0.35, crime: 0, town: 'saw',
    truth: (e) => `Tom put money in ${n(e)}'s hand to keep it from the police`,
    mine: (e) => `Paid ${n(e)} to say nothing to the police`,
  },
  law_turned_witness: {
    sev: 0.3, val: -0.1, crime: 0, town: 'saw',
    truth: (e) => `Tom stopped ${n(e)} on the way to the phone box and talked it over`,
    mine: (e) => `Talked ${n(e)} out of going to the police`,
  },
  law_helped_witness: {
    sev: 0.3, val: 0.4, crime: 0, town: 'open',
    truth: (e) => `Tom walked ${n(e)} home and carried the bag`,
    mine: (e) => `Did ${n(e)} a decent turn`,
  },
  law_searched: {
    sev: 0.6, val: -0.3, crime: 0, town: 'saw', loud: 1,
    truth: (e) => `A constable stopped Tom on ${e.zone} and went through his pockets`,
    mine: (e) => `Stopped and searched on ${e.zone}${e.what ? ': he kept ' + e.what : ''}`,
  },
  law_note_offered: {
    sev: 0.8, val: -0.6, crime: 1, town: 'saw',
    truth: (e) => `Tom offered a police officer money on ${e.zone}`,
    mine: () => 'Offered a note to an officer who would not take it',
  },
  law_officer_paid: {
    sev: 0.7, val: -0.5, crime: 0, town: 'saw', priv: 1,
    truth: (e) => `Tom put money in ${n(e)}'s hand`,
    mine: (e) => `Paid ${n(e)}`,
  },
  law_found: {
    sev: 0.6, val: -0.4, crime: 0, town: null, noself: true,
    truth: (e) => `Somebody found ${e.what || 'what was left'} on ${e.zone}`,
    mine: (e) => `${e.what || 'What was left'} on ${e.zone} has been found`,
  },
  law_missing: {
    sev: 0.8, val: -0.3, crime: 0, town: null, noself: true,
    truth: (e) => `Nobody has seen ${n(e)} since ${e.since || 'the other day'}`,
    mine: (e) => `People are asking where ${n(e)} is`,
  },
  law_office_searched: {
    sev: 0.8, val: -0.4, crime: 0, town: null, noself: true,
    truth: () => "The police went through Mickey's office with a warrant",
    mine: () => 'The police searched the office',
  },
  law_manhunt: {
    sev: 1, val: -0.7, crime: 0, town: null, noself: true,
    truth: () => "A police car went down Quay Street giving Tom's description",
    mine: () => 'The police are giving out his description',
  },
};
