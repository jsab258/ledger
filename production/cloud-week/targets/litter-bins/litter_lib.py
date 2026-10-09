"""Shared helpers of the litter-bins family (cloud week 42, 9 October 2026): panorama access, rectilinear and flat elevations,
the horizon (brick-course) camera-height method, colour sampling, a small glTF reader. numpy / scipy / PIL only.

The panoramas are Poly Haven's CC0 8192 x 4096 tone-mapped JPGs (api.polyhaven.com/files/<id>); they are measuring evidence only:
not placed in the game, not traced, not fed to an image model. PANO_DIR defaults to $LITTER_PANO_DIR or ./pano_cache; a missing file is
downloaded from Poly Haven (the only host the cloud reaches)."""
import json, math, os, struct, urllib.request
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get('LITTER_CACHE', '/tmp/litter-bins-cache')
PANO_DIR = os.environ.get('LITTER_PANO_DIR', os.path.join(CACHE, 'pano'))
UA = {'User-Agent': 'Mozilla/5.0 (litter-bins target writer, cloud week 42; measuring only)'}


def http_get(url, timeout=120):
    """bytes of a URL (Poly Haven refuses a request without a User-Agent)"""
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def http_json(url, timeout=60):
    return json.loads(http_get(url, timeout))
_cache = {}


def pano_path(pid):
    os.makedirs(PANO_DIR, exist_ok=True)
    p = os.path.join(PANO_DIR, f'tm_{pid}.jpg')
    if not os.path.exists(p):
        meta = http_json(f'https://api.polyhaven.com/files/{pid}')
        with open(p, 'wb') as f:
            f.write(http_get(meta['tonemapped']['url'], 300))
    return p


def load(pid):
    if pid not in _cache:
        _cache[pid] = np.asarray(Image.open(pano_path(pid)).convert('RGB'))
    return _cache[pid]


def rot(yaw, pitch):
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    return np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]) @ np.array([[1, 0, 0], [0, cp, sp], [0, -sp, cp]])


def to_uv(d, W, H):
    lon = np.arctan2(d[..., 0], d[..., 2])
    lat = np.arcsin(np.clip(d[..., 1] / np.linalg.norm(d, axis=-1), -1, 1))
    return (lon / (2 * np.pi) + .5) * W, (.5 - lat / np.pi) * H


def sample(img, u, v):
    out = np.empty(u.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = map_coordinates(img[..., c].astype(np.float32), [v, u], order=1, mode='wrap')
    return out


def view(pid, yaw, pitch, fov, w, h):
    """rectilinear view; yaw bearing (deg, from +z toward +x), pitch up positive, fov horizontal"""
    img = load(pid); H, W, _ = img.shape
    f = (w / 2) / math.tan(math.radians(fov) / 2)
    X, Y = np.meshgrid((np.arange(w) - w / 2 + .5) / f, -(np.arange(h) - h / 2 + .5) / f)
    d = np.stack([X, Y, np.ones_like(X)], -1) @ rot(yaw, pitch).T
    return sample(img, *to_uv(d, W, H))


def rectify(pid, psi, d_axis, h_cam, t0, t1, z0, z1, mm):
    """square-on elevation of the vertical plane through the point at bearing psi (deg) and horizontal distance d_axis (m),
    perpendicular to the bearing; picture x = t (right positive, from t0 to t1 mm), rows from z1 (top) to z0 (bottom), mm a pixel;
    h_cam = camera height above the ground at the object (m)."""
    img = load(pid); H, W, _ = img.shape
    px = mm / 1000.0
    T, Z = np.meshgrid(np.arange(t0 / 1000, t1 / 1000, px) + px / 2, np.arange(z1 / 1000, z0 / 1000, -px) - px / 2)
    p = math.radians(psi)
    e_f = np.array([math.sin(p), 0, math.cos(p)]); e_t = np.array([math.cos(p), 0, -math.sin(p)])
    pts = (d_axis * e_f)[None, None, :] + T[..., None] * e_t[None, None, :] + np.array([0, 1, 0])[None, None, :] * ((Z - h_cam)[..., None])
    return sample(img, *to_uv(pts, W, H))


def save_jpg(arr, path, quality=88, max_side=1200, max_kb=290):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if max(im.size) > max_side:
        s = max_side / max(im.size)
        im = im.resize((int(im.size[0] * s), int(im.size[1] * s)), Image.LANCZOS)
    q = quality
    while True:
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) <= max_kb * 1000 or q <= 40:
            break
        q -= 6
    return os.path.getsize(path)


# ---- horizon method (after bollards/calibrate.py of this cloud week; the same maths) -----------------------------------------------
def horizon_height(pid, x0, x1, y0, y1, foot_row, gauge_mm, px_pitch_by_eye):
    """camera height above the foot of a brick wall from its courses: in a levelled equirectangular panorama the horizon is the middle
    row; courses of gauge g are evenly spaced in tan(angle below the horizon); h = g * tan(theta_foot) / pitch_tan.
    returns (pitch_tan, height_mm, fit_on_edge)"""
    im = Image.fromarray(load(pid)).convert('L')
    H = im.size[1]
    a = np.asarray(im.crop((x0, y0, x1, y1)), float)
    prof = a.mean(1)
    rows = np.arange(y0, y1) + 0.5
    t = np.tan((rows - H / 2) * math.pi / H)
    tu = np.linspace(t[0], t[-1], 4 * len(t))
    pu = np.interp(tu, t, prof)
    pu = pu - np.convolve(pu, np.ones(61) / 61, mode='same')
    pu = pu[40:-40]; tu = tu[40:-40]
    guess = px_pitch_by_eye * math.pi / H
    ps = np.linspace(0.85 * guess, 1.15 * guess, 1200)
    nb = 24

    def folded(q):
        ph = ((tu - tu[0]) / q) % 1.0
        idx = np.minimum((ph * nb).astype(int), nb - 1)
        m = np.array([pu[idx == k].mean() if (idx == k).any() else 0.0 for k in range(nb)])
        return m.var()
    cs = np.array([folded(q) for q in ps])
    k = int(np.argmax(cs))
    p = float(ps[k])
    edge = k <= 2 or k >= len(ps) - 3
    tf = math.tan((foot_row - H / 2) * math.pi / H)
    return p, gauge_mm * tf / p, bool(edge)


# ---- glTF / GLB readers (positions only) --------------------------------------------------------------------------------------------
def _acc(js, binc, i):
    a = js['accessors'][i]; bv = js['bufferViews'][a['bufferView']]
    off = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    n = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[a['type']]
    ct = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8}[a['componentType']]
    return np.frombuffer(binc, dtype=ct, count=a['count'] * n, offset=off).reshape(-1, n)


def read_glb(path):
    """[(node name, Nx3 positions)] and the json, of a .glb (nodes with transforms are returned raw: the caller applies translation)"""
    b = open(path, 'rb').read()
    _, _, length = struct.unpack('<III', b[:12])
    off = 12; js = binc = None
    while off < length:
        cl, ct = struct.unpack('<II', b[off:off + 8]); data = b[off + 8:off + 8 + cl]
        if ct == 0x4E4F534A: js = json.loads(data)
        elif ct == 0x004E4942: binc = data
        off += 8 + cl
    out = []
    for n in js['nodes']:
        if 'mesh' not in n: continue
        for pr in js['meshes'][n['mesh']]['primitives']:
            out.append((n.get('name'), _acc(js, binc, pr['attributes']['POSITION']).astype(float), js['materials'][pr['material']] if 'material' in pr else {}))
    return js, out


def read_gltf(path):
    js = json.load(open(path)); binc = open(os.path.join(os.path.dirname(path), js['buffers'][0]['uri']), 'rb').read()
    out = []
    for n in js['nodes']:
        if 'mesh' not in n: continue
        m = js['meshes'][n['mesh']]
        out.append((n.get('name'), _acc(js, binc, m['primitives'][0]['attributes']['POSITION']).astype(float), n.get('translation', [0, 0, 0])))
    return js, out


def region_colour(arr, box):
    """median/p10/p90/mean sRGB of arr[y0:y1, x0:x1]"""
    x0, y0, x1, y1 = box
    c = arr[y0:y1, x0:x1].reshape(-1, 3)
    return dict(median=np.median(c, 0).round().astype(int).tolist(), p10=np.percentile(c, 10, axis=0).round().astype(int).tolist(),
                p90=np.percentile(c, 90, axis=0).round().astype(int).tolist(), mean=c.mean(0).round().astype(int).tolist(), n_px=int(len(c)))
