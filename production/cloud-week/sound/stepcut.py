#!/usr/bin/env python3
"""Footfall cutting, adapted from tools/ue/make_steps.py (30 September 2026; that file is not edited).

Same method, numpy only: take the rumble off, find each footfall's onset, cut it so its loudest hit lands
12 ms in, end it where it has fallen 35 dB, keep it only if it died away, is 80 to 250 ms long and passes
the tests below. What differs from make_steps.py, and why:
  - the length cap, the centroid range and the transient count are parameters, because Tom's steps were
    cut from trainers on slabs and the other surfaces (setts, wet, wood) ring longer and sit lower;
  - steps are scored for how much they differ from each other, so a set of variants is not eight copies
    of the same step;
  - nothing is written here: make_sound.py levels and writes.
"""
import numpy as np

from sndlib import RATE


def highpass(m, cut):
    X = np.fft.rfft(m)
    f = np.fft.rfftfreq(len(m), 1.0 / RATE)
    X *= np.clip((f - (cut - 20.0)) / 20.0, 0.0, 1.0)
    return np.fft.irfft(X, len(m))


def envelope(m, ms):
    n = max(1, int(RATE * ms / 1000.0))
    return np.sqrt(np.convolve(m * m, np.ones(n) / n, "same"))


def transients(step):
    e = envelope(step, 2.0)
    thr = 0.3 * e.max()
    peaks = []
    for i in range(1, len(e) - 1):
        if e[i] >= thr and e[i] >= e[i - 1] and e[i] > e[i + 1]:
            if not peaks or i - peaks[-1] > int(0.015 * RATE):
                peaks.append(i)
    return peaks


def centroid(s):
    X = np.abs(np.fft.rfft(s * np.hanning(len(s)))) ** 2
    f = np.fft.rfftfreq(len(s), 1.0 / RATE)
    return float((X * f).sum() / X.sum())


def footfall_first(s):
    return int(0.005 * RATE) <= int(np.argmax(envelope(s, 2.0))) <= int(0.02 * RATE)


def cut(m, max_ms=250.0, thr_scale=0.08, min_gap=0.2, min_transients=2, centroid_range=(500.0, 1600.0),
        min_ms=80.0, died_db=-20.0, ring_db=-35.0, min_snr_db=12.0):
    """Every footfall in m that passes the tests: a list of (start_sample, samples).

    Outdoor takes carry a noise floor, so "has died away" and "where it ends" are judged against the larger of
    the original's thresholds (20 dB and 35 dB below the step's loudest hit) and a level 2.5 times the take's own
    noise floor (the 20th percentile of its 5 ms envelope); a step must also stand min_snr_db above that floor.
    On a clean take the floor is below both thresholds and this is make_steps.py's test exactly."""
    e = envelope(m, 2.0)
    floor = float(np.percentile(envelope(m, 5.0), 20))
    thr = np.percentile(e, 99.5) * thr_scale
    onsets, last = [], -RATE
    for i in range(1, len(e)):
        if e[i] > thr and e[i - 1] <= thr and i - last > int(min_gap * RATE):
            onsets.append(i)
            last = i
    steps = []
    for k, on in enumerate(onsets):
        a = max(0, on - int(0.005 * RATE))
        b = min(len(m), on + int(max_ms / 1000.0 * RATE))
        if k + 1 < len(onsets):
            b = min(b, onsets[k + 1] - int(0.01 * RATE))
        s = m[a:b].copy()
        if len(s) < int(0.05 * RATE):
            continue
        hit = int(np.argmax(envelope(s, 2.0)))
        a2 = max(0, a + hit - int(0.012 * RATE))
        s = m[a2:min(len(m), a2 + int(max_ms / 1000.0 * RATE))].copy()
        if k + 1 < len(onsets):
            s = s[:max(0, onsets[k + 1] - int(0.01 * RATE) - a2)]
        if len(s) < int(0.05 * RATE):
            continue
        se = envelope(s, 5.0)
        if 20.0 * np.log10(se.max() / (floor + 1e-12)) < min_snr_db:
            continue
        quiet = np.where(se > max(se.max() * 10 ** (ring_db / 20.0), 2.5 * floor))[0]
        end = min(len(s), quiet[-1] + int(0.01 * RATE)) if len(quiet) else len(s)
        if end < int(0.05 * RATE):
            continue
        if se[max(0, end - int(0.02 * RATE)):end].max() > max(se.max() * 10 ** (died_db / 20.0), 3.0 * floor):
            continue
        s = s[:end]
        n = min(len(s), int(0.015 * RATE))
        s[-n:] *= np.linspace(1.0, 0.0, n)
        s[:int(0.002 * RATE)] *= np.linspace(0.0, 1.0, int(0.002 * RATE))
        ms = 1000.0 * len(s) / RATE
        if (min_ms <= ms <= max_ms + 5 and len(transients(s)) >= min_transients and footfall_first(s)
                and centroid_range[0] <= centroid(s) <= centroid_range[1]):
            steps.append((a2, s))
    return steps


def band_signature(s):
    """Log energy in 12 bands, 100 Hz to 8 kHz: the shape used to tell steps apart."""
    X = np.abs(np.fft.rfft(s * np.hanning(len(s)), n=4096)) ** 2
    f = np.fft.rfftfreq(4096, 1.0 / RATE)
    edges = np.geomspace(100.0, 8000.0, 13)
    sig = np.array([10 * np.log10(X[(f >= edges[i]) & (f < edges[i + 1])].sum() + 1e-12) for i in range(12)])
    return sig - sig.mean()


def pick_distinct(steps, n, loud):
    """n steps spread through the take and as different from each other as the take allows:
    greedy farthest-point choice on band signature plus length, starting from the step nearest the median loudness."""
    if len(steps) <= n:
        return list(range(len(steps)))
    sigs = np.array([np.append(band_signature(s), 0.02 * len(s) / RATE * 1000) for _, s in steps])
    first = int(np.argmin(np.abs(loud - np.median(loud))))
    chosen = [first]
    while len(chosen) < n:
        d = np.min(np.linalg.norm(sigs[:, None, :] - sigs[chosen][None, :, :], axis=2), axis=1)
        # keep steps from the same moment of the take apart too (neighbouring steps are near-identical)
        for c in chosen:
            d[abs(np.array([a for a, _ in steps]) - steps[c][0]) < int(0.8 * RATE)] *= 0.3
        d[chosen] = -1
        chosen.append(int(np.argmax(d)))
    return sorted(chosen, key=lambda i: steps[i][0])


def max_xcorr(a, b):
    """Highest normalised cross-correlation of two steps over every lag (1.0 is the same step, 0 unrelated)."""
    n = len(a) + len(b)
    nf = 1 << (n - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(a, nf) * np.conj(np.fft.rfft(b, nf)), nf)
    return float(np.abs(c).max() / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))
