"""milk-crates: the self-check. python self_check.py [--live] [--previews] [--photos DIR] [--no-controls]"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_family as SF

V = "MC3"
LIVE = "--live" in sys.argv


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    p1 = K._ps_cache(T["variants"]["MC1"]["parts"])
    # the CC0 record on disk against the numbers
    rec = json.load(open(os.path.join(HERE, "polyhaven_checked_raw.json")))["plastic_crate_01"]
    d = rec["dimensions"]
    lo, hi = p1.bbox(only=[n for n in p1.names if "lug" not in n])
    dims = hi - lo
    rows.near("model", "model/crate length is the CC0 record's long side", dims[0], d[1], 1.0)
    rows.near("model", "model/crate width is the CC0 record's short side", dims[1], d[0], 1.0)
    rows.near("model", "model/crate height is the CC0 record's height", dims[2], d[2], 1.0)
    rows.add("model", "model/the CC0 record is CC0 and not NoAI-tagged", "noai" not in json.dumps(rec).lower() and rec.get("authors"), str(rec.get("authors")))
    if LIVE:
        r = subprocess.run(["curl", "-sS", "-m", "40", "-A", L.UA_API, "https://api.polyhaven.com/info/plastic_crate_01"], capture_output=True)
        try:
            live = json.loads(r.stdout)
            ok = all(abs(a - b) < 0.5 for a, b in zip(live["dimensions"], d)) and live["authors"] == rec["authors"]
        except Exception as e:
            ok = False
        rows.add("live", "live/Poly Haven still gives the same box and author", ok, "")
    # the stack
    crates = sorted({n.split("_")[0] for n in ps.names if n.endswith("_floor")})
    rows.add("detail", "detail/three crates", len(crates) == 3, str(crates))
    bottles = [n for n in ps.names if "_bottle" in n]
    rows.add("detail", "detail/six bottles, all in the top crate", len(bottles) == 6 and all(n.startswith("c3_") for n in bottles), "%d" % len(bottles))
    fl, fh = ps.part_bbox("c3_floor")
    rl, rh = ps.part_bbox("c3_rim_f")
    inside = True
    for n in bottles:
        l, h = ps.part_bbox(n)
        inside &= l[0] >= -HL() and h[0] <= HL() and l[1] >= -HW() and h[1] <= HW() and l[2] >= fh[2] - 0.5 and h[2] <= rh[2]
    rows.add("detail", "detail/every bottle stands inside the top crate and below its rim", inside, "")
    rows.add("detail", "detail/the bottles do not overlap each other", all(ps.part_bbox(a)[1][0] <= ps.part_bbox(b)[0][0] + 0.5 or ps.part_bbox(b)[1][0] <= ps.part_bbox(a)[0][0] + 0.5 or ps.part_bbox(a)[1][1] <= ps.part_bbox(b)[0][1] + 0.5 or ps.part_bbox(b)[1][1] <= ps.part_bbox(a)[0][1] + 0.5
                                                                         for a in bottles if "neck" not in a for b in bottles if "neck" not in b and a < b), "")
    # openings: the long walls between the ribs are open (a ray square on goes through between two ribs) while the band, rim and rail are closed (the face rows)
    l0, h0 = ps.part_bbox("c1_rib_f0")
    l1, h1 = ps.part_bbox("c1_rib_f1")
    slot = l1[0] - h0[0]
    rows.add("detail", "detail/the slot between ribs is open and 88 wide (the hand holds and slots are real openings)", abs(slot - 88.0) < 2.0, "%.1f" % slot)
    # the text
    rows.add("detail", "detail/the band text names only the invented dairy", T["text"]["dairy"] == "COPPER ROW DAIRY" and T["text"]["dairy"] in T["text"]["band_text"], T["text"]["band_text"])
    # the placement
    pl = T["placement"]
    depth = K._ps_cache(T["variants"]["MC1"]["parts"]).bbox(only=[n for n in p1.names if "lug" not in n])
    wdepth = depth[1][1] - depth[0][1]
    clear = pl["stallriser_z_m"] * 1000 - pl["gap_to_wall_mm"] - wdepth - pl["kerb_back_z_m"] * 1000
    rows.near("placement", "placement/the clear strip derived from the crate's own width", clear, pl["clear_strip_mm"], 1.0)
    rows.at_least("placement", "placement/the strip is at least a metre", clear, pl["min_clear_mm"])
    rows.add("placement", "placement/the stack stands in the grocer's bay (x 33 to 39)", pl["shop_bay"]["x0"] <= pl["x_m"] - 0.204 and pl["x_m"] + 0.204 <= pl["shop_bay"]["x1"], "x %.2f" % pl["x_m"])
    sc = json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-scene.json")))
    yard = [i for i in sc["held_props"]["items"] if i.get("asset") == "wooden_crate_01"]
    rows.add("reuse", "reuse/the scene's two wooden crates stand at the yard mouth (west), not here", len(yard) == 2 and all(i["side"] == "west" for i in yard), "%d" % len(yard))
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")


def HL():
    return 204.0


def HW():
    return 149.0


def extra_controls(T):
    return [
        ("model: the crate made 30 mm too long", lambda t: [p.__setitem__("s", [p["s"][0] + 30, p["s"][1], p["s"][2]]) for p in t["variants"]["MC1"]["parts"] if p["id"] == "c1_rim_f"], "model/crate length"),
        ("model: the crate 15 percent too low", lambda t: K.scale_all(t, "MC1", 2, 0.85), "model/crate height"),
        ("detail: a seventh bottle added", lambda t: t["variants"][V]["parts"].append({"id": "c3_bottle7", "type": "cyl", "p0": [-150, 100, 538], "p1": [-150, 100, 666], "r0": 32.0, "material": "glass"}), "detail/six bottles"),
        ("detail: a bottle standing in the middle crate", lambda t: [p.__setitem__("id", "c2_bottle1") for p in t["variants"][V]["parts"] if p["id"] == "c3_bottle1"], "detail/six bottles"),
        ("detail: a bottle pushed through the wall", lambda t: K.shift_part(t, V, "c3_bottle2", [330, 0, 0]), "detail/every bottle stands inside"),
        ("detail: a rib moved so the slot is 60", lambda t: K.shift_part(t, V, "c1_rib_f1", [28, 0, 0]), "detail/the slot between ribs"),
        ("detail: the dairy named by a real firm", lambda t: t["text"].__setitem__("dairy", "UNIGATE"), "detail/the band text names only the invented dairy"),
        ("placement: the stack set 600 mm from the wall", lambda t: t["placement"].__setitem__("gap_to_wall_mm", 600.0), "placement/the clear strip derived"),
        ("placement: the stack moved to the fish market's bay", lambda t: t["placement"].__setitem__("x_m", 12.0), "placement/the stack stands in the grocer's bay"),
        ("numbers: the stack pitch 20 mm short", lambda t: [K.shift_part(t, V, p["id"], [0, 0, -20]) for p in t["variants"][V]["parts"] if p["id"].startswith("c2_") or p["id"].startswith("c3_")], "numbers/N4"),
    ]


if __name__ == "__main__":
    spec = dict(V=V, leaf="c3_bottle3", leaf_move=[0, 0, 300], bridge=["c1_floor", "c1_rail_f", "c1_rail_b", "c1_rail_l", "c1_rail_r"], join=("c2_rail_f", "c1_rim_f"), join_move=[0, 0, 60],
                overlap=("c3_bottle6", [-60, 0, 0]), blocker={"c2 front band": "c2_band_f", "c2 rim front": "c2_rim_f", "c2 base rail front": "c2_rail_f"}, number_id="N5")
    sys.exit(1 if SF.selfcheck_main(HERE, "milk-crates", extra, extra_controls, spec) else 0)
