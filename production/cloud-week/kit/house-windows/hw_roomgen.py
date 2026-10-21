"""The thirteen rooms behind the house windows, built by script in Blender (Cycles, CPU) to target.json section 7 and rendered to the game's rule: for each room three pictures (day, night_lit,
night_dark) at the target's size, with the JSON beside them.

`HRoom` is `hw_room.Room` (a copy, 14 October, of the shop kit's sw_room.Room: materials, model templates with the glass kept, placement, Cycles render) with a shell, forms, objects and lights driven by
the target's rooms. Nothing here is a shop's: the room's size, finishes, objects (class, stand-off, place), forms and lights come from target.json `rooms`.

Room frame (the recipe's): x across, 0 at the card's centre, +x the PICTURE's right; y back from the card (the front plane) to the back wall at D; z up from the floor. The camera stands on the centre line
d = W in front of the card and frames the card rectangle W x H exactly (horizontal field 2 atan(W / 2d) = 53.13 degrees).

Lessons applied from the shops' fresh reviews (14 October): the night wash is the window's own size, not the card's width (the top corners must not burn); every model keeps all its meshes (the glass kept as
a see-through material, not alpha-blended); every model is at scale 1.0 (never shrunk to fit); every piece rests on something or hangs from something (the floating-goods check reads placed.json); the framed
pictures are crops of CC0 photographs, one per placement.
"""
import json
import math
import os
import random
import re
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Vector, Matrix, Euler  # noqa: E402
import hw_t as T  # noqa: E402
import hw_assets as A  # noqa: E402
import hw_room as S  # noqa: E402
import hw_models as M  # noqa: E402

A.POLY = T.POLY
rgb8 = S.rgb8
STATES = ("day", "night_lit", "night_dark")
RENDER_ORDER = ("day", "night_dark", "night_lit")          # night_dark before night_lit: an empty room's night_lit is its night_dark
S.KEEP_BLEND["vintage_oil_lamp"] = ("flame",)        # the lamp's flame is a card with its own material: kept, and lit in night_lit only
WARM = (1.0, 0.714, 0.344)                          # the pendant's 2700 K tungsten, linear (target 7.1)
SODIUM = (1.0, 0.25, 0.0)                           # the game's lantern_linear_rgb (unreal-look.json), not the scene file's stale (1, 0.7055, 0)
TV_COOL = (0.62, 0.74, 1.0)
PAINT_WHITE = (0.70, 0.68, 0.62)


WASH_SIZE, WASH_RATIO = (1.8, 0.30), 0.14
FILL_SIZE = (1.6, 2.4)                              # the lit lounges' and bedrooms' fill light (metres across, deep): a soft room-wide area light under the ceiling's centre
ROLL_KNEE, ROLL_TOP = 0.60, 0.85       # linear: below the knee a pixel is as rendered; above it the largest channel eases toward 0.85 (sRGB 237) and never reaches it; the three channels scale together, so the hue stays tungsten


def roll_off(lin):
    """Roll the highlights off before the 8-bit write: scale all three channels together by m'/m, m the pixel's largest channel in scene-linear, m' = knee + (top - knee) x (1 - exp(-(m - knee) / (top - knee))) above the knee
    (the close review asked for 'over 0.85 scaled to 0.85'; this is the same ceiling reached smoothly, so no plateau: no channel of a lit picture reaches 250, PIC-13)."""
    m = lin.max(axis=2, keepdims=True)
    over = m > ROLL_KNEE
    m2 = np.where(over, ROLL_KNEE + (ROLL_TOP - ROLL_KNEE) * (1.0 - np.exp(-(m - ROLL_KNEE) / (ROLL_TOP - ROLL_KNEE))), m)
    return lin * (m2 / np.maximum(m, 1e-9))


def read_exr(path):
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    a = np.array(img.pixels[:], np.float32).reshape(h, w, img.channels)[..., :3]
    bpy.data.images.remove(img)
    return np.ascontiguousarray(a[::-1])               # Blender's rows run bottom to top


def write_rolled(lin_img, path):
    r = roll_off(np.maximum(lin_img, 0.0))
    s = np.where(r <= 0.0031308, r * 12.92, 1.055 * np.clip(r, 0, None) ** (1 / 2.4) - 0.055)
    Image.fromarray(np.clip(s * 255.0 + 0.5, 0, 255).astype(np.uint8)).save(path)


def lin_of(v):
    v = np.asarray(v, np.float32) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def tex_files(asset):
    d = os.path.join(A.POLY, asset, "1k", "textures")
    out = {}
    for f in sorted(os.listdir(d)):
        for k in ("diff", "arm", "nor_gl", "rough"):
            if "_%s_" % k in f and k not in out and "_clean" not in f:
                out[k] = os.path.join(d, f)
    return out


def tex_mean(asset):
    f = tex_files(asset)["diff"]
    a = np.asarray(Image.open(f).convert("RGB").resize((128, 128))).astype(np.float32)
    return lin_of(a).reshape(-1, 3).mean(axis=0)


class HRoom(S.Room):
    keep_glass = True
    shadow_trick = True

    def __init__(self, rid, work, seed=11):
        self.rid = rid
        self.R = T.room(rid)
        fam = T.families()[self.R["family"]]
        self.W, self.H, self.D = fam["w"], fam["h"], fam["d"]
        self.camd = fam["camd"]
        self.pix = tuple(self.R["picture_px"])
        self.work = work
        self.tex = os.path.join(work, "tex")
        os.makedirs(self.tex, exist_ok=True)
        self.rnd = random.Random(seed)
        self.placed = []
        self.fixtures = []
        self.templates = {}
        self.hand_base = {}
        self.mats = {}
        self.forms_rec = []
        self.notes = []
        self.print_log = []
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.sc = bpy.context.scene
        self.coll_t = bpy.data.collections.new("templates")
        self.sc.collection.children.link(self.coll_t)
        self.coll_t.hide_render = True
        self.lit_flame = []
        self.parents = {}
        self.tv_screen = None
        self.bulb_disc = None

    # ------------------------------------------------------------------------------------------------ materials of the finishes
    def pattern_mat(self, name, asset, tile_m, base_lin, rough=0.8, mode="bw", contrast=1.0, normal=True):
        """A Poly Haven texture laid in world metres (box projection), its pattern carried onto the target's base colour: out = base x tex / mean(tex) (bw: by luminance; rgb: by channel)."""
        fl = tex_files(asset)
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        p = nt.nodes["Principled BSDF"]
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (1.0 / tile_m,) * 3
        nt.links.new(geo.outputs["Position"], mp.inputs["Vector"])

        def img(path, colour):
            n = nt.nodes.new("ShaderNodeTexImage")
            n.image = bpy.data.images.load(path, check_existing=True)
            n.image.colorspace_settings.name = "sRGB" if colour else "Non-Color"
            n.projection = "BOX"
            n.projection_blend = 0.2
            nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
            return n
        d = img(fl["diff"], True)
        mean = tex_mean(asset)
        base = np.asarray(base_lin, np.float32)
        mul = nt.nodes.new("ShaderNodeMix")
        mul.data_type = "RGBA"
        mul.blend_type = "MULTIPLY"
        mul.inputs[0].default_value = 1.0
        if mode == "bw":
            bw = nt.nodes.new("ShaderNodeRGBToBW")
            nt.links.new(d.outputs["Color"], bw.inputs["Color"])
            gain = nt.nodes.new("ShaderNodeMath")
            gain.operation = "MULTIPLY"
            gain.inputs[1].default_value = float(1.0 / max(float(mean @ np.array([0.2126, 0.7152, 0.0722])), 1e-3))
            nt.links.new(bw.outputs["Val"], gain.inputs[0])
            last = gain
            if contrast != 1.0:
                pw = nt.nodes.new("ShaderNodeMath")
                pw.operation = "POWER"
                pw.inputs[1].default_value = contrast
                nt.links.new(gain.outputs["Value"], pw.inputs[0])
                last = pw
            comb = nt.nodes.new("ShaderNodeCombineColor")
            for ch in ("Red", "Green", "Blue"):
                nt.links.new(last.outputs["Value"], comb.inputs[ch])
            mul.inputs[6].default_value = (*base, 1.0)
            nt.links.new(comb.outputs["Color"], mul.inputs[7])
        else:
            tint = np.clip(base / np.maximum(mean, 1e-3), 0.02, 4.0)
            nt.links.new(d.outputs["Color"], mul.inputs[6])
            mul.inputs[7].default_value = (*[float(t) for t in tint], 1.0)
        nt.links.new(mul.outputs[2], p.inputs["Base Color"])
        p.inputs["Roughness"].default_value = rough
        if normal and "nor_gl" in fl:
            n = img(fl["nor_gl"], False)
            nm = nt.nodes.new("ShaderNodeNormalMap")
            nm.inputs["Strength"].default_value = 0.6
            nt.links.new(n.outputs["Color"], nm.inputs["Color"])
            nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
        self.mats[name] = m
        return m

    def stripe_mat(self, base_lin, alt_lin, period_m=0.09):
        """wallpaper_stripe: a script-drawn vertical stripe, cream and fawn, 90 mm period, with a little paper grain (the stripes run up the wall: the box projection takes u along the wall)."""
        n = 512
        rng = np.random.default_rng(5)
        img = np.zeros((n, n, 3), np.float32)
        half = n // 2
        a = np.array(base_lin, np.float32)
        b = np.array(alt_lin, np.float32)
        img[:, :half] = a
        img[:, half:] = b
        # a thin darker line at each stripe edge (a printed edge) and the paper's grain
        img[:, :3] *= 0.82
        img[:, half:half + 3] *= 0.85
        img *= (1.0 + rng.normal(0, 0.02, (n, n, 1)))
        out = np.where(img <= 0.0031308, img * 12.92, 1.055 * np.clip(img, 0, 1) ** (1 / 2.4) - 0.055)
        path = os.path.join(self.tex, "stripe.png")
        Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path)
        return self.image_mat("wallpaper_stripe", path, tile_m=period_m, rough=0.7)

    def finish_mat(self, key):
        fin = T.target()["rooms"]["finishes"][key]
        base = fin["base_lin"]
        tex = fin.get("texture")
        rough = fin["rough"]
        if key == "wallpaper_stripe":
            return self.stripe_mat(base, fin["stripe_alt"], fin["stripe_period_mm"] / 1000.0)
        tile = {"wallpaper_floral": 0.55, "boards": 1.3, "carpet_brown": 1.0, "lino": 0.9, "ceiling_white": 1.2, "stripped_paper": 1.1, "peeling_paint": 1.3}.get(key, 1.5)
        mode = "rgb" if key == "peeling_paint" else "bw"
        if key == "ceiling_white":
            base = [v * (0.92 if self.R["type"] in ("lounge", "bedroom", "front_room", "landing") else 1.0) for v in base]
        return self.pattern_mat("fin_" + key, tex, tile, base, rough=rough, mode=mode)

    # ------------------------------------------------------------------------------------------------ the shell and the forms
    def shell(self):
        W, H, D = self.W, self.H, self.D
        R = self.R
        wall_m = self.finish_mat(R["walls"])
        ceil_m = self.finish_mat(R["ceiling"])
        floor_m = self.finish_mat(R["floor"])
        self.wall_m = wall_m
        self.box("floor", -W / 2 - 0.1, W / 2 + 0.1, 0, D + 0.1, -0.05, 0.0, floor_m)
        self.box("ceiling", -W / 2 - 0.1, W / 2 + 0.1, 0, D + 0.1, H, H + 0.05, ceil_m)
        self.box("wall_left", -W / 2 - 0.1, -W / 2, 0, D + 0.1, -0.05, H + 0.05, wall_m)
        self.box("wall_right", W / 2, W / 2 + 0.1, 0, D + 0.1, -0.05, H + 0.05, wall_m)
        self.box("wall_back", -W / 2, W / 2, D, D + 0.1, -0.05, H + 0.05, wall_m)
        self.paint = self.mat("paint_white", PAINT_WHITE, rough=0.5)
        self.paint_dim = self.mat("paint_white_dim", tuple(0.8 * v for v in PAINT_WHITE), rough=0.55)
        self.shade_m = self.mat("form_shade", (0.05, 0.04, 0.035), rough=0.9)

    def _wall_band(self, nm, z0, z1, proud, mat, back=True, sides=True, y0=0.0, gap=False):
        """A flat band on the back and side walls (from y0 to the back wall), `proud` off the surface: the scripted forms of target 7.2."""
        W, D = self.W, self.D
        out = []
        gb, gr = (self.door_gap() if gap else (None, None))        # a doorway has no skirting: a band that ran behind the door's leaf stood on the same plane and shadowed it black
        if back:
            segs = [(-W / 2 + proud, W / 2 - proud)] if gb is None else [(-W / 2 + proud, gb[0]), (gb[1], W / 2 - proud)]
            for k, (a, b) in enumerate(segs):
                out.append(self.box(nm + "_back" + ("" if k == 0 else "_%d" % k), a, b, D - proud, D, z0, z1, mat))
        if sides:
            out.append(self.box(nm + "_left", -W / 2, -W / 2 + proud, y0, D - proud, z0, z1, mat))
            segs = [(y0, D - proud)] if gr is None else [(y0, gr[0]), (gr[1], D - proud)]
            for k, (a, b) in enumerate(segs):
                out.append(self.box(nm + "_right" + ("" if k == 0 else "_%d" % k), W / 2 - proud, W / 2, a, b, z0, z1, mat))
        return out

    def door_gap(self):
        """The doorway's width on the back wall (x range) and on the right wall (y range), or None."""
        if "internal_door_flat" not in self.R["forms"]:
            return None, None
        w = T.target()["rooms"]["forms"]["internal_door_flat"]["w"]
        if self.R["type"] == "landing":
            xc = -0.55 if self.R["variant"] == 1 else 0.55
            return (xc - w / 2, xc + w / 2), None
        return None, (1.7 - w / 2, 1.7 + w / 2)

    def forms(self):
        W, H, D = self.W, self.H, self.D
        F = T.target()["rooms"]["forms"]
        R = self.R
        for f in R["forms"]:
            spec = F[f]
            if f == "skirting":
                self._wall_band("skirting", 0.0, spec["h"], spec["proud"], self.paint, gap=True)
                self.forms_rec.append({"form": f, "surface": "side+back", "proud": spec["proud"]})
            elif f == "picture_rail":
                z = spec["z"]
                self._wall_band("picture_rail", z - spec["h"] / 2, z + spec["h"] / 2, spec["proud"], self.paint)
                self._wall_band("picture_rail_shade", z - spec["h"] / 2 - 0.012, z - spec["h"] / 2, 0.004, self.shade_m)
                self.forms_rec.append({"form": f, "surface": "side+back", "proud": spec["proud"]})
            elif f == "coving":
                self._wall_band("coving", H - spec["h"], H, spec["proud"], self.paint_dim)
                self._wall_band("coving_shade", H - spec["h"] - 0.008, H - spec["h"], 0.004, self.shade_m)
                self.forms_rec.append({"form": f, "surface": "ceiling edge", "proud": spec["proud"]})
            elif f == "ceiling_rose":
                self.cyl("rose_a", 0.0, 0.55, H - spec["proud"] / 2 * 0.5, spec["d"] / 2, spec["proud"] * 0.5, self.paint_dim, verts=40)
                self.cyl("rose_b", 0.0, 0.55, H - spec["proud"] * 0.75, spec["d"] * 0.32, spec["proud"] * 0.5, self.paint, verts=40)
                self.forms_rec.append({"form": f, "surface": "ceiling", "proud": spec["proud"]})
            elif f == "bare_bulb":
                self.bulb_mat = self.mat("bare_bulb_disc", (0.9, 0.9, 0.85), rough=0.4, emit=(1.0, 0.8, 0.5), emit_strength=0.0)
                self.bulb_disc = self.cyl("bare_bulb", 0.0, 0.55, H - spec["proud"] / 2, spec["d"] / 2, spec["proud"], self.bulb_mat, verts=24)
                self.forms_rec.append({"form": f, "surface": "ceiling", "proud": spec["proud"]})
            elif f == "fire_surround_flat":
                self._fire_surround(spec, left=(self.R["variant"] % 2 == 1))
            elif f == "internal_door_flat":
                self._door(spec)
            elif f == "radiator_flat":
                self._radiator(spec)
            elif f == "stair_flat":
                self._stair(spec)
            elif f == "chimney_breast_flat":
                self._chimney(spec)
            elif f == "picture_ghost":
                self._ghost(spec)

    def _fire_surround(self, spec, left=True):
        W, D = self.W, self.D
        pr = spec["proud"]
        x0, x1 = (-W / 2, -W / 2 + pr) if left else (W / 2 - pr, W / 2)
        yc = 2.2
        w, h = spec["w"], spec["h"]
        tile = self.mat("fire_tile", rgb8(136, 104, 72), rough=0.35)
        dark = self.mat("grate_dark", (0.012, 0.011, 0.01), rough=0.7)
        iron = self.mat("grate_iron", (0.03, 0.03, 0.032), rough=0.45, metal=0.8)
        self.box("fire_surround", x0, x1, yc - w / 2, yc + w / 2, 0.0, h, tile)
        # the opening (dark) and a hearth strip: flat on the surround's face, 3 mm further out than the surround would bury them (they are inside the 0.03 total)
        o0, o1 = (x0, x1) if left else (x0, x1)
        d = 0.003
        if left:
            xs0, xs1 = x1, x1 + d
        else:
            xs0, xs1 = x0 - d, x0
        self.box("fire_opening", xs0, xs1, yc - 0.28, yc + 0.28, 0.12, 0.78, dark)
        self.box("fire_bars", xs0 - (d if not left else 0), xs1 + (d if left else 0), yc - 0.27, yc + 0.27, 0.15, 0.17, iron)
        self.forms_rec.append({"form": "fire_surround_flat", "surface": "left" if left else "right", "proud": pr + d})

    def _door(self, spec):
        W, D = self.W, self.D
        pr = spec["proud"]
        r = self.R
        door_m = self.mat("door_paint", (0.62, 0.60, 0.55), rough=0.5)
        glass_m = self.mat("door_glass_dark", (0.03, 0.035, 0.04), rough=0.15)
        w, h = spec["w"], spec["h"]
        if r["type"] == "landing":
            xc = -0.55 if r["variant"] == 1 else 0.55
            y0, y1 = D - pr, D
            x0, x1 = xc - w / 2, xc + w / 2
            panels = [(0.08, 0.76, 0.08, 0.82), (0.08, 0.76, 0.98, 1.82)]
            # a half-glazed landing door: the upper two panels glazed (dark: the hall beyond is unlit)
            lower = [(x0 + 0.1, x1 - 0.1, 0.1, 0.55), (x0 + 0.1, x1 - 0.1, 0.64, 1.02)]
            upper = [(x0 + 0.1, x1 - 0.1, 1.12, 1.78)]
            self.box("door_leaf", x0, x1, y0, y1, 0.0, h, door_m)
            for k, (a, b, c, d_) in enumerate(lower):
                self.box("door_panel_%d" % k, a, b, y0 - 0.003, y0, c, d_, self.paint_dim)
            for k, (a, b, c, d_) in enumerate(upper):
                self.box("door_glass_%d" % k, a, b, y0 - 0.003, y0, c, d_, glass_m)
            self.forms_rec.append({"form": "internal_door_flat", "surface": "back", "proud": pr + 0.003})
        else:
            # gf_front_2: the hall door on the right wall
            x0, x1 = W / 2 - pr, W / 2
            yc = 1.7
            self.box("door_leaf", x0, x1, yc - w / 2, yc + w / 2, 0.0, h, door_m)
            for k, (c, d_) in enumerate(((0.1, 0.55), (0.64, 1.02), (1.12, 1.50), (1.58, 1.88))):
                self.box("door_panel_%d" % k, x0 - 0.003, x0, yc - w / 2 + 0.1, yc + w / 2 - 0.1, c, d_, self.paint_dim)
            self.forms_rec.append({"form": "internal_door_flat", "surface": "right", "proud": pr + 0.003})

    def _radiator(self, spec):
        W = self.W
        pr = spec["proud"]
        rad = self.mat("radiator", (0.65, 0.64, 0.6), rough=0.4)
        x0, x1 = (W / 2 - pr, W / 2)
        yc = 2.4
        w, h = spec["w"], spec["h"]
        self.box("radiator", x0, x1, yc - w / 2, yc + w / 2, 0.15, 0.15 + h, rad)
        self.forms_rec.append({"form": "radiator_flat", "surface": "right", "proud": pr})

    def _prism_yz(self, name, pts, x0, x1, mat):
        """A board drawn in the side wall's plane: the polygon `pts` (y, z) extruded across x0..x1."""
        n = len(pts)
        verts = [(x0, y, z) for y, z in pts] + [(x1, y, z) for y, z in pts]
        faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
        for k in range(n):
            faces.append((k, (k + 1) % n, n + (k + 1) % n, n + k))
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces)
        me.update()
        o = bpy.data.objects.new(name, me)
        self.sc.collection.objects.link(o)
        o.data.materials.append(mat)
        for poly in me.polygons:
            poly.use_smooth = False
        return o

    def _stair(self, spec):
        """The flight along the left wall, rising toward the back wall at 36 degrees: a stringer (a 0.30 board along the slope, cut vertical where it meets the floor, ending at the back wall), a handrail 0.9
        above the floor at the foot and a newel and balusters (30 mm boards, the stringer's own 0.03 proud), the rail ending under the ceiling where the flight goes on through the stairwell. A first
        version had the slope the wrong way (rising toward the window) and ran through the picture rail and the ceiling."""
        W, D, H = self.W, self.D, self.H
        pr = spec["proud"]
        wood = self.mat("stair_paint", (0.5, 0.46, 0.38), rough=0.5)
        rail_m = self.mat("stair_rail", (0.30, 0.22, 0.15), rough=0.45)
        t = math.tan(math.radians(36.0))
        x0, x1 = -W / 2, -W / 2 + pr
        ya, yb = 1.4, D - 0.03
        zline = lambda y: (y - ya) * t
        # three front planes (26, 29 and 30 mm proud) so no two faces share a plane (coplanar boards shadow each other black)
        self._prism_yz("stair_stringer", [(ya, 0.0), (yb, zline(yb)), (yb, zline(yb) + 0.30), (ya, 0.30)], x0, x0 + 0.026, wood)
        ye = 3.45                                                  # the rail ends here, under the coving
        self._prism_yz("stair_handrail", [(ya, 0.87), (ye, zline(ye) + 0.87), (ye, zline(ye) + 0.93), (ya, 0.93)], x0, x1, rail_m)
        self.box("stair_newel", x0, x1, ya - 0.09, ya, 0.0, 1.02, rail_m)
        y = ya + 0.14
        k = 0
        while y < ye - 0.02:
            self.box("stair_baluster_%d" % k, x0, x0 + 0.029, y, y + 0.032, zline(y) + 0.20, zline(y + 0.032) + 0.90, wood)
            y += 0.14
            k += 1
        self.forms_rec.append({"form": "stair_flat", "surface": "left", "proud": pr, "balusters": k})

    def _chimney(self, spec):
        W, D = self.W, self.D
        pr = spec["proud"]
        xc = 0.0 if self.R["variant"] == 1 else 0.3
        w = spec["w"]
        m = self.mat("chimney_plaster", (0.30, 0.27, 0.22), rough=0.9)
        side = self.mat("chimney_shade", (0.1, 0.09, 0.075), rough=0.9)
        self.box("chimney_breast", xc - w / 2, xc + w / 2, D - pr, D, 0.0, self.H, m)
        self.box("chimney_edge_l", xc - w / 2 - 0.004, xc - w / 2, D - pr, D, 0.0, self.H, side)
        self.box("chimney_edge_r", xc + w / 2, xc + w / 2 + 0.004, D - pr, D, 0.0, self.H, side)
        self.forms_rec.append({"form": "chimney_breast_flat", "surface": "back", "proud": pr})

    def _ghost(self, spec):
        D = self.D
        xc, zc = 0.62, 1.55
        w, h = spec["w"], spec["h"]
        m = self.mat("picture_ghost", (0.52, 0.47, 0.38), rough=0.9)
        self.box("picture_ghost", xc - w / 2, xc + w / 2, D - 0.001, D - 0.0, zc - h / 2, zc + h / 2, m)
        self.forms_rec.append({"form": "picture_ghost", "surface": "back", "proud": 0.001})

    # ------------------------------------------------------------------------------------------------ the objects
    def _hide_extra_flame(self, objs, on):
        pass

    def fix_material_quirks(self, asset, objs):
        """A model's materials after import: the leaves' map has no alpha channel in the 1k jpg (the cutout is the black ground): the alpha is made from the map's brightness; the lamp's
        flame is a card whose material becomes an emission with the same cut-out, shown in night_lit only."""
        for nm in objs:
            ob = bpy.data.objects[nm]
            for sl in ob.material_slots:
                m = sl.material
                if m is None or not m.use_nodes:
                    continue
                low = m.name.lower()
                if low.startswith("ornate_mirror") and not m.get("hw_mirror"):
                    # the mirror reflected the day's area light and the dark world: a white or black arch (14 October): its roughness is kept at 0.4 or more and its metal at most 0.5, a dim old mirror
                    nt = m.node_tree
                    p = nt.nodes["Principled BSDF"]
                    for lk in list(nt.links):
                        if lk.to_socket == p.inputs["Roughness"]:
                            mx = nt.nodes.new("ShaderNodeMath")
                            mx.operation = "MAXIMUM"
                            mx.inputs[1].default_value = 0.42
                            nt.links.new(lk.from_socket, mx.inputs[0])
                            nt.links.new(mx.outputs["Value"], p.inputs["Roughness"])
                    for lk in list(nt.links):
                        if lk.to_socket == p.inputs["Metallic"]:
                            mn = nt.nodes.new("ShaderNodeMath")
                            mn.operation = "MINIMUM"
                            mn.inputs[1].default_value = 0.45
                            nt.links.new(lk.from_socket, mn.inputs[0])
                            nt.links.new(mn.outputs["Value"], p.inputs["Metallic"])
                    m["hw_mirror"] = True
                if "leaves" in low and not m.get("hw_alpha"):
                    nt = m.node_tree
                    p = nt.nodes["Principled BSDF"]
                    tx = next((n for n in nt.nodes if n.type == "TEX_IMAGE" and n.image is not None and "diff" in n.image.name.lower()), None)
                    if tx is not None:
                        bw = nt.nodes.new("ShaderNodeRGBToBW")
                        gt = nt.nodes.new("ShaderNodeMath")
                        gt.operation = "GREATER_THAN"
                        gt.inputs[1].default_value = 0.035
                        nt.links.new(tx.outputs["Color"], bw.inputs["Color"])
                        nt.links.new(bw.outputs["Val"], gt.inputs[0])
                        nt.links.new(gt.outputs["Value"], p.inputs["Alpha"])
                        m["hw_alpha"] = True
                if "flame" in low and not m.get("hw_flame"):
                    nt = m.node_tree
                    for n in list(nt.nodes):
                        nt.nodes.remove(n)
                    tx = nt.nodes.new("ShaderNodeTexImage")
                    tx.image = bpy.data.images.load(os.path.join(A.POLY, "vintage_oil_lamp", "1k", "textures", "vintage_oil_lamp_flame_diff_1k.jpg"), check_existing=True)
                    bw = nt.nodes.new("ShaderNodeRGBToBW")
                    gt = nt.nodes.new("ShaderNodeMath")
                    gt.operation = "GREATER_THAN"
                    gt.inputs[1].default_value = 0.05
                    em = nt.nodes.new("ShaderNodeEmission")
                    em.inputs["Strength"].default_value = 6.0
                    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
                    mx = nt.nodes.new("ShaderNodeMixShader")
                    out = nt.nodes.new("ShaderNodeOutputMaterial")
                    nt.links.new(tx.outputs["Color"], bw.inputs["Color"])
                    nt.links.new(bw.outputs["Val"], gt.inputs[0])
                    nt.links.new(tx.outputs["Color"], em.inputs["Color"])
                    nt.links.new(gt.outputs["Value"], mx.inputs["Fac"])
                    nt.links.new(tr.outputs[0], mx.inputs[1])
                    nt.links.new(em.outputs[0], mx.inputs[2])
                    nt.links.new(mx.outputs[0], out.inputs[0])
                    m["hw_flame"] = True
                    self.lit_flame.append(nm)

    def swap_print(self, objs, asset, k):
        """The frame's artwork: this placement's own copy of the mesh and of the artwork material, its picture node pointing at the print made for this placement."""
        dst = os.path.join(self.tex, "%s_%s_print%d.jpg" % (self.rid, asset, k))
        rec = M.print_map(asset, k, dst)
        for nm in objs:
            ob = bpy.data.objects[nm]
            ob.data = ob.data.copy()
            for i, m in enumerate(ob.data.materials):
                if m is not None and "artwork" in m.name.lower():
                    m2 = m.copy()
                    for n in m2.node_tree.nodes:
                        if n.type == "TEX_IMAGE" and n.image is not None and "artwork_diff" in n.image.name:
                            n.image = bpy.data.images.load(dst, check_existing=True)
                            n.image.colorspace_settings.name = "sRGB"
                    ob.data.materials[i] = m2
        self.print_log.append(rec)

    def support_z(self, parent_objs, x, y):
        """The height of the parent's own surface under (x, y): a ray cast down from just under the ceiling, the first hit on one of the parent's meshes (None: nothing of it there)."""
        dg = bpy.context.evaluated_depsgraph_get()
        origin = Vector((x, y, self.H - 0.02))
        d = Vector((0.0, 0.0, -1.0))
        for _ in range(12):
            ok, loc, nrm, idx, ob, mat = self.sc.ray_cast(dg, origin, d)
            if not ok:
                return None
            if ob.name in parent_objs:
                return loc.z
            origin = loc + d * 0.001
        return None

    def rest_on(self, parent, cx, cy, w, dpt):
        """Where a piece that stands on another piece (a clock on a cabinet, the television on its table) rests: the x of its centre that puts it on the flattest part of the parent's top
        (the lowest gap under its footprint, then the nearest to the target's x), and the height that rests it there. A gap of more than 6 mm is split: the base sinks into the crest by half of it,
        so nothing floats. Returns (x, z, record)."""
        objs, pext = parent
        bpy.context.view_layer.update()
        lo, hi = pext[0] + w / 2, pext[1] - w / 2
        cands = sorted(set([round(v, 3) for v in np.arange(lo, hi + 1e-9, 0.02)] + [min(max(cx, lo), hi)])) if hi > lo else [cx]
        best = None
        for c in cands:
            hs = [self.support_z(objs, gx, gy) for gx in np.linspace(c - w / 2 + 0.01, c + w / 2 - 0.01, 7) for gy in np.linspace(cy - dpt / 2 + 0.02, cy + dpt / 2 - 0.02, 3)]
            miss = sum(1 for h in hs if h is None)
            hv = [h for h in hs if h is not None]
            if not hv:
                continue
            gap = max(hv) - min(hv)
            score = gap + 0.004 * abs(c - cx) + 0.2 * miss
            if best is None or score < best[0]:
                best = (score, c, max(hv), gap, miss)
        if best is None:
            return cx, 0.0, {"on": None, "gap_mm": None}
        _, c, ztop, gap, miss = best
        z = ztop - (0.5 * gap if gap > 0.006 else 0.0)
        return c, z, {"gap_mm": round(gap * 1000, 1), "z_top_m": round(ztop, 4), "z_base_m": round(z, 4), "sink_mm": round((ztop - z) * 1000, 1), "points_off_the_parent": miss}

    def objects(self, frame_counter):
        W, H, D = self.W, self.H, self.D
        for k, o in enumerate(self.R["objects"]):
            asset = o["model"]
            pl = o["place"]
            surf = o["surface"]
            if surf == "back":
                rot = (0.0, 0.0, 0.0)
                cx = (pl["x_across"][0] + pl["x_across"][1]) / 2
                cy = (pl["y_back"][0] + pl["y_back"][1]) / 2
            else:
                sgn = 1 if pl["wall"] == "left" else -1
                rot = (0.0, 0.0, math.radians(90.0 * sgn))
                cx = (-W / 2 + (pl["x_from_wall"][0] + pl["x_from_wall"][1]) / 2) if sgn > 0 else (W / 2 - (pl["x_from_wall"][0] + pl["x_from_wall"][1]) / 2)
                cy = (pl["y_back"][0] + pl["y_back"][1]) / 2
            z0 = pl["z"][0]
            rest = None
            if o.get("on") and o["on"] in self.parents:
                dx, dy, dz = self.dims(asset, rot)
                cx, z0, rest = self.rest_on(self.parents[o["on"]], cx, cy, dx, dy)
            ext = self.place(asset, (cx, cy, z0), rot=rot, scale=1.0, fixture="obj%d" % k, anchor=("c", "c", "min"))
            objs = list(self.last_objs)
            self.parents[asset] = (objs, ext)
            self.fix_material_quirks(asset, objs)
            if asset.startswith("hanging_picture_frame"):
                idx = frame_counter.setdefault("n", 0)
                frame_counter["n"] = idx + 1
                self.swap_print(objs, asset, frame_counter.get("base", 0) + idx)
            self.placed[-1].update({"support": rest, "surface": surf, "class": o["class"], "stand_off_m": o["stand_off_m"], "on": o.get("on"), "wall": pl.get("wall"),
                                    "target_ext": [pl["x_across"][0], pl["x_across"][1], pl["y_back"][0], pl["y_back"][1], pl["z"][0], pl["z"][1]] if surf == "back" else None,
                                    "target_dims_mm": o["dims_mm"]})
            if asset == "television_02":
                self.tv = ext
            if asset == "vintage_oil_lamp":
                self.lamp = ext
        bpy.context.view_layer.update()

    # ------------------------------------------------------------------------------------------------ lights, camera, states
    def window_rects(self):
        """The window openings in the room frame: [(x0, x1, z0, z1)]: one in an upper room, two in a cottage's front room (target sites[].card.window_in_card_m)."""
        out = []
        for s in T.sites():
            if s["room"] == self.rid:
                c = s["card"]
                w = c["window_in_card_m"]
                x0, x1 = w["x0"] - self.W / 2, w["x1"] - self.W / 2
                out.append((x0, x1, w["z0"], w["z1"]))
        seen = []
        for r in out:
            if all(abs(r[0] - q[0]) > 1e-6 for q in seen):
                seen.append(r)
        return seen

    def lights(self):
        W, H, D = self.W, self.H, self.D
        self.sc.world = bpy.data.worlds.new("world")
        self.sc.world.use_nodes = True
        self.sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

        def area(name, loc, rot, sx, sy, colour):
            ld = bpy.data.lights.new(name, "AREA")
            ld.shape = "RECTANGLE"
            ld.size, ld.size_y = sx, sy
            ld.energy = 0.0
            ld.color = colour
            o = bpy.data.objects.new(name, ld)
            self.sc.collection.objects.link(o)
            o.location, o.rotation_euler = loc, rot
            o.visible_camera = False
            return o
        # day: an overcast sky as an area light the size of the card on its plane, shining into the room (6500 K)
        self.L_day = area("daylight", (0.0, -0.04, H / 2), (math.pi / 2, 0.0, 0.0), W, H, (0.96, 0.97, 1.0))
        # night_lit: the pendant at the ceiling rose, 0.30 below the ceiling (the shade itself is the kit's mesh): a small sphere of tungsten light
        ld = bpy.data.lights.new("pendant", "POINT")
        ld.color = WARM
        ld.shadow_soft_size = 0.09
        ld.energy = 0.0
        self.L_pend = bpy.data.objects.new("pendant", ld)
        self.sc.collection.objects.link(self.L_pend)
        bare = self.R["type"] in ("landing", "empty")
        self.L_pend.location = (0.0, 0.55, H - (0.10 if bare else 0.40))
        self.L_pend.visible_camera = False
        # 14 Oct, from the try 2 close review (narrow point 1): the pendant's point light made the ceiling round the rose a flat plateau at the roll-off's ceiling (34 per cent of that band at luma 200 or more in the close views); in the six lit lounges and bedrooms
        # the pendant is halved and the picture's mean is made up by a room-wide fill: a soft area light under the ceiling's centre, shining down (it lights the walls, the furniture and the floor and leaves the ceiling round the rose to the pendant's falloff)
        self.L_fill = None
        self.L_back = None
        if self.R["family"] == "UP" and self.R["type"] in ("lounge", "bedroom"):
            self.L_fill = area("fill", (0.0, D * 0.5, H - 0.06), (0.0, 0.0, 0.0), FILL_SIZE[0], FILL_SIZE[1], WARM)
            # and the back wall's own wash, a small share of the fill (WASH_RATIO): a street window sees the back wall's upper part and the ceiling, and a down-facing fill leaves the wall's top to the halved pendant (a lit lounge's clear
            # glass would then read under half of its net: NIGHT-07); a soft strip of light under the ceiling, 1.2 m in front of the back wall, shining at it
            self.L_back = area("wash_back", (0.0, D - 1.2, H - 0.25), (math.pi / 2.0, 0.0, 0.0), WASH_SIZE[0], WASH_SIZE[1], WARM)
        # a table lamp's glow on the back wall in the front rooms; the television's cool glow where tv_glow
        self.L_lamp = None
        if self.R["family"] == "GF":
            ld2 = bpy.data.lights.new("lamp", "POINT")
            ld2.color = WARM
            ld2.shadow_soft_size = 0.05
            ld2.energy = 0.0
            self.L_lamp = bpy.data.objects.new("lamp", ld2)
            self.sc.collection.objects.link(self.L_lamp)
            lx, lz = -0.5, 1.45
            if hasattr(self, "lamp"):
                lx, lz = (self.lamp[0] + self.lamp[1]) / 2, self.lamp[5] - 0.2
            elif hasattr(self, "tv"):
                lx, lz = (self.tv[0] + self.tv[1]) / 2 - 0.75, 1.3
            else:
                lx, lz = 0.9, 1.2
            self.L_lamp.location = (lx, D - 0.35, lz)
            self.L_lamp.visible_camera = False
        self.L_tv = None
        if self.R.get("tv_glow") and hasattr(self, "tv"):
            self.L_tv = area("tv_glow", ((self.tv[0] + self.tv[1]) / 2, self.tv[2] - 0.01, (self.tv[4] + self.tv[5]) / 2), (math.pi / 2 - 0.0, 0.0, math.pi), 0.30, 0.22, TV_COOL)
            self.L_tv.rotation_euler = (-math.pi / 2, 0.0, 0.0)
        # night_dark: the sodium wash through the window opening(s): each window's own size, tipped 30 degrees down (a card-wide wash burnt the shops' top corners: 14 October)
        self.L_wash = []
        for k, (x0, x1, z0, z1) in enumerate(self.window_rects()):
            self.L_wash.append(area("wash_%d" % k, ((x0 + x1) / 2, -0.04, (z0 + z1) / 2 - 0.05), (math.radians(60.0), 0.0, 0.0), x1 - x0, (z1 - z0) * 0.6, SODIUM))
        # the lit bare bulb of a landing: a warm point light at the disc
        if self.bulb_disc is not None:
            self.bulb_disc.location = (0.0, 0.55, H - 0.01)

    def camera(self):
        cam = bpy.data.cameras.new("cam")
        cam.sensor_fit = "HORIZONTAL"
        cam.angle = 2.0 * math.atan(self.W / (2.0 * self.camd))
        o = bpy.data.objects.new("cam", cam)
        self.sc.collection.objects.link(o)
        o.location = (0.0, -self.camd, self.H / 2.0)
        o.rotation_euler = (math.pi / 2.0, 0.0, 0.0)
        self.sc.camera = o
        self.cam = o

    def lit_possible(self):
        return self.R["type"] != "empty"

    def set_state(self, state, P):
        """P: the energies {day, pend, lamp, tv, wash, bulb}."""
        lit = state == "night_lit" and self.lit_possible()
        wash_state = state == "night_dark" or (state == "night_lit" and not self.lit_possible())
        self.L_day.data.energy = P["day"] if state == "day" else 0.0
        bare = self.R["type"] in ("landing", "empty")
        self.L_pend.data.energy = P["pend_bare" if bare else "pend"] if lit else 0.0
        if self.L_fill is not None:
            self.L_fill.data.energy = P.get("fill", 0.0) if lit else 0.0
            self.L_back.data.energy = P.get("fill", 0.0) * WASH_RATIO if lit else 0.0
        if self.L_lamp is not None:
            self.L_lamp.data.energy = P["lamp"] if lit else 0.0
        if self.L_tv is not None:
            self.L_tv.data.energy = P["tv"] if lit else 0.0
        for o in self.L_wash:
            o.data.energy = P["wash"] if wash_state else 0.0
        if self.bulb_disc is not None:
            self.bulb_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 8.0 if lit else 0.0
            self.bulb_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (1.0, 0.714, 0.344, 1.0)
        for nm in self.lit_flame:
            bpy.data.objects[nm].hide_render = not lit
        if self.tv_screen is not None:
            self.tv_screen.hide_render = not lit

    def render(self, path, samples, res, state=None):
        """A night_lit picture is rendered to a float EXR and written as 8-bit only after the highlight roll-off (14 October, from the try 1 close review, fault 2: the ceiling round the rose clipped (255, 253, 178), so
        the hue went yellow and the card's gain then made it olive). The other states are written as before."""
        if state == "night_lit" and self.lit_possible():
            exr = os.path.splitext(path)[0] + ".exr"
            super().render(exr, samples, res, exr=True)
            lin_img = read_exr(exr)
            os.remove(exr)
            write_rolled(lin_img, path)
            return
        super().render(path, samples, res)

    def build(self):
        self.shell()
        self.forms()
        import zlib
        self.frame_counter = {"base": zlib.crc32(self.rid.encode()) % 12}
        self.objects(self.frame_counter)
        self.lights()
        self.camera()
        if self.R.get("tv_glow") and hasattr(self, "tv"):
            # the television's screen: a cool emissive card on the front of the set, shown in night_lit only
            x0, x1, y0, y1, z0, z1 = self.tv
            m = self.mat("tv_screen", (0.05, 0.06, 0.09), rough=0.2, emit=TV_COOL, emit_strength=0.45)
            self.tv_screen = self.box("tv_screen", (x0 + x1) / 2 - 0.12, (x0 + x1) / 2 + 0.12, y0 - 0.002, y0 - 0.0005, z0 + 0.09, z0 + 0.26, m)
        return self


DEFAULT_P = {"day": 38.0, "pend": 34.0, "pend_bare": 14.0, "lamp": 4.0, "tv": 6.0, "wash": 4.2}
TARGET_MEAN = {"day": 105.0, "night_lit": 70.0, "night_dark": 15.0}
LANDING_MEAN = 40.0


def luma_stats(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    y = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
    return float(y.mean())


def calibrate(r, work, log=print, res=None, samples=8):
    """The light strengths so each state's mean luma meets the picture standard (day 105, night_lit 70 (landings 40), night_dark 15), by a few small renders."""
    res = res or (int(r.pix[0] / 4), int(r.pix[1] / 4))
    P = dict(DEFAULT_P)
    tmp = os.path.join(work, "cal.png")
    bare = r.R["type"] in ("landing", "empty")

    def measure(state):
        r.set_state(state, P)
        r.render(tmp, samples, res, state=state)
        return luma_stats(tmp)

    def tune(keys, state, tgt, iters=4):
        for _ in range(iters):
            m = measure(state)
            log("   calibrate %s %s: %.4g -> mean %.1f (target %.1f)" % (state, keys[0], P[keys[0]], m, tgt))
            if abs(m - tgt) / tgt < 0.04:
                break
            f = (tgt / max(m, 0.5)) ** 2.2
            for k in keys:
                P[k] = float(np.clip(P[k] * f, 1e-3, 1e6))
    tune(["day"], "day", TARGET_MEAN["day"])
    if r.lit_possible():
        tune(["pend_bare" if bare else "pend"] + (["lamp", "tv"] if not bare else []), "night_lit", LANDING_MEAN if bare else TARGET_MEAN["night_lit"])
    tune(["wash"], "night_dark", TARGET_MEAN["night_dark"])
    P["measured"] = {s: measure(s) for s in STATES}
    return P


def render_room(rid, out_dir, samples=24, log=print, states=RENDER_ORDER, work=None, scale=1.0, quick=False):
    """Build the room, calibrate, render the three states (the empty rooms' night_lit is their night_dark), write the pictures and <room>.json. Returns the times."""
    work = work or os.path.join(T.SCRATCH, "work", rid)
    os.makedirs(work, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    r = HRoom(rid, work).build()
    if r.R["family"] == "GF":
        samples = min(samples, 16)          # four times the pixels of an upper room: the denoised noise per pixel is the same at 16 samples (PIC-09 measures it)
    log("%s built in %.0f s" % (rid, time.time() - t0))
    P = dict(DEFAULT_P) if quick else calibrate(r, work, log)
    times = {}
    res = (int(r.pix[0] * scale), int(r.pix[1] * scale))
    rec = {"room": rid, "w": r.W, "h": r.H, "d": r.D, "camera_d": r.camd, "pixels": list(r.pix), "states": {}, "made_by": "production/cloud-week/kit/house-windows/build_windows.py (hw_roomgen.py)",
           "samples": samples, "light_params": {k: (round(v, 4) if not isinstance(v, dict) else v) for k, v in P.items()}, "prints": r.print_log, "wash": "the window's own size, tipped 30 degrees down"}
    for s in states:
        path = os.path.join(out_dir, "%s_%s.png" % (rid, s))
        if s == "night_lit" and not r.lit_possible():
            if os.path.exists(os.path.join(out_dir, "%s_night_dark.png" % rid)):
                import shutil
                shutil.copyfile(os.path.join(out_dir, "%s_night_dark.png" % rid), path)
                rec["states"][s] = os.path.basename(path)
                continue
        r.set_state(s, P)
        t1 = time.time()
        r.render(path, samples, res, state=s)
        times[s] = round(time.time() - t1, 1)
        rec["states"][s] = os.path.basename(path)
        log("render %s %s: %.0f s, mean luma %.1f" % (rid, s, times[s], luma_stats(path)))
    for s in STATES:
        rec["states"].setdefault(s, "%s_%s.png" % (rid, s))
    rec["render_s"] = times
    json.dump(rec, open(os.path.join(out_dir, rid + ".json"), "w"), indent=1)
    placed = {"room": rid, "placed": r.placed, "forms": r.forms_rec, "audit": r.__dict__.get("audit", {}), "size_m": [r.W, r.H, r.D]}
    json.dump(placed, open(os.path.join(out_dir, rid + ".placed.json"), "w"), indent=1)
    return times


def rebake_lit(rid, out_dir, samples=24, log=print, work=None):
    """14 October, from the try 1 close review (fault 2): re-render ONLY the room's night_lit picture with the highlight roll-off; the day and night_dark pictures, the placement and the room's JSON are kept (the room is built
    again by the same script and seed, so every object stands where it stood: `<room>.placed.json` is not written). The pendant's (and the lamp's and the television's) strength is tuned again so the ROLLED-OFF picture meets the
    standard (mean luma 70, a landing 40, within 15 per cent): the fill is raised, the peak is not (the roll-off ceiling holds it). Returns the seconds."""
    work = work or os.path.join(T.SCRATCH, "work", rid)
    os.makedirs(work, exist_ok=True)
    jp = os.path.join(out_dir, rid + ".json")
    rec = json.load(open(jp))
    t0 = time.time()
    r = HRoom(rid, work).build()
    if not r.lit_possible():
        log("%s: an empty room, its night_lit is its night_dark: kept" % rid)
        return 0.0
    if r.R["family"] == "GF":
        samples = min(samples, 16)
    P = {k: v for k, v in rec["light_params"].items() if k != "measured"}
    bare = r.R["type"] in ("landing", "empty")
    keys = ["pend_bare" if bare else "pend"] + (["lamp", "tv"] if not bare else [])
    tgt = LANDING_MEAN if bare else TARGET_MEAN["night_lit"]
    res_q = (int(r.pix[0] / 4), int(r.pix[1] / 4))
    tmp = os.path.join(work, "cal_lit.png")
    for it in range(5):
        r.set_state("night_lit", P)
        r.render(tmp, 8, res_q, state="night_lit")
        m = luma_stats(tmp)
        log("   rebake %s night_lit %s %.4g -> rolled-off mean %.1f (target %.1f)" % (rid, keys[0], P[keys[0]], m, tgt))
        if abs(m - tgt) / tgt < 0.04:
            break
        f = (tgt / max(m, 0.5)) ** 2.2
        for k in keys:
            P[k] = float(np.clip(P[k] * f, 1e-3, 1e6))
    path = os.path.join(out_dir, "%s_night_lit.png" % rid)
    r.set_state("night_lit", P)
    t1 = time.time()
    r.render(path, samples, (int(r.pix[0]), int(r.pix[1])), state="night_lit")
    dt = round(time.time() - t1, 1)
    mean = luma_stats(path)
    a = np.asarray(Image.open(path).convert("RGB"))
    log("render %s night_lit (rolled off): %.0f s, mean luma %.1f, pixels with a channel at 250+: %.4f%%" % (rid, dt, mean, 100.0 * float((a >= 250).any(axis=2).mean())))
    P["measured"] = dict(rec["light_params"].get("measured", {}))
    P["measured"]["night_lit"] = mean
    rec["light_params"] = {k: (round(v, 4) if not isinstance(v, dict) else v) for k, v in P.items()}
    rec["lit_rolloff"] = {"knee_linear": ROLL_KNEE, "top_linear": ROLL_TOP, "what": "14 Oct: the night_lit picture was re-rendered to a float picture and rolled off before the 8-bit write (hw_roomgen.roll_off); day and night_dark are unchanged"}
    rec.setdefault("render_s", {})["night_lit"] = dt
    json.dump(rec, open(jp, "w"), indent=1)
    return time.time() - t0


LIT_MEAN_AIM = 77.0             # the lit lounges' and bedrooms' mean luma aim (the standard is 70 +-15 per cent): a first set at 71 left the Hook's lit windows at 0.8 of their old light (the pendant's upper wall and ceiling halved) and NIGHT-08's lit-to-dark ratio at 2.49 against 2.5; 77 is inside the standard and restores it
PEND_CAP = 13.5                 # try 3: the pendant's point light is halved, and at most this (the ceiling round the rose stays under the roll-off's knee: at 17 the close view's band had 12 per cent of its pixels over luma 200, at 13.4 four)
GF_BOX = (849.0 / 3072.0, 649.0 / 2349.0, 2223.0 / 3072.0, 1700.0 / 2349.0)     # the close review's back wall box of a cottage picture (x0, y0, x1, y1 as fractions of the picture)
GF_BOX_AIM = 0.15               # the aim for its mean linear luminance (PIC-14 asks at least 0.12; the lit net glows 0.306)


def box_mean_Y(path, box=GF_BOX):
    a = np.asarray(Image.open(path).convert("RGB"))
    l_ = lin_of(a)
    Y = 0.2126 * l_[..., 0] + 0.7152 * l_[..., 1] + 0.0722 * l_[..., 2]
    h, w = Y.shape
    return float(Y[int(round(box[1] * h)):int(round(box[3] * h)), int(round(box[0] * w)):int(round(box[2] * w))].mean())


def relight_v3(rid, out_dir, samples=24, log=print, work=None):
    """14 October, from the try 2 close review (narrow point 1 and the row rulings): re-render ONLY a lit room's night_lit picture with new lights, keeping the day and night_dark pictures, the placement and the stored light parameters of everything else.
    The lit lounges and bedrooms (six): the pendant is halved (and at most PEND_CAP) and a room-wide fill (`fill`, an area light under the ceiling's centre, with WASH_RATIO of its power as a strip on the back wall's top) makes up the mean 70 (within 3 per cent).
    The cottages' front rooms (three): the table lamp's glow on the back wall (`lamp`) is raised, the pendant is not, until the back wall box [848.8, 649.1, 2223.2, 1700.1] reads GF_BOX_AIM linear (PIC-14: at least 0.12). The picture is rolled off before the 8-bit write as before."""
    work = work or os.path.join(T.SCRATCH, "work", rid)
    os.makedirs(work, exist_ok=True)
    jp = os.path.join(out_dir, rid + ".json")
    rec = json.load(open(jp))
    t0 = time.time()
    r = HRoom(rid, work).build()
    if not r.lit_possible():
        log("%s: an empty room, its night_lit is its night_dark: kept" % rid)
        return 0.0
    gf = r.R["family"] == "GF"
    if gf:
        samples = min(samples, 16)
    P = {k: v for k, v in rec["light_params"].items() if k != "measured"}
    v2 = dict(rec["relit_try3"]["was"]) if "relit_try3" in rec else {k: P[k] for k in ("pend", "lamp") if k in P}          # the lights of the try 2 picture, kept in the record: a second relight starts from them, not from the first relight's
    for k, v in v2.items():
        P[k] = v
    P.pop("fill", None)
    res_q = (int(r.pix[0] / 4), int(r.pix[1] / 4))
    tmp = os.path.join(work, "cal_lit_v3.png")
    if gf:
        key, tgt = "lamp", GF_BOX_AIM
        P["lamp"] = v2["lamp"] * 8.0
        measure = lambda path: box_mean_Y(path)
    else:
        key, tgt = "fill", LIT_MEAN_AIM
        P["pend"] = min(0.5 * v2["pend"], PEND_CAP)
        P["fill"] = (15.0 + 5.0) * v2["pend"] / 26.5
        measure = luma_stats
    hist = []
    for it in range(6):
        r.set_state("night_lit", P)
        r.render(tmp, 8, res_q, state="night_lit")
        m = measure(tmp)
        log("   relight %s night_lit %s %.4g -> %s %.4f (aim %.4g)" % (rid, key, P[key], "box mean Y" if gf else "mean luma", m, tgt))
        hist.append((P[key], m))
        if abs(m - tgt) / tgt < (0.04 if gf else 0.03):
            break
        if len(hist) == 1:
            P[key] = P[key] * (tgt / max(m, 1e-3)) ** (1.0 if gf else 1.0)
        else:
            (f0, m0), (f1, m1) = hist[-2], hist[-1]
            P[key] = float(max(f1 + (tgt - m1) * (f1 - f0) / (m1 - m0), 0.05 * f1)) if abs(m1 - m0) > 1e-9 else P[key] * 1.2
    path = os.path.join(out_dir, "%s_night_lit.png" % rid)
    r.set_state("night_lit", P)
    t1 = time.time()
    r.render(path, samples, (int(r.pix[0]), int(r.pix[1])), state="night_lit")
    dt = round(time.time() - t1, 1)
    mean = luma_stats(path)
    a = np.asarray(Image.open(path).convert("RGB"))
    extra = ", back wall box mean linear %.4f" % box_mean_Y(path) if gf else ""
    log("render %s night_lit (try 3 lights): %.0f s, mean luma %.1f%s, pixels with a channel at 250+: %.4f%%" % (rid, dt, mean, extra, 100.0 * float((a >= 250).any(axis=2).mean())))
    P["measured"] = dict(rec["light_params"].get("measured", {}))
    P["measured"]["night_lit"] = mean
    rec["light_params"] = {k: (round(v, 4) if not isinstance(v, dict) else v) for k, v in P.items()}
    rec["relit_try3"] = {"what": "14 Oct, from the try 2 close review: only the night_lit picture was re-rendered with new lights (hw_roomgen.relight_v3); the day and night_dark pictures and the placement are as before",
                         "was": v2, "now": {k: round(P[k], 4) for k in ("pend", "lamp", "fill") if k in P}, "mean_luma": round(mean, 2), "back_wall_box_mean_Y": round(box_mean_Y(path), 4) if gf else None,
                         "wash_ratio": WASH_RATIO if not gf else None, "fill_size_m": list(FILL_SIZE) if not gf else None, "render_s": dt}
    rec.setdefault("render_s", {})["night_lit"] = dt
    json.dump(rec, open(jp, "w"), indent=1)
    return time.time() - t0


if __name__ == "__main__":
    if "--relight-v3" in sys.argv:
        args = [a for a in sys.argv[1:] if not a.startswith("--")]
        relight_v3(args[0], args[1] if len(args) > 1 else T.ROOMS, samples=int(args[2]) if len(args) > 2 else 24)
        sys.exit(0)
    if "--rebake-lit" in sys.argv:
        args = [a for a in sys.argv[1:] if not a.startswith("--")]
        rebake_lit(args[0], args[1] if len(args) > 1 else T.ROOMS, samples=int(args[2]) if len(args) > 2 else 24)
        sys.exit(0)
    rid = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(T.ROOMS)
    samples = int(sys.argv[3]) if len(sys.argv) > 3 else 48
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    quick = "--quick" in sys.argv
    sts = tuple(a.split("=")[1].split(",") for a in sys.argv if a.startswith("--states="))
    render_room(rid, out, samples=samples, scale=scale, quick=quick, states=sts[0] if sts else RENDER_ORDER)
