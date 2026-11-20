// Shared small helpers of the rise's systems (crew, rivals, rise, firm, dial). No rules here.
import { G } from '../state.js';
import { ensureX } from './core.js';

export const P_ = (id) => G.people[id];
export const X = (id) => ensureX()[id] || {};
// The act the story is in (the spine's state), read with a default.
export const actNow = () => (G.x && G.x.acts && G.x.acts.act) || 1;
export const runEnded = () =>
  !!((G.x && G.x.jobsx && G.x.jobsx.arrangement === 'ended') || G.story.flags.choice === 'wind' || G.story.flags.ask1 === 'no');
export const rungNow = () => (G.x && G.x.rise && G.x.rise.rung) || 1;
export const first = (P) => (P && P.def ? P.def.name.split(' ')[0] : '');
// Everybody who holds an event, seen or heard or told.
export function knowers(E) {
  const out = [];
  for (const id in G.people) {
    const P = G.people[id];
    if (P && P.mind && P.mind.by && P.mind.by[E.id]) out.push(id);
  }
  return out;
}
export const moneyAll = () => G.money.clean + G.money.dirty;
export const zoneOf = (P) => (G.env.zone ? G.env.zone(P.x, P.z) : 'Quay Street');
// Tom and a person are both on the street (or in the same room) and within d metres.
export function near(P, d) {
  const t = G.tom;
  return !!P && !P.gone && !P.dead && P.space === t.space && Math.hypot(P.x - t.x, P.z - t.z) < d;
}
