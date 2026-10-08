"""The road against the Hook sheet's values, per view (his order of 8 October, 2c; the lab's targets,
production/lab/ROAD-NOTES.md section 4): the hook's near lane 152, the reverse's near centre 164 and
middle 183 (sRGB means), each to be within 12 levels. Boxes on the 2560x1440 frames: the hook's near
lane as the lab placed it (x 0.18-0.32, y 0.80-0.92); the reverse's as its fresh reviewer measured
(the road's centre, x 450-1150: its near part y 1150-1440, its middle y 900-1100, x 600-1000).
python measure_road.py HOOK_DAY.png REVERSE_DAY.png"""
import sys
from PIL import Image

TARGETS = (("hook", "near lane", (461, 1152, 819, 1325), 152),
           ("reverse", "near centre", (450, 1150, 1150, 1440), 164),
           ("reverse", "middle", (600, 900, 1000, 1100), 183))


def mean_luma(im, box):
    px = list(im.convert("L").crop(box).getdata())
    return sum(px) / len(px)


if __name__ == "__main__":
    frames = {"hook": Image.open(sys.argv[1]), "reverse": Image.open(sys.argv[2])}
    ok = True
    for view, name, box, want in TARGETS:
        got = mean_luma(frames[view], box)
        good = abs(got - want) <= 12
        ok &= good
        print("%-8s %-12s %5.1f  sheet %d  %+6.1f  %s" % (view, name, got, want, got - want, "ok" if good else "OUT"))
    print("ROAD", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
