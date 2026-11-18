// LEDGER. Checks the test hook can run: LEDGER.check.arrivals() and LEDGER.check.nights().
// Both step the game forward by hand and answer for the player when a box comes up, so they need
// window.LEDGER_MANUAL = true (the checks set it and put it back).
import { G, day, hour, PAUSE } from './state.js';
import { clockText, dateText } from './util.js';
import { RULES } from './rules.js';
import { ui, dialogNow, advance, pickOpt, closePanel } from './ui.js';
import { endTalk } from './talk.js';
import { advanceTo } from './work.js';
import { goalName } from './hook.js';
import { TRIPS } from './routines.js';
import { ROOMS, zoneAt } from './map.js';

const wait = (ms) => new Promise((res) => setTimeout(res, ms));
const stamp = (t) => dateText(t) + ', ' + clockText(t);

export function makeChecks(hook, x) {
  // When the game is paused, do what a player would: read the line on, take the first choice, leave a talk,
  // shut a panel; or, when the game is busy (a fade, time passing), wait for it. Returns what it did.
  async function attend(choice = 0) {
    if (!G.paused) return null;
    const why = G.pauseWhy;
    if (ui.modal === 'dialog') {
      const d = dialogNow();
      if (d) {
        if (!d.done) advance();
        if (d.opts) pickOpt(Math.min(choice, d.opts.length - 1));
        else advance();
      }
      await wait(0);
      return 'answered: ' + why;
    }
    if (ui.modal === 'talk') {
      endTalk();
      await wait(0);
      return 'left the talk';
    }
    if (ui.modal === 'ledger') {
      x.closeLedger();
      return 'closed the Ledger';
    }
    if (ui.modal && ui.modal !== 'end') {
      closePanel();
      return 'closed a panel';
    }
    for (let k = 0; k < 4; k++) x.logic(0.05); // a fade, or time passing: it ends by itself as the game steps
    await wait(0);
    return 'waited';
  }

  // Step from now until a game minute, attending to anything that pauses the game. A pause that has not
  // ended after stuckAfterRealSeconds is reported and the run stops.
  async function run(untilGameMinute, o = {}) {
    const dt = o.stepRealSeconds || 0.25,
      limit = (o.stuckAfterRealSeconds || 20) * 1000,
      each = o.each;
    let pausedSince = 0,
      stuck = null,
      guard = 0;
    while (G.t < untilGameMinute && !G.story.ended && guard++ < 4e6) {
      if (G.paused) {
        if (!pausedSince) pausedSince = performance.now();
        await attend(o.choice || 0);
        if (performance.now() - pausedSince > limit) {
          stuck = {
            reason: G.pauseWhy,
            sinceRealSeconds: Math.round((performance.now() - pausedSince) / 1000),
            at: stamp(G.t),
            gameMinute: Math.round(G.t),
            boxOpen: ui.modal || null,
          };
          break;
        }
        continue;
      }
      pausedSince = 0;
      for (let i = 0; i < dt / 0.05; i++) x.logic(0.05);
      if (each) each();
      if (guard % 400 === 0) await wait(0); // let timers and promises run
    }
    return stuck;
  }

  return {
    // Does every named person who sets off for a place get there?
    // Steps the game from now (or fromGameMinute) for forGameHours, with Tom wherever he is (or at tomAt, a
    // named place), and reads the record the routines keep of every walk: set off, arrived, or turned for
    // somewhere else before arriving. It also watches for anyone marked as walking who is not moving.
    //   stoodStill: anyone marked as walking who has not moved for stoodStillRealSeconds (must be none);
    //   gaveUp: every walk given up for another place before arriving (the routine gave it too little time).
    //   A walk to or from "away" starts or ends at the edge of the map: those are marked involvesTheMapEdge.
    async arrivals(o = {}) {
      const manual = window.LEDGER_MANUAL;
      window.LEDGER_MANUAL = true;
      const hours = o.forGameHours ?? 24,
        still = o.stoodStillRealSeconds ?? 40,
        dt = o.stepRealSeconds || 0.25;
      if (o.fromGameMinute != null && o.fromGameMinute > G.t) advanceTo(o.fromGameMinute);
      if (o.tomAt) hook.goTo(o.tomAt);
      const from = G.t,
        mark = TRIPS.length,
        watch = {},
        faults = [];
      const where = (kind, x, z) =>
        kind === 'off' ? 'away' : kind === 'home' ? 'home' : ROOMS[kind] ? ROOMS[kind].name : zoneAt(x, z);
      const each = () => {
        for (const P of G.named) {
          const going = P.moving && P.route && !P.fight && !P.gone && !P.chat && !P.hold;
          if (!going) {
            delete watch[P.id];
            continue;
          }
          const W = watch[P.id] || (watch[P.id] = { x: P.x, z: P.z, stillRealSeconds: 0 });
          if (Math.hypot(P.x - W.x, P.z - W.z) > 0.3) {
            W.x = P.x;
            W.z = P.z;
            W.stillRealSeconds = 0;
            W.reported = false;
          } else W.stillRealSeconds += dt;
          if (!W.reported && W.stillRealSeconds > still) {
            W.reported = true;
            faults.push({
              kind: 'stood still',
              person: P.def.name,
              personId: P.id,
              goingTo: goalName(P.route.g),
              fault: `marked as walking but has not moved for ${Math.round(W.stillRealSeconds)} real seconds`,
              at: stamp(G.t),
              whereXMetres: Math.round(P.x),
              whereZMetres: Math.round(P.z),
              metresFromTom: Math.round(Math.hypot(P.x - G.tom.x, P.z - G.tom.z)),
            });
          }
        }
      };
      const stuck = await run(from + hours * 60, { stepRealSeconds: dt, each });
      const trips = TRIPS.slice(mark).filter(
        (T) => T.setOffGameMinute >= from - 0.01 && G.people[T.personId] && !G.people[T.personId].def.police,
      );
      // through the door of the place and on the way to a seat when the next hour came counts as getting there
      const inside = (T) => T.ended === 'turned' && T.goal.kind === 'room' && T.endSpace === T.goal.room;
      const arrived = trips.filter((T) => T.ended === 'arrived' || inside(T)),
        turned = trips.filter((T) => T.ended === 'turned' && !inside(T)),
        gaveUp = [];
      for (const T of turned)
        gaveUp.push({
          person: G.people[T.personId].def.name,
          personId: T.personId,
          from: where(T.fromSpace, T.fromX, T.fromZ),
          goingTo: goalName(T.goal),
          setOffAt: stamp(T.setOffGameMinute),
          fault: `gave up after ${Math.round(T.endedGameMinute - T.setOffGameMinute)} game minutes and turned for ${goalName(T.turnedFor)}, having covered ${Math.round(Math.hypot(T.endX - T.fromX, T.endZ - T.fromZ))} of about ${Math.round(T.streetMetres)} metres`,
          at: stamp(T.endedGameMinute),
          involvesTheMapEdge: T.fromSpace === 'off' || T.goal.kind === 'off',
        });
      window.LEDGER_MANUAL = manual;
      const walking = G.named.filter((P) => P.trip && !P.def.police);
      return {
        from: stamp(from),
        until: stamp(G.t),
        tomAt: hook.read().tom.place,
        walksSetOff: trips.length + walking.filter((P) => P.trip.setOffGameMinute >= from).length,
        walksArrived: arrived.length,
        walksGivenUpForAnotherPlace: turned.length,
        ofThoseToOrFromTheMapEdge: turned.filter((T) => T.fromSpace === 'off' || T.goal.kind === 'off')
          .length,
        stillWalkingAtTheEnd: walking.map((P) => ({
          person: P.def.name,
          goingTo: goalName(P.trip.goal),
          setOffAt: stamp(P.trip.setOffGameMinute),
        })),
        longestWalkGameMinutes: Math.round(
          arrived.reduce((m, T) => Math.max(m, T.endedGameMinute - T.setOffGameMinute), 0),
        ),
        stoodStill: faults,
        gaveUp,
        pauseNeverEnded: stuck,
        everyoneArrived: !faults.length && !gaveUp.length,
        ok: !faults.length && !stuck, // nobody is held on the spot and no pause is left hanging
      };
    },

    // Does every pause end? Steps through the nights given (by default Tuesday and Wednesday night, 10pm to
    // 6am) with Tom out on the street, answering any box as a player would, and reports every pause with its
    // game time and reason, and any pause with no resume.
    async nights(o = {}) {
      const manual = window.LEDGER_MANUAL;
      window.LEDGER_MANUAL = true;
      const nights = o.dayIndexes || [1, 2],
        fromHour = o.fromHour ?? 22,
        untilHour = o.untilHour ?? 6,
        out = [];
      let neverEnded = null;
      for (const d of nights) {
        const start = d * 1440 + fromHour * 60,
          end = (d + 1) * 1440 + untilHour * 60;
        if (G.t > end || G.story.ended) continue;
        if (G.t < start) advanceTo(start);
        if (o.tomAt !== null) hook.goTo(o.tomAt || 'the rank');
        const mark = PAUSE.log.length;
        neverEnded = await run(end, {
          stepRealSeconds: o.stepRealSeconds || 0.25,
          stuckAfterRealSeconds: o.stuckAfterRealSeconds || 20,
          choice: o.choice || 0,
        });
        // a pause that began just before the end of the night is given its time to end before it is judged
        for (let i = 0; i < 400 && G.paused && !neverEnded; i++) await attend(o.choice || 0);
        const log = PAUSE.log.slice(mark),
          pauses = [];
        for (let i = 0; i < log.length; i++) {
          if (!log[i].paused) continue;
          const res = log.slice(i + 1).find((p) => !p.paused);
          pauses.push({
            at: stamp(log[i].gameMinute),
            gameMinute: log[i].gameMinute,
            reason: log[i].reason,
            resumed: !!res,
            resumedBecause: res ? res.reason : null,
            realSecondsPaused: res ? Math.round((res.atRealMs - log[i].atRealMs) / 100) / 10 : null,
          });
        }
        out.push({
          night: dateText(start),
          from: stamp(start),
          until: stamp(Math.min(G.t, end)),
          tomAt: hook.read().tom.place,
          pauses,
          pausesWithNoResume: pauses.filter((p) => !p.resumed),
        });
        if (neverEnded) break;
      }
      window.LEDGER_MANUAL = manual;
      const none = out.every((n) => !n.pausesWithNoResume.length) && !neverEnded;
      return {
        nights: out,
        pauseNeverEnded: neverEnded,
        watchdogFaults: PAUSE.faults,
        ok: none && PAUSE.faults === 0,
        now: { day: day(), hour: Math.round(hour() * 100) / 100 },
      };
    },
    attend,
    run,
  };
}
