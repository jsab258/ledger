// LEDGER, the whole game: the system "rivals". Three rivals, each after a different ledger, each knowing only what
// its own people saw or heard (DESIGN 13; parts 2.10.1 to 2.10.4, 3.5.5). Each climbs the same ladder, never
// skipping a rung, each rung said to his face or shown on his street; every pressure has three answers; the Fixer
// sells true reads, a meeting and one truce. Rules: pieces/rivals.js. No faction is a number.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on } from './core.js';
import { G } from '../state.js';
import { quid } from '../util.js';
import { pay } from '../money.js';
import { KINDS } from '../kinds.js';
import { choose, scene, say } from '../ui.js';
import { RULES } from '../rules.js';
import { PIECE as RIV } from './pieces/rivals.js';
import { letter, sign } from './ledgerx.js';

const T = RULES.game.rivals;
const R = RIV.fns;
const called = (id) => T.rivals[id].called;
// What he knows that a rival would not want known (the counter): facts his hands or his fares turned up.
// Mickey's real book, once Sheila has put it on the desk, holds what he paid each of them and when: a counter to any of the three.
const book = () => (G.x.crime.facts.real_book ? "what Mickey paid them, week by week, in his own hand" : null);
const KNOWS = { widow: () => (G.x.fares.learned.gate_tax ? "who takes the money in the hut at the dock gate" : book()), agar: () => (G.x.crime.facts.agar_licence ? "who wrote the complaint on the Board's paper" : book()), cammack: () => (G.x.crime.facts.rita_book ? "whose lads are in Rita's book every week" : book()) };

// Something one of a rival's own people saw or heard of him (ER-RIV-01).
export function learns(id, by, what, e) {
  const x = X('rivals');
  const r = R.learns(id, x.r[id], { by, what, t: G.t, e });
  if (r.took) x.r[id] = r.rival;
  return r.took;
}
function climbAll() {
  const x = X('rivals');
  for (const id in x.r) {
    const sooner = G.story.flags.choice === 'wind' ? T.rivalsComeSoonerIfArrangementEndedGameDays * 1440 : 0;
    if (!R.standing(x.sitDown, id, x.r[id].rung).mayClimb) continue; // what the sit-down settled stands (3.5.5)
    const r = R.climb(id, x.r[id], G.t + (x.r[id].rung === 0 ? sooner : 0));
    if (!r.climbed) continue;
    x.r[id] = Object.assign(r.rival, { lastT: G.t });
    x.moves.push({ id, rung: r.rival.rung, name: r.rung, trace: r.trace, show: r.show, t: Math.round(G.t), shownT: null });
    emit('rivals.climbed', { id, rung: r.rival.rung });
  }
}
// Each rung is said to his face or shown on his street (ER-RIV-02). Until it has been, the rival cannot climb again.
async function showMoves() {
  const x = X('rivals'),
    t = G.tom;
  const m = x.moves.find((q) => !q.shownT);
  if (!m || G.paused || t.inCar || G.hooks.modal()) return;
  const sh = m.show,
    Rv = T.rivals[m.id];
  if (sh.how === 'said to his face') {
    const P = (sh.by && P_(sh.by) && here(P_(sh.by), RULES.game.law.signHeardWithinMetres) ? P_(sh.by) : null) || G.named.find((Q) => Rv.eyes.includes(Q.id) && here(Q, RULES.game.law.signHeardWithinMetres));
    if (!P && m.rung < 3) return; // it waits for one of its people to be near him
    m.shownT = Math.round(G.t);
    if (sh.pressure) return pressure(m, P);
    if (sh.sitDown) return sitDown(m);
    tell('"' + sh.line + '"', P.def.name, 7);
    write(`${P.def.name} says ${sh.line[0].toLowerCase() + sh.line.slice(1)}`, { who: P.id, how: 'Said to his face', key: 'rival:' + m.id + ':' + m.rung });
  } else {
    if (t.space !== 'street' && t.space !== 'mickeys') return;
    m.shownT = Math.round(G.t);
    tell(sh.line, '', 8);
    write(sh.line + (sh.threat ? ` That is ${called(m.id)}.` : ''), { how: 'Saw it himself', key: 'rival:' + m.id + ':' + m.rung });
    if (sh.threat) threat(m.id);
  }
  x.r[m.id] = R.shown(x.r[m.id]);
}
// ---- a pressure and its three answers (2.10.3): pay, defy, or counter with what he knows ----
async function pressure(m, P) {
  const x = X('rivals'),
    Rv = T.rivals[m.id],
    cost = Rv.taxPencePerWeek || Rv.feePence || Rv.damagePence;
  if (m.id === 'agar') letter('agar' + dayNow(), 'Agar & Co, Solicitors', 'The private-hire licence of Mickey\'s Cars', 'Dear Mr Nowak,\nWe act for certain interests on the Harbour Board. A complaint has been laid touching the private-hire licence held in the name of the late Mr Suddaby.\nThe matter may be settled without a hearing on payment of our fee of ninety pounds.\nYours faithfully, G. Agar');
  const knows = KNOWS[m.id]();
  const i = await scene(async () => {
    await say(P ? P.id : called(m.id), m.id === 'widow' ? `Mrs Jensen says your drivers pay at the dock gate now, like everybody. ${quid(cost)} a week.` : m.id === 'agar' ? `Mr Agar's letter is on your desk. ${quid(cost)}, and the licence is not looked at.` : `Danny says Quay Street is a rough street lately. ${quid(cost)} and it stops being.`);
    return choose('', `${called(m.id)}: ${Rv.pressure}.`, ['Pay.', 'Defy it.', knows ? 'Tell them what he knows: ' + knows + '.' : 'Counter (he knows nothing to counter with).']);
  });
  const choice = T.answers[i];
  let r = R.answer(m.id, x.r[m.id], choice, { pocketPence: G.money.clean + G.money.dirty, knows });
  if (!r.ok) r = R.answer(m.id, x.r[m.id], 'defy', {}); // an answer he cannot make is a defiance: nothing ends
  if (r.flow) pay(r.flow.pence, false, r.flow.why);
  x.r[m.id] = R.shown(r.rival);
  x.answers.push({ id: m.id, rung: m.rung, choice: r.flow ? 'pay' : r.rival.answered[m.rung], t: Math.round(G.t) });
  write(`${called(m.id)}'s pressure: ${Rv.pressure}. ${r.flow ? 'Paid.' : r.then[0].toUpperCase() + r.then.slice(1)}.`, { how: 'Did it', key: 'pressure:' + m.id + ':' + m.rung });
  emit('rivals.answered', { id: m.id, choice: x.answers[x.answers.length - 1].choice });
}
// What a threat does, each to its own ledger: his people, his clean money, his cover.
function threat(id) {
  const x = X('rivals');
  x.threats.push({ id, t: Math.round(G.t) });
  emit('rivals.threat', { id });
  if (id === 'widow') {
    const men = G.x.crew.men,
      worst = Object.keys(men).filter((k) => men[k].in && !['sheila', 'ron', 'pauline'].includes(k)).sort((a, b) => men[a].loyalty - men[b].loyalty)[0];
    if (worst && men[worst].loyalty < 0.5) {
      Object.assign(men[worst], { in: false, fate: 'poached' });
      write(`${RULES.game.crew.men[worst].name} drives for the Widow now.`, { how: 'Found out', key: 'poached:' + worst });
    }
  } else if (id === 'agar') G.x.econ.drivers = Math.max(1, G.x.econ.drivers - 1), (x.inspectUntilT = G.t + 2 * 1440);
  else if (G.x.law) G.x.law.deeds.push({ street: 'Quay Street', seen: true, t: G.t }, { street: 'Quay Street', seen: true, t: G.t }, { street: 'Quay Street', seen: true, t: G.t }); // heat he did not earn
}
// ---- the sit-down (3.5.5): one head; accept, defy, or counter with what he knows ----
async function sitDown(m) {
  const x = X('rivals'),
    knows = KNOWS[m.id]();
  const i = await scene(async () => {
    await say(called(m.id), 'Sit down, Mr Nowak. The Hook is the gate of this port, and a gate has one keeper. We will decide today who it is.');
    return choose(called(m.id), 'You work under me, or against me. I would rather under.', ['Accept.', 'Defy.', knows ? 'Counter: ' + knows + '.' : 'Counter (he knows nothing to counter with).']);
  });
  let r = R.sitDown(['accept', 'defy', 'counter'][i], { head: called(m.id), knows: !!knows });
  if (!r.ok) r = R.sitDown('defy', { head: called(m.id) });
  x.sitDown = { head: m.id, headCalled: called(m.id), how: r.how, state: r.state, tributePencePerWeek: r.tributePencePerWeek, othersHeldAtRung: r.othersHeldAtRung, headThreatEveryGameDays: r.headThreatEveryGameDays, headsMenArmed: r.headsMenArmed, t: Math.round(G.t), lastThreatT: G.t, weeksPaid: 0, weeksShort: 0 };
  if (r.how === 'holds') x.r[m.id].truceUntilT = null;
  x.r[m.id] = R.shown(x.r[m.id]);
  write(`The sit-down with ${called(m.id)}: ${r.state}.`, { how: 'Did it', key: 'sitdown' });
  await scene(() => say(called(m.id), r.how === 'under' ? `Good. ${quid(r.tributePencePerWeek)} every Friday, by a man of mine who will call. And nobody else troubles you: that is what it buys.` : r.how === 'war' ? 'Then we are finished talking, Mr Nowak. You will see my people on your street, and you will not like how they come.' : 'I see. Then you and I will leave one another alone. I cannot speak for the others.'));
  emit('rivals.sitdown', { head: m.id, state: r.state, how: r.how, headsMenArmed: r.headsMenArmed });
}
// ---- what the sit-down settled, week after week (3.5.5) ----
function standingWeek() {
  const x = X('rivals'),
    sd = x.sitDown;
  if (!sd) return;
  if (sd.how === 'under') {
    if (pay(sd.tributePencePerWeek, false, sd.headCalled + "'s share, Friday")) {
      sd.weeksPaid++;
      tell(`A man of ${sd.headCalled}'s is at the counter for the Friday envelope. ${quid(sd.tributePencePerWeek)} goes up the hill.`, '', 8);
      write(`Friday: ${quid(sd.tributePencePerWeek)} to ${sd.headCalled}. That is what being under him costs, and what keeps the other two off.`, { how: 'Did it', key: 'tribute:' + sd.weeksPaid });
    } else {
      // he has not got it: the head's second move comes, as for any man who does not pay
      sd.weeksShort++;
      tell(`The Friday envelope for ${sd.headCalled} is short. His man looks at it, and leaves it on the counter.`, '', 8);
      write(`Could not make ${sd.headCalled}'s Friday share. It will be answered.`, { how: 'Did it', key: 'tributeshort:' + sd.weeksShort });
      threat(sd.head);
    }
  }
}
function standingDay() {
  const x = X('rivals'),
    sd = x.sitDown;
  if (!sd || sd.how !== 'war' || G.t - sd.lastThreatT < sd.headThreatEveryGameDays * 1440) return;
  sd.lastThreatT = G.t;
  const Rv = T.rivals[sd.head];
  tell(`${sd.headCalled} again: ${Rv.second}.`, '', 8);
  write(`At war with ${sd.headCalled}: ${Rv.second}. It will come every week until one of them stops.`, { how: 'Saw it himself', key: 'war:' + Math.round(G.t) });
  threat(sd.head);
}
// ---- the Fixer (2.10.4): true reads, a meeting, one truce ----
async function fixer() {
  const x = X('rivals'),
    F = T.fixer;
  const i = await scene(async () => {
    await say(F.name, 'I sell three things, Mr Nowak, and all of them are true.');
    return choose(F.name, 'Which?', [`A read on one of them (${quid(F.readPence)}).`, `A meeting (${quid(F.meetingPence)}).`, `A truce, once (${quid(F.trucePence)}).`, 'Nothing today.']);
  });
  if (i > 2) return;
  const buy = ['read', 'meeting', 'truce'][i];
  const worst = Object.keys(x.r).sort((a, b) => x.r[b].rung - x.r[a].rung)[0];
  const r = R.fixer(buy, { pocketPence: G.money.clean + G.money.dirty, rival: x.r[worst], trucesSold: x.truces, t: G.t });
  if (!r.ok) return tell(r.why === 'one truce only' ? '"I sold you the one truce there is."' : '"Come back when you can pay."', F.name);
  pay(r.pence, false, 'Keith Garbutt, for a ' + buy);
  x.fixer.push({ buy, about: worst, pence: r.pence, read: r.read || null, t: Math.round(G.t) });
  if (buy === 'read') {
    const knows = r.read.knows.length ? r.read.knows.join('; ') : 'nothing yet';
    await scene(() => say(F.name, `${called(worst)} has you at: ${r.read.rung}. What ${called(worst)} knows of you: ${knows}.`));
    write(`Garbutt's read: ${called(worst)} has him at "${r.read.rung}", and knows: ${knows}.`, { how: 'Garbutt said, for money' });
  } else if (buy === 'truce') {
    x.truces++;
    x.r[worst].truceUntilT = r.truceUntilT;
    write(`Garbutt brokered a truce with ${called(worst)}: two weeks. There will not be another.`, { how: 'Garbutt said, for money' });
  } else {
    x.meeting = worst;
    write(`Garbutt can get him in front of ${called(worst)}.`, { how: 'Garbutt said, for money' });
  }
}

register({
  id: 'rivals',
  fresh: () => ({ r: R.fresh(), moves: [], answers: [], threats: [], fixer: [], truces: 0, sitDown: null, meeting: null, inspectUntilT: null }),
  minute(m) {
    if (m % 5 === 0) showMoves();
    const x = X('rivals');
    if (x.inspectUntilT && G.t >= x.inspectUntilT) {
      x.inspectUntilT = null;
      G.x.econ.drivers++;
    }
  },
  hourly(h) {
    if (h === 9 && (G.x.acts ? G.x.acts.act : 1) >= 2) climbAll();
    if (h === 12) standingDay();
  },
  hotspots(out) {
    if (G.tom.space === 'tearoom' && hourNow() >= 14 && hourNow() < 17 && G.x.acts && G.x.acts.fired.includes('rivalNoticed')) out.push({ k: 'T', t: "Keith Garbutt's table", run: fixer });
  },
  hook: {
    x: () => X('rivals'),
    learns,
    climbAll,
    showMoves,
    fixer,
    knows: (id) => KNOWS[id](),
    // ER-RIV-01: every move prints the sightings it rests on
    trace: () => X('rivals').moves.map((m) => ({ id: m.id, rung: m.name, trace: m.trace })),
  },
});
// a rival learns only through its own people: what one of them saw him do, or heard on the radio
on('act', (E) => {
  const k = KINDS[E.kind];
  if (!k || k.word || (k.val >= 0 && k.sev < 0.3)) return;
  const saw = new Set([...(E.wit || []), ...(E.party || [])]);
  for (const id in T.rivals) for (const eye of T.rivals[id].eyes) if (saw.has(eye)) learns(id, eye, k.truth(E).replace(/^Tom /, 'he '), E.id);
});
on('fare.done', ({ f, P }) => {
  // the radio nobody can help overhearing: his day driver hears every fare he takes
  if (G.x.crew.men.kevin.in && f && f.id && ['wait', 'parcel', 'tail_hal'].includes(f.id)) learns('widow', 'kevin', 'he took an odd fare off the radio (' + f.id + ')', null);
});
on('crew.broke', ({ id, fate }) => {
  if (fate === 'talks to a rival') for (const r in T.rivals) learns(r, T.rivals[r].eyes[0], RULES.game.crew.men[id].name + ' told them what he knows', null);
});
on('crew.struck', ({ rival }) => {
  const x = X('rivals');
  if (x.r[rival]) x.r[rival].sightings.push({ by: T.rivals[rival].eyes[0], what: 'his men came at their property', t: G.t, e: null });
});
on('econ.week', () => standingWeek());
// Act II's beats that are the rivals' business: each is something their own people can see, so they come sooner
on('acts.beat', ({ id }) => {
  if (id === 'realBook') G.x.crime.facts.real_book = Math.round(G.t); // a fact he holds now: it answers a pressure or a sit-down
  if (id === 'rivalNoticed') write('If somebody is asking about him, somebody sells the answers: Keith Garbutt, at the back table of the tea room, two till five.', { key: 'garbutt', how: 'Sheila says', who: 'sheila' });
  const what = T.beatSightings[id];
  if (!what) return;
  const x = X('rivals');
  for (const r in x.r) {
    // the whole port can see three cars on the air, or open ground: each rival's first man counts it, twice over if the ground is open
    const n = id === 'fleet' ? 1 : T.climbsOnSightingsAtLeast;
    for (let i = 0; i < n; i++) learns(r, T.rivals[r].eyes[0], what, null);
  }
});
