#!/usr/bin/env python3
"""Meridian's street lighting column (E1_lighting_column / E2_sodium_lantern_head),
authored in Blender. THE AUTHORING LINE'S FIRST TEST, ruled by Jafar 2026-09-21:
"if a lamp column comes out right in Blender, the facades are the same method
at scale." Read the ruling in full before touching this file:
game-design/decision-2026-09-21-ruling-the-lamp-column-is-authored-and-it-is-the-authoring-lines-first-test.md

    blender --background --factory-startup --python tools/art-recipes/lighting-column.py \
        -- --out DIR --root <workspace>

WHICH SOURCES GOVERN THE FORM, AND WHY THIS DIFFERS FROM THE FIRST BRIEF. A
correction arrived mid-task, from Jafar, subordinating his own reply to the
project's own material: "its form comes from the approved in-house Hook sheet
and the period research, not from my reply, which was general knowledge
rather than our own research and could contradict it... where they are more
specific than he was, they win." Both were read directly, not taken on
report, and both are cited at the exact formal choice they govern below:

    RESEARCH: game-design/research/art-direction.md line 346, in the
      British-tells list: "sodium lanterns on swan-neck STEEL columns."
      Steel, not concrete. R-B4 (line 319) is the accent budget: a low-chroma
      street punctuated by a very small number of mandated high-chroma
      objects, "period sodium amber" named as one of three. That is why the
      column body below is near-black and only the lens is saturated.
    HOOK SHEET: production/art/atlas-01/concepts/hook.png on
      origin/art/atlas-01, the street panel, foreground column, viewed
      directly and cropped to 3x and again to 8x for the head. It is SLENDER
      and DARK (painted steel, not the thicker paler concrete), carries a
      LONG SHALLOW GENTLE swan-neck arc (not a tight quarter circle), a
      SMALL FLAT SHALLOW CANOPY head aimed down the street (not a bowl, not
      a box), lit warm amber, with NO ornament: no fluting, no ladder bar,
      no scroll, no finial.

Two consequences follow, and both are implemented, not just described:
  1. The column body is dark painted steel throughout. No concrete variant is
     authored here.
  2. THE NECK ENDPOINTS DO NOT MOVE. lantern0..3 sit at y = 4.965 m (world,
     including the street's own 0.065 m ground camber) and the shaft is
     4.7 m at 0.114 m round: production/specs/vignette-pieces.json, read
     below rather than retyped, and cross-checked against it every run so
     the authored mesh and the blockout cannot drift (see cross_check()).
     What DOES move is the ARC SHAPE between those two fixed points. The
     naive reading of the blockout's own comment ("three pitched cylinders
     on a quarter circle") is a quarter circle of radius = outreach_m. The
     authored neck instead sweeps a TRUE circular arc of a LARGER radius
     (constant, and therefore strictly lower, curvature throughout) that
     starts tangent-vertical at the shaft top and runs into a short straight
     dropper down to the exact spec-pinned lantern mount. Because curvature
     is constant along a true circle, "shallower than the naive quarter
     circle" is a closed-form fact of geometry for ANY radius bigger than
     outreach_m, not an artifact of one shipped number: see neck_arc()'s
     docstring for the proof, and the selftest checks it over a range of
     radii, not only the one shipped here. Both the authored and naive
     figures are printed every run so the difference is visible rather than
     asserted.
  3. A wall fixture seen on the same sheet, a dark conical bracket lamp with
     a wire cage guard under the Harbour Office eaves, is a DIFFERENT, real
     asset the street will need. It is named here and NOT built: see the
     queue item this recipe ships beside.

WHAT IS ALREADY DIMENSIONALLY RIGHT, READ FROM THE SPEC AND NOT RETYPED.
`production/specs/vignette-scene.json`'s `lighting.column` and
`lighting.lantern` blocks are the single source for every physical dimension
below: mounting height, base and shaft diameters, outreach, lantern box size,
the sodium colour in both linear and gamma sRGB. load_lighting_spec() reads
them at run time, `--plan` prints them, and cross_check() re-reads
`production/specs/vignette-pieces.json` and compares the four placed columns'
actual piece coordinates against what this file derives from the named
fields, so a future edit to either file is caught rather than silently
diverging. NOTHING BELOW HARDCODES A DIMENSION FROM EITHER FILE: the one
authored number that is NOT in either spec file is the neck's arc radius
ratio (NECK_ARC_RADIUS_RATIO), because no dimensioned drawing of the
reference photo exists to read a radius from, and that gap is named rather
than papered over with false precision (rule 8: an invented period detail is
worse than an admitted gap).

WHAT SHIPS UNRUN. Blender is not installed in the container this was written
in (confirmed: `python3 -c "import bpy"` raises ModuleNotFoundError here), so
every line touching `bpy` ships UNRUN and the first run on Jafar's PC is its
accepting case, exactly as Mickey's did
(tools/art-recipes/mickeys-blockout.py, read in full before writing this
file). What IS covered, and deliberately carries all the arithmetic, every
mesh's vertices and faces, and every printed string: spec loading, the
cross-check against the blockout, the circular-arc neck math and its
closed-form arc-length and curvature comparison against the naive quarter
circle, EVERY mesh's vertex and face list (box, wedge canopy, cylinder,
swept tube), a pure-Python manifoldness and outward-normal check run over
every one of them, the wear layer's areas and coverage fractions, argument
parsing, `--plan`, and the refusals. `--plan` prints the whole plan with no
Blender anywhere. The BLENDER LAYER below is kept thin and mechanical on
purpose, mirroring Mickey's docstring: it decides nothing, it only turns
already-computed vertex and face lists into bpy.data meshes and objects, so
the one class of fault Blender alone could reveal is topology this script's
own manifold check already rules out on every part, every run, without
Blender.

GEOMETRY IS BUILT THROUGH bpy.data, NEVER bpy.ops, for the same reason
Mickey's file gives: `bpy.context.window` is None in `--background` mode and
any bpy.ops call that depends on window or view-layer context raises there.
"""
import hashlib
import json
import math
import os
import sys
import time

try:
    import bpy
    import mathutils
except ImportError:  # not inside Blender: the pure layer below still imports
    bpy = None
    mathutils = None

RECIPE_STEM = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
#: Fallback only; the lane (once one exists for this recipe) passes --root
#: explicitly, exactly as mickeys-blockout.py's docstring explains for the
#: same three-dirname derivation from tools/art-recipes/.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC_REL = "production/specs/vignette-scene.json"
PIECES_REL = "production/specs/vignette-pieces.json"

AUTHORED_RES = (1600, 1100)
ENGINE_CANDIDATES = ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES")
CYCLES_FALLBACK_SAMPLES = 64

# ---------------------------------------------------------------------------
# TESSELLATION. Fixed, authored, not exposed on the command line: only --res
# is, matching mickeys-blockout.py's own "a fast check can be asked for"
# carve-out. These describe RENDER SMOOTHNESS, never a physical dimension.
# ---------------------------------------------------------------------------
CYLINDER_RADIAL_SEGMENTS = 16   # base and shaft: a round pole, cheap to smooth
NECK_TUBE_SEGMENTS = 10         # facets along the circular-arc portion
NECK_RADIAL_SEGMENTS = 8        # octagonal cross section, reads round at range

#: StreetVignette.cs Columns() (read 2026-09-21, line ~1226): neck pieces are
#: `SX = sd * 0.8` where sd is shaft_diameter_m. An authored constant in
#: version-controlled source, cited by line the way mickeys-blockout.py cites
#: its commission recipe's line numbers, not a value read off a generated
#: asset a pipeline is expected to replace (queue 416's fault class).
NECK_DIAMETER_RATIO = 0.8

#: NOT IN EITHER SPEC FILE, see the module docstring's point 2. R = ratio *
#: outreach_m. 1.5 is a clean, clearly labelled choice giving a comfortable
#: margin on both the length and curvature comparisons (arc length +18
#: percent over the arc portion alone and +120 percent once the dropper is
#: counted; curvature -33 percent) rather than a value that only barely
#: clears them; the exact figures are computed and printed every run, not
#: quoted from this comment.
NECK_ARC_RADIUS_RATIO = 1.5

#: The lantern's total height (spec lantern.height_m) is split between a
#: plain housing body and a shallow pitched canopy on top, so the OVERALL
#: bounding box still matches the spec box exactly; only the split between
#: "body" and "roof" is authored and it is named here rather than folded
#: silently into a derived number.
LANTERN_BODY_FRACTION = 0.7

#: Wear proportions, all expressed as fractions of an already spec-derived
#: dimension so they scale if the spec ever does. D53 point 5: wear is
#: authored as a separable layer so its coverage can be printed; point 2:
#: THE FLOOR HAS NO NUMBER, so nothing here claims to be a bound, only a
#: reading. Exactly the three zones the brief names and no more: rain running
#: down the shaft, road spray at the bottom, staining below the lantern.
WEAR = {
    "rain_streak": {"width_ratio_of_shaft_d": 0.35, "height_ratio_of_shaft_h": 0.85},
    "road_spray": {"height_ratio_of_base_h": 0.9, "width_ratio_of_base_circumference": 0.5},
    "lantern_drip": {"length_m": 0.16, "width_ratio_of_neck_d": 2.4},
}
#: Grime sits proud of the clean surface by this many metres so it never
#: z-fights the surface it dirties; small next to every dimension it touches.
WEAR_STANDOFF_M = 0.0015

#: Flat Principled BSDF colours, RAW, exactly mickeys-blockout.py's own
#: convention (its MATERIALS constant and _materials(), read in full before
#: writing this): these are authored choices assigned directly to Base Color,
#: not a colour-managed conversion, because converting them would be a look
#: change wearing the clothes of a correctness fix. steel_dark is the Hook
#: sheet's "slender and dark... near-black or very dark grey against the
#: sky"; grime is a desaturated brownish-black buildup colour, since no wear
#: texture is held and none is fetched (nothing is purchased).
MATERIALS = (
    ("steel_dark", (0.021, 0.021, 0.024), 0.42),
    ("grime", (0.048, 0.038, 0.032), 0.90),
)
#: The lens is emissive and carries the spec's own sodium colour rather than
#: an authored guess. linear_srgb is used because Blender's node sockets
#: store LINEAR values on a direct Python property set with no colour
#: management applied, the same reasoning mickeys-blockout.py's docstring
#: gives for assigning Base Color RAW. gamma_srgb is read too and printed
#: alongside it so a reviewer can see which triple was used and why.
LENS_EMISSION_STRENGTH = 3.0   # a Blender-side render choice, not a unitful
                                # conversion of the spec's intensity=3.2,
                                # which is a Unity light unit with no defined
                                # conversion to Blender emission strength;
                                # stated as a separate number on purpose.

#: Night point light, placed per the spec's OWN placement rule
#: ("one-point-light-0.05m-below-the-centre-of-each-emissive-piece", the
#: `lantern` block of production/specs/vignette-pieces.json), energy chosen
#: as a Blender-side render value and NOT a unit conversion of range_m /
#: intensity for the same reason as LENS_EMISSION_STRENGTH above.
NIGHT_LANTERN_LIGHT_ENERGY = 40.0
NIGHT_LANTERN_LIGHT_DROP_M = 0.05

#: overcast_day and wet_night, production/specs/vignette-scene.json
#: `conditions`, read 2026-09-21: sun_intensity, sky_intensity and the held
#: HDRI path. Applied as order-of-magnitude proxies to Blender's Sun/
#: Background strengths, not as a claimed unit conversion; the HDRI is
#: attempted and falls back to a flat colour on any failure, announced
#: either way (see _world_for_condition).
CONDITIONS = {
    "overcast_day": {"sun_on": True, "sun_intensity": 3.0, "sky_intensity": 0.7,
                      "hdri_rel": "ledger/Assets/Resources/Sky/polyhaven/belfast_open_field_2k.hdr",
                      "flat_rgba": (0.65, 0.70, 0.74, 1.0), "lanterns_on": False},
    "wet_night": {"sun_on": False, "sun_intensity": 0.0, "sky_intensity": 0.35,
                  "hdri_rel": "ledger/Assets/Resources/Sky/polyhaven/kloppenheim_04_2k.hdr",
                  "flat_rgba": (0.015, 0.016, 0.020, 1.0), "lanterns_on": True},
}

#: Two authored shots: one for silhouette and wear at range, one close on the
#: neck and lantern where the sheet's departure from a tight quarter circle
#: actually reads. Both rendered under both conditions, four frames total.
#: This is a small pilot's own camera choice, not read from a per-asset JSON:
#: there is exactly one asset here, unlike atlas-01's five-view commission.
AUTHORED_SHOTS = (
    {"id": "hero_full", "position": (-4.4, -6.6, 2.0), "target": (0.25, 0.0, 2.7),
     "lens": 32.0},
    {"id": "head_detail", "position": (0.5, -1.35, 4.35),
     "target": (0.5, 0.0, 4.9), "lens": 50.0},
)


# ---------------------------------------------------------------------------
# PURE. No bpy below this line until the marked section. Everything here
# runs in the container, under --dry-run and --plan, and under --selftest.
# ---------------------------------------------------------------------------


def _num(d, key, where):
    if key not in d:
        raise KeyError("%s missing %s" % (where, key))
    v = d[key]
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        raise TypeError("%s.%s is not numeric: %r" % (where, key, v))
    return float(v)


def load_lighting_spec(root, spec_rel=SPEC_REL):
    """(params, error). Reads ONLY lighting.column and lighting.lantern.

    Every physical dimension the geometry below uses comes from here, named
    by key so a diff of vignette-scene.json is a diff of this recipe's
    output. Refuses by name rather than raising, so a caller in the pure
    layer never needs a try/except around this.
    """
    path = os.path.join(root, spec_rel)
    if not os.path.exists(path):
        return None, "no-spec-file/%s" % path.replace(" ", "~")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, ValueError) as exc:
        return None, "unreadable-spec-json/%s" % type(exc).__name__
    lighting = raw.get("lighting")
    if not isinstance(lighting, dict):
        return None, "spec-has-no-lighting-block"
    col = lighting.get("column")
    lan = lighting.get("lantern")
    if not isinstance(col, dict):
        return None, "spec-has-no-lighting.column"
    if not isinstance(lan, dict):
        return None, "spec-has-no-lighting.lantern"
    try:
        params = {
            "mounting_height_m": _num(col, "mounting_height_m", "column"),
            "base_diameter_m": _num(col, "base_diameter_m", "column"),
            "base_height_m": _num(col, "base_height_m", "column"),
            "shaft_diameter_m": _num(col, "shaft_diameter_m", "column"),
            "outreach_m": _num(col, "outreach_m", "column"),
            "column_surface": str(col.get("surface", "")),
            "lantern_length_m": _num(lan, "length_m", "lantern"),
            "lantern_width_m": _num(lan, "width_m", "lantern"),
            "lantern_height_m": _num(lan, "height_m", "lantern"),
            "lantern_linear_srgb": [float(c) for c in lan.get("linear_srgb", [])],
            "lantern_gamma_srgb": [float(c) for c in lan.get("gamma_srgb", [])],
        }
    except (KeyError, TypeError) as exc:
        return None, "spec-field-refused/%s" % str(exc).replace(" ", "~")[:80]
    if params["mounting_height_m"] <= params["base_height_m"]:
        return None, ("degenerate-shaft/mounting_height_m=%.4f<=base_height_m=%.4f"
                      % (params["mounting_height_m"], params["base_height_m"]))
    for key in ("base_diameter_m", "base_height_m", "shaft_diameter_m",
                "outreach_m", "lantern_length_m", "lantern_width_m",
                "lantern_height_m"):
        if params[key] <= 0:
            return None, "non-positive-dimension/%s=%.6f" % (key, params[key])
    if len(params["lantern_linear_srgb"]) != 3 or len(params["lantern_gamma_srgb"]) != 3:
        return None, "lantern-colour-not-a-triple"
    params["shaft_height_m"] = params["mounting_height_m"] - params["base_height_m"]
    params["neck_diameter_m"] = params["shaft_diameter_m"] * NECK_DIAMETER_RATIO
    params["lantern_body_height_m"] = params["lantern_height_m"] * LANTERN_BODY_FRACTION
    params["lantern_roof_rise_m"] = params["lantern_height_m"] - params["lantern_body_height_m"]
    params["_path"] = path
    params["_sha256"] = hashlib.sha256(open(path, "rb").read()).hexdigest()
    return params, ""


def load_pieces(root, pieces_rel=PIECES_REL):
    """(pieces_by_name, error). column0_* and lantern0, the east-side column,
    used only as a cross-check against load_lighting_spec's derived numbers,
    never as a second source of truth."""
    path = os.path.join(root, pieces_rel)
    if not os.path.exists(path):
        return None, "no-pieces-file/%s" % path.replace(" ", "~")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, ValueError) as exc:
        return None, "unreadable-pieces-json/%s" % type(exc).__name__
    wanted = {"column0_base", "column0_shaft", "column0_neck0", "lantern0"}
    found = {}
    source_list = raw.get("pieces")
    if not isinstance(source_list, list):
        return None, "pieces-file-has-no-pieces-list/keys=%s" % ",".join(sorted(raw.keys()))
    for piece in source_list:
        name = piece.get("name")
        if name in wanted:
            found[name] = piece
    missing = wanted - set(found)
    if missing:
        return None, "pieces-missing/%s" % ",".join(sorted(missing))
    return found, ""


def cross_check(params, pieces):
    """[(label, spec_value, piece_value, agree)], entirely self-deriving: every
    number on both sides is read fresh from the two files passed in, never a
    literal pinned in this source file. This is the check queue 416 asks
    every guard to be able to pass: nothing here can be broken by doing the
    work the spec authors are expected to do (editing either file), only by
    the two files disagreeing with each other.
    """
    tol = 1e-4
    checks = []

    def eq(label, spec_v, piece_v):
        checks.append((label, spec_v, piece_v, abs(spec_v - piece_v) <= tol))

    b, s, n0, lan0 = (pieces["column0_base"], pieces["column0_shaft"],
                      pieces["column0_neck0"], pieces["lantern0"])
    eq("base_diameter_m", params["base_diameter_m"], b["sx_m"])
    eq("base_height_m", params["base_height_m"], b["sy_m"])
    eq("shaft_diameter_m", params["shaft_diameter_m"], s["sx_m"])
    eq("shaft_height_m", params["shaft_height_m"], s["sy_m"])
    eq("neck_diameter_m", params["neck_diameter_m"], n0["sx_m"])
    eq("lantern_length_m", params["lantern_length_m"], lan0["sx_m"])
    eq("lantern_height_m", params["lantern_height_m"], lan0["sy_m"])
    eq("lantern_width_m", params["lantern_width_m"], lan0["sz_m"])
    eq("outreach_m", params["outreach_m"], abs(s["z_m"] - lan0["z_m"]))
    # Ground camber at this piece, recovered rather than assumed, then used
    # to check the lantern's absolute mount height the same way: base.y is
    # the base cylinder's CENTRE (StreetVignette.cs Columns():
    # `Y = gy + bh * 0.5`), so gy = base.y - base_height/2.
    gy = b["y_m"] - params["base_height_m"] * 0.5
    expected_lantern_y = gy + params["mounting_height_m"] - params["lantern_height_m"] * 0.5
    eq("lantern_mount_absolute_y_m", expected_lantern_y, lan0["y_m"])
    agree = sum(1 for c in checks if c[3])
    return checks, agree, len(checks)


# --- the neck: a TRUE circular arc (constant curvature) plus a straight
# dropper into the exact spec-pinned lantern mount ---


def neck_arc(params, radius_ratio=NECK_ARC_RADIUS_RATIO):
    """A dict describing the neck's circular arc and its dropper.

    CONSTANT CURVATURE BY CONSTRUCTION: this is a real circle, not a spline
    whose curvature can spike between control points (an earlier draft of
    this file used a cubic Bezier here and its PEAK curvature measured
    HIGHER than the naive quarter circle despite looking gentler, because a
    Bezier's curvature is not constant and spikes exactly where two
    unaligned tangents are reconciled; that failure is why this is a circle
    instead). The arc starts tangent-vertical at the shaft top (continuing
    the shaft's own line, so there is no visible kink at that joint) and
    sweeps outward; a short straight dropper then carries it down to the
    exact spec-pinned lantern centre, because the arc's own end tangent is
    not yet horizontal at the point where it reaches outreach_m sideways (a
    consequence of requiring a vertical start over a modest sideways
    reach), and forcing it to be would require a value this pilot has no
    dimensioned source for. The dropper's own joint angle is computed and
    printed rather than hidden.

    CLOSED FORM, proved once rather than only observed on today's numbers:

        R = radius_ratio * outreach_m
        cos(sweep) = 1 - outreach_m / R
        arc_length = R * sweep
        curvature  = 1 / R                         (constant along the arc)

    For any radius_ratio > 1: R > outreach_m, so curvature = 1/R is STRICTLY
    LESS than the naive quarter circle's 1/outreach_m, always. sweep stays
    under 90 degrees for every radius_ratio the selftest exercises (1.05
    through 4.0), so the arc gets longer as R grows over that whole range;
    arc_length is printed every run rather than assumed monotonic beyond
    what is tested.
    """
    mh = params["mounting_height_m"]
    reach = params["outreach_m"]
    lantern_z = mh - params["lantern_height_m"] * 0.5
    radius = radius_ratio * reach
    cos_sweep = max(-1.0, min(1.0, 1.0 - reach / radius))
    sweep = math.acos(cos_sweep)
    arc_end_z = mh + radius * math.sin(sweep)
    dropper_length = arc_end_z - lantern_z
    tangent_at_end = (math.sin(sweep), 0.0, math.cos(sweep))
    dropper_dir = (0.0, 0.0, -1.0)
    joint_cos = max(-1.0, min(1.0, sum(a * b for a, b in zip(tangent_at_end, dropper_dir))))
    return {
        "radius_m": radius, "radius_ratio": radius_ratio,
        "sweep_deg": math.degrees(sweep), "sweep_rad": sweep,
        "arc_portion_length_m": radius * sweep,
        "curvature_per_m": 1.0 / radius,
        "arc_end_point": (reach, 0.0, arc_end_z),
        "dropper_length_m": dropper_length,
        "joint_angle_deg": math.degrees(math.acos(joint_cos)),
        "mh": mh, "reach": reach, "lantern_z": lantern_z,
    }


def neck_curve(params, arc_segments=NECK_TUBE_SEGMENTS, radius_ratio=NECK_ARC_RADIUS_RATIO):
    """neck_arc()'s dict, plus "points" (arc_segments+1 facets along the
    circle, then the dropper's far end) and "total_length_m" (arc portion
    plus dropper, the whole tube's length)."""
    neck = neck_arc(params, radius_ratio)
    radius, sweep, mh, reach = (neck["radius_m"], neck["sweep_rad"],
                                neck["mh"], neck["reach"])
    points = []
    for i in range(arc_segments + 1):
        t = sweep * i / float(arc_segments)
        points.append([radius * (1.0 - math.cos(t)), 0.0, mh + radius * math.sin(t)])
    points.append([reach, 0.0, neck["lantern_z"]])
    neck["points"] = points
    neck["total_length_m"] = neck["arc_portion_length_m"] + neck["dropper_length_m"]
    return neck


def naive_quarter_circle(params):
    """(arc_length_m, curvature_per_m) for a literal quarter circle of
    radius = outreach_m, the blockout comment's own description
    (StreetVignette.cs Columns(): "three pitched cylinders on a quarter
    circle"). The baseline this file's neck is measured against, not a claim
    about what the blockout's disjoint segment centres actually trace."""
    r = params["outreach_m"]
    return r * (math.pi / 2.0), 1.0 / r


# --- generic pure-geometry mesh builders: verts/faces only, no bpy ---


def _box_verts(cx, cy, cz, sx, sy, sz):
    """8 verts, 6 quads, centred at (cx,cy,cz). Same vertex order and face
    winding as mickeys-blockout.py's _box_mesh, reused so the winding is
    proven rather than re-derived: bottom (0,3,2,1), top (4,5,6,7), sides."""
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
    v = [(cx - hx, cy - hy, cz - hz), (cx + hx, cy - hy, cz - hz),
         (cx + hx, cy + hy, cz - hz), (cx - hx, cy + hy, cz - hz),
         (cx - hx, cy - hy, cz + hz), (cx + hx, cy - hy, cz + hz),
         (cx + hx, cy + hy, cz + hz), (cx - hx, cy + hy, cz + hz)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return [list(p) for p in v], [list(q) for q in f]


def _wedge_verts(cx, cy, z0, sx, sy, rise):
    """6 verts, 5 faces: a shallow ridge roof, footprint sx*sy at z0, ridge
    along the X (length) axis at height z0+rise. Hand-derived winding,
    verified by mesh_check below (every face outward, whole solid
    watertight) rather than trusted on sight: see selftest().
    """
    hx, hy = sx / 2.0, sy / 2.0
    v = [[cx - hx, cy - hy, z0], [cx + hx, cy - hy, z0],
         [cx + hx, cy + hy, z0], [cx - hx, cy + hy, z0],
         [cx - hx, cy, z0 + rise], [cx + hx, cy, z0 + rise]]
    f = [[0, 3, 2, 1], [0, 4, 3], [1, 2, 5], [3, 4, 5, 2], [0, 1, 5, 4]]
    return v, f


def _cyl_verts(cx, cy, z0, z1, radius, segments):
    """Capped cylinder, axis along Z, centred on (cx,cy). Two rings plus an
    n-gon fan cap at each end; radius is uniform (the spec gives one
    diameter, so no taper is authored)."""
    bottom = [[cx + radius * math.cos(2 * math.pi * i / segments),
               cy + radius * math.sin(2 * math.pi * i / segments), z0]
              for i in range(segments)]
    top = [[cx + radius * math.cos(2 * math.pi * i / segments),
            cy + radius * math.sin(2 * math.pi * i / segments), z1]
           for i in range(segments)]
    v = bottom + top
    f = []
    for i in range(segments):
        j = (i + 1) % segments
        f.append([i, j, segments + j, segments + i])
    f.append(list(reversed(range(segments))))               # bottom cap, facing -Z
    f.append([segments + i for i in range(segments)])        # top cap, facing +Z
    return v, f


def _frame(tangent):
    """(side, up): a stable perpendicular frame for a tangent that always
    lies in the local X-Z plane (Y == 0), as neck_curve's points do. Using
    world Y as the reference is safe here and ONLY here: cross(tangent, Y)
    is zero only if tangent is parallel to Y, which never happens for a
    curve confined to the X-Z plane, so there is no degenerate case to
    guard for this specific curve family."""
    tx, ty, tz = tangent
    n = math.sqrt(tx * tx + ty * ty + tz * tz)
    if n <= 0:
        return (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)
    tx, ty, tz = tx / n, ty / n, tz / n
    side = (ty * 0 - tz * 1, tz * 0 - tx * 0, tx * 1 - ty * 0)   # tangent x (0,1,0)
    sn = math.sqrt(sum(c * c for c in side))
    side = tuple(c / sn for c in side)
    up = (side[1] * tz - side[2] * ty, side[2] * tx - side[0] * tz,
          side[0] * ty - side[1] * tx)                            # side x tangent
    return side, up


def _tube_verts(points, radius, segments):
    """Swept tube through `points` (>=2), capped at both ends. Ring i uses a
    tangent estimated by central difference (forward/backward at the ends),
    framed by _frame(). Faces mirror _cyl_verts's winding convention."""
    n = len(points)
    tangents = []
    for i in range(n):
        if i == 0:
            t = [points[1][k] - points[0][k] for k in range(3)]
        elif i == n - 1:
            t = [points[n - 1][k] - points[n - 2][k] for k in range(3)]
        else:
            t = [points[i + 1][k] - points[i - 1][k] for k in range(3)]
        tangents.append(t)
    v = []
    for i in range(n):
        side, up = _frame(tangents[i])
        for s in range(segments):
            a = 2 * math.pi * s / segments
            ca, sa = math.cos(a), math.sin(a)
            v.append([points[i][k] + radius * (ca * side[k] + sa * up[k])
                      for k in range(3)])
    f = []
    for i in range(n - 1):
        base_i, base_j = i * segments, (i + 1) * segments
        for s in range(segments):
            s2 = (s + 1) % segments
            f.append([base_i + s, base_i + s2, base_j + s2, base_j + s])
    f.append(list(reversed(range(segments))))                       # start cap
    last = (n - 1) * segments
    f.append([last + s for s in range(segments)])                    # end cap
    return v, f


# --- pure-Python mesh sanity: outward normals and watertightness ---


def _face_normal_and_centroid(verts, face):
    pts = [verts[i] for i in face]
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    cz = sum(p[2] for p in pts) / len(pts)
    # Newell's method: correct for planar polygons of any vertex count,
    # unlike a single three-point cross product.
    nx = ny = nz = 0.0
    for i in range(len(pts)):
        x1, y1, z1 = pts[i]
        x2, y2, z2 = pts[(i + 1) % len(pts)]
        nx += (y1 - y2) * (z1 + z2)
        ny += (z1 - z2) * (x1 + x2)
        nz += (x1 - x2) * (y1 + y2)
    return (nx, ny, nz), (cx, cy, cz)


def mesh_check(verts, faces):
    """(manifold_ok, bad_edges, degenerate_faces, bbox). Every edge must be
    shared by EXACTLY two faces with opposite winding (the standard closed-
    manifold test); a degenerate face has a near-zero normal. This is the
    check that stands in for opening the file in Blender."""
    edge_count = {}
    degenerate = 0
    for face in faces:
        normal, _ = _face_normal_and_centroid(verts, face)
        if math.sqrt(sum(c * c for c in normal)) < 1e-12:
            degenerate += 1
        for i in range(len(face)):
            a, b = face[i], face[(i + 1) % len(face)]
            key = (a, b) if a < b else (b, a)
            direction = 1 if a < b else -1
            edge_count.setdefault(key, []).append(direction)
    bad_edges = 0
    for key, dirs in edge_count.items():
        if len(dirs) != 2 or sum(dirs) != 0:
            bad_edges += 1
    lo = [min(v[k] for v in verts) for k in range(3)]
    hi = [max(v[k] for v in verts) for k in range(3)]
    manifold_ok = bad_edges == 0 and degenerate == 0
    return manifold_ok, bad_edges, degenerate, (lo, hi)


# --- the parts list: everything the bpy layer will instantiate, unchanged ---


def build_parts(params):
    """[part, ...]. Each part: id, kind, material, verts, faces, area_m2,
    wear_of (surface name or None), note. ALL vertex and face data is final
    here; the bpy layer only creates meshes and objects from it."""
    parts = []
    mh = params["mounting_height_m"]
    bh, bd = params["base_height_m"], params["base_diameter_m"]
    sh, sd = params["shaft_height_m"], params["shaft_diameter_m"]
    reach = params["outreach_m"]
    ll, lw, lh = (params["lantern_length_m"], params["lantern_width_m"],
                  params["lantern_height_m"])
    lbh, lrr = params["lantern_body_height_m"], params["lantern_roof_rise_m"]

    v, f = _cyl_verts(0, 0, 0.0, bh, bd / 2.0, CYLINDER_RADIAL_SEGMENTS)
    parts.append({"id": "base", "kind": "cyl", "material": "steel_dark",
                  "verts": v, "faces": f,
                  "area_m2": math.pi * bd * bh, "wear_of": "base",
                  "note": "base_diameter_m/base_height_m, column.surface=%s"
                          % params["column_surface"]})

    v, f = _cyl_verts(0, 0, bh, mh, sd / 2.0, CYLINDER_RADIAL_SEGMENTS)
    parts.append({"id": "shaft", "kind": "cyl", "material": "steel_dark",
                  "verts": v, "faces": f,
                  "area_m2": math.pi * sd * sh, "wear_of": "shaft",
                  "note": "shaft_diameter_m uniform, no taper authored"})

    neck = neck_curve(params)
    v, f = _tube_verts(neck["points"], params["neck_diameter_m"] / 2.0, NECK_RADIAL_SEGMENTS)
    parts.append({"id": "neck", "kind": "tube", "material": "steel_dark",
                  "verts": v, "faces": f,
                  "area_m2": math.pi * params["neck_diameter_m"] * neck["total_length_m"],
                  "wear_of": "neck",
                  "note": "one continuous swept tube, radius_m=%.4f sweep_deg=%.2f "
                          "plus a %.4f m dropper, total_length_m=%.4f"
                          % (neck["radius_m"], neck["sweep_deg"],
                             neck["dropper_length_m"], neck["total_length_m"])})

    lz0 = mh - lh   # bottom of the whole lantern assembly (box centred at mh - lh/2)
    v, f = _box_verts(reach, 0, lz0 + lbh / 2.0, ll, lw, lbh)
    parts.append({"id": "lantern_body", "kind": "box", "material": "steel_dark",
                  "verts": v, "faces": f,
                  "area_m2": 2 * (ll + lw) * lbh + ll * lw, "wear_of": "lantern",
                  "note": "housing; length_m/width_m unchanged, height split "
                          "body=%.4f roof=%.4f of lantern_height_m=%.4f"
                          % (lbh, lrr, lh)})

    lens_l, lens_w, lens_h = ll * 0.8, lw * 0.7, 0.02
    v, f = _box_verts(reach, 0, lz0 + lens_h / 2.0, lens_l, lens_w, lens_h)
    parts.append({"id": "lantern_lens", "kind": "box", "material": "lens_amber",
                  "verts": v, "faces": f,
                  "area_m2": lens_l * lens_w, "wear_of": None,
                  "note": "recessed diffuser, flush with the housing underside, "
                          "inset so the OVERALL bounding box is unchanged"})

    v, f = _wedge_verts(reach, 0, lz0 + lbh, ll, lw, lrr)
    slope_len = math.sqrt((lw / 2.0) ** 2 + lrr ** 2)
    parts.append({"id": "lantern_roof", "kind": "wedge", "material": "steel_dark",
                  "verts": v, "faces": f,
                  "area_m2": 2 * ll * slope_len, "wear_of": "lantern",
                  "note": "shallow ridge canopy, NOT a bowl and NOT a plain box, "
                          "per the Hook sheet; ridge along the length axis"})

    photocell_r, photocell_h = 0.02, 0.025
    v, f = _cyl_verts(reach, 0, lz0 + lh, lz0 + lh + photocell_h, photocell_r, 10)
    parts.append({"id": "photocell", "kind": "cyl", "material": "steel_dark",
                  "verts": v, "faces": f, "area_m2": 0.0, "wear_of": None,
                  "note": "small functional dusk-to-dawn sensor housing, read "
                          "off the sheet's small ridge-top bump; NOT a finial, "
                          "which the ruling forbids: a finial is decorative, "
                          "this is a sensor, and it is kept deliberately tiny"})

    # --- wear, three zones, each its own object and its own material ---
    rs_w = WEAR["rain_streak"]["width_ratio_of_shaft_d"] * sd
    rs_h = WEAR["rain_streak"]["height_ratio_of_shaft_h"] * sh
    rs_r = sd / 2.0 + WEAR_STANDOFF_M
    v, f = _box_verts(rs_r, 0, bh + rs_h / 2.0, WEAR_STANDOFF_M * 2, rs_w, rs_h)
    parts.append({"id": "wear_rain_streak", "kind": "box", "material": "grime",
                  "verts": v, "faces": f, "area_m2": rs_w * rs_h, "wear_of": "shaft",
                  "note": "rain running down the shaft from the neck attachment, "
                          "on the outreach-facing (weather) side"})

    circumference = math.pi * bd
    sp_w = WEAR["road_spray"]["width_ratio_of_base_circumference"] * circumference
    sp_h = WEAR["road_spray"]["height_ratio_of_base_h"] * bh
    sp_r = bd / 2.0 + WEAR_STANDOFF_M
    v, f = _box_verts(sp_r, 0, sp_h / 2.0, WEAR_STANDOFF_M * 2, sp_w, sp_h)
    parts.append({"id": "wear_road_spray", "kind": "box", "material": "grime",
                  "verts": v, "faces": f, "area_m2": sp_w * sp_h, "wear_of": "base",
                  "note": "road spray thrown up at the base, contained within "
                          "base_height_m, no cross-surface overlap with the shaft"})

    dr_l = min(WEAR["lantern_drip"]["length_m"], neck["dropper_length_m"] * 0.9)
    dr_w = WEAR["lantern_drip"]["width_ratio_of_neck_d"] * params["neck_diameter_m"]
    dr_r = params["neck_diameter_m"] / 2.0 + WEAR_STANDOFF_M
    drip_z = (neck["arc_end_point"][2] + neck["lantern_z"]) / 2.0   # dropper midpoint
    v, f = _box_verts(reach + dr_r, 0, drip_z, WEAR_STANDOFF_M * 2, dr_w, dr_l)
    parts.append({"id": "wear_lantern_drip", "kind": "box", "material": "grime",
                  "verts": v, "faces": f, "area_m2": dr_w * dr_l, "wear_of": "neck",
                  "note": "staining below the lantern, centred on the dropper "
                          "between the arc and the housing, from drips off the fitting"})
    return parts


def wear_summary(parts):
    """{surface: {clean_area_m2, wear_area_m2, coverage}}, plus the minimum
    surface and an aggregate. D53 point 2: a surface with no wear authored on
    it prints a REAL fraction (0 over its clean area), not `nothing measured`,
    because the absence here is a scope choice this run can separate, not an
    albedo bake it cannot."""
    clean = {}
    wear = {}
    for p in parts:
        surf = p["wear_of"]
        if p["id"] not in ("lantern_lens", "photocell") and not p["id"].startswith("wear_"):
            key = "lantern" if p["id"].startswith("lantern") else p["id"]
            clean[key] = clean.get(key, 0.0) + p["area_m2"]
        if p["id"].startswith("wear_"):
            wear[surf] = wear.get(surf, 0.0) + p["area_m2"]
    surfaces = {}
    for surf, area in clean.items():
        w = wear.get(surf, 0.0)
        surfaces[surf] = {"clean_area_m2": area, "wear_area_m2": w,
                          "coverage": (w / area) if area > 0 else 0.0}
    total_clean = sum(s["clean_area_m2"] for s in surfaces.values())
    total_wear = sum(s["wear_area_m2"] for s in surfaces.values())
    minimum = min(surfaces.items(), key=lambda kv: kv[1]["coverage"])
    return surfaces, minimum, (total_wear / total_clean if total_clean > 0 else 0.0)


def build_plan(root, opts):
    """Everything decided before a single Blender call. Pure, printable."""
    params, err = load_lighting_spec(root, opts.get("spec", SPEC_REL))
    if err:
        return None, err
    pieces, perr = load_pieces(root)
    if perr:
        return None, perr
    checks, agree, total_checks = cross_check(params, pieces)
    parts = build_parts(params)
    for p in parts:
        ok, bad_edges, degenerate, bbox = mesh_check(p["verts"], p["faces"])
        p["manifold_ok"] = ok
        p["bad_edges"] = bad_edges
        p["degenerate_faces"] = degenerate
    surfaces, wear_min, wear_total = wear_summary(parts)
    neck = neck_curve(params)
    naive_len, naive_curv = naive_quarter_circle(params)
    lo = [min(min(v[k] for v in p["verts"]) for p in parts) for k in range(3)]
    hi = [max(max(v[k] for v in p["verts"]) for p in parts) for k in range(3)]
    return {
        "params": params, "pieces": pieces, "checks": checks,
        "checks_agree": agree, "checks_total": total_checks,
        "parts": parts, "surfaces": surfaces, "wear_min": wear_min,
        "wear_total": wear_total, "neck": neck,
        "neck_arc_length_m": neck["total_length_m"],
        "neck_peak_curvature_per_m": neck["curvature_per_m"],
        "naive_arc_length_m": naive_len, "naive_curvature_per_m": naive_curv,
        "bounds_lo": lo, "bounds_hi": hi,
        "objects_planned": len(parts),
    }, ""


def plan_lines(plan):
    """PER-PART AND PER-SURFACE LINES ONLY. Whole-run numbers are on the done
    line (instruments.md: never both moments under one key)."""
    lines = []
    for c in plan["checks"]:
        label, spec_v, piece_v, ok = c
        lines.append("lcCheck field=%s specValue=%.6f pieceValue=%.6f "
                     "diff=%.6f agree=%s"
                     % (label, spec_v, piece_v, abs(spec_v - piece_v),
                        "yes" if ok else "no"))
    neck = plan["neck"]
    lines.append(
        "lcNeck radius_m=%.4f radiusRatio=%.2f sweep_deg=%.2f "
        "arcPortion_m=%.4f dropperLength_m=%.4f jointAngle_deg=%.2f "
        "authoredArcTotal_m=%.4f naiveQuarterArc_m=%.4f "
        "arcLongerThanNaive=%s arcRatio=%.4f "
        "authoredCurvature_perM=%.4f naiveQuarterCurvature_perM=%.4f "
        "shallowerThanNaive=%s curvatureRatio=%.4f"
        % (neck["radius_m"], neck["radius_ratio"], neck["sweep_deg"],
           neck["arc_portion_length_m"], neck["dropper_length_m"], neck["joint_angle_deg"],
           plan["neck_arc_length_m"], plan["naive_arc_length_m"],
           "yes" if plan["neck_arc_length_m"] > plan["naive_arc_length_m"] else "no",
           plan["neck_arc_length_m"] / plan["naive_arc_length_m"],
           plan["neck_peak_curvature_per_m"], plan["naive_curvature_per_m"],
           "yes" if plan["neck_peak_curvature_per_m"] < plan["naive_curvature_per_m"] else "no",
           plan["neck_peak_curvature_per_m"] / plan["naive_curvature_per_m"]))
    for p in plan["parts"]:
        lines.append(
            "lcPart id=%s kind=%s material=%s verts=%d faces=%d area_m2=%.5f "
            "wearOf=%s manifold=%s badEdges=%d degenerateFaces=%d note=%s"
            % (p["id"], p["kind"], p["material"], len(p["verts"]), len(p["faces"]),
               p["area_m2"], p["wear_of"] or "none",
               "yes" if p["manifold_ok"] else "no", p["bad_edges"],
               p["degenerate_faces"], p["note"].replace(" ", "~")[:140]))
    for surf, s in sorted(plan["surfaces"].items()):
        lines.append(
            "lcWear surface=%s cleanArea_m2=%.5f wearArea_m2=%.5f "
            "wearCoverage=%.6f"
            % (surf, s["clean_area_m2"], s["wear_area_m2"], s["coverage"]))
    return lines


def done_line(plan, opts, built, frames, status, seconds):
    total_shots = len(AUTHORED_SHOTS)
    conditions = sorted(CONDITIONS.keys())
    wrote = sum(1 for f in frames if f["bytes"] > 0)
    wrote_token = ("%d/%d" % (wrote, total_shots * len(conditions)) if frames
                  else "0/%d-no-frame-attempted" % (total_shots * len(conditions)))
    manifold_all = sum(1 for p in plan["parts"] if p["manifold_ok"])
    lo, hi = plan["bounds_lo"], plan["bounds_hi"]
    extent = "%.3f/%.3f/%.3f" % (hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])
    wmin_surf, wmin_val = plan["wear_min"][0], plan["wear_min"][1]["coverage"]
    return (
        "%s done: status=%s runSha=%s studioSha=%s "
        "specSha256=%s specPath=%s "
        "crossCheckAgree=%d/%d "
        "objectsPlanned=%d objectsBuilt=%s manifoldParts=%d/%d "
        "neckArcLonger=%s neckShallower=%s "
        "wearCoverageMin=%.6f/%s wearCoverageTotal=%.6f "
        "boundsExtent_m=%s "
        "previewsWrote=%s "
        "engineAsked=%s engineUsed=%s res=%dx%d "
        "outDir=%s root=%s elapsedSeconds=%.1f"
        % (RECIPE_STEM, status, opts["run_sha"], opts["studio_sha"],
           plan["params"]["_sha256"][:16],
           os.path.relpath(plan["params"]["_path"], opts["root"]).replace(" ", "~"),
           plan["checks_agree"], plan["checks_total"],
           plan["objects_planned"],
           "%d/%d-planned" % (built["objects"], plan["objects_planned"]) if built
           else "0/%d-planned-nothing-built" % plan["objects_planned"],
           manifold_all, len(plan["parts"]),
           "yes" if plan["neck_arc_length_m"] > plan["naive_arc_length_m"] else "no",
           "yes" if plan["neck_peak_curvature_per_m"] < plan["naive_curvature_per_m"] else "no",
           wmin_val, wmin_surf, plan["wear_total"],
           extent, wrote_token,
           opts["engine"], (sorted({f["engine"] for f in frames}) or ["not-reached"])[0]
           if frames else "not-reached",
           opts["res"][0], opts["res"][1],
           (opts["out"] or "none/dry-run").replace(" ", "~"),
           opts["root"].replace(" ", "~"), seconds))


def verdict_text(plan, opts, built, frames, status, seconds, now=None):
    stamp = int(now if now is not None else time.time())
    lines = [
        "artPreviewVerdict=1 commit=%s recipe=%s status=%s at=%d"
        % (opts["run_sha"], RECIPE_STEM, status, stamp),
        "",
        "The authoring line's first test (Jafar, 2026-09-21). Read this file",
        "instead of the job log. A run that measured nothing says NO RUN.",
        "",
    ]
    lines.extend(plan_lines(plan))
    for frame in frames:
        lines.append(
            "lcFrame idx=%d/%d id=%s condition=%s png=%s bytes=%d engine=%s "
            "renderSeconds=%.1f"
            % (frame["index"] + 1, len(frames), frame["id"], frame["condition"],
               frame["png"], frame["bytes"], frame["engine"], frame["seconds"]))
    for note in (built or {}).get("notes", []):
        lines.append("lcNote " + note)
    if not frames:
        lines.append("NO RUN - no frame was rendered on this commit.")
    lines.append(done_line(plan, opts, built, frames, status, seconds))
    return "\n".join(lines) + "\n"


def refusal_verdict(opts, reason, now=None):
    stamp = int(now if now is not None else time.time())
    return ("artPreviewVerdict=1 commit=%s recipe=%s status=NO-RUN at=%d\n\n"
            "NO RUN - the recipe refused before any frame was rendered.\n"
            "%s refused: status=NO-RUN reason=%s root=%s outDir=%s "
            "previewsWrote=0/0-shots-reached nothing measured\n"
            % (opts["run_sha"], RECIPE_STEM, stamp, RECIPE_STEM, reason,
               opts["root"].replace(" ", "~"), (opts["out"] or "none").replace(" ", "~")))


def receipt_dict(plan, opts, built, frames, status, seconds):
    return {
        "schema": "ledger.art-preview.receipt/1",
        "status": status, "recipe": RECIPE_STEM,
        "run_sha": opts["run_sha"], "studio_sha": opts["studio_sha"],
        "blender_version": built["blender_version"] if built else "not-run",
        "spec_sha256": plan["params"]["_sha256"],
        "cross_check_agree": "%d/%d" % (plan["checks_agree"], plan["checks_total"]),
        "objects_planned": plan["objects_planned"],
        "objects_built": built["objects"] if built else 0,
        "wear_coverage_by_surface": {k: round(v["coverage"], 6)
                                     for k, v in plan["surfaces"].items()},
        "frames": [{"id": f["id"], "condition": f["condition"], "png": f["png"],
                    "bytes": f["bytes"], "seconds": round(f["seconds"], 2),
                    "engine": f["engine"]} for f in frames],
        "elapsed_seconds": round(seconds, 1),
        "scope": "authored geometry and materials; no engine export, no runtime verification",
    }


def parse_args(argv):
    args = list(argv)
    if "--" in args:
        args = args[args.index("--") + 1:]
    else:
        args = args[1:] if args and args[0].endswith(".py") else args
    out = {"out": "", "root": ROOT, "spec": SPEC_REL, "res": AUTHORED_RES,
           "engine": "AUTO", "samples": 0, "run_sha": "not-passed",
           "studio_sha": "not-passed", "blend": True, "dry_run": False,
           "selftest": False, "plan": False, "error": ""}
    i = 0

    def need(flag):
        if i + 1 >= len(args):
            out["error"] = "flag-without-a-value/" + flag
            return None
        return args[i + 1]

    while i < len(args):
        a = args[i]
        if a in ("--out", "--output-dir"):
            v = need(a)
            if v is None:
                break
            out["out"] = v
            i += 2
        elif a == "--root":
            v = need(a)
            if v is None:
                break
            out["root"] = v
            i += 2
        elif a == "--spec":
            v = need(a)
            if v is None:
                break
            out["spec"] = v
            i += 2
        elif a == "--run-sha":
            v = need(a)
            if v is None:
                break
            out["run_sha"] = v.replace(" ", "~")
            i += 2
        elif a == "--studio-sha":
            v = need(a)
            if v is None:
                break
            out["studio_sha"] = v.replace(" ", "~")
            i += 2
        elif a == "--res":
            v = need(a)
            if v is None:
                break
            try:
                w, h = v.lower().split("x")
                out["res"] = (int(w), int(h))
            except ValueError:
                out["error"] = "res-is-not-WxH/" + v
                break
            if min(out["res"]) <= 0:
                out["error"] = "res-is-not-positive/" + v
                break
            i += 2
        elif a == "--engine":
            v = need(a)
            if v is None:
                break
            if v.upper() not in ("AUTO", "EEVEE", "CYCLES"):
                out["error"] = "engine-is-not-AUTO-or-EEVEE-or-CYCLES/" + v
                break
            out["engine"] = v.upper()
            i += 2
        elif a == "--samples":
            v = need(a)
            if v is None:
                break
            try:
                out["samples"] = int(v)
            except ValueError:
                out["error"] = "samples-is-not-an-integer/" + v
                break
            i += 2
        elif a == "--no-blend":
            out["blend"] = False
            i += 1
        elif a == "--dry-run":
            out["dry_run"] = True
            i += 1
        elif a == "--plan":
            out["plan"] = True
            out["dry_run"] = True
            i += 1
        elif a == "--selftest":
            out["selftest"] = True
            i += 1
        else:
            out["error"] = "unknown-flag/" + a.replace(" ", "~")
            break
    if not out["error"] and not out["out"] and not out["dry_run"] and not out["selftest"]:
        out["error"] = "missing-flag/--out"
    return out


# ---------------------------------------------------------------------------
# SELFTEST. Accepting case FIRST, against the live tree: this repository's
# own production/specs files are the accepting fixture, exactly as
# .claude/rules/instruments.md asks. NO EXPECTED VALUE BELOW IS A CONSTANT
# READ OFF A LIVE FILE (queue 416's fault class): every comparison either
# re-reads the same file fresh at test time, or checks a structural
# invariant of this file's own code (winding, manifoldness, a closed-form
# geometric proof over a RANGE of ratios) that holds regardless of what the
# spec says. Rejecting fixtures are synthetic paths and malformed JSON that
# exist nowhere in this repo.
# ---------------------------------------------------------------------------


def selftest(root):
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    # --- accepting case: the live spec and pieces files ---
    params, err = load_lighting_spec(root)
    check("accept/spec-loads", not err, err)
    if not err:
        with open(params["_path"], encoding="utf-8") as fh:
            fresh = json.load(fh)["lighting"]["column"]
        check("accept/mounting-height-matches-fresh-read",
              params["mounting_height_m"] == fresh["mounting_height_m"],
              "%.6f vs %.6f" % (params["mounting_height_m"], fresh["mounting_height_m"]))
        check("accept/shaft-height-is-mounting-minus-base",
              abs(params["shaft_height_m"] -
                  (params["mounting_height_m"] - params["base_height_m"])) < 1e-9)

        pieces, perr = load_pieces(root)
        check("accept/pieces-load", not perr, perr)
        if not perr:
            checks, agree, total = cross_check(params, pieces)
            check("accept/cross-check-all-agree", agree == total,
                  "%d/%d, %s" % (agree, total,
                                 ",".join(c[0] for c in checks if not c[3])))

        parts = build_parts(params)
        check("accept/parts-nonempty", len(parts) >= 8, "n=%d" % len(parts))
        for p in parts:
            ok, bad_edges, degenerate, bbox = mesh_check(p["verts"], p["faces"])
            check("accept/manifold/%s" % p["id"], ok,
                  "badEdges=%d degenerate=%d" % (bad_edges, degenerate))
        wv, wf = _wedge_verts(0, 0, 0, 2.0, 1.0, 0.3)
        expect_axis = [(2, -1), (0, -1), (0, 1), (1, 1), (1, -1)]  # (axis, sign)
        wedge_ok = True
        for face, (axis, sign) in zip(wf, expect_axis):
            normal, _ = _face_normal_and_centroid(wv, face)
            if (normal[axis] > 0) != (sign > 0):
                wedge_ok = False
        check("accept/wedge-face-winding-matches-construction", wedge_ok)

        surfaces, wear_min, wear_total = wear_summary(parts)
        check("accept/every-surface-has-a-coverage-fraction",
              all(0.0 <= s["coverage"] <= 1.0 for s in surfaces.values()),
              str({k: round(v["coverage"], 4) for k, v in surfaces.items()}))
        check("accept/lantern-is-the-minimum-wear-surface-by-design",
              wear_min[0] == "lantern", wear_min[0])

        neck = neck_curve(params)
        naive_len, naive_curv = naive_quarter_circle(params)
        check("accept/authored-neck-longer-than-naive-quarter-circle",
              neck["total_length_m"] > naive_len,
              "%.4f vs %.4f" % (neck["total_length_m"], naive_len))
        check("accept/authored-neck-shallower-than-naive-quarter-circle",
              neck["curvature_per_m"] < naive_curv,
              "%.4f vs %.4f" % (neck["curvature_per_m"], naive_curv))
        check("accept/neck-starts-exactly-at-shaft-top",
              neck["points"][0] == [0.0, 0.0, params["mounting_height_m"]])
        check("accept/neck-ends-exactly-at-spec-lantern-mount",
              abs(neck["points"][-1][0] - params["outreach_m"]) < 1e-9 and
              abs(neck["points"][-1][2] - (params["mounting_height_m"]
                                           - params["lantern_height_m"] * 0.5)) < 1e-9)

        # THE CLOSED-FORM PROOF, exercised over a RANGE the shipped
        # NECK_ARC_RADIUS_RATIO (1.5) sits inside, not only at that one
        # value: this is the check that would have caught the earlier
        # Bezier draft's failure before it was ever printed.
        all_shallower = all(neck_arc(params, k)["curvature_per_m"] < naive_curv
                            for k in (1.05, 1.2, 1.5, 2.0, 3.0, 4.0))
        check("accept/shallower-holds-for-every-radius-ratio-above-one", all_shallower)
        sweeps_under_90 = all(neck_arc(params, k)["sweep_deg"] < 90.0
                              for k in (1.05, 1.2, 1.5, 2.0, 3.0, 4.0))
        check("accept/sweep-stays-under-90-degrees-over-tested-ratios", sweeps_under_90)

        plan, plan_err = build_plan(root, {"spec": SPEC_REL})
        check("accept/build-plan-succeeds", not plan_err, plan_err)
        if not plan_err:
            lines = plan_lines(plan)
            check("accept/plan-lines-nonempty-and-no-spaces-in-values",
                  len(lines) > 0 and all(
                      " " not in tok.split("=", 1)[1] for ln in lines
                      for tok in ln.split() if "=" in tok),
                  "n=%d" % len(lines))

    # --- argument parsing: happy path and refusals ---
    ok_args = parse_args(["x.py", "--", "--out", "/tmp/x", "--root", root,
                          "--run-sha", "abc123"])
    check("args/happy-path", not ok_args["error"], ok_args["error"])
    check("args/missing-out-refused",
          parse_args(["x.py", "--"])["error"] == "missing-flag/--out")
    check("args/unknown-flag-refused",
          parse_args(["x.py", "--", "--wat"])["error"].startswith("unknown-flag/"))
    check("args/bad-res-refused",
          parse_args(["x.py", "--", "--out", "o", "--res", "nope"])["error"]
          .startswith("res-is-not-WxH/"))
    check("args/zero-res-refused",
          parse_args(["x.py", "--", "--out", "o", "--res", "0x10"])["error"]
          .startswith("res-is-not-positive/"))
    check("args/bad-engine-refused",
          parse_args(["x.py", "--", "--out", "o", "--engine", "POVRAY"])["error"]
          .startswith("engine-is-not-"))
    check("args/dry-run-needs-no-out",
          parse_args(["x.py", "--", "--dry-run"])["error"] == "")

    # --- rejecting fixtures: synthetic, exist nowhere in this repo ---
    check("reject/missing-spec-file",
          load_lighting_spec(root, "production/specs/does-not-exist-9xz.json")[1]
          .startswith("no-spec-file/"))
    check("reject/missing-pieces-file",
          load_pieces("/tmp/definitely-not-a-real-root-9xz")[1]
          .startswith("no-pieces-file/"))

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        specdir = os.path.join(td, "production", "specs")
        os.makedirs(specdir)

        def write_spec(obj):
            path = os.path.join(specdir, "vignette-scene.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(obj, fh)
            return load_lighting_spec(td)

        check("reject/no-lighting-block", write_spec({})[1] == "spec-has-no-lighting-block")
        check("reject/no-column", write_spec({"lighting": {"lantern": {}}})[1]
              == "spec-has-no-lighting.column")
        check("reject/missing-required-field",
              write_spec({"lighting": {"column": {"mounting_height_m": 5.0},
                                       "lantern": {"length_m": 1, "width_m": 1,
                                                    "height_m": 1,
                                                    "linear_srgb": [1, 1, 1],
                                                    "gamma_srgb": [1, 1, 1]}}})[1]
              .startswith("spec-field-refused/"))
        check("reject/non-positive-dimension",
              write_spec({"lighting": {
                  "column": {"mounting_height_m": 5.0, "base_diameter_m": 0.2,
                             "base_height_m": 0.3, "shaft_diameter_m": 0.114,
                             "outreach_m": -0.1},
                  "lantern": {"length_m": 0.55, "width_m": 0.3, "height_m": 0.2,
                             "linear_srgb": [1, 1, 1], "gamma_srgb": [1, 1, 1]}}})[1]
              .startswith("non-positive-dimension/"))
        check("reject/degenerate-shaft",
              write_spec({"lighting": {
                  "column": {"mounting_height_m": 0.2, "base_diameter_m": 0.2,
                             "base_height_m": 0.3, "shaft_diameter_m": 0.114,
                             "outreach_m": 0.5},
                  "lantern": {"length_m": 0.55, "width_m": 0.3, "height_m": 0.2,
                             "linear_srgb": [1, 1, 1], "gamma_srgb": [1, 1, 1]}}})[1]
              .startswith("degenerate-shaft/"))

    # --- mesh helper sanity on non-authored inputs, catching a general bug
    # class rather than only this asset's own numbers ---
    for radius in (0.05, 0.5, 1.3):
        v, f = _cyl_verts(0, 0, 0, 1.0, radius, 12)
        ok, bad_edges, deg, _ = mesh_check(v, f)
        check("mesh/cylinder-manifold/r=%.2f" % radius, ok,
              "badEdges=%d degenerate=%d" % (bad_edges, deg))
    for n in (2, 3, 6):
        pts = [[0.1 * i, 0.0, 0.2 * i * i] for i in range(n)]
        v, f = _tube_verts(pts, 0.05, 8)
        ok, bad_edges, deg, _ = mesh_check(v, f)
        check("mesh/tube-manifold/points=%d" % n, ok,
              "badEdges=%d degenerate=%d" % (bad_edges, deg))
    v, f = _box_verts(0, 0, 0, 1, 2, 3)
    ok, bad_edges, deg, _ = mesh_check(v, f)
    check("mesh/box-manifold", ok, "badEdges=%d degenerate=%d" % (bad_edges, deg))

    passed = sum(1 for _, ok, _ in results if ok)
    return passed, len(results), [(n, d) for n, ok, d in results if not ok]


# ---------------------------------------------------------------------------
# THE BLENDER LAYER. Every line below touches bpy and ships UNRUN from the
# container this was written in. Thin and mechanical on purpose, mirroring
# mickeys-blockout.py: it decides nothing, it instantiates the verts/faces
# the pure layer already computed and mesh_check() already validated.
# ---------------------------------------------------------------------------


def _require_bpy():
    if bpy is None:
        raise RuntimeError("no-bpy")


def _clear_scene():
    _require_bpy()
    scene = bpy.context.scene
    before = len(bpy.data.objects)
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    scene.name = "LightingColumn"
    return scene, before - len(bpy.data.objects), before


def _materials():
    _require_bpy()
    made = {}
    for name, rgb, rough in MATERIALS:
        mat = bpy.data.materials.new("LC_" + name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is not None:
            bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1)
            bsdf.inputs["Roughness"].default_value = rough
        made[name] = mat
    lens = bpy.data.materials.new("LC_lens_amber")
    lens.use_nodes = True
    nt = lens.node_tree
    emission = nt.nodes.new("ShaderNodeEmission")
    made["lens_amber"] = lens
    made["_lens_node"] = emission
    made["_lens_nodetree"] = nt
    return made


def _finish_lens_material(materials, linear_srgb):
    _require_bpy()
    nt = materials["_lens_nodetree"]
    emission = materials["_lens_node"]
    emission.inputs["Color"].default_value = (linear_srgb[0], linear_srgb[1],
                                               linear_srgb[2], 1.0)
    emission.inputs["Strength"].default_value = LENS_EMISSION_STRENGTH
    output = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    if output is not None:
        nt.links.new(emission.outputs["Emission"], output.inputs["Surface"])


def _mesh_from_part(part):
    _require_bpy()
    mesh = bpy.data.meshes.new("LC_" + part["id"])
    mesh.from_pydata(part["verts"], [], part["faces"])
    mesh.update()
    return mesh


def _add_part(part, materials, collection):
    _require_bpy()
    obj = bpy.data.objects.new("LC_" + part["id"], _mesh_from_part(part))
    collection.objects.link(obj)
    mat = materials.get(part["material"])
    if mat is not None:
        obj.data.materials.append(mat)
    obj["bom"] = ("E2_sodium_lantern_head" if part["id"].startswith("lantern")
                 else "E1_lighting_column")
    obj["wear_layer"] = part["id"].startswith("wear_")
    obj["wear_of"] = part["wear_of"] or "none"
    obj["status"] = "authored geometry; engine export unverified"
    return obj


def _resolve_engine(scene, asked):
    _require_bpy()
    notes = []
    try:
        offered = [item.identifier for item in
                   scene.render.bl_rna.properties["engine"].enum_items]
    except Exception as exc:
        offered = []
        notes.append("engineEnumUnreadable=%s" % type(exc).__name__)
    wanted = (["CYCLES"] if asked == "CYCLES"
             else [e for e in ENGINE_CANDIDATES if e != "CYCLES"] if asked == "EEVEE"
             else list(ENGINE_CANDIDATES))
    for name in wanted:
        if offered and name not in offered:
            continue
        try:
            scene.render.engine = name
        except (TypeError, ValueError):
            notes.append("engineRefused=%s" % name)
            continue
        if scene.render.engine == name:
            return name, offered, notes
    return scene.render.engine, offered, notes + ["engineNoneOffered"]


def _configure_render(scene, opts, engine):
    _require_bpy()
    scene.render.resolution_x, scene.render.resolution_y = opts["res"]
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    if engine == "CYCLES":
        want = opts["samples"] or CYCLES_FALLBACK_SAMPLES
        try:
            scene.cycles.samples = want
            scene.cycles.use_denoising = True
        except AttributeError:
            pass
    elif opts["samples"]:
        try:
            scene.eevee.taa_render_samples = opts["samples"]
        except AttributeError:
            pass


def _world_for_condition(condition, root):
    """(world, note). Tries the held HDRI first (already fetched, not a new
    purchase: ledger/Assets/Resources/Sky/polyhaven/*), falls back to a flat
    colour on any failure, always returning a usable world and saying which
    it used."""
    _require_bpy()
    cond = CONDITIONS[condition]
    world = bpy.data.worlds.new("LC_World_" + condition)
    world.use_nodes = True
    background = world.node_tree.nodes.get("Background")
    hdri_path = os.path.join(root, cond["hdri_rel"])
    note = "noBackgroundNode"
    if background is not None:
        if os.path.exists(hdri_path):
            try:
                img = bpy.data.images.load(hdri_path)
                env = world.node_tree.nodes.new("ShaderNodeTexEnvironment")
                env.image = img
                world.node_tree.links.new(env.outputs["Color"], background.inputs["Color"])
                background.inputs["Strength"].default_value = cond["sky_intensity"]
                return world, "hdri=%s" % cond["hdri_rel"]
            except Exception as exc:
                note = "hdriLoadFailed=%s/fellBackToFlat" % type(exc).__name__
        else:
            note = "hdriNotFound/fellBackToFlat"
        background.inputs["Color"].default_value = cond["flat_rgba"]
        background.inputs["Strength"].default_value = cond["sky_intensity"]
    return world, note


def _add_sun(scene, condition):
    _require_bpy()
    cond = CONDITIONS[condition]
    light = bpy.data.lights.new("LC_Sun_" + condition, "SUN")
    light.energy = cond["sun_intensity"]
    obj = bpy.data.objects.new("LC_Sun_" + condition, light)
    scene.collection.objects.link(obj)
    obj.rotation_euler = (math.radians(55), 0, math.radians(205 - 90))
    obj.hide_render = not cond["sun_on"]
    return obj


def _add_lantern_lights(scene, plan, condition):
    """One point light for the one lantern authored here, dropped 0.05 m
    below the lens centre, per the spec's own `lantern.placement` field:
    "one-point-light-0.05m-below-the-centre-of-each-emissive-piece"
    (production/specs/vignette-pieces.json, top-level `lantern` block).
    Only added for conditions where the spec's own condition flag says
    lanterns are on."""
    _require_bpy()
    if not CONDITIONS[condition]["lanterns_on"]:
        return 0
    reach = plan["params"]["outreach_m"]
    mh = plan["params"]["mounting_height_m"]
    lh = plan["params"]["lantern_height_m"]
    lens_z = (mh - lh * 0.5) - NIGHT_LANTERN_LIGHT_DROP_M
    light = bpy.data.lights.new("LC_LanternLight", "POINT")
    light.energy = NIGHT_LANTERN_LIGHT_ENERGY
    light.color = plan["params"]["lantern_linear_srgb"]
    obj = bpy.data.objects.new("LC_LanternLight", light)
    scene.collection.objects.link(obj)
    obj.location = (reach, 0, lens_z)
    return 1


def _add_camera(shot, scene):
    _require_bpy()
    data = bpy.data.cameras.new(shot["id"])
    data.lens = shot["lens"]
    data.clip_end = 200.0
    obj = bpy.data.objects.new("LC_CAM_" + shot["id"], data)
    scene.collection.objects.link(obj)
    obj.location = shot["position"]
    direction = (mathutils.Vector(shot["target"]) - mathutils.Vector(shot["position"]))
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return obj


def _render_to(scene, path):
    _require_bpy()
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def _build(plan, materials, collection):
    _require_bpy()
    objects = 0
    for part in plan["parts"]:
        _add_part(part, materials, collection)
        objects += 1
    _finish_lens_material(materials, plan["params"]["lantern_linear_srgb"])
    return {"objects": objects}


def main(argv):
    started = time.time()
    opts = parse_args(argv)
    if opts["error"]:
        print("%s refused: status=BAD-ARGS reason=%s nothing measured"
              % (RECIPE_STEM, opts["error"]))
        return 2
    opts["root"] = os.path.abspath(opts["root"])

    if opts["selftest"]:
        passed, total, failures = selftest(opts["root"])
        for name, detail in failures:
            print("%s selftest FAIL %s: %s" % (RECIPE_STEM, name, detail))
        print("%s selftest done: passed=%d/%d failures=%d"
              % (RECIPE_STEM, passed, total, len(failures)))
        return 0 if passed == total else 3

    plan, err = build_plan(opts["root"], opts)
    if err:
        print("%s refused: status=NO-SPEC-DATA reason=%s root=%s "
              "previewsWrote=0/0-shots-reached nothing measured"
              % (RECIPE_STEM, err, opts["root"]))
        if opts["out"]:
            _write_refusal(opts, err)
        return 3
    for line in plan_lines(plan):
        print(line)
    if opts["dry_run"]:
        print(done_line(plan, opts, None, [],
                        "PLAN/nothing-built-and-nothing-measured" if opts["plan"]
                        else "DRY-RUN/nothing-built-and-nothing-measured",
                        time.time() - started))
        return 0
    if bpy is None:
        print("%s refused: status=NO-BPY reason=run-me-through-blender-not-python "
              "nothing measured" % RECIPE_STEM)
        return 6

    out_dir = os.path.abspath(opts["out"])
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print("%s refused: status=NO-OUTDIR reason=%s nothing measured"
              % (RECIPE_STEM, type(exc).__name__))
        return 7

    scene, removed, before = _clear_scene()
    notes = ["sceneReset=dataApi/removed=%d/%d-objects" % (removed, before)]
    collection = bpy.data.collections.new("LC_Column")
    scene.collection.children.link(collection)
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1
    materials = _materials()
    built = _build(plan, materials, collection)
    print("lcBuild objectsBuilt=%d/%d-planned elapsedSeconds=%.1f"
          % (built["objects"], plan["objects_planned"], time.time() - started))

    engine, offered, engine_notes = _resolve_engine(scene, opts["engine"])
    notes.extend(engine_notes)
    _configure_render(scene, opts, engine)
    built["blender_version"] = bpy.app.version_string.replace(" ", "~")

    frames = []
    for condition in sorted(CONDITIONS.keys()):
        world, world_note = _world_for_condition(condition, opts["root"])
        scene.world = world
        notes.append("world/%s=%s" % (condition, world_note))
        _add_sun(scene, condition)
        lit = _add_lantern_lights(scene, plan, condition)
        for shot in AUTHORED_SHOTS:
            cam = _add_camera(shot, scene)
            scene.camera = cam
            png = "%s-%s-%s.png" % (RECIPE_STEM, condition, shot["id"])
            path = os.path.join(out_dir, png)
            t0 = time.time()
            _render_to(scene, path)
            took = time.time() - t0
            size = os.path.getsize(path) if os.path.exists(path) else 0
            used = engine
            if size == 0 and engine != "CYCLES" and opts["engine"] == "AUTO":
                notes.append("engineFellBack=%s..CYCLES/shot=%s/%s"
                             % (engine, shot["id"], condition))
                engine, _, more = _resolve_engine(scene, "CYCLES")
                notes.extend(more)
                _configure_render(scene, opts, engine)
                t0 = time.time()
                _render_to(scene, path)
                took += time.time() - t0
                size = os.path.getsize(path) if os.path.exists(path) else 0
                used = engine
            frames.append({"index": len(frames), "id": shot["id"], "condition": condition,
                           "png": png, "bytes": size, "seconds": took, "engine": used})
            print("lcFrame idx=%d id=%s condition=%s png=%s bytes=%d engine=%s "
                  "renderSeconds=%.1f lanternLightsAdded=%d"
                  % (len(frames), shot["id"], condition, png, size, used, took, lit))

    built["blend_bytes"] = "not-asked/--no-blend"
    if opts["blend"]:
        blend = os.path.join(out_dir, RECIPE_STEM + ".blend")
        try:
            bpy.ops.wm.save_as_mainfile(filepath=blend)
            built["blend_bytes"] = str(os.path.getsize(blend) if os.path.exists(blend) else 0)
        except Exception as exc:
            built["blend_bytes"] = "save-refused/" + type(exc).__name__
            notes.append("blendNotSaved=%s" % type(exc).__name__)
    built["notes"] = notes

    wrote = sum(1 for f in frames if f["bytes"] > 0)
    status = "RAN" if wrote == len(frames) and frames else "PARTIAL"
    seconds = time.time() - started
    _write_verdict(plan, opts, built, frames, status, seconds, out_dir)
    for note in notes:
        print("lcNote " + note)
    print(done_line(plan, opts, built, frames, status, seconds))
    return 0 if wrote == len(frames) else 8


def _write_verdict(plan, opts, built, frames, status, seconds, out_dir):
    text = verdict_text(plan, opts, built, frames, status, seconds)
    path = os.path.join(out_dir, RECIPE_STEM + "-verdict.txt")
    try:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        size = os.path.getsize(path)
    except OSError as exc:
        print("%s note: verdictNotWritten=%s" % (RECIPE_STEM, type(exc).__name__))
        return
    print("%s verdict: path=%s bytes=%d lines=%d"
          % (RECIPE_STEM, path.replace(" ", "~"), size, text.count("\n")))
    receipt = os.path.join(out_dir, "receipt.json")
    try:
        with open(receipt, "w", encoding="utf-8") as handle:
            json.dump(receipt_dict(plan, opts, built, frames, status, seconds),
                      handle, indent=2)
            handle.write("\n")
    except OSError as exc:
        print("%s note: receiptNotWritten=%s" % (RECIPE_STEM, type(exc).__name__))


def _write_refusal(opts, reason):
    out_dir = os.path.abspath(opts["out"])
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, RECIPE_STEM + "-verdict.txt")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(refusal_verdict(opts, reason))
        print("%s verdict: path=%s status=NO-RUN" % (RECIPE_STEM, path.replace(" ", "~")))
    except OSError as exc:
        print("%s note: verdictNotWritten=%s" % (RECIPE_STEM, type(exc).__name__))


if __name__ == "__main__" or bpy is not None:
    sys.exit(main(sys.argv))
