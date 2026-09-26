#!/usr/bin/env python3
"""The weekend page's voices: each character's sheet lines in the current voice and in Pocket TTS, blind-lettered and evened in loudness.

    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/voice-live/page_voices.py SPEC.json

WHY, 26 September. Jafar: Pocket TTS "blind beside the current voice, with
the measured delay for each". SPEC.json names, per character, the two
engines' WAV folders (made by speaking the sheet's three lines through
voice-server.py and pocket-server.py, the game's own two servers), the lines
that passed the accent check in BOTH voices (a line one voice fails is left
out for both, so the comparison stays like for like), and each engine's
measured delay. The letters are drawn with a fixed seed; which is which goes
to production/casting/voice-key-2026-09-26.json and never onto the page.
Loudness is evened to -20 LUFS, peak at most 0.89, as the casting pages were
(tools/voice-live/speak_lines.py's loud()), so neither voice wins by volume.
"""
import importlib.util
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "production" / "casting" / "voices-2026-09-26"
KEY = ROOT / "production" / "casting" / "voice-key-2026-09-26.json"


def loud():
    spec = importlib.util.spec_from_file_location("speak_lines", ROOT / "tools" / "voice-live" / "speak_lines.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.loud


def main(spec_path):
    import soundfile as sf
    spec = json.load(open(spec_path, encoding="utf-8"))
    even = loud()
    rng = random.Random(20260926)
    key = {"what": "Which letter is which voice on the 26 September weekend page. The page must not show this file.",
           "made": "2026-09-26", "engines": spec["engines"]}
    for slug, c in spec["characters"].items():
        (OUT / slug).mkdir(parents=True, exist_ok=True)
        engines = list(c["folders"])
        rng.shuffle(engines)
        letters = {}
        for letter, engine in zip("AB", engines):
            letters[letter] = {"engine": engine, "delay": spec["engines"][engine]["delay"], "lines": []}
            for n in c["lines"]:
                data, sr = sf.read(str(pathlib.Path(c["folders"][engine]) / ("%s-%d.wav" % (c["who"], n))), dtype="float32")
                if data.ndim > 1:
                    data = data.mean(axis=1)
                dest = OUT / slug / ("%s-line%d.wav" % (letter, len(letters[letter]["lines"]) + 1))
                sf.write(str(dest), even(data, sr), sr, subtype="PCM_16")
                letters[letter]["lines"].append({"file": str(dest.relative_to(ROOT)).replace("\\", "/"), "sheetLine": n})
        key[slug] = {"letters": letters}
        # the speaking faces' own line: the audio their animation was made from
        if c.get("speaking"):
            data, sr = sf.read(c["speaking"], dtype="float32")
            sf.write(str(OUT / slug / "speaking-line.wav"), data if data.ndim == 1 else data.mean(axis=1), sr, subtype="PCM_16")
    for slug in spec.get("speakingOnly", {}):
        (OUT / slug).mkdir(parents=True, exist_ok=True)
        data, sr = sf.read(spec["speakingOnly"][slug], dtype="float32")
        sf.write(str(OUT / slug / "speaking-line.wav"), data if data.ndim == 1 else data.mean(axis=1), sr, subtype="PCM_16")
    KEY.write_text(json.dumps(key, indent=1), encoding="utf-8")
    print("page_voices: %d characters, key at %s" % (len(spec["characters"]), KEY.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
