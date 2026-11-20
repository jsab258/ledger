// RULE PIECE: the story's spine (DESIGN 16, A7). Pure. Unreal ports it and passes test/cases/story.json.
// Act II's beats fire on states, never on days. Act III is one deciding step each morning, graded by what the
// books hold. The endings are states, never picked from a list; every cost that decides the ending shows its
// sign before it decides, and no ending lands while Tom's own reading says things are quiet.
import { TUNE as A } from '../tune/acts.js';
import { TUNE as E } from '../tune/endings.js';

// Which act it is. s: { answeredSheila, cars, weeks, sitDownDone, inspectionDone }
const act = (s) => (!s.answeredSheila ? 1 : s.inspectionDone ? 4 : s.sitDownDone || s.weeksInAct2 >= A.act2AtMostGameWeeks ? 3 : 2);
// Act II's beats: every beat whose state holds and has not fired, in the written order.
function beats(s, fired) {
  const anyRivalRung = Math.max(0, ...Object.values(s.rivals || {}).map((r) => r.rung || 0));
  const env = Object.assign({ cars: 2, recruits: 0, sheilaTrusts: false, ellisStage: 0, fireAsked: false, friendship: 0, nightWork: 0, keptArrangement: false, rung: 1, weeks: 0 }, s, { anyRivalRung });
  const holds = (expr) => expr.split('&&').every((c) => {
    const m = /^\s*(!?)(\w+)\s*(>=)?\s*(\d+)?\s*$/.exec(c);
    const v = env[m[2]];
    return m[3] ? v >= +m[4] : m[1] ? !v : !!v;
  });
  return A.beats.filter((b) => !fired.includes(b.id) && holds(b.when)).map((b) => ({ id: b.id, says: b.says }));
}
// No dead weeks (7.4): a week of Act II with no beat, no rival move and no job is flagged for the writing.
const deadWeek = (w) => (w.beats || 0) + (w.rivalMoves || 0) + (w.jobs || 0) < A.noDeadWeekNeedsBeatsAtLeast;
// Act III: one item each morning. He produces it or asks for it in writing. Graded by what the books hold.
function inspect(day, books, choice, inWritingUsed = 0) {
  const item = A.inspectionItems[day];
  if (item === undefined) return { item: null, grade: null, done: true };
  const off = books.booksOffPence || 0;
  const state = off < A.bookStandsIfOffUnderPence ? 'stands' : off < A.bookStrainedIfOffUnderPence ? 'strained' : 'does not stand';
  // asking in writing buys a day, twice in the week and no more: after that he must produce it (the stall the depth check found)
  if (choice === 'in writing' && inWritingUsed < A.inWritingAtMost) return { item, grade: 'put off a day', manner: 'he writes it down, courteous', sign: null, done: false, inWritingLeft: A.inWritingAtMost - inWritingUsed - 1 };
  const lieHeld = books.sheilaTrusts && books.sheilaSaidWhereItHolds && state === 'strained';
  const grade = state === 'stands' || lieHeld ? 'holds' : state === 'strained' ? 'questions' : 'fails';
  return { item, grade, manner: grade === 'holds' ? 'he nods and turns the page' : grade === 'questions' ? 'he reads the same line twice' : 'he stops being courteous', sign: grade === 'holds' ? null : E.signs.inspector, done: day >= A.inspectionItems.length - 1 };
}
const inspectionResult = (grades) => (grades.filter((g) => g === 'fails').length >= 2 || grades.filter((g) => g !== 'holds').length >= 4 ? 'the books do not hold' : 'the books hold');
// The ending, as a state. s: { business (the firm stands at the close), booksHold, friendHolds, streetHoldsRackets,
// hunted (a manhunt for a killing), handedOver (to someone who can keep it), charged }
function ending(s) {
  const business = !!s.business && !!s.booksHold && !s.hunted;
  let built, shown, turn;
  if (business && s.under) [built, shown, turn] = ['Kingdom', 'The Kingdom', 'under another man'];
  else if (business && s.friendHolds && !s.streetHoldsRackets) [built, shown, turn] = ['Both', 'The Kingdom', 'at its best'];
  else if (business) [built, shown, turn] = ['Kingdom', 'The Kingdom', 'at its plainest'];
  else if (s.friendHolds && s.handedOver && !s.hunted) [built, shown, turn] = ['Quiet', 'The Straight Life', 'at its best'];
  else if (s.friendHolds && !s.hunted) [built, shown, turn] = ['Straight', 'The Straight Life', 'at its plainest'];
  else [built, shown, turn] = ['Burn', 'Burn Both', s.hunted ? 'hunted' : 'what doing nothing produces'];
  return { built, shown, turn, close: closeLine(shown, turn, s) };
}
const closeLine = (shown, turn, s) => (shown === 'The Kingdom' && turn === 'under another man' ? 'The cabs go out at six, and every Friday an envelope goes up the hill. It is his name over the door.' : shown === 'The Kingdom' ? (turn === 'at its best' ? 'The cabs go out at six. One friend still counts him, and the street says "Tom".' : 'The cabs go out at six. People are civil, and no more.') : shown === 'The Straight Life' ? (turn === 'at its best' ? "Somebody else's name goes over the door. He walks to the ferry with one suitcase, clean." : 'The office is shut. One person still asks him in for tea.') : s.hunted ? 'A car on the street and his description. The office door stands open.' : 'The sign comes down. Nobody on Quay Street says his name.');
// The signs he has been shown, and Tom's reading built only from them (6.2.5, ER-END-02).
function reading(signs) {
  const lines = [];
  const has = (k) => signs.includes(k);
  const books = has('inspector') || has('sheila');
  const law = has('ellis') || has('police');
  lines.push(books ? 'The books: they will not stand as they are.' : 'The books: nobody has said a word against them.');
  lines.push(has('friend') ? 'One friend still counts him.' : has('telling') ? 'The street says it as fact now.' : 'Nobody has come to him unasked.');
  lines.push(law ? 'The law: they are past asking.' : 'The law: quiet.');
  if (has('successor')) lines.push('Somebody would take it over, if he let go.');
  const quiet = !books && !law && !has('telling');
  return { lines, quiet, expects: books && law ? 'Burn Both' : books ? (has('friend') ? 'The Straight Life' : 'Burn Both') : 'The Kingdom' };
}
// ER-END-02: an ending that costs him may land only if its signs were shown; else the sign is owed first.
function mayLand(end, signsShown) {
  const need = [];
  if (end.shown !== 'The Kingdom') need.push(['inspector', 'sheila', 'ellis', 'police', 'successor'].some((k) => signsShown.includes(k)) ? null : 'inspector');
  if (end.turn === 'hunted' && !signsShown.includes('police')) need.push('police');
  const owed = need.filter(Boolean);
  return { may: owed.length === 0, owed: owed.map((k) => E.signs[k]) };
}
// After the ending (A7): the close, the credits, then control in the town as it stands, or quit to the title.
const after = (end) => ({ close: end.close, credits: true, creditsSeconds: E.creditsRealSeconds, controlWithinSeconds: E.controlAfterCreditsWithinRealSeconds, place: end.shown === 'The Straight Life' ? 'the ferry landing' : "outside Mickey's", newMainBeats: false, newGamePlus: false, ledgerLastPage: 'The story is told. The town goes on.' });
// The asks of Act I fall on nights one, three, five and seven; rent on Friday; Sheila's question on Sunday.
const week1 = (dayIndex) => ({ askTonight: A.askNights.includes(dayIndex), rentDue: dayIndex === 4, sheilaAsks: dayIndex === A.sheilaAsksOnDayIndex });
// Keeping or ending the arrangement (2.9.2): both branches reach Act II.
const arrangement = (answer) => (answer === 'take' ? { kept: true, act2: true, gives: 'night money, cover and asks that grow' } : answer === 'wind' ? { kept: false, act2: true, gives: 'freedom without cover; the rivals come sooner' } : { kept: false, act2: true, gives: 'the street says it for him' });
export const PIECE = { name: 'story', fns: { act, beats, deadWeek, inspect, inspectionResult, ending, reading, mayLand, after, week1, arrangement } };
