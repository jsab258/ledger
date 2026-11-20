// LEDGER rule piece: the car in the town. Pure: plain data in, plain data out. `t` is the table game/tune/cars.js.
// Ported to Unreal with the same cases (test/cases/car_rules.json).
const mps = (t, mph) => mph * t.metresPerSecondPerMph;

// What one hit does to the car, by closing speed (DESIGN 5; ER-DRIVE-01, ER-DRIVE-08).
function damage(t, mph, damageBefore) {
  if (mph < t.forgivenBelowMph) return { stage: 'none', damage: damageBefore, drives: true };
  if (mph >= t.willNotDriveOnFromMph) return { stage: 'dead', damage: t.damageAtMost, drives: false };
  const add = mph >= t.crumplesFromMph ? t.crumpleAddsDamage : t.dentAddsDamage;
  return {
    stage: mph >= t.crumplesFromMph ? 'crumpled' : 'dented',
    damage: Math.min(t.damageAtMost, damageBefore + add),
    drives: true,
  };
}
// What a hit does to a person (canon: hurts badly, never kills; ER-DRIVE-03). against: what they land on, which
// never matters for a car (DESIGN 7: a car strike is never a blow under the fall rule).
function hurt(t, mph, aimed, against) {
  void against;
  if (mph < t.knocksDownAboveMph) return { kind: 'none', down: false, hurt: 0, hospitalDays: 0, dies: false, attack: false };
  const h = Math.min(t.hurtAtMost, mph * t.hurtPerMph);
  const kind = mph < t.clipBelowMph ? 'clip' : mph >= t.brokenLegFromMph ? 'brokenleg' : 'badly';
  return {
    kind,
    down: true,
    hurt: Math.round(h * 1000) / 1000,
    downGameMinutes: Math.round(mph * t.downGameMinutesPerMph),
    hospitalDays: kind === 'brokenleg' ? t.hospitalDaysBrokenLeg : kind === 'badly' ? t.hospitalDaysBadly : 0,
    dies: false,
    attack: !!aimed && mph >= t.aimedIsAnAttackFromMph, // a car aimed at a man is an attack with a weapon (rung 7)
  };
}
// The two answers after a hit (ER-DRIVE-05, ER-DRIVE-10). Neither ends the game.
function afterHit(t, choice) {
  if (choice === 'help')
    return { hitAndRun: false, costsGameMinutes: t.helpCostsGameMinutes, faceBesideTheCab: true, firmDays: t.helpedCostsFirmGameDays, faresLostShare: t.helpedFaresLostShareAtFirst, gameOver: false };
  return { hitAndRun: true, costsGameMinutes: 0, faceBesideTheCab: false, carDescribed: true, firmDays: t.driveOffCostsFirmGameDays, faresLostShare: t.driveOffFaresLostShareAtFirst, gameOver: false };
}
// The share of fares people give the other firm, so many game days after a hit. It fades to nothing; the person hit
// never forgets (that is memory, not this). Another hit starts it again from the top.
function faresLost(t, daysSince, hitAndRun) {
  const days = hitAndRun ? t.driveOffCostsFirmGameDays : t.helpedCostsFirmGameDays,
    top = hitAndRun ? t.driveOffFaresLostShareAtFirst : t.helpedFaresLostShareAtFirst;
  if (daysSince < 0 || daysSince >= days) return 0;
  return Math.round(top * (1 - daysSince / days) * 1000) / 1000;
}
// Does a sighting of the car name the car as it is now? (ER-PAINT-01, ER-EYES-10: a deed from the car names the car.)
function names(seen, now) {
  if (seen.paint !== now.paint || seen.sign !== now.sign || seen.plate !== now.plate) return { names: false, firm: false };
  return { names: true, firm: !!now.sign }; // the roof sign makes it the firm's
}
// Does the patrol car stop him? (ER-TRAFFIC-01, 02.) Only a reckless act an officer saw.
function stop(t, did, seen) {
  const why = did.hitAPerson ? 'a hit' : did.onThePavement ? 'the pavement' : did.redLightAtSpeed ? 'a red light' : did.mph >= t.farOverTheLimitMph ? 'speed' : null;
  if (!why) return { stop: false, why: null };
  if (!seen.inLineOfSight || seen.metres > t.patrolSeesWithinMetres) return { stop: false, why: null };
  return { stop: true, why };
}
// How a car chase stands (ER-POL-04): it always ends within 90 real seconds and can always be lost by breaking sight.
function chase(t, s) {
  if (s.metresApart <= t.chaseCaughtWithinMetres && s.slowSeconds >= t.chaseCaughtAfterRealSeconds) return 'caught';
  if (s.unseenSeconds >= t.chaseLostAfterUnseenRealSeconds) return 'lost';
  if (s.metresApart >= t.chaseLostBeyondMetres) return 'lost';
  if (s.elapsedSeconds >= t.chaseEndsByRealSeconds) return 'lost'; // they give it up and put his plate out instead
  return 'on';
}
// The horn (A32): who hears it, and whether a waiting fare comes out.
function hornReach(t, hour, rain) {
  const night = hour >= t.hornNightFromHour || hour < t.hornNightUntilHour;
  return (night ? t.hornReachByNightMetres : t.hornReachByDayMetres) * (1 - t.hornRainCutsShare * rain);
}
const hornHeard = (t, hour, rain, metres) => metres <= hornReach(t, hour, rain);
const hornBringsOut = (t, metres) => (metres <= t.hornBringsFareOutWithinMetres ? t.hornFareOutRealSeconds : null);
// A tail by car (A2; ER-TAIL-01, 02): the man ahead only ever catches what he can see when he looks in his mirror.
// s: { doubt: 0|1, made: false }. look: { looks: bool, inSight: bool, metres, roofSign: bool }.
function tail(t, s, look) {
  if (s.made || !look.looks || !look.inSight) return { doubt: s.doubt, made: !!s.made, shows: null };
  const reach = t.tailMarkWithinMetres * (look.roofSign ? t.tailRoofSignTimes : 1);
  if (look.metres > reach) return { doubt: s.doubt, made: false, shows: null }; // no distance he cannot see ever fails it
  if (!s.doubt) return { doubt: 1, made: false, shows: 'doubt' }; // the doubt always comes first
  return { doubt: 1, made: true, shows: 'made' };
}
// Taking a parked car (A27; ER-TAKE-01).
function take(t, car, nowMinute) {
  if (car.occupied) return { can: false, why: 'somebody is in it' };
  const reported = car.takenAtMinute != null && nowMinute >= car.takenAtMinute + t.ownerFindsItGoneAfterGameMinutes;
  return { can: true, loudMetres: t.takeForceNoiseMetres, seconds: t.takeForceRealSeconds, reported, firms: false };
}
// The ambulance (A22; ER-AMB-01).
const ambulance = (t, calledAtMinute) => calledAtMinute + t.ambulanceArrivesGameMinutes;
// A skipped ride passes exactly its drive time (ER-RIDE-01).
const rideGameMinutes = (t, metres, realSecondsPerGameHour) => (metres / t.rideCruiseMetresPerSecond / realSecondsPerGameHour) * 60;
// Does a driver brake in time for somebody in the road? (4.5.1; ER-DRIVE-03: only the player's car strikes anybody.)
function brakes(t, metresPerSecond, metresAhead, looksAheadMetres) {
  const stopIn = (metresPerSecond * metresPerSecond) / (2 * t.trafficBrakesMetresPerSecondSquared);
  return { sees: metresAhead <= looksAheadMetres, stopsInMetres: Math.round(stopIn * 100) / 100, contact: metresAhead <= looksAheadMetres ? stopIn >= metresAhead : true };
}
export const PIECE = {
  name: 'car_rules',
  fns: { mps, damage, hurt, afterHit, faresLost, names, stop, chase, hornReach, hornHeard, hornBringsOut, tail, take, ambulance, rideGameMinutes, brakes },
};
