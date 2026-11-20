// RULE PIECE: the law (DESIGN 8, A12, A13, A22, A36, A37). Pure. Unreal ports it and passes test/cases/law.json.
// A pressure he can read and answer, never the end of the game. The real town code decides who goes to the police
// over the week's damage; this piece holds what the design adds around it.
import { TUNE as T } from '../tune/law.js';

// ER-POL-01: no arrest without a named statement or an officer who saw it; never twice for one deed.
function mayArrest(deed) {
  if (deed.takenFor) return { may: false, why: 'never taken twice for one deed' };
  if (deed.officerSaw) return { may: true, why: 'an officer saw it' };
  if ((deed.statements || []).some((s) => s.namesHim && s.signed)) return { may: true, why: 'a signed statement names him' };
  return { may: false, why: 'talk alone brings questions, never an arrest' };
}
// What an arrest costs: game hours by the offence, a caution or a charge; never the game.
function custody(offence, s = {}) {
  const key = offence === 'damage' && s.ownedUp ? 'damageOwnedUp' : offence;
  const hours = T.custodyGameHours[key] ?? T.custodyGameHours.damage;
  const ends = offence === 'damage' && (s.ownedUp || s.first) ? 'cautioned' : offence === 'killing' ? 'charged, bail' : 'charged';
  return { gameHours: hours, ends, coatKept: !!s.woreCoat, solicitor: 'the duty solicitor, free', gameOver: false, joinsEllisCase: ends !== 'cautioned' };
}
// DS Ellis's four stages. No stage is skipped unseen (ER-POL-05): the file moves one stage at a time and each
// stage's sign must have been shown before the next can begin. file: { stage, signShown, signShownT }
function ellis(file, ev, t) {
  const f = Object.assign({ stage: 0, signShown: true, signShownT: null }, file);
  if (ev.what === 'sign shown') return Object.assign(f, { signShown: true, signShownT: t });
  const wants = ev.what === 'talk' ? 1 : ev.what === 'detective crime reported' || ev.what === 'body' ? 2 : ev.what === 'witnessed killing' || ev.what === 'charge' ? 3 : f.stage;
  if (wants > f.stage && f.signShown) return Object.assign(f, { stage: f.stage + 1, signShown: false, signShownT: null, sign: T.stageSigns[f.stage + 1], owed: wants > f.stage + 1 ? wants : null });
  if (wants > f.stage) return Object.assign(f, { owed: wants }); // waits for the sign before the next step
  return f;
}
// May an arrest land from a manhunt? Only an hour after its sign showed.
const manhuntArrest = (file, t) => file.stage === 3 && file.signShown && file.signShownT != null && t - file.signShownT >= T.manhuntSignShowsGameHoursBeforeArrest * 60;
// Does she come for talk? From day 4, once three people of his day world pass talk of his nights.
const ellisForTalk = (dayIndex, dayPeopleTalking) => dayIndex >= T.ellisFromDayIndex && dayPeopleTalking >= T.ellisTalkNeedsDayPeople;
// The constable's challenge: what he has cause for, and the three answers (stand, run, a word).
function challenge(s) {
  const cause = s.carryingAtNight || s.running || s.bloodied || s.trespassing || s.weaponShown;
  if (!cause) return { challenges: false };
  return { challenges: true, announcedSecondsBefore: T.announcesBeforeChallengeRealSeconds, callsOutFirst: true, answers: ['stand and be searched', 'run', 'a word'] };
}
function answerChallenge(answer, s) {
  if (answer === 'stand and be searched') return { result: 'searched', finds: (s.carried || []).slice(), keeps: (s.carried || []).filter((c) => c.unlawful).map((c) => c.id) };
  if (answer === 'run') return { result: 'a chase', finds: [], keeps: [] };
  // a word: talked round if he has no real cause; a note to a bought man; to an honest one it is a crime he saw
  if (s.noteOffered) return s.officerBought ? { result: 'he looks away', finds: [], keeps: [] } : { result: 'a crime he saw: bribery', finds: [], keeps: [] };
  return s.weakCause ? { result: 'talked round', finds: [], keeps: [] } : { result: 'searched', finds: (s.carried || []).slice(), keeps: (s.carried || []).filter((c) => c.unlawful).map((c) => c.id) };
}
// Traffic stops (A12): only on a reckless act an officer saw; ordinary fast driving is never stopped.
function stop(s) {
  const reckless = s.hit || s.onPavement || (s.redLightAtSpeed && true) || s.speed > T.speedLimitMetresPerSecond * T.recklessFarOverSpeedShare;
  if (!reckless || !s.inOfficersSight) return { stops: false };
  return { stops: true, atMostRealSeconds: T.stopRealSecondsAtMost, pullOver: 'looks at the car and the driver, notes the plate, a caution', refuse: 'a chase', fine: null };
}
// Bought men (A13): each does only what his limit says; a colleague who saw the payment keeps it.
function boughtMan(id, ask, s = {}) {
  const m = T.bought[id];
  if (!m) return { does: false, why: 'not a bought man: a crime he saw' };
  if (!s.paid) return { does: false, why: 'not paid' };
  if (ask !== m.limit) return { does: false, why: 'past his limit' };
  if ((s.used || 0) >= m.uses) return { does: false, why: 'he has done it once and will not again' };
  return { does: true, why: null, colleagueKeepsIt: !!s.colleagueSaw, stationChanged: false };
}
// The office searched (A13): never without the sign the evening before; what is stored there counts.
function officeSearch(s, t) {
  if (s.stage < 2) return { may: false, why: 'she is not investigating' };
  if (s.done) return { may: false, why: 'once only' };
  if (s.noticeT == null) return { may: false, why: 'no notice given', giveNotice: true };
  if (t - s.noticeT < T.officeSearchNoticeGameHours * 60) return { may: false, why: 'the notice was this evening' };
  return { may: true, finds: (s.stored || []).filter((x) => x.unlawful).map((x) => x.id) };
}
// A street on edge (A37): three seen deeds on one street within two game days.
function onEdge(deeds, street, t) {
  const recent = deeds.filter((d) => d.street === street && d.seen && t - d.t <= T.edgeWithinGameDays * 1440);
  const last = deeds.filter((d) => d.street === street && d.seen).reduce((m, d) => Math.max(m, d.t), -1e9);
  const burst = deeds.filter((d) => d.street === street && d.seen && last - d.t <= T.edgeWithinGameDays * 1440).length >= T.edgeDeeds;
  const edge = recent.length >= T.edgeDeeds || (burst && t - last <= T.edgeEasesAfterGameDays * 1440);
  return { onEdge: edge, walkStartsTimes: edge ? T.edgeWalkStartsSoonerTimes : 1, beatVisitsTimes: edge ? T.edgeBeatVisitsTimes : 1, shows: edge ? ['doors locked earlier', 'windows watched longer', 'shops shut early'] : [] };
}
// Police after a deed (A36).
const afterDeed = (deed) => (!deed.reported ? { officer: false } : { officer: true, withinGameMinutes: T.officerAtTheSpotWithinGameMinutes, tape: !!deed.body, torchAtNight: true, ellisNextMorning: !!deed.body, watchedUntilHour: T.spotWatchedUntilHour, onScreenMark: null });
// Cars and people (DESIGN 5): a hit hurts by speed and never kills; then the choice, at once.
function carHit(speed, aimed) {
  if (speed < T.carForgivenBelowMetresPerSecond) return { hurt: 'a mouthful', dies: false, rung: null, choiceWithinSeconds: null };
  const hurt = speed >= T.carHurtAtMetresPerSecond.badly ? 'badly' : speed >= T.carHurtAtMetresPerSecond['broken leg'] ? 'broken leg' : 'bruise';
  return { hurt, dies: false, rung: aimed ? 7 : null, hospitalDays: T.hospitalDaysByHurt[hurt], choiceWithinSeconds: 2, choices: ['stop and help', 'drive off'] };
}
function afterHit(choice) {
  if (choice === 'stop and help') return { costsMinutes: true, faceBesideTheCab: true, remembered: 'he stopped', chase: false, firmFaresShare: 1, gameOver: false };
  return { hitAndRun: true, carDescribed: true, chaseIfSeen: true, told: "a Mickey's cab knocked her down and never stopped", firmFaresShare: T.hitAndRunFareShare, forGameDays: T.hitAndRunCostsFirmGameDays, gameOver: false };
}
const ambulance = (calledT) => ({ arrivesT: calledT + T.ambulanceArrivesGameMinutes });
export const PIECE = { name: 'law', fns: { mayArrest, custody, ellis, manhuntArrest, ellisForTalk, challenge, answerChallenge, stop, boughtMan, officeSearch, onEdge, afterDeed, carHit, afterHit, ambulance } };
