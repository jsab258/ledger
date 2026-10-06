"""The shop door in its frame: a half-glazed painted leaf (a fielded panel under a lock rail, the
glass above it left open for Unreal), a brass kick plate, letter plate, lever handle on a
backplate and a Yale-type rim cylinder, three butt hinges on the inside; the frame with a
terrazzo threshold, jambs with stops, a door head, a fanlight, the transom at 2.40 continued from
the window, a toplight with glazing bars and the head under the fascia. Part of the shopfront kit
for the east parade (production/art/shopfront-kit/README.md).

    blender.exe -b --factory-startup -P tools/art-recipes/shopfront-kit/shop_door.py -- \
        [--width 0.90] [--height 2.04] [--glazed-from 1.00] [--hinge left|right] \
        [--metal brass|chrome] [--upper glazed|panel] [--paint r,g,b] [--name shop_door] \
        [--no-render] [--out-dir <folder>]

SIZE (production/specs/vignette-scene.json, C8_door_shop; the research,
production/research/shopfronts/FRONTAGE-2026-10-06.md): the leaf 0.90 x 2.04, glazed from 1.00
above the pavement, 50 mm thick; stiles 110, top rail 120, bottom rail 230 (Ellis, Modern
Practical Joinery, 1902: bottom rails 9 in), lock rail 200 under the glass. The frame adds a
50 mm jamb and a 3 mm gap each side (1.006 overall) and runs up to the fascia at 2.85.
THE RESEARCH DIFFERS on two points, modelled as the spec says: the guides glaze a shop door from
about the stallriser's height ("two-thirds glazed", Brighton & Hove SPD02; the bottom panel the
stallriser's height, Coventry 2014), not from 1.0; and 2.04 is a metric leaf height,
where Ellis gives period entrance doors 7 ft (2.13 m) or more.

TWO OBJECTS in one glb: "shop_door" (the frame; origin on the bay's datum at the middle of the
back face on the pavement, front toward -Y) and its child "shop_door_leaf", whose origin is on
its hinge axis, so it opens inward by turning about Z (positive angles for a left hinge, seen
from the street; negative for a right hinge). --hinge names the side seen from the street.
"""
# ---------------------------------------------------------------------------------------------
# SET 2 KIT, copied from tools/art-recipes/mickeys-props/counter.py on 6 October 2026 so each
# script stands alone; the shopfront kit's few changes to it are marked SHOPFRONT.
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

GLB_DIR = r"F:\LedgerTools\game-inputs\production\assets\shopfront-kit"
BLEND_DIR = r"F:\LedgerTools\shopfront-kit\blend"
PREVIEW_DIR = r"F:\LedgerTools\shopfront-kit\previews"


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
    bpy.context.preferences.filepaths.save_version = 0     # SHOPFRONT: no .blend1 copy beside the .blend
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


def part(name, build, mat, bevel=0.0, segs=2, angle=30.0, smooth=True, weighted=True, profile=0.5, sharp=None,
         inset=None, cuts=0.3):
    """Make one part: build(bm) fills a bmesh; support loops for the vertex masks; then bevel
    (Harden Normals) and Weighted Normal, applied. The parts are joined into the prop at the end.

    Vertex masks only know what their vertices know: a flat face whose only vertices sit on its
    bevels reads as all edge. So each face bounded by a sharp edge gets a ring inset 2.5 bevel
    widths in (flat vertices just past the bevel, so 'edges' falls to 0 there), and long parts are
    cut every 'cuts' metres (ambient occlusion sampled along them)."""
    bm = bmesh.new()
    build(bm)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if inset is None:
        inset = 2.5 * bevel
    if inset > 0:
        lim = math.radians(angle)
        faces = [f for f in bm.faces if len(f.edges) >= 3
                 and min(e.calc_length() for e in f.edges) > 3.0 * inset
                 and any(e.is_manifold and e.calc_face_angle(0.0) > lim for e in f.edges)]
        if faces:
            bmesh.ops.inset_individual(bm, faces=faces, thickness=inset, depth=0.0, use_even_offset=True)
    if cuts > 0 and bm.verts:
        for axis in range(3):
            lo = min(v.co[axis] for v in bm.verts)
            hi = max(v.co[axis] for v in bm.verts)
            n = int((hi - lo) / cuts)
            for k in range(1, n + 1):
                co, no = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
                co[axis], no[axis] = lo + (hi - lo) * k / (n + 1), 1.0
                bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-7, edges=bm.edges[:])     # no zero-length edges or empty faces
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
        if np.nanmin(uvs) < -1e-6 or np.nanmax(uvs) > 1 + 1e-6:
            inside = False
        tri = uvs[loops].reshape(-1, 3, 2) * res
        for ti, t in enumerate(tri):
            tri_ref.append((o.name, int(polys[ti])))
            gid = len(tri_ref)
            if not np.isfinite(t).all():          # a face the projection could not place: re-cut it
                over += 1
                inside = False
                bad.add(tri_ref[gid - 1])
                continue
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


def _components(me):
    """Connected-part index of every vertex (union-find over the edges)."""
    n = len(me.vertices)
    ev = np.zeros(len(me.edges) * 2, dtype=np.int64)
    me.edges.foreach_get("vertices", ev)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for a, b in ev.reshape(-1, 2):
        ra, rb = find(int(a)), find(int(b))
        if ra != rb:
            parent[ra] = rb
    roots = np.array([find(i) for i in range(n)])
    return np.unique(roots, return_inverse=True)[1]


def bake_masks(objs, ao_distance=0.25, samples=96, occluders=()):
    """'ao': Cycles ambient occlusion; 'edges': Cycles' Pointiness through a ramp (convex edges
    1, flat and hollow 0). Both baked into point-domain float colour attributes."""
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.render.threads_mode = "FIXED"     # four threads: a build machine may be busy on this PC
    sc.render.threads = 4
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
        # Cycles welds any vertices closer than 0.35 mm before it measures Pointiness (its
        # duplicate test is a squared distance under FLT_EPSILON). Where two of a prop's parts
        # touch face to face, their vertices weld, the facing normals cancel and a flat face reads
        # as all edge. So for this bake each connected part stands apart from the others.
        co = np.zeros(len(me.vertices) * 3)
        me.vertices.foreach_get("co", co)
        k = _components(me).astype(float)
        sp = 0.5173
        off = np.c_[(k % 16) * sp, ((k // 16) % 16) * sp, (k // 256) * sp]
        me.vertices.foreach_set("co", (co.reshape(-1, 3) + off).ravel())
        me.update()
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.bake(type="EMIT")
        me.vertices.foreach_set("co", co)
        me.update()
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


def preview(objs, path, wall=False, res=(800, 800), az=-35.0, el=18.0, lens=55.0, fill=1.0, target=None, engine=None,
            ground_z=None):
    """Front three-quarter view on a neutral grey ground (and a wall behind wall pieces), Eevee."""
    # SHOPFRONT: the graphics card belongs to Unreal and the build machine. While either runs
    # there is no Workbench check, and the preview is rendered by Cycles on the processor.
    cpu = gpu_busy()
    if cpu and engine == "BLENDER_WORKBENCH":
        return None
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
        if ground_z is not None:          # SHOPFRONT: kit pieces stand on the pavement datum
            gz = ground_z
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
    sc.render.engine = engine or ("CYCLES" if cpu else _eevee_id())
    if sc.render.engine == "CYCLES":     # SHOPFRONT: on the processor only, never the card
        sc.cycles.device = "CPU"
        sc.cycles.samples = 64
        sc.cycles.use_denoising = True
        sc.cycles.denoising_use_gpu = False
        sc.render.threads_mode = "FIXED"
        sc.render.threads = 4
    print("PREVIEW ENGINE", sc.render.engine, path)
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


def shading_check(objs, path, az=-35.0, el=18.0, wall=False, **kw):
    """A Workbench render with a shiny matcap-like studio light: faceting and normal faults show."""
    sc = bpy.context.scene
    eng = sc.render.engine
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"
    sh.color_type = "SINGLE"
    sh.single_color = (0.6, 0.6, 0.6)
    sh.show_specular_highlight = True
    out = preview(objs, path, az=az, el=el, engine="BLENDER_WORKBENCH", wall=wall, **kw)   # SHOPFRONT: **kw
    sc.render.engine = eng
    return out


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
        # SHOPFRONT: each render checks the graphics card first: while it is busy the preview is
        # Cycles on the processor and the Workbench check is skipped (None)
        got = preview(objs, prev, wall=wall, **v)
        rep["preview_engine"] = bpy.context.scene.render.engine if got else None
        chk = shading_check(objs, os.path.join(out_dir or PREVIEW_DIR, "checks", name + "_shading.png"), wall=wall,
                            **{k: v[k] for k in v if k not in ("res",)})
        rep["preview"] = got
        rep["shading_check"] = chk
    os.makedirs(os.path.dirname(blend), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
    rep["blend"] = blend
    rep["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(os.path.dirname(blend), name + ".report.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print("REPORT " + json.dumps(rep))
    return rep
# ---- END OF SET 2 KIT ------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# SHOPFRONT KIT (the same block in every shopfront-kit recipe, so each script stands alone).
# Research: production/research/shopfronts/FRONTAGE-2026-10-06.md. The bay's datum, shared by
# every piece: x along the street, left to right seen from the street; y = 0 the wall face, which
# is the back of every piece, the street toward -Y; z = 0 the pavement. Each piece's origin is on
# that datum at the middle of its width, so it drops into a bay with no height offset (the window
# frame starts 0.60 up, on the stallriser's sill; the console and fascia start at 2.85).
# ---------------------------------------------------------------------------------------------
import subprocess

DEFAULT_PAINT = "0.11,0.23,0.16"    # sRGB 0..1: a dark green ("dark green", Brighton & Hove SPD02)
GLASS_Y = -0.030           # the glass plane: 0.12 behind the stallriser's sill nose (spec glazing_recess_m)
SILL_Z = 0.60              # the stallriser's sill top (spec stallriser_height_m)
TRANSOM = (2.40, 2.48)     # spec transom_height_m 2.40 and transom_thickness_m 0.08
HEAD = (2.79, 2.85)        # the frame head; its top is the fascia's bottom (spec fascia_bottom_m 2.85)
FRAME_D = 0.085            # depth of the window frame's jambs and head
DOOR_D = 0.10              # depth of the door frames
JAMB = 0.05                # width of every jamb
LEAF_GAP = 0.003           # the gap round a door leaf in its frame


def gpu_busy():
    """The graphics card belongs to Unreal and the build machine: True when UnrealEditor or
    Runner.Worker is running, or when the check itself fails. True means: do not render."""
    try:
        out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True,
                             timeout=60).stdout.lower()
    except Exception as e:  # noqa: BLE001
        print("GPU CHECK FAILED, treated as busy, no render:", e)
        return True
    hits = [n for n in ("unrealeditor", "runner.worker") if n in out]
    if hits:
        print("GPU BUSY (%s): nothing rendered on the graphics card" % ", ".join(hits))
    return bool(hits)


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lin(r, g, b):
    return tuple(srgb_to_linear(x) for x in (r, g, b))


def parse_rgb(s):
    """'r,g,b' in sRGB, 0..1 (or 0..255 when any value is over 1), to linear RGB."""
    v = [float(x) for x in str(s).replace(" ", "").split(",")][:3]
    if max(v) > 1.0:
        v = [x / 255.0 for x in v]
    return lin(*[min(max(x, 0.0), 1.0) for x in v])


def paint_material(rgb_lin):
    """Painted softwood: oil gloss gone dull; in the preview its edges and sills are worn to a pale
    undercoat and grey timber, with grime in the hollows (the glb keeps the plain constants)."""
    return material("painted_timber", rgb_lin, 0.50, dirt=0.55, edge=lin(0.52, 0.49, 0.43),
                    edge_amount=0.8, edge_rough=0.85)


def metal_material(kind="brass"):
    if kind == "chrome":
        return material("chrome", (0.62, 0.62, 0.62), 0.20, metal=1.0, dirt=0.55)
    # aged brass: darker than new (linear base 0.91, 0.78, 0.42), bright where hands wear it
    return material("brass", (0.55, 0.40, 0.17), 0.38, metal=1.0, dirt=0.7, edge=(0.85, 0.70, 0.38),
                    edge_amount=0.5, edge_rough=0.22)


# ---- profiles and sweeps ----------------------------------------------------------------------
def quarter_round(r, n=4):
    """A closed (d, h) outline: a quarter-round bead in the angle at (0, 0)."""
    return [(0.0, 0.0)] + [(r * math.cos(math.pi / 2 * k / n), r * math.sin(math.pi / 2 * k / n)) for k in range(n + 1)]


def sweep_path(bm, path, profile, z0=0.0):
    """A moulding run along a plan path [(x, y), ...] at the height z0. 'profile' is a closed
    outline of (o, z): o the offset out from the path (o = 0 on the block's face; out is to the
    right of travel, so run the path from the wall, down the block's left side seen from the
    street, across its front and back up its right side), z above z0. Mitred corners; the two
    ends, at the wall, capped flat."""
    P = [Vector((x, y, 0.0)) for x, y in path]
    nrm = []
    for i in range(len(P) - 1):
        t = (P[i + 1] - P[i]).normalized()
        nrm.append(Vector((t.y, -t.x, 0.0)))
    rings = []
    for i in range(len(P)):
        if i == 0:
            m = nrm[0]
        elif i == len(P) - 1:
            m = nrm[-1]
        else:
            a, b = nrm[i - 1], nrm[i]
            m = (a + b) / (1.0 + a.dot(b))
        rings.append([bm.verts.new((P[i].x + m.x * o, P[i].y + m.y * o, z0 + z)) for o, z in profile])
    n = len(profile)
    for i in range(len(rings) - 1):
        r0, r1 = rings[i], rings[i + 1]
        for k in range(n):
            j = (k + 1) % n
            bm.faces.new((r0[k], r0[j], r1[j], r1[k]))
    bm.faces.new(rings[0])
    bm.faces.new(list(reversed(rings[-1])))
    return rings


def sweep_rect(bm, x0, x1, z0, z1, yf, profile, out=-1.0):
    """A moulding round a rectangular opening drawn on the face y = yf. 'profile' is a closed
    outline of (d, h): d in from the opening's edge, h out from the face (toward the street when
    out = -1; out = +1 for a back face). Mitred at the four corners."""
    corners = ((x0, z0, 1, 1), (x1, z0, -1, 1), (x1, z1, -1, -1), (x0, z1, 1, -1))
    rings = [[bm.verts.new((cx + sx * d, yf + out * h, cz + sz * d)) for d, h in profile]
             for cx, cz, sx, sz in corners]
    n = len(profile)
    for i in range(4):
        r0, r1 = rings[i], rings[(i + 1) % 4]
        for k in range(n):
            j = (k + 1) % n
            bm.faces.new((r0[k], r0[j], r1[j], r1[k]))


def raised_field(bm, x0, x1, z0, z1, yf, inset, rise, out=-1.0):
    """The raised field of a fielded panel on the face y = yf: margins 'inset' wide rising 'rise'
    to a flat field (a solid; its base lies on the panel board)."""
    a = [bm.verts.new(c) for c in ((x0, yf, z0), (x1, yf, z0), (x1, yf, z1), (x0, yf, z1))]
    yt = yf + out * rise
    b = [bm.verts.new(c) for c in ((x0 + inset, yt, z0 + inset), (x1 - inset, yt, z0 + inset),
                                   (x1 - inset, yt, z1 - inset), (x0 + inset, yt, z1 - inset))]
    bm.faces.new(a)
    bm.faces.new(list(reversed(b)))
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((a[i], a[j], b[j], b[i]))


def bm_lathe(bm, c, axis, profile, n=16):
    """A turned part (knob, rose, cylinder) from c along 'axis': 'profile' is (r, t) pairs, r the
    radius at t along the axis (r > 0 at both ends; both ends capped)."""
    ax = Vector(axis).normalized()
    t0 = ax.orthogonal().normalized()
    b0 = ax.cross(t0).normalized()
    c = Vector(c)
    rings = [[bm.verts.new(c + ax * t + (t0 * math.cos(2 * math.pi * k / n) + b0 * math.sin(2 * math.pi * k / n)) * r)
              for k in range(n)] for r, t in profile]
    for i in range(len(rings) - 1):
        for k in range(n):
            j = (k + 1) % n
            bm.faces.new((rings[i][k], rings[i][j], rings[i + 1][j], rings[i + 1][k]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])


def fielded_panel(bm, x0, x1, z0, z1, yb_front, yb_back, sides=("front", "back"), field_inset=0.032,
                  rise=0.010, bead=0.012, what=("fields", "beads")):
    """A panel in an opening x0..x1, z0..z1 of a framed piece: on each face named, a raised field
    and a quarter-round bead (the 'sticking') round it. The 18 mm board between yb_front and
    yb_back is not modelled: the fields and beads cover both its faces and the frame's members
    enclose its edges. 'what' builds the fields, the beads or both (the beads go in a part of
    their own with a lighter bevel)."""
    for side in sides:
        yf, out = (yb_front, -1.0) if side == "front" else (yb_back, 1.0)
        if "fields" in what:
            raised_field(bm, x0 + bead, x1 - bead, z0 + bead, z1 - bead, yf, field_inset, rise, out)
        if "beads" in what:
            sweep_rect(bm, x0, x1, z0, z1, yf, quarter_round(bead, 3), out)


def transom_profile(z0, z1, depth=0.10):
    """The transom's section (y, z): a flat bed at the back for the toplight glass (the glass plane
    at y = -0.03), a weathered top falling to the street (Ellis 1902: top edges bevelled to shed
    rain), a rounded nose and a drip groove under it."""
    return [(0.0, z0), (-0.070, z0), (-0.070, z0 + 0.006), (-0.077, z0 + 0.006), (-0.077, z0),
            (-depth + 0.004, z0), (-depth, z0 + 0.004), (-depth, z1 - 0.034), (-depth + 0.002, z1 - 0.029),
            (-depth + 0.007, z1 - 0.026), (-0.046, z1), (0.0, z1)]


def mullion_section(w=0.055, d=0.078):
    """A mullion's section (x, y): square at the back, a rounded (oval) nose toward the street;
    rounded or oval, "projecting about 40-70mm from the glass" (Cornwall Shopfront Design Guide)."""
    hw = w / 2
    pts = [(-hw, 0.0), (-hw, -(d - hw * 0.9))]
    for k in range(1, 8):
        a = math.pi * k / 8
        pts.append((-hw * math.cos(a), -(d - hw * 0.9) - hw * 0.9 * math.sin(a)))
    pts += [(hw, -(d - hw * 0.9)), (hw, 0.0)]
    return pts


def glazing_bars(bm, xs, z0, z1, w=0.025, d=0.055):
    """Upright glazing bars for toplights: w wide, the mullion's rounded section, from the frame's
    back (y = 0) out to -d; the glass stands in them at y = -0.03."""
    for x in xs:
        bm_prism(bm, [(px + x, py) for px, py in mullion_section(w, d)], "z", z0, z1)


def occluder(x0, x1, y0, y1, z0, z1, name="_occluder"):
    """A box that shades the ambient-occlusion bake (the wall, the pavement, a neighbour) and is
    removed before export."""
    bm = bmesh.new()
    bm_box(bm, x0, x1, y0, y1, z0, z1)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def street_occluders(x0, x1, z_top=3.6, extra=()):
    """The wall behind (y >= 0) and the pavement under (z <= 0) a piece, plus any boxes given."""
    obs = [occluder(x0 - 1.0, x1 + 1.0, 0.0, 0.3, -0.3, z_top, "_wall"),
           occluder(x0 - 1.0, x1 + 1.0, -2.0, 0.3, -0.3, 0.0, "_pavement")]
    for k, b in enumerate(extra):
        obs.append(occluder(*b, name="_near%d" % k))
    return obs


def bbox(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    return lo, hi


def ray_hit(obj, origin, direction):
    """Where a ray first meets an object's mesh (world space), or None: for measuring openings."""
    from mathutils.bvhtree import BVHTree
    mw = obj.matrix_world
    tree = BVHTree.FromPolygons([mw @ v.co for v in obj.data.vertices], [tuple(p.vertices) for p in obj.data.polygons])
    hit = tree.ray_cast(Vector(origin), Vector(direction).normalized())
    return hit[0]


def measured(target, got):
    """{target, measured, error %} for the report."""
    return {"target": round(target, 4), "measured": round(got, 4),
            "error_pct": round(100.0 * (got - target) / target, 2) if target else None}


def door_frame(W, H, threshold_mat, paint, upper="glazed", tl_bars=None, step_depth=0.13):
    """The frame of a door whose leaf is W x H: a weathered threshold, two jambs with stops, a door
    head, a fanlight up to the transom at 2.40 (continuing the window's), above it a toplight
    with glazing bars ('glazed') or a fielded panel ('panel'), and the head under the fascia.
    Returns the frame's layout: the leaf's bottom, the glass openings."""
    TH = 0.025                                   # the threshold's top under the leaf
    lz0 = TH + LEAF_GAP                          # the leaf's bottom
    lz1 = lz0 + H
    xi = W / 2 + LEAF_GAP                        # the jambs' inner faces
    xo = xi + JAMB
    dh0, dh1 = lz1 + LEAF_GAP, lz1 + LEAF_GAP + 0.06     # the door head
    lay = {"leaf_z": [round(lz0, 4), round(lz1, 4)], "frame_inner_x": [round(-xi, 4), round(xi, 4)],
           "frame_outer_x": [round(-xo, 4), round(xo, 4)], "glass_y": None, "openings": []}

    def threshold(bm):
        # weathered: 25 mm at the leaf falling to 12 mm at a rounded nose, out on the pavement
        prof = [(0.0, 0.0), (-step_depth, 0.0), (-step_depth, 0.010), (-step_depth + 0.004, 0.015),
                (-step_depth + 0.010, 0.017), (-0.075, TH - 0.002), (-0.070, TH), (0.0, TH)]
        bm_prism(bm, prof, "x", -xo, xo)
    part("threshold", threshold, threshold_mat, bevel=0.002, segs=2)

    def frame(bm):
        for s in (-1, 1):
            a, b = sorted((s * xi, s * xo))
            bm_box(bm, a, b, -DOOR_D, 0.0, TH, HEAD[1])                       # jamb
            c, d = sorted((s * xi, s * (xi - 0.015)))
            bm_box(bm, c, d, -DOOR_D, -0.075, TH, dh0)                        # its stop, before the leaf
        bm_box(bm, -xi, xi, -DOOR_D, 0.0, dh0, dh1)                          # door head
        bm_box(bm, -xi + 0.015, xi - 0.015, -DOOR_D, -0.075, dh0 - 0.015, dh0)   # head stop
        bm_prism(bm, transom_profile(*TRANSOM, depth=DOOR_D), "x", -xi, xi)  # transom
        bm_box(bm, -xi, xi, -DOOR_D, 0.0, HEAD[0], HEAD[1])                  # head
    part("frame", frame, paint, bevel=0.003, segs=2)
    if TRANSOM[0] - dh1 > 0.05:
        lay["openings"].append({"what": "fanlight", "x": [round(-xi, 4), round(xi, 4)],
                                "z": [round(dh1, 4), TRANSOM[0]], "glass_y": GLASS_Y})
        # the fanlight's glass bead on the door head
        part("fanlight_bead", lambda bm: bm_prism(bm, [(GLASS_Y - 0.003, dh1), (GLASS_Y - 0.018, dh1),
                                                       (GLASS_Y - 0.003, dh1 + 0.014)], "x", -xi, xi),
             paint, bevel=0.0, smooth=True)
    if upper == "glazed":
        n = tl_bars if tl_bars is not None else max(0, round(2 * xi / 0.32) - 1)
        xs = [-xi + 2 * xi * k / (n + 1) for k in range(1, n + 1)]
        if xs:
            part("toplight_bars", lambda bm: glazing_bars(bm, xs, TRANSOM[1], HEAD[0]), paint, bevel=0.002, segs=2)
        lay["openings"].append({"what": "toplight", "x": [round(-xi, 4), round(xi, 4)], "z": [TRANSOM[1], HEAD[0]],
                                "glass_y": GLASS_Y, "bars_x": [round(x, 4) for x in xs]})
    else:
        part("upper_panel", lambda bm: fielded_panel(bm, -xi, xi, TRANSOM[1], HEAD[0], -0.068, -0.050, what=("fields",)),
             paint, bevel=0.002, segs=2)
        part("upper_panel_beads", lambda bm: fielded_panel(bm, -xi, xi, TRANSOM[1], HEAD[0], -0.068, -0.050, what=("beads",)),
             paint, bevel=0.0015, segs=1)
    lay["glass_y"] = GLASS_Y
    return lay, lz0, lz1, xi, xo
# ---- END OF SHOPFRONT KIT --------------------------------------------------------------------


A = parse_args({"width": 0.90, "height": 2.04, "glazed_from": 1.00, "hinge": "left", "metal": "brass",
                "upper": "glazed", "paint": DEFAULT_PAINT, "name": "shop_door"})
clean_scene()
paint = paint_material(parse_rgb(A["paint"]))
metal = metal_material(A["metal"])
terrazzo = material("terrazzo", lin(0.60, 0.57, 0.52), 0.42, dirt=0.65, edge=lin(0.72, 0.70, 0.66),
                    edge_amount=0.3, edge_rough=0.6)

W, H, GF = A["width"], A["height"], A["glazed_from"]
lay, lz0, lz1, xi, xo = door_frame(W, H, terrazzo, paint, upper=A["upper"])
frame = join(A["name"])
hw = W / 2
hs = -1.0 if A["hinge"] == "left" else 1.0       # the hinge side's sign along x
ls = -hs                                          # the lock side
YF, YB = -0.072, -0.022                          # the leaf's faces (50 mm, behind the stops)
ST, TR, BR, LR = 0.11, 0.12, 0.23, 0.20           # stiles, top, bottom and lock rails
GY = (YF + YB) / 2                               # the leaf's glass plane
MEAS = {}


def leaf(bm):
    for s in (-1, 1):
        a, b = sorted((s * hw, s * (hw - ST)))
        bm_box(bm, a, b, YF, YB, lz0, lz1)                                   # stiles
    bm_box(bm, -(hw - ST), hw - ST, YF, YB, lz0, lz0 + BR)                   # bottom rail
    bm_box(bm, -(hw - ST), hw - ST, YF, YB, GF - LR, GF)                     # lock rail
    bm_box(bm, -(hw - ST), hw - ST, YF, YB, lz1 - TR, lz1)                   # top rail
    fielded_panel(bm, -(hw - ST), hw - ST, lz0 + BR, GF - LR, GY - 0.009, GY + 0.009, what=("fields",))


def leaf_beads(bm):
    fielded_panel(bm, -(hw - ST), hw - ST, lz0 + BR, GF - LR, GY - 0.009, GY + 0.009, what=("beads",))
    bead = [(0.0, 0.0), (0.014, 0.0), (0.012, 0.004), (0.006, 0.010), (0.0, 0.012)]
    sweep_rect(bm, -(hw - ST), hw - ST, GF, lz1 - TR, GY - 0.003, bead, -1.0)   # glazing beads
    sweep_rect(bm, -(hw - ST), hw - ST, GF, lz1 - TR, GY + 0.003, bead, 1.0)


leaf_wood = part("leaf", leaf, paint, bevel=0.003, segs=2)
part("leaf_beads", leaf_beads, paint, bevel=0.0015, segs=1)
MEAS["leaf"] = bbox([leaf_wood])
# where the glass starts: a ray down the glazed opening, just behind the leaf's front face
MEAS["glazed_from"] = ray_hit(leaf_wood, (0.0, YF + 0.004, lz1 - TR - 0.05), (0, 0, -1)).z
xl = ls * (hw - ST / 2)                          # the lock stile's centre line
zh = GF + 0.05                                   # the lever's height


def fittings(bm):
    # kick plate, 1.5 mm brass over the bottom rail and the stiles' feet
    bm_box(bm, -(hw - 0.015), hw - 0.015, YF - 0.0015, YF, lz0 + 0.012, lz0 + 0.212)
    # letter plate on the lock rail: a plate, its flap, the flap's knuckle
    zc = GF - LR / 2
    bm_box(bm, -0.150, 0.150, YF - 0.004, YF, zc - 0.0375, zc + 0.0375)
    bm_box(bm, -0.130, 0.130, YF - 0.008, YF - 0.004, zc - 0.024, zc + 0.020)
    bm_cyl(bm, (-0.130, YF - 0.008, zc + 0.022), 0.0045, 0.26, n=10, axis="x")
    # lever handle on a backplate, outside and in
    for face, out in ((YF, -1.0), (YB, 1.0)):
        bm_box(bm, xl - 0.0225, xl + 0.0225, *sorted((face, face + out * 0.006)), zh - 0.13, zh + 0.10)
        bm_lathe(bm, (xl, face + out * 0.006, zh), (0, out, 0), [(0.019, 0.0), (0.019, 0.004), (0.012, 0.009), (0.009, 0.011)], n=16)
        bm_tube(bm, [(xl, face + out * 0.016, zh), (xl, face + out * 0.050, zh),
                     (xl + hs * 0.030, face + out * 0.058, zh), (xl + hs * 0.115, face + out * 0.058, zh - 0.004)],
                0.0085, n=10)
        bm_lathe(bm, (xl, face + out * 0.006, zh - 0.085), (0, out, 0), [(0.007, 0.0), (0.007, 0.003), (0.005, 0.004)], n=10)
    # Yale-type rim cylinder outside, its night latch's case inside
    zc2 = GF + 0.30
    bm_lathe(bm, (xl, YF, zc2), (0, -1, 0), [(0.019, 0.0), (0.019, 0.004), (0.016, 0.009), (0.012, 0.012),
                                            (0.0095, 0.012), (0.0095, 0.0135), (0.006, 0.014)], n=20)
    a, b = sorted((ls * hw, ls * (hw - 0.092)))
    bm_box(bm, a, b, YB, YB + 0.030, zc2 - 0.037, zc2 + 0.037)
    bm_lathe(bm, (xl + hs * 0.01, YB + 0.030, zc2), (0, 1, 0), [(0.013, 0.0), (0.013, 0.012), (0.010, 0.016)], n=14)
    # three butt hinges on the inside at the hinge edge (the door opens in)
    for z in (lz0 + 0.20, (lz0 + lz1) / 2, lz1 - 0.20):
        bm_cyl(bm, (hs * (hw + 0.0015), YB + 0.006, z - 0.05), 0.0065, 0.10, n=12)
        a, b = sorted((hs * hw, hs * (hw - 0.032)))
        bm_box(bm, a, b, YB, YB + 0.0025, z - 0.05, z + 0.05)


part("leaf_fittings", fittings, metal, bevel=0.0008, segs=1, angle=40)
leaf_ob = join(A["name"] + "_leaf", origin=(hs * (hw + 0.0015), YB + 0.006, lz0))
leaf_ob.parent = frame
leaf_ob.matrix_parent_inverse = frame.matrix_world.inverted()
objs = [frame, leaf_ob]
lo, hi = bbox(objs)
lay["openings"].insert(0, {"what": "door glass", "x": [round(-(hw - ST), 4), round(hw - ST, 4)],
                           "z": [round(GF, 4), round(lz1 - TR, 4)], "glass_y": round(GY, 4), "in": "shop_door_leaf"})
occ = street_occluders(-xo, xo, extra=[(-xo - 0.6, xo + 0.6, -0.12, 0.0, HEAD[1], HEAD[1] + 0.55)])
extra = {"target_m": {"leaf_width": W, "leaf_height": H, "glazed_from": GF},
         "measured": {"leaf_width": measured(W, MEAS["leaf"][1][0] - MEAS["leaf"][0][0]),
                      "leaf_height": measured(H, MEAS["leaf"][1][2] - MEAS["leaf"][0][2]),
                      "glazed_from": measured(GF, MEAS["glazed_from"]),
                      "overall_width": round(hi[0] - lo[0], 4), "overall_height": round(hi[2] - lo[2], 4),
                      "overall_depth": round(-lo[1], 4)},
         "layout": lay, "hinge": A["hinge"], "metal": A["metal"], "upper": A["upper"], "paint_srgb": A["paint"]}
finish(A["name"], objs, A, wall=True, ao_distance=0.15, occluders=occ, extra=extra,
       view={"az": -30.0, "el": 10.0, "fill": 1.0, "ground_z": 0.0})
