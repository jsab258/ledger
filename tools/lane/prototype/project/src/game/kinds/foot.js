// New kinds of act of the system "foot": street manners, noises made on purpose, things thrown in the water,
// trespass, a vault, marks seen. Fields as kinds.js.
const n = (e) => e.name || 'someone';
export const KINDS_ADD = {
  nod: { sev: 0.05, val: 0.1, crime: 0, town: 'open', truth: (e) => `Tom Nowak nodded to ${n(e)}`, mine: (e) => `Nodded to ${n(e)}` },
  greeting: { sev: 0.08, val: 0.2, crime: 0, town: 'open', truth: (e) => `Tom Nowak said good day to ${n(e)}`, mine: (e) => `Said good day to ${n(e)}` },
  hard_look: { sev: 0.25, val: -0.3, crime: 0, town: 'saw', truth: (e) => `Tom Nowak gave ${n(e)} a hard look`, mine: (e) => `Gave ${n(e)} a hard look` },
  street_shove: { sev: 0.45, val: -0.5, crime: 1, town: 'saw', truth: (e) => `Tom Nowak shoved ${n(e)} in the street`, mine: (e) => `Shoved ${n(e)}` },
  called_out: { sev: 0.15, val: -0.05, crime: 0, loud: 1, town: 'open', truth: (e) => `Tom Nowak shouted after ${n(e)}`, mine: (e) => `Called out to stop ${n(e)}` },
  noise_made: { sev: 0.2, val: -0.1, crime: 0, loud: 1, noself: true, town: null, truth: () => 'There was a noise in the street and nobody by it', mine: () => 'Made a noise to turn a head' },
  threw_in: { sev: 0.4, val: -0.35, crime: 1, town: 'saw', truth: (e) => `Tom Nowak threw ${e.thing || 'something'} into the water`, mine: (e) => `Threw ${e.thing || 'something'} into the water. It is gone` },
  trespass: { sev: 0.45, val: -0.4, crime: 1, town: 'saw', truth: (e) => `Tom Nowak was where he had no business, at ${e.place || 'a private place'}`, mine: (e) => `Was told off ${e.place || 'private ground'} and stayed` },
  sat_about: { sev: 0.03, val: 0.05, crime: 0, noself: true, town: 'open', truth: () => 'Tom Nowak sat a while in the street', mine: () => 'Sat a while' },
  marked_face: { sev: 0.3, val: -0.2, crime: 0, noself: true, town: 'saw', truth: () => 'Tom Nowak is going about with a bruised face', mine: () => 'His bruises were seen' },
  collared: { sev: 0.4, val: -0.35, crime: 1, town: 'saw', truth: (e) => `Tom Nowak ran ${n(e)} down and took him by the collar`, mine: (e) => `Ran ${n(e)} down and collared him` },
  doctor_visit: { sev: 0.2, val: 0, crime: 0, priv: 1, town: null, truth: () => 'Tom Nowak was stitched by the old doctor on the quay', mine: () => 'Stitched by the old doctor on the quay, for money. He does not ask' },
};
