// LEDGER, the whole game: the system "acts". The story's spine (DESIGN 16; parts 3.1.1 to 3.1.3, 2.9.2, 7.4, 7.3):
// Act I, the Inheritance, ends on his answer to Sheila; Act II, the Rise and the Squeeze, fires its beats on states,
// never on days, and ends at a sit-down with one head; Act III, the Ledger Comes Due, is one deciding step each
// morning of the inspection week. Rules: pieces/story.js.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on } from './core.js';
import { G, setPaused } from '../state.js';
import { choose, scene, say, fade } from '../ui.js';
import { advanceTo } from '../work.js';
import { RULES } from '../rules.js';
import { PIECE as STORY } from './pieces/story.js';
import { letter, sign } from './ledgerx.js';
import { townWeekGive, WeekAnswer, townAnswerAsk, NightAnswer } from './town.js';
import { ellisEvent } from './law.js';

const T = RULES.game.acts;
const S_ = STORY.fns;

// What Act II's beats read: the firm, the crew, the rivals, the law and the friendship, as they stand.
function state() {
  const x = X('acts');
  return { cars: G.x.firm.f.cars.length, recruits: Object.values(G.x.crew.men).filter((m) => m.in).length - 6, sheilaTrusts: P_('sheila') && P_('sheila').mind.regard >= 0.2 && G.x.rise.rung >= 2, rivals: G.x.rivals.r, ellisStage: G.x.law.ellis.stage, fireAsked: !!G.ledger.notes.find((n) => n.key === 'firestreet') || !!G.story.flags.alison, friendship: G.x.endings.friend.honestVisits, nightWork: G.x.jobsx ? Object.values(G.x.jobsx.jobs).filter((j) => j.st === 'done').length + (G.story.flags.job1 === 'done' ? 1 : 0) + (G.story.flags.job2 === 'done' ? 1 : 0) : 0, keptArrangement: x.kept, rung: G.x.rise.rung, weeks: x.weeksInAct2 };
}
// ---- Act I ends on his answer (2.9.2): both branches reach Act II ----
async function act1End(choice) {
  const x = X('acts');
  const a = S_.arrangement(choice);
  x.kept = a.kept;
  x.answer = choice;
  townWeekGive(choice === 'take' ? WeekAnswer.TakeOver : choice === 'wind' ? WeekAnswer.WindDown : WeekAnswer.WontSay);
  setPaused(true, 'the end of Act I');
  await fade(true, (choice === 'silent' ? 'You say nothing.\n\nBy Monday dinner time the street has said it for you.' : 'By Monday dinner time the whole of Quay Street knows what you said in that back room.') + '\n\nThe Inheritance is over. What you make of it begins.');
  emit('act.end', { act: 1 });
  x.act = 2;
  x.act2StartDay = dayNow() + 1;
  advanceTo((dayNow() + 1) * 1440 + 8 * 60);
  write(`Told Sheila: ${choice === 'take' ? 'taking it on, all of it' : choice === 'wind' ? 'winding it down, just the cabs' : 'nothing'}. That means ${a.gives}.`, { key: 'act1end', who: 'sheila', how: 'Did it' });
  if (G.hooks.save) G.hooks.save();
  await fade(false);
  setPaused(false, 'Act II has begun');
  G.story.objective = 'The firm is his to grow: the board in the office, the people on the street, and whoever comes asking.';
  emit('act.begin', { act: 2 });
}
// ---- Act II: beats fire on states, never on days (3.1.2) ----
function beats() {
  const x = X('acts');
  const due = S_.beats(state(), x.fired);
  for (const b of due.slice(0, 1)) {
    x.fired.push(b.id);
    x.beatLog.push({ id: b.id, t: Math.round(G.t), week: x.weeksInAct2 });
    tell(b.says, '', 8);
    write(b.says, { key: 'beat:' + b.id, how: 'Saw it himself' });
    if (b.id === 'realBook') write("Mickey's real book: everything he ran, in his own hand. The landing, the doors, who was paid and who paid.", { key: 'realbook', who: 'sheila', how: 'Sheila showed him' });
    if (b.id === 'collision') collision();
    emit('acts.beat', { id: b.id }); // each beat changes the game in the system that owns it (rivals, law, crew, crime, endings)
  }
}
// The one guaranteed collision: an evening of his day life interrupted by his night life at the door.
async function collision() {
  await scene(async () => {
    await say('ada', 'Sit down, the pot is fresh. I was saying to Father Walsh, that lad has turned out steadier than his uncle.');
    await say('ron', 'Boss. Sorry. There is a man at the yard gate who says it will not wait.');
    const i = await choose('', "Ada's cup is halfway to her mouth. Ron is in her doorway with his cap in his hand.", ['Stay. "It will wait, Ron."', 'Go. "I am sorry, Ada."']);
    X('acts').collision = i === 0 ? 'stayed' : 'went';
    emit('acts.collision', { stayed: i === 0 });
    await say('ada', i === 0 ? 'Well. That is the first time anybody from that office has said that in my hearing.' : 'Go on, then. Mickey always went, too.');
  });
  write(`The evening at Ada's, and Ron at the door: ${X('acts').collision === 'stayed' ? 'he stayed' : 'he went'}. Ada saw which.`, { who: 'ada', how: 'Did it', key: 'collision' });
}
// ---- Act III: the inspection week, one deciding step each morning (3.1.3) ----
function act3Begin() {
  const x = X('acts');
  x.act = 3;
  x.insp = { letterT: G.t, startDay: dayNow() + T.act3LetterNoticeGameDays, day: 0, grades: [], inWriting: 0, done: false };
  letter('vat', 'H.M. Customs and Excise', 'Inspection of records: Mickey\'s Cars', `Dear Mr Nowak,\nAn officer of this Department will call at your premises on each of five mornings, beginning the day after tomorrow, to inspect the records of the business under the Value Added Tax Act 1983.\nYou are asked to have the following to hand: ${T.inspectionItems.join('; ')}.\nI am, Sir, your obedient servant.`);
  tell('A buff envelope on the mat at the office, On Her Majesty\'s Service. It is very courteous.', '', 8);
  emit('act.end', { act: 2 });
  emit('act.begin', { act: 3 });
}
async function inspectionMorning() {
  const x = X('acts'),
    I = x.insp;
  const books = { booksOffPence: G.money.booksOff, sheilaTrusts: state().sheilaTrusts, sheilaSaidWhereItHolds: I.sheilaSaid };
  const item = T.inspectionItems[I.day];
  let r;
  await scene(async () => {
    if (books.sheilaTrusts && !I.sheilaSaid && G.money.booksOff > 0) {
      await say('sheila', 'Before he comes. Weeks three and five are where it does not add up. Give him four first. He will tire before he gets back to them.');
      I.sheilaSaid = true;
      books.sheilaSaidWhereItHolds = true;
    }
    await say('The inspector', `Good morning, Mr Nowak. This morning, if you would: ${item}.`);
    const left = T.inWritingAtMost - I.inWriting;
    const i = left > 0 ? await choose('The inspector', 'I can wait while you find it.', ['Produce it.', `Ask for the request in writing (${left === 1 ? 'he will do that once more' : 'he will do that twice'}).`]) : await choose('The inspector', 'You have had it in writing twice, Mr Nowak. This morning I must see it.', ['Produce it.']);
    r = S_.inspect(I.day, books, i === 0 ? 'produce' : 'in writing', I.inWriting);
    await say('The inspector', r.grade === 'put off a day' ? 'In writing. Certainly. You shall have it by the second post.' : r.grade === 'holds' ? 'Thank you. That is in order.' : r.grade === 'questions' ? 'I see. I shall want to look at this page again, Mr Nowak.' : 'These figures are not a record of a taxi business, Mr Nowak. I think you know that.');
  });
  I.steps = (I.steps || []).concat([{ day: I.day, item, grade: r.grade, t: Math.round(G.t) }]);
  if (r.grade === 'put off a day') {
    I.inWriting++;
    I.lastDay = dayNow();
    write(`The inspector asked for ${item}. Asked for it in writing: a day bought.`, { key: 'insp:w' + I.inWriting, how: 'Did it' });
    return;
  }
  I.grades.push(r.grade);
  if (r.sign) sign('inspector', `The inspector: ${r.manner}, over ${item}.`);
  else write(`The inspector looked at ${item}: ${r.manner}.`, { key: 'insp:' + I.day, how: 'Saw it himself' });
  I.day++;
  I.lastDay = dayNow();
  if (r.done) {
    I.done = true;
    I.result = S_.inspectionResult(I.grades);
    x.inspectionDone = true;
    write(`The inspection is over: ${I.result}.`, { key: 'inspresult', how: 'Saw it himself' });
    emit('act.end', { act: 3 });
    emit('acts.inspected', { result: I.result });
  }
}
// Ellis offers a trade in Act III: give her a rival, and the street learns who talks.
async function ellisTrade() {
  const x = X('acts');
  x.tradeOffered = true;
  const i = await scene(async () => {
    await say('ellis', 'You have a week with the Excise in your office, Mr Nowak. I can make my part of it smaller. Tell me about the dock gate.');
    return choose('ellis', 'Nobody need know where I heard it.', ['Give her the Widow.', 'Say nothing.']);
  });
  x.traded = i === 0;
  if (i === 0) {
    G.x.law.ellis.stage = Math.max(0, G.x.law.ellis.stage - 1);
    sign('telling', 'It is said on the quay that Nowak talks to the police.');
  }
  write(i === 0 ? "Gave DS Ellis the Widow's dock gate. The street will learn who talks." : 'DS Ellis offered a trade. Said nothing.', { who: 'ellis', how: 'Did it', key: 'trade' });
}
// Someone in the crew may ask to take it over.
async function successor() {
  const x = X('acts'),
    men = G.x.crew.men;
  const id = ['julie', 'ron'].find((k) => men[k].in && men[k].loyalty >= 0.6);
  if (!id) return;
  x.successorOffered = id;
  const name = RULES.game.crew.men[id].name;
  const i = await scene(async () => {
    await say(id, 'If you ever wanted out, boss. I could keep it going. Just the cabs. I would not ask if I did not mean it.');
    return choose(id, 'Would you let it go?', ['Not yet.', 'Yes. It is yours, when this week is done.']);
  });
  x.handedOver = i === 1 ? id : null;
  sign('successor', `${name} offered to take the firm over.`);
  if (i === 1) write(`Told ${name} the firm is theirs when the week is done.`, { who: id, how: 'Agreed it', key: 'handover' });
}

register({
  id: 'acts',
  fresh: () => ({ act: 1, kept: false, answer: null, act2StartDay: null, weeksInAct2: 0, fired: [], beatLog: [], deadWeeks: [], sitDownDone: false, insp: null, inspectionDone: false, tradeOffered: false, traded: false, successorOffered: null, handedOver: null, collision: null }),
  loaded() {
    G.hooks.act1End = act1End;
  },
  hourly(h, d) {
    const x = X('acts');
    if (x.act === 1) {
      // his answers to the nights' asks reach the real town's own week (the bridge)
      const f = G.story.flags;
      if (f.job1 === 'done') townAnswerAsk(0, NightAnswer.Did);
      else if (f.ask1 === 'no') townAnswerAsk(0, NightAnswer.Refused);
      if (f.job2 === 'done' || f.job3) townAnswerAsk(2, f.job3 === 'noshow' ? NightAnswer.NoShow : NightAnswer.Did);
      else if (f.ask2 === 'no' || f.ask2 === 'tea') townAnswerAsk(2, NightAnswer.Refused);
      return;
    }
    if (x.act === 2) {
      beats();
      const a = S_.act({ answeredSheila: true, weeksInAct2: x.weeksInAct2, sitDownDone: x.sitDownDone, inspectionDone: false });
      if (a === 3 && !G.paused) act3Begin();
    } else if (x.act === 3 && x.insp && !x.insp.done) {
      if (d >= x.insp.startDay && h === 9 && x.insp.lastDay !== d && !G.paused) inspectionMorning();
      if (d >= x.insp.startDay + 1 && h === 14 && !x.tradeOffered && G.x.law.ellis.stage >= 1 && !G.paused) ellisTrade();
      if (d >= x.insp.startDay + 2 && h === 17 && !x.successorOffered && !G.paused) successor();
    }
  },
  daily(d) {
    const x = X('acts');
    if (x.act !== 2 || (d - x.act2StartDay) % 7 !== 0 || d === x.act2StartDay) return;
    const w = x.weeksInAct2;
    const week = { beats: x.beatLog.filter((b) => b.week === w).length, rivalMoves: G.x.rivals.moves.filter((m) => m.t >= (d - 7) * 1440).length, jobs: Object.values(G.x.jobsx.jobs).filter((j) => j.offeredT >= (d - 7) * 1440).length };
    if (S_.deadWeek(week)) x.deadWeeks.push(w); // a week with nothing in it is a fault in the writing (7.4)
    x.weeksInAct2++;
  },
  hook: {
    x: () => X('acts'),
    act: () => X('acts').act,
    state,
    beats,
    act1End,
    act3Begin,
    inspectionMorning,
    ellisTrade,
    successor,
    setAct: (n) => (X('acts').act = n),
  },
});
on('rivals.sitdown', () => {
  X('acts').sitDownDone = true;
});
