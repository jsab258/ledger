// People: Quaternius' Universal Base Characters driven by the Universal Animation Library (both CC0),
// dressed by the tailor for 1990, with the game's posture layer (stoop, breath, guarding arm, limp, a look) laid over the clips.
import { THREE, lit, boxG } from './core.js';
import { tailor, headwear, extras, merge, cluster, weld, SLOT, BN } from './tailor.js';
import { SKINS } from '../cast.js';

const NB = 23,
  V3 = THREE.Vector3,
  Q4 = THREE.Quaternion;
const PP = { ready: false, mat: null, propMat: null, lod: 26 };
export const peopleReady = () => PP.ready;
export const peopleInfo = () => PP;
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v),
  sstep = (a, b, v) => {
    const t = clamp((v - a) / (b - a), 0, 1);
    return t * t * (3 - 2 * t);
  };
const UVR = {
    skinM: [0, 0, 0.5],
    skinF: [0.5, 0, 0.5],
    hair1: [0, 0.5, 0.25],
    hair2: [0.25, 0.5, 0.25],
    eye: [0.5, 0.5, 0.125],
  },
  WHITE_UV = [0.93, 0.93];
const UPPER = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
  ALL = Array.from({ length: NB }, (_, i) => i),
  PARENT = new Int8Array(NB);
const lin = (hex) => {
  const c = new THREE.Color(hex);
  return [c.r, c.g, c.b];
};

export async function loadPeople(lowTex) {
  const res = await fetch('people.txt');
  if (!res.ok) throw new Error('people.txt ' + res.status);
  const bin = atob((await res.text()).trim()),
    u8 = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
  if (bin.slice(0, 4) !== 'LGR1') throw new Error('not a LEDGER people file');
  const dv = new DataView(u8.buffer),
    jl = dv.getUint32(4, true),
    H = JSON.parse(new TextDecoder().decode(u8.subarray(8, 8 + jl))),
    base = 8 + jl;
  const TA = { Float32Array, Int8Array, Uint8Array, Uint16Array, Int16Array, Uint32Array };
  const arr = (name) => {
    const [off, len, type] = H.dir[name],
      C = TA[type];
    return new C(u8.buffer.slice(base + off, base + off + len * C.BYTES_PER_ELEMENT));
  };
  const getMesh = (name, slot) => {
    const m = H.meshes[name],
      n = m.n,
      r = UVR[m.tex],
      nq = arr(name + '.nor'),
      uq = arr(name + '.uv'),
      w8 = arr(name + '.bw'),
      nor = new Float32Array(n * 3),
      uv = new Float32Array(n * 2),
      bw = new Float32Array(n * 4);
    for (let i = 0; i < n * 3; i++) nor[i] = nq[i] / 127;
    for (let i = 0; i < n * 4; i++) bw[i] = w8[i] / 255;
    for (let i = 0; i < n; i++) {
      uv[i * 2] = r[0] + (uq[i * 2] / 32767.5) * r[2];
      uv[i * 2 + 1] = r[1] + (uq[i * 2 + 1] / 32767.5) * r[2];
    }
    return {
      n,
      pos: arr(name + '.pos'),
      nor,
      uv,
      bi: arr(name + '.bi'),
      bw,
      idx: Uint32Array.from(arr(name + '.idx')),
      slot: new Uint8Array(n).fill(slot),
    };
  };
  const hairSrc = {};
  for (const k of ['parted', 'buzz', 'beard', 'buzzf', 'long', 'buns']) {
    hairSrc[k] = getMesh('hair_' + k, SLOT.hair);
    hairSrc[k].sex = H.meshes['hair_' + k].sex;
  }
  for (const sex of ['M', 'F']) {
    const rest = H.rests[sex],
      W = [],
      one = new V3(1, 1, 1);
    rest.forEach((b, i) => {
      PARENT[i] = b.parent;
      const m = new THREE.Matrix4().compose(new V3(...b.t), new Q4(...b.r), one);
      W[i] = b.parent >= 0 ? W[b.parent].clone().multiply(m) : m;
    });
    const joints = W.map((m) => {
      const p = new V3().setFromMatrixPosition(m);
      return [p.x, p.y, p.z];
    });
    const body = getMesh(sex + '_body', SLOT.skin),
      eyes = getMesh(sex + '_eyes', SLOT.eye),
      brows = getMesh(sex + '_brows', SLOT.brow),
      T = tailor(body, joints, sex);
    let ex = 0,
      ey = 0,
      ez = -9;
    for (let i = 0; i < eyes.n; i++) {
      ex += Math.abs(eyes.pos[i * 3]);
      ey += eyes.pos[i * 3 + 1];
      ez = Math.max(ez, eyes.pos[i * 3 + 2]);
    }
    PP[sex] = {
      sex,
      rest,
      joints,
      body,
      eyes,
      brows,
      T,
      face: { eyeX: ex / eyes.n, eyeY: ey / eyes.n, eyeZ: ez },
      height: T.L.top,
      restT: rest.map((b) => b.t),
      restQ: rest.map((b) => b.r),
    };
  }
  // hair made for one head, moved onto the other
  for (const sex of ['M', 'F']) {
    const D = PP[sex],
      set = { _head: D.T.wb };
    for (const k in hairSrc) {
      const h = hairSrc[k];
      if (h.sex === sex) {
        set[k] = h;
        continue;
      }
      const S = PP[h.sex],
        dy = D.face.eyeY - S.face.eyeY,
        dz = D.joints[BN.head][2] - S.joints[BN.head][2],
        c = Object.assign({}, h, { pos: Float32Array.from(h.pos) });
      for (let i = 0; i < c.n; i++) {
        c.pos[i * 3 + 1] += dy;
        c.pos[i * 3 + 2] += dz;
      }
      set[k] = c;
    }
    D.hair = set;
  }
  // clips, carried onto each body as offsets from its own rest pose
  const q = new Q4();
  for (const sex of ['M', 'F']) {
    const D = PP[sex],
      C = D.rest.map((b, i) => new Q4(...b.r).multiply(new Q4(...H.restU[i].r).invert())),
      sp = new V3(...D.rest[1].t),
      up = new V3(...H.restU[1].t),
      k = sp.length() / up.length();
    D.clips = {};
    for (const name in H.clips) {
      const cl = H.clips[name],
        q16 = arr('clip.' + name + '.q'),
        p = arr('clip.' + name + '.p'),
        n = cl.n,
        qo = new Float32Array(n * NB * 4),
        po = new Float32Array(n * 3);
      for (let f = 0; f < n; f++) {
        for (let b = 0; b < NB; b++) {
          const o = (f * NB + b) * 4;
          q.set(q16[o] / 32767, q16[o + 1] / 32767, q16[o + 2] / 32767, q16[o + 3] / 32767)
            .normalize()
            .premultiply(C[b]);
          q.toArray(qo, o);
        }
        po[f * 3] = sp.x + (p[f * 3] - up.x) * k;
        po[f * 3 + 1] = sp.y + (p[f * 3 + 1] - up.y) * k;
        po[f * 3 + 2] = sp.z + (p[f * 3 + 2] - up.z) * k;
      }
      D.clips[name] = { name, n, dur: cl.dur, q: qo, p: po };
    }
    // measure the clips once: how fast each gait covers ground, when the cross lands, how the hand sits at rest
    const Q = new Float32Array(NB * 4),
      P = [0, 0, 0],
      wq = new Q4(),
      wp = new V3();
    D.speed = {};
    for (const g of ['Walk_Loop', 'Walk_Formal_Loop', 'Jog_Fwd_Loop', 'Sprint_Loop']) {
      let lo = 9,
        hi = -9;
      for (let s = 0; s < 24; s++) {
        sample(D.clips[g], (s / 24) * D.clips[g].dur, true, Q, P);
        fk(D, Q, P, BN.footL, wq, wp);
        lo = Math.min(lo, wp.z);
        hi = Math.max(hi, wp.z);
      }
      D.speed[g] = (2 * (hi - lo) * 0.92) / D.clips[g].dur;
    }
    let best = -9;
    D.peak = 0.4;
    for (let s = 0; s < 40; s++) {
      const t = (s / 40) * D.clips.Punch_Cross.dur;
      sample(D.clips.Punch_Cross, t, false, Q, P);
      fk(D, Q, P, BN.handR, wq, wp);
      if (wp.z > best) {
        best = wp.z;
        D.peak = t;
      }
    }
    sample(D.clips.Idle_Loop, 0, true, Q, P);
    fk(D, Q, P, BN.handR, wq, wp);
    D.handFix = wq.clone().invert();
  }
  const tex = await new THREE.TextureLoader().loadAsync(lowTex ? 'people_lo.jpg' : 'people.jpg');
  tex.flipY = false;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  tex.needsUpdate = true;
  PP.mat = lit(
    new THREE.MeshLambertMaterial({
      vertexColors: true,
      map: tex,
      side: THREE.DoubleSide,
      color: new THREE.Color(1 / GAIN, 1 / GAIN, 1 / GAIN),
    }),
    { gain: 0.6 },
  );
  PP.propMat = lit(new THREE.MeshLambertMaterial({ vertexColors: true }));
  PP.ready = true;
  return PP;
}

// ---------- pose maths on plain arrays ----------
function sample(cl, time, loop, Q, P) {
  const tt = loop ? ((time % cl.dur) + cl.dur) % cl.dur : clamp(time, 0, cl.dur),
    ft = (tt / cl.dur) * (cl.n - 1),
    f0 = Math.floor(ft),
    f1 = Math.min(cl.n - 1, f0 + 1),
    u = ft - f0,
    a = cl.q,
    o0 = f0 * NB * 4,
    o1 = f1 * NB * 4;
  for (let b = 0; b < NB * 4; b += 4) {
    const d =
        a[o0 + b] * a[o1 + b] +
        a[o0 + b + 1] * a[o1 + b + 1] +
        a[o0 + b + 2] * a[o1 + b + 2] +
        a[o0 + b + 3] * a[o1 + b + 3],
      s = d < 0 ? -u : u,
      v = 1 - u;
    let x = a[o0 + b] * v + a[o1 + b] * s,
      y = a[o0 + b + 1] * v + a[o1 + b + 1] * s,
      z = a[o0 + b + 2] * v + a[o1 + b + 2] * s,
      w = a[o0 + b + 3] * v + a[o1 + b + 3] * s;
    const l = 1 / Math.hypot(x, y, z, w);
    Q[b] = x * l;
    Q[b + 1] = y * l;
    Q[b + 2] = z * l;
    Q[b + 3] = w * l;
  }
  if (P) for (let c = 0; c < 3; c++) P[c] = cl.p[f0 * 3 + c] * (1 - u) + cl.p[f1 * 3 + c] * u;
}
function mix(Q, R, w, bones) {
  // Q toward R by w on the listed bones
  for (const bi of bones) {
    const b = bi * 4,
      d = Q[b] * R[b] + Q[b + 1] * R[b + 1] + Q[b + 2] * R[b + 2] + Q[b + 3] * R[b + 3],
      s = d < 0 ? -w : w,
      v = 1 - w;
    const x = Q[b] * v + R[b] * s,
      y = Q[b + 1] * v + R[b + 1] * s,
      z = Q[b + 2] * v + R[b + 2] * s,
      ww = Q[b + 3] * v + R[b + 3] * s,
      l = 1 / (Math.hypot(x, y, z, ww) || 1);
    Q[b] = x * l;
    Q[b + 1] = y * l;
    Q[b + 2] = z * l;
    Q[b + 3] = ww * l;
  }
}
const _a = new Q4(),
  _b = new Q4(),
  _r = new Q4(),
  _p = new V3(),
  _t = new V3();
function worldQ(Q, bone, out) {
  out.set(Q[bone * 4], Q[bone * 4 + 1], Q[bone * 4 + 2], Q[bone * 4 + 3]);
  for (let p = PARENT[bone]; p >= 0; p = PARENT[p])
    out.premultiply(_b.set(Q[p * 4], Q[p * 4 + 1], Q[p * 4 + 2], Q[p * 4 + 3]));
  return out;
}
function fk(D, Q, P, bone, wq, wp) {
  const chain = [];
  for (let b = bone; b >= 0; b = PARENT[b]) chain.push(b);
  wq.set(0, 0, 0, 1);
  wp.set(0, 0, 0);
  for (let i = chain.length - 1; i >= 0; i--) {
    const b = chain[i],
      t = b === 1 ? P : D.restT[b];
    _t.set(t[0], t[1], t[2]).applyQuaternion(wq);
    wp.add(_t);
    wq.multiply(_b.set(Q[b * 4], Q[b * 4 + 1], Q[b * 4 + 2], Q[b * 4 + 3]));
  }
}
const AX = { x: new V3(1, 0, 0), y: new V3(0, 1, 0), z: new V3(0, 0, 1) };
// turn one bone about an axis of the figure's own space, whatever its local axes are
function twist(Q, bone, axis, ang) {
  if (Math.abs(ang) < 1e-4) return;
  worldQ(Q, bone, _a);
  _r.setFromAxisAngle(AX[axis], ang);
  _b.copy(_a).invert().multiply(_r).multiply(_a);
  _a.set(Q[bone * 4], Q[bone * 4 + 1], Q[bone * 4 + 2], Q[bone * 4 + 3])
    .multiply(_b)
    .normalize();
  Q[bone * 4] = _a.x;
  Q[bone * 4 + 1] = _a.y;
  Q[bone * 4 + 2] = _a.z;
  Q[bone * 4 + 3] = _a.w;
}

// ---------- building a figure ----------
const GAIN = 0.68; // the skin texture averages this bright; the material's colour lifts everything back
const HATS = { flatcap: 1, woolly: 1, headscarf: 1, rainhood: 1, helmet: 1 };
export function buildCharR(look, o = {}) {
  const sex = o.sex === 'f' ? 'F' : 'M',
    D = PP[sex],
    age = o.age || 30,
    scale = clamp((look.h || 1.75) / D.height, 0.84, 1.1),
    fat = 0.94 + 0.2 * clamp(look.b ?? 0.4, 0, 1);
  const mesh = new THREE.Group(),
    arm = new THREE.Group();
  arm.scale.set(scale * fat, scale, scale * fat);
  mesh.add(arm);
  const bones = D.rest.map((b) => {
    const bn = new THREE.Bone();
    bn.name = b.name;
    bn.position.set(...b.t);
    bn.quaternion.set(...b.r);
    return bn;
  });
  D.rest.forEach((b, i) => {
    if (b.parent >= 0) bones[b.parent].add(bones[i]);
  });
  bones[0].updateMatrixWorld(true);
  const skel = new THREE.Skeleton(bones);
  arm.add(bones[0]);
  const c = {
    mesh,
    arm,
    bones,
    skel,
    sex,
    look,
    o,
    scale,
    props: {},
    held: null,
    t: Math.random() * 10,
    seed: Math.random(),
    old: age > 62,
    stoop: age > 70 ? 0.2 : age > 60 ? 0.09 : 0,
    frail: o.frail,
    formal: look.top[0] === 'tunic' || look.top[0] === 'cassock' || age > 66,
    an: {
      base: null,
      t: 0,
      prev: null,
      prevT: 0,
      fade: 1,
      act: null,
      actT: 0,
      actW: 0,
      talkW: 0,
      yaw: 0,
      O: new Float32Array(NB * 4),
      hasO: false,
    },
    Q: new Float32Array(NB * 4),
    P: [0, 0, 0],
    near: null,
    far: null,
    lodFar: false,
    tick: 0,
    acc: 0,
  };
  const hand = new THREE.Group();
  hand.quaternion.copy(D.handFix);
  const hold = new THREE.Group();
  hold.position.set(0, 0.085, 0);
  hold.add(hand);
  bones[BN.handR].add(hold);
  c.hand = hand;
  const _c = new THREE.Color(),
    Pm = (name, g, col) => {
      const m = new THREE.Mesh(g, PP.propMat),
        n = g.attributes.position.count,
        ca = new Float32Array(n * 3);
      _c.set(col);
      for (let i = 0; i < n; i++) {
        ca[i * 3] = _c.r;
        ca[i * 3 + 1] = _c.g;
        ca[i * 3 + 2] = _c.b;
      }
      g.setAttribute('color', new THREE.BufferAttribute(ca, 3));
      m.visible = false;
      m.scale.setScalar(1 / scale);
      hand.add(m);
      c.props[name] = m;
      return m;
    };
  if (o.props) {
    Pm('suitcase', boxG(0.14, 0.42, 0.62, 0, -0.26, 0), '#5a4028');
    Pm('bag', boxG(0.24, 0.26, 0.56, 0, -0.2, 0), '#1d2a22');
    Pm('cosh', boxG(0.045, 0.045, 0.36, 0, -0.02, 0.16), '#141414');
    Pm('flick knife', boxG(0.018, 0.03, 0.2, 0, -0.01, 0.1), '#c8c8c8');
    Pm('brick', boxG(0.1, 0.07, 0.21, 0, -0.02, 0.05), '#6e3327');
    Pm('chair', boxG(0.36, 0.5, 0.36, 0, -0.2, 0.2), '#7a2a22');
    Pm('wheel brace', boxG(0.03, 0.03, 0.42, 0, -0.02, 0.18), '#777');
    Pm('cargo hook', boxG(0.03, 0.06, 0.3, 0, -0.02, 0.14), '#3a3530');
    Pm('dustbin lid', boxG(0.5, 0.5, 0.04, 0, 0, 0.1), '#6f7478');
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
function geometry(g, pal, src) {
  // tailor mesh -> buffers; src picks a subset of vertices (far figures)
  const n = src ? src.length : g.n,
    pos = new Float32Array(n * 3),
    nor = new Int8Array(n * 4),
    uv = new Uint16Array(n * 2),
    col = new Uint8Array(n * 4),
    si = new Uint8Array(n * 4),
    sw = new Uint8Array(n * 4);
  for (let j = 0; j < n; j++) {
    const i = src ? src[j] : j,
      p = pal[g.slot[i]];
    pos[j * 3] = g.pos[i * 3];
    pos[j * 3 + 1] = g.pos[i * 3 + 1];
    pos[j * 3 + 2] = g.pos[i * 3 + 2];
    nor[j * 4] = g.nor[i * 3] * 127;
    nor[j * 4 + 1] = g.nor[i * 3 + 1] * 127;
    nor[j * 4 + 2] = g.nor[i * 3 + 2] * 127;
    uv[j * 2] = g.uv[i * 2] * 65535;
    uv[j * 2 + 1] = g.uv[i * 2 + 1] * 65535;
    col[j * 4] = Math.min(255, p[0] * 255 + 0.5);
    col[j * 4 + 1] = Math.min(255, p[1] * 255 + 0.5);
    col[j * 4 + 2] = Math.min(255, p[2] * 255 + 0.5);
    col[j * 4 + 3] = 255;
    let s = 0;
    for (let k = 0; k < 4; k++) {
      si[j * 4 + k] = g.bi[i * 4 + k];
      sw[j * 4 + k] = Math.round(g.bw[i * 4 + k] * 255);
      s += sw[j * 4 + k];
    }
    sw[j * 4] += 255 - s;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(nor, 4, true));
  geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2, true));
  geo.setAttribute('color', new THREE.BufferAttribute(col, 4, true));
  geo.setAttribute('skinIndex', new THREE.BufferAttribute(si, 4));
  geo.setAttribute('skinWeight', new THREE.BufferAttribute(sw, 4, true));
  geo.boundingSphere = new THREE.Sphere(new V3(0, 0.9, 0), 1.9);
  geo.boundingBox = new THREE.Box3(new V3(-1.2, -0.2, -1.2), new V3(1.2, 2, 1.2));
  return geo;
}
function realise(c) {
  const D = PP[c.sex],
    T = D.T,
    lk = c.look,
    hk = lk.hair[0],
    x = lk.x || [],
    top = T.top(lk.top[0]),
    bot = lk.top[0] === 'cassock' ? null : T.bottom(lk.bot[0]),
    sh = T.shoes(lk.bot[0] === 'trackies' ? 'trainer' : 'shoe');
  const hat = headwear(hk, D.hair, T.L, D.face, c.sex),
    ex = extras(x, T.L, D.face, c.sex),
    beard = x.includes('beard') ? weld(D.hair.beard, SLOT.hair) : null;
  // the body, less whatever the clothes cover
  const B = D.body,
    hide = new Uint8Array(B.n);
  for (const g of [top, bot, sh]) if (g) for (let i = 0; i < B.n; i++) hide[i] |= g.hide[i];
  const id = [];
  for (let t = 0; t < B.idx.length; t += 3) {
    const a = B.idx[t],
      b = B.idx[t + 1],
      d = B.idx[t + 2];
    if (!(hide[a] && hide[b] && hide[d])) id.push(a, b, d);
  }
  const used = new Int32Array(B.n).fill(-1),
    keep = [];
  for (let i = 0; i < id.length; i++) {
    if (used[id[i]] < 0) {
      used[id[i]] = keep.length;
      keep.push(id[i]);
    }
    id[i] = used[id[i]];
  }
  const sub = {
    n: keep.length,
    pos: new Float32Array(keep.length * 3),
    nor: new Float32Array(keep.length * 3),
    uv: new Float32Array(keep.length * 2),
    bi: new Uint8Array(keep.length * 4),
    bw: new Float32Array(keep.length * 4),
    slot: new Uint8Array(keep.length).fill(SLOT.skin),
    idx: Uint32Array.from(id),
  };
  keep.forEach((i, j) => {
    sub.pos.set(B.pos.subarray(i * 3, i * 3 + 3), j * 3);
    sub.nor.set(B.nor.subarray(i * 3, i * 3 + 3), j * 3);
    sub.uv.set(B.uv.subarray(i * 2, i * 2 + 2), j * 2);
    sub.bi.set(B.bi.subarray(i * 4, i * 4 + 4), j * 4);
    sub.bw.set(B.bw.subarray(i * 4, i * 4 + 4), j * 4);
  });
  const parts = [sub, D.eyes, D.brows, hat, beard, top, bot, sh, ex].filter(Boolean),
    g = merge(parts);
  g.uv = new Float32Array(g.n * 2);
  let at = 0;
  for (const m of parts) {
    for (let i = 0; i < m.n; i++) {
      g.uv[(at + i) * 2] = m.uv ? m.uv[i * 2] : WHITE_UV[0];
      g.uv[(at + i) * 2 + 1] = m.uv ? m.uv[i * 2 + 1] : WHITE_UV[1];
    }
    at += m.n;
  }
  const hatCol = HATS[hk] ? lin(lk.hair[1]) : null,
    hairCol = HATS[hk] ? lin(c.old ? '#8f8a80' : '#3a2a1c') : lin(lk.hair[1]),
    skin = lin(SKINS[lk.skin % SKINS.length] || SKINS[0]),
    pal = [];
  pal[SLOT.skin] = skin;
  pal[SLOT.hair] = hairCol;
  pal[SLOT.top] = lin(lk.top[1]);
  pal[SLOT.top2] = lin(lk.top[2] || '#d8d2c2');
  pal[SLOT.bot] = lin(lk.bot[1]);
  pal[SLOT.shoe] = lin(lk.bot[0] === 'trackies' ? '#cfcfc6' : c.sex === 'F' ? '#2a2420' : '#17161a');
  pal[SLOT.eye] = [1, 1, 1];
  pal[SLOT.dark] = lin(x.includes('bag') ? '#3a2a1c' : '#15151a');
  pal[SLOT.brow] = hairCol.map((v, k) => v * 0.45 + skin[k] * (c.sex === 'F' ? 0.5 : 0.3));
  pal[SLOT.hat] = hatCol || hairCol;
  pal[SLOT.gold] = lin('#b89a3a');
  for (let k = 0; k < pal.length; k++) if (pal[k] && k !== SLOT.skin) pal[k] = pal[k].map((v) => v * GAIN);
  const near = new THREE.SkinnedMesh(geometry(g, pal), PP.mat);
  near.geometry.setIndex(new THREE.BufferAttribute(g.n < 65536 ? Uint16Array.from(g.idx) : g.idx, 1));
  const cl = cluster(g, 0.05),
    far = new THREE.SkinnedMesh(geometry(g, pal, cl.src), PP.mat);
  far.geometry.setIndex(new THREE.BufferAttribute(Uint16Array.from(cl.idx), 1));
  for (const m of [near, far]) {
    m.bind(c.skel, new THREE.Matrix4());
    m.frustumCulled = true;
    c.arm.add(m);
  }
  far.visible = false;
  c.near = near;
  c.far = far;
  c.tris = [g.idx.length / 3, cl.idx.length / 3];
}
export function realiseChar(c) {
  if (c.rigged && !c.near) realise(c);
}
export function holdPropR(c, name) {
  for (const k in c.props) c.props[k].visible = k === name;
}

// ---------- animating ----------
const Q2 = new Float32Array(NB * 4),
  P2 = [0, 0, 0],
  GUARD = { guard: 1, square: 1, block: 1 };
export function poseCharR(c, a, dt) {
  if (!c.near) realise(c);
  if (c.near.visible === c.lodFar) {
    c.near.visible = !c.lodFar;
    c.far.visible = c.lodFar;
  }
  if (c.lodFar) {
    c.acc += dt;
    if ((c.tick++ & 1) === 0) return;
    dt = c.acc;
    c.acc = 0;
  } // far figures move at half rate
  const A = c.an,
    D = PP[c.sex],
    mode = a.mode || 'stand',
    v = a.v || 0,
    Q = c.Q,
    P = c.P,
    hurt = a.hurt || 0;
  c.t += dt;
  const moving = v > 0.15 && mode !== 'sit' && mode !== 'down' && mode !== 'drive';
  let base = 'Idle_Loop',
    loop = true,
    rate = 1;
  if (mode === 'down') {
    base = 'Death01';
    loop = false;
  } else if (mode === 'sit') base = 'Sitting_Idle_Loop';
  else if (mode === 'drive') base = 'Driving_Loop';
  else if (moving) {
    base = a.run ? (v > 5.4 ? 'Sprint_Loop' : 'Jog_Fwd_Loop') : c.formal ? 'Walk_Formal_Loop' : 'Walk_Loop';
    rate = clamp(v / (D.speed[base] * c.scale), 0.45, 1.9);
  } else if (mode === 'mend' || mode === 'cower') base = 'Crouch_Idle_Loop';
  else if (mode === 'work' || mode === 'paint') {
    base = 'Interact';
    rate = 0.7;
  }
  if (base !== A.base) {
    const was = A.base && D.clips[A.base],
      now = D.clips[base],
      gait = /Walk|Jog|Sprint/;
    A.prev = A.base;
    A.prevT = A.t;
    A.t =
      was && gait.test(A.base) && gait.test(base)
        ? (A.t / was.dur) * now.dur
        : loop && A.base === null
          ? c.seed * now.dur
          : 0;
    A.base = base;
    A.fade = A.prev ? 0 : 1;
  }
  A.t += dt * rate;
  A.fade = Math.min(1, A.fade + dt / 0.24);
  sample(D.clips[base], A.t, loop, Q, P);
  if (A.fade < 1 && A.prev) {
    const pc = D.clips[A.prev];
    A.prevT += dt;
    sample(pc, A.prevT, A.prev !== 'Death01', Q2, P2);
    const w = 1 - sstep(0, 1, A.fade);
    mix(Q, Q2, w, ALL);
    for (let k = 0; k < 3; k++) P[k] += (P2[k] - P[k]) * w;
  }
  // talking hands
  A.talkW += ((a.talk && !moving && mode === 'stand' ? 0.8 : 0) - A.talkW) * Math.min(1, dt * 4);
  if (A.talkW > 0.02) {
    sample(D.clips.Idle_Talking_Loop, c.t, true, Q2, null);
    mix(Q, Q2, A.talkW, UPPER);
  }
  // the rungs of a fight, laid over whatever the legs are doing
  let act = null;
  if (mode === 'windup' || mode === 'strike') act = 'Punch_Cross';
  else if (GUARD[mode]) act = 'Punch_Jab';
  else if (mode === 'shove') act = 'Push_Loop';
  else if (mode === 'stagger') act = hurt > 0.55 ? 'Hit_Head' : 'Hit_Chest';
  if (act !== A.act) {
    if (act && act !== A.lastAct) A.actT = 0;
    A.act = act;
    if (act) A.lastAct = act;
  }
  A.actW += ((act ? 1 : 0) - A.actW) * Math.min(1, dt * (act ? 14 : 5));
  if (A.actW > 0.02 && A.lastAct) {
    const cl = D.clips[A.lastAct];
    let lp = false;
    if (mode === 'windup') A.actT = Math.min(A.actT + dt * 0.7, D.peak * 0.5);
    else if (mode === 'strike') A.actT = Math.min(cl.dur * 0.8, Math.max(A.actT, D.peak * 0.5) + dt * 1.7);
    else if (GUARD[mode]) A.actT = mode === 'block' ? 0.04 : 0;
    else if (mode === 'shove') {
      A.actT += dt * 1.5;
      lp = true;
    } else A.actT = Math.min(cl.dur, A.actT + dt);
    sample(cl, A.actT, lp, Q2, null);
    if (!A.hasO) {
      A.O.set(Q2);
      A.hasO = true;
    } else mix(A.O, Q2, Math.min(1, dt * (a.snap || 13) * 1.6), ALL);
    mix(Q, A.O, A.actW, mode === 'stagger' ? ALL : UPPER);
    if (mode === 'block') {
      twist(Q, BN.uarmL, 'x', -0.5 * A.actW);
      twist(Q, BN.uarmR, 'x', -0.5 * A.actW);
    }
  } else A.hasO = false;
  // posture over the clip: what a health bar would say, said with the body
  if (base === 'Idle_Loop' && !act) {
    twist(Q, BN.thighL, 'z', -0.085);
    twist(Q, BN.thighR, 'z', 0.085);
  } // townsfolk stand with their feet under them
  const st = c.stoop + hurt * 0.22 + (mode === 'stare' ? 0.07 : 0) + (mode === 'cower' ? 0.2 : 0);
  if (mode !== 'down') {
    if (st) {
      twist(Q, BN.sp1, 'x', st * 0.55);
      twist(Q, BN.sp3, 'x', st * 0.45);
      twist(Q, BN.head, 'x', -st * 0.35);
    }
    twist(
      Q,
      BN.sp3,
      'x',
      Math.sin(c.t * (1.5 + hurt * 2.2 + (a.puff || 0) * 2.5)) *
        (0.012 + hurt * 0.02 + (a.puff || 0) * 0.025),
    );
    let yaw = 0;
    if (a.look != null) {
      yaw = a.look - a.ang;
      while (yaw > Math.PI) yaw -= 2 * Math.PI;
      while (yaw < -Math.PI) yaw += 2 * Math.PI;
      yaw = clamp(yaw, -1.15, 1.15);
    }
    A.yaw += (yaw - A.yaw) * Math.min(1, dt * 5);
    if (Math.abs(A.yaw) > 0.01) {
      twist(Q, BN.sp3, 'y', A.yaw * 0.2);
      twist(Q, BN.neck, 'y', A.yaw * 0.3);
      twist(Q, BN.head, 'y', A.yaw * 0.5);
    }
    const g = act ? 0 : sstep(0.3, 0.75, hurt);
    if (g > 0.01) {
      twist(Q, BN.uarmR, 'y', 0.5 * g);
      twist(Q, BN.larmR, 'x', -1.25 * g);
      twist(Q, BN.larmR, 'y', 0.95 * g);
    }
    if (a.carry && !act) twist(Q, BN.larmR, 'x', -0.3);
    if (mode === 'smoke') {
      const k = sstep(0.55, 0.75, Math.sin(c.t * 0.55 + c.seed * 6));
      twist(Q, BN.uarmR, 'x', -0.55 * k);
      twist(Q, BN.larmR, 'x', -1.85 * k);
      twist(Q, BN.larmR, 'y', 0.35 * k);
    }
    if (mode === 'point') {
      twist(Q, BN.uarmR, 'x', -1.35);
      twist(Q, BN.larmR, 'x', -0.1);
    }
    if (mode === 'paint') twist(Q, BN.uarmR, 'x', -0.5);
    if (mode === 'cower') {
      twist(Q, BN.uarmL, 'x', -1.2);
      twist(Q, BN.uarmR, 'x', -1.2);
      twist(Q, BN.larmL, 'x', -1.3);
      twist(Q, BN.larmR, 'x', -1.3);
    }
    const lp = a.limp || 0;
    if (lp > 0.01 && moving) {
      const ph = (A.t / D.clips[base].dur) * Math.PI * 2,
        s = Math.max(0, Math.sin(ph + 1.2));
      P[2] -= lp * 0.035 * s;
      twist(Q, BN.sp1, 'z', lp * 0.1 * s);
      twist(Q, BN.thighR, 'x', lp * 0.12 * s);
    }
  }
  for (let i = 0; i < NB; i++) c.bones[i].quaternion.set(Q[i * 4], Q[i * 4 + 1], Q[i * 4 + 2], Q[i * 4 + 3]);
  c.bones[1].position.set(P[0], P[1], P[2]);
  if (c.props.cig) c.props.cig.visible = mode === 'smoke';
}
// tests and the frame-time panel
export function poseClip(c, name, t) {
  if (!c.near) realise(c);
  const D = PP[c.sex];
  sample(D.clips[name], t, false, c.Q, c.P);
  for (let i = 0; i < NB; i++) c.bones[i].quaternion.fromArray(c.Q, i * 4);
  c.bones[1].position.fromArray(c.P);
}
