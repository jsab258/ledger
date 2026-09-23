"""Nano on the card: the ten listening-test lines spoken in Nano's BUILT-IN voice
(no cast voice is recorded; Jafar's consent questions are open), on DirectML,
timed line by line. Nothing is written but the timing lines and a JSON summary.

    python nano_card_timing.py <repo> <summary.json> <label> [rounds]
"""
import json, os, sys, time, pathlib, types, importlib
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
NANO_PKG = os.environ.get("NANO_PKG", "")
NANO_WEIGHTS = os.environ.get("NANO_WEIGHTS", "")
if NANO_PKG:
    sys.path.insert(0, NANO_PKG)
_pr = types.ModuleType("pkg_resources")
_pr.resource_filename = lambda pkg, name: os.path.join(os.path.dirname(importlib.import_module(pkg).__file__), name)
sys.modules.setdefault("pkg_resources", _pr)
import torch
import torch_directml
# Nano's built-in voice (conds.pt) was saved on a CUDA card; for any device
# but cpu/mps from_local passes map_location=None and the load fails on a
# machine without CUDA. Loaded to the CPU first, then moved to the card.
_orig_load = torch.load
def _load_to_cpu(*a, **k):
    if k.get("map_location") is None:
        k["map_location"] = "cpu"
    return _orig_load(*a, **k)
torch.load = _load_to_cpu
# DirectML cannot slice an inference-mode tensor ("Cannot set version_counter
# for inference tensor"); Nano's generator is decorated with inference_mode,
# so it runs under no_grad instead, which is what inference_mode adds to.
class _NoGradMode(torch.no_grad):
    def __init__(self, mode=True):
        super().__init__()
torch.inference_mode = _NoGradMode
# DirectML refuses a concatenation that includes an empty tensor ("The
# parameter is incorrect"); Nano's conditioning joins three empty ones, which
# add nothing, so they are left out.
_orig_cat = torch.cat
def _cat(tensors, dim=0, **k):
    if "out" in k:
        return _orig_cat(tensors, dim, **k)
    ts = [t for t in tensors if t.numel() > 0]
    if not ts:
        return _orig_cat(tensors, dim)
    return ts[0] if len(ts) == 1 else _orig_cat(ts, dim)
torch.cat = _cat
repo, summary, label = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
rounds = int(sys.argv[4]) if len(sys.argv) > 4 else 1
dev = torch_directml.device()
from chatterbox.tts_turbo import ChatterboxTurboTTS
spec = json.loads((repo / "production/research/nano-listening-test/lines.json").read_text(encoding="utf-8"))
torch.manual_seed(20260924)
t0 = time.time()
model = ChatterboxTurboTTS.from_local(NANO_WEIGHTS, dev, nano=True)
# THE VOCODER STAYS ON THE CPU: DirectML has no complex numbers ("Invalid or
# unsupported data type ComplexFloat", a fatal abort), and the step that turns
# the model's sound tokens into a waveform uses them. The token model, which
# is most of the work, runs on the card.
model.s3gen.to("cpu")
model.conds.gen = {k: (v.to("cpu") if torch.is_tensor(v) else v) for k, v in model.conds.gen.items()}
_s3_inference = model.s3gen.inference
def _s3_on_cpu(speech_tokens, ref_dict, **k):
    return _s3_inference(speech_tokens=speech_tokens.to("cpu"), ref_dict=ref_dict, **k)
model.s3gen.inference = _s3_on_cpu
load_s = time.time() - t0
print("nanoCard loaded=%.1fs device=dml label=%s" % (load_s, label), flush=True)
# One warm line first, so the first timed line is not paying for kernels.
model.generate(spec["lines"][0]["nano"])
rows = []
start = time.time()
for r in range(rounds):
    for ln in spec["lines"]:
        t = time.time()
        wav = model.generate(ln["nano"])
        work = time.time() - t
        speech = wav.shape[-1] / model.sr
        rows.append({"id": ln["id"], "round": r, "work_s": round(work, 3), "speech_s": round(speech, 3),
                     "rtf": round(work / speech, 3), "at_s": round(time.time() - start, 1)})
        print("nanoCard label=%s id=%s work=%.2fs speech=%.2fs rtf=%.2f" % (label, ln["id"], work, speech, work / speech), flush=True)
work = sum(x["work_s"] for x in rows)
speech = sum(x["speech_s"] for x in rows)
rtfs = sorted(x["rtf"] for x in rows)
out = {"label": label, "device": "dml-tokens/cpu-vocoder", "voice": "nano-built-in (conds.pt), no cast voice", "load_s": round(load_s, 1),
       "lines": len(rows), "work_s": round(work, 2), "speech_s": round(speech, 2), "rtf_overall": round(work / speech, 3),
       "rtf_median": rtfs[len(rtfs) // 2], "rtf_worst": rtfs[-1], "rows": rows}
summary.write_text(json.dumps(out, indent=1), encoding="utf-8")
print("nanoCardSummary label=%s lines=%d rtfOverall=%.2f rtfMedian=%.2f rtfWorst=%.2f" % (label, len(rows), out["rtf_overall"], out["rtf_median"], out["rtf_worst"]), flush=True)
