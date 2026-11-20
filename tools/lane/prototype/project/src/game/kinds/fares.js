// New kinds of act of the system "fares". town: what the real town is told of it.
const n = (e) => e.name || 'a fare';
export const KINDS_ADD = {
  fare_parcel: { sev: 0.45, val: -0.35, crime: 1, town: 'saw', truth: (e) => `One of Mickey's cabs left a parcel at ${e.dest || 'a side door'}, no questions`, mine: (e) => `Left a fare's parcel at ${e.dest || 'a side door'}` },
  fare_wait: { sev: 0.4, val: -0.3, crime: 0, town: 'saw', truth: (e) => `One of Mickey's cabs sat waiting on ${e.zone} with its engine running`, mine: (e) => `Sat waiting for a fare on ${e.zone}, engine running` },
  fare_collared: { sev: 0.45, val: -0.2, crime: 0, town: 'saw', truth: (e) => `Tom ran ${n(e)} down on foot for a cab fare on ${e.zone}`, mine: (e) => `Ran ${n(e)} down for the fare on ${e.zone}` },
  fare_late: { sev: 0.3, val: -0.15, crime: 0, town: 'open', truth: (e) => `Tom promised ${n(e)} and got them there late`, mine: (e) => `Promised ${n(e)} and was late` },
  fare_kept_word: { sev: 0.25, val: 0.25, crime: 0, town: 'open', truth: (e) => `Tom said he would get ${n(e)} there, and did`, mine: (e) => `Got ${n(e)} there as promised` },
  fare_handed: { sev: 0.1, val: 0, crime: 0, town: null, noself: true, truth: () => 'Tom gave a fare to one of his drivers', mine: () => 'Gave a fare to a driver' },
  tail_made: { sev: 0.5, val: -0.3, crime: 0, town: 'saw', truth: (e) => `One of Mickey's cabs followed ${e.name || 'a van'} across the Hook and was seen doing it`, mine: (e) => `Followed ${e.name || 'a van'} in the cab and was made` },
};
