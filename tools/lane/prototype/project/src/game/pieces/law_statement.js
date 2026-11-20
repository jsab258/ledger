// Rule piece: who will go to the police about what they saw (DESIGN section 8; rulings 1 Oct and 3 Oct). Pure.
// The thresholds are the prototype's own (rules.js police), handed in so one table stays their home.
// w: { sawPlainly, sure, fear, bought, regard, upright, mickeys, tradeKeepsAway, dead, lost }
// n: { needsSure, noStatementIfFear, uprightQuietAboveRegard, othersQuietAboveRegard }
export function willState(w, n) {
  if (w.dead) return { goes: false, why: 'dead' };
  if (w.mickeys) return { goes: false, why: "Mickey's people never go to the police about one of their own" };
  if (w.tradeKeepsAway) return { goes: false, why: 'their trade keeps them away from the police' };
  if (!w.sawPlainly) return { goes: false, why: 'a noise, a shape or a telling is suspicion, never a statement' };
  if (w.sure < n.needsSure) return { goes: false, why: 'not sure it was him' };
  if (w.fear >= n.noStatementIfFear) return { goes: false, why: 'frightened' };
  if (w.bought) return { goes: false, why: 'paid' };
  if (w.regard > (w.upright ? n.uprightQuietAboveRegard : n.othersQuietAboveRegard)) return { goes: false, why: 'on his side' };
  if (w.lost) return { goes: false, why: 'the statement was lost at the station' };
  return { goes: true, why: 'saw him plainly' };
}
// What stopping a witness on her walk does (DESIGN section 2): a threat can stop a report to the police, never the
// street's talk. answer: 'round' | 'pay' | 'threat' | 'help' | 'go'.
// w: { regard, venal, nerve }; s: the stop table; pence: what he has; crime: the deed's level.
export function stopWitness(answer, w, s, pence, crime) {
  const price = s.payBasePence + s.payMorePencePerCrimeLevel * crime;
  if (answer === 'go') return { police: true, street: true, cost: 0, fear: 0, regard: 0, why: 'let go' };
  if (answer === 'round') {
    const ok = w.regard > s.talkedRoundAboveRegard;
    return { police: !ok, street: true, cost: 0, fear: 0, regard: 0, why: ok ? 'talked round' : 'she thinks too little of him' };
  }
  if (answer === 'pay') {
    const ok = w.venal >= s.paidOnlyIfVenalAtLeast && pence >= price;
    return { police: !ok, street: true, cost: ok ? price : 0, fear: 0, regard: 0, why: ok ? 'paid' : pence < price ? 'he has not got it' : 'she will not be bought' };
  }
  if (answer === 'threat') {
    const ok = w.nerve < s.threatWorksIfNerveBelow;
    return { police: !ok, street: true, cost: 0, fear: ok ? s.threatFearAdded : s.threatFearAdded / 3, regard: -s.threatRegardLost, why: ok ? 'frightened off' : 'she stands' };
  }
  if (answer === 'help') {
    const ok = w.regard + s.helpRegardAdded > s.helpStopsIfRegardThenAbove;
    return { police: !ok, street: true, cost: 0, fear: 0, regard: s.helpRegardAdded, why: ok ? 'a decent turn' : 'a decent turn, and she still goes' };
  }
  return { police: true, street: true, cost: 0, fear: 0, regard: 0, why: 'no answer' };
}
// Where a witness who means to tell goes: a friend near by, a phone box, or the station (no mobiles in 1990).
export function walkTo(w) {
  if (w.friendNearMetres != null && w.friendNearMetres <= w.friendWithinMetres) return 'friend';
  if (w.crime >= 3) return 'station';
  return 'phone';
}
// ER-EYES-04: seen to go, and at least 30 real seconds when it starts in his sight (longer with the assist).
export function walkLasts(walkSeconds, startsInSight, t, assist) {
  const least = startsInSight ? t.lastsAtLeastRealSeconds * (assist ? t.longerWalksAssistTimes : 1) : 0;
  return Math.max(walkSeconds, least);
}
export const PIECE = { name: 'law_statement', fns: { willState, stopWitness, walkTo, walkLasts } };
