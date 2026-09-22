#!/usr/bin/env python3
"""THE PAIR: our street beside the Hook sheet's own street, side by side.

    python3 tools/hook-pair.py --ours FRAME.png --out PAIR.png
    python3 tools/hook-pair.py --selftest

WHY THIS IS A TOOL AND NOT A HABIT. Stage 1's exit test is one a person
performs: a frame of the built street FROM THE SHEET'S OWN VIEWPOINT stands
beside the sheet, and when Jafar cannot say which way the gap runs, the budget
moves on. Ruled 2026-09-22: every step now ends with that pair, in DAYLIGHT as
the sheet is, and the dusk frame is a second, occasional check rather than the
working comparison. A comparison performed by eye from two files in two
directories is a comparison nobody repeats the same way twice.

WHICH SHEET, AND THE WEEK THIS GOT WRONG. Jafar's ruling of 9 September made
the IN-HOUSE Hook sheet the reference and retired Codex's. This tool was still
hard-wired to Codex's file, production/art/atlas-01/concepts/hook.png on the
art branch - and that file is STILL THERE, which is exactly why nothing ever
failed and why a week of comparisons went to the wrong picture in silence. A
reference that resolves is not the same as a reference that governs.

SO THERE IS NOW ONE PLACE A REFERENCE LIVES, production/reference/, and this
reads from it and from nowhere else. No branch, no git show, no second copy to
drift: if the sheet is not at that path the tool refuses and says so, which is
the behaviour that would have caught this on day one.

WHICH PANEL. The sheet is a poster: a title, a harbour panel, a STREET panel,
a strip of material swatches, a footer of object studies. The street panel is
the one our viewpoint is a viewpoint of, and it is found by measurement rather
than by typed pixel coordinates, because somebody may re-export the sheet at
another size. The paper is plain and every panel is not, so the bands are
found by scanning for rows that are entirely paper, and the street panel is
the LAST band tall enough to be a photograph.
"""
import os
import sys

#: THE ONE REFERENCE PATH. Relative to the repository root.
REFERENCE = os.path.join("production", "reference", "hook-sheet.png")

#: A band has to be at least this tall a fraction of the sheet to count as a
#: photograph rather than a swatch strip or a rule. MEASURED on the committed
#: sheet: its two photographs are 0.36 and 0.40 of the height and its swatch
#: strip is 0.11, so anything over a fifth is a panel and nothing else is.
PANEL_MIN_FRACTION = 0.20

#: How light the paper is, as a MINIMUM CHANNEL value, and it is DERIVED per
#: sheet rather than typed. The retired sheet was printed on near-white and
#: this one is on cream: measured at the four corners, the approved sheet's
#: paper is (249, 245, 231), so its minimum channel is 231 and the old typed
#: 235 would have called the whole page ink and found one band covering
#: everything. A constant measured off one sheet is a constant that silently
#: stops describing the next one, which is the same failure as the sheet path
#: itself. This is the fallback only, for a sheet whose corners cannot be read.
PAPER_MIN = 235

#: How far below the paper's own value a row has to sit to count as ink.
#: The gaps between this sheet's panels read as clean paper and the panels'
#: lightest rows (overcast sky) sit far below, so there is a wide margin here;
#: 12 is chosen to be well inside it and well clear of JPEG-style mottle.
PAPER_MARGIN = 12

#: A POSTER HAS PAPER IN ALL FOUR CORNERS AND A PHOTOGRAPH DOES NOT. From 22
#: September the approved reference is pass 4 of the regenerated sheet: ONE
#: full-frame street photograph, 2048 x 1088, with no margins and no panels -
#: generated as a panel precisely because a poster is what cost the old one
#: its resolution. The panel search above would find no paper in it and
#: refuse, which is correct for a poster and wrong for this.
#: SO THE MODE IS DECIDED BY MEASURING, AND PRINTED. The darkest corner of the
#: retired poster is cream paper at 231; the darkest corner of pass 4 is
#: brick. A sheet whose darkest corner is this light or lighter is a poster
#: and is searched for its street panel; anything darker IS the panel, whole.
#: Printed as sheetMode on every run, so which one happened is never silent.
POSTER_PAPER_MIN = 200


def sheet_mode(a):
    """'poster' when all four corners are paper, else 'panel'."""
    return "poster" if paper_value(a) >= POSTER_PAPER_MIN else "panel"


def panel_bands(grey_rows, height, paper_min=PAPER_MIN, min_fraction=PANEL_MIN_FRACTION):
    """[(y0, y1)] for every band of rows that is NOT paper and is tall enough.

    Pure, so the selftest can drive it with a made-up sheet: the row statistic
    comes in as a list of minimum channel values per row.
    """
    bands = []
    start = None
    for y, v in enumerate(grey_rows):
        ink = v < paper_min
        if ink and start is None:
            start = y
        elif not ink and start is not None:
            bands.append((start, y))
            start = None
    if start is not None:
        bands.append((start, len(grey_rows)))
    keep = [(a, b) for (a, b) in bands if (b - a) >= min_fraction * height]
    return keep


def street_band(bands):
    """(y0, y1) of the street panel, or None.

    THE LAST TALL BAND, and it is the last rather than the second because a
    sheet that gained a third photograph should still hand back the street:
    the street is the lowest photograph on this poster, above the swatches,
    and the swatch strip is already excluded by height.
    """
    return bands[-1] if bands else None


def ink_columns(col_values, paper_min=PAPER_MIN):
    """(x0, x1) of the inked part of a band, so the paper margin is trimmed."""
    xs = [x for x, v in enumerate(col_values) if v < paper_min]
    if not xs:
        return None
    return (xs[0], xs[-1] + 1)


def layout(sheet_wh, ours_wh, gutter=24, label=34):
    """(canvas_w, canvas_h, sheet_box, ours_box). Both panels to ONE HEIGHT,
    because two pictures at two sizes are not a comparison: the eye reads the
    difference in size before it reads anything about the buildings."""
    sw, sh = sheet_wh
    ow, oh = ours_wh
    h = max(sh, oh)
    sw2 = max(1, int(round(sw * h / float(sh))))
    ow2 = max(1, int(round(ow * h / float(oh))))
    return (sw2 + gutter + ow2, h + label,
            (0, label, sw2, label + h),
            (sw2 + gutter, label, sw2 + gutter + ow2, label + h))


# ---------------------------------------------------------------------------


def paper_value(a, pad=25):
    """The sheet's own paper, as a minimum channel value, from its corners.

    FOUR CORNERS AND THE LOWEST OF THEM. A sheet with one stained corner or
    one panel bled to an edge should not be able to talk this up into the
    picture; taking the darkest corner errs towards calling something paper,
    which loses a little margin at the edge of a panel and never swallows the
    page.
    """
    h, w = a.shape[0], a.shape[1]
    p = min(pad, h // 4, w // 4)
    corners = (a[:p, :p], a[:p, -p:], a[-p:, :p], a[-p:, -p:])
    return min(int(c.min()) for c in corners)


def _read_sheet(root, scratch):
    """The approved sheet, from the one place references live."""
    dest = os.path.join(root, REFERENCE)
    if not os.path.exists(dest) or os.path.getsize(dest) == 0:
        return None, "no-sheet-at-%s" % REFERENCE.replace(chr(92), "/")
    return dest, ""


def build(root, ours_path, out_path, scratch, caption=""):
    from PIL import Image, ImageDraw
    import numpy as np

    sheet_file, err = _read_sheet(root, scratch)
    if err:
        return err
    sheet = Image.open(sheet_file).convert("RGB")
    a = np.asarray(sheet).astype(int)
    mode = sheet_mode(a)
    paper = max(1, paper_value(a) - PAPER_MARGIN)
    if mode == "panel":
        x0, y0, x1, y1 = 0, 0, sheet.size[0], sheet.size[1]
    else:
        rows = a.min(axis=(1, 2)).tolist()
        bands = panel_bands(rows, sheet.size[1], paper_min=paper)
        band = street_band(bands)
        if band is None:
            return "no-panel-found-in-the-sheet/bands=%d" % len(bands)
        y0, y1 = band
        cols = a[y0:y1].min(axis=(0, 2)).tolist()
        span = ink_columns(cols, paper_min=paper)
        if span is None:
            return "the-street-panel-is-all-paper"
        x0, x1 = span
    panel = sheet.crop((x0, y0, x1, y1))

    ours = Image.open(ours_path).convert("RGB")
    cw, ch, sbox, obox = layout(panel.size, ours.size)
    canvas = Image.new("RGB", (cw, ch), (20, 20, 22))
    canvas.paste(panel.resize((sbox[2] - sbox[0], sbox[3] - sbox[1]), Image.LANCZOS),
                 (sbox[0], sbox[1]))
    canvas.paste(ours.resize((obox[2] - obox[0], obox[3] - obox[1]), Image.LANCZOS),
                 (obox[0], obox[1]))
    d = ImageDraw.Draw(canvas)
    d.text((6, 10), "THE HOOK SHEET, the bar", fill=(235, 235, 235))
    d.text((obox[0] + 6, 10), "OURS  " + caption, fill=(235, 235, 235))
    canvas.save(out_path)
    print("hookPair sheet=%s sheetMode=%s paper=%d sheetPanel=%d,%d..%d,%d ours=%dx%d "
          "out=%s bytes=%d"
          % (REFERENCE.replace(chr(92), "/"), mode, paper, x0, y0, x1, y1,
             ours.size[0], ours.size[1],
             os.path.basename(out_path), os.path.getsize(out_path)))
    return ""


def selftest():
    passed = failed = 0

    def check(name, ok, detail=""):
        nonlocal passed, failed
        if ok:
            passed += 1
        else:
            failed += 1
            print("hook-pair selftest FAIL %s: %s" % (name, detail))

    # A SYNTHETIC SHEET, the shape the real one is: paper, a tall panel, paper,
    # a tall panel, paper, a short strip, paper.
    rows = ([255] * 10 + [100] * 40 + [255] * 6 + [90] * 45
            + [255] * 6 + [120] * 12 + [255] * 10)
    h = len(rows)
    bands = panel_bands(rows, h)
    check("accept/the-two-photographs-are-found-and-the-swatch-strip-is-not",
          len(bands) == 2, "%d band(s): %s" % (len(bands), bands))
    check("accept/the-street-is-the-lower-of-the-two",
          street_band(bands) == (56, 101), str(street_band(bands)))
    # REJECTING: a sheet that is all paper has no panel, and says so rather
    # than handing back the whole page.
    check("reject/an-all-paper-sheet-yields-no-panel",
          panel_bands([255] * 120, 120) == [], "")
    check("reject/and-street_band-refuses-an-empty-list",
          street_band([]) is None)
    # REJECTING: a strip too short to be a photograph is not one.
    # THE FIXTURE HAS TO BE THE SHAPE OF A REAL SHEET, which the first one
    # was not: a 12-row strip in a 32-row page is more than a fifth of it and
    # IS a panel by this rule, so the check failed and was right to. The
    # swatch strip on the committed sheet is a ninth of its height.
    check("reject/a-short-strip-is-not-a-panel",
          panel_bands([255] * 50 + [100] * 12 + [255] * 58, 120) == [],
          str(panel_bands([255] * 50 + [100] * 12 + [255] * 58, 120)))
    check("accept/the-margin-is-trimmed-off-a-band",
          ink_columns([255, 255, 40, 40, 40, 255]) == (2, 5),
          str(ink_columns([255, 255, 40, 40, 40, 255])))
    check("reject/an-all-paper-band-has-no-columns",
          ink_columns([255, 255, 255]) is None)

    # THE PAPER IS DERIVED, and cream paper is the case that broke the typed
    # constant: the approved sheet's corners are (249, 245, 231), so its
    # minimum channel is 231 and a fixed 235 called the entire page ink.
    import numpy as _np
    cream = _np.full((80, 80, 3), 249, dtype=int)
    cream[:, :, 2] = 231
    # THE MODE, both ways: a page with paper corners is a poster, a street
    # photograph with brick in a corner is the panel itself.
    import numpy as _np
    poster = _np.full((100, 80, 3), 231)
    check("accept/paper-in-every-corner-is-a-poster", sheet_mode(poster) == "poster",
          sheet_mode(poster))
    photo = _np.full((100, 80, 3), 200)
    photo[:30, :30] = (110, 50, 40)          # brick in the top-left corner
    check("accept/a-photograph-with-brick-in-a-corner-is-the-panel",
          sheet_mode(photo) == "panel", sheet_mode(photo))
    check("accept/cream-paper-is-read-as-paper-not-ink", paper_value(cream) == 231,
          str(paper_value(cream)))
    stained = cream.copy()
    stained[:20, :20] = 180
    check("accept/the-darkest-corner-wins", paper_value(stained) == 180,
          str(paper_value(stained)))

    # AND THE ONE REFERENCE IS WHERE IT IS SUPPOSED TO BE. This is the check
    # whose absence cost a week: the old tool read a path that still resolved
    # and never said which sheet it had.
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    check("accept/the-approved-sheet-is-at-the-one-reference-path",
          os.path.exists(os.path.join(_root, REFERENCE)), REFERENCE)

    # BOTH PANELS COME OUT THE SAME HEIGHT, which is the whole point: two
    # pictures at two sizes are not a comparison.
    cw, ch, sbox, obox = layout((800, 400), (1400, 1100))
    check("accept/both-halves-are-one-height",
          (sbox[3] - sbox[1]) == (obox[3] - obox[1]) == 1100,
          "%d vs %d" % (sbox[3] - sbox[1], obox[3] - obox[1]))
    check("accept/the-sheet-half-keeps-its-aspect",
          abs((sbox[2] - sbox[0]) / 1100.0 - 800 / 400.0) < 0.01,
          "%d wide" % (sbox[2] - sbox[0]))
    check("accept/they-do-not-overlap", obox[0] >= sbox[2], "%d vs %d" % (obox[0], sbox[2]))
    check("accept/the-canvas-holds-both", cw >= obox[2] and ch >= obox[3])

    print("hook-pair selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 0 if failed == 0 else 4


def main(argv):
    args = argv[1:]
    out = {"ours": "", "out": "", "caption": "", "scratch": os.environ.get("TEMP", ".")}
    i = 0
    while i < len(args):
        if args[i] == "--selftest":
            return selftest()
        if args[i] in ("--ours", "--out", "--caption", "--scratch") and i + 1 < len(args):
            out[args[i][2:]] = args[i + 1]
            i += 2
            continue
        print("hook-pair refused: unknown-flag/%s nothing measured" % args[i])
        return 2
    if not out["ours"] or not out["out"]:
        print("hook-pair refused: --ours and --out are both required, nothing measured")
        return 2
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    err = build(root, out["ours"], out["out"], out["scratch"], out["caption"])
    if err:
        print("hook-pair refused: %s nothing measured" % err)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
