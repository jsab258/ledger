// New kinds of act of the system "life" (happenings, side stories, calls, pastimes). town: what the real town is told.
const n = (e) => e.name || 'somebody';
export const KINDS_ADD = {
  good_turn: { sev: 0.45, val: 0.5, crime: 0, town: 'open', truth: (e) => `Tom ${e.what || 'did somebody a good turn'} on ${e.zone}`, mine: (e) => `${cap(e.what || 'did somebody a good turn')} on ${e.zone}` },
  looked_away: { sev: 0.25, val: -0.2, crime: 0, town: 'open', truth: (e) => `Tom ${e.what || 'walked past somebody who wanted help'} on ${e.zone}`, mine: (e) => `${cap(e.what || 'walked past somebody who wanted help')} on ${e.zone}` },
  hard_word: { sev: 0.35, val: -0.35, crime: 0, town: 'open', truth: (e) => `Tom ${e.what || 'spoke hard to a man'} on ${e.zone}`, mine: (e) => `${cap(e.what || 'spoke hard to a man')} on ${e.zone}` },
  forced_for: { sev: 0.45, val: 0.1, crime: 0, loud: 1, town: 'open', truth: (e) => `Tom put his shoulder to a door on ${e.zone} for a woman locked out`, mine: (e) => `Forced a door on ${e.zone} for a woman locked out. It was loud` },
  visit: { sev: 0.2, val: 0.2, crime: 0, town: 'open', truth: (e) => `Tom called on ${n(e)}`, mine: (e) => `Called on ${n(e)}` },
  visit_lie: { sev: 0.3, val: -0.3, crime: 0, town: null, priv: 1, truth: (e) => `Tom told ${n(e)} less than the truth`, mine: (e) => `Told ${n(e)} less than the truth` },
  spar: { sev: 0.3, val: 0.15, crime: 0, town: 'open', truth: () => 'Tom sparred three rounds with the gloves on at the boxing club', mine: () => 'Three rounds with the gloves on at the boxing club' },
  story_end: { sev: 0.4, val: 0.3, crime: 0, town: 'open', truth: (e) => `Tom ${e.what || 'saw a small thing through'}`, mine: (e) => cap(e.what || 'saw a small thing through') },
  story_grey: { sev: 0.4, val: -0.25, crime: 0, town: 'saw', truth: (e) => `Tom ${e.what || 'kept something that was not his'}`, mine: (e) => cap(e.what || 'kept something that was not his') },
};
function cap(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
