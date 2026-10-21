"""The fish market's awning (awning_02.glb, the held prop) read from the repository: used by make_target.py (to write the walking-strip numbers) and by self_check.py (to recompute them).
The body of the awning slopes: it falls from the fascia's underside at the frontage wall to a front edge over the rail line, with a scalloped valance hanging below that edge."""
import json, math, os, struct
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
GLB = os.path.join(ROOT, 'ledger/Assets/Props/base-mesh/awning_02.glb')
# the scene's piece prop_awning_02_0 (production/specs/vignette-pieces.json): centre and size in metres
AWP = dict(x_m=12.0, y_m=2.28835, z_m=4.25745, sx_m=3.0, sy_m=1.3233, sz_m=1.7351)
FRONTAGE_Z = 5.125


def read_awning(path=GLB):
    data = open(path, 'rb').read()
    magic, ver, length = struct.unpack_from('<4sII', data, 0)
    off, js, binb = 12, None, None
    while off < length:
        clen, ctype = struct.unpack_from('<I4s', data, off)
        chunk = data[off + 8: off + 8 + clen]
        if ctype == b'JSON':
            js = json.loads(chunk.decode())
        elif ctype == b'BIN\x00':
            binb = chunk
        off += 8 + clen
    acc = js['accessors'][js['meshes'][0]['primitives'][0]['attributes']['POSITION']]
    bv = js['bufferViews'][acc['bufferView']]
    base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    stride = bv.get('byteStride', 12)
    pts = np.array([struct.unpack_from('<fff', binb, base + i * stride) for i in range(acc['count'])])
    front = pts[:, 2] > 1.72
    return dict(depth_m=round(float(pts[:, 2].max()), 4), width_m=round(float(pts[:, 0].max() - pts[:, 0].min()), 3), mesh_y_min=round(float(pts[:, 1].min()), 4), mesh_y_max=round(float(pts[:, 1].max()), 4),
                body_front_edge_mesh_y=round(float(pts[front][:, 1].max()), 4), valance_bottom_mesh_y=round(float(pts[front][:, 1].min()), 4))


AW = read_awning()
y_off = AWP['y_m'] - (AW['mesh_y_min'] + AW['mesh_y_max']) / 2.0     # world y = mesh y + this
slope = -AW['body_front_edge_mesh_y'] / AW['depth_m']                 # the body falls this much per metre of projection


def footway_y(z):
    return 0.05 + (z - 3.125) / 40.0                                  # the scene's section: kerb top 0.05 at the kerb's back, 1 in 40 up


def underside_above_footway(z):
    zl = FRONTAGE_Z - z
    return (y_off + 0.0 - slope * zl) - footway_y(z)


def valance_bottom_above_footway(z=3.39):
    return y_off + AW['valance_bottom_mesh_y'] - footway_y(z)


def clear_at_height(h_m, rear_face=3.400, stallriser_face=4.975):
    """the free width between the rail's rear face and the stallriser face for a body h_m high: the awning's sloping underside must clear its head"""
    z = rear_face
    while z < stallriser_face and underside_above_footway(z) < h_m:
        z += 0.0005
    return round(stallriser_face - max(z, rear_face), 3)
