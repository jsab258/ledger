// New kinds of act of the system "cars". town: what the real town is told of it.
const n = (e) => e.name || 'somebody';
export const KINDS_ADD = {
  hit_helped: { sev: 0.55, val: 0.2, crime: 0, town: 'open', truth: (e) => `Tom stopped and saw to ${n(e)} after his cab knocked them down on ${e.zone}`, mine: (e) => `Stopped and saw to ${n(e)} after the cab knocked them down` },
  hit_run: { sev: 0.85, val: -0.8, crime: 2, town: 'saw', loud: 1, grudge: 1, truth: (e) => `A Mickey's cab knocked ${n(e)} down on ${e.zone} and never stopped`, mine: (e) => `Knocked ${n(e)} down with the cab and drove off` },
  car_aimed: { sev: 0.9, val: -0.9, crime: 2, town: 'saw', loud: 1, grudge: 1, truth: (e) => `Tom drove his cab at ${n(e)} on ${e.zone}`, mine: (e) => `Drove the cab at ${n(e)}` },
  car_dead: { sev: 0.35, val: -0.1, crime: 0, town: 'open', loud: 1, truth: (e) => `Tom wrecked one of Mickey's cabs on ${e.zone} and walked home`, mine: (e) => `Wrecked the cab on ${e.zone}` },
  car_taken: { sev: 0.6, val: -0.5, crime: 1, town: 'deed', loud: 1, truth: (e) => `Somebody broke into ${e.name || 'a parked car'} on ${e.zone} and drove it away`, mine: (e) => `Broke into ${e.name || 'a parked car'} on ${e.zone} and took it` },
  horn_night: { sev: 0.15, val: -0.05, crime: 0, town: null, loud: 1, noself: true, truth: (e) => `A car horn went on ${e.zone} in the night`, mine: (e) => `Sounded the horn on ${e.zone} at night` },
  stop_taken: { sev: 0.3, val: -0.1, crime: 0, town: 'open', truth: (e) => `The police pulled one of Mickey's cabs over on ${e.zone}`, mine: (e) => `Was pulled over by the patrol car on ${e.zone}` },
  stop_refused: { sev: 0.6, val: -0.4, crime: 1, town: 'saw', loud: 1, truth: (e) => `One of Mickey's cabs would not stop for the police on ${e.zone}`, mine: (e) => `Drove off from the patrol car on ${e.zone}` },
  car_rammed: { sev: 0.55, val: -0.4, crime: 1, town: 'deed', loud: 1, truth: (e) => `Tom rammed ${e.name || 'a car'} with the cab on ${e.zone}`, mine: (e) => `Rammed ${e.name || 'a car'} with the cab` },
  car_repaint: { sev: 0.2, val: -0.1, crime: 0, town: null, truth: () => "One of Mickey's cars went into Hewson's shed and came out another colour", mine: () => 'Had Shaun Hewson repaint the car' },
};
