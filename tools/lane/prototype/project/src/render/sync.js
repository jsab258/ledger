// Puts the simulation on screen: one figure per person, Tom's two coats, the cabs, ground markers, speech bubbles.
import { THREE } from './core.js';
import { buildChar, poseChar, holdProp, realiseChar } from './actors.js';
import { buildCar, carLights, setCarEnv } from './cars.js';
import { setBlobs } from './effects.js';
import { rooms } from './rooms.js';
import { town } from './town.js';
import { G, hour } from '../state.js';
import { groundY } from '../map.js';
import { hyp, clamp, angDiff } from '../util.js';
import { nightF } from '../seeing.js';

export const LOD = { far: 26 };
export const S = {
  chars: {},
  tom: null,
  tomCoat: null,
  cab: null,
  cab1: null,
  marker: null,
  tomAnim: { mode: 'stand' },
  bubbles: [],
  traffic: [],
};
const TOM_LOOK = {
  h: 1.8,
  b: 0.4,
  skin: 1,
  hair: ['short', '#2a2018'],
  top: ['carcoat', '#55604f', '#2a2a2a'],
  bot: ['jeans', '#2f3a52'],
  x: [],
};
const TOM_COAT = Object.assign({}, TOM_LOOK, { top: ['runner', '#17181c', '#17181c'] });

export function buildActors(scene) {
  for (const P of G.named.concat(G.crowd)) {
    const c = buildChar(P.def.look, {
      sex: P.def.sex,
      age: P.def.age,
      frail: P.def.frail,
      props: !!P.lad || P.id === 'dennis',
    });
    c.mesh.visible = false;
    scene.add(c.mesh);
    S.chars[P.id] = c;
  }
  S.tom = buildChar(TOM_LOOK, { sex: 'm', age: 32, props: true });
  S.tomCoat = buildChar(TOM_COAT, { sex: 'm', age: 32, props: true });
  scene.add(S.tom.mesh, S.tomCoat.mesh);
  {
    const t0 = performance.now();
    for (const id in S.chars) realiseChar(S.chars[id]);
    realiseChar(S.tom);
    realiseChar(S.tomCoat);
    S.dressMs = Math.round(performance.now() - t0);
  } // everyone is dressed before the curtain goes up, so nobody hitches into view
  S.cab = buildCar('saloon', '#1d2a5c', { cab: true, beams: true });
  scene.add(S.cab.g);
  // a head and shoulders at the glass for everyone who has a window on the street: this is how a window watcher shows now
  S.busts = {};
  for (const P of G.named) {
    if (!P.win) continue;
    const W = town.winAt[P.id] || { x: P.win.x, y: P.win.y, z: P.win.z, ang: P.win.ang, w: 1, h: 1.45 },
      L = P.def.look || {},
      g = new THREE.Group(),
      col = (h, k) => new THREE.MeshBasicMaterial({ color: new THREE.Color(h || '#888').multiplyScalar(k) });
    const skin = ['#e3bfa3', '#d6a98a', '#b98564', '#7d5236'][L.skin | 0] || '#d6a98a',
      hair = (L.hair && L.hair[1]) || '#4a4038',
      top = (L.top && L.top[1]) || '#5a5a60',
      sill = -W.h / 2 + 0.02;
    const body = new THREE.Group();
    body.position.y = sill + 0.6; // shoulders a little above the sill, as someone stood back from the glass
    const sh = new THREE.Mesh(new THREE.SphereGeometry(0.25, 14, 8), col(top, 0.8));
    sh.scale.set(1.05, 0.5, 0.4);
    sh.position.y = -0.33;
    const chest = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.3, 0.1), col(top, 0.74));
    chest.position.y = -0.45;
    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, 0.12, 8), col(skin, 0.7));
    neck.position.y = -0.2;
    const head = new THREE.Group(),
      face = new THREE.Mesh(new THREE.SphereGeometry(0.105, 12, 10), col(skin, 0.82));
    face.scale.set(0.9, 1.12, 0.95);
    const cap = new THREE.Mesh(
      new THREE.SphereGeometry(0.113, 12, 8, 0, Math.PI * 2, 0, Math.PI * 0.56),
      col(hair, 0.85),
    );
    cap.position.set(0, 0.012, -0.014);
    cap.scale.set(0.93, 1.12, 1);
    head.add(face, cap);
    head.position.y = -0.04;
    body.add(sh, chest, neck, head);
    const curt = new THREE.Mesh(
      new THREE.PlaneGeometry(W.w * 0.36, W.h - 0.04),
      new THREE.MeshBasicMaterial({ color: '#cfc8b6' }),
    );
    curt.position.set(-W.w / 2 + W.w * 0.18, 0, -0.07);
    const cx0 = curt.position.x;
    g.add(body, curt);
    g.position.set(W.x + Math.sin(W.ang) * 0.12, W.y, W.z + Math.cos(W.ang) * 0.12);
    g.rotation.y = W.ang;
    g.visible = false;
    scene.add(g);
    const mats = [sh.material, chest.material, neck.material, face.material, cap.material, curt.material];
    S.busts[P.id] = {
      g,
      body,
      head,
      sh,
      curt,
      cx0,
      W,
      by: body.position.y,
      mats,
      base: mats.map((m) => m.color.clone()),
      yaw: 0,
      k: 0,
    };
  }
  S.cab1 = buildCar('saloon', '#6a1f24', { cab: true });
  S.cab1.g.position.set(4.1, 0, 32.2);
  scene.add(S.cab1.g);
  const mk = new THREE.Mesh(
    new THREE.RingGeometry(0.9, 1.15, 28).rotateX(-Math.PI / 2),
    new THREE.MeshBasicMaterial({
      color: new THREE.Color(2.2, 1.7, 0.5),
      transparent: true,
      opacity: 0.8,
      depthWrite: false,
    }),
  );
  mk.visible = false;
  mk.layers.set(1);
  scene.add(mk);
  S.marker = mk;
  // a few parked cars for life
  for (const [k, c, x, z, a] of [
    ['hatch', '#7a6a2a', -30, -17.2, 1.57],
    ['saloon', '#4a4a48', -58, -19.8, -1.57],
    ['van', '#d8d4c8', 29.2, -4, 0],
    ['flatbed', '#3a4a5a', -97, 36, 0.3],
    ['hatch', '#5a2a2a', 12, -127.4, 1.57],
    ['van', '#2f4a3a', 86, 51.4, 1.57],
    ['saloon', '#2a3a4a', -40, -182, 0],
  ]) {
    const car = buildCar(k, c, k === 'van' && z > 50 ? { lettering: ['JENSEN & SON', 'FISH'] } : {});
    car.g.position.set(x, 0, z);
    car.g.rotation.y = a;
    carLights(car, false, false);
    scene.add(car.g);
    S.traffic.push({ car, x, z, r: 1.5, parked: true });
  }
}
function modeFor(P) {
  if (P.down) return 'down';
  if (P.fight) return P.fight.mode || 'guard';
  if (P.react) return P.react;
  const st = P.state;
  if (P.moving) return 'stand';
  if (st === 'sit' || st === 'queueSit') return 'sit';
  if (st === 'mend') return 'mend';
  if (st === 'smoke') return 'smoke';
  if (st === 'paint') return 'paint';
  if (st === 'work') return 'work';
  return 'stand';
}
const SEAT = { sit: 0.0, drive: -0.08 };
export function syncActors(dt, camera) {
  const t = G.tom,
    blobs = [],
    cx = camera.position.x,
    cz = camera.position.z,
    room = t.space !== 'street' ? t.space : null;
  for (const P of G.named.concat(G.crowd)) {
    const c = S.chars[P.id];
    if (!c) continue;
    const vis =
      !P.gone &&
      !P.dead &&
      P.space === t.space &&
      P.space !== 'home' &&
      hyp(P.x, P.z, cx, cz) < 110 &&
      !P.inCar;
    c.mesh.visible = vis;
    if (!vis) continue;
    const y = groundY(P.x, P.z);
    c.mesh.position.set(P.x, y, P.z);
    c.mesh.rotation.y = P.ang;
    const dist = hyp(P.x, P.z, cx, cz),
      near = dist < 60;
    c.lodFar = dist > LOD.far;
    if (near) {
      if (P.glanceT > 0) P.glanceT -= dt; // two people talking, and a glance his way
      const glance = P.glanceT > 0 && P.chat && !P.talking,
        toTom = Math.atan2(t.x - P.x, t.z - P.z);
      const look = P.talking
        ? toTom
        : glance
          ? P.glanceT % 1.3 > 0.55
            ? toTom
            : null
          : P.mind.look > 0
            ? toTom
            : null;
      if (P.backT > 0) {
        P.backT -= dt;
        const k = clamp(Math.min(3.4 - P.backT, P.backT) / 0.45, 0, 1) * 0.75,
          dd = hyp(P.x - t.x, P.z - t.z, 0, 0) || 1;
        c.mesh.position.x += ((P.x - t.x) / dd) * k;
        c.mesh.position.z += ((P.z - t.z) / dd) * k;
        c.mesh.rotation.y = toTom;
      }
      const halted = P.pauseT > 0 || P.backT > 0;
      poseChar(
        c,
        {
          v: P.moving && !halted ? P.v || 1.3 : 0,
          run: (P.hurry || 1) > 1.8,
          mode: modeFor(P),
          ang: P.backT > 0 ? toTom : P.ang,
          look,
          talk: !!P.chat || P.talking,
          hurt: P.hurt || 0,
          limp: (P.hurt || 0) > 0.4 ? 0.7 : 0,
          snap: P.fight ? 22 : 13,
        },
        dt,
      );
      if (P.weapon !== c.held) {
        holdProp(c, P.weapon || null);
        c.held = P.weapon;
      }
    }
    blobs.push([P.x, y, P.z, P.down ? 1.6 : 0.85]);
  }
  // at the windows: somebody stood at the glass, and the head follows him when the seeing rule says they have him
  if (S.busts) {
    const nf = nightF(),
      watching = new Set();
    for (const w of G.watch || []) watching.add(w.P.id);
    for (const id in S.busts) {
      const b = S.busts[id],
        P = G.people[id],
        W = b.W,
        on =
          !!P &&
          P.space === 'home' &&
          P.atWindow &&
          !P.dead &&
          t.space === 'street' &&
          (P.winLit || nf < 0.6) &&
          hyp(W.x, W.z, cx, cz) < 90; // a dark window at night keeps its secret, as the rule says b.k += ((on ? 1 : 0) - b.k) * Math.min(1, dt * 3.5); b.g.visible = b.k > 0.03; if (!b.g.visible) continue;
      const lit = P.winLit ? 0.08 : 0.92 - nf * 0.72;
      b.mats.forEach((m, i) => m.color.copy(b.base[i]).multiplyScalar(i === 5 ? Math.max(lit, 0.32) : lit));
      const sees = watching.has(id);
      let yaw = sees ? angDiff(W.ang, Math.atan2(t.x - W.x, t.z - W.z)) : Math.sin(G.t * 0.11 + W.z) * 0.5;
      yaw = clamp(yaw, -1.25, 1.25);
      b.yaw += (yaw - b.yaw) * Math.min(1, dt * (sees ? 4 : 1.2));
      b.head.rotation.y = b.yaw * 0.8;
      b.head.rotation.x = sees ? 0.32 : 0.12;
      b.sh.rotation.y = b.yaw * 0.25;
      b.body.position.y = b.by - (1 - b.k) * 0.45;
      b.body.position.x = W.w * 0.1;
      b.curt.scale.x = 1 - b.k * 0.45;
      b.curt.position.x = b.cx0 - b.k * W.w * 0.08;
    }
  }
  // Tom
  const coat = t.coat && t.hasCoat,
    tc = coat ? S.tomCoat : S.tom,
    other = coat ? S.tom : S.tomCoat;
  other.mesh.visible = false;
  tc.mesh.visible = t.space !== 'away' && (!t.inCar || !!tc.rigged);
  if (tc.mesh.visible && t.inCar) {
    // at the wheel of his cab
    const c = G.car,
      sx = -0.36,
      sz = 0.02,
      s = Math.sin(c.ang),
      co = Math.cos(c.ang);
    tc.mesh.position.set(c.x + sx * co + sz * s, SEAT.drive, c.z - sx * s + sz * co);
    tc.mesh.rotation.y = c.ang;
    tc.lodFar = false;
    poseChar(tc, { mode: 'drive', v: 0, ang: c.ang }, dt);
    if (tc.held) {
      holdProp(tc, null);
      tc.held = null;
    }
  } else if (tc.mesh.visible) {
    const y = groundY(t.x, t.z);
    tc.mesh.position.set(t.x, y, t.z);
    tc.mesh.rotation.y = t.ang;
    const a = S.tomAnim;
    a.v = t.v;
    a.run = t.run && t.v > 2.4;
    a.ang = t.ang;
    a.hurt = t.hurt;
    a.limp = t.hurt > 0.4 ? clamp((t.hurt - 0.3) * 1.4, 0, 1) : 0;
    a.carry = !!t.carry || (t.armed && !!t.weapon);
    a.puff = t.puff || 0;
    if (t.sit) a.mode = 'sit';
    poseChar(tc, a, dt);
    const held = t.carry || (t.armed ? t.weapon : null);
    if (held !== tc.held) {
      holdProp(tc, held);
      tc.held = held;
    }
    blobs.push([t.x, y, t.z, 0.9]);
  }
  // the cabs
  const c = G.car,
    n = nightF();
  setCarEnv(1 - n);
  LOD.far = G.settings.quality === 'low' ? 11 : G.settings.quality === 'medium' ? 20 : 28;
  S.cab.g.position.set(c.x, 0, c.z);
  S.cab.g.rotation.y = c.ang;
  S.cab.g.visible = t.space === 'street' || t.inCar;
  for (const w of S.cab.wheels) w.rotation.x += (c.v * dt) / 0.3;
  carLights(S.cab, t.inCar ? n > 0.25 : false, t.inCar && c.braking);
  blobs.push([c.x, 0, c.z, 2.6, 5, c.ang]);
  const kev = G.people.kevin,
    ter = G.people.terry,
    h = hour();
  const out = h >= 7 && h < 18.4 ? kev.gone : ter.gone && !(h >= 6.2 && h < 7);
  S.cab1.g.visible = !out && !room;
  if (S.cab1.g.visible) blobs.push([4.1, 0, 32.2, 2.6, 5, 0]);
  for (const v of S.traffic) {
    if (v.car.g.visible)
      blobs.push([
        v.car.g.position.x,
        0,
        v.car.g.position.z,
        v.car.wid + 1,
        v.car.len + 0.8,
        v.car.g.rotation.y,
      ]);
    if (v.parked) v.car.g.visible = !room;
  }
  setBlobs(room ? blobs.filter((b) => b[0] > 900) : blobs);
  // story dressing
  if (rooms.coat) rooms.coat.visible = !t.hasCoat && !G.story.flags.coatGone;
  if (rooms.suitcase) rooms.suitcase.visible = !!G.story.flags.unpacked;
  if (S.marker.visible) {
    const s = 1 + Math.sin(performance.now() * 0.005) * 0.12;
    S.marker.scale.set(s, 1, s);
  }
}
export function setMarker(x, z) {
  if (x == null) {
    S.marker.visible = false;
    return;
  }
  S.marker.position.set(x, groundY(x, z) + 0.05, z);
  S.marker.visible = true;
}
// Project a world point to screen for bubbles and name tags.
const v = new THREE.Vector3();
export function toScreen(x, y, z, camera) {
  v.set(x, y, z).project(camera);
  if (v.z > 1) return null;
  return [(v.x * 0.5 + 0.5) * window.innerWidth, (-v.y * 0.5 + 0.5) * window.innerHeight, v.z];
}
export function charOf(P) {
  return S.chars[P.id];
}
