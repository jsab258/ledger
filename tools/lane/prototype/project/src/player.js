// Tom: keyboard, mouse and touch; walking, doors, the cab, the coat; the third-person camera.
import { G, hour } from './state.js';
import { hyp, clamp, angDiff, pick } from './util.js';
import { blocked, ROOMS, roomPos, PROPS, BLD, WALLS, groundY, roomSightBlocked, bigThingAt, thinThingAt } from './map.js';
import { inRect } from './util.js';
import { nightF } from './seeing.js';

import { BARKS } from './cast.js';
import { ui, key as uiKey, setPrompts, sub, bubble, tomName, show , choose, scene } from './ui.js';
import { F, frontUp, climb, backDown, input as fightInput, block as fightBlock, target, grab as fightGrab, carried as fightCarried } from './fight.js';
import { stepCar, nearCar, exitPoint, footSolid, footClear, clearGround, vehicleAt } from './drive.js';
import { hotspots, beatFor } from './scenes.js';
import { fareAccept } from './fares.js';
import { startTalk } from './talk.js';
import { setInside } from './render/effects.js';
import { AT_ONCE } from './talk_lines.js';
import { RULES } from './rules.js';
import { gameKey, gameCarPrompts, freshLine } from './game/index.js';
const SHOPS = RULES.shops;
const PADS = RULES.pad;
const LAD = RULES.ladder;
const TOMS = RULES.tom;
const STORY = RULES.story;

export const keys = {},
  cam = {
    yaw: Math.PI,
    pitch: 0.3,
    dist: 5.4,
    px: 0,
    py: 3,
    pz: 0,
    tx: 0,
    ty: 1.5,
    tz: 0,
    idle: 9,
    shake: 0,
  };
const touch = { x: 0, y: 0, on: false, run: false };
// Round 6 (the gate): what a pad is holding now. The frame loop reads the pad (main.js padStep) and writes it here;
// its buttons come through onKey like keys. x, y: the left stick (y forward). cx, cy: the right stick. gas, brake:
// the triggers, 0 to 1.
export const pad = { x: 0, y: 0, cx: 0, cy: 0, gas: 0, brake: 0, hb: false };
// what the hands are doing that a save does not hold: how far Tom is into his stride, a press made a moment early,
// how long he has pushed at something without moving
const feel = { stride: 0, wx: 0, wz: 0, sp: 0, early: null, stuck: 0 };
let mdown = 0,
  mbtn = -1,
  lastP = 0,
  prompts = [],
  locked = false,
  camera = null,
  canvasEl = null;
const HOURS = {
  caff: [SHOPS.caffOpensAtHour, SHOPS.caffShutsAtHour],
  fish: [SHOPS.fishOpensAtHour, SHOPS.fishShutsAtHour],
  laund: [SHOPS.launderetteOpensAtHour, SHOPS.launderetteShutsAtHour],
  grocer: [SHOPS.grocerOpensAtHour, SHOPS.grocerShutsAtHour],
  tangs: [SHOPS.chipShopOpensAtHour, SHOPS.chipShopShutsAtHour],
  news: [SHOPS.newsagentOpensAtHour, SHOPS.newsagentShutsAtHour],
  iron: [SHOPS.ironmongerOpensAtHour, SHOPS.ironmongerShutsAtHour],
  tearoom: [SHOPS.tearoomOpensAtHour, SHOPS.tearoomShutsAtHour],
  rita: [SHOPS.ritasOpensAtHour, SHOPS.ritasShutsAtHour],
  chandler: [SHOPS.chandlerOpensAtHour, SHOPS.chandlerShutsAtHour],
  coin: [SHOPS.coinShopOpensAtHour, SHOPS.coinShopShutsAtHour],
  chapel: [SHOPS.chapelOpensAtHour, SHOPS.chapelShutsAtHour],
  harbour: [SHOPS.harbourOpensAtHour, SHOPS.harbourShutsAtHour],
};
const isOpen = (id) => {
  const o = HOURS[id];
  if (!o) return true;
  const h = hour();
  return h >= o[0] && h < o[1];
};

export function initPlayer(cv, cameraObj) {
  camera = cameraObj;
  canvasEl = cv;
  addEventListener('keydown', (e) => {
    // typing is for talk and for the settings: a typing box swallows the keys only while its own page is open (a box
    // left in focus behind a shut page took the move keys with it)
    if (
      e.target &&
      e.target.tagName === 'INPUT' &&
      ui.modal &&
      !['Enter', 'Escape', 'Tab', 'ArrowUp', 'ArrowDown', 'F2'].includes(e.code)
    )
      return;
    if (
      e.code === 'Tab' ||
      e.code === 'F2' ||
      (e.target && e.target.tagName === 'INPUT' && e.code.startsWith('Arrow'))
    )
      e.preventDefault();
    if (e.repeat && !['KeyZ'].includes(e.code)) {
      keys[e.code] = true;
      return;
    }
    keys[e.code] = true;
    if (ui.pad) {
      ui.pad = false; // round 6: back on the keys, the prompts show the keys again
      ui.pk = null;
    }
    onKey(e.code);
    if (['Space', 'ArrowUp', 'ArrowDown'].includes(e.code) && e.target.tagName !== 'INPUT')
      e.preventDefault();
  });
  addEventListener('keyup', (e) => {
    keys[e.code] = false;
    if (e.code === 'KeyK') fightBlock(false);
  });
  addEventListener('blur', () => {
    for (const k in keys) keys[k] = false;
  });
  cv.addEventListener('mousedown', (e) => {
    if (ui.modal || G.story.phase !== 'play') return;
    mdown = performance.now();
    mbtn = e.button;
    if (F.on && F.rung >= LAD.strikeRung) {
      if (e.button === 2) fightBlock(true);
    }
    if (!locked && cv.requestPointerLock && !G.settings.touch) {
      try {
        const p = cv.requestPointerLock();
        if (p && p.catch) p.catch(() => {});
      } catch (err) {
        /* refused */
      }
    }
  });
  addEventListener('mouseup', (e) => {
    if (mbtn === 2) fightBlock(false);
    if (mbtn === 0 && F.on && F.rung >= LAD.strikeRung && !ui.modal)
      fightInput(performance.now() - mdown > LAD.heavyWhenHeldRealMilliseconds ? 'heavy' : 'light');
    mbtn = -1;
  });
  addEventListener('mousemove', (e) => {
    if (ui.modal || G.story.phase !== 'play') return;
    if (locked || mbtn >= 0) {
      cam.yaw -= e.movementX * 0.0028 * G.settings.sens;
      cam.pitch = clamp(
        cam.pitch + e.movementY * 0.0022 * G.settings.sens * (G.settings.invertY ? -1 : 1),
        -0.12,
        1.15,
      );
      cam.idle = 0;
    }
  });
  cv.addEventListener('contextmenu', (e) => e.preventDefault());
  cv.addEventListener(
    'wheel',
    (e) => {
      cam.dist = clamp(cam.dist + Math.sign(e.deltaY) * 0.5, 2.6, 9);
    },
    { passive: true },
  );
  document.addEventListener('pointerlockchange', () => {
    locked = document.pointerLockElement === cv;
  });
  initTouch(cv);
}
export const unlock = () => {
  if (locked && document.exitPointerLock) document.exitPointerLock();
};
// One key, as the keyboard sends it. The test hook comes through here too, so it takes the same path.
export function onKey(code) {
  if (G.story.phase !== 'play' || ui.shot) return; // nothing is his to do while the ferry comes in (Escape there ends the shot: main.js)
  if (uiKey(code)) return;
  if (code === 'Escape' || code === 'KeyP') {
    unlock();
    if (ui.hooks.pause) ui.hooks.pause();
    return;
  }
  if (code === 'KeyL') {
    // L, and only L, opens the Ledger. Tab means the suggested lines in a talk and nothing else.
    unlock();
    if (ui.hooks.ledger) ui.hooks.ledger('keyboard');
    return;
  }
  if (G.paused) return;
  if (gameKey(code)) return; // the whole game's systems may take a key first (game/core.js)
  // the hands-on run's fault: E moves a talk on and E goes through a door, so the press that ended a talk at a
  // doorway took him in and out. The use key rests for a moment after a written scene ends.
  if (code === 'KeyE' && ui.sceneEndedAt != null && G.played - ui.sceneEndedAt >= 0 && G.played - ui.sceneEndedAt < RULES.game.feel.useKeyRestsAfterASceneRealSeconds) return;
  if (code === 'KeyE') useKey('E');
  else if (code === 'KeyT') useKey('T');
  else if (code === 'KeyF') carKey();
  else if (code === 'KeyQ') {
    const P = target();
    if (P && !G.tom.inCar) frontUp(P);
  } else if (code === 'KeyR') {
    if (F.on) climb();
  } else if (code === 'KeyX') backDown();
  else if (code === 'KeyC') coat();
  else if (code === 'KeyG') {
    // round 4: in a fight, G snatches up whatever is to hand
    if (F.on && F.rung >= LAD.strikeRung) fightGrab();
    else useKey('G');
  }
  else if (code === 'KeyY') fareAccept();
  else if (code === 'KeyJ') fightInput('light');
  else if (code === 'KeyU') fightInput('heavy');
  else if (code === 'KeyK') fightBlock(true);
  else if (code === 'KeyV') fightInput('finish');
  else if (code === 'Space') {
    if (F.on && F.rung >= LAD.strikeRung) fightInput('dodge');
  }
}
function coat() {
  const t = G.tom;
  if (!t.hasCoat || t.inCar) return;
  t.coat = !t.coat;
  sub(
    t.coat
      ? "Mickey's coat. Collar up. Harder to name after dark; a strange thing to wear at noon."
      : 'Coat off, over your arm.',
    '',
    'over',
    3.5,
  );
  if (G.hooks.sfx) G.hooks.sfx('paper');
}
function carKey(again) {
  const t = G.tom,
    c = G.car;
  if (F.on) return;
  const early = () => {
    if (!again) feel.early = { k: 'F', t: TOMS.earlyPressCountsRealSeconds }; // round 6: a press a moment early still counts
  };
  if (t.inCar) {
    if (Math.abs(c.v) > TOMS.cabLeftBelowMetresPerSecond) return early();
    const [x, z] = exitPoint();
    t.inCar = false;
    t.x = x;
    t.z = z;
    t.v = 0;
    feel.early = null;
    if (G.hooks.sfx) G.hooks.sfx('cardoor');
    return;
  }
  if (t.space !== 'street' || !nearCar(TOMS.cabWithinMetres)) return early();
  if (!c.keys) return again ? null : sub('Locked. The keys will be in the office.', '', 'over');
  t.inCar = true;
  c.v = 0;
  cam.idle = 9;
  feel.early = null;
  if (G.hooks.sfx) G.hooks.sfx('cardoor');
}
export function enterRoom(id, quiet) {
  const t = G.tom,
    r = ROOMS[id];
  const [x, z] = roomPos(id, r.mat[0], r.mat[1] - 0.9);
  t.space = id;
  t.x = x;
  t.z = z;
  t.ang = Math.PI;
  t.inCar = false;
  setInside(r);
  ui.roomName = r.name;
  cam.yaw = Math.PI;
  cam.pitch = 0.62;
  cam.dist = 6.4;
  snapCam();
  if (!quiet && G.hooks.sfx) G.hooks.sfx('door');
  if (G.hooks.ambience) G.hooks.ambience(id);
  if (id === 'boarding' && (hour() >= TOMS.landladyHearsFromHour || hour() < TOMS.landladyHearsUntilHour)) {
    const S = G.people.sylvia;
    if (S && S.space === 'home') {
      S.wake = 1;
      sub("The stair creaks. Mrs Rennison's door stands an inch open.", '', 'over', 4);
    }
  }
}
export function leaveRoom(exit2) {
  const t = G.tom,
    r = ROOMS[t.space];
  if (!r) return;
  if (r.upFrom) {
    // the one-shot: a room up a stair is left down the stair, into the room below
    enterRoom(r.upFrom, true);
    const [sx, sz] = roomPos(r.upFrom, r.stair[0] - 0.9, r.stair[1] - 0.5);
    t.x = sx;
    t.z = sz;
    t.ang = -1.57;
    cam.yaw = -1.57;
    snapCam();
    if (G.hooks.sfx) G.hooks.sfx('stair');
    return;
  }
  const s = exit2 ? r.exit2.street : r.street;
  t.space = 'street';
  t.x = s[0];
  t.z = s[1];
  t.ang = s[2];
  setInside(null);
  ui.roomName = null;
  cam.yaw = s[2];
  cam.pitch = 0.3;
  cam.dist = 5.4;
  snapCam();
  if (G.hooks.sfx) G.hooks.sfx('door');
  if (G.hooks.ambience) G.hooks.ambience(null);
}
export function buildPrompts() {
  const t = G.tom,
    out = [];
  if (ui.modal || G.paused) return out;
  if (t.inCar) {
    if (Math.abs(G.car.v) < TOMS.cabLeftBelowMetresPerSecond) out.push({ k: 'E', t: 'Get out', run: () => carKey() });
    if (G.story.fare && G.story.fare.st === 'offer')
      out.push({ k: 'Y', t: 'Take the fare', run: fareAccept });
    gameCarPrompts(out);
    return out;
  }
  if (F.on) return out;
  for (const h of hotspots()) out.push(h);
  // people
  const P = target();
  if (P && hyp(P.x, P.z, t.x, t.z) < TOMS.talksWithinMetres) {
    if (!out.some((o) => o.k === 'E'))
      out.push({
        k: 'E',
        t: (P.anon ? 'Speak to ' : 'Talk to ') + tomName(P).replace(/^A /, 'a ').replace(/^The /, 'the '),
        run: () => talkTo(P),
        person: true,
      });
    if (!P.keeper) out.push({ k: 'Q', t: 'Front up' });
  }
  // the hands-on run's fault: Ron wanted a word, stood beside Tom at the office door, and E only went through the
  // door. Somebody who has something to say to him and stands within reach is offered before a door, whichever way
  // Tom is facing.
  if (!out.some((o) => o.k === 'E')) {
    const W = G.named.find((Q) => !Q.gone && !Q.dead && !Q.down && Q.space === t.space && hyp(Q.x, Q.z, t.x, t.z) < TOMS.talksWithinMetres && beatFor(Q));
    if (W) out.push({ k: 'E', t: 'Talk to ' + tomName(W).replace(/^A /, 'a ').replace(/^The /, 'the ') + ' (a word)', run: () => talkTo(W), person: true });
  }
  // doors
  if (t.space === 'street') {
    for (const id in ROOMS) {
      const r = ROOMS[id];
      if (r.locked) continue;
      if (hyp(t.x, t.z, r.street[0], r.street[1]) < TOMS.doorWithinMetres && !out.some((o) => o.k === 'E' && !o.person))
        out.push({
          k: 'E',
          t: isOpen(id) ? 'Go into ' + r.name : r.name + ': shut',
          run: () => {
            if (isOpen(id)) enterRoom(id);
            else sub('Shut. A card in the door gives the hours.', '', 'over', 2.5);
          },
        });
    }
    const y = ROOMS.mickeys.exit2.street;
    if (hyp(t.x, t.z, y[0], y[1]) < TOMS.yardDoorWithinMetres && !out.some((o) => o.k === 'E' && !o.person))
      out.push({
        k: 'E',
        t: "Back door of Mickey's",
        run: () => {
          enterRoom('mickeys');
          const [x, z] = roomPos('mickeys', 5.6, 1.6);
          t.x = x;
          t.z = z;
          t.ang = -1.57;
        },
      });
    if (nearCar(TOMS.cabWithinMetres)) out.push({ k: 'E', t: G.car.keys ? "Get in car two, by the driver's door" : 'Car two (locked: the keys are in the office)', run: () => carKey(), car: true });
    for (const p of PROPS)
      if (p.hand && !p.broken && hyp(t.x, t.z, p.x, p.z) < p.r + TOMS.reachesAThingWithinMetres && t.weapon !== p.hand) {
        out.push({
          k: 'G',
          t: 'Pick up a ' + p.hand,
          run: () => {
            t.weapon = p.hand;
            fightCarried(p); // round 4: so it can break, and a broken one stays broken
            sub('A ' + p.hand + ', to hand if it comes to that.', '', 'over', 3);
          },
        });
        break;
      }
  } else {
    const r = ROOMS[t.space];
    if (r) {
      const [mx, mz] = roomPos(r.id, r.mat[0], r.mat[1]);
      if (hyp(t.x, t.z, mx, mz) < TOMS.doorMatWithinMetres && !out.some((o) => o.k === 'E' && !o.person))
        out.push({ k: 'E', t: r.upFrom ? 'Down the stair to the office' : 'Leave ' + r.name + ' by the street door', run: () => leaveRoom(false) });
      if (r.exit2) {
        const [ex, ez] = roomPos(r.id, r.exit2.mat[0], r.exit2.mat[1]);
        if (hyp(t.x, t.z, ex, ez) < TOMS.wayOutWithinMetres && !out.some((o) => o.k === 'E' && !o.person))
          out.push({ k: 'E', t: 'Out to ' + r.exit2.label, run: () => leaveRoom(true) });
      }
    }
  }
  if (t.hasCoat) out.push({ k: 'C', t: t.coat ? 'Coat off' : 'Coat on' });
  if (G.story.fare && G.story.fare.st === 'offer') out.push({ k: 'Y', t: 'Take the fare', run: fareAccept });
  // a person and a door on the one use key: one prompt, and pressing it asks which (the person is offered first)
  const es = out.filter((o) => o.k === 'E');
  if (es.length > 1) {
    const at = out.indexOf(es[0]);
    for (const e of es) out.splice(out.indexOf(e), 1);
    out.splice(at, 0, {
      k: 'E',
      t: es.map((e) => e.t).join(' / '),
      run: async () => {
        const i = await scene(() => choose('', 'Which?', es.map((e) => e.t + '.').concat(['Neither.'])));
        if (i < es.length) return es[i].run();
      },
    });
  }
  return out;
}
// What the E prompt does beside a person: the written scene that is waiting with them, or else a talk.
export function talkTo(P) {
  if (P.anon) {
    bubble(
      P,
      freshLine(P.def.bark || (P.lad ? BARKS.lads : nightF() > STORY.nightVoicesAboveNight ? BARKS.night : BARKS.day), 'Aye.'),
      3.5,
    );
    P.mind.look = STORY.looksAfterBarkingRealSeconds;
    return;
  }
  if (P.fight || P.down) return;
  P.ang = Math.atan2(G.tom.x - P.x, G.tom.z - P.z);
  unlock();
  const b = beatFor(P);
  if (b) b();
  else startTalk(P);
}
function useKey(k, again) {
  prompts = buildPrompts();
  const p = prompts.find((x) => x.k === k && x.run);
  lastP = 0;
  if (p) {
    feel.early = null;
    p.run();
  } else if (!again) feel.early = { k, t: TOMS.earlyPressCountsRealSeconds }; // round 6 (ER-INPUT-01): a press a moment early still counts
}
// Round 6 (the gate): the cabs, lamp posts and parked cars stop a step only when it takes him deeper in, so a man
// who finds himself inside one (put back from a save made at the wheel, a car that rolled over where he stood) can
// always walk out.
function solidFor(x, z) {
  if (blocked(x, z, TOMS.bodyRadiusMetres)) return true;
  if (G.tom.space === 'street') {
    const c = G.car,
      t = G.tom,
      deeper = (cx, cz) => {
        const d = hyp(x, z, cx, cz);
        return d < TOMS.cabBodyRadiusMetres && d < hyp(t.x, t.z, cx, cz);
      };
    for (const k of [1.3, 0, -1.3]) if (deeper(c.x + Math.sin(c.ang) * k, c.z + Math.cos(c.ang) * k)) return true;
    if (!G.people.kevin?.gone || hour() < TOMS.kevinsCabOutFromHour || hour() > TOMS.kevinsCabBackAtHour) {
      for (const k of [1.3, 0, -1.3]) if (deeper(4.1, 32.2 + k)) return true;
    }
    if (footSolid(x, z, t.x, t.z, TOMS.bodyRadiusMetres)) return true;
  }
  return false;
}
// Could he stand here? (the same test his own steps use; the story player plans its walks by it)
export const standable = (x, z) => !solidFor(x, z);
// A wait always stops for what the town has for him (a man at the door, a message, a constable): the wait key must be
// let go and pressed again to go on waiting.
let waitBroken = false;
export function stopWaiting() {
  waitBroken = true;
}
export function stepPlayer(dt) {
  const t = G.tom;
  // keys are on or off; a stick (touch, pad) is analogue
  const kx = (keys.KeyD || keys.ArrowRight ? 1 : 0) - (keys.KeyA || keys.ArrowLeft ? 1 : 0),
    ax = touch.x + pad.x;
  let mx = kx + ax,
    my = (keys.KeyW || keys.ArrowUp ? 1 : 0) - (keys.KeyS || keys.ArrowDown ? 1 : 0) + touch.y;
  if (!keys.KeyZ) waitBroken = false;
  const waiting = !!keys.KeyZ && !waitBroken && !t.inCar && !F.on && Math.abs(mx) + Math.abs(my + pad.y) < 0.1;
  ui.wait = waiting;
  G.fast = waiting ? TOMS.waitingTimeRunsTimes : 1;
  // round 6: the pad's right stick looks about, as the mouse does
  if (pad.cx || pad.cy) {
    cam.yaw -= pad.cx * PADS.lookRadiansPerSecond * dt;
    cam.pitch = clamp(
      cam.pitch + pad.cy * PADS.pitchRadiansPerSecond * dt * (G.settings.invertY ? -1 : 1),
      PADS.pitchAtLeastRadians,
      PADS.pitchAtMostRadians,
    );
    cam.idle = 0;
  }
  if (t.inCar) {
    // round 6: steering from keys (kx) is eased in the cab; a stick is used as it is. The pad's triggers drive.
    stepCar(dt, {
      kx,
      x: clamp(ax, -1, 1),
      y: clamp(my + pad.gas - pad.brake, -1, 1),
      hb: !!keys.Space || pad.hb,
    });
    t.run = false;
    feel.stride = 0;
    feel.stuck = 0;
  } else {
    stepCar(dt, { x: 0, y: 0 });
    my += pad.y;
    const l = Math.hypot(mx, my),
      pressing = l > 0.1,
      fighting = F.on && F.rung >= LAD.strikeRung;
    let sp = 0,
      wx = feel.wx,
      wz = feel.wz;
    if (pressing && !(F.on && F.rung < LAD.strikeRung && F.rung > 0 && false)) {
      mx /= Math.max(1, l);
      my /= Math.max(1, l);
      const fx = Math.sin(cam.yaw),
        fz = Math.cos(cam.yaw),
        rx = -Math.cos(cam.yaw),
        rz = Math.sin(cam.yaw);
      wx = fx * my + rx * mx;
      wz = fz * my + rz * mx;
      const run =
        (keys.ShiftLeft || keys.ShiftRight || touch.run || pad.gas > PADS.runsAboveTrigger) &&
        !fighting &&
        t.hurt < TOMS.cannotRunAboveHurt &&
        !t.carry;
      sp =
        (fighting
          ? TOMS.fightingMetresPerSecond
          : run
            ? TOMS.runningMetresPerSecond * (G.hooks.limp ? G.hooks.limp() : 1)
            : TOMS.walkingMetresPerSecond) *
        (1 - t.hurt * TOMS.hurtSlowsByShare) *
        Math.min(1, l) *
        (F.st === 'block' ? TOMS.blockingSlowsToShare : 1);
      t.run = run;
      // the one-shot: he no longer reverses his way in one frame while his body takes its time to turn
      if (!fighting) {
        const off = Math.abs(angDiff(t.ang, Math.atan2(wx, wz)));
        if (off > FEELT.turnSlowsAboveRadians) sp *= clamp(1 - (off - FEELT.turnSlowsAboveRadians) / (Math.PI - FEELT.turnSlowsAboveRadians), FEELT.turnSlowestShare, 1);
        if (keys.KeyZ) sp = Math.min(sp, TOMS.walkingMetresPerSecond * RULES.game.foot.slowWalkShareOfWalk); // Z held while moving: walking slowly (A1)
        t.slow = !!keys.KeyZ;
      }
      if (!fighting)
        t.ang += clamp(
          angDiff(t.ang, Math.atan2(wx, wz)),
          -TOMS.turnsRadiansPerSecond * dt,
          TOMS.turnsRadiansPerSecond * dt,
        );
      t.puff = clamp(
        (t.puff || 0) + (run ? dt * TOMS.puffGainedPerSecondRunning : -dt * TOMS.puffLostPerSecondWalking),
        0,
        1,
      );
      t.still = 0;
      feel.wx = wx;
      feel.wz = wz;
      feel.sp = sp;
      // round 6 (ER-INPUT-01): movement on keys is eased. He comes up to his pace over a few steps of the clock
      // and does not stop dead. In a fight the feet stay sharp.
      feel.stride = fighting ? 1 : Math.min(1, feel.stride + dt / TOMS.reachesPaceInRealSeconds);
    } else {
      t.run = false;
      t.still += dt;
      t.puff = Math.max(0, (t.puff || 0) - dt * TOMS.puffLostPerSecondStill);
      feel.stride = fighting || F.on ? 0 : Math.max(0, feel.stride - dt / TOMS.stopsInRealSeconds);
    }
    const go = (pressing ? sp : feel.sp) * feel.stride;
    if (go > 0) {
      const x0 = t.x,
        z0 = t.z,
        nx = t.x + wx * go * dt,
        nz = t.z + wz * go * dt;
      if (!solidFor(nx, t.z)) t.x = nx;
      if (!solidFor(t.x, nz)) t.z = nz;
      // round 6 (ER-CORE-01): never stuck. Pushing a way for a second without moving, while standing inside
      // something solid, puts him on the nearest clear ground.
      if (pressing && hyp(t.x, t.z, x0, z0) < TOMS.stuckIfSlowerThanMetresPerSecond * dt) {
        feel.stuck += dt;
        if (feel.stuck > TOMS.stuckAfterRealSeconds && !footClear(t.x, t.z, TOMS.bodyRadiusMetres)) {
          const p = clearGround(
            t.x,
            t.z,
            TOMS.bodyRadiusMetres,
            TOMS.clearGroundSearchMetres,
            TOMS.clearGroundStepMetres,
          );
          if (p) {
            t.x = p[0];
            t.z = p[1];
            sub(AT_ONCE.jam.foot, '', 'over');
          }
          feel.stuck = 0;
        }
      } else feel.stuck = 0;
    } else feel.stuck = 0;
    t.v = pressing ? sp : go;
    // do not stand inside people
    for (const P of G.named.concat(G.crowd)) {
      if (P.gone || P.space !== t.space || P.down || P.inCar) continue;
      const d = hyp(P.x, P.z, t.x, t.z);
      if (d < TOMS.pushedApartWithinMetres && d > 0.01) {
        const px = t.x + ((t.x - P.x) / d) * (TOMS.pushedApartWithinMetres - d),
          pz = t.z + ((t.z - P.z) / d) * (TOMS.pushedApartWithinMetres - d);
        // round 6: nobody shoulders him into a lamp post or a parked car
        // the one-shot: nor into the band beside a wall or a door jamb where he could not then take a step (the wall
        // that held him in Mickey's): he is moved only onto ground he can stand on
        if (!solidFor(px, pz)) {
          t.x = px;
          t.z = pz;
        }
      }
    }
    // never stuck: found standing inside something solid (put there by a talk, a load or a shove), he is eased at once
    // onto the nearest ground he can stand on
    if (solidFor(t.x, t.z)) {
      let best = null;
      for (let r = 0.1; r <= 1.5 && !best; r += 0.1)
        for (let k = 0; k < 12 && !best; k++) {
          const a = (k * Math.PI) / 6,
            x = t.x + Math.sin(a) * r,
            z = t.z + Math.cos(a) * r;
          if (!blocked(x, z, TOMS.bodyRadiusMetres) && !(t.space === 'street' && !footClear(x, z, TOMS.bodyRadiusMetres))) best = [x, z];
        }
      if (best) {
        const d = hyp(best[0], best[1], t.x, t.z),
          step = Math.min(d, 3 * dt);
        t.x += ((best[0] - t.x) / d) * step;
        t.z += ((best[1] - t.z) / d) * step;
      }
    }
  }
  t.y = groundY(t.x, t.z);
  // round 6 (ER-INPUT-01): a press made a moment before the thing came into reach is taken when it does
  if (feel.early) {
    feel.early.t -= dt;
    if (feel.early.t <= 0 || ui.modal || G.paused) feel.early = null;
    else if (feel.early.k === 'F') carKey(true);
    else useKey(feel.early.k, true);
  }
  lastP -= dt;
  if (lastP <= 0) {
    lastP = 0.15;
    prompts = buildPrompts();
    if (F.on) prompts = [];
    setPrompts(prompts);
  }
}
// ---------- camera ----------
const solidCam = (x, z) => {
  for (const b of BLD) if (b.st > 1 && inRect(x, z, b, 0.35)) return true;
  for (const w of WALLS) if (inRect(x, z, w, 0.3)) return true;
  return false;
};
// Is the camera, where it stands now, inside something solid (a building, a wall, a post, a shelter's side, a vehicle)?
// The picture would show the inside of it. Read by the tests on every sampled frame.
export function cameraInside() {
  const p = camera.position;
  if (G.tom.space !== 'street') return false;
  for (const b of BLD) if (b.st > 1 && inRect(p.x, p.z, b, 0) && p.y < 9) return 'building';
  for (const w of WALLS) if (inRect(p.x, p.z, w, 0)) return 'wall';
  if (thinThingAt(p.x, p.z, p.y)) return 'post or shelter';
  if (vehicleAt(p.x, p.z, p.y)) return 'vehicle';
  return false;
}
export function snapCam() {
  cam.snap = true;
}
const FEELT = RULES.game.feel; // the camera and turn faults measured on 20 Nov, mended (game/tune/feel.js)
export function stepCamera(dt) {
  const t = G.tom,
    room = t.space !== 'street' ? ROOMS[t.space] : null;
  cam.idle += dt;
  if (t.inCar && keys.KeyB) {
    cam.yaw = G.car.ang + Math.PI; // the one-shot: B held at the wheel looks back through the rear window (A24)
    cam.idle = 0;
  } else if (t.inCar) {
    if (cam.idle > 1.2) cam.yaw += clamp(angDiff(cam.yaw, G.car.ang), -2.2 * dt, 2.2 * dt);
  } else if (!room && cam.idle > 1.6 && t.v > 0.5 && !F.on)
    cam.yaw +=
      clamp(angDiff(cam.yaw, t.ang), -0.7 * dt, 0.7 * dt) * (Math.abs(angDiff(cam.yaw, t.ang)) > 2.4 ? 0 : 1);
  if (F.on && F.T && !room && cam.idle > 0.8) {
    const a = Math.atan2(F.T.x - t.x, F.T.z - t.z);
    cam.yaw += clamp(angDiff(cam.yaw, a + 0.5), -1.2 * dt, 1.2 * dt);
  }
  if (room) {
    cam.yaw = Math.PI + clamp(angDiff(Math.PI, cam.yaw), -0.7, 0.7);
    cam.pitch = clamp(cam.pitch, 0.42, 1.0);
  }
  const tx = t.x,
    tz = t.z,
    ty = (t.inCar ? 1.35 : 1.5) + (t.y || 0);
  // the one-shot: the cab's camera sits in its band (5 to 6.5 m back, 1.6 to 2.0 m up) and the fight's in its own (3.5 to 5.0 m)
  const cabPitch = Math.asin(clamp((FEELT.cabCameraUpMetres - FEELT.cabCameraTargetHeightMetres) / FEELT.cabCameraBackMetres, 0, 1));
  const fightCam = F.on && F.rung >= LAD.strikeRung && !room;
  const dist = t.inCar ? FEELT.cabCameraBackMetres / Math.cos(cabPitch) : room ? Math.max(cam.dist, 5.2) : fightCam ? Math.min(cam.dist, FEELT.fightCameraMetres) : cam.dist,
    pitch = t.inCar ? cabPitch : cam.pitch;
  // the view at the wheel: 60 to 65 degrees across at rest, widening to 64 to 70 at 30 mph; on foot the street lens
  {
    const across = FEELT.cabViewAcrossAtRestDegrees + (FEELT.cabViewAcrossAt30MphDegrees - FEELT.cabViewAcrossAtRestDegrees) * clamp(Math.abs(G.car.v) / FEELT.cabViewWidensUpToMetresPerSecond, 0, 1);
    const want = t.inCar ? (Math.atan(Math.tan((across * Math.PI) / 360) / (camera.aspect || 1)) * 360) / Math.PI : FEELT.onFootViewUpDownDegrees;
    const now = camera.fov + (want - camera.fov) * (cam.snap ? 1 : clamp(dt * FEELT.viewEasesPerSecond, 0, 1));
    if (Math.abs(now - camera.fov) > 1e-3 && !window.LEDGER_CAM) {
      camera.fov = now;
      camera.updateProjectionMatrix();
    }
  }
  if (room) {
    // Round 6 (ER-CAM-01): indoors the camera never goes behind a side wall or a partition. Only the part of its
    // arm that is lower than the walls can be hidden by one; if that part crosses a wall, the camera swings back
    // toward straight behind him until it is clear.
    const low = Math.min(
      Math.cos(pitch) * dist,
      (TOMS.roomWallHeightMetres - TOMS.lookTargetHeightMetres) / Math.tan(pitch),
    );
    let a = angDiff(Math.PI, cam.yaw);
    const hidden = () =>
      roomSightBlocked(
        room,
        tx,
        tz,
        tx + Math.sin(a) * low,
        tz + Math.cos(a) * low,
        TOMS.roomCameraKeepsOffWallsMetres,
      );
    while (a !== 0 && hidden())
      a = Math.abs(a) <= TOMS.roomCameraYawStepRadians ? 0 : a - Math.sign(a) * TOMS.roomCameraYawStepRadians;
    cam.yaw = Math.PI + a;
  }
  const fx = Math.sin(cam.yaw),
    fz = Math.cos(cam.yaw),
    cp = Math.cos(pitch),
    spn = Math.sin(pitch);
  let d = dist;
  if (!room) {
    for (let s = 0.6; s <= dist; s += 0.35) {
      if (
        (solidCam(tx - fx * cp * s, tz - fz * cp * s) && ty + spn * s < 9) ||
        // round 6 (ER-CAM-01, ER-DRIVE-06): nor behind a scrap heap, a stall or a crane leg, unless it looks over it
        (bigThingAt(tx - fx * cp * s, tz - fz * cp * s) && ty + spn * s < TOMS.cameraClearsBigThingsUnderMetres) ||
        thinThingAt(tx - fx * cp * s, tz - fz * cp * s, ty + spn * s) ||
        ((!t.inCar || s > RULES.game.feel.cameraAndVehicles.armClearOfOwnCabMetres) && vehicleAt(tx - fx * cp * s, tz - fz * cp * s, ty + spn * s))
      ) {
        d = Math.max(0.9, s - 0.45);
        break;
      }
    }
  }
  const px = tx - fx * cp * d,
    pz = tz - fz * cp * d,
    // the one-shot: pulled in close by a wall, a post or a shelter, the camera rises and looks down, so his feet stay in frame
    squeeze = !room && !t.inCar ? clamp((dist - d) / Math.max(1, dist), 0, 1) : 0,
    py = Math.max(0.5, ty + spn * d + (d < 2 ? 0.25 : 0)) + squeeze * FEELT.squeezedCameraRisesMetres;
  const k = cam.snap ? 1 : 1 - Math.exp(-dt * 9);
  cam.snap = false;
  cam.px += (px - cam.px) * k;
  cam.py += (py - cam.py) * k;
  cam.pz += (pz - cam.pz) * k;
  cam.tx += (tx - cam.tx) * k;
  cam.ty += (ty - squeeze * FEELT.squeezedCameraLooksDownMetres - cam.ty) * k;
  cam.tz += (tz - cam.tz) * k;
  cam.shake = Math.max(0, cam.shake - dt * 2);
  camera.position.set(
    cam.px + (Math.random() - 0.5) * cam.shake * 0.3,
    cam.py + (Math.random() - 0.5) * cam.shake * 0.3,
    cam.pz,
  );
  // the one-shot: the easing never leaves it inside something that has come up behind (a following car, a post passed
  // on a bend): it goes at once to the clear place the arm found
  if (!room && cameraInside()) {
    cam.px = px;
    cam.py = py;
    cam.pz = pz;
    camera.position.set(px, py, pz);
    if (cameraInside()) {
      // still inside (the thing overlaps the cab's own tail): right up over the roof
      cam.px = tx - fx * cp * 0.9;
      cam.pz = tz - fz * cp * 0.9;
      cam.py = ty + 2.6;
      camera.position.set(cam.px, cam.py, cam.pz);
      if (cameraInside()) {
        // his back is to a wall: straight over his head, looking down, until he steps away from it
        cam.px = tx - fx * 0.12;
        cam.pz = tz - fz * 0.12;
        cam.py = ty + 3.4;
        camera.position.set(cam.px, cam.py, cam.pz);
      }
    }
  }
  camera.lookAt(cam.tx, cam.ty + 0.15, cam.tz);
}
export function titleCamera(t) {
  const z = 46 - ((t * 0.55) % 70);
  camera.position.set(-1.6 + Math.sin(t * 0.07) * 1.6, 2.5 + Math.sin(t * 0.05) * 0.4, z);
  camera.lookAt(1.5 + Math.sin(t * 0.04) * 3, 2.0, z - 24);
}
// ---------- touch ----------
function initTouch(cv) {
  const stick = document.getElementById('stick'),
    nub = stick.firstElementChild,
    tb = document.getElementById('tb');
  let sid = null,
    lid = null,
    lx = 0,
    ly = 0;
  const btns = [
    ['E', 'Use', () => useKey('E')],
    ['T', 'Do', () => useKey('T')],
    ['F', 'Cab', carKey],
    [
      'Q',
      'Front',
      () => {
        const P = target();
        if (P) frontUp(P);
      },
    ],
    [
      'R',
      'Up',
      () => {
        if (F.on) climb();
      },
    ],
    ['X', 'Off', backDown],
    ['J', 'Hit', () => fightInput('light')],
    ['K', 'Block', () => fightBlock(F.st !== 'block')],
    ['C', 'Coat', coat],
    ['Y', 'Fare', fareAccept],
    ['L', 'Ledger', () => ui.hooks.ledger && ui.hooks.ledger()],
    [
      'Run',
      'Run',
      () => {
        touch.run = !touch.run;
      },
    ],
    [
      'Z',
      'Wait',
      () => {
        keys.KeyZ = !keys.KeyZ;
      },
    ],
    ['G', 'Take', () => useKey('G')],
    ['P', 'Menu', () => ui.hooks.pause && ui.hooks.pause()],
  ];
  tb.innerHTML = btns.map((b, i) => `<button data-i="${i}">${b[1]}</button>`).join('');
  tb.addEventListener('pointerdown', (e) => {
    const b = e.target.closest('button');
    if (b) {
      e.preventDefault();
      if (ui.modal === 'dialog') uiKey('KeyE');
      else btns[+b.dataset.i][2]();
    }
  });
  stick.addEventListener('pointerdown', (e) => {
    sid = e.pointerId;
    stick.setPointerCapture(sid);
  });
  stick.addEventListener('pointermove', (e) => {
    if (e.pointerId !== sid) return;
    const r = stick.getBoundingClientRect(),
      dx = (e.clientX - r.left - 60) / 50,
      dy = (e.clientY - r.top - 60) / 50,
      l = Math.max(1, Math.hypot(dx, dy));
    touch.x = dx / l;
    touch.y = -dy / l;
    nub.style.transform = `translate(${touch.x * 35}px,${-touch.y * 35}px)`;
  });
  const up = (e) => {
    if (e.pointerId === sid) {
      sid = null;
      touch.x = touch.y = 0;
      nub.style.transform = '';
    }
  };
  stick.addEventListener('pointerup', up);
  stick.addEventListener('pointercancel', up);
  cv.addEventListener('pointerdown', (e) => {
    if (e.pointerType !== 'touch') return;
    if (!G.settings.touch) {
      G.settings.touch = true;
      show('touch', G.story.phase === 'play');
    }
    lid = e.pointerId;
    lx = e.clientX;
    ly = e.clientY;
  });
  cv.addEventListener('pointermove', (e) => {
    if (e.pointerId !== lid || ui.modal) return;
    cam.yaw -= (e.clientX - lx) * 0.006;
    cam.pitch = clamp(cam.pitch + (e.clientY - ly) * 0.004, -0.1, 1.1);
    lx = e.clientX;
    ly = e.clientY;
    cam.idle = 0;
  });
  cv.addEventListener('pointerup', (e) => {
    if (e.pointerId === lid) lid = null;
  });
}
