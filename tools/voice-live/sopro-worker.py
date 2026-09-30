#!/usr/bin/env python3
"""SOPRO BEHIND THE VOICE SERVER: one JSON line each way, in the voice server's own shape.

    F:/LedgerTools/sopro/.venv/Scripts/python.exe tools/voice-live/sopro-worker.py --out DIR
    python tools/voice-live/sopro-worker.py --selftest

WHY, 29 September (Jafar's list, item 6, the voice half of the delay, free
routes only). The game's engine (Chatterbox Nano) takes about 4 s to the first
sound; Sopro V2 Turbo (Apache-2.0, on the processor) took 0.8 to 1.4 s and held
Ron's accent on 15 of 16 test lines of the accent gate at a steadier sampler
(temperature 0.5, top-k 15) with his approved in-game line added to the
reference (tools/voice-live/sopro_takes.py; it lost Darren's Scottish). The
voice server (voice-server.py) starts this worker for the characters that
production/specs/voice-engines.json gives to Sopro and forwards their lines,
so the game's side is unchanged. Nobody is given to Sopro without Jafar's yes
on a blind page ("no voice is cast without his yes").

IN:  {"id":1,"who":"rocco","text":"...","clip":"C:/.../rocco.p227.mp3","extra":"C:/.../ron-kirby.wav"}
OUT: {"id":1,"part":0,"last":false,"who":"rocco","wav":"DIR/1-0.wav","ms":910,"seconds":2.1,"rate":24000}
     or {"id":1,"who":"rocco","error":"failed","why":"..."}; first {"ready":true,...}.
"""
import json
import os
import pathlib
import sys
import time

TEMPERATURE, TOP_K = 0.5, 15
# STREAMED, ON CAPPED THREADS (item 2, the delay; production/research/voice-latency):
# LEDGER_SOPRO_STREAM=1 sends each sentence's sound in 64-frame chunks as they
# are made, the first on its own and the rest "joined" onto it (the game adds a
# joined piece to the sound already playing), then a closing line with no
# sound; LEDGER_SOPRO_THREADS caps the processor threads (3 of the 5600X's 6
# by default, leaving the game its share). Measured alone on 30 September:
# first chunk 0.81 s median against 1.81 s for the whole sentence.
STREAM_CHUNK_FRAMES = 64


def threads_wanted(env=None):
    env = os.environ if env is None else env
    try:
        n = int(env.get("LEDGER_SOPRO_THREADS", "3"))
    except ValueError:
        n = 3
    return max(1, min(n, 16))


def streaming(env=None):
    env = os.environ if env is None else env
    return env.get("LEDGER_SOPRO_STREAM", "") == "1"


def raise_priority():
    """ITS SHORT BURSTS AHEAD OF THE GAME'S (item 2): beside the game on 30
    September the first chunk took 1.4 to 4.6 s against 0.8 alone; the worker
    asks Windows for "above normal" priority for its own process only (a
    process setting, not a system one). True when granted."""
    if os.name != "nt" or os.environ.get("LEDGER_SOPRO_PRIORITY", "above") != "above":
        return False
    try:
        import ctypes
        k = ctypes.windll.kernel32
        return bool(k.SetPriorityClass(k.GetCurrentProcess(), 0x00008000))   # ABOVE_NORMAL_PRIORITY_CLASS
    except Exception:
        return False
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def dumps(d):
    return json.dumps(d, separators=(",", ":"))


_VS = []


def sentences(text):
    """The voice server's own split, so both engines break an answer alike."""
    if not _VS:
        import importlib.util
        spec = importlib.util.spec_from_file_location("voice_server", HERE / "voice-server.py")
        vs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vs)
        _VS.append(vs)
    return _VS[0].sentences(text)


def joined_reference(clip, extra, out):
    """The cast clip, with the approved in-game line after it when there is one."""
    if not extra:
        return clip
    import numpy as np
    import soundfile as sf
    a, sra = sf.read(clip, dtype="float32", always_2d=True)
    b, srb = sf.read(extra, dtype="float32", always_2d=True)
    if srb != sra:
        import torch
        import torchaudio
        b = torchaudio.functional.resample(torch.from_numpy(b.T.copy()), srb, sra).numpy().T
    p = pathlib.Path(out) / ("ref-%s-%s.wav" % (pathlib.Path(clip).stem, pathlib.Path(extra).stem))
    sf.write(str(p), np.concatenate([a.mean(axis=1), np.zeros(int(0.4 * sra), "float32"), b.mean(axis=1)]), sra)
    return str(p)


def serve(out):
    os.environ.setdefault("HF_HOME", "F:/LedgerTools/hf")
    os.environ["HF_HUB_OFFLINE"] = "1"
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    lifted = raise_priority()
    import torch
    torch.set_num_threads(threads_wanted())
    from sopro import SoproTTS
    tts = SoproTTS.from_pretrained("samuel-vitorino/sopro-v2-turbo", device="cpu")
    sr = getattr(tts, "sample_rate", None) or 24000
    split = sentences
    refs = {}
    print(dumps({"ready": True, "engine": "sopro", "loadS": round(time.time() - t0, 1), "threads": torch.get_num_threads(),
                 "stream": streaming(), "priority": "above" if lifted else "normal"}), flush=True)
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            d = json.loads(line)
            i, who, text, clip = d["id"], d["who"], d["text"], d["clip"]
        except Exception as e:
            print(dumps({"error": "bad-line", "why": str(e)[:80]}), flush=True)
            continue
        t = time.time()
        try:
            key = (clip, d.get("extra") or "")
            if key not in refs:
                refs[key] = tts.prepare_reference(joined_reference(clip, d.get("extra"), out))
            pieces = split(text)
            if streaming():
                n = 0
                for k, piece in enumerate(pieces):
                    torch.manual_seed(20260929 + i * 100 + k)
                    for j, chunk in enumerate(tts.stream(piece, ref=refs[key], lang="en", temperature=TEMPERATURE, top_k=TOP_K,
                                                         chunk_frames=STREAM_CHUNK_FRAMES)):
                        path = out / ("s%d-%d-%d.wav" % (i, k, j))
                        tts.save_wav(str(path), chunk)
                        print(dumps({"id": i, "part": n, "last": False, "joined": j > 0, "who": who, "wav": str(path),
                                     "ms": int((time.time() - t) * 1000), "seconds": round(chunk.numel() / sr, 2), "rate": sr}), flush=True)
                        n += 1
                print(dumps({"id": i, "part": n, "last": True, "who": who, "ms": int((time.time() - t) * 1000)}), flush=True)
                continue
            for k, piece in enumerate(pieces):
                torch.manual_seed(20260929 + i * 100 + k)
                wav = tts.synthesize(piece, ref=refs[key], lang="en", temperature=TEMPERATURE, top_k=TOP_K)
                path = out / ("s%d-%d.wav" % (i, k))
                tts.save_wav(str(path), wav)
                print(dumps({"id": i, "part": k, "last": k == len(pieces) - 1, "who": who, "wav": str(path),
                             "ms": int((time.time() - t) * 1000), "seconds": round(wav.numel() / sr, 2), "rate": sr}), flush=True)
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
            print("sopro-worker selftest FAIL " + name)
    check("it splits an answer as the voice server does",
          sentences("So listen. You were here, weren't you?") == ["So listen.", "You were here, weren't you?"])
    check("a clip with no extra line is used as it is", joined_reference("a.mp3", "", ".") == "a.mp3")
    check("its output lines have the voice server's shape",
          set(json.loads(dumps({"id": 1, "part": 0, "last": True, "who": "rocco", "wav": "x", "ms": 1, "seconds": 1.0, "rate": 24000})))
          == {"id", "part", "last", "who", "wav", "ms", "seconds", "rate"})
    check("the sampler is the one that held Ron's accent", (TEMPERATURE, TOP_K) == (0.5, 15))
    check("threads are capped at three unless set, never below one or above sixteen",
          threads_wanted({}) == 3 and threads_wanted({"LEDGER_SOPRO_THREADS": "0"}) == 1 and threads_wanted({"LEDGER_SOPRO_THREADS": "99"}) == 16)
    check("streaming only when asked", streaming({}) is False and streaming({"LEDGER_SOPRO_STREAM": "1"}) is True)
    print("sopro-worker selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(serve(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "F:/LedgerTools/tmp/sopro-voice"))
