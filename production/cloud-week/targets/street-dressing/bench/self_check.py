"""bench: the self-check. python self_check.py [--live] [--previews] [--photos DIR] [--no-controls]"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_family as SF

V = "B1"


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    pl = T["placement"]
    lo, hi = ps.bbox(only=[n for n in ps.names if not n.startswith("bolt")])
    depth = hi[1] - lo[1]
    need = depth + 900.0 + 1000.0
    rows.add("placement", "placement/the footway cannot hold it (depth + 900 leg room + 1000 clear exceeds the footway)", need > pl["footway_mm"], "needs %.0f mm, footway %.0f" % (need, pl["footway_mm"]))
    rows.at_least("placement", "placement/the apron is at least 3 m wide where it stands", pl["min_pavement_mm"], 3000.0)
    rows.add("placement", "placement/it stands south of the street's end (x below 0) and faces -x", pl["x_m"] < 0 and pl["faces"] == "-x", "")
    rows.near("placement", "placement/the stated depth is the bench's", depth, pl["bench_depth_mm"], 50.0)
    # slats: counts and gaps measured from the parts
    seat = [n for n in ps.names if n.startswith("seat_slat_")]
    back = [n for n in ps.names if n.startswith("back_slat_")]
    rows.add("detail", "detail/five seat slats and five back slats", len(seat) == 5 and len(back) == 5, "%d and %d" % (len(seat), len(back)))
    gaps = []
    for a, b in zip(seat, seat[1:]):
        la, ha = ps.part_bbox(a)
        lb, hb = ps.part_bbox(b)
        gaps.append(lb[1] - ha[1])
    rows.add("detail", "detail/the seat gaps are equal at 23.5", all(abs(g - 23.5) < 1.0 for g in gaps), str([round(g, 1) for g in gaps]))
    # back slat gaps measured perpendicular to the rake: along z, between centres less the slat's own height
    zc = []
    for n in back:
        lo_, hi_ = ps.part_bbox(n)
        zc.append((lo_[2] + hi_[2]) / 2)
    pitches = [b - a for a, b in zip(zc, zc[1:])]
    rows.add("detail", "detail/the back slats' pitch is 86.5 along z (cos of the rake aside)", all(abs(p - 86.5) < 1.0 for p in pitches), str([round(p, 1) for p in pitches]))
    # the three frames are identical
    def frame_sig(tag):
        return sorted((n[len(tag):], round(ps.part_bbox(n)[1][2] - ps.part_bbox(n)[0][2], 1), round(ps.part_bbox(n)[1][1] - ps.part_bbox(n)[0][1], 1)) for n in ps.names if n.startswith(tag))
    sl, sr, sm = frame_sig("end_l_"), frame_sig("end_r_"), frame_sig("mid_")
    rows.add("detail", "detail/the three end frames are identical in section", sl == sr == sm, "")
    rows.add("detail", "detail/the rear seat slat stops in front of the back posts", ps.part_bbox("seat_slat_5")[1][1] <= ps.part_bbox("end_l_post")[0][1] + 0.5, "")
    rows.near("detail", "detail/the end legs are 100 thick and 146 mm in from the slat end (P1)", ps.part_bbox("end_r_slab")[1][0] - ps.part_bbox("end_r_slab")[0][0], 100.0, 1.0)
    rows.near("detail", "detail/the leg centre is 146 mm in from the slat end", ps.bbox(only=["seat_slat_1"])[1][0] - (ps.part_bbox("end_r_slab")[0][0] + ps.part_bbox("end_r_slab")[1][0]) / 2, 146.0, 2.0)
    # the rake: the end post's top is behind its foot by tan(rake) x height
    lo_p, hi_p = ps.part_bbox("end_l_post")
    rake = math.degrees(math.atan2(hi_p[1] - lo_p[1] - 40.0, hi_p[2] - lo_p[2]))
    rows.near("detail", "detail/the post's rake is 10 degrees", rake, 10.0, 1.0, unit="deg")
    # bolts sit on the back slats' faces, proud 7 mm
    bad = []
    for k in range(1, 6):
        lo_s, hi_s = ps.part_bbox("back_slat_%d" % k)
        lo_b, hi_b = ps.part_bbox("bolt_m%d" % k)
        if not (lo_b[1] < lo_s[1] + 8.0 and lo_b[2] >= lo_s[2] and hi_b[2] <= hi_s[2]):
            bad.append(k)
    rows.add("detail", "detail/every bolt head lies on its slat's face", not bad, str(bad))
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    n2 = K._ps_cache(T["variants"]["B2"]["parts"]).names
    rows.add("detail", "detail/B2 is the short bench: ten slats, two frames, no centre frame, 1200 long", sum(1 for n in n2 if n.startswith(("seat_slat", "back_slat"))) == 10 and not any(n.startswith("mid_") for n in n2) and abs(K._ps_cache(T["variants"]["B2"]["parts"]).bbox()[1][0] - K._ps_cache(T["variants"]["B2"]["parts"]).bbox()[0][0] - 1200.0) < 12.0, "")
    rows.add("detail", "detail/no plaque or lettering part", not any(("plaque" in n or "plate" in n or "text" in n) for v in T["variants"].values() for n in K._ps_cache(v["parts"]).names), "")
    # the scene file keeps benches off the footway
    sc = json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-scene.json")))
    benches = [x for x in sc["held_props"]["not_placed"] if x.get("bom") == "E7_benches"]
    rows.add("reuse", "reuse/the scene's four held benches are all not placed", len(benches) == 4 and all("2.0 m" in b["why"] or "footway" in b["why"].lower() for b in benches), "%d held" % len(benches))


def extra_controls(T):
    return [
        ("placement: the footway stated as 3 m", lambda t: t["placement"].__setitem__("footway_mm", 3000.0), "placement/the footway cannot hold it"),
        ("placement: the bench put at x +20 on the street", lambda t: t["placement"].__setitem__("x_m", 20.0), "placement/it stands south"),
        ("detail: one back slat moved 20 mm out of pitch", lambda t: K.shift_part(t, V, "back_slat_3", [0, 0, 20]), "detail/the back slats' pitch"),
        ("detail: one seat gap closed", lambda t: K.shift_part(t, V, "seat_slat_3", [0, -15, 0]), "detail/the seat gaps"),
        ("detail: a bolt head off its slat", lambda t: K.shift_part(t, V, "bolt_m2", [0, 60, 0]), "detail/every bolt head lies on its slat"),
        ("detail: the centre frame different", lambda t: [p["poly"].__setitem__(1, [245.0, 120.0]) for p in t["variants"][V]["parts"] if p["id"] == "mid_slab"], "detail/the three end frames are identical in section"),
        ("detail: a plaque part added", lambda t: t["variants"][V]["parts"].append({"id": "memorial_plaque", "type": "box", "c": [0, 100, 600], "s": [100, 5, 50], "material": "galvanised"}), "detail/no plaque"),
        ("photograph: a back slat 30 mm out", lambda t: K.shift_part(t, V, "back_slat_4", [0, 0, 30]), "photo/P1/gap1_bottom"),
        ("photograph: the bench 20 percent too short", lambda t: K.scale_all(t, V, 0, 0.8), "photo/P1/left_end"),
        ("numbers: the seat 80 mm too high", lambda t: [K.shift_part(t, V, "seat_slat_%d" % k, [0, 0, 80]) for k in range(1, 6)], "numbers/N2"),
    ]


if __name__ == "__main__":
    spec = dict(V=V, leaf="bolt_m2", leaf_move=[0, -40, 0], bridge=["end_l_slab", "end_r_slab", "mid_slab"], join=("bolt_l1", "back_slat_1"), join_move=[0, -60, 0], overlap=("back_slat_3", [0, 40, 0]), blocker={}, number_id="N4", photo_squeeze=0.7)
    sys.exit(1 if SF.selfcheck_main(HERE, "bench", extra, extra_controls, spec) else 0)
