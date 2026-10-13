"""bicycle: writes target.json and TARGET.md (cloud week 42, unit 13, family 7: an adult's roadster leaning on a wall)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_family as SF
from sd_lib import B, CY

FAMILY = "bicycle"
R, TS = 330.0, 38.0            # wheel outer radius (26 x 1 3/8: a 660 mm tyre), tyre section
NSEG = 16
HEAD = math.radians(68.0)
SEAT = math.radians(72.0)
Z_AXLE = R
BB = (449.0, 300.0)
SEAT_TOP = (BB[0] - 560.0 * math.cos(SEAT), BB[1] + 560.0 * math.sin(SEAT))
HT1 = (SEAT_TOP[0] + 570.0, SEAT_TOP[1] + 7.0)
HT2 = (HT1[0] + 150.0 * math.cos(HEAD), HT1[1] - 150.0 * math.sin(HEAD))
RAKE = 45.0
FX = HT2[0] + (HT2[1] - Z_AXLE) / math.tan(HEAD) + RAKE      # the front axle's x = the wheelbase
STEM_TOP = (HT1[0] - 170.0 * math.cos(HEAD), HT1[1] + 170.0 * math.sin(HEAD))


def tube(id, a, b, r, mat, y=0.0, **kw):
    return CY(id, (a[0], y, a[1]), (b[0], y, b[1]), r, mat, **kw)


def wheel(tag, cx):
    P = []
    rc = R - TS / 2
    ch = 2 * rc * math.tan(math.pi / NSEG)
    for k in range(NSEG):
        a = 2 * math.pi * k / NSEG
        c = [cx + rc * math.cos(a), 0.0, Z_AXLE + rc * math.sin(a)]
        P.append({"id": "%s_tyre%d" % (tag, k + 1), "type": "box", "c": [round(v, 2) for v in c], "s": [round(ch, 1), TS, TS], "rot": [0, -(math.degrees(a) + 90.0), 0], "material": "tyre",
                  "note": "tyre and rim segment (16 round the wheel), section 38 x 38"})
    P.append(CY("%s_hub" % tag, (cx, -50.0, Z_AXLE), (cx, 50.0, Z_AXLE), 22.0, "steel", note="hub 44 across, 100 long"))
    for k in range(8):
        a = 2 * math.pi * (k + 0.5) / 8
        r0, r1 = 24.0, R - TS - 2.0
        P.append(CY("%s_spoke%d" % (tag, k + 1), (cx + r0 * math.cos(a), 0.0, Z_AXLE + r0 * math.sin(a)), (cx + r1 * math.cos(a), 0.0, Z_AXLE + r1 * math.sin(a)), 1.2, "steel", note="spoke 2.4 across (8 drawn of 36)"))
    return P


def guard(tag, cx, a0, a1):
    P = []
    n = 5
    rg = R + 8.0
    chord = 2 * rg * math.tan(math.radians((a1 - a0) / n / 2)) + 2.0
    for k in range(n):
        a = math.radians(a0 + (k + 0.5) * (a1 - a0) / n)
        P.append({"id": "%s_guard%d" % (tag, k + 1), "type": "box", "c": [round(cx + rg * math.cos(a), 2), 0.0, round(Z_AXLE + rg * math.sin(a), 2)], "s": [round(chord, 1), 60.0, 2.0], "rot": [0, -(math.degrees(a) + 90.0), 0], "material": "paint_black",
                  "note": "mudguard segment, 60 wide, 2 thick"})
    return P


def bike():
    P = []
    P += wheel("rw", 0.0) + wheel("fw", FX)
    P += guard("rw", 0.0, 20.0, 160.0) + guard("fw", FX, 20.0, 150.0)
    P.append(tube("seat_tube", BB, SEAT_TOP, 14.0, "paint_black", note="seat tube 28 across, 560 centre to top, 72 degrees"))
    P.append(tube("top_tube", SEAT_TOP, HT1, 14.0, "paint_black", note="top tube 28, 570 long, level"))
    P.append(tube("down_tube", BB, HT2, 15.0, "paint_black", note="down tube 30"))
    P.append(tube("head_tube", HT2, HT1, 18.0, "paint_black", note="head tube 36 across, 150 long, 68 degrees"))
    for s, y in (("l", -55.0), ("r", 55.0)):
        P.append(tube("chain_stay_%s" % s, BB, (0.0, Z_AXLE), 8.0, "paint_black", y=y, note="chain stay 16, 450 long"))
        P.append(tube("seat_stay_%s" % s, SEAT_TOP, (0.0, Z_AXLE), 8.0, "paint_black", y=y, note="seat stay 16"))
        P.append(tube("fork_%s" % s, HT2, (FX, Z_AXLE), 11.0, "paint_black", y=y * 1.05, note="fork blade 22, rake 45 at the foot"))
    P.append(B("seat_bridge", SEAT_TOP[0] - 8, SEAT_TOP[0] + 8, -60.0, 60.0, SEAT_TOP[1] - 10, SEAT_TOP[1] + 10, "paint_black", note="seat-stay bridge"))
    P.append(B("fork_crown", HT2[0] - 12, HT2[0] + 12, -62.0, 62.0, HT2[1] - 30, HT2[1] - 6, "paint_black", note="fork crown"))
    P.append(CY("seat_post", (SEAT_TOP[0], 0.0, SEAT_TOP[1]), (SEAT_TOP[0] - 45.0, 0.0, 985.0), 11.0, "steel", note="seat post 22"))
    P.append(B("saddle", SEAT_TOP[0] - 45.0 - 150.0, SEAT_TOP[0] - 45.0 + 130.0, -90.0, 90.0, 985.0, 1035.0, "saddle_black", edge="nose r 30, edges r 8", note="saddle 280 x 180 x 50, leather-look, springs not modelled"))
    P.append(tube("stem", HT1, STEM_TOP, 11.0, "steel", note="stem 22, 170 above the head tube"))
    P.append(CY("bar_mid", (STEM_TOP[0], -190.0, STEM_TOP[1]), (STEM_TOP[0], 190.0, STEM_TOP[1]), 11.0, "steel", note="handlebar: the straight middle, 22 across, 380 wide"))
    for s, y in (("l", -1.0), ("r", 1.0)):
        P.append(CY("bar_sweep_%s" % s, (STEM_TOP[0], y * 190.0, STEM_TOP[1]), (STEM_TOP[0] - 85.0, y * 290.0, STEM_TOP[1] + 12.0), 11.0, "steel", note="swept-back end, 100 across to 580 over the grips"))
        P.append(CY("grip_%s" % s, (STEM_TOP[0] - 85.0, y * 290.0, STEM_TOP[1] + 12.0), (STEM_TOP[0] - 90.0, y * 395.0, STEM_TOP[1] + 14.0), 14.0, "grip_black", note="grip 28 across, 105 long"))
    P.append(CY("bell", (STEM_TOP[0] + 5.0, -150.0, STEM_TOP[1] + 14.0), (STEM_TOP[0] + 5.0, -150.0, STEM_TOP[1] + 40.0), 26.0, "steel", note="bell 52 across, a plain dome"))
    P.append(CY("bb_spindle", (BB[0], -70.0, BB[1]), (BB[0], 70.0, BB[1]), 12.0, "steel", note="bottom bracket spindle"))
    P.append(CY("chainring", (BB[0], 52.0, BB[1]), (BB[0], 58.0, BB[1]), 90.0, "steel", note="chainring 180 across, 6 thick (the chainguard is not modelled)"))
    P.append(B("crank_r", BB[0] - 10.0, BB[0] + 170.0, 58.0, 70.0, BB[1] - 10.0, BB[1] + 10.0, "steel", note="right crank arm 170 long"))
    P.append(B("crank_l", BB[0] - 170.0, BB[0] + 10.0, -70.0, -58.0, BB[1] - 10.0, BB[1] + 10.0, "steel", note="left crank arm 170 long"))
    P.append(B("pedal_r", BB[0] + 100.0, BB[0] + 200.0, 70.0, 175.0, BB[1] - 12.0, BB[1] + 12.0, "steel", note="pedal 100 x 105 x 24, rubber blocks not modelled"))
    P.append(B("pedal_l", BB[0] - 200.0, BB[0] - 100.0, -175.0, -70.0, BB[1] - 12.0, BB[1] + 12.0, "steel"))
    return P


def build():
    P1 = bike()
    # the leaning variant: the same parts rolled 12 degrees about the line of the two tyre contacts (the x axis at the ground) toward +y, with a wall
    lean = 12.0
    P2 = []
    for p in P1:
        q = json.loads(json.dumps(p))
        q["xf"] = {"rot": [0, 0, lean], "t": [0, 0, 0], "pivot": [0, 0, 0]}
        P2.append(q)
    ps2 = L.PartSet(P2)
    wall_y = float(max(ps2.part_bbox(n)[1][1] for n in ("grip_r", "bar_sweep_r", "pedal_r")))
    P2.append(B("wall", -600.0, 2000.0, wall_y, wall_y + 200.0, -50.0, 2400.0, "wall_brick", note="the wall (a stand-in slab)"))
    ps1 = L.PartSet(P1)
    lo, hi = ps1.bbox()
    T = {
        "family": FAMILY, "title": "Quay Street's bicycle against a wall",
        "units": "millimetres; angles in degrees; z up; x forward (the front wheel at +x); y to the rider's right; the pivot is the rear wheel's ground contact",
        "status": "written 13 October 2026, not yet reviewed", "sample": "BI2",
        "materials": {
            "paint_black": {"name": "black enamel, chipped and rusting at the welds", "srgb": [24, 26, 26], "rough": 0.45, "rough_words": "semi-gloss", "metal": True, "note": "frame, forks, mudguards: chipped to red-brown rust at the dropouts, the lower head tube and the mudguard stays"},
            "steel": {"name": "chrome-plated steel gone dull", "srgb": [150, 152, 150], "rough": 0.4, "rough_words": "dull satin", "metal": True, "note": "bars, stem, cranks, hubs, spokes: pitted with orange rust spots, never mirror bright"},
            "tyre": {"name": "black rubber tyre, cracked, grey-white dust", "srgb": [30, 30, 30], "rough": 0.8, "rough_words": "matt", "metal": False, "note": "a pale grey bloom of dust on the sidewalls; the rim (not separate) is dull steel in the 2 mm inner edge"},
            "saddle_black": {"name": "saddle black leather-look, cracked", "srgb": [34, 30, 28], "rough": 0.55, "rough_words": "semi-matt", "metal": False, "note": "cracked and shiny at the nose, a worn nose edge"},
            "grip_black": {"name": "grips black rubber, worn", "srgb": [22, 22, 22], "rough": 0.7, "rough_words": "matt", "metal": False, "note": ""},
            "wall_brick": {"name": "soot-blackened brick (the street's)", "srgb": [78, 64, 58], "rough": 0.9, "rough_words": "rough", "metal": False, "note": "a stand-in"},
        },
        "variants": {
            "BI1": {"name": "BI1: an adult's roadster standing upright (a stand-in for a bicycle held up by its rider)", "parts": P1, "overall": {"w": round(float(hi[0] - lo[0]), 1), "d": round(float(hi[1] - lo[1]), 1), "h": round(float(hi[2] - lo[2]), 1)}, "overall_tol": 2.0, "contact_tol": 3.0,
                    "joins": [["seat_tube", "top_tube"], ["top_tube", "head_tube"], ["down_tube", "head_tube"], ["down_tube", "seat_tube"], ["rw_hub", "chain_stay_l"], ["fw_hub", "fork_l"], ["rw_tyre2", "rw_spoke1"], ["fw_tyre2", "fw_spoke1"], ["rw_hub", "rw_spoke1"], ["bar_mid", "stem"], ["grip_r", "bar_sweep_r"], ["saddle", "seat_post"], ["crank_r", "bb_spindle"], ["pedal_r", "crank_r"]],
                    "embeds": [["seat_tube", "top_tube", 14.0], ["seat_tube", "down_tube", 14.0], ["head_tube", "top_tube", 16.0], ["head_tube", "down_tube", 16.0], ["head_tube", "fork_crown", 12.0], ["head_tube", "stem", 12.0], ["seat_tube", "seat_post", 12.0], ["seat_tube", "seat_bridge", 12.0], ["seat_tube", "chain_stay_l", 8.0], ["seat_tube", "chain_stay_r", 8.0],
                               ["down_tube", "chain_stay_l", 8.0], ["down_tube", "chain_stay_r", 8.0], ["chain_stay_l", "bb_spindle", 12.0], ["chain_stay_r", "bb_spindle", 12.0], ["down_tube", "bb_spindle", 12.0], ["seat_tube", "bb_spindle", 12.0], ["rw_hub", "chain_stay_l", 22.0], ["rw_hub", "chain_stay_r", 22.0], ["rw_hub", "seat_stay_l", 22.0], ["rw_hub", "seat_stay_r", 22.0],
                               ["fw_hub", "fork_l", 22.0], ["fw_hub", "fork_r", 22.0], ["bar_mid", "stem", 12.0], ["bar_mid", "bar_sweep_l", 12.0], ["bar_mid", "bar_sweep_r", 12.0], ["bell", "bar_mid", 12.0], ["grip_l", "bar_sweep_l", 12.0], ["grip_r", "bar_sweep_r", 12.0], ["crank_r", "chainring", 12.0], ["crank_r", "bb_spindle", 12.0], ["crank_l", "bb_spindle", 12.0],
                               ["pedal_r", "crank_r", 12.0], ["pedal_l", "crank_l", 12.0], ["seat_bridge", "seat_stay_l", 8.0], ["top_tube", "stem", 8.0], ["down_tube", "fork_crown", 9.0], ["fork_l", "fork_crown", 9.0], ["fork_r", "fork_crown", 9.0], ["seat_bridge", "seat_stay_r", 8.0], ["fork_crown", "fork_l", 12.0], ["fork_crown", "fork_r", 12.0], ["saddle", "seat_post", 12.0], ["seat_post", "top_tube", 12.0], ["stem", "head_tube", 12.0]],
                    "overlap_allow": 6.0, "faces": []},
            "BI2": {"name": "BI2: the roadster leaning 12 degrees against a brick wall, handlebar end and pedal against it (the sample)", "parts": P2, "overlap_allow": 6.0, "contact_tol": 3.0, "joins": [["grip_r", "wall"]], "embeds": "SAME_AS_BI1", "faces": []},
        },
        "drawing": {"views": ["front", "left", "plan"], "sections": [{"id": "y0", "axis": "y", "at": 0.0}, {"id": "x449", "axis": "x", "at": 449.0}]},
        "numbers": [
            {"id": "N1", "what": "tyre outer diameter (the wheel)", "value": 2 * R, "kind": "Judgement", "source": "a 26 x 1 3/8 inch roadster tyre: 590 mm bead seat plus two 35 mm sections is about 660 (the ISO number is from memory: not reached on a page this session); error 10", "tol": 10.0, "measure": {"kind": "bbox", "axis": "z", "parts": ["rw_tyre%d" % k for k in range(1, 17)]}, "variant": "BI1"},
            {"id": "N2", "what": "wheelbase (axle to axle)", "value": round(FX, 1), "kind": "Judgement", "source": "a gent's roadster's wheelbase is about 1100 to 1140; from the stated tube lengths and angles: %.0f; error 40" % FX, "tol": 40.0, "measure": {"kind": "centre_dx", "axis": "x", "a": "rw_hub", "b": "fw_hub"}, "variant": "BI1"},
            {"id": "N3", "what": "saddle top above the ground", "value": 1035.0, "kind": "Judgement", "source": "a rider of 1.75 m sits with the saddle about 1.0 m up; error 40", "tol": 40.0, "measure": {"kind": "edge", "axis": "z", "part": "saddle", "side": "hi"}, "variant": "BI1"},
            {"id": "N4", "what": "handlebar grips above the ground", "value": round(STEM_TOP[1] + 13.0 + 14.0, 1), "kind": "Judgement", "source": "roadster bars stand about as high as the saddle or just above it; error 40", "tol": 40.0, "measure": {"kind": "edge", "axis": "z", "part": "grip_r", "side": "hi"}, "variant": "BI1"},
            {"id": "N5", "what": "bottom bracket height", "value": 300.0, "kind": "Judgement", "source": "a roadster's bottom bracket is about 300 mm up (30 mm below the axles); error 15", "tol": 15.0, "measure": {"kind": "centre", "axis": "z", "part": "bb_spindle"}, "variant": "BI1"},
            {"id": "N6", "what": "handlebar width over the grips", "value": 790.0, "kind": "Judgement", "source": "swept-back roadster bars are 560 to 620 between the bends and about 790 over the grips' ends; error 50", "tol": 50.0, "measure": {"kind": "span", "axis": "y", "a": "grip_l", "b": "grip_r"}, "variant": "BI1"},
            {"id": "N7", "what": "crank length", "value": 170.0, "kind": "Judgement", "source": "170 mm, the usual crank; error 6", "tol": 6.0, "measure": {"kind": "span", "axis": "x", "a": "crank_l", "b": "crank_r"}, "variant": "BI1"},
        ],
        "photos": [], "sources": [], "previews": [], "checks": [], "owed": [],
    }
    T["variants"]["BI2"]["embeds"] = T["variants"]["BI1"]["embeds"]
    T["numbers"][6]["value"] = 340.0
    T["numbers"][6]["what"] = "crank span: the two arms' outer ends along x (two cranks of 170, crossing at the spindle)"
    T["lean"] = {"deg": lean, "wall_y_mm": round(wall_y, 1)}
    return T


def finish(T):
    T["sources"] = [
        {"id": "S1", "url": "https://www.geograph.org.uk/photo/2932507", "read": "2026-10-13", "author": "Jeremy Bolwell", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2012-05-06", "kind": "photograph",
         "shows": "a rusted gent's roadster leaning on a stone wall in a ruined building: a diamond frame with a level top tube, two big spoked wheels with mudguards, swept-back bars, a sprung saddle, a rear carrier; the rear wheel nearer the camera so the perspective is strong",
         "used": True, "not_used_for": "any number (the camera is oblique and close, the picture low in contrast); the rust is a wear state, not the sample's",
         "period": "2012; a roadster of the 1950s to 1970s kind, the type an old man or a dock worker still rode in 1990"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/4155634", "read": "2026-10-13", "author": "DS Pugh", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2014-09-01", "kind": "photograph",
         "shows": "a modern road bicycle leaning with its front tyre against a dry-stone wall: shows how a bicycle leans on a wall (front wheel and bar end against the stone, the rear wheel on the ground at a lean of about 10 to 15 degrees); a pannier and a bottle (brands masked)",
         "used": True, "not_used_for": "the bicycle's form (modern: 700c wheels, derailleur, drop frame) and any number", "period": "2014; used only for the leaning pose"},
        {"id": "S3", "url": "https://www.geograph.org.uk/photo/4811433", "read": "2026-10-13", "author": "Bill Nicholls", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2014-09-21", "kind": "photograph",
         "shows": "a black gent's roadster on a display stand in a museum room: the diamond frame in a clean side view, swept bars, a plain saddle, 28 inch wheels",
         "used": False, "not_used_for": "everything (an interior display of an older machine, not a street photograph: looked at for the frame's layout only)", "period": "2014 interior of a heritage machine"},
        {"id": "S4", "url": "https://api.polyhaven.com/assets?t=models", "read": "2026-10-13", "author": "Poly Haven artists", "licence": "CC0 1.0", "taken": "n/a (the list of 521 models)", "kind": "model list",
         "shows": "no bicycle", "used": False, "not_used_for": "everything: no CC0 bicycle exists, so it is made by script", "period": "n/a"},
        {"id": "S5", "url": "https://api.geograph.org.uk/syndicator.php (terms bicycle, bicycles, bicycle wall, bike leaning; takenyear 1975 to 1996 and without a year)", "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)", "taken": "1975 to 1996 searched", "kind": "search record",
         "shows": "1975 to 1996: a 1991 timbered house with a bicycle at its door, a 1992 station platform with cyclists, a 1993 night view of parked bicycles, a 1994 trail rider, a 1996 sporting photograph; none of a bicycle against a wall close up",
         "used": False, "not_used_for": "measuring", "period": "n/a"},
        {"id": "S6", "url": "canon.md, the content rule (D18)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "n/a", "kind": "own",
         "shows": "the content rule keeps young people out of every image and every prop: the bicycle is an adult's, the frame 560 mm, no small wheels, no stabilisers, no basket", "used": True, "not_used_for": "shape", "period": "n/a"},
    ]
    T["previews"] = [
        {"file": "p1-ruin-roadster-leaning.jpg", "source": "S1", "credit": "Jeremy Bolwell, Geograph 2932507, CC BY-SA 2.0, 2012-05-06, cropped to the bicycle", "masked": ["nothing to mask: no person, no lettering"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
    ]
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the bicycle stands against the blank wall between lamp pools; the chrome catches the lantern colour (1.0, 0.25, 0.0) as thin glints on the rims and bars, the black frame vanishes"}
    T["placement"] = {
        "slot": "west side, against the blank soot-brick wall of the west_south block (the plain ground floor: no shopfront), centre x 15.0 m, the bicycle parallel to the wall with its handlebar end touching it, leaning 12 degrees, its tyres 0.34 m from the wall at the ground (the wall at z -5.125)",
        "x_m": 15.0, "wall_z_m": -5.125, "footway_mm": 2000.0, "min_clear_mm": 1000.0, "length_mm": T["variants"]["BI1"]["overall"]["w"],
        "reasons": [
            "the blank west wall is where the street's small things lean (the poster wall of the scene, x 11.4); a bicycle there blocks no shopfront and no door (the side door is at x 25.5)",
            "leaning, it takes a footway depth of its roll: a 12 degree lean puts the bar end and pedal 0.36 m from the tyres' line, leaving 1.64 m of the 2.0 m footway clear",
            "it is an adult's bicycle, ambient dressing that belongs to no one on the street's list of residents",
        ],
    }
    T["wear"] = [
        "enamel chipped to red-brown rust at the dropouts, the head tube's lower end, the seat-stay bridge and the mudguard stays; paint dulled, a few small dents in the mudguards",
        "chrome gone to dull grey with orange pitting on the bars, rims and spokes; the chain brown with oil and rust (not modelled)",
        "tyres hard, cracked at the sidewalls, one slightly soft (flat at the ground by 8 mm: a seed), grey dust bloom",
        "the saddle cracked and shiny at the nose; the grips worn smooth at their ends",
        "a wet street under it: darkness on the lowest 150 mm of the tyres and a grit splash on the mudguard",
        "NOT shown: a lock or chain bar (a chain through the wheel is a variant, a seed), a basket, stabilisers, any maker's badge on the head tube (a real bicycle has one; this has a blank plate)",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "which bicycle", "book": "the research notes list none; the brief asks for a bicycle against a wall", "photo": "S1 shows an old roadster leaning on a wall (the type of the period's older riders); S2 shows the leaning pose with a modern bicycle", "chose": "the roadster, upright geometry from the tube lengths and angles, the leaning pose from S2"},
        {"id": "W2", "what": "the lean", "book": "none", "photo": "S2: the rear tyre on the ground, the front tyre and the bar end on the wall, a lean of about 12 degrees", "chose": "12 degrees, the wall touching the right grip's end"},
    ]
    T["variants_note"] = [
        "BI2 (the sample): the roadster leaning 12 degrees on the wall.",
        "BI1: the same upright (for a bicycle held by a figure or standing on a stand).",
        "a ten-speed with drop bars is the second kind of adult bicycle of 1990: not written (its frame would be a new target); one kind only, as the street needs one bicycle.",
        "conditions (materials): C0 sound, C1 worn (the sample's wear), C2 rusted solid (S1's state, a derelict leaning for years).",
    ]
    T["owed"] = []
    T["not_settled"] = [
        "no 1975 to 1995 bicycle photograph was measurable and S1 and S2 are oblique and low in contrast: every number is Judgement (a gent's roadster's usual geometry), checked for internal consistency and against ranges, not against pixels",
        "the 26 x 1 3/8 wheel's exact tyre diameter (660 mm is from memory; the page that gives the ISO 590 bead seat was not reached)",
        "whether the street's bicycle should be a roadster or a ten-speed (the roadster is chosen because S1 is a street-leaning roadster)",
        "the rear carrier, lamp and chain guard are not modelled (they are textures and decals); the chain is not modelled",
        "the lean's wall contact is by the handlebar end (S2 shows the front tyre against the wall): either is a seed",
    ]
    T["content_rule_note"] = "an adult's bicycle only: no small frame, no stabilisers, no child seat, no toy (a statement of the content rule)."
    T["builder_notes"] = [
        "build by script: the tubes as cylinders from the end points in target.json (a part's p0 and p1), the tyres as one torus of section 38 (the 16 boxes are the engine's approximation), the 36 spokes (8 drawn) in the real wheel; the mudguards as one swept strip per wheel",
        "BI2 is BI1 with the part transform (a roll of 12 degrees about the x axis through the tyre contacts) and the wall; the builder places the bicycle with the transform",
        "no maker's badge, no transfer, no lettering of any kind",
        "the right pedal and the right grip end are the two points that can touch the wall",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.0f mm" % n["value"], "tol": "+-%.0f mm" % n["tol"]})
    C += [
        {"name": "C1: both wheels the same diameter, on the ground", "measure": "the tyres' bounding boxes", "expect": "660 mm, z 0", "tol": "+-10 mm"},
        {"name": "C2: no part floats; the bicycle touches the ground and the wall", "measure": "the contact graph", "expect": "connected", "tol": "0 floating"},
        {"name": "C3: the frame's tube angles", "measure": "seat tube 72 degrees, head tube 68 degrees", "expect": "72 and 68", "tol": "+-2 degrees"},
        {"name": "C4: no lettering, no badge", "measure": "textures and text", "expect": "none", "tol": "exact"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The bicycle is an adult's gent's roadster (26 x 1 3/8 wheels 660 mm over the tyre, a 1097 mm wheelbase, a level top tube on a 72 degree seat tube and a 68 degree head tube, swept-back bars 790 over the grips, a sprung saddle at 1035, mudguards, a plain bell, 170 mm cranks) in the enamel-chipped, dull-chromed state of a street bicycle, no badge or lettering, shown leaning 12 degrees on the blank west wall at x 15.0 with its right grip end against the brick; "
           "no period photograph was measurable (the two street photographs are oblique and low in contrast), so every number is Judgement within stated ranges and the target is checked for internal consistency, the tube angles and the ranges, not against pixels; an adult's bicycle only.")


def story(T):
    return {
        "no": "7", "title": "Quay Street's bicycle against a wall: the exact target", "summary": SUMMARY, "previews_list": "p1 (S1 cropped; no overlay: the photograph is too oblique and low in contrast to lay a drawing on)",
        "rulings": {"ruling_2oct": "not a car, skip or pallet; plain street dressing", "sources_order": "no CC0 bicycle exists (S4); so own work by script",
                    "content": "an adult's bicycle only; the data scan finds none of what the rule forbids", "noai": "S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to look at; no NoAI source",
                    "look": "dull chrome, rust spots and a wet street: grime is the strategy", "night": "chrome glints, the frame vanishes"},
        "searched": "What was searched: Poly Haven's model list (no bicycle); Geograph's feed for `bicycle`, `bicycles`, `bicycle wall`, `bike leaning` with each year 1975 to 1996 and without a year. Wikimedia Commons was not asked.",
        "reuse": [
            ["Poly Haven models", "no bicycle", "NOT USED", "S4"],
            ["vignette-scene.json, the asset plan, the research notes", "no bicycle anywhere", "NONE to reuse", "this is a new prop"],
            ["git branches (git log --all for bicycle, bike)", "none", "none to reuse", ""],
        ],
        "axes": "Axes: x forward (the front wheel at +x), y to the rider's right, z up from the ground at the tyres' contact. Cylinders for tubes, spokes and the hub, boxes for the tyre segments, the saddle, the cranks and the pedals; BI2 adds a transform and a wall.",
        "assembly": [
            "**Wheels**: 26 x 1 3/8, 660 over the tyre (a ring of 16 segments 38 x 38), a hub 44 across and 100 long, spokes 2.4 across (8 drawn of 36), mudguards 60 wide and 2 thick 8 mm over the tyre round the top 140 degrees.",
            "**Frame**: seat tube 28 across, 560 from the bottom bracket centre, 72 degrees; level top tube 28 across, 570 long; down tube 30 across; head tube 36 across and 150 long at 68 degrees; chain stays 16 across and 450 long, seat stays 16 across; the bottom bracket 300 up (30 below the axles).",
            "**Fork**: two blades 22 across with 45 rake at the foot, a crown 24 x 124 x 24.",
            "**Cockpit**: a stem 22 across rising 170 along the steering axis, a bar of 22 across, 380 straight between swept-back ends to 580 over the bends and 790 over the 105 mm grips, a bell 52 across.",
            "**Saddle and post**: a post 22 across to z 985, a saddle 280 x 180 x 50 at 985 to 1035.",
            "**Drive**: a spindle 24 across, a chainring 180 across, cranks 170, pedals 100 x 105 x 24 (the chain, the chain guard, the carrier and the lamp are textures or not modelled).",
        ],
        "own_rows": "the tube angles from the parts' own end points, the ranges for a roadster, the lean and the wall contact, the footway clearance",
    }


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
