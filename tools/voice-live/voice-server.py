#!/usr/bin/env python3
"""THE CAST SPEAKS: a voice server beside the game, one JSON line each way.

    env-dml\\Scripts\\python.exe tools/voice-live/voice-server.py [--cpu] [--out DIR]
    python tools/voice-live/voice-server.py --selftest

WHY, 24 September. The roadmap's slice asks for talk "in their cast voices,
with the voice running". The playable encounter answers in text; this speaks
the answer in the character's own cast voice (Rocco p227, Lena p228, Sam
p241, from game-design/picked-clips), so the game can play it where they
stand.

HOW, from what this project already measured:
- The small model (Nano) makes the sound tokens on the card, and the vocoder
  runs on the processor, because DirectML has no complex numbers
  (production/research/nano-listening-test/nano_card_timing.py).
- Learning a voice aborts on the card (FINDINGS), so each cast voice is
  learned ONCE, on the processor, the first time that character speaks. The
  result is kept and handed to the card model.

IN:  {"id":1,"who":"sam","text":"So listen..."}
OUT: {"id":1,"who":"sam","wav":"C:/.../1.wav","ms":2310,"seconds":3.4}
     or {"id":1,"error":"no-clip"} - never a guess.
A first line {"ready":true,...} once the model is loaded.
"""
import glob
import json
import os
import pathlib
import sys
import tempfile
import time
import types
import importlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def dumps(d):
    """One compact line, the shape the game reads ("key":"value", no spaces)."""
    return json.dumps(d, separators=(",", ":"))
CLIPS = ROOT / "game-design" / "picked-clips"


def clip_for(who, clips=CLIPS):
    """The cast clip a character's voice is learned from: <who>.<speaker>.wav,
    or .mp3, the first by name. None if the character has no cast clip."""
    if not who or not all(c.isalnum() or c == "_" for c in who):
        return None
    found = sorted(glob.glob(str(clips / (who + ".*.wav")))) + sorted(glob.glob(str(clips / (who + ".*.mp3"))))
    return found[0] if found else None


def parse(line):
    """(id, who, text) or raises ValueError, naming what is missing."""
    d = json.loads(line)
    if not isinstance(d, dict):
        raise ValueError("not-an-object")
    i, who, text = d.get("id"), d.get("who"), d.get("text")
    if not isinstance(i, int) or not isinstance(who, str) or not isinstance(text, str) or not text.strip():
        raise ValueError("needs-id-who-text")
    return i, who, text.strip()[:600]


def load_models(cpu_only):
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    pkg = os.environ.get("NANO_PKG", r"C:\LedgerTools\chatterbox-nano\src-master\src")
    weights = os.environ.get("NANO_WEIGHTS", r"C:\LedgerTools\chatterbox-nano\weights")
    sys.path.insert(0, pkg)
    pr = types.ModuleType("pkg_resources")
    pr.resource_filename = lambda p, n: os.path.join(os.path.dirname(importlib.import_module(p).__file__), n)
    sys.modules.setdefault("pkg_resources", pr)
    import torch
    orig_load = torch.load

    def load_to_cpu(*a, **k):
        if k.get("map_location") is None:
            k["map_location"] = "cpu"
        return orig_load(*a, **k)
    torch.load = load_to_cpu

    class NoGrad(torch.no_grad):
        def __init__(self, mode=True):
            super().__init__()
    torch.inference_mode = NoGrad
    orig_cat = torch.cat

    def cat(tensors, dim=0, **k):
        if "out" in k:
            return orig_cat(tensors, dim, **k)
        ts = [t for t in tensors if t.numel() > 0]
        if not ts:
            return orig_cat(tensors, dim)
        return ts[0] if len(ts) == 1 else orig_cat(ts, dim)
    torch.cat = cat
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    learner = ChatterboxTurboTTS.from_local(weights, "cpu", nano=True)
    if cpu_only:
        return torch, learner, learner, "cpu"
    import torch_directml
    dev = torch_directml.device()
    speaker = ChatterboxTurboTTS.from_local(weights, dev, nano=True)
    speaker.s3gen.to("cpu")
    inf = speaker.s3gen.inference
    speaker.s3gen.inference = lambda speech_tokens, ref_dict, **k: inf(speech_tokens=speech_tokens.to("cpu"), ref_dict=ref_dict, **k)
    return torch, learner, speaker, dev


def serve(args):
    out = pathlib.Path(args.get("out") or tempfile.mkdtemp(prefix="ledger-voice-"))
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    torch, learner, speaker, dev = load_models(args.get("cpu"))
    import soundfile as sf
    voices = {}
    print(dumps({"ready": True, "device": str(dev), "loadS": round(time.time() - t0, 1), "out": str(out)}), flush=True)
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            i, who, text = parse(line)
        except Exception as e:
            print(dumps({"error": "bad-line", "why": str(e)[:80]}), flush=True)
            continue
        clip = clip_for(who)
        if clip is None:
            print(dumps({"id": i, "who": who, "error": "no-clip"}), flush=True)
            continue
        t = time.time()
        try:
            if who not in voices:
                learner.prepare_conditionals(clip)
                voices[who] = learner.conds
            conds = voices[who]
            if speaker is not learner:
                conds = type(conds)(t3=conds.t3.to(device=dev), gen={k: (v.to("cpu") if torch.is_tensor(v) else v)
                                                             for k, v in conds.gen.items()})
            speaker.conds = conds
            torch.manual_seed(20260924 + i)
            wav = speaker.generate(text)
            path = out / ("%d.wav" % i)
            data = wav.squeeze(0).detach().cpu().numpy()
            sf.write(str(path), data, speaker.sr, subtype="PCM_16")
            print(dumps({"id": i, "who": who, "wav": str(path), "ms": int((time.time() - t) * 1000),
                              "seconds": round(len(data) / speaker.sr, 2), "rate": speaker.sr}), flush=True)
        except Exception as e:
            print(dumps({"id": i, "who": who, "error": "failed", "why": type(e).__name__}), flush=True)
    return 0


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("voice-server selftest FAIL " + name)
    check("the three talkers have cast clips", all(clip_for(w) for w in ("rocco", "lena", "sam")))
    check("Sam's clip is his cast voice", (clip_for("sam") or "").replace("\\\\", "/").endswith("sam.p241.mp3"))
    check("nobody else's name reaches a path", clip_for("../secrets") is None and clip_for("") is None)
    check("a character with no clip is none", clip_for("nobody") is None)
    check("a good line parses", parse('{"id":3,"who":"lena","text":" New management. "}') == (3, "lena", "New management."))
    for badline in ('[1]', '{"id":"3","who":"lena","text":"x"}', '{"id":3,"who":"lena","text":"  "}', '{"id":3,"text":"x"}'):
        try:
            parse(badline)
            check("refuses " + badline, False)
        except ValueError:
            check("refuses " + badline, True)
    print("voice-server selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    a = {"cpu": "--cpu" in sys.argv}
    if "--out" in sys.argv:
        a["out"] = sys.argv[sys.argv.index("--out") + 1]
    sys.exit(serve(a))
