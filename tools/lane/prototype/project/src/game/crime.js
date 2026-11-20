// LEDGER, the whole game: the system "crime": the verbs of jobs done with the hands (DESIGN 4; DESIGN-ADDENDUM A2,
// A4, A5, A23, A30, A33 to A35). Getting in three ways, searching and taking, lifts and the hot mark, the fence,
// a hand in a pocket, damage by hand, tails, minding, casing, getting rid of things, pockets and storage, yard dogs.
// Every verb works with or without a job; the job list (jobsx.js) hears of each through core's emit().
// The rules are the pure piece pieces/crime_rules.js; this file only joins them to the street.
import { G, day, hour } from '../state.js';
import { hyp, clamp, money, angDiff } from '../util.js';
import { act, seed, remember } from '../events.js';
import { note, meet } from '../ledger.js';
import { sub, say, choose, scene, tomName } from '../ui.js';
import { roomPos, INSIDE } from '../map.js';
import { sense, tomTarget, knowsWho, noiseRadius, perceivers } from '../seeing.js';
import { goToPoint } from '../routines.js';
import { pay, earn } from '../money.js';
import { F } from '../fight.js';
import { endTalk } from '../talk.js';
import { RULES } from '../rules.js';
import { register, on, emit, X, PLACES } from './core.js';
import { PIECE } from './pieces/crime_rules.js';
import { SITES, BREAKABLES, POCKETS } from './crime_sites.js';

const R = PIECE.fns;
const T = () => RULES.game.crime;
const C = () => X('crime');
const tom = () => G.tom;
const near = (xz, r) => tom().space === 'street' && !tom().inCar && hyp(tom().x, tom().z, xz[0], xz[1]) < r;
const P_ = (id) => G.people[id];
const zoneNow = () => G.env.zone(tom().x, tom().z);

function fresh() {
  return {
    items: { coat: [], hand: null }, // what the crime verbs have put on him (his weapon and a job's bag are added in carried)
    carried: { coat: [], hand: null }, // exactly what a search would find (A5); kept current every step
    drawer: [], // the locked drawer at the office: small things
    shed: [], // the yard shed: big things
    goods: {}, // thing -> { honestPence, owner, street, takenAt, cash }
    keys: {}, // site -> 'lent' | 'lifted' | 'copy'
    sites: {}, // site -> { in, forcedAt, way, searched: { containerId: minute } }
    cased: {}, // site -> { secs, got: ['hours', 'key', 'way'] }
    marks: [], // damage that stays until mended: { id, thing, owner, at, untilMinute, mended, known }
    lifts: [], // pockets lifted: { who, thing, at, missedAt, suspects, missed }
    dogs: {}, // site -> { fedAt, barkedAt }
    blood: false,
    coatBlood: false,
    tails: {}, // target -> { st, doubts, learned }
    minded: {}, // target -> minutes stood with
    fence: { walkedAt: null, sold: 0 },
    purses: null, // debtor -> pence in the purse today
    log: [], // what was done, for the tests and the variety check
  };
}

// ---------- A5 pockets ----------
function refreshCarried() {
  const c = C(),
    t = tom();
  const coat = c.items.coat.slice();
  if (t.weapon && !coat.includes(t.weapon)) coat.push(t.weapon);
  const hand = c.items.hand || (t.carry === 'bag' ? 'the holdall' : t.carry === 'suitcase' ? 'the suitcase' : null);
  c.carried = { coat, hand };
  return c.carried;
}
export const carried = () => refreshCarried();
function pocket(thing, where) {
  const c = C(),
    r = R.take(refreshCarried(), thing, where);
  if (!r.ok) {
    sub(r.why, '', 'over', 3);
    return false;
  }
  if (r.where === 'hand') c.items.hand = thing;
  else c.items.coat.push(thing);
  refreshCarried();
  return true;
}
function unpocket(thing) {
  const c = C(),
    i = c.items.coat.indexOf(thing);
  if (i >= 0) c.items.coat.splice(i, 1);
  else if (c.items.hand === thing) c.items.hand = null;
  else return false;
  refreshCarried();
  return true;
}
const has = (thing) => C().items.coat.includes(thing) || C().items.hand === thing;
const lg = (what, x = {}) => {
  const c = C();
  c.log.push(Object.assign({ what, t: Math.round(G.t), played: Math.round(G.played) }, x));
  if (c.log.length > 300) c.log.splice(0, 100);
};

// ---------- timed acts: a held moment, never a test of reflexes ----------
// One at a time. It ends when its time is up, or stops when Tom walks off. (Not saved: a load starts with none.)
let busy = null;
function begin(what, seconds, done, x = {}) {
  const t = tom();
  busy = Object.assign({ what, t: 0, need: seconds, x0: t.x, z0: t.z, done }, x);
}
function stepBusy(dt) {
  if (!busy) return;
  const t = tom(),
    b = busy;
  if (hyp(t.x, t.z, b.x0, b.z0) > (b.slack || T().search.stopsWhenTomMovesMetres) || t.inCar || F.on) {
    busy = null;
    if (b.stopped) b.stopped();
    return;
  }
  b.t += dt;
  if (b.tick) b.tick(b);
  if (busy === b && b.t >= b.need) {
    busy = null;
    b.done();
  }
}

// ---------- 1.6.1 getting in ----------
const siteState = (id) => C().sites[id] || (C().sites[id] = { in: false, forcedAt: null, way: null, searched: {} });
function waysNow(S) {
  return R.waysIn(S, { hasKey: !!C().keys[S.id], hour: hour(), dayIndex: day() });
}
function enter(S, way) {
  const st = siteState(S.id),
    E = T().entry;
  if (way === 'force') {
    begin(
      'forcing ' + S.name,
      E.forceRealSeconds,
      () => {
        st.in = true;
        st.way = 'force';
        st.forcedAt = Math.round(G.t);
        const ev = act('break_in', { what: S.name, noiseR: E.forceNoiseMetres, zone: zoneNow() });
        mark({ id: S.id + 'door', thing: 'the door of ' + S.name, owner: S.owner, untilMinute: G.t + E.forceMarkLastsGameMinutes, door: true });
        sub('The frame gives with a crack that carries. The door will show it for a day.', '', 'over', 4.5);
        lg('entered', { site: S.id, way: 'force', seen: ev.wit.length });
        emit('deed', { E: ev });
        emit('crime:entered', { site: S.id, way: 'force', E: ev });
      },
      { slack: 1.2 },
    );
    sub('He puts his shoulder to it.', '', 'over', 2.5);
    return;
  }
  st.in = true;
  st.way = way;
  const ev = act('let_in', { what: S.name, zone: zoneNow() });
  sub(way === 'key' ? 'The key turns. Inside, and the door pulled to.' : 'In by ' + S.backWay.words.split(',')[0] + '. Nobody about.', '', 'over', 4);
  lg('entered', { site: S.id, way, seen: ev.wit.length });
  emit('crime:entered', { site: S.id, way, E: ev });
}
function leaveSites() {
  for (const id in SITES) {
    const st = C().sites[id];
    if (st && st.in && !near(SITES[id].door, T().entry.insideWithinMetres)) {
      st.in = false;
      st.warn = 0;
      emit('crime:left', { site: id });
    }
  }
}
// the night rule: the owner near and looking warns, warns again, then acts, within half a minute at worst
function ownerWatch(dt) {
  const E = T().entry;
  for (const id in SITES) {
    const st = C().sites[id];
    if (!st || !st.in) continue;
    const S = SITES[id],
      O = P_(S.owner);
    if (!O || O.dead || O.gone) continue;
    const d = hyp(O.x, O.z, tom().x, tom().z);
    if (d > E.ownerWarnsWithinMetres || !sense(O, tomTarget()).see) continue;
    st.warn = (st.warn || 0) + dt;
    if (!st.w1) {
      st.w1 = 1;
      sub('"Oi. What are you doing in there?"', tomName(O), 'face', 4);
    } else if (st.w1 === 1 && st.warn > E.secondWarningAfterRealSeconds) {
      st.w1 = 2;
      sub('"I said out. I\'ll not say it a third time."', tomName(O), 'face', 4);
    } else if (st.w1 === 2 && st.warn > E.actsAfterRealSeconds) {
      st.w1 = 0;
      st.warn = 0;
      st.in = false;
      const ev = act('trespass', { what: S.name, target: S.owner, zone: zoneNow() });
      sub('He has had a good look, and he is going for somebody.', '', 'over', 4);
      note(`${O.def.name} found Tom inside ${S.name} and warned him off twice. He knows the face now.`, 'note', null, { who: S.owner, how: 'Was there', ev: ev.id });
      emit('crime:caught', { site: id, by: S.owner, E: ev });
    }
  }
}

// ---------- A4 searching and taking ----------
function search(S, K) {
  const st = siteState(S.id),
    t = tom(),
    light = t.light === undefined ? 1 : t.light,
    q = R.searchTime({ container: K.kind, forced: !!K.forced, light: Math.min(light, 0.25), torch: !!t.torchOn });
  // inside a shut place it is dark: the street's light does not reach, so the torch decides (A33)
  begin(
    'searching ' + K.name,
    q.seconds,
    () => {
      st.searched[K.id] = Math.round(G.t);
      const H = K.holds,
        ev = act(K.forced ? 'forced_cupboard' : 'searched_place', { what: K.forced ? K.name : S.name, noiseR: q.noiseMetres, zone: zoneNow() });
      lg('searched', { site: S.id, container: K.id, seconds: q.seconds, noise: q.noiseMetres, dark: q.dark });
      if (K.forced) emit('deed', { E: ev });
      if (!H) return sub('Nothing in ' + K.name + ' worth the taking.', '', 'over', 3);
      if (H.paper) {
        note(H.paper, 'note', 'paper_' + S.id + '_' + K.id, { how: 'Found it', ev: ev.id });
        sub('In ' + K.name + ': ' + H.thing + '. He reads it and puts it back as it lay.', '', 'over', 5);
      } else if (H.goods) {
        if (!pocket(H.thing, H.hand ? 'hand' : undefined)) {
          delete st.searched[K.id];
          return;
        }
        C().goods[H.thing] = { honestPence: H.goods.honestPence, owner: S.owner, street: S.street, takenAt: Math.round(G.t), cash: !!H.goods.cash, site: S.id };
        act('took_goods', { what: H.thing, from: S.name, zone: zoneNow() });
        sub('In ' + K.name + ': ' + H.thing + '. ' + (H.hand ? 'In his arms.' : 'Under the coat.'), '', 'over', 4);
        note(`Took ${H.thing} from ${S.name}. ${P_(S.owner) ? P_(S.owner).def.name : 'Its owner'} would know it anywhere.`, 'note', null, { how: 'Did it', ev: ev.id });
      }
      emit('crime:found', { site: S.id, container: K.id, thing: H.thing, E: ev });
    },
    {},
  );
  sub((q.dark ? 'Dark in here. He goes through ' : 'He goes through ') + K.name + (q.dark ? ' by feel.' : '.'), '', 'over', 2.5);
}

// ---------- A35 damage by hand ----------
function mark(m) {
  const c = C();
  c.marks.push(Object.assign({ at: Math.round(G.t), mended: false, known: false }, m));
  if (c.marks.length > 40) c.marks.shift();
}
function smash(B) {
  const D = T().damage;
  begin(
    'breaking ' + B.thing,
    D.takesRealSeconds,
    () => {
      const d = R.damage({ atMinute: G.t }),
        ev = act('damage_thing', { what: B.thing, target: undefined, noiseR: d.noiseMetres, zone: B.zone });
      mark({ id: B.id, thing: B.thing, owner: B.owner, untilMinute: d.markUntilMinute, knowsBy: d.ownerKnowsByMinute, ev: ev.id });
      sub('Glass goes. In a quiet street that is the loudest thing for a hundred yards.', '', 'over', 4.5);
      lg('damage', { thing: B.id, seen: ev.wit.length });
      emit('deed', { E: ev });
      emit('crime:damage', { thing: B.id, owner: B.owner, E: ev });
    },
    { slack: 1.5 },
  );
}
// by morning the owner knows, and reads it as a message from whoever he suspects
function ownersLearn(minute) {
  for (const m of C().marks) {
    if (!m.mended && minute >= m.untilMinute) m.mended = true;
    if (m.known || m.door || !m.knowsBy || minute < m.knowsBy) continue;
    m.known = true;
    const O = P_(m.owner);
    if (!O || O.dead) continue;
    const E = G.ev[m.ev];
    if (E && !O.mind.by[E.id]) {
      // he holds only the aftermath: he saw the damage, not who did it, unless somebody tells him
      remember(O, E, { src: 'heard', who: 'man', sure: 0.5, heat: 0.7 });
    }
    seed('damage_found', [m.owner], { name: O.def.name, what: m.thing });
    emit('crime:damagefound', { thing: m.id, owner: m.owner });
  }
  // a forced door shows for a day, then is mended
  for (const id in C().sites) {
    const st = C().sites[id];
    if (st.forcedAt !== null && !R.doorShowsForced(st.forcedAt, minute)) st.forcedAt = null;
  }
}

// ---------- A34 a hand in a pocket ----------
function peopleNear(P, r) {
  let n = 0;
  for (const Q of perceivers()) if (Q !== P && !Q.gone && !Q.dead && Q.space === P.space && hyp(Q.x, Q.z, P.x, P.z) < r) n++;
  return n;
}
function liftTarget() {
  const t = tom(),
    K = T().pocket;
  if (t.inCar || F.on) return null;
  for (const id in POCKETS) {
    const P = P_(id);
    if (!P || P.dead || P.gone || P.space !== t.space) continue;
    if (C().lifts.some((l) => l.who === id)) continue;
    if (hyp(P.x, P.z, t.x, t.z) < K.besideWithinMetres) return P;
  }
  return null;
}
function lift(P) {
  const K = T().pocket,
    W = POCKETS[P.id],
    t = tom();
  const dir = Math.atan2(t.x - P.x, t.z - P.z),
    attentive = Math.abs(angDiff(P.ang, dir)) < K.attentiveFacingWithinRadians || !!P.talking,
    q = R.pocketLift({ attentive, light: G.env.lightAt(t.x, t.z, t.space), peopleNear: peopleNear(P, K.crowdWithinMetres) });
  let turned = false;
  begin(
    'lifting from ' + P.def.name,
    q.takesSeconds,
    () => {
      if (q.felt) {
        const ev = act('pocket_felt', { target: P.id, zone: zoneNow() });
        P.mind.regard = clamp(P.mind.regard - 0.3, -1, 1);
        sub('"Get your hand out of there!"', tomName(P), 'face', 4);
        note(`${tomName(P)} felt a hand in the pocket and turned on Tom there and then.`, 'note', null, { who: P.id, how: 'Was there', ev: ev.id });
        lg('lift', { who: P.id, felt: true });
        emit('crime:lift', { who: P.id, felt: true, E: ev });
        return;
      }
      if (!pocket(W.thing)) return;
      const noticed = sense(P, tomTarget()).see || P.mind.attn > 0.2 ? ['tom'] : [],
        km = R.keyMissed({ liftedAtMinute: G.t, noticedNear: noticed });
      C().lifts.push({ who: P.id, thing: W.thing, at: Math.round(G.t), missedAt: km.missedAtMinute, suspects: km.suspects, missed: false });
      if (W.key) C().keys[W.key] = 'lifted';
      const ev = act('pocket_lift', { target: undefined, name: P.def.name, what: W.thing, zone: zoneNow() });
      if (W.paper) note(W.paper, 'note', 'pocket_' + P.id, { how: 'Read it', ev: ev.id });
      else note(`${W.thing.replace(/^./, (m) => m.toUpperCase())}, out of ${tomName(P)}'s pocket. It will be missed by morning.`, 'note', null, { how: 'Did it', ev: ev.id });
      sub('Two fingers, and it is his. ' + tomName(P) + ' never turns.', '', 'over', 4);
      lg('lift', { who: P.id, felt: false, thing: W.thing });
      emit('crime:lift', { who: P.id, felt: false, thing: W.thing, E: ev });
    },
    {
      slack: 0.7,
      tick: (b) => {
        // his head turns before any felt lift (ER-EYES-03): Tom can stop by stepping away
        if (q.felt && !turned && b.t >= q.headTurnsAtSeconds) {
          turned = true;
          P.ang = dir;
          P.alert = { x: t.x, z: t.z, t: 2 };
          lg('headturn', { who: P.id, at: b.t });
          sub('His head starts to turn.', '', 'over', 1.5);
        }
      },
      stopped: () => lg('lift_stopped', { who: P.id, turned }),
    },
  );
}
function keysMissed(minute) {
  for (const l of C().lifts) {
    if (l.missed || minute < l.missedAt) continue;
    l.missed = true;
    const P = P_(l.who);
    if (!P || P.dead) continue;
    const ev = seed('key_missed', [l.who], { name: P.def.name, what: l.thing });
    // suspicion falls only on people he noticed near him (ER-EYES-05)
    if (l.suspects.includes('tom')) {
      P.mind.regard = clamp(P.mind.regard - 0.15, -1, 1);
      l.suspectsTom = true;
    }
    emit('crime:missed', { who: l.who, thing: l.thing, suspects: l.suspects, E: ev });
  }
}

// ---------- 2.7.6 the fence, with A30's haggle ----------
function sellable() {
  return Object.keys(C().goods).filter((g) => has(g) && !C().goods[g].cash);
}
async function fenceScene(thing) {
  const c = C(),
    g = c.goods[thing],
    Rt = P_('rita'),
    F_ = T().fence;
  const hot = R.hotMark({ honestPence: g.honestPence, gameDaysSince: (G.t - g.takenAt) / 1440, onTheOwnersStreet: g.street === 'Quay Street' });
  // Rita knows her own goods on sight: the owner never forgets
  if (g.owner === 'rita') {
    await say('rita', "That's mine. That's off my own shelf. Put it down and get out of my shop.");
    Rt.mind.regard = clamp(Rt.mind.regard - 0.4, -1, 1);
    const ev = act('fenced', { what: thing, target: 'rita', zone: 'Quay Street' });
    note(`Offered Rita ${thing}. It was hers. She knew it on sight.`, 'note', null, { who: 'rita', how: 'Was there', ev: ev.id });
    lg('fence', { thing, own: true });
    emit('crime:fenced', { thing, sold: false, own: true });
    return;
  }
  let asks = 0,
    spoken = [];
  for (;;) {
    const o = R.fenceOffer({ honestPence: g.honestPence, hot, pursePence: F_.ritaPursePence, regard: Rt.mind.regard }, asks);
    if (o.walks) {
      await say('rita', "No. That's me done. Take it somewhere else.");
      c.fence.walkedAt = Math.round(G.t);
      lg('fence', { thing, sold: false, offers: spoken });
      emit('crime:fenced', { thing, sold: false });
      return;
    }
    spoken.push(o.offerPence);
    const opts = ['Take it.', o.last ? 'Walk away.' : 'Ask for more.'];
    if (!o.last) opts.push('Walk away.');
    const i = await choose('rita', `${o.face} "${money(o.offerPence)}.${hot > 0.5 ? " It's warm, that. I can feel it from here." : ''}"`, opts);
    if (i === 0) {
      unpocket(thing);
      delete c.goods[thing];
      earn(o.offerPence, true, 'fenced ' + thing);
      c.fence.sold++;
      const ev = act('fenced', { what: thing, target: 'rita', zone: 'Quay Street' });
      note(`Sold ${thing} to Rita for ${money(o.offerPence)}. In the tin.`, 'money', null, { who: 'rita', how: 'Counted it', ev: ev.id });
      lg('fence', { thing, sold: true, pence: o.offerPence, offers: spoken });
      emit('crime:fenced', { thing, sold: true, pence: o.offerPence });
      return;
    }
    if (opts[i] === 'Walk away.') {
      Rt.mind.regard = clamp(Rt.mind.regard - F_.walkingAwayCostsRegard, -1, 1);
      c.fence.walkedAt = Math.round(G.t);
      await say('rita', Rt.mind.regard > 0 ? "Suit yourself. It'll not be worth more tomorrow." : "Mind the step on your way out.");
      lg('fence', { thing, sold: false, walked: true, offers: spoken });
      emit('crime:fenced', { thing, sold: false, walked: true });
      return;
    }
    asks++;
  }
}

// ---------- A2 tailing on foot ----------
// A tail is live while a job (or the test hook) names a target. The target looks back on a rhythm; made on the
// watcher's ladder; losing sight is never failing.
let tail = null; // { who, lookIn, doubts, still, sawMove, goal }
export function startTail(who, learns) {
  const P = P_(who);
  if (!P) return false;
  tail = { who, lookIn: R.tailLooksEvery(P.def.nerve), doubts: 0, still: 0, sawMove: false, learns: learns || null, looks: [] };
  C().tails[who] = { st: 'on', doubts: 0, learned: null };
  return true;
}
export function stopTail(why = 'stopped') {
  if (!tail) return;
  endTail(why);
}
function endTail(end) {
  const tl = tail,
    P = P_(tl.who),
    st = C().tails[tl.who];
  tail = null;
  st.st = end;
  let ev = null;
  if (end === 'made') {
    ev = act('tailed', { target: tl.who, zone: zoneNow() });
    sub('"You following me? Aye. Thought so."', tomName(P), 'face', 4);
    note(`${tomName(P)} caught Tom following and said so to his face.`, 'note', null, { who: tl.who, how: 'Was there', ev: ev.id });
  } else if (end === 'arrived') {
    const where = G.env.zone(P.x, P.z),
      line = tl.learns || `Followed ${tomName(P)} to ${where}. That is where the walk ends at this hour.`;
    st.learned = line;
    note(line, 'note', null, { who: tl.who, how: 'Saw it' });
    sub('So that is where he goes.', '', 'over', 3);
  }
  lg('tail', { who: tl.who, end, doubts: tl.doubts, looks: tl.looks });
  emit('crime:tail', { who: tl.who, end, doubts: tl.doubts, E: ev });
}
function stepTail(dt) {
  if (!tail) return;
  const K = T().tail,
    P = P_(tail.who),
    t = tom();
  if (!P || P.dead || P.gone) return endTail('stopped');
  const d = hyp(P.x, P.z, t.x, t.z),
    inSight = P.space === t.space && d < K.followsWithinMetres && G.env.los(P.x, P.z, t.x, t.z);
  if (P.moving) {
    tail.still = 0;
    if (inSight) tail.sawMove = true;
  } else tail.still += dt;
  if (tail.sawMove && !P.moving && tail.still > K.arrivesAfterStillRealSeconds && inSight) return endTail('arrived');
  if (!P.moving) return; // he looks back as he walks, and at every corner and stop
  tail.lookIn -= dt;
  if (tail.lookIn > 0) return;
  tail.lookIn = R.tailLooksEvery(P.def.nerve);
  lookBack(P, inSight, d);
}
function lookBack(P, inSight, d) {
  const t = tom(),
    caught = R.tailCaught({ inSight: inSight && t.space === 'street', metres: d, light: G.env.lightAt(t.x, t.z, t.space) }),
    r = R.tailLook({ caught, knowsHim: knowsWho(P), doubts: tail.doubts });
  tail.looks.push({ caught, state: r.state, d: Math.round(d) });
  if (inSight) P.ang = Math.atan2(t.x - P.x, t.z - P.z);
  tail.doubts = r.doubts;
  C().tails[tail.who].doubts = r.doubts;
  if (r.state === 'doubt') {
    P.hurry = 1;
    sub(r.sign.replace(/^He/, tomName(P)), '', 'over', 3.5);
    emit('crime:taildoubt', { who: tail.who, doubts: r.doubts });
  } else if (r.state === 'made') endTail('made');
}

// ---------- minding: stood with somebody ----------
let mind = null; // { who, t }
export function startMind(who) {
  mind = { who, t: 0 };
  return true;
}
function stepMind(dt) {
  if (!mind) return;
  const K = T().mind,
    P = P_(mind.who),
    t = tom();
  if (!P || P.dead || P.gone) {
    mind = null;
    return emit('crime:mind', { who: null, ok: false });
  }
  if (P.space !== t.space || hyp(P.x, P.z, t.x, t.z) > K.standsWithinMetres) {
    if (mind.t > 2 && hyp(P.x, P.z, t.x, t.z) > K.standsWithinMetres * 3) {
      const who = mind.who;
      mind = null;
      lg('mind', { who, ok: false });
      emit('crime:mind', { who, ok: false });
    }
    return;
  }
  mind.t += dt;
  if (mind.t >= K.countsAfterRealSeconds) {
    const who = mind.who;
    mind = null;
    const ev = act('stood_with', { target: who, zone: zoneNow() });
    C().minded[who] = (C().minded[who] || 0) + 1;
    note(`Stood with ${tomName(P)} on ${zoneNow()}. Whoever passed saw the two together.`, 'note', null, { who, how: 'Was there', ev: ev.id });
    lg('mind', { who, ok: true, seen: ev.wit.length });
    emit('crime:mind', { who, ok: true, E: ev });
  }
}

// ---------- A23 casing ----------
function caseSpot() {
  const K = T().casing,
    t = tom();
  if (t.space !== 'street' || F.on) return null;
  const x = t.inCar ? G.car.x : t.x,
    z = t.inCar ? G.car.z : t.z;
  for (const id in SITES) {
    const S = SITES[id],
      d = hyp(x, z, S.door[0], S.door[1]),
      cs = C().cased[id];
    if (d >= K.fromAtLeastMetres && d <= K.fromAtMostMetres && G.env.los(x, z, S.door[0], S.door[1]) && (!cs || cs.got.length < 3)) return S;
  }
  return null;
}
const hh = (h) => {
  const m = Math.round((h % 1) * 60);
  return (Math.floor(h) % 24) + (m ? ':' + String(m).padStart(2, '0') : " o'clock").replace(/^(\d+) o'clock$/, "$1 o'clock");
};
const span = (a) => a.map((s) => `${hh(s.fromHour)} to ${hh(s.untilHour)}`).join(' and ');
export function casingLines(S) {
  const O = P_(S.owner),
    name = O ? O.def.name : 'its owner',
    hours = R.hoursAt(RULES.schedules[S.owner] || [], S.ownerAt, day());
  return {
    hours: `${name} is at ${S.name} from ${hours.length ? span(hours) : 'no set hour'}, as far as Tom has seen.`,
    key: `${P_(S.key.holder) ? P_(S.key.holder).def.name : 'Somebody'} keeps the key to ${S.name}, in a pocket.`,
    way: `${S.name}: ${S.backWay.words}, from ${hh(S.backWay.fromHour)} to ${hh(S.backWay.untilHour)}.`,
  };
}
function casing(S) {
  const K = T().casing,
    cs = C().cased[S.id] || (C().cased[S.id] = { secs: 0, got: [] }),
    lines = casingLines(S);
  begin(
    'watching ' + S.name,
    K.openWayAfterRealSeconds - cs.secs + 0.2,
    () => {
      const ev = act('cased', { what: S.name, zone: zoneNow() });
      lg('cased', { site: S.id, got: cs.got.slice(), seen: ev.wit.length });
      emit('crime:cased', { site: S.id, got: cs.got.slice() });
    },
    {
      slack: K.stopsWhenTomMovesMetres,
      tick: (b) => {
        cs.secs = Math.max(cs.secs, K.openWayAfterRealSeconds - (b.need - b.t) + 0.2);
        for (const k of R.caseLearns(cs.secs))
          if (!cs.got.includes(k)) {
            cs.got.push(k);
            note(lines[k], 'note', 'case_' + S.id + '_' + k, { who: S.owner, how: 'Watched it' });
            sub(lines[k], '', 'over', 5);
          }
      },
      stopped: () => lg('cased_stopped', { site: S.id, got: cs.got.slice() }),
    },
  );
  sub('He settles to watch ' + S.name + ' from ' + S.watchFrom + '.', '', 'over', 3);
}

// ---------- 1.6.7 getting rid of things ----------
const atWater = () => tom().space === 'street' && !tom().inCar && tom().z > T().rid.waterFromZ - T().rid.waterWithinMetres && tom().z < T().rid.waterFromZ + 3;
function throwIn(thing) {
  unpocket(thing);
  delete C().goods[thing];
  if (thing === tom().weapon) tom().weapon = null;
  const ev = act('threw_in', { what: thing, zone: zoneNow() });
  sub('It goes in with hardly a sound. What goes in the water is gone.' + (ev.wit.length ? ' Somebody was looking.' : ''), '', 'over', 4.5);
  lg('threw', { thing, seen: ev.wit.length });
  emit('crime:rid', { thing, how: 'water', seen: ev.wit.length });
}
function unseenNow() {
  const Tt = tomTarget();
  for (const P of perceivers()) if (sense(P, Tt).see) return false;
  return true;
}
function washUp() {
  const r = R.washBlood({ water: true, private: unseenNow() });
  if (!r.clean) return sub(r.why, '', 'over', 3);
  C().blood = false;
  act('washed_up', { zone: zoneNow(), silent: true });
  sub('Cold water and the door shut. The blood is off his hands. Not off the coat.', '', 'over', 4);
  lg('washed', { where: 'sink' });
  emit('crime:rid', { thing: 'blood', how: 'water' });
}

// ---------- 4.11.1 yard dogs: never hurt, by any verb ----------
function stepDogs() {
  const K = T().dogs,
    t = tom();
  for (const id in SITES) {
    const D = SITES[id].dog;
    if (!D || t.space !== 'street') continue;
    const ds = C().dogs[id] || (C().dogs[id] = { fedAt: null, barkedAt: null, played: -99 }),
      d = hyp(t.inCar ? G.car.x : t.x, t.inCar ? G.car.z : t.z, D.x, D.z);
    if (!R.dogBarks({ stranger: true, metres: d, fedMinutesAgo: ds.fedAt === null ? null : G.t - ds.fedAt })) continue;
    if (G.played - ds.played < K.barksAgainAfterRealSeconds) continue;
    ds.played = G.played;
    ds.barkedAt = Math.round(G.t);
    t.noiseP = Math.max(t.noiseP, K.barkNoiseMetres);
    sub('A dog barks behind the gate, and keeps on.', '', 'over', 3);
    // the bark is a noise that draws the owner, if he is within its reach
    const O = P_(SITES[id].owner),
      reach = noiseRadius(K.barkNoiseMetres);
    let drew = false;
    if (O && !O.dead && !O.gone && O.space === 'street' && hyp(O.x, O.z, D.x, D.z) < reach) {
      O.alert = { x: D.x, z: D.z, t: K.ownerLooksWithinRealSeconds };
      if (!O.hold) goToPoint(O, D.x + 1.5, D.z - 2.5);
      drew = true;
    }
    lg('bark', { site: id, drew });
    emit('crime:bark', { site: id, drew });
  }
}
function feedDog(id) {
  unpocket('a bag of scraps');
  C().dogs[id] = Object.assign(C().dogs[id] || {}, { fedAt: Math.round(G.t) });
  act('fed_dog', { zone: zoneNow() });
  sub('A handful of scraps through the gate. The barking stops, and a tail goes instead.', '', 'over', 4);
  lg('fed', { site: id });
}

// ---------- blood: a give-away until washed ----------
let wasFight = false;
function stepBlood() {
  if (F.on && (F.usedW || (F.struck && tom().hurt > 0.3))) wasFight = true;
  if (!F.on && wasFight) {
    wasFight = false;
    C().blood = true;
    if (tom().coat) C().coatBlood = true;
  }
}

// ---------- storage: the locked drawer and the yard shed ----------
async function storeScene(which) {
  const c = C(),
    store = c[which],
    name = which === 'drawer' ? 'the locked drawer' : 'the yard shed';
  for (;;) {
    const mine = c.items.coat.concat(c.items.hand ? [c.items.hand] : []),
      opts = mine.map((x) => 'Put ' + x + ' in').concat(store.map((x) => 'Take ' + x + ' out'), ['Shut it.']);
    const words = R.carriedWords(refreshCarried()) + (store.length ? ' In ' + name + ': ' + store.join(', ') + '.' : ' ' + name.replace(/^./, (m) => m.toUpperCase()) + ' is empty.');
    const i = await choose('', words, opts);
    if (i >= mine.length + store.length) return;
    if (i < mine.length) {
      unpocket(mine[i]);
      store.push(mine[i]);
    } else {
      const thing = store[i - mine.length];
      if (R.take(refreshCarried(), thing, which === 'shed' ? 'hand' : undefined).ok) {
        store.splice(i - mine.length, 1);
        pocket(thing, which === 'shed' ? 'hand' : undefined);
      } else await say('', 'His pockets are full and his hand is taken.');
    }
    emit('crime:stored', { where: which, has: store.slice() });
  }
}

// ---------- collections: what a purse holds (2.8.2) ----------
function purses() {
  const c = C();
  if (!c.purses) c.purses = Object.assign({}, T().debts.pursePence);
  return c.purses;
}

// ---------- the system ----------
function hotspots(out) {
  const t = tom(),
    c = C(),
    E = T().entry;
  if (busy) {
    out.push({ k: 'E', t: 'Leave off ' + busy.what, run: () => (busy = null) });
    return;
  }
  if (t.space === 'street') {
    for (const id in SITES) {
      const S = SITES[id],
        st = siteState(id);
      if (!st.in && near(S.door, E.doorWithinMetres)) {
        const ways = waysNow(S);
        for (const w of ways) {
          if (w.way === 'key') out.push({ k: 'E', t: 'Unlock ' + S.name, run: () => enter(S, 'key') });
          else if (w.way === 'back') out.push({ k: 'E', t: 'In by ' + S.backWay.words.split(',')[0], run: () => enter(S, 'back') });
          else out.push({ k: 'T', t: 'Force the door of ' + S.name, run: () => enter(S, 'force') });
        }
      } else if (st.in && near(S.door, E.insideWithinMetres)) {
        const K = S.containers.find((k) => !st.searched[k.id]);
        if (K) out.push({ k: 'E', t: (K.forced ? 'Break open ' : 'Search ') + K.name, run: () => search(S, K) });
      }
      if (S.dog && has('a bag of scraps') && hyp(t.x, t.z, S.dog.x, S.dog.z) < T().dogs.barksWithinMetres)
        out.push({ k: 'G', t: 'Give the dog a scrap', run: () => feedDog(id) });
    }
    for (const B of BREAKABLES)
      if (near(B.at, T().damage.withinMetres) && !c.marks.some((m) => m.id === B.id && R.markShows(m, G.t))) {
        out.push({ k: 'G', t: 'Smash ' + B.thing, run: () => smash(B) });
        break;
      }
    if (atWater()) {
      const thing = c.items.hand || c.items.coat[c.items.coat.length - 1] || (t.weapon && !t.armed ? t.weapon : null);
      if (thing) out.push({ k: 'G', t: 'Throw ' + thing + ' in the water', run: () => throwIn(thing) });
    }
    const S = caseSpot();
    if (S && !out.some((o) => o.k === 'T')) out.push({ k: 'T', t: 'Watch ' + S.name + ' a while', run: () => casing(S) });
    if (hyp(t.x, t.z, 23.4, 36) < 2.2) out.push({ k: 'G', t: 'The yard shed', run: () => scene(() => storeScene('shed')) });
  } else if (t.space === 'mickeys') {
    const [dx, dz] = roomPos('mickeys', INSIDE.cot.x - 1.4, INSIDE.cot.z);
    if (hyp(t.x, t.z, dx, dz) < T().pockets.drawerWithinMetres) {
      out.push({ k: 'G', t: 'The locked drawer: get ready', run: () => scene(() => storeScene('drawer')) });
      if (c.blood) out.push({ k: 'T', t: 'Wash at the sink', run: washUp });
    }
  } else if (t.space === 'boarding' && c.blood) {
    const [bx, bz] = roomPos('boarding', INSIDE.bed.x, INSIDE.bed.z);
    if (hyp(t.x, t.z, bx, bz) < 3) out.push({ k: 'T', t: 'Wash at the basin', run: washUp });
  } else if (t.space === 'tangs') {
    const [cx, cz] = roomPos('tangs', INSIDE.chipCounter.x, INSIDE.chipCounter.z);
    if (hyp(t.x, t.z, cx, cz) < INSIDE.chipCounter.within && !has('a bag of scraps'))
      out.push({
        k: 'G',
        t: 'A bag of scraps, ' + money(T().dogs.scrapPence),
        run: () => {
          if (!R.canTake(refreshCarried(), 'coat')) return sub('His pockets are full.', '', 'over', 2.5);
          if (!pay(T().dogs.scrapPence, false, 'a bag of scraps')) return sub('Not enough on him.', '', 'over', 2.5);
          pocket('a bag of scraps', 'coat');
          sub('A bag of scraps, hot through the paper.', '', 'over', 3);
        },
      });
  }
  const L = liftTarget();
  if (L) out.push({ k: 'G', t: 'Lift from ' + tomName(L) + "'s pocket", run: () => lift(L) });
}

function matters(P, a) {
  const c = C(),
    id = P.id;
  if (id === 'rita') {
    const things = sellable();
    if (things.length && (c.fence.walkedAt === null || G.t - c.fence.walkedAt > 60))
      a.push({
        key: 'fence',
        ask: 'what Rita will give for what he has under his coat',
        raise: "If you've something for the back room, show me. I'll say a price. I don't say it four times.",
        keep: ['Where does it go after?', 'Who else sells to you?'],
        keepSay: "I don't ask where it's been and you don't ask where it's going.",
        opts: things.slice(0, 3).map((thing) => ({
          say: ['What will you give me for ' + thing + '?', 'How much for ' + thing + '?'],
          take: async () => {
            endTalk();
            await scene(() => fenceScene(thing));
          },
        })),
      });
  }
  if (id === 'k_laund' && (c.coatBlood || (c.blood && tom().hasCoat)))
    a.push({
      key: 'wash',
      direct: true,
      ask: 'whether to have the coat washed',
      raise: 'Service wash is a pound. That coat wants it, whatever that is on the cuff.',
      opts: [
        {
          agree: 1,
          q: 'A pound. Yes or no?',
          yes: ['Yes. Wash it.', 'Yes. A pound.'],
          no: ['No. Leave it.', 'No. Not today.'],
          keep: ['How long will it take?', 'Does it come out?'],
          keepSay: "Most things come out. I'll remember what did, mind. A pound. Yes or no?",
          noSay: 'Suit yourself.',
          take: () => {
            if (!pay(T().rid.launderettePence, false, 'the coat washed')) return "It's a pound, love. Come back with a pound.";
            const r = R.washBlood({ at: 'launderette' });
            c.coatBlood = !r.clean;
            c.blood = false;
            const ev = act('coat_washed', { target: 'k_laund' });
            note('Had the coat washed at the Washeteria. The attendant saw what came out of it, and she will remember.', 'note', null, { how: 'Was there', ev: ev.id });
            lg('washed', { where: 'launderette' });
            emit('crime:rid', { thing: 'blood', how: 'launderette' });
            return "Come back in an hour. I've seen worse, and I remember all of it.";
          },
        },
      ],
    });
  if (id === 'k_iron') {
    const lifted = Object.keys(c.keys).filter((k) => c.keys[k] === 'lifted' || c.keys[k] === 'lent');
    if (lifted.length)
      a.push({
        key: 'keycut',
        direct: true,
        ask: 'whether to have a key cut',
        raise: 'Key cut? One pound fifty, while you wait. I never ask whose door.',
        opts: [
          {
            agree: 1,
            q: 'One fifty. Cut it?',
            yes: ['Yes. Cut it.', 'Yes. One fifty.'],
            no: ['No. Leave it.', 'No. Not today.'],
            keep: ['Do you know every lock on this street?', 'Who else has had one cut?'],
            keepSay: 'I fitted most of them. And I never say who. One fifty. Cut it?',
            noSay: 'Right you are.',
            take: () => {
              if (!pay(T().entry.keyCopyPence, false, 'a key cut')) return 'One fifty, I said.';
              for (const k of lifted) c.keys[k] = 'copy';
              // with a copy cut, the lifted key can go back before it is missed: nobody finds one gone
              for (const l of c.lifts) if (!l.missed && POCKETS[l.who] && POCKETS[l.who].key) l.copied = true;
              lg('keycut', { sites: lifted });
              emit('crime:keycut', { sites: lifted });
              return 'There. Works better than the one it came off.';
            },
          },
        ],
      });
  }
  // a key lent: each holder by his own need
  for (const sid in SITES) {
    const S = SITES[sid];
    if (S.key.holder !== id || c.keys[sid] || id === S.owner) continue;
    a.push({
      key: 'lend_' + sid,
      direct: true,
      ask: 'whether ' + P.def.name + ' will lend ' + S.key.thing,
      raise: `You're after ${S.key.thing}, aren't you. A fiver and I never had it on me. Yes?`,
      opts: [
        {
          agree: 1,
          q: 'A fiver. Yes or no?',
          yes: ['Yes. A fiver.', 'Yes. Lend it me.'],
          no: ['No. Forget it.', 'No. Not today.'],
          keep: ['When is the place empty?', 'Who else has a key?'],
          keepSay: "That's two questions and one fiver. Yes or no?",
          noSay: 'Then I never offered.',
          take: () => {
            if (!pay(500, false, 'a key lent')) return "Come back when you've a fiver.";
            c.keys[sid] = 'lent';
            act('paid_info', { target: id });
            note(`${P.def.name} lent ${S.key.thing} for a fiver. He knows what it is for.`, 'note', null, { who: id, how: 'Was there' });
            lg('lent', { site: sid, by: id });
            emit('crime:lent', { site: sid, by: id });
            return 'Back on the nail by morning. And I was never asked.';
          },
        },
      ],
    });
  }
}

register({
  id: 'crime',
  fresh,
  loaded: (x) => {
    busy = null;
    tail = null;
    mind = null;
    const f = fresh();
    for (const k in f) if (x[k] === undefined) x[k] = f[k];
    refreshCarried();
  },
  step: (dt) => {
    if (G.paused || G.story.phase !== 'play') return;
    refreshCarried();
    stepBusy(dt);
    stepTail(dt);
    stepMind(dt);
    stepBlood();
    leaveSites();
    ownerWatch(dt);
    stepDogs();
  },
  minute: (m) => {
    ownersLearn(m);
    keysMissed(m);
  },
  daily: () => {
    C().purses = Object.assign({}, T().debts.pursePence); // a purse is what the week puts in it: filled again each day, never more
  },
  hotspots,
  matters,
  hook: {
    sites: () => SITES,
    breakables: () => BREAKABLES,
    pockets: () => POCKETS,
    places: () => PLACES,
    state: () => C(),
    carried: () => refreshCarried(),
    busy: () => (busy ? { what: busy.what, t: busy.t, need: busy.need } : null),
    waysNow: (id) => waysNow(SITES[id]),
    enter: (id, way) => enter(SITES[id], way),
    search: (id, k) => search(SITES[id], SITES[id].containers.find((c) => c.id === k)),
    smash: (id) => smash(BREAKABLES.find((b) => b.id === id)),
    lift: (who) => lift(P_(who)),
    liftTarget: () => (liftTarget() ? liftTarget().id : null),
    pocket,
    unpocket,
    give: (thing, goods) => {
      if (!pocket(thing)) return false;
      if (goods) C().goods[thing] = Object.assign({ takenAt: Math.round(G.t), owner: 'norman', street: 'the warehouse row' }, goods);
      return true;
    },
    fence: (thing) => scene(() => fenceScene(thing)),
    fenceOffer: (thing, asks) => {
      const g = C().goods[thing];
      return R.fenceOffer({ honestPence: g.honestPence, hot: R.hotMark({ honestPence: g.honestPence, gameDaysSince: (G.t - g.takenAt) / 1440, onTheOwnersStreet: g.street === 'Quay Street' }), pursePence: T().fence.ritaPursePence, regard: P_('rita').mind.regard }, asks);
    },
    startTail,
    stopTail,
    tail: () => (tail ? { who: tail.who, doubts: tail.doubts, lookIn: tail.lookIn, looks: tail.looks } : null),
    lookNow: () => {
      if (!tail) return null;
      const P = P_(tail.who),
        t = tom(),
        d = hyp(P.x, P.z, t.x, t.z);
      lookBack(P, P.space === t.space && d < T().tail.followsWithinMetres && G.env.los(P.x, P.z, t.x, t.z), d);
      return tail ? { state: 'on', doubts: tail.doubts } : { state: C().tails[P.id].st };
    },
    startMind,
    casing: (id) => casing(SITES[id]),
    casingLines: (id) => casingLines(SITES[id]),
    caseSpot: () => (caseSpot() ? caseSpot().id : null),
    throwIn,
    washUp,
    feedDog,
    purses,
    store: (which) => scene(() => storeScene(which)),
    dogVerbs: () => R.dogVerbs(),
    bloody: (on) => {
      C().blood = on;
      C().coatBlood = on && !!tom().coat;
    },
  },
});

// a constable's search takes what he finds: the law builder says what went
on('police:searched', (p) => {
  const c = C();
  for (const thing of (p && p.took) || []) {
    unpocket(thing);
    delete c.goods[thing];
  }
});
export { purses, has, pocket, unpocket, lg, P_ as person };
