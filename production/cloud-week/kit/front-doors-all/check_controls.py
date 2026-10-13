"""Wrong copies for check_doors.py (cloud week 42, unit 9): each one breaks the doors, the street data or a text in one named way and must make a named row fail.

A control passes (is "caught") only if the named row exists and FAILS on the wrong copy; a crash is not a catch (the target's fresh review found rows that could never
fail and controls that tested something other than their name). Run with `check_doors.py --controls`.
"""
import copy
import json
import os
import re
import traceback

import numpy as np


def run_controls(N, H, mods, houses_mods, furn_cache, C):
    rows = []
    paints_json = json.load(open(os.path.join(C.ASSET, "paints.json")))
    cond_json = json.load(open(os.path.join(C.ASSET, "conditions.json")))
    tgt = {}
    for c in N["checks"]:
        tgt.setdefault(c["group"], []).append(c)
    byid = {c["id"]: c for c in N["checks"]}
    texts_ok = {fn: open(os.path.join(C.HERE, fn), encoding="utf-8").read() for fn in sorted(os.listdir(C.HERE)) if fn.endswith(".py") and fn != "check_controls.py"}
    for fn in ("houses.json", "paints.json", "conditions.json", "manifest.json"):
        texts_ok[fn] = open(os.path.join(C.ASSET, fn), encoding="utf-8").read()
    glb_paths = {k: os.path.join(C.ASSET, "door_%s.glb" % k) for k in C.KINDS}

    def ctl(name, row_id, fn):
        try:
            rep = fn()
            failed = {r["id"] for r in rep.rows if r["ok"] is False}
            caught = row_id in failed and any(r["id"] == row_id for r in rep.rows)
            rows.append({"name": name, "row": row_id, "caught": bool(caught), "failed_rows": sorted(failed)[:6]})
        except Exception as e:                                          # a crash is not a catch
            rows.append({"name": name, "row": row_id, "caught": False, "crash": "".join(traceback.format_exception_only(type(e), e)).strip()})

    def new():
        return C.Report()

    def pl(kind, Nx, mod=None):
        rep = new()
        m = mod or mods[kind]
        holes, inner = C.interior_holes(m)
        C.row_PL(Nx, m, rep, holes, inner)
        return rep

    # ---- panel layout against a wrong target (the mesh is right, the number is wrong)
    def n_edit(kind, fn):
        Nx = copy.deepcopy(N)
        fn(Nx["kinds"][kind]["leaf"])
        for c in Nx["checks"]:
            if c["kind"] == kind and c["type"] == "opening_bounds":
                o = [o for o in Nx["kinds"][kind]["leaf"]["openings"] if o["id"] == c["opening"]]
                if o:
                    c["expect"] = [o[0]["u0"], o[0]["u1"], o[0]["v0"], o[0]["v1"]]
        return Nx

    def bar_moved(lf):
        for o in lf["openings"]:
            if o["id"] == "light2":
                o["v0"] += 20.0
                o["v1"] += 20.0
    ctl("T2: a bar moved 20 mm (light 2 20 mm higher in the target)", "PL-T2-light2", lambda: pl("T2", n_edit("T2", bar_moved)))

    def three(lf):
        lf["openings"] = lf["openings"][:3]
    Nx = copy.deepcopy(N)
    for c in Nx["checks"]:
        if c["id"] == "PL-T2-count":
            c["expect"] = 3
    ctl("T2: three lights expected, four built", "PL-T2-count", lambda: pl("T2", Nx))

    def slit_wide(lf):
        o = lf["openings"][0]
        o["u0"] -= 50.0
        o["u1"] += 50.0
    ctl("F5: the slit 50 mm wider on each side in the target", "PL-F5-slit", lambda: pl("F5", n_edit("F5", slit_wide)))

    def light_low(lf):
        for o in lf["openings"]:
            if o["id"] == "small_light":
                o["v0"] -= 60.0
                o["v1"] -= 60.0
    ctl("T3: the small light 60 mm lower in the target", "PL-T3-small_light", lambda: pl("T3", n_edit("T3", light_low)))

    def one_outline(lf):
        for o in lf["openings"]:
            if o["id"] == "upper_panel":
                o["inner"]["u0"] += 60.0
    Nx = n_edit("T3", one_outline)
    for c in Nx["checks"]:
        if c["id"] == "PL-T3-upper_panel-inner":
            c["expect"][0] += 60.0
    ctl("T3: the upper panel's inner outline 60 mm narrower in the target", "PL-T3-upper_panel-inner", lambda: pl("T3", Nx))

    def flat_heads(lf):
        for o in lf["openings"]:
            if o["id"] == "long_l":
                o["head_rise"] = 0.0
    Nx = n_edit("F3", flat_heads)
    for c in Nx["checks"]:
        if c["id"] == "PL-F3-long_l-head":
            c["expect"]["head_rise"] = 0.0
    ctl("F3: square panel heads expected, raked ones built (the first draft)", "PL-F3-long_l-head", lambda: pl("F3", Nx))

    def stiles_wrong(lf):
        lf["stile_right"] = 114.3
    Nx = copy.deepcopy(N)
    for c in Nx["checks"]:
        if c["id"] == "PL-T2-members":
            c["expect"]["stile_right"] = 114.3
    ctl("T2: both stiles 114.3 expected (the first draft), 94 and 69 built", "PL-T2-members", lambda: pl("T2", Nx))

    # ---- nothing shows through
    def cv(kind, mod):
        rep = new()
        C.row_CV(N, mod, rep)
        return rep
    shift_leaf = lambda n: n.startswith(("leaf_", "panel_", "moulding_", "bead_", "glass_light", "glass_slit", "glass_small", "net_", "iron_nail", "glass_lens"))
    ctl("T1: a leaf shifted 14 mm (the left stop laps it by only 6.4)", "CV-T1-angle", lambda: cv("T1", mods["T1"].copy_with(shift=(shift_leaf, (14.0, 0.0, 0.0)))))
    ctl("T1: a leaf set back 12 mm behind the stops", "CV-T1-angle", lambda: cv("T1", mods["T1"].copy_with(shift=(shift_leaf, (0.0, 12.0, 0.0)))))
    ctl("T1: a leaf hung 12 mm in front of its stops", "CV-T1-inward", lambda: cv("T1", mods["T1"].copy_with(shift=(shift_leaf, (0.0, -12.0, 0.0)))))
    ctl("F1: a leaf 40 mm lower (the lap under the transom lost)", "CV-F1-angle", lambda: cv("F1", mods["F1"].copy_with(shift=(shift_leaf, (0.0, 0.0, -40.0)))))
    ctl("F1: a panel left out (a see-through hole)", "CV-F1-elevation", lambda: cv("F1", mods["F1"].copy_with(drop=("panel_top_left", "moulding_bolection_top_left", "moulding_single_top_left"))))
    ctl("F7: the last board left out (a slot beside the leaf)", "CV-F7-elevation", lambda: cv("F7", mods["F7"].copy_with(drop=("leaf_board_6",))))

    def f7_gap():
        m = mods["F7"]
        V, F = m.M["leaf_board_3"]
        # a board with no tongue: cut the tongue's vertices back to the board's own edge
        V2 = V.copy()
        edge = (V2[np.abs(V2[:, 1] - (m.LY0 + 2.0) / 1000.0) < 1e-5][:, 0]).max()
        V2[V2[:, 0] > edge + 1e-6, 0] = edge
        rep = new()
        C.row_CV(N, m.copy_with(extra={"leaf_board_3": (V2, F)}), rep)
        return rep
    ctl("F7: a board with no tongue", "CV-F7-joints", f7_gap)

    # ---- furniture
    def fu(kind, mutate):
        rec = copy.deepcopy([h for h in H["houses"] if h["kind"] == kind][0])
        mutate(rec)
        m = C.assemble(N, mods[kind], rec, furn_cache)
        rep = new()
        C.row_FU(N, kind, m, rep)
        return rep

    def move(slot, dz=0.0, dx=0.0):
        def f(rec):
            for fu_ in rec["furniture"]:
                if fu_["slot"] == slot:
                    fu_["frame_mm"][2] += dz
                    fu_["frame_mm"][0] += dx
        return f
    ctl("T1: the letter plate moved 40 mm", "FU-T1-letter_plate-LP1", lambda: fu("T1", move("letter_plate", dz=40.0)))
    ctl("T2: the bar pull moved 40 mm", "FU-T2-handle-HD3", lambda: fu("T2", move("handle", dz=40.0)))
    ctl("F6: the lever on the wrong stile (700 mm to the left)", "FU-F6-handle-HD2a", lambda: fu("F6", move("handle", dx=-300.0)))

    def drop_slot(slot):
        def f(rec):
            rec["furniture"] = [x for x in rec["furniture"] if x["slot"] != slot]
        return f
    ctl("F6: the lock under the lever left out", "FU-F6-latch-LK3", lambda: fu("F6", drop_slot("latch")))
    ctl("F1: the plugged keyhole left out", "FU-F1-keyhole-KH1", lambda: fu("F1", drop_slot("keyhole")))

    def fit_clear(mutate):
        rec = copy.deepcopy([h for h in H["houses"] if h["kind"] == "F2"][0])
        mutate(rec)
        rep = new()
        C.row_FIT(N, C.assemble(N, mods["F2"], rec, furn_cache), rep, rec["house"])
        return rep

    def back_to_1545(rec):
        for fu_ in rec["furniture"]:
            if fu_["slot"] == "letter_plate":
                fu_["frame_mm"][2] -= 5.0
    ctl("F2: the letter plate at the target's v 1545 (its foot on the long panels' moulding lip)", "FIT:F2:east_parade_bay1:clear_of_mouldings", lambda: fit_clear(back_to_1545))

    # ---- the bell push
    def bell(extra_part=None, name=None):
        fc = dict(furn_cache)
        parts = dict(fc["BL1"])
        if extra_part:
            parts[extra_part] = parts["iron_bellpush"]
        fc["BL1"] = parts
        rep = new()
        C.row_BP(N, H, mods, fc, rep)
        return rep
    ctl("the push given a bezel part", "BP-form", lambda: bell("iron_bellpush_bezel"))
    ctl("the push given a button part", "BP-no-modern", lambda: bell("iron_bellpush_button"))

    def bell_on_f1():
        Hx = copy.deepcopy(H)
        for h in Hx["houses"]:
            if h["kind"] == "F1":
                h["furniture"].append({"slot": "bell", "variant": "BL1"})
        rep = new()
        C.row_BP(N, Hx, mods, furn_cache, rep)
        return rep
    ctl("a bell push on every F1 house", "BP-houses", bell_on_f1)

    def bell_part_in_f1():
        rep = new()
        C.row_BP(N, H, {**mods, "F1": mods["F1"].copy_with(extra={"iron_bellpush": mods["F1"].M["frame_head"]})}, furn_cache, rep)
        return rep
    ctl("F1 carrying a part named iron_bellpush", "BP-none-elsewhere", bell_part_in_f1)

    # ---- the street and the paints
    def street(mutate, ids=("AD", "PN", "WR"), cond=None, texts=None, paints=None):
        Hx = copy.deepcopy(H)
        mutate(Hx)
        rep = new()
        C.row_AD_PN_WR_NM(N, Hx, rep, [c for g in ids for c in tgt[g]], paints or paints_json, cond or cond_json, glb_paths, texts or texts_ok)
        return rep

    def same_paint(Hx):
        b = {h["house"]: h for h in Hx["houses"]}
        b["east_parade_bay1"]["paint"] = b["east_parade_bay0"]["paint"]
    ctl("two neighbours given one paint", "AD-adjacent-east", lambda: street(same_paint))

    def same_kind(Hx):
        b = {h["house"]: h for h in Hx["houses"]}
        b["west_north_bay0"]["kind"] = b["west_north_bay1"]["kind"]
    ctl("two neighbours given one kind", "AD-adjacent-west", lambda: street(same_kind))

    def same_furn(Hx):
        b = {h["house"]: h for h in Hx["houses"]}
        b["east_parade_bay2"]["variants"] = dict(b["east_parade_bay1"]["variants"])
        b["east_parade_bay2"]["kind"] = "F2"
    ctl("two neighbours given the same fittings", "AD-adjacent-east", lambda: street(same_furn))

    def facing(Hx):
        b = {h["house"]: h for h in Hx["houses"]}
        b["west_south_bay2"]["paint_class"] = b["east_parade_bay0"]["paint_class"]
    ctl("a door facing another in the same paint class", "AD-opposite", lambda: street(facing))

    def cottage_flat(Hx):
        b = {h["house"]: h for h in Hx["houses"]}
        b["west_south_bay1"]["kind"] = "F5"
    ctl("a cottage given a flat kind", "AD-frame-set", lambda: street(cottage_flat))

    def missing(Hx):
        Hx["houses"] = [h for h in Hx["houses"] if h["house"] != "east_parade_bay3"]
    ctl("a house missing from the street", "AD-coverage", lambda: street(missing))

    def puce(Hx):
        Hx["houses"][0]["paint"] = "puce"
    pj = copy.deepcopy(paints_json)
    ctl("a paint outside the palette on a house (palette list changed)", "PN-palette", lambda: street(puce, ids=("PN",)))

    def bright5(Hx):
        for h in Hx["houses"][:5]:
            h["paint_class"] = "bright"
    ctl("five bright doors", "PN-light-doors", lambda: street(bright5, ids=("PN",)))

    def cream_frame(Hx):
        Hx["houses"][0]["frame_colour"] = "cream"
    ctl("a cream frame colour on a house", "PN-frames", lambda: street(cream_frame, ids=("PN",)))

    pj2 = copy.deepcopy(paints_json)
    pj2["door_paints"][0]["srgb"] = [36, 36, 40]
    ctl("the black paint changed from 3.1's value in the data", "PN-srgb", lambda: street(lambda Hx: None, ids=("PN",), paints=pj2))

    def hill_alike(Hx):
        Hx["hill"][1]["kind"] = Hx["hill"][0]["kind"]
    ctl("the hill's neighbours alike", "AD-backdrop", lambda: street(hill_alike, ids=("AD",)))
    cj = copy.deepcopy(cond_json)
    cj["conditions"]["neglected"]["paint_flake_share"] = 0.20
    ctl("neglected wear share 0.20 instead of 0.40", "WR-wear-target", lambda: street(lambda Hx: None, ids=("WR",), cond=cj))
    cj2 = copy.deepcopy(cond_json)
    cj2["conditions"]["tired"]["paint_flake_share"] = 0.01
    ctl("tired wear share below kept", "WR-order", lambda: street(lambda Hx: None, ids=("WR",), cond=cj2))

    def conds(Hx):
        for h in Hx["houses"]:
            if h["condition"] == "neglected":
                h["condition"] = "tired"
    ctl("no neglected house in the street", "WR-houses", lambda: street(conds, ids=("WR",)))
    t_stale = dict(texts_ok)
    t_stale["stale.py"] = "NIGHT = (1, 0." + "7055, 0)"
    t_stale["houses.json"] = re.sub(r"\[\s*1\.0,\s*0\.25,\s*0\.0\s*\]", "[1, 0." + "7055, 0]", texts_ok["houses.json"])
    ctl("the stale night colour in a text", "NM-night", lambda: street(lambda Hx: None, ids=("NM",), texts=t_stale))
    t_maker = dict(texts_ok)
    t_maker["houses.json"] = texts_ok["houses.json"] + " a " + C.TC.BLOCKLIST[0].capitalize() + " rim latch"
    ctl("a maker's name in a text", "NM-maker", lambda: street(lambda Hx: None, ids=("NM",), texts=t_maker))

    # ---- glass
    def gl(mods_x, Nx=None):
        rep = new()
        C.row_GL(Nx or N, mods_x, rep, tgt["GL"])
        return rep
    Nx = copy.deepcopy(N)
    for c in Nx["checks"]:
        if c["id"] == "GL-leaded":
            c["expect"]["came_w"] = 10.0
    tg = copy.deepcopy(tgt["GL"])
    for c in tg:
        if c["id"] == "GL-leaded":
            c["expect"] = dict(c["expect"], came_w=10.0)

    def gl_tg(mods_x, tglist):
        rep = new()
        C.row_GL(N, mods_x, rep, tglist)
        return rep
    ctl("the leaded came expected 10 wide (built 6)", "GL-leaded", lambda: gl_tg(mods, tg))
    tg2 = copy.deepcopy(tgt["GL"])
    for c in tg2:
        if c["id"] == "GL-reeded":
            c["expect"] = dict(c["expect"], pitch=9.0)
    ctl("the reeded pitch expected 9 mm (built 6)", "GL-reeded", lambda: gl_tg(mods, tg2))
    ctl("T2's fanlight plain (no came built)", "GL-leaded", lambda: gl_tg({**mods, "T2": mods["T2"].copy_with(drop=("lead_came",))}, tgt["GL"]))
    ctl("F6's transom flat (no flutes built)", "GL-reeded", lambda: gl_tg({**mods, "F6": mods["F6"].copy_with(drop=("glass_fanlight_flutes",))}, tgt["GL"]))

    # ---- photographs: a recorded box moved
    def ph(mut):
        Nx = copy.deepcopy(N)
        mut(Nx)
        rep = new()
        C.row_PH(Nx, mods, houses_mods, H, rep, [c for c in tgt["PH"] if c["id"] in ("PH-T2-D3", "PH-F5-D2", "PH-T3-D4", "PH-F6-D5", "PH-F4-D2")])
        return rep

    def d3_rows(Nx):
        r = Nx["sources"]["measurements"]["D3_rows"]["rows_px"]
        for k_ in r:
            r[k_] = [x + 12.0 for x in r[k_]]
    ctl("D3's light rows moved 12 px", "PH-T2-D3", lambda: ph(d3_rows))

    def d2_slit(Nx):
        b = Nx["sources"]["measurements"]["D2_F5_slit"]["box"]
        b[1] += 20.0
        b[3] += 20.0
    ctl("D2's slit box moved 20 px", "PH-F5-D2", lambda: ph(d2_slit))

    def d4_light(Nx):
        b = Nx["sources"]["measurements"]["D4_T3_light"]["box"]
        b[1] += 8.0
        b[3] += 8.0
    ctl("D4's small light box moved 8 px", "PH-T3-D4", lambda: ph(d4_light))

    # ---- drawings and profiles
    def draw(kind, mod, Nx=None):
        rep = new()
        C.check_drawings(Nx or N, mod, rep, None)
        return rep
    ctl("F1: the transom missing", "A1:F1:frame", lambda: draw("F1", mods["F1"].copy_with(drop=("frame_transom",))))
    ctl("T2: the leaf's lights 20 mm out (a glass pane moved is not a hole: the leaf slab shifted)", "A1:T2:visible", lambda: draw("T2", mods["T2"].copy_with(shift=(lambda n: n == "leaf_frame", (20.0, 0.0, 0.0)))))

    def prof_bol():
        Nx = copy.deepcopy(N)
        pr = Nx["kinds"]["T1"]["mouldings"]["outside"]["profile_dh"]
        for q in pr:
            q[0] *= 36.0 / 46.0
        rep = new()
        C.profile_rows(Nx, mods["T1"], rep)
        return rep
    ctl("T1: the target's bolection 36 wide instead of the built 46", "A4:T1:bolection", prof_bol)

    # ---- the files
    def shared():
        m = mods["F1"].copy_with(extra={"leaf_dup": mods["F1"].M["leaf_frame"]})
        rep = new()
        C.row_coplanar(N, m, rep, "F1")
        return rep
    ctl("a second part on the leaf's own face planes", "GLB:F1:no_shared_face_plane", shared)

    def dims():
        rep = new()
        C.row_DIM(N, mods["F2"].copy_with(shift=(lambda n: n == "leaf_frame", (0.0, 0.0, 6.0))), rep)
        return rep
    ctl("F2: the leaf 6 mm too high", "DIM:F2:leaf_z0", dims)

    def notch_off():
        rep = new()
        C.notch_rows(N, rep, neglected_npz=os.path.join(C.NPZ, "door_F4_kept.npz"))
        return rep
    ctl("a neglected door built with no notch (the kept copy read as the neglected one)", "WR:F4:notch", notch_off)
    caught = sum(1 for r in rows if r["caught"])
    return {"run": len(rows), "caught": caught, "rows": rows}
