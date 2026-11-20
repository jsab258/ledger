// RULE PIECE: what a witness keeps of him, from the rung the real rule gives (Perception::IdRung: 0 someone,
// 1 a silhouette, 2 a mark, 3 a face, 4 recognised). Pure: plain data in, plain data out. Unreal ports this and
// passes test/cases/witness_mind.json. The rung itself is the town code's; this is only how a mind holds it.
//
// who: 'tom' (it was him, by name), 'owner' (the new man at Mickey's, face not sure), 'coat' or 'cab' (a thing of
// his: a mark), 'man' (somebody). face: how well the face was caught, 0 to 1 (a face caught and not yet placed can
// be placed later, once the witness learns who he is). sure: a witness is only as sure as what they caught.
export function mindOfRung(rung, o, T) {
  // o: { knowsWho, inCar, coat }   T: the tuning table (RULES.game.town)
  const r = Math.max(0, Math.min(4, rung | 0));
  let who = 'man';
  if (r >= 4) who = o.knowsWho ? 'tom' : 'man'; // recognised: a name only from somebody who knows who he is
  else if (r === 3) who = o.knowsWho ? 'owner' : 'man';
  else if (r === 2) who = o.inCar ? 'cab' : o.coat ? 'coat' : 'man';
  if (o.inCar && r >= 1 && who === 'man') who = 'cab'; // a deed done from the car always names the car (ER-EYES-10)
  const named = who === 'tom';
  return { who, face: T.faceScoreAtRung[r], sure: T.sureAtRung[r], rung: r, named };
}
// The rung a kept memory supports, for telling the town of something a mind already holds.
export function rungOfMind(m) {
  if (Number.isInteger(m.rung)) return m.rung;
  if (m.who === 'tom') return 4;
  if (m.who === 'owner') return 3;
  if (m.who === 'coat' || m.who === 'cab') return 2;
  return m.face > 0.2 ? 3 : 1;
}
// What the police file calls a kind of act (Offence: 0 suspicious, 1 damage, 2 assault, 3 wounding, 4 robbery, 5 killing).
export function offenceOf(kindId, kind, T) {
  if (kind && Number.isInteger(kind.offence)) return kind.offence;
  if (Object.prototype.hasOwnProperty.call(T.offenceOfKind, kindId)) return T.offenceOfKind[kindId];
  if (kind && kind.town === 'deed') return 1;
  if (kind && kind.town !== undefined) return T.offenceOfCrimeLevel[Math.max(0, Math.min(4, kind.crime | 0))] || 0;
  return 0;
}
// Whether his face is toward a witness: the witness stands within the half angle of the way he faces; in the cab only
// close and lit; under the runner's coat, collar up, not once night is on (the coat buys doubt about the face).
export function faceToward(o, T) {
  // o: { offRadians, inCar, metres, light, coat, night }
  if (o.inCar) return o.metres < T.inCabFaceWithinMetres && o.light > T.inCabFaceAboveLight;
  if (o.coat && o.night > T.coatHidesFaceWhenNightAbove) return false;
  return Math.abs(o.offRadians) <= T.faceTowardHalfAngleRadians;
}
// The goodwill toward him the real rule (PoliceFile::WouldReport) is asked with, for somebody the cast file lacks.
export function hostLoyalty(regard, T) {
  return Math.max(0, Math.min(1, T.hostLoyaltyBase + T.hostLoyaltyPerRegard * regard));
}
export const PIECE = { name: 'witness_mind', fns: { mindOfRung, rungOfMind, offenceOf, faceToward, hostLoyalty } };
