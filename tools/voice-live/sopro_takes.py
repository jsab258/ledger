"""Sopro V2 Turbo's takes of a character's test lines, timed as the game would stream them.

    F:/LedgerTools/sopro/.venv/Scripts/python.exe tools/voice-live/sopro_takes.py WHO REFERENCE [OUT]

WHO is a key of OUT/lines.json (the four test lines per character the VoxCPM2
trial used, F:/LedgerTools/tmp/voxcpm-trial/lines.json, copied beside); REFERENCE
the approved voice's clip (repo path). Writes OUT/<who>-<feeling>.wav and
OUT/<who>-report.json in take_gate.py's form, with each take's time to its first
streamed chunk, its compute time and its length.

WHY, 29 September (Jafar's list, item 6, and his ruling: no paid voice service,
keep working the free routes). The game's voice engine (Chatterbox Nano) takes
about 4 s after the words arrive; the latency research of 25 September
(production/research/live-speech-architecture/conversation-latency-2026-09-25.md)
names Sopro V2 Turbo (Apache-2.0, 120M, streaming, clones from a 5 to 20 s
reference) as the free engine to audition if Pocket's likeness failed, which it
did (it drifted American). Installed 29 September in F:/LedgerTools/sopro (CPU
torch, sopro 2.2.0); its model in F:/LedgerTools/hf. The accent and likeness
are judged by take_gate.py before anyone hears a take.
"""
import json
import os
import shutil
import sys
import time

os.environ.setdefault("HF_HOME", "F:/LedgerTools/hf")
import torch
from sopro import SoproTTS

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
who, ref = sys.argv[1], sys.argv[2]
OUT = sys.argv[3] if len(sys.argv) > 3 else "F:/LedgerTools/tmp/sopro-trial"
os.makedirs(OUT, exist_ok=True)
if not os.path.exists(OUT + "/lines.json"):
    shutil.copy("F:/LedgerTools/tmp/voxcpm-trial/lines.json", OUT + "/lines.json")
LINES = json.load(open(OUT + "/lines.json", encoding="utf-8"))[who]

t0 = time.time()
tts = SoproTTS.from_pretrained("samuel-vitorino/sopro-v2-turbo", device="cpu")
load_s = time.time() - t0
# ATTEMPT 2 (the first drifted off accent on most lines, likeness strong): a
# steadier sampler and, optionally, the approved in-game line added to the
# reference (SOPRO_TEMP, SOPRO_TOPK, SOPRO_EXTRA_REF, a repo path).
TEMP = float(os.environ.get("SOPRO_TEMP", "0") or 0) or None
TOPK = int(os.environ.get("SOPRO_TOPK", "0") or 0) or None
ref_path = os.path.join(ROOT, ref)
extra = os.environ.get("SOPRO_EXTRA_REF", "")
if extra:
    import soundfile as sf
    import numpy as np
    a, sra = sf.read(ref_path, dtype="float32", always_2d=True)
    b, srb = sf.read(os.path.join(ROOT, extra), dtype="float32", always_2d=True)
    if srb != sra:
        import torchaudio
        b = torchaudio.functional.resample(torch.from_numpy(b.T.copy()), srb, sra).numpy().T
    joined = np.concatenate([a.mean(axis=1), np.zeros(int(0.4 * sra), "float32"), b.mean(axis=1)])
    ref_path = os.path.join(OUT, "%s-ref-joined.wav" % who)
    sf.write(ref_path, joined, sra)
t0 = time.time()
reference = tts.prepare_reference(ref_path)                      # once per voice, as the game would at start
prep_s = time.time() - t0
print("LOADED %.1f s, reference %.1f s, threads %d" % (load_s, prep_s, torch.get_num_threads()), flush=True)
sr = getattr(tts, "sample_rate", None) or getattr(getattr(tts, "config", None), "sample_rate", None) or 24000

report = {"who": who, "engine": "sopro-v2-turbo (sopro 2.2.0, CPU)", "reference": ref, "extra_reference": extra,
          "temperature": TEMP, "top_k": TOPK, "load_s": round(load_s, 1),
          "reference_s": round(prep_s, 2), "threads": torch.get_num_threads(), "takes": []}
for feeling, line in LINES.items():
    chunks, first = [], None
    t0 = time.time()
    for chunk in tts.stream(line, ref=reference, lang="en", temperature=TEMP, top_k=TOPK):
        if first is None:
            first = time.time() - t0
        chunks.append(chunk.detach().cpu().reshape(-1))
    secs = time.time() - t0
    wav = torch.cat(chunks) if chunks else torch.zeros(1)
    f = OUT + "/%s-%s.wav" % (who, feeling)
    tts.save_wav(f, wav)
    dur = wav.numel() / sr
    print("TAKE %s %s: first sound %.2f s, %.1f s of audio in %.1f s" % (who, feeling, first or -1, dur, secs), flush=True)
    report["takes"].append({"feeling": feeling, "file": f, "text": line, "first_chunk_s": round(first or -1, 2),
                            "compute_s": round(secs, 2), "audio_s": round(dur, 2)})
json.dump(report, open(OUT + "/%s-report.json" % who, "w", encoding="utf-8"), indent=1)
print("DONE", who, flush=True)
