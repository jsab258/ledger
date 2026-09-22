#!/usr/bin/env python3
"""The D1b vignette's DETERMINISTIC 2D lines. Pillow, no model, no network.

    python3 tools/props/make_vignette_2d.py            # write them
    python3 tools/props/make_vignette_2d.py --selftest # both outcomes

FIVE OF THE SEVEN 2D BILL-OF-MATERIALS LINES, and the routing decision for
each is written down in production/queue/025-step-4a-seven-images.md rather
than here. The short version: geometry and masks are measurements, and a
diffusion model cannot hold a constant band width, a seamless tile, or an
alpha channel that MEANS something. C11_lit_interior_card is depicted content
and went to the model; G7_graffiti_tags is blocked on canon minting crew names
and no name is invented here to unblock it.

  A5_double_yellow_lines   road_double_yellow.png    MANDATORY
  A9_puddle_mask           puddle_mask.png           MANDATORY
  E10_street_name_plate    plate_<name>.png x3       MANDATORY
  B4_gutter_water          gutter_water.png          DRESSING
  C12_net_curtain          net_curtain_a/b.png       DRESSING
  C6_fascia_lettering      fascia_mickeys_plain.png  the cab office's own board
  C6_letting_board         board_to_let.png          the empty unit's board

THE LAST TWO ARE LETTERING, and they are here rather than in the image lane
for the same reason the plates are: a sign is a measured board with a canon
word on it, and the diffusion model spells. Added 22 September, when the
shopfronts were reworked to the 1989 photographs - see make_fascia and
make_letting_board.

THE SCALE IS 1 MILLIMETRE PER PIXEL AND EVERY DIMENSION BELOW IS IN
MILLIMETRES, because the BOM states A5 in millimetres ("two 100 mm bands, gap
100 mm") and a texture whose scale is a guess cannot be placed against a kerb
whose scale is not. It is written into the manifest beside every file so the
scene generator binds metres rather than pixels.

A BLANK IMAGE MUST FAIL RATHER THAN PASS A FILE-EXISTS CHECK, and this file
does not write a second checker for that. tools/imagegen/imagegen.py carries
the one this project measured its bound on (BLANK_MAX_SPREAD = 2 over 255,
BLANK_MAX_STDEV = 1.0, both read off a printed series, both ANDed because
either alone eventually calls a real image blank), written for
leejet/stable-diffusion.cpp#1031 where Z-Image on Vulkan writes a blank PNG
and exits success. It is imported here and every file written is put through
it before this tool will exit 0. NOTE FOR THE READER OF THE BRIEF: that check
is NOT in tools/decal-ink.py, which measures ink, alpha coverage and mask
separation over the Unity decal sets and has no blankness verdict in it at
all; the brief said decal-ink and the code says imagegen, checked by grep on
2026-09-02.

CANON IS READ, NEVER INVENTED. The street plates take their names from the
"Streets minted:" line of canon.md at run time and this tool REFUSES any name
that is not on it, so the rule that canon outranks a builder is enforced by
the tool rather than remembered by a person. The plate's legend line is a
canon DISTRICT for the same reason: canon mints districts and does not mint a
council, so no council is printed.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "production" / "assets" / "vignette" / "decals2d"
CANON = ROOT / "canon.md"
FONT = ROOT / "ledger" / "Assets" / "Resources" / "LedgerSans.ttf"

MM = 1          # pixels per millimetre. See the docstring: not a guess.
SEED = 20260902  # every image below is a pure function of this number.


def _blank_check():
    """The project's ONE blankness instrument, imported rather than copied."""
    sys.path.insert(0, str(ROOT / "tools" / "imagegen"))
    import imagegen                                          # noqa: E402
    return imagegen


def canon_streets(canon=CANON):
    """The minted street names, out of canon.md, as canon writes them."""
    for line in canon.read_text(encoding="utf-8").splitlines():
        if "Streets minted:" in line:
            tail = line.split("Streets minted:", 1)[1].strip().rstrip(".")
            return [s.strip() for s in tail.split(",") if s.strip()]
    return []


def canon_districts(canon=CANON):
    """The seven districts, for the plate's legend line.

    PARSED BY THE PARENTHESES, NOT BY COMMAS, and the first version of this
    was wrong in exactly the way that matters: canon writes the districts as
    "the Hook (old port, the player's pub), Copper Row (market quarter), ..."
    over four wrapped lines, so splitting on commas returned "the player's
    pub)" as a district and would have printed it on a street plate. Every
    district in canon is "<name> (<gloss>)", so the name is what precedes the
    bracket. Canon mints districts and mints NO council, which is why a plate
    carries a district legend and no council line.
    """
    text = canon.read_text(encoding="utf-8")
    if "seven districts" not in text:
        return []
    tail = text.split("seven districts", 1)[1]
    tail = tail.split("\n- ", 1)[0].replace("\n", " ")
    names = [n.strip(" :,.") for n in re.findall(r"([A-Za-z'][A-Za-z' ]*?)\s*\(", tail)]
    return [n for n in names if 2 < len(n) < 24]


def canon_minted(canon=CANON):
    """The names canon.md's "Minted:" line mints, as canon writes them.

    THE LINE WRAPS AND CARRIES GLOSSES, "Mickey's (the minicab office; a pub
    until D19), the Tivoli (cinema), Meridian Harbour Board, Meridian\n
    Ferry. The brand bible still owes: ...", so the brackets go first, then
    the sentence ends at its full stop, then it is split on commas. A leading
    "the" is canon's grammar and not part of a name.
    """
    text = canon.read_text(encoding="utf-8")
    if "- Minted:" not in text:
        return []
    tail = text.split("- Minted:", 1)[1]
    tail = re.sub(r"\([^)]*\)", "", tail)
    tail = " ".join(tail.split())
    tail = tail.split(". ", 1)[0].rstrip(".")
    names = []
    for n in tail.split(","):
        n = n.strip()
        if n.lower().startswith("the "):
            n = n[4:]
        if n:
            names.append(n)
    return names


def _rng(tag):
    """A named stream per image, so adding one image cannot change another."""
    return np.random.default_rng(
        int(hashlib.sha256(f"{SEED}:{tag}".encode()).hexdigest()[:8], 16))


def _tileable_noise(w, h, cells, rng):
    """Value noise on a periodic lattice, so the edges meet. Returns 0..1."""
    g = rng.random((cells, cells))
    g = np.vstack([g, g[:1]])
    g = np.hstack([g, g[:, :1]])
    ys = np.linspace(0, cells, h, endpoint=False)
    xs = np.linspace(0, cells, w, endpoint=False)
    y0, x0 = np.floor(ys).astype(int), np.floor(xs).astype(int)
    fy, fx = (ys - y0)[:, None], (xs - x0)[None, :]
    sy, sx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
    a = g[np.ix_(y0, x0)]
    b = g[np.ix_(y0, (x0 + 1))]
    c = g[np.ix_((y0 + 1), x0)]
    d = g[np.ix_((y0 + 1), (x0 + 1))]
    return (a * (1 - sx) * (1 - sy) + b * sx * (1 - sy)
            + c * (1 - sx) * sy + d * sx * sy)


def _fbm(w, h, rng, octaves=4, cells=4):
    out, amp, total = np.zeros((h, w)), 1.0, 0.0
    for o in range(octaves):
        out += amp * _tileable_noise(w, h, cells * (2 ** o), rng)
        total += amp
        amp *= 0.5
    return out / total


# ---------------------------------------------------------------------------
# C6. The cab office's fascia: its name in plain capitals on its own paint.
# ---------------------------------------------------------------------------
#: THE BOARD IS THE FACE OF THE FASCIA THE RECIPE BUILDS, 5650 x 460 mm - the
#: 6.0 m band less half a pier each end, less 45 mm top and bottom - so the
#: image lands at 1 mm a pixel with no stretch.
FASCIA_BOARD_MM = (5650, 460)
#: THE PAINT AND THE LETTERING, sampled off the approved Hook sheet's own
#: MICKEY'S on 22 September: the fascia measures 66, 79, 90 sRGB, a slate
#: blue-grey, and its letters 178, 159, 116 at their brightest fifth - a dull
#: gold, which is what signwriter's gold looks like after a year of rain.
#: The sheet governs palette; that is all these two numbers are.
FASCIA_PAINT_SRGB = (66, 79, 90)
FASCIA_INK_SRGB = (196, 174, 122)
#: CAP HEIGHT, 240 mm on a 460 mm board: the sheet's letters fill a little
#: over half the fascia's height, and a sign is read from across the road.
FASCIA_CAP_MM = 240


def make_fascia(name, rng, minted=None):
    """A painted fascia with a canon name signwritten across it.

    PLAIN CAPITALS, NOT A PUB'S SERIF BOARD. The board this replaces was the
    image lane's, made against the retired sheet when Mickey's was still a
    pub, and it was a maroon signboard with gilt serifs and a border - the
    look of a pub. The approved sheet paints the name straight onto the
    fascia in plain sans capitals, which is what a minicab office's front
    looked like in 1989. The name is REFUSED unless canon mints it.
    """
    minted = canon_minted() if minted is None else minted
    if name not in minted:
        raise ValueError(
            f"'{name}' is not a name canon.md mints. Canon mints "
            f"{len(minted)}: {', '.join(minted) or 'none'}. A name is not "
            "invented here to unblock a picture; canon.md outranks this tool.")
    w, h = FASCIA_BOARD_MM[0] * MM, FASCIA_BOARD_MM[1] * MM
    img = Image.new("RGB", (w, h), FASCIA_PAINT_SRGB)
    d = ImageDraw.Draw(img)
    # PT Sans caps are 0.70 of the em, so the em is the cap height over that.
    font = ImageFont.truetype(str(FONT), int(FASCIA_CAP_MM * MM / 0.70))
    text = name.upper().replace("'", "\u2019")
    # A SIGNWRITER'S WEIGHT, drawn as a stroke of the same paint: the face
    # is PT Sans Regular and a fascia letter is heavier than a book's.
    d.text((w // 2, h // 2), text, font=font, fill=FASCIA_INK_SRGB,
           anchor="mm", stroke_width=5 * MM, stroke_fill=FASCIA_INK_SRGB)
    a = np.asarray(img).astype(np.float32) / 255.0
    dirt = _fbm(w, h, rng, octaves=5, cells=6)[..., None]
    # RAIN RUNS DOWN A FASCIA AND COLLECTS AT ITS FOOT, so the bottom is
    # a little darker than the top, on top of the ordinary mottle.
    fall = np.linspace(1.0, 0.86, h)[:, None, None]
    a = np.clip(a * (0.86 + 0.20 * dirt) * fall, 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8), "RGB")


# ---------------------------------------------------------------------------
# C6. The empty unit's letting board.
# ---------------------------------------------------------------------------
#: A FLAT BOARD FIXED TO THE FASCIA, 900 x 450 mm, which is R05's
#: "neighbouring letting board" on the 1989 Princes Avenue parade.
LETTING_BOARD_MM = (900, 450)


def make_letting_board(rng):
    """TO LET, and nothing else.

    NO AGENT AND NO TELEPHONE NUMBER, on purpose. A real letting board
    carries both, and both would be minted here: canon mints no estate agent,
    and any number printed on a board is somebody's. So the board says what
    it is and leaves the rest white, which is also how a board looks from
    across a street once the small print is too small to read.
    """
    w, h = LETTING_BOARD_MM[0] * MM, LETTING_BOARD_MM[1] * MM
    img = Image.new("RGB", (w, h), (236, 234, 226))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=(150, 32, 36), width=22 * MM)
    font = ImageFont.truetype(str(FONT), int(150 * MM / 0.70))
    d.text((w // 2, h // 2), "TO LET", font=font, fill=(150, 32, 36),
           anchor="mm", stroke_width=4 * MM, stroke_fill=(150, 32, 36))
    a = np.asarray(img).astype(np.float32) / 255.0
    dirt = _fbm(w, h, rng, octaves=5, cells=4)[..., None]
    a = np.clip(a * (0.84 + 0.22 * dirt), 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8), "RGB")


# ---------------------------------------------------------------------------
# A5. Double yellow lines. Two 100 mm bands, 100 mm gap, from the BOM.
# ---------------------------------------------------------------------------
def double_yellow(rng):
    w, h = 2048 * MM, 512 * MM
    band, gap = 100 * MM, 100 * MM
    rgba = np.zeros((h, w, 4), dtype=np.float32)
    # The BOM's colour is British road-marking yellow, dulled: fresh paint is
    # not what a wet 1990 kerb looks like and the whole visual target is grime.
    base = np.array([0.78, 0.62, 0.13])
    wear = _fbm(w, h, rng, octaves=5, cells=6)
    # Kerb-side band first, then the gap, then the outer band.
    y0 = h // 2 - (band + gap // 2)
    for i in range(2):
        top = y0 + i * (band + gap)
        rows = slice(top, top + band)
        n = wear[rows, :]
        # Paint thins toward both edges of a hand-laid band, and lifts where
        # the noise is high: that lift is the alpha, so the road shows through
        # rather than the yellow going grey.
        edge = np.linspace(0, 1, band)[:, None]
        edge = np.minimum(edge, 1 - edge) * 2
        edge = np.clip(edge * 3.2, 0, 1)
        alpha = np.clip(edge * (1.0 - 0.85 * np.clip(n - 0.42, 0, 1) * 2.4), 0, 1)
        # Scuffing: tyres wear the paint in streaks along the run, not across.
        streak = _fbm(w, h, rng, octaves=3, cells=2)[rows, :]
        alpha *= np.clip(0.55 + 0.75 * streak, 0, 1)
        rgba[rows, :, 0] = base[0] * (0.82 + 0.30 * n)
        rgba[rows, :, 1] = base[1] * (0.82 + 0.30 * n)
        rgba[rows, :, 2] = base[2] * (0.70 + 0.55 * n)
        rgba[rows, :, 3] = alpha
    return Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), "RGBA")


# ---------------------------------------------------------------------------
# A9. Puddle mask. Where the water IS, not what water looks like.
# ---------------------------------------------------------------------------
def puddle_mask(rng):
    w = h = 1024 * MM
    n = _fbm(w, h, rng, octaves=5, cells=3)
    # Low ground holds water: threshold the field, then soften the shoreline so
    # the shader gets a gradient to fade wetness across rather than a stencil.
    #
    # THE THRESHOLD IS READ OFF A PRINTED SERIES, AND THE FIRST ONE WAS WRONG.
    # It was 0.44/0.56, which LOOKED fine as a number and covered 64 percent of
    # the tile once the picture was opened: a mask that says "water almost
    # everywhere", which is the uniformly-wet-plane the BOM wrote this line to
    # avoid. Coverage here is the fraction of pixels above 0.5 in the finished
    # mask, measured over the whole 1024x1024 tile on this seed:
    #     0.44/0.56  0.637      0.54/0.66  0.259
    #     0.50/0.62  0.414      0.58/0.70  0.182   <- taken
    #     0.62/0.74  0.104      0.66/0.78  0.038
    # 0.58/0.70 is the rung where the tile reads as puddles joined by damp
    # rather than as a lake with dry islands in it. It is a starting bound from
    # a series and not a law: the number that settles it is a wet frame in the
    # D1b vignette, which does not exist yet.
    lo, hi = 0.58, 0.70
    m = np.clip((n - lo) / (hi - lo), 0, 1)
    m = m * m * (3 - 2 * m)
    # A second, finer field breaks the blobs up: standing water in a road is
    # puddles joined by damp, not one lake.
    m *= np.clip(0.35 + 1.2 * _fbm(w, h, rng, octaves=3, cells=9), 0, 1)
    print(f"  puddle coverage={float((m > 0.5).mean()):.3f} "
          f"(fraction of the whole {w}x{h} tile above 0.5, "
          f"bound taken from the series in the comment above)")
    return Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8), "L")


# ---------------------------------------------------------------------------
# B4. Gutter water. A strip that ramps into the kerb line.
# ---------------------------------------------------------------------------
def gutter_water(rng):
    w, h = 2048 * MM, 256 * MM
    y = np.linspace(0, 1, h)[:, None]
    # Deepest at the kerb (top of the strip), thinning to nothing at the crown.
    depth = np.clip(1.0 - y * 1.9, 0, 1) ** 1.6
    flow = _fbm(w, h, rng, octaves=4, cells=2)
    alpha = np.clip(depth * (0.55 + 0.75 * flow), 0, 1)
    # Water in a gutter reads as a DARKENING plus a sky-coloured sheen, so the
    # colour is a cold grey rather than blue paint.
    rgb = np.stack([0.16 + 0.30 * flow, 0.18 + 0.31 * flow, 0.20 + 0.33 * flow], -1)
    # Debris: grit and one or two leaves, as bright specks in the alpha only.
    grit = (_fbm(w, h, rng, octaves=2, cells=40) > 0.72).astype(np.float32)
    alpha = np.clip(alpha + grit * 0.25 * depth[:, 0][:, None], 0, 1)
    out = np.concatenate([rgb, alpha[..., None]], axis=-1)
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGBA")


# ---------------------------------------------------------------------------
# C12. Net curtain. A weave and a gather, twice.
# ---------------------------------------------------------------------------
def net_curtain(rng, pitch_mm, gather):
    w = h = 1024 * MM
    xs = np.arange(w)[None, :]
    ys = np.arange(h)[:, None]
    # The gather displaces the weave horizontally, which is what makes a net
    # read as cloth rather than as graph paper.
    shift = gather * np.sin(xs / (w / 6.0) * np.pi) * 12.0
    warp = (np.cos((xs + shift) / pitch_mm * 2 * np.pi) + 1) / 2
    weft = (np.cos(ys / pitch_mm * 2 * np.pi) + 1) / 2
    thread = np.clip(warp ** 3 + weft ** 3, 0, 1)
    grime = _fbm(w, h, rng, octaves=4, cells=3)
    # Nets in a port town are not white and the grime is the point.
    v = np.clip(0.72 + 0.22 * thread - 0.20 * grime, 0, 1)
    alpha = np.clip(0.22 + 0.55 * thread + 0.10 * grime, 0, 1)
    # Heavier at the foot where the fabric bunches.
    alpha *= np.clip(0.75 + 0.45 * (np.arange(h)[:, None] / h), 0, 1)
    rgb = np.stack([v * 0.98, v * 0.97, v * 0.92], -1)
    out = np.concatenate([rgb, alpha[..., None]], -1)
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGBA")


# ---------------------------------------------------------------------------
# E10. Street name plate. CANON STRINGS ONLY.
# ---------------------------------------------------------------------------
def street_plate(name, district, rng, streets=None):
    streets = canon_streets() if streets is None else streets
    if name not in streets:
        raise ValueError(
            f"'{name}' is not a street canon.md mints. Canon mints "
            f"{len(streets)}: {', '.join(streets) or 'none'}. A name is not "
            "invented here to unblock a picture; canon.md outranks this tool.")
    w, h = 900 * MM, 260 * MM
    img = Image.new("RGB", (w, h), (238, 236, 230))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=(28, 28, 32), width=6 * MM)
    d.rectangle([14 * MM, 14 * MM, w - 15 * MM, h - 15 * MM],
                outline=(28, 28, 32), width=3 * MM)
    big = ImageFont.truetype(str(FONT), 92 * MM)
    small = ImageFont.truetype(str(FONT), 34 * MM)
    d.text((w // 2, h // 2 + 16 * MM), name.upper(), font=big,
           fill=(24, 24, 28), anchor="mm")
    # The legend is a canon DISTRICT. Canon mints no council, so none is drawn.
    d.text((w // 2, 52 * MM), district.upper(), font=small,
           fill=(52, 52, 58), anchor="mm")
    a = np.asarray(img).astype(np.float32) / 255.0
    dirt = _fbm(w, h, rng, octaves=5, cells=4)[..., None]
    a = np.clip(a * (0.80 + 0.28 * dirt) - 0.05 * (dirt > 0.66), 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8), "RGB")


# ---------------------------------------------------------------------------
def build(dest=DEST, streets=None, districts=None):
    """Write every deterministic line, check each one, attribute all of them.

    Returns (written, blank, unknown, rows). A file that fails the blankness
    check is COUNTED AND KEPT so it can be looked at, and the caller fails.
    """
    dest = pathlib.Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    ig = _blank_check()
    streets = canon_streets() if streets is None else streets
    districts = canon_districts() if districts is None else districts
    home = districts[0] if districts else "MERIDIAN"

    jobs = [("road_double_yellow.png", "A5_double_yellow_lines",
             lambda: double_yellow(_rng("A5")),
             "2048x512mm tile, two 100mm bands with a 100mm gap, 1mm/px"),
            ("puddle_mask.png", "A9_puddle_mask",
             lambda: puddle_mask(_rng("A9")),
             "1024x1024mm tiling greyscale mask, 255 = standing water"),
            ("gutter_water.png", "B4_gutter_water",
             lambda: gutter_water(_rng("B4")),
             "2048x256mm strip, alpha deepest at the kerb edge (top)"),
            ("net_curtain_a.png", "C12_net_curtain",
             lambda: net_curtain(_rng("C12a"), 26.0, 1.0),
             "1024x1024mm, 26mm weave pitch, gathered"),
            ("net_curtain_b.png", "C12_net_curtain",
             lambda: net_curtain(_rng("C12b"), 17.0, 0.35),
             "1024x1024mm, 17mm weave pitch, nearly flat")]
    jobs.append(("fascia_mickeys_plain.png", "C6_fascia_lettering",
                 lambda: make_fascia("Mickey's", _rng("C6mickeys")),
                 "5650x460mm fascia face, canon name in plain capitals, "
                 "paint and ink sampled off the approved Hook sheet"))
    jobs.append(("board_to_let.png", "C6_letting_board",
                 lambda: make_letting_board(_rng("C6let")),
                 "900x450mm letting board, no agent and no number minted"))
    for s in streets:
        slug = s.lower().replace(" ", "_")
        jobs.append((f"plate_{slug}.png", "E10_street_name_plate",
                     (lambda s=s: street_plate(s, home, _rng("E10" + s), streets)),
                     f"900x260mm plate, canon street name, canon district legend '{home}'"))

    rows, written, blank, unknown = [], 0, 0, 0
    for fname, bom, make, note in jobs:
        p = dest / fname
        try:
            make().save(p)
        except Exception as e:                                # noqa: BLE001
            rows.append({"file": fname, "bom": bom, "status": "FAILED",
                         "why": f"{type(e).__name__}: {e}"})
            print(f"  {fname:<28} FAILED {type(e).__name__}: {e}")
            continue
        st = ig.png_stats(p)
        verdict, why = ig.blank_verdict(st)
        written += 1
        blank += verdict == "blank"
        unknown += verdict == "unknown"
        rows.append({"file": fname, "bom": bom, "note": note,
                     "bytes": p.stat().st_size,
                     "measured": f"{st.get('width')}x{st.get('height')}"
                                 f" colourType={st.get('colour_type')}",
                     "blankCheck": verdict, "why": why})
        print(f"  {fname:<28} {st.get('width')}x{st.get('height')} "
              f"{p.stat().st_size / 1024:.0f}KB  {verdict}: "
              f"spread {st.get('spread')}/255 stdev {st.get('stdev')} "
              f"over {st.get('sampled')} of {st.get('pixels')} px")

    (dest / "ATTRIBUTION.json").write_text(json.dumps({
        "what": "The D1b street vignette's deterministic 2D lines.",
        "made_by": "tools/props/make_vignette_2d.py (Pillow, numpy), "
                   f"seed {SEED}, written {time.strftime('%Y-%m-%dT%H:%M:%S')}",
        "licence": "generated by this project, no third-party asset was an input",
        "third_party_inputs": {
            "font": "ledger/Assets/Resources/LedgerSans.ttf (PT Sans, "
                    "ParaType, SIL Open Font License 1.1). Used to RENDER "
                    "letters into an image, which the OFL permits without "
                    "restriction on the result; the font itself is not "
                    "redistributed by these files. Already attributed in "
                    "THIRD-PARTY.md under 'SIL Open Font License'."},
        "canon": {"streets_used": streets, "district_legend": home,
                  "rule": "street names come from canon.md at run time and any "
                          "name not minted there is refused, so no name is "
                          "invented to unblock a picture"},
        "content_rules": "no real person, no real trade mark, in-world only; "
                         "the only lettering is canon street and district "
                         "names, the canon name Mickey's, and the words TO LET",
        "scale": "1 pixel = 1 millimetre in every file here",
        "blank_check": {
            "by": "tools/imagegen/imagegen.py png_stats + blank_verdict, "
                  "imported rather than reimplemented",
            "bound": f"blank when spread <= {ig.BLANK_MAX_SPREAD}/255 AND "
                     f"stdev <= {ig.BLANK_MAX_STDEV}, or alpha 0 everywhere sampled",
            "checked": written, "blank": blank, "unknown": unknown},
        "review": "pending: no image here has been looked at by a person yet",
        "files": rows,
    }, indent=1) + "\n", encoding="utf-8")
    return written, blank, unknown, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEST))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    streets = canon_streets()
    print(f"canon.md mints {len(streets)} street name(s): "
          f"{', '.join(streets) or 'NONE, and a plate cannot be made without one'}")
    if not streets:
        print("NOTHING MEASURED: no minted street name, so E10 is not attempted "
              "and no name is invented to replace it.")
    written, blank, unknown, rows = build(pathlib.Path(a.out))
    print(f"\n{written} file(s) written of {len(rows)} attempted, "
          f"{blank} blank, {unknown} could not be checked, "
          f"{written - blank - unknown} varied")
    if written == 0:
        print("NOTHING WAS WRITTEN, which is a failure and not a clean run.")
        return 1
    if blank or unknown:
        print("A BLANK OR UNCHECKABLE IMAGE IS A FAILURE, not a file that exists.")
        return 1
    return 0


def selftest():
    """Accepting case first, on the live canon and the live font."""
    import tempfile
    bad = 0
    ig = _blank_check()

    streets = canon_streets()
    print(f"ACCEPT: canon.md mints {len(streets)} street(s): {streets}")
    if not streets:
        print("  FAIL: canon.md has no minted street line to read"); bad = 1
    districts = canon_districts()
    print(f"ACCEPT: canon.md mints {len(districts)} district(s): {districts[:3]} ...")
    if len(districts) < 3:
        print("  FAIL: the district legend has nothing to read"); bad = 1

    with tempfile.TemporaryDirectory() as d:
        written, blank, unknown, rows = build(pathlib.Path(d))
        print(f"\nACCEPT: {written} generated file(s), {blank} blank, "
              f"{unknown} unchecked")
        if written != len(rows) or written == 0:
            print("  FAIL: every job must write a file"); bad = 1
        if blank or unknown:
            print("  FAIL: a generated file was blank or could not be read"); bad = 1

        # REJECTING 1: the blank check must be able to REFUSE. A flat image
        # through the same instrument, so a green above cannot be the check
        # never working.
        flat = pathlib.Path(d) / "flat.png"
        Image.new("RGB", (64, 64), (91, 91, 91)).save(flat)
        v, why = ig.blank_verdict(ig.png_stats(flat))
        print(f"\nREJECT: a uniform 64x64 image -> {v}")
        if v != "blank":
            print("  FAIL: the blank check cannot see a blank image"); bad = 1

        # REJECTING 3: a shop name canon does not mint.
        try:
            make_fascia("Acme Cars", _rng("x"))
            print("\nREJECT: an unminted shop name -> ACCEPTED")
            print("  FAIL: a name not in canon must be refused"); bad = 1
        except ValueError as e:
            print(f"\nREJECT: an unminted shop name -> refused ({e})")
        minted = canon_minted()
        print(f"ACCEPT: canon.md mints {minted}")
        if "Mickey's" not in minted:
            print("  FAIL: Mickey's must read as minted"); bad = 1

        # REJECTING 2: a street name canon does not mint.
        try:
            street_plate("Acacia Avenue", "the Hook", _rng("x"), streets)
            print("\nREJECT: an unminted street name -> ACCEPTED")
            print("  FAIL: a name not in canon must be refused"); bad = 1
        except ValueError as e:
            print(f"\nREJECT: an unminted street name -> refused ({e})")

    print("\nmake_vignette_2d selftest " + ("FAILED" if bad else "ok"))
    return bad


if __name__ == "__main__":
    sys.exit(main())
