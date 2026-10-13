"""milk-crates: writes target.json and TARGET.md (cloud week 42, unit 13, family 4: milk crates, a stack, with empties)."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_family as SF
from sd_lib import B, CY

FAMILY = "milk-crates"
CL, CW, CH = 408.0, 298.0, 264.0        # outer length, width, height (Poly Haven plastic_crate_01's measured box; CC0 data)
HL, HW = CL / 2, CW / 2
DAIRY = "COPPER ROW DAIRY"
PINT = {"body_r": 32.0, "body_h": 128.0, "neck_r": 14.0, "neck_h": 56.0}


def crate(tag, zo, bottles=0):
    P = []
    pf = lambda n: "%s_%s" % (tag, n)
    P.append(B(pf("floor"), -HL + 4, HL - 4, -HW + 4, HW - 4, zo, zo + 10, "crate_plastic", edge="edges r 2", note="floor plate, 10 thick, with 36 drain slots 20 x 8 (a mask in the build; see the text)"))
    for nm, (x0, x1, y0, y1) in (("rail_f", (-HL, HL, -HW, -HW + 4)), ("rail_b", (-HL, HL, HW - 4, HW)), ("rail_l", (-HL, -HL + 4, -HW + 4, HW - 4)), ("rail_r", (HL - 4, HL, -HW + 4, HW - 4))):
        P.append(B(pf(nm), x0, x1, y0, y1, zo, zo + 24, "crate_plastic", edge="lower edge r 2", note="base rail 24 high, 4 thick"))
    for nm, (x0, x1, y0, y1) in (("rim_f", (-HL, HL, -HW, -HW + 6)), ("rim_b", (-HL, HL, HW - 6, HW)), ("rim_l", (-HL, -HL + 6, -HW + 6, HW - 6)), ("rim_r", (HL - 6, HL, -HW + 6, HW - 6))):
        P.append(B(pf(nm), x0, x1, y0, y1, zo + CH - 28, zo + CH, "crate_plastic", edge="top edge r 3", note="rim 28 high, 6 thick, a stiffening band"))
    for nm, sx, sy in (("post_fl", -1, -1), ("post_fr", 1, -1), ("post_bl", -1, 1), ("post_br", 1, 1)):
        x0, x1 = (-HL, -HL + 16) if sx < 0 else (HL - 16, HL)
        y0, y1 = (-HW, -HW + 16) if sy < 0 else (HW - 16, HW)
        P.append(B(pf(nm), x0, x1, y0, y1, zo + 24, zo + CH - 28, "crate_plastic", edge="vertical edge r 4", note="corner post 16 x 16"))
    for i, x in enumerate((-102.0, 0.0, 102.0)):
        P.append(B(pf("rib_f%d" % i), x - 7, x + 7, -HW, -HW + 4, zo + 24, zo + CH - 28, "crate_plastic", note="rib 14 wide between the slots"))
        P.append(B(pf("rib_b%d" % i), x - 7, x + 7, HW - 4, HW, zo + 24, zo + CH - 28, "crate_plastic"))
    P.append(B(pf("band_f"), -HL + 16, HL - 16, -HW, -HW + 4, zo + 118, zo + 184, "crate_plastic", note="solid band 66 high that carries the dairy's name"))
    P.append(B(pf("band_b"), -HL + 16, HL - 16, HW - 4, HW, zo + 118, zo + 184, "crate_plastic"))
    P.append(B(pf("rib_l"), -HL, -HL + 4, -7, 7, zo + 24, zo + CH - 28, "crate_plastic", note="centre rib of each end wall; the two openings beside it are the hand holds"))
    P.append(B(pf("rib_r"), HL - 4, HL, -7, 7, zo + 24, zo + CH - 28, "crate_plastic"))
    for nm, sx, sy in (("lug_fl", -1, -1), ("lug_fr", 1, -1), ("lug_bl", -1, 1), ("lug_br", 1, 1)):
        x0, x1 = (-HL + 6, -HL + 20) if sx < 0 else (HL - 20, HL - 6)
        y0, y1 = (-HW + 6, -HW + 20) if sy < 0 else (HW - 20, HW - 6)
        P.append(B(pf(nm), x0, x1, y0, y1, zo + CH, zo + CH + 9, "crate_plastic", note="stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail"))
    # empties: pint bottles in a 4 x 3 grid of 100 mm cells (left, front)
    cells = [(-150.0 + 100.0 * i, -100.0 + 100.0 * j) for j in range(3) for i in range(4)]
    for k in range(bottles):
        x, y = cells[(k * 5) % 12 if bottles < 12 else k]
        P.append(CY(pf("bottle%d" % (k + 1)), (x, y, zo + 10), (x, y, zo + 10 + PINT["body_h"]), PINT["body_r"], "glass", note="empty pint bottle body (glass, no cap, foil gone)"))
        P.append(CY(pf("neck%d" % (k + 1)), (x, y, zo + 10 + PINT["body_h"]), (x, y, zo + 10 + PINT["body_h"] + PINT["neck_h"]), PINT["neck_r"], "glass", transparent=True, note="neck 28 across with a lip ring"))
    return P


def stack(n, bottles_top=0):
    P = []
    for i in range(n):
        P += crate("c%d" % (i + 1), i * CH, bottles_top if i == n - 1 else 0)
    return P


def joins(P):
    names = {p["id"] for p in P}
    J = []
    for c in sorted({n.split("_")[0] for n in names}):
        J += [[c + "_rail_f", c + "_floor"], [c + "_post_fl", c + "_rail_f"], [c + "_rim_f", c + "_post_fl"], [c + "_rib_f0", c + "_rail_f"], [c + "_band_f", c + "_rib_f0"],
              [c + "_lug_fl", c + "_rim_f"], [c + "_rim_l", c + "_rim_f"], [c + "_rail_l", c + "_rail_f"]]
    for i in range(1, len([n for n in names if n.endswith("_floor")])):
        J += [["c%d_rail_f" % (i + 1), "c%d_rim_f" % i], ["c%d_floor" % (i + 1), "c%d_lug_fl" % i]]
    return J


def embeds(P):
    names = {p["id"] for p in P}
    E = []
    for c in sorted({n.split("_")[0] for n in names}):
        for k in range(1, 7):
            if "%s_bottle%d" % (c, k) in names:
                E += [["%s_bottle%d" % (c, k), "%s_neck%d" % (c, k), 20.0], ["%s_bottle%d" % (c, k), "%s_floor" % c, 6.0]]
    for i in range(1, 4):
        for e in ("fl", "fr", "bl", "br"):
            E.append(["c%d_lug_%s" % (i, e), "c%d_floor" % (i + 1), 6.0])
    return E


def faces(P, tag, zo=0.0):
    return [
        {"id": "%s front band" % tag, "o": [-HL + 16, -HW - 0.0, zo + 118.0], "u": [1, 0, 0], "v": [0, 0, 1], "n": [0, -1, 0], "nu": CL - 32, "nv": 66.0, "depth": 8.0, "blockers": ["%s_band_f" % tag]},
        {"id": "%s rim front" % tag, "o": [-HL + 2, -HW, zo + CH - 26.0], "u": [1, 0, 0], "v": [0, 0, 1], "n": [0, -1, 0], "nu": CL - 4, "nv": 24.0, "depth": 10.0, "blockers": ["%s_rim_f" % tag]},
        {"id": "%s base rail front" % tag, "o": [-HL + 2, -HW, zo + 2.0], "u": [1, 0, 0], "v": [0, 0, 1], "n": [0, -1, 0], "nu": CL - 4, "nv": 20.0, "depth": 8.0, "blockers": ["%s_rail_f" % tag]},
    ]


def build():
    V1 = crate("c1", 0, 0)
    V3 = stack(3, 6)
    T = {
        "family": FAMILY, "title": "Quay Street's milk crates: a stack, with empties",
        "units": "millimetres; angles in degrees; z up; the long side's dairy band faces -y; the pivot is the bottom crate's footprint centre on the ground",
        "status": "fixes applied, not re-reviewed", "sample": "MC3",
        "materials": {
            "crate_plastic": {"name": "moulded crate plastic, faded", "srgb": [168, 40, 36], "rough": 0.5, "rough_words": "semi-gloss", "metal": False,
                              "note": "the sample crate is red: a JUDGEMENT (a dairy chose one colour for all its crates and dairies used many: red, blue, yellow, green, orange; the red was first seen on the rejected Poly Haven crate and S2's photograph shows blue crates, which stay the first variant); UV-faded to a lighter, chalky red on the top rim; grime in every slot; NO printed brand (the CC0 texture's 'GALLER STORAGE' print is not used)"},
            "glass": {"name": "clear glass, milk-filmed", "srgb": [210, 218, 214], "rough": 0.05, "rough_words": "smooth", "metal": False, "note": "a faint milky film on the inside, a dull ring where the cap sat; embossed dairy name on the shoulder"},
        },
        "variants": {
            "MC1": {"name": "MC1: one 12-pint crate, empty", "parts": V1, "overall": {"w": CL, "d": CW, "h": CH + 9.0}, "overall_tol": 1.0, "joins": joins(V1), "embeds": embeds(V1), "overlap_allow": 5.0, "faces": faces(V1, "c1")},
            "MC3": {"name": "MC3: a stack of three crates, six empty pint bottles in the top one (the sample)", "parts": V3, "overall": {"w": CL, "d": CW, "h": 3 * CH + 9.0}, "overall_tol": 1.0,
                    "joins": joins(V3), "embeds": embeds(V3), "overlap_allow": 5.0, "faces": faces(V3, "c2", CH)},
        },
        "drawing": {"views": ["front", "left", "plan"], "sections": [{"id": "x0", "axis": "x", "at": 0.0}, {"id": "z140", "axis": "z", "at": 140.0}]},
        "numbers": [
            {"id": "N1", "what": "crate outer length", "value": CL, "kind": "Read", "source": "Poly Haven plastic_crate_01 (CC0, tagged beverage crate and milk crate): dimensions [298.0, 408.0, 264.2] read from api.polyhaven.com/info on 13 October 2026; the self-check's --live re-reads them", "tol": 1.0, "measure": {"kind": "bbox", "axis": "x", "parts": [p["id"] for p in V1 if "lug" not in p["id"]]}, "variant": "MC1"},
            {"id": "N2", "what": "crate outer width", "value": CW, "kind": "Read", "source": "same record: 298.0", "tol": 1.0, "measure": {"kind": "bbox", "axis": "y", "parts": [p["id"] for p in V1 if "lug" not in p["id"]]}, "variant": "MC1"},
            {"id": "N3", "what": "crate height to the rim (lugs excluded)", "value": CH, "kind": "Read", "source": "same record: 264.2; 264 kept", "tol": 1.0, "measure": {"kind": "bbox", "axis": "z", "parts": [p["id"] for p in V1 if "lug" not in p["id"]]}, "variant": "MC1"},
            {"id": "N4", "what": "stack pitch: one crate's base on the next one's rim", "value": CH, "kind": "Derived", "source": "the base rail's underside rests on the rim top; the lugs (9 high) enter the next floor's recesses; so the pitch is the crate height", "tol": 1.0, "measure": {"kind": "centre_dx", "axis": "z", "a": "c1_floor", "b": "c2_floor"}},
            {"id": "N5", "what": "stack height of three crates with lugs", "value": 3 * CH + 9.0, "kind": "Derived", "source": "3 x 264 + 9", "tol": 1.5, "measure": {"kind": "bbox", "axis": "z", "parts": [p["id"] for p in V3 if "bottle" not in p["id"] and "neck" not in p["id"]]}},
            {"id": "N6", "what": "bottle body diameter", "value": 64.0, "kind": "Judgement", "source": "a pint milk bottle's body is about 64 mm across (twelve fit a 4 x 3 grid of 100 mm cells with room); not measured on a photograph; error 6", "tol": 6.0, "measure": {"kind": "extent", "axis": "x", "part": "c3_bottle1"}},
            {"id": "N7", "what": "bottle height (body and neck)", "value": 184.0, "kind": "Judgement", "source": "about 184 mm for a pint (128 body + 56 neck); error 15", "tol": 15.0, "measure": {"kind": "span", "axis": "z", "a": "c3_bottle1", "b": "c3_neck1"}},
            {"id": "N8", "what": "name band height", "value": 66.0, "kind": "Judgement", "source": "P1's name panel on the front wall reads about 60 to 70 mm (oblique view); error 12", "tol": 12.0, "measure": {"kind": "extent", "axis": "z", "part": "c1_band_f"}, "variant": "MC1"},
            {"id": "N9", "what": "rim height", "value": 28.0, "kind": "Judgement", "source": "P1's rim band reads 13 px of 105 for 528 mm = 65 mm including the rim's top face seen from 45 degrees above; the front face alone is taken as 28 (error 12)", "tol": 12.0, "measure": {"kind": "extent", "axis": "z", "part": "c1_rim_f"}, "variant": "MC1"},
        ],
        "photos": [], "sources": [], "previews": [], "checks": [], "owed": [],
    }
    return T


def polyhaven_record():
    UA = "LedgerProject-reference-research/1.0 (street furniture measurement; no contact)"
    pth = os.path.join(HERE, "polyhaven_checked_raw.json")
    if os.path.exists(pth):
        return json.load(open(pth))
    out = {}
    for k in ("plastic_crate_01", "plastic_crate_02", "plastic_crate_03", "wooden_crate_01", "wooden_crate_02"):
        r = subprocess.run(["curl", "-sS", "-m", "40", "-A", UA, "https://api.polyhaven.com/info/%s" % k], capture_output=True)
        try:
            out[k] = json.loads(r.stdout)
        except Exception:
            out[k] = None
    json.dump(out, open(pth, "w"), indent=1)
    return out


def finish(T):
    ph = polyhaven_record()
    T["polyhaven"] = {k: {"dimensions": v["dimensions"], "authors": v["authors"], "tags": v["tags"][:6], "description": v["description"]} for k, v in ph.items() if v}
    T["sources"] = [
        {"id": "S1", "url": "https://polyhaven.com/a/plastic_crate_01 (api.polyhaven.com/info/plastic_crate_01 and /files/plastic_crate_01)", "read": "2026-10-13", "author": "PierreB3D (Poly Haven)", "licence": "CC0 1.0", "taken": "model published 2026-06",
         "kind": "model", "shows": "a deep red plastic crate with lattice sides, cutout handles and a worn storage print, 298 x 408 x 264 mm, 18,320 triangles, tagged milk crate; its 1k base colour carries the lettering GALLER STORAGE (looked at at 100 percent on 13 October)",
         "used": True, "not_used_for": "its mesh and texture: the lattice sides and the print disagree with the photographs and the rules; ONLY its box (298 x 408 x 264) is used as the measured size", "period": "a modern storage crate; the 12-pint milk crate's box is the same"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/6898849", "read": "2026-10-13", "author": "Jaggery", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2021-07-14", "kind": "photograph",
         "shows": "two blue crates stacked on a pavement against a shutter, seen from about 45 degrees above: a deep rim band, a name band on the front wall, slots between ribs, a stack with the upper crate's base on the lower rim; four plastic bottles in the top crate (a 2021 pack, not glass pints)",
         "used": True, "not_used_for": "any number (oblique; the view's foreshortening makes every vertical ratio unusable); the dairy's name (masked); the plastic bottles", "period": "2021; the crate form is that of 1990 (the design has not changed) but the bottles are modern"},
        {"id": "S3", "url": "https://www.geograph.org.uk/photo/4802548", "read": "2026-10-13", "author": "Robert Lamb", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2016-01-23", "kind": "photograph",
         "shows": "stacks of red, blue, green and orange crates used as benches: shows the colour range and the stacking in courses",
         "used": False, "not_used_for": "everything (looked at only: two people in the frame; a stall's lettering)", "period": "2016"},
        {"id": "S4", "url": "https://api.polyhaven.com/assets?t=models", "read": "2026-10-13", "author": "Poly Haven artists", "licence": "CC0 1.0", "taken": "n/a (the list of 521 models)", "kind": "model list",
         "shows": "plastic_crate_01 (298 x 408 x 264), plastic_crate_02 (506 x 406 x 254), plastic_crate_03 (481 x 265 x 266), wooden_crate_01 and 02, cardboard_box_01; no pint bottle", "used": True, "not_used_for": "any other model", "period": "n/a"},
        {"id": "S5", "url": "https://api.geograph.org.uk/syndicator.php (terms milk crates, crates, milk float, milk bottles, each with takenyear 1975 to 1996)", "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)", "taken": "1975 to 1996 searched", "kind": "search record",
         "shows": "milk floats of 1975 to 1995 in village and town photographs, none showing crates closely; the term 'crates' alone returned nothing", "used": False, "not_used_for": "measuring", "period": "n/a"},
        {"id": "S6", "url": "production/specs/vignette-scene.json (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "n/a", "kind": "own",
         "shows": "the yard mouth holds two wooden crates (wooden_crate_01 twice, x 22.4 and 23.1 west) and a barrel; no milk crates, no pallet, no skip", "used": True, "not_used_for": "any shape", "period": "n/a"},
    ]
    T["previews"] = [{"file": "p1-pavement-two-crates-stacked.jpg", "source": "S2", "credit": "Jaggery, Geograph 6898849, CC BY-SA 2.0, 2021-07-14, cropped to the crates; the printed dairy's name on the front band painted out, the bottles' labels blurred",
                      "masked": ["the dairy's name on the front band (painted out)", "the bottle labels (blurred)"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True}]
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the crates stand in the grocer's doorway recess, outside the lamp pools; the red plastic reads near black under the lantern colour (1, 0.25, 0) with a glint on the rim's top edge and on the bottles' glass"}
    T["text"] = {"dairy": DAIRY, "dairy_note": "a FICTIONAL PLACEHOLDER (the town has not minted the dairy yet: handover H1): carried by a separate, swappable lettering layer (a normal map and a colour decal on the front band and on each bottle's shoulder, NOT mesh), blank in any picture for his page; capitals 18 mm tall on the band, 6 mm on the bottles; no logo, no real dairy's name, no cow, no price",
                 "layer": {"kind": "a normal and colour decal, not mesh", "swappable": True, "blank_in_pictures_for_his_page": True, "where": ["band_f", "band_b", "bottle shoulders"]},
                 "band_text": DAIRY + " | PROPERTY OF THE DAIRY | THIS CRATE IS NOT TO BE USED FOR ANY OTHER PURPOSE", "band_text_mm": [18.0, 6.0], "bottle_text": DAIRY}
    T["placeholders"] = [{"name": "Copper Row Dairy", "marked": "fictional placeholder", "kind": "the dairy's name on the crates' bands and the bottles' shoulders", "where": "text.dairy and the lettering layer (a swappable decal, blank in pictures for his page)", "until": "the town mints the dairy (handover H1)"}]
    T["handovers"] = [{"id": "H1", "line": "For the town: mint the dairy that supplies the grocer and the tea room (its name for the crates' bands and the bottles' shoulders; now the placeholder 'Copper Row Dairy' in a swappable lettering layer, never shown on Jafar's page), within canon's naming rules."}]
    T["placement"] = {
        "slot": "east side, bay 5 (the grocer, x 33 to 39): one stack of three crates against the window's stallriser, centre x 37.30 (the stack's x 37.096 to 37.504, 0.14 m from the door jamb at x 37.644; the grocer has NO side door: its shop door is the 1006 mm at the high-x end, x 37.644 to 38.650, in a 600 mm recessed lobby), back 0.05 m clear of the stallriser line (z 4.975), long side facing the road; a second, single crate (MC1) is the street's spare, not placed",
        "x_m": 37.3, "stallriser_z_m": 4.975, "gap_to_wall_mm": 50.0, "kerb_back_z_m": 3.125, "clear_strip_mm": 1502.0, "footway_mm": 2000.0, "min_clear_mm": 1000.0, "shop_bay": {"name": "grocer", "x0": 33.0, "x1": 39.0},
        "milk_float": "yes: Quay Street's grocer and the tea room are doorstep customers of the dairy (a 1990 fact of British shops; Judgement, no source in canon names a float): the empties are put out for collection at the shop door; no milk float is drawn (the cars ruling), only its crates",
        "reasons": [
            "crates stand at the shop that sells milk: the grocer (bay 5) takes a daily delivery; the stack stands 50 mm clear of the stallriser line (z 4.975) so it never leans on the glass, its 298 mm width taking 4.627 to 4.925 of the footway and leaving 1.50 m clear from the kerb's back edge (3.125)",
            "THE FIRST VERSION STOOD IT ACROSS THE SHOP DOOR (x 38.0, 'the grocer's side-door end'): the grocer has no side door (terrace-front.py BAY_WITHOUT_SIDE_DOOR = 5); its shop door is the outer 1006 mm at the high-x end, x 37.644 to 38.650 (centre 38.147), in a 600 mm recessed lobby (shopfronts target, shops[grocer]), and the stack (x 37.796 to 38.204) stood in the lobby's mouth; the placement rows tested only that it lay inside x 33 to 39 and the strip to the kerb. At x 37.30 it stands against the window's stallriser (x 33.35 to 37.644), 0.14 m from the door's jamb; the shared placement rows now test it against the shopfronts target's door zones and every piece of the scene",
            "it stands at the shop's door end, clear of the door, beside the litter and bin traffic of the east parade's end, 6.4 m from the chandler's shop door (x 43.70 to 44.71; the chandler's doors are at x 43.70 to 45.65)",
            "the scene's yard-mouth crates are wooden and stay (one family's yard stuff); these are the grocer's",
        ],
        "poses": [{"id": "stack", "variant": "MC3", "x_m": 37.3, "z_m": round(4.975 - 0.05 - 0.149, 4), "yaw_deg": 0.0, "zone": "east_footway", "front_faces": "-z"}],
    }
    T["wear"] = [
        "the plastic is scuffed white along the rim's top edge and the lugs, and along the base rail's lower edge where crates are dragged; the faded top rim is chalkier than the body",
        "dirt in every slot and in the floor's drain slots (a darker mask), a milky film on the floor under the bottles, a dried ring where bottles stood",
        "the bottles: cap-less, a dull ring on each lip, embossed shoulder, a smear of old milk inside the lowest 10 mm (a mask on the glass)",
        "one crate in the stack is a different colour (blue) from the other two: crates were swapped between dairies' rounds only within a dairy, so the stack is one colour in the sample and a blue one is a variant",
        "NOT shown: any lettering but the dairy's name, a person, any other drink, a sticker",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "the crate model", "book": "S1 (CC0): a lattice-sided storage crate with a printed brand-like name; the asset plan wants CC0 first", "photo": "S2: slot-sided crates with a solid name band on the front wall and a deep rim", "chose": "built by script to S1's box with slot sides and a name band; S1's mesh and texture are not used (its base colour carries the lettering GALLER STORAGE)"},
        {"id": "W2", "what": "the bottles", "book": "the photograph's four-pint plastic bottles", "photo": "S2 shows 2021 plastic bottles; 1990's were glass pints", "chose": "glass pint bottles, empty, no cap, an embossed fictional name"},
        {"id": "W3", "what": "the stacking", "book": "none", "photo": "S2 shows the upper crate's base resting on the lower crate's rim with the lugs inside", "chose": "pitch = crate height 264, lugs 9 high entering the next floor"},
    ]
    T["variants_note"] = [
        "MC3 (the sample): three crates, six empty pint bottles in the top one, one colour (red).",
        "MC1: a single crate, empty (a spare for the yard or a doorstep).",
        "colours: red (the sample, a Judgement), blue (S2's photograph), yellow, green, orange (a dairy's crates are all one colour); fade and grime as wear.",
        "a crate on its side or two stacked with bottles in the lower one (a seed, not a mesh): the builder may place the MC1 mesh as it likes.",
    ]
    T["owed"] = []
    T["not_settled"] = [
        "no photograph of a 1975 to 1995 crate was reached; P1 is a 2021 oblique view, so the slot layout, the rim depth (28 mm, error 12) and the name band (66 mm, error 12) are judged; the box is Poly Haven's measured 298 x 408 x 264",
        "whether a 1990 12-pint crate is 264 high (the CC0 record, a storage crate tagged milk crate) or nearer 200: the bottles then stand fully inside (their tops 70 mm below the rim); one number for the builder to confirm against a period crate if one is ever reached",
        "the stack's lettering layer is not yet textured (a decal on the band and the shoulders): the dairy is a placeholder (handover H1)",
        "the crate's slot sizes and the floor's drain slots (36 slots 20 x 8 are a Judgement written as a texture mask, not geometry)",
        "whether a milk float served Quay Street: stated as a Judgement; the empties are the only sign of it",
        "the pint bottle's exact shape (body 64 across, neck 28, 184 high: Judgement)",
    ]
    T["content_rule_note"] = "milk, not drink: no beer, wine or spirit bottle, no crate with a drinks brand, no person (a statement of the content rule)."
    T["builder_notes"] = [
        "build the crate by script in one mesh: floor plate with 36 drain slots cut (a mask or real holes), four walls as ribs and slots (the gaps between the ribs are open), rim, base rail with four recesses under the corners for the lugs, name band with the raised text",
        "stack by instancing the crate at z 0, 264, 528 (no scale), rotate each crate by a seed of 0 to 2 degrees about z (not more: they interlock)",
        "bottles: glass, a body 128 and neck 56 with a lip ring; six in the top crate in a 4 x 3 grid of 100 mm cells (six of the twelve cells)",
        "texture: our own colour map for the crate; the CC0 model's texture is NOT used (its lettering); the dairy's name is a separate swappable decal layer (normal and colour), blank in any picture for his page",
        "stand the stack at x 37.30, z 4.776 (its centre), 0.14 m clear of the grocer's door jamb; never in front of the lobby (x 37.644 to 38.650)",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.1f mm" % n["value"], "tol": "+-%.1f mm" % n["tol"]})
    C += [
        {"name": "C1: the crate's box", "measure": "outer box of one crate without its lugs", "expect": "408 x 298 x 264", "tol": "+-1 mm"},
        {"name": "C2: three crates stacked, six bottles", "measure": "count crates and bottles", "expect": "3 and 6", "tol": "exact"},
        {"name": "C3: the walls closed where they should be", "measure": "rays at the front band, the rim and the base rail at 0, 30 and 45 degrees", "expect": "0 get through", "tol": "exact"},
        {"name": "C4: no part floats, every join meets", "measure": "the contact graph", "expect": "all parts reach the ground", "tol": "0 floating"},
        {"name": "C5: the text", "measure": "the lettering layer (a swappable decal, not mesh)", "expect": "the placeholder dairy only, blank in pictures for his page", "tol": "exact"},
        {"name": "C7: the stack clear of the shop door", "measure": "the stack's x range against the grocer's shop door zone", "expect": "x 37.096 to 37.504, 0.14 m from the jamb at 37.644", "tol": "+-0.05 m"},
        {"name": "C6: the CC0 model's lettering is not in the base colour", "measure": "the crate colour map at 100 percent", "expect": "no GALLER or STORAGE", "tol": "exact"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The milk crates are a stack of three 408 x 298 x 264 mm plastic crates (the measured box of the CC0 crate on Poly Haven, whose lattice sides and printed storage name are not used) built by script with a 28 mm rim, a 24 mm base rail, ribs and slots, a 66 mm name band carrying only the invented COPPER ROW DAIRY, stacking lugs 9 mm high and a pitch of 264, red, with six empty glass pint bottles in the top crate because the grocer and the tea room took a daily delivery (a Judgement: no float is drawn); "
           "the stack stands against the grocer's window at east x 37.30, 0.14 m clear of its shop door (the first version stood it across the door at x 38.0; the scene's wooden yard crates stay); no 1975 to 1995 crate photograph was reached and the one photograph (2021, oblique) gives form only, so the slots, rim and band are judged.")


def story(T):
    return {
        "no": "4", "title": "Quay Street's milk crates: the exact target", "summary": SUMMARY, "previews_list": "p1 (S2 cropped, the dairy's name and labels masked); no overlay: the photograph is oblique and no ratio could be fitted",
        "rulings": {"ruling_2oct": "no car, skip or pallet; a float is not drawn, only the crates it leaves", "sources_order": "a CC0 crate exists (S1) and was checked first; its mesh and texture are rejected for stated reasons (W1), its measured box is kept; the rest is own work by script",
                    "content": "milk, not drink: a dairy's crate and empty milk bottles only; the data scan finds none of what the rule forbids", "noai": "S1 is CC0 with no NoAI tag; S2 and S3 are CC BY-SA 2.0 photographs used only to look at; nothing is traced",
                    "look": "red plastic, grime and scuffs; one saturated patch of colour in a grey doorway", "night": "the crates read near black"},
        "searched": "What was searched: Poly Haven's model list (521 models, 13 October; the info and files of plastic_crate_01, 02, 03 and wooden_crate_01, 02 read); Geograph's feed for `milk crates`, `crates`, `milk float`, `milk bottles` with each year 1975 to 1996. Wikimedia Commons was not asked.",
        "reuse": [
            ["Poly Haven plastic_crate_01 (CC0)", "a red plastic crate 298 x 408 x 264 with lattice sides, handle cutouts and a printed storage name", "BOX KEPT, mesh and texture REJECTED", "W1: the lattice and the lettering (its base colour reads GALLER STORAGE at 100 percent); the builder may still use it as a size reference"],
            ["Poly Haven plastic_crate_02 and 03", "506 x 406 x 254 and 481 x 265 x 266 crates", "NOT USED", "other sizes"],
            ["vignette-scene.json: wooden_crate_01 twice at the yard mouth (west, x 22.4 and 23.1)", "wooden crates for the yard", "KEPT, unchanged", "a different family; these are the grocer's plastic crates"],
            ["production/research/asset-plan 3 and period-vehicles-and-props", "no milk crate line (the 29 September research note put two kinds of crate under one exclusion)", "READ", "milk is not drink: the 29 September exclusion of milk crates is lifted by this target (a DECISIONS entry); the crates carry milk bottles only"],
            ["git branches (git log --all for milk, crate)", "none", "none to reuse", ""],
        ],
        "axes": "Axes: x along the crate's length (the dairy band faces -y), y across, z up from the ground at the bottom crate's floor. Boxes and cylinders; the self-check measures every number back off the parts.",
        "assembly": [
            "**One crate (408 x 298 x 264)**: a 10 mm floor plate with 36 drain slots (a mask), a base rail 24 high and 4 thick all round, a rim 28 high and 6 thick all round, four corner posts 16 x 16, ribs 14 wide (three inner on each long wall, one centre rib on each end wall) between rail and rim, a solid name band 66 high on each long wall at z 118 to 184, and four stacking lugs 14 x 14 x 9 on the rim's corners. The openings between the ribs are open (slots about 88 wide); the end walls' two openings are the hand holds.",
            "**The stack**: three crates at z 0, 264, 528: each base rail rests on the rim below and the lugs enter the next floor's recesses (the floor plate, 10 thick, has a 14 x 14 x 9 recess under each lug: Judgement). Overall 408 x 298 x 801.",
            "**The empties**: six glass pint bottles standing on the top crate's floor, a body 64 across and 128 high, a neck 28 across and 56 high, in the cells of a 4 x 3 grid at 100 mm, no caps, a faint lip ring (not modelled).",
            "**Edges and fixings**: all outer edges r 2, the rim's top edge r 3, vertical post edges r 4; no fixings (moulded in one piece).",
        ],
        "lettering": ["Dairy: %s (a fictional placeholder until the town mints one): a SEPARATE swappable layer (a normal and colour decal, not mesh), blank in any picture for his page: capitals 18 mm tall, centred on each long wall's band; the second line on the band's lower half 6 mm tall: PROPERTY OF THE DAIRY, then the warning line." % DAIRY, "Bottles: the same name on the shoulder in the same kind of layer, 6 mm capitals."],
        "own_rows": "the crate's box against the CC0 record read live, the stack pitch, the bottles inside the top crate, the dairy's name as a placeholder in its own layer, the stack against the street's pieces and the shopfronts' door zones (the grocer's door), the clear strip",
    }


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
