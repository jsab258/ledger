#!/usr/bin/env python
"""Re-makes the reduced reference crops of TARGET.md (kerbs and covers family), each ortho drawn at the MEASURED camera height of its panorama
(calibration_data.py), not at the 1.6 m the first draft assumed.

Needs the Poly Haven tone-mapped 8k panoramas (CC0, https://api.polyhaven.com/files/<id>, 'tonemapped')
saved as <PANO_DIR>/tm_<id>.jpg, and (for the two texture crops) the 2k diffuse of metal_grate_rusty.
Usage: /home/user/.bpyenv/bin/python make_previews.py PANO_DIR OUT_DIR
Every crop is of the object only (ground, kerb, cover): no cars, no people, no shop names, no number plates.
"""
import sys, os, numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

Image.MAX_IMAGE_PIXELS = None


def load(path):
    return np.asarray(Image.open(path).convert('RGB'))


def rot(yaw, pitch):
    cy, sy = np.cos(np.radians(yaw)), np.sin(np.radians(yaw))
    cp, sp = np.cos(np.radians(pitch)), np.sin(np.radians(pitch))
    return np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]) @ np.array([[1, 0, 0], [0, cp, sp], [0, -sp, cp]])


def to_uv(d, W, H):
    lon = np.arctan2(d[..., 0], d[..., 2])
    lat = np.arcsin(np.clip(d[..., 1] / np.linalg.norm(d, axis=-1), -1, 1))
    return (lon / (2 * np.pi) + 0.5) * W, (0.5 - lat / np.pi) * H


def sample(img, u, v):
    out = np.empty(u.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = map_coordinates(img[..., c].astype(np.float32), [v, u], order=1, mode='wrap')
    return out


def view(img, yaw, pitch, fov, w, h):
    H, W, _ = img.shape
    f = (w / 2) / np.tan(np.radians(fov) / 2)
    X, Y = np.meshgrid((np.arange(w) - w / 2 + .5) / f, -(np.arange(h) - h / 2 + .5) / f)
    d = np.stack([X, Y, np.ones_like(X)], -1) @ rot(yaw, pitch).T
    return sample(img, *to_uv(d, W, H))


def ground_ortho(img, yaw0, cam_h, x0, x1, z0, z1, mm):
    """Plane at cam_h below the camera. x right, z forward along azimuth yaw0 (deg). Picture: x right, z up."""
    H, W, _ = img.shape
    px = mm / 1000.0
    X, Z = np.meshgrid(np.arange(x0, x1, px) + px / 2, np.arange(z1, z0, -px) - px / 2)
    d = np.stack([X, np.full_like(X, -cam_h), Z], -1)
    cy, sy = np.cos(np.radians(yaw0)), np.sin(np.radians(yaw0))
    d = np.stack([d[..., 0] * cy + d[..., 2] * sy, d[..., 1], -d[..., 0] * sy + d[..., 2] * cy], -1)
    return sample(img, *to_uv(d, W, H))


def ortho_at(img, yaw_c, dist, rot_deg, hu, hv, mm, camh=1.6):
    H, W, _ = img.shape
    px = mm / 1000.0
    U, V = np.meshgrid(np.arange(-hu, hu, px) + px / 2, np.arange(hv, -hv, -px) - px / 2)
    Px, Pz = dist * np.sin(np.radians(yaw_c)), dist * np.cos(np.radians(yaw_c))
    e2 = (np.sin(np.radians(rot_deg)), np.cos(np.radians(rot_deg)))
    e1 = (np.cos(np.radians(rot_deg)), -np.sin(np.radians(rot_deg)))
    X = Px + U * e1[0] + V * e2[0]
    Z = Pz + U * e1[1] + V * e2[1]
    d = np.stack([X, np.full_like(X, -camh), Z], -1)
    return sample(img, *to_uv(d, W, H))


def save(arr, path, maxside=1200, quality=88, size_cap=300_000):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if max(im.size) > maxside:
        s = maxside / max(im.size)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    q = quality
    while True:
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) < size_cap or q <= 50:
            break
        q -= 6
    print(os.path.basename(path), im.size, os.path.getsize(path))


def mask_wrapper(v, box):
    """hide a litter wrapper (white and red pixels) inside box = (x0, y0, x1, y1) of the 1400 x 900 view with clean tarmac from below the grate"""
    from scipy.ndimage import binary_dilation, gaussian_filter
    x0, y0, x1, y1 = box
    reg = v[y0:y1, x0:x1]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    m = ((r > 165) & (g > 120) & (b > 105)) | ((r > 150) & (g < 90) & (b < 90))
    m = binary_dilation(m, iterations=7)
    patch = v[740:740 + (y1 - y0), x0:x1]   # clean tarmac straight below the grate
    w = gaussian_filter(m.astype(np.float32), 2.0)[..., None]
    out = v.copy()
    out[y0:y1, x0:x1] = reg * (1 - w) + patch * w
    return out


# The main photograph's frame, in true millimetres at the measured camera height (calibration_data.py): the first draft drew it at an assumed 1.6 m
# (x -2300 to 1100, z 3150 to 5000); the same view at the measured height spans the same angles, i.e. those numbers x h / 1.6.
def heights():
    import calibration_data as CD
    return {k: v['h_m'] for k, v in CD.HEIGHTS.items()}


def main(pano_dir, out):
    H = heights()
    os.makedirs(out, exist_ok=True)
    P = {}

    def pano(i):
        if i not in P:
            P[i] = load(os.path.join(pano_dir, f'tm_{i}.jpg'))
        return P[i]

    import corrected_numbers as CN
    r3 = H['urban_street_03'] / 1.6
    k_up = CN.N['U'] / 1000.0
    h3 = H['urban_street_03']
    x0, x1, z0, z1 = -2300 * r3 / 1000.0, 1100 * r3 / 1000.0, 3150 * r3 / 1000.0, 5000 * r3 / 1000.0
    save(ground_ortho(pano('urban_street_03'), 272.2, h3, x0, x1, z0, z1, 3.0), f'{out}/ph-urban_street_03-crossover-gully-ortho.jpg')
    save(ground_ortho(pano('urban_street_03'), 272.2, h3 - k_up, x0, x1, z0, z1, 3.0), f'{out}/ph-urban_street_03-crossover-top-ortho.jpg')
    save(view(pano('urban_street_03'), 100, -22, 22, 1200, 750), f'{out}/ph-urban_street_03-granite-kerb-run-view.jpg')
    save(view(pano('urban_street_03'), 281, -21, 16, 1200, 750), f'{out}/ph-urban_street_03-kerb-end-flank-view.jpg')
    # gully grate: ortho 1.5 mm a pixel about the grate (the first draft's distance 3.815 m and half-sizes x r)
    save(ortho_at(pano('urban_street_03'), 249.9, 3.815 * r3, 272.2, 0.45 * r3, 0.28 * r3, 1.5, h3), f'{out}/ph-urban_street_03-gully-grate-ortho.jpg')
    # footway recessed cover: the footway plane stands (U - 5) above the channel
    save(ground_ortho(pano('urban_street_03'), 272.2, h3 - (CN.N['FLAGS_Z'] / 1000.0), 0.45 * r3, 1.75 * r3, 5.35 * r3, 6.05 * r3, 3.0), f'{out}/ph-urban_street_03-footway-cover-ortho.jpg')
    rb = H['bethnal_green_entrance'] / 1.6
    save(ortho_at(pano('bethnal_green_entrance'), 10.1, 1.87 * rb, 27, 0.7 * rb, 0.7 * rb, 1.5, H['bethnal_green_entrance']), f'{out}/ph-bethnal_green_entrance-stud-cover-ortho.jpg')
    r2 = H['urban_street_02'] / 1.6
    save(ground_ortho(pano('urban_street_02'), 180, H['urban_street_02'], -0.5 * r2, 0.9 * r2, 3.0 * r2, 4.5 * r2, 3.0), f'{out}/ph-urban_street_02-tarmac-infill-cover-ortho.jpg')
    save(view(pano('birbeck_street_underpass'), 150, -22, 20, 1200, 750), f'{out}/ph-birbeck_street_underpass-concrete-kerb-view.jpg')
    v = view(pano('birbeck_street_underpass'), 0.96, -23, 12, 1400, 900)
    v = mask_wrapper(v, (846, 262, 1155, 420))   # a printed crisp wrapper lies on the grate: masked with clean tarmac from below it
    save(v, f'{out}/ph-birbeck_street_underpass-gully-grate-view.jpg')
    r4 = H['urban_street_04'] / 1.6
    save(ground_ortho(pano('urban_street_04'), 135, H['urban_street_04'], -4.0 * r4, 6.0 * r4, 2.5 * r4, 8.0 * r4, 9.0), f'{out}/ph-urban_street_04-kerb-corner-radius-ortho.jpg')
    save(view(pano('urban_street_04'), 15, -12, 24, 1200, 750), f'{out}/ph-urban_street_04-road-cover-view.jpg')
    r1 = H['urban_street_01'] / 1.6
    save(ground_ortho(pano('urban_street_01'), 20, H['urban_street_01'], -2.0 * r1, 2.0 * r1, 2.3 * r1, 4.8 * r1, 3.5), f'{out}/ph-urban_street_01-kerb-mitred-corner-ortho.jpg')
    tex = os.path.join(pano_dir, 'mgr_diff_2k.jpg')
    if os.path.exists(tex):
        save(load(tex), f'{out}/ph-metal_grate_rusty-tread-pattern.jpg')


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1], sys.argv[2])
