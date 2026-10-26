#!/usr/bin/env python3
"""The same lines as speak_lines.py, spoken through Pocket TTS on the processor, for the listening page.

    F:\\LedgerTools\\pocket-tts\\env\\Scripts\\python.exe tools/voice-live/speak_lines_pocket.py OUT.json
    (OUT.json names the jobs, as speak_lines.py's: [{"who": "sam", "lines": ["...", ...]}, ...]; WAVs land beside it)

WHY, 26 October. Jafar: "the listening test first. Put the same three lines in the cast voice and in Pocket on
my page. If Pocket's accent passes, live lines move to Pocket." The cast voice's lines come from speak_lines.py
(the game's own voice program); these come from tools/voice-live/pocket-server.py, the game's own Pocket server,
learning each character from the same cast clip. The server streams each sentence in pieces; a piece marked
"joined" continues the one before it with no gap, and sentences are set 0.18 s apart, as speak_lines.py sets
the cast voice's. Loudness is evened to -20 LUFS (peak at most 0.89), speak_lines.py's loud().
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SERVER = ROOT / "tools" / "voice-live" / "pocket-server.py"


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
    jobs = json.load(open(jobs_path, encoding="utf-8"))
    out = pathlib.Path(jobs_path).parent
    tmp = out / "pocket-pieces"
    tmp.mkdir(exist_ok=True)
    p = subprocess.Popen([sys.executable, str(SERVER), "--out", str(tmp)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1)
    while True:
        msg = json.loads(p.stdout.readline())
        if msg.get("ready"):
            break
    done = []
    i = 0
    for job in jobs:
        who = job["who"]
        for n, line in enumerate(job["lines"], 1):
            i += 1
            p.stdin.write(json.dumps({"id": i, "who": who, "text": line}) + "\n")
            p.stdin.flush()
            parts, sr = [], 24000
            while True:
                msg = json.loads(p.stdout.readline())
                if msg.get("error"):
                    raise SystemExit("pocket: %s for %s" % (msg["error"], who))
                if msg.get("id") != i:
                    continue
                data, sr = sf.read(msg["wav"], dtype="float32")
                if msg.get("joined") and parts:
                    parts[-1] = np.concatenate([parts[-1], data])
                else:
                    parts.append(data)
                if msg.get("last"):
                    break
            gap = np.zeros(int(sr * 0.18), dtype=parts[0].dtype)
            data = np.concatenate([x for q in parts for x in (q, gap)][:-1])
            try:
                data = loud(data, sr)
            except Exception:
                pass                                           # loudness is a nicety, not a gate
            path = out / ("%s-%d.wav" % (who, n))
            sf.write(str(path), data, sr, subtype="PCM_16")
            done.append({"who": who, "n": n, "text": line, "wav": str(path).replace("\\", "/"), "seconds": round(len(data) / sr, 2)})
            print(json.dumps(done[-1]), flush=True)
    p.stdin.close()
    p.wait(timeout=30)
    json.dump(done, open(out / "spoken.json", "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
