// The driving study's car in LEDGER (qr/cab.js), measured on the game's own frame loop at 60 frames a second with
// real key events: the driving gate's rules (tools/lane/driving-gate/README.md, checks 1 to 3 and 6) applied to the
// game's page, because that gate's own harness speaks only the study page's interface (window.QR).
//   smooth on keys (each move of the wheel and of the yaw takes at least 0.1 s from 10% to 90%; no frame moves the
//   wheel more than 0.15 of lock or the yaw rate more than 0.15 rad/s) · the study's numbers hold in the game
//   (0 to 30 mph, braking from 30 mph) · a crash is told in words at once · never stranded after any crash.
// The car is put on the quay road by the test (a machine check, not a play story).
import { open } from './stories/play.mjs';

let bad = 0;
const ok = (c, what, got) => { console.log((c ? 'ok   ' : 'TEST FAIL ') + what + (c ? '' : ' | got ' + JSON.stringify(got))); if (!c) bad++; };
const P = await open({ from: 'S02' });
await P.cont();
const put = (x, z, ang) => P.world(({ x, z, ang }) => { const G = LEDGER.G; for (const Q of G.named.concat(G.crowd)) if (Q.space === 'street' && Q.z > 40 && Q.z < 56) { Q.gone = true; Q.hold = true; } G.weather.rain = 0; G.weather.wet = 0; Object.assign(G.car, { x, z, ang, v: 0, dmg: 0, keys: true }); if (G.x.cars) G.x.cars.wrecked = null; const t = G.tom; t.space = 'street'; t.inCar = true; t.x = x; t.z = z; }, { x, z, ang });
const rec = () => P.world(() => { const S = window.__S; S.q = []; S.eachs.q = () => { const c = LEDGER.G.car; S.q.push([c.x, c.z, c.ang, c.v, LEDGER.cabFeel().steerMinusOneToOne]); }; });
const got = () => P.world(() => { const q = window.__S.q; delete window.__S.eachs.q; return q; });
const MPH = 2.2369;
// ---- straight-line numbers
await put(-55, 49.6, Math.PI / 2); await P.secs(0.5);
await rec(); await P.down('KeyW'); await P.secs(9); await P.up('KeyW');
let q = await got();
const t30 = q.findIndex((r) => r[3] * MPH >= 30) / 60, vTop = Math.max(...q.map((r) => r[3])) * MPH;
ok(t30 > 2.5 && t30 < 6, 'W held from rest: 30 mph in ' + t30.toFixed(2) + ' s (the study: about 4)', [t30, vTop]);
await put(-3.2, 38, Math.PI); await P.secs(0.3); // Quay Street: tarmac (the quay itself is setts, with less grip)
await P.down('KeyW'); await P.until(() => LEDGER.G.car.v * 2.2369 >= 30, 12); await P.up('KeyW');
await rec(); await P.down('KeyS'); await P.until(() => Math.abs(LEDGER.G.car.v) < 0.15, 6); await P.up('KeyS');
q = await got();
const bd = Math.hypot(q[q.length - 1][0] - q[0][0], q[q.length - 1][1] - q[0][1]);
ok(bd > 6 && bd < 16, 'S held from 30 mph on the keys: stopped in ' + bd.toFixed(1) + ' m from the key going down (the study, full pedal from the first brake row: 8 to 11; a held key gives 0.84 of the pedal and ramps in)', bd);
// ---- smooth on keys at a held 30 mph
const rise = (a, lo, hi) => { const d = hi - lo; let i0 = -1, i1 = -1; for (let i = 0; i < a.length; i++) { const u = (a[i] - lo) / d; if (i0 < 0 && u >= 0.1) i0 = i; if (i1 < 0 && u >= 0.9) { i1 = i; break; } } return i1 < 0 || i0 < 0 ? -1 : (i1 - i0) / 60; };
const hold30 = async (frames, keys) => { for (let f = 0; f < frames; f++) { const v = await P.world(() => LEDGER.G.car.v * 2.2369); if (f % 3 === 0) { if (v < 30) await P.down('KeyW'); else await P.up('KeyW'); } await P.frames(1); } };
await put(-60, 49.6, Math.PI / 2); await P.secs(0.3);
await P.down('KeyW'); await P.until(() => LEDGER.G.car.v * 2.2369 >= 30, 12);
const move = async (name, press, release, frames = 40) => {
  await rec();
  for (const k of release) await P.up(k);
  for (const k of press) await P.down(k);
  await hold30(frames);
  const a = await got();
  const st = a.map((r) => r[4]), yaw = a.map((r, i) => (i ? (r[2] - a[i - 1][2]) * 60 : 0));
  let dS = 0, dY = 0;
  for (let i = 2; i < a.length; i++) { dS = Math.max(dS, Math.abs(st[i] - st[i - 1])); dY = Math.max(dY, Math.abs(yaw[i] - yaw[i - 1])); }
  const tS = rise(st.map((v) => Math.abs(v - st[0])), 0, Math.abs(st[st.length - 1] - st[0]) || 1);
  ok(tS >= 0.1 && dS <= 0.15 && dY <= 0.15, name + ': the wheel moves over ' + tS.toFixed(3) + ' s (10% to 90%), biggest frame step ' + dS.toFixed(3) + ' of lock, yaw ' + dY.toFixed(3) + ' rad/s', [tS, dS, dY, st[0], st[st.length - 1]]);
};
await move('press A', ['KeyA'], []);
await move('release A', [], ['KeyA']);
await put(-60, 49.6, Math.PI / 2); await P.secs(0.2); await P.down('KeyW'); await P.until(() => LEDGER.G.car.v * 2.2369 >= 30, 12);
await move('press D', ['KeyD'], []);
await move('D to A', ['KeyA'], ['KeyD']);
await move('release A again', [], ['KeyA']);
await P.up('KeyW');
// ---- crashes: told in words at once, and never stranded
const wallRun = async (mph) => {
  await put(15, 47.5, Math.PI); await P.secs(0.3); // facing north at the front wall of Mickey's row
  await P.world((v) => { LEDGER.G.car.v = v; }, mph / MPH);
  await P.down('KeyW'); await P.secs(1.2); await P.up('KeyW');
  await P.secs(0.6);
  const said = (await P.screen()).subs; // what is on the screen 0.6 s after the hit
  const c0 = await P.car();
  await P.down('KeyS'); await P.secs(3.2); await P.up('KeyS');
  const c1 = await P.car();
  let moved = Math.hypot(c1.x - c0.x, c1.z - c0.z);
  if (moved < 1) { await P.down('KeyW'); await P.secs(2.5); await P.up('KeyW'); const c2 = await P.car(); moved = Math.max(moved, Math.hypot(c2.x - c1.x, c2.z - c1.z)); }
  const wrecked = await P.world(() => !!(LEDGER.G.x.cars && LEDGER.G.x.cars.wrecked));
  return { said, moved, wrecked, dmg: c1.dmg, at: [c0.x, c0.z] };
};
for (const mph of [8, 18, 28]) {
  const r = await wallRun(mph);
  ok(mph < 11 || r.said.some((s) => /cab|car|bumper|wing|lamp|dent|radiator|bonnet/i.test(s)), 'into a wall at ' + mph + ' mph: told in words at once', r.said);
  ok(r.moved >= 1 || r.wrecked, '... and not stranded: it backs off ' + r.moved.toFixed(1) + ' m inside 5 s' + (r.wrecked ? ' (it will not drive on, and says so)' : ''), r);
}
{
  const r = await wallRun(40);
  const s = await P.screen();
  ok(r.wrecked ? s.prompts.some((p) => /Get out/.test(p)) : r.moved >= 1, 'into a wall at 40 mph: it will not drive on, and the way out is offered (or it backs off)', [r, s.prompts]);
}
ok((await P.world(() => (LEDGER.faults ? LEDGER.faults().length : 0))) === 0, 'no fault inside any system', 0);
console.log(bad ? 'qrcar: ' + bad + ' FAIL' : 'qrcar: PASS');
await P.close();
process.exit(bad ? 1 : 0);
