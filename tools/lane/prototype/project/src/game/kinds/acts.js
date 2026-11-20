// New kinds of act of the system "acts". Each: { sev, val, crime, truth: (E) => words, mine: (E) => words, town }.
// sev 0..1 newsworthy, val -1 menace..1 decent, crime 0..3. town: what the real town is told of it.
const head = (e) => e.head || 'one of the three';
export const KINDS_ADD = {
  sitdown_accept: { sev: 0.8, val: -0.2, crime: 0, town: 'open', truth: (e) => `Tom Nowak sat down with ${head(e)} and took the terms`, mine: (e) => `Sat down with ${head(e)} and took the terms` },
  sitdown_defy: { sev: 0.85, val: -0.3, crime: 0, town: 'open', truth: (e) => `Tom Nowak sat down with ${head(e)} and told them no`, mine: (e) => `Sat down with ${head(e)} and said no` },
  sitdown_counter: { sev: 0.85, val: -0.5, crime: 0, town: 'saw', truth: (e) => `Tom Nowak sat down with ${head(e)} and named what he knows about them`, mine: (e) => `Sat down with ${head(e)} and put what he knows on the seat between them` },
  traded_rival: { sev: 0.9, val: -0.6, crime: 0, town: 'open', truth: (e) => `Tom Nowak gave ${head(e)} to DS Ellis`, mine: (e) => `Gave ${head(e)} to DS Ellis. The street will learn who talks` },
  handed_over: { sev: 0.7, val: 0.3, crime: 0, town: 'open', truth: (e) => `Tom Nowak handed Mickey's over to ${e.name || 'one of his own'}`, mine: (e) => `Handed the firm over to ${e.name || 'one of his own'}` },
  collision_went: { sev: 0.5, val: -0.3, crime: 0, town: 'open', truth: (e) => `Tom Nowak got up from ${e.name || "a friend's"} table and went out with Ron Kirby`, mine: () => "Left a friend's table for the night's business" },
  collision_stayed: { sev: 0.4, val: 0.3, crime: 0, town: 'open', truth: (e) => `Tom Nowak sent Ron Kirby away from ${e.name || "a friend's"} door and stayed`, mine: () => "Stayed at a friend's table and let the night's business go" },
  inspected: { sev: 0.6, val: 0, crime: 0, town: 'open', truth: () => "A Customs and Excise inspector is going through the books at Mickey's", mine: () => 'The VAT inspector has started on the books' },
};
