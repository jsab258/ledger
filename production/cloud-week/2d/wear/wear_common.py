"""wear_common.py: what the wear mask maker and its check share (unit 4.5, cloud week 42).

Loads the wear target (production/cloud-week/targets/wear/target.json), its drawing module (target_drawing.py: each kind's shape envelope, in millimetres, from target.json alone) and its
reader (self_check.py: `measure`, `run_mask_check`, the composition functions and the deliberately wrong masks). Nothing here draws a mask.
"""
import hashlib
import importlib.util
import json
import sys
import zlib
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TDIR = ROOT / "production" / "cloud-week" / "targets" / "wear"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def load_target():
    """(tj, draw, scw): the target's json, its drawing module and its reader (self_check.py), loaded under their own names."""
    tj = json.loads((TDIR / "target.json").read_text(encoding="utf-8"))
    draw = _load("wear_target_drawing", TDIR / "target_drawing.py")
    scw = _load("wear_self_check", TDIR / "self_check.py")
    return tj, draw, scw


def rng_for(seed, *parts):
    return np.random.default_rng(zlib.crc32(("%s/%s" % (seed, "/".join(str(p) for p in parts))).encode()) & 0xFFFFFFFF)


def wrap_mode(k):
    """How a kind's mask repeats: 'xy' (a seamless square tile), 'x' (a tile along the wall) or False (a stamp), by its own `mask.origin` text, as the target's part D reads it."""
    org = k["mask"]["origin"]
    return "xy" if "seamless" in org else "x" if "tile" in org else False


def pix_hash(arr):
    a = np.ascontiguousarray(arr)
    return hashlib.sha256(str(a.shape).encode() + str(a.dtype).encode() + a.tobytes()).hexdigest()


def noise_field(shape, scale_px, rng, wrap=False, octaves=2):
    """Smooth noise, zero mean, unit standard deviation; wrap=True: periodic in both axes (a seamless tile), 'x': periodic along x."""
    mode = ("wrap", "wrap") if wrap in (True, "xy") else ("reflect", "wrap") if wrap == "x" else ("reflect", "reflect")
    out = np.zeros(shape, np.float32)
    amp = 1.0
    for o in range(octaves):
        a = rng.standard_normal(shape).astype(np.float32)
        out += amp * ndi.gaussian_filter(a, max(0.8, scale_px / (2 ** o)), mode=mode)
        amp *= 0.6
    out -= out.mean()
    s = out.std()
    return out / s if s > 0 else out
