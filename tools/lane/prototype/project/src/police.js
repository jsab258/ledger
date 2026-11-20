// LEDGER. Police: what reaches the station, the constable, custody, and DS Ellis asking the street.
import { G, day, hour, pausedWhile } from './state.js';
import { hyp, rnd, money } from './util.js';
import { act, seed, logLine, remember } from './events.js';
import { loudness } from './gossip.js';
import { note, ledgerSeen } from './ledger.js';
import { tomNotices, attached } from './seeing.js';
import { KINDS } from './kinds.js';
import { placeAll, goToPoint } from './routines.js';
import { ROOMS } from './map.js';
import { sub, say, choose, scene, fade, news, $, tomName, bubble, after } from './ui.js';
import { setInside } from './render/effects.js';
import { fl, advanceTo } from './work.js';
import { RULES } from './rules.js';
import { emit, ensureX } from './game/core.js';
import { PIECE as CUSTODY } from './game/pieces/law_custody.js';
import { PIECE as STATEMENT } from './game/pieces/law_statement.js';

const POL = RULES.police;
const LAW = RULES.game.law;
const { deedClass, custody: custodyRule, mayArrest } = CUSTODY.fns;
const { willState } = STATEMENT.fns;
// the law system's saved state (game/law.js); read here with defaults so this file stands by itself
const LX = () => {
  const x = ensureX();
  return x.law || (x.law = {});
};
const MICKEYS = ['sheila', 'ron', 'pauline', 'kevin', 'terry', 'darren'];
export const classOf = (E) => (E ? (E.lawClass ? E.lawClass : deedClass(Object.assign({ kills: E.kind === 'kill' }, KINDS[E.kind]))) : 'window');

export function policeStep(dt) {
  const st = G.story,
    a = st.arrest,
    t = G.tom;
  if (!a) return;
  const P = G.people[a.violent ? 'ellis' : 'pc'];
  if (!P) return;
  if (!a.st) {
    if (G.t < a.due) return;
    a.st = 'come';
    P.override = null;
    P.gone = false;
    P.space = 'street';
    P.awake = true;
    P.x = POL.arrivesAtXMetres;
    P.z = POL.arrivesAtZMetres;
    P.route = null;
    P.hold = true;
    P.mark = '!';
    a.rt = 0;
    logLine((a.violent ? 'DS Ellis' : 'A constable') + ' came down Quay Street for Tom', 'police');
  }
  if (a.st === 'come' || a.st === 'chase') {
    a.rt -= dt;
    const same = P.space === t.space && !P.gone,
      d = same ? hyp(P.x, P.z, t.x, t.z) : 999;
    if (a.rt <= 0 && !P.gone && P.space === 'street') {
      a.rt = a.st === 'chase' ? POL.looksAgainWhenChasingEveryRealSeconds : POL.looksAgainEveryRealSeconds;
      const tx =
          t.space === 'street' ? (t.inCar ? G.car.x : t.x) : ROOMS[t.space] ? ROOMS[t.space].street[0] : t.x,
        tz =
          t.space === 'street' ? (t.inCar ? G.car.z : t.z) : ROOMS[t.space] ? ROOMS[t.space].street[1] : t.z;
      // While Tom stays where he was at the last look and the walk to him is under way, the constable keeps to
      // it. Planned afresh from wherever he stood, the way could flip between two ways round the lane east of
      // Quay Street, and he walked back and forth there and never arrived.
      if (!P.route || a.tx === undefined || hyp(a.tx, a.tz, tx, tz) > POL.keepsHisWayWhileTomWithinMetres) {
        a.tx = tx;
        a.tz = tz;
        goToPoint(P, tx, tz, a.st === 'chase' ? POL.chasingMetresPerSecond : POL.walkingMetresPerSecond);
      }
    }
    if (a.st === 'come' && d < POL.speaksWithinMetres && !t.inCar && !G.paused) arrestScene(P, a);
    if (a.st === 'chase') {
      a.ct += dt;
      const los = same && G.env.los(P.x, P.z, t.x, t.z) && d < POL.seesHimWithinMetres;
      a.lost = los ? 0 : a.lost + dt;
      if (d < POL.catchesWithinMetres && !t.inCar) {
        a.st = 'held';
        custody(P, a, true);
      } else if (
        a.lost > POL.losesHimAfterRealSecondsUnseen ||
        d > POL.losesHimBeyondMetres ||
        a.ct > POL.chaseLastsAtMostRealSeconds
      ) {
        a.st = 'gone';
        P.hurry = 1;
        P.mark = null;
        P.override = { where: 'off', act: 'idle' };
        P.goalKey = '';
        fl().ranPolice = 1;
        st.arrest = null;
        sub('You have lost him. He knows your name, and where you sleep.', '', 'over', 5);
        st.nightDone[day()] = 0;
      }
    }
  }
}

export function arrestNow(P) {
  const st = G.story;
  st.arrest = { e: null, violent: true, due: G.t, st: 'held', by: [], officerSaw: true, cls: 'wounding' };
  custody(P, st.arrest, true);
}

async function arrestScene(P, a) {
  a.st = 'talk';
  const E = a.e ? G.ev[a.e] : null,
    what = E ? KINDS[E.kind].truth(E).replace(/^Tom /, 'you ') : a.what || 'yesterday',
    cls = a.cls || classOf(E),
    lx = LX();
  // an officer at his door: that is the sign of the second stage, shown here if nowhere sooner
  if (lx.signs) for (const sg of lx.signs) if (sg.stage === 2 && !sg.shown) sg.shown = true;
  const i = await scene(async () => {
    const opts = (who) => ['Go with ' + who + '.', 'Run.'].concat(cls === 'window' && E ? ['Own up to it, and go.'] : []);
    if (P.id === 'ellis') {
      await say('ellis', 'Mr Nowak. Carol Ellis, CID. Somebody has told me that ' + what + '.');
      return choose('ellis', "I'd like you to come up to the station. It's better done quietly.", opts('her'));
    }
    await say(P.id, "Thomas Nowak? We've had a statement, sir. That " + what + '.');
    return choose(P.id, "I'd like you to come along to the station, sir. It's better done quietly.", opts('him'));
  });
  if (i === 1) {
    a.st = 'chase';
    a.ct = 0;
    a.lost = 0;
    P.hurry = POL.chaseHurry;
    lx.ran = (lx.ran || 0) + 1;
    act('ran_police', { noiseR: POL.runningNoiseMetres });
    sub('Oi! Stop there!', tomName(P), 'face');
  } else {
    a.ownedUp = i === 2;
    custody(P, a, false);
  }
}

// Custody costs hours, never the game (DESIGN section 8): about six for a window (two and a caution if he owns up),
// eight for a wounding, twelve for a robbery, twenty-two for a killing and then bail. The duty solicitor is free.
// The coat is kept if he wore it. He is never taken twice for one deed.
async function custody(P, a, ran) {
  const t = G.tom,
    E = a.e ? G.ev[a.e] : null,
    lx = LX(),
    cls = a.cls || classOf(E),
    r = custodyRule(cls, !!a.ownedUp, !!ran),
    hours = r.hours,
    coat = t.hasCoat && (t.coat || (E && E.coat));
  const outcome = a.outcome || r.outcome,
    ends =
      outcome === 'cautioned'
        ? 'You own up. A caution, written down, and the door.'
        : outcome === 'charged'
          ? cls === 'killing'
            ? 'Charged, and bailed to come back. Nobody says when.'
            : 'Charged, and bailed. It goes in a file with your name on it.'
          : 'Released. No charge, this time.';
  await pausedWhile('custody at the town station', async () => {
    const taken = act('arrested', {});
    P.mark = null;
    await fade(
      true,
      `${hours} hours at the town station.\nThe duty solicitor sits in. He costs nothing and says little.\n${ends}` +
        (coat ? '\nThey keep the coat as evidence.' : ''),
    );
    if (t.inCar) {
      t.inCar = false;
    }
    if (coat) {
      t.hasCoat = false;
      t.coat = false;
      fl().coatGone = 1;
    }
    if (t.carry === 'bag') {
      t.carry = null;
      if (G.story.job) {
        G.story.job.st = 'missed';
        G.story.job.carrying = false;
      }
      note('The police kept the bag.', 'police', null, { ev: taken.id });
    }
    note(
      `Taken in${E ? ' over: ' + KINDS[E.kind].mine(E).toLowerCase() : ''}. ${hours} hours. ${ends}`,
      'police',
      'arrest' + day() + (E ? 'e' + E.id : ''),
      { ev: taken.id },
    );
    if (a.by)
      for (const id of a.by) {
        const W = G.people[id];
        if (W) W.mind.stmtGiven = 1;
      }
    // never twice for one deed; a charge joins DS Ellis's case and is read at the ending
    lx.taken = lx.taken || {};
    if (E) lx.taken[E.id] = 1;
    lx.case = lx.case || { charges: [], statements: 0, officeFinds: 0, strength: 0 };
    if (outcome === 'charged') lx.case.charges.push({ e: E ? E.id : null, cls, t: Math.round(G.t) });
    lx.arrests = (lx.arrests || 0) + 1;
    lx.lastArrest = { e: E ? E.id : null, cls, hours, outcome, ran: !!ran, fromT: Math.round(G.t) };
    advanceTo(G.t + hours * 60);
    P.hurry = 1;
    P.override = { where: 'off', act: 'idle' };
    P.goalKey = '';
    G.story.arrest = null;
    fl().ranPolice = 0;
    fl().assaultPolice = 0;
    lx.hunted = 0;
    t.space = 'street';
    try {
      setInside(null);
    } catch (e) {
      /* a rules-only run (test/game/law_headless.mjs) has nothing drawn to switch */
    }
    t.x = POL.releasedAtXMetres;
    t.z = POL.releasedAtZMetres;
    t.ang = 1.57;
    placeAll();
    await fade(false);
  });
  news(
    cls === 'window' ? 'CAB OFFICE MAN QUESTIONED' : 'QUAY STREET CAB MAN HELD',
    outcome === 'charged' ? 'Charged and bailed after ' + hours + ' hours' : outcome === 'cautioned' ? 'Cautioned and released after ' + hours + ' hours' : 'Released without charge after ' + hours + ' hours',
  );
  emit('arrest', { E, hours, outcome, cls, ran: !!ran });
  if (G.hooks.save) G.hooks.save();
}

// ---------- Ellis asks along the street ----------
export function ellisClock() {
  const st = G.story,
    d = day(),
    h = hour();
  st.ellisDays = st.ellisDays || {};
  const due =
    d >= POL.ellisFirstDayIndex &&
    d <= POL.ellisLastDayIndex &&
    h >= POL.ellisFromHour &&
    h <= POL.ellisUntilHour;
  if (!due || st.ellisDays[d] || st.ellis || st.arrest) return;
  st.ellisDays[d] = 1;
  const L = loudness();
  st.loudAt = st.loudAt || {};
  st.loudAt[d] = L;
  if (L < POL.ellisComesAtLoudness && !fl().dead && !fl().forceEllis) return;
  startEllis('the talk. Loudness ' + L.toFixed(1));
}
// DS Ellis comes down Quay Street and asks along it. Why she came is said in the log. True if she set out.
export function startEllis(why) {
  const st = G.story;
  if (st.ellis || !G.people.ellis || G.people.ellis.dead) return false;
  const E = G.people.ellis,
    list = G.named
      .filter(
        (p) =>
          p.def.local !== false &&
          !p.def.police &&
          !p.gone &&
          !p.dead &&
          p.space === 'street' &&
          p.z > -70 &&
          p.z < 60 &&
          Math.abs(p.x) < 60,
      )
      .sort(() => rnd() - 0.5)
      .slice(0, POL.ellisAsksPeopleAtMost)
      .map((p) => p.id);
  if (!list.length) return false;
  st.ellis = { q: list, i: 0, t: 0, ev: seed('ellis_asked', []).id };
  E.override = null;
  E.gone = false;
  E.space = 'street';
  E.awake = true;
  E.x = POL.arrivesAtXMetres;
  E.z = POL.arrivesAtZMetres;
  E.route = null;
  E.hold = true;
  LX().ellisAsked = Math.round(G.t);
  logLine('DS Ellis came down Quay Street asking about Tom: ' + why, 'police');
  emit('police:ellis', { why });
  return true;
}

export function ellisStep(dt) {
  const st = G.story,
    e = st.ellis;
  if (!e) return;
  const E = G.people.ellis,
    t = G.tom;
  if (E.gone || E.space !== 'street') return;
  e.t -= dt;
  if (e.wait > 0) {
    e.wait -= dt;
    if (e.wait <= 0) e.i++;
    return;
  }
  if (e.i >= e.q.length) {
    if (
      !e.tom &&
      t.space === 'street' &&
      !t.inCar &&
      hyp(E.x, E.z, t.x, t.z) < POL.ellisSeeksHimWithinMetres
    ) {
      if (e.t <= 0) {
        e.t = POL.looksAgainEveryRealSeconds;
        goToPoint(E, t.x, t.z, POL.ellisWalkingMetresPerSecond);
      }
      if (hyp(E.x, E.z, t.x, t.z) < POL.ellisSpeaksWithinMetres && !G.paused) {
        e.tom = 1;
        if (G.hooks.ellisTalk) G.hooks.ellisTalk();
      }
      e.life = (e.life || 0) + dt;
      if (e.life < POL.ellisLeavesAfterRealSecondsLooking) return;
    }
    E.override = { where: 'off', act: 'idle' };
    E.goalKey = '';
    st.ellis = null;
    return;
  }
  const P = G.people[e.q[e.i]];
  if (!P || P.gone || P.space !== 'street') {
    e.i++;
    return;
  }
  if (e.t <= 0) {
    e.t = POL.looksAgainEveryRealSeconds;
    goToPoint(E, P.x + 1, P.z + 0.6, POL.ellisWalkingMetresPerSecond);
  }
  if (hyp(E.x, E.z, P.x, P.z) < POL.ellisStopsWithinMetres) {
    e.wait = POL.ellisAsksForRealSeconds;
    E.chat = { with: P.id, t: POL.ellisAsksForRealSeconds };
    P.chat = { with: 'ellis', t: POL.ellisAsksForRealSeconds };
    P.hold = true;
    after(POL.personHeldWhileAskedRealSeconds, () => {
      P.hold = false;
    });
    const Ev = G.ev[e.ev];
    remember(P, Ev, { src: 'self', who: 'tom', sure: 1, heat: POL.askedMemoryHeat });
    bubble(P, '...');
    if (tomNotices(E) && tomNotices(P)) {
      ledgerSeen(Ev, P, 'saw');
      sub('That detective has stopped ' + tomName(P) + '. They both look your way.', '', 'over', 4);
    }
  }
}

// Who will give a statement about a crime: someone who saw him plainly, is not frightened or bought, and has not
// warmed to him (the rule is the piece law_statement). Mickey's people never go; those whose trade keeps them away
// never go. Once the real town runs, the people its cast holds are the town's to decide.
export function wouldState(P, E) {
  const lx = LX();
  if (!P || !E) return { goes: false, why: 'nobody' };
  if (lx.live && LAW.townCast.includes(P.id)) return { goes: false, why: 'the town decides for this person' };
  const m = P.mind.by[E.id],
    key = E.id + ':' + P.id;
  return willState(
    {
      dead: !!P.dead,
      mickeys: MICKEYS.includes(P.id),
      tradeKeepsAway: !!P.def.nostmt,
      sawPlainly: !!(m && m.src !== 'told' && m.src !== 'heard' && attached(m)),
      sure: m ? m.sure : 0,
      fear: P.mind.fear,
      bought: !!P.mind.bought || !!(lx.turned && lx.turned[key]),
      regard: P.mind.regard,
      upright: !!P.def.upright,
      lost: !!(lx.lost && lx.lost[key]),
    },
    {
      needsSure: POL.statementNeedsSureAtLeast,
      noStatementIfFear: POL.noStatementIfFearAtLeast,
      uprightQuietAboveRegard: POL.uprightStaysQuietAboveRegard,
      othersQuietAboveRegard: POL.othersStayQuietAboveRegard,
    },
  );
}
export function statements(dayIdx) {
  const out = [];
  for (const E of G.events) {
    const k = KINDS[E.kind];
    if (k.crime < 1 || E.stmt !== undefined || Math.floor(E.t / 1440) > dayIdx) continue;
    const givers = [];
    for (const id of new Set([...(E.wit || []), ...(E.party || [])])) {
      const P = G.people[id];
      if (P && wouldState(P, E).goes) givers.push(id);
    }
    E.stmt = givers;
    if (givers.length) out.push(E);
  }
  return out;
}

// A statement is on record: the one road by which anything reaches the police, whoever decided it (a witness's
// walk ending, the night's run for those who slept on it, or the real town's morning). ER-POL-01: no arrest
// without a named statement or an officer who saw it; never twice for one deed.
export function record(E, by, how) {
  const st = G.story,
    lx = LX();
  by = (by || []).filter((id) => !(lx.lost && E && lx.lost[E.id + ':' + id]));
  if (E) E.stmt = [...new Set([...(E.stmt || []), ...by])];
  if (!by.length && !(E && E.officerSaw)) return false;
  lx.reported = lx.reported || {};
  const first = E && !lx.reported[E.id];
  if (E) lx.reported[E.id] = [...new Set([...(lx.reported[E.id] || []), ...by])];
  lx.case = lx.case || { charges: [], statements: 0, officeFinds: 0, strength: 0 };
  lx.case.statements += by.length;
  logLine(
    'A statement was made to the police: ' +
      (E ? KINDS[E.kind].truth(E) : 'about him') +
      ' (by ' +
      (by.map((id) => G.people[id]?.def.name || id).join(', ') || 'an officer') +
      (how ? '; ' + how : '') +
      ')',
    'police',
  );
  const ok = mayArrest({
    takenAlready: !!(E && lx.taken && lx.taken[E.id]),
    officerSaw: !!(E && E.officerSaw),
    statements: by.map((id) => ({ by: id, knewItWasHim: true })),
  }).ok;
  if (ok) {
    const cls = classOf(E),
      rank = { window: 1, wounding: 2, robbery: 3, killing: 4 },
      cur = st.arrest;
    if (!cur || (!cur.st && rank[cls] > rank[cur.cls || 'window'])) {
      const d0 = Math.floor(G.t / 1440),
        at = d0 * 1440 + POL.comesNextDayAtHour * 60;
      st.arrest = {
        e: E ? E.id : null,
        violent: (E && KINDS[E.kind].crime >= POL.violentFromCrimeLevel) || !!fl().ranPolice || !!fl().assaultPolice,
        due: cur && cur.due ? cur.due : G.t + 30 <= at ? at : at + 1440, // the next nine in the morning
        by: E ? E.stmt : by,
        cls,
      };
    } else if (cur && cur.e === (E ? E.id : null)) cur.by = E ? E.stmt : by;
  }
  if (first || !E) emit('police:reported', { E, by, how: how || '' });
  return true;
}

export function nightly(d) {
  // run once per night: who went to the police about what they saw, of those who had not already walked there
  const st = G.story;
  st.nightDone = st.nightDone || {};
  if (st.nightDone[d]) return;
  st.nightDone[d] = 1;
  const evs = statements(d);
  if (!evs.length && !fl().ranPolice && !fl().assaultPolice) return;
  evs.sort((a, b) => KINDS[b.kind].crime - KINDS[a.kind].crime);
  for (const E of evs) record(E, E.stmt, 'went up in the morning');
  if (!evs.length && !st.arrest) {
    // he ran from them, or laid hands on one: an officer saw that himself
    st.arrest = { e: null, violent: true, due: (d + 1) * 1440 + POL.comesNextDayAtHour * 60, by: [], cls: 'wounding', officerSaw: true };
    logLine('A statement was made to the police: he ran from them', 'police');
  } else if (st.arrest && !st.arrest.st) st.arrest.due = Math.min(st.arrest.due, (d + 1) * 1440 + POL.comesNextDayAtHour * 60);
}
