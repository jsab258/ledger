// New kinds of act of the system "rivals": how he answered a pressure, and what a rival did on his street.
const n = (e) => e.name || 'them';
export const KINDS_ADD = {
  rival_paid: {
    sev: 0.6, val: -0.2, crime: 0, town: 'open',
    truth: (e) => `Tom paid ${n(e)} what was asked`,
    mine: (e) => `Paid ${n(e)}`,
  },
  rival_defied: {
    sev: 0.7, val: 0.2, crime: 0, town: 'open',
    truth: (e) => `Tom told ${n(e)} no, to the face of the one who came`,
    mine: (e) => `Told ${n(e)} no`,
  },
  rival_countered: {
    sev: 0.7, val: -0.1, crime: 0, town: null,
    truth: (e) => `Tom knew something about ${n(e)} and used it`,
    mine: (e) => `Used what he knew about ${n(e)}`,
  },
  rival_sat_down: {
    sev: 0.9, val: 0, crime: 0, town: 'open',
    truth: (e) => `Tom sat down with ${n(e)}`,
    mine: (e) => `Sat down with ${n(e)}`,
  },
  rival_trouble: {
    sev: 0.7, val: -0.4, crime: 2, town: 'saw', loud: 1, noself: true,
    truth: (e) => `There was trouble on ${e.zone}, and people put it down to Mickey's`,
    mine: (e) => `Trouble on ${e.zone} that was not his`,
  },
  fixer_paid: {
    sev: 0.3, val: -0.1, crime: 0, town: null,
    truth: () => 'Tom paid Keith Garbutt for his time',
    mine: () => 'Paid the Fixer',
  },
};
