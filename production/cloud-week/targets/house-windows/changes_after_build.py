"""Changes after the build: the changes to target.json and TARGET.md that the two fresh reviews of the BUILT kit asked for (cloud week 42, unit 8, try 1 reviews, 14 October 2026).

The target was written, reviewed and fixed on 13 October and the kit built to it on 14 October; the street review (REVIEW-v1-street.md) and the close review (REVIEW-v1-close.md) of the built kit found that some of the target's rows were
mis-set (WB-03, WB-07, NIGHT-01, NIGHT-02), that the lit room's gain was wrong (7.1 and 9: x 0.7 x 0.4), and that rows were missing (the glass of the kit's own slab, a lit window's clear glass against its net, clipped highlights, black joinery,
the grime band). This script applies those changes, each marked "14 Oct, from the try 1 reviews", to target.json and TARGET.md, and adds a "Changes after the build" section to both. It is idempotent (run it again and nothing changes) and
must be run again after any regeneration by make_target.py and make_doc.py, which do not know these changes: the author tools stay as they were on 13 October so that the record of what the review saw is kept.

Second round (14 October 2026, the try 3 of the build): the two fresh reviews of the try 2 build (REVIEW-v2-street.md, REVIEW-v2-close.md) both PASSED under Jafar's ruling of 9 October with narrow points; the points that touch the target are applied here, each marked
"14 Oct, from the try 2 reviews" (MARK3) in TARGET.md section 14 and in target.json `changes_after_the_build` (`round_2`). The first round's rows above are kept as they stand; the second round updates the rows named in CHANGED_3 and adds the rows in NEW_3.

Run: python3 changes_after_build.py   (no Blender; json and re only)
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TJ = os.path.join(HERE, "target.json")
TM = os.path.join(HERE, "TARGET.md")
MARK = "14 Oct, from the try 1 reviews"
MARK3 = "14 Oct, from the try 2 reviews"
SEC = "## 14. Changes after the build"
SEC3 = "### 14.2 Changes after the build, second round"
GF_NIGHT_LIT_MEAN = None         # the cottages' front rooms' night_lit mean luma standard (the relit pictures' mean, +-15 per cent), filled in when the pictures are rendered

STATUS_JSON = "built (unit 8, 14 October 2026); changes after the build from the two try 1 reviews and, in the second round, from the two try 2 reviews (which passed with narrow points) applied 14 October 2026 (changes_after_the_build, TARGET.md section 14); the second round's changed rows are not re-reviewed"

# -------------------------------------------------------------------------------------------------------------------------------------------- the changed and the new rows
CHANGED = {
    "MAT-04": {
        "measure": "render the kit's own slab pane (the glb's glass__lower node: a closed 2.5 mm slab, a front and a back face) with the pane shader at 16 degrees from the wall: (a) against a uniform sky of luma 1.0 with the room black; (b) against the same sky with the room a uniform card of 1.0 behind it",
        "expected": "(a) the pane's luma 0.26 of the sky with F0 0.08 (Schlick at 74 degrees from the normal: Unreal's own figure for Specular 1, 1a section 2); Cycles' dielectric Fresnel at specular level 1.0 may read up to 0.31; (b) 1.0 of the sky and the card: what the pane reflects and what it passes add up to the whole, no light is lost in the slab (the back face is not a mirror)",
        "tolerance": "+-0.05 each",
        "source": "1a Fresnel table: true two-face 0.38, Unreal 0.26; " + MARK + ": redone on the slab, not on a single plane (a single plane passed a pane whose back face was a total mirror; reading (a) alone cannot see that mirror, reading (b) does); negative control NEG-01",
    },
    "WB-03": {
        "expected": "0.35 to 0.90 and blue minus red at least -3 levels (the pane is no warmer than the neutral overcast dome it reflects)",
        "source": "P8_L, P8_R: 0.59, 0.49, all four panes together 0.57; (85, 100, 133); " + MARK + " (street review N1, close review): the old band 0.35 to 0.70 and blue over red 10 came from P8, a clear blue sky; the game's sky is the overcast dome (the scene file's, the Hook sheet), neutral; P3_d 0.36, P8 0.49 to 0.59, P6_up 0.89 with sky in its glass",
    },
    "WB-07": {
        "expected": "3.0 to 9.0 for white_fresh and white_upvc; 2.5 to 9.0 for white_grimy and white_flaking",
        "source": "P1 3.75 and P8 4.1 on photographs (film contrast; L the joinery's 90th percentile); the game's albedos give 0.82/0.13 = 6.3; the concept sheet's 7 is outside the photographs; " + MARK + " (street review N2, close review): the floor 3.0 sits at 0.8 of the lowest photograph (P1, 3.75) taken for sound white; 2.5 is 3.0 x 0.66 / 0.82 for the grimy paint, rounded up so that a dull frame still reads clearly above its brick (the close review's 2.2 for white_flaking alone is 3.0 x 0.58 / 0.81; the street review's 2.5 is used for both dull paints and the close review's figure passes too)",
    },
    "NIGHT-01": {
        "measure": "at 20:30 over the 20 street windows (GS_A and GS_B together, rendered from the one camera that sees each squarely): a window is LIT when its pane median luma is at least 2.5 times the dark windows' median luma and the pane's mean linear colour has r > g > b; DARK when its CLEAR (net-free) glass reads 8 to 35 (NIGHT-04) and its net, if it has one, reads at most 0.7 of its own frame's L at night (the game's own night sky light, sky_light_gain_night 0.15, lights a dark window's net as it lights the frame). The clear glass and the net are told apart by the mask with the glass clear. The absolute emissions of the curtains, blinds and the landing bulb (`night_lit_emission_linear`, `landing_bulb`) are starting values, not the pass line",
        "source": "rooms.lit_share; TARGET-REVIEW narrow point 5; " + MARK + " (street review F2 cause 3): the dark band 8 to 30 counted a net window's net, which no net window can meet (a dark net reads 0.51 to 0.64 of its frame under the night sky light, the clear glass of a dark room 16 to 17); the close review's wording, per window against its own frame (dark P/L at most 0.70, lit P/L at least 1.0 with r > g > b), is reported beside the street rule and not failed",
    },
    "NIGHT-02": {
        "measure": "the median pane luma of the lit windows over that of the dark windows, night; the pane against the pane (the clear glass and the net together as seen), like for like",
        "expected": "at least 2.5 (linear at least 6)",
        "source": "NIGHT-2026-10-08.md: real lit windows are 10 to 100 times the lit paving (the game's exposure: OWED-07); " + MARK + " (street review F2 cause 3, close review): the old 4 rested on a dark pane with no lit net in it; with the game's own night sky light on a dark net, and the lit card at x 1.0, the street review expects 2.6 to 2.8; the close review asks 2.0 against each window's own frame",
    },
    "NIGHT-03": {
        "measure": "a lit net's mean colour (linear) ratio r:g:b; a lit curtain's or blind's mean colour; and, block by block, every 32 x 32 px block lying wholly inside a lit pane in every night frame",
        "expected": "net: r > g > b, g/r 0.55 to 0.80, b/r 0.20 to 0.45 (tungsten 2700 K and the fabric); curtain or blind: its own colour x that light (curtains.*.night_lit_emission_linear): r > g > b for the cream and brown curtains and the white and cream blinds (the brown curtain's g/r is 0.39); a green curtain's g > r is its own colour and none is lit at 20:30; every 32 x 32 block of a lit pane: r > g > b and linear g/r at most 0.85",
        "source": "interior_lit (1.0, 0.714, 0.344); " + MARK + " (close review fault 2): a row that averages the whole pane missed an olive band round a clipped ceiling light (g/r 1.0, 17 per cent of the lit window's glass at the tight close view)",
    },
}

NEW = [
    ("MAT-04", {
        "id": "GLS-06", "group": "glass", "name": "the glass passes the room at every angle from the wall",
        "measure": "render the kit's own glass__lower node, exported as it is (a closed 2.5 mm slab: a front and a back face), with the pane shader at 15, 20, 35, 50 and 70 degrees from the wall in front of an emission card of 0.5 under a black sky",
        "expected": "the card through the pane reads at least (1 - F_front(angle)) of its own, less 0.03 (F_front: the dielectric Fresnel of the one front face at IOR 1.789: 0.29 at 15 degrees from the wall, 0.21 at 20, 0.11 at 35, 0.09 at 50, 0.08 at 70); the first build read 0.00 at 15 to 50 degrees (its back face was a total mirror past the critical angle)",
        "tolerance": "limit", "applies_to": "the pane material", "kind": "Derived",
        "source": MARK + ": street review F1 fix 4 (15, 20, 35, 50 degrees), close review fault 1 fix 3 (at least 0.75 of itself at 20 and 70 degrees: met); the negative control NEG-01 makes the back face a mirror again and must fail this row and MAT-04"}),
    ("WB-09", {
        "id": "JNR-01", "group": "gate", "name": "no black joinery by day",
        "measure": "by day, in every window of every day frame: the joinery pixels (material index 2) inside the window's outline whose luma is under 10",
        "expected": "none: at most 0.1 per cent of the window's joinery pixels (the anti-aliased edge between the mask and the beauty frame); the first build's black notch at the head of the far jamb was 0.9 per cent of one window's joinery",
        "tolerance": "limit", "applies_to": "GS_A GS_B", "kind": "Derived",
        "source": MARK + ": close review narrow point 1 (the stand-in wall's opening cut exactly at the kit's lining planes, so faces shared the brick's planes: a joinery face that got no light, about 35 x 35 mm)"}),
    ("JNR-01", {
        "id": "GRM-01", "group": "kit", "name": "the grime band on grimy windows",
        "measure": "the kit's own bottom rail (paint_joinery__lower_bottom_rail) painted as a grimy house's, square on under a uniform sky: the luma of its lowest 30 mm over that of the 30 mm above them; the same for a sound house",
        "expected": "grimy 0.68 to 0.85 (the band x 0.75 on top of the rail's x 0.85); sound 0.97 or more (a sound house's rail is clean)",
        "tolerance": "band", "applies_to": "grimy windows (east_parade_bay0, west_south_bay0)", "kind": "Judgement",
        "source": MARK + ": close review narrow point 3 (target 4.2 says a grime band 30 mm high along the sill; only the x 0.85 was built); the factor 0.75 is the close review's, a Judgement within the box shade and above KIT-09's floor of 0.25. The band is the gate's by the house's condition and is listed per site in hw_manifest.json for the PC (the glb carries the default paint of every house of its kind, so a band baked into its COLOR_0 would dirty the sound houses)"}),
    ("NIGHT-05", {
        "id": "NIGHT-07", "group": "gate", "name": "a lit window's clear glass against its net",
        "measure": "in every lit window of H_ACROSS_0 at night: the clear (net-free) glass's linear luminance over its lit net's, curtain's or blind's, each the MEAN over its region, the two regions told apart by the mask with the glass clear (the street review wrote 'median'; its own figures, 0.26 to 0.31 at the old gain and 0.6 to 0.8 at 1.0, reproduce with the mean: the median of the clear glass is dominated by the dim upper sash and the walls under a bright transom and ceiling and reads 0.27 at gain 1.0, so it is reported beside)",
        "expected": "0.5 to 1.0",
        "tolerance": "band", "applies_to": "GS_A GS_B", "kind": "Judgement",
        "source": MARK + ": street review F2 cause 2: with the lit card at x 0.28 (picture x 0.7 x 0.4) the room seen through clear glass read 0.26 to 0.31 of the lit net, which glows 0.48 from the same light that lights the room; with the card at x 1.0 the clear glass reads 0.6 to 0.8 of the net (street review); the PC's M_LedgerInterior Brightness for a lit house room at night follows (OWED-04 measures it)"}),
    ("PIC-08", {
        "id": "PIC-13", "group": "pictures", "name": "no clipped highlights in a lit room picture",
        "measure": "in every night_lit picture, the share of pixels with any channel at 250 or more",
        "expected": "at most 0.1 per cent: the highlights are rolled off before the 8-bit write (the pixel's largest channel in linear eases from a knee of 0.60 toward 0.85 and never reaches it; the three channels scale together, so the hue stays tungsten)",
        "tolerance": "limit", "applies_to": "the 11 lit rooms (an empty room's night_lit is its night_dark)", "kind": "Derived",
        "source": MARK + ": close review fault 2: every lit picture clipped round the ceiling light (red at 250 or more on 0.55 to 2.8 per cent of the pixels; the ceiling near the rose read (255, 253, 178)), so the hue went yellow and the card's gain then made it olive; 17 per cent of the lit window's glass at the tight close view"}),
]

OWED_07 = {"id": "OWED-07", "what": "the game's night exposure: the research's 'real lit windows are 10 to 100 times the lit paving' (NIGHT-2026-10-08.md) is the game's exposure, not the cloud's stand-in sky and lamps; the cloud's absolute night levels are stand-ins",
           "check": "the lit windows against the lit paving in the packaged game's night frames (14 Oct, from the try 1 close review)"}

CHANGES = [
    {"where": "7.1 and 9 (gate.scene.night, rooms.lights_by_state.night_lit and landing_bulb)", "was": "a lit room's card is the night_lit picture x 0.7 x room_glow_gain_night 0.4 = 0.28", "now": "a lit room's card is the night_lit picture x 1.0 (a dark room's card stays x 0.7); the PC's M_LedgerInterior Brightness for a lit house room at night follows (OWED-04 measures it)",
     "why": "the same light passes through the net and lights the room, so the room seen through clear glass cannot be a quarter of the net: the clear glass read 0.26 to 0.31 of the lit net with 0.28 against a dark room's 0.7 (street review F2 cause 2)", "from": "street review"},
    {"where": "7.1 (the night_lit pictures)", "was": "the night_lit picture is the 8-bit render as it came, clipped at the ceiling light", "now": "the night_lit picture is rendered to a float picture and rolled off before the 8-bit write: the largest channel of a pixel eases from linear 0.60 toward 0.85 (sRGB 237) and never reaches it, the three channels scale together; the mean stays 70 +-15 per cent (landings 40); PIC-13 holds the clip at 0.1 per cent",
     "why": "the ceiling round the rose clipped to (255, 253, 178): red clipped, so the hue went yellow, and the gain then made it olive (close review fault 2)", "from": "close review"},
    {"where": "5.1 (the pane in the cloud)", "was": "Cycles Principled BSDF with Specular IOR Level 1.0", "now": "the gate's pane is a Mix of a Transparent BSDF and a Glossy GGX (roughness 0.03) weighted by the dielectric Fresnel of F0 0.08 (IOR 1.789) x (1 - Backfacing): the kit's panes are closed 2.5 mm slabs (a front and a back face), the back face is pure Transparent and the front face stands for both faces, as the game's pane does (Specular 1.0, F0 0.08 for both faces of a single pane)",
     "why": "Cycles' Fresnel node inverts the IOR on a back face, so past the critical angle (34 degrees from the normal: any view under 56 degrees from the wall) the back face was a total mirror and nothing passed the pane: by day every pane was a mirror and no net, curtain or room showed; at night the back face mirrored the sky at 0.2 into every pane (both reviews, fault 1)", "from": "both reviews"},
    {"where": "10 MAT-04", "was": "a flat single plane at 16 degrees against a sky, the room black", "now": "the kit's own slab, two readings (reflection 0.26 +-0.05, and reflection plus transmission 1.0 +-0.05)", "why": "the single plane passed the mirror", "from": "both reviews"},
    {"where": "10 GLS-06 (new)", "was": "-", "now": "the kit's own slab at 15, 20, 35, 50 and 70 degrees from the wall in front of an emission card of 0.5: the card reads at least (1 - F_front) of its own, less 0.03", "why": "no row could see a pane that blocks the room", "from": "both reviews"},
    {"where": "10 WB-03", "was": "0.35 to 0.70 and blue over red at least 10 levels", "now": "0.35 to 0.90 and blue minus red at least -3 levels", "why": "the band came from P8, a clear blue sky; the game's sky is overcast and neutral", "from": "both reviews (the street review's numbers are used)"},
    {"where": "10 WB-07", "was": "3.0 to 9.0", "now": "3.0 to 9.0 for white_fresh and white_upvc; 2.5 to 9.0 for white_grimy and white_flaking", "why": "the floor sat at 0.8 of the lowest sound-white photograph and the dull paints are darker on purpose", "from": "both reviews (2.5 is the street review's; the close review's 2.2 is for white_flaking alone and also passes)"},
    {"where": "10 NIGHT-01", "was": "DARK when its pane luma is 8 to 30; LIT when at least 4 times the dark median", "now": "DARK when the CLEAR glass reads 8 to 35 and a dark window's net at most 0.7 of its own frame's L; LIT when the pane median is at least 2.5 times the dark median with r > g > b", "why": "no net window can hold the old band: its net is lit by the game's own night sky light", "from": "street review (the close review's per-window wording, dark P/L at most 0.70 and lit P/L at least 1.0, is reported beside)"},
    {"where": "10 NIGHT-02", "was": "at least 4 (linear at least 10)", "now": "at least 2.5 (linear at least 6), the pane against the pane", "why": "the old 4 rested on a dark pane with no lit net in it", "from": "street review (the close review asks 2.0 against each window's own frame)"},
    {"where": "10 NIGHT-03", "was": "the lit pane's mean colour", "now": "the mean, and every 32 x 32 block of a lit pane: r > g > b and linear g/r at most 0.85", "why": "a mean hid an olive band round a clipped ceiling light", "from": "close review"},
    {"where": "10 NIGHT-07 (new)", "was": "-", "now": "in every lit window at H_ACROSS_0 night the clear glass's mean linear luminance is 0.5 to 1.0 of its lit net's, curtain's or blind's (the review said median; its figures are means)", "why": "the lit room was four times dimmer than its own net", "from": "street review"},
    {"where": "10 PIC-13 (new)", "was": "-", "now": "no night_lit picture has more than 0.1 per cent of its pixels with a channel at 250 or more", "why": "every lit picture clipped round the ceiling light", "from": "close review"},
    {"where": "10 JNR-01 (new), GRM-01 (new)", "was": "-", "now": "no joinery pixel under luma 10 inside a window outline by day; the grime band's 0.75 on a grimy window's lowest 30 mm of bottom rail", "why": "the black notch at the head of the far jamb; target 4.2's grime band was not built", "from": "close review"},
    {"where": "10 OWED-07 (new)", "was": "-", "now": "the game's night exposure: 'real lit windows are 10 to 100 times the lit paving' is the game's, not the cloud's", "why": "the cloud's absolute night levels are stand-ins", "from": "close review"},
    {"where": "status", "was": "fixes applied, not re-reviewed", "now": STATUS_JSON, "why": "", "from": "-"},
]

ROW_ORDER_NOTE = "Rows made only in the check (not in the target's list, because they test the build and the reviewers' own acceptance, not the target): NEG-01 (the negative control: the back-face mirror must fail GLS-06 and MAT-04), ACC-01 and ACC-02 (the street review's acceptance by day in cam_A and the Hook), NIGHT-08 and NIGHT-09 (its acceptance at night in the Hook and the reverse view)."


# ==================================================================================================================================================================== the second round (14 October, from the try 2 reviews)
SRC3 = {
    "WB-01": MARK3 + " (street review 7, close review WB-01): east_parade_bay1_upper_w1 (an S11 with a voile on its lower sash only, the clear upper sash half the pane) read 0.545 against 0.55, the floor that P4_E's 0.555 (the one photographed net on a lower half) sets; 0.50 is 0.9 of it, a margin like WB-07's floor at 0.8 of its lowest photograph; the gate's own repeatability is wider than 0.005 (the same bare window reads 0.476 in the 2560 x 1440 frame and 0.509 in a 1280 x 720 one: the close review's 0.03); a far window's 434 glass pixels read 0.458. The two reviews' fixes (the street's lower floor, the close review's tolerance) are both applied",
    "WB-02": MARK3 + " (street review 6, close review WB-02): both reviews rendered the bare window and read 0.423 with the glass's reflection off and 0.509 with it on (the gate's frame 0.476): the room is right and the stand-in dome's reflection adds 0.06 to 0.09 to it; the band's photographs are not at this geometry (P1_c is at 22 degrees but its frame is dark brown and its L includes white stone, P4_G a ground window at 46 degrees, P3_d square on) and target 5.1's own two-face table asks 0.21 to 0.31 of what lies opposite at 18 to 24 degrees. The street review's higher top (0.55) for an upper window from its own footway and the close review's reading on a reflection-off day frame (0.10 to 0.45) are both applied",
    "WB-04b": MARK3 + " (street review 5, close review WB-04b): the one window over (east_parade_bay2_upper_w1 in h-along15road-bay3w1, 0.62) is cut by the picture's top edge and one of its pane edges crosses brick seen through the glass (GLS-07), not a dark line; the rule that keeps a cut window out of WB-06 and WB-07 now holds for every per-window row (WB-01 to WB-07, NIGHT-01, NIGHT-02, NIGHT-07)",
    "WB-07": MARK3 + " (street review 4, close review WB-07): the brick ring took in the stone sill and head (material 'brick' with G 0 like the brick, but pale stone: (186, 184, 175) at the sill) and lifted a small far window's ring median from 97-101 to 107-112; with the ring cut to the window's own rows the low readings are 2.43 to 2.83; and white_flaking's linear albedo is 0.60, so its floor is 3.0 x 0.60 / 0.82 = 2.2 (the street review's own try 1 2.5 was the rounding for grimy, 0.66: 2.4); the close review's 5,000 joinery pixels (a far window's joinery is mostly reveal-facing faces, shaded to 0.6 by design) is applied as well",
    "NIGHT-01": MARK3 + " (street review 2): 'at least 2.5 times the dark median' was NIGHT-02's own ratio of the two medians, so when the medians stand 2.5 apart about half of the lit windows fall under the line by construction (7 of 9 lit readings failed it, among them the parade's lounges at 120 and 122 against the line 125); the lowest lit reading (79, the cottage net under a clear sash) is above the highest dark one (65, a cream roller blind); 1.58 is the geometric midpoint of 1 and 2.5, rounded down to 1.5",
    "NIGHT-02": MARK3 + " (street review 3): the dark side is set by cloth that the gate's stand-in lamps light (the dark nets read 0.56 to 0.66 of their own frames and the blinds 0.73, in every view alike), so the dark level follows the stand-in lamps' power while the lit glow (net 0.48, card x 1.0) does not; the research (NIGHT-2026-10-08) puts real lit windows at 10 to 100 times the lit paving, which the cloud's Standard view, with the paving at 150, cannot draw: it is the game's exposure (OWED-07). The cloud reads the parade's windows alone and the whole set beside",
    "NIGHT-03": MARK3 + " (street review 8, 9): east_parade_bay2_upper_w0 IS lit at 20:30 (7.3's order lights it) and carries the open green pair, so 'none is lit' was wrong; a green curtain lit from behind glows yellow-green, its own colour x the warm light (g/r 1.35); the 14 blocks of h-along30-gf2w1 night that read g/r 0.87 to 0.89 are the framed print's own green field (belfast_open_field) on the back wall, not a world seen past the card: no see-through slot exists in any mask",
    "NIGHT-07": MARK3 + " (street review 1, close review): the lit cottage's clear upper sash showed the back wall (a mean linear luminance of 0.040 to 0.048 in the three cottage night_lit pictures) against the lit net's 0.306; the parade's lounges pass only because from the street they show the ceiling round the rose. The cottage pictures are relit with the table lamp's glow raised, not the pendant (PIC-14: the close review's way; the street review's x 3.0 before the roll-off would have pushed the cottages' mean to 115); the lit lounges and bedrooms keep their ceilings under the knee (PIC-15) and the parade's windows stay under 1.0 of their nets",
    "PIC-02": MARK3 + " (close review, the cottage rooms): the cottages' front rooms' night_lit standard is the relit pictures' mean luma (picture_standards.night_lit_mean_luma_gf) +-15 per cent; every other room keeps 70",
}

CHANGED_3 = {
    "WB-01": {
        "expected": "0.55 to 0.97 for a full-height net (N2); 0.50 to 0.97 for a net on the lower sash only (N1: the clear upper sash is half the pane); a tolerance of 0.03 under either floor; a window with under 5,000 glass pixels is reported, not failed; a window cut by the picture's edge is not measured",
        "tolerance": "band, 0.03 under the floor",
    },
    "WB-02": {
        "measure": "P/L of every BARE window (N0 with no curtain and no blind: on the street east_parade_bay3_upper_w1 only) seen at 15 to 30 degrees from the wall, by day, on the beauty frame and on a day frame with the glass's reflection off (the room alone, 1280 x 720); a window cut by the picture's edge is not measured; draped windows have no P/L band",
        "expected": "beauty frame: 0.10 to 0.55 for an upper window seen from its own footway at 15 to 30 degrees, 0.10 to 0.45 in other cases; reflection-off frame: 0.10 to 0.45; a window with under 5,000 glass pixels is reported, not failed",
        "tolerance": "band",
    },
    "WB-04b": {
        "expected": "a dip at least 1 px wide to at most 0.60 of L; read in windows not cut by the picture's edge and with at least 3 pane edges profiled",
    },
    "WB-07": {
        "measure": "L (linear) over the brick's median (linear) beside the window, by day; the brick ring is the window's own rows (its outline's top to bottom), one window width each side, with no sill and no head (the stone sill and head are 'brick' in the mask too, but pale stone); a window cut by the picture's edge is not measured; only windows with at least 5,000 joinery pixels are read",
        "expected": "3.0 to 9.0 for white_fresh and white_upvc; 2.4 to 9.0 for white_grimy; 2.2 to 9.0 for white_flaking (each floor is 3.0 x the paint's linear albedo / 0.82)",
    },
    "NIGHT-01": {
        "measure": "at 20:30 over the 20 street windows (GS_A and GS_B together, rendered from the one camera that sees each squarely; a window cut by the picture's edge is not measured): a window is LIT when its pane median luma is at least 1.5 times the dark windows' median luma AND above every dark window's pane median, and the pane's mean linear colour has r > g > b; DARK when its CLEAR (net-free) glass reads 8 to 35 (NIGHT-04) and its net, if it has one, reads at most 0.7 of its own frame's L at night (the game's own night sky light, sky_light_gain_night 0.15, lights a dark window's net as it lights the frame). The clear glass and the net are told apart by the mask with the glass clear. The absolute emissions of the curtains, blinds and the landing bulb (`night_lit_emission_linear`, `landing_bulb`) are starting values, not the pass line",
    },
    "NIGHT-02": {
        "expected": "at least 2.5 (linear at least 6) on the PC, measured in the packaged game under the game's lamps and exposure (OWED-07); in the cloud it is REPORTED against 2.5 (with the parade's windows alone beside), not failed",
        "tolerance": "limit (PC); reported (cloud)",
    },
    "NIGHT-03": {
        "expected": "net: r > g > b, g/r 0.55 to 0.80, b/r 0.20 to 0.45 (tungsten 2700 K and the fabric); curtain or blind: its own colour x that light (curtains.*.night_lit_emission_linear): r > g > b for the cream and brown curtains and the white and cream blinds (the brown curtain's g/r is 0.39); a green curtain's g > r is its own colour (east_parade_bay2_upper_w0 is lit at 20:30 with one, an open pair): its pixels are read against r and g of the curtain's own colour x the warm light (g/r 1.35 +-0.12, b under r), not against g/r 0.85; every 32 x 32 block of a lit pane behind the room card: r > g > b and linear g/r at most 0.85 (a framed print's own green field is its own colour too: a block of it is read against the print's colour)",
    },
    "PIC-02": {
        "expected": "day 105, night_lit 70 (the cottages' front rooms: the relit mean `night_lit_mean_luma_gf`), night_dark 15 (landings and empty rooms at night_lit: bare bulb: 40)",
    },
}

NEW_3 = [
    ("GLS-06", {
        "id": "GLS-07", "group": "glass", "name": "no glass pixel sees brick",
        "measure": "by day and at night, in every gate frame, for every window: the glass pixels (material 1) whose clear-glass mask (the glass made transparent) shows the stand-in street's brick (code 4) behind them",
        "expected": "none: at most 0.05 per cent of a window's glass pixels and at most 10 pixels (the anti-aliased edge). The try 2 build read 7,678 of 28,912 glass pixels of west_south_bay1_gf_w1 at the worst (h-along30-gf2w1 day) and about half of one small cottage window in the Hook: the RC and RC2 frames ended at 142.5 mm into the wall with no inner reveal, so a ray under about 30 degrees from the wall passed the frame's back and met the brick of the reveal. The negative control NEG-04 (the try 2 frames) must fail it",
        "tolerance": "limit", "applies_to": "every window of every gate frame (RC and RC2 were the faulty kinds)", "kind": "Derived",
        "source": MARK3 + ": close review, outside this view, item 1 (REVIEW-v2-close.md); the fix is the inner reveal of 4.3 and 4.5"}),
    ("NIGHT-07", {
        "id": "NIGHT-10", "group": "gate", "name": "a lit curtain's folds read",
        "measure": "the lit green curtain's two strips beside the lower light of east_parade_bay2_upper_w0 at H_ACROSS_0 night (the street review's two boxes, 1203 to 1211 and 1347 to 1354 across, 668 to 725 down in the 2560 frame, eroded 2 px): (p95 - p5) / median of the luma",
        "expected": "at least 0.08: a lit curtain's emission carries the curtain's own fold brightness map (the +-25 per cent its base colour carries by day: C2 'folds dark', brightness modulation 0.25); the try 2 build's constant emission read 0.017 (two flat lime bars). The try 2 frame must read under 0.05 (negative control)",
        "tolerance": "limit", "applies_to": "lit curtains (C1, C2)", "kind": "Judgement",
        "source": MARK3 + ": street review, narrow point 8 (REVIEW-v2-street.md)"}),
    ("NIGHT-10", {
        "id": "NIGHT-11", "group": "gate", "name": "the lit ceiling seen through an upper sash is not a flat plateau",
        "measure": "in each upper pane of east_parade_bay0_upper_w1 in the close and close2 views at night: the local spread (the median, over the pane's interior eroded by 5 px, of the standard deviation of the luma over 15 px) and the share of the pane's pixels within 3 levels of its 90th percentile",
        "expected": "a local spread of at least 2 levels and under 25 per cent of the pane within 3 levels of its 90th percentile. The try 2 close2's upper-right pane read 0.75 and 48 per cent (the ceiling within 0.6 m of the rose lay over the roll-off's knee: a flat warm plateau)",
        "tolerance": "limits", "applies_to": "the close views", "kind": "Judgement",
        "source": MARK3 + ": close review, narrow point 1 (REVIEW-v2-close.md): the pendant halved and the picture's mean made up by a room-wide fill"}),
    ("PIC-13", {
        "id": "PIC-14", "group": "pictures", "name": "the cottage rooms' back wall is lit",
        "measure": "in each of the three cottage night_lit pictures (gf_front_1 to 3): the mean linear luminance of the box [848.8, 649.1, 2223.2, 1700.1] of the 3072 x 2349 picture (the back wall that the clear upper sash shows at eye level)",
        "expected": "at least 0.12 (it read 0.040 to 0.048 against the lit net's 0.306: a clear sash at 0.19 of its net): raised by the table lamp's glow on the back wall, not by the pendant; PIC-13 (no channel at 250 or more) and NIGHT-03 (no block with g/r over 0.85) hold",
        "tolerance": "limit", "applies_to": "gf_front_1, gf_front_2, gf_front_3", "kind": "Judgement",
        "source": MARK3 + ": close review, item 3 of the row rulings (REVIEW-v2-close.md), street review narrow point 1: the two reviews differ on how (the close review raises the lamp's glow, the street review scales the cottage pictures x 3.0 before the roll-off to a mean of 115); the close review's way is used"}),
    ("PIC-14", {
        "id": "PIC-15", "group": "pictures", "name": "the lit ceiling near the rose is no plateau",
        "measure": "in each of the six lit lounge and bedroom night_lit pictures: the ceiling band within about 0.6 m of the rose that the close views see through the upper sash (x 177 to 807, y 39 to 123 of the 1536 x 1399 picture)",
        "expected": "under 15 per cent of the band at luma 200 or more (it read 34 per cent) and under 25 per cent of it within 3 levels of its 90th percentile; the local spread is read on the frames (NIGHT-11)",
        "tolerance": "limits", "applies_to": "up_lounge_1 to 3, up_bedroom_1 to 3", "kind": "Judgement",
        "source": MARK3 + ": close review, narrow point 1"}),
]

CHANGES_3 = [
    {"where": "4.3 and 4.5 (RC and RC2: the inner reveal)", "was": "the frame ends at 142.5 mm into the wall and there is no inner reveal", "now": "four always-on painted lining boards, y 142.5 to 268 (short of the card at 270): two jamb linings 12.5 mm at x +-412.5 to +-425, z 0 to 1676.4; a head lining 12.5 mm at z 1663.9 to 1676.4; a window board 25 mm at z 0 to 25; white emulsion, linear (0.72, 0.70, 0.64), roughness 0.9, box shade 1.0 at 142.5 falling to 0.6 at 268 (kinds.RC.inner_reveal, kinds.RC2.inner_reveal)",
     "why": "brick seen through the glass beside the far jamb (7,678 of 28,912 glass pixels at the worst; about half of one small cottage window in the Hook): the S22 and S11 carry the lab's inner linings to 250.8, these two kinds had none, so a ray under about 30 degrees from the wall met the stand-in wall's brick where a real house has plaster", "from": "close review (outside this view, item 1)"},
    {"where": "7.2 and 8 (the pendant shade)", "was": "a mesh node pendant__shade 0.55 m behind the opaque room card in every upper kit piece and in the cottages' card glb", "now": "no node: the shade is drawn into the card's bake the way trace draws the room: the eye's ray is tested against the shade's truncated cone (radius 0.170 m at its foot, 0.105 at its top, 0.24 high, axis 0.55 m behind the card, top 0.30 m below the ceiling) before the room box; where it hits first the card shows the shade, lit: warm emission (the cloud scales it to 0.85 in its largest channel, the game's x 3.0 is its own exposure), otherwise the paper (0.93, 0.89, 0.77) lit by the room's own day or sodium light. The game's M_LedgerInterior does the same test (or writes the traced depth as Pixel Depth Offset)",
     "why": "the card is opaque, so the shade could never be seen in any frame; 88 of its 144 projected points fall on the lit window's glass from across (H_ACROSS_0 night); 7.2's 'at night a warm ceiling and the shade' got only the ceiling", "from": "close review (outside this view, item 2)"},
    {"where": "7.1 (night_lit lights of the lit lounges and bedrooms)", "was": "the pendant alone (a point light at the ceiling rose)", "now": "the pendant's point light is halved (and capped at 13.5 so that the ceiling round the rose stays under the roll-off's knee) and a room-wide fill makes up the mean 70 +-15 per cent: a soft area light under the ceiling's centre shining down, with 14 per cent of its power as a strip of light on the back wall's top; the roll-off is as it was", "why": "the ceiling within 0.6 m of the rose lay over the knee (34 per cent of that band at luma 200 or more) and the roll-off eased it all onto one plateau; the close views see exactly that part through the upper sash (NIGHT-11, PIC-15)", "from": "close review (narrow point 1)"},
    {"where": "7.1 (night_lit lights of the cottages' front rooms)", "was": "the pendant and a table lamp's glow on the back wall at 4 (the back wall box a mean of 0.040 to 0.048 linear), mean luma 70", "now": "the table lamp's glow on the back wall raised, the pendant untouched, until the back wall box reads at least 0.12 (PIC-14); the cottages' night_lit mean standard becomes the relit pictures' mean +-15 per cent (picture_standards.night_lit_mean_luma_gf)", "why": "a lit cottage's clear upper sash showed a back wall at a seventh of the lit net's glow (NIGHT-07 0.19)", "from": "close review (the street review's way, x 3.0 before the roll-off, is not used)"},
    {"where": "6 (a lit curtain)", "was": "a lit curtain's emission is one constant colour", "now": "a lit curtain's emission is multiplied by the curtain's own fold brightness map (the +-25 per cent its base colour carries by day), its mean the target's night_lit_emission_linear; NIGHT-10 reads it", "why": "the lit green curtain read as two flat lime bars (H_ACROSS_0 night); C2 asks 'folds dark'", "from": "street review (narrow point 8)"},
    {"where": "10 NIGHT-03 and 7.3", "was": "'a green curtain's g > r is its own colour and none is lit at 20:30'", "now": "east_parade_bay2_upper_w0 is lit at 20:30 with an open green pair: its pixels are read against the curtain's own colour x the warm light (g/r 1.35 +-0.12), not against g/r 0.85", "why": "7.3's order lights this window; the text said none is", "from": "street review (narrow point 8)"},
    {"where": "10 WB-01", "was": "0.55 to 0.97", "now": "0.55 to 0.97 for a full-height net, 0.50 to 0.97 for a net on the lower sash only, each with a tolerance of 0.03 under the floor; under 5,000 glass pixels reported, not failed", "why": "one S11 window read 0.545 (P4_E, the one photographed net on a lower half, 0.555); the gate's repeatability is wider than 0.005", "from": "both reviews (the street review's N1 floor and the close review's tolerance, both)"},
    {"where": "10 WB-02", "was": "0.10 to 0.45 on the beauty frame", "now": "an upper window seen from its own footway at 15 to 30 degrees: 0.10 to 0.55 on the beauty frame; other cases 0.10 to 0.45; and 0.10 to 0.45 on a day frame with the glass's reflection off; under 5,000 glass pixels reported", "why": "the stand-in dome's reflection adds 0.06 to 0.09 to the room's 0.42 (both reviews rendered it); the band's photographs are not at this geometry", "from": "both reviews (both fixes applied)"},
    {"where": "10 WB-04b", "was": "every bare and net window at 15 to 30 degrees", "now": "windows not cut by the picture's edge with at least 3 pane edges profiled; and one rule for every per-window row (WB-01 to WB-07, NIGHT-01, NIGHT-02, NIGHT-07): a window whose outline touches the picture's edge is not measured", "why": "the one failing window is cut by the top edge and shows brick through its glass", "from": "both reviews"},
    {"where": "10 WB-07", "was": "3.0 to 9.0 (2.5 for the dull paints); the ring 1.0 window width each side and half a window's height above and below", "now": "3.0 for white_fresh and white_upvc, 2.4 for white_grimy, 2.2 for white_flaking; the ring is the window's own rows with no sill and no head; windows with at least 5,000 joinery pixels only", "why": "the stone sill and head lifted the ring of a small far window; white_flaking's albedo is 0.60: 3.0 x 0.60 / 0.82 = 2.2", "from": "both reviews"},
    {"where": "10 NIGHT-01", "was": "LIT when the pane median is at least 2.5 times the dark median", "now": "LIT when at least 1.5 times the dark median and above every dark window's pane median, with r > g > b", "why": "2.5 was NIGHT-02's own ratio, so half of any set at that limit fell under it by construction", "from": "street review"},
    {"where": "10 NIGHT-02", "was": "at least 2.5 (linear 6) in the cloud", "now": "reported in the cloud against 2.5 (parade alone and whole set), held at linear 6 or more on the PC (OWED-07)", "why": "the dark side follows the stand-in lamps' power; the game's exposure is the PC's", "from": "street review"},
    {"where": "10 GLS-07 (new), NIGHT-10 (new), NIGHT-11 (new), PIC-14 (new), PIC-15 (new)", "was": "-", "now": "no glass pixel sees brick; a lit curtain's folds read; the lit ceiling seen through an upper sash is no plateau; the cottage rooms' back wall is lit; the lit ceiling near the rose is no plateau", "why": "the reviews' narrow points as rows", "from": "both reviews"},
    {"where": "status", "was": "built; the first round of changes applied", "now": STATUS_JSON, "why": "", "from": "-"},
]

ROW_ORDER_NOTE_3 = " Try 3 adds, in the check only: KIT-20 (the RC and RC2 inner reveal's four boards at the review's sizes), KIT-21 (no glb carries a pendant node), BAK-01 (the pendant shade is drawn into the card's bake), NEG-04 (the negative control: the try 2 frames must fail GLS-07)."

INNER_REVEAL = {"y_from_mm": 142.5, "y_to_mm": 268.0, "material": "paint_white_emulsion", "colour_linear": [0.72, 0.70, 0.64], "roughness": 0.9, "box_shade": {"at_y_142_5": 1.0, "at_y_268": 0.6},
                "boards": [{"name": "reveal_jamb_L", "x": [-425.0, -412.5], "z_up": [0.0, 1676.4]}, {"name": "reveal_jamb_R", "x": [412.5, 425.0], "z_up": [0.0, 1676.4]},
                           {"name": "reveal_head", "x": [-412.5, 412.5], "z_up": [1663.9, 1676.4]}, {"name": "reveal_board", "x": [-412.5, 412.5], "z_up": [0.0, 25.0]}],
                "note": MARK3 + ": close review, outside this view, item 1. The lab's S22 and S11 carry inner linings to 250.8; RC and RC2 had none. hw_kit.REVEAL mirrors these numbers (KIT-20 reads the glb against them)"}


def patch_json_3(t):
    checks = t["checks"]
    by = {c["id"]: c for c in checks}
    for rid, ch in CHANGED_3.items():
        by[rid].update(ch)
        if MARK3 not in by[rid]["source"]:
            by[rid]["source"] = by[rid]["source"] + "; " + SRC3[rid]
    new_ids = {n["id"] for _, n in NEW + NEW_3}
    for after, c in NEW_3:
        if c["id"] in by:
            by[c["id"]].update(c)
            continue
        i = next(k for k, x in enumerate(checks) if x["id"] == after)
        while i + 1 < len(checks) and checks[i + 1]["id"] in new_ids:
            i += 1
        checks.insert(i + 1, c)
        by[c["id"]] = c
    # the standards and lights
    ps = t["rooms"]["picture_standards"]
    if GF_NIGHT_LIT_MEAN is not None:
        ps["night_lit_mean_luma_gf"] = GF_NIGHT_LIT_MEAN
        ps["night_lit_mean_luma_gf_note"] = MARK3 + ": the cottages' front rooms' night_lit pictures are relit (the table lamp's glow raised, PIC-14); their standard is the relit pictures' mean, +-15 per cent"
    lbs = t["rooms"]["lights_by_state"]
    lbs["night_lit_try3"] = (MARK3 + ": the lit lounges and bedrooms: the pendant's point light is halved (and capped at 13.5, so that the ceiling round the rose stays under the roll-off's knee) and a room-wide fill (a soft area light under the ceiling's centre shining down, 14 per cent of its power also as a strip of light on the back wall's top) makes up the mean 70 +-15 per cent (PIC-15, NIGHT-11); the cottages' front rooms: the table lamp's glow on the back wall is raised, the pendant is not, until the back wall box reads at least 0.12 linear (PIC-14), and their mean standard is the relit pictures' (picture_standards.night_lit_mean_luma_gf)")
    lbs["pendant_shade"] = (MARK3 + ": the pendant shade is drawn into the card's bake, not a mesh behind the opaque card: the eye's ray is tested against its truncated cone (radius 0.170 m at the foot, 0.105 at the top, 0.24 high, axis 0.55 m behind the card on the room's centre line, top 0.30 m below the ceiling) before the room box; lit: warm emission (the cloud scales it to 0.85 in its largest channel, the game's x 3.0 is its own exposure), otherwise the paper (0.93, 0.89, 0.77) lit by the room's own light (the picture's ceiling light over the ceiling's albedo 0.72). The game's M_LedgerInterior does the same test or writes the traced depth as Pixel Depth Offset")
    c1 = t["curtains"]["C1"]
    if "night_lit_emission_note" in c1 and MARK3 not in c1["night_lit_emission_note"]:
        c1["night_lit_emission_note"] = c1["night_lit_emission_note"].replace("The lit set at 20:30 has no green drawn curtain (g > r would break r > g > b).", "The lit set at 20:30 has no green DRAWN curtain (g > r would break r > g > b); it has one green open pair (C2: east_parade_bay2_upper_w0), whose g > r is its own colour (" + MARK3 + ": NIGHT-03). A lit curtain's emission is multiplied by the curtain's own fold map (the +-25 per cent its base colour carries by day) in the cloud (NIGHT-10).")
    for k in ("RC", "RC2"):
        t["kinds"][k]["inner_reveal"] = INNER_REVEAL
    for k, pk in t["kit_pieces"]["per_kind"].items():
        nodes = pk["added_nodes"]
        keep = [n for n in nodes if n["name"] != "pendant__shade"]
        if len(keep) != len(nodes):
            pk["added_nodes"] = keep
            pk["dropped_nodes"] = [{"name": "pendant__shade", "note": MARK3 + ": no node: the shade is drawn into the card's bake (close review, outside this view, item 2); it stood 0.55 m behind the opaque card and could not be seen"}]
        if k in ("RC", "RC2") and "inner_reveal_nodes" not in pk:
            pk["inner_reveal_nodes"] = [{"name": "paint_joinery__" + b["name"], "material": "paint_white_emulsion", "x": b["x"], "y_into_wall": [142.5, 268.0], "z_up": b["z_up"], "note": MARK3 + ": always on; box shade 1.0 at y 142.5 falling to 0.6 at 268"} for b in INNER_REVEAL["boards"]]
    ch = t["changes_after_the_build"]
    ch["round_2"] = {"made": "14 October 2026", "reviews": ["production/cloud-week/kit/house-windows/REVIEW-v2-street.md", "production/cloud-week/kit/house-windows/REVIEW-v2-close.md"],
                     "what": "both second fresh reviews PASSED under Jafar's ruling of 9 October (0 faults; narrow points listed); the points that touch the target are applied here, not re-reviewed", "changes": CHANGES_3, "check_only_rows": ROW_ORDER_NOTE_3.strip()}
    ch["reviews"] = list(dict.fromkeys(ch["reviews"] + ch["round_2"]["reviews"]))
    t["status"] = STATUS_JSON
    return t


def patch_md_3(t):
    s = open(TM, encoding="utf-8").read()
    by = {c["id"]: c for c in t["checks"]}

    def sub_line(prefix, new_line):
        nonlocal s
        pat = re.compile(r"^" + re.escape(prefix) + r".*$", re.M)
        assert pat.search(s), prefix
        s = pat.sub(lambda m: new_line, s, count=1)
    for rid in CHANGED_3:
        sub_line("| %s |" % rid, md_row(by[rid]))
    new_ids = {n["id"] for _, n in NEW + NEW_3}
    for after, c in NEW_3:
        if re.search(r"^\| %s \|" % re.escape(c["id"]), s, re.M):
            sub_line("| %s |" % c["id"], md_row(c))
        else:
            m = re.search(r"^\| %s \|.*$" % re.escape(after), s, re.M)
            end = m.end()
            while True:
                nxt = re.match(r"\n\| ([A-Z]+-\d+[a-z]?) \|[^\n]*", s[end:])
                if nxt and nxt.group(1) in new_ids:
                    end += nxt.end()
                else:
                    break
            s = s[:end] + "\n" + md_row(c) + s[end:]
    n_checks = len(t["checks"])
    s = re.sub(r"^\d+ checks\. Kinds of number", "%d checks. Kinds of number" % n_checks, s, count=1, flags=re.M)
    s = re.sub(r"the gate, \d+ checks,", "the gate, %d checks," % n_checks, s, count=1)
    # the pendant node rows of section 8 (the four kits)
    for m in list(re.finditer(r"^\| pendant__shade \|.*$", s, re.M))[::-1]:
        if MARK3 not in m.group(0):
            s = s[:m.start()] + "| ~~pendant__shade~~ | - | - | - | - | " + MARK3 + ": no node: the shade is drawn into the card's bake (close review, outside this view, item 2); it stood 0.55 m behind the opaque card and could not be seen. Radius 0.170 m at its foot, 0.105 at its top, 0.24 high, axis 0.55 m behind the card, top 0.30 m below the ceiling; " + MARK3 + " |" + s[m.end():]
    # the status line
    s = re.sub(r"\*\*Status: built \(unit 8, 14 October 2026\); changes after the build from the two try 1 reviews applied on 14 October \(section 14\)[^*]*\*\*", "**Status: built (unit 8, 14 October 2026); changes after the build from the two try 1 reviews and, in a second round, from the two try 2 reviews (which passed with narrow points) applied on 14 October (section 14); the second round's changed rows are not re-reviewed. Before the build: fixes applied, not re-reviewed (13 October 2026).**", s, count=1)
    # the inner reveal lines under 4.3 and 4.5
    for head in ("### 4.3 ", "### 4.5 "):
        if "**The inner reveal, " + MARK3 not in s.split(head)[1].split("\n### ")[0].split("\n## ")[0]:
            i = s.index(head)
            j_candidates = [x for x in (s.find("\n### ", i + 5), s.find("\n## ", i + 5)) if x != -1]
            j = min(j_candidates)
            s = s[:j] + "\n\n**The inner reveal, " + MARK3 + ":** RC and RC2 carry four painted lining boards 12.5 mm (the window board 25 mm) from y 142.5 to 268: two jamb linings at x +-412.5 to +-425, z 0 to 1676.4; a head lining at z 1663.9 to 1676.4; a window board at z 0 to 25; white emulsion, linear (0.72, 0.70, 0.64), roughness 0.9, box shade 1.0 at 142.5 falling to 0.6 at 268 (`kinds.RC.inner_reveal`; GLS-07 reads the brick that the frames no longer show through the glass)." + s[j:]
    # section 14.2
    if SEC3 not in s:
        out = ["", SEC3 + " (14 October 2026, from the try 2 reviews)", "",
               "Both second fresh reviews of the built kit (REVIEW-v2-street.md, REVIEW-v2-close.md in production/cloud-week/kit/house-windows/) PASSED under Jafar's ruling of 9 October (a piece failing only on narrow points passes, with the points listed). The points that touch the target are applied below, each marked \"%s\" where it stands in sections 4.3, 4.5, 6, 7.1, 8 and 10 and in `target.json` (`changes_after_the_build.round_2`); `changes_after_build.py` applies them (idempotent). Where the two reviews differ on one point, the way with the better evidence is used and said here." % MARK3, "",
               "| where | was | now | why | from |", "|---|---|---|---|---|"]
        for c in CHANGES_3:
            out.append("| %s | %s | %s | %s | %s |" % (c["where"], c["was"], c["now"], c["why"], c["from"]))
        out += ["", ROW_ORDER_NOTE_3.strip(), ""]
        s = s.rstrip("\n") + "\n" + "\n".join(out) + "\n"
    open(TM, "w", encoding="utf-8").write(s)


def md_row(c):
    return "| %s | %s | %s | %s | %s | %s | %s | %s |" % tuple(c[k] for k in ("id", "name", "measure", "expected", "tolerance", "applies_to", "kind", "source"))


def patch_json():
    t = json.load(open(TJ, encoding="utf-8"))
    checks = t["checks"]
    by = {c["id"]: c for c in checks}
    for rid, ch in CHANGED.items():
        by[rid].update(ch)
    for after, c in NEW:
        if c["id"] in by:
            by[c["id"]].update(c)
            continue
        i = next(k for k, x in enumerate(checks) if x["id"] == after)
        # keep a run of new rows after the same anchor in their given order
        while i + 1 < len(checks) and checks[i + 1]["id"] in {n["id"] for _, n in NEW}:
            i += 1
        checks.insert(i + 1, c)
        by[c["id"]] = c
    # the lit gain
    lbs = t["rooms"]["lights_by_state"]
    lbs["landing_bulb"]["what"] = lbs["landing_bulb"]["what"].replace("(the card's emission is picture x 0.7 x room_glow_gain_night 0.4)", "(the card's emission is picture x 1.0 from 14 Oct, from the try 1 reviews; it was x 0.7 x room_glow_gain_night 0.4)")
    lbs["night_lit_pictures"] = "14 Oct, from the try 1 reviews: a night_lit picture is rendered to a float picture and rolled off before the 8-bit write (the pixel's largest channel in linear eases from a knee of 0.60 toward 0.85 and never reaches it; the three channels scale together); mean 70 +-15 per cent (landings 40); PIC-13: at most 0.1 per cent of the pixels with a channel at 250 or more"
    lbs["lit_card_gain"] = "14 Oct, from the try 1 reviews: a lit room's card is the night_lit picture x 1.0 (a dark room's card x 0.7); it was x 0.7 x room_glow_gain_night 0.4 = 0.28, which put the room seen through clear glass at a quarter of its own net (NIGHT-07). The PC's M_LedgerInterior Brightness for a lit house room at night follows; OWED-04 measures it"
    g = t["gate"]["scene"]
    g["night"] = g["night"].replace("lit room card (night_lit picture x 0.7 x room_glow_gain_night 0.4)", "lit room card (night_lit picture x 1.0; 14 Oct, from the try 1 reviews: it was x 0.7 x room_glow_gain_night 0.4)")
    bd = t["gate"]["bands"]["bare_N0_over_60_deg_from_across"]
    bd["P_over_L"] = [0.35, 0.9]
    bd.pop("blue_over_red_min", None)
    bd["blue_minus_red_min"] = -3
    bd["changed"] = MARK + ": was P/L 0.35 to 0.70 and blue over red at least 10 (P8, a clear blue sky); the game's sky is the overcast dome, neutral: 0.35 to 0.90 (P3_d 0.36, P8 0.49 to 0.59, P6_up 0.89 with sky in its glass) and blue minus red at least -3"
    t["glass"]["pane"]["cloud_stand_in_14_oct"] = CHANGES[2]["now"]
    # owed
    if not any(o["id"] == "OWED-07" for o in t["owed_on_pc"]):
        t["owed_on_pc"].append(OWED_07)
    t["status"] = STATUS_JSON
    t["changes_after_the_build"] = {"made": "14 October 2026", "by": "changes_after_build.py in this folder (re-run it after any regeneration by make_target.py and make_doc.py)", "reviews": ["production/cloud-week/kit/house-windows/REVIEW-v1-street.md", "production/cloud-week/kit/house-windows/REVIEW-v1-close.md"],
                                    "changes": CHANGES, "check_only_rows": ROW_ORDER_NOTE,
                                    "note": "the self_check result below is the 13 October one (424 rows); it does not know the changed rows"}
    json.dump(t, open(TJ, "w", encoding="utf-8"), indent=1)
    return t


def patch_md(t):
    s = open(TM, encoding="utf-8").read()
    by = {c["id"]: c for c in t["checks"]}

    def sub_line(prefix, new_line):
        nonlocal s
        pat = re.compile(r"^" + re.escape(prefix) + r".*$", re.M)
        assert pat.search(s), prefix
        s = pat.sub(lambda m: new_line, s, count=1)
    for rid in CHANGED:
        sub_line("| %s |" % rid, md_row(by[rid]))
    for after, c in NEW:
        if re.search(r"^\| %s \|" % re.escape(c["id"]), s, re.M):
            sub_line("| %s |" % c["id"], md_row(c))
        else:
            m = re.search(r"^\| %s \|.*$" % re.escape(after), s, re.M)
            end = m.end()
            # skip the new rows already placed after this anchor
            while True:
                nxt = re.match(r"\n\| ([A-Z]+-\d+[a-z]?) \|[^\n]*", s[end:])
                if nxt and nxt.group(1) in {n["id"] for _, n in NEW}:
                    end += nxt.end()
                else:
                    break
            s = s[:end] + "\n" + md_row(c) + s[end:]
    n_checks = len(t["checks"])
    s = re.sub(r"^\d+ checks\. Kinds of number", "%d checks. Kinds of number" % n_checks, s, count=1, flags=re.M)
    s = re.sub(r"the gate, \d+ checks,", "the gate, %d checks," % n_checks, s, count=1)
    # the OWED-07 line, after OWED-06
    if "**OWED-07**" not in s:
        m = re.search(r"^- \*\*OWED-06\*\*.*$", s, re.M)
        s = s[:m.end()] + "\n- **OWED-07** %s. Check: %s." % (OWED_07["what"][0].upper() + OWED_07["what"][1:], OWED_07["check"]) + s[m.end():]
    # status line
    s = re.sub(r"\*\*Status: fixes applied, not re-reviewed \(13 October 2026\)\.\*\*", "**Status: built (unit 8, 14 October 2026); changes after the build from the two try 1 reviews applied on 14 October (section 14); the changed rows are not re-reviewed. Before the build: fixes applied, not re-reviewed (13 October 2026).**", s, count=1)
    # 7.1 brightness
    old = "night 0.7 as the shops (shop-interiors.json); the pane composite measured in the gate decides."
    if old in s and "lit room's card" not in s.split(old)[1][:400]:
        s = s.replace(old, "night 0.7 as the shops (shop-interiors.json) for a dark room; **a lit room's card at night is the night_lit picture x 1.0** (" + MARK + ": it was x 0.7 x room_glow_gain_night 0.4 = 0.28, a quarter of the lit net's own glow; NIGHT-07); the pane composite measured in the gate decides. **A night_lit picture is rolled off before its 8-bit write** (" + MARK + ": the pixel's largest channel in linear eases from a knee of 0.60 toward 0.85 and never reaches it, the three channels scale together; PIC-13).")
    # 9 night
    s = s.replace("lit room card (night_lit picture x 0.7 x room_glow_gain_night 0.4), lit net emissive 0.48", "lit room card (night_lit picture x 1.0; " + MARK + ": it was x 0.7 x room_glow_gain_night 0.4), lit net emissive 0.48")
    # 9 bands: bare from across
    s = s.replace("- **bare_N0_over_60_deg_from_across:** P/L 0.35 to 0.7; pane blue minus red at least 10 levels.", "- **bare_N0_over_60_deg_from_across:** P/L 0.35 to 0.90; pane blue minus red at least -3 levels (" + MARK + ": was 0.35 to 0.7 and blue over red 10, from P8's clear blue sky; the game's sky is overcast and neutral).")
    # 5.1 note
    if "Cycles' Fresnel node inverts the IOR" not in s:
        m = re.search(r"^### 5\.2 ", s, re.M)
        s = s[:m.start()] + "**The pane in the cloud, " + MARK + ":** " + CHANGES[2]["now"] + ". Why: " + CHANGES[2]["why"] + ". MAT-04 is redone on the slab and GLS-06 and the negative control NEG-01 are new (section 10).\n\n" + s[m.start():]
    # section 14
    if SEC not in s:
        out = ["", SEC + " (14 October 2026, from the try 1 reviews)", "",
               "The built kit failed two fresh reviews (REVIEW-v1-street.md, REVIEW-v1-close.md in production/cloud-week/kit/house-windows/). Each change below is marked \"%s\" where it stands in sections 5, 7.1, 9 and 10 and in `target.json` (`changes_after_the_build`); `changes_after_build.py` in this folder applies them (idempotent; re-run it after any regeneration, the author tools are as they were on 13 October). Where the two reviews differ, the street review's rows are used for the street rows, and the close review's wording is reported beside." % MARK, "",
               "| where | was | now | why | from |", "|---|---|---|---|---|"]
        for c in CHANGES:
            out.append("| %s | %s | %s | %s | %s |" % (c["where"], c["was"], c["now"], c["why"], c["from"]))
        out += ["", ROW_ORDER_NOTE, ""]
        m = re.search(r"^## 13\. ", s, re.M)
        # after section 13 (the last): append at the end
        s = s.rstrip("\n") + "\n" + "\n".join(out) + "\n"
    open(TM, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    t = patch_json()
    patch_md(t)
    t = patch_json_3(t)
    json.dump(t, open(TJ, "w", encoding="utf-8"), indent=1)
    patch_md_3(t)
    print("changes applied: %d checks in target.json" % len(t["checks"]))
