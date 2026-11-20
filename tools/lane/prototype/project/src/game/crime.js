// LEDGER, the whole game: the system "crime". Crime with the hands (DESIGN 4; A4, A5, A23, A27, A33 to A35, A41;
// parts 1.6.1 to 1.6.3, 1.6.7, 1.6.9, 1.6.11 to 1.6.14, 2.7.6, 3.5.3, 4.11.1 and hold-ups): getting in three ways,
// searching and taking, goods with a hot mark and the fence, a hand in a pocket, damage by hand, casing a place, a
// torch, the yard dog, getting rid of things, the pockets and the office drawer, and holding a place up.
// No lockpicking, no search game: a press, a time, a noise at its reach, and what the town then holds.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on, PLACES } from './core.js';
import { G } from '../state.js';
import { hyp, angDiff, quid } from '../util.js';
import { act } from '../events.js';
import { earn } from '../money.js';
import { advanceTo } from '../work.js';
import { choose, scene, say } from '../ui.js';
import { RULES } from '../rules.js';
import { PIECE as EYES } from './pieces/eyes.js';
import { PIECE as TALK } from './pieces/talk.js';
import { PIECE as LIFE } from './pieces/life.js';
import { PIECE as RISE } from './pieces/rise.js';
import { setTorch } from './foot.js';
import { target as aimedAt } from '../fight.js';

const T = RULES.game.crime;
const F = RULES.game.foot;
const E = EYES.fns;
const S = { doing: null, inside: null, casing: null };
const night = () => hourNow() >= F.nightFromHour || hourNow() < F.nightUntilHour;
const raining = () => G.weather.rain > RULES.weather.rainingAboveRain;

// ---- the pockets (A5): two things under the coat; the rest lives at the office ----
export const has = (id) => X('crime').pockets.some((i) => i.id === id);
export function take(id, o = {}) {
  const x = X('crime'),
    th = T.things[id] || { name: o.name || id };
  if (x.pockets.length >= T.underTheCoatAtMost) return tell('Two things under the coat is all it hides. Something has to go in the drawer at the office first.', ''), false;
  x.pockets.push(Object.assign({ id, name: th.name, unlawful: !!th.unlawful }, o));
  return true;
}
export function drop(id) {
  const x = X('crime'),
    i = x.pockets.findIndex((p) => p.id === id);
  return i >= 0 ? x.pockets.splice(i, 1)[0] : null;
}
// What a constable's search finds: exactly what he carries (ER-POCKET-01).
export const carried = () => X('crime').pockets.map((p) => ({ id: p.id, name: p.name, unlawful: p.unlawful })).concat(G.tom.carry === 'bag' ? [{ id: 'bag', name: 'the holdall', unlawful: true }] : []);
export const stored = () => X('crime').stored.slice();
// ---- a thing that takes a moment: started with one press, done if he stays put (ER-SEARCH-02) ----
function begin(label, seconds, done) {
  S.doing = { label, left: seconds, x: G.tom.x, z: G.tom.z, done };
  tell(label + '...', '', seconds + 1);
}
// ---- getting in (1.6.1): a key, a back way a routine leaves open, or force ----
function wayIn(site, how) {
  const x = X('crime'),
    p = PLACES[site.place];
  if (how === 'force') {
    const Ev = act('forced_door', { thing: 'the door of ' + site.name, noiseR: E.reach('forcedDoor', hourNow(), raining()) });
    x.marks.push({ what: 'the forced door of ' + site.name, place: site.place, untilT: G.t + T.damageShowsGameDays * 1440, e: Ev.id });
    emit('crime.damage', { e: Ev.id, owner: p.owner, thing: 'the door of ' + site.name, place: site.place });
  }
  x.entries.push({ site: site.place, how, t: Math.round(G.t) });
  S.inside = { site: site.place, how };
  x.inside = site.place;
  if (site.room && G.hooks.enterRoom) G.hooks.enterRoom(site.room, how !== 'force');
  write(`Got into ${site.name}: ${how === 'key' ? 'with the key' : how === 'back way' ? site.backWay.what : 'forced the door, and it shows'}.`, { how: 'Did it' });
  emit('crime.entered', { site: site.place, how });
}
function siteHotspots(out) {
  const t = G.tom,
    x = X('crime');
  for (const id in T.sites) {
    const s = T.sites[id],
      p = PLACES[s.place];
    if (s.fromRung && (G.x.rise ? G.x.rise.rung : 1) < s.fromRung) continue;
    const open = E.trespass(p, hourNow(), 0).stage === 'free';
    const inside = x.inside === s.place && (s.room ? t.space === s.room : hyp(t.x, t.z, s.door[0], s.door[1]) < T.containerWithinMetres * 2);
    if (!inside && t.space === 'street' && hyp(t.x, t.z, s.door[0], s.door[1]) < T.doorWithinMetres && (!open || !s.room)) {
      if (has(s.key + 'key') || x.pockets.some((i) => i.key === s.key)) out.push({ k: 'E', t: 'Use the key: ' + s.name, run: () => wayIn(s, 'key') });
      else if (x.cased[s.place] && hourNow() >= s.backWay.fromHour && hourNow() < s.backWay.untilHour) out.push({ k: 'E', t: 'The back way: ' + s.name, run: () => wayIn(s, 'back way') });
      else out.push({ k: 'E', t: 'Locked: ' + s.name, run: () => tell(x.cased[s.place] ? `Locked. ${s.backWay.what}: that is the hour for it. Or a key (${s.keyFrom}).` : 'Locked. A key, a way somebody leaves open, or the door itself.', '') });
      out.push({ k: 'G', t: 'Force the door (loud)', run: () => wayIn(s, 'force') });
    }
    if (inside)
      for (const c of s.containers) {
        if (x.searched[s.place + ':' + c.id]) continue;
        out.push({ k: out.some((o) => o.k === 'E') ? 'T' : 'E', t: 'Search ' + c.name, run: () => searchStart(s, c) });
        if (out.filter((o) => o.k === 'E' || o.k === 'T').length >= 2) break;
      }
  }
}
// ---- searching and taking (A4, A33) ----
function searchStart(site, c) {
  const x = X('crime');
  if (c.needsKey && !x.pockets.some((i) => i.key === c.needsKey)) return tell('It wants its key. Somebody carries it.', '');
  const dark = night() && G.env.lightAt(G.tom.x, G.tom.z, G.tom.space) < F.light.unlit + T.darkAboveUnlitBy;
  const r = E.search(c.kind, { dark, torch: x.torchOn, window: !!site.room, night: night() });
  if (r.beamSeenFromStreet) {
    // a beam moving behind a window is seen from the street, as a precursor only (A33)
    const seenBy = G.named.filter((P) => !P.gone && P.space === 'street' && P.awake && hyp(P.x, P.z, site.door[0], site.door[1]) < F.markAtMetres);
    if (seenBy.length) act('torch_seen', { place: site.name, silent: true, told: seenBy.map((P) => P.id) });
  }
  G.tom.noiseP = Math.max(G.tom.noiseP, r.noiseMetres);
  begin('Searching ' + c.name, r.seconds, () => {
    x.searched[site.place + ':' + c.id] = Math.round(G.t);
    x.searches.push({ site: site.place, c: c.id, seconds: r.seconds, dark, torch: x.torchOn, t: Math.round(G.t) });
    act('searched', { thing: c.name, place: site.name });
    if (c.holds) earn(c.holds.pence, true, c.holds.why);
    if (c.goods) x.goods.push(Object.assign({ takenT: G.t, from: site.place }, c.goods));
    if (c.fact) x.facts[c.fact] = Math.round(G.t);
    write(c.line, { key: 'found:' + site.place + ':' + c.id, how: 'Found it' });
    tell(c.line, '', 7);
    emit('crime.found', { site: site.place, c: c.id, fact: c.fact || null, pence: c.holds ? c.holds.pence : 0 });
  });
}
// ---- the fence (2.7.6, A30): Rita's back room buys, haggles in three offers at most, and remembers ----
async function fence() {
  const x = X('crime'),
    g = x.goods[0];
  if (!g) return;
  const r0 = LIFE.fns.sell('rita', { name: g.name, honestPence: g.honestPence, hot: 1, owner: g.owner }, {});
  if (!r0.ok) {
    act('sold_back', { target: 'rita' });
    x.refused.rita = dayNow();
    return scene(() => say('rita', `That is off my own shelf. Get out of my shop.`));
  }
  const hot = LIFE.fns.hotMark(g, (G.t - g.takenT) / 1440, 0).hot > 0.5;
  const buyer = { purse: x.purse.rita, honestPrice: g.honestPence, fence: true, hot, likes: P_('rita').mind.regard > 0.3 };
  let st = null,
    r = TALK.fns.haggle(buyer, st, 'open');
  st = r.state;
  await scene(async () => {
    for (let n = 0; n < RULES.game.econ.haggleOffersAtMost + 1 && !st.done; n++) {
      const i = await choose('rita', `${quid(r.price)} for ${g.name}. ${r.says === 'his last price' ? 'That is my last word.' : hot ? 'It is warm, that. I can feel it from here.' : 'Take it or leave it.'}`, ['Take it.', 'Ask for more.', 'Walk away.']);
      r = TALK.fns.haggle(buyer, st, ['take', 'more', 'walk'][i]);
      st = r.state;
    }
  });
  x.haggles.push({ goods: g.id, offers: st.offers, done: st.done, t: Math.round(G.t) });
  if (st.done === 'sold') {
    x.goods.shift();
    x.purse.rita -= r.price;
    earn(r.price, true, 'sold ' + g.name + " at Rita's");
    act('fenced', { thing: g.name, silent: true, told: ['rita'] });
    write(`Sold ${g.name} in Rita's back room for ${quid(r.price)}. It went in the tin.`, { kind: 'money', who: 'rita', how: 'Did it' });
  } else write(`Rita would not come up on ${g.name}. She will remember he walked.`, { who: 'rita', how: 'Did it' });
}
// ---- a hand in a pocket (A34): fixed limits, never a roll; his head turns before he feels it ----
function pocketHotspot(out) {
  const P = aimedAt(),
    t = G.tom,
    x = X('crime');
  if (!P || P.anon || !T.pockets[P.id] || x.lifted[P.id] || t.space !== P.space) return;
  const d = hyp(P.x, P.z, t.x, t.z),
    behind = Math.abs(angDiff(P.ang, Math.atan2(t.x - P.x, t.z - P.z))) > T.liftFromBehindAboveRadians;
  if (d > T.liftWithinMetres || !behind) return;
  out.push({
    k: 'G',
    t: 'Lift from his pocket',
    run: () => {
      const near = G.named.concat(G.crowd).filter((Q) => Q !== P && !Q.gone && Q.space === P.space && hyp(Q.x, Q.z, P.x, P.z) < F.amongPeopleWithinMetres * 2);
      const r = E.lift({ attentive: !!P.mind.look || P.state === 'idle', light: t.light, peopleNear: near.length, noticedNear: near.filter((Q) => !Q.anon).map((Q) => Q.id) });
      if (r.felt) {
        P.ang = Math.atan2(t.x - P.x, t.z - P.z); // his head turns first: there is a moment to stop
        begin('His head is turning', r.headTurnsFirstBySeconds, () => {
          act('pocket', { target: P.id });
          x.lifts.push({ from: P.id, felt: true, t: Math.round(G.t) });
          tell('"Oi. What do you think you are doing?"', P.def.name);
          emit('crime.felt', { P });
        });
      } else
        begin('Easing it out', r.holdSeconds, () => {
          x.lifted[P.id] = Math.round(G.t);
          x.lifts.push({ from: P.id, felt: false, suspects: r.suspects, missedBy: (dayNow() + 1) * 1440 + 7 * 60, t: Math.round(G.t) });
          take(T.pockets[P.id], { key: T.things[T.pockets[P.id]].key });
          write(`Lifted ${T.things[T.pockets[P.id]].name} from ${P.def.name}'s pocket. It will be missed by morning.`, { who: P.id, how: 'Did it' });
        });
    },
  });
}
// ---- damage by hand (A35) ----
function damageHotspot(out) {
  const t = G.tom,
    x = X('crime');
  if (t.space !== 'street' || !night()) return;
  for (const d of T.damage) {
    if (x.damaged[d.id] || hyp(t.x, t.z, d.at[0], d.at[1]) > T.doorWithinMetres + 1) continue;
    out.push({
      k: 'G',
      t: 'Put it in: ' + d.thing,
      run: () => {
        const Ev = act('window_in', { thing: d.thing, noiseR: E.reach('brokenGlass', hourNow(), raining()) });
        x.damaged[d.id] = Math.round(G.t);
        x.marks.push({ what: d.thing + ', broken', place: d.id, untilT: null, e: Ev.id }); // it stays until mended (2.19)
        write(`Put ${d.thing} in. It will be there to see in the morning.`, { how: 'Did it', ev: Ev.id });
        emit('crime.damage', { e: Ev.id, owner: d.owner, thing: d.thing, place: d.id });
      },
    });
    return;
  }
}
// ---- casing (A23): watching a place a while learns its hours, its key holder and the way left open ----
function casingHotspot(out) {
  const t = G.tom,
    x = X('crime');
  if (t.space !== 'street') return;
  for (const id in T.sites) {
    const s = T.sites[id],
      d = hyp(t.inCar ? G.car.x : t.x, t.inCar ? G.car.z : t.z, s.door[0], s.door[1]);
    if (x.cased[s.place] || d < T.doorWithinMetres + 2 || d > T.casingWithinMetres) continue;
    out.push({ k: 'T', t: 'Watch ' + s.name + ' a while', run: () => caseNow(s) });
    return;
  }
}
function caseNow(s) {
  const x = X('crime'),
    p = PLACES[s.place];
  advanceTo(G.t + F.casingLearnsAfterGameMinutes, false); // he stands and watches, and can be seen doing it
  const r = E.cased(F.casingLearnsAfterGameMinutes, { openFromHour: p.openFromHour ?? null, openUntilHour: p.openUntilHour ?? null, keyHolder: p.owner, openWay: s.backWay.what });
  x.cased[s.place] = Math.round(G.t);
  act('cased', { place: s.name });
  write(`Watched ${s.name}. ${p.openFromHour != null ? `Open ${p.openFromHour} to ${p.openUntilHour}. ` : ''}The key: ${s.keyFrom}. Left open: ${r.openWay}.${s.dog ? ' There is a dog.' : ''}`, { key: 'cased:' + s.place, how: 'Watched it himself' });
}
// ---- the yard dog (A23): barks at a stranger; a scrap of food quiets it; dogs are never hurt ----
function dogStep() {
  const t = G.tom,
    x = X('crime'),
    p = PLACES.scrap;
  if (t.space !== 'street' || hyp(t.x, t.z, p.x, p.z) > T.dogBarksWithinMetres) return;
  if (E.trespass(p, hourNow(), 0).stage === 'free' || G.t < x.dogQuietUntilT || G.t - x.dogBarkedT < 5) return;
  if (has('scrap')) {
    drop('scrap');
    x.dogQuietUntilT = G.t + T.dogQuietForGameMinutes;
    return tell('The dog takes the scrap of fish and lies down with it.', '');
  }
  x.dogBarkedT = G.t;
  x.barks.push(Math.round(G.t));
  t.noiseP = Math.max(t.noiseP, E.reach('bark', hourNow(), raining()));
  act('dog_barked', { place: "Iveson's yard", silent: true });
  tell("Iveson's dog goes off at the end of its chain.", '');
  emit('crime.bark', { owner: 'dennis' });
}
// ---- getting rid of things (1.6.7, A11) ----
function ridHotspots(out) {
  const t = G.tom,
    x = X('crime');
  if (t.space === 'street' && t.z > T.quayEdgeZMetres - T.waterWithinMetres && x.pockets.length)
    out.push({ k: 'T', t: 'Throw ' + x.pockets[0].name + ' in the water', run: () => {
      const it = drop(x.pockets[0].id);
      act('threw_in', { thing: it.name }); // what goes in is gone, and anybody who saw it keeps it
      write(`${it.name[0].toUpperCase() + it.name.slice(1)} went in the river.`, { how: 'Did it' });
    } });
  if (t.space === 'laund' && (t.blood || x.bloody)) out.push({ k: 'T', t: 'A service wash for the coat (a pound)', run: () => {
    x.bloody = false;
    t.blood = 0;
    act('washed', { silent: true, told: ['k_laund'] }); // the launderette washes it, and remembers
    write('Put the coat through a service wash. The attendant looked at the collar, and at him.', { how: 'Did it' });
  } });
  if (t.space === 'mickeys') out.push({ k: 'G', t: 'The locked drawer', run: drawer });
}
async function drawer() {
  const x = X('crime');
  const opts = x.pockets.map((p) => 'Put away ' + p.name).concat(x.stored.map((s) => 'Take ' + s.name), ['Shut it.']);
  const i = await scene(() => choose('', 'The locked drawer. ' + (x.stored.length ? 'In it: ' + x.stored.map((s) => s.name).join(', ') + '.' : 'Empty.'), opts));
  if (i < x.pockets.length) x.stored.push(x.pockets.splice(i, 1)[0]);
  else if (i < x.pockets.length + x.stored.length) {
    if (x.pockets.length >= T.underTheCoatAtMost) return tell('Two things under the coat is all it hides.', '');
    x.pockets.push(x.stored.splice(i - x.pockets.length, 1)[0]);
  }
}
// ---- holding a place up (A41): rare and late, loud, always witnessed, never a game over ----
function holdupHotspot(out) {
  const t = G.tom,
    x = X('crime'),
    shop = RULES.game.rise.holdupTargets.includes(t.space) && PLACES[t.space] ? t.space : null;
  if (!shop || !t.armed) return;
  const owner = G.people[PLACES[shop].owner];
  const keeper = owner && owner.space === t.space && !owner.gone ? owner : G.named.concat(G.crowd).find((P) => P.space === t.space && P.keeper);
  const gun = has('gun');
  const may = RISE.fns.holdupMay({ rung: G.x.rise ? G.x.rise.rung : 1, weaponOut: true, gun, gunThrough: gun ? G.x.dial && G.x.dial.gunThrough : null, target: shop, keeper: keeper ? { age: keeper.def.age || 40, priest: keeper.id === 'walsh' } : null, heldUpBefore: x.heldUp, thisWeek: x.holdups.filter((h) => Math.floor(h.t / 10080) === Math.floor(G.t / 10080)).length, streetOnEdge: !!(G.x.law && G.x.law.edge) });
  if (!may.may || !keeper) return;
  out.push({ k: 'G', t: 'Hold the place up', run: () => holdup(shop, keeper, gun) });
}
async function holdup(shop, keeper, gun) {
  const x = X('crime'),
    p = PLACES[shop],
    inside = G.named.concat(G.crowd).filter((P) => P !== keeper && P.space === G.tom.space && !P.gone);
  const s = { target: shop, tillPence: Math.min(x.purse[shop] ?? RISE.fns.till(hourNow()), RISE.fns.till(hourNow())), keeperNerve: keeper.def.nerve ?? 0.4, inside: inside.map((P) => P.id), gun };
  let r,
    waited = false;
  await scene(async () => {
    for (let n = 0; n < 3; n++) {
      const i = await choose('', n ? `${keeper.anon ? 'The keeper' : keeper.def.name} has not moved. "There is nothing in it," and both of them know there is.` : `"The till. Now." ${p.name} goes very quiet.`, ['Wait.', 'Threaten again.', 'Go.']);
      r = RISE.fns.holdup(Object.assign({ waited }, s), ['wait', 'threaten again', 'go'][i]);
      waited = true;
      if (r.outcome !== 'stalls') break;
    }
  });
  const Ev = act('holdup', { place: p.name, weapon: gun ? 'gun' : G.tom.weapon || 'weapon', told: [keeper.id].concat(s.inside).filter((id) => G.people[id]), noiseR: E.reach('shout', hourNow(), raining()) });
  x.heldUp.push(shop);
  x.refused[shop] = dayNow();
  if (r.flow) {
    earn(r.take, true, r.flow.why);
    x.purse[shop] = 0;
    take('tillnotes');
  }
  x.holdups.push({ shop, outcome: r.outcome, take: r.take, witnesses: r.witnesses, reported: r.reported, e: Ev.id, t: Math.round(G.t) });
  write(`Held up ${p.name}: ${r.outcome}${r.take ? ', ' + quid(r.take) + ' in the tin' : ''}. Everybody in there saw his face.`, { how: 'Did it', ev: Ev.id });
  emit('crime.holdup', { shop, keeper, r, e: Ev.id, gun });
}

register({
  id: 'crime',
  fresh: () => ({ pockets: [], stored: [], goods: [], facts: {}, cased: {}, searched: {}, searches: [], entries: [], inside: null, marks: [], damaged: {}, lifted: {}, lifts: [], haggles: [], refused: {}, purse: { rita: RULES.game.shops.shops.rita.pursePence }, heldUp: [], holdups: [], torchOn: false, bloody: false, dogQuietUntilT: 0, dogBarkedT: -99, barks: [], allowed: {} }),
  loaded(x) {
    S.doing = null;
    setTorch(x.torchOn);
  },
  step(dt) {
    if (G.paused) return;
    const t = G.tom,
      x = X('crime');
    const d = S.doing;
    if (d) {
      if (hyp(t.x, t.z, d.x, d.z) > 0.6) S.doing = null; // he moved off: nothing is taken, nothing is found
      else if ((d.left -= dt) <= 0) {
        S.doing = null;
        d.done();
      }
    }
    if (x.inside) {
      const s = Object.values(T.sites).find((q) => q.place === x.inside);
      if (s.room ? t.space !== s.room : hyp(t.x, t.z, s.door[0], s.door[1]) > T.containerWithinMetres * 3) x.inside = null;
    }
    dogStep();
  },
  hourly() {
    const x = X('crime');
    x.marks = x.marks.filter((m) => m.untilT === null || m.untilT > G.t); // a forced door shows for a day; a window until mended
  },
  daily(d) {
    if (d % 7 === 0) X('crime').purse = { rita: RULES.game.shops.shops.rita.pursePence }; // the weekly restock
  },
  key(code) {
    if (code !== 'KeyI' || G.tom.inCar) return false;
    const x = X('crime');
    if (!has('torch')) return tell('He has no torch. The ironmonger sells them.', ''), true;
    x.torchOn = !x.torchOn;
    setTorch(x.torchOn);
    tell(x.torchOn ? 'The torch is on. He can see what he is doing, and can be seen doing it.' : 'Torch off.', '');
    return true;
  },
  hotspots(out) {
    if (S.doing) return;
    siteHotspots(out);
    pocketHotspot(out);
    damageHotspot(out);
    casingHotspot(out);
    ridHotspots(out);
    holdupHotspot(out);
    if (G.tom.space === 'rita' && X('crime').goods.length && here(P_('rita'), 6) && X('crime').refused.rita === undefined) out.push({ k: 'T', t: "Show Rita what he has to sell", run: fence });
  },
  hook: {
    x: () => X('crime'),
    has,
    take,
    drop,
    carried,
    stored,
    sites: () => T.sites,
    wayIn: (site, how) => wayIn(T.sites[site], how),
    search: (site, c) => searchStart(T.sites[site], T.sites[site].containers.find((q) => q.id === c)),
    doing: () => (S.doing ? { label: S.doing.label, left: S.doing.left } : null),
    finishDoing: () => {
      const d = S.doing;
      S.doing = null;
      if (d) d.done();
      return !!d;
    },
    caseNow: (site) => caseNow(T.sites[site]),
    fence,
    holdup: (shop) => holdup(shop, G.named.concat(G.crowd).find((P) => P.keeper && P.space === shop) || P_(PLACES[shop].owner), has('gun')),
    marks: () => X('crime').marks,
  },
});
on('econ.week', () => {});
