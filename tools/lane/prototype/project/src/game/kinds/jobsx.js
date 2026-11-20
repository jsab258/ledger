// New kinds of act of the system "jobsx" (the job template). town: what the real town is told of it.
const n = (e) => e.name || 'someone';
const K = (sev, val, crime, truth, mine, o = {}) => Object.assign({ sev, val, crime, truth, mine }, o);
export const KINDS_ADD = {
  job_word: K(0.4, -0.2, 0, (e) => `Tom gave ${n(e)} his answer about ${e.what || 'a job'}`, (e) => `Gave ${n(e)} my answer about ${e.what || 'the job'}`, { priv: 1, town: 'saw' }),
  hand_over: K(0.6, -0.5, 1, (e) => `Tom handed ${e.what || 'something'} over at ${e.zone}`, (e) => `Handed ${e.what || 'it'} over at ${e.zone}`, { town: 'saw' }),
  took_up: K(0.6, -0.5, 1, (e) => `Tom picked up ${e.what || 'something'} at ${e.zone}`, (e) => `Picked up ${e.what || 'it'} at ${e.zone}`, { town: 'saw' }),
  job_dropped: K(0.4, -0.2, 0, (e) => `Tom never turned up for ${e.what || 'what he said he would do'}`, (e) => `Never turned up for ${e.what || 'it'}`, { noself: true, town: null }),
};
