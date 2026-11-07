"""A head or body mesh's points and faces read out of a MetaHuman DNA uasset (big-endian RigLogic stream; DNA.h RawMesh).

Checked 7 November 2026 against Tom's exported face: the first mesh matches to 0.0002 mm. No Unreal needed.
"""
import numpy as np


def scan(p, nmin=500):
    b = np.fromfile(p, dtype=np.uint8)
    n, out = len(b), []
    for al in range(4):
        u = np.frombuffer(b[al:al + ((n - al) // 4) * 4].tobytes(), dtype=">u4")
        for i in np.where((u >= nmin) & (u <= 200000))[0]:
            N = int(u[i])
            j, k = i + 1 + N, i + 2 + 2 * N
            if k + 1 + N < len(u) and u[j] == N and u[k] == N:
                f = np.frombuffer(u[i + 1:i + 1 + N].tobytes(), dtype=">f4")
                if np.isfinite(f).all() and 2 < abs(f).max() < 1000 and len(np.unique(f)) > N * 0.5:
                    out.append((al + i * 4, N))
    return sorted(out)


def meshes(p):
    """Every RawMesh in the file: positions, then UVs, normals, layouts, faces."""
    data = open(p, "rb").read()
    res, seen = [], 0

    def u32(o):
        return int.from_bytes(data[o:o + 4], "big")

    def farr(o):
        N = u32(o)
        return np.frombuffer(data, dtype=">f4", count=N, offset=o + 4).astype(float), o + 4 + 4 * N

    def iarr(o):
        N = u32(o)
        return np.frombuffer(data, dtype=">u4", count=N, offset=o + 4).astype(np.int64), o + 4 + 4 * N

    for o, N in scan(p):
        if o < seen:
            continue
        try:
            xs, c = farr(o)
            ys, c = farr(c)
            zs, c = farr(c)
            us, c = farr(c)
            vs, c = farr(c)
            nx, c = farr(c)
            ny, c = farr(c)
            nz, c = farr(c)
            if not (len(nx) == N and abs(nx).max() <= 1.001):
                continue
            lp, c = iarr(c)
            lt, c = iarr(c)
            ln, c = iarr(c)
            if not (len(lp) == len(lt) == len(ln) and lp.max() < N):
                continue
            F = u32(c)
            c += 4
            tris = []
            for _ in range(F):
                ix, c = iarr(c)
                v = lp[ix]
                tris.extend((v[0], v[i], v[i + 1]) for i in range(1, len(v) - 1))
            res.append({"offset": o, "P": np.c_[xs, ys, zs], "tri": np.array(tris), "end": c})
            seen = c
        except Exception:
            continue
    return res


def to_blender(P):
    """DNA centimetres, y up, z forward -> the FBX files' metres, z up, front -Y."""
    return np.c_[P[:, 0], -P[:, 2], P[:, 1]] / 100.0
