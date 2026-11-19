// Renderer, weather and time of day: overcast sky, real dusk, sodium lamps striking, rain, mist, gulls, the Humber.
import { THREE, U, lampMapTexture, noiseTex, blobTex } from './core.js';
import { stepExtras } from './extras.js';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
import { clamp, lerp } from '../util.js';
import { G, hour } from '../state.js';
import { lightState } from '../light.js';
import { town } from './town.js';
import { WATER } from '../map.js';

export const fx = { scale: 1, maxScale: 1.5, fade: 1, hurt: 0, light: 1, inside: false, fps: 60 };
let renderer,
  scene,
  camera,
  reflCam,
  reflRT,
  composer,
  bloom,
  grade,
  sky,
  sun,
  hemi,
  fill,
  rain,
  water,
  gulls = [],
  blobs,
  roomLight;
const QUAL = {
  low: { refl: 0, bloom: false, rain: 1200, cap: 1, msaa: 0 },
  medium: { refl: 0.4, bloom: true, rain: 2600, cap: 1.25, msaa: 0 },
  high: { refl: 0.5, bloom: true, rain: 4200, cap: 1.5, msaa: 4 },
};
const col = (h) => new THREE.Color(h);
const C = {
  topD: col('#77828c'),
  topK: col('#3a3350'),
  topN: col('#04060a'),
  horD: col('#a9aeac'),
  horK: col('#b06f52'),
  horN: col('#0d0b0a'),
  sunD: col('#e4eaee'),
  sunK: col('#ffac74'),
  sunN: col('#6a80a8'),
  hsD: col('#c2ccd4'),
  hsN: col('#28324a'),
  hgD: col('#57524b'),
  hgN: col('#15110f'),
};
const tmp = new THREE.Color(),
  tmp2 = new THREE.Color();

export function initRenderer(cv) {
  renderer = new THREE.WebGLRenderer({ canvas: cv, antialias: false, powerPreference: 'high-performance' });
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x8a8f90, 0.006);
  camera = new THREE.PerspectiveCamera(56, 1.6, 0.2, 620);
  camera.layers.enable(1);
  reflCam = new THREE.PerspectiveCamera(56, 1.6, 0.2, 700);
  lampMapTexture();
  noiseTex();
  hemi = new THREE.HemisphereLight(0xc2ccd4, 0x57524b, 1);
  scene.add(hemi);
  sun = new THREE.DirectionalLight(0xe4eaee, 1);
  sun.position.set(-60, 90, 40);
  scene.add(sun);
  fill = new THREE.PointLight(0x7088b0, 0, 16, 1.6);
  scene.add(fill);
  roomLight = new THREE.PointLight(0xffd9a0, 0, 30, 1.0);
  scene.add(roomLight);
  // sky
  sky = new THREE.Mesh(
    new THREE.SphereGeometry(560, 24, 14),
    new THREE.ShaderMaterial({
      side: THREE.BackSide,
      depthWrite: false,
      fog: false,
      uniforms: {
        cTop: { value: col('#77828c') },
        cHor: { value: col('#a9aeac') },
        cGlow: { value: new THREE.Color(1.0, 0.42, 0.12) },
        uGlow: { value: 0 },
        uDusk: { value: 0 },
        uTime: U.uTime,
        tNoise: U.tNoise,
      },
      vertexShader:
        'varying vec3 vD; void main(){ vD = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
      fragmentShader: `uniform vec3 cTop; uniform vec3 cHor; uniform vec3 cGlow; uniform float uGlow; uniform float uDusk; uniform float uTime; uniform sampler2D tNoise; varying vec3 vD;
      void main(){ vec3 d = normalize(vD); float h = max(d.y, 0.0); vec3 c = mix(cHor, cTop, pow(h, 0.5));
        vec2 p = d.xz / (h + 0.18), u1 = p * 0.07 + vec2(uTime * 0.0016, uTime * 0.0006), u2 = p * 0.19 + vec2(uTime * 0.0042, -uTime * 0.0011);
        float lo = texture2D(tNoise, u1).r * 0.55 + texture2D(tNoise, u1 * 2.3 + 0.37).g * 0.3 + texture2D(tNoise, u1 * 5.1).b * 0.15;      // the high deck, slow
        float hi = texture2D(tNoise, u2).g * 0.6 + texture2D(tNoise, u2 * 2.9 + 0.11).r * 0.4;                                             // low scud, quicker
        float cl = smoothstep(0.3, 0.75, lo), sc = smoothstep(0.5, 0.8, hi) * 0.55;
        c *= 0.66 + 0.52 * lo; c = mix(c, c * 0.6, sc); c += (cHor - c) * 0.25 * cl * (1.0 - h);
        float west = max(dot(normalize(d.xz + 1e-4), vec2(-0.86, 0.5)), 0.0);      // the sun goes down over the land, up-river
        c += uDusk * vec3(1.0, 0.45, 0.2) * pow(1.0 - h, 5.0) * pow(west, 3.0) * (0.35 + 0.9 * lo); c += uDusk * vec3(0.5, 0.2, 0.25) * sc * 0.25 * west;
        c += cGlow * uGlow * pow(1.0 - h, 7.0) * (0.5 + 0.7 * lo);
        gl_FragColor = vec4(c, 1.0); }`,
    }),
  );
  sky.renderOrder = -10;
  sky.frustumCulled = false;
  scene.add(sky);
  // the river and the cut
  const wm = new THREE.ShaderMaterial({
    fog: true,
    uniforms: THREE.UniformsUtils.merge([THREE.UniformsLib.fog, { cSky: { value: col('#8a9096') } }]),
    vertexShader:
      '#include <fog_pars_vertex>\nvarying vec3 vWp; void main(){ vec4 wp = modelMatrix * vec4(position,1.0); vWp = wp.xyz; vec4 mvPosition = viewMatrix * wp; gl_Position = projectionMatrix * mvPosition;\n#include <fog_vertex>\n}',
    fragmentShader: `#include <fog_pars_fragment>
      uniform vec3 cSky; uniform float uTime; uniform sampler2D tNoise; uniform sampler2D uLampMap; uniform vec2 uLampOrg; uniform vec2 uLampInv; uniform vec4 uLampOn; uniform vec3 uSodium; varying vec3 vWp;
      void main(){ vec2 n = (texture2D(tNoise, vWp.xz * 0.045 + vec2(uTime * 0.011, uTime * 0.017)).rg - 0.5) + (texture2D(tNoise, vWp.xz * 0.16 - vec2(uTime * 0.021, uTime * 0.013)).ba - 0.5) * 0.6;
        vec3 V = normalize(cameraPosition - vWp); float fres = 0.03 + 0.97 * pow(1.0 - max(V.y, 0.0), 4.0);
        vec3 c = mix(vec3(0.010, 0.017, 0.018), cSky, clamp(fres * 0.8 + n.x * 0.25, 0.0, 1.0));
        float dq = max(vWp.z - 62.0, 0.0);
        float lamp = texture2D(uLampMap, (vec2(vWp.x + n.x * (5.0 + dq * 0.35), 49.0 + n.y * 3.0) - uLampOrg) * uLampInv).r * uLampOn.x;
        c += uSodium * lamp * exp(-dq * 0.03) * (0.5 + 1.6 * max(n.y + 0.2, 0.0)) * step(0.0, vWp.z) * 1.5;
        float sw = texture2D(tNoise, vWp.xz * 0.42 + vec2(uTime * 0.05, -uTime * 0.035)).r; c += cSky * pow(sw, 6.0) * 0.5 * fres;      // glints on the chop
        float far = smoothstep(120.0, 300.0, vWp.z); c += uSodium * uLampOn.x * far * smoothstep(0.55, 0.85, texture2D(tNoise, vec2(vWp.x * 0.0035, 0.21)).g) * (0.3 + 0.7 * texture2D(tNoise, vWp.xz * vec2(0.02, 0.004) + uTime * 0.01).b) * 0.9;      // the far bank's lamps, drawn out across the river
        gl_FragColor = vec4(c, 1.0);
        #include <fog_fragment>
      }`,
  });
  for (const k of ['uTime', 'tNoise', 'uLampMap', 'uLampOrg', 'uLampInv', 'uLampOn', 'uSodium'])
    wm.uniforms[k] = U[k];
  water = new THREE.Group();
  for (const w of WATER) {
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry(w.x1 - w.x0 + 600, w.n === 'river' ? 700 : w.z1 - w.z0),
      wm,
    );
    m.rotation.x = -Math.PI / 2;
    m.position.set((w.x0 + w.x1) / 2, -1.55, w.n === 'river' ? w.z0 + 350 : (w.z0 + w.z1) / 2);
    m.layers.set(1);
    water.add(m);
  }
  scene.add(water);
  fx.waterMat = wm;
  // blob shadows
  blobs = new THREE.InstancedMesh(
    new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2),
    new THREE.MeshBasicMaterial({
      map: blobTex(),
      transparent: true,
      depthWrite: false,
      polygonOffset: true,
      polygonOffsetFactor: -4,
      polygonOffsetUnits: -4,
    }),
    140,
  );
  blobs.layers.set(1);
  blobs.frustumCulled = false;
  blobs.count = 0;
  scene.add(blobs);
  for (let i = 0; i < 12; i++) gulls.push(mkGull());
  setQuality(G.settings.quality);
  return { renderer, scene, camera };
}
function mkGull() {
  const g = new THREE.Group(),
    m = new THREE.MeshBasicMaterial({ color: 0xd8d8d2, side: THREE.DoubleSide, fog: true });
  const wing = () => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute(
      'position',
      new THREE.Float32BufferAttribute([0, 0, -0.12, 0.75, 0, -0.02, 0, 0, 0.14], 3),
    );
    return new THREE.Mesh(geo, m);
  };
  const l = wing(),
    r = wing();
  r.scale.x = -1;
  const body = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.4, 5).rotateX(Math.PI / 2), m);
  g.add(l, r, body);
  scene.add(g);
  return {
    g,
    l,
    r,
    cx: 20 + Math.random() * 80 - 40,
    cz: 58 + Math.random() * 30,
    rad: 8 + Math.random() * 22,
    h: 10 + Math.random() * 16,
    sp: 0.25 + Math.random() * 0.3,
    ph: Math.random() * 6.3,
    dir: Math.random() < 0.5 ? 1 : -1,
  };
}
function mkRain(n) {
  if (rain) {
    scene.remove(rain);
    rain.geometry.dispose();
  }
  const pos = new Float32Array(n * 6),
    end = new Float32Array(n * 2);
  for (let i = 0; i < n; i++) {
    const x = Math.random() * 44,
      y = Math.random() * 20,
      z = Math.random() * 44;
    pos.set([x, y, z, x, y, z], i * 6);
    end[i * 2] = 0;
    end[i * 2 + 1] = 1;
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setAttribute('aEnd', new THREE.BufferAttribute(end, 1));
  const m = new THREE.ShaderMaterial({
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    uniforms: {
      uCam: { value: new THREE.Vector3() },
      uAmt: { value: 0.3 },
      uTime: U.uTime,
      uLampMap: U.uLampMap,
      uLampOrg: U.uLampOrg,
      uLampInv: U.uLampInv,
      uLampOn: U.uLampOn,
      uSodium: U.uSodium,
      uDay: { value: 1 },
    },
    vertexShader: `attribute float aEnd; uniform vec3 uCam; uniform float uTime; uniform float uAmt; uniform sampler2D uLampMap; uniform vec2 uLampOrg; uniform vec2 uLampInv; uniform vec4 uLampOn; varying float vA; varying float vL;
      void main(){ vec3 p = position; float sp = 17.0 + fract(p.x * 7.13) * 7.0; p.y = mod(p.y - uTime * sp, 20.0); p.xz = mod(p.xz - uCam.xz + 22.0, 44.0) - 22.0 + uCam.xz; p.y += uCam.y - 7.0;
        p += vec3(0.05, 1.0, 0.02) * aEnd * (0.35 + 0.5 * uAmt); vL = texture2D(uLampMap, (p.xz - uLampOrg) * uLampInv).r * uLampOn.x * (1.0 - smoothstep(3.0, 9.0, p.y));
        vA = (1.0 - aEnd * 0.6) * step(fract(position.z * 3.7), uAmt * 1.05); gl_Position = projectionMatrix * viewMatrix * vec4(p, 1.0); }`,
    fragmentShader:
      'uniform vec3 uSodium; uniform float uDay; varying float vA; varying float vL; void main(){ vec3 c = vec3(0.55,0.6,0.66) * (0.05 + 0.2 * uDay) + uSodium * vL * 0.9; gl_FragColor = vec4(c * vA, 1.0); }',
  });
  rain = new THREE.LineSegments(g, m);
  rain.frustumCulled = false;
  rain.layers.set(1);
  scene.add(rain);
}
export function setQuality(q) {
  const Q = QUAL[q] || QUAL.high;
  fx.Q = Q;
  fx.maxScale = Math.min(window.devicePixelRatio || 1, Q.cap);
  fx.scale = Math.min(fx.scale, fx.maxScale);
  mkRain(Q.rain);
  U.uReflOn.value = Q.refl ? 1 : 0;
  resize(true);
}
export function resize(rebuild) {
  const w = window.innerWidth,
    h = window.innerHeight;
  renderer.setPixelRatio(fx.scale);
  renderer.setSize(w, h, false);
  camera.aspect = reflCam.aspect = w / h;
  camera.updateProjectionMatrix();
  const pw = Math.max(2, Math.floor(w * fx.scale)),
    ph = Math.max(2, Math.floor(h * fx.scale));
  if (rebuild || !composer) {
    if (composer) composer.dispose();
    const rt = new THREE.WebGLRenderTarget(pw, ph, { type: THREE.HalfFloatType, samples: fx.Q.msaa });
    composer = new EffectComposer(renderer, rt);
    composer.addPass(new RenderPass(scene, camera));
    bloom = new UnrealBloomPass(new THREE.Vector2(pw, ph), 0.5, 0.55, 0.92);
    bloom.enabled = fx.Q.bloom && G.settings.bloom;
    composer.addPass(bloom);
    composer.addPass(new OutputPass());
    grade = new ShaderPass({
      uniforms: {
        tDiffuse: { value: null },
        uTime: { value: 0 },
        uHurt: { value: 0 },
        uFade: { value: 1 },
        uNight: { value: 0 },
        uLight: { value: 1 },
      },
      vertexShader:
        'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
      fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime; uniform float uHurt; uniform float uFade; uniform float uNight; uniform float uLight; varying vec2 vUv;
        void main(){ vec3 c = texture2D(tDiffuse, vUv).rgb; float l = dot(c, vec3(0.299, 0.587, 0.114));
          c = mix(vec3(l), c, 0.88); c *= mix(vec3(0.965, 1.0, 1.05), vec3(1.07, 0.99, 0.88), uNight); c += vec3(-0.010, 0.004, 0.016) * (1.0 - l); c += vec3(0.028, 0.010, -0.02) * smoothstep(0.45, 1.0, l);
          vec2 q = vUv - 0.5; float vd = length(q * vec2(1.0, 1.12)); float vig = smoothstep(mix(0.70, 1.04, uLight), mix(0.13, 0.34, uLight), vd); c *= mix(mix(0.20, 0.74, uLight) - 0.07 * uNight, 1.0, vig);
          float g = fract(sin(dot(vUv * vec2(1920.0, 1080.0) + uTime * 61.0, vec2(12.9898, 78.233))) * 43758.5453); c += (g - 0.5) * 0.04;
          c = mix(c, vec3(0.22, 0.0, 0.0), uHurt * (1.0 - vig) * 0.85); gl_FragColor = vec4(c * uFade, 1.0); }`,
    });
    composer.addPass(grade);
    if (reflRT) reflRT.dispose();
    reflRT = fx.Q.refl
      ? new THREE.WebGLRenderTarget(
          Math.max(2, Math.floor(pw * fx.Q.refl)),
          Math.max(2, Math.floor(ph * fx.Q.refl)),
          { type: THREE.HalfFloatType },
        )
      : null;
    U.tRefl.value = reflRT ? reflRT.texture : null;
  }
  composer.setPixelRatio(1);
  composer.setSize(pw, ph);
  if (reflRT)
    reflRT.setSize(Math.max(2, Math.floor(pw * fx.Q.refl)), Math.max(2, Math.floor(ph * fx.Q.refl)));
}
export function setInside(room) {
  fx.inside = !!room;
  U.uInside.value = room ? 1 : 0;
  if (room) {
    roomLight.position.set(room.ox, 2.9, room.oz + 0.6);
    roomLight.intensity = 34;
    roomLight.color.set(
      room.k === 'chapel' ? '#ffe2b0' : room.k === 'fish' || room.k === 'laund' ? '#e8f0ff' : '#ffd9a0',
    );
  } else roomLight.intensity = 0;
}
const mat4 = new THREE.Matrix4(),
  v3 = new THREE.Vector3(),
  bias = new THREE.Matrix4().set(0.5, 0, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0, 0.5, 0.5, 0, 0, 0, 1);
let blankTex = null;
function renderReflection() {
  if (!reflRT || fx.inside) {
    U.uReflOn.value = 0;
    return;
  }
  U.uReflOn.value = 1;
  camera.getWorldDirection(v3);
  reflCam.position.set(camera.position.x, -camera.position.y, camera.position.z);
  reflCam.up.set(0, -1, 0);
  reflCam.lookAt(
    camera.position.x + v3.x * 10,
    -(camera.position.y + v3.y * 10),
    camera.position.z + v3.z * 10,
  );
  reflCam.fov = camera.fov;
  reflCam.updateProjectionMatrix();
  reflCam.updateMatrixWorld();
  U.uReflMat.value
    .copy(bias)
    .multiply(reflCam.projectionMatrix)
    .multiply(mat4.copy(reflCam.matrixWorld).invert());
  // the wet ground samples this target, so it must not be bound while the target is being drawn (no feedback loop)
  const keep = U.tRefl.value;
  U.tRefl.value = blankTex || (blankTex = new THREE.DataTexture(new Uint8Array([0, 0, 0, 255]), 1, 1));
  blankTex.needsUpdate = !blankTex.version;
  U.uReflOn.value = 0;
  fx.reflPass = true;
  const old = renderer.getRenderTarget();
  renderer.setRenderTarget(reflRT);
  renderer.clear();
  renderer.render(scene, reflCam);
  renderer.setRenderTarget(old);
  U.tRefl.value = keep;
  U.uReflOn.value = 1;
  fx.reflPass = false;
}
const dummy = new THREE.Object3D();
export function setBlobs(list) {
  let i = 0;
  for (const b of list) {
    if (i >= 140) break;
    dummy.position.set(b[0], b[1] + 0.03, b[2]);
    dummy.scale.set(b[3], 1, b[4] || b[3]);
    dummy.rotation.y = b[5] || 0;
    dummy.updateMatrix();
    blobs.setMatrixAt(i++, dummy.matrix);
  }
  blobs.count = i;
  blobs.instanceMatrix.needsUpdate = true;
}

let acc = 0,
  frames = 0,
  cool = 0;
export function frame(dt, t) {
  const s = lightState(),
    h = hour(),
    n = s.n,
    w = G.weather,
    ins = fx.inside;
  const dusk = Math.exp(-Math.pow((h - 18.0) / 0.85, 2)) + Math.exp(-Math.pow((h - 7.0) / 0.8, 2)) * 0.8;
  U.uTime.value = t;
  U.uWet.value = w.wet;
  U.uRain.value = w.rain;
  U.uNight.value = n;
  U.uLampOn.value.set(s.on, s.on, s.late, s.early);
  U.uFerry.value.w = s.ferry ? 0 : 1;
  const gloom = clamp(w.rain * 0.5 + w.mist * 0.3, 0, 0.5);
  U.uWinLevel.value =
    n * (h >= 16.5 && h < 22.5 ? 0.62 : h >= 22.5 || h < 0.5 ? 0.3 : h < 5.5 ? 0.05 : 0.42) +
    (1 - n) * 0.1 * gloom;
  U.uShopLit.value.set(
    h >= 8 && h < 17.6 ? 0.07 + 0.93 * Math.max(n, gloom * 0.25) : 0,
    h >= 16.5 && h < 23.6 ? 0.2 + 0.8 * n : 0,
    h >= 8.5 || h < 0.6 ? 0.14 + 0.86 * n : 0,
  );
  // sky, fog, sun
  const top = sky.material.uniforms.cTop.value
      .copy(C.topD)
      .lerp(C.topN, n)
      .lerp(C.topK, dusk * 0.6),
    hor = sky.material.uniforms.cHor.value
      .copy(C.horD)
      .lerp(C.horN, n)
      .lerp(C.horK, dusk * 0.7);
  top.multiplyScalar(1 - 0.25 * w.rain * (1 - n));
  sky.material.uniforms.uGlow.value = n * 0.16;
  sky.material.uniforms.uDusk.value = dusk * (1 - 0.5 * w.rain);
  scene.fog.color.copy(hor).lerp(tmp.set(0x1c1510), n * 0.5);
  scene.fog.density = ins ? 0 : 0.0042 + w.mist * 0.011 + w.rain * 0.0035 + n * 0.0015;
  fx.waterMat.uniforms.cSky.value.copy(hor).multiplyScalar(0.8);
  sun.color
    .copy(C.sunD)
    .lerp(C.sunN, n)
    .lerp(C.sunK, dusk * 0.7);
  sun.intensity = ins ? 0.3 : lerp(2.9, 0.22, n) * (1 - 0.25 * w.rain);
  const sa = ((h - 6) / 12) * Math.PI;
  sun.position.set(
    camera.position.x - Math.cos(sa) * 80,
    40 + Math.max(0, Math.sin(sa)) * 70,
    camera.position.z + 50,
  );
  sun.target.position.copy(camera.position);
  sun.target.updateMatrixWorld();
  hemi.color.copy(C.hsD).lerp(C.hsN, n);
  hemi.groundColor.copy(C.hgD).lerp(C.hgN, n);
  hemi.intensity = ins ? 2.3 : lerp(3.1, 0.62, n);
  if (ins) {
    hemi.color.set(0xd8cdb8);
    hemi.groundColor.set(0x4a4038);
  }
  fill.intensity = ins ? 0 : n * 5;
  fill.position.copy(camera.position);
  fill.position.y += 1.5;
  stepExtras(dt, t, n, w, h, hor, scene.fog.color, camera, ins);
  renderer.toneMappingExposure = ins ? 1.05 : lerp(0.92, 1.08, n);
  sky.position.copy(camera.position);
  sky.visible = !ins;
  water.visible = !ins;
  // rain
  rain.visible = !ins && w.rain > 0.03;
  rain.material.uniforms.uCam.value.copy(camera.position);
  rain.material.uniforms.uAmt.value = w.rain;
  rain.material.uniforms.uDay.value = 1 - n * 0.85;
  // lamps strike pink, then burn orange
  for (const hh of town.halos) {
    let on = s.on * (hh.l.ferry && !s.ferry ? 0 : 1);
    if (hh.l.dim) on *= Math.sin(t * 9 + hh.ph) > -0.86 ? 1 : 0.15;
    hh.s.visible = on > 0.02 && !ins;
    hh.s.material.opacity = on * 0.5;
    hh.s.scale.setScalar(hh.base * (1 + w.mist * 1.5 + w.rain * 0.4));
    tmp.setRGB(1.0, 0.25, 0.28).lerp(tmp2.setRGB(1.0, 0.5, 0.14), clamp(s.on * 1.6 - 0.5, 0, 1));
    hh.s.material.color.copy(tmp);
    hh.lens.material.color.setRGB(
      0.25 + 4.8 * on,
      0.2 + 2.0 * on * clamp(s.on * 1.6 - 0.3, 0.3, 1),
      0.15 + 0.4 * on,
    );
  }
  for (const b of town.blinkers)
    b.material.color.setRGB(...(Math.sin(t * 4.2) > 0 ? [3.2, 1.6, 0.2] : [0.5, 0.25, 0.05]));
  if (town.fire) {
    const on = h >= 18.5 || h < 6.6;
    town.fire.visible = on;
    town.fire.scale.set(1, 0.8 + Math.sin(t * 13) * 0.2 + Math.sin(t * 7.3) * 0.15, 1);
  }
  if (town.phoneGlow) town.phoneGlow.opacity = n * 0.35;
  if (town.stained)
    town.stained.emissiveIntensity = (h >= 7.2 && h < 9.2) || (h >= 16.8 && h < 19.2) ? 0.5 + n : 0;
  for (const id in town.winLights) {
    const P = G.people[id];
    town.winLights[id].visible = !!(P && P.space === 'home' && P.atWindow && P.winLit);
  }
  // the ferry comes in four times a day; the trawlers ride the swell
  const ft = [7.75, 12.25, 17.25, 22.3].map((a) => h - a).find((d) => d > -0.35 && d < 0.85);
  if (town.ferry) {
    const f = town.ferry;
    if (ft === undefined) f.visible = false;
    else {
      f.visible = !ins;
      const k = ft < 0 ? 1 + ft / 0.35 : ft > 0.6 ? 1 - (ft - 0.6) / 0.25 : 1;
      f.position.x = -55 - (1 - clamp(k, 0, 1)) * 140;
      f.position.y = -1.0 + Math.sin(t * 0.7) * 0.06;
      if (town.ferryLights) town.ferryLights.color.setRGB(0.3 + 1.6 * n, 0.3 + 1.3 * n, 0.3 + 0.7 * n);
    }
  }
  for (const b of town.boats) {
    b.position.y = b.userData.y + Math.sin(t * 0.8 + b.userData.ph) * 0.07;
    b.rotation.z = Math.sin(t * 0.6 + b.userData.ph) * 0.025;
  }
  for (const g of gulls) {
    const vis = n < 0.6 && !ins;
    g.g.visible = vis;
    if (!vis) continue;
    g.ph += dt * g.sp * g.dir;
    const x = g.cx + Math.cos(g.ph) * g.rad,
      z = g.cz + Math.sin(g.ph) * g.rad * 0.7,
      y = g.h + Math.sin(g.ph * 2.3) * 2;
    g.g.position.set(x, y, z);
    g.g.rotation.y = -g.ph + (g.dir > 0 ? Math.PI : 0);
    const fl = Math.sin(t * 7 + g.rad) * 0.5 * (Math.sin(g.ph * 1.7) > 0.2 ? 1 : 0.15);
    g.l.rotation.z = fl;
    g.r.rotation.z = -fl;
    g.g.rotation.z = 0.25 * g.dir;
  }
  if (bloom) {
    bloom.enabled = fx.Q.bloom && G.settings.bloom;
    bloom.strength = ins ? 0.22 : 0.3 + n * 0.22 + w.mist * 0.12;
  }
  grade.uniforms.uTime.value = t;
  grade.uniforms.uHurt.value = fx.hurt;
  grade.uniforms.uFade.value = fx.fade;
  grade.uniforms.uNight.value = n;
  grade.uniforms.uLight.value = fx.light;
  renderReflection();
  composer.render(dt);
  // hold the frame rate by trading resolution
  acc += dt;
  frames++;
  cool -= dt;
  if (acc >= 0.6) {
    const avg = acc / frames;
    fx.fps = 1 / avg;
    acc = 0;
    frames = 0;
    if (G.settings.autoRes && cool <= 0) {
      let sc = fx.scale;
      if (avg > 1 / 44) sc -= 0.09;
      else if (avg < 1 / 57 && sc < fx.maxScale) sc += 0.05;
      sc = clamp(sc, 0.5, fx.maxScale);
      if (Math.abs(sc - fx.scale) > 0.02) {
        fx.scale = sc;
        resize(false);
        cool = 1.2;
      }
    }
  }
}
// Draw a run of frames back to back and wait for the card each time: the true cost of a frame on this machine.
export function benchmark(n = 40) {
  const gl = renderer.getContext(),
    px = new Uint8Array(4),
    auto = G.settings.autoRes,
    was = fx.scale;
  G.settings.autoRes = false;
  let bt = performance.now() / 1000;
  if (fx.scale !== fx.maxScale) {
    fx.scale = fx.maxScale;
    resize(false);
  } // measured at full resolution, whatever the automatic scale had settled on
  const one = () => {
    frame(1 / 60, (bt += 1 / 60));
    gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
  };
  one();
  one();
  renderer.info.autoReset = false;
  renderer.info.reset();
  one();
  const calls = renderer.info.render.calls,
    tris = renderer.info.render.triangles;
  renderer.info.autoReset = true;
  const t0 = performance.now();
  for (let i = 0; i < n; i++) one();
  const ms = (performance.now() - t0) / n,
    w = renderer.domElement.width,
    h = renderer.domElement.height;
  G.settings.autoRes = auto;
  if (was !== fx.scale) {
    fx.scale = was;
    resize(false);
  }
  const dbg = gl.getExtension('WEBGL_debug_renderer_info');
  return {
    ms,
    calls,
    tris,
    w,
    h,
    gpu: dbg ? String(gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL)) : 'unknown card',
  };
}
export const gfx = () => ({ renderer, scene, camera });
