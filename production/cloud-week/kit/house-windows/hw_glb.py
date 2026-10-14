"""A small .glb reader for the checks (numpy only, no Blender): nodes with their triangles in the KIT frame (millimetres: x across, y into the wall, z up), vertex colours, UVs, materials, images.

glTF is y-up with the wall at negative z; the kit frame is kit (x, y, z) = (x_glb, -z_glb, y_glb) (target section 8): metres to millimetres here.
"""
import io
import json
import struct

import numpy as np
from PIL import Image

CT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


class Glb:
    def __init__(self, path):
        b = open(path, "rb").read()
        self.size = len(b)
        jl = struct.unpack("<I", b[12:16])[0]
        self.j = json.loads(b[20:20 + jl])
        off = 20 + jl
        bl = struct.unpack("<I", b[off:off + 4])[0]
        self.bin = b[off + 8:off + 8 + bl]
        self.nodes = {}
        for n in self.j["nodes"]:
            self.nodes[n["name"]] = self._node(n)

    def acc(self, i):
        a = self.j["accessors"][i]
        bv = self.j["bufferViews"][a["bufferView"]]
        dt = np.dtype(CT[a["componentType"]])
        nc = NC[a["type"]]
        start = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        stride = bv.get("byteStride", 0)
        if stride and stride != dt.itemsize * nc:
            arr = np.frombuffer(self.bin, dtype=np.uint8, count=a["count"] * stride, offset=start).reshape(a["count"], stride)
            arr = arr[:, :dt.itemsize * nc].copy().view(dt).reshape(a["count"], nc)
        else:
            arr = np.frombuffer(self.bin, dtype=dt, count=a["count"] * nc, offset=start).reshape(a["count"], nc)
        if a.get("normalized"):
            arr = arr.astype(np.float32) / float(np.iinfo(dt).max)
        return arr

    def _node(self, n):
        me = self.j["meshes"][n["mesh"]]
        T = np.array(n.get("translation", [0, 0, 0]), float)
        q = np.array(n.get("rotation", [0, 0, 0, 1]), float)
        S = np.array(n.get("scale", [1, 1, 1]), float)
        x, y, z, w = q
        R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                      [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                      [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
        P = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float)           # glTF -> kit
        pos, nor, uv, col, idx, mats = [], [], [], [], [], []
        base = 0
        for p in me["primitives"]:
            a = p["attributes"]
            v = self.acc(a["POSITION"]).astype(float)
            vw = (v * S) @ R.T + T
            pos.append(vw @ P.T * 1000.0)
            nv = self.acc(a["NORMAL"]).astype(float) @ R.T @ P.T if "NORMAL" in a else np.zeros_like(v)
            nor.append(nv)
            uv.append(self.acc(a["TEXCOORD_0"]).astype(float) if "TEXCOORD_0" in a else np.full((len(v), 2), np.nan))
            col.append(self.acc(a["COLOR_0"]).astype(float) if "COLOR_0" in a else np.full((len(v), 4), np.nan))
            ii = self.acc(p["indices"]).reshape(-1).astype(np.int64) + base
            idx.append(ii.reshape(-1, 3))
            mats.append(p.get("material"))
            base += len(v)
        pos = np.concatenate(pos)
        idx = np.concatenate(idx)
        return {"pos": pos, "nor": np.concatenate(nor), "uv": np.concatenate(uv), "col": np.concatenate(col), "tri": idx, "mat": [self.j["materials"][m]["name"] if m is not None else None for m in mats],
                "T_kit": (np.array([T[0], -T[2], T[1]]) * 1000.0), "R_kit": P @ R @ P.T, "n_tri": len(idx), "mesh": me["name"]}

    def bbox(self, name):
        p = self.nodes[name]["pos"]
        return p.min(axis=0), p.max(axis=0)

    def material(self, name):
        return next(m for m in self.j["materials"] if m["name"] == name)

    def image(self, i):
        im = self.j["images"][i]
        bv = self.j["bufferViews"][im["bufferView"]]
        data = self.bin[bv.get("byteOffset", 0):bv.get("byteOffset", 0) + bv["byteLength"]]
        return Image.open(io.BytesIO(data))

    def triangles_total(self):
        return sum(n["n_tri"] for n in self.nodes.values())

    def tri_normals(self, name):
        n = self.nodes[name]
        p = n["pos"][n["tri"]]
        nn = np.cross(p[:, 1] - p[:, 0], p[:, 2] - p[:, 0])
        ln = np.linalg.norm(nn, axis=1, keepdims=True)
        return nn / np.maximum(ln, 1e-12)
