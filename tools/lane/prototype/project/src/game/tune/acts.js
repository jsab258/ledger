// The numbers of the system "acts" (the three acts; DESIGN 16): plain data, imports nothing.
export const TUNE = {
  startsOnDayIndex: 0, // Monday 15 October 1990
  askNights: [0, 2, 4, 6], // nights one, three, five and seven
  sheilaAsksOnDayIndex: 6, // Sunday
  act2AtMostGameWeeks: 7,
  act2OpensWhenCars: 3, // the business has grown
  act3InspectionDays: 5,
  act3LetterNoticeGameDays: 2,
  // Act II's beats fire on states, never on days
  beats: [
    { id: 'fleet', when: 'cars >= 3', says: 'Pauline has three cars to call and says so on the air.' },
    { id: 'firstRecruit', when: 'recruits >= 1', says: "A new face behind the counter at Mickey's." },
    { id: 'realBook', when: 'sheilaTrusts', says: "Sheila unlocks the back office and puts Mickey's real book on the desk." },
    { id: 'rivalNoticed', when: 'anyRivalRung >= 1', says: 'Somebody has been asking who runs the firm now.' },
    { id: 'oneCase', when: 'ellisStage >= 2 && fireAsked', says: 'DS Ellis joins the street crimes to the fire: one case.' },
    { id: 'collision', when: 'friendship >= 1 && nightWork >= 3', says: 'An evening of his day life, and his night life at the door.' },
    { id: 'oldFirmFades', when: 'keptArrangement && rung >= 3', says: 'The men behind the landing hand him their end of the Hook, and fade.' },
    { id: 'openGround', when: '!keptArrangement && weeks >= 2', says: 'The ground is open, and all three come sooner.' },
    { id: 'sitDown', when: 'anyRivalRung >= 5', says: 'A sit-down, with one head.' },
  ],
  noDeadWeekNeedsBeatsAtLeast: 1,
  inspectionItems: ['the fare book, weeks one to four', 'the drivers\' wage slips', 'the cars\' log books and receipts', 'the bank paying-in book', 'the fare book, the last three weeks'],
  inWritingAtMost: 2, // asking for the request in writing buys a day, twice and no more
  bookStandsIfOffUnderPence: 2000,
  bookStrainedIfOffUnderPence: 12000,
};
export const SCHEDULES = {};
export const PEOPLE = {};
