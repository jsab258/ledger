"""Rita's near metre: the display as real meshes in one glb (target 4.5).

Used by build_ritas.py (stage `display`). Local frame (the approved display's): x along the window, + to the viewer's right, centred on the window zone (3.35 m);
y back from the glass; z up from the bed (the stallriser's top, 0.60 above the footway). The target's table gives each model a zone (u from the window zone's viewer-left edge,
v out from the back of the glass, w above the bed); each piece stands in its zone at its real size on a velvet bed with a front strip, a low step and two velvet tiers, a ticket
on every piece. 13 October, try 2 (from the try 1 close and street reviews):

  no pedestals (close fault 1): every piece on the step stands ON the step (v 0.26 to 0.52, its longest side along the window); the bed's front strip (v 0.04 to 0.22) carries only
      bed pieces (w 0). The middle tier (w 0.40) holds pieces at most 0.32 tall, the top tier (w 0.75) the taller ones. Nothing passes through a shelf.
  the front row (close fault 2, street N5): the approved display's ring trays, watch pads and chains, the crammed loop of tools/art-recipes/shop-room.py at its pitches (0.255,
      0.275, 0.16), laid along the strip from u 0.14 to 3.20 with the cigarette case, the lighter, the spectacles and the magnifier among them.
  return walls (close fault 3): at each end of the window zone a wall from the back of the glass to the card plane (0.61 deep) over the card's full height, plaster above the dado
      line and brown dado below (street z 1.65), part of this glb so the game has it too.
  furniture (close narrow 6): velvet as a Principled BSDF with sheen 0.8 (roughness 0.3), its base colour varied +-5 per cent at 0.05 m and a CC0 fabric normal map (ambientCG
      Fabric034) at strength 0.2 on a 0.25 m tile; a 4 mm bevel on every tier, the step and the bed; the posts 12 mm round rods in black lacquer.
13 October, from the try 2 reviews (the narrow points):

  the raked riser (street review 3): the front strip stood flat on the bed (w 0 to 0.03) and from the far pavement the sight line over the window's bottom rail (z 0.637 above the
      footway, 0.037 above the bed) hid everything lower than 28 mm at its front edge to 8 mm at its back, so the trays, rings and pads did not show. A velvet riser raked 20 degrees now
      lies under the strip: w 0.05 at its front edge (v 0.04) rising to w 0.12 where it meets the step (v 0.24); the 4 trays, 4 pads, 2 chains and the small pieces lie on it as laid before,
      25 mm up the slope from its front edge so that each ticket stands on the velvet too.
  the scripted watches and chains (close review 7): each wrist and pocket watch's dial is a painted map (256 px a dial: 12 hour marks, two hands at a random time, four grounds:
      white, cream, black, champagne; the 12 toward the back of the case); each chain is 60 links of 4 x 1.2 mm, each turned 90 degrees to the last, 2.4 mm apart, along the same arc.
KEPT from the approved production/assets/shop-displays/pawnbroker-display.glb: the stepped velvet bed, the ticket on each piece, the cut of each model to about 4,500 triangles
(never by more than 70 per cent), the display's size (3.35 x 0.55), the 512-pixel JPEG pictures and its scripted ring trays, watch pads and chains (the target's `inventory.scripted`).
"""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402
import sw_assets as A  # noqa: E402
import sw_room as S  # noqa: E402

TRIS = 4500
L_DISPLAY = 3.35
DEPTH = 0.55
BED_TOP = 0.0
# the structure (local metres): the step, the two tiers (board 15 mm under its w), their y extents
STEP = {"w": 0.12, "y": (0.24, DEPTH - 0.02), "x_in": 0.05}
TIERS = {"middle": {"w": 0.40, "y": (0.18, DEPTH - 0.02), "piece_v": (0.20, 0.505), "max_h": 0.32, "post_z": (STEP["w"], 0.40 - 0.015)},
         "top": {"w": 0.75, "y": (0.22, DEPTH - 0.02), "piece_v": (0.232, 0.505), "max_h": 0.70, "post_z": (0.40, 0.75 - 0.015)}}
STEP_V = (0.26, 0.505)             # pieces stop 9 mm short of the posts (y 0.514 to 0.526)
BED_V = (0.04, 0.22)
CARD_PLANE_LOCAL_Y = 0.605            # the card stands 0.61 behind the glass's back face; the display's y = 0 is 5 mm inside the glass (the gate puts it at y_m -0.025)
WALL_Z = (-0.05, 2.35)                # the card's full height (street z 0.65 to 3.05), local to the bed's top at z_m 0.60
DADO_TOP = 0.95                       # street z 1.65 = 1.0 m above the room's floor
ROT = {
    "standing_picture_frame_01": (0.0, 0.0, -math.pi / 2),
    "standing_picture_frame_02": (0.0, 0.0, -math.pi / 2),
    "magnifying_glass_01": (math.pi / 2, 0.0, 0.0),
    "round_spectacles": (0.0, 0.0, 0.0),
    "vintage_lighter": (math.pi / 2, 0.0, 0.0),                 # lying on its back
    "pocket_watch": (-math.pi / 2, 0.0, 0.0),                   # lying face up (try 1 stood them; a quarter turn the other way showed the case's back), crown to the back
    "vintage_pocket_watch": (-math.pi / 2, 0.0, 0.0),
    "cigarette_case": (0.0, 0.0, 0.0),
}
# sizes (largest dimension, m) where the approved front-row loop sized a piece, and where the target gives one; everything else stands at its real size (scale 1.0)
SIZE = {"round_spectacles": 0.13, "vintage_lighter": 0.08, "cigarette_case": 0.12, "magnifying_glass_01": 0.15, "pocket_watch": 0.06, "vintage_pocket_watch": 0.06}
# the bed's front row, in order, each with the width of its slot (m): the approved recipe's trays (0.24), pads (0.26) and chains (0.14 of links), then the small pieces among them. The
# recipe's own pitches (0.255, 0.275, 0.16: its loop took a tray's centre as its place and drew from a shuffled bag) leave gaps of 0.015 to 0.02 between trays; here every piece has a
# slot of its own so that nothing overlaps its neighbour (the close review's DSP-03), and the pitches come out at 0.26 to 0.28 with the same gaps. 4 trays, 4 pads, 2 chains, 4 small pieces
BED_SEQUENCE = [("ring_tray", 0.24), ("watch_pad", 0.26), ("round_spectacles", 0.13), ("chain", 0.16), ("ring_tray", 0.24), ("watch_pad", 0.26), ("vintage_lighter", 0.08),
                ("magnifying_glass_01", 0.15), ("chain", 0.16), ("cigarette_case", 0.12), ("ring_tray", 0.24), ("watch_pad", 0.26), ("ring_tray", 0.24), ("watch_pad", 0.26)]
# the four Poly Haven pocket watches lie on two of the pads, two on each (the pad's slots they take are not drawn by script): sequence index -> model. The small pieces and these two pads
# stand in the left two thirds of the strip: from CLOSE_35 the window's right end is out of frame and from the street the sill hides the strip (DSP-03 asks each piece to show)
PAD_WATCHES = {1: "pocket_watch", 5: "vintage_pocket_watch"}
BED_U0 = 0.14
# the raked riser under the front strip (street review 3): front edge (v 0.04, w 0.05), rising to the step (v 0.24, w 0.12): 19.3 degrees, the review's 20. Pieces lie on its surface,
# their old v 0.04 now 25 mm up the slope (a piece's local y becomes s = y - 0.015 along the slope, its local z the height off the velvet)
RISER = {"y0": 0.04, "w0": 0.05, "y1": 0.24, "w1": 0.12, "s_off": 0.015, "x0": 0.10, "x1": 3.24}
RISER["theta"] = math.atan2(RISER["w1"] - RISER["w0"], RISER["y1"] - RISER["y0"])


def rake_xyz(x, y, z):
    """A point of the strip in its old flat frame (y = v, z = height above the bed's top) to the display's frame on the raked riser."""
    s = y - RISER["s_off"]
    th = RISER["theta"]
    return (x, RISER["y0"] + s * math.cos(th) - z * math.sin(th), RISER["w0"] + s * math.sin(th) + z * math.cos(th))


def make_dial_atlas(path):
    """The dial maps (close review 7): one 512 px picture, four dials of 256 px (2 x 2 cells; cell k's origin is (k % 2, k // 2) / 2 in UV): white, cream, black and champagne grounds, 12 hour
    marks (the four quarters longer), an hour hand and a minute hand at a random time (a seeded draw: the same four times every build), a hub. The 12 is at the top of each cell. Painted
    at 4 times the size and reduced."""
    from PIL import ImageDraw as _ID
    rng = random.Random(31)
    # the white and cream grounds are a little under paper white (206 and 212, not 238 and 232): lit by the strips at night a white dial burnt at 250 (PIC-05g), as the frames' paint did in
    # the room (judgement 25)
    grounds = [((206, 205, 198), (30, 30, 34)), ((212, 201, 172), (46, 36, 28)), ((26, 26, 30), (228, 222, 206)), ((214, 196, 150), (52, 40, 26))]
    S4 = 1024
    atlas = Image.new("RGB", (512, 512), (128, 128, 128))
    times = []
    for k, (ground, ink) in enumerate(grounds):
        im = Image.new("RGB", (S4, S4), ground)
        d = _ID.Draw(im)
        c = S4 / 2.0
        d.ellipse([c - 0.97 * c, c - 0.97 * c, c + 0.97 * c, c + 0.97 * c], outline=ink, width=14)
        d.ellipse([c - 0.80 * c, c - 0.80 * c, c + 0.80 * c, c + 0.80 * c], outline=ink, width=4)
        for h in range(12):
            a = math.radians(30.0 * h)
            r1, r2, wd = (0.64, 0.80, 26) if h % 3 == 0 else (0.70, 0.80, 14)
            d.line([c + r1 * c * math.sin(a), c - r1 * c * math.cos(a), c + r2 * c * math.sin(a), c - r2 * c * math.cos(a)], fill=ink, width=wd)
        hh, mm = rng.randrange(12), rng.randrange(60)
        times.append("%d:%02d" % (hh if hh else 12, mm))
        ah = math.radians(30.0 * hh + 0.5 * mm)
        am = math.radians(6.0 * mm)
        d.line([c, c, c + 0.42 * c * math.sin(ah), c - 0.42 * c * math.cos(ah)], fill=ink, width=34)
        d.line([c, c, c + 0.68 * c * math.sin(am), c - 0.68 * c * math.cos(am)], fill=ink, width=20)
        d.ellipse([c - 36, c - 36, c + 36, c + 36], fill=ink)
        atlas.paste(im.resize((256, 256), Image.LANCZOS), ((k % 2) * 256, (1 - k // 2) * 256))       # cell 0 and 1 in the bottom row (v 0 to 0.5): image row 0 is the TOP of the picture
    atlas.save(path)
    return times


def turned_rot(r, asset, base_rot):
    """Rotation about the vertical so that the piece's longest horizontal side runs along the window (the step's rule): turned a quarter if its depth exceeds its width."""
    d = r.dims(asset, base_rot, tris=TRIS)
    if d.y > d.x * 1.05:
        return (base_rot[0], base_rot[1], base_rot[2] + math.pi / 2)
    return base_rot


def piece_rot(r, asset, tier):
    """The step's rule: the longest horizontal side along the window. On the tiers a piece keeps its modelled front to the street unless it is deeper than the tier."""
    base = ROT.get(asset, (0.0, 0.0, 0.0))
    if tier == "step":
        return turned_rot(r, asset, base)
    if tier in TIERS:
        avail = TIERS[tier]["piece_v"][1] - TIERS[tier]["piece_v"][0] - 0.016
        if r.dims(asset, base, tris=TRIS).y > avail:
            return turned_rot(r, asset, base)
    return base


def piece_scale(r, asset, rot, zone_w, zone_d, zone_h, size=None):
    """Real size (1.0), or the target's/approved size where one is given; smaller only if the zone is."""
    d = r.dims(asset, rot, tris=TRIS)
    s = 1.0
    sz = size if size is not None else SIZE.get(asset)
    if sz:
        s = min(s, sz / max(d.x, d.y, d.z))
    return min(s, zone_w / d.x, zone_d / d.y, zone_h / d.z), d


# ---------------------------------------------------------------------------------------------------------------------- small mesh helpers (numpy, one object per group)
class MB:
    """Collects boxes, cylinders and tori into one mesh with a material index per face (and, for a dial's top face, its own UVs)."""

    def __init__(self):
        self.V, self.F, self.M, self.U = [], [], [], []

    def add(self, V, F, mi, uv=None):
        off = len(self.V)
        self.V.extend(tuple(float(c) for c in v) for v in V)
        for k, f in enumerate(F):
            self.F.append(tuple(off + int(i) for i in f))
            self.M.append(mi[k] if isinstance(mi, (list, tuple)) else mi)
            self.U.append(uv[k] if uv else None)

    def box(self, x0, x1, y0, y1, z0, z1, mi):
        V = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        self.add(V, F, mi)

    def cyl(self, x, y, z0, z1, r, mi, n=16, mi_top=None, dial=None):
        """A cylinder; with `dial` = (u0, v0) the cell's origin in the dial atlas, the top face carries the dial map (material `mi_top`), the 12 toward +y."""
        V = []
        for z in (z0, z1):
            for k in range(n):
                t = 2 * math.pi * k / n
                V.append((x + r * math.cos(t), y + r * math.sin(t), z))
        F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        mis = [mi] * len(F)
        uvs = [None] * len(F)
        if dial is not None:
            mis[1] = mi_top if mi_top is not None else mi
            uvs[1] = [(dial[0] + 0.25 + 0.25 * math.cos(2 * math.pi * k / n), dial[1] + 0.25 + 0.25 * math.sin(2 * math.pi * k / n)) for k in range(n)]
        self.add(V, F, mis, uvs)

    def torus(self, c, R, r, mi, axis="y", nm=12, nn=5):
        """A torus about `c` with its axis along x, y or z (a ring standing on its edge has its axis along y)."""
        V, F = [], []
        for i in range(nm):
            a = 2 * math.pi * i / nm
            for j in range(nn):
                b = 2 * math.pi * j / nn
                rho = R + r * math.cos(b)
                p = (rho * math.cos(a), rho * math.sin(a), r * math.sin(b))          # axis z
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

    def link(self, centre, tangent, up, a, b, r, mi, edge, nm=10, nn=4):
        """One chain link (13 Oct, close review 7): an oval of 2a x 2b (centre line) along `tangent`, a round wire of radius r. Flat (the oval in the plane of tangent and the horizontal
        normal) or on edge (the oval in the plane of tangent and `up`): `edge` turns it 90 degrees to the flat one."""
        t = np.array(tangent, float)
        t /= np.linalg.norm(t)
        up = np.array(up, float)
        side = np.cross(up, t)
        side /= np.linalg.norm(side)
        e2 = up if edge else side            # the oval's second axis
        ax = side if edge else up            # the wire's cross-section plane's normal to the oval: the link's axis
        V, F = [], []
        for i in range(nm):
            th = 2 * math.pi * i / nm
            cc = np.array(centre, float) + a * math.cos(th) * t + b * math.sin(th) * e2
            tg = -a * math.sin(th) * t + b * math.cos(th) * e2
            tg /= np.linalg.norm(tg)
            nrm = math.cos(th) * b * t + math.sin(th) * a * e2           # outward in the oval's plane
            nrm /= np.linalg.norm(nrm)
            for j in range(nn):
                ph = 2 * math.pi * j / nn
                V.append(cc + r * (math.cos(ph) * nrm + math.sin(ph) * ax))
        for i in range(nm):
            for j in range(nn):
                i2, j2 = (i + 1) % nm, (j + 1) % nn
                F.append((i * nn + j, i2 * nn + j, i2 * nn + j2, i * nn + j2))
        self.add(V, F, mi)

    def to_object(self, name, mats, scene):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.V, [], self.F)
        me.validate()
        for m in mats:
            me.materials.append(m)
        for p, mi in zip(me.polygons, self.M):
            p.material_index = mi
            p.use_smooth = False
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
        ob = bpy.data.objects.new(name, me)
        scene.collection.objects.link(ob)
        ob["_special_uv"] = json.dumps([[i, u] for i, u in enumerate(self.U) if u is not None]) if any(u is not None for u in self.U) else ""
        return ob


def apply_special_uvs(ob):
    """After box_uvs (which gives every face a cube projection): the faces that carry a map of their own (a dial's top face) get their own UVs."""
    spec = ob.get("_special_uv")
    if not spec:
        return
    me = ob.data
    layer = me.uv_layers.active
    for i, uvs in json.loads(spec):
        p = me.polygons[i]
        for li, uv in zip(p.loop_indices, uvs):
            layer.data[li].uv = uv


def box_uvs(ob, tile_m=0.25):
    """Cube projection in metres, one UV unit = one tile of `tile_m` (the velvet's normal map and base-colour tile)."""
    me = ob.data
    mw = ob.matrix_world
    bm = bmesh.new()
    bm.from_mesh(me)
    layer = bm.loops.layers.uv.verify()
    for f in bm.faces:
        n = (mw.to_3x3() @ f.normal)
        ax = max(range(3), key=lambda i: abs(n[i]))
        for l in f.loops:
            c = mw @ l.vert.co
            uv = (c.x, c.z) if ax == 1 else ((c.y, c.z) if ax == 0 else (c.x, c.y))
            l[layer].uv = (uv[0] / tile_m, uv[1] / tile_m)
    bm.to_mesh(me)
    bm.free()


def solid_box(r, name, x0, x1, y0, y1, z0, z1, mat, bevel=0.004, tile_m=0.25):
    """A box with real vertices (no object scale), UVs by cube projection, a 4 mm bevel (a modifier, applied at export)."""
    mb = MB()
    mb.box(x0, x1, y0, y1, z0, z1, 0)
    ob = mb.to_object(name, [mat], r.sc)
    box_uvs(ob, tile_m)
    if bevel:
        md = ob.modifiers.new("bevel", "BEVEL")
        md.width = min(bevel, 0.45 * min(x1 - x0, y1 - y0, z1 - z0))
        md.segments = 2
        md.limit_method = "ANGLE"
        md.angle_limit = math.radians(30.0)
    return ob


def make_velvet_textures(out_dir):
    """Per colour a 256 px base-colour tile (0.25 m) with the colour varied +-5 per cent at 0.05 m (smoothed noise, periodic), and the ambientCG Fabric034 normal map at 512 px
    (CC0; fetched into SCRATCH/polyhaven/_acg/Fabric034 by the build's assets step). Returns {name: base path}, normal path."""
    os.makedirs(out_dir, exist_ok=True)
    rng = np.random.default_rng(11)
    out = {}
    for nm, rgb in (("velvet_red", (96, 10, 20)), ("velvet_blue", (14, 22, 66))):
        n = 256
        f = rng.normal(0, 1, (n, n))
        f = ndimage.gaussian_filter(f, 12.0, mode="wrap")              # 0.05 m = 51 px: blobs of about that size
        f /= max(f.std(), 1e-6)
        fine = ndimage.gaussian_filter(rng.normal(0, 1, (n, n)), 1.2, mode="wrap")
        fine /= max(fine.std(), 1e-6)
        k = 1.0 + 0.04 * np.clip(f, -2.5, 2.5) / 1.0 + 0.012 * fine        # about +-5 per cent
        img = np.clip(np.array(rgb, np.float32)[None, None, :] * k[..., None], 0, 255).astype(np.uint8)
        p = os.path.join(out_dir, nm + "_base.png")
        Image.fromarray(img).save(p)
        out[nm] = p
    src = os.path.join(A.POLY, "_acg", "Fabric034", "Fabric034_1K-JPG_NormalGL.jpg")
    nrm = os.path.join(out_dir, "fabric034_normal.png")
    Image.open(src).convert("RGB").resize((512, 512), Image.LANCZOS).save(nrm)
    return out, nrm


def velvet_material(name, base_path, nrm_path):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(base_path, check_existing=True)
    t.image.colorspace_settings.name = "sRGB"
    nt.links.new(t.outputs["Color"], p.inputs["Base Color"])
    ni = nt.nodes.new("ShaderNodeTexImage")
    ni.image = bpy.data.images.load(nrm_path, check_existing=True)
    ni.image.colorspace_settings.name = "Non-Color"
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.inputs["Strength"].default_value = 0.2
    nt.links.new(ni.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
    p.inputs["Roughness"].default_value = 0.88
    p.inputs["Sheen Weight"].default_value = 0.8
    p.inputs["Sheen Roughness"].default_value = 0.3
    return m


def build_display(work, out_dir, log=print):
    T = A.load_target()
    r = S.Room(work, T)
    R = r.R
    disp = R["display"]
    r.make_textures()
    tex_dir = os.path.join(work, "tex")
    bases, nrm = make_velvet_textures(tex_dir)
    velvet = velvet_material("velvet_red", bases["velvet_red"], nrm)
    velvet_b = velvet_material("velvet_blue", bases["velvet_blue"], nrm)
    dial_png = os.path.join(tex_dir, "dial_atlas.png")
    dial_times = make_dial_atlas(dial_png)
    dial_map_m = r.image_mat("dial_atlas", dial_png, rough=0.3)
    drng = random.Random(23)            # which of the four dials a watch gets: its own draw, so the main stream (tickets, trays' colours) is the one the try 2 build used
    board = r.mat("bed_board", S.rgb8(70, 44, 28), rough=0.7)
    lacquer = r.mat("post_lacquer", S.rgb8(12, 12, 12), rough=0.25)
    plaster = r.mat("return_plaster", S.rgb8(242, 219, 168), rough=0.9)
    dado = r.mat("return_dado", S.rgb8(107, 69, 43), rough=0.9)
    paper = r.image_mat("tickets_atlas", os.path.join(r.tex, "tickets.png"), rough=0.8)
    gold = r.mat("gold", S.rgb8(218, 160, 66), rough=0.25, metal=1.0)
    silver = r.mat("silver", S.rgb8(204, 204, 208), rough=0.2, metal=1.0)
    leather = r.mat("strap_leather", S.rgb8(31, 15, 8), rough=0.6)
    dial_m = r.mat("dial_white", S.rgb8(230, 224, 210), rough=0.3)
    L = L_DISPLAY
    x0 = -L / 2
    rnd = random.Random(11)
    groups = []                    # {"kind", "model", "objs": [names]} for the checks (DSP-03, DSP-04)
    structure = []
    # ---- the bed, the step, the two tiers on their posts (13 Oct: the velvet is the bed's own top, z -0.006 to 0, so the step stands on it with no overlap)
    def struct(ob, kind, rec):
        structure.append({"kind": kind, "obj": ob.name, "ext": [round(v, 4) for v in rec]})
        return ob
    struct(solid_box(r, "bed", -L / 2, L / 2, 0.0, DEPTH, -0.026, -0.006, board), "bed", [-L / 2, L / 2, 0.0, DEPTH, -0.026, -0.006])
    struct(solid_box(r, "bed_velvet", -L / 2 + 0.01, L / 2 - 0.01, 0.01, DEPTH - 0.01, -0.006, 0.0, velvet, bevel=0.0), "bed_velvet", [-L / 2 + 0.01, L / 2 - 0.01, 0.01, DEPTH - 0.01, -0.006, 0.0])
    struct(solid_box(r, "step_0", x0 + STEP["x_in"], x0 + L - STEP["x_in"], STEP["y"][0], STEP["y"][1], 0.0, STEP["w"], velvet), "step", [x0 + STEP["x_in"], x0 + L - STEP["x_in"], STEP["y"][0], STEP["y"][1], 0.0, STEP["w"]])
    for k, (nm, td) in enumerate(TIERS.items()):
        w = td["w"]
        struct(solid_box(r, "tier_%s" % nm, x0 + 0.05, x0 + L - 0.05, td["y"][0], td["y"][1], w - 0.015, w, velvet_b if k else velvet), "tier_" + nm,
               [x0 + 0.05, x0 + L - 0.05, td["y"][0], td["y"][1], w - 0.015, w])
        # the posts stand on what is under the tier: the middle tier's on the step's top, the top tier's on the middle tier's board (a post through a board would intersect it: DSP-03)
        pz0, pz1 = td["post_z"]
        for px in np.linspace(x0 + 0.08, x0 + L - 0.08, 5):
            mb = MB()
            mb.cyl(px, DEPTH - 0.03, pz0, pz1, 0.006, 0, n=12)
            ob = mb.to_object("tier_post_%s_%.2f" % (nm, px), [lacquer], r.sc)
            struct(ob, "post", [px - 0.006, px + 0.006, DEPTH - 0.036, DEPTH - 0.024, pz0, pz1])
    # ---- the raked riser under the front strip (street review 3): a velvet wedge, front edge (v 0.04, w 0.05) rising to the step at (v 0.24, w 0.12), over u 0.10 to 3.24
    rx0, rx1 = x0 + RISER["x0"], x0 + RISER["x1"]
    mbr = MB()
    mbr.add([(rx0, RISER["y0"], 0.0), (rx1, RISER["y0"], 0.0), (rx1, RISER["y1"], 0.0), (rx0, RISER["y1"], 0.0),
             (rx0, RISER["y0"], RISER["w0"]), (rx1, RISER["y0"], RISER["w0"]), (rx1, RISER["y1"], RISER["w1"]), (rx0, RISER["y1"], RISER["w1"])],
            [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], 0)
    riser_ob = mbr.to_object("riser", [velvet], r.sc)
    box_uvs(riser_ob)
    md_ = riser_ob.modifiers.new("bevel", "BEVEL")
    md_.width = 0.004
    md_.segments = 2
    md_.limit_method = "ANGLE"
    md_.angle_limit = math.radians(30.0)
    struct(riser_ob, "riser", [rx0, rx1, RISER["y0"], RISER["y1"], 0.0, RISER["w1"]])
    # the rake: pieces of the bed's row (the Poly Haven ones) are placed in the slope's own frame (x along the case, y up the slope from the riser's front edge, z off the velvet)
    rake_ob = bpy.data.objects.new("rake", None)
    r.sc.collection.objects.link(rake_ob)
    rake_ob.location = (0.0, RISER["y0"], RISER["w0"])
    rake_ob.rotation_euler = (RISER["theta"], 0.0, 0.0)

    def rake_ext(e):
        """A piece's extents [x0, x1, s0, s1, h0, h1] in the slope's frame to the display's frame (the box of the eight corners)."""
        th = RISER["theta"]
        pts = [(x, RISER["y0"] + s * math.cos(th) - h * math.sin(th), RISER["w0"] + s * math.sin(th) + h * math.cos(th)) for x in (e[0], e[1]) for s in (e[2], e[3]) for h in (e[4], e[5])]
        return [min(p[0] for p in pts), max(p[0] for p in pts), min(p[1] for p in pts), max(p[1] for p in pts), min(p[2] for p in pts), max(p[2] for p in pts)]

    # ---- the return walls (close fault 3): at each end of the window zone, from the back of the glass to the card plane, over the card's full height
    ya, yb = -0.005, CARD_PLANE_LOCAL_Y
    for side, (xa, xb) in (("l", (-L / 2 - 0.01, -L / 2)), ("r", (L / 2, L / 2 + 0.01))):
        struct(solid_box(r, "return_wall_%s_dado" % side, xa, xb, ya, yb, WALL_Z[0], DADO_TOP, dado, bevel=0.0), "return_wall", [xa, xb, ya, yb, WALL_Z[0], DADO_TOP])
        struct(solid_box(r, "return_wall_%s_plaster" % side, xa, xb, ya, yb, DADO_TOP, WALL_Z[1], plaster, bevel=0.0), "return_wall", [xa, xb, ya, yb, DADO_TOP, WALL_Z[1]])

    items = []

    def ticket(x_c, y_front, w0, y_min, rake=False):
        """A 3 mm price card standing in front of a piece, leaning back a little, the front face from the atlas."""
        tw = rnd.uniform(0.026, 0.034)
        tx = x_c + rnd.uniform(-0.02, 0.02)
        ty = max(y_front - 0.012, y_min)
        cell = rnd.randrange(96)
        cu, cv = (cell % 12) / 12.0, (cell // 12) / 8.0
        t = 0.003
        x_a, x_b = tx - tw / 2, tx + tw / 2
        lean = 0.004
        V = [(x_a, ty, w0 + 0.001), (x_b, ty, w0 + 0.001), (x_b, ty - lean, w0 + 0.019), (x_a, ty - lean, w0 + 0.019),
             (x_a, ty + t, w0 + 0.001), (x_b, ty + t, w0 + 0.001), (x_b, ty + t - lean, w0 + 0.019), (x_a, ty + t - lean, w0 + 0.019)]
        V0 = list(V)                                 # the flat frame's x and z give the UVs
        if rake:
            V = [rake_xyz(*v) for v in V]
        me = bpy.data.meshes.new("ticket")
        me.from_pydata(V, [], [(0, 1, 2, 3), (5, 4, 7, 6), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)])
        uv = me.uv_layers.new(name="UVMap")
        for loop in me.loops:
            vx, vz = V0[loop.vertex_index][0], V0[loop.vertex_index][2]
            a_ = (vx - x_a) / max(x_b - x_a, 1e-6)
            b_ = (vz - (w0 + 0.001)) / 0.018
            uv.data[loop.index].uv = (cu + a_ / 12.0, cv + b_ / 8.0)
        tob = bpy.data.objects.new("ticket", me)
        r.sc.collection.objects.link(tob)
        tob.data.materials.append(paper)
        groups.append({"kind": "ticket", "model": "ticket", "objs": [tob.name]})

    def put(asset, tier, xc, w0, v_range, size=None, frac=None, yaw=0.0):
        rot = piece_rot(r, asset, tier)
        rot = (rot[0], rot[1], rot[2] + yaw)
        zone_w = 3.3
        s, d = piece_scale(r, asset, rot, zone_w, v_range[1] - v_range[0], 9.0, size)
        dd = r.dims(asset, rot, tris=TRIS)
        depth = dd.y * s
        f = rnd.uniform(0.15, 0.6) if frac is None else frac
        # the piece's front stands at least 16 mm behind the zone's front edge: the ticket (12 mm in front of the piece, 3 mm thick) stands on the tier, not in the piece
        y_front = v_range[0] + 0.016 + f * max(0.0, (v_range[1] - v_range[0] - 0.016) - depth)
        yc = y_front + depth / 2
        ext = r.place(asset, (xc, yc, w0), rot=rot, scale=s, fixture="display", anchor=("c", "c", "min"), tris=TRIS)
        names = list(r.last_objs)
        ticket(xc, ext[2], w0, v_range[0] + 0.004)
        groups.append({"kind": "piece", "model": asset, "tier": tier, "objs": names})
        items.append({"model": asset, "tier": tier, "scale": round(s, 3), "ext": [round(v, 4) for v in ext], "objs": names})
        return ext

    # ---- the data-driven tiers: each item of the target's table that is not the bed's own row stands in its zone (u centred in the zone)
    tier_of_w = lambda w0: "step" if abs(w0 - STEP["w"]) < 1e-6 else ("middle" if abs(w0 - TIERS["middle"]["w"]) < 1e-6 else ("top" if abs(w0 - TIERS["top"]["w"]) < 1e-6 else "bed"))
    bed_models = {}
    for it in disp["items"]:
        u0, u1, v0, v1, w0, w1 = it["zone"]
        tier = it.get("tier") or tier_of_w(w0)
        if tier == "bed":
            bed_models.setdefault(it["model"], []).append(it)
            continue
        if it["model"].startswith("script:"):
            continue
        n = it["n"]
        for k in range(n):
            xc = (u0 + u1) / 2 - L / 2 if n == 1 else u0 + (u1 - u0) * (k + 0.5) / n - L / 2
            vr = STEP_V if tier == "step" else TIERS[tier]["piece_v"]
            put(it["model"], tier, xc, w0, vr, it.get("size_m"), yaw=rnd.uniform(-0.12, 0.12) if tier != "top" or it["model"] not in ("boombox", "filmstrip_projector_8mm") else 0.0)
    # ---- the bed's front row: the approved generator (tools/art-recipes/shop-room.py), laid along the strip in the target's sequence
    def dial_cell():
        k = drng.randrange(4)
        return ((k % 2) * 0.5, (k // 2) * 0.5)

    def wristwatch(mb, wx, wy, z, metal_i, strap_i):
        mb.box(wx - 0.009, wx + 0.009, wy - 0.045, wy + 0.045, z, z + 0.003, strap_i)
        mb.cyl(wx, wy, z + 0.003, z + 0.010, 0.0155, metal_i, n=16)
        mb.cyl(wx, wy, z + 0.010, z + 0.0108, 0.0125, 3, n=16, mi_top=6, dial=dial_cell())          # the dial: a painted map, the 12 toward the back of the case (close review 7)

    def pocketwatch(mb, wx, wy, z, metal_i):
        mb.cyl(wx, wy, z, z + 0.009, 0.022, metal_i, n=20)
        mb.cyl(wx, wy, z + 0.009, z + 0.0098, 0.019, 3, n=20, mi_top=6, dial=dial_cell())
        mb.torus((wx, wy + 0.027, z + 0.004), 0.006, 0.0015, metal_i, axis="y", nm=10, nn=4)

    def place_on_riser(asset, x, y_old, h, rot, scale):
        """A Poly Haven piece lying on the raked riser: placed in the slope's frame (x, s, h) and parented to the rake. Returns (extents in the slope's frame, object names)."""
        ext_ = r.place(asset, (x, y_old - RISER["s_off"], h), rot=rot, scale=scale, fixture="display", anchor=("c", "c", "min"), tris=TRIS)
        names_ = list(r.last_objs)
        root = bpy.data.objects[names_[0]].parent
        root.parent = rake_ob
        root.matrix_parent_inverse = Matrix.Identity(4)
        return ext_, names_

    bed_mats = [gold, silver, leather, dial_m, velvet_b, velvet, dial_map_m]
    GOLD, SILVER, LEATHER, DIAL, BLUE, RED = 0, 1, 2, 3, 4, 5
    total_w = sum(e[1] for e in BED_SEQUENCE)
    gap = (3.20 - BED_U0 - total_w) / (len(BED_SEQUENCE) - 1)
    x = x0 + BED_U0                 # the left edge of the next slot (display x)
    scripted = []
    n_rings = n_watches = n_chains = 0
    for idx, (kind, wd) in enumerate(BED_SEQUENCE):
        xc = x + wd / 2
        if kind == "ring_tray":
            mb = MB()
            mb.box(x, x + 0.24, 0.04, 0.20, 0.0, 0.024, BLUE if rnd.random() < 0.6 else RED)
            for rr in range(4):
                for cc in range(6):
                    mb.torus((x + 0.02 + cc * 0.04, 0.065 + rr * 0.035, 0.024 + 0.009 + 0.0025 - 0.001), 0.009, 0.0025, GOLD if rnd.random() < 0.75 else SILVER, axis="y", nm=12, nn=5)
            mb.V = [rake_xyz(*v) for v in mb.V]                          # on the raked riser
            ob = mb.to_object("ring_tray", bed_mats, r.sc)
            box_uvs(ob)
            groups.append({"kind": "scripted", "model": "script:ring_tray", "objs": [ob.name]})
            ticket(xc, 0.04, 0.0, 0.004, rake=True)
            scripted.append({"model": "script:ring_tray", "u": [round(x - x0, 3), round(x - x0 + 0.24, 3)], "rings": 24})
            n_rings += 24
        elif kind == "watch_pad":
            mb = MB()
            mb.box(x, x + 0.26, 0.04, 0.20, 0.0, 0.016, BLUE if rnd.random() < 0.5 else RED)
            nw = 0
            poly = PAD_WATCHES.get(idx)
            poly_slots = [(0, 1), (0, 2)] if poly else []        # the two slots of the near row's middle that the Poly Haven watches take
            for rr in range(2):
                for cc in range(4):
                    wx, wy = x + 0.035 + cc * 0.063, 0.08 + rr * 0.075
                    metal = GOLD if rnd.random() < 0.55 else SILVER
                    scripted_kind = rnd.random() < 0.6
                    if (rr, cc) in poly_slots:
                        continue
                    if scripted_kind:
                        wristwatch(mb, wx, wy, 0.016, metal, LEATHER if rnd.random() < 0.5 else metal)
                    else:
                        pocketwatch(mb, wx, wy, 0.016, metal)
                    nw += 1
            mb.V = [rake_xyz(*v) for v in mb.V]
            ob = mb.to_object("watch_pad", bed_mats, r.sc)
            box_uvs(ob)
            apply_special_uvs(ob)
            groups.append({"kind": "scripted", "model": "script:watch_pad", "objs": [ob.name]})
            ticket(xc + 0.10, 0.04, 0.0, 0.004, rake=True)
            scripted.append({"model": "script:watch_pad", "u": [round(x - x0, 3), round(x - x0 + 0.26, 3)], "watches": nw + len(poly_slots)})
            n_watches += nw
            for (rr, cc) in poly_slots:
                wrot = ROT[poly]
                ws, _ = piece_scale(r, poly, wrot, 0.06, 0.07, 0.05)
                wx, wy = x + 0.035 + cc * 0.063, 0.08 + rr * 0.075
                ext2, names2 = place_on_riser(poly, wx, wy, 0.016, (wrot[0], wrot[1], wrot[2] + rnd.uniform(-0.4, 0.4)), ws)
                ext2 = rake_ext(ext2)
                groups.append({"kind": "piece", "model": poly, "tier": "bed", "objs": names2})
                items.append({"model": poly, "tier": "bed", "scale": round(ws, 3), "ext": [round(v, 4) for v in ext2], "objs": names2})
        elif kind == "chain":
            # 13 Oct, close review 7: 60 links of 4 x 1.2 mm (an oval of 4 mm outside length, a 1.2 mm wire), each turned 90 degrees to the last, 2.4 mm apart along the same arc (try 2: 18
            # beads); one object, so the interlocking is not an intersection of two meshes. The arc is the old one: x from 0.01 to 0.15 along the slot, y 0.12 + 0.035 sin(a); the chain
            # is centred on it
            mb = MB()
            tt = np.linspace(0.0, math.pi, 4001)
            ax_ = 0.14 * tt / math.pi
            ay_ = 0.035 * np.sin(tt)
            cum = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(ax_), np.diff(ay_)))])
            n_l, pitch_l = 60, 0.0024
            s0 = (cum[-1] - (n_l - 1) * pitch_l) / 2.0
            for i in range(n_l):
                k = int(np.searchsorted(cum, s0 + i * pitch_l))
                k = min(max(k, 1), len(tt) - 1)
                cx, cy = x + 0.01 + ax_[k], 0.12 + ay_[k]
                tg = (0.14 / math.pi, 0.035 * math.cos(tt[k]), 0.0)
                edge = bool(i % 2)
                mb.link((cx, cy, 0.0013 if edge else 0.0006), tg, (0.0, 0.0, 1.0), 0.0014, 0.0007, 0.0006, GOLD, edge)
            mb.V = [rake_xyz(*v) for v in mb.V]
            ob = mb.to_object("chain", bed_mats, r.sc)
            groups.append({"kind": "scripted", "model": "script:chain", "objs": [ob.name]})
            ticket(xc, 0.04, 0.0, 0.004, rake=True)
            scripted.append({"model": "script:chain", "u": [round(x - x0, 3), round(x - x0 + 0.16, 3)], "links": n_l})
            n_chains += 1
        else:
            asset = kind
            rot = turned_rot(r, asset, ROT.get(asset, (0.0, 0.0, 0.0)))
            rot = (rot[0], rot[1], rot[2] + rnd.uniform(-0.15, 0.15))
            s, _ = piece_scale(r, asset, rot, wd, 0.17, 0.2)
            ext_s, names = place_on_riser(asset, xc, 0.04 + 0.01 + 0.085, 0.0, rot, s)
            ext = rake_ext(ext_s)
            groups.append({"kind": "piece", "model": asset, "tier": "bed", "objs": names})
            items.append({"model": asset, "tier": "bed", "scale": round(s, 3), "ext": [round(v, 4) for v in ext], "objs": names})
            ticket(xc, ext_s[2] + RISER["s_off"], 0.0, 0.004, rake=True)
        x += wd + gap
    # ---- 13 Oct, try 3 (PIC-05g in the night frames, once the strips light the display): the white of the standing frames' mounts and of the white ceramics is 0.8 of the model's white, as the hung
    # frames' paint is 0.75 of it in the room (judgement 25 of NOTES.md)
    for mname, f_ in (("standing_picture_frame_01", 0.8), ("standing_picture_frame_02", 0.8), ("standing_picture_frame_01_artwork", 0.8), ("standing_picture_frame_02_artwork", 0.8), ("ceramic_vase_01", 0.85),
                      ("antique_ceramic_vase_01", 0.85), ("jug_01", 0.85), ("horse_statue_01", 0.85), ("pocket_watch", 0.85), ("vintage_pocket_watch", 0.85)):
        if mname in bpy.data.materials:
            r.tone_material(mname, f_)
    # ---- no alpha cut-out or blend anywhere in the display (DSP-02: real geometry): the boombox's speaker grille is a perforated-looking alpha card in its glTF; here it is opaque
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
    log("display: %d materials lost an alpha link" % n_alpha)
    # ---- pictures to 512 px (the approved display's rule) and export with JPEG textures
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
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        e = o.evaluated_get(dg)
        me = e.to_mesh()
        me.calc_loop_triangles()
        tri += len(me.loop_triangles)
        e.to_mesh_clear()
    info = {"glb": path, "bytes": os.path.getsize(path), "triangles": tri, "pieces": len(items), "models": sorted({i["model"] for i in items}), "items": items,
            "length_m": L, "depth_m": DEPTH, "scripted": scripted, "scripted_counts": {"ring_trays": sum(1 for s_ in scripted if s_["model"] == "script:ring_tray"), "rings": n_rings,
                                                                                           "watch_pads": sum(1 for s_ in scripted if s_["model"] == "script:watch_pad"), "watches_on_pads": n_watches, "chains": n_chains},
            "groups": groups, "structure": structure, "tiers": {"step": {"w": STEP["w"], "v": list(STEP_V), "u": [x0 + STEP["x_in"], x0 + L - STEP["x_in"]]},
                                                                 "middle": {"w": TIERS["middle"]["w"], "v": list(TIERS["middle"]["piece_v"]), "max_h": TIERS["middle"]["max_h"], "u": [x0 + 0.05, x0 + L - 0.05]},
                                                                 "top": {"w": TIERS["top"]["w"], "v": list(TIERS["top"]["piece_v"]), "max_h": TIERS["top"]["max_h"], "u": [x0 + 0.05, x0 + L - 0.05]},
                                                                 "bed": {"w": 0.0, "v": list(BED_V), "u": [x0 + BED_U0, x0 + 3.20]}}}
    info["dial_times"] = dial_times
    info["riser"] = dict(RISER)
    json.dump(info, open(os.path.join(work, "display_items.json"), "w"), indent=1)
    log("display: %d pieces of %d models + %d trays, %d pads, %d chains, %d triangles, %d bytes" % (info["pieces"], len(info["models"]), info["scripted_counts"]["ring_trays"], info["scripted_counts"]["watch_pads"], n_chains, tri, info["bytes"]))
    return info


if __name__ == "__main__":
    scratch = os.environ.get("LEDGER_SW_SCRATCH", "/home/user/ledger-scratch")
    build_display(os.path.join(scratch, "shop-windows", "display_work"), os.path.join(A.REPO, "production", "assets", "cloud-week", "shop-windows"))
