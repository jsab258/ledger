// Rule piece: fighter types (DESIGN-ADDENDUM A29). Pure.
// Every fight's men are each one of a few kinds: a boxer who guards, a brawler who rushes, a big man slow to
// drop, a man with a knife who keeps distance (authored only: nobody is handed a knife by this rule).
// ER-TYPES-01: no two fights in a row use the same mix of fighter types.
export const TYPES = ['boxer', 'brawler', 'big'];
const BY_HASH = ['boxer', 'brawler']; // a big man is big by his build, never by chance
const hash = (s) => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return h >>> 0;
};
export const mixOf = (types) => types.slice().sort().join('+');
// men: [{ id, authored (a type written for him, or null), build (0..1, his body) }]. lastMix: the mix of the fight
// before, or ''. Gives the type of each man, in order.
export function pickTypes(men, lastMix) {
  const out = men.map((m) => m.authored || (m.build != null && m.build > 0.7 ? 'big' : BY_HASH[hash(m.id) % BY_HASH.length]));
  if (lastMix && mixOf(out) === lastMix) {
    // change the first man whose type is not authored to the next kind that gives a new mix
    for (let i = 0; i < men.length; i++) {
      if (men[i].authored) continue;
      for (const t of TYPES) {
        const tryIt = out.slice();
        tryIt[i] = t;
        if (mixOf(tryIt) !== lastMix) return tryIt;
      }
    }
  }
  return out;
}
export const PIECE = { name: 'fight_types', fns: { pickTypes, mixOf } };
