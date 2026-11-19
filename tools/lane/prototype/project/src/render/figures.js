// People drawn in code: one skinned mesh each, built from a description of body and 1990 clothes,
// and posed procedurally so posture, breath and a limp can carry what a health bar would.
import { THREE, lit, mergeGeometries, boxG } from './core.js';
import { clamp, angDiff } from '../util.js';
import { SKINS } from '../cast.js';

let charMat, propMat;
const LONG = { overcoat: 0.5, mac: 0.5, carcoat: 0.62, duffel: 0.6, cassock: 0.1, runner: 0.44 };
const _c = new THREE.Color();
export const BONE = {
  hips: 0,
  spine: 1,
  chest: 2,
  neck: 3,
  head: 4,
  armL: 5,
  foreL: 6,
  armR: 7,
  foreR: 8,
  thighL: 9,
  shinL: 10,
  thighR: 11,
  shinR: 12,
};

export function buildChar(look, o = {}) {
  if (!charMat) {
    charMat = lit(new THREE.MeshLambertMaterial({ vertexColors: true }), { gain: 1.15 });
    propMat = lit(new THREE.MeshLambertMaterial({ vertexColors: true }));
  }
  const s = look.h / 1.75,
    fem = o.sex === 'f',
    bw = (0.86 + 0.42 * look.b) * (fem ? 0.92 : 1),
    bd = 0.8 + 0.6 * look.b;
  const parts = [];
  const add = (g, bone, col) => {
    g = g.index ? g.toNonIndexed() : g;
    g.deleteAttribute('uv');
    const n = g.attributes.position.count;
    _c.set(col);
    const ca = new Float32Array(n * 3),
      si = new Uint16Array(n * 4),
      sw = new Float32Array(n * 4);
    for (let i = 0; i < n; i++) {
      ca[i * 3] = _c.r;
      ca[i * 3 + 1] = _c.g;
      ca[i * 3 + 2] = _c.b;
      si[i * 4] = bone;
      sw[i * 4] = 1;
    }
    g.setAttribute('color', new THREE.BufferAttribute(ca, 3));
    g.setAttribute('skinIndex', new THREE.BufferAttribute(si, 4));
    g.setAttribute('skinWeight', new THREE.BufferAttribute(sw, 4));
    parts.push(g);
  };
  const T = (g, x, y, z, rx = 0, ry = 0, rz = 0, sx = 1, sy = 1, sz = 1) => {
    g.scale(sx, sy, sz);
    if (rx) g.rotateX(rx);
    if (rz) g.rotateZ(rz);
    if (ry) g.rotateY(ry);
    g.translate(x, y, z);
    return g;
  };
  const cap = (r, len, x, y, z, bone, col) =>
    add(T(new THREE.CapsuleGeometry(r, len, 2, 7), x, y, z), bone, col);
  const cyl = (rt, rb, h, x, y, z, bone, col, sz = 1, open = false) =>
    add(T(new THREE.CylinderGeometry(rt, rb, h, 10, 1, open), x, y, z, 0, 0, 0, 1, 1, sz), bone, col);
  const sph = (r, x, y, z, bone, col, sx = 1, sy = 1, sz = 1, th = Math.PI, t0 = 0) =>
    add(T(new THREE.SphereGeometry(r, 10, 7, 0, 6.2832, t0, th), x, y, z, 0, 0, 0, sx, sy, sz), bone, col);
  const bx = (w, h, d, x, y, z, bone, col, rx = 0) =>
    add(T(new THREE.BoxGeometry(w, h, d), x, y, z, rx), bone, col);
  const skin = SKINS[look.skin] || SKINS[0],
    [top, tc, ta] = look.top,
    [bot, bc] = look.bot,
    [hair, hc] = look.hair,
    xs = look.x || [];
  const hipH = 0.93 * s,
    th = 0.45 * s,
    sh = 0.4 * s,
    ua = 0.29 * s,
    fa = 0.26 * s,
    swd = (fem ? 0.175 : 0.2) * bw * s,
    hw = 0.085 * bw * s;
  const yS = hipH + 0.12 * s,
    yC = yS + 0.17 * s,
    yN = yC + 0.24 * s,
    yH = yN + 0.1 * s,
    ySh = yC + 0.2 * s,
    hr = 0.105 * s,
    hy = yH + 0.075 * s;
  // legs
  const legCol = bot === 'skirt' ? '#3a3232' : bc;
  for (const [sx, tB, sB] of [
    [1, 9, 10],
    [-1, 11, 12],
  ]) {
    cap(0.082 * bw * s, th - 0.08 * s, sx * hw, hipH - th / 2, 0, tB, legCol);
    cap(0.064 * bw * s, sh - 0.06 * s, sx * hw, hipH - th - sh / 2 + 0.02 * s, 0, sB, legCol);
    bx(
      0.095 * s,
      0.075 * s,
      0.25 * s,
      sx * hw,
      0.04 * s,
      0.045 * s,
      sB,
      top === 'shell' ? '#e8e8e4' : '#17171a',
    );
    if (bot === 'trackies')
      bx(0.012, th + sh - 0.1, 0.03, sx * (hw + 0.07 * bw * s), hipH - (th + sh) / 2, 0, tB, ta);
  }
  cyl(
    0.16 * bw * s,
    0.165 * bw * s,
    0.2 * s,
    0,
    hipH + 0.02 * s,
    0,
    0,
    bot === 'skirt' ? bc : legCol,
    bd * 0.74,
  );
  if (bot === 'skirt') cyl(0.165 * bw * s, 0.2 * bw * s, 0.5 * s, 0, hipH - 0.22 * s, 0, 0, bc, bd * 0.8);
  // torso
  cyl(0.15 * bw * s, 0.16 * bw * s, 0.24 * s, 0, yS + 0.06 * s, 0, 1, tc, bd * 0.76);
  if (look.b > 0.55) sph(0.15 * bw * s, 0, yS + 0.04 * s, 0.05 * s * bd, 1, tc, 1, 0.9, bd * 0.85);
  cyl((fem ? 0.165 : 0.185) * bw * s, 0.155 * bw * s, 0.3 * s, 0, yC + 0.1 * s, 0, 2, tc, bd * 0.7);
  if (fem) sph(0.1 * bw * s, 0, yC + 0.1 * s, 0.06 * s * bd, 2, tc, 1.45, 0.8, 0.8);
  for (const sx of [1, -1]) sph(0.078 * bw * s, sx * swd, ySh, 0, 2, tc);
  cyl(0.045 * s, 0.05 * s, 0.09 * s, 0, yN + 0.04 * s, 0, 3, skin);
  const long = LONG[top];
  if (long) {
    const y1 = long * s;
    cyl(
      0.16 * bw * s,
      (0.19 + (0.93 - long) * 0.08) * bw * s,
      hipH + 0.08 * s - y1,
      0,
      (hipH + 0.08 * s + y1) / 2,
      0,
      0,
      tc,
      bd * 0.82,
    );
  }
  if (top === 'donkey') bx(0.4 * bw * s, 0.14 * s, 0.26 * s * bd, 0, ySh - 0.03 * s, -0.01, 2, ta);
  if (top === 'shell') {
    cyl(0.19 * bw * s, 0.18 * bw * s, 0.08 * s, 0, yC + 0.13 * s, 0, 2, ta, bd * 0.72);
  }
  if (
    top === 'cardigan' ||
    top === 'blouse' ||
    top === 'overall' ||
    top === 'denim' ||
    top === 'leather' ||
    top === 'mac' ||
    top === 'carcoat'
  )
    bx(0.07 * s, 0.34 * s, 0.02, 0, yC + 0.02 * s, 0.125 * s * bd * (0.9 + look.b * 0.2), 2, ta);
  if (top === 'apron') {
    bx(0.26 * bw * s, 0.3 * s, 0.02, 0, yC + 0.0 * s, 0.13 * s * bd, 2, ta);
    bx(0.3 * bw * s, 0.42 * s, 0.02, 0, hipH - 0.1 * s, 0.135 * s * bd, 0, ta);
  }
  if (top === 'tunic') {
    cyl(0.165 * bw * s, 0.165 * bw * s, 0.04 * s, 0, yS + 0.0 * s, 0, 1, '#0c0d10', bd * 0.8);
    for (let i = 0; i < 4; i++)
      sph(0.012, 0, yS + 0.08 * s + i * 0.085 * s, 0.128 * s * bd, i < 2 ? 1 : 2, ta);
  }
  if (top === 'cassock') {
    bx(0.05 * s, 0.03 * s, 0.02, 0, yN + 0.01 * s, 0.05 * s, 3, ta);
  }
  if (top === 'overcoat' || top === 'runner' || top === 'mac' || top === 'duffel' || top === 'donkey')
    cyl(
      0.07 * s,
      0.085 * s,
      top === 'runner' ? 0.1 * s : 0.05 * s,
      0,
      yN + (top === 'runner' ? 0.03 : 0.0) * s,
      -0.01,
      3,
      tc,
      1,
      true,
    );
  if (top === 'mac') cyl(0.168 * bw * s, 0.168 * bw * s, 0.035 * s, 0, yS + 0.02 * s, 0, 1, ta, bd * 0.8);
  // arms
  for (const [sx, aB, fB] of [
    [1, 5, 6],
    [-1, 7, 8],
  ]) {
    cap(0.058 * bw * s, ua - 0.06 * s, sx * swd, ySh - ua / 2, 0, aB, tc);
    cap(0.05 * bw * s, fa - 0.05 * s, sx * swd, ySh - ua - fa / 2 + 0.01 * s, 0, fB, tc);
    sph(0.05 * s, sx * swd, ySh - ua - fa - 0.035 * s, 0, fB, skin, 0.8, 1.15, 1);
    if (top === 'shell')
      cyl(0.047 * bw * s, 0.047 * bw * s, 0.04 * s, sx * swd, ySh - ua - fa + 0.05 * s, 0, fB, ta);
  }
  // head
  sph(hr, 0, hy, 0, 4, skin, 0.92, 1.12, 1);
  sph(hr * 0.5, 0, hy - hr * 0.55, hr * 0.25, 4, skin, 1.1, 0.8, 1.1);
  bx(0.022 * s, 0.035 * s, 0.03 * s, 0, hy - 0.012 * s, hr * 0.96, 4, skin);
  for (const sx of [1, -1]) {
    sph(0.011 * s, sx * 0.036 * s, hy + 0.018 * s, hr * 0.9, 4, '#16120f');
    bx(
      0.032 * s,
      0.007 * s,
      0.01,
      sx * 0.036 * s,
      hy + 0.04 * s,
      hr * 0.9,
      4,
      hair === 'bald' ? '#5a4a3a' : hc,
    );
  }
  bx(0.045 * s, 0.006 * s, 0.01, 0, hy - 0.058 * s, hr * 0.86, 4, fem ? '#8a3a3a' : '#7a4a40');
  const hz = -0.022 * s,
    H = (r, thLen, col = hc, sy = 1, yo = 0, t0 = 0) =>
      sph(hr * r, 0, hy + 0.012 * s + yo, hz, 4, col, 0.95, 1.1 * sy, 1.04, thLen, t0);
  if (hair === 'short') H(1.07, 1.75);
  else if (hair === 'balding') H(1.05, 0.9, hc, 1, 0, 0.95);
  else if (hair === 'set') {
    H(1.17, 1.9);
  } else if (hair === 'perm') {
    H(1.12, 2.0);
    for (let i = 0; i < 9; i++) {
      const a = (i / 9) * 6.28;
      sph(
        hr * 0.42,
        Math.sin(a) * hr * 0.9,
        hy + hr * 0.45 + (i % 2) * 0.03,
        hz + Math.cos(a) * hr * 0.9 - 0.01,
        4,
        hc,
      );
    }
    sph(hr * 0.6, 0, hy + hr * 1.0, hz, 4, hc);
  } else if (hair === 'bob') H(1.12, 2.25);
  else if (hair === 'long') {
    H(1.1, 2.3);
    bx(0.2 * s, 0.26 * s, 0.05 * s, 0, hy - 0.12 * s, hz - hr * 0.8, 4, hc);
  } else if (hair === 'bun') {
    H(1.08, 1.8);
    sph(hr * 0.42, 0, hy + hr * 0.75, hz - hr * 0.95, 4, hc);
  } else if (hair === 'mullet') {
    H(1.07, 1.75);
    bx(0.14 * s, 0.14 * s, 0.035 * s, 0, hy - 0.1 * s, hz - hr * 0.85, 4, hc);
  } else if (hair === 'quiff') {
    H(1.07, 1.75);
    sph(hr * 0.5, 0, hy + hr * 0.95, hr * 0.5, 4, hc, 1.2, 0.8, 1.2);
  } else if (hair === 'flatcap') {
    H(1.05, 0.9, hc, 1, 0, 0.95);
    add(
      T(new THREE.CylinderGeometry(hr * 1.2, hr * 1.25, 0.045 * s, 10), 0, hy + hr * 0.92, hz + 0.02, -0.14),
      4,
      '#5a554a',
    );
    bx(0.16 * s, 0.014 * s, 0.09 * s, 0, hy + hr * 0.74, hr * 0.95, 4, '#4e493f');
  } else if (hair === 'woolly') H(1.13, 1.62, '#27324a');
  else if (hair === 'headscarf') {
    H(1.13, 2.2, hc);
    sph(0.03 * s, 0, hy - hr * 1.05, hr * 0.7, 4, hc);
  } else if (hair === 'rainhood') H(1.14, 2.1, '#b9c4c6');
  else if (hair === 'helmet') {
    H(1.05, 1.6, '#3a2a1a');
    sph(hr * 1.12, 0, hy + hr * 0.5, hz + 0.01, 4, '#0d0f14', 1, 1.6, 1.08, 1.6);
    cyl(hr * 1.3, hr * 1.36, 0.02 * s, 0, hy + hr * 0.62, hz + 0.01, 4, '#0d0f14');
    sph(0.022 * s, 0, hy + hr * 1.25, hr * 1.0, 4, '#c9c9c9');
  }
  if (xs.includes('woolly')) H(1.13, 1.62, '#7a2a22');
  if (xs.includes('glasses')) {
    bx(0.15 * s, 0.012 * s, 0.01, 0, hy + 0.02 * s, hr * 0.98, 4, '#1a1a1a');
    for (const sx of [1, -1])
      bx(0.05 * s, 0.035 * s, 0.008, sx * 0.037 * s, hy + 0.014 * s, hr * 0.985, 4, '#2a3038');
  }
  if (xs.includes('tash')) bx(0.06 * s, 0.016 * s, 0.014, 0, hy - 0.04 * s, hr * 0.93, 4, hc);
  if (xs.includes('beard')) sph(hr * 0.72, 0, hy - hr * 0.55, hr * 0.28, 4, '#c9c4ba', 1.15, 0.95, 1.1);
  if (xs.includes('earrings'))
    for (const sx of [1, -1]) sph(0.014 * s, sx * hr * 0.93, hy - 0.04 * s, 0, 4, '#d8b24a');
  if (xs.includes('pager')) bx(0.05, 0.07, 0.025, 0.16 * bw * s, hipH + 0.08 * s, 0.05, 0, '#111');
  if (xs.includes('bag')) {
    bx(0.26 * s, 0.2 * s, 0.09 * s, swd + 0.02, ySh - ua - fa - 0.16 * s, 0, 6, fem ? '#5a2a22' : '#3a3a30');
  }
  const geo = mergeGeometries(parts, false);
  parts.forEach((p) => p.dispose());
  // skeleton
  const bones = [];
  const mk = (par, x, y, z) => {
    const b = new THREE.Bone();
    b.position.set(x, y, z);
    if (par) par.add(b);
    bones.push(b);
    return b;
  };
  const hips = mk(null, 0, hipH, 0),
    spine = mk(hips, 0, 0.12 * s, 0),
    chest = mk(spine, 0, 0.17 * s, 0),
    neck = mk(chest, 0, 0.24 * s, 0);
  mk(neck, 0, 0.1 * s, 0);
  const aL = mk(chest, swd, 0.2 * s, 0);
  mk(aL, 0, -ua, 0);
  const aR = mk(chest, -swd, 0.2 * s, 0);
  mk(aR, 0, -ua, 0);
  const tL = mk(hips, hw, 0, 0);
  mk(tL, 0, -th, 0);
  const tR = mk(hips, -hw, 0, 0);
  mk(tR, 0, -th, 0);
  const mesh = new THREE.SkinnedMesh(geo, charMat);
  mesh.add(hips);
  mesh.bind(new THREE.Skeleton(bones));
  mesh.boundingSphere = new THREE.Sphere(new THREE.Vector3(0, 0.9, 0), 2.4);
  mesh.frustumCulled = false;
  const c = {
    mesh,
    bones,
    s,
    hipH,
    fa,
    phase: Math.random() * 6,
    t: Math.random() * 10,
    cur: bones.map(() => [0, 0, 0]),
    hy: hipH,
    props: {},
    old: (o.age || 30) > 62,
    stoop: (o.age || 30) > 70 ? 0.16 : (o.age || 30) > 60 ? 0.07 : 0,
    frail: o.frail,
  };
  // things held in the right hand hang off the forearm bone
  const hand = new THREE.Group();
  hand.position.set(0, -fa - 0.05 * s, 0.01);
  bones[8].add(hand);
  c.hand = hand;
  const P = (name, g, col) => {
    const m = new THREE.Mesh(g, propMat);
    const n = g.attributes.position.count,
      ca = new Float32Array(n * 3);
    _c.set(col);
    for (let i = 0; i < n; i++) {
      ca[i * 3] = _c.r;
      ca[i * 3 + 1] = _c.g;
      ca[i * 3 + 2] = _c.b;
    }
    g.setAttribute('color', new THREE.BufferAttribute(ca, 3));
    m.visible = false;
    hand.add(m);
    c.props[name] = m;
    return m;
  };
  if (o.props) {
    P('suitcase', boxG(0.14, 0.42, 0.62, 0, -0.26, 0), '#5a4028');
    P('bag', boxG(0.24, 0.26, 0.56, 0, -0.2, 0), '#1d2a22');
    P('cosh', boxG(0.045, 0.045, 0.36, 0, -0.02, 0.16), '#141414');
    P('flick knife', boxG(0.018, 0.03, 0.2, 0, -0.01, 0.1), '#c8c8c8');
    P('brick', boxG(0.1, 0.07, 0.21, 0, -0.02, 0.05), '#6e3327');
    P('chair', boxG(0.36, 0.5, 0.36, 0, -0.2, 0.2), '#7a2a22');
    P('wheel brace', boxG(0.03, 0.03, 0.42, 0, -0.02, 0.18), '#777');
    P('cargo hook', boxG(0.03, 0.06, 0.3, 0, -0.02, 0.14), '#3a3530');
    P('dustbin lid', boxG(0.5, 0.5, 0.04, 0, 0, 0.1), '#6f7478');
  }
  if (o.cig !== false) {
    const cg = new THREE.Mesh(
      new THREE.BoxGeometry(0.012, 0.012, 0.07),
      new THREE.MeshBasicMaterial({ color: new THREE.Color(2.5, 1.2, 0.4) }),
    );
    cg.position.set(0, 0, 0.05);
    cg.visible = false;
    hand.add(cg);
    c.props.cig = cg;
  }
  return c;
}
export function holdProp(c, name) {
  for (const k in c.props) c.props[k].visible = k === name;
}

const Z = () => [0, 0, 0];
// a: { v, run, mode, hurt, limp, look (world yaw or null), ang (body yaw), talk, breath }
export function poseChar(c, a, dt) {
  const R = c.cur.map(Z);
  let hipY = c.hipH,
    hipX = 0;
  const t = (c.t += dt),
    s = c.s,
    hurt = a.hurt || 0,
    mode = a.mode || 'stand';
  const B = BONE,
    v = a.v || 0,
    moving = v > 0.15 && mode !== 'sit' && mode !== 'down';
  R[B.spine][0] = c.stoop + hurt * 0.22;
  const br =
    Math.sin(t * (1.5 + hurt * 2.2 + (a.puff || 0) * 2.5)) * (0.012 + hurt * 0.02 + (a.puff || 0) * 0.02);
  R[B.chest][0] = br;
  R[B.armL][2] = 0.06;
  R[B.armR][2] = -0.06;
  if (moving) {
    const run = a.run,
      w = (2 * Math.PI * v) / ((run ? 2.5 : 1.42) * s);
    c.phase += dt * w;
    const p = c.phase,
      A = run ? 0.85 : 0.5 * (c.frail ? 0.7 : 1),
      lp = a.limp || 0;
    R[B.thighL][0] = -A * Math.sin(p);
    R[B.thighR][0] = A * Math.sin(p) * (1 - lp * 0.55);
    R[B.shinL][0] = (run ? 1.5 : 0.75) * Math.max(0, Math.cos(p));
    R[B.shinR][0] = (run ? 1.5 : 0.75) * Math.max(0, -Math.cos(p)) * (1 - lp * 0.6);
    R[B.armL][0] = A * 0.75 * Math.sin(p);
    R[B.armR][0] = -A * 0.75 * Math.sin(p);
    R[B.foreL][0] = -(run ? 1.3 : 0.22) - 0.25 * Math.max(0, Math.sin(p));
    R[B.foreR][0] = -(run ? 1.3 : 0.22) - 0.25 * Math.max(0, -Math.sin(p));
    R[B.spine][1] = 0.07 * Math.sin(p);
    R[B.chest][1] = -0.12 * Math.sin(p);
    R[B.spine][0] += run ? 0.24 : 0.03;
    R[B.hips][2] = 0.035 * Math.sin(p) + lp * 0.09 * Math.max(0, -Math.sin(p));
    hipY -= (run ? 0.05 : 0.022) * s * Math.abs(Math.sin(p)) + lp * 0.03 * Math.max(0, -Math.sin(p));
  } else if (mode === 'stand') {
    R[B.hips][2] = Math.sin(t * 0.5) * 0.015;
    R[B.foreL][0] = -0.12;
    R[B.foreR][0] = -0.12;
  }
  if (mode === 'sit' || mode === 'mend') {
    hipY = 0.5 * s;
    R[B.thighL][0] = R[B.thighR][0] = -1.5;
    R[B.shinL][0] = R[B.shinR][0] = 1.45;
    R[B.armL][0] = R[B.armR][0] = -0.55;
    R[B.foreL][0] = R[B.foreR][0] = -0.95;
    R[B.spine][0] += 0.05;
    if (mode === 'mend') {
      R[B.foreR][0] = -1.3 + Math.sin(t * 3.2) * 0.25;
      R[B.foreL][0] = -1.2;
      R[B.spine][0] += 0.2;
      R[B.head][0] = 0.3;
    }
  } else if (mode === 'down') {
    hipY = 0.2;
    R[B.hips][0] = -1.5;
    R[B.armL][2] = 1.1;
    R[B.armR][2] = -0.9;
    R[B.thighL][0] = -0.2;
    R[B.shinR][0] = 0.5;
    R[B.spine][0] = 0;
  } else if (mode === 'smoke') {
    const k = t % 7 < 1.6 ? 1 : 0;
    R[B.armR][0] = -0.55 * k - 0.1;
    R[B.foreR][0] = -2.05 * k - 0.2;
    R[B.armL][0] = -0.2;
    R[B.foreL][0] = -1.3;
    R[B.armL][2] = -0.3;
  } else if (mode === 'paint') {
    R[B.armR][0] = -2.5 + Math.sin(t * 2.2) * 0.22;
    R[B.foreR][0] = -0.3;
    R[B.armR][2] = Math.sin(t * 1.1) * 0.2;
    R[B.head][0] = -0.35;
    R[B.spine][0] = -0.05;
  } else if (mode === 'work') {
    R[B.armR][0] = -0.6 + Math.sin(t * 1.7) * 0.25;
    R[B.foreR][0] = -1.1 + Math.sin(t * 2.3) * 0.3;
    R[B.armL][0] = -0.5;
    R[B.foreL][0] = -1.0 + Math.sin(t * 1.3) * 0.2;
  } else if (mode === 'carry' && !moving) {
    R[B.foreR][0] = -0.05;
  } else if (mode === 'guard') {
    R[B.armL][0] = -0.85;
    R[B.foreL][0] = -1.75;
    R[B.armR][0] = -0.6;
    R[B.foreR][0] = -1.95;
    R[B.spine][0] += 0.12;
    R[B.chest][1] = 0.3;
    R[B.thighL][0] = -0.25;
    R[B.thighR][0] = 0.2;
    R[B.shinR][0] = 0.3;
    hipY -= 0.04;
  } else if (mode === 'windup') {
    R[B.chest][1] = 0.75;
    R[B.spine][1] = 0.3;
    R[B.armR][0] = 0.75;
    R[B.foreR][0] = -2.0;
    R[B.armL][0] = -0.9;
    R[B.foreL][0] = -1.6;
    R[B.thighL][0] = -0.3;
    R[B.thighR][0] = 0.25;
    hipY -= 0.05;
  } else if (mode === 'heavy') {
    R[B.chest][1] = 1.05;
    R[B.spine][1] = 0.45;
    R[B.armR][0] = 1.2;
    R[B.foreR][0] = -1.6;
    R[B.armL][0] = -0.8;
    R[B.foreL][0] = -1.5;
    R[B.thighR][0] = 0.4;
    R[B.shinR][0] = 0.4;
    hipY -= 0.08;
  } else if (mode === 'strike') {
    R[B.chest][1] = -0.7;
    R[B.spine][1] = -0.25;
    R[B.armR][0] = -1.55;
    R[B.foreR][0] = -0.12;
    R[B.armL][0] = -0.5;
    R[B.foreL][0] = -1.9;
    R[B.spine][0] += 0.2;
    R[B.thighL][0] = -0.45;
    R[B.thighR][0] = 0.3;
    hipY -= 0.04;
  } else if (mode === 'block') {
    R[B.armL][0] = -1.35;
    R[B.foreL][0] = -2.0;
    R[B.armR][0] = -1.35;
    R[B.foreR][0] = -2.0;
    R[B.armL][2] = -0.3;
    R[B.armR][2] = 0.3;
    R[B.head][0] = 0.35;
    R[B.spine][0] += 0.18;
    hipY -= 0.06;
  } else if (mode === 'stagger') {
    R[B.spine][0] = -0.4;
    R[B.head][0] = -0.3;
    R[B.armL][2] = 0.9;
    R[B.armR][2] = -0.9;
    R[B.thighL][0] = 0.3;
    R[B.shinL][0] = 0.3;
    hipY -= 0.05;
  } else if (mode === 'shove') {
    R[B.armL][0] = R[B.armR][0] = -1.45;
    R[B.foreL][0] = R[B.foreR][0] = -0.15;
    R[B.spine][0] += 0.25;
    R[B.thighR][0] = 0.3;
  } else if (mode === 'point') {
    R[B.armR][0] = -1.4;
    R[B.foreR][0] = -0.1 + Math.sin(t * 8) * 0.06;
    R[B.spine][0] += 0.16;
    R[B.head][0] = 0.08;
  } else if (mode === 'square') {
    R[B.spine][0] = -0.08 + hurt * 0.1;
    R[B.chest][0] = -0.08;
    R[B.armL][2] = 0.4;
    R[B.armR][2] = -0.4;
    R[B.foreL][0] = R[B.foreR][0] = -0.4;
    R[B.head][0] = -0.12;
  } else if (mode === 'stare') {
    R[B.head][0] = 0.06;
    R[B.spine][0] += 0.04;
  } else if (mode === 'cower') {
    R[B.spine][0] = 0.4;
    R[B.armL][0] = R[B.armR][0] = -1.0;
    R[B.foreL][0] = R[B.foreR][0] = -2.1;
    R[B.head][0] = 0.4;
    hipY -= 0.12;
    R[B.thighL][0] = R[B.thighR][0] = -0.3;
    R[B.shinL][0] = R[B.shinR][0] = 0.6;
  }
  if (a.talk && mode === 'stand' && !moving) {
    R[B.armR][0] = -0.35;
    R[B.foreR][0] = -1.15 + Math.sin(t * 5.5) * 0.25;
    R[B.armR][2] = -0.15 + Math.sin(t * 2.7) * 0.1;
    R[B.head][0] = Math.sin(t * 3.1) * 0.05;
  }
  if (hurt > 0.45 && mode !== 'down') {
    R[B.armL][0] = -0.35;
    R[B.foreL][0] = -1.55;
    R[B.armL][2] = -0.45;
  }
  if (a.carry && !['guard', 'windup', 'heavy', 'strike', 'block'].includes(mode)) {
    R[B.armR][0] = moving ? R[B.armR][0] * 0.25 : 0;
    R[B.foreR][0] = -0.05;
    R[B.armR][2] = -0.1;
  }
  if (a.look != null && mode !== 'down') {
    const d = angDiff(a.ang, a.look);
    if (Math.abs(d) < 1.7) {
      R[B.head][1] = clamp(d, -1.0, 1.0) * 0.75;
      R[B.neck][1] = clamp(d, -1.0, 1.0) * 0.25;
    }
  }
  const k = 1 - Math.exp(-dt * (a.snap || 13));
  for (let i = 0; i < 13; i++) {
    const cu = c.cur[i],
      r = R[i],
      b = c.bones[i];
    cu[0] += (r[0] - cu[0]) * k;
    cu[1] += (r[1] - cu[1]) * k;
    cu[2] += (r[2] - cu[2]) * k;
    b.rotation.set(cu[0], cu[1], cu[2]);
  }
  c.hy += (hipY - c.hy) * k;
  c.bones[0].position.y = c.hy;
  c.bones[0].position.x = hipX;
  if (c.props.cig) c.props.cig.visible = mode === 'smoke';
}
