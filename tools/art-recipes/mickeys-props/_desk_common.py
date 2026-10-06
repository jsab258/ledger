"""Shared steps for the desk props of Mickey's front office (set 1).

Each prop script (radio-base-station.py, telephone.py, jug-kettle.py, mugs.py,
ashtray.py, desk-lamp.py) builds its prop from nothing with these helpers and
then calls finish_prop(), which does the method of
production/research/shop-window-interiors/MICKEYS-OTHER-DIRECTION-2026-10-04.md
section 4 in one place:

  - mid-poly parts, each bevelled with Harden Normals, then a Weighted Normal
    modifier (face area, keep sharp); no high-to-low bake;
  - the parts joined into one mesh, origin at the centre of the base on z=0,
    front toward -Y;
  - one UV map (Smart UV Project, uniform texel scale, margin) checked for
    overlaps with Blender's own Select Overlap;
  - ambient occlusion and Cycles Pointiness baked into two colour attributes,
    "ao" (1 = open, 0 = occluded) and "edges" (0 = flat or concave, 1 = sharp
    convex edge), for a master material's dirt and edge wear;
  - glTF binary out (Y-up, modifiers applied); the two masks travel packed in
    COLOR_0 (red = ao, green = edges, blue 0, alpha 1), from the attribute
    "ao_edges"; the .blend keeps "ao" and "edges" as well; a preview render.

No textures are used: every material is a plain PBR value set (base colour,
roughness, metallic), so nothing here has an outside source.

Run a prop:  blender.exe -b --factory-startup -P <prop>.py [-- --no-render]
"""
import json
import math
import os
import struct
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

GLB_DIR = r"F:\LedgerTools\game-inputs\production\assets\mickeys-props"
BLEND_DIR = r"F:\LedgerTools\mickeys-props\blend"
PREVIEW_DIR = r"F:\LedgerTools\mickeys-props\previews"


# --------------------------------------------------------------------------
# command line and scene

def cli():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return {"render": "--no-render" not in argv, "argv": argv}


def reset():
    PARTS.clear()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.scale_length = 1.0
    return sc


def lin(c):
    """sRGB 0-1 -> linear."""
    def f(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return tuple(f(v) for v in c)


def material(name, srgb, rough, metal=0.0, transmission=0.0, ior=1.5,
             coat=0.0, spec=0.5):
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    b = m.node_tree.nodes.get("Principled BSDF")
    c = lin(srgb)
    b.inputs["Base Color"].default_value = (c[0], c[1], c[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = spec
    if transmission > 0:
        b.inputs["Transmission Weight"].default_value = transmission
        b.inputs["IOR"].default_value = ior
        # Eevee preview only: raytraced refraction through a solid object
        for k, v in (("use_raytrace_refraction", True), ("refraction_depth", 0.0),
                     ("surface_render_method", "DITHERED"), ("thickness_mode", "SLAB")):
            if hasattr(m, k):
                try:
                    setattr(m, k, v)
                except Exception:
                    pass
    if coat > 0:
        b.inputs["Coat Weight"].default_value = coat
        b.inputs["Coat Roughness"].default_value = 0.05
    m.diffuse_color = (c[0], c[1], c[2], 1.0)
    m.roughness = rough
    m.metallic = metal
    return m


# --------------------------------------------------------------------------
# building parts (all geometry is written in world space; objects stay at
# the identity transform so custom normals never need re-transforming)

PARTS = []


def _link(name, bm, mat):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    if mat is not None:
        me.materials.append(mat)
    PARTS.append(ob)
    return ob


def mat4(loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    from mathutils import Euler
    return (Matrix.Translation(Vector(loc)) @ Euler(rot, "XYZ").to_matrix().to_4x4()
            @ Matrix.Diagonal((scale[0], scale[1], scale[2], 1.0)))


def box(name, size, loc=(0, 0, 0), mat=None, rot=(0, 0, 0), bevel=0.0,
        segs=2, matrix=None):
    """Box of size (x, y, z) centred at loc (after rotation)."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    m = (matrix if matrix is not None else Matrix.Identity(4)) @ mat4(loc, rot, size)
    bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
    ob = _link(name, bm, mat)
    if bevel > 0:
        # never let the bevel meet itself: that leaves zero-area faces
        bevel_part(ob, min(bevel, 0.4 * min(size)), segs)
    return ob


def box_z(name, x0, x1, y0, y1, z0, z1, mat=None, bevel=0.0, segs=2):
    return box(name, (x1 - x0, y1 - y0, z1 - z0),
               ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), mat, bevel=bevel, segs=segs)


def cyl(name, r, depth, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, segs=32,
        r2=None, bevel=0.0, bsegs=2, matrix=None, cap=True):
    """Cylinder (or cone with r2) along local Z, centred at loc."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=cap, cap_tris=False, segments=segs,
                          radius1=r, radius2=(r if r2 is None else r2), depth=depth)
    m = (matrix if matrix is not None else Matrix.Identity(4)) @ mat4(loc, rot)
    bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
    ob = _link(name, bm, mat)
    if bevel > 0:
        bevel_part(ob, min(bevel, 0.4 * min(depth, r, r if r2 is None else max(r2, 1e-4))), bsegs)
    return ob


def lathe(name, profile, segs=48, mat=None, matrix=None, mat_of=None):
    """Spin a profile [(r, z), ...] about Z. Ends at r=0 are closed to a pole.
    mat_of(i) may return a material slot index for the faces swept from
    profile segment i (slots then come from the object's material list)."""
    bm = bmesh.new()
    rings = []
    for k in range(segs):
        a = 2 * math.pi * k / segs
        ring = []
        for (r, z) in profile:
            ring.append(bm.verts.new((r * math.cos(a), r * math.sin(a), z)))
        rings.append(ring)
    n = len(profile)
    for k in range(segs):
        r0, r1 = rings[k], rings[(k + 1) % segs]
        for i in range(n - 1):
            vs = [r0[i], r1[i], r1[i + 1], r0[i + 1]]
            # collapse poles
            uniq = []
            for v in vs:
                if all((v.co - u.co).length > 1e-9 for u in uniq):
                    uniq.append(v)
            if len(uniq) < 3:
                continue
            f = bm.faces.new(uniq)
            if mat_of is not None:
                f.material_index = mat_of(i)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if matrix is not None:
        bmesh.ops.transform(bm, matrix=matrix, verts=bm.verts)
    return _link(name, bm, mat)


def catmull(points, per_seg=8):
    """Catmull-Rom through points (list of Vector), returns dense list."""
    P = [Vector(p) for p in points]
    P = [P[0] + (P[0] - P[1])] + P + [P[-1] + (P[-1] - P[-2])]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for s in range(per_seg):
            t = s / per_seg
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-2].copy())
    return out


def resample(pts, step):
    """Even arc-length resample of a polyline."""
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + (b - a).length)
    total = L[-1]
    n = max(2, int(total / step) + 1)
    out, j = [], 0
    for k in range(n):
        s = total * k / (n - 1)
        while j < len(L) - 2 and L[j + 1] < s:
            j += 1
        seg = L[j + 1] - L[j]
        t = 0 if seg == 0 else (s - L[j]) / seg
        out.append(pts[j].lerp(pts[j + 1], t))
    return out, total


def frames(pts):
    """Parallel-transport frames (T, N, B) along a polyline."""
    T = []
    for i in range(len(pts)):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        T.append((b - a).normalized())
    up = Vector((0, 0, 1)) if abs(T[0].z) < 0.9 else Vector((1, 0, 0))
    N = [T[0].cross(up).normalized()]
    for i in range(1, len(pts)):
        n = N[-1] - T[i] * N[-1].dot(T[i])
        if n.length < 1e-9:
            n = N[-1]
        N.append(n.normalized())
    B = [t.cross(n) for t, n in zip(T, N)]
    return T, N, B



def _ring_uvs(bm, rings, closed_n, perim, chunk=0.06):
    """Analytic UVs for a ring sweep: u around, v along, cut into islands of
    about `chunk` metres so a long cord packs well; tags faces '_tube' = 1."""
    uvl = bm.loops.layers.uv.get("UVMap") or bm.loops.layers.uv.new("UVMap")
    tag = bm.faces.layers.int.get("_tube") or bm.faces.layers.int.new("_tube")
    L = [0.0]
    for i in range(1, len(rings)):
        a = sum((v.co for v in rings[i - 1]), Vector()) / len(rings[i - 1])
        b = sum((v.co for v in rings[i]), Vector()) / len(rings[i])
        L.append(L[-1] + (b - a).length)
    start = 0
    starts = []
    for i in range(len(rings)):
        if L[i] - L[start] > chunk:
            start = i
        starts.append(start)
    lookup = {}
    for i in range(len(rings) - 1):
        s0 = L[starts[i]]
        for k in range(closed_n):
            lookup[(i, k)] = (s0, L[i] - s0, L[i + 1] - s0)
    return uvl, tag, lookup


def _assign_ring_faces(bm, rings, n, perim, uvl, tag, lookup, faces):
    for (i, k), f in faces.items():
        _, v0, v1 = lookup[(i, k)]
        u0, u1 = perim * k / n, perim * (k + 1) / n
        uv = {rings[i][k]: (u0, v0), rings[i][(k + 1) % n]: (u1, v0),
              rings[i + 1][(k + 1) % n]: (u1, v1), rings[i + 1][k]: (u0, v1)}
        for l in f.loops:
            l[uvl].uv = uv[l.vert]
        f[tag] = 1

def tube(name, pts, radius, sides=8, mat=None, caps=True, radii=None):
    """Sweep a circle along a polyline (pts already dense)."""
    T, N, B = frames(pts)
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bm.faces.layers.int.new("_tube")
    rings = []
    for i, p in enumerate(pts):
        r = radius if radii is None else radii[i]
        ring = []
        for k in range(sides):
            a = 2 * math.pi * k / sides
            ring.append(bm.verts.new(p + (N[i] * math.cos(a) + B[i] * math.sin(a)) * r))
        rings.append(ring)
    faces = {}
    for i in range(len(rings) - 1):
        for k in range(sides):
            faces[(i, k)] = bm.faces.new([rings[i][k], rings[i][(k + 1) % sides],
                                          rings[i + 1][(k + 1) % sides], rings[i + 1][k]])
    uvl, tag, lookup = _ring_uvs(bm, rings, sides, 2 * math.pi * radius)
    _assign_ring_faces(bm, rings, sides, 2 * math.pi * radius, uvl, tag, lookup, faces)
    if caps:
        for f in (bm.faces.new(list(reversed(rings[0]))), bm.faces.new(rings[-1])):
            f[tag] = 0
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _link(name, bm, mat)


def coil(path_pts, coil_r, pitch, step=None, floor_z=None):
    """Points of a helix wound around a path (a coiled cord). floor_z keeps
    the turns that lie on the desk from dipping through it."""
    if step is None:
        step = pitch / 10.0
    pts, total = resample(path_pts, step)
    T, N, B = frames(pts)
    out = []
    s = 0.0
    for i, p in enumerate(pts):
        if i:
            s += (pts[i] - pts[i - 1]).length
        a = 2 * math.pi * s / pitch
        q = p + (N[i] * math.cos(a) + B[i] * math.sin(a)) * coil_r
        if floor_z is not None and q.z < floor_z:
            q.z = floor_z
        out.append(q)
    return out


def profile_sweep(name, pts, profile, mat=None, caps=True, scale=None):
    """Sweep a closed 2D profile [(u, v), ...] (u along N, v along B)."""
    T, N, B = frames(pts)
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bm.faces.layers.int.new("_tube")
    rings = []
    for i, p in enumerate(pts):
        s = 1.0 if scale is None else scale[i]
        rings.append([bm.verts.new(p + (N[i] * u + B[i] * v) * s) for (u, v) in profile])
    n = len(profile)
    faces = {}
    for i in range(len(rings) - 1):
        for k in range(n):
            faces[(i, k)] = bm.faces.new([rings[i][k], rings[i][(k + 1) % n],
                                          rings[i + 1][(k + 1) % n], rings[i + 1][k]])
    perim = sum((Vector(profile[k] + (0,)) - Vector(profile[(k + 1) % n] + (0,))).length
                for k in range(n))
    uvl, tag, lookup = _ring_uvs(bm, rings, n, perim)
    _assign_ring_faces(bm, rings, n, perim, uvl, tag, lookup, faces)
    if caps:
        for f in (bm.faces.new(list(reversed(rings[0]))), bm.faces.new(rings[-1])):
            f[tag] = 0
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _link(name, bm, mat)


def rounded_rect(w, h, r, n=4):
    """Closed rounded-rectangle profile, counter-clockwise."""
    out = []
    cs = [(w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
          (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)]
    for cx, cy, a0 in cs:
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def ellipse(w, h, n=12):
    return [(w / 2 * math.cos(2 * math.pi * k / n), h / 2 * math.sin(2 * math.pi * k / n))
            for k in range(n)]


def extrude_profile(name, outline, z0, z1, mat=None, plane="XY", offset=(0, 0, 0)):
    """Prism from a closed outline: plane 'XY' extrudes along Z,
    'XZ' along Y (outline as (x, z)), 'YZ' along X (outline as (y, z))."""
    bm = bmesh.new()

    def P(a, b, c):
        if plane == "XY":
            v = (a, b, c)
        elif plane == "XZ":
            v = (a, c, b)
        else:
            v = (c, a, b)
        return (v[0] + offset[0], v[1] + offset[1], v[2] + offset[2])
    lo = [bm.verts.new(P(a, b, z0)) for a, b in outline]
    hi = [bm.verts.new(P(a, b, z1)) for a, b in outline]
    n = len(outline)
    bm.faces.new(lo)
    bm.faces.new(hi)
    for k in range(n):
        bm.faces.new([lo[k], lo[(k + 1) % n], hi[(k + 1) % n], hi[k]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _link(name, bm, mat)


# --------------------------------------------------------------------------
# finishing: bevel with harden normals, weighted normals, join

def bevel_part(ob, width, segs=2, angle=30.0, harden=True):
    md = ob.modifiers.new("Bevel", "BEVEL")
    md.width = width
    md.segments = segs
    md.limit_method = "ANGLE"
    md.angle_limit = math.radians(angle)
    md.harden_normals = harden
    md.use_clamp_overlap = True
    md.miter_outer = "MITER_ARC"
    return md


def smooth_part(ob, sharp_angle=35.0):
    me = ob.data
    me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    try:
        me.set_sharp_from_angle(angle=math.radians(sharp_angle))
    except Exception:
        pass


def densify(ob, longest=0.06, spacing=0.045):
    """Split long edges so vertex-baked masks have samples along a part, not
    only at its (often buried) ends."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    groups = {}
    for e in bm.edges:
        L = e.calc_length()
        if L > longest:
            groups.setdefault(int(math.ceil(L / spacing)) - 1, []).append(e)
    for cuts, edges in sorted(groups.items(), reverse=True):
        edges = [e for e in edges if e.is_valid]
        if edges:
            bmesh.ops.subdivide_edges(bm, edges=edges, cuts=cuts, use_grid_fill=True)
    bm.to_mesh(ob.data)
    bm.free()


def finish_parts(name, sharp_angle=35.0):
    """Smooth + weighted normals on every part, apply, join into one mesh."""
    ctx = bpy.context
    for ob in PARTS:
        if not ob.get("no_dense"):
            densify(ob)
    for ob in PARTS:
        smooth_part(ob, ob.get("sharp_angle", sharp_angle))
        if not ob.get("no_wn"):
            wn = ob.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
            wn.mode = "FACE_AREA"
            wn.weight = 50
            wn.keep_sharp = True
    dg = ctx.evaluated_depsgraph_get()
    for ob in PARTS:
        ev = ob.evaluated_get(dg)
        me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=dg)
        # clean what a clamped bevel can leave: coincident vertices and
        # zero-area faces (they show as UV overlaps and shading specks)
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=2e-6)
        bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=2e-6)
        bm.to_mesh(me)
        bm.free()
        old = ob.data
        ob.modifiers.clear()
        ob.data = me
        bpy.data.meshes.remove(old)
    bpy.ops.object.select_all(action="DESELECT")
    for ob in PARTS:
        ob.select_set(True)
    ctx.view_layer.objects.active = PARTS[0]
    bpy.ops.object.join()
    ob = ctx.view_layer.objects.active
    ob.name = name
    ob.data.name = name
    PARTS.clear()
    PARTS.append(ob)
    return ob


# --------------------------------------------------------------------------
# UVs, bake, checks, export

def uv_unwrap(ob, margin=0.004):
    """Smart UV Project for every face not swept with analytic UVs, then one
    pack of all islands at a common texel scale."""
    ctx = bpy.context
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    ctx.view_layer.objects.active = ob
    me = ob.data
    if "UVMap" not in me.uv_layers:
        while len(me.uv_layers):
            me.uv_layers.remove(me.uv_layers[0])
        me.uv_layers.new(name="UVMap")
    me.uv_layers.active = me.uv_layers["UVMap"]
    tube = me.attributes.get("_tube")
    flags = [0] * len(me.polygons)
    if tube is not None:
        tube.data.foreach_get("value", flags)
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(me)
    for f, t in zip(bm.faces, flags):
        f.select = not t
    bmesh.update_edit_mesh(me)
    bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=margin,
                             area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
    bpy.ops.mesh.select_all(action="SELECT")
    ctx.scene.tool_settings.use_uv_select_sync = True
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.average_islands_scale()
    bpy.ops.uv.pack_islands(rotate=True, margin=margin)
    ctx.scene.tool_settings.use_uv_select_sync = False
    bpy.ops.object.mode_set(mode="OBJECT")
    if me.attributes.get("_tube") is not None:
        me.attributes.remove(me.attributes["_tube"])


def uv_overlaps(ob):
    """Faces Blender's Select Overlap flags (0 = no overlaps)."""
    ctx = bpy.context
    ts = ctx.scene.tool_settings
    ts.use_uv_select_sync = False
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    ctx.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="DESELECT")
    bpy.ops.uv.select_overlap(extend=False)
    bm = bmesh.from_edit_mesh(ob.data)
    n = 0
    for f in bm.faces:
        if getattr(f, "uv_select", False) or all(getattr(l, "uv_select_vert", False)
                                                 for l in f.loops):
            n += 1
    bpy.ops.object.mode_set(mode="OBJECT")
    return n


def _ensure_world():
    sc = bpy.context.scene
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    return sc.world


def bake_masks(ob, ao_distance, edge_span=0.08, samples=64):
    """Bake AO and pointiness into colour attributes 'ao' and 'edges'."""
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    world = _ensure_world()
    world.light_settings.distance = ao_distance
    me = ob.data
    for nm in ("ao", "edges"):
        a = me.color_attributes.get(nm)
        if a:
            me.color_attributes.remove(a)
    ao = me.color_attributes.new("ao", "FLOAT_COLOR", "POINT")
    ed = me.color_attributes.new("edges", "FLOAT_COLOR", "POINT")
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bk = sc.render.bake
    bk.target = "VERTEX_COLORS"
    bk.use_selected_to_active = False

    me.color_attributes.active_color = ao
    bpy.ops.object.bake(type="AO", target="VERTEX_COLORS")

    # pointiness through an emission material on every slot, then restore
    em = bpy.data.materials.new("_bake_pointiness")
    em.use_nodes = True
    nt = em.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = 0.5
    mr.inputs["From Max"].default_value = 0.5 + edge_span
    mr.clamp = True
    emi = nt.nodes.new("ShaderNodeEmission")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(geo.outputs["Pointiness"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], emi.inputs["Color"])
    nt.links.new(emi.outputs["Emission"], out.inputs["Surface"])
    saved = [s.material for s in ob.material_slots]
    for s in ob.material_slots:
        s.material = em
    me.color_attributes.active_color = ed
    bpy.ops.object.bake(type="EMIT", target="VERTEX_COLORS")
    for s, m in zip(ob.material_slots, saved):
        s.material = m
    bpy.data.materials.remove(em)
    # glTF keeps one colour set reliably (the active one; "export all" swaps
    # in a white COLOR_0 and drops it), so the two masks are also packed into
    # "ao_edges" (R = ao, G = edges, B = 0, A = 1), exported as COLOR_0
    n = len(me.vertices)
    a_ = [0.0] * (4 * n)
    e_ = [0.0] * (4 * n)
    ao.data.foreach_get("color", a_)
    ed.data.foreach_get("color", e_)
    packed = [0.0] * (4 * n)
    packed[0::4] = a_[0::4]
    packed[1::4] = e_[0::4]
    packed[3::4] = [1.0] * n
    old = me.color_attributes.get("ao_edges")
    if old:
        me.color_attributes.remove(old)
    pk = me.color_attributes.new("ao_edges", "FLOAT_COLOR", "POINT")
    pk.data.foreach_set("color", packed)
    me.color_attributes.active_color = pk
    try:
        me.color_attributes.render_color_index = me.color_attributes.find("ao_edges")
    except Exception:
        pass
    return mask_stats(ob)


def mask_stats(ob):
    me = ob.data
    out = {}
    for nm in ("ao", "edges"):
        a = me.color_attributes[nm]
        vals = [d.color[0] for d in a.data]
        vals.sort()
        n = len(vals)
        out[nm] = {"min": round(vals[0], 3), "median": round(vals[n // 2], 3),
                   "max": round(vals[-1], 3),
                   "share_dark": round(sum(1 for v in vals if v < 0.5) / n, 3),
                   "share_lit": round(sum(1 for v in vals if v > 0.5) / n, 3)}
    return out


def triangles(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


def dims(ob):
    xs = [v.co.x for v in ob.data.vertices]
    ys = [v.co.y for v in ob.data.vertices]
    zs = [v.co.z for v in ob.data.vertices]
    return {"x": (min(xs), max(xs)), "y": (min(ys), max(ys)), "z": (min(zs), max(zs))}


def dims_of(ob, pred):
    """Bounding box of vertices of faces whose material name passes pred."""
    me = ob.data
    vs = set()
    for p in me.polygons:
        if pred(me.materials[p.material_index].name if me.materials else ""):
            vs.update(p.vertices)
    co = [me.vertices[i].co for i in vs]
    return {"x": (min(c.x for c in co), max(c.x for c in co)),
            "y": (min(c.y for c in co), max(c.y for c in co)),
            "z": (min(c.z for c in co), max(c.z for c in co))}


def export(objs, stem):
    os.makedirs(GLB_DIR, exist_ok=True)
    path = os.path.join(GLB_DIR, stem + ".glb")
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(
        filepath=path, export_format="GLB", use_selection=True, export_apply=True,
        export_yup=True, export_texcoords=True, export_normals=True,
        export_materials="EXPORT", export_image_format="NONE",
        export_vertex_color="ACTIVE", export_all_vertex_colors=False,
        export_active_vertex_color_when_no_material=True,
        export_animations=False, export_skins=False, export_morph=False,
        export_cameras=False, export_lights=False)
    return path, glb_report(path)


def glb_report(path):
    with open(path, "rb") as f:
        data = f.read()
    jlen = struct.unpack_from("<I", data, 12)[0]
    j = json.loads(data[20:20 + jlen])
    tris, attrs = 0, set()
    for m in j["meshes"]:
        for p in m["primitives"]:
            attrs.update(p["attributes"].keys())
            if "indices" in p:
                tris += j["accessors"][p["indices"]]["count"] // 3
    # medians of COLOR_0's red (ao) and green (edges), read back from the file
    col = {}
    try:
        import numpy as np
        off = 20 + jlen
        blen = struct.unpack_from("<I", data, off)[0]
        binc = data[off + 8:off + 8 + blen]
        chans = [[], []]
        for m in j["meshes"]:
            for p in m["primitives"]:
                if "COLOR_0" not in p["attributes"]:
                    continue
                a = j["accessors"][p["attributes"]["COLOR_0"]]
                bv = j["bufferViews"][a["bufferView"]]
                ct = {5126: np.float32, 5123: np.uint16, 5121: np.uint8}[a["componentType"]]
                nc = {"VEC3": 3, "VEC4": 4}[a["type"]]
                arr = np.frombuffer(binc, dtype=ct, count=a["count"] * nc,
                                    offset=bv.get("byteOffset", 0) + a.get("byteOffset", 0))
                arr = arr.reshape(-1, nc).astype(float)
                if ct != np.float32:
                    arr /= np.iinfo(ct).max
                chans[0].append(arr[:, 0])
                chans[1].append(arr[:, 1])
        if chans[0]:
            col = {"COLOR_0_R_ao_median": round(float(np.median(np.concatenate(chans[0]))), 3),
                   "COLOR_0_G_edges_median": round(float(np.median(np.concatenate(chans[1]))), 3)}
    except Exception as e:  # report, never fail the build on the check
        col = {"colour_check_error": str(e)}
    return {"bytes": len(data), "triangles": tris, "attributes": sorted(attrs), **col,
            "materials": [m.get("name") for m in j.get("materials", [])],
            "images": len(j.get("images", []))}


def save_blend(stem):
    os.makedirs(BLEND_DIR, exist_ok=True)
    path = os.path.join(BLEND_DIR, stem + ".blend")
    bpy.context.preferences.filepaths.save_version = 0      # no .blend1 copies
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    return path


# --------------------------------------------------------------------------
# preview: Eevee, neutral grey ground, front three-quarter

def preview(objs, stem, size=800, azimuth=-32.0, elevation=22.0, focal=85.0,
            fill=1.08, show_masks=False):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    ee = sc.eevee
    for k, v in (("use_raytracing", True), ("use_shadows", True),
                 ("taa_render_samples", 64), ("use_gtao", True)):
        if hasattr(ee, k):
            setattr(ee, k, v)
    sc.render.resolution_x = size
    sc.render.resolution_y = size
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "None"
    world = _ensure_world()
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.20, 0.20, 0.20, 1)
    bg.inputs["Strength"].default_value = 0.35

    # bounds
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z)))
            hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
    ctr = (lo + hi) / 2
    rad = (hi - lo).length / 2

    gm = material("_preview_ground", (0.36, 0.36, 0.36), 0.85)
    bpy.ops.mesh.primitive_plane_add(size=max(rad * 40, 4.0), location=(ctr.x, ctr.y, 0))
    ground = bpy.context.active_object
    ground.data.materials.append(gm)

    az, el = math.radians(azimuth), math.radians(elevation)
    d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam_d = bpy.data.cameras.new("cam")
    cam_d.lens = focal
    cam_d.sensor_width = 36
    fov = 2 * math.atan(18 / focal)
    dist = rad / math.sin(fov / 2) * fill
    cam = bpy.data.objects.new("cam", cam_d)
    sc.collection.objects.link(cam)
    cam.location = ctr + d * dist
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    cam_d.clip_start = dist * 0.05
    cam_d.clip_end = dist * 10

    def area(name, energy, direction, size_):
        ld = bpy.data.lights.new(name, "AREA")
        ld.energy = energy * (rad / 0.15) ** 2
        ld.size = size_ * rad * 4
        lo_ = bpy.data.objects.new(name, ld)
        sc.collection.objects.link(lo_)
        dv = Vector(direction).normalized()
        lo_.location = ctr + dv * rad * 6
        lo_.rotation_euler = (-dv).to_track_quat("-Z", "Y").to_euler()
    area("key", 38, (-0.8, -1.0, 1.2), 0.6)
    area("fill", 9, (1.2, -0.6, 0.5), 1.0)
    area("rim", 22, (0.4, 1.2, 0.9), 0.6)

    os.makedirs(PREVIEW_DIR, exist_ok=True)
    path = os.path.join(PREVIEW_DIR, stem + ".png")
    sc.render.filepath = path
    sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)
    return path


def report(stem, info):
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    p = os.path.join(PREVIEW_DIR, stem + ".json")
    with open(p, "w") as f:
        json.dump(info, f, indent=1, default=str)
    print("PROP_REPORT " + json.dumps(info, default=str))


def finish_prop(stem, name, ao_distance, edge_span=0.08, ref=None, render=True,
                preview_kw=None, uv_margin=0.004):
    """Join, UV, bake, check, save, export, render. ref = {axis: metres}."""
    ob = finish_parts(name)
    uv_unwrap(ob, uv_margin)
    overl = uv_overlaps(ob)
    masks = bake_masks(ob, ao_distance, edge_span)
    d = dims(ob)
    size = {k: round(v[1] - v[0], 4) for k, v in d.items()}
    blend = save_blend(stem)
    glb, g = export([ob], stem)
    info = {"prop": stem, "triangles_blender": triangles(ob), "glb": glb, "glb_report": g,
            "blend": blend, "uv_overlap_faces": overl, "masks": masks,
            "size_m": size, "bounds": {k: [round(v[0], 4), round(v[1], 4)] for k, v in d.items()},
            "materials": [m.name if m else None for m in ob.data.materials],
            "colour_attributes": [a.name for a in ob.data.color_attributes]}
    if ref:
        info["vs_reference"] = {k: {"model_m": size[k], "ref_m": r,
                                    "diff_pct": round(100 * (size[k] - r) / r, 2)}
                                for k, r in ref.items()}
    if render:
        info["preview"] = preview([ob], stem, **(preview_kw or {}))
    report(stem, info)
    return ob, info
