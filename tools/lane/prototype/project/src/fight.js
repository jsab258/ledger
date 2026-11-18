// The street's way: an escalation ladder Tom can stop on at any rung. Most of it ends before a blow.
// stare, square up, threaten, shove, strike, weapon out, weapon used, kill.
import { G } from './state.js';
import { hyp, clamp, chance, rnd, angDiff, pick } from './util.js';
import { act, logLine } from './events.js';
import { menaceTo } from './gossip.js';
import { meet } from './ledger.js';
import { blocked } from './map.js';
import { sub, bubble, show, $, tomName } from './ui.js';
import { S } from './render/sync.js';

export const F = {
  on: false,
  T: null,
  rung: 0,
  foes: [],
  st: 'idle',
  t: 0,
  stam: 1,
  cool: 0,
  demand: null,
  struck: false,
  usedW: false,
  open: 0,
};
const RUNGS = ['', 'Stare', 'Square up', 'Threaten', 'Shove', 'Strike', 'Weapon out'];
const KIND = ['', 'stare', 'squareup', 'threat', 'shove'];
const WDMG = {
  cosh: 1.7,
  'flick knife': 2.1,
  brick: 1.6,
  chair: 1.5,
  'wheel brace': 1.8,
  'cargo hook': 1.9,
  'dustbin lid': 1.1,
};
const YIELD = [
  [],
  ['Looks away.'],
  ['All right. All right.', 'No need for that.'],
  ["Don't. I'm saying nothing, me.", "All right! You've made your point."],
  ['Get off! All right!'],
];
const STAND = [
  [],
  ['What you looking at?', 'Seen enough?'],
  ['Come on, then.', "You don't want to do that."],
  ["You'll have to do better than that.", "I've been threatened by better."],
  ["Right. You've done it now."],
];
// Tom will not lay hands on women, on anyone of sixty or over, or on the priest. The ladder stops at a threat for them.
const soft = (P) => P.def.sex === 'f' || P.def.frail || (P.def.age || 30) >= 60 || P.id === 'walsh';

export function target() {
  // whoever is in front of Tom, close
  const t = G.tom;
  let best = null,
    bd = 3.6;
  for (const P of G.named.concat(G.crowd)) {
    if (P.gone || P.dead || P.down || P.inCar || P.space !== t.space || P.space === 'home') continue;
    let d = hyp(P.x, P.z, t.x, t.z);
    if (d > 3.6) continue;
    if (Math.abs(angDiff(t.ang, Math.atan2(P.x - t.x, P.z - t.z))) > 1.2) continue;
    d -= (P.anon ? 0 : 1.2) + (P.mark ? 1 : 0);
    if (d > bd) continue;
    bd = d;
    best = P;
  } // named people, and anyone with something to say, come first
  return best;
}
function allies(P) {
  const out = [];
  for (const Q of G.crowd.concat(G.named)) {
    if (Q === P || Q.gone || Q.down || Q.dead || Q.space !== P.space) continue;
    if (hyp(Q.x, Q.z, P.x, P.z) > 9) continue;
    if ((P.lad && Q.lad) || (P.id === 'dennis' && Q.yardLad) || (Q.id === 'dennis' && P.yardLad)) out.push(Q);
  }
  return out;
}
export function frontUp(P, demand) {
  if (F.on && F.T === P) return;
  if (F.on) end();
  F.on = true;
  F.T = P;
  F.rung = 0;
  F.proxy = false;
  F.settled = false;
  F.foes = [];
  F.demand = demand || (G.hooks.demandFor ? G.hooks.demandFor(P) : null);
  F.struck = false;
  F.usedW = false;
  P.hold = true;
  P.route = null;
  P.moving = false;
  meet(P);
  climb();
}
function mood(P, m) {
  P.react = m;
  P.reactT = 2.5;
}
export function climb() {
  if (!F.on) return;
  const P = F.T,
    t = G.tom,
    m = P.mind,
    d = P.def;
  if (F.rung >= 5) {
    if (F.rung === 5 && t.weapon && !t.armed) drawWeapon();
    return;
  }
  const next = F.rung + 1;
  if (next >= 4 && soft(P)) {
    const al = allies(P).filter((q) => !soft(q));
    if (!al.length) {
      sub('No. Not ' + (d.sex === 'f' ? 'her' : 'him') + '. Not with your hands.', '', 'over', 3);
      return;
    }
    F.rung = 5;
    G.stats.fights++;
    sub("Right. You've done it now.", tomName(al[0]));
    F.proxy = true;
    startFight(al[0], true);
    ladderUI();
    return; // his minder steps in; the old man is never touched
  }
  F.rung = next;
  G.stats.fights += next === 5 ? 1 : 0;
  P.ang = Math.atan2(t.x - P.x, t.z - P.z);
  if (next === 5) {
    startFight(P, true);
    ladderUI();
    return;
  }
  S.tomAnim.mode = ['stand', 'stare', 'square', 'point', 'shove'][next];
  F.animT = next === 4 ? 0.5 : 0;
  act(KIND[next], { target: P.id, noiseR: next >= 3 ? 14 : 0 });
  if (next >= 3 && G.hooks.sfx) G.hooks.sfx('shout');
  if (d.police && next >= 4) {
    G.story.flags.assaultPolice = 1;
    sub('That is assault on a police officer.', tomName(P), 'face');
    if (G.hooks.arrestNow) G.hooks.arrestNow(P);
    end();
    return;
  }
  const al = allies(P),
    pressure =
      [0, 0.18, 0.32, 0.5, 0.66][next] + menaceTo(P) + (t.armed ? 0.3 : 0) - al.length * 0.16 - t.hurt * 0.25;
  if (next === 4) {
    const dx = P.x - t.x,
      dz = P.z - t.z,
      l = Math.hypot(dx, dz) || 1;
    const nx = P.x + (dx / l) * 1.2,
      nz = P.z + (dz / l) * 1.2;
    if (!blocked(nx, nz)) {
      P.x = nx;
      P.z = nz;
    }
  }
  if (pressure > (d.nerve ?? 0.5) + (P.lad ? 0.12 : 0)) {
    m.fear = clamp(m.fear + 0.14 * next, 0, 1);
    m.regard = clamp(m.regard - 0.1 * next, -1, 1);
    mood(P, next >= 3 ? 'cower' : 'stand');
    const line = pick(YIELD[next]);
    if (next > 1) sub(line, tomName(P));
    else bubble(P, line);
    F.yielded = true;
    if (F.demand && next >= 2 && G.hooks.yielded) G.hooks.yielded(P, F.demand, next);
  } else {
    F.yielded = false;
    mood(P, next >= 2 ? 'square' : 'stare');
    sub(pick(STAND[next]), tomName(P));
    if (next === 4 || (next === 3 && (d.nerve ?? 0.5) > 0.7 && (P.lad || P.yardLad) && chance(0.6))) {
      startFight(P, false);
    }
  }
  ladderUI();
}
export function backDown() {
  if (!F.on) return;
  if (F.foes.some((f) => f.st !== 'down' && f.st !== 'flee') && F.rung >= 5) {
    sub('You step off. They may not let you.', '', 'over', 2.5);
    F.rung = 4;
  }
  end(F.foes.some((f) => f.st !== 'down' && f.st !== 'flee'));
}
function drawWeapon() {
  const t = G.tom;
  if (!t.weapon) return;
  t.armed = true;
  F.rung = 6;
  act('weapon_out', { target: F.T.id, weapon: t.weapon, noiseR: 10 });
  for (const f of F.foes) {
    if (f.st === 'down') continue;
    if (0.55 + menaceTo(f.P) > (f.P.def.nerve ?? 0.5) + 0.25) {
      f.st = 'flee';
      flee(f.P);
      sub("He's got a " + t.weapon + '!', tomName(f.P));
    }
  }
  ladderUI();
}
function flee(P) {
  P.fight = null;
  P.hold = false;
  P.hurry = 2.6;
  P.override = { where: P.def.sched ? 'home' : 'off', act: 'sleep', until: G.t + 300 };
  P.goalKey = '';
  P.mind.fear = clamp(P.mind.fear + 0.3, 0, 1);
}
function startFight(P, tomFirst) {
  F.rung = Math.max(F.rung, 5);
  S.tomAnim.mode = 'guard';
  F.st = 'idle';
  F.t = 0;
  const add = (Q) => {
    if (F.foes.find((f) => f.P === Q) || soft(Q)) return;
    Q.hold = true;
    Q.route = null;
    Q.moving = false;
    Q.fight = { mode: 'guard' };
    F.foes.push({ P: Q, st: 'guard', t: rnd(0.4, 1.2), cd: rnd(0.6, 1.6) });
  };
  add(P);
  for (const Q of allies(P)) add(Q);
  if (F.T && F.T !== P) for (const Q of allies(F.T)) add(Q);
  if (!tomFirst) {
    act('set_on', {
      target: P.id,
      noiseR: 24,
      name: F.foes.length > 1 ? P.def.name + ' and ' + (F.foes.length - 1) + ' more' : P.def.name,
    });
  }
  if (G.hooks.sfx) G.hooks.sfx('thud');
}
// Others can start on Tom (Cammack's lads, late on).
export function setOn(list) {
  if (F.on) return;
  F.on = true;
  F.settled = false;
  F.proxy = false;
  F.T = list[0];
  F.rung = 4;
  F.demand = null;
  F.struck = false;
  F.usedW = false;
  F.foes = [];
  startFight(list[0], false);
  for (const Q of list.slice(1)) {
    Q.hold = true;
    Q.route = null;
    Q.fight = { mode: 'guard' };
    if (!F.foes.find((f) => f.P === Q)) F.foes.push({ P: Q, st: 'guard', t: rnd(0.8, 1.6), cd: rnd(1, 2) });
  }
  ladderUI();
}
export function input(kind) {
  if (!F.on || F.rung < 5) return;
  const t = G.tom;
  if (kind === 'finish') return finish();
  if (F.st !== 'idle' && F.st !== 'block') return;
  if (kind === 'light' || kind === 'heavy') {
    if (F.stam < 0.15) {
      if (G.hooks.sfx) G.hooks.sfx('tick');
      return;
    }
    F.st = kind === 'heavy' ? 'heavyUp' : 'windup';
    F.t = kind === 'heavy' ? 0.55 : 0.2;
    F.heavy = kind === 'heavy';
    F.stam -= kind === 'heavy' ? 0.28 : 0.15;
  } else if (kind === 'dodge') {
    if (F.cool > 0) return;
    const bx = t.x - Math.sin(t.ang) * 1.6,
      bz = t.z - Math.cos(t.ang) * 1.6;
    if (!blocked(bx, bz)) {
      t.x = bx;
      t.z = bz;
    }
    F.st = 'dodge';
    F.t = 0.3;
    F.cool = 0.9;
  }
}
export function block(on) {
  if (!F.on || F.rung < 5) return;
  if (on && F.st === 'idle') F.st = 'block';
  else if (!on && F.st === 'block') F.st = 'idle';
}
function hurtFoe(f, dmg, heavy) {
  const P = f.P,
    t = G.tom;
  P.hurt = clamp((P.hurt || 0) + dmg, 0, 1.2);
  if (heavy || f.st !== 'windup') {
    f.st = 'stagger';
    f.t = heavy ? 0.7 : 0.28;
    P.fight.mode = 'stagger';
  } // a light one does not stop a man already swinging
  if (!F.struck) {
    F.struck = true;
    act('strike', { target: P.anon ? undefined : P.id, name: P.def.name, noiseR: 26 });
  }
  if (t.armed && !F.usedW) {
    F.usedW = true;
    act('weapon_used', { target: P.id, weapon: t.weapon, noiseR: 26 });
  }
  P.mind.fear = clamp(P.mind.fear + 0.12, 0, 1);
  P.mind.regard = clamp(P.mind.regard - 0.25, -1, 1);
  if (G.hooks.sfx) G.hooks.sfx('hit');
  if (G.hooks.blood && (t.armed || heavy)) G.hooks.blood(P.x, P.z);
  const dx = P.x - t.x,
    dz = P.z - t.z,
    l = Math.hypot(dx, dz) || 1,
    nx = P.x + (dx / l) * 0.45,
    nz = P.z + (dz / l) * 0.45;
  if (!blocked(nx, nz)) {
    P.x = nx;
    P.z = nz;
  }
  if (!f.hitOnce && P.hurt < 1) {
    f.hitOnce = 1;
    if ((P.def.nerve ?? 0.5) < 0.4 && chance(0.6)) {
      f.st = 'flee';
      flee(P);
      sub('All right! All right!', tomName(P));
      return;
    }
  }
  if (P.hurt >= 1) {
    f.st = 'down';
    P.down = true;
    P.fight = null;
    sub("He's down.", '', 'over', 2);
    for (const g of F.foes)
      if (g !== f && g.st !== 'down' && (g.P.def.nerve ?? 0.5) < 0.85 && chance(0.6)) {
        g.st = 'flee';
        flee(g.P);
      }
  }
}
function finish() {
  const t = G.tom,
    f = F.foes.find((x) => x.st === 'down' && hyp(x.P.x, x.P.z, t.x, t.z) < 2);
  if (!f || !t.armed) return;
  const P = f.P;
  P.dead = true;
  P.down = true;
  G.story.flags.dead = G.story.flags.dead || {};
  G.story.flags.dead[P.id] = Math.round(G.t);
  act('kill', { target: P.anon ? undefined : P.id, name: P.def.name, weapon: t.weapon, noiseR: 20 });
  logLine('Tom killed ' + P.def.name, 'kill');
  if (G.hooks.blood) for (let i = 0; i < 5; i++) G.hooks.blood(P.x + rnd(-0.5, 0.5), P.z + rnd(-0.5, 0.5));
  if (G.hooks.killed) G.hooks.killed(P);
}
export function step(dt) {
  const t = G.tom;
  if (!F.on) {
    if (S.tomAnim.mode !== 'stand' && !G.tom.sit) S.tomAnim.mode = 'stand';
    return;
  }
  for (const P of G.named.concat(G.crowd))
    if (P.reactT) {
      P.reactT -= dt;
      if (P.reactT <= 0) {
        P.reactT = 0;
        P.react = null;
      }
    }
  const T = F.T,
    dT = hyp(T.x, T.z, t.x, t.z);
  if (F.rung < 5) {
    if (F.animT > 0) {
      F.animT -= dt;
      if (F.animT <= 0) S.tomAnim.mode = 'square';
    }
    if (dT > 7 || T.gone) end();
    return;
  }
  F.stam = clamp(F.stam + dt * (F.st === 'block' ? -0.05 : 0.13), 0, 1);
  G.tom.puff = Math.max(G.tom.puff || 0, 1 - F.stam);
  F.cool -= dt;
  F.open = Math.max(0, F.open - dt);
  const live = F.foes.filter((f) => f.st !== 'down' && f.st !== 'flee');
  // face the nearest standing foe
  let near = null,
    nd = 1e9;
  for (const f of live) {
    const d = hyp(f.P.x, f.P.z, t.x, t.z);
    if (d < nd) {
      nd = d;
      near = f;
    }
  }
  if (near && nd < 5 && F.st !== 'dodge')
    t.ang += clamp(angDiff(t.ang, Math.atan2(near.P.x - t.x, near.P.z - t.z)), -9 * dt, 9 * dt);
  // Tom's swing
  if (F.st === 'windup' || F.st === 'heavyUp') {
    S.tomAnim.mode = F.heavy ? 'heavy' : 'windup';
    F.t -= dt;
    if (F.t <= 0) {
      F.st = 'strike';
      F.t = 0.16;
      S.tomAnim.mode = 'strike';
      const hit =
        near && nd < 1.75 && Math.abs(angDiff(t.ang, Math.atan2(near.P.x - t.x, near.P.z - t.z))) < 0.9;
      if (hit && !(near.st === 'guard' && chance(F.heavy ? 0.15 : 0.36))) {
        hurtFoe(
          near,
          (F.heavy ? 0.3 : 0.15) * (t.armed ? WDMG[t.weapon] || 1.5 : 1) * (1 - t.hurt * 0.3),
          F.heavy,
        );
        F.rec = F.heavy ? 0.45 : 0.28;
      } else {
        F.rec = F.heavy ? 0.95 : 0.6;
        F.open = F.rec;
        if (hit && G.hooks.sfx) G.hooks.sfx('block');
      } // a miss leaves you open
    }
  } else if (F.st === 'strike') {
    F.t -= dt;
    if (F.t <= 0) {
      F.st = 'recover';
      F.t = F.rec;
      S.tomAnim.mode = 'guard';
    }
  } else if (F.st === 'recover' || F.st === 'dodge' || F.st === 'stagger') {
    F.t -= dt;
    if (F.st === 'stagger') S.tomAnim.mode = 'stagger';
    if (F.t <= 0) {
      F.st = 'idle';
      S.tomAnim.mode = 'guard';
    }
  } else if (F.st === 'block') S.tomAnim.mode = 'block';
  else S.tomAnim.mode = 'guard';
  // them
  let k = 0;
  for (const f of live) {
    const P = f.P;
    if (f.st === 'flee' || f.st === 'down' || !P.fight) continue;
    const d = hyp(P.x, P.z, t.x, t.z),
      a = Math.atan2(t.x - P.x, t.z - P.z);
    P.ang += clamp(angDiff(P.ang, a), -7 * dt, 7 * dt);
    f.t -= dt;
    k++;
    if (f.st === 'stagger') {
      if (f.t <= 0) {
        f.st = 'guard';
        f.t = rnd(0.15, 0.55);
        P.fight.mode = 'guard';
        if ((P.hurt || 0) > 0.75 && (P.def.nerve ?? 0.5) < 0.9 && chance(0.5)) {
          f.st = 'flee';
          flee(P);
        }
      }
      continue;
    }
    if (d > 1.5) {
      const sp = 2.4 * dt,
        off = k * 0.9 - 0.9,
        tx = t.x + Math.sin(a + Math.PI + off) * 1.25,
        tz = t.z + Math.cos(a + Math.PI + off) * 1.25,
        l = Math.hypot(tx - P.x, tz - P.z) || 1;
      const ux = (tx - P.x) / l,
        uz = (tz - P.z) / l;
      for (const [vx, vz] of [
        [ux, uz],
        [ux * 0.5 - uz * 0.87, uz * 0.5 + ux * 0.87],
        [ux * 0.5 + uz * 0.87, uz * 0.5 - ux * 0.87],
        [-uz, ux],
        [uz, -ux],
      ]) {
        const nx = P.x + vx * sp,
          nz = P.z + vz * sp;
        if (!blocked(nx, nz, 0.3)) {
          P.x = nx;
          P.z = nz;
          break;
        }
      }
      P.moving = true;
      P.v = 2.4;
      if (f.st !== 'guard') {
        f.st = 'guard';
        P.fight.mode = 'guard';
      }
      continue;
    }
    P.moving = false;
    if (f.st === 'guard' && f.t <= 0) {
      f.st = 'windup';
      f.heavy = chance(0.3);
      f.t = f.heavy ? 0.75 : 0.5;
      P.fight.mode = f.heavy ? 'heavy' : 'windup';
    } // a readable wind-up
    else if (f.st === 'windup' && f.t <= 0) {
      f.st = 'strike';
      f.t = 0.18;
      P.fight.mode = 'strike';
      if (d < 1.9 && F.st !== 'dodge') {
        let dmg = (f.heavy ? 0.23 : 0.125) * (P.weapon ? 1.7 : 1) * (1 - (P.hurt || 0) * 0.3);
        const facing = Math.abs(angDiff(t.ang, Math.atan2(P.x - t.x, P.z - t.z))) < 1.1;
        if (F.st === 'block' && facing) {
          dmg *= t.weapon === 'dustbin lid' && t.armed ? 0.03 : 0.15;
          F.stam -= 0.12;
          if (G.hooks.sfx) G.hooks.sfx('block');
        } else {
          if (F.open > 0) dmg *= 1.5;
          F.st = 'stagger';
          F.t = 0.32;
          if (G.hooks.sfx) G.hooks.sfx('hit');
          if (G.hooks.shake) G.hooks.shake(0.25);
        }
        t.hurt = clamp(t.hurt + dmg, 0, 1.05);
        t.noiseP = 24;
      }
    } else if (f.st === 'strike' && f.t <= 0) {
      f.st = 'guard';
      f.t = rnd(0.7, 1.6) + (live.length > 1 ? 0.5 : 0);
      P.fight.mode = 'guard';
    }
  }
  if (t.hurt >= 1) {
    act('beaten', { noiseR: 20 });
    const foes = F.foes.map((f) => f.P);
    end(true);
    if (G.hooks.beaten) G.hooks.beaten(foes);
    return;
  }
  if (!live.length) {
    const any = F.foes.some((f) => f.st === 'down');
    if (F.demand && !F.settled && F.struck && G.hooks.yielded) {
      F.settled = true;
      if (!F.T.down) {
        F.T.mind.fear = clamp(F.T.mind.fear + 0.5, 0, 1);
        F.T.react = 'cower';
        F.T.reactT = 4;
      }
      G.hooks.yielded(F.T, F.demand, 5);
    }
    ladderUI(any && t.armed);
    if (!any || nd > 6 || !t.armed) {
      F.endT = (F.endT || 0) + dt;
      if (F.endT > (any && t.armed ? 6 : 1.2)) end();
    }
  } else if (nd > 16) end(true);
}
export function end(hostile) {
  for (const f of F.foes) {
    const P = f.P;
    P.fight = null;
    P.hold = false;
    P.moving = false;
    if (P.down && !P.dead) {
      P.downT = G.t + 25;
    } else if (!P.dead) {
      P.mind.fear = clamp(P.mind.fear + 0.2, 0, 1);
      if (!hostile || f.st === 'flee') {
        P.goalKey = '';
      }
    }
  }
  if (F.T && !F.T.down) {
    F.T.hold = false;
    F.T.goalKey = '';
  }
  F.on = false;
  F.proxy = false;
  F.foes = [];
  F.rung = 0;
  F.endT = 0;
  F.st = 'idle';
  G.tom.armed = false;
  S.tomAnim.mode = 'stand';
  show('ladder', false);
  if (G.hooks.fightOver) G.hooks.fightOver();
}
// People put down get up after a while and go home sore.
export function recover() {
  for (const P of G.named.concat(G.crowd)) {
    if (P.down && !P.dead && P.downT && G.t > P.downT) {
      P.down = false;
      P.downT = 0;
      P.hurt = 0.7;
      P.hurry = 0.7;
      P.override = { where: P.def.sched ? 'home' : 'off', act: 'sleep', until: G.t + 600 };
      P.goalKey = '';
    }
    if (P.hurt > 0 && !P.down) P.hurt = Math.max(0, P.hurt - 0.00002);
  }
}
function ladderUI(canFinish) {
  const el = $('ladder');
  show('ladder', true);
  const t = G.tom;
  el.innerHTML =
    `<div class="h">${F.rung >= 5 ? 'IT HAS COME TO BLOWS' : 'FRONTING UP'}: ${tomName(F.T)}</div>` +
    RUNGS.slice(1)
      .map(
        (r, i) =>
          `<div class="r ${i + 1 === F.rung ? 'on' : i + 1 < F.rung ? 'done' : ''}">${i + 1}. ${r}${i === 5 ? (t.weapon ? ' (' + t.weapon + ')' : ' (none carried)') : ''}</div>`,
      )
      .join('') +
    `<div class="k">${F.rung < 5 ? '[R] step up  ·  [X] walk away' : '[LMB/J] hit, hold for heavy · [RMB/K] block · [Space] step back · [X] break off' + (t.weapon && !t.armed ? ' · [R] weapon out' : '') + (canFinish ? '<br><b>[V] use it on a man who is down. This cannot be undone.</b>' : '')}</div>`;
}
