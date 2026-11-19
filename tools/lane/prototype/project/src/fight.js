// The street's way: an escalation ladder Tom can stop on at any rung. Most of it ends before a blow.
// stare, square up, threaten, shove, strike, weapon out, weapon used, kill.
import { G } from './state.js';
import { hyp, clamp, chance, rnd, angDiff, pick } from './util.js';
import { act, logLine } from './events.js';
import { menaceTo } from './gossip.js';
import { meet } from './ledger.js';
import { blocked, PROPS } from './map.js';
import { sub, bubble, show, $, tomName } from './ui.js';
import { S } from './render/sync.js';
import { RULES } from './rules.js';
const LAD = RULES.ladder;

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
  stop: 0, // hit-stop left: both men held for a moment on contact (round 3)
  clock: 0, // real seconds since the fight began, for the drills' record
  lastFoeStart: -Infinity,
  tele: null, // set to [] to record the melee drills' events (tools/lane/melee_drills.py's format)
  watch: [],
};
// The melee drills' record: one event a moment, in the format tools/lane/melee_drills.py scores.
// a man's attack is over whenever he is no longer winding up or striking, for whatever reason (struck, fled, down)
function attackEnds() {
  for (const f of F.foes)
    if (f.att && f.st !== 'windup' && f.st !== 'strike') {
      f.att = false;
      tl('attack_end', { actor: who(f.P) });
    }
}
function tl(ev, o) {
  if (F.tele) F.tele.push(Object.assign({ t: F.clock, ev }, o || {}));
}
const who = (P) => P.id || P.def.name;
const SHOUT = ['Come here!', 'Have that!', 'Go on, then!', 'You asked for it!'];
const WATCH = ['Fight!', "Leave him, he's had enough!", "Somebody fetch the police!", 'Go on, lad!', 'Oi! Pack it in!'];
// People near a fight stop to look; the timid back off; some call it out. Their faces only: what they make of
// it stays the town's own business (the witness rules are not touched).
function watchers() {
  const t = G.tom;
  for (const P of G.named.concat(G.crowd)) {
    if (P.gone || P.dead || P.down || P.inCar || P.space !== t.space || P === F.T) continue;
    if (F.foes.find((f) => f.P === P) || F.watch.includes(P)) continue;
    if (hyp(P.x, P.z, t.x, t.z) > LAD.watchersWithinMetres) continue;
    if (P.moving || P.react || P.state === 'sit' || P.state === 'queueSit') continue; // walking, seated or already showing something: left be
    F.watch.push(P);
    P.react = (P.def.nerve ?? LAD.nerveAssumed) < LAD.watcherBacksOffBelowNerve ? 'cower' : 'stare';
    P.watchReact = P.react;
    P.reactT = LAD.watchersLookRealSeconds;
    if (chance(LAD.watcherShoutChance)) bubble(P, pick(WATCH));
  }
}
const RUNGS = ['', 'Stare', 'Square up', 'Threaten', 'Shove', 'Strike', 'Weapon out'];
const KIND = ['', 'stare', 'squareup', 'threat', 'shove'];
const WDMG = {
  cosh: LAD.coshDamageTimes,
  'flick knife': LAD.flickKnifeDamageTimes,
  brick: LAD.brickDamageTimes,
  chair: LAD.chairDamageTimes,
  'wheel brace': LAD.wheelBraceDamageTimes,
  'cargo hook': LAD.cargoHookDamageTimes,
  'dustbin lid': LAD.dustbinLidDamageTimes,
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
// round 4: what a man says when he will not be shown up in front of folk, or when he is put against a wall
const FACE = [
  "Not in front of this lot, you don't.",
  "Everybody's looking, son. I'm not crawling to you.",
  "In the street? With them watching? Go on, then.",
];
// round 5: a debtor with someone bigger behind him (Lee: Cammack's lads have offered him easier money, his card) stands
const BACKED = ["Cammack's lot said I'd not be on my own. So go on.", "I've got friends now. Bigger than Mickey's lot ever were."];
const CORNER = ["You've got me against a wall. Big mistake.", 'Nowhere to go, have I? Right.'];
// round 4: improvised things break (melee sheet C12); a wheel brace or a cargo hook, like a pipe, does not
const BREAKS = {
  chair: LAD.chairBreaksAfterBlows,
  brick: LAD.brickBreaksAfterBlows,
  'dustbin lid': LAD.dustbinLidBreaksAfterBlows,
};
const SINGLE = { chair: 1, 'dustbin lid': 1 };
// round 4: Tom picks a thing up outside a fight (the G prompt): remembered so that it can break later
export function carried(p) {
  F.wProp = p;
  p.wHits = 0;
}
const BROKEN = { chair: 'The chair goes to pieces.', brick: 'The brick crumbles in his hand.', 'dustbin lid': 'The lid buckles and he drops it.' };
// round 4: the things on the street a man can snatch up (for the drills)
export const handProps = () => PROPS.filter((p) => p.hand);
// round 4: folk near enough to see a man backed down: each one makes backing down cost him more
export function faceOf(P, al) {
  let n = 0;
  for (const Q of G.named.concat(G.crowd)) {
    if (Q === P || Q.gone || Q.dead || Q.down || Q.inCar || Q.space !== P.space || Q.space === 'home') continue;
    if (al && al.includes(Q)) continue;
    if (hyp(Q.x, Q.z, P.x, P.z) > LAD.faceWatchersWithinMetres) continue;
    n++;
  }
  return Math.min(LAD.faceNerveAtMost, n * LAD.faceNervePerWatcher);
}
// Tom will not lay hands on women, on anyone of sixty or over, or on the priest. The ladder stops at a threat for them.
const soft = (P) =>
  P.def.sex === 'f' ||
  P.def.frail ||
  (P.def.age || LAD.ageAssumedYears) >= LAD.handsOffFromAgeYears ||
  P.id === 'walsh';

// Round 6 (the gate, ER-INPUT-02): the prompt names the person ahead and in view. Of the people in reach and
// within about 30 degrees of his facing, it is the one most nearly straight ahead; distance only settles a near
// tie, and a named or marked person wins over a stranger about as far off his facing. A choice once made is held a
// moment (targetHeldRealSeconds) unless another is clearly better, so the prompt does not flicker between two.
const HELD = { P: null, cand: null, since: 0, x: 0, z: 0, ang: 0 };
export function target() {
  const t = G.tom;
  const score = (P) => {
    if (P.gone || P.dead || P.down || P.inCar || P.space !== t.space || P.space === 'home') return null;
    const d = hyp(P.x, P.z, t.x, t.z);
    if (d > LAD.targetWithinMetres) return null;
    const off = Math.abs(angDiff(t.ang, Math.atan2(P.x - t.x, P.z - t.z)));
    if (off > LAD.targetWithinFacingRadians) return null;
    // someone with their back to him counts as a little further off than someone facing him: of two people on
    // one spot, it is the one looking at him
    const away = Math.abs(angDiff(P.ang || 0, Math.atan2(t.x - P.x, t.z - P.z))) / Math.PI;
    return (
      off +
      d * LAD.targetMetreCountsAsRadians +
      away * LAD.targetBackTurnedCountsAsRadians -
      (P.anon && !P.mark ? 0 : LAD.targetNamedPreferredByRadians)
    );
  };
  let best = null,
    bs = Infinity;
  for (const P of G.named.concat(G.crowd)) {
    const sc = score(P);
    if (sc === null || sc > bs) continue; // on a dead tie the later one, as before round 6
    bs = sc;
    best = P;
  }
  // put somewhere else at a stroke (a door, a test): a new place, a new choice, nothing held
  const jumped =
    hyp(t.x, t.z, HELD.x, HELD.z) > LAD.targetHeldWithinMetres ||
    Math.abs(angDiff(t.ang, HELD.ang)) > LAD.targetHeldWithinRadians;
  HELD.x = t.x;
  HELD.z = t.z;
  HELD.ang = t.ang;
  const hs = HELD.P && HELD.P !== best && !jumped ? score(HELD.P) : null;
  if (best && hs !== null && hs - bs < LAD.targetHeldUnlessBetterByRadians) {
    // the one in hand is still about as good: it stays until the other has been better for a moment
    if (HELD.cand !== best) {
      HELD.cand = best;
      HELD.since = G.played;
    }
    if (G.played - HELD.since < LAD.targetHeldRealSeconds) return HELD.P;
  }
  HELD.P = best;
  HELD.cand = null;
  return best;
}
function allies(P) {
  const out = [];
  for (const Q of G.crowd.concat(G.named)) {
    if (Q === P || Q.gone || Q.down || Q.dead || Q.space !== P.space) continue;
    if (hyp(Q.x, Q.z, P.x, P.z) > LAD.alliesWithinMetres) continue;
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
  F.face = 0;
  F.standWhy = '';
  F.wHits = 0;
  // round 4: the name Tom carries as he steps up. Each rung's own pressure already prices that rung, so the
  // stare, threat and shove of this one fronting-up are not counted a second time as his name grows mid-ladder
  // (they were: a threat and a shove added 0.24, and no debtor ever stood).
  F.menace0 = menaceTo(P);
  P.hold = true;
  P.route = null;
  P.moving = false;
  meet(P);
  climb();
}
function mood(P, m) {
  P.react = m;
  P.reactT = LAD.moodShowsRealSeconds;
}
export function climb() {
  if (!F.on) return;
  const P = F.T,
    t = G.tom,
    m = P.mind,
    d = P.def;
  if (F.rung >= LAD.strikeRung) {
    if (F.rung === LAD.strikeRung && t.weapon && !t.armed) drawWeapon();
    return;
  }
  const next = F.rung + 1;
  if (next >= LAD.shoveRung && soft(P)) {
    const al = allies(P).filter((q) => !soft(q));
    if (!al.length) {
      sub('No. Not ' + (d.sex === 'f' ? 'her' : 'him') + '. Not with your hands.', '', 'over', 3);
      return;
    }
    F.rung = LAD.strikeRung;
    G.stats.fights++;
    sub("Right. You've done it now.", tomName(al[0]));
    F.proxy = true;
    startFight(al[0], true);
    ladderUI();
    return; // his minder steps in; the old man is never touched
  }
  F.rung = next;
  G.stats.fights += next === LAD.strikeRung ? 1 : 0;
  P.ang = Math.atan2(t.x - P.x, t.z - P.z);
  if (next === LAD.strikeRung) {
    startFight(P, true);
    ladderUI();
    return;
  }
  S.tomAnim.mode = ['stand', 'stare', 'square', 'point', 'shove'][next];
  F.animT = next === LAD.shoveRung ? LAD.shoveAnimRealSeconds : 0;
  act(KIND[next], { target: P.id, noiseR: next >= LAD.threatRung ? LAD.threatNoiseCarriesMetres : 0 });
  if (next >= LAD.threatRung && G.hooks.sfx) G.hooks.sfx('shout');
  if (d.police && next >= LAD.shoveRung) {
    G.story.flags.assaultPolice = 1;
    sub('That is assault on a police officer.', tomName(P), 'face');
    if (G.hooks.arrestNow) G.hooks.arrestNow(P);
    end();
    return;
  }
  const al = allies(P),
    pressure =
      [0, LAD.pressureOfStare, LAD.pressureOfSquareUp, LAD.pressureOfThreat, LAD.pressureOfShove][next] +
      F.menace0 +
      (t.armed ? LAD.pressureAddedWhenArmed : 0) -
      al.length * LAD.pressureLostPerAlly -
      t.hurt * LAD.pressureLostPerHurt;
  let cornered = false;
  if (next === LAD.shoveRung) {
    const dx = P.x - t.x,
      dz = P.z - t.z,
      l = Math.hypot(dx, dz) || 1;
    const nx = P.x + (dx / l) * LAD.shovePushesMetres,
      nz = P.z + (dz / l) * LAD.shovePushesMetres;
    if (!blocked(nx, nz)) {
      P.x = nx;
      P.z = nz;
    } else {
      // shoved back into a wall: it shows; round 4: with nowhere to go he is likelier to come off it swinging
      cornered = true;
      sub('Back into the wall.', '', 'over', LAD.wallLineRealSeconds);
      if (G.hooks.sfx) G.hooks.sfx('thud');
      if (G.hooks.shake) G.hooks.shake(LAD.wallSlamShake);
    }
  }
  const backed = d.backed ? LAD.backedNerveAdded : 0,
    nerve0 = (d.nerve ?? LAD.nerveAssumed) + (P.lad ? LAD.ladsNerveAdded : 0) + backed,
    face = faceOf(P, al),
    corner = cornered ? LAD.corneredNerveAdded : 0;
  F.face = face;
  F.last = { rung: next, pressure, nerve: nerve0, face, corner, backed, allies: al.length, menace: F.menace0 };
  if (pressure > nerve0 + face + corner) {
    m.fear = clamp(m.fear + LAD.fearAddedPerRungWhenYielding * next, 0, 1);
    m.regard = clamp(m.regard - LAD.regardLostPerRungWhenYielding * next, -1, 1);
    mood(P, next >= LAD.threatRung ? 'cower' : 'stand');
    const line = pick(YIELD[next]);
    if (next > 1) sub(line, tomName(P));
    else bubble(P, line);
    F.yielded = true;
    F.standWhy = '';
    if (F.demand && next >= 2 && G.hooks.yielded) G.hooks.yielded(P, F.demand, next);
  } else {
    F.yielded = false;
    mood(P, next >= 2 ? 'square' : 'stare');
    // round 4: say why he stands when the corner or the watchers tipped it, so the player can read it
    const why =
      pressure > nerve0 + face
        ? 'corner'
        : pressure > nerve0 && next >= 2
          ? 'face'
          : backed && pressure > nerve0 - backed && next >= 2
            ? 'backed'
            : '';
    F.standWhy = why;
    sub(
      pick(why === 'corner' ? CORNER : why === 'face' ? FACE : why === 'backed' ? BACKED : STAND[next]),
      tomName(P),
    );
    if (why) tl('stands', { actor: who(P), why });
    if (
      next === LAD.shoveRung ||
      (next === LAD.threatRung &&
        (d.nerve ?? LAD.nerveAssumed) > LAD.fightsBackAtThreatAboveNerve &&
        (P.lad || P.yardLad) &&
        chance(LAD.fightsBackAtThreatChance))
    ) {
      startFight(P, false);
    }
  }
  ladderUI();
}
export function backDown() {
  if (!F.on) return;
  if (F.foes.some((f) => f.st !== 'down' && f.st !== 'flee') && F.rung >= LAD.strikeRung) {
    sub('You step off. They may not let you.', '', 'over', 2.5);
    F.rung = LAD.shoveRung;
  }
  end(F.foes.some((f) => f.st !== 'down' && f.st !== 'flee'));
}
function drawWeapon() {
  const t = G.tom;
  if (!t.weapon) return;
  t.armed = true;
  F.rung = LAD.weaponOutRung;
  act('weapon_out', { target: F.T.id, weapon: t.weapon, noiseR: LAD.weaponOutNoiseCarriesMetres });
  for (const f of F.foes) {
    if (f.st === 'down') continue;
    if (
      LAD.weaponOutPressure + menaceTo(f.P) >
      (f.P.def.nerve ?? LAD.nerveAssumed) + LAD.weaponOutNerveMargin
    ) {
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
  P.hurry = LAD.fleeHurryTimes;
  P.override = {
    where: P.def.sched ? 'home' : 'off',
    act: 'sleep',
    until: G.t + LAD.fleeStaysAwayGameMinutes,
  };
  P.goalKey = '';
  P.mind.fear = clamp(P.mind.fear + LAD.fleeFearAdded, 0, 1);
}
function startFight(P, tomFirst) {
  F.rung = Math.max(F.rung, LAD.strikeRung);
  S.tomAnim.mode = 'guard';
  F.st = 'idle';
  F.t = 0;
  F.stop = 0;
  F.clock = 0;
  F.lastFoeStart = -Infinity;
  const add = (Q) => {
    if (F.foes.find((f) => f.P === Q) || soft(Q)) return;
    Q.hold = true;
    Q.route = null;
    Q.moving = false;
    Q.fight = { mode: 'guard' };
    F.foes.push({
      P: Q,
      st: 'guard',
      t: rnd(LAD.foeFirstMoveAfterRealSecondsAtLeast, LAD.foeFirstMoveAfterRealSecondsAtMost),
      cd: rnd(LAD.foeFirstSwingAfterRealSecondsAtLeast, LAD.foeFirstSwingAfterRealSecondsAtMost),
    });
  };
  add(P);
  for (const Q of allies(P)) add(Q);
  if (F.T && F.T !== P) for (const Q of allies(F.T)) add(Q);
  if (!tomFirst) {
    act('set_on', {
      target: P.id,
      noiseR: LAD.setOnNoiseCarriesMetres,
      name: F.foes.length > 1 ? P.def.name + ' and ' + (F.foes.length - 1) + ' more' : P.def.name,
    });
  }
  if (G.hooks.sfx) G.hooks.sfx('thud');
  watchers();
}
// Others can start on Tom (Cammack's lads, late on).
export function setOn(list) {
  if (F.on) return;
  F.wHits = 0;
  F.on = true;
  F.settled = false;
  F.proxy = false;
  F.T = list[0];
  F.rung = LAD.shoveRung;
  F.demand = null;
  F.struck = false;
  F.usedW = false;
  F.foes = [];
  startFight(list[0], false);
  for (const Q of list.slice(1)) {
    Q.hold = true;
    Q.route = null;
    Q.fight = { mode: 'guard' };
    if (!F.foes.find((f) => f.P === Q))
      F.foes.push({
        P: Q,
        st: 'guard',
        t: rnd(LAD.ladsFirstMoveAfterRealSecondsAtLeast, LAD.ladsFirstMoveAfterRealSecondsAtMost),
        cd: rnd(1, 2),
      });
  }
  ladderUI();
}
export function input(kind) {
  if (!F.on || F.rung < LAD.strikeRung) return;
  const t = G.tom;
  if (kind === 'finish') return finish();
  if (F.st !== 'idle' && F.st !== 'block') return;
  if (kind === 'light' || kind === 'heavy') {
    if (F.stam < LAD.tooTiredBelowStamina) {
      if (G.hooks.sfx) G.hooks.sfx('tick');
      return;
    }
    const action = kind === 'heavy' ? 'heavy' : 'jab';
    tl('input', { actor: 'player', action });
    F.st = kind === 'heavy' ? 'heavyUp' : 'windup';
    F.t = kind === 'heavy' ? LAD.heavyWindUpRealSeconds : LAD.lightWindUpRealSeconds;
    F.heavy = kind === 'heavy';
    F.stam -= kind === 'heavy' ? LAD.heavyStaminaCost : LAD.lightStaminaCost;
    F.rest = LAD.staminaRestsAfterSpendRealSeconds;
    tl('hit_start', { actor: 'player', action, weapon: t.armed ? t.weapon : 'fists' });
    tl('stamina', { actor: 'player', value: F.stam });
    if (F.stam < LAD.tooTiredBelowStamina) tl('stamina_empty', { actor: 'player' }); // too tired to swing counts as empty
  } else if (kind === 'dodge') {
    if (F.cool > 0) return;
    const bx = t.x - Math.sin(t.ang) * LAD.dodgeBackMetres,
      bz = t.z - Math.cos(t.ang) * LAD.dodgeBackMetres;
    if (!blocked(bx, bz)) {
      t.x = bx;
      t.z = bz;
    }
    F.st = 'dodge';
    F.t = LAD.dodgeRealSeconds;
    tl('input', { actor: 'player', action: 'dodge' });
    tl('dodge_start', { actor: 'player' });
    tl('invuln_start', { actor: 'player' });
    F.cool = LAD.dodgeCoolDownRealSeconds;
  }
}
// round 4: snatch up whatever is to hand mid-fight (G): it takes a moment, and he is open while he does it
export function grab() {
  if (!F.on || F.rung < LAD.strikeRung) return false;
  if (F.st !== 'idle' && F.st !== 'block') return false;
  const t = G.tom;
  let best = null,
    bd = Infinity;
  for (const p of PROPS) {
    if (!p.hand || p.broken || p.hand === (t.armed ? t.weapon : null)) continue;
    const d = hyp(t.x, t.z, p.x, p.z) - p.r;
    if (d < LAD.grabReachMetres && d < bd) {
      bd = d;
      best = p;
    }
  }
  if (!best) {
    sub('Nothing to hand here.', '', 'over', LAD.grabLineRealSeconds);
    return false;
  }
  F.st = 'grab';
  F.t = LAD.grabRealSeconds;
  F.grabbing = best;
  tl('input', { actor: 'player', action: 'grab' });
  tl('grab_start', { actor: 'player', weapon: best.hand });
  return true;
}
function breakWeapon() {
  const t = G.tom,
    w = t.weapon;
  if (F.wProp && SINGLE[F.wProp.hand]) F.wProp.broken = true; // a skip or a scrap heap has more where that came from
  F.wProp = null;
  t.weapon = null;
  t.armed = false;
  F.rung = LAD.strikeRung;
  F.wHits = 0;
  tl('weapon_break', { actor: 'player', weapon: w });
  sub(BROKEN[w] || 'It breaks.', '', 'over', LAD.grabLineRealSeconds);
  if (G.hooks.sfx) G.hooks.sfx('thud');
  ladderUI();
}
export function block(on) {
  if (!F.on || F.rung < LAD.strikeRung) return;
  if (on && F.st === 'idle') {
    F.st = 'block';
    tl('input', { actor: 'player', action: 'block' });
    tl('guard_up', { actor: 'player' });
  }
  else if (!on && F.st === 'block') F.st = 'idle';
}
function hurtFoe(f, dmg, heavy) {
  const P = f.P,
    t = G.tom;
  // knocked back: into a wall if one is close behind him
  const kx = P.x - t.x,
    kz = P.z - t.z,
    kl = Math.hypot(kx, kz) || 1,
    wall =
      blocked(P.x + (kx / kl) * LAD.blowKnocksBackMetres, P.z + (kz / kl) * LAD.blowKnocksBackMetres) ||
      blocked(P.x + (kx / kl) * LAD.wallBehindWithinMetres, P.z + (kz / kl) * LAD.wallBehindWithinMetres);
  if (wall) dmg += LAD.wallSlamHurts;
  P.hurt = clamp((P.hurt || 0) + dmg, 0, LAD.foeHurtAtMost);
  if (heavy || wall || f.st !== 'windup') {
    f.st = 'stagger';
    f.t = wall ? LAD.wallSlamStaggerRealSeconds : heavy ? LAD.heavyStaggerRealSeconds : LAD.lightStaggerRealSeconds;
    P.fight.mode = 'stagger';
    tl('stagger_start', { actor: who(P), severity: heavy || wall ? 'heavy' : 'light' });
  } // a light one does not stop a man already swinging
  if (wall) {
    tl('fall_hazard', { actor: who(P), surface: 'wall' });
    sub('Into the wall.', '', 'over', LAD.wallLineRealSeconds);
    if (G.hooks.sfx) G.hooks.sfx('thud');
    if (G.hooks.shake) G.hooks.shake(LAD.wallSlamShake);
  } else if (heavy && G.hooks.shake) G.hooks.shake(LAD.hitShakeHeavy);
  if (!F.struck) {
    F.struck = true;
    act('strike', {
      target: P.anon ? undefined : P.id,
      name: P.def.name,
      noiseR: LAD.strikeNoiseCarriesMetres,
    });
  }
  if (t.armed && !F.usedW) {
    F.usedW = true;
    act('weapon_used', { target: P.id, weapon: t.weapon, noiseR: LAD.weaponUsedNoiseCarriesMetres });
  }
  P.mind.fear = clamp(P.mind.fear + LAD.fearAddedPerBlow, 0, 1);
  P.mind.regard = clamp(P.mind.regard - LAD.regardLostPerBlow, -1, 1);
  if (G.hooks.sfx) G.hooks.sfx('hit');
  if (G.hooks.blood && (t.armed || heavy)) G.hooks.blood(P.x, P.z);
  const dx = P.x - t.x,
    dz = P.z - t.z,
    l = Math.hypot(dx, dz) || 1,
    nx = P.x + (dx / l) * LAD.blowKnocksBackMetres,
    nz = P.z + (dz / l) * LAD.blowKnocksBackMetres;
  if (!blocked(nx, nz)) {
    P.x = nx;
    P.z = nz;
  }
  if (!f.hitOnce && P.hurt < 1) {
    f.hitOnce = 1;
    if ((P.def.nerve ?? LAD.nerveAssumed) < LAD.fleesWhenHitBelowNerve && chance(LAD.fleesWhenHitChance)) {
      f.st = 'flee';
      flee(P);
      sub('All right! All right!', tomName(P));
      return;
    }
  }
  if (P.hurt >= 1) {
    f.st = 'down';
    P.down = true;
    tl('knockdown', { actor: who(P) });
    P.fight = null;
    sub("He's down.", '', 'over', 2);
    for (const g of F.foes)
      if (
        g !== f &&
        g.st !== 'down' &&
        (g.P.def.nerve ?? LAD.nerveAssumed) < LAD.othersFleeBelowNerve &&
        chance(LAD.othersFleeChance)
      ) {
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
  act('kill', {
    target: P.anon ? undefined : P.id,
    name: P.def.name,
    weapon: t.weapon,
    noiseR: LAD.killNoiseCarriesMetres,
  });
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
  F.clock += dt;
  if (F.stop > 0) {
    // hit-stop: both men held on the blow
    F.stop -= dt;
    if (F.stop <= 0) tl('hitstop_end', { actor: 'player' });
    return;
  }
  attackEnds();
  if (F.rung < LAD.strikeRung) {
    if (F.animT > 0) {
      F.animT -= dt;
      if (F.animT <= 0) S.tomAnim.mode = 'square';
    }
    if (dT > LAD.ladderEndsBeyondMetres || T.gone) end();
    return;
  }
  F.rest = Math.max(0, (F.rest || 0) - dt);
  const was0 = F.stam;
  F.stam = clamp(
    F.stam +
      dt * (F.st === 'block' ? -LAD.blockStaminaCostPerRealSecond : F.rest > 0 ? 0 : LAD.staminaBackPerRealSecond),
    0,
    1,
  );
  if (was0 < 1 && F.stam >= 1) tl('stamina', { actor: 'player', value: 1 });
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
  if (near && nd < LAD.turnsToFoeWithinMetres && F.st !== 'dodge')
    t.ang += clamp(
      angDiff(t.ang, Math.atan2(near.P.x - t.x, near.P.z - t.z)),
      -LAD.tomTurnsRadiansPerRealSecond * dt,
      LAD.tomTurnsRadiansPerRealSecond * dt,
    );
  // Tom's swing
  if (F.st === 'windup' || F.st === 'heavyUp') {
    S.tomAnim.mode = F.heavy ? 'heavy' : 'windup';
    F.t -= dt;
    if (F.t <= 0) {
      F.st = 'strike';
      F.t = LAD.strikeRealSeconds;
      S.tomAnim.mode = 'strike';
      const hit =
        near &&
        nd < LAD.tomReachMetres &&
        Math.abs(angDiff(t.ang, Math.atan2(near.P.x - t.x, near.P.z - t.z))) < LAD.tomHitsWithinFacingRadians;
      if (
        hit &&
        !(near.st === 'guard' && chance(F.heavy ? LAD.guardStopsHeavyChance : LAD.guardStopsLightChance))
      ) {
        F.stop = t.armed ? LAD.hitStopWeaponRealSeconds : F.heavy ? LAD.hitStopHeavyRealSeconds : LAD.hitStopLightRealSeconds;
        tl('hit_contact', { actor: 'player', target: who(near.P), action: F.heavy ? 'heavy' : 'jab', weapon: t.armed ? t.weapon : 'fists' });
        tl('hitstop_start', { actor: 'player' });
        hurtFoe(
          near,
          (F.heavy ? LAD.heavyBlowHurts : LAD.lightBlowHurts) *
            (t.armed ? WDMG[t.weapon] || LAD.unknownWeaponDamageTimes : 1) *
            (1 - t.hurt * LAD.hurtWeakensBlowsByShare),
          F.heavy,
        );
        F.rec = F.heavy ? LAD.heavyHitRecoverRealSeconds : LAD.lightHitRecoverRealSeconds;
        if (t.armed && BREAKS[t.weapon]) {
          // the blows are counted on the thing itself, so a chair carried from one fight to the next keeps its count
          const w = F.wProp && F.wProp.hand === t.weapon ? F.wProp : F;
          w.wHits = (w.wHits || 0) + 1;
          if (w.wHits >= BREAKS[t.weapon]) breakWeapon();
        }
      } else {
        F.rec = F.heavy ? LAD.heavyMissRecoverRealSeconds : LAD.lightMissRecoverRealSeconds;
        F.open = F.rec;
        if (hit) tl('guarded', { actor: who(near.P), against: 'player' }); // the man's guard stopped Tom's blow
        tl('miss', { actor: 'player' });
        if (hit && G.hooks.sfx) G.hooks.sfx('block');
      } // a miss leaves you open
    }
  } else if (F.st === 'grab') {
    S.tomAnim.mode = 'guard';
    F.t -= dt;
    if (F.t <= 0) {
      const p = F.grabbing;
      F.grabbing = null;
      F.st = 'idle';
      if (p) {
        if (t.weapon && t.weapon !== p.hand) sub('He lets the ' + t.weapon + ' fall.', '', 'over', LAD.grabLineRealSeconds);
        p.wHits = 0;
        t.weapon = p.hand;
        t.armed = false;
        F.wProp = p;
        F.wHits = 0;
        tl('grab_end', { actor: 'player', weapon: p.hand });
        drawWeapon();
        sub('A ' + p.hand + ', snatched up.', '', 'over', LAD.grabLineRealSeconds);
      }
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
      tl(F.st === 'recover' ? 'recovery_end' : F.st === 'dodge' ? 'dodge_end' : 'stagger_end', { actor: 'player' });
      if (F.st === 'dodge') tl('invuln_end', { actor: 'player' });
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
    P.ang += clamp(
      angDiff(P.ang, a),
      -LAD.foeTurnsRadiansPerRealSecond * dt,
      LAD.foeTurnsRadiansPerRealSecond * dt,
    );
    f.t -= dt;
    k++;
    if (f.st === 'stagger') {
      if (f.t <= 0) {
        tl('stagger_end', { actor: who(P) });
        f.st = 'guard';
        f.t = rnd(LAD.foeGuardAfterStaggerRealSecondsAtLeast, LAD.foeGuardAfterStaggerRealSecondsAtMost);
        P.fight.mode = 'guard';
        if (
          (P.hurt || 0) > LAD.foeFleesAboveHurt &&
          (P.def.nerve ?? LAD.nerveAssumed) < LAD.foeFleesWhenHurtBelowNerve &&
          chance(LAD.foeFleesWhenHurtChance)
        ) {
          f.st = 'flee';
          flee(P);
        }
      }
      continue;
    }
    if (d > LAD.foeClosesBeyondMetres) {
      const sp = LAD.foeClosesMetresPerRealSecond * dt,
        off = k * LAD.foesSpreadRadians - LAD.foesSpreadRadians,
        tx = t.x + Math.sin(a + Math.PI + off) * LAD.foeStandsOffMetres,
        tz = t.z + Math.cos(a + Math.PI + off) * LAD.foeStandsOffMetres,
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
        if (!blocked(nx, nz, LAD.foeBodyRadiusMetres)) {
          P.x = nx;
          P.z = nz;
          break;
        }
      }
      P.moving = true;
      P.v = LAD.foeClosesMetresPerRealSecond;
      if (f.st !== 'guard') {
        f.st = 'guard';
        P.fight.mode = 'guard';
      }
      continue;
    }
    P.moving = false;
    if (f.st === 'guard' && f.t <= 0) {
      // attack tickets: at most two men swinging at once, their swings started a beat apart
      const swinging = live.filter((g) => g.st === 'windup' || g.st === 'strike').length;
      if (swinging >= LAD.attackersAtOnceAtMost || F.clock - F.lastFoeStart < LAD.swingStartsApartRealSecondsAtLeast) {
        f.t = LAD.swingStartsApartRealSecondsAtLeast - Math.max(0, F.clock - F.lastFoeStart) + dt;
        continue;
      }
      F.lastFoeStart = F.clock;
      f.st = 'windup';
      f.heavy = chance(LAD.foeHeavyChance);
      f.t = f.heavy ? LAD.foeHeavyWindUpRealSeconds : LAD.foeLightWindUpRealSeconds;
      P.fight.mode = f.heavy ? 'heavy' : 'windup';
      tl('attack_start', { actor: who(P) });
      f.att = true;
      tl('hit_start', { actor: who(P), action: f.heavy ? 'heavy' : 'jab', weapon: P.weapon || 'fists' });
      tl('telegraph_start', { actor: who(P), action: f.heavy ? 'heavy' : 'jab' });
      if (f.heavy && chance(LAD.foeShoutsBeforeHeavyChance)) {
        bubble(P, pick(SHOUT), LAD.shoutShowsRealSeconds);
        if (G.hooks.sfx) G.hooks.sfx('shout');
        tl('sound', { actor: who(P), kind: 'shout' });
      }
    } // a readable wind-up, and with a heavy one often a shout
    else if (f.st === 'windup' && f.t <= 0) {
      f.st = 'strike';
      f.t = LAD.foeStrikeRealSeconds;
      P.fight.mode = 'strike';
      if (d < LAD.foeReachMetres && F.st !== 'dodge') {
        let dmg =
          (f.heavy ? LAD.foeHeavyBlowHurts : LAD.foeLightBlowHurts) *
          (P.weapon ? LAD.foeWeaponDamageTimes : 1) *
          (1 - (P.hurt || 0) * LAD.hurtWeakensBlowsByShare);
        const facing =
          Math.abs(angDiff(t.ang, Math.atan2(P.x - t.x, P.z - t.z))) < LAD.blockWorksWithinFacingRadians;
        tl(F.st === 'block' && facing ? 'block' : 'hit_contact', { actor: who(P), target: 'player', action: f.heavy ? 'heavy' : 'jab' });
        if (F.st === 'block' && facing) {
          dmg *=
            t.weapon === 'dustbin lid' && t.armed ? LAD.lidBlockLetsThroughShare : LAD.blockLetsThroughShare;
          F.stam -= LAD.blockStaminaCostPerBlow;
          if (G.hooks.sfx) G.hooks.sfx('block');
        } else {
          if (F.open > 0) dmg *= LAD.openToBlowDamageTimes;
          F.st = 'stagger';
          F.t = LAD.tomStaggerRealSeconds;
          if (G.hooks.sfx) G.hooks.sfx('hit');
          if (G.hooks.shake) G.hooks.shake(0.25);
        }
        t.hurt = clamp(t.hurt + dmg, 0, LAD.tomHurtAtMost);
        t.noiseP = LAD.beingHitNoiseCarriesMetres;
      }
    } else if (f.st === 'strike' && f.t <= 0) {
      f.st = 'guard';
      f.t =
        rnd(LAD.foeGuardAfterSwingRealSecondsAtLeast, LAD.foeGuardAfterSwingRealSecondsAtMost) +
        (live.length > 1 ? LAD.foeWaitsAddedWhenSeveralRealSeconds : 0);
      P.fight.mode = 'guard';
    }
  }
  if (t.hurt >= 1) {
    act('beaten', { noiseR: LAD.beatenNoiseCarriesMetres });
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
        F.T.mind.fear = clamp(F.T.mind.fear + LAD.yieldFearAddedAtBlows, 0, 1);
        F.T.react = 'cower';
        F.T.reactT = LAD.cowerShowsRealSeconds;
      }
      G.hooks.yielded(F.T, F.demand, LAD.strikeRung);
    }
    ladderUI(any && t.armed);
    if (!any || nd > LAD.armedStandoffWithinMetres || !t.armed) {
      F.endT = (F.endT || 0) + dt;
      if (F.endT > (any && t.armed ? LAD.armedStandoffEndsAfterRealSeconds : LAD.fightEndsAfterRealSeconds))
        end();
    }
  } else if (nd > LAD.walkedAwayBeyondMetres) end(true);
}
export function end(hostile) {
  for (const f of F.foes) {
    const P = f.P;
    P.fight = null;
    P.hold = false;
    P.moving = false;
    if (P.down && !P.dead) {
      P.downT = G.t + LAD.downForGameMinutes;
    } else if (!P.dead) {
      P.mind.fear = clamp(P.mind.fear + LAD.fearAddedAfterFight, 0, 1);
      if (!hostile || f.st === 'flee') {
        P.goalKey = '';
      }
    }
  }
  if (F.T && !F.T.down) {
    F.T.hold = false;
    F.T.goalKey = '';
  }
  for (const f of F.foes) if (f.att) f.st = 'over';
  attackEnds();
  for (const P of F.watch)
    if (P.react === P.watchReact) {
      P.react = null;
      P.reactT = 0;
    }
  F.watch = [];
  F.stop = 0;
  F.on = false;
  F.proxy = false;
  F.foes = [];
  F.rung = 0;
  F.endT = 0;
  F.st = 'idle';
  F.grabbing = null;
  if (!G.tom.weapon || !F.wProp || F.wProp.hand !== G.tom.weapon) F.wProp = null; // still carried: keep it for the next fight
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
      P.hurt = LAD.hurtAfterGettingUp;
      P.hurry = LAD.hurryAfterGettingUpTimes;
      P.override = {
        where: P.def.sched ? 'home' : 'off',
        act: 'sleep',
        until: G.t + LAD.goesHomeAfterBeatingGameMinutes,
      };
      P.goalKey = '';
    }
    if (P.hurt > 0 && !P.down) P.hurt = Math.max(0, P.hurt - LAD.foeHurtHealsPerTick);
  }
}
function ladderUI(canFinish) {
  const el = $('ladder');
  show('ladder', true);
  const t = G.tom;
  el.innerHTML =
    `<div class="h">${F.rung >= LAD.strikeRung ? 'IT HAS COME TO BLOWS' : 'FRONTING UP'}: ${tomName(F.T)}</div>` +
    RUNGS.slice(1)
      .map(
        (r, i) =>
          `<div class="r ${i + 1 === F.rung ? 'on' : i + 1 < F.rung ? 'done' : ''}">${i + 1}. ${r}${i === 5 ? (t.weapon ? ' (' + t.weapon + ')' : ' (none carried)') : ''}</div>`,
      )
      .join('') +
    `<div class="k">${F.rung < LAD.strikeRung ? '[R] step up  ·  [X] walk away' : '[LMB/J] hit, hold for heavy · [RMB/K] block · [Space] step back · [G] grab what is to hand · [X] break off' + (t.weapon && !t.armed ? ' · [R] weapon out' : '') + (canFinish ? '<br><b>[V] use it on a man who is down. This cannot be undone.</b>' : '')}</div>`;
}
