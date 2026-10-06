"""The venetian blind for the shop window: pale aluminium 25 mm slats on ladder strings under a
steel head rail, a bottom rail, lift cords through the slats, two pull cords with an acorn on
the right and a tilt wand on the left. Width, drop and the slats' tilt are arguments. Set 2 (the
furniture) of Mickey's front-office hero props.

    blender.exe -b --factory-startup -P tools/art-recipes/mickeys-props/blind.py -- \
        [--width 1.2] [--drop 1.5] [--tilt 35] [--name blind] [--no-render]

--drop is from the head rail's top to the bottom rail's underside (the blind let down that far);
--tilt is the slats' angle in degrees, 0 open flat, about 80 shut, the room side turned down.

SIZE (researched 6 October 2026): 25 mm slats of 0.18 or 0.21 mm aluminium; ladder string
21.5 x 28 mm (the slats' pitch and the ladder's width); head rails of 24 x 25, 24 x 26 or 19 x 27 mm;
bottom rail 10 x 20 mm; a 6 mm hexagonal tilt wand (Cottai, 25 mm venetian blind components,
https://www.cottai.com.tw/en/products-detail/25mm-venetian-Components/); headrail "24mm high x
27mm deep" or "24mm height x 25mm depth" (Veneta Blinds specifications,
https://venetablinds.com.au/pages/venetian-blinds-specifications). Modelled: slats 25 mm at
21.5 mm pitch, 0.21 mm thick with a 1.8 mm crown; head rail 24 x 25 mm; bottom rail 10 x 20 mm.
Origin at the back face's bottom centre (the head rail's back, y=0, at the blind's lowest point);
front toward -Y.
"""
# ---------------------------------------------------------------------------------------------
# SET 2 KIT (the same block in every set-2 furniture recipe, so each script stands alone).
# Mid-poly method (production/research/shop-window-interiors/MICKEYS-OTHER-DIRECTION-2026-10-04.md
# section 4): parts bevelled with Harden Normals, then a Weighted Normal pass, no high-to-low
# bake; one non-overlapping UV map; ambient occlusion and Cycles' Pointiness baked into the
# colour attributes "ao" and "edges"; at most three plain PBR materials; metres, origin at the
# base's centre on z=0 (wall pieces: the back face's bottom centre), front toward -Y.
# ---------------------------------------------------------------------------------------------
import json
import math
import os
import sys
import time

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

GLB_DIR = r"F:\LedgerTools\game-inputs\production\assets\mickeys-props"
BLEND_DIR = r"F:\LedgerTools\mickeys-props\blend"
PREVIEW_DIR = r"F:\LedgerTools\mickeys-props\previews"


def parse_args(defaults):
    """--key value pairs after '--', typed by the defaults; --no-render skips the preview."""
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = dict(defaults)
    out.setdefault("no_render", False)
    out.setdefault("out_dir", "")          # a test run can write somewhere else
    i = 0
    while i < len(argv):
        a = argv[i]
        if not a.startswith("--"):
            i += 1
            continue
        key = a[2:].replace("-", "_")
        if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            val, i = argv[i + 1], i + 2
        else:
            val, i = "1", i + 1
        cur = out.get(key)
        if isinstance(cur, bool):
            out[key] = val.lower() not in ("0", "false", "no")
        elif isinstance(cur, float):
            out[key] = float(val)
        elif isinstance(cur, int):
            out[key] = int(val)
        else:
            out[key] = val
    return out


def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.scale_length = 1.0
    return sc


# ---- materials --------------------------------------------------------------------------------
def _sock(sockets, ident):
    return [x for x in sockets if x.identifier == ident][0]


def material(name, base, rough, metal=0.0, dirt=0.35, edge=None, edge_amount=0.0, edge_rough=None):
    """A plain Principled material: base colour (linear RGB), roughness, metallic. The preview
    adds wear that costs nothing, from the baked masks broken up by a procedural noise: grime
    where 'ao' is dark, the 'edge' colour in patches along the 'edges' mask. export_glb strips
    that back to the plain constants; the game's master material does its own wear from the
    same masks."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (base[0], base[1], base[2], 1.0)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    m["plain"] = json.dumps({"base": list(base), "rough": rough, "metal": metal})
    m.diffuse_color = (base[0], base[1], base[2], 1.0)
    m.roughness = rough
    m.metallic = metal
    L = nt.links.new
    ao = nt.nodes.new("ShaderNodeAttribute"); ao.attribute_name = "ao"
    ed = nt.nodes.new("ShaderNodeAttribute"); ed.attribute_name = "edges"
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 22.0
    nz.inputs["Detail"].default_value = 6.0
    L(tc.outputs["Object"], nz.inputs["Vector"])
    # grime: (1 - ao) * dirt, varied by the noise
    inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
    L(ao.outputs["Fac"], inv.inputs[1])
    nvar = nt.nodes.new("ShaderNodeMapRange")
    nvar.inputs["From Min"].default_value = 0.3; nvar.inputs["From Max"].default_value = 0.7
    nvar.inputs["To Min"].default_value = 0.5; nvar.inputs["To Max"].default_value = 1.0
    L(nz.outputs["Fac"], nvar.inputs["Value"])
    dm = nt.nodes.new("ShaderNodeMath"); dm.operation = "MULTIPLY"
    L(inv.outputs[0], dm.inputs[0]); L(nvar.outputs["Result"], dm.inputs[1])
    dm2 = nt.nodes.new("ShaderNodeMath"); dm2.operation = "MULTIPLY"; dm2.inputs[1].default_value = dirt
    L(dm.outputs[0], dm2.inputs[0])
    mix_d = nt.nodes.new("ShaderNodeMix"); mix_d.data_type = "RGBA"
    L(dm2.outputs[0], _sock(mix_d.inputs, "Factor_Float"))
    _sock(mix_d.inputs, "A_Color").default_value = (base[0], base[1], base[2], 1.0)
    _sock(mix_d.inputs, "B_Color").default_value = (base[0] * 0.40 + 0.010, base[1] * 0.37 + 0.008, base[2] * 0.33 + 0.005, 1.0)
    last = _sock(mix_d.outputs, "Result_Color")
    if edge is not None and edge_amount > 0:
        # chips: the edges mask where the noise is high, so wear comes in patches, not outlines
        chip = nt.nodes.new("ShaderNodeMapRange")
        chip.inputs["From Min"].default_value = 0.48; chip.inputs["From Max"].default_value = 0.62
        L(nz.outputs["Fac"], chip.inputs["Value"])
        em = nt.nodes.new("ShaderNodeMath"); em.operation = "MULTIPLY"
        L(ed.outputs["Fac"], em.inputs[0]); L(chip.outputs["Result"], em.inputs[1])
        em2 = nt.nodes.new("ShaderNodeMath"); em2.operation = "MULTIPLY"; em2.inputs[1].default_value = edge_amount
        em2.use_clamp = True
        L(em.outputs[0], em2.inputs[0])
        mix_e = nt.nodes.new("ShaderNodeMix"); mix_e.data_type = "RGBA"
        L(em2.outputs[0], _sock(mix_e.inputs, "Factor_Float"))
        L(last, _sock(mix_e.inputs, "A_Color"))
        _sock(mix_e.inputs, "B_Color").default_value = (edge[0], edge[1], edge[2], 1.0)
        last = _sock(mix_e.outputs, "Result_Color")
        if edge_rough is not None:
            mr = nt.nodes.new("ShaderNodeMix"); mr.data_type = "FLOAT"
            L(em2.outputs[0], _sock(mr.inputs, "Factor_Float"))
            _sock(mr.inputs, "A_Float").default_value = rough
            _sock(mr.inputs, "B_Float").default_value = edge_rough
            L(_sock(mr.outputs, "Result_Float"), p.inputs["Roughness"])
    L(last, p.inputs["Base Color"])
    return m


def _plain(m, on):
    """on=True: unlink the preview wear and set the plain constants (for export)."""
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    v = json.loads(m["plain"])
    if on:
        m["wear_links"] = json.dumps([[l.from_node.name, l.from_socket.identifier, l.to_socket.identifier]
                                      for l in nt.links if l.to_node == p and l.to_socket.name in ("Base Color", "Roughness")])
        for l in [l for l in nt.links if l.to_node == p and l.to_socket.name in ("Base Color", "Roughness")]:
            nt.links.remove(l)
        p.inputs["Base Color"].default_value = (v["base"][0], v["base"][1], v["base"][2], 1.0)
        p.inputs["Roughness"].default_value = v["rough"]
        p.inputs["Metallic"].default_value = v["metal"]
    else:
        for fn, fs, ts in json.loads(m.get("wear_links", "[]")):
            node = nt.nodes[fn]
            out = [s for s in node.outputs if s.identifier == fs][0]
            inp = [s for s in p.inputs if s.identifier == ts][0]
            nt.links.new(out, inp)


# ---- geometry ---------------------------------------------------------------------------------
def bm_box(bm, x0, x1, y0, y1, z0, z1):
    vs = [bm.verts.new(c) for c in ((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                    (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1))]
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        bm.faces.new([vs[i] for i in f])
    return vs


def bm_prism(bm, poly, axis, a0, a1):
    """Extrude a closed 2D outline (counter-clockwise seen from +axis) from a0 to a1 along
    'x', 'y' or 'z'. For 'x' the outline is (y, z); for 'y' it is (z, x); for 'z' (x, y)."""
    def p3(u, v, a):
        if axis == "x":
            return (a, u, v)
        if axis == "y":
            return (v, a, u)
        return (u, v, a)
    lo = [bm.verts.new(p3(u, v, a0)) for u, v in poly]
    hi = [bm.verts.new(p3(u, v, a1)) for u, v in poly]
    n = len(poly)
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((lo[i], lo[j], hi[j], hi[i]))
    return lo, hi


def bm_cyl(bm, c, r, h, n=16, axis="z", r_top=None, caps=True):
    """A cylinder (or frustum) from c along +axis for length h."""
    r_top = r if r_top is None else r_top
    ax = Vector({"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[axis]) if isinstance(axis, str) else Vector(axis).normalized()
    t = ax.orthogonal().normalized()
    b = ax.cross(t).normalized()
    c = Vector(c)
    ring0, ring1 = [], []
    for k in range(n):
        a = 2 * math.pi * k / n
        d = t * math.cos(a) + b * math.sin(a)
        ring0.append(bm.verts.new(c + d * r))
        ring1.append(bm.verts.new(c + ax * h + d * r_top))
    for k in range(n):
        j = (k + 1) % n
        bm.faces.new((ring0[k], ring0[j], ring1[j], ring1[k]))
    if caps:
        bm.faces.new(list(reversed(ring0)))
        bm.faces.new(ring1)
    return ring0, ring1


def bm_tube(bm, pts, r, n=8, caps=True, closed=False):
    """A round tube swept along a polyline (parallel-transported rings)."""
    pts = [Vector(p) for p in pts]
    tans = []
    for i in range(len(pts)):
        if closed:
            a, b = pts[i - 1], pts[(i + 1) % len(pts)]
        else:
            a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        tans.append((b - a).normalized())
    nrm = tans[0].orthogonal().normalized()
    rings = []
    for i, p in enumerate(pts):
        if i > 0:
            nrm = (nrm - tans[i] * nrm.dot(tans[i])).normalized()
        bin_ = tans[i].cross(nrm).normalized()
        rings.append([bm.verts.new(p + (nrm * math.cos(2 * math.pi * k / n) + bin_ * math.sin(2 * math.pi * k / n)) * r)
                      for k in range(n)])
    segs = len(rings) if closed else len(rings) - 1
    for i in range(segs):
        r0, r1 = rings[i], rings[(i + 1) % len(rings)]
        for k in range(n):
            j = (k + 1) % n
            bm.faces.new((r0[k], r0[j], r1[j], r1[k]))
    if caps and not closed:
        bm.faces.new(list(reversed(rings[0])))
        bm.faces.new(rings[-1])
    return rings


def bm_grid_box(bm, x0, x1, y0, y1, z0, z1, nx, ny, nz=1):
    """A box cut into a grid (for cushions that are then shaped)."""
    geom = bmesh.ops.create_cube(bm, size=1.0)
    vs = geom["verts"]
    for v in vs:
        v.co = Vector((x0 if v.co.x < 0 else x1, y0 if v.co.y < 0 else y1, z0 if v.co.z < 0 else z1))
    for k in range(1, nx):
        x = x0 + (x1 - x0) * k / nx
        bmesh.ops.bisect_plane(bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces), plane_co=(x, 0, 0), plane_no=(1, 0, 0))
    for k in range(1, ny):
        y = y0 + (y1 - y0) * k / ny
        bmesh.ops.bisect_plane(bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces), plane_co=(0, y, 0), plane_no=(0, 1, 0))
    for k in range(1, nz):
        z = z0 + (z1 - z0) * k / nz
        bmesh.ops.bisect_plane(bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces), plane_co=(0, 0, z), plane_no=(0, 0, 1))


def transform(bm, verts, mat):
    bmesh.ops.transform(bm, matrix=mat, verts=verts)


PARTS = []


def part(name, build, mat, bevel=0.0, segs=2, angle=30.0, smooth=True, weighted=True, profile=0.5, sharp=None):
    """Make one part: build(bm) fills a bmesh; then bevel (Harden Normals) and Weighted Normal,
    applied. The parts are joined into the prop at the end."""
    bm = bmesh.new()
    build(bm)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if sharp is not None:            # thin sheet: keep its two faces' shading apart at the folds
        for e in bm.edges:
            if e.is_manifold and e.calc_face_angle(0.0) > math.radians(sharp):
                e.smooth = False
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    me.materials.append(mat)
    if smooth:
        me.shade_smooth()
    else:
        me.shade_flat()
    if bevel > 0:
        m = ob.modifiers.new("bevel", "BEVEL")
        m.width = bevel
        m.segments = segs
        m.limit_method = "ANGLE"
        m.angle_limit = math.radians(angle)
        m.harden_normals = True
        m.use_clamp_overlap = True
        m.miter_outer = "MITER_ARC"
        m.profile = profile
    if weighted:
        w = ob.modifiers.new("weighted", "WEIGHTED_NORMAL")
        w.mode = "FACE_AREA"
        w.weight = 50
        w.keep_sharp = True
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob], selected_editable_objects=[ob]):
        for m in list(ob.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)
    PARTS.append(ob)
    return ob


def join(name, parts=None, origin=(0.0, 0.0, 0.0)):
    parts = list(parts if parts is not None else PARTS)
    main = parts[0]
    with bpy.context.temp_override(active_object=main, object=main, selected_objects=parts, selected_editable_objects=parts):
        bpy.ops.object.join()
    main.name = name
    main.data.name = name
    # origin: move the mesh so 'origin' (world) becomes the object's origin
    main.data.transform(Matrix.Translation(-Vector(origin)))
    main.location = Vector(origin)
    bpy.context.view_layer.update()
    for p in parts:
        if p in PARTS:
            PARTS.remove(p)
    return main


# ---- UVs ---------------------------------------------------------------------------------------
def _select_polys(objs, polys):
    """In edit mode: select exactly these polygons (per object), nothing else."""
    for o in objs:
        bm = bmesh.from_edit_mesh(o.data)
        bm.faces.ensure_lookup_table()
        for v in bm.verts:
            v.select_set(False)
        for e in bm.edges:
            e.select_set(False)
        for f in bm.faces:
            f.select_set(False)
        for i in polys.get(o.name, ()):
            bm.faces[i].select_set(True)
        bm.select_flush_mode()
        bmesh.update_edit_mesh(o.data)


def unwrap(objs, margin=0.004):
    """Smart UV Project over every object together, packed into one 0..1 map. Faces whose
    islands still overlap (a fold the projection could not flatten) are cut into their own
    islands and the whole map packed again, until nothing overlaps."""
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
        if not o.data.uv_layers:
            o.data.uv_layers.new(name="UVMap")
    bpy.context.view_layer.objects.active = objs[0]

    def pack():
        bpy.ops.uv.average_islands_scale()      # one texel density, whatever was re-cut
        try:
            bpy.ops.uv.pack_islands(rotate=True, margin_method="FRACTION", margin=margin, shape_method="CONVEX")
        except TypeError:
            bpy.ops.uv.pack_islands(rotate=True, margin=margin)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=margin, area_weight=0.0,
                             correct_aspect=True, scale_to_bounds=False)
    pack()
    bpy.ops.object.mode_set(mode="OBJECT")
    for attempt in range(6):
        over, cov, _, bad = uv_overlap(objs, res=2048, want_polys=True)
        print("UVPASS", attempt, over, cov, {k: len(v) for k, v in bad.items()})
        if not over:
            break
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="FACE")
        _select_polys(objs, bad)
        # the culprits are slivers the bevel left twisted at cushion corners: as triangles,
        # each in its own island, they cannot fold over themselves
        bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY", ngon_method="BEAUTY")
        bpy.ops.uv.smart_project(angle_limit=math.radians(1), island_margin=margin,
                                 area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
        bpy.ops.mesh.select_all(action="SELECT")
        pack()
        bpy.ops.object.mode_set(mode="OBJECT")


def uv_overlap(objs, res=2048, want_polys=False):
    """Rasterise every UV triangle of every object at res x res; a pixel inside two triangles
    (strictly inside, so shared edges never count) is an overlap. Returns (overlap pixels,
    covered pixels, all UVs inside 0..1[, the overlapping polygons per object])."""
    owner = np.zeros((res, res), dtype=np.int64)     # 0 = empty, else global triangle id + 1
    over = 0
    inside = True
    tri_ref = []
    bad = set()
    for o in objs:
        me = o.data
        me.calc_loop_triangles()
        uv = me.uv_layers.active.data
        n = len(me.loop_triangles)
        loops = np.zeros(n * 3, dtype=np.int64)
        me.loop_triangles.foreach_get("loops", loops)
        polys = np.zeros(n, dtype=np.int64)
        me.loop_triangles.foreach_get("polygon_index", polys)
        uvs = np.zeros(len(uv) * 2)
        uv.foreach_get("uv", uvs)
        uvs = uvs.reshape(-1, 2)
        if uvs.min() < -1e-6 or uvs.max() > 1 + 1e-6:
            inside = False
        tri = uvs[loops].reshape(-1, 3, 2) * res
        for ti, t in enumerate(tri):
            tri_ref.append((o.name, int(polys[ti])))
            gid = len(tri_ref)
            (x0, y0), (x1, y1), (x2, y2) = t
            area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
            if abs(area) < 1e-12:
                continue
            ix0, ix1 = int(max(math.floor(min(x0, x1, x2)), 0)), int(min(math.ceil(max(x0, x1, x2)), res - 1))
            iy0, iy1 = int(max(math.floor(min(y0, y1, y2)), 0)), int(min(math.ceil(max(y0, y1, y2)), res - 1))
            if ix1 < ix0 or iy1 < iy0:
                continue
            px, py = np.meshgrid(np.arange(ix0, ix1 + 1) + 0.5, np.arange(iy0, iy1 + 1) + 0.5)
            w0 = ((x1 - px) * (y2 - py) - (x2 - px) * (y1 - py)) / area
            w1 = ((x2 - px) * (y0 - py) - (x0 - px) * (y2 - py)) / area
            w2 = 1.0 - w0 - w1
            eps = 1e-5
            m = (w0 > eps) & (w1 > eps) & (w2 > eps)
            if not m.any():
                continue
            sub = owner[iy0:iy1 + 1, ix0:ix1 + 1]
            hit = sub[m]
            k = int((hit > 0).sum())
            if k:
                over += k
                if want_polys:
                    bad.add(tri_ref[gid - 1])
                    for g in np.unique(hit[hit > 0]):
                        bad.add(tri_ref[int(g) - 1])
            sub[m] = gid
    covered = int((owner > 0).sum())
    if want_polys:
        per = {}
        for name, pi in bad:
            per.setdefault(name, set()).add(pi)
        return over, covered, inside, per
    return over, covered, inside


# ---- baking ------------------------------------------------------------------------------------
POINTINESS_RANGE = (0.54, 0.58)  # Cycles Pointiness: flat 0.5, a 24-sided cylinder 0.538, a 2-segment bevel 0.557, its corners 0.589 (calibrated 6 Oct 2026)


def bake_masks(objs, ao_distance=0.25, samples=96, occluders=()):
    """'ao': Cycles ambient occlusion; 'edges': Cycles' Pointiness through a ramp (convex edges
    1, flat and hollow 0). Both baked into point-domain float colour attributes."""
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    sc.world.light_settings.distance = ao_distance
    sc.render.bake.target = "VERTEX_COLORS"
    sc.render.bake.margin = 0
    for o in occluders:
        o.hide_render = False
    for o in objs:
        me = o.data
        for nm in ("ao", "edges"):
            if nm in me.color_attributes:
                me.color_attributes.remove(me.color_attributes[nm])
            me.color_attributes.new(nm, "FLOAT_COLOR", "POINT")
    # ambient occlusion
    for o in objs:
        me = o.data
        me.color_attributes.active_color = me.color_attributes["ao"]
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.bake(type="AO")
    # edges: an emission material from Pointiness
    em = bpy.data.materials.new("_pointiness")
    em.use_nodes = True
    nt = em.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = POINTINESS_RANGE[0]
    mr.inputs["From Max"].default_value = POINTINESS_RANGE[1]
    mr.clamp = True
    emit = nt.nodes.new("ShaderNodeEmission")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(geo.outputs["Pointiness"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], emit.inputs["Color"])
    nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
    for o in objs:
        me = o.data
        keep = [s.material for s in o.material_slots]
        for s in o.material_slots:
            s.material = em
        me.color_attributes.active_color = me.color_attributes["edges"]
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.bake(type="EMIT")
        for s, m in zip(o.material_slots, keep):
            s.material = m
    bpy.data.materials.remove(em)
    # glTF carries one colour set (its exporter writes white into COLOR_0 when asked for more),
    # and Unreal reads one: so the glb gets "ao_edges", red = ao, green = edges, blue 0, alpha 1
    # (the same packing as set 1's desk props, so one master material reads both sets)
    for o in objs:
        me = o.data
        n = len(me.vertices)
        ao = np.zeros(n * 4); me.color_attributes["ao"].data.foreach_get("color", ao)
        ed = np.zeros(n * 4); me.color_attributes["edges"].data.foreach_get("color", ed)
        packed = np.zeros((n, 4))
        packed[:, 0] = ao.reshape(-1, 4)[:, 0]
        packed[:, 1] = ed.reshape(-1, 4)[:, 0]
        packed[:, 3] = 1.0
        if "ao_edges" in me.color_attributes:
            me.color_attributes.remove(me.color_attributes["ao_edges"])
        pk = me.color_attributes.new("ao_edges", "FLOAT_COLOR", "POINT")
        pk.data.foreach_set("color", packed.ravel())
        me.color_attributes.active_color = pk
        me.color_attributes.render_color_index = list(me.color_attributes).index(pk)


def mask_stats(o, name):
    a = o.data.color_attributes[name].data
    v = np.zeros(len(a) * 4)
    a.foreach_get("color", v)
    v = v.reshape(-1, 4)[:, 0]
    return {"min": round(float(v.min()), 3), "mean": round(float(v.mean()), 3), "max": round(float(v.max()), 3)}


# ---- export ------------------------------------------------------------------------------------
def export_glb(objs, path):
    mats = {s.material for o in objs for s in o.material_slots if s.material}
    for m in mats:
        _plain(m, True)
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True,
                              export_yup=True, export_texcoords=True, export_normals=True,
                              export_tangents=False, export_materials="EXPORT", export_vertex_color="ACTIVE",
                              export_all_vertex_colors=False, export_attributes=False, export_image_format="NONE")
    for m in mats:
        _plain(m, False)
    return os.path.getsize(path)


# ---- preview ----------------------------------------------------------------------------------
def _eevee_id():
    items = [i.identifier for i in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    for e in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        if e in items:
            return e
    return items[0]


def preview(objs, path, wall=False, res=(800, 800), az=-35.0, el=18.0, lens=55.0, fill=1.0, target=None, engine=None):
    """Front three-quarter view on a neutral grey ground (and a wall behind wall pieces), Eevee."""
    sc = bpy.context.scene
    coll = bpy.data.collections.get("preview") or bpy.data.collections.new("preview")
    if coll.name not in sc.collection.children:
        sc.collection.children.link(coll)
    grey = bpy.data.materials.get("_ground") or material("_ground", (0.18, 0.18, 0.18), 0.85, dirt=0.0)
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    ctr = (lo + hi) / 2 if target is None else Vector(target)
    if not bpy.data.objects.get("_ground"):
        bm = bmesh.new()
        gz = -0.18 if wall else 0.0       # wall pieces shown hung a little above the floor
        bm_box(bm, -20, 20, -20, 20, gz - 0.01, gz)
        me = bpy.data.meshes.new("_ground"); bm.to_mesh(me); bm.free()
        g = bpy.data.objects.new("_ground", me); g.data.materials.append(grey); coll.objects.link(g)
        if wall:
            bm = bmesh.new()
            bm_box(bm, -20, 20, max(hi.y, 0.0), max(hi.y, 0.0) + 0.01, -0.5, 20)
            me = bpy.data.meshes.new("_wall"); bm.to_mesh(me); bm.free()
            w = bpy.data.objects.new("_wall", me)
            w.data.materials.append(bpy.data.materials.get("_wallmat") or material("_wallmat", (0.42, 0.42, 0.41), 0.9, dirt=0.0))
            coll.objects.link(w)
    # camera fitted to the bounding sphere
    rad = (hi - lo).length / 2
    cam_d = bpy.data.cameras.new("_cam"); cam_d.lens = lens
    cam = bpy.data.objects.new("_cam", cam_d); coll.objects.link(cam)
    fov = 2 * math.atan(cam_d.sensor_width / 2 / lens)
    dist = rad / math.sin(fov / 2) * fill
    a, e = math.radians(az), math.radians(el)
    d = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    cam.location = ctr + d * dist
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    # light: a soft key from front left above, a fill, a grey sky
    if not bpy.data.objects.get("_key"):
        k = bpy.data.lights.new("_key", "AREA"); k.energy = 260.0 * max(rad, 0.4) ** 2; k.size = 3.0 * max(rad, 0.4)
        ko = bpy.data.objects.new("_key", k); coll.objects.link(ko)
        ko.location = ctr + Vector((-1.6, -2.2, 2.6)) * max(rad, 0.4) * 1.6
        ko.rotation_euler = (ctr - ko.location).to_track_quat("-Z", "Y").to_euler()
        f = bpy.data.lights.new("_fill", "AREA"); f.energy = 60.0 * max(rad, 0.4) ** 2; f.size = 4.0 * max(rad, 0.4)
        fo = bpy.data.objects.new("_fill", f); coll.objects.link(fo)
        fo.location = ctr + Vector((2.4, -1.4, 1.0)) * max(rad, 0.4) * 1.6
        fo.rotation_euler = (ctr - fo.location).to_track_quat("-Z", "Y").to_euler()
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.32, 0.33, 0.35, 1.0)
    bg.inputs[1].default_value = 0.35
    sc.render.engine = engine or _eevee_id()
    try:
        sc.eevee.taa_render_samples = 64
    except AttributeError:
        pass
    sc.view_settings.view_transform = "AgX"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    return path


def shading_check(objs, path, az=-35.0, el=18.0):
    """A Workbench render with a shiny matcap-like studio light: faceting and normal faults show."""
    sc = bpy.context.scene
    eng = sc.render.engine
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"
    sh.color_type = "SINGLE"
    sh.single_color = (0.6, 0.6, 0.6)
    sh.show_specular_highlight = True
    preview(objs, path, az=az, el=el, engine="BLENDER_WORKBENCH")
    sc.render.engine = eng


def report(name, objs, extra=None):
    """Measured size, triangles, attributes, UV overlap: printed and returned."""
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    tris = 0
    for o in objs:
        o.data.calc_loop_triangles()
        tris += len(o.data.loop_triangles)
    over, covered, inside = uv_overlap(objs)
    out = {"prop": name, "size_m": {"x": round(hi[0] - lo[0], 4), "y": round(hi[1] - lo[1], 4), "z": round(hi[2] - lo[2], 4)},
           "min": [round(v, 4) for v in lo], "max": [round(v, 4) for v in hi], "triangles": tris,
           "materials": sorted({s.material.name for o in objs for s in o.material_slots if s.material}),
           "uv_maps": sorted({l.name for o in objs for l in o.data.uv_layers}),
           "uv_overlap_px_2048": over, "uv_covered_px_2048": covered, "uv_inside_0_1": inside,
           "attributes": {o.name: sorted(a.name for a in o.data.color_attributes) for o in objs},
           "ao": {o.name: mask_stats(o, "ao") for o in objs if "ao" in o.data.color_attributes},
           "edges": {o.name: mask_stats(o, "edges") for o in objs if "edges" in o.data.color_attributes}}
    if extra:
        out.update(extra)
    print("REPORT " + json.dumps(out))
    return out


def finish(name, objs, args, wall=False, ao_distance=0.25, occluders=(), extra=None, view=None):
    """Unwrap, bake, preview, export the glb, save the .blend, write the report."""
    t0 = time.time()
    unwrap(objs)
    bake_masks(objs, ao_distance=ao_distance, occluders=occluders)
    for o in occluders:
        bpy.data.objects.remove(o)
    out_dir = args.get("out_dir") or ""
    glb = os.path.join(out_dir or GLB_DIR, name + ".glb")
    blend = os.path.join(out_dir or BLEND_DIR, name + ".blend")
    prev = os.path.join(out_dir or PREVIEW_DIR, name + ".png")
    size = export_glb(objs, glb)
    rep = report(name, objs, extra)
    rep["glb_bytes"] = size
    rep["glb"] = glb
    if not args.get("no_render"):
        v = view or {}
        preview(objs, prev, wall=wall, **v)
        shading_check(objs, os.path.join(out_dir or PREVIEW_DIR, "checks", name + "_shading.png"), **{k: v[k] for k in ("az", "el") if k in v})
        rep["preview"] = prev
    os.makedirs(os.path.dirname(blend), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
    rep["blend"] = blend
    rep["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(os.path.dirname(blend), name + ".report.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print("REPORT " + json.dumps(rep))
    return rep
# ---- END OF SET 2 KIT ------------------------------------------------------------------------

A = parse_args({"width": 1.2, "drop": 1.5, "tilt": 35.0, "name": "blind"})
clean_scene()

slat_mat = material("blind_pale_aluminium", (0.66, 0.655, 0.62), 0.33, metal=0.55, dirt=0.4,
                    edge=(0.45, 0.43, 0.39), edge_amount=0.25)
cord_mat = material("blind_nylon_cord", (0.56, 0.54, 0.48), 0.85, dirt=0.4)
plastic = material("blind_plastic", (0.50, 0.46, 0.37), 0.40, dirt=0.3)

W, DROP = A["width"], A["drop"]
TILT = math.radians(A["tilt"])
HR_H, HR_D = 0.024, 0.025          # head rail
BR_H, BR_D = 0.010, 0.020          # bottom rail
SLAT_W, SLAT_T, CROWN = 0.025, 0.00021, 0.0018
PITCH = 0.0215
LADDER_W = 0.028
YC = -HR_D / 2                     # the ladders' centre plane
CAP = 0.007                        # end caps' thickness
FRONT_CORD_Y = -0.032              # pull cords and wand hang in front of the slats

# the slats: as many as the drop holds at the ladder's pitch
z_top = DROP - HR_H - 0.013
z_bot = BR_H + 0.011
n_slats = int((z_top - z_bot) / PITCH) + 1


def slat_section():
    """The slat's crowned section in (y, z) about its centre, 7 points over, 7 under."""
    top, bot = [], []
    for k in range(7):
        u = -1 + 2 * k / 6
        y = u * SLAT_W / 2
        z = CROWN * (1 - u * u) - CROWN / 2
        top.append((y, z + SLAT_T / 2))
        bot.append((y, z - SLAT_T / 2))
    return top + list(reversed(bot))


def slats(bm):
    sec = slat_section()
    ct, st = math.cos(TILT), math.sin(TILT)
    x0, x1 = -W / 2 + CAP + 0.002, W / 2 - CAP - 0.002
    for i in range(n_slats):
        zc = z_top - i * PITCH
        # tilt about the slat's long axis: the room side (-y) turns down
        poly = [(YC + y * ct - z * st, zc + y * st + z * ct) for (y, z) in sec]
        bm_prism(bm, poly, "x", x0, x1)


part("slats", slats, slat_mat, bevel=0.0, smooth=True, weighted=True, sharp=60.0)


# THE RAILS: a pressed-steel head rail with plastic end caps; the bottom rail the same
def rails(bm):
    bm_box(bm, -W / 2 + CAP, W / 2 - CAP, -HR_D, 0.0, DROP - HR_H, DROP)
    bm_box(bm, -W / 2 + CAP, W / 2 - CAP, YC - BR_D / 2, YC + BR_D / 2, 0.0, BR_H)


part("rails", rails, slat_mat, bevel=0.0018, segs=2)


def caps(bm):
    for s in (-1, 1):
        a, b = sorted((s * (W / 2 - CAP), s * W / 2))
        bm_box(bm, a, b, -HR_D - 0.001, 0.0, DROP - HR_H - 0.001, DROP)
        bm_box(bm, a, b, YC - BR_D / 2 - 0.001, YC + BR_D / 2 + 0.001, 0.0, BR_H + 0.001)


part("end_caps", caps, plastic, bevel=0.0015, segs=2)


# THE LADDERS and LIFT CORDS: front and back strings past the slats' edges, a cord through them
def ladder_xs():
    n = 2 if W < 0.9 else (3 if W < 1.8 else 4)
    inset = 0.10 if W > 0.6 else W * 0.18
    return [-W / 2 + inset + (W - 2 * inset) * k / (n - 1) for k in range(n)]


def strings(bm):
    half = SLAT_W / 2 * math.cos(TILT) + 0.0006
    for xl in ladder_xs():
        for s in (-1, 1):
            # each string steps out round every slat edge: a straight tape is close enough
            y = YC + s * half
            bm_box(bm, xl - 0.0008, xl + 0.0008, y - 0.0003, y + 0.0003, BR_H, DROP - HR_H)
        bm_cyl(bm, (xl + 0.004, YC, BR_H), 0.0007, DROP - HR_H - BR_H, n=6)


part("ladders", strings, cord_mat, bevel=0.0, smooth=True, weighted=False)


# THE PULL CORDS on the right, to an acorn; the TILT WAND on the left
CORD_X = W / 2 - 0.055
CORD_END = max(0.25, DROP * 0.42)


def pull_cords(bm):
    for dx in (-0.002, 0.002):
        bm_tube(bm, [(CORD_X + dx, YC, DROP - HR_H), (CORD_X + dx, FRONT_CORD_Y, DROP - HR_H - 0.02),
                     (CORD_X + dx * 0.5, FRONT_CORD_Y, CORD_END + 0.03)], 0.0008, n=6)


part("pull_cords", pull_cords, cord_mat, bevel=0.0, smooth=True, weighted=False)


def acorn(bm):
    rings = []
    prof = [(0.0, 0.0), (0.004, 0.003), (0.0065, 0.010), (0.0068, 0.016), (0.0055, 0.024), (0.003, 0.030), (0.0012, 0.033)]
    n = 16
    for r, z in prof:
        rings.append([bm.verts.new((CORD_X + r * math.cos(2 * math.pi * k / n),
                                    FRONT_CORD_Y + r * math.sin(2 * math.pi * k / n), CORD_END + z - 0.003))
                      for k in range(n)])
    for a, b in zip(rings[:-1], rings[1:]):
        for k in range(n):
            j = (k + 1) % n
            bm.faces.new((a[k], a[j], b[j], b[k]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])


part("acorn", acorn, plastic, bevel=0.0, smooth=True, weighted=True)

WAND_X = -W / 2 + 0.055
WAND_LEN = min(0.75, DROP * 0.55)


def wand(bm):
    bm_cyl(bm, (WAND_X, FRONT_CORD_Y, DROP - HR_H - 0.022 - WAND_LEN), 0.003, WAND_LEN, n=6)
    bm_cyl(bm, (WAND_X, FRONT_CORD_Y, DROP - HR_H - 0.022), 0.0035, 0.012, n=10)          # its hook's sleeve
    bm_box(bm, WAND_X - 0.002, WAND_X + 0.002, FRONT_CORD_Y, -HR_D + 0.002, DROP - HR_H - 0.012, DROP - HR_H - 0.006)


part("tilt_wand", wand, plastic, bevel=0.0006, segs=1, angle=40)

blind = join(A["name"])
finish(A["name"], [blind], A, wall=True, ao_distance=0.04,
       extra={"target_m": {"width": W, "drop": DROP, "slat_width": SLAT_W, "pitch": PITCH,
                           "head_rail_h": HR_H, "head_rail_d": HR_D},
              "slats": n_slats, "tilt_deg": A["tilt"]},
       view={"az": -30.0, "el": 10.0})
