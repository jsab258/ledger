#!/usr/bin/env python3
"""The acting test: the same speaker from a calm and an acted reference, blind.

    C:\\LedgerTools\\chatterbox-nano\\env-dml\\Scripts\\python.exe tools/voice-live/acting-test.py [--only sheila-dunn]
    python tools/voice-live/acting-test.py --selftest

WHY, 25 September. Jafar judged every voice on the casting page "very flat".
The research he ordered (production/research/character-pipeline) says a calm
reference can carry calm delivery into every line, that nobody can say how
much of the flatness is the reference and how much the model without an A/B
test, and that the original Chatterbox's own advice for drama is about 0.7
exaggeration and 0.3 guidance (CFG), which also speeds speech. His ruling:
test calm against acted references with the engine we have, and try those
settings.

WHAT IT MAKES, per character (the voice he picked on the casting page):
- four lines, one each for threat, warmth, embarrassment and humour, so he
  judges each on its own;
- an ACTED reference per feeling: the same voice, cloned from its calm
  reference, reading a short passage in that feeling with the original
  engine pushed hard (exaggeration 1.0, CFG 0.3). There is no recording of
  these speakers acting, so this is the only acted reference of the SAME
  speaker there can be; said plainly on the page;
- every line four ways: calm or acted reference, times default settings
  (0.5, 0.5) or drama settings (0.7, 0.3). Same text, same seed, same engine.
The files are lettered at random per line; which is which goes in
production/casting/acting-key.json only.

THE ENGINE is the original Chatterbox (ChatterboxTTS, MIT, the one the crowd
lines are made with), on the processor: the game's live model (Nano) has
other controls, and the research warns the slider recipe may not carry over.
"""
import json
import os
import random
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CASTING = os.path.join(ROOT, "production", "casting")
KEY = os.path.join(CASTING, "acting-key.json")

VOICE = {   # the voice he picked on the casting page, 25 September morning
    "sheila-dunn": "production/casting/sheila-dunn/voices/sheila-dunn-D-reference.mp3",
    "ron-kirby": "production/casting/ron-kirby/voices/ron-kirby-A-reference.mp3",
    "darren-milner": "production/casting/darren-milner/voices/darren-milner-A-reference.mp3",
}

LINES = {
    "sheila-dunn": {
        "threat": "Put that book down. Now. You touch Mickey's ledgers again and the whole street will know what you are.",
        "warmth": "Sit down, love, you look done in. I'll put the kettle on. Mickey would have liked you, I think.",
        "embarrassment": "Oh. I didn't hear you come in. I was just talking to myself. Don't look at me like that.",
        "humour": "Thirty-one years, and the only thing that's ever balanced in this office is the dust on that shelf.",
    },
    "ron-kirby": {
        "threat": "Walk away, son. Thirty years on the docks, and I never once had to ask a man twice.",
        "warmth": "Here, get this tea down you. Mickey would've wanted someone looking out for you, and it may as well be me.",
        "embarrassment": "Ah. You weren't meant to see that. It's a letter, that's all. From my sister. Leave it, will you.",
        "humour": "Rain again. I've been wet since nineteen fifty-eight, boss. I don't even notice any more.",
    },
    "darren-milner": {
        "threat": "You want to be careful, you. People round here talk, and I'm the one they talk to.",
        "warmth": "So listen, you did me a good turn back there. I don't forget that. Anything you need, you come to me first.",
        "embarrassment": "That's not my pager. I'm minding it. For a mate. Stop laughing, it's not funny.",
        "humour": "So listen, I can get it you by Friday. Thursday I'd be lying. Wednesday I'd be in the cells.",
    },
}

# What the acted reference reads, per feeling: a passage in that feeling, not
# the test line (the reference must not rehearse the line it is judged on).
PASSAGES = {
    "threat": "I'm going to say this once, and you are going to listen. Stay away from this street, stay away from my door, and if I ever see you round here again, you will regret the day you came.",
    "warmth": "Oh, come here, you daft thing. It's all right. Honestly, it's all right. You did your best, and that's all anybody could ever ask of you. I'm proud of you, I really am.",
    "embarrassment": "Oh no. Oh, I'm so sorry, I didn't mean for you to hear that. I don't know what I was thinking. Can we just, can we forget I said anything? Please?",
    "humour": "And then he turns round, bold as brass, and says the cat did it. The cat! We haven't got a cat! I laughed so hard I had to sit down on the kerb.",
}

SETTINGS = {"default": (0.5, 0.5), "drama": (0.7, 0.3)}      # (exaggeration, cfg_weight)
ACTED_REF_SETTINGS = (1.0, 0.3)
SEED = 20260925


def conditions():
    return [(ref, s) for ref in ("calm", "acted") for s in ("default", "drama")]


def letters_for(slug, feeling):
    """Letters shuffled per line, by a fixed seed, so a rerun letters the same."""
    conds = conditions()
    r = random.Random("%s/%s/%d" % (slug, feeling, SEED))
    r.shuffle(conds)
    return {chr(ord("A") + i): {"reference": c[0], "settings": c[1]} for i, c in enumerate(conds)}


def load_model():
    import importlib
    import types
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    sys.path.insert(0, os.environ.get("NANO_PKG", r"C:\LedgerTools\chatterbox-nano\src-master\src"))
    # perth (the watermarker) needs pkg_resources.resource_filename, missing
    # in this environment; the voice server's own shim (voice-server.py).
    pr = types.ModuleType("pkg_resources")
    pr.resource_filename = lambda p, n: os.path.join(os.path.dirname(importlib.import_module(p).__file__), n)
    sys.modules.setdefault("pkg_resources", pr)
    import torch
    from chatterbox.tts import ChatterboxTTS
    return torch, ChatterboxTTS.from_pretrained(device="cpu")


def loud(data, sr, target=-20.0):
    import numpy as np
    import pyloudnorm as pyln
    lufs = pyln.Meter(sr).integrated_loudness(data)
    out = pyln.normalize.loudness(data, lufs, target)
    peak = float(np.max(np.abs(out))) or 1.0
    if peak > 0.89:
        out = out * (0.89 / peak)
    return out, lufs


def run(only=None):
    import soundfile as sf
    torch, model = load_model()
    key = json.load(open(KEY, encoding="utf-8")) if os.path.exists(KEY) else {}
    key.update({"what": "The acting test: which letter is which reference and settings. The approval page must not show this file.",
                "engine": "Chatterbox (original ChatterboxTTS, MIT), on the processor, temperature 0.8, min_p 0.05, repetition_penalty 1.2; every output carries Chatterbox's Perth watermark",
                "settings": {k: {"exaggeration": v[0], "cfg_weight": v[1]} for k, v in SETTINGS.items()},
                "acted_reference": {"exaggeration": ACTED_REF_SETTINGS[0], "cfg_weight": ACTED_REF_SETTINGS[1],
                                    "how": "the calm reference cloned, reading a passage in the feeling"},
                "seed": SEED})
    chars = key.setdefault("characters", {})
    for slug, calm_rel in VOICE.items():
        if only and slug != only:
            continue
        out_dir = os.path.join(CASTING, slug, "acting")
        os.makedirs(out_dir, exist_ok=True)
        calm = os.path.join(ROOT, calm_rel)
        ch = chars.setdefault(slug, {"voice": calm_rel, "lines": {}})
        for feeling, line in LINES[slug].items():
            done = ch["lines"].get(feeling)
            if done and done.get("line") == line and all(os.path.exists(os.path.join(ROOT, v["file"])) for v in done["letters"].values()):
                continue      # RESUMABLE: a line already made, with the same words, is kept
            t0 = time.time()
            # the acted reference, same speaker, this feeling
            torch.manual_seed(SEED)
            wav = model.generate(PASSAGES[feeling], audio_prompt_path=calm,
                                 exaggeration=ACTED_REF_SETTINGS[0], cfg_weight=ACTED_REF_SETTINGS[1])
            acted = os.path.join(out_dir, "%s-acted-reference-%s.mp3" % (slug, feeling))
            sf.write(acted, wav.squeeze(0).numpy(), model.sr, format="MP3")
            refs = {"calm": calm, "acted": acted}
            letters = letters_for(slug, feeling)
            entry = {"line": line, "acted_reference": os.path.relpath(acted, ROOT).replace("\\", "/"), "letters": {}}
            for letter, c in letters.items():
                ex, cfg = SETTINGS[c["settings"]]
                torch.manual_seed(SEED + 7)
                w = model.generate(line, audio_prompt_path=refs[c["reference"]], exaggeration=ex, cfg_weight=cfg)
                data = w.squeeze(0).numpy()
                norm, raw_lufs = loud(data, model.sr)
                name = "%s-%s-%s.mp3" % (slug, feeling, letter)
                sf.write(os.path.join(out_dir, name), norm, model.sr, format="MP3")
                entry["letters"][letter] = dict(c, file="production/casting/%s/acting/%s" % (slug, name),
                                                seconds=round(len(data) / model.sr, 2), raw_lufs=round(raw_lufs, 1))
            ch["lines"][feeling] = entry
            with open(KEY, "w", encoding="utf-8") as fh:
                json.dump(key, fh, indent=1, ensure_ascii=False)
            print("acting-test: %s %s done in %.0f s" % (slug, feeling, time.time() - t0), flush=True)
    return 0


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("acting-test selftest FAIL " + name)
    check("four conditions: calm and acted, default and drama", len(conditions()) == 4 and len(set(conditions())) == 4)
    a, b = letters_for("ron-kirby", "threat"), letters_for("ron-kirby", "threat")
    check("the letters are the same on a rerun", a == b)
    check("the letters differ between lines", any(letters_for("ron-kirby", f) != a for f in ("warmth", "humour", "embarrassment")))
    check("every character has the four feelings", all(set(v) == {"threat", "warmth", "embarrassment", "humour"} for v in LINES.values()))
    check("every picked voice is on disk", all(os.path.exists(os.path.join(ROOT, p)) for p in VOICE.values()))
    check("the drama settings are the research's", SETTINGS["drama"] == (0.7, 0.3))
    import re
    words = re.compile(r"\b(pint|beer|drunk|bet|bets|betting|child|children|kid|kids|boy|girl|pub)\b", re.I)
    check("no line breaks the content rule's commonest words",
          not any(words.search(t) for v in LINES.values() for t in v.values()) and not any(words.search(t) for t in PASSAGES.values()))
    print("acting-test selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    sys.exit(run(only))
