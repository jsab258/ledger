"""The clothing session's shared tools for sewing a FreeSewing pattern round a MetaHuman body in Blender.

Imported by the garment scripts beside it (sew_donkey.py and those after it):

    import sys, os; sys.path.insert(0, os.path.dirname(__file__)); import tailor

WHY, 29 September (the clothing session, CLOTHES.md item 2): every garment is
made the same way, from the research (production/research/clothing-pipeline/
pattern-jacket-2026-09-29.md, SLEEVES-2026-09-29.md): cut from a real
pattern, each piece meshed flat with the same number of points along both
sides of every seam, placed round the body, sewn by Blender's sewing springs
and draped. What is common lives here: the pattern's lines, the flat pieces,
the body and its pose, the flat pattern kept as the cloth's rest shape, the
checks (seam gaps, cloth inside the body, strain against the pattern) and the
check pictures. The helpers for the pattern's lines are sew_cap.py's and
sew_jacket.py's, the builder's, gathered here.

THE REST SHAPE (tested 29 September on Blender 4.5.13, F:/LedgerTools/tmp/
clothes/rsk_test.py): with a shape key holding the flat pattern set as the
cloth's rest shape key AND a pass-through geometry-nodes modifier before the
cloth (bug #115321's workaround), the cloth starts where it is placed and is
pulled towards the pattern's own lengths; without the modifier the key is
ignored. So a piece may be placed bent or stretched and still hang with the
pattern's lengths.
"""
import json
import math

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import delaunay_2d_cdt

BLENDER = "C:/LedgerTools/blender/4.5.13/blender-4.5.13-windows-x64/blender.exe"
ARMISH = ("upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky", "wrist", "elbow")


# ---- the pattern's lines (mm, y down, as FreeSewing draws) ---------------------

def closed(pts):
    pts = [tuple(p) for p in pts]
    return pts[:-1] if pts[0] == pts[-1] else pts


def near(poly, p):
    d = [(q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 for q in poly]
    return d.index(min(d))


def walk(poly, a, b):
    i, j, n = near(poly, a), near(poly, b), len(poly)
    out = [poly[i]]
    while i != j:
        i = (i + 1) % n
        out.append(poly[i])
    return out


def length(poly):
    return sum(math.dist(poly[k], poly[k - 1]) for k in range(1, len(poly)))


def seg(poly, a, b):
    """The outline from a to b, the shorter way round by length (by points a curve's dense sampling misleads)."""
    fwd = walk(poly, a, b)
    bwd = list(reversed(walk(poly, b, a)))
    return fwd if length(fwd) <= length(bwd) else bwd


def resample(poly, n):
    cum = [0.0]
    for k in range(1, len(poly)):
        cum.append(cum[-1] + math.dist(poly[k], poly[k - 1]))
    out = []
    for s in np.linspace(0, cum[-1], n + 1):
        k = max(1, min(len(poly) - 1, int(np.searchsorted(cum, s))))
        t = 0.0 if cum[k] == cum[k - 1] else (s - cum[k - 1]) / (cum[k] - cum[k - 1])
        a, b = poly[k - 1], poly[k]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def split_at(poly, s):
    run = 0.0
    for k in range(1, len(poly)):
        d = math.dist(poly[k], poly[k - 1])
        if run + d >= s:
            t = (s - run) / d
            a, b = poly[k - 1], poly[k]
            m = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            return poly[:k] + [m], [m] + poly[k:]
        run += d
    return poly, [poly[-1]]


def loop(segments):
    """A piece's outline from named segments (name, polyline, points): the points, and each segment's indices, ends included."""
    pts, idx = [], {}
    for name, poly, n in segments:
        r = resample(poly, n)
        start = len(pts)
        pts.extend(r[:-1])
        idx[name] = list(range(start, start + n)) + [None]
    total = len(pts)
    for name in idx:
        s = idx[name]
        s[-1] = (s[-2] + 1) % total
    return pts, idx


def _inside(poly, xy):
    poly = np.asarray(poly)
    x, y = xy[:, 0][:, None], xy[:, 1][:, None]
    x1, y1 = poly[:, 0][None], poly[:, 1][None]
    x2, y2 = np.roll(poly[:, 0], -1)[None], np.roll(poly[:, 1], -1)[None]
    cross = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)
    return cross.sum(axis=1) % 2 == 1


def _clearance2d(poly, xy):
    a = np.asarray(poly)
    b = np.roll(a, -1, axis=0)
    ab = b - a
    t = np.clip(((xy[:, None] - a[None]) * ab[None]).sum(-1) / ((ab * ab).sum(-1)[None] + 1e-12), 0, 1)
    proj = a[None] + t[..., None] * ab[None]
    return np.sqrt(((xy[:, None] - proj) ** 2).sum(-1)).min(axis=1)


def panel(boundary, edge):
    """A flat piece filled with even triangles about `edge` mm across; the boundary's points come first, in order."""
    b = np.asarray(boundary)
    lo, hi = b.min(axis=0), b.max(axis=0)
    rows = np.arange(lo[1], hi[1] + edge, edge * math.sqrt(3) / 2)
    grid = []
    for r, y in enumerate(rows):
        xs = np.arange(lo[0] + (edge / 2 if r % 2 else 0), hi[0] + edge, edge)
        grid.extend((x, y) for x in xs)
    grid = np.asarray(grid)
    grid = grid[_inside(boundary, grid)]
    grid = grid[_clearance2d(boundary, grid) > edge * 0.55]
    verts = [Vector(p) for p in boundary] + [Vector(p) for p in grid]
    nb = len(boundary)
    edges = [(k, (k + 1) % nb) for k in range(nb)]
    out_v, _e, out_f, orig_v, _oe, _of = delaunay_2d_cdt(verts, edges, [list(range(nb))], 1, 1e-6, True)
    remap, flat = {}, [tuple(v) for v in verts]
    for k, ov in enumerate(orig_v):
        if ov:
            remap[k] = ov[0]
        else:
            remap[k] = len(flat)
            flat.append(tuple(out_v[k]))
    return flat, [[remap[k] for k in f] for f in out_f]


# ---- the body ---------------------------------------------------------------

def load_body(fbx, lod=None):
    """The body FBX into an empty scene: its armature and one level of its mesh (the finest, or `lod`), the
    others removed, its points split along texture seams joined again.

    THE FULL BODY, HEAD AND ALL (29 September, run 4): the body alone is open
    at the neck, and a point near the hole read as inside the body and was
    pushed through it to the back of the neck, a spike 39 times its length.
    With the head the surface is shut. Level 1 (12,634 points against 51,619)
    keeps the collisions quick; its surface lies within millimetres of level 0's."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=fbx)
    arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
    meshes = sorted([o for o in bpy.context.scene.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
    keep = meshes[0]
    if lod is not None:
        keep = next((o for o in meshes if o.name.endswith("_LOD%d" % lod)), meshes[0])
    for o in meshes:
        if o is not keep:
            bpy.data.objects.remove(o, do_unlink=True)
    bm = bmesh.new()
    bm.from_mesh(keep.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0001)
    bm.to_mesh(keep.data)
    bm.free()
    keep.data.update()
    return arm, keep


def joint(arm, name, posed=True):
    if posed:
        return arm.matrix_world @ arm.pose.bones[name].head
    return arm.matrix_world @ arm.data.bones[name].head_local


def arm_angle(arm, side):
    """The upper arm's angle below the horizontal, degrees, as posed now."""
    bpy.context.view_layer.update()
    sh = joint(arm, "upperarm_" + side)
    el = joint(arm, "lowerarm_" + side)
    d = (el - sh).normalized()
    return math.degrees(math.asin(max(-1.0, min(1.0, -d.z))))


def pose_arms(arm, deg):
    """Each upper arm turned about its own joint, square to itself and the vertical (abduction only, no roll),
    until the elbow is `deg` below the shoulder's horizontal. Returns the rest rotations, to key the way back."""
    rest = {}
    for side in ("l", "r"):
        pb = arm.pose.bones["upperarm_" + side]
        pb.rotation_mode = "QUATERNION"
        rest[side] = pb.rotation_quaternion.copy()
        bpy.context.view_layer.update()
        sh = arm.matrix_world @ pb.head
        el = arm.matrix_world @ arm.pose.bones["lowerarm_" + side].head
        d = (el - sh).normalized()
        now = math.degrees(math.asin(max(-1.0, min(1.0, -d.z))))
        ax = d.cross(Vector((0, 0, 1))).normalized()
        R = Matrix.Rotation(math.radians(now - deg), 4, ax)
        if (R.to_3x3() @ d).z < d.z:
            R = Matrix.Rotation(math.radians(deg - now), 4, ax)
        M = arm.matrix_world
        Ra = (M.inverted() @ R @ M).to_3x3().to_4x4()
        h = pb.head.copy()
        pb.matrix = Matrix.Translation(h) @ Ra @ Matrix.Translation(-h) @ pb.matrix
        bpy.context.view_layer.update()
    return rest


def evaluated_copy(obj, name):
    """The object as deformed now, as a plain mesh object in world space."""
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(obj.evaluated_get(dg))
    me.transform(obj.matrix_world)
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return o


def dominant_bones(obj):
    names = {g.index: g.name for g in obj.vertex_groups}
    out = []
    for v in obj.data.vertices:
        best, w = "", 0.0
        for g in v.groups:
            if g.weight > w:
                best, w = names.get(g.group, ""), g.weight
        out.append(best)
    return out


def bvh_of(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.transform(obj.matrix_world)
    t = BVHTree.FromBMesh(bm)
    bm.free()
    return t


def depth_inside(bvh, co):
    """How far a point lies inside the body (metres, 0 outside), by the nearest surface's normal."""
    hit, nrm, _f, d = bvh.find_nearest(co)
    if hit is None:
        return 0.0
    return d if (co - hit).dot(nrm) < 0.0 else 0.0


# ---- the garment mesh ------------------------------------------------------------

class Garment:
    """Pieces as flat meshes (mm), placed in 3D (m), sewn by named seams, built as one Blender object."""

    def __init__(self):
        self.verts, self.flat, self.rest, self.faces, self.piece_of = [], [], [], [], []
        self.groups = {}
        self.seams = {}

    def add(self, name, flat, faces, placed, layout=(0.0, 0.0), mirror=False, share=None, rest=None):
        """One piece: its flat points (mm), faces, and 3D places (m). `share` maps a point's index to a point
        already in the garment (a fold welded to its mirror). `rest`, if given, is the piece wrapped without
        stretching (on a cylinder, round an arm), the shape its cloth remembers: the pattern's lengths with the
        wrap's curvature (a flat rest makes a tube want to unroll; the research, SLEEVES-RECIPE-2026-09-29.md).
        Returns the piece's point -> garment index map."""
        at = {}
        grp = self.groups.setdefault(name, [])
        for k, f2 in enumerate(flat):
            if share and k in share:
                at[k] = share[k]
                continue
            at[k] = len(self.verts)
            self.verts.append(tuple(placed[k]))
            self.rest.append(tuple(rest[k]) if rest is not None else None)
            sx = -1.0 if mirror else 1.0
            self.flat.append((layout[0] + sx * f2[0] / 1000.0, layout[1] - f2[1] / 1000.0, 0.0))
            self.piece_of.append(name)
            grp.append(at[k])
        for f in faces:
            g = [at[k] for k in f]
            self.faces.append(list(reversed(g)) if mirror else g)
        return at

    def seam(self, label, ia, ib):
        assert len(ia) == len(ib), (label, len(ia), len(ib))
        self.seams.setdefault(label, []).extend((a, b) for a, b in zip(ia, ib) if a != b)

    def build(self, name="Garment"):
        pairs = list(dict.fromkeys(tuple(sorted(p)) for v in self.seams.values() for p in v))
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.verts, pairs, self.faces)
        me.validate()
        obj = bpy.data.objects.new(name, me)
        bpy.context.collection.objects.link(obj)
        for g, ids in self.groups.items():
            vg = obj.vertex_groups.new(name=g)
            vg.add(ids, 1.0, "REPLACE")
        uv = me.uv_layers.new(name="pattern")
        for poly in me.polygons:
            for li in poly.loop_indices:
                c = self.flat[me.loops[li].vertex_index]
                uv.data[li].uv = (c[0], c[1])
        # THE REST SHAPE (see the module's note): each piece wrapped without
        # stretching where given, else the flat pattern
        obj.shape_key_add(name="Basis")
        rest = obj.shape_key_add(name="rest")
        for k, c in enumerate(self.flat):
            rest.data[k].co = self.rest[k] if self.rest[k] is not None else c
        rest.value = 0.0
        self.sewing = pairs
        return obj


def weld(obj, pairs, co, max_gap=0.045):
    """The garment as one piece of cloth: each seam pair within max_gap merged at its midpoint, the sewing edges
    gone, the shape now `co` (the stitched frame). Returns how many pairs were merged."""
    if obj.data.shape_keys:
        obj.shape_key_clear()
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    for v in bm.verts:
        v.co = Vector(co[v.index])
    # a point in two seams (the armpit, where side, armhole and underarm meet)
    # joins one group: union-find over every pair, each group to its mean
    parent = list(range(len(bm.verts)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    merged = 0
    for a, b in pairs:
        if np.linalg.norm(co[a] - co[b]) <= max_gap:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
            merged += 1
    groups = {}
    for i in range(len(parent)):
        groups.setdefault(find(i), []).append(i)
    targetmap = {}
    for r, members in groups.items():
        if len(members) < 2:
            continue
        m = Vector(np.mean([co[i] for i in members], axis=0))
        for i in members:
            bm.verts[i].co = m
            if i != r:
                targetmap[bm.verts[i]] = bm.verts[r]
    bmesh.ops.delete(bm, geom=[e for e in bm.edges if not e.link_faces], context="EDGES")
    bmesh.ops.weld_verts(bm, targetmap=targetmap)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    return merged


def push_out(obj, bvh, clear=0.003):
    """Every point of the garment inside the body put back out, clear of its surface."""
    n = 0
    for v in obj.data.vertices:
        co = obj.matrix_world @ v.co
        hit, nrm, _f, _d = bvh.find_nearest(co)
        if hit is not None and (co - hit).dot(nrm) < clear:
            v.co = obj.matrix_world.inverted() @ (hit + nrm * clear)
            n += 1
    obj.data.update()
    return n


def cloth(obj, quality=12, mass=0.01, tension=40.0, compression=40.0, shear=15.0, bending=20.0, air=2.0,
          distance=0.004, self_collision=False, self_distance=0.002, sewing=False, rest_key=None, frames=100):
    """A cloth modifier with the research's settings (OpenSew-2's, SLEEVES-RECIPE-2026-09-29.md)."""
    if rest_key:
        passthrough(obj)
    cl = obj.modifiers.new("Cloth", "CLOTH")
    st, cs = cl.settings, cl.collision_settings
    st.quality = quality
    st.mass = mass
    st.air_damping = air
    st.tension_stiffness, st.compression_stiffness = tension, compression
    st.shear_stiffness, st.bending_stiffness = shear, bending
    st.use_sewing_springs = sewing
    st.sewing_force_max = 0.0            # unlimited: a capped force stops pulling once a gap passes a few mm
    st.shrink_min = 0.0
    if rest_key:
        st.rest_shape_key = obj.data.shape_keys.key_blocks[rest_key]
    cs.use_collision = True
    cs.collision_quality = 6
    cs.distance_min = distance
    cs.use_self_collision = self_collision
    cs.self_distance_min = self_distance
    cl.point_cache.frame_start = 1
    cl.point_cache.frame_end = frames
    return cl


def collider(obj, friction=60.0):
    col = obj.modifiers.new("Collision", "COLLISION")
    c = obj.collision
    c.thickness_outer = 0.002
    c.thickness_inner = 0.02
    c.cloth_friction = friction
    c.use_culling = True                 # single sided: cloth inside is pushed out along the body's normals
    c.use_normal = True
    return col


def apply_frame(obj):
    """The object's evaluated shape at the current frame made its own mesh; its modifiers removed."""
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(obj.evaluated_get(dg))
    old = obj.data
    obj.modifiers.clear()
    obj.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return obj


def passthrough(obj):
    """The pass-through geometry-nodes modifier that makes the cloth honour its rest shape key (bug #115321)."""
    gn = obj.modifiers.new("RestKeyFix", "NODES")
    tree = bpy.data.node_groups.get("RestKeyFix")
    if tree is None:
        tree = bpy.data.node_groups.new("RestKeyFix", "GeometryNodeTree")
        tree.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
        tree.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
        i_, o_ = tree.nodes.new("NodeGroupInput"), tree.nodes.new("NodeGroupOutput")
        tree.links.new(i_.outputs[0], o_.inputs[0])
    gn.node_group = tree
    return gn


# ---- the checks --------------------------------------------------------------

def coords(obj, evaluated=True):
    if evaluated:
        ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    else:
        ev = obj.data
    a = np.empty(len(ev.vertices) * 3)
    ev.vertices.foreach_get("co", a)
    a = a.reshape(-1, 3)
    M = np.array(obj.matrix_world)
    return a @ M[:3, :3].T + M[:3, 3]


def seam_gaps(co, seams):
    """The widest gap along each seam, mm."""
    return {k: round(float(np.max(np.linalg.norm(co[[a for a, _ in v]] - co[[b for _, b in v]], axis=1))) * 1000, 1)
            for k, v in seams.items() if v}


def strain(obj, co, groups, flat):
    """Each piece's edge lengths against the pattern's: the 5th, 50th and 95th percentile of placed / flat."""
    flat = np.asarray(flat)
    out = {}
    edges = np.array([ed.vertices[:] for ed in obj.data.edges])
    lf = np.linalg.norm(flat[edges[:, 0]] - flat[edges[:, 1]], axis=1)
    lp = np.linalg.norm(co[edges[:, 0]] - co[edges[:, 1]], axis=1)
    piece = np.full(len(flat), -1)
    for n, (g, ids) in enumerate(groups.items()):
        piece[ids] = n
    for n, g in enumerate(groups):
        # the piece's own edges only: a seam's sewing edge joins two pieces
        m = (lf > 1e-6) & (piece[edges[:, 0]] == n) & (piece[edges[:, 1]] == n)
        if m.any():
            r = lp[m] / lf[m]
            out[g] = [round(float(np.percentile(r, q)), 3) for q in (5, 50, 95)]
    return out


def inside_count(bvh, co, ids, tol=0.001):
    """How many of these points lie inside the body by more than tol, and the deepest, mm."""
    deep = [depth_inside(bvh, Vector(co[i])) for i in ids]
    bad = [d for d in deep if d > tol]
    return len(bad), round(max(bad) * 1000, 1) if bad else 0.0


# ---- the check pictures ----------------------------------------------------------

def material(name, rgb, rough=0.9):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = rough
    m.diffuse_color = (*rgb, 1)
    return m


def pictures(out_prefix, centre, views=(("front", (0, -3.4, 0.1)), ("side", (3.4, 0, 0.1)), ("back", (0, 3.4, 0.1)),
                                          ("three-quarter", (2.3, -2.4, 0.4))), res=(700, 950), lens=60):
    """Workbench stills (the processor draws them in a second or two): one file per view."""
    scn = bpy.context.scene
    scn.render.engine = "BLENDER_WORKBENCH"
    scn.display.shading.light = "STUDIO"
    scn.display.shading.color_type = "MATERIAL"
    scn.display.shading.show_specular_highlight = False
    scn.render.resolution_x, scn.render.resolution_y = res
    cam = scn.camera
    if cam is None:
        cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
        scn.collection.objects.link(cam)
        scn.camera = cam
    cam.data.lens = lens
    files = []
    for label, off in views:
        cam.location = centre + Vector(off)
        cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
        scn.render.filepath = "%s-%s.png" % (out_prefix, label)
        bpy.ops.render.render(write_still=True)
        files.append(scn.render.filepath)
    return files


def worst_edges(obj, co, flat, piece_of, n=6):
    """The most stretched and most squeezed edges against the pattern: piece, ratio, and where (m)."""
    flat = np.asarray(flat)
    edges = np.array([ed.vertices[:] for ed in obj.data.edges])
    same = np.array([piece_of[a] == piece_of[b] for a, b in edges])
    edges = edges[same]
    lf = np.linalg.norm(flat[edges[:, 0]] - flat[edges[:, 1]], axis=1)
    lp = np.linalg.norm(co[edges[:, 0]] - co[edges[:, 1]], axis=1)
    ok = lf > 1e-6
    edges, r = edges[ok], lp[ok] / lf[ok]
    order = np.argsort(r)
    pick = list(order[-n:][::-1]) + list(order[:2])
    return [(piece_of[int(edges[k, 0])], round(float(r[k]), 2), [round(float(c), 3) for c in co[edges[k, 0]]]) for k in pick]


def pattern_rest(obj, smooth=8, iterations=300, uv_name="pattern"):
    """A rest shape for a welded garment: its edges the flat pattern's lengths, its bending smooth.

    WHY, 29 September (the clothing session, run 12): once the seams are
    welded the cloth remembers the shape it was welded in, crinkles and all
    (the sewing drew the sleeves up their arms and squeezed them), so the
    crinkles could never relax out. The rest shape needs only lengths and
    angles, not a place free of the body, so it is made here: the welded
    shape smoothed (the crinkles' angles gone), then each edge drawn back to
    its length on the flat pattern (each edge lies in one piece, and its
    faces' pattern UVs give that length), a few hundred rounds of moving both
    ends halfway. Set as the cloth's rest shape key, it lets the jacket settle
    out of the crinkles into broad folds, at the pattern's own size."""
    me = obj.data
    uv = me.uv_layers[uv_name]
    n = len(me.vertices)
    x = np.array([v.co[:] for v in me.vertices])
    target = {}
    for poly in me.polygons:
        li = list(poly.loop_indices)
        for k in range(len(li)):
            a, b = li[k], li[(k + 1) % len(li)]
            va, vb = me.loops[a].vertex_index, me.loops[b].vertex_index
            key = (min(va, vb), max(va, vb))
            ua, ub = uv.data[a].uv, uv.data[b].uv
            target[key] = math.hypot(ua[0] - ub[0], ua[1] - ub[1])
    edges = np.array(list(target.keys()))
    L = np.array([target[tuple(e)] for e in edges])
    deg = np.bincount(edges.ravel(), minlength=n).astype(float)
    for _ in range(smooth):
        acc = np.zeros_like(x)
        np.add.at(acc, edges[:, 0], x[edges[:, 1]])
        np.add.at(acc, edges[:, 1], x[edges[:, 0]])
        x = 0.5 * x + 0.5 * acc / np.maximum(deg, 1)[:, None]
    for _ in range(iterations):
        d = x[edges[:, 1]] - x[edges[:, 0]]
        ln = np.linalg.norm(d, axis=1)
        corr = ((ln - L) / np.maximum(ln, 1e-9))[:, None] * d * 0.5
        acc = np.zeros_like(x)
        np.add.at(acc, edges[:, 0], corr)
        np.add.at(acc, edges[:, 1], -corr)
        x = x + acc / np.maximum(deg, 1)[:, None] * 1.6
    ln = np.linalg.norm(x[edges[:, 1]] - x[edges[:, 0]], axis=1)
    r = ln / np.maximum(L, 1e-9)
    if obj.data.shape_keys is None:
        obj.shape_key_add(name="Basis")
    key = obj.shape_key_add(name="rest")
    for i in range(n):
        key.data[i].co = x[i]
    key.value = 0.0
    return [round(float(np.percentile(r, q)), 3) for q in (5, 50, 95)]


def press(obj, body_bvh, rounds=40, smooth=0.3, lengths=4, clear=0.004, uv_name="pattern"):
    """The garment pressed, as a tailor presses a finished jacket: its small crinkles smoothed out, its size
    kept, nothing inside the body. Returns the edges against the pattern (5/50/95%) and the points moved (mm).

    WHY, 29 September (the clothing session, runs 12 to 14): the sleeves come
    out of the sewing crinkled all over (their caps are stretched about 40%
    to reach the armholes, and the cloth buckles round them), and neither a
    rest shape of the pattern's lengths nor bending eight times as stiff
    settled them out. The drape's large shape is right; only its smallest
    folds are wrong. So each round moves every point a little towards the
    middle of its neighbours (the crinkles go, the large folds stay), draws
    each edge back towards its length on the flat pattern (so smoothing
    cannot shrink it), and puts any point nearer the body than `clear` back
    out along the body's normal."""
    me = obj.data
    uv = me.uv_layers[uv_name]
    n = len(me.vertices)
    x0 = np.array([v.co[:] for v in me.vertices])
    x = x0.copy()
    target = {}
    for poly in me.polygons:
        li = list(poly.loop_indices)
        for k in range(len(li)):
            a, b = li[k], li[(k + 1) % len(li)]
            va, vb = me.loops[a].vertex_index, me.loops[b].vertex_index
            ua, ub = uv.data[a].uv, uv.data[b].uv
            target[(min(va, vb), max(va, vb))] = math.hypot(ua[0] - ub[0], ua[1] - ub[1])
    edges = np.array(list(target.keys()))
    L = np.array([target[tuple(e)] for e in edges])
    deg = np.bincount(edges.ravel(), minlength=n).astype(float)
    boundary = set()
    bm = bmesh.new()
    bm.from_mesh(me)
    for e in bm.edges:
        if e.is_boundary:
            boundary.update(v.index for v in e.verts)
    bm.free()
    free = np.ones(n, dtype=bool)
    free[list(boundary)] = False                   # the hem, cuffs and neckline keep their line
    M = np.array(obj.matrix_world)
    Mi = np.linalg.inv(M)
    for _ in range(rounds):
        acc = np.zeros_like(x)
        np.add.at(acc, edges[:, 0], x[edges[:, 1]])
        np.add.at(acc, edges[:, 1], x[edges[:, 0]])
        avg = acc / np.maximum(deg, 1)[:, None]
        x[free] = x[free] + (avg[free] - x[free]) * smooth
        for _k in range(lengths):
            d = x[edges[:, 1]] - x[edges[:, 0]]
            ln = np.linalg.norm(d, axis=1)
            corr = ((ln - L) / np.maximum(ln, 1e-9))[:, None] * d * 0.5
            acc = np.zeros_like(x)
            np.add.at(acc, edges[:, 0], corr)
            np.add.at(acc, edges[:, 1], -corr)
            x = x + acc / np.maximum(deg, 1)[:, None]
        w = x @ M[:3, :3].T + M[:3, 3]
        for i in range(n):
            p = Vector(w[i])
            hit, nrm, _f, _d = body_bvh.find_nearest(p)
            if hit is not None and (p - hit).dot(nrm) < clear:
                q = hit + nrm * clear
                w[i] = (q.x, q.y, q.z)
        x = w @ Mi[:3, :3].T + Mi[:3, 3]
    for i, v in enumerate(me.vertices):
        v.co = x[i]
    me.update()
    ln = np.linalg.norm(x[edges[:, 1]] - x[edges[:, 0]], axis=1)
    r = ln / np.maximum(L, 1e-9)
    moved = np.linalg.norm(x - x0, axis=1) * 1000
    return {"edgesVsPattern": [round(float(np.percentile(r, q)), 3) for q in (5, 50, 95)],
            "movedMm": [round(float(np.percentile(moved, q)), 1) for q in (50, 95, 100)]}
