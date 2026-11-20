// LEDGER. Seeing: who can see Tom, how well, and what they make of him. Light, facing, distance and noise.
import { clamp, hyp, angDiff, smooth } from './util.js';
import { G, day, hour, tally } from './state.js';
import { KINDS } from './kinds.js';
import { NONE, mkEvent, logLine, link, remember } from './events.js';
import { ledgerSelf, ledgerSeen } from './ledger.js';
import { RULES } from './rules.js';
const LAD = RULES.ladder;

const TIME = RULES.time,
  SEE = RULES.seeing,
  NOISE = RULES.noise,
  WATCH = RULES.watching,
  NOTICE = RULES.noticing;

// ---------- time of day ----------
export function nightF(h = hour()) {
  if (h >= TIME.dayFullHour && h < TIME.duskStartsHour) return 0;
  if (h >= TIME.nightFullHour || h < TIME.dawnStartsHour) return 1;
  return h >= TIME.duskStartsHour
    ? smooth(TIME.duskStartsHour, TIME.nightFullHour, h)
    : 1 - smooth(TIME.dawnStartsHour, TIME.dayFullHour, h);
}

export const smallHours = (h = hour()) => h >= TIME.smallHoursFromHour || h < TIME.smallHoursUntilHour;

// ---------- the readable rules ----------
// Light sets the distance. Under a sodium lamp (L about 0.75) you are seen at 35 m; in a dark doorway (L about 0.1) at 6 m.
export function visRange(L) {
  return (
    (SEE.rangeInBlackMetres +
      SEE.rangeAddedByFullLightMetres * Math.pow(clamp(L, 0, 1), SEE.lightCurvePower)) *
    (1 - SEE.rainCutsRangeByShare * G.weather.rain) *
    (1 - SEE.mistAtNightCutsRangeByShare * G.weather.mist * nightF())
  );
}

// Noise depends on the hour. At 3 a.m. a footstep carries; at noon the street hides it; rain is cover.
export function hourNoise(h = hour()) {
  if (h >= NOISE.noonFromHour && h < NOISE.noonUntilHour) return NOISE.noonTimes;
  if (h < NOISE.deadOfNightUntilHour) return NOISE.deadOfNightTimes;
  if (h < NOISE.earlyUntilHour) return NOISE.earlyTimes;
  if (h >= NOISE.lateEveningFromHour) return NOISE.lateEveningTimes;
  return NOISE.otherwiseTimes;
}

export function noiseRadius(base) {
  return base * hourNoise() * (1 - NOISE.rainCutsByShare * G.weather.rain);
}

export function tomTarget() {
  const t = G.tom;
  const sx = t.inCar ? G.car.x : t.x,
    sz = t.inCar ? G.car.z : t.z;
  const L = G.env.lightAt(sx, sz, t.space);
  let base = t.inCar
    ? NOISE.cabIdlingMetres +
      NOISE.cabAddedAtSpeedMetres * Math.min(1, Math.abs(G.car.v) / NOISE.cabFullNoiseAtMetresPerSecond)
    : t.v < NOISE.stillBelowMetresPerSecond
      ? NOISE.standingMetres
      : t.run
        ? NOISE.runningMetres
        : NOISE.walkingMetres;
  base = Math.max(base, t.noiseP);
  t.light = L;
  t.noiseR = noiseRadius(base);
  return {
    x: sx,
    z: sz,
    space: t.space,
    light: L,
    noiseR: t.noiseR,
    coat: t.coat,
    inCar: t.inCar,
    lights: t.inCar && G.car.lights,
  };
}

// Where a person's eyes are. Someone at home sees only from their window, if they have one on the street.
export function eye(P) {
  if (P.space === 'home')
    return P.atWindow && P.win
      ? {
          x: P.win.x,
          z: P.win.z,
          ang: P.win.ang,
          fov: SEE.windowViewHalfAngleRadians,
          space: 'street',
          win: true,
        }
      : null;
  return { x: P.x, z: P.z, ang: P.ang, fov: SEE.viewHalfAngleRadians, space: P.space };
}

export function sense(P, T) {
  if (P.dead || P.gone || P.down) return NONE;
  if (!P.awake) {
    // asleep: only noise can reach them, at their window
    if (!P.win || T.space !== 'street') return NONE;
    const d = hyp(P.win.x, P.win.z, T.x, T.z);
    return { see: false, hear: d <= T.noiseR * NOISE.throughAWindowTimes, c: 0, d, asleep: true };
  }
  const e = eye(P);
  if (!e || e.space !== T.space) return NONE;
  const d = hyp(e.x, e.z, T.x, T.z);
  const hear = d <= T.noiseR * (e.win ? NOISE.throughAWindowTimes : 1);
  let range = visRange(T.light);
  if (T.lights) range = Math.max(range, SEE.headlampsSeenFromMetres);
  if (T.space !== 'street') range = Math.max(range, SEE.indoorsSeenFromMetres);
  let see = false,
    c = 0;
  if (d <= range) {
    const dir = Math.atan2(T.x - e.x, T.z - e.z);
    const off = Math.abs(angDiff(e.ang, dir));
    const close = d < SEE.closeByMetres && off < SEE.closeByViewHalfAngleRadians;
    if ((off < e.fov || close) && G.env.los(e.x, e.z, T.x, T.z)) {
      see = true;
      c = clamp(1 - d / range, SEE.leastClarity, 1);
    }
  }
  return { see, hear, c, d };
}

export const attached = (m) => m.who === 'tom' || m.who === 'owner';

export function knowsWho(P) {
  return !!P.mind.inh || P.mind.fam > SEE.knowsHimAboveFamiliarity;
}

export function faceScore(P, c, d, T) {
  let b = P.mind.fam * (SEE.faceBase + SEE.facePerClarity * c);
  if (T.coat && nightF() > SEE.coatHidesWhenNightAbove) b *= SEE.coatAtNightFaceTimes; // the runner's coat: harder to name at night
  if (T.inCar)
    b *=
      d < SEE.inCabCloseMetres && T.light > SEE.inCabLitAboveLight
        ? SEE.inCabCloseAndLitFaceTimes
        : SEE.inCabOtherwiseFaceTimes;
  return b;
}

export function identify(P, c, d, T) {
  const b = faceScore(P, c, d, T),
    k = knowsWho(P);
  if (b > SEE.namesHimAboveFace && k) return 'tom';
  if (b > SEE.placesHimAboveFace && k) return 'owner';
  return T.inCar ? 'cab' : T.coat ? 'coat' : 'man';
}

export function perceivers() {
  return G.named.concat(G.crowd);
}

// Tom only learns he was seen if the watcher was in front of him, in view and lit. This is all his Ledger gets.
export function tomNotices(P) {
  const t = G.tom,
    e = eye(P);
  if (!e || e.space !== t.space) return false;
  const tx = t.inCar ? G.car.x : t.x,
    tz = t.inCar ? G.car.z : t.z;
  const d = hyp(e.x, e.z, tx, tz);
  if (d > NOTICE.furthestMetres) return false;
  const facing = Math.abs(angDiff(G.env.camYaw(), Math.atan2(e.x - tx, e.z - tz)));
  if (d > NOTICE.mustFaceBeyondMetres && facing > NOTICE.facingHalfAngleRadians) return false;
  if (e.win && !P.winLit && d > NOTICE.darkWindowHidesBeyondMetres) return false; // a dark window keeps its secret
  const dark = G.env.lightAt(e.x, e.z, e.space) < NOTICE.darkBelowLight;
  if (d > NOTICE.darkFigureHidesBeyondMetres && dark && !e.win) return false;
  return G.env.los(tx, tz, e.x, e.z);
}

export function witness(P, E, s, T, fixedWho) {
  const face = faceScore(P, s.c, s.d, T);
  const who = fixedWho || identify(P, s.c, s.d, T);
  const k = KINDS[E.kind];
  const sure =
    clamp(SEE.sureBase + SEE.surePerClarity * s.c, 0, 1) * (who === 'tom' ? 1 : SEE.sureIfNotNamedTimes);
  const firstSight = !P.mind.by[E.id];
  tally('sightings');
  const r = remember(P, E, {
    src: 'saw',
    who,
    sure,
    heat: clamp(k.sev + SEE.heatAddedToSeverity, 0, 1),
    face,
  });
  if (!E.wit.includes(P.id)) E.wit.push(P.id);
  const gain = attached(r) ? SEE.familiarityPerWitnessedActIfKnown : SEE.familiarityPerWitnessedAct;
  P.mind.fam = clamp(P.mind.fam + gain * s.c, 0, 1);
  P.mind.look = Math.max(
    P.mind.look || 0,
    WATCH.lookAfterWitnessRealSeconds + WATCH.lookAddedPerSeverityRealSeconds * k.sev,
  );
  // Said with the body: a pause in the walk, or a step back. Once for one act: an act that goes on (being out
  // at night) is seen again and again, and must not hold a walker on the spot. G.played is real seconds.
  const rested = !(P.bodyAt > G.played - WATCH.pauseAgainAfterRealSeconds);
  if (firstSight && rested && !P.fight && !P.lad && s.d < WATCH.bodyReactsWithinMetres) {
    if (P.moving) {
      P.pauseT = WATCH.pauseInWalkRealSeconds + WATCH.pauseAddedPerSeverityRealSeconds * k.sev;
      P.bodyAt = G.played;
    } else if (
      (P.def.nerve == null ? LAD.nerveAssumed : P.def.nerve) < WATCH.stepBackIfNerveBelow &&
      (nightF() > WATCH.stepBackWhenNightAbove || k.crime) &&
      !P.keeper &&
      !P.chat
    ) {
      P.backT = WATCH.stepBackRealSeconds;
      P.bodyAt = G.played;
    }
  }
  if (tomNotices(P)) ledgerSeen(E, P, 'saw');
  if (G.hooks.sighted) G.hooks.sighted(P, E, r); // the game's real town is told (game/town.js)
  return r;
}

// Passive sightings: being somewhere, at some hour, looking some way.
export function sightingKind() {
  const t = G.tom,
    h = hour(),
    n = nightF(h);
  if (t.space !== 'street') return null;
  if (t.inCar) return smallHours(h) || t.carry === 'bag' ? 'cab_night' : 'cab_drive';
  if (t.carry === 'bag') return 'parcel';
  if (smallHours(h)) return 'night_out';
  if (t.coat && n < SEE.coatByDayWhenNightBelow) return 'coat_day';
  if (t.run && n > SEE.runningAtNightWhenNightAbove && t.v > SEE.runningFasterThanMetresPerSecond)
    return 'ran';
  return null;
}

function sightEvent(kind) {
  const key =
    kind + ':' + day() + ':' + Math.floor(hour() / SEE.sameSightingLastsGameHours) + ':' + G.tom.zone;
  let id = G.sightIdx[key];
  if (id && G.ev[id]) return G.ev[id];
  const E = mkEvent(kind, {});
  G.sightIdx[key] = E.id;
  if (!KINDS[kind].noself) ledgerSelf(E);
  return E;
}

export function perceiveTick(dt) {
  const T = tomTarget(),
    kind = sightingKind(),
    watch = [];
  const t = G.tom;
  t.noiseP = Math.max(0, t.noiseP - dt * NOISE.burstFadesMetresPerRealSecond);
  for (const P of perceivers()) {
    const m = P.mind,
      s = sense(P, T);
    if (m.look > 0) m.look -= dt;
    if (s.asleep) {
      if (s.hear && T.noiseR > NOISE.wakesASleeperAboveMetres) P.wake = 1;
      continue;
    }
    if (!s.see) {
      m.attn = Math.max(0, m.attn - dt * SEE.attentionFadesPerRealSecond);
      if (s.hear && !P.anon && T.noiseR > NOISE.remarkedInSmallHoursAboveMetres && smallHours()) {
        P.alert = { x: T.x, z: T.z, t: NOISE.alertLastsRealSeconds };
        if (!m.heardT || G.t - m.heardT > NOISE.sameNoiseRemarkedEveryGameMinutes) {
          m.heardT = G.t;
          const E = sightEvent('noise');
          tally('heard');
          remember(P, E, { src: 'heard', who: 'man', sure: NOISE.heardSure, heat: NOISE.heardHeat });
        }
      }
      continue;
    }
    const who = identify(P, s.c, s.d, T),
      noticed = tomNotices(P);
    watch.push({ P, c: s.c, who, noticed });
    G.stats.seenTicks++;
    m.attn +=
      dt *
      (SEE.attentionPerRealSecond + SEE.attentionPerRealSecondPerClarity * s.c) *
      (kind ? SEE.attentionFasterWhenRemarkableTimes : 1);
    if (m.attn < 1) continue;
    m.attn = 0;
    if (kind) {
      const E = sightEvent(kind),
        had = m.by[E.id];
      const r = witness(P, E, s, T);
      if (!had && attached(r)) logLine(`${P.def.name} saw: ${KINDS[kind].truth(E)}`, 'saw');
    } else if ((m.seenCool || 0) < G.t) {
      m.seenCool = G.t + SEE.plainSightingEveryGameMinutes;
      const known = who === 'tom' || who === 'owner';
      if (s.d < WATCH.looksOnlyWithinMetres)
        m.look = Math.max(
          m.look || 0,
          known ? WATCH.lookAtKnownManRealSeconds : WATCH.lookAtStrangerRealSeconds,
        ); // the head turns to him
      if (known) {
        m.fam = clamp(
          m.fam +
            SEE.familiarityPerPlainSightingIfKnown +
            SEE.familiarityPerPlainSightingIfKnownPerClarity * s.c,
          0,
          1,
        );
        m.last = { z: t.zone, t: G.t };
      } else
        m.fam = clamp(
          m.fam + SEE.familiarityPerPlainSighting + SEE.familiarityPerPlainSightingPerClarity * s.c,
          0,
          SEE.strangerFamiliarityStopsAt,
        );
      link(P);
    }
  }
  G.watch = watch;
}
