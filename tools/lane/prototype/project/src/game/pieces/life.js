// RULE PIECE: the town's days and what money buys (DESIGN 2, 6 and 9; A9, A18 to A21, A24, A31). Pure. Unreal ports
// it and passes test/cases/life.json.
import { TUNE as L } from '../tune/life.js';
import { TUNE as S } from '../tune/shops.js';
import { TUNE as E } from '../tune/econ.js';
import { TUNE as X } from '../tune/ledgerx.js';

const DAYS_IN = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
// The calendar from Monday 15 October 1990: the weekday, the date, and what the day is.
function calendar(dayIndex) {
  let d = L.firstDay.dayOfMonth + dayIndex,
    m = L.firstDay.month,
    y = L.firstDay.year;
  while (d > DAYS_IN[m - 1]) {
    d -= DAYS_IN[m - 1];
    m++;
    if (m > 12) {
      m = 1;
      y++;
    }
  }
  const weekday = (L.firstDay.weekday + dayIndex) % 7;
  const is = [];
  if (weekday === L.marketDayWeekday) is.push('market day in Copper Row');
  if (weekday === L.matchWeekday) is.push('the Saturday match');
  if (weekday === L.sundayWeekday) is.push('Sunday: shops shut, the chapel busy');
  if (d === L.bonfireNight.dayOfMonth && m === L.bonfireNight.month) is.push('Bonfire Night: a display on the quay, adults only');
  if (d === L.remembranceSunday.dayOfMonth && m === L.remembranceSunday.month) is.push('Remembrance Sunday at the chapel');
  return { weekday, dayOfMonth: d, month: m, year: y, week: Math.floor(dayIndex / 7) + 1, is, paperOut: L.paperWeekdays.includes(weekday), children: 0 };
}
// How many of the crowd are out: the hour, the weather and the calendar, the same way every time.
function crowd(hour, weather, dayIndex, most, where = 'hook') {
  const c = calendar(dayIndex);
  let share = L.crowdShareByHour[Math.floor(hour) % 24] * (L.weatherOutShare[weather] ?? 1);
  if (c.weekday === L.marketDayWeekday && where === 'hook' && hour >= 9 && hour < 16) share *= L.marketDayHookShare;
  if (c.weekday === L.matchWeekday && L.matchFillsAtHours.includes(Math.floor(hour))) share *= L.matchHourShare;
  if (c.weekday === L.sundayWeekday) share *= L.sundayShare;
  return Math.max(0, Math.round(most * share));
}
// Cooling by kind: how hot a deed still is in talk (0..1). The memory itself never fades.
function hot(kind, daysSince) {
  const d = L.coolsAfterGameDays[kind];
  if (d === null) return 1; // a body never cools
  if (d === undefined) return Math.max(0, 1 - daysSince / L.coolsAfterGameDays.sighting);
  return Math.max(0, Math.round((1 - daysSince / d) * 1000) / 1000);
}
// The paper (A19): every printed line traces to what Alison saw or was told, at the strength she holds it.
function paper(alisonHolds, dayIndex) {
  if (!calendar(dayIndex).paperOut) return { out: false, lines: [] };
  const lines = alisonHolds.filter((h) => !h.printed && h.sure >= 0.5).map((h) => ({ text: h.sure >= 0.85 && h.namesHim ? h.words : h.words.replace(/\bTom( Nowak)?\b/g, 'a man').replace(/^a man/, 'A man'), from: h.src, e: h.e, sure: h.sure }));
  return { out: true, lines };
}
// A shop sells only its list, by its hours, from its purse; it refuses and remembers.
function shop(id, item, s) {
  const P = S.shops[id];
  if (!P) return { ok: false, why: 'no such shop' };
  const sunday = calendar(s.dayIndex).weekday === L.sundayWeekday && S.shutOnSunday.includes(id);
  if (sunday || s.hour < P.fromHour || s.hour >= P.untilHour) return { ok: false, why: 'shut' };
  if (s.refusesHim) return { ok: false, why: 'he is not served here: the keeper remembers' };
  if (!P.sells.includes(item)) return { ok: false, why: 'not on its list' };
  const pence = E.prices[item];
  if (s.pocketPence < pence) return { ok: false, why: 'he has not got it' };
  return { ok: true, pence, flow: { from: 'pocket', to: 'world', pence, why: item + ' at ' + P.name }, outfit: S.outfitBought[item] || null, remembered: !!P.remembers };
}
// Selling to a shop: it buys only from its purse; the fence at 0.4 of an honest price; the owner knows his goods.
function sell(id, goods, s) {
  const P = S.shops[id];
  if (!P || !P.buys) return { ok: false, why: 'does not buy' };
  if (goods.owner === id) return { ok: false, why: 'the owner recognises the goods', toldAs: 'tried to sell her own goods back to her' };
  const price = Math.min(s.pursePence ?? P.pursePence, Math.round(goods.honestPence * (goods.hot > 0 ? E.fencePaysShareOfHonestPrice : 1)));
  return { ok: true, pence: price, flow: { from: 'world', to: goods.hot > 0 ? 'tin' : 'pocket', pence: price, why: 'sold ' + goods.name + ' at ' + P.name } };
}
// The hot mark fades with value's time and with distance, and the owner never forgets.
const hotMark = (goods, daysSince, metresFromOwner) => ({ hot: Math.max(0, Math.round((1 - daysSince / E.hotMarkFadesOverGameDays) * (metresFromOwner >= E.hotMarkFadesBeyondMetres ? 0.5 : 1) * 1000) / 1000), ownerKnowsIt: true });
// Getting rid of things (1.6.7): washing clears the give-away and plants a witness at the launderette; the water takes anything.
const rid = (how) => (how === 'launderette' ? { clears: 'blood', witness: 'k_laund', remembered: true } : how === 'water and privacy' ? { clears: 'blood', witness: null, remembered: false } : how === 'the water' ? { clears: 'the thing', gone: true, keptByWhoSaw: true } : { clears: null });
// Finding the way (A9): the nudge when lost fires once per goal and never inside 90 s.
function lost(s) {
  if (s.nudged) return s.secondsNoProgress >= X.lostOfferAfterRealSeconds && !s.offered ? { nudge: null, offer: 'the next person within 5 m offers the way' } : { nudge: null, offer: null };
  return s.secondsNoProgress >= X.lostNudgeAfterRealSeconds ? { nudge: 'his own line notes the landmark again', offer: null } : { nudge: null, offer: null };
}
// Asked the way: people who know it say it by landmark; shopkeepers and the constable always know.
const askWay = (p, place) => (p.keeper || p.police || (p.knows || []).includes(place.id) ? { says: place.landmark, knows: true } : { says: 'No idea. Try the caff.', knows: false });
// Knowing the time (A31): the watch for 2 s, street clocks, the chapel bell by day. Never a screen clock.
const time = (s) => ({ watchShowsSeconds: X.watchShowsRealSeconds, knownWithinSeconds: X.hourKnownWithinRealSeconds, bell: s.hour >= X.chapelBellFromHour && s.hour <= X.chapelBellUntilHour && s.minute === 0, screenClock: false });
// Riding as a passenger (A24): a skipped ride passes exactly its drive time.
const ride = (metres, metresPerSecond, realSecondsPerGameHour) => ({ realSeconds: Math.round((metres / metresPerSecond) * 10) / 10, gameMinutes: Math.round((metres / metresPerSecond / realSecondsPerGameHour) * 60 * 100) / 100 });
// Plates and paint (A24): after a respray, sightings of the old paint no longer name this car.
const named = (sighting, car) => !!sighting.sawCar && sighting.paint === car.paint && (car.roofSign ? true : sighting.plate === car.plate || sighting.paint === car.paint);
// Car damage in stages by closing speed (DESIGN 5).
const crash = (mph) => (mph < 10 ? { stage: 'nothing', drives: true } : mph < 20 ? { stage: 'dented', drives: true } : mph < 35 ? { stage: 'crumpled', drives: true } : { stage: 'will not drive on', drives: false, offTheRoadDays: 1, saysSoAtOnce: true, canGetOut: true });
// Street happenings (A18): placed by a named state and the hour, never by dice.
function happening(h, s, log) {
  if (!h.needs.every((n) => s[n])) return { place: false, why: 'its state does not hold' };
  if (s.hour < h.fromHour || s.hour >= h.untilHour) return { place: false, why: 'not its hour' };
  if (log.some((l) => s.playedSeconds - l.playedSeconds < L.happeningNotTwiceWithinRealMinutes * 60 && l.id === h.id)) return { place: false, why: 'not twice in thirty minutes' };
  if (log.some((l) => l.id === h.id && l.street === h.street && s.dayIndex - l.dayIndex < L.happeningNotTwiceAWeekOnOneStreet)) return { place: false, why: 'not twice in a week on one street' };
  return { place: true, why: null, by: h.needs, atMostSeconds: L.happeningLastsAtMostRealSeconds };
}
// Play time booked by activity against the shares (ER-CORE-06, 7.5).
function budget(seconds) {
  const total = Object.values(seconds).reduce((a, b) => a + b, 0) || 1;
  const share = Object.fromEntries(Object.entries(seconds).map(([k, v]) => [k, Math.round((v / total) * 100) / 100]));
  const faults = [];
  if ((share.talk || 0) > L.talkShareAtMost) faults.push('talk over 30%');
  if ((share.waiting || 0) > L.waitShareAtMost) faults.push('waiting over 10%');
  if ((share.driving || 0) > L.drivingShareAtMost) faults.push('driving over 25%');
  return { share, faults };
}
export const PIECE = { name: 'life', fns: { calendar, crowd, hot, paper, shop, sell, hotMark, rid, lost, askWay, time, ride, named, crash, happening, budget } };
