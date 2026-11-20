// LEDGER, the whole game: the system "shops". Spending, the wardrobe and haggling (DESIGN section 9, ADDENDUM A21,
// A30). Each shop sells only its list, by its hours, from its stock; a fence buys from its purse in three offers at
// most; what money buys is position (a coat, a brief, a tool), never a number.
import { register, PLACES, X, emit } from './core.js';
import { G, day, hour } from '../state.js';
import { RULES } from '../rules.js';
import { PIECE as SHOP } from './pieces/shop_rules.js';
import { PIECE as CAL } from './pieces/calendar_days.js';
import { PIECE as COAT } from './pieces/life_coat.js';
import { say, choose, scene, sub } from '../ui.js';
import { pay, earn } from '../money.js';
import { act } from '../events.js';
import { note } from '../ledger.js';
import { money } from '../util.js';
import { ROOMS } from '../map.js';

const T = RULES.game.shops;
const S = SHOP.fns;
const SHOPS = {};
for (const id in T.shops) {
  const s = T.shops[id];
  SHOPS[id] = Object.assign({ id }, s);
}
const placeOf = (shop) => PLACES[shop.place] || {};
const stOf = (id) => {
  const x = X('shops');
  return x.st[id] || (x.st[id] = S.freshState(SHOPS[id]));
};
export function shopOpen(id, h = hour(), d = day()) {
  const s = SHOPS[id],
    p = placeOf(s);
  if (s.alwaysOpen) return true;
  return CAL.fns.shopOpen({ openFromHour: p.openFromHour ?? 9, openUntilHour: p.openUntilHour ?? 17, sundayOpen: !!s.sundayOpen }, d, h);
}
const keeperName = (s) => (s.keeper && G.people[s.keeper] ? s.keeper : '');
const VOICE = {
  shut: "We're shut.",
  'not sold here': "We don't keep that.",
  'none left this week': "Sold the last. There's more Monday.",
  'not enough money': "That's not enough, and I don't do tick.",
};
// ---------- the wardrobe (1.6.10) ----------
const NIGHT = () => {
  const h = hour();
  return h >= RULES.time.nightFullHour || h < RULES.time.dawnStartsHour;
};
export function dress() {
  const w = X('shops').wardrobe,
    t = G.tom;
  const coat = t.coat ? 'dark' : w.day;
  return {
    coat,
    dayCoat: w.day,
    standing: COAT.fns.standingOfDress(w.day),
    hat: !!(w.up && w.hat),
    scarf: !!(w.up && w.scarf),
    night: NIGHT(),
    barberSince: w.barberDay == null ? null : day() - w.barberDay,
    drawsALook: COAT.fns.drawsALook({ coat, hat: !!(w.up && w.hat), scarf: !!(w.up && w.scarf), night: NIGHT() }),
    catchCap: COAT.fns.catchCap({ hat: !!(w.up && w.hat), scarf: !!(w.up && w.scarf), night: NIGHT() }),
  };
}
// A change of coat: everybody who had tied a deed to the old coat, and not to him, is left with a shape (ER-COAT-01).
function coatChanged(kind, from, to) {
  let broke = 0;
  for (const id in G.people) {
    const P = G.people[id],
      m = P.mind;
    if (!m) continue;
    for (const r of m.mem) {
      if (r.who !== 'coat' || r.linked) continue;
      const E = G.ev[r.e];
      if (!E) continue;
      const was = E.coatId || (E.coat ? (kind === 'night' ? from : 'dark') : from);
      const now = COAT.fns.tieNow({ rung: 2, markCoat: was }, { coat: to }, { barberLastsDays: T.barberLastsDays });
      if (now < 2) {
        r.who = 'man';
        r.coatWas = was;
        r.sure *= 0.5;
        broke++;
      }
    }
    if (kind === 'night' && m.knowsCoat) {
      (m.knewCoats || (m.knewCoats = {}))[from] = 1;
      m.knowsCoat = m.knewCoats[to] ? 1 : 0;
    }
  }
  return broke;
}
export function wear(coat) {
  const w = X('shops').wardrobe;
  if (!w.owned[coat]) return false;
  if (coat === 'dark' || coat === 'mickeys') {
    if (w.night === coat) return true;
    const broke = coatChanged('night', w.night || 'mickeys', coat);
    w.night = coat;
    w.lastBroke = broke;
    return true;
  }
  if (w.day === coat) return true;
  const from = w.day;
  w.day = coat;
  w.lastBroke = coatChanged('day', from, coat);
  emit('dress', dress());
  return true;
}
// ---------- buying ----------
function apply(shop, item) {
  const x = X('shops'),
    w = x.wardrobe,
    it = T.items[item] || {},
    t = G.tom;
  if (it.coat) {
    w.owned[it.coat] = 1;
    if (it.coat === 'dark') {
      t.hasCoat = true; // a dark coat for nights: on and off with the coat key, as Mickey's
      wear('dark');
    } else wear(it.coat);
    act('bought_coat', { what: item, shop: placeOf(shop).name, target: keeperName(shop) || undefined });
    note(`Bought ${item} at ${placeOf(shop).name}.`, 'money', 'coat_' + it.coat, { how: 'Bought it' });
  }
  if (it.wear) w[it.wear] = 1;
  if (it.pocket) {
    t.items[it.pocket] = (t.items[it.pocket] || 0) + 1;
    emit('bought', { item: it.pocket, shop: shop.id });
    if (shop.id === 'ironmonger' && it.pocket !== 'padlock') act('bought_tool', { what: item, target: keeperName(shop) || undefined });
  }
  if (it.mends) t.hurt = Math.max(0, (t.hurt || 0) - it.mends);
  if (it.barber) {
    w.barberDay = day();
    act('haircut', {});
  }
  if (it.flag === 'brief') {
    x.brief = { since: day() };
    act('hired_brief', {});
    note('A solicitor on call: Pym and Tasker, the Corn Exchange. A brief if the police take him in.', 'money', 'brief', { how: 'Paid for it' });
  }
  if (it.wash) {
    act('washed_coat', { target: keeperName(shop) || undefined });
    emit('washed', { what: 'coat' });
    t.bloody = 0;
  }
  if (it.stitches) {
    t.hurt = Math.max(0, (t.hurt || 0) - 0.5);
    act('stitched', { silent: true, told: ['calvert'] });
    emit('stitched', {});
  }
  if (it.read) emit('paper:bought', {});
}
// One sale, with no screen: the rule and its effects. Returns { ok, why, pricePence }.
export function buy(shopId, item) {
  const shop = SHOPS[shopId];
  if (!shop) return { ok: false, why: 'no such shop' };
  const m = G.money,
    it = T.items[item] || {},
    x = X('shops');
  if (it.needs === 'a key to copy' && !(G.hooks.keyToCopy && G.hooks.keyToCopy())) return { ok: false, why: 'nothing to copy', pricePence: 0 };
  if (it.flag === 'brief' && x.brief) return { ok: false, why: 'already has one', pricePence: 0 };
  const r = S.sell(shop, stOf(shopId), item, shopOpen(shopId), m.clean + m.dirty);
  if (!r.ok) {
    stOf(shopId).refused[item] = day();
    return { ok: false, why: r.why, pricePence: 0 };
  }
  if (!pay(r.pricePence, false, 'bought ' + item + ' at ' + shopId)) return { ok: false, why: 'not enough money', pricePence: 0 };
  x.st[shopId] = r.st;
  x.spent.push({ t: Math.round(G.t), shop: shopId, item, pence: r.pricePence });
  if (x.spent.length > 200) x.spent.splice(0, 50);
  apply(shop, item);
  return { ok: true, why: null, pricePence: r.pricePence };
}
async function counter(shopId) {
  const shop = SHOPS[shopId],
    who = keeperName(shop),
    name = placeOf(shop).name || shopId;
  await scene(async () => {
    if (!shopOpen(shopId)) {
      sub(`${name}: shut.`, '', 'over', 3);
      return;
    }
    for (let turn = 0; turn < 6; turn++) {
      const st = stOf(shopId);
      const items = Object.keys(shop.sells);
      const opts = items.map((i) => `${i[0].toUpperCase() + i.slice(1)}, ${money(shop.sells[i])}${(st.stock[i] || 0) <= 0 ? ' (none left)' : ''}`);
      const goods = shop.buys.length && G.hooks.goodsCarried ? G.hooks.goodsCarried().filter((g) => shop.buys.includes(g.kind)) : [];
      if (goods.length) opts.push('Sell: ' + goods[0].name);
      opts.push('Nothing more');
      const i = await choose(who, turn ? 'Anything else?' : `${name}. What will it be?`, opts);
      if (i < 0 || i === opts.length - 1) return;
      if (goods.length && i === items.length) {
        await sellScene(shopId, goods[0]);
        continue;
      }
      const r = buy(shopId, items[i]);
      if (r.ok) await say(who, r.pricePence >= 1000 ? `${money(r.pricePence)}. Thank you.` : `${money(r.pricePence)}.`);
      else await say(who, VOICE[r.why] || (r.why === 'nothing to copy' ? 'Bring me the key and I will cut you another.' : r.why === 'already has one' ? 'You are on our books already, Mr Nowak.' : "I can't do that."));
    }
  });
  if (G.hooks.save) G.hooks.save();
}
// ---------- selling and the haggle (A30) ----------
const regardOf = (shop) => (shop.keeper && G.people[shop.keeper] ? G.people[shop.keeper].mind.regard : 0);
export function startHaggle(shopId, goods) {
  const shop = SHOPS[shopId],
    st = stOf(shopId);
  const no = S.wontBuy(shop, goods, T.haggle) || (st.refused['buy:' + goods.name] != null ? 'told you no' : null);
  if (no) {
    st.refused['buy:' + goods.name] = day();
    return { refused: no };
  }
  return S.startHaggle(goods, regardOf(shop), st.pursePence, T.haggle);
}
export function settle(shopId, goods, h) {
  const shop = SHOPS[shopId],
    st = stOf(shopId),
    who = keeperName(shop);
  if (h.sold) {
    st.pursePence -= h.pricePence;
    earn(h.pricePence, true, 'sold ' + goods.name + ' at ' + shopId);
    act('fenced', { what: goods.name, target: who || undefined, silent: !who });
    if (G.hooks.goodsSold) G.hooks.goodsSold(goods.id, h.pricePence, shopId);
    emit('sold', { goods, pence: h.pricePence, shop: shopId });
  } else {
    st.walked++;
    if (who) act('walked_off', { target: who, silent: true });
  }
}
async function sellScene(shopId, goods) {
  const shop = SHOPS[shopId],
    who = keeperName(shop);
  let h = startHaggle(shopId, goods);
  if (h.refused) return say(who, h.refused === 'not my line' ? 'Not my line. Try elsewhere.' : h.refused === 'told you no' ? 'I told you no. I have not changed.' : 'Too warm for me. Take it away.');
  if (h.done) return say(who, "I've nothing in the drawer for it this week.");
  await say(who, `Let me see it. Hm. ${money(h.offers[0])}.`);
  while (!h.done) {
    const i = await choose(who, h.round === 3 ? `${money(h.offers[2])}. That is the last of it.` : `${money(h.offers[h.round - 1])}. Well?`, ['Take it', 'Ask for more', 'Walk away']);
    h = S.haggle(h, ['take', 'more', 'walk'][i < 0 ? 2 : i], T.haggle);
    if (!h.done && !h.moved) await say(who, 'I said what I said.');
  }
  if (h.sold) await say(who, `${money(h.pricePence)}. You never brought it here.`);
  else if (h.calledBack) {
    const i = await choose(who, `Hold on. ${money(h.offers[h.round])}. Not a penny over.`, ['Take it', 'Keep walking']);
    if (i === 0) h = Object.assign({}, h, { sold: true, pricePence: h.offers[h.round] });
  } else await say(who, h.said === 'last' ? 'Then we are done.' : 'Suit yourself.');
  settle(shopId, goods, h);
}
// ---------- changing ----------
async function change() {
  await scene(async () => {
    const w = X('shops').wardrobe;
    const NAMES = { arrival: 'The coat he arrived in', secondhand: 'The second-hand coat', jacket: 'The decent jacket', overcoat: 'The good overcoat' };
    const opts = [],
      runs = [];
    for (const c of ['arrival', 'secondhand', 'jacket', 'overcoat'])
      if (w.owned[c] && w.day !== c) {
        opts.push(NAMES[c]);
        runs.push(() => wear(c));
      }
    if (w.owned.dark && G.tom.hasCoat) {
      const other = w.night === 'dark' ? 'mickeys' : 'dark';
      if (w.owned[other]) {
        opts.push(other === 'dark' ? 'For nights: the donkey jacket' : "For nights: Mickey's coat");
        runs.push(() => wear(other));
      }
    }
    if (w.hat && w.scarf) {
      opts.push(w.up ? 'Scarf down, hat back' : 'Scarf up, hat down');
      runs.push(() => {
        w.up = !w.up;
      });
    }
    opts.push('As he is');
    const i = await choose('', 'The mirror. What does he put on?', opts);
    if (i >= 0 && runs[i]) {
      runs[i]();
      sub(w.lastBroke ? 'A different man to anybody who only knew the coat.' : 'It will do.', '', 'over', 4);
      w.lastBroke = 0;
    }
  });
}
const canChange = () => {
  const w = X('shops').wardrobe;
  return Object.keys(w.owned).length > 1 || (w.hat && w.scarf);
};
const here = (shop) => {
  const t = G.tom,
    p = placeOf(shop);
  if (shop.room) return t.space === shop.room;
  return t.space === 'street' && p.x != null && Math.hypot(t.x - p.x, t.z - p.z) < T.doorWithinMetres;
};

register({
  id: 'shops',
  fresh: () => ({ st: {}, wardrobe: { day: 'arrival', owned: { arrival: 1, mickeys: 1 }, night: 'mickeys', hat: 0, scarf: 0, up: false, barberDay: null }, brief: null, spent: [], week: 0 }),
  loaded(x) {
    if (!x.wardrobe) x.wardrobe = { day: 'arrival', owned: { arrival: 1, mickeys: 1 }, night: 'mickeys', hat: 0, scarf: 0, up: false, barberDay: null };
    if (!x.st) x.st = {};
    if (!x.spent) x.spent = [];
    G.hooks.dress = dress;
    G.hooks.hasBrief = () => !!X('shops').brief;
    G.hooks.shopOpen = shopOpen;
    G.hooks.sellGoods = (shopId, goods) => scene(() => sellScene(shopId, goods));
    G.hooks.buy = buy;
  },
  daily(d) {
    // the weekly restock, on Monday (DESIGN 9)
    if (!CAL.fns.dayKind(d).restock) return;
    const x = X('shops'),
      wk = Math.floor(d / 7);
    for (const id in SHOPS) x.st[id] = S.restock(SHOPS[id], stOf(id), wk);
    x.week = wk;
  },
  hotspots(out) {
    const t = G.tom;
    for (const id in SHOPS) {
      const shop = SHOPS[id];
      if (!here(shop)) continue;
      if (!Object.keys(shop.sells).length && !(G.hooks.goodsCarried && G.hooks.goodsCarried().length)) continue;
      const name = placeOf(shop).name || id;
      if (!shop.room && !shopOpen(id)) out.push({ k: 'G', t: name + ': shut' });
      else out.push({ k: 'G', t: shop.room ? 'Buy at the counter' : id === 'doctor' ? "Ring Dr Calvert's bell" : 'Go in: ' + name, run: () => counter(id) });
      return;
    }
    if ((t.space === 'boarding' || t.space === 'mickeys') && canChange()) out.push({ k: 'G', t: 'Change at the mirror', run: change });
  },
  hook: {
    list: () => Object.keys(SHOPS).map((id) => ({ id, place: SHOPS[id].place, room: SHOPS[id].room, sells: SHOPS[id].sells, open: shopOpen(id), stock: Object.assign({}, stOf(id).stock), pursePence: stOf(id).pursePence })),
    open: (id, h, d) => shopOpen(id, h, d),
    buy,
    wear,
    dress,
    state: () => JSON.parse(JSON.stringify(X('shops'))),
    startHaggle,
    haggle: (h, move) => S.haggle(h, move, T.haggle),
    settle,
    goInto(id) {
      // put Tom where the shop is used, as the hook's goTo does for other places
      const shop = SHOPS[id],
        p = placeOf(shop),
        t = G.tom;
      if (t.inCar) t.inCar = false;
      if (shop.room && ROOMS[shop.room]) G.hooks.enterRoom(shop.room, true);
      else {
        if (t.space !== 'street' && G.hooks.leaveRoom) G.hooks.leaveRoom();
        t.x = p.x;
        t.z = p.z;
      }
      return here(shop);
    },
    counter,
    restockNow(week) {
      const x = X('shops');
      for (const id in SHOPS) x.st[id] = S.restock(SHOPS[id], stOf(id), week);
    },
  },
});
