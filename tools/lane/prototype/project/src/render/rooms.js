// Interiors: small sets with the fourth wall away, furnished from a few shared pieces.
import { THREE, lit, mat, Batch, boxG, xform, planeXZ, plainTex, textTex, canvas, tex } from './core.js';
import { ROOMS, FURN, TALL } from '../map.js';

export const rooms = { coat: null, lockDoor: null, suitcase: null, groups: {} };
let M = null,
  rs = 5;
const rr = () => {
  rs = (rs * 16807) % 2147483647;
  return rs / 2147483647;
};
function photoTex() {
  const c = canvas(128, 160),
    x = c.getContext('2d');
  x.fillStyle = '#1a1612';
  x.fillRect(0, 0, 128, 160);
  x.fillStyle = '#d9cfb4';
  x.fillRect(8, 8, 112, 144);
  const g = x.createLinearGradient(0, 16, 0, 144);
  g.addColorStop(0, '#b8a888');
  g.addColorStop(1, '#6a5a44');
  x.fillStyle = g;
  x.fillRect(16, 16, 96, 128);
  x.fillStyle = '#3a3024';
  x.fillRect(16, 96, 96, 48);
  x.beginPath();
  x.moveTo(20, 96);
  x.lineTo(60, 70);
  x.lineTo(108, 96);
  x.fill(); // a trawler's bow behind him
  x.fillStyle = '#2a221a';
  x.beginPath();
  x.ellipse(64, 122, 30, 26, 0, 0, 7);
  x.fill();
  x.beginPath();
  x.arc(64, 78, 15, 0, 7);
  x.fill();
  x.fillRect(44, 62, 40, 7);
  x.fillRect(58, 58, 34, 6);
  return tex(c, false);
}
export function buildRooms(scene) {
  M = {
    flat: mat({}),
    wall: mat({ map: plainTex('plaster') }),
    iron: mat({ map: plainTex('iron') }),
    wood: mat({ map: plainTex('boards') }),
    glow: new THREE.MeshBasicMaterial({ color: new THREE.Color(2.2, 1.6, 0.8) }),
    floor: {},
  };
  for (const k of ['lino', 'check', 'tile', 'boards', 'carpet']) M.floor[k] = mat({ map: plainTex(k) });
  for (const id in ROOMS) room(scene, ROOMS[id]);
}
function room(scene, r) {
  const g = new THREE.Group();
  g.position.set(r.ox, 0, r.oz);
  scene.add(g);
  rooms.groups[r.id] = g;
  const bt = new Batch(),
    w = r.w,
    d = r.d,
    hw = w / 2,
    hd = d / 2,
    solid = (FURN[r.id] = []),
    tall = (TALL[r.id] = []); // round 6: full-height partitions, so the camera can keep Tom in sight
  const B = (bw, bh, bd, x, y, z, col, m = M.flat, ry = 0) => bt.add(m, boxG(bw, bh, bd, x, y, z, ry), col);
  const S = (x, z, sw, sd) => solid.push({ x0: x - sw / 2, x1: x + sw / 2, z0: z - sd / 2, z1: z + sd / 2 });
  const W = (x, z, sw, sd) => tall.push({ x0: x - sw / 2, x1: x + sw / 2, z0: z - sd / 2, z1: z + sd / 2 });
  const sign = (x, y, sw, sh, t, z = -hd + 0.03) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(sw, sh), lit(new THREE.MeshLambertMaterial({ map: t })));
    m.position.set(x, y, z);
    g.add(m);
    return m;
  };
  const counter = (x, z, cw, cd, col = '#5a4a3a', h = 0.95) => {
    B(cw, h, cd, x, h / 2, z, col);
    B(cw + 0.1, 0.05, cd + 0.1, x, h + 0.02, z, '#2a2622');
    S(x, z, cw, cd);
  };
  const table = (x, z, col = '#8a2a22', tw = 0.85) => {
    B(tw, 0.04, tw, x, 0.74, z, col);
    B(0.08, 0.72, 0.08, x, 0.36, z, '#888');
    S(x, z, tw * 0.7, tw * 0.7);
  };
  const chair = (x, z, a = 0, col = '#3a3530') => {
    B(0.4, 0.05, 0.4, x, 0.46, z, col);
    B(0.4, 0.5, 0.05, x - Math.sin(a) * 0.19, 0.72, z - Math.cos(a) * 0.19, col, M.flat, a);
    B(0.34, 0.44, 0.34, x, 0.22, z, '#555');
  };
  const shelf = (x, sw, n = 3, z = -hd + 0.2) => {
    B(sw, 2.0, 0.3, x, 1.0, z, '#4a3c2c', M.wood);
    for (let i = 0; i < n; i++)
      for (let j = 0; j < Math.floor(sw / 0.16); j++) {
        if (rr() < 0.15) continue;
        const hh = 0.14 + rr() * 0.2;
        B(
          0.11,
          hh,
          0.12,
          x - sw / 2 + 0.1 + j * 0.16,
          0.42 + i * 0.52 + hh / 2,
          z + 0.12,
          `hsl(${Math.floor(rr() * 360)},${20 + rr() * 35}%,${22 + rr() * 30}%)`,
        );
      }
    S(x, z, sw, 0.3);
  };
  const cabinet = (x, z) => {
    B(0.5, 1.32, 0.6, x, 0.66, z, '#55614f', M.iron);
    for (let i = 0; i < 4; i++) B(0.2, 0.03, 0.02, x, 0.2 + i * 0.32, z + 0.31, '#222');
    S(x, z, 0.5, 0.6);
  };
  const armchair = (x, z, a, col = '#6a4a3a') => {
    B(0.7, 0.42, 0.7, x, 0.21, z, col, M.flat, a);
    B(0.7, 0.55, 0.16, x - Math.sin(a) * 0.3, 0.68, z - Math.cos(a) * 0.3, col, M.flat, a);
  };
  const doorB = (x, col = '#3a2a1e') => {
    B(0.95, 2.1, 0.08, x, 1.05, -hd + 0.05, col);
    B(1.1, 0.1, 0.1, x, 2.15, -hd + 0.06, '#2a2622');
    B(0.05, 0.05, 0.06, x + 0.36, 1.0, -hd + 0.12, '#b8943a');
  };
  // shell
  bt.add(M.floor[r.floor] || M.floor.lino, planeXZ(-hw, -hd, hw, hd + 0.9, 0, 1.6));
  const wc = r.wall;
  B(w + 0.3, 3.1, 0.15, 0, 1.55, -hd - 0.075, wc, M.wall);
  B(0.15, 3.1, d + 1, -hw - 0.075, 1.55, 0.35, wc, M.wall);
  B(0.15, 3.1, d + 1, hw + 0.075, 1.55, 0.35, wc, M.wall);
  B(w, 1.0, 0.02, 0, 0.5, -hd + 0.01, '#6a6250');
  B(w, 0.06, 0.03, 0, 1.02, -hd + 0.02, '#3a342a');
  B(1.4, 0.02, 0.8, r.mat[0], 0.012, r.mat[1] + 0.2, '#3a2f22');
  const k = r.k,
    sp = r.spots;
  if (k === 'office') {
    B(0.15, 3.1, 4.4, 0.5, 1.55, -1.8, wc, M.wall);
    S(0.5, -1.8, 0.15, 4.4);
    W(0.5, -1.8, 0.15, 4.4);
    B(0.15, 3.1, 1.5, 0.5, 1.55, 3.3, wc, M.wall);
    S(0.5, 3.3, 0.15, 1.5);
    W(0.5, 3.3, 0.15, 1.5);
    B(0.15, 0.6, 2.2, 0.5, 2.8, 1.5, wc, M.wall);
    counter(-3.6, -2.2, 2.4, 0.9, '#5a4a36', 0.78);
    B(0.5, 0.34, 0.3, -3.0, 0.98, -2.3, '#2f3a2c', M.iron);
    B(0.3, 0.05, 0.02, -3.0, 1.02, -2.14, '#c8a850', M.glow);
    B(0.03, 0.3, 0.03, -3.4, 0.98, -2.0, '#222');
    B(0.22, 0.1, 0.2, -4.3, 0.87, -2.1, '#d9d0b8');
    B(0.2, 0.02, 0.28, -3.9, 0.82, -1.95, '#f1c9cf');
    B(0.5, 0.45, 2.8, -6.5, 0.23, -0.3, '#4a3a2a', M.wood);
    S(-6.5, -0.3, 0.5, 2.8);
    sign(
      -5.0,
      1.95,
      1.7,
      1.15,
      textTex(['MERIDIAN', '& DISTRICT', 'street plan'], {
        w: 256,
        h: 170,
        bg: '#d9d2b4',
        fg: '#3a4a3a',
        font: 'serif',
      }),
    );
    sign(-1.2, 1.85, 0.5, 0.62, photoTex());
    sign(
      -2.7,
      2.1,
      1.1,
      0.8,
      textTex(['FARES', 'Station 1.80', 'Ferry 1.20', 'Infirmary 2.40', 'After 12: time and a half'], {
        w: 256,
        h: 190,
        bg: '#f0c818',
        fg: '#111',
        font: 'cab',
      }),
    );
    sign(
      -6.3,
      1.9,
      0.5,
      0.7,
      textTex(['OCTOBER', '1990'], { w: 128, h: 170, bg: '#e9e4d2', fg: '#8a1a1a', font: 'serif' }),
      -hd + 0.03,
    );
    counter(4.1, -1.9, 1.9, 0.95, '#4a3a2a', 0.76);
    B(0.42, 0.06, 0.3, 4.2, 0.83, -1.8, '#5a1f1a');
    B(0.26, 0.14, 0.3, 3.5, 0.87, -1.9, '#6a6a60', M.iron);
    B(0.24, 0.1, 0.12, 4.75, 1.04, -2.05, '#2f6a3a', M.glow);
    B(0.03, 0.26, 0.03, 4.75, 0.9, -2.05, '#b8943a');
    chair(4.1, -1.0, 3.14);
    cabinet(1.9, -3.6);
    cabinet(2.45, -3.6);
    cabinet(3.0, -3.6);
    B(0.26, 0.16, 0.2, 2.45, 1.4, -3.6, '#7a2a22', M.iron);
    doorB(5.4, '#33271c');
    rooms.lockDoor = new THREE.Mesh(
      new THREE.BoxGeometry(0.4, 0.5, 0.03),
      lit(
        new THREE.MeshLambertMaterial({
          map: textTex(['PRIVATE'], { w: 128, h: 40, bg: '#2a2018', fg: '#b8943a', font: 'serif' }),
        }),
      ),
    );
    rooms.lockDoor.geometry = new THREE.PlaneGeometry(0.5, 0.14);
    rooms.lockDoor.position.set(5.4, 1.6, -hd + 0.1);
    g.add(rooms.lockDoor);
    B(0.06, 0.06, 0.12, 1.1, 1.85, -hd + 0.07, '#b8943a');
    const coat = new THREE.Mesh(
      new THREE.BoxGeometry(0.5, 1.25, 0.14),
      lit(new THREE.MeshLambertMaterial({ color: '#1c1d22' })),
    );
    coat.position.set(1.1, 1.2, -hd + 0.12);
    g.add(coat);
    rooms.coat = coat;
    B(0.85, 0.4, 1.9, 6.3, 0.2, -2.6, '#4a4238');
    B(0.85, 0.1, 1.9, 6.3, 0.46, -2.6, '#6a6a5a');
    S(6.3, -2.6, 0.85, 1.9);
    B(0.08, 2.1, 0.95, hw - 0.04, 1.05, 1.6, '#2f4a3a');
    B(0.9, 0.02, 1.0, 6.2, 0.012, 1.6, '#3a2f22');
  } else if (k === 'caff') {
    counter(2.2, -2.0, 5.2, 0.7, '#b8a98a');
    bt.add(M.iron, xform(new THREE.CylinderGeometry(0.2, 0.2, 0.55, 10), 0.3, 1.27, -2.0), '#c8c8c8');
    B(0.3, 0.26, 0.3, 1.0, 1.1, -2.0, '#3a3a3a');
    B(1.2, 0.3, 0.4, 3.4, 1.14, -2.0, '#c8d8d8', M.flat);
    for (let i = 0; i < 5; i++) B(0.14, 0.08, 0.14, 3.0 + i * 0.2, 1.06, -2.0, '#c89a4a');
    doorB(4.5, '#6a6250');
    sign(
      1.6,
      2.3,
      3.4,
      0.85,
      textTex(['BREAKFAST 1.20    BACON SARNIE 70p', 'TEA 20p    CHIPS 45p    PIE & PEAS 95p'], {
        w: 512,
        h: 128,
        bg: '#1a1a1a',
        fg: '#e8e0c8',
        font: 'type',
      }),
    );
    for (const [tx, tz, a, b2] of [
      [-3, -1.6, 's1', 's2'],
      [-3, 0.9, 's3', 's4'],
      [0.4, 1.2, 's5', 's6'],
      [3.6, 1.2, 's7', 's8'],
    ]) {
      table(tx, tz);
      for (const s of [a, b2]) chair(sp[s][0], sp[s][1], sp[s][2] + Math.PI, '#7a2a22');
      B(0.05, 0.14, 0.05, tx + 0.1, 0.83, tz, '#8a1a1a');
      B(0.05, 0.14, 0.05, tx - 0.1, 0.83, tz, '#3a2418');
    }
  } else if (k === 'fish') {
    counter(-0.4, -1.3, 5, 0.9, '#dfe8ea', 0.9);
    for (let i = 0; i < 26; i++)
      bt.add(
        M.flat,
        xform(
          new THREE.SphereGeometry(0.16, 6, 4),
          -2.6 + rr() * 4.4,
          0.98,
          -1.6 + rr() * 0.6,
          rr() * 3,
          0,
          0,
          1.6,
          0.3,
          0.6,
        ),
        ['#8a9aa2', '#aab4b8', '#6a7a82', '#c8b0a0'][i % 4],
      );
    B(4.8, 0.04, 0.8, -0.4, 0.95, -1.3, '#f4f8f8');
    sign(
      -0.4,
      2.2,
      3,
      0.6,
      textTex(['FRESH OFF THE DOCK DAILY'], { w: 512, h: 96, bg: '#1f4a6b', fg: '#f0ead8', font: 'slab' }),
    );
    B(0.4, 0.4, 0.3, 2.9, 1.15, -1.3, '#c8c8c8', M.iron);
  } else if (k === 'laund') {
    for (let i = 0; i < 5; i++) {
      B(0.7, 0.95, 0.65, -2.8 + i * 0.8, 0.48, -2.6, '#e8e8e0');
      bt.add(
        M.flat,
        xform(new THREE.CylinderGeometry(0.2, 0.2, 0.04, 12), -2.8 + i * 0.8, 0.5, -2.26, 0, Math.PI / 2),
        '#22303a',
      );
    }
    S(-1.2, -2.6, 4.2, 0.7);
    B(0.9, 1.9, 0.7, 2.9, 0.95, -2.6, '#d8d8d0');
    S(2.9, -2.6, 0.9, 0.7);
    B(2.6, 0.45, 0.45, -2.0, 0.23, 1.25, '#5a6a7a');
    sign(
      -2.0,
      2.1,
      1.3,
      0.5,
      textTex(['No 4 OUT OF ORDER'], { w: 256, h: 80, bg: '#f4f0e0', fg: '#a01818', font: 'plain' }),
    );
  } else if (k === 'grocer' || k === 'news' || k === 'iron' || k === 'chandler') {
    const left = k === 'iron';
    shelf(left ? 1.2 : -1.4, 4.2);
    counter(sp.k[0], -1.3, 2.4, 0.7);
    if (k === 'news') {
      for (let i = 0; i < 5; i++)
        B(0.34, 0.1 + rr() * 0.1, 0.26, sp.k[0] - 0.9 + i * 0.42, 1.04, -1.3, i % 2 ? '#e8e4d8' : '#c8c2b0');
      sign(
        -1.4,
        2.35,
        2.6,
        0.5,
        textTex(['EVENING MAIL: FIRE FILE "STILL OPEN"'], {
          w: 512,
          h: 90,
          bg: '#f4f0e0',
          fg: '#111',
          font: 'serif',
        }),
      );
      for (let i = 0; i < 6; i++)
        bt.add(
          M.flat,
          xform(new THREE.CylinderGeometry(0.09, 0.09, 0.24, 8), -3.0 + i * 0.26, 0.35, 1.2),
          `hsl(${i * 55},60%,45%)`,
        );
    }
    if (k === 'grocer')
      for (let i = 0; i < 4; i++) {
        B(0.6, 0.35, 0.45, -2.8 + i * 0.7, 0.18, 1.3, '#6a5a3a', M.wood);
        for (let j = 0; j < 5; j++)
          bt.add(
            M.flat,
            xform(new THREE.SphereGeometry(0.09, 6, 5), -3.0 + i * 0.7 + rr() * 0.4, 0.42, 1.2 + rr() * 0.3),
            ['#b8401a', '#3a7a2a', '#c8b82a', '#8a5a1a'][i],
          );
      }
    if (k === 'iron') {
      for (let i = 0; i < 9; i++) B(0.04, 0.6 + rr() * 0.6, 0.04, -3.1 + i * 0.22, 1.7, -2.9, '#777');
      for (let i = 0; i < 3; i++)
        bt.add(
          M.iron,
          xform(new THREE.CylinderGeometry(0.28, 0.28, 0.8, 10), 2.6 - i * 0.65, 0.4, 1.4),
          '#3a5a7a',
        );
    }
    if (k === 'chandler') {
      for (let i = 0; i < 4; i++)
        bt.add(
          M.flat,
          xform(new THREE.TorusGeometry(0.3, 0.09, 6, 12), -3.3 + i * 0.75, 1.7, -2.85),
          ['#b8a070', '#8a7a50', '#c8641a', '#b8a070'][i],
        );
      for (let i = 0; i < 3; i++) B(0.5, 1.1, 0.12, 2.6 - i * 0.6, 1.45, -2.85, '#c8a820');
      bt.add(M.flat, xform(new THREE.TorusGeometry(0.34, 0.08, 6, 14), 3.4, 2.2, -2.9), '#d85a1a');
    }
  } else if (k === 'takeaway') {
    counter(0.3, -1.3, 6, 0.6, '#a4161a', 1.15);
    B(5, 1.0, 0.6, 0.3, 0.5, -2.6, '#b8b8b8', M.iron);
    S(0.3, -2.6, 5, 0.6);
    sign(
      0.3,
      2.35,
      5.2,
      1.0,
      textTex(
        [
          'GOLDEN RIVER',
          '1 CHOP SUEY ROLL 60p   2 CHICKEN CHOW MEIN 1.90   3 SWEET & SOUR PORK 2.10',
          '4 KING PRAWN CURRY 2.60   CHIPS 45p   CURRY SAUCE 30p   PRAWN CRACKERS 40p',
        ],
        { w: 1024, h: 200, bg: '#f6d55c', fg: '#a4161a', font: 'slab' },
      ),
    );
    chair(-3.2, 1.4, 1.57);
    chair(3.2, 1.4, -1.57);
    sign(
      -3.3,
      1.7,
      0.6,
      0.8,
      textTex(['1990', 'YEAR OF', 'THE HORSE'], {
        w: 128,
        h: 170,
        bg: '#a4161a',
        fg: '#f6d55c',
        font: 'serif',
      }),
    );
  } else if (k === 'tearoom') {
    counter(sp.k[0], -1.6, 1.8, 0.7, '#7b3f2a');
    for (let i = 0; i < 3; i++)
      bt.add(
        M.flat,
        xform(
          new THREE.CylinderGeometry(0.16 - i * 0.04, 0.16 - i * 0.04, 0.03, 10),
          2.6,
          1.05 + i * 0.12,
          -1.6,
        ),
        '#e8e4d8',
      );
    for (const [tx, tz, a, b2] of [
      [-1.9, -0.6, 's1', 's2'],
      [1.3, 0.9, 's3', 's4'],
    ]) {
      table(tx, tz, '#f0ece0');
      for (const s of [a, b2]) chair(sp[s][0], sp[s][1], sp[s][2] + Math.PI, '#5a3a2a');
      bt.add(M.flat, xform(new THREE.SphereGeometry(0.1, 8, 6), tx, 0.86, tz), '#d8c8a8');
    }
    sign(
      -1.5,
      2.0,
      1.0,
      0.7,
      textTex(['Humber', 'at dusk'], { w: 128, h: 90, bg: '#6a7a8a', fg: '#d8c8a8', font: 'script' }),
    );
  } else if (k === 'pawn') {
    counter(-0.6, -1.3, 5, 0.7, '#3a3028');
    for (let i = 0; i < 16; i++) B(0.03, 1.15, 0.03, -3.0 + i * 0.32, 1.55, -1.0, '#8a8478');
    B(5, 0.06, 0.06, -0.6, 2.13, -1.0, '#8a8478');
    shelf(-1.2, 3.6, 3);
    B(0.5, 0.36, 0.3, -2.4, 1.2, -2.6, '#3a3a40');
    B(0.6, 0.5, 0.4, 0.2, 0.7, -2.6, '#2a2a2a');
    bt.add(
      M.flat,
      xform(new THREE.CylinderGeometry(0.18, 0.18, 0.08, 12), -1.0, 1.75, -2.75, 0, Math.PI / 2),
      '#e8dfb8',
    );
    doorB(3.2, '#2a2420');
    sign(
      1.0,
      2.5,
      2.4,
      0.4,
      textTex(['PLEDGES TAKEN · NO CHEQUES'], { w: 512, h: 80, bg: '#161616', fg: '#d8b24a', font: 'serif' }),
    );
  } else if (k === 'boarding') {
    B(0.15, 3.1, 4.3, 1.2, 1.55, -1.35, wc, M.wall);
    S(1.2, -1.35, 0.15, 4.3);
    W(1.2, -1.35, 0.15, 4.3);
    counter(-3.4, -1.6, 1.8, 0.8, '#4a3526');
    sign(
      -3.4,
      1.9,
      1.1,
      0.8,
      textTex(['1  2  3  4', '5  6  7  8'], { w: 200, h: 140, bg: '#3a2a1e', fg: '#b8943a', font: 'serif' }),
    );
    for (let i = 0; i < 6; i++) {
      B(1.3, 0.25, 0.5, -1.0, 0.13 + i * 0.25, -3.2 + i * 0.0, '#5a4030', M.wood);
    }
    S(-1.0, -3.0, 1.3, 0.9);
    armchair(sp.june[0], sp.june[1], sp.june[2], '#5a4a52');
    armchair(sp.chair[0], sp.chair[1], sp.chair[2], '#5a4a52');
    B(0.95, 0.42, 1.95, 4.3, 0.21, -2.3, '#4a4238');
    B(0.95, 0.12, 1.95, 4.3, 0.48, -2.3, '#8a8a7a');
    B(0.9, 0.12, 0.4, 4.3, 0.58, -3.05, '#d8d4c8');
    S(4.3, -2.3, 0.95, 1.95);
    B(0.9, 1.9, 0.55, 2.0, 0.95, -3.1, '#3f2e20', M.wood);
    S(2.0, -3.1, 0.9, 0.55);
    B(0.5, 0.8, 0.4, 5.0, 0.4, 0.4, '#d8d4c8');
    S(5.0, 0.4, 0.5, 0.4);
    const sc = new THREE.Mesh(
      new THREE.BoxGeometry(0.62, 0.42, 0.16),
      lit(new THREE.MeshLambertMaterial({ color: '#5a4028' })),
    );
    sc.position.set(3.0, 0.21, -3.2);
    g.add(sc);
    rooms.suitcase = sc;
    sign(4.3, 1.9, 1.1, 1.3, textTex([''], { w: 32, h: 32, bg: '#8a96a0' }));
  } else if (k === 'coin') {
    counter(0.2, -0.9, 3.4, 0.6, '#4a4238');
    B(0.4, 0.03, 0.3, 0.2, 1.0, -0.9, '#2a1a3a');
    for (let i = 0; i < 3; i++)
      bt.add(
        M.flat,
        xform(new THREE.CylinderGeometry(0.03, 0.03, 0.01, 8), 0.08 + i * 0.12, 1.02, -0.9),
        '#b8943a',
      );
    B(2.6, 2.0, 0.3, -1.4, 1.0, -2.4, '#3a3026', M.wood);
    S(-1.4, -2.4, 2.6, 0.3);
    doorB(2.3, '#2a2420');
    sign(
      0.4,
      2.3,
      1.6,
      0.36,
      textTex(['BETWEEN STOCK'], { w: 256, h: 60, bg: '#d8d0b8', fg: '#333', font: 'type' }),
    );
  } else if (k === 'chapel') {
    B(1.6, 0.02, d, 0, 0.012, 0.4, '#6a1f24');
    B(w - 1, 0.18, 2.6, 0, 0.09, -5.2, '#8a8474');
    B(2.2, 0.95, 0.8, 0, 0.66, -5.4, '#e8e4d8');
    S(0, -5.4, 2.2, 0.8);
    B(0.1, 1.5, 0.06, 0, 2.4, -hd + 0.06, '#5a4028');
    B(0.8, 0.1, 0.06, 0, 2.75, -hd + 0.06, '#5a4028');
    for (const x of [-0.8, 0.8]) {
      B(0.05, 0.3, 0.05, x, 1.28, -5.4, '#e8e0c8');
      B(0.03, 0.05, 0.03, x, 1.46, -5.4, '#fff', M.glow);
    }
    for (const z of [-2.4, -0.4, 1.6, 3.6])
      for (const x of [-2.7, 2.7]) {
        B(3.2, 0.06, 0.4, x, 0.45, z, '#4a3526', M.wood);
        B(3.2, 0.5, 0.06, x, 0.7, z + 0.2, '#4a3526', M.wood);
        B(3.2, 0.45, 0.06, x, 0.22, z, '#3f2e20');
        S(x, z + 0.1, 3.2, 0.5);
      }
    B(0.6, 0.9, 0.4, 3.9, 0.45, -3.6, '#2a2622', M.iron);
    for (let i = 0; i < 7; i++) B(0.03, 0.06, 0.03, 3.68 + i * 0.07, 0.95, -3.6, '#fff', M.glow);
  } else if (k === 'harbour') {
    counter(1.8, -1.2, 4, 0.7, '#3a4a52');
    B(4, 0.9, 0.04, 1.8, 1.45, -0.9, '#8a9aa0', M.flat);
    sign(
      -2.6,
      1.9,
      1.8,
      1.2,
      textTex(['TIDE TABLES', 'HW 0412  1638', 'NOTICES TO MARINERS', 'FERRY: 0800 1230 1730 2230'], {
        w: 256,
        h: 170,
        bg: '#e9e4d2',
        fg: '#17243a',
        font: 'type',
      }),
    );
    B(2.4, 0.45, 0.45, -2.8, 0.23, 1.2, '#4a3a2a', M.wood);
    cabinet(4.1, -2.6);
    cabinet(3.5, -2.6);
  } else if (k === 'parlour') {
    armchair(sp.ada[0], sp.ada[1], sp.ada[2], '#6a5a6a');
    armchair(sp.tom[0], sp.tom[1], sp.tom[2], '#6a5a6a');
    table(-0.25, -0.9, '#4a3526', 0.6);
    bt.add(M.flat, xform(new THREE.SphereGeometry(0.1, 8, 6), -0.25, 0.86, -0.9), '#e8e0d0');
    for (const dx of [-0.2, 0.2])
      bt.add(
        M.flat,
        xform(new THREE.CylinderGeometry(0.04, 0.03, 0.06, 8), -0.25 + dx, 0.8, -0.75),
        '#f0ece0',
      );
    B(1.5, 1.15, 0.3, 0.6, 0.58, -hd + 0.15, '#3a3530');
    B(0.7, 0.6, 0.05, 0.6, 0.4, -hd + 0.32, '#c8501a', M.glow);
    B(1.7, 0.06, 0.38, 0.6, 1.18, -hd + 0.18, '#4a3526');
    for (let i = 0; i < 4; i++) B(0.14, 0.2, 0.03, 0.1 + i * 0.32, 1.32, -hd + 0.2, '#b8a888');
    B(1.5, 0.85, 0.45, -2.5, 0.43, -hd + 0.25, '#4a3526', M.wood);
    S(-2.5, -hd + 0.25, 1.5, 0.45);
    B(0.4, 0.28, 0.2, -2.5, 1.0, -hd + 0.25, '#5a4030');
    B(1.9, 0.02, 2.6, 0, 0.012, -0.6, '#5a2f35');
    B(0.04, 1.4, 1.2, hw - 0.02, 1.6, 0.6, '#c8d0d0', M.glow);
    B(0.03, 1.4, 1.2, hw - 0.05, 1.6, 0.6, '#e8e8e0');
  }
  bt.build(g, { cull: false });
}
