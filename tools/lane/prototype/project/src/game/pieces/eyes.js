// RULE PIECE: eyes and ears (DESIGN 2, A1 to A4, A10, A21, A23, A26, A27, A32 to A34, A38). Pure. Unreal ports it and
// passes test/cases/eyes.json. The real town code holds the canonical perception (its rows pass in the browser
// copy); this piece holds the parts of being seen that are new in the design and not yet behind the town's door.
import { TUNE as T } from '../tune/foot.js';

const RUNGS = ['nothing', 'someone', 'a shape', 'a mark', 'a face', 'recognised'];
// What a watcher catches of him. s: { metres, light (0..1), knowsHim, lineOfSight, still, inDoorway, backTurned,
// coat, marked, peopleNear, torchOn, scarfAndHat, newCoatSince, sawOldCoat, facing }
function caught(s) {
  if (s.lineOfSight === false || s.facing === false) return { rung: 0, what: RUNGS[0], glanceSeconds: null };
  let light = s.torchOn ? Math.max(s.light, T.torchLightsHimAs) : s.light;
  if (s.inDoorway && s.still && !s.torchOn) light = Math.min(light, T.light.doorway);
  const reach = (m) => m * light; // light scales how far each rung is caught (DESIGN 2)
  let rung = 0;
  if (s.metres <= reach(T.shapeAtMetres)) rung = 2;
  if (s.metres <= reach(T.markAtMetres) && (s.coat || s.marked || s.scarfAndHat || s.carrying)) rung = 3;
  if (s.metres <= reach(T.faceAtMetres) && !s.backTurned && !s.scarfAndHat) rung = 4;
  if (s.knowsHim && s.metres <= reach(T.recognisedAtMetres) && !s.backTurned && !s.scarfAndHat && rung >= 2) rung = 5;
  if (s.inDoorway && s.still && !s.torchOn && s.metres > T.stillShapeOnlyBeyondMetres) rung = Math.min(rung, 2);
  // a second coat breaks the mark rung for anybody who saw the first (ER-COAT-01)
  if (s.sawOldCoat && s.newCoatSince && rung === 3) rung = 2;
  const glance = T.glanceRealSeconds * ((s.peopleNear || 0) >= T.amongPeopleAtLeast ? T.amongPeopleGlanceTimes : 1) / (s.running ? T.runningNoticedTimesFaster : 1);
  return { rung, what: RUNGS[rung], glanceSeconds: rung ? Math.round(glance * 1000) / 1000 : null };
}
// The head turns at the start of the time it takes to know him, not the end (ER-EYES-03).
const cue = () => ({ headTurnsAtSeconds: 0, knowsAtSeconds: T.knowingRealSeconds, warningSeconds: T.knowingRealSeconds, enough: T.knowingRealSeconds >= T.cueBeforeKnowingRealSecondsAtLeast });
// A man stopped who belongs (sitting, smoking, at the bus stop) draws no second look; one standing about at night does.
const secondLook = (s) => !s.belongs && s.night && s.standingAbout;
// How far a noise carries: the act, the hour, the rain.
function reach(act, hour, rain, slow) {
  const night = hour >= T.nightFromHour || hour < T.nightUntilHour;
  let m = act === 'footstep' ? (night ? T.nightFootstepMetres : 0) : (T.reachMetres[act] || 0) * (night ? T.nightReachTimes : 1);
  if (act === 'footstep' && slow) m *= T.slowWalkHalvesFootsteps;
  if (rain) m *= T.rainReachTimes;
  return Math.round(m * 100) / 100;
}
const hears = (metres, act, hour, rain) => metres <= reach(act, hour, rain);
// The horn (A32): everyone inside its reach hears it; a waiting fare inside 15 m comes out within 10 s.
const horn = (s) => ({ heardBy: s.listeners.filter((l) => l.metres <= reach('horn', s.hour, s.rain)).map((l) => l.id), fareComesOutWithinSeconds: s.fareMetres != null && s.fareMetres <= T.hornFareComesWithinMetres ? T.hornFareComesWithinRealSeconds : null, alarmsPolice: false });
// A thrown stone or a rattled bin (A23): a watcher inside the reach turns to it and remembers a noise.
const drawn = (metres, what, hour, rain) => (hears(metres, what, hour, rain) ? { turns: true, forSeconds: T.noiseHoldsAWatcherRealSeconds, remembers: 'a noise' } : { turns: false, forSeconds: 0, remembers: null });
// Street manners (A10): each gesture is an act, answered within a second.
const MANNERS = { nod: { rung: 0, answer: 'a nod back' }, greeting: { rung: 0, answer: 'a word back' }, 'hard look': { rung: 1, answer: 'looks away or holds it' }, shove: { rung: 4, answer: 'steps back or squares up' }, oi: { rung: 0, answer: 'stops and turns', stopsSeconds: T.oiStopsAWalkerRealSeconds } };
const manner = (g) => (MANNERS[g] ? Object.assign({ act: g, answeredWithinSeconds: T.mannersAnsweredWithinRealSeconds, remembered: true }, MANNERS[g]) : null);
// Tails (A2). state: { doubt: 0|1, ended: null }. ev: { rung (what the target caught on a look back), arrived, stopped, cabBehindTimes }
function tail(state, ev) {
  const s = Object.assign({ doubt: 0, ended: null, learned: null }, state);
  if (s.ended) return s;
  if (ev.stopped) return Object.assign(s, { ended: 'he stopped' });
  if (ev.arrived) return Object.assign(s, { ended: 'arrived', learned: ev.arrived });
  const mark = ev.rung === 3 || (ev.cabBehindTimes || 0) >= T.cabBehindTwiceIsADoubt;
  if (ev.rung >= 4) return s.doubt ? Object.assign(s, { ended: 'made' }) : Object.assign(s, { doubt: 1, sign: 'a look back held' }); // the doubt always comes first (ER-TAIL-02)
  if (mark) return Object.assign(s, { doubt: 1, sign: 'a change of pace' });
  return s; // a shape is nothing; losing sight is not failing (ER-TAIL-01)
}
// A foot chase, either way round (A3, DESIGN 8): caught, lost or still on. Always over within 90 s.
function chase(s) {
  if (s.metres <= T.collarWithinMetres && s.fromBehind !== false) return { st: 'caught', why: 'a hand on the collar' };
  if (s.unseenSeconds >= T.lostAfterUnseenRealSeconds) return { st: 'lost', why: 'out of sight for 7 s' };
  if (s.metres >= T.lostBeyondMetres) return { st: 'lost', why: '70 m away' };
  if (s.seconds >= T.chaseEndsWithinRealSeconds) return { st: 'lost', why: 'he gives it up' };
  return { st: 'on', why: null };
}
// A whole straight chase in numbers: a pursuer on a direct line catches; one who lags loses (ER-PURSUE-02).
function pursuit(startMetres, pursuerSpeedShare, tomRunMetresPerSecond) {
  const runner = tomRunMetresPerSecond * T.runnerSpeedShareOfToms,
    closing = tomRunMetresPerSecond * pursuerSpeedShare - runner;
  if (closing > 0) {
    const t = (startMetres - T.collarWithinMetres) / closing;
    return t <= T.chaseEndsWithinRealSeconds ? { st: 'caught', seconds: Math.round(t * 10) / 10 } : { st: 'lost', seconds: T.chaseEndsWithinRealSeconds };
  }
  const t = closing < 0 ? (T.lostBeyondMetres - startMetres) / -closing : T.chaseEndsWithinRealSeconds;
  return { st: 'lost', seconds: Math.round(Math.min(t, T.chaseEndsWithinRealSeconds) * 10) / 10 };
}
// Vaulting (A26): set places only, under 1.2 m, running.
const vault = (s) => (s.setPlace && s.heightMetres < T.vaultUnderMetres && s.running ? { vaults: true, seconds: s.pursuer ? T.pursuerVaultTakesRealSeconds : T.vaultTakesRealSeconds } : { vaults: false, seconds: 0 });
// Searching (A4, A33): time by container, doubled in the dark without a torch; the noise by container.
const search = (container, s = {}) => ({ seconds: (T.searchRealSeconds[container] || T.searchRealSeconds.desk) * (s.dark && !s.torch ? T.searchInTheDarkTimes : 1), noiseMetres: s.forced ? T.reachMetres.forcedCupboard * (s.night ? 1 : 0.5) : T.reachMetres.drawer, beamSeenFromStreet: !!(s.torch && s.window), needsHold: true, puzzle: false });
// Lifting from a pocket (A34): fixed limits, never a roll.
function lift(s) {
  const felt = s.attentive || s.light > T.liftGoodLightAbove || s.peopleNear < T.liftCrowdAtLeast;
  return { felt, headTurnsFirstBySeconds: felt ? T.headTurnsBeforeFeltRealSeconds : null, holdSeconds: T.liftHoldRealSeconds, missedBy: 'next morning', suspects: felt ? ['tom'] : s.noticedNear || [] };
}
// Finding an unseen deed (A38): the first person whose routine passes the trace finds it and holds only the aftermath.
function found(deed, passers) {
  if (deed.hidden || deed.sunk || !deed.trace) return { by: null, atT: null, holds: null };
  const first = passers.filter((p) => p.t >= deed.t).sort((a, b) => a.t - b.t)[0];
  return first ? { by: first.id, atT: first.t, holds: 'aftermath' } : { by: null, atT: null, holds: null };
}
// Taking a parked car (A27): only empty parked cars, loud, six seconds; reported when its owner finds it gone.
const takeCar = (car) => (car.someoneInIt || !car.parked ? { can: false, why: 'never a car with somebody in it' } : { can: true, seconds: T.takeCarRealSeconds, noise: 'brokenGlass', roofSign: false, reportedWhen: 'its owner finds it gone', namedAs: car.plate });
// Trespass (A10): the label of the ground and the hour give the warnings, in order.
function trespass(place, hour, secondsThere) {
  const open = place.label === 'public' || (place.label === 'hours' && hour >= place.openFromHour && hour < place.openUntilHour);
  if (open) return { stage: 'free', warnings: 0 };
  const skipFirst = place.label === 'forbidden';
  if (secondsThere >= T.trespassActsAfterRealSeconds) return { stage: 'calls someone or acts', warnings: skipFirst ? 1 : 2 };
  if (secondsThere >= T.trespassSecondWarningAfterRealSeconds || skipFirst) return { stage: 'warns again', warnings: skipFirst ? 1 : 2 };
  return { stage: 'warns', warnings: 1 };
}
// Marks that last (A21): bruises three game days, a limp one; caught like any give-away while they last.
const marks = (daysSinceBeaten) => ({ bruised: daysSinceBeaten < T.bruisesLastGameDays, limp: daysSinceBeaten < T.limpLastsGameDays });
// Casing (A23): watched long enough, a place's hours, key holder and open way are learned as the routines have them.
const cased = (minutesWatched, place) => (minutesWatched >= T.casingLearnsAfterGameMinutes ? { learned: true, hours: [place.openFromHour, place.openUntilHour], keyHolder: place.keyHolder, openWay: place.openWay } : { learned: false });
// The walk (DESIGN 2 "The walk", ER-EYES-04): a witness who means to tell sets off and is seen going. No phones in
// pockets in 1990: the walk is the timer, and until it ends nothing is on record. s: { metres, inHisSight, onEdge }
function walk(s) {
  const W = T.walk;
  const startsAfterSeconds = W.startsAfterRealSeconds * (s.onEdge ? W.onEdgeStartsSoonerTimes : 1);
  const walkSeconds = s.metres / W.metresPerSecond;
  const lastsSeconds = s.inHisSight ? Math.max(walkSeconds, W.lastsAtLeastRealSecondsInHisSight) : walkSeconds;
  return { startsAfterSeconds, lastsSeconds, standsFirstSeconds: lastsSeconds - walkSeconds };
}
// He reaches the witness first: talk them round, pay, threaten, put it right, or let them go. A threat can stop
// a report to the police, never the street's talk (ruling 3 Oct). s: { regard, nerve, venal, upright, crime
// (1 minor, 2 violence, 3 killing), damage, askedBefore, pocketPence }
function reached(choice, s) {
  const W = T.walk,
    out = (stops, o = {}) => Object.assign({ stops, costPence: 0, fearTo: null, regardBy: 0, streetStillTalks: true, makesAnAct: null, sooner: false }, o);
  if (s.askedBefore) return out(false, { regardBy: W.askedTwiceRegardBy, sooner: true }); // one go at each witness
  if (choice === 'let go') return out(false);
  if (choice === 'talk round') {
    const ok = s.crime <= 1 && s.regard >= (s.upright ? W.talkRoundNeedsRegardUpright : W.talkRoundNeedsRegard);
    return ok ? out(true, { regardBy: W.talkedRoundRegardBy }) : out(false, { regardBy: W.talkFailedRegardBy });
  }
  if (choice === 'pay') {
    const price = W.payPenceByCrime[Math.min(3, Math.max(1, s.crime))];
    if (s.upright || s.venal < W.payNeedsVenal || s.crime >= 3) return out(false, { regardBy: W.payRefusedRegardBy, makesAnAct: 'bribe_try', sooner: true });
    if (s.pocketPence < price) return out(false, { costPence: 0, short: true });
    return out(true, { costPence: price, bought: true });
  }
  if (choice === 'threaten') {
    // it works on anybody whose nerve is under the bar; it is itself a thing done to them, and the street hears of it
    const ok = s.nerve < W.threatWorksBelowNerve;
    return ok ? out(true, { fearTo: W.threatFearTo, regardBy: W.threatRegardBy, makesAnAct: 'threat' }) : out(false, { regardBy: W.threatRegardBy, makesAnAct: 'threat', sooner: true });
  }
  if (choice === 'put it right') {
    // only damage can be put right, with money for the mending, and only with somebody not set against him
    if (!s.damage || s.crime > 1) return out(false);
    if (s.pocketPence < W.putRightPence) return out(false, { short: true });
    return s.regard > W.putRightNeedsRegardAbove ? out(true, { costPence: W.putRightPence, regardBy: W.putRightRegardBy, streetStillTalks: true }) : out(false, { regardBy: 0 });
  }
  return out(false);
}
export const PIECE = { name: 'eyes', fns: { walk, reached, caught, cue, secondLook, reach, hears, horn, drawn, manner, tail, chase, pursuit, vault, search, lift, found, takeCar, trespass, marks, cased } };
