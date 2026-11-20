// LEDGER, the whole game: the system "shops". What money buys (DESIGN 9; A21, A30; parts 2.7.5, 2.7.8, 1.6.10,
// 1.6.6): each shop sells only its list, by its hours, from its purse; it refuses and remembers; three outfits and a
// scarf and hat; a barber; the doctor who stitches without asking. No stock tables, no sliders. Rules: pieces/life.js.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on, PLACES } from './core.js';
import { G } from '../state.js';
import { hyp, quid } from '../util.js';
import { pay } from '../money.js';
import { choose, scene } from '../ui.js';
import { RULES } from '../rules.js';
import { PIECE as LIFE } from './pieces/life.js';
import { take } from './crime.js';

const T = RULES.game.shops;
const PRICE = RULES.game.econ.prices;
const WORDS = { cigarettes: 'Twenty cigarettes', paper: 'The paper', meal: 'A plate of dinner', tea: 'A mug of tea', scrap: 'A scrap of fish in paper', crowbar: 'A crowbar', torch: 'A torch', keyCut: 'A key cut', decentJacket: 'A decent jacket', goodOvercoat: 'A good overcoat', scarf: 'A scarf', hat: 'A hat', secondHandCoat: 'A second-hand coat', barber: 'A haircut', stitches: 'Stitches, no questions', usedCar: 'A used car', solicitorRetainer: 'A brief on call', respray: 'A respray' };

// One purchase. The piece decides; the pocket pays; what was bought takes effect.
export function buy(shop, item) {
  const x = X('shops');
  const r = LIFE.fns.shop(shop, item, { hour: hourNow(), dayIndex: dayNow(), pocketPence: G.money.clean, refusesHim: G.x.crime.refused[shop] !== undefined });
  x.tries.push({ shop, item, ok: r.ok, why: r.why || null, t: Math.round(G.t) });
  if (!r.ok) return r;
  if (['torch', 'crowbar', 'scrap'].includes(item) && !take(item)) return { ok: false, why: 'his coat is full' };
  pay(r.pence, true, r.flow.why);
  x.bought.push({ shop, item, pence: r.pence, t: Math.round(G.t) });
  const foot = G.x.foot;
  if (r.outfit) {
    x.outfit = Math.max(x.outfit, r.outfit);
    x.coatSince = G.t; // a new coat breaks the mark for anybody who saw the old one (ER-COAT-01)
  }
  if (item === 'secondHandCoat') x.coatSince = G.t;
  if (item === 'scarf' || item === 'hat') {
    x[item] = true;
    foot.scarf = x.scarf && x.hat;
  }
  if (item === 'barber') x.barberUntilT = G.t + RULES.game.foot.barberLastsGameDays * 1440;
  if (item === 'stitches') {
    G.tom.hurt = 0;
    foot.beatenDay = Math.min(foot.beatenDay, dayNow() - RULES.game.foot.limpLastsGameDays);
  }
  if (item === 'solicitorRetainer') x.brief = true;
  if (item === 'keyCut' && G.x.crime.cased.hut) take('hutkey', { key: 'hut' });
  write(`${WORDS[item]} at ${T.shops[shop].name}: ${quid(r.pence)}.`, { kind: 'money', how: 'Paid for it' });
  emit('shops.bought', { shop, item });
  return r;
}
async function counter(shop) {
  const P = T.shops[shop];
  const items = P.sells.filter((i) => i !== 'usedCar' && i !== 'respray');
  const i = await scene(() => choose('', P.name + '.', items.map((it) => `${WORDS[it]} (${quid(PRICE[it])})`).concat(['Nothing.'])));
  if (i >= items.length) return;
  const r = buy(shop, items[i]);
  if (!r.ok) tell(r.why === 'he has not got it' ? 'He has not got it on him.' : r.why === 'shut' ? 'Shut.' : r.why === 'he is not served here: the keeper remembers' ? '"Not you. Not in here."' : 'They do not sell that.', '');
}
const STREET_SHOPS = { barber: 'barber', doctor: 'doctor', solicitor: 'solicitor' };

register({
  id: 'shops',
  fresh: () => ({ bought: [], tries: [], outfit: 1, coatSince: null, scarf: false, hat: false, barberUntilT: 0, brief: false }),
  hotspots(out) {
    const t = G.tom;
    if (T.shops[t.space] && !['caff', 'news'].includes(t.space) && !out.some((o) => o.k === 'T')) out.push({ k: 'T', t: 'Buy something', run: () => counter(t.space) });
    else if (['caff', 'news'].includes(t.space)) out.push({ k: 'G', t: 'What else do they sell', run: () => counter(t.space) });
    if (t.space !== 'street') return;
    for (const id in STREET_SHOPS) {
      const p = PLACES[STREET_SHOPS[id]];
      if (hyp(t.x, t.z, p.x, p.z) < RULES.game.crime.doorWithinMetres) out.push({ k: 'T', t: p.name[0].toUpperCase() + p.name.slice(1), run: () => counter(id) });
    }
  },
  hook: {
    x: () => X('shops'),
    buy,
    outfit: () => T.outfits[X('shops').outfit],
    list: (shop) => T.shops[shop].sells,
  },
});
