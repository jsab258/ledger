// LEDGER, the whole game: the system "law". The police as a pressure he can read and answer, never the end of the
// game (DESIGN 8; A12, A13, A36, A37; parts 2.6.1 to 2.6.10, 2.5.4). The real town code decides who goes to the
// police over the week's damage, DS Ellis's mornings and the arrest for it; the prototype's own rule still decides
// statements about violence (the gap is in ONE-SHOT-SIM-DIFFERENCES.md). This file adds what the design adds
// around them: the nightly beat and its challenge with three answers, the hours each offence costs, DS Ellis's
// four stages each with its sign, the office searched with notice, traffic stops, bought men, an officer at the
// spot after a reported deed, and a street on edge. The rules are pieces/law.js.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on, tomXZ, freshLine, inView } from './core.js';
import { G } from '../state.js';
import { hyp, quid } from '../util.js';
import { act, logLine } from '../events.js';
import { pay } from '../money.js';
import { choose, scene, say, sub, after } from '../ui.js';
import { goToPoint, gameMinPerSec } from '../routines.js';
import { freeSpot } from '../map.js';
import { KINDS } from '../kinds.js';
import { sense, tomTarget, tomNotices } from '../seeing.js';
import { RULES } from '../rules.js';
import { PIECE as LAW } from './pieces/law.js';
import { PIECE as EYES } from './pieces/eyes.js';
import { carried, drop, stored } from './crime.js';
import { sign } from './ledgerx.js';

const T = RULES.game.law;
const L = LAW.fns;
const S = { beat: null, chase: null, carChase: null, heard: 0 };
const night = (h = hourNow()) => h >= T.beatFromHour || h < T.beatUntilHour;
const offenceOf = (a, E) => (a.offence ? a.offence : E && KINDS[E.kind].damage ? 'damage' : E && E.kind === 'kill' ? 'killing' : E && (E.kind === 'weapon_used' || E.kind === 'knocked') ? 'wounding' : a.violent ? 'assault' : 'damage');

// ---- what an arrest costs (2.6.3, 2.6.4): hours by the offence, a caution or a charge, never the game ----
function custody(a, ran, E) {
  const x = X('law'),
    offence = offenceOf(a, E);
  // once DS Ellis has joined the street crimes to the fire (Act II's beat), nothing of his is small: no caution, and longer
  const c = L.custody(offence, { ownedUp: !ran && offence === 'damage' && !x.charges.length && !x.oneCase, first: !x.charges.length && !x.cautions && !x.oneCase, woreCoat: G.tom.coat });
  const hours = c.gameHours + (ran ? RULES.police.heldGameHoursAddedIfHeRan : 0) + (x.oneCase ? T.oneCaseAddsGameHours : 0);
  if (c.ends === 'cautioned') x.cautions++;
  else {
    x.charges.push({ offence, t: Math.round(G.t), e: E ? E.id : null });
    ellisEvent('charge');
  }
  x.arrests.push({ offence, hours, ends: c.ends, t: Math.round(G.t) });
  if (E) x.takenFor[E.id] = 1;
  emit('law.arrested', { offence, hours, ends: c.ends });
  return { hours, ends: c.ends === 'cautioned' ? 'A caution, and the door.' : c.ends === 'charged, bail' ? 'Charged, and bailed to come back.' : 'Charged. It is written down now, and it stays written.' };
}
// ---- DS Ellis's four stages (2.6.5): no stage skipped unseen, each with its sign ----
export function ellisEvent(what) {
  const x = X('law'),
    before = x.ellis.stage;
  x.ellis = L.ellis(x.ellis, { what }, G.t);
  if (x.ellis.stage !== before) logLine(`DS Ellis: ${T.stages[x.ellis.stage]} (${what})`, 'police');
  return x.ellis;
}
function ellisSigns() {
  const x = X('law'),
    f = x.ellis,
    t = G.tom;
  if (f.signShown) {
    if (f.owed && f.owed > f.stage) ellisEvent(f.owed === 3 ? 'witnessed killing' : f.owed === 2 ? 'body' : 'talk'); // the next step, now its sign was seen
    return;
  }
  if (G.paused || t.inCar) return;
  let shown = null;
  if (f.stage === 1) {
    // her name in the street's talk: somebody near him says it
    const P = G.named.find((Q) => here(Q, T.signHeardWithinMetres) && !Q.def.police && Q.mind.regard > -0.5);
    if (P) {
      tell('"That detective has been asking about you. Ellis, her name is."', P.def.name);
      shown = 'DS Ellis has been asking the street about him. ' + P.def.name + ' said so.';
    }
  } else if (f.stage === 2 && t.space === 'mickeys') {
    tell('"Mr Nowak? DS Ellis would like a word, when it suits. And she will want to see round the office. Tomorrow."', 'PC Ibbotson');
    x.search.noticeT = G.t; // the sign the evening before any search (ER-SEARCHED-01)
    shown = 'An officer at the office door: DS Ellis is investigating, and the office is to be looked at tomorrow.';
  } else if (f.stage === 3 && t.space === 'street') {
    tell('A police car at the kerb on Quay Street, the window down. "A man of about thirty, dark coat, from the cab office."', '');
    shown = 'A police car on Quay Street, and his description said aloud. They are looking for him.';
  }
  if (shown) {
    x.ellis = L.ellis(x.ellis, { what: 'sign shown' }, G.t);
    sign(f.stage === 3 ? 'police' : 'ellis', shown);
  }
}
// ---- the nightly beat (2.6.1) and the challenge with three answers (2.6.2, A13) ----
// what is heard and said on the beat: a line of five words or more is used once a week (core.js freshLine)
const BEAT_HEARD = [
  'Measured footsteps on the wet. The constable is on his beat.',
  'A torch swings at the far end of the street. The beat constable.',
  'Boots, slow and even, a street away. The constable is about.',
  'A cough, and the scrape of a boot on the kerb. The constable, on his round.',
];
const BEAT_STOPS = [
  '"You there. Stand still a minute. What have you got on you?"',
  '"Hold on, sir. A moment of your time. Turn your pockets out for me."',
  '"Stop there, please. I will have a look at what you are carrying."',
  '"Late to be out, sir. Stand where you are and show me your hands."',
];
const BEAT_LETS_GO = [
  'Right. On your way, then. It is late to be about.',
  'Nothing on you. Get yourself home, sir.',
  'That will do. Mind how you go tonight.',
  'Very good, sir. I will know you again.',
];
function beatStep(dt) {
  const P = P_('pc'),
    t = G.tom,
    x = X('law'),
    st = G.story;
  const busy = (st.job && st.job.watch && st.job.watch.st !== 'over') || (st.arrest && st.arrest.st) || S.chase || x.spot;
  const visits = L.onEdge(x.deeds, 'Quay Street', G.t).beatVisitsTimes;
  const on_ = night() && !busy && !P.dead; // the one-shot: he walks Quay Street and the quay all night (on a street on edge he turns sooner: beatVisitsTimes)
  void visits;
  if (!on_) {
    if (S.beat && !busy) {
      P.override = { where: 'off', act: 'idle' };
      P.goalKey = '';
    }
    return void (S.beat = null);
  }
  if (!S.beat) {
    S.beat = { leg: 0, warned: false };
    // he comes on at the top of his beat; a constable already out on the street walks from where he stands
    if (P.gone || P.space !== 'street') Object.assign(P, { x: T.beatEnds[0][0], z: T.beatEnds[0][1] });
    Object.assign(P, { override: null, gone: false, space: 'street', awake: true, route: null, hold: false });
    goToPoint(P, T.beatEnds[1][0], T.beatEnds[1][1], T.beatWalkMetresPerSecond);
  }
  const wg = x.watched.find((w) => w.untilT > G.t),
    ends = wg ? [T.beatEnds[0], [wg.x, wg.z]] : T.beatEnds; // on a watched night his round turns at the watched ground
  const to = ends[1 - S.beat.leg];
  if (hyp(P.x, P.z, to[0], to[1]) < 2 || !P.route) {
    S.beat.leg = hyp(P.x, P.z, to[0], to[1]) < 2 ? 1 - S.beat.leg : S.beat.leg;
    const nx = ends[1 - S.beat.leg];
    goToPoint(P, nx[0], nx[1], T.beatWalkMetresPerSecond);
  }
  if (t.space !== 'street' || t.inCar || G.paused) return;
  const d = hyp(P.x, P.z, t.x, t.z);
  // he is heard or seen before he can challenge (ER-POL-02)
  if (d < T.beatHeardWithinMetres && !S.beat.warned) {
    S.beat.warned = true;
    S.heard = G.played;
    tell(freshLine(BEAT_HEARD, 'The constable. His beat.'), '');
  }
  if (d > T.beatHeardWithinMetres * 1.5) S.beat.warned = false;
  // his boots on the setts: in the mix at their distance, before he is near enough to challenge (2.6.1)
  S.stepT = (S.stepT || 0) - dt;
  if (d < T.beatHeardWithinMetres && P.moving && S.stepT <= 0) {
    S.stepT = 0.55;
    if (G.hooks.heard) G.hooks.heard('steps', Math.max(0.05, 0.6 * (1 - d / T.beatHeardWithinMetres)), 'the constable');
  }
  if (G.t - x.challengedT < T.challengeAgainAfterGameMinutes || G.played - S.heard < T.announcesBeforeChallengeRealSeconds) return;
  const s = sense(P, tomTarget());
  if (!s.see || d > T.challengeWithinMetres) return;
  const items = carried();
  const cause = { carryingAtNight: !!t.carry || items.some((i) => i.unlawful) || items.length >= 2, running: t.run, bloodied: !!(G.x.crime && G.x.crime.bloody) || t.hurt > 0.5, trespassing: false, weaponShown: !!t.armed };
  const c = L.challenge(cause);
  if (!c.challenges) return;
  x.challengedT = G.t;
  challenge(P, cause, items);
}
async function challenge(P, cause, items) {
  const x = X('law'),
    t = G.tom;
  P.route = null;
  P.hold = true;
  P.ang = Math.atan2(t.x - P.x, t.z - P.z);
  // he calls out first, always: heard and shown before anything is put to him
  sub(cause.backAtTheSpot ? '"You. Stop there."' : '"You, there. Hold on a minute."', 'The constable', 'face', 3);
  if (G.hooks.sfx) G.hooks.sfx('shout', 0.6);
  x.calledOutPlayed = G.played;
  await new Promise((res) => after(T.callsOutBeforeHeActsRealSeconds, res));
  const weak = !cause.weaponShown && !cause.bloodied && !items.some((i) => i.unlawful) && !t.carry;
  const bought = x.bought.harker && x.bought.harker.paid;
  const i = await scene(() => choose('pc', cause.backAtTheSpot ? '"Back for another look, are we? Stand there. What have you got on you?"' : freshLine(BEAT_STOPS, '"You again. Pockets, please."'), ['Stand and be searched.', 'Run.', 'A word.']));
  const r = L.answerChallenge(['stand and be searched', 'run', 'a word'][i], { carried: items, weakCause: weak, noteOffered: false, officerBought: bought });
  x.challenges.push({ answer: i, result: r.result, t: Math.round(G.t) });
  if (r.result === 'searched') {
    for (const id of r.keeps) drop(id);
    if (r.keeps.includes('bag') && G.story.job) {
      t.carry = null;
      G.story.job.st = 'lost';
      G.story.job.carrying = false;
    }
    act('searched_by', { told: ['pc'] });
    await scene(() => say('pc', r.keeps.length ? `I will keep ${r.finds.filter((f) => r.keeps.includes(f.id)).map((f) => f.name).join(' and ')}. And your name, sir. I am writing it down.` : freshLine(BEAT_LETS_GO, 'Go on, then.')));
    write(r.keeps.length ? `Searched by the constable on Quay Street. He kept ${r.finds.filter((f) => r.keeps.includes(f.id)).map((f) => f.name).join(' and ')}, and wrote the name down.` : 'Searched by the constable on Quay Street. He found nothing to keep.', { how: 'Did it', kind: 'note' });
    if (r.keeps.length) ellisEvent('talk');
  } else if (r.result === 'talked round') {
    act('talked_round', { silent: true, told: ['pc'] });
    await scene(() => say('pc', 'Aye, well. Get yourself home.'));
  } else if (r.result === 'a chase') {
    S.chase = { seconds: 0, unseen: 0 };
    act('ran_police', { noiseR: RULES.police.runningNoiseMetres });
    if (G.hooks.happened) G.hooks.happened('ran'); // whoever could see him just then saw him run (game/back.js)
    tell('"Oi! Stop!" A whistle behind him.', 'PC Ibbotson');
  }
  P.hold = false;
}
function chaseStep(dt) {
  const c = S.chase;
  if (!c) return;
  const P = P_('pc'),
    t = G.tom,
    x = X('law');
  c.seconds += dt;
  const seeable = t.space === 'street' && !t.inCar,
    d = hyp(P.x, P.z, t.x, t.z),
    los = seeable && G.env.los(P.x, P.z, t.x, t.z);
  // where sight broke he does not know which way the man went: at that place he checks, a breath, before he runs on
  if (los && c.unseen > 0.6) c.pause = T.constableLooksAboutRealSeconds;
  c.unseen = los ? 0 : c.unseen + dt;
  if (los || c.lx === undefined) (c.lx = t.x), (c.lz = t.z); // the last place the constable saw him: all he knows
  if (c.pause > 0) {
    c.pause -= dt;
    P.route = null;
    P.moving = false;
    P.ang = Math.atan2(t.x - P.x, t.z - P.z);
  } else if (los && (!P.route || c.seconds % 1 < dt))
    // a big man in a greatcoat: he runs hard for a short while, and then he is blown and it shows in his pace
    goToPoint(P, t.x, t.z, c.seconds < T.constableBlownAfterRealSeconds ? T.constableRunsMetresPerSecond : T.constableBlownMetresPerSecond);
  const r = EYES.fns.chase({ metres: seeable ? d : 99, unseenSeconds: c.unseen, seconds: c.seconds });
  if (r.st === 'on') return;
  S.chase = null;
  x.chases.push({ st: r.st, seconds: Math.round(c.seconds), t: Math.round(G.t) });
  if (r.st === 'caught') {
    const items = carried();
    for (const i of items.filter((q) => q.unlawful)) drop(i.id);
    G.story.arrest = { e: null, violent: false, offence: 'damage', due: G.t, st: undefined, by: [], ran: true };
    tell('A hand on his shoulder. "Nobody runs from me for nothing."', 'PC Ibbotson');
  } else {
    // he walks to the last place he saw him and looks round for about a game hour: the law stays near (A3)
    x.watched.push({ x: Math.round(c.lx), z: Math.round(c.lz), untilT: G.t + RULES.game.foot.constableLooksRoundGameMinutes, why: 'the constable lost him here' });
    tell('No boots behind him now. He has lost him.', '');
    // and he does walk there: to the last place he saw him, to stand and look about for the hour
    if (!x.spot) x.spot = { x: Math.round(c.lx), z: Math.round(c.lz), e: null, st: 'going', arriveByT: G.t + 30, staysUntilT: null, tape: false, torch: true, seen: true, speed: T.officerToTheSpotMetresPerSecond };
    P.route = null;
    write('Ran from the constable on Quay Street and lost him. He saw a man; whether he saw a face is another thing.', { how: 'Did it' });
    ellisEvent('talk');
  }
}
// ---- police after a deed (A36, part 2.6.10): once it is reported an officer walks to the spot and stands there a
// while, with a torch at night; a body brings tape, and DS Ellis the next morning; the spot is watched ground
// until morning, and going back there is the risk. Nothing on screen marks it: he reads the man, the torch, the tape.
function afterDeed(E, body) {
  const x = X('law');
  if (!E || x.watched.some((w) => w.e === E.id)) return;
  const r = L.afterDeed({ reported: true, body });
  if (!r.officer) return;
  const untilT = (dayNow() + (hourNow() >= r.watchedUntilHour ? 1 : 0)) * 1440 + r.watchedUntilHour * 60;
  x.watched.push({ x: E.x, z: E.z, untilT, why: KINDS[E.kind].mine(E), tape: r.tape, e: E.id, tapeSeen: false });
  // one officer: a graver deed, or the first, has him
  if (!x.spot || (r.tape && !x.spot.tape)) x.spot = { x: E.x, z: E.z, e: E.id, st: 'sent', arriveByT: G.t + r.withinGameMinutes, staysUntilT: null, tape: r.tape, torch: r.torchAtNight, seen: false };
  if (r.ellisNextMorning) x.ellisDue = { t: (dayNow() + 1) * 1440 + T.ellisNextMorningAtHour * 60, what: 'body' };
  logLine('An officer is sent to the spot: ' + KINDS[E.kind].truth(E), 'police');
}
function spotStep() {
  const x = X('law'),
    sp = x.spot,
    P = P_('pc'),
    t = G.tom;
  if (!sp || !P || P.dead || S.chase || (G.story.arrest && G.story.arrest.st)) return;
  const d = hyp(P.x, P.z, sp.x, sp.z),
    tomFar = t.space !== 'street' || hyp(P.x, P.z, t.x, t.z) > 60;
  if (sp.st === 'sent') {
    if (P.gone || P.space !== 'street') Object.assign(P, { override: null, gone: false, space: 'street', awake: true, x: RULES.police.arrivesAtXMetres, z: RULES.police.arrivesAtZMetres });
    P.override = null;
    P.route = null;
    // he is to be there inside the time the rule gives: a walk if that will do it, else at the double
    sp.speed = Math.min(T.constableRunsMetresPerSecond, Math.max(T.officerToTheSpotMetresPerSecond, (d * 1.25) / Math.max(1, (sp.arriveByT - G.t) / gameMinPerSec())));
    goToPoint(P, sp.x, sp.z, sp.speed);
    sp.st = 'going';
    S.beat = null;
  } else if (sp.st === 'going') {
    if (!P.route && d > 3) goToPoint(P, sp.x, sp.z, sp.speed || T.officerToTheSpotMetresPerSecond);
    if (d <= 3 || (G.t >= sp.arriveByT && tomFar)) {
      // he is there inside the time the rule gives; nobody is put anywhere while he could be seen walking
      if (d > 3) {
        const f = freeSpot(sp.x, sp.z) || [sp.x, sp.z];
        Object.assign(P, { x: f[0], z: f[1] });
      }
      Object.assign(P, { route: null, hold: true });
      sp.st = 'there';
      sp.staysUntilT = G.t + T.officerStaysAtTheSpotGameMinutes;
    }
  } else if (sp.st === 'there') {
    P.hold = true;
    // he looks about him the whole time he stands there, and round at any step close by
    P.ang = inView(P, 9) ? Math.atan2(t.x - P.x, t.z - P.z) : P.ang + 0.02;
    if (G.t >= sp.staysUntilT) {
      x.spot = null;
      P.hold = false;
      P.override = { where: 'off', act: 'idle' };
      P.goalKey = '';
      return;
    }
  }
  // what he can read of it: the man at the spot, the torch at night, the tape
  if (!sp.seen && sp.st !== 'sent' && (tomNotices(P) || inView(P, 30)) && hyp(P.x, P.z, t.x, t.z) < T.beatHeardWithinMetres * 1.5) {
    sp.seen = true;
    const where = sp.st === 'there' ? 'standing where it happened' : 'walking down to where it happened';
    tell(night() && sp.torch ? `A torch, going slowly over the ground. The constable is ${where}.` : `The constable is ${where}, his notebook out.`, '', 7);
    write(`A constable at the spot (${x.watched.find((w) => w.e === sp.e)?.why.toLowerCase() || 'what was done'}). Somebody rang them. That ground is watched until morning.`, { key: 'spot' + sp.e, how: 'Saw it himself', ev: sp.e });
  }
}
// The watched ground: tape he can see, and an officer with cause if he comes back to it.
function watchedStep() {
  const x = X('law'),
    t = G.tom;
  if (t.space !== 'street' || G.paused || S.chase) return; // a man he is already running after is not called to again
  const [tx, tz] = tomXZ();
  const w = watchedNear(tx, tz);
  if (!w) return;
  if (w.tape && !w.tapeSeen && G.env.los(tx, tz, w.x, w.z)) {
    w.tapeSeen = true;
    tell('Blue and white tape across the way, tied off on a drainpipe. Nobody is getting through there today.', '', 7);
    write('Police tape where it happened. A detective comes for that, in the morning.', { key: 'tape' + w.e, how: 'Saw it himself', ev: w.e });
  }
  const P = P_('pc');
  if (t.inCar || !P || P.gone || P.space !== 'street' || G.t - x.challengedT < T.backAtTheSpotCallAfterGameMinutes) return;
  const s = sense(P, tomTarget());
  if (!(s.see || inView(P, T.challengeWithinMetres)) || hyp(P.x, P.z, t.x, t.z) > T.challengeWithinMetres) return;
  const c = L.challenge({ trespassing: true }); // back at the spot is cause enough
  if (!c.challenges) return;
  x.challengedT = G.t;
  x.backAtTheSpot = (x.backAtTheSpot || 0) + 1;
  challenge(P, { trespassing: true, backAtTheSpot: true }, carried());
}
export const watchedNear = (x, z) => X('law').watched.find((w) => w.untilT > G.t && hyp(w.x, w.z, x, z) < T.watchedGroundWithinMetres) || null;
// ---- traffic police (A12): one patrol car on its loop; a stop only on a reckless act in its sight ----
function patrolAt() {
  const n = T.patrolLoop.length,
    f = ((G.played % T.patrolLoopRealSeconds) / T.patrolLoopRealSeconds) * n,
    a = T.patrolLoop[Math.floor(f) % n],
    b = T.patrolLoop[(Math.floor(f) + 1) % n],
    k = f - Math.floor(f);
  return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
}
export function patrolSees(x, z) {
  const [px, pz] = patrolAt();
  return hyp(px, pz, x, z) < T.patrolSeesWithinMetres && G.env.los(px, pz, x, z);
}
async function trafficStop(why) {
  const x = X('law');
  if (S.carChase || G.t - x.stoppedT < 30) return;
  x.stoppedT = G.t;
  const i = await scene(() => choose('', 'A blue light in the mirror, and two tones of the horn. The patrol car wants him to pull over.', ['Pull over.', 'Put his foot down.']));
  if (i === 0) {
    G.car.v = 0;
    x.plateNoted = true;
    act('stopped_car', {});
    const bought = x.bought.harker && x.bought.harker.paid;
    await scene(() => say('PC Harker', bought ? 'Mr Nowak. Mind how you go. I never saw you.' : `${why === 'hit' ? 'You have knocked somebody down.' : 'That is no way to drive a hire car.'} I have your plate. Consider yourself cautioned.`));
    write('Pulled over by the patrol car. A caution, and the plate written down.', { how: 'Did it' });
    x.stops.push({ why, result: 'cautioned', t: Math.round(G.t) });
  } else {
    act('drove_off_police', {});
    S.carChase = { seconds: 0, unseen: 0, slow: 0, trail: [tomXZ()] };
    x.stops.push({ why, result: 'a chase', t: Math.round(G.t) });
  }
}
function carChaseStep(dt) {
  const c = S.carChase;
  if (!c) return;
  const [tx, tz] = tomXZ(),
    x = X('law');
  c.seconds += dt;
  c.trail.push([tx, tz]);
  // the patrol car follows his trail a little way behind: break its line of sight and it loses him
  let back = c.trail[0],
    acc = 0;
  for (let i = c.trail.length - 1; i > 0 && acc < T.carChaseFollowsMetresBehind; i--) {
    acc += hyp(c.trail[i][0], c.trail[i][1], c.trail[i - 1][0], c.trail[i - 1][1]);
    back = c.trail[i - 1];
  }
  if (c.trail.length > 4000) c.trail.splice(0, 2000);
  const los = G.env.los(back[0], back[1], tx, tz);
  c.unseen = los ? 0 : c.unseen + dt;
  if (los || c.lx === undefined) (c.lx = t.x), (c.lz = t.z); // the last place the constable saw him: all he knows
  c.slow = G.tom.inCar && Math.abs(G.car.v) < T.carChaseCaughtBelowMetresPerSecond ? c.slow + dt : 0;
  let st = EYES.fns.chase({ metres: los ? T.carChaseFollowsMetresBehind : 40, unseenSeconds: c.unseen, seconds: c.seconds, fromBehind: false }).st;
  if (c.slow >= T.carChaseCaughtAfterRealSeconds && los) st = 'caught';
  if (st === 'on') return;
  S.carChase = null;
  x.carChases.push({ st, seconds: Math.round(c.seconds), t: Math.round(G.t) });
  if (st === 'caught') {
    G.car.v = 0;
    G.story.arrest = { e: null, violent: false, offence: 'damage', due: G.t, by: [], ran: true };
    tell('The patrol car is across his bonnet. Out you get.', '');
  } else {
    tell('The blue light is gone from the mirror. They have the plate, all the same.', '');
    write('Would not stop for the patrol car, and lost it. They have the cab now, if not the driver.', { how: 'Did it' });
    x.plateNoted = true;
    ellisEvent('talk');
  }
}
// ---- bought men (A13): two named officers, each with a price and a limit ----
export function buy(id) {
  const x = X('law'),
    m = T.bought[id];
  if (!m || (x.bought[id] && x.bought[id].paid)) return false;
  if (!pay(m.pricePence, false, 'paid ' + m.name)) return false;
  x.bought[id] = { paid: true, used: 0 };
  act('paid_officer', { name: m.name, silent: true });
  write(`${m.name} took ${quid(m.pricePence)}. He ${m.limit}, and nothing more.`, { how: 'Did it' });
  return true;
}
export function useBought(id, ask, colleagueSaw) {
  const x = X('law'),
    b = x.bought[id] || {};
  const r = L.boughtMan(id, ask, { paid: b.paid, used: b.used, colleagueSaw });
  if (r.does) b.used = (b.used || 0) + 1;
  return r;
}
// ---- the office searched (A13): once, with notice the evening before ----
function officeSearchStep() {
  const x = X('law');
  const r = L.officeSearch({ stage: x.ellis.stage, noticeT: x.search.noticeT, done: x.search.done, stored: stored() }, G.t);
  if (!r.may || hourNow() < 9 || hourNow() > 17) return;
  x.search.done = true;
  x.search.found = r.finds;
  act('office_searched', { silent: true, told: ['sheila', 'pauline'] });
  for (const id of r.finds) {
    const i = G.x.crime.stored.findIndex((s) => s.id === id);
    if (i >= 0) G.x.crime.stored.splice(i, 1);
  }
  if (r.finds.length) {
    x.charges.push({ offence: 'what was in the office drawer', t: Math.round(G.t), e: null });
    ellisEvent('charge');
  }
  write(r.finds.length ? `DS Ellis searched the office and took ${r.finds.join(' and ')} out of the drawer. It goes on her file.` : 'DS Ellis searched the office and found nothing to take.', { how: 'Sheila says', who: 'sheila' });
  tell(r.finds.length ? '"They went through every drawer. They took what was in the locked one."' : '"They went through every drawer. They found nothing, and they did not like that."', 'sheila');
}

register({
  id: 'law',
  fresh: () => ({ ellis: { stage: 0, signShown: true, signShownT: null, owed: null }, charges: [], cautions: 0, arrests: [], takenFor: {}, watched: [], spot: null, ellisDue: null, deeds: [], edge: false, bought: {}, search: { noticeT: null, done: false, found: [] }, challengedT: -1e9, challenges: [], chases: [], stops: [], carChases: [], stoppedT: -1e9, plateNoted: false, manhuntArrest: false, oneCase: false }),
  loaded() {
    G.hooks.custody = custody;
    S.beat = S.chase = S.carChase = null;
  },
  step(dt) {
    if (G.paused) return;
    spotStep();
    watchedStep();
    beatStep(dt);
    chaseStep(dt);
    carChaseStep(dt);
  },
  minute() {
    const x = X('law');
    ellisSigns();
    x.watched = x.watched.filter((w) => w.untilT > G.t);
    if (x.ellisDue && G.t >= x.ellisDue.t) {
      ellisEvent(x.ellisDue.what); // a body: DS Ellis the next morning (A36)
      x.ellisDue = null;
    }
    const was = x.edge;
    x.edge = L.onEdge(x.deeds, 'Quay Street', G.t).onEdge;
    if (x.edge && !was) {
      tell('Quay Street has changed. Doors are locked that stood open, and somebody is at every other window.', '');
      write('Quay Street is on edge: three things seen in two days. Doors locked early, windows watched, the constable round twice as often.', { key: 'edge' + dayNow(), how: 'Saw it himself' });
    }
    // a manhunt: its sign shows at least a game hour before an arrest can land (ER-POL-05)
    if (L.manhuntArrest(x.ellis, G.t) && !G.story.arrest && !x.manhuntArrest) {
      x.manhuntArrest = true;
      G.story.arrest = { e: null, violent: true, offence: x.charges.some((c) => c.offence === 'killing') ? 'killing' : 'wounding', due: G.t, by: [] };
    }
  },
  hourly() {
    officeSearchStep();
  },
  hook: {
    x: () => X('law'),
    ellis: () => X('law').ellis,
    ellisEvent,
    custody: (offence, o) => L.custody(offence, o),
    buy,
    useBought,
    patrolAt,
    patrolSees,
    trafficStop,
    watchedNear,
    beat: () => S.beat,
    chase: () => S.chase,
    carChase: () => S.carChase,
    challenge: (cause) => challenge(P_('pc'), cause || { carryingAtNight: true }, carried()),
  },
});
// every seen crime counts toward a street on edge; a reported one brings an officer to its spot
on('act', (E) => {
  const k = KINDS[E.kind];
  if (!k || k.crime < 1) return;
  X('law').deeds.push({ street: /Quay Street/.test(E.zone) ? 'Quay Street' : E.zone, seen: (E.wit || []).length > 0 || (E.party || []).length > 0, t: G.t, e: E.id });
  if (X('law').deeds.length > 60) X('law').deeds.shift();
});
// a deed is reported when a walk to the phone box ends: an officer to the spot; a killing somebody saw moves DS Ellis
on('walks.told', ({ e, aftermath }) => {
  const E = G.ev[e];
  if (!E) return;
  afterDeed(E, E.kind === 'kill');
  if (E.kind === 'kill' && !aftermath) ellisEvent('witnessed killing');
});
on('town.hour', (h) => {
  const x = X('law');
  if (h.ellis) ellisEvent(h.ellis === 'talk' ? 'talk' : 'detective crime reported');
  if (h.taken && !G.story.arrest) {
    // the real town's ten o'clock: he is taken for the damage. The prototype plays the scene; the hours are the offence's.
    const d = (G.x.town.deeds.find((q) => q.deed) || {}).e;
    if (!(d && x.takenFor[d]) && d && (G.ev[d].stmt || []).length) G.story.arrest = { e: d || null, violent: false, offence: 'damage', due: G.t, by: G.x.town.went.map((w) => w.who), town: h.taken };
  }
});
on('crime.holdup', ({ e, r }) => {
  const E = G.ev[e];
  if (r.reported) {
    afterDeed(E, false);
    ellisEvent('detective crime reported');
    // a robbery with a witness at face distance: a statement next morning, twelve hours if he is taken for it
    G.story.arrest = G.story.arrest || { e, violent: true, offence: 'robbery', due: (dayNow() + 1) * 1440 + T.robberyStatementNextDayAtHour * 60, by: [] };
  }
});
on('cars.reckless', ({ why, x, z }) => {
  if (L.stop({ hit: why === 'hit', onPavement: why === 'pavement', speed: Math.abs(G.car.v), inOfficersSight: patrolSees(x, z) }).stops) trafficStop(why);
});
// Act II: DS Ellis joins the street crimes to the fire. From then every arrest is part of one case.
on('acts.beat', ({ id }) => {
  if (id !== 'oneCase') return;
  X('law').oneCase = true;
  sign('ellis', 'DS Ellis has the fire and the street crimes in one file now. Nothing of his will be treated as small again.');
});
