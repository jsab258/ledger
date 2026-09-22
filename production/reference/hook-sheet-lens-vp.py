"""Find the new sheet's vanishing point from its own straight edges.

Plain numpy + scipy: gradient orientation, a simple Hough transform over the
left terrace region, the strongest non-vertical, non-horizontal lines, and the
least-squares point they converge on. Every line used is printed, and an
overlay is written so the lines can be looked at rather than trusted.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

REF = "production/reference/hook-sheet.png"
OUT = sys.argv[1]

im = Image.open(REF).convert("L")
a = np.asarray(im).astype(float)
H, W = a.shape

gx = ndimage.sobel(a, axis=1)
gy = ndimage.sobel(a, axis=0)
mag = np.hypot(gx, gy)

# THE LEFT TERRACE ONLY, x 280..1200, y 60..920: the frontage, the eaves, the
# sills and the fascias all run along the street there. The right side is a
# different building line and the far end curves.
mask = np.zeros_like(a, bool)
mask[60:920, 280:1200] = True
thr = np.percentile(mag[mask], 85)
ys, xs = np.nonzero(mask & (mag > thr))
theta_edge = np.arctan2(gy[ys, xs], gx[ys, xs])          # gradient direction
# a line's normal IS the gradient direction; keep edges whose LINE is
# between 8 and 60 degrees off horizontal (street-parallel lines on the
# terrace), which excludes verticals (pilasters, downpipes) and flat rules.
line_angle = np.degrees(theta_edge) + 90.0
line_angle = (line_angle + 90.0) % 180.0 - 90.0            # -90..90
keep = (np.abs(line_angle) > 8) & (np.abs(line_angle) < 60)
ys, xs, theta_edge = ys[keep], xs[keep], theta_edge[keep]

# Hough over (theta, rho), voting with the edge's own normal +-2 degrees.
thetas = np.radians(np.arange(-90, 90, 0.25))
diag = int(np.hypot(W, H))
acc = np.zeros((len(thetas), 2 * diag + 1), np.int32)
for dt in np.radians(np.arange(-2.0, 2.01, 0.25)):
    t = theta_edge + dt
    t = (t + np.pi / 2) % np.pi - np.pi / 2
    ti = np.clip(np.round((np.degrees(t) + 90) / 0.25).astype(int), 0, len(thetas) - 1)
    rho = np.round(xs * np.cos(thetas[ti]) + ys * np.sin(thetas[ti])).astype(int) + diag
    np.add.at(acc, (ti, rho), 1)

# strongest peaks with non-maximum suppression
lines = []
acc2 = acc.copy()
for _ in range(40):
    i, j = np.unravel_index(np.argmax(acc2), acc2.shape)
    votes = acc2[i, j]
    if votes < 25:
        break
    lines.append((thetas[i], j - diag, votes))
    acc2[max(0, i - 12):i + 13, max(0, j - 25):j + 26] = 0

# least-squares intersection of all lines, weighted by votes, then refit
# after dropping lines far from the consensus (robust to a stray rule)
def solve(ls):
    A = np.array([[np.cos(t), np.sin(t)] for t, r, v in ls])
    b = np.array([r for t, r, v in ls], float)
    w = np.array([v for t, r, v in ls], float)
    Aw = A * w[:, None]
    p, *_ = np.linalg.lstsq(Aw, b * w, rcond=None)
    res = np.abs(A @ p - b)
    return p, res

lines_used = lines
p, res = solve(lines_used)
for _ in range(3):
    med = np.median(res)
    good = [l for l, r in zip(lines_used, res) if r <= max(3 * med, 15)]
    if len(good) < 4:
        break
    lines_used = good
    p, res = solve(lines_used)
print("lines found %d, used %d" % (len(lines), len(lines_used)))
print("VANISHING POINT x=%.1f y=%.1f  (image %dx%d, centre %.0f,%.0f)" % (p[0], p[1], W, H, W / 2, H / 2))
print("residuals px: median %.1f, max %.1f" % (np.median(res), res.max()))

ov = Image.open(REF).convert("RGB")
d = ImageDraw.Draw(ov)
for t, r, v in lines_used:
    c, s_ = np.cos(t), np.sin(t)
    pts = []
    for x in (0, W):
        if abs(s_) > 1e-6:
            pts.append((x, (r - x * c) / s_))
    d.line(pts, fill=(255, 0, 255), width=2)
d.ellipse([p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10], outline=(255, 255, 0), width=4)
ov.save(OUT)
np.save(OUT + ".npy", np.array(p))
