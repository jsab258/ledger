#!/usr/bin/env python
"""Re-makes the reduced reference pictures of TARGET.md (bollards family) from Poly Haven's CC0 panoramas.

Needs the 8k tone-mapped JPGs (https://api.polyhaven.com/files/<id> -> 'tonemapped'; CC0) saved as <PANO_DIR>/tm_<id>.jpg.
Usage: /home/user/.bpyenv/bin/python make_previews.py PANO_DIR OUT_DIR
Every picture is of the object only: the bollard and a 15 mm margin, the rest of each elevation flat grey; the foot close-ups and the ground
pictures show paving and kerb only (no cars, no people, no lettering). Writes frames.json (the frame of each elevation, for self_check.py)."""
import sys, os, json, math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bollard_data as D
import bollard_lib as L

Image.MAX_IMAGE_PIXELS = None
MARGIN = 28.0
HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    return np.asarray(Image.open(path).convert('RGB'))


def to_uv(d, W, H):
    lon = np.arctan2(d[..., 0], d[..., 2])
    lat = np.arcsin(np.clip(d[..., 1] / np.linalg.norm(d, axis=-1), -1, 1))
    return (lon / (2 * np.pi) + .5) * W, (.5 - lat / np.pi) * H


def sample(img, u, v):
    out = np.empty(u.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = map_coordinates(img[..., c].astype(np.float32), [v, u], order=1, mode='wrap')
    return out


def rectify(img, psi, d_a, h_cam, t0, t1, z0, z1, mm):
    """square-on elevation of a vertical plane through the point at bearing psi and horizontal distance d_a (m), perpendicular to the bearing;
    columns: lateral t (mm, right positive) from t0; rows: height z above the ground from z1 down to z0"""
    H, W, _ = img.shape
    T, Z = np.meshgrid(np.arange(t0, t1, mm) + mm / 2, np.arange(z1, z0, -mm) - mm / 2)
    p = math.radians(psi)
    e_f = np.array([math.sin(p), 0, math.cos(p)]); e_t = np.array([math.cos(p), 0, -math.sin(p)])
    pts = (d_a * e_f)[None, None, :] + (T[..., None] / 1000.) * e_t[None, None, :] + np.array([0, 1, 0])[None, None, :] * ((Z[..., None] / 1000.) - h_cam)
    return sample(img, *to_uv(pts, W, H))


def ground(img, psi, d_a, h_cam, half_x, y0, y1, mm):
    H, W, _ = img.shape
    px = mm / 1000.
    X, Y = np.meshgrid(np.arange(-half_x, half_x, px) + px / 2, np.arange(y1, y0, -px) - px / 2)
    p = math.radians(psi)
    e_f = np.array([math.sin(p), 0, math.cos(p)]); e_t = np.array([math.cos(p), 0, -math.sin(p)])
    pts = (d_a * e_f)[None, None, :] + Y[..., None] * e_f[None, None, :] + X[..., None] * e_t[None, None, :] + np.array([0, -h_cam, 0])[None, None, :]
    return sample(img, *to_uv(pts, W, H))


def save(arr, path, maxside=1200, quality=88, cap=290_000):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if max(im.size) > maxside:
        s = maxside / max(im.size)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    q = quality
    while True:
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) < cap or q <= 50:
            break
        q -= 6
    print(os.path.basename(path), im.size, os.path.getsize(path))


def blur_patch(arr, t_left, z_top, mm, ta, tb, za, zb, sigma=7.0):
    """hide an embossed mark: the region t in [ta, tb], z in [za, zb] (mm) is replaced by a heavy blur of itself"""
    from scipy.ndimage import gaussian_filter
    c0, c1 = int((ta - t_left) / mm), int((tb - t_left) / mm)
    r0, r1 = int((z_top - zb) / mm), int((z_top - za) / mm)
    out = arr.copy()
    for c in range(3):
        out[r0:r1, c0:c1, c] = gaussian_filter(arr[r0 - 12:r1 + 12, c0 - 12:c1 + 12, c], sigma)[12:-12, 12:-12]
    return out


def d_axis(pano_h, depr, R):
    return pano_h / math.tan(math.radians(depr)) + R / 1000.0


def main(pano_dir, out):
    os.makedirs(out, exist_ok=True)
    T = json.load(open(os.path.join(HERE, 'target.json')))
    profiles = {k: v for k, v in T['profiles_final'].items()}
    frames = {}
    imgs = {}
    for fid, F in D.FRAMES.items():
        pano = F['pano']
        if pano not in imgs:
            imgs[pano] = load(os.path.join(pano_dir, f'tm_{pano}.jpg'))
        h = D.PANOS[pano]['h_cam']
        da = d_axis(h, F['depr'], F['R'] * h / F['h_read'])
        prof = profiles[fid]
        H = max(z for r, z in prof)
        t0, t1 = -170, 170
        z0, z1 = -70, H + 60
        mmpx = max(1.0, math.ceil((z1 - z0) / 1190.0 * 20) / 20.0)      # the picture is at most 1200 px long
        el = rectify(imgs[pano], F['psi'], da, h, t0, t1, z0, z1, mmpx)
        if fid == 'LH_b':
            el = blur_patch(el, t0, z1, mmpx, 35, 110, 55, 135)
        gray = el.mean(-1)
        a0, lean, sc = L.fit_axis(gray, mmpx, t0, z1, prof)
        # mask: the bollard and 28 mm round it; ground strip kept for the foot
        zs = z1 - (np.arange(el.shape[0]) + 0.5) * mmpx
        ts = t0 + (np.arange(el.shape[1]) + 0.5) * mmpx
        s = math.tan(math.radians(lean))
        r = L.r_of_z(prof, np.clip(zs, 0.0, H))
        r = np.where(zs < 0, max(p[0] for p in prof[:6]), r)
        r = np.where(zs > H, 0, r)
        r = np.nan_to_num(r, nan=0.0)
        keep = np.abs(ts[None, :] - (a0 + s * np.clip(zs, 0, None))[:, None]) <= (r[:, None] + (16.0 if fid == 'LH_b' else MARGIN))
        keep &= (zs[:, None] <= H + 30)
        masked = np.where(keep[..., None], el, 118.0)
        fname = f'ph-{pano}-{fid.lower()}-{F["kind"].lower()}-elevation.jpg'
        save(masked, os.path.join(out, fname))
        frames[fid] = dict(file=fname, pano=pano, mm_per_px=mmpx, t_left_mm=t0, z_top_mm=z1, h_cam_m=h, d_axis_m=round(da, 4), psi_deg=F['psi'],
                           axis_offset_mm=round(float(a0), 1), lean_deg=round(float(lean), 2), fit_score=round(float(sc), 1), kind=F['kind'])
        # foot close-up (unmasked): paving or ground and the foot, 400 mm wide
        foot = rectify(imgs[pano], F['psi'], da, h, -200, 200, -70, 230, 1.0)
        if fid == 'LH_b':
            foot = blur_patch(foot, -200, 230, 1.0, 35, 110, 55, 135)
        save(foot, os.path.join(out, f'ph-{pano}-{fid.lower()}-foot-close.jpg'))
    json.dump(frames, open(os.path.join(HERE, 'frames.json'), 'w'), indent=1)
    # ground pictures for the set-back from the kerb or the edge (z = 0 plane, axis at the centre, 0.5 m grid);
    # window per bollard (x0, x1, y0, y1 in m) chosen to leave out litter (a wrapper, a bottle) and anything not paving or kerb
    for fid, mmpx, win in (('US01_b', 3.0, (-1.6, 1.6, -1.2, 1.5)), ('BB_b', 3.0, (-1.6, 0.9, -1.1, 1.5)),
                           ('US02_a', 3.0, (-1.6, 0.3, -1.0, 0.45)), ('LH_b', 2.0, (-1.6, 1.6, -1.5, 1.5))):
        F = D.FRAMES[fid]
        pano = F['pano']
        h = D.PANOS[pano]['h_cam']
        da = d_axis(h, F['depr'], F['R'] * h / F['h_read'])
        x0, x1, y0, y1 = win
        g = ground(imgs[pano], F['psi'], da, h, 1.6, -1.5, 1.5, mmpx)          # full square, then cut to the window
        px = mmpx / 1000.0
        c0, c1 = int((x0 + 1.6) / px), int((x1 + 1.6) / px)
        r0, r1 = int((1.5 - y1) / px), int((1.5 - y0) / px)
        g = g[r0:r1, c0:c1]
        im = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
        dr = ImageDraw.Draw(im, 'RGBA')
        W, Hh = im.size
        for k in range(-1500, 1501, 500):
            x = (k / 1000.0 - x0) / px
            dr.line([(x, 0), (x, Hh)], fill=(0, 255, 255, 120))
            y = (y1 - k / 1000.0) / px
            dr.line([(0, y), (W, y)], fill=(255, 0, 255, 120))
        c = (-x0 / px, y1 / px)
        dr.ellipse([c[0] - 4, c[1] - 4, c[0] + 4, c[1] + 4], outline=(255, 255, 0, 255))
        fn = os.path.join(out, f'ph-{pano}-{fid.lower()}-ground-plan.jpg')
        save(np.asarray(im), fn)
    return frames


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
