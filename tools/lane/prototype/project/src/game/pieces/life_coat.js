// Rule piece: Tom's wardrobe against what a witness caught (DESIGN section 2 "the coat buys doubt about the face
// and none about the car", section 14 clothes, ADDENDUM A21). Rungs: 0 someone, 1 a shape, 2 a mark, 3 a face,
// 4 recognised. Pure golden rows: ER-COAT-01.
//
// mem: { rung, markCoat: coat id the witness tied the deed to, or null, sawFace: bool }
// now: { coat, hat, scarf, night, barberSince: days since a barber changed his look or null }

// What a witness of an old deed can tie to the man in front of them now.
function tieNow(mem, now, t) {
  let rung = mem.rung;
  // a memory that rests on the coat: a different coat leaves a shape at most
  if (mem.rung === 2 && mem.markCoat && now.coat !== mem.markCoat) rung = 1;
  // a face remembered: a barber changes the look for a week; a scarf up and a hat down hide it at night
  if (mem.rung === 3) {
    const fallback = mem.markCoat && now.coat === mem.markCoat ? 2 : 1;
    if (now.barberSince != null && now.barberSince < t.barberLastsDays) rung = fallback;
    if (now.hat && now.scarf && now.night) rung = Math.min(rung, fallback);
  }
  // recognition is gated by knowing him, never by clothes (the moat): rung 4 stays
  return rung;
}
// What a watcher can catch of him now at most, by what he wears (before distance and light).
function catchCap(now) {
  if (now.hat && now.scarf && now.night) return 2; // the face rung is broken at night; the get-up is itself a mark
  return 4;
}
// A scarf up and a hat down by day are themselves a mark and draw a look (A21).
function drawsALook(now) {
  return !!(now.hat && now.scarf && !now.night) || (now.coat === 'dark' && !now.night);
}
// Which outfit strangers answer to: 0 as he arrived, 1 a decent jacket, 2 a good overcoat (DESIGN 14).
function standingOfDress(coat) {
  return { arrival: 0, secondhand: 0, dark: 0, jacket: 1, overcoat: 2 }[coat] || 0;
}
// A door that asks for dress: he is let in when his dress is at least what the door asks.
function doorOpens(coat, asks) {
  return standingOfDress(coat) >= asks;
}
export const PIECE = { name: 'life_coat', fns: { tieNow, catchCap, drawsALook, standingOfDress, doorOpens } };
