"""A reduced preview of a picture, for git, so outside reviewers can see the work.

    python tools/make_preview.py SOURCE NAME [--date 2026-10-03]   # writes production/previews/NAME-DATE.jpg
    python tools/make_preview.py --selftest

WHY, 3 October, evening (Jafar): "for every proof-view step and every picture on my pages, a
reduced preview goes into git, about 1600 pixels wide, JPEG, under 500 KB each, under
production/previews/, named by step and date. Full-size pictures stay on the drive." The one
exception to "only text and small files go into git" (tools/git-size-guard.py lets these through
and nothing else of their kind). Our own frames only: other games' screenshots never go into the
repository, so a comparison sheet with KCD2 frames is never previewed.

NAME is the step and what it shows, e.g. proof-2.2-atmosphere-sky; the date is the day the
picture was made. The width is 1600 (a narrower source keeps its own; nothing is enlarged); the
JPEG quality steps down from 90 until the file is under 500 KB.
"""
import argparse
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "production", "previews")
WIDTH = 1600
MAX_BYTES = 500_000
NAME_RULE = re.compile(r"^[a-z0-9][a-z0-9.\-]*$")


def encode(im, width=WIDTH, max_bytes=MAX_BYTES):
    """The picture at WIDTH as JPEG bytes under max_bytes, and the quality used."""
    from PIL import Image
    im = im.convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    for q in range(90, 39, -5):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() < max_bytes:
            return buf.getvalue(), q, im.size
    raise ValueError("no quality from 90 to 40 brings it under %d bytes" % max_bytes)


def make(source, name, date):
    from PIL import Image
    if not NAME_RULE.match(name):
        raise ValueError("a name is lower case, digits, dots and dashes: %r" % name)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        raise ValueError("a date is YYYY-MM-DD: %r" % date)
    data, q, size = encode(Image.open(source))
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "%s-%s.jpg" % (name, date))
    with open(out, "wb") as f:
        f.write(data)
    return out, len(data), q, size


def selftest():
    from PIL import Image
    passed = failed = 0

    def check(what, ok):
        nonlocal passed, failed
        passed += bool(ok)
        failed += not ok
        print(("ok    " if ok else "FAIL  ") + what)

    noisy = Image.effect_noise((2560, 1440), 90).convert("RGB")
    data, q, size = encode(noisy)
    check("a 2560-wide frame comes out 1600 wide, its height in proportion", size == (1600, 900))
    check("under 500 KB even when the picture is all noise (quality %d)" % q, len(data) < MAX_BYTES)
    small = Image.new("RGB", (800, 450), (120, 90, 70))
    check("a narrower picture is never enlarged", encode(small)[2] == (800, 450))
    check("names are the step and what it shows, lower case", NAME_RULE.match("proof-2.1-composition-try1") and not NAME_RULE.match("Proof 2.1"))
    print("make_preview selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if argv and argv[0] == "--selftest":
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("name")
    ap.add_argument("--date", required=True)
    a = ap.parse_args(argv)
    out, n, q, size = make(a.source, a.name, a.date)
    print("%s %dx%d %d KB (quality %d)" % (os.path.relpath(out, REPO).replace("\\", "/"), size[0], size[1], n // 1000, q))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
