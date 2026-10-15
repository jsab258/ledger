"""A second reader for the models' base-colour maps (15 Oct 2026, the ironmonger's try 2 close review, narrow 1: "Polybubble" survived outside every blanking box, and INV-07 reads only the boxes).
Run under the OCR venv (/home/user/.ocrenv: rapidocr-onnxruntime, a tool of the check only, nothing of it is shipped): python ocr_words.py out.json image [image ...]
Each image is read three ways (as it is; twice the size with its contrast stretched; its local contrast lifted, which is what lets a moulded or embossed word show), and every line the reader finds is written
with its box in the image's own pixels, so that someone can look at the place at 100 per cent."""
import json
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps
from rapidocr_onnxruntime import RapidOCR


def variants(im):
    yield "raw", im, 1.0
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1).resize((im.width * 2, im.height * 2), Image.LANCZOS)
    yield "x2 contrast", g.convert("RGB"), 2.0
    a = np.asarray(im.convert("L")).astype(np.float32)
    blur = np.asarray(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(12))).astype(np.float32)
    loc = np.clip(128 + (a - blur) * 4.0, 0, 255).astype(np.uint8)
    yield "local contrast", Image.fromarray(loc).convert("RGB"), 1.0


def main(argv):
    out, paths = argv[0], argv[1:]
    ocr = RapidOCR()
    res = {}
    for p in paths:
        im = Image.open(p).convert("RGB")
        found = []
        for name, v, scale in variants(im):
            r, _ = ocr(np.asarray(v))
            for box, text, conf in (r or []):
                xs = [pt[0] for pt in box]
                ys = [pt[1] for pt in box]
                found.append({"text": text, "conf": round(float(conf), 3), "box": [int(min(xs) / scale), int(min(ys) / scale), int(max(xs) / scale), int(max(ys) / scale)], "variant": name})
        res[p] = found
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
