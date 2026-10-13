"""Rita's room, built to target.json (section 4.4) and rendered to the game's rule: three 4096 x 1855 pictures (day, night_lit, night_dark) with the JSON beside them.

Used by build_ritas.py (stage `room`). Needs bpy (Blender 5.2.2 as a module). Room frame (the shop-room.py recipe's, which the target keeps): x across, 0 at the card's
centre, +x the PICTURE's right; y back from the card (the front plane) to the back wall at D; z up from the box floor (the card's bottom edge). The camera stands on the centre
line d = 5.3 m in front of the card and frames W x H exactly (horizontal field 2 atan(W / 2d)).

What stands where is the target's (fixtures, stand-off, goods by name and count); each placed piece's world extents are written to rooms/placed.json for the checks (SO-01 to SO-05,
INV-02, INV-03). The goods are the target's 1k Poly Haven models with their maker's marks painted out (sw_assets.blank): the glTF this loads is `<id>_clean.gltf` where there is one.
"""
import json
import math
import os
import random
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Vector, Matrix, Euler  # noqa: E402
import sw_assets as A  # noqa: E402

REPO = A.REPO
W, H, D = 5.3, 2.4, 4.5
CAM_D = 5.3
PIX = (4096, 1855)
FONT = os.path.join(REPO, "production", "fonts", "libre-franklin", "LibreFranklin[wght].ttf")
STATES = ("day", "night_lit", "night_dark")
BOARD_T = 0.025        # shelf boards 25 mm
TV_LOW_END = 0.20      # the z 1.35 television board ends here (13 Oct, close review 5)
RISER_H = 0.20         # the riser shelves on the television boards (close review 4): 0.20 above the board, 0.20 deep against the wall
RISER_D = 0.20
ALLOW_RISER = ("vintage_video_camera", "alarm_clock_01", "cassette_player", "portable_cassette_player", "binoculars", "vintage_binocular", "mantel_clock_01", "brass_vase_03", "hand_plane_no4", "Camera_01")
ALLOW_FRONT = ("cassette_player", "portable_cassette_player", "alarm_clock_01", "mantel_clock_01")
GLASSY = ("glass", "lense", "lens_glass")


def srgb_to_lin(c):
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c)


def rgb8(r, g, b):
    return srgb_to_lin((r / 255.0, g / 255.0, b / 255.0))


class Room:
    def __init__(self, work, T, seed=7):
        self.work = work
        self.tex = os.path.join(work, "tex")
        os.makedirs(self.tex, exist_ok=True)
        self.T = T
        self.R = A.ritas(T)
        self.rnd = random.Random(seed)
        self.placed = []             # extents of every placed piece: dict(fixture, model, ext=[x0,x1,y0,y1,z0,z1], scale, kind)
        self.fixtures = []           # extents of built fixtures (boards, counter, ...)
        self.templates = {}
        self.hand_base = {}
        self.mats = {}
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.sc = bpy.context.scene
        self.coll_t = bpy.data.collections.new("templates")
        self.sc.collection.children.link(self.coll_t)
        self.coll_t.hide_render = True

    # ------------------------------------------------------------------------------------------------ materials
    def mat(self, name, rgb, rough=0.6, metal=0.0, emit=None, emit_strength=0.0, glass=False, alpha_img=None):
        if name in self.mats:
            return self.mats[name]
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        p = nt.nodes["Principled BSDF"]
        p.inputs["Base Color"].default_value = (*rgb, 1.0)
        p.inputs["Roughness"].default_value = rough
        p.inputs["Metallic"].default_value = metal
        if glass:
            p.inputs["Transmission Weight"].default_value = 1.0
            p.inputs["IOR"].default_value = 1.45
            p.inputs["Roughness"].default_value = 0.02
            # real glass lets a lamp's light through: Cycles' glass blocks the shadow rays (and caustics are off), so for shadow rays the pane is clear
            # (without this the counter's case under its glass top, lit by the battens above, rendered black: PIC-02's first run, 13 October)
            lp = nt.nodes.new("ShaderNodeLightPath")
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            mx = nt.nodes.new("ShaderNodeMixShader")
            out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
            nt.links.new(lp.outputs["Is Shadow Ray"], mx.inputs["Fac"])
            nt.links.new(p.outputs["BSDF"], mx.inputs[1])
            nt.links.new(tr.outputs["BSDF"], mx.inputs[2])
            nt.links.new(mx.outputs["Shader"], out.inputs["Surface"])
        if emit is not None:
            p.inputs["Emission Color"].default_value = (*emit, 1.0)
            p.inputs["Emission Strength"].default_value = emit_strength
        self.mats[name] = m
        return m

    def texmat(self, name, asset, tile_m, tint, base=None, box=True):
        """Poly Haven texture laid in world metres (the recipe's texmat), tinted."""
        folder = os.path.join(A.POLY, asset, "1k", "textures")
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        p = nt.nodes["Principled BSDF"]
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (1.0 / tile_m,) * 3
        nt.links.new(geo.outputs["Position"], mp.inputs["Vector"])

        def img(kind, colour):
            path = next((os.path.join(folder, f) for f in os.listdir(folder) if "_%s_" % kind in f), None)
            if path is None:
                return None
            n = nt.nodes.new("ShaderNodeTexImage")
            n.image = bpy.data.images.load(path, check_existing=True)
            n.image.colorspace_settings.name = "sRGB" if colour else "Non-Color"
            n.projection = "BOX"
            n.projection_blend = 0.2
            nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
            return n
        d = img("diff", True)
        if d is not None:
            mul = nt.nodes.new("ShaderNodeMix")
            mul.data_type = "RGBA"
            mul.blend_type = "MULTIPLY"
            mul.inputs[0].default_value = 1.0
            mul.inputs[7].default_value = (*tint, 1.0)
            nt.links.new(d.outputs["Color"], mul.inputs[6])
            nt.links.new(mul.outputs[2], p.inputs["Base Color"])
        r = img("arm", False)
        if r is not None:
            sep = nt.nodes.new("ShaderNodeSeparateColor")
            nt.links.new(r.outputs["Color"], sep.inputs["Color"])
            nt.links.new(sep.outputs["Green"], p.inputs["Roughness"])
        nm = img("nor_gl", False)
        if nm is not None:
            nmap = nt.nodes.new("ShaderNodeNormalMap")
            nt.links.new(nm.outputs["Color"], nmap.inputs["Color"])
            nt.links.new(nmap.outputs["Normal"], p.inputs["Normal"])
        self.mats[name] = m
        return m

    def image_mat(self, name, path, tile_m=None, rough=0.7, alpha=False, nonc=False, tint=None):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        p = nt.nodes["Principled BSDF"]
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(path, check_existing=True)
        t.image.colorspace_settings.name = "Non-Color" if nonc else "sRGB"
        if tile_m:
            geo = nt.nodes.new("ShaderNodeNewGeometry")
            mp = nt.nodes.new("ShaderNodeMapping")
            mp.inputs["Scale"].default_value = (1.0 / tile_m,) * 3
            nt.links.new(geo.outputs["Position"], mp.inputs["Vector"])
            t.projection = "BOX"
            t.projection_blend = 0.1
            nt.links.new(mp.outputs["Vector"], t.inputs["Vector"])
        nt.links.new(t.outputs["Color"], p.inputs["Base Color"])
        if alpha:
            nt.links.new(t.outputs["Alpha"], p.inputs["Alpha"])
        p.inputs["Roughness"].default_value = rough
        self.mats[name] = m
        return m

    # ------------------------------------------------------------------------------------------------ primitives
    def box(self, name, x0, x1, y0, y1, z0, z1, m, fixture=None):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        o = bpy.context.object
        o.name = name
        o.scale = (max(x1 - x0, 1e-3), max(y1 - y0, 1e-3), max(z1 - z0, 1e-3))
        o.data.materials.append(m)
        if fixture:
            self.fixtures.append({"fixture": fixture, "name": name, "ext": [x0, x1, y0, y1, z0, z1]})
        return o

    def cyl(self, name, x, y, z, r, depth, m, axis="z", verts=24):
        rot = {"z": (0, 0, 0), "x": (0, math.pi / 2, 0), "y": (math.pi / 2, 0, 0)}[axis]
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=(x, y, z), rotation=rot)
        o = bpy.context.object
        o.name = name
        o.data.materials.append(m)
        return o

    def text(self, name, body, x, y, z, size, m, rot=(math.pi / 2, 0, 0), extrude=0.0015):
        bpy.ops.object.text_add(location=(x, y, z), rotation=rot)
        o = bpy.context.object
        o.name = name
        o.data.body = body
        o.data.size = size
        o.data.font = bpy.data.fonts.load(FONT, check_existing=True)
        o.data.align_x = "CENTER"
        o.data.extrude = extrude
        o.data.resolution_u = 4
        o.data.materials.append(m)
        return o

    # ------------------------------------------------------------------------------------------------ models
    def template(self, asset, tris=None, min_keep=0.3):
        """The model imported once (glass meshes left out as the recipe did: the glTF's opacity maps are not in the 1k set), kept in a hidden collection.
        With `tris`, cut to about that many triangles (never by more than 70 per cent: the recipe's rule for the display)."""
        key = asset if tris is None else (asset, tris)
        if key in self.templates:
            return self.templates[key]
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=A.gltf_path(asset))
        new = [o for o in bpy.data.objects if o not in before]
        for o in new:
            if o.type != "MESH":
                continue
        for o in [o for o in new if o.type != "MESH"]:
            mw = None
        bpy.context.view_layer.update()
        meshes = []
        for o in new:
            if o.type == "MESH":
                mw = o.matrix_world.copy()
                o.parent = None
                o.matrix_world = mw
                meshes.append(o)
        for o in new:
            if o.type != "MESH":
                bpy.data.objects.remove(o, do_unlink=True)

        def is_glassy(m):
            return m is not None and (getattr(m, "surface_render_method", "") == "BLENDED" or any(g in m.name.lower() for g in GLASSY))
        # a mesh whose every slot is glass or alpha goes; in a mesh that mixes them (the clocks' faces) the glass faces are cut out
        keep = []
        for o in meshes:
            gidx = [i for i, ms in enumerate(o.material_slots) if is_glassy(ms.material)]
            if gidx and len(gidx) == len(o.material_slots):
                continue
            if gidx:
                bm = bmesh.new()
                bm.from_mesh(o.data)
                dead = [f for f in bm.faces if f.material_index in gidx]
                bmesh.ops.delete(bm, geom=dead, context="FACES")
                bm.to_mesh(o.data)
                bm.free()
            keep.append(o)
        if keep:
            for o in meshes:
                if o not in keep:
                    bpy.data.objects.remove(o, do_unlink=True)
            meshes = keep
        if asset == "filmstrip_projector_8mm":
            meshes = self.projector_fix(meshes)
        for o in meshes:
            for c in list(o.users_collection):
                c.objects.unlink(o)
            self.coll_t.objects.link(o)
            if o.data.shape_keys is not None:
                o.shape_key_clear()
        if tris is not None:
            total = 0
            for o in meshes:
                o.data.calc_loop_triangles()
                total += len(o.data.loop_triangles)
            ratio = max(min_keep, min(1.0, tris / float(max(total, 1))))
            for o in meshes:
                bpy.ops.object.select_all(action="DESELECT")
                o.select_set(True)
                bpy.context.view_layer.objects.active = o
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                if ratio < 1.0:
                    md = o.modifiers.new("cut", "DECIMATE")
                    md.ratio = ratio
                    bpy.ops.object.modifier_apply(modifier=md.name)
        if asset == "filmstrip_projector_8mm":
            meshes = meshes + self.bs1363_plug()
        pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
        lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        self.templates[key] = (meshes, lo, hi)
        return self.templates[key]

    # ------------------------------------------------------------------------------------------------ the projector's lead (13 Oct, from the try 2 reviews, close 11)
    PLUG_END_Y = 0.2185          # the lead's tube ends here (world y of the template): beyond it the model's own plug head, a continental round two-pin one
    PLUG_X = -0.1349             # the lead's x

    def projector_fix(self, meshes):
        """The model carries a continental (Schuko) plug on its lead and, loose beside the projector, a right-angled Schuko plug and a kettle-lead connector. A British shop's projector
        carries a 13 A plug (BS 1363): the loose plug and connector are dropped, the lead is cut where its own plug head starts, and bs1363_plug() puts a scripted 13 A plug on it."""
        out = []
        for o in meshes:
            if o.name.endswith(("_schuko", "_connector")):
                bpy.data.objects.remove(o, do_unlink=True)
                continue
            if o.name.endswith("_cable"):
                bm = bmesh.new()
                bm.from_mesh(o.data)
                mw = o.matrix_world
                dead = [v for v in bm.verts if (mw @ v.co).y > self.PLUG_END_Y]
                bmesh.ops.delete(bm, geom=dead, context="VERTS")
                bm.to_mesh(o.data)
                bm.free()
                o.data.update()
            out.append(o)
        return out

    def bs1363_plug(self):
        """A scripted BS 1363 13 A plug (13 Oct, close review 11): a black body 51 x 45 x 25 mm lying flat on the shelf at the lead's end, three flat pins standing up from its face: the earth
        pin (4 x 8 mm, 17.7 high) at the far end, the live and neutral pins (4 x 6.35 mm) 22.2 mm apart, 22.2 mm nearer the lead, their lower 9 mm sleeved in black. World coordinates of the
        projector's template (Z up, the lead along y)."""
        black = self.mat("plug_black", rgb8(22, 22, 22), rough=0.45)
        brass = self.mat("plug_brass", rgb8(184, 152, 78), rough=0.3, metal=1.0)
        x0, y0 = self.PLUG_X, self.PLUG_END_Y
        made = []

        def blk(name, xa, xb, ya, yb, za, zb, m, bevel=0.0):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=((xa + xb) / 2, (ya + yb) / 2, (za + zb) / 2))
            o = bpy.context.object
            o.name = name
            o.scale = (xb - xa, yb - ya, zb - za)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            o.data.materials.append(m)
            if bevel:
                md = o.modifiers.new("bevel", "BEVEL")
                md.width = bevel
                md.segments = 2
            for c in list(o.users_collection):
                c.objects.unlink(o)
            self.coll_t.objects.link(o)
            made.append(o)
        by0, by1 = y0 - 0.003, y0 + 0.048
        blk("plug_body", x0 - 0.0225, x0 + 0.0225, by0, by1, 0.0, 0.025, black, 0.003)
        blk("plug_cable_sleeve", x0 - 0.0045, x0 + 0.0045, y0 - 0.006, y0 + 0.002, 0.0045, 0.0135, black)
        ye = y0 + 0.036                      # the earth pin, toward the far end
        yl = ye - 0.0222                     # live and neutral
        blk("plug_pin_earth", x0 - 0.002, x0 + 0.002, ye - 0.004, ye + 0.004, 0.025, 0.0427, brass)
        for k, sx in enumerate((-1, 1)):
            xp = x0 + sx * 0.0111
            blk("plug_pin_sleeve_%d" % k, xp - 0.002, xp + 0.002, yl - 0.00318, yl + 0.00318, 0.025, 0.034, black)
            blk("plug_pin_%d" % k, xp - 0.002, xp + 0.002, yl - 0.00318, yl + 0.00318, 0.034, 0.0427, brass)
        return made

    def dims(self, asset, rot=(0.0, 0.0, 0.0), tris=None):
        meshes, lo, hi = self.template(asset, tris)
        E = Euler(rot, "XYZ").to_matrix()
        corners = [E @ Vector((x, y, z)) for x in (lo.x, hi.x) for y in (lo.y, hi.y) for z in (lo.z, hi.z)]
        mn = Vector((min(c.x for c in corners), min(c.y for c in corners), min(c.z for c in corners)))
        mx = Vector((max(c.x for c in corners), max(c.y for c in corners), max(c.z for c in corners)))
        return mx - mn

    def hand_angle(self, ob):
        """The clockwise angle, in degrees from 12, of the tip of a clock-hand mesh seen from the front of the model (the model's face looks toward -y, +x is the viewer's right): the
        vertex farthest from the hub, which is the model's origin. World coordinates of the template."""
        me = ob.data
        mw = ob.matrix_world
        pts = [mw @ v.co for v in me.vertices]
        tip = max(pts, key=lambda p: p.x * p.x + p.z * p.z)
        return math.degrees(math.atan2(tip.x, tip.z)) % 360.0

    def place(self, asset, ref, rot=(0.0, 0.0, 0.0), scale=1.0, fixture="", anchor=("c", "c", "min"), record=True, tris=None, clock=None, tag=None):
        """Put a model so that its (scaled, rotated) bounding box has the anchor point at ref: anchor per axis is 'min', 'c' or 'max'.
        Returns the world extents [x0, x1, y0, y1, z0, z1]."""
        meshes, lo, hi = self.template(asset, tris)
        E = Euler(rot, "XYZ").to_matrix()
        corners = [E @ Vector((x, y, z)) * scale for x in (lo.x, hi.x) for y in (lo.y, hi.y) for z in (lo.z, hi.z)]
        mn = Vector((min(c.x for c in corners), min(c.y for c in corners), min(c.z for c in corners)))
        mx = Vector((max(c.x for c in corners), max(c.y for c in corners), max(c.z for c in corners)))
        off = Vector()
        for i in range(3):
            a = anchor[i]
            ref_i = mn[i] if a == "min" else (mx[i] if a == "max" else (mn[i] + mx[i]) / 2)
            off[i] = ref[i] - ref_i
        root = bpy.data.objects.new(asset + "_root", None)
        self.sc.collection.objects.link(root)
        root.rotation_euler = rot
        root.scale = (scale,) * 3
        # rotation about the model's own origin then translation: the corners above were rotated about the origin, so the same offset applies
        root.location = off
        self.last_objs = []
        for m in meshes:
            c = m.copy()
            self.sc.collection.objects.link(c)
            c.parent = root
            c.matrix_parent_inverse = Matrix.Identity(4)
            if clock is not None and m.name.endswith(("_hours_hand", "_minute_hand", "_second_hand")):
                # 13 Oct, from the try 2 reviews (close 4): each clock shows a time of its own: (hour, minute, second) -> the hands turned about the dial's axis through the hub
                hh, mm, ss = clock
                want = {"_hours_hand": (hh % 12) * 30.0 + mm * 0.5, "_minute_hand": mm * 6.0, "_second_hand": ss * 6.0}[[k for k in ("_hours_hand", "_minute_hand", "_second_hand") if m.name.endswith(k)][0]]
                if m.name not in self.hand_base:
                    self.hand_base[m.name] = self.hand_angle(m)
                c.matrix_basis = Matrix.Rotation(math.radians(want - self.hand_base[m.name]), 4, "Y") @ m.matrix_world
            self.last_objs.append(c.name)
        ext = [mn.x + off.x, mx.x + off.x, mn.y + off.y, mx.y + off.y, mn.z + off.z, mx.z + off.z]
        if record:
            self.placed.append({"fixture": fixture, "model": asset, "ext": [round(v, 4) for v in ext], "scale": round(scale, 4), "rot_deg": [round(math.degrees(r), 1) for r in rot], "objs": list(self.last_objs), "tag": tag, "clock": list(clock) if clock else None})
        return ext

    # ------------------------------------------------------------------------------------------------ textures made by script
    def make_textures(self):
        # hardboard pegboard: tan with a grain and 25 mm holes, 0.6 m to the tile
        n = 1024
        rng = np.random.default_rng(3)
        base = np.zeros((n, n, 3), np.float32)
        base[:] = (150, 112, 72)
        grain = rng.normal(0, 5, (n, 1, 1)).astype(np.float32) + rng.normal(0, 3, (n, n, 1)).astype(np.float32)
        base += grain
        pitch = n / 24.0
        yy, xx = np.mgrid[0:n, 0:n]
        fx = (xx % pitch) - pitch / 2
        fy = (yy % pitch) - pitch / 2
        hole = (fx ** 2 + fy ** 2) < (pitch * 0.17) ** 2
        base[hole] = (34, 24, 16)
        Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).save(os.path.join(self.tex, "pegboard.png"))
        # worn path on the lino: a soft darker band from the door to the counter (hand-painted mask; the floor's generated coordinates, x -2.65..2.65 across, y 0..4.5 back)
        m = np.ones((512, 512), np.float32)
        pts = np.array([[-2.0, 0.0], [-1.9, 0.8], [-1.5, 1.6], [-1.0, 2.6], [-0.7, 3.5]])
        gy, gx = np.mgrid[0:512, 0:512]
        X = gx / 511.0 * W - W / 2
        Y = gy / 511.0 * D
        dmin = np.full((512, 512), 9.0, np.float32)
        for a, b in zip(pts[:-1], pts[1:]):
            t = np.clip(((X - a[0]) * (b[0] - a[0]) + (Y - a[1]) * (b[1] - a[1])) / ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2), 0, 1)
            px, py = a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
            dmin = np.minimum(dmin, np.hypot(X - px, Y - py))
        m = 1.0 - 0.30 * np.exp(-(dmin / 0.42) ** 2) - 0.06 * rng.random((512, 512)) * np.exp(-(dmin / 0.8) ** 2)
        Image.fromarray(np.stack([np.clip(m * 255, 0, 255).astype(np.uint8)] * 3, axis=-1)).save(os.path.join(self.tex, "worn_path.png"))
        # tickets: 12 x 8 cells of 128 x 64 px: a numbered pawn ticket in blue-black ink on cream card
        cells = (12, 8)
        cw, ch = 128, 64
        atl = Image.new("RGB", (cw * cells[0], ch * cells[1]), (222, 214, 192))
        dr = ImageDraw.Draw(atl)
        f1 = ImageFont.truetype(FONT, 22)
        f2 = ImageFont.truetype(FONT, 15)
        r2 = random.Random(5)
        for j in range(cells[1]):
            for i in range(cells[0]):
                x0, y0 = i * cw, j * ch
                dr.rectangle([x0, y0, x0 + cw - 1, y0 + ch - 1], fill=(r2.randint(214, 232), r2.randint(206, 226), r2.randint(180, 200)), outline=(150, 140, 120))
                dr.text((x0 + 10, y0 + 6), "No. %04d" % r2.randint(1000, 9999), fill=(28, 30, 70), font=f1)
                dr.text((x0 + 10, y0 + 38), "£%d.%02d" % (r2.randint(2, 60), r2.choice((0, 50, 75, 99))), fill=(120, 20, 20), font=f2)
        atl.save(os.path.join(self.tex, "tickets.png"))
        # notices (paper, drawn by script): the licence card, the unredeemed pledges card, the counter's two cards
        def card(name, size_px, bg, lines, ink):
            im = Image.new("RGB", size_px, bg)
            d = ImageDraw.Draw(im)
            y = int(size_px[1] * 0.12)
            for body, sz in lines:
                f = ImageFont.truetype(FONT, int(size_px[1] * sz))
                tw = d.textlength(body, font=f)
                d.text(((size_px[0] - tw) / 2, y), body, fill=ink, font=f)
                y += int(size_px[1] * sz * 1.45)
            d.rectangle([2, 2, size_px[0] - 3, size_px[1] - 3], outline=tuple(int(c * 0.7) for c in ink), width=2)
            im = im.filter(ImageFilter.GaussianBlur(0.4))
            im.save(os.path.join(self.tex, name + ".png"))
        card("notice_licence", (512, 200), (186, 180, 164), [("LICENSED PAWNBROKER", 0.2), ("Consumer Credit Act 1974", 0.13), ("Loans on all articles of value", 0.12)], (28, 30, 70))
        card("notice_unredeemed", (480, 160), (166, 150, 104), [("UNREDEEMED", 0.26), ("PLEDGES FOR SALE", 0.26)], (130, 24, 18))
        card("notice_tested", (1024, 120), (172, 160, 122), [("ALL ELECTRICAL GOODS TESTED", 0.38)], (130, 24, 18))
        # 13 Oct, from the try 2 reviews (close 10): paper (235, 232, 222), ink (25, 25, 50) (it was (188, 182, 168) and (50, 52, 96), and read as a grey smear in the shade under the z 1.35 board)
        card("notice_loans", (1024, 260), (235, 232, 222), [("CASH LOANS", 0.30), ("on Gold, Watches & Tools", 0.17)], (25, 25, 50))
        # frame prints are in sw_assets (the invented coastal prints)

    def flat_card(self, name, tex, x, y0, y1, z0, z1, standoff=0.004, wall="left"):
        """A paper card (an image) on a side wall (facing into the room), UVs 0..1: wall 'left' faces +x, 'right' faces -x; or on the counter's front (wall 'front')."""
        m = self.image_mat("card_" + name, os.path.join(self.tex, tex + ".png"), rough=0.8)
        me = bpy.data.meshes.new(name)
        if wall == "left":
            V = [(x, y0, z0), (x, y1, z0), (x, y1, z1), (x, y0, z1)]
        elif wall == "right":
            V = [(x, y1, z0), (x, y0, z0), (x, y0, z1), (x, y1, z1)]
        else:           # on a face looking at the camera (-y): x runs y0..y1 here as x range
            V = [(y0, x, z0), (y1, x, z0), (y1, x, z1), (y0, x, z1)]
        me.from_pydata(V, [], [(0, 1, 2, 3)])
        uv = me.uv_layers.new(name="UVMap")
        for loop, (a, b) in zip(me.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
            uv.data[loop.index].uv = (a, b)
        ob = bpy.data.objects.new(name, me)
        self.sc.collection.objects.link(ob)
        ob.data.materials.append(m)
        return ob

    # ------------------------------------------------------------------------------------------------ the shell
    def shell(self):
        self.make_textures()
        floor_m = self.texmat("lino_old", "old_linoleum_flooring_01", 1.2, (0.62, 0.55, 0.50), base=None)
        # the worn path: multiply the floor's base colour by the hand-painted mask in the floor's generated coordinates
        nt = floor_m.node_tree
        p = nt.nodes["Principled BSDF"]
        link = [l for l in nt.links if l.to_socket == p.inputs["Base Color"]][0]
        src = link.from_socket
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mimg = nt.nodes.new("ShaderNodeTexImage")
        mimg.image = bpy.data.images.load(os.path.join(self.tex, "worn_path.png"), check_existing=True)
        mimg.image.colorspace_settings.name = "Non-Color"
        nt.links.new(tc.outputs["Generated"], mimg.inputs["Vector"])
        mm = nt.nodes.new("ShaderNodeMix")
        mm.data_type = "RGBA"
        mm.blend_type = "MULTIPLY"
        mm.inputs[0].default_value = 1.0
        nt.links.new(src, mm.inputs[6])
        nt.links.new(mimg.outputs["Color"], mm.inputs[7])
        nt.links.new(mm.outputs[2], p.inputs["Base Color"])
        wall_m = self.texmat("plaster_cream", "painted_plaster_wall", 1.5, (0.95, 0.86, 0.66))
        dado_m = self.texmat("plaster_brown", "painted_plaster_wall", 1.5, (0.42, 0.27, 0.17))
        ceil_m = self.mat("ceiling", rgb8(180, 173, 158), rough=0.9)
        rail_m = self.mat("dado_rail", rgb8(96, 62, 40), rough=0.45)
        self.wall_m, self.dado_m = wall_m, dado_m
        self.box("floor", -W / 2, W / 2, 0, D, -0.02, 0.0, floor_m)
        self.box("ceiling", -W / 2, W / 2, 0, D, H, H + 0.02, ceil_m)
        # side walls: dado to z 1.0, plaster above, a dado rail (12 mm) between
        for sgn, nm in ((-1, "left"), (1, "right")):
            x0, x1 = (-W / 2 - 0.1, -W / 2) if sgn < 0 else (W / 2, W / 2 + 0.1)
            self.box("wall_%s_dado" % nm, x0, x1, 0, D, 0.0, 1.0, dado_m)
            self.box("wall_%s_up" % nm, x0, x1, 0, D, 1.0, H, wall_m)
        # back wall with the doorway (x 1.45 to 2.35, z 0 to 2.0)
        yb0, yb1 = D, D + 0.1
        self.box("wall_back_dado_l", -W / 2, 1.45, yb0, yb1, 0.0, 1.0, dado_m)
        self.box("wall_back_up_l", -W / 2, 1.45, yb0, yb1, 1.0, H, wall_m)
        self.box("wall_back_dado_r", 2.35, W / 2, yb0, yb1, 0.0, 1.0, dado_m)
        self.box("wall_back_up_r", 2.35, W / 2, yb0, yb1, 1.0, H, wall_m)
        self.box("wall_back_over_door", 1.45, 2.35, yb0, yb1, 2.0, H, wall_m)
        # the back room behind the doorway: a plain cream room, lit by its own light (state by state)
        br = self.mat("backroom_wall", rgb8(205, 196, 170), rough=0.9)
        self.box("backroom_floor", 1.35, 2.45, D + 0.1, D + 2.4, -0.02, 0.0, self.mat("backroom_floor", rgb8(70, 58, 44), rough=0.6))
        self.box("backroom_ceiling", 1.35, 2.45, D + 0.1, D + 2.4, H, H + 0.02, br)
        self.box("backroom_end", 1.35, 2.45, D + 2.4, D + 2.42, 0.0, H, br)
        self.box("backroom_left", 1.33, 1.35, D + 0.1, D + 2.4, 0.0, H, br)
        self.box("backroom_right", 2.45, 2.47, D + 0.1, D + 2.4, 0.0, H, br)
        # ceiling battens (T12 in slim fittings): fitting 0.02 + opal diffuser 0.025 = 0.045 below the ceiling
        self.diff_m = self.mat("tube_diffuser", rgb8(172, 174, 168), rough=0.5, emit=(0.95, 0.97, 1.0), emit_strength=0.0)
        fit_m = self.mat("batten_fitting", rgb8(190, 188, 180), rough=0.5)
        self.tube_objs = []
        for k, t in enumerate(self.R["room"]["lights"]["tubes"]):
            # 13 Oct (close review, narrow 13): the fitting and the diffuser 0.025 deep in all (try 1: 0.045, painted on the ceiling and stretched about 0.2 m in depth)
            self.box("batten_%d" % k, -0.78, 0.78, t["y"] - 0.06, t["y"] + 0.06, H - 0.010, H, fit_m, fixture="R-ceiling-tubes")
            o = self.box("tube_%d" % k, -0.75, 0.75, t["y"] - 0.045, t["y"] + 0.045, H - 0.025, H - 0.010, self.diff_m, fixture="R-ceiling-tubes")
            self.tube_objs.append(o)

    # ------------------------------------------------------------------------------------------------ fixtures
    def back_fixtures(self):
        shelf_m = self.mat("shelf", rgb8(150, 108, 70), rough=0.55)
        upright_m = self.mat("upright", rgb8(120, 84, 54), rough=0.6)
        fx = {f["id"]: f for f in self.R["room"]["fixtures"]}
        stock = fx["R-back-stock"]
        x0s, x1s = stock["x"]                                        # -2.6, 1.35
        cx0, cx1 = fx["R-back-counter"]["x"]                         # -1.9, 0.9
        tiers = stock["tiers"]                                       # 0.5, 0.85, 1.35, 1.80, 2.05  (13 Oct: the TV tiers 0.45 apart, the review's z 1.35 and 1.80)
        self.tv_tiers = fx["R-back-tv-tiers"]["tiers"]               # 1.35, 1.80
        self.tiers = tiers
        self.tier_defs = []
        for z in tiers:
            if z in (0.5, 0.85):
                ranges = [(x0s, cx0), (cx1, x1s)]                    # the lowest two tiers only at the ends: the counter stands in front of the middle
            elif z in self.tv_tiers:
                # 13 Oct, from the try 2 reviews (close 5): the z 1.35 board ENDS at x 0.20 (the till stands at x 0.28 to 0.72 and rises to z 1.47: the board, 25 mm thick, ran through it)
                ranges = [(x0s, cx0), (cx0, TV_LOW_END if z == min(self.tv_tiers) else cx1), (cx1, x1s)]
            else:
                # the top tier over the ends only: a television at its real size (0.41) on the upper TV tier stands 2.21 high, through a board at 2.05 (the review's z 1.35 and 1.80
                # for the TV tiers did not allow for the top tier); over the TVs the wall is open to the ceiling
                ranges = [(x0s, cx0), (cx1, x1s)]
            rng = []
            for (a, b) in ranges:
                is_tv = z in self.tv_tiers and a == cx0
                d_board = fx["R-back-tv-tiers"]["depth_m"] if is_tv else 0.30
                # (13 Oct, SO-07: a shelf stops at the upright's face, 15 mm in from the run's end, instead of running through it)
                self.box("shelf_%s_%.2f_%.2f" % (str(z), a, b), a + (0.015 if abs(a - x0s) < 1e-9 else 0.0), b - (0.015 if abs(b - x1s) < 1e-9 else 0.0), D - d_board, D - 0.005, z - BOARD_T, z, shelf_m,
                         fixture="R-back-tv-tiers" if is_tv else "R-back-stock")
                above = [t for t in tiers if t > z + 1e-6]
                if is_tv and z == max(self.tv_tiers):
                    gap = H - z                                       # open above the upper TV tier
                else:
                    gap = (min(above) if above else H) - z
                rng.append((a, b, gap, d_board, is_tv))
            self.tier_defs.append({"z": z, "ranges": rng})
        for x in (x0s, x1s):
            self.box("upright_%.2f" % x, x - 0.015, x + 0.015, D - 0.30, D - 0.005, 0.5 - BOARD_T, 2.05, upright_m, fixture="R-back-stock")
        # the door-boxes' tier: over the back door only, z 2.05 to 2.25, boards 0.30 deep
        self.box("shelf_door_boxes", 1.45, 2.35, D - 0.30, D - 0.005, 2.05 - BOARD_T, 2.05, shelf_m, fixture="R-back-door-boxes")
        # the counter: a glass-topped case on a velvet bed, against the wall (0.6 deep, 1.05 high, 2.8 long). 13 Oct (close review, narrow 4): the velvet bed is RAKED 25 degrees up toward
        # the back so the jewellery on it shows as rings, not as a row of points, from the low angle the camera sees the case at
        cy0, cy1 = D - 0.60, D - 0.005
        wood = self.mat("counter_wood", rgb8(96, 58, 34), rough=0.42)
        velvet = self.mat("velvet", rgb8(112, 14, 24), rough=0.92)
        glass = self.mat("counter_glass", (1, 1, 1), glass=True)
        self.box("counter_base", cx0, cx1, cy0, cy1, 0.0, 0.75, wood, fixture="R-back-counter")
        self.rake_deg = 25.0
        yf, yb = cy0 + 0.04, cy1 - 0.04
        th = math.radians(self.rake_deg)
        zf = 0.77
        zb = zf + (yb - yf) * math.tan(th)
        # a wedge of velvet: front edge z 0.75 to 0.77, rising to the back
        V = [(cx0 + 0.04, yf, 0.75), (cx1 - 0.04, yf, 0.75), (cx1 - 0.04, yb, 0.75), (cx0 + 0.04, yb, 0.75), (cx0 + 0.04, yf, zf), (cx1 - 0.04, yf, zf), (cx1 - 0.04, yb, zb), (cx0 + 0.04, yb, zb)]
        me = bpy.data.meshes.new("counter_velvet")
        me.from_pydata(V, [], [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
        me.validate()
        ob = bpy.data.objects.new("counter_velvet", me)
        self.sc.collection.objects.link(ob)
        ob.data.materials.append(velvet)
        self.rake_origin = (yf, zf)
        # (13 Oct, SO-07: the front and the two ends stop under the top, and the ends stop behind the front, so the four slabs only touch)
        for nm, (a, b, c, d_, e, f) in {"top": (cx0, cx1, cy0, cy1, 1.04, 1.05), "front": (cx0, cx1, cy0, cy0 + 0.006, 0.75, 1.04),
                                       "end_l": (cx0, cx0 + 0.006, cy0 + 0.006, cy1, 0.75, 1.04), "end_r": (cx1 - 0.006, cx1, cy0 + 0.006, cy1, 0.75, 1.04)}.items():
            self.box("counter_glass_" + nm, a, b, c, d_, e, f, glass)
        self.counter_ext = (cx0, cx1, cy0, cy1)
        # the notices: CASH LOANS moves from the counter's front to the back wall above the counter (close review, narrow 5), flat on the wall (0.004 off it), so the card moves true
        # with the stock wall instead of shearing as a counter does; the tested-goods card stays on the counter's front
        self.flat_card("notice_loans", "notice_loans", D - 0.004, cx0 + 0.45, cx0 + 1.40, 1.025, 1.265, wall="front")        # hung 0.05 m lower (13 Oct, close review 10)
        self.flat_card("notice_tested", "notice_tested", cy0 - 0.004, cx0 + 1.55, cx1 - 0.15, 0.12, 0.30, wall="front")
        # the back door: half-glazed painted door, ajar, hinged at the right jamb (x 2.35), swinging into the back room; frame 40 proud of the wall
        door_m = self.mat("door_paint", rgb8(210, 204, 186), rough=0.4)
        # (13 Oct, SO-07: the jambs stop under the head and the head stops under the door-boxes' shelf at 2.025, so no frame member runs through another)
        for nm, (a, b, z0, z1) in {"jamb_l": (1.41, 1.45, 0.0, 2.0), "jamb_r": (2.35, 2.39, 0.0, 2.0), "head": (1.41, 2.39, 2.0, 2.02)}.items():
            self.box("doorframe_" + nm, a, b, D - 0.04, D, z0, z1, door_m, fixture="R-back-door")
        hinge_x = 2.345            # (13 Oct, SO-07: 5 mm inside the opening, so the leaf's hinge stile, turned 10 degrees, does not run into the wall)
        leaf_w = 0.86
        ang = math.asin(0.15 / leaf_w)
        leaf = bpy.data.objects.new("door_leaf_root", None)
        self.sc.collection.objects.link(leaf)
        leaf.location = (hinge_x, D + 0.05, 0.0)
        leaf.rotation_euler = (0.0, 0.0, -ang)      # the free edge (the left one) swings back into the room: +y
        # leaf pieces in the hinge frame: x from 0 to -leaf_w (toward the left jamb)
        gl = self.mat("door_glass", (1, 1, 1), glass=True)
        parts = [("stile_l", -leaf_w, -leaf_w + 0.11, 0.0, 1.98, door_m), ("stile_r", -0.11, 0.0, 0.0, 1.98, door_m), ("rail_b", -leaf_w + 0.11, -0.11, 0.0, 0.25, door_m),
                 ("rail_m", -leaf_w + 0.11, -0.11, 0.95, 1.10, door_m), ("rail_t", -leaf_w + 0.11, -0.11, 1.86, 1.98, door_m), ("panel", -leaf_w + 0.11, -0.11, 0.25, 0.95, door_m)]
        for nm, a, b, z0, z1, m in parts:
            o = self.box("door_" + nm, a, b, -0.02, 0.02, z0, z1, m)
            o.parent = leaf
        o = self.box("door_glass_pane", -leaf_w + 0.11, -0.11, -0.005, 0.005, 1.10, 1.86, gl)
        o.parent = leaf
        knob = self.cyl("door_knob", -leaf_w + 0.05, -0.045, 1.0, 0.03, 0.03, self.mat("brass", rgb8(160, 120, 55), rough=0.3, metal=1.0), axis="y")
        knob.parent = leaf
        self.fixtures.append({"fixture": "R-back-door", "name": "door_leaf", "ext": [1.45, 2.35, D - 0.04, D + 0.15 + 0.05, 0.0, 2.0]})

    # ------------------------------------------------------------------------------------------------ the back wall's stock
    def stock(self):
        """The stock wall (13 Oct, close review narrow 3; try 2 narrow points 4 and 5): every piece at its real size or at 0.9 to 1.0 of it (never scaled up), each shelf filled by COUNT. A piece
        that does not fit a tier at 0.9 goes to the next; one that fits none is reported.
        Try 3: the two television boards carry RISER SHELVES (0.20 above the board, 0.20 deep, against the wall) in every free stretch between and beside the sets; the pieces of the pool that
        fit stand on them (ALLOW_RISER), a front row of the slim ones stands on the board in front of them (ALLOW_FRONT), and the rest of the pool fills the two ends of the stock wall as before.
        One cardboard box stands on top of each upper set. The z 1.35 board ends at x 0.20."""
        R = self.R
        goods = [g for g in R["room"]["goods"] if g["on"] in ("R-back-stock", "R-back-tv-tiers", "R-back-door-boxes") and not g["model"].startswith("script:")]
        rnd = self.rnd
        JIT = 0.03                    # the turn of a piece about the vertical, +-: 1.7 degrees (try 2: 2.9, which overlapped neighbours by a few mm)

        def fit(asset, gap, depth_max, size=None):
            best = None
            for turn in (0.0, math.pi / 2):
                d = self.dims(asset, (0, 0, turn))
                clear, deep = gap - BOARD_T - 0.015, depth_max - 0.035
                if size:
                    s = size / max(d)
                    if d.z * s > clear + 1e-9 or d.y * s > deep + 1e-9:
                        continue
                else:
                    s = min(1.0, clear / d.z, deep / d.y)
                    if s < 0.9 - 1e-9:
                        continue
                if best is None or s > best[0] + 1e-9 or (abs(s - best[0]) < 1e-9 and d.y < best[2].y):
                    best = (s, turn, d)
            return best

        def fit2(asset, clear, deep):
            """The same with the clearance and the depth given outright (a riser or a front row), never below 0.9."""
            best = None
            for turn in (0.0, math.pi / 2):
                d = self.dims(asset, (0, 0, turn))
                s = min(1.0, clear / d.z, deep / d.y)
                if s < 0.9 - 1e-9:
                    continue
                if best is None or s > best[0] + 1e-9 or (abs(s - best[0]) < 1e-9 and d.y < best[2].y):
                    best = (s, turn, d)
            return best
        pool = []
        for g in goods:
            for _ in range(g["n"]):
                pool.append({"model": g["model"], "on": g["on"], "size": g.get("size_m")})
        tvs = [p for p in pool if p["model"] == "television_02"]
        boxes_door = [p for p in pool if p["on"] == "R-back-door-boxes"]
        rest = [p for p in pool if p not in tvs and p not in boxes_door]
        # the doorway's boxes: three over the back door at z 2.05 to 2.25 (0.30 largest side)
        # (13 Oct, SO-07: three boxes of 0.285 largest side, 0.30 apart, so they stand clear of one another and inside the shelf's ends (1.45 to 2.35); try 2: 0.30 on a 0.28 pitch)
        xs = [1.4525 + 0.1425 + 0.30 * k for k in range(3)]
        for p, x in zip(boxes_door, xs):
            s = 0.285 / max(self.dims("cardboard_box_01"))
            self.place("cardboard_box_01", (x, D - 0.005, 2.05), rot=(0, 0, math.pi / 2 + rnd.uniform(-0.02, 0.02)), scale=s, fixture="R-back-door-boxes", anchor=("c", "max", "min"))
        # the four television sets on the two TV tiers, at their real size (1.0: the tiers are 0.45 apart); back to the wall, 0.35 deep
        zt = sorted(self.tv_tiers)
        tv_x = {zt[0]: [-1.55, -0.25], zt[1]: [-1.1, 0.25]}
        self.tv_ext = {}
        for z, xl in tv_x.items():
            for x in xl:
                ext = self.place("television_02", (x, D, z), rot=(0, 0, 0), scale=1.0, fixture="R-back-tv-tiers", anchor=("c", "max", "min"))
                self.tv_ext[(z, x)] = ext
                self.tickets_for(x, ext[2] - 0.003, z)
        self.tv_spans = tv_x
        # one cardboard box on top of each upper set (close review 4): the set's top is at 2.2114 and the ceiling at 2.40, so the box (the model is 0.342 high) is scaled to fit under it with
        # 12 mm to spare; it keeps the target's rule that a box has a size of its own (the SO-06 test leaves the boxes out)
        self.box_on_tv = 0
        self.scales = []
        for x in tv_x[zt[1]]:
            cand = [p for p in rest if p["model"] == "cardboard_box_01"]
            if not cand:
                break
            rest.remove(cand[0])
            top = self.tv_ext[(zt[1], x)][5]
            d0 = self.dims("cardboard_box_01")
            sb = min(0.3 / max(d0), (H - 0.012 - top) / d0.z)
            ext = self.place("cardboard_box_01", (x, D - 0.005, top), rot=(0, 0, 0), scale=sb, fixture="R-back-stock", anchor=("c", "max", "min"))
            self.scales.append({"model": "cardboard_box_01", "scale": round(sb, 3), "sized": True})
            self.tickets_for(x, ext[2] - 0.003, top)
            self.box_on_tv += 1
        rest.sort(key=lambda p: -max(self.dims(p["model"])))
        queue = rest[:]
        self.fill_log = []
        self.riser_log = []
        shelf_m = self.mat("shelf", rgb8(150, 108, 70), rough=0.55)

        def place_row(queue, allowed, xa, xb, y_back, z, clear, deep, tag, fixture="R-back-stock"):
            """Greedy fill of one row (the widest piece that fits, left to right) from the queue's models in `allowed`. Returns (pieces placed, width placed)."""
            x = xa + 0.01
            n, wsum = 0, 0.0
            last_model = None
            while True:
                cands = []
                for i, p in enumerate(queue):
                    if p["model"] not in allowed:
                        continue
                    f = fit2(p["model"], clear, deep)
                    if f is None:
                        continue
                    sc_, turn, d = f
                    w = d.x * sc_
                    if x + w <= xb - 0.005:
                        cands.append((w, i, sc_, turn, d))
                if not cands:
                    break
                cands.sort(key=lambda c: -c[0])
                alt = [c for c in cands if queue[c[1]]["model"] != last_model] or cands          # (try 3) not the same model twice running when another fits
                w, i, sc_, turn, d = alt[rnd.randrange(min(3, len(alt)))]            # one of the three widest that fit: the row is not sorted by width
                p = queue[i]
                clk = None
                if p["model"] == "wall_clock":
                    clk = self.next_clock()
                self.place(p["model"], (x + w / 2, y_back, z), rot=(0, 0, turn + rnd.uniform(-JIT, JIT)), scale=sc_, fixture=fixture, anchor=("c", "max", "min"), clock=clk, tag=tag)
                self.scales.append({"model": p["model"], "scale": round(sc_, 3), "sized": bool(p["size"]), "row": tag})
                self.tickets_for(x + w / 2, y_back - d.y * sc_ - 0.008, z)
                last_model = p["model"]
                queue.pop(i)
                n += 1
                wsum += w
                x += w + rnd.uniform(0.008, 0.02)
            return n, wsum
        # the risers on the two television boards: one in every free stretch of 0.20 m or more between and beside the sets
        for z in zt:
            run_a = -1.9
            run_b = TV_LOW_END if z == zt[0] else 0.9
            obst = sorted([(e[0] - 0.01, e[1] + 0.01) for (zz, xx), e in self.tv_ext.items() if zz == z])
            stretches, cur = [], run_a
            for (o0, o1) in obst:
                if o0 > cur:
                    stretches.append((cur, o0))
                cur = max(cur, o1)
            if cur < run_b:
                stretches.append((cur, run_b))
            zr = z + RISER_H
            for (a, b) in stretches:
                if b - a < 0.20:
                    continue
                self.box("riser_%.2f_%.2f" % (z, a), a + 0.005, b - 0.005, D - RISER_D, D - 0.005, zr - BOARD_T, zr, shelf_m, fixture="R-back-stock")
                clear_r = (zt[1] - BOARD_T - zr - 0.015) if z == zt[0] else (H - zr - 0.02)
                n, w = place_row(queue, ALLOW_RISER, a, b, D - 0.005, zr, clear_r, RISER_D - 0.005, "riser")
                self.riser_log.append({"z": z, "x": [round(a, 3), round(b, 3)], "kind": "riser", "length": round(b - a, 3), "n": n, "filled": round(w / (b - a), 3)})
                # the front row on the board, backs against the riser's front edge 5 mm clear of it; the board is 0.35 deep: a piece at most 0.35 - 0.205 - 0.015 deep
                clear_f = (zt[1] - BOARD_T - z - 0.015) if z == zt[0] else (H - z - 0.02)
                # the front row stands on the television board (0.35 deep, the stand-off rule of the TV tiers): its fixture is the TV tier's
                n2, w2 = place_row(queue, ALLOW_FRONT, a, b, D - RISER_D - 0.005, z, clear_f, 0.35 - RISER_D - 0.005 - 0.015, "front", fixture="R-back-tv-tiers")
                self.riser_log.append({"z": z, "x": [round(a, 3), round(b, 3)], "kind": "front", "length": round(b - a, 3), "n": n2, "filled": round(w2 / (b - a), 3)})

        def free_stretches(z, a, b):
            obst = sorted([(x - 0.21, x + 0.21) for x in tv_x.get(z, []) if a - 0.25 <= x <= b + 0.25])
            out, cur = [], a
            for (o0, o1) in obst:
                if o0 > cur:
                    out.append((cur, min(o0, b)))
                cur = max(cur, o1)
            if cur < b:
                out.append((cur, b))
            return out
        # the two ends of the stock wall (and the lower tiers), as before
        for td in self.tier_defs:
            z = td["z"]
            for (a, b, gap, d_board, tv_run) in td["ranges"]:
                if tv_run:
                    continue
                n_in = 0
                for (fa, fb) in free_stretches(z, a, b):
                    x = fa + 0.02
                    while queue:
                        cands = []
                        for i, p in enumerate(queue):
                            f = fit(p["model"], gap, d_board if d_board <= 0.30 else 0.30, size=p["size"])
                            if f is None:
                                continue
                            s, turn, d = f
                            w = d.x * s
                            if x + w <= fb - 0.01:
                                cands.append((w, i, s, turn, d))
                        if not cands:
                            break
                        w, i, s, turn, d = max(cands, key=lambda c: c[0])
                        p = queue[i]
                        clk = self.next_clock() if p["model"] == "wall_clock" else None
                        self.place(p["model"], (x + w / 2, D - 0.005, z), rot=(0, 0, turn + rnd.uniform(-JIT, JIT)), scale=s, fixture="R-back-stock", anchor=("c", "max", "min"), clock=clk)
                        self.scales.append({"model": p["model"], "scale": round(s, 3), "sized": bool(p["size"])})
                        self.tickets_for(x + w / 2, D - 0.30, z)
                        queue.pop(i)
                        n_in += 1
                        x += w + rnd.uniform(0.006, 0.02)
                self.fill_log.append((z, round(a, 2), round(b, 2), n_in))
        self.leftover_count = len(queue)
        self.leftovers = [p["model"] for p in queue]

    CLOCK_TIMES = [(9, 25, 14), (2, 35, 41), (7, 50, 3), (4, 20, 28), (11, 45, 52), (5, 5, 33), (1, 15, 8), (8, 40, 47)]

    def next_clock(self):
        """The next clock's time, never one already shown (13 Oct, close review 4)."""
        k = getattr(self, "_clock_k", 0)
        self._clock_k = k + 1
        return self.CLOCK_TIMES[k % len(self.CLOCK_TIMES)]

    def tickets_for(self, x, y_front, z):
        """A white ticket standing in front of each piece, on the shelf's edge."""
        paper = self.mat("ticket", rgb8(226, 218, 196), rough=0.85)
        w = self.rnd.uniform(0.026, 0.036)
        self.box("ticket", x - w / 2 + self.rnd.uniform(-0.03, 0.03), x + w / 2, y_front - 0.003, y_front + 0.0, z + 0.002, z + 0.002 + 0.02, paper)

    # ------------------------------------------------------------------------------------------------ the counter's goods
    def counter_goods(self):
        cx0, cx1, cy0, cy1 = self.counter_ext
        rnd = self.rnd
        gold = self.mat("gold", rgb8(218, 160, 66), rough=0.25, metal=1.0)
        silver = self.mat("silver", rgb8(204, 204, 208), rough=0.2, metal=1.0)
        black = self.mat("plastic_black", rgb8(24, 24, 24), rough=0.35)
        ticket = self.mat("ticket", rgb8(226, 218, 196), rough=0.85)
        # the raked bed: a parent empty at the bed's front edge turned 25 degrees about x; everything laid on the velvet is a child in the bed's own frame (x along the case, s up the
        # slope, h off the velvet)
        yf, zf = self.rake_origin
        th = math.radians(self.rake_deg)
        rake = bpy.data.objects.new("rake", None)
        self.sc.collection.objects.link(rake)
        rake.location = (0.0, yf, zf)
        rake.rotation_euler = (th, 0.0, 0.0)

        def child(o):
            o.parent = rake
            o.matrix_parent_inverse = Matrix.Identity(4)
            return o
        s_max = (cy1 - 0.04 - yf) / math.cos(th)
        # script:counter_jewellery: rings (tori), watch discs on straps, chains of links; on the velvet, each with a ticket. (13 Oct, SO-07: each item has its left and right extent along the
        # case, tag included, and the next stands clear of the last: try 2's step of 0.05 to 0.10 let a chain, 0.12 long, run through its neighbours and their tags; the watch's disc
        # sits on its strap, z 0.0035 up; a chain's tag stands beyond the chain's end)
        x = cx0 + 0.12
        prev_right = None
        while x < cx1 - 0.35:
            s_ = 0.06 + rnd.random() * 0.32
            kind = rnd.random()
            left, right = (0.015, 0.045) if kind < 0.45 else ((0.018, 0.045) if kind < 0.8 else (0.06, 0.091))
            if prev_right is not None:
                x = max(x, prev_right + 0.01 + left)
            if x >= cx1 - 0.35:
                break
            if kind < 0.45:
                bpy.ops.mesh.primitive_torus_add(major_radius=0.012, minor_radius=0.0032, location=(x, s_, 0.0033))
                o = bpy.context.object
                o.data.materials.append(gold if rnd.random() < 0.7 else silver)
                child(o)
                tag_dx = 0.02
            elif kind < 0.8:
                o = self.cyl("watch", x, s_, 0.0036 + 0.004, 0.018, 0.008, gold if rnd.random() < 0.5 else silver)
                child(o)
                child(self.box("strap", x - 0.008, x + 0.008, s_ - 0.05, s_ + 0.05, 0.0, 0.0035, black))
                tag_dx = 0.02
            else:
                child(self.box("chain", x - 0.06, x + 0.06, s_ - 0.004, s_ + 0.004, 0.0, 0.0045, gold))
                tag_dx = 0.066
            child(self.box("tag", x + tag_dx, x + tag_dx + 0.025, s_ - 0.01, s_ + 0.01, 0.0, 0.0022, ticket))
            prev_right = x + right
            x = prev_right + 0.01 + rnd.random() * 0.04
        # pocket_watch x3, vintage_pocket_watch x3 on the velvet (0.06 largest side), lying on the slope
        for i, (a, xx) in enumerate(zip(["pocket_watch"] * 3 + ["vintage_pocket_watch"] * 3, np.linspace(cx0 + 0.5, cx1 - 0.7, 6))):
            sc_ = 0.06 / max(self.dims(a))
            s_ = 0.14 + 0.05 * (i % 2)
            # the model stands upright; laid face up on the slope: a quarter turn about x (face up), then the rake's 25 degrees
            ypos = yf + s_ * math.cos(th)
            zpos = zf + s_ * math.sin(th)
            rot = (th - math.pi / 2, 0.0, rnd.uniform(-0.4, 0.4))
            ext = self.place(a, (xx, ypos, zpos), rot=rot, scale=sc_, fixture="R-back-counter", anchor=("c", "c", "min"))
        # the till at the counter's right end, on the glass top
        s = 0.42 / max(self.dims("CashRegister_01"))
        self.place("CashRegister_01", (cx1 - 0.40, cy0 + 0.32, 1.05), rot=(0, 0, rnd.uniform(-0.15, 0.15)), scale=s, fixture="R-back-counter")

    # ------------------------------------------------------------------------------------------------ the side walls
    def watch_cards(self, xl, spots, side="left"):
        """script:watch_chain_cards (13 Oct, close review narrow 2): paper cards 0.10 x 0.14 x 0.01 pinned to the board, each with a gold watch and a hanging chain and a ticket under it,
        one mesh. `spots` are (y, z) centres on the left board (x = xl + 0.02 .. 0.03, the face toward +x)."""
        card_m = self.mat("watchcard_paper", rgb8(214, 204, 178), rough=0.85)
        gold = self.mat("gold", rgb8(218, 160, 66), rough=0.25, metal=1.0)
        tk = self.mat("ticket", rgb8(226, 218, 196), rough=0.85)
        V, F, M = [], [], []

        turn = [0.0, 0.0, 0.0]            # (angle, centre y, centre z) of the card being added: its parts turn about its centre (13 Oct, try 3: the 40 cards were two ruled rows)

        def add_box(x0, x1, y0, y1, z0, z1, mi):
            o = len(V)
            ang, cy_, cz_ = turn
            ca_, sa_ = math.cos(ang), math.sin(ang)

            def tp(x, y, z):
                dy, dz = y - cy_, z - cz_
                return (x, cy_ + dy * ca_ - dz * sa_, cz_ + dy * sa_ + dz * ca_)
            V.extend([tp(x0, y0, z0), tp(x1, y0, z0), tp(x1, y1, z0), tp(x0, y1, z0), tp(x0, y0, z1), tp(x1, y0, z1), tp(x1, y1, z1), tp(x0, y1, z1)])
            F.extend([(o + 0, o + 3, o + 2, o + 1), (o + 4, o + 5, o + 6, o + 7), (o + 0, o + 1, o + 5, o + 4), (o + 1, o + 2, o + 6, o + 5), (o + 2, o + 3, o + 7, o + 6), (o + 3, o + 0, o + 4, o + 7)])
            M.extend([mi] * 6)

        def add_disc(x0, x1, yc, zc, r, mi, n=14):
            o = len(V)
            ang, cy_, cz_ = turn
            ca_, sa_ = math.cos(ang), math.sin(ang)
            for xx in (x0, x1):
                for k in range(n):
                    t = 2 * math.pi * k / n
                    py, pz = yc + r * math.cos(t), zc + r * math.sin(t)
                    dy, dz = py - cy_, pz - cz_
                    V.append((xx, cy_ + dy * ca_ - dz * sa_, cz_ + dy * sa_ + dz * ca_))
            F.append(tuple(o + i for i in range(n))[::-1])
            F.append(tuple(o + n + i for i in range(n)))
            for i in range(n):
                F.append((o + i, o + (i + 1) % n, o + n + (i + 1) % n, o + n + i))
            M.extend([mi] * (n + 2))
        for spot in spots:
            y, z = spot[0], spot[1]
            turn[0], turn[1], turn[2] = (spot[2] if len(spot) > 2 else 0.0), y, z
            x0 = xl + 0.021
            add_box(x0, x0 + 0.010, y - 0.05, y + 0.05, z - 0.07, z + 0.07, 0)                       # the card 0.10 x 0.14 x 0.01
            add_disc(x0 + 0.010, x0 + 0.016, y, z + 0.032, 0.022, 1)                                  # the watch
            add_box(x0 + 0.010, x0 + 0.0125, y - 0.002, y + 0.002, z - 0.02, z + 0.012, 1)            # its chain, hanging
            add_box(x0 + 0.010, x0 + 0.0125, y - 0.016, y + 0.016, z - 0.062, z - 0.044, 2)           # the ticket
        me = bpy.data.meshes.new("watch_chain_cards")
        me.from_pydata(V, [], F)
        me.validate()
        for m in (card_m, gold, tk):
            me.materials.append(m)
        for p_, mi in zip(me.polygons, M):
            p_.material_index = mi
        ob = bpy.data.objects.new("watch_chain_cards", me)
        self.sc.collection.objects.link(ob)
        self.fixtures.append({"fixture": "R-left-board", "name": "watch_chain_cards(%d)" % len(spots), "ext": [xl, xl + 0.032, 0.3, 4.2, 0.45, 2.15], "n": len(spots), "boxes_yz": [[round(sp[0] - 0.05, 3), round(sp[0] + 0.05, 3), round(sp[1] - 0.07, 3), round(sp[1] + 0.07, 3)] for sp in spots]})
        return ob

    def tone_material(self, name, f):
        """The material's base-colour map times a grey f (a Multiply node between the map and the shader): a model's white paint made a little less white."""
        m = bpy.data.materials[name]
        nt = m.node_tree
        for l in list(nt.links):
            if l.to_socket.name == "Base Color" and l.to_node.type == "BSDF_PRINCIPLED":
                mix = nt.nodes.new("ShaderNodeMix")
                mix.data_type = "RGBA"
                mix.blend_type = "MULTIPLY"
                mix.inputs[0].default_value = 1.0
                mix.inputs[7].default_value = (f, f, f, 1.0)
                src, to = l.from_socket, l.to_socket
                nt.links.new(src, mix.inputs[6])
                nt.links.new(mix.outputs[2], to)

    def print_variant(self, names, asset, k):
        """Another print for one hung frame (the five frames on the pledge board differ): its own copy of the mesh and of the artwork material, the picture node pointing at
        <asset>_artwork_diff_1k_clean_v<k>.jpg (made by sw_assets.harbour_print)."""
        path = os.path.join(A.POLY, asset, "1k", "textures", "%s_artwork_diff_1k_clean_v%d.jpg" % (asset, k))
        if not os.path.exists(path):
            return
        for nm in names:
            ob = bpy.data.objects[nm]
            ob.data = ob.data.copy()
            for i, m in enumerate(ob.data.materials):
                if m is not None and "artwork" in m.name.lower():
                    m2 = m.copy()
                    for n in m2.node_tree.nodes:
                        if n.type == "TEX_IMAGE" and n.image is not None and "artwork_diff" in n.image.name:
                            n.image = bpy.data.images.load(path, check_existing=True)
                            n.image.colorspace_settings.name = "sRGB"
                    ob.data.materials[i] = m2

    def side_walls(self):
        rnd = self.rnd
        peg = self.image_mat("pegboard", os.path.join(self.tex, "pegboard.png"), tile_m=0.6, rough=0.8)
        batt = self.mat("batten", rgb8(120, 90, 60), rough=0.7)
        ink = self.mat("ink", rgb8(14, 14, 28), rough=0.8)
        # LEFT WALL (x = -W/2, faces +x): pledge board over the whole wall (y 0.3 to 4.2, z 0.45 to 2.15), 0.08 deep
        xl = -W / 2
        for k, (ya, yb) in enumerate(((0.3, 1.6), (1.6, 2.9), (2.9, 4.2))):
            for j, (za, zb) in enumerate(((0.45, 1.3), (1.3, 2.15))):
                self.box("left_peg_%d_%d" % (k, j), xl + 0.012, xl + 0.02, ya + 0.004, yb - 0.004, za + 0.004, zb - 0.004, peg, fixture="R-left-board")
        for k, ya in enumerate((0.3, 2.9)):
            self.box("left_batten_%d" % k, xl, xl + 0.012, ya, ya + 0.04, 0.45, 2.15, batt, fixture="R-left-board")
        # 13 Oct (close review, narrow 2) the board covered with goods at real size (scale 1.0), at most 0.08 off the wall: 5 framed pictures, 2 mirrors, 6 clocks, 2 ukuleles, the two
        # notices and 40 watch-and-chain cards. Turn +90 degrees: the front toward +x. Try 3 (close review 4: the six clocks in two staggered rows, z 1.55 and 1.85): laid out in three bands.
        # LOW band (z 0.52 to 1.03): the five frames side by side (0.752 wide, 0.03 apart). MID band (z 1.08 to 1.38): the 40 watch-and-chain cards in two rows. UPPER band (z 1.40 to 2.15):
        # mirror, ukulele, the six clocks in two staggered rows (z 1.58 and 1.85, +-0.03: 3 in each row, 0.27 m apart along the wall so that no two are more than three in a line and
        # neighbours in different rows clear each other by 0.05 m), ukulele, mirror, and the licence card with the unredeemed-pledges card above it
        def hang(asset, y, z, label, variant=0, clock=None):
            ext = self.place(asset, (xl + 0.022, y, z), rot=(0, 0, math.pi / 2), scale=1.0, fixture="R-left-board", anchor=("min", "c", "c"), clock=clock, tag=label)
            if variant:
                self.print_variant(list(self.last_objs), asset, variant)
            return ext
        for k in range(5):
            hang("hanging_picture_frame_02", 0.30 + 0.376 + k * 0.782, 0.775, "frame", variant=k)
        # 13 Oct, try 2 (PIC-05 measured before the shoulder: the white paint of the frames burnt at the lit edge): the frames' paint is 0.75 of the model's white in every state
        self.tone_material("hanging_picture_frame_02", 0.75)
        hang("ornate_mirror_01", 0.543, 1.775, "mirror")
        hang("Ukulele_01", 0.93, 1.75, "ukulele")
        zrow = {0: 1.58, 1: 1.85, 2: 1.60, 3: 1.88, 4: 1.57, 5: 1.83}
        for i in range(6):
            hang("wall_clock", 1.20 + 0.27 * i, zrow[i], "clock", clock=self.next_clock())
        hang("Ukulele_01", 2.85, 1.75, "ukulele")
        hang("ornate_mirror_01", 3.263, 1.775, "mirror")
        self.flat_card("notice_licence", "notice_licence", xl + 0.03, 3.58, 4.18, 1.55, 1.55 + 0.6 * 200.0 / 512.0, wall="left")
        self.flat_card("notice_unredeemed", "notice_unredeemed", xl + 0.03, 3.64, 4.12, 1.85, 2.01, wall="left")
        lic = (3.58, 4.18, 1.55, 1.55 + 0.6 * 200.0 / 512.0)
        unr = (3.64, 4.12, 1.85, 2.01)
        self.fixtures.append({"fixture": "R-left-notices", "name": "notices", "ext": [xl, xl + 0.035, 3.58, 4.18, 1.55, 2.01]})
        self.fixtures.append({"fixture": "R-left-board", "name": "notice_boxes", "ext": [xl, xl + 0.035, lic[0], lic[1], lic[2], lic[3]], "box_yz": list(lic)})
        self.fixtures.append({"fixture": "R-left-board", "name": "notice_boxes", "ext": [xl, xl + 0.035, unr[0], unr[1], unr[2], unr[3]], "box_yz": list(unr)})
        # the 40 watch-and-chain cards (13 Oct, try 3: in clusters with uneven gaps, each a little up or down and turned by up to 6 degrees; try 2's two ruled rows of 20 read as a grid):
        # two bands of z (1.15 and 1.30, +-0.012) from y 0.42 to 4.10, the pitch 0.145 to 0.215, the lower row begun 0.07 to 0.12 along
        spots = []
        for zc, y0_, n_ in ((1.30, 0.42, 20), (1.15, 0.50, 20)):
            y_ = y0_
            for i in range(n_):
                spots.append((round(y_, 4), round(zc + rnd.uniform(-0.012, 0.012), 4), math.radians(rnd.uniform(-6.0, 6.0))))
                y_ += rnd.uniform(0.145, 0.215) if i % 5 != 4 else rnd.uniform(0.2, 0.26)         # a wider gap after every fifth card
            # (the row is then squeezed or stretched to end at y 4.10)
            last = spots[-1][0]
            first = spots[-n_][0]
            k_ = (4.10 - first) / (last - first)
            for j in range(len(spots) - n_, len(spots)):
                sp = spots[j]
                spots[j] = (round(first + (sp[0] - first) * k_, 4), sp[1], sp[2])
        self.watch_cards(xl, spots)
        # 90 pawn tickets pinned on the pegboard (25 x 12 mm each: one mesh, UVs into the ticket atlas), where nothing hangs: the boxes of everything placed on the board
        keep_out = []
        for q in self.placed:
            if q["fixture"] == "R-left-board":
                e = q["ext"]
                keep_out.append((e[2], e[3], e[4], e[5]))
        for f in self.fixtures:
            if f.get("fixture") == "R-left-board":
                for b_ in f.get("boxes_yz", []) + ([f["box_yz"]] if "box_yz" in f else []):
                    keep_out.append((b_[0], b_[1], b_[2], b_[3]))
        pts = []
        tries = 0
        while len(pts) < 90 and tries < 40000:
            tries += 1
            y, z = rnd.uniform(0.4, 4.1), rnd.uniform(0.5, 2.1)
            if any(a - 0.02 <= y <= b + 0.02 and c - 0.02 <= z <= d + 0.02 for (a, b, c, d) in keep_out):
                continue
            if any(abs(y - p[0]) < 0.05 and abs(z - p[1]) < 0.035 for p in pts):
                continue
            pts.append((y, z))
        V, F, UVs = [], [], []
        for n, (y, z) in enumerate(pts):
            w, h = 0.025, 0.012
            a = rnd.uniform(-0.15, 0.15)
            ca, sa = math.cos(a), math.sin(a)
            cell = rnd.randrange(96)
            cu, cv = (cell % 12) / 12.0, (cell // 12) / 8.0
            base = len(V)
            for (dy, dz), (uu, vv) in zip(((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)), ((0, 0), (1, 0), (1, 1), (0, 1))):
                V.append((xl + 0.0225, y + dy * ca - dz * sa, z + dy * sa + dz * ca))
                UVs.append((cu + uu / 12.0, cv + vv / 8.0))
            F.append((base, base + 1, base + 2, base + 3))
        me = bpy.data.meshes.new("pledge_tickets")
        me.from_pydata(V, [], F)
        uv = me.uv_layers.new(name="UVMap")
        for loop in me.loops:
            uv.data[loop.index].uv = UVs[loop.vertex_index]
        ob = bpy.data.objects.new("pledge_tickets", me)
        self.sc.collection.objects.link(ob)
        ob.data.materials.append(self.image_mat("tickets_atlas", os.path.join(self.tex, "tickets.png"), rough=0.8))
        self.fixtures.append({"fixture": "R-left-board", "name": "pledge_tickets(90)", "ext": [xl, xl + 0.025, 0.4, 4.1, 0.5, 2.1], "n": len(pts)})
        self.n_tickets = len(pts)
        # RIGHT WALL (x = +W/2, faces -x): tools hung flat on pegboard panels over the far part (y 1.3 to 4.2, z 0.45 to 2.15), 0.08 deep in all
        xr = W / 2
        for k, (ya, yb) in enumerate(((1.3, 2.25), (2.25, 3.2), (3.2, 4.2))):
            for j, (za, zb) in enumerate(((0.45, 1.3), (1.3, 2.15))):
                self.box("right_peg_%d_%d" % (k, j), xr - 0.02, xr - 0.012, ya + 0.004, yb - 0.004, za + 0.004, zb - 0.004, peg, fixture="R-right-board")
        for k, ya in enumerate((1.3, 3.2)):
            self.box("right_batten_%d" % k, xr - 0.012, xr, ya, ya + 0.04, 0.45, 2.15, batt, fixture="R-right-board")
        # 13 Oct, try 3 (close review 6): the board is filled by ROWS across its full 2.9 m, each row's tools 0.04 to 0.06 m apart, from the same models at 0.9 to 1.0 of their size, each tool
        # turned so that its thinnest side is against the wall and (the saws and the planes) its long side along the wall or (the rest) up it. Rows by height: saws z 1.85 to 2.10; hammers and
        # pipe wrenches 1.40 to 1.80; pliers and adjustable wrenches 0.95 to 1.35; combination wrenches and the planes 0.50 to 0.90. A tool and the board together stand at most 0.10 off the
        # wall (SO-02's limit): the plane, 0.084 thick, is at 0.9
        t_front = xr - 0.02          # the pegboard's face
        ROWS = [("R1", 1.975, [("handsaw_wood", "h")] * 4),
                ("R2", 1.60, [("cross_pein_hammer", "v"), ("cross_pein_hammer", "v"), ("pipe_wrench", "v")] * 6 + [("cross_pein_hammer", "v")]),
                ("R3", 1.15, [("pliers", "v"), ("pliers", "v"), ("adjustable_wrench", "v")] * 8),
                ("R4", 0.70, [("combination_wrench", "v")] * 5 + [("hand_plane_no4", "h")] + [("combination_wrench", "v")] * 5 + [("hand_plane_no4", "h")] + [("combination_wrench", "v")] * 5 + [("hand_plane_no4", "h")])]
        want = {}
        for g in self.R["room"]["goods"]:
            if g["on"] == "R-right-board":
                want[g["model"]] = want.get(g["model"], 0) + g["n"]
        used = {}
        self.right_rows = {}
        y_lo, y_hi = 1.30 + 0.03, 4.20 - 0.03
        for tag, zc, items in ROWS:
            seq = []
            for asset, orient in items:
                if used.get(asset, 0) >= want.get(asset, 0):
                    continue
                used[asset] = used.get(asset, 0) + 1
                d0 = self.dims(asset)
                order = sorted(range(3), key=lambda i: (d0.x, d0.y, d0.z)[i])
                thin = order[0]
                rot = {0: (0, 0, 0), 1: (0, 0, math.radians(-90)), 2: (0, math.radians(-90), 0)}[thin]
                d1 = self.dims(asset, rot)
                # d1.x is the thin side (against the wall); y and z are the tool's face. 'h': the longer of y and z along the wall (y); 'v': along z. A quarter turn about the wall's normal swaps them
                long_is_y = d1.y >= d1.z
                if (orient == "h") != long_is_y:
                    qm = Matrix.Rotation(math.radians(90.0), 3, "X") @ Euler(rot, "XYZ").to_matrix()
                    rot = tuple(qm.to_euler("XYZ"))
                d2 = self.dims(asset, rot)
                s_ = min(1.0, (0.10 - 0.02 - 0.004) / d2.x)
                if s_ < 0.9 - 1e-9:
                    continue
                seq.append((asset, rot, s_, d2.y * s_, d2.z * s_))
            gaps = [rnd.uniform(0.04, 0.06) for _ in range(max(len(seq) - 1, 0))]
            # a row as long as the board allows: drop the last tools until it fits, then centre it
            while seq and sum(t[3] for t in seq) + sum(gaps[:len(seq) - 1]) > y_hi - y_lo:
                seq.pop()
            total = sum(t[3] for t in seq) + sum(gaps[:max(len(seq) - 1, 0)])
            y = y_lo + ((y_hi - y_lo) - total) / 2.0
            n_row = 0
            for k, (asset, rot, s_, wy, hz) in enumerate(seq):
                self.place(asset, (t_front, y + wy / 2, zc), rot=rot, scale=s_, fixture="R-right-board", anchor=("max", "c", "c"), tag=tag)
                n_row += 1
                y += wy + (gaps[k] if k < len(gaps) else 0.0)
            self.right_rows[tag] = {"z_centre": zc, "n": n_row, "span": round(total, 3)}
        # near end: two ukuleles hung by their heads and the ornate mirror, flat to the wall (0.07)
        for k, y in enumerate((0.80, 1.10)):
            s = 0.62 / max(self.dims("Ukulele_01"))
            self.place("Ukulele_01", (xr - 0.004, y, 1.62), rot=(0, 0, math.radians(-90 + 5 * (k * 2 - 1) * 0)), scale=s, fixture="R-right-hung", anchor=("max", "c", "c"))
        s = 0.42 / max(self.dims("ornate_mirror_01"))
        self.place("ornate_mirror_01", (xr - 0.004, 0.45, 1.30), rot=(0, 0, math.radians(-90)), scale=s, fixture="R-right-hung", anchor=("max", "c", "c"))
        # floor mat (flat)
        self.box("door_mat", -2.45, -1.55, 0.15, 0.85, 0.0, 0.012, self.mat("mat", rgb8(40, 30, 24), rough=0.95), fixture="R-floor-mat")

    # ------------------------------------------------------------------------------------------------ lights and camera
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
            ld.cycles.is_portal = False if hasattr(ld, "cycles") else False
            o = bpy.data.objects.new(name, ld)
            self.sc.collection.objects.link(o)
            o.location, o.rotation_euler = loc, rot
            return o
        # daylight: an overcast sky as an area light the size of the card, on its plane, shining into the room (6500 K)
        self.L_day = area("daylight", (0.0, -0.04, H / 2), (math.pi / 2, 0.0, 0.0), W, H, (0.96, 0.97, 1.0))
        # the three T12 battens, cool white 4000 K: each a 1.5 x 0.09 area light under its diffuser
        self.L_tube = []
        for k, t in enumerate(self.R["room"]["lights"]["tubes"]):
            self.L_tube.append(area("tube_light_%d" % k, (0.0, t["y"], H - 0.03), (0.0, 0.0, 0.0), 1.5, 0.09, (1.0, 0.89, 0.76)))
        # sodium wash through the front (linear 1.0, 0.25, 0.0: the game's lantern_linear_rgb), and the back-room light (2700 K) in the doorway's room
        self.L_sod = area("sodium", (0.0, -0.04, H * 0.9), (math.pi / 2 - 0.3, 0.0, 0.0), W, 0.5, (1.0, 0.25, 0.0))
        self.L_back = area("backroom_light", (1.9, D + 1.2, H - 0.1), (0.0, 0.0, 0.0), 0.9, 0.3, (1.0, 0.71, 0.45))
        self.sodium_rgb = tuple(self.L_sod.data.color)

    def camera(self):
        cam = bpy.data.cameras.new("cam")
        cam.sensor_fit = "HORIZONTAL"
        cam.angle = 2.0 * math.atan(W / (2.0 * CAM_D))
        o = bpy.data.objects.new("cam", cam)
        self.sc.collection.objects.link(o)
        o.location = (0.0, -CAM_D, H / 2.0)
        o.rotation_euler = (math.pi / 2.0, 0.0, 0.0)
        self.sc.camera = o
        self.cam = o

    def set_state(self, state, P):
        """P: the calibrated energies {day, tube, sodium_ratio, back_day, back_nl, back_nd, diff_emit}."""
        tube_w = P["tube"]
        for k, o in enumerate(self.L_tube):
            o.data.energy = tube_w * (0.35 if k == len(self.L_tube) - 1 else 1.0) if state in ("day", "night_lit") else 0.0
        self.L_day.data.energy = P["day"] if state == "day" else 0.0
        self.L_sod.data.energy = P["sodium_ratio"] * tube_w * len(self.L_tube) if state == "night_dark" else 0.0
        self.L_back.data.energy = {"day": P["back_day"], "night_lit": P["back_nl"], "night_dark": P["back_nd"]}[state]
        em = P["diff_emit"] if state in ("day", "night_lit") else 0.0
        self.diff_m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = em

    def render(self, path, samples, res, state=None):
        sc = self.sc
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = samples
        sc.cycles.use_denoising = True
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
        sc.cycles.use_adaptive_sampling = True
        sc.cycles.adaptive_threshold = 0.01
        sc.cycles.max_bounces = 6
        sc.cycles.glossy_bounces = 4
        sc.cycles.transmission_bounces = 4
        sc.cycles.caustics_reflective = False
        sc.cycles.caustics_refractive = False
        sc.cycles.sample_clamp_indirect = 12.0
        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
        sc.view_settings.exposure = 0.0
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.resolution_percentage = 100
        sc.render.image_settings.file_format = "PNG"
        sc.render.image_settings.color_mode = "RGB"
        sc.render.image_settings.color_depth = "8"
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)


ROLLOFF = {"from": 232, "slope": 0.45}


def rolloff(path):
    """A highlight shoulder on the 8-bit picture: values above 232 are compressed (232 + 0.45 x the excess, so 255 becomes 242), so that the tubes, the white cards and the
    clock dials stay under PIC-05's burnt level (250) without clipping to flat white. Below 232 nothing changes."""
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    f, k = ROLLOFF["from"], ROLLOFF["slope"]
    out = np.where(im > f, f + (im - f) * k, im)
    Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(path)


def rolloff_all(rooms_dir):
    """Apply the shoulder to every picture of a finished room render once (the JSON beside them records it)."""
    jp = os.path.join(rooms_dir, "pawnbroker.json")
    rec = json.load(open(jp))
    if rec.get("highlight_rolloff"):
        return False
    for s_ in STATES:
        rolloff(os.path.join(rooms_dir, "pawnbroker_%s.png" % s_))
    rec["highlight_rolloff"] = ROLLOFF
    json.dump(rec, open(jp, "w"), indent=1)
    return True


def luma_stats(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    y = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
    return float(y.mean())


# ---------------------------------------------------------------------------------------------------------------------------------- the driver
DEFAULT_P = {"day": 900.0, "tube": 60.0, "sodium_ratio": 0.06, "back_day": 14.0, "back_nl": 25.0, "back_nd": 4.0, "diff_emit": 0.5}
TARGET_MEAN = {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7}


def build_scene(work, T=None):
    T = T or A.load_target()
    r = Room(work, T)
    r.shell()
    r.back_fixtures()
    r.stock()
    r.counter_goods()
    r.side_walls()
    r.lights()
    r.camera()
    return r


def calibrate(r, work, log=print, res=(768, 348), samples=24):
    """Set the light strengths so each state's mean luma meets the approved picture's (119.5, 79.8, 17.7): tubes on night_lit, the sky on day, the back-room light on night_dark."""
    P = dict(DEFAULT_P)
    tmp = os.path.join(work, "cal.png")

    def measure(state):
        r.set_state(state, P)
        r.render(tmp, samples, res)
        return luma_stats(tmp)

    def tune(key, state, lo_hi=(1e-3, 1e5), iters=4):
        for _ in range(iters):
            m = measure(state)
            tgt = TARGET_MEAN[state]
            log("   calibrate %s: %s=%.4g -> mean %.1f (target %.1f)" % (state, key, P[key], m, tgt))
            if abs(m - tgt) / tgt < 0.03:
                break
            # display luma goes about as the 1/2.2 power of the light: update by the ratio to that power
            f = (tgt / max(m, 1.0)) ** 2.2
            P[key] = float(np.clip(P[key] * f, *lo_hi))
        return P[key]
    tune("tube", "night_lit")
    tune("day", "day")
    tune("back_nd", "night_dark")
    P["measured"] = {s: measure(s) for s in STATES}
    json.dump(P, open(os.path.join(work, "light_params.json"), "w"), indent=1)
    return P


def render_states(r, work, P, out_dir, samples=128, res=PIX, states=STATES, log=print):
    import time
    os.makedirs(out_dir, exist_ok=True)
    times = {}
    record = {"shop": "pawnbroker", "w": W, "h": H, "d": D, "camera_d": CAM_D, "pixels": list(res), "states": {}, "made_by": "production/cloud-week/kit/shop-windows/build_ritas.py (sw_room.py)", "samples": samples, "highlight_rolloff": ROLLOFF}
    raw_dir = os.path.join(out_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    record["pre_shoulder_burnt_share"] = {}
    for s in states:
        r.set_state(s, P)
        path = os.path.join(out_dir, "pawnbroker_%s.png" % s)
        t0 = time.time()
        r.render(path, samples, res)
        # the highlight shoulder is a Judgement (13 Oct, close review narrow 10): PIC-05 (at most 1 per cent of the pixels at 250 or above) is measured on the render BEFORE it, and the
        # raw render is kept beside the picture (rooms/raw/); the shoulder only keeps what is white from clipping flat in the game's picture
        raw_path = os.path.join(raw_dir, "pawnbroker_%s_raw.png" % s)
        shutil.copyfile(path, raw_path)
        raw = np.asarray(Image.open(raw_path).convert("RGB"))
        record["pre_shoulder_burnt_share"][s] = round(float((raw.max(axis=2) >= 250).mean()), 5)
        rolloff(path)
        times[s] = round(time.time() - t0, 1)
        record["states"][s] = os.path.basename(path)
        log("render %s: %.0f s, mean luma %.1f, burnt share before the shoulder %.4f" % (s, times[s], luma_stats(path), record["pre_shoulder_burnt_share"][s]))
    for s in STATES:
        record["states"].setdefault(s, "pawnbroker_%s.png" % s)
    json.dump(record, open(os.path.join(out_dir, "pawnbroker.json"), "w"), indent=1)
    return times
