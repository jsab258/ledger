#!/usr/bin/env python3
"""Rebuild every sound of Quay Street (unit 10, cloud week 42) from the fetched CC0 sources.

    python fetch_sources.py            # once: the sources, outside the repository
    python make_sound.py               # writes WAVs to SOUND_OUT (default /home/user/ledger-scratch/sound-out)
                                       # and manifest.json beside this file
    python make_sound.py amb_wind      # only the outputs whose name starts with these
    python check_sound.py              # then the check (checks/check_v1.json)

Everything is deterministic: fixed cut points, seeded random numbers (gull calls placed, voices scrambled),
seeded dither. A second run gives byte-identical WAVs (the manifest holds each file's sha256).

What it makes (BRIEF.md says why, and what each must sound like):
  21 ambience loops, 75 s, 48 kHz 16 bit WAV: traffic, gulls, harbour, wind, voices through a window and a radio
     through a window, each in day, night and rain versions; the rain itself on pavement, on an awning and in
     a gutter (rain version only). Beds are stereo; point sources (gulls, voices, radio) and the mono pavement rain are mono.
  footsteps: 8 variants on each of paving, setts, asphalt, wet, wood (mono one-shots)
  one-shots: shop door (open, close, latch), house door (open, close, latch), the shop bell, the phone box (door creak,
     door shut, a telephone ringing)

Loops are seamless by construction: a bed's tail is crossfaded (equal power, 4 s) into its head, so the sample after
its last is the one that followed it in the source; point-source layers are mixed round a circle, so an event that
runs past the end continues at the start. Levels are set by measured gain (BS.1770-4 integrated loudness for loops,
the highest 400 ms momentary loudness for one-shots), never by a limiter.
"""
import hashlib
import json
import os
import sys

import numpy as np
from scipy import signal

import sndlib as sl
import stepcut
from sndlib import RATE

LOOP_S = 75.0     # every loop is this long (the brief asks for at least 60 s)
XF_S = 4.0        # equal-power crossfade that closes a bed's loop

# --- loudness targets: BRIEF.md's targets-json block is the one home; nothing is copied here ---
TARGETS = sl.load_targets()
LOOP_TARGET = TARGETS["loops_lufs"]            # by output name, integrated LUFS
SHOT_TARGET = TARGETS["one_shot_lufs_m"]       # by class, highest 400 ms momentary LUFS
SHOT_TOL = TARGETS["one_shot_tolerance"]
TP_LIMIT = TARGETS["true_peak_max_dbtp"]

_cache = {}
MANIFEST = {"outputs": {}}


# ------------------------------------------------------------------------------------------------ sources
def src_path(sid):
    d = sl.SOURCES_DIR
    for name in sorted(os.listdir(d)):
        if name.startswith(sid + "."):
            return os.path.join(d, name)
    raise SystemExit("make_sound: source %s is not in %s (run fetch_sources.py)" % (sid, d))


def S(sid, channels=None):
    key = (sid, channels)
    if key not in _cache:
        _cache[key] = sl.decode(src_path(sid), channels=channels)
    return _cache[key]


def cut_src(sid, a, b, channels=None):
    return sl.seg(S(sid, channels), a, b)


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# --------------------------------------------------------------------------------------------- processing
def leveller(x, strength=0.6, win_s=2.0, max_db=10.0):
    """Slow gain riding: pulls the moving 2 s level toward its median so single passes stop standing out."""
    m = sl.to_mono(x)
    n = int(win_s * RATE)
    c = np.concatenate([[0.0], np.cumsum(m * m)])
    pad = n // 2
    cp = np.concatenate([np.full(pad, c[0]), c, np.full(n - pad, c[-1])])
    env = np.sqrt((cp[n:n + len(m)] - cp[:len(m)]) / n + 1e-14)
    db = 20 * np.log10(env)
    db_s = signal.sosfiltfilt(signal.butter(2, 0.15, fs=RATE / 480, output="sos"), db[::480])
    db_s = np.interp(np.arange(len(db)), np.arange(len(db_s)) * 480, db_s)
    g = np.clip(-strength * (db_s - np.median(db_s)), -max_db, max_db)
    g = 10 ** (g / 20)
    return x * (g[:, None] if x.ndim > 1 else g)


def room_ir(rt60, seed, length_s=None):
    """A short diffuse tail (decaying noise), for gull calls heard across a quay."""
    rng = np.random.default_rng(seed)
    n = int((length_s or rt60 * 1.2) * RATE)
    t = np.arange(n) / RATE
    ir = rng.standard_normal(n) * 10 ** (-3.0 * t / rt60)
    ir[0] = 0
    return ir / np.sqrt(np.sum(ir ** 2))


def add_circular(buf, clip, start):
    """Mix clip into buf starting at sample `start`, continuing at the beginning when it runs past the end."""
    n = len(buf)
    i = start % n
    end = i + len(clip)
    if end <= n:
        buf[i:end] += clip
    else:
        k = n - i
        buf[i:] += clip[:k]
        buf[:end - n] += clip[k:]


def spliced_bed(parts, xfade_s=3.0, need_s=LOOP_S + XF_S):
    """Excerpts joined with equal-power crossfades; must come to at least need_s."""
    x = sl.spliced(parts, xfade_s) if len(parts) > 1 else parts[0]
    if len(x) < int(need_s * RATE):
        raise SystemExit("bed is %.1f s, needs %.1f s" % (len(x) / RATE, need_s))
    return x


def bed_loop(x):
    return sl.make_loop(x, LOOP_S, XF_S)


def circ_filter(x, kind, freq, order=4):
    """Filter a signal that is a circle (a loop mixed round its own end): wrap it three times, filter, keep the middle,
    so the filtered loop still closes without a step."""
    n = len(x)
    y = sl.sos_filter(np.tile(x, 3) if x.ndim == 1 else np.tile(x, (3, 1)), kind, freq, order)
    return y[n:2 * n]


def apply_chain(x, chain):
    for kind, f, order in chain:
        x = sl.sos_filter(x, kind, f, order)
    return x


# ---------------------------------------------------------------------------------------------- gull calls
def gull_clip(sid, a, b, lp_hz, gain_db, seed, speed=1.0):
    """One call: cut with 60 ms margins, rumble off, nearer or farther by low-pass and level, a tail like open air.
    speed above 1 plays it faster and higher (a different bird, by a few percent)."""
    m = sl.to_mono(S(sid))
    a = max(0.0, a - 0.06)
    c = sl.seg(m, a, b + 0.25)
    if speed != 1.0:
        from fractions import Fraction
        fr = Fraction(speed).limit_denominator(40)
        c = signal.resample_poly(c, fr.denominator, fr.numerator)
    c = sl.sos_filter(c, "hp", 450.0, 2)
    c = sl.sos_filter(c, "lp", lp_hz, 4)
    c = sl.fade(c, int(0.03 * RATE), int(0.2 * RATE))
    tail = signal.fftconvolve(c, room_ir(0.7, seed))[:len(c) + int(0.5 * RATE)]
    wet = 0.35 if lp_hz < 3000 else 0.2
    c = np.concatenate([c, np.zeros(len(tail) - len(c))]) * (1 - wet) + tail * wet * np.sqrt(np.mean(c ** 2) / (np.mean(tail ** 2) + 1e-20))
    return c * 10 ** (gain_db / 20)


# The calls used, cut by hand from each take's spectrogram (seconds): a call, a run of calls, or the whole take.
GULL_POOLS = {
    "fs_538015": [(0.0, 1.6), (2.6, 3.77), (7.67, 9.06), (18.92, 20.28)],   # herring gull, long calls and mews, close
    "fs_538016": [(8.37, 12.54), (13.87, 17.4)],                              # the same bird, two 'kyow' runs
    "fs_73497": [(0.07, 3.39)],                                               # one raucous call
    "fs_372213": [(14.84, 17.37), (5.46, 6.05)],                              # gulls off a headland, already far
    "fs_744592": [(0.0, 13.4)],                                               # a bird passing over a roof at night
}

GULL_PLANS = {
    # (source, call, second in the loop, level dB, low-pass Hz, speed): near calls bright and loud, far calls dull and quiet;
    # the speed (0.93 to 1.07) makes one bird's call another bird's
    "day": [("fs_538015", 0, 4.0, -4, 5200, 1.0), ("fs_73497", 0, 13.5, -9, 4200, 1.0), ("fs_538016", 0, 21.0, -14, 3000, 1.0),
            ("fs_538015", 2, 29.5, -8, 4400, 1.04), ("fs_372213", 0, 37.0, -16, 2600, 1.0), ("fs_538015", 1, 45.5, -12, 3400, 0.96),
            ("fs_538016", 1, 52.0, -6, 4800, 1.0), ("fs_73497", 0, 61.0, -15, 2800, 1.07), ("fs_538015", 3, 68.0, -13, 3200, 0.93)],
    "night": [("fs_744592", 0, 31.0, -9, 3200, 1.0), ("fs_538015", 3, 66.0, -20, 2200, 0.95)],
    "rain": [("fs_538015", 1, 18.0, -15, 2000, 1.0), ("fs_538016", 1, 52.0, -17, 1900, 1.0)],
}


def build_gulls(version):
    buf = np.zeros(int(LOOP_S * RATE))
    cuts = []
    for k, (sid, idx, t, gdb, lp, speed) in enumerate(GULL_PLANS[version]):
        a, b = GULL_POOLS[sid][idx]
        clip = gull_clip(sid, a, b, lp, gdb, seed=100 + k, speed=speed)
        add_circular(buf, clip, int(t * RATE))
        cuts.append({"source": sid, "from_s": a, "to_s": b, "placed_at_s": t, "level_db": gdb, "lowpass_hz": lp, "speed": speed})
    return buf, {"calls": cuts, "call_count": len(cuts)}


# ---------------------------------------------------------------------------- voices and radio through glass
def grain_babble(sources, weights, length_s, seed, grain_ms=(80, 150), hop_frac=0.5, phrase_hz=0.25, floor_gain=0.25):
    """Speech turned to a murmur: grains of 80 to 150 ms taken from random places in the sources, laid in random order
    with Hann windows (50 percent overlap) round a circle, under a slow random swell so it comes and goes in
    phrases. No word survives: a grain is shorter than any syllable run. Seamless as a loop."""
    rng = np.random.default_rng(seed)
    N = int(length_s * RATE)
    out = np.zeros(N)
    pools = [sl.to_mono(S(sid)) for sid in sources]
    w = np.array(weights, dtype=float) / np.sum(weights)
    pos = 0
    while pos < N:
        g = int(rng.uniform(*grain_ms) / 1000 * RATE)
        p = pools[rng.choice(len(pools), p=w)]
        s0 = rng.integers(int(0.3 * RATE), len(p) - g - int(0.3 * RATE))
        grain = p[s0:s0 + g] * np.hanning(g)
        add_circular(out, grain, pos)
        pos += int(g * hop_frac)
    # slow swell (circular, so the loop closes): smoothed noise with a few cycles in the loop
    k = max(2, int(phrase_hz * length_s))
    ctrl = rng.random(k)
    ctrl = np.append(ctrl, ctrl[0])
    sw = np.interp(np.linspace(0, k, N, endpoint=False), np.arange(k + 1), ctrl)
    sw = floor_gain + (1 - floor_gain) * (0.5 - 0.5 * np.cos(np.pi * sw))
    return out * sw


def build_voices(version):
    if version == "day":
        x = grain_babble(["fs_757318", "fs_260124"], [0.7, 0.3], LOOP_S, seed=11)
        lp, extra = 1150.0, 0
    elif version == "night":
        x = grain_babble(["fs_260124"], [1.0], LOOP_S, seed=12, phrase_hz=0.15, floor_gain=0.05)
        lp, extra = 1000.0, 0
    else:
        x = grain_babble(["fs_757318"], [1.0], LOOP_S, seed=13, phrase_hz=0.2, floor_gain=0.15)
        lp, extra = 800.0, 1
    x = circ_filter(x, "hp", 160.0, 2)
    x = circ_filter(x, "lp", lp, 4)         # a pane of glass and a wall: nothing above about 1 kHz gets through
    return x, {"lowpass_hz": lp, "grain_ms": [80, 150], "sources": ["fs_757318", "fs_260124"] if version == "day" else (["fs_260124"] if version == "night" else ["fs_757318"])}


def build_radio(version):
    x = grain_babble(["fs_528615"], [1.0], LOOP_S, seed=21, grain_ms=(90, 160), phrase_hz=0.12, floor_gain=0.35)
    x = circ_filter(x, "bp", [320.0, 3200.0], 2)                   # a small speaker's band
    x = np.tanh(2.2 * x / (np.std(x) + 1e-12)) * np.std(x)           # a little cone distortion
    rng = np.random.default_rng(22)
    hiss = circ_filter(rng.standard_normal(len(x)), "bp", [1500.0, 5000.0], 2)
    x = x + hiss * 0.12 * np.std(x) / (np.std(hiss) + 1e-12)
    lp = {"day": 1250.0, "night": 1050.0, "rain": 800.0}[version]
    x = circ_filter(x, "lp", lp, 4)                                 # then the window
    return x, {"lowpass_hz": lp, "band_hz": [320, 3200], "grain_ms": [90, 160], "sources": ["fs_528615"]}


# -------------------------------------------------------------------------------------------------- beds
def build_traffic(version):
    if version == "day":
        x = cut_src("fs_503456", 140.0, 224.0)
        x = apply_chain(x, [("hp", 70.0, 2), ("lp", 1800.0, 4)])
        x = leveller(x, 0.6)
        meta = {"cuts": [["fs_503456", 140.0, 224.0]], "chain": "highpass 70 Hz, lowpass 1800 Hz (distance), leveller 0.6"}
    elif version == "night":
        x = cut_src("fs_395686", 20.0, 104.0)
        x = apply_chain(x, [("hp", 70.0, 2), ("lp", 1500.0, 4)])
        x = leveller(x, 0.35)
        meta = {"cuts": [["fs_395686", 20.0, 104.0]], "chain": "highpass 70 Hz, lowpass 1500 Hz, leveller 0.35"}
    else:
        x = spliced_bed([cut_src("bsb_621", 0.0, 46.0), cut_src("bsb_621", 24.0, 68.0)])
        x = apply_chain(x, [("hp", 80.0, 2)])
        x = x + 2.0 * sl.sos_filter(x, "hp", 1500.0, 2)      # tyre hiss on wet tarmac: about 8 dB more above 1.5 kHz
        x = apply_chain(x, [("lp", 6000.0, 4)])
        x = leveller(x, 0.3)
        meta = {"cuts": [["bsb_621", 0.0, 46.0], ["bsb_621", 24.0, 68.0]], "chain": "highpass 80 Hz, +8 dB above 1.5 kHz (wet-road hiss), lowpass 6000 Hz, leveller 0.3; two excerpts crossfaded 3 s"}
    return bed_loop(x), meta


def far_engine(a, b, lp=700.0, fade_s=8.0):
    x = cut_src("fs_559821", a, b)
    x = apply_chain(x, [("hp", 50.0, 2), ("lp", lp, 4)])
    return sl.fade(x, int(fade_s * RATE), int(fade_s * RATE))


def build_harbour(version):
    if version == "day":
        water = apply_chain(cut_src("fs_182611", 12.0, 96.0), [("hp", 100.0, 2), ("lp", 6000.0, 2)])
        rig = apply_chain(cut_src("fs_360633", 4.0, 88.0), [("hp", 250.0, 2), ("lp", 5000.0, 2)])
        mix = water + rig * 10 ** (-8 / 20)
        loop = bed_loop(mix)
        eng = far_engine(150.0, 186.0)
        eng_m = eng if eng.ndim == loop.ndim else (np.stack([eng, eng], axis=1) if loop.ndim > 1 else sl.to_mono(eng))
        add_circular(loop, eng_m * 10 ** (-12 / 20) * np.std(water) / (np.std(eng) + 1e-12), int(22 * RATE))
        meta = {"cuts": [["fs_182611", 12.0, 96.0], ["fs_360633", 4.0, 88.0], ["fs_559821", 150.0, 186.0]],
                "chain": "water: highpass 100, lowpass 6000; rigging -8 dB from highpass 250; a far boat engine (lowpass 700, 8 s fades) at 22 s, -12 dB re the water"}
        return loop, meta
    if version == "night":
        water = apply_chain(cut_src("fs_182610", 14.0, 98.0), [("hp", 100.0, 2), ("lp", 3500.0, 4)])
        rig = apply_chain(cut_src("fs_360633", 20.0, 104.0 if False else 100.0), [("hp", 250.0, 2), ("lp", 3000.0, 4)])
        n = min(len(water), len(rig))
        mix = water[:n] + rig[:n] * 10 ** (-14 / 20)
        return bed_loop(mix), {"cuts": [["fs_182610", 14.0, 98.0], ["fs_360633", 20.0, 100.0]],
                               "chain": "water highpass 100, lowpass 3500; rigging -14 dB, lowpass 3000"}
    water = apply_chain(cut_src("fs_182612", 12.0, 96.0), [("hp", 100.0, 2), ("lp", 4500.0, 4)])
    whistle = apply_chain(cut_src("fs_463373", 0.0, 72.0), [("hp", 400.0, 2), ("lp", 4000.0, 2)])
    whistle = sl.spliced([whistle, whistle[int(10 * RATE):]], 3.0)[:len(water)]
    n = min(len(water), len(whistle))
    mix = water[:n] + whistle[:n] * 10 ** (-12 / 20)
    return bed_loop(mix), {"cuts": [["fs_182612", 12.0, 96.0], ["fs_463373", 0.0, 72.0]],
                           "chain": "water highpass 100, lowpass 4500; rigging whistle -12 dB from highpass 400; whistle excerpt repeated from 10 s"}


def build_wind(version):
    if version == "day":
        x = spliced_bed([cut_src("fs_454374", 0.0, 50.0), cut_src("fs_454374", 8.0, 44.0), cut_src("fs_454374", 20.0, 66.0)])
        x = apply_chain(x, [("hp", 60.0, 2), ("lp", 2500.0, 2)])
        meta = {"cuts": [["fs_454374", 0.0, 50.0], ["fs_454374", 8.0, 44.0], ["fs_454374", 20.0, 66.0]], "chain": "highpass 60, lowpass 2500; three excerpts crossfaded 3 s"}
    elif version == "night":
        x = cut_src("fs_554845", 20.0, 104.0)
        x = apply_chain(x, [("hp", 90.0, 2), ("lp", 1800.0, 4)])
        meta = {"cuts": [["fs_554845", 20.0, 104.0]], "chain": "highpass 90, lowpass 1800"}
    else:
        x = spliced_bed([cut_src("bsb_625", 0.0, 50.0), cut_src("bsb_625", 38.0, 91.0)])
        x = apply_chain(x, [("hp", 90.0, 2), ("lp", 3500.0, 4)])
        meta = {"cuts": [["bsb_625", 0.0, 50.0], ["bsb_625", 38.0, 91.0]], "chain": "highpass 90, lowpass 3500; two excerpts crossfaded 3 s"}
    return bed_loop(x), meta


def build_rain(kind):
    if kind == "rain_pavement":
        x = cut_src("bsb_1289", 0.0, LOOP_S + XF_S + 0.5, channels=1)
        x = sl.sos_filter(x, "hp", 120.0, 2)
        meta = {"cuts": [["bsb_1289", 0.0, LOOP_S + XF_S + 0.5]], "chain": "highpass 120 (mono source)"}
    elif kind == "rain_awning":
        x = cut_src("fs_454130", 0.0, 81.5)
        x = sl.sos_filter(x, "hp", 150.0, 2)
        meta = {"cuts": [["fs_454130", 0.0, 81.5]], "chain": "highpass 150"}
    else:
        x = cut_src("fs_846446", 8.0, 92.0)
        x = sl.sos_filter(x, "hp", 250.0, 2)
        meta = {"cuts": [["fs_846446", 8.0, 92.0]], "chain": "highpass 250"}
    return bed_loop(x), meta


# ----------------------------------------------------------------------------------------- loop registry
def loop_jobs():
    jobs = []
    for layer, fn in (("traffic", build_traffic), ("gulls", build_gulls), ("harbour", build_harbour), ("wind", build_wind),
                      ("voices", build_voices), ("radio", build_radio)):
        for v in ("day", "night", "rain"):
            jobs.append(("amb_%s_%s" % (layer, v), layer, v, (lambda f=fn, vv=v: f(vv))))
    for kind in ("rain_pavement", "rain_awning", "rain_gutter"):
        jobs.append(("amb_%s" % kind, kind, "rain", (lambda k=kind: build_rain(k))))
    return jobs


def write_loop(name, layer, version, build):
    x, meta = build()
    target = LOOP_TARGET[name]
    x = x - np.mean(x, axis=0)                      # no DC
    g = sl.gain_to_target(x, target)
    y = x * 10 ** (g / 20)
    tp = sl.true_peak_db(y)
    if tp > TP_LIMIT:
        raise SystemExit("%s: true peak %.1f dBTP at target %.1f LUFS; the cut needs a gentler leveller" % (name, tp, target))
    path = os.path.join(sl.OUT_DIR, name + ".wav")
    sl.write_wav16(path, y, seed=abs(hash_name(name)) % (2 ** 31))
    z, sr, bits = sl.read_wav16(path)
    chans = 1 if z.ndim == 1 else z.shape[1]
    seam = seam_measures(z)
    rec = {"file": name + ".wav", "kind": "loop", "layer": layer, "version": version, "sources": sorted({c[0] if isinstance(c, list) else c.get("source") for c in meta.get("cuts", [])} | set(meta.get("sources", []))
                                                                                                      | {c["source"] for c in meta.get("calls", [])}),
           "build": meta, "channels": chans, "sample_rate": sr, "bit_depth": bits, "seconds": round(len(z) / RATE, 3),
           "target_lufs": target, "lufs_integrated": round(sl.integrated_lufs(z), 2), "true_peak_dbtp": round(sl.true_peak_db(z), 2),
           "sample_peak_dbfs": round(sl.sample_peak_db(z), 2), "gain_applied_db": round(g, 2), "seam": seam,
           "sha256": file_sha256(path)}
    MANIFEST["outputs"][name] = rec
    print("%-26s %2d ch  %5.1f s  %6.2f LUFS (target %5.1f)  TP %6.2f  seam jump %.2f x, step %.2f dB (pctl %.2f)" % (
        name, chans, rec["seconds"], rec["lufs_integrated"], target, rec["true_peak_dbtp"], seam["jump_ratio"], seam["level_step_db"], seam["step_percentile"]))
    return z


def hash_name(name):
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)


def seam_measures(z):
    """How the loop closes, read on the loop as a circle.
    jump_ratio: the step from the last sample to the first, in units of the typical sample-to-sample step in the two
    seconds round the seam (a click is far above 1).
    level_step_db: the level of the second before the seam against the second after it.
    step_percentile: the share of all other places on the circle (every 0.1 s) where the same one-second-against-one-second
    step is smaller than at the seam. 0.5 is an ordinary place; 0.99 is a seam that stands out."""
    m = z if z.ndim == 1 else z.mean(axis=1)
    n = int(2 * RATE)
    d = np.diff(np.concatenate([m[-n:], m[:n]]))
    typical = np.sqrt(np.mean(np.delete(d, n - 1) ** 2)) + 1e-12
    jump = abs(m[0] - m[-1]) / typical
    w = int(1.0 * RATE)
    c = np.concatenate([[0.0], np.cumsum(np.concatenate([m, m, m]) ** 2)])
    N = len(m)
    pos = np.arange(0, N, int(0.1 * RATE))
    before = (c[pos + N] - c[pos + N - w]) / w + 1e-14
    after = (c[pos + N + w] - c[pos + N]) / w + 1e-14
    step = np.abs(10 * np.log10(before / after))
    return {"jump_ratio": round(float(jump), 3), "level_step_db": round(float(step[0]), 2),
            "step_percentile": round(float(np.mean(step[1:] < step[0])), 3), "crossfade_s": XF_S}


# --------------------------------------------------------------------------------------- one-shot helpers
def level_shot(x, kind):
    """Gain for a one-shot: its highest 400 ms momentary loudness to the target, held back where that would pass
    -1.5 dBTP (then it ends up under target, never over)."""
    target = SHOT_TARGET[kind]
    g = target - sl.momentary_max(x)
    y = x * 10 ** (g / 20)
    tp = sl.true_peak_db(y)
    limited = False
    if tp > -1.5:
        y *= 10 ** ((-1.5 - tp) / 20)
        limited = True
    return y, limited


def write_shot(name, kind, x, meta, group):
    x = x - np.mean(x) if len(x) > RATE else x
    n = min(len(x), int(0.012 * RATE))                      # every one-shot ends on a 12 ms raised-cosine fade, on top of any longer one
    x = x.copy()
    x[-n:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, n))
    y, limited = level_shot(x, kind)
    path = os.path.join(sl.OUT_DIR, name + ".wav")
    sl.write_wav16(path, y, seed=hash_name(name) % (2 ** 31))
    z, sr, bits = sl.read_wav16(path)
    rec = {"file": name + ".wav", "kind": "one-shot", "group": group, "class": kind, "sources": meta.pop("sources"), "build": meta,
           "channels": 1, "sample_rate": sr, "bit_depth": bits, "seconds": round(len(z) / RATE, 3),
           "target_lufs_m": SHOT_TARGET[kind], "lufs_m_max": round(sl.momentary_max(z), 2), "true_peak_dbtp": round(sl.true_peak_db(z), 2),
           "sample_peak_dbfs": round(sl.sample_peak_db(z), 2), "limited_by_peak": limited, "sha256": file_sha256(path)}
    MANIFEST["outputs"][name] = rec
    return rec


# ------------------------------------------------------------------------------------------------ footsteps
STEP_TAKES = {
    # surface: [(source, high-pass Hz, cut options)]
    "paving": [("fs_273071", 70.0, {}), ("fs_273067", 70.0, {})],
    "setts": [("fs_637555", 70.0, {}), ("fs_868548", 70.0, {})],
    "asphalt": [("fs_637556", 70.0, {}), ("fs_455056", 70.0, {})],
    "wet": [("fs_263495", 70.0, {}), ("fs_531566", 70.0, {})],
    "wood": [("fs_536770", 70.0, {}), ("fs_575898", 70.0, {})],
}
STEP_OPTS = dict(min_transients=1, centroid_range=(300.0, 3500.0), max_ms=260.0)
STEPS_PER_SURFACE = 8


def build_steps(surface):
    cand = []   # (source, start sample, samples)
    for sid, hp, opts in STEP_TAKES[surface]:
        m = stepcut.highpass(sl.to_mono(S(sid)), hp)
        for a, st in stepcut.cut(m, **dict(STEP_OPTS, **opts)):
            cand.append((sid, a, st))
    if len(cand) < STEPS_PER_SURFACE:
        raise SystemExit("%s: only %d clean steps found" % (surface, len(cand)))
    loud = np.array([sl.momentary_max(st) for _, _, st in cand])
    # a step whose peak stands more than 25 dB over its momentary loudness cannot reach the target without passing -1.5 dBTP
    crest = np.array([sl.true_peak_db(st) - l for (_, _, st), l in zip(cand, loud)])
    keep = np.flatnonzero(crest <= -1.5 - SHOT_TARGET["step"])
    if len(keep) >= 3 * STEPS_PER_SURFACE:
        cand, loud = [cand[i] for i in keep], loud[keep]
    # distinct choice across sources; any two of the eight must also correlate under 0.8 (the check allows 0.9)
    pairs = [(a + (hash_name(sid) % 1000) * 10 ** 7, st) for sid, a, st in cand]   # keep takes apart in the time test
    alive = list(range(len(cand)))
    for _ in range(40):
        pick_local = stepcut.pick_distinct([pairs[i] for i in alive], STEPS_PER_SURFACE, loud[alive])
        pick = [alive[i] for i in pick_local]
        worst, bad = 0.0, None
        for x in range(len(pick)):
            for y in range(x + 1, len(pick)):
                c = stepcut.max_xcorr(cand[pick[x]][2], cand[pick[y]][2])
                if c > worst:
                    worst, bad = c, (pick[x], pick[y])
        if worst <= 0.8:
            break
        alive.remove(bad[1])          # drop the later of the two look-alikes and choose again
    else:
        raise SystemExit("%s: could not find %d steps that differ" % (surface, STEPS_PER_SURFACE))
    outs = []
    for k, i in enumerate(pick, 1):
        sid, a, st = cand[i]
        name = "step_%s_%02d" % (surface, k)
        meta = {"sources": [sid], "cut_at_s": round(a / RATE, 3), "length_ms": round(1000 * len(st) / RATE), "highpass_hz": 70.0, "keep_edges": True}
        outs.append(write_shot(name, "step", st, meta, "step_" + surface))
    return outs


# ------------------------------------------------------------------------------------------------ one-shots
# (name, class, group, source, from s, to s, low-pass Hz or None, fade-out ms, what it is). Cut points were read from each take's
# envelope and spectrogram in the cloud, not by ear: BRIEF.md and NOTES.md list what only an ear can confirm (which door
# movement is "open" and which "close", which click is the latch).
def _latches(sid, times, pre=0.04, post=0.30):
    return [(sid, round(t - pre, 3), round(t + post, 3)) for t in times]


ONE_SHOTS = []
for k, (sid, a, b, what) in enumerate([("bsb_1270", 1.70, 2.45, "old glass door, the soft opening"),
                                        ("fs_402460", 38.0, 41.0, "heavy glass and metal door, opening with creaks")], 1):
    ONE_SHOTS.append(("door_shop_open_%02d" % k, "door_open", "door_shop", sid, a, b, None, 40, what))
for k, (sid, a, b, what) in enumerate([("bsb_1270", 0.10, 1.35, "old glass door, shutting, glass rattling"),
                                        ("bsb_1270", 3.85, 5.75, "old glass door, swinging shut and hitting its frame"),
                                        ("fs_402460", 43.6, 45.7, "heavy glass and metal door, closing")], 1):
    ONE_SHOTS.append(("door_shop_close_%02d" % k, "door_close", "door_shop", sid, a, b, None, 60, what))
for k, (sid, a, b) in enumerate(_latches("bsb_224", [2.401, 6.171, 9.574, 13.225]), 1):
    ONE_SHOTS.append(("door_shop_latch_%02d" % k, "door_latch", "door_shop", sid, a, b, None, 40, "a lightweight door's latch"))
for k, (sid, a, b, what) in enumerate([("fs_402464", 0.40, 2.10, "heavy wooden door, opening"),
                                        ("fs_402465", 0.00, 1.20, "heavy wooden door, opened quickly"),
                                        ("bsb_1320", 1.25, 3.00, "entrance door, opening after the key")], 1):
    ONE_SHOTS.append(("door_house_open_%02d" % k, "door_open", "door_house", sid, a, b, None, 40, what))
for k, (sid, a, b, what) in enumerate([("fs_402464", 5.90, 6.80, "heavy wooden door, closing on its seal"),
                                        ("fs_402465", 2.90, 3.80, "heavy wooden door, closing hard"),
                                        ("fs_402466", 0.00, 1.60, "heavy wooden door, closed quietly"),
                                        ("bsb_545", 0.30, 1.30, "front door, a sharp closure"),
                                        ("bsb_545", 4.60, 5.50, "front door, a sharp closure")], 1):
    ONE_SHOTS.append(("door_house_close_%02d" % k, "door_close", "door_house", sid, a, b, None, 60, what))
for k, (sid, a, b) in enumerate(_latches("bsb_1320", [0.392, 1.281, 2.256]), 1):
    ONE_SHOTS.append(("door_house_latch_%02d" % k, "door_latch", "door_house", sid, a, b, None, 40, "key, bolt or latch of an entrance door"))
for k, (sid, a, b, what) in enumerate([("fs_57743", 0.00, 3.20, "a bell on a shop door as someone enters"),
                                        ("fs_494565", 0.25, 2.10, "a shop door bell, opening"),
                                        ("fs_494565", 2.35, 3.80, "a shop door bell, opening"),
                                        ("fs_494565", 4.40, 5.70, "a shop door bell, opening"),
                                        ("fs_494565", 6.70, 7.70, "a shop door bell, opening")], 1):
    ONE_SHOTS.append(("bell_shop_%02d" % k, "bell", "bell_shop", sid, a, b, None, 150, what))
for k, (sid, a, b, what) in enumerate([("fs_674027", 0.07, 2.60, "old telephone booth door creaking"),
                                        ("fs_402460", 3.90, 5.80, "heavy glass and metal door creaking slowly"),
                                        ("fs_402460", 10.4, 12.4, "heavy glass and metal door, a squeak and a creak"),
                                        ("bsb_605", 0.18, 1.40, "door spring grinding"),
                                        ("bsb_605", 4.40, 5.40, "door spring grinding")], 1):
    ONE_SHOTS.append(("phonebox_door_creak_%02d" % k, "phonebox_creak", "phonebox", sid, a, b, None, 60, what))
for k, (sid, a, b, what) in enumerate([("fs_402459", 11.35, 12.25, "heavy glass and metal door, shutting sharply"),
                                        ("fs_402459", 8.55, 9.40, "heavy glass and metal door, shutting"),
                                        ("fs_402460", 22.9, 24.9, "heavy glass and metal door, swinging shut")], 1):
    ONE_SHOTS.append(("phonebox_door_shut_%02d" % k, "phonebox_shut", "phonebox", sid, a, b, None, 60, what))
for k, (a, b) in enumerate([(0.55, 2.60), (3.50, 5.55), (6.50, 8.55)], 1):
    ONE_SHOTS.append(("phonebox_ring_%02d" % k, "phonebox_ring", "phonebox", "fs_435577", a, b, None, 200,
                      "a GPO 746 telephone ringing, one double ring (a house telephone: no kiosk payphone recording was found)"))


def build_one_shots(sel):
    for name, cls, group, sid, a, b, lp, fade_ms, what in ONE_SHOTS:
        if not sel(name):
            continue
        x = sl.to_mono(S(sid))
        x = sl.seg(x, a, b)
        x = sl.sos_filter(x, "hp", 60.0, 2)
        if lp:
            x = sl.sos_filter(x, "lp", lp, 4)
        x = sl.fade(x, int(0.002 * RATE), int(fade_ms / 1000.0 * RATE))
        meta = {"sources": [sid], "from_s": a, "to_s": b, "what": what, "highpass_hz": 60.0, "fade_out_ms": fade_ms, "keep_edges": True}
        rec = write_shot(name, cls, x, meta, group)
        print("%-26s %5d ms  M %6.2f (target %5.1f)  TP %6.2f  %s" % (rec["file"], round(rec["seconds"] * 1000), rec["lufs_m_max"],
              rec["target_lufs_m"], rec["true_peak_dbtp"], "peak-limited" if rec["limited_by_peak"] else ""))


def save_manifest():
    path = os.path.join(sl.HERE, "manifest.json")
    old = {}
    if os.path.exists(path) and len(sys.argv) > 1:      # a partial run updates its own rows; a full run starts clean
        with open(path, encoding="utf8") as f:
            old = json.load(f).get("outputs", {})
    old.update(MANIFEST["outputs"])
    src = sl.load_json("sources.json")["sources"]
    out = {
        "about": "Every output of make_sound.py: what it is made from, where it was cut, how loud it measures (BS.1770-4), and for loops how the seam closes. "
                 "Rebuilt by make_sound.py from the sources listed in sources.json; the sha256 of each WAV shows a rebuild is identical.",
        "rate": RATE, "loop_seconds": LOOP_S, "loop_crossfade_seconds": XF_S,
        "loop_targets_lufs_integrated": dict(sorted(LOOP_TARGET.items())),
        "one_shot_targets_lufs_momentary_max": SHOT_TARGET, "one_shot_tolerance_lu": SHOT_TOL, "true_peak_limit_dbtp": TP_LIMIT,
        "sources_md5": {s["id"]: s.get("md5") for s in src},
        "outputs": {k: old[k] for k in sorted(old)},
    }
    sl.save_json("manifest.json", out)


def main():
    only = sys.argv[1:]
    os.makedirs(sl.OUT_DIR, exist_ok=True)
    sel = lambda n: not only or any(n.startswith(o) for o in only)
    for name, layer, version, build in loop_jobs():
        if sel(name):
            write_loop(name, layer, version, build)
    for surface in STEP_TAKES:
        if sel("step_" + surface):
            for rec in build_steps(surface):
                print("%-26s %5d ms  M %6.2f (target %5.1f)  TP %6.2f  %s" % (rec["file"], round(rec["seconds"] * 1000), rec["lufs_m_max"],
                      rec["target_lufs_m"], rec["true_peak_dbtp"], "peak-limited" if rec["limited_by_peak"] else ""))
    build_one_shots(sel)
    save_manifest()
    n = len(MANIFEST["outputs"])
    print("%d outputs written to %s; manifest.json updated" % (n, sl.OUT_DIR))


if __name__ == "__main__":
    main()
