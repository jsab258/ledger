"""The kit master material's detail maps, made from the street's own surface photographs.

    python tools/props/make_kit_detail.py            # writes F:/LedgerTools/game-inputs/production/assets/kit-detail
    python tools/props/make_kit_detail.py --selftest

WHY, 21 October 2026: lamp post C, the first cloud kit piece in the street, rendered as a clean,
flat, pale block (three gate reviewers). The research note
production/research/aaa-street/KIT-MATERIALS-2026-10-21.md recommends world-aligned detail with
the authored colour in charge: a detail map high-passed to a mean of 0.5, stored without sRGB, and
applied as lerp(1, 2 x detail, intensity) (Epic's DetailTexturing asks for a high-passed map with
sRGB off, multiplied against the diffuse). No new fetched input: each map is cut from a CC0
ambientCG photograph the street already ships (ledger/Assets/StreamingAssets/CityPack, its
ATTRIBUTION.json and THIRD-PARTY.md).

EACH MAP, 512 square, tileable (every blur wraps round, so the tile still repeats):
  R  the photograph's luminance, high-passed (a 32-pixel wrap blur taken away), to a mean of 0.5
  G  its roughness map, high-passed the same way, to a mean of 0.5
  B  a broad grunge: the luminance's own low frequencies, stretched to 0..1, to break the edge of
     the dirt band at a piece's foot
and <name>_n.png, the photograph's normal map resized (tangent space, as the source).
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "ledger", "Assets", "StreamingAssets", "CityPack", "textures")
# OUT OF GIT (the push guard refuses pictures outside the previews): the maps are remade by this script
# and imported once into /Game/Ledger/Kit (tools/ue/make_kit_materials.py), whose textures are committed.
OUT = os.environ.get("LEDGER_KIT_DETAIL", "F:/LedgerTools/game-inputs/production/assets/kit-detail")
SIZE = 512   # each imported texture stays under the push guard's 1 MB
# detail name: the street photograph it is cut from (square sources only, so one size fits all axes)
DETAILS = {
    "concrete": "concrete_b",   # ambientCG Concrete042A
    "stone": "kerb",            # ambientCG Rock048
    "metal": "metal",           # ambientCG Metal005
    "brick": "brick_red_b",     # the street's second red brick
}
HIGH_PASS_PX = 32
GRUNGE_PX = 48


def _wrap_blur(a, px):
    import numpy as np
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(a, sigma=px / 2.0, mode="wrap") if a.ndim == 2 else np.stack(
        [gaussian_filter(a[..., c], sigma=px / 2.0, mode="wrap") for c in range(a.shape[2])], -1)


def _lin(srgb):
    import numpy as np
    return np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)


def _high_pass(a, px, spread=0.18):
    """a (2-D, 0..1) minus its wrap blur, scaled so its 1st..99th percentile spans +-spread
    about 0.5 (the multiply then moves the authored colour by at most about a third)."""
    import numpy as np
    d = a - _wrap_blur(a, px)
    lo, hi = np.percentile(d, [1, 99])
    s = max(abs(lo), abs(hi), 1e-6)
    return np.clip(0.5 + d / s * spread, 0.0, 1.0)


def make(name, src, out_dir=OUT, size=SIZE):
    import numpy as np
    from PIL import Image
    alb = Image.open(os.path.join(SRC, src + ".jpg")).convert("RGB").resize((size, size), Image.LANCZOS)
    rough = Image.open(os.path.join(SRC, src + "_r.jpg")).convert("L").resize((size, size), Image.LANCZOS)
    nrm = Image.open(os.path.join(SRC, src + "_n.jpg")).convert("RGB").resize((size, size), Image.LANCZOS)
    a = _lin(np.asarray(alb, dtype=np.float64) / 255.0)
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    r = _high_pass(lum, HIGH_PASS_PX)
    g = _high_pass(np.asarray(rough, dtype=np.float64) / 255.0, HIGH_PASS_PX)
    low = _wrap_blur(lum, GRUNGE_PX)
    lo, hi = np.percentile(low, [2, 98])
    b = np.clip((low - lo) / max(hi - lo, 1e-6), 0.0, 1.0)
    rgb = (np.stack([r, g, b], -1) * 255.0 + 0.5).astype(np.uint8)
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, name + "_detail.png")
    Image.fromarray(rgb, "RGB").save(p, optimize=True)
    pn = os.path.join(out_dir, name + "_n.png")
    nrm.save(pn, optimize=True)
    return {"name": name, "from": src, "detail": p.replace(os.sep, "/"),
            "normal": pn.replace(os.sep, "/"),
            "meanR": round(float(r.mean()), 3), "meanG": round(float(g.mean()), 3),
            "bytes": os.path.getsize(p) + os.path.getsize(pn)}


def make_streaks(out_dir=OUT, size=SIZE, seed=1990, count=70):
    """THE RAIN STREAKS (21 October 2026, his ruling: the lamp columns "weathered and a shade
    darker"): a tileable map of vertical runs, drawn here from numbers alone (no photograph): each
    run starts at a random height, is 2 to 9 px wide, fades as it falls and wanders a little; the
    master material stretches it tall on vertical faces only. R carries the runs (0 clean, 1 full)."""
    import numpy as np
    from PIL import Image
    rng = np.random.default_rng(seed)
    a = np.zeros((size, size))
    ys = np.arange(size)
    for _ in range(count):
        x0 = rng.uniform(0, size)
        top = rng.uniform(0, size)
        length = rng.uniform(0.25, 0.9) * size
        width = rng.uniform(2.0, 9.0)
        strength = rng.uniform(0.35, 1.0)
        wander = rng.uniform(1.0, 6.0) * np.sin(ys / rng.uniform(30, 90) + rng.uniform(0, 6.3))
        d = (ys - top) % size                     # distance fallen below the run's top, wrapped
        fall = np.where(d < length, np.clip(1.0 - d / length, 0.0, 1.0) ** 0.6, 0.0) * strength
        for x in range(size):
            dx = np.abs(((x - (x0 + wander)) + size / 2) % size - size / 2)
            a[:, x] = np.maximum(a[:, x], fall * np.clip(1.0 - dx / width, 0.0, 1.0))
    a = _wrap_blur(a, 1.5)
    a = np.clip(a / max(a.max(), 1e-6), 0.0, 1.0)
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, "streaks_detail.png")
    rgb = (np.stack([a, a, a], -1) * 255.0 + 0.5).astype(np.uint8)
    Image.fromarray(rgb, "RGB").save(p, optimize=True)
    return {"name": "streaks", "from": "drawn (seed %d, %d runs)" % (seed, count), "detail": p.replace(os.sep, "/"),
            "meanR": round(float(a.mean()), 3), "bytes": os.path.getsize(p)}


def main():
    rows = [make(n, s) for n, s in DETAILS.items()]
    rows.append(make_streaks())
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"what": "the kit master material's detail maps (tools/props/make_kit_detail.py), cut from the "
                           "street's own CC0 ambientCG photographs in ledger/Assets/StreamingAssets/CityPack",
                   "size": SIZE, "high_pass_px": HIGH_PASS_PX, "grunge_px": GRUNGE_PX, "maps": rows}, f, indent=1)
    for r in rows:
        print("kitDetail %s from=%s meanR=%.3f bytes=%d" % (r["name"], r["from"], r["meanR"], r["bytes"]))
    return 0


def selftest():
    import numpy as np
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_kit_detail selftest FAIL " + name)
    rng = np.random.default_rng(1)
    a = rng.random((64, 64))
    h = _high_pass(a, 8)
    check("a high pass sits at a mean of 0.5", abs(h.mean() - 0.5) < 0.02)
    check("a high pass stays inside 0..1", h.min() >= 0.0 and h.max() <= 1.0)
    flat = np.full((64, 64), 0.3)
    check("a flat picture high-passes to a flat 0.5", np.allclose(_high_pass(flat, 8), 0.5))
    check("every source photograph is in the shipped pack", all(os.path.exists(os.path.join(SRC, s + ".jpg"))
                                                               for s in DETAILS.values()))
    import tempfile
    r = make_streaks(tempfile.mkdtemp(), size=64, count=8)
    check("the streak map is drawn and mostly clean between runs", 0.0 < r["meanR"] < 0.5)
    print("make_kit_detail selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
