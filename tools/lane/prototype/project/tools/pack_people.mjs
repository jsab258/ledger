// Packs Quaternius' Universal Base Characters (CC0) and Universal Animation Library (CC0) into one compact file for LEDGER.
// Bodies, eyes, brows and hair keep their shapes; the skeleton is reduced to 23 bones (fingers are baked into a relaxed hand);
// the clips are resampled for those bones. Clothes are not in the file: the game tailors them from the body at run time.
// usage: node pack_people.mjs <ubc dir> <anims.txt> <out dir>
import fs from 'fs'; import path from 'path'; import * as THREE from 'three';
const [UBC, ANIMS, OUT] = process.argv.slice(2);
export const KEEP = ['root', 'pelvis', 'spine_01', 'spine_02', 'spine_03', 'neck_01', 'Head', 'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l', 'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r', 'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r'];
const CLIPS = ['Idle_Loop', 'Walk_Loop', 'Walk_Formal_Loop', 'Jog_Fwd_Loop', 'Sprint_Loop', 'Idle_Talking_Loop', 'Sitting_Idle_Loop', 'Driving_Loop', 'Interact', 'Push_Loop', 'Crouch_Idle_Loop', 'Punch_Jab', 'Punch_Cross', 'Hit_Head', 'Hit_Chest', 'Death01', 'Roll'];
const CT = { 5120: Int8Array, 5121: Uint8Array, 5122: Int16Array, 5123: Uint16Array, 5125: Uint32Array, 5126: Float32Array }, CN = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16 };
function reader(j, bin) {
  return (i) => {
    const a = j.accessors[i], bv = j.bufferViews[a.bufferView], n = CN[a.type], C = CT[a.componentType], off = bin.byteOffset + (bv.byteOffset || 0) + (a.byteOffset || 0), sz = C.BYTES_PER_ELEMENT, stride = bv.byteStride || n * sz;
    const out = new Float64Array(a.count * n), dv = new DataView(bin.buffer, off);
    const get = { 5120: 'getInt8', 5121: 'getUint8', 5122: 'getInt16', 5123: 'getUint16', 5125: 'getUint32', 5126: 'getFloat32' }[a.componentType];
    const k = a.normalized ? (a.componentType === 5121 ? 1 / 255 : a.componentType === 5123 ? 1 / 65535 : 1) : 1;
    for (let e = 0; e < a.count; e++) for (let c = 0; c < n; c++) out[e * n + c] = dv[get](e * stride + c * sz, true) * k;
    return out;
  };
}
function loadGltf(file) { const j = JSON.parse(fs.readFileSync(file, 'utf8')); return { j, acc: reader(j, fs.readFileSync(path.join(path.dirname(file), j.buffers[0].uri))) }; }
function loadGlbText(file) { let b = Buffer.from(fs.readFileSync(file, 'latin1'), 'base64'); const jl = b.readUInt32LE(12), j = JSON.parse(b.slice(20, 20 + jl).toString('utf8')); const bin = b.slice(20 + jl + 8); return { j, acc: reader(j, bin) }; }
// rest skeleton of a file: local TRS by bone name, parent names
function skeletonOf(j) {
  const par = {}; j.nodes.forEach((n, i) => (n.children || []).forEach((c) => { par[c] = i; }));
  const sk = {}; j.nodes.forEach((n, i) => { sk[n.name] = { name: n.name, parent: par[i] !== undefined ? j.nodes[par[i]].name : null, t: n.translation || [0, 0, 0], r: n.rotation || [0, 0, 0, 1], s: n.scale || [1, 1, 1] }; });
  return sk;
}
const keepOf = (name) => { if (KEEP.includes(name)) return name; const m = name.match(/^(thumb|index|middle|ring|pinky)_.*_(l|r)$/); if (m) return 'hand_' + m[2]; const b = name.match(/^ball_leaf_(l|r)$/); if (b) return 'ball_' + b[1]; return null; };
const M4 = (b) => new THREE.Matrix4().compose(new THREE.Vector3(...b.t), new THREE.Quaternion(...b.r), new THREE.Vector3(...b.s));
function worlds(sk, localOf = (b) => M4(b)) { const W = {}; const w = (n) => { if (W[n]) return W[n]; const b = sk[n]; const m = localOf(b); W[n] = b.parent && sk[b.parent] ? w(b.parent).clone().multiply(m) : m; return W[n]; }; for (const n in sk) w(n); return W; }

const anims = loadGlbText(ANIMS), skU = skeletonOf(anims.j);
// the idle clip's first frame gives a relaxed finger pose to bake into the hands
const fingerPose = {}; { const a = anims.j.animations.find((x) => x.name === 'Walk_Loop'); for (const ch of a.channels) { const nm = anims.j.nodes[ch.target.node].name; if (ch.target.path === 'rotation' && /^(thumb|index|middle|ring|pinky)_/.test(nm)) { const o = anims.acc(a.samplers[ch.sampler].output); const r = new THREE.Quaternion(...skU[nm].r).slerp(new THREE.Quaternion(o[0], o[1], o[2], o[3]), /^thumb/.test(nm) ? 0.3 : 0.42); fingerPose[nm] = [r.x, r.y, r.z, r.w]; } } }

function mesh(g, nodeName) {
  const { j, acc } = g, node = j.nodes.find((n) => n.name === nodeName && n.mesh !== undefined); if (!node) throw new Error('no mesh ' + nodeName);
  const p = j.meshes[node.mesh].primitives[0], joints = j.skins[node.skin].joints.map((i) => j.nodes[i].name);
  const pos = acc(p.attributes.POSITION), nor = acc(p.attributes.NORMAL), uv = acc(p.attributes.TEXCOORD_0), ji = acc(p.attributes.JOINTS_0), jw = acc(p.attributes.WEIGHTS_0), idx = acc(p.indices), n = pos.length / 3;
  return { n, pos, nor, uv, ji, jw, idx, joints };
}
// skin a mesh's fingers into the relaxed pose, then fold every finger weight into the hand bone
function reduce(m, sk) {
  const rest = worlds(sk), posed = worlds(sk, (b) => { const fp = fingerPose[b.name]; if (!fp) return M4(b); const u = skU[b.name], C = new THREE.Quaternion(...b.r).multiply(new THREE.Quaternion(...u.r).invert()); return new THREE.Matrix4().compose(new THREE.Vector3(...b.t), C.multiply(new THREE.Quaternion(...fp)), new THREE.Vector3(1, 1, 1)); });
  const skinM = {}; for (const n in sk) skinM[n] = posed[n].clone().multiply(rest[n].clone().invert());
  const N = m.n, pos = new Float32Array(N * 3), nor = new Float32Array(N * 3), bi = new Uint8Array(N * 4), bw = new Float32Array(N * 4), v = new THREE.Vector3(), acc = new THREE.Vector3(), nv = new THREE.Vector3(), nacc = new THREE.Vector3();
  for (let i = 0; i < N; i++) {
    const w = {}; let fing = false; acc.set(0, 0, 0); nacc.set(0, 0, 0);
    for (let k = 0; k < 4; k++) { const wt = m.jw[i * 4 + k]; if (wt <= 0) continue; const name = m.joints[m.ji[i * 4 + k]]; if (fingerPose[name]) fing = true; const kn = keepOf(name); if (!kn) throw new Error('unmapped bone ' + name); w[kn] = (w[kn] || 0) + wt;
      v.set(m.pos[i * 3], m.pos[i * 3 + 1], m.pos[i * 3 + 2]).applyMatrix4(skinM[name]); acc.addScaledVector(v, wt); nv.set(m.nor[i * 3], m.nor[i * 3 + 1], m.nor[i * 3 + 2]).transformDirection(skinM[name]); nacc.addScaledVector(nv, wt); }
    const tot = Object.values(w).reduce((a, b) => a + b, 0);
    if (fing) { acc.multiplyScalar(1 / tot); nacc.normalize(); pos.set([acc.x, acc.y, acc.z], i * 3); nor.set([nacc.x, nacc.y, nacc.z], i * 3); } else { pos.set(m.pos.subarray(i * 3, i * 3 + 3), i * 3); nor.set(m.nor.subarray(i * 3, i * 3 + 3), i * 3); }
    const e = Object.entries(w).sort((a, b) => b[1] - a[1]).slice(0, 4), t2 = e.reduce((a, b) => a + b[1], 0);
    e.forEach(([name, wt], k) => { bi[i * 4 + k] = KEEP.indexOf(name); bw[i * 4 + k] = wt / t2; });
  }
  return { n: N, pos, nor, uv: Float32Array.from(m.uv), bi, bw, idx: Uint32Array.from(m.idx) };
}

const bufs = [], dir = {}; let at = 0;
const put = (name, arr) => { const b = Buffer.from(arr.buffer, arr.byteOffset, arr.byteLength); dir[name] = [at, arr.length, arr.constructor.name]; bufs.push(b); at += b.length; const pad = (4 - at % 4) % 4; if (pad) { bufs.push(Buffer.alloc(pad)); at += pad; } };
const putMesh = (name, m, tex) => {
  put(name + '.pos', m.pos); const nq = new Int8Array(m.n * 3); for (let i = 0; i < m.n * 3; i++) nq[i] = Math.round(Math.max(-1, Math.min(1, m.nor[i])) * 127); put(name + '.nor', nq);
  { let a0 = 9, a1 = -9; for (let i = 0; i < m.n * 2; i++) { a0 = Math.min(a0, m.uv[i]); a1 = Math.max(a1, m.uv[i]); } if (a0 < -0.001 || a1 > 2.001) console.log('uv outside 0..1', name, a0.toFixed(3), a1.toFixed(3)); }
  const uq = new Uint16Array(m.n * 2); for (let i = 0; i < m.n * 2; i++) uq[i] = Math.round(Math.max(0, Math.min(2, m.uv[i])) * 32767.5); put(name + '.uv', uq);
  put(name + '.bi', m.bi); const wq = new Uint8Array(m.n * 4); for (let i = 0; i < m.n; i++) { let s = 0; for (let k = 0; k < 4; k++) { wq[i * 4 + k] = Math.round(m.bw[i * 4 + k] * 255); s += wq[i * 4 + k]; } wq[i * 4] += 255 - s; } put(name + '.bw', wq);
  put(name + '.idx', m.n < 65536 ? Uint16Array.from(m.idx) : m.idx); meshes[name] = { n: m.n, tris: m.idx.length / 3, tex };
};
const meshes = {}, rests = {};
const B = path.join(UBC, 'Base Characters'), H = path.join(UBC, 'Hairstyles', 'Rigged');
for (const [sex, file, bodyNode] of [['M', 'Superhero_Male_FullBody.gltf', 'SuperHero_Male'], ['F', 'Superhero_Female_FullBody.gltf', 'Superhero_Female']]) {
  const g = loadGltf(path.join(B, file)), sk = skeletonOf(g.j);
  rests[sex] = KEEP.map((n) => ({ name: n, parent: KEEP.indexOf(sk[n].parent), t: sk[n].t, r: sk[n].r }));
  putMesh(sex + '_body', reduce(mesh(g, bodyNode), sk), sex === 'M' ? 'skinM' : 'skinF');
  putMesh(sex + '_eyes', reduce(mesh(g, 'Eyes'), sk), 'eye');
  putMesh(sex + '_brows', reduce(mesh(g, 'Eyebrows'), sk), sex === 'M' ? 'hair1' : 'hair2');
}
// hair is rigged to the head of the body it was made for
for (const [name, file, sex, tex] of [['hair_parted', 'Hair_SimpleParted', 'M', 'hair1'], ['hair_buzz', 'Hair_Buzzed', 'M', 'hair1'], ['hair_beard', 'Hair_Beard', 'M', 'hair1'], ['hair_buzzf', 'Hair_BuzzedFemale', 'F', 'hair2'], ['hair_long', 'Hair_Long', 'F', 'hair2'], ['hair_buns', 'Hair_Buns', 'F', 'hair2']]) {
  const g = loadGltf(path.join(H, file + '.gltf')), sk = skeletonOf(g.j); putMesh(name, reduce(mesh(g, file), sk), tex); meshes[name].sex = sex;
}
// clips: 30 keys a second for the 23 bones, rotations as int16, pelvis travel as float
const clips = {}, ua = anims.j;
for (const name of CLIPS) {
  const a = ua.animations.find((x) => x.name === name); if (!a) throw new Error('no clip ' + name);
  const tracks = {}; let times = null, pel = null;
  for (const ch of a.channels) { const nm = ua.nodes[ch.target.node].name, s = a.samplers[ch.sampler]; if (ch.target.path === 'rotation' && KEEP.includes(nm)) { tracks[nm] = anims.acc(s.output); times = times || anims.acc(s.input); } else if (ch.target.path === 'translation' && nm === 'pelvis') pel = anims.acc(s.output); }
  const n = times.length, q = new Int16Array(n * KEEP.length * 4), p = new Float32Array(n * 3);
  for (let f = 0; f < n; f++) { KEEP.forEach((b, bi) => { const t = tracks[b], r = t ? [t[f * 4], t[f * 4 + 1], t[f * 4 + 2], t[f * 4 + 3]] : skU[b].r; for (let c = 0; c < 4; c++) q[(f * KEEP.length + bi) * 4 + c] = Math.round(r[c] * 32767); }); for (let c = 0; c < 3; c++) p[f * 3 + c] = pel ? pel[f * 3 + c] : skU.pelvis.t[c]; }
  put('clip.' + name + '.q', q); put('clip.' + name + '.p', p); clips[name] = { n, dur: times[n - 1] };
}
const head = { v: 1, bones: KEEP, rests, restU: KEEP.map((n) => ({ t: skU[n].t, r: skU[n].r })), meshes, clips, dir };
const js = Buffer.from(JSON.stringify(head)), pad = (4 - js.length % 4) % 4, hd = Buffer.alloc(8); hd.write('LGR1', 0); hd.writeUInt32LE(js.length + pad, 4);
const bin = Buffer.concat([hd, js, Buffer.alloc(pad, 32), ...bufs]);
fs.writeFileSync(path.join(OUT, 'people.bin'), bin); fs.writeFileSync(path.join(OUT, 'people.txt'), bin.toString('base64'));
console.log('people.bin', bin.length, 'txt', Math.round(bin.length * 4 / 3), 'meshes', Object.entries(meshes).map(([k, m]) => k + ':' + m.n + 'v/' + m.tris + 't').join(' '), 'clips', Object.keys(clips).length);
