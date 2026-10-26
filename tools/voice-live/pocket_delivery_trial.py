#!/usr/bin/env python3
"""One character's lines through Pocket at several temperatures, made exactly as the game's voice program makes them,
for the gate (take_gate.py) and then his ear.

    F:/LedgerTools/pocket-tts/env/Scripts/python.exe tools/voice-live/pocket_delivery_trial.py OUT_DIR
        [--ref game-design/pocket-voices/sam.wav] [--temps 0.3,0.45,0.6,0.8] [--lines LINES.json] [--whole]

WHY, 26 October 2026. His note on Darren's new voice: "A is ok, but very robotic and unemotional". The research
(production/research/voice-latency/POCKET-DELIVERY-2026-10-26.md) found the clip the voice is learned from sets its
style (Darren's is read newspaper sentences), and temperature is Pocket's only liveliness setting (Kyutai's docs:
1.0 "more expressive"; the game runs at the default, 0.3; higher also moves the voice further from its clip). This
makes the cheapest try first: the same lines at each temperature, each a separate take for the gate.

AS THE GAME MAKES THEM (tools/voice-live/pocket-server.py): each line cut into pieces by voice-server.py's
sentences() (the first piece kept short, cut at a comma), each piece made from the clip alone with the server's own
seed, the pieces joined with --gap seconds of silence (the game's pause between sentences). --whole makes each line
in one piece instead, to hear what the comma cut does.

Writes OUT_DIR/t<temp>/<n>.wav and OUT_DIR/t<temp>/report.json ({"reference", "takes": [{"file", "text"}]}), and the
time each line's first sound took.
"""
import importlib.util
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
SHEET = [
    "Alright? Darren. You'll have heard of me. No? You will, give it a week.",
    "Tell you what, I can get you anything, me. Radio, pager, a lift to Grimsby. Mates' rates.",
    "I never saw nothing. Well. I saw a bit. Depends who's asking, doesn't it, and what it's worth.",
    "A shape's not much to go on. Half the town could pass for that on a night like this.",
    "You'd know him again, that's something. Next time that face shows, you sing out.",
    "The new owner and a broken window on Quay Street. That'll travel faster than the tide does.",
]


def main(a):
    import numpy as np
    import soundfile as sf
    import torch
    from pocket_tts import TTSModel

    opt = lambda n, d: a[a.index(n) + 1] if n in a else d  # noqa: E731
    out = pathlib.Path(a[0])
    ref = str(ROOT / opt("--ref", "game-design/pocket-voices/sam.wav"))
    temps = [float(t) for t in opt("--temps", "0.3,0.45,0.6,0.8").split(",")]
    lines = json.load(open(opt("--lines", ""), encoding="utf-8")) if "--lines" in a else SHEET
    gap = float(opt("--gap", "0.25"))
    spec = importlib.util.spec_from_file_location("voice_server", ROOT / "tools" / "voice-live" / "voice-server.py")
    vs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vs)
    for temp in temps:
        model = TTSModel.load_model(temp=temp)
        sr = model.sample_rate
        st = model.get_state_for_audio_prompt(ref, truncate=True)
        d = out / ("t%s%s" % (str(temp).replace(".", ""), "-whole" if "--whole" in a else ""))
        d.mkdir(parents=True, exist_ok=True)
        takes = []
        for i, line in enumerate(lines):
            pieces = [line] if "--whole" in a else vs.sentences(line)
            audio, t0, first = [], time.time(), None
            for k, piece in enumerate(pieces):
                torch.manual_seed(20260926 + i * 100 + k)
                for c in model.generate_audio_stream(st, piece):
                    if first is None:
                        first = time.time() - t0
                    audio.append(c.detach().cpu().numpy().reshape(-1))
                if k < len(pieces) - 1:
                    audio.append(np.zeros(int(gap * sr), dtype=np.float32))
            f = d / ("%d.wav" % (i + 1))
            sf.write(str(f), np.concatenate(audio), sr, subtype="PCM_16")
            takes.append({"file": str(f), "text": line, "temp": temp, "pieces": pieces, "firstSoundS": round(first or 0, 3)})
            print("t=%s line %d first sound %.2f s" % (temp, i + 1, first or 0), flush=True)
        json.dump({"reference": ref, "takes": takes}, open(d / "report.json", "w", encoding="utf-8"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
