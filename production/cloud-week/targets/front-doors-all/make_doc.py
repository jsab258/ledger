"""Writes TARGET.md of the front-doors-all target from target.json and td_data.py. Run after make_target.py; run again after self_check.py --write so the
result block carries the live run. /home/user/.bpyenv/bin/python make_doc.py"""
import json
import os
import sys

from td_common import HERE, TARGET_JSON, load_json
import td_data as D

sys.dont_write_bytecode = True

TRADE = {
    "east_parade_bay0": "Mickey's, the minicab office (the quay end of the parade)", "east_parade_bay1": "the fishmonger", "east_parade_bay2": "Rita's, the pawnbroker",
    "east_parade_bay3": "the empty unit to let", "east_parade_bay4": "the launderette", "east_chandler_bay0": "the ship chandler",
    "west_south_bay2": "a cottage of the plain terraces (quay end)", "west_south_bay1": "a cottage of the plain terraces", "west_south_bay0": "a cottage of the plain terraces (by the yard slot)",
    "west_north_bay2": "a shop of the west shop row (by the yard slot)", "west_north_bay1": "a shop of the west shop row", "west_north_bay0": "a shop of the west shop row (north end)",
}


def rnd(o, n=3):
    if isinstance(o, float):
        return round(o, n)
    if isinstance(o, dict):
        return {k: rnd(v, n) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [rnd(v, n) for v in o]
    return o


def md_table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def num(x, n=1):
    if isinstance(x, (int, float)):
        return ("%." + str(n) + "f") % x if abs(x - round(x)) > 1e-9 else "%d" % round(x)
    return str(x)


def kind_section(T, k):
    sp = T["kinds"][k]
    lf = sp["leaf"]
    houses = T["kind_use"].get(k, [])
    L = []
    L.append("### %s: %s" % (k, sp["name"]))
    L.append("")
    L.append("Frame set %s. Houses: %s. Photographs: %s." % (sp["frame_set"], ", ".join(houses) if houses else "none", ", ".join(sp["photographs"]) if sp["photographs"] else "none reached (Hasluck's figures only)"))
    L.append("")
    mem = [(a, lf[a]) for a in ("stile_left", "stile_right", "top_rail", "bottom_rail", "lock_rail", "frieze_rail", "muntin", "bar", "border", "light_h", "light_w", "lipping", "board_w", "board_t") if a in lf]
    L.append("Leaf %s x %s x %s mm, %s, lock on the %s as seen from outside. Members (structural, mm): %s." % (num(lf["w"]), num(lf["h"]), num(lf["t"]), lf["construction"], lf["lock_side"], ", ".join("%s %s" % (a, num(v, 2)) for a, v in mem)))
    if "visible_note" in lf:
        L.append("")
        L.append(lf["visible_note"] + ".")
    L.append("")
    if lf["openings"]:
        rows = []
        for o in lf["openings"]:
            ty = o["type"] + ((", head %s" % o["head"]) if o.get("head") else "") + ((", top corners r %s" % num(o["corner_r"])) if o.get("corner_r") else "") \
                + ((" (%s lower at the outer corner, high toward the %s)" % (num(o["head_rise"]), o["rise_toward"])) if o.get("head") == "raked" else "")
            rows.append((o["id"], ty, num(o["u0"]), num(o["u1"]), num(o["v0"]), num(o["v1"]), o.get("moulding") or o.get("glass") or ""))
            if o.get("inner"):
                iv = o["inner"]
                rows.append(("%s, inner outline" % o["id"], "outline, head %s%s" % (iv["head"], (", springing %s below the crown" % num(iv["springing_below_crown"])) if iv.get("springing_below_crown") else ""),
                             num(iv["u0"]), num(iv["u1"]), num(iv["v0"]), num(iv["v1"]), "a 14 mm cove at this line too"))
        L.append(md_table(["opening", "type", "u0", "u1", "v0", "v1", "moulding or glass"], rows))
        L.append("")
    for fx in sp.get("small_fixings", []):
        L.append("Small fitting that is no furniture variant: %s at u %s, v %s, %s x %s mm, %s proud, dark (%s). %s. What it is not: %s." % (fx["name"], num(fx["u"]), num(fx["v"]), num(fx["size_mm"][0]), num(fx["size_mm"][1]), num(fx["proud_mm"]),
                                                                                                                    ",".join(str(c) for c in fx["srgb"]), fx["src"], fx["what_it_is_not"]))
        L.append("")
    mo = sp["mouldings"]["outside"]
    L.append("Mouldings: %s." % (mo.get("note") or "%s, %s mm on the face (%s)" % (mo["kind"], num(mo.get("width_on_face")), mo.get("src", ""))))
    if mo.get("profile_dh"):
        L.append("")
        L.append("Profile (d across the face from the moulding's outer edge, h above the framing face, mm): " + " ".join("(%s,%s)" % (num(a, 2), num(b, 2)) for a, b in mo["profile_dh"]) + ".")
    if k == "F7":
        L.append("")
        L.append("Boards: edges at u " + ", ".join(num(u, 1) for u in lf["board_edges_u"]) + "; ledges (v) " + "; ".join("%s to %s" % (num(a), num(b)) for a, b in lf["ledges_v"]) + "; nail heads 9 across, 3 proud, one per board at each ledge (" + str(len(lf["nail_heads"]["at"])) + " in all). " + sp["sources"])
    g = sp["glass"]
    L.append("")
    L.append("Glazing: transom %s; leaf %s%s." % (g["transom"], g.get("leaf") or "none", ("; " + g["nets_behind"]) if g.get("nets_behind") else ""))
    if "frame_change" in sp:
        L.append("")
        L.append("Frame change: " + json.dumps(sp["frame_change"]).replace('"', "") + ".")
    if "measured_fractions_of_leaf_height" in sp or "measured_fractions_of_leaf" in sp or "fractions_of_visible_height" in sp or "measured_from_left_edge_mm" in sp:
        key = [x for x in ("measured_fractions_of_leaf_height", "measured_fractions_of_leaf", "fractions_of_visible_height", "measured_from_left_edge_mm") if x in sp][0]
        L.append("")
        L.append("Photograph numbers behind it (%s): %s." % (key, json.dumps(rnd(sp[key])).replace('"', "")))
    L.append("")
    L.append("Part by part against the 3.1 door (door_T1.glb, door_F1.glb):")
    L.append("")
    L.append(md_table(["3.1 part", "status", "why"], sp["parts_vs_3_1"]))
    L.append("")
    return "\n".join(L)


def build(T):
    S = T["self_check"]
    L = []
    L.append(T["summary"] + " Self-check: " + (S.get("result") or "not run") + ".")
    L.append("")
    L.append("# Front doors for every house kind: the target (cloud week 42, unit 9)")
    L.append("")
    L.append("Files in this folder: `TARGET.md` (this), `target.json` (the same numbers: frame sets, 10 kinds, the furniture, paints, wear, the street's house table, the gate and %d checks, with the self-check result), `target_drawing.py` (draws target.json alone: an elevation of each kind in the 3.1 frame, the sections, the street's rows; `OUT_DIR [--json F] [--overlay KIND PHOTO OUT BOX]`), `self_check.py` (`--live --previews --photos DIR --write`), the makers (`td_data.py`, `td_kinds.py`, `td_furn.py`, `td_checks.py`, `td_sites.py`, `td_photos.py`, `make_target.py`, `make_doc.py`, `make_previews.py`) and `pages_read.json`. Run with `/home/user/.bpyenv/bin/python`. Previews: `production/previews/cloud-week/refs/front-doors-all/`." % len(T["checks"]))
    L.append("")
    L.append("Units and axes as the 3.1 target: millimetres; frame x across the opening from the left reveal, z up from the top of the threshold; leaf u across from the leaf's left edge seen from outside, v up from its bottom. The leaf laps behind each stop and behind the transom by 20.4 mm, so a photograph's visible face is the leaf less that lap: `u_structural = 20.4 + fraction x visible width`, `v = fraction x visible height` (visible T 772 x 1927.6, F 797.2 x 1960.6). Kinds of number: Read (printed), Scaled, Photo (with its box and error), Derived, Judgement.")
    L.append("")
    L.append("## 1. What was asked, and what is reused")
    L.append("")
    L.append("Jafar, 12 October: \"Front doors for every house kind, from the 3.1 door with its bell push fixed, with door furniture variants.\" The 3.1 door is built and passed (try 2, one narrow point): `production/cloud-week/targets/front-door/` (target and photographs), `production/cloud-week/kit/door/` (build_door.py, departures.py, check_door.py, views, NOTES.md, the reviews), `production/assets/cloud-week/door/door_T1.glb` and `door_F1.glb`, HANDOVER.md row 3.1. Every number taken from 3.1 here is its target.json with `departures.py` applied (the build's moulding widths 46 and 43, the collar standing 5.0 proud, the vertical keyway): the self-check re-reads both and fails on a difference.")
    L.append("")
    L.append("The handover's fix is the first line of the work: **delete the parts `iron_bellpush_bezel` and `iron_bellpush_button` from door_T1 (rebuild without them) so a plain dark oblong remains.** The two-part push read as a modern video doorbell (the 3.1 close review). The only bell push in this target is BL1, one part, 22 x 72.6 x 3 proud, square-cornered (radius at most 1), a 14 x 2 groove 1 deep a little below its middle (the darker band P1 shows), no bezel, no button, no ring, no bright element; it is on T1 only. Checks BP-form, BP-none-elsewhere, BP-no-modern and BP-houses hold it, and the negative controls build a push with a bezel, a push on F1 and a brass push to prove they fail.")
    L.append("")
    L.append("The new kinds are made from 3.1's script and method: the frame sets T (the cottage's brick opening, cambered head, transom 65, step) and F (the flat's side slot, flat head at 2400, transom 102, jambs showing 49) are 3.1's unchanged (every kind, F6 included, stands in one of them: the stops in front of the leaf, an inward-opening door); the leaf is rebuilt per kind from the same members (stiles 114.3, rails, 1.6 mm margins, panels floating in their grooves where there are panels); the fittings are 3.1's parts with new places. Section 5 says part by part, kind by kind, what is kept, changed, removed or added and why.")
    L.append("")
    L.append("## 2. Sources")
    L.append("")
    rows = []
    for pid, ph in T["sources"]["photographs"].items():
        rows.append((pid, "%s, %s" % (ph["title"], ph.get("url") or ph.get("src")), "13 Oct 2026 (%s)" % ph.get("reached_by_me", ph.get("read_by_me", "page opened, file measured")), "%s, %s" % (ph["author"], ph["licence"]), ph["taken"], ph.get("shows", ""), ph.get("used_for", "")))
    L.append(md_table(["id", "photograph and page", "read", "author, licence", "taken", "shows", "used for"], rows))
    L.append("")
    L.append("All photographs are references for measuring only: never placed in the game, never traced into a texture, never fed to an image model. No NoAI source is used. Each Geograph page was opened by this writer and its title, author, taken date and CC BY-SA 2.0 read there (`pages_read.json`; `self_check.py --live` reads them again). D5 is a Wikimedia Commons file (the Tower Block Archive of Edinburgh College of Art, uploaded with the University of Edinburgh), page read through the Commons API: date 1987, licence CC BY 4.0, author Miles Glendinning; the 1920 px copy served by Commons (`?width=1920`) was measured, the original is 4000 x 2646. **D5 is an indoor landing door** (the file's own description: \"View of hallway and door inside one of Hazlehead I blocks\"; the frame shows a carpeted landing, a plant and a floor number): it is used for the flush face and the places of the plate, lever, lock and spyhole only, never for a street frame, a leaf width, stops or a transom. D9's door is 6 px wide, so \"half-glazed\" is a best reading; only its lower panel's turquoise is used. D10 is a later photograph (2014) of a cast-iron fixture left in place since the 19th century; P1 (2012) and P2 (2024) are 3.1's, their previews only (the lab's pages could not be reached then).")
    L.append("")
    L.append("Books (public domain by age): Hasluck, Cassell's Carpentry and Joinery (1907), pp.312-317, Figs. 1015-1039 (ledged and braced doors), read as the OCR text from archive.org, page images not opened; Ellis (1902) and Riley (1905) only through the 3.1 target.")
    L.append("")
    L.append("Repository files read: canon.md and RULINGS.md (section 11), `production/specs/vignette-scene.json`, `production/specs/vignette-pieces.json`, `production/assets/street/quay-street.json`, `tools/art-recipes/terrace-front.py` (the street's doors, derived live by `td_sites.py`), `production/cloud-week/targets/SCENE-SLOTS.md`, the house-windows target (which houses were modernised), the wear target and `production/cloud-week/2d/wear/NOTES.md`, the Hook sheet (`production/reference/hook-sheet.png`: dark doors in white surrounds, a blue-grey shop door, a cream house; no household door is large enough in it to measure).")
    L.append("")
    L.append("**Dating.** Photographs D1 to D9 were taken between 1975 and 1994, as stated on their pages; all show the period object. D3's door is a 1930s type kept in 1994; D4 is black and white; D2, D6 to D9 are slides whose colour shifts, so no paint value is taken from a photograph except as a hue family (section 8).")
    L.append("")
    L.append("**Unreached or not usable.** Geograph's search page refuses the session (its syndicator feed does not); Commons' API answered 429 repeatedly and its text search returned nothing usable for doors, so only the Hazlehead file and one category listing were used; no photograph of a knocker, bell pull, wired glass, frosted door glass, black iron plate or a ledged service door of these streets was reached. A search summary is a lead, never a number.")
    L.append("")
    L.append("## 3. The house kinds: every household door of the street")
    L.append("")
    L.append("From `tools/art-recipes/terrace-front.py plan_street` (the drawn street; `td_sites.py` re-derives it) with `vignette-scene.json` and `vignette-pieces.json`. The files give each household door a leaf 0.838 x 1.981 m (SCENE-SLOTS: the imperial 2 ft 9 in x 6 ft 6 in; the parade's drawn leaf is 766 between 36 mm casings, the cottages' 678 between 80 mm casings; head casing to 2.117 above the footway in the parade, 2.161 in the cottages; the cottages stand on a stone step 998 x 352.5 x 70 mm; the stand-in letter plate is 250 x 40 at 1.0 m). The scene's coarse side doors (`east_parade_sidedoor0..5`, `west_south_door0..2`, `west_north_sidedoor0..2`, `east_chandler_sidedoor0`) have the same sizes; the drawn street omits east_parade_bay5's side door (the grocer's flat is reached from the rear yard).")
    L.append("")
    L.append("**The house kinds.** (1) The plain terraces across from Mickey's: three cottages whose doors open onto the footway over a stone step (frame set T). (2) The flats' side doors beside the shops: five in the parade (bay 2 is the shopfront kit's own door with a fanlight), the chandler's, and three in the west shop row, which the drawn street makes one storey (frame set F). (3) The modernised houses: those the windows target gave replacement windows (east_parade bays 2 and 4, the chandler's flat, the cottage west_south bay 1); they may take a modern door (T3, F5, F6). (4) Council-owned: none; no file names a council house on Quay Street, so the council-style flush door F6 goes on a modernised flat. (5) The yard slot between the west blocks (x 21 to 24) is a gap in the data with no door piece; any gate there belongs to the gate family. (6) The hill's 12 doors (backdrop rows e, w, x, seen at 44 m and more) take kind and paint only.")
    L.append("")
    rows = []
    for h in T["street"]["houses"]:
        si = h["stand_in"]
        fu = h["furniture"]
        short = {"letter_plate": "plate", "handle": "handle", "latch": "latch", "keyhole": "keyhole", "knocker": "knocker", "bell": "bell", "number": "number", "scraper": "scraper"}
        flist = ", ".join("%s %s" % (short[s], d["variant"]) for s, d in fu.items() if d["variant"][-1] != "0")
        rows.append((h["house"], "%s %.2f" % (h["side"], h["x_centre_m"]), TRADE[h["house"]], "%s%s%s" % (num(si["opening_w_mm"]), (", leaf %s x %s" % (num(si["leaf_w_mm"]), num(si["leaf_h_mm"]))) if si["leaf_w_mm"] else ", the kit's", ", step" if si["step"] else ""),
                     h["kind"], h["frame_set"], h["paint"], h["condition"], flist, "modernised" if h["windows_modernised"] else ""))
    L.append(md_table(["house", "side, door centre x (m)", "trade", "the files' opening (mm)", "kind", "frame", "paint", "condition", "fittings", "windows"], rows))
    L.append("")
    L.append("Why each house has its kind, paint and fittings:")
    L.append("")
    for h in T["street"]["houses"]:
        L.append("- %s: %s." % (h["house"], h["why"]))
    L.append("")
    L.append("**The street's order and the neighbours rule.** East side, quay end to chandler: " + ", ".join(T["street"]["order"]["east"]) + ". West side, quay end to north: " + ", ".join(T["street"]["order"]["west"]) + ". Neighbours are consecutive doors on a side (east_parade_bay5 has none, so bay 4 and the chandler's are neighbours; the yard slot has none, so west_south bay 0 and west_north bay 2 are). Every neighbouring pair differs in kind, in paint, and in at least 2 of the slots letter plate, handle, latch, number (checks AD-adjacent-east and -west); every pair facing each other within 4.6 m across the street differs in paint class (AD-opposite): " + "; ".join("%s / %s (%.2f m)" % tuple(p) for p in T["street"]["opposite_pairs_within_4_6_m"]) + ". " + T["mix_rule"]["text"])
    L.append("")
    L.append("**The hill's 12 doors.** " + T["street"]["backdrop"]["rule"] + " Table: " + "; ".join("%s %s %s" % (d["id"].replace("backdrop_rise_approach_", ""), d["kind"], d["paint"]) for d in T["street"]["backdrop"]["doors"]) + ".")
    L.append("")
    L.append("## 4. The reading of the photographs, element by element")
    L.append("")
    L.append("What the photographs show on a door, and where it is in this target: panel layout and counts (section 5, per kind); mouldings and profiles (T1 F1 F2 the 3.1 bolection at 46 and 43; F3 a stuck ovolo; T3 an embossed step; the rest none); glazing (plain, reeded, leaded; section 5); the fanlight (a plain dark light over D2's doors and D4's; a leaded light over D3's; a reeded light on F6, Judgement; the T and F frames' transoms carry them); the frame and its stops (frame sets T and F); the number (forms NM1, NM3, NM6; the digits are the town's); furniture (section 6); paint and wear (sections 7 and 8). Hoods over the doors, arched recesses and painted reveals (D1, D6, D7) belong to the wall and are listed for the wall kit.")
    L.append("")
    L.append("**The brief's door types, and where each is.** Four-panel: T1, F1 (3.1). Six-panel: F2. Two long panels (a 1930s door, D1): F3. Half-glazed: F4 (three long lights over a low rail, D2) and T2 (four stacked lights, D3, D1); half-glazed with a small light: T3 (a small flat-topped light in a moulded panel, D4) and F5 (a tall slit light, D2, D4). A council replacement flush door of the 1970s or 1980s: F6 (the fittings' places from D5, an indoor door; the hue from D9; a flush leaf in a white street frame as D4's middle door). A ledged door to a yard or a service passage: F7 (Hasluck only). A fanlight: every door has one, the frame sets' transom light (plain dark over D2's and D4's doors, leaded over D3's, reeded on F6 as Judgement); a door with no fanlight is not offered, because every door read (D1 to D4, P1, P2) has a light or a panel above its leaf. Glazing: plain (T2, F4, F5, T3, every transom but two), leaded diamond (T2's fanlight), reeded (F6's transom); frosted and wired are listed and placed nowhere. The frame and its stops: frame sets T and F as 3.1 (rebate 22 x 53, stop 74 deep, a 5 x 2.5 stop bead on F), every kind in one of them. Letter plates, knockers, knobs and levers, the rim night latch with its escutcheon (the collar), the bell, house numbers, the boot scraper: section 6.")
    L.append("")
    L.append("## 5. The doors, kind by kind")
    L.append("")
    L.append("**Covering every opening.** " + T["covering_every_opening"])
    L.append("")
    for k in T["kinds"]:
        L.append(kind_section(T, k))
    L.append("## 6. Door furniture variants")
    L.append("")
    L.append("Every variant with its size, place by kind, material, colour and source. Positions are the fitting's centre in the leaf frame (u, v mm). No real maker's name or mark on any fitting: the lock is a rim night latch.")
    L.append("")
    for slot, cat in T["furniture"].items():
        L.append("**%s**" % slot.replace("_", " "))
        L.append("")
        rows = []
        for vid, v in cat.items():
            size = v.get("outer") or v.get("size") or v.get("lever") or ([v.get("collar"), v.get("collar")] if v.get("collar") else None) or v.get("digit") or v.get("dia") or v.get("plate") or ""
            place = "; ".join("%s: u %s, v %s" % (k2, (num(p.get("u")) if isinstance(p.get("u"), (int, float)) else p.get("u", "")), num(p.get("v")) if isinstance(p.get("v"), (int, float)) else p.get("stacked", p.get("on", p.get("z_range", "")))) for k2, p in v.get("place", {}).items()) if v.get("place") else ("not placed" if v.get("name") != "none" else "")
            mat = "%s (%s)" % (v.get("material", ""), ",".join(str(c) for c in v["srgb"])) if v.get("srgb") else v.get("material", "")
            rows.append((vid, v["name"] + (" [NOT OFFERED]" if v.get("offered") is False else ""), size, place, mat, v.get("src", v.get("note", ""))))
        L.append(md_table(["id", "variant", "size (mm)", "place", "material (sRGB)", "source"], rows))
        L.append("")
    L.append("Bell push BL1 in full: " + json.dumps(T["furniture"]["bell"]["BL1"]).replace('"', "") + ".")
    L.append("")
    L.append("Glass: " + "; ".join("%s: %s" % (k, json.dumps({a: b for a, b in v.items() if a != "name"}).replace('"', "")) for k, v in T["glass"].items()) + ".")
    L.append("")
    L.append("## 7. Paint and condition")
    L.append("")
    L.append("**Door colours** (sRGB as the engine takes them; plain names; gloss paint roughness 0.35 kept, 0.55 tired, 0.65 neglected on the weather side low down; metal 0). Class is used by the facing rule.")
    L.append("")
    used = {}
    for h in T["street"]["houses"]:
        used.setdefault(h["paint"], []).append(h["house"].replace("_bay", " bay "))
    L.append(md_table(["id", "name", "sRGB", "class", "on", "source"], [(p["id"], p["name"], ",".join(str(c) for c in p["srgb"]), p["class"], "; ".join(used.get(p["id"], [])) or "no house today", p["src"]) for p in T["paints"]]))
    L.append("")
    L.append("**Frames:** " + "; ".join("%s %s (%s)" % (f["id"], ",".join(str(c) for c in f["srgb"]), f["src"]) for f in T["frame_colours"]) + ". Cream is dropped (3.1 allowed it at 0.3): see section 10.")
    L.append("")
    L.append("**Colour boxes measured** (median RGB of a box inside the door leaf, film slides of 1975 to 1994, so a hue family and never a target value): " + "; ".join("%s %s median %s (%s)" % (k, v["box"], v["median_rgb"], v["note"]) for k, v in T["sources"]["colour_boxes"].items()) + ". D7's green is a painted brick reveal, not a door, and is not used.")
    L.append("")
    L.append("**Wear by condition** (kept, tired, neglected):")
    L.append("")
    cn = T["conditions"]
    rows = [(a, cn["kept"][a], cn["tired"][a], cn["neglected"][a]) for a in ("paint_flake_share", "paint_fade", "crazing", "chips", "bottom_rail", "kick_marks", "polish", "frame", "roughness")]
    L.append(md_table(["mark", "kept", "tired", "neglected"], rows))
    L.append("")
    L.append("Houses: " + "; ".join("%s %s" % (h["house"].replace("_bay", " bay "), h["condition"]) for h in T["street"]["houses"]) + ".")
    L.append("")
    L.append("**The wear layer of unit 4.5** (`production/cloud-week/2d/wear/`, its target `production/cloud-week/targets/wear/target.json`) is named for the PC and covers these marks by its kinds: " + ", ".join(T["wear_kinds_used"]) + " (paint_flake on door bottoms and arrises at the shares above, handle_wear's grease halo p50 0.17 m round plates and handles, wall_foot_splash for the dark splash band to 0.24 m, 1.2 x higher within 0.6 m of a door, iron_wear on the boot scraper, paint_fade on the leaf). The check WR-wear-target and `self_check.py --live` compare the shares with that target's numbers. **Not covered by the layer, owed to it or to the door's build:** " + "; ".join(T["wear_not_covered"]) + ".")
    L.append("")
    L.append("## 8. Photograph measurements, with their boxes")
    L.append("")
    L.append("Every row a reviewer can reproduce: the box is [x0, y0, x1, y1] in the pixels of the file named in section 2 (Geograph's largest size, or Commons' 1920 px copy for D5). The leaf boxes are the visible face of the door as the gate will measure it: the white or painted leaf only, no neighbouring stone, brick or frame inside the box (a box that held brick gave the numbers of the windows target's first draft). Scales are the visible face's height over the box's height.")
    L.append("")
    rows = []
    for key, m in T["sources"]["measurements"].items():
        rows.append((key, m["photo"], json.dumps({a: b for a, b in m.items() if a not in ("photo", "what", "error_px")}).replace('"', ""), m.get("error_px", ""), m["what"]))
    L.append(md_table(["record", "photo", "boxes and rows (px)", "error (px)", "what"], rows))
    L.append("")
    L.append("The photograph rows of the self-check (group photo) compare each kind's numbers with these records: T2's four lights and rails against D3 and D1, T3's panels, light and plate against D4, F5's slit, plate and lever against D2, F4's three lights against D2, F6's plate, lever, lock and spyhole against D5 (an indoor door: places only), the lozenge pattern and the stiles' white against D3's re-measured leaf, LP5's height against D1 and D4. Each of the six PH records of the checks list carries those fractions as its expected values with a tolerance, and the self-check recomputes both sides (the recorded boxes, the kind's own drawn parts). The live rows then re-measure the boxes on the pixels: the small light's flat head and the seven outline rows (D4), the lever's mark on the door (D4), the slit's dark run and the leaf's foot above the sill (D2), the plate's light run and the lock's dark mark (D5), the leaf's own edges row by row, its top, its foot, the stiles' white and the fanlight's plain pane against its lozenge band (D3), and the colour medians.")
    L.append("")
    L.append("## 9. The gate in the cloud")
    L.append("")
    L.append("The same views and checks as 3.1 (`kit/door/views_T1.json` for the cottage kinds, `views_F1.json` for the flat kinds): front (orthographic), street (3.5 m out, 2 m along, eye 1.6 m), close, low (7 m along, 2.7 m out), front_head, front_foot, close_plate, with the close and close_plate cameras lowered or raised to each kind's own fittings (%s) and a close_foot view for a kind with a low plate. Pass rule as 3.1: front view by layer IoU >= 0.97, outline p95 <= 2 mm, worst <= 6 mm; sections the same; profiles p95 <= 1.5, worst <= 3. One fresh reviewer per view, never bundled, its last good picture beside; the photographs of each kind beside the render (below). Street views: %s. Night light is the game's lantern colour, linear (1.0, 0.25, 0.0)." % ("; ".join("%s close at %.2f m" % (k, [v for v in vs if v["name"] == "close"][0]["target"][2]) for k, vs in T["gate"]["views"].items()), "; ".join("%s (%s)" % (v["name"], v.get("from", "")) for v in T["gate"]["street_views"])))
    L.append("")
    L.append("No model from a library is placed by this target (the doors are built by script from numbers), so there are no base-colour maps to read for lettering; the previews and the gate's renders carry no firm's name, house number or vehicle plate, and \"rim night latch\" is the only name for the lock anywhere in the text, data or pictures.")
    L.append("")
    L.append("Photograph pairs for the reviewer: " + "; ".join("%s against %s: %s" % (p["kind"], ", ".join(p["photographs"]) or "no photograph", p["reads"]) for p in T["gate"]["photograph_pairs"]) + ".")
    L.append("")
    L.append("**The checks** (`target.json` checks, %d records, each with name, what to measure, expected value, tolerance and source):" % len(T["checks"]))
    L.append("")
    grp = {}
    for c in T["checks"]:
        grp.setdefault(c["group"], []).append(c)
    names = {"PL": "panel layout per kind (counts, every opening's bounds to 3 mm, members to 2 mm, framing)", "CV": "nothing shows through, in elevation and from 60 degrees, per kind; F7's joints", "FU": "furniture size and place per kind and variant (8 mm)",
             "BP": "the bell push: one plain part, only on T1, no two-part modern push on any variant", "AD": "the street: neighbours, facing doors, every house, frame sets, every kind used, the hill", "PN": "paint palette, white frames, at most 3 light doors, the 3.1 colours' values",
             "GL": "glass types and values", "WR": "wear numbers equal the wear target's", "PH": "each kind against its photograph", "NM": "no maker's name, the lantern colour, the lines for Jafar", "GA": "the gate's views per kind"}
    L.append(md_table(["group", "count", "what", "examples"], [(g, len(cs), names[g], "; ".join(c["id"] for c in cs[:4])) for g, cs in sorted(grp.items())]))
    L.append("")
    L.append("**For the builder.** " + " ".join("(%d) %s" % (i, t) for i, t in enumerate(T["for_builder"], 1)))
    L.append("")
    L.append("## 10. Photographs win: where a photograph and the scene, a book or a ruling differ")
    L.append("")
    L.append(md_table(["id", "what", "scene or book", "photograph", "chosen"], [(d["id"], d["what"], d["scene_or_book"], d["photograph"], d["chosen"]) for d in T["disagreements_photographs_win"]]))
    L.append("")
    L.append("Where a photograph disagrees with a ruling of Jafar's the ruling stands and the disagreement goes to him on his page (section 12). The Hull streets (D6 to D8) show window frames and surrounds painted in blue, red and yellow; his ruling of 3 October is windows with white frames, so every frame here is white or grimed white and the finding is owed line 2. \"Photographs win\" settles books and the scene's stand-ins against photographs; it does not settle a tally against his word.")
    L.append("")
    L.append("## 11. Rulings checked")
    L.append("")
    L.append(md_table(["ruling", "how this target keeps it"], [(r["ruling"], r["applies"]) for r in T["rulings_checked"]]))
    L.append("")
    L.append("## 12. Owed to Jafar's page (one line each, recommendation first)")
    L.append("")
    for o in T["owed_for_jafar"]:
        L.append("- " + o)
    L.append("")
    L.append("## 13. Self-check")
    L.append("")
    L.append("`python self_check.py [--live] [--photos DIR] [--previews] [--write]` writes its result into target.json under self_check. Result recorded: **%s** (options: %s; run %s)." % (S.get("result"), S.get("options"), S.get("run")))
    L.append("")
    L.append("Groups: 31 (3.1's numbers as built, the handover's fix), meta (each photograph's title, author, licence, date and period note; every box inside its image), photo (the fractions above), street (the 12 doors, kinds, paints, neighbours, facing doors, the hill, no knocker, no council house), geom (the drawing: openings inside the leaf and not overlapping, fittings on the leaf, nothing shows through in elevation or at 60 degrees, the leaf's lap computed from the stop edges and the leaf's edges at 60 degrees in plan, every leaf behind its stops, the margins of each kind's leaf in its frame, the lead came's uprights and crossings counted on the drawing, the numerals inside the top rail, the boards and nails, the bars, the sections), checks (every record of the list, and that every opening and every placed fitting has one), wear (the numbers, and live against the wear target), text (no maker's name, no dash, the lantern colour, owed lines), gate, live (the street re-derived from terrace-front.py and the windows target, the photographs fetched and measured again on their pixels, the pages read again), previews (sizes, flat grey masks, credits).")
    L.append("")
    L.append("**Negative controls** (wrong copies of the target, each run offline, each must make some row fail): " + "; ".join(c["name"] for c in S.get("controls", [])) + ". Counts are printed with the options named, offline and with --live (the controls always run offline, since the live rows read the world and not the copy).")
    L.append("")
    L.append("**How to read it honestly.** The photograph fractions that are independent of the numbers drawn from them are T2's bottom rail and bars (3.1's frame, not the photograph, gives 205 and 30), D1's lights against T2 (a second photograph, oblique), D4's panels and plates, D2's slit and plate (the live rows measure them on pixels), and the stiles' white and the fanlight's three parts (D3, re-measured on the leaf's own face; the stiles 94.0 and 69.0 and the fanlight pattern were set from the review's re-measure, then compared with the boxes). T2's lights, T3's panels, F5's slit and F6's fittings were fitted to the same photographs, so their near-zero differences are by construction; the live edge rows are what test them, and the first draft's wrong boxes (D3's, D2's, D4's) are among the live negative controls. F5's slit, plate and lever and T3's lever are the review's numbers, 5 to 12 mm from what the recorded boxes give (inside the stated error), and the photograph rows hold that difference. Everything not measured is marked Judgement, and section 14 lists it.")
    L.append("")
    L.append("## 14. Could not settle")
    L.append("")
    for i, c in enumerate(T["could_not_settle"], 1):
        L.append("%d. %s" % (i, c))
    L.append("")
    L.append("## 15. Credits for the previews in `production/previews/cloud-week/refs/front-doors-all/`")
    L.append("")
    L.append("Reduced crops of the doors only (at most 1200 px, under 300 KB), for measuring and for the reviewers, never placed in the game. Masked flat grey by script and recorded in `preview_masks.json`: a pole-mounted board and an oval plaque (D2), small numerals (D3), a small label (D5), a painted numeral (D6), a board on a fence (D8). No people, no child, no drink or betting, no firm's name, no house number and no vehicle plate in any preview; each was looked at in full.")
    L.append("")
    cred = []
    for pid, ph in T["sources"]["photographs"].items():
        if ph.get("preview") and not ph["preview"].startswith("production"):
            cred.append((ph["preview"], "%s, %s, %s, taken %s (%s); cropped, reduced, masked as above" % (ph["author"], ph["licence"], ph.get("url", ""), ph["taken"], ph["title"])))
    over = {"d3-levenshulme-ratcliffe-street-1994-target-on-photo.jpg": "T2", "d2-railway-street-1987-target-on-photo.jpg": "F5", "d5-aberdeen-hazlehead-1987-target-on-photo.jpg": "F6"}
    for f, k in over.items():
        cred.append((f, "the target's drawing of %s (own work) laid on the photograph it was measured from (%s), %s; yellow the visible face, red the openings, orange the mouldings, green the fittings" % (k, f.split("-")[0].upper(),
                  "fitted on height and width because D5 is an indoor door with a narrower leaf and only the fittings' places are taken from it" if k == "F6" else "the scale fitted on the visible height only")))
    cred.append(("target-ten-door-kinds-elevations.jpg", "the target's own drawing of the ten kinds (own work), each in its house's first paint"))
    cred.append(("target-street-rows-east-and-west.jpg", "the target's own drawing of the street's two rows of doors in street order (own work)"))
    L.append(md_table(["file", "credit"], cred))
    L.append("")
    return "\n".join(L)


def main():
    T = load_json(TARGET_JSON)
    txt = build(T)
    with open(os.path.join(HERE, "TARGET.md"), "w") as f:
        f.write(txt)
    print("wrote TARGET.md", len(txt))


if __name__ == "__main__":
    main()
