// RULE PIECE: talk (DESIGN 11, A25, A30, A39). Pure. Unreal ports it and passes test/cases/talk.json.
// Talk never decides alone: every decision is the game's own yes and no, only a plain yes is taken, and what cannot
// be undone asks twice. A character says only what the simulation knows. Greetings by regard are how the rise is heard.
import { TUNE as T } from '../tune/ledgerx.js';
import { TUNE as E } from '../tune/econ.js';

const YES = /^(yes|yeah|aye|all right|alright|ok|okay|go on then|i will|done|agreed|yes please)[.! ]*$/i;
const NO = /^(no|nope|nah|never|not now|no thanks|no thank you|i won'?t)[.! ]*$/i;
// What a typed or picked line is, to the game: 'yes' only when it is a plain yes.
const plain = (text) => (YES.test(String(text).trim()) ? 'yes' : NO.test(String(text).trim()) ? 'no' : 'talk');
// One step of a decision. spec: { undoable: bool }. state: { asked: 0|1 }. A choice that cannot be undone asks twice.
function decide(spec, state, text) {
  const p = plain(text);
  if (p === 'no') return { result: 'no', state: { asked: 0 }, says: null };
  if (p === 'talk') return { result: null, state, says: 'keeps talking' };
  if (!spec.undoable && !state.asked) return { result: null, state: { asked: 1 }, says: 'asks again: this cannot be undone' };
  return { result: 'yes', state: { asked: 0 }, says: null };
}
// A reply's timing (ER-TALK-01): heard in time, the written line instead, or dropped with a brush-off.
const reply = (seconds) => (seconds <= T.replyHeardWithinRealSeconds ? 'heard' : seconds <= T.replyDroppedAfterRealSeconds ? 'the written line plays, the live one follows' : 'dropped with an in-character brush-off');
// The claim check (ER-TALK-04): a reply may state only facts the speaker holds. claims: [fact ids]. Returns the bad ones.
const claims = (said, holds) => said.filter((f) => !holds.includes(f));
// A line may be said again? own line once a day, a shared line once a week per street (ER-TALK-02).
const lineFree = (line, lastSaidDay, today) => lastSaidDay == null || today - lastSaidDay >= (line.shared ? T.sharedLineOnceEveryGameDays : T.ownLineOnceEveryGameDays);
// Greeting by regard (DESIGN 11, ER-RISE-03): which kind of greeting a person gives, from what they hold of him.
function greeting(p) {
  if (!p.knowsHim) return p.rung >= 3 ? 'a nod to a man who matters' : 'neutral';
  if (p.fear >= 0.5) return 'afraid';
  if (p.regard <= -0.3) return 'angry';
  if (p.regard >= 0.3) return 'knows and likes him';
  if (p.marked || p.coatByDay) return 'his appearance';
  return p.rung >= 3 ? 'a door held' : 'neutral';
}
// Haggling without a meter (A30): three offers at most, only prices spoken. buyer: { purse, honestPrice, hot, likes }.
function haggle(buyer, state, move) {
  const base = Math.round(buyer.honestPrice * (buyer.fence ? E.fencePaysShareOfHonestPrice : 1) * (buyer.hot ? 1 - E.haggleHotGoodsCutShare : 1) * (1 + (buyer.likes ? E.haggleLikedAddsShare : 0)));
  const offerAt = (n) => Math.min(buyer.purse, Math.round(base * (1 + (n >= 2 ? E.haggleSecondOfferAddsShare : 0) + (n >= 3 ? E.haggleThirdOfferAddsShare : 0))));
  const s = state || { offers: 0, done: null };
  if (s.done) return { state: s, says: null, price: null };
  if (move === 'open') return { state: { offers: 1, done: null }, says: 'names a price', price: offerAt(1) };
  if (move === 'take') return { state: { offers: s.offers, done: 'sold' }, says: 'counts it out', price: offerAt(s.offers) };
  if (move === 'walk') return { state: { offers: s.offers, done: 'walked' }, says: buyer.likes && s.offers < E.haggleOffersAtMost ? 'calls him back' : 'lets him go, and remembers', price: buyer.likes && s.offers < E.haggleOffersAtMost ? offerAt(s.offers + 1) : null };
  if (move === 'more') {
    if (s.offers >= E.haggleOffersAtMost) return { state: { offers: s.offers, done: 'refused' }, says: 'that is his last word', price: offerAt(s.offers) };
    return { state: { offers: s.offers + 1, done: null }, says: s.offers + 1 >= E.haggleOffersAtMost ? 'his last price' : 'comes up a little', price: offerAt(s.offers + 1) };
  }
  return { state: s, says: null, price: null };
}
// Calling on people (A39): only where and when the routine allows; no score; a second call too soon is cooler.
function visit(p, t) {
  if (!p.routineAllows) return { possible: false, door: 'nobody answers', score: null };
  const soon = p.lastVisitT != null && t - p.lastVisitT < T.visitAgainAfterGameHours * 60;
  return { possible: true, door: soon ? 'cooler: "you again"' : 'asked in', score: null, lastsAtMostRealSeconds: T.visitLastsAtMostRealSeconds, carries: p.knowsOfLastNight ? 'what they heard of last night' : null };
}
// The friendship worth being honest for (3.2.5): it holds on honest visits and breaks on a lie caught.
const friendship = (f) => (f.lieCaught ? 'lost' : f.honestVisits >= T.friendshipHoldsAtVisits ? 'holds' : f.honestVisits > 0 ? 'begun' : 'none');
// How the player speaks (A25): every decision can be reached by pad alone.
const padCan = (talk) => talk.suggested.length > 0 && talk.suggested.some((l) => plain(l) === 'yes') && talk.leaveOffered === true;
export const PIECE = { name: 'talk', fns: { plain, decide, reply, claims, lineFree, greeting, haggle, visit, friendship, padCan } };
