#!/usr/bin/env python3
"""Tom's footsteps, cut from two CC0 recordings of real trainers.

    python tools/ue/make_steps.py              # writes production/assets/steps/
    python tools/ue/make_steps.py --selftest   # checks what is there without writing

WHY, 30 September. Two CC0 packs failed independent review as the player's
footsteps: Kenney's concrete steps were a single dull 250 Hz knock, and
Fantozzi's "stone" steps turned out to be foley (cork pressed into salt), a
crunch of grit. The research (production/research/footsteps/
NOTE-2026-09-30.md) found recordings of the real thing, both CC0 and both
fetched without signing in:

- WALK: sturmankin, "paving_11a_sneakers_walk" (Freesound 273077, uploaded
  1 May 2015, "Creative Commons 0"): trainers on three real paving slabs.
  Its public high-quality preview (48 kHz mono); the lossless original needs
  a Freesound login, which is Jafar's to use or not.
- RUN: Joseph Sardin, BigSoundBank s0514 "Footsteps, Shoe on Concrete"
  (its page, read 30 September 2026: "CC0 (public domain)"): a man running in trainers
  on concrete outdoors, lossless.

Both are continuous takes, so each footfall is cut out: the rumble below the
cut-off taken off (a basement's for the walk, wind for the run), from 5 ms
before its onset to where it has fallen 35 dB (at most 250 ms walking, 200
running), a 15 ms fade; kept only if it lasts 80 to 250 ms and has both a
heel and a toe, has died away by its end, and sits between 500 and 1600 Hz
(a hard smooth surface, not a hiss or a thud); each cut so its loudest hit
lands 12 ms in, so evenly timed steps sound even; eight of each taken from across the take, nearest the
median loudness, and levelled (the run 3 dB above the walk). 48 kHz,
16-bit, mono. The sources are kept in F:/LedgerTools/steps-sources.
"""
import glob
import os
import sys

import numpy as np
import soundfile as sf

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "production", "assets", "steps")
SOURCES = "F:/LedgerTools/steps-sources"
TAKES = {
    "walk": {"file": "273077_paving_11a_sneakers_walk-hq.mp3", "highpass": 60.0, "max_ms": 250.0, "level": -35.0},
    "run": {"file": "0514.flac", "highpass": 100.0, "max_ms": 200.0, "level": -32.0},
}
KEEP = 8
RATE = 48000


def highpass(m, sr, cut):
    X = np.fft.rfft(m)
    f = np.fft.rfftfreq(len(m), 1.0 / sr)
    X *= np.clip((f - (cut - 20.0)) / 20.0, 0.0, 1.0)
    return np.fft.irfft(X, len(m))


def envelope(m, sr, ms):
    n = max(1, int(sr * ms / 1000.0))
    return np.sqrt(np.convolve(m * m, np.ones(n) / n, "same"))


def a_weighted_db(m, sr):
    X = np.fft.rfft(m, n=max(len(m), int(0.15 * sr)))
    f = np.fft.rfftfreq(max(len(m), int(0.15 * sr)), 1.0 / sr)
    f2 = f * f
    ra = (12194.0 ** 2 * f2 ** 2) / ((f2 + 20.6 ** 2) * np.sqrt((f2 + 107.7 ** 2) * (f2 + 737.9 ** 2)) * (f2 + 12194.0 ** 2) + 1e-20)
    a = np.fft.irfft(X * ra * 10 ** (2.0 / 20.0))
    return 20.0 * np.log10(np.sqrt(np.mean(a[:int(0.15 * sr)] ** 2)) + 1e-12)


def transients(step, sr):
    e = envelope(step, sr, 2.0)
    thr = 0.3 * e.max()
    peaks = []
    for i in range(1, len(e) - 1):
        if e[i] >= thr and e[i] >= e[i - 1] and e[i] > e[i + 1]:
            if not peaks or i - peaks[-1] > int(0.015 * sr):
                peaks.append(i)
    return peaks


def centroid(s, sr):
    X = np.abs(np.fft.rfft(s * np.hanning(len(s)))) ** 2
    f = np.fft.rfftfreq(len(s), 1.0 / sr)
    return float((X * f).sum() / X.sum())


def footfall_first(s, sr):
    """The loudest moment 5 to 20 ms from the cut's start: every step is cut
    so its hit lands 12 ms in, and a cut whose loudest moment came later had
    started on some other sound before the step (two of the first run's
    eight)."""
    return int(0.005 * sr) <= int(np.argmax(envelope(s, sr, 2.0))) <= int(0.02 * sr)


def cut(m, sr, max_ms):
    e = envelope(m, sr, 2.0)
    thr = np.percentile(e, 99.5) * 0.08
    onsets, last = [], -sr
    for i in range(1, len(e)):
        if e[i] > thr and e[i - 1] <= thr and i - last > int(0.2 * sr):
            onsets.append(i)
            last = i
    steps = []
    for k, on in enumerate(onsets):
        a = max(0, on - int(0.005 * sr))
        b = min(len(m), on + int(max_ms / 1000.0 * sr))
        if k + 1 < len(onsets):
            b = min(b, onsets[k + 1] - int(0.01 * sr))
        s = m[a:b].copy()
        if len(s) < int(0.05 * sr):
            continue
        # EVERY STEP'S LOUDEST HIT AT THE SAME MOMENT, 12 ms in (the reviewer,
        # 30 September: the running hits sat 10 to 50 ms into their clips, so
        # evenly timed steps landed 0.33 to 0.42 s apart, a slight stumble).
        hit = int(np.argmax(envelope(s, sr, 2.0)))
        a2 = max(0, a + hit - int(0.012 * sr))
        s = m[a2:min(len(m), a2 + int(max_ms / 1000.0 * sr))].copy()
        if k + 1 < len(onsets):
            s = s[:max(0, onsets[k + 1] - int(0.01 * sr) - a2)]
        if len(s) < int(0.05 * sr):
            continue
        se = envelope(s, sr, 5.0)
        quiet = np.where(se > se.max() * 10 ** (-35.0 / 20.0))[0]
        end = min(len(s), quiet[-1] + int(0.01 * sr)) if len(quiet) else len(s)
        # NOT CUT OFF STILL SOUNDING: a step whose last 20 ms is within 20 dB
        # of its loudest was stopped mid-sound (run-3's second hit, faded out
        # 7 dB down), so it is left out.
        if 20.0 * np.log10(se[max(0, end - int(0.02 * sr)):end].max() / se.max() + 1e-12) > -20.0:
            continue
        s = s[:end]
        n = min(len(s), int(0.015 * sr))
        s[-n:] *= np.linspace(1.0, 0.0, n)
        s[:int(0.002 * sr)] *= np.linspace(0.0, 1.0, int(0.002 * sr))
        ms = 1000.0 * len(s) / sr
        if 80.0 <= ms <= 250.0 and len(transients(s, sr)) >= 2 and footfall_first(s, sr) and 500.0 <= centroid(s, sr) <= 1600.0:
            steps.append((a, s))
    return steps


def make(write=True):
    made = {}
    for label, take in TAKES.items():
        d, sr = sf.read(os.path.join(SOURCES, take["file"]))
        m = d.mean(axis=1) if d.ndim > 1 else d
        if sr != RATE:
            raise SystemExit("make_steps: %s is %d Hz, not %d" % (take["file"], sr, RATE))
        m = highpass(m, sr, take["highpass"])
        steps = cut(m, sr, take["max_ms"])
        loud = np.array([a_weighted_db(s, sr) for _, s in steps])
        # Nearest the median loudness, then spread through the take.
        near = sorted(range(len(steps)), key=lambda i: abs(loud[i] - np.median(loud)))[:max(KEEP * 2, KEEP)]
        near = sorted(near, key=lambda i: steps[i][0])
        pick = [near[int(round(j * (len(near) - 1) / (KEEP - 1)))] for j in range(KEEP)]
        out = []
        for j, i in enumerate(pick):
            s = steps[i][1] * 10 ** ((take["level"] - loud[i]) / 20.0)
            out.append(s)
            if write:
                sf.write(os.path.join(OUT, "step-%s-%d.wav" % (label, j)), s.astype(np.float32), sr, subtype="PCM_16")
        made[label] = {"found": len(steps), "kept": len(out),
                       "ms": [round(1000.0 * len(s) / sr) for s in out],
                       "peak": round(float(max(np.abs(s).max() for s in out)), 3)}
    return made


def selftest():
    failed = 0
    have = sorted(glob.glob(os.path.join(OUT, "step-*.wav")))
    checks = [("eight walking and eight running steps", len([h for h in have if "-walk-" in h]) == KEEP and len([h for h in have if "-run-" in h]) == KEEP, str(len(have)))]
    for h in have:
        s, sr = sf.read(h)
        ms = 1000.0 * len(s) / sr
        checks.append(("%s lasts 80 to 250 ms, 48 kHz mono, never clips" % os.path.basename(h),
                       80.0 <= ms <= 250.0 and sr == RATE and s.ndim == 1 and np.abs(s).max() < 0.99, "%.0f ms %d Hz" % (ms, sr)))
        checks.append(("%s has a heel and a toe" % os.path.basename(h), len(transients(s, sr)) >= 2, ""))
        se = envelope(s, sr, 5.0)
        checks.append(("%s has died away by its end" % os.path.basename(h),
                       20.0 * np.log10(se[-int(0.02 * sr):].max() / se.max() + 1e-12) <= -20.0, ""))
        checks.append(("%s hits 5 to 20 ms in, 500 to 1600 Hz" % os.path.basename(h),
                       footfall_first(s, sr) and 500.0 <= centroid(s, sr) <= 1600.0, "%.0f Hz" % centroid(s, sr)))
    for name, ok, detail in checks:
        if not ok:
            failed += 1
            print("make_steps selftest FAIL %s: %s" % (name, detail))
    print("make_steps selftest: passed=%d/%d failed=%d" % (len(checks) - failed, len(checks), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    os.makedirs(OUT, exist_ok=True)
    print(make())
