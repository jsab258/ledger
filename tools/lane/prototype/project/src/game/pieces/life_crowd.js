// Rule piece: who is out (DESIGN section 2 "the crowd keeps a few clock windows", section 6 "rain empties the
// street"). Pure and without dice: the same hour, weather and day give the same count. Adults only (canon).
// windows: [{ untilHour, walkers }] in clock order, the last one runs to midnight. wet: 0 dry .. 1 pouring.
function windowCount(hour, windows) {
  for (const w of windows) if (hour < w.untilHour) return w.walkers;
  return windows[windows.length - 1].walkers;
}
function weatherShare(rain, t) {
  if (rain >= t.rainFromRain) return t.rainShare;
  if (rain >= t.drizzleFromRain) return t.drizzleShare;
  return 1;
}
// The count of walkers that should be out. calendarShare from calendar_days.crowdShare.
function crowdCount(hour, rain, calendarShare, windows, t) {
  const base = windowCount(hour, windows);
  return Math.max(0, Math.min(t.walkersAtMost, Math.round(base * weatherShare(rain, t) * calendarShare)));
}
// Voices: rain halves how often the street speaks (DESIGN 6, 17).
function chatterEverySeconds(rain, t) {
  return rain >= t.rainFromRain ? t.streetTalkEveryRealSeconds * 2 : t.streetTalkEveryRealSeconds;
}
// The kinds of people a crowd may hold. Never a child (canon's content rule): ages below are refused.
function crowdAgeOk(ageYears, t) {
  return ageYears >= t.youngestCrowdAgeYears;
}
export const PIECE = { name: 'life_crowd', fns: { windowCount, weatherShare, crowdCount, chatterEverySeconds, crowdAgeOk } };
