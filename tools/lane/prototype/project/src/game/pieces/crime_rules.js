// LEDGER rule piece: the verbs of jobs done with the hands (DESIGN 4; DESIGN-ADDENDUM A2, A4, A5, A23, A30, A33 to A35;
// parts 1.1.6, 1.6.1 to 1.6.3, 1.6.7, 1.6.9, 1.6.11 to 1.6.14, 2.7.6, 2.8.2, 4.11.1). Pure: plain data in, plain data
// out; nothing rolled, no clock but what is handed in. Every number comes from the tune table (game/tune/crime.js),
// which is plain data; a case may hand in its own table as the last argument.
import { TUNE } from '../tune/crime.js';

const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);

// ---------- A4 searching (ER-SEARCH-01, 02) ----------
// in: { container: 'drawer' | 'desk' | 'wardrobe' | 'crate' | 'cupboard', forced, light 0..1, torch }
// out: { seconds, noiseMetres, dark }. No reflexes and no puzzle: the time passes with the use key held.
function searchTime(q, T = TUNE) {
  const S = T.search,
    base = S[q.container + 'RealSeconds'];
  if (base === undefined) return null;
  const dark = q.light < S.darkBelowLight && !q.torch;
  return {
    seconds: base * (dark ? S.darkWithoutTorchTimes : 1),
    noiseMetres: q.forced && q.container === 'cupboard' ? S.forcedCupboardNoiseMetres : S[q.container + 'NoiseMetres'],
    dark,
  };
}

// ---------- 1.6.1 getting in: a lock has several keys, never a picking game ----------
// site: { key: { holder }, backWay: { fromHour, untilHour, days? }, forceable }
// in: { hasKey, hour, dayIndex }. out: the ways open now, each with what the town can perceive of it.
function waysIn(site, q, T = TUNE) {
  const out = [];
  if (site.key && q.hasKey) out.push({ way: 'key', seconds: 0, noiseMetres: 0, crime: false, mark: false });
  const b = site.backWay;
  if (b) {
    const wraps = b.untilHour <= b.fromHour,
      inside = wraps ? q.hour >= b.fromHour || q.hour < b.untilHour : q.hour >= b.fromHour && q.hour < b.untilHour;
    if (inside && (!b.days || b.days.includes(q.dayIndex % 7)))
      out.push({ way: 'back', seconds: 0, noiseMetres: 0, crime: false, mark: false });
  }
  if (site.forceable !== false)
    out.push({
      way: 'force',
      seconds: T.entry.forceRealSeconds,
      noiseMetres: T.entry.forceNoiseMetres,
      crime: true,
      mark: true,
      markLastsGameMinutes: T.entry.forceMarkLastsGameMinutes,
    });
  return out;
}
// A forced door shows for a day.
function doorShowsForced(forcedAtMinute, nowMinute, T = TUNE) {
  return forcedAtMinute !== null && forcedAtMinute !== undefined && nowMinute - forcedAtMinute < T.entry.forceMarkLastsGameMinutes;
}

// ---------- A5 coat, pockets and storage (ER-POCKET-01, 02) ----------
// carried: { coat: [things], hand: thing | null }. Two things under the coat, one in the hand or a holdall.
function canTake(carried, where, T = TUNE) {
  if (where === 'hand') return !carried.hand;
  return carried.coat.length < T.pockets.underTheCoatAtMost;
}
function take(carried, thing, where, T = TUNE) {
  const c = { coat: carried.coat.slice(), hand: carried.hand };
  const spot = where || (c.coat.length < T.pockets.underTheCoatAtMost ? 'coat' : !c.hand ? 'hand' : null);
  if (!spot || !canTake(c, spot, T)) return { carried: c, ok: false, why: 'His pockets are full and his hand is taken.' };
  if (spot === 'hand') c.hand = thing;
  else c.coat.push(thing);
  return { carried: c, ok: true, where: spot };
}
function drop(carried, thing) {
  const c = { coat: carried.coat.slice(), hand: carried.hand };
  const i = c.coat.indexOf(thing);
  if (i >= 0) c.coat.splice(i, 1);
  else if (c.hand === thing) c.hand = null;
  else return { carried: c, ok: false };
  return { carried: c, ok: true };
}
// A constable's search finds exactly what is under the coat and in the hand, and nothing kept at the office.
function searchFinds(carried) {
  return carried.coat.concat(carried.hand ? [carried.hand] : []);
}
// What he carries, in words, for the Ledger's Open list.
function carriedWords(carried) {
  const parts = [];
  if (carried.coat.length) parts.push('under the coat: ' + carried.coat.join(' and '));
  if (carried.hand) parts.push('in his hand: ' + carried.hand);
  return parts.length ? cap(parts.join('; ')) + '.' : 'Nothing on him.';
}

// ---------- 1.6.3 lifts and the hot mark ----------
// How hot a lifted thing still is in talk, 1 (just taken) to 0. It fades with value (cheap things fastest) and with
// distance (off the owner's street it is half as hot). The owner never forgets, whatever the mark says.
function hotMark(q, T = TUNE) {
  const H = T.hot,
    per = q.honestPence < H.cheapBelowPence ? H.cheapFadesPerGameDay : q.honestPence >= H.dearFromPence ? H.dearFadesPerGameDay : H.middlingFadesPerGameDay;
  let hot = Math.max(0, 1 - per * q.gameDaysSince);
  if (!q.onTheOwnersStreet) hot *= H.offTheOwnersStreetTimes;
  return Math.round(hot * 1000) / 1000;
}
function ownerRecognises(q) {
  // the owner knows his own goods on sight, at any age of the mark; anybody else only while it is hot
  return q.isOwner ? true : hotMark(q) >= TUNE.hot.coldBelow && !!q.heardOfTheTheft;
}

// ---------- 2.7.6 fencing, with A30's haggle (ER-HAGGLE-01) ----------
// The buyer names a price; Tom asks more, takes it or walks. Three offers at most, each a price spoken, no meter.
// in: { honestPence, hot 0..1, pursePence, regard -1..1 }, asks: how often Tom has asked for more (0, 1, 2 ...)
// out: { offerPence, last, walks, face }. face is how he looks: the only sign of how close Tom is.
function fenceOffer(q, asks, T = TUNE) {
  const F = T.fence;
  if (asks >= F.offersAtMost) return { offerPence: 0, last: true, walks: true, face: 'She puts the thing back on the counter and turns away.' };
  const first = q.honestPence * F.shareOfHonestPrice * (1 - F.hotCutsOfferByShare * q.hot),
    ceiling = q.honestPence * F.ceilingShareOfHonestPrice * (1 - F.hotCutsOfferByShare * q.hot);
  let offer = first;
  if (q.regard >= F.holdsWhenRegardBelow) for (let i = 0; i < asks; i++) offer += (ceiling - offer) * F.eachAskClosesShareOfGap;
  offer = Math.min(Math.round(offer / 10) * 10, q.pursePence);
  const last = asks === F.offersAtMost - 1;
  return {
    offerPence: offer,
    last,
    walks: false,
    face: q.regard < F.holdsWhenRegardBelow ? 'Her face does not move at all.' : last ? 'She looks at the door, then back. That is as far as she goes.' : asks ? 'She sucks her teeth and looks it over again.' : 'She turns it over once and names a figure.',
  };
}

// ---------- A34 lifting from a pocket: fixed limits, never dice ----------
// in: { attentive, light 0..1, peopleNear }. Felt when he is attentive, or the light is good, or fewer than three
// people are near. His head turns before any felt lift (ER-EYES-03), so Tom can stop.
function pocketLift(q, T = TUNE) {
  const P = T.pocket,
    felt = !!q.attentive || q.light >= P.poorLightBelow || q.peopleNear < P.crowdAtLeastPeople;
  return { felt, headTurnsAtSeconds: felt ? P.headTurnsAtRealSeconds : null, takesSeconds: P.holdRealSeconds };
}
// A lifted key is missed by the next morning; suspicion falls only on people he noticed near him.
function keyMissed(q, T = TUNE) {
  const dayStart = Math.floor(q.liftedAtMinute / 1440) * 1440,
    missedAt = dayStart + 1440 + T.pocket.missedAtHour * 60;
  return { missedAtMinute: missedAt, suspects: (q.noticedNear || []).slice() };
}

// ---------- A35 damage by hand ----------
function damage(q, T = TUNE) {
  const D = T.damage,
    dayStart = Math.floor(q.atMinute / 1440) * 1440,
    morning = dayStart + D.ownerKnowsAtHour * 60;
  return {
    noiseMetres: D.noiseMetres,
    markUntilMinute: q.atMinute + D.mendedAfterGameMinutes,
    ownerKnowsByMinute: q.atMinute < morning ? morning : morning + 1440,
    town: 'deed',
  };
}
function markShows(mark, nowMinute) {
  return !mark.mended && nowMinute < mark.untilMinute;
}

// ---------- A2 tailing on foot (ER-TAIL-01 to 03) ----------
// One look back by the target. caught: what his look caught of Tom on the watcher's ladder ('nothing', 'shape',
// 'mark', 'face'); knowsHim: whether he can put a name to the face; doubts: looks so far that caught a mark or more.
// A shape is nothing. A mark is a doubt (he speeds up or changes his way). A face he knows ends the tail, but never
// before a doubt has shown (ER-TAIL-02): the first such look is a doubt, held long.
function tailLook(q) {
  if (q.caught === 'nothing' || q.caught === 'shape') return { state: 'clear', doubts: q.doubts, sign: null };
  if (q.caught === 'face' && q.knowsHim && q.doubts >= 1)
    return { state: 'made', doubts: q.doubts + 1, sign: 'He stops, turns right round and looks straight at Tom.' };
  return {
    state: 'doubt',
    doubts: q.doubts + 1,
    sign: q.doubts >= 1 ? 'He looks back again, longer, and takes the next turning.' : 'He looks back, holds it a moment, and walks on quicker.',
  };
}
function tailLooksEvery(nerve, T = TUNE) {
  return nerve <= T.tail.waryAtOrBelowNerve ? T.tail.looksBackEveryRealSecondsWary : T.tail.looksBackEveryRealSecondsCalm;
}
// What the look catches, by the distance and the light (the town's own bands: a shape, a mark, a face).
function tailCaught(q, T = TUNE) {
  if (!q.inSight) return 'nothing';
  const k = Math.max(0.12, q.light);
  if (q.metres <= T.tail.faceWithinMetres * (k >= 0.7 ? 1 : k / 0.7)) return 'face';
  if (q.metres <= T.tail.shapeBeyondMetres * (k >= 0.7 ? 1 : k / 0.7)) return 'mark';
  return 'shape';
}
// A tail never fails on distance (ER-TAIL-01): it ends only made, arrived or stopped by the player.
function tailEnds(q) {
  if (q.made) return 'made';
  if (q.targetArrived && q.sawHimArrive) return 'arrived';
  if (q.playerStopped) return 'stopped';
  return null;
}

// ---------- A23 casing ----------
// What watching a place for so long has taught: its hours, who holds the key, which way is left open.
function caseLearns(secondsWatched, T = TUNE) {
  const C = T.casing,
    out = [];
  if (secondsWatched >= C.hoursAfterRealSeconds) out.push('hours');
  if (secondsWatched >= C.keyHolderAfterRealSeconds) out.push('key');
  if (secondsWatched >= C.openWayAfterRealSeconds) out.push('way');
  return out;
}
// The hours the owner keeps at a place, read from his week (rows in the shape of RULES.schedules): the hours the
// Ledger shows are the routine's own (ER-CASE-01).
function hoursAt(rows, place, dayIndex) {
  const day = rows
    .filter((r) => !r.onDayIndexes || r.onDayIndexes.includes(dayIndex % 7))
    .slice()
    .sort((a, b) => a.fromHour - b.fromHour);
  // a day's own row replaces the everyday row that starts at the same hour
  const rowsToday = day.filter((r, i) => !day.some((o, j) => j !== i && o.fromHour === r.fromHour && o.onDayIndexes && !r.onDayIndexes));
  const out = [];
  for (let i = 0; i < rowsToday.length; i++) {
    if (rowsToday[i].place !== place) continue;
    const until = i + 1 < rowsToday.length ? rowsToday[i + 1].fromHour : 24;
    if (out.length && out[out.length - 1].untilHour === rowsToday[i].fromHour) out[out.length - 1].untilHour = until;
    else out.push({ fromHour: rowsToday[i].fromHour, untilHour: until });
  }
  return out;
}

// ---------- 1.6.7 getting rid of things ----------
// Blood comes off with water and privacy. The launderette washes a coat too, and remembers it.
function washBlood(q) {
  if (q.at === 'launderette') return { clean: true, rememberedBy: 'the attendant' };
  if (q.water && q.private) return { clean: true, rememberedBy: null };
  return { clean: false, rememberedBy: null, why: q.water ? 'Somebody would see.' : 'No water here.' };
}
// What goes in the water is gone, and anybody who saw it keeps it (A11).
function throwIn(carried, thing) {
  const r = drop(carried, thing);
  return { carried: r.carried, gone: r.ok };
}

// ---------- 4.11.1 yard dogs (ER-DOG-01) ----------
function dogBarks(q, T = TUNE) {
  if (!q.stranger) return false;
  if (q.fedMinutesAgo !== null && q.fedMinutesAgo !== undefined && q.fedMinutesAgo < T.dogs.scrapQuietsForGameMinutes) return false;
  return q.metres <= T.dogs.barksWithinMetres;
}
// The verbs a player has toward a dog. None harms it.
const DOG_VERBS = ['give it a scrap', 'walk away'];
function dogVerbs() {
  return DOG_VERBS.slice();
}

// ---------- 2.8.2 partial payment and the book ----------
// A debtor pays what his purse holds and the rest stays on the book. rung: how far the fronting-up went (0 asked,
// 1 stare, 2 square up, 3 threat, 4 shove and on).
function debtPays(q, T = TUNE) {
  const share = q.rung >= 3 ? 1 : T.debts.shareOfPurseBelowAThreat,
    paid = Math.max(0, Math.min(q.owedPence, Math.floor(q.pursePence * share))),
    left = q.owedPence - paid;
  return { paidPence: paid, leftPence: left, purseLeftPence: q.pursePence - paid, st: left === 0 ? 'paid' : 'open' };
}
// Paying in kind: what he hears, goods, or work. worthPence comes off the book; nothing goes in the tin.
function debtInKind(q) {
  const off = Math.min(q.owedPence, q.worthPence);
  return { offPence: off, leftPence: q.owedPence - off, st: q.owedPence - off === 0 ? 'paid' : 'open' };
}

export const PIECE = {
  name: 'crime_rules',
  fns: {
    searchTime,
    waysIn,
    doorShowsForced,
    canTake,
    take,
    drop,
    searchFinds,
    carriedWords,
    hotMark,
    ownerRecognises,
    fenceOffer,
    pocketLift,
    keyMissed,
    damage,
    markShows,
    tailLook,
    tailLooksEvery,
    tailCaught,
    tailEnds,
    caseLearns,
    hoursAt,
    washBlood,
    throwIn,
    dogBarks,
    dogVerbs,
    debtPays,
    debtInKind,
  },
};
