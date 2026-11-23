"""READ THE CHASE'S DISTANCE MARKER IN A DRILL'S HOLD GRABS (n23-1, Sleeping Dogs, 23 Nov 2026).

    python tools/drills/marker_read.py F:/LedgerTools/tmp/drills/<run folder> <out folder>

Finds the small green shield the game draws over the target (its distance in whole metres above it)
in every walk4/run4 grab, by colour (green well above red and blue, not the teal of the market's
nets) and shape (a 6-20 px blob, mostly filled), and tiles the number with each grab's time from
times.jsonl into <run>-<hold>-marker.jpg, read by eye. Speed = the metres between the first and last
change of the readout over the time between them, while the target stands (SLEEPING-DOGS-DRILL-2026-11-23.md).
Method researched: HUD-ICON-READING-NOTES-2026-11-23.md (fixed colour and shape, checked by eye on sheets).
Reads frames only; never touches the game.
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
d = sys.argv[1]; out = sys.argv[2]
rows = [json.loads(l) for l in open(os.path.join(d, 'times.jsonl'))]
def find(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    m = (G - R > 50) & (G - B > 30) & (G > 105) & (G < 215)
    lab, n = ndimage.label(m)
    best = None
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        size = (lab[sl] == i).sum()
        if 6 <= w <= 20 and 6 <= h <= 20 and size >= 25 and size / (w * h) > 0.45:
            if best is None or size > best[0]:
                best = (size, (sl[1].start + sl[1].stop) // 2, sl[0].start)
    return best
for hold in ('walk4', 'run4'):
    r = [x for x in rows if x.get('hold') == hold]; t0 = r[0]['t0']
    files = sorted(f for f in os.listdir(d) if f.startswith(hold + '-'))
    crops = []; found = 0
    for k, f in enumerate(files):
        im = Image.open(os.path.join(d, f)).convert('RGB'); b = find(np.asarray(im).astype(int))
        c = Image.new('RGB', (160, 62))
        if b:
            found += 1; x, y = b[1], b[2]
            c.paste(im.crop((x - 40, y - 20, x + 40, y + 11)).resize((160, 62)), (0, 0))
        ImageDraw.Draw(c).text((2, 50), '%d %.2f' % (k + 1, (r[k]['t0'] + r[k]['t1']) / 2 - t0), fill='yellow')
        crops.append(c)
    cols = 10; rn = (len(crops) + cols - 1) // cols
    sh = Image.new('RGB', (160 * cols, 62 * rn))
    for i, c in enumerate(crops): sh.paste(c, ((i % cols) * 160, (i // cols) * 62))
    sh.save(os.path.join(out, '%s-%s-marker.jpg' % (os.path.basename(d)[-4:], hold)), quality=92); print(hold, found, len(files))

