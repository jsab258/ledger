"""The room class of the house windows' pictures: materials, model templates with the glass kept, placement, Cycles render.

Copied on 14 October 2026 (03:13 UTC) from production/cloud-week/kit/shop-windows/sw_room.py (md5 23f5d4c582194c0eef6974ff7dce858a at the copy; that day's version carries the batch B changes: the glass of a good
is kept as a see-through material, `keep_glass`) and TRIMMED: Rita's pawnbroker's fixtures, stock, display and calibration are not copied; what is kept is the shop kit's Room class's mat, image_mat, box, cyl, template,
see_through, dims, hand_angle, place and render, as they were. The house rooms' own class is hw_roomgen.HRoom, which derives from this.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Vector, Matrix, Euler  # noqa: E402
import hw_assets as A  # noqa: E402

STATES = ("day", "night_lit", "night_dark")
BOARD_T = 0.025
GLASSY = ("glass", "lense", "lens_glass")
KEEP_BLEND = {}


def srgb_to_lin(c):
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c)


def rgb8(r, g, b):
    return srgb_to_lin((r / 255.0, g / 255.0, b / 255.0))


class Room:
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

        # 14 October (batch B, from the ironmonger's close review, fault 2; a shared-kit change): the glass of a good (a bulb's envelope, a lantern's chimney, a lens, a clock's cover) is kept, as a
        # see-through Principled material (transmission 1, nothing alpha-blended: DSP-02 still holds), where the room class asks for it (`keep_glass`: the generated shops; Rita's room is unchanged). A material
        # that is blended and not glass (foliage and labels cut out by an opacity map that is not in the 1k set) is still left out. The audit says, per model, how many of its meshes there are and what
        # was dropped (DSP-05 reads it).
        audit = {"source_meshes": len(meshes), "glass_kept": [], "dropped": []}
        if getattr(self, "keep_glass", False):
            for o in meshes:
                for sl in o.material_slots:
                    m0 = sl.material
                    if m0 is not None and any(g in m0.name.lower() for g in GLASSY) and not any(k in m0.name.lower() for k in KEEP_BLEND.get(asset, ())):
                        audit["glass_kept"].append("%s:%s" % (o.name, m0.name))
                        sl.material = self.see_through(m0)

        def is_glassy(m):
            if m is not None and any(k in m.name.lower() for k in KEEP_BLEND.get(asset, ())):
                m.surface_render_method = "DITHERED"          # a model whose blended material is real geometry (the brooms' bristles), kept: dithered, as the display's alpha materials are
                return False
            return m is not None and (getattr(m, "surface_render_method", "") == "BLENDED" or any(g in m.name.lower() for g in GLASSY))
        # a mesh whose every slot is glass or alpha goes; in a mesh that mixes them (the clocks' faces) the glass faces are cut out
        keep = []
        for o in meshes:
            gidx = [i for i, ms in enumerate(o.material_slots) if is_glassy(ms.material)]
            if gidx and len(gidx) == len(o.material_slots):
                audit["dropped"].append("%s (all %d materials blended or glass: %s)" % (o.name, len(gidx), ", ".join(ms.material.name for ms in o.material_slots if ms.material)))
                continue
            if gidx:
                audit["dropped"].append("%s (faces of %s cut out)" % (o.name, ", ".join(o.material_slots[i].material.name for i in gidx)))
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
        elif audit["dropped"]:
            # nothing would be left (a crate whose one material is blended): the model stays whole, as its glTF has it
            audit["kept_whole"] = audit["dropped"]
            audit["dropped"] = []
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
        pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
        lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        audit["kept_meshes"] = len(meshes)
        self.__dict__.setdefault("audit", {})[asset] = audit
        self.templates[key] = (meshes, lo, hi)
        return self.templates[key]

    def see_through(self, m0):
        """The material that stands for a good's glass (see `template`): Principled, base colour white, roughness 0.05, IOR 1.5, transmission 1, alpha 1 (not blended). In the room's own pictures the shadow-ray
        trick of `mat(glass=True)` is added (lesson 19: a lamp's light reaches what stands under a pane); for a glb (the display) `shadow_trick` is False and the plain Principled is what is exported."""
        key = "pane_see_through" + ("_st" if getattr(self, "shadow_trick", False) else "")
        if key in self.mats:
            return self.mats[key]
        if getattr(self, "shadow_trick", False):
            m = self.mat(key, (1.0, 1.0, 1.0), rough=0.05, glass=True)
            m.node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value = 1.5
            m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.05
            return m
        m = bpy.data.materials.new(key)
        m.use_nodes = True
        p = m.node_tree.nodes["Principled BSDF"]
        p.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        p.inputs["Roughness"].default_value = 0.05
        p.inputs["IOR"].default_value = 1.5
        p.inputs["Transmission Weight"].default_value = 1.0
        p.inputs["Alpha"].default_value = 1.0
        self.mats[key] = m
        return m

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

    def render(self, path, samples, res, state=None, exr=False):
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
        sc.render.image_settings.file_format = "OPEN_EXR" if exr else "PNG"      # exr: the scene-linear float picture, for the lit pictures' highlight roll-off before the 8-bit write (14 October)
        sc.render.image_settings.color_mode = "RGB"
        sc.render.image_settings.color_depth = "32" if exr else "8"
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
