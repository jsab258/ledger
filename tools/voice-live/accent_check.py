#!/usr/bin/env python3
"""Which accent a voice has, for the approval gate: no American voice reaches Jafar.

    python tools/voice-live/accent_check.py FILE_OR_DIR ... [--want england] [--json OUT]
    python tools/voice-live/accent_check.py --selftest

WHY, 25 September (evening): some voice samples on his approval page had
American accents. CLAUDE.md's gate now says a voice drifting American, or
away from the accent its casting sheet names, is rejected before he hears it.
This is the measuring half of that check: CommonAccent's accent classifier
(Jzuluaga/accent-id-commonaccent_ecapa, MIT; SpeechBrain, Apache-2.0),
trained on Common Voice speakers of sixteen English accents, kept on drive F
(F:/LedgerTools/accent-id/ecapa-src), never shipped.

A verdict per file:
  REJECT  American (US or Canada) is the top accent, or together over 0.30
  PASS    the wanted accent is the top one (england for the Northern
          English cast) and American is under 0.30
  REVIEW  anything else: another British Isles accent on top, or unsure
The classifier knows "england", not Yorkshire from Surrey, so a PASS means
English, not American; the sheet's region is still a thing to listen for.
Runs on the chatterbox env (C:/LedgerTools/chatterbox-nano/env-dml), which
has torch and torchaudio.
"""
import glob
import json
import os
import sys

MODEL = os.environ.get("LEDGER_ACCENT_MODEL", "F:/LedgerTools/accent-id/ecapa-src")
AMERICAN = ("us", "canada")
REJECT_AT = 0.30
SCALE = 30.0
AUDIO = (".wav", ".mp3", ".flac", ".ogg")

_clf = None


def classifier():
    global _clf
    if _clf is None:
        from speechbrain.inference.classifiers import EncoderClassifier
        from speechbrain.utils.fetching import LocalStrategy
        # The model's own settings name its Hugging Face home for the weights;
        # pointed at the copy on drive F instead, it never goes online.
        _clf = EncoderClassifier.from_hparams(source=MODEL, savedir=MODEL, run_opts={"device": "cpu"},
                                              overrides={"pretrained_path": MODEL},
                                              local_strategy=LocalStrategy.NO_LINK)
    return _clf


def load(path):
    """Mono, 16 kHz, as the classifier was trained."""
    import librosa
    import torch
    y, _ = librosa.load(path, sr=16000, mono=True)
    return torch.tensor(y).unsqueeze(0)


def scores(path):
    import torch
    c = classifier()
    out = c.classify_batch(load(path))
    # The classifier gives each accent a cosine similarity, not a probability;
    # it was trained with an additive-margin softmax at scale 30, so the same
    # scale turns them into probabilities (unscaled they all read about 0.1).
    cos = out[0][0] if out[0].dim() == 2 else out[0]
    probs = torch.softmax(cos * SCALE, dim=-1)
    labels = c.hparams.label_encoder.decode_ndim(list(range(len(probs))))
    return {str(l): float(p) for l, p in zip(labels, probs)}


def verdict(sc, want="england"):
    top = max(sc, key=sc.get)
    american = sum(sc.get(a, 0.0) for a in AMERICAN)
    if top in AMERICAN or american >= REJECT_AT:
        return "REJECT", top, american
    if top == want:
        return "PASS", top, american
    return "REVIEW", top, american


def files(args):
    out = []
    for a in args:
        a = a.strip()                      # a list read from a Windows file ends lines in a return
        if os.path.isdir(a):
            out += sorted(f for f in glob.glob(os.path.join(a, "**", "*"), recursive=True) if f.lower().endswith(AUDIO))
        elif a.lower().endswith(AUDIO):
            out.append(a)
    return out


def main(argv):
    want = "england"
    js = None
    if "--want" in argv:
        want = argv[argv.index("--want") + 1]
    if "--json" in argv:
        js = argv[argv.index("--json") + 1]
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] not in ("--want", "--json"))]
    rows = []
    for f in files(args):
        sc = scores(f)
        v, top, am = verdict(sc, want)
        second = sorted(sc, key=sc.get, reverse=True)[1]
        rows.append({"file": f.replace("\\", "/"), "verdict": v, "top": top, "p_top": round(sc[top], 3),
                     "second": second, "p_second": round(sc[second], 3), "p_american": round(am, 3)})
        print("%-6s %-10s %.2f  american %.2f  %s" % (v, top, sc[top], am, f.replace("\\", "/")), flush=True)
    if js:
        with open(js, "w", encoding="utf-8") as fh:
            json.dump({"model": "Jzuluaga/accent-id-commonaccent_ecapa", "want": want, "reject_at": REJECT_AT, "files": rows}, fh, indent=1)
    return rows


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("accent_check selftest FAIL " + name)
    check("an American top is rejected", verdict({"us": 0.6, "england": 0.4})[0] == "REJECT")
    check("American at 0.30 in all is rejected", verdict({"england": 0.5, "us": 0.2, "canada": 0.1, "wales": 0.2})[0] == "REJECT")
    check("English on top, little American, passes", verdict({"england": 0.8, "us": 0.1, "wales": 0.1})[0] == "PASS")
    check("Scottish on top is for a listen", verdict({"scotland": 0.7, "england": 0.2, "us": 0.1})[0] == "REVIEW")
    data = os.path.join(MODEL, "data")
    if os.path.isdir(data):
        eng = verdict(scores(os.path.join(data, "england_1.wav")))
        us = verdict(scores(os.path.join(data, "us_1.wav")))
        check("the model's own English sample passes (%s %s)" % eng[:2], eng[0] == "PASS")
        check("the model's own American sample is rejected (%s %s)" % us[:2], us[0] == "REJECT")
    print("accent_check selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main(sys.argv[1:])
