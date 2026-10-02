#!/usr/bin/env python3
"""The gate's first half for a voice take: the accent, the words, and whether it is still the same voice.

    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/voice-live/take_gate.py REPORT.json [--want england] [--out GATE.json]

REPORT.json lists takes ({"reference": <the approved voice's clip>, "takes": [{"file", "text", ...}]},
as F:/LedgerTools/tmp/voxcpm-trial/trial.py writes). For each take:
  ACCENT   CommonAccent's classifier (tools/voice-live/accent_check.py's model) over the whole take and
           2.5 s windows every 0.5 s: REJECT if American (US + Canada) tops the whole take, reaches 0.5
           over it, or reads 0.30 or more in windows running for more than 3 s (the rule calibrated on
           genuine English speech, 29 September: see WHY);
  WORDS    Whisper small.en's transcript against the line (word error rate; over 0.15 fails);
  LIKENESS ECAPA speaker embeddings (SpeechBrain spkrec-ecapa-voxceleb), cosine against the
           reference: under 0.45 fails (the approved voices' own lines score 0.5 to 0.8 against
           their references; Pocket's other man scored 0.51 to 0.58 and was heard as someone else,
           so 0.45 is a floor, not a pass on likeness).
WHY, 29 September (Jafar's list, item 6: VoxCPM2's acted lines on a blind page; CLAUDE.md's
gate: a voice drifting American or away from the named accent is rejected before he hears it).
THE WINDOW RULE, CALIBRATED, the same day (production/research/voice-alternatives-2026-09-24/
ACCENT-WINDOWS-2026-09-29.md): the first rule failed a take on any single 2.5 s window at 0.30
American, and it failed 11 of 50 clips of genuine northern English women (OpenSLR 83) as well
as three of their four ten-second references; their American stretches run up to 4.5 s. A run
of such windows longer than 3 s, or 0.5 over the whole take, still catches all 40 clips the
project had already judged American (the 39 casting clips taken out on 25 September and Pocket's
rejected take) and flags 3 of the 50 genuine ones.
"""
import json
import os
import re
import sys
import warnings

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPK_MODEL = os.environ.get("LEDGER_SPK_MODEL", "speechbrain/spkrec-ecapa-voxceleb")   # Apache-2.0; fetched to drive F
WER_MAX, LIKE_MIN, AMERICAN_MAX = 0.15, 0.45, 0.30
AMERICAN_RUN_MAX_S, AMERICAN_WHOLE_MAX = 3.0, 0.5


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def spell(n):
    """Numbers as they are spoken in these lines: to 99, and years as two pairs (1958: nineteen fifty eight)."""
    n = int(n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if 1000 <= n < 10000 and n % 100:
        return spell(n // 100) + " " + (("oh " + ONES[n % 100]) if n % 100 < 10 else spell(n % 100))
    return str(n)


def norm(s):
    s = re.sub(r"^\([^)]*\)", "", s).lower().replace("-", " ").replace("anymore", "any more")
    s = re.sub(r"\d+", lambda m: " " + spell(m.group()) + " ", s)
    return re.sub(r"[^a-z' ]", " ", s).split()


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = [[i + j if i * j == 0 else 0 for j in range(len(h) + 1)] for i in range(len(r) + 1)]
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (r[i - 1] != h[j - 1]))
    return d[-1][-1] / max(1, len(r))


def main(argv):
    import librosa
    import torch
    from speechbrain.inference.speaker import SpeakerRecognition
    from speechbrain.utils.fetching import LocalStrategy
    from transformers import pipeline
    from transformers.utils import logging as tl
    tl.set_verbosity_error()
    rep = json.load(open(argv[0], encoding="utf-8"))
    want = argv[argv.index("--want") + 1] if "--want" in argv else "england"
    out = argv[argv.index("--out") + 1] if "--out" in argv else argv[0].replace("-report.json", "-gate.json")
    # THE ACCENT exactly as the project's own check reads it (accent_check.py:
    # its model on drive F, its scale of 30 that turns the classifier's
    # cosines into probabilities, its verdict), over the whole take and its
    # worst 2.5 s window
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import accent_check as ac
    clf = ac.classifier()
    labels = clf.hparams.label_encoder.decode_ndim(list(range(16)))
    local = os.path.isdir(SPK_MODEL)
    sv = SpeakerRecognition.from_hparams(source=SPK_MODEL, savedir="F:/LedgerTools/models/sb-spk", run_opts={"device": "cpu"},
                                         local_strategy=LocalStrategy.COPY, **({"overrides": {"pretrained_path": SPK_MODEL}} if local else {}))
    asr = pipeline("automatic-speech-recognition", model="openai/whisper-small.en", device="cpu")

    def acc(y):
        out = clf.classify_batch(torch.tensor(y).unsqueeze(0))
        cos = out[0][0] if out[0].dim() == 2 else out[0]
        p = torch.softmax(cos * ac.SCALE, dim=-1)
        return {str(l): float(v) for l, v in zip(labels, p)}

    def load(f):
        return librosa.load(f if os.path.isabs(f) else os.path.join(ROOT, f), sr=16000)[0]
    ref = load(rep["reference"])
    ref_emb = sv.encode_batch(torch.tensor(ref).unsqueeze(0))[0, 0]
    rows = []
    for t in rep["takes"]:
        y = load(t["file"])
        sc = acc(y)
        verdict, top, us = ac.verdict(sc, want)
        worst = 0.0
        run = longest = 0
        for s in range(0, max(1, len(y) - 40000 + 1), 8000):
            sw = acc(y[s:s + 40000])
            a = sum(sw.get(x, 0.0) for x in ac.AMERICAN)
            worst = max(worst, a)
            run = run + 1 if a >= AMERICAN_MAX else 0
            longest = max(longest, run)
        # seconds the American-reading windows run for: 2.5 s for one, 0.5 s more for each after it
        run_s = (longest - 1) * 0.5 + 2.5 if longest else 0.0
        heard = asr({"raw": y, "sampling_rate": 16000})["text"].strip()
        w = wer(t["text"], heard)
        like = float(torch.nn.functional.cosine_similarity(sv.encode_batch(torch.tensor(y).unsqueeze(0))[0, 0], ref_emb, dim=0))
        fails = []
        if verdict == "REJECT" or us >= AMERICAN_WHOLE_MAX or run_s > AMERICAN_RUN_MAX_S:
            fails.append("american")
        elif verdict != "PASS":
            fails.append("accent:" + top)
        if w > WER_MAX:
            fails.append("words")
        # A STRAY FIRST WORD: cloned from a reference and its transcript, the
        # take can begin with the reference's own last word ("above." before
        # every one of Ron's, 29 September)
        hw, lw = norm(heard), norm(t["text"])
        if hw and lw and hw[0] != lw[0] and len(hw) > 1 and hw[1] == lw[0]:
            fails.append("stray-start:" + hw[0])
        if like < LIKE_MIN:
            fails.append("likeness")
        row = dict(t, accentTop=top, want=round(sc.get(want, 0.0), 2), american=round(us, 2), worstWindowAmerican=round(worst, 2), americanRunS=round(run_s, 1),
                   heard=heard, wer=round(w, 2), likeness=round(like, 2), verdict="PASS" if not fails else "FAIL:" + ",".join(fails))
        rows.append(row)
        print("%-9s %-38s %s=%.2f us=%.2f worst=%.2f wer=%.2f like=%.2f" % (row["verdict"], os.path.basename(t["file"]), want,
                                                                              row["want"], us, worst, w, like), flush=True)
    json.dump({"reference": rep["reference"], "rules": {"werMax": WER_MAX, "likenessMin": LIKE_MIN, "americanWindow": AMERICAN_MAX,
                                                        "americanRunMaxS": AMERICAN_RUN_MAX_S, "americanWholeMax": AMERICAN_WHOLE_MAX},
               "takes": rows}, open(out, "w", encoding="utf-8"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
