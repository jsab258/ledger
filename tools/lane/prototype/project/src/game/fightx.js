// LEDGER, the whole game: the system "fightx". What the one-shot adds round the fight the prototype already has
// (DESIGN 7; A23, A28, A29; parts 1.3.6, 1.3.12, 7.16): the quiet blow from behind on a man who has not seen him,
// searching a man who is down, fighter types so written fights differ, and the boxing club: sparring with the
// gloves on, no stakes, no blood, the fall rule off. Guard, slip, counter and breath are the prototype's own keys
// (K, Space, J after either); their rules are held to pieces/fights.js.
import { register, X, write, tell, hourNow, P_, emit, PLACES } from './core.js';
import { G } from '../state.js';
import { hyp, angDiff } from '../util.js';
import { act } from '../events.js';
import { choose, scene, say } from '../ui.js';
import { RULES } from '../rules.js';
import { PIECE as FIGHTS } from './pieces/fights.js';
import { PIECE as EYES } from './pieces/eyes.js';
import { target as aimedAt } from '../fight.js';
import { has, take } from './crime.js';

const T = RULES.game.fightx;
const F = FIGHTS.fns;
const S = { doing: null };

// The quiet blow (A23): a cosh or a fist from behind on a man who has not seen him. A strike like any other.
function quietHotspot(out) {
  const P = aimedAt(),
    t = G.tom;
  if (!P || P.anon || P.down || P.fight || t.space !== P.space) return;
  const d = hyp(P.x, P.z, t.x, t.z),
    behind = Math.abs(angDiff(P.ang, Math.atan2(t.x - P.x, t.z - P.z))) > T.quietBlowFromBehindAboveRadians;
  if (d > T.quietBlowWithinMetres || !behind || (P.mind.look || 0) > 0 || !F.mayLayHandsOn({ woman: P.def.sex === 'f', age: P.def.age || 40, priest: P.id === 'walsh' })) return;
  if (!has('cosh') && !t.weapon) return;
  out.push({ k: 'G', t: 'Put him down from behind', run: () => {
    P.down = true;
    P.downT = G.t + T.quietBlowDownGameMinutes;
    P.route = null;
    P.moving = false;
    const Ev = act('quiet_blow', { target: P.id, weapon: has('cosh') ? 'cosh' : t.weapon });
    X('fightx').quiet.push({ who: P.id, e: Ev.id, sawShape: (Ev.wit || []).length, t: Math.round(G.t) });
    write(`Put ${P.def.name} down from behind. He never saw who.`, { who: P.id, how: 'Did it' });
  } });
}
// A man down can be searched (A29): what he carried, in the time the table gives; seen like any act.
function searchHotspot(out) {
  const t = G.tom,
    x = X('fightx');
  const P = G.named.find((Q) => Q.down && !Q.dead && Q.space === t.space && hyp(Q.x, Q.z, t.x, t.z) < T.searchManWithinMetres && !x.searched[Q.id]);
  if (!P) return;
  out.push({ k: 'T', t: 'Go through his pockets', run: () => {
    const r = EYES.fns.search('man', {});
    S.doing = { left: r.seconds, x: t.x, z: t.z, done: () => {
      x.searched[P.id] = Math.round(G.t);
      act('searched_man', { target: P.id });
      const thing = RULES.game.crime.pockets[P.id];
      if (thing && !G.x.crime.lifted[P.id] && take(thing, { key: RULES.game.crime.things[thing].key })) {
        G.x.crime.lifted[P.id] = Math.round(G.t);
        write(`Went through ${P.def.name}'s pockets while he was down: ${RULES.game.crime.things[thing].name}.`, { who: P.id, how: 'Did it' });
      } else write(`Went through ${P.def.name}'s pockets while he was down. Nothing worth the taking.`, { who: P.id, how: 'Did it' });
    } };
    tell('Going through his pockets...', '', r.seconds + 1);
  } });
}
// The boxing club (A28): sparring with gloves, the fall rule off, no stakes of any kind.
async function spar() {
  const x = X('fightx');
  let his = 0,
    mine = 0;
  await scene(async () => {
    await say('The trainer', 'Gloves on. Three rounds, nobody gets hurt, nobody gets paid. Hands up.');
    for (let r = 0; r < T.sparRounds; r++) {
      const blow = ['jab', 'heavy', 'jab'][r];
      const i = await choose('', `Round ${r + 1}. His shoulder drops: a ${blow === 'heavy' ? 'big right' : 'jab'} is coming.`, ['Guard.', 'Slip it.', 'Swing first.']);
      const res = F.incoming(blow, ['guard', 'slip', 'nothing'][i], 0.5);
      const c = F.counter(['guard', 'slip', 'nothing'][i], 0.2);
      his += res.hurt;
      if (c.lands) mine += RULES.game.fightx.hurt.counter;
    }
    await say('The trainer', mine > his ? 'You read him. That is all boxing is. Come again.' : 'You swung first every time. He was waiting for it. Come again.');
  });
  const fall = F.fall({ surface: 'wall', secondsSinceBlow: 0, sparring: true }, 0);
  act('sparred', { silent: true, told: ['ron'].filter((id) => P_(id) && !P_(id).dead) });
  x.spars.push({ won: mine > his, dies: fall.dies, stakes: 0, t: Math.round(G.t) });
  write('Three rounds with the gloves on at the boxing club. No money in it, and nobody hurt.', { key: 'spar:' + Math.floor(G.t / 1440), how: 'Did it' });
  emit('fightx.sparred', { won: mine > his });
}
// No two written fights running use the same mix of fighter types (ER-TYPES-01).
export function fightMix(ids) {
  const x = X('fightx');
  const types = ids.map((id) => T.typeOf[id] || 'brawler');
  const ok = F.mixAllowed(types, x.lastMix);
  if (!ok && types.length) types[0] = types[0] === 'brawler' ? 'boxer' : 'brawler'; // the writing changes one man's kind rather than repeat
  x.lastMix = types.slice().sort().join('+');
  x.mixes.push(x.lastMix);
  return types;
}

register({
  id: 'fightx',
  fresh: () => ({ quiet: [], searched: {}, spars: [], lastMix: '', mixes: [] }),
  step(dt) {
    const d = S.doing,
      t = G.tom;
    if (!d || G.paused) return;
    if (hyp(t.x, t.z, d.x, d.z) > 0.6) S.doing = null;
    else if ((d.left -= dt) <= 0) {
      S.doing = null;
      d.done();
    }
  },
  hotspots(out) {
    const t = G.tom,
      p = PLACES.boxing;
    quietHotspot(out);
    searchHotspot(out);
    if (t.space === 'street' && hyp(t.x, t.z, p.x, p.z) < RULES.game.crime.doorWithinMetres + 1 && hourNow() >= T.sparFromHour && hourNow() < T.sparUntilHour) out.push({ k: 'T', t: 'The boxing club: spar a round', run: spar });
  },
  hook: {
    x: () => X('fightx'),
    spar,
    fightMix,
    finishDoing: () => {
      const d = S.doing;
      S.doing = null;
      if (d) d.done();
      return !!d;
    },
    types: () => T.typeOf,
    rules: { incoming: F.incoming, counter: F.counter, breath: F.breath, stands: F.stands, odds: F.odds },
  },
});
