// RULE PIECE: what gives him away (DESIGN 2, ER-EYES-10; parts 2.2.5 and 1.4.4). Pure. Unreal ports this and
// passes test/cases/giveaways.json. Each give-away makes a witness catch more than the same act without it.
//
// A give-away is a mark a witness can hold when the face is not caught (the coat, blood, dirt, a weapon in the hand,
// clothes wrong for the door, a bruise, the car, a load), or a thing that draws the eye sooner (running). None is a
// meter: each changes only what a watcher catches.
export const GIVEAWAYS = ['running', 'coat', 'blood', 'dirt', 'weapon', 'wrong_clothes', 'marks', 'car', 'load'];
// tom: { run, coat, blood, dirt, armed, wrongClothes, marks, inCar, carry }  ->  the list he shows now
export function shown(tom) {
  const out = [];
  if (tom.run) out.push('running');
  if (tom.coat) out.push('coat');
  if (tom.blood) out.push('blood');
  if (tom.dirt) out.push('dirt');
  if (tom.armed) out.push('weapon');
  if (tom.wrongClothes) out.push('wrong_clothes');
  if (tom.marks) out.push('marks');
  if (tom.inCar) out.push('car');
  if (tom.carry) out.push('load');
  return out;
}
// Does he carry a mark a witness can hold (the real rule's bHasDistinguishingMark)?
export function hasMark(list) {
  return list.some((g) => g !== 'running');
}
// How much faster he is noticed (running doubles it: DESIGN 2).
export function noticeTimes(list) {
  return list.includes('running') ? 2 : 1;
}
// What a witness catches with the give-aways shown, from the rung the same sighting gives without any (rungPlain)
// and with a mark (rungMarked), both from the real rule. Returns { rung, holds: the things they can describe, more }.
export function caught(rungPlain, rungMarked, list) {
  const mark = hasMark(list);
  const rung = mark ? Math.max(rungPlain, rungMarked) : rungPlain;
  const holds = rung >= 1 ? list.filter((g) => g !== 'running' && (rung >= 2 || g === 'car')) : [];
  return { rung, holds, more: rung > rungPlain || holds.length > 0 || noticeTimes(list) > 1 };
}
export const PIECE = { name: 'giveaways', fns: { shown, hasMark, noticeTimes, caught } };
