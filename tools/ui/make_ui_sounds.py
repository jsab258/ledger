"""The interface's four sounds, made here (production/design/ui/STYLE-GUIDE.md, Sound).

    python tools/ui/make_ui_sounds.py              # writes production/audio/ui/*.wav
    python tools/ui/make_ui_sounds.py --selftest

WHY, 1 October (the interface as drawn): the guide asks for four sounds,
"short, quiet and switchable off, all recorded or made by us": a soft paper
rustle when a menu opens, a pencil tick when a choice is taken, the distant
run of a press under the loading page, and a soft key sound as he types, the
first thing to go if it tires. Nothing is recorded or downloaded: each is
synthesised from noise and decaying tones, shaped by what the real thing
does (paper: many tiny crackles in the 1.5 to 7 kHz band over a soft swish;
a pencil: a short bright transient and a graphite scratch; a rotary press
heard through a wall: a low rumble with a thump and a clack each turn, its
top cut away and a short room tail; a key: a small plastic click with a
low thock). Seeded, so the same files come out each run. Out: 44.1 kHz mono
16-bit WAV, quiet by design (peaks well under full scale), read by the game
(LedgerPaper.cpp, UiSound) and staged with its data.
"""
import os
import sys
import wave

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "production", "audio", "ui")
SR = 44100
#: name -> the loudest peak it may have, in dB below full scale
PEAK_DB = {"rustle": -14.0, "tick": -16.0, "press": -20.0, "key1": -20.0, "key2": -20.0, "key3": -20.0}


def band(x, lo, hi):
    """Band-pass by FFT (circular, so a loop stays seamless)."""
    f = np.fft.rfftfreq(len(x), 1.0 / SR)
    X = np.fft.rfft(x)
    X[(f < lo) | (f > hi)] = 0.0
    return np.fft.irfft(X, len(x))


def env_exp(n, tau_s):
    t = np.arange(n) / SR
    return np.exp(-t / tau_s)


def at_peak(x, db):
    p = np.max(np.abs(x))
    return x if p == 0 else x * (10 ** (db / 20.0) / p)


def fade(x, ms_in, ms_out):
    a, b = int(SR * ms_in / 1000.0), int(SR * ms_out / 1000.0)
    x = x.copy()
    if a:
        x[:a] *= np.linspace(0.0, 1.0, a)
    if b:
        x[-b:] *= np.linspace(1.0, 0.0, b)
    return x


def rustle(rng):
    n = int(0.45 * SR)
    out = np.zeros(n)
    # the swish: soft mid noise under a smooth swell
    swell = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    out += band(rng.standard_normal(n), 300, 1500) * swell * 0.25
    # the crackles: tiny bright bursts, densest in the middle
    for _ in range(46):
        c = int(rng.beta(2.2, 2.2) * (n - 800))
        L = int(rng.uniform(0.003, 0.015) * SR)
        g = band(rng.standard_normal(L), 1500, 7000) * env_exp(L, rng.uniform(0.001, 0.004))
        out[c:c + L] += g * rng.uniform(0.3, 1.0) * swell[c]
    return fade(out, 6, 60)


def tick(rng):
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    click = band(rng.standard_normal(n), 2000, 6000) * env_exp(n, 0.0007)
    scratch = band(rng.standard_normal(n), 3000, 9000) * env_exp(n, 0.008) * 0.18
    knock = np.sin(2 * np.pi * 900 * t) * env_exp(n, 0.006) * 0.25
    return fade(click + scratch + knock, 0, 15)


def press(rng):
    # eight turns of a rotary press, 0.6 s each, made circularly so the loop has no seam
    turn = 0.6
    n = int(8 * turn * SR)
    out = band(rng.standard_normal(n), 30, 200) * 0.35          # the rumble of the machine room
    for k in range(8):
        jitter = rng.uniform(-0.012, 0.012)
        a = int((k * turn + jitter) * SR)
        L = int(0.12 * SR)
        tt = np.arange(L) / SR
        thump = np.sin(2 * np.pi * rng.uniform(62, 74) * tt) * env_exp(L, 0.03)
        idx = (a + np.arange(L)) % n
        out[idx] += thump * rng.uniform(0.8, 1.0)
        b = int((k * turn + turn * 0.48 + rng.uniform(-0.01, 0.01)) * SR)
        Lc = int(0.04 * SR)
        clack = band(rng.standard_normal(Lc), 800, 2500) * env_exp(Lc, 0.006)
        idx = (b + np.arange(Lc)) % n
        out[idx] += clack * rng.uniform(0.4, 0.6)
    # heard through a wall: the top cut away, a short room tail (circular)
    out = band(out, 25, 2000)
    tail_n = int(0.3 * SR)
    ir = np.zeros(n)
    ir[0] = 1.0
    ir[1:tail_n] = rng.standard_normal(tail_n - 1) * env_exp(tail_n - 1, 0.08) * 0.05
    out = np.fft.irfft(np.fft.rfft(out) * np.fft.rfft(ir), n)
    return out


def key(rng, pitch):
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    click = band(rng.standard_normal(n), 1000, 4000) * env_exp(n, 0.0006)
    body = np.sin(2 * np.pi * pitch * t) * env_exp(n, 0.004) * 0.3
    thock = np.sin(2 * np.pi * 300 * t) * env_exp(n, 0.008) * 0.35
    return fade(click + body + thock, 0, 10)


def make():
    rng = np.random.default_rng(19901001)
    sounds = {"rustle": rustle(rng), "tick": tick(rng), "press": press(rng),
              "key1": key(rng, 1800), "key2": key(rng, 2100), "key3": key(rng, 2400)}
    os.makedirs(OUT, exist_ok=True)
    for name, x in sounds.items():
        x = at_peak(x, PEAK_DB[name])
        pcm = np.clip(np.round(x * 32767), -32768, 32767).astype("<i2")
        with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
        print("%s.wav: %.2f s, peak %.1f dBFS" % (name, len(pcm) / SR, PEAK_DB[name]))


def read(name):
    with wave.open(os.path.join(OUT, name + ".wav"), "rb") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float) / 32768.0, w.getframerate(), w.getnchannels()


def selftest():
    ok = bad = 0

    def check(what, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_ui_sounds selftest FAIL " + what)
    have = [n for n in PEAK_DB if os.path.isfile(os.path.join(OUT, n + ".wav"))]
    check("the six files are made (or none yet)", len(have) in (0, len(PEAK_DB)))
    for n in have:
        x, sr, ch = read(n)
        check(n + " is 44.1 kHz mono", sr == SR and ch == 1)
        peak = 20 * np.log10(max(np.max(np.abs(x)), 1e-9))
        check(n + " is quiet: its peak at or under its limit", peak <= PEAK_DB[n] + 0.2)
        check(n + " is short, the press a loop of a few seconds", (len(x) / sr) <= (6.0 if n == "press" else 0.5))
    if "press" in have:
        x, _, _ = read("press")
        check("the press loops with no seam (its last and first samples close)", abs(x[-1] - x[0]) < 0.01)
    if "rustle" in have:
        x, _, _ = read("rustle")
        spec = np.abs(np.fft.rfft(x))
        f = np.fft.rfftfreq(len(x), 1.0 / SR)
        check("the rustle is mostly above 1 kHz, as paper is", spec[f > 1000].sum() > spec[f <= 1000].sum())
    print("make_ui_sounds selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    make()
