"""Changes after the build: the changes to target.json and TARGET.md that the two fresh reviews of the BUILT kit asked for (cloud week 42, unit 8, try 1 reviews, 14 October 2026).

The target was written, reviewed and fixed on 13 October and the kit built to it on 14 October; the street review (REVIEW-v1-street.md) and the close review (REVIEW-v1-close.md) of the built kit found that some of the target's rows were
mis-set (WB-03, WB-07, NIGHT-01, NIGHT-02), that the lit room's gain was wrong (7.1 and 9: x 0.7 x 0.4), and that rows were missing (the glass of the kit's own slab, a lit window's clear glass against its net, clipped highlights, black joinery,
the grime band). This script applies those changes, each marked "14 Oct, from the try 1 reviews", to target.json and TARGET.md, and adds a "Changes after the build" section to both. It is idempotent (run it again and nothing changes) and
must be run again after any regeneration by make_target.py and make_doc.py, which do not know these changes: the author tools stay as they were on 13 October so that the record of what the review saw is kept.

Run: python3 changes_after_build.py   (no Blender; json and re only)
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TJ = os.path.join(HERE, "target.json")
TM = os.path.join(HERE, "TARGET.md")
MARK = "14 Oct, from the try 1 reviews"
SEC = "## 14. Changes after the build"

STATUS_JSON = "built (unit 8, 14 October 2026); changes after the build from the two try 1 reviews applied 14 October 2026 (changes_after_the_build, TARGET.md section 14); the changed rows are not re-reviewed"

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
    print("changes applied: %d checks in target.json" % len(t["checks"]))
