// The numbers of the system "crew" (DESIGN 12, A16, A40): plain data, imports nothing.
export const TUNE = {
  orders: ['with me', 'wait here', 'watch that', 'fetch him', 'take this there', 'drive', 'lean on him'],
  orderInputsAtMost: 2,
  orderAnsweredWithinRealSeconds: 1,
  followsAtMetres: 2,
  lagsAtMostRealSeconds: 10,
  // the eight sent verbs of Act II (D56), in his order
  verbs: ['have a man hurt', 'point a plan at a person', 'frame someone', 'lean on a witness', 'move or hide a body', 'dock, expel or beat one of his own', 'send men at a rival property', 'have someone vouch for him'],
  verbsCannotBeUndone: ['have a man hurt', 'move or hide a body', 'frame someone'],
  // who the crew are: nerve and the loyalty ceiling, and what each brings
  men: {
    ron: { name: 'Ron Kirby', inherited: true, nerve: 0.8, loyaltyCeiling: 0.95, loyalty: 0.7, use: 'the door and the rank' },
    sheila: { name: 'Sheila Dunn', inherited: true, nerve: 0.7, loyaltyCeiling: 0.9, loyalty: 0.5, use: 'the book' },
    pauline: { name: 'Pauline Kitching', inherited: true, nerve: 0.5, loyaltyCeiling: 0.8, loyalty: 0.6, use: 'the radio' },
    kevin: { name: 'Kevin Needham', inherited: true, nerve: 0.4, loyaltyCeiling: 0.6, loyalty: 0.45, use: 'the day car' },
    terry: { name: 'Terry Hodgson', inherited: true, nerve: 0.55, loyaltyCeiling: 0.75, loyalty: 0.55, use: 'the night car' },
    darren: { name: 'Darren Milner', inherited: true, nerve: 0.3, loyaltyCeiling: 0.6, loyalty: 0.4, use: 'messages, and what he hears' },
    julie: { name: 'Julie Kettlewell', road: 'need', need: 'work', nerve: 0.5, loyaltyCeiling: 0.9, loyalty: 0.6, use: 'a third driver' },
    ian: { name: 'Ian Megginson', road: 'need', need: 'his shop rent', nerve: 0.45, loyaltyCeiling: 0.8, loyalty: 0.5, use: 'every lock on the street' },
    lee: { name: 'Lee Drewery', road: 'hook', hook: 'the debt he owes', nerve: 0.75, loyaltyCeiling: 0.55, loyalty: 0.35, use: 'his fists' },
    norman: { name: 'Norman Dent', road: 'need', need: 'company on the night watch', nerve: 0.35, loyaltyCeiling: 0.7, loyalty: 0.45, use: 'his nights on the warehouse row' },
    karen: { name: 'Karen Grummitt', road: 'hook', hook: 'what he saw at the ferry', nerve: 0.4, loyaltyCeiling: 0.5, loyalty: 0.3, use: 'her view of the ferry' },
    shaun: { name: 'Shaun Hewson', road: 'need', need: 'paid work', nerve: 0.45, loyaltyCeiling: 0.75, loyalty: 0.5, use: 'paint for a cab that should not look like a cab' },
  },
  needRoadLoyaltyStart: 0.6,
  hookRoadLoyaltyStart: 0.3,
  hookRoadLoyaltyCeiling: 0.55,
  // breaking: the load on a man against his nerve; the sign always comes first
  loadPerThingHeKnows: 0.12,
  loadWhenFrightened: 0.25,
  loadWhenArrested: 0.3,
  loadEasedByLoyalty: 0.4,
  signAtShareOfNerve: 0.75,
  signs: ['he looks away', 'he asks for his cut early', 'he is not at his post'],
  fates: ['holds', 'poached', 'frightened off', 'arrested', 'talks to a rival', 'talks to the police', 'killed'],
};
export const SCHEDULES = {};
export const PEOPLE = {};
