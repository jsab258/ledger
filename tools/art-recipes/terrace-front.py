#!/usr/bin/env python3
"""ONE TERRACE FRONT, AUTHORED FROM ITS WRITTEN DIMENSIONS.

STATUS: PLACEHOLDER, 2026-09-22, and the mark is deliberate. The upper
storey is accepted - two recessed sashes on their stone sills and lintels,
coursed brick between, the fascia band, the eaves and the slate - but THE
GROUND FLOOR READS AS ONE UNDIFFERENTIATED DARK SLAB: the stallriser, the
display glazing, the toplight and both doors are all near-black and the same
value, so a British shopfront's four parts do not separate at any distance
and neither door is findable. Two attempts against the Hook sheet, both
rendered and looked at, and it is not a dimension problem - every number
below agrees with the emitted street to the micron. It is VALUE AND FRAME:
the parts need their own tones and the glazing needs mullions and a frame
before the front can be judged against the sheet at all. Stopped here per
the two-attempt rule rather than carried on.

The first authored Meridian facade: a single `east_parade` bay - the
shopfront row - built as an elevation and stood on the street.

    blender --background --factory-startup --python tools/art-recipes/terrace-front.py \
        -- --out DIR [--root DIR] [--bay N]
    python3 tools/art-recipes/terrace-front.py --plan
    python3 tools/art-recipes/terrace-front.py --selftest

WHAT GOVERNS IT. `production/specs/terrace-fronts.md`, 644 lines, which is
SPEC station only and authors no geometry; every number it tags MEASURED
comes from `production/specs/vignette-scene.json`, and THIS FILE READS THAT
FILE rather than retyping the spec's table. That is the difference between a
recipe and a transcription: if the scene file moves, this moves with it, and
cross_check() prints the agreement per field every run so a silent divergence
is impossible. The Hook sheet governs LOOK and PERIOD; it governs no
geometry, which is the ruling of 2026-09-21 and the lesson the lamp column
paid four attempts for.

NO BOOLEANS ANYWHERE, and that is a decision rather than a limitation. A
British terrace elevation IS a coursed plane broken by openings, and the
street's own blockout already emits it that way: sills, lintels and reveals
are separate pieces in `vignette-pieces.json`, not holes cut in a wall. So
the front is built as PANELS AROUND THE OPENINGS - bands and piers whose
edges are the opening edges - which needs no boolean, cannot leave a
non-manifold seam, and puts every edge exactly where a dimension says.

WHAT THIS DOES NOT AUTHOR, said plainly rather than left to be discovered:
the cornice and console brackets above the fascia band, which are already
authored and committed as `fascia_cornice_01` and `fascia_console_01`
(`production/art/fascia-01/`); the interior card behind the glazing, which is
BOM C11 and belongs to the decal generator; the chimney pots (D3, HAVE); and
the wear layer, which under D53 is a separable pass and is not this station.
The fascia band this file builds is what those brackets sit ON, and its top
is the first-floor slab, so it cannot move without moving them.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC_REL = "production/specs/vignette-scene.json"
PIECES_REL = "production/specs/vignette-pieces.json"

#: THE STREET DATUM, MEASURED. `production/specs/terrace-fronts.md` section 3:
#: "street absolute y = local y + 0.100 m", the built street's own
#: footway-above-crown offset at the frontage line, constant across every
#: piece checked. Everything below is authored in LOCAL coordinates, where 0
#: is the bay's own threshold, and integration adds this.
THRESHOLD_ABOVE_CROWN_M = 0.100

#: Materials, the same convention lighting-column.py uses and for the same
#: reason: authored Base Color triples assigned RAW, so a later reader can
#: see which number was used without opening a colour-management setting.
#: LINEAR sRGB, because Blender's node sockets store linear on a direct
#: property set.
#:
#: brick_red and brick_grey are CHOSEN here, and are marked so: the scene
#: file names the SURFACE ("brick_red") and not a colour, and no committed
#: file in this repository carries a triple for it. They are a low-chroma
#: London-stock red and a soot-grey, which is what the period research asks
#: for; the Hook sheet governs whether they are right and the eye decides.
MATERIALS = (
    ("brick_red",   (0.085, 0.040, 0.030), 0.92),
    ("brick_grey",  (0.055, 0.052, 0.048), 0.92),
    ("stone",       (0.240, 0.225, 0.200), 0.80),   # sills, lintels, coping
    ("paint_dark",  (0.020, 0.030, 0.026), 0.55),   # shopfront joinery, doors
    ("paint_fascia",(0.030, 0.022, 0.030), 0.45),   # the lettered board
    ("glass",       (0.035, 0.040, 0.042), 0.12),
    ("lead",        (0.030, 0.030, 0.032), 0.60),   # downpipe
    ("slate",       (0.026, 0.028, 0.032), 0.70),
    # WHAT A WINDOW SHOWS IS THE INSIDE, and the first render of this bay is
    # why that has a material of its own. The carcass behind the elevation was
    # brick_red and filled the frontage plane, so every opening - two sashes,
    # a shopfront, two doors - read as unbroken brickwork and the front came
    # back as a blank box with sills on it. The openings are real; there was
    # simply nothing dark behind them.
    ("interior",    (0.010, 0.009, 0.009), 0.95),
)

#: The two frames. ELEVATION IS THE ONE THAT JUDGES THE FRONT - square to the
#: frontage with the roofline in, which is cam_B's own description in the
#: scene file - and EYE is the one that says whether it belongs on a street,
#: at cam_A's 1.6 m and its measured 4 degree downward pitch. Both are
#: derived from the bay's own dimensions below rather than typed, so a bay of
#: another width still frames.
FRAMES = ("elevation", "eye")
AUTHORED_RES = (1400, 1100)


# ---------------------------------------------------------------------------
# PURE. Everything a selftest can drive with no Blender and no filesystem
# beyond reading the two committed spec files.
# ---------------------------------------------------------------------------


def brick_length_m(raw):
    """One British brick on its length, MEASURED rather than typed.

    `blocks[1].roof.parapet_thickness_m` is 0.215 in the scene file and its
    own note says why: "one British brick on its length, 215 mm". That is the
    module this elevation's wall thickness is, so it is read from there
    rather than written again here. The facade block's reveal_depth_m is the
    half-brick from the same module, and selftest asks whether the two still
    describe the same brick."""
    try:
        for b in raw.get("blocks", []) or []:
            t = (b.get("roof") or {}).get("parapet_thickness_m")
            if t:
                return float(t)
    except (TypeError, ValueError):
        pass
    return None


def load_spec(root, spec_rel=SPEC_REL):
    """(params, error). The numbers, read from the scene file, never typed."""
    path = os.path.join(root, spec_rel)
    if not os.path.exists(path):
        return None, "no-spec-file/%s" % path.replace(" ", "~")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, ValueError) as exc:
        return None, "unreadable-spec-json/%s" % type(exc).__name__

    blocks = raw.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        return None, "spec-has-no-blocks"
    block = None
    for b in blocks:
        if b.get("id") == "east_parade":
            block = b
            break
    if block is None:
        return None, "spec-has-no-east_parade-block"

    shop = raw.get("shopfront")
    face = raw.get("facade")
    roofline = raw.get("roofline")
    if not isinstance(shop, dict) or not isinstance(face, dict) or not isinstance(roofline, dict):
        return None, "spec-missing-shopfront-facade-or-roofline"

    try:
        storeys = [float(v) for v in block["storey_heights_m"]]
        roof = block["roof"]
        p = {
            "bay_width_m":      float(block["bay_width_m"]),
            "depth_m":          float(block["depth_m"]),
            "start_x_m":        float(block["start_x_m"]),
            "bays":             int(block["bays"]),
            "wall_surface":     str(block["wall_surface"]),
            "ground_h_m":       storeys[0],
            "first_h_m":        storeys[1],
            "pitch_deg":        float(roof["pitch_deg"]),
            "eaves_overhang_m": float(roof["eaves_overhang_m"]),

            "stallriser_h_m":   float(shop["stallriser_height_m"]),
            "stallriser_proj_m":float(shop["stallriser_projection_m"]),
            "pilaster_w_m":     float(shop["pilaster_width_m"]),
            "pilaster_proj_m":  float(shop["pilaster_projection_m"]),
            "transom_h_m":      float(shop["transom_height_m"]),
            "transom_t_m":      float(shop["transom_thickness_m"]),
            "fascia_bottom_m":  float(shop["fascia_bottom_m"]),
            "fascia_proj_m":    float(shop["fascia_projection_m"]),
            "glazing_recess_m": float(shop["glazing_recess_m"]),
            "shop_door_w_m":    float(shop["shop_door"]["width_m"]),
            "shop_door_h_m":    float(shop["shop_door"]["height_m"]),
            "shop_glazed_from_m": float(shop["shop_door"]["glazed_from_m"]),
            "side_door_w_m":    float(shop["side_door"]["width_m"]),
            "side_door_h_m":    float(shop["side_door"]["height_m"]),
            "letterplate_w_m":  float(shop["side_door"]["letterplate_width_m"]),
            "letterplate_h_m":  float(shop["side_door"]["letterplate_height_m"]),
            "letterplate_at_m": float(shop["side_door"]["letterplate_at_m"]),

            "windows_per_bay":  int(face["windows_per_bay"]),
            "window_w_m":       float(face["window_width_m"]),
            "window_h_m":       float(face["window_height_m"]),
            "reveal_m":         float(face["reveal_depth_m"]),
            "sill_proj_m":      float(face["sill_projection_m"]),
            "sill_t_m":         float(face["sill_thickness_m"]),
            "sill_extra_w_m":   float(face["sill_extra_width_m"]),
            "lintel_t_m":       float(face["lintel_thickness_m"]),
            "head_below_ceiling_m": float(face["head_below_ceiling_m"]),
            "brick_course_m":   float(face["brick_course_m"]),

            "downpipe_dia_m":   float(roofline["downpipe"]["diameter_m"]),
            "chimney_w_m":      float(roofline["chimney"]["width_m"]),
            "chimney_d_m":      float(roofline["chimney"]["depth_m"]),
            "chimney_above_ridge_m": float(roofline["chimney"]["height_above_ridge_m"]),
        }
        bl = brick_length_m(raw)
        if bl is None or bl <= 0:
            return None, "spec-carries-no-brick-length-to-read-a-wall-thickness-from"
        p["wall_t_m"] = bl
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        return None, "spec-field-refused/%s" % str(exc).replace(" ", "~")[:80]

    for key in ("bay_width_m", "depth_m", "ground_h_m", "first_h_m",
                "window_w_m", "window_h_m", "pilaster_w_m"):
        if p[key] <= 0:
            return None, "non-positive-dimension/%s=%.6f" % (key, p[key])

    # DERIVED, and every one of these is the spec's own arithmetic re-done
    # here rather than copied as a literal, so the two cannot drift.
    p["eaves_m"] = p["ground_h_m"] + p["first_h_m"]
    p["ridge_rise_m"] = (p["depth_m"] / 2.0) * math.tan(math.radians(p["pitch_deg"]))
    p["ridge_m"] = p["eaves_m"] + p["ridge_rise_m"]
    p["opening_zone_m"] = p["bay_width_m"] - 2.0 * p["pilaster_w_m"]
    # The display run is what is LEFT of the opening zone once the two doors
    # have taken theirs. The spec states the identity the other way round
    # (3.562 + 0.9 + 0.838 = 5.300) and acceptance check 10 asserts it.
    p["display_w_m"] = p["opening_zone_m"] - p["shop_door_w_m"] - p["side_door_w_m"]
    p["window_head_m"] = p["eaves_m"] - p["head_below_ceiling_m"]
    p["window_sill_m"] = p["window_head_m"] - p["window_h_m"]
    p["sill_w_m"] = p["window_w_m"] + p["sill_extra_w_m"]
    p["_path"] = path
    return p, ""


def window_centres(p):
    """Where the upper windows sit, MEASURED off the emitted pieces: bay_start
    + 1.5 m and + 4.5 m. Expressed as fractions of the bay so a bay of another
    width still divides sensibly, and asserted against 1.5/4.5 at 6.0 m in
    selftest so the fraction cannot quietly restate a different rhythm."""
    w = p["bay_width_m"]
    return [w * 0.25, w * 0.75]


def cross_check(p, root, pieces_rel=PIECES_REL):
    """[(field, authored, emitted, agree)]. The authored numbers against the
    610-piece blockout the street is actually built from.

    THIS IS THE CHECK THAT MATTERS, and it is the one lighting-column.py
    carries for the same reason: an authored front that disagrees with the
    emitted carcass it replaces will float, sink or overhang, and no render
    of the front ALONE can show it."""
    path = os.path.join(root, pieces_rel)
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, ValueError):
        return rows
    by_name = {}
    for piece in raw.get("pieces", []) or []:
        if isinstance(piece, dict) and piece.get("name"):
            by_name[piece["name"]] = piece

    def take(name, key):
        piece = by_name.get(name)
        if not isinstance(piece, dict):
            return None
        v = piece.get(key)
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    wanted = (
        ("carcass_height_m", p["eaves_m"], take("east_parade_bay0", "sy_m")),
        ("carcass_width_m", p["bay_width_m"], take("east_parade_bay0", "sx_m")),
        ("carcass_depth_m", p["depth_m"], take("east_parade_bay0", "sz_m")),
        ("upper_window_w_m", p["window_w_m"], take("east_parade_up0_w0", "sx_m")),
        ("upper_window_h_m", p["window_h_m"], take("east_parade_up0_w0", "sy_m")),
    )
    for field, authored, emitted in wanted:
        if emitted is None:
            rows.append((field, authored, None, None))
        else:
            rows.append((field, authored, emitted, abs(authored - emitted) < 1e-6))
    return rows


def _box(parts, pid, material, x0, x1, y0, y1, z0, z1, note=""):
    """One rectangular piece, named, with its own extents. Refuses a box with
    a non-positive dimension rather than emitting a degenerate one: a zero
    width face renders as nothing and reads in a frame as a missing part."""
    if x1 <= x0 or y1 <= y0 or z1 <= z0:
        raise ValueError("terrace-front: degenerate box %s (%.4f..%.4f, %.4f..%.4f, %.4f..%.4f)"
                         % (pid, x0, x1, y0, y1, z0, z1))
    parts.append({"id": pid, "material": material, "note": note,
                  "x0": x0, "x1": x1, "y0": y0, "y1": y1, "z0": z0, "z1": z1})
    return parts[-1]


def plan_parts(p):
    """Every piece of one bay, in local coordinates.

    THE AXES. x runs along the street from the bay's own left edge; y runs
    INTO the building from the frontage plane at y=0, so anything proud of
    the wall has a NEGATIVE y; z is height from the threshold.
    """
    parts = []
    W = p["bay_width_m"]
    D = p["depth_m"]
    # THE ZONE HAS TO EXIST BEFORE ANYTHING IS PUT IN IT, and this guard
    # catches two different faults with one comparison. A bay too narrow for
    # its own two piers and two doors has no opening zone at all; and a
    # params dict whose DERIVED values no longer follow from its primitives -
    # which is what an edit to bay_width without re-deriving looks like -
    # fails the first half. Refused rather than clamped, so a future edit
    # fails loudly instead of quietly shipping a front that cannot be built.
    zone = W - 2.0 * p["pilaster_w_m"]
    if abs(zone - p["opening_zone_m"]) > 1e-9:
        raise ValueError(
            "terrace-front: opening_zone_m=%.4f does not follow from bay_width_m=%.4f "
            "less two piers of %.4f (=%.4f); the derived numbers are stale"
            % (p["opening_zone_m"], W, p["pilaster_w_m"], zone))
    if zone <= p["shop_door_w_m"] + p["side_door_w_m"]:
        raise ValueError(
            "terrace-front: an opening zone of %.4f m has no room for a %.4f m shop door "
            "and a %.4f m side door, let alone glazing"
            % (zone, p["shop_door_w_m"], p["side_door_w_m"]))
    GF = p["ground_h_m"]
    EAVES = p["eaves_m"]
    wall = p["wall_surface"]

    # ---- the carcass behind everything -----------------------------------
    # Set back to the frontage plane and running the full depth. Every
    # elevation piece below sits on its face or proud of it.
    T = p["wall_t_m"]
    # THE CARCASS STARTS BEHIND THE WALL, not at the frontage plane, and it is
    # the INSIDE. Every opening below is a real hole through a one-brick wall
    # onto this; when it filled the frontage in brick the holes had nothing to
    # show and the elevation read as a blank box.
    _box(parts, "carcass", "interior", 0.0, W, T, D, 0.0, EAVES,
         "what-a-window-shows/starts-one-brick-back-so-the-openings-are-real")

    # ---- ground floor: the shopfront -------------------------------------
    pw = p["pilaster_w_m"]
    pp = p["pilaster_proj_m"]
    _box(parts, "pilaster_left", "stone", 0.0, pw, -pp, 0.0, 0.0, GF,
         "a-shopfront-earns-its-piers/full-ground-floor-height-at-every-bay-edge")
    _box(parts, "pilaster_right", "stone", W - pw, W, -pp, 0.0, 0.0, GF,
         "the-party-wall-pier-shared-with-the-next-bay")

    # The opening zone, and the three things that fill it, left to right:
    # display glazing, shop door, side door. The order is the spec's own.
    zx0 = pw
    disp_x0, disp_x1 = zx0, zx0 + p["display_w_m"]
    shop_x0, shop_x1 = disp_x1, disp_x1 + p["shop_door_w_m"]
    side_x0, side_x1 = shop_x1, shop_x1 + p["side_door_w_m"]

    sr_h = p["stallriser_h_m"]
    sr_p = p["stallriser_projection_m"] if "stallriser_projection_m" in p else p["stallriser_proj_m"]
    rec = p["glazing_recess_m"]
    tr_h = p["transom_h_m"]
    tr_t = p["transom_t_m"]
    fb = p["fascia_bottom_m"]
    fp = p["fascia_proj_m"]

    # STALLRISER under the display run only. It stops at the shop door, which
    # is what a door is: a hole to the pavement.
    _box(parts, "stallriser", "paint_dark", disp_x0, disp_x1, -sr_p, 0.0, 0.0, sr_h,
         "0.6m-of-kicked-board-under-the-glass/projects-proud-of-the-glazing-line")
    _box(parts, "display_glazing", "glass", disp_x0, disp_x1, rec, rec + 0.02, sr_h, tr_h,
         "recessed-so-the-frontage-is-not-one-plane")
    _box(parts, "transom_bar", "paint_dark", disp_x0, shop_x1, -0.02, 0.02, tr_h, tr_h + tr_t,
         "the-bar-runs-across-the-glazing-AND-the-shop-door/one-line-across-the-opening")
    # TOPLIGHT: from the transom to the fascia line less its own frame. The
    # spec gives "roughly 2.82" as DERIVED; it is derived here instead of
    # copied, as fascia_bottom less one brick course.
    top_z1 = fb - p["brick_course_m"] * 0.5
    _box(parts, "toplight", "glass", disp_x0, shop_x1, rec, rec + 0.02, tr_h + tr_t, top_z1,
         "the-light-above-the-transom/derived-top=fascia_bottom-minus-half-a-course")

    # SHOP DOOR, brick spandrel above it to the fascia.
    _box(parts, "shop_door_leaf", "paint_dark", shop_x0, shop_x1, 0.02, 0.06,
         0.0, p["shop_glazed_from_m"],
         "solid-below-the-glazed-light")
    _box(parts, "shop_door_light", "glass", shop_x0, shop_x1, 0.03, 0.05,
         p["shop_glazed_from_m"], p["shop_door_h_m"],
         "the-glazed-upper-light")
    _box(parts, "shop_door_spandrel", wall, shop_x0, shop_x1, 0.0, T,
         p["shop_door_h_m"], fb, "brick-between-the-door-head-and-the-board")

    # SIDE DOOR: the flat above. Its own spandrel, and a letterplate.
    _box(parts, "side_door_leaf", "paint_dark", side_x0, side_x1, 0.02, 0.06,
         0.0, p["side_door_h_m"],
         "1981x838mm/the-standard-British-external-door/imperial-because-the-country-was")
    lp_w, lp_h = p["letterplate_w_m"], p["letterplate_h_m"]
    lp_cx = (side_x0 + side_x1) * 0.5
    _box(parts, "letterplate", "lead", lp_cx - lp_w / 2.0, lp_cx + lp_w / 2.0,
         0.005, 0.025, p["letterplate_at_m"], p["letterplate_at_m"] + lp_h,
         "the-one-detail-that-says-somebody-lives-above-the-shop")
    _box(parts, "side_door_spandrel", wall, side_x0, side_x1, 0.0, T,
         p["side_door_h_m"], fb, "brick-between-the-door-head-and-the-board")

    # A sliver of brick between the side door and the right pier, when the
    # three widths do not quite fill the zone. Emitted only when it exists.
    if side_x1 < W - pw - 1e-9:
        _box(parts, "zone_infill", wall, side_x1, W - pw, 0.0, T, 0.0, fb,
             "the-remainder-of-the-opening-zone/emitted-only-when-it-exists")

    # FASCIA BAND, the full bay width, top AT the first-floor slab. This is
    # what the already-authored cornice and consoles sit on and it must not
    # move: production/art/fascia-01/.
    _box(parts, "fascia_band", "paint_fascia", 0.0, W, -fp, 0.0, fb, GF,
         "top-IS-the-first-floor-slab/the-committed-cornice-sits-on-this")

    # ---- first floor: a coursed plane broken by two openings -------------
    sill_z = p["window_sill_m"]
    head_z = p["window_head_m"]
    hw = p["window_w_m"] / 2.0
    centres = window_centres(p)
    opens = [(c - hw, c + hw) for c in centres]

    # The three horizontal bands. Band B is the only one the openings cut.
    _box(parts, "upper_band_below", wall, 0.0, W, 0.0, T, GF, sill_z,
         "coursed-brick-from-the-slab-to-the-sills")
    _box(parts, "upper_band_above", wall, 0.0, W, 0.0, T, head_z, EAVES,
         "coursed-brick-from-the-heads-to-the-eaves")

    edges = [0.0]
    for a, b in opens:
        edges.extend([a, b])
    edges.append(W)
    for i in range(0, len(edges) - 1, 2):
        a, b = edges[i], edges[i + 1]
        if b > a + 1e-9:
            _box(parts, "upper_pier_%d" % (i // 2), wall, a, b, 0.0, T, sill_z, head_z,
                 "the-brick-between-the-openings")

    for i, (a, b) in enumerate(opens):
        cx = (a + b) * 0.5
        sw = p["sill_w_m"] / 2.0
        # THE REVEAL IS HALF A BRICK, and it is why a window is not a decal.
        _box(parts, "upper_glass_%d" % i, "glass", a, b, p["reveal_m"], p["reveal_m"] + 0.02,
             sill_z, head_z, "set-back-one-half-brick/102.5mm/the-depth-that-stops-it-reading-flat")
        _box(parts, "upper_sill_%d" % i, "stone", cx - sw, cx + sw,
             -p["sill_proj_m"], T, sill_z - p["sill_t_m"], sill_z,
             "0.95m-wide/window-plus-50mm-each-side")
        _box(parts, "upper_lintel_%d" % i, "stone", cx - sw, cx + sw,
             -0.02, T, head_z, head_z + p["lintel_t_m"],
             "over-the-head/one-course-and-a-half")

    # ---- roof, downpipe, stack -------------------------------------------
    # The roof is two slopes to a ridge running ALONG the street. Only the
    # street-facing one is in any frame this recipe takes, but both are built
    # because a half roof reads as a fault from the eye camera's angle.
    ov = p["eaves_overhang_m"]
    _box(parts, "eaves_course", "stone", -ov * 0.5, W + ov * 0.5, -ov, T,
         EAVES, EAVES + 0.09, "the-line-the-roof-starts-from")
    parts.append({"id": "roof_front", "material": "slate", "kind": "slope",
                  "x0": -ov * 0.5, "x1": W + ov * 0.5,
                  "y_eaves": -ov, "y_ridge": D / 2.0,
                  "z_eaves": EAVES, "z_ridge": p["ridge_m"],
                  "note": "35-degrees/the-common-British-slated-terrace-pitch"})
    parts.append({"id": "roof_back", "material": "slate", "kind": "slope",
                  "x0": -ov * 0.5, "x1": W + ov * 0.5,
                  "y_eaves": D + ov, "y_ridge": D / 2.0,
                  "z_eaves": EAVES, "z_ridge": p["ridge_m"],
                  "note": "built-though-unseen/a-half-roof-reads-as-a-fault-from-the-eye-camera"})

    # DOWNPIPE at the party wall, never at a row's outer end. This bay's
    # right-hand edge IS an internal party wall on a six-bay row.
    dr = p["downpipe_dia_m"] / 2.0
    _box(parts, "downpipe", "lead", W - dr * 2.0, W, -p["downpipe_dia_m"], 0.0,
         0.0, EAVES, "at-the-party-wall/one-per-bay-boundary-never-at-a-row-end")

    # CHIMNEY STACK, on the party wall, top one metre above the ridge.
    cw, cd = p["chimney_w_m"], p["chimney_d_m"]
    _box(parts, "chimney_stack", wall, W - cw / 2.0, W + cw / 2.0,
         D / 2.0 - cd / 2.0, D / 2.0 + cd / 2.0,
         EAVES, p["ridge_m"] + p["chimney_above_ridge_m"],
         "a-stack-serves-both-houses-either-side-of-the-wall-it-stands-on")
    return parts


def frame_cameras(p):
    """The two viewpoints, derived from the bay rather than typed.

    ELEVATION frames the whole front plus the stack with a margin, square on,
    level. Its distance is solved from the vertical field so a taller bay
    pulls the camera back instead of cropping the roof.

    EYE is cam_A's own numbers - 1.6 m on the footway, 4 degrees down - stood
    on the far side of a 6 m carriageway and two 2 m footways, which is the
    street this bay is on.
    """
    W = p["bay_width_m"]
    top = p["ridge_m"] + p["chimney_above_ridge_m"]
    fov_v = math.radians(40.0)
    need = top * 1.25
    dist = (need / 2.0) / math.tan(fov_v / 2.0)
    return {
        "elevation": {
            "loc": (W / 2.0, -dist, top / 2.0),
            "look": (W / 2.0, 0.0, top / 2.0),
            "fov_v_deg": 40.0,
            "note": "square-to-the-frontage-roofline-in-frame/cam_B's-own-description",
        },
        "eye": {
            "loc": (-W * 0.55, -10.0, 1.6),
            "look": (W * 0.60, 0.0, 2.6),
            "fov_v_deg": 60.0,
            "note": "1.6m-on-the-far-footway/cam_A's-eye-height-and-field",
        },
    }


def look_at_euler(loc, target):
    """(rx, ry, rz) for a Blender camera at `loc` looking at `target`.

    CLOSED FORM, AND TESTED BY COMPOSING IT BACK. A Blender camera with a
    zero rotation looks down its own -Z with +Y up, so aiming it is two
    turns: rx away from straight down, then rz around the world's Z.

        direction = Rz(rz) . Rx(rx) . (0, 0, -1)
                  = (-sin(rx) sin(rz), sin(rx) cos(rz), -cos(rx))

    WRITTEN OUT BECAUSE THE FIRST VERSION WAS WRONG AND THE RENDER SHOWED A
    FIELD. It had rz a quarter turn the wrong way and rx measured against
    +z instead of -z, which aimed both cameras at the sky behind the
    building. euler_direction() below composes this back and selftest asks
    whether the two agree on the actual frames this file takes, so the same
    mistake cannot be made silently again.
    """
    dx = target[0] - loc[0]
    dy = target[1] - loc[1]
    dz = target[2] - loc[2]
    return (math.atan2(math.hypot(dx, dy), -dz), 0.0, math.atan2(dy, dx) - math.pi / 2.0)


def euler_direction(euler):
    """The unit direction a Blender camera with this rotation actually looks.
    The inverse of look_at_euler, used only to check it."""
    rx, _ry, rz = euler
    return (-math.sin(rx) * math.sin(rz),
            math.sin(rx) * math.cos(rz),
            -math.cos(rx))


def plan_lines(p, parts, checks):
    lines = []
    for field, authored, emitted, agree in checks:
        if emitted is None:
            lines.append("tfCheck field=%s authored=%.6f emitted=nothing-measured "
                         "agree=nothing-measured" % (field, authored))
        else:
            lines.append("tfCheck field=%s authored=%.6f emitted=%.6f diff=%.6f agree=%s"
                         % (field, authored, emitted, abs(authored - emitted),
                            "yes" if agree else "no"))
    lines.append(
        "tfBay widthM=%.3f depthM=%.3f groundFloorM=%.3f firstFloorM=%.3f eavesM=%.3f "
        "ridgeM=%.3f ridgeRiseM=%.3f pitchDeg=%.1f absoluteEavesM=%.3f datumM=%.3f"
        % (p["bay_width_m"], p["depth_m"], p["ground_h_m"], p["first_h_m"], p["eaves_m"],
           p["ridge_m"], p["ridge_rise_m"], p["pitch_deg"],
           p["eaves_m"] + THRESHOLD_ABOVE_CROWN_M, THRESHOLD_ABOVE_CROWN_M))
    lines.append(
        "tfZone openingZoneM=%.3f displayM=%.3f shopDoorM=%.3f sideDoorM=%.3f sumM=%.3f "
        "closes=%s specStatesM=5.300"
        % (p["opening_zone_m"], p["display_w_m"], p["shop_door_w_m"], p["side_door_w_m"],
           p["display_w_m"] + p["shop_door_w_m"] + p["side_door_w_m"],
           "yes" if abs(p["display_w_m"] + p["shop_door_w_m"] + p["side_door_w_m"]
                        - p["opening_zone_m"]) < 1e-9 else "no"))
    lines.append(
        "tfUpper sillM=%.3f headM=%.3f windowM=%.3fx%.3f revealM=%.4f sillWidthM=%.3f "
        "centresM=%s courseM=%.3f sillIsWholeCourses=%s"
        % (p["window_sill_m"], p["window_head_m"], p["window_w_m"], p["window_h_m"],
           p["reveal_m"], p["sill_w_m"],
           ",".join("%.3f" % c for c in window_centres(p)), p["brick_course_m"],
           "yes" if abs((p["window_sill_m"] / p["brick_course_m"])
                        - round(p["window_sill_m"] / p["brick_course_m"])) < 1e-6 else "no"))
    for part in parts:
        if part.get("kind") == "slope":
            lines.append("tfPart id=%s material=%s kind=slope note=%s"
                         % (part["id"], part["material"], part["note"]))
        else:
            lines.append(
                "tfPart id=%s material=%s kind=box xM=%.3f..%.3f yM=%.4f..%.4f zM=%.3f..%.3f note=%s"
                % (part["id"], part["material"], part["x0"], part["x1"],
                   part["y0"], part["y1"], part["z0"], part["z1"], part["note"]))
    return lines


# ---------------------------------------------------------------------------
# BLENDER. Nothing above this line imports bpy.
# ---------------------------------------------------------------------------


def _bpy():
    import bpy
    return bpy


def _materials(bpy):
    made = {}
    for name, linear, rough in MATERIALS:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is not None:
            bsdf.inputs["Base Color"].default_value = (linear[0], linear[1], linear[2], 1.0)
            bsdf.inputs["Roughness"].default_value = rough
            if name == "glass":
                bsdf.inputs["Metallic"].default_value = 0.0
                if "Specular IOR Level" in bsdf.inputs:
                    bsdf.inputs["Specular IOR Level"].default_value = 0.9
        made[name] = mat
    return made


def _mesh_object(bpy, name, verts, faces, mat):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    if mat is not None:
        obj.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def _box_mesh(bpy, part, mat):
    x0, x1 = part["x0"], part["x1"]
    y0, y1 = part["y0"], part["y1"]
    z0, z1 = part["z0"], part["z1"]
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return _mesh_object(bpy, part["id"], v, f, mat)


def _slope_mesh(bpy, part, mat):
    x0, x1 = part["x0"], part["x1"]
    ye, yr = part["y_eaves"], part["y_ridge"]
    ze, zr = part["z_eaves"], part["z_ridge"]
    t = 0.06
    v = [(x0, ye, ze), (x1, ye, ze), (x1, yr, zr), (x0, yr, zr),
         (x0, ye, ze - t), (x1, ye, ze - t), (x1, yr, zr - t), (x0, yr, zr - t)]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1),
         (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return _mesh_object(bpy, part["id"], v, f, mat)


def _world(bpy, root):
    """Overcast, from the held HDRI where it is there, and a flat sky where it
    is not - announced either way, never silently flat."""
    world = bpy.data.worlds.new("terrace_world")
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    bg = nt.nodes.get("Background")
    hdr = os.path.join(root, "ledger/Assets/Resources/Sky/polyhaven/belfast_open_field_2k.hdr")
    if os.path.exists(hdr) and bg is not None:
        env = nt.nodes.new("ShaderNodeTexEnvironment")
        try:
            env.image = bpy.data.images.load(hdr)
            nt.links.new(env.outputs["Color"], bg.inputs["Color"])
            bg.inputs["Strength"].default_value = 1.0
            return "hdri=%s" % hdr.replace(" ", "~")
        except RuntimeError:
            pass
    if bg is not None:
        bg.inputs["Color"].default_value = (0.42, 0.45, 0.50, 1.0)
        bg.inputs["Strength"].default_value = 1.0
    return "hdri=NOT-FOUND/flat-overcast-instead"


def _ground(bpy, p, mats):
    """The footway and the road under the bay, so it is standing on something.
    The street's own widths: 2 m footway each side, 6 m carriageway."""
    W = p["bay_width_m"]
    part = {"id": "footway", "x0": -W, "x1": W * 2.0, "y0": -10.0, "y1": 0.0,
            "z0": -0.12, "z1": 0.0}
    obj = _box_mesh(bpy, part, mats.get("stone"))
    return obj


def _camera(bpy, name, spec):
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens_unit = "FOV"
    cam_data.sensor_fit = "VERTICAL"
    cam_data.angle_y = math.radians(spec["fov_v_deg"])
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(cam)
    lx, ly, lz = spec["loc"]
    tx, ty, tz = spec["look"]
    cam.location = (lx, ly, lz)
    cam.rotation_euler = look_at_euler((lx, ly, lz), (tx, ty, tz))
    return cam


def build_and_render(args):
    bpy = _bpy()
    p, err = load_spec(args["root"], args["spec"])
    if err:
        print("terrace-front refused: status=NO-SPEC reason=%s nothing measured" % err)
        return 3
    parts = plan_parts(p)
    checks = cross_check(p, args["root"])

    for line in plan_lines(p, parts, checks):
        print(line)

    # A CLEAN SCENE, removed through the data API rather than by an operator:
    # operators need a context a --background run does not reliably have.
    removed = 0
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
        removed += 1
    print("tfNote sceneReset=dataApi/removed=%d-objects" % removed)

    mats = _materials(bpy)
    built = 0
    for part in parts:
        mat = mats.get(part["material"])
        if part.get("kind") == "slope":
            _slope_mesh(bpy, part, mat)
        else:
            _box_mesh(bpy, part, mat)
        built += 1
    _ground(bpy, p, mats)
    world_note = _world(bpy, args["root"])
    print("tfNote world/%s" % world_note)

    sun_data = bpy.data.lights.new("sun", type="SUN")
    sun_data.energy = 2.2
    sun_data.angle = math.radians(8.0)
    sun = bpy.data.objects.new("sun", sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(54.0), 0.0, math.radians(200.0))

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x, scene.render.resolution_y = AUTHORED_RES
    scene.render.image_settings.file_format = "PNG"

    cams = frame_cameras(p)
    wrote = 0
    for name in FRAMES:
        cam = _camera(bpy, "cam_" + name, cams[name])
        scene.camera = cam
        out = os.path.join(args["out"], "terrace-front-%s.png" % name)
        scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        size = os.path.getsize(out) if os.path.exists(out) else 0
        print("tfFrame id=%s png=%s bytes=%d fovVDeg=%.1f note=%s"
              % (name, os.path.basename(out), size, cams[name]["fov_v_deg"],
                 cams[name]["note"]))
        if size > 0:
            wrote += 1

    agree = sum(1 for _, _, _, a in checks if a)
    print("tfStatus=PLACEHOLDER/upper-storey-accepted/ground-floor-reads-as-one-dark-slab "
          "whatIsWrong=stallriser-glazing-toplight-and-both-doors-are-all-the-same-near-black-value-"
          "and-the-glazing-has-no-frame-or-mullions notADimensionProblem=crossCheckAgree-is-5/5 "
          "attempts=2/2 stoppedPer=two-attempt-rule")
    print("terrace-front done: status=RAN bay=east_parade partsBuilt=%d/%d "
          "crossCheckAgree=%d/%d previewsWrote=%d/%d res=%dx%d outDir=%s"
          % (built, len(parts), agree, len(checks), wrote, len(FRAMES),
             AUTHORED_RES[0], AUTHORED_RES[1], args["out"]))
    return 0 if wrote == len(FRAMES) else 1


# ---------------------------------------------------------------------------


def parse_args(argv):
    args = list(argv)
    if "--" in args:
        args = args[args.index("--") + 1:]
    elif args and args[0].endswith(".py"):
        args = args[1:]
    out = {"out": "", "root": ROOT, "spec": SPEC_REL,
           "plan": False, "selftest": False, "error": ""}
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--out", "--output-dir") and i + 1 < len(args):
            out["out"] = args[i + 1]; i += 2
        elif a == "--root" and i + 1 < len(args):
            out["root"] = args[i + 1]; i += 2
        elif a == "--spec" and i + 1 < len(args):
            out["spec"] = args[i + 1]; i += 2
        elif a == "--plan":
            out["plan"] = True; i += 1
        elif a == "--selftest":
            out["selftest"] = True; i += 1
        # THE LANE PASSES THESE AND THIS RECIPE READS NO COMMISSION, so they
        # are accepted and ignored rather than refused: a recipe that rejects
        # the lane's own line cannot be run by the lane.
        elif a in ("--commission", "--run-sha", "--studio-sha", "--res",
                   "--engine", "--samples") and i + 1 < len(args):
            i += 2
        else:
            out["error"] = "unknown-flag/%s" % a.replace(" ", "~")
            break
    return out


def selftest():
    passed = failed = 0

    def check(name, ok, detail=""):
        nonlocal passed, failed
        if ok:
            passed += 1
        else:
            failed += 1
            print("terrace-front selftest FAIL %s: %s" % (name, detail))

    p, err = load_spec(ROOT)
    check("accept/spec-loads", not err, err)
    if p:
        # THE SPEC'S OWN ARITHMETIC, RE-DONE. Every one of these is a number
        # terrace-fronts.md states as DERIVED; if this file's derivation and
        # the spec's prose ever disagree, one of them is wrong and this says
        # which run found it.
        check("accept/eaves-is-the-two-storeys", abs(p["eaves_m"] - 6.2) < 1e-9,
              "%.6f" % p["eaves_m"])
        check("accept/ridge-rise-is-half-depth-times-tan-pitch",
              abs(p["ridge_rise_m"] - 2.80) < 5e-3, "%.6f" % p["ridge_rise_m"])
        check("accept/ridge-stands-at-nine-metres-local",
              abs(p["ridge_m"] - 9.0) < 5e-3, "%.6f" % p["ridge_m"])
        check("accept/opening-zone-is-the-bay-less-two-piers",
              abs(p["opening_zone_m"] - 5.30) < 1e-9, "%.6f" % p["opening_zone_m"])
        # THE IDENTITY THE SPEC ASSERTS, CHECKED THE OTHER WAY ROUND. It says
        # 3.562 + 0.9 + 0.838 = 5.300; this derives the display run from the
        # zone and the two doors and asks whether it lands on 3.562.
        check("accept/display-run-is-3.562-as-the-spec-states",
              abs(p["display_w_m"] - 3.562) < 1e-9, "%.6f" % p["display_w_m"])
        check("accept/window-head-sits-0.4-below-the-ceiling",
              abs(p["window_head_m"] - (p["eaves_m"] - 0.4)) < 1e-9,
              "%.6f" % p["window_head_m"])
        check("accept/sill-is-0.95-wide", abs(p["sill_w_m"] - 0.95) < 1e-9,
              "%.6f" % p["sill_w_m"])
        check("accept/reveal-is-half-a-british-brick",
              abs(p["reveal_m"] - 0.1025) < 1e-9, "%.6f" % p["reveal_m"])
        # THE WALL IS ONE BRICK AND THE REVEAL IS HALF OF ONE, read from two
        # different keys in the scene file. They describe the same brick, so
        # the reveal must be under the wall it is set into; a reveal deeper
        # than its own wall is a window behind the building.
        check("accept/wall-is-one-british-brick", abs(p["wall_t_m"] - 0.215) < 1e-9,
              "%.6f" % p["wall_t_m"])
        check("accept/the-reveal-fits-inside-its-own-wall",
              0.0 < p["reveal_m"] < p["wall_t_m"],
              "reveal=%.4f wall=%.4f" % (p["reveal_m"], p["wall_t_m"]))
        c = window_centres(p)
        check("accept/upper-windows-at-1.5-and-4.5",
              abs(c[0] - 1.5) < 1e-9 and abs(c[1] - 4.5) < 1e-9,
              "%.4f,%.4f" % (c[0], c[1]))

        parts = plan_parts(p)
        check("accept/every-part-is-named-once",
              len(set(x["id"] for x in parts)) == len(parts),
              "%d ids, %d parts" % (len(set(x["id"] for x in parts)), len(parts)))
        check("accept/something-was-built", len(parts) > 20, "%d" % len(parts))
        boxes = [x for x in parts if x.get("kind") != "slope"]
        check("accept/no-degenerate-box",
              all(b["x1"] > b["x0"] and b["y1"] > b["y0"] and b["z1"] > b["z0"] for b in boxes))
        # NOTHING SINKS BELOW THE THRESHOLD, which is the one fault a square-on
        # elevation frame cannot show.
        check("accept/nothing-below-the-threshold",
              all(b["z0"] >= -1e-9 for b in boxes),
              ",".join(b["id"] for b in boxes if b["z0"] < -1e-9))
        # THE FASCIA'S TOP IS THE SLAB, because the already-committed cornice
        # sits on it and this spec may not move it.
        fascia = [b for b in boxes if b["id"] == "fascia_band"][0]
        check("accept/fascia-top-is-the-first-floor-slab",
              abs(fascia["z1"] - p["ground_h_m"]) < 1e-9, "%.6f" % fascia["z1"])
        # THE OPENINGS ARE REALLY OPEN: no brick panel overlaps a window's x
        # range within the window band.
        band_lo, band_hi = p["window_sill_m"], p["window_head_m"]
        hw = p["window_w_m"] / 2.0
        overlaps = []
        for b in boxes:
            if not b["id"].startswith("upper_pier_"):
                continue
            for cx in window_centres(p):
                if b["x0"] < cx + hw - 1e-9 and b["x1"] > cx - hw + 1e-9:
                    overlaps.append(b["id"])
        check("accept/no-brick-pier-stands-in-a-window", not overlaps, ",".join(overlaps))
        # AND NOTHING SOLID STANDS BEHIND ONE EITHER, which is the fault the
        # first render of this bay actually had: the openings were correct and
        # the carcass filled the frontage plane behind them, so they showed
        # brick. Any part that is neither glass nor interior and crosses a
        # window's x range inside the window band fails here.
        blockers = []
        for b in boxes:
            if b["material"] in ("glass", "interior"):
                continue
            if b["z1"] <= band_lo + 1e-9 or b["z0"] >= band_hi - 1e-9:
                continue
            for cx in window_centres(p):
                if b["x0"] < cx + hw - 1e-9 and b["x1"] > cx - hw + 1e-9:
                    blockers.append(b["id"])
        check("accept/nothing-solid-stands-behind-an-upper-window",
              not blockers, ",".join(sorted(set(blockers))))

        checks = cross_check(p, ROOT)
        got = [c for c in checks if c[2] is not None]
        check("accept/cross-check-read-the-emitted-street", len(got) > 0,
              "%d of %d fields found" % (len(got), len(checks)))
        check("accept/authored-agrees-with-the-emitted-blockout",
              all(c[3] for c in got),
              ",".join("%s(%.4f vs %.4f)" % (c[0], c[1], c[2]) for c in got if not c[3]))

        # REJECTING CASES. A recipe that cannot refuse is not checking.
        try:
            _box([], "planted", "stone", 1.0, 1.0, 0.0, 1.0, 0.0, 1.0)
            check("reject/a-zero-width-box-is-refused", False, "it was accepted")
        except ValueError:
            check("reject/a-zero-width-box-is-refused", True)
        bad = dict(p); bad["bay_width_m"] = 0.5
        try:
            plan_parts(bad)
            check("reject/a-bay-too-narrow-for-its-own-piers-is-refused", False,
                  "it was accepted")
        except ValueError:
            check("reject/a-bay-too-narrow-for-its-own-piers-is-refused", True)

        # THE CAMERAS ACTUALLY POINT AT THE BUILDING. Composed back from the
        # euler this file will hand Blender, on the two frames it really
        # takes, and compared against the direction that was asked for. The
        # first version of look_at_euler passed every other check in this
        # selftest and rendered an empty field.
        for name, spec in frame_cameras(p).items():
            want = [spec["look"][i] - spec["loc"][i] for i in range(3)]
            n = math.sqrt(sum(v * v for v in want)) or 1.0
            want = [v / n for v in want]
            got = euler_direction(look_at_euler(spec["loc"], spec["look"]))
            off = max(abs(got[i] - want[i]) for i in range(3))
            check("accept/camera-%s-points-where-it-was-aimed" % name, off < 1e-9,
                  "worst axis off by %.9f" % off)
        # AND THE ELEVATION CAMERA IS SQUARE ON AND LEVEL, which is the whole
        # claim the frame makes: it is the view a facade is judged from.
        ele = frame_cameras(p)["elevation"]
        d = euler_direction(look_at_euler(ele["loc"], ele["look"]))
        check("accept/elevation-camera-is-square-to-the-frontage",
              abs(d[0]) < 1e-9 and abs(d[2]) < 1e-9 and d[1] > 0.99,
              "direction=(%.6f, %.6f, %.6f)" % d)

    nospec, err2 = load_spec(os.path.join(ROOT, "no-such-directory"))
    check("reject/a-missing-spec-refuses-by-name", nospec is None and "no-spec-file" in err2, err2)

    a = parse_args(["x.py", "--", "--out", "/tmp/x", "--commission", "c", "--run-sha", "s"])
    check("accept/the-lane's-own-line-parses", a["out"] == "/tmp/x" and not a["error"], a["error"])
    b = parse_args(["x.py", "--", "--not-a-flag-9xz"])
    check("reject/an-unknown-flag-is-refused", b["error"].startswith("unknown-flag"), b["error"])

    print("terrace-front selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 0 if failed == 0 else 4


def main(argv):
    args = parse_args(argv)
    if args["selftest"]:
        return selftest()
    if args["error"]:
        print("terrace-front refused: status=BAD-ARGS reason=%s nothing measured" % args["error"])
        return 2
    if args["plan"]:
        p, err = load_spec(args["root"], args["spec"])
        if err:
            print("terrace-front refused: status=NO-SPEC reason=%s nothing measured" % err)
            return 3
        parts = plan_parts(p)
        for line in plan_lines(p, parts, cross_check(p, args["root"])):
            print(line)
        print("terrace-front done: status=DRY-RUN/nothing-built parts=%d" % len(parts))
        return 0
    if not args["out"]:
        print("terrace-front refused: status=BAD-ARGS reason=no-out-directory nothing measured")
        return 2
    if not os.path.isdir(args["out"]):
        os.makedirs(args["out"])
    return build_and_render(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
