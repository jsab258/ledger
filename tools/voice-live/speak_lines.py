#!/usr/bin/env python3
"""Lines spoken through the game's own voice engine, from a character's game clip, for checking and for the approval page.

    env-dml\\Scripts\\python.exe tools/voice-live/speak_lines.py OUT.json
    (OUT.json names the jobs: [{"who": "sam", "lines": ["...", ...]}, ...]; the WAVs land beside it)

WHY, 25 September (evening): the approval page shows each character in the
game speaking in their voice, so the sound must be what the game makes: the
voice server's model (Chatterbox Nano), its seeds, its way of splitting a
line, from the clip the game uses (game-design/picked-clips). This imports
tools/voice-live/voice-server.py rather than copying it. Each line is then
checked by tools/voice-live/accent_check.py before it can reach the page,
and loudness is evened to -20 LUFS (peak at most 0.89), as the casting pages'
lines were; the reviewer found these 7 dB quieter than the references.
"""
import importlib.util
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def server():
    spec = importlib.util.spec_from_file_location("voice_server", ROOT / "tools" / "voice-live" / "voice-server.py")
    vs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vs)
    return vs


def loud(data, sr):
    import numpy as np
    import pyloudnorm
    meter = pyloudnorm.Meter(sr)
    y = pyloudnorm.normalize.loudness(data, meter.integrated_loudness(data), -20.0)
    peak = float(np.max(np.abs(y))) or 1.0
    return y * min(1.0, 0.89 / peak)


def main(jobs_path):
    import numpy as np
    import soundfile as sf
    vs = server()
    jobs = json.load(open(jobs_path, encoding="utf-8"))
    out = pathlib.Path(jobs_path).parent
    torch, speaker, dev = vs.load_models(False)
    done = []
    for job in jobs:
        who = job["who"]
        clip = job.get("clip") or vs.clip_for(who)
        conds, _ = vs.learn(torch, speaker, who, clip)
        speaker.conds = type(conds)(t3=conds.t3.to(device=dev),
                                    gen={k: (v.to("cpu") if torch.is_tensor(v) else v) for k, v in conds.gen.items()})
        for n, line in enumerate(job["lines"], 1):
            parts = []
            for k, piece in enumerate(vs.sentences(line)):
                torch.manual_seed(20260924 + n * 100 + k)      # the server's own seeds
                parts.append(speaker.generate(piece).squeeze(0).detach().cpu().numpy())
            gap = np.zeros(int(speaker.sr * 0.18), dtype=parts[0].dtype)
            data = np.concatenate([x for p in parts for x in (p, gap)][:-1])
            try:
                data = loud(data, speaker.sr)
            except Exception:
                pass                                           # loudness is a nicety, not a gate
            path = out / ("%s-%d.wav" % (who, n))
            sf.write(str(path), data, speaker.sr, subtype="PCM_16")
            done.append({"who": who, "clip": str(clip).replace("\\", "/"), "n": n, "text": line, "wav": str(path).replace("\\", "/"),
                         "seconds": round(len(data) / speaker.sr, 2)})
            print(json.dumps(done[-1]), flush=True)
    json.dump(done, open(out / "spoken.json", "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
