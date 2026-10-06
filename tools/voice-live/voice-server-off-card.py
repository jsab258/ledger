#!/usr/bin/env python3
"""THE CAST SPEAKS OFF THE CARD (proof P2, 6 October 2026): today's voice server's
protocol, one JSON line each way, with the whole voice on the processor
(tools/voice-live/off_card.py). Today's voice-server.py is untouched and stays
the game's voice; this is for measuring beside it, and the game can be pointed
at it with -VoicePython= and -VoiceScript= (no change to the game).

    env-dml\\Scripts\\python.exe tools/voice-live/voice-server-off-card.py [--prewarm] [--out DIR]

Settings (environment):
  LEDGER_VOICE_STEP_GRAPH   the token step graph (default nano-step-int8.onnx)
  LEDGER_VOICE_FLOW_GRAPH   the decoder's flow graph (default nano-flow-int8.onnx; "torch" = the library's)
  LEDGER_VOICE_REF_TOKENS   the decoder reads only the reference's last N tokens (default all 250)
  LEDGER_VOICE_THREADS      threads (default 4), never spinning
  LEDGER_VOICE_CORES        logical processors the voice keeps to, e.g. "8-11" (default none)

IN:  {"id":1,"who":"sam","text":"So listen...","turn":3}
OUT: {"id":1,"part":0,"last":false,"who":"sam","wav":"F:/.../1-0.wav","ms":910,"seconds":1.4,"rate":24000,...}
A first line {"ready":true,...} once the model is loaded.
"""
import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import threading
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def dumps(d):
    return json.dumps(d, separators=(",", ":"))


def main(argv):
    import off_card
    t0 = time.time()
    pinned = off_card.pin_process(off_card.cores_from(os.environ.get("LEDGER_VOICE_CORES", "")))
    step = os.environ.get("LEDGER_VOICE_STEP_GRAPH", "nano-step-int8.onnx")
    flow = os.environ.get("LEDGER_VOICE_FLOW_GRAPH", "nano-flow-int8.onnx")
    v = off_card.OffCardVoice(step=step, flow=None if flow == "torch" else flow)
    vs = v.vs
    import soundfile as sf
    scratch = pathlib.Path("F:/LedgerTools/tmp")
    out = pathlib.Path(argv[argv.index("--out") + 1]) if "--out" in argv else \
        pathlib.Path(tempfile.mkdtemp(prefix="ledger-voice-offcard-", dir=str(scratch) if scratch.is_dir() else None))
    out.mkdir(parents=True, exist_ok=True)
    warmed = []
    if "--prewarm" in argv:
        for who in vs.CAST:
            clip = vs.clip_for(who)
            if clip:
                v.ready(who, clip)
                v.speak("Right.", 1)
                warmed.append(who)
    print(dumps({"ready": True, "device": "cpu", "engine": "off-card", "step": step, "flow": flow,
                 "refTokens": int(os.environ.get("LEDGER_VOICE_REF_TOKENS", "0") or 0), "threads": v.threads,
                 "pinned": pinned, "loadS": round(time.time() - t0, 1), "out": str(out), "warmed": warmed}), flush=True)
    inbox, gate, ended = [], threading.Condition(), [False]

    def reader():
        for raw in sys.stdin:
            if raw.strip():
                with gate:
                    inbox.append((vs.turn_of(raw), raw))
                    gate.notify()
        with gate:
            ended[0] = True
            gate.notify()
    threading.Thread(target=reader, daemon=True).start()
    newest = 0

    def newer_waiting(turn):
        with gate:
            return turn > 0 and any(t2 > turn for t2, _ in inbox)
    while True:
        with gate:
            while not inbox and not ended[0]:
                gate.wait()
            if not inbox and ended[0]:
                break
            line, dropped, rest, newest = vs.pick(inbox, newest)
            inbox[:] = rest
        for old in dropped:
            try:
                oi, owho, _ = vs.parse(old)
                print(dumps({"id": oi, "who": owho, "last": True, "skipped": "older-turn"}), flush=True)
            except Exception:
                pass
        if line is None:
            continue
        this_turn = vs.turn_of(line)
        try:
            i, who, text = vs.parse(line)
        except Exception as e:
            print(dumps({"error": "bad-line", "why": str(e)[:80]}), flush=True)
            continue
        clip = vs.clip_for(who)
        if clip is None:
            print(dumps({"id": i, "who": who, "error": "no-clip"}), flush=True)
            continue
        t = time.time()
        try:
            pieces = vs.sentences(text)
            for k, piece in enumerate(pieces):
                if k > 0 and newer_waiting(this_turn):
                    print(dumps({"id": i, "who": who, "last": True, "cut": "newer-turn"}), flush=True)
                    break
                v.ready(who, clip)
                wav, timing = v.speak(piece, 20260924 + i * 100 + k)
                path = out / ("%d-%d.wav" % (i, k))
                sf.write(str(path), wav, v.speaker.sr, subtype="PCM_16")
                d = {"id": i, "part": k, "last": k == len(pieces) - 1, "who": who, "wav": str(path),
                     "ms": int((time.time() - t) * 1000), "seconds": round(len(wav) / v.speaker.sr, 2), "rate": v.speaker.sr}
                d.update(timing)
                print(dumps(d), flush=True)
        except Exception as e:
            print(dumps({"id": i, "who": who, "error": "failed", "why": type(e).__name__, "msg": str(e)[:160]}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
