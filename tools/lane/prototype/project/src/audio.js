// Sound made in the page: rain, the river, gulls, a ship's horn far off, the office radio, footsteps that carry at night, a sparse score.
import { G } from './state.js';
import { clamp, rnd, pick } from './util.js';
import { nightF, hourNoise } from './seeing.js';

const A = { ctx: null, room: null };
let master,
  amb,
  sfxBus,
  world,
  worldWet,
  mus,
  rev,
  rainG,
  rainF,
  seaG,
  humG,
  engO,
  engG,
  engF,
  noiseBuf,
  nextGull = 4,
  nextHorn = 30,
  nextNote = 3,
  nextPad = 1,
  stepT = 0,
  radioT = 6;
export function initAudio() {
  if (A.ctx) {
    if (A.ctx.state === 'suspended') A.ctx.resume();
    return;
  }
  try {
    A.ctx = new (window.AudioContext || window.webkitAudioContext)();
  } catch (e) {
    return;
  }
  const c = A.ctx;
  master = c.createGain();
  master.gain.value = G.settings.vol;
  master.connect(c.destination);
  amb = c.createBiquadFilter();
  amb.type = 'lowpass';
  amb.frequency.value = 18000;
  amb.connect(master);
  sfxBus = c.createGain();
  sfxBus.connect(master);
  world = c.createGain();
  world.connect(master);
  mus = c.createGain();
  mus.gain.value = G.settings.music * 0.5;
  mus.connect(master);
  // a plain reverb from decaying noise
  const len = c.sampleRate * 2.6,
    ir = c.createBuffer(2, len, c.sampleRate);
  for (let ch = 0; ch < 2; ch++) {
    const d = ir.getChannelData(ch);
    for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.6);
  }
  rev = c.createConvolver();
  rev.buffer = ir;
  const rg = c.createGain();
  rg.gain.value = 0.5;
  rev.connect(rg);
  rg.connect(master);
  worldWet = c.createGain();
  worldWet.gain.value = 0.1;
  world.connect(worldWet);
  worldWet.connect(rev);
  noiseBuf = c.createBuffer(1, c.sampleRate * 3, c.sampleRate);
  const nd = noiseBuf.getChannelData(0);
  for (let i = 0; i < nd.length; i++) nd[i] = Math.random() * 2 - 1;
  const loop = (type, freq, q) => {
    const s = c.createBufferSource();
    s.buffer = noiseBuf;
    s.loop = true;
    const f = c.createBiquadFilter();
    f.type = type;
    f.frequency.value = freq;
    f.Q.value = q;
    const g = c.createGain();
    g.gain.value = 0;
    s.connect(f);
    f.connect(g);
    g.connect(amb);
    s.start();
    return [g, f];
  };
  [rainG, rainF] = loop('bandpass', 5200, 0.5);
  [seaG] = loop('lowpass', 420, 0.3);
  [humG] = loop('lowpass', 150, 0.5);
  engO = c.createOscillator();
  engO.type = 'sawtooth';
  engF = c.createBiquadFilter();
  engF.type = 'lowpass';
  engF.frequency.value = 300;
  engG = c.createGain();
  engG.gain.value = 0;
  engO.connect(engF);
  engF.connect(engG);
  engG.connect(master);
  engO.start();
}
function env(g, t, a, peak, d) {
  g.gain.cancelScheduledValues(t);
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(peak, t + a);
  g.gain.exponentialRampToValueAtTime(0.0001, t + a + d);
}
function tone(type, f0, f1, dur, vol, o = {}) {
  const c = A.ctx,
    t = c.currentTime + (o.at || 0),
    os = c.createOscillator(),
    g = c.createGain();
  os.type = type;
  os.frequency.setValueAtTime(f0, t);
  if (f1) os.frequency.exponentialRampToValueAtTime(f1, t + dur);
  env(g, t, o.a || 0.01, vol, dur);
  os.connect(g);
  g.connect(o.dry === false ? rev : o.bus || sfxBus);
  if (o.wet) {
    const w = c.createGain();
    w.gain.value = o.wet;
    g.connect(w);
    w.connect(rev);
  }
  os.start(t);
  os.stop(t + dur + (o.a || 0.01) + 0.1);
}
function burst(freq, q, dur, vol, o = {}) {
  const c = A.ctx,
    t = c.currentTime + (o.at || 0),
    s = c.createBufferSource(),
    f = c.createBiquadFilter(),
    g = c.createGain();
  s.buffer = noiseBuf;
  s.loopStart = Math.random() * 2;
  f.type = o.type || 'bandpass';
  f.frequency.value = freq;
  f.Q.value = q;
  env(g, t, o.a || 0.004, vol, dur);
  s.connect(f);
  f.connect(g);
  g.connect(o.bus || sfxBus);
  if (o.wet) {
    const w = c.createGain();
    w.gain.value = o.wet;
    g.connect(w);
    w.connect(rev);
  }
  s.start(t, Math.random() * 2);
  s.stop(t + dur + 0.2);
}
export const MIX = []; // every sound asked for: { n: name, loud: 0..1, who?, at: real seconds played }
export function heard(n, loud = 0.5, who) {
  MIX.push({ n, loud: Math.round(loud * 100) / 100, who: who || '', at: Math.round(G.played * 100) / 100, t: Math.round(G.t * 10) / 10 });
  if (MIX.length > 4000) MIX.splice(0, 1000);
}
// A spoken line: every subtitle comes with its audio (a voice in the mix, as long as the line)
export function voice(who, text, loud = 0.6) {
  heard('voice', loud, who);
  if (!A.ctx) return;
  const n = Math.min(14, Math.max(2, Math.round(String(text).length / 9)));
  const base = 110 + ((String(who).length * 37) % 90);
  for (let i = 0; i < n; i++) tone('sawtooth', base + rnd(-14, 26), base + rnd(-20, 20), 0.09, 0.05 * loud, { at: i * 0.11, bus: world, a: 0.01 });
}
const LOUD = { tick: 0.03, paper: 0.07, stamp: 0.5, coin: 0.08, door: 0.35, cardoor: 0.5, shout: 0.6, thud: 0.5, hit: 0.6, block: 0.3, crash: 0.7, face: 0.07, radio: 0.14, step: 0.05, stair: 0.2 };
export function sfx(name, loud) {
  if (name !== 'tick') heard(name, loud == null ? LOUD[name] || 0.2 : loud);
  if (!A.ctx) return;
  if (name.startsWith('bell:')) {
    for (let i = 0; i < +name.slice(5); i++) tone('sine', 523, 0, 1.4, 0.12 * (loud || 0.5) * 2, { at: i * 1.1, bus: world, wet: 0.7 });
    return;
  }
  switch (name) {
    case 'tick':
      burst(3200, 3, 0.02, 0.03);
      break;
    case 'paper':
      burst(2400, 0.7, 0.16, 0.07);
      break;
    case 'stamp':
      tone('sine', 120, 50, 0.16, 0.5);
      burst(900, 1, 0.07, 0.12);
      break;
    case 'coin':
      tone('triangle', 2100, 0, 0.09, 0.08);
      tone('triangle', 2900, 0, 0.14, 0.07, { at: 0.06 });
      break;
    case 'cloth':
      burst(1800, 0.6, 0.12, 0.03);
      break;
    case 'ferryhorn':
      tone('sawtooth', 98, 92, 1.6, 0.35, { bus: world, a: 0.2 });
      break;
    case 'stair':
      for (let i = 0; i < 4; i++) tone('sine', 140, 80, 0.07, 0.2, { at: i * 0.24, bus: world });
      break;
    case 'door':
      tone('sine', 150, 70, 0.14, 0.35, { bus: world });
      burst(500, 1, 0.1, 0.12, { at: 0.02, bus: world });
      break;
    case 'cardoor':
      tone('sine', 120, 58, 0.11, 0.5, { bus: world });
      burst(380, 1.4, 0.07, 0.3, { bus: world });
      burst(2600, 2, 0.02, 0.08, { at: 0.05, bus: world });
      break;
    case 'shout':
      tone('sawtooth', 250, 170, 0.26, 0.2, { bus: world, a: 0.02 });
      tone('sawtooth', 505, 340, 0.22, 0.07, { bus: world, a: 0.02 });
      burst(1100, 2.2, 0.2, 0.2, { bus: world, type: 'bandpass' });
      break;
    case 'thud':
      tone('sine', 110, 45, 0.2, 0.5, { bus: world });
      break;
    case 'hit':
      tone('sine', 170, 55, 0.13, 0.6, { bus: world });
      burst(1300, 0.8, 0.08, 0.3, { bus: world });
      break;
    case 'block':
      burst(700, 1.2, 0.08, 0.3, { bus: world });
      tone('sine', 220, 120, 0.07, 0.2, { bus: world });
      break;
    case 'crash':
      burst(600, 0.4, 0.5, 0.7, { bus: world });
      tone('sawtooth', 160, 40, 0.4, 0.4, { bus: world });
      break;
    case 'face':
      tone('sine', 392, 0, 0.5, 0.07, { wet: 0.6 });
      tone('sine', 466, 0, 0.7, 0.06, { at: 0.16, wet: 0.6 });
      break;
    case 'radio':
      radio();
      break;
    case 'step':
      burst(G.weather.wet > 0.6 ? 1500 : 900, 1.1, 0.05, 0.05, { bus: world, type: 'bandpass' });
      break;
  }
}
function radio() {
  burst(2200, 2, 0.09, 0.14);
  for (let i = 0; i < 7; i++)
    tone('sawtooth', rnd(150, 240), rnd(140, 260), 0.1, 0.035, { at: 0.12 + i * 0.13, bus: sfxBus });
  burst(2200, 2, 0.06, 0.1, { at: 1.1 });
}
const SCALE = [146.83, 174.61, 196, 220, 261.63, 293.66, 349.23, 392, 440]; // D minor, mostly
export function audioStep(dt) {
  const c = A.ctx;
  if (!c) return;
  const t = G.tom,
    n = nightF(),
    w = G.weather,
    inside = t.space !== 'street',
    now = c.currentTime,
    title = G.story.phase === 'title';
  master.gain.setTargetAtTime(G.settings.vol, now, 0.2);
  mus.gain.setTargetAtTime(G.settings.music * (inside ? 0.3 : 0.5), now, 0.5);
  amb.frequency.setTargetAtTime(inside ? 700 : t.inCar ? 1800 : 18000, now, 0.2);
  // noise, said with sound alone: the same rule as the noise radius. Footsteps, a car door, a shout carry at night and in quiet
  // streets, and drown under rain and the noon street
  {
    const k = inside ? 0.8 : clamp(hourNoise() * (1 - 0.6 * w.rain), 0.2, 2);
    A.carry = k;
    world.gain.setTargetAtTime(0.34 + 0.62 * k, now, 0.4);
    worldWet.gain.setTargetAtTime(inside ? 0.05 : 0.07 * k * k, now, 0.4);
  }
  const quay = clamp(1 - Math.abs((t.inCar ? G.car.z : inside ? 0 : t.z) - 62) / 60, 0, 1);
  rainG.gain.setTargetAtTime(w.rain * 0.5 * (inside ? 0.5 : 1), now, 0.5);
  rainF.frequency.setTargetAtTime(3600 + w.rain * 3000, now, 0.5);
  seaG.gain.setTargetAtTime((0.05 + quay * 0.16) * (1 + Math.sin(now * 0.5) * 0.3), now, 0.4);
  humG.gain.setTargetAtTime(0.1 + n * 0.05 + (inside ? 0 : (2 - hourNoise()) * 0.035), now, 1);
  engG.gain.setTargetAtTime(t.inCar ? 0.055 : 0, now, 0.1);
  engO.frequency.setTargetAtTime(48 + Math.abs(G.car.v) * 9, now, 0.08);
  engF.frequency.setTargetAtTime(220 + Math.abs(G.car.v) * 50, now, 0.1);
  // gulls: a long falling cry answered now and then by a laughing run; thick on the quay, thin up the street, quiet after dark
  nextGull -= dt;
  if (nextGull <= 0) {
    const R = Math.random;
    nextGull = (3.5 + R() * 9) / (0.45 + quay);
    if (n < 0.65 && !inside) {
      const v = (0.07 + quay * 0.11) * (1 - n),
        far = 0.45 + R() * 0.55,
        p = 0.9 + R() * 0.25;
      if (R() < 0.62) {
        const k = 2 + Math.floor(R() * 3);
        for (let i = 0; i < k; i++) {
          const at = i * 0.62 + R() * 0.06,
            f = (1500 - i * 70) * p;
          tone('triangle', f * 0.62, f, 0.09, v * far, { at, a: 0.02, wet: 0.6, bus: amb });
          tone('triangle', f, f * 0.6, 0.46, v * far, { at: at + 0.085, a: 0.01, wet: 0.6, bus: amb });
          tone('sine', f * 2.02, f * 1.2, 0.4, v * far * 0.25, {
            at: at + 0.085,
            a: 0.01,
            wet: 0.6,
            bus: amb,
          });
        }
      } else {
        const k = 5 + Math.floor(R() * 5);
        for (let i = 0; i < k; i++) {
          const f = (1350 - i * 28) * p;
          tone('triangle', f, f * 0.78, 0.13, v * far * (1 - i / (k + 3)), {
            at: i * 0.17,
            a: 0.012,
            wet: 0.55,
            bus: amb,
          });
        }
      }
    }
  }
  nextHorn -= dt;
  if (nextHorn <= 0) {
    nextHorn = rnd(55, 140);
    if (!inside) {
      const two = Math.random() < 0.4 ? [0, 3.4] : [0];
      for (const at of two) {
        tone('sawtooth', 87, 86, 2.6, 0.065, { at, a: 0.5, dry: false });
        tone('sawtooth', 110, 109, 2.6, 0.05, { at, a: 0.5, dry: false });
      }
    }
  }
  if (t.space === 'mickeys' || t.inCar) {
    radioT -= dt;
    if (radioT <= 0) {
      radioT = rnd(9, 22);
      radio();
    }
  }
  // footsteps: listen at three in the morning and you will hear the rule
  if (!t.inCar && t.v > 0.4 && !title && t.space !== 'away') {
    stepT -= dt * (t.run ? 3.4 : 2.0);
    if (stepT <= 0) {
      stepT = 1;
      sfx('step');
    }
  }
  // the score: slow pads and a few low notes, more of it at night
  nextPad -= dt;
  if (nextPad <= 0) {
    nextPad = rnd(9, 16);
    const root = pick([73.42, 87.31, 65.41, 98]);
    for (const [m, d] of [
      [1, 0],
      [1.5, 4],
      [2.4, -5],
    ]) {
      const os = c.createOscillator(),
        g = c.createGain(),
        f = c.createBiquadFilter();
      os.type = 'sawtooth';
      os.frequency.value = root * m;
      os.detune.value = d;
      f.type = 'lowpass';
      f.frequency.value = 320 + n * 140;
      g.gain.setValueAtTime(0.0001, now);
      g.gain.linearRampToValueAtTime(0.045, now + 3.5);
      g.gain.linearRampToValueAtTime(0.0001, now + 11);
      os.connect(f);
      f.connect(g);
      g.connect(mus);
      g.connect(rev);
      os.start(now);
      os.stop(now + 11.5);
    }
  }
  nextNote -= dt;
  if (nextNote <= 0) {
    nextNote = rnd(2.5, 9) * (1.4 - n * 0.5);
    if (Math.random() < 0.75) {
      const f = pick(SCALE) * (Math.random() < 0.3 ? 0.5 : 1);
      tone('sine', f, 0, 2.2, 0.05, { bus: mus, wet: 0.9, a: 0.015 });
      tone('sine', f * 2, 0, 0.9, 0.012, { bus: mus, wet: 0.5, a: 0.01 });
      if (Math.random() < 0.35)
        tone('sine', f * 1.5, 0, 1.8, 0.03, { bus: mus, wet: 0.9, at: rnd(0.4, 0.9) });
    }
  }
}
