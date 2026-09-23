"""The street's distant-traffic bed, made from noise: production/assets/sounds/traffic-distant.wav.

    python tools/props/make_street_ambience.py            # writes the wav
    python tools/props/make_street_ambience.py --check    # the committed wav is what this makes

WHY IT EXISTS, 23 September. Jafar's presentable checklist: "sound is
positional" - and the street made no sound at all. A far-off road is a low,
steady rumble with slow swells as something heavier passes; that is brown noise
(random steps, so the energy sits low), softened further, with a slow swell
laid on it. No recording, no sample library, nothing fetched: the seed makes
the same file every time, so the file is ours and can be checked.

SEAMLESS: the last second is crossfaded into the first, so Unreal's loop has
no click. Mono, since the engine places it; 32 kHz, 16-bit.
"""
import os
import sys
import wave

import numpy as np

RATE = 32000
SECONDS = 24.0
FADE_S = 1.0
SEED = 23092026
OUT_REL = "production/assets/sounds/traffic-distant.wav"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def make():
    rng = np.random.default_rng(SEED)
    n = int(RATE * (SECONDS + FADE_S))
    brown = np.cumsum(rng.standard_normal(n))
    # A LEAKY walk, so it does not wander off: the drift is taken out over
    # about a fifth of a second.
    k = int(RATE * 0.2)
    kernel = np.ones(k) / k
    drift = np.convolve(brown, kernel, mode="same")
    x = brown - drift
    # SOFTER STILL: a short moving average takes off the hiss.
    s = int(RATE / 600)
    x = np.convolve(x, np.ones(s) / s, mode="same")
    # SLOW SWELLS, a vehicle passing every few seconds, never silent.
    t = np.arange(n) / RATE
    swell = 0.65 + 0.2 * np.sin(2 * np.pi * t / 7.3) + 0.15 * np.sin(2 * np.pi * t / 3.1 + 1.0)
    x = x * swell
    # SEAMLESS: the tail crossfades into the head.
    f = int(RATE * FADE_S)
    body = x[: n - f].copy()
    ramp = np.linspace(0.0, 1.0, f)
    body[:f] = body[:f] * ramp + x[n - f:] * (1.0 - ramp)
    body = body / np.max(np.abs(body)) * 0.5
    return (body * 32767).astype("<i2")


def write(path, pcm):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())


def main():
    path = os.path.join(repo_root(), OUT_REL)
    pcm = make()
    if "--check" in sys.argv:
        with wave.open(path, "rb") as w:
            same = w.readframes(w.getnframes()) == pcm.tobytes()
        print("make_street_ambience check: %s" % ("same" if same else "DIFFERS"))
        return 0 if same else 1
    write(path, pcm)
    print("make_street_ambience: wrote %s (%.1f s, %d Hz mono)" % (OUT_REL, len(pcm) / RATE, RATE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
