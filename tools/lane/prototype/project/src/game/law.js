// LEDGER, the whole game: the system "law". The police as a pressure he can read and answer, never the end of the
// game (DESIGN 8; A12, A13, A36, A37; parts 2.6.1 to 2.6.10, 2.5.4). The real town code decides who goes to the
// police over the week's damage, DS Ellis's mornings and the arrest for it; the prototype's own rule still decides
// statements about violence (the gap is in ONE-SHOT-SIM-DIFFERENCES.md). This file adds what the design adds
// around them: the nightly beat and its challenge with three answers, the hours each offence costs, DS Ellis's
// four stages each with its sign, the office searched with notice, traffic stops, bought men, an officer at the
// spot after a reported deed, and a street on edge. The rules are pieces/law.js.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on, tomXZ } from './core.js';
import { G } from '../state.js';
import { hyp, quid } from '../util.js';
import { act, logLine } from '../events.js';
import { pay } from '../money.js';
import { choose, scene, say } from '../ui.js';
import { goToPoint } from '../routines.js';
import { KINDS } from '../kinds.js';
import { sense, tomTarget } from '../seeing.js';
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
  const c = L.custody(offence, { ownedUp: !ran && offence === 'damage' && !x.charges.length, first: !x.charges.length && !x.cautions, woreCoat: G.tom.coat });
  const hours = c.gameHours + (ran ? RULES.police.heldGameHoursAddedIfHeRan : 0);
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
function beatStep(dt) {
  const P = P_('pc'),
    t = G.tom,
    x = X('law'),
    st = G.story;
  const busy = (st.job && st.job.watch && st.job.watch.st !== 'over') || st.arrest || S.chase;
  const visits = L.onEdge(x.deeds, 'Quay Street', G.t).beatVisitsTimes;
  const on_ = night() && !busy && !P.dead && (visits > 1 || Math.floor(G.t / 60) % 2 === 0); // every other hour; every hour on a street on edge
  if (!on_) {
    if (S.beat && !busy) {
      P.override = { where: 'off', act: 'idle' };
      P.goalKey = '';
    }
    return void (S.beat = null);
  }
  if (!S.beat) {
    S.beat = { leg: 0, warned: false };
    Object.assign(P, { override: null, gone: false, space: 'street', awake: true, x: T.beatEnds[0][0], z: T.beatEnds[0][1], route: null, hold: false });
    goToPoint(P, T.beatEnds[1][0], T.beatEnds[1][1], T.beatWalkMetresPerSecond);
  }
  const to = T.beatEnds[1 - S.beat.leg];
  if (hyp(P.x, P.z, to[0], to[1]) < 2 || !P.route) {
    S.beat.leg = hyp(P.x, P.z, to[0], to[1]) < 2 ? 1 - S.beat.leg : S.beat.leg;
    const nx = T.beatEnds[1 - S.beat.leg];
    goToPoint(P, nx[0], nx[1], T.beatWalkMetresPerSecond);
  }
  if (t.space !== 'street' || t.inCar || G.paused) return;
  const d = hyp(P.x, P.z, t.x, t.z);
  // he is heard or seen before he can challenge (ER-POL-02)
  if (d < T.beatHeardWithinMetres && !S.beat.warned) {
    S.beat.warned = true;
    S.heard = G.played;
    tell('Measured footsteps on the wet. The constable is on his beat.', '');
  }
  if (d > T.beatHeardWithinMetres * 1.5) S.beat.warned = false;
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
  const weak = !cause.weaponShown && !cause.bloodied && !items.some((i) => i.unlawful) && !t.carry;
  const bought = x.bought.harker && x.bought.harker.paid;
  const i = await scene(() => choose('pc', '"You there. Stand still a minute. What have you got on you?"', ['Stand and be searched.', 'Run.', 'A word.']));
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
    await scene(() => say('pc', r.keeps.length ? `I will keep ${r.finds.filter((f) => r.keeps.includes(f.id)).map((f) => f.name).join(' and ')}. And your name, sir. I am writing it down.` : 'Right. On your way, then. It is late to be about.'));
    write(r.keeps.length ? `Searched by the constable on Quay Street. He kept ${r.finds.filter((f) => r.keeps.includes(f.id)).map((f) => f.name).join(' and ')}, and wrote the name down.` : 'Searched by the constable on Quay Street. He found nothing to keep.', { how: 'Did it', kind: 'note' });
    if (r.keeps.length) ellisEvent('talk');
  } else if (r.result === 'talked round') {
    act('talked_round', { silent: true, told: ['pc'] });
    await scene(() => say('pc', 'Aye, well. Get yourself home.'));
  } else if (r.result === 'a chase') {
    S.chase = { seconds: 0, unseen: 0 };
    act('ran_police', { noiseR: RULES.police.runningNoiseMetres });
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
  c.unseen = los ? 0 : c.unseen + dt;
  if (los && (!P.route || c.seconds % 1 < dt)) goToPoint(P, t.x, t.z, T.constableRunsMetresPerSecond);
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
    x.watched.push({ x: Math.round(t.x), z: Math.round(t.z), untilT: G.t + RULES.game.foot.constableLooksRoundGameMinutes, why: 'the constable lost him here' });
    tell('He has lost him. The constable will stand about that corner for an hour.', '');
    write('Ran from the constable on Quay Street and lost him. He saw a man; whether he saw a face is another thing.', { how: 'Did it' });
    ellisEvent('talk');
  }
}
// ---- police after a deed (A36): an officer at the spot, the ground watched until morning ----
function afterDeed(E, body) {
  const x = X('law');
  const r = L.afterDeed({ reported: true, body });
  x.watched.push({ x: E.x, z: E.z, untilT: (dayNow() + (hourNow() >= r.watchedUntilHour ? 1 : 0)) * 1440 + r.watchedUntilHour * 60, why: KINDS[E.kind].mine(E), tape: r.tape, e: E.id });
  logLine('An officer went to the spot: ' + KINDS[E.kind].truth(E), 'police');
  if (r.ellisNextMorning) ellisEvent('body');
}
export const watchedNear = (x, z) => X('law').watched.find((w) => w.untilT > G.t && hyp(w.x, w.z, x, z) < T.challengeWithinMetres * 2) || null;
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
  fresh: () => ({ ellis: { stage: 0, signShown: true, signShownT: null, owed: null }, charges: [], cautions: 0, arrests: [], takenFor: {}, watched: [], deeds: [], edge: false, bought: {}, search: { noticeT: null, done: false, found: [] }, challengedT: -1e9, challenges: [], chases: [], stops: [], carChases: [], stoppedT: -1e9, plateNoted: false, manhuntArrest: false }),
  loaded() {
    G.hooks.custody = custody;
    S.beat = S.chase = S.carChase = null;
  },
  step(dt) {
    if (G.paused) return;
    beatStep(dt);
    chaseStep(dt);
    carChaseStep(dt);
  },
  minute() {
    const x = X('law');
    ellisSigns();
    x.watched = x.watched.filter((w) => w.untilT > G.t);
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
  if (E.kind === 'kill') {
    afterDeed(E, true);
    ellisEvent((E.wit || []).length ? 'witnessed killing' : 'body');
  }
});
on('town.hour', (h) => {
  const x = X('law');
  if (h.went.length) {
    const d = (G.x.town.deeds.find((q) => q.deed) || {}).e;
    if (d && G.ev[d]) afterDeed(G.ev[d], false);
  }
  if (h.ellis) ellisEvent(h.ellis === 'talk' ? 'talk' : 'detective crime reported');
  if (h.taken && !G.story.arrest) {
    // the real town's ten o'clock: he is taken for the damage. The prototype plays the scene; the hours are the offence's.
    const d = (G.x.town.deeds.find((q) => q.deed) || {}).e;
    if (!(d && x.takenFor[d])) G.story.arrest = { e: d || null, violent: false, offence: 'damage', due: G.t, by: G.x.town.went.map((w) => w.who), town: h.taken };
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
