#!/usr/bin/env python3
"""Meridian's street lighting column (E1_lighting_column / E2_sodium_lantern_head),
authored in Blender. THE AUTHORING LINE'S FIRST TEST, ruled by Jafar 2026-09-21:
"if a lamp column comes out right in Blender, the facades are the same method
at scale." Read the ruling in full before touching this file:
game-design/decision-2026-09-21-ruling-the-lamp-column-is-authored-and-it-is-the-authoring-lines-first-test.md

    blender --background --factory-startup --python tools/art-recipes/lighting-column.py \
        -- --out DIR --root <workspace> --commission <name> --run-sha <sha> \
           --studio-sha <sha>

THAT LINE IS THE LANE'S, NOT THIS FILE'S IDEA OF IT: it is what
.github/workflows/ledger-art-blender-preview.yml executes on the self-hosted
runner. Written here for a reader only; the selftest DERIVES it from the
workflow and from run-recipe.py rather than from this docstring, because this
paragraph is a comment and comments decay. See lane_contract().

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
      and DARK (painted steel, not the thicker paler concrete), a SMALL FLAT
      SHALLOW CANOPY head aimed down the street (not a bowl, not a box), lit
      warm amber, with NO ornament: no fluting, no ladder bar, no scroll, no
      finial. CORRECTED 2026-09-21, and the false phrase is named rather than
      quietly dropped: this entry used to say the arc was "LONG SHALLOW
      GENTLE... not a tight quarter circle". A pixel-level crop-and-measure
      of the same sheet this session (SHEET_REF below; method: threshold the
      column's own silhouette against the sky and trace it row by row) found
      the opposite: the curve resolves in well under 10 vertical pixels
      against some 450 pixels of dead-straight pole, i.e. COMPACT and
      TOP-CONCENTRATED. The first render, built to the old phrase's naive
      quarter-circle-BEATING radius, is exactly what read wrong against the
      sheet: see point 2. The old phrase was written from a description of
      the sheet, not from cropping and measuring it, which is the fault
      rule 4 and this role's own standing instruction both name; this
      correction is the accepting case for why that instruction exists.

Two consequences follow, and both are implemented, not just described:
  1. The column body is dark painted steel throughout. No concrete variant is
     authored here.
  2. THE NECK ENDPOINTS DO NOT MOVE. lantern0..3 sit at y = 4.965 m (world,
     including the street's own 0.065 m ground camber) and the shaft is
     4.7 m at 0.114 m round: production/specs/vignette-pieces.json, read
     below rather than retyped, and cross-checked against it every run so
     the authored mesh and the blockout cannot drift (see cross_check()).
     What DOES move is the ARC SHAPE between those two fixed points, and it
     has moved TWICE now: first (2026-09-08) to a naive-quarter-circle-
     beating radius of 1.5x outreach_m, which the first real Blender render
     showed as "a near-straight shaft that hooks over sharply in a small
     radius at the very top... reads as a shepherd's crook, not a swan
     neck"; then (2026-09-21, this revision) to 0.6x outreach_m, chosen
     against the corrected sheet reading above and against a CLOSED-FORM
     FINDING that the first fix attempt's own working uncovered: because the
     lantern mount (locally y = 4.9 m) sits BELOW the shaft top (y = 5.0 m),
     any curve leaving the shaft tangent-vertically and reaching the mount
     is forced through a large total turning angle (roughly 120 to 200
     degrees, checked numerically over a wide sweep of single-arc and
     opposite-curvature two-arc constructions during this revision, not
     shipped as code because it changes no output here, only the honest
     menu of shapes) REGARDLESS of how many arcs build it or which way they
     curve. So "long and gradual" was never reachable from these pinned
     endpoints; what IS reachable, and what 0.6 is chosen for, is a curve
     whose EXTERNAL DROPPER (the straight rod that would otherwise show
     above the lantern housing, see neck_arc()'s own docstring) is short
     enough to read as subordinate to the fitting rather than as a separate
     part. Because curvature is constant along a true circle, "shallower
     than the naive quarter circle" is a closed-form fact of geometry for
     ANY radius bigger than outreach_m, and 0.6 is smaller than that, on
     purpose: see NECK_ARC_RADIUS_RATIO's own comment for the full trade-off
     (a bigger radius reads gentler but makes the external dropper LONGER,
     never shorter, given these endpoints) and neck_arc()'s docstring for
     the general proof, which the selftest still checks over a range of
     ratios above 1.0 as a property of the formula. Both the authored and
     naive figures are still printed every run (lcNeck), now informational
     rather than gating: see NECK_ARC_RADIUS_RATIO.
  2B. REVISED AGAIN, 2026-09-21, SAME DAY: the 0.6-ratio render above landed
     and was compared against the sheet by BOUNDING BOX, not only by the
     row-count read point 2 already used, and refused. The sheet's own
     fixture, re-traced independently this pass (crop x233-285 y745-800,
     same luminance-threshold-vs-sky method, PLUS the small isolated dark
     patch at y751-752 counted in as the ridge-top bump/photocell rather
     than noise, since it is dark and contiguous with the curve two rows
     below it, not scattered): 25 px wide by 11 px tall, y751-761 x237-261,
     ASPECT 2.27:1, FLAT AND WIDE (SHEET_REF["assembly_bbox_aspect"]). The
     0.6-ratio render's own neck+lantern envelope read far closer to
     SQUARE. This is not a tuning miss, it is a CLOSED-FORM property of a
     single circular arc: a quarter turn (vertical tangent to horizontal
     tangent) has a local bounding box of exactly radius_m by radius_m, for
     ANY radius, because the same R sets both the sideways reach
     (R(1-cos90)=R) and the rise (R sin90=R) of that turn. The shipped arc
     swept PAST 90 degrees (131.81) to reach outreach_m sideways at all
     (point 2 above), so its own bend still read close to square rather
     than flat: the extra sweep buys width but keeps costing height on the
     way back down. NO SINGLE RADIUS FIXES THIS: aspect-at-the-bend is a
     property of using only curvature to cover the reach, not of which
     curvature.
     THE FIX is a family the earlier closed-form search (single arcs and
     opposite-curvature arc pairs, point 2 above) never included: a literal
     STRAIGHT segment, zero curvature, which covers reach WITHOUT costing
     any turning angle. neck_bracket() (below neck_arc(), which is KEPT,
     UNCHANGED and UNUSED BY THE SHIPPED PATH as of this revision, for its
     own closed-form coverage and selftest) splits the neck into a TIGHT
     quarter circle corner, fixed at exactly 90 degrees so the level arm
     that follows is tangent-continuous with it (no kink at that joint),
     then a LEVEL straight arm to outreach_m, then the same short vertical
     dropper as before into the pinned mount. This decouples "how tight is
     the corner" from "how much reach is covered": NECK_CORNER_RADIUS_RATIO
     can be small (tight, matching the sheet's compact read) while the arm
     alone, free of any height cost because a level line costs no height by
     definition, carries whatever reach the corner did not.
     THE DROPPER IS STILL UNAVOIDABLE, for the same reason as point 2's own
     proof: the arm's height is mh + radius_m, always ABOVE mh for a
     positive radius, and the pinned mount sits BELOW mh. A member reaching
     the mount with NO vertical segment anywhere, while ALSO starting
     tangent-vertical at the shaft top, is still impossible (the same
     sin(sweep)>=0-for-sweep-under-180 argument, now applied to the arm's
     constant height rather than an arc's varying one). What IS achieved is
     a LEVEL ARM, the member that actually reads as the fixture's reach,
     arriving at zero degrees from horizontal; the lantern hangs LEVEL
     beneath the arm's own short end on a dropper of length radius_m +
     lantern_height_m/2. That is the brief's own words for this shape ("a
     flat wide lantern hanging level beneath the arm's end"), not a
     workaround for them.
     NECK_CORNER_RADIUS_RATIO=0.28 is chosen so the printed assembly aspect
     (lcAssembly, from assembly_bbox()) lands near 2.27, not read off the
     photo: the sheet's own 25x11 reading is explicitly LOW-TO-MODERATE
     CONFIDENCE (SHEET_REF["confidence"]) and, measured a second way this
     same pass (9 rows instead of 11, from a stricter widen-threshold that
     excludes the ridge-top bump), the SAME crop gives 2.78, a 20%+ swing
     from a one-row difference at this resolution.
     ASSEMBLY_ASPECT_TOLERANCE_PCT=25 is set from that observed swing, not
     assumed. lcAssembly is PRINTED every run, per D41 (2026-09-08): this
     is visual work, ungated; the studio compares the rendered frame
     against the sheet and iterates, and no selftest check asserts
     proximity to 2.27.
  3. A wall fixture seen on the same sheet, a dark conical bracket lamp with
     a wire cage guard under the Harbour Office eaves, is a DIFFERENT, real
     asset the street will need. It is named here and NOT built: see the
     queue item this recipe ships beside.
  4. THE LANTERN HEAD AND THE BASE ALSO MOVED, 2026-09-21, against the same
     corrected sheet reading. The first render's housing read as "a chunky
     slab, visibly too deep and too bulky" and its base as "a chunky sleeve
     slipped over the shaft": see LANTERN_BODY_FRACTION,
     LANTERN_BODY_INSET_RATIO and build_parts()'s base construction for what
     changed and why. Neither the lantern's overall length_m/width_m/
     height_m nor the base's own diameter_m/height_m moved: those are
     spec-pinned and cross-checked exactly as before, only how each fills
     its own pinned envelope did.

WHAT A PRINTED COMPARISON AGAINST THE SHEET CAN AND CANNOT BE, a finding of
this 2026-09-21 revision and not only a disclaimer. This file CAN and DOES
print a comparison against the sheet (SHEET_REF, emitted every run as
lcSheetRef): a dated, sourced, one-time pixel measurement, checked into this
file the same way a spec value is. What it CANNOT do is RECOMPUTE that
comparison at run time the way cross_check() recomputes agreement with
vignette-pieces.json: this script has no image-reading dependency and does
not open production/art/atlas-01/concepts/hook.png, so SHEET_REF is a
constant, not a function of anything measured this run. That means a future
edit to the sheet, or a better crop, or a second pair of eyes, cannot be
caught automatically the way a drifted spec value is caught by cross_check;
it can only be caught by someone re-cropping the sheet and re-editing
SHEET_REF, exactly as happened to the phrase this revision corrects in point
2 above. SILHOUETTE ITSELF IS A DIFFERENT CLAIM AGAIN, one this file cannot
settle at all: mesh_check() proves a part is a valid closed manifold, never
that it reads as the right SHAPE from a camera, and no arrangement of
printed numbers substitutes for looking at a rendered frame or, failing
that, at a scale-matched drawing of the planned geometry next to the sheet
crop, the way this revision's own working did before choosing
NECK_ARC_RADIUS_RATIO. `--plan` proves the geometry is what the numbers say
it is; it does not prove the numbers are the right shape.

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

#: THE LANE'S ARGUMENT CONTRACT LIVES IN THE LANE, NOT HERE. These two files
#: are the only places the Blender invocation is written down, and the
#: selftest reads the flag list OUT OF THEM at test time rather than holding a
#: retyped copy: a hardcoded list is the snapshot fault (queue 416) and goes
#: stale the next time the lane changes. See lane_contract() and the
#: `lane/` checks in selftest(). Paths are relative to the STUDIO checkout
#: (this file's own ROOT), not to --root, which on the runner is the
#: workspace above the studio checkout and holds no .github.
LANE_WORKFLOW_REL = ".github/workflows/ledger-art-blender-preview.yml"
LANE_WRAPPER_REL = "tools/art-recipes/run-recipe.py"
#: Characters a commission name may not contain, same set and same reason as
#: mickeys-blockout.py: the name reaches a path and a branch ref.
ID_BAD = set(' \t/\\:*?"<>|=')

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
#: outreach_m. REVISED 2026-09-21, first-render iteration: 1.5 shipped a
#: shape the first real Blender frame showed wrong against the Hook sheet
#: (production/art/atlas-01/concepts/hook.png on origin/art/atlas-01,
#: cropped x185-320 y700-1000 and re-measured pixel by pixel this session:
#: the reference's own curve resolves in under 10 vertical pixels against
#: roughly 450 px of dead-straight visible pole, i.e. COMPACT and
#: top-concentrated, not the long gradual sweep it was first read as). 0.6
#: is the smallest ratio that keeps the neck's EXTERNAL dropper (the part
#: that would show as a separate straight rod above the lantern housing,
#: neck_arc()'s radius_m * sin(sweep_rad)) under lantern_width_m, printed
#: and checked every run by selftest rather than asserted here; see
#: neck_arc()'s docstring for why no ratio, and no pair of arcs of opposite
#: curvature, can make this join gentle given the pinned endpoints. Below
#: 1.0 the arc is no longer shallower than the naive quarter circle, and
#: that comparison is INFORMATIONAL ONLY as of this revision, per Jafar's
#: 2026-09-21 ruling on the first render: "the quarter circle was never the
#: reference... pick the radius ratio from the sheet, and print the new
#: comparison against the sheet rather than against a quarter circle." The
#: sheet itself does not yield a dimensioned radius (rule 8: an admitted gap,
#: not invented precision), so 0.6 is a labelled choice bounded by the
#: dropper-elimination requirement above, not a value read off the photo.
NECK_ARC_RADIUS_RATIO = 0.6
#: KEPT FOR neck_arc() ONLY, which is itself kept for its own closed-form
#: properties and selftest coverage (module docstring point 2B) and is
#: UNUSED BY THE SHIPPED PATH as of 2026-09-21 (same day, second revision):
#: neck_curve() calls neck_bracket() (near NECK_CORNER_RADIUS_RATIO) instead.
#: Left in place, unchanged, rather than deleted, because deleting a
#: working, still-true, still-tested closed-form utility to shrink a diff is
#: not this file's own convention anywhere else in it.

#: THE SHEET MEASUREMENT ITSELF, taken this session, NOT recomputed at run
#: time (this script does not open images; see plan_lines()'s lcSheetRef
#: comment for why that is named rather than papered over). The brief's own
#: crop box was production/art/atlas-01/concepts/hook.png on
#: origin/art/atlas-01, x185-320 y700-1000; the pixel trace that produced
#: the figures below used a narrower sub-window of that same box (x220-280,
#: to isolate the column from the Harbour Office chimney at its left edge)
#: and a luminance threshold against the sky's own ~200-210 baseline in that
#: photo. CONFIDENCE IS LOW-TO-MODERATE AND SAID SO: the column is 2 to 3
#: pixels wide at the sheet's native resolution, so this is close to the
#: image's own resolution floor and the figures are directional, not
#: dimensioned (rule 8). What the trace found, run row by row from y700 to
#: y1300: the pole is dead straight (x238-240, +/-1px) for roughly 450
#: rows, and everything that is not plain pole width (the curve, the head,
#: the small ridge-top bump) resolves inside about 8 ROWS at the very top,
#: y751 to y759, widening from the pole's own width out to x261 at its
#: widest (y756) before returning to plain pole width by y759. That is
#: COMPACT and TOP-CONCENTRATED: it does not resolve a curve beginning
#: "two thirds up the shaft", and it does not resolve any separately
#: readable straight segment between the curve and the head. Both readings
#: fed directly into this file's choices: NECK_ARC_RADIUS_RATIO above is
#: chosen for a short, compact transition rather than a long gradual one,
#: and LANTERN_BODY_FRACTION below is chosen against the ~3.3:1
#: width-to-height read at the widest traced row, not against a "long lazy
#: sweep" the sheet's own pixels do not show at this crop.
SHEET_REF = {
    "source": "production/art/atlas-01/concepts/hook.png@origin/art/atlas-01",
    "crop_px": "185,700,320,1000/tracedSubWindow-220,690,280,800",
    "method": "luminance-threshold~silhouette~trace~vs~sky~baseline~~200-210",
    "measured_at": "2026-09-21",
    "curve_vertical_fraction": "~8px/~450px-visible-pole~(~1.8pct),compact,top-concentrated",
    "head_width_to_height": "~23px:7px~is~3.3to1~at~widest~traced~row~(y756,x238-261)",
    # SECOND, INDEPENDENT RE-TRACE, same session, same crop, same method, of
    # the FULL fixture's own bounding box rather than only the widest row:
    # rows y751-761 (the isolated 2-row dark patch at y751-752, the
    # ridge-top bump/photocell, counted in because it is dark and
    # contiguous with the curve two rows below it, not scattered), x237-261.
    # 25 px wide, 11 px tall. Sensitivity checked, not assumed: a stricter
    # widen-threshold that excludes the 2-row bump gives 9 rows and 2.78:1
    # instead of 11 rows and 2.27:1, a 20%+ swing from one row of difference
    # at this resolution, which is why ASSEMBLY_ASPECT_TOLERANCE_PCT below
    # is 25, not a smaller number chosen to look precise.
    "assembly_bbox_aspect": "25px:11px~is~2.27to1~(y751-761~x237-261,~flat~and~wide)",
    "dropper_visible": "no/widens-and-returns-to-plain-pole-width-within~7~rows",
    "confidence": "low-to-moderate/pole~is~2-3px~wide~at~native~res,~near~the~image's~own~floor",
}

#: THE SHIPPED CORNER RADIUS, 2026-09-21 (same day, second revision): see
#: module docstring point 2B and neck_bracket()'s own docstring for the
#: construction this feeds (a fixed 90-degree corner, then a level arm,
#: then a dropper) and why it replaces NECK_ARC_RADIUS_RATIO's single
#: continuous arc as what ships. R = ratio * outreach_m = 0.28 * 0.5 =
#: 0.14 m: a tight corner (smaller than the old 0.6-ratio's 0.30 m radius),
#: chosen so assembly_bbox()'s printed aspect lands near the sheet's own
#: 2.27:1 (SHEET_REF["assembly_bbox_aspect"]), not read off the photo
#: directly: no dimensioned drawing of the reference exists to read a
#: radius from (rule 8), so this is a labelled choice bounded by that
#: target and by external_dropper_m staying under lantern_width_m (checked
#: every run by selftest, the same requirement NECK_ARC_RADIUS_RATIO's own
#: comment named for the earlier construction), not a value the sheet
#: itself yields.
NECK_CORNER_RADIUS_RATIO = 0.28

#: THE TARGET AND ITS TOLERANCE, printed every run (lcAssembly) beside the
#: achieved aspect so the comparison is in the verdict, not only in a
#: report: SHEET_REF["assembly_bbox_aspect"]'s own figure, 2.27, and a
#: tolerance MEASURED from this session's own re-trace sensitivity, not
#: assumed: reading the same crop with a stricter widen-threshold (9 rows,
#: excluding the small ridge-top bump) instead of 11 gives 2.78, a 20.5
#: percent swing from ONE row of difference at 11 px tall, which is near
#: the image's own resolution floor (SHEET_REF["confidence"]). 25 is chosen
#: to comfortably cover that observed swing rather than to look precise.
#: Per D41 (2026-09-08): this is VISUAL, UNGATED work; the studio compares
#: the rendered frame against the sheet and iterates. NOTHING in selftest
#: asserts assembly_aspect is within this tolerance: it is printed, not
#: gated, exactly the demotion the module docstring's point 2 already
#: applied to the naive-quarter-circle comparison, and for the same reason
#: (a gate whose baseline was never the reference is worse than no gate).
ASSEMBLY_SHEET_TARGET_ASPECT = 2.27
ASSEMBLY_ASPECT_TOLERANCE_PCT = 25.0

#: The lantern's total height (spec lantern.height_m) is split between a
#: plain housing body and a shallow pitched canopy on top, so the OVERALL
#: bounding box still matches the spec box exactly; only the split between
#: "body" and "roof" is authored and it is named here rather than folded
#: silently into a derived number. REVISED 2026-09-21: the first render
#: showed the housing as "a chunky slab, visibly too deep and too bulky",
#: against a Hook sheet reference measured this session as a shallow,
#: elongated head, roughly 3:1 wide-to-tall at the widest visible row of its
#: own silhouette (production/art/atlas-01/concepts/hook.png, same crop as
#: above). 0.7 gave a tall vertical-walled body with a token 0.06 m roof;
#: 0.4 gives most of the height to the sloped canopy instead, which is the
#: element the sheet actually shows.
LANTERN_BODY_FRACTION = 0.4
#: NEW 2026-09-21, same iteration. The body housing is authored NARROWER
#: than the roof/canopy above it, so the canopy overhangs the housing on
#: every side, exactly as a cobra-head fitting's hood oversails its lamp
#: chamber. Purely a proportion choice (no dimensioned source), kept modest
#: so the lens (0.8 x ll, 0.7 x lw) still sits inside the narrowed body with
#: margin: see build_parts().
LANTERN_BODY_INSET_RATIO = 0.82

#: Wear proportions, all expressed as fractions of an already spec-derived
#: dimension so they scale if the spec ever does. D53 point 5: wear is
#: authored as a separable layer so its coverage can be printed; point 2:
#: THE FLOOR HAS NO NUMBER, so nothing here claims to be a bound, only a
#: reading. Exactly the three zones the brief names and no more: rain running
#: down the shaft, road spray at the bottom, staining below the lantern.
#:
#: WIDTHS REVISED 2026-09-21. road_spray and lantern_drip were fractions of
#: the local CIRCUMFERENCE (0.5x and, via a 2.4x neck-diameter multiplier,
#: over 2x a diameter): a flat standoff box that wide is wider than the
#: cylinder it sits on, so it cannot lie flush against the curve and instead
#: stands proud of the round silhouette as its own straight-edged shape.
#: Measured in the first render: this is what read as "a separate vertical
#: tab sticking up" beside the neck and as a visible fin beside the base,
#: not as staining. Both are now fractions of the local DIAMETER, capped
#: at 0.6 of it, so the flat chord stays within the round profile's own
#: projected width from most angles. rain_streak was already a diameter
#: fraction (0.35, i.e. already under 1) and is unchanged.
#:
#: road_spray's HEIGHT ALSO REVISED, same session, for a DIFFERENT reason:
#: the base became a taper (see build_parts()'s base construction) so its
#: true radius shrinks with height, and a flat panel positioned at one fixed
#: radius drifts away from the true surface the further up the taper it
#: reaches. 0.9 (covering almost the whole base height) would drift by
#: several centimetres at its own top edge; 0.35 keeps the patch low, where
#: the taper has only just started, so a single interpolated radius (taken
#: at the patch's own vertical centre, see build_parts()) stays close to
#: flush along its whole height. Physically apt anyway: road spray is
#: heaviest right at ground level.
WEAR = {
    "rain_streak": {"width_ratio_of_shaft_d": 0.35, "height_ratio_of_shaft_h": 0.85},
    "road_spray": {"height_ratio_of_base_h": 0.35, "width_ratio_of_base_d": 0.55},
    "lantern_drip": {"length_m": 0.16, "width_ratio_of_neck_d": 0.55},
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
#: grime's RGB REVISED 2026-09-21: the first render's wear boxes were both a
#: shape bug (see WEAR above) AND, independently, close enough to steel_dark
#: in raw value that even the correctly-shaped patches would read as barely
#: distinct at this object's on-screen size. This is a JUDGEMENT CALL, not a
#: sheet measurement: the sheet is not resolved enough at this crop to show
#: grime on a lamp column at all, and none is claimed from it. Brightened
#: roughly 60 percent over the previous value while keeping the same warm,
#: desaturated, brownish-black hue (still far darker than any clean painted
#: surface in the scene), so the two materials separate under the same
#: overcast lighting the base crop was read against rather than only in a
#: swatch. Roughness (0.90 vs steel's 0.42) is unchanged; that contrast was
#: never in question.
MATERIALS = (
    ("steel_dark", (0.021, 0.021, 0.024), 0.42),
    ("grime", (0.078, 0.061, 0.048), 0.90),
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
    under 90 degrees for every radius_ratio the selftest exercises in that
    range (1.05 through 4.0), so the arc gets longer as R grows over that
    whole range; arc_length is printed every run rather than assumed
    monotonic beyond what is tested. NONE OF THIS IS THE SHIPPED REGIME as
    of 2026-09-21: NECK_ARC_RADIUS_RATIO is 0.6, below 1, and sweep at 0.6
    is 131.81 degrees, well past the range above. The mathematical property
    above is still checked (it is a true, general fact about this formula,
    and the selftest still exercises it, now clearly labelled as informing
    the formula's behaviour rather than the shipped ratio), but it is not
    why 0.6 was chosen.

    THE TRADE-OFF THAT DECIDES THE SHIPPED RATIO, proved rather than
    tuned by eye. Because the lantern mount (lantern_z) sits BELOW mh (the
    shaft top) by a fixed amount independent of radius_ratio, arc_end_z
    ALWAYS ends up above lantern_z once sweep passes 0, so the dropper's
    EXTERNAL portion (the part that would show above the lantern housing's
    own top, at z = mh, i.e. arc_end_z - mh = R * sin(sweep)) is unavoidable
    for any single circular arc. Differentiate the trade-off rather than
    merely observe it: for radius_ratio in (0.5, 1] this external length
    GROWS MONOTONICALLY with radius_ratio (from exactly 0 at 0.5, the
    smallest radius that still reaches outreach_m at all, up through
    naive_curv's own 0.5 m at radius_ratio 1.0, to 0.7071 m at the
    2026-09-08 draft's 1.5), so a GENTLER curve (bigger R, lower curvature)
    ALWAYS makes the visible straight dropper LONGER, never shorter, given
    these pinned endpoints; there is no radius that is both gentle and
    dropper-free. 0.6 is chosen near the short end of that range: see
    NECK_ARC_RADIUS_RATIO's own comment for the exact bound it is chosen to
    clear (external dropper under lantern_width_m) and the module
    docstring's point 2 for the sheet reading that motivated preferring a
    short dropper over a shallow curve once both could not be had together.
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


def neck_bracket(params, radius_ratio=NECK_CORNER_RADIUS_RATIO, corner_segments=9):
    """A dict describing the neck's TIGHT CORNER (a true quarter circle,
    constant curvature, fixed at exactly 90 degrees so the LEVEL ARM that
    follows is tangent-continuous with it: no visible kink at that joint),
    the level arm itself, and the DROPPER that carries the arm's end down
    to the exact spec-pinned lantern mount. REPLACES neck_arc() (kept
    above, unused by the shipped path) as what ships, 2026-09-21 (same day,
    second revision): see the module docstring's point 2B for why, and
    NECK_CORNER_RADIUS_RATIO's own comment for the chosen radius.

    CLOSED FORM. The corner never needs to be solved for (unlike
    neck_arc()'s, whose sweep is wherever the circle first reaches
    outreach_m sideways): it is fixed at pi/2 by construction, so the
    endpoint algebra is direct rather than inverse trigonometry:

        R = radius_ratio * outreach_m                        (corner radius)
        corner: (0, mh) -> (R, mh+R), tangent rotates smoothly from
            vertical to horizontal over the fixed sweep of pi/2
        arm_length_m = outreach_m - R                         (must be > 0)
        arm: level at z = mh+R, from x=R to x=outreach_m
        dropper_length_m = (mh+R) - lantern_z = R + lantern_height_m/2
        curvature = 1/R on the corner, exactly 0 on the arm and the dropper

    radius_ratio must keep R strictly inside (0, outreach_m) or the arm has
    non-positive length; refused with ValueError rather than silently
    clamped, so a future edit to this ratio fails loudly instead of quietly
    shipping a shape that stopped reaching outreach_m (selftest exercises
    both the accepting case, the shipped ratio, and a planted rejecting
    case: reject/neck-bracket-refuses-radius-ratio-at-least-one).
    """
    mh = params["mounting_height_m"]
    reach = params["outreach_m"]
    lantern_z = mh - params["lantern_height_m"] * 0.5
    radius = radius_ratio * reach
    if not (0.0 < radius < reach):
        raise ValueError(
            "neck_bracket: radius_ratio=%.4f gives corner radius_m=%.4f, "
            "not inside (0, outreach_m=%.4f); the arm would have "
            "non-positive length" % (radius_ratio, radius, reach))
    corner_points = []
    for i in range(corner_segments + 1):
        t = (math.pi / 2.0) * i / float(corner_segments)
        corner_points.append([radius * (1.0 - math.cos(t)), 0.0,
                              mh + radius * math.sin(t)])
    arm_end_point = (reach, 0.0, mh + radius)
    arm_length = reach - radius
    dropper_length = (mh + radius) - lantern_z
    tangent_at_arm_end = (1.0, 0.0, 0.0)     # exact: the arm is level, by
                                              # construction, not measured
    dropper_dir = (0.0, 0.0, -1.0)
    joint_cos = max(-1.0, min(1.0, sum(a * b for a, b in
                                       zip(tangent_at_arm_end, dropper_dir))))
    return {
        "radius_m": radius, "radius_ratio": radius_ratio,
        "corner_sweep_deg": 90.0,
        "corner_points": corner_points,
        "arc_portion_length_m": radius * (math.pi / 2.0),
        "curvature_per_m": 1.0 / radius,
        "arm_end_point": arm_end_point, "arm_length_m": arm_length,
        # "dropper_start_point" is read by build_parts() (wear_lantern_drip),
        # plan_lines() (externalDropper_m) and selftest() (the same check):
        # the point the final straight vertical drop into the mount begins,
        # exactly what neck_arc()'s own "arc_end_point" meant when that
        # function's arc fed the dropper directly with no arm between them.
        "dropper_start_point": arm_end_point,
        "dropper_length_m": dropper_length,
        "joint_angle_deg": math.degrees(math.acos(joint_cos)),
        "mh": mh, "reach": reach, "lantern_z": lantern_z,
    }


def assembly_bbox(params, neck):
    """(width_m, height_m): the HEAD ASSEMBLY's own local X-Z envelope,
    CLOSED FORM from the same params and neck dict every other printed
    number here already trusts, not a second, independent source:

        width_m  = outreach_m + lantern_length_m/2   (shaft top, x=0, to the
                    roof's own outer edge, which overhangs the housing)
        height_m = neck["radius_m"] + lantern_height_m   (the corner/arm's
                    own peak, mh+radius_m, down to the lantern's bottom,
                    mh-lantern_height_m)

    Printed every run (lcAssembly) beside SHEET_REF["assembly_bbox_aspect"]
    and ASSEMBLY_SHEET_TARGET_ASPECT so the comparison is in the verdict.
    EXCLUDES the neck tube's own few-centimetre radius at the x=0 end (the
    neck is ~0.09 m across against a ~0.5-0.8 m assembly; folding it in
    would move the printed aspect by a few percent, not change the
    finding) and is a DIRECTIONAL figure, not a dimensioned one, for the
    same reason SHEET_REF's own confidence is rated low-to-moderate: see
    ASSEMBLY_ASPECT_TOLERANCE_PCT.
    """
    width = params["outreach_m"] + params["lantern_length_m"] / 2.0
    height = neck["radius_m"] + params["lantern_height_m"]
    return width, height


def neck_curve(params, radius_ratio=NECK_CORNER_RADIUS_RATIO, corner_segments=9):
    """neck_bracket()'s dict, plus "points" (the corner's own samples, then
    the arm's end, then the dropper's far end: one continuous list for
    _tube_verts) and "total_length_m" (corner arc length, plus arm length,
    plus dropper length: the whole tube's length)."""
    neck = neck_bracket(params, radius_ratio, corner_segments)
    points = [list(p) for p in neck["corner_points"]]
    points.append(list(neck["arm_end_point"]))
    points.append([neck["reach"], 0.0, neck["lantern_z"]])
    neck["points"] = points
    neck["total_length_m"] = (neck["arc_portion_length_m"] + neck["arm_length_m"]
                              + neck["dropper_length_m"])
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


def _cyl_verts(cx, cy, z0, z1, radius, segments, radius1=None):
    """Capped cylinder OR FRUSTUM, axis along Z, centred on (cx,cy). Two
    rings plus an n-gon fan cap at each end. `radius` is the ring at z0;
    `radius1` (default: same as radius, an ordinary cylinder, which is what
    every call site shipped before 2026-09-21 used and what the shaft and
    photocell still use) is the ring at z1. A tapered ring pair is still two
    PLANAR n-gons joined by PLANAR quads (a frustum face is a trapezoid, not
    a warped quad, for the same reason a cone's polygonal approximation
    always is), so mesh_check()'s Newell-normal and edge-sharing proof below
    needs no special case for this: it is exercised on both a taper and a
    true cylinder by selftest's mesh/* fuzz checks."""
    r1 = radius if radius1 is None else radius1
    bottom = [[cx + radius * math.cos(2 * math.pi * i / segments),
               cy + radius * math.sin(2 * math.pi * i / segments), z0]
              for i in range(segments)]
    top = [[cx + r1 * math.cos(2 * math.pi * i / segments),
            cy + r1 * math.sin(2 * math.pi * i / segments), z1]
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

    # TAPERED 2026-09-21, replacing a uniform cylinder. The first render's
    # flush step from a 0.2 m base to the 0.114 m shaft read as "a chunky
    # sleeve slipped over the shaft" against the Hook sheet, which shows no
    # visible collar at this camera distance. base_diameter_m still names
    # the WIDEST point (the foot, matching what cross_check compares it
    # against); the top of the taper meets shaft_diameter_m exactly, so
    # there is no step at the base/shaft joint at all.
    base_r0, base_r1 = bd / 2.0, sd / 2.0
    base_slant_m = math.hypot(base_r0 - base_r1, bh)
    v, f = _cyl_verts(0, 0, 0.0, bh, base_r0, CYLINDER_RADIAL_SEGMENTS, radius1=base_r1)
    parts.append({"id": "base", "kind": "frustum", "material": "steel_dark",
                  "verts": v, "faces": f,
                  "area_m2": math.pi * (base_r0 + base_r1) * base_slant_m, "wear_of": "base",
                  "note": "base_diameter_m at the foot tapering to shaft_diameter_m "
                          "at the top, no step at the shaft joint, column.surface=%s"
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
                  "note": "one continuous swept tube: a %.4f m radius quarter-"
                          "circle corner (fixed 90 degree sweep), then a "
                          "%.4f m level arm, then a %.4f m dropper, "
                          "total_length_m=%.4f"
                          % (neck["radius_m"], neck["arm_length_m"],
                             neck["dropper_length_m"], neck["total_length_m"])})

    lz0 = mh - lh   # bottom of the whole lantern assembly (box centred at mh - lh/2)
    # NARROWED 2026-09-21: the housing is authored at LANTERN_BODY_INSET_RATIO
    # of the full ll x lw envelope, so the roof/canopy (still full size, see
    # below) overhangs it on every side, the way a cobra-head fitting's hood
    # oversails its lamp chamber. The OVERALL lantern envelope used by
    # cross_check is unaffected: cross_check compares spec-derived scalars
    # against the blockout's own box, never this mesh's individual parts.
    lbl, lbw = ll * LANTERN_BODY_INSET_RATIO, lw * LANTERN_BODY_INSET_RATIO
    v, f = _box_verts(reach, 0, lz0 + lbh / 2.0, lbl, lbw, lbh)
    parts.append({"id": "lantern_body", "kind": "box", "material": "steel_dark",
                  "verts": v, "faces": f,
                  "area_m2": 2 * (lbl + lbw) * lbh + lbl * lbw, "wear_of": "lantern",
                  "note": "housing inset to %.2fx of length_m/width_m so the roof "
                          "overhangs it, height split body=%.4f roof=%.4f of "
                          "lantern_height_m=%.4f"
                          % (LANTERN_BODY_INSET_RATIO, lbh, lrr, lh)})

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
                  "verts": v, "faces": f,
                  # FIXED 2026-09-21: this printed area_m2=0.00000 every run, which
                  # the brief read (correctly) as suspicious for a 20-vertex,
                  # 12-face part. It was not a geometry problem: the literal was
                  # never computed, unlike every other part's area (compare base,
                  # shaft, neck above, each its own formula). Lateral surface only,
                  # matching the convention those use (no end caps counted).
                  "area_m2": 2 * math.pi * photocell_r * photocell_h, "wear_of": None,
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

    sp_w = WEAR["road_spray"]["width_ratio_of_base_d"] * bd
    sp_h = WEAR["road_spray"]["height_ratio_of_base_h"] * bh
    # THE BASE IS A TAPER (bd/2 at the foot, sd/2 at the top), so its true
    # radius at the patch's own mid-height is a linear blend between the two,
    # not the foot radius used before the base was tapered: using the foot
    # radius unchanged here would leave this patch floating clear of the
    # surface the further up the (now-narrowing) taper it reached.
    sp_z_frac = (sp_h / 2.0) / bh if bh > 0 else 0.0
    sp_base_r = (bd / 2.0) + sp_z_frac * ((sd / 2.0) - (bd / 2.0))
    sp_r = sp_base_r + WEAR_STANDOFF_M
    v, f = _box_verts(sp_r, 0, sp_h / 2.0, WEAR_STANDOFF_M * 2, sp_w, sp_h)
    parts.append({"id": "wear_road_spray", "kind": "box", "material": "grime",
                  "verts": v, "faces": f, "area_m2": sp_w * sp_h, "wear_of": "base",
                  "note": "road spray thrown up at the base, contained within "
                          "base_height_m, no cross-surface overlap with the shaft"})

    dr_l = min(WEAR["lantern_drip"]["length_m"], neck["dropper_length_m"] * 0.9)
    dr_w = WEAR["lantern_drip"]["width_ratio_of_neck_d"] * params["neck_diameter_m"]
    dr_r = params["neck_diameter_m"] / 2.0 + WEAR_STANDOFF_M
    drip_z = (neck["dropper_start_point"][2] + neck["lantern_z"]) / 2.0   # dropper midpoint
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
    assembly_width_m, assembly_height_m = assembly_bbox(params, neck)
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
        "assembly_width_m": assembly_width_m, "assembly_height_m": assembly_height_m,
        "assembly_aspect": (assembly_width_m / assembly_height_m
                            if assembly_height_m > 0 else 0.0),
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
    external_dropper_m = (neck["dropper_start_point"][2]
                          - plan["params"]["mounting_height_m"])
    lines.append(
        "lcNeck cornerRadius_m=%.4f cornerRadiusRatio=%.2f cornerSweep_deg=%.2f "
        "armLength_m=%.4f dropperLength_m=%.4f externalDropper_m=%.4f "
        "jointAngle_deg=%.2f "
        "authoredTotalLength_m=%.4f naiveQuarterArc_m=%.4f "
        "totalLongerThanNaive=%s totalRatio=%.4f "
        "cornerCurvature_perM=%.4f naiveQuarterCurvature_perM=%.4f "
        "shallowerThanNaive=%s curvatureRatio=%.4f "
        "naiveComparisonIsInformationalOnlyPer=2026-09-21-ruling "
        "constructionPer=2026-09-21-corner-arm-dropper-revision"
        % (neck["radius_m"], neck["radius_ratio"], neck["corner_sweep_deg"],
           neck["arm_length_m"], neck["dropper_length_m"], external_dropper_m,
           neck["joint_angle_deg"],
           plan["neck_arc_length_m"], plan["naive_arc_length_m"],
           "yes" if plan["neck_arc_length_m"] > plan["naive_arc_length_m"] else "no",
           plan["neck_arc_length_m"] / plan["naive_arc_length_m"],
           plan["neck_peak_curvature_per_m"], plan["naive_curvature_per_m"],
           "yes" if plan["neck_peak_curvature_per_m"] < plan["naive_curvature_per_m"] else "no",
           plan["neck_peak_curvature_per_m"] / plan["naive_curvature_per_m"]))
    # THE COMPARISON AGAINST THE SHEET ITSELF, replacing the naive quarter
    # circle as the thing this run reports itself against, per the brief
    # this revision answers: "print the new comparison against the sheet
    # rather than against a quarter circle." THIS LINE IS A STATIC, DATED,
    # SOURCED RECORD OF A ONE-TIME VISUAL MEASUREMENT, not a live recomputation:
    # this script cannot open a PNG concept sheet and measure it at run time,
    # and does not pretend to (see the module docstring's "what a printed
    # comparison against the sheet can and cannot be"). The figures below are
    # SHEET_REF_* constants, defined once, near NECK_ARC_RADIUS_RATIO, with
    # their own provenance; printing them here keeps the comparison in the
    # one file a reader of a run already has open, instead of only in a
    # report nobody archives beside the verdict.
    lines.append(
        "lcSheetRef source=%s cropPx=%s method=%s measuredAt=%s "
        "curveVerticalFraction_ofVisiblePole~=%s headWidthToHeight~=%s "
        "dropperVisibleOnSheet=%s confidence=%s"
        % (SHEET_REF["source"], SHEET_REF["crop_px"], SHEET_REF["method"],
           SHEET_REF["measured_at"], SHEET_REF["curve_vertical_fraction"],
           SHEET_REF["head_width_to_height"], SHEET_REF["dropper_visible"],
           SHEET_REF["confidence"]))
    # THE ACHIEVED-VS-SHEET COMPARISON ITSELF, printed so it is in the
    # verdict and not only in a report nobody archives beside it (Jafar,
    # 2026-09-21, on the 0.6-ratio render: "print the achieved aspect every
    # run beside the sheet's figure"). UNGATED per D41 (2026-09-08): visual
    # work, the studio compares the frame against the sheet and iterates;
    # no selftest check asserts withinTolerance=yes.
    delta_pct = (100.0 * (plan["assembly_aspect"] - ASSEMBLY_SHEET_TARGET_ASPECT)
                / ASSEMBLY_SHEET_TARGET_ASPECT)
    within_tol = abs(delta_pct) <= ASSEMBLY_ASPECT_TOLERANCE_PCT
    lines.append(
        "lcAssembly widthM=%.4f heightM=%.4f aspect=%.3f "
        "sheetTargetAspect=%.2f sheetTargetSource=%s "
        "deltaPct=%.1f toleranceAppliedPct=%.0f withinTolerance=%s "
        "toleranceBasis=own-remeasure-2026-09-21-9to11px-row-swing-2.27to2.78 "
        "gate=none/D41-ungated-visual-comparison"
        % (plan["assembly_width_m"], plan["assembly_height_m"],
           plan["assembly_aspect"], ASSEMBLY_SHEET_TARGET_ASPECT,
           SHEET_REF["source"], delta_pct, ASSEMBLY_ASPECT_TOLERANCE_PCT,
           "yes" if within_tol else "no"))
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
        "%s done: status=%s commission=%s runSha=%s studioSha=%s "
        "specSha256=%s specPath=%s "
        "crossCheckAgree=%d/%d "
        "objectsPlanned=%d objectsBuilt=%s manifoldParts=%d/%d "
        "neckArcLonger=%s neckShallower=%s "
        "wearCoverageMin=%.6f/%s wearCoverageTotal=%.6f "
        "boundsExtent_m=%s "
        "previewsWrote=%s "
        "engineAsked=%s engineUsed=%s res=%dx%d "
        "outDir=%s root=%s elapsedSeconds=%.1f"
        % (RECIPE_STEM, status, opts["commission"], opts["run_sha"],
           opts["studio_sha"],
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
        "artPreviewVerdict=1 commit=%s commission=%s recipe=%s status=%s at=%d"
        % (opts["run_sha"], opts["commission"], RECIPE_STEM, status, stamp),
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
    return ("artPreviewVerdict=1 commit=%s commission=%s recipe=%s "
            "status=NO-RUN at=%d\n\n"
            "NO RUN - the recipe refused before any frame was rendered.\n"
            "%s refused: status=NO-RUN reason=%s root=%s outDir=%s "
            "previewsWrote=0/0-shots-reached nothing measured\n"
            % (opts["run_sha"], opts["commission"], RECIPE_STEM, stamp,
               RECIPE_STEM, reason, opts["root"].replace(" ", "~"),
               (opts["out"] or "none").replace(" ", "~")))


def receipt_dict(plan, opts, built, frames, status, seconds):
    return {
        "schema": "ledger.art-preview.receipt/1",
        "status": status, "recipe": RECIPE_STEM,
        "commission": opts["commission"],
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
           "studio_sha": "not-passed", "commission": "not-passed",
           "blend": True, "dry_run": False,
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
        elif a == "--commission":
            # THE LANE ALWAYS PASSES THIS AND THIS RECIPE READS NO COMMISSION
            # DATA, which are both true at once and neither is a reason to
            # ignore it. The workflow renders into
            # production/art/<commission>/previews and commits to
            # art/<commission>, so the name is this run's PUBLICATION
            # IDENTITY; it is validated exactly as mickeys-blockout.py
            # validates it (it reaches a path and a branch ref) and recorded on
            # line 1 of the verdict, in the done line and in the receipt,
            # beside the same key the workflow's own NO-RUN verdicts carry.
            # What it does NOT do here, unlike mickeys-blockout.py, is locate
            # input files: this recipe's input is production/specs/, which is
            # commission-independent. Recorded, not used to read: that is the
            # whole difference, and it is written down rather than left as a
            # silent no-op.
            v = need(a)
            if v is None:
                break
            if not v or set(v) & ID_BAD or ".." in v:
                out["error"] = "commission-is-not-a-plain-name/" + v.replace(" ", "~")
                break
            out["commission"] = v
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


def _lane_flags_from_tokens(tokens):
    """Tokens after a bare `--`, paired into (flag, takes-a-value).

    A token starting with `--` is a flag; the token after it is its VALUE
    SLOT unless that token is itself a flag. That is the whole grammar the
    lane uses, and reading it this way means a flag ADDED to the lane later
    arrives here on its own, which a retyped list cannot do.
    """
    flags = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if not token.startswith("--"):
            i += 1
            continue
        takes_value = i + 1 < len(tokens) and not tokens[i + 1].startswith("--")
        flags.append((token, takes_value))
        i += 2 if takes_value else 1
    return flags


def lane_contract(root=None):
    """THE ARGUMENT CONTRACT, READ OUT OF THE LANE AT TEST TIME.

    Run 35649856734 failed because this recipe's selftest tested the flags
    the AUTHOR chose and the lane sends a different set: 48/48 green, and the
    first real invocation died on `unknown-flag/--commission`. A list of flag
    names retyped into the test would have gone stale exactly the same way
    (queue 416's snapshot fault), so the list is DERIVED from the two files
    that are the lane:

        .github/workflows/ledger-art-blender-preview.yml   the Blender
            invocation the self-hosted runner executes, read as text and
            tokenised after its bare `--`.
        tools/art-recipes/run-recipe.py   the wrapper any human or job uses,
            asked for its argv by CALLING build_argv() rather than reading it.

    Returns (flags, sources). `flags` is an ordered, deduplicated list of
    (flag, takes-a-value) merged across the sources; `sources` is one
    (name, status, relpath) per source TRIED, so a source that could not be
    read is a named zero rather than a shorter list. Both counts are printed
    by selftest(): a contract derived from nothing must never read as a
    contract that passed.

    Searched relative to this file's own ROOT rather than --root: on the
    runner --root is the workspace ABOVE the studio checkout and holds no
    .github, while this file always sits inside the studio checkout.
    """
    base = root or ROOT
    sources = []
    flags = []

    workflow = os.path.join(base, LANE_WORKFLOW_REL)
    matched = []
    try:
        with open(workflow, encoding="utf-8") as handle:
            for number, line in enumerate(handle, 1):
                tokens = line.split()
                if "--python" not in tokens:
                    continue
                rest = tokens[tokens.index("--python"):]
                if "--" not in rest:
                    continue
                found = _lane_flags_from_tokens(rest[rest.index("--") + 1:])
                if found:
                    matched.append((number, found))
    except OSError as exc:
        sources.append(("workflow", "unreadable/" + type(exc).__name__,
                        LANE_WORKFLOW_REL))
    else:
        if matched:
            for _, found in matched:
                flags.extend(found)
            sources.append(("workflow",
                            "read/" + "+".join("L%d" % n for n, _ in matched),
                            LANE_WORKFLOW_REL))
        else:
            sources.append(("workflow", "no-blender-invocation-line-matched",
                            LANE_WORKFLOW_REL))

    wrapper = os.path.join(base, LANE_WRAPPER_REL)
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("lane_wrapper_probe_9xz",
                                                      wrapper)
        if spec is None or spec.loader is None:
            raise ImportError("no-loader-for-" + LANE_WRAPPER_REL)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        argv = list(module.build_argv("blender", "recipe.py", "OUTDIR"))
        found = (_lane_flags_from_tokens(argv[argv.index("--") + 1:])
                 if "--" in argv else [])
    except Exception as exc:  # an unreadable wrapper is a finding, not a crash
        sources.append(("run-recipe", "unreadable/" + type(exc).__name__,
                        LANE_WRAPPER_REL))
    else:
        if found:
            flags.extend(found)
            sources.append(("run-recipe", "read/build_argv", LANE_WRAPPER_REL))
        else:
            sources.append(("run-recipe", "build_argv-emitted-no-flags",
                            LANE_WRAPPER_REL))

    merged, seen = [], {}
    for flag, takes_value in flags:
        if flag in seen:
            seen[flag][1] = seen[flag][1] or takes_value
        else:
            seen[flag] = [flag, takes_value]
            merged.append(seen[flag])
    return [(flag, takes) for flag, takes in merged], sources


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
        # "shallower/longer than the naive quarter circle" ARE NO LONGER
        # GATES, as of the 2026-09-21 iteration: Jafar's ruling on the first
        # render read that baseline as never having been the reference, and
        # passing it as having proved nothing about the sheet. Both figures
        # are still computed and printed every run (see lcNeck in
        # plan_lines()), now as labelled, informational numbers only. The
        # length comparison happens to still hold at the shipped ratio
        # (checked below, not asserted here) but that is a fact about this
        # one ratio, not a requirement the file enforces.
        check("accept/naive-quarter-circle-comparison-is-computed-not-asserted",
              naive_len > 0.0 and naive_curv > 0.0,
              "len=%.4f curv=%.4f, informational only, see module docstring "
              "point 2" % (naive_len, naive_curv))
        check("accept/neck-starts-exactly-at-shaft-top",
              neck["points"][0] == [0.0, 0.0, params["mounting_height_m"]])
        check("accept/neck-ends-exactly-at-spec-lantern-mount",
              abs(neck["points"][-1][0] - params["outreach_m"]) < 1e-9 and
              abs(neck["points"][-1][2] - (params["mounting_height_m"]
                                           - params["lantern_height_m"] * 0.5)) < 1e-9)
        # THE GATE THAT REPLACES IT, tied to a spec-derived scale rather than
        # to a baseline the sheet never supported: the EXTERNAL dropper (the
        # part of the straight run above the lantern housing's own top,
        # z = mounting_height_m, where the "tab" the first render showed
        # actually reads) must stay shorter than the lantern's own width, so
        # any residual straight stub reads as subordinate to the fitting it
        # feeds into rather than as a separate rod. Since the 2026-09-21
        # corner+arm+dropper revision this is exactly the corner's own
        # radius_m (the arm sits level at mh+radius_m, so the whole external
        # run above the housing IS the corner's radius); NECK_CORNER_RADIUS_
        # RATIO's own comment explains why this is a requirement the shipped
        # ratio is chosen to clear, not an arbitrary bound.
        external_dropper_m = (neck["dropper_start_point"][2]
                              - params["mounting_height_m"])
        check("accept/external-dropper-shorter-than-lantern-width",
              0.0 <= external_dropper_m < params["lantern_width_m"],
              "%.4f m vs lantern_width_m=%.4f m"
              % (external_dropper_m, params["lantern_width_m"]))
        # CONSTANT CURVATURE, VERIFIED ON THE ACTUAL SAMPLED POINTS rather
        # than trusted from the formula that generated them: every point on
        # the CORNER (the arm and dropper are straight, zero curvature, and
        # do not lie on this circle at all except at the corner's own last
        # point, which is also the arm's first) must sit at exactly
        # radius_m from the corner's own centre (radius_m, mounting_height_m).
        cx, cz, R = neck["radius_m"], params["mounting_height_m"], neck["radius_m"]
        radii = [math.hypot(p[0] - cx, p[2] - cz) for p in neck["corner_points"]]
        check("accept/neck-corner-points-lie-on-one-circle-of-the-authored-radius",
              all(abs(r - R) < 1e-6 for r in radii),
              "maxDeviation=%.8f over %d points" % (max(abs(r - R) for r in radii), len(radii)))
        # THE ARM IS LEVEL AND THE DROPPER IS VERTICAL, verified on the
        # actual sampled points rather than assumed from the construction:
        # this is the claim the sheet comparison (module docstring point
        # 2B, lcAssembly) rests on, so it is checked here, not only implied
        # by neck_bracket()'s own math.
        corner_end_z = neck["corner_points"][-1][2]
        check("accept/neck-arm-is-level",
              abs(neck["arm_end_point"][2] - corner_end_z) < 1e-9,
              "armEnd.z=%.6f vs corner's own last sample.z=%.6f"
              % (neck["arm_end_point"][2], corner_end_z))
        check("accept/neck-dropper-is-vertical",
              abs(neck["points"][-1][0] - neck["arm_end_point"][0]) < 1e-9,
              "dropperEnd.x=%.6f vs armEnd.x=%.6f"
              % (neck["points"][-1][0], neck["arm_end_point"][0]))
        check("accept/neck-joint-is-a-right-angle-arm-to-dropper",
              abs(neck["joint_angle_deg"] - 90.0) < 1e-6,
              "%.6f" % neck["joint_angle_deg"])
        # THE ASSEMBLY ASPECT ITSELF IS PRINTED, NOT GATED (D41, 2026-09-08:
        # visual work, ungated, the studio compares and iterates), so only
        # its ARITHMETIC is checked here, not its proximity to the sheet.
        aw, ah = assembly_bbox(params, neck)
        check("accept/assembly-width-is-reach-plus-half-lantern-length",
              abs(aw - (params["outreach_m"] + params["lantern_length_m"] / 2.0))
              < 1e-9)
        check("accept/assembly-height-is-corner-radius-plus-lantern-height",
              abs(ah - (neck["radius_m"] + params["lantern_height_m"])) < 1e-9)
        # THE GUARD ON radius_ratio, TESTED ON BOTH THE CASE IT SHOULD PASS
        # AND A PLANTED CASE IT MUST REFUSE (instruments.md 5b): a ratio
        # that puts the corner radius at or past outreach_m, where the arm's
        # length would be zero or negative, must raise.
        try:
            neck_bracket(params, radius_ratio=NECK_CORNER_RADIUS_RATIO)
            guard_accepts_shipped = True
        except ValueError:
            guard_accepts_shipped = False
        check("accept/neck-bracket-accepts-the-shipped-radius-ratio",
              guard_accepts_shipped)
        try:
            neck_bracket(params, radius_ratio=1.2)
            guard_rejected_oversized = False
        except ValueError:
            guard_rejected_oversized = True
        check("reject/neck-bracket-refuses-radius-ratio-at-least-one",
              guard_rejected_oversized)

        # THE CLOSED-FORM PROOF, exercised over a RANGE of radius ratios that
        # does NOT include the shipped value (0.6, since 2026-09-21): this
        # checks a general, still-true property of neck_arc()'s formula for
        # ratio > 1 (this is the check that would have caught the earlier
        # Bezier draft's failure before it was ever printed, and it still
        # would if the formula regressed), not a claim about what ships. The
        # shipped ratio's own behaviour is checked above instead.
        all_shallower = all(neck_arc(params, k)["curvature_per_m"] < naive_curv
                            for k in (1.05, 1.2, 1.5, 2.0, 3.0, 4.0))
        check("accept/formula-is-shallower-than-naive-for-every-ratio-above-one-tested",
              all_shallower)
        sweeps_under_90 = all(neck_arc(params, k)["sweep_deg"] < 90.0
                              for k in (1.05, 1.2, 1.5, 2.0, 3.0, 4.0))
        check("accept/formula-sweep-stays-under-90-degrees-for-every-ratio-above-one-tested",
              sweeps_under_90)

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

    # --- THE LANE'S OWN CONTRACT, derived rather than retyped. This block is
    # the one that would have caught run 35649856734: every check above tests
    # a flag this file's author chose, and the lane sends --commission. See
    # lane_contract() for where the list comes from and why it is read at test
    # time. The accepting fixture is the live lane (the workflow and the
    # wrapper as they stand in this checkout); the rejecting fixture is
    # synthetic, a flag name that exists in no lane, below. ---
    lane, lane_sources = lane_contract(root)
    for name, status, rel in lane_sources:
        check("lane/source-read/%s" % name, status.startswith("read"),
              "%s status=%s" % (rel, status))
    sources_read = sum(1 for _, s, _ in lane_sources if s.startswith("read"))
    check("lane/contract-derived-at-all", len(lane) > 0,
          "flagsDerived=0 sourcesRead=%d/%d-named nothing measured"
          % (sources_read, len(lane_sources)))
    # A VALUE THAT IS VALID FOR A NAME-SHAPED FLAG AND FOR NOTHING ELSE. The
    # assertion below is about RECOGNITION, not about value shapes: a lane
    # flag that takes a typed value (a --res the lane does not send today)
    # would refuse this placeholder BY SHAPE, which is a different and
    # non-failing fact, counted separately and printed. Only
    # `unknown-flag/<flag>` is the fault this catches.
    probe = "lane-probe"
    # Prefixed with --out because a probe missing it refuses with
    # `missing-flag/--out`, an error about the probe rather than about the
    # flag under test. --out is itself in the derived list; if it ever left
    # the lane this prefix would only make the probe stricter, never laxer.
    recognised, shape_refused = 0, []
    for flag, takes_value in lane:
        argv = ["x.py", "--", "--out", probe, flag] + ([probe] if takes_value else [])
        err = parse_args(argv)["error"]
        ok = err != "unknown-flag/" + flag
        check("lane/flag-recognised/%s" % flag, ok, err or "accepted")
        recognised += 1 if ok else 0
        if ok and err:
            shape_refused.append("%s..%s" % (flag, err))
    whole = ["x.py", "--"]
    for flag, takes_value in lane:
        whole.append(flag)
        if takes_value:
            whole.append(probe)
    whole_err = parse_args(whole)["error"]
    check("lane/whole-invocation-line-carries-no-unknown-flag",
          not whole_err.startswith("unknown-flag/"), whole_err or "accepted")
    # THE PRINTED SERIES, so a green run says how much it looked at. Zero
    # derived flags print "nothing measured" and the check above is already
    # red: a contract derived from nothing must never read as one that passed.
    print("%s laneContract: sourcesRead=%d/%d-named flagsDerived=%d "
          "flagsRecognised=%d/%d-derived valueShapeRefused=%d/%d-derived "
          "wholeLine=%s flags=%s %s%s"
          % (RECIPE_STEM, sources_read, len(lane_sources), len(lane),
             recognised, len(lane), len(shape_refused), len(lane),
             (whole_err or "accepted").replace(" ", "~"),
             "/".join(f for f, _ in lane) or "none",
             " ".join("source/%s=%s..%s" % (n, r.replace(" ", "~"), s)
                      for n, s, r in lane_sources),
             "" if lane else " nothing measured"))
    if shape_refused:
        print("%s laneContractNote: valueShapeRefused=%d/%d-derived flags=%s "
              "(recognised but the name-shaped probe value was refused, which "
              "is not an unknown flag)"
              % (RECIPE_STEM, len(shape_refused), len(lane),
                 "/".join(shape_refused)))

    # --- WHAT A REFUSAL LEAVES BEHIND. Run 35649856734's second fault: the
    # BAD-ARGS refusal fired before --out was established and wrote nothing at
    # all, so a contract mismatch produced total silence and the only evidence
    # was one line in a job log. main() is driven here for real, in a
    # temporary directory, and the FILE ON DISK is what is asserted, not the
    # code path. ---
    import contextlib
    import io
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        out_dir = os.path.join(td, "previews")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = main(["x.py", "--", "--out", out_dir, "--root", root,
                         "--commission", "atlas-01", "--run-sha", "deadbee",
                         "--not-a-lane-flag-9xz"])
        said = buf.getvalue()
        path = os.path.join(out_dir, RECIPE_STEM + "-verdict.txt")
        wrote = os.path.exists(path)
        text = open(path, encoding="utf-8").read() if wrote else ""
        check("refusal/bad-args-exits-2", code == 2, "exit=%s" % code)
        check("refusal/bad-args-writes-a-verdict-file-when---out-parsed",
              wrote and len(text) > 0,
              "path=%s bytes=%d" % (path, len(text)))
        check("refusal/bad-args-verdict-line-1-is-the-lane-format",
              text.split("\n")[0].startswith("artPreviewVerdict=1 ")
              and "status=NO-RUN" in text.split("\n")[0],
              text.split("\n")[0] or "empty-file")
        check("refusal/bad-args-verdict-names-the-rejected-flag",
              "--not-a-lane-flag-9xz" in text, text[:120] or "empty-file")
        # The workflow's gate greps this key out of the committed file
        # (ledger-art-blender-preview.yml, "Gate on what was measured"), so a
        # refusal verdict without it is a file the gate cannot read.
        check("refusal/bad-args-verdict-carries-previewsWrote-for-the-gate",
              "previewsWrote=0/0-shots-reached" in text
              and "nothing measured" in text, text[:120] or "empty-file")
        check("refusal/bad-args-stdout-names-the-path-and-the-byte-count",
              "verdict: path=" in said and "bytes=%d" % len(text) in said,
              said.strip().replace("\n", " | ") or "silent")
    # AND THE OTHER HALF, which is a different fact: with no usable --out
    # nothing CAN be written, and the recipe has to say so in those words
    # rather than fall silent, because "could not" and "chose not to" are not
    # the same finding.
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = main(["x.py", "--", "--root", root, "--not-a-lane-flag-9xz"])
    said = buf.getvalue()
    check("refusal/no-out-dir-exits-2", code == 2, "exit=%s" % code)
    check("refusal/no-out-dir-says-it-could-not-write-a-verdict",
          "could not write a verdict" in said
          and "verdictWritten=0/1-expected" in said,
          said.strip().replace("\n", " | ") or "silent")

    # --- rejecting fixtures: synthetic, exist nowhere in this repo ---
    # THE LANE CHECK'S OWN REJECTING CASE: a flag no lane sends must still be
    # refused by name, so the recognition assertion above cannot be satisfied
    # by a parser that accepts everything.
    check("reject/lane-shaped-flag-that-exists-in-no-lane",
          parse_args(["x.py", "--", "--out", "o", "--not-a-lane-flag-9xz",
                      "v"])["error"] == "unknown-flag/--not-a-lane-flag-9xz")
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
        # A BAD-ARGS REFUSAL LEAVES THE SAME RECORD EVERY OTHER REFUSAL
        # LEAVES, WHEN IT CAN. Measured on run 35649856734 (job 106499292604,
        # 2026-09-21, the first real Blender run): this recipe refused
        # `unknown-flag/--commission` during argument parsing, which is BEFORE
        # the output directory was established, so it wrote no PNG, no verdict
        # and staged nothing, and the only evidence of the whole run was one
        # line in a job log. The workflow's gate caught the silence correctly
        # (artGateStatus=NO-VERDICT) and published nothing false, but a refusal
        # whose own record does not survive is the fault being fixed here.
        #
        # --out IS KNOWN THE MOMENT IT PARSES, and the lane passes it first, so
        # a flag rejected later in the line still has a directory to write to.
        # The two outcomes are printed as DIFFERENT FACTS: a verdict written
        # (path and bytes) versus could not write a verdict (and why), never a
        # silence that reads like a choice.
        print("%s refused: status=BAD-ARGS reason=%s nothing measured"
              % (RECIPE_STEM, opts["error"]))
        if opts["out"]:
            _write_refusal(opts, "BAD-ARGS/" + opts["error"])
        else:
            print("%s note: verdictWritten=0/1-expected "
                  "reason=no-out-dir-parsed/--out-absent-or-valueless "
                  "(could not write a verdict here, which is not the same "
                  "fact as chose not to) nothing measured" % RECIPE_STEM)
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
    """The refusal's own record, written wherever --out reached.

    Returns True when the file is on disk. The failure branch says COULD NOT
    WRITE A VERDICT in those words, because a reader who finds no file needs
    to tell a refused write from a refusal that never tried: the second is a
    decision, the first is a broken output directory.
    """
    out_dir = os.path.abspath(opts["out"])
    path = os.path.join(out_dir, RECIPE_STEM + "-verdict.txt")
    text = refusal_verdict(opts, reason)
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        size = os.path.getsize(path)
    except OSError as exc:
        print("%s note: verdictWritten=0/1-expected "
              "reason=out-dir-unusable/%s outDir=%s "
              "(could not write a verdict here, which is not the same fact as "
              "chose not to) nothing measured"
              % (RECIPE_STEM, type(exc).__name__, out_dir.replace(" ", "~")))
        return False
    print("%s verdict: path=%s bytes=%d lines=%d status=NO-RUN cause=%s"
          % (RECIPE_STEM, path.replace(" ", "~"), size, text.count("\n"),
             reason.replace(" ", "~")))
    return True


if __name__ == "__main__" or bpy is not None:
    sys.exit(main(sys.argv))
