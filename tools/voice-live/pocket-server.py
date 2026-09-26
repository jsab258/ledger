#!/usr/bin/env python3
"""The cast speaking through Pocket TTS on the processor: the voice server's own line format, for trying beside it.

    F:\\LedgerTools\\pocket-tts\\env\\Scripts\\python.exe tools/voice-live/pocket-server.py [--prewarm] [--out DIR]

WHY, 26 September. Jafar: "Then Pocket TTS on the processor, with Sheila's,
Ron's and Darren's voices, beside the game. Check the accent before I hear
anything; reject any drift." Pocket TTS (Kyutai; code MIT, weights CC BY 4.0,
kyutai/pocket-tts) is a 100-million-parameter voice that runs on the processor
and clones a voice from a few seconds of speech, so it leaves the graphics
card to the game. It learns each character from the same clip the game uses
(game-design/picked-clips, voice-server.py's clip_for) and speaks the same
way: IN {"id":1,"who":"sam","text":"..."}; OUT one line per sentence,
{"id","part","piece","joined","pieceLast","last","who","wav","ms","seconds","rate"}:
it streams, so each sentence ("part") comes in pieces as its sound is made,
the first 0.16 s of sound at once and then every half second; a piece with
"joined": true continues the one before it with no gap, and "pieceLast" ends
the sentence. --prewarm learns the three cast voices
and speaks once before saying it is ready.
"""
import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
CAST = ("lena", "rocco", "sam")


def dumps(d):
    """Compact, as voice-server.py writes: the game reads "key":value with no space."""
    return json.dumps(d, separators=(",", ":"))


def server_module():
    spec = importlib.util.spec_from_file_location("voice_server", ROOT / "tools" / "voice-live" / "voice-server.py")
    vs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vs)
    return vs


def main(argv):
    # THE SIGN-IN (Jafar, 26 September: Kyutai's terms accepted, signed in on
    # this PC): the model cache lives on F:, the sign-in where hf put it.
    signed_in = pathlib.Path.home() / ".cache" / "huggingface" / "token"
    if "HF_TOKEN_PATH" not in os.environ and signed_in.exists():
        os.environ["HF_TOKEN_PATH"] = str(signed_in)
    os.environ.setdefault("HF_HOME", "F:/LedgerTools/hf")
    import numpy as np
    import soundfile as sf
    import torch
    from pocket_tts import TTSModel
    vs = server_module()
    out = pathlib.Path(argv[argv.index("--out") + 1]) if "--out" in argv else pathlib.Path(tempfile.mkdtemp(prefix="ledger-pocket-"))
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    torch.set_num_threads(max(2, (os.cpu_count() or 4) // 2))   # half the processor: the game keeps the rest
    # --temp: how freely the model varies its speech (Kyutai's default when
    # absent). Lower keeps a cloned voice nearer its clip (Darren's drifted
    # American at the default, 26 September).
    temp = float(argv[argv.index("--temp") + 1]) if "--temp" in argv else None
    model = TTSModel.load_model(temp=temp) if temp is not None else TTSModel.load_model()
    sr = model.sample_rate
    voices = {}

    def voice(who):
        if who not in voices:
            clip = vs.clip_for(who)
            if clip is None:
                return None
            voices[who] = model.get_state_for_audio_prompt(str(clip), truncate=True)
        return voices[who]

    def emit(i, who, k, g, chunks, piece_last, last_piece, t, n):
        data = np.concatenate(chunks)
        path = out / ("%d-%d-%d.wav" % (i, k, g))
        sf.write(str(path), data, sr, subtype="PCM_16")
        print(dumps({"id": i, "part": k, "piece": g, "joined": g > 0, "pieceLast": piece_last,
                          "last": piece_last and last_piece, "firstChunk": n == 0, "who": who, "wav": str(path),
                          "ms": int((time.time() - t) * 1000), "seconds": round(len(data) / sr, 2), "rate": sr}), flush=True)

    if "--prewarm" in argv:
        for who in CAST:
            st = voice(who)
            if st is not None:
                for _ in model.generate_audio_stream(st, "Right."):
                    pass
    print(dumps({"ready": True, "device": "cpu", "loadS": round(time.time() - t0, 1), "out": str(out), "rate": sr}), flush=True)
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            i, who, text = vs.parse(line)
        except Exception as e:
            print(dumps({"error": "bad-line", "why": str(e)[:80]}), flush=True)
            continue
        t = time.time()
        st = voice(who)
        if st is None:
            print(dumps({"id": i, "who": who, "error": "no-clip"}), flush=True)
            continue
        pieces = vs.sentences(text)
        n = 0
        for k, piece in enumerate(pieces):
            torch.manual_seed(20260926 + i * 100 + k)
            group, g = [], 0
            # THE FIRST SOUND AT ONCE, THE REST IN STEP: a piece's sound goes out
            # in groups as it is made, the first after two chunks (0.16 s of
            # sound), then every half second; the game joins a group to the one
            # before it with no gap ("joined"), and leaves its usual pause only
            # between sentences.
            want = 2
            for c in model.generate_audio_stream(st, piece):
                group.append(c.detach().cpu().numpy().reshape(-1))
                if len(group) >= want:
                    emit(i, who, k, g, group, False, k == len(pieces) - 1, t, n)
                    g, n, group, want = g + 1, n + 1, [], 6
            emit(i, who, k, g, group or [np.zeros(240, dtype=np.float32)], True, k == len(pieces) - 1, t, n)
            n += 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
