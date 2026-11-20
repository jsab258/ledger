// The numbers of the system "rivals" (DESIGN 13): plain data, imports nothing.
export const TUNE = {
  ladder: ['unnoticed', 'noticed', 'a visit', 'pressure', 'a threat', 'a sit-down'],
  rivals: {
    widow: { name: 'Maureen Jensen', called: 'the Widow', ground: 'the docks', goesAfter: 'his people', eyes: ['lee', 'kevin'], pressure: 'a tax on his drivers at the dock gate', second: 'his least loyal man poached', taxPencePerWeek: 3000 },
    agar: { name: 'Geoffrey Agar', called: 'Mr Agar', ground: 'old money, lawyers and stamps', goesAfter: 'his clean money', eyes: ['susan'], pressure: "a solicitor's letter over the private-hire licence", second: 'an inspection of the cars', feePence: 9000 },
    cammack: { name: 'Danny Cammack', called: 'Cammack', ground: 'the new crew', goesAfter: 'his cover', eyes: ['rita'], pressure: 'trouble on Quay Street that brings heat he did not earn', second: 'a window of his own put in', damagePence: 4000 },
  },
  climbsOnSightingsAtLeast: 2, // things one of its people saw or heard, per rung
  rungNotSoonerThanGameDays: 2,
  answers: ['pay', 'defy', 'counter with what he knows'],
  fixer: { name: 'Keith Garbutt', readPence: 2000, meetingPence: 5000, trucePence: 20000, truces: 1, truceLastsGameDays: 14 },
  rivalsComeSoonerIfArrangementEndedGameDays: 7,
  sitDown: { underTributePencePerWeek: 6000, underOthersHeldAtRung: 2, warThreatEveryGameDays: 7 },
  beatSightings: { fleet: 'three of his cars are on the air now', openGround: 'the old arrangement is gone and nobody holds his ground', oldFirmFades: 'the men behind the landing have handed him their end' },
};
export const SCHEDULES = {};
export const PEOPLE = {};
