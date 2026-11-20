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

const POL = RULES.police;

export function policeStep(dt) {
  const st = G.story,
    a = st.arrest,
    t = G.tom;
  if (!a) return;
  const P = G.people[a.violent ? 'ellis' : 'pc'];
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
  st.arrest = { e: null, violent: true, due: G.t, st: 'held', by: [] };
  custody(P, st.arrest, true);
}

async function arrestScene(P, a) {
  a.st = 'talk';
  const E = a.e ? G.ev[a.e] : null,
    what = E ? KINDS[E.kind].truth(E).replace(/^Tom /, 'you ') : 'yesterday';
  const i = await scene(async () => {
    if (P.id === 'ellis') {
      await say('ellis', 'Mr Nowak. Carol Ellis, CID. Somebody has told me that ' + what + '.');
      return choose('ellis', "I'd like you to come up to the station. It's better done quietly.", [
        'Go with her.',
        'Run.',
      ]);
    }
    await say('pc', "Thomas Nowak? We've had a statement, sir. That " + what + '.');
    return choose('pc', "I'd like you to come along to the station, sir. It's better done quietly.", [
      'Go with him.',
      'Run.',
    ]);
  });
  if (i === 0) custody(P, a, false);
  else {
    a.st = 'chase';
    a.ct = 0;
    a.lost = 0;
    P.hurry = POL.chaseHurry;
    act('ran_police', { noiseR: POL.runningNoiseMetres });
    sub('Oi! Stop there!', tomName(P), 'face');
  }
}

async function custody(P, a, ran) {
  const t = G.tom,
    m = G.money,
    E = a.e ? G.ev[a.e] : null;
  const hours0 =
      (a.violent ? POL.heldGameHoursIfViolent : POL.heldGameHours) +
      (ran ? POL.heldGameHoursAddedIfHeRan : 0),
    bill0 = ran ? POL.briefBillPenceIfHeRan : POL.briefBillPence,
    coat = t.hasCoat && (t.coat || (E && E.coat));
  // the one-shot: the hours are the offence's own (six for a window, eight for a wounding, twelve for a robbery,
  // twenty-two for a killing), the duty solicitor is free, and it ends in a caution or a charge (game/law.js)
  const law = G.hooks.custody ? G.hooks.custody(a, ran, E) : null;
  const hours = law ? law.hours : hours0,
    bill = law ? 0 : bill0;
  await pausedWhile('custody at the town station', async () => {
    const taken = act('arrested', {});
    P.mark = null;
    await fade(
      true,
      (law
        ? `${hours} hours at the town station.\nThe duty solicitor sits in and says little.\n${law.ends}`
        : `${hours} hours at the town station.\nA brief you never sent for arrives from Agar & Co.\nThe clerk settles it and leaves a bill for ${money(bill)}.`) +
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
    const paid = Math.min(m.clean, bill);
    m.clean -= paid;
    m.spent += paid;
    if (paid > 0 && G.hooks.flow) G.hooks.flow('pocket', 'world', paid, "the solicitor's bill");
    if (paid < bill) {
      fl().oweAgar = (fl().oweAgar || 0) + bill - paid;
    }
    note(
      law ? `Taken in${E ? ' over: ' + KINDS[E.kind].mine(E).toLowerCase() : ''}. ${hours} hours. ${law.ends}` : `Taken in${E ? ' over: ' + KINDS[E.kind].mine(E).toLowerCase() : ''}. Agar's clerk paid for a brief nobody asked for.`,
      'police',
      'arrest' + day(),
      { ev: taken.id },
    );
    if (a.by)
      for (const id of a.by) {
        const W = G.people[id];
        if (W) W.mind.stmtGiven = 1;
      }
    advanceTo(G.t + hours * 60);
    P.hurry = 1;
    P.override = { where: 'off', act: 'idle' };
    P.goalKey = '';
    G.story.arrest = null;
    fl().ranPolice = 0;
    fl().assaultPolice = 0;
    t.space = 'street';
    setInside(null);
    t.x = POL.releasedAtXMetres;
    t.z = POL.releasedAtZMetres;
    t.ang = 1.57;
    placeAll();
    await fade(false);
  });
  news(
    a.violent ? 'QUAY STREET CAB MAN HELD' : 'CAB OFFICE MAN QUESTIONED',
    'Released without charge after ' + hours + ' hours',
  );
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
  // the one-shot: with the real town running, DS Ellis comes on the mornings the town's own rules send her (game/town.js)
  const townSays = G.hooks.townEllis ? G.hooks.townEllis() : null;
  if ((townSays === null ? L < POL.ellisComesAtLoudness : !townSays) && !fl().dead && !fl().forceEllis) return;
  if (G.hooks.townEllisShown) G.hooks.townEllisShown();
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
  if (!list.length) return;
  st.ellis = { q: list, i: 0, t: 0, ev: seed('ellis_asked', []).id };
  E.override = null;
  E.gone = false;
  E.space = 'street';
  E.awake = true;
  E.x = POL.arrivesAtXMetres;
  E.z = POL.arrivesAtZMetres;
  E.route = null;
  E.hold = true;
  logLine('DS Ellis came down Quay Street asking about Tom. Loudness ' + L.toFixed(1), 'police');
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

// Who will give a statement about a crime: someone who saw him plainly, is not frightened or bought, and has not warmed to him.
export function statements(dayIdx) {
  const out = [];
  for (const E of G.events) {
    const k = KINDS[E.kind];
    if (k.crime < 1 || E.stmt !== undefined || Math.floor(E.t / 1440) > dayIdx) continue;
    const givers = [];
    for (const id of new Set([...(E.wit || []), ...(E.party || [])])) {
      const P = G.people[id];
      if (!P || P.dead || P.def.nostmt) continue;
      const m = P.mind.by[E.id];
      const plain = m && m.src !== 'told' && m.src !== 'heard' && attached(m);
      if (!plain || m.sure < POL.statementNeedsSureAtLeast) continue; // saw him plainly
      if (P.mind.fear >= POL.noStatementIfFearAtLeast || P.mind.bought) continue; // a threat can stop a report
      const quietAbove = P.def.upright ? POL.uprightStaysQuietAboveRegard : POL.othersStayQuietAboveRegard;
      if (P.mind.regard > quietAbove) continue; // has warmed to him
      givers.push(id);
    }
    E.stmt = givers;
    if (givers.length) out.push(E);
  }
  return out;
}

export function nightly(d) {
  // run once per night: who went to the police about what they saw
  const st = G.story;
  st.nightDone = st.nightDone || {};
  if (st.nightDone[d]) return;
  st.nightDone[d] = 1;
  const evs = statements(d);
  if (!evs.length && !fl().ranPolice && !fl().assaultPolice) return;
  const worst = evs.sort((a, b) => KINDS[b.kind].crime - KINDS[a.kind].crime)[0];
  st.arrest = {
    e: worst ? worst.id : null,
    violent:
      (worst && KINDS[worst.kind].crime >= POL.violentFromCrimeLevel) ||
      !!fl().ranPolice ||
      !!fl().assaultPolice,
    due: (d + 1) * 1440 + POL.comesNextDayAtHour * 60,
    by: worst ? worst.stmt : [],
  };
  logLine(
    'A statement was made to the police: ' +
      (worst
        ? KINDS[worst.kind].truth(worst) +
          ' (by ' +
          worst.stmt.map((id) => G.people[id]?.def.name).join(', ') +
          ')'
        : 'he ran from them'),
    'police',
  );
}
