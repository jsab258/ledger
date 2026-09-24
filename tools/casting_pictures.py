#!/usr/bin/env python3
"""Place the image lane's casting portraits beside their sheets, as JPEGs.

    python tools/casting_pictures.py <folder of PNGs from imagegen>

Each <slug>-<front|profile|full>.png becomes
production/casting/<slug>/<front|profile|full>.jpg (quality 88, the image
lane's own size), which is what SHEET.md and the approval page show. A PNG
is 1.6 MB; the JPEG about a tenth, which matters in a public repository.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(src):
    from PIL import Image
    n = 0
    for f in sorted(os.listdir(src)):
        m = re.match(r"^([a-z-]+)-(front|profile|full)\.png$", f)
        if not m:
            continue
        slug, shot = m.groups()
        dst_dir = os.path.join(REPO, "production", "casting", slug)
        if not os.path.isdir(dst_dir):
            continue
        Image.open(os.path.join(src, f)).convert("RGB").save(os.path.join(dst_dir, shot + ".jpg"), quality=88, optimize=True)
        n += 1
    print("casting_pictures: placed %d pictures" % n)
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
