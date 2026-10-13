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

    def box(self, x0, x1, y0, y1, z0, z1, mi=0, uv_front=None, front="-y", uv_other=None):
        """A box; `uv_front` = (u0, v0, u1, v1) gives the face on `front` (-y toward the room's camera by default) the picture's rectangle (u to the right as seen from the front, v up)."""
        V = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        uv = [None] * 6
        if uv_front is not None:
            u0, v0, u1, v1 = uv_front
            if front == "-y":
                uv[2] = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
            elif front == "+x":              # seen from +x (a card on the LEFT wall, facing the room): u runs along +y
                uv[3] = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
            elif front == "-x":              # seen from -x (a card on the RIGHT wall): u runs along -y
                uv[5] = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
        if uv_other is not None:             # every other face takes one point of the picture (a plain colour), not the corner
            uo = [(uv_other[0], uv_other[1])] * 4
            uv = [u if u is not None else uo for u in uv]
        self.add(V, F, mi, uv)

    def sheet(self, c, w, h, t, tilt=0.0, yaw=0.0, mi=0, uv=None, uv_other=None, roll=0.0):
        """A thin box w wide (x), h tall (z), t thick (y) centred at c, the face on -y carrying `uv`; leaned `tilt` degrees (the top toward +y, away from the camera), then `roll` about its own y, then turned `yaw` about the vertical."""
        hx, hy, hz = w / 2.0, t / 2.0, h / 2.0
        V0 = [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz), (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]
        ta, ra, ya = math.radians(tilt), math.radians(roll), math.radians(yaw)
        V = []
        for x, y, z in V0:
            x, z = x * math.cos(ra) - z * math.sin(ra), x * math.sin(ra) + z * math.cos(ra)         # roll about y
            y, z = y * math.cos(ta) - z * math.sin(ta), y * math.sin(ta) + z * math.cos(ta)         # tilt about x: the top (z > 0) goes toward +y
            x, y = x * math.cos(ya) - y * math.sin(ya), x * math.sin(ya) + y * math.cos(ya)         # yaw about z
            V.append((c[0] + x, c[1] + y, c[2] + z))
        F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        uvs = [None] * 6
        if uv is not None:
            u0, v0, u1, v1 = uv
            uvs[2] = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
        if uv_other is not None:
            uo = [(uv_other[0], uv_other[1])] * 4
            uvs = [u if u is not None else uo for u in uvs]
        self.add(V, F, mi, uvs)

    def band(self, cx, cy, z0, z1, r, a0, a1, mi=0, uv=None, n=8):
        """A curved strip (a label on a jar): from angle a0 to a1 (degrees, 0 = toward -y, the camera; + toward +x), radius r about (cx, cy), z0 to z1; `uv` = (u0, v0, u1, v1) for the strip."""
        V, F, U = [], [], []
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            x, y = cx + r * math.sin(a), cy - r * math.cos(a)
            V.append((x, y, z0))
            V.append((x, y, z1))
        for i in range(n):
            k = 2 * i
            F.append((k, k + 2, k + 3, k + 1))
            if uv:
                u0, v0, u1, v1 = uv
                ua, ub = u0 + (u1 - u0) * i / n, u0 + (u1 - u0) * (i + 1) / n
                U.append([(ua, v0), (ub, v0), (ub, v1), (ua, v1)])
            else:
                U.append(None)
        self.add(V, F, mi, U)

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


# ---------------------------------------------------------------------------------------------------------------------------------- the newsagent's printed things (13 Oct, batch A)
# Every title, headline and name below is the project's own; none is a real paper, magazine, card maker or tobacco brand, and nobody is drawn (objects and landscapes only). The strings are
# kept in TEXTS so that the checks (INV-05, NEV-01) read exactly what is printed.
TEXTS = []

MAGAZINE_TITLES = [
    ("GARDEN LOG", "Spring bulbs, pruning roses, a greenhouse in a weekend", "garden"),
    ("THE ANGLER'S WEEK", "Spinning for pike; river reports; new rods tried", "river"),
    ("MODEL RAILWAY NEWS", "A branch line in OO gauge; scenery in a day", "train"),
    ("WEEKEND COOK", "Seasonal suppers, bread and puddings, a roast guide", "teapot"),
    ("MOTOR WORLD", "Used cars tested; the roads of the west coast", "car"),
    ("YACHT AND DINGHY", "The autumn regattas; refitting a small cruiser", "boat"),
    ("HOME & HEARTH", "Decorating on a budget; a colour guide for halls", "house"),
    ("THE WALKER", "Ten coastal paths; boots reviewed; maps and routes", "hills"),
    ("STAMP CORNER", "New issues; the 1d black; collecting by country", "stamp"),
    ("CRAFT & MAKING", "Knitting, quilting and woodwork patterns inside", "yarn"),
    ("COUNTRY DIARY", "Hedgerows in autumn; birds of the estuary", "bird"),
    ("PHOTO MONTHLY", "Cameras compared; landscapes in black and white", "camera"),
    ("RADIO AND HI-FI", "Receivers tested; building a cassette deck", "radio"),
    ("PUZZLE BOOK", "Crosswords, wordsearch and logic puzzles", "grid"),
    ("THE GARDENER'S YEAR", "A month by month planting calendar", "flower"),
    ("COAST & SEA", "Lighthouses of the west; the working harbour", "lighthouse"),
]
PAPER_NAMES = [("THE MERIDIAN HERALD", "COUNCIL APPROVES NEW BRIDGE", "Work to begin on the river crossing in the spring"),
               ("MERIDIAN EVENING NEWS", "HARBOUR REPAIRS TO BEGIN", "Quay wall closed for six weeks, ferry times change"),
               ("WEST COAST DAILY", "RAIN FORECAST FOR THE WEEKEND", "Gales expected on the coast, bridge open"),
               ("THE QUAYSIDE MAIL", "TRAWLER BACK IN PORT", "Crew safe after engine failure off the point"),
               ("MERIDIAN MORNING STAR", "BUS FARES TO RISE IN MAY", "Operator blames fuel costs; passengers protest"),
               ("THE WEST COUNTRY CHRONICLE", "NEW LIBRARY OPENS ON FRIDAY", "Reading rooms and a lending section for all")]
CARD_WORDS = ["BIRTHDAY GREETINGS", "BEST WISHES", "GET WELL SOON", "THANK YOU", "HAPPY ANNIVERSARY", "WITH SYMPATHY", "CONGRATULATIONS", "GOOD LUCK", "HAPPY RETIREMENT", "NEW HOME"]
POSTCARD_WORDS = ["GREETINGS FROM MERIDIAN", "THE HARBOUR AT DUSK", "MERIDIAN QUAY", "THE LIGHTHOUSE", "WEST COAST BEACH", "THE OLD MILL", "BRIDGE OVER THE RIVER", "MERIDIAN FROM THE HILL"]
PACK_BRANDS = [("HOLLINGWORTH", "KING SIZE FILTER", (150, 30, 36), (236, 226, 190), (220, 190, 90)),
               ("KESTRELL", "SMOOTH FILTER", (24, 70, 120), (236, 236, 232), (196, 40, 40)),
               ("MARSDEN", "MILD VIRGINIA", (232, 226, 206), (150, 30, 36), (40, 40, 60)),
               ("ALDERLEY", "GOLD FILTER", (196, 160, 70), (40, 30, 24), (120, 30, 30)),
               ("CASTLEMERE", "EXTRA MILD", (226, 232, 238), (24, 70, 120), (110, 120, 130)),
               ("SELWYN", "NAVY CUT", (30, 50, 90), (236, 226, 190), (200, 60, 50)),
               ("TOWNLEY", "KING SIZE", (40, 100, 60), (240, 236, 220), (200, 170, 70)),
               ("AVONLEA", "LIGHTS", (240, 238, 232), (30, 90, 110), (190, 190, 196)),
               ("BRANSTONE", "FULL FLAVOUR", (60, 40, 30), (230, 190, 100), (230, 190, 100)),
               ("RIVERMEAD", "MENTHOL FILTER", (30, 130, 120), (244, 244, 240), (120, 200, 190)),
               ("DEVEREUX", "SPECIAL FILTER", (110, 28, 60), (240, 226, 200), (220, 190, 120)),
               ("WYNDHAM", "IMPERIAL", (20, 20, 24), (210, 176, 80), (210, 176, 80))]
JAR_LABELS = [("HUMBUGS", "stripes", (240, 240, 236), (30, 24, 24)), ("PEAR DROPS", "dots", (210, 220, 130), (150, 170, 60)), ("MINT IMPERIALS", "dots", (244, 244, 240), (214, 220, 214)),
              ("FRUIT DROPS", "mix", (200, 60, 50), (230, 190, 60)), ("TOFFEES", "dots", (150, 96, 50), (96, 56, 28)), ("SHERBET LEMONS", "dots", (236, 210, 70), (200, 170, 40)),
              ("ACID DROPS", "mix", (230, 180, 60), (180, 60, 60)), ("BARLEY SUGAR", "dots", (226, 170, 70), (190, 120, 40)), ("CHERRY LIPS", "dots", (190, 40, 50), (130, 20, 30)),
              ("LIQUORICE MIXED", "mix", (30, 28, 30), (200, 80, 90))]


def _wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _picture(d, kind, box, rnd, pal):
    """An object or landscape drawn in a box (x0, y0, x1, y1); no figures."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sky, a, b, c = pal
    d.rectangle(box, fill=sky)
    ground = lambda col, fr=0.62: d.rectangle((x0, y0 + h * fr, x1, y1), fill=col)
    if kind in ("garden", "flower"):
        ground(a, 0.55)
        for i in range(7):
            cx = x0 + w * (0.1 + 0.13 * i + rnd.uniform(-0.02, 0.02))
            cy = y0 + h * rnd.uniform(0.35, 0.6)
            d.line((cx, cy, cx, y1), fill=(40, 110, 50), width=max(2, int(w * 0.015)))
            r = w * rnd.uniform(0.04, 0.07)
            col = rnd.choice([b, c, (240, 220, 80), (220, 90, 120)])
            for k in range(6):
                ang = k * math.pi / 3
                d.ellipse((cx + math.cos(ang) * r - r * 0.8, cy + math.sin(ang) * r - r * 0.8, cx + math.cos(ang) * r + r * 0.8, cy + math.sin(ang) * r + r * 0.8), fill=col)
            d.ellipse((cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5), fill=(240, 200, 60))
    elif kind in ("river", "boat", "lighthouse"):
        d.rectangle((x0, y0 + h * 0.6, x1, y1), fill=a)
        for i in range(9):
            yy = y0 + h * (0.64 + 0.04 * i)
            d.line((x0 + w * 0.05, yy, x1 - w * 0.05, yy), fill=b, width=2)
        if kind == "boat":
            d.polygon([(x0 + w * 0.3, y0 + h * 0.66), (x1 - w * 0.25, y0 + h * 0.66), (x1 - w * 0.33, y0 + h * 0.76), (x0 + w * 0.38, y0 + h * 0.76)], fill=c)
            d.line((x0 + w * 0.55, y0 + h * 0.66, x0 + w * 0.55, y0 + h * 0.18), fill=(80, 60, 40), width=3)
            d.polygon([(x0 + w * 0.57, y0 + h * 0.2), (x0 + w * 0.57, y0 + h * 0.62), (x0 + w * 0.82, y0 + h * 0.62)], fill=(244, 240, 230))
        elif kind == "lighthouse":
            d.polygon([(x0 + w * 0.42, y0 + h * 0.62), (x0 + w * 0.58, y0 + h * 0.62), (x0 + w * 0.54, y0 + h * 0.22), (x0 + w * 0.46, y0 + h * 0.22)], fill=(236, 232, 224))
            d.rectangle((x0 + w * 0.44, y0 + h * 0.38, x0 + w * 0.56, y0 + h * 0.46), fill=c)
            d.rectangle((x0 + w * 0.45, y0 + h * 0.14, x0 + w * 0.55, y0 + h * 0.22), fill=(60, 60, 70))
        else:
            d.line((x0 + w * 0.1, y0 + h * 0.5, x1 - w * 0.1, y0 + h * 0.5), fill=(90, 70, 50), width=3)
            d.line((x0 + w * 0.75, y0 + h * 0.5, x0 + w * 0.75, y0 + h * 0.3), fill=(90, 70, 50), width=2)
    elif kind in ("train", "car"):
        ground((90, 90, 96), 0.7)
        if kind == "train":
            d.rectangle((x0 + w * 0.1, y0 + h * 0.45, x0 + w * 0.9, y0 + h * 0.68), fill=c)
            d.rectangle((x0 + w * 0.64, y0 + h * 0.32, x0 + w * 0.9, y0 + h * 0.45), fill=b)
            d.rectangle((x0 + w * 0.8, y0 + h * 0.16, x0 + w * 0.86, y0 + h * 0.32), fill=(40, 40, 44))
            for i in range(5):
                d.ellipse((x0 + w * (0.14 + 0.15 * i), y0 + h * 0.62, x0 + w * (0.22 + 0.15 * i), y0 + h * 0.74), fill=(30, 30, 34))
        else:
            d.rounded_rectangle((x0 + w * 0.1, y0 + h * 0.5, x0 + w * 0.9, y0 + h * 0.68), radius=8, fill=c)
            d.polygon([(x0 + w * 0.26, y0 + h * 0.5), (x0 + w * 0.36, y0 + h * 0.36), (x0 + w * 0.66, y0 + h * 0.36), (x0 + w * 0.76, y0 + h * 0.5)], fill=c)
            for xx in (0.26, 0.72):
                d.ellipse((x0 + w * (xx - 0.07), y0 + h * 0.6, x0 + w * (xx + 0.07), y0 + h * 0.78), fill=(24, 24, 28))
    elif kind in ("house", "hills", "bird"):
        ground(a, 0.64)
        if kind == "house":
            d.rectangle((x0 + w * 0.28, y0 + h * 0.42, x0 + w * 0.72, y0 + h * 0.66), fill=b)
            d.polygon([(x0 + w * 0.24, y0 + h * 0.42), (x0 + w * 0.5, y0 + h * 0.2), (x0 + w * 0.76, y0 + h * 0.42)], fill=c)
            d.rectangle((x0 + w * 0.46, y0 + h * 0.52, x0 + w * 0.56, y0 + h * 0.66), fill=(80, 54, 40))
        elif kind == "hills":
            d.polygon([(x0, y0 + h * 0.64), (x0 + w * 0.3, y0 + h * 0.3), (x0 + w * 0.55, y0 + h * 0.64)], fill=b)
            d.polygon([(x0 + w * 0.4, y0 + h * 0.64), (x0 + w * 0.7, y0 + h * 0.24), (x1, y0 + h * 0.64)], fill=c)
        else:
            d.line((x0 + w * 0.05, y0 + h * 0.7, x1 - w * 0.05, y0 + h * 0.7), fill=(90, 70, 50), width=4)
            d.ellipse((x0 + w * 0.36, y0 + h * 0.48, x0 + w * 0.62, y0 + h * 0.7), fill=b)
            d.ellipse((x0 + w * 0.56, y0 + h * 0.42, x0 + w * 0.7, y0 + h * 0.54), fill=b)
            d.polygon([(x0 + w * 0.69, y0 + h * 0.47), (x0 + w * 0.78, y0 + h * 0.5), (x0 + w * 0.69, y0 + h * 0.52)], fill=(230, 170, 40))
    elif kind in ("teapot", "stamp", "yarn", "camera", "radio", "grid"):
        d.rectangle(box, fill=a)
        cx, cy = x0 + w * 0.5, y0 + h * 0.52
        if kind == "teapot":
            d.ellipse((cx - w * 0.22, cy - h * 0.16, cx + w * 0.22, cy + h * 0.22), fill=c)
            d.rectangle((cx - w * 0.1, cy - h * 0.24, cx + w * 0.1, cy - h * 0.14), fill=b)
            d.arc((cx + w * 0.18, cy - h * 0.1, cx + w * 0.36, cy + h * 0.14), 270, 90, fill=c, width=5)
            d.polygon([(cx - w * 0.22, cy - h * 0.02), (cx - w * 0.38, cy - h * 0.1), (cx - w * 0.2, cy + h * 0.06)], fill=c)
        elif kind == "stamp":
            d.rectangle((cx - w * 0.2, cy - h * 0.24, cx + w * 0.2, cy + h * 0.24), fill=(244, 240, 226), outline=c, width=4)
            d.rectangle((cx - w * 0.15, cy - h * 0.18, cx + w * 0.15, cy + h * 0.18), fill=b)
        elif kind == "yarn":
            for i, col in enumerate((b, c, (240, 220, 90))):
                d.ellipse((cx - w * (0.28 - 0.1 * i), cy - h * 0.14 + i * h * 0.06, cx - w * (0.28 - 0.1 * i) + w * 0.26, cy - h * 0.14 + i * h * 0.06 + w * 0.26), fill=col)
        elif kind == "camera":
            d.rounded_rectangle((cx - w * 0.28, cy - h * 0.12, cx + w * 0.28, cy + h * 0.16), radius=6, fill=(50, 50, 54))
            d.ellipse((cx - w * 0.12, cy - h * 0.12, cx + w * 0.12, cy + h * 0.12), fill=(120, 130, 140), outline=(20, 20, 24), width=4)
        elif kind == "radio":
            d.rounded_rectangle((cx - w * 0.3, cy - h * 0.14, cx + w * 0.3, cy + h * 0.16), radius=6, fill=b)
            d.ellipse((cx - w * 0.24, cy - h * 0.08, cx - w * 0.06, cy + h * 0.1), fill=(40, 40, 44))
            d.rectangle((cx + w * 0.02, cy - h * 0.06, cx + w * 0.24, cy + h * 0.02), fill=(220, 210, 160))
        else:
            for i in range(6):
                for j in range(6):
                    d.rectangle((x0 + w * (0.2 + 0.1 * i), y0 + h * (0.2 + 0.1 * j), x0 + w * (0.28 + 0.1 * i), y0 + h * (0.28 + 0.1 * j)), fill=(244, 244, 240) if (i + j + rnd.randrange(2)) % 3 else (30, 30, 34), outline=(60, 60, 64))
    else:
        ground(a)


def cover_atlas(path, kind="magazine", cols=4, rows=4, tile=(256, 340), seed=3):
    """Magazine covers (`kind` magazine: 16 invented titles, an object or landscape each) or newspapers (`kind` paper: front pages with an invented masthead and headline, no picture of a person) in one atlas.
    Returns {index: (u0, v0, u1, v1)} (v 0 at the bottom)."""
    rnd = random.Random(seed)
    W, H = cols * tile[0], rows * tile[1]
    im = Image.new("RGB", (W, H), (236, 232, 224))
    d = ImageDraw.Draw(im)
    out = {}
    n = cols * rows
    for k in range(n):
        c, r = k % cols, k // cols
        x0, y0 = c * tile[0], r * tile[1]
        if kind == "magazine":
            title, cl, art = MAGAZINE_TITLES[k % len(MAGAZINE_TITLES)]
            pal = rnd.choice([((220, 230, 238), (110, 150, 90), (200, 80, 60), (60, 90, 150)), ((238, 226, 190), (150, 170, 100), (190, 60, 50), (50, 80, 120)),
                              ((200, 220, 230), (70, 110, 140), (230, 190, 60), (170, 50, 60)), ((240, 214, 200), (160, 120, 90), (60, 100, 70), (200, 70, 80))])
            bg = rnd.choice([(244, 240, 228), (30, 40, 70), (150, 30, 40), (236, 232, 200), (28, 80, 60)])
            d.rectangle([x0, y0, x0 + tile[0] - 1, y0 + tile[1] - 1], fill=bg)
            fg = (30, 30, 34) if sum(bg) > 560 else (244, 240, 226)
            f1 = font("abril-fatface", 34 if len(title) < 15 else 25)
            lines = _wrap(d, title, f1, tile[0] - 24)
            yy = y0 + 12
            for ln in lines[:2]:
                tw = d.textlength(ln, font=f1)
                d.text((x0 + (tile[0] - tw) / 2, yy), ln, font=f1, fill=fg)
                yy += f1.size * 1.1
            _picture(d, art, (x0 + 14, yy + 6, x0 + tile[0] - 14, y0 + tile[1] - 92), rnd, pal)
            f2 = font("oswald", 15)
            yy = y0 + tile[1] - 84
            for ln in _wrap(d, cl, f2, tile[0] - 28)[:3]:
                d.text((x0 + 14, yy), ln, font=f2, fill=fg)
                yy += 19
            f3 = font("josefin-sans", 12)
            d.text((x0 + 14, y0 + tile[1] - 22), "£1.20   AUTUMN ISSUE", font=f3, fill=fg)
            TEXTS.extend([title, cl, "AUTUMN ISSUE"])
        else:
            name, head, sub = PAPER_NAMES[k % len(PAPER_NAMES)]
            d.rectangle([x0, y0, x0 + tile[0] - 1, y0 + tile[1] - 1], fill=rnd.choice([(238, 234, 222), (232, 228, 214), (240, 238, 230)]))
            f1 = font("old-standard-tt", 26 if len(name) < 20 else 20)
            lines = _wrap(d, name, f1, tile[0] - 20)
            yy = y0 + 12
            for ln in lines[:2]:
                tw = d.textlength(ln, font=f1)
                d.text((x0 + (tile[0] - tw) / 2, yy), ln, font=f1, fill=(24, 24, 28))
                yy += f1.size * 1.1
            d.line((x0 + 10, yy + 4, x0 + tile[0] - 10, yy + 4), fill=(24, 24, 28), width=3)
            f2 = font("alfa-slab-one", 30)
            yy += 14
            for ln in _wrap(d, head, f2, tile[0] - 20)[:3]:
                d.text((x0 + 10, yy), ln, font=f2, fill=(20, 20, 24))
                yy += f2.size * 1.05
            # a plain halftone picture of a landscape or an object (no person)
            pal = ((200, 204, 206), (130, 134, 136), (90, 94, 98), (60, 62, 66))
            _picture(d, rnd.choice(["hills", "boat", "house", "river"]), (x0 + 10, yy + 6, x0 + tile[0] - 10, yy + 6 + (tile[1] - (yy - y0) - 70)), rnd, pal)
            f3 = font("old-standard-tt", 13)
            yy2 = y0 + tile[1] - 56
            for ln in _wrap(d, sub, f3, tile[0] - 20)[:2]:
                d.text((x0 + 10, yy2), ln, font=f3, fill=(30, 30, 34))
                yy2 += 16
            for i in range(3):
                d.line((x0 + 10, yy2 + 4 + i * 5, x0 + tile[0] - 10, yy2 + 4 + i * 5), fill=(120, 120, 124), width=1)
            TEXTS.extend([name, head, sub])
        d.rectangle([x0, y0, x0 + tile[0] - 1, y0 + tile[1] - 1], outline=(110, 108, 100))
        out[k] = (x0 / W, 1.0 - (y0 + tile[1]) / H, (x0 + tile[0]) / W, 1.0 - y0 / H)
    im = im.filter(ImageFilter.GaussianBlur(0.4))
    im.save(path)
    return out


def card_art_atlas(path, words, cols=5, rows=4, tile=(180, 250), seed=5, postcard=False):
    """Greetings cards (portrait) or postcards (landscape, `postcard`): an invented view or flowers and a line of lettering. Returns {index: (u0, v0, u1, v1)}."""
    rnd = random.Random(seed)
    W, H = cols * tile[0], rows * tile[1]
    im = Image.new("RGB", (W, H), (240, 236, 226))
    d = ImageDraw.Draw(im)
    out = {}
    arts = ["garden", "flower", "boat", "lighthouse", "house", "hills", "river", "bird"]
    pals = [((226, 238, 244), (100, 150, 90), (220, 90, 80), (70, 110, 170)), ((244, 232, 200), (140, 170, 100), (200, 60, 60), (60, 90, 140)),
            ((206, 226, 236), (70, 120, 150), (240, 200, 70), (180, 60, 70)), ((246, 220, 214), (150, 130, 100), (60, 110, 70), (210, 80, 100))]
    for k in range(cols * rows):
        c, r = k % cols, k // cols
        x0, y0 = c * tile[0], r * tile[1]
        d.rectangle([x0, y0, x0 + tile[0] - 1, y0 + tile[1] - 1], fill=rnd.choice([(250, 248, 240), (246, 240, 226), (240, 244, 246)]))
        txt = words[k % len(words)]
        f = font("fraunces" if not postcard else "josefin-sans", 18 if not postcard else 15)
        pad = 10
        if postcard:
            _picture(d, arts[k % len(arts)], (x0 + pad, y0 + pad, x0 + tile[0] - pad, y0 + tile[1] - 40), rnd, pals[k % len(pals)])
            ty = y0 + tile[1] - 32
        else:
            _picture(d, arts[k % len(arts)], (x0 + pad, y0 + pad, x0 + tile[0] - pad, y0 + int(tile[1] * 0.68)), rnd, pals[k % len(pals)])
            ty = y0 + int(tile[1] * 0.72)
        for ln in _wrap(d, txt, f, tile[0] - 2 * pad)[:2]:
            tw = d.textlength(ln, font=f)
            d.text((x0 + (tile[0] - tw) / 2, ty), ln, font=f, fill=(60, 40, 60))
            ty += f.size * 1.2
        d.rectangle([x0, y0, x0 + tile[0] - 1, y0 + tile[1] - 1], outline=(150, 146, 136))
        TEXTS.append(txt)
        out[k] = (x0 / W, 1.0 - (y0 + tile[1]) / H, (x0 + tile[0]) / W, 1.0 - y0 / H)
    im.save(path)
    return out


def pack_atlas(path, seed=9):
    """The cigarette packs' fronts (fictional brands: the names are the project's own, none a real maker): 12 tiles of 150 x 260 in 4 columns x 3 rows; the first row of the tile is the top of the pack.
    Returns {index: (u0, v0, u1, v1)}."""
    rnd = random.Random(seed)
    tw, th = 150, 260
    W, H = 4 * tw, 3 * th
    im = Image.new("RGB", (W, H), (200, 200, 200))
    d = ImageDraw.Draw(im)
    out = {}
    for k, (brand, sub, bg, fg, accent) in enumerate(PACK_BRANDS):
        c, r = k % 4, k // 4
        x0, y0 = c * tw, r * th
        d.rectangle([x0, y0, x0 + tw - 1, y0 + th - 1], fill=bg)
        d.rectangle([x0, y0 + 8, x0 + tw - 1, y0 + 22], fill=accent)
        fs = 28
        f = font("alfa-slab-one", fs)
        while d.textlength(brand, font=f) > tw - 16 and fs > 10:
            fs -= 1
            f = font("alfa-slab-one", fs)
        t_w = d.textlength(brand, font=f)
        d.text((x0 + (tw - t_w) / 2, y0 + 50), brand, font=f, fill=fg)
        # a crest: a plain shield
        cx, cy = x0 + tw / 2, y0 + 118
        d.polygon([(cx - 26, cy - 24), (cx + 26, cy - 24), (cx + 26, cy + 8), (cx, cy + 34), (cx - 26, cy + 8)], fill=accent, outline=fg)
        d.line((cx, cy - 20, cx, cy + 26), fill=fg, width=2)
        d.line((cx - 22, cy - 6, cx + 22, cy - 6), fill=fg, width=2)
        f2 = font("oswald", 15)
        t2 = d.textlength(sub, font=f2)
        d.text((x0 + (tw - t2) / 2, y0 + 168), sub, font=f2, fill=fg)
        d.text((x0 + (tw - d.textlength("20 CIGARETTES", font=font("oswald", 11))) / 2, y0 + 192), "20 CIGARETTES", font=font("oswald", 11), fill=fg)
        d.rectangle([x0, y0 + th - 38, x0 + tw - 1, y0 + th - 1], fill=(20, 20, 22) if sum(bg) > 300 else (240, 238, 230))
        d.text((x0 + 10, y0 + th - 30), "HEALTH WARNING", font=font("oswald", 11), fill=(240, 238, 230) if sum(bg) > 300 else (20, 20, 22))
        out[k] = (x0 / W, 1.0 - (y0 + th) / H, (x0 + tw) / W, 1.0 - y0 / H)
        TEXTS.extend([brand, sub, "20 CIGARETTES", "HEALTH WARNING"])
    im.save(path)
    return out


def jar_atlas(path, seed=11):
    """The sweet jars: per jar one tile of 256 x 256: the top half is the contents' colour pattern (stripes, dots or a mix, tiled round the jar), the bottom half is the paper label. Returns {index: ((cu0, cv0, cu1, cv1), (lu0, lv0, lu1, lv1))}."""
    rnd = random.Random(seed)
    W, H = 5 * 256, 2 * 256
    im = Image.new("RGB", (W, H), (200, 200, 200))
    d = ImageDraw.Draw(im)
    out = {}
    for k, (name, pat, c1, c2) in enumerate(JAR_LABELS):
        c, r = k % 5, k // 5
        x0, y0 = c * 256, r * 256
        d.rectangle([x0, y0, x0 + 255, y0 + 160], fill=c1)
        if pat == "stripes":
            for i in range(-8, 20):
                d.polygon([(x0 + i * 22, y0 + 160), (x0 + i * 22 + 11, y0 + 160), (x0 + i * 22 + 11 + 40, y0), (x0 + i * 22 + 40, y0)], fill=c2)
        elif pat == "dots":
            for i in range(120):
                xx, yy = x0 + rnd.randrange(256), y0 + rnd.randrange(160)
                rr = rnd.randint(7, 12)
                d.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=rnd.choice([c1, c2, tuple(min(255, int(v * 1.1)) for v in c1)]), outline=tuple(int(v * 0.7) for v in c1))
        else:
            cols = [(200, 60, 50), (230, 190, 60), (60, 140, 70), (230, 130, 60), (200, 80, 110), (240, 240, 230)]
            for i in range(130):
                xx, yy = x0 + rnd.randrange(256), y0 + rnd.randrange(160)
                rr = rnd.randint(7, 12)
                d.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=rnd.choice(cols) if c1 != (30, 28, 30) else rnd.choice([(30, 28, 30), (200, 80, 90), (240, 240, 230), (30, 28, 30)]), outline=(60, 50, 40))
        d.rectangle([x0, y0 + 160, x0 + 255, y0 + 255], fill=(236, 228, 206))
        f = font("alfa-slab-one", 24)
        lines = _wrap(d, name, f, 220)
        yy = y0 + 172
        for ln in lines[:2]:
            tw = d.textlength(ln, font=f)
            d.text((x0 + (256 - tw) / 2, yy), ln, font=f, fill=(120, 30, 40))
            yy += 28
        d.rectangle([x0 + 8, y0 + 166, x0 + 247, y0 + 249], outline=(120, 30, 40), width=2)
        TEXTS.append(name)
        out[k] = ((x0 / W, 1.0 - (y0 + 160) / H, (x0 + 256) / W, 1.0 - y0 / H), (x0 / W, 1.0 - (y0 + 256) / H, (x0 + 256) / W, 1.0 - (y0 + 160) / H))
    im.save(path)
    return out
