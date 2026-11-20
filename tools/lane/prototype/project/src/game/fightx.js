// LEDGER, the whole game: the system "fightx". What joins the fight (fight.js) to the rest: fighter types (A29), the
// grab that holds a man (A29), the quiet blow from behind (A23), the weapon on a held input (ER-FIGHT-08), a man
// put in the water (A11), people stepping in, a man down searched, and how every fight ended ('fight:end').
import { register, emit, on } from './core.js';
import { G } from '../state.js';
import { hyp, clamp, angDiff } from '../util.js';
import { act, mkEvent, remember } from '../events.js';
import { sub, bubble, tomName } from '../ui.js';
import { blocked, inWater } from '../map.js';
import { perceivers, sense, tomTarget } from '../seeing.js';
import { F, target, end as fightEnd, drawHeld } from '../fight.js';
import { keys } from '../player.js';
import { RULES } from '../rules.js';
import { pickTypes, mixOf } from './pieces/fight_types.js';

const FX = RULES.game.fightx,
  LAD = RULES.ladder;
const R = { held: 0, hold: null, holdCool: 0, wet: [], log: [], searchT: 0, searchP: null };
const said = (what, x) => {
  R.log.push(Object.assign({ what, t: G.t }, x || {}));
  if (R.log.length > 200) R.log.shift();
};
const live = () => F.foes.filter((f) => f.st !== 'down' && f.st !== 'flee');

// ---------- fighter types (A29, ER-TYPES-01) ----------
function types(foes) {
  const need = foes.filter((f) => !f.type);
  if (!need.length) return;
  const men = foes.map((f) => ({ id: f.P.id || f.P.def.name || 'man', authored: f.type || f.P.def.fighter || (f.P.weapon === 'knife' ? 'knife' : null), build: f.P.def.look ? f.P.def.look.b : null }));
  const got = pickTypes(men, G.x.fightx.lastMix || '');
  foes.forEach((f, i) => (f.type = got[i]));
  G.x.fightx.mixNow = mixOf(got);
}

// ---------- the grab: holds a man about 2 s (A29) ----------
function holdMan() {
  if (R.hold || R.holdCool > 0 || !F.on || F.rung < LAD.strikeRung) return false;
  const t = G.tom;
  let best = null,
    bd = FX.hold.reachMetres;
  for (const f of live()) {
    const d = hyp(f.P.x, f.P.z, t.x, t.z);
    if (d < bd && f.st !== 'windup' && f.st !== 'strike' && Math.abs(angDiff(t.ang, Math.atan2(f.P.x - t.x, f.P.z - t.z))) < 1.0) {
      bd = d;
      best = f;
    }
  }
  if (!best) return false;
  best.was = best.st;
  best.st = 'held';
  best.P.fight.mode = 'stagger';
  R.hold = { f: best, t: FX.hold.lastsRealSeconds };
  sub(`He has ${tomName(best.P)} by the collar. [J] push him, [G] take what is in his hand, [X] let go.`, '', 'over', 2.5);
  said('hold', { who: best.P.id });
  return true;
}
function letGo(why) {
  const h = R.hold;
  if (!h) return;
  R.hold = null;
  R.holdCool = FX.hold.coolDownRealSeconds;
  if (h.f.st === 'held') {
    h.f.st = 'guard';
    h.f.t = 0.6;
    if (h.f.P.fight) h.f.P.fight.mode = 'guard';
  }
  said('let go', { who: h.f.P.id, why });
}
function push() {
  const h = R.hold,
    t = G.tom,
    f = h.f,
    P = f.P;
  const dx = Math.sin(t.ang),
    dz = Math.cos(t.ang);
  let x = P.x,
    z = P.z,
    into = null;
  for (let s = 0.2; s <= FX.hold.pushMetres; s += 0.2) {
    const nx = P.x + dx * s,
      nz = P.z + dz * s;
    if (inWater(nx, nz)) {
      into = 'water';
      x = nx;
      z = nz;
      break;
    }
    if (blocked(nx, nz, 0.3)) {
      into = 'wall';
      break;
    }
    x = nx;
    z = nz;
  }
  R.hold = null;
  R.holdCool = FX.hold.coolDownRealSeconds;
  if (into === 'water') {
    f.st = 'flee';
    intoWater(P, x, z);
    return 'water';
  }
  P.x = x;
  P.z = z;
  f.st = 'stagger';
  f.t = into ? FX.hold.pushStaggerRealSeconds : 0.5;
  if (P.fight) P.fight.mode = 'stagger';
  if (into) {
    P.hurt = clamp((P.hurt || 0) + FX.hold.pushIntoPlaceHurts, 0, 0.98);
    sub('Into the wall.', '', 'over', 2);
    if (G.hooks.sfx) G.hooks.sfx('thud');
    if (G.hooks.shake) G.hooks.shake(0.3);
  }
  said('push', { who: P.id, into: into || 'clear ground' });
  return into || 'clear';
}
function disarm() {
  const h = R.hold,
    P = h.f.P,
    t = G.tom;
  if (!P.weapon) {
    sub('Nothing in his hands.', '', 'over', 2);
    return false;
  }
  const w = P.weapon;
  P.weapon = null;
  if (h.f.type === 'knife') h.f.type = 'brawler';
  t.weapon = w;
  t.armed = false; // it is in his hand now; bringing it out is still the held input
  sub(`The ${w} is out of his hand and in Tom's coat.`, '', 'over', 3);
  said('disarm', { who: P.id, weapon: w });
  letGo('disarmed');
  return true;
}

// ---------- a man in the water (A11, ER-WATER-02): out within a minute, soaked, alive ----------
function intoWater(P, x, z) {
  P.fight = null;
  P.hold = true;
  P.moving = false;
  P.inWater = true;
  P.react = null;
  const from = { x: P.x, z: P.z };
  R.wet.push({ P, t: FX.water.climbsOutAfterRealSeconds, from });
  P.x = x;
  P.z = z;
  act('put_in_water', { target: P.anon ? undefined : P.id, name: tomName(P), noiseR: 14 });
  sub(`${tomName(P)} goes over the edge and into the water.`, '', 'over', 3.5);
  if (G.hooks.sfx) G.hooks.sfx('crash');
  said('water', { who: P.id });
}
function stepWet(dt) {
  for (let i = R.wet.length - 1; i >= 0; i--) {
    const w = R.wet[i],
      P = w.P;
    w.t -= dt;
    if (w.t > 0) continue;
    R.wet.splice(i, 1);
    // he climbs out at the nearest ladder: the dry ground he left
    P.x = w.from.x;
    P.z = w.from.z;
    P.inWater = false;
    P.soaked = G.t;
    P.hold = false;
    P.hurry = LAD.fleeHurryTimes;
    P.override = { where: P.def.sched ? 'home' : 'off', act: 'sleep', until: G.t + LAD.fleeStaysAwayGameMinutes };
    P.goalKey = '';
    P.mind.fear = clamp(P.mind.fear + 0.2, 0, 1);
    bubble(P, 'Soaked and spitting, he hauls himself out.', 3);
    said('out of the water', { who: P.id, alive: !P.dead });
    emit('water:out', { P });
  }
}

// ---------- the quiet blow (A23): from behind, on a man who has not seen him ----------
export function quietBlow() {
  const t = G.tom;
  if (F.on || t.inCar) return false;
  let P = null,
    bd = FX.quiet.reachMetres;
  for (const Q of G.named.concat(G.crowd)) {
    if (Q.gone || Q.down || Q.dead || Q.space !== t.space) continue;
    const d = hyp(Q.x, Q.z, t.x, t.z);
    if (d >= bd) continue;
    if (Math.abs(angDiff(t.ang, Math.atan2(Q.x - t.x, Q.z - t.z))) > 1.0) continue; // he must be facing the man
    P = Q;
    bd = d;
  }
  if (!P) return false;
  // from behind: Tom is outside what the man faces, and the man has not seen him
  const behind = Math.abs(angDiff(P.ang, Math.atan2(t.x - P.x, t.z - P.z))) > Math.PI - FX.quiet.behindHalfAngleRadians,
    seesHim = sense(P, tomTarget()).see;
  if (!behind || seesHim) return false; // face to face it is the ladder's business [Q], not this
  const def = P.def || {};
  if (def.sex === 'f' || (def.age || 0) >= 60 || def.priest || def.police) return false; // Tom's own line (QUESTIONS 2, recommended)
  const cosh = t.weapon === 'cosh',
    secs = cosh ? FX.quiet.coshOutRealSeconds : FX.quiet.fistOutRealSeconds;
  P.down = true;
  P.hurt = 1;
  P.fight = null;
  P.moving = false;
  P.route = null;
  P.downT = G.t + (secs * 60) / RULES.time.realSecondsPerGameHour; // real seconds on the playing clock
  // a strike with the seven slots like any other: whoever sees or hears it has it; the man himself caught a shape at most
  const E = act('quiet_blow', { name: tomName(P), victim: P.id, weapon: cosh ? 'cosh' : 'fists', noiseR: FX.quiet.noiseMetres });
  remember(P, E, { src: 'heard', who: 'man', sure: FX.quiet.shapeSure, heat: 0.8 });
  if (G.hooks.sfx) G.hooks.sfx('thud');
  said('quiet blow', { who: P.id, cosh, secs, e: E.id, seenBy: E.wit.length });
  emit('fight:end', { how: 'down', foes: [P], tier: cosh ? FX.tiers.carried : FX.tiers.fists, seconds: 0, weapon: cosh ? 'cosh' : null, quiet: true, types: [] });
  return true;
}

// ---------- a man down can be searched (A29, A4's time) ----------
function downNear() {
  const t = G.tom;
  if (F.on || t.inCar) return null;
  for (const Q of G.named.concat(G.crowd)) if (Q.down && !Q.gone && Q.space === t.space && !Q.searched && hyp(Q.x, Q.z, t.x, t.z) < 1.6) return Q;
  return null;
}
function search(P) {
  P.searched = true;
  const found = [];
  if (P.weapon) {
    found.push('a ' + P.weapon);
    if (!G.tom.weapon) G.tom.weapon = P.weapon;
    P.weapon = null;
  }
  const E = act('searched_man', { target: P.anon ? undefined : P.id, name: tomName(P) });
  sub(found.length ? `In his pockets: ${found.join(', ')}.` : 'Nothing on him worth the taking.', '', 'over', 3.5);
  emit('searched', { P, E, found }); // the jobs builder may add what he carried
  said('searched', { who: P.id, found });
}

register({
  id: 'fightx',
  fresh: () => ({ lastMix: '', mixNow: '', fights: 0, ends: {} }),
  loaded(x) {
    if (!x.ends) x.ends = {};
    G.hooks.fighterTypes = types;
    G.hooks.holdMan = holdMan;
    G.hooks.intoWater = intoWater;
    // the police arriving, or anybody else with cause, may stop a fight: G.hooks.fightBrokenUp('police')
    G.hooks.fightBrokenUp = (why = 'police') => {
      if (!F.on) return false;
      fightEnd(false, why);
      return true;
    };
    R.hold = null;
    R.wet.length = 0;
    R.held = 0;
  },
  step(dt) {
    const t = G.tom;
    R.holdCool = Math.max(0, R.holdCool - dt);
    stepWet(dt);
    // the weapon on a held input (ER-FIGHT-08)
    if (keys.Semicolon && !t.inCar && t.weapon && !t.armed) {
      R.held += dt;
      if (R.held >= FX.weapon.heldToDrawRealSeconds) {
        R.held = 0;
        if (F.on && F.rung >= LAD.strikeRung) drawHeld();
        else if (!F.on) {
          t.armed = true;
          act('weapon_drawn', { weapon: t.weapon, noiseR: 2 });
          sub(`The ${t.weapon} is out. It cannot go back unseen by anyone who is looking.`, '', 'over', 3.5);
        }
        said('weapon out', { weapon: t.weapon, inFight: F.on });
      }
    } else R.held = 0;
    if (R.hold) {
      const h = R.hold;
      h.t -= dt;
      if (h.t <= 0 || h.f.st !== 'held' || !F.on) letGo('time');
      else if (h.f.P.fight) h.f.P.fight.mode = 'stagger';
    }
    // out of breath: he is heard (no bar)
    if (F.on && F.stam < FX.defend.breathHeardBelowStamina) {
      R.breath = (R.breath || 0) - dt;
      if (R.breath <= 0) {
        R.breath = FX.defend.breathHeardAtMostEveryRealSeconds;
        if (G.hooks.sfx) G.hooks.sfx('breath');
        said('breath', { stam: F.stam });
      }
    }
    // people step in to a long fist fight
    if (F.on && F.rung >= LAD.strikeRung && !t.armed && F.clock > FX.ends.stepInAfterRealSeconds && live().length && !live().some((f) => f.P.weapon)) {
      const near = G.named.filter((P) => !P.gone && !P.down && !P.fight && P.space === t.space && !P.lad && (P.def.age || 40) < 60 && P.def.sex !== 'f' && hyp(P.x, P.z, t.x, t.z) < FX.ends.stepInWithinMetres);
      if (near.length >= FX.ends.stepInWatchersAtLeast) {
        sub("Two men get between them. \"That'll do. Both of you.\"", tomName(near[0]), 'face', 4);
        const E = mkEvent('stepped_in', {});
        for (const P of near.slice(0, 3)) remember(P, E, { src: 'self', who: 'tom', sure: 1, heat: 0.4 });
        fightEnd(false, 'stepped in');
      }
    }
    // a search of a man down: the use key held (ER-SEARCH-02: no test of reflexes)
    const P = downNear();
    if (P && keys.KeyE) {
      if (R.searchP !== P) {
        R.searchP = P;
        R.searchT = 0;
      }
      R.searchT += dt;
      if (R.searchT >= 4) search(P);
    } else R.searchP = null;
  },
  hotspots(out) {
    const P = downNear();
    if (P && !out.some((o) => o.k === 'E')) out.push({ k: 'E', t: 'Hold to go through his pockets', run: () => {} });
  },
  key(code) {
    if (R.hold) {
      if (code === 'KeyJ') return push(), true;
      if (code === 'KeyG') return disarm(), true;
      if (code === 'KeyX') return letGo('let go'), true;
    }
    if (code === 'KeyJ' && !F.on) return quietBlow();
    return false;
  },
  hook: {
    log: () => R.log.slice(),
    types: () => F.foes.map((f) => f.type || null),
    mix: () => ({ last: G.x.fightx.lastMix, now: G.x.fightx.mixNow }),
    drawHeld, // what the held [;] does in a fight
    holdMan,
    holding: () => (R.hold ? R.hold.f.P.id : null),
    push: () => (R.hold ? push() : null),
    disarm: () => (R.hold ? disarm() : null),
    letGo: () => letGo('test'),
    quietBlow,
    lastEnd: () => F.lastEnd || null,
    counterOpen: () => F.clock < (F.counterUntil || 0),
    wet: () => R.wet.map((w) => ({ who: w.P.id, left: w.t })),
    brokenUp: (why) => G.hooks.fightBrokenUp(why),
  },
});
on('fight:end', (e) => {
  const x = G.x.fightx;
  if (!x || !e || e.quiet) return;
  x.fights++;
  x.ends[e.how] = (x.ends[e.how] || 0) + 1;
  if (x.mixNow) x.lastMix = x.mixNow;
  R.hold = null;
});
