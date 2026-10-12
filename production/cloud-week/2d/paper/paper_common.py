"""paper_common.py: what the paper maker and its check share (unit 4.2, 4.3 and 4.4, cloud week 42).

Loads the posters, boards and plates target (production/cloud-week/targets/posters-boards-plates/target.json) and its reader (self_check.py,
glyphlib.py), puts the fonts where the reader looks for them, and holds the target's own ageing formulas, the noise helpers, the item's
colours and the tape tab and string-and-sucker geometry. Nothing here draws a picture.
"""
import hashlib
import json
import math
import os
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TARGET_DIR = ROOT / "production" / "cloud-week" / "targets" / "posters-boards-plates"
FONT_SRC = ROOT / "production" / "fonts"


def flat_font_dir(work):
    """The reader finds a font by its file's own name in one folder (PBP_FONTS) or by the target's path under production/fonts; two of the three fonts the
    target asked for sit in their own sub-folders here, so the maker copies every font file it needs into one flat folder and points the reader at it."""
    d = Path(work) / "_fonts"
    d.mkdir(parents=True, exist_ok=True)
    for p in FONT_SRC.rglob("*"):
        if p.suffix.lower() in (".ttf", ".otf"):
            tgt = d / p.name
            if not tgt.exists() or tgt.stat().st_size != p.stat().st_size:
                shutil.copy2(p, tgt)
    return d


def load_reader(work):
    """Import the target's reader with the fonts set; returns (self_check, glyphlib)."""
    os.environ["PBP_FONTS"] = str(flat_font_dir(work))
    if str(TARGET_DIR) not in sys.path:
        sys.path.insert(0, str(TARGET_DIR))
    import glyphlib as gl            # noqa: E402
    import self_check as sc          # noqa: E402
    return sc, gl


# ------------------------------------------------------------------------------------------ the target's own ageing formulas (make_target.py)
AGE = {"A": dict(t_days=3, grime=0.00, yellow=0.00), "B": dict(t_days=18, grime=0.05, yellow=0.20),
       "C": dict(t_days=70, grime=0.12, yellow=0.50), "D": dict(t_days=200, grime=0.22, yellow=1.00)}
GRIME = (62, 58, 52)
YELLOWED = (214, 200, 168)
CLASSES = ("A", "B", "C", "D")


def mix(a, b, t):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def rnd(c):
    return tuple(int(round(v)) for v in c)


class Palette(object):
    """Aged colours of stocks, inks and paints, by the target's formulas; checked against the target's own tables on construction."""

    def __init__(self, T):
        self.T = T
        P = T["palette"]
        self.stocks, self.inks, self.paints = P["stocks"], P["inks"], P["paints"]
        for k, s in self.stocks.items():
            for c in CLASSES:
                got = rnd(self.stock(k, c))
                assert max(abs(got[i] - s["aged"][c][i]) for i in range(3)) <= 1, (k, c, got, s["aged"][c])
        for k, s in self.paints.items():
            for c in ("B", "D"):
                got = rnd(self.paint(k, c))
                ref = s["aged"].get(c)
                if ref:
                    assert max(abs(got[i] - ref[i]) for i in range(3)) <= 1, (k, c, got, ref)

    def stock(self, key, cls, tau_scale=1.0):
        s, a = self.stocks[key], AGE[cls]
        rgb = tuple(s["fresh"])
        if s.get("fade_to") is not None and s.get("tau_days"):
            f = 1 - math.exp(-a["t_days"] / (s["tau_days"] * tau_scale))
            rgb = mix(rgb, s["fade_to"], f)
        rgb = mix(rgb, YELLOWED, 0.30 * a["yellow"])
        return mix(rgb, GRIME, a["grime"])

    def paint_rgb(self, rgb, cls):
        a = AGE[cls]
        return mix(mix(rgb, YELLOWED, 0.25 * a["yellow"]), GRIME, a["grime"] * 1.1)

    def paint(self, key, cls):
        return self.paint_rgb(self.paints[key]["fresh"], cls)

    def ink(self, key, stock, cls, tau_scale=1.0):
        if key == "paper":
            return self.stock(stock, cls, tau_scale)
        if key in self.paints and key not in self.inks:
            return self.paint(key, cls)
        ink, a = self.inks[key], AGE[cls]
        f = 1 - math.exp(-a["t_days"] / (ink["tau_days"] * tau_scale))
        base = mix(ink["fresh"], self.stock(stock, cls, tau_scale), f)
        return mix(base, GRIME, a["grime"] * 0.35)

    def ground(self, item, on, cls, tau_scale=1.0):
        """The colour behind a block (the target's ground_colours)."""
        if on is None or on == "stock":
            return self.stock(item["stock"], cls, tau_scale)
        kind, key = on.split(":", 1)
        if kind == "art":
            return self.paint_rgb(tuple(int(v) for v in key.split(",")), cls)
        if kind == "ink":
            return self.ink(key, item["stock"], cls, tau_scale)
        return self.paint(key, cls)


# ------------------------------------------------------------------------------------------ noise and geometry
def seed_of(*parts):
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "little")


def rng_for(base, *parts):
    return np.random.default_rng(seed_of(base, *parts))


def value_noise(shape, scale_px, rng, aniso=1.0, octaves=1):
    """Smooth noise in [0, 1], feature size scale_px (aniso > 1 stretches the features down the sheet: paste brush marks)."""
    h, w = shape
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        sx = max(1.0, scale_px / (2 ** o))
        sy = max(1.0, scale_px * aniso / (2 ** o))
        gh, gw = int(h / sy) + 3, int(w / sx) + 3
        g = rng.random((gh, gw)).astype(np.float32)
        im = Image.fromarray(g, mode="F").resize((int(round(gw * sx)), int(round(gh * sy))), Image.BICUBIC)
        a = np.asarray(im)[:h, :w]
        if a.shape != (h, w):
            a = np.pad(a, ((0, h - a.shape[0]), (0, w - a.shape[1])), mode="edge")
        out += amp * a
        tot += amp
        amp *= 0.5
    out /= tot
    lo, hi = np.percentile(out[::max(1, h // 200), ::max(1, w // 200)], [1, 99])
    return np.clip((out - lo) / max(1e-6, hi - lo), 0, 1)


def smooth(a, sigma):
    return ndi.gaussian_filter(a, sigma, mode="nearest") if sigma > 0 else a


def tape_polygon(centre_mm, ppm, H_mm, spec, flip_x=False, flip_y=False, W_mm=None):
    """Polygon (pixel coordinates, row 0 the top) of a tab of yellowed tape: length x width at angle_deg about its centre, the way the target's own card_picture draws it.
    flip_x and flip_y mirror the tab to the other corners of a sheet taped by four tabs."""
    cx, cy = centre_mm
    L, Wd, a = spec["length_mm"] * ppm, spec["width_mm"] * ppm, math.radians(spec["angle_deg"])
    pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        px, py = sx * L / 2, sy * Wd / 2
        x = px * math.cos(a) + py * math.sin(a)
        y = -px * math.sin(a) + py * math.cos(a)
        if flip_x:
            x = -x
        if flip_y:
            y = -y
        pts.append((cx * ppm + x, (H_mm - cy) * ppm + y))
    return pts


def lab_of(rgb):
    def s2l(c):
        c = c / 255.0
        return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    r, g_, b = [s2l(np.asarray(rgb)[..., i].astype(float)) for i in range(3)]
    x = (0.4124 * r + 0.3576 * g_ + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g_ + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g_ + 0.9505 * b) / 1.08883
    f = lambda t: np.where(t > 0.008856, np.cbrt(t), 7.787 * t + 16 / 116)
    fx, fy, fz = f(x), f(y), f(z)
    return np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], -1)


def dE76(a, b):
    return np.sqrt(((np.asarray(a, float) - np.asarray(b, float)) ** 2).sum(-1))


# ------------------------------------------------------------------------------------------ where an item's wear table and tabs differ from the target's (one home: the maker, the reader and the check read these)
WEAR_OVERRIDE = {
    ("P02", "A"): "glass_bill",          # the target hangs P02 in the cottage window (SF9) taped inside the glass: it is not a pasted bill there
    ("C01a", "B"): "glass_bill",         # the appeal hangs inside the empty unit's glass (SF2) by four tabs: no sleeve, beads or fog inside a window (the close review's finding 5)
    ("C02", "A"): "glass_two_tabs",      # C02 hangs inside the same glass by two tabs at its top corners: no beads, ties or fog (the close review's finding 5)
}
TAB_SCALE = {"P02": 1 / 0.585}           # P02 is shown at 0.585 of its size in the cottage window (SF9): its tabs are drawn 1/0.585 bigger so that they are the target's 38 x 16 mm on the glass


def wear_table(item, cls):
    return WEAR_OVERRIDE.get((item["id"], cls), item["wear"].get("table"))


def tab_layout(T, item, cls):
    """[(centre_mm (x from the left, y from the bottom), flip_x, flip_y, spec)]: every tab of yellowed tape the item carries in a class: the hand card's one tab at the top-left (its mirror cue),
    four tabs across the corners of a sheet of A4 or more inside glass, two across the top corners of C02."""
    fx = T["fixings"]
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    out = []
    mc = item.get("mirror_cue")
    if mc and mc.get("kind") == "tape":
        out.append((tuple(mc["tab_centre_mm"]), False, False, fx["tape_tab"]))
    table = wear_table(item, cls)
    rows = (False, True) if (table == "glass_bill" and W >= 200) else ((False,) if table == "glass_two_tabs" else ())
    if rows:
        k = TAB_SCALE.get(item["id"], 1.0)
        f4 = fx["four_tabs"]
        spec = dict(length_mm=f4["length_mm"] * k, width_mm=f4["width_mm"] * k, angle_deg=f4["angle_deg"], rgb=f4["rgb"], opacity=f4["opacity"])
        c = [v * k for v in fx["tape_tab"]["centre_in_mm"]]
        for right in (False, True):
            for bottom in rows:
                out.append(((W - c[0] if right else c[0], c[1] if bottom else H - c[1]), right, bottom, spec))
    return out
