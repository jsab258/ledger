// The tailor. 1990 clothes cut from the body they are worn on: each garment is a shell lifted off the skin
// (clipped at hem, cuff and collar, smoothed so cloth does not show muscle), or a draped tube for coats and skirts,
// and keeps the body's bone weights so it moves with the same skeleton. Pure arrays: runs in the page and in tests.
export const BN = {
  root: 0,
  pelvis: 1,
  sp1: 2,
  sp2: 3,
  sp3: 4,
  neck: 5,
  head: 6,
  clavL: 7,
  uarmL: 8,
  larmL: 9,
  handL: 10,
  clavR: 11,
  uarmR: 12,
  larmR: 13,
  handR: 14,
  thighL: 15,
  calfL: 16,
  footL: 17,
  ballL: 18,
  thighR: 19,
  calfR: 20,
  footR: 21,
  ballR: 22,
};
export const SLOT = {
  skin: 0,
  hair: 1,
  top: 2,
  top2: 3,
  bot: 4,
  shoe: 5,
  eye: 6,
  dark: 7,
  brow: 8,
  hat: 9,
  gold: 10,
};
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v),
  lerp = (a, b, t) => a + (b - a) * t,
  sstep = (a, b, v) => {
    const t = clamp((v - a) / (b - a), 0, 1);
    return t * t * (3 - 2 * t);
  };

// ---------- mesh basics ----------
export function mk(n, tris) {
  return {
    n,
    pos: new Float32Array(n * 3),
    nor: new Float32Array(n * 3),
    bi: new Uint8Array(n * 4),
    bw: new Float32Array(n * 4),
    slot: new Uint8Array(n),
    uv: null,
    idx: new Uint32Array(tris * 3),
  };
}
export function weld(m, slot = 0) {
  const map = new Map(),
    rm = new Uint32Array(m.n),
    src = [];
  let k = 0;
  for (let i = 0; i < m.n; i++) {
    const key =
      Math.round(m.pos[i * 3] * 20000) +
      ',' +
      Math.round(m.pos[i * 3 + 1] * 20000) +
      ',' +
      Math.round(m.pos[i * 3 + 2] * 20000);
    let j = map.get(key);
    if (j === undefined) {
      j = k++;
      map.set(key, j);
      src.push(i);
    }
    rm[i] = j;
  }
  const o = mk(k, 0);
  for (let j = 0; j < k; j++) {
    const i = src[j];
    o.pos.set(m.pos.subarray(i * 3, i * 3 + 3), j * 3);
    o.bi.set(m.bi.subarray(i * 4, i * 4 + 4), j * 4);
    o.bw.set(m.bw.subarray(i * 4, i * 4 + 4), j * 4);
    o.slot[j] = slot;
  }
  const id = [];
  for (let t = 0; t < m.idx.length; t += 3) {
    const a = rm[m.idx[t]],
      b = rm[m.idx[t + 1]],
      c = rm[m.idx[t + 2]];
    if (a !== b && b !== c && a !== c) id.push(a, b, c);
  }
  o.idx = Uint32Array.from(id);
  o.src = src;
  o.rm = rm;
  normals(o);
  return o;
}
export function normals(m) {
  const p = m.pos,
    nr = m.nor;
  nr.fill(0);
  for (let t = 0; t < m.idx.length; t += 3) {
    const a = m.idx[t] * 3,
      b = m.idx[t + 1] * 3,
      c = m.idx[t + 2] * 3;
    const ux = p[b] - p[a],
      uy = p[b + 1] - p[a + 1],
      uz = p[b + 2] - p[a + 2],
      vx = p[c] - p[a],
      vy = p[c + 1] - p[a + 1],
      vz = p[c + 2] - p[a + 2];
    const x = uy * vz - uz * vy,
      y = uz * vx - ux * vz,
      z = ux * vy - uy * vx;
    for (const q of [a, b, c]) {
      nr[q] += x;
      nr[q + 1] += y;
      nr[q + 2] += z;
    }
  }
  for (let i = 0; i < m.n * 3; i += 3) {
    const l = Math.hypot(nr[i], nr[i + 1], nr[i + 2]) || 1;
    nr[i] /= l;
    nr[i + 1] /= l;
    nr[i + 2] /= l;
  }
  return m;
}
function mixW(m, a, b, t, bi, bw) {
  // blend two vertices' bone weights, keep the four strongest
  const w = new Map();
  for (let k = 0; k < 4; k++) {
    if (m.bw[a * 4 + k] > 0)
      w.set(m.bi[a * 4 + k], (w.get(m.bi[a * 4 + k]) || 0) + m.bw[a * 4 + k] * (1 - t));
    if (m.bw[b * 4 + k] > 0) w.set(m.bi[b * 4 + k], (w.get(m.bi[b * 4 + k]) || 0) + m.bw[b * 4 + k] * t);
  }
  const e = [...w.entries()].sort((x, y) => y[1] - x[1]).slice(0, 4),
    s = e.reduce((x, y) => x + y[1], 0) || 1;
  for (let k = 0; k < 4; k++) {
    bi.push(e[k] ? e[k][0] : 0);
    bw.push(e[k] ? e[k][1] / s : 0);
  }
}
// keep the part of the mesh where f >= 0, cutting triangles cleanly along f = 0
export function clip(m, f) {
  const pos = [],
    bi = [],
    bw = [],
    slot = [],
    uv = m.uv ? [] : null,
    idx = [],
    old = new Int32Array(m.n).fill(-1),
    cut = new Map();
  let n = 0;
  const keep = (i) => {
    if (old[i] < 0) {
      old[i] = n++;
      pos.push(m.pos[i * 3], m.pos[i * 3 + 1], m.pos[i * 3 + 2]);
      for (let k = 0; k < 4; k++) {
        bi.push(m.bi[i * 4 + k]);
        bw.push(m.bw[i * 4 + k]);
      }
      slot.push(m.slot[i]);
      if (uv) uv.push(m.uv[i * 2], m.uv[i * 2 + 1]);
    }
    return old[i];
  };
  const split = (a, b) => {
    const key = a < b ? a * 1e6 + b : b * 1e6 + a;
    let j = cut.get(key);
    if (j !== undefined) return j;
    const t = f[a] / (f[a] - f[b]);
    j = n++;
    for (let c = 0; c < 3; c++) pos.push(lerp(m.pos[a * 3 + c], m.pos[b * 3 + c], t));
    mixW(m, a, b, t, bi, bw);
    slot.push(m.slot[a]);
    if (uv) uv.push(lerp(m.uv[a * 2], m.uv[b * 2], t), lerp(m.uv[a * 2 + 1], m.uv[b * 2 + 1], t));
    cut.set(key, j);
    return j;
  };
  for (let t = 0; t < m.idx.length; t += 3) {
    const v = [m.idx[t], m.idx[t + 1], m.idx[t + 2]],
      inn = v.map((i) => f[i] >= 0),
      c = inn[0] + inn[1] + inn[2];
    if (!c) continue;
    if (c === 3) {
      idx.push(keep(v[0]), keep(v[1]), keep(v[2]));
      continue;
    }
    const poly = [];
    for (let e = 0; e < 3; e++) {
      const a = v[e],
        b = v[(e + 1) % 3];
      if (inn[e]) poly.push(keep(a));
      if (inn[e] !== inn[(e + 1) % 3]) poly.push(split(a, b));
    }
    for (let k = 1; k + 1 < poly.length; k++) idx.push(poly[0], poly[k], poly[k + 1]);
  }
  const o = {
    n,
    pos: Float32Array.from(pos),
    nor: new Float32Array(n * 3),
    bi: Uint8Array.from(bi),
    bw: Float32Array.from(bw),
    slot: Uint8Array.from(slot),
    uv: uv ? Float32Array.from(uv) : null,
    idx: Uint32Array.from(idx),
  };
  return normals(o);
}
function edges(m) {
  // boundary edges (directed as in their triangle) and vertex neighbours
  const E = new Map(),
    nb = Array.from({ length: m.n }, () => []);
  for (let t = 0; t < m.idx.length; t += 3)
    for (let e = 0; e < 3; e++) {
      const a = m.idx[t + e],
        b = m.idx[t + ((e + 1) % 3)];
      E.set(a * 1e6 + b, 1);
      nb[a].push(b);
      nb[b].push(a);
    }
  const bd = [];
  for (const k of E.keys()) {
    const a = Math.floor(k / 1e6),
      b = k - a * 1e6;
    if (!E.has(b * 1e6 + a)) bd.push([a, b]);
  }
  return { bd, nb };
}
export function smooth(m, iters, lam = 0.5, pinBoundary = 0.7) {
  const { bd, nb } = edges(m),
    pin = new Float32Array(m.n);
  for (const [a, b] of bd) {
    pin[a] = pinBoundary;
    pin[b] = pinBoundary;
  }
  const p = m.pos,
    q = new Float32Array(p.length);
  for (let it = 0; it < iters; it++) {
    for (let i = 0; i < m.n; i++) {
      const N = nb[i];
      if (!N.length) {
        q[i * 3] = p[i * 3];
        q[i * 3 + 1] = p[i * 3 + 1];
        q[i * 3 + 2] = p[i * 3 + 2];
        continue;
      }
      let x = 0,
        y = 0,
        z = 0;
      for (const j of N) {
        x += p[j * 3];
        y += p[j * 3 + 1];
        z += p[j * 3 + 2];
      }
      const k = (lam * (1 - pin[i])) / N.length,
        w = 1 - lam * (1 - pin[i]);
      q[i * 3] = p[i * 3] * w + x * k;
      q[i * 3 + 1] = p[i * 3 + 1] * w + y * k;
      q[i * 3 + 2] = p[i * 3 + 2] * w + z * k;
    }
    p.set(q);
  }
  return normals(m);
}
export function inflate(m, d) {
  for (let i = 0; i < m.n; i++) {
    const k = typeof d === 'function' ? d(m.pos[i * 3], m.pos[i * 3 + 1], m.pos[i * 3 + 2], i) : d;
    m.pos[i * 3] += m.nor[i * 3] * k;
    m.pos[i * 3 + 1] += m.nor[i * 3 + 1] * k;
    m.pos[i * 3 + 2] += m.nor[i * 3 + 2] * k;
  }
  return m;
}
function grow(m, extraV, extraT) {
  const o = mk(m.n + extraV, 0);
  o.pos.set(m.pos);
  o.nor.set(m.nor);
  o.bi.set(m.bi);
  o.bw.set(m.bw);
  o.slot.set(m.slot);
  o.idx = new Uint32Array(m.idx.length + extraT * 3);
  o.idx.set(m.idx);
  return o;
}
// run a strip off chosen boundary edges: steps are functions (x,y,z,nx,ny,nz) -> [x,y,z]; gives hems their thickness and makes collars
export function strip(m, pick, steps, slot) {
  const { bd } = edges(m),
    sel = bd.filter(([a, b]) => pick(a) && pick(b));
  if (!sel.length) return m;
  const vs = [...new Set(sel.flat())],
    at = new Map(),
    S = steps.length,
    o = grow(m, vs.length * S, sel.length * 2 * S);
  vs.forEach((v, i) => at.set(v, m.n + i * S));
  for (const v of vs)
    for (let s = 0; s < S; s++) {
      const j = at.get(v) + s,
        p = steps[s](
          m.pos[v * 3],
          m.pos[v * 3 + 1],
          m.pos[v * 3 + 2],
          m.nor[v * 3],
          m.nor[v * 3 + 1],
          m.nor[v * 3 + 2],
        );
      o.pos.set(p, j * 3);
      o.bi.set(m.bi.subarray(v * 4, v * 4 + 4), j * 4);
      o.bw.set(m.bw.subarray(v * 4, v * 4 + 4), j * 4);
      o.slot[j] = slot === undefined ? m.slot[v] : slot;
    }
  let w = m.idx.length;
  for (const [a, b] of sel)
    for (let s = 0; s < S; s++) {
      const a0 = s ? at.get(a) + s - 1 : a,
        b0 = s ? at.get(b) + s - 1 : b,
        a1 = at.get(a) + s,
        b1 = at.get(b) + s;
      o.idx.set([b0, a0, a1, b0, a1, b1], w);
      w += 6;
    }
  return normals(o);
}
export function merge(list) {
  const L = list.filter(Boolean),
    n = L.reduce((a, m) => a + m.n, 0),
    o = mk(n, 0),
    id = [];
  let at = 0;
  for (const m of L) {
    o.pos.set(m.pos, at * 3);
    o.nor.set(m.nor, at * 3);
    o.bi.set(m.bi, at * 4);
    o.bw.set(m.bw, at * 4);
    o.slot.set(m.slot, at);
    for (let i = 0; i < m.idx.length; i++) id.push(m.idx[i] + at);
    at += m.n;
  }
  o.idx = Uint32Array.from(id);
  return o;
}
export function subdivide(m) {
  const mid = new Map(),
    pos = Array.from(m.pos),
    bi = Array.from(m.bi),
    bw = Array.from(m.bw),
    slot = Array.from(m.slot),
    idx = [];
  let n = m.n;
  const M = (a, b) => {
    const key = a < b ? a * 1e6 + b : b * 1e6 + a;
    let j = mid.get(key);
    if (j === undefined) {
      j = n++;
      for (let c = 0; c < 3; c++) pos.push((m.pos[a * 3 + c] + m.pos[b * 3 + c]) / 2);
      mixW(m, a, b, 0.5, bi, bw);
      slot.push(m.slot[a]);
      mid.set(key, j);
    }
    return j;
  };
  for (let t = 0; t < m.idx.length; t += 3) {
    const a = m.idx[t],
      b = m.idx[t + 1],
      c = m.idx[t + 2],
      ab = M(a, b),
      bc = M(b, c),
      ca = M(c, a);
    idx.push(a, ab, ca, ab, b, bc, ca, bc, c, ab, bc, ca);
  }
  return normals({
    n,
    pos: Float32Array.from(pos),
    nor: new Float32Array(n * 3),
    bi: Uint8Array.from(bi),
    bw: Float32Array.from(bw),
    slot: Uint8Array.from(slot),
    uv: null,
    idx: Uint32Array.from(idx),
  });
}
const hash3 = (x, y, z) => {
  const s = Math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453;
  return s - Math.floor(s);
};
function noise3(x, y, z) {
  const xi = Math.floor(x),
    yi = Math.floor(y),
    zi = Math.floor(z),
    u = x - xi,
    v = y - yi,
    w = z - zi,
    s = (t) => t * t * (3 - 2 * t),
    a = s(u),
    b = s(v),
    c = s(w);
  let r = 0;
  for (let k = 0; k < 8; k++) {
    const dx = k & 1,
      dy = (k >> 1) & 1,
      dz = (k >> 2) & 1;
    r += hash3(xi + dx, yi + dy, zi + dz) * (dx ? a : 1 - a) * (dy ? b : 1 - b) * (dz ? c : 1 - c);
  }
  return r * 2 - 1;
}
// simple solids, each bound to one bone
function solid(verts, tris, bone, slot) {
  const m = mk(verts.length / 3, tris.length / 3);
  m.pos.set(verts);
  m.idx.set(tris);
  for (let i = 0; i < m.n; i++) {
    m.bi[i * 4] = bone;
    m.bw[i * 4] = 1;
    m.slot[i] = slot;
  }
  return normals(m);
}
export function box(cx, cy, cz, w, h, d, bone, slot, ry = 0) {
  const v = [],
    t = [],
    c = Math.cos(ry),
    s = Math.sin(ry);
  const F = [
      [0, 1, 2, 1, 1],
      [0, 1, 2, -1, -1],
      [1, 2, 0, 1, 1],
      [1, 2, 0, -1, -1],
      [2, 0, 1, 1, 1],
      [2, 0, 1, -1, -1],
    ],
    hs = [w / 2, h / 2, d / 2];
  for (const [ax, u, w2, sg] of F) {
    const b = v.length / 3;
    for (const [du, dv] of [
      [-1, -1],
      [1, -1],
      [1, 1],
      [-1, 1],
    ]) {
      const p = [0, 0, 0];
      p[ax] = sg * hs[ax];
      p[u] = du * hs[u];
      p[w2] = dv * hs[w2];
      v.push(cx + p[0] * c + p[2] * s, cy + p[1], cz - p[0] * s + p[2] * c);
    }
    if (sg > 0) t.push(b, b + 1, b + 2, b, b + 2, b + 3);
    else t.push(b, b + 2, b + 1, b, b + 3, b + 2);
  }
  return solid(v, t, bone, slot);
}
export function ball(cx, cy, cz, r, bone, slot, sy = 1, seg = 8) {
  const v = [],
    t = [];
  for (let i = 0; i <= seg; i++)
    for (let j = 0; j < seg * 2; j++) {
      const a = (i / seg) * Math.PI,
        b = (j / (seg * 2)) * Math.PI * 2;
      v.push(
        cx + r * Math.sin(a) * Math.cos(b),
        cy + r * sy * Math.cos(a),
        cz + r * Math.sin(a) * Math.sin(b),
      );
    }
  for (let i = 0; i < seg; i++)
    for (let j = 0; j < seg * 2; j++) {
      const a = i * seg * 2 + j,
        b = i * seg * 2 + ((j + 1) % (seg * 2)),
        c = a + seg * 2,
        d = b + seg * 2;
      t.push(a, b, c, b, d, c);
    }
  return solid(v, t, bone, slot);
}
function ringLoft(rings, bone, slot, closed = true) {
  // rings: arrays of [x,y,z], same length
  const R = rings.length,
    K = rings[0].length,
    v = [],
    t = [];
  for (const r of rings) for (const p of r) v.push(p[0], p[1], p[2]);
  for (let i = 0; i + 1 < R; i++)
    for (let j = 0; j < (closed ? K : K - 1); j++) {
      const a = i * K + j,
        b = i * K + ((j + 1) % K),
        c = a + K,
        d = b + K;
      t.push(a, c, b, b, c, d);
    }
  return solid(v, t, bone, slot);
}

// recolour the part of a mesh where g >= 0, cutting along g = 0 so the edge is a clean line
export function paint(m, g, slot, only) {
  const f = new Float32Array(m.n),
    h = new Float32Array(m.n);
  for (let i = 0; i < m.n; i++) {
    f[i] = g(m.pos[i * 3], m.pos[i * 3 + 1], m.pos[i * 3 + 2], i);
    h[i] = -f[i] - 1e-6;
  }
  const a = clip(m, f),
    b = clip(m, h);
  for (let i = 0; i < a.n; i++) if (a.slot[i] === only) a.slot[i] = slot;
  return normals(merge([a, b]));
}
// ---------- the body, measured ----------
export function measure(body, joints) {
  // joints: world rest positions [x,y,z] by bone index
  const J = (k) => joints[BN[k]],
    L = {
      neck: J('neck')[1],
      headY: J('head')[1],
      headZ: J('head')[2],
      shoulder: J('uarmL')[1],
      shoulderX: J('uarmL')[0],
      elbowX: J('larmL')[0],
      wristX: J('handL')[0],
      hip: J('thighL')[1],
      hipX: J('thighL')[0],
      knee: J('calfL')[1],
      ankle: J('footL')[1],
      chest: J('sp3')[1],
      waist: J('sp1')[1] + 0.03,
      legZ: [J('thighL')[2], J('calfL')[2], J('footL')[2]],
      legX: [J('thighL')[0], J('calfL')[0], J('footL')[0]],
    };
  let cr = 9,
    top = 0;
  for (let i = 0; i < body.n; i++) {
    const x = body.pos[i * 3],
      y = body.pos[i * 3 + 1];
    if (Math.abs(x) < 0.015 && y > L.knee && y < L.hip + 0.05 && y < cr) cr = y;
    if (y > top) top = y;
  }
  L.crotch = cr;
  L.top = top;
  return L;
}

// ---------- garments ----------
const TOPS = {
  //            d: lift off the skin, sm: smoothing passes, hem: where the shell ends, tube: hem of a draped skirt below it (fraction of hip height, 0 none)
  blouse: { d: 0.013, sm: 3, hem: 'hip', collar: 'fold', v: 0.07 },
  jumper: { d: 0.019, sm: 5, hem: 'hip', collar: 'shirt', v: 0.12 },
  cardigan: { d: 0.021, sm: 5, hem: 'seat', collar: 'shirt', v: 0.24 },
  denim: { d: 0.02, sm: 3, hem: 'waist', collar: 'fold', v: 0.1 },
  leather: { d: 0.024, sm: 4, hem: 'hip', collar: 'fold', v: 0.12 },
  bomber: { d: 0.036, sm: 7, hem: 'waist', collar: 'roll', v: 0 },
  shell: { d: 0.034, sm: 7, hem: 'hip', collar: 'roll', v: 0, pat: 'shell' },
  anorak: { d: 0.034, sm: 6, hem: 'seat', tube: 0.86, collar: 'hood', v: 0 },
  donkey: { d: 0.03, sm: 5, hem: 'seat', tube: 0.8, collar: 'big', v: 0.06, pat: 'yoke' },
  carcoat: { d: 0.028, sm: 5, hem: 'seat', tube: 0.66, collar: 'big', v: 0.1 },
  runner: { d: 0.03, sm: 5, hem: 'seat', tube: 0.5, collar: 'big', v: 0.05 },
  overcoat: { d: 0.03, sm: 5, hem: 'seat', tube: 0.5, collar: 'big', v: 0.13 },
  mac: { d: 0.027, sm: 5, hem: 'seat', tube: 0.5, collar: 'big', v: 0.12 },
  duffel: { d: 0.034, sm: 6, hem: 'seat', tube: 0.6, collar: 'hood', v: 0 },
  cassock: { d: 0.024, sm: 5, hem: 'seat', tube: 0.1, collar: 'stand', v: 0 },
  overall: { d: 0.02, sm: 4, hem: 'hip', collar: 'fold', v: 0.08 },
  apron: { d: 0.015, sm: 3, hem: 'hip', collar: 'fold', v: 0.06, pat: 'apron' },
  tunic: { d: 0.024, sm: 4, hem: 'seat', tube: 0.86, collar: 'fold', v: 0.09, pat: 'tunic' },
};
const BOTS = {
  trousers: { d: 0.012, sm: 4, leg: 0.086, cuff: 0.092 },
  jeans: { d: 0.009, sm: 3, leg: 0.074, cuff: 0.078 },
  trackies: { d: 0.02, sm: 6, leg: 0.09, cuff: 0.062 },
  skirt: { skirt: 0.5 },
};
export const topKinds = Object.keys(TOPS),
  botKinds = Object.keys(BOTS);
const isArm = (m, i) => {
  let w = 0;
  for (let k = 0; k < 4; k++) {
    const b = m.bi[i * 4 + k];
    if ((b >= 8 && b <= 10) || (b >= 12 && b <= 14)) w += m.bw[i * 4 + k];
  }
  return w;
};
const isHead = (m, i) => {
  let w = 0;
  for (let k = 0; k < 4; k++) {
    const b = m.bi[i * 4 + k];
    if (b === 5 || b === 6) w += m.bw[i * 4 + k];
  }
  return w;
};

export function tailor(body, joints, sex) {
  const L = measure(body, joints),
    wb = weld(body),
    fem = sex === 'F',
    cache = {};
  const hemY = (h) => (h === 'waist' ? L.hip + 0.075 : h === 'hip' ? L.crotch + 0.085 : L.crotch + 0.05);
  const collarY = (z, lift) => L.neck + lift - (z - L.headZ) * 0.42;
  // a draped tube from the body's outline: support radii of the legs and hips at each height, eased outward
  function drape(yTop, yBot, off0, off1, slot, o = {}) {
    const K = 26,
      R = Math.max(4, Math.round((yTop - yBot) / 0.055)),
      zc = (L.legZ[0] + L.legZ[1]) / 2 + 0.005,
      rad = [],
      band = 0.05;
    for (let r = 0; r <= R; r++) {
      const y = lerp(yTop, yBot, r / R),
        ys = Math.max(y, L.knee + 0.04),
        h = new Float32Array(K);
      for (let i = 0; i < body.n; i++) {
        const py = body.pos[i * 3 + 1];
        if (Math.abs(py - ys) > band || isArm(body, i) > 0.3) continue;
        const x = body.pos[i * 3],
          z = body.pos[i * 3 + 2] - zc;
        if (Math.abs(x) > 0.3) continue;
        for (let k = 0; k < K; k++) {
          const a = (k / K) * Math.PI * 2,
            s = x * Math.cos(a) + z * Math.sin(a);
          if (s > h[k]) h[k] = s;
        }
      }
      rad.push(h);
    }
    for (let pass = 0; pass < 2; pass++)
      for (let r = 0; r <= R; r++) {
        const h = rad[r],
          c = Float32Array.from(h);
        for (let k = 0; k < K; k++) h[k] = (c[(k + K - 1) % K] + c[k] * 2 + c[(k + 1) % K]) / 4;
      }
    const rings = [];
    for (let r = 0; r <= R; r++) {
      const t = r / R,
        y = lerp(yTop, yBot, t),
        ring = [];
      for (let k = 0; k < K; k++) {
        const a = (k / K) * Math.PI * 2;
        let h = rad[r][k];
        if (r && !o.fitted) h = Math.max(h, rad[r - 1][k] * 0.985);
        rad[r][k] = h;
        const rr = h + lerp(off0, off1, t) + (o.flare || 0) * t * t;
        ring.push([Math.cos(a) * rr, y, zc + Math.sin(a) * rr * (1 + (o.deep || 0) * t)]);
      }
      rings.push(ring);
    }
    const m = ringLoft(rings, BN.pelvis, slot);
    for (let i = 0; i < m.n; i++) {
      const x = m.pos[i * 3],
        y = m.pos[i * 3 + 1],
        t = clamp((L.crotch + 0.06 - y) / 0.42, 0, 0.8),
        s = clamp(x / 0.06, -1, 1);
      m.bi.set([BN.pelvis, BN.thighL, BN.thighR, 0], i * 4);
      m.bw.set([1 - t, t * (0.5 + 0.5 * s), t * (0.5 - 0.5 * s), 0], i * 4);
    }
    return strip(m, () => true, [
      (x, y, z, nx, ny, nz) => [x - nx * 0.012, y + (y < (yTop + yBot) / 2 ? 0.004 : -0.004), z - nz * 0.012],
    ]);
  }
  function top(kind) {
    const T = TOPS[kind] || TOPS.jumper,
      hy = hemY(T.hem),
      f = new Float32Array(wb.n),
      lift = T.collar === 'stand' || T.collar === 'roll' ? 0.045 : 0.03;
    for (let i = 0; i < wb.n; i++) {
      const x = wb.pos[i * 3],
        y = wb.pos[i * 3 + 1],
        z = wb.pos[i * 3 + 2];
      f[i] = Math.min(L.wristX - 0.012 - Math.abs(x), collarY(z, lift) - y, y - hy);
    }
    let m = clip(wb, f);
    smooth(m, T.sm, 0.5, 0.6);
    const flareHem = T.tube ? 0.02 : 0.006;
    inflate(
      m,
      (x, y) =>
        T.d +
        sstep(hy + 0.16, hy, y) * flareHem +
        (Math.abs(x) > L.elbowX ? 0.004 : 0) +
        (fem ? 0 : sstep(L.chest, L.waist, y) * 0.008),
    );
    smooth(m, 1, 0.4, 0.3);
    for (let i = 0; i < m.n; i++) m.slot[i] = SLOT.top;
    const vb = L.neck + 0.02 - T.v,
      pat = T.pat,
      zf = L.headZ + 0.025;
    if (fem)
      for (let i = 0; i < m.n; i++) {
        const y = m.pos[i * 3 + 1],
          z = m.pos[i * 3 + 2],
          k =
            sstep(L.waist + 0.03, L.waist + 0.15, y) *
            sstep(L.shoulder - 0.01, L.shoulder - 0.1, y) *
            (Math.abs(m.pos[i * 3]) < L.shoulderX ? 1 : 0);
        if (z > zf && k > 0) m.pos[i * 3 + 2] = zf + (z - zf) * (1 - 0.6 * k);
      }
    if (fem) smooth(m, 2, 0.5, 0.6);
    const neckLoop = (i) => m.pos[i * 3 + 1] > L.shoulder + 0.0 && Math.abs(m.pos[i * 3]) < 0.16,
      out = (x, z, k) => {
        const dz = z - L.headZ,
          l = Math.hypot(x, dz) || 1;
        return [x + (x / l) * k, z + (dz / l) * k];
      };
    const st = (o1, u1) => (x, y, z) => {
      const [a, b] = out(x, z, o1);
      return [a, y + u1, b];
    };
    const cs = {
      fold: [st(0.012, 0.024), st(0.036, -0.004)],
      shirt: [st(0.008, 0.028), st(0.026, 0.004)],
      big: [st(0.02, 0.04), st(0.055, 0.0)],
      stand: [st(0.002, 0.03)],
      roll: [st(0.016, 0.012), st(0.016, 0.034), st(0.0, 0.04)],
      hood: [st(0.03, 0.02), st(0.05, 0.06), st(0.02, 0.09), st(-0.005, 0.07)],
    }[T.collar];
    const cslot =
      T.collar === 'shirt' || T.collar === 'stand' || pat === 'yoke' || kind === 'carcoat'
        ? SLOT.top2
        : pat === 'apron'
          ? SLOT.top2
          : SLOT.top;
    const cuffs = (i) => !neckLoop(i);
    m = strip(m, cuffs, [
      (x, y, z, nx, ny, nz) => [x - nx * T.d * 0.9, y - ny * T.d * 0.9, z - nz * T.d * 0.9],
    ]);
    if (cs) m = strip(m, neckLoop, cs, cslot);
    if (T.v)
      m = paint(
        m,
        (x, y, z) => Math.min((y - vb) * 0.6 - Math.abs(x), 0.09 - Math.abs(x), (z - zf) * 3),
        SLOT.top2,
        SLOT.top,
      );
    if (pat === 'yoke')
      m = paint(
        m,
        (x, y) => Math.min(y - (L.shoulder - 0.085 - Math.abs(x) * 0.1), L.shoulderX + 0.1 - Math.abs(x)),
        SLOT.top2,
        SLOT.top,
      );
    if (pat === 'shell') {
      m = paint(
        m,
        (x, y) =>
          Math.min(
            0.036 - Math.abs(y - (L.chest + 0.03 - Math.abs(x) * 0.5)),
            L.shoulderX + 0.03 - Math.abs(x),
          ),
        SLOT.top2,
        SLOT.top,
      );
      m = paint(
        m,
        (x) => Math.min(Math.abs(x) - (L.elbowX - 0.05), L.elbowX + 0.03 - Math.abs(x)),
        SLOT.top2,
        SLOT.top,
      );
    }
    if (pat === 'apron') for (let i = 0; i < m.n; i++) m.slot[i] = SLOT.top2;
    const parts = [m];
    let tubeBot = null;
    if (T.tube) {
      tubeBot = L.hip * T.tube;
      parts.push(
        drape(hy + 0.035, tubeBot, T.d * 0.82, T.d + 0.012, SLOT.top, {
          flare: kind === 'cassock' ? 0.05 : 0.02,
        }),
      );
    }
    if (pat === 'apron') {
      const yb = L.hip * 0.62,
        rings = [];
      for (let r = 0; r <= 6; r++) {
        const y = lerp(L.chest + 0.02, yb, r / 6),
          ring = [],
          wd = y > L.waist ? 0.115 : 0.17;
        for (let k = 0; k <= 8; k++) {
          const a = (k / 8 - 0.5) * 1.5;
          ring.push([
            Math.sin(a) * wd * 1.25,
            y,
            L.legZ[0] +
              0.02 +
              Math.cos(a) * (y > L.waist ? 0.105 : 0.135) +
              (fem && y > L.waist + 0.12 ? 0.03 : 0),
          ]);
        }
        rings.push(ring);
      }
      const ap = ringLoft(rings, BN.sp2, SLOT.top, false);
      for (let i = 0; i < ap.n; i++) {
        const y = ap.pos[i * 3 + 1],
          x = ap.pos[i * 3],
          t = clamp((L.crotch + 0.06 - y) / 0.4, 0, 0.7),
          up = sstep(L.hip, L.waist + 0.1, y),
          s = clamp(x / 0.06, -1, 1);
        ap.bi.set([BN.pelvis, BN.sp2, BN.thighL, BN.thighR], i * 4);
        ap.bw.set([(1 - t) * (1 - up), (1 - t) * up, t * (0.5 + 0.5 * s), t * (0.5 - 0.5 * s)], i * 4);
      }
      for (let t = 0; t < ap.idx.length; t += 3) {
        const b = ap.idx[t + 1];
        ap.idx[t + 1] = ap.idx[t + 2];
        ap.idx[t + 2] = b;
      }
      parts.push(normals(ap));
    }
    const g = merge(parts),
      hide = new Uint8Array(body.n);
    for (let i = 0; i < body.n; i++) {
      const x = body.pos[i * 3],
        y = body.pos[i * 3 + 1],
        z = body.pos[i * 3 + 2];
      const fi = Math.min(L.wristX - 0.012 - Math.abs(x), collarY(z, lift) - y, y - hy);
      if (fi > 0.014 && !(T.v && z > 0 && y > vb + 0.02 && Math.abs(x) < 0.03 && false)) hide[i] = 1;
      if (tubeBot !== null && y < hy + 0.03 && y > tubeBot + 0.05 && isArm(body, i) < 0.3) hide[i] = 1;
    }
    g.hide = hide;
    g.hem = tubeBot !== null ? tubeBot : hy;
    return g;
  }
  function bottom(kind) {
    const T = BOTS[kind] || BOTS.trousers,
      hide = new Uint8Array(body.n),
      wy = L.hip + 0.11;
    if (T.skirt) {
      const yb = L.hip * T.skirt,
        g = drape(wy, yb, 0.012, 0.03, SLOT.bot, { flare: 0.035 });
      for (let i = 0; i < body.n; i++) {
        const y = body.pos[i * 3 + 1];
        if (y < wy - 0.02 && y > yb + 0.05 && isArm(body, i) < 0.3) hide[i] = 1;
      }
      g.hide = hide;
      return g;
    }
    const cy = L.ankle - 0.012,
      f = new Float32Array(wb.n);
    for (let i = 0; i < wb.n; i++) {
      const y = wb.pos[i * 3 + 1];
      f[i] = Math.min(wy - y, y - cy);
    }
    let m = clip(wb, f);
    smooth(m, T.sm, 0.5, 0.5);
    inflate(m, T.d);
    for (let i = 0; i < m.n; i++) {
      // straight legs: no cloth clings to a calf
      const x = m.pos[i * 3],
        y = m.pos[i * 3 + 1],
        z = m.pos[i * 3 + 2];
      m.slot[i] = SLOT.bot;
      if (y > L.crotch - 0.03) continue;
      const sx = x > 0 ? 1 : -1,
        t = clamp((L.hip - y) / (L.hip - L.ankle), 0, 1),
        k = t < 0.5 ? 0 : 1,
        u = t < 0.5 ? t * 2 : (t - 0.5) * 2,
        ax = sx * lerp(L.legX[k], L.legX[k + 1], u),
        az = lerp(L.legZ[k], L.legZ[k + 1], u),
        dx = x - ax,
        dz = z - az,
        r = Math.hypot(dx, dz) || 1e-4;
      const want =
        lerp(T.leg, T.cuff, sstep(L.knee, L.ankle, y)) *
        (fem ? 0.93 : 1) *
        sstep(L.crotch - 0.03, L.crotch - 0.2, y);
      if (r < want) {
        const s = lerp(1, want / r, 0.85);
        m.pos[i * 3] = ax + dx * s;
        m.pos[i * 3 + 2] = az + dz * s;
      }
    }
    smooth(m, 1, 0.4, 0.3);
    m = strip(m, () => true, [
      (x, y, z, nx, ny, nz) => [x - nx * T.d * 0.9, y - ny * T.d * 0.9, z - nz * T.d * 0.9],
    ]);
    for (let i = 0; i < body.n; i++) {
      const y = body.pos[i * 3 + 1];
      if (Math.min(wy - y, y - cy) > 0.014) hide[i] = 1;
    }
    m.hide = hide;
    return m;
  }
  function shoes(kind) {
    // the foot, rounded off into a shoe with a sole
    const ty = L.ankle + (kind === 'boot' ? 0.07 : 0.02),
      f = new Float32Array(wb.n);
    for (let i = 0; i < wb.n; i++) f[i] = ty - wb.pos[i * 3 + 1];
    let m = clip(wb, f);
    smooth(m, 6, 0.6, 0.3);
    inflate(m, 0.014);
    for (let i = 0; i < m.n; i++) {
      m.slot[i] = SLOT.shoe;
      if (m.pos[i * 3 + 1] < 0.022) m.pos[i * 3 + 1] = Math.max(-0.004, m.pos[i * 3 + 1] * 0.3);
      if (m.pos[i * 3 + 2] > L.legZ[2] + 0.1) m.pos[i * 3 + 2] += 0.008;
    }
    normals(m);
    const hide = new Uint8Array(body.n);
    for (let i = 0; i < body.n; i++) if (ty - body.pos[i * 3 + 1] > 0.006) hide[i] = 1;
    m.hide = hide;
    return m;
  }
  const get = (k, fn) => cache[k] || (cache[k] = fn());
  return {
    L,
    wb,
    top: (k) => get('t' + k, () => top(k)),
    bottom: (k) => get('b' + k, () => bottom(k)),
    shoes: (k) => get('s' + k, () => shoes(k)),
  };
}

// ---------- heads: hair, hats and small things ----------
// hair: the pack's hair meshes by name; face: {eyeX, eyeY, eyeZ}; dy lifts a mesh made for the other body onto this head
export function headwear(kind, hair, L, face, sex, hideOut) {
  const fem = sex === 'F',
    own = fem ? hair.buzzf : hair.buzz,
    toHead = (m, s) => {
      const o = weld(m, s);
      return o;
    };
  const { eyeY, eyeZ } = face,
    top = L.top,
    hz = L.headZ,
    capLine = (z) => eyeY + 0.052 - (z - hz) * 0.12;
  const cap = (d, line, slot, lam = 0) => {
    let m = toHead(own, slot);
    const f = new Float32Array(m.n);
    for (let i = 0; i < m.n; i++) f[i] = m.pos[i * 3 + 1] - line(m.pos[i * 3 + 2]);
    m = clip(m, f);
    if (lam) smooth(m, lam, 0.5, 0.5);
    inflate(m, d);
    return strip(m, () => true, [(x, y, z, nx, ny, nz) => [x - nx * d, y - 0.004, z - nz * d]]);
  };
  const curls = (d, amp, freq, slot) => {
    let m = subdivide(toHead(own, slot));
    inflate(
      m,
      (x, y, z) =>
        d * sstep(eyeY - 0.03, eyeY + 0.05, y) +
        0.004 +
        amp * (0.5 + 0.5 * noise3(x * freq, y * freq, z * freq)) * sstep(eyeY - 0.02, eyeY + 0.04, y),
    );
    return normals(m);
  };
  switch (kind) {
    case 'bald':
      return null;
    case 'short':
      return fem ? inflate(toHead(hair.buzzf, SLOT.hair), 0.011) : toHead(hair.parted, SLOT.hair);
    case 'quiff': {
      const m = toHead(hair.parted, SLOT.hair);
      for (let i = 0; i < m.n; i++) {
        const z = m.pos[i * 3 + 2] - hz,
          y = m.pos[i * 3 + 1];
        const k = sstep(0.02, 0.09, z) * sstep(top - 0.09, top - 0.02, y);
        m.pos[i * 3 + 1] += k * 0.035;
        m.pos[i * 3 + 2] += k * 0.014;
      }
      return normals(m);
    }
    case 'balding': {
      let m = toHead(own, SLOT.hair);
      const f = new Float32Array(m.n);
      for (let i = 0; i < m.n; i++) f[i] = top - 0.062 + (m.pos[i * 3 + 2] - hz) * -0.22 - m.pos[i * 3 + 1];
      m = clip(m, f);
      return inflate(m, 0.004);
    }
    case 'mullet': {
      const a = toHead(hair.parted, SLOT.hair);
      let b = toHead(hair.long, SLOT.hair);
      const f = new Float32Array(b.n);
      for (let i = 0; i < b.n; i++)
        f[i] = Math.min(-(b.pos[i * 3 + 2] - hz) - 0.035, b.pos[i * 3 + 1] - (L.neck - 0.02));
      b = clip(b, f);
      return merge([a, b]);
    }
    case 'perm':
      return curls(0.03, 0.03, 46, SLOT.hair);
    case 'set':
      return curls(0.018, 0.014, 60, SLOT.hair);
    case 'bob': {
      let m = toHead(hair.long, SLOT.hair);
      const f = new Float32Array(m.n);
      for (let i = 0; i < m.n; i++) f[i] = m.pos[i * 3 + 1] - (eyeY - 0.105);
      m = clip(m, f);
      return m;
    }
    case 'long':
      return toHead(hair.long, SLOT.hair);
    case 'bun':
      return toHead(hair.buns, SLOT.hair);
    case 'woolly': {
      const m = cap(0.017, (z) => eyeY + 0.03 - (z - hz) * 0.18, SLOT.hat, 2);
      return merge([m, ball(0, top + 0.03, hz - 0.01, 0.028, BN.head, SLOT.hat)]);
    }
    case 'flatcap': {
      const m = cap(0.013, capLine, SLOT.hat, 1),
        ty = top - 0.004;
      for (let i = 0; i < m.n; i++) {
        if (m.pos[i * 3 + 1] > ty) m.pos[i * 3 + 1] = ty + (m.pos[i * 3 + 1] - ty) * 0.25;
        if (m.pos[i * 3 + 2] > hz + 0.03) m.pos[i * 3 + 2] += 0.014;
      }
      const by = capLine(hz + 0.09) + 0.004,
        rings = [[], []];
      for (let k = 0; k <= 10; k++) {
        const a = (k / 10 - 0.5) * 2.5;
        rings[0].push([Math.sin(a) * 0.082, by + 0.004, hz + 0.02 + Math.cos(a) * 0.075]);
        rings[1].push([Math.sin(a) * 0.092, by - 0.012, hz + 0.03 + Math.cos(a) * 0.125]);
      }
      const brim = ringLoft(rings, BN.head, SLOT.hat, false),
        under = ringLoft(
          [rings[1].map((p) => [p[0], p[1] - 0.004, p[2]]), rings[0].map((p) => [p[0], p[1] - 0.006, p[2]])],
          BN.head,
          SLOT.dark,
          false,
        );
      let side = toHead(own, SLOT.hair);
      const f = new Float32Array(side.n);
      for (let i = 0; i < side.n; i++) f[i] = capLine(side.pos[i * 3 + 2]) + 0.012 - side.pos[i * 3 + 1];
      side = inflate(clip(side, f), 0.003);
      return merge([normals(m), brim, under, side]);
    }
    case 'headscarf':
    case 'rainhood': {
      // cut from the head itself: everything but the face, down to the jaw
      const b = hair._head,
        f = new Float32Array(b.n);
      for (let i = 0; i < b.n; i++) {
        const x = b.pos[i * 3],
          y = b.pos[i * 3 + 1],
          z = b.pos[i * 3 + 2] - hz;
        const face = Math.max(z - 0.052 - Math.max(0, y - (eyeY + 0.035)) * 1.4, eyeY - 0.118 - y + 0.0);
        f[i] = Math.min(-face, y - (eyeY - 0.125), isHead(b, i) - 0.45);
      }
      let m = clip(b, f);
      for (let i = 0; i < m.n; i++) m.slot[i] = SLOT.hat;
      smooth(m, 3, 0.5, 0.5);
      inflate(m, kind === 'rainhood' ? 0.02 : 0.016);
      m = strip(m, () => true, [(x, y, z, nx, ny, nz) => [x - nx * 0.014, y - ny * 0.014, z - nz * 0.014]]);
      return merge([m, box(0, eyeY - 0.135, hz + 0.075, 0.035, 0.03, 0.025, BN.head, SLOT.hat)]);
    }
    case 'helmet': {
      // a constable's helmet
      const prof = [
          [0.106, -0.012],
          [0.094, 0.0],
          [0.09, 0.03],
          [0.084, 0.075],
          [0.066, 0.118],
          [0.036, 0.146],
          [0.012, 0.156],
          [0.008, 0.172],
          [0.0, 0.176],
        ],
        base = eyeY + 0.05,
        rings = prof.map(([r, y]) => {
          const ring = [];
          for (let k = 0; k < 16; k++) {
            const a = (k / 16) * Math.PI * 2;
            ring.push([Math.cos(a) * r, base + y, hz + 0.004 + Math.sin(a) * r * 1.12]);
          }
          return ring;
        });
      const m = ringLoft(rings, BN.head, SLOT.hat);
      for (let t = 0; t < m.idx.length; t += 3) {
        const b = m.idx[t + 1];
        m.idx[t + 1] = m.idx[t + 2];
        m.idx[t + 2] = b;
      }
      return merge([normals(m), box(0, base + 0.065, hz + 0.1, 0.03, 0.036, 0.006, BN.head, SLOT.gold)]);
    }
    default:
      return fem ? toHead(hair.long, SLOT.hair) : toHead(hair.parted, SLOT.hair);
  }
}
export function extras(list, L, face, sex) {
  const { eyeX, eyeY, eyeZ } = face,
    hz = L.headZ,
    out = [];
  for (const x of list) {
    if (x === 'glasses') {
      for (const s of [-1, 1]) {
        const ring = [],
          ring2 = [];
        for (let k = 0; k < 12; k++) {
          const a = (k / 12) * Math.PI * 2;
          ring.push([s * eyeX + Math.cos(a) * 0.024, eyeY + Math.sin(a) * 0.019, eyeZ + 0.016]);
          ring2.push([s * eyeX + Math.cos(a) * 0.019, eyeY + Math.sin(a) * 0.014, eyeZ + 0.017]);
        }
        out.push(ringLoft([ring, ring2], BN.head, SLOT.dark), ringLoft([ring2, ring], BN.head, SLOT.dark));
        out.push(box(s * 0.073, eyeY + 0.004, eyeZ - 0.045, 0.004, 0.005, 0.12, BN.head, SLOT.dark));
      }
      out.push(box(0, eyeY + 0.004, eyeZ + 0.016, 0.022, 0.005, 0.004, BN.head, SLOT.dark));
    }
    if (x === 'tash') out.push(box(0, eyeY - 0.071, eyeZ + 0.012, 0.052, 0.012, 0.016, BN.head, SLOT.hair));
    if (x === 'earrings')
      for (const s of [-1, 1])
        out.push(ball(s * 0.074, eyeY - 0.055, hz + 0.012, 0.009, BN.head, SLOT.gold, 1, 4));
    if (x === 'pager')
      out.push(box(-0.13, L.hip + 0.085, L.legZ[0] + 0.115, 0.05, 0.07, 0.026, BN.pelvis, SLOT.dark));
    if (x === 'bag') {
      out.push(box(0.235, L.hip + 0.0, L.legZ[0] + 0.02, 0.09, 0.2, 0.27, BN.pelvis, SLOT.dark));
      for (let k = 0; k < 6; k++) {
        const t = k / 5,
          y = lerp(L.hip + 0.1, L.shoulder + 0.07, t),
          xx = lerp(0.215, -0.1, t * t);
        out.push(
          box(
            xx,
            y,
            L.legZ[0] + 0.115 * Math.sin(Math.PI * (0.25 + t * 0.3)),
            0.03,
            (L.shoulder - L.hip) / 5 + 0.03,
            0.012,
            t < 0.3 ? BN.pelvis : t < 0.6 ? BN.sp2 : BN.sp3,
            SLOT.dark,
            0,
          ),
        );
      }
    }
  }
  return out.length ? merge(out) : null;
}
// far figures: one vertex per small cell, so a few hundred triangles carry the same outline and colours
export function cluster(g, cell) {
  const map = new Map(),
    rm = new Uint32Array(g.n),
    src = [];
  for (let i = 0; i < g.n; i++) {
    const key =
      Math.floor(g.pos[i * 3] / cell) +
      ',' +
      Math.floor(g.pos[i * 3 + 1] / cell) +
      ',' +
      Math.floor(g.pos[i * 3 + 2] / cell) +
      ',' +
      g.slot[i];
    let j = map.get(key);
    if (j === undefined) {
      j = src.length;
      map.set(key, j);
      src.push(i);
    }
    rm[i] = j;
  }
  const id = [];
  for (let t = 0; t < g.idx.length; t += 3) {
    const a = rm[g.idx[t]],
      b = rm[g.idx[t + 1]],
      c = rm[g.idx[t + 2]];
    if (a !== b && b !== c && a !== c) id.push(a, b, c);
  }
  return { src, idx: Uint32Array.from(id) };
}
