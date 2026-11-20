// Rule piece: the town's calendar (DESIGN-ADDENDUM A20). The game runs from Monday 15 October 1990 for about nine
// game weeks. Pure. dayIndex 0 is Monday 15 October 1990. No real people, events or news; no children anywhere.
const WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const MONTHS = [['October', 31], ['November', 30], ['December', 31], ['January', 31]];

function dateOf(dayIndex) {
  let d = 15 + dayIndex, m = 0;
  while (d > MONTHS[m][1]) { d -= MONTHS[m][1]; m++; }
  return { weekday: WEEKDAYS[((dayIndex % 7) + 7) % 7], dayOfMonth: d, month: MONTHS[m][0], week: Math.floor(dayIndex / 7) + 1 };
}
// What kind of day it is. Bonfire Night is Monday 5 November (day 21); Remembrance Sunday is 11 November (day 27).
function dayKind(dayIndex) {
  const wd = ((dayIndex % 7) + 7) % 7, dt = dateOf(dayIndex);
  return {
    market: wd === 3, // Thursday, Copper Row
    match: wd === 5, // Saturday, at home every week in the prototype
    sunday: wd === 6,
    bonfire: dt.month === 'November' && dt.dayOfMonth === 5,
    remembrance: dt.month === 'November' && dt.dayOfMonth === 11,
    paper: wd === 1 || wd === 4, // the paper comes out Tuesday and Friday
    restock: wd === 0, // shops restock on Monday
    rent: wd === 4,
  };
}
// What changes at this hour of this day, as plain facts the town reads. t: the calendar's numbers (tune/life.js).
function changes(dayIndex, hour, t) {
  const k = dayKind(dayIndex), out = { shopsShut: false, hookShopsQuiet: false, streetFull: false, chapelBusy: false, quayDisplay: false, marketBusy: false, wreath: false };
  if (k.sunday) {
    out.shopsShut = true;
    out.chapelBusy = hour >= t.sundayServiceFromHour && hour < t.sundayServiceUntilHour;
  }
  if (k.market && hour >= t.marketFromHour && hour < t.marketUntilHour) { out.hookShopsQuiet = true; out.marketBusy = true; }
  if (k.match) out.streetFull = t.matchStreetFullHours.some((h) => hour >= h && hour < h + t.matchStreetFullForHours);
  if (k.bonfire) out.quayDisplay = hour >= t.bonfireFromHour && hour < t.bonfireUntilHour;
  if (k.remembrance) { out.wreath = true; out.chapelBusy = hour >= t.remembranceFromHour && hour < t.remembranceUntilHour; }
  return out;
}
// Is a shop open? Shut on Sunday whatever its hours (the caff and the hot food counter excepted: sundayOpen).
function shopOpen(shop, dayIndex, hour) {
  const k = dayKind(dayIndex);
  if (k.sunday && !shop.sundayOpen) return false;
  return hour >= shop.openFromHour && hour < shop.openUntilHour;
}
// Where a person's day differs: returns the place to be, or null for the ordinary routine.
// person: { id, churchgoer, trader (keeps a market stall or shops there), follows (the match), shopkeeper }
function placeFor(person, dayIndex, hour, t) {
  const c = changes(dayIndex, hour, t), k = dayKind(dayIndex);
  if (c.chapelBusy && person.churchgoer) return 'chapel';
  if (c.marketBusy && person.trader) return 'market';
  if (c.quayDisplay && !person.shopkeeper && !person.stayIn) return 'quay';
  if (k.match && person.follows && hour >= t.matchAwayFromHour && hour < t.matchAwayUntilHour) return 'off';
  return null;
}
// The crowd on the Hook's streets as a share of an ordinary weekday at that hour.
function crowdShare(dayIndex, hour, t) {
  const c = changes(dayIndex, hour, t), k = dayKind(dayIndex);
  if (c.streetFull) return t.matchCrowdShare;
  if (c.quayDisplay) return t.bonfireCrowdShare;
  if (c.hookShopsQuiet) return t.marketDayHookShare;
  if (k.sunday) return c.chapelBusy ? t.sundayServiceShare : t.sundayShare;
  return t.weekdayShare;
}
export const PIECE = { name: 'calendar_days', fns: { dateOf, dayKind, changes, shopOpen, placeFor, crowdShare } };
