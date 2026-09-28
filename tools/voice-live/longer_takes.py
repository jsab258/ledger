#!/usr/bin/env python3
"""Longer takes of the approved cast voices, for Pocket TTS to learn each voice from.

    F:/LedgerTools/pocket-tts/env/Scripts/python.exe tools/voice-live/longer_takes.py vctk OUTDIR
    F:/LedgerTools/parler-tts/env/Scripts/python.exe tools/voice-live/longer_takes.py sheila OUTDIR
    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/voice-live/longer_takes.py pick OUTDIR

WHY, 28 September (Jafar's list, item 6: "Pocket TTS again, from longer takes
of my approved voices, with the accent checked before I hear anything"). On
26 September Pocket learnt each voice from the game's ten-second clip and
drifted American or away from the approved voice in parts of lines. Cloning
research (production/research/live-speech-architecture) says a longer, cleaner
reference holds a voice better.

  vctk    Ron's approved voice is VCTK speaker p227 and Darren's p241 (CC BY 4.0,
          CSTR, University of Edinburgh). Twelve of each speaker's own
          recordings are read from the corpus's parquet files (the row group
          where the speaker begins, as production/research/voice-alternatives-
          2026-09-24/fetch.py does), trimmed of silence and joined with short
          pauses into about 25 seconds: OUTDIR/rocco.wav and OUTDIR/sam.wav.
  sheila  Sheila's approved voice D was designed with Parler-TTS mini v1 from a
          written description and seed 101 (production/casting/voice-key.json).
          Three more sentences are made the same way, same description and
          seed, and joined after her approved reference into about 25 to 30
          seconds: OUTDIR/lena.wav.
          CHECKED FIRST, 28 September: that take read American (1.00) though
          her reference reads English (0.97): the same seed on other words
          is not the same voice. So `sheila` now makes each sentence with
          several seeds into OUTDIR/sheila-cand/, and
  pick    (run in the chatterbox env, which has the accent classifier) keeps
          only the candidates that read English whole and in every 2.5 s
          window (tools/voice-live/accent_check.py), and joins them after her
          reference: OUTDIR/lena.wav.

Loudness is evened to -20 LUFS. Nothing here is heard by Jafar: the takes only
teach Pocket; what it says is checked for accent before any page.
"""
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
INV = ROOT / "production" / "research" / "voice-alternatives-2026-09-24" / "vctk-inventory.json"
SPEAKERS = {"rocco": "p227", "sam": "p241"}
SEEDS = [101, 102, 103, 104, 105]
SHEILA_MORE = [
    "I kept the ledgers for the whole row of shops, the chandler's and the fish market and the rest, and I never once lost a penny.",
    "You get to know a street when you've walked up it every morning for thirty years, who comes early and who never pays on time.",
    "If you want my opinion, and I doubt you do, you'd leave well alone and let the police do what they're paid for.",
]


def even(data, sr):
    import numpy as np
    import pyloudnorm
    meter = pyloudnorm.Meter(sr)
    y = pyloudnorm.normalize.loudness(data, meter.integrated_loudness(data), -20.0)
    peak = float(np.max(np.abs(y))) or 1.0
    return y * min(1.0, 0.89 / peak)


def trim(a, sr, top_db=35):
    import numpy as np
    frame = int(sr * 0.02)
    if len(a) < frame * 3:
        return a
    rms = np.array([np.sqrt(np.mean(a[i:i + frame] ** 2)) for i in range(0, len(a) - frame, frame)])
    loud = np.where(20 * np.log10(rms + 1e-9) > 20 * np.log10(rms.max() + 1e-9) - top_db)[0]
    if len(loud) == 0:
        return a
    return a[max(0, loud[0] * frame - frame): min(len(a), (loud[-1] + 2) * frame)]


def join(pieces, sr, gap=0.35):
    import numpy as np
    out = []
    for p in pieces:
        out += [p, np.zeros(int(sr * gap), dtype=np.float32)]
    return np.concatenate(out[:-1]).astype("float32")


def vctk(out):
    import numpy as np
    import fsspec
    import huggingface_hub as hub
    import pyarrow.parquet as pq
    import soundfile as sf
    inv = json.loads(INV.read_text(encoding="utf-8"))
    fs = fsspec.filesystem("http")
    report = {}
    for who, spk in SPEAKERS.items():
        f, i = inv["first_row_group"][spk]
        u = hub.hf_hub_url("CSTR-Edinburgh/vctk", f, repo_type="dataset", revision="refs/convert/parquet")
        pf = pq.ParquetFile(fs.open(u, block_size=1 << 20, cache_type="none"))
        rows = []
        for g in (i, i + 1):
            if g >= pf.metadata.num_row_groups or len(rows) >= 12:
                break
            rows += [r for r in pf.read_row_group(g, columns=["speaker_id", "audio", "text", "text_id"]).to_pylist()
                     if str(r["speaker_id"]) == spk]
        pieces, sr, used = [], None, []
        for r in rows:
            a, s = sf.read(io.BytesIO(r["audio"]["bytes"]), dtype="float32")
            a = a if a.ndim == 1 else a.mean(axis=1)
            sr = sr or s
            if s != sr:
                continue
            a = trim(a, s)
            if len(a) / s < 1.2:          # a word or two teaches little
                continue
            pieces.append(a)
            used.append(r["text_id"])
            if sum(len(p) for p in pieces) / sr >= 25.0:
                break
        data = even(join(pieces, sr), sr)
        sf.write(str(out / (who + ".wav")), data, sr, subtype="PCM_16")
        report[who] = {"speaker": spk, "recordings": used, "seconds": round(len(data) / sr, 1)}
        print(who, spk, len(used), "recordings", report[who]["seconds"], "s", flush=True)
    (out / "vctk-takes.json").write_text(json.dumps(report, indent=1), encoding="utf-8")


def sheila(out):
    import numpy as np
    import soundfile as sf
    import torch
    from parler_tts import ParlerTTSForConditionalGeneration
    from transformers import AutoTokenizer
    key = json.loads((ROOT / "production" / "casting" / "voice-key.json").read_text(encoding="utf-8"))
    d = (key.get("characters") or key)["sheila-dunn"]["letters"]["D"]
    model = ParlerTTSForConditionalGeneration.from_pretrained(d["model"])
    tok = AutoTokenizer.from_pretrained(d["model"])
    sr = model.config.sampling_rate
    ref, rsr = sf.read(str(ROOT / d["reference_file"]), dtype="float32")
    ref = ref if ref.ndim == 1 else ref.mean(axis=1)
    if rsr != sr:
        import librosa
        ref = librosa.resample(ref, orig_sr=rsr, target_sr=sr)
    cand = out / "sheila-cand"
    cand.mkdir(exist_ok=True)
    sf.write(str(cand / "reference.wav"), trim(ref, sr), sr, subtype="PCM_16")
    desc = tok(d["description"], return_tensors="pt").input_ids
    for k, line in enumerate(SHEILA_MORE):
        for seed in SEEDS:
            torch.manual_seed(seed)
            gen = model.generate(input_ids=desc, prompt_input_ids=tok(line, return_tensors="pt").input_ids)
            a = gen.cpu().numpy().squeeze().astype("float32")
            sf.write(str(cand / ("line%d-seed%d.wav" % (k + 1, seed))), trim(a, sr), sr, subtype="PCM_16")
            print("sheila line", k + 1, "seed", seed, round(len(a) / sr, 1), "s", flush=True)
    (cand / "made.json").write_text(json.dumps({"description": d["description"], "seeds": SEEDS, "reference": d["reference_file"],
                                                "lines": SHEILA_MORE}, indent=1), encoding="utf-8")


def english_throughout(path):
    """The accent verdict of a file whole and of every 2.5 s window (1.25 s hop): (all pass, worst American share)."""
    import os
    import tempfile
    import librosa
    import soundfile as sf
    sys.path.insert(0, str(ROOT / "tools" / "voice-live"))
    import accent_check as ac
    y, sr = librosa.load(path, sr=16000)
    tmp = os.path.join(tempfile.mkdtemp(), "w.wav")
    verdicts = [ac.verdict(ac.scores(path))]
    for s in range(0, max(1, len(y) - int(2.5 * sr) + 1), int(1.25 * sr)):
        sf.write(tmp, y[s:s + int(2.5 * sr)], sr)
        verdicts.append(ac.verdict(ac.scores(tmp)))
    return all(v == "PASS" for v, _, _ in verdicts), max(am for _, _, am in verdicts)


def pick(out):
    import soundfile as sf
    cand = out / "sheila-cand"
    ref, sr = sf.read(str(cand / "reference.wav"), dtype="float32")
    pieces, used, report = [ref], [], {}
    for k in range(1, len(SHEILA_MORE) + 1):
        best = None
        for seed in SEEDS:
            f = cand / ("line%d-seed%d.wav" % (k, seed))
            if not f.exists():
                continue
            ok, am = english_throughout(str(f))
            report[f.name] = {"english": ok, "american": round(am, 3)}
            print(f.name, "english throughout" if ok else "not", "american %.3f" % am, flush=True)
            if ok and (best is None or am < best[1]):
                best = (f, am)
        if best:
            a, _ = sf.read(str(best[0]), dtype="float32")
            pieces.append(a)
            used.append(best[0].name)
    data = even(join(pieces, sr), sr)
    sf.write(str(out / "lena.wav"), data, sr, subtype="PCM_16")
    ok, am = english_throughout(str(out / "lena.wav"))
    (out / "sheila-takes.json").write_text(json.dumps({"used": used, "candidates": report, "seconds": round(len(data) / sr, 1),
                                                       "joinedEnglishThroughout": ok, "joinedAmerican": round(am, 3)}, indent=1), encoding="utf-8")
    print("lena", round(len(data) / sr, 1), "s, used", used, "english throughout" if ok else "NOT english throughout", "american %.3f" % am)


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    {"vctk": vctk, "sheila": sheila, "pick": pick}[sys.argv[1]](out)
