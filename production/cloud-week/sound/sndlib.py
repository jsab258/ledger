#!/usr/bin/env python3
"""Shared helpers for the Quay Street sound build (unit 10, cloud week 42).

numpy and scipy for the signal work; ffmpeg only to decode the sources and to
encode previews. Loudness is ITU-R BS.1770-4 (K-weighting, 400 ms blocks with
75 percent overlap, absolute gate -70 LUFS, relative gate -10 LU) and true peak
is the maximum of a 4x oversampled signal. check_sound.py measures the loops a
second time with ffmpeg's own ebur128 filter, so a fault in this module cannot
pass its own check.
"""
import json
import os
import subprocess
import wave

import numpy as np
from scipy import signal

RATE = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES_DIR = os.environ.get("SOUND_SOURCES", "/home/user/ledger-scratch/sound-sources")
OUT_DIR = os.environ.get("SOUND_OUT", "/home/user/ledger-scratch/sound-out")

# BS.1770-4 K-weighting at 48 kHz: stage 1 (head-related shelf), stage 2 (RLB high-pass).
_K1 = ([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585])
_K2 = ([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621])


def decode(path, channels=None, start=None, dur=None):
    """Decode any file ffmpeg reads to float32 at 48 kHz. Returns (n,) for mono, (n, 2) for stereo.
    channels=1 mixes down; channels=None keeps the source's layout (more than two is mixed to stereo)."""
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=channels",
                            "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    src_ch = int(probe.stdout.strip().strip(",").split(",")[0])
    ch = channels or min(src_ch, 2)
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", "%.6f" % start]
    cmd += ["-i", path]
    if dur is not None:
        cmd += ["-t", "%.6f" % dur]
    cmd += ["-ac", str(ch), "-ar", str(RATE), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return a.reshape(-1, ch) if ch > 1 else a


def to_mono(x):
    return x.mean(axis=1) if x.ndim > 1 else x


def seg(x, a, b):
    """Seconds a to b of x."""
    return x[int(round(a * RATE)):int(round(b * RATE))]


def kweight(x):
    y = signal.lfilter(*_K1, x, axis=0)
    return signal.lfilter(*_K2, y, axis=0)


def _block_loudness(x, win, hop):
    k = kweight(x)
    k = k[:, None] if k.ndim == 1 else k
    p = k * k
    c = np.concatenate([np.zeros((1, p.shape[1])), np.cumsum(p, axis=0)])
    n = (len(p) - win) // hop + 1
    if n < 1:
        return np.array([])
    idx = np.arange(n) * hop
    ms = (c[idx + win] - c[idx]) / win
    return -0.691 + 10 * np.log10(ms.sum(axis=1) + 1e-20)


def integrated_lufs(x):
    """BS.1770-4 gated integrated loudness (400 ms blocks, 75 percent overlap)."""
    win, hop = int(0.4 * RATE), int(0.1 * RATE)
    if len(x) < win:
        x = np.concatenate([x, np.zeros((win - len(x),) + x.shape[1:])])
    l = _block_loudness(x, win, hop)
    l = l[l > -70.0]
    if len(l) == 0:
        return -70.0
    mean_all = 10 * np.log10(np.mean(10 ** (l / 10)))
    l = l[l > mean_all - 10.0]
    return float(10 * np.log10(np.mean(10 ** (l / 10))) if len(l) else -70.0)


def momentary_max(x):
    """Highest 400 ms momentary loudness (LUFS-M); a clip shorter than 400 ms is padded with silence."""
    win, hop = int(0.4 * RATE), int(0.01 * RATE)
    if len(x) < win:
        x = np.concatenate([x, np.zeros((win - len(x),) + x.shape[1:])])
    l = _block_loudness(x, win, hop)
    return float(l.max())


def true_peak_db(x):
    y = signal.resample_poly(x, 4, 1, axis=0)
    return float(20 * np.log10(np.abs(y).max() + 1e-12))


def sample_peak_db(x):
    return float(20 * np.log10(np.abs(x).max() + 1e-12))


def rms_db(x):
    return float(10 * np.log10(np.mean(np.square(x)) + 1e-20))


def sos_filter(x, kind, freq, order=4):
    """Zero-phase Butterworth: kind is 'lp', 'hp' or 'bp' (freq a pair for bp)."""
    btype = {"lp": "lowpass", "hp": "highpass", "bp": "bandpass", "bs": "bandstop"}[kind]
    sos = signal.butter(order, freq, btype=btype, fs=RATE, output="sos")
    return signal.sosfiltfilt(sos, x, axis=0)


def peaking(x, f0, q, gain_db):
    """RBJ peaking EQ."""
    a = 10 ** (gain_db / 40)
    w = 2 * np.pi * f0 / RATE
    al = np.sin(w) / (2 * q)
    b = [1 + al * a, -2 * np.cos(w), 1 - al * a]
    aa = [1 + al / a, -2 * np.cos(w), 1 - al / a]
    return signal.lfilter(np.array(b) / aa[0], np.array(aa) / aa[0], x, axis=0)


def fade(x, n_in=0, n_out=0):
    x = x.copy()
    if n_in:
        r = np.linspace(0, 1, n_in)
        x[:n_in] *= r if x.ndim == 1 else r[:, None]
    if n_out:
        r = np.linspace(1, 0, n_out)
        x[-n_out:] *= r if x.ndim == 1 else r[:, None]
    return x


def make_loop(x, length_s, xfade_s):
    """A seamless loop of length_s taken from the start of x (which must hold length_s + xfade_s).
    The tail beyond the loop's end is mixed into its head with an equal-power crossfade, so the sample
    after the last is exactly the one that followed it in the source: no jump, no level step."""
    n, xf = int(round(length_s * RATE)), int(round(xfade_s * RATE))
    if len(x) < n + xf:
        raise ValueError("source too short for loop: have %.1f s, need %.1f s" % (len(x) / RATE, (n + xf) / RATE))
    body = x[:n].copy()
    tail = x[n:n + xf]
    t = np.linspace(0, np.pi / 2, xf)
    fi, fo = np.sin(t), np.cos(t)
    if x.ndim > 1:
        fi, fo = fi[:, None], fo[:, None]
    body[:xf] = body[:xf] * fi + tail * fo
    return body


def spliced(parts, xfade_s=1.0):
    """Join excerpts end to end with equal-power crossfades (used to lengthen a short source)."""
    xf = int(xfade_s * RATE)
    out = parts[0].copy()
    t = np.linspace(0, np.pi / 2, xf)
    fi, fo = np.sin(t), np.cos(t)
    for p in parts[1:]:
        if out.ndim > 1:
            a, b = fi[:, None], fo[:, None]
        else:
            a, b = fi, fo
        mid = out[-xf:] * b + p[:xf] * a
        out = np.concatenate([out[:-xf], mid, p[xf:]])
    return out


def gain_to_target(x, target_lufs, tol=0.005):
    """Gain in dB that brings the integrated loudness to target. Gated loudness is not exactly proportional to gain
    (the -70 LUFS absolute gate does not move with it), so the gain is refined until it lands within tol LU."""
    g = target_lufs - integrated_lufs(x)
    for _ in range(12):
        err = target_lufs - integrated_lufs(x * 10 ** (g / 20))
        if abs(err) <= tol:
            break
        g += err
    return g


def write_wav16(path, x, dither=True, seed=1):
    """48 kHz 16-bit PCM WAV. Rounds with TPDF dither (seeded, so a rebuild is bit-identical)."""
    x = np.asarray(x)
    if dither:
        rng = np.random.default_rng(seed)
        d = (rng.random(x.shape) - rng.random(x.shape)) / 32768.0
        x = x + d
    pcm = np.clip(np.round(x * 32767.0), -32768, 32767).astype("<i2")
    ch = 1 if pcm.ndim == 1 else pcm.shape[1]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())


def read_wav16(path):
    with wave.open(path, "rb") as w:
        ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    a = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    return (a.reshape(-1, ch) if ch > 1 else a), sr, sw * 8


def load_targets():
    """The numbers in BRIEF.md's targets-json block: the one home of every target and tolerance."""
    with open(os.path.join(HERE, "BRIEF.md"), encoding="utf8") as f:
        text = f.read()
    a = text.index("```targets-json") + len("```targets-json")
    return json.loads(text[a:text.index("```", a)])


def load_json(name):
    with open(os.path.join(HERE, name), encoding="utf8") as f:
        return json.load(f)


def save_json(name, obj):
    with open(os.path.join(HERE, name), "w", encoding="utf8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")
