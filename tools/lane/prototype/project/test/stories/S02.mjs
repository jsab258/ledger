// S02 The first fare (ONE-SHOT-PROMPT.md). From the save S01 leaves at the radio; then, for the two things that hang on
// the first hour's own timing (the fare by 3:00 of play, dusk falling as he drives), the same fare once more from New
// game by the straight way a player takes. Played by keys; judged by the screen, the mix and the world.
import { run } from './play.mjs';

await run('S02', { from: 'S01' }, async (P, t, n) => {
  const go = async (x, z, o = {}) => { const r = await P.walkTo(x, z, Object.assign({ maxSecs: 60 }, o)); if (r < 0) { const m = await P.tom(); t.ok(false, 'he can walk to ' + Math.round(x) + ', ' + Math.round(z), [Math.round(m.x * 10) / 10, Math.round(m.z * 10) / 10, m.space]); } return r; };
  const drive = async (pts, what, o = {}) => { const r = await P.drive(pts, Object.assign({ maxSecs: 120, speed: 7.5 }, o)); if (r < 0) t.ok(false, 'he can drive ' + what, await P.car()); return r; };
  const subs = async () => (await P.screen()).subs;
  const lastSub = async (rx) => (await P.subsLog()).filter((x) => rx.test(x.s)).pop();
  // what is watched on every frame of the driving: the camera, the wheel, who brakes for whom, who steps out
  const watchDriving = () => P.world(() => {
    const S = window.__S, G = LEDGER.G;
    S.dr = { n: 0, camInside: 0, where: [], backMin: 99, backMax: 0, backIn: 0, backN: 0, fovRest: 0, fovFast: 0, hitPeople: 0, steppedOut: 0, trafficHits: 0, braked: 0, walshMoving: [], maxV: 0 };
    const was = {};
    S.eachs.drive = () => {
      const t = G.tom, c = G.car, cam = LEDGER.camera, D = S.dr;
      if (!t.inCar || G.paused) return;
      D.n++;
      D.maxV = Math.max(D.maxV, Math.abs(c.v));
      const inside = LEDGER.cameraInside();
      if (inside) { D.camInside++; if (D.where.length < 4) D.where.push([Math.round(cam.position.x), Math.round(cam.position.z), inside]); }
      if (!S.keys.KeyB) { const back = Math.hypot(cam.position.x - c.x, cam.position.z - c.z); if (D.n > 90) { D.backN++; D.bk = D.bk || {}; const key = Math.floor(back) + (Math.abs(c.v) > 2 ? 'm' : 's'); D.bk[key] = (D.bk[key] || 0) + 1; if (back > 5.0 && back < 6.6) D.backIn++; D.backMin = Math.min(D.backMin, back); D.backMax = Math.max(D.backMax, back); } if (Math.abs(c.v) < 0.5) D.fovRest = cam.fov; if (Math.abs(c.v) > 6) D.fovFast = Math.max(D.fovFast, cam.fov); }
      // nobody on foot steps into the road inside the stopping distance of the cab at 30 mph or less
      const fx = Math.sin(c.ang), fz = Math.cos(c.ang), stop = (c.v * c.v) / (2 * LEDGER.rules.driving.brakingMetresPerSecondSquared);
      for (const Q of G.named.concat(G.crowd)) {
        if (Q.gone || Q.inCar || Q.space !== 'street') continue;
        const dx = Q.x - c.x, dz = Q.z - c.z, f = dx * fx + dz * fz, l = Math.abs(dx * fz - dz * fx), inPath = f > 2.2 && f < stop + 2.2 && l < 1.1, w = was[Q.id];
        if (inPath && w === false && c.v > 1 && c.v <= 13.5 && Q.moving) D.steppedOut++;
        was[Q.id] = inPath;
        if (Math.hypot(dx, dz) < 0.9 && Math.abs(c.v) > 0.5) D.hitPeople++;
      }
      // other cars brake for people and for him: none of them drives into a person or into the cab
      for (const v of LEDGER.streetThings().cars) {
        if (v.parked) continue;
        if (Math.hypot(v.xMetres - c.x, v.zMetres - c.z) < 1.6 && v.speedMetresPerSecond > 1) D.trafficHits++;
        for (const Q of G.named.concat(G.crowd)) if (!Q.gone && !Q.inCar && Q.space === 'street' && Math.hypot(v.xMetres - Q.x, v.zMetres - Q.z) < 0.7 && v.speedMetresPerSecond > 1) D.trafficHits++;
        const key = 'v' + Math.round(v.xMetres * 0 + v.lengthMetres * 100) + ':' + (v.bus ? 'b' : 'c');
        void key;
      }
      for (const e of document.querySelectorAll('#subs .s')) { const s = e.innerText.trim(); if (/WALSH/i.test(s) && !D.walshMoving.some((x) => x.s === s)) D.walshMoving.push({ s, v: Math.round(Math.abs(c.v) * 10) / 10 }); }
    };
  });

  // ---------- A. from the save S01 leaves ----------
  let s = await P.screen();
  t.ok(s.title && s.title.some((b) => /^continue/i.test(b)), 'the title offers Continue', s.title);
  await P.cont();
  let me = await P.tom();
  t.ok(me.space === 'mickeys', 'Continue puts him back in the office, at the radio', me);
  const mat = await P.world(() => { const r = LEDGER.roomOf('mickeys'); return [r.ox + r.mat[0], r.oz + r.mat[1] - 0.3]; });
  await go(mat[0], mat[1], { near: 0.6 });
  await P.use(/Leave/);
  await P.until(() => LEDGER.G.tom.space === 'street', 5);
  // 1. car two from the rank: E at the driver's door
  const car0 = await P.car();
  await go(car0.x + 1.5, car0.z - 0.8, { near: 0.5 });
  await P.secs(0.4);
  s = await P.screen();
  t.ok(s.prompts.some((p) => /car two/i.test(p) && /driver's door/i.test(p)), "at car two the prompt names the driver's door", s.prompts);
  await watchDriving();
  let t0 = await P.played();
  await P.use(/car two/);
  const inT = await P.until(() => LEDGER.G.tom.inCar, 4);
  t.ok(inT >= 0 && (await P.played()) - t0 < 2, 'getting in takes under 2 real seconds', (await P.played()) - t0);
  await P.secs(1.2);
  s = await P.screen();
  const toPick = await lastSub(/PAULINE, ON THE RADIO.*Infirmary/i);
  t.ok(!!toPick && /Harbour Office clock/.test(toPick.s) && /lamp over its door/.test(toPick.s), 'Pauline gives the way to the fare by landmarks', toPick);
  // the wheel on keys: to full lock in 0.2 to 0.35 s, back to the centre in 0.4 to 0.9 s (standing, so the car does not turn)
  const lock = await P.world(async () => { const S = window.__S; S.kd('KeyD'); const n = await S.run(120, () => Math.abs(LEDGER.cabFeel().steerMinusOneToOne) >= 0.995); S.ku('KeyD'); const m = await S.run(240, () => Math.abs(LEDGER.cabFeel().steerMinusOneToOne) <= 0.005); return [n / 60, m / 60]; });
  t.ok(lock[0] >= 0.2 && lock[0] <= 0.35, 'on keys the steering eases to lock in 0.2 to 0.35 s', [lock, await P.world(() => [LEDGER.G.paused, LEDGER.G.pauseWhy, LEDGER.ui.modal, LEDGER.G.tom.inCar, LEDGER.cabFeel()]), await P.screen()]);
  t.ok(lock[1] >= 0.4 && lock[1] <= 0.9, 'and centres itself in 0.4 to 0.9 s', lock[1]);
  // 3. the watch and the office clock agree
  await P.tap('KeyN');
  await P.frames(6);
  const w0 = await P.world(() => ({ watch: LEDGER.watch(), clocks: LEDGER.clocks(), t: LEDGER.G.t, on: document.getElementById('watch').classList.contains('on'), words: document.getElementById('watchwords').innerText }));
  t.ok(w0.on && w0.watch && /\w+, Monday/.test(w0.words), 'N raises his watch: the hour on its face, in words under it', w0.words);
  const office = w0.clocks.find((c) => /office clock/.test(c.name)), harbour = w0.clocks.find((c) => /Harbour/.test(c.name));
  t.ok(office && Math.abs(office.showsGameMinute - Math.floor(w0.watch.hourFloat * 60 + 0.001) % 1440 - Math.floor(w0.t / 1440) * 1440) <= 1, 'the watch agrees with the office clock on the wall beside the rank', [office, w0.watch]);
  const gone = await P.until(() => !document.getElementById('watch').classList.contains('on'), 4);
  t.ok(gone > 1.6 && gone < 2.4, 'the watch shows for 2 seconds', gone);
  // R has Pauline say the way again
  const before = (await P.world(() => LEDGER.mix.filter((m) => m.n === 'radio').length));
  await P.secs(1);
  await P.tap('KeyR'); await P.secs(0.4);
  s = await P.screen();
  t.ok(s.subs.some((x) => /Infirmary/.test(x)) && (await P.world(() => LEDGER.mix.filter((m) => m.n === 'radio').length)) > before, 'R has Pauline say the way again, on the radio', s.subs);
  // 2. the fare, driven by her words alone: down to the quay, right, past the Harbour Office clock and the ferry landing,
  // the last building with the lamp over its door
  const fareT0 = t0, clockT0 = await P.clock(), clockAt = await P.played(); // the fare is his from the moment he sat in
  await drive([[3.6, 42.5], [0, 49.6], [-20, 49.6], [-28.5, 49.6]], 'to the Harbour Office clock', { stopWithin: 6 });
  const passing = await P.world(() => ({ clocks: LEDGER.clocks(), t: LEDGER.G.t }));
  const hc = passing.clocks.find((c) => /Harbour/.test(c.name));
  t.ok(hc && Math.abs(hc.showsGameMinute - Math.floor(passing.t)) <= 1, 'the Harbour Office clock, as he drives past it, shows the same hour as the game clock', [hc, passing.t]);
  await drive([[-60, 49.6], [-115.5, 49.6]], 'on to the Infirmary', { stopWithin: 2 });
  const picked = await P.until(() => LEDGER.G.people.walsh.inCar, 8);
  t.ok(picked >= 0, 'Father Walsh is waiting at the Infirmary and gets in', await P.world(() => { const W = LEDGER.G.people.walsh; return [W.x, W.z, W.space, LEDGER.G.car.x, LEDGER.G.car.z]; }));
  await P.secs(1);
  const way = await lastSub(/PAULINE, ON THE RADIO.*priest's house/i);
  t.ok(!!way && /over the crossing/.test(way.s) && /green door/.test(way.s) && /slippers on the step/.test(way.s), "Pauline gives the way to the priest's house by landmarks", way);
  const before2 = (await P.world(() => LEDGER.mix.filter((m) => m.n === 'radio').length));
  await P.tap('KeyR'); await P.secs(0.4);
  t.ok((await subs()).some((x) => /slippers on the step/.test(x)) && (await P.world(() => LEDGER.mix.filter((m) => m.n === 'radio').length)) > before2, 'R says the way to the house again', await subs());
  // back along the quay, left up Quay Street, over the crossing and past the caff; the chapel on the left
  await drive([[-118, 48.4], [-106, 46.6], [-60, 46.6], [-9, 46.6], [-3.2, 40], [-3.2, 14], [-3.2, -40], [-3.2, -66]], "back to the priest's house by her words");
  const done = await P.until(() => !LEDGER.G.story.fare, 8);
  const fareSecs = (await P.played()) - fareT0, gameMin = (await P.clock()) - clockT0, clockSecs = (await P.played()) - clockAt;
  t.ok(done >= 0, "following her words alone arrives at the priest's house", await P.car());
  t.ok(fareSecs >= 60 && fareSecs <= 120, 'the fare lasts 1 to 2 real minutes', fareSecs);
  t.ok(Math.abs(gameMin / (clockSecs / 45) - 60) < 2, 'one game hour takes 45 real seconds of play', [gameMin, clockSecs]);
  await P.secs(1.5);
  const paid = await lastSub(/^FATHER[^a-z]*WALSH|^BRENDAN WALSH|WALSH/i);
  const spoken = (await P.subsLog()).filter((x) => /pounds? /.test(x.s) && /There you are/.test(x.s)).pop();
  t.ok(!!spoken && /two pounds thirty/i.test(spoken.s), 'the fare is spoken: 80p and the distance, two pounds thirty', spoken || paid);
  t.ok((await P.world(() => LEDGER.mix.some((m) => m.n === 'voice' && /Walsh/.test(m.who)))), 'in his voice, in the mix', 0);
  const dr = await P.world(() => window.__S.dr);
  t.ok(dr.walshMoving.filter((x) => x.v > 1).length >= 1, 'the fare talks from the back seat while the car moves', dr.walshMoving);
  const mv = Object.entries(dr.bk || {}).filter(([k]) => k.endsWith('m')), mvAll = mv.reduce((a, [, v]) => a + v, 0), mvIn = mv.filter(([k]) => k === '4m' || k === '5m' || k === '6m').reduce((a, [, v]) => a + v, 0), mvMost = mv.slice().sort((a, b) => b[1] - a[1])[0][0];
  t.ok(mvIn / mvAll > 0.9 && (mvMost === '5m' || mvMost === '6m') && dr.backMax < 6.8, 'driving, the car camera sits about 5.8 m back (nearer only when something is close behind the cab)', [mvIn, mvAll, dr.backMin, dr.backMax, dr.bk]);
  t.ok(dr.fovFast > dr.fovRest + 1, 'and widens with speed', [dr.fovRest, dr.fovFast, dr.maxV]);
  t.ok(dr.camInside === 0, 'no frame at the wheel shows the inside of a wall, a car or a post', [dr.camInside, dr.n, dr.where]);
  t.ok(dr.steppedOut === 0, 'nobody steps out inside the stopping distance of the cab', dr.steppedOut);
  t.ok(dr.hitPeople === 0 && dr.trafficHits === 0, 'nobody is struck: the other cars brake for people and for him', [dr.hitPeople, dr.trafficHits]);
  // the Money page, in words, and the fare book
  s = { ledger: await P.ledger('money') };
  t.ok(/fare book/i.test(s.ledger) && /two pounds thirty|£2\.30/i.test(s.ledger), 'the Money page shows the fare in the fare book, in words', [s.ledger.slice(60, 400), await P.world(() => [LEDGER.G.money.clean, LEDGER.G.money.fares, LEDGER.G.money.fareCount])]);
  t.note('the Money page after the first fare', s.ledger.replace(/\s+/g, ' ').slice(0, 400));
  await P.ledgerClose();
  // 4. out at the chapel by the kerb side
  let c = await P.car();
  t0 = await P.played();
  await P.use(/Get out/);
  await P.until(() => !LEDGER.G.tom.inCar, 4);
  me = await P.tom();
  t.ok(!me.inCar && (await P.played()) - t0 < 2, 'getting out takes under 2 real seconds', (await P.played()) - t0);
  t.ok(me.x < c.x - 1, 'at the chapel he gets out on the kerb side', [me.x, c.x]);
  await P.secs(1);
  // back to the rank outside Mickey's: up to the top of the street, round, and down
  await P.use(/car two/);
  await P.until(() => LEDGER.G.tom.inCar, 4);
  await drive([[-3.2, -84], [0, -92], [3.2, -84], [3.2, 18], [1.4, 24], [1.4, 29], [3.6, 34], [4.1, 37]], 'back to the rank', { stopWithin: 2 });
  await P.use(/Get out/);
  await P.until(() => !LEDGER.G.tom.inCar, 4);
  // the bell: every hour struck while he was out, by day, was struck with the right number of strokes
  const bells = await P.world(() => LEDGER.mix.filter((m) => /^bell:/.test(m.n)).map((m) => [m.n, Math.round(m.t / 60) % 24]));
  t.ok(bells.every((b) => +b[0].slice(5) === (b[1] % 12 || 12)), 'the chapel bell, when it strikes, strikes the hour the watch shows', bells);
  // back in the office, the save this story leaves
  await go(6.2, 36, { near: 0.6 });
  await P.face(7.2, 36); await P.secs(0.4);
  await P.use(/Go into Mickey/);
  await P.until(() => LEDGER.G.tom.space === 'mickeys', 5);
  t.ok((await P.tom()).space === 'mickeys', 'back at the office', await P.tom());
  await P.tap('Escape'); await P.secs(0.3);
  await P.click('[data-act="save"]'); await P.secs(0.5);
  await P.tap('Escape'); await P.secs(0.3);
  if (t.first) await P.keep('S02');
  t.note('fares in the book', await P.world(() => [LEDGER.G.money.fareCount, LEDGER.G.money.fares, LEDGER.G.money.clean]));

  // ... and once more (after the save, so the evening's clock is not spent on it) with a parked car against the kerb-side
  // door: he leaves by the road side
  await P.tap('Escape'); await P.secs(0.3); // out of the pause menu the save left open
  if ((await P.screen()).book) { await P.tap('Escape'); await P.secs(0.3); }
  await go(mat[0], mat[1], { near: 0.6 }); await P.use(/Leave/); await P.until(() => LEDGER.G.tom.space === 'street', 5);
  const cr = await P.car();
  await go(cr.x + 1.5, cr.z - 0.8, { near: 0.5 }); await P.secs(0.3);
  await P.use(/car two/);
  await P.until(() => LEDGER.G.tom.inCar, 4);
  const parked = await P.world(() => LEDGER.streetThings().cars.filter((v) => v.parked).map((v) => [v.xMetres, v.zMetres, v.facingRadians, v.widthMetres, v.lengthMetres]).find((v) => Math.abs(v[1] - 51) < 2 && v[0] > 40));
  t.ok(!!parked, 'a car stands parked at the kerb on the quay, by the fish dock', parked);
  if (parked) {
    // up to the top of the street, round, down to the quay, left along it, round again and in beside the parked car
    const lane = parked[1] - parked[3] / 2 - 1.6; // close beside it: a hand's width between the two cars
    await drive([[3.2, 41.5], [3.4, 45.6], [10, 46.6], [parked[0] + 30, 46.6], [parked[0] + 37, 47.8], [parked[0] + 30, lane], [parked[0] + 16, lane]], 'round to the fish dock', { maxSecs: 200, stopWithin: 3 });
    await drive([[parked[0] + 6, lane], [parked[0], lane]], 'in beside the parked car', { maxSecs: 40, stopWithin: 1.2, speed: 3, besideParked: true });
    c = await P.car();
    t.ok(Math.abs(c.x - parked[0]) < 2.2 && Math.abs(c.z - lane) < 0.5, 'he stops close beside it, its side against his kerb-side door', [c.x, c.z, parked]);
    await P.use(/Get out/);
    await P.until(() => !LEDGER.G.tom.inCar, 4);
    me = await P.tom();
    t.ok(!me.inCar, 'the blocked door does not trap him', me);
    t.ok(me.z < c.z - 1, 'he leaves by the road side', [me.z, c.z, parked[1]]);
    t.ok(await P.world(() => LEDGER.standable(LEDGER.G.tom.x, LEDGER.G.tom.z)), 'onto clear ground', me);
  }
  // ---------- B. the same fare from New game by the straight way: the first hour's own timing ----------
  await P.tap('Escape'); await P.secs(0.3);
  await P.click('[data-act="totitle"]'); await P.secs(1);
  await P.newGame();
  await P.secs(1);
  await P.tap('Escape');
  await P.until(() => LEDGER.G.story.phase === 'play' && !LEDGER.G.paused && LEDGER.G.tom.space === 'street' && !LEDGER.ui.shot, 5);
  const start = await P.played();
  // a newcomer's pace: he looks about on the quay, and stops a moment for each of the people who speak to him
  await go(-40, 43.5); await P.secs(12); await go(-2, 43); await P.secs(6); await go(7.3, 41); await P.secs(8); await go(7.3, 31.5); await P.secs(8); await go(-4.6, 31); await P.secs(6); await go(6.2, 36, { near: 0.6 });
  await P.face(7.2, 36); await P.secs(0.3);
  await P.use(/Go into Mickey/);
  await P.until(() => LEDGER.G.tom.space === 'mickeys', 5);
  for (let k = 0; k < 150; k++) {
    if (await P.world(() => LEDGER.G.car.keys)) break;
    const sh = await P.world(() => { const S = LEDGER.G.people.sheila; return [S.x, S.z]; });
    me = await P.tom();
    if (Math.hypot(me.x - sh[0], me.z - sh[1]) > 2.0) await P.walkTo(sh[0], sh[1], { maxSecs: 1.5, near: 1.7 }); else await P.secs(0.3);
  }
  t.ok(await P.world(() => LEDGER.G.car.keys), 'the walk-round ends with the keys of car two', await P.world(() => LEDGER.game.hour1.x().round));
  await go(mat[0], mat[1], { near: 0.6 });
  await P.use(/Leave/);
  await P.until(() => LEDGER.G.tom.space === 'street', 5);
  const c2 = await P.car();
  await go(c2.x + 1.5, c2.z - 0.8, { near: 0.5 });
  await P.secs(0.3);
  await P.use(/car two/);
  await P.until(() => !!LEDGER.G.story.fare && LEDGER.G.tom.inCar, 6);
  const fareAt = (await P.played()) - start + 20; // the ferry shot is 20 s of the first hour
  t.ok(fareAt <= 180, 'the first fare starts by 3 real minutes of play', fareAt);
  t.ok(fareAt >= 120 && fareAt <= 180, 'at about 2:30 (the straight way, the ferry shot counted)', fareAt);
  const lamps0 = await P.world(() => LEDGER.lampsOn());
  await drive([[3.6, 42.5], [0, 49.6], [-60, 49.6], [-115.5, 49.6]], 'to the Infirmary', { stopWithin: 2 });
  await P.until(() => LEDGER.G.people.walsh.inCar, 8);
  await drive([[-118, 48.4], [-106, 46.6], [-60, 46.6], [-9, 46.6], [-3.2, 40], [-3.2, 14], [-3.2, -40], [-3.2, -66]], "to the priest's house");
  await P.until(() => !LEDGER.G.story.fare, 8);
  const lamps1 = await P.world(() => LEDGER.lampsOn());
  t.ok(lamps0 < 0.5 && lamps1 > lamps0 + 0.4, 'dusk falls and the lamps come on while he drives', [lamps0, lamps1, await P.clock()]);
  t.note('lamps', [lamps0 < 0.5, lamps1 > 0.5]);
});
