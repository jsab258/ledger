// LEDGER rule piece: the escalation dial (DESIGN section 7). Pure: plain data in, plain data out.
// The dial is a fact in the town's memory, four states: 0 Fists, 1 Shown, 2 Fired, 3 War.
import { TUNE as D } from '../tune/dial.js';

// An event the town may have learned of. ev: { type, witnesses } where witnesses counts everyone who saw or heard it.
// types: blade_seen, gun_seen, gun_fired, crew_armed, guns_bought.
// ER-FIGHT-08: the dial never moves on a deed nobody saw or heard.
function step(state, ev) {
  const same = (why) => ({ state, moved: false, why });
  if (!ev || !(ev.witnesses > 0)) return same('nobody saw or heard it');
  let to = state;
  if (ev.type === 'blade_seen') return same('a blade is no gun');
  if (ev.type === 'gun_seen') to = Math.max(state, 1);
  else if (ev.type === 'gun_fired') to = state >= 2 ? 3 : 2;
  else if (ev.type === 'crew_armed' || ev.type === 'guns_bought') to = state >= 2 ? 3 : Math.max(state, 1);
  else return same('not a thing the dial reads');
  to = Math.min(3, to);
  return to === state ? same('the town knew as much already') : { state: to, moved: true, why: ev.type };
}
// Quiet weeks: one step down after about two quiet game weeks, never back to Fists.
function quiet(state, quietGameDays) {
  if (state > D.neverFallsBelowState && quietGameDays >= D.fallsOneStepAfterQuietGameDays)
    return { state: state - 1, fell: true };
  return { state, fell: false };
}
// How far a shot is heard, in metres. hour 0..24, rain 0..1.
function shotReach(hour, rain) {
  const night = hour >= D.nightFromHour || hour < D.nightUntilHour;
  const r = D.shotHeardByDayMetres * (night ? D.shotHeardAtNightTimes : 1);
  return Math.round(r * (1 - (1 - D.shotHeardInFullRainTimes) * Math.max(0, Math.min(1, rain || 0))));
}
const carriersPerSide = (state) => D.namedCarriersPerSideByState[state] || 0;
// What a shot that hits does. roll 0..1 is handed in (the game's seeded number). Deaths are capped an act.
function shotOutcome(state, deathsThisAct, roll) {
  const kills =
    state >= D.shotKillsFromState && deathsThisAct < D.deathsAnActAtMost && roll < D.shotKillsWhenRollBelowShare;
  return { kills, hurt: kills ? 'dead' : 'badly hurt' };
}
const police = (state) => ({ armedOfficersForGunCalls: state >= 2, armedCars: state >= 3, stopAndSearch: state >= 3 });
const town = (state) => ({
  watchersRunSoonerTimes: D.watchersRunSoonerTimesByState[state],
  witnessesReportMoreTimes: D.witnessesReportMoreTimesByState[state],
  nightFaresTimes: D.nightFaresTimesByState[state],
});
// ER-FIGHT-09: seeded game weeks at War; guns stay rare and killing stays rare.
function warWeeks(seed, weeks) {
  let s = seed >>> 0;
  const rnd = () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  let deaths = 0,
    shots = 0;
  for (let w = 0; w < weeks; w++) {
    const n = Math.floor(rnd() * (D.warIncidentsAGameWeekAtMost + 1));
    for (let i = 0; i < n; i++) {
      shots++;
      if (rnd() < 0.5 && shotOutcome(3, deaths, rnd()).kills) deaths++; // half of all shots hit anybody
    }
  }
  return { carriersPerSide: carriersPerSide(3), shots, deaths, deathsAtMost: D.deathsAnActAtMost };
}
export const PIECE = { name: 'dial_rules', fns: { step, quiet, shotReach, carriersPerSide, shotOutcome, police, town, warWeeks } };
