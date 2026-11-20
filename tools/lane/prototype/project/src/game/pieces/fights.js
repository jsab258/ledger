// RULE PIECE: fights (DESIGN 7, A29). Pure. Unreal ports it and passes test/cases/fights.json.
// The ladder the street watches, the odds, the other man's nerve, how a fight ends, defence without icons, breath
// without a bar, and the fall rule. Tom cannot die. The feel (frames, camera, sound) is not here.
import { TUNE as T } from '../tune/fightx.js';

// A seeded generator handed in, never the clock: the same seed gives the same fight.
function rng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rung = (n) => T.rungs[n - 1] || null;
// What the odds are called, by count: fair, deadly, a beating (and the same the other way round).
function odds(hisSide, theirSide) {
  const d = theirSide - hisSide;
  return d <= -2 ? 'he has them cold' : d === -1 ? 'in his favour' : d === 0 ? 'fair' : d === 1 ? 'deadly' : 'a beating';
}
// At most two men swing at once, 0.4 s apart (ER-FIGHT-02): when may the nth attacker start his swing?
const swingAt = (n, firstAt) => (n < T.swingAtOnceAtMost ? firstAt + n * T.swingsApartRealSeconds : null);
// The other man's nerve: does he stand at this rung? A man watched stands longer, and so does a man cornered.
function stands(man, s) {
  const pressure = s.rung * T.nervePressurePerRung + Math.max(0, (s.against || 1) - (s.withHim || 1)) * T.nervePressurePerExtraManAgainst + (s.hurt || 0) * T.nervePressurePerHurt + (s.weaponShown ? T.nervePressureWeaponShown : 0);
  const nerve = man.nerve + (s.watched ? T.nerveWatchedStandsLongerBy : 0) + (s.cornered ? T.nerveCorneredStandsLongerBy : 0);
  return { stands: pressure < nerve, pressure: Math.round(pressure * 1000) / 1000, nerve: Math.round(nerve * 1000) / 1000 };
}
// Defence (A29): what an incoming blow does by what he was doing when it landed.
function incoming(blow, doing, sinceTellSeconds) {
  const read = sinceTellSeconds >= 0 && sinceTellSeconds <= T.tellRealSecondsAtMost;
  if (doing === 'slip' && read) return { hurt: 0, staggered: 0, opens: 'counter', through: false };
  if (doing === 'guard') {
    if (blow === 'weapon') return { hurt: T.hurt.weaponBlunt, staggered: 0, opens: null, through: true };
    if (blow === 'heavy') return { hurt: T.hurt.blockedHeavy, staggered: T.blockedHeavyStaggersRealSeconds, opens: 'counter', through: false };
    return { hurt: T.hurt.blockedFist, staggered: 0, opens: 'counter', through: false };
  }
  return { hurt: blow === 'weapon' ? T.hurt.weaponBlunt : blow === 'heavy' ? T.hurt.heavy : T.hurt.jab, staggered: 0, opens: null, through: false };
}
// A counter only lands after a slip or a block, inside the window (ER-DEFEND-01).
const counter = (after, sinceSeconds) => ({ lands: (after === 'slip' || after === 'guard') && sinceSeconds <= T.counterWindowRealSeconds, as: 'heavy', atSpeedOf: 'jab' });
// Breath: each fast jab spends it; empty, his blows are slower. No number is shown: he is heard and seen breathing.
function breath(fastJabs, restedSeconds) {
  const spent = Math.max(0, fastJabs - Math.floor((restedSeconds / T.breathBackRealSeconds) * T.breathEmptyAfterFastJabs));
  const empty = spent >= T.breathEmptyAfterFastJabs;
  return { empty, blowsTakeTimes: empty ? T.emptyBlowsSlowerTimes : 1, sign: empty ? 'breathing hard, guard dropping' : spent > T.breathEmptyAfterFastJabs / 2 ? 'breathing through his mouth' : null };
}
// The fall rule (ruling 30 Oct): fists alone never kill. A fall against a kerb, wall or step within 3 s of a blow
// can, rarely. A car strike is never such a blow; water never kills; in the boxing club the rule is off.
function fall(s, roll) {
  if (s.byCar || s.sparring || s.surface === 'water') return { dies: false, why: s.byCar ? 'a car never kills' : s.sparring ? 'gloves on' : 'water never kills' };
  if (!T.hardSurfaces.includes(s.surface)) return { dies: false, why: 'no hard edge' };
  if (!(s.secondsSinceBlow <= T.fallKillsWithinRealSecondsOfABlow)) return { dies: false, why: 'no blow in the 3 s before' };
  return { dies: roll < T.fallKillChance, why: 'a fall against a ' + s.surface };
}
// How a fight ends: one of five ways, and what each leaves. Tom is never dead (ER-FIGHT-04).
function ending(s) {
  if (s.policeArrived) return { how: 'the police arrive', tom: 'challenged', town: 'saw it broken up' };
  if (s.peopleStepIn) return { how: 'people step in', tom: 'free', town: 'pulled them apart' };
  if (s.tomDown) return { how: 'someone goes down', tom: 'beaten: comes round within a minute, robbed by chance', town: 'knows he lost', controlWithinRealSeconds: T.beatenBackInControlRealSecondsAtMost };
  if (s.otherDown) return { how: 'someone goes down', tom: 'standing', town: 'saw him put a man down' };
  if (s.someoneRan) return { how: 'someone runs', tom: s.tomRan ? 'ran' : 'may give chase', town: 'saw who ran' };
  return { how: 'someone backs off', tom: 'standing', town: 'saw who gave way' };
}
// Things to hand break; a carried weapon is seen, found and has to be got rid of.
const breaks = (thing, blows) => blows >= (T.breaksAfterBlows[thing] || 1);
function weaponOut(s) {
  // only on a held input (ER-FIGHT-08); drawn it cannot be undrawn unseen; watchers scatter
  if (!s.held) return { out: false, why: 'a tap never draws it' };
  return { out: true, rung: 6, watchersScatter: true, dialMoves: !!(s.gun && s.seenOrHeard) };
}
// No two fights running use the same mix of fighter types (ER-TYPES-01).
const mixKey = (types) => types.slice().sort().join('+');
const mixAllowed = (types, lastMix) => mixKey(types) !== lastMix && types.every((t) => t in T.types);
// The prototype's standing rule (QUESTIONS 2, awaiting his ruling): no hands on a woman, anyone of sixty or over, or the priest.
const mayLayHandsOn = (p) => !(p.woman || p.age >= T.refusesToLayHandsOnAge || p.priest);
// A whole fair one-on-one, simulated at the level of exchanges (for ER-FIGHT-05 and 07): style 'patient' reads the
// tell and counters; 'mashing' throws jabs until empty. Returns who went down and whether anyone died.
function simulate(seed, style, type = 'brawler', surface = 'open') {
  const r = rng(seed),
    F = T.types[type],
    M = T.sim;
  let tom = 0,
    man = 0,
    jabs = 0,
    n = 0,
    lastBlowOnMan = 99;
  while (tom < 1 && man < 1 && n++ < M.exchangesAtMost) {
    const hisSwing = r() < (F.rushes + M.hisSwingBase) / (1 + M.hisSwingBase); // he swings this exchange
    if (style === 'patient') {
      if (hisSwing) {
        const readIt = r() < M.patientReadsShare;
        if (readIt) {
          man += T.hurt.counter / F.takes;
          lastBlowOnMan = 0;
        } else tom += r() < M.hisBlowHeavyShare ? T.hurt.heavy : T.hurt.jab;
      } else if (r() > F.guards) {
        man += T.hurt.jab / F.takes;
        lastBlowOnMan = 0;
      }
      jabs = 0;
    } else {
      jabs++;
      const b = breath(jabs, 0);
      if (!b.empty && r() > F.guards) {
        man += T.hurt.jab / F.takes;
        lastBlowOnMan = 0;
      } else if (b.empty && r() < M.emptyRestsShare) jabs = 0; // he has to stop and breathe
      if (hisSwing) tom += (r() < M.hisBlowHeavyShare ? T.hurt.heavy : T.hurt.jab) * (b.empty ? M.emptyTakesTimes : M.mashingTakesTimes);
    }
    lastBlowOnMan += 1;
  }
  const tomWon = man >= 1 && tom < 1;
  const death = tomWon ? fall({ surface, secondsSinceBlow: lastBlowOnMan }, r()).dies : false;
  return { tomWon, tomDead: false, otherDead: death, exchanges: n };
}
// Many seeded fights at once: how many he won, how many deaths, and by what (the checks of ER-FIGHT-05 and 07).
function tally(fromSeed, count, style, type, surface) {
  let won = 0,
    deaths = 0,
    tomDeaths = 0;
  for (let i = 0; i < count; i++) {
    const f = simulate(fromSeed + i, style, type, surface);
    if (f.tomWon) won++;
    if (f.otherDead) deaths++;
    if (f.tomDead) tomDeaths++;
  }
  return { fights: count, wonShare: Math.round((won / count) * 100) / 100, deaths, tomDeaths };
}
export const PIECE = { name: 'fights', fns: { rung, odds, swingAt, stands, incoming, counter, breath, fall, ending, breaks, weaponOut, mixAllowed, mayLayHandsOn, simulate, tally } };
