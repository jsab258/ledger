"""bus-stop: the self-check. python self_check.py [--live] [--previews] [--photos DIR] [--no-controls]"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_family as SF

V = "BS1"


def times(spec):
    if not spec:
        return []
    t = (spec["first"] // 100) * 60 + spec["first"] % 100
    end = (spec["last"] // 100) * 60 + spec["last"] % 100
    out = []
    while t <= end:
        out.append(t)
        t += spec["every"]
    return out


def atlas_names():
    a = json.load(open(os.path.join(L.REPO, "production", "art", "atlas-01", "data", "atlas.json")))
    names = set()
    for r in a["routes"]:
        names.add(re.sub(r"\s*\(.*?\)", "", r["name"]).strip().lower())
    for l in a["landmarks"]:
        names.add(l["name"].strip().lower())
    for p in a["working_town"]["places"]:
        names.add(p["name"].strip().lower())
    return names


def card_lines(T):
    n = 3  # operator, stop, rule line
    for s in T["text"]["services"]:
        n += 1 + len(s["stops"]) + 3
    return n


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    names = atlas_names()
    tx = T["text"]
    for s in tx["services"]:
        for key in ("mf", "sat", "sun"):
            sp = s[key]
            if not sp:
                continue
            ts = times(sp)
            ok = ts[-1] == (sp["last"] // 100) * 60 + sp["last"] % 100 and len(ts) >= 2 and ts[0] >= 6 * 60 and ts[-1] <= 23 * 60
            rows.add("timetable", "timetable/service %s %s: first plus whole intervals reaches the last" % (s["no"], key), ok, "%d departures from %d to %d min, every %d" % (len(ts), ts[0], ts[-1], sp["every"]))
        offs = [m for n, m in s["stops"]]
        rows.add("timetable", "timetable/service %s: minutes from the stop rise" % s["no"], offs[0] == 0 and all(b > a for a, b in zip(offs, offs[1:])), str(offs))
        bad = [n for n, m in s["stops"][1:] if n.strip().lower() not in names]
        rows.add("timetable", "timetable/service %s: every stop is a road or place on the town's map" % s["no"], not bad, "not on the map: %s" % bad)
    rows.add("timetable", "timetable/the first stop is this stop", all(s["stops"][0][0].lower() == tx["stop_name"].lower().replace(" (top)", " (top)") for s in tx["services"]), tx["stop_name"])
    rows.add("timetable", "timetable/services numbered differently", len({s["no"] for s in tx["services"]}) == len(tx["services"]), "")
    # the card's capacity and place
    c = tx["card"]
    need = card_lines(T) * c["line_pitch_mm"] + c["head_mm"] * 2 + len(tx["services"]) * c["service_no_mm"]
    rows.at_most("card", "card/its lines fit the card's height", need, c["h"] - 2 * c["margin"])
    cl, ch = ps.part_bbox("case_card")
    gl, gh = ps.part_bbox("case_glass")
    rows.add("card", "card/the card lies inside the window", cl[0] >= gl[0] and ch[0] <= gh[0] and cl[2] >= gl[2] and ch[2] <= gh[2], "card %s to %s window %s to %s" % (cl, ch, gl, gh))
    rows.near("card", "card/the card's size is the text's", ch[0] - cl[0], c["w"], 0.6)
    rows.near("card", "card/the card's height is the text's", ch[2] - cl[2], c["h"], 0.6)
    # placement
    pl = T["placement"]
    hc = json.load(open(os.path.join(L.REPO, "production", "specs", "hook-cast.json")))["places"]["bus_stop"]
    rows.near("placement", "placement/x is the cast's bus stop", pl["x_m"], hc["x_m"], 0.001, unit="m")
    rows.add("placement", "placement/the waiting spot lies behind the pole on the pavement", pl["frontage_z_m"] < pl["z_wait_m"] < pl["z_m"] and abs(pl["z_wait_m"] - hc["z_m"]) < 0.001, "")
    clear = pl["footway_mm"] - pl["set_back_mm"] - 38.0
    rows.at_least("placement", "placement/footway clear behind the pole", clear, pl["min_clear_behind_mm"])
    rows.near("placement", "placement/z is the kerb's back edge less the set-back", abs(pl["z_m"] - pl["kerb_back_z_m"]) * 1000.0, pl["set_back_mm"], 0.5)
    lb = json.load(open(os.path.join(HERE, "..", "..", pl["bin_slot"]["file"], "target.json")))
    b3 = [b for b in lb["placements"]["bins"] if b["id"] == pl["bin_slot"]["slot"]][0]
    d = ((pl["x_m"] - b3["axis_x_m"]) ** 2 + (pl["z_m"] - b3["axis_z_m"]) ** 2) ** 0.5
    rows.at_most("placement", "placement/the bin is within 3 m of the pole", d, pl["bin_slot"]["max_m"], unit="m")
    # the case and the pole
    pb = ps.part_bbox("pole_foot")
    cb = ps.part_bbox("case_bar_top")
    rows.add("detail", "detail/the case is clamped to the white length of the pole", ps.part_bbox("pole_white")[0][2] < cb[0][2] and ps.part_bbox("pole_white")[1][2] > ps.part_bbox("case_bar_top")[1][2], "")
    fb = ps.part_bbox("flag_plate")
    rows.add("detail", "detail/the flag is on the black upper length", fb[0][2] >= ps.part_bbox("pole_upper")[0][2] - 1 and fb[1][2] <= ps.part_bbox("pole_upper")[1][2] + 1, "")
    rows.add("detail", "detail/the flag and the case face the same way (-y)", fb[0][1] < pb[0][1] and cb[0][1] < pb[0][1], "")
    rows.add("detail", "detail/the flag text is two lines BUS and STOP", T["text"]["flag_text"] == ["BUS", "STOP"], str(T["text"]["flag_text"]))
    rows.add("detail", "detail/BS2 has no case", not any(n.startswith("case_") for n in K._ps_cache(T["variants"]["BS2"]["parts"]).names), "")
    rows.add("detail", "detail/the card has no logo", "no operator logo" in T["text"]["no_logo"], "")
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    # the earlier script's flag and case really are different from this target
    scr = os.path.join(L.REPO, "tools", "meshgen", "blender", "clutter", "bus_stop.py")
    txt = open(scr).read()
    m = re.search(r"FW, FH, FT = ([0-9.]+), ([0-9.]+), ([0-9.]+)", txt)
    old_w, old_h = float(m.group(1)) * 1000, float(m.group(2)) * 1000
    rows.add("reuse", "reuse/the old script's flag (450 x 375) is not the target's plate", abs(old_w - (fb[1][0] - fb[0][0])) > 100, "old %.0f x %.0f, target %.0f x %.0f" % (old_w, old_h, fb[1][0] - fb[0][0], fb[1][2] - fb[0][2]))
    mp = re.search(r"radius=0\.038, depth=([0-9.]+)", txt)
    rows.add("reuse", "reuse/the old pole (76 mm, 3.0 m) is kept", mp is not None and abs(float(mp.group(1)) * 1000 - 3000) < 1 and abs(pb[1][0] - pb[0][0] - 76) < 1, "")


def extra_controls(T):
    def svc(t, i, key, field, val):
        t["text"]["services"][i][key][field] = val
    C = [
        ("timetable: the last time not on the interval", lambda t: svc(t, 0, "mf", "last", 1755), "timetable/service 4 mf"),
        ("timetable: the stops' minutes not rising", lambda t: t["text"]["services"][1]["stops"].__setitem__(2, ["Retort Works", 3]), "timetable/service 9: minutes from the stop rise"),
        ("timetable: a stop that is not on the town's map", lambda t: t["text"]["services"][2]["stops"].__setitem__(3, ["Leeds Station", 18]), "timetable/service 12: every stop is a road or place"),
        ("timetable: too many services for the card", lambda t: t["text"]["services"].extend([dict(t["text"]["services"][0], no=str(20 + i)) for i in range(6)]), "card/its lines fit"),
        ("card: the card made wider than the window", lambda t: [p.__setitem__("s", [260.0, p["s"][1], p["s"][2]]) for p in t["variants"][V]["parts"] if p["id"] == "case_card"], "card/the card lies inside the window"),
        ("placement: the stop moved to x 30", lambda t: t["placement"].__setitem__("x_m", 30.0), "placement/x is the cast's bus stop"),
        ("placement: the pole 1.2 m behind the kerb", lambda t: (t["placement"].__setitem__("set_back_mm", 1500.0), t["placement"].__setitem__("z_m", -4.625)), "placement/footway clear behind the pole"),
        ("placement: the bin 8 m away", lambda t: t["placement"]["bin_slot"].__setitem__("max_m", 1.0), "placement/the bin is within 3 m"),
        ("detail: the flag text changed", lambda t: t["text"].__setitem__("flag_text", ["BUS", "STOP", "HERE"]), "detail/the flag text"),
        ("detail: a case part added to BS2", lambda t: t["variants"]["BS2"]["parts"].append({"id": "case_bar_x", "type": "box", "c": [0, -60, 1500], "s": [100, 40, 100], "material": "case_green"}), "detail/BS2 has no case"),
        ("photograph: the case 120 mm too high", lambda t: (K.shift_part(t, V, "case_bar_top", [0, 0, 120]), K.shift_part(t, V, "case_bar_left", [0, 0, 120]), K.shift_part(t, V, "case_bar_right", [0, 0, 120])), "photo/P1/case_top"),
        ("photograph: the flag 90 mm too narrow", lambda t: [p.__setitem__("s", [210.0, p["s"][1], p["s"][2]]) for p in t["variants"][V]["parts"] if p["id"] == "flag_plate"], "photo/P1/flag_left"),
        ("numbers: the pole 300 mm too short", lambda t: [(p.__setitem__("p0", [0, 0, p["p0"][2] * 0.9]), p.__setitem__("p1", [0, 0, p["p1"][2] * 0.9])) for p in t["variants"][V]["parts"] if p["id"].startswith("pole_") and p["id"] != "pole_collar"], "numbers/N1"),
    ]
    return C


if __name__ == "__main__":
    spec = dict(V=V, leaf="case_lock", leaf_move=[0, -40, 0], bridge="pole_upper", join=("case_card", "case_glass"), join_move=[0, 30, 0], overlap=("case_bar_top", [0, 40, 0]), photo_squeeze=0.7,
                blocker={"flag plate": "flag_plate"}, number_id="N5")
    sys.exit(1 if SF.selfcheck_main(HERE, "bus-stop", extra, extra_controls, spec) else 0)
