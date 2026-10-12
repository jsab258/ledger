"""Rita's near metre: the display as real meshes in one glb (target 4.5).

Used by build_ritas.py (stage `display`). Local frame (the approved display's): x along the window, + to the viewer's right, centred on the window zone (3.35 m);
y back from the glass; z up from the bed (the stallriser's top, 0.60 above the footway). The target's table gives each model a zone (u from the window's viewer-left edge,
v out from the back of the glass, w above the bed); each piece stands in its zone, at its real size or smaller where the zone is smaller, on a velvet bed with two velvet
tiers and small pedestals, a ticket on every piece.

KEPT from the approved production/assets/shop-displays/pawnbroker-display.glb (23 Poly Haven models, 23 MB): the stepped velvet bed, the ticket on each piece, the cut of each
model to about 4,500 triangles (never by more than 70 per cent), the display's size (3.35 x 0.55) and the 512-pixel JPEG pictures. CHANGED: the pieces and their places are the
target's table (36 pieces, 26 models; none more than twice), every model carries its blanked 1k maps (sw_assets), digital_wrist_watch is gone, glass meshes are left out as
before; the scripted ring trays, watch pads and chains of the approved display are not made again (the target's table fills the bed with models and they were not in it).
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
import bmesh  # noqa: E402
import sw_assets as A  # noqa: E402
import sw_room as S  # noqa: E402

TRIS = 4500
L_DISPLAY = 3.35
DEPTH = 0.55
# orientation per model (about the vertical, or lying): the front toward the street (-y)
ROT = {
    "standing_picture_frame_01": (0.0, 0.0, math.pi / 2),
    "standing_picture_frame_02": (0.0, 0.0, math.pi / 2),
    "magnifying_glass_01": (math.pi / 2, 0.0, 0.0),
}
LEVELS = (0.12, 0.40, 0.75)


def build_display(work, out_dir, log=print):
    T = A.load_target()
    r = S.Room(work, T)
    R = r.R
    disp = R["display"]
    velvet = r.mat("velvet_red", S.rgb8(96, 10, 20), rough=0.92)
    velvet_b = r.mat("velvet_blue", S.rgb8(14, 22, 66), rough=0.92)
    board = r.mat("bed_board", S.rgb8(70, 44, 28), rough=0.7)
    r.make_textures()
    paper = r.image_mat("tickets_atlas", os.path.join(r.tex, "tickets.png"), rough=0.8)
    L = L_DISPLAY
    x0 = -L / 2
    r.box("bed", -L / 2, L / 2, 0.0, DEPTH, -0.02, 0.0, board)
    r.box("bed_velvet", -L / 2 + 0.01, L / 2 - 0.01, 0.01, DEPTH - 0.01, 0.0, 0.006, velvet)
    # two velvet tiers (w 0.40 and 0.75) on back posts, and a low step (w 0.12) at the back
    r.box("step_0", x0 + 0.05, x0 + L - 0.05, 0.24, DEPTH - 0.02, 0.0, 0.12, velvet)
    for k, (w, v0) in enumerate(((0.40, 0.18), (0.75, 0.22))):
        r.box("tier_%d" % k, x0 + 0.05, x0 + L - 0.05, v0, DEPTH - 0.02, w - 0.015, w, velvet_b if k else velvet)
        for px in np.linspace(x0 + 0.08, x0 + L - 0.08, 5):
            r.box("tier_post_%d_%.2f" % (k, px), px - 0.012, px + 0.012, DEPTH - 0.04, DEPTH - 0.016, 0.0, w - 0.015, board)
    items = []
    rows = []
    for it in disp["items"]:
        u0, u1, v0, v1, w0, w1 = it["zone"]
        n = it["n"]
        asset = it["model"]
        rot = ROT.get(asset, (0.0, 0.0, 0.0))
        d = r.dims(asset, rot, tris=TRIS)
        zw, zd, zh = (u1 - u0) / n, (v1 - v0), (w1 - w0)
        # the tier the piece stands on: its footprint is clipped in v so it stands on the step or the tier
        vv0 = v0
        if abs(w0 - 0.12) < 1e-6:
            vv0 = max(v0, 0.26) if d.y <= (v1 - 0.26) else v0
        elif abs(w0 - 0.40) < 1e-6:
            vv0 = max(v0, 0.20)
        elif abs(w0 - 0.75) < 1e-6:
            vv0 = max(v0, 0.24)
        zd = v1 - vv0
        s = min(1.0, zw / d.x, zd / d.y, zh / d.z)
        if it.get("size_m"):
            s = min(s, it["size_m"] / max(d.x, d.y, d.z))
        for k in range(n):
            xc = u0 + zw * (k + 0.5) - L / 2
            yc = (vv0 + v1) / 2
            ext = r.place(asset, (xc, yc, w0), rot=(rot[0], rot[1], rot[2] + (0.0 if n == 1 else (-0.25 + 0.5 * k))), scale=s, fixture="display", anchor=("c", "c", "min"), tris=TRIS)
            # a pedestal under pieces standing on the low level in front of the step
            if abs(w0 - 0.12) < 1e-6 and ext[2] < 0.24 - 1e-6:
                r.box("pedestal", ext[0] - 0.015, ext[1] + 0.015, ext[2] - 0.015, ext[3] + 0.015, 0.0, 0.12, velvet_b)
            # the ticket: a small card standing in front of the piece, from the atlas (a number and a price)
            tw = r.rnd.uniform(0.026, 0.034)
            tx = (ext[0] + ext[1]) / 2 + r.rnd.uniform(-0.02, 0.02)
            ty = ext[2] - 0.012
            cell = r.rnd.randrange(96)
            cu, cv = (cell % 12) / 12.0, (cell // 12) / 8.0
            me = bpy.data.meshes.new("ticket")
            me.from_pydata([(tx - tw / 2, ty, w0 + 0.001), (tx + tw / 2, ty, w0 + 0.001), (tx + tw / 2, ty - 0.004, w0 + 0.019), (tx - tw / 2, ty - 0.004, w0 + 0.019)], [], [(0, 1, 2, 3)])
            uv = me.uv_layers.new(name="UVMap")
            for loop, (a, b) in zip(me.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
                uv.data[loop.index].uv = (cu + a / 12.0, cv + b / 8.0)
            tob = bpy.data.objects.new("ticket", me)
            r.sc.collection.objects.link(tob)
            tob.data.materials.append(paper)
            items.append({"model": asset, "n_of": n, "zone": it["zone"], "scale": round(s, 3), "ext": [round(v, 4) for v in ext]})
    # pictures to 512 px (the approved display's rule) and export with JPEG textures
    for im in bpy.data.images:
        if im.size[0] > 512 and im.name not in ("Render Result",):
            try:
                im.scale(512, 512)
            except Exception:
                pass
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "ritas_display.glb")
    objs = [o for o in bpy.data.objects if o.type == "MESH" and r.coll_t not in o.users_collection]
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True, export_materials="EXPORT", export_image_format="JPEG",
                              export_jpeg_quality=85, export_cameras=False, export_lights=False, export_yup=True)
    tri = 0
    for o in objs:
        o.data.calc_loop_triangles()
        tri += len(o.data.loop_triangles)
    info = {"glb": path, "bytes": os.path.getsize(path), "triangles": tri, "pieces": len(items), "models": sorted({i["model"] for i in items}), "items": items,
            "length_m": L, "depth_m": DEPTH}
    json.dump(info, open(os.path.join(work, "display_items.json"), "w"), indent=1)
    log("display: %d pieces of %d models, %d triangles, %d bytes" % (info["pieces"], len(info["models"]), tri, info["bytes"]))
    return info


if __name__ == "__main__":
    scratch = os.environ.get("LEDGER_SW_SCRATCH", "/home/user/ledger-scratch")
    build_display(os.path.join(scratch, "shop-windows", "display_work"), os.path.join(A.REPO, "production", "assets", "cloud-week", "shop-windows"))
