// The art pass that is not people or cars: Poly Haven surfaces (CC0), the quay edge and what the street looks onto,
// the far bank and the rooflines beyond the map, mist on the water, light spilled at night, litter, perched gulls, steam.
import { THREE, lit, U, mat, canvas, tex, glowTex, boxG, xform, wallBox, Batch } from './core.js';
import { BLD } from '../map.js';

const X = {
  pools: null,
  shopPools: null,
  sprites: [],
  sil: [],
  far: null,
  mist: [],
  litter: null,
  lit: [],
  steam: [],
  t: 0,
};
const hash = (x, z) => {
  const s = Math.sin(x * 12.9898 + z * 78.233) * 43758.5453;
  return s - Math.floor(s);
};
export const hash2 = hash;
const TL = new THREE.TextureLoader();
function ph(name) {
  const d = TL.load('tx_' + name + '_d.jpg'),
    n = TL.load('tx_' + name + '_n.jpg');
  d.colorSpace = THREE.SRGBColorSpace;
  for (const t of [d, n]) {
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.anisotropy = 8;
  }
  return { map: d, normalMap: n };
}
// mortar depth: a normal map read off the painted brick itself
function normalFrom(tx, k) {
  const src = tx.image,
    w = src.width,
    h = src.height,
    c = canvas(w, h),
    x = c.getContext('2d'),
    d = src.getContext('2d').getImageData(0, 0, w, h).data,
    o = x.createImageData(w, h),
    L = (i, j) => {
      const p = (((j + h) % h) * w + ((i + w) % w)) * 4;
      return (d[p] * 0.3 + d[p + 1] * 0.59 + d[p + 2] * 0.11) / 255;
    };
  for (let j = 0; j < h; j++)
    for (let i = 0; i < w; i++) {
      const dx = (L(i + 1, j) - L(i - 1, j)) * k,
        dy = (L(i, j + 1) - L(i, j - 1)) * k,
        l = 1 / Math.hypot(dx, dy, 1),
        p = (j * w + i) * 4;
      o.data[p] = (-dx * l * 0.5 + 0.5) * 255;
      o.data[p + 1] = (dy * l * 0.5 + 0.5) * 255;
      o.data[p + 2] = (l * 0.5 + 0.5) * 255;
      o.data[p + 3] = 255;
    }
  x.putImageData(o, 0, 0);
  const t = tex(c, true, false);
  t.repeat.copy(tx.repeat);
  return t;
}
export function extraMaterials(M) {
  const road = ph('road'),
    plaza = ph('plaza'),
    wood = ph('wood'),
    plaster = ph('plaster'),
    stone = ph('stone');
  Object.assign(M.setts, road);
  M.setts.normalScale = new THREE.Vector2(1.3, 1.3);
  M.setts.color.setScalar(1.55); // setts on the quay, the yards and the back lanes
  Object.assign(M.planks, wood);
  M.planks.color.setScalar(0.8);
  Object.assign(M.stone, stone);
  M.stone.color.set('#a39a8c'); // dressed stone, sooted: chapel, harbour office, bank, quay walls
  M.kerb = lit(
    new THREE.MeshLambertMaterial(
      Object.assign({ vertexColors: true, color: new THREE.Color(0.8, 0.8, 0.82) }, plaza),
    ),
  );
  M.wood = mat(wood);
  M.render = mat(Object.assign({ color: new THREE.Color(0.86, 0.85, 0.8) }, plaster));
  for (const k of ['soot', 'red', 'yellow']) {
    try {
      M[k].normalMap = normalFrom(M[k].map, 2.2);
      M[k].normalScale = new THREE.Vector2(0.9, 0.9);
    } catch (e) {
      /* keep it flat */
    }
  }
  for (const b of BLD)
    if (['caff', 'boarding', 'tearoom', 'coin', 'h3', 'h7'].includes(b.id)) b.brick = 'render';
  // soot under sills and copings, damp at the foot of walls: one streaked gradient
  {
    const c = canvas(128, 128),
      x = c.getContext('2d');
    for (let i = 0; i < 128; i += 2) {
      const len = 40 + hash(i, 1) * 88,
        g = x.createLinearGradient(0, 0, 0, len);
      g.addColorStop(0, `rgba(12,10,9,${0.34 + hash(i, 2) * 0.3})`);
      g.addColorStop(1, 'rgba(12,10,9,0)');
      x.fillStyle = g;
      x.fillRect(i, 0, 2, len);
    }
    const t = tex(c, false);
    M.streak = new THREE.MeshBasicMaterial({
      map: t,
      transparent: true,
      depthWrite: false,
      polygonOffset: true,
      polygonOffsetFactor: -3,
      polygonOffsetUnits: -3,
      color: new THREE.Color(0.5, 0.48, 0.46),
    });
  }
  // door numbers and the posters on the empty unit share one sheet
  {
    const c = canvas(512, 512),
      x = c.getContext('2d');
    x.fillStyle = '#16140f';
    x.fillRect(0, 0, 512, 256);
    x.fillStyle = '#d8cf9a';
    x.font = 'bold 44px Georgia, serif';
    x.textAlign = 'center';
    x.textBaseline = 'middle';
    for (let n = 0; n < 32; n++) x.fillText(String(n + 1), (n % 8) * 64 + 32, Math.floor(n / 8) * 64 + 34);
    const P = [
      ['#c8b23a', '#1a1a1a', 'TO LET', 'AGAR & CO', 'Meridian 40417'],
      ['#d8d2c0', '#8a1c1c', 'CLOSING', 'DOWN', 'everything must go'],
      ['#2a4a7a', '#f0e8d0', 'SPEEDWAY', 'SATURDAY', 'Humber Road 7.30'],
      ['#e8e2d0', '#1a3a2a', 'JUMBLE', 'SALE', "St Hilda's hall"],
    ];
    P.forEach(([bg, fg, a, b2, s], i) => {
      const ox = i * 128;
      x.fillStyle = bg;
      x.fillRect(ox + 4, 260, 120, 248);
      x.fillStyle = fg;
      x.font = 'bold 30px Georgia, serif';
      x.fillText(a, ox + 64, 320);
      x.fillText(b2, ox + 64, 362);
      x.font = '13px Georgia, serif';
      x.fillText(s, ox + 64, 420);
      for (let k = 0; k < 60; k++) {
        x.fillStyle = `rgba(40,30,20,${hash(i, k) * 0.2})`;
        x.fillRect(ox + 4 + hash(k, i) * 116, 260 + hash(k, 7) * 240, 6, 3);
      }
    });
    M.sheet = mat({ map: tex(c, false) });
  }
}
export const numUV = (n) => {
  const k = n % 32,
    u = (k % 8) / 8,
    v = 1 - Math.floor(k / 8) / 8;
  return [u, v - 0.125, u + 0.125, v];
};
export const posterUV = (i) => [(i % 4) / 4 + 0.01, 0.01, (i % 4) / 4 + 0.24, 0.49];
export function aerial(bt, M, x, y, z) {
  bt.add(M.flat, boxG(0.04, 1.7, 0.04, x + 0.22, y + 2.3, z), '#8a8a88');
  bt.add(M.flat, boxG(0.03, 0.03, 1.15, x + 0.22, y + 3.05, z), '#8a8a88');
  for (let i = 0; i < 6; i++)
    bt.add(M.flat, boxG(0.5 - i * 0.04, 0.02, 0.02, x + 0.22, y + 3.05, z - 0.5 + i * 0.2), '#8a8a88');
}

function skyline(kind, seed) {
  // a strip of town cut out against the sky
  const c = canvas(2048, 256),
    x = c.getContext('2d');
  let px = 0,
    k = 0;
  x.fillStyle = '#fff';
  const r = () => hash(seed, ++k);
  const stack = (cx, h, w = 10) => {
    x.fillRect(cx - w / 2, 256 - h, w, h);
    x.fillRect(cx - w / 2 - 2, 256 - h, w + 4, 5);
  };
  if (kind === 'bank') {
    x.fillRect(0, 236, 2048, 20);
    while (px < 2048) {
      const w = 30 + r() * 120,
        h = 8 + r() * 26;
      if (r() < 0.6) x.fillRect(px, 236 - h, w, h);
      if (r() < 0.12) stack(px + w / 2, 70 + r() * 70, 7);
      if (r() < 0.07) {
        x.beginPath();
        x.moveTo(px, 236);
        x.quadraticCurveTo(px + 14, 190, px + 10, 150);
        x.lineTo(px + 44, 150);
        x.quadraticCurveTo(px + 40, 190, px + 54, 236);
        x.fill();
      }
      px += w + r() * 40;
    }
  } else
    while (px < 2048) {
      const t = r();
      if (kind === 'docks' && t < 0.14) {
        const h = 120 + r() * 60;
        x.fillRect(px + 20, 256 - h, 6, h);
        x.fillRect(px + 44, 256 - h, 6, h);
        x.fillRect(px + 14, 256 - h - 12, 44, 14);
        x.save();
        x.translate(px + 36, 256 - h - 6);
        x.rotate(-0.5 - r() * 0.3);
        x.fillRect(0, -3, 110, 6);
        x.restore();
        for (let y = 256 - h; y < 250; y += 18) {
          x.fillRect(px + 20, y, 30, 2);
        }
        px += 90;
      } else if (t < 0.05) {
        const w = 96,
          h = 96;
        x.fillRect(px, 256 - h * 0.7, w, h * 0.7);
        for (let i = 0; i <= 6; i++) x.fillRect(px + (i * w) / 6 - 1.5, 256 - h, 3, h);
        x.fillRect(px - 2, 256 - h, w + 4, 3);
        x.fillRect(px - 2, 256 - h * 0.85, w + 4, 2);
        px += w + 14;
      } // a gasholder
      else if (t < 0.09) {
        x.fillRect(px, 196, 54, 60);
        x.beginPath();
        x.moveTo(px + 10, 196);
        x.lineTo(px + 22, 96);
        x.lineTo(px + 34, 196);
        x.fill();
        px += 60;
      } // a spire
      else if (t < 0.16) {
        stack(px + 8, 110 + r() * 90, 9);
        x.fillRect(px, 216, 70, 40);
        px += 76;
      } else if (t < 0.3) {
        const w = 70 + r() * 80,
          h = 50 + r() * 50;
        x.fillRect(px, 256 - h, w, h);
        for (let i = 0; i < w - 20; i += 26) {
          x.beginPath();
          x.moveTo(px + i, 256 - h);
          x.lineTo(px + i + 10, 256 - h - 12);
          x.lineTo(px + i + 26, 256 - h);
          x.fill();
        }
        px += w + 6;
      } // a works with a north-light roof
      else {
        const n = 3 + Math.floor(r() * 6),
          w = 22,
          h = 34 + r() * 22;
        for (let i = 0; i < n; i++) {
          x.fillRect(px, 256 - h, w, h);
          x.beginPath();
          x.moveTo(px - 1, 256 - h);
          x.lineTo(px + w / 2, 256 - h - 13);
          x.lineTo(px + w + 1, 256 - h);
          x.fill();
          x.fillRect(px + 2, 256 - h - 20, 6, 14);
          x.fillRect(px + 2.5, 256 - h - 24, 2, 5);
          x.fillRect(px + 5.5, 256 - h - 24, 2, 5);
          if (r() < 0.4) {
            x.fillRect(px + 14, 256 - h - 30, 1, 18);
            x.fillRect(px + 10, 256 - h - 30, 9, 1);
          }
          px += w;
        }
        px += 4 + r() * 10;
      }
    }
  const t = tex(c, false);
  t.wrapS = THREE.RepeatWrapping;
  return t;
}
export function buildExtras(root, M, town) {
  const bt = new Batch(),
    E = new THREE.Group();
  E.name = 'extras';
  root.add(E);
  // ---- the quay edge: granite coping, railings, bollards, kerbs
  bt.add(M.kerb, wallBox(330, 0.26, 1.0, 15, 0.03, 62.1, 1.6), '#d0d0d0');
  for (const sx of [-1, 1])
    for (const [z0, z1] of [
      [-90, -24],
      [-12.5, 11],
      [15, 43.4],
    ])
      bt.add(M.kerb, wallBox(0.2, 0.19, z1 - z0, sx * 5.0, 0.055, (z0 + z1) / 2, 1.4), '#c4c4c4');
  const gaps = [
      [-64, -46],
      [52, 76],
      [116, 128],
    ],
    open = (x) => gaps.some(([a, b]) => x > a && x < b);
  for (let x = -128; x <= 158; x += 2) {
    if (open(x) || open(x + 2)) continue;
    bt.add(M.flat, boxG(0.05, 1.05, 0.05, x, 0.68, 62.45), '#141414');
    for (const y of [1.18, 0.74]) bt.add(M.flat, boxG(2, 0.045, 0.045, x + 1, y, 62.45), '#141414');
  }
  for (let x = -124; x <= 156; x += 14) {
    if (
      Math.abs(x - 20) < 2 ||
      Math.abs(x) < 2 ||
      Math.abs(x + 30) < 2 ||
      Math.abs(x - 110) < 2 ||
      Math.abs(x - 140) < 2
    )
      continue;
    bt.add(M.flat, xform(new THREE.CylinderGeometry(0.17, 0.24, 0.62, 9), x, 0.46, 61.75), '#17171a');
    bt.add(
      M.flat,
      xform(new THREE.SphereGeometry(0.25, 9, 5, 0, Math.PI * 2, 0, 1.6), x, 0.74, 61.75, 0, 0, 0, 1, 0.5, 1),
      '#17171a',
    );
  }
  // ---- fish boxes, net piles and timbers by the dock
  const boxes = (x, z, n, a) => {
    for (let i = 0; i < n; i++) {
      const col = i % 3,
        lay = Math.floor(i / 3),
        plastic = hash(x + i, z) < 0.3;
      bt.add(
        plastic ? M.flat : M.wood,
        xform(
          new THREE.BoxGeometry(0.78, 0.26, 0.5),
          x + Math.cos(a) * col * 0.84,
          0.3 + lay * 0.27,
          z - Math.sin(a) * col * 0.84 + (lay % 2) * 0.06,
          a + (hash(i, x) - 0.5) * 0.12,
        ),
        plastic ? '#c85a1a' : '#b8a888',
      );
    }
  };
  boxes(48.2, 55.6, 11, 0.1);
  boxes(52.6, 59.6, 8, 1.4);
  boxes(71.2, 57.4, 12, 0.3);
  boxes(101.5, 56.2, 9, 0);
  boxes(63.2, 68.4, 6, 1.57);
  boxes(-48.5, 58.8, 5, 0.4);
  const nets = (x, z, r) => {
    const g = new THREE.SphereGeometry(r, 9, 6),
      p = g.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const k = 1 + (hash(p.getX(i) * 9 + x, p.getZ(i) * 7) - 0.5) * 0.35;
      p.setXYZ(i, p.getX(i) * k, Math.max(0, p.getY(i) * 0.42 * k), p.getZ(i) * k);
    }
    g.computeVertexNormals();
    bt.add(M.flat, xform(g, x, 0.13, z), ['#2f4a44', '#3a4a5a', '#4a4030'][Math.floor(hash(x, z) * 3)]);
    for (let i = 0; i < 7; i++)
      bt.add(
        M.flat,
        xform(
          new THREE.SphereGeometry(0.1, 6, 4),
          x + (hash(i, x) - 0.5) * r * 1.5,
          0.2 + hash(i, z) * r * 0.25,
          z + (hash(x, i) - 0.5) * r * 1.5,
        ),
        i % 2 ? '#d8601a' : '#e8e0c8',
      );
  };
  nets(45.8, 58.8, 1.25);
  nets(42.2, 60.6, 1.0);
  nets(104.5, 59.4, 1.3);
  nets(67.4, 82.8, 0.9);
  nets(-45.5, 60.6, 0.9);
  for (let x = 58; x <= 72; x += 2.4)
    bt.add(M.wood, xform(new THREE.BoxGeometry(0.3, 0.3, 3.4), x, -0.2, 63.4), '#6a5a48'); // fendering under the pier head
  // ---- warehouse row: loading doors, hoist beams and numbers on the ends that face the quay
  for (const b of BLD)
    if (b.k === 'ware') {
      const cx = (b.x0 + b.x1) / 2,
        z = b.z1 + 0.04,
        n = Math.round((b.x0 - 36) / 24) + 1;
      for (const y of [0.1, 4.0, 7.6])
        bt.add(
          M.wood,
          xform(new THREE.BoxGeometry(3.2, y ? 2.6 : 3.4, 0.12), cx, y + (y ? 1.3 : 1.7), z),
          b.burnt ? '#2a2420' : '#8a7a68',
        );
      bt.add(M.flat, boxG(0.3, 0.3, 2.6, cx, 11.0, z + 1.2), '#1c1a18');
      bt.add(M.flat, boxG(0.06, 1.4, 0.06, cx, 10.2, z + 2.3), '#1c1a18');
      if (!b.burnt)
        bt.add(M.sheet, xform(new THREE.PlaneGeometry(1.7, 1.7), b.x0 + 2.6, 9.3, z + 0.03), '#ffffff');
      const g = bt.m.get(M.sheet);
      if (!b.burnt && g) {
        const q = g[g.length - 1],
          uv = q.attributes.uv,
          r = numUV(n - 1),
          a = [r[0], r[3], r[0], r[1], r[2], r[3], r[0], r[1], r[2], r[1], r[2], r[3]];
        for (let i = 0; i < 6; i++) uv.setXY(i, a[i * 2], a[i * 2 + 1]);
      }
    }
  // ---- gulls on the quay roofs and the rail
  const gull = (x, y, z, a) => {
    bt.add(
      M.flat,
      xform(new THREE.SphereGeometry(0.13, 7, 5), x, y + 0.14, z, a, 0, 0, 0.75, 0.8, 1.6),
      '#e4e2dc',
    );
    bt.add(
      M.flat,
      xform(new THREE.SphereGeometry(0.07, 6, 4), x + Math.sin(a) * 0.17, y + 0.26, z + Math.cos(a) * 0.17),
      '#f0eee8',
    );
    bt.add(
      M.flat,
      xform(
        new THREE.BoxGeometry(0.02, 0.02, 0.07),
        x + Math.sin(a) * 0.25,
        y + 0.25,
        z + Math.cos(a) * 0.25,
        a,
      ),
      '#d8a020',
    );
    bt.add(
      M.flat,
      xform(
        new THREE.BoxGeometry(0.1, 0.06, 0.24),
        x - Math.sin(a) * 0.1,
        y + 0.17,
        z - Math.cos(a) * 0.1,
        a,
      ),
      '#8a8f96',
    );
  };
  for (const [x, y, z] of [
    [80, 5.2, 56],
    [83.5, 5.2, 58.2],
    [91, 5.2, 55.9],
    [97, 5.2, 60.9],
    [-63, 2.95, 56],
    [-60.4, 2.95, 59.8],
    [31, 1.2, 62.45],
    [37, 1.2, 62.45],
    [-9, 1.2, 62.45],
    [86, 1.2, 62.45],
    [20, 0.9, 61.75],
    [-30, 0.9, 61.75],
    [8, 7.9, 43.5],
    [61, 0.3, 97],
  ])
    gull(x, y, z, hash(x, z) * 6.28);
  bt.build(E, { cull: false });
  // ---- riding lights on the boats, glows for the phone box, bus shelter, ferry shelter
  const halo = new THREE.SpriteMaterial({
    map: glowTex(),
    color: new THREE.Color(1, 0.86, 0.6),
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    fog: false,
  });
  X.halo = halo;
  const glow = (parent, x, y, z, s, col) => {
    const m = col ? halo.clone() : halo;
    if (col) {
      m.color.set(col);
      X.lit.push(m);
    }
    const sp = new THREE.Sprite(m);
    sp.position.set(x, y, z);
    sp.scale.setScalar(s);
    parent.add(sp);
    X.sprites.push(sp);
    return sp;
  };
  town.boats.forEach((b, i) => {
    glow(b, 0, 7.9, 2, 1.6, i === 1 ? '#ff3a20' : '#d8ffd0');
    glow(b, 0, 3.6, -3, 1.3);
  });
  if (town.ferry) {
    glow(town.ferry, 0, 7.6, 2, 2.2);
    for (let z = -8; z <= 5; z += 3.2) glow(town.ferry, 3.1, 3.4, z, 1.5);
  }
  glow(E, 7.3, 2.05, -13.2, 2.4);
  glow(E, -7.3, 2.1, 20, 2.2, '#d8e4ff');
  glow(E, -42.4, 2.3, 56.6, 2.6);
  glow(E, -63, 2.4, 58, 2.2);
  glow(E, 8.6, 3.3, -6.8, 2.4, '#ff5a30');
  // pools of light on the ground: additive, never part of the rule that says who can be seen
  const mkPools = (list) => {
    const im = new THREE.InstancedMesh(
        new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2),
        new THREE.MeshBasicMaterial({
          map: glowTex(),
          blending: THREE.AdditiveBlending,
          depthWrite: false,
          transparent: true,
          fog: false,
          polygonOffset: true,
          polygonOffsetFactor: -5,
          polygonOffsetUnits: -5,
        }),
        list.length,
      ),
      d = new THREE.Object3D(),
      c = new THREE.Color();
    list.forEach(([x, z, sx, sz, col], i) => {
      d.position.set(x, 0.16, z);
      d.scale.set(sx, 1, sz);
      d.updateMatrix();
      im.setMatrixAt(i, d.matrix);
      im.setColorAt(i, c.set(col));
    });
    im.layers.set(1);
    im.frustumCulled = false;
    E.add(im);
    return im;
  };
  X.pools = mkPools([
    [7.3, -13.2, 5, 5, '#6a5030'],
    [-6.6, 20, 6, 5, '#3a4050'],
    [-42.4, 56.6, 7, 6, '#6a5030'],
    [-63, 58, 6, 6, '#6a5030'],
    [-55, 66, 9, 14, '#3a3020'],
  ]);
  const sp = [];
  for (const b of BLD)
    if (b.k === 'shop' && !b.shut && !b.tolet) {
      const w = b.face === 'W' || b.face === 'E' ? b.z1 - b.z0 : b.x1 - b.x0,
        cx = (b.x0 + b.x1) / 2,
        cz = (b.z0 + b.z1) / 2,
        o = 2.3;
      if (b.face === 'W') sp.push([b.x0 - o, cz, 6, w + 2, '#5a4426']);
      else if (b.face === 'E') sp.push([b.x1 + o, cz, 6, w + 2, '#5a4426']);
      else if (b.face === 'S') sp.push([cx, b.z1 + o, w + 2, 6, '#5a4426']);
      else sp.push([cx, b.z0 - o, w + 2, 6, '#5a4426']);
    }
  if (sp.length) X.shopPools = mkPools(sp);
  // ---- what the street looks onto: the far bank with its lights, and rooflines beyond the edges of the map
  const sil = (kind, seed, w, h, x, y, z, ry, k, rep = 1) => {
    const t = skyline(kind, seed);
    t.repeat.x = rep;
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry(w, h),
      new THREE.MeshBasicMaterial({ map: t, transparent: true, alphaTest: 0.5, fog: false }),
    );
    m.position.set(x, y, z);
    m.rotation.y = ry;
    m.userData.k = k;
    m.renderOrder = -5;
    m.frustumCulled = false;
    E.add(m);
    X.sil.push(m);
  };
  sil('bank', 3, 1800, 64, 0, 27, 400, Math.PI, 0.3, 1.5);
  sil('docks', 5, 900, 60, 120, 25, 330, Math.PI, 0.2, 1);
  sil('town', 7, 620, 62, 20, 27, -268, 0, 0.5);
  sil('town', 11, 520, 58, -182, 25, -70, Math.PI / 2, 0.5);
  sil('docks', 13, 520, 60, 214, 26, -50, -Math.PI / 2, 0.5);
  sil('town', 17, 900, 80, 20, 36, -330, 0, 0.25, 1.5);
  {
    const n = 190,
      p = new Float32Array(n * 3),
      c = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      p[i * 3] = (hash(i, 3) - 0.5) * 1500;
      p[i * 3 + 1] = 3 + hash(i, 5) * hash(i, 6) * 26;
      p[i * 3 + 2] = 392 - hash(i, 9) * 60;
      const t = hash(i, 11);
      c.set(t < 0.7 ? [1, 0.55, 0.16] : t < 0.9 ? [1, 0.95, 0.8] : [1, 0.15, 0.1], i * 3);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(p, 3));
    g.setAttribute('color', new THREE.BufferAttribute(c, 3));
    X.far = new THREE.Points(
      g,
      new THREE.PointsMaterial({
        size: 2.6,
        sizeAttenuation: false,
        vertexColors: true,
        transparent: true,
        opacity: 0,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        fog: false,
      }),
    );
    X.far.frustumCulled = false;
    E.add(X.far);
  }
  // ---- harbour mist lying on the water
  const mm = new THREE.ShaderMaterial({
    transparent: true,
    depthWrite: false,
    uniforms: { tNoise: U.tNoise, uTime: U.uTime, cFog: { value: new THREE.Color() }, uAmt: { value: 0.5 } },
    vertexShader:
      'varying vec3 vW; varying vec2 vUv; void main(){ vUv = uv; vec4 w = modelMatrix * vec4(position,1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }',
    fragmentShader:
      'uniform sampler2D tNoise; uniform float uTime; uniform vec3 cFog; uniform float uAmt; varying vec3 vW; varying vec2 vUv; void main(){ float n = texture2D(tNoise, vW.xz * 0.006 + vec2(uTime * 0.004, 0.0)).r * 0.6 + texture2D(tNoise, vW.xz * 0.017 - vec2(uTime * 0.007, uTime * 0.002)).g * 0.4; float e = smoothstep(0.0, 0.25, vUv.y) * smoothstep(1.0, 0.6, vUv.y) * smoothstep(0.0, 0.1, vUv.x) * smoothstep(1.0, 0.9, vUv.x); gl_FragColor = vec4(cFog, smoothstep(0.32, 0.75, n) * e * uAmt); }',
  });
  for (const [z, y, d] of [
    [96, 0.5, 60],
    [150, 1.4, 120],
    [240, 3.0, 200],
  ]) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(1100, d).rotateX(-Math.PI / 2), mm);
    m.position.set(10, y, z);
    m.layers.set(1);
    m.renderOrder = 4;
    m.frustumCulled = false;
    E.add(m);
    X.mist.push(m);
  }
  X.mistM = mm;
  // ---- litter that drifts when the wind gets up
  {
    const N = 46,
      im = new THREE.InstancedMesh(
        new THREE.PlaneGeometry(0.24, 0.17),
        lit(new THREE.MeshLambertMaterial({ side: THREE.DoubleSide })),
        N,
      ),
      c = new THREE.Color(),
      L = [];
    for (let i = 0; i < N; i++) {
      const quay = i % 3 === 0;
      L.push({
        x: quay ? -40 + hash(i, 1) * 150 : (hash(i, 2) - 0.5) * 15,
        z: quay ? 46 + hash(i, 3) * 14 : -88 + hash(i, 4) * 130,
        a: hash(i, 5) * 6.28,
        r: 0,
        quay,
        k: 0.5 + hash(i, 6),
      });
      im.setColorAt(i, c.set(['#d8d2c0', '#c8c0a8', '#b03a2a', '#e8e4da', '#3a5a8a', '#d8b83a'][i % 6]));
    }
    im.layers.set(1);
    im.frustumCulled = false;
    E.add(im);
    X.litter = { im, L, d: new THREE.Object3D() };
  }
  // ---- steam off the takeaway's vent
  {
    const sm = new THREE.SpriteMaterial({
      map: glowTex(),
      color: new THREE.Color(0.8, 0.8, 0.78),
      transparent: true,
      opacity: 0.2,
      depthWrite: false,
      fog: false,
    });
    for (let i = 0; i < 7; i++) {
      const s = new THREE.Sprite(sm.clone());
      E.add(s);
      X.steam.push({ s, ph: i / 7 });
    }
  }
  X.E = E;
  return X;
}
const _c = new THREE.Color(),
  _d = new THREE.Color();
export function stepExtras(dt, t, n, w, hour, hor, fog, cam, inside) {
  if (!X.E) return;
  X.E.visible = !inside;
  if (inside) return;
  X.t += dt;
  // silhouettes sit in the haze: mostly the colour of the horizon, a little darker the nearer they are
  for (const m of X.sil) {
    const k = m.userData.k * (1 - 0.35 * w.mist);
    m.material.color.copy(hor).lerp(_d.set(n > 0.5 ? 0x030304 : 0x1a1d20), k * (1 - n * 0.35) + n * 0.5);
  }
  X.far.material.opacity = n * 0.95 * (1 - 0.6 * w.mist);
  X.mistM.uniforms.cFog.value.copy(fog).lerp(_d.set(0xffffff), 0.12 * (1 - n));
  X.mistM.uniforms.uAmt.value = 0.3 + w.mist * 0.55 + n * 0.1 + (hour < 9 ? 0.2 : 0);
  const open = hour >= 6 && hour < 23.6 ? 1 : 0.15;
  X.halo.opacity = n;
  for (const m of X.lit) m.opacity = n;
  for (const s of X.sprites) s.visible = n > 0.03;
  X.pools.material.color.setScalar(n * 1.5);
  X.pools.visible = n > 0.03;
  if (X.shopPools) {
    X.shopPools.material.color.setScalar(n * 1.25 * (hour >= 8 && hour < 23.4 ? 1 : 0));
    X.shopPools.visible = n > 0.03 && hour >= 8 && hour < 23.4;
  }
  // litter: a gust every so often, stronger in rain; pieces skitter downwind and tumble
  const gust = Math.max(0, Math.sin(X.t * 0.21) * Math.sin(X.t * 0.053 + 1.3)) * (0.6 + w.rain * 1.6),
    wx = 0.85,
    wz = 0.5,
    Lt = X.litter;
  Lt.L.forEach((p, i) => {
    const g = gust * p.k * (0.4 + 0.6 * Math.abs(Math.sin(X.t * 1.7 + i)));
    if (g > 0.05) {
      p.x += wx * g * dt * 2.6;
      p.z += wz * g * dt * 2.6;
      p.a += dt * g * 4;
      p.r += dt * g * 9;
      if (p.quay) {
        if (p.x > 112) p.x = -42;
        if (p.z > 60.8) p.z = 46;
      } else {
        if (p.x > 7.6) p.x = -7.6;
        if (p.z > 42) p.z = -88;
      }
    } else p.r *= 0.9;
    const d = Lt.d;
    d.position.set(
      p.x,
      (p.quay || Math.abs(p.x) < 5 ? 0.03 : 0.17) + Math.abs(Math.sin(p.r)) * 0.07 * Math.min(1, g * 3),
      p.z,
    );
    d.rotation.set(-Math.PI / 2 + Math.sin(p.r) * 0.9 * Math.min(1, g * 3), p.a, 0, 'YXZ');
    d.updateMatrix();
    Lt.im.setMatrixAt(i, d.matrix);
  });
  Lt.im.instanceMatrix.needsUpdate = true;
  const on = hour >= 16.4 && hour < 23.6;
  for (const q of X.steam) {
    const u = (X.t * 0.22 + q.ph) % 1;
    q.s.visible = on;
    q.s.position.set(
      8.7 + u * 1.3 * wx,
      3.9 + u * 2.6,
      -3.6 + u * 0.9 * wz + Math.sin(u * 9 + q.ph * 6) * 0.12,
    );
    q.s.scale.setScalar(0.5 + u * 1.9);
    q.s.material.opacity = 0.26 * (1 - u) * Math.min(1, u * 6) * (0.6 + 0.4 * (1 - n));
    q.s.material.color.copy(fog).lerp(_c.set(0xffffff), 0.5 - 0.3 * n);
  }
}
