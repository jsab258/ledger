// LEDGER, the whole game: the system "law". Witnesses who walk to tell, and the police (DESIGN sections 2 and 8;
// addendum A3, A13, A36, A37, A38). A pressure Tom can read and answer, never the end of the game.
//
// One road: everything that reaches the police goes through police.js record(), whoever decided it: a witness's
// walk ending here, the night's run for those who slept on it, or the real town's morning ('town:hour').
// The saved state is G.x.law: stage (0 nothing, 1 asking round, 2 investigating, 3 a manhunt), signs, case
// ({ charges, statements, officeFinds, strength }, read by the endings), walks, spots, bodies, bought.
import { G, day, hour } from '../state.js';
import { hyp, clamp, pounds, DAYS } from '../util.js';
import { register, on, emit, X } from './core.js';
import { RULES } from '../rules.js';
import { KINDS } from '../kinds.js';
import { act, mkEvent, remember, logLine } from '../events.js';
import { tell } from '../gossip.js';
import { note } from '../ledger.js';
import { sense, tomTarget, tomNotices, attached } from '../seeing.js';
import { send, goToPoint } from '../routines.js';
import { SPOTS, zoneAt } from '../map.js';
import { sub, news, ui, tomName } from '../ui.js';
import { pay } from '../money.js';
import { record, wouldState, classOf, startEllis } from '../police.js';
import { PIECE as STATEMENT } from './pieces/law_statement.js';
import { PIECE as STAGES } from './pieces/law_stages.js';
import { PIECE as TOWN } from './pieces/law_town.js';
import { beatStep, beatHook, beatLoaded } from './law_beat.js';

const LAW = RULES.game.law,
  WALK = LAW.walk,
  REACT = LAW.reaction;
const { stopWitness, walkTo, walkLasts } = STATEMENT.fns;
const { wanted, advance, manhuntMayArrest, ellisComes, caseStrength } = STAGES.fns;
const { onEdge, finder, missingAsked, response } = TOWN.fns;

const fresh = () => ({
  stage: 0,
  signs: [], // { stage, t, shown, why }
  case: { charges: [], statements: 0, officeFinds: 0, strength: 0 },
  taken: {}, // event id -> 1: never twice for one deed
  reported: {}, // event id -> who stated
  turned: {}, // 'event:person' -> the answer that stopped her
  lost: {}, // 'event:person' -> 1: a statement lost at the station
  walks: [], // { id, e, who, st, startAt, to, tx, tz, realLeft, landBy, inSight }
  nextWalk: 1,
  lastE: 0, // the last event looked at
  deeds: {}, // street -> game minutes of its seen deeds (A37)
  edge: {}, // street -> on edge since
  spots: [], // { e, x, z, zone, from, until, body, armed, said }
  traces: [], // unseen deeds with a trace: { e, x, z, zone, t, hidden, sunk, found }
  bodies: [], // { id, e, x, z, t, hidden, sunk, found }
  missing: {}, // person id -> { since, asked }
  quiet: {}, // person id -> talks quieter until this game minute
  bought: { pashby: { paid: 0, used: 0, night: -1 }, thwaite: { paid: 0, used: 0 }, seen: [] },
  office: { noticeT: null, done: false, found: [] },
  ellisAsked: 0,
  ran: 0,
  hunted: 0,
  live: false,
  armed: { calls: 0, stops: 0, lastStopT: -1e9 },
  beat: {},
});
const L = () => X('law');
const inPlay = () => G.story.phase === 'play' && !G.paused && !ui.modal;
const personOf = (id) => G.people[id];
const tomXZ = () => (G.tom.inCar ? [G.car.x, G.car.z] : [G.tom.x, G.tom.z]);
const mins = (m) => Math.round(m);
const kindOf = (E) => KINDS[E.kind] || { crime: 0, sev: 0, val: 0 };

// ---------- the walk: a witness who means to tell sets off, and is seen going ----------
function friendNear(P) {
  let best = null,
    bd = 1e9;
  for (const id of P.def.close || []) {
    const F = personOf(id);
    if (!F || F.dead || F.gone || F.space !== 'street' || F.def.police) continue;
    const d = hyp(P.x, P.z, F.x, F.z);
    if (d < bd) {
      bd = d;
      best = F;
    }
  }
  return best ? { F: best, d: bd } : null;
}
export function startWalk(P, E, soonerTimes = 1) {
  const x = L();
  if (x.walks.some((w) => w.e === E.id && w.who === P.id)) return null;
  const fr = P.space === 'street' ? friendNear(P) : null,
    to = walkTo({ friendNearMetres: fr ? fr.d : null, friendWithinMetres: WALK.friendWithinMetres, crime: kindOf(E).crime });
  const w = {
    id: x.nextWalk++,
    e: E.id,
    who: P.id,
    st: 'pending',
    startAt: G.t + (WALK.setsOffAfterRealSeconds * soonerTimes * 60) / RULES.time.realSecondsPerGameHour,
    to,
    friend: to === 'friend' ? fr.F.id : null,
    realLeft: 0,
    landBy: G.t + WALK.landsAnywayAfterGameMinutes,
    inSight: false,
  };
  x.walks.push(w);
  return w;
}
function target(w) {
  if (w.to === 'friend') {
    const F = personOf(w.friend);
    if (F && !F.gone && F.space === 'street') return [F.x, F.z];
    w.to = 'phone';
  }
  const s = w.to === 'station' ? SPOTS.station : SPOTS.phone;
  return [s[0], s[1]];
}
function setOff(w) {
  const P = personOf(w.who),
    E = G.ev[w.e];
  if (!P || !E || P.dead) return (w.st = 'dropped');
  if (!wouldState(P, E).goes) return (w.st = 'dropped'); // she has thought better of it since
  w.st = 'walking';
  const [tx, tz] = tomXZ();
  const near = P.space === G.tom.space && hyp(P.x, P.z, tx, tz) < WALK.startsInSightWithinMetres;
  w.inSight = near && (tomNotices(P) || G.env.los(tx, tz, P.x, P.z));
  w.realLeft = walkLasts(0, w.inSight, WALK, !!G.settings.longWalks);
  P.lawWalk = w.id;
  if (w.to === 'friend') {
    const [x, z] = target(w);
    goToPoint(P, x + 0.8, z + 0.5);
  } else send(P, w.to === 'station' ? 'station' : 'phone', 'idle', w.landBy + 30);
  if (w.inSight && inPlay()) {
    const where = w.to === 'station' ? 'up the street towards the station' : w.to === 'friend' ? 'across to ' + tomName(personOf(w.friend)) : 'towards the phone box';
    sub(`${tomName(P)} has seen enough, and is walking off ${where}.`, '', 'over', 5);
    w.said = 1;
  }
  logLine(`${P.def.name} set off to tell (${w.to}) about: ${KINDS[E.kind].truth(E)}`, 'police');
  emit('witness:walk', { who: P.id, E, to: w.to, inSight: w.inSight });
}
function land(w, how) {
  const P = personOf(w.who),
    E = G.ev[w.e];
  w.st = 'landed';
  w.landedT = mins(G.t);
  if (P) {
    P.lawWalk = null;
    if (P.override && (P.override.where === 'phone' || P.override.where === 'station')) P.override = null;
    P.hold = false;
  }
  if (!P || !E || !wouldState(P, E).goes) return (w.st = 'dropped');
  record(E, [P.id], how || (w.to === 'station' ? 'at the station desk' : 'from the phone box'));
  if (inPlay() && P.space === G.tom.space && tomNotices(P))
    sub(`${tomName(P)} is in the phone box with the door shut. That is on record now.`, '', 'over', 5);
}
function stepWalks(dt) {
  const x = L();
  for (const w of x.walks) {
    if (w.st === 'pending' && G.t >= w.startAt) setOff(w);
    if (w.st !== 'walking') continue;
    const P = personOf(w.who);
    if (!P || P.dead) {
      w.st = 'dropped';
      continue;
    }
    w.realLeft -= dt;
    const [x2, z2] = target(w),
      there = P.space === 'street' && hyp(P.x, P.z, x2, z2) < WALK.arrivesWithinMetres + (w.to === 'friend' ? 1.2 : 0);
    if (w.to === 'friend' && there) {
      // told to a friend first: that is the street's talk, and then the phone box
      const F = personOf(w.friend),
        m = P.mind.by[w.e];
      if (F && m) tell(P, F, m, zoneAt(P.x, P.z));
      w.to = 'phone';
      P.hold = false;
      send(P, 'phone', 'idle', w.landBy + 30);
      continue;
    }
    if (w.to === 'friend' && !P.route && !P.moving) goToPoint(P, x2 + 0.8, z2 + 0.5);
    if ((there && w.realLeft <= 0) || G.t >= w.landBy) land(w);
  }
  if (x.walks.length > 60) x.walks = x.walks.filter((w) => w.st === 'pending' || w.st === 'walking').concat(x.walks.filter((w) => w.st !== 'pending' && w.st !== 'walking').slice(-30));
}
const walkOf = (P) => L().walks.find((w) => w.who === P.id && (w.st === 'pending' || w.st === 'walking'));

// Stopping a witness (DESIGN section 2): reach her first and talk her round, pay, threaten, help, or let her go.
// A threat can stop a report to the police, never the street's talk.
export function stopWalk(P, answer) {
  const x = L(),
    w = walkOf(P);
  if (!w) return null;
  const E = G.ev[w.e],
    d = P.def;
  const r = stopWitness(
    answer,
    { regard: P.mind.regard, venal: d.venal == null ? 0.3 : d.venal, nerve: d.nerve == null ? 0.5 : d.nerve },
    LAW.stop,
    G.money.clean + G.money.dirty,
    kindOf(E).crime,
  );
  if (r.cost) pay(r.cost, false, 'a witness paid to keep quiet');
  P.mind.fear = clamp(P.mind.fear + r.fear, 0, 1);
  P.mind.regard = clamp(P.mind.regard + r.regard, -1, 1);
  if (answer === 'pay' && !r.police) {
    P.mind.bought = true;
    act('law_paid_witness', { target: P.id });
  } else if (answer === 'threat') act('threat', { target: P.id });
  else if (answer === 'help') act('law_helped_witness', { target: P.id });
  else if (answer === 'round' && !r.police) act('law_turned_witness', { target: P.id });
  w.answer = answer;
  w.why = r.why;
  if (!r.police) {
    w.st = 'stopped';
    x.turned[w.e + ':' + P.id] = answer;
    P.lawWalk = null;
    if (P.override && (P.override.where === 'phone' || P.override.where === 'station')) P.override = null;
    P.hold = false;
    P.route = null;
    P.goalKey = '';
    note(`${P.def.name} was on the way to the police. She is not going now: ${r.why}. What the street says is another matter.`.replace('She is', P.def.sex === 'm' ? 'He is' : 'She is'), 'police', 'stopped' + w.id, { who: P.id, how: 'Did it' });
  }
  emit('witness:stopped', { who: P.id, E, answer, police: r.police, street: r.street });
  return r;
}
function walkMatter(P, a) {
  const w = walkOf(P);
  if (!w) return;
  const E = G.ev[w.e];
  if (!E) return;
  const price = LAW.stop.payBasePence + LAW.stop.payMorePencePerCrimeLevel * kindOf(E).crime,
    sir = P.def.sex === 'm',
    say = (r, yes, no) => (r && !r.police ? yes : no);
  a.unshift({
    key: 'lawwalk' + w.id,
    ask: 'whether this witness goes to the police about what they saw',
    raise: "I saw it. I'm not having it on this street. I'm going to ring the police.",
    keep: ['What is it you think you saw?', 'Who else was looking?'],
    keepSay: 'I know what I saw, and I know who. Stand out of my way.',
    opts: [
      {
        say: ['Hear me out first. It was not what it looked like.', 'Give me a minute before you ring anybody.'],
        take: () => say(stopWalk(P, 'round'), "Well. I'll not ring tonight. Don't make me sorry.", "I've heard you out. I'm still ringing them."),
      },
      {
        say: [`Would ${pounds(price)} help you forget it?`, `There is ${pounds(price)} here if you turn round.`],
        q: `${pounds(price).replace(/^./, (c) => c.toUpperCase())}. To say nothing. Is that it?`,
        yes: ['Yes. Take it.', 'Yes. And we never spoke.'],
        no: ['No. Forget I said it.', 'No. Leave it.'],
        keep: ['What would you tell them?', 'Who else was looking?'],
        keepSay: 'What I saw. Is that what the money is for?',
        take: () => say(stopWalk(P, 'pay'), 'I never saw a thing. And you never gave me this.', sir ? 'Keep your money, pal.' : 'Keep your money. I know what I saw.'),
      },
      {
        say: ['You saw nothing. Think about where you live.', 'Ring them, and I will know who did.'],
        q: 'Is that a threat?',
        yes: ['Yes. It is.', 'Yes. Take it as one.'],
        no: ['No. Forget I said it.', 'No. I only meant, think on.'],
        keep: ['What would you tell them?', 'Who else was looking?'],
        keepSay: 'I asked you a question. Is that a threat?',
        take: () => say(stopWalk(P, 'threat'), "All right. All right. I saw nothing. But folk talk, and that's not me.", "You don't frighten me. I'm ringing them, and I'll tell them that an' all."),
      },
      {
        say: ["Let me see you home. It's late to be out.", "I'll walk you back. Give me the bag."],
        take: () => say(stopWalk(P, 'help'), "Well. That's more than your uncle would have done. I'll sleep on it.", "Thank you. I'm still going, mind."),
      },
    ],
  });
}

// ---------- after a seen deed: look, gather, drift back, talk quieter (ER-EYES-09) ----------
function reaction(E) {
  const x = L(),
    out = { looked: [], gathered: null };
  for (const P of [...G.named, ...G.crowd]) {
    if (P.dead || P.gone || P.down || !P.awake || P.space !== 'street' || P.def.police || P.fight) continue;
    const d = hyp(P.x, P.z, E.x, E.z);
    if (d > REACT.lookWithinMetres) continue;
    P.alert = { x: E.x, z: E.z, t: REACT.lookForRealSeconds };
    P.mind.look = Math.max(P.mind.look || 0, REACT.lookForRealSeconds);
    out.looked.push(P.id);
    if (!out.gathered && !P.keeper && !P.lawWalk && d > REACT.gatherStopsShortMetres + 1 && !E.wit.includes(P.id)) out.gathered = P;
  }
  if (!out.gathered) {
    const P = [...G.named, ...G.crowd].find((p) => out.looked.includes(p.id) && !p.keeper && !p.lawWalk && hyp(p.x, p.z, E.x, E.z) > REACT.gatherStopsShortMetres + 1);
    if (P) out.gathered = P;
  }
  if (out.gathered) {
    const P = out.gathered,
      d = hyp(P.x, P.z, E.x, E.z),
      k = (d - REACT.gatherStopsShortMetres) / d;
    goToPoint(P, P.x + (E.x - P.x) * k, P.z + (E.z - P.z) * k);
    P.lawGather = REACT.gatherForRealSeconds;
    x.gatherers = (x.gatherers || []).filter((g) => g.id !== P.id).concat([{ id: P.id }]);
    out.gathered = P.id;
  }
  for (const id of E.wit) x.quiet[id] = mins(G.t + REACT.quietForGameMinutes);
  x.lastReaction = { e: E.id, looked: out.looked, gathered: out.gathered, quiet: E.wit.slice(), t: mins(G.t) };
  return out;
}
function stepGatherers(dt) {
  const x = L();
  if (!x.gatherers || !x.gatherers.length) return;
  x.gatherers = x.gatherers.filter((g) => {
    const P = personOf(g.id) || G.crowd.find((c) => c.id === g.id);
    if (!P) return false;
    P.lawGather -= dt;
    if (P.lawGather > 0) return true;
    // drifts back to what the routine has for them
    P.hold = false;
    P.route = null;
    P.goalKey = '';
    P.lawGather = 0;
    return false;
  });
}
export const talksQuieter = (P) => (L().quiet[P.id] || 0) > G.t;

// ---------- every new deed is looked at once ----------
function scan() {
  const x = L();
  const evs = G.events;
  if (!evs.length || evs[evs.length - 1].id <= x.lastE) return;
  for (let i = evs.length - 1; i >= 0 && evs[i].id > x.lastE; i--) lookAt(evs[i]);
  x.lastE = evs[evs.length - 1].id;
}
function lookAt(E) {
  const x = L(),
    k = kindOf(E);
  if (k.noself && !k.kills) return;
  const seen = (E.wit || []).length > 0,
    zone = E.zone || 'Quay Street';
  if (k.crime >= 1 && seen) {
    reaction(E);
    (x.deeds[zone] || (x.deeds[zone] = [])).push(mins(E.t));
    if (x.deeds[zone].length > 12) x.deeds[zone].shift();
    const edge = onEdge(x.deeds[zone], G.t);
    if (edge.edge && !x.edge[zone]) {
      x.edge[zone] = mins(G.t);
      x.edgeSay = zone;
      emit('street:edge', { zone, on: true });
      logLine(zone + ' is on edge: three seen deeds inside two days', 'police');
    }
    // those who saw him plainly and will not keep quiet set off to tell: two walk, the rest sleep on it
    let n = 0;
    for (const id of new Set([...(E.wit || []), ...(E.party || [])])) {
      const P = personOf(id);
      if (!P || P.anon || n >= 2 || !wouldState(P, E).goes) continue;
      startWalk(P, E, (edge.edge ? edge.setsOffTimes : 1) * (1 + n * 3));
      n++;
    }
  }
  const body = E.kind === 'kill' || k.kills;
  if (body && E.target) {
    x.bodies.push({ id: E.target, e: E.id, x: E.x, z: E.z, zone, t: mins(E.t), hidden: !!E.hidden, sunk: !!E.sunk, found: seen ? mins(E.t) : null });
    x.missing[E.target] = { since: mins(E.t), asked: 0 };
  }
  if (k.crime >= 1 && !seen && (k.trace || E.trace || body) && E.zone !== 'away')
    x.traces.push({ e: E.id, x: E.x, z: E.z, zone, t: mins(E.t), hidden: !!E.hidden, sunk: !!E.sunk, found: null });
  if (k.gun || E.gun) gunCall(E);
}

// ---------- finding an unseen deed (A38): the first routine that passes its trace, never a roll ----------
function findTraces() {
  const x = L();
  for (const tr of x.traces) {
    if (tr.found) continue;
    const passes = [];
    for (const P of G.named) {
      if (P.dead || P.gone || !P.awake || P.space !== 'street' || P.def.police) continue;
      const d = hyp(P.x, P.z, tr.x, tr.z);
      if (d < LAW.find.steppedOnWithinMetres || (d < LAW.find.seenWithinMetres && G.env.los(P.x, P.z, tr.x, tr.z))) passes.push({ who: P.id, t: G.t });
    }
    const f = finder({ trace: true, hidden: tr.hidden, sunk: tr.sunk, t: tr.t }, passes);
    if (f) found(tr, f.who);
  }
}
function found(tr, who) {
  const x = L(),
    P = personOf(who),
    E = G.ev[tr.e];
  if (!P || !E) return;
  tr.found = { who, t: mins(G.t) };
  const body = x.bodies.find((b) => b.e === tr.e);
  if (body) body.found = mins(G.t);
  const what = body ? 'a body' : E.what || 'the damage';
  // the finder holds only the aftermath: what was left, never who did it
  const A = mkEvent('law_found', { zone: tr.zone, x: tr.x, z: tr.z, what, about: tr.e, coat: false, car: false });
  remember(P, A, { src: 'saw', who: 'man', sure: 0.25, heat: clamp(kindOf(E).sev + 0.2, 0, 1) });
  A.wit.push(P.id);
  logLine(`${P.def.name} came by and found ${what} on ${tr.zone}`, 'police');
  // found is known to the police as a thing done, with nobody named: an officer at the spot, no arrest (ER-POL-01)
  spot(E, body ? 'a body' : 'found');
  emit('deed:found', { E, by: who, holds: ['aftermath'] });
  if (inPlay() && P.space === G.tom.space && tomNotices(P)) sub(`${tomName(P)} has stopped, and is looking at ${what}.`, '', 'over', 5);
}

// ---------- the spot after a deed (A36): an officer there, a body brings tape and Ellis, watched till morning ----------
function spot(E, why) {
  const x = L();
  if (x.spots.some((s) => s.e === E.id)) return;
  const d = Math.floor(G.t / 1440),
    h = hour(),
    until = (h < LAW.spot.watchedUntilHour ? d : d + 1) * 1440 + LAW.spot.watchedUntilHour * 60;
  const body = why === 'a body' || E.kind === 'kill' || !!kindOf(E).kills;
  x.spots.push({ e: E.id, x: E.x, z: E.z, zone: E.zone || 'Quay Street', from: mins(G.t + LAW.spot.officerComesWithinGameMinutes), until, body, said: 0, officer: 0 });
  if (body) x.bodyEllisDay = d + 1;
  emit('police:spot', { E, body, until });
}
export const watchedGround = (px, pz) => L().spots.find((s) => G.t >= s.from && G.t < s.until && hyp(px, pz, s.x, s.z) < LAW.spot.watchedWithinMetres) || null;
function stepSpots() {
  const x = L();
  x.spots = x.spots.filter((s) => G.t < s.until + 60);
  const s = x.spots.find((sp) => G.t >= sp.from && G.t < sp.until);
  x.beat.detour = s ? { x: s.x + 1.5, z: s.z + 1, e: s.e } : null;
  if (!s) return;
  const [tx, tz] = tomXZ();
  if (!s.said && inPlay() && G.tom.space === 'street' && hyp(tx, tz, s.x, s.z) < 40 && G.env.los(tx, tz, s.x, s.z)) {
    s.said = 1;
    sub(s.body ? 'Police tape across the pavement, and a constable with a torch. Nobody goes near.' : 'A constable is standing where it happened, writing in his book.', '', 'over', 6);
    note(`The police are at the spot on ${s.zone}${s.body ? ', with tape up' : ''}. It is watched until morning.`, 'police', 'spot' + s.e, { how: 'Saw it' });
  }
}

// ---------- the four stages, each with its sign (ER-POL-05) ----------
function facts() {
  const x = L(),
    st = G.story;
  let worst = null,
    n = 0;
  const rank = { window: 1, wounding: 2, robbery: 3, killing: 4 };
  for (const id in x.reported) {
    if (x.taken[id]) continue;
    const E = G.ev[id];
    if (!E) continue;
    n++;
    const c = classOf(E);
    if (!worst || rank[c] > rank[worst]) worst = c;
  }
  return {
    ellisAsked: !!x.ellisAsked || !!st.ellis,
    statements: n,
    worstClass: worst,
    ranFromPolice: x.ran > 0 || !!(st.flags && st.flags.ranPolice),
    body: x.bodies.some((b) => b.found),
    hunted: !!x.hunted,
  };
}
const SIGN = [
  null,
  { say: 'That detective has been asking after you. Ellis, they call her.', note: "DS Ellis is asking round about Tom. Her name is in the street's talk." },
  { say: 'There has been a constable at the office door, asking for you by name.', note: 'An officer has been at the office door for Tom. They are looking into him.' },
  { say: 'A police car comes slowly down the street. A voice from it gives your height, your coat and your name.', note: 'The police are out looking for Tom, and giving out his description.' },
];
function stepStages() {
  const x = L();
  const want = wanted(facts());
  x.want = want;
  const next = advance(x, want, G.t);
  if (next !== x.stage) {
    x.stage = next;
    x.signs.push({ stage: next, t: mins(G.t), shown: false, why: want === 3 ? 'hunted' : want === 2 ? 'a statement' : 'asking' });
    if (x.signs.length > 20) x.signs.shift();
    logLine('Police interest: stage ' + next + ' (' + ['nothing', 'asking round', 'investigating', 'a manhunt'][next] + ')', 'police');
    emit('police:stage', { stage: next, why: x.signs[x.signs.length - 1].why });
    if (next === 2 && !x.office.done && x.office.noticeT == null) x.office.wanted = 1;
  }
  // a sign is shown when he is there to see or hear it; until then the next stage waits
  const sg = x.signs[x.signs.length - 1];
  if (sg && !sg.shown && sg.stage === x.stage && inPlay() && G.tom.space !== 'away') {
    const S = SIGN[sg.stage];
    sg.shown = true;
    sg.t = mins(G.t); // the hour before a manhunt's arrest runs from when he was shown it
    sub(S.say, sg.stage === 3 ? '' : 'Passed along the street', sg.stage === 3 ? 'over' : 'face', 7);
    note(S.note, 'police', 'stage' + sg.stage + 'd' + day(), { how: sg.stage === 3 ? 'Saw it' : 'Passed along the street' });
    if (sg.stage === 3) {
      news('POLICE SEEK QUAY STREET MAN', 'Description given out on the Hook');
      mkEvent('law_manhunt', { zone: 'Quay Street', coat: false, car: false });
    }
  }
  // a manhunt: once its sign has been up a game hour, any officer who finds him takes him
  if (x.stage === 3 && manhuntMayArrest(x, G.t) && !G.story.arrest) {
    G.story.arrest = { e: worstReported(), violent: true, due: G.t, by: [], cls: facts().worstClass || 'wounding', officerSaw: x.ran > 0 };
    logLine('The manhunt found its hour: officers are coming for Tom', 'police');
  }
  x.case.strength = caseStrength({ statements: x.case.statements, charges: x.case.charges.length, officeFinds: x.case.officeFinds });
}
function worstReported() {
  const x = L();
  let best = null;
  for (const id in x.reported) {
    if (x.taken[id] || !G.ev[id]) continue;
    if (!best || kindOf(G.ev[id]).crime > kindOf(G.ev[best]).crime) best = +id;
  }
  return best;
}

// ---------- DS Ellis: for a body, for a detective's crime once reported, from day 4 for talk ----------
function dayPeopleTalking() {
  let n = 0;
  for (const P of G.named) {
    if (P.dead || P.def.police || ['sheila', 'ron', 'pauline', 'kevin', 'terry', 'darren'].includes(P.id)) continue;
    if (P.mind.mem.some((m) => attached(m) && m.src === 'told' && G.ev[m.e] && kindOf(G.ev[m.e]).crime >= 1)) n++;
  }
  return n;
}
function ellisHour(h, d) {
  const x = L(),
    st = G.story;
  if (h !== LAW.spot.ellisAfterABodyAtHour || st.ellis || st.arrest) return;
  st.ellisDays = st.ellisDays || {};
  if (st.ellisDays[d]) return;
  let cls = null;
  for (const id in x.reported) if (!x.taken[id] && G.ev[id] && (!x.ellisFor || !x.ellisFor[id])) cls = cls === 'killing' ? cls : classOf(G.ev[id]);
  const why = ellisComes({ body: x.bodyEllisDay === d, reportedClass: cls, dayIndex: d, dayPeopleTalking: x.live ? 0 : dayPeopleTalking() });
  if (!why) return;
  if (startEllis(why)) {
    st.ellisDays[d] = 1;
    x.ellisFor = x.ellisFor || {};
    for (const id in x.reported) x.ellisFor[id] = 1;
  }
}

// ---------- the office searched (A13): once, at investigating, with notice the evening before ----------
function officeHour(h, d) {
  const x = L(),
    o = x.office;
  if (o.done || !o.wanted) return;
  if (o.noticeT == null) {
    if (h === LAW.office.noticeAtHour) {
      o.noticeT = mins(G.t);
      o.said = 0;
      logLine('Notice given: the office will be searched in the morning', 'police');
      emit('police:notice', { searchAt: (d + 1) * 1440 + LAW.office.searchAtHour * 60 });
    }
    return;
  }
  if (h === LAW.office.searchAtHour && G.t - o.noticeT >= 12 * 60) searchOffice();
}
const incriminating = (it) => (typeof it === 'string' ? true : it && it.hot !== false);
const nameOf = (it) => (typeof it === 'string' ? it : (it && (it.name || it.id)) || 'a thing');
export function searchOffice() {
  const x = L(),
    o = x.office,
    crime = G.x.crime || {};
  if (o.done) return null;
  if (o.noticeT == null) return null; // ER-SEARCHED-01: never without the sign the evening before
  const stored = Array.isArray(crime.office) ? crime.office : crime.office && typeof crime.office === 'object' ? Object.values(crime.office).flat() : [];
  const found = stored.filter(incriminating).map(nameOf);
  o.done = true;
  o.doneT = mins(G.t);
  o.found = found;
  if (Array.isArray(crime.office)) crime.office = crime.office.filter((it) => !incriminating(it));
  x.case.officeFinds += found.length;
  mkEvent('law_office_searched', { zone: 'Quay Street', coat: false, car: false });
  o.tell = 1;
  logLine('The office was searched: ' + (found.length ? found.join(', ') : 'nothing found'), 'police');
  emit('police:office', { found });
  return found;
}
function officeSay() {
  const o = L().office;
  if (!inPlay()) return;
  if (o.noticeT != null && !o.said && !o.done) {
    o.said = 1;
    sub('Word from the station, by way of Sheila: they are coming to go through the office in the morning. With a warrant.', 'Passed along the street', 'face', 8);
    note('The police will search the office in the morning. Whatever is kept there will be found.', 'police', 'officenotice', { who: 'sheila', how: 'Sheila says' });
  }
  if (o.done && o.tell) {
    o.tell = 0;
    sub(o.found.length ? `They went through the office this morning. They took ${o.found.join(', ')}.` : 'They went through the office this morning and found nothing.', 'Passed along the street', 'face', 8);
    note(o.found.length ? `The office was searched. The police took ${o.found.join(', ')}. It goes in DS Ellis's file.` : 'The office was searched. Nothing was found.', 'police', 'officesearched', { how: 'Passed along the street' });
  }
}

// ---------- bought men (A13): two named officers, each a price and a limit ----------
// ask: 'car' (PC Pashby looks away from a car) | 'statement' (Sergeant Thwaite loses a statement, once)
export function buyOfficer(who, ask) {
  const x = L(),
    b = x.bought[who],
    P = personOf(who);
  if (!b) {
    // anybody else at the station is honest: a note offered is a crime he saw
    const E = act('law_note_offered', { target: who, told: [who] });
    E.officerSaw = true;
    record(E, [], 'an officer saw it');
    return { does: false, crime: true };
  }
  const price = who === 'pashby' ? LAW.bought.pashbyPricePence : LAW.bought.thwaitePricePence;
  if (who === 'pashby' && b.night !== day()) {
    b.night = day();
    b.used = 0;
  }
  const can = TOWN.fns.boughtDoes(who, true, ask, b.used);
  if (!can.does) return { does: false, crime: false, why: 'that is past what he will do' };
  if (!pay(price, false, 'an officer paid')) return { does: false, crime: false, why: 'he has not got it' };
  b.paid += price;
  b.used++;
  const E = act('law_officer_paid', { target: who });
  // a colleague who saw the payment keeps it
  for (const id of ['pc', 'pashby', 'thwaite', 'ellis']) {
    const C = personOf(id);
    if (!C || id === who || C.gone || C.dead || !P || C.space !== P.space) continue;
    if (hyp(C.x, C.z, P.x, P.z) < LAW.bought.colleagueSeesWithinMetres && sense(C, tomTarget()).see) {
      x.bought.seen.push({ by: id, who, t: mins(G.t), e: E.id });
      E.officerSaw = true;
      E.lawClass = 'window';
      record(E, [], 'a colleague saw the money change hands');
    }
  }
  if (ask === 'statement') {
    // the statement is lost: the arrest it would have brought never comes
    const a = G.story.arrest,
      id = a && !a.st ? a.e : worstReported();
    if (id != null && G.ev[id]) {
      for (const w of G.ev[id].stmt || []) x.lost[id + ':' + w] = 1;
      delete x.reported[id];
      G.ev[id].stmt = [];
      if (a && !a.st && a.e === id) G.story.arrest = null;
      b.lostE = id;
    }
  }
  emit('police:bought', { who, ask });
  return { does: true, crime: false, price };
}
function officerMatter(P, a) {
  const x = L();
  if (P.id === 'thwaite') {
    const pend = G.story.arrest && !G.story.arrest.st && G.story.arrest.e != null,
      can = TOWN.fns.boughtDoes('thwaite', true, 'statement', x.bought.thwaite.used).does;
    if (pend && can)
      a.push({
        key: 'lawthwaite',
        direct: true,
        ask: 'whether to pay the sergeant to lose a statement',
        raise: `There is a statement on my desk with your name in it. Paper goes astray in a station. ${pounds(LAW.bought.thwaitePricePence).replace(/^./, (c) => c.toUpperCase())} would see to it. Once.`,
        opts: [
          {
            agree: 1,
            q: 'Once, I said. Yes or no?',
            yes: ['Yes. Lose it.', 'Yes. Here.'],
            no: ['No. Leave it where it is.', 'No. Not today.'],
            keep: ['Whose statement is it?', 'What happens if it stays?'],
            keepSay: 'I do not say whose. If it stays, a constable calls at nine. Yes or no?',
            noSay: 'Then it stays on the desk.',
            take: () => {
              const r = buyOfficer('thwaite', 'statement');
              return r.does ? 'I never saw it. Nor you. Mind how you go.' : r.why === 'he has not got it' ? 'Come back with the money, or do not come back.' : 'No. That I will not do.';
            },
          },
        ],
      });
  }
}
// Sergeant Thwaite smokes outside the station door at dinner time; otherwise he is off the map.
function thwaiteHour(h) {
  const P = personOf('thwaite');
  if (!P || P.dead) return;
  if (h === 12) send(P, 'station', 'smoke', G.t + 120);
}

// ---------- the dial's police (DESIGN section 7): armed response and, at War, stop and search ----------
function gunCall(E) {
  const x = L(),
    dial = (G.x.dial && G.x.dial.state) || 0,
    r = response(dial, 'gun');
  if (!r.armed) return;
  x.armed.calls++;
  x.spots.push({ e: E.id, x: E.x, z: E.z, zone: E.zone || 'Quay Street', from: mins(G.t + r.arrivesGameMinutes), until: mins(G.t + r.arrivesGameMinutes + 240), body: false, armed: true, said: 0 });
  x.armed.sayAt = mins(G.t + r.arrivesGameMinutes);
  logLine('A gun call: armed officers sent from the station, ' + r.arrivesGameMinutes + ' game minutes out', 'police');
  emit('police:armed', { E, arrivesGameMinutes: r.arrivesGameMinutes, officersAtMost: r.armedOfficersAtMost });
}
function warStep() {
  const x = L(),
    dial = (G.x.dial && G.x.dial.state) || 0;
  if (x.armed.sayAt && G.t >= x.armed.sayAt && inPlay()) {
    x.armed.sayAt = 0;
    sub('Armed officers from the town station are on the street. They took their time, and they are not leaving.', '', 'over', 7);
    note('Armed police came down from the station after the shot.', 'police', 'armed' + day(), { how: 'Saw it' });
  }
  if (!response(dial, 'other').stopAndSearch) return;
  const h = hour(),
    t = G.tom;
  if (h < LAW.armed.warStopSearchFromHour || h >= LAW.armed.warStopSearchUntilHour) return;
  if (G.t - x.armed.lastStopT < LAW.armed.warStopSearchEveryGameMinutes) return;
  if (!inPlay() || t.space !== 'street' || t.inCar || G.story.arrest) return;
  x.armed.lastStopT = mins(G.t);
  x.armed.stops++;
  x.beat.stopSearch = 1; // the beat takes it from here (law_beat.js)
}

// ---------- death, bodies and the missing (DESIGN section 7): a body never cools ----------
function missingHour() {
  const x = L();
  for (const id in x.missing) {
    const m = x.missing[id],
      body = x.bodies.find((b) => b.id === id);
    if (body && body.found) continue; // found: then it is a body, and a body is news for good
    const r = missingAsked({ goneSince: m.since, found: false }, G.t);
    if (!r.asked || r.times <= m.asked) continue;
    m.asked = r.times;
    const P = personOf(id);
    if (!P) continue;
    const since = DAYS[Math.floor(m.since / 1440) % 7];
    const A = mkEvent('law_missing', { zone: P.def.street || 'Quay Street', name: P.def.name, target: null, about: id, since, coat: false, car: false });
    for (const cid of P.def.close || []) {
      const C = personOf(cid);
      if (C && !C.dead) remember(C, A, { src: 'self', who: 'man', sure: 1, heat: 1 });
    }
    m.sayName = P.def.name;
    m.say = since;
    logLine(`${P.def.name} has not kept the routine since ${since}: people are asking`, 'police');
    emit('town:missing', { who: id, since: m.since });
  }
  // a body never cools: whoever holds a killing keeps it hot
  for (const b of x.bodies) {
    if (!b.found) continue;
    for (const P of G.named) {
      const mm = P.mind.by[b.e];
      if (mm) mm.heat = Math.max(mm.heat, 0.9);
    }
  }
}
function missingSay() {
  const x = L();
  if (!inPlay()) return;
  for (const id in x.missing) {
    const m = x.missing[id];
    if (!m.say) continue;
    sub(`Nobody has seen ${m.sayName} since ${m.say}. People have started to ask.`, 'Passed along the street', 'face', 7);
    note(`${m.sayName} has not been seen since ${m.say}. The street is asking where.`, 'police', 'missing' + id + m.asked, { how: 'Passed along the street' });
    m.say = null;
    return;
  }
}
// Others may tell the law that a body has been moved, hidden or sunk (the crew's verb; the water's edge).
export function bodyMoved(id, how) {
  const x = L(),
    b = x.bodies.find((q) => q.id === id);
  if (!b || b.found) return false;
  b.hidden = how === 'hidden' || b.hidden;
  b.sunk = how === 'sunk' || b.sunk;
  const tr = x.traces.find((t) => t.e === b.e);
  if (tr) {
    tr.hidden = b.hidden;
    tr.sunk = b.sunk;
  }
  return true;
}

// ---------- the real town's hour (the bridge): the same road ----------
const ids = (v) => (Array.isArray(v) ? v : v ? [v] : []).map((q) => (typeof q === 'string' ? q : q && (q.id || q.who))).filter(Boolean);
function townHour(h) {
  const x = L();
  if (!h) return;
  const deed = () => {
    for (let i = G.events.length - 1; i >= 0; i--) if (kindOf(G.events[i]).crime >= 1 && kindOf(G.events[i]).town === 'deed') return G.events[i];
    for (let i = G.events.length - 1; i >= 0; i--) if (kindOf(G.events[i]).crime >= 1 && !kindOf(G.events[i]).noself) return G.events[i];
    return null;
  };
  const went = ids(h.went).filter((id) => personOf(id));
  if (went.length) {
    const E = deed();
    if (E) {
      const was = x.live;
      x.live = false; // the town has decided: record it as it stands
      record(E, went, 'the town: went to the police this morning');
      x.live = was;
    }
  }
  for (const id of ids(h.found)) {
    const E = deed();
    if (!E) break;
    const tr = x.traces.find((t) => t.e === E.id) || { e: E.id, x: E.x, z: E.z, zone: E.zone || 'Quay Street', t: mins(E.t), found: null };
    if (!tr.found && personOf(id)) found(tr, id);
  }
  if (h.ellis) startEllis(typeof h.ellis === 'string' ? h.ellis : 'the town');
  if (h.taken) {
    const E = deed(),
      out = /caution/i.test(h.taken) ? 'cautioned' : 'charged';
    if (!G.story.arrest) G.story.arrest = { e: E ? E.id : null, violent: false, due: G.t, by: E ? E.stmt || [] : [], cls: E ? classOf(E) : 'window' };
    G.story.arrest.due = Math.min(G.story.arrest.due, G.t);
    G.story.arrest.outcome = out;
    if (out === 'cautioned') G.story.arrest.ownedUp = true;
  }
}

// ---------- the system ----------
register({
  id: 'law',
  fresh,
  loaded(x) {
    const f = fresh();
    for (const k in f) if (x[k] === undefined) x[k] = f[k];
    if (!x.lastE && G.events.length) x.lastE = G.events[G.events.length - 1].id; // an older save: its past is not walked again
    for (const w of x.walks) {
      if (w.st !== 'walking') continue;
      const P = personOf(w.who);
      if (P) {
        P.lawWalk = w.id;
        send(P, w.to === 'station' ? 'station' : 'phone', 'idle', w.landBy + 30);
      }
    }
    beatLoaded(x);
  },
  step(dt) {
    const x = L();
    x.live = !!(G.x.town && G.x.town.live);
    scan();
    stepWalks(dt);
    stepGatherers(dt);
    beatStep(dt, x);
    if (x.edgeSay && inPlay()) {
      sub(`${x.edgeSay} is on edge. Doors shut early, and the curtains move as you pass.`, '', 'over', 6);
      note(`${x.edgeSay} is on edge after what it has seen. People set off to tell sooner, and the constable walks it more.`, 'police', 'edge' + x.edgeSay + day(), { how: 'Saw it' });
      x.edgeSay = null;
    }
  },
  minute() {
    const x = L();
    stepStages();
    stepSpots();
    findTraces();
    warStep();
    officeSay();
    missingSay();
    for (const z in x.edge)
      if (!onEdge(x.deeds[z] || [], G.t).edge) {
        delete x.edge[z];
        emit('street:edge', { zone: z, on: false });
      }
    for (const id in x.quiet) if (x.quiet[id] <= G.t) delete x.quiet[id];
    // a walk nobody could follow (asleep, away, time skipped) still ends
    for (const w of x.walks) if (w.st === 'walking' && G.t >= w.landBy) land(w, 'rang from home');
  },
  hourly(h, d) {
    ellisHour(h, d);
    officeHour(h, d);
    thwaiteHour(h);
    missingHour();
  },
  matters(P, a) {
    walkMatter(P, a);
    officerMatter(P, a);
  },
  hook: {
    state: () => L(),
    facts,
    // plant a statement: this person saw this deed plainly and has gone to the police (the walk skipped)
    plantStatement(eid, who) {
      const E = G.ev[eid];
      return E ? record(E, [who], 'planted by a test') : false;
    },
    // make somebody a plain witness of a deed, as if they had stood and watched
    plantWitness(eid, who, sure = 0.9) {
      const E = G.ev[eid],
        P = personOf(who);
      if (!E || !P) return false;
      remember(P, E, { src: 'saw', who: 'tom', sure, heat: 0.8, face: 0.9 });
      if (!E.wit.includes(who)) E.wit.push(who);
      return true;
    },
    startWalk(who, eid) {
      const P = personOf(who),
        E = G.ev[eid];
      return P && E ? startWalk(P, E) : null;
    },
    walks: () => L().walks,
    stopWalk: (who, answer) => stopWalk(personOf(who), answer),
    wouldState: (who, eid) => wouldState(personOf(who), G.ev[eid]),
    setStage(n) {
      // for tests: ask for a stage; it is still reached one sign at a time
      const x = L();
      x.hunted = n >= 3 ? 1 : 0;
      if (n >= 1 && !x.ellisAsked) x.ellisAsked = mins(G.t);
      return x.stage;
    },
    stepStages,
    spot: (eid) => spot(G.ev[eid], 'test'),
    watchedGround,
    searchOffice,
    giveNotice() {
      const o = L().office;
      o.wanted = 1;
      o.noticeT = mins(G.t);
      o.said = 0;
    },
    buyOfficer,
    bodyMoved,
    found: (eid, who) => {
      const E = G.ev[eid];
      const tr = L().traces.find((t) => t.e === eid) || { e: eid, x: E.x, z: E.z, zone: E.zone, t: mins(E.t), found: null };
      found(tr, who);
      return tr.found;
    },
    townHour,
    reaction: (eid) => reaction(G.ev[eid]),
    talksQuieter: (who) => talksQuieter(personOf(who)),
    gunCall: (eid) => gunCall(G.ev[eid]),
    missingHour,
    beat: beatHook,
  },
});
on('town:hour', townHour);
on('loaded', () => {
  // what other systems may call without importing this file
  Object.assign(G.hooks, {
    lawWatchedGround: watchedGround,
    lawBodyMoved: bodyMoved,
    lawBuyOfficer: buyOfficer,
    lawTalksQuieter: talksQuieter,
    lawStage: () => L().stage,
    lawCase: () => L().case,
  });
});
