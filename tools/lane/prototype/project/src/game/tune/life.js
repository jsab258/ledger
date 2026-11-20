// The numbers of the system "life" (the town's days; DESIGN 2 and 6, A18 to A20): plain data, imports nothing.
export const TUNE = {
  firstDay: { weekday: 0, dayOfMonth: 15, month: 10, year: 1990 }, // Monday 15 October 1990
  marketDayWeekday: 3, // Thursday, in Copper Row: it empties the Hook's shops
  matchWeekday: 5, // Saturday: the street fills at three and five
  matchFillsAtHours: [15, 17],
  sundayWeekday: 6, // shops shut, the chapel busy
  bonfireNight: { dayOfMonth: 5, month: 11 }, // a display on the quay, adults only
  remembranceSunday: { dayOfMonth: 11, month: 11 },
  paperWeekdays: [1, 4], // the paper comes out twice a week: Tuesday and Friday
  // how many of the crowd are out, by hour of the day (share of the crowd's most), dry weather
  crowdShareByHour: [0.03, 0.02, 0.02, 0.02, 0.05, 0.15, 0.35, 0.6, 0.85, 0.9, 0.85, 0.9, 1, 0.9, 0.8, 0.85, 0.95, 1, 0.8, 0.6, 0.45, 0.35, 0.2, 0.08],
  weatherOutShare: { dry: 1, drizzle: 0.75, rain: 0.45, heavy: 0.25, mist: 0.8 },
  marketDayHookShare: 0.6,
  matchHourShare: 1.4,
  sundayShare: 0.55,
  // how long a deed stays hot in talk, by kind (game days); a body never cools; the memory itself is for good
  coolsAfterGameDays: { manners: 1, sighting: 1, debt: 2, damage: 3, theft: 4, violence: 5, weapon: 6, holdup: 7, killing: null },
  // street happenings (A18)
  happeningNotTwiceWithinRealMinutes: 30,
  happeningNotTwiceAWeekOnOneStreet: 7,
  happeningLastsAtMostRealSeconds: 120,
  happeningReturnsAfterGameDays: 3,
  somethingNewAtLeastEveryRealMinutes: 5,
  idleProbeWithinRealSeconds: 30,
  waitShareAtMost: 0.1,
  talkShareAtMost: 0.3,
  drivingShareAtMost: 0.25,
  kinds: { helped: [0.3, 0.5, 0], walked_past: [0.1, -0.1, 0], stepped_in: [0.4, 0.3, 0], body_hidden: [0.9, -1, 3] },
  paperStrengthTimes: 0.8, // what the paper prints is believed a little less than a person
  paperReaders: ['k_news', 'grace', 'sheila', 'pauline', 'brenda', 'sylvia', 'albert', 'nora'],
  missingAskedAfterGameDays: 2,
  bodyFoundAtHour: 6,
  happeningWithinMetres: 9,
  happeningCheckedEveryGameMinutes: 30,
  // street happenings (A18): each written once, placed by a named state and the hour, never by dice
  happenings: [
    { id: 'shoplifter', street: 'Quay Street', needs: ['grocerOpen', 'darrenOut'], fromHour: 9, untilHour: 17, at: [6.4, 10], text: "A lad comes out of Hook Stores fast with his coat held shut, and the grocer behind him shouting.", choices: [['Put a foot out.', 'stepped_in', "Tripped the lad who robbed Hook Stores. The grocer has her tins back and knows who to thank."], ['Let him run.', 'walked_past', 'Watched a lad rob Hook Stores and let him run.']], who: 'k_grocer' },
    { id: 'row', street: 'Chapel Lane', needs: ['evening', 'noraHome'], fromHour: 18, untilHour: 22, at: [-42, -15.5], text: 'A row on a doorstep on Chapel Lane: a man with a rent book, and Nora Cronin with the door half shut on his foot.', choices: [['Stand beside her.', 'stepped_in', "Stood on Nora Cronin's step until the rent man took his foot out of the door."], ['Walk on.', 'walked_past', "Walked past Nora Cronin's row with the rent man."]], who: 'nora' },
    { id: 'van', street: 'the back lane', needs: ['marketDay'], fromHour: 7, untilHour: 11, at: [29.5, 5], text: 'A van broken down across the back lane, bonnet up, the driver looking at the engine as if it owed him money.', choices: [['Give him a push.', 'helped', 'Pushed a broken-down van out of the back lane. The driver said he would not forget it.'], ['Go round.', 'walked_past', 'Left a van stuck across the back lane.']], who: null, returns: 'A van driver he once pushed out of the back lane stops him: there is a constable asking for the cab office at the far end of the street.' },
    { id: 'lostman', street: 'the ferry landing', needs: ['ferryHour'], fromHour: 15, untilHour: 22.5, at: [-44, 55], text: 'A man with a suitcase at the landing, turning a piece of paper round and round. He has an address and no idea.', choices: [['Read it and point him right.', 'helped', 'Set a lost man off the ferry on the right road for Regent House.'], ['Not his business.', 'walked_past', 'Left a lost man standing on the landing.']], who: null, returns: 'The man from the ferry is lodging at Regent House now. He says Mrs Rennison lets the back room to a customs officer, nights.' },
    { id: 'dogloose', street: 'the quay', needs: ['normanOnRow'], fromHour: 19, untilHour: 23, at: [60, 47], text: 'A dog loose on the quay with her lead trailing, pleased with herself.', choices: [['Catch the lead.', 'helped', "Caught a loose dog on the quay. She is Norman Dent's, off the warehouse row."], ['Leave her.', 'walked_past', 'Left a loose dog to the quay.']], who: 'norman' },
    { id: 'lockedout', street: 'Quay Street', needs: ['night', 'sylviaHome'], fromHour: 22, untilHour: 24, at: [5.6, -44], text: 'A woman on the step of Regent House going through her bag for a key that is not in it.', choices: [['Knock Mrs Rennison up for her.', 'helped', 'Knocked Mrs Rennison up for a lodger locked out of Regent House. Mrs Rennison was not grateful; the lodger was.'], ['Walk on.', 'walked_past', 'Left a woman locked out on the step of Regent House.']], who: 'sylvia' },
  ],
  hourBudgetShares: { foot: 0.25, driving: 0.22, talk: 0.19, jobs: 0.17, fights: 0.08, ledger: 0.06, waiting: 0.03 },
};
export const SCHEDULES = {};
export const PEOPLE = {};
