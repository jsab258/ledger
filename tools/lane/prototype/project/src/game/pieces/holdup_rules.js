// LEDGER rule piece: hold-ups of shops and people (DESIGN-ADDENDUM A41). Pure.
import { TUNE as D } from '../tune/dial.js';

const tier = (weapon) => D.holdUpWeapons[weapon] || null;
// ER-HOLDUP-01. ctx: { rung, weapon, shown, target: { kind: 'shop'|'person'|'house'|'car', open, sex, age, priest } }
function can(ctx) {
  const t = ctx.target || {};
  const no = (why) => ({ ok: false, why });
  if ((ctx.rung || 1) < D.holdUpFromRung) return no('Not yet. He is nobody here, and a nobody with a knife is only a thief.');
  if (!tier(ctx.weapon)) return no('Not with bare hands. That is fronting a man up, not a hold-up.');
  if (!ctx.shown) return no('The weapon has to be out first.');
  if (t.kind === 'house') return no('Not a house. He does not go into homes for a purse.');
  if (t.kind === 'car') return no('Not a car with somebody in it.');
  if (t.kind === 'shop' && !t.open) return no('The shop is shut. There is nobody at the counter.');
  if (t.sex === 'f' || t.priest || (t.age || 0) >= D.holdUpTomSparesFromAgeYears)
    return no('No. Not a woman, not the old, not the priest. That is his own line.');
  return { ok: true, why: '' };
}
// How the mark answers: by his own nerve and by who is watching. Never a roll.
function outcome(mark, ctx) {
  const face = Math.min(D.holdUpNerveAddedAtMost, (ctx.watchers || 0) * D.holdUpNerveAddedPerWatcher);
  const nerve = (mark.nerve ?? 0.5) + face;
  const press = D.holdUpPressureByWeapon[tier(ctx.weapon)] || 0;
  if (nerve >= press + 0.25) return 'stands';
  if (nerve >= press) return ctx.watchers > 0 ? 'shouts' : 'runs';
  return 'gives';
}
// ER-HOLDUP-03: only what the purse or the till holds, and only when he gives way.
const take = (pursePence, how) => (how === 'gives' ? Math.max(0, Math.round(pursePence)) : 0);
const till = (dayIndex) => (dayIndex % 7 === 5 ? D.holdUpShopTillSaturdayPence : D.holdUpShopTillPence);
// ER-HOLDUP-02: the mark is always a witness, at the face rung unless the face was covered.
function witness(covered) {
  return covered ? { rung: 2, as: 'a mark', sure: 0.6 } : { rung: 3, as: 'a face', sure: 1 };
}
// ER-HOLDUP-04: what the dial is told.
const dialEvent = (weapon, witnesses) => ({ type: tier(weapon) === 'gun' ? 'gun_seen' : 'blade_seen', witnesses });
// ER-HOLDUP-05: what follows, each step carried by a person. t in game minutes.
function aftermath(ctx) {
  const day = Math.floor(ctx.t / 1440),
    next9 = (day + 1) * 1440 + D.holdUpEllisComesAtHour * 60;
  let a = [
    { what: 'walk', by: ctx.mark, at: ctx.t },
    { what: 'report', by: ctx.mark, at: ctx.t + 30 },
    { what: 'street on edge', street: ctx.street, from: ctx.t, until: ctx.t + D.holdUpStreetOnEdgeGameDays * 1440, by: ctx.mark },
    { what: 'ellis', street: ctx.street, at: next9, by: ctx.mark },
    { what: 'a cooler name', by: ctx.mark, from: ctx.t, until: ctx.t + D.holdUpNameCoolsGameDays * 1440 },
    { what: 'night fares fall', street: ctx.street, from: ctx.t, until: ctx.t + D.holdUpFaresFallGameDays * 1440, times: D.holdUpFaresTimes, by: ctx.mark },
  ];
  // reached first (talked round, paid or threatened before the phone): no report and no detective; the talk stands
  if (ctx.reached) a = a.filter((x) => x.what !== 'report' && x.what !== 'ellis');
  return a;
}
const withinADay = (ctx) => aftermath(ctx).every((x) => (x.at ?? x.from) - ctx.t <= 1440 && !!x.by);
export const PIECE = { name: 'holdup_rules', fns: { can, outcome, take, till, witness, dialEvent, aftermath, withinADay, tier } };
