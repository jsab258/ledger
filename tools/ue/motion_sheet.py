"""A motion film's pictures on one sheet, for looking and for the gate.

    python tools/ue/motion_sheet.py OUT.jpg DIR [DIR ...] [--frames 0,2,4,6] [--crop 0.3,0.0,0.7,1.0] [--width 640]

Each DIR is one view of the portrait tool's motion film (ue-motion-<who>-<take>[-v<turn>]/fNNNN.png),
one row per view; --frames picks the pictures (every one by default), --crop keeps
that part of each (fractions of width and height: left, top, right, bottom), and
--width sets each picture's width on the sheet. Rows are labelled with the view.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    opts = {"--frames": None, "--crop": "0,0,1,1", "--width": "640"}
    rest = []
    i = 0
    while i < len(argv):
        if argv[i] in opts:
            opts[argv[i]] = argv[i + 1]
            i += 2
        else:
            rest.append(argv[i])
            i += 1
    out, dirs = rest[0], rest[1:]
    crop = [float(x) for x in opts["--crop"].split(",")]
    w = int(opts["--width"])
    rows = []
    for d in dirs:
        files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        if opts["--frames"]:
            pick = [int(x) for x in opts["--frames"].split(",")]
            files = [files[k] for k in pick if k < len(files)]
        ims = []
        for f in files:
            im = Image.open(os.path.join(d, f)).convert("RGB")
            W, H = im.size
            im = im.crop((int(crop[0] * W), int(crop[1] * H), int(crop[2] * W), int(crop[3] * H)))
            ims.append(im.resize((w, round(im.height * w / im.width)), Image.LANCZOS))
        rows.append((os.path.basename(os.path.normpath(d)), ims))
    bar = 30
    h = max(im.height for _, ims in rows for im in ims)
    cols = max(len(ims) for _, ims in rows)
    sheet = Image.new("RGB", (cols * w, len(rows) * (h + bar)), (18, 18, 18))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    for r, (label, ims) in enumerate(rows):
        y = r * (h + bar)
        d.text((8, y + 5), label, fill=(235, 235, 235), font=font)
        for c, im in enumerate(ims):
            sheet.paste(im, (c * w, y + bar))
    sheet.save(out, quality=90)
    print("motion_sheet: %s, %d rows of up to %d" % (out, len(rows), cols))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
