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
from PIL import Image

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
        self.box_uvs(ob)
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

    def start(self, bed_rgb, wall_rgb, dado_rgb):
        L = self.L
        bed_m = self.mat("bed_paint", rgb8(*bed_rgb), rough=0.62)
        board_m = self.mat("bed_board", rgb8(70, 44, 28), rough=0.7)
        self.bed_top = bed_m
        self.solid("bed", -L / 2, L / 2, 0.0, DEPTH, -0.026, -0.006, board_m, "bed", bevel=0.0)
        self.solid("bed_top", -L / 2 + 0.01, L / 2 - 0.01, 0.01, DEPTH - 0.01, -0.006, 0.0, bed_m, "bed_top", bevel=0.0)
        plaster = self.mat("return_plaster", rgb8(*wall_rgb), rough=0.9)
        dado = self.mat("return_dado", rgb8(*dado_rgb), rough=0.9)
        ya, yb = -0.005, CARD_PLANE_LOCAL_Y
        dado_top = 0.95
        for side, (xa, xb) in (("l", (-L / 2 - 0.01, -L / 2)), ("r", (L / 2, L / 2 + 0.01))):
            self.solid("return_wall_%s_dado" % side, xa, xb, ya, yb, WALL_Z[0], dado_top, dado, "return_wall", bevel=0.0)
            self.solid("return_wall_%s_plaster" % side, xa, xb, ya, yb, dado_top, WALL_Z[1], plaster, "return_wall", bevel=0.0)

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

    def gm_object(self, name, gm, mats, kind, model, tier="bed", scale=1.0, bevel=0.0):
        ob = gm.to_object(name, mats, self.sc)
        ext = gm.extents()
        self.groups.append({"kind": kind, "model": model, "tier": tier, "objs": [ob.name]})
        if kind in ("scripted", "support"):
            self.scripted.append({"model": model, "u": [round(ext[0] + self.L / 2, 3), round(ext[1] + self.L / 2, 3)], "v": [round(ext[2], 3), round(ext[3], 3)], "w": [round(ext[4], 3), round(ext[5], 3)], "tier": tier})
        return ob, ext

    def crate(self, name, u0, u1, v0, v1, w0, w1, tier="bed"):
        """A plain timber crate (the boxes that stand for what Poly Haven has no model of): slats on the sides and a lid of boards, one mesh."""
        wood = self.mat("crate_wood", rgb8(176, 140, 92), rough=0.8)
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

    # ---------------------------------------------------------------------------------------------- the export
    def finish(self, out_dir, log=print):
        for im in bpy.data.images:
            if im.size[0] > 512 and im.name not in ("Render Result",):
                try:
                    im.scale(512, 512)
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
    """The ironmonger's window (target `shops.ironmonger.display`, 14 item rows). The bed is painted deal in the shop's own dark green. The zones overlap in volume (the blowtorch's w 0.2 to 0.41 is
    on top of the watering cans' w 0 to 0.2; the oil and cleaner tins' w 0.35 over the toolboxes, which stand open with their lids up; the lightbulbs' w 0.7 on the apex of the pyramid; the gloves' zone
    is 0.09 deep for a glove 0.30 long; three plastic brooms of 0.57 lean in a corner 0.25 wide), so every piece has a place of its own on a surface that exists:

    pyramid: 36 tins, a triangular stack 8 high (8 + 7 + ... + 1), one tin deep, against a painted backing board (u 0.20 to 0.98, v 0.40 to 0.50); the tin is 0.095 across and 0.086 high so that the
    apex is 0.69 (the zone's 0.70).
    gloves: 6 lying in three stacks of two on a card 0.78 x 0.32 hung on four cords from the window head at w 0.62 (the target's `hung card`), in front of the pyramid's upper rows (v 0.06 to 0.38).
    lightbulbs: two open trays of six on the bed in front of the pyramid (u 0.22 to 0.62, v 0.09 to 0.215), not on its apex.
    trowels: 4, lying two on two, long side along the window, in front of the toolboxes (u 1.05 to 1.80).
    toolboxes: 2, side by side at the back, their lids up as modelled; the oil and cleaner tins (4 and 4) stand on a crate beside them (u 1.95 to 2.85, 0.35 high), the blowtorch on a small crate.
    watering cans: 2 in the front row, turned so the spout runs along the window (the model is 0.45 long); the sprinkler in the back row; the pump and the sledgehammer at the right end; two plastic
    brooms (the target's three: a third would stand where the pump stands) leaning on the right return wall.
    price cards: 12, at the front edge in front of each group, the project's own hand lettering."""
    ctx = d.ctx
    rr = d.RR
    sh = d.R["display"]
    walls = rr["walls"]
    wall_rgb = RG._rgb(walls["above"])
    dado_rgb = RG._rgb(walls["dado"])
    d.start((30, 62, 44), wall_rgb, dado_rgb)
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    metal, label = d.tin_materials()
    n_py = 36
    # ---- the pyramid and its backing board
    r_t, h_t = 0.0475, 0.086
    u_c = 0.59
    gm = GM()
    k = 0
    tins_ext = None
    layers = 8
    for row in range(layers):
        nrow = layers - row
        x_start = X(u_c) - nrow * 2 * r_t * 1.02 / 2
        for i in range(nrow):
            cx = x_start + (i + 0.5) * 2 * r_t * 1.02
            prof = [(0.0, 0.0), (r_t * 0.94, 0.0), (r_t, 0.004), (r_t, h_t - 0.010), (r_t * 1.035, h_t - 0.010), (r_t * 1.035, h_t - 0.002), (r_t * 0.9, h_t - 0.002), (r_t * 0.9, h_t - 0.006), (0.0, h_t - 0.006)]
            gm.lathe(cx, 0.45, row * h_t, prof, mi=0, n=16, label=(2, 3), mi_label=1, label_uv=d.tin_uv[(row + i) % 16])
            k += 1
    ob_py, ext_py = d.gm_object("tin_pyramid", gm, [metal, label], "scripted", "script:paint_tin_pyramid")
    board_m = d.mat("backing_board", rgb8(150, 150, 140), rough=0.75)
    gm = GM()
    gm.box(X(0.14), X(1.04), 0.502, 0.518, 0.0, 0.74, 0)
    d.gm_object("pyramid_backing", gm, [board_m], "support", "script:backing_board")
    # ---- the hung card and the gloves
    card_m = d.mat("hung_card", rgb8(190, 178, 150), rough=0.8)
    gm = GM()
    cu0, cu1, cv0, cv1, cw = 0.20, 0.98, 0.06, 0.38, 0.62
    gm.box(X(cu0), X(cu1), cv0, cv1, cw, cw + 0.012, 0)
    d.gm_object("hung_card", gm, [card_m], "support", "script:hung_card")
    d.cords(([(X(cu0) + 0.01, cv0 + 0.01), (X(cu1) - 0.01, cv0 + 0.01), (X(cu0) + 0.01, cv1 - 0.01), (X(cu1) - 0.01, cv1 - 0.01)], cw + 0.012), 1.75)
    gd = d.dims("garden_gloves_01", (0, 0, 0))
    for i, uc in enumerate((0.34, 0.59, 0.84)):
        for lay in range(2):
            d.piece("garden_gloves_01", uc, 0.22, cw + 0.012 + lay * gd.z, rot=(0, 0, math.pi + rnd.uniform(-0.12, 0.12)), tier="hung_card")
    # ---- the front row: bulbs in two trays
    tray_m = d.mat("bulb_tray", rgb8(176, 150, 106), rough=0.85)
    for t in range(2):
        gm = GM()
        xc, yb = X(0.32 + 0.24 * t), 0.215
        tw, td = 0.19, 0.125
        gm.box(xc - tw / 2, xc + tw / 2, yb - td, yb, 0.0, 0.004, 0)
        gm.box(xc - tw / 2, xc + tw / 2, yb - td, yb - td + 0.003, 0.0, 0.028, 0)
        gm.box(xc - tw / 2, xc + tw / 2, yb - 0.003, yb, 0.0, 0.028, 0)
        gm.box(xc - tw / 2, xc - tw / 2 + 0.003, yb - td, yb, 0.0, 0.028, 0)
        gm.box(xc + tw / 2 - 0.003, xc + tw / 2, yb - td, yb, 0.0, 0.028, 0)
        d.gm_object("bulb_tray_%d" % t, gm, [tray_m], "support", "script:bulb_tray")
        for i in range(3):
            for j in range(2):
                d.piece("lightbulb_01", 0.32 + 0.24 * t - 0.06 + i * 0.06, yb - 0.04 - j * 0.05, 0.004, tier="bulb_tray")
    # ---- trowels lying two on two, long side along the window
    td_ = d.dims("trowel_01", (0, 0, math.pi / 2))
    for i, uc in enumerate((1.22, 1.62)):
        for lay in range(2):
            d.piece("trowel_01", uc, 0.10, lay * 0.05 + 0.0, rot=(0, 0, math.pi / 2), yaw=rnd.uniform(-0.05, 0.05), tier="bed" if lay == 0 else "trowels")
    # ---- the toolboxes at the back, lids up
    tb = d.dims("metal_toolbox")
    for i, uc in enumerate((1.20, 1.66)):
        d.piece("metal_toolbox", uc, 0.40, 0.0, rot=(0, 0, 0), yaw=rnd.uniform(-0.04, 0.04))
    # ---- the crate with the oil and cleaner tins on it
    d.crate("tin_crate", 1.98, 2.88, 0.30, 0.54, 0.0, 0.35)
    od = d.dims("oil_tin", (0, 0, math.pi / 2))
    for i in range(2):
        for j in range(2):
            d.piece("oil_tin", 2.10 + i * 0.17, 0.36 + j * 0.13, 0.35, rot=(0, 0, math.pi / 2), tier="crate")
    for i in range(2):
        for j in range(2):
            d.piece("cleaner_tin_01", 2.62 + i * 0.10, 0.36 + j * 0.10, 0.35, tier="crate")
    # ---- the blowtorch on a small crate, the sprinkler at the back
    d.crate("torch_crate", 2.94, 3.20, 0.36, 0.54, 0.0, 0.20)
    d.piece("brass_blowtorch", 3.07, 0.45, 0.20, rot=(0, 0, math.pi / 2), tier="crate")
    d.piece("garden_sprinkler_01", 2.0, 0.17, 0.0, rot=(0, 0, 0))
    # ---- the front row: the watering cans (spout along the window), the pump, the sledgehammer
    for i, uc in enumerate((2.15, 2.62)):
        d.piece("watering_can_metal_01", uc, 0.20, 0.0, rot=(0, 0, math.pi / 2), yaw=rnd.uniform(-0.08, 0.08))
    d.piece("tire_pump", 3.14, 0.12, 0.0, rot=(0, 0, 0))
    d.piece("sledgehammer_01", 3.28, 0.30, 0.0, rot=(0, 0, 0), size=0.85)
    # ---- the plastic brooms leaning at the right end (two)
    for i, (uc, vc) in enumerate(((2.95, 0.50), (3.10, 0.50))):
        d.piece("plastic_broom", uc, vc, 0.0, rot=(0, 0, math.pi / 2), tier="bed")
    # ---- the price cards
    texts = ["TINS\n99p", "OIL\n£1.15", "BULBS\n40p", "TROWELS\n£2.45", "GLOVES\n£1.30", "CANS\n£3.95", "PUMP\n£4.50", "SPRINKLER\n£3.75", "PAINT\n£2.99", "TOOL BOXES\n£6.95", "BROOMS\n£2.25", "TORCH\n£8.50"]
    path = os.path.join(d.tex, "price_cards.png")
    uvs = GEN.card_atlas(path, texts, cols=4, tile=(256, 128), size=46)
    pm = [d.image_mat("price_cards", path, rough=0.8), d.mat("stake", rgb8(60, 60, 62), rough=0.5, metal=0.7)]
    for k, uc in enumerate((0.30, 0.68, 1.00, 1.30, 1.66, 2.05, 2.40, 2.76, 3.04, 1.95, 2.95, 3.20)):
        d.price_card(uc, 0.025, 0.0, k, uvs, pm)


LAYOUTS = {"ironmonger": layout_ironmonger}


def build_display(work, out_dir, ctx, log=print):
    d = GDisplay(work, ctx)
    LAYOUTS[ctx.id](d)
    path, tri, n_alpha = d.finish(out_dir, log)
    info = {"glb": path, "bytes": os.path.getsize(path), "triangles": tri, "pieces": len(d.items), "models": sorted({i["model"] for i in d.items}), "items": d.items, "length_m": d.L, "depth_m": DEPTH,
            "scripted": d.scripted, "groups": d.groups, "structure": d.structure, "tiers": {"bed": {"w": 0.0, "v": [0.0, DEPTH], "u": [-d.L / 2, d.L / 2]}}, "alpha_links_removed": n_alpha}
    os.makedirs(work, exist_ok=True)
    json.dump(info, open(os.path.join(work, "display_items.json"), "w"), indent=1)
    log("display: %d pieces of %d models, %d scripted, %d triangles, %d bytes" % (info["pieces"], len(info["models"]), len(info["scripted"]), tri, info["bytes"]))
    return info
