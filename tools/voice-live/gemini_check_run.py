"""The lab's Gemini talk check (production/lab/talk-check/gemini_check.py, unchanged) run on a named model.

    python tools/voice-live/gemini_check_run.py MODEL [--no-thinking-config]

WHY, 22 October 2026 (his order of 21 October, item 8: "the Gemini Flash test once he has put the key
in the file"). The lab wrote the runner on 8 October and could not run it (the key file was empty).
Gemini 3.5 Flash-Lite refuses the runner's "thinking off" setting (thinkingBudget 0: HTTP 400, 22
October), and answers without it; --no-thinking-config sends the same request without that one
setting. Everything else, the key handling included (read into memory, sent only in the
x-goog-api-key header, never printed or written), is the lab's own code, imported, not copied.
"""
import importlib.util
import json
import os
import sys
import time
import urllib.request

LAB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "production", "lab", "talk-check", "gemini_check.py")


def load_lab():
    spec = importlib.util.spec_from_file_location("gemini_check", LAB)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    g = load_lab()
    if "--no-thinking-config" in argv:
        def call(key, model, system, user):
            body = {"systemInstruction": {"parts": [{"text": system}]}, "contents": [{"role": "user", "parts": [{"text": user}]}],
                    "generationConfig": {"maxOutputTokens": 300, "temperature": 0, "responseMimeType": "application/json"}}
            req = urllib.request.Request("%s/models/%s:generateContent" % (g.API, model), data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json", "x-goog-api-key": key})
            t = time.perf_counter()
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.load(r)
            return out, time.perf_counter() - t
        g.call = call
    sys.argv = [g.__file__] + [a for a in argv if not a.startswith("--")]
    g.main()


if __name__ == "__main__":
    main(sys.argv[1:])
