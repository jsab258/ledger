"""One garment's colour changed inside a person's glb, the folds kept.

    python tools/art-recipes/person_recolour.py --selftest
    python tools/art-recipes/person_recolour.py [--preview out.jpg]

WHY IT EXISTS, 6 November. A Mixamo body's clothes are painted into one texture
with no tint to set. Martha's beige trousers matched her skin, so three of four
fresh reviewers read her as bare from the waist down, in frames his note of
4 November says must show plain clothes.

WHAT IT DOES: flood-fills the garment's island in the texture from a seed, keeps
its light and shade as a ratio to the island's median, and multiplies a target
colour by that. The new picture is appended to the glb's buffer and its buffer
view pointed there; nothing else in the file changes. The result goes to the game
inputs under the same path, since the push guard refuses a glb over 1 MB;
tools/ue/import_people.py takes that copy whenever it exists.
"""
import io
import json
import os
import struct
import sys
from collections import deque

from PIL import Image, ImageFilter

GAME_INPUTS = os.environ.get("LEDGER_GAME_INPUTS", r"F:\LedgerTools\game-inputs")
REL = os.path.join("production", "assets", "people")
# stem, image name, flood seeds (x, y in the 1024 texture), tolerance, target colour
JOBS = [("martha-idle", "Ch27_1001_Diffuse", [(300, 700), (560, 950), (640, 950), (420, 585), (270, 885), (255, 490), (465, 985), (605, 990)], 16, (46, 46, 52))]
#: Above this row the island's colour runs on into her skin; the seams are closed over, this wide.
TOP_ROW, CLOSE_PX = 452, 13


def read_glb(data):
    json_len = struct.unpack("<I", data[12:16])[0]
    doc = json.loads(data[20:20 + json_len])
    return doc, data[20 + json_len + 8:]


def write_glb(doc, binary):
    text = json.dumps(doc, separators=(",", ":")).encode("utf-8")
    text += b" " * (-len(text) % 4)
    binary += b"\0" * (-len(binary) % 4)
    total = 12 + 8 + len(text) + 8 + len(binary)
    return (struct.pack("<III", 0x46546C67, 2, total)
            + struct.pack("<I", len(text)) + b"JSON" + text
            + struct.pack("<I", len(binary)) + b"BIN\0" + binary)


def flood(px, size, seeds, tol):
    """The pixels connected to a seed within tol of that seed's colour, each channel."""
    w, h = size
    seen = bytearray(w * h)
    out = []
    for sx, sy in seeds:
        ref = px[sx, sy]
        todo = deque([(sx, sy)])
        while todo:
            x, y = todo.popleft()
            if not (0 <= x < w and 0 <= y < h) or seen[y * w + x]:
                continue
            c = px[x, y]
            if max(abs(c[i] - ref[i]) for i in range(3)) > tol:
                continue
            seen[y * w + x] = 1
            out.append((x, y))
            todo.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return out


def recolour(im, seeds, tol, target, top_row=0, close_px=1):
    im = im.convert("RGB")
    px = im.load()
    w, h = im.size
    mask = Image.new("L", im.size, 0)
    mp = mask.load()
    for x, y in flood(px, im.size, seeds, tol):
        if y >= top_row:
            mp[x, y] = 255
    # Closing the mask takes in the seams and folds a flood stops at.
    mask = mask.filter(ImageFilter.MaxFilter(close_px)).filter(ImageFilter.MinFilter(close_px))
    mp = mask.load()
    cells = [(x, y) for y in range(top_row, h) for x in range(w) if mp[x, y]]
    lums = sorted(sum(px[x, y]) / 3.0 for x, y in cells)
    mid = lums[len(lums) // 2] or 1.0
    for x, y in cells:
        ratio = min(1.6, (sum(px[x, y]) / 3.0) / mid)
        px[x, y] = tuple(min(255, int(t * ratio)) for t in target)
    return im, len(cells)


def run(root, preview=None):
    for stem, name, seeds, tol, target in JOBS:
        src = os.path.join(root, REL, stem + ".glb")
        with open(src, "rb") as f:
            doc, binary = read_glb(f.read())
        image = next(i for i in doc["images"] if i.get("name") == name)
        view = doc["bufferViews"][image["bufferView"]]
        start = view.get("byteOffset", 0)
        im = Image.open(io.BytesIO(binary[start:start + view["byteLength"]]))
        new, count = recolour(im, seeds, tol, target, TOP_ROW, CLOSE_PX)
        if preview:
            new.save(preview, quality=90)
        buf = io.BytesIO()
        new.save(buf, "JPEG", quality=92)
        binary += b"\0" * (-len(binary) % 4)
        view["byteOffset"] = len(binary)
        view["byteLength"] = buf.tell()
        binary += buf.getvalue()
        doc["buffers"][0]["byteLength"] = len(binary) + (-len(binary) % 4)
        dest = os.path.join(GAME_INPUTS, REL, stem + ".glb")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(write_glb(doc, binary))
        print("personRecolour %s %s cells=%d of %d out=%s" % (stem, name, count, new.size[0] * new.size[1], dest))


def selftest():
    im = Image.new("RGB", (8, 8), (200, 180, 160))
    px = im.load()
    for y in range(8):
        px[4, y] = (10, 10, 90)
    new, count = recolour(im, [(1, 1)], 30, (40, 40, 40))
    good = count == 32 and new.getpixel((1, 1)) == (40, 40, 40) and new.getpixel((4, 1)) == (10, 10, 90)
    doc, binary = read_glb(write_glb({"a": 1}, b"abc"))
    good = good and doc == {"a": 1} and binary[:3] == b"abc"
    print("person_recolour selftest: %s" % ("passed" if good else "FAILED"))
    return 0 if good else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    run(here, sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None)
