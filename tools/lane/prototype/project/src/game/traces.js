// LEDGER, the whole game: the system "traces". FINDING AN UNSEEN DEED (A38, part 2.5.5). Every deed leaves its
// trace where it was done (a forced door, glass, a missing thing, a body), and whoever's routine next brings them
// past finds it: a named person who really is there, with a clear line to it; the owner when the owner comes back;
// never a roll of chance and never a made-up passer. The finder holds only the aftermath (somebody did this, not
// who), and sets off to ring the police as a witness would (game/walks.js): he can be reached first. A body sunk
// or hidden is never found here; the missing man becomes the town's question instead (game/life.js).
// The real town's own finder of the week's damage is taken as it says. Rule: pieces/eyes.js found.
import { register, X, tell, emit, on, PLACES } from './core.js';
import { G } from '../state.js';
import { hyp, clamp } from '../util.js';
import { remember, logLine } from '../events.js';
import { KINDS } from '../kinds.js';
import { tomNotices } from '../seeing.js';
import { tomName } from '../ui.js';
import { RULES } from '../rules.js';
import { PIECE as EYES } from './pieces/eyes.js';
import { walkFor } from './walks.js';

const T = RULES.game.foot.trace;
export function leaveTrace(kind, what, E, o = {}) {
  const x = X('traces');
  if (!E || x.list.some((q) => q.e === E.id && q.kind === kind)) return null;
  const tr = { n: x.n++, kind, what, e: E.id, x: o.x ?? E.x, z: o.z ?? E.z, owner: o.owner || null, place: o.place || null, t: Math.round(G.t), notBefore: Math.round(o.notBefore || G.t + T.notFoundBeforeGameMinutes), ownerOnly: !!o.ownerOnly, hidden: !!o.hidden, found: null, notBy: [] };
  x.list.push(tr);
  if (x.list.length > 80) x.list.splice(0, x.list.length - 80);
  return tr;
}
const able = (P) => P && !P.dead && !P.gone && !P.anon && P.awake !== false && !P.def.police && !P.fight && !P.down;
// Who is at the trace this minute, by their own routine: the owner first.
function passing(tr) {
  const out = [];
  const pl = tr.place ? PLACES[tr.place] : null;
  for (const P of G.named) {
    if (!able(P) || tr.notBy.includes(P.id) || P.with) continue;
    const owner = P.id === tr.owner;
    if (tr.ownerOnly && !owner) continue;
    const atPlace = owner && pl && pl.room && P.space === pl.room;
    const near = P.space === 'street' && hyp(P.x, P.z, tr.x, tr.z) <= (owner ? T.ownerFindsWithinMetres : T.foundWithinMetres) && G.env.los(P.x, P.z, tr.x, tr.z);
    if (tr.kind === 'pocket' ? owner : atPlace || near) out.push({ id: P.id, t: owner ? G.t - 0.5 : G.t });
  }
  return out;
}
function find(tr, by, atT) {
  const P = G.people[by],
    E = G.ev[tr.e];
  tr.found = { by, t: Math.round(atT) };
  if (!P || !E) return;
  // the aftermath only: somebody did this, never who (unless they saw it done themselves)
  if (!P.mind.by[E.id]) remember(P, E, { src: 'saw', who: 'man', sure: T.aftermathSure, heat: clamp(KINDS[E.kind].sev + T.aftermathHeatAdded, 0, 1) }).aftermath = 1;
  logLine(P.def.name + ' found ' + tr.what, 'police');
  if (tomNotices(P)) tell(`${tomName(P)} has stopped at ${tr.what}, and is looking up and down the street.`, '', 6);
  emit('traces.found', { n: tr.n, by, kind: tr.kind, e: tr.e, what: tr.what });
  // and tells as a witness would: unless the police have it already, off to the phone box
  if (!(E.stmt && E.stmt.length) && tr.kind !== 'pocket') walkFor(E, P, { aftermath: tr.what });
}

register({
  id: 'traces',
  fresh: () => ({ n: 1, list: [] }),
  minute() {
    const x = X('traces');
    for (const tr of x.list) {
      if (tr.found || tr.hidden || G.t < tr.notBefore) continue;
      const r = EYES.fns.found({ t: tr.t, trace: tr.what, hidden: tr.hidden }, passing(tr));
      if (r.by && r.holds === 'aftermath') find(tr, r.by, r.atT);
    }
  },
  hook: {
    x: () => X('traces'),
    open: () => X('traces').list.filter((q) => !q.found && !q.hidden).map((q) => ({ n: q.n, kind: q.kind, what: q.what, x: q.x, z: q.z, owner: q.owner })),
  },
});
// a forced door, a broken window: there to be found
on('crime.damage', (d) => leaveTrace(/door/.test(d.thing) ? 'door' : 'glass', d.thing + (/door/.test(d.thing) ? ', forced' : ', broken'), G.ev[d.e], { owner: d.owner, place: PLACES[d.place] ? d.place : null }));
// a thing gone from a place: its owner finds it on coming back, nobody else would know
on('crime.found', (d) => d.e && leaveTrace('missing', 'the ' + d.thing + ' at ' + (PLACES[d.site] ? PLACES[d.site].name : 'the place') + ' gone through', G.ev[d.e], { owner: (PLACES[d.site] || {}).owner, place: d.site, ownerOnly: true }));
// a pocket picked unfelt: missed by morning, by its owner
on('crime.lifted', (d) => leaveTrace('pocket', 'an empty pocket', G.ev[d.e], { owner: d.from, ownerOnly: true, notBefore: d.missedBy }));
// a body lies where it fell until somebody's day brings them past it
on('act', (E) => E.kind === 'kill' && leaveTrace('body', 'a man lying on ' + E.zone, E, {}));
// the real town names who found the week's damage: that person holds the aftermath
on('town.found', (f) => {
  const x = X('traces'),
    E = G.ev[f.e];
  if (!E || !G.people[f.who]) return;
  const tr = x.list.find((q) => q.e === f.e) || leaveTrace('glass', (E.thing || 'a window') + ', broken', E, {});
  if (tr && !tr.found) find(tr, f.who, G.t);
});
// a finder he stopped never rang: the trace is still there for the next one
on('walks.stopped', (s) => {
  const tr = X('traces').list.find((q) => q.e === s.e && q.found && q.found.by === s.who);
  if (tr && s.aftermath) {
    tr.notBy.push(s.who);
    tr.found = null;
    tr.notBefore = Math.round(G.t + T.nextFinderAfterGameMinutes);
  }
});
