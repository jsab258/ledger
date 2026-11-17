"""A skinned body read straight from a binary FBX, without Blender: its skin points and triangles, its skeleton's bind
pose, its bone tree and its skin weights, all in Blender's world frame (metres, z up, the body facing -y), the frame
tools/md/pose_body.py and unpose_garment.py record their turns in.

    from fbx_skin import load_skinned
    body = load_skinned("F:/LedgerTools/bodies/standard-2026-11-16/ron/ron_standard_body.fbx")
    body.verts (N, 3), body.tris (T, 3), body.bones {name: 4x4}, body.parent {name: parent}, body.weights {bone: (idx, w)}

WHY, 17 November 2026 (Kiln M5, KILN-M5-RIGGING-METHOD-2026-11-17.md step a): the turns record for each standard
body, and the bend-back that uses it, need the bodies' joints, skin and weights. Reading them here keeps both steps
testable in plain Python and runnable in seconds, with no Blender job on a shared machine. The file parser is the one
tools/body-proportions.py already uses (Kaydara binary records, its parse_fbx), with the array cap lifted.

HOW.
- The mesh read is the one with the most points (the skin, LOD0), as standard_body.py and bind_garment.py choose.
- Points are the geometry's control points, one to one with Blender's mesh vertices (the importer and exporter keep
  them), placed by the mesh's own bind-pose matrix; polygons are split into fans of triangles.
- Bones are placed by the bind pose (each node's full world matrix as bound), never by walking local offsets
  (body-proportions.py records why).
- The file's axes come from GlobalSettings: its right axis goes to Blender's +x, its up axis to +z and its front
  axis to -y; its units (UnitScaleFactor centimetres a unit) to metres. Unreal's FBX (z up) and Blender's own export
  (y up) both land in the frame Blender's importer gives, which joints-mm.json and pose_body.py's records were read in.
"""
import importlib.util
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("body_proportions", os.path.join(HERE, "..", "body-proportions.py"))
_bp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bp)
parse_fbx = _bp.parse_fbx

BIG = 1 << 40


def _name(raw):
    return raw.split("\x00")[0] if isinstance(raw, str) else str(raw)


def _gs(root):
    out = {}
    gs = root.find("GlobalSettings")
    p70 = gs.find("Properties70") if gs is not None else None
    for p in (p70.find_all("P") if p70 is not None else []):
        if p.props:
            vals = [v for v in p.props[4:]]
            out[p.props[0]] = vals[0] if len(vals) == 1 else vals
    return out


def axis_matrix(up_axis, up_sign, front_axis, front_sign, coord_axis, coord_sign):
    """3x3 taking the file's axes to Blender's: the right axis to +x, up to +z, front to -y."""
    C = np.zeros((3, 3))
    C[:, coord_axis] = [coord_sign, 0.0, 0.0]
    C[:, up_axis] = [0.0, 0.0, up_sign]
    C[:, front_axis] = [0.0, -front_sign, 0.0]
    if abs(abs(np.linalg.det(C)) - 1.0) > 1e-9:
        raise ValueError("the file's axes are not three different axes: up %d front %d right %d" % (up_axis, front_axis, coord_axis))
    return C


def file_to_blender(gs):
    """(3x3 rotation, metres per file unit) from a GlobalSettings dict."""
    C = axis_matrix(int(gs.get("UpAxis", 1)), int(gs.get("UpAxisSign", 1)), int(gs.get("FrontAxis", 2)),
                    int(gs.get("FrontAxisSign", 1)), int(gs.get("CoordAxis", 0)), int(gs.get("CoordAxisSign", 1)))
    return C, float(gs.get("UnitScaleFactor", 1.0)) / 100.0


def _mat(t):
    """FBX's column-major 16 numbers as a row-major 4x4 (translation in the last column)."""
    return np.array(t, dtype=float).reshape(4, 4).T


def _bind_ids(objs):
    ids = set()
    for p in objs.find_all("Pose"):
        if any(s == "BindPose" for s in p.props if isinstance(s, str)):
            for pn in p.find_all("PoseNode"):
                if pn.find("Node") is not None:
                    ids.add(pn.find("Node").props[0])
    return ids


def _static(path, g, mesh_name, C, unit):
    """A mesh with no bind pose (a static export): its points as stored, in Blender's frame, no bones or weights."""
    out = Skinned()
    out.path, out.mesh_name, out.geometry = path, mesh_name, g
    out.frame = {"axes": C.tolist(), "metresPerUnit": unit}
    local = np.array(g.find("Vertices").props[0], dtype=float).reshape(-1, 3)
    out.verts = local @ (C * unit).T
    pvi = np.array(g.find("PolygonVertexIndex").props[0], dtype=np.int64)
    idx = np.where(pvi < 0, -pvi - 1, pvi)
    tris, start = [], 0
    for e in np.nonzero(pvi < 0)[0]:
        poly = idx[start:e + 1]
        tris += [(poly[0], poly[k], poly[k + 1]) for k in range(1, len(poly) - 1)]
        start = e + 1
    out.tris = np.array(tris, dtype=np.int64)
    return out


class Skinned:
    def __init__(self):
        self.path = None
        self.mesh_name = None
        self.verts = None
        self.tris = None
        self.bones = {}
        self.parent = {}
        self.weights = {}
        self.frame = None
        self.geometry = None

    def joint(self, name):
        return self.bones[name][:3, 3].copy()

    def subtree(self, root):
        """The bone and every bone below it."""
        kids = {}
        for c, p in self.parent.items():
            kids.setdefault(p, []).append(c)
        out, todo = [], [root]
        while todo:
            b = todo.pop()
            out.append(b)
            todo.extend(kids.get(b, []))
        return out


def load_skinned(path, mesh=None, need_weights=True):
    """need_weights=False (step 2, skin_transfer.py) also reads a static mesh: no bones or weights required. The
    mesh's Geometry node is kept as .geometry, for callers that read its polygons or UV layers."""
    root, _version = parse_fbx(path, max_array=BIG)
    gs = _gs(root)
    C, unit = file_to_blender(gs)
    objs = root.find("Objects")
    models, geoms, clusters, skins = {}, {}, {}, set()
    for n in objs.children:
        if n.name == "Model":
            models[n.props[0]] = (_name(n.props[1]), n.props[2])
        elif n.name == "Geometry":
            geoms[n.props[0]] = n
        elif n.name == "Deformer":
            kind = n.props[2] if len(n.props) > 2 else ""
            if kind == "Cluster":
                clusters[n.props[0]] = n
            elif kind == "Skin":
                skins.add(n.props[0])
    children = {}
    parent_of = {}
    for c in root.find("Connections").find_all("C"):
        if len(c.props) >= 3 and c.props[0] == "OO":
            ch, pa = c.props[1], c.props[2]
            children.setdefault(pa, []).append(ch)
            parent_of.setdefault(ch, []).append(pa)
    # the mesh: a Model of type Mesh whose geometry has the most points (or the one named)
    best = None
    for gid, g in geoms.items():
        v = g.find("Vertices")
        if v is None or v.props[0] is None:
            continue
        owner = next((p for p in parent_of.get(gid, []) if p in models), None)
        if owner is None:
            continue
        nm = models[owner][0]
        n_pts = len(v.props[0]) // 3
        if mesh is not None and nm != mesh:
            continue
        if best is None or n_pts > best[0]:
            best = (n_pts, gid, owner, nm)
    if best is None:
        raise ValueError("%s: no mesh%s" % (path, "" if mesh is None else " named " + mesh))
    _, gid, mesh_id, mesh_name = best
    g = geoms[gid]
    if not need_weights and mesh_id not in _bind_ids(objs):
        return _static(path, g, mesh_name, C, unit)
    # bind poses: the mesh's own pose first (each skinned mesh has one), then the others for bones it lacks
    poses = [p for p in objs.find_all("Pose") if any(s == "BindPose" for s in p.props if isinstance(s, str))]
    def pose_has(p, nid):
        return any(pn.find("Node") is not None and pn.find("Node").props[0] == nid for pn in p.find_all("PoseNode"))
    poses.sort(key=lambda p: (not pose_has(p, mesh_id), -len(p.find_all("PoseNode"))))
    bind = {}
    for p in poses:
        for pn in p.find_all("PoseNode"):
            node, m = pn.find("Node"), pn.find("Matrix")
            if node is None or m is None or node.props[0] in bind:
                continue
            arr = next((x for x in m.props if isinstance(x, tuple)), None)
            if arr is not None and len(arr) >= 16:
                bind[node.props[0]] = _mat(arr)
    if mesh_id not in bind:
        raise ValueError("%s: the mesh %s has no bind-pose matrix" % (path, mesh_name))
    A = np.eye(4)
    A[:3, :3] = C * unit
    out = Skinned()
    out.path = path
    out.mesh_name = mesh_name
    out.frame = {"axes": C.tolist(), "metresPerUnit": unit}
    local = np.array(g.find("Vertices").props[0], dtype=float).reshape(-1, 3)
    M = A @ bind[mesh_id]
    out.verts = local @ M[:3, :3].T + M[:3, 3]
    pvi = np.array(g.find("PolygonVertexIndex").props[0], dtype=np.int64)
    ends = np.nonzero(pvi < 0)[0]
    idx = np.where(pvi < 0, -pvi - 1, pvi)
    tris = []
    start = 0
    for e in ends:
        poly = idx[start:e + 1]
        for k in range(1, len(poly) - 1):
            tris.append((poly[0], poly[k], poly[k + 1]))
        start = e + 1
    out.tris = np.array(tris, dtype=np.int64)
    out.geometry = g
    # bones: every LimbNode/Root model; world matrices in Blender's frame (rotation columns made unit length)
    for mid, (nm, kind) in models.items():
        if kind not in ("LimbNode", "Root", "Null") or mid not in bind:
            continue
        W = A @ bind[mid]
        R = W[:3, :3]
        W[:3, :3] = R / np.linalg.norm(R, axis=0, keepdims=True)
        out.bones[nm] = W
    for mid, (nm, kind) in models.items():
        if nm in out.bones:
            pa = next((p for p in parent_of.get(mid, []) if p in models), None)
            if pa is not None and models[pa][0] in out.bones:
                out.parent[nm] = models[pa][0]
    # weights: geometry <- skin <- clusters <- bone
    skin_ids = [c for c in children.get(gid, []) if c in skins]
    for sid in skin_ids:
        for cid in children.get(sid, []):
            if cid not in clusters:
                continue
            cl = clusters[cid]
            bone_id = next((b for b in children.get(cid, []) if b in models), None)
            if bone_id is None:
                continue
            ix, wt = cl.find("Indexes"), cl.find("Weights")
            if ix is None or wt is None or ix.props[0] is None:
                continue
            out.weights[models[bone_id][0]] = (np.array(ix.props[0], dtype=np.int64), np.array(wt.props[0], dtype=float))
    if not out.weights and need_weights:
        raise ValueError("%s: the mesh %s carries no skin weights" % (path, mesh_name))
    return out
