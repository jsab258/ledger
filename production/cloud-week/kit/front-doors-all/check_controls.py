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
    shift_leaf = lambda n: n.startswith(("leaf_", "panel_", "moulding_", "bead_", "glass_light", "glass_slit", "glass_small", "net_", "iron_nail", "glass_lens", "iron_hinge", "iron_spyhole"))
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
    # ======================================================== try 2: the fresh reviews of 13 October (each wrong copy is the first build's fault, or what the review said was wrong)
    # ---- F7's boards shaded as rounded staves (the close review's fault): the .glb's own normals of one board tilted 17 degrees by the side of its face they stand on
    def staves():
        meshes, _ = C.cd.read_glb(os.path.join(C.ASSET, "door_F7.glb"))
        bad = {}
        for name, prims in meshes.items():
            if name == "leaf_board_3":
                prims2 = []
                for pr in prims:
                    P, Nn = pr["P"].copy(), pr["N"].copy()
                    front = Nn[:, 2] > 0.999                                   # glTF z is the street: the board's front face
                    xc = 0.5 * (P[front, 0].min() + P[front, 0].max())
                    t = np.radians(17.0)
                    sgn = np.where(P[front, 0] < xc, -1.0, 1.0)
                    Nn[front] = np.stack([sgn * np.sin(t), np.zeros(sgn.shape), np.cos(t) * np.ones(sgn.shape)], axis=1)
                    prims2.append({**pr, "N": Nn})
                bad[name] = prims2
            else:
                bad[name] = prims
        rep = new()
        C.row_flat_shading(rep, bad, "F7", "F7")
        return rep
    ctl("F7: board 3's front face shaded with the averaged normals of its V-joint chamfers (17 degrees off: rounded staves)", "GLB:F7:flat_faces_flat_shaded", staves)

    # ---- LP2's liner back at the first build's place, 0.5 in front of the face: its front face within 0.1 mm of the dished flap's middle
    def liner_back():
        parts = {n: (V.copy(), F) for n, (V, F) in furn_cache["LP2"].items()}
        V, F = parts["iron_letter_liner"]
        V[:, 1] -= 0.25e-3
        parts["iron_letter_liner"] = (V, F)
        rep = new()
        C.row_near_coplanar(rep, parts, "LP2")
        return rep
    ctl("LP2: the liner 0.25 mm further out (its front face 0.5 in front of the leaf's, as the first build had it)", "GLB:LP2:no_near_coplanar_faces", liner_back)

    # ---- the hinge-stile fitting left out
    def fixing(drop):
        rep = new()
        C.row_hinge_fixing(N, mods["T2"].copy_with(drop=drop), rep)
        return rep
    ctl("T2: the hinge-stile fitting left out (the first build)", "FU-T2-hinge_fixing", lambda: fixing(("iron_hinge_fixing_1", "iron_hinge_fixing_2")))
    ctl("T2: the hinge-stile fitting built as one box", "FU-T2-hinge_fixing", lambda: fixing(("iron_hinge_fixing_2",)))

    # ---- the keyhole's pocket: a kind with no pocket given a keyhole in the target
    def kh_pocket():
        Nx = copy.deepcopy(N)
        Nx["furniture"]["keyhole"]["KH1"]["place"]["F4"] = {"u": 782.8, "v": 1151.0}
        rep = new()
        C.row_kh_pocket(Nx, mods["F4"], rep)
        return rep
    ctl("F4: a sunk keyhole expected where the leaf has no pocket", "FU-F4-keyhole-pocket", kh_pocket)

    def kh_moved():
        Nx = copy.deepcopy(N)
        Nx["furniture"]["keyhole"]["KH1"]["place"]["F1"] = {"u": 700.0, "v": 1151.0}
        rep = new()
        C.row_kh_pocket(Nx, mods["F1"], rep)
        return rep
    ctl("F1: the keyhole expected 83 mm from where its pocket is cut", "FU-F1-keyhole-pocket", kh_moved)

    # ---- the notch: a crisp rectangle (the first build's) in place of the irregular worn edge
    def rectangle_notch():
        def rect(m):
            left = m.spec["leaf"]["lock_side"] == "right"
            return C.sbox(m.X0, m.Z0, m.X0 + 130.0, m.Z0 + 25.0) if left else C.sbox(m.X0 + m.W - 130.0, m.Z0, m.X0 + m.W, m.Z0 + 25.0)
        rep = new()
        C.notch_rows(N, rep, void_override=rect)
        return rep
    ctl("a neglected door's notch a crisp 130 x 25 rectangle (the first build's)", "WR:F4:notch", rectangle_notch)

    # ---- the glass and the materials
    def tinted():
        ms = copy.deepcopy(C.glb_materials(os.path.join(C.ASSET, "door_T2.glb"))[0])
        for n_ in ms:
            if n_ == "glass":
                ms[n_]["base"] = [C.bd.lin(121), C.bd.lin(131), C.bd.lin(139), 1.0]
        rep = new()
        C.glass_rows(rep, "T2", None, {}, mats=ms)
        return rep
    ctl("T2: the glass tinted dark blue-grey (121, 131, 139), the 3.1 kit's material", "GLB:T2:glass_clear", tinted)

    def reeded_plain():
        pj = json.load(open(os.path.join(C.NPZ, "door_F6.parts.json")))
        pj = {n: ({"material": "glass"} if n.startswith("glass_fanlight") else v) for n, v in pj.items()}
        rep = new()
        C.glass_rows(rep, "F6", os.path.join(C.ASSET, "door_F6.glb"), pj, expect_reeded=True)
        return rep
    ctl("F6: the reeded transom carrying the clear glass material (the first build)", "GLB:F6:reeded_glass_own_material", reeded_plain)

    def nets_white():
        pj = json.load(open(os.path.join(C.NPZ, "door_T2.parts.json")))
        pj = {n: ({"material": "net_white"} if n.startswith("net_") else v) for n, v in pj.items()}
        rep = new()
        C.glass_rows(rep, "T2", os.path.join(C.ASSET, "door_T2.glb"), pj, nets=True)
        return rep
    ctl("T2: the net cards in a plain net_white card (the first build)", "GLB:T2:nets_net_voile", nets_white)

    # ---- the pictures: the first build's own pictures are the wrong copies
    v1 = os.path.join(C.REPO, "production", "previews", "cloud-week", "front-doors-all")

    def dip_v1():
        rep = new()
        C.row_t3_street_dip(N, rep, os.path.join(v1, "T3-street-v1-2026-10-13.jpg"))
        return rep
    ctl("T3: the first build's street picture (outlines 3 mm deep over 14)", "PL-T3-street-dip", dip_v1)

    def nets_v1():
        rep = new()
        C.row_t2_nets_lit(N, rep, os.path.join(v1, "T2-street-v1-2026-10-13.jpg"))
        return rep
    ctl("T2: the first build's street picture (the nets slate grey)", "GA-T2-nets-lit", nets_v1)

    # ---- the profile, the thickness and the scraper as the first target had them
    def old_t3_profile():
        Nx = copy.deepcopy(N)
        old = [[0.0, 0.0], [2.0, 0.166], [4.0, 0.595], [6.0, 1.181], [8.0, 1.819], [10.0, 2.405], [12.0, 2.834], [14.0, 3.0], [76.0, 3.0]]
        Nx["kinds"]["T3"]["mouldings"]["outside"]["profile_dh"] = [q for q in old if q[0] <= 60.0] + [[60.0, 3.0], [76.0, 3.0]]
        rep = new()
        C.profile_rows(Nx, mods["T3"], rep)
        return rep
    ctl("T3: the first target's profile (steps 3 mm deep over 14) expected of the new leaf", "A4:T3:embossed_step", old_t3_profile)

    def f7_38():
        Nx = copy.deepcopy(N)
        Nx["kinds"]["F7"]["leaf"]["t"] = 38.0
        rep = new()
        C.row_DIM(Nx, C.Model(Nx, "F7", mods["F7"].M, mods["F7"].pivot), rep)
        return rep
    ctl("F7: a leaf 38 thick expected (the first target), 47 built", "DIM:F7:leaf_t", f7_38)

    def scraper_330():
        Nx = copy.deepcopy(N)
        for c in Nx["checks"]:
            if c["id"] == "FU-T1-scraper-BS1":
                c["expect"]["size"] = [330.0, 130.0, 200.0]
        rep = new()
        C.row_FU(Nx, "T1", houses_mods["T1"], rep)
        return rep
    ctl("T1: the scraper expected 330 long, the scrolls curling inward over the blade (the first build)", "FU-T1-scraper-BS1", scraper_330)

    # ---- the street: the neighbours and the numbers
    def teal_beside_green(Hx):
        b = {h["house"]: h for h in Hx["houses"]}
        b["west_north_bay1"]["paint"] = "dark_green"
    pj_ = None

    def extra(mutate=None, numbers=None):
        Hx = copy.deepcopy(H)
        if mutate:
            mutate(Hx)
        rep = new()
        C.row_street_extra(N, Hx, rep, numbers)
        return rep
    ctl("F3 dark green beside F7 deep teal (the first table)", "AD-neighbours-deltaE", lambda: extra(teal_beside_green))

    def twin_f1(Hx):
        b = {h["house"]: h for h in Hx["houses"]}
        b["west_north_bay0"]["paint"] = b["east_parade_bay0"]["paint"]
    ctl("two F1 houses in the same maroon (the first table)", "AD-same-kind-other-paint", lambda: extra(twin_f1))
    ctl("a 246 on the east side (the first numbers: 34, 21, 15 on one side)", "AD-numbers", lambda: extra(None, {"NM1:T1": "34", "NM1:F2": "246", "NM6:T2": "21", "NM3:F3": "15"}))
    ctl("odd and even mixed on the west side", "AD-numbers", lambda: extra(None, {"NM1:T1": "17", "NM1:F2": "14", "NM6:T2": "22", "NM3:F3": "29"}))
    ctl("the west numbers falling from the quay", "AD-numbers", lambda: extra(None, {"NM1:T1": "29", "NM1:F2": "14", "NM6:T2": "21", "NM3:F3": "17"}))

    # ---- try 3 (14 Oct): the rows the second fresh reviews asked for, each with a wrong copy that must fail it
    def t3_house(kind):
        rec = copy.deepcopy([h for h in H["houses"] if h["kind"] == kind][0])
        return C.assemble(N, mods[kind], rec, furn_cache)

    def grip_close():
        m = t3_house("T2")
        V, F = m.M["fit:handle:iron_pull_bar"]
        m.M["fit:handle:iron_pull_bar"] = (V + np.array([0.0, 0.0095, 0.0]), F)         # the grip 9.5 mm nearer the face: 20.5 clear, the first build's stand-off
        rep = new()
        C.row_try3_FU(N, "T2", m, rep)
        return rep
    ctl("T2: the bar pull's grip 9.5 mm nearer the face (20.5 clear, the first build)", "FU-T2-grip_gap", grip_close)

    def bow_close():
        m = t3_house("F7")
        V, F = m.M["fit:handle:iron_latch_bow"]
        m.M["fit:handle:iron_latch_bow"] = (V + np.array([0.0, 0.0095, 0.0]), F)
        rep = new()
        C.row_try3_FU(N, "F7", m, rep)
        return rep
    ctl("F7: the thumb latch's bow 9.5 mm nearer the plate", "FU-F7-grip_gap", bow_close)

    def thumb_flat():
        m = t3_house("F7")
        py = float(m.M["fit:handle:iron_latch_plate"][0][:, 1].min())
        V, F = m.M["fit:handle:iron_latch_thumb"]
        V2 = V.copy()
        V2[:, 1] = py - 0.005 + (V[:, 1] - V[:, 1].mean()) * 0.1                        # an upright lever: 5 mm out from the plate (the first build's reached 13.7)
        m.M["fit:handle:iron_latch_thumb"] = (V2, F)
        rep = new()
        C.row_try3_FU(N, "F7", m, rep)
        return rep
    ctl("F7: an upright thumb lever (5 mm out from the plate)", "FU-F7-thumb", thumb_flat)

    def thumb_high():
        m = t3_house("F7")
        V, F = m.M["fit:handle:iron_latch_thumb"]
        m.M["fit:handle:iron_latch_thumb"] = (V + np.array([0.0, 0.0, 0.020]), F)       # the lever 20 mm higher: it rises over 15 above its slot and lands on the bow
        rep = new()
        C.row_try3_FU(N, "F7", m, rep)
        return rep
    ctl("F7: the thumb lever 20 mm higher (rises more than 15 above its slot)", "FU-F7-thumb", thumb_high)

    def scraper_old():
        Nx = copy.deepcopy(N)
        Nx["furniture"]["scraper"]["BS1"]["standard_profile_xz"] = [[25.0, 0.0], [0.0, 0.0], [0.0, 154.0], [0.0, 169.0], [5.8, 185.8], [18.8, 197.0], [35.0, 200.0], [49.8, 194.7], [59.5, 183.2], [62.0, 169.0],
                                                                    [57.2, 156.2], [47.2, 147.9], [35.0, 146.0], [35.0, 158.0], [41.2, 158.3], [46.8, 162.2], [50.0, 169.0], [49.1, 177.2], [43.8, 184.3], [35.0, 188.0],
                                                                    [24.8, 186.6], [16.2, 179.8], [12.0, 169.0], [25.0, 154.0]]
        m = t3_house("T1")
        rep = new()
        C.row_try3_FU(Nx, "T1", m, rep)
        return rep
    ctl("T1: the scraper's scroll as the first target had it (a point every 30 degrees, 16 mm facets), 7.5 degrees built", "FU-T1-scraper-facets", scraper_old)

    def quirk_wide():
        Nx = copy.deepcopy(N)
        [c.update({"expect": dict(c["expect"], width=8.0)}) for c in Nx["checks"] if c["id"] == "PL-T3-quirk"]
        rep = new()
        C.row_quirk(Nx, mods["T3"], rep)
        return rep
    ctl("T3: a quirk 8 wide expected, 5 built", "PL-T3-quirk", quirk_wide)

    def quirk_deep():
        Nx = copy.deepcopy(N)
        [c.update({"expect": dict(c["expect"], depth=5.0)}) for c in Nx["checks"] if c["id"] == "PL-T3-quirk"]
        rep = new()
        C.row_quirk(Nx, mods["T3"], rep)
        return rep
    ctl("T3: a quirk 5 deep expected, 3 built", "PL-T3-quirk", quirk_deep)

    def quirk_none():
        Nx = copy.deepcopy(N)
        Nx["kinds"]["T3"]["mouldings"]["outside"]["quirk"]["gap_to_outline"] = 4.0     # the probes read 4 mm further out: off the groove
        rep = new()
        C.row_quirk(Nx, mods["T3"], rep)
        return rep
    ctl("T3: the quirk expected 4 mm off the outline", "PL-T3-quirk", quirk_none)

    def chrome_old():
        rep = new()
        C.row_chrome(N, rep, want=[170, 170, 168])
        return rep
    ctl("chrome_nickel expected at (170, 170, 168), (196, 197, 196) built", "MAT-chrome_nickel", chrome_old)

    def no_guard():
        rep = new()
        C.row_makers_frozen(N, rep, texts={"make_target.py": "def main(): pass\nif __name__ == '__main__': main()\n", "make_doc.py": "def main(): pass\n"})
        return rep
    ctl("the target's makers without their guard", "TG-makers-frozen", no_guard)

    def dip_v2():
        rep = new()
        C.row_t3_street_dip(N, rep, os.path.join(v1, "T3-street-v2-2026-10-13.jpg"))
        return rep
    ctl("T3: the second build's street picture (left-hand outlines 1 to 2 per cent)", "PL-T3-street-dip", dip_v2)

    def nets_v2():
        rep = new()
        C.row_t2_nets_lit(N, rep, os.path.join(v1, "T2-street-v2-2026-10-13.jpg"))
        return rep
    ctl("T2: the second build's street picture (the nets read 0.95 to 1.0 of the transom bar)", "GA-T2-nets-lit", nets_v2)

    caught = sum(1 for r in rows if r["caught"])
    return {"run": len(rows), "caught": caught, "rows": rows}
