// New kinds of act of the system "firm": the firm growing, in the open and not.
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  car_bought: {
    sev: 0.5, val: 0.2, crime: 0, town: 'open',
    truth: (e) => `Mickey's has another car on the road, bought off ${n(e)}`,
    mine: (e) => `Bought a car off ${n(e)}`,
  },
  account_won: {
    sev: 0.6, val: 0.4, crime: 0, town: 'open',
    truth: (e) => `Mickey's has ${e.what || 'a contract'}`,
    mine: (e) => `Won ${e.what || 'a contract'}`,
  },
  rank_won: {
    sev: 0.5, val: 0.1, crime: 0, town: 'open',
    truth: (e) => `Mickey's cars work ${e.what || 'another rank'} now`,
    mine: (e) => `Took ${e.what || 'another rank'}`,
  },
  front_bought: {
    sev: 0.5, val: 0.1, crime: 0, town: 'open',
    truth: (e) => `Tom has put money into ${e.what || 'a business on the street'}`,
    mine: (e) => `Bought into ${e.what || 'a business'}`,
  },
  front_pressed: {
    sev: 0.7, val: -0.7, crime: 2, town: 'saw', grudge: 1,
    truth: (e) => `Tom leaned on ${n(e)} for a share of ${e.what || 'the business'}`,
    mine: (e) => `Leaned on ${n(e)} for a share`,
  },
  round_taken: {
    sev: 0.6, val: -0.6, crime: 2, town: 'saw',
    truth: (e) => `Mickey's men collect on ${e.what || 'the street'} now`,
    mine: (e) => `Started a round on ${e.what || 'the street'}`,
  },
  wages_missed: {
    sev: 0.5, val: -0.3, crime: 0, town: 'open', noself: true,
    truth: () => "Mickey's could not pay its drivers on the Friday",
    mine: () => 'Could not pay the drivers',
  },
};
