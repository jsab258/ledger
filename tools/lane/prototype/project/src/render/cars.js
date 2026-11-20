// Vehicles drawn in code, as fictional 1990 shapes: a Kestrel saloon (Mickey's cabs), a Wren hatchback, a Carrier van,
// a flatbed and a corporation double-decker. Bevelled panels, arches, bumpers, glass that carries the sky, and lights that work.
import { THREE, lit, boxG, xform, textTex, glowTex, signTex, mergeGeometries } from './core.js';

let glassM, darkM, chromeM, blackM, haloM, tailHaloM, poolM, skinM, plateTex;
const KIND = {
  saloon: {
    L: 4.3,
    W: 1.68,
    wb: 1.3,
    wr: 0.3,
    low: [
      [-2.15, 0.74, 0.8],
      [-2.06, 0.82, 0.9],
      [-1.3, 0.84, 0.93],
      [1.05, 0.84, 0.95],
      [1.98, 0.82, 0.86],
      [2.15, 0.76, 0.72],
    ],
    cab: { r0: -1.32, r1: -0.84, f1: 0.42, f0: 1.04, belt: 0.94, roof: 1.39, hb: 0.8, hr: 0.64 },
    chrome: true,
  },
  hatch: {
    L: 3.7,
    W: 1.6,
    wb: 1.12,
    wr: 0.28,
    low: [
      [-1.85, 0.72, 0.84],
      [-1.78, 0.79, 0.95],
      [0.85, 0.8, 0.95],
      [1.7, 0.78, 0.85],
      [1.85, 0.72, 0.7],
    ],
    cab: { r0: -1.76, r1: -1.4, f1: 0.28, f0: 0.86, belt: 0.95, roof: 1.39, hb: 0.76, hr: 0.62 },
  },
  van: {
    L: 4.6,
    W: 1.8,
    wb: 1.4,
    wr: 0.32,
    low: [
      [-2.3, 0.86, 1.02],
      [1.15, 0.88, 1.2],
      [1.8, 0.88, 1.2],
      [2.22, 0.84, 1.04],
      [2.3, 0.8, 0.8],
    ],
    box: [-2.3, 1.12, 1.98, 0.9],
    cab: { r0: 1.13, r1: 1.14, f1: 1.26, f0: 1.82, belt: 1.2, roof: 1.92, hb: 0.86, hr: 0.76 },
  },
  flatbed: {
    L: 5.6,
    W: 2.0,
    wb: 1.75,
    wr: 0.36,
    low: [
      [-2.8, 0.9, 0.96],
      [0.72, 0.9, 0.96],
      [0.74, 0.96, 1.28],
      [2.25, 0.96, 1.28],
      [2.7, 0.92, 1.1],
      [2.8, 0.88, 0.85],
    ],
    cab: { r0: 0.76, r1: 0.9, f1: 1.5, f0: 2.24, belt: 1.28, roof: 2.02, hb: 0.94, hr: 0.82 },
  },
};
function mats() {
  if (glassM) return;
  glassM = lit(
    new THREE.MeshPhongMaterial({
      vertexColors: true,
      specular: new THREE.Color(0.55, 0.6, 0.65),
      shininess: 120,
      transparent: true,
      opacity: 0.78,
      depthWrite: false,
    }),
  );
  darkM = lit(new THREE.MeshLambertMaterial({ color: '#0c0c0d' }));
  blackM = lit(new THREE.MeshStandardMaterial({ color: '#161617', roughness: 0.55 }));
  chromeM = lit(new THREE.MeshStandardMaterial({ color: '#a4aaae', roughness: 0.22, metalness: 0.85 }));
  haloM = new THREE.SpriteMaterial({
    map: glowTex(),
    color: new THREE.Color(1, 0.95, 0.8),
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    fog: false,
  });
  tailHaloM = new THREE.SpriteMaterial({
    map: glowTex(),
    color: new THREE.Color(1, 0.08, 0.04),
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    fog: false,
  });
  poolM = new THREE.MeshBasicMaterial({
    map: glowTex(),
    color: new THREE.Color(0.55, 0.5, 0.38),
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    fog: false,
    polygonOffset: true,
    polygonOffsetFactor: -6,
    polygonOffsetUnits: -6,
  });
  skinM = lit(new THREE.MeshLambertMaterial({ vertexColors: true }));
  plateTex = ['F417 MRD', 'D962 KAT', 'G208 HUL', 'B735 RYE', 'E551 WKY'].map((t) => [
    textTex([t], { w: 128, h: 32, bg: '#e9e9e2', fg: '#111', font: 'plain' }),
    textTex([t], { w: 128, h: 32, bg: '#e2c21a', fg: '#111', font: 'plain' }),
  ]);
}
export function setCarEnv(day) {
  if (glassM) glassM.color.setScalar(0.22 + 0.78 * day);
}
// a run of rounded cross-sections, flat-shaded so every panel catches the light on its own
function loft(st, y0, r = 0.07, caps = true) {
  const ring = ([z, hw, y1]) => [
    [-hw, y0, z],
    [-hw, y1 - r, z],
    [-hw + r * 0.32, y1 - r * 0.3, z],
    [-hw + r, y1, z],
    [hw - r, y1, z],
    [hw - r * 0.32, y1 - r * 0.3, z],
    [hw, y1 - r, z],
    [hw, y0, z],
  ];
  const R = st.map(ring),
    v = [],
    q = (a, b, c, d) => v.push(...a, ...b, ...c, ...a, ...c, ...d);
  for (let i = 0; i + 1 < R.length; i++)
    for (let j = 0; j < 7; j++) q(R[i][j], R[i + 1][j], R[i + 1][j + 1], R[i][j + 1]);
  if (caps) {
    const a = R[0],
      b = R[R.length - 1];
    for (let j = 1; j < 7; j++) {
      v.push(...a[0], ...a[j], ...a[j + 1]);
      v.push(...b[0], ...b[j + 1], ...b[j]);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3));
  g.computeVertexNormals();
  return g;
}
function beam(a, b, t) {
  const d = new THREE.Vector3(b[0] - a[0], b[1] - a[1], b[2] - a[2]),
    l = d.length(),
    g = new THREE.BoxGeometry(t, l, t),
    q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
  g.applyQuaternion(q);
  g.translate((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2);
  return g;
}
function pane(pts) {
  // glass: dark at the sill, sky at the top
  const g = new THREE.BufferGeometry(),
    v = [],
    c = [],
    ys = pts.map((p) => p[1]),
    y0 = Math.min(...ys),
    y1 = Math.max(...ys);
  for (const i of [0, 1, 2, 0, 2, 3]) {
    v.push(...pts[i]);
    const k = (pts[i][1] - y0) / (y1 - y0 || 1);
    c.push(0.04 + 0.3 * k, 0.055 + 0.36 * k, 0.07 + 0.42 * k);
  }
  g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3));
  g.setAttribute('color', new THREE.Float32BufferAttribute(c, 3));
  g.computeVertexNormals();
  return g;
}
const mesh = (g, geo, m) => {
  const o = new THREE.Mesh(geo, m);
  g.add(o);
  return o;
};
function wheelsOf(car, g, K, zs, track) {
  const tyre = new THREE.CylinderGeometry(K.wr, K.wr, 0.2, 14).rotateZ(Math.PI / 2),
    hub = new THREE.CylinderGeometry(K.wr * 0.56, K.wr * 0.56, 0.21, 10).rotateZ(Math.PI / 2),
    arch = new THREE.CircleGeometry(K.wr + 0.07, 14, 0, Math.PI);
  for (const z of zs)
    for (const s of [-1, 1]) {
      const w = new THREE.Group();
      w.add(new THREE.Mesh(tyre, darkM), new THREE.Mesh(hub, chromeM));
      w.position.set(s * track, K.wr, z);
      g.add(w);
      car.wheels.push(w);
      const a = new THREE.Mesh(arch, darkM);
      a.rotation.y = (s * Math.PI) / 2;
      a.position.set(s * (track + 0.105), K.wr - 0.01, z);
      g.add(a);
    }
}
function driverOf(g, x, y, z) {
  // someone at the wheel, seen through the glass
  const geo = mergeGeometries([
    colour(xform(new THREE.SphereGeometry(0.11, 8, 6), x, y + 0.36, z), '#d9b8a0'),
    colour(boxG(0.4, 0.42, 0.2, x, y + 0.04, z - 0.02), '#2a2c33'),
    colour(boxG(0.44, 0.5, 0.1, x, y + 0.02, z - 0.16), '#17171a'),
  ]);
  mesh(g, geo, skinM);
}
function colour(geo, hex) {
  const c = new THREE.Color(hex),
    n = geo.attributes.position.count,
    a = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    a[i * 3] = c.r;
    a[i * 3 + 1] = c.g;
    a[i * 3 + 2] = c.b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(a, 3));
  return geo;
}
let plateN = 0;
export function buildCar(kind, color, o = {}) {
  mats();
  const g = new THREE.Group(),
    body = lit(new THREE.MeshStandardMaterial({ color, roughness: 0.36, metalness: 0.3 }));
  const car = { g, kind, wheels: [], len: 4.3, wid: 1.7, halos: [], tails: [], body, signParts: [] };
  const headM = new THREE.MeshBasicMaterial({ color: '#3a3a36' }),
    tailM = new THREE.MeshBasicMaterial({ color: '#3a0a0a' }),
    amber = new THREE.MeshBasicMaterial({ color: '#7a4a10' });
  car.headM = headM;
  car.tailM = tailM;
  const plates = plateTex[plateN++ % plateTex.length],
    plate = (z, rear) => {
      const p = mesh(
        g,
        new THREE.PlaneGeometry(0.5, 0.12),
        new THREE.MeshBasicMaterial({ map: plates[rear ? 1 : 0], color: new THREE.Color(0.6, 0.6, 0.6) }),
      );
      p.position.set(0, 0.46, z);
      if (rear) p.rotation.y = Math.PI;
    };
  let hx = 0.56,
    hy = 0.66,
    front,
    rear;
  if (kind === 'bus') {
    car.len = 9.6;
    car.wid = 2.5;
    front = 4.8;
    rear = -4.8;
    hx = 0.92;
    hy = 0.78;
    const cream = lit(new THREE.MeshStandardMaterial({ color: '#d9d2b8', roughness: 0.5 })),
      run = [
        [-4.8, 1.16, 2.3],
        [-4.6, 1.25, 2.3],
        [4.5, 1.25, 2.3],
        [4.8, 1.14, 2.3],
      ];
    mesh(g, loft(run, 0.36, 0.05), body);
    mesh(
      g,
      loft(
        run.map(([z, hw]) => [z, hw, 4.32]),
        2.3,
        0.22,
      ),
      cream,
    );
    mesh(g, boxG(2.54, 0.12, 9.5, 0, 2.3, 0), body);
    const lw = new THREE.MeshBasicMaterial({ color: new THREE.Color(0.2, 0.2, 0.16) });
    car.inside = lw;
    // decks of windows: the lit saloon behind, glass in front, pillars between
    for (const [y0, y1, z0, z1] of [
      [1.3, 2.1, -4.4, 3.6],
      [2.95, 3.72, -4.5, 4.4],
    ]) {
      for (const s of [-1, 1]) {
        const w = mesh(g, new THREE.PlaneGeometry(z1 - z0, y1 - y0), lw);
        w.rotation.y = (s * Math.PI) / 2;
        w.position.set(s * 1.262, (y0 + y1) / 2, (z0 + z1) / 2);
        mesh(
          g,
          pane([
            [s * 1.268, y0, s > 0 ? z1 : z0],
            [s * 1.268, y0, s > 0 ? z0 : z1],
            [s * 1.268, y1, s > 0 ? z0 : z1],
            [s * 1.268, y1, s > 0 ? z1 : z0],
          ]),
          glassM,
        );
        for (let z = z0; z <= z1 + 0.01; z += (z1 - z0) / 6)
          mesh(g, boxG(0.03, y1 - y0 + 0.06, 0.09, s * 1.27, (y0 + y1) / 2, z), y0 > 2.5 ? cream : body);
      }
    }
    for (const [y0, y1] of [
      [1.25, 2.1],
      [2.95, 3.72],
    ]) {
      const f = mesh(g, new THREE.PlaneGeometry(2.1, y1 - y0), lw);
      f.position.set(0, (y0 + y1) / 2, 4.802);
      mesh(
        g,
        pane([
          [-1.05, y0, 4.81],
          [1.05, y0, 4.81],
          [1.05, y1, 4.81],
          [-1.05, y1, 4.81],
        ]),
        glassM,
      );
      mesh(g, boxG(0.06, y1 - y0, 0.04, 0, (y0 + y1) / 2, 4.82), y0 > 2.5 ? cream : body);
    }
    mesh(g, boxG(0.04, 1.75, 1.0, 1.27, 1.25, 3.95), blackM); // the platform doors, nearside
    const bl = mesh(
      g,
      new THREE.PlaneGeometry(1.5, 0.36),
      new THREE.MeshBasicMaterial({
        map: textTex([o.blind || '14 QUAY ST'], { w: 256, h: 64, bg: '#111', fg: '#e8d820', font: 'plain' }),
      }),
    );
    bl.position.set(0, 2.55, 4.83);
    const side = textTex(['MERIDIAN CORPORATION TRANSPORT'], {
      w: 512,
      h: 40,
      bg: '#d9d2b8',
      fg: '#1f3f7a',
      font: 'plain',
    });
    for (const s of [-1, 1]) {
      const p = mesh(
        g,
        new THREE.PlaneGeometry(4.2, 0.3),
        new THREE.MeshBasicMaterial({ map: side, color: new THREE.Color(0.55, 0.55, 0.55) }),
      );
      p.rotation.y = (s * Math.PI) / 2;
      p.position.set(s * 1.275, 2.5, -0.5);
    }
    mesh(g, boxG(2.4, 0.22, 0.12, 0, 0.42, 4.84), blackM);
    mesh(g, boxG(2.4, 0.22, 0.12, 0, 0.42, -4.84), blackM);
    wheelsOf(car, g, { wr: 0.5 }, [3.2, -2.8], 1.1);
    for (const x of [-hx, hx]) {
      mesh(g, boxG(0.3, 0.2, 0.05, x, hy, 4.83), headM);
      mesh(g, boxG(0.18, 0.34, 0.05, x * 1.1, 1.0, -4.83), tailM);
    }
  } else {
    const K = KIND[kind] || KIND.saloon,
      C = K.cab,
      parts = [];
    car.len = K.L;
    car.wid = K.W;
    front = K.L / 2;
    rear = -K.L / 2;
    hx = K.W / 2 - 0.26;
    hy = kind === 'saloon' || kind === 'hatch' ? 0.66 : 0.82;
    parts.push(loft(K.low, 0.3));
    if (K.box)
      parts.push(
        loft(
          [
            [K.box[0], K.box[3], K.box[2]],
            [K.box[1], K.box[3], K.box[2]],
          ],
          1.0,
          0.06,
        ),
      );
    // roof and pillars: an open cabin with something inside it
    parts.push(
      loft(
        [
          [C.r1 - 0.03, C.hr + 0.02, C.roof],
          [C.f1 + 0.03, C.hr + 0.02, C.roof],
        ],
        C.roof - 0.055,
        0.05,
      ),
    );
    for (const s of [-1, 1]) {
      parts.push(beam([s * C.hb, C.belt, C.f0], [s * C.hr, C.roof - 0.03, C.f1], 0.06));
      parts.push(beam([s * C.hb, C.belt, C.r0], [s * C.hr, C.roof - 0.03, C.r1], 0.07));
      if (C.f1 - C.r1 > 0.9) {
        const zm = (C.r1 + C.f1) / 2 - 0.1;
        parts.push(beam([s * (C.hb + 0.005), C.belt, zm], [s * (C.hr + 0.005), C.roof - 0.03, zm], 0.055));
      }
    }
    if (kind === 'flatbed') {
      parts.push(boxG(1.9, 0.9, 0.06, 0, 1.45, 0.7));
      for (const s of [-1, 1]) parts.push(boxG(0.05, 0.3, 3.5, s * 0.95, 1.1, -1.05));
      parts.push(boxG(1.9, 0.3, 0.05, 0, 1.1, -2.78));
    }
    mesh(
      g,
      mergeGeometries(
        parts.map((p) => {
          const q = p.index ? p.toNonIndexed() : p;
          q.deleteAttribute('uv');
          q.computeVertexNormals();
          return q;
        }),
      ),
      body,
    );
    const gl = [
      pane([
        [-C.hb + 0.04, C.belt, C.f0 + 0.01],
        [C.hb - 0.04, C.belt, C.f0 + 0.01],
        [C.hr - 0.03, C.roof - 0.04, C.f1 + 0.01],
        [-C.hr + 0.03, C.roof - 0.04, C.f1 + 0.01],
      ]),
    ];
    if (C.r1 - C.r0 > 0.05)
      gl.push(
        pane([
          [C.hb - 0.04, C.belt, C.r0 - 0.01],
          [-C.hb + 0.04, C.belt, C.r0 - 0.01],
          [-C.hr + 0.03, C.roof - 0.04, C.r1 - 0.01],
          [C.hr - 0.03, C.roof - 0.04, C.r1 - 0.01],
        ]),
      );
    for (const s of [-1, 1]) {
      const a = [s * (C.hb + 0.006), C.belt, C.r0],
        b = [s * (C.hb + 0.006), C.belt, C.f0],
        c = [s * (C.hr + 0.006), C.roof - 0.05, C.f1],
        d = [s * (C.hr + 0.006), C.roof - 0.05, C.r1];
      gl.push(pane(s > 0 ? [b, a, d, c] : [a, b, c, d]));
    }
    const gm = mesh(g, mergeGeometries(gl), glassM);
    gm.renderOrder = 3;
    mesh(
      g,
      boxG(
        C.hb * 2 - 0.1,
        0.34,
        Math.max(0.5, C.f0 - C.r0 - 0.3),
        0,
        C.belt - 0.06,
        (C.f0 + C.r0) / 2 - 0.05,
      ),
      darkM,
    ); // seats and dash, dark
    if (o.driver) driverOf(g, -0.36 * (K.W / 1.68), C.belt + 0.02, (C.f0 + C.f1) / 2 - 0.55);
    const bm = K.chrome ? chromeM : blackM;
    mesh(g, boxG(K.W + 0.04, 0.13, 0.14, 0, 0.42, front - 0.02), bm);
    mesh(g, boxG(K.W + 0.04, 0.13, 0.14, 0, 0.42, rear + 0.02), bm);
    mesh(g, boxG(K.W - 0.62, 0.16, 0.04, 0, hy, front + 0.012), blackM); // grille
    for (const s of [-1, 1]) {
      mesh(g, boxG(0.26, 0.15, 0.05, s * hx, hy, front + 0.015), headM);
      mesh(g, boxG(0.1, 0.1, 0.05, s * (hx + 0.2), hy - 0.01, front + 0.005), amber);
      mesh(g, boxG(0.3, 0.13, 0.05, s * (hx - 0.02), hy + 0.06, rear - 0.015), tailM);
      mesh(g, boxG(0.02, 0.04, K.L * 0.5, s * (K.W / 2 + 0.008), 0.62, 0), blackM);
      mesh(g, boxG(0.05, 0.07, 0.12, s * (C.hb + 0.07), C.belt + 0.07, C.f0 - 0.12), blackM);
    }
    plate(front + 0.06, false);
    plate(rear - 0.06, true);
    wheelsOf(car, g, K, [K.wb, -K.wb], K.W / 2 - 0.13);
    if (o.police || o.ambulance) {
      // the one-shot (20 Nov): a patrol car's or an ambulance's blue lamp, and a band along the side
      const blue = new THREE.MeshBasicMaterial({ color: new THREE.Color(0.2, 0.5, 2.4) });
      car.lamp = blue;
      mesh(g, boxG(0.3, 0.16, 0.2, 0, C.roof + 0.09, (C.r1 + C.f1) / 2 + 0.1), blue);
      const band = new THREE.MeshBasicMaterial({ color: o.police ? '#c9461e' : '#b02a2a' });
      for (const s of [-1, 1]) mesh(g, boxG(0.02, 0.1, K.L * 0.62, s * (K.W / 2 + 0.012), 0.72, 0), band);
    }
    if (o.cab) {
      // the roof sign of a Mickey's cab
      const st = signTex("MICKEY'S", '', '#e8d24a', '#14182a', 'slab', 256, 64),
        sm = new THREE.MeshBasicMaterial({ map: st, color: new THREE.Color(0.5, 0.5, 0.5) });
      car.sign = sm;
      car.signParts.push(mesh(g, boxG(0.62, 0.17, 0.2, 0, C.roof + 0.1, (C.r1 + C.f1) / 2 + 0.1), blackM));
      for (const s of [-1, 1]) {
        const p = mesh(g, new THREE.PlaneGeometry(0.58, 0.14), sm);
        car.signParts.push(p);
        p.position.set(0, C.roof + 0.1, (C.r1 + C.f1) / 2 + 0.1 + s * 0.102);
        if (s < 0) p.rotation.y = Math.PI;
      }
      const dt = textTex(["MICKEY'S CARS", 'MERIDIAN 51296'], {
        w: 256,
        h: 64,
        bg: '#e8e2cc',
        fg: '#14182a',
        font: 'plain',
      });
      for (const s of [-1, 1]) {
        const p = mesh(
          g,
          new THREE.PlaneGeometry(0.62, 0.17),
          new THREE.MeshBasicMaterial({
            map: dt,
            color: new THREE.Color(0.55, 0.55, 0.55),
            polygonOffset: true,
            polygonOffsetFactor: -2,
            polygonOffsetUnits: -2,
          }),
        );
        p.rotation.y = (s * Math.PI) / 2;
        p.position.set(s * (K.W / 2 + 0.004), 0.68, -0.25);
      }
    }
    if (o.lettering && K.box) {
      const lt = textTex(o.lettering, { w: 512, h: 128, bg: '#d8d4c8', fg: '#1f3a5a', font: 'slab' });
      for (const s of [-1, 1]) {
        const p = mesh(
          g,
          new THREE.PlaneGeometry(2.6, 0.62),
          new THREE.MeshBasicMaterial({ map: lt, color: new THREE.Color(0.6, 0.6, 0.6) }),
        );
        p.rotation.y = (s * Math.PI) / 2;
        p.position.set(s * (K.box[3] + 0.006), 1.5, -0.6);
      }
    }
  }
  // lamps: halos, a pool thrown on the road, tail glow; real beams for the car Tom drives
  for (const x of [-1, 1]) {
    const s = new THREE.Sprite(haloM);
    s.position.set(x * hx, hy, front + 0.12);
    s.scale.setScalar(1.25);
    s.visible = false;
    g.add(s);
    car.halos.push(s);
    const t = new THREE.Sprite(tailHaloM);
    t.position.set(x * hx, hy + 0.1, rear - 0.1);
    t.scale.setScalar(0.55);
    t.visible = false;
    g.add(t);
    car.tails.push(t);
  }
  const pool = new THREE.Mesh(new THREE.PlaneGeometry(5.5, 11).rotateX(-Math.PI / 2), poolM);
  pool.position.set(0, 0.03, front + 5.2);
  pool.visible = false;
  pool.layers.set(1);
  g.add(pool);
  car.pool = pool;
  if (o.beams) {
    car.beams = [];
    for (const x of [-0.5, 0.5]) {
      const sp = new THREE.SpotLight(0xfff0d0, 0, 34, 0.42, 0.7, 1.4);
      sp.position.set(x, 0.75, car.len / 2);
      sp.target.position.set(x * 1.5, 0.1, car.len / 2 + 14);
      g.add(sp, sp.target);
      car.beams.push(sp);
    }
  }
  return car;
}
export function carLights(car, on, brake) {
  car.headM.color.setRGB(...(on ? [4, 3.6, 2.6] : [0.22, 0.22, 0.2]));
  car.tailM.color.setRGB(...(brake ? [4, 0.3, 0.2] : on ? [1.3, 0.1, 0.08] : [0.22, 0.04, 0.04]));
  for (const h of car.halos) h.visible = on;
  for (const t of car.tails) {
    t.visible = on || !!brake;
    t.scale.setScalar(brake ? 0.95 : 0.55);
  }
  if (car.pool) car.pool.visible = on && !car.beams;
  if (car.beams) for (const b of car.beams) b.intensity = on ? 70 : 0;
  if (car.inside) car.inside.color.setRGB(...(on ? [1.9, 1.7, 1.1] : [0.2, 0.2, 0.16]));
  if (car.sign) car.sign.color.setScalar(on ? 2.6 : 0.5);
}

// The one-shot (20 Nov, A24): a car's paint and roof sign can change (Shaun Hewson's shed; a parked car he has taken).
export function restyleCar(car, color, sign) {
  if (color && car.body) car.body.color.set(color);
  for (const p of car.signParts || []) p.visible = !!sign;
}
