// The numbers and the jobs of the system "jobsx" (the job template and its content; DESIGN 4, A17): plain data.
export const TUNE = {
  windowAtLeastGameHours: 2, // no lateness fail inside a shorter window (ER-JOB-04)
  directionsAtLeast: 2, // sources of direction a step (ER-JOB-02)
  approachesAtLeast: 2, // three keys: at least two scripted ways through (ER-JOB-03)
  ledgerLineWordsAtMost: 30,
  setPieceNotTwiceWithinRealMinutes: 30, // law 6
  minding: { paysPencePerGameHour: 300, countsAfterGameMinutes: 20 },
  stepWithinMetres: 5,
  mindingWithinMetres: 6,
  kinds: { minded: [0.25, -0.1, 0], side_done: [0.3, 0.4, 0], side_bad: [0.3, -0.3, 0] },
};
// Every job is written here once, with a giver, a channel that names a place, at least two approaches (one needing no
// talk, fight or car), and steps that name their place by a landmark with two sources of direction. Never rolled.
// when: a state that offers it (read by game/jobsx.js). pays: [pence, 'tin' | 'pocket'].
const DIR = ['the giver said', 'the Ledger keeps it'];
export const JOBS = [
  { id: 'hut', name: "Iveson's hut", family: 'break-in', giver: 'darren', channel: 'in person', channelPlace: 'the pavement outside the office', when: 'night2', offer: "Iveson keeps it in a tin box in the hut. The lad chains the gap at five. Not that I'm telling you anything.",
    approaches: [{ id: 'the back way before five' }, { id: 'a key', needsTalk: true }, { id: 'force' }],
    takeLine: "Darren's tip: Iveson's tin box, in the hut at the scrap yard.", failLine: "Never went near Iveson's hut. The tip went stale.", refuseLine: 'Told Darren he had heard nothing.',
    steps: [{ id: 'in', place: 'hut', landmark: 'the tarred hut by the weighbridge', directions: DIR, line: "Got into Iveson's hut.", ev: 'crime.entered:hut' }, { id: 'box', place: 'hut', landmark: 'the tin box under the bench', directions: DIR, line: 'The tin box: eighty pounds.', ev: 'crime.found:hut:tinbox' }] },
  { id: 'ritaback', name: "Rita's back room", family: 'break-in', giver: 'wayne', channel: 'a man waiting by the car', channelPlace: "the rank outside Mickey's", when: 'wayneOwes', offer: "There's a clock on the back shelf she has not written down. Side door is on the latch till six. We split it.",
    approaches: [{ id: 'the side door before six' }, { id: 'a key from Wayne', needsTalk: true }, { id: 'force' }],
    takeLine: "Wayne's offer: the clock off Rita's back shelf, and a split.", failLine: "Left Rita's back room alone.", refuseLine: 'Told Wayne no.',
    steps: [{ id: 'in', place: 'ritaside', landmark: 'the green door in the lane behind the pawn shop', directions: DIR, line: "In at Rita's side door.", ev: 'crime.entered:rita' }, { id: 'clock', place: 'rita', landmark: 'the back shelf', directions: DIR, line: 'The carriage clock, off the back shelf.', ev: 'crime.found:rita:shelf' }] },
  { id: 'tail_susan', name: 'where Miss Coverdale goes', family: 'tail', giver: 'sheila', channel: 'a message', channelPlace: 'the office counter', when: 'rung2', offer: 'Somebody at the Harbour Office is writing letters about our licence. I would like to know who she takes them to.',
    approaches: [{ id: 'on foot from the Harbour Office' }, { id: 'by cab', needsCar: true }],
    takeLine: 'Sheila wants to know who Susan Coverdale takes her letters to.', failLine: 'Never followed Miss Coverdale.', refuseLine: 'Told Sheila it was not his business.',
    steps: [{ id: 'follow', place: 'harbour', landmark: 'the stone office with the clock over the door, at half past four', directions: DIR, line: "Followed Susan Coverdale from the Harbour Office to the solicitor's door on Copper Row: Agar's.", ev: 'foot.tail:susan:arrived', tail: { id: 'susan', learns: "to the solicitor's on Copper Row" } }] },
  { id: 'mind_julie', name: "standing at Julie Kettlewell's door", family: 'minding', giver: 'julie', channel: 'in person', channelPlace: 'Chapel Lane', when: 'julieFriend', offer: 'The rent man comes at six and he does not come alone. Would you just stand there. You need not say anything.',
    approaches: [{ id: 'stand at her door' }, { id: 'sit in the cab outside', needsCar: true }],
    takeLine: "Julie Kettlewell wants somebody stood at her door at six, when the rent man comes.", failLine: 'Julie faced the rent man on her own.', refuseLine: 'Told Julie he could not.',
    steps: [{ id: 'stand', place: 'unit', landmark: "Julie's door on Chapel Lane, the one with the blue step", directions: DIR, line: "Stood at Julie Kettlewell's door while the rent man came and went. He looked, and said nothing.", mind: { minutes: 20, with: 'julie' }, window: { fromHour: 17.5, untilHour: 20 } }] },
  { id: 'mind_ron', name: 'the door at the boxing club', family: 'minding', giver: 'ron', channel: 'in person', channelPlace: 'the rank', when: 'rung2', offer: "The club's got a show on Saturday. They want a face on the door who is not from the docks.",
    approaches: [{ id: 'stand on the door' }, { id: 'send Ron', needsTalk: true }],
    takeLine: 'Ron: the boxing club wants a face on the door on Saturday.', failLine: 'Nobody from Mickey\'s was on the club door.', refuseLine: 'Told Ron the club could mind its own door.',
    steps: [{ id: 'stand', place: 'boxing', landmark: "the hall behind the chandler's, a bare bulb over the door", directions: DIR, line: 'Stood the door at the boxing club. People saw who stood there.', mind: { minutes: 30, with: 'ron' }, window: { fromHour: 17, untilHour: 22 } }] },
  { id: 'lift_coin', name: "the tray in Metcalfe's window", family: 'lift', giver: 'wayne', channel: 'in person', channelPlace: "Rita's back room", when: 'fencedOnce', offer: "Metcalfe leaves a tray of medals in the window overnight. Rita would take them, if she did not know whose they were.",
    approaches: [{ id: 'the window, at night', needsFight: false }, { id: 'the back door in the alley' }],
    takeLine: "Wayne says Metcalfe leaves a tray of medals in his window overnight.", failLine: "Left Metcalfe's medals where they were.", refuseLine: 'Told Wayne he was not a window man.',
    steps: [{ id: 'take', place: 'coin', landmark: 'the coin shop that sells no coins, the window by the door', directions: DIR, line: "Put Metcalfe's window in and took the tray of medals. Hal Metcalfe never forgets his own goods.", ev: 'crime.damage:coinwin', goods: { id: 'medals', name: 'a tray of medals', honestPence: 9000, owner: 'hal' } }] },
  { id: 'damage_portside', name: "a word to Portside Cars", family: 'damage', giver: 'ron', channel: 'in person', channelPlace: 'the rank', when: 'otherFirmTaking', offer: "Portside are sat on the north rank taking our fares. One windscreen, at night, and they will read it right.",
    approaches: [{ id: 'by hand, at night' }, { id: 'send a man', needsTalk: true }],
    takeLine: "Ron: one Portside windscreen, at night, as a message.", failLine: 'Portside kept the north rank and their windscreens.', refuseLine: 'Told Ron no windows.',
    steps: [{ id: 'do', place: 'northrank', landmark: 'the lay-by under the station clock', directions: DIR, line: "Put a Portside windscreen in on the north rank. Len Wardle will know who by morning.", ev: 'crime.damage:portside' }] },
  // side stories (3.3): found on foot, no markers, each ends in something the town knows
  { id: 'side_ada_cat', name: "Ada's lamp", family: 'side', giver: 'ada', channel: 'in person', channelPlace: 'her step', when: 'adaTea', offer: 'The lamp on my landing has gone and I cannot reach it. Mickey used to do it.',
    approaches: [{ id: 'buy a bulb and fit it' }, { id: 'send Darren', needsTalk: true }],
    takeLine: "Ada's landing lamp has gone. Mickey used to see to it.", failLine: "Ada's landing stayed dark.", refuseLine: 'Told Ada he was no electrician.',
    steps: [{ id: 'fit', place: 'ada', landmark: "Ada's, the window opposite Mickey's", directions: DIR, line: "Fitted Ada's landing lamp. She watched from the foot of the stairs and said nothing, which from Ada is thanks.", good: true, visit: 'ada' }] },
  { id: 'side_walsh_roof', name: "the chapel's lead", family: 'side', giver: 'walsh', channel: 'in person', channelPlace: 'the bench by the chapel', when: 'metWalsh', offer: 'Somebody has had the lead off the vestry roof. I would sooner have it back than have the police in.',
    approaches: [{ id: "ask at Iveson's yard", needsTalk: true }, { id: 'look in the yard at night' }],
    takeLine: "Father Walsh has lost the lead off the vestry roof and would sooner have it back than have the police in.", failLine: "The chapel's lead was never found.", refuseLine: 'Told Father Walsh he could not help.',
    steps: [{ id: 'find', place: 'scrap', landmark: 'the scrap yard with the crane and the dog', directions: DIR, line: "Found the chapel's lead in Iveson's yard, under a tarpaulin.", near: true }, { id: 'back', place: 'chapel', landmark: 'the chapel with the green door', directions: DIR, line: 'Told Father Walsh where his lead is. What he does with it is his.', good: true, near: true }] },
  { id: 'side_grace_till', name: "Grace's short till", family: 'side', giver: 'grace', channel: 'in person', channelPlace: "Rinaldi's counter", when: 'metGrace', offer: 'My till is a pound short every Thursday and I have one girl on a Thursday. I do not want to be right.',
    approaches: [{ id: 'sit and watch on a Thursday' }, { id: 'ask the girl', needsTalk: true }],
    takeLine: "Grace Rinaldi's till is a pound short every Thursday.", failLine: "Grace never found out about her till.", refuseLine: 'Told Grace to count it herself.',
    steps: [{ id: 'watch', place: 'caff', landmark: "the caff on the corner of Chapel Lane", directions: DIR, line: "Sat in Rinaldi's on a Thursday and watched the till. It is the delivery man, not the girl.", good: true, mind: { minutes: 20, with: 'grace' } }] },
  { id: 'side_norman_dog', name: "Norman's dog", family: 'side', giver: 'norman', channel: 'in person', channelPlace: 'the warehouse row', when: 'metNorman', offer: 'My dog has slipped her lead and gone along the quay. I cannot leave the row.',
    approaches: [{ id: 'walk the quay and bring her back' }, { id: 'drive the quay', needsCar: true }],
    takeLine: "Norman Dent's dog is loose on the quay and he cannot leave the row.", failLine: "Norman's dog came home on her own, in the end.", refuseLine: 'Told Norman he had no time for dogs.',
    steps: [{ id: 'find', place: 'fishdock', landmark: 'the stacked fish boxes and the ice hut', directions: DIR, line: "Found Norman's dog at the fish boxes, eating what she should not.", near: true }, { id: 'back', place: 'row', landmark: 'the brick warehouses, numbers painted on the doors', directions: DIR, line: "Walked Norman Dent's dog back to the row. He owes him a turn now, and knows it.", good: true, near: true }] },
];
export const SCHEDULES = {};
export const PEOPLE = {};
