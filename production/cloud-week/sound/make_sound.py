#!/usr/bin/env python3
"""Rebuild every sound of Quay Street (unit 10, cloud week 42) from the fetched CC0 sources.

    python fetch_sources.py            # once: the sources, outside the repository
    python make_sound.py               # writes WAVs to SOUND_OUT (default /home/user/ledger-scratch/sound-out)
                                       # and manifest.json beside this file
    python make_sound.py amb_wind      # only the outputs whose name starts with these
    python check_sound.py              # then the check (checks/check_v1.json)
    python make_previews.py            # the spectrogram JPEGs (minutes); the listening clips come with a full make_sound.py run

Everything is deterministic: fixed cut points, seeded random numbers (gull calls placed, voices scrambled),
seeded dither. A second run gives byte-identical WAVs (the manifest holds each file's sha256).

What it makes (BRIEF.md says why, and what each must sound like):
  21 ambience loops, 60 to 75 s, 48 kHz 16 bit WAV: traffic, gulls, harbour, wind, voices through a window and a radio
     through a window, each in day, night and rain versions; the rain itself on pavement, on an awning and in
     a gutter (rain version only). Beds are stereo; point sources (gulls, voices, radio) and the mono pavement rain are mono.
     A loop is 75 s unless its recording is too short for that without playing part of it twice: the rain traffic, the day wind
     and the rain harbour are 60 s. Steady tones (mains hum, a recorder's whine) are notched out of every bed's source cuts.
  footsteps: 8 variants on each of paving, setts, asphalt, wet, wood (mono one-shots)
  one-shots: shop door (open, close, latch), house door (open, close, latch), the shop bell, the phone box (door creak,
     door shut, a telephone ringing)

Loops are seamless by construction: a bed's tail is crossfaded (equal power, 4 s) into its head, so the sample after
its last is the one that followed it in the source; point-source layers are mixed round a circle, so an event that
runs past the end continues at the start (the voices and the radio, being circles, start where the level changes least). Levels are set by measured gain (BS.1770-4 integrated loudness for loops,
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

RADIO_BODY_DB, RADIO_DRIVE, RADIO_HISS = 5.0, 2.6, 0.06
RADIO_LP = {"day": 2600.0, "night": 2200.0, "rain": 1500.0}
NIGHT_WIND_LP = 1000   # Hz: the night wind is darker than the day wind (2500 Hz); the first build's 1800 Hz was brighter
LOOP_S = 75.0     # a loop's length unless its source is too short for it (the brief allows 60 to 75 s)
SHORT_LOOP_S = 60.0   # loops whose source holds only about 67 s: 60 s plus the 4 s crossfade, with no part of the source played twice
XF_S = 4.0        # equal-power crossfade that closes a bed's loop

# --- loudness targets: BRIEF.md's targets-json block is the one home; nothing is copied here ---
TARGETS = sl.load_targets()
LOOP_TARGET = TARGETS["loops_lufs"]            # by output name, integrated LUFS
SHOT_TARGET = TARGETS["one_shot_lufs_m"]       # by class, highest 400 ms momentary LUFS
SHOT_TOL = TARGETS["one_shot_tolerance"]
STEP_CUT_DB = TARGETS["step_cut_db"]            # a footfall must die away, and start from, at least this far under its own peak (dB)
WET_OPTS = dict(died_db=STEP_CUT_DB["step_wet"], pre_db=STEP_CUT_DB["step_wet"], fade_ms=40.0, fade_in_ms=8.0, centroid_range=(300.0, 6000.0))   # see STEP_TAKES
GRAIN_REUSE_S = TARGETS["grain_reuse_min_s"]    # by output name: seconds before a moment of a speech source may come back
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


def bed_loop(x, loop_s=LOOP_S):
    return sl.make_loop(x, loop_s, XF_S)


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


def find_lines(x, seg_s=8.0, min_db=11.0, fmin=45.0, fmax=11000.0, block_hz=2.0, max_width_hz=4.0):
    """Steady tones in one channel of a source cut (mains hum, a recorder's whine, a machine's drone): lines far narrower than any
    real sound. The cut is read in 8 s frames (0.125 Hz bins) and each bin takes its level as the median over the frames, so
    what is there in the quiet stretches counts, which is where a tone is heard. The floor is the 30th percentile of the 2 Hz
    blocks' lower quartiles over the 41 blocks round it, so a crowd of lines does not lift it. A peak is a line when it stands
    min_db over that floor and is under max_width_hz wide at 10 dB down. Returns [(Hz, dB over, width Hz)].
    The check reads tones another way (1 s frames, 1 Hz bins), so this finder cannot pass its own check."""
    from scipy import ndimage
    nper = int(seg_s * RATE)
    f, _, S = signal.spectrogram(x, fs=RATE, window="hann", nperseg=nper, noverlap=nper // 2, detrend=False, mode="psd")
    S = S[:, S.sum(axis=0) > 1e-14]
    P = 10 ** (np.percentile(10 * np.log10(S + 1e-24), 50, axis=1) / 10)
    df = f[1]
    bpb = max(3, int(round(block_hz / df)))
    nb = len(P) // bpb
    blocks = np.percentile(P[:nb * bpb].reshape(nb, bpb), 25, axis=1)
    fl = ndimage.percentile_filter(blocks, 30, size=41, mode="nearest")
    floor = np.concatenate([np.repeat(fl, bpb), np.full(len(P) - nb * bpb, fl[-1])]) * 1.5      # the lower quartile sits 1.8 dB under the median
    ratio_db = 10 * np.log10(P / (floor + 1e-30))
    ok = (f >= fmin) & (f <= fmax)
    peaks, _ = signal.find_peaks(np.where(ok, ratio_db, -99.0), height=min_db, distance=max(1, int(0.5 / df)))
    out = []
    for k in peaks:
        lo, hi = k, k                                   # the width at 10 dB down, walking out from the peak
        while lo > 0 and P[lo - 1] > P[k] / 10 and k - lo < int(3 / df):
            lo -= 1
        while hi < len(P) - 1 and P[hi + 1] > P[k] / 10 and hi - k < int(3 / df):
            hi += 1
        width = (hi - lo + 1) * df
        if width <= max_width_hz:
            out.append((float(f[k]), float(ratio_db[k]), float(width)))
    return out


def detone(x):
    """Take the steady tones out of a source cut: a notch on each line found by find_lines (as wide as three times the line, and
    never narrower than f/80), zero-phase, on each channel separately. Returns (cleaned cut, {channel: [Hz, ...]})."""
    y = np.array(x, dtype=float)
    cols = [y] if y.ndim == 1 else [y[:, c] for c in range(y.shape[1])]
    found = {}
    for c, col in enumerate(cols):
        lines = find_lines(col)
        found[c] = [round(l[0], 2) for l in lines]
        for f0, _, width in lines:
            bw = max(3.0 * width, f0 / 80.0, 0.4)
            b, a = signal.iirnotch(f0, f0 / bw, fs=RATE)
            col[:] = signal.sosfiltfilt(signal.tf2sos(b, a), col)
    return (y if y.ndim == 1 else np.stack(cols, axis=1)), {str(k): v for k, v in found.items() if v}


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
CELL = int(0.010 * RATE)     # the grain plan's bookkeeping on a source: 10 ms cells
RUN_GAP_MS = 50              # neighbouring grains must lie at least this far apart in the source, so no grain continues another
NEAR_S = 0.32                # "neighbouring": starting within this much loop time of each other (two of the longest grains)
SRC_MARGIN_S = 0.3           # grains are never taken from the first or last 0.3 s of a source


def swell(rng, N, length_s, phrase_hz, floor_gain, gate=0.0):
    """A slow random swell round a circle (so the loop closes): the murmur comes and goes in phrases. gate above 0 cuts its low
    part away smoothly, so the quiet stretches are real gaps and not just a lower level."""
    k = max(2, int(phrase_hz * length_s))
    ctrl = rng.random(k)
    ctrl = np.append(ctrl, ctrl[0])
    sw = np.interp(np.linspace(0, k, N, endpoint=False), np.arange(k + 1), ctrl)
    sw = floor_gain + (1 - floor_gain) * (0.5 - 0.5 * np.cos(np.pi * sw))
    return np.clip((sw - gate) / (1 - gate), 0.0, 1.0) if gate > 0 else sw


def speech_bursts(rng, N, burst_s=(0.6, 2.0), gap_s=(0.7, 3.0), level=(0.55, 1.0), edge_s=0.10):
    """A radio's speech comes in bursts of different lengths and levels with gaps of different lengths between (the burst that
    runs past the end of the loop continues at its start)."""
    env = np.zeros(N)
    t = 0
    while t < N:
        b = int(rng.uniform(*burst_s) * RATE)
        w = signal.windows.tukey(b, alpha=min(1.0, 2 * edge_s * RATE / b)) * rng.uniform(*level)
        add_circular(env, w, t)
        t += b + int(rng.uniform(*gap_s) * RATE)
    return np.minimum(env, 1.0)


def grain_plan(rng, N, lens, weights, env, grain_ms, hop, no_repeat_s):
    """Where every grain goes, and which part of which source it is taken from.
    Grains of grain_ms[0] to grain_ms[1] start where env is above 0.03, one after another, a random hop (in grain lengths) apart.
    Each source is cut into slots as long as the longest grain, and each grain is given one slot, at a random place inside it,
    such that
      - no grain continues another: grains starting within NEAR_S of each other (round the circle) take slots that are neither
        the same nor next to each other, so there are at least RUN_GAP_MS between their places in a source and a run of speech
        is never longer than one grain;
      - no slot comes back within no_repeat_s of loop time (round the circle), as far as the source holds enough slots;
        where it does not, the least used slot is taken and the grain counted in 'fallbacks'.
    Returns arrays (pos, length, source index, source start; all in samples) and the number of fallbacks."""
    pos, glen = [], []
    p = 0
    while p < N:
        if env[p] < 0.03:
            p += CELL
            continue
        g = int(rng.uniform(*grain_ms) / 1000.0 * RATE)
        pos.append(p)
        glen.append(g)
        p += max(CELL, int(g * rng.uniform(*hop)))
    pos, glen = np.array(pos), np.array(glen)
    n, m = len(pos), len(lens)
    w = np.array(weights, dtype=float) / np.sum(weights)
    margin = int(SRC_MARGIN_S * RATE)
    slot = -(-int(grain_ms[1] / 1000.0 * RATE) // CELL) * CELL            # slot length in samples, a whole number of cells
    nslots = [(L - 2 * margin) // slot for L in lens]
    R, near = int((no_repeat_s + 0.3) * RATE), int(NEAR_S * RATE)
    sl_of = np.full(n, -1)
    src = np.full(n, -1)
    fallbacks = 0
    for j in range(n):
        d = np.abs(pos[:j] - pos[j])
        d = np.minimum(d, N - d)
        order = rng.choice(m, size=m, replace=False, p=w) if m > 1 else [0]
        pick, best = None, None
        for k in order:
            same = src[:j] == k
            win = np.zeros(nslots[k] + 2)
            np.add.at(win, sl_of[:j][same & (d < R)], 1)
            nb = np.zeros(nslots[k] + 2)
            for off in (-1, 0, 1):
                np.add.at(nb, np.clip(sl_of[:j][same & (d < near)] + off, 0, nslots[k] + 1), 1)
            free = np.flatnonzero((win[:nslots[k]] == 0) & (nb[:nslots[k]] == 0))
            if len(free):
                pick = (k, int(free[rng.integers(len(free))]))
                break
            load = win[:nslots[k]] + 1000.0 * nb[:nslots[k]]
            cand = np.flatnonzero(load == load.min())
            if best is None or load.min() < best[0]:
                best = (float(load.min()), k, int(cand[rng.integers(len(cand))]))
        if pick is None:
            pick = (best[1], best[2])
            fallbacks += 1
        src[j], sl_of[j] = pick
    st = np.array([margin + int(sl_of[j]) * slot + int(rng.integers(0, max(1, slot - glen[j]))) for j in range(n)])
    return pos, glen, src, st, fallbacks


def reuse_and_run(src, st, glen, pos, N):
    """From a grain plan: the shortest loop-time distance (s) between two grains that use overlapping places in a source, and
    the longest run (ms) of neighbouring grains whose places in a source touch or lie within RUN_GAP_MS of each other."""
    n = len(pos)
    best, run = 1e9, 0.0
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for j in range(n):
        d = np.abs(pos - pos[j])
        d = np.minimum(d, N - d)
        same = (src == src[j]) & (np.arange(n) > j)
        over = same & (st < st[j] + glen[j]) & (st[j] < st + glen)
        if over.any():
            best = min(best, float(d[over].min()) / RATE)
        gap = RUN_GAP_MS * RATE // 1000
        touch = same & (d < NEAR_S * RATE) & (st < st[j] + glen[j] + gap) & (st[j] < st + glen + gap)
        for i in np.flatnonzero(touch):
            parent[find(int(i))] = find(j)
    groups = {}
    for j in range(n):
        groups.setdefault(find(j), []).append(j)
    for g in groups.values():
        run = max(run, float(max(st[i] + glen[i] for i in g) - min(st[i] for i in g)) / RATE * 1000.0)
    return best, run


def grain_babble(sources, weights, length_s, seed, grain_ms=(80, 150), hop=(0.5, 0.5), phrase_hz=0.25, floor_gain=0.25,
                 gate=0.0, bursts=False, gain_jitter_db=0.0, no_repeat_s=20.0, tukey=None):
    """Speech turned to a murmur: grains of 80 to 150 ms taken from places in the sources chosen by grain_plan, laid in random
    order with Hann windows (or flat-topped Tukey ones where tukey is set) round a circle (hop 0.5 grains is 50 percent overlap, a
    dense murmur), under a slow random swell (or,
    for a radio, in bursts with gaps) so it comes and goes in phrases. No word survives: a grain is shorter than any syllable run
    and no grain continues another. Seamless as a loop. Returns the signal and a record of every grain (the check reads it)."""
    rng = np.random.default_rng(seed)
    N = int(length_s * RATE)
    pools = [sl.to_mono(S(sid)) for sid in sources]
    env = speech_bursts(rng, N) if bursts else swell(rng, N, length_s, phrase_hz, floor_gain, gate)
    pos, glen, src, st, fb = grain_plan(rng, N, [len(p) for p in pools], weights, env, grain_ms, hop, no_repeat_s)
    out = np.zeros(N)
    gains = 10 ** (rng.uniform(-gain_jitter_db, gain_jitter_db, len(pos)) / 20.0)
    for j in range(len(pos)):
        win = signal.windows.tukey(glen[j], tukey) if tukey else np.hanning(glen[j])
        g = pools[src[j]][st[j]:st[j] + glen[j]] * win * gains[j]
        add_circular(out, g, int(pos[j]))
    out *= env
    reuse, run = reuse_and_run(src, st, glen, pos, N)
    ms = lambda a: [int(round(v * 1000.0 / RATE)) for v in a]
    plan = {"sources": list(sources), "grains_n": int(len(pos)), "grain_ms": [int(round(glen.min() * 1000.0 / RATE)), int(round(glen.max() * 1000.0 / RATE))],
            "no_repeat_s_asked": no_repeat_s, "fallback_grains": int(fb), "min_reuse_s": round(reuse, 2), "longest_run_ms": round(run),
            "voiced_fraction": round(float(np.mean(env > 0.03)), 3),
            "plan": {"src": [int(v) for v in src], "start_ms": ms(st), "len_ms": ms(glen), "pos_ms": ms(pos)}}
    return out, plan


def circ_apply(x, fn):
    """Apply a causal filter to a circle: run it over three turns and keep the middle one, so the loop still closes."""
    n = len(x)
    return fn(np.tile(x, 3))[n:2 * n]


def build_voices(version):
    if version == "day":
        x, plan = grain_babble(["fs_757318", "fs_260124"], [0.7, 0.3], LOOP_S, seed=11, no_repeat_s=GRAIN_REUSE_S["amb_voices_day"])
        lp = 1150.0
    elif version == "night":
        # two adults, very quiet, in gaps: shorter phrases with real gaps between (gate), grains hopping 0.85 of their length
        # (Tukey windows), so the 19.7 s of recording is not used up and no moment of it comes back within 20 s
        x, plan = grain_babble(["fs_260124"], [1.0], LOOP_S, seed=12, hop=(0.85, 0.85), phrase_hz=0.25, floor_gain=0.05, gate=0.5,
                               no_repeat_s=GRAIN_REUSE_S["amb_voices_night"], tukey=0.5)
        lp = 1000.0
    else:
        x, plan = grain_babble(["fs_757318"], [1.0], LOOP_S, seed=13, phrase_hz=0.2, floor_gain=0.15, no_repeat_s=GRAIN_REUSE_S["amb_voices_rain"])
        lp = 800.0
    x = circ_filter(x, "hp", 160.0, 2)
    x = circ_filter(x, "lp", lp, 4)         # a pane of glass and a wall: nothing above about 1 kHz gets through
    plan["lowpass_hz"] = lp
    return x, plan


def build_radio(version):
    """A small speaker in a room next door: speech in bursts with gaps of different lengths (the grains hop 0.8 to 1.6 grains,
    so some touch and some leave a gap), cut to 300 Hz to 3 kHz (nothing below: no hum), a little more midrange body, a little
    cone distortion, a faint hiss, then the window. The recording it is made from is already muffled (nine tenths of its power
    between 445 and 727 Hz), so the body and the distortion are what give the band its width."""
    x, plan = grain_babble(["fs_528615"], [1.0], LOOP_S, seed=21, grain_ms=(90, 160), hop=(0.8, 1.6), bursts=True, gain_jitter_db=3.0,
                           no_repeat_s=GRAIN_REUSE_S["amb_radio_%s" % version], tukey=0.5)
    x = circ_filter(x, "bp", [300.0, 3000.0], 2)                           # a small speaker's band, hum-free
    x = circ_apply(x, lambda y: sl.peaking(y, 1000.0, 0.7, RADIO_BODY_DB))   # midrange body
    speech = np.std(x[np.abs(x) > 0.1 * np.abs(x).max()]) + 1e-12
    x = np.tanh(RADIO_DRIVE * x / speech) * speech                         # a little cone distortion
    rng = np.random.default_rng(22)
    hiss = circ_filter(rng.standard_normal(len(x)), "bp", [400.0, 1800.0], 2)
    x = x + hiss * RADIO_HISS * speech / (np.std(hiss) + 1e-12)
    lp = {"day": RADIO_LP["day"], "night": RADIO_LP["night"], "rain": RADIO_LP["rain"]}[version]
    x = circ_filter(x, "lp", lp, 4)                                         # then the window
    plan.update({"lowpass_hz": lp, "band_hz": [300, 3000], "body_db_at_1k": RADIO_BODY_DB, "drive": RADIO_DRIVE, "hiss_re_speech": RADIO_HISS})
    return x, plan


# -------------------------------------------------------------------------------------------------- beds
def cut_clean(sid, a, b, tones):
    """A source cut with its steady tones notched out (find_lines/detone); what was found is added to tones."""
    x, found = detone(cut_src(sid, a, b))
    if found:
        tones.setdefault(sid, {}).update(found)
    return x


def tones_meta(meta, tones):
    if tones:
        meta["notched_tones_hz"] = tones          # {source: {channel: [Hz, ...]}}
    return meta


def build_traffic(version):
    tones = {}
    if version == "day":
        x = cut_clean("fs_503456", 140.0, 224.0, tones)
        x = apply_chain(x, [("hp", 70.0, 2), ("lp", 1800.0, 4)])
        x = leveller(x, 0.6)
        meta = {"cuts": [["fs_503456", 140.0, 224.0]], "chain": "highpass 70 Hz, lowpass 1800 Hz (distance), leveller 0.6"}
        return bed_loop(x), tones_meta(meta, tones)
    if version == "night":
        x = cut_clean("fs_395686", 20.0, 104.0, tones)
        x = apply_chain(x, [("hp", 70.0, 2), ("lp", 1500.0, 4)])
        x = leveller(x, 0.35)
        meta = {"cuts": [["fs_395686", 20.0, 104.0]], "chain": "highpass 70 Hz, lowpass 1500 Hz, leveller 0.35"}
        return bed_loop(x), tones_meta(meta, tones)
    # rain: one 64 s cut of a 67 s recording, a 60 s loop: no part of the road is heard twice (the 12 October first build
    # spliced two cuts of it and played 22 s of it twice)
    x = cut_clean("bsb_621", 0.0, SHORT_LOOP_S + XF_S, tones)    # its right channel carries a 1281 Hz whine, notched out here
    x = apply_chain(x, [("hp", 80.0, 2)])
    x = x + 2.0 * sl.sos_filter(x, "hp", 1500.0, 2)      # tyre hiss on wet tarmac: about 8 dB more above 1.5 kHz
    x = apply_chain(x, [("lp", 6000.0, 4)])
    x = leveller(x, 0.3)
    meta = {"cuts": [["bsb_621", 0.0, SHORT_LOOP_S + XF_S]], "chain": "steady tones notched, highpass 80 Hz, +8 dB above 1.5 kHz (wet-road hiss), lowpass 6000 Hz, leveller 0.3; a 60 s loop of one uninterrupted cut"}
    return bed_loop(x, SHORT_LOOP_S), tones_meta(meta, tones)


def far_engine(a, b, lp=700.0, fade_s=8.0):
    x = cut_src("fs_559821", a, b)
    x = apply_chain(x, [("hp", 50.0, 2), ("lp", lp, 4)])
    return sl.fade(x, int(fade_s * RATE), int(fade_s * RATE))


def build_harbour(version):
    tones = {}
    if version == "day":
        water = apply_chain(cut_clean("fs_182611", 12.0, 96.0, tones), [("hp", 100.0, 2), ("lp", 6000.0, 2)])
        rig = apply_chain(cut_clean("fs_360633", 4.0, 88.0, tones), [("hp", 250.0, 2), ("lp", 5000.0, 2)])
        mix = water + rig * 10 ** (-8 / 20)
        loop = bed_loop(mix)
        eng = far_engine(150.0, 186.0)
        eng_m = eng if eng.ndim == loop.ndim else (np.stack([eng, eng], axis=1) if loop.ndim > 1 else sl.to_mono(eng))
        add_circular(loop, eng_m * 10 ** (-12 / 20) * np.std(water) / (np.std(eng) + 1e-12), int(22 * RATE))
        meta = {"cuts": [["fs_182611", 12.0, 96.0], ["fs_360633", 4.0, 88.0], ["fs_559821", 150.0, 186.0]],
                "chain": "water: highpass 100, lowpass 6000; rigging -8 dB from highpass 250; a far boat engine (lowpass 700, 8 s fades) at 22 s, -12 dB re the water"}
        return loop, tones_meta(meta, tones)
    if version == "night":
        water = apply_chain(cut_clean("fs_182610", 14.0, 98.0, tones), [("hp", 100.0, 2), ("lp", 3500.0, 4)])
        rig = apply_chain(cut_clean("fs_360633", 20.0, 100.0, tones), [("hp", 250.0, 2), ("lp", 3000.0, 4)])
        n = min(len(water), len(rig))
        mix = water[:n] + rig[:n] * 10 ** (-14 / 20)
        return bed_loop(mix), tones_meta({"cuts": [["fs_182610", 14.0, 98.0], ["fs_360633", 20.0, 100.0]],
                                          "chain": "water highpass 100, lowpass 3500; rigging -14 dB, lowpass 3000"}, tones)
    # rain: a 60 s loop. The Dorset take 182612 carries a steady engine-like drone (73 to 193 Hz) the whole way, so its water is
    # high-passed at 200 Hz; the whistle is 64 s of one 72 s take, so it is not repeated inside the loop
    water = apply_chain(cut_clean("fs_182612", 12.0, 12.0 + SHORT_LOOP_S + XF_S, tones), [("hp", 200.0, 4), ("lp", 4500.0, 4)])
    whistle = apply_chain(cut_clean("fs_463373", 0.0, SHORT_LOOP_S + XF_S, tones), [("hp", 400.0, 2), ("lp", 4000.0, 2)])
    n = min(len(water), len(whistle))
    mix = water[:n] + whistle[:n] * 10 ** (-12 / 20)
    return bed_loop(mix, SHORT_LOOP_S), tones_meta(
        {"cuts": [["fs_182612", 12.0, 12.0 + SHORT_LOOP_S + XF_S], ["fs_463373", 0.0, SHORT_LOOP_S + XF_S]],
         "chain": "water highpass 200 (order 4: the take's drone lies at 73 to 193 Hz), lowpass 4500; rigging whistle -12 dB from highpass 400; a 60 s loop of one uninterrupted cut of each"}, tones)


def build_wind(version):
    tones = {}
    if version == "day":
        # one 64 s cut of the 66.5 s recording, a 60 s loop (the first build spliced three cuts and played 28 s of it twice)
        x = cut_clean("fs_454374", 0.0, SHORT_LOOP_S + XF_S, tones)
        x = apply_chain(x, [("hp", 60.0, 2), ("lp", 2500.0, 2)])
        meta = {"cuts": [["fs_454374", 0.0, SHORT_LOOP_S + XF_S]], "chain": "highpass 60, lowpass 2500; a 60 s loop of one uninterrupted cut"}
        return bed_loop(x, SHORT_LOOP_S), tones_meta(meta, tones)
    if version == "night":
        x = cut_clean("fs_554845", 20.0, 104.0, tones)
        x = apply_chain(x, [("hp", 90.0, 2), ("lp", NIGHT_WIND_LP, 4)])
        meta = {"cuts": [["fs_554845", 20.0, 104.0]], "chain": "highpass 90, lowpass %d (darker than the day wind: the brief's 'lower, darker')" % NIGHT_WIND_LP}
        return bed_loop(x), tones_meta(meta, tones)
    # rain: one 79.5 s cut of the 90.75 s recording (the first build spliced two cuts and played its seconds 41 to 50 twice, back to back)
    x = cut_clean("bsb_625", 0.0, 79.5, tones)
    x = apply_chain(x, [("hp", 90.0, 2), ("lp", 3500.0, 4)])
    meta = {"cuts": [["bsb_625", 0.0, 79.5]], "chain": "highpass 90, lowpass 3500; one uninterrupted cut"}
    return bed_loop(x), tones_meta(meta, tones)


def build_rain(kind):
    tones = {}
    if kind == "rain_pavement":
        x = cut_clean_mono("bsb_1289", 0.0, LOOP_S + XF_S + 0.5, tones)
        x = sl.sos_filter(x, "hp", 120.0, 2)
        meta = {"cuts": [["bsb_1289", 0.0, LOOP_S + XF_S + 0.5]], "chain": "highpass 120 (mono source)"}
    elif kind == "rain_awning":
        x = cut_clean("fs_454130", 0.0, 81.5, tones)
        x = sl.sos_filter(x, "hp", 150.0, 2)
        meta = {"cuts": [["fs_454130", 0.0, 81.5]], "chain": "steady tones notched (117 and 120 Hz hum), highpass 150"}
    else:
        x = cut_clean("fs_846446", 8.0, 92.0, tones)
        x = sl.sos_filter(x, "hp", 250.0, 2)
        meta = {"cuts": [["fs_846446", 8.0, 92.0]], "chain": "highpass 250"}
    return bed_loop(x), tones_meta(meta, tones)


def cut_clean_mono(sid, a, b, tones):
    x, found = detone(sl.seg(S(sid, channels=1), a, b))
    if found:
        tones.setdefault(sid, {}).update(found)
    return x


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


def quiet_start(x):
    """For a loop that is a circle (grains laid round it, so any point can be its start): the sample at which the level changes
    least across the join (a second before against a second after, tried every 0.1 s), among the places where the signal is
    as smooth as everywhere else (no jump larger than 1.5 typical sample steps). Returns the start in samples."""
    m = x if x.ndim == 1 else x.mean(axis=1)
    N = len(m)
    c = np.concatenate([[0.0], np.cumsum(np.concatenate([m, m, m]) ** 2)])
    pos = np.arange(0, N, RATE // 10)
    before = (c[pos + N] - c[pos + N - RATE]) / RATE + 1e-14
    after = (c[pos + N + RATE] - c[pos + N]) / RATE + 1e-14
    step = np.abs(10 * np.log10(before / after))
    typical = np.sqrt(np.mean(np.diff(m) ** 2)) + 1e-12
    step[np.abs(m[pos] - m[pos - 1]) > 1.5 * typical] = 1e9
    return int(pos[int(np.argmin(step))])


def write_loop(name, layer, version, build):
    x, meta = build()
    if layer in ("voices", "radio"):                # grains laid round a circle: start the file where the level changes least
        shift = quiet_start(x)
        x = np.roll(x, -shift, axis=0)
        n_ms = int(round(len(x) * 1000.0 / RATE))
        meta["plan"]["pos_ms"] = [(p - int(round(shift * 1000.0 / RATE))) % n_ms for p in meta["plan"]["pos_ms"]]
        meta["starts_at_circle_s"] = round(shift / RATE, 2)
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
    # The two puddle takes are noisy and hold few single steps: judged against the step's own peak, only 1 footfall dies away by 20 dB,
    # 4 by 14 dB and 8 by 12 dB. So the wet set takes the 8 that die away by 12 dB (BRIEF.md: step_cut_db), with a long (40 ms) fade-out
    # and an 8 ms fade-in, and the brighter splash a puddle makes (centroid up to 6 kHz).
    "wet": [("fs_263495", 70.0, dict(WET_OPTS)), ("fs_531566", 70.0, dict(WET_OPTS))],
    "wood": [("fs_536770", 70.0, {}), ("fs_575898", 70.0, {})],
}
STEP_OPTS = dict(min_transients=1, centroid_range=(300.0, 3500.0), max_ms=260.0, died_db=STEP_CUT_DB["default"], pre_db=STEP_CUT_DB["default"])
STEPS_PER_SURFACE = 8


def build_steps(surface):
    cand = []   # (source, start sample, samples, measures)
    for sid, hp, opts in STEP_TAKES[surface]:
        m = stepcut.highpass(sl.to_mono(S(sid)), hp)
        for a, st, info in stepcut.cut(m, **dict(STEP_OPTS, **opts)):
            cand.append((sid, a, st, info))
    if len(cand) < STEPS_PER_SURFACE:
        raise SystemExit("%s: only %d clean steps found" % (surface, len(cand)))
    loud = np.array([sl.momentary_max(st) for _, _, st, _ in cand])
    # a step whose peak stands more than 25 dB over its momentary loudness cannot reach the target without passing -1.5 dBTP
    crest = np.array([sl.true_peak_db(st) - l for (_, _, st, _), l in zip(cand, loud)])
    keep = np.flatnonzero(crest <= -1.5 - SHOT_TARGET["step"])
    if len(keep) >= 3 * STEPS_PER_SURFACE:
        cand, loud = [cand[i] for i in keep], loud[keep]
    # distinct choice across sources; any two of the eight must also correlate under 0.8 (the check allows 0.9)
    pairs = [(a + (hash_name(sid) % 1000) * 10 ** 7, st) for sid, a, st, _ in cand]   # keep takes apart in the time test
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
        sid, a, st, info = cand[i]
        name = "step_%s_%02d" % (surface, k)
        meta = {"sources": [sid], "cut_at_s": round(a / RATE, 3), "length_ms": round(1000 * len(st) / RATE), "highpass_hz": 70.0, "keep_edges": True,
                "cutter": dict(info, fade_out_ms=dict(STEP_TAKES[surface][0][2]).get("fade_ms", 15.0), fade_in_ms=dict(STEP_TAKES[surface][0][2]).get("fade_in_ms", 2.0))}
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
        "rate": RATE, "loop_seconds_max": LOOP_S, "loop_seconds_short": SHORT_LOOP_S, "loop_crossfade_seconds": XF_S,
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
    if not only:                      # a full run also makes the nine listening clips (audio: kept out of git; see make_previews.make_clips)
        import make_previews
        make_previews.make_clips()
        print("9 listening clips written to %s and %s" % (make_previews.PREV, os.path.join(sl.OUT_DIR, "clips")))


if __name__ == "__main__":
    main()
