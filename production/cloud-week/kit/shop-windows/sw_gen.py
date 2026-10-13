"""Small shared pieces for the rooms and displays of the shops built after Rita's (batch A, 13 October): a mesh collector, lathed tins and jars with label strips, label and card pictures drawn by script
(fictional makers, hand lettering), and the placement helpers. Nothing here knows a shop: the layouts that use it are in sw_room_gen.py and sw_display_gen.py and read their numbers from target.json.

Every name drawn on a label is the project's own (a made-up maker and a plain word for the goods); none is a real firm (the target's brand blocklist is checked on every string by INV-05 / NEV-01).
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import bpy
import bmesh

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FONTS = os.path.join(REPO, "production", "fonts")


def font(name, size):
    """A project font by folder name: the first .ttf in production/fonts/<name>/."""
    d = os.path.join(FONTS, name)
    ttf = sorted(f for f in os.listdir(d) if f.lower().endswith((".ttf", ".otf")))
    return ImageFont.truetype(os.path.join(d, ttf[0]), size)


class GM:
    """A mesh collector: vertices, faces, a material index and (optionally) per-vertex UVs per face; one Blender object per collector."""

    def __init__(self):
        self.V, self.F, self.M, self.U = [], [], [], []

    def add(self, V, F, mi=0, uv=None):
        off = len(self.V)
        self.V.extend(tuple(float(c) for c in v) for v in V)
        for k, f in enumerate(F):
            self.F.append(tuple(off + int(i) for i in f))
            self.M.append(mi[k] if isinstance(mi, (list, tuple)) else mi)
            self.U.append(uv[k] if uv else None)

    def box(self, x0, x1, y0, y1, z0, z1, mi=0, uv_front=None, front="-y"):
        """A box; `uv_front` = (u0, v0, u1, v1) gives the face on `front` (-y toward the room's camera by default) the picture's rectangle (u to the right as seen from the front, v up)."""
        V = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        uv = [None] * 6
        if uv_front is not None:
            u0, v0, u1, v1 = uv_front
            if front == "-y":
                uv[2] = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
            elif front == "+x":              # seen from +x: left is -y... the face (2, 3, 7, 6) runs y1 -> y0 along... use the right face
                uv[3] = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
        self.add(V, F, mi, uv)

    def lathe(self, cx, cy, z0, profile, mi=0, n=16, label=None, mi_label=None, label_uv=None):
        """A solid of revolution about the vertical axis through (cx, cy): `profile` = [(radius, dz), ...] from the bottom up (a radius of 0 closes on the axis). `label` = (index range of the
        profile points whose side faces carry the label strip) with `label_uv` = (u0, v0, u1, v1): u wraps once round, v runs from the lower to the upper label edge."""
        rings = []
        V = []
        for r, dz in profile:
            if r < 1e-6:
                V.append((cx, cy, z0 + dz))
                rings.append(("pole", len(V) - 1))
            else:
                idx = []
                for k in range(n):
                    t = 2 * math.pi * k / n
                    V.append((cx + r * math.cos(t), cy + r * math.sin(t), z0 + dz))
                    idx.append(len(V) - 1)
                rings.append(("ring", idx))
        F, M, U = [], [], []
        for si, ((ka, a), (kb, b)) in enumerate(zip(rings[:-1], rings[1:])):
            lab = label is not None and label[0] <= si < label[1]
            for k in range(n):
                k2 = (k + 1) % n
                if ka == "ring" and kb == "ring":
                    # the face (a[k], a[k2], b[k2], b[k]) seen from outside runs counter-clockwise when the profile goes up
                    F.append((a[k], a[k2], b[k2], b[k]))
                elif ka == "pole":
                    F.append((a, b[k2], b[k]))
                else:
                    F.append((a[k], a[k2], b))
                M.append(mi_label if lab else mi)
                if lab and ka == "ring" and kb == "ring":
                    u0, v0, u1, v1 = label_uv
                    ua = u0 + (u1 - u0) * k / n
                    ub = u0 + (u1 - u0) * (k + 1) / n
                    sl = label[1] - label[0]
                    va = v0 + (v1 - v0) * (si - label[0]) / sl
                    vb = v0 + (v1 - v0) * (si - label[0] + 1) / sl
                    U.append([(ua, va), (ub, va), (ub, vb), (ua, vb)])
                else:
                    U.append(None)
        # a lathe's faces face outward when the profile runs bottom to top and the ring runs counter-clockwise seen from above: the bottom cap is closed by the pole or by a flat ring
        off = len(self.V)
        self.V.extend(V)
        for f, m, u in zip(F, M, U):
            self.F.append(tuple(off + i for i in f))
            self.M.append(m)
            self.U.append(u)

    def cylinder(self, cx, cy, z0, z1, r, mi=0, n=16):
        self.lathe(cx, cy, z0, [(0.0, 0.0), (r, 0.0), (r, z1 - z0), (0.0, z1 - z0)], mi, n)

    def torus(self, c, R, r, mi=0, axis="z", nm=12, nn=5):
        V, F = [], []
        for i in range(nm):
            a = 2 * math.pi * i / nm
            for j in range(nn):
                b = 2 * math.pi * j / nn
                rho = R + r * math.cos(b)
                p = (rho * math.cos(a), rho * math.sin(a), r * math.sin(b))
                if axis == "y":
                    p = (p[0], p[2], p[1])
                elif axis == "x":
                    p = (p[2], p[0], p[1])
                V.append((c[0] + p[0], c[1] + p[1], c[2] + p[2]))
        for i in range(nm):
            for j in range(nn):
                i2, j2 = (i + 1) % nm, (j + 1) % nn
                F.append((i * nn + j, i2 * nn + j, i2 * nn + j2, i * nn + j2))
        self.add(V, F, mi)

    def rod(self, p0, p1, r, mi=0, n=8):
        a = np.array(p0, float)
        b = np.array(p1, float)
        ax = b - a
        L = np.linalg.norm(ax)
        ax /= L
        helper = np.array([0.0, 0.0, 1.0]) if abs(ax[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
        e1 = np.cross(ax, helper)
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(ax, e1)
        V = []
        for c in (a, b):
            for k in range(n):
                t = 2 * math.pi * k / n
                V.append(c + r * (math.cos(t) * e1 + math.sin(t) * e2))
        F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self.add(V, F, mi)

    def extents(self):
        a = np.array(self.V)
        return [float(a[:, 0].min()), float(a[:, 0].max()), float(a[:, 1].min()), float(a[:, 1].max()), float(a[:, 2].min()), float(a[:, 2].max())]

    def to_object(self, name, mats, scene, smooth=False):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.V, [], self.F)
        me.validate()
        for m in mats:
            me.materials.append(m)
        for p, mi in zip(me.polygons, self.M):
            p.material_index = mi
            p.use_smooth = smooth
        if any(u is not None for u in self.U):
            uvl = me.uv_layers.new(name="UVMap")
            for p, u in zip(me.polygons, self.U):
                for li, uv in zip(p.loop_indices, u or [(0.0, 0.0)] * len(p.loop_indices)):
                    uvl.data[li].uv = uv
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
        ob = bpy.data.objects.new(name, me)
        scene.collection.objects.link(ob)
        return ob


# ---------------------------------------------------------------------------------------------------------------------------------- pictures by script
def tin_labels(path):
    """The paint and oil tins' label strips (fictional makers; no real firm): a 1024 x 512 atlas of 4 columns x 4 rows of 256 x 128 strips, wrapping once round a tin. Returns {name: (u0, v0, u1, v1)}.
    v 0 is the BOTTOM of the picture (the strips are listed top row first)."""
    W, H = 1024, 512
    im = Image.new("RGB", (W, H), (200, 200, 200))
    d = ImageDraw.Draw(im)
    designs = [
        ("BRANTHAM", "GLOSS PAINT", "WHITE", (232, 228, 214), (120, 24, 24), (40, 40, 70)),
        ("BRANTHAM", "GLOSS PAINT", "BLACK", (36, 36, 40), (200, 170, 60), (230, 226, 212)),
        ("COLDWELL", "EMULSION", "MAGNOLIA", (236, 222, 184), (30, 60, 110), (30, 60, 110)),
        ("COLDWELL", "EMULSION", "BRILLIANT WHITE", (240, 240, 236), (30, 60, 110), (30, 60, 110)),
        ("HARTSIDE", "WHITE SPIRIT", "1 LITRE", (60, 90, 150), (240, 230, 210), (240, 230, 210)),
        ("HARTSIDE", "METAL PRIMER", "RED OXIDE", (150, 70, 50), (240, 230, 210), (240, 230, 210)),
        ("ELMSTEAD", "WOOD PRESERVER", "DARK OAK", (90, 56, 30), (230, 200, 120), (230, 200, 120)),
        ("ELMSTEAD", "WOOD STAIN", "TEAK", (160, 100, 50), (30, 24, 20), (30, 24, 20)),
        ("BRANTHAM", "UNDERCOAT", "WHITE", (222, 222, 214), (30, 100, 60), (30, 100, 60)),
        ("COLDWELL", "GARDEN PAINT", "GREEN", (40, 100, 60), (240, 236, 220), (240, 236, 220)),
        ("HARTSIDE", "PARAFFIN", "5 LITRES", (200, 190, 60), (30, 30, 30), (30, 30, 30)),
        ("ELMSTEAD", "BITUMEN PAINT", "BLACK", (40, 40, 42), (220, 200, 120), (220, 200, 120)),
        ("BRANTHAM", "GLOSS PAINT", "BRILLIANT RED", (170, 36, 30), (240, 236, 220), (240, 236, 220)),
        ("BRANTHAM", "GLOSS PAINT", "DARK GREEN", (30, 70, 50), (230, 210, 140), (230, 210, 140)),
        ("COLDWELL", "EMULSION", "PEACH", (232, 190, 160), (120, 40, 30), (120, 40, 30)),
        ("HARTSIDE", "THINNERS", "1 LITRE", (180, 180, 190), (30, 50, 100), (30, 50, 100)),
    ]
    f1, f2, f3 = font("alfa-slab-one", 40), font("oswald", 26), font("oswald", 22)
    out = {}
    for k, (maker, what, detail, bg, ink, ink2) in enumerate(designs):
        c, r = k % 4, k // 4
        x0, y0 = c * 256, r * 128
        d.rectangle([x0, y0, x0 + 255, y0 + 127], fill=bg)
        d.rectangle([x0, y0 + 6, x0 + 255, y0 + 12], fill=ink)
        d.rectangle([x0, y0 + 115, x0 + 255, y0 + 121], fill=ink)
        for txt, f, yy, col in ((maker, f1, 20, ink), (what, f2, 66, ink2), (detail, f3, 94, ink2)):
            # each strip repeats across two panels of the label (a tin shows its name from every side): the text drawn at 1/2 the width twice
            for rep in (0, 1):
                tw = d.textlength(txt, font=f)
                sc = min(1.0, 118.0 / max(tw, 1.0))
                tile = Image.new("RGBA", (int(tw) + 4, int(f.size * 1.4)), (0, 0, 0, 0))
                ImageDraw.Draw(tile).text((2, 0), txt, font=f, fill=col + (255,))
                tile = tile.resize((max(1, int(tile.width * sc)), tile.height), Image.LANCZOS)
                im.paste(tile, (x0 + rep * 128 + 64 - tile.width // 2, y0 + yy), tile)
        out[k] = (x0 / W, 1.0 - (y0 + 128) / H, (x0 + 256) / W, 1.0 - y0 / H)
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    im.save(path)
    return out


def card_atlas(path, texts, cols=4, tile=(256, 128), font_name="patrick-hand", bg=(236, 230, 210), ink=(40, 36, 60), size=44):
    """A picture of hand-lettered cards (one text each, centred on two lines at most). Returns {index: (u0, v0, u1, v1)} (v 0 at the bottom)."""
    rows = (len(texts) + cols - 1) // cols
    W, H = cols * tile[0], rows * tile[1]
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    f = font(font_name, size)
    out = {}
    rnd = random.Random(5)
    for k, txt in enumerate(texts):
        c, r = k % cols, k // cols
        x0, y0 = c * tile[0], r * tile[1]
        shade = tuple(int(b * rnd.uniform(0.94, 1.0)) for b in bg)
        d.rectangle([x0, y0, x0 + tile[0] - 1, y0 + tile[1] - 1], fill=shade, outline=tuple(int(v * 0.72) for v in shade))
        lines = txt.split("\n")
        lh = f.size * 1.15
        y = y0 + (tile[1] - lh * len(lines)) / 2.0
        for ln in lines:
            tw = d.textlength(ln, font=f)
            d.text((x0 + (tile[0] - tw) / 2.0 + rnd.uniform(-2, 2), y), ln, font=f, fill=ink)
            y += lh
        out[k] = (x0 / W, 1.0 - (y0 + tile[1]) / H, (x0 + tile[0]) / W, 1.0 - y0 / H)
    im.save(path)
    return out
