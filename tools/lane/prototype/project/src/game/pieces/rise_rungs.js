// LEDGER rule piece: the rise (DESIGN section 14). Position, never numbers. Pure.
import { TUNE as R } from '../tune/rise.js';

const met = (needs, h) =>
  (!needs.tookItOn || !!h.tookItOn) &&
  (h.cars || 0) >= (needs.carsAtLeast || 0) &&
  (h.recruits || 0) >= (needs.recruitsAtLeast || 0) &&
  (!needs.nightDesk || !!h.nightDesk) &&
  (h.fronts || 0) >= (needs.frontsAtLeast || 0) &&
  (h.rounds || 0) >= (needs.roundsAtLeast || 0) &&
  (!needs.coldStore || !!h.coldStore) &&
  (h.posts || 0) >= (needs.postsAtLeast || 0) &&
  (!needs.solicitor || !!h.solicitor);
// The rung his holdings give. One step at a time, and a step never goes back (ER-RISE-02).
function rungFor(h, current) {
  let r = Math.max(1, current || 1);
  if (r < 4 && met(R.rungs[r + 1].needs, h)) r++;
  return r;
}
function missing(h, rung) {
  const n = (R.rungs[rung] || {}).needs || {},
    out = [];
  if (n.tookItOn && !h.tookItOn) out.push('his answer to Sheila');
  if ((h.cars || 0) < (n.carsAtLeast || 0)) out.push('more cars');
  if ((h.recruits || 0) < (n.recruitsAtLeast || 0)) out.push('a recruit');
  if (n.nightDesk && !h.nightDesk) out.push('a night desk');
  if ((h.fronts || 0) < (n.frontsAtLeast || 0)) out.push('a front');
  if ((h.rounds || 0) < (n.roundsAtLeast || 0)) out.push('a round');
  if (n.coldStore && !h.coldStore) out.push('the cold-store contract');
  if ((h.posts || 0) < (n.postsAtLeast || 0)) out.push('men on the gates');
  if (n.solicitor && !h.solicitor) out.push('a brief on call');
  return out;
}
const called = (rung) => R.rungs[rung].called;
const holds = (rung) => R.rungs[rung].holds;
const opens = (rung) => R.rungs.slice(1, rung + 1).flatMap((x) => x.opens);
// ER-RISE-03: what a newcomer can point to between two rungs.
const differences = (a, b) => R.rungs.slice(Math.min(a, b) + 1, Math.max(a, b) + 1).flatMap((x) => x.changes);
// A door: open on standing and dress, or on an introduction, or on an appointment. have: { rung, dress, introducedBy: [ids], appointment: [doorIds] }
function access(doorId, have) {
  const d = R.doors[doorId];
  if (!d) return { open: false, by: null, missing: ['no such door'] };
  if ((have.introducedBy || []).some((id) => d.introducedBy.includes(id))) return { open: true, by: 'an introduction', missing: [] };
  if (d.appointment && (have.appointment || []).includes(doorId)) return { open: true, by: 'an appointment', missing: [] };
  const missing = [];
  if ((have.rung || 1) < d.standingRung) missing.push('standing');
  if ((have.dress || 0) < d.dress) missing.push('dress');
  return { open: !missing.length, by: missing.length ? null : 'standing', missing };
}
const property = (rung) => ({ office: R.officeByRung[rung], flat: R.flatByRung[rung] });
export const PIECE = { name: 'rise_rungs', fns: { rungFor, missing, called, holds, opens, differences, access, property } };
