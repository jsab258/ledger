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
        # whichever way round lands nearer the angle asked for (the first
        # version assumed the arms always go up, and 'arms down' raised them)
        best = None
        for sgn in (1.0, -1.0):
            Rc = Matrix.Rotation(math.radians((now - deg) * sgn), 4, ax)
            dc = Rc.to_3x3() @ d
            err = abs(math.degrees(math.asin(max(-1.0, min(1.0, -dc.z)))) - deg)
            if best is None or err < best[0]:
                best = (err, Rc)
        R = best[1]
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
    for r, members in groups.items():
        if len(members) < 2:
            continue
        m = Vector(np.mean([co[i] for i in members], axis=0))
        for i in members:
            bm.verts[i].co = m
    verts = list(bm.verts)
    bmesh.ops.delete(bm, geom=[e for e in bm.edges if not e.link_faces], context="EDGES")
    # a point no face uses (two pattern points the triangulation merged) goes with its sewing edge: each group
    # is welded onto a member that is still there (the cap, 29 September)
    targetmap = {}
    for r, members in groups.items():
        alive = [verts[i] for i in members if verts[i].is_valid]
        for v in alive[1:]:
            targetmap[v] = alive[0]
    bmesh.ops.weld_verts(bm, targetmap=targetmap)
    # and a point no face uses is dropped (smoothing pulls it to the origin: the cap, 29 September)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
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


MELTON = 0.7        # kg per square metre, melton wool (Epic's own figure; FIT-AND-STIFFNESS-2026-09-29.md)


def mass_per_point(obj, density=MELTON):
    """Blender's cloth mass is per point, not per garment: the fabric's weight per area times each point's
    share of the area. (0.006 kg a point made Ron's jacket weigh 84 kg, and it sagged, clung and stretched.)"""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    area = sum(f.calc_area() for f in bm.faces)
    n = len(bm.verts)
    bm.free()
    return density * area / max(1, n)


def cloth(obj, quality=12, mass=0.01, tension=40.0, compression=40.0, shear=15.0, bending=20.0, air=2.0,
          distance=0.004, self_collision=False, self_distance=0.002, sewing=False, rest_key=None, frames=100):
    """A cloth modifier with the research's settings (OpenSew-2's, SLEEVES-RECIPE-2026-09-29.md). mass=None
    takes the true weight of melton for this mesh (mass_per_point)."""
    if mass is None:
        mass = mass_per_point(obj)
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


def press(obj, body_bvh, rounds=40, smooth=0.3, lengths=4, clear=0.004, uv_name="pattern", only=None):
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
    if only is not None:                           # a second pass on some pieces alone (the sleeves)
        keep = np.zeros(n, dtype=bool)
        keep[list(only)] = True
        free &= keep
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


def unpose(obj, arm):
    """The garment's points taken back through the skeleton's current pose to its rest pose, by the garment's
    own skin weights (vertex groups named for the bones), so that an Armature modifier on the body's own
    skeleton puts them back exactly where they are now, and carries them as the skeleton moves.

    WHY, 29 September (the clothing session): the jacket is sewn with the
    arms held out and must end in the body's rest pose. A second skeleton
    whose rest was the sewing pose (Blender's 'apply pose as rest') did
    nothing in a background run, and the arms came down out of the sleeves.
    Inverting the blended skinning transform point by point needs no
    operator: each point's pose-to-rest is the inverse of the weighted sum of
    its bones' skinning matrices."""
    A = arm.matrix_world
    Ai = A.inverted()
    S = {}
    for pb in arm.pose.bones:
        S[pb.name] = np.array(A @ pb.matrix @ pb.bone.matrix_local.inverted() @ Ai)
    names = {g.index: g.name for g in obj.vertex_groups}
    Mw = np.array(obj.matrix_world)
    Mwi = np.linalg.inv(Mw)
    moved = 0
    for v in obj.data.vertices:
        tot = 0.0
        M = np.zeros((4, 4))
        for g in v.groups:
            nm = names.get(g.group)
            if nm in S and g.weight > 0:
                M += S[nm] * g.weight
                tot += g.weight
        if tot <= 0:
            continue
        M /= tot
        p = Mw @ np.array([v.co.x, v.co.y, v.co.z, 1.0])
        r = np.linalg.solve(M, p)
        lr = Mwi @ r
        if np.linalg.norm(lr[:3] - np.array(v.co[:])) > 1e-6:
            moved += 1
        v.co = lr[:3]
    obj.data.update()
    return moved


def _hull2(pts):
    pts = sorted(set((round(float(a), 5), round(float(b), 5)) for a, b in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def _to_hull(p, hull):
    """The nearest point on a closed 2D polygon's boundary to p."""
    best, bd = None, 1e9
    n = len(hull)
    for k in range(n):
        a, b = np.array(hull[k]), np.array(hull[(k + 1) % n])
        ab = b - a
        t = max(0.0, min(1.0, float(np.dot(p - a, ab) / max(1e-12, np.dot(ab, ab)))))
        q = a + ab * t
        d = float(np.linalg.norm(p - q))
        if d < bd:
            best, bd = q, d
    return best, bd


def span_hollows(obj, ids_body, ids_front, ids_back, z_max, band=0.012, tol=0.003, deepest=0.03, smooth_rounds=6):
    """Stiff melton spans the body's small hollows instead of sinking into them: each body-piece point below
    z_max lying in a hollow of the cloth's own outline, across (a slice at its height) or down (a strip at its
    place across the front or back), no deeper than `deepest`, goes out to the outline's convex hull there;
    the moves are then smoothed over the cloth, so no slice or strip leaves a step. Returns how many points
    moved and the most, mm.

    WHY, 29 September (the clothing session, the first blind review: FAIL, 'the
    chest moulds to the body ... both pectorals and a crease under them, like
    a stretch shirt'): the drape settles into every hollow of a heavy man's
    front, under the chest and in the small of the back, where a donkey
    jacket's thick wool bridges them (the builder's jacket was filled the same
    way, slice by slice). Only small hollows, and none above the armpits: at
    the first try, unbounded, it squared the shoulders into a cardboard box
    (the slope from the neck to the shoulder is shape, not a hollow)."""
    me = obj.data
    x = np.array([v.co[:] for v in me.vertices])
    disp = np.zeros_like(x)
    body = np.array(sorted(i for i in ids_body if x[i, 2] < z_max))

    def keep(i, dv):
        if np.linalg.norm(dv) > np.linalg.norm(disp[i]):
            disp[i] = dv
    zs = x[body, 2]
    for z0 in np.arange(zs.min(), zs.max() + band, band):
        sel = body[(zs >= z0) & (zs < z0 + band)]
        if len(sel) < 8:
            continue
        hull = _hull2(x[sel][:, :2])
        if len(hull) < 3:
            continue
        for i in sel:
            q, d = _to_hull(x[i, :2], hull)
            if tol < d <= deepest:
                keep(i, np.array([q[0] - x[i, 0], q[1] - x[i, 1], 0.0]))
    for ids, sign in ((ids_front, -1.0), (ids_back, 1.0)):
        ids = np.array(sorted(i for i in ids if x[i, 2] < z_max))
        if len(ids) < 8:
            continue
        xs = x[ids, 0]
        for x0 in np.arange(xs.min(), xs.max() + band, band):
            sel = ids[(xs >= x0) & (xs < x0 + band)]
            if len(sel) < 8:
                continue
            H = np.array(_hull2([(float(x[i, 2]), float(x[i, 1]) * sign) for i in sel]))
            if len(H) < 3:
                continue
            n = len(H)
            for i in sel:
                z, o = float(x[i, 2]), float(x[i, 1]) * sign
                ext = None
                for k in range(n):
                    a, b = H[k], H[(k + 1) % n]
                    if (a[0] - z) * (b[0] - z) <= 0 and abs(b[0] - a[0]) > 1e-9:
                        e = a[1] + (b[1] - a[1]) * (z - a[0]) / (b[0] - a[0])
                        ext = e if ext is None else max(ext, e)
                if ext is not None and tol < ext - o <= deepest:
                    keep(i, np.array([0.0, (ext - o) * sign, 0.0]))
    # the moves smoothed over the cloth's own edges (no steps between slices)
    edges = np.array([e.vertices[:] for e in me.edges])
    deg = np.bincount(edges.ravel(), minlength=len(x)).astype(float)
    for _ in range(smooth_rounds):
        acc = np.zeros_like(disp)
        np.add.at(acc, edges[:, 0], disp[edges[:, 1]])
        np.add.at(acc, edges[:, 1], disp[edges[:, 0]])
        avg = acc / np.maximum(deg, 1)[:, None]
        disp = (disp + avg) * 0.5
    # nothing moves above z_max, the moves fading in over 6 cm beneath it
    fade = np.clip((z_max - x[:, 2]) / 0.06, 0.0, 1.0)[:, None]
    x = x + disp * fade
    for i, v in enumerate(me.vertices):
        v.co = x[i]
    me.update()
    mag = np.linalg.norm(disp * fade, axis=1)
    return int((mag > 0.001).sum()), round(float(mag.max()) * 1000, 1)



def torso_weights(obj, arm_bones=ARMISH, keep_near=0.06, uv_name="pattern", smooth=8):
    """The garment's copied skin weights put right for a jacket: the body pieces (their flat pattern at u
    within 1.5) lose the arms' weights except within keep_near of a sleeve, then every weight is smoothed and
    normalised, so the change from arm to torso spreads over the armhole instead of one row.

    WHY (FIT-AND-STIFFNESS-2026-09-29.md): copied from the nearest place on the
    body, the side panels took upper-arm weights, and raising the arm dragged
    the side of the jacket up into a sail."""
    me = obj.data
    uv = me.uv_layers[uv_name]
    u_of = {lp.vertex_index: uv.data[lp.index].uv[0] for lp in me.loops}
    co = np.array([v.co[:] for v in me.vertices])
    sleeve = np.array([i for i, u in u_of.items() if abs(u) >= 1.5])
    tree = None
    if len(sleeve):
        from mathutils.kdtree import KDTree
        tree = KDTree(len(sleeve))
        for k, i in enumerate(sleeve):
            tree.insert(Vector(co[i]), k)
        tree.balance()
    arm_groups = [g.index for g in obj.vertex_groups if g.name.startswith(arm_bones)]
    cut = 0
    for v in me.vertices:
        if abs(u_of.get(v.index, 0.0)) >= 1.5:
            continue
        if tree is not None and tree.find(v.co)[2] < keep_near:
            continue
        for gi in arm_groups:
            try:
                obj.vertex_groups[gi].remove([v.index])
                cut += 1
            except RuntimeError:
                pass
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
    if smooth:
        bpy.ops.object.vertex_group_smooth(group_select_mode="ALL", factor=0.5, repeat=smooth)
    bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    return cut


# ---- the body's sections, and a collider for trousers --------------------------------

def section_loops(obj, co, no):
    """The body cut by a plane (a point on it and its normal, world space): each closed or open line of the
    cut as an array of points (m), in order along the line."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.transform(obj.matrix_world)
    r = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no)
    cut = [e for e in r["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    adj = {}
    for e in cut:
        a, b = e.verts
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    seen, loops = set(), []
    # open lines first from their ends, then whatever is left is closed
    starts = [v for v in adj if len(adj[v]) == 1] + list(adj)
    for s in starts:
        if s in seen:
            continue
        line, prev, cur = [s], None, s
        seen.add(s)
        while True:
            nxt = [n for n in adj[cur] if n is not prev and n not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)
            line.append(cur)
        loops.append(np.array([v.co[:] for v in line]))
    bm.free()
    return loops


def part_thighs(body, apart=0.008, z_lo=0.74, z_full=(0.80, 0.875), z_hi=0.895, reach=0.05):
    """The inner thighs moved apart by `apart` each where they touch, as a shape key 'apart' set on: a
    collider only, so trousers' cloth can lie between them.

    WHY, 29 September (the work trousers, CLOTHES.md item 4): Ron's thighs
    touch from his crotch 8 cm down (sections through his body: no gap
    between them from 0.80 to 0.885 m). Cloth cannot lie between two surfaces
    that touch; a collision pushes it out in front or behind, a web across
    the crotch. A real pair of trousers lies there pressed between the
    thighs; parted by 8 mm each, the two layers of cloth fit."""
    if body.data.shape_keys is None:
        body.shape_key_add(name="Basis")
    key = body.shape_key_add(name="apart")
    M = body.matrix_world
    Mi = M.inverted()
    moved = 0
    for v in body.data.vertices:
        w = M @ v.co
        ax = abs(w.x)
        if ax >= reach or w.z <= z_lo or w.z >= z_hi or ax < 1e-5:
            continue
        if w.z < z_full[0]:
            f = (w.z - z_lo) / (z_full[0] - z_lo)
        elif w.z > z_full[1]:
            f = (z_hi - w.z) / (z_hi - z_full[1])
        else:
            f = 1.0
        g = 1.0 - ax / reach
        d = apart * f * g * (1.0 if w.x > 0 else -1.0)
        key.data[v.index].co = Mi @ (w + Vector((d, 0.0, 0.0)))
        moved += 1
    key.value = 1.0
    return moved


def relax(obj, pairs, fixed, body_bvh, iterations=300, clear=0.004, uv_name="pattern", ramp=100, report=None,
          gravity=0.0, length_rounds=1):
    """The garment sewn by projection, without dynamics: each round every edge is drawn towards its length on
    the flat pattern, every seam pair towards its midpoint (gently at first, `ramp` rounds to full), the
    `fixed` points put back, and anything nearer the body than `clear` put out along its normal. Returns the
    widest seam gap (mm) and the edges against the pattern (5/50/95%).

    WHY, 29 September (the work trousers, runs 4 and 5): Blender's sewing
    springs, weightless and fast, pulled the trouser legs up the calves into
    a crumple and left two seams 5 cm open, because the laying out had a band
    of cloth stretched fourteen times at the crotch that the placed rest shape
    kept. A projection has no momentum: it takes each piece towards its
    pattern and each seam shut a little at a time, the body always in the way."""
    me = obj.data
    uv = me.uv_layers[uv_name]
    n = len(me.vertices)
    M = np.array(obj.matrix_world)
    x = np.array([v.co[:] for v in me.vertices]) @ M[:3, :3].T + M[:3, 3]
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
    P = np.array(pairs) if len(pairs) else np.zeros((0, 2), dtype=int)
    fx = np.zeros(n, dtype=bool)
    fx[list(fixed)] = True
    x0 = x.copy()
    for it in range(iterations):
        if gravity:
            # SETTLED THE SAME WAY (29 September, run 6: Blender's cloth, settling
            # the projection-sewn trousers under gravity, let them fall through the
            # body at the fly, a hip and a buttock): each round a small step down,
            # then the pattern's lengths and the body take it back
            x[:, 2] -= gravity
        for _r in range(length_rounds):
            d = x[edges[:, 1]] - x[edges[:, 0]]
            ln = np.linalg.norm(d, axis=1)
            corr = ((ln - L) / np.maximum(ln, 1e-9))[:, None] * d * 0.5
            acc = np.zeros_like(x)
            np.add.at(acc, edges[:, 0], corr)
            np.add.at(acc, edges[:, 1], -corr)
            x = x + acc / np.maximum(deg, 1)[:, None]
            x[fx] = x0[fx]
        if len(P):
            rate = 0.5 * min(1.0, (it + 1) / max(1, ramp))
            mid = 0.5 * (x[P[:, 0]] + x[P[:, 1]])
            x[P[:, 0]] += (mid - x[P[:, 0]]) * rate
            x[P[:, 1]] += (mid - x[P[:, 1]]) * rate
        x[fx] = x0[fx]
        for i in range(n):
            p = Vector(x[i])
            hit, nrm, _f, _d = body_bvh.find_nearest(p)
            if hit is not None and (p - hit).dot(nrm) < clear:
                x[i] = hit + nrm * clear
        if report and (it + 1) % 50 == 0:
            gap = float(np.max(np.linalg.norm(x[P[:, 0]] - x[P[:, 1]], axis=1))) * 1000 if len(P) else 0.0
            report("relax round %d: widest seam gap %.1f mm" % (it + 1, gap))
    Mi = np.linalg.inv(M)
    xl = x @ Mi[:3, :3].T + Mi[:3, 3]
    for i, v in enumerate(me.vertices):
        v.co = xl[i]
    me.update()
    ln = np.linalg.norm(x[edges[:, 1]] - x[edges[:, 0]], axis=1)
    r = ln / np.maximum(L, 1e-9)
    gap = float(np.max(np.linalg.norm(x[P[:, 0]] - x[P[:, 1]], axis=1))) * 1000 if len(P) else 0.0
    return round(gap, 1), [round(float(np.percentile(r, q)), 3) for q in (5, 50, 95)]


# ---- the test poses (moved from pose_test.py, 29 September, for the trousers' test too) ----------------

def turn(arm, bone, axis, deg, child=None, want=None):
    """Turn a pose bone about a world axis through its own joint. If `want` is given (a world direction), the
    sign is chosen so that `child`'s joint moves that way."""
    pb = arm.pose.bones[bone]
    bpy.context.view_layer.update()
    M = arm.matrix_world
    head = pb.head.copy()
    before = pb.matrix.copy()

    def apply(sign):
        R = Matrix.Rotation(math.radians(deg * sign), 4, axis)
        Ra = (M.inverted() @ R @ M).to_3x3().to_4x4()
        pb.matrix = Matrix.Translation(head) @ Ra @ Matrix.Translation(-head) @ before
        bpy.context.view_layer.update()

    if want is None or child is None:
        apply(1)
        return
    c0 = M @ arm.pose.bones[child].head
    apply(1)
    moved = (M @ arm.pose.bones[child].head) - c0
    if moved.dot(want) < 0:
        apply(-1)


def make_pose(arm, name):
    X, Z = Vector((1, 0, 0)), Vector((0, 0, 1))
    fwd, up = Vector((0, -1, 0)), Vector((0, 0, 1))
    if name in ("down", "walk", "sit", "stair"):
        pose_arms(arm, 80.0)
    if name == "up":
        pose_arms(arm, -35.0)
    if name == "walk":
        turn(arm, "thigh_l", X, 25, "calf_l", fwd)
        turn(arm, "thigh_r", X, 15, "calf_r", -fwd)
        turn(arm, "calf_r", X, 30, "foot_r", -fwd + up * 0.3)
        turn(arm, "upperarm_l", X, 20, "lowerarm_l", -fwd)       # arms swing against the legs
        turn(arm, "upperarm_r", X, 20, "lowerarm_r", fwd)
    if name == "stair":
        # one foot up a stair: the left thigh 55 degrees forward, its knee bent 75
        turn(arm, "thigh_l", X, 55, "calf_l", fwd)
        turn(arm, "calf_l", X, 75, "foot_l", -fwd - up)
    if name == "sit":
        turn(arm, "spine_01", X, 10, "spine_03", fwd)
        for s in ("l", "r"):
            turn(arm, "thigh_" + s, X, 85, "calf_" + s, fwd + up)
            turn(arm, "calf_" + s, X, 85, "foot_" + s, -fwd - up)
            turn(arm, "lowerarm_" + s, X, 50, "hand_" + s, fwd)


def bridge_slices(obj, z_lo, z_hi, split_z, step=0.008, deepest=0.04, smooth_rounds=10):
    """Heavy cloth bridges the body's hollows: each horizontal slice of the garment between z_lo and z_hi goes
    out to its own convex hull (the whole slice above split_z; below it, each side's, x > 0 and x < 0, apart),
    each point no more than `deepest`; the moves are then smoothed over the cloth so no slice leaves a step.
    Returns how many points moved and the most, mm.

    WHY, 29 September (the work trousers, first blind review: 'it wraps the
    seat so closely that the cleft between the buttocks shows ... like thin
    stretch fabric, not heavy work twill'): the projection lays the cloth on
    the body wherever the pattern's lengths allow; twill spans the cleft."""
    me = obj.data
    M = np.array(obj.matrix_world)
    x = np.array([v.co[:] for v in me.vertices]) @ M[:3, :3].T + M[:3, 3]
    disp = np.zeros_like(x)
    for z in np.arange(z_lo, z_hi, step):
        sel = np.where(np.abs(x[:, 2] - z) < step * 0.5)[0]
        groups = [sel] if z > split_z else [sel[x[sel, 0] > 0], sel[x[sel, 0] < 0]]
        for g in groups:
            if len(g) < 6:
                continue
            hull = _hull2(x[g, :2])
            if len(hull) < 3:
                continue
            for i in g:
                q, d = _to_hull(x[i, :2], hull)
                if 1e-4 < d <= deepest:
                    disp[i, :2] = q - x[i, :2]
    edges = np.array([e.vertices[:] for e in me.edges])
    deg = np.bincount(edges.ravel(), minlength=len(x)).astype(float)
    mag0 = np.linalg.norm(disp, axis=1)
    for _ in range(smooth_rounds):
        acc = np.zeros_like(disp)
        np.add.at(acc, edges[:, 0], disp[edges[:, 1]])
        np.add.at(acc, edges[:, 1], disp[edges[:, 0]])
        avg = acc / np.maximum(deg, 1)[:, None]
        # smoothed, but never below what a point needed to reach its hull
        grow = np.linalg.norm(avg, axis=1) > np.linalg.norm(disp, axis=1)
        disp = np.where(grow[:, None] | (mag0[:, None] < 1e-6), 0.5 * (disp + avg), disp)
    x = x + disp
    Mi = np.linalg.inv(M)
    xl = x @ Mi[:3, :3].T + Mi[:3, 3]
    for i, v in enumerate(me.vertices):
        v.co = xl[i]
    me.update()
    mag = np.linalg.norm(disp, axis=1)
    return int((mag > 0.001).sum()), round(float(mag.max()) * 1000, 1)


def smooth_edges_of(obj, z_max, rounds=12):
    """The garment's open edges below z_max (a trouser leg's hem) smoothed along themselves: each point to the
    middle of its two neighbours on the edge, `rounds` times. Returns how many points moved.

    WHY, 29 September (the work trousers, first blind review: 'the edge is
    crinkled like torn paper'): the hem is where the projection's rows ran
    round the foot; a hem is a clean, turned edge."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    nb = {}
    for e in bm.edges:
        if e.is_boundary:
            a, b = e.verts
            nb.setdefault(a.index, []).append(b.index)
            nb.setdefault(b.index, []).append(a.index)
    M = obj.matrix_world
    ids = [i for i, n in nb.items() if len(n) == 2 and (M @ bm.verts[i].co).z < z_max]
    co = {i: bm.verts[i].co.copy() for i in nb}
    for _ in range(rounds):
        new = {}
        for i in ids:
            a, b = nb[i]
            new[i] = 0.5 * co[i] + 0.25 * (co[a] + co[b])
        co.update(new)
    for i in ids:
        bm.verts[i].co = co[i]
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    return len(ids)
