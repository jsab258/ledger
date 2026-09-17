"""Import ONE body and ONE animation clip to uassets, from a script, in CI.

    UnrealEditor-Cmd.exe LedgerProbe.uproject -run=pythonscript \
        -script="tools/ue/import_figure.py" -unattended -nopause -nosplash
    python3 tools/ue/import_figure.py --selftest   # runs without Unreal
    python3 tools/ue/import_figure.py --measure    # container half only

WHY IT EXISTS, and it is the same reason tools/ue/import_prop_meshes.py and
tools/ue/make_base_material.py exist, stated there in full. A skeletal mesh
asset is a cooked package, the FBX importer that makes one is EDITOR ONLY,
and a packaged game can only place meshes that already exist as assets. So
the figure is a BUILD PRODUCT, made by a script that runs in the cook step,
never by a human in an editor.

WHAT IT MAKES, all under /Game/Ledger/Figure, which DefaultGame.ini already
carries in DirectoriesToAlwaysCook:

    SK_michelle           the skeletal mesh, from ledger/Assets/Characters/
                          Michelle.fbx
    SK_michelle_Skeleton  the skeleton the importer derives from it
    A_michelle_idle_2     the anim sequence, from the clip FBX, bound to that
                          skeleton

WHICH BODY AND WHY. Michelle is one of the four the project picked for
itself (tools/mixamo-pick/fetch_bodies.py names michelle, remy, sophie,
shae), she is tracked in git, she is CLOTHED AND SKINNED rather than one of
the two grey mannequins (X Bot and Y Bot, which are excluded on sight), and
she is an ADULT. D18 forbids children anywhere, in the crowd or rendered, so
that last clause is not a style note: it is checked as a MEASUREMENT here
rather than assumed from a name, and figureD18 on the line carries the body
name beside its measured height in centimetres.

WHICH CLIP AND WHY. B/idle_2__Standing Idle 01: the figure stands on a
footway under a lamp, so the clip has to be a person STANDING. The two
nearby alternatives were considered and refused for reasons that are
measurable rather than aesthetic: lean_wall (Leaning On A Wall) needs a wall
at a hand's distance and this placement has none, so the figure would lean
on air; walk_old and carry_bag are locomotion, and a locomotion clip frozen
at one time is a person caught mid-stride with no motion blur and no
displacement, which reads as a statue rather than a person.

THE HEIGHT IS THE NUMBER THIS WHOLE SCRIPT IS FOR. A Mixamo FBX and an
Unreal scene disagree about units, and the two failure modes are a figure a
hundred times too large and a figure a hundred times too small. Neither is a
rendering opinion and neither needs a frame to diagnose: both are
arithmetic, and the frame cannot tell you WHICH without the number. So the
height is measured TWICE and both readings go on the line:

  1. IN THIS CONTAINER, off the FBX's own bytes. fbx_geometry_bounds() walks
     the binary FBX node tree, inflates every Geometry's Vertices array and
     takes the min and max of each axis; fbx_unit_scale() reads
     GlobalSettings' UnitScaleFactor and UpAxis. That gives the source
     height in the file's own units with no engine in the loop.
  2. ON THE RUNNER, off the asset the importer just made, through
     unreal.SkeletalMesh.get_bounds(). That is the engine's opinion, and the
     engine's opinion is a measurement: what an importer returns is not what
     its documentation says it returns until a run says so.

figureHeightRatio is the second over the first and it is the reading that
names the fault. A ratio near 1 is agreement; near 0.01 is a figure a
hundred times too small; near 100 is a figure a hundred times too large.
NOTHING IS SCALED TO FIX IT. If the ratio is wrong the import is wrong, and
scaling the actor would hide the one number that could say so.

WHAT THE EVIDENCE IS. ue-figure.txt beside the project, one key=value line,
copied into the build verdict by the workflow step, because a log tail is
not an evidence channel in this project and a committed file is. Plus
ue-figure.json for the per-asset readings that do not fit on a line.

NOTHING THIS SCRIPT DOES MAY WRITE INTO THE REPO WHEN IT IS RUN OUTSIDE THE
EDITOR. make_base_material.py carries the same _inside_unreal() discipline
because a side-effecting check once appended junk into a file shaped like
the build evidence channel on every verify run. --selftest and --measure
read; only the editor half writes, and it writes beside the uproject.

THE STATUS WORD, THE RETURN CODE AND EVERY PLACEMENT NUMBER ARE PURE
FUNCTIONS AT THE TOP OF THIS FILE, exercised by --selftest in the container
that writes them, for the reason .claude/rules/instruments.md gives as a
standing rule: a formatter written where the tests do not run ships UNRUN,
and an unrun formatter printing a plausible string is the silent-instrument
failure. The engine half supplies live state and decides nothing.
"""

import json
import math
import os
import re
import struct
import sys
import zlib

# ---- the path conventions, which are a contract with the C++ --------------

CHARACTERS_DIR = os.path.join("ledger", "Assets", "Characters")
BODY_FILE = "Michelle.fbx"
BODY_ID = "michelle"
CLIP_DIR = "B"
CLIP_FILE = "idle_2__Standing Idle 01_2dee24f8-3b49-48af-b735-c6377509eaac.fbx"
CLIP_ID = "idle_2"

PACKAGE_DIR = "/Game/Ledger/Figure"
MESH_PREFIX = "SK_"
ANIM_PREFIX = "A_"

# THE TWO GREY MANNEQUINS, EXCLUDED BY NAME. They are featureless, they are
# not people, and one of them standing in Quay Street reported as a figure is
# precisely the failure the sky dome rule exists to stop.
EXCLUDED_BODIES = ("X Bot.fbx", "Y Bot.fbx")


def mesh_name():
    return MESH_PREFIX + BODY_ID


def anim_name():
    return ANIM_PREFIX + BODY_ID + "_" + CLIP_ID


def mesh_object_path():
    """THE STRING VignetteShot.cpp LOADS. --selftest reads the C++ rather
    than trusting that the two were kept in step by hand."""
    n = mesh_name()
    return PACKAGE_DIR + "/" + n + "." + n


def anim_object_path():
    n = anim_name()
    return PACKAGE_DIR + "/" + n + "." + n


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(here))


def body_source():
    return os.path.join(CHARACTERS_DIR, BODY_FILE)


def clip_source():
    return os.path.join(CHARACTERS_DIR, CLIP_DIR, CLIP_FILE)


# ---- THE STREET, AS THE BRIEF STATES IT, IN METRES ------------------------
#
# Every number in this block is a description of the street that already
# exists, not a decision this file makes. The decisions are below it, in
# placement_series(), and each one is derived from these.
STREET_LENGTH_M = 42.0
CARRIAGEWAY_Z_M = 3.0          # the carriageway runs z = -3.0 .. +3.0
FOOTWAY_WIDTH_M = 2.0          # a footway outside each kerb
KERB_UPSTAND_M = 0.125         # the footway surface sits this far above z=0
LANTERN_HEAD_Y_M = 4.96
# (x, z) of each lantern. East is +z.
LANTERNS_M = ((8.0, 3.23), (18.0, -3.23), (28.0, 3.23), (38.0, -3.23))
# cam_A: east footway, looking down +x.
CAM_A_X_M = 4.0
CAM_A_Z_M = 4.0
CAM_A_EYE_M = 1.6
CAM_A_FOV_V_DEG = 60.0
# The east footway's centre line, which is also cam_A's own z.
EAST_FOOTWAY_MID_Z_M = CARRIAGEWAY_Z_M + FOOTWAY_WIDTH_M * 0.5

# A STANDING ADULT'S TORSO, used only to ask where the light comes FROM.
# It is not a height claim about the body: the body's height is MEASURED,
# twice, and printed. This is the height of the surface the backlight has to
# graze for the figure to read as a silhouette rather than as a top-lit
# shape, and 1.0 m is chest height on any adult.
TORSO_Y_M = 1.0

# ---- THE THREE CONSTRAINTS THE PLACEMENT IS DERIVED UNDER -----------------
#
# EVERY ONE IS THE FIRST VALUE OF A SERIES and says so on the line
# (figurePlacementBound). No frame has been seen. They are written down
# BEFORE the search rather than fitted to its answer, which is the only
# thing that makes the search a derivation instead of a preference.
#
# 1. THE BACKLIGHT MUST BE BEHIND, NOT ABOVE. A lamp head 4.96 m up and 2 m
#    away is 63 degrees above the torso, which is top light: it lands on the
#    head and shoulders and leaves the body dark against a dark street, and
#    the picture is a shape, not a person. 35 degrees is the first bound and
#    it is a geometric one, not a taste one: below it the light is mostly
#    along the street rather than down it.
MAX_BACKLIGHT_ELEVATION_DEG = 35.0
# 2. THE FIGURE MUST BE FAR ENOUGH TO STAND IN THE FRAME AND NEAR ENOUGH TO
#    HAVE PIXELS. At cam_A's 60 degree vertical field a frame is 1.1547d tall,
#    so a 1.7 m figure is 177 px of 720 (25%) at 6 m and 53 px (7%) at 20 m.
#    THOSE ARE figure_height_px's OWN NUMBERS, corrected 2026-09-16 from the 28%
#    and 8% written here first, which no function in this file ever printed. Both bounds are printed beside
#    the chosen one as figureHeightPx so the next run can move them off a
#    measured picture rather than off this comment.
MIN_CAM_DISTANCE_M = 6.0
MAX_CAM_DISTANCE_M = 20.0
# 3. AND IT STANDS ON THE FOOTWAY, on the camera's own side, so that the
#    ground under it is the ground the camera stands on and the lit pool
#    behind it is along the footway rather than across the carriageway.
#
# 4. AND SOMETHING MUST BE ABLE TO SEE IT. QUEUE 379. Run 53 chose x=17.5 on
#    the backlight term alone and stood the figure behind the telephone
#    kiosk: 461 of the 5460 pixels inside its own projected box differed
#    from the same rectangle before the figure existed, 8 per cent of its
#    own bounds. The search had no term for whether anything was in the way,
#    so it could not see the kiosk. This is that term, and the numbers below
#    are what it reads.
#
#    IT IS A MAXIMAND AND NOT A GATE, WHICH IS MEASURED RATHER THAN
#    PREFERRED: of the 25 admissible candidates on the east footway centre
#    line, ZERO are fully clear. The shop awning at x=12 has its underside
#    at 1.628 m and clips the head of everything beyond it, and the public
#    bin at x=8 clips the near shin of everything before it. A constraint
#    demanding a clear body would have chosen nothing at all, so the search
#    MAXIMISES what is visible and the backlight ratio decides between
#    positions that are equally visible. That order is a decision and it is
#    named here: Jafar's sentence is that a person is standing in the
#    street, and a silhouette nobody can see is not one.
#
#    THE BODY IS A NOMINAL STANDING ADULT BOX and not the asset. The asset's
#    height is measured, twice, and printed (figureHeightCm); this box is
#    the thing the rays are cast at, 0.60 m across and 1.70 m tall, which is
#    wider than a posed adult and so reads a little MORE occlusion than the
#    body will suffer. Every number it produces is the first value of a
#    series and says so.
BODY_BOX_W_M = 0.60
BODY_BOX_H_M = 1.70
# THE SAMPLE GRID, AND ITS DENOMINATOR IS PRINTED EVERYWHERE THE COUNT IS.
# 5 columns across the body by 9 levels up it, from 5 to 95 per cent of the
# height, is 45 rays. This is a SAMPLED PROXY for the fraction of the figure
# the camera can see and it is not a pixel measurement: FigureNow in
# VignetteShot.cpp measures the pixels, and this exists to choose a position
# before any frame exists.
OCCLUSION_RAY_COLS = 5
OCCLUSION_RAY_ROWS = 9


def deg(rad):
    return rad * 180.0 / math.pi


def backlight_reading(fx, fz, cam_x=CAM_A_X_M, cam_z=CAM_A_Z_M):
    """Where the light on a figure at (fx, fz) comes FROM, per lamp.

    Returns (back, front, dominant) where back and front are lists of
    (lamp index, horizontal separation m, 3D distance m, elevation deg) and
    dominant is the nearest BACK lamp or None.

    A lamp is BEHIND the figure when it is further from the camera along the
    camera-to-figure direction, which is the only sense of "behind" that
    matters for a silhouette: the camera, the figure and the lamp in that
    order along one ray. A lamp with a negative dot product is in FRONT and
    lights the side of the figure the camera can see, which is the thing
    that destroys a silhouette.
    """
    vx, vz = fx - cam_x, fz - cam_z
    vlen = math.hypot(vx, vz)
    if vlen <= 0.0:
        return [], [], None
    vx, vz = vx / vlen, vz / vlen
    back, front = [], []
    for i, (lx, lz) in enumerate(LANTERNS_M):
        dx, dz = lx - fx, lz - fz
        s = math.hypot(dx, dz)
        dy = LANTERN_HEAD_Y_M - TORSO_Y_M
        r = math.hypot(s, dy)
        elev = deg(math.atan2(dy, s)) if s > 0 else 90.0
        row = (i, s, r, elev)
        (back if (dx * vx + dz * vz) > 0.0 else front).append(row)
    dominant = min(back, key=lambda r: r[2]) if back else None
    return back, front, dominant


def silhouette_ratio(back, front):
    """How much more light reaches the figure from BEHIND than from in
    FRONT, as a ratio of inverse-square terms.

    THIS IS THE SILHOUETTE, AS A NUMBER. FigureReadsAsSilhouette in
    FrameStats.h asks the same question of the PIXELS (is the core darker
    than the ring); this asks it of the GEOMETRY, before any frame exists,
    so that the placement is derived rather than tuned to a picture nobody
    has seen. Above 1 means the backlight wins.

    It is a RATIO OF IRRADIANCE TERMS, not a luminance and not a prediction
    of any pixel: every lamp is the same fixture at the same intensity, so
    the intensity cancels and only 1/r^2 is left. Nothing here knows what the
    tonemapper will do with it.
    """
    b = sum(1.0 / (r[2] * r[2]) for r in back)
    f = sum(1.0 / (r[2] * r[2]) for r in front)
    if f <= 0.0:
        return None if b <= 0.0 else float("inf")
    return b / f


def _chosen_blocker(place):
    """WHAT IS MOST IN THE WAY AT THE CHOSEN POSITION, named, so a placement
    that is 43 of 45 clear says WHICH prop takes the other two."""
    if place is None:
        return "nothing-measured"
    _c, _t, name, count = clear_reading(place[0], place[1])
    return "%s:%d" % (name, count)


def _pieces_path():
    return os.path.join(repo_root(), "production", "specs",
                        "vignette-pieces.json")


def _piece_box(p):
    """ONE PIECE AS AN AXIS-ALIGNED WORLD BOX, in the file's own frame
    (x along the street, y up, z across, sizes FULL and the position the
    CENTRE), which is the frame every number in this file is already in.

    A yaw of 90 or 270 swaps the two horizontal sizes exactly; any other
    non-zero yaw gives the AABB of the rotated footprint, which is LARGER
    than the piece. Pitch and roll are ignored for the same reason and with
    the same sign: this over-reads occlusion rather than under-reading it,
    and an over-read costs a position, while an under-read costs a frame
    nobody can see a person in.
    """
    yaw = float(p.get("yaw_deg") or 0.0) % 180.0
    sx, sz = float(p["sx_m"]), float(p["sz_m"])
    if abs(yaw - 90.0) < 1e-9:
        sx, sz = sz, sx
    elif yaw > 1e-9:
        c, sn = abs(math.cos(math.radians(yaw))), abs(math.sin(math.radians(yaw)))
        sx, sz = sx * c + sz * sn, sx * sn + sz * c
    x, y, z = float(p["x_m"]), float(p["y_m"]), float(p["z_m"])
    sy = float(p["sy_m"])
    return (x - sx / 2.0, x + sx / 2.0,
            y - sy / 2.0, y + sy / 2.0,
            z - sz / 2.0, z + sz / 2.0)


_OCCLUDERS = None


def occluders():
    """EVERY PIECE OF THE SCENE, AS BOXES, OUT OF THE ONE JSON THE SCENE IS
    BUILT FROM. Returns (boxes, note); boxes is a list of (name, aabb) and
    the note names the file, the count and what was skipped.

    NOTHING IS EXCLUDED BY NAME. The kerbs, the ground planes and the
    shopfronts are all in the list, because a term that only knows about the
    obstacles somebody remembered is the term run 53 already had. Decals are
    the one omission and they are counted out loud: they are zero-thickness
    cards lying ON surfaces that are themselves in the list, so counting
    them would count the same obstruction twice and would let a stain on a
    wall block a ray.

    A missing file is not an empty scene: it returns no boxes and a note
    that says nothing was measured, and every reading downstream then prints
    the words rather than a plausible zero.
    """
    global _OCCLUDERS
    if _OCCLUDERS is not None:
        return _OCCLUDERS
    path = _pieces_path()
    if not os.path.exists(path):
        _OCCLUDERS = ([], "nothing-measured/no-vignette-pieces.json-at/"
                          + path.replace(" ", "_"))
        return _OCCLUDERS
    try:
        with open(path, "r", encoding="utf-8") as f:
            doc = json.load(f)
        pieces = doc.get("pieces") or []
    except (ValueError, OSError) as exc:
        _OCCLUDERS = ([], "nothing-measured/unreadable/%s"
                          % str(exc)[:60].replace(" ", "_"))
        return _OCCLUDERS
    boxes, decals = [], 0
    for p in pieces:
        if p.get("shape") == "decal":
            decals += 1
            continue
        boxes.append((str(p.get("name", "unnamed")), _piece_box(p)))
    _OCCLUDERS = (boxes, "vignette-pieces.json/boxes=%d/decalsSkipped=%d/of=%d"
                         % (len(boxes), decals, len(pieces)))
    return _OCCLUDERS


def _ray_hits_box(o, d, b):
    """The slab test, over the SEGMENT from the eye to the sample point
    (t in 0..1) and not over an infinite ray: a box behind the body is not
    in front of it."""
    lo, hi = 0.0, 1.0
    for i in range(3):
        a, bb = b[2 * i], b[2 * i + 1]
        if abs(d[i]) < 1e-12:
            if o[i] < a or o[i] > bb:
                return False
            continue
        t1, t2 = (a - o[i]) / d[i], (bb - o[i]) / d[i]
        if t1 > t2:
            t1, t2 = t2, t1
        lo, hi = max(lo, t1), min(hi, t2)
        if lo > hi:
            return False
    return True


_CLEAR_CACHE = {}


def clear_reading(fx, fz, cam_x=CAM_A_X_M, cam_z=CAM_A_Z_M,
                  cam_eye_m=CAM_A_EYE_M):
    """HOW MUCH OF A BODY AT (fx, fz) CAM_A CAN ACTUALLY SEE, as a count of
    unblocked sample rays over the count cast.

    Returns (clear, total, worst_name, worst_count). clear is None and total
    is 0 when there is no scene to test against, which prints the words
    nothing measured rather than a clear body nobody looked at.

    IT IS CAM_A'S READING AND SAYS SO. The other two terms of this search are
    cam_A's as well (the distance band is cam_A's field of view and BEHIND is
    behind as cam_A sees it), so a fourth term taken from a different camera
    would be a different question answered in the same tuple.
    """
    key = (round(fx, 4), round(fz, 4), round(cam_x, 4), round(cam_z, 4),
           round(cam_eye_m, 4))
    if key in _CLEAR_CACHE:
        return _CLEAR_CACHE[key]
    boxes, _note = occluders()
    if not boxes:
        out = (None, 0, "nothing-measured", 0)
        _CLEAR_CACHE[key] = out
        return out
    # ONLY WHAT LIES BETWEEN THEM CAN BE IN THE WAY. A box entirely behind
    # the camera or entirely beyond the body cannot be crossed by a segment
    # that runs from one to the other, and dropping those is exact rather
    # than approximate: x increases monotonically along the segment.
    x0, x1 = (cam_x, fx) if cam_x <= fx else (fx, cam_x)
    near = [b for b in boxes if b[1][1] >= x0 and b[1][0] <= x1]
    o = (cam_x, cam_eye_m, cam_z)
    foot = footway_top_m()
    clear, worst = 0, {}
    total = OCCLUSION_RAY_COLS * OCCLUSION_RAY_ROWS
    for i in range(OCCLUSION_RAY_COLS):
        z = fz + BODY_BOX_W_M * (i / (OCCLUSION_RAY_COLS - 1.0) - 0.5)
        for j in range(OCCLUSION_RAY_ROWS):
            y = foot + BODY_BOX_H_M * (0.05 + 0.90 * j
                                       / (OCCLUSION_RAY_ROWS - 1.0))
            d = (fx - o[0], y - o[1], z - o[2])
            blocker = None
            for name, box in near:
                if _ray_hits_box(o, d, box):
                    blocker = name
                    break
            if blocker is None:
                clear += 1
            else:
                worst[blocker] = worst.get(blocker, 0) + 1
    if worst:
        name, count = max(worst.items(), key=lambda kv: (kv[1], kv[0]))
    else:
        name, count = "none", 0
    out = (clear, total, name, count)
    _CLEAR_CACHE[key] = out
    return out


def figure_height_px(dist_m, height_m, frame_h=720,
                     fov_v_deg=CAM_A_FOV_V_DEG):
    """How tall a figure of height_m stands in the frame at dist_m, in
    pixels. A small-angle-free version: the frame is 2*d*tan(fov/2) metres
    tall at that distance."""
    if dist_m <= 0.0:
        return 0.0
    frame_m = 2.0 * dist_m * math.tan(math.radians(fov_v_deg * 0.5))
    if frame_m <= 0.0:
        return 0.0
    return frame_h * height_m / frame_m


def placement_series(z=EAST_FOOTWAY_MID_Z_M, lo=6.0, hi=32.0, step=0.5):
    """EVERY CANDIDATE POSITION ALONG THE EAST FOOTWAY, SCORED, IN ORDER.

    This is the printed series rule taken literally: the bound (which x) is
    read off a series this function produces rather than typed into the C++
    from an opinion. --measure prints it whole; --selftest asserts that the
    constant VignetteShot.cpp actually carries is this function's argmax, so
    the C++ and the derivation cannot drift apart in silence.

    A row is (x, ratio, cam distance, dominant back lamp elevation,
    admissible, why-not, clear rays, rays cast, worst blocker). Admissible
    is the three constraints above; the last three are the fourth term,
    which is a MAXIMAND and not part of admissible, because no admissible
    candidate on this line is fully clear and a gate would choose nothing.
    """
    rows = []
    n = int(round((hi - lo) / step))
    for i in range(n + 1):
        x = lo + i * step
        d = math.hypot(x - CAM_A_X_M, z - CAM_A_Z_M)
        back, front, dom = backlight_reading(x, z)
        ratio = silhouette_ratio(back, front)
        why = []
        if dom is None:
            why.append("no-lamp-behind")
        elif dom[3] > MAX_BACKLIGHT_ELEVATION_DEG:
            why.append("backlight-is-overhead")
        if d < MIN_CAM_DISTANCE_M:
            why.append("too-near-the-camera")
        if d > MAX_CAM_DISTANCE_M:
            why.append("too-far-from-the-camera")
        if ratio is None:
            why.append("no-lamp-at-all")
        clear, cast, blocker, blocked = clear_reading(x, z)
        rows.append((round(x, 3),
                     None if ratio is None else round(ratio, 4),
                     round(d, 4),
                     None if dom is None else round(dom[3], 3),
                     not why,
                     "/".join(why) if why else "admissible",
                     clear, cast,
                     "%s:%d" % (blocker, blocked)))
    return rows


def placement_key(row):
    """THE ORDER THE SEARCH CHOOSES IN, as one named function, so the rule
    can be exercised on rows nobody measured and so there is exactly one
    place it is written down.

    (clear rays, backlight ratio, nearer camera), lexicographically, largest
    first. Visibility outranks the silhouette: run 53 put a figure with the
    best backlight score on the street with 4 of its 45 rays reaching the
    camera, and a person nobody can see is not the thing being built. Among
    equally visible positions the backlight ratio still decides, which is
    the term this file was written for and it still does work: at 40 of 45
    clear there are eight tied positions and the ratio separates them.

    A row whose occlusion could not be read sorts as -1, which ties every
    such row and leaves the ratio deciding: the old behaviour exactly, under
    a note that says nothing was measured.
    """
    clear = -1 if row[6] is None else row[6]
    return (clear, row[1], -row[2])


def chosen_placement(rows=None):
    """The one position, and it is the argmax of the series above under
    placement_key.

    Returns (x, z, ratio, cam distance, elevation, clear rays, rays cast) or
    None when NOTHING is admissible, which is a real answer and not a crash:
    a street whose lamps moved could have no silhouette position at all, and
    this must say so rather than return the least bad one.

    THE ANSWER SITS EXACTLY ON THE NEAR DISTANCE BOUND and that is said out
    loud rather than left for a reader to notice: x=10.0 is 6.00 m from
    cam_A and MIN_CAM_DISTANCE_M is 6.0, so the bound is load-bearing for
    this choice. The window between that bound and the awning that clips the
    head from x=10.5 on is one grid step wide. Move either and the answer
    moves, which is what the printed series is for.
    """
    rows = placement_series() if rows is None else rows
    ok = [r for r in rows if r[4] and r[1] is not None]
    if not ok:
        return None
    best = max(ok, key=placement_key)
    return (best[0], EAST_FOOTWAY_MID_Z_M, best[1], best[2], best[3],
            best[6], best[7])


def footway_top_m():
    """The surface the figure's FEET sit on. The kerb upstand is the whole
    of it: the carriageway is y=0 and the footway is one kerb above."""
    return KERB_UPSTAND_M


# ---- WHERE IN THE CLIP THE POSE IS FROZEN ---------------------------------
#
# A FRACTION AND NOT A TIME IN SECONDS, so it cannot overrun a clip whose
# duration nothing here has measured, and so the same number means the same
# thing for any clip. 0.35 IS THE FIRST VALUE OF A SERIES: it is away from
# t=0, where a Mixamo clip often sits close to the neutral pose the mesh was
# bound in, and away from the loop point. The resolved time in seconds is
# printed beside the clip's measured duration so the next run can move it off
# a frame rather than off this comment.
POSE_FRACTION = 0.35


def pose_time_s(duration_s, fraction=POSE_FRACTION):
    """The time the single-node instance is frozen at, in seconds, clamped
    into the clip. A duration that was never measured gives 0.0 rather than
    a plausible number, because a time computed from nothing is the unrun
    formatter failure."""
    try:
        d = float(duration_s)
    except (TypeError, ValueError):
        return 0.0
    if not (d > 0.0):
        return 0.0
    t = d * float(fraction)
    return max(0.0, min(t, d))


# ---- THE HEIGHT VERDICT, WHICH IS WHAT THIS SCRIPT IS FOR -----------------

HEIGHT_AGREES = "AGREES"
HEIGHT_HUNDRED_SMALL = "A-HUNDRED-TIMES-TOO-SMALL"
HEIGHT_HUNDRED_LARGE = "A-HUNDRED-TIMES-TOO-LARGE"
HEIGHT_DISAGREES = "DISAGREES"
HEIGHT_UNMEASURED = "nothing-measured"


def height_verdict(engine_cm, source_cm):
    """One word for the two height readings, taken from their RATIO.

    THE BANDS ARE DECADES AND NOT A TUNED THRESHOLD, which matters because
    rule 2 forbids a bound nobody has measured. This does not ask whether a
    figure is the right height; it asks which of two ARITHMETIC faults
    happened, and those two are a factor of 100 apart in opposite
    directions. A half-to-double band cannot be crossed by a units error and
    cannot separate two bodies of different height, which is the point: the
    reading that judges the figure is the frame.

    Either side unmeasured is the WORD nothing-measured, never a ratio of 0.
    """
    try:
        e, s = float(engine_cm), float(source_cm)
    except (TypeError, ValueError):
        return HEIGHT_UNMEASURED, None
    if not (e > 0.0) or not (s > 0.0):
        return HEIGHT_UNMEASURED, None
    ratio = e / s
    if 0.5 <= ratio <= 2.0:
        return HEIGHT_AGREES, ratio
    if 0.005 <= ratio <= 0.02:
        return HEIGHT_HUNDRED_SMALL, ratio
    if 50.0 <= ratio <= 200.0:
        return HEIGHT_HUNDRED_LARGE, ratio
    return HEIGHT_DISAGREES, ratio


# ---- the status word and the return code ----------------------------------

STATUS_IMPORTED = "IMPORTED"
STATUS_NO_SOURCES = "NO-SOURCES"
STATUS_NO_MESH = "NO-SKELETAL-MESH"
STATUS_NO_SKIN = "MESH-BUT-NO-SKIN"
STATUS_SKIN_UNMEASURED = "MESH-SKIN-NOT-MEASURED"
STATUS_NO_ANIM = "MESH-BUT-NO-ANIM"
STATUS_NOT_SAVED = "NOT-SAVED"
# THE WORD FOR A RAISE THAT GOT PAST EVERY _try. It is already the word in
# this channel: make_base_material.py's except clause writes
# figureImportStatus=RAISED when this script's main() throws. Defining it
# HERE, in the layer --selftest runs in, means the raise still produces a
# WHOLE figure line (paths, placement, source height, the lot) instead of the
# two-key stub that clause can manage, and means one word is spelt in one
# place instead of two.
STATUS_RAISED = "RAISED"

# ---- THE SKIN IS THREE OUTCOMES AND NOT TWO -------------------------------
#
# RUN 54 IS WHY THIS FUNCTION EXISTS. Every vertex-count route this script
# knew raised on UE 5.8 ('SkeletalMesh' object has no attribute
# 'get_num_vertices', and the same for get_num_lod_vertices), _try caught
# both and returned None, figureSkinVerts printed the words nothing-measured
# HONESTLY, and then the status line turned that None into MESH-BUT-NO-SKIN,
# which is a claim that the skin is ABSENT derived from a count that never
# happened. The same run measured 65 bones, a matching skeleton, one material
# slot and bounds 166.50 cm tall off the same asset: nothing in it said the
# skin was missing.
#
# CLAUDE.md rule 3b, in one function: a zero needs a denominator, and a
# never-ran case prints the words. A FAILED MEASUREMENT IS NOT EVIDENCE OF
# ABSENCE, so the three outcomes are three words and they never collapse into
# two.
SKIN_PRESENT = "MEASURED-PRESENT"
SKIN_ABSENT = "MEASURED-ABSENT"
SKIN_UNMEASURED = "NOT-MEASURED"


def skin_reading(skin_verts):
    """Which of the three the skin vertex count is, as one word.

    A bool is refused explicitly: isinstance(True, int) is True in Python,
    and a True arriving here would read as one vertex and then as a present
    skin, which is a plausible string standing in for a reading nobody took.
    A negative count is a reading no engine should give and is therefore not
    trusted as a zero either: it is NOT-MEASURED.
    """
    if isinstance(skin_verts, bool) or not isinstance(skin_verts, int):
        return SKIN_UNMEASURED
    if skin_verts < 0:
        return SKIN_UNMEASURED
    return SKIN_PRESENT if skin_verts > 0 else SKIN_ABSENT


def import_status(sources, mesh_loaded, skin_verts, bones, anim_loaded,
                  anim_frames, saved):
    """The one word, and every clause in it is a thing the C++ then has to
    cope with rather than a thing this script would like to be true.

    MESH-BUT-NO-SKIN MEANS A COUNT WAS TAKEN AND IT WAS ZERO. A skeletal
    mesh asset that imported with zero skinned vertices is a skeleton with
    nothing on it: it renders as nothing, or worse, as a default shape, and
    an object that cannot be dressed is worth its own word.

    MESH-SKIN-NOT-MEASURED MEANS NO COUNT WAS TAKEN AT ALL, and it is a
    different fact about the script rather than about the asset. It sits
    LAST, after the anim and the save, on purpose: a MEASURED fault
    (no anim, not saved) still wins the line, because the word should name
    the thing somebody can act on, and a missing reading only gets the line
    when everything that WAS measured passed.

    NOTHING IN THE ENGINE READS THIS WORD, checked rather than assumed on
    2026-09-17: VignetteShot.cpp builds its own GFigureState from its own
    proxy (GetRefSkeleton().GetNum(), GetMaterials().Num(), GetBounds()) and
    never parses ue-figure.txt, and no gate, workflow step or test greps for
    MESH-BUT-NO-SKIN. The sentence that used to stand here, that the C++
    destroys the actor on this word, was a comment and not a check.

    MESH-BUT-NO-ANIM is the T-pose case and it is separated for its own
    reason: a bind-pose mannequin standing in Quay Street is worse than no
    figure, because it looks plausible.
    """
    if sources < 2:
        return STATUS_NO_SOURCES
    if not mesh_loaded:
        return STATUS_NO_MESH
    if not (isinstance(bones, int) and bones > 0):
        return STATUS_NO_MESH
    skin = skin_reading(skin_verts)
    if skin == SKIN_ABSENT:
        return STATUS_NO_SKIN
    if not anim_loaded or not (isinstance(anim_frames, int) and anim_frames > 0):
        return STATUS_NO_ANIM
    if not saved:
        return STATUS_NOT_SAVED
    if skin == SKIN_UNMEASURED:
        return STATUS_SKIN_UNMEASURED
    return STATUS_IMPORTED


def import_return(status):
    """0 only for the word that means a skinned adult body and a real clip
    are both saved uassets. The verdict travels in the FILE as
    figureImportReturn; the editor process's exit code is the editor's, which
    is the pair run 19 of the material generator could not explain.

    MESH-SKIN-NOT-MEASURED RETURNS 2, and that is a deliberate choice rather
    than an oversight: 0 means PROVEN, and an import whose skin nobody could
    count is not proven. It is NOT the same claim as a fault, and the line
    keeps the two apart under figureSkin= (MEASURED-ABSENT against
    NOT-MEASURED) so that a reader of the return code alone can never read a
    missing reading as a broken asset.
    """
    return 0 if status == STATUS_IMPORTED else 2


def flat(value):
    """No spaces in any value, ever: every reader of these files splits on
    whitespace and truncates silently."""
    return str(value).replace(" ", "~")


NOTE_CAP = 600


def note_of(report, cap=NOTE_CAP):
    """The report as ONE value, capped, AND THE CAP ANNOUNCES WHEN IT BIT.

    The cap was a bare [:600] until 2026-09-17 and it bit in silence, which
    is the one thing .claude/rules/instruments.md forbids of a cap: run 54's
    note ran to within a few characters of it while carrying the only
    description of the fault that run had. A truncated note that does not say
    it was truncated reads as a complete account of what happened.
    """
    if not report:
        return "none"
    whole = "/".join(str(x) for x in report)
    if len(whole) <= cap:
        return whole
    room = max(0, cap - 40)
    kept = whole[:room]
    dropped = len(whole) - len(kept)
    return "%s..(+%d~chars~not~shown/of=%d)" % (kept, dropped, len(whole))


def raised_line(exc, readings=None):
    """A WHOLE FIGURE LINE FOR A RAISE THAT GOT PAST EVERY _try.

    THE POINT IS THAT A FAULT IN THIS SCRIPT CANNOT COST THE RUN ITS
    EVIDENCE. Before this, a raise anywhere in run_in_unreal() outside a
    _try propagated into make_base_material.py, whose except clause could
    write two keys and a truncated message; the placement, the two heights,
    the asset paths and the body's name all went with it, and the next run
    had to rediscover them.

    It returns the same (line, manifest) pair run_in_unreal does, so the
    caller cannot tell the two apart and cannot forget to write one of them.
    """
    r = dict(readings or {})
    prior = r.get("note")
    r["note"] = note_of([x for x in (prior, "RAISED/%s/%s"
                                     % (type(exc).__name__, str(exc)[:200]))
                         if x and x != "none"])
    return figure_line(STATUS_RAISED, r), {
        "schema": "ledger.figure-import/1",
        "measuredBy": "editor",
        "raised": "%s: %s" % (type(exc).__name__, exc),
        "readings": r,
    }


def num(v, fmt="%.4f"):
    """A number, or the WORD nothing-measured. Never a zero standing in for
    a reading nobody took."""
    if v is None:
        return "nothing-measured"
    try:
        return fmt % float(v)
    except (TypeError, ValueError):
        return "nothing-measured"


def figure_line(status, readings):
    """The one line the workflow copies into the build verdict.

    Every key, in the order a reader needs them when it comes back wrong:

      figureImportStatus   the word import_status decided
      figureImportReturn   0 only for IMPORTED. THIS is the script's verdict;
                           the editor process's exit code is the editor's.
      figureBody/figureClip  which FBX each half came from, named so the
                           hand-back's claim about WHICH body stood can be
                           checked against the run rather than believed.
      figureD18            the body and its MEASURED height, because D18
                           forbids children anywhere and a name is not a
                           measurement.
      figureBones          bones in the imported skeleton. Zero is not a
                           skeleton and the status word says so.
      figureSkinVerts      vertices the skin came through with, or the WORD
                           nothing-measured when no route answered.
      figureSkin           WHICH OF THE THREE THAT WAS: MEASURED-PRESENT,
                           MEASURED-ABSENT or NOT-MEASURED. The count and
                           this word are a pair on purpose, because
                           nothing-measured and 0 are the two readings run 54
                           collapsed into one claim.
      figureSkinVia        which readback answered, or none-of-N. A fallback
                           that works silently is a fallback nobody knows
                           they depend on, and every name in that ladder is
                           a GUESS at this engine's bindings until a run
                           names the one that answered.
      figureLodsVia        the same, for the LOD count.
      figureHeightCm       THE NUMBER THIS SCRIPT EXISTS FOR, read off the
                           asset the importer made, in centimetres, which is
                           the engine's own unit.
      figureSourceCm       the same height measured in THIS CONTAINER off
                           the FBX's own vertex arrays, with the file's unit
                           scale factor and up axis beside it.
      figureHeightRatio    engine over source, and the word it decides. Near
                           1 agrees; near 0.01 or 100 is the units fault,
                           which is arithmetic and not a rendering opinion.
      figureBoundsCm       the engine's bounds in the ENGINE's axis order,
                           x/y/z, full sizes. The axis order is the
                           importer's opinion and not ours, so it is printed
                           rather than assumed.
      figureAnimFrames/figureAnimDurationS/figureAnimRate
                           the clip as the engine sees it. A clip with one
                           frame is a pose, not an animation.
      figureAnimSkeleton   WHICH skeleton the anim bound to. A Mixamo clip
                           carries its own rig, and an anim bound to a
                           skeleton that is not the body's drives nothing.
      figurePoseTimeS      where the single-node instance is frozen, from
                           POSE_FRACTION of the MEASURED duration.
      figurePlacement      the derived position, with the numbers it was
                           derived from, all first-of-series.
    """
    r = readings
    status_word = status
    hv, ratio = height_verdict(r.get("heightCm"), r.get("sourceHeightCm"))
    place = chosen_placement()
    if place is None:
        placement = "NONE-ADMISSIBLE/no-position-meets-the-three-constraints"
    else:
        clear = ("nothing-measured" if place[5] is None
                 else "%d/of=%d" % (place[5], place[6]))
        placement = ("x=%.2f/z=%.2f/footwayTopM=%.3f/camDistM=%.2f"
                     "/backlightRatio=%.2f/backlightElevDeg=%.1f"
                     "/clearRays=%s/worstBlocker=%s"
                     % (place[0], place[1], footway_top_m(), place[3],
                        place[2], place[4], clear, _chosen_blocker(place)))
    return (
        "figureImportStatus=%s figureImportReturn=%d "
        "figureBody=%s figureClip=%s "
        "figureD18=%s/adult/measuredHeightCm=%s/no-child-bodies-exist-in-this-set "
        "figureMeshPath=%s figureAnimPath=%s "
        "figureBones=%s figureSkinVerts=%s figureSkin=%s figureSkinVia=%s "
        "figureSkinStat=one-count-and-the-word-for-it"
        "/MEASURED-PRESENT..MEASURED-ABSENT..NOT-MEASURED"
        "/a-count-that-raised-is-NOT-MEASURED-and-is-never-MEASURED-ABSENT/run-54 "
        "figureMaterials=%s figureLods=%s figureLodsVia=%s "
        "figureHeightCm=%s figureSourceCm=%s figureHeightRatio=%s figureHeight=%s "
        "figureHeightStat=engine-bounds-full-size-on-the-up-axis"
        "/over-the-same-height-measured-off-the-FBX-vertex-arrays-in-the-container "
        "figureBoundsCm=%s figureBoundsOriginCm=%s "
        "figureBoundsAxisOrder=engine-x-forward/y-right/z-up/the-importers-opinion-not-ours "
        "figureFbxUnitScale=%s figureFbxUpAxis=%s figureFbxVerts=%s figureFbxGeoms=%s "
        "figureAnimFrames=%s figureAnimDurationS=%s figureAnimRate=%s "
        "figureAnimSkeleton=%s figureMeshSkeleton=%s figureSkeletonsMatch=%s "
        "figurePoseFraction=%.3f figurePoseTimeS=%s "
        "figurePlacement=%s "
        "figurePlacementStat=clear-rays-are-a-45-ray-SAMPLE-of-what-cam_A-can-see-of-a-nominal-body-box"
        "/not-a-pixel-measurement/the-pixels-are-figureSil-on-the-shot-line "
        "figurePlacementOrder=clear-rays-THEN-backlight-ratio-THEN-nearer-camera"
        "/visibility-outranks-the-silhouette/queue-379 "
        "figurePlacementBound=NONE-YET/every-number-here-is-the-first-value-of-a-series "
        "figureScalePolicy=1/never-scaled/a-wrong-height-is-a-wrong-import "
        "figureImportVia=%s figureSaved=%s figureUassetBytes=%s "
        "figureVerdictIs=figureImportReturn/not-the-editor-process-exit "
        "figureNote=%s"
        % (status_word, import_return(status_word),
           flat(BODY_FILE), flat(CLIP_FILE),
           flat(BODY_ID), num(r.get("heightCm"), "%.2f"),
           mesh_object_path(), anim_object_path(),
           num(r.get("bones"), "%d") if r.get("bones") is not None else "nothing-measured",
           num(r.get("skinVerts"), "%d") if r.get("skinVerts") is not None else "nothing-measured",
           skin_reading(r.get("skinVerts")),
           flat(r.get("skinVia", "nothing-measured")),
           num(r.get("materials"), "%d") if r.get("materials") is not None else "nothing-measured",
           num(r.get("lods"), "%d") if r.get("lods") is not None else "nothing-measured",
           flat(r.get("lodsVia", "nothing-measured")),
           num(r.get("heightCm"), "%.2f"), num(r.get("sourceHeightCm"), "%.2f"),
           num(ratio, "%.4f"), hv,
           flat(r.get("boundsCm", "nothing-measured")),
           flat(r.get("boundsOriginCm", "nothing-measured")),
           num(r.get("fbxUnitScale"), "%.4f"), flat(r.get("fbxUpAxis", "nothing-measured")),
           num(r.get("fbxVerts"), "%d") if r.get("fbxVerts") is not None else "nothing-measured",
           num(r.get("fbxGeoms"), "%d") if r.get("fbxGeoms") is not None else "nothing-measured",
           num(r.get("animFrames"), "%d") if r.get("animFrames") is not None else "nothing-measured",
           num(r.get("animDurationS"), "%.4f"), num(r.get("animRate"), "%.3f"),
           flat(r.get("animSkeleton", "nothing-measured")),
           flat(r.get("meshSkeleton", "nothing-measured")),
           flat(r.get("skeletonsMatch", "nothing-measured")),
           POSE_FRACTION, num(pose_time_s(r.get("animDurationS")), "%.4f"),
           placement,
           flat(r.get("importVia", "nothing-measured")),
           flat(r.get("saved", "nothing-measured")),
           num(r.get("uassetBytes"), "%d") if r.get("uassetBytes") is not None else "nothing-measured",
           flat(r.get("note", "none"))))


# ---- THE FBX READER: THE CONTAINER'S HALF OF THE HEIGHT --------------------
#
# A BINARY FBX IS A TREE OF NODE RECORDS and this reads exactly as much of it
# as the height needs. Header: 21 bytes of magic, two bytes, then a uint32
# version at offset 23. A node record is EndOffset, NumProperties,
# PropertyListLen (uint32 before version 7500, uint64 from it), a uint8 name
# length, the name, the properties, then nested records until a null record.
# A property is a one-byte type code and then its data; the array types
# (f d l i b) carry length, encoding and compressed length, and encoding 1 is
# a raw zlib stream.
#
# WHY NOT A LIBRARY: nothing that reads FBX is on the licence allowlist and
# nothing is purchased. This reads bytes the repository already tracks.

_ARRAY_TYPES = {"f": ("f", 4), "d": ("d", 8), "l": ("q", 8),
                "i": ("i", 4), "b": ("b", 1)}
_SCALAR_TYPES = {"Y": ("h", 2), "C": ("?", 1), "I": ("i", 4),
                 "F": ("f", 4), "D": ("d", 8), "L": ("q", 8)}


def fbx_version(data):
    """The file's own version, or None when these bytes are not a binary
    FBX. An ASCII FBX is not a binary one and must not be half-parsed into a
    plausible number."""
    if data is None or len(data) < 27:
        return None
    if not data.startswith(b"Kaydara FBX Binary"):
        return None
    return struct.unpack("<I", data[23:27])[0]


def _read_property(data, at):
    """One property. Returns (value, next offset) with value a scalar, a
    bytes, or a list for an array type. None as the value means a type this
    reader does not decode, which is refused rather than guessed at."""
    code = chr(data[at])
    at += 1
    if code in _SCALAR_TYPES:
        fmt, n = _SCALAR_TYPES[code]
        return struct.unpack("<" + fmt, data[at:at + n])[0], at + n
    if code in ("S", "R"):
        n = struct.unpack("<I", data[at:at + 4])[0]
        at += 4
        return data[at:at + n], at + n
    if code in _ARRAY_TYPES:
        fmt, size = _ARRAY_TYPES[code]
        length, encoding, comp = struct.unpack("<III", data[at:at + 12])
        at += 12
        raw = data[at:at + comp] if encoding == 1 else data[at:at + length * size]
        at += comp if encoding == 1 else length * size
        if encoding == 1:
            try:
                raw = zlib.decompress(raw)
            except zlib.error:
                return None, at
        if len(raw) < length * size:
            return None, at
        return list(struct.unpack("<%d%s" % (length, fmt), raw[:length * size])), at
    return None, None


def fbx_walk(data, want, limit=200000):
    """Every node whose name is in `want`, as (name, [properties]).

    A depth-first walk that stops at the first malformed record rather than
    guessing: a reader that recovers from garbage is a reader that invents
    numbers. `limit` is a ceiling on records visited and it ANNOUNCES ITSELF
    by returning the count beside the hits, per the standing rule that any
    cap says when it bit.
    """
    ver = fbx_version(data)
    if ver is None:
        return None, 0, False
    wide = ver >= 7500
    hdr = struct.Struct("<QQQB") if wide else struct.Struct("<IIIB")
    hits = []
    visited = [0]
    truncated = [False]

    def walk(at, end):
        while at < end:
            if visited[0] >= limit:
                truncated[0] = True
                return
            if at + hdr.size > len(data):
                return
            end_off, nprops, plen, nlen = hdr.unpack_from(data, at)
            if end_off == 0:
                return
            visited[0] += 1
            name_at = at + hdr.size
            name = data[name_at:name_at + nlen].decode("ascii", "replace")
            props_at = name_at + nlen
            props = []
            p = props_at
            if name in want:
                for _ in range(nprops):
                    if p is None or p >= len(data):
                        break
                    v, p = _read_property(data, p)
                    props.append(v)
                hits.append((name, props))
            nested = props_at + plen
            if nested < end_off <= len(data):
                walk(nested, end_off)
            at = end_off
    walk(27, len(data))
    return hits, visited[0], truncated[0]


def fbx_geometry_bounds(path):
    """The min and max of every Geometry's Vertices array in one FBX, in the
    file's own units, plus the vertex count and how many geometries there
    were.

    THIS IS THE GEOMETRY'S OWN BOUNDS AND IT IGNORES NODE TRANSFORMS, said
    here rather than discovered later. A Model node may carry a scale this
    does not apply, so this is the source's own claim about its size and not
    a prediction of what the engine will answer. The pair is the point: the
    run prints the engine's reading beside it and figureHeightRatio is the
    reading that names a units fault.

    Returns a dict, or None when the file is not a binary FBX at all.
    """
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return None
    hits, visited, truncated = fbx_walk(data, ("Vertices", "P"))
    if hits is None:
        return None
    lo = [None, None, None]
    hi = [None, None, None]
    verts = 0
    geoms = 0
    for name, props in hits:
        if name != "Vertices" or not props or not isinstance(props[0], list):
            continue
        xs = props[0]
        if len(xs) < 3:
            continue
        geoms += 1
        verts += len(xs) // 3
        for i in range(0, len(xs) - 2, 3):
            for a in range(3):
                v = xs[i + a]
                if lo[a] is None or v < lo[a]:
                    lo[a] = v
                if hi[a] is None or v > hi[a]:
                    hi[a] = v
    unit, up = None, None
    for name, props in hits:
        if name != "P" or not props or not isinstance(props[0], bytes):
            continue
        key = props[0].decode("ascii", "replace")
        if key == "UnitScaleFactor" and len(props) >= 5:
            try:
                unit = float(props[4])
            except (TypeError, ValueError):
                unit = None
        elif key == "UpAxis" and len(props) >= 5:
            try:
                up = int(props[4])
            except (TypeError, ValueError):
                up = None
    return {
        "path": path,
        "fbxVersion": fbx_version(data),
        "bytes": len(data),
        "geoms": geoms,
        "verts": verts,
        "min": lo,
        "max": hi,
        "size": [None if (lo[a] is None or hi[a] is None) else hi[a] - lo[a]
                 for a in range(3)],
        "unitScaleFactor": unit,
        "upAxisIndex": up,
        "recordsVisited": visited,
        "recordCapBit": truncated,
    }


def source_height_cm(stats):
    """The source's height in CENTIMETRES, and which axis it was taken on.

    THE UP AXIS IS READ OUT OF THE FILE, not assumed: GlobalSettings' UpAxis
    is 0 for x, 1 for y and 2 for z, and Mixamo writes y-up while Unreal is
    z-up, which is exactly the kind of assumption that costs a round trip.
    A file that does not say gets the LONGEST axis, which is the right guess
    for a standing human and is NAMED as a guess in the returned via.

    UnitScaleFactor is centimetres per unit: 1.0 is a file in centimetres,
    2.54 is inches, 100.0 is metres. Applied, and printed, so a units fault
    has two places to show rather than one.
    """
    if not stats or not stats.get("size"):
        return None, "nothing-measured"
    size = stats["size"]
    if all(v is None for v in size):
        return None, "no-vertices-read"
    up = stats.get("upAxisIndex")
    if up in (0, 1, 2) and size[up] is not None:
        axis, via = up, "upAxis-from-GlobalSettings"
    else:
        axis = max((a for a in range(3) if size[a] is not None),
                   key=lambda a: size[a])
        via = "longest-axis-GUESSED-no-UpAxis-in-the-file"
    scale = stats.get("unitScaleFactor")
    if scale is None or not (scale > 0):
        scale, via = 1.0, via + "/unitScaleFactor-absent-assumed-1"
    return size[axis] * scale, via + "/axis=%d" % axis


# ---- the container half: what can be measured here, printed ---------------


def measure_only():
    """The container's half of every reading this script takes, printed and
    written nowhere. Nothing under the repository is touched."""
    root = repo_root()
    rc = 0
    for label, rel in (("body", body_source()), ("clip", clip_source())):
        path = os.path.join(root, rel)
        print("%s: %s" % (label, rel))
        if not os.path.exists(path):
            print("  NOTHING MEASURED: not on disk")
            rc = 2
            continue
        st = fbx_geometry_bounds(path)
        if st is None:
            print("  NOTHING MEASURED: not a binary FBX")
            rc = 2
            continue
        h, via = source_height_cm(st)
        print("  fbxVersion=%s bytes=%d geoms=%d verts=%d records=%d capBit=%s"
              % (st["fbxVersion"], st["bytes"], st["geoms"], st["verts"],
                 st["recordsVisited"], st["recordCapBit"]))
        print("  unitScaleFactor=%s upAxisIndex=%s"
              % (st["unitScaleFactor"], st["upAxisIndex"]))
        print("  size(file units)=%s" % ([None if v is None else round(v, 4)
                                          for v in st["size"]],))
        print("  heightCm=%s via=%s" % (None if h is None else round(h, 3), via))
    print("")
    print("placement series over the east footway centre line, z=%.2f, "
          "x from 6.0 to 32.0 by 0.5:" % EAST_FOOTWAY_MID_Z_M)
    print("  %6s %10s %8s %9s %11s  %s"
          % ("x", "ratio", "camDist", "backElev", "clear/cast", "why"))
    for row in placement_series():
        print("  %6.2f %10s %8.2f %9s %11s  %s"
              % (row[0], "inf" if row[1] == float("inf") else row[1],
                 row[2], row[3],
                 "nothing-measured" if row[6] is None
                 else "%d/%d %s" % (row[6], row[7], row[8]),
                 row[5]))
    print("occluders: %s" % (occluders()[1],))
    place = chosen_placement()
    print("chosen=%s" % (place,))
    print("figureHeightPx at the chosen distance, for a 1.70 m figure: %.1f"
          % figure_height_px(place[3], 1.70) if place else "chosen=NONE")
    return rc


# ---- the selftest, which runs with no engine anywhere near it -------------


def _cpp_path():
    return os.path.join(repo_root(), "ue-probe", "Source", "LedgerProbe",
                        "Private", "VignetteShot.cpp")


def _cpp_const(text, name):
    """One `const <type> kName = <number>;` out of the C++, as a float.

    READ, NOT RETYPED. The C++ carries the placement literals because that
    is where the actor is spawned; this file carries the derivation because
    this is where the tests run. A constant typed in two places is a
    constant that drifts, and this one would drift into a figure standing
    somewhere nobody derived.
    """
    m = re.search(r"\b%s\s*=\s*(-?[0-9]*\.?[0-9]+)f?\s*;" % re.escape(name), text)
    return float(m.group(1)) if m else None


def selftest():
    """Accepting case first in every section. The live repository is the
    accepting fixture for everything that checks the project itself, so doing
    the work this tool prompts can never break this tool; the rejecting
    fixtures are synthetic, because a repository with a hundred-times-wrong
    import in it is not a repository anybody wants."""
    checks = [0]
    bad = []

    def ok(name, cond, detail=""):
        checks[0] += 1
        if not cond:
            bad.append("FAIL: %s%s" % (name, (" [" + str(detail) + "]") if detail else ""))

    root = repo_root()

    # -- A. THE TWO SOURCE FILES, WHICH ARE THE ACCEPTING CASE -------------
    body = os.path.join(root, body_source())
    clip = os.path.join(root, clip_source())
    ok("the body FBX is tracked and on disk", os.path.exists(body), body_source())
    ok("the clip FBX is tracked and on disk", os.path.exists(clip), clip_source())
    ok("the body is not one of the two grey mannequins",
       BODY_FILE not in EXCLUDED_BODIES, BODY_FILE)
    ok("and neither mannequin is reachable through the body path",
       all(not body_source().endswith(x) for x in EXCLUDED_BODIES))

    body_stats = fbx_geometry_bounds(body) if os.path.exists(body) else None
    clip_stats = fbx_geometry_bounds(clip) if os.path.exists(clip) else None
    ok("the body parses as a binary FBX", body_stats is not None)
    ok("the clip parses as a binary FBX", clip_stats is not None)
    if body_stats:
        ok("and the body carries geometry with vertices in it",
           body_stats["geoms"] > 0 and body_stats["verts"] > 0,
           "%s geoms %s verts" % (body_stats["geoms"], body_stats["verts"]))
        ok("the record cap did not bite on the body",
           not body_stats["recordCapBit"], body_stats["recordsVisited"])
        h, via = source_height_cm(body_stats)
        ok("the body has a measurable height", h is not None, via)
        # D18, AS A MEASUREMENT AND NOT AS A NAME. A body under 120 cm is a
        # child-sized body whatever its file is called, and D18 forbids one
        # anywhere. The bound is not a tuned threshold: it is the height
        # below which a standing human figure cannot be an adult.
        ok("the body measures as an ADULT, which is D18 checked rather than "
           "assumed", h is not None and h >= 120.0,
           None if h is None else round(h, 2))
    if clip_stats:
        ok("the clip is an FBX the reader can walk",
           clip_stats["recordsVisited"] > 0, clip_stats["recordsVisited"])

    # -- B. THE FBX READER'S REJECTING FIXTURES ---------------------------
    ok("bytes that are not an FBX read as no version at all",
       fbx_version(b"not an fbx at all, no") is None)
    ok("an empty file is refused", fbx_version(b"") is None)
    ok("and an ASCII FBX is refused rather than half-parsed",
       fbx_version(b"; FBX 7.4.0 project file\n") is None)
    ok("a walk over non-FBX bytes returns nothing measured",
       fbx_walk(b"rubbish", ("Vertices",))[0] is None)

    # -- C. THE HEIGHT VERDICT. ACCEPTING CASE FIRST ----------------------
    ok("two agreeing heights read AGREES",
       height_verdict(170.0, 170.0)[0] == HEIGHT_AGREES)
    ok("and a different body of a different height still AGREES, because "
       "this word is about arithmetic and not about the figure",
       height_verdict(196.0, 152.0)[0] == HEIGHT_AGREES,
       height_verdict(196.0, 152.0))
    ok("a metres-for-centimetres import reads a hundred times too small",
       height_verdict(1.70, 170.0)[0] == HEIGHT_HUNDRED_SMALL,
       height_verdict(1.70, 170.0))
    ok("a centimetres-for-metres import reads a hundred times too large",
       height_verdict(17000.0, 170.0)[0] == HEIGHT_HUNDRED_LARGE,
       height_verdict(17000.0, 170.0))
    ok("something else entirely is DISAGREES and is not silently a pass",
       height_verdict(600.0, 170.0)[0] == HEIGHT_DISAGREES,
       height_verdict(600.0, 170.0))
    ok("an unread engine height is the WORD nothing-measured, never a zero",
       height_verdict(None, 170.0) == (HEIGHT_UNMEASURED, None))
    ok("and an unread source height is too",
       height_verdict(170.0, None) == (HEIGHT_UNMEASURED, None))
    ok("a zero on either side is nothing measured and not a ratio",
       height_verdict(0.0, 170.0)[0] == HEIGHT_UNMEASURED
       and height_verdict(170.0, 0.0)[0] == HEIGHT_UNMEASURED)

    # -- D. THE STATUS WORD. ACCEPTING CASE FIRST -------------------------
    ok("a skinned body and a real clip is IMPORTED",
       import_status(2, True, 15000, 65, True, 120, True) == STATUS_IMPORTED)
    ok("a MEASURED zero is its own word: a skeleton with nothing on it",
       import_status(2, True, 0, 65, True, 120, True) == STATUS_NO_SKIN)

    # -- D2. THE RUN 54 FIXTURE: A COUNT THAT NEVER HAPPENED --------------
    #
    # THE ACCEPTING CASE IS THE ONE THIS SECTION EXISTS FOR and it is a real
    # run's numbers, not an invention: run 54 imported seven assets, read 65
    # bones, a matching skeleton, one material slot and bounds 166.50 cm
    # tall, and every vertex-count route raised on this engine. The line then
    # said MESH-BUT-NO-SKIN, which is a claim that the skin is ABSENT taken
    # from a count that never ran. A failed measurement is not evidence of
    # absence, and this is the check that says so.
    ok("a skin count that could not be taken is NOT the word for an absent "
       "skin, which is the run 54 fault",
       import_status(2, True, None, 65, True, 120, True) != STATUS_NO_SKIN,
       import_status(2, True, None, 65, True, 120, True))
    ok("it is the word that says no count was taken",
       import_status(2, True, None, 65, True, 120, True)
       == STATUS_SKIN_UNMEASURED)
    ok("and it is not IMPORTED either, because IMPORTED means proven",
       import_status(2, True, None, 65, True, 120, True) != STATUS_IMPORTED)
    ok("the three outcomes are three different words and never two",
       len({STATUS_NO_SKIN, STATUS_SKIN_UNMEASURED, STATUS_IMPORTED}) == 3)
    # THE THREE-WAY READING ITSELF, every branch, accepting case first.
    ok("a positive count reads as a measured present skin",
       skin_reading(15000) == SKIN_PRESENT)
    ok("a zero reads as a measured ABSENT skin, so the absent case is still "
       "reachable and this is not a ratchet",
       skin_reading(0) == SKIN_ABSENT)
    ok("no reading at all reads as NOT-MEASURED",
       skin_reading(None) == SKIN_UNMEASURED)
    ok("and so does a reading of the wrong type, however plausible",
       skin_reading("15000") == SKIN_UNMEASURED
       and skin_reading(1.5e4) == SKIN_UNMEASURED, skin_reading("15000"))
    ok("a True is never one vertex, which Python would otherwise allow",
       skin_reading(True) == SKIN_UNMEASURED
       and skin_reading(False) == SKIN_UNMEASURED)
    ok("a negative count is not trusted as a zero",
       skin_reading(-1) == SKIN_UNMEASURED)
    # AND A MEASURED FAULT STILL OUTRANKS A MISSING READING, which is the
    # order the status function states: the word names the thing somebody can
    # act on.
    ok("a missing anim still wins the line over an unmeasured skin",
       import_status(2, True, None, 65, False, 0, True) == STATUS_NO_ANIM)
    ok("and so does an unsaved asset",
       import_status(2, True, None, 65, True, 120, False) == STATUS_NOT_SAVED)
    ok("but a MEASURED absent skin outranks both, because it is a fact "
       "about the asset rather than about this script",
       import_status(2, True, 0, 65, False, 0, False) == STATUS_NO_SKIN)
    ok("no anim is its own word, because a T-pose is not a person",
       import_status(2, True, 15000, 65, False, 0, True) == STATUS_NO_ANIM)
    ok("an anim that loaded with no frames is the same word as no anim",
       import_status(2, True, 15000, 65, True, 0, True) == STATUS_NO_ANIM)
    ok("a mesh with no bones is not a skeletal mesh",
       import_status(2, True, 15000, 0, True, 120, True) == STATUS_NO_MESH)
    ok("one source file of two is NO-SOURCES",
       import_status(1, False, None, None, False, None, False) == STATUS_NO_SOURCES)
    ok("imported but unsaved is NOT-SAVED and never IMPORTED",
       import_status(2, True, 15000, 65, True, 120, False) == STATUS_NOT_SAVED)
    ok("and only IMPORTED returns zero",
       import_return(STATUS_IMPORTED) == 0
       and all(import_return(w) == 2 for w in
               (STATUS_NO_SOURCES, STATUS_NO_MESH, STATUS_NO_SKIN,
                STATUS_NO_ANIM, STATUS_NOT_SAVED, STATUS_SKIN_UNMEASURED,
                STATUS_RAISED)))

    # -- E. THE POSE TIME --------------------------------------------------
    ok("the pose time is the fraction of a measured duration",
       abs(pose_time_s(10.0) - 3.5) < 1e-9, pose_time_s(10.0))
    ok("a duration nobody measured gives 0.0 and not a plausible number",
       pose_time_s(None) == 0.0 and pose_time_s(0.0) == 0.0)
    ok("and the time can never overrun the clip",
       pose_time_s(2.0, 5.0) == 2.0, pose_time_s(2.0, 5.0))

    # -- F. THE PLACEMENT, DERIVED HERE AND CARRIED THERE -----------------
    rows = placement_series()
    ok("the series has rows at all", len(rows) > 10, len(rows))
    ok("and at least one of them is admissible, so the street HAS a "
       "silhouette position",
       any(r[4] for r in rows), len([r for r in rows if r[4]]))
    place = chosen_placement(rows)
    ok("a position was chosen", place is not None)
    if place:
        ok("the chosen position stands on the east footway",
           CARRIAGEWAY_Z_M < place[1] < CARRIAGEWAY_Z_M + FOOTWAY_WIDTH_M,
           place[1])
        ok("its backlight is behind rather than overhead",
           place[4] is not None and place[4] <= MAX_BACKLIGHT_ELEVATION_DEG,
           place[4])
        # THIS CHECK USED TO READ place[2] > 1.0, AND QUEUE 379 RETIRED IT.
        # It was true of a position standing behind a telephone kiosk, which
        # is the fault: a silhouette ratio above 1 says the light is behind
        # the body and says nothing at all about whether the body is behind
        # something else. The two claims that replace it are the measured
        # reason the fourth term is a maximand and the order the search
        # actually chooses in, and the ratio at the chosen position is
        # REPORTED on figurePlacement rather than asserted here. It is 0.237:
        # the first chosen position that is front-lit, and figureSil on the
        # shot line is the instrument that judges that, on pixels.
        ok("no admissible position is both fully clear and backlit, which "
           "is the measured reason a clear body is not a constraint",
           not [r for r in rows
                if r[4] and r[6] is not None and r[6] == r[7]
                and (r[1] or 0.0) > 1.0],
           "fullyClear=%d of admissible=%d"
           % (len([r for r in rows if r[4] and r[6] is not None
                   and r[6] == r[7]]),
              len([r for r in rows if r[4]])))
        ok("and the chosen position is the best backlit of the most visible "
           "ones, which is the order the search states",
           place[2] == max(r[1] for r in rows
                           if r[4] and r[1] is not None and r[6] == place[5]),
           place[2])
        ok("and it is inside the distance band the frame can hold",
           MIN_CAM_DISTANCE_M <= place[3] <= MAX_CAM_DISTANCE_M, place[3])
    # THE REJECTING FIXTURE FOR THE SEARCH: a figure standing at a lamp's
    # own foot is TOP-LIT, which is the picture this placement exists not to
    # make, and the search has to refuse it on the numbers rather than
    # because nobody tried it.
    #
    # THE FIRST WRITING OF THIS FIXTURE ASSERTED THE WRONG CLAUSE AND THE
    # SELFTEST CAUGHT IT, which is the fixture earning its keep: it claimed
    # the DOMINANT BACKLIGHT would read as overhead, and at x=8 the dominant
    # backlight is the lamp 20 m down the street at 18.4 degrees. The lamp
    # overhead is at separation zero, so it is not behind the figure at all
    # under any reading of behind: it is in the FRONT term, at 90 degrees,
    # where it swamps the ratio. That is what the series says and it is why
    # x=8 scores 0.15 against the chosen 2.62.
    _b, _f, _dom = backlight_reading(8.0, 3.23)
    _at_foot = [r for r in (_b + _f) if r[0] == 0]
    ok("a lamp at the figure's own feet reads as directly overhead, at 90 "
       "degrees, and is never counted as a backlight",
       len(_at_foot) == 1 and _at_foot[0][1] == 0.0 and _at_foot[0][3] == 90.0
       and _at_foot[0] in _f, _at_foot)
    # THE 0.25 MARGIN THIS CHECK CARRIED WAS A PROPERTY OF THE OLD CHOSEN
    # RATIO (2.62) AND NOT OF THIS FIXTURE, and with visibility outranking
    # the ratio it is arithmetically unavailable. It is replaced by the two
    # facts it was standing in for, both of them checked: the lamp's foot
    # scores lower on the backlight term, and the series refuses x=8 outright
    # on the distance band, so it can never be chosen whatever it scores.
    ok("so standing at a lamp's foot scores below the chosen position on "
       "the backlight term, and the series refuses x=8 on distance anyway",
       place is not None
       and silhouette_ratio(_b, _f) is not None
       and silhouette_ratio(_b, _f) < place[2]
       and not [r for r in rows if abs(r[0] - 8.0) < 1e-9 and r[4]],
       "%s vs %s" % (silhouette_ratio(_b, _f), None if not place else place[2]))
    ok("and the search never chooses a position at a lamp's own foot",
       place is None or all(abs(place[0] - lx) > 1.0
                            for lx, lz in LANTERNS_M
                            if abs(lz - place[1]) < FOOTWAY_WIDTH_M * 2.0),
       None if place is None else place[0])
    ok("a figure standing on the camera reads as no direction at all "
       "rather than as a position",
       backlight_reading(CAM_A_X_M, CAM_A_Z_M) == ([], [], None))

    # -- F2. THE FOURTH TERM: IS ANYTHING IN THE WAY ----------------------
    # ACCEPTING CASE FIRST, and the live scene is the fixture: the same JSON
    # the street is built from, read by the same function the search uses.
    _boxes, _note = occluders()
    ok("the scene the occlusion term tests against was read at all",
       len(_boxes) > 100 and "nothing-measured" not in _note, _note)
    ok("and it counts what it left out rather than dropping it silently",
       "decalsSkipped=" in _note, _note)
    _cast = OCCLUSION_RAY_COLS * OCCLUSION_RAY_ROWS
    ok("every row carries a clear count over the rays cast, denominator "
       "included",
       all(r[6] is not None and r[7] == _cast for r in rows),
       "%d of %d rows" % (len([r for r in rows if r[6] is not None]),
                          len(rows)))
    if place:
        ok("the chosen position is the most visible admissible position",
           place[5] == max(r[6] for r in rows if r[4]),
           "%s of %s" % (place[5], max(r[6] for r in rows if r[4])))
    # THE REJECTING FIXTURE IS RUN 53 ITSELF. x=17.5 has the best backlight
    # ratio of any admissible candidate and 4 of its 45 rays reach cam_A,
    # which is the frame Jafar could not see a person in. The search has to
    # refuse it ON THE NUMBERS, and the ratio-only argmax it was chosen by
    # has to still choose it, or this is not the fault being tested.
    _r53 = [r for r in rows if abs(r[0] - 17.5) < 1e-9]
    ok("the position run 53 chose is still in the series", len(_r53) == 1)
    if _r53 and place:
        _r53 = _r53[0]
        ok("run 53's position is admissible on the three old constraints, "
           "so nothing but the fourth term can refuse it", _r53[4], _r53[5])
        ok("and it has the best backlight ratio of any admissible row, "
           "which is why the old search chose it",
           _r53[1] == max(r[1] for r in rows if r[4] and r[1] is not None),
           _r53[1])
        ok("and under a tenth of it reaches the camera",
           _r53[6] * 10 < _r53[7], "%d/%d %s" % (_r53[6], _r53[7], _r53[8]))
        ok("the ratio-only argmax run 53 used still chooses it, so this "
           "fixture plants the real fault",
           max([r for r in rows if r[4] and r[1] is not None],
               key=lambda r: (r[1], -r[2]))[0] == _r53[0])
        ok("and the search with the fourth term refuses it, by more than "
           "half the rays cast",
           place[0] != _r53[0] and (place[5] - _r53[6]) * 2 > _r53[7],
           "%s clear=%s vs %s clear=%s"
           % (place[0], place[5], _r53[0], _r53[6]))
    # AND THE ORDER ITSELF, ON ROWS NOBODY MEASURED, both ways round, because
    # a comparator exercised only on the one series it was written against is
    # a comparator nobody has tested.
    _hi = (10.0, 1.0, 6.0, 20.0, True, "admissible", 40, 45, "none:0")
    _lo = (20.0, 9.9, 9.0, 20.0, True, "admissible", 4, 45, "kiosk:30")
    ok("a far better backlight never outranks a body the camera cannot see",
       max([_lo, _hi], key=placement_key) is _hi)
    _tie_near = (11.0, 0.5, 7.0, 20.0, True, "admissible", 40, 45, "awn:5")
    _tie_far = (15.0, 1.3, 11.0, 20.0, True, "admissible", 40, 45, "awn:5")
    ok("and between two equally visible positions the backlight ratio still "
       "decides, so the term this file was written for still does work",
       max([_tie_near, _tie_far], key=placement_key) is _tie_far)
    _unread = (11.0, 0.5, 7.0, 20.0, True, "admissible", None, 0,
               "nothing-measured:0")
    ok("a row whose occlusion could not be read sorts below one that was, "
       "rather than winning on a zero",
       max([_unread, _lo], key=placement_key) is _lo)

    # -- G. THE C++ CARRIES WHAT THIS FILE DERIVED ------------------------
    cpp_file = _cpp_path()
    if not os.path.exists(cpp_file):
        ok("VignetteShot.cpp is where this expects it", False, cpp_file)
    else:
        with open(cpp_file, "r", encoding="utf-8") as f:
            cpp = f.read()
        cx = _cpp_const(cpp, "kFigureXM")
        cz = _cpp_const(cpp, "kFigureZM")
        cy = _cpp_const(cpp, "kFigureFootYM")
        cf = _cpp_const(cpp, "kFigurePoseFraction")
        ok("the C++ carries the x this file derived",
           place is not None and cx is not None and abs(cx - place[0]) < 1e-6,
           "%s vs %s" % (cx, None if not place else place[0]))
        ok("the C++ carries the z this file derived",
           place is not None and cz is not None and abs(cz - place[1]) < 1e-6,
           "%s vs %s" % (cz, None if not place else place[1]))
        ok("the C++ stands the figure on the footway surface, not on the "
           "carriageway",
           cy is not None and abs(cy - footway_top_m()) < 1e-6,
           "%s vs %s" % (cy, footway_top_m()))
        ok("the C++ freezes the pose at the fraction this file names",
           cf is not None and abs(cf - POSE_FRACTION) < 1e-6,
           "%s vs %s" % (cf, POSE_FRACTION))
        ok("the C++ loads the mesh this script writes, at the path this "
           "script writes it to",
           mesh_object_path() in cpp, mesh_object_path())
        ok("and the anim the same way",
           anim_object_path() in cpp, anim_object_path())
        ok("the C++ spawns the figure only where the lanterns are lit",
           "LanternsOn" in cpp and "kFigureXM" in cpp)

    # -- G2. THE CALL SITE, BECAUSE BUILT IS NOT RUNNING ------------------
    # A script nothing calls is a script that never runs, and the run is the
    # only place any of this can be measured. Both halves of the chain are
    # checked here: something calls this file inside the editor, and the
    # workflow reads the file this one appends its line to.
    mb_path = os.path.join(root, "tools", "ue", "make_base_material.py")
    if not os.path.exists(mb_path):
        ok("make_base_material.py is where this expects it", False, mb_path)
    else:
        with open(mb_path, "r", encoding="utf-8") as f:
            mb = f.read()
        ok("the editor step's script calls this one",
           "import import_figure" in mb and "import_figure.main()" in mb)
        ok("and it does so only inside the editor, so no repository file is "
           "touched by a container run",
           mb.index("import import_figure") > mb.rindex("def _inside_unreal"),
           "call site is above the guard")
    wf_path = os.path.join(root, ".github", "workflows",
                           "ledger-probe-unreal.yml")
    if not os.path.exists(wf_path):
        ok("the probe workflow is where this expects it", False, wf_path)
    else:
        with open(wf_path, "r", encoding="utf-8") as f:
            wf = f.read()
        ok("the workflow reads the evidence file this line is appended to, "
           "whole, so the figure keys reach the verdict with no yml change",
           "ue-material.txt" in wf and "$matOut -Raw" in wf)
        ok("and it deletes that file before the run, so no previous run's "
           "line can be carried forward under this run's name",
           "Remove-Item $matOut" in wf)

    # -- H. THE LINE ------------------------------------------------------
    good = {"bones": 65, "skinVerts": 15000, "materials": 2, "lods": 1,
            "heightCm": 168.4, "sourceHeightCm": 168.2,
            "boundsCm": "x=44.1/y=52.0/z=168.4",
            "boundsOriginCm": "x=0.1/y=0.4/z=84.2",
            "fbxUnitScale": 1.0, "fbxUpAxis": "1",
            "fbxVerts": 15000, "fbxGeoms": 1,
            "animFrames": 120, "animDurationS": 4.0, "animRate": 30.0,
            "animSkeleton": "SK_michelle_Skeleton",
            "meshSkeleton": "SK_michelle_Skeleton", "skeletonsMatch": "yes",
            "importVia": "AssetImportTask", "saved": "yes",
            "uassetBytes": 4000000, "note": "none"}
    line = figure_line(STATUS_IMPORTED, good)
    ok("no value on the line carries a space",
       all("=" not in tok or " " not in tok for tok in line.split(" ")), line)
    ok("every key is key=value with exactly one equals in the key half",
       all(t.count("=") >= 1 for t in line.split(" ")), line)
    ok("the line carries the height, the source height and the ratio",
       "figureHeightCm=168.40" in line and "figureSourceCm=168.20" in line
       and "figureHeight=AGREES" in line, line)
    ok("and it names which body and which clip stood",
       "figureBody=Michelle.fbx" in line and "idle_2__Standing" in line, line)
    ok("it carries the D18 reading as a measured height",
       "figureD18=michelle/adult/measuredHeightCm=168.40" in line, line)
    ok("it says out loud that no placement number is a gate yet",
       "figurePlacementBound=NONE-YET" in line, line)
    ok("and that nothing is ever scaled",
       "figureScalePolicy=1/never-scaled" in line, line)
    ok("the return code on the line is the one the status word decides",
       "figureImportReturn=0" in line, line)
    empty = figure_line(STATUS_NO_SOURCES, {})
    ok("a run that measured nothing says so on every reading rather than "
       "printing zeros",
       empty.count("nothing-measured") >= 10
       and "figureHeightCm=nothing-measured" in empty
       and "figureHeight=nothing-measured" in empty, empty)
    ok("and it returns non-zero", "figureImportReturn=2" in empty, empty)
    ok("a mesh whose skin was counted at zero says the absent word",
       "figureImportStatus=MESH-BUT-NO-SKIN"
       in figure_line(STATUS_NO_SKIN, good))

    # -- H2. THE LINE KEEPS THE THREE OUTCOMES APART ----------------------
    ok("a counted skin prints the count AND the word for it",
       "figureSkinVerts=15000" in line and "figureSkin=MEASURED-PRESENT" in line,
       line)
    zero_skin = dict(good, skinVerts=0)
    zline = figure_line(import_status(2, True, 0, 65, True, 120, True), zero_skin)
    ok("a skin counted at zero prints a zero and the MEASURED-ABSENT word, "
       "so the absent case is reachable on the line and not only in a status",
       "figureSkinVerts=0 " in zline and "figureSkin=MEASURED-ABSENT" in zline,
       zline)
    # RUN 54'S OWN READINGS, WHICH ARE THE REJECTING FIXTURE FOR THE CLAIM
    # THE OLD LINE MADE. Every number here was read off the run's committed
    # evidence (production/d1-probe/ue-build.txt), not invented.
    run54 = dict(good, skinVerts=None, lods=None, materials=1,
                 heightCm=166.50, skinVia="none-of-6/lodIndex=0/lodCountVia=none-of-4",
                 lodsVia="none-of-4", importVia="AssetImportTask/made=7")
    r54 = figure_line(import_status(2, True, None, 65, True, 120, True), run54)
    ok("run 54's readings no longer produce a claim that the skin is absent",
       "MESH-BUT-NO-SKIN" not in r54, r54)
    ok("they produce the word that says no count was taken",
       "figureImportStatus=MESH-SKIN-NOT-MEASURED" in r54, r54)
    ok("the count itself still prints the words rather than a zero",
       "figureSkinVerts=nothing-measured" in r54 and "figureSkin=NOT-MEASURED"
       in r54, r54)
    ok("and the line names which readbacks were tried and that none "
       "answered, so the next run knows what to change",
       "figureSkinVia=none-of-6" in r54 and "figureLodsVia=none-of-4" in r54,
       r54)
    ok("everything run 54 DID measure still reaches the line beside it",
       "figureBones=65" in r54 and "figureMaterials=1" in r54
       and "figureHeightCm=166.50" in r54
       and "figureSkeletonsMatch=yes" in r54, r54)
    ok("no value on the run 54 line carries a space either",
       all("=" not in tok or " " not in tok for tok in r54.split(" ")), r54)

    # -- H3. THE NOTE'S CAP ANNOUNCES WHEN IT BITES -----------------------
    ok("a short report is carried whole and says nothing about a cap",
       note_of(["a", "b"]) == "a/b", note_of(["a", "b"]))
    ok("an empty report is the word none and not an empty value",
       note_of([]) == "none")
    _long = note_of(["x" * 50] * 40)
    ok("a report past the cap is cut AND SAYS SO, with how much went and "
       "how much there was",
       len(_long) <= NOTE_CAP and "not~shown" in _long and "of=" in _long,
       _long[-60:])
    ok("the announcement carries no space, so the line stays parseable",
       " " not in _long)

    # -- H4. A RAISE STILL PRODUCES A WHOLE LINE --------------------------
    # C OF THE BRIEF, AS A CHECK: a fault in this script must not cost the
    # run its evidence, and the accepting case is that everything measurable
    # before the raise is still on the line.
    rl, rman = raised_line(RuntimeError("the importer said no"),
                           {"bones": 65, "sourceHeightCm": 166.2})
    ok("a raise is a figure line like any other, with the status word for it",
       "figureImportStatus=RAISED" in rl and "figureImportReturn=2" in rl, rl)
    ok("and it carries what was measured before the raise rather than "
       "starting from nothing",
       "figureBones=65" in rl and "figureSourceCm=166.20" in rl, rl)
    ok("and the placement and the paths, which are derived here and need no "
       "engine at all",
       mesh_object_path() in rl and "figurePlacement=x=" in rl, rl)
    ok("the exception's own words are on the line with no spaces in them",
       "RAISED/RuntimeError/the~importer~said~no" in rl, rl)
    ok("no value on a raised line carries a space",
       all("=" not in tok or " " not in tok for tok in rl.split(" ")), rl)
    ok("and the manifest says it raised", rman.get("raised", "").startswith(
        "RuntimeError"), rman.get("raised"))

    # -- I. THE NAME CONTRACT ---------------------------------------------
    ok("the mesh object path is the package path plus the object name",
       mesh_object_path() == "/Game/Ledger/Figure/SK_michelle.SK_michelle",
       mesh_object_path())
    ok("the anim object path names the body and the clip",
       anim_object_path() ==
       "/Game/Ledger/Figure/A_michelle_idle_2.A_michelle_idle_2",
       anim_object_path())
    ok("both live under a directory DefaultGame.ini already cooks",
       PACKAGE_DIR.startswith("/Game/Ledger"), PACKAGE_DIR)

    for b in bad:
        print(b)
    print("import_figure --selftest: %d check(s), %d failure(s)"
          % (checks[0], len(bad)))
    return 1 if bad else 0


# ---- the half that needs Unreal. It supplies numbers and decides nothing ---


def _try(calls, report, accept=None):
    """Take the first route that answers and RECORD WHICH ONE, the shape
    import_prop_meshes.py uses, for the reason it gives: a fallback that
    works silently is a fallback nobody knows they depend on."""
    for name, fn in calls:
        try:
            v = fn()
        except Exception as e:
            report.append("%s-raised/%s" % (name, str(e)[:80]))
            continue
        if accept is not None and not accept(v):
            report.append("%s-refused/%s" % (name, str(v)[:40]))
            continue
        return v, name
    return None, "none-of-%d" % len(calls)


def _prop(obj, name, report, default=None):
    try:
        return obj.get_editor_property(name)
    except Exception as e:
        report.append("prop-%s-refused/%s" % (name, str(e)[:60]))
        return default


def _import_one(unreal, abs_fbx, dest_name, skeleton, report):
    """One FBX through the import task, as a skeletal mesh when skeleton is
    None and as an anim sequence when it is not.

    THE OPTIONS ARE ASKED FOR BY NAME AND EVERY REFUSAL IS RECORDED, because
    an import option this engine version renamed is a silent default, and a
    silent default here is a figure imported at the wrong scale or an anim
    bound to a skeleton it did not come from.
    """
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", abs_fbx)
    task.set_editor_property("destination_path", PACKAGE_DIR)
    task.set_editor_property("destination_name", dest_name)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)
    opts = None
    try:
        opts = unreal.FbxImportUI()
        opts.set_editor_property("import_mesh", skeleton is None)
        opts.set_editor_property("import_as_skeletal", True)
        opts.set_editor_property("import_animations", skeleton is not None)
        opts.set_editor_property("import_materials", True)
        opts.set_editor_property("import_textures", True)
        opts.set_editor_property(
            "mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH
            if skeleton is None else unreal.FBXImportType.FBXIT_ANIMATION)
        if skeleton is not None:
            opts.set_editor_property("skeleton", skeleton)
        # THE SCALE IS NOT TOUCHED, AND THAT IS THE MEASUREMENT. Setting an
        # import uniform scale here would make figureHeightRatio a number
        # about this line rather than about the importer, and the ratio is
        # the one reading that can name a units fault.
        report.append("fbx-options-built")
    except Exception as e:
        report.append("fbx-options-refused/%s" % str(e)[:80])
        opts = None
    if opts is not None:
        task.set_editor_property("options", opts)
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    tools.import_asset_tasks([task])
    made = []
    try:
        made = [str(p) for p in (task.get_editor_property("imported_object_paths") or [])]
    except Exception as e:
        report.append("imported-paths-refused/%s" % str(e)[:60])
    return made


def run_in_unreal():
    """Import both halves and READ BACK off the assets, never off the
    intentions. Every number on the line comes from a loaded asset."""
    import unreal
    report = []
    root = repo_root()
    r = {}
    body = os.path.join(root, body_source())
    clip = os.path.join(root, clip_source())
    sources = len([p for p in (body, clip) if os.path.exists(p)])
    # THE CONTAINER'S HALF, RUN HERE TOO. The same parser, on the same bytes,
    # inside the editor, so the two heights on the line are measured in one
    # process and no reader has to align two runs to compare them.
    st = fbx_geometry_bounds(body) if os.path.exists(body) else None
    src_cm, src_via = source_height_cm(st)
    r["sourceHeightCm"] = src_cm
    r["fbxUnitScale"] = None if not st else st.get("unitScaleFactor")
    r["fbxUpAxis"] = "nothing-measured" if not st else "%s/%s" % (
        st.get("upAxisIndex"), src_via)
    r["fbxVerts"] = None if not st else st.get("verts")
    r["fbxGeoms"] = None if not st else st.get("geoms")
    if sources < 2:
        r["note"] = "missing-source/body=%s/clip=%s" % (
            os.path.exists(body), os.path.exists(clip))
        return figure_line(import_status(sources, False, None, None, False,
                                         None, False), r), {"readings": r}
    # DELETE FIRST, for the reason import_prop_meshes.py's
    # preexisting_field() gives: the agent workspace is persistent, so an
    # asset left by an earlier run makes every later reading a reading of
    # that run.
    deleted = 0
    for n in (mesh_name(), anim_name(), mesh_name() + "_Skeleton",
              mesh_name() + "_PhysicsAsset"):
        p = PACKAGE_DIR + "/" + n
        try:
            if unreal.EditorAssetLibrary.does_asset_exist(p):
                unreal.EditorAssetLibrary.delete_asset(p)
                deleted += 1
        except Exception as e:
            report.append("delete-refused/%s/%s" % (n, str(e)[:50]))
    report.append("preexisting-deleted=%d" % deleted)

    made = _import_one(unreal, body, mesh_name(), None, report)
    report.append("mesh-import-made=%d" % len(made))
    mesh = None
    try:
        mesh = unreal.EditorAssetLibrary.load_asset(mesh_object_path())
    except Exception as e:
        report.append("mesh-load-refused/%s" % str(e)[:60])
    r["importVia"] = "AssetImportTask/made=%d" % len(made)
    skeleton = None
    if mesh is not None:
        r["bones"] = None
        bones, via = _try([
            ("skeleton.num_bones", lambda: len(
                _prop(mesh, "skeleton", report).get_editor_property("bone_tree") or [])),
            ("get_num_bones", lambda: mesh.get_num_bones()),
        ], report, accept=lambda v: isinstance(v, int) and v >= 0)
        r["bones"] = bones
        report.append("bones-via=%s" % via)
        skeleton = _prop(mesh, "skeleton", report)
        r["meshSkeleton"] = "none" if skeleton is None else str(skeleton.get_name())
        # ---- THE LOD COUNT FIRST, BECAUSE THE VERTEX COUNT NEEDS AN INDEX --
        #
        # RUN 54 MEASURED THE WHOLE OF THIS LADDER'S PROBLEM, and the
        # measurement is why the order below is what it is. On UE 5.8 the
        # three METHOD names this script had all raised with "object has no
        # attribute": get_num_vertices, get_num_lod_vertices, get_num_lods.
        # In the same run get_number_of_sampled_keys raised on AnimSequence
        # and the EDITOR PROPERTY number_of_sampled_keys answered. That is
        # the pattern, and it is a reading rather than a guess: on this
        # engine the properties answer where the wrapper methods do not. So
        # every ladder here leads with a property read.
        #
        # EVERY NAME BELOW IS A GUESS AT A BINDING AND NONE OF THEM IS
        # CHECKED. _try wraps each one, so a name that does not exist costs
        # one note line and the word nothing-measured, never a raise and
        # never a negative finding. The run names the one that answered, in
        # figureSkinVia, which is the only way any of this becomes known.
        lods, lvia = _try([
            # 1. the property route, which is the one run 54's evidence
            #    points at. LODInfo is the UPROPERTY on USkeletalMesh.
            ("lod_info.len", lambda: len(mesh.get_editor_property("lod_info"))),
            # 2. the UE5 editor subsystem.
            ("SkeletalMeshEditorSubsystem.get_lod_count",
             lambda: unreal.get_editor_subsystem(
                 unreal.SkeletalMeshEditorSubsystem
             ).get_lod_count(mesh)),
            # 3. the UE4-era scripting library, kept because a deprecated
            #    name that still answers is a reading and a free one.
            ("EditorSkeletalMeshLibrary.get_lod_count",
             lambda: unreal.EditorSkeletalMeshLibrary
             .get_lod_count(mesh)),
            # 4. THE ROUTE RUN 54 REFUTED, kept last and named as refuted so
            #    that a future engine adding it shows up as a via rather
            #    than as a silent change.
            ("get_num_lods-refuted-in-run-54", lambda: mesh.get_num_lods()),
        ], report, accept=lambda v: isinstance(v, int) and v >= 0)
        r["lods"] = lods
        r["lodsVia"] = lvia
        # ---- AND THE SKIN, WHICH IS THE READING RUN 54 LOST ---------------
        #
        # LOD 0 IS THE INDEX AND THE LOD COUNT IS PRINTED BESIDE IT, because
        # asking LOD 0 of a mesh with no LODs is how a count raises on an
        # INDEX rather than on a NAME, and those two failures read
        # identically in a note. figureSkinVia carries both, so the next run
        # can tell them apart without guessing.
        lod_ix = 0
        verts, vvia = _try([
            # 1. the UE5 editor subsystem, which is where the UE4 scripting
            #    library's mesh functions were moved.
            ("SkeletalMeshEditorSubsystem.get_num_verts",
             lambda: int(unreal.get_editor_subsystem(
                 unreal.SkeletalMeshEditorSubsystem
             ).get_num_verts(mesh, lod_ix))),
            # 2. the UE4-era library of the same function.
            ("EditorSkeletalMeshLibrary.get_num_verts",
             lambda: int(unreal.EditorSkeletalMeshLibrary
                         .get_num_verts(mesh, lod_ix))),
            # 3. THE ASSET REGISTRY, which is the only route here that does
            #    not depend on a Python binding existing at all: the tag is
            #    written by the asset itself when it is saved. Two spellings,
            #    because the tag name is not checked either.
            ("assetdata.tag.VertexCount",
             lambda: int(str(unreal.EditorAssetLibrary
                             .find_asset_data(mesh_object_path())
                             .get_tag_value("VertexCount")))),
            ("assetdata.tag.Vertices",
             lambda: int(str(unreal.EditorAssetLibrary
                             .find_asset_data(mesh_object_path())
                             .get_tag_value("Vertices")))),
            # 4. THE TWO ROUTES RUN 54 REFUTED, last and named as refuted.
            ("get_num_vertices-refuted-in-run-54",
             lambda: mesh.get_num_vertices(lod_ix)),
            ("get_num_lod_vertices-refuted-in-run-54",
             lambda: mesh.get_num_lod_vertices(lod_ix)),
        ], report, accept=lambda v: isinstance(v, int) and v >= 0)
        r["skinVerts"] = verts
        r["skinVia"] = "%s/lodIndex=%d/lodCountVia=%s" % (vvia, lod_ix, lvia)
        # THE WORD, BESIDE THE COUNT, AT THE MOMENT THE COUNT WAS TAKEN.
        report.append("skin=%s/via=%s" % (skin_reading(verts), vvia))
        mats = _prop(mesh, "materials", report)
        r["materials"] = None if mats is None else len(mats)
        # THE HEIGHT, OFF THE ASSET, IN THE ENGINE'S OWN UNITS.
        b, bvia = _try([("get_bounds", lambda: mesh.get_bounds())], report,
                       accept=lambda v: v is not None)
        report.append("bounds-via=%s" % bvia)
        if b is not None:
            try:
                o = b.origin
                e = b.box_extent
                r["boundsCm"] = "x=%.2f/y=%.2f/z=%.2f" % (
                    abs(e.x) * 2.0, abs(e.y) * 2.0, abs(e.z) * 2.0)
                r["boundsOriginCm"] = "x=%.2f/y=%.2f/z=%.2f" % (o.x, o.y, o.z)
                r["heightCm"] = abs(e.z) * 2.0
            except Exception as ex:
                report.append("bounds-read-refused/%s" % str(ex)[:60])

    anim = None
    if skeleton is not None:
        amade = _import_one(unreal, clip, anim_name(), skeleton, report)
        report.append("anim-import-made=%d" % len(amade))
        try:
            anim = unreal.EditorAssetLibrary.load_asset(anim_object_path())
        except Exception as e:
            report.append("anim-load-refused/%s" % str(e)[:60])
        if anim is None and amade:
            # THE PATH THE IMPORTER ACTUALLY USED, when it differs from the
            # one asked for. Recorded rather than guessed at, the same way
            # import_prop_meshes.py resolves a renamed static mesh.
            for p in amade:
                try:
                    a = unreal.EditorAssetLibrary.load_asset(p)
                except Exception:
                    a = None
                if a is not None:
                    anim = a
                    report.append("anim-found-at/%s" % str(p).replace(" ", "~"))
                    break
    if anim is not None:
        frames, fvia = _try([
            ("get_number_of_sampled_keys", lambda: anim.get_number_of_sampled_keys()),
            ("number_of_sampled_keys", lambda: _prop(anim, "number_of_sampled_keys", report)),
            ("number_of_frames", lambda: _prop(anim, "number_of_frames", report)),
        ], report, accept=lambda v: isinstance(v, int) and v >= 0)
        r["animFrames"] = frames
        report.append("frames-via=%s" % fvia)
        dur, dvia = _try([
            ("get_play_length", lambda: anim.get_play_length()),
            ("sequence_length", lambda: _prop(anim, "sequence_length", report)),
        ], report, accept=lambda v: isinstance(v, float) and v >= 0.0)
        r["animDurationS"] = dur
        report.append("duration-via=%s" % dvia)
        if dur and frames:
            r["animRate"] = float(frames) / float(dur) if dur > 0 else None
        ask = _prop(anim, "skeleton", report)
        r["animSkeleton"] = "none" if ask is None else str(ask.get_name())
        r["skeletonsMatch"] = ("yes" if (ask is not None and skeleton is not None
                                         and ask == skeleton) else "NO")
    saved = []
    for n, path in (("mesh", mesh_object_path()), ("anim", anim_object_path())):
        try:
            if unreal.EditorAssetLibrary.does_asset_exist(path.split(".")[0]):
                unreal.EditorAssetLibrary.save_asset(path.split(".")[0], False)
                saved.append(n)
        except Exception as e:
            report.append("save-refused/%s/%s" % (n, str(e)[:50]))
    r["saved"] = "/".join(saved) if saved else "none"
    try:
        p = os.path.join(unreal.Paths.project_dir(), "Content", "Ledger",
                         "Figure", mesh_name() + ".uasset")
        r["uassetBytes"] = os.path.getsize(p) if os.path.exists(p) else 0
    except Exception:
        r["uassetBytes"] = None
    r["note"] = note_of(report)
    status = import_status(sources, mesh is not None, r.get("skinVerts"),
                           r.get("bones"), anim is not None,
                           r.get("animFrames"), len(saved) == 2)
    return figure_line(status, r), {
        "schema": "ledger.figure-import/1",
        "measuredBy": "editor",
        "body": body_source(),
        "clip": clip_source(),
        "meshPath": mesh_object_path(),
        "animPath": anim_object_path(),
        "placementSeries": placement_series(),
        "chosen": chosen_placement(),
        "readings": r,
        "report": report,
    }


def _beside_project(name):
    try:
        import unreal
        root = unreal.Paths.project_dir()
    except Exception:
        root = os.path.join(repo_root(), "ue-probe") + os.sep
    return os.path.join(root, name)


def _write(line, man):
    for name, blob in (("ue-figure.txt", line + "\n"),
                       ("ue-figure.json", json.dumps(man, indent=1,
                                                     sort_keys=True,
                                                     default=str))):
        path = _beside_project(name)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(blob)
        except Exception as e:
            print("import_figure: could not write %s (%s)" % (path, e))
    # AND INTO THE CHANNEL THE WORKFLOW ALREADY READS. The build step does
    # `if (Test-Path $matOut) { $L += (Get-Content $matOut -Raw).Trim() }`
    # over ue-material.txt, which it DELETES before the run, so appending
    # here puts the figure keys in the verdict with no yml change and with
    # no way for a previous run's line to be carried forward under this
    # run's name. Why there is no step of its own: the build block is 17
    # characters under the largest one GitHub has ever accepted here, which
    # tools/workflow-size.py measures, and this is the same answer
    # make_sky_material.py already uses for the same constraint.
    try:
        with open(_beside_project("ue-material.txt"), "a",
                  encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print("import_figure: could not append to ue-material.txt (%s)" % e)
    print(line)
    try:
        import unreal
        unreal.log("LEDGER " + line)
    except Exception:
        pass


def _inside_unreal():
    try:
        import unreal  # noqa: F401
        return True
    except Exception:
        return False


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if "--measure" in sys.argv:
        return measure_only()
    # NOTHING THIS SCRIPT DOES MAY WRITE INTO THE REPO WHEN IT IS RUN
    # OUTSIDE THE EDITOR, which is make_base_material.py's discipline and the
    # reason it has one: a side-effecting check once appended junk into a
    # file shaped like the build evidence channel on every verify run.
    if not _inside_unreal():
        print("import_figure: NOTHING MEASURED, no unreal module. "
              "Use --selftest or --measure outside the editor.")
        return 1
    # ---- NOTHING IN HERE MAY REACH THE CALLER ---------------------------
    #
    # THE CALLER IS make_base_material.py, INSIDE THE ONE EDITOR PROCESS THE
    # BUILD STEP STARTS, and the previous specialist named that arrangement's
    # cost in writing: a failure here takes that run's material work with it.
    # This is the half of that cost an exception can cause, and it is closed:
    # every raise becomes a WHOLE figure line and a return code, and the
    # caller sees an ordinary return.
    #
    # BaseException AND NOT Exception, deliberately and for this file's own
    # stated reason: inside the editor this runs on an embedded interpreter
    # that is not exiting anything, so a SystemExit raised by any library
    # under here is not a request to end a process, it is a bug that would
    # end the EDITOR'S process. KeyboardInterrupt is in the same position.
    #
    # THE HALF THIS CANNOT CLOSE IS NAMED RATHER THAN IMPLIED: a hard crash
    # in native importer code is not an exception and no except clause in
    # Python reaches it. Only a separate editor process would, and that is a
    # workflow step, which tools/workflow-size.py says this workflow has no
    # room for. It is not attempted here.
    try:
        line, man = run_in_unreal()
    except BaseException as exc:  # noqa: BLE001
        line, man = raised_line(exc)
        try:
            import traceback
            traceback.print_exc()
        except BaseException:
            pass
    # THE WRITE IS INSIDE THE GUARD TOO. _write already catches per file,
    # but a raise from anything else in it would propagate into the caller
    # and cost the material run the thing this whole block exists to stop.
    try:
        _write(line, man)
    except BaseException as exc:  # noqa: BLE001
        print("import_figure: could not write the line (%s: %s)"
              % (type(exc).__name__, exc))
    try:
        m = re.search(r"figureImportReturn=(\d+)", line)
        return int(m.group(1)) if m else 2
    except BaseException:  # noqa: BLE001
        return 2


if __name__ == "__main__":
    # SYS.EXIT IS FOR A REAL PROCESS ONLY, for the reason the material
    # generator states: inside the editor this runs on an embedded
    # interpreter that is not exiting anything, and raising SystemExit there
    # is a plausible way to turn a script that worked into a process that
    # reports failure. The verdict travels in the file as figureImportReturn.
    _code = main()
    if _inside_unreal():
        print("import_figure: returning %d without sys.exit (inside the "
              "editor; the verdict is figureImportReturn in ue-figure.txt)"
              % _code)
    else:
        sys.exit(_code)
