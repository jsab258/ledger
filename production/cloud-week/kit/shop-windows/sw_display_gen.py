"""The near metre (target section 4.5 of each shop's row) as real meshes in one glb, for the shops built after Rita's (batch A, 13 October 2026).

Local frame (Rita's): x along the window, + to the viewer's right, centred on the window zone (3.35 m); y back from the glass; z up from the bed (the stallriser's top, 0.60 above the footway). The target's
table gives each model a zone (u from the window zone's viewer-left edge, v out from the back of the glass, w above the bed); the zones of a shop overlap in volume (Rita's close review found the same in
hers), so each layout below places every piece at an explicit (u, v, w) that is inside or beside its zone and stands on a surface of the display (the bed, a crate or a hung card); what moved and why is
named in the layout's docstring and in NOTES.md.

A bed (a painted timber board, the stallriser's top level), a return wall at each end of the window zone (plaster above the room's dado line, the dado below: the room's own colours, from the target) so that
from CLOSE_35_B the glass shows a wall and not the gap beside the card (Rita's close fault 3), and the goods. Nothing floats: a hung card hangs on four cords from the window head.
13 October lessons kept: no pedestals under goods (every piece stands on a surface that exists), nothing through anything (DSP-03), every piece readable from the street (DSP-03 asks the front row from
STREET_SQUARE), real geometry, no alpha cut-outs, textures 512 px, a 4 mm bevel on a stand.
"""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402
import sw_assets as A  # noqa: E402
import sw_room as S  # noqa: E402
import sw_room_gen as RG  # noqa: E402
import sw_gen as GEN  # noqa: E402
from sw_gen import GM  # noqa: E402

TRIS = 4500
DEPTH = 0.55
WALL_Z = (-0.05, 2.35)
CARD_PLANE_LOCAL_Y = 0.605
rgb8 = S.rgb8


class GDisplay(RG.GRoom):
    shadow_trick = False        # a glb carries the plain Principled glass (transmission 1, alpha 1), not the room's shadow-ray node tree

    def __init__(self, work, ctx):
        super().__init__(work, ctx)
        self.L = ctx.window_len
        self.groups = []                 # {"kind", "model", "tier", "objs"} for the checks
        self.items = []                  # {"model", "tier", "scale", "ext", "objs"}
        self.scripted = []
        self.structure = []
        self.rnd = random.Random(11)
        self.make_pegboard_texture()     # (the room's textures dir exists; the pegboard is not used here)

    # ---------------------------------------------------------------------------------------------- structure
    def struct(self, ob, kind, ext):
        self.structure.append({"kind": kind, "obj": ob.name, "ext": [round(float(v), 4) for v in ext]})
        return ob

    def solid(self, name, x0, x1, y0, y1, z0, z1, mat, kind, bevel=0.004):
        gm = GM()
        gm.box(x0, x1, y0, y1, z0, z1, 0)
        ob = gm.to_object(name, [mat], self.sc)
        if bevel:
            md = ob.modifiers.new("bevel", "BEVEL")
            md.width = min(bevel, 0.45 * min(x1 - x0, y1 - y0, z1 - z0))
            md.segments = 2
            md.limit_method = "ANGLE"
            md.angle_limit = math.radians(30.0)
        self.box_uvs(ob, getattr(self, "uv_tile", 0.25))
        self.struct(ob, kind, [x0, x1, y0, y1, z0, z1])
        return ob

    @staticmethod
    def box_uvs(ob, tile_m=0.25):
        me = ob.data
        bm = bmesh.new()
        bm.from_mesh(me)
        layer = bm.loops.layers.uv.verify()
        mw = ob.matrix_world
        for f in bm.faces:
            n = mw.to_3x3() @ f.normal
            ax = max(range(3), key=lambda i: abs(n[i]))
            for l in f.loops:
                c = mw @ l.vert.co
                uv = (c.x, c.z) if ax == 1 else ((c.y, c.z) if ax == 0 else (c.x, c.y))
                l[layer].uv = (uv[0] / tile_m, uv[1] / tile_m)
        bm.to_mesh(me)
        bm.free()

    def start(self, bed_rgb, wall_rgb, dado_rgb, bed_png=None, board_png=None):
        """`bed_png` / `board_png` (try 2, 14 Oct): the painted top of the bed and the bed's timber edge as pictures (a painted plywood, a bare deal) in place of a flat base-colour factor."""
        L = self.L
        if bed_png:
            bed_m = self.image_mat("bed_paint", bed_png, rough=0.62)
            board_m = self.image_mat("bed_board", board_png, rough=0.7) if board_png else self.mat("bed_board", rgb8(70, 44, 28), rough=0.7)
            self.uv_tile = 0.8
        else:
            bed_m = self.mat("bed_paint", rgb8(*bed_rgb), rough=0.62)
            board_m = self.mat("bed_board", rgb8(70, 44, 28), rough=0.7)
        self.bed_top = bed_m
        self.solid("bed", -L / 2, L / 2, 0.0, DEPTH, -0.026, -0.006, board_m, "bed", bevel=0.0)
        self.solid("bed_top", -L / 2 + 0.01, L / 2 - 0.01, 0.01, DEPTH - 0.01, -0.006, 0.0, bed_m, "bed_top", bevel=0.0)
        self.uv_tile = 0.25
        plaster = self.mat("return_plaster", rgb8(*wall_rgb), rough=0.9)
        dado = self.mat("return_dado", rgb8(*dado_rgb), rough=0.9)
        ya, yb = -0.005, CARD_PLANE_LOCAL_Y
        dado_top = 0.95
        for side, (xa, xb) in (("l", (-L / 2 - 0.01, -L / 2)), ("r", (L / 2, L / 2 + 0.01))):
            self.solid("return_wall_%s_dado" % side, xa, xb, ya, yb, WALL_Z[0], dado_top, dado, "return_wall", bevel=0.0)
            self.solid("return_wall_%s_plaster" % side, xa, xb, ya, yb, dado_top, WALL_Z[1], plaster, "return_wall", bevel=0.0)

    def tone(self, obj_names, k):
        """Scale the base-colour image of the materials of the named objects by `k` in the image's own (sRGB) values, clipped, once per image: k under 1 takes the white out of a model that burns under
        the gate's night spill (the tea room's white chairs: PIC-05g), k over 1 lifts a model that reads dark against the room (the walnut table: LIT-08). The model's own texture is changed (CC0)."""
        import numpy as _np
        done = self.__dict__.setdefault("_toned", set())
        for nm in obj_names:
            ob = bpy.data.objects.get(nm)
            if ob is None:
                continue
            for sl in ob.material_slots:
                m = sl.material
                if not m or not m.use_nodes:
                    continue
                pb = m.node_tree.nodes.get("Principled BSDF")
                if pb is None or not pb.inputs["Base Color"].links:
                    continue
                src = pb.inputs["Base Color"].links[0].from_node
                if src.type in ("MIX", "MIX_RGB"):                  # (14 Oct) the importer multiplies a model's picture by its colour factor through a Mix node (the grocer's red crates): follow it to the picture
                    for inp_ in src.inputs:
                        if inp_.is_linked and inp_.links[0].from_node.type == "TEX_IMAGE":
                            src = inp_.links[0].from_node
                            break
                if src.type != "TEX_IMAGE" or src.image is None or src.image.name in done:
                    continue
                im = src.image
                done.add(im.name)
                a = _np.empty(len(im.pixels), dtype=_np.float32)
                im.pixels.foreach_get(a)
                a = a.reshape(-1, 4)
                a[:, :3] = _np.clip(a[:, :3] * k, 0.0, 1.0)
                im.pixels.foreach_set(a.reshape(-1))
                im.update()

    def tone_metal(self, obj_names, f):
        """Scale the metallic channel (blue of the ARM picture) of the named objects' materials by `f` once per image: a brass or black-iron model whose metal reflects only a dark night room reads as black
        against the lit room behind it (the chandler's storm lanterns: LIT-08 0.32 to 0.45 with their base colour lifted 2 times); f under 1 lets the diffuse colour show. The model's own texture is changed (CC0)."""
        import numpy as _np
        done = self.__dict__.setdefault("_metal_toned", set())
        for nm in obj_names:
            ob = bpy.data.objects.get(nm)
            if ob is None:
                continue
            for sl in ob.material_slots:
                m = sl.material
                if not m or not m.use_nodes:
                    continue
                pb = m.node_tree.nodes.get("Principled BSDF")
                if pb is None or not pb.inputs["Metallic"].links:
                    continue
                sep = pb.inputs["Metallic"].links[0].from_node
                if not sep.inputs or not sep.inputs[0].links:
                    continue
                src = sep.inputs[0].links[0].from_node
                if src.type != "TEX_IMAGE" or src.image is None or src.image.name in done:
                    continue
                im = src.image
                done.add(im.name)
                a = _np.empty(len(im.pixels), dtype=_np.float32)
                im.pixels.foreach_get(a)
                a = a.reshape(-1, 4)
                a[:, 2] = _np.clip(a[:, 2] * f, 0.0, 1.0)
                im.pixels.foreach_set(a.reshape(-1))
                im.update()

    # ---------------------------------------------------------------------------------------------- placing
    def piece(self, asset, u, v, w, rot=(0.0, 0.0, 0.0), scale=1.0, size=None, tier="bed", yaw=0.0, tris=TRIS, tag=None):
        """A Poly Haven piece with its bounding box's middle at (u, v) (u from the window zone's left edge) and its foot on w. Returns (ext in the display frame, names)."""
        rot = (rot[0], rot[1], rot[2] + yaw)
        d = self.dims(asset, rot, tris=tris)
        if size:
            scale = min(scale, size / max(d.x, d.y, d.z))
        ext = self.place(asset, (u - self.L / 2, v, w), rot=rot, scale=scale, fixture="display", anchor=("c", "c", "min"), tris=tris, tag=tag)
        names = list(self.last_objs)
        self.groups.append({"kind": "piece", "model": asset, "tier": tier, "objs": names})
        self.items.append({"model": asset, "tier": tier, "scale": round(scale, 3), "ext": [round(float(x), 4) for x in ext], "objs": names})
        return ext, names

    def piece_x(self, asset, x_max, v, w, rot=(0.0, 0.0, 0.0), scale=1.0, tier="bed", tris=TRIS, tag=None):
        """Like `piece`, but the piece's bounding box has its +x edge at `x_max` (display frame, centred on the window) and its middle at v: a thing that leans on the return wall."""
        ext = self.place(asset, (x_max, v, w), rot=rot, scale=scale, fixture="display", anchor=("max", "c", "min"), tris=tris, tag=tag)
        names = list(self.last_objs)
        self.groups.append({"kind": "piece", "model": asset, "tier": tier, "objs": names})
        self.items.append({"model": asset, "tier": tier, "scale": round(scale, 3), "ext": [round(float(x), 4) for x in ext], "objs": names})
        return ext, names

    def gm_object(self, name, gm, mats, kind, model, tier="bed", scale=1.0, bevel=0.0, smooth=False):
        ob = gm.to_object(name, mats, self.sc, smooth=smooth)
        ext = gm.extents()
        self.groups.append({"kind": kind, "model": model, "tier": tier, "objs": [ob.name]})
        if kind in ("scripted", "support"):
            self.scripted.append({"model": model, "u": [round(ext[0] + self.L / 2, 3), round(ext[1] + self.L / 2, 3)], "v": [round(ext[2], 3), round(ext[3], 3)], "w": [round(ext[4], 3), round(ext[5], 3)], "tier": tier})
        return ob, ext

    def crate(self, name, u0, u1, v0, v1, w0, w1, tier="bed"):
        """A plain timber crate (the boxes that stand for what Poly Haven has no model of): slats on the sides and a lid of boards, one mesh."""
        wood = self.mat("crate_wood", rgb8(150, 113, 72), rough=0.8)       # weathered deal (176, 140, 92 burnt under the gate's night spill: PIC-05g)
        gm = GM()
        x0, x1 = u0 - self.L / 2, u1 - self.L / 2
        gm.box(x0, x1, v0, v1, w0, w1 - 0.012, 0)
        n = max(2, int((x1 - x0) / 0.1))
        for k in range(n):
            xa = x0 + (x1 - x0) * k / n
            xb = x0 + (x1 - x0) * (k + 1) / n - 0.004
            gm.box(xa, xb, v0 + 0.002, v1 - 0.002, w1 - 0.012, w1, 0)
        ob, ext = self.gm_object(name, gm, [wood], "support", "script:crate", tier)
        return ext

    def price_card(self, u, v, w, k, texts_uv, mats):
        """A hand-lettered card 70 x 50 mm on a wire stake 100 mm high, the face toward the street, leaning back 4 mm: one mesh, a ticket for the checks."""
        gm = GM()
        x = u - self.L / 2
        gm.rod((x, v, w), (x, v, w + 0.07), 0.0012, 1, 6)
        gm.box(x - 0.035, x + 0.035, v - 0.002, v + 0.002, w + 0.050, w + 0.100, 0, uv_front=texts_uv[k % len(texts_uv)])
        ob = gm.to_object("price_card_%d" % k, mats, self.sc)
        self.groups.append({"kind": "ticket", "model": "script:price_cards", "objs": [ob.name]})
        return ob

    def cords(self, corners_w, top_w, name="hung_cords"):
        """Four wire cords from a hung card's corners to the window head, as one mesh."""
        wire = self.mat("wire", rgb8(60, 60, 62), rough=0.5, metal=0.7)
        gm = GM()
        for (x, v) in corners_w[0]:
            gm.rod((x, v, corners_w[1]), (x, v, top_w), 0.0015, 0, 6)
        ob = gm.to_object(name, [wire], self.sc)
        self.struct(ob, "cords", gm.extents())
        return ob

    # ---------------------------------------------------------------------------------------------- timber that is not a flat colour (14 Oct, try 2: ironmonger close review narrow 1 and street 4, 5)
    def poly_map(self, asset, kind="diff"):
        folder = os.path.join(A.POLY, asset, "1k", "textures")
        f = next(os.path.join(folder, x) for x in sorted(os.listdir(folder)) if "_%s_" % kind in x)
        return np.asarray(Image.open(f).convert("RGB")).astype(np.float32)

    def painted_png(self, name, asset, rgb, grain=0.55):
        """A Poly Haven wood map painted in one colour: the paint's colour times the wood's own luma variation about its mean, softened by `grain` (a painted board still shows its grain, less than bare wood). Written to the
        display's texture folder (a 1k PNG): the glb carries it as a plain base-colour image."""
        a = self.poly_map(asset)
        lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])
        k = 1.0 + grain * (lum / float(lum.mean()) - 1.0)
        out = np.clip(np.array(rgb, np.float32)[None, None, :] * k[..., None], 0, 255)
        path = os.path.join(self.tex, name + ".png")
        Image.fromarray(out.astype(np.uint8)).save(path)
        return path

    def hang_cords(self, pairs, name="hung_cords", r=0.0015):
        """Cords from `pairs` = [((x, v, w) lower end, (x, v, w) upper end)] as one mesh: a cord ends INSIDE the part it ties to (the card's top, the rod's axis), so that every end is within 2 mm of a solid part."""
        wire = self.mat("wire", rgb8(60, 60, 62), rough=0.5, metal=0.7)
        gm = GM()
        for a, b in pairs:
            gm.rod(a, b, r, 0, 6)
        ob = gm.to_object(name, [wire], self.sc)
        self.struct(ob, "cords", gm.extents())
        self.cord_ends = getattr(self, "cord_ends", []) + [[list(map(float, a)), list(map(float, b))] for a, b in pairs]
        return ob

    def lean_rot(self, asset, phi_deg, head_z=0.10, long_axis=(1.0, 0.0, 0.0), toward=(1.0, 0.0)):
        """The Euler rotation that stands a model on the END of its handle with its head up, the handle leaning `phi_deg` from the vertical toward `toward` (x, y), and the head's long axis (`long_axis`, the model's own)
        lying across the lean: the head is the part of the model below `head_z` (its z 0 end), the handle's end the vertex farthest from the head's centre."""
        meshes, lo, hi = self.template(asset)
        pts = np.array([tuple(m.matrix_world @ v.co) for m in meshes for v in m.data.vertices])
        head = pts[pts[:, 2] < head_z]
        H = Vector(head.mean(0))
        E = Vector(pts[int(np.argmax(np.linalg.norm(pts - np.array(H), axis=1)))])
        n = math.hypot(*toward)
        sp, cp = math.sin(math.radians(phi_deg)), math.cos(math.radians(phi_deg))
        T = Vector((toward[0] / n * sp, toward[1] / n * sp, cp))
        R1 = (H - E).normalized().rotation_difference(T).to_matrix()
        hx = R1 @ Vector(long_axis)
        across = Vector((-toward[1] / n, toward[0] / n, 0.0))               # horizontal and square to the lean
        hp = hx - T * hx.dot(T)
        hp.normalize()
        ang = math.atan2(T.dot(hp.cross(across)), hp.dot(across))
        if ang > math.pi / 2:
            ang -= math.pi
        elif ang < -math.pi / 2:
            ang += math.pi
        R = Matrix.Rotation(ang, 3, T) @ R1
        e = R.to_euler("XYZ")
        return (e.x, e.y, e.z)

    @staticmethod
    def euler_of(*mats):
        """The Euler (XYZ) of the product of 3 x 3 rotations given left to right (the last is applied first)."""
        R = Matrix.Identity(3)
        for m in mats:
            R = R @ m
        e = R.to_euler("XYZ")
        return (e.x, e.y, e.z)

    def wood_strips(self, name, n, rgb, var=0.08, size=(1024, 64), stencils=None, seed=1, asset="plywood"):
        """A picture of `n` plank strips (each `size`, the grain along the strip) cut from a Poly Haven wood map at random places and tinted to `rgb` with +-`var` of its own (every plank a little different), then
        `stencils` = [(strip index, [(text, font name, size px, x px, y px)...])...] stencilled in black paint with a little wear (a stencil's bridges are left out). Returns (path, [(u0, v0, u1, v1) per strip]) (v 0 at the bottom)."""
        rng = np.random.default_rng(seed)
        a = self.poly_map(asset)
        lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])
        ratio = lum / float(lum.mean())
        W, H = size
        atlas = Image.new("RGB", (W, H * n))
        for k in range(n):
            y0 = int(rng.integers(0, 1024 - H))
            x0 = int(rng.integers(0, 1024 - 512))
            crop = ratio[y0:y0 + H, x0:x0 + 512]
            crop = np.asarray(Image.fromarray((crop * 100).astype(np.uint8)).resize((W, H), Image.BILINEAR)).astype(np.float32) / 100.0
            tint = np.array(rgb, np.float32) * (1.0 + var * rng.uniform(-1, 1))
            strip = np.clip(tint[None, None, :] * (1.0 + 0.9 * (crop - 1.0))[..., None], 0, 255)
            atlas.paste(Image.fromarray(strip.astype(np.uint8)), (0, k * H))
        for (k, lines) in (stencils or []):
            for (text, fnt, px, xx, yy) in lines:
                f = GEN.font(fnt, px)
                if xx == "c":                                   # centred on the part of the strip a plank shows (`span` of it, default 0.42)
                    xx = W * 0.42 / 2.0 - f.getlength(text) / 2.0
                tmp = Image.new("L", (W, H), 0)
                ImageDraw.Draw(tmp).text((xx, yy), text, font=f, fill=255)
                m = np.asarray(tmp).astype(np.float32) / 255.0 * (rng.random((H, W)) > 0.10).astype(np.float32)
                cur = np.asarray(atlas.crop((0, k * H, W, (k + 1) * H))).astype(np.float32)
                cur = cur * (1 - 0.88 * m[..., None]) + np.array([22, 20, 18], np.float32)[None, None, :] * 0.88 * m[..., None]
                atlas.paste(Image.fromarray(np.clip(cur, 0, 255).astype(np.uint8)), (0, k * H))
        path = os.path.join(self.tex, name + ".png")
        atlas.save(path)
        return path, [(0.0, 1.0 - (k + 1) / n, 1.0, 1.0 - k / n) for k in range(n)]

    @staticmethod
    def _span(length, h, strip_aspect=16.0):
        """The share of a strip's width a board `length` long and `h` high takes so that a picture pixel is square (the strips are 16 : 1)."""
        return min(1.0, length / (h * strip_aspect))

    def planked_box(self, name, x0, x1, y0, y1, z0, z1, mats, strips, n_plain, plank_h=0.12, tier="bed", stencil=None, nails=True, seed=None):
        """A timber box built of planks (the stepped crate): horizontal planks `plank_h` high on the front face with 3 mm grooves between them that show the core 2 mm deeper, each plank its own strip of the wood
        atlas (`strips[:n_plain]`, tinted a little differently), the two ends planked the same, lid boards along the top, and a nail head near each end of every plank. One mesh, two materials (`mats` = [wood,
        nails]). `stencil` = (plank index from the bottom, strip index): that plank of the front carries a stencilled strip (its own picture, whole)."""
        gm = GM()
        g, t = 0.003, 0.012
        gm.box(x0 + 0.003, x1 - 0.003, y0 + 0.002, y1 - 0.002, z0, z1 - t, 0, uv_front=strips[0], uv_other=(0.5, strips[0][1] + 0.01))
        nj = max(1, int(round((z1 - z0) / plank_h)))
        ph = (z1 - z0) / nj
        rnd = random.Random(seed if seed is not None else int(abs(x0 * 1000) + abs(z1 * 100)))
        nails_at = []
        sp = self._span(x1 - x0, ph)
        for j in range(nj):
            za, zb = z0 + j * ph + (g / 2 if j else 0.0), z0 + (j + 1) * ph - g / 2
            if stencil is not None and stencil[0] == j:
                u0, v0, u1, v1 = strips[stencil[1]]
                uvf = (u0, v0, u0 + sp, v1)
            else:
                u0, v0, u1, v1 = strips[rnd.randrange(n_plain)]
                uo = rnd.uniform(0.0, max(0.0, 1.0 - sp))
                uvf = (u0 + uo, v0, u0 + uo + sp, v1)
            gm.box(x0, x1, y0, y0 + t, za, zb, 0, uv_front=uvf, uv_other=(u0 + 0.02, 0.5 * (v0 + v1)))
            for xn in (x0 + 0.016, x1 - 0.016):
                nails_at.append((xn, y0, (za + zb) / 2))
        sd = self._span(y1 - y0, ph)
        for (xa, xb) in ((x0, x0 + t), (x1 - t, x1)):
            for j in range(nj):
                za, zb = z0 + j * ph + (g / 2 if j else 0.0), z0 + (j + 1) * ph - g / 2
                u0, v0, u1, v1 = strips[rnd.randrange(n_plain)]
                gm.box(xa, xb, y0 + t, y1, za, zb, 0, uv_ends=(u0, v0, u0 + sd, v1), uv_other=(u0 + 0.02, 0.5 * (v0 + v1)))
        nb = max(1, int(round((y1 - y0) / 0.10)))
        bw = (y1 - y0) / nb
        for b_ in range(nb):
            ya, yb = y0 + b_ * bw + (g / 2 if b_ else 0.0), y0 + (b_ + 1) * bw - g / 2
            u0, v0, u1, v1 = strips[rnd.randrange(n_plain)]
            gm.box(x0, x1, ya, yb, z1 - t, z1, 0, uv_top=(u0, v0, u0 + sp, v1), uv_other=(u0 + 0.02, 0.5 * (v0 + v1)))
        if nails:
            for (xn, yn, zn) in nails_at:
                gm.rod((xn, yn - 0.0016, zn), (xn, yn, zn), 0.0032, 1, 8)
        ob, ext = self.gm_object(name, gm, mats, "support", "script:crate", tier)
        return ob, ext

    def tray_box(self, name, xc, y0, y1, w, h, mat, strips, n_plain, tier="bed", model="script:crate"):
        """A shallow open tray (the bulb trays, the trowel trays): a floor 4 mm thick and four boards 4 mm thick `h` high, each face its own piece of the wood atlas. One mesh. Returns the extents."""
        gm = GM()
        rnd = random.Random(int(abs(xc * 1000) + y0 * 100))

        def uvs(length, hh):
            u0, v0, u1, v1 = strips[rnd.randrange(n_plain)]
            sp = self._span(length, hh)
            uo = rnd.uniform(0.0, max(0.0, 1.0 - sp))
            return (u0 + uo, v0, u0 + uo + sp, v1)

        x0, x1 = xc - w / 2, xc + w / 2
        t = 0.004
        gm.box(x0, x1, y0, y1, 0.0, t, 0, uv_front=uvs(w, t), uv_top=uvs(w, t), uv_other=(0.5, strips[0][1] + 0.01))
        gm.box(x0, x1, y0, y0 + t, 0.0, h, 0, uv_front=uvs(w, h), uv_top=uvs(w, t), uv_other=(0.5, strips[0][1] + 0.01))
        gm.box(x0, x1, y1 - t, y1, 0.0, h, 0, uv_front=uvs(w, h), uv_top=uvs(w, t), uv_other=(0.5, strips[0][1] + 0.01))
        for (xa, xb) in ((x0, x0 + t), (x1 - t, x1)):
            gm.box(xa, xb, y0 + t, y1 - t, 0.0, h, 0, uv_top=uvs(y1 - y0, t), uv_ends=uvs(y1 - y0, h), uv_other=(0.5, strips[0][1] + 0.01))
        return self.gm_object(name, gm, [mat], "support", model, tier)

    # ---------------------------------------------------------------------------------------------- the export
    def finish(self, out_dir, log=print):
        lim = getattr(self, "tex_limit", 512)
        for im in bpy.data.images:
            if im.size[0] > lim and im.name not in ("Render Result",):
                try:
                    im.scale(lim, lim)
                except Exception:
                    pass
        # no alpha cut-out or blend anywhere in the display (DSP-02: real geometry)
        n_alpha = 0
        for m in bpy.data.materials:
            if m.use_nodes and m.users:
                pb = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
                if pb is not None and pb.inputs["Alpha"].is_linked:
                    for l in list(pb.inputs["Alpha"].links):
                        m.node_tree.links.remove(l)
                    pb.inputs["Alpha"].default_value = 1.0
                    n_alpha += 1
                if hasattr(m, "surface_render_method"):
                    m.surface_render_method = "DITHERED"
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, self.ctx.display_glb)
        objs = [o for o in bpy.data.objects if o.type == "MESH" and self.coll_t not in o.users_collection]
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True, export_materials="EXPORT", export_image_format="JPEG",
                                  export_jpeg_quality=85, export_cameras=False, export_lights=False, export_yup=True)
        tri = 0
        dg = bpy.context.evaluated_depsgraph_get()
        for o in objs:
            e = o.evaluated_get(dg)
            me = e.to_mesh()
            me.calc_loop_triangles()
            tri += len(me.loop_triangles)
            e.to_mesh_clear()
        return path, tri, n_alpha


# ---------------------------------------------------------------------------------------------------------------------------------- the ironmonger
def layout_ironmonger(d):
    """The ironmonger's window (target `shops.ironmonger.display`, 14 item rows), try 2 (14 Oct 2026: both fresh reviews of try 1, the brief's step 0 f). Every good now stands at its own size (DSP-06: 0.9 to 1.1;
    try 1 shrank the toolboxes, cans, pump, sledge and brooms to 0.80 to 0.85 and swelled the bulbs to 1.25), so what the 3.35 m window cannot take beside the rest is moved, not shrunk (each move is in NOTES.md).
    u runs along the window from its left edge, v is the depth from the glass, w the height above the bed. Every support is a picture (a painted plywood, a deal plank map from Poly Haven's plywood, CC0), never a flat factor.

    pyramid: 36 tins, a triangular stack 8 high, one tin deep, u 0.20 to 0.98 at v 0.45, against a backing board of painted green plywood (u 0.14 to 1.04, v 0.502 to 0.518, 0.74 high).
    gloves: 6, three stacks of two on a deal shelf 0.78 x 0.32 hung on four cords from a 12 mm black iron rod fixed to the back of the transom (the rod at v 0.012, w 1.794 touches the transom's underside), the
    shelf's underside at w 0.76, over the pyramid's apex (0.69).
    lightbulbs: 12 in two open deal trays of six at their own size (0.10 high, 0.06 across; the pitch 0.064), glass and B22 caps (sw_room.bulb_b22).
    trowels: 4, two pairs on two shallow trays 60 mm high; toolboxes: 2 side by side at the back at 1.0; crate: a stepped crate of nailed planks (a stencilled plank on each step) u 1.92 to 2.70, the front step
    0.35 high with four labelled cleaner tins and the blowtorch, the rear step 0.45 high with four oil tins; cans: 2 watering cans in front of the crate at 1.0; sprinkler, tyre pump and the sledgehammer (head down,
    its handle against the right return wall) in the front row; brooms: 3, their handle ends on the bed, heads up against the right return wall (the handle 13 degrees from the vertical), heads 0.11 apart.
    price cards: 11 (try 1's TINS 99p is gone, TORCH is BLOWLAMP), each at the front edge before its goods."""
    ctx = d.ctx
    rr = d.RR
    walls = rr["walls"]
    wall_rgb = RG._rgb(walls["above"])
    dado_rgb = RG._rgb(walls["dado"])
    d.tex_limit = 1024
    # the bed and the backing board are painted plywood: the green is the shop's own (30, 62, 44); the backing board is a shade darker so the tins' labels stand out (the street review, narrow 4: luma 25 to 45)
    bed_png = d.painted_png("bed_green", "plywood", (30, 62, 44), grain=0.6)
    board_png = d.painted_png("bed_edge", "plywood", (92, 62, 40), grain=0.8)
    back_png = d.painted_png("backing_ply", "plywood", (26, 54, 38), grain=0.6)
    d.start((30, 62, 44), wall_rgb, dado_rgb, bed_png=bed_png, board_png=board_png)
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    metal, label = d.tin_materials()
    # the deal planks: ten plain strips and two with a stencil ("HARTSIDE" on the front step, "PAINTS & OILS" on the rear one, in black paint)
    deal_png, strips = d.wood_strips("deal_strips", 12, (150, 113, 72), var=0.08, seed=4,
                                     stencils=[(10, [("HARTSIDE", "oswald", 50, "c", 4)]), (11, [("PAINTS & OILS", "oswald", 44, "c", 8)])])
    deal_m = d.image_mat("deal", deal_png, rough=0.8)
    nail_m = d.mat("nail_iron", rgb8(70, 68, 66), rough=0.5, metal=0.8)
    # ---- the pyramid and its backing board
    r_t, h_t = 0.0475, 0.086
    u_c = 0.59
    gm = GM()
    layers = 8
    for row in range(layers):
        nrow = layers - row
        x_start = X(u_c) - nrow * 2 * r_t * 1.02 / 2
        for i in range(nrow):
            cx = x_start + (i + 0.5) * 2 * r_t * 1.02
            prof = [(0.0, 0.0), (r_t * 0.94, 0.0), (r_t, 0.004), (r_t, h_t - 0.010), (r_t * 1.035, h_t - 0.010), (r_t * 1.035, h_t - 0.002), (r_t * 0.9, h_t - 0.002), (r_t * 0.9, h_t - 0.006), (0.0, h_t - 0.006)]
            gm.lathe(cx, 0.45, row * h_t, prof, mi=0, n=16, label=(2, 3), mi_label=1, label_uv=d.tin_uv[(row + i) % 16])
    d.gm_object("tin_pyramid", gm, [metal, label], "scripted", "script:paint_tin_pyramid")
    board_m = d.image_mat("backing_board", back_png, rough=0.75)
    gm = GM()
    gm.box(X(0.14), X(1.04), 0.502, 0.518, 0.0, 0.74, 0, uv_front=(0.0, 0.0, 1.6, 1.3), uv_top=(0.0, 0.0, 1.6, 0.04), uv_ends=(0.0, 0.0, 0.04, 1.3), uv_other=(0.3, 0.3))
    d.gm_object("pyramid_backing", gm, [board_m], "support", "script:backing_board")
    # ---- the hung shelf and the gloves: a deal shelf on four cords from a black iron rod under the transom
    sh_png, sh_strips = d.wood_strips("shelf_strips", 3, (138, 116, 86), var=0.05, seed=8)
    shelf_m = d.image_mat("hung_shelf", sh_png, rough=0.8)
    cu0, cu1, cv0, cv1, cw = 0.20, 0.98, 0.06, 0.38, 0.76
    sp_ = d._span(cu1 - cu0, 0.012)
    gm = GM()
    gm.box(X(cu0), X(cu1), cv0, cv1, cw, cw + 0.012, 0, uv_front=(0.0, sh_strips[0][1], min(1.0, sp_), sh_strips[0][3]), uv_top=(0.0, sh_strips[1][1], 1.0, sh_strips[1][3]), uv_other=(0.5, sh_strips[2][1] + 0.01))
    d.gm_object("hung_card", gm, [shelf_m], "support", "script:hung_card")
    iron = d.mat("iron_rod", rgb8(34, 34, 36), rough=0.45, metal=0.8)
    rod_w, rod_v, rod_r = 1.794, 0.012, 0.006
    gm = GM()
    gm.rod((X(0.18), rod_v, rod_w), (X(1.00), rod_v, rod_w), rod_r, 0, 12)
    for xa, xb in ((X(0.18) - 0.014, X(0.18)), (X(1.00), X(1.00) + 0.014)):  # the rod's end caps: a short thicker sleeve each end
        gm.rod((xa, rod_v, rod_w), (xb, rod_v, rod_w), rod_r * 1.5, 0, 12)
    d.gm_object("hang_rod", gm, [iron], "support", "script:hang_rod")
    cx_ = [X(cu0) + 0.012, X(cu1) - 0.012]
    pairs = []
    for xx in cx_:
        for vv in (cv0 + 0.012, cv1 - 0.012):
            pairs.append(((xx, vv, cw + 0.009), (xx, rod_v, rod_w)))        # lower end 3 mm inside the shelf, upper end on the rod's axis
    d.hang_cords(pairs)
    gd = d.dims("garden_gloves_01", (0, 0, 0))
    for i, uc in enumerate((0.34, 0.59, 0.84)):
        for lay in range(2):
            d.piece("garden_gloves_01", uc, 0.22, cw + 0.012 + lay * gd.z, rot=(0, 0, math.pi + rnd.uniform(-0.12, 0.12)), tier="hung_card")
    # ---- the bulbs: two open trays of six at their own size, the bulbs standing on the tray's floor 0.064 apart (the model is 0.06 across)
    for t in range(2):
        xc = X(0.32 + 0.42 * t)
        d.tray_box("bulb_tray_%d" % t, xc, 0.125, 0.195, 0.40, 0.028, deal_m, strips, 10, model="script:bulb_tray")
        for i in range(6):
            d.piece("lightbulb_01", 0.32 + 0.42 * t - 0.16 + i * 0.064, 0.160, 0.004, tier="bulb_tray")
    # ---- trowels: two pairs on two shallow trays 60 mm high (the sill hides the lowest 40 mm of what lies on the bed from the far pavement)
    for i, uc in enumerate((1.18, 1.58)):
        d.tray_box("trowel_tray_%d" % i, X(uc), 0.035, 0.235, 0.36, 0.06, deal_m, strips, 10)
        for lay in range(2):
            d.piece("trowel_01", uc, 0.095 + 0.08 * lay, 0.06 + lay * 0.05, rot=(0, 0, math.pi / 2), yaw=rnd.uniform(-0.04, 0.04), tier="tray" if lay == 0 else "trowels")
    # ---- the toolboxes at the back at their own size, lids up as modelled
    for i, uc in enumerate((1.26, 1.68)):
        d.piece("metal_toolbox", uc, 0.40, 0.0, rot=(0, 0, 0))
    # ---- the stepped crate of nailed planks: the front step (0.35 high) for the cleaner tins and the blowtorch, the rear step (0.45 high) for the oil tins
    d.planked_box("tin_crate_front", X(1.92), X(2.70), 0.28, 0.42, 0.0, 0.35, [deal_m, nail_m], strips, 10, stencil=(1, 10), seed=21)
    d.planked_box("tin_crate_rear", X(1.92), X(2.70), 0.42, 0.54, 0.0, 0.45, [deal_m, nail_m], strips, 10, stencil=(3, 11), seed=22)
    for i in range(4):
        d.piece("oil_tin", 2.06 + i * 0.165, 0.48, 0.45, rot=(0, 0, math.pi / 2), tier="crate")
    for i in range(4):
        d.piece("cleaner_tin_01", 2.00 + i * 0.10, 0.35, 0.35, tier="crate")
    d.piece("brass_blowtorch", 2.55, 0.35, 0.35, rot=(0, 0, 0), tier="crate")
    # ---- the front row: two watering cans in front of the crate (spouts along the window), the sprinkler, the pump, the sledgehammer
    for i, uc in enumerate((2.00, 2.48)):
        d.piece("watering_can_metal_01", uc, 0.14, 0.0, rot=(0, 0, math.pi / 2), yaw=rnd.uniform(-0.05, 0.05))
    d.piece("garden_sprinkler_01", 2.90, 0.16, 0.0, rot=(0, 0, 0))
    d.piece("tire_pump", 3.145, 0.15, 0.0, rot=(0, 0, math.pi / 2))
    wall_x = L / 2
    rot_s = d.euler_of(Matrix.Rotation(math.radians(5.0), 3, "Y"), Matrix.Rotation(math.pi / 2, 3, "Z"), Matrix.Rotation(math.pi, 3, "X"))
    ext_s, _ = d.piece_x("sledgehammer_01", wall_x - 0.004, 0.14, 0.0, rot=rot_s)
    # ---- three plastic brooms standing on their handle ends, heads up against the right return wall (heads 0.11 apart, the first touching it)
    rot_b = d.lean_rot("plastic_broom", 13.0)
    for k in range(3):
        d.piece_x("plastic_broom", wall_x - 0.004 - 0.11 * k, 0.32, 0.0, rot=rot_b, tier="bed")
    # ---- the price cards, each in front of its goods at the front edge of the bed
    cards = [("OIL\n\u00a31.15", 2.24), ("BULBS\n40p", 0.37), ("TROWELS\n\u00a32.45", 1.18), ("GLOVES\n\u00a31.30", 0.17), ("CANS\n\u00a33.95", 2.00), ("PUMP\n\u00a34.50", 3.145), ("SPRINKLER\n\u00a33.75", 2.90),
             ("PAINT\n\u00a32.99", 0.74), ("TOOL BOXES\n\u00a36.95", 1.58), ("BROOMS\n\u00a32.25", 3.03), ("BLOWLAMP\n\u00a38.50", 2.62)]
    path = os.path.join(d.tex, "price_cards.png")
    uvs = GEN.card_atlas(path, [c[0] for c in cards], cols=4, tile=(256, 128), size=46)
    pm = [d.image_mat("price_cards", path, rough=0.8), d.mat("stake", rgb8(60, 60, 62), rough=0.5, metal=0.7)]
    for k, (_, uc) in enumerate(cards):
        d.price_card(uc, 0.025, 0.0, k, uvs, pm)


def _lazy(mod, fn):
    def f(d):
        m = __import__(mod)
        return getattr(m, fn)(d)
    return f


LAYOUTS = {"ironmonger": layout_ironmonger, "newsagent": _lazy("sw_shops_news", "display"), "tea_rooms": _lazy("sw_shops_tea", "display"), "steam_laundry": _lazy("sw_shops_laundry", "display"),
           "grocer": _lazy("sw_shops_grocer", "display"), "chandler": _lazy("sw_shops_chandler", "display"), "fish_market": _lazy("sw_shops_fish", "display")}


def build_display(work, out_dir, ctx, log=print):
    d = GDisplay(work, ctx)
    LAYOUTS[ctx.id](d)
    path, tri, n_alpha = d.finish(out_dir, log)
    info = {"glb": path, "bytes": os.path.getsize(path), "triangles": tri, "pieces": len(d.items), "models": sorted({i["model"] for i in d.items}), "items": d.items, "length_m": d.L, "depth_m": DEPTH,
            "scripted": d.scripted, "groups": d.groups, "structure": d.structure, "texts": list(getattr(d, "display_texts", [])), "tiers": {"bed": {"w": 0.0, "v": [0.0, DEPTH], "u": [-d.L / 2, d.L / 2]}}, "alpha_links_removed": n_alpha, "mesh_audit": getattr(d, "audit", {})}
    os.makedirs(work, exist_ok=True)
    json.dump(info, open(os.path.join(work, "display_items.json"), "w"), indent=1)
    log("display: %d pieces of %d models, %d scripted, %d triangles, %d bytes" % (info["pieces"], len(info["models"]), len(info["scripted"]), tri, info["bytes"]))
    return info
