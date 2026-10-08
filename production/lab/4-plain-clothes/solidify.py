"""Fuse a garment's modelled parts into one smooth surface.

The parts (closed tubes of sections, and the shoulder layer lifted off the body) overlap where
they meet: the jumper's body and yoke with each sleeve at the armhole, the two legs and the
seat at the crotch. Each part is measured as a signed distance on a 5 mm grid (exact distance
to its sections), parts unite by the smaller distance, a light blur of the distance rounds the
joins, and the surface is its zero level (surface nets), lightly smoothed and cut open at the
hem, cuffs and waist. The body is never moved and nothing is simulated.

The poke-through check reads the same distance: a body point is covered if it is negative there.
"""
import numpy as np
from scipy import ndimage
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

LEVEL = 0.5


BIG = 0.05


class Grid:
    """A garment's solid as a signed distance on a grid (metres, negative inside). Parts unite by
    taking the smaller distance; a light blur of the distance rounds the joins; the surface is
    its zero level, so it lies where the sections put it to well under a millimetre."""

    def __init__(self, lo, hi, h=0.005):
        self.h = h
        self.lo = np.asarray(lo, float) - 3 * h
        self.shape = tuple(int(x) for x in np.ceil((np.asarray(hi, float) + 3 * h - self.lo) / h) + 1)
        self.sdf = np.full(self.shape, BIG, np.float32)
        self.field = None

    def points(self, sl=None):
        return [self.lo[i] + self.h * np.arange(self.shape[i]) for i in range(3)]

    def _box(self, lo, hi):
        ax = self.points()
        ix = [np.where((ax[i] >= lo[i]) & (ax[i] <= hi[i]))[0] for i in range(3)]
        I, J, K = np.meshgrid(*ix, indexing="ij")
        I, J, K = I.ravel(), J.ravel(), K.ravel()
        return I, J, K, np.stack([ax[0][I], ax[1][J], ax[2][K]], 1)

    def _put(self, I, J, K, sd):
        sd = np.clip(sd, -BIG, BIG).astype(np.float32)
        self.sdf[I, J, K] = np.minimum(self.sdf[I, J, K], sd)

    def add_slices(self, rings, axes_ok=True):
        """A tube of horizontal rings (m, n, 3): each grid layer's distance to the ring at its height."""
        ax = self.points()
        zs = rings[:, 0, 2]
        X, Y = np.meshgrid(ax[0], ax[1], indexing="ij")
        XY = np.stack([X.ravel(), Y.ravel()], 1)
        for k, z in enumerate(ax[2]):
            if z < zs.min() - 1e-9 or z > zs.max() + 1e-9:
                continue
            r = int(np.argmin(np.abs(zs - z)))
            Q = rings[r][:, :2]
            lo, hi = Q.min(0) - BIG, Q.max(0) + BIG
            box = (XY[:, 0] >= lo[0]) & (XY[:, 0] <= hi[0]) & (XY[:, 1] >= lo[1]) & (XY[:, 1] <= hi[1])
            sd = np.full(len(XY), BIG, np.float32)
            sd[box] = sd_poly(XY[box], Q)
            self.sdf[:, :, k] = np.minimum(self.sdf[:, :, k], sd.reshape(X.shape))

    def add_tube(self, rings, C, A):
        """A tube of rings square to a bent axis: each grid point near it measured in the plane of
        the ring whose plane is nearest."""
        lo = rings.reshape(-1, 3).min(0) - 0.03
        hi = rings.reshape(-1, 3).max(0) + 0.03
        I, J, K, P = self._box(lo, hi)
        sd = np.full(len(P), BIG)
        for s in range(0, len(P), 100000):
            sd[s:s + 100000] = signed_tube(P[s:s + 100000], rings, C, A)
        self._put(I, J, K, sd)

    def add_near(self, BV, BN, region, dist, depth=0.04):
        """A layer lifted off the body over a region: between `depth` inside the body and
        dist(nearest body point) outside it, for points whose nearest body point is in the region."""
        pts = BV[region]
        dmax = float(dist.max())
        lo, hi = pts.min(0) - dmax - depth, pts.max(0) + dmax + depth
        I, J, K, P = self._box(lo, hi)
        full = np.zeros(len(BV))
        full[region] = dist
        d, j = cKDTree(BV).query(P, distance_upper_bound=dmax + depth)
        ok = np.isfinite(d)
        ok[ok] = region[j[ok]]
        jj = j[ok]
        sn = np.einsum("ij,ij->i", P[ok] - BV[jj], BN[jj])
        sd = np.maximum(sn - full[jj], -depth - sn)
        self._put(I[ok], J[ok], K[ok], sd)

    def finish(self, sigma_m=0.004):
        self.field = ndimage.gaussian_filter(self.sdf, sigma_m / self.h) if sigma_m > 0 else self.sdf.copy()

    def merge_max(self, others):
        """Unite separately finished solids: the smaller distance wins, so pieces meet in a crease
        (a seam) instead of webbing across the gaps between them."""
        for o in others:
            self.field = np.minimum(self.field, o.field)

    def sample(self, P):
        """The signed distance at world points (trilinear); negative inside."""
        q = (np.asarray(P) - self.lo) / self.h
        return ndimage.map_coordinates(self.field, q.T, order=1, mode="constant", cval=BIG)

    def surface(self, smooth_iters=8):
        V, F = surface_nets(-self.field, 0.0)
        V = self.lo + V * self.h
        V, F = largest_component(V, F)
        V = taubin(V, F, smooth_iters)
        return V, F


def sd_poly(P, Q):
    """Signed distance from 2D points to a closed polygon (negative inside)."""
    A = Q[None, :, :]
    Bq = np.roll(Q, -1, 0)[None, :, :]
    AB = Bq - A
    AP = P[:, None, :] - A
    t = np.clip(np.einsum("pmk,pmk->pm", AP, np.broadcast_to(AB, AP.shape)) / np.maximum((AB ** 2).sum(-1), 1e-18), 0, 1)
    D = np.linalg.norm(AP - t[..., None] * AB, axis=2).min(1)
    return np.where(in_poly(P, Q), -D, D)


def signed_tube(P, R, C, A, reach=0.35, slab=0.008):
    Dp = np.einsum("pmk,mk->pm", P[:, None, :] - C[None], A)
    far = np.linalg.norm(P[:, None, :] - C[None], axis=2) > reach
    D = np.where(far, np.inf, np.abs(Dp))
    i = np.argmin(D, axis=1)
    ok = D[np.arange(len(P)), i] <= slab
    out = np.full(len(P), BIG)
    for r in np.unique(i[ok]):
        sel = np.where(ok & (i == r))[0]
        e1, e2 = _basis(A[r])
        q = P[sel] - C[r]
        Q = R[r] - C[r]
        out[sel] = sd_poly(np.stack([q @ e1, q @ e2], 1), np.stack([Q @ e1, Q @ e2], 1))
    return out


def in_poly(P, Q):
    x, y = P[:, 0][:, None], P[:, 1][:, None]
    x1, y1 = Q[:, 0][None], Q[:, 1][None]
    x2, y2 = np.roll(Q[:, 0], -1)[None], np.roll(Q[:, 1], -1)[None]
    dy = np.where(y2 == y1, 1e-12, y2 - y1)
    c = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / dy + x1)
    return (c.sum(1) % 2) == 1


def _basis(a):
    e1 = np.cross(a, [0, 0, 1.0]) if abs(a[2]) < 0.99 else np.array([1.0, 0, 0])
    e1 /= np.linalg.norm(e1)
    return e1, np.cross(a, e1)


def inside_tube(P, R, C, A, reach=0.35, slab=0.008):
    D = np.einsum("pmk,mk->pm", P[:, None, :] - C[None], A)
    far = np.linalg.norm(P[:, None, :] - C[None], axis=2) > reach
    D = np.where(far, np.inf, np.abs(D))
    i = np.argmin(D, axis=1)
    ok = D[np.arange(len(P)), i] <= slab
    out = np.zeros(len(P), bool)
    for r in np.unique(i[ok]):
        sel = np.where(ok & (i == r))[0]
        e1, e2 = _basis(A[r])
        q = P[sel] - C[r]
        Q = R[r] - C[r]
        out[sel] = in_poly(np.stack([q @ e1, q @ e2], 1), np.stack([Q @ e1, Q @ e2], 1))
    return out


CORNERS = [(i, j, k) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
EDGES = [(a, b) for a in range(8) for b in range(a + 1, 8)
         if sum(abs(CORNERS[a][t] - CORNERS[b][t]) for t in range(3)) == 1]


def surface_nets(f, level):
    """Naive surface nets: one vertex per cell the surface crosses (the mean of its edge
    crossings), one quad per grid edge the surface crosses; quads wound outward."""
    s = f > level
    nx, ny, nz = f.shape
    c = np.stack([s[i:nx - 1 + i, j:ny - 1 + j, k:nz - 1 + k] for i, j, k in CORNERS])
    active = c.any(0) & ~c.all(0)
    ids = np.argwhere(active)
    idx = -np.ones(active.shape, np.int64)
    idx[tuple(ids.T)] = np.arange(len(ids))
    vals = np.stack([f[ids[:, 0] + i, ids[:, 1] + j, ids[:, 2] + k] for i, j, k in CORNERS], 1)
    acc = np.zeros((len(ids), 3))
    cnt = np.zeros(len(ids))
    for a, b in EDGES:
        fa, fb = vals[:, a], vals[:, b]
        m = (fa > level) != (fb > level)
        t = (level - fa[m]) / (fb[m] - fa[m])
        pa, pb = np.array(CORNERS[a], float), np.array(CORNERS[b], float)
        acc[m] += pa + t[:, None] * (pb - pa)
        cnt[m] += 1
    V = ids + acc / cnt[:, None]
    quads = []
    # x-edges: cells (i, j-1..j, k-1..k)
    e = s[:-1, 1:-1, 1:-1] != s[1:, 1:-1, 1:-1]
    i, j, k = np.nonzero(e)
    j, k = j + 1, k + 1
    q = np.stack([idx[i, j - 1, k - 1], idx[i, j, k - 1], idx[i, j, k], idx[i, j - 1, k]], 1)
    out = s[i, j, k]
    quads.append(np.where(out[:, None], q, q[:, ::-1]))
    # y-edges: cells (i-1..i, j, k-1..k)
    e = s[1:-1, :-1, 1:-1] != s[1:-1, 1:, 1:-1]
    i, j, k = np.nonzero(e)
    i, k = i + 1, k + 1
    q = np.stack([idx[i - 1, j, k - 1], idx[i - 1, j, k], idx[i, j, k], idx[i, j, k - 1]], 1)
    out = s[i, j, k]
    quads.append(np.where(out[:, None], q, q[:, ::-1]))
    # z-edges: cells (i-1..i, j-1..j, k)
    e = s[1:-1, 1:-1, :-1] != s[1:-1, 1:-1, 1:]
    i, j, k = np.nonzero(e)
    i, j = i + 1, j + 1
    q = np.stack([idx[i - 1, j - 1, k], idx[i, j - 1, k], idx[i, j, k], idx[i - 1, j, k]], 1)
    out = s[i, j, k]
    quads.append(np.where(out[:, None], q, q[:, ::-1]))
    Q = np.vstack(quads)
    Q = Q[(Q >= 0).all(1)]
    F = np.vstack([Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]])
    return V, F


def largest_component(V, F):
    n = len(V)
    A = coo_matrix((np.ones(len(F) * 3), (F.ravel(), np.roll(F, 1, 1).ravel())), shape=(n, n))
    _, lab = connected_components(A, directed=False)
    big = np.bincount(lab[F[:, 0]]).argmax()
    F = F[lab[F[:, 0]] == big]
    used = np.unique(F)
    remap = -np.ones(n, np.int64)
    remap[used] = np.arange(len(used))
    return V[used], remap[F]


def taubin(V, F, iters, lam=0.5, mu=-0.53):
    n = len(V)
    rows = np.concatenate([F[:, 0], F[:, 1], F[:, 2], F[:, 1], F[:, 2], F[:, 0]])
    cols = np.concatenate([F[:, 1], F[:, 2], F[:, 0], F[:, 0], F[:, 1], F[:, 2]])
    W = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n)).tocsr()
    W.data[:] = 1.0
    deg = np.asarray(W.sum(1)).ravel()
    for _ in range(iters):
        for f in (lam, mu):
            V = V + f * (W @ V / deg[:, None] - V)
    return V


def face_normals(V, F):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)


def open_end(V, F, C, A, h):
    """Remove the cap the solid makes across an opening: faces at the end plane (centre C,
    outward axis A) facing out along it."""
    N = face_normals(V, F)
    d = np.einsum("fij,j->fi", V[F] - C, A)
    near = (d > -2.5 * h).all(1)
    cap = near & (N @ A > 0.6)
    F = F[~cap]
    used = np.unique(F)
    remap = -np.ones(len(V), np.int64)
    remap[used] = np.arange(len(used))
    return V[used], remap[F]


def clip_open(V, F, C, A):
    """Open the surface at a plane (centre C, outward axis A): faces wholly beyond it go, and
    the vertices left beyond it are laid on the plane, so the opening has a crisp edge."""
    d = (V - C) @ A
    keep = ~(d[F] > 0).all(1)
    F = F[keep]
    V = V.copy()
    out = d > 0
    V[out] -= d[out, None] * A[None, :]
    used = np.unique(F)
    remap = -np.ones(len(V), np.int64)
    remap[used] = np.arange(len(used))
    return V[used], remap[F]
