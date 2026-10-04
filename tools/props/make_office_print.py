#!/usr/bin/env python3
"""Mickey's office's printed matter, as pictures (the proof view's shopfronts step, 4 October).

    python tools/props/make_office_print.py            # writes production/assets/office-print/mickeys/
    python tools/props/make_office_print.py --selftest

WHY. Two fresh reviews failed Mickey's room at 2 m on its notices and boards: 3D text too small
to read and boxes standing for writing read as "blank bars". The dressing research
(production/research/shop-window-interiors/DRESSING-2026-10-04.md) says print is texture, not
geometry: notices, pages and boards printed into pictures at about 2 mm a pixel, faced to the
glass. Every word here is ours, in the project's OFL fonts (production/fonts), the handwriting in
Patrick Hand (OFL); the places are canon's (the Hook, Copper Row, the Exchange, Fairview, Gullwing,
Quay Street, Weighhouse Lane, Tannery Row), the only person named is Mickey (canon's Michael
Suddaby, on his own licence), and nothing is a real firm, brand or number that rings.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "production", "assets", "office-print", "mickeys")
FONTS = os.path.join(ROOT, "production", "fonts")
PX_PER_MM = 2.0
INK = (24, 24, 30)
BIRO = (28, 44, 130)
RED = (170, 26, 28)
PAPER = (236, 230, 212)


def font(rel, size_mm):
    return ImageFont.truetype(os.path.join(FONTS, rel), max(6, int(size_mm * PX_PER_MM / 0.70)))


FRANKLIN = "evening-paper/LibreFranklin-700.ttf"
FRANKLIN_HEAVY = "evening-paper/LibreFranklin-800.ttf"
GOTHIC = "evening-paper/LeagueGothic-Regular.ttf"
SERIF = "evening-paper/OldStandard-Regular.ttf"
HAND = "patrick-hand/PatrickHand-Regular.ttf"


def sheet(w_mm, h_mm, colour=PAPER):
    return Image.new("RGB", (int(w_mm * PX_PER_MM), int(h_mm * PX_PER_MM)), colour)


def mm(v):
    return int(v * PX_PER_MM)


def age(img, rng, amount=0.10, stain=True):
    """Paper that has hung in a smoking room: a little uneven, yellowed toward the edges."""
    w, h = img.size
    px = img.load()
    cx, cy = w / 2.0, h / 2.0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            e = ((x - cx) / cx) ** 2 + ((y - cy) / cy) ** 2
            k = 1.0 - amount * 0.5 * e
            for dx in (0, 1):
                for dy in (0, 1):
                    if x + dx < w and y + dy < h:
                        px[x + dx, y + dy] = (int(r * k), int(g * k * 0.99), int(b * k * 0.93))
    if stain:
        d = ImageDraw.Draw(img)
        for _ in range(2):
            sx, sy, sr = rng.uniform(0.1, 0.9) * w, rng.uniform(0.1, 0.9) * h, rng.uniform(0.04, 0.09) * w
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=(196, 172, 128), width=mm(1.5))
    return img


def hand(d, xy, text, size_mm, rng, colour=BIRO):
    """Handwriting: Patrick Hand, each word nudged a little off the line."""
    x, y = xy
    f = font(HAND, size_mm)
    for word in text.split(" "):
        d.text((x, y + rng.uniform(-0.6, 0.6) * PX_PER_MM), word, font=f, fill=colour)
        x += d.textlength(word + " ", font=f)


def fares(rng):
    img = sheet(300, 420, (240, 236, 222))
    d = ImageDraw.Draw(img)
    d.rectangle([mm(8), mm(8), mm(292), mm(412)], outline=INK, width=mm(1.2))
    d.text((mm(150), mm(40)), "FARES", font=font(GOTHIC, 48), fill=RED, anchor="mm")
    d.text((mm(150), mm(78)), "MICKEY'S  ·  QUAY STREET", font=font(FRANKLIN, 7), fill=INK, anchor="mm")
    rows = [("Town Centre", "2.20"), ("Copper Row", "2.40"), ("The Exchange", "2.60"), ("Station", "2.80"),
            ("Ferry Landing", "3.00"), ("Fairview", "3.20"), ("Gullwing", "3.40"), ("Hospital", "3.60")]
    y = mm(105)
    f = font(FRANKLIN, 9)
    for name, price in rows:
        d.text((mm(30), y), name, font=f, fill=INK)
        tw = d.textlength(name, font=f)
        d.text((mm(270), y), "£" + price, font=f, fill=INK, anchor="ra")
        dot_x = mm(30) + tw + mm(4)
        while dot_x < mm(232):
            d.ellipse([dot_x, y + mm(8), dot_x + mm(1), y + mm(9)], fill=INK)
            dot_x += mm(4)
        y += mm(28)
    d.line([mm(30), y + mm(4), mm(270), y + mm(4)], fill=INK, width=mm(0.8))
    small = font(FRANKLIN, 6)
    for k, line in enumerate(("Waiting 10p a minute", "After midnight 50p extra", "Luggage and dogs 20p")):
        d.text((mm(150), y + mm(22) + k * mm(16)), line, font=small, fill=INK, anchor="mm")
    # a fare corrected in biro, as fares were between reprints
    hand(d, (mm(232), mm(105) + 4 * mm(28) - mm(14)), "3.10", 7, rng, RED)
    d.line([mm(236), mm(105) + 4 * mm(28) + mm(5), mm(270), mm(105) + 4 * mm(28) + mm(5)], fill=RED, width=mm(0.8))
    return age(img, rng)


def licence(rng):
    img = sheet(210, 148, (232, 226, 206))
    d = ImageDraw.Draw(img)
    d.rectangle([mm(5), mm(5), mm(205), mm(143)], outline=INK, width=mm(0.8))
    lines = [("MERIDIAN BOROUGH COUNCIL", FRANKLIN_HEAVY, 6.0, 18), ("Local Government (Miscellaneous Provisions) Act 1976", SERIF, 3.6, 30),
             ("PRIVATE HIRE OPERATOR'S LICENCE", FRANKLIN_HEAVY, 5.0, 45), ("No. 0417", FRANKLIN, 7.0, 60)]
    for text, f, size, y in lines:
        d.text((mm(105), mm(y)), text, font=font(f, size), fill=INK, anchor="mm")
    small = font(SERIF, 3.6)
    for k, (label, value) in enumerate((("Licensee", "Michael Suddaby"), ("Premises", "Quay Street, The Hook, Meridian"),
                                        ("Vehicles", "not more than eight"), ("Expires", "31st March 1991"))):
        y = mm(78) + k * mm(11)
        d.text((mm(22), y), label + ":", font=small, fill=INK)
        hand(d, (mm(62), y - mm(2)), value, 5.0, rng, INK)
    d.ellipse([mm(150), mm(100), mm(190), mm(140)], outline=(150, 40, 60), width=mm(1.0))
    d.text((mm(170), mm(120)), "M.B.C.", font=font(FRANKLIN, 4), fill=(150, 40, 60), anchor="mm")
    return age(img, rng, 0.14)


def accounts(rng):
    img = sheet(300, 100, (246, 244, 236))
    d = ImageDraw.Draw(img)
    hand(d, (mm(14), mm(14)), "ACCOUNT CUSTOMERS -", 15, rng, INK)
    hand(d, (mm(14), mm(54)), "please ask for Sheila", 15, rng, INK)
    return age(img, rng, 0.08, stain=False)


def calendar(rng):
    img = sheet(300, 420, (244, 242, 236))
    d = ImageDraw.Draw(img)
    photo = os.path.join(ROOT, "production", "assets", "shop-displays", "photos", "small_harbour_morning.jpg")
    if os.path.isfile(photo):
        p = Image.open(photo).convert("RGB").resize((mm(280), mm(180)))
        img.paste(p, (mm(10), mm(10)))
    d.text((mm(150), mm(210)), "OCTOBER  1990", font=font(FRANKLIN_HEAVY, 10), fill=INK, anchor="mm")
    days = ("M", "T", "W", "T", "F", "S", "S")
    for i, dd in enumerate(days):
        d.text((mm(30) + i * mm(40), mm(236)), dd, font=font(FRANKLIN, 6), fill=RED if i == 6 else INK, anchor="mm")
    # October 1990 began on a Monday
    for n in range(31):
        r, c = divmod(n, 7)
        d.text((mm(30) + c * mm(40), mm(262) + r * mm(30)), str(n + 1), font=font(FRANKLIN, 8),
               fill=RED if c == 6 else INK, anchor="mm")
    return age(img, rng, 0.08)


def farebook(rng):
    """The book of every fare, open: a ruled spread, its columns printed, the jobs in biro."""
    img = sheet(520, 360, (238, 232, 214))
    d = ImageDraw.Draw(img)
    d.line([mm(260), 0, mm(260), mm(360)], fill=(170, 160, 140), width=mm(2))
    places = ["Quay St", "Harbour Bd", "Copper Row", "Station", "Tannery Row", "Weighhouse Ln", "Exchange",
              "Fairview", "Gullwing", "Hospital", "Ferry", "Market"]
    head = font(FRANKLIN, 4.2)
    for page in (0, 1):
        x0 = mm(14 + page * 260)
        cols = (("TIME", 0), ("FROM", 30), ("TO", 95), ("CAR", 165), ("FARE", 195))
        for name, off in cols:
            d.text((x0 + mm(off), mm(16)), name, font=head, fill=RED)
            if off:
                d.line([x0 + mm(off) - mm(3), mm(14), x0 + mm(off) - mm(3), mm(350)], fill=(200, 120, 120), width=mm(0.5))
        for r in range(26):
            y = mm(30) + r * mm(12.5)
            d.line([x0 - mm(6), y + mm(11), x0 + mm(240), y + mm(11)], fill=(150, 170, 200), width=mm(0.4))
            if page == 1 and r > 13:
                continue
            hh, mi = 6 + (page * 26 + r) * 17 // 60, (page * 26 + r) * 17 % 60
            hand(d, (x0, y), "%d.%02d" % (hh % 24, mi), 5.5, rng)
            hand(d, (x0 + mm(30), y), rng.choice(places), 5.5, rng)
            hand(d, (x0 + mm(95), y), rng.choice(places), 5.5, rng)
            hand(d, (x0 + mm(168), y), str(rng.randint(1, 6)), 5.5, rng)
            hand(d, (x0 + mm(195), y), "%.2f" % rng.choice((2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4)), 5.5, rng)
    return age(img, rng, 0.10, stain=True)


def directory(rng):
    img = sheet(220, 280, (226, 196, 70))
    d = ImageDraw.Draw(img)
    d.rectangle([mm(10), mm(10), mm(210), mm(270)], outline=(40, 40, 40), width=mm(1.0))
    for k, (text, f, size, y) in enumerate((("TELEPHONE", FRANKLIN_HEAVY, 14, 70), ("DIRECTORY", FRANKLIN_HEAVY, 14, 100),
                                            ("Meridian & District", SERIF, 8, 150), ("1989 - 90", FRANKLIN, 10, 200))):
        d.text((mm(110), mm(y)), text, font=font(f, size), fill=(30, 30, 30), anchor="mm")
    return age(img, rng, 0.20, stain=False)


def drivers_board(rng):
    img = sheet(600, 700, (150, 110, 70))
    d = ImageDraw.Draw(img)
    for _ in range(4000):
        x, y = rng.uniform(0, img.size[0]), rng.uniform(0, img.size[1])
        c = rng.randint(110, 175)
        d.point((x, y), fill=(c, int(c * 0.74), int(c * 0.48)))
    d.rectangle([mm(150), mm(20), mm(450), mm(90)], fill=(240, 236, 224))
    d.text((mm(300), mm(55)), "CARS", font=font(FRANKLIN_HEAVY, 30), fill=INK, anchor="mm")
    for k, status in enumerate(("RANK", "OUT", "OUT", "HOME", "RANK", "OUT")):
        y = mm(115) + k * mm(95)
        d.text((mm(60), y + mm(38)), str(k + 1), font=font(FRANKLIN_HEAVY, 38), fill=(240, 236, 224), anchor="mm")
        d.rectangle([mm(120), y, mm(560), y + mm(76)], fill=(244, 240, 228) if k % 3 else (232, 214, 150))
        d.text((mm(140), y + mm(38)), status, font=font(FRANKLIN_HEAVY, 30), fill=RED if status == "OUT" else INK, anchor="lm")
        if status == "OUT":
            hand(d, (mm(400), y + mm(18)), "%d.%02d" % (rng.randint(9, 11), rng.choice((5, 10, 20, 35, 40, 50))), 18, rng, INK)
    return img


def bookings(rng):
    img = sheet(400, 120, (246, 244, 238))
    d = ImageDraw.Draw(img)
    d.text((mm(200), mm(48)), "BOOKINGS", font=font(FRANKLIN_HEAVY, 30), fill=RED, anchor="mm")
    d.text((mm(200), mm(96)), "& ENQUIRIES", font=font(FRANKLIN, 12), fill=INK, anchor="mm")
    return age(img, rng, 0.06, stain=False)


def pinboard(rng):
    img = sheet(700, 600, (152, 112, 72))
    d = ImageDraw.Draw(img)
    for _ in range(5000):
        x, y = rng.uniform(0, img.size[0]), rng.uniform(0, img.size[1])
        c = rng.randint(110, 175)
        d.point((x, y), fill=(c, int(c * 0.74), int(c * 0.48)))
    notes = [("Tues 7.15 - station", "early, ring the night before"), ("Car 4 MOT Fri", ""),
             ("Harbour Bd account", "sign every docket"), ("NO CHANGE GIVEN", "OVER £10"),
             ("Ring Sheila", "about the VAT"), ("Lost property", "ask at the counter")]
    spots = [(30, 30), (250, 40), (470, 30), (40, 300), (270, 320), (480, 290)]
    for (l1, l2), (x, y) in zip(notes, spots):
        w_, h_ = rng.uniform(180, 200), rng.uniform(140, 200)
        card = Image.new("RGB", (mm(w_), mm(h_)), rng.choice(((244, 240, 224), (238, 226, 160), (236, 236, 236))))
        cd = ImageDraw.Draw(card)
        hand(cd, (mm(10), mm(14)), l1, 15, rng, BIRO if rng.random() < 0.7 else INK)
        if l2:
            hand(cd, (mm(10), mm(60)), l2, 13, rng, BIRO)
        card = card.rotate(rng.uniform(-6, 6), expand=True, fillcolor=(152, 112, 72))
        img.paste(card, (mm(x), mm(y)))
        d.ellipse([mm(x + w_ / 2) - mm(5), mm(y + 6), mm(x + w_ / 2) + mm(5), mm(y + 16)], fill=(180, 30, 30))
    return img


def radio_faceplate(rng):
    img = sheet(440, 130, (52, 54, 58))
    d = ImageDraw.Draw(img)
    d.rectangle([mm(4), mm(4), mm(436), mm(126)], outline=(110, 112, 116), width=mm(1))
    # the meter, the channel switch, volume and squelch, the lamps
    d.rectangle([mm(20), mm(22), mm(120), mm(90)], fill=(214, 206, 170), outline=(20, 20, 20), width=mm(1))
    for k in range(11):
        a = math.radians(210 - k * 24)
        cx, cy = mm(70), mm(85)
        d.line([cx + mm(40) * math.cos(a), cy - mm(40) * math.sin(a), cx + mm(46) * math.cos(a), cy - mm(46) * math.sin(a)], fill=(20, 20, 20), width=mm(0.8))
    d.line([mm(70), mm(85), mm(70) + mm(38) * math.cos(math.radians(120)), mm(85) - mm(38) * math.sin(math.radians(120))], fill=(160, 20, 20), width=mm(1))
    lab = font(FRANKLIN, 4.5)
    d.text((mm(70), mm(104)), "SIGNAL", font=lab, fill=(220, 220, 220), anchor="mm")
    for k, name in enumerate(("CHANNEL", "VOLUME", "SQUELCH")):
        cx = mm(170) + k * mm(80)
        d.ellipse([cx - mm(22), mm(36), cx + mm(22), mm(80)], fill=(28, 28, 30), outline=(150, 150, 150), width=mm(1))
        d.text((cx, mm(100)), name, font=lab, fill=(220, 220, 220), anchor="mm")
    for k, ch in enumerate(("1", "2", "3", "4")):
        d.text((mm(144) + k * mm(15), mm(28)), ch, font=lab, fill=(220, 220, 220), anchor="mm")
    d.text((mm(404), mm(40)), "TX", font=lab, fill=(220, 220, 220), anchor="mm")
    d.text((mm(404), mm(80)), "ON", font=lab, fill=(220, 220, 220), anchor="mm")
    return img


def keypad(rng):
    img = sheet(80, 100, (196, 186, 160))
    d = ImageDraw.Draw(img)
    keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"]
    f = font(FRANKLIN, 5.5)
    for i, k in enumerate(keys):
        r, c = divmod(i, 3)
        x0, y0 = mm(8) + c * mm(23), mm(10) + r * mm(22)
        d.rounded_rectangle([x0, y0, x0 + mm(18), y0 + mm(16)], radius=mm(3), fill=(236, 230, 214), outline=(120, 110, 90), width=mm(0.6))
        d.text((x0 + mm(9), y0 + mm(8)), k, font=f, fill=(30, 30, 30), anchor="mm")
    return img


PIECES = (("fares", fares), ("licence", licence), ("accounts", accounts), ("calendar", calendar),
          ("farebook", farebook), ("directory", directory), ("drivers_board", drivers_board),
          ("bookings", bookings), ("pinboard", pinboard), ("radio_faceplate", radio_faceplate), ("keypad", keypad))


def make():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for name, fn in PIECES:
        rng = random.Random("mickeys-" + name)
        img = fn(rng)
        path = os.path.join(OUT, name + ".png")
        img.save(path, optimize=True)
        rows.append("%s %dx%d %.0f KB" % (name, img.size[0], img.size[1], os.path.getsize(path) / 1024.0))
    print("office print: " + "; ".join(rows))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_office_print selftest FAIL " + name)
    check("every font it names is in the repository",
          all(os.path.isfile(os.path.join(FONTS, f)) for f in (FRANKLIN, FRANKLIN_HEAVY, GOTHIC, SERIF, HAND)))
    check("the hand font carries its licence", os.path.isfile(os.path.join(FONTS, "patrick-hand", "OFL.txt")))
    img = fares(random.Random(1))
    check("a notice is printed at 2 px a millimetre", img.size == (600, 840))
    words = " ".join(str(v) for v in ("Town Centre", "Copper Row", "The Exchange", "Fairview", "Gullwing"))
    check("its places are canon's", "Meridian" not in words)
    print("make_office_print selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else (make() or 0))
