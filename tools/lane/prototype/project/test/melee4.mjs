// The lane's round 4 (18 Nov): a debt that can come to blows (face and corners) and things to hand (melee part 2).
// Face: a man fronted up with folk watching will not back down where he would alone. Corner: a man shoved against
// a wall with nowhere to go comes off it swinging. Grab: G in a fight snatches up a thing to hand. Breakage (drill M7,
// melee sheet C12): a chair 1 to 3 blows, a brick 2 to 5, a wheel brace (like the sheet's pipe) never in 25.
import fs from 'fs';
import { launch } from './harness.mjs';

let bad = 0;
const ok = (cond, what) => {
  console.log((cond ? 'ok   ' : 'FAIL ') + what);
  if (!cond) bad++;
};
const OUT = process.env.MELEE4_OUT || 'melee4-drills.jsonl';
const h = await launch({ port: 8798, quality: 'low' });
const runs = {};
// one man (crowd, not a lad, under sixty) at d metres in front of Tom; everyone else sent out of the street
// except `watchers` men put round him at 6 m. Returns his id.
const stage = (o) =>
  h.ev((o) => {
    const G = LEDGER.G, t = G.tom;
    if (LEDGER.F.on) LEDGER.fight.end();
    const all = G.named.concat(G.crowd);
    window.__spaces = window.__spaces || new Map();
    for (const Q of all) if (!window.__spaces.has(Q)) window.__spaces.set(Q, Q.space);
    for (const Q of all) Q.space = 'elsewhere';
    const men = G.crowd.filter((p) => !p.gone && !p.dead && !p.inCar && !p.lad && !p.yardLad && p.def.sex !== 'f' && (p.def.age || 30) < 60);
    const P = men[0];
    t.x = o.x ?? t.x; t.z = o.z ?? t.z; t.ang = o.ang ?? t.ang; t.space = 'street'; t.hurt = 0; t.weapon = null; t.armed = false;
    P.space = 'street'; P.down = false; P.hurt = 0; P.mind.fear = 0; P.mind.mem = []; // nothing known of Tom: no menace
    P.x = t.x + Math.sin(t.ang) * (o.d || 1.2); P.z = t.z + Math.cos(t.ang) * (o.d || 1.2);
    P.def.nerve = o.nerve;
    for (let i = 0; i < (o.watchers || 0); i++) {
      const Q = men[i + 1];
      if (!Q) break;
      const a = (i / Math.max(1, o.watchers)) * Math.PI * 2;
      Q.space = 'street'; Q.x = P.x + Math.sin(a) * 6; Q.z = P.z + Math.cos(a) * 6; Q.down = false;
    }
    return { id: P.def.name, face: LEDGER.fight.faceOf(P, []) };
  }, o);
const restore = () => h.ev(() => { if (LEDGER.F.on) LEDGER.fight.end(); for (const [Q, s] of window.__spaces || []) Q.space = s; window.__spaces = null; });
// climb the ladder from a stare to a shove; report where it stopped
const ladder = () =>
  h.ev(() => {
    const G = LEDGER.G, t = G.tom, F = LEDGER.F;
    const P = G.crowd.find((p) => p.space === 'street' && Math.hypot(p.x - t.x - Math.sin(t.ang) * 1.2, p.z - t.z - Math.cos(t.ang) * 1.2) < 0.05) ||
      G.crowd.filter((p) => p.space === 'street').sort((a, b) => Math.hypot(a.x - t.x, a.z - t.z) - Math.hypot(b.x - t.x, b.z - t.z))[0];
    LEDGER.fight.frontUp(P, null);
    for (let i = 0; i < 4 && F.on && F.rung < 4 && !F.yielded; i++) LEDGER.fight.climb();
    return { rung: F.rung, yielded: !!F.yielded, fight: F.on && F.rung >= 5, why: F.standWhy || '', face: F.face, last: F.last, foes: F.foes.length };
  });
const tick = (secs, fn) =>
  h.ev(([secs, fn]) => {
    const f = fn ? eval(fn) : null;
    for (let i = 0; i < Math.round(secs * 60); i++) {
      if (f) f(LEDGER.F.clock);
      if (!LEDGER.F.on) break;
      LEDGER.tick(1 / 60);
    }
    return LEDGER.F.tele.slice();
  }, [secs, fn]);
// a still man in front of Tom, Tom standing just by a thing to hand, fight on
const fightBy = (prop) =>
  h.ev((prop) => {
    const G = LEDGER.G, t = G.tom, F = LEDGER.F, isBlocked = LEDGER.isBlocked;
    if (F.on) LEDGER.fight.end();
    const p = LEDGER.fight.handProps().find((q) => q.hand === prop && !q.broken);
    if (!p) return { error: 'no ' + prop + ' on the map' };
    // a free spot just beside it, and a free spot 1 m on for the man
    for (let k = 0; k < 16; k++) {
      const a = (k / 16) * Math.PI * 2, x = p.x + Math.sin(a) * (p.r + 0.5), z = p.z + Math.cos(a) * (p.r + 0.5);
      const mx = x + Math.sin(a) * 1.0, mz = z + Math.cos(a) * 1.0;
      if (isBlocked(x, z) || isBlocked(mx, mz) || isBlocked(mx + Math.sin(a) * 0.6, mz + Math.cos(a) * 0.6)) continue;
      t.x = x; t.z = z; t.ang = a; t.space = 'street'; t.hurt = 0; t.weapon = null; t.armed = false;
      const P = G.crowd.find((q) => !q.gone && !q.dead && !q.inCar && q.def.sex !== 'f' && (q.def.age || 30) < 60);
      P.space = 'street'; P.x = mx; P.z = mz; P.hurt = 0; P.down = false; P.def.nerve = 0.95;
      LEDGER.fight.setOn([P]);
      F.tele = []; F.stam = 1;
      for (const f of F.foes) f.st = 'still';
      return { at: [x, z], prop: p.hand };
    }
    return { error: 'no free spot by the ' + prop };
  }, prop);
const endFight = () => h.ev(() => { LEDGER.F.tele = null; if (LEDGER.F.on) LEDGER.fight.end(); for (const P of LEDGER.G.crowd) { P.down = false; P.hurt = 0; } LEDGER.G.tom.weapon = null; });
try {
  await h.newWeek();
  await h.ev(() => { window.LEDGER_MANUAL = true; LEDGER.G.paused = false; });
  // open ground: where the week starts, as melee3 uses
  const home = await h.ev(() => ({ x: LEDGER.G.tom.x, z: LEDGER.G.tom.z, ang: LEDGER.G.tom.ang }));
  // FACE: alone he gives way at the shove; with three men watching he stands and it comes to blows
  let s = await stage({ ...home, nerve: 0.56, watchers: 0 });
  ok(s.face === 0, 'face alone is nothing: ' + JSON.stringify(s));
  let r = await ladder();
  ok(r.yielded && !r.fight, 'alone, a man of middling nerve gives way when shoved: ' + JSON.stringify(r));
  await restore();
  s = await stage({ ...home, nerve: 0.56, watchers: 3 });
  ok(Math.abs(s.face - 0.18) < 1e-9, 'three men watching add 0.18 to his nerve: ' + JSON.stringify(s));
  r = await ladder();
  ok(!r.yielded && r.fight && r.why === 'face', 'with folk watching the same man will not be shown up and it comes to blows: ' + JSON.stringify(r));
  await restore();
  s = await stage({ ...home, nerve: 0.56, watchers: 6 });
  ok(Math.abs(s.face - 0.24) < 1e-9, 'face is capped at 0.24 however many watch: ' + JSON.stringify(s));
  await restore();
  // a very timid man gives way even in front of a crowd
  s = await stage({ ...home, nerve: 0.3, watchers: 6 });
  r = await ladder();
  ok(r.yielded && !r.fight, 'a timid man still gives way in front of a crowd: ' + JSON.stringify(r));
  await restore();
  // CORNER: a man with a wall 1 m behind him, shoved into it with nowhere to go
  const slam = await h.ev(() => {
    const G = LEDGER.G, t = G.tom, isBlocked = LEDGER.isBlocked;
    for (let rr = 2; rr < 40; rr += 1)
      for (let k = 0; k < 24; k++) {
        const a = (k / 24) * Math.PI * 2, px = t.x + Math.sin(a) * rr, pz = t.z + Math.cos(a) * rr;
        if (isBlocked(px, pz)) continue;
        for (let j = 0; j < 8; j++) {
          const b = (j / 8) * Math.PI * 2, bx = Math.sin(b), bz = Math.cos(b);
          // the man stands 0.4 m off the wall, Tom 1.2 m behind him
          if (isBlocked(px + bx * 0.6, pz + bz * 0.6) && !isBlocked(px, pz) && !isBlocked(px - bx * 1.2, pz - bz * 1.2) && !isBlocked(px - bx * 2, pz - bz * 2))
            return { x: px - bx * 1.2, z: pz - bz * 1.2, ang: b };
        }
      }
    return { error: 'no wall found' };
  });
  ok(!slam.error, 'found a wall to put a man against: ' + JSON.stringify(slam));
  if (!slam.error) {
    s = await stage({ ...slam, nerve: 0.56, watchers: 0 });
    r = await ladder();
    ok(!r.yielded && r.fight && r.why === 'corner', 'shoved against a wall with nowhere to go, the same man comes off it swinging: ' + JSON.stringify(r));
    await restore();
  }
  // GRAB: nothing to hand on open ground
  await h.ev((home) => { const G = LEDGER.G, t = G.tom; t.x = home.x; t.z = home.z; }, home);
  const far = await h.ev(() => {
    const t = LEDGER.G.tom;
    return Math.min(...LEDGER.fight.handProps().map((p) => Math.hypot(p.x - t.x, p.z - t.z) - p.r));
  });
  if (far > 1.2) {
    await stage({ ...home, nerve: 0.95, watchers: 0 });
    await h.ev(() => { const F = LEDGER.F, P = LEDGER.G.crowd.find((p) => p.space === 'street'); LEDGER.fight.setOn([P]); F.tele = []; });
    const g0 = await h.ev(() => LEDGER.fight.grab());
    ok(g0 === false, 'G with nothing to hand does nothing');
    await endFight();
    await restore();
  } else console.log('skip the nothing-to-hand check: a thing lies ' + far.toFixed(2) + ' m from the start');
  // GRAB and M7 BREAKAGE: chair, brick, dustbin lid, wheel brace
  const hitsTo = {};
  for (const [prop, lo, hi] of [['chair', 1, 3], ['brick', 2, 5], ['dustbin lid', 2, 6], ['wheel brace', 25, 99]]) {
    const st = await fightBy(prop);
    ok(!st.error, 'set up by a ' + prop + ': ' + JSON.stringify(st));
    if (st.error) continue;
    const g = await h.ev(() => LEDGER.fight.grab());
    ok(g === true, 'G by a ' + prop + ' starts to snatch it up');
    let ev = await tick(1.0);
    const armed = await h.ev(() => ({ w: LEDGER.G.tom.weapon, armed: LEDGER.G.tom.armed, rung: LEDGER.F.rung }));
    const gs = ev.find((e) => e.ev === 'grab_start'), ge = ev.find((e) => e.ev === 'grab_end');
    ok(armed.armed && armed.w === prop && armed.rung === 6, 'after half a second the ' + prop + ' is in his hand, weapon out: ' + JSON.stringify(armed));
    ok(gs && ge && Math.abs(ge.t - gs.t - 0.5) < 0.05, 'the snatch takes 0.5 s: ' + (gs && ge ? (ge.t - gs.t).toFixed(3) : 'none'));
    // swing each time he can act, until it breaks or 25 hits on a still man who never falls
    ev = await tick(60, "(()=>{return (c)=>{const F=LEDGER.F;F.stam=1;for(const f of F.foes){f.P.hurt=0;f.P.down=false;if(f.st!=='stagger')f.st='still';}const hits=F.tele.filter((e)=>e.ev==='hit_contact'&&e.actor==='player'&&e.weapon&&e.weapon!=='fists').length;if(F.tele.some((e)=>e.ev==='weapon_break')||hits>=25)return;if(F.st==='idle')LEDGER.fight.input('light');}})()");
    runs['M7_breakage_' + prop.replace(' ', '_')] = ev;
    const br = ev.find((e) => e.ev === 'weapon_break');
    const hits = ev.filter((e) => e.ev === 'hit_contact' && e.actor === 'player' && e.weapon === prop && (!br || e.t <= br.t)).length;
    hitsTo[prop] = br ? hits : '>' + hits;
    if (hi < 99) ok(br && hits >= lo && hits <= hi, 'M7: the ' + prop + ' breaks after ' + lo + ' to ' + hi + ' blows: ' + hits + (br ? '' : ' (did not break)'));
    else ok(!br && hits >= 25, 'M7: the ' + prop + ' does not break in 25 blows: ' + hits);
    if (br) {
      const after = await h.ev(() => { for (let i = 0; i < 60 && LEDGER.F.st !== 'idle'; i++) LEDGER.tick(1 / 60); const t = LEDGER.G.tom; return { w: t.weapon, armed: t.armed, st: LEDGER.F.st, on: LEDGER.F.on, rung: LEDGER.F.rung, near: Math.min(...LEDGER.fight.handProps().filter((p) => !p.broken).map((p) => Math.hypot(p.x - t.x, p.z - t.z) - p.r)).toFixed(2), again: LEDGER.fight.grab() }; });
      ok(!after.armed && !after.w, 'once broken it is gone from his hand: ' + JSON.stringify(after));
      if (prop === 'brick') ok(Number(after.near) < 1.1, 'a skip has more bricks: one is still in reach: ' + JSON.stringify(after));
      else ok(after.again === false, 'the broken ' + prop + ' cannot be snatched up again: ' + JSON.stringify(after));
    }
    await endFight();
  }
  console.log('hits to break: ' + JSON.stringify(hitsTo));
  // a blow while he stoops for it stops the snatch
  const st = await fightBy('brick');
  if (!st.error) {
    await h.ev(() => { for (const f of LEDGER.F.foes) f.st = 'guard'; LEDGER.fight.grab(); });
    const res = await h.ev(() => {
      const F = LEDGER.F;
      // the man's blow lands while Tom stoops
      F.st = 'stagger'; F.t = 0.4;
      for (let i = 0; i < 60; i++) LEDGER.tick(1 / 60);
      return { armed: LEDGER.G.tom.armed, w: LEDGER.G.tom.weapon };
    });
    ok(!res.armed, 'struck while stooping for it, he does not come up with it: ' + JSON.stringify(res));
    await endFight();
  }
  {
    // pick up a dustbin lid outside a fight with the G prompt's own call, then fight with it: it breaks after 4 and stays broken
    const res = await h.ev(() => {
      const G = LEDGER.G, t = G.tom, F = LEDGER.F;
      if (F.on) LEDGER.fight.end();
      const p = LEDGER.fight.handProps().find((q) => q.hand === 'dustbin lid' && !q.broken);
      if (!p) return { error: 'no whole lid left' };
      LEDGER.fight.carried(p); t.weapon = p.hand; t.armed = false;
      const P = G.crowd.find((q) => !q.gone && !q.dead && !q.inCar && q.def.sex !== 'f' && (q.def.age || 30) < 60);
      P.space = 'street'; t.space = 'street'; P.x = t.x + Math.sin(t.ang); P.z = t.z + Math.cos(t.ang); P.def.nerve = 0.95; P.hurt = 0; P.down = false;
      let n = 0;
      for (let fight = 0; fight < 2; fight++) {
        LEDGER.fight.setOn([P]); F.tele = []; F.stam = 1;
        for (const f of F.foes) f.st = 'still';
        LEDGER.fight.climb(); // weapon out
        for (let i = 0; i < 60 * 6 && n < 2 + fight * 2; i++) {
          for (const f of F.foes) { f.P.hurt = 0; f.P.down = false; if (f.st !== 'stagger') f.st = 'still'; }
          F.stam = 1;
          if (F.st === 'idle' && t.armed) LEDGER.fight.input('light');
          LEDGER.tick(1 / 60);
          n = Math.max(n, (fight ? 2 : 0) + F.tele.filter((e) => e.ev === 'hit_contact' && e.actor === 'player' && e.weapon === 'dustbin lid').length);
        }
        if (fight === 0) LEDGER.fight.end();
      }
      const broke = F.tele.some((e) => e.ev === 'weapon_break');
      LEDGER.fight.end();
      return { hits: n, broke, weapon: t.weapon, broken: !!p.broken };
    });
    ok(!res.error && res.broke && res.hits === 4 && !res.weapon && res.broken, 'a lid picked up before the fight keeps its count across two fights and breaks on its fourth blow, then stays broken: ' + JSON.stringify(res));
  }
  fs.writeFileSync(OUT, Object.entries(runs).map(([k, v]) => v.map((e) => JSON.stringify(Object.assign({ drill: k }, e))).join('\n')).join('\n') + '\n');
  console.log('drill events written to ' + OUT);
  ok(h.errors.length === 0, 'no page errors' + (h.errors.length ? ': ' + h.errors.join(' | ') : ''));
} finally {
  await h.close();
}
console.log(bad ? 'FAIL: ' + bad : 'PASS');
process.exit(bad ? 1 : 0);
