// Renderer plumbing: shared uniforms, the lamp-light patch every material gets, wet-ground reflections,
// procedural textures drawn in code, and a geometry batcher.
import * as THREE from 'three';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import { BOUNDS } from '../map.js';
import { field, GW, GH, FERRY, bake } from '../light.js';

export { THREE };
export const U = {
  uLampMap: { value: null },
  uLampOrg: { value: new THREE.Vector2(BOUNDS.x0, BOUNDS.z0) },
  uLampInv: { value: new THREE.Vector2(1 / (GW * 0.75), 1 / (GH * 0.75)) },
  uLampOn: { value: new THREE.Vector4(0, 0, 0, 0) },
  uFerry: { value: new THREE.Vector4(FERRY.x, FERRY.z, FERRY.r, 0) },
  uSodium: { value: new THREE.Color(1.0, 0.46, 0.1) },
  uWhite: { value: new THREE.Color(1.0, 0.84, 0.6) },
  uInside: { value: 0 },
  uTime: { value: 0 },
  uWet: { value: 0.8 },
  uRain: { value: 0.3 },
  tRefl: { value: null },
  uReflMat: { value: new THREE.Matrix4() },
  uReflOn: { value: 1 },
  tNoise: { value: null },
  uWinLevel: { value: 0 },
  uShopLit: { value: new THREE.Vector3(0, 0, 0) },
  uNight: { value: 0 },
};
const LAMP_PARS = `
uniform sampler2D uLampMap; uniform vec2 uLampOrg; uniform vec2 uLampInv; uniform vec4 uLampOn; uniform vec4 uFerry; uniform vec3 uSodium; uniform vec3 uWhite; uniform float uInside;
varying vec3 vWp;
vec3 lampLight(vec3 wp){
  vec3 wn = normalize(cross(dFdx(wp), dFdy(wp)));
  vec4 l = texture2D(uLampMap, (wp.xz + wn.xz * 0.8 - uLampOrg) * uLampInv);
  float fo = uFerry.w * pow(max(0.0, 1.0 - distance(wp.xz, uFerry.xy) / uFerry.z), 1.5) * 0.95;
  float sod = max(0.0, l.r - fo) * uLampOn.x;
  float wh = l.g * uLampOn.x + l.b * uLampOn.z + l.a * uLampOn.w;
  float hf = 1.0 - smoothstep(4.0, 15.0, wp.y);
  return (uSodium * sod * 1.75 + uWhite * wh * 1.25) * hf * (1.0 - uInside);
}`;
const GROUND_PARS = `
uniform sampler2D tRefl; uniform mat4 uReflMat; uniform float uWet; uniform float uRain; uniform float uTime; uniform sampler2D tNoise; uniform float uReflOn;`;
const GROUND_APPLY = `
{ float pn = texture2D(tNoise, vWp.xz * 0.037).r * 0.62 + texture2D(tNoise, vWp.xz * 0.151).g * 0.38;
  float puddle = smoothstep(0.60 - uWet * 0.16, 0.69 - uWet * 0.14, pn) * (1.0 - uInside) * PUDDLE;
  float wet = clamp(uWet * 0.5 + puddle, 0.0, 1.0) * (1.0 - uInside);
  vec3 V = normalize(cameraPosition - vWp);
  float fres = 0.05 + 0.95 * pow(1.0 - max(V.y, 0.0), 4.0);
  vec2 rough = (texture2D(tNoise, vWp.xz * 0.7).rg - 0.5) * (1.0 - puddle) * 0.045;
  vec2 rip = (texture2D(tNoise, vWp.xz * 1.3 + vec2(uTime * 0.9, uTime * 0.6)).ba - 0.5) * uRain * puddle * 0.03;
  vec4 rc = uReflMat * vec4(vWp.x, 0.0, vWp.z, 1.0);
  vec2 ruv = rc.xy / max(rc.w, 0.001) + rough + rip;
  float blur = mix(0.045, 0.006, puddle);
  vec3 rf = vec3(0.0);
  for (int i = 0; i < 6; i++) { rf += texture2D(tRefl, ruv + vec2(0.0, (float(i) * 1.5 - 1.2) * blur)).rgb; }
  rf *= 0.1667 * uReflOn;
  outgoingLight *= 1.0 - 0.38 * wet;
  outgoingLight += rf * fres * mix(0.55, 1.25, puddle) * wet;
  outgoingLight += lampLight(vWp) * wet * (0.05 + 0.16 * puddle) * (0.6 + 0.4 * fres);
}`;
// Give a standard material the town's lamp light (and, for ground, the wet reflections).
export function lit(mat, opts = {}) {
  mat.onBeforeCompile = (sh) => {
    for (const k in U) sh.uniforms[k] = U[k];
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vWp;')
      .replace(
        '#include <project_vertex>',
        '#include <project_vertex>\n{ vec4 wp_ = vec4(transformed, 1.0);\n#ifdef USE_INSTANCING\nwp_ = instanceMatrix * wp_;\n#endif\nvWp = (modelMatrix * wp_).xyz; }',
      );
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', '#include <common>\n' + LAMP_PARS + (opts.ground ? GROUND_PARS : ''))
      .replace(
        '#include <opaque_fragment>',
        'outgoingLight += diffuseColor.rgb * lampLight(vWp) * ' +
          (opts.gain || 1).toFixed(2) +
          ';\n' +
          (opts.ground ? GROUND_APPLY.replace('PUDDLE', (opts.puddle ?? 1).toFixed(2)) : '') +
          '\n#include <opaque_fragment>',
      );
  };
  mat.customProgramCacheKey = () => 'lit' + (opts.ground ? 'G' + (opts.puddle ?? 1) : '') + (opts.gain || 1);
  return mat;
}
export function lampMapTexture() {
  bake();
  const data = new Uint8Array(GW * GH * 4);
  for (let i = 0; i < GW * GH; i++)
    for (let c = 0; c < 4; c++) data[i * 4 + c] = Math.min(255, Math.round(field[c][i] * 255));
  const t = new THREE.DataTexture(data, GW, GH, THREE.RGBAFormat);
  t.magFilter = t.minFilter = THREE.LinearFilter;
  t.needsUpdate = true;
  U.uLampMap.value = t;
  return t;
}

// ---------- canvas textures ----------
export function canvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  return c;
}
export function tex(c, rep = true, srgb = true) {
  const t = new THREE.CanvasTexture(c);
  if (rep) t.wrapS = t.wrapT = THREE.RepeatWrapping;
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  t.needsUpdate = true;
  return t;
}
let seed = 7;
const rr = () => {
  seed = (seed * 16807) % 2147483647;
  return seed / 2147483647;
};
const shade = (hex, f) => {
  const c = new THREE.Color(hex);
  c.multiplyScalar(f);
  return '#' + c.getHexString();
};
const jit = (hex, a) => {
  const c = new THREE.Color(hex);
  const k = 1 + (rr() - 0.5) * a;
  c.r *= k;
  c.g *= k * (1 + (rr() - 0.5) * a * 0.3);
  c.b *= k;
  return '#' + c.getHexString();
};
function speckle(ctx, S, n, a, col = '0,0,0') {
  for (let i = 0; i < n; i++) {
    ctx.fillStyle = `rgba(${col},${rr() * a})`;
    ctx.fillRect(rr() * S, rr() * S, 1 + rr() * 2, 1 + rr() * 2);
  }
}
// height canvas (greyscale) to a tangent-space normal map
function normalFrom(hc, strength = 2) {
  const S = hc.width,
    src = hc.getContext('2d').getImageData(0, 0, S, S).data,
    out = canvas(S, S),
    o = out.getContext('2d'),
    img = o.createImageData(S, S);
  const H = (x, y) => src[(((y + S) % S) * S + ((x + S) % S)) * 4];
  for (let y = 0; y < S; y++)
    for (let x = 0; x < S; x++) {
      const dx = ((H(x + 1, y) - H(x - 1, y)) / 255) * strength,
        dy = ((H(x, y + 1) - H(x, y - 1)) / 255) * strength,
        l = Math.hypot(dx, dy, 1),
        i = (y * S + x) * 4;
      img.data[i] = ((-dx / l) * 0.5 + 0.5) * 255;
      img.data[i + 1] = ((dy / l) * 0.5 + 0.5) * 255;
      img.data[i + 2] = ((1 / l) * 0.5 + 0.5) * 255;
      img.data[i + 3] = 255;
    }
  o.putImageData(img, 0, 0);
  return tex(out, true, false);
}
export function noiseTex() {
  const S = 256,
    d = new Uint8Array(S * S * 4);
  for (let c = 0; c < 4; c++) {
    const acc = new Float32Array(S * S);
    for (const [g, amp] of [
      [8, 0.5],
      [16, 0.28],
      [32, 0.14],
      [64, 0.08],
    ]) {
      const r = new Float32Array(g * g).map(() => rr());
      for (let y = 0; y < S; y++)
        for (let x = 0; x < S; x++) {
          const fx = (x / S) * g,
            fy = (y / S) * g,
            x0 = Math.floor(fx),
            y0 = Math.floor(fy),
            u = fx - x0,
            v = fy - y0,
            su = u * u * (3 - 2 * u),
            sv = v * v * (3 - 2 * v);
          const a = r[(y0 % g) * g + (x0 % g)],
            b = r[(y0 % g) * g + ((x0 + 1) % g)],
            cc = r[((y0 + 1) % g) * g + (x0 % g)],
            dd = r[((y0 + 1) % g) * g + ((x0 + 1) % g)];
          acc[y * S + x] += amp * ((a * (1 - su) + b * su) * (1 - sv) + (cc * (1 - su) + dd * su) * sv);
        }
    }
    for (let i = 0; i < S * S; i++) d[i * 4 + c] = acc[i] * 255;
  }
  const t = new THREE.DataTexture(d, S, S, THREE.RGBAFormat);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.magFilter = t.minFilter = THREE.LinearFilter;
  t.needsUpdate = true;
  U.tNoise.value = t;
  return t;
}
export function brickTex(kind) {
  const S = 512,
    c = canvas(S, S),
    x = c.getContext('2d');
  const P =
    {
      soot: ['#3a322c', ['#5a4a40', '#4f3f33', '#463c36', '#66483c', '#57504a', '#3d3531']],
      red: ['#4a3a32', ['#8e4533', '#7a3c2e', '#96523c', '#693a2e', '#844a38', '#55362e']],
      yellow: ['#4a4336', ['#8a7650', '#7a6846', '#6d5d42', '#5a4f3c']],
    }[kind] || null;
  if (kind === 'stone') {
    x.fillStyle = '#4b4840';
    x.fillRect(0, 0, S, S);
    for (let r = 0; r < 6; r++) {
      let px = r % 2 ? -60 : 0;
      while (px < S) {
        const w = 110 + rr() * 70;
        x.fillStyle = jit('#77705f', 0.25);
        x.fillRect(px + 2, (r * S) / 6 + 2, w - 4, S / 6 - 4);
        px += w;
      }
    }
    speckle(x, S, 5000, 0.18);
    for (let i = 0; i < 30; i++) {
      const g = x.createLinearGradient(0, 0, 0, S);
      g.addColorStop(0, 'rgba(15,12,10,0.25)');
      g.addColorStop(1, 'rgba(15,12,10,0)');
      x.fillStyle = g;
      x.fillRect(rr() * S, 0, 6 + rr() * 22, S * rr());
    }
    return tex(c);
  }
  x.fillStyle = P[0];
  x.fillRect(0, 0, S, S);
  const rows = 32,
    bw = S / 10,
    bh = S / rows;
  for (let r = 0; r < rows; r++)
    for (let i = -1; i < 11; i++) {
      const bx = i * bw + (r % 2 ? bw / 2 : 0);
      x.fillStyle = jit(P[1][Math.floor(rr() * P[1].length)], 0.3);
      x.fillRect(bx + 1.2, r * bh + 1.2, bw - 2.4, bh - 2.4);
      if (rr() < 0.12) {
        x.fillStyle = 'rgba(0,0,0,0.3)';
        x.fillRect(bx + 1.2, r * bh + 1.2, bw - 2.4, bh - 2.4);
      }
    }
  speckle(x, S, 9000, 0.22);
  for (let i = 0; i < 26; i++) {
    const g = x.createLinearGradient(0, 0, 0, S);
    g.addColorStop(0, 'rgba(8,7,6,0.3)');
    g.addColorStop(1, 'rgba(8,7,6,0)');
    x.fillStyle = g;
    x.fillRect(rr() * S, 0, 5 + rr() * 30, S * (0.3 + rr() * 0.7));
  }
  return tex(c);
}
export function slateTex() {
  const S = 256,
    c = canvas(S, S),
    x = c.getContext('2d');
  x.fillStyle = '#17181b';
  x.fillRect(0, 0, S, S);
  for (let r = 0; r < 12; r++)
    for (let i = -1; i < 9; i++) {
      x.fillStyle = jit('#2b2e35', 0.35);
      x.fillRect(i * 32 + (r % 2 ? 16 : 0) + 1, (r * S) / 12 + 1, 30, S / 12 - 1.5);
    }
  speckle(x, S, 2500, 0.2);
  speckle(x, S, 300, 0.25, '120,140,90');
  return tex(c);
}
export function groundTex(kind) {
  const S = 512,
    c = canvas(S, S),
    x = c.getContext('2d'),
    h = canvas(S, S),
    hx = h.getContext('2d');
  hx.fillStyle = '#808080';
  hx.fillRect(0, 0, S, S);
  if (kind === 'asphalt') {
    x.fillStyle = '#26272a';
    x.fillRect(0, 0, S, S);
    speckle(x, S, 26000, 0.35, '90,90,95');
    speckle(x, S, 16000, 0.4);
    for (let i = 0; i < 9; i++) {
      x.fillStyle = `rgba(${rr() < 0.5 ? '10,10,12' : '60,60,64'},${0.12 + rr() * 0.14})`;
      x.beginPath();
      x.ellipse(rr() * S, rr() * S, 30 + rr() * 90, 20 + rr() * 50, rr() * 3, 0, 7);
      x.fill();
    }
    for (let i = 0; i < 9000; i++) {
      const v = 100 + rr() * 60;
      hx.fillStyle = `rgb(${v},${v},${v})`;
      hx.fillRect(rr() * S, rr() * S, 2, 2);
    }
    return { map: tex(c), normalMap: normalFrom(h, 1.2) };
  }
  if (kind === 'flags') {
    x.fillStyle = '#34322e';
    x.fillRect(0, 0, S, S);
    for (let r = 0; r < 3; r++)
      for (let i = -1; i < 3; i++) {
        const bx = i * 256 + (r % 2 ? 128 : 0),
          by = (r * S) / 3;
        x.fillStyle = jit('#5f5d57', 0.2);
        x.fillRect(bx + 2, by + 2, 252, S / 3 - 4);
        hx.fillStyle = '#909090';
        hx.fillRect(bx + 3, by + 3, 250, S / 3 - 6);
      }
    hx.strokeStyle = '#303030';
    hx.lineWidth = 4;
    for (let r = 0; r <= 3; r++) {
      hx.beginPath();
      hx.moveTo(0, (r * S) / 3);
      hx.lineTo(S, (r * S) / 3);
      hx.stroke();
    }
    speckle(x, S, 12000, 0.2);
    speckle(x, S, 60, 0.5, '20,20,20');
    for (let i = 0; i < 40; i++) {
      x.fillStyle = 'rgba(200,200,190,0.25)';
      x.beginPath();
      x.arc(rr() * S, rr() * S, 1.5 + rr() * 2, 0, 7);
      x.fill();
    }
    return { map: tex(c), normalMap: normalFrom(h, 1.5) };
  }
  // setts
  x.fillStyle = '#1b1b1c';
  x.fillRect(0, 0, S, S);
  const rows = 12,
    sw = S / 8,
    sh = S / rows;
  for (let r = 0; r < rows; r++)
    for (let i = -1; i < 9; i++) {
      const bx = i * sw + (r % 2 ? sw / 2 : 0) + (rr() - 0.5) * 3,
        by = r * sh;
      x.fillStyle = jit('#4a4a4c', 0.35);
      x.beginPath();
      x.roundRect(bx + 2, by + 2, sw - 4, sh - 4, 6);
      x.fill();
      const g = hx.createRadialGradient(bx + sw / 2, by + sh / 2, 2, bx + sw / 2, by + sh / 2, sw * 0.6);
      g.addColorStop(0, '#d0d0d0');
      g.addColorStop(1, '#505050');
      hx.fillStyle = g;
      hx.beginPath();
      hx.roundRect(bx + 2, by + 2, sw - 4, sh - 4, 6);
      hx.fill();
    }
  speckle(x, S, 9000, 0.25);
  return { map: tex(c), normalMap: normalFrom(h, 2.4) };
}
export function plainTex(kind) {
  const S = 256,
    c = canvas(S, S),
    x = c.getContext('2d');
  if (kind === 'boards') {
    x.fillStyle = '#4a3a2a';
    x.fillRect(0, 0, S, S);
    for (let i = 0; i < 6; i++) {
      x.fillStyle = jit('#5b4632', 0.25);
      x.fillRect((i * S) / 6 + 1, 0, S / 6 - 2, S);
    }
    for (let i = 0; i < 400; i++) {
      x.fillStyle = `rgba(20,12,6,${rr() * 0.25})`;
      x.fillRect(rr() * S, rr() * S, 1, 20 + rr() * 60);
    }
  } else if (kind === 'check') {
    for (let i = 0; i < 4; i++)
      for (let j = 0; j < 4; j++) {
        x.fillStyle = (i + j) % 2 ? '#b8a98a' : '#5a2a22';
        x.fillRect(i * 64, j * 64, 64, 64);
      }
    speckle(x, S, 2500, 0.2);
  } else if (kind === 'tile') {
    x.fillStyle = '#8a9296';
    x.fillRect(0, 0, S, S);
    for (let i = 0; i < 4; i++)
      for (let j = 0; j < 4; j++) {
        x.fillStyle = jit('#b4bcbc', 0.1);
        x.fillRect(i * 64 + 1.5, j * 64 + 1.5, 61, 61);
      }
    speckle(x, S, 1500, 0.15);
  } else if (kind === 'carpet') {
    x.fillStyle = '#5a2f35';
    x.fillRect(0, 0, S, S);
    for (let i = 0; i < 8; i++)
      for (let j = 0; j < 8; j++) {
        x.fillStyle = (i + j) % 2 ? '#6a3a3f' : '#4f2a30';
        x.beginPath();
        x.arc(i * 32 + 16, j * 32 + 16, 9, 0, 7);
        x.fill();
      }
    speckle(x, S, 5000, 0.2);
  } else if (kind === 'lino') {
    x.fillStyle = '#6f6a55';
    x.fillRect(0, 0, S, S);
    speckle(x, S, 9000, 0.18);
    speckle(x, S, 3000, 0.2, '200,190,150');
  } else if (kind === 'iron') {
    x.fillStyle = '#4a4a46';
    x.fillRect(0, 0, S, S);
    for (let i = 0; i < 16; i++) {
      const g = x.createLinearGradient(i * 16, 0, i * 16 + 16, 0);
      g.addColorStop(0, '#2c2c2a');
      g.addColorStop(0.5, '#6a6a64');
      g.addColorStop(1, '#2c2c2a');
      x.fillStyle = g;
      x.fillRect(i * 16, 0, 16, S);
    }
    speckle(x, S, 1500, 0.4, '110,60,30');
  } else if (kind === 'concrete') {
    x.fillStyle = '#3b3a37';
    x.fillRect(0, 0, S, S);
    speckle(x, S, 12000, 0.22);
    speckle(x, S, 5000, 0.15, '120,120,110');
  } else if (kind === 'planks') {
    x.fillStyle = '#2f2a24';
    x.fillRect(0, 0, S, S);
    for (let i = 0; i < 8; i++) {
      x.fillStyle = jit('#4a4238', 0.3);
      x.fillRect(0, i * 32 + 1, S, 30);
    }
    speckle(x, S, 4000, 0.25);
  } else {
    x.fillStyle = '#b9b294';
    x.fillRect(0, 0, S, S);
    speckle(x, S, 5000, 0.08);
  }
  return tex(c);
}
// windows: column 0 dark, 1 warm lit, 2 net curtain lit, 3 the blue of a television
export function windowTex() {
  const c = canvas(512, 256),
    x = c.getContext('2d');
  for (let k = 0; k < 4; k++) {
    const ox = k * 128;
    x.fillStyle = '#d8d2c0';
    x.fillRect(ox, 0, 128, 256);
    const g = x.createLinearGradient(ox, 0, ox + 128, 256);
    if (k === 0) {
      g.addColorStop(0, '#1a2026');
      g.addColorStop(0.5, '#0c0f13');
      g.addColorStop(1, '#232a30');
    } else if (k === 1) {
      g.addColorStop(0, '#ffcf7a');
      g.addColorStop(1, '#e89a3a');
    } else if (k === 2) {
      g.addColorStop(0, '#f6efd6');
      g.addColorStop(1, '#d9cba0');
    } else {
      g.addColorStop(0, '#5a7ab8');
      g.addColorStop(1, '#8aa4d8');
    }
    x.fillStyle = g;
    x.fillRect(ox + 10, 10, 108, 236);
    if (k === 1) {
      x.fillStyle = 'rgba(150,60,20,0.55)';
      x.fillRect(ox + 10, 10, 26, 236);
      x.fillRect(ox + 92, 10, 26, 236);
      x.fillStyle = 'rgba(255,240,200,0.6)';
      x.beginPath();
      x.arc(ox + 64, 70, 16, 0, 7);
      x.fill();
    }
    if (k === 2) {
      for (let i = 0; i < 18; i++) {
        x.fillStyle = 'rgba(255,255,255,0.25)';
        x.fillRect(ox + 10 + i * 6, 10, 2, 236);
      }
    }
    if (k === 0) {
      x.fillStyle = 'rgba(210,205,190,0.16)';
      x.fillRect(ox + 10, 10, 108, 90);
    }
    x.fillStyle = k === 0 ? 'rgba(206,202,190,0.3)' : 'rgba(255,250,235,0.34)';
    x.fillRect(ox + 10, 128, 108, 118);
    for (let i = 0; i < 27; i++) {
      x.fillStyle = 'rgba(255,255,255,' + (k === 0 ? 0.06 : 0.12) + ')';
      x.fillRect(ox + 10 + i * 4, 128, 1.5, 118);
    } // net curtains in the lower sash
    x.fillStyle = '#cfc8b4';
    x.fillRect(ox + 10, 122, 108, 12);
    x.fillRect(ox + 60, 10, 8, 236);
    x.strokeStyle = '#8f8974';
    x.lineWidth = 3;
    x.strokeRect(ox + 10, 10, 108, 236);
  }
  return tex(c, false);
}
export function shopInsideTex() {
  const c = canvas(512, 256),
    x = c.getContext('2d');
  const g = x.createLinearGradient(0, 0, 0, 256);
  g.addColorStop(0, '#c9a060');
  g.addColorStop(0.55, '#e6c890');
  g.addColorStop(1, '#6a4a2a');
  x.fillStyle = g;
  x.fillRect(0, 0, 512, 256);
  for (let r = 0; r < 2; r++) {
    x.fillStyle = 'rgba(50,30,15,0.85)';
    x.fillRect(0, 62 + r * 56, 512, 5);
    for (let i = 0; i < 46; i++) {
      if (rr() < 0.25) continue;
      x.fillStyle = `hsla(${rr() * 360},${12 + rr() * 22}%,${22 + rr() * 26}%,0.9)`;
      const w = 5 + rr() * 12,
        hh = 10 + rr() * 26;
      x.fillRect(i * 11.2 + rr() * 4, 62 + r * 56 - hh, w, hh);
    }
  }
  x.fillStyle = 'rgba(40,26,14,0.9)';
  x.fillRect(0, 190, 512, 66);
  x.fillStyle = 'rgba(255,240,200,0.5)';
  for (let i = 0; i < 4; i++) {
    x.beginPath();
    x.ellipse(64 + i * 128, 18, 30, 9, 0, 0, 7);
    x.fill();
  }
  return tex(c, true);
}
const FONTS = {
  cab: '700 %px Oswald, Impact, sans-serif',
  slab: '400 %px "Alfa Slab One", Georgia, serif',
  serif: '900 %px "Playfair Display", Georgia, serif',
  round: '600 %px Fredoka, "Arial Rounded MT Bold", sans-serif',
  script: '400 %px Yellowtail, "Brush Script MT", cursive',
  type: '700 %px "Courier Prime", monospace',
  plain: '700 %px Oswald, sans-serif',
};
export const font = (k, px) => (FONTS[k] || FONTS.serif).replace('%', px);
// A painted fascia, hand lettered, weathered.
export function signTex(text, sub, bg, fg, fontKey, w = 1024, h = 128, o = {}) {
  const c = canvas(w, h),
    x = c.getContext('2d');
  const g = x.createLinearGradient(0, 0, 0, h);
  g.addColorStop(0, shade(bg, 1.12));
  g.addColorStop(1, shade(bg, 0.8));
  x.fillStyle = g;
  x.fillRect(0, 0, w, h);
  x.strokeStyle = shade(fg, 0.8);
  x.lineWidth = 3;
  x.strokeRect(8, 8, w - 16, h - 16);
  x.textAlign = 'center';
  x.textBaseline = 'middle';
  const big = sub ? h * 0.5 : h * 0.62;
  let px = big;
  x.font = font(fontKey, px);
  while (x.measureText(text).width > w * 0.86 && px > 10) {
    px -= 2;
    x.font = font(fontKey, px);
  }
  const cy = sub ? h * 0.4 : h * 0.52;
  x.fillStyle = 'rgba(0,0,0,0.5)';
  x.fillText(text, w / 2 + px * 0.05, cy + px * 0.06);
  x.fillStyle = fg;
  x.fillText(text, w / 2, cy);
  if (sub) {
    let sp = h * 0.19;
    x.font = font('plain', sp);
    while (x.measureText(sub).width > w * 0.84 && sp > 8) {
      sp -= 1;
      x.font = font('plain', sp);
    }
    x.fillStyle = shade(fg, 0.92);
    x.fillText(sub, w / 2, h * 0.8);
  }
  if (!o.clean) {
    for (let i = 0; i < 500; i++) {
      x.fillStyle = `rgba(0,0,0,${rr() * 0.14})`;
      x.fillRect(rr() * w, rr() * h, 1 + rr() * 3, 4 + rr() * 26);
    }
    for (let i = 0; i < 14; i++) {
      const gg = x.createLinearGradient(0, 0, 0, h);
      gg.addColorStop(0, 'rgba(10,8,6,0.25)');
      gg.addColorStop(1, 'rgba(10,8,6,0)');
      x.fillStyle = gg;
      x.fillRect(rr() * w, 0, 8 + rr() * 40, h);
    }
  }
  return tex(c, false);
}
export function textTex(lines, o = {}) {
  // small painted notices and decals
  const w = o.w || 256,
    h = o.h || 128,
    c = canvas(w, h),
    x = c.getContext('2d');
  if (o.bg) {
    x.fillStyle = o.bg;
    x.fillRect(0, 0, w, h);
  }
  x.textAlign = 'center';
  x.textBaseline = 'middle';
  x.fillStyle = o.fg || '#fff';
  lines.forEach((ln, i) => {
    let px = o.px || h / (lines.length + 0.6);
    x.font = font(o.font || 'plain', px);
    while (x.measureText(ln).width > w * 0.92 && px > 6) {
      px -= 1;
      x.font = font(o.font || 'plain', px);
    }
    x.fillText(ln, w / 2, (h / lines.length) * (i + 0.5));
  });
  const t = tex(c, false);
  return t;
}
export function glowTex() {
  const c = canvas(128, 128),
    x = c.getContext('2d'),
    g = x.createRadialGradient(64, 64, 0, 64, 64, 64);
  g.addColorStop(0, 'rgba(255,255,255,1)');
  g.addColorStop(0.12, 'rgba(255,255,255,0.75)');
  g.addColorStop(0.4, 'rgba(255,255,255,0.16)');
  g.addColorStop(1, 'rgba(255,255,255,0)');
  x.fillStyle = g;
  x.fillRect(0, 0, 128, 128);
  return tex(c, false);
}
export function blobTex() {
  const c = canvas(64, 64),
    x = c.getContext('2d'),
    g = x.createRadialGradient(32, 32, 2, 32, 32, 32);
  g.addColorStop(0, 'rgba(0,0,0,0.55)');
  g.addColorStop(1, 'rgba(0,0,0,0)');
  x.fillStyle = g;
  x.fillRect(0, 0, 64, 64);
  return tex(c, false);
}

// ---------- geometry batching ----------
const _c = new THREE.Color();
export class Batch {
  constructor() {
    this.m = new Map();
  }
  add(mat, geo, color) {
    if (!geo.attributes.color) {
      const n = geo.attributes.position.count,
        a = new Float32Array(n * 3);
      _c.set(color || '#ffffff');
      for (let i = 0; i < n; i++) {
        a[i * 3] = _c.r;
        a[i * 3 + 1] = _c.g;
        a[i * 3 + 2] = _c.b;
      }
      geo.setAttribute('color', new THREE.BufferAttribute(a, 3));
    }
    if (geo.index) geo = geo.toNonIndexed();
    for (const k of Object.keys(geo.attributes))
      if (!['position', 'normal', 'uv', 'color', 'aLit'].includes(k)) geo.deleteAttribute(k);
    if (!this.m.has(mat)) this.m.set(mat, []);
    this.m.get(mat).push(geo);
    return this;
  }
  build(parent, o = {}) {
    const out = [];
    for (const [mat, list] of this.m) {
      const g = mergeGeometries(list, false);
      if (!g) continue;
      const mesh = new THREE.Mesh(g, mat);
      mesh.matrixAutoUpdate = false;
      if (o.layer !== undefined) mesh.layers.set(o.layer);
      mesh.frustumCulled = o.cull !== false;
      parent.add(mesh);
      out.push(mesh);
      list.forEach((x) => x.dispose());
    }
    this.m.clear();
    return out;
  }
}
const _m = new THREE.Matrix4(),
  _q = new THREE.Quaternion(),
  _e = new THREE.Euler(),
  _v = new THREE.Vector3(),
  _s = new THREE.Vector3();
export function xform(geo, x, y, z, ry = 0, rx = 0, rz = 0, sx = 1, sy = 1, sz = 1) {
  _e.set(rx, ry, rz, 'YXZ');
  _q.setFromEuler(_e);
  _m.compose(_v.set(x, y, z), _q, _s.set(sx, sy, sz));
  geo.applyMatrix4(_m);
  return geo;
}
export const boxG = (w, h, d, x, y, z, ry = 0) => xform(new THREE.BoxGeometry(w, h, d), x, y, z, ry);
// A box whose uv follows world size, so brick and stone keep their scale.
export function wallBox(w, h, d, x, y, z, tile = 2.4) {
  const g = new THREE.BoxGeometry(w, h, d),
    uv = g.attributes.uv,
    p = g.attributes.position,
    n = g.attributes.normal;
  for (let i = 0; i < uv.count; i++) {
    const nx = Math.abs(n.getX(i)),
      ny = Math.abs(n.getY(i));
    const u = nx > 0.5 ? p.getZ(i) + z : p.getX(i) + x,
      v = ny > 0.5 ? p.getZ(i) + z : p.getY(i) + y;
    uv.setXY(i, u / tile, v / tile);
  }
  return xform(g, x, y, z);
}
export function planeXZ(x0, z0, x1, z1, y, tile = 2) {
  const g = new THREE.PlaneGeometry(x1 - x0, z1 - z0);
  g.rotateX(-Math.PI / 2);
  g.translate((x0 + x1) / 2, y, (z0 + z1) / 2);
  const uv = g.attributes.uv,
    p = g.attributes.position;
  for (let i = 0; i < uv.count; i++) uv.setXY(i, p.getX(i) / tile, p.getZ(i) / tile);
  return g;
}
export function mat(o) {
  return lit(new THREE.MeshLambertMaterial(Object.assign({ vertexColors: true }, o)));
}
export { mergeGeometries };
