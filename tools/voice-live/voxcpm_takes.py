"""Acted lines made in advance with VoxCPM2: each line cloned from a character's voice, plain and with acting direction.

    F:/LedgerTools/voxcpm2/.venv/Scripts/python.exe tools/voice-live/voxcpm_takes.py WHO REFERENCE   (run in OUT, beside lines.json)

WHY, 29 September (Jafar's list, item 6: "livelier lines: VoxCPM2 with acting
direction per line for the lines made in advance, on a blind page";
production/research/character-pipeline/RESEARCH-2026-09-25.md, route 2).
VoxCPM2 (openbmb/VoxCPM2, Apache-2.0) runs here on the processor (the card is
not one its examples support), about 25 times slower than speech, which is
fine for lines made in advance. Its model is in F:/LedgerTools/hf and its
environment in F:/LedgerTools/voxcpm2 (CPU torch; optimize=False, since
compiling the model ended the process without a word).

For each of the four feelings of tools/voice-live/acting-test.py a line is
made two ways: PLAIN, cloned from the reference and its transcript (Whisper
small.en), and DIRECTED, from the reference alone with the direction in
brackets before the line. The plain way began every one of Ron's takes with
the reference's own last word ("above"), so directed is the one to use. Every
take goes through tools/voice-live/take_gate.py before anyone hears it.
"""
import os, sys, time, json, re
os.environ.setdefault("HF_HOME", "F:/LedgerTools/hf")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, soundfile as sf, librosa, torch
torch.set_num_threads(os.cpu_count())
ROOT = "C:/Users/Jafar/ledger-local"
OUT = "F:/LedgerTools/tmp/voxcpm-trial"
who, ref = sys.argv[1], sys.argv[2]
LINES = json.load(open(OUT + "/lines.json", encoding="utf-8"))[who]
DIRECTION = {
    "threat": "low, slow and cold, quietly menacing",
    "warmth": "warm and gentle, kindly, a little tired",
    "embarrassment": "awkward and flustered, hesitant, caught out",
    "humour": "dry and wry, deadpan, amused",
}
# the reference, as 16 kHz mono wav, and its words
y, sr = librosa.load(ROOT + "/" + ref, sr=16000, mono=True)
refwav = OUT + "/%s-ref.wav" % who
sf.write(refwav, y, 16000)
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="openai/whisper-small.en", device="cpu")
ref_text = asr({"raw": y, "sampling_rate": 16000})["text"].strip()
print("REF", who, round(len(y) / 16000, 1), "s:", ref_text, flush=True)
from voxcpm import VoxCPM
t0 = time.time()
model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device="cpu", optimize=False)
print("LOADED", round(time.time() - t0, 1), "s", flush=True)
report = {"who": who, "reference": ref, "reference_text": ref_text, "takes": []}
for feeling, line in LINES.items():
    for mode in ("plain", "directed"):
        text = line if mode == "plain" else "(%s)%s" % (DIRECTION[feeling], line)
        t0 = time.time()
        if mode == "plain":
            wav = model.generate(text=text, prompt_wav_path=refwav, prompt_text=ref_text, reference_wav_path=refwav)
        else:
            wav = model.generate(text=text, reference_wav_path=refwav)
        secs = time.time() - t0
        osr = getattr(model, "sample_rate", None) or getattr(getattr(model, "tts_model", None), "sample_rate", 48000)
        f = OUT + "/%s-%s-%s.wav" % (who, feeling, mode)
        sf.write(f, np.asarray(wav, dtype="float32"), osr)
        dur = len(wav) / osr
        print("TAKE", who, feeling, mode, "%.1f s audio in %.1f s" % (dur, secs), flush=True)
        report["takes"].append({"feeling": feeling, "mode": mode, "file": f, "text": text, "audio_s": round(dur, 2), "compute_s": round(secs, 1)})
json.dump(report, open(OUT + "/%s-report.json" % who, "w", encoding="utf-8"), indent=1)
print("DONE", who)
