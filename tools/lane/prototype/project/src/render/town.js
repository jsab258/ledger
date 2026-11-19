// The static town: ground, buildings with painted fascias, street furniture, the quay.
import {
  THREE,
  U,
  lit,
  mat,
  Batch,
  boxG,
  wallBox,
  planeXZ,
  xform,
  brickTex,
  slateTex,
  plainTex,
  windowTex,
  shopInsideTex,
  signTex,
  textTex,
  glowTex,
  blobTex,
  groundTex,
} from './core.js';
import { extraMaterials, buildExtras, aerial, hash2, numUV, posterUV } from './extras.js';
import { BOUNDS, ROADS, SETTS, PAVE, BLD, WALLS, PROPS, LAMPS, WINDOWS } from '../map.js';

export const town = {
  halos: [],
  blinkers: [],
  winLights: {},
  winSpots: [],
  winAt: {},
  fire: null,
  ferry: null,
  boats: [],
  signs: [],
};
let rs = 11;
const rr = () => {
  rs = (rs * 16807) % 2147483647;
  return rs / 2147483647;
};
const M = {};
const DOORS = ['#2f3a4a', '#4a2a22', '#243a2a', '#3a3a3a', '#5a4a2a', '#1f2a3a', '#4a3040'];

function materials() {
  const g = (k, o = {}, puddle = 1) =>
    lit(
      new THREE.MeshStandardMaterial(
        Object.assign({ ...groundTex(k), roughness: 0.82, metalness: 0, vertexColors: true }, o),
      ),
      { ground: true, puddle },
    );
  M.asphalt = g('asphalt');
  M.flags = g('flags', {}, 0.45);
  M.setts = g('setts', { roughness: 0.7 }, 0.75);
  M.concrete = lit(
    new THREE.MeshStandardMaterial({ map: plainTex('concrete'), roughness: 0.9, vertexColors: true }),
    { ground: true },
  );
  M.planks = lit(
    new THREE.MeshStandardMaterial({ map: plainTex('planks'), roughness: 0.8, vertexColors: true }),
    { ground: true },
  );
  for (const k of ['soot', 'red', 'yellow', 'stone']) M[k] = mat({ map: brickTex(k) });
  M.slate = mat({ map: slateTex() });
  M.iron = mat({ map: plainTex('iron') });
  M.flat = mat({});
  M.paint = mat({});
  M.mark = lit(
    new THREE.MeshLambertMaterial({
      vertexColors: true,
      polygonOffset: true,
      polygonOffsetFactor: -3,
      polygonOffsetUnits: -3,
      transparent: true,
      opacity: 0.82,
    }),
  );
  M.win = mat({ map: windowTex() });
  const wt = M.win.map;
  M.winGlow = new THREE.ShaderMaterial({
    uniforms: { map: { value: wt }, uWinLevel: U.uWinLevel },
    vertexShader:
      'attribute float aLit; varying float vL; varying vec2 vUv; void main(){ vL = aLit; vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader:
      'uniform sampler2D map; uniform float uWinLevel; varying float vL; varying vec2 vUv; void main(){ if (vL > uWinLevel) discard; vec3 c = texture2D(map, vUv).rgb; gl_FragColor = vec4(c * c * 2.1, 1.0); }',
    polygonOffset: true,
    polygonOffsetFactor: -2,
    polygonOffsetUnits: -2,
  });
  M.shop = new THREE.ShaderMaterial({
    uniforms: { map: { value: shopInsideTex() }, uShopLit: U.uShopLit, uNight: U.uNight },
    vertexShader:
      'attribute float aLit; attribute vec3 color; varying float vL; varying vec2 vUv; varying vec3 vC; void main(){ vL = aLit; vUv = uv; vC = color; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: `uniform sampler2D map; uniform vec3 uShopLit; uniform float uNight; varying float vL; varying vec2 vUv; varying vec3 vC;
      void main(){ float l = vL < 0.5 ? uShopLit.x : vL < 1.5 ? uShopLit.y : vL < 2.5 ? uShopLit.z : 0.0; vec3 inside = texture2D(map, vUv).rgb * vC; vec3 glass = mix(vec3(0.035,0.04,0.048), vec3(0.15,0.17,0.19), (1.0 - uNight) * (0.25 + 0.75 * vUv.y));
        if (vL > 2.5) glass = mix(glass, vC * 0.5, 0.75); gl_FragColor = vec4(glass * (1.0 - 0.7 * l) + inside * inside * l * 1.5, 1.0); }`,
  });
  M.lens = new THREE.MeshBasicMaterial({ color: new THREE.Color(5, 2.2, 0.5) });
  M.lensW = new THREE.MeshBasicMaterial({ color: new THREE.Color(3, 2.8, 2.2) });
  M.halo = new THREE.SpriteMaterial({
    map: glowTex(),
    color: new THREE.Color(1.0, 0.5, 0.14),
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    fog: false,
  });
  M.fireM = new THREE.MeshBasicMaterial({ color: new THREE.Color(4, 1.6, 0.3) });
  extraMaterials(M);
}
// ---------- facades ----------
function frame(b) {
  const f = b.face;
  if (f === 'W')
    return {
      ox: b.x0,
      oz: b.z0,
      ux: 0,
      uz: 1,
      nx: -1,
      nz: 0,
      W: b.z1 - b.z0,
      D: b.x1 - b.x0,
      ry: -Math.PI / 2,
    };
  if (f === 'E')
    return {
      ox: b.x1,
      oz: b.z1,
      ux: 0,
      uz: -1,
      nx: 1,
      nz: 0,
      W: b.z1 - b.z0,
      D: b.x1 - b.x0,
      ry: Math.PI / 2,
    };
  if (f === 'S')
    return { ox: b.x0, oz: b.z1, ux: 1, uz: 0, nx: 0, nz: 1, W: b.x1 - b.x0, D: b.z1 - b.z0, ry: 0 };
  return { ox: b.x1, oz: b.z0, ux: -1, uz: 0, nx: 0, nz: -1, W: b.x1 - b.x0, D: b.z1 - b.z0, ry: Math.PI };
}
const fp = (F, a, out) => [F.ox + F.ux * a + F.nx * out, F.oz + F.uz * a + F.nz * out];
function fquad(F, a0, a1, y0, y1, out, uv) {
  const g = new THREE.PlaneGeometry(a1 - a0, y1 - y0);
  if (uv) {
    const t = g.attributes.uv;
    for (let i = 0; i < 4; i++)
      t.setXY(i, uv[0] + t.getX(i) * (uv[2] - uv[0]), uv[1] + t.getY(i) * (uv[3] - uv[1]));
  }
  const [x, z] = fp(F, (a0 + a1) / 2, out);
  return xform(g, x, (y0 + y1) / 2, z, F.ry);
}
function fbox(F, a0, a1, y0, y1, out, depth) {
  const [x, z] = fp(F, (a0 + a1) / 2, out - depth / 2);
  return xform(new THREE.BoxGeometry(a1 - a0, y1 - y0, depth), x, (y0 + y1) / 2, z, F.ry);
}
function withLit(g, v) {
  const n = g.attributes.position.count;
  g.setAttribute('aLit', new THREE.BufferAttribute(new Float32Array(n).fill(v), 1));
  return g;
}
function win(bt, F, a, y, w, h, glow = true) {
  {
    const [wx, wz] = fp(F, a, 0.03);
    town.winSpots.push({ x: wx, z: wz, y: y + h / 2, w, h, nx: F.nx, nz: F.nz });
  }
  bt.add(M.win, fquad(F, a - w / 2, a + w / 2, y, y + h, 0.03, [0, 0, 0.25, 1]));
  bt.add(M.flat, fbox(F, a - w / 2 - 0.1, a + w / 2 + 0.1, y - 0.12, y, 0.1, 0.12), '#8d887a');
  bt.add(M.flat, fbox(F, a - w / 2 - 0.1, a + w / 2 + 0.1, y + h, y + h + 0.16, 0.06, 0.08), '#7d786c');
  if (M.streak && y > 0.5)
    bt.add(
      M.streak,
      fquad(F, a - w / 2 - 0.08, a + w / 2 + 0.08, y - 1.3, y - 0.12, 0.012, [
        hash2(a, y) * 0.5,
        0,
        hash2(a, y) * 0.5 + 0.5,
        1,
      ]),
    );
  if (glow) {
    const k = 1 + Math.floor(rr() * 3);
    bt.add(
      M.winGlow,
      withLit(
        fquad(F, a - w / 2, a + w / 2, y, y + h, 0.035, [k * 0.25, 0, k * 0.25 + 0.25, 1]),
        0.05 + rr() * 0.95,
      ),
    );
  }
}
function board(bt, F, a, y, w, h) {
  bt.add(M.wood || M.flat, fbox(F, a - w / 2, a + w / 2, y, y + h, 0.06, 0.06), '#a89c8c');
}
function gable(bt, b, y, rh, axis, roofMat = M.slate, endMat = M.soot, over = 0.25) {
  const x0 = b.x0 - (axis === 'z' ? over : 0),
    x1 = b.x1 + (axis === 'z' ? over : 0),
    z0 = b.z0 - (axis === 'x' ? over : 0),
    z1 = b.z1 + (axis === 'x' ? over : 0);
  const P =
    axis === 'z'
      ? {
          A: [x0, y, z0],
          B: [x1, y, z0],
          R0: [(x0 + x1) / 2, y + rh, z0],
          A2: [x0, y, z1],
          B2: [x1, y, z1],
          R1: [(x0 + x1) / 2, y + rh, z1],
        }
      : {
          A: [x0, y, z1],
          B: [x0, y, z0],
          R0: [x0, y + rh, (z0 + z1) / 2],
          A2: [x1, y, z1],
          B2: [x1, y, z0],
          R1: [x1, y + rh, (z0 + z1) / 2],
        };
  const quad = (a, b2, c, d, su, sv) => {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute([...a, ...b2, ...c, ...a, ...c, ...d], 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute([0, 0, su, 0, su, sv, 0, 0, su, sv, 0, sv], 2));
    g.computeVertexNormals();
    return g;
  };
  const L = axis === 'z' ? z1 - z0 : x1 - x0,
    sl = Math.hypot((axis === 'z' ? x1 - x0 : z1 - z0) / 2, rh);
  bt.add(roofMat, quad(P.A, P.A2, P.R1, P.R0, L / 1.8, sl / 1.8));
  bt.add(roofMat, quad(P.B2, P.B, P.R0, P.R1, L / 1.8, sl / 1.8));
  {
    const zr = axis === 'z',
      mx = (P.R0[0] + P.R1[0]) / 2,
      mz = (P.R0[2] + P.R1[2]) / 2;
    bt.add(M.flat, boxG(zr ? 0.3 : L, 0.14, zr ? L : 0.3, mx, y + rh + 0.05, mz), '#3d3833'); // ridge tiles
    for (const [e0, e1] of [
      [P.A, P.A2],
      [P.B, P.B2],
    ])
      bt.add(
        M.flat,
        boxG(zr ? 0.15 : L, 0.12, zr ? L : 0.15, (e0[0] + e1[0]) / 2, y - 0.02, (e0[2] + e1[2]) / 2),
        '#141414',
      );
  } // gutters
  const tri = (a, b2, c) => {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute([...a, ...b2, ...c], 3));
    const w = Math.hypot(a[0] - b2[0], a[2] - b2[2]);
    g.setAttribute('uv', new THREE.Float32BufferAttribute([0, 0, w / 2.4, 0, w / 4.8, rh / 2.4], 2));
    g.computeVertexNormals();
    return g;
  };
  bt.add(endMat, tri(P.B, P.A, P.R0), '#9a9a9a');
  bt.add(endMat, tri(P.A2, P.B2, P.R1), '#9a9a9a');
}
function chimney(bt, x, y, z, m) {
  bt.add(m, wallBox(0.75, 1.5, 1.0, x, y + 0.75, z), '#8a8a8a');
  bt.add(M.flat, boxG(0.95, 0.22, 1.2, x, y + 0.14, z), '#5f666c');
  bt.add(M.flat, boxG(0.85, 0.1, 1.1, x, y + 1.52, z), '#6a6660');
  if (hash2(x, z) < 0.6) aerial(bt, M, x, y, z);
  for (const o of [-0.25, 0.25])
    bt.add(M.flat, xform(new THREE.CylinderGeometry(0.11, 0.14, 0.45, 6), x, y + 1.7, z + o), '#5a3a2a');
}

function building(bt, b, root) {
  const F = frame(b),
    wm = M[b.brick] || M.soot,
    cx = (b.x0 + b.x1) / 2,
    cz = (b.z0 + b.z1) / 2,
    w = b.x1 - b.x0,
    d = b.z1 - b.z0,
    k = b.k;
  let H = b.st * 3.0 + 0.5;
  const axis = F.ux === 0 ? 'z' : 'x',
    W = F.W;
  const tone = b.burnt
    ? '#3a3632'
    : ['#ffffff', '#e6e2dc', '#f2ece6', '#d8d4d0', '#f4e6dc', '#cfc8c2', '#ece8f0', '#e0d6cc'][
        Math.floor(rr() * 8)
      ];
  if (k === 'yards') {
    bt.add(M.soot, wallBox(w, 2.5, d, cx, 1.25, cz), '#b8b4ae');
    bt.add(M.slate, planeXZ(b.x0, b.z0, b.x1, b.z1, 2.52, 1.8));
    for (let i = 0; i < Math.floor(Math.max(w, d) / 7); i++) {
      const t = (i + 0.5) / Math.floor(Math.max(w, d) / 7);
      bt.add(
        M.soot,
        wallBox(2.2, 1.0, 2.4, w > d ? b.x0 + t * w : cx + 1, 3.0, w > d ? cz : b.z0 + t * d),
        '#aaa',
      );
    }
    return;
  }
  if (k === 'cabin' || k === 'shed') {
    H = k === 'shed' ? 5 : 2.9;
    bt.add(M.iron, wallBox(w, H, d, cx, H / 2, cz), k === 'shed' ? '#9aa39a' : '#b0a890');
    bt.add(M.iron, wallBox(w + 0.5, 0.18, d + 0.5, cx, H + 0.09, cz), '#666');
    if (b.sign)
      signMesh(
        root,
        F,
        0.6,
        W - 0.6,
        H - 1.5,
        H - 0.35,
        0.05,
        signTex(b.sign, '', k === 'shed' ? '#d9d4c0' : '#e8e2cc', '#1a2f4a', 'slab', 1024, 128),
      );
    bt.add(
      M.flat,
      fbox(
        F,
        W / 2 - (k === 'shed' ? 3 : 0.5),
        W / 2 + (k === 'shed' ? 3 : 0.5),
        0.05,
        k === 'shed' ? 3.6 : 2.1,
        0.05,
        0.08,
      ),
      k === 'shed' ? '#2a3a30' : '#3a3530',
    );
    if (k === 'cabin') {
      bt.add(M.win, fquad(F, 0.7, 2.1, 1.0, 2.0, 0.03, [0, 0, 0.25, 1]));
      bt.add(M.winGlow, withLit(fquad(F, 0.7, 2.1, 1.0, 2.0, 0.035, [0.5, 0, 0.75, 1]), 0.02));
    }
    return;
  }
  if (k === 'garages') {
    bt.add(M.soot, wallBox(w, 2.7, d, cx, 1.35, cz), '#bbb');
    bt.add(M.flat, wallBox(w + 0.3, 0.15, d + 0.3, cx, 2.78, cz), '#3a3a3a');
    for (let a = 0.3; a < W - 2.6; a += 3.1)
      bt.add(
        M.iron,
        fbox(F, a, a + 2.6, 0.05, 2.2, 0.04, 0.06),
        ['#5a6a7a', '#7a5a4a', '#5a7a5a', '#888', '#6a6a50'][Math.floor(rr() * 5)],
      );
    return;
  }
  if (k === 'ware') H = 11.5;
  if (k === 'chapel') H = 7;
  if (k === 'school') H = 8.5;
  if (k === 'hall') H = 8;
  if (k === 'bank') H = 11;
  bt.add(wm, wallBox(w, H, d, cx, H / 2, cz), tone);
  bt.add(M.flat, wallBox(w + 0.06, 0.5, d + 0.06, cx, 0.25, cz), '#2a2623'); // grimy plinth
  if (M.streak && !b.burnt) {
    bt.add(M.streak, fquad(F, 0, W, 0.5, 1.7, 0.012, [0, 1, W / 5, 0]));
    bt.add(M.streak, fquad(F, 0, W, H - 1.5, H, 0.012, [0, 0, W / 6, 1]));
  } // damp at the foot, soot under the eaves
  if (!b.burnt) {
    if (k === 'chapel') gable(bt, b, H, 4.2, axis === 'z' ? 'x' : 'z', M.slate, wm, 0.2);
    else if (k === 'bank' || k === 'hall' || k === 'ware') {
      bt.add(M.flat, wallBox(w + 0.5, 0.5, d + 0.5, cx, H + 0.25, cz), '#57534a');
      if (k !== 'bank') gable(bt, b, H + 0.5, 2.6, axis, M.slate, wm, 0);
    } else gable(bt, b, H, Math.min(F.D, 12) * 0.3, axis, M.slate, wm);
  } else {
    for (let i = 0; i < 14; i++)
      bt.add(
        M.flat,
        xform(
          new THREE.BoxGeometry(0.25, 0.3, 4 + rr() * 9),
          b.x0 + rr() * w,
          H - 0.5 - rr() * 3.5,
          b.z0 + rr() * d,
          rr() * 3,
          (rr() - 0.5) * 0.9,
        ),
        '#0c0b0a',
      );
    bt.add(M.flat, wallBox(w - 1, 0.3, d - 1, cx, 1.6, cz), '#0e0d0c');
  }
  if (['house', 'shop', 'hotel', 'pub'].includes(k)) {
    const rh = Math.min(F.D, 12) * 0.3;
    const [c1x, c1z] = fp(F, 0.5, -F.D / 2),
      [c2x, c2z] = fp(F, W - 0.5, -F.D / 2);
    chimney(bt, c1x, H + rh - 0.4, c1z, wm);
    if (W > 9) chimney(bt, c2x, H + rh - 0.4, c2z, wm);
  }
  const upper = (y0, n, ww = 1.05, hh = 1.6, glow = true) => {
    for (let i = 0; i < n; i++) win(bt, F, (W * (i + 0.5)) / n, y0, ww, hh, glow);
  };
  if (k === 'house') {
    const flip = rr() < 0.5,
      da = flip ? W - 1.4 : 1.4,
      wa = flip ? 2.2 : W - 2.2,
      col = b.door || DOORS[Math.floor(rr() * DOORS.length)];
    bt.add(M.paint, fbox(F, da - 0.5, da + 0.5, 0.14, 2.2, 0.02, 0.1), col);
    bt.add(M.flat, fbox(F, da - 0.62, da + 0.62, 2.2, 2.38, 0.06, 0.1), '#8d887a');
    bt.add(M.flat, fbox(F, da - 0.6, da + 0.6, 0, 0.14, 0.3, 0.34), '#77736a');
    bt.add(M.flat, fbox(F, 0.04, 0.15, 0.2, H, 0.11, 0.1), '#151515');
    if (M.sheet)
      bt.add(
        M.sheet,
        fquad(F, da - 0.12, da + 0.12, 1.66, 1.9, 0.03, numUV(Math.floor(hash2(b.x0 + F.W, b.z0) * 32))),
        '#ffffff',
      ); // downpipe, door number
    win(bt, F, wa, 1.0, 1.25, 1.55);
    for (let s = 1; s < b.st; s++) upper(3.5 + (s - 1) * 3 + 0.5, Math.max(1, Math.round(W / 3.4)));
  } else if (k === 'shop' || k === 'pub') {
    const fb = b.fb || '#3a3530',
      code = b.tolet || b.shut ? 3 : b.id === 'rita' ? 2 : b.late ? 1 : 0;
    bt.add(M.paint, fbox(F, 0.1, W - 0.1, 0, 0.55, 0.08, 0.1), fb);
    bt.add(M.paint, fbox(F, 0.05, 0.4, 0, 3.5, 0.12, 0.14), fb);
    bt.add(M.paint, fbox(F, W - 0.4, W - 0.05, 0, 3.5, 0.12, 0.14), fb);
    bt.add(M.paint, fbox(F, 0.05, W - 0.05, 2.62, 3.5, 0.13, 0.15), fb);
    bt.add(M.paint, fbox(F, 0, W, 3.5, 3.62, 0.24, 0.26), '#2a2826');
    if (b.shut) {
      board(bt, F, W / 2 + 0.6, 0.6, W - 2.6, 1.95);
      board(bt, F, 0.95, 0.15, 1.0, 2.2);
    } else {
      const tint = b.tolet ? '#d8d6cc' : ['#ffffff', '#ffe6c0', '#e8f0ff', '#fff0d8'][Math.floor(rr() * 4)];
      const g = withLit(fquad(F, 1.75, W - 0.5, 0.6, 2.55, 0.04, [0, 0, (W - 2.25) / 6, 1]), code);
      bt.add(M.shop, g, tint);
      const dg = withLit(fquad(F, 0.6, 1.5, 1.0, 2.1, 0.05, [0.1, 0.3, 0.3, 0.9]), code);
      bt.add(M.shop, dg, tint);
      bt.add(M.paint, fbox(F, 0.5, 1.6, 0.1, 1.0, 0.03, 0.06), fb);
      bt.add(M.paint, fbox(F, 1.6, 1.72, 0.55, 2.62, 0.08, 0.08), fb);
    }
    if (b.sign)
      signMesh(
        root,
        F,
        0.45,
        W - 0.45,
        2.72,
        3.42,
        0.14,
        signTex(
          b.sign,
          b.sub,
          fb,
          b.ff || '#e8dfc4',
          b.font || 'serif',
          1024,
          Math.round((1024 * 0.7) / (W - 0.9)),
        ),
        b.id,
      );
    if (b.tolet && M.sheet)
      for (let i = 0; i < 3; i++)
        bt.add(
          M.sheet,
          fquad(
            F,
            2.2 + i * 1.7,
            3.15 + i * 1.7,
            0.72 + (i % 2) * 0.3,
            2.05 + (i % 2) * 0.3,
            0.05,
            posterUV(i + 1),
          ),
          '#ffffff',
        ); // fly-posters on the empty unit
    if (b.tolet) {
      const [x, z] = fp(F, W / 2, 0.55);
      const t = new THREE.Mesh(
        new THREE.PlaneGeometry(1.5, 1.0),
        lit(
          new THREE.MeshLambertMaterial({
            map: textTex(['TO LET', 'APPLY AGAR & CO', 'SOLICITORS'], {
              w: 256,
              h: 170,
              bg: '#e9e4d2',
              fg: '#8a1a1a',
              font: 'serif',
            }),
            side: THREE.DoubleSide,
          }),
        ),
      );
      t.position.set(x, 5.2, z);
      t.rotation.y = F.ry + Math.PI / 2;
      root.add(t);
      const [bx, bz] = fp(F, W / 2, 0.3);
      bt.add(M.flat, xform(new THREE.BoxGeometry(0.06, 0.06, 1.2), bx, 5.75, bz, F.ry), '#333');
    }
    if (b.id === 'fish') bt.add(M.paint, fbox(F, 0.3, W - 0.3, 2.44, 2.5, 1.5, 1.5), '#d9e4ea');
    upper(4.2, Math.max(1, Math.round(W / 3.6)), 1.05, 1.55, !b.shut);
    if (k === 'pub') {
      for (let i = 0; i < 2; i++) board(bt, F, (W * (i + 0.5)) / 2, 4.2, 1.15, 1.6, '#5d584c');
    }
  } else if (k === 'hotel') {
    bt.add(wm, fbox(F, 3.4, W - 0.6, 0, 3.0, 0.9, 0.9), tone);
    bt.add(M.slate, fbox(F, 3.3, W - 0.5, 3.0, 3.2, 1.0, 1.1), '#aaa');
    win(bt, F, 5.4, 0.9, 1.3, 1.7);
    win(bt, F, W - 2.6, 0.9, 1.3, 1.7);
    bt.add(M.paint, fbox(F, 1.0, 2.2, 0.14, 2.3, 0.02, 0.1), '#1f2a3a');
    bt.add(M.flat, fbox(F, 0.8, 2.4, 2.3, 2.5, 0.5, 0.6), '#77736a');
    signMesh(
      root,
      F,
      3.4,
      W - 0.6,
      3.3,
      3.95,
      0.05,
      signTex(b.sign, b.sub, '#2a2420', '#d9c98a', 'serif', 1024, 96),
    );
    for (let s = 1; s < b.st; s++) upper(4.6 + (s - 1) * 3, 3);
  } else if (k === 'works' || k === 'school') {
    const n = Math.max(2, Math.round(W / 4.2));
    for (let s = 0; s < b.st; s++)
      for (let i = 0; i < n; i++) {
        const a = (W * (i + 0.5)) / n,
          y = 1.2 + s * (H / b.st);
        if (b.shut) {
          board(bt, F, a, y, 1.7, 2.3, s ? '#57534a' : '#625c50');
        } else win(bt, F, a, y, 1.6, 2.2);
      }
    if (b.sign)
      signMesh(
        root,
        F,
        W * 0.08,
        W * 0.92,
        H - 1.25,
        H - 0.35,
        0.03,
        signTex(b.sign, '', b.brick === 'red' ? '#4a2a22' : '#3a322c', '#b9ad92', 'slab', 1024, 72),
      );
    if (b.id === 'laundry') {
      bt.add(M.red, wallBox(2.2, 19, 2.2, b.x1 - 2, 9.5, b.z0 + 3), '#999');
      bt.add(M.iron, fbox(F, W / 2 - 1.8, W / 2 + 1.8, 0, 3.2, 0.05, 0.08), '#3a4a3a');
    }
    if (k === 'school') bt.add(M.iron, fbox(F, W / 2 - 1.6, W / 2 + 1.6, 0, 2.8, 0.05, 0.08), '#2a2f3a');
  } else if (k === 'ware') {
    bt.add(M.iron, fbox(F, W / 2 - 2, W / 2 + 2, 0, 3.8, 0.05, 0.1), b.burnt ? '#1a1816' : '#2f4a3a');
    for (let s = 1; s < 3; s++) {
      bt.add(
        M.iron,
        fbox(F, W / 2 - 1.1, W / 2 + 1.1, s * 3.7 + 0.3, s * 3.7 + 2.7, 0.04, 0.08),
        b.burnt ? '#141210' : '#3a3530',
      );
      for (const a of [W * 0.2, W * 0.8]) {
        if (b.burnt)
          bt.add(M.flat, fbox(F, a - 0.6, a + 0.6, s * 3.7 + 0.7, s * 3.7 + 2.1, 0.02, 0.05), '#050505');
        else win(bt, F, a, s * 3.7 + 0.7, 1.2, 1.4, false);
      }
    }
    bt.add(M.flat, fbox(F, W / 2 - 0.12, W / 2 + 0.12, H - 0.9, H - 0.6, 1.6, 1.8), '#222');
    signMesh(
      root,
      F,
      W / 2 + 2.6,
      W / 2 + 4.4,
      1.6,
      3.2,
      0.03,
      textTex([b.sign], {
        w: 128,
        h: 128,
        bg: b.burnt ? '#1c1a18' : '#d9d2bc',
        fg: b.burnt ? '#6a655a' : '#1a1a1a',
        font: 'slab',
      }),
    );
    if (b.burnt) {
      for (let a = -1; a < W + 1; a += 2.4) {
        const [x, z] = fp(F, a, 2.2);
        bt.add(M.iron, xform(new THREE.BoxGeometry(0.06, 2.1, 0.06), x, 1.05, z), '#777');
      }
      const [x, z] = fp(F, W / 2, 2.2);
      bt.add(M.mark, xform(new THREE.BoxGeometry(W + 2, 1.9, 0.02), x, 1.05, z, F.ry), '#59605c');
      signMesh(
        root,
        F,
        W / 2 - 1,
        W / 2 + 1,
        0.9,
        1.7,
        2.24,
        textTex(['DANGER', 'KEEP OUT'], { w: 256, h: 110, bg: '#e8d820', fg: '#111', font: 'plain' }),
      );
    }
  } else if (k === 'chapel') {
    bt.add(M.paint, fbox(F, W / 2 - 0.9, W / 2 + 0.9, 0.1, 2.9, 0.04, 0.12), '#3a2a1e');
    bt.add(M.flat, fbox(F, W / 2 - 1.15, W / 2 + 1.15, 2.9, 3.15, 0.1, 0.16), '#8d887a');
    const stained = textTex([''], { w: 64, h: 128, bg: '#22304a' });
    const sm = new THREE.Mesh(
      fquad(F, W / 2 - 0.8, W / 2 + 0.8, 4.0, 7.4, 0.04),
      lit(
        new THREE.MeshLambertMaterial({
          map: stained,
          emissive: new THREE.Color('#c08a3a'),
          emissiveIntensity: 0,
        }),
      ),
    );
    root.add(sm);
    town.stained = sm.material;
    bt.add(M.flat, fbox(F, W / 2 - 0.09, W / 2 + 0.09, 11.2, 12.8, 0.0, 0.18), '#9a958a');
    bt.add(M.flat, fbox(F, W / 2 - 0.5, W / 2 + 0.5, 12.1, 12.3, 0.0, 0.18), '#9a958a');
    for (const a of [3.5, W - 3.5]) win(bt, F, a, 1.6, 0.9, 2.6, false);
    signMesh(
      root,
      F,
      W / 2 + 1.5,
      W / 2 + 3.3,
      1.0,
      2.0,
      0.05,
      textTex(['STAR OF THE SEA', 'R.C. CHAPEL', 'Mass daily 8'], {
        w: 256,
        h: 150,
        bg: '#1a2a1e',
        fg: '#d9c98a',
        font: 'serif',
      }),
    );
  } else if (k === 'office') {
    bt.add(M.stone, fbox(F, 0, W, 3.3, 3.7, 0.08, 0.1), '#ccc');
    bt.add(M.paint, fbox(F, W / 2 - 0.7, W / 2 + 0.7, 0.14, 2.4, 0.03, 0.1), '#1a2a40');
    bt.add(M.flat, fbox(F, W / 2 - 1.2, W / 2 + 1.2, 2.4, 2.6, 0.7, 0.8), '#6a665c');
    for (const a of [2.2, W - 2.2]) win(bt, F, a, 1.0, 1.3, 1.7);
    upper(4.3, 3);
    signMesh(
      root,
      F,
      W / 2 - 2.6,
      W / 2 + 2.6,
      2.65,
      3.3,
      0.72,
      signTex(b.sign, b.sub, '#17243a', '#e3dcc6', 'serif', 1024, 128),
    );
    bt.add(M.flat, xform(new THREE.CylinderGeometry(0.04, 0.05, 5, 6), cx, H + 4, cz), '#bbb');
  } else if (k === 'bank' || k === 'hall') {
    const n = Math.max(3, Math.round(W / 5));
    for (let i = 0; i < n; i++) {
      const a = (W * (i + 0.5)) / n;
      bt.add(
        M.flat,
        fbox(F, a - 1.3, a + 1.3, 0.1, k === 'hall' ? 4.6 : 3.4, 0.03, 0.2),
        i === Math.floor(n / 2) ? '#141414' : '#1c1f24',
      );
      bt.add(
        M.stone,
        fbox(F, a - 1.5, a + 1.5, k === 'hall' ? 4.6 : 3.4, (k === 'hall' ? 4.6 : 3.4) + 0.35, 0.12, 0.2),
        '#ddd',
      );
      if (k === 'bank') for (let s = 1; s < 3; s++) win(bt, F, a, 4.6 + (s - 1) * 3.2, 1.2, 1.9);
    }
    signMesh(
      root,
      F,
      W * 0.12,
      W * 0.88,
      H - 1.6,
      H - 0.5,
      0.04,
      signTex(
        b.sign,
        '',
        b.brick === 'stone' ? '#6d6858' : '#4a2a22',
        b.brick === 'stone' ? '#1c1a16' : '#d9cfb4',
        'serif',
        1024,
        96,
      ),
    );
    if (k === 'bank') {
      signMesh(
        root,
        F,
        0.5,
        1.5,
        1.4,
        1.9,
        0.05,
        textTex(['AGAR & CO', 'SOLICITORS'], { w: 200, h: 100, bg: '#b8943a', fg: '#1a1408', font: 'serif' }),
      );
      const [x, z] = fp(F, W / 2 + 0.2, 0.5);
      bt.add(M.flat, xform(new THREE.BoxGeometry(0.22, 0.2, 0.5), x, 4.4, z, F.ry), '#d8d8d8');
    }
    if (b.id === 'station') {
      const [x, z] = fp(F, W / 2, 0.1);
      const ck = new THREE.Mesh(
        new THREE.CircleGeometry(0.9, 24),
        new THREE.MeshBasicMaterial({ color: '#e8dfb8' }),
      );
      ck.position.set(x, H + 1.2, z);
      ck.rotation.y = F.ry;
      root.add(ck);
      town.clock = ck;
    }
  }
  // the other faces: a few dark windows so backs and sides are not blank
  if (!['ware', 'chapel', 'cabin', 'shed', 'bank', 'hall'].includes(k) && F.D > 6 && !b.burnt) {
    const Fb = frame(Object.assign({}, b, { face: { W: 'E', E: 'W', N: 'S', S: 'N' }[b.face] }));
    for (let s = 0; s < b.st; s++) {
      const n = Math.max(1, Math.round(W / 5));
      for (let i = 0; i < n; i++) win(bt, Fb, (W * (i + 0.5)) / n, 1.2 + s * 3, 0.95, 1.4, rr() < 0.4);
    }
  }
}
function signMesh(root, F, a0, a1, y0, y1, out, texture, id) {
  const m = new THREE.Mesh(
    fquad(F, a0, a1, y0, y1, out + 0.012),
    lit(new THREE.MeshLambertMaterial({ map: texture })),
  );
  m.matrixAutoUpdate = false;
  root.add(m);
  if (id) town.signs.push(m);
  return m;
}

// ---------- ground ----------
function ground(bt) {
  const land = [
    [BOUNDS.x0 - 60, BOUNDS.z0 - 60, BOUNDS.x1 + 60, -118],
    [BOUNDS.x0 - 60, -96, BOUNDS.x1 + 60, 62],
  ];
  for (const l of land) bt.add(M.concrete, planeXZ(l[0], l[1], l[2], l[3], -0.03, 3), '#b8b8b8');
  ROADS.forEach((r) => bt.add(M.asphalt, planeXZ(r.x0, r.z0, r.x1, r.z1, r.n === 'qs' ? 0 : 0.003, 4)));
  SETTS.forEach((r, i) =>
    bt.add(
      r.n === 'pier' ? M.planks : M.setts,
      planeXZ(r.x0, r.z0, r.x1, r.z1, 0.006 + i * 0.0015, r.n === 'pier' ? 2 : 1.6),
      r.n === 'scrap' ? '#8a7a6a' : '#ffffff',
    ),
  );
  bt.add(M.planks, planeXZ(-58, 62, -52, 78, 0.01, 2));
  PAVE.forEach((r) => {
    const g = wallBox(r.x1 - r.x0, 0.3, r.z1 - r.z0, (r.x0 + r.x1) / 2, -0.03, (r.z0 + r.z1) / 2, 1.8);
    bt.add(M.flags, g);
  });
  const mk = (x0, z0, x1, z1, c = '#d9d6cc') => bt.add(M.mark, planeXZ(x0, z0, x1, z1, 0.012), c);
  for (let z = -204; z < 38; z += 6) {
    if ((z > -24 && z < -12) || (z > 9 && z < 17)) continue;
    mk(-0.06, z, 0.06, z + 3);
  }
  for (let x = -124; x < 158; x += 6) {
    if (x > -8 && x < 8) continue;
    mk(x, 47.94, x + 3, 48.06);
  }
  for (let x = -4.6; x < 5; x += 1.2) mk(x, 11.4, x + 0.6, 14.6, '#e2e0d6');
  for (const sx of [-1, 1]) {
    mk(sx * 4.85 - 0.04, -90, sx * 4.85 + 0.04, -26, '#b89a2a');
    mk(sx * 4.65 - 0.04, -90, sx * 4.65 + 0.04, -26, '#b89a2a');
    for (let z = 5; z < 22; z += 2) {
      mk(sx * 4.75 - 0.05, z, sx * 4.75 + 0.05, z + 1);
    }
  }
  for (let x = -4.6; x < 4.8; x += 1.0) {
    mk(x, 43.3, x + 0.6, 43.5);
  }
  mk(3.1, 30.5, 3.2, 41.5);
  mk(3.1, 30.5, 5, 30.6);
  mk(3.1, 41.4, 5, 41.5);
  // quay walls and the bridge
  bt.add(
    M.stone,
    wallBox(BOUNDS.x1 - BOUNDS.x0 + 120, 2.6, 0.8, (BOUNDS.x0 + BOUNDS.x1) / 2, -1.3, 62.2),
    '#999',
  );
  bt.add(
    M.stone,
    wallBox(BOUNDS.x1 - BOUNDS.x0 + 120, 2.6, 0.8, (BOUNDS.x0 + BOUNDS.x1) / 2, -1.3, -96.2),
    '#888',
  );
  bt.add(
    M.stone,
    wallBox(BOUNDS.x1 - BOUNDS.x0 + 120, 2.6, 0.8, (BOUNDS.x0 + BOUNDS.x1) / 2, -1.3, -117.8),
    '#888',
  );
  bt.add(M.stone, wallBox(16.8, 0.9, 26, 0, -0.5, -107), '#aaa');
  for (const sx of [-1, 1]) {
    bt.add(M.stone, wallBox(0.5, 1.15, 31, sx * 8.25, 0.57, -107), '#bbb');
    for (const z of [-99, -107, -115]) bt.add(M.stone, wallBox(1.4, 3.2, 1.4, sx * 7.6, -1.6, z), '#999');
  }
  bt.add(M.asphalt, planeXZ(-5, -122, 5, -92, 0.002, 4));
  bt.add(M.flags, wallBox(3, 0.14, 30, 6.5, 0.05, -107, 1.8));
  bt.add(M.flags, wallBox(3, 0.14, 30, -6.5, 0.05, -107, 1.8));
  for (let z = 64; z < 98; z += 5)
    for (const x of [60.3, 69.7])
      bt.add(M.flat, xform(new THREE.CylinderGeometry(0.22, 0.22, 3.2, 7), x, -1.5, z), '#2a241e');
  bt.add(M.flat, boxG(6, 0.5, 16, -55, -0.26, 70), '#3a3a36');
  for (const w of WALLS) {
    const scrap = w.x1 < -78 && w.z0 > 15,
      sh = w.z0 > 58 && w.x0 < -40;
    if (sh) continue;
    bt.add(
      scrap ? M.iron : M.soot,
      wallBox(
        w.x1 - w.x0 + 0.02,
        scrap ? 2.5 : 2.3,
        w.z1 - w.z0 + 0.02,
        (w.x0 + w.x1) / 2,
        scrap ? 1.25 : 1.15,
        (w.z0 + w.z1) / 2,
      ),
      scrap ? '#8a8474' : '#c8c4be',
    );
  }
}

// ---------- street furniture ----------
function lamp(bt, root, l) {
  const col = '#3d4a44',
    h = l.k === 2 ? 4.6 : 7.4;
  let ax = 0,
    az = 0;
  if (Math.abs(l.x) < 9 && l.z < 41) ax = -Math.sign(l.x);
  else if (l.z > 56) az = -1;
  else if (l.z > 41) az = 1;
  else if (l.z > -16 && l.z < -12) az = -1;
  else az = 1;
  let hx = l.x,
    hz = l.z;
  if (l.k === 1) {
    bt.add(M.flat, xform(new THREE.CylinderGeometry(0.07, 0.11, h, 7), l.x, h / 2, l.z), col);
    bt.add(M.flat, xform(new THREE.CylinderGeometry(0.16, 0.18, 1.1, 7), l.x, 0.55, l.z), col);
    hx = l.x + ax * 1.5;
    hz = l.z + az * 1.5;
    bt.add(
      M.flat,
      xform(new THREE.BoxGeometry(ax ? 1.6 : 0.07, 0.07, ax ? 0.07 : 1.6), (l.x + hx) / 2, h, (l.z + hz) / 2),
      col,
    );
  }
  bt.add(M.flat, boxG(0.34, 0.16, 0.7, hx, h - 0.02, hz, ax ? Math.PI / 2 : 0), '#555');
  const lens = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.08, 0.56), M.lens.clone());
  lens.position.set(hx, h - 0.13, hz);
  if (ax) lens.rotation.y = Math.PI / 2;
  root.add(lens);
  const s = new THREE.Sprite(M.halo.clone());
  s.position.set(hx, h - 0.2, hz);
  s.scale.setScalar(l.dim ? 2.4 : 4.2);
  root.add(s);
  town.halos.push({ s, lens, l, base: l.dim ? 2.4 : 4.2, ph: rr() * 10 });
}
function prop(bt, root, p) {
  const { x, z, t } = p,
    c = (g, col, m = M.flat) => bt.add(m, g, col);
  if (t === 'phonebox') {
    c(boxG(0.95, 2.35, 0.95, x, 1.18, z), '#a3161a', M.paint);
    c(boxG(1.02, 0.14, 1.02, x, 2.42, z), '#8a1216');
    const g = new THREE.Mesh(
      new THREE.BoxGeometry(0.97, 1.5, 0.97),
      new THREE.MeshBasicMaterial({ color: new THREE.Color(1.6, 1.5, 1.2), transparent: true, opacity: 0.0 }),
    );
    g.position.set(x, 1.35, z);
    root.add(g);
    town.phoneGlow = g.material;
    for (const [dx, dz] of [
      [0.48, 0],
      [-0.48, 0],
      [0, 0.48],
      [0, -0.48],
    ])
      c(boxG(dx ? 0.02 : 0.7, 1.45, dz ? 0.02 : 0.7, x + dx, 1.4, z + dz), '#1a2024');
    c(boxG(0.6, 0.16, 0.02, x, 2.22, z - 0.49), '#e8e0c8');
  } else if (t === 'pillarbox') {
    c(xform(new THREE.CylinderGeometry(0.24, 0.24, 1.35, 12), x, 0.68, z), '#a3161a', M.paint);
    c(xform(new THREE.CylinderGeometry(0.28, 0.25, 0.12, 12), x, 1.4, z), '#8a1216');
    c(xform(new THREE.CylinderGeometry(0.26, 0.26, 0.25, 12), x, 0.12, z), '#151515');
    c(boxG(0.03, 0.05, 0.22, x + 0.24, 1.08, z), '#111');
  } else if (t === 'busshelter') {
    for (const dz of [-1.7, 1.7]) c(boxG(0.07, 2.3, 0.07, x, 1.15, z + dz), '#2f4a6a');
    c(boxG(1.5, 0.07, 3.7, x + 0.6, 2.33, z), '#2f4a6a');
    c(boxG(0.03, 1.5, 3.4, x - 0.05, 1.35, z), '#6f8088', M.mark);
    c(boxG(0.3, 0.06, 2.4, x + 0.3, 0.5, z), '#7a4a2a');
    c(boxG(0.06, 2.9, 0.06, x + 1.3, 1.45, z + 2.2), '#555');
    c(boxG(0.04, 0.4, 0.5, x + 1.3, 2.75, z + 2.2), '#c8a020');
  } else if (t === 'busstop') {
    c(boxG(0.06, 2.9, 0.06, x, 1.45, z), '#555');
    c(boxG(0.04, 0.4, 0.5, x, 2.75, z), '#c8a020');
  } else if (t === 'ranksign') {
    c(boxG(0.06, 2.6, 0.06, x, 1.3, z), '#555');
    signMesh(
      root,
      { ox: x - 0.35, oz: z, ux: 1, uz: 0, nx: 0, nz: 1, ry: 0 },
      0,
      0.7,
      2.1,
      2.6,
      0.02,
      textTex(['CABS', "MICKEY'S"], { w: 128, h: 96, bg: '#f0c818', fg: '#111', font: 'cab' }),
    );
  } else if (t === 'belisha') {
    for (let i = 0; i < 5; i++)
      c(
        xform(new THREE.CylinderGeometry(0.05, 0.05, 0.5, 6), x, 0.25 + i * 0.5, z),
        i % 2 ? '#e8e8e0' : '#141414',
      );
    const b = new THREE.Mesh(
      new THREE.SphereGeometry(0.17, 10, 8),
      new THREE.MeshBasicMaterial({ color: '#c87a10' }),
    );
    b.position.set(x, 2.68, z);
    root.add(b);
    town.blinkers.push(b);
  } else if (t === 'bin') {
    c(xform(new THREE.CylinderGeometry(0.26, 0.22, 0.85, 8), x, 0.55, z), '#2a3a2e');
    c(boxG(0.06, 1.1, 0.06, x, 0.55, z), '#333');
  } else if (t === 'dustbin') {
    c(xform(new THREE.CylinderGeometry(0.3, 0.26, 0.8, 10), x, 0.4, z), '#6f7478', M.iron);
    c(xform(new THREE.CylinderGeometry(0.33, 0.33, 0.07, 10), x, 0.84, z), '#5a5f63');
  } else if (t === 'skip') {
    c(boxG(2.2, 1.0, 1.5, x, 0.55, z), '#b8901a', M.iron);
    for (let i = 0; i < 6; i++)
      c(
        boxG(
          0.4 + rr() * 0.6,
          0.2,
          0.3 + rr() * 0.5,
          x + (rr() - 0.5) * 1.6,
          1.1 + rr() * 0.2,
          z + (rr() - 0.5),
          rr() * 3,
        ),
        ['#5a3327', '#777', '#4a4238'][i % 3],
      );
  } else if (t === 'boxes') {
    const cols = ['#c85a1a', '#d8d4c8', '#2f5a8a', '#c85a1a'];
    for (let i = 0; i < 9; i++) {
      const lx = ((i % 3) - 1) * 0.72,
        lz = (Math.floor(i / 3) - 1) * 0.5,
        n = 1 + Math.floor(rr() * 4);
      for (let j = 0; j < n; j++)
        c(
          boxG(0.68, 0.24, 0.45, x + lx, 0.13 + j * 0.25, z + lz, (rr() - 0.5) * 0.15),
          cols[Math.floor(rr() * 4)],
          M.paint,
        );
    }
  } else if (t === 'nets') {
    for (let i = 0; i < 5; i++)
      c(
        xform(
          new THREE.IcosahedronGeometry(0.75, 1),
          x + (rr() - 0.5) * 1.4,
          0.3 + rr() * 0.25,
          z + (rr() - 0.5) * 1.2,
          rr() * 3,
          0,
          0,
          1,
          0.5,
          1,
        ),
        ['#2f5a4a', '#3a4a3a', '#8a4a1a', '#2a4a5a'][i % 4],
      );
    for (let i = 0; i < 6; i++)
      c(
        xform(
          new THREE.SphereGeometry(0.11, 6, 5),
          x + (rr() - 0.5) * 1.8,
          0.55 + rr() * 0.3,
          z + (rr() - 0.5) * 1.5,
        ),
        '#c8641a',
      );
  } else if (t === 'bollard') {
    c(xform(new THREE.CylinderGeometry(0.2, 0.26, 0.6, 8), x, 0.3, z), '#1a1a1a');
    c(xform(new THREE.CylinderGeometry(0.3, 0.2, 0.14, 8), x, 0.66, z), '#1a1a1a');
  } else if (t === 'crane') {
    const col = '#4a5a52';
    for (const [dx, dz] of [
      [-1.6, -1.3],
      [1.6, -1.3],
      [-1.6, 1.3],
      [1.6, 1.3],
    ])
      c(boxG(0.28, 9, 0.28, x + dx, 4.5, z + dz), col, M.iron);
    c(boxG(3.6, 0.3, 3.0, x, 9, z), col, M.iron);
    c(boxG(2.4, 2.4, 2.2, x, 10.3, z), '#56665c', M.iron);
    c(boxG(1.0, 0.9, 0.05, x - 0.4, 10.6, z + 1.12), '#11161a');
    c(xform(new THREE.BoxGeometry(0.3, 0.3, 17), x, 15.5, z + 6.6, 0, -0.62), col, M.iron);
    c(xform(new THREE.BoxGeometry(0.16, 0.16, 12), x, 14.4, z + 2.4, 0, -1.05), col, M.iron);
    c(boxG(0.03, 9, 0.03, x, 16, z + 13.4), '#111');
    c(boxG(0.4, 0.5, 0.4, x, 11.5, z + 13.4), '#222');
  } else if (t === 'hut') {
    c(boxG(2.0, 2.3, 2.0, x, 1.15, z), '#3a4a3a', M.planks);
    c(boxG(2.3, 0.1, 2.3, x, 2.35, z), '#222');
    c(boxG(0.7, 0.6, 0.03, x + 0.3, 1.5, z - 1.01), '#c8a850', M.fireM);
  } else if (t === 'brazier') {
    c(xform(new THREE.CylinderGeometry(0.3, 0.24, 0.5, 8), x, 0.75, z), '#1a1614', M.iron);
    for (const a of [0, 2.1, 4.2])
      c(boxG(0.04, 0.55, 0.04, x + Math.sin(a) * 0.22, 0.27, z + Math.cos(a) * 0.22), '#1a1614');
    const f = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.5, 6), M.fireM);
    f.position.set(x, 1.15, z);
    root.add(f);
    town.fire = f;
  } else if (t === 'shelter') {
    for (const dx of [-3, 3]) c(boxG(0.08, 2.3, 0.08, x + dx, 1.15, z - 1.3), '#2a3a4a');
    c(boxG(6.3, 0.08, 1.9, x, 2.34, z - 0.1), '#2a3a4a');
    c(boxG(6.1, 2.2, 0.06, x, 1.15, z + 0.85), '#4a5a62', M.iron);
    c(boxG(5, 0.07, 0.4, x, 0.5, z + 0.55), '#7a4a2a');
    for (const dx of [-3, 3]) c(boxG(0.06, 2.2, 1.7, x + dx, 1.15, z), '#4a5a62', M.mark);
  } else if (t === 'scrap') {
    for (let i = 0; i < 26; i++) {
      const a = rr() * 6.3,
        d = rr() * p.r,
        hh = (1 - d / p.r) * 2.2;
      c(
        xform(
          rr() < 0.3
            ? new THREE.CylinderGeometry(0.2, 0.2, 0.8 + rr(), 6)
            : new THREE.BoxGeometry(0.4 + rr() * 1.2, 0.15 + rr() * 0.5, 0.3 + rr() * 0.9),
          x + Math.sin(a) * d,
          rr() * hh + 0.2,
          z + Math.cos(a) * d,
          rr() * 3,
          rr() * 1.4,
          rr(),
        ),
        ['#5a3a26', '#6a4a34', '#4a4a48', '#3a2a22', '#77736a'][i % 5],
        M.iron,
      );
    }
  } else if (t === 'scrapcar') {
    c(boxG(1.7, 0.7, 4, x, 0.5, z, 0.4), '#4a2f22', M.iron);
    c(boxG(1.5, 0.55, 2, x, 1.1, z, 0.4), '#3a2a22', M.iron);
  } else if (t === 'stall') {
    for (const [dx, dz] of [
      [-1.3, -0.8],
      [1.3, -0.8],
      [-1.3, 0.8],
      [1.3, 0.8],
    ])
      c(boxG(0.06, 2.3, 0.06, x + dx, 1.15, z + dz), '#555');
    c(boxG(2.8, 0.08, 1.7, x, 0.9, z), '#6a5a44', M.planks);
    const s = rr() < 0.5 ? '#a3261a' : '#1f5a3a';
    for (let i = 0; i < 6; i++)
      c(
        xform(new THREE.BoxGeometry(0.5, 0.04, 2.0), x - 1.25 + i * 0.5, 2.35, z, 0, 0, 0),
        i % 2 ? s : '#e2dcc8',
        M.paint,
      );
    for (let i = 0; i < 6; i++)
      c(
        boxG(0.35, 0.2, 0.3, x - 1 + i * 0.4, 1.05, z + (rr() - 0.5) * 0.8),
        ['#8a5a1a', '#3a7a2a', '#b8401a', '#c8b82a'][i % 4],
      );
  } else if (t === 'clock') {
    c(xform(new THREE.CylinderGeometry(0.12, 0.2, 4.4, 8), x, 2.2, z), '#1f3a2a');
    c(boxG(0.9, 0.9, 0.5, x, 4.8, z), '#1f3a2a');
    const ck = new THREE.Mesh(
      new THREE.CircleGeometry(0.36, 16),
      new THREE.MeshBasicMaterial({ color: '#e8dfb8' }),
    );
    ck.position.set(x, 4.8, z + 0.26);
    root.add(ck);
  } else if (t === 'ladder') {
    for (const dz of [-0.22, 0.22])
      c(xform(new THREE.BoxGeometry(0.05, 4.2, 0.05), x + 0.2, 2.0, z + dz, 0, 0, 0.2), '#b8a070');
    for (let i = 0; i < 9; i++) c(boxG(0.03, 0.03, 0.44, x + 0.58 - i * 0.094, 0.4 + i * 0.44, z), '#b8a070');
  } else if (t === 'bench') {
    c(boxG(0.45, 0.06, 1.9, x, 0.47, z), '#3a4a34', M.planks);
    c(boxG(0.06, 0.5, 1.9, x - 0.22, 0.75, z), '#3a4a34', M.planks);
    for (const dz of [-0.8, 0.8]) c(boxG(0.4, 0.45, 0.06, x, 0.23, z + dz), '#222');
  } else if (t === 'cross') {
    c(boxG(0.7, 0.3, 0.7, x, 0.15, z), '#77736a', M.stone);
    c(boxG(0.22, 2.2, 0.22, x, 1.4, z), '#8a867a', M.stone);
    c(boxG(0.9, 0.22, 0.22, x, 2.0, z), '#8a867a', M.stone);
  } else if (t === 'chair') {
    c(boxG(0.4, 0.04, 0.4, x, 0.45, z), '#7a2a22');
    c(boxG(0.04, 0.45, 0.4, x - 0.18, 0.7, z), '#7a2a22');
    for (const [dx, dz] of [
      [-0.17, -0.17],
      [0.17, -0.17],
      [-0.17, 0.17],
      [0.17, 0.17],
    ])
      c(boxG(0.03, 0.45, 0.03, x + dx, 0.22, z + dz), '#999');
  }
}
function boat(root, kind, x, z, ry, col) {
  const g = new THREE.Group(),
    bt = new Batch(),
    L = kind === 'ferry' ? 26 : 13,
    Wd = kind === 'ferry' ? 7 : 4;
  const hull = new THREE.BoxGeometry(Wd, kind === 'ferry' ? 3 : 2.2, L, 1, 1, 6),
    p = hull.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const zz = p.getZ(i) / (L / 2);
    const k = zz > 0.3 ? 1 - Math.pow((zz - 0.3) / 0.7, 1.6) * 0.92 : 1;
    p.setX(i, p.getX(i) * k * (p.getY(i) < 0 ? 0.8 : 1));
    if (zz > 0.6 && p.getY(i) > 0) p.setY(i, p.getY(i) + (zz - 0.6) * 1.2);
  }
  hull.computeVertexNormals();
  bt.add(M.paint, hull, col);
  if (kind === 'ferry') {
    bt.add(M.paint, boxG(6, 2.4, 15, 0, 2.7, -2), '#e8e4d8');
    bt.add(M.paint, boxG(4.4, 2, 5, 0, 4.9, 2), '#e8e4d8');
    bt.add(M.paint, xform(new THREE.CylinderGeometry(0.8, 0.9, 2.6, 10), 0, 6, -4), '#c8401a');
    const wm = new THREE.Mesh(
      new THREE.BoxGeometry(6.06, 0.7, 13),
      new THREE.MeshBasicMaterial({ color: new THREE.Color(1.8, 1.5, 0.9) }),
    );
    wm.position.set(0, 3.0, -2);
    g.add(wm);
    town.ferryLights = wm.material;
  } else {
    bt.add(M.paint, boxG(2.4, 2.2, 3, 0, 2.1, -3), '#e2dccb');
    bt.add(M.flat, boxG(2.0, 0.6, 0.05, 0, 2.6, -1.48), '#11161a');
    bt.add(M.flat, xform(new THREE.CylinderGeometry(0.08, 0.1, 6.5, 6), 0, 4.2, 2), '#3a3530');
    bt.add(M.flat, xform(new THREE.BoxGeometry(0.08, 0.08, 5), 0, 5.2, 0, 0, 0.5), '#3a3530');
    bt.add(M.iron, boxG(3, 2.6, 0.2, 0, 2.4, -5.6), '#4a4a44');
    bt.add(M.flat, boxG(2.8, 0.2, 5.4, 0, 1.15, 1.6), '#4a4238');
  }
  bt.build(g);
  g.position.set(x, kind === 'ferry' ? -1.0 : -0.9, z);
  g.rotation.y = ry;
  root.add(g);
  g.userData = { y: g.position.y, ph: rr() * 6 };
  return g;
}

export function buildTown(scene) {
  materials();
  const root = new THREE.Group();
  root.name = 'town';
  scene.add(root);
  const gb = new Batch();
  ground(gb);
  town.groundMeshes = gb.build(root, { layer: 1, cull: false });
  const bt = new Batch();
  for (const b of BLD) building(bt, b, root);
  for (const l of LAMPS) lamp(bt, root, l);
  for (const p of PROPS) prop(bt, root, p);
  bt.build(root, { cull: false });
  {
    const list = PROPS.filter((p) => p.r > 0.15 && !['crane', 'scrap'].includes(p.t))
      .map((p) => [p.x, p.z, p.r * 2.6 + 0.5])
      .concat(LAMPS.filter((l) => l.k === 1).map((l) => [l.x, l.z, 0.9]));
    const im = new THREE.InstancedMesh(
      new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2),
      new THREE.MeshBasicMaterial({
        map: blobTex(),
        transparent: true,
        depthWrite: false,
        polygonOffset: true,
        polygonOffsetFactor: -4,
        polygonOffsetUnits: -4,
      }),
      list.length,
    );
    const d = new THREE.Object3D();
    list.forEach((b, i) => {
      d.position.set(b[0], 0.135, b[1]);
      d.scale.set(b[2], 1, b[2]);
      d.updateMatrix();
      im.setMatrixAt(i, d.matrix);
    });
    im.layers.set(1);
    im.frustumCulled = false;
    root.add(im);
  }
  town.boats.push(
    boat(root, 'trawler', 57.2, 76, 0, '#1f3a5a'),
    boat(root, 'trawler', 72.8, 86, Math.PI, '#5a2a22'),
    boat(root, 'trawler', 122, 65, Math.PI / 2, '#2a3f34'),
  );
  town.ferry = boat(root, 'ferry', -55, 86, Math.PI / 2, '#1f2f4a');
  // windows where named people sit at home: lit when they are roused, dark when they only watch
  for (const id in WINDOWS) {
    let [x, z, a, y] = WINDOWS[id],
      ww = 1.0,
      wh = 1.45;
    {
      let best = null,
        bd = 1e9;
      for (const sp of town.winSpots) {
        if (sp.nx * Math.sin(a) + sp.nz * Math.cos(a) < 0.7 || Math.abs(sp.y - y) > 1.3) continue;
        const d = Math.hypot(sp.x - x, sp.z - z);
        if (d < bd) {
          bd = d;
          best = sp;
        }
      } // the watcher's window is a real one on the wall: the nearest pane to where the rule puts their eyes
      if (best && bd < 5) {
        x = best.x - best.nx * 0.03;
        z = best.z - best.nz * 0.03;
        y = best.y;
        ww = best.w;
        wh = best.h;
        a = Math.atan2(best.nx, best.nz);
      }
      town.winAt[id] = { x, y, z, ang: a, w: ww, h: wh, snapped: !!best && bd < 5 };
    }
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry(ww, wh),
      new THREE.MeshBasicMaterial({ color: new THREE.Color(2.4, 1.8, 0.9) }),
    );
    m.position.set(x + Math.sin(a) * 0.06, y, z + Math.cos(a) * 0.06);
    m.rotation.y = a;
    m.visible = false;
    root.add(m);
    const sil = new THREE.Mesh(
      new THREE.PlaneGeometry(0.42, 0.75),
      new THREE.MeshBasicMaterial({ color: '#0a0806' }),
    );
    sil.position.set(0, -0.3, 0.01);
    m.add(sil);
    town.winLights[id] = m;
  }
  town.root = root;
  town.M = M;
  buildExtras(root, M, town);
  return root;
}
