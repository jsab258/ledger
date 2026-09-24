"""From the fetched recordings, two files per speaker, at 24 kHz mono:
  own_<speaker>.wav  their own recording of the one sentence every VCTK speaker
                     reads ("Ask her to bring these things with her from the
                     store."), so the page compares like with like;
  ref_<speaker>.wav  about ten seconds of their speech, silences trimmed, for
                     the voice engine to clone from. The four current voices
                     use their cast clips instead, as the game does.

    python prepare.py VOICEDIR"""
import json, pathlib, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
V = pathlib.Path(sys.argv[1]); src = V / "vctk"
idx = json.loads((src / "index.json").read_text(encoding="utf-8"))

def load24(path):
    a, sr = sf.read(path)
    if a.ndim > 1:
        a = a.mean(axis=1)
    if sr != 24000:
        g = np.gcd(sr, 24000)
        a = resample_poly(a, 24000 // g, sr // g)
    return a

def trim(a, thr=0.02, pad=2400):
    loud = np.where(np.abs(a) > thr * max(1e-9, np.abs(a).max()))[0]
    return a[max(0, loud[0] - pad): loud[-1] + pad] if len(loud) else a

for s, rows in idx.items():
    seen, uniq = set(), []
    for r in rows:
        if r["text_id"] not in seen:
            seen.add(r["text_id"]); uniq.append(r)
    own = next((r for r in uniq if r["text_id"] == "002"), uniq[0])
    sf.write(V / ("own_%s.wav" % s), trim(load24(src / own["file"])), 24000)
    parts, total = [], 0.0
    for r in uniq:
        if r["text_id"] in ("001", "002"):
            continue
        a = trim(load24(src / r["file"]))
        parts += [a, np.zeros(4800)]
        total += len(a) / 24000
        if total >= 10.0:
            break
    ref = np.concatenate(parts)[: 12 * 24000]
    sf.write(V / ("ref_%s.wav" % s), ref, 24000)
    print(s, "own %.1fs" % (len(trim(load24(src / own["file"]))) / 24000), "ref %.1fs" % (len(ref) / 24000))
