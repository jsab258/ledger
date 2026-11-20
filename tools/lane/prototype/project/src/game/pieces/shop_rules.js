// Rule piece: shops and spending (DESIGN section 9 "everybody's money is somebody's circumstance", ADDENDUM A21, A30).
// Each shop sells only its list, by its hours, from its stock; it buys only from its purse; restocked weekly.
// Pure. shop: { id, sells: { item: pricePence }, stock: { item: n }, pursePence, buys: [itemKinds], openFromHour,
// openUntilHour, sundayOpen }. state: { stock: { item: n }, pursePence, refused: { key: day }, walked: n }

function freshState(shop) {
  return { stock: Object.assign({}, shop.stock), pursePence: shop.pursePence, refused: {}, walked: 0, week: 0 };
}
// ER-SPEND-01. Why a sale cannot happen, or null when it can.
function cannotSell(shop, st, item, open, pocketPence) {
  if (!open) return 'shut';
  if (!(item in shop.sells)) return 'not sold here';
  if ((st.stock[item] || 0) <= 0) return 'none left this week';
  if (pocketPence < shop.sells[item]) return 'not enough money';
  return null;
}
function sell(shop, st, item, open, pocketPence) {
  const why = cannotSell(shop, st, item, open, pocketPence);
  if (why) return { ok: false, why, st, pricePence: 0 };
  const n = Object.assign({}, st, { stock: Object.assign({}, st.stock, { [item]: st.stock[item] - 1 }), pursePence: st.pursePence + shop.sells[item] });
  return { ok: true, why: null, st: n, pricePence: shop.sells[item] };
}
// The weekly restock (Monday): stock back to the list, the purse back to its float.
function restock(shop, st, week) {
  if (st.week === week) return st;
  return Object.assign({}, st, { stock: Object.assign({}, shop.stock), pursePence: shop.pursePence, week });
}
// A30: a haggle is three offers at most. The buyer names a price; Tom asks more, takes it, or walks.
// goods: { honestPence, hot: 0..1 }. regard: -1..1 (how the buyer regards Tom). share: the buyer's opening share of
// the honest price (Rita's back room about 0.4). Returns the buyer's offers for rounds 1 to 3, never over the purse.
function offers(goods, regard, pursePence, t) {
  const open = t.openingShare * (1 - t.hotCutsShare * goods.hot) * (1 + t.regardAddsShare * regard);
  const top = Math.min(t.topShare, open + t.risePerAskShare * 2);
  const out = [];
  for (let i = 0; i < 3; i++) {
    const share = Math.min(top, open + t.risePerAskShare * i);
    out.push(Math.max(0, Math.min(pursePence, Math.round((goods.honestPence * share) / 5) * 5)));
  }
  return out;
}
// One move of a haggle. h: { round: 1..3, offers, done, sold, pricePence }. move: 'take' | 'more' | 'walk'.
// ER-HAGGLE-01: never more than three offers; the only numbers are the prices spoken.
function haggle(h, move, t) {
  if (h.done) return h;
  const n = Object.assign({}, h);
  if (move === 'take') return Object.assign(n, { done: true, sold: true, pricePence: h.offers[h.round - 1] });
  if (move === 'walk') return Object.assign(n, { done: true, sold: false, pricePence: 0, calledBack: h.round < 3 && h.offers[h.round] > h.offers[h.round - 1] && !!t.callsBack });
  // 'more': the next offer if there is one and it is better; else he will not go higher and it stands or falls
  if (h.round >= 3) return Object.assign(n, { done: true, sold: false, pricePence: 0, said: 'last' });
  n.round = h.round + 1;
  n.moved = h.offers[n.round - 1] > h.offers[h.round - 1];
  return n;
}
function startHaggle(goods, regard, pursePence, t) {
  const o = offers(goods, regard, pursePence, t);
  if (o[0] <= 0) return { round: 0, offers: o, done: true, sold: false, pricePence: 0, said: 'refused' };
  return { round: 1, offers: o, done: false, sold: false, pricePence: 0 };
}
// A shop that will not touch goods: too hot for an honest counter, or not its kind of thing. It remembers.
function wontBuy(shop, goods, t) {
  if (!(shop.buys || []).includes(goods.kind)) return 'not my line';
  if (!shop.fence && goods.hot > t.honestShopRefusesAboveHot) return 'too warm for me';
  return null;
}
export const PIECE = { name: 'shop_rules', fns: { freshState, cannotSell, sell, restock, offers, haggle, startHaggle, wontBuy } };
