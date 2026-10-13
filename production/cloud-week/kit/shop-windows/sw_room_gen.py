"""The rooms of the shops built after Rita's (batch A, 13 October 2026): the same room rule, the same Cycles render, the same three pictures, with the fixtures and goods read from target.json (`shops[<id>].room`).

`GRoom` is `sw_room.Room` (its materials, model templates, placement, camera and render are kept as they were, so Rita's room is untouched) with a shell, lights and calibration driven by the target's
colours, tubes and floor, and the building blocks every shop's layout is made from: the back-wall shelf unit, the counter, the drawer wall, the pegboard that tools hang flat on (rows by family, thin side
to the wall: Rita's lesson 10), the gantry and the racks. A shop's own layout is one function (`layout_ironmonger`, ...), which reads the fixture rectangles and goods counts from the target and states, in
words in its docstring, every choice the target left open (each is a Judgement in NOTES.md).

Room frame (the recipe's, as Rita's): x across, 0 at the card's centre, +x the PICTURE's right (the viewer's right); y back from the card (the front plane) to the back wall at D; z up from the box floor.
Stand-off rules (target method.standoff_rules_m): shelf goods on the back wall 0.30, furniture at the back wall 0.60, a side wall's relief 0.10 (flat 0.05), floor and ceiling 0.025 (0.05 tolerated).
"""
import json
import math
import os
import random
import re
import shutil
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Vector, Matrix, Euler  # noqa: E402
import sw_assets as A  # noqa: E402
import sw_room as S  # noqa: E402
import sw_gen as GEN  # noqa: E402
from sw_gen import GM  # noqa: E402

W, H, D = S.W, S.H, S.D
rgb8 = S.rgb8


def _rgb(text):
    m = re.search(r"\((\d+),\s*(\d+),\s*(\d+)\)", text)
    return tuple(int(v) for v in m.groups())


def _lin(v):
    v = np.asarray(v, np.float32) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def tex_mean_lin(asset):
    """The mean linear colour of a Poly Haven texture's diffuse map."""
    d = os.path.join(A.POLY, asset, "1k", "textures")
    f = next(os.path.join(d, x) for x in sorted(os.listdir(d)) if "_diff_" in x)
    a = np.asarray(Image.open(f).convert("RGB").resize((128, 128))).astype(np.float32)
    return _lin(a).reshape(-1, 3).mean(axis=0)


class GRoom(S.Room):
    BOARD_T = S.BOARD_T

    def __init__(self, work, ctx, seed=7):
        A.set_shop(ctx.id)
        T = A.load_target()
        super().__init__(work, T, seed)
        self.ctx = ctx
        self.RR = self.R["room"]
        self.fxd = {f["id"]: f for f in self.RR["fixtures"]}
        self.rows = {}                  # per board: row tag -> {z_top, n, span, y0, y1} (for the checks)
        self.notes = []                 # what the layout decided (written to placed.json's sibling for NOTES.md)
        self.count_left = {}
        for g in self.RR["goods"]:
            self.count_left[g["model"]] = self.count_left.get(g["model"], 0) + g["n"]
        self.subs = {}

    # ------------------------------------------------------------------------------------------------ bookkeeping
    def fixture_rec(self, fid, name, ext, **kw):
        rec = {"fixture": fid, "name": name, "ext": [round(v, 4) for v in ext]}
        rec.update(kw)
        self.fixtures.append(rec)

    def placed_rec(self, fid, model, ext, objs, scale=1.0, tag=None, **kw):
        rec = {"fixture": fid, "model": model, "ext": [round(float(v), 4) for v in ext], "scale": round(scale, 4), "rot_deg": [0.0, 0.0, 0.0], "objs": list(objs), "tag": tag, "clock": None}
        rec.update(kw)
        self.placed.append(rec)

    def sub_template(self, asset, tag, pred):
        """A model's meshes filtered by name (the bins' clean and rust variants are two sets of meshes in one glTF), registered as its own template `asset#tag`."""
        key = "%s#%s" % (asset, tag)
        if key in self.templates:
            return key
        meshes, lo, hi = self.template(asset)
        keep = [m for m in meshes if pred(m.name)]
        pts = [m.matrix_world @ Vector(c) for m in keep for c in m.bound_box]
        lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        self.templates[key] = (keep, lo, hi)
        return key

    # ------------------------------------------------------------------------------------------------ the shell
    def floor_material(self):
        rr = self.RR
        asset = re.search(r"Poly Haven ([a-z0-9_]+)", rr["floor"]["material"]).group(1)
        base = rr["floor"]["base"]
        mean = tex_mean_lin(asset)
        tgt = _lin(base)
        tint = tuple(float(v) for v in np.clip(tgt / np.maximum(mean, 1e-3), 0.05, 1.6))
        k = max(t * m for t, m in zip(tint, mean))
        if k > 0.85:
            tint = tuple(t * 0.85 / k for t in tint)
        kind = {"tea_rooms": "chequer", "newsagent": "tiles"}.get(self.ctx.id, "boards")
        m = self.texmat("floor_" + self.ctx.id, asset, 1.2 if kind == "boards" else 0.6, tint)
        if kind in ("chequer", "tiles"):
            # a 300 mm chequer (the target's "cream and brown 300 mm" / "grey and blue vinyl tile 300 mm"): a checker node's two colours times the texture's grain (its mean taken out)
            nt = m.node_tree
            p = nt.nodes["Principled BSDF"]
            link = [l for l in nt.links if l.to_socket == p.inputs["Base Color"]][0]
            grain_src = None
            # the texmat's Multiply node (diffuse x tint) is replaced: grain = diffuse / its mean, then x the checker colour
            geo = nt.nodes.new("ShaderNodeNewGeometry")
            chk = nt.nodes.new("ShaderNodeTexChecker")
            chk.inputs["Scale"].default_value = 1.0 / 0.3
            c1, c2 = ((rgb8(*(176, 156, 118)), rgb8(*(110, 74, 46))) if kind == "chequer" else (rgb8(*(118, 120, 124)), rgb8(*(64, 82, 122))))
            chk.inputs["Color1"].default_value = (*c1, 1.0)
            chk.inputs["Color2"].default_value = (*c2, 1.0)
            nt.links.new(geo.outputs["Position"], chk.inputs["Vector"])
            mix = nt.nodes.new("ShaderNodeMix")
            mix.data_type = "RGBA"
            mix.blend_type = "MULTIPLY"
            mix.inputs[0].default_value = 1.0
            nt.links.new(chk.outputs["Color"], mix.inputs[6])
            gain = nt.nodes.new("ShaderNodeMix")
            gain.data_type = "RGBA"
            gain.blend_type = "MULTIPLY"
            gain.inputs[0].default_value = 1.0
            gain.inputs[7].default_value = (*(float(1.0 / max(v, 1e-3)) for v in mean), 1.0)
            nt.links.new(link.from_node.inputs[6].links[0].from_socket, gain.inputs[6])        # the diffuse texture's colour
            nt.links.new(gain.outputs[2], mix.inputs[7])
            nt.links.new(mix.outputs[2], p.inputs["Base Color"])
        return m

    def shell(self):
        rr = self.RR
        wall_rgb = _rgb(rr["walls"]["above"])
        dado_rgb = _rgb(rr["walls"]["dado"])
        self.dado_top = float(re.search(r"to z ([0-9.]+)", rr["walls"]["dado"]).group(1))
        ceil_rgb = _rgb(rr["ceiling"])
        pm = tex_mean_lin("painted_plaster_wall")

        def tint_for(rgb):
            t = _lin(rgb) / np.maximum(pm, 1e-3)
            k = float((t * pm).max())
            if k > 0.82:
                t = t * 0.82 / k
            return tuple(float(v) for v in np.clip(t, 0.02, 1.6))
        self.floor_m = self.floor_material()
        wall_m = self.texmat("plaster_wall", "painted_plaster_wall", 1.5, tint_for(wall_rgb))
        dado_m = self.texmat("plaster_dado", "painted_plaster_wall", 1.5, tint_for(dado_rgb))
        ceil_m = self.mat("ceiling", rgb8(*ceil_rgb), rough=0.9)
        self.wall_m, self.dado_m = wall_m, dado_m
        self.box("floor", -W / 2, W / 2, 0, D, -0.02, 0.0, self.floor_m)
        self.box("ceiling", -W / 2, W / 2, 0, D, H, H + 0.02, ceil_m)
        dt = self.dado_top
        for sgn, nm in ((-1, "left"), (1, "right")):
            x0, x1 = (-W / 2 - 0.1, -W / 2) if sgn < 0 else (W / 2, W / 2 + 0.1)
            self.box("wall_%s_dado" % nm, x0, x1, 0, D, 0.0, dt, dado_m)
            self.box("wall_%s_up" % nm, x0, x1, 0, D, dt, H, wall_m)
        self.box("wall_back_dado", -W / 2, W / 2, D, D + 0.1, 0.0, dt, dado_m)
        self.box("wall_back_up", -W / 2, W / 2, D, D + 0.1, dt, H, wall_m)
        # ceiling battens (T12 in slim fittings): fitting 0.010 + opal diffuser 0.015 = 0.025 below the ceiling (as Rita's)
        lt = rr["lights"]
        self.tube_len = lt.get("tube_length_m", 1.5)
        self.diff_m = self.mat("tube_diffuser", rgb8(172, 174, 168), rough=0.5, emit=(0.95, 0.97, 1.0), emit_strength=0.0)
        fit_m = self.mat("batten_fitting", rgb8(190, 188, 180), rough=0.5)
        self.tube_objs = []
        hl = self.tube_len / 2.0
        cid = next(f["id"] for f in rr["fixtures"] if f["kind"] == "light")
        for k, t in enumerate(lt["tubes"]):
            self.box("batten_%d" % k, t["x"] - hl - 0.03, t["x"] + hl + 0.03, t["y"] - 0.06, t["y"] + 0.06, H - 0.010, H, fit_m, fixture=cid)
            o = self.box("tube_%d" % k, t["x"] - hl, t["x"] + hl, t["y"] - 0.045, t["y"] + 0.045, H - 0.025, H - 0.010, self.diff_m, fixture=cid)
            self.tube_objs.append(o)
        self.shelf_m = self.mat("shelf", rgb8(150, 108, 70), rough=0.55)
        self.upright_m = self.mat("upright", rgb8(120, 84, 54), rough=0.6)
        self.wood_m = self.mat("counter_wood", rgb8(96, 58, 34), rough=0.42)
        self.brass_m = self.mat("brass", rgb8(160, 120, 55), rough=0.3, metal=1.0)

    # ------------------------------------------------------------------------------------------------ lights, states, calibration, pictures
    def lights(self):
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
            return o
        self.L_day = area("daylight", (0.0, -0.04, H / 2), (math.pi / 2, 0.0, 0.0), W, H, (0.96, 0.97, 1.0))
        self.L_tube = []
        for k, t in enumerate(self.RR["lights"]["tubes"]):
            self.L_tube.append(area("tube_light_%d" % k, (t["x"], t["y"], H - 0.03), (0.0, 0.0, 0.0), self.tube_len, 0.09, (1.0, 0.89, 0.76)))
        self.L_sod = area("sodium", (0.0, -0.04, H * 0.9), (math.pi / 2 - 0.3, 0.0, 0.0), W, 0.5, (1.0, 0.25, 0.0))
        self.sodium_rgb = tuple(self.L_sod.data.color)
        self.L_back = None

    def set_state(self, state, P):
        tube_w = P["tube"]
        for o in self.L_tube:
            o.data.energy = tube_w if state in ("day", "night_lit") else 0.0
        self.L_day.data.energy = P["day"] if state == "day" else 0.0
        self.L_sod.data.energy = P["sodium_ratio"] * tube_w * len(self.L_tube) if state == "night_dark" else 0.0
        em = P["diff_emit"] if state in ("day", "night_lit") else 0.0
        self.diff_m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = em
        if getattr(self, "pilot", None) is not None:
            self.pilot.data.energy = P.get("pilot", 0.0) if state == "night_dark" else 0.0

    def calibrate(self, work, log=print, res=(768, 348), samples=24):
        """Light strengths so each state's mean luma meets the approved pictures' (119.5, 79.8, 17.7): the tubes on night_lit, the sky on day, the sodium wash on night_dark."""
        P = dict(S.DEFAULT_P)
        P["sodium_ratio"] = 0.12
        tmp = os.path.join(work, "cal.png")
        tgt_mean = S.TARGET_MEAN

        def measure(state):
            self.set_state(state, P)
            self.render(tmp, samples, res)
            return S.luma_stats(tmp)

        def tune(key, state, lo_hi=(1e-3, 1e5), iters=4):
            for _ in range(iters):
                m = measure(state)
                tgt = tgt_mean[state]
                log("   calibrate %s: %s=%.4g -> mean %.1f (target %.1f)" % (state, key, P[key], m, tgt))
                if abs(m - tgt) / tgt < 0.03:
                    break
                f = (tgt / max(m, 1.0)) ** 2.2
                P[key] = float(np.clip(P[key] * f, *lo_hi))
            return P[key]
        tune("tube", "night_lit")
        tune("day", "day")
        tune("sodium_ratio", "night_dark", lo_hi=(1e-4, 5.0))
        P["measured"] = {s: measure(s) for s in S.STATES}
        json.dump(P, open(os.path.join(work, "light_params.json"), "w"), indent=1)
        return P

    def render_states(self, work, P, out_dir, samples=128, res=S.PIX, states=S.STATES, log=print):
        os.makedirs(out_dir, exist_ok=True)
        name = self.ctx.picture_name
        times = {}
        record = {"shop": name, "w": W, "h": H, "d": D, "camera_d": S.CAM_D, "pixels": list(res), "states": {}, "made_by": "production/cloud-week/kit/shop-windows/build_shop.py (sw_room_gen.py)", "samples": samples,
                  "highlight_rolloff": S.ROLLOFF}
        raw_dir = os.path.join(out_dir, "raw")
        os.makedirs(raw_dir, exist_ok=True)
        record["pre_shoulder_burnt_share"] = {}
        for s in states:
            self.set_state(s, P)
            path = os.path.join(out_dir, "%s_%s.png" % (name, s))
            t0 = time.time()
            self.render(path, samples, res)
            raw_path = os.path.join(raw_dir, "%s_%s_raw.png" % (name, s))
            shutil.copyfile(path, raw_path)
            raw = np.asarray(Image.open(raw_path).convert("RGB"))
            record["pre_shoulder_burnt_share"][s] = round(float((raw.max(axis=2) >= 250).mean()), 5)
            S.rolloff(path)
            times[s] = round(time.time() - t0, 1)
            record["states"][s] = os.path.basename(path)
            log("render %s: %.0f s, mean luma %.1f, burnt share before the shoulder %.4f" % (s, times[s], S.luma_stats(path), record["pre_shoulder_burnt_share"][s]))
        for s in S.STATES:
            record["states"].setdefault(s, "%s_%s.png" % (name, s))
        json.dump(record, open(os.path.join(out_dir, "%s.json" % name), "w"), indent=1)
        return times

    # ------------------------------------------------------------------------------------------------ fixtures: the building blocks
    def shelf_unit(self, fid, tiers, depth=None, bottom=0.0):
        """The back-wall shelf unit: `tiers` = [(z of the board's TOP, x from, x to), ...]. A board is 25 mm; an upright (30 mm square) stands at every board's two ends from the floor (or `bottom`) to
        the highest board's top, so no board runs through one (a shelf stops at the upright's face: SO-07). Registers the fixtures. Returns the boards' records."""
        f = self.fxd[fid]
        depth = depth or f["depth_m"]
        recs = []
        xs = sorted({x for (_, a, b) in tiers for x in (a, b)})
        xmin, xmax = xs[0], xs[-1]
        ztop = max(z for z, _, _ in tiers)
        for x in (xmin, xmax):
            self.box("upright_%s_%.2f" % (fid, x), x - 0.015, x + 0.015, D - depth, D - 0.005, bottom, ztop, self.upright_m, fixture=fid)
        for z, a, b in tiers:
            for x in (a, b):
                if xmin < x < xmax:          # a board that begins inside the run stands on a post that stops under it
                    self.box("post_%s_%.2f_%.2f" % (fid, x, z), x - 0.015, x + 0.015, D - depth, D - 0.005, bottom, z - self.BOARD_T, self.upright_m, fixture=fid)
            aa = a + 0.015
            bb = b - 0.015
            self.box("shelf_%s_%.2f_%.2f_%.2f" % (fid, z, a, b), aa, bb, D - depth, D - 0.005, z - self.BOARD_T, z, self.shelf_m, fixture=fid)
            recs.append({"z": z, "x": (aa, bb), "depth": depth})
        return recs

    def counter(self, fid, x0=None, x1=None, top_h=None):
        f = self.fxd[fid]
        x0 = f["x"][0] if x0 is None else x0
        x1 = f["x"][1] if x1 is None else x1
        dep = f["depth_m"]
        h = f["z"][1] if top_h is None else top_h
        cy0 = D - dep
        self.box("counter_%s_base" % fid, x0, x1, cy0, D - 0.005, 0.0, h - 0.03, self.wood_m, fixture=fid)
        top = self.mat("counter_top_" + self.ctx.id, rgb8(120, 80, 48), rough=0.38)
        self.box("counter_%s_top" % fid, x0, x1, cy0, D - 0.005, h - 0.03, h, top, fixture=fid)
        self.counter_ext = (x0, x1, cy0, D - 0.005, h)
        return x0, x1, cy0, D - 0.005, h

    def pegboard_panels(self, fid, side):
        """Pegboard on a side wall over the fixture's y and z range: panels 0.95 x 0.85 with a 40 mm batten between, 8 to 20 mm off the wall; the board and the tools together stay under 0.10."""
        f = self.fxd[fid]
        y0, y1 = f["y"]
        z0, z1 = f["z"]
        peg = self.image_mat("pegboard", os.path.join(self.tex, "pegboard.png"), tile_m=0.6, rough=0.8)
        batt = self.mat("batten", rgb8(120, 90, 60), rough=0.7)
        xw = -W / 2 if side == "left" else W / 2
        nY = max(1, int(round((y1 - y0) / 0.95)))
        nZ = max(1, int(round((z1 - z0) / 0.85)))
        ys = np.linspace(y0, y1, nY + 1)
        zs = np.linspace(z0, z1, nZ + 1)
        for i in range(nY):
            for j in range(nZ):
                if side == "left":
                    self.box("%s_peg_%d_%d" % (side, i, j), xw + 0.012, xw + 0.02, ys[i] + 0.004, ys[i + 1] - 0.004, zs[j] + 0.004, zs[j + 1] - 0.004, peg, fixture=fid)
                else:
                    self.box("%s_peg_%d_%d" % (side, i, j), xw - 0.02, xw - 0.012, ys[i] + 0.004, ys[i + 1] - 0.004, zs[j] + 0.004, zs[j + 1] - 0.004, peg, fixture=fid)
        for k in (0, nY):
            ya = ys[k] if k == 0 else ys[k] - 0.04
            if side == "left":
                self.box("%s_batten_%d" % (side, k), xw, xw + 0.012, ya, ya + 0.04, z0, z1, batt, fixture=fid)
            else:
                self.box("%s_batten_%d" % (side, k), xw - 0.012, xw, ya, ya + 0.04, z0, z1, batt, fixture=fid)
        return xw + 0.02 if side == "left" else xw - 0.02

    def make_pegboard_texture(self):
        n = 1024
        rng = np.random.default_rng(3)
        base = np.zeros((n, n, 3), np.float32)
        base[:] = (150, 112, 72)
        base += rng.normal(0, 5, (n, 1, 1)).astype(np.float32) + rng.normal(0, 3, (n, n, 1)).astype(np.float32)
        pitch = n / 24.0
        yy, xx = np.mgrid[0:n, 0:n]
        hole = (((xx % pitch) - pitch / 2) ** 2 + ((yy % pitch) - pitch / 2) ** 2) < (pitch * 0.17) ** 2
        base[hole] = (34, 24, 16)
        Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).save(os.path.join(self.tex, "pegboard.png"))

    def hang_tools(self, fid, side, items, y_range, z_range, gap=(0.04, 0.06), max_off=0.10, margin=0.03, tag_prefix="R", min_scale=0.75, tall=0.6):
        """Hang tools flat on a pegboard in ROWS (Rita's lesson 10): each tool turned so its thinnest side is against the board (and, by `orient`, its long side along the wall 'h' or up it 'v'), at 1.0 of its
        size, or smaller (never below `min_scale`) where a thick one would stand more than `max_off` off the wall with the board; the tall ones (taller than `tall`: the brooms) hang in columns from the two
        ends, the rest in rows across what is left, filled in order of height so the rows are of one height, each row's tools hung from one line (their tops level), gaps `gap`, each row centred.
        `items` = [(asset, count, orient), ...]. Returns the rows' records."""
        rnd = self.rnd
        t_front = (-W / 2 + 0.02) if side == "left" else (W / 2 - 0.02)
        tools = []
        for asset, count, orient in items:
            for _ in range(count):
                d0 = self.dims(asset)
                order = sorted(range(3), key=lambda i: (d0.x, d0.y, d0.z)[i])
                thin = order[0]
                rot = {0: (0, 0, 0), 1: (0, 0, math.radians(-90)), 2: (0, math.radians(-90), 0)}[thin]
                d1 = self.dims(asset, rot)
                long_is_y = d1.y >= d1.z
                if (orient == "h") != long_is_y:
                    qm = Matrix.Rotation(math.radians(90.0), 3, "X") @ Euler(rot, "XYZ").to_matrix()
                    rot = tuple(qm.to_euler("XYZ"))
                d2 = self.dims(asset, rot)
                s_ = min(1.0, (max_off - 0.02 - 0.004) / d2.x)
                if s_ < min_scale - 1e-9:
                    self.notes.append("%s does not hang flat within %.2f of the wall (needs %.3f): left off %s" % (asset, max_off, d2.x, fid))
                    continue
                tools.append({"asset": asset, "rot": rot, "s": s_, "w": d2.y * s_, "h": d2.z * s_})
        y_lo, y_hi = y_range[0] + margin, y_range[1] - margin
        anc = ("max", "c", "c") if side == "right" else ("min", "c", "c")
        talls = [t for t in tools if t["h"] > tall]
        rest = [t for t in tools if t["h"] <= tall]
        # the tall ones in columns at the two ends (alternately), hung from the board's top line
        z_top0 = z_range[1] - 0.02
        recs = []
        ya, yb = y_lo, y_hi
        for i, t in enumerate(talls):
            if i % 2 == 0:
                yc = ya + t["w"] / 2
                ya += t["w"] + 0.05
            else:
                yc = yb - t["w"] / 2
                yb -= t["w"] + 0.05
            self.place(t["asset"], (t_front, yc, z_top0 - t["h"] / 2), rot=t["rot"], scale=t["s"], fixture=fid, anchor=anc, tag="%sC%d" % (tag_prefix, i + 1))
        if talls:
            recs.append({"tag": "%sC" % tag_prefix, "z_top": z_top0, "n": len(talls), "span": round(sum(t["w"] for t in talls), 3), "columns": True})
        width = yb - ya
        rest.sort(key=lambda t: -t["h"])
        rows = []
        for t in rest:
            if rows and rows[-1]["w"] + t["w"] + gap[1] <= width:
                rows[-1]["tools"].append(t)
                rows[-1]["w"] += t["w"] + gap[1]
            else:
                rows.append({"tools": [t], "w": t["w"]})
        for r_ in rows:
            r_["h"] = max(t["h"] for t in r_["tools"])
        z = z_top0
        for k, r_ in enumerate(rows):
            if z - r_["h"] < z_range[0] - 0.12:
                self.notes.append("%s: %d tools do not fit the board's rows and are left off" % (fid, sum(len(x["tools"]) for x in rows[k:])))
                break
            gaps = [rnd.uniform(*gap) for _ in range(len(r_["tools"]) - 1)]
            total = sum(t["w"] for t in r_["tools"]) + sum(gaps)
            y = ya + (width - total) / 2.0
            tag = "%s%d" % (tag_prefix, k + 1)
            n = 0
            r_["tools"].sort(key=lambda t: rnd.random())
            gaps = [rnd.uniform(*gap) for _ in range(len(r_["tools"]) - 1)]
            total = sum(t["w"] for t in r_["tools"]) + sum(gaps)
            y = ya + (width - total) / 2.0
            for i, t in enumerate(r_["tools"]):
                self.place(t["asset"], (t_front, y + t["w"] / 2, z - t["h"] / 2), rot=t["rot"], scale=t["s"], fixture=fid, anchor=anc, tag=tag)
                n += 1
                y += t["w"] + (gaps[i] if i < len(gaps) else 0.0)
            recs.append({"tag": tag, "z_top": z, "n": n, "span": round(total, 3), "region": [round(ya, 3), round(yb, 3)]})
            z -= r_["h"] + rnd.uniform(0.05, 0.08)
        self.rows[fid] = recs
        return recs

    # ------------------------------------------------------------------------------------------------ the tins, drums and drawers (scripts)
    def tin_materials(self):
        if hasattr(self, "_tin_m"):
            return self._tin_m
        path = os.path.join(self.tex, "tin_labels.png")
        self.tin_uv = GEN.tin_labels(path)
        label = self.image_mat("tin_label", path, rough=0.5)
        metal = self.mat("tin_metal", rgb8(168, 168, 164), rough=0.35, metal=0.85)
        self._tin_m = (metal, label)
        return self._tin_m

    def tin_stack(self, cx, cy, z, tins, fid, labels, tag="tins", n=18):
        """A vertical stack of upright tins at (cx, cy) on a surface at z: `tins` = [(radius, height), ...] from the bottom; one mesh. A tin: a recessed lid with a rolled rim, the body, a chime; the label strip
        on the body (an index into the label atlas). Returns the extents."""
        metal, label = self.tin_materials()
        gm = GM()
        zz = 0.0
        for (r, h), lb in zip(tins, labels):
            prof = [(0.0, 0.0), (r * 0.94, 0.0), (r, 0.004), (r, h - 0.010), (r * 1.035, h - 0.010), (r * 1.035, h - 0.002), (r * 0.90, h - 0.002), (r * 0.90, h - 0.006), (0.0, h - 0.006)]
            gm.lathe(cx, cy, z + zz, prof, mi=0, n=n, label=(2, 3), mi_label=1, label_uv=self.tin_uv[lb % len(self.tin_uv)])
            zz += h
        ob = gm.to_object("tins_%s_%d" % (fid, len(self.placed)), [metal, label], self.sc)
        ext = gm.extents()
        self.placed_rec(fid, "script:paint_tins", ext, [ob.name], tag=tag, n=len(tins))
        return ext

    def drawer_wall(self, fid, label_texts):
        """The back wall's run of small drawers (script:drawer_fronts): a carcass 0.085 deep, 6 columns x 10 rows of flat fronts standing 0.015 proud, each with a brass label holder carrying a hand-lettered
        card and a brass ring pull. One carcass, one mesh of fronts, one of brass, one of labels."""
        f = self.fxd[fid]
        x0, x1 = f["x"]
        z0, z1 = f["z"]
        dep = f["depth_m"]
        carcass = self.mat("drawer_carcass", rgb8(86, 54, 34), rough=0.6)
        front_m = self.mat("drawer_front", rgb8(150, 104, 62), rough=0.55)
        cols, rowsn = 6, 10
        pw, ph = (x1 - x0) / cols, (z1 - z0) / rowsn
        yc = D - 0.075                       # the carcass's front face
        self.box("drawers_carcass", x0, x1, yc, D - 0.005, z0, z1, carcass, fixture=fid)
        gm_f, gm_b, gm_l = GM(), GM(), GM()
        path = os.path.join(self.tex, "drawer_labels.png")
        uvs = GEN.card_atlas(path, label_texts, cols=4, tile=(256, 96), size=40)
        lab_m = self.image_mat("drawer_labels", path, rough=0.8)
        yf = yc - 0.015                      # the fronts' face: 15 proud of the carcass
        for c in range(cols):
            for r in range(rowsn):
                xa, xb = x0 + c * pw + 0.004, x0 + (c + 1) * pw - 0.004
                za, zb = z0 + r * ph + 0.004, z0 + (r + 1) * ph - 0.004
                gm_f.box(xa, xb, yf, yc, za, zb, 0)
                xm = (xa + xb) / 2
                zl = zb - 0.040
                gm_b.box(xm - 0.036, xm + 0.036, yf - 0.0035, yf, zl - 0.014, zl + 0.014, 0)            # the label holder (a brass frame)
                k = (c * rowsn + r) % len(label_texts)
                gm_l.box(xm - 0.033, xm + 0.033, yf - 0.0045, yf - 0.0035, zl - 0.011, zl + 0.011, 0, uv_front=uvs[k])
                gm_b.torus((xm, yf - 0.003, za + (zb - za) * 0.32), 0.011, 0.0016, 0, axis="y", nm=12, nn=5)    # the ring pull
        o1 = gm_f.to_object("drawer_fronts", [front_m], self.sc)
        o2 = gm_b.to_object("drawer_brass", [self.brass_m], self.sc)
        o3 = gm_l.to_object("drawer_labels", [lab_m], self.sc)
        ext = [x0, x1, yf - 0.0045, D - 0.005, z0, z1]
        self.fixture_rec(fid, "drawer_wall", ext)
        self.placed_rec(fid, "script:drawer_fronts", ext, [o1.name, o2.name, o3.name], tag="drawers", n=cols * rowsn)
        return ext

    # ------------------------------------------------------------------------------------------------ packing goods along a tier
    def fit_row(self, items, xa, xb, y_back, z, clear, deep, fid, tag, gap=(0.008, 0.02)):
        """Fill one tier left to right from `items` (a list of dicts: {"build": fn(xc, y_back, z) -> ext, "w": width, "h": height, "d": depth}): the next item that fits the clearance and the depth, never the
        same kind twice running when another fits. Returns (placed, remaining items)."""
        rnd = self.rnd
        x = xa + 0.01
        placed = 0
        left = list(items)
        last = None
        while True:
            cands = [(i, it) for i, it in enumerate(left) if it["h"] <= clear + 1e-9 and it["d"] <= deep + 1e-9 and x + it["w"] <= xb - 0.005]
            if not cands:
                break
            alt = [c for c in cands if c[1]["kind"] != last] or cands
            i, it = alt[0]
            it["build"](x + it["w"] / 2, y_back, z)
            last = it["kind"]
            left.pop(i)
            placed += 1
            x += it["w"] + rnd.uniform(*gap)
        return placed, left

    def ph_item(self, asset, rot=(0.0, 0.0, 0.0), scale=1.0, fid="", tag=None, size=None):
        d = self.dims(asset, rot)
        if size:
            scale = min(scale, size / max(d.x, d.y, d.z))
        w, dd, h = d.x * scale, d.y * scale, d.z * scale

        def build(xc, yb, z, asset=asset, rot=rot, scale=scale):
            return self.place(asset, (xc, yb, z), rot=rot, scale=scale, fixture=fid, anchor=("c", "max", "min"), tag=tag)
        return {"kind": asset, "w": w, "d": dd, "h": h, "build": build}

    def tins_item(self, n_tins, fid, kind="tins", sizes=((0.052, 0.098), (0.058, 0.128), (0.068, 0.178))):
        rnd = self.rnd
        r, h = rnd.choice(sizes)
        tins = [(r, h)] * n_tins
        labels = [rnd.randrange(16)] * n_tins

        def build(xc, yb, z, tins=tins, labels=labels):
            return self.tin_stack(xc, yb - r - 0.01, z, tins, fid, labels)
        return {"kind": kind, "w": 2 * r * 1.035, "d": 2 * r * 1.035 + 0.01, "h": h * n_tins, "build": build}


# ---------------------------------------------------------------------------------------------------------------------------------- the ironmonger
def layout_ironmonger(r):
    """The ironmonger's room (target `shops.ironmonger.room`: fixtures I-*, goods by name and count). What the target leaves open, and what this does (each a Judgement in NOTES.md):

    shelf unit I-back-shelves (x -0.45 to 2.6, 0.28 deep, tiers 0.4, 0.8, 1.2, 1.6, 1.95): the counter (x -0.45 to 1.15, 1.0 high) hides everything under 1.0 there and the floor goods stand in front of it
    to 1.1 at x 1.3 to 2.6, so the tiers at 0.4 and 0.8 are not seen from any camera and are not built; the tier at 1.2 runs where the till is not (x from 1.3: the till stands 0.42 high on the counter and
    would go through a board at 1.175); the tiers at 1.6 and 1.95 run the whole length. The goods go on the three tiers: the tins in stacks of one to three (the tier's clearance), then the oils, cleaners,
    bulbs (two open trays of six: `lightbulb_01 n 12 in a box`), the blowtorch and the drain cleaner.
    counter I-back-counter: the till (0.42 largest side, the target's size), the measuring tape, the two toolboxes and ONE of the three watering cans (a can is 0.45 deep with its spout: it fits no shelf and
    the counter has room for one; the display holds two). A brass rule is let into the top along its front edge.
    I-back-floor (x 1.3 to 2.6, 0.58 deep): the dustbins are one of the model's two variants (the glTF holds a clean and a rusted bin 1.85 m apart; the clean one) at 0.85 of its size (a galvanised dustbin
    of 1990 stood 0.6 to 0.7 high: the model's 0.906 is too big), three jerrycans of paraffin in a row in front of nothing, three cement bags at 0.75 stacked on the right (the model's bag is 0.70 long: at
    full size three would not stand in the run). The step ladder (0.96 x 0.50 x 1.34) fits nowhere in a 1.3 m run that also holds the bins and the bags: left out, named.
    pegboards I-left-pegboard, I-right-pegboard (2.4 x 1.2, z 0.7 to 1.9): the tools by rows (hang_tools). The target's counts are low for a 2.9 m2 board (33 hand tools; 17 garden pieces): both boards
    take the counts the rows need (written back to the target as 'counts placed'); the brooms hang at 0.84 so that broom and board stay under 0.10."""
    rr = r.RR
    fx = r.fxd
    rnd = r.rnd
    r.make_pegboard_texture()
    ctx_notes = r.notes
    cnt = r.count_left
    # ---- the drawer wall
    labels = ["NAILS 1\"", "NAILS 2\"", "NAILS 3\"", "SCREWS No 6", "SCREWS No 8", "SCREWS No 10", "HINGES", "WASHERS", "NUTS & BOLTS", "HOOKS", "RAWLPLUGS", "STAPLES", "TACKS",
              "FUSE WIRE", "BRASS CUP HOOKS", "PICTURE WIRE", "STRING", "SASH CORD", "PADLOCKS", "KEYS", "BOLTS", "CASTORS", "BRADS", "BEADING PINS"]
    r.drawer_wall("I-back-drawers", labels)
    # ---- the counter
    cx0, cx1, cy0, cy1, ch = r.counter("I-back-counter")
    rule = r.mat("brass_rule", rgb8(184, 150, 70), rough=0.28, metal=1.0)
    r.box("counter_rule", cx0 + 0.04, cx1 - 0.04, cy0 + 0.012, cy0 + 0.040, ch, ch + 0.002, rule, fixture="I-back-counter")
    # goods on the counter (back edge at the wall: the till stands at the right end, clear of the shelf tier at 1.6 above it: 0.62 + 1.0 = 1.62? the till is scaled to the target's 0.42)
    till_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "CashRegister_01") / max(r.dims("CashRegister_01"))
    e = r.place("CashRegister_01", (cx1 - 0.30, D - 0.09, ch), rot=(0, 0, 0), scale=till_s, fixture="I-back-counter", anchor=("c", "max", "min"))
    r.place("measuring_tape_01", (cx0 + 0.50, cy0 + 0.14, ch), rot=(0, 0, 0.5), scale=1.0, fixture="I-back-counter", anchor=("c", "c", "min"))
    x = cx0 + 0.02
    for k in range(2):
        d = r.dims("metal_toolbox")
        r.place("metal_toolbox", (x + d.x / 2, D - 0.02, ch), rot=(0, 0, 0), scale=1.0, fixture="I-back-counter", anchor=("c", "max", "min"))
        x += d.x + 0.04
    d = r.dims("watering_can_metal_01")
    r.place("watering_can_metal_01", (x + d.x / 2 + 0.01, D - 0.02, ch), rot=(0, 0, 0), scale=1.0, fixture="I-back-counter", anchor=("c", "max", "min"))
    ctx_notes.append("watering cans: 1 of the room's 3 on the counter (a can is 0.45 deep with its spout); the display holds 2")
    # ---- the shelf unit and its goods
    sh = fx["I-back-shelves"]
    x0s, x1s = sh["x"]
    tiers = [(1.95, x0s, x1s), (1.6, x0s, x1s), (1.2, 1.3, x1s)]
    r.shelf_unit("I-back-shelves", tiers)
    n_tin = next(g["n"] for g in rr["goods"] if g["model"] == "script:paint_tins")
    items = []
    # tins in stacks (the clearance of the tier decides the height: 1.6 -> 0.325, 1.95 -> 0.40, 1.2 -> 0.35)
    left = n_tin
    while left > 0:
        k = min(left, rnd.choice((1, 2, 2, 3)))
        items.append(r.tins_item(k, "I-back-shelves"))
        left -= k
    def ph(model, n, rot=(0.0, 0.0, 0.0), **kw):
        return [r.ph_item(model, rot, fid="I-back-shelves", **kw) for _ in range(n)]
    items += ph("oil_tin", cnt["oil_tin"])
    items += ph("small_oil_can_01", cnt["small_oil_can_01"])
    items += ph("cleaner_tin_01", cnt["cleaner_tin_01"])
    items += ph("drain_cleaner", cnt["drain_cleaner"])
    items += ph("brass_blowtorch", cnt["brass_blowtorch"], (0, 0, math.pi / 2))
    # the bulbs: two open cardboard trays of six, as one placed good each (script: box; lightbulb_01 x 12)
    for t in range(2):
        def bulb_tray(xc, yb, z, t=t):
            tray = r.mat("bulb_tray", rgb8(176, 150, 106), rough=0.85)
            gm = GM()
            tw, td = 0.19, 0.125
            gm.box(xc - tw / 2, xc + tw / 2, yb - td, yb, z, z + 0.004, 0)
            gm.box(xc - tw / 2, xc + tw / 2, yb - td, yb - td + 0.003, z, z + 0.028, 0)
            gm.box(xc - tw / 2, xc + tw / 2, yb - 0.003, yb, z, z + 0.028, 0)
            gm.box(xc - tw / 2, xc - tw / 2 + 0.003, yb - td, yb, z, z + 0.028, 0)
            gm.box(xc + tw / 2 - 0.003, xc + tw / 2, yb - td, yb, z, z + 0.028, 0)
            ob = gm.to_object("bulb_tray_%d" % t, [tray], r.sc)
            r.placed_rec("I-back-shelves", "script:bulb_tray", gm.extents(), [ob.name], tag="tray")
            for i in range(3):
                for j in range(2):
                    r.place("lightbulb_01", (xc - 0.06 + i * 0.06, yb - 0.04 - j * 0.05, z + 0.004), rot=(0, 0, 0), scale=1.0, fixture="I-back-shelves", anchor=("c", "c", "min"))
        items.append({"kind": "bulbs", "w": 0.19, "d": 0.125, "h": 0.105, "build": bulb_tray})
    # fill: the tall tier first so the bulky pieces go where there is room; each tier is filled left to right from what is left
    rnd.shuffle(items)
    for z, a, b in tiers:
        clear = {1.95: 0.40, 1.6: 0.325, 1.2: 0.35}[z]
        n, items = r.fit_row(items, a, b, D - 0.005, z, clear, 0.28 - 0.035, "I-back-shelves", "tier")
        r.fixtures.append({"fixture": "I-back-shelves", "name": "tier_fill_%.2f" % z, "ext": [a, b, D - 0.28, D - 0.005, z, z + 0.001], "n": n})
    if items:
        ctx_notes.append("shelves: %d pieces did not fit the three tiers: %s" % (len(items), sorted({i["kind"] for i in items})))
    # ---- I-back-floor
    fl = fx["I-back-floor"]
    fx0, fx1 = fl["x"]
    bin_key = r.sub_template("metal_trash_can", "clean", lambda n: "rust" not in n)
    bd = r.dims(bin_key)
    bs_ = 0.85
    e1 = r.place(bin_key, (fx0 + bd.x * bs_ / 2 + 0.02, D - 0.005, 0.0), rot=(0, 0, 0), scale=bs_, fixture="I-back-floor", anchor=("c", "max", "min"))
    jd = r.dims("metal_jerrycan_green", (0, 0, math.pi / 2))
    xj = e1[1] + 0.06
    for k in range(3):
        r.place("metal_jerrycan_green", (xj + jd.x / 2, D - 0.02, 0.0), rot=(0, 0, math.pi / 2), scale=1.0, fixture="I-back-floor", anchor=("c", "max", "min"))
        xj += jd.x + 0.02
    bag_s = 0.75
    bg = r.dims("cement_bag", (0, 0, 0))
    zz = 0.0
    for k in range(3):
        r.place("cement_bag", (fx1 - bg.x * bag_s / 2 - 0.01 + rnd.uniform(-0.01, 0.01), D - 0.005, zz), rot=(0, 0, rnd.uniform(-0.04, 0.04)), scale=bag_s, fixture="I-back-floor", anchor=("c", "max", "min"))
        zz += bg.z * bag_s
    ctx_notes.append("I-back-floor: the dustbins are the clean variant of the model's pair at 0.85; the cement bags at 0.75 (the model's bag is 0.70 long); the wooden step ladder is left out (it fits no part of a 1.3 m run that also holds the bins, the cans and the bags)")
    # ---- the pegboards (counts raised: see the docstring)
    left_items = [("handsaw_wood", 2, "h"), ("bolt_cutters_01", 1, "h"), ("crowbar_01", 1, "v"), ("cross_pein_hammer", 3, "v"), ("wooden_hammer_01", 2, "v"), ("pipe_wrench", 2, "v"), ("adjustable_wrench", 3, "v"),
                  ("combination_wrench", 5, "v"), ("pliers", 4, "v"), ("tongue_groove_pliers", 3, "v"), ("screwdriver", 6, "v"), ("flathead_screwdriver", 5, "v"), ("ratchet_wrench", 3, "v"), ("hatchet", 2, "v"), ("screwdrivers_02", 2, "v")]
    r.pegboard_panels("I-left-pegboard", "left")
    r.hang_tools("I-left-pegboard", "left", left_items, fx["I-left-pegboard"]["y"], fx["I-left-pegboard"]["z"])
    right_items = [("trowel_01", 8, "v"), ("garden_gloves_01", 8, "v"), ("dustpan", 4, "v"), ("mousetrap", 14, "v")]
    r.pegboard_panels("I-right-pegboard", "right")
    r.hang_tools("I-right-pegboard", "right", right_items, fx["I-right-pegboard"]["y"], fx["I-right-pegboard"]["z"], max_off=0.10)
    # the two wooden brooms hang on the wall itself past the end of the board (y 3.5 and 3.9): a broom's head is 0.113 thick, which on a board 0.02 off the wall would stand 0.137 out; at 0.82 and
    # hung on the wall it stands 0.093 (the side wall's tolerated 0.10)
    for k, yb in enumerate((3.55, 3.95)):
        r.place("wooden_broom", (W / 2 - 0.002, yb, 0.06), rot=(0, 0, math.radians(-90)), scale=0.82, fixture="I-right-pegboard", anchor=("max", "c", "min"), tag="broom")
    ctx_notes.append("the brooms (2 of the room's pieces on the right wall) hang on the wall past the board's end at 0.82: the head is 0.113 thick")
    # a door mat? the target gives none: not built


def _lazy(mod, fn):
    def f(r):
        m = __import__(mod)
        return getattr(m, fn)(r)
    return f


LAYOUTS = {"ironmonger": layout_ironmonger, "newsagent": _lazy("sw_shops_news", "room"), "tea_rooms": _lazy("sw_shops_tea", "room")}


def build_scene(work, ctx):
    r = GRoom(work, ctx)
    r.shell()
    LAYOUTS[ctx.id](r)
    r.lights()
    r.camera()
    return r
