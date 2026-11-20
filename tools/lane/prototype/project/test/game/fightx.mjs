// The whole game, system "fightx": slip and counter, the hold, fighter types, the quiet blow, the weapon on a held
// input, a man in the water, people stepping in, and how each fight ended. Each check names its rule.
import { launch } from '../harness.mjs';
let bad = 0;
const ok = (c, what) => {
  console.log((c ? 'ok   ' : 'FAIL ') + what);
  if (!c) bad++;
};
const h = await launch({ port: 8842, quality: 'low' });
try {
  await h.newWeek();
  const L = (fn, ...a) => h.ev(fn, ...a);
  await L(() => {
    const G = LEDGER.G;
    window.__ends = [];
    window.__run = (s) => { for (let i = 0; i < s * 60; i++) LEDGER.tick(1 / 60); };
    window.__put = (x, z, a = 0) => { const t = G.tom; t.inCar = false; t.space = 'street'; t.x = x; t.z = z; t.ang = a; t.v = 0; t.carry = null; t.hurt = 0; };
    window.__man = (id, x, z, ang) => { const P = G.people[id]; P.gone = false; P.space = 'street'; P.x = x; P.z = z; P.ang = ang; P.hold = true; P.route = null; P.moving = false; P.awake = true; P.down = false; P.hurt = 0; P.fight = null; return P; };
    window.__key = (code, up) => dispatchEvent(new KeyboardEvent(up ? 'keyup' : 'keydown', { code }));
    window.__fight = (ids, x = 0, z = -60) => { if (LEDGER.F.on) LEDGER.fight.end(); __put(x, z, 0); const Ps = ids.map((id, i) => __man(id, x + i * 0.9, z + 1.0, Math.PI)); LEDGER.fight.setOn(Ps); return Ps; };
    for (const f of ['tour', 'metRon', 'metDarren', 'metJune']) G.story.flags[f] = 1;
    G.t = 1 * 1440 + 11 * 60;
    LEDGER.game.emit; // (the systems' own bus)
  });
  await L(() => { const core = LEDGER.game; window.__onEnd = (e) => __ends.push({ how: e.how, tier: e.tier, n: e.foes.length, quiet: !!e.quiet }); });

  // ---- fighter types (ER-TYPES-01) and the fight's end told to every system
  const types = await L(() => {
    const out = [], G = LEDGER.G;
    for (let i = 0; i < 3; i++) { __fight(['lee']); out.push(LEDGER.game.fightx.types()[0]); LEDGER.fight.end(); }
    __fight(['lee', 'wayne']); const two = LEDGER.game.fightx.types().slice(); LEDGER.fight.end();
    return { out, two, last: LEDGER.game.fightx.lastEnd(), n: G.x.fightx.fights, ends: G.x.fightx.ends };
  });
  ok(types.out.every((t) => ['boxer', 'brawler', 'big'].includes(t)) && types.out[0] !== types.out[1] && types.out[1] !== types.out[2], `ER-TYPES-01 the same man fought three times running is never the same kind twice in a row (${types.out.join(', ')}); two men: ${types.two.join(' and ')}`);
  ok(types.last && types.last.how === 'backed off' && types.n === 4 && types.ends['backed off'] === 4, `'fight:end' is told at every end, with how it ended (${JSON.stringify(types.ends)})`);

  // ---- the slip and the counter (ER-DEFEND-01, 02)
  const slip = await L(() => {
    const G = LEDGER.G, F = LEDGER.F, out = {};
    const [P] = __fight(['lee']);
    const f = F.foes[0]; f.type = 'boxer';
    // his blow comes; the tell is the whole of his wind-up
    f.st = 'guard'; f.t = 0; F.lastFoeStart = -99; __run(0.05);
    out.windup = f.st; out.tell = f.tell;
    // slip to the side just before it lands
    while (f.st === 'windup' && f.t > 0.12) LEDGER.tick(1 / 60);
    const x0 = G.tom.x, hurt0 = G.tom.hurt;
    __key('KeyD'); __key('Space'); __key('Space', true); __key('KeyD', true);
    out.st = F.st; out.moved = Math.hypot(G.tom.x - x0, 0);
    __run(0.2);
    out.hurt = G.tom.hurt - hurt0; out.counterOpen = LEDGER.game.fightx.counterOpen();
    while (F.st !== 'idle') LEDGER.tick(1 / 60);
    // the counter: a jab inside the window lands as a heavy blow
    P.x = G.tom.x; P.z = G.tom.z + 1.0; G.tom.ang = 0; f.st = 'guard'; f.t = 5;
    const h0 = P.hurt || 0; LEDGER.fight.input('light'); out.counterFlag = !!F.counter;
    __run(0.6); out.counterHurt = (P.hurt || 0) - h0;
    // a plain jab, later, for comparison (guard may stop it: try until one lands)
    let jab = 0;
    for (let i = 0; i < 12 && !jab; i++) { while (F.st !== 'idle' || F.stop > 0) LEDGER.tick(1 / 60); F.stam = 1; P.x = G.tom.x; P.z = G.tom.z + 1.0; G.tom.ang = 0; f.st = 'guard'; f.t = 5; const a = P.hurt || 0; F.counterUntil = 0; LEDGER.fight.input('light'); __run(0.6); jab = (P.hurt || 0) - a; if (P.hurt > 0.8) P.hurt = 0.2; }
    out.jabHurt = jab;
    out.cues = [...document.querySelectorAll('#bubbles .eye, #bubbles .mark')].length;
    LEDGER.fight.end();
    return out;
  });
  ok(slip.windup === 'windup' && slip.tell >= 0.45 - 1e-9 && slip.tell <= 0.9, `ER-FIGHT-02 his blow can be read before it lands (${slip.tell.toFixed(2)} s of wind-up)`);
  ok(slip.st === 'dodge' && slip.moved > 0.5 && slip.hurt === 0 && slip.counterOpen, `ER-DEFEND-01 a tap with a direction slips the blow to the side (${slip.moved.toFixed(2)} m): nothing lands, and the counter opens`);
  ok(slip.counterFlag && slip.counterHurt > slip.jabHurt * 1.5 && slip.jabHurt > 0, `ER-DEFEND-01 a jab inside the counter's window lands as a heavy blow (${slip.counterHurt.toFixed(2)} against a jab's ${slip.jabHurt.toFixed(2)})`);
  ok(slip.cues === 0, 'ER-DEFEND-02 no defence cue is drawn on screen');

  // ---- the hold: push into a wall, disarm
  const hold = await L(() => {
    const G = LEDGER.G, F = LEDGER.F, fx = LEDGER.game.fightx, out = {};
    // by the west side of Quay Street, the wall 1 m behind him
    if (F.on) LEDGER.fight.end();
    __put(-6.0, -40, -Math.PI / 2); const P = __man('lee', -7.0, -40, Math.PI / 2); LEDGER.fight.setOn([P]);
    const f = F.foes[0]; f.st = 'guard'; f.t = 9; P.x = -7.0; P.z = -40; G.tom.x = -6.0; G.tom.z = -40; G.tom.ang = -Math.PI / 2;
    out.held = fx.holdMan(); out.who = fx.holding(); out.st = f.st;
    const h0 = P.hurt || 0; out.push = fx.push(); out.hurt = (P.hurt || 0) - h0; out.after = f.st;
    // disarm: the same man with a knife in his hand
    __run(2.7); f.st = 'guard'; f.t = 9; P.x = G.tom.x - 1; P.z = G.tom.z; G.tom.ang = -Math.PI / 2; P.weapon = 'knife'; G.tom.weapon = null;
    out.held2 = fx.holdMan(); out.disarmed = fx.disarm(); out.his = P.weapon; out.toms = G.tom.weapon; out.armed = G.tom.armed;
    // held and left alone: he is let go after about 2 s
    __run(2.7); f.st = 'guard'; f.t = 9; P.x = G.tom.x - 1; P.z = G.tom.z; G.tom.ang = -Math.PI / 2;
    out.held3 = fx.holdMan(); __run(1.5); const mid = fx.holding(); __run(0.8); out.timed = mid === 'lee' && fx.holding() === null;
    LEDGER.fight.end(); G.tom.weapon = null;
    return out;
  });
  ok(hold.held && hold.who === 'lee' && hold.st === 'held' && hold.push === 'wall' && hold.hurt > 0.2 && hold.after === 'stagger', `A29 the grab holds a man; pushed into the wall behind him he is hurt (${hold.hurt.toFixed(2)}) and staggered`);
  ok(hold.held2 && hold.disarmed && hold.his === null && hold.toms === 'knife' && !hold.armed, 'A29 the disarm: what was in his hand is taken, and it is not out in Tom\'s until the held input');
  ok(hold.held3 && hold.timed, 'A29 a man held and left alone is let go after about 2 s');

  // ---- the weapon on a held input (ER-FIGHT-08)
  const weapon = await L(() => {
    const G = LEDGER.G, F = LEDGER.F, out = {};
    G.tom.weapon = 'cosh'; G.tom.armed = false;
    __fight(['lee']);
    LEDGER.fight.climb(); out.tap = G.tom.armed; // a tap of R no longer brings it out
    __key('Semicolon'); __run(0.2); out.short = G.tom.armed; __run(0.35); out.held = G.tom.armed; __key('Semicolon', true);
    LEDGER.fight.end(); G.tom.weapon = null; G.tom.armed = false;
    return out;
  });
  ok(!weapon.tap && !weapon.short && weapon.held, 'ER-FIGHT-08 a weapon comes out only on a held input: not on a tap of R, not on a touch of [;], out after [;] is held 0.4 s');

  // ---- the quiet blow (A23)
  const quiet = await L(() => {
    const G = LEDGER.G, fx = LEDGER.game.fightx, out = {};
    if (LEDGER.F.on) LEDGER.fight.end();
    G.t = 1 * 1440 + 23 * 60;
    for (const id in G.people) if (id !== 'lee') { G.people[id].gone = true; }
    // face to face: nothing happens (that is the ladder's business)
    __put(60, 30, 0); const P = __man('lee', 60, 31.1, Math.PI);
    out.faceToFace = fx.quietBlow();
    // from behind, unseen
    P.ang = 0; const n0 = G.events.length;
    __key('KeyJ'); __run(0.1);
    out.down = P.down; out.kind = G.events.length > n0 ? G.events[G.events.length - 1].kind : null;
    const m = P.mind.mem.find((x) => G.ev[x.e].kind === 'quiet_blow'); out.his = m ? { who: m.who, sure: m.sure } : null;
    out.fightOn = LEDGER.F.on;
    out.outForRealSeconds = (P.downT - G.t) * LEDGER.rules.time.realSecondsPerGameHour / 60;
    out.prompt = LEDGER.prompts().map((x) => x.text);
    // a woman is never struck this way
    const W = __man('brenda', 60, 35, 0); __put(60, 33.9, 0); out.woman = fx.quietBlow();
    for (const id in G.people) G.people[id].gone = false;
    return out;
  });
  ok(quiet.faceToFace === false && quiet.down && quiet.kind === 'quiet_blow' && !quiet.fightOn, 'A23 a fist from behind on a man who has not seen him knocks him out, with no fight and no prompt for the blow; face to face nothing happens');
  ok(quiet.his && quiet.his.who === 'man' && quiet.his.sure <= 0.2 && Math.abs(quiet.outForRealSeconds - 20) < 1 && quiet.woman === false, `A23 the man himself caught a shape at most (${JSON.stringify(quiet.his)}), is out about 20 s, and Tom never does it to a woman`);
  ok(quiet.prompt.some((p) => /pockets/.test(p)), 'A29 a man down can be searched: the prompt is there (' + quiet.prompt.join(' | ') + ')');
  const search = await L(() => {
    const G = LEDGER.G, n0 = G.events.length;
    __key('KeyE'); __run(3.5); const early = G.people.lee.searched; __run(0.8); __key('KeyE', true);
    return { early: !!early, done: !!G.people.lee.searched, kind: G.events.slice(n0).map((E) => E.kind) };
  });
  ok(!search.early && search.done && search.kind.includes('searched_man'), 'ER-SEARCH-02 the search of a man down completes with the use key held, in its table time (4 s), and is an act the town can see');

  // ---- a man in the water (ER-WATER-02)
  const water = await L(() => {
    const G = LEDGER.G, F = LEDGER.F, fx = LEDGER.game.fightx, out = {};
    G.people.lee.down = false; G.people.lee.searched = false; G.t = 1 * 1440 + 11 * 60;
    __put(30, 59.6, 0); const P = __man('lee', 30, 60.6, Math.PI); LEDGER.fight.setOn([P]);
    const f = F.foes[0]; f.st = 'guard'; f.t = 9; P.x = 30; P.z = 60.6; G.tom.x = 30; G.tom.z = 59.6; G.tom.ang = 0;
    out.edge = LEDGER.game.feel.inWater(30, 62.6);
    out.held = fx.holdMan(); out.push = fx.push();
    out.inWater = !!P.inWater; out.wet = fx.wet().length; out.kind = G.events[G.events.length - 1].kind;
    let secs = 0; while (P.inWater && secs < 70) { __run(1); secs++; }
    out.secs = secs; out.alive = !P.dead; out.dry = !LEDGER.game.feel.inWater(P.x, P.z); out.tomDry = !LEDGER.game.feel.inWater(G.tom.x, G.tom.z);
    if (F.on) LEDGER.fight.end();
    return out;
  });
  ok(water.edge && water.held && water.push === 'water' && water.inWater, 'A11 at the quay edge a held man pushed toward the water goes in (the edge is one of the street places)');
  ok(water.secs <= 60 && water.alive && water.dry && water.tomDry, `ER-WATER-02 he is out within 60 real seconds (${water.secs} s), alive, on dry ground; Tom is never in the water`);

  // ---- people step in; the police break it up
  const ends = await L(() => {
    const G = LEDGER.G, F = LEDGER.F, out = {};
    __fight(['lee'], 0, -60);
    __man('albert', 4, -58, 0); __man('wayne', -4, -58, 0); __man('hal', 3, -64, 0);
    F.clock = 29; F.foes[0].st = 'guard'; F.foes[0].t = 9; __run(0.1);
    out.steppedIn = !F.on && LEDGER.game.fightx.lastEnd().how;
    __fight(['lee'], 0, -60); out.police = LEDGER.game.fightx.brokenUp('police') && LEDGER.game.fightx.lastEnd().how;
    return out;
  });
  ok(ends.steppedIn === 'stepped in' && ends.police === 'police', `DESIGN 7 the five endings: backed off, ran, down (fight.js), and here people stepping in to a long fist fight (${ends.steppedIn}) and the police arriving (${ends.police})`);

  const faults = await L(() => LEDGER.game.faults.slice());
  ok(faults.length === 0, 'no fault inside any system' + (faults.length ? ': ' + faults[0] : ''));
  ok(h.errors.length === 0, 'no page errors' + (h.errors.length ? ': ' + h.errors[0] : ''));
} catch (e) {
  console.log('FAIL TEST FAIL ' + (e.stack || e));
  bad++;
}
await h.close();
console.log(bad ? `fightx: ${bad} FAIL` : 'PASS');
process.exit(bad ? 1 : 0);
