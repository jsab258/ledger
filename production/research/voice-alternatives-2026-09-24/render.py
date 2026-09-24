"""Each character's line, spoken by Nano in each candidate voice, cloned from
that speaker's reference clip (the cast clip for the current voice). Nano's
DirectML patches are the ones from ../nano-listening-test/nano_card_timing.py.
Runs on the processor: on the card, learning a new voice aborts (see below).

    NANO_PKG=... NANO_WEIGHTS=... env-dml/python render.py <repo> <voicedir>
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
repo, vdir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
page = json.loads((pathlib.Path(__file__).parent / "page.json").read_text(encoding="utf-8"))
from chatterbox.tts_turbo import ChatterboxTurboTTS
import soundfile as sf

def load(dev):
    m = ChatterboxTurboTTS.from_local(NANO_WEIGHTS, dev, nano=True)
    if dev != "cpu":
        # THE VOCODER STAYS ON THE CPU, as in nano_card_timing.py: DirectML
        # has no complex numbers, and the vocoder uses them.
        m.s3gen.to("cpu")
        inf = m.s3gen.inference
        m.s3gen.inference = lambda speech_tokens, ref_dict, **k: inf(speech_tokens=speech_tokens.to("cpu"), ref_dict=ref_dict, **k)
    return m

def say(m, dev, text, ref):
    m.prepare_conditionals(str(ref))
    if dev != "cpu":
        m.conds.gen = {k: (v.to("cpu") if torch.is_tensor(v) else v) for k, v in m.conds.gen.items()}
    torch.manual_seed(20260924)
    return m.generate(text)

# ON THE PROCESSOR, 24 September: on the card, learning a new voice aborted
# the whole process in the voice encoder ("Invalid or unsupported data type
# ComplexFloat"), a fatal abort no try can catch. The processor does the same
# work a little slower; nothing here is timed.
dev = "cpu"
model, where = load(dev), "cpu"
for c in page["characters"]:
    for s in [c["current"]] + c["alternatives"]:
        ref = (repo / "game-design/picked-clips" / ("%s.%s.wav" % (c["id"], s))) if s == c["current"] else (vdir / ("ref_%s.wav" % s))
        t = time.time()
        try:
            wav = say(model, dev if where == "card" else "cpu", c["line"], ref)
        except Exception as e:
            if where != "card":
                raise
            print("voiceAlt card failed (%s: %s); the rest on the processor" % (type(e).__name__, str(e)[:120]), flush=True)
            model, where = load("cpu"), "cpu"
            wav = say(model, "cpu", c["line"], ref)
        a = wav.squeeze().detach().cpu().numpy()
        sf.write(vdir / ("line_%s_%s.wav" % (c["id"], s)), a, model.sr)
        print("voiceAlt %s %s on=%s work=%.1fs speech=%.1fs" % (c["id"], s, where, time.time() - t, len(a) / model.sr), flush=True)
