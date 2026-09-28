#!/usr/bin/env python3
"""The thinking sounds, tidied: tails trimmed and faded, and none with a hole in its hiss.

    python tools/voice-live/tidy_acks.py FILE_OR_DIR ...     # tidies in place, prints what it did
    python tools/voice-live/tidy_acks.py --check FILE_OR_DIR  # only reports
    python tools/voice-live/tidy_acks.py --selftest

WHY, 28 September. The game plays one of these the moment the player asks
someone something (ue-probe CrimeProbe.cpp AckStart; content/voice/acks).
The blind reviewer failed two of Sheila's: her voice carries a faint hiss,
and in one the hiss dropped to digital silence for 0.19 s mid-sound; both
ended on 0.3 s of hiss cut off without a fade. Each file here is cut 0.1 s
after its last sound 15 dB over its own hiss, and faded in over 10 ms and out
over 40 ms. A run of near silence (under -80 dB) longer than 50 ms inside the
sound is a hole: reported, never patched (the file is made again instead).
"""
import glob
import os
import sys

TAIL_S, FADE_IN_S, FADE_OUT_S, HOLE_S, OVER_FLOOR_DB, SILENT_DB = 0.1, 0.01, 0.04, 0.05, 15.0, -80.0


def frames_db(a, sr):
    """Each 10 ms frame's loudness (RMS, dB of full scale)."""
    import numpy as np
    frame = max(1, int(sr * 0.01))
    return frame, [20 * np.log10(float(np.sqrt(np.mean(a[i:i + frame] ** 2))) + 1e-12) for i in range(0, len(a), frame)]


def tidy(a, sr):
    # SPEECH IS WHAT STANDS OUT OF THE FILE'S OWN HISS (the reviewer's recheck:
    # a cutoff 40 dB under the loudest sample left Sheila's hiss, which is
    # louder than that, as "sound"): the floor is the quietest tenth of the
    # frames, and speech is 15 dB over it.
    import numpy as np
    frame, db = frames_db(a, sr)
    floor = float(np.percentile(db, 10))
    loud = [k * frame for k, d in enumerate(db) if d > floor + OVER_FLOOR_DB]
    end = min(len(a), (loud[-1] + frame if loud else len(a)) + int(sr * TAIL_S))
    out = a[:end].astype("float32").copy()
    n_in, n_out = int(sr * FADE_IN_S), int(sr * FADE_OUT_S)
    if len(out) > n_in + n_out:
        out[:n_in] *= np.linspace(0.0, 1.0, n_in, dtype="float32")
        out[-n_out:] *= np.linspace(1.0, 0.0, n_out, dtype="float32")
    return out


def holes(a, sr):
    """Runs of near silence (under SILENT_DB, not only exact zeros) longer than HOLE_S, as (start s, length s),
    inside the sound (not at its ends)."""
    quiet = 10 ** (SILENT_DB / 20.0)
    out, run, start = [], 0, 0
    for i, x in enumerate(a):
        if abs(x) < quiet:
            if run == 0:
                start = i
            run += 1
        else:
            if run > sr * HOLE_S and start > 0:
                out.append((round(start / sr, 2), round(run / sr, 2)))
            run = 0
    return out


def files(args):
    out = []
    for p in args:
        out += sorted(glob.glob(os.path.join(p, "**", "*.wav"), recursive=True)) if os.path.isdir(p) else [p]
    return out


def main(args):
    import soundfile as sf
    check = "--check" in args
    bad = 0
    for f in files([a for a in args if a != "--check"]):
        a, sr = sf.read(f, dtype="float32")
        a = a if a.ndim == 1 else a.mean(axis=1)
        h = holes(a, sr)
        bad += bool(h)
        if check or h:
            print("%s %.2f s%s" % (f, len(a) / sr, "  HOLES %s" % h if h else ""))
            continue
        t = tidy(a, sr)
        sf.write(f, t, sr, subtype="PCM_16")
        print("%s %.2f -> %.2f s" % (f, len(a) / sr, len(t) / sr))
    return 1 if bad else 0


def selftest():
    import numpy as np
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("tidy_acks selftest FAIL " + name)
    sr = 1000
    a = np.concatenate([np.full(300, 0.5, "float32"), np.full(500, 0.001, "float32")])
    t = tidy(a, sr)
    check("the tail is cut to a tenth of a second after the sound", abs(len(t) - 400) <= 10)
    check("the end is faded to nothing", abs(t[-1]) < 1e-6 and abs(t[0]) < 1e-6)
    h = np.concatenate([np.full(100, 0.2, "float32"), np.zeros(80, "float32"), np.full(100, 0.2, "float32")])
    check("a hole in the sound is found", holes(h, sr) == [(0.1, 0.08)])
    check("zeros at the start are not a hole", holes(np.concatenate([np.zeros(80, "float32"), h[:100]]), sr) == [])
    rng = np.random.default_rng(1)
    hiss = lambda n: (rng.standard_normal(n) * 0.005).astype("float32")
    t2 = tidy(np.concatenate([np.full(300, 0.5, "float32") + hiss(300), hiss(600)]), sr)
    check("a hiss louder than 40 dB under the peak is still cut as tail", abs(len(t2) - 400) <= 20)
    near = np.concatenate([np.full(100, 0.2, "float32"), np.full(80, 1e-6, "float32"), np.full(100, 0.2, "float32")])
    check("a hole of the faintest noise is found", holes(near, sr) == [(0.1, 0.08)])
    print("tidy_acks selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
