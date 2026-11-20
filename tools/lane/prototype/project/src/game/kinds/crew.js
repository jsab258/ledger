// New kinds of act of the system "crew": what a man of his did on his word, and what he paid him.
const n = (e) => e.name || 'someone';
const KN = { ron: 'Ron Kirby', darren: 'Darren Milner', kevin: 'Kevin Needham', terry: 'Terry Hodgson', lee: 'Lee Drewery', julie: 'Julie Kettlewell' };
const via = (e) => KN[e.via] || e.viaName || 'one of his men';
const S = (sev, val, crime, what, extra = {}) =>
  Object.assign(
    {
      sev, val, crime, town: 'saw',
      truth: (e) => `${via(e)} ${what} ${n(e)}, and it was Tom who sent him`,
      mine: (e) => `Sent ${via(e)}: ${what} ${n(e)}`,
    },
    extra,
  );
export const KINDS_ADD = {
  crew_leaned: S(0.6, -0.6, 2, 'leaned on', { grudge: 1 }),
  crew_fetched: S(0.3, -0.2, 0, 'fetched'),
  sent_hurt: S(0.9, -0.9, 3, 'hurt', { grudge: 1, loud: 1 }),
  sent_plan: S(0.5, -0.4, 1, 'put a plan round'),
  sent_frame: S(0.7, -0.7, 2, 'put a story about on'),
  sent_lean_witness: S(0.7, -0.8, 3, 'leaned on a witness,', { grudge: 1 }),
  sent_body: S(0.9, -0.9, 3, 'moved what was left of'),
  sent_discipline: S(0.6, -0.5, 1, 'made an example of', { grudge: 1 }),
  sent_property: S(0.8, -0.8, 3, 'went at the place of', { grudge: 1, loud: 1 }),
  sent_vouch: {
    sev: 0.4, val: 0.4, crime: 0, town: 'open',
    truth: (e) => `${via(e)} spoke up for Tom to ${n(e)}`,
    mine: (e) => `Had ${via(e)} speak for him to ${n(e)}`,
  },
  crew_joined: {
    sev: 0.5, val: 0.1, crime: 0, town: 'open',
    truth: (e) => `${n(e)} is working for Mickey's now`,
    mine: (e) => `Took ${n(e)} on`,
  },
  crew_hooked: {
    sev: 0.6, val: -0.5, crime: 1, town: 'saw', grudge: 1,
    truth: (e) => `Tom has something over ${n(e)}, and ${n(e)} works for him because of it`,
    mine: (e) => `Used what he had on ${n(e)}`,
  },
  crew_paid_short: {
    sev: 0.4, val: -0.4, crime: 0, town: 'open', grudge: 1,
    truth: (e) => `Tom paid ${n(e)} short for a night's work`,
    mine: (e) => `Paid ${n(e)} short`,
  },
  crew_talked: {
    sev: 0.8, val: -0.3, crime: 0, town: null, noself: true,
    truth: (e) => `${n(e)} has been talking about what he did for Tom`,
    mine: (e) => `${n(e)} talked`,
  },
};
