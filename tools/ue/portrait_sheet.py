"""One sheet per cast member: the close-up and the mid-shot from -LedgerPortrait, beside the KCD2 people frame.

    python tools/ue/portrait_sheet.py [label]     # after a -LedgerPortrait run
    python tools/ue/portrait_sheet.py --selftest

WHY, 24 September. Jafar: "Lena, Sam and Rocco, each in a close-up and a
mid-shot in the street, in daylight, beside the KCD2 people frame." The KCD2
frame is a comparison reference only (production/reference/, never shipped):
its townsfolk are small, so the sheet shows the part of it where they stand,
enlarged, at the height of the two shots.
"""
import os
import sys

WHO = ("lena", "sam", "rocco")
# THE PEOPLE IN THE FOUNTAIN FRAME: the man in the orange coat, the man in
# green and the monk, bottom left (x0, y0, x1, y1 in its 1650x825 pixels).
KCD2 = os.path.join("production", "reference", "kcd2-town-fountain.jpg")
KCD2_PEOPLE = (120, 480, 720, 825)
SHOT_H = 540


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def out_path(root, who, label):
    return os.path.join(root, "production", "d1-probe", "portraits", "%s-%s.jpg" % (who, label))


def make(label):
    from PIL import Image, ImageDraw, ImageFont
    root = repo_root()
    ref = Image.open(os.path.join(root, KCD2)).convert("RGB").crop(KCD2_PEOPLE)
    ref = ref.resize((round(ref.width * SHOT_H / ref.height), SHOT_H), Image.LANCZOS)
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
    made = []
    for who in WHO:
        shots = []
        for kind in ("close", "mid"):
            p = os.path.join(root, "ue-probe", "ue-portrait-%s-%s.png" % (who, kind))
            if not os.path.exists(p):
                print("portrait_sheet: missing " + p)
                return 1
            im = Image.open(p).convert("RGB")
            shots.append(im.resize((round(im.width * SHOT_H / im.height), SHOT_H), Image.LANCZOS))
        bar = 34
        w = sum(s.width for s in shots) + ref.width + 16
        sheet = Image.new("RGB", (w, SHOT_H + bar), (18, 18, 18))
        d = ImageDraw.Draw(sheet)
        x = 0
        captions = ("%s, close" % who.capitalize(), "%s, mid" % who.capitalize(), "KCD2, the people frame (reference)")
        for im, cap in zip(shots + [ref], captions):
            if im is ref:
                x += 16
            sheet.paste(im, (x, bar))
            d.text((x + 8, 6), cap, fill=(235, 235, 235), font=font)
            x += im.width
        out = out_path(root, who, label)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sheet.save(out, quality=86)
        made.append(out)
    print("portrait_sheet: made %d sheets: %s" % (len(made), ", ".join(os.path.basename(m) for m in made)))
    return 0


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("portrait_sheet selftest FAIL " + name)
    check("three of the cast", WHO == ("lena", "sam", "rocco"))
    check("the crop is inside the 1650x825 frame", 0 <= KCD2_PEOPLE[0] < KCD2_PEOPLE[2] <= 1650 and 0 <= KCD2_PEOPLE[1] < KCD2_PEOPLE[3] <= 825)
    check("the sheets land under the probe's portraits", out_path("r", "lena", "x").replace("\\", "/") == "r/production/d1-probe/portraits/lena-x.jpg")
    check("the reference is read from the reference folder", KCD2.replace("\\", "/").startswith("production/reference/"))
    print("portrait_sheet selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(make(sys.argv[1] if len(sys.argv) > 1 else "latest"))
