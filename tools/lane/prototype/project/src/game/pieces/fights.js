// LEDGER rule piece: fights. The ladder's eight rungs and what each shows the street, the other man's nerve (face,
// corners, backing), the odds, how a fight ends, condition without bars, weapon tiers, things that break, the fall
// rule (ruling 30 Oct), and a whole fight simulated from a seed so the rules can be held to their numbers:
// ER-FIGHT-01 (the melee sheet's bands), 02, 04, 05 (10,000 fights), 07 (skill beats mashing), 08. DESIGN section 7.
// Pure: plain data in, plain data out; chance only from the seed handed in. The game's own fight (fight.js) still
// runs its own code; this piece states the same rules from the same numbers for the port.
import { RULES } from '../../rules.js';
const L = RULES.ladder; // the prototype's fight numbers (rules.js)
export const TABLE = RULES.game.econ.fights; // the piece's own (game/tune/econ.js)

// A seeded generator: the same seed, the same fight.
export function rng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------- the ladder ----------
// Slots: 0 precursor, 1 draw, 2 act, 3 victim, 4 actor, 5 flight, 6 aftermath. Each rung is an act the town can catch.
const RUNGS = [
  null,
  { rung: 1, name: 'stare', kind: 'stare', slots: [0, 4], crime: 0 },
  { rung: 2, name: 'square up', kind: 'square_up', slots: [0, 3, 4], crime: 0 },
  { rung: 3, name: 'threaten', kind: 'threat', slots: [0, 2, 3, 4], crime: 1, heardMetres: L.threatNoiseCarriesMetres },
  { rung: 4, name: 'shove or grab', kind: 'shove', slots: [0, 2, 3, 4, 6], crime: 1 },
  { rung: 5, name: 'strike', kind: 'strike', slots: [0, 2, 3, 4, 5, 6], crime: 2, heardMetres: L.strikeNoiseCarriesMetres },
  { rung: 6, name: 'weapon out', kind: 'weapon_out', slots: [0, 1, 3, 4, 5], crime: 2, heardMetres: L.weaponOutNoiseCarriesMetres },
  { rung: 7, name: 'weapon used', kind: 'weapon_used', slots: [0, 1, 2, 3, 4, 5, 6], crime: 3, heardMetres: L.weaponUsedNoiseCarriesMetres },
  { rung: 8, name: 'kill', kind: 'kill', slots: [0, 1, 2, 3, 4, 5, 6], crime: 4, heardMetres: L.killNoiseCarriesMetres },
];
export const rung = (n) => RUNGS[n] || null;
export const rungs = () => RUNGS.slice(1);
// The pressure a rung puts on the other man.
export function pressure(n, x = {}) {
  const base = [0, L.pressureOfStare, L.pressureOfSquareUp, L.pressureOfThreat, L.pressureOfShove][Math.min(n, L.shoveRung)] || 0;
  return base + (x.armed ? L.pressureAddedWhenArmed : 0) - (x.hisAllies || 0) * L.pressureLostPerAlly - (x.tomHurt || 0) * L.pressureLostPerHurt + (x.menace || 0);
}
// His nerve on the day: his own, plus face (people watching), a wall at his back, somebody bigger behind him.
export function nerve(own, x = {}) {
  const face = Math.min(L.faceNerveAtMost, (x.watchers || 0) * L.faceNervePerWatcher);
  return (own == null ? L.nerveAssumed : own) + face + (x.cornered ? L.corneredNerveAdded : 0) + (x.backed ? L.backedNerveAdded : 0) + (x.lads ? L.ladsNerveAdded : 0);
}
// Fronted up at a rung: he gives way, stands, or (from the threat up) comes back at Tom.
export function answer(n, own, x = {}) {
  const p = pressure(n, x),
    nv = nerve(own, x);
  if (p > nv) return { gives: true, fights: false, pressure: p, nerve: nv };
  const fights = n >= L.shoveRung || (n >= L.threatRung && nv > L.fightsBackAtThreatAboveNerve && !!x.willSwing);
  return { gives: false, fights, pressure: p, nerve: nv };
}
// The odds, in the design's words.
export function odds(tomSide, otherSide) {
  const d = otherSide - tomSide;
  return d <= 0 ? (d < 0 ? 'his way' : 'a fair fight') : d === 1 ? 'deadly' : 'a beating';
}
// Tom's own line (QUESTIONS 2, built to the recommended answer): he will not lay hands on a woman, anyone of
// sixty or over, or the priest.
export function handsOff(p) {
  return p.sex === 'f' || (p.age || L.ageAssumedYears) >= L.handsOffFromAgeYears || !!p.priest;
}
// Weapon tiers: 0 fists, 1 things to hand (left behind), 2 carried, 3 firearms. What the town makes of a blow
// rises by tier; no number is shown.
const TO_HAND = { chair: L.chairDamageTimes, brick: L.brickDamageTimes, 'dustbin lid': L.dustbinLidDamageTimes, 'wheel brace': L.wheelBraceDamageTimes, 'cargo hook': L.cargoHookDamageTimes };
const CARRIED = { cosh: L.coshDamageTimes, 'flick knife': L.flickKnifeDamageTimes, knuckleduster: L.unknownWeaponDamageTimes, knife: L.flickKnifeDamageTimes, bat: L.wheelBraceDamageTimes };
const GUNS = ['pistol', 'revolver', 'shotgun'];
export function weapon(name, T = TABLE) {
  const tier = !name ? 0 : name in TO_HAND ? 1 : GUNS.includes(name) ? TABLE.tierCrimeLevel.length - 1 : 2;
  const times = !name ? 1 : TO_HAND[name] || CARRIED[name] || L.unknownWeaponDamageTimes;
  const breaks = { chair: L.chairBreaksAfterBlows, brick: L.brickBreaksAfterBlows, 'dustbin lid': L.dustbinLidBreaksAfterBlows }[name] || 0;
  return { tier, damageTimes: times, breaksAfterBlows: breaks, leftBehind: tier === 1, foundInASearch: tier >= 2, crime: T.tierCrimeLevel[tier], reads: T.tierReadsMenace[tier] };
}
// Condition without bars: what a man's hurt looks like.
export function condition(hurt, T = TABLE) {
  const w = T.conditionWordsAtHurt;
  return hurt < w[0] ? 'fresh' : hurt < w[1] ? 'breathing hard' : hurt < w[2] ? 'guard dropping, blood on his face' : hurt < w[3] ? 'limping, barely up' : 'down';
}
// The fall rule. Fists alone never kill. A fall against a kerb, a wall or a step within three seconds of a blow can.
// A car strike is never a blow under this rule.
export function fall(x, T = TABLE) {
  const hard = ['kerb', 'wall', 'step'].includes(x.landedOn);
  if (x.by === 'car') return { canKill: false, why: 'a car strike is never a blow under the fall rule' };
  if (x.who === 'tom') return { canKill: false, why: 'Tom cannot die' };
  if (!hard) return { canKill: false, why: 'he did not land on a kerb, a wall or a step' };
  if (!(x.secondsSinceBlow <= T.fallKillsWithinRealSecondsOfABlow)) return { canKill: false, why: 'no blow in the three seconds before the fall' };
  return { canKill: true, why: 'a fall against a ' + x.landedOn + ' after a blow' };
}
// Was this death allowed by his ruling? (The melee sheet's C7 count of breaks.)
export function deathBreaksRuling(d, T = TABLE) {
  if (d.who === 'tom') return true;
  if (d.cause === 'fall') return !fall({ who: d.who, by: d.by, landedOn: d.landedOn, secondsSinceBlow: d.secondsSinceBlow }, T).canKill;
  if (d.cause === 'weapon' || d.cause === 'shot' || d.cause === 'finished') return false; // a weapon used, or the separate decision afterwards
  return true; // fists alone, a car, anything else
}
// How a fight ends: one of five (DESIGN 7).
export function ending(s) {
  if (s.policeArrived) return 'the police arrive';
  if (s.peopleSteppedIn) return 'people step in';
  if (s.someoneDown) return 'someone goes down';
  if (s.someoneRan) return 'someone runs';
  return 'someone backs off';
}
// At most two men swing at once, their swings starting apart (ER-FIGHT-02, C8).
export function maySwing(now, swingStarts) {
  const live = swingStarts.filter((t) => now - t < L.foeHeavyWindUpRealSeconds + L.foeStrikeRealSeconds);
  if (live.length >= L.attackersAtOnceAtMost) return false;
  return live.every((t) => now - t >= L.swingStartsApartRealSecondsAtLeast);
}
// The melee sheet's bands against the table's own numbers (ER-FIGHT-01), by name.
export function bands(T = TABLE) {
  const within = (v, b) => v >= b[0] && v <= b[1];
  const rows = [
    ['C2 jab to contact', L.lightWindUpRealSeconds, T.jabBandRealSeconds],
    ['C2 heavy to contact', L.heavyWindUpRealSeconds, T.heavyBandRealSeconds],
    ['C2 heavy miss recovery', L.heavyMissRecoverRealSeconds, T.heavyMissBandRealSeconds],
    ['C3 hit-stop jab', L.hitStopLightRealSeconds, T.hitStopJabBandRealSeconds],
    ['C3 hit-stop heavy', L.hitStopHeavyRealSeconds, T.hitStopHeavyBandRealSeconds],
    ['C4 light reaction', L.lightStaggerRealSeconds, T.lightReactionBandRealSeconds],
    ['C4 heavy reaction', L.heavyStaggerRealSeconds, T.heavyReactionBandRealSeconds],
    ['C5 enemy heavy readable', L.foeHeavyWindUpRealSeconds, [T.readableBlowRealSecondsAtLeast, T.readableBlowRealSecondsAtMost]],
    ['C5 enemy jab readable', L.foeLightWindUpRealSeconds, [T.readableBlowRealSecondsAtLeast, T.readableBlowRealSecondsAtMost]],
    ['C8 gap between two swings', L.swingStartsApartRealSecondsAtLeast, [T.swingGapBandRealSecondsAtLeast, Infinity]],
    ['C8 men swinging at once', L.attackersAtOnceAtMost, [1, 2]],
    ['C11 jabs to empty', Math.ceil((1 - L.tooTiredBelowStamina) / L.lightStaminaCost), T.jabsToEmptyBand],
    ['C11 heavies to empty', Math.ceil((1 - L.tooTiredBelowStamina) / L.heavyStaminaCost), T.heaviesToEmptyBand],
    ['C11 empty to full', (1 - L.tooTiredBelowStamina) / L.staminaBackPerRealSecond + L.staminaRestsAfterSpendRealSeconds, T.emptyToFullBandRealSeconds],
    ['C12 chair', L.chairBreaksAfterBlows, T.chairBlowsBand],
    ['C12 brick', L.brickBreaksAfterBlows, T.brickBlowsBand],
    ['C15 heavies to put a man down', Math.ceil(L.foeHurtAtMost / L.heavyBlowHurts), T.heaviesToPutAManDownBand],
  ];
  const out = rows.map(([name, value, band]) => ({ name, value: Math.round(value * 1000) / 1000, ok: within(value, band) }));
  return { ok: out.every((r) => r.ok), rows: out, failed: out.filter((r) => !r.ok).map((r) => r.name) };
}

// ---------- a whole fight from a seed ----------
// o: { seed, style: 'patient' | 'masher' | 'plain', foes: [{ nerve, weapon? }] or a count, allies: n, tomWeapon,
//      hardEdgeNear: true | false | undefined (by chance), watched: bool }
// Tom's styles: patient guards or slips the blows he can read and hits back in the opening after; a masher throws
// jabs without stopping and never guards; plain is between the two.
export function simulate(o, T = TABLE) {
  const R = rng(o.seed == null ? 1 : o.seed),
    dt = T.simStepRealSeconds;
  const nFoes = typeof o.foes === 'number' ? o.foes : (o.foes || [{}]).length;
  const foes = [];
  for (let i = 0; i < nFoes; i++) {
    const f = (typeof o.foes === 'object' && o.foes[i]) || {};
    foes.push({ hurt: 0, nerve: nerve(f.nerve, { watchers: o.watched ? L.faceNerveAtMost / L.faceNervePerWatcher : 0 }), weapon: f.weapon || null, up: true, ran: false, next: L.foeFirstSwingAfterRealSecondsAtLeast + R() * (L.foeFirstSwingAfterRealSecondsAtMost - L.foeFirstSwingAfterRealSecondsAtLeast) + i * L.swingStartsApartRealSecondsAtLeast, swing: null, stag: 0, guard: 0, lastHit: -99 });
  }
  let allies = o.allies || 0; // a man at his side takes the second man (A16): he ties one foe up
  const tom = { hurt: 0, stam: 1, busy: 0, rest: 0, stag: 0, open: 0, blows: 0 };
  const reads = o.style === 'patient' ? T.patientReadsTellShare : o.style === 'masher' ? T.masherGuardsShare : T.plainReadsTellShare;
  const tw = weapon(o.tomWeapon, T);
  const edge = o.hardEdgeNear == null ? R() < T.hardEdgeNearChance : !!o.hardEdgeNear;
  const deaths = [],
    starts = [];
  let t = 0,
    counter = 0,
    queued = null;
  const live = () => foes.filter((f) => f.up && !f.ran);
  const tied = () => live().slice(0, Math.max(0, Math.min(allies, live().length - 1 + (allies > 0 && live().length === 1 ? 0 : 0))));
  while (t < T.simEndsAfterRealSeconds) {
    t += dt;
    const L_ = live();
    if (!L_.length) break;
    const busyWithAllies = new Set(allies > 0 ? L_.slice(L_.length - Math.min(allies, L_.length - 1)) : []);
    void tied;
    // Tom's breath
    if (tom.rest > 0) tom.rest -= dt;
    else tom.stam = Math.min(1, tom.stam + L.staminaBackPerRealSecond * dt);
    if (tom.stag > 0) tom.stag -= dt;
    if (tom.open > 0) tom.open -= dt;
    if (counter > 0) counter -= dt;
    // the other men
    for (const f of L_) {
      if (f.stag > 0) {
        f.stag -= dt;
        f.swing = null;
        f.next = Math.max(f.next, t + T.swingsAgainAfterAReactionRealSeconds);
        if (f.stag <= 0) f.guard = L.foeGuardAfterStaggerRealSecondsAtMost + T.guardHeldAfterAReactionRealSeconds; // he comes out of it with his hands up
        continue;
      }
      if (f.guard > 0) f.guard -= dt;
      if (busyWithAllies.has(f)) continue;
      if (f.swing) {
        if (t >= f.swing.lands) {
          const heavy = f.swing.heavy;
          f.swing = null;
          f.next = t + L.foeGuardAfterSwingRealSecondsAtLeast + R() * (L.foeGuardAfterSwingRealSecondsAtMost - L.foeGuardAfterSwingRealSecondsAtLeast) + (L_.length > 1 ? L.foeWaitsAddedWhenSeveralRealSeconds : 0);
          let dmg = (heavy ? L.foeHeavyBlowHurts : L.foeLightBlowHurts) * (f.weapon ? L.foeWeaponDamageTimes : 1);
          // he can read it (0.45 to 0.80 s of wind-up) and answer it, if he is free to and chooses to
          const canAnswer = tom.stag <= 0 && tom.busy <= dt && tom.stam > L.blockStaminaCostPerBlow;
          if (canAnswer && R() < reads / (1 + (L_.length - busyWithAllies.size - 1) * T.readingHarderPerExtraManShare)) {
            tom.stam -= L.blockStaminaCostPerBlow;
            dmg *= f.weapon ? 1 : L.blockLetsThroughShare;
            counter = L.foeGuardAfterSwingRealSecondsAtLeast; // the opening after a blocked or slipped blow
          } else if (tom.busy > 0 || tom.open > 0) dmg *= L.openToBlowDamageTimes;
          else tom.stag = L.tomStaggerRealSeconds;
          tom.hurt += dmg;
          if (dmg > L.foeLightBlowHurts * L.blockLetsThroughShare) queued = null;
        }
      } else if (t >= f.next && maySwing(t, starts)) {
        const heavy = R() < L.foeHeavyChance;
        f.swing = { heavy, lands: t + (heavy ? L.foeHeavyWindUpRealSeconds : L.foeLightWindUpRealSeconds) + L.foeStrikeRealSeconds };
        starts.push(t);
        if (starts.length > 8) starts.shift();
      }
    }
    if (tom.hurt >= L.tomHurtAtMost) break;
    // Tom
    if (tom.busy > 0) {
      tom.busy -= dt;
      if (tom.busy <= 0 && queued) {
        const q = queued,
          f = q.f;
        queued = null;
        if (f.up && !f.ran) {
          const up = f.guard > 0 ? (q.heavy ? T.guardUpStopsHeavyChance : T.guardUpStopsLightChance) : q.heavy ? L.guardStopsHeavyChance : L.guardStopsLightChance;
          const guarded = f.stag <= 0 && !f.swing && !q.counter && R() < up;
          if (!guarded) {
            let dmg = (q.heavy ? L.heavyBlowHurts : L.lightBlowHurts) * tw.damageTimes * (1 - L.hurtWeakensBlowsByShare * Math.min(1, tom.hurt)) * (q.counter ? T.counterAfterBlockDamageTimes : 1);
            if (q.tired) dmg *= T.tiredBlowDamageTimes;
            f.hurt += dmg;
            // a reaction is not started again by the next blow, and a jab does not stop a blow already on its way:
            // only a committed blow or a counter does (so trading jabs with a swinging man loses)
            if (f.stag <= 0 && (q.heavy || q.counter || !f.swing)) f.stag = q.heavy || q.counter ? L.heavyStaggerRealSeconds : L.lightStaggerRealSeconds;
            f.lastHit = t;
            tom.blows++;
            tom.busy = q.heavy ? L.heavyHitRecoverRealSeconds : L.lightHitRecoverRealSeconds;
            if (f.hurt >= L.foeHurtAtMost) {
              f.up = false;
              // the fall: only now, within moments of the blow, and only where there is something hard to land on
              if (edge && R() < T.fallAgainstHardEdgeChance && R() < T.fallOnHardEdgeKillsChance) deaths.push({ who: 'foe', cause: 'fall', by: tw.tier ? 'weapon' : 'fists', landedOn: ['kerb', 'wall', 'step'][Math.floor(R() * 3)], secondsSinceBlow: 0 });
            } else if (f.hurt >= L.foeFleesAboveHurt && f.nerve < L.foeFleesWhenHurtBelowNerve && R() < L.foeFleesWhenHurtChance) f.ran = true;
          } else {
            tom.busy = q.heavy ? L.heavyMissRecoverRealSeconds : L.lightMissRecoverRealSeconds;
            tom.open = tom.busy;
          }
        }
      }
    } else if (tom.stag <= 0) {
      const target = live().find((f) => !busyWithAllies.has(f)) || live()[0];
      if (target) {
        const tired = tom.stam < L.tooTiredBelowStamina;
        let go = false,
          heavy = false,
          isCounter = false;
        if (o.style === 'masher') go = true; // jab, jab, jab: tired or not
        else if (o.style === 'patient') {
          if (counter > 0 && !tired) (go = true), (heavy = true), (isCounter = true);
          else if (target.stag > L.lightWindUpRealSeconds && !tired) (go = true), (heavy = target.stag > L.heavyWindUpRealSeconds);
          else if (!target.swing && !target.guard && !tired && tom.stam > T.patientJabsAboveBreath) go = R() < dt * T.patientJabsPerRealSecond;
        } else if (!tired) (go = R() < dt * T.plainBlowsPerRealSecond), (heavy = R() < T.plainHeavyShare), (isCounter = counter > 0 && go);
        if (go) {
          const cost = heavy ? L.heavyStaminaCost : L.lightStaminaCost;
          tom.stam = Math.max(0, tom.stam - cost);
          tom.rest = L.staminaRestsAfterSpendRealSeconds;
          tom.busy = (heavy && !isCounter ? L.heavyWindUpRealSeconds : L.lightWindUpRealSeconds) * (tired ? T.tiredBlowSlowerTimes : 1) + L.strikeRealSeconds;
          queued = { f: target, heavy, counter: isCounter, tired };
          if (isCounter) counter = 0;
        }
      }
    }
  }
  const up = live(),
    beaten = tom.hurt >= L.tomHurtAtMost,
    down = foes.some((f) => !f.up),
    ran = foes.some((f) => f.ran);
  const winner = beaten ? 'foes' : !up.length ? 'tom' : 'none';
  return {
    winner,
    ending: ending({ someoneDown: beaten || down, someoneRan: !beaten && !down && ran, peopleSteppedIn: winner === 'none' }),
    seconds: Math.round(t * 100) / 100,
    tomBeaten: beaten,
    tomDied: false, // Tom cannot die
    tomCondition: condition(tom.hurt / L.tomHurtAtMost, T),
    blowsLanded: tom.blows,
    deaths,
  };
}
// Many fights from one seed: the counts the rules are held to.
export function simulateMany(n, seed, o = {}, T = TABLE) {
  const out = { fights: n, tomWins: 0, foesWin: 0, neither: 0, deaths: 0, deathsBreakingTheRuling: 0, tomDeaths: 0, endings: {}, longestSeconds: 0 };
  for (let i = 0; i < n; i++) {
    const r = simulate(Object.assign({}, o, { seed: (seed >>> 0) + i * 7919 }), T);
    if (r.winner === 'tom') out.tomWins++;
    else if (r.winner === 'foes') out.foesWin++;
    else out.neither++;
    out.endings[r.ending] = (out.endings[r.ending] || 0) + 1;
    out.longestSeconds = Math.max(out.longestSeconds, r.seconds);
    if (r.tomDied) out.tomDeaths++;
    for (const d of r.deaths) {
      out.deaths++;
      if (deathBreaksRuling(d, T)) out.deathsBreakingTheRuling++;
    }
  }
  out.tomWinsShare = Math.round((out.tomWins / n) * 1000) / 1000;
  return out;
}
// The rules as yes or no, for the cases file (each runs its own fights from the seed).
export function holds(rule, seed, T = TABLE) {
  const n = rule === 'ER-FIGHT-05' ? T.simulatedFights : T.simulatedFights / 10;
  if (rule === 'ER-FIGHT-05') {
    const a = simulateMany(n / 2, seed, { style: 'plain', foes: 1 }, T),
      b = simulateMany(n / 2, seed + 1, { style: 'patient', foes: 2, hardEdgeNear: true }, T);
    return { ok: a.deathsBreakingTheRuling + b.deathsBreakingTheRuling === 0 && a.tomDeaths + b.tomDeaths === 0, fights: n, deaths: a.deaths + b.deaths, deathsBreakingTheRuling: a.deathsBreakingTheRuling + b.deathsBreakingTheRuling, tomDeaths: 0 };
  }
  if (rule === 'ER-FIGHT-07') {
    const p = simulateMany(n, seed, { style: 'patient', foes: 1 }, T),
      m = simulateMany(n, seed, { style: 'masher', foes: 1 }, T);
    return { ok: p.tomWinsShare >= T.patientWinsShareAtLeast && m.tomWinsShare <= T.masherWinsShareAtMost, patient: p.tomWinsShare, masher: m.tomWinsShare };
  }
  if (rule === 'fair') {
    const a = simulateMany(n, seed, { style: 'plain', foes: 1 }, T);
    return { ok: a.tomWinsShare >= T.fairFightTomWinsShareAtLeast && a.tomWinsShare <= T.fairFightTomWinsShareAtMost, share: a.tomWinsShare };
  }
  if (rule === 'odds') {
    const two = simulateMany(n, seed, { style: 'plain', foes: 2 }, T),
      three = simulateMany(n, seed, { style: 'plain', foes: 3 }, T),
      sided = simulateMany(n, seed, { style: 'plain', foes: 2, allies: 1 }, T);
    return { ok: two.tomWinsShare <= T.twoOnOneTomWinsShareAtMost && three.tomWinsShare <= T.threeOnOneTomWinsShareAtMost && sided.tomWinsShare > two.tomWinsShare, two: two.tomWinsShare, three: three.tomWinsShare, twoWithAManAtHisSide: sided.tomWinsShare };
  }
  if (rule === 'ER-FIGHT-04') {
    const a = simulateMany(n, seed, { style: 'masher', foes: 3 }, T);
    return { ok: a.tomDeaths === 0 && a.longestSeconds <= T.simEndsAfterRealSeconds + T.simStepRealSeconds, tomDeaths: a.tomDeaths, beaten: a.foesWin };
  }
  return { ok: false, why: 'no such rule here' };
}

export const PIECE = {
  name: 'fights',
  fns: { rung, rungs, pressure, nerve, answer, odds, handsOff, weapon, condition, fall, deathBreaksRuling, ending, maySwing, bands, simulate, simulateMany, holds },
};
