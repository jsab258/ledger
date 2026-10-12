#!/usr/bin/env python3
"""The automatic check of Quay Street's sound against BRIEF.md (unit 10, cloud week 42).

    python check_sound.py              # checks SOUND_OUT, writes checks/check_v1.json, prints "N of M rows pass"
    python check_sound.py --out v2     # writes checks/check_v2.json instead

One row per test: each of BRIEF.md's automatic acceptance cases (numbers 1 to 16 and 22 to 25) and each file. A missing output fails
by name. Every number comes from BRIEF.md's targets-json block. This script does not import make_sound.py: loop loudness
and true peak are measured with ffmpeg's own ebur128 filter (a second implementation of BS.1770), the seam and the
rest with code written here, so a fault in the build cannot pass its own check.
"""
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("SOUND_OUT", "/home/user/ledger-scratch/sound-out")
SOURCES_DIR = os.environ.get("SOUND_SOURCES", "/home/user/ledger-scratch/sound-sources")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PREVIEWS = os.path.join(REPO, "production", "previews", "cloud-week", "sound")
RATE = 48000

LAYERS = ["traffic", "gulls", "harbour", "wind", "voices", "radio"]
SURFACES = ["paving", "setts", "asphalt", "wet", "wood"]
SPEC_PREVIEWS = ["spec_%s.jpg" % n for n in LAYERS + ["rain"]] + ["spec_steps_%s.jpg" % s for s in SURFACES] + \
                ["spec_doors_shop.jpg", "spec_doors_house.jpg", "spec_bell.jpg", "spec_phonebox.jpg"]
CLIP_PREVIEWS = ["clip_mix_day.ogg", "clip_mix_night.ogg", "clip_mix_rain.ogg"] + ["clip_steps_%s.ogg" % s for s in SURFACES] + ["clip_doors.ogg"]
CC0_TEXT = {"Creative Commons 0", "CC0 (public domain)"}
# words that would put something the content rule or the era forbids into a source (case-insensitive, whole words)
FORBIDDEN = ["child", "children", "kid", "kids", "baby", "babies", "toddler", "playground", "school", "pupil", "pub", "bar", "beer", "wine",
             "alcohol", "drunk", "pint", "gambling", "casino", "betting", "racing", "ice cream", "cellphone", "iphone",
             "smartphone", "ringtone", "car alarm", "reversing", "electric car", "lyrics", "song", "music", "bbc", "radio station"]

rows = []


def add(case, test, ok, detail="", file=None):
    rows.append({"case": case, "test": test, "file": file, "pass": bool(ok), "detail": detail})


# ------------------------------------------------------------------------------------------------ readers
def read_wav(path):
    with wave.open(path, "rb") as w:
        ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    a = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0 if sw == 2 else None
    if a is not None and ch > 1:
        a = a.reshape(-1, ch)
    return a, ch, sw * 8, sr, raw


def ffmpeg_loudness(path, pad_to=None):
    """(integrated LUFS, true peak dBTP, highest momentary LUFS) from ffmpeg's ebur128; pad_to pads a short clip with silence."""
    af = ("apad=whole_dur=%s," % pad_to if pad_to else "") + "ebur128=peak=true:framelog=verbose"
    r = subprocess.run(["ffmpeg", "-v", "verbose", "-hide_banner", "-nostats", "-i", path, "-af", af, "-f", "null", "-"],
                       capture_output=True, text=True)
    t = r.stderr
    summ = t[t.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", summ)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
    ms = [float(x) for x in re.findall(r" M:\s*(-?[\d.]+) ", t)]
    return (float(i.group(1)) if i else None, float(tp.group(1)) if tp else None, max(ms) if ms else None)


def seam(m):
    """Own measure of how a loop closes (see BRIEF.md case 6)."""
    n = 2 * RATE
    d = np.diff(np.concatenate([m[-n:], m[:n]]))
    typical = np.sqrt(np.mean(np.delete(d, n - 1) ** 2)) + 1e-12
    jump = abs(m[0] - m[-1]) / typical
    w = RATE
    c = np.concatenate([[0.0], np.cumsum(np.concatenate([m, m, m]) ** 2)])
    N = len(m)
    pos = np.arange(0, N, RATE // 10)
    before = (c[pos + N] - c[pos + N - w]) / w + 1e-14
    after = (c[pos + N + w] - c[pos + N]) / w + 1e-14
    step = np.abs(10 * np.log10(before / after))
    return float(jump), float(step[0]), float(np.mean(step[1:] < step[0]))


def centroid(m):
    X = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2
    f = np.fft.rfftfreq(len(m), 1.0 / RATE)
    return float((X * f).sum() / X.sum())


def hf_fraction(m, f0=2500.0):
    X = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2
    f = np.fft.rfftfreq(len(m), 1.0 / RATE)
    return float(X[f > f0].sum() / X.sum())


def max_xcorr(a, b):
    n = len(a) + len(b)
    nf = 1 << (n - 1).bit_length()
    A, B = np.fft.rfft(a, nf), np.fft.rfft(b, nf)
    c = np.fft.irfft(A * np.conj(B), nf)
    return float(np.abs(c).max() / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def mono(x):
    return x if x.ndim == 1 else x.mean(axis=1)


def channels(x):
    return [x] if x.ndim == 1 else [x[:, c] for c in range(x.shape[1])]


def spectral_stats(m):
    """(centroid Hz, 95 percent roll-off Hz, {band: share of power}) of a loop, from a Welch spectrum."""
    f, P = signal.welch(m, fs=RATE, nperseg=16384)
    tot = P.sum()
    share = lambda a, b: float(P[(f >= a) & (f < b)].sum() / tot)
    return (float((P * f).sum() / tot), float(f[np.searchsorted(np.cumsum(P) / tot, 0.95)]),
            {"lt250": share(0, 250), "300_3000": share(300, 3000), "1000_2500": share(1000, 2500)})


def level_spread_db(m, lo=10, hi=95):
    """How much the 100 ms level moves: the 10th to 95th percentile of the 100 ms RMS in dB."""
    n = RATE // 10
    k = len(m) // n
    e = 10 * np.log10((m[:k * n].reshape(k, n) ** 2).mean(axis=1) + 1e-14)
    return float(np.percentile(e, hi) - np.percentile(e, lo))


def gap_fraction(m, below_db=15.0):
    """The share of 100 ms frames more than below_db under the loop's loud frames (its 90th percentile level)."""
    n = RATE // 10
    k = len(m) // n
    e = 10 * np.log10((m[:k * n].reshape(k, n) ** 2).mean(axis=1) + 1e-14)
    return float(np.mean(e < np.percentile(e, 90) - below_db))


def gull_calls(m, thr_db=-45.0, merge_s=1.5, min_s=0.15):
    """Gull calls counted from the audio: sound above thr_db under the loop's loudest 50 ms (high-passed at 500 Hz), runs closer
    than merge_s joined (a call and its tail, or a run of calls), runs shorter than min_s dropped."""
    y = signal.sosfilt(signal.butter(2, 500.0, btype="highpass", fs=RATE, output="sos"), m)
    n = int(0.05 * RATE)
    e = np.sqrt(np.convolve(y * y, np.ones(n) / n, "same"))
    act = e > e.max() * 10 ** (thr_db / 20)
    idx = np.flatnonzero(np.diff(np.concatenate([[0], act.astype(int), [0]])))
    runs = []
    for i in range(0, len(idx), 2):
        a, b = int(idx[i]), int(idx[i + 1])
        if runs and a - runs[-1][1] < merge_s * RATE:
            runs[-1][1] = b
        else:
            runs.append([a, b])
    return sum(1 for a, b in runs if (b - a) / RATE >= min_s)


def repeat_scan(m, p):
    """Does any part of a loop play twice inside it? The loop (one channel, taken down to RATE/p) is read in windows of window_s
    every hop_s; each window is compared, by normalised waveform correlation, with the whole loop taken as a circle, at every lag
    from min_lag_s up to half the loop (nearer than that, the same sound is compared with itself). Returns (highest correlation,
    window start s, other start s). A window with no sound in it is skipped, and so is a place with under 5 percent of its amplitude.
    1.0 is a repeat, about 0.1 is two different stretches of noise."""
    fs = RATE // p["decimate"]
    x = signal.resample_poly(m, 1, p["decimate"])
    N, W, H = len(x), int(p["window_s"] * fs), int(p["hop_s"] * fs)
    X = np.fft.rfft(x)
    e = np.concatenate([[0.0], np.cumsum(np.concatenate([x, x]) ** 2)])
    ex = np.sqrt(np.maximum(e[np.arange(N) + W] - e[np.arange(N)], 1e-18))
    lag_ok = lambda t0: ((np.arange(N) - t0) % N >= int(p["min_lag_s"] * fs)) & ((np.arange(N) - t0) % N <= N // 2)
    best = (0.0, 0.0, 0.0)
    for t0 in range(0, N, H):
        w = x[(np.arange(W) + t0) % N]
        ew = np.sqrt(np.sum(w * w))
        if ew < 1e-6:
            continue
        wp = np.zeros(N)
        wp[:W] = w
        c = np.fft.irfft(X * np.conj(np.fft.rfft(wp)), N) / (ew * ex)
        v = np.where(lag_ok(t0) & (ex > 0.05 * ew), np.abs(c), 0.0)
        i = int(np.argmax(v))
        if v[i] > best[0]:
            best = (float(v[i]), t0 / fs, i / fs)
    return best


def steady_tones(m, p):
    """The steady tones of one channel: it is read in 1 s frames (1 Hz bins), each bin takes its level as the median over the frames
    (so what stands there in the quiet stretches counts), and a peak's prominence is its level over the median level of the
    bins 5 to 60 Hz either side of it. Returns [(Hz, dB over its neighbours)] for the highest three peaks between fmin and fmax."""
    f, _, S = signal.spectrogram(m, fs=RATE, window="hann", nperseg=RATE, noverlap=RATE // 2, detrend=False, mode="psd")
    S = S[:, S.sum(axis=0) > 1e-14]
    D = np.median(10 * np.log10(S + 1e-22), axis=1)
    lo, hi = p["near_hz"]
    offs = np.concatenate([np.arange(-hi, -lo + 1), np.arange(lo, hi + 1)])
    cand = np.flatnonzero((f >= p["fmin_hz"]) & (f <= p["fmax_hz"]))
    prom = np.zeros(len(D))
    prom[cand] = D[cand] - np.median(np.stack([D[np.clip(cand + o, 0, len(D) - 1)] for o in offs]), axis=0)
    peaks = [i for i in cand if prom[i] > 0 and prom[i] >= prom[i - 1] and prom[i] >= prom[i + 1]]
    peaks.sort(key=lambda i: -prom[i])
    out = []
    for i in peaks:
        if all(abs(i - j) > 8 for j, _ in out):
            out.append((i, prom[i]))
        if len(out) >= 3:
            break
    return [(float(f[i]), float(v)) for i, v in out]


def grain_runs(plan, N_ms, near_ms=320, gap_ms=50):
    """From a speech loop's grain plan (what the build recorded of every grain: source, start and length in the source, place in the
    loop, all in ms): (the longest grain, the longest run, the shortest distance in loop time between two grains that use
    overlapping places of a source). A run is a chain of grains that start within near_ms of each other (round the circle) and
    whose places in a source touch or lie within gap_ms of each other; its length is the stretch of source it covers. Written
    here, not shared with the build."""
    src, st, ln, pos = (np.array(plan["plan"][k]) for k in ("src", "start_ms", "len_ms", "pos_ms"))
    n = len(pos)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    reuse = 1e9
    for j in range(n):
        d = np.abs(pos[j + 1:] - pos[j])
        d = np.minimum(d, N_ms - d)
        later = slice(j + 1, n)
        same = src[later] == src[j]
        overlap = same & (st[later] < st[j] + ln[j]) & (st[j] < st[later] + ln[later])
        if overlap.any():
            reuse = min(reuse, float(d[overlap].min()) / 1000.0)
        touch = same & (d < near_ms) & (st[later] < st[j] + ln[j] + gap_ms) & (st[j] < st[later] + ln[later] + gap_ms)
        for i in np.flatnonzero(touch):
            parent[find(int(i) + j + 1)] = find(j)
    groups = {}
    for j in range(n):
        groups.setdefault(find(j), []).append(j)
    run = max(max(st[i] + ln[i] for i in g) - min(st[i] for i in g) for g in groups.values())
    return int(ln.max()), int(run), reuse


_src_cache = {}


def source_mono(path):
    """A source as the footstep cutter reads it: decoded to stereo at 48 kHz, the two channels averaged, and the rumble taken off with
    a high-pass that rises from nothing at 50 Hz to everything at 70 Hz (the definition in BRIEF.md; written here, not shared)."""
    if path not in _src_cache:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(RATE), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        a = np.frombuffer(raw, dtype=np.float32).astype(np.float64).reshape(-1, 2).mean(axis=1)
        F = np.fft.rfft(a)
        F *= np.clip((np.fft.rfftfreq(len(a), 1.0 / RATE) - 50.0) / 20.0, 0.0, 1.0)
        _src_cache[path] = np.fft.irfft(F, len(a))
    return _src_cache[path]


def rms_env(x, ms):
    n = max(1, int(RATE * ms / 1000.0))
    return np.sqrt(np.convolve(x * x, np.ones(n) / n, "same"))


def step_end_db(x):
    """How far under its loudest 5 ms the last 20 ms of a footstep (as written) still is."""
    e = rms_env(x, 5.0)
    return float(20 * np.log10(e[-int(0.02 * RATE):].max() / e.max() + 1e-12))


def step_pre_db(src_path, cut_s, length_ms):
    """Measured on the source: how far under the footstep's loudest 5 ms the 20 ms before its cut lies. Near 0 means the step
    starts inside a sound already going, and the fade-in then makes a second onset."""
    m = source_mono(src_path)
    a = int(round(cut_s * RATE))
    e = rms_env(m, 5.0)
    peak = e[a:a + int(length_ms / 1000.0 * RATE)].max()
    lo, hi = a - int(0.0225 * RATE), a - int(0.0025 * RATE)
    if lo < 0:
        return 0.0
    return float(20 * np.log10(e[lo:hi].max() / peak + 1e-12))


# --------------------------------------------------------------------------------------------------- main
def main():
    tag = "v1"
    if "--out" in sys.argv:
        tag = sys.argv[sys.argv.index("--out") + 1]
    brief = open(os.path.join(HERE, "BRIEF.md"), encoding="utf8").read()
    a = brief.index("```targets-json") + len("```targets-json")
    T = json.loads(brief[a:brief.index("```", a)])
    manifest = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf8"))["outputs"] if os.path.exists(os.path.join(HERE, "manifest.json")) else {}
    sources = {s["id"]: s for s in json.load(open(os.path.join(HERE, "sources.json"), encoding="utf8"))["sources"]}

    files = sorted(f for f in os.listdir(OUT_DIR) if f.endswith(".wav")) if os.path.isdir(OUT_DIR) else []
    names = {f[:-4] for f in files}

    # case 1: inventory ---------------------------------------------------------------------------------
    loops = sorted(T["loops_lufs"])
    for n in loops:
        add(1, "loop exists", n in names, "" if n in names else "MISSING %s.wav" % n, n + ".wav")
    groups = {}
    for n in names:
        g = re.sub(r"_\d+$", "", n)
        groups.setdefault(g, []).append(n)
    for g, need in sorted(T["min_variants"].items()):
        have = len(groups.get(g, []))
        add(1, "at least %d variants of %s" % (need, g), have >= need, "%d found%s" % (have, "" if have >= need else " (MISSING %d)" % (need - have)))

    shots = sorted(n for g, v in groups.items() if g in T["min_variants"] for n in v)
    present_loops = [n for n in loops if n in names]
    expected = present_loops + shots

    # classes of one-shots for the loudness target
    def shot_class(n):
        g = re.sub(r"_\d+$", "", n)
        if g.startswith("step_"):
            return "step"
        if g.endswith("_open"):
            return "door_open"
        if g.endswith("_close"):
            return "door_close"
        if g.endswith("_latch"):
            return "door_latch"
        return {"bell_shop": "bell", "phonebox_door_creak": "phonebox_creak", "phonebox_door_shut": "phonebox_shut", "phonebox_ring": "phonebox_ring"}[g]

    audio = {}
    loud_I = {}
    tmp = tempfile.mkdtemp(prefix="soundcheck_")
    for n in expected:
        p = os.path.join(OUT_DIR, n + ".wav")
        x, ch, bits, sr, raw = read_wav(p)
        audio[n] = x
        is_loop = n in T["loops_lufs"]
        # case 2: format
        add(2, "WAV 16-bit 48 kHz", bits == 16 and sr == RATE, "%d-bit %d Hz %d ch" % (bits, sr, ch), n + ".wav")
        if is_loop:
            sec = len(x) / RATE
            add(2, "loop is %g to %g s" % (T["loop_seconds_min"], T["loop_seconds_max"]), T["loop_seconds_min"] - 0.01 <= sec <= T["loop_seconds_max"] + 0.01, "%.2f s" % sec, n + ".wav")
            add(3, "loop at least %d s" % T["loop_seconds_min"], sec >= T["loop_seconds_min"], "%.1f s" % sec, n + ".wav")
            I, tp, _ = ffmpeg_loudness(p)
            loud_I[n] = I
            tgt = T["loops_lufs"][n]
            add(4, "integrated loudness within %.1f LU of %.1f" % (T["loop_lufs_tolerance"], tgt), I is not None and abs(I - tgt) <= T["loop_lufs_tolerance"],
                "%.2f LUFS" % I if I is not None else "unmeasured", n + ".wav")
            add(5, "true peak at most %.1f dBTP" % T["true_peak_max_dbtp"], tp is not None and tp <= T["true_peak_max_dbtp"], "%.2f dBTP" % tp if tp is not None else "unmeasured", n + ".wav")
            m = x if x.ndim == 1 else x.mean(axis=1)
            j, st, pc = seam(m)
            add(6, "no click at the seam (jump at most %.1f)" % T["seam_jump_max"], j <= T["seam_jump_max"], "jump %.2f x typical step" % j, n + ".wav")
            add(6, "no level step across the seam", st <= T["seam_step_ok_db"] or pc <= T["seam_step_percentile_max"],
                "%.2f dB, larger than at %.0f%% of other places" % (st, 100 * pc), n + ".wav")
            rp = T["repeat"]
            best = max((repeat_scan(c, rp) for c in channels(x)), key=lambda r: r[0])
            add(22, "no part of the loop plays twice inside it (%g s windows, lags %g s to half the loop, correlation at most %.2f)" % (rp["window_s"], rp["min_lag_s"], rp["max_correlation"]),
                best[0] <= rp["max_correlation"], "highest correlation %.2f (the window at %.0f s against the loop at %.0f s)" % best, n + ".wav")
            tn = T["tone"]
            worst = None
            for ci, c in enumerate(channels(x)):
                pk = steady_tones(c, tn)
                if pk and (worst is None or pk[0][1] > worst[2]):
                    worst = (("left", "right")[ci] if x.ndim > 1 else "mono", pk[0][0], pk[0][1])
            add(23, "no steady tone stands more than %g dB over its neighbours" % tn["margin_db"], worst is not None and worst[2] <= tn["margin_db"],
                "highest peak +%.1f dB at %.0f Hz (%s)" % (worst[2], worst[1], worst[0]) if worst else "no peak found", n + ".wav")
        else:
            add(2, "one-shot is mono", ch == 1, "%d ch" % ch, n + ".wav")
            I, tp, M = ffmpeg_loudness(p, pad_to=1.5)
            tgt = T["one_shot_lufs_m"][shot_class(n)]
            lim = bool(manifest.get(n, {}).get("limited_by_peak"))
            ok = M is not None and ((abs(M - tgt) <= T["one_shot_tolerance"]) or (M < tgt and lim))
            add(7, "momentary loudness within %.1f LU of %.1f, or lower and peak-limited" % (T["one_shot_tolerance"], tgt), ok,
                "%.2f LUFS-M%s" % (M, " (peak-limited)" if lim else "") if M is not None else "unmeasured", n + ".wav")
            add(5, "true peak at most %.1f dBTP" % T["true_peak_max_dbtp"], tp is not None and tp <= T["true_peak_max_dbtp"], "%.2f dBTP" % tp if tp is not None else "unmeasured", n + ".wav")
            m = x
            head, tail = abs(m[0]), np.abs(m[-int(0.002 * RATE):]).max()
            add(8, "no click at either end", head <= 10 ** (-50 / 20) and tail <= 10 ** (-50 / 20), "start %.1f dBFS, end %.1f dBFS" % (20 * np.log10(head + 1e-9), 20 * np.log10(tail + 1e-9)), n + ".wav")
            if n.startswith("step_"):
                kind = "step_wet" if n.startswith("step_wet_") else "default"
                end_db = step_end_db(x)
                lim = T["step_end_db_max"][kind]
                add(24, "the step has died away at its end (last 20 ms at least %g dB under its peak)" % -lim, end_db <= lim, "%.1f dB" % end_db, n + ".wav")
                b = manifest.get(n, {}).get("build", {})
                sfile = sources.get((manifest.get(n, {}).get("sources") or ["?"])[0], {}).get("file")
                if sfile and os.path.exists(os.path.join(SOURCES_DIR, sfile)) and "cut_at_s" in b:
                    pre = step_pre_db(os.path.join(SOURCES_DIR, sfile), b["cut_at_s"], b["length_ms"])
                    plim = T["step_pre_db_max"][kind]
                    add(24, "the step does not start inside a sound (the 20 ms before its cut in the source at least %g dB under its peak)" % -plim, pre <= plim, "%.1f dB" % pre, n + ".wav")
                else:
                    add(24, "the step does not start inside a sound (the 20 ms before its cut in the source at least %g dB under its peak)" % -T["step_pre_db_max"][kind], False, "source or cut point missing", n + ".wav")
        add(5, "no clipping (no full-scale sample)", float(np.abs(x).max()) < 0.999, "peak %.2f dBFS" % (20 * np.log10(np.abs(x).max() + 1e-12)), n + ".wav")
        add(15, "sha256 matches manifest.json", n in manifest and manifest[n].get("sha256") == sha256(p),
            "" if n in manifest else "no manifest row", n + ".wav")
        # case 13: licence rows
        srcs = manifest.get(n, {}).get("sources", [])
        okrows = bool(srcs) and all(
            s in sources and all(sources[s].get(k) for k in ("page_url", "author", "licence", "date_read", "download_url", "md5", "title")) for s in srcs)
        add(13, "every source has a full row in sources.json", okrows, ", ".join(srcs) if srcs else "no sources listed in manifest", n + ".wav")

    # case 9: footstep variants differ -------------------------------------------------------------------
    for s in SURFACES:
        g = sorted(n for n in names if re.fullmatch(r"step_%s_\d+" % s, n))
        worst, pair = 0.0, None
        for i in range(len(g)):
            for k in range(i + 1, len(g)):
                if g[i] in audio and g[k] in audio:
                    c = max_xcorr(audio[g[i]], audio[g[k]])
                    if c > worst:
                        worst, pair = c, (g[i], g[k])
        hashes = [sha256(os.path.join(OUT_DIR, n + ".wav")) for n in g]
        add(9, "variants of step_%s differ (no pair above %.2f, none identical)" % (s, T["step_variant_max_correlation"]),
            len(g) > 1 and worst <= T["step_variant_max_correlation"] and len(set(hashes)) == len(hashes),
            "closest pair %s correlate %.2f" % (pair, worst) if pair else "no pair", "step_%s_*" % s)

    # case 10: the three beds ---------------------------------------------------------------------------
    for v in ("day", "night", "rain"):
        parts = ["amb_%s_%s" % (l, v) for l in LAYERS] + (["amb_rain_pavement", "amb_rain_awning", "amb_rain_gutter"] if v == "rain" else [])
        if not all(p in audio for p in parts):
            add(10, "%s bed mix measures within %.1f LU of %.1f" % (v, T["bed_mix_tolerance"], T["bed_mix_lufs"][v]), False, "MISSING " + ", ".join(p for p in parts if p not in audio))
            continue
        tot = None
        lens = {len(audio[p]) for p in parts}
        L = math.lcm(*lens)                  # loops of 60 and 75 s come round together every 300 s: the mix is measured over that
        if L > 600 * RATE:
            L = max(lens)
        for p in parts:
            x = audio[p]
            x = np.stack([x, x], axis=1) * np.sqrt(0.5) if x.ndim == 1 else x
            x = np.concatenate([x] * (-(-L // len(x))))[:L].astype(np.float32)
            tot = x if tot is None else tot + x
        path = os.path.join(tmp, "mix_%s.wav" % v)
        pcm = (np.clip(tot, -1, 1) * 32767).astype("<i2")
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(pcm.tobytes())
        I, tp, _ = ffmpeg_loudness(path)
        T.setdefault("_mix", {})[v] = I
        add(10, "%s bed mix measures within %.1f LU of %.1f" % (v, T["bed_mix_tolerance"], T["bed_mix_lufs"][v]), I is not None and abs(I - T["bed_mix_lufs"][v]) <= T["bed_mix_tolerance"], "%.2f LUFS" % I if I is not None else "unmeasured")
        add(5, "%s bed mix true peak at most %.1f dBTP" % (v, T["true_peak_max_dbtp"]), tp is not None and tp <= T["true_peak_max_dbtp"], "%.2f dBTP" % tp if tp is not None else "unmeasured")
    mix = T.get("_mix", {})
    if len(mix) == 3:
        add(10, "night bed at least 2 LU under day", mix["night"] <= mix["day"] - 2.0, "night %.1f, day %.1f" % (mix["night"], mix["day"]))
        add(10, "rain bed at least 2 LU over day", mix["rain"] >= mix["day"] + 2.0, "rain %.1f, day %.1f" % (mix["rain"], mix["day"]))

    # case 11: what changes between versions ---------------------------------------------------------------
    if "amb_traffic_day" in audio and "amb_traffic_rain" in audio:
        cd, cr = (centroid(audio[n] if audio[n].ndim == 1 else audio[n].mean(axis=1)) for n in ("amb_traffic_day", "amb_traffic_rain"))
        add(11, "rain traffic's spectral centroid above day traffic's", cr > cd, "rain %.0f Hz, day %.0f Hz" % (cr, cd))
    cnt = {v: manifest.get("amb_gulls_%s" % v, {}).get("build", {}).get("call_count") for v in ("day", "night", "rain")}
    add(11, "night gulls: fewer calls than day and at most three", cnt["night"] is not None and cnt["day"] is not None and cnt["night"] < cnt["day"] and cnt["night"] <= 3, "calls day %s, night %s, rain %s" % (cnt["day"], cnt["night"], cnt["rain"]))
    add(11, "rain gulls: fewer calls than day", cnt["rain"] is not None and cnt["day"] is not None and cnt["rain"] < cnt["day"], "rain %s, day %s" % (cnt["rain"], cnt["day"]))
    heard = {}
    for v in ("day", "night", "rain"):
        if "amb_gulls_%s" % v in audio:
            heard[v] = gull_calls(mono(audio["amb_gulls_%s" % v]))
    if len(heard) == 3:
        add(11, "gull calls counted from the audio: night fewer than day and at most three, rain fewer than day",
            heard["night"] < heard["day"] and heard["night"] <= 3 and heard["rain"] < heard["day"], "heard day %d, night %d, rain %d" % (heard["day"], heard["night"], heard["rain"]))
        add(11, "gull calls heard in the audio agree with the build's record (within one)", all(cnt[v] is not None and abs(heard[v] - cnt[v]) <= 1 for v in heard),
            "heard %s, recorded %s" % ([heard[v] for v in ("day", "night", "rain")], [cnt[v] for v in ("day", "night", "rain")]))
    if "amb_wind_day" in audio and "amb_wind_night" in audio:
        wd, wn = mono(audio["amb_wind_day"]), mono(audio["amb_wind_night"])
        cd, cn = centroid(wd), centroid(wn)
        add(11, "night wind is darker than day wind (spectral centroid)", cn < cd, "night %.0f Hz, day %.0f Hz" % (cn, cd))
        add(11, "night wind is quieter than day wind (integrated loudness)", loud_I.get("amb_wind_night") is not None and loud_I["amb_wind_night"] < loud_I["amb_wind_day"],
            "night %.2f LUFS, day %.2f LUFS" % (loud_I["amb_wind_night"], loud_I["amb_wind_day"]))
        sd, sn = level_spread_db(wd), level_spread_db(wn)
        add(11, "night wind is steadier than day wind (spread of its 100 ms level, 10th to 95th percentile)", sn < sd, "night %.1f dB, day %.1f dB" % (sn, sd))

    # case 12: voices and radio indistinct -------------------------------------------------------------------
    for layer in ("voices", "radio"):
        for v in ("day", "night", "rain"):
            n = "amb_%s_%s" % (layer, v)
            if n not in audio:
                continue
            plan = manifest.get(n, {}).get("build", {})
            if plan.get("plan"):
                longest, run, reuse = grain_runs(plan, int(round(len(audio[n]) * 1000.0 / RATE)))
                add(12, "no grain longer than %d ms (every grain of the build's record)" % T["grain_ms_max"], longest <= T["grain_ms_max"], "longest grain %d ms of %d" % (longest, len(plan["plan"]["src"])), n + ".wav")
                add(12, "no run of speech longer than %d ms (no grain continues another)" % T["grain_ms_max"], run <= T["grain_ms_max"], "longest run %d ms" % run, n + ".wav")
                need = T["grain_reuse_min_s"][n]
                add(12, "no moment of the recording comes back within %g s" % need, reuse >= need, "shortest return %.1f s" % reuse, n + ".wav")
            else:
                for what in ("no grain longer than %d ms" % T["grain_ms_max"], "no run of speech longer than %d ms" % T["grain_ms_max"], "no moment of the recording comes back"):
                    add(12, what, False, "no grain record in manifest.json", n + ".wav")
            hf = hf_fraction(audio[n])
            add(12, "power above 2.5 kHz at most %.1f%%" % (100 * T["voice_hf_fraction_max"]), hf <= T["voice_hf_fraction_max"], "%.4f%%" % (100 * hf), n + ".wav")

    # case 25: the radio is a radio, not more voices --------------------------------------------------------
    rd = T["radio"]
    for v in ("day", "night", "rain"):
        rn, vn = "amb_radio_%s" % v, "amb_voices_%s" % v
        if rn not in audio or vn not in audio:
            continue
        _, r95, rsh = spectral_stats(mono(audio[rn]))
        _, v95, _ = spectral_stats(mono(audio[vn]))
        add(25, "radio holds no hum: at most %.1f%% of its power under 250 Hz" % (100 * rd["lt250_max"]), rsh["lt250"] <= rd["lt250_max"], "%.2f%%" % (100 * rsh["lt250"]), rn + ".wav")
        add(25, "radio is a band of its own: at least %.0f%% of its power between 300 Hz and 3 kHz" % (100 * rd["band_min"]), rsh["300_3000"] >= rd["band_min"], "%.1f%%" % (100 * rsh["300_3000"]), rn + ".wav")
        add(25, "radio has more midrange than the voices: its 95%% roll-off at least %d Hz above the %s voices'" % (rd["roll95_over_voices_hz"], v), r95 - v95 >= rd["roll95_over_voices_hz"],
            "radio %.0f Hz, voices %.0f Hz" % (r95, v95), rn + ".wav")
        gf = gap_fraction(mono(audio[rn]))
        add(25, "radio is intermittent: at least %.0f%% of its 100 ms frames lie 15 dB or more under its loud ones" % (100 * rd["gap_fraction_min"]), gf >= rd["gap_fraction_min"], "%.0f%%" % (100 * gf), rn + ".wav")

    # case 14: licences and content words ------------------------------------------------------------------------
    used = sorted({s for n in expected for s in manifest.get(n, {}).get("sources", [])})
    for sid in sorted(sources):
        s = sources[sid]
        add(13, "source file on disk matches its md5", os.path.exists(os.path.join(SOURCES_DIR, s.get("file", "?"))) and
            hashlib.md5(open(os.path.join(SOURCES_DIR, s["file"]), "rb").read()).hexdigest() == s.get("md5"), s.get("file", "no file"), sid)
        add(14, "licence reads CC0 on the page", s.get("licence") in CC0_TEXT and "publicdomain/zero" in (s.get("licence_url") or ""), "%s | %s" % (s.get("licence"), s.get("licence_url")), sid)
        text = " ".join(str(s.get(k) or "") for k in ("title", "description_on_page", "page_title")).lower()
        hits = [w for w in FORBIDDEN if re.search(r"(?<![a-z])%s(?![a-z])" % re.escape(w), text)]
        add(14, "title and page text hold no content-rule word", not hits, ", ".join(hits) if hits else "clean", sid)
    add(13, "every source in sources.json is used by an output", set(sources) <= set(used), "unused: %s" % (sorted(set(sources) - set(used)) or "none"))
    for sid in sorted(sources):
        if sources[sid].get("host") == "freesound":
            add(13, "a Freesound source has the date its page gives for the upload", bool(sources[sid].get("uploaded")), str(sources[sid].get("uploaded")), sid)

    # case 16: previews ------------------------------------------------------------------------------------------
    for f in SPEC_PREVIEWS:
        p = os.path.join(PREVIEWS, f)
        ok = os.path.exists(p) and os.path.getsize(p) < 500 * 1024
        add(16, "spectrogram JPEG exists, under 500 KB", ok, "%d KB" % (os.path.getsize(p) // 1024) if os.path.exists(p) else "MISSING", f)
    for f in CLIP_PREVIEWS:
        p = os.path.join(PREVIEWS, f)
        if not os.path.exists(p):
            add(16, "listening clip exists, at most 20 s and under 300 KB", False, "MISSING", f)
            continue
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() or 0)
        codec = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip().strip(",")
        add(16, "listening clip is Vorbis, at most 20 s, under 300 KB", codec == "vorbis" and dur <= 20.05 and os.path.getsize(p) < 300 * 1024,
            "%s %.1f s %d KB" % (codec, dur, os.path.getsize(p) // 1024), f)

    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)

    passed = sum(1 for r in rows if r["pass"])
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    out = {"check": "check_sound.py %s" % tag, "brief": "BRIEF.md", "outputs_dir": OUT_DIR, "rows_pass": passed, "rows_total": len(rows),
           "failing": [{"case": r["case"], "test": r["test"], "file": r["file"], "detail": r["detail"]} for r in rows if not r["pass"]], "rows": rows}
    with open(os.path.join(HERE, "checks", "check_%s.json" % tag), "w", encoding="utf8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    for r in rows:
        if not r["pass"]:
            print("FAIL case %d: %s: %s (%s)" % (r["case"], r["file"] or "-", r["test"], r["detail"]))
    print("%d of %d rows pass" % (passed, len(rows)))
    return 0 if passed == len(rows) else 1


def negative_controls():
    """Break eleven outputs on purpose in a scratch copy and require the check to fail each one by name, and show the two grain tests on
    records made up here. Run: check_sound.py --negative-controls
    The first six are the first build's; the next five (a repeat put in, a tone put in, a footstep cut off, a night wind brighter than
    the day's, a radio that is only voices) and the two grain records are the tests added after the review."""
    import shutil
    tmp = tempfile.mkdtemp(prefix="soundneg_")
    for f in os.listdir(OUT_DIR):
        os.symlink(os.path.join(OUT_DIR, f), os.path.join(tmp, f))

    def broken(name, fn):
        os.remove(os.path.join(tmp, name + ".wav"))
        x, ch, bits, sr, raw = read_wav(os.path.join(OUT_DIR, name + ".wav"))
        y = np.clip(fn(x.copy()), -1, 1)
        pcm = (np.round(y * 32767)).astype("<i2")
        with wave.open(os.path.join(tmp, name + ".wav"), "wb") as w:
            w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

    os.remove(os.path.join(tmp, "amb_traffic_rain.wav"))                                   # 1 an output missing
    broken("amb_traffic_day", lambda x: x * 2.0)                                           # 2 +6 dB: off its loudness target
    def click(x):                                                                           # 3 a step at the loop's seam
        x[len(x) // 2:] += 0.25 if x.ndim == 1 else 0.25
        return x
    broken("amb_gulls_day", click)
    os.remove(os.path.join(tmp, "step_paving_02.wav"))                                      # 4 two variants the same
    shutil.copy(os.path.join(OUT_DIR, "step_paving_01.wav"), os.path.join(tmp, "step_paving_02.wav"))
    broken("door_shop_latch_01", lambda x: x[int(0.012 * RATE) + 2000:] * 8.0)             # 5 a hard start and too loud
    broken("amb_voices_night", lambda x: x * 40.0)                                         # 6 clipped

    def repeat(x):                                                                          # 7 9 s of the loop played again 30 s later (the review's wind fault)
        x[int(40 * RATE):int(49 * RATE)] = x[int(10 * RATE):int(19 * RATE)]
        return x
    broken("amb_harbour_night", repeat)

    def tone(x):                                                                            # 8 a faint steady 1234.5 Hz whine in the right channel, 36 dB under its power
        t = np.arange(len(x)) / RATE
        x[:, 1] += np.sqrt(np.mean(x[:, 1] ** 2)) * 10 ** (-36 / 20) * np.sqrt(2) * np.sin(2 * np.pi * 1234.5 * t)
        return x
    broken("amb_traffic_night", tone)

    def cut_off(x):                                                                         # 9 a step cut off while still sounding, then faded as the cutter does
        e = rms_env(x, 5.0)
        k = int(np.argmax(e))
        end = k + int(np.argmax(e[k:] < e.max() * 10 ** (-8 / 20)))
        y = x[:end].copy()
        n = min(len(y), int(0.015 * RATE))
        y[-n:] *= np.linspace(1.0, 0.0, n)
        return y
    broken("step_paving_03", cut_off)

    def brighter(x):                                                                        # 10 the night wind made brighter than the day wind
        return x + 10.0 * np.gradient(x, axis=0)
    broken("amb_wind_night", brighter)
    voices, _, _, _, _ = read_wav(os.path.join(OUT_DIR, "amb_voices_day.wav"))
    broken("amb_radio_day", lambda x: voices.copy())                                       # 11 a radio that is only voices (same loudness class, no gaps, no midrange)
    env = dict(os.environ, SOUND_OUT=tmp)
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--out", "negative"], capture_output=True, text=True, env=env)
    out = r.stdout
    expect = [("an output missing", "MISSING amb_traffic_rain.wav"), ("loop off its target", "FAIL case 4: amb_traffic_day.wav"),
              ("a step across the loop's seam", "FAIL case 6: amb_gulls_day.wav"), ("two identical footsteps", "FAIL case 9: step_paving_*"),
              ("a click at a one-shot's start", "FAIL case 8: door_shop_latch_01.wav"), ("clipping", "FAIL case 5: amb_voices_night.wav"),
              ("a repeat put into a loop", "FAIL case 22: amb_harbour_night.wav"), ("a steady tone put in", "FAIL case 23: amb_traffic_night.wav"),
              ("a footstep cut off while sounding", "FAIL case 24: step_paving_03.wav"), ("a night wind brighter than the day's", "FAIL case 11: -: night wind is darker"),
              ("a radio that is only voices", "FAIL case 25: amb_radio_day.wav")]
    caught = 0
    for what, needle in expect:
        ok = needle in out
        caught += ok
        print("%-40s %s" % (what, "caught" if ok else "NOT CAUGHT (%s)" % needle))
    # the grain record is read from manifest.json, so its two tests are shown on records made up here
    T = json.loads(open(os.path.join(HERE, "BRIEF.md"), encoding="utf8").read().split("```targets-json")[1].split("```")[0])
    run_plan = {"plan": {"src": [0, 0, 0], "start_ms": [1000, 1110, 5000], "len_ms": [120, 120, 120], "pos_ms": [0, 60, 40000]}}   # grain 2 takes up where grain 1 stops
    reuse_plan = {"plan": {"src": [0, 0], "start_ms": [2000, 2050], "len_ms": [120, 120], "pos_ms": [0, 5000]}}                     # the same place again 5 s later
    _, run, _ = grain_runs(run_plan, 75000)
    _, _, reuse = grain_runs(reuse_plan, 75000)
    for what, ok in (("a grain that continues another (a run of %d ms)" % run, run > T["grain_ms_max"]),
                     ("a moment of a recording back after %.0f s" % reuse, reuse < min(T["grain_reuse_min_s"].values()))):
        expect.append((what, ""))
        caught += ok
        print("%-40s %s" % (what, "caught" if ok else "NOT CAUGHT"))
    print("negative controls: %d of %d caught" % (caught, len(expect)))
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    neg = os.path.join(HERE, "checks", "check_negative.json")
    if os.path.exists(neg):
        os.remove(neg)
    return 0 if caught == len(expect) else 1


if __name__ == "__main__":
    if "--negative-controls" in sys.argv:
        sys.exit(negative_controls())
    sys.exit(main())
