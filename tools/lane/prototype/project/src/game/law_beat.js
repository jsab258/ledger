// LEDGER, the system "law": the beat constable (DESIGN section 8; addendum A3, A13, A36, A37).
// He walks Quay Street and the quay at night. He is heard or seen 3 s before he can challenge, and he calls out
// before he acts (ER-POL-02). Stand, and he searches: what he finds he keeps. Have a word, offer a note, or run:
// a chase that is lost once Tom is unseen for 7 s or 70 m clear, and always ends inside 90 s (ER-POL-04). After
// losing him he walks to where he last saw him and looks round a while (A3). The carry's own constable (jobs.js)
// keeps the nights a bag is being carried; this one keeps every other night.
import { G, day, hour } from '../state.js';
import { hyp } from '../util.js';
import { emit } from './core.js';
import { RULES } from '../rules.js';
import { act, logLine } from '../events.js';
import { note } from '../ledger.js';
import { sense, tomTarget } from '../seeing.js';
import { goToPoint } from '../routines.js';
import { zoneAt } from '../map.js';
import { sub, say, choose, scene, ui, tomName } from '../ui.js';
import { F } from '../fight.js';
import { record } from '../police.js';
import { PIECE as BEAT } from './pieces/police_beat.js';
import { PIECE as TOWN } from './pieces/law_town.js';

const LAW = RULES.game.law,
  B = LAW.beat;
const { cause, mayChallenge, search, word } = BEAT.fns;
const inPlay = () => G.story.phase === 'play' && !G.paused && !ui.modal;
const fl = () => G.story.flags;
let forced = null; // a test may hold the beat on or off

const officerId = () => (day() % 2 === 1 && G.people.pashby && !G.people.pashby.dead ? 'pashby' : 'pc');
const nightNow = (h = hour()) => h >= B.fromHour || h < B.untilHour;
function wantedOut(x) {
  if (forced != null) return forced;
  const st = G.story;
  if (st.arrest && (st.arrest.st || G.t >= st.arrest.due - 30)) return false; // he is about an arrest
  if (st.job && st.job.watch && st.job.watch.st !== 'over') return false; // the carry's own constable has the night
  if (x.beat.detour || x.beat.stopSearch) return true;
  const h = hour();
  if (nightNow(h)) return true;
  // a street on edge is walked more often: from early evening, and once round at dinner time (A37)
  if (Object.keys(x.edge || {}).length) return h >= 18 || (h >= 12 && h < 13.5);
  return false;
}
// what he could hold against Tom, as far as a man on the street can see it
export function causeNow(x) {
  const t = G.tom,
    crime = G.x.crime || {},
    carried = Array.isArray(crime.carried) ? crime.carried : [],
    px = t.inCar ? G.car.x : t.x,
    pz = t.inCar ? G.car.z : t.z;
  const c = cause({
    night: nightNow(),
    carrying: (!!t.carry && t.carry !== 'suitcase') || carried.some((it) => it && (it.big || it.hand)),
    running: !!t.run && t.v > 3,
    bloodied: t.hurt > 0.45 || !!t.bloody,
    weaponInHand: !!t.armed,
    trespass: !!(G.x.foot && G.x.foot.trespass),
  });
  const spot = (x.spots || []).find((s) => G.t >= s.from && G.t < s.until && hyp(px, pz, s.x, s.z) < LAW.spot.watchedWithinMetres);
  if (spot) c.why.push('back where it happened');
  if (x.beat.stopSearch) c.why.push('stop and search');
  c.cause = c.why.length > 0;
  return c;
}
function bring(P, x, z) {
  // on his beat by this system's doing, not by his week: held, so the routine leaves him to it
  P.override = { where: 'off', act: 'idle', beat: 1 };
  P.gone = false;
  P.space = 'street';
  P.awake = true;
  P.x = x;
  P.z = z;
  P.route = null;
  P.hold = true;
}
function sendOff(P) {
  if (!P) return;
  P.mark = null;
  P.hurry = 1;
  P.hold = false;
  P.override = { where: 'off', act: 'idle' };
  P.goalKey = '';
}
export function beatLoaded(x) {
  x.beat = { st: 'off', leg: 0, heard: 0 };
  forced = null;
}
export function beatStep(dt, x) {
  const b = x.beat;
  if (!b.st) Object.assign(b, { st: 'off', leg: 0, heard: 0 });
  if (G.story.phase !== 'play') return;
  const out = wantedOut(x);
  if (b.st === 'off') {
    if (!out) return;
    b.officer = officerId();
    const P = G.people[b.officer];
    if (!P || P.dead) return;
    const p0 = b.detour ? [RULES.police.arrivesAtXMetres, RULES.police.arrivesAtZMetres] : B.points[0];
    bring(P, p0[0], p0[1]);
    Object.assign(b, { st: 'walk', leg: 1, heard: 0, said: 0, t: 0 });
    logLine(`${P.def.name} came on to his beat`, 'police');
    return;
  }
  const P = G.people[b.officer],
    t = G.tom;
  if (!P || P.dead) return (b.st = 'off');
  if (b.st === 'scene') return;
  if (!out && (b.st === 'walk' || b.st === 'look')) {
    // called away. If the same man is wanted for an arrest or for the carry's own beat, they have him now: leave him be
    const st = G.story,
      taken = b.officer === 'pc' && ((st.arrest && st.arrest.st) || (st.job && st.job.watch && st.job.watch.st !== 'over'));
    if (!taken) sendOff(P);
    b.st = 'off';
    return;
  }
  const street = t.space === 'street',
    tx = t.inCar ? G.car.x : t.x,
    tz = t.inCar ? G.car.z : t.z,
    d = street && P.space === 'street' ? hyp(P.x, P.z, tx, tz) : 999,
    s = street ? sense(P, tomTarget()) : { see: false },
    seen = s.see && d < B.seesWithinMetres;
  // heard or seen: his boots carry, and he is there to be looked at
  if (d < B.heardWithinMetres) {
    b.heard += dt;
    if (!b.said && inPlay() && !G.paused) {
      b.said = 1;
      sub('Boots on the setts. A constable on his beat, coming along the street.', '', 'over', 4);
      emit('police:heard', { officer: b.officer, metres: d });
    }
  } else {
    b.heard = 0;
    if (d > B.heardWithinMetres + 25) b.said = 0;
  }
  if (b.st === 'walk') {
    b.t += dt;
    const to = b.detour ? [b.detour.x, b.detour.z] : B.points[b.leg % B.points.length];
    if (b.stand) {
      P.ang = Math.atan2(tx - P.x, tz - P.z); // a test has stood him here, facing Tom
    } else if (hyp(P.x, P.z, to[0], to[1]) < B.turnsWithinMetres) {
      if (!b.detour) {
        b.leg = (b.leg + 1) % B.points.length;
        const nx = B.points[b.leg];
        goToPoint(P, nx[0], nx[1], B.walkMetresPerSecond);
      }
    } else if (!P.route || b.t > 4) {
      b.t = 0;
      if (!P.route) goToPoint(P, to[0], to[1], B.walkMetresPerSecond);
    }
    if (G.t < (b.restUntil || 0) || t.inCar || !inPlay() || F.on) return;
    const c = causeNow(x);
    if (c.cause && seen && d < B.callsOutWithinMetres && mayChallenge(b.heard, false).callOut) callOut(P, b, c);
    return;
  }
  if (b.st === 'called') {
    b.called += dt;
    b.look = (b.look || 0) - dt;
    const moved = hyp(tx, tz, b.at.x, b.at.z);
    if (!street || t.inCar || t.run || moved > 6 || d > B.callsOutWithinMetres + 10) return startChase(P, b);
    if (b.look <= 0) {
      b.look = 1.2;
      goToPoint(P, tx, tz, B.walkMetresPerSecond * 1.2);
    }
    if (mayChallenge(b.heard + b.called, true).act && b.called >= B.actsAfterCallingRealSeconds && d < B.speaksWithinMetres && inPlay() && !F.on) challenge(P, b, x);
    return;
  }
  if (b.st === 'chase') {
    b.ct += dt;
    b.look = (b.look || 0) - dt;
    const los = street && d < RULES.police.seesHimWithinMetres && G.env.los(P.x, P.z, tx, tz);
    b.lost = los ? 0 : b.lost + dt;
    if (los) b.last = { x: tx, z: tz };
    if (b.look <= 0) {
      b.look = RULES.police.looksAgainWhenChasingEveryRealSeconds;
      if (los) goToPoint(P, tx, tz, B.chaseMetresPerSecond);
    }
    if (d < B.catchesWithinMetres && street && !t.inCar && inPlay()) {
      b.chases = (b.chases || []).concat([{ end: 'caught', seconds: Math.round(b.ct * 10) / 10 }]).slice(-20);
      return searchScene(P, b, x, true);
    }
    if (b.lost > B.losesHimAfterRealSecondsUnseen || d > B.losesHimBeyondMetres || b.ct > B.chaseEndsWithinRealSeconds - 2) {
      b.chases = (b.chases || []).concat([{ end: 'lost', seconds: Math.round(b.ct * 10) / 10 }]).slice(-20);
      act('ran_police', { zone: zoneAt(t.x, t.z), noiseR: RULES.police.runningNoiseMetres });
      fl().ranBeat = (fl().ranBeat || 0) + 1;
      P.mark = null;
      // A3: he walks to the last place he saw him and looks round about a game hour, so the law stays near
      b.st = 'look';
      b.lookLeft = Math.min(30, (B.looksRoundAfterLosingGameMinutes * RULES.time.realSecondsPerGameHour) / 60);
      const l = b.last || b.at;
      goToPoint(P, l.x, l.z, B.walkMetresPerSecond * 1.3);
      b.restUntil = 0;
      b.heard = 0;
      if (inPlay()) sub('You have lost him. He will walk back to where he last saw you, and look round a while.', '', 'over', 6);
      note('Ran from a constable on ' + zoneAt(t.x, t.z) + '. Lost him. He saw a man run; whether he saw a face is another matter.', 'police', null, { how: 'Did it' });
      emit('police:chase', { end: 'lost', seconds: b.ct });
    }
    return;
  }
  if (b.st === 'look') {
    b.lookLeft -= dt;
    if (seen && d < B.callsOutWithinMetres && mayChallenge(b.heard, false).callOut && inPlay() && !t.inCar) return callOut(P, b, { cause: true, why: ['ran from him'] });
    if (b.lookLeft <= 0) {
      b.st = 'walk';
      b.t = 9;
      b.restUntil = G.t + B.restsBetweenChallengesGameMinutes;
    }
  }
}
function callOut(P, b, c) {
  const t = G.tom;
  b.st = 'called';
  b.called = 0;
  b.cause = c;
  b.at = { x: t.x, z: t.z };
  P.mark = '!';
  P.ang = Math.atan2(t.x - P.x, t.z - P.z);
  goToPoint(P, t.x, t.z, B.walkMetresPerSecond * 1.2);
  sub('"You there. Stand where you are a minute." Stand and wait for him, or run [Shift].', tomName(P), 'over', 5);
  logLine(`${P.def.name} called out to Tom (${c.why.join(', ')})`, 'police');
  emit('police:called', { officer: P.id, why: c.why, heardForRealSeconds: b.heard });
}
function startChase(P, b) {
  b.st = 'chase';
  b.ct = 0;
  b.lost = 0;
  b.look = 0;
  b.last = { x: G.tom.x, z: G.tom.z };
  P.hurry = RULES.police.chaseHurry;
  G.tom.noiseP = Math.max(G.tom.noiseP, RULES.police.runningNoiseMetres);
  sub('"Oi! Stop!" A whistle behind you.', tomName(P), 'over', 4);
  logLine('Tom ran from ' + P.def.name, 'police');
}
async function challenge(P, b, x) {
  b.st = 'scene';
  P.route = null;
  P.hold = true;
  const c = b.cause || { cause: false, why: [] },
    pence = G.money.clean + G.money.dirty,
    opts = ['Stand and let him look.', 'Have a word with him.'],
    noteAt = pence >= LAW.bought.pashbyPricePence ? opts.push('Offer him a note.') - 1 : -1,
    runAt = opts.push('Run.') - 1;
  const i = await scene(async () => {
    await say(P.id, P.id === 'pashby' ? "Now then, son. Where are we off to at this hour?" : 'Stand still, sir. Where are you going at this time of night?');
    return choose(P.id, c.why.includes('stop and search') ? 'Everybody is being stopped this week. Turn your pockets out.' : "I'll have a look at what you've got on you.", opts);
  });
  if (i === runAt) return startChase(P, b);
  let w = { ends: 'search', crime: false };
  if (i === 1) w = word(P.id, c.cause && !c.why.every((y) => y === 'stop and search' && false), false, 0);
  if (i === noteAt) {
    const used = x.bought.pashby.night === day() ? x.bought.pashby.used : 0;
    w = word(P.id, c.cause, true, used);
    if (w.ends === 'looks away') {
      const r = G.hooks.lawBuyOfficer ? G.hooks.lawBuyOfficer('pashby', 'car') : { does: false };
      if (!r.does) w = { ends: 'search', crime: false };
    }
  }
  b.lastWord = w.ends;
  if (w.ends === 'talked round') {
    await scene(() => say(P.id, P.id === 'pashby' ? "Aye, well. Get yourself home, son." : 'Very good, sir. Mind how you go.'));
    return done(P, b);
  }
  if (w.ends === 'looks away') {
    await scene(() => say(P.id, 'I never stopped anybody tonight. Go on. Once, mind.'));
    note('PC Pashby took a note and looked the other way. Once a night, he says.', 'police', 'pashby' + day(), { who: 'pashby', how: 'Did it' });
    return done(P, b);
  }
  if (w.ends === 'arrest') {
    // a note offered to an honest officer is a crime he saw: he writes it down, and searches all the same
    const E = act('law_note_offered', { target: P.id, told: [P.id] });
    E.officerSaw = true;
    record(E, [], 'an officer saw it');
    await scene(() => say(P.id, "Put that away, sir. I'll be writing that down as well. Now. Pockets."));
  }
  return searchScene(P, b, x, false);
}
async function searchScene(P, b, x, ran) {
  b.st = 'scene';
  P.route = null;
  P.hold = true;
  const r = doSearch(P, x, ran);
  await scene(async () => {
    await say(P.id, ran ? "Nobody runs from me for nothing. Let's see it." : "Let's have a look, then.");
    await say(P.id, r.found.length ? `${cap(listWords(r.found))}. I'll keep ${r.found.length > 1 ? 'those' : 'that'}. Name? I'll be writing it down.` : "Nothing. Then you'll not mind me asking again another night. Go on.");
  });
  done(P, b);
}
const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
const listWords = (a) => (a.length > 1 ? a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1] : a[0] || '');
const nameOf = (it) => (typeof it === 'string' ? it : (it && (it.name || it.id)) || 'a thing');
// A search finds exactly what is under the coat and in the hand, and he keeps it.
export function doSearch(P, x, ran) {
  const t = G.tom,
    crime = G.x.crime || {},
    carried = Array.isArray(crime.carried) ? crime.carried.map(nameOf) : [];
  if (t.weapon) carried.push('a ' + t.weapon);
  const hand = t.carry && t.carry !== 'suitcase' ? (t.carry === 'bag' ? 'the bag' : nameOf(t.carry)) : null;
  const r = search(carried, hand);
  if (Array.isArray(crime.carried)) crime.carried = [];
  t.weapon = null;
  t.armed = false;
  if (hand) {
    t.carry = null;
    const j = G.story.job;
    if (j && j.carrying) {
      j.carrying = false;
      j.st = 'lost';
      fl()['job' + j.n] = 'lost';
    }
  }
  const E = act('law_searched', { zone: zoneAt(t.x, t.z), what: listWords(r.kept), told: [P.id], noiseR: ran ? RULES.police.runningNoiseMetres : 0 });
  if (r.kept.length)
    note(`${P.def.name} stopped Tom on ${E.zone} and kept ${listWords(r.kept)}. He wrote the name down.`, 'police', null, { how: 'Did it', ev: E.id });
  x.beat.searches = (x.beat.searches || 0) + 1;
  x.beat.lastSearch = { found: r.found, kept: r.kept, ran: !!ran, officer: P.id, t: Math.round(G.t) };
  x.beat.stopSearch = 0;
  emit('police:search', { found: r.found, officer: P.id, ran: !!ran });
  return r;
}
function done(P, b) {
  P.mark = null;
  P.hurry = 1;
  b.st = 'walk';
  b.t = 9;
  b.heard = 0;
  b.restUntil = G.t + B.restsBetweenChallengesGameMinutes;
  if (G.hooks.save) G.hooks.save();
}
export const beatHook = {
  state: () => G.x.law.beat,
  officer: officerId,
  cause: () => causeNow(G.x.law),
  force(on) {
    forced = on;
  },
  // put the night's officer on the street this far from Tom, walking his beat (a test stages the meeting)
  place(metres = 20) {
    const x = G.x.law,
      b = x.beat,
      t = G.tom;
    forced = true;
    b.officer = officerId();
    const P = G.people[b.officer];
    bring(P, t.x, t.z - metres);
    P.ang = 0;
    Object.assign(b, { st: 'walk', leg: 1, heard: 0, said: 0, t: 0, restUntil: 0, stand: 1 });
    P.route = null;
    return b.officer;
  },
  search: (ran) => doSearch(G.people[G.x.law.beat.officer || officerId()], G.x.law, !!ran),
  boughtDoes: TOWN.fns.boughtDoes,
};
