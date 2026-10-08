"""The night's nearest lamp pool, measured (his order of 8 October 11:10, 2b: clipped red back to 2% of
the pavement or less). The pavement under the lamp by Mickey's in the hook camera's night frame
(2560x1440): two boxes on the flags, clear of the tiled stallriser above them. Clipped: red >= 250.
python pool_clip.py FRAME [FRAME ...]"""
import sys
from PIL import Image

# the flags only: clear of the kerb's double yellow lines (they clip by themselves, painted) and of
# the tiled stallriser and the people (the first boxes, 11:25, caught the yellow lines)
BOXES = ((1400, 1080, 1550, 1125), (1570, 1150, 1900, 1240))

for p in sys.argv[1:]:
    im = Image.open(p).convert("RGB")
    n = clip = 0
    reds = []
    for b in BOXES:
        for r, g, bl in im.crop(b).getdata():
            n += 1
            reds.append(r)
            if r >= 250:
                clip += 1
    reds.sort()
    print("%s  clipped red %.1f%% of %d px, red p50 %d p95 %d" % (p, 100.0 * clip / n, n, reds[n // 2], reds[int(n * 0.95)]))
