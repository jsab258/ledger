"""phone-box: the self-check. python self_check.py [--live] [--previews] [--photos DIR] [--no-controls]
Offline: every row is derived from target.json's parts and text. --live re-reads the Geograph pages and re-measures the
photograph's edges from its pixels. --previews checks the preview files."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K

V = "KX1"


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    lo, hi = ps.bbox(only=[n for n in ps.names if n != "f_pull"])
    depth = hi[1] - lo[1]
    pl = T["placement"]
    # the clear strip from the target's own numbers
    kiosk_face = pl["stallriser_line_z_m"] * 1000.0 - depth
    clear = kiosk_face - pl["kerb_back_z_m"] * 1000.0
    rows.near("placement", "placement/clear strip is derived from the kiosk's own depth", clear, pl["clear_strip_mm"], 1.0)
    rows.at_least("placement", "placement/the strip is at least a walking person", clear, pl["min_clear_mm"])
    rows.near("placement", "placement/the stated face range matches", kiosk_face / 1000.0, pl["kiosk_face_z_m"][0], 0.001, unit="m")
    # the pull stands 28 proud of the band, the band 10 proud of the frame, three hinges
    pull_lo, _ = ps.part_bbox("f_pull")
    band_lo, _ = ps.part_bbox("f_band")
    stile_lo, _ = ps.part_bbox("f_stile_l")
    rows.near("detail", "detail/the pull stands 28 mm out of the band", band_lo[1] - pull_lo[1], 28.0, 3.0)
    rows.near("detail", "detail/the band stands 10 mm out of the frame", stile_lo[1] - band_lo[1], 10.0, 2.0)
    rows.near("detail", "detail/three hinges on the right post", ps.names.__len__() and len([n for n in ps.names if n.startswith("f_hinge")]), 3, 0.1, unit="")
    # the glass lies inside its frame, in the stated places
    gl, gh = ps.part_bbox("f_glass_up")
    zl = T["text"]["logo_zone"]
    rows.add("detail", "detail/the logo zone lies on the upper front pane and holds no part",
             zl[0] >= gl[0] and zl[1] <= gh[0] and zl[2] >= gl[2] and zl[3] <= gh[2] and not any(
                 p["id"].startswith("f_") and p["id"] not in ("f_glass_up",) and ps.part_bbox(p["id"])[0][2] < zl[3] and ps.part_bbox(p["id"])[1][2] > zl[2] and ps.part_bbox(p["id"])[0][0] < zl[1] and ps.part_bbox(p["id"])[1][0] > zl[0]
                 for p in T["variants"][V]["parts"] if p["id"] not in ("f_stile_l", "f_stile_r", "f_hinge1", "f_hinge2", "f_hinge3")), "")
    rows.add("detail", "detail/the header word is the plain word and nothing else", T["text"]["header_word"] == "Telephone", T["text"]["header_word"])
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    rows.add("detail", "detail/only glass is transparent", all((p.get("material") == "glass") == bool(p.get("transparent")) for v in T["variants"].values() for p in v["parts"]), "")
    # the doorless variant has the same lid, posts, back and payphone as the door variant, and no leaf
    ps2 = K._ps_cache(T["variants"]["KX2"]["parts"])
    same = all(n in ps2.names for n in ("lid_top", "p_fl", "back_panel", "pp_body", "f_header"))
    leafless = not any(n.startswith(("f_glass", "f_stile", "f_band", "f_hinge", "f_pull", "f_rail")) for n in ps2.names)
    rows.add("detail", "detail/KX2 keeps the shell and drops the leaf", same and leafless, "")
    # the earlier script's numbers really are the ones the target says it replaces
    scr = os.path.join(L.REPO, "tools", "meshgen", "blender", "clutter", "kx100_kiosk.py")
    if os.path.exists(scr):
        txt = open(scr).read()
        H0 = float(re.search(r"^H = ([0-9.]+)", txt, re.M).group(1)) * 1000
        band = re.search(r'panel\("band", ([0-9.]+), ([0-9.]+)', txt)
        zc, hh = float(band.group(1)), float(band.group(2))
        old_b0, old_b1 = (zc - hh / 2) * 1000, (zc + hh / 2) * 1000
        n_b0 = ps.part_bbox("f_band")[0][2]
        rows.add("reuse", "reuse/the old script's band (1.00 to 1.12 m) is not the target's", abs((old_b0 + old_b1) / 2 - (n_b0 + ps.part_bbox("f_band")[1][2]) / 2) > 20, "old %.0f to %.0f, target %.0f to %.0f" % (old_b0, old_b1, n_b0, ps.part_bbox("f_band")[1][2]))
        rows.add("reuse", "reuse/the old script's height (2.18 m) differs from the printed 2192", abs(H0 - hi[2]) > 5, "old %.0f, target %.0f" % (H0, hi[2]))
    else:
        rows.add("reuse", "reuse/the old script is present", False, scr)
    sc_path = os.path.join(L.REPO, "production", "specs", "vignette-scene.json")
    if os.path.exists(sc_path):
        sc = json.load(open(sc_path))
        e3 = [f for f in sc["furniture"] if f.get("bom") == "E3_telephone_kiosk"][0]
        rows.add("reuse", "reuse/the scene's kiosk is the older proportions (plan 0.914, height 2.515)", abs(e3["plan_m"] * 1000 - 914) < 1 and abs(e3["height_m"] * 1000 - 2515) < 1, str((e3["plan_m"], e3["height_m"])))
        rows.add("reuse", "reuse/the scene's setback leaves less than a walking person", (2000 - e3["setback_from_kerb_m"] * 1000 - e3["plan_m"] * 1000) < pl["min_clear_mm"], "%.0f mm" % (2000 - e3["setback_from_kerb_m"] * 1000 - e3["plan_m"] * 1000))
        # Rita's bay: the scene's x lies within bay 2 (x 15 to 21); the target's does not
        rows.add("placement", "placement/the old x stands in Rita's bay and the new x does not", 15.0 <= e3["x_m"] <= 21.0 and not (15.0 <= pl["x_centre_m"] <= 21.0), "old %.1f new %.1f" % (e3["x_m"], pl["x_centre_m"]))
        rows.add("placement", "placement/the new x stands in bay 3 (x 21 to 27), the empty unit", 21.0 <= pl["x_centre_m"] - 0.445 and pl["x_centre_m"] + 0.445 <= 27.0, "%.2f to %.2f" % (pl["x_centre_m"] - 0.445, pl["x_centre_m"] + 0.445))


def extra_controls(T):
    def ch(t, key, val):
        t["placement"][key] = val

    def bad_setback(t):
        t["placement"]["stallriser_line_z_m"] = 3.125 + 0.55 + 0.89 + 0.0  # the scene's set-back
        t["placement"]["kiosk_face_z_m"][0] = 3.125 + 0.55
    C = [
        ("placement: the scene's 0.55 m set-back put back", bad_setback, "placement/the strip is at least a walking person"),
        ("placement: the clear strip stated wrongly", lambda t: ch(t, "clear_strip_mm", 560.0), "placement/clear strip is derived"),
        ("placement: the box moved back before Rita's window", lambda t: ch(t, "x_centre_m", 16.5), "placement/the new x stands in bay 3"),
        ("detail: the pull only 10 mm out", lambda t: K.shift_part(t, V, "f_pull", [0, 18, 0]), "detail/the pull stands 28 mm"),
        ("detail: a hinge removed", lambda t: K.drop_part(t, V, "f_hinge3"), "detail/three hinges"),
        ("detail: the header word changed", lambda t: t["text"].__setitem__("header_word", "Telephone Kiosk"), "detail/the header word"),
        ("detail: a logo part put in the logo zone", lambda t: t["variants"][V]["parts"].append({"id": "f_logo", "type": "box", "c": [0, -430, 1400], "s": [200, 4, 200], "material": "handle_yellow"}), "detail/the logo zone"),
        ("detail: a material missing", lambda t: t["variants"][V]["parts"][0].__setitem__("material", "chrome"), "detail/every part's material"),
        ("detail: the doorless variant given a glass pane", lambda t: t["variants"]["KX2"]["parts"].append({"id": "f_glass_x", "type": "box", "c": [0, -430, 1400], "s": [600, 4, 600], "material": "glass", "transparent": True}), "detail/KX2 keeps the shell"),
        ("photograph: the handle band moved 40 mm up", lambda t: K.shift_part(t, V, "f_band", [0, 0, 40]), "photo/P1/band_top"),
        ("photograph: the header 60 mm too low", lambda t: K.shift_part(t, V, "f_header", [0, 0, -60]), "photo/P1/header_bottom"),
        ("photograph: the glazing 60 mm too narrow", lambda t: (K.shift_part(t, V, "f_stile_l", [60, 0, 0]), K.shift_part(t, V, "f_stile_r", [-60, 0, 0])), "photo/P1/glass_l"),
        ("photograph: the posts 30 mm too thick", lambda t: [p.__setitem__("s", [70.0, p["s"][1], p["s"][2]]) for p in t["variants"][V]["parts"] if p["id"] in ("p_fl",)], "photo/P1/frame_l_outer"),
        ("numbers: the lid skirt 40 mm deeper", lambda t: [p.__setitem__("s", [p["s"][0], p["s"][1], p["s"][2] + 40]) for p in t["variants"][V]["parts"] if p["id"] == "lid_skirt_front"], "numbers/N4"),
    ]
    return C


if __name__ == "__main__":
    spec = dict(V=V, leaf="pp_keypad", bridge="back_panel", join=("f_pull", "f_band"), join_move=[0, 0, 200], overlap=("f_hinge2", [-30, 0, 0]),
                blocker={"back": "back_panel", "roof": "lid_top", "header front": "f_header", "handle band": "f_band", "left side header": "sl_header"}, number_id="N6")
    sys.exit(1 if K.main("phone-box", HERE, extra=extra, extra_controls=extra_controls, ctl_spec=spec) else 0)
