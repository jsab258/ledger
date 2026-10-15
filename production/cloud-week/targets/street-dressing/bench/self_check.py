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
import sd_place as PL

V = "B1"


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    pl = T["placement"]
    lo, hi = ps.bbox(only=[n for n in ps.names if not n.startswith("bolt")])
    depth = hi[1] - lo[1]
    need = depth + 900.0 + 1000.0
    rows.add("placement", "placement/the footway cannot hold it (depth + 900 leg room + 1000 clear exceeds the footway)", need > pl["footway_mm"], "needs %.0f mm, footway %.0f" % (need, pl["footway_mm"]))
    pose = pl["poses"][0]
    rows.add("placement", "placement/the pose is the stated slot", abs(pose["x_m"] - pl["x_m"]) < 1e-6 and abs(pose["z_m"] - pl["z_m"]) < 1e-6 and PL.direction_name(PL.front_direction(pose)) == pl["faces"], "pose x %.2f z %.2f faces %s; slot x %.2f z %.2f faces %s" % (pose["x_m"], pose["z_m"], PL.direction_name(PL.front_direction(pose)), pl["x_m"], pl["z_m"], pl["faces"]))
    # the cameras: the stated distance to the reverse camera is the scene's own
    cams = {c["id"]: c for c in json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-scene.json")))["cameras"]}
    cr = cams["cam_reverse"]
    d_rev = math.hypot(cr["x_m"] - pose["x_m"], cr["z_m"] - pose["z_m"])
    rows.add("placement", "placement/the stated distance to the reverse camera is the scene's (cam_reverse)", abs(d_rev - pl["cam_reverse"]["distance_m"]) < 0.5 and abs(cr["x_m"] - pl["cam_reverse"]["x_m"]) < 0.01, "%.1f m (stated %.1f)" % (d_rev, pl["cam_reverse"]["distance_m"]))
    rows.add("placement", "placement/the reasons do not claim that the reverse view sees the bench", d_rev > 50.0 and not any("reverse view sees" in r.lower() for r in pl["reasons"]), "%.0f m away" % d_rev)
    # handover H1: the town's own quay place lies on the road arm, not on the apron (the geometry decides)
    h1 = next(h for h in T["handovers"] if h["id"] == "H1")
    hc = json.load(open(os.path.join(L.REPO, h1["place"]["file"])))["places"][h1["place"]["place"]]
    from shapely.geometry import Point
    Q = PL.quay()
    pt = Point(hc["x_m"], hc["z_m"])
    rows.add("placement", "placement/handover H1 is true: the town's quay place is on the road arm and not on the apron", abs(hc["x_m"] - h1["place"]["x_m"]) < 0.01 and abs(hc["z_m"] - h1["place"]["z_m"]) < 0.01 and Q["roads"].buffer(1e-6).contains(pt) and not Q["apron"].contains(pt),
             "places.quay (%.1f, %.1f): on the road arm %s, on the apron %s" % (hc["x_m"], hc["z_m"], Q["roads"].buffer(1e-6).contains(pt), Q["apron"].contains(pt)))
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
        PL.ctl("placement: the first version's slot (x -9.0, z 2.5) is on the road arm", "bench", "place/bench/footprint plus", x_m=-9.0, z_m=2.5),
        PL.ctl("placement: the first version's slot touches the road and the footway of the quay kit", "bench", "place/bench/footprint plus the margin touches no quay road", x_m=-9.0, z_m=2.5),
        PL.ctl("placement: the bench turned to face the street (+x)", "bench", "place/bench/front faces", yaw_deg=90.0),
        PL.ctl("placement: the bench 1 m from the cope (x -68.4)", "bench", "place/bench/the piece is at least", x_m=-68.4),
        PL.ctl("placement: the bench beside a quay bollard (x -68.2, z -28)", "bench", "place/bench/nothing of the quay's furniture", x_m=-68.2, z_m=-28.0),
        PL.ctl("placement: the bench at the level of the street's crown, not the apron", "bench", "place/bench/ground level is the apron's", base_y_m=0.0),
        ("placement: the stated slot changed without the pose", lambda t: t["placement"].__setitem__("x_m", -9.0), "placement/the pose is the stated slot"),
        ("placement: the reverse camera's distance stated as 38 m", lambda t: t["placement"]["cam_reverse"].__setitem__("distance_m", 38.0), "placement/the stated distance to the reverse camera"),
        ("placement: the town's quay place recorded on the apron (x -40)", lambda t: t["handovers"][0]["place"].__setitem__("x_m", -40.0), "placement/handover H1 is true"),
        ("numbers: the end leg 100 mm nearer the slat end", lambda t: K.shift_part(t, V, "end_r_slab", [100.0, 0, 0]), "numbers/N9"),
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
