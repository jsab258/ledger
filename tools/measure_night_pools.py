"""How far the night's light falls between the lamps, measured in a frame (the proof frame's night test).

    python tools/measure_night_pools.py FRAME.png [FRAME2.png ...]
    python tools/measure_night_pools.py --selftest

WHY, 1 October (the proof frame, stage 1; production/research/aaa-street,
section 3): real sodium pools fall off by about four stops between lamps (a
35 W lamp on a 6 m column: about 10 lux beneath it, 0.5 lux midway, 4.3
stops), and the street's night read as "one flat orange". This reads the
ground in the bottom third of a frame (road and pavement in the hook camera's
view) as relative luminance from its sRGB pixels, and prints the spread in
stops between its bright pools and its dark gaps (the 95th and the 10th
percentile), the share of near-black, and the mean hue, so the night test's
frames (sky light off, fog off, both) can be compared by number as well as by
eye. Pixel values after the tonemapper are not scene light: the spread here
is what the player sees, which is what has to read as pools.
"""
import sys

import numpy as np
from PIL import Image


def lum(rgb):
    x = rgb / 255.0
    lin = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
    return 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]


def measure(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(float)
    h = im.shape[0]
    ground = im[int(h * 2 / 3):, :, :]
    L = lum(ground)
    p95, p50, p10 = np.percentile(L, 95), np.percentile(L, 50), np.percentile(L, 10)
    spread = np.log2(max(p95, 1e-6) / max(p10, 1e-6))
    dark = float((L < 0.005).mean())
    mean = ground.reshape(-1, 3).mean(0)
    return {"spread_stops": round(float(spread), 2), "p95": round(float(p95), 4), "p50": round(float(p50), 4),
            "p10": round(float(p10), 5), "near_black_share": round(dark, 3),
            "mean_rgb": [int(v) for v in mean]}


def selftest():
    ok = bad = 0

    def check(what, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("measure_night_pools selftest FAIL " + what)
    import os
    import tempfile
    d = tempfile.mkdtemp()
    flat = np.full((300, 400, 3), (150, 90, 30), dtype=np.uint8)
    Image.fromarray(flat).save(os.path.join(d, "flat.png"))
    pools = np.zeros((300, 400, 3), dtype=np.uint8)
    yy, xx = np.mgrid[0:300, 0:400]
    for cx in (60, 200, 340):
        r = np.hypot(xx - cx, yy - 280)
        v = np.clip(220 * np.exp(-r / 25.0), 0, 255)
        pools[..., 0] = np.maximum(pools[..., 0], v.astype(np.uint8))
        pools[..., 1] = np.maximum(pools[..., 1], (v * 0.6).astype(np.uint8))
    Image.fromarray(pools).save(os.path.join(d, "pools.png"))
    mf, mp = measure(os.path.join(d, "flat.png")), measure(os.path.join(d, "pools.png"))
    check("a flat wash has no spread", mf["spread_stops"] < 0.1)
    check("pools with dark between spread over four stops", mp["spread_stops"] > 4.0)
    print("measure_night_pools selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    for p in sys.argv[1:]:
        print(p, measure(p))
