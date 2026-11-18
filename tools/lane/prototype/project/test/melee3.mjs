// The lane's round 3 (18 Nov): the melee feel targets, part 1 (weight, readable wind-ups, walls, being
// outnumbered, people watching). Drives fight.js through the test hook at 1/60 s steps and records the drills'
// events in the format tools/lane/melee_drills.py scores; the lane's runner scores the file it writes.
import fs from 'fs';
import { launch } from './harness.mjs';

let bad = 0;
const ok = (cond, what) => {
  console.log((cond ? 'ok   ' : 'FAIL ') + what);
  if (!cond) bad++;
};
const OUT = process.env.MELEE_OUT || 'melee3-drills.jsonl';
const h = await launch({ port: 8799, quality: 'low' });
const runs = {};
// set Tom and n men on open ground at the opening spot, the first d metres in front of him, then start a fight.
// dummy: the men never swing (a still target). wallBehind: put the first man with his back to a wall.
const setup = (o) =>
  h.ev((o) => {
    const G = LEDGER.G,
      t = G.tom,
      F = LEDGER.F;
    const men = G.crowd.filter((p) => !p.gone && !p.dead && !p.inCar && p.def.sex !== 'f' && (p.def.age || 30) < 60).slice(0, o.n);
    if (men.length < o.n) return { error: 'not enough men in the crowd: ' + men.length };
    let x = o.x ?? t.x,
      z = o.z ?? t.z,
      ang = o.ang ?? t.ang;
    t.x = x;
    t.z = z;
    t.ang = ang;
    t.hurt = 0;
    t.space = 'street';
    men.forEach((P, i) => {
      const a = ang + (i === 0 ? 0 : i === 1 ? 1.2 : -1.2);
      const d = i === 0 ? o.d : o.d2 || 3;
      P.space = 'street';
      P.x = x + Math.sin(a) * d;
      P.z = z + Math.cos(a) * d;
      P.hurt = 0;
      P.down = false;
      P.def.nerve = 0.95; // stands his ground (no flight in a drill)
    });
    LEDGER.fight.setOn(men);
    F.tele = [];
    F.stam = 1;
    if (o.dummy) for (const f of F.foes) f.st = 'still';
    return { men: men.map((p) => p.id || p.def.name), foes: F.foes.length };
  }, o);
const tick = (secs, fn) =>
  h.ev(
    ([secs, fn]) => {
      const f = fn ? eval(fn) : null;
      for (let i = 0; i < Math.round(secs * 60); i++) {
        if (f) f(LEDGER.F.clock);
        if (!LEDGER.F.on) break;
        LEDGER.tick(1 / 60);
      }
      return LEDGER.F.tele.slice();
    },
    [secs, fn],
  );
const endFight = () => h.ev(() => { LEDGER.F.tele = null; if (LEDGER.F.on) LEDGER.fight.end(); for (const P of LEDGER.G.crowd) { P.down = false; P.hurt = 0; } });
try {
  await h.newWeek();
  await h.ev(() => { window.LEDGER_MANUAL = true; LEDGER.G.paused = false; });
  // find an open spot: Tom where the week starts, facing along the street
  // M1 heavy at 1.0 m, a still man
  let s = await setup({ n: 1, d: 1.0, dummy: true });
  ok(!s.error && s.foes === 1, 'M1 set up: ' + JSON.stringify(s));
  let ev = await tick(3, "(()=>{let done=false;return (c)=>{if(!done&&c>0.5){done=true;LEDGER.fight.input('heavy');}}})()");
  runs.M1_heavy = ev;
  const hc = ev.find((e) => e.ev === 'hit_contact' && e.actor === 'player');
  const hs = ev.find((e) => e.ev === 'hit_start' && e.actor === 'player');
  const st0 = ev.find((e) => e.ev === 'hitstop_start'), st1 = ev.find((e) => e.ev === 'hitstop_end');
  ok(hc && hs && hc.t - hs.t >= 0.63 && hc.t - hs.t <= 0.85, 'M1 heavy: start to contact inside 0.63 to 0.85 s: ' + (hc && hs ? (hc.t - hs.t).toFixed(3) : 'no contact'));
  ok(st0 && st1 && st1.t - st0.t >= 0.06 && st1.t - st0.t <= 0.12 + 1 / 60, 'M1 heavy: hit-stop inside 0.06 to 0.12 s: ' + (st0 && st1 ? (st1.t - st0.t).toFixed(3) : 'none'));
  const sg = ev.find((e) => e.ev === 'stagger_start' && e.actor !== 'player');
  ok(sg && sg.severity === 'heavy', 'M1 heavy: the man struck reels (heavy): ' + JSON.stringify(sg));
  const sge = ev.find((e) => e.ev === 'stagger_end' && e.actor !== 'player');
  ok(sg && sge && sge.t - sg.t >= 0.9 && sge.t - sg.t <= 1.3 + 1 / 60, 'M1 heavy: his reaction lasts 0.9 to 1.3 s: ' + (sg && sge ? (sge.t - sg.t).toFixed(3) : 'none'));
  const rc = ev.find((e) => e.ev === 'recovery_end' && e.actor === 'player');
  ok(hc && st1 && rc && rc.t - hc.t - (st1.t - st0.t) >= 0.35 && rc.t - hc.t - (st1.t - st0.t) <= 0.5 + 1 / 60, 'M1 heavy: Tom busy 0.35 to 0.50 s after contact (freeze not counted): ' + (rc && hc ? (rc.t - hc.t - (st1.t - st0.t)).toFixed(3) : 'none'));
  await endFight();
  // M1 jab
  s = await setup({ n: 1, d: 1.0, dummy: true });
  ev = await tick(2, "(()=>{let done=false;return (c)=>{if(!done&&c>0.5){done=true;LEDGER.fight.input('light');}}})()");
  runs.M1_jab = ev;
  const jc = ev.find((e) => e.ev === 'hit_contact' && e.actor === 'player'), js = ev.find((e) => e.ev === 'hit_start' && e.actor === 'player');
  ok(jc && js && jc.t - js.t >= 0.25 && jc.t - js.t <= 0.4, 'M1 jab: start to contact inside 0.25 to 0.40 s: ' + (jc && js ? (jc.t - js.t).toFixed(3) : 'no contact'));
  const jg = ev.find((e) => e.ev === 'stagger_start' && e.actor !== 'player'), jge = ev.find((e) => e.ev === 'stagger_end' && e.actor !== 'player');
  ok(jg && jge && jge.t - jg.t >= 0.5 && jge.t - jg.t <= 0.7 + 1 / 60, 'M1 jab: his reaction lasts 0.5 to 0.7 s: ' + (jg && jge ? (jge.t - jg.t).toFixed(3) : 'none'));
  await endFight();
  // wall: a man with his back to a wall, struck
  // M9 stamina: jab until too tired, then idle until full
  s = await setup({ n: 1, d: 1.0, dummy: true });
  ev = await tick(16, "(()=>{return (c)=>{const F=LEDGER.F;for(const f of F.foes){f.P.hurt=0;if(f.st!=='still'&&f.st!=='stagger')f.st='still';}if(!F.tele.some((e)=>e.ev==='stamina_empty')&&F.st==='idle')LEDGER.fight.input('light');}})()");
  runs.M9_stamina = ev;
  const jabsToEmpty = (() => { const e = ev.find((x) => x.ev === 'stamina_empty'); return e ? ev.filter((x) => x.ev === 'hit_start' && x.actor === 'player' && x.t <= e.t).length : 0; })();
  ok(jabsToEmpty >= 6 && jabsToEmpty <= 10, 'M9: jabs from full to too tired inside 6 to 10: ' + jabsToEmpty);
  const emp = ev.find((x) => x.ev === 'stamina_empty'), full = emp && ev.find((x) => x.ev === 'stamina' && x.value >= 0.99 && x.t > emp.t);
  ok(emp && full && full.t - emp.t >= 4 && full.t - emp.t <= 8, 'M9: tired to full breath inside 4 to 8 s: ' + (emp && full ? (full.t - emp.t).toFixed(2) : 'not reached'));
  await endFight();
  // M6 two attackers, Tom does nothing for 20 s (he is not allowed to go down: hurt reset each step)
  s = await setup({ n: 3, d: 2.5, d2: 2.5 });
  ok(!s.error && s.foes >= 2, 'M6 set up: ' + JSON.stringify(s));
  ev = await tick(20, "(()=>{return (c)=>{LEDGER.G.tom.hurt=0;}})()");
  runs.M6_three = ev;
  // peak men swinging at once, and the smallest gap between two men's swing starts
  const starts = ev.filter((e) => e.ev === 'attack_start');
  let cur = 0, peak = 0;
  for (const e of ev) { if (e.ev === 'attack_start') peak = Math.max(peak, ++cur); if (e.ev === 'attack_end') cur--; }
  let gap = 9;
  for (let i = 1; i < starts.length; i++) if (starts[i].actor !== starts[i - 1].actor) gap = Math.min(gap, starts[i].t - starts[i - 1].t);
  ok(starts.length >= 4, 'M6: the men swing (' + starts.length + ' swings in 20 s)');
  ok(peak <= 2, 'M6: at most two men swinging at once: ' + peak);
  ok(gap >= 0.4, 'M6: two men\'s swings start at least 0.40 s apart: ' + gap.toFixed(3));
  const tele = ev.filter((e) => e.ev === 'telegraph_start'), contacts = ev.filter((e) => (e.ev === 'hit_contact' || e.ev === 'block') && e.actor !== 'player');
  let minLead = 9;
  for (const c of contacts) { const t0 = [...tele].reverse().find((x) => x.actor === c.actor && x.t <= c.t); if (t0) minLead = Math.min(minLead, c.t - t0.t); }
  ok(minLead >= 0.45 && minLead <= 0.8 + 1 / 60, 'M6: every wind-up readable 0.45 to 0.80 s before it lands: ' + minLead.toFixed(3));
  const watching = await h.ev(() => LEDGER.F.watch.length);
  await endFight();
  // the wall slam: search the map near Tom for a man-sized spot with a wall just behind
  const slam = await h.ev(() => {
    const G = LEDGER.G, t = G.tom, F = LEDGER.F;
    const isBlocked = LEDGER.isBlocked;
    if (!isBlocked) return { error: 'no isBlocked in the hook' };
    for (let r = 2; r < 40; r += 1)
      for (let k = 0; k < 24; k++) {
        const a = (k / 24) * Math.PI * 2, px = t.x + Math.sin(a) * r, pz = t.z + Math.cos(a) * r;
        if (isBlocked(px, pz)) continue;
        for (let j = 0; j < 8; j++) {
          const b = (j / 8) * Math.PI * 2, bx = Math.sin(b), bz = Math.cos(b);
          if (isBlocked(px + bx * 0.6, pz + bz * 0.6) && !isBlocked(px - bx * 1.0, pz - bz * 1.0) && !isBlocked(px - bx * 2, pz - bz * 2))
            return { x: px - bx * 1.0, z: pz - bz * 1.0, ang: b };
        }
      }
    return { error: 'no wall found' };
  });
  ok(!slam.error, 'found a wall to drive a man into: ' + JSON.stringify(slam));
  if (!slam.error) {
    s = await setup({ n: 1, d: 1.0, dummy: true, x: slam.x, z: slam.z, ang: slam.ang });
    ev = await tick(3, "(()=>{let done=false;return (c)=>{if(!done&&c>0.5){done=true;LEDGER.fight.input('light');}}})()");
    runs.wall = ev;
    const fh = ev.find((e) => e.ev === 'fall_hazard'), sw = ev.find((e) => e.ev === 'stagger_start' && e.actor !== 'player'), se = ev.find((e) => e.ev === 'stagger_end' && e.actor !== 'player');
    ok(fh && fh.surface === 'wall', 'a jab into a man with his back to a wall drives him into it: ' + JSON.stringify(fh));
    ok(sw && sw.severity === 'heavy' && se && se.t - sw.t >= 0.9 && se.t - sw.t <= 1.3 + 1 / 60, 'and he reels as from a heavy blow (0.9 to 1.3 s): ' + (sw && se ? (se.t - sw.t).toFixed(3) : JSON.stringify([sw, se])));
    await endFight();
  }
  console.log('watchers at the M6 fight: ' + watching);
  fs.writeFileSync(OUT, Object.entries(runs).map(([k, v]) => v.map((e) => JSON.stringify(Object.assign({ drill: k }, e))).join('\n')).join('\n') + '\n');
  console.log('drill events written to ' + OUT);
  ok(h.errors.length === 0, 'no page errors' + (h.errors.length ? ': ' + h.errors.join(' | ') : ''));
} finally {
  await h.close();
}
console.log(bad ? "FAIL: " + bad : "PASS");
process.exit(bad ? 1 : 0);
