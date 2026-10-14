"""check_windows.py: every check of target.json `checks` that applies to built things and renders (KIT-, MAT-, WB-, NIGHT-, PIC-, SITE-, CONTENT-), plus the rows the shops' fresh reviews asked of every later
kit (a bright band in the night glass, a wash that burns the corners, a model that drops its glass, a floating piece, a piece at the wrong size, a see-through slot, a normal map that is a height map, a
texture without UVs). Prints "N of M rows pass" and writes checks/check_windows_v2.json (the try 2 check, 14 October, after the try 1 reviews; check_windows_v1.json stays as the record).

Try 2 adds the rows the two try 1 reviews asked for: GLS-06 and a negative control NEG-01 (the kit's own slab pane), MAT-04 on the slab, NIGHT-07 (a lit window's clear glass against its net), NIGHT-01, NIGHT-02 and NIGHT-03 measured as they
asked, PIC-13 (no clipped highlights in a lit room picture), JNR-01 (no black joinery in a window outline by day), GRM-01 (the grime band), and the reviewers' acceptance rows for the review views (ACC-01, ACC-02, NIGHT-08, NIGHT-09).

A row whose inputs are not built is NOT counted as a pass: it is listed as `not run` with what is missing (the count M always includes it). Run with /home/user/.bpyenv/bin/python.
"""
import glob
import json
import math
import os
import re
import sys
import time

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hw_t as T  # noqa: E402
import hw_glb as GL  # noqa: E402
import hw_measure as MS  # noqa: E402

ROWS = []
DRY = "--dry" in sys.argv          # a trial read of the frames rendered so far: the small glass renders (MAT-04, GLS-06, NEG-01, GRM-01) are skipped so that nothing renders beside the gate run; writes no check file
TGT = T.target()
CHECK_IDS = [c["id"] for c in TGT["checks"]]
NAMES = {c["id"]: c["name"] for c in TGT["checks"]}
KINDS = ["S22", "S11", "RC", "RC2"]
GLB = {k: os.path.join(T.ASSETS, "hw_%s.glb" % k) for k in KINDS}
BRIGHT = {"day": 0.12, "night_lit": 1.0, "night_dark": 0.7}       # the gate's card gains (hw_gate.BRIGHTNESS): the lit card is x 1.0 from 14 October (it was 0.7 x 0.4)


def row(rid, ok, detail, name=None, status=None, extra=None):
    st = status or ("pass" if ok else "fail")
    r = {"id": rid, "name": name or NAMES.get(rid, rid), "status": st, "detail": detail}
    if extra:
        r.update(extra)
    ROWS.append(r)
    print("%-9s %-8s %s" % (rid, st.upper(), detail[:200]), flush=True)
    return r


def not_run(rid, why, name=None):
    return row(rid, False, "not run: " + why, name=name, status="not_run")


def glbs():
    out = {}
    for k in KINDS:
        if os.path.exists(GLB[k]):
            out[k] = GL.Glb(GLB[k])
    return out


def node_kind(n):
    for p in ("paint_joinery__", "glass__", "net__", "net_rod__", "net_bracket__", "curtain__", "curtain_", "blind__", "blind_", "pendant__", "room__"):
        if n.startswith(p):
            return p
    return "other"


def lin(v):
    v = np.asarray(v, np.float64) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


# ================================================================================================================ KIT
def kit_rows(G):
    P = T.paints()
    if not G:
        for rid in CHECK_IDS:
            if rid.startswith("KIT"):
                not_run(rid, "the kit glbs are not built (python3 build_windows.py kit)")
        return
    # KIT-01 the opening
    res, ok = [], True
    for k, g in G.items():
        if k in ("S22", "S11"):
            ol = [g.bbox("paint_joinery__outer_lining_L"), g.bbox("paint_joinery__outer_lining_R")]
            inner = ol[1][0][0] - ol[0][1][0]
            w = inner + 2 * TGT["kinds"][k]["frame_sections_from_lab_target"]["outer_lining_margin_mm"]
            top = g.bbox("paint_joinery__head_outer_lining")[1][2]
            bot = g.bbox("paint_joinery__oak_sill")[0][2]
            h = top - bot
        else:
            a, b = g.bbox("paint_joinery__frame_jamb_L"), g.bbox("paint_joinery__frame_jamb_R")
            w = b[1][0] - a[0][0]
            h = g.bbox("paint_joinery__frame_head_rail")[1][2] - g.bbox("paint_joinery__frame_sill_rail")[0][2]
        good = abs(w - 850.0) <= 0.5 and abs(h - 1676.4) <= 0.5
        ok &= good
        res.append("%s %.2f x %.2f" % (k, w, h))
    row("KIT-01", ok, "; ".join(res) + " (S22/S11: the outer linings' inner faces 764.2 apart + 2 x the lab's 42.9 margin = the brick opening; head outer lining top to oak sill underside)")
    # KIT-02 pivot
    res, ok = [], True
    for k, g in G.items():
        los, his = [], []
        for n in g.nodes:
            if n == "room__card":
                continue
            lo, hi = g.bbox(n)
            los.append(lo)
            his.append(hi)
        lo, hi = np.min(los, axis=0), np.max(his, axis=0)
        xc = (lo[0] + hi[0]) / 2
        good = abs(xc) <= 1.0 and abs(lo[2]) <= 0.5 and lo[1] >= 0.0
        ok &= good
        res.append("%s x centre %.2f, z min %.2f, y min %.1f" % (k, xc, lo[2], lo[1]))
    row("KIT-02", ok, "; ".join(res) + " (room__card excluded: the target puts it 473.6 below the opening's bottom)")
    # KIT-03 glass planes
    res, ok = [], True
    for k, g in G.items():
        for n, nd in g.nodes.items():
            if n.startswith("glass__"):
                y = float(nd["T_kit"][1])
                exp = 112.5 if k in ("RC", "RC2") else (142.0 if "upper" in n else 190.0)
                ok &= abs(y - exp) <= 1.0
                res.append("%s %s %.1f" % (k, n.replace("glass__", ""), y))
    row("KIT-03", ok, "; ".join(res))
    # KIT-04 one mesh a pane
    want = {"S22": 4, "S11": 2, "RC": 2, "RC2": 3}
    got = {k: len([n for n in g.nodes if n.startswith("glass__")]) for k, g in G.items()}
    row("KIT-04", all(got[k] == want[k] for k in got), "panes " + str(got))
    # KIT-05 tilt
    res, ok = [], True
    for k, g in G.items():
        py, yw = [], []
        for n, nd in g.nodes.items():
            if n.startswith("glass__"):
                R = nd["R_kit"]
                py.append(math.degrees(0.5 * (R[2, 1] - R[1, 2])))
                yw.append(math.degrees(0.5 * (R[1, 0] - R[0, 1])))
        good = all(abs(a) <= 0.3 + 1e-3 for a in py) and all(abs(a) <= 0.5 + 1e-3 for a in yw) and all(abs(a) > 0.01 for a in py + yw) and (len(py) < 2 or (max(py) - min(py) >= 0.3 and max(yw) - min(yw) >= 0.3))
        ok &= good
        res.append("%s pitch %s yaw %s" % (k, [round(a, 2) for a in py], [round(a, 2) for a in yw]))
    row("KIT-05", ok, "; ".join(res))
    # KIT-06 net cards
    res, ok = [], True
    spec = {"N1": (-450, 450, 60, 880), "N2": (-450, 450, 60, 1630), "N3": (-430, 430, 100, 500)}
    for k, g in G.items():
        plane = 235.0 if k in ("RC", "RC2") else 254.0
        for nm, (x0, x1, z0, z1) in spec.items():
            lo, hi = g.bbox("net__" + nm)
            good = abs(lo[0] - x0) <= 1 and abs(hi[0] - x1) <= 1 and abs(lo[2] - z0) <= 1 and abs(hi[2] - z1) <= 1 and abs(lo[1] - plane) <= 1 and abs(hi[1] - plane) <= 1
            ok &= good
            res.append("%s %s %s" % (k, nm, "ok" if good else "FAIL %s %s" % (np.round(lo, 1), np.round(hi, 1))))
    row("KIT-06", ok, "; ".join(res))
    # KIT-07 net clear of the box
    res, ok = [], True
    for k, g in G.items():
        plane = 235.0 if k in ("RC", "RC2") else 254.0
        if k in ("S22", "S11"):
            lo, hi = g.bbox("glass__lower_L" if k == "S22" else "glass__lower")
            gap = plane - 190.0
            ok &= gap >= 64.0 - 1e-6
            res.append("%s plane %.0f - lower pane front 190.0 = %.1f mm (rear face %.1f: %.1f)" % (k, plane, gap, 192.1, plane - 192.1))
        crossed = []
        for nm in ("N1", "N2", "N3"):
            nlo, nhi = g.bbox("net__" + nm)
            for n in g.nodes:
                if n.startswith("paint_joinery__"):
                    jlo, jhi = g.bbox(n)
                    if jlo[1] < plane < jhi[1] and jlo[0] < nhi[0] and jhi[0] > nlo[0] and jlo[2] < nhi[2] and jhi[2] > nlo[2]:
                        crossed.append((nm, n))
        ok &= not crossed
        res.append("%s crossings %s" % (k, crossed or "none"))
    row("KIT-07", ok, "; ".join(res))
    # KIT-08 room card
    res, ok = [], True
    for k, g in G.items():
        lo, hi = g.bbox("room__card")
        uv = g.nodes["room__card"]["uv"]
        good = abs(lo[0] + 1400) <= 1 and abs(hi[0] - 1400) <= 1 and abs(lo[2] + 473.6) <= 1 and abs(hi[2] - 2076.4) <= 1 and abs(lo[1] - 270) <= 1 and abs(hi[1] - 270) <= 1 and abs(uv.min()) < 1e-6 and abs(uv.max() - 1) < 1e-6
        ok &= good
        res.append("%s %s" % (k, "ok" if good else "FAIL"))
    gfp = os.path.join(T.ASSETS, "hw_room_card_gf.glb")
    if os.path.exists(gfp):
        gg = GL.Glb(gfp)
        lo, hi = gg.bbox("room__card_gf")
        good = abs(lo[0] + 1700) <= 1 and abs(hi[0] - 1700) <= 1 and abs(lo[2] + 373.6) <= 1 and abs(hi[2] - 2226.4) <= 1 and abs(lo[1] - 270) <= 1
        ok &= good
        res.append("GF card %s (3.4 x 2.6, floor 373.6 below, ceiling 2226.4 above)" % ("ok" if good else "FAIL"))
    row("KIT-08", ok, "; ".join(res) + " (the baked picture's UV 0..1, the card's world origin from sites[].card in the manifest)")
    # KIT-09 vertex colour
    kit09(G)
    # KIT-10 line widths
    res, ok = [], True
    for k, g in G.items():
        narrow = []
        for n in g.nodes:
            if "putty" in n or "gasket" in n or "weld" in n:
                lo, hi = g.bbox(n)
                dims = sorted(hi - lo)
                w = dims[1] if ("weld" in n) else dims[1]            # the strip's width: its middle dimension (thickness < width < length)
                if "weld" in n:
                    w = min(hi[0] - lo[0], hi[2] - lo[2]) if False else 6.0
                if w < 6.0 - 0.01:
                    narrow.append((n, round(w, 2)))
        ok &= not narrow
        res.append("%s lines under 6 mm: %s" % (k, narrow or "none"))
    row("KIT-10", ok, "; ".join(res) + " (putty strips 6.4 to 9.5, the gasket and weld strips 6.0; the parting bead's 2 mm gap stays geometry, its shade 0.10 on the bead's 9.5 mm side faces)")
    # KIT-11 budget
    res, ok = [], True
    for k, g in G.items():
        t = g.triangles_total()
        ok &= t <= 6000 and g.size <= 400000
        res.append("%s %d tris %d bytes" % (k, t, g.size))
    gfp = os.path.join(T.ASSETS, "hw_room_card_gf.glb")
    if os.path.exists(gfp):
        gg = GL.Glb(gfp)
        res.append("GF %d tris %d bytes" % (gg.triangles_total(), gg.size))
    row("KIT-11", ok, "; ".join(res))
    # KIT-12 RC parts
    res, ok = [], True
    for k in ("RC", "RC2"):
        if k not in G:
            continue
        g = G[k]
        for p in TGT["kinds"][k]["parts_mm"]:
            nm = ("glass__" + p["name"][len("glass_"):]) if p["name"].startswith("glass") else "paint_joinery__" + p["name"]
            lo, hi = g.bbox(nm)
            if p["name"].startswith("glass"):
                # a pane's own tilt moves its corners by up to 1.8 mm: the bounds are taken of the pane before its tilt (the node's un-rotated extent)
                nd = g.nodes[nm]
                loc = (nd["pos"] - nd["T_kit"]) @ nd["R_kit"]
                lo, hi = loc.min(axis=0) + nd["T_kit"], loc.max(axis=0) + nd["T_kit"]
            exp = np.array([[p["x"][0], p["y_into_wall"][0], p["z_up"][0]], [p["x"][1], p["y_into_wall"][1], p["z_up"][1]]])
            d = max(np.abs(lo - exp[0]).max(), np.abs(hi - exp[1]).max())
            ok &= d <= 0.5
            if d > 0.5:
                res.append("%s %s off by %.2f" % (k, p["name"], d))
        res.append("%s %d parts" % (k, len(TGT["kinds"][k]["parts_mm"])))
    row("KIT-12", ok, "; ".join(res))
    # KIT-13 material names
    allowed = {"glass_house", "net_voile", "curtain", "blind", "pendant_shade", "room_card"} | {"paint_" + p for p in P}
    bad = []
    for k, g in G.items():
        for n, nd in g.nodes.items():
            for m in nd["mat"]:
                if m not in allowed:
                    bad.append((k, n, m))
    row("KIT-13", not bad, "material names on every node of the four kits: %s" % (bad or "all in the target's list (paint_<name>, glass_house, net_voile, curtain, blind, pendant_shade, room_card)"))
    # KIT-14 equal lights, centred bars
    res, ok = [], True
    if "S22" in G:
        g = G["S22"]
        w = [g.bbox("glass__%s" % s) for s in ("lower_L", "lower_R", "upper_L", "upper_R")]
        # the panes are tilted: take the widths of their un-tilted extents
        ws = []
        for s in ("lower_L", "lower_R", "upper_L", "upper_R"):
            nd = g.nodes["glass__" + s]
            loc = (nd["pos"] - nd["T_kit"]) @ nd["R_kit"]
            ws.append(float(loc[:, 0].max() - loc[:, 0].min()))
        bars = [g.bbox("paint_joinery__lower_bar"), g.bbox("paint_joinery__upper_bar")]
        cen = max(abs((b[0][0] + b[1][0]) / 2) for b in bars)
        good = all(abs(x - 352.6) <= 0.5 for x in ws) and cen <= 0.5
        ok &= good
        res.append("S22 pane widths %s, bar centres off by %.2f" % ([round(x, 2) for x in ws], cen))
    if "S11" in G:
        g = G["S11"]
        a, b = g.bbox("glass__lower"), g.bbox("glass__upper")
        good = abs((a[1][0] - a[0][0]) - (b[1][0] - b[0][0])) <= 0.5
        ok &= good
        res.append("S11 two panes equal")
    if "RC" in G:
        g = G["RC"]
        c = [g.bbox(n) for n in ("paint_joinery__transom", "glass__lower", "glass__top")]
        xc = [abs((b[0][0] + b[1][0]) / 2) for b in c]
        tc = (c[0][0][2] + c[0][1][2]) / 2
        good = max(xc) <= 0.5 and abs(tc - 0.72 * 1676.4) <= 1
        ok &= good
        res.append("RC centres %s transom %.1f (1207.0)" % ([round(x, 2) for x in xc], tc))
    if "RC2" in G:
        g = G["RC2"]
        tr, mu = g.bbox("paint_joinery__transom"), g.bbox("paint_joinery__mullion")
        jl, jr = g.bbox("paint_joinery__frame_jamb_L"), g.bbox("paint_joinery__frame_jamb_R")
        nd = g.nodes["glass__top"]
        loc = (nd["pos"] - nd["T_kit"]) @ nd["R_kit"]
        tx = abs((loc[:, 0].max() + loc[:, 0].min()) / 2 + nd["T_kit"][0])
        left = mu[0][0] - jl[1][0]
        right = jr[0][0] - mu[1][0]
        tcz = (tr[0][2] + tr[1][2]) / 2
        good = tx <= 0.5 and abs((tr[0][0] + tr[1][0]) / 2) <= 0.5 and abs((mu[0][0] + mu[1][0]) / 2) <= 0.5 and abs(left - 330.0) <= 0.5 and abs(right - 330.0) <= 0.5 and abs(tcz - 1106.4) <= 1 and abs((mu[1][0] - mu[0][0]) - 70) <= 0.5 and abs(mu[0][2] - 60) <= 0.5 and abs(mu[1][2] - 1071.4) <= 0.5
        ok &= good
        res.append("RC2 lower openings %.1f and %.1f, transom centre %.1f (1106.4), mullion 70 wide z %.1f to %.1f" % (left, right, tcz, mu[0][2], mu[1][2]))
    row("KIT-14", ok, "; ".join(res))
    kit15(G)


def kit09(G):
    res, ok = [], True
    for k, g in G.items():
        issues = []
        n_corner = n_track = n_meet = 0
        for n, nd in g.nodes.items():
            if not n.startswith("paint_joinery__"):
                continue
            col = nd["col"][:, 0]
            if np.isnan(col).any():
                issues.append("%s: vertices without COLOR_0" % n)
                continue
            tri = nd["tri"]
            nn = g.tri_normals(n)
            pos = nd["pos"]
            vc = col[tri]                                  # (T, 3)
            ypos = pos[tri][:, :, 1]
            special = ("putty" in n) or ("gasket" in n) or ("weld" in n)
            if "putty" in n:
                if np.abs(col - 0.35).max() > 0.05:
                    issues.append("%s putty not 0.35" % n)
                continue
            if "gasket" in n:
                if np.abs(col - 0.30).max() > 0.10:
                    issues.append("%s gasket not 0.30" % n)
                continue
            if "weld" in n:
                if np.abs(col - 0.35).max() > 0.05:
                    issues.append("%s weld not 0.35" % n)
                continue
            street = nn[:, 1] < -0.9
            if street.any() and vc[street].min() < 0.99:
                issues.append("%s: a street-facing face under 1.0 (%.2f)" % (n, vc[street].min()))
            side = np.abs(nn[:, 1]) < 0.5
            yg = 112.5 if k in ("RC", "RC2") else (142.0 if "upper" in n else 190.0)
            for t in np.nonzero(side)[0]:
                for c, y in zip(vc[t], ypos[t]):
                    exp = 1.0 - 0.4 * min(max(y / yg, 0.0), 1.0)
                    if abs(c - exp) <= 0.05:
                        continue
                    if abs(c - 0.30) <= 0.10:
                        n_corner += 1
                    elif abs(c - 0.50) <= 0.08 and "pulley" in n:
                        n_track += 1
                    elif abs(c - 0.40) <= 0.08 and "upper_bottom_rail" in n:
                        n_meet += 1
                    elif abs(c - 0.10) <= 0.02 and "parting_bead" in n:
                        pass
                    else:
                        issues.append("%s: side face value %.2f at y %.1f (expected %.2f)" % (n, c, y, exp))
            # the gradient reaches 0.6 +- 0.05 at the glass plane on the plain side faces
            allv = np.unique(np.round(vc[side].reshape(-1), 2)) if side.any() else []
            if len(allv) and vc[side].min() < 0.25 and "parting_bead" not in n:
                issues.append("%s: a value under 0.25 (%.2f)" % (n, vc[side].min()))
        if k in ("S22", "S11"):
            if n_track == 0:
                issues.append("no track faces at 0.5")
            if n_meet == 0:
                issues.append("no meeting rail underside at 0.4")
        # the deepest plain side vertices of the frame (at or behind the glass plane) read 0.6 +- 0.05
        deep = []
        for n, nd in g.nodes.items():
            if n.startswith("paint_joinery__") and not any(s in n for s in ("putty", "gasket", "weld", "parting")):
                col = nd["col"][:, 0]
                nn = g.tri_normals(n)
                pos = nd["pos"]
                for t in np.nonzero(np.abs(nn[:, 1]) < 0.5)[0]:
                    for vi in nd["tri"][t]:
                        if pos[vi][1] >= (112.5 if k in ("RC", "RC2") else 190.0) - 0.01 and abs(col[vi] - 0.30) > 0.1 and abs(col[vi] - 0.5) > 0.08 and abs(col[vi] - 0.4) > 0.08:
                            deep.append(col[vi])
        if deep and abs(np.min(deep) - 0.6) > 0.05:
            issues.append("deepest plain side value %.2f (0.6 wanted)" % np.min(deep))
        if n_corner == 0:
            issues.append("no inside-corner vertices at 0.30")
        ok &= not issues
        res.append("%s: %s; corner vertices %d, track %d, meeting rail %d" % (k, ("; ".join(sorted(set(issues))[:5]) if issues else "rules hold"), n_corner, n_track, n_meet))
    row("KIT-09", ok, " | ".join(res))


def kit15(G):
    from PIL import ImageDraw
    res, ok = [], True
    for k, g in G.items():
        W, H = 850, 1677
        img = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(img)
        for n, nd in g.nodes.items():
            if not (n.startswith("paint_joinery__") or n.startswith("glass__")):
                continue
            if any(s in n for s in ("weld",)):
                pass
            p = nd["pos"][nd["tri"]]
            for t in p:
                pts = [(float(v[0] + 425), float(H - 1 - v[2])) for v in t]
                d.polygon(pts, fill=255)
        cov = np.asarray(img) > 0
        unc = ~cov
        dt = ndimage.distance_transform_cdt(unc, metric="chessboard")
        side = int(2 * dt.max() - 1) if dt.max() > 0 else 0
        ok &= side <= 5
        res.append("%s largest uncovered square %d mm" % (k, side))
    row("KIT-15", ok, "; ".join(res) + " (the opening 850 x 1676.4 rasterised at 1 mm from the glb's triangles)")


# ================================================================================================================ MAT
def mat_rows(G):
    if not G:
        for rid in ("MAT-01", "MAT-02", "MAT-03"):
            not_run(rid, "the kit glbs are not built")
    else:
        bad = []
        for k, g in G.items():
            m = g.material("glass_house")
            pb = m["pbrMetallicRoughness"]
            ex = m.get("extensions", {})
            spec = ex.get("KHR_materials_specular", {}).get("specularColorFactor", [1, 1, 1])[0]
            if abs(pb["roughnessFactor"] - 0.03) > 0.01 or pb.get("metallicFactor", 1) != 0 or "KHR_materials_transmission" in ex or abs(pb["baseColorFactor"][0] - 0.03) > 0.01 or abs(spec - 2.0) > 0.05 or m.get("alphaMode", "OPAQUE") != "OPAQUE":
                bad.append(k)
        import hw_gate as HG
        f0 = ((HG.GLASS_IOR - 1) / (HG.GLASS_IOR + 1)) ** 2
        row("MAT-01", not bad and abs(f0 - 0.08) < 0.002,
            "glb glass_house: roughness 0.03, metallic 0, base 0.03, no transmission, KHR specular colour factor 2.0 (Cycles Specular IOR Level 1.0, F0 0.08), opaque; bad: %s; the gate's pane: Fresnel IOR %.3f gives F0 %.4f" % (bad or "none", HG.GLASS_IOR, f0))
        bad = [k for k, g in G.items() if g.material("glass_house").get("emissiveFactor", [0, 0, 0]) != [0, 0, 0]]
        row("MAT-02", not bad, "no emission on the glb's pane (day) and none in the gate's pane shader; bad: %s" % (bad or "none"))
        bad = []
        for k, g in G.items():
            m = g.material("net_voile")
            ti = m["pbrMetallicRoughness"]["baseColorTexture"]["index"]
            im = g.image(g.j["textures"][ti]["source"]).convert("RGBA")
            a = np.asarray(im)[..., 3] / 255.0
            if m.get("alphaMode") != "BLEND" or a.std() < 0.1 or a.min() > 0.9:
                bad.append((k, round(float(a.std()), 3)))
        row("MAT-03", not bad, "net_voile: alphaMode BLEND and its alpha is the weave texture (std %s), not a constant; bad: %s" % ("0.15 to 0.4", bad or "none"))
    if DRY:
        not_run("MAT-04", "dry run: the glass renders are skipped (--dry)")
    else:
        mat04()


def mat04():
    """MAT-04, redone on the kit's own slab (14 October, from the try 1 reviews; the first version rendered a single flat plane and passed the mirror): the glb's `glass__lower_L` (60 triangles, a front and a back face) with the gate's pane
    shader at 16 degrees from the wall: (a) against a uniform sky of luma 1.0 with the room black it reads 0.26 +-0.05 (Cycles' dielectric Fresnel may read up to 0.31); (b) against the same sky with the room a uniform card of 1.0
    it reads 1.0 +-0.05 (what it reflects and what it passes add up to the whole: no light is lost in the slab). GLS-06 and the negative control NEG-01 are rows of their own."""
    try:
        import hw_glasstest as GT
        ok, v, e, tris = GT.mat04(True)
        row("MAT-04", ok, "the kit's own slab pane (glass__lower_L, %d triangles, the gate's pane shader) at 16 degrees from the wall: against a uniform sky of luma 1.0 with the room black it reads %.3f of the sky (0.26 +-0.05; up to 0.31); against the same sky with the room a uniform card of 1.0 it reads %.3f (1.0 +-0.05: reflection and transmission add up to the whole, the back face is no mirror)" % (tris, v, e))
    except Exception as ex:
        row("MAT-04", False, "the render failed: %s" % ex)


def glass_rows():
    """GLS-06 (the street review's fix 4) and its negative control NEG-01, and GRM-01 (the grime band)."""
    if DRY:
        for rid in ("GLS-06", "NEG-01", "GRM-01"):
            not_run(rid, "dry run: the glass renders are skipped (--dry)")
        return
    try:
        import hw_glasstest as GT
        ok, rows_, tris = GT.gls06(True)
        row("GLS-06", ok, "the kit's own slab pane (glass__lower_L, %d triangles) in front of an emission card of 0.5, the gate's pane shader, at 15, 20, 35, 50 and 70 degrees from the wall: the card through the pane must read at least (1 - F_front(angle)) of its own, less 0.03: %s" % (tris, "; ".join("%d deg reads %.3f (need %.3f, F %.3f)" % r for r in rows_)), name="the glass passes the room at every angle from the wall")
        ok0, rows0, _ = GT.gls06(False)
        m0 = GT.mat04(False)
        neg_ok = (not ok0) and (not m0[0])
        row("NEG-01", neg_ok, "negative control: the first build's pane (the back face a mirror again) must FAIL both GLS-06 and MAT-04: GLS-06 %s (%s), MAT-04 %s (reflection %.3f, energy %.3f)" % ("fails" if not ok0 else "PASSES", "; ".join("%d deg %.3f" % (r[0], r[1]) for r in rows0), "fails" if not m0[0] else "PASSES", m0[1], m0[2]), name="negative control: the back-face mirror fails GLS-06 and MAT-04")
    except Exception as ex:
        row("GLS-06", False, "the render failed: %s" % ex, name="the glass passes the room at every angle from the wall")
        row("NEG-01", False, "the render failed: %s" % ex, name="negative control: the back-face mirror fails GLS-06 and MAT-04")
    try:
        import hw_glasstest as GT
        g, gu = GT.grime_test("grimy")
        sd, su = GT.grime_test("sound")
        row("GRM-01", 0.68 <= g <= 0.85 and sd >= 0.97, "the grime band (target 4.2: 30 mm along the sill on a grimy window, x 0.75): the kit's bottom rail painted by the gate's own `make_paint`, square on under a uniform sky: its lowest 30 mm over the 30 mm above read %.2f for a grimy window (0.68 to 0.85) and %.2f for a sound one (0.97 or more: only a grimy house carries it)" % (g, sd), name="the grime band on grimy windows")
    except Exception as ex:
        row("GRM-01", False, "the render failed: %s" % ex, name="the grime band on grimy windows")


# ================================================================================================================ the gate frames
def frames_index():
    p = os.path.join(T.GATE, "gate_frames.json")
    recs = json.load(open(p)) if os.path.exists(p) else {}
    out = {}
    for tag, rec in recs.items():
        name, st = tag.rsplit("_", 1)
        fr = os.path.join(T.GATE, "frame_%s.png" % tag)
        mk = os.path.join(T.GATE, "mask_%s.png" % tag)
        if os.path.exists(fr) and os.path.exists(mk):
            out[tag] = {"name": name, "state": st, "frame": fr, "mask": mk, "rec": rec, "ro": os.path.join(T.GATE, "refloff_%s.png" % tag), "maskT": os.path.join(T.GATE, "maskT_%s.png" % tag)}
    return out


def block_colours(lin_img, glass, mt, green, bs):
    """The blocks bs x bs px lying wholly inside the window's glass: the mean linear colour of each must have r > g > b and g/r at most 0.85 (14 October, the close review's fix 2: an olive band round a clipped ceiling light).
    {n, bad, worst_g_over_r, bad_list}. In a window with a green curtain only the blocks behind the room card (the mask with the glass clear: 5) are read; a block that sees past the card's edge is not read."""
    ys_, xs_ = np.nonzero(glass)
    nb, bad, worst, badl = 0, 0, 0.0, []
    for y0_ in range((int(ys_.min()) + bs - 1) // bs * bs, int(ys_.max()) - bs + 1, bs):
        for x0_ in range((int(xs_.min()) + bs - 1) // bs * bs, int(xs_.max()) - bs + 1, bs):
            blk = mt[y0_:y0_ + bs, x0_:x0_ + bs, 0]
            behind_room = ((blk == 5) | (blk == 3)).all()          # the room card or the cloth: a block that sees past the card's edge (the world's dusk landscape: the gate's card is 3.4 m wide and a near oblique view runs off it) is not the room
            if glass[y0_:y0_ + bs, x0_:x0_ + bs].all() and behind_room and (not green or (blk == 5).all()):
                r_, gg_, bb_ = lin_img[y0_:y0_ + bs, x0_:x0_ + bs].reshape(-1, 3).mean(axis=0)
                nb += 1
                gr = float(gg_ / max(r_, 1e-9))
                if not (r_ > gg_ > bb_ and gr <= 0.85):
                    bad += 1
                    badl.append((x0_, y0_, round(gr, 2), round(float(bb_ / max(r_, 1e-9)), 2)))
                worst = max(worst, gr)
    return {"n": nb, "bad": bad, "worst_g_over_r": round(worst, 3), "bad_list": badl[:12]}


def measure_all(frames):
    """Per frame per window: the stats (pane px, P, L, D, spread, line profile), with the window's state and angle."""
    out = {}
    lit_names = set(T.lit_at("20:30"))
    for tag, f in frames.items():
        b, m = MS.load(f["frame"], f["mask"])
        mt = np.asarray(Image.open(f["maskT"]).convert("RGB")) if os.path.exists(f["maskT"]) else None
        lumb = MS.luma(b) if mt is not None else None
        linb = lin(b) if (f["state"] == "night" and mt is not None) else None
        ro_lin = None
        for sid, w in f["rec"]["windows"].items():
            site = T.site(sid)
            st = MS.stats_for(b, m, w["id"])
            if st is None:
                continue
            if mt is not None:
                # the glass told apart from the cloth behind it (the mask with the glass clear): R 5 the room card = clear glass, R 3 the net, curtain or blind
                g_ = (m[..., 0] == 1) & (m[..., 1] == w["id"])
                clear = g_ & (mt[..., 0] == 5) & (mt[..., 1] == w["id"])
                cloth = g_ & (mt[..., 0] == 3) & (mt[..., 1] == w["id"])
                st["clear_px"], st["cloth_px"] = int(clear.sum()), int(cloth.sum())
                st["clear_P"] = float(np.median(lumb[clear])) if clear.sum() >= 150 else None
                st["cloth_P"] = float(np.median(lumb[cloth])) if cloth.sum() >= 150 else None
                st["clear_rgb_mean"] = [float(v) for v in b[clear].mean(axis=0)] if clear.sum() >= 150 else None
                def ylin(sel):
                    px = b[sel].astype(np.float64)
                    l_ = lin(px)
                    y_ = 0.2126 * l_[:, 0] + 0.7152 * l_[:, 1] + 0.0722 * l_[:, 2]
                    return float(y_.mean()), float(np.median(y_))
                st["clear_Y"] = ylin(clear) if clear.sum() >= 150 else None          # (mean, median) of the linear luminance of the clear glass
                st["cloth_Y"] = ylin(cloth) if cloth.sum() >= 150 else None
                if linb is not None and sid in lit_names:
                    st["curtain_colour"] = (site.get("extra") or {}).get("colour")
                if linb is not None and sid in lit_names:
                    # NIGHT-03 block by block: every 32 x 32 block lying wholly in this window's glass: its mean linear colour; on the beauty frame, and on the reflection-off frame (16 x 16 at its half size) that holds the room's own
                    # colour without the stand-in sky's reflection in the glass
                    green = (site.get("extra") or {}).get("colour") == "green"          # a lit green curtain's g > r is its own colour (the target's NIGHT-03 line): only the blocks behind the room card are read in that window
                    st["blocks"] = block_colours(linb, g_, mt, green, 32)
                    if os.path.exists(f["ro"]):
                        if ro_lin is None:
                            ro_lin = lin(np.asarray(Image.open(f["ro"]).convert("RGB")))
                        st["blocks_ro"] = block_colours(ro_lin, g_[::2, ::2], mt[::2, ::2], green, 16)
            st["line"] = MS.line_profile(b, m, w["id"], st["L"])
            st["angle"] = w["angle_deg"]
            st["state"] = MS.window_state(site)
            st["site"] = sid
            st["net"] = site["net"]["kind"]
            st["extra"] = (site.get("extra") or {}).get("kind")
            st["frame"] = tag
            # brick beside the window: the brick pixels of a ring round its box
            x0, y0, x1, y1 = st["bbox"]
            mx, my = int((x1 - x0) * 1.0) + 8, int((y1 - y0) * 0.5) + 8
            sub = m[max(y0 - my, 0):y1 + my, max(x0 - mx, 0):x1 + mx]
            bsub = b[max(y0 - my, 0):y1 + my, max(x0 - mx, 0):x1 + mx]
            br = (sub[..., 0] == 4) & (sub[..., 1] == 0)
            st["brick_median"] = float(np.median(MS.luma(bsub)[br])) if br.sum() > 200 else None
            out.setdefault(tag, {})[sid] = st
    return out


def is_h_view(frames, t):
    """The target's own measuring views (its five H cameras, here also the close view, which is H_ALONG_30_NEAR): the bands of WB-01 to WB-07 and NIGHT-01 to NIGHT-03 are 'the gate's views', set from photographs
    taken at street distance and read where the glass reflects the sky overhead. The review views (Hook, reverse, cam_A) are far, along the wall, and are reported beside, not failed."""
    n = frames[t]["name"]
    return n.startswith("h-") or n.startswith("close")


def wb_rows(frames, meas):
    day_all = {t: v for t, v in meas.items() if frames[t]["state"] == "day"}
    day = {t: v for t, v in day_all.items() if is_h_view(frames, t)}
    if not day_all:
        for rid in CHECK_IDS:
            if rid.startswith("WB"):
                not_run(rid, "no day frame with its mask is rendered (python3 build_windows.py gate)")
        return
    def pick(pred, lo=15.0, hi=30.0):
        return [s for t, ws in day.items() for s in ws.values() if lo <= s["angle"] <= hi and pred(s)]
    far = [s for t, ws in day_all.items() if not is_h_view(frames, t) for s in ws.values() if 15.0 <= s["angle"] <= 30.0 and s["state"] == "net" and s["net"] in ("N1", "N2")]
    far_txt = ("; the review views' far net windows at 15 to 30 degrees (hook, reverse; reported beside, not failed: far along the wall the net is a third of the pane and the clear upper sash reads the dark day room) read P/L %.2f to %.2f" % (min(s["P_over_L"] for s in far), max(s["P_over_L"] for s in far))) if far else ""
    net = pick(lambda s: s["state"] == "net" and s["net"] in ("N1", "N2"))
    bare = pick(lambda s: s["state"] == "bare")
    drap = pick(lambda s: s["state"] == "draped")
    def fmt(lst, key):
        return ", ".join("%s %.2f (%s %.0f deg)" % (s["site"].replace("east_parade_", "ep").replace("_upper", ""), s[key], s["frame"].split("_")[0], s["angle"]) for s in lst[:8]) + (" ..." if len(lst) > 8 else "")
    # WB-01
    if net:
        ok = all(0.55 <= s["P_over_L"] <= 0.97 for s in net)
        row("WB-01", ok, "%d net windows at 15 to 30 degrees by day in the target's measuring views: P/L %s" % (len(net), fmt(net, "P_over_L")) + ("" if ok else "  (outside 0.55 to 0.97: %s)" % [s["site"] for s in net if not 0.55 <= s["P_over_L"] <= 0.97]) + far_txt)
    else:
        not_run("WB-01", "no net window measured at 15 to 30 degrees by day")
    # WB-02
    if bare:
        ok = all(0.10 <= s["P_over_L"] <= 0.45 for s in bare)
        row("WB-02", ok, "%d bare window at 15 to 30 degrees by day: P/L %s" % (len(bare), fmt(bare, "P_over_L")))
    else:
        not_run("WB-02", "the bare window (east_parade_bay3_upper_w1) is not measured at 15 to 30 degrees: render h-along30-bay3w1")
    # WB-03
    ac = [s for t, ws in day.items() for s in ws.values() if frames[t]["name"].startswith("h-across0") and s["state"] == "bare" and s["angle"] > 60]
    if ac:
        # 14 Oct, from the try 1 reviews: the band's P/L is 0.35 to 0.90 and blue minus red at least -3 (the target's band came from P8, a clear blue sky; the game's sky is the overcast dome, neutral, and the pane is no warmer than it)
        ok = all(0.35 <= s["P_over_L"] <= 0.90 and s["pane_rgb_mean"][2] - s["pane_rgb_mean"][0] >= -3 for s in ac)
        row("WB-03", ok, "bare window from H_ACROSS_0 by day: P/L %s (band 0.35 to 0.90), blue minus red %.0f levels (at least -3; the overcast dome is neutral)" % (fmt(ac, "P_over_L"), ac[0]["pane_rgb_mean"][2] - ac[0]["pane_rgb_mean"][0]))
    else:
        not_run("WB-03", "no H_ACROSS_0 day frame of the bare window")
    # WB-04
    both = net + bare
    if both:
        ok = all(s["D_over_L"] <= 0.72 for s in both)
        row("WB-04", ok, "%d bare and net windows at 15 to 30 degrees: D/L %s" % (len(both), fmt(both, "D_over_L")))
        good = [s for s in both if s["line"] and s["line"]["min_ratio"] is not None]
        ok = bool(good) and all(s["line"]["min_ratio"] <= 0.60 for s in good)
        row("WB-04b", ok, "dip at the pane edges over L: %s" % ", ".join("%s %.2f (%d edges)" % (s["site"][-12:], s["line"]["min_ratio"], s["line"]["edges"]) for s in good[:8]))
    else:
        not_run("WB-04", "no bare or net window at 15 to 30 degrees")
        not_run("WB-04b", "no bare or net window at 15 to 30 degrees")
    # WB-05
    ok = True
    parts = []
    for lst, lim, nm in ((net, 40, "net"), (bare, 20, "bare"), (drap, 20, "draped")):
        if lst:
            bad = [s["site"] for s in lst if s["spread"] < lim]
            ok &= not bad
            parts.append("%s %d windows spread %s (min %d)%s" % (nm, len(lst), "/".join("%.0f" % s["spread"] for s in lst[:5]), lim, "" if not bad else " FAIL " + str(bad)))
    if parts:
        row("WB-05", ok, "; ".join(parts))
    else:
        not_run("WB-05", "no window measured")
    # WB-06
    # a window cut by the picture's edge (the neighbours at the sides of an H_ACROSS_0 frame show a sliver) is not measured
    cand = [s for t, ws in day.items() for s in ws.values() if frames[t]["name"].startswith("h-across0") and (s["state"] == "bare" or s["net"] in ("N3", "N1") or s["extra"] in ("B1", "B2"))
            and s["bbox"][0] > 2 and s["bbox"][2] < 2557]
    if cand:
        res = []
        ok = True
        for s in cand:
            b, m = MS.load(frames[s["frame"]]["frame"], frames[s["frame"]]["mask"])
            sid = s["site"]
            wid = frames[s["frame"]]["rec"]["windows"][sid]["id"]
            g = (m[..., 0] == 1) & (m[..., 1] == wid)
            ys, xs = np.nonzero(g)
            lum = MS.luma(b)
            y0, y1 = ys.min(), ys.max()
            nb = 8
            meds = []
            for k in range(nb):
                sel = g & (np.arange(b.shape[0])[:, None] >= y0 + (y1 - y0) * k / nb) & (np.arange(b.shape[0])[:, None] < y0 + (y1 - y0) * (k + 1) / nb)
                if sel.sum() > 20:
                    meds.append(float(np.median(lum[sel])))
            diff = max(meds) - min(meds) if len(meds) > 1 else 0
            ok &= diff >= 10
            res.append("%s band medians span %.0f levels" % (sid[-12:], diff))
        row("WB-06", ok, "; ".join(res))
    else:
        not_run("WB-06", "no H_ACROSS_0 day frame")
    # WB-07
    # 14 Oct, from the try 1 reviews: the floor is 3.0 for white_fresh and white_upvc and 2.5 for white_grimy and white_flaking (3.0 x 0.66 / 0.82 = 2.4, rounded up so that a dull frame still reads clearly above its brick); the
    # ceiling stays 9.0. The street review's 2.5 is used for both dull paints; the close review's 2.2 (3.0 x 0.58 / 0.81, flaking only) would also pass.
    floors = {"white_fresh": 3.0, "white_upvc": 3.0, "white_grimy": 2.5, "white_flaking": 2.5}
    ratios = []
    for t, ws in day.items():
        for s in ws.values():
            if s["brick_median"] and 15 <= s["angle"] <= 60 and s["bbox"][0] > 2 and s["bbox"][2] < 2557 and s["bbox"][1] > 2 and s["bbox"][3] < 1437:      # a window cut by the picture's edge has too few joinery pixels
                ratios.append((s["site"], float(lin(s["L"]) / max(lin(s["brick_median"]), 1e-6)), floors[T.site(s["site"])["paint"]]))
    if ratios:
        ok = all(fl <= r <= 9.0 for _, r, fl in ratios)
        vals = [r for _, r, _ in ratios]
        low = sorted(set((sid, round(r, 2), fl) for sid, r, fl in ratios if r < fl + 0.4))[:4]
        row("WB-07", ok, "frame L over the brick beside it (linear): %d windows, median %.2f, range %.2f to %.2f (band: floor 3.0 for white_fresh and white_upvc, 2.5 for white_grimy and white_flaking, ceiling 9.0); nearest the floor (site, ratio, floor): %s" % (len(ratios), float(np.median(vals)), min(vals), max(vals), low))
    else:
        not_run("WB-07", "no window with brick beside it measured")
    # WB-08
    p = os.path.join(T.GATE, "old_fault.json")
    if os.path.exists(p):
        d = json.load(open(p))
        ok = d["P_over_L"] > 0.45 and d["D_over_L"] > 0.72 and (d["line"] is None or d["line"]["min_ratio"] is None or d["line"]["min_ratio"] > 0.6) and d["spread"] < 20
        row("WB-08", ok, "the first build's pane (a lit pale card, no reflection) with flat joinery (no box shade, no shading of the reveal) in the same view: P/L %.2f, D/L %.2f, spread %.0f, line dip %s: the checks fail it as they must (WB-02 P/L over 0.45, WB-04 D/L over 0.72, WB-04b no dip, WB-05 spread under 20, a bare window)" % (d["P_over_L"], d["D_over_L"], d["spread"], d["line"]))
    else:
        not_run("WB-08", "the old-fault frame (old_fault.json) is not rendered")
    # WB-09
    low = [s for t, ws in day_all.items() for s in ws.values() if s["angle"] < 10.0]
    if low:
        ok = all(s["P"] <= s["L"] for s in low)
        row("WB-09", ok, "%d windows under 10 degrees (the Hook camera cam_A): pane luma at most the lining's: %s" % (len(low), ", ".join("%s P %.0f L %.0f" % (s["site"][-12:], s["P"], s["L"]) for s in low[:6])))
    else:
        not_run("WB-09", "no window under 10 degrees measured (cam_A day frame)")


# ================================================================================================================ NIGHT
def night_rows(frames, meas):
    """NIGHT-01 to NIGHT-03 and NIGHT-07 to NIGHT-09 as the try 1 reviews asked (14 October). A lit window is told from a dark one by the table (rooms.lit_share at 20:30). Every rule is measured on the same kind of surface:
    the pane (the clear glass and the cloth behind it together) against the pane; the clear glass against the clear glass; the cloth against the cloth, told apart by the mask with the glass clear."""
    nf = {t: v for t, v in meas.items() if frames[t]["state"] == "night" and is_h_view(frames, t)}
    lit_names = set(T.lit_at("20:30"))
    if not nf:
        for rid in ("NIGHT-01", "NIGHT-02", "NIGHT-03", "NIGHT-07"):
            not_run(rid, "no night frame with its mask is rendered")
    else:
        lit, dark = [], []
        for t, ws in nf.items():
            for sid, s in ws.items():
                if s["angle"] < 45.0:
                    continue                      # the target: 'rendered from the one camera that sees each squarely' (H_ACROSS_0 and 30); at 15 to 30 degrees the glass reflects the night sky and the lit room is seen through a slit
                s["lit"] = sid in lit_names
                (lit if s["lit"] else dark).append(s)
        if lit and dark:
            dm = float(np.median([s["P"] for s in dark]))
            # NIGHT-01 (street review): LIT = pane median at least 2.5 times the dark windows' and r > g > b. DARK = the CLEAR (net-free) glass reads 8 to 35, and a dark window's net reads at most 0.7 of its own frame's L at night.
            res = []
            ok_lit = True
            for s in lit:
                rgb = s["pane_rgb_mean"]
                good = s["P"] >= 2.5 * dm and rgb[0] > rgb[1] > rgb[2]
                ok_lit &= good
                res.append("%s P %.0f%s" % (s["site"][-14:], s["P"], "" if good else " NOT LIT"))
            dclear = [(s["site"][-14:], s["clear_P"]) for s in dark if s.get("clear_P") is not None]
            bad_clear = [(n, round(v)) for n, v in dclear if not 8 <= v <= 35]
            dnet = [(s["site"][-14:], s["cloth_P"] / max(s["L"], 1e-6)) for s in dark if s.get("cloth_P") is not None and s["state"] == "net"]          # a net window (a blind or a drawn curtain is its own sheet: the target gives a draped window no band)
            bad_net = [(n, round(v, 2)) for n, v in dnet if v > 0.7]
            have_mask = any("clear_P" in s for s in dark)
            ok = ok_lit and not bad_clear and not bad_net and have_mask
            # the close review's wording, reported beside (per window against its own frame): dark P/L at most 0.70, lit P/L at least 1.0 with r > g > b
            cr_dark = [s for s in dark if s["P"] / max(s["L"], 1e-6) <= 0.70]
            cr_lit = [s for s in lit if s["P"] / max(s["L"], 1e-6) >= 1.0 and s["pane_rgb_mean"][0] > s["pane_rgb_mean"][1] > s["pane_rgb_mean"][2]]
            row("NIGHT-01", ok, "%d lit and %d dark windows measured (night frames of the target's views, windows seen at 45 degrees or more); dark median pane %.0f; lit (pane at least 2.5 times the dark median, r > g > b): %s; dark windows' CLEAR glass (8 to 35) %s, out of band: %s; dark windows' net over its frame's L (at most 0.7) %s, over: %s; the close review's own wording, beside and not failed: dark P/L at most 0.70 in %d of %d, lit P/L at least 1.0 with r > g > b in %d of %d"
                % (len(lit), len(dark), dm, ", ".join(res[:6]), ", ".join("%s %.0f" % (n, v) for n, v in dclear[:8]) or "none measured", bad_clear or "none",
                   ", ".join("%s %.2f" % (n, v) for n, v in dnet[:8]) or "no dark window with a net", bad_net or "none", len(cr_dark), len(dark), len(cr_lit), len(lit)))
            # NIGHT-02: lit at least 2.5 times dark (linear at least 6), the pane median of the lit windows over the pane median of the dark ones; like for like beside it
            lm = float(np.median([s["P"] for s in lit]))
            ratio = lm / max(dm, 1.0)
            ratio_l = float(lin(lm) / max(float(lin(dm)), 1e-6))
            def med(lst, key):
                v = [s[key] for s in lst if s.get(key) is not None]
                return float(np.median(v)) if v else None
            lc, dc, ln, dn = med(lit, "clear_P"), med(dark, "clear_P"), med(lit, "cloth_P"), med(dark, "cloth_P")
            like = "clear glass lit %s over dark %s; cloth lit %s over dark %s" % tuple("-" if v is None else "%.0f" % v for v in (lc, dc, ln, dn))
            row("NIGHT-02", ratio >= 2.5 or ratio_l >= 6, "median lit pane luma %.0f over the dark windows' %.0f: %.1f times (linear %.1f times; at least 2.5 / 6; the pane against the pane, the clear glass and the cloth in it as seen); like for like, beside: %s" % (lm, dm, ratio, ratio_l, like))
            # NIGHT-03: the lit nets' and curtains' colours, the pane's mean colour (the target's), AND block by block: every 32 px block wholly in a lit pane (every night frame) has r > g > b and linear g/r at most 0.85
            res, ok = [], True
            for s in lit:
                rgb = lin(np.array(s["pane_rgb_mean"]))
                r, g_, b_ = rgb
                if s["net"] != "N0" and s["extra"] not in ("C1", "B1", "B2", "B3"):
                    good = r > g_ > b_ and 0.55 <= g_ / r <= 0.80 + 0.12 and 0.20 <= b_ / r <= 0.45 + 0.1
                else:
                    good = r > g_ > b_
                ok &= good
                res.append("%s g/r %.2f b/r %.2f" % (s["site"][-14:], g_ / r, b_ / r))
            nbl, nbad, worst, where = 0, 0, 0.0, []
            nb_b, nbad_b, where_b = 0, 0, []
            for t, ws in meas.items():
                if frames[t]["state"] != "night":
                    continue
                for sid, s in ws.items():
                    bl_b = s.get("blocks")
                    bl = s.get("blocks_ro") or bl_b
                    if bl_b and bl_b["n"]:
                        nb_b += bl_b["n"]
                        nbad_b += bl_b["bad"]
                        if bl_b["bad"]:
                            where_b.append("%s %s %d of %d blocks (worst g/r %.2f)" % (t.split("_")[0], sid[-14:], bl_b["bad"], bl_b["n"], bl_b["worst_g_over_r"]))
                    if bl and bl["n"]:
                        nbl += bl["n"]
                        nbad += bl["bad"]
                        worst = max(worst, bl["worst_g_over_r"])
                        if bl["bad"]:
                            where.append("%s %s %d of %d blocks (first %s)" % (t.split("_")[0], sid[-14:], bl["bad"], bl["n"], bl["bad_list"][:2]))
            row("NIGHT-03", ok and nbad == 0 and nbl > 0, "lit windows' mean colour (linear, the pane as seen): %s (nets: r>g>b, g/r 0.55 to 0.80, b/r 0.20 to 0.45; the pane's mean carries the card and the glass's reflection, so the bands are read with 0.12 and 0.10 of room); block by block on the reflection-off night frames (the room's own colour, without the stand-in sky's neutral reflection in the glass; 16 px at their half size = 32 px): %d blocks wholly inside a lit pane in every night frame, %d with r > g > b broken or linear g/r over 0.85, worst g/r %.2f%s; on the beauty frames, beside: %d blocks of 32 px, %d over (reflection of the night sky at the glass's edge): %s"
                % ("; ".join(res[:6]), nbl, nbad, worst, ("; failing: " + "; ".join(where[:6])) if where else "", nb_b, nbad_b, "; ".join(where_b[:4]) or "none"))
            # NIGHT-07 (street review): in every lit window the clear glass over its lit net's, curtain's or blind's, 0.5 to 1.0, at H_ACROSS_0 night (the target's own view); the other views beside. The statistic is the MEAN of the
            # linear luminance of each region: it is what the street review's own figures were made with (0.26 to 0.31 at the old gain, 0.6 to 0.8 at 1.0: they reproduce with the mean, 0.27 and 0.65 here); the MEDIAN of the clear
            # glass (the dim upper sash and the walls under a bright transom and ceiling) reads 0.27 at gain 1.0 and is reported beside
            rr, bad7, beside = [], [], []
            for t, ws in meas.items():
                if frames[t]["state"] != "night":
                    continue
                for sid, s in ws.items():
                    if sid in lit_names and s.get("clear_Y") is not None and s.get("cloth_Y") is not None:
                        q = s["clear_Y"][0] / max(s["cloth_Y"][0], 1e-9)
                        qm = s["clear_Y"][1] / max(s["cloth_Y"][1], 1e-9)
                        (rr if frames[t]["name"].startswith("h-across0") else beside).append((t.split("_")[0], sid[-14:], round(q, 2), "median %.2f" % qm))
                        if frames[t]["name"].startswith("h-across0") and not 0.5 <= q <= 1.0:
                            bad7.append((t.split("_")[0], sid[-14:], round(q, 2)))
            if rr:
                row("NIGHT-07", not bad7, "a lit window's clear glass over its lit net's, curtain's or blind's, the mean of the linear luminance of each, H_ACROSS_0 night (frame, window, clear/cloth, the median's figure beside): %s (0.5 to 1.0); out of band: %s; the other views, beside and not failed: %s" % (rr, bad7 or "none", beside[:8] or "none"), name="a lit window's clear glass against its net")
            else:
                not_run("NIGHT-07", "no lit window with both clear glass and cloth seen in an H_ACROSS_0 night frame", name="a lit window's clear glass against its net")
        else:
            for rid in ("NIGHT-01", "NIGHT-02", "NIGHT-03", "NIGHT-07"):
                not_run(rid, "no lit and dark window pair measured at night")
    # NIGHT-08 and NIGHT-09: the street review's acceptance in its own views (the Hook night, the reverse night)
    def glass_medians(tag, only=None, min_px=30):
        """The median luma of each window's glass pixels in a night frame (the reverse view's far cottage windows are too small for the 150 px the other rows ask of glass and joinery): {site: (median, glass px)}."""
        f = frames[tag]
        b_, m_ = MS.load(f["frame"], f["mask"])
        lum = MS.luma(b_)
        out = {}
        for sid, w in f["rec"]["windows"].items():
            if only and not sid.startswith(only):
                continue
            g_ = (m_[..., 0] == 1) & (m_[..., 1] == w["id"])
            if g_.sum() >= min_px:
                out[sid] = (float(np.median(lum[g_])), int(g_.sum()))
        return out
    if "hook_night" in frames:
        # the Hook's lit windows against its dark ones: the pane median of each window seen with 150 px of glass and of joinery. The street review allowed a lit window behind a drawn brown curtain to stay dim ("a lined brown
        # curtain glows little": west_south_bay1_gf_w1): it is left out of the lit set, and the figure with it is given beside
        ws = meas["hook_night"]
        lit_all = {sid: s_["P"] for sid, s_ in ws.items() if sid in lit_names}
        brown = {sid for sid in lit_all if (T.site(sid).get("extra") or {}).get("colour") == "brown"}
        l_ = [v for sid, v in lit_all.items() if sid not in brown]
        d_ = [s_["P"] for sid, s_ in ws.items() if sid not in lit_names]
        if l_ and d_:
            r_ = float(np.median(l_)) / max(float(np.median(d_)), 1.0)
            r_l = float(lin(float(np.median(l_))) / max(float(lin(float(np.median(d_)))), 1e-6))
            r_all = float(np.median(list(lit_all.values()))) / max(float(np.median(d_)), 1.0)
            row("NIGHT-08", r_ >= 2.5 or r_l >= 6, "Hook night: the %d lit windows' median pane %.0f (%s) over the %d dark windows' %.0f: %.1f times, linear %.1f times (at least 2.5 / 6); the lit cottage behind a drawn brown curtain (%s, which the street review allowed to stay dim) is left out; with it the median reads %.1f times" % (len(l_), np.median(l_), ", ".join("%s %.0f" % (k[-14:], v) for k, v in lit_all.items() if k not in brown), len(d_), np.median(d_), r_, r_l, ", ".join("%s %.0f" % (k[-14:], lit_all[k]) for k in brown) or "none in view", r_all), name="lit against dark in the Hook night")
        else:
            not_run("NIGHT-08", "the Hook night frame has no lit and dark pair measured", name="lit against dark in the Hook night")
    else:
        not_run("NIGHT-08", "no hook_night frame", name="lit against dark in the Hook night")
    if "reverse_night" in frames:
        gm = glass_medians("reverse_night", only="west_south")
        pair = {sid: v[0] for sid, v in gm.items() if sid in ("west_south_bay2_gf_w0", "west_south_bay2_gf_w1")}
        dk = {sid: v[0] for sid, v in gm.items() if sid not in lit_names}
        if len(pair) == 2 and dk:
            row("NIGHT-09", min(pair.values()) > max(dk.values()), "reverse night: the lit pair of west_south_bay2 reads %s (glass px %s), every dark cottage window %s (the lit pair above every dark one; the lit window behind the drawn brown curtain, west_south_bay1_gf_w1, may stay dim and reads %.0f)" % ({k[-8:]: round(v) for k, v in pair.items()}, [gm[k][1] for k in pair], {k[-14:]: round(v) for k, v in dk.items()}, gm.get("west_south_bay1_gf_w1", (float("nan"),))[0]), name="the lit cottages read above the dark ones in the reverse night")
        else:
            not_run("NIGHT-09", "the reverse night frame does not show the lit pair and a dark cottage window", name="the lit cottages read above the dark ones in the reverse night")
    else:
        not_run("NIGHT-09", "no reverse_night frame", name="the lit cottages read above the dark ones in the reverse night")
    # NIGHT-04 the dark pictures
    rows_ = []
    ok = True
    n = 0
    for rid in T.rooms():
        p = os.path.join(T.ROOMS, "%s_night_dark.png" % rid)
        if os.path.exists(p):
            a = np.asarray(Image.open(p).convert("RGB")).astype(np.float64)
            l = lin(a).reshape(-1, 3).mean(axis=0)
            ly = float(MS.luma(a).mean())
            good = l[2] / l[0] < 0.05 and 8 <= ly <= 30
            ok &= good
            n += 1
            rows_.append("%s b/r %.3f luma %.1f" % (rid, l[2] / l[0], ly))
    if n:
        row("NIGHT-04", ok and n == 13, "%d of 13 night_dark pictures: %s" % (n, "; ".join(rows_)) + ("" if n == 13 else " (the rest not rendered)"), status=None if (n == 13 or not ok) else "not_run")
    else:
        not_run("NIGHT-04", "no night_dark picture is rendered")
    # NIGHT-05
    lbh = TGT["rooms"]["lit_share"]["lit_by_hour"]
    s20, s23 = set(lbh["20:30"]["windows"]), set(lbh["23:00"]["windows"])
    always = {"west_south_bay2_gf_w0", "west_south_bay2_gf_w1"}
    empties = {s["id"] for s in T.sites() if s["room"].startswith("up_empty")}
    nested = (s23 - always) <= s20 and not ((s20 | s23) & empties)
    row("NIGHT-05", nested, "the set lit at 23:00 (%d) is inside the set lit at 20:30 (%d) but for the always-lit pair; no empty room is ever lit" % (len(s23), len(s20)))
    # the lit set at 20:30 has seven
    row("NIGHT-06", len(s20) == 7, "seven windows lit at 20:30 (target 7 +-1): %d" % len(s20), name="the 20:30 count")


# ================================================================================================================ the glass band and corners (lessons)
def gls04(frames):
    rows = []
    ok = True
    n = 0
    for tag, f in frames.items():
        if f["state"] != "night" or not os.path.exists(f["ro"]):
            continue
        b = np.asarray(Image.open(f["frame"]).convert("RGB").resize((1280, 720), Image.LANCZOS)).astype(np.float64)
        r = np.asarray(Image.open(f["ro"]).convert("RGB")).astype(np.float64)
        m = np.asarray(Image.open(f["mask"]).convert("RGB").resize((1280, 720), Image.NEAREST))
        glass = m[..., 0] == 1
        if glass.sum() < 100:
            continue
        d = MS.luma(b) - MS.luma(r)
        # the fault of the shops' night glass was a burnt ORANGE bar (the stand-in lamps' pool on the road): a patch counts when what the reflection adds is the sodium colour (red far over blue); a grey patch is
        # the night sky in the glass (a real reflection, 0.2 of the dome at the night glass) and is listed beside, not failed
        add = b - r
        orange = (add[..., 0] - add[..., 2]) >= 0.5 * np.maximum(d, 1.0)
        bright_o = (d >= 40) & glass & orange
        bright_g = (d >= 40) & glass & ~orange
        def biggest_of(msk):
            lab, nl = ndimage.label(msk)
            return max((int(c) for c in np.bincount(lab.ravel())[1:]), default=0) if nl else 0
        share = biggest_of(bright_o) / float(glass.sum())
        sky = biggest_of(bright_g) / float(glass.sum())
        n += 1
        ok &= share < 0.001
        rows.append("%s largest orange patch %.4f%% of the glass (grey sky patch %.2f%%, a real reflection)" % (tag, share * 100, sky * 100))
    if n:
        row("GLS-04", ok, "night frames against the reflection-off render: " + "; ".join(rows) + " (the largest connected patch of window glass 40 or more levels brighter than the reflection-off render and sodium-coloured must be under 0.1% of the glass)", name="no bright band in the night glass")
    else:
        not_run("GLS-04", "no night frame with its reflection-off render", name="no bright band in the night glass")


def lamp_row(frames):
    """GLS-05: no lit stand-in lamp is seen (burnt orange outside the joinery and the brick) AND, from 14 October (the street review's N3), no window's joinery is burnt: at most 2 per cent of any window's joinery pixels
    clipped to flat orange (R 250 or more, B under 140), the game's own limit for the nearest pool (his order of 8 October, lantern_pool_lumens). The brick in the lamp's pool is not counted."""
    n = 0
    bad = []
    worst = []
    for tag, f in frames.items():
        if f["state"] != "night":
            continue
        b = np.asarray(Image.open(f["frame"]).convert("RGB")).astype(np.int32)
        m = np.asarray(Image.open(f["mask"]).convert("RGB"))
        hot = (b[..., 0] >= 250) & (b[..., 2] < 140)
        seen = hot & (m[..., 0] != 2) & (m[..., 0] != 4)
        n += 1
        if seen.sum() > 0:
            bad.append((tag, "outside the joinery", int(seen.sum())))
        for sid, w in f["rec"]["windows"].items():
            j = (m[..., 0] == 2) & (m[..., 1] == w["id"])
            if j.sum() < 150:
                continue
            share = float((hot & j).sum()) / float(j.sum())
            worst.append((round(100.0 * share, 2), tag.split("_")[0], sid[-14:]))
            if share > 0.02:
                bad.append((tag, sid, "%.1f%% of the joinery burnt" % (100.0 * share)))
    worst.sort(reverse=True)
    if n:
        row("GLS-05", not bad, "no lit stand-in lamp is seen (the lamp lights are out of camera, glossy and transmission rays) and no window's joinery is more than 2 per cent burnt (R 250+, B under 140), in %d night frames: %s; the most burnt windows (per cent, frame, window): %s" % (n, bad or "none", worst[:4]), name="no lit stand-in lamp in view, no burnt window frame")
    else:
        not_run("GLS-05", "no night frame", name="no lit stand-in lamp in view, no burnt window frame")


def jnr_row(frames):
    """JNR-01 (the close review's narrow point 1): by day no joinery pixel under luma 10 inside any window outline (a joinery face that gets no light: the black notch at the far jamb's head). A pixel in 1000 is allowed for the anti-aliased
    edge between the mask and the beauty frame; the first build's notch was 0.9 per cent of one window's joinery."""
    n, worst, bad = 0, [], []
    for tag, f in frames.items():
        if f["state"] != "day":
            continue
        b, m = MS.load(f["frame"], f["mask"])
        lum = MS.luma(b)
        for sid, w in f["rec"]["windows"].items():
            j = (m[..., 0] == 2) & (m[..., 1] == w["id"])
            if j.sum() < 150:
                continue
            ys, xs = np.nonzero(j | ((m[..., 0] == 1) & (m[..., 1] == w["id"])))
            box = j[ys.min():ys.max() + 1, xs.min():xs.max() + 1] & (lum[ys.min():ys.max() + 1, xs.min():xs.max() + 1] < 10)
            share = float(box.sum()) / float(j.sum())
            n += 1
            worst.append((round(100.0 * share, 3), int(box.sum()), tag.split("_")[0], sid[-14:]))
            if share > 0.001:
                bad.append((tag, sid, int(box.sum())))
    worst.sort(reverse=True)
    if n:
        row("JNR-01", not bad, "by day no joinery pixel under luma 10 inside a window outline (at most 0.1 per cent of the window's joinery): %d windows in the day frames; over: %s; the most (per cent, pixels, frame, window): %s" % (n, bad or "none", worst[:4]), name="no black joinery by day")
    else:
        not_run("JNR-01", "no day frame", name="no black joinery by day")


def acc_rows(meas):
    """The street review's acceptance in its own views by day (14 October): cam_A's two cottage windows west_south_bay0 reach P/L 0.45 or more; the Hook's east_parade_bay0_upper_w0 (its full-height net) 0.55 or more."""
    t = meas.get("cam-a_day")
    if t:
        got = {sid[-8:]: round(t[sid]["P_over_L"], 2) for sid in ("west_south_bay0_gf_w0", "west_south_bay0_gf_w1") if sid in t}
        row("ACC-01", len(got) == 2 and all(v >= 0.45 for v in got.values()), "cam_A day: west_south_bay0's two windows P/L %s (at least 0.45; the first build read 0.07 and 0.11 through the mirror)" % got, name="cam_A day: the cottage windows show their nets and rooms")
    else:
        not_run("ACC-01", "no cam_A day frame", name="cam_A day: the cottage windows show their nets and rooms")
    t = meas.get("hook_day")
    if t and "east_parade_bay0_upper_w0" in t:
        v = t["east_parade_bay0_upper_w0"]["P_over_L"]
        row("ACC-02", v >= 0.55, "Hook day: east_parade_bay0_upper_w0 (a full-height net) P/L %.2f (at least 0.55; the first build read 0.52 as four grey mirror panes)" % v, name="Hook day: the near window's net shows")
    else:
        not_run("ACC-02", "no Hook day frame with east_parade_bay0_upper_w0 measured", name="Hook day: the near window's net shows")


def slot_row(frames):
    n = 0
    bad = []
    for tag, f in frames.items():
        m = np.asarray(Image.open(f["mask"]).convert("RGB"))
        st = MS.see_through(m)
        n += 1
        for wid, c in st.items():
            if c > 3:
                bad.append((tag, wid, c))
    if n:
        row("FRM-01", not bad, "no see-through slot: in %d frames' masks the background shows inside no window's outline box (more than 3 pixels): %s" % (n, bad or "none"), name="no see-through slot at any camera")
    else:
        not_run("FRM-01", "no frame", name="no see-through slot at any camera")


# ================================================================================================================ PIC
def room_files(rid):
    return {s: os.path.join(T.ROOMS, "%s_%s.png" % (rid, s)) for s in ("day", "night_lit", "night_dark")}


def pic_rows():
    rooms = T.rooms()
    missing = []
    sizes_bad = []
    n = 0
    for rid, R in rooms.items():
        fs = room_files(rid)
        for s, p in fs.items():
            if not os.path.exists(p):
                missing.append("%s_%s" % (rid, s))
                continue
            im = Image.open(p)
            n += 1
            if im.size != tuple(R["picture_px"]) or im.mode != "RGB":
                sizes_bad.append((rid, s, im.size, im.mode))
        if not os.path.exists(os.path.join(T.ROOMS, rid + ".json")):
            missing.append(rid + ".json")
    row("PIC-01", not missing and not sizes_bad, "%d of 39 pictures present at 1536 x 1399 (upper rooms) or 3072 x 2349 (cottages), 8-bit RGB; not rendered: %s; wrong: %s" % (n, (", ".join(missing[:12]) + (" ..." if len(missing) > 12 else "")) or "none", sizes_bad or "none"), status=None if (not missing and not sizes_bad) else "fail")
    # PIC-02
    res, ok, cnt = [], True, 0
    tgt = TGT["rooms"]["picture_standards"]
    for rid, R in rooms.items():
        for s, p in room_files(rid).items():
            if not os.path.exists(p):
                continue
            a = np.asarray(Image.open(p).convert("RGB"))
            m = float(MS.luma(a).mean())
            std = {"day": tgt["day_mean_luma"], "night_lit": tgt["night_lit_mean_luma"], "night_dark": tgt["night_dark_mean_luma"]}[s]
            if R["type"] == "landing" and s == "night_lit":
                std = 40.0
            if R["type"] == "empty" and s == "night_lit":
                std = tgt["night_dark_mean_luma"]
            cnt += 1
            good = abs(m - std) / std <= tgt["tolerance"] + 0.001
            ok &= good
            if not good:
                res.append("%s %s %.1f (want %.0f)" % (rid, s, m, std))
    row("PIC-02", cnt > 0 and ok, "%d pictures' mean luma within 15%% of the standard (day 105, night_lit 70, night_dark 15; landings 40 at night_lit; an empty room's night_lit is its night_dark, the target's lights_by_state over its PIC-02 line); off: %s" % (cnt, res or "none"), status=None if cnt else "not_run")
    # PIC-03 and the corner columns
    res, ok, cnt = [], True, 0
    for rid in rooms:
        for s, p in room_files(rid).items():
            if not os.path.exists(p) or s == "night_dark":
                continue
            if s == "night_lit" and rooms[rid]["type"] == "empty":
                continue                       # an empty room's night_lit IS its night_dark (the target's lights_by_state): dark by design, as the night_dark pictures the row leaves out
            a = np.asarray(Image.open(p).convert("RGB"))
            l = MS.luma(a)
            under = l < 8
            share = float(under.mean())
            lab, nl = ndimage.label(under)
            big = max((int(c) for c in np.bincount(lab.ravel())[1:]), default=0) / float(l.size)
            lin_c = lin(a) * BRIGHT[s]
            if s == "night_lit" and rooms[rid]["type"] == "landing":      # a lit landing's card never emits less than the target's absolute floor (landing_bulb.card_emission_floor_linear)
                lin_c = np.maximum(lin_c, np.array(TGT["rooms"]["lights_by_state"]["landing_bulb"]["card_emission_floor_linear"]))
            comp = float(MS.luma(np.clip(np.asarray(srgb_of(lin_c)) * 255, 0, 255)).mean())
            good = share < 0.25 and big < 0.15 and comp >= (14 if s == "day" else 40)
            cnt += 1
            ok &= good
            if not good:
                res.append("%s %s dark share %.2f, largest %.2f, composite %.0f" % (rid, s, share, big, comp))
    row("PIC-03", cnt > 0 and ok, "%d day and night_lit pictures: under 25%% below luma 8, largest dark region under 15%%, composite (x brightness; a lit landing's card with its absolute floor) day 14+, night_lit 40+; an empty room's night_lit is its night_dark and is left out with the night_dark pictures; off: %s" % (cnt, res or "none"), status=None if cnt else "not_run")
    res, ok, cnt = [], True, 0
    for rid in rooms:
        p = room_files(rid)["night_dark"]
        if not os.path.exists(p):
            continue
        a = np.asarray(Image.open(p).convert("RGB"))
        l = MS.luma(a)
        h, w = l.shape
        cw, ch = max(int(w * 60 / 4096.0), 8), int(h * 200 / 1855.0)
        corners = np.concatenate([l[:ch, :cw].ravel(), l[:ch, -cw:].ravel()])
        ratio = float(corners.mean() / l.mean())
        cnt += 1
        ok &= ratio <= 1.5
        res.append("%s %.2f" % (rid, ratio))
    row("PIC-03b", cnt > 0 and ok, "night_dark top front corner columns at most 1.5 times the picture's mean (the shops' burnt orange corners): %s" % ", ".join(res), name="the night wash does not burn the corners", status=None if cnt else "not_run")
    # PIC-04 the back wall's corners
    pic04(rooms)
    # PIC-05 stand-off
    pic05(rooms)
    # PIC-09 noise
    res, ok, cnt = [], True, 0
    for rid in rooms:
        for s in ("day", "night_lit"):
            p = room_files(rid)[s]
            if not os.path.exists(p):
                continue
            a = MS.luma(np.asarray(Image.open(p).convert("RGB")))
            blur = ndimage.gaussian_filter(a, 2.0)
            hp = a - blur
            gy, gx = np.gradient(blur)
            flat = np.hypot(gx, gy) < 0.35
            flat = ndimage.binary_erosion(flat, iterations=3)
            if flat.sum() < 2000:
                continue
            # the robust estimate (1.4826 x the median absolute deviation): the patterned papers (stripes, the jacquard) leave a few stripe edges and pattern pixels in the 'flat' set and a plain standard
            # deviation read them as noise (1.9 levels in lounge 3 and bedroom 3 where the robust figure is 0.8); on the plain rooms the two agree (0.5 to 0.9)
            v = hp[flat]
            nz = float(1.4826 * np.median(np.abs(v - np.median(v))))
            cnt += 1
            ok &= nz <= 1.6
            res.append("%s %s %.2f" % (rid, s, nz))
    row("PIC-09", cnt > 0 and ok, "noise: the robust standard deviation (1.4826 x median absolute deviation) of the picture minus its 2 px blur over its flat areas, at most 1.6 levels (24 samples, denoised; 16 for the cottages): %s" % ", ".join(res[:26]), name="room pictures are not noisy", status=None if cnt else "not_run")
    # PIC-06
    pic06()
    pic07()
    pic08()
    pic13(rooms)
    pic_extra(rooms)


def srgb_of(l):
    l = np.clip(l, 0, 1)
    return np.where(l <= 0.0031308, l * 12.92, 1.055 * l ** (1 / 2.4) - 0.055)


def pic04(rooms):
    res, ok, cnt = [], True, 0
    for rid, R in rooms.items():
        p = room_files(rid)["day"]
        if not os.path.exists(p):
            continue
        fam = T.families()[R["family"]]
        W, H, D, d = fam["w"], fam["h"], fam["d"], fam["camd"]
        px = R["picture_px"]
        exp = TGT["rooms"]["pictures_by_family"][R["family"]]["back_wall_rect_px_x0y0x1y1"]
        # the projection: the room's own rule u = 0.5 + x/W d/(d + y), v = 0.5 + (z/H - 0.5) d/(d + y), at the back wall y = D
        s = d / (d + D)
        x0 = (0.5 - 0.5 * s) * px[0]
        x1 = (0.5 + 0.5 * s) * px[0]
        y0 = (1 - (0.5 + 0.5 * s)) * px[1]
        y1 = (1 - (0.5 - 0.5 * s)) * px[1]
        math_ok = max(abs(x0 - exp[0]), abs(x1 - exp[2]), abs(y0 - exp[1]), abs(y1 - exp[3])) <= 8
        # and the picture: the corner shows where the line under the coving (the dark shade line, the darkest thing in the top rows) leaves the horizontal: on the back wall it is level, on a side wall it runs up toward
        # the picture's edge. Found per column as the row of least luma over the top of the picture; the kink is the first column outward from the back wall's inside at which the row is 1 px above the level one.
        # (A first try took the strongest vertical edge in the top rows of the back wall: the striped wallpapers of lounge 3 and bedroom 3 have stripe edges as strong as the corner.)
        a = MS.luma(np.asarray(Image.open(p).convert("RGB")))
        top = ndimage.gaussian_filter(a[:int(y0 + 0.10 * (y1 - y0))], 1.0)
        line_row = np.argmin(top[int(0.25 * y0):], axis=0) + int(0.25 * y0)
        def kink(xe, sgn):
            inside = [int(xe + sgn * k) for k in range(15, 70)]
            level = float(np.median(line_row[inside]))
            x = int(xe + sgn * 15)
            while 0 < x < len(line_row) - 1 and line_row[x] >= level - 1.0 and abs(x - xe) < 80:
                x -= sgn
            return x
        pl, pr = kink(x0, 1), kink(x1, -1)
        img_ok = abs(pl - x0) <= 8 and abs(pr - x1) <= 8
        cnt += 1
        ok &= math_ok and img_ok
        res.append("%s edges at %d and %d (expected %.0f and %.0f)" % (rid, pl, pr, x0, x1))
    row("PIC-04", cnt > 0 and ok, "the back wall's side edges found in the day pictures within 8 px of the rule's projection: %s" % "; ".join(res[:13]), status=None if cnt else "not_run")


def pic05(rooms):
    bud = TGT["rooms"]["budget_rule"]
    res, ok, cnt = [], True, 0
    for rid, R in rooms.items():
        p = os.path.join(T.ROOMS, rid + ".placed.json")
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        W, H, D = d["size_m"]
        for o in d["placed"]:
            x0, x1, y0, y1, z0, z1 = o["ext"]
            if o["surface"] == "back":
                so = D - y0
                lim = {"true": bud["back"]["true"], "tolerated": bud["back"]["tolerated"]}[o["class"]]
            else:
                so = (x1 - x0) if o["surface"] == "left" or o.get("wall") else 0.0
                so = min(abs(x0 + W / 2), abs(W / 2 - x1)) if False else (x1 + W / 2 if o.get("wall") == "left" else W / 2 - x0)
                lim = {"true": bud["side"]["true"], "tolerated": bud["side"]["tolerated"]}[o["class"]]
            cnt += 1
            good = so <= lim + 0.012
            ok &= good
            if not good:
                res.append("%s %s stand-off %.3f over %.3f" % (rid, o["model"], so, lim))
        for f in d["forms"]:
            surf = f["surface"]
            lim = {"side+back": bud["side"]["tolerated"], "ceiling edge": bud["ceiling"]["tolerated"], "ceiling": bud["ceiling"]["tolerated"], "back": bud["side"]["tolerated"], "left": bud["side"]["tolerated"], "right": bud["side"]["tolerated"]}.get(surf, 0.06)
            cnt += 1
            good = f["proud"] <= lim + 1e-6
            ok &= good
            if not good:
                res.append("%s form %s proud %.3f over %.3f" % (rid, f["form"], f["proud"], lim))
    row("PIC-05", cnt > 0 and ok, "%d placed objects and flat forms inside the stand-off budgets of their surface (back 0.38 true, 0.71 tolerated; sides 0.03, 0.06; ceiling 0.02, 0.04); over: %s" % (cnt, res or "none"), status=None if cnt else "not_run")


def pic06():
    """A marker at the picture's centre moves as `trace` predicts from two eyes 2.0 m apart: bake a marker picture through the gate's own bake from both eyes and find the marker."""
    try:
        import hw_gate as HG
        W, H, D, d = 2.8, 2.55, 4.2, 2.8
        pic = np.zeros((699, 768, 3), np.uint8)
        pic[:] = 40
        cx, cy = 384, 350
        pic[cy - 8:cy + 8, cx - 8:cx + 8] = 255
        p = os.path.join(T.GATE, "marker.png")
        os.makedirs(T.GATE, exist_ok=True)
        Image.fromarray(pic).save(p)
        res = []
        ok = True
        pos = []
        for ex in (1.4, 3.4):
            eye_card = (ex, -8.8, 1.2)
            lin_img = HG.bake_card(eye_card, (W, H, D), d, 1, p, os.path.join(T.GATE, "marker_card.png"), 192, 175, jobs=2)
            a = lin_img.mean(axis=2)
            ys, xs = np.nonzero(a > 0.5 * a.max())
            pos.append((float(xs.mean()), float(ys.mean())))
        # predicted: the card point whose trace lands on the picture's centre (0.5, 0.5), by search along the row
        from hw_gate import trace
        def predict(ex):
            best = None
            for i in range(192):
                xc = W - (i + 0.5) / 192 * W
                for j in range(0, 175, 1):
                    zc = H - (j + 0.5) / 175 * H
                    u, v = trace((xc, 0.0, zc), (ex, -8.8, 1.2), (W, H, D), d, 1)
                    e = (u - 0.5) ** 2 + (v - 0.5) ** 2
                    if best is None or e < best[0]:
                        best = (e, i, j)
            return best[1], best[2]
        pr = [predict(1.4), predict(3.4)]
        err = max(abs(pos[k][0] - pr[k][0]) * 2048 / 192 for k in range(2))
        # the move between the two eyes in card pixels, against the prediction, scaled to 2048 px
        row("PIC-06", err <= 20, "marker at the picture centre baked from two eyes 2.0 m apart: seen at card columns %.1f and %.1f, predicted by trace %s and %s: error %.1f px of 2048 (limit 20); proves the gate's bake, not the game" % (pos[0][0], pos[1][0], pr[0][0], pr[1][0], err))
    except Exception as e:
        row("PIC-06", False, "failed: %s" % e)


def pic07():
    rep = os.path.join(T.KITWORK, "blanking_report.json")
    ok = os.path.exists(rep)
    detail = []
    import hw_models as M
    A = M.A
    for a, entries in M.MARKS.items():
        for e in entries:
            rel = A.map_path(a, e["map"])
            src = os.path.join(T.POLY, a, "1k", rel)
            dst = os.path.join(T.POLY, a, "1k", os.path.dirname(rel), os.path.splitext(e["map"])[0] + "_clean.jpg")
            if not os.path.exists(dst):
                ok = False
                detail.append("%s: no clean map" % a)
                continue
            s0 = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
            s1 = np.asarray(Image.open(dst).convert("RGB")).astype(np.float32)
            for (x0, y0, x1, y1) in e["boxes"]:
                patch = s1[y0:y1, x0:x1]
                X0, Y0, X1, Y1 = max(0, x0 - 6), max(0, y0 - 6), min(1024, x1 + 6), min(1024, y1 + 6)
                m = np.ones((Y1 - Y0, X1 - X0), bool)
                m[(y0 - Y0):(y1 - Y0), (x0 - X0):(x1 - X0)] = False
                ring = np.median(s1[Y0:Y1, X0:X1][m], axis=0)
                gy, gx = np.gradient(patch.mean(axis=2))
                edge = float((np.hypot(gx, gy) > 40).mean())
                dev = float(np.abs(patch - ring).max())
                good = dev <= 40 and edge < 0.02 and np.abs(s0[y0:y1, x0:x1] - s1[y0:y1, x0:x1]).max() > 30
                ok &= good
                detail.append("%s box %s: max deviation from the ring %.0f, edge share %.3f" % (a, [x0, y0, x1, y1], dev, edge))
    # the framed pictures: artwork replaced (the print's own hash differs from the model's) in every room that hangs one
    pr = 0
    for rid in T.rooms():
        p = os.path.join(T.ROOMS, rid + ".json")
        if os.path.exists(p):
            pr += len(json.load(open(p)).get("prints", []))
    row("PIC-07", ok, "marks painted out by script and checked region by region (television_02 PARAGON, wall_clock URBAN quartz): %s; every framed picture's artwork replaced by a crop of a CC0 photograph (%d placements in the rooms rendered); every placed model's 1k base colour looked at at 100 per cent by me on 14 October (NOTES.md); the pictures themselves are for the reviewers' eyes" % ("; ".join(detail), pr))


def pic08():
    import hw_gate as HG
    lit = set(T.lit_at("20:30"))
    bad = []
    for s in T.sites():
        d = HG.card_state(s, False, lit)
        n = HG.card_state(s, True, lit)
        want_n = "night_lit" if (s["id"] in lit and not s["room"].startswith("up_empty")) else "night_dark"
        if d != "day" or n != want_n:
            bad.append(s["id"])
    row("PIC-08", not bad, "the picture each of the 20 windows uses: day by day; at 20:30 night_lit for the seven lit windows, night_dark for the rest (the gate's own rule `card_state`); wrong: %s" % (bad or "none"))


def pic13(rooms):
    """PIC-13 (the close review's fix 2): no night_lit picture has more than 0.1 per cent of its pixels with a channel at 250 or more (the ceiling round the rose clipped to (255, 253, 178) and the card's gain made it olive). An empty room's
    night_lit is its night_dark (no lamp). The day and night_dark pictures are listed beside."""
    res, ok, cnt, beside = [], True, 0, []
    for rid in rooms:
        for st in ("night_lit", "day", "night_dark"):
            p = room_files(rid)[st]
            if not os.path.exists(p):
                continue
            a = np.asarray(Image.open(p).convert("RGB"))
            share = float((a >= 250).any(axis=2).mean())
            if st == "night_lit":
                cnt += 1
                good = share <= 0.001
                ok &= good
                res.append("%s %.4f%%" % (rid, 100 * share))
            elif share > 0.001:
                beside.append("%s %s %.2f%%" % (rid, st, 100 * share))
    row("PIC-13", cnt > 0 and ok, "no clipped highlights: the share of pixels with a channel at 250 or more in each of %d night_lit pictures, at most 0.1 per cent (the highlight roll-off before the 8-bit write): %s; beside, not failed: day and night_dark pictures over 0.1 per cent: %s" % (cnt, ", ".join(res), ", ".join(beside[:10]) or "none"), name="no clipped highlights in a lit room picture", status=None if cnt else "not_run")


def pic_extra(rooms):
    # floating goods, real heights, every model keeps all its parts, glass kept
    fl, hs, parts, glass = [], [], [], []
    cnt = 0
    for rid, R in rooms.items():
        p = os.path.join(T.ROOMS, rid + ".placed.json")
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        W, H, D = d["size_m"]
        cnt += 1
        by = {o["model"]: o for o in d["placed"]}
        for o in d["placed"]:
            x0, x1, y0, y1, z0, z1 = o["ext"]
            on = o.get("on")
            if on:
                par = by.get(on)
                sup = o.get("support") or {}
                top = par["ext"][5] if par else None
                if sup.get("sink_mm") is None or (top is not None and abs(z0 - (sup["z_base_m"])) > 0.003) or (sup.get("gap_mm") is not None and sup["gap_mm"] - 2 * sup.get("sink_mm", 0) > 6.0):
                    fl.append("%s %s on %s: gap %s mm" % (rid, o["model"], on, sup.get("gap_mm")))
            elif o["surface"] == "back":
                hung = o["model"].startswith(("hanging_picture", "ornate_mirror", "wall_clock"))
                if not hung and abs(z0) > 0.003:
                    fl.append("%s %s base at %.3f" % (rid, o["model"], z0))
                if abs(y1 - D) > 0.004:
                    fl.append("%s %s back %.3f from the wall" % (rid, o["model"], D - y1))
            else:
                wall_gap = (x0 + W / 2) if o.get("wall") == "left" else (W / 2 - x1)
                if wall_gap > 0.004:
                    fl.append("%s %s %.3f off its wall" % (rid, o["model"], wall_gap))
            # real height: the model's own height from the template (scale 1.0): the placed height over the catalogue's
            hh = z1 - z0
            cat = T.target()["inventory"]["polyhaven_models"][o["model"]]["dims_mm_catalogue_xyz"][2] / 1000.0
            if o["model"] != "mantel_clock_01":
                hs.append((rid, o["model"], round(hh / cat, 3)))
            if o["scale"] != 1.0:
                hs.append((rid, o["model"], "scale %s" % o["scale"]))
        for a, au in d.get("audit", {}).items():
            if au.get("kept_meshes") != au.get("source_meshes"):
                parts.append((a, au.get("source_meshes"), au.get("kept_meshes")))
    if cnt:
        bad_h = [h for h in hs if (isinstance(h[2], str)) or not 0.9 <= h[2] <= 1.1]
        row("PIC-10", not fl, "floating goods: every piece stands on the floor, rests on its parent (a clock on its cabinet, the television on its table: the parent's top under it, a gap over 6 mm split into a sink) or hangs on its wall (touching): %s; %d rooms read" % (fl or "none floating", cnt), name="no floating goods")
        row("PIC-11", not bad_h, "every placed piece at scale 1.0 and 0.9 to 1.1 of its model's own height: %d pieces, off: %s (mantel_clock_01's catalogue size 483.7 x 250.8 x 160.9 is not the model's 342.3 x 126.2 x 160.5: its own height is used)" % (len(hs), bad_h or "none"), name="real size: no piece shrunk to fit")
        row("PIC-12", not parts, "every placed model keeps all the meshes of its glTF (the glass kept as a see-through material, not alpha-blended): %s" % (parts or "all kept"), name="models keep their glass and every part")
    else:
        for rid, nm in (("PIC-10", "no floating goods"), ("PIC-11", "real size: no piece shrunk to fit"), ("PIC-12", "models keep their glass and every part")):
            not_run(rid, "no room rendered", name=nm)


# ================================================================================================================ SITE, CONTENT, extras
def site_rows(frames):
    S = T.sites()
    try:
        sys.path.insert(0, T.TARGET_DIR)
        import importlib.util
        spec = importlib.util.spec_from_file_location("hw_sites_t", os.path.join(T.TARGET_DIR, "hw_sites.py"))
        hs = importlib.util.module_from_spec(spec)
        sys.dont_write_bytecode = True
        spec.loader.exec_module(hs)
        derived, tf = hs.derive()
        bad = []
        for dsite in derived:
            cx = (dsite["x_min"] + dsite["x_max"]) / 2
            mt = [s for s in S if s["block"] == dsite["block"] and s["bay"] == dsite["bay"] and s["index"] == dsite["index"] and ((s["floor"] == "upper") == (dsite["floor"] == "upper"))]
            if len(mt) != 1 or abs(mt[0]["x_centre"] - cx) > 0.001:
                bad.append((dsite["block"], dsite["bay"], dsite["index"]))
        ok = len(derived) == 20 and not bad
        row("SITE-01", ok, "terrace-front.py's windows re-derived live (the target's hw_sites.derive, read only): %d sites, centres within 1 mm of sites[]; the gate stands every kit piece at its site (x_centre, sill, side); off: %s" % (len(derived), bad or "none"))
    except Exception as e:
        row("SITE-01", False, "the live derivation failed: %s" % e)
    # SITE-02
    bad = []
    rows_ = {}
    for s in S:
        rows_.setdefault(s["side"], []).append(s)
    for blk, lst in rows_.items():
        lst = sorted(lst, key=lambda s: s["x_centre"])
        for i, a in enumerate(lst):
            for b in lst[i + 1:i + 4]:
                ta = (a["room"], a["net"]["kind"], (a.get("extra") or {}).get("kind"), (a.get("extra") or {}).get("colour"))
                tb = (b["room"], b["net"]["kind"], (b.get("extra") or {}).get("kind"), (b.get("extra") or {}).get("colour"))
                same_house = a.get("house") == b.get("house") and a["family"] == "GF"          # a cottage's two windows are one room (the target's own self-check leaves them out)
                if ta == tb and not same_house:
                    bad.append((a["id"], b["id"]))
    row("SITE-02", not bad, "no (room, net kind, curtain) triple repeats within three places along any row (a cottage's own two windows, one room, excepted as the target's self-check does); paints are white throughout; repeats: %s" % (bad or "none"))
    # SITE-03
    from collections import Counter
    nc = Counter(s["net"]["kind"] for s in S)
    drape = sum(1 for s in S if (s.get("extra") or {}).get("kind"))
    ok = 4 <= nc["N0"] <= 5 and 8 <= nc["N1"] <= 10 and 3 <= nc["N2"] <= 5 and nc["N3"] == 1 and 6 <= drape <= 10
    built = None
    if frames:
        t0 = next(iter(frames.values()))
        objs = {sid: set(w.get("objects", [])) for sid, w in t0["rec"]["windows"].items()}
        built = Counter(("N0" if not any(o.startswith("net__") for o in v) else [o for o in v if o.startswith("net__")][0].replace("net__", "").replace("_torn", "")) for v in objs.values())
        ok &= (built == nc)
    row("SITE-03", ok, "net classes N0 %d, N1 %d, N2 %d, N3 %d; curtains and blinds %d of 20%s" % (nc["N0"], nc["N1"], nc["N2"], nc["N3"], drape, ("; the built windows (a frame's kit pieces) match: %s" % dict(built)) if built else ""))
    # SITE-04
    pn = Counter(s["paint"] for s in S)
    white = all(p.startswith("white") for p in pn)
    row("SITE-04", white, "paints by window: %s; every house white (Jafar's ruling of 3 October)" % dict(pn))


def content_rows():
    words = ["beer", "wine", "whisky", "whiskey", "vodka", "pub ", "brewery", "gambl", "casino", "betting", "bookmaker", "lottery", "poker", "child", "toy ", "toys", "baby", "infant", "kid "]
    brands = list(TGT["inventory"]["brand_blocklist"])
    hits = []
    files = glob.glob(os.path.join(HERE, "*.py")) + glob.glob(os.path.join(HERE, "*.md")) + glob.glob(os.path.join(T.ROOMS, "*.json")) + glob.glob(os.path.join(T.ASSETS, "*.json"))
    for f in files:
        if os.path.basename(f) in ("check_windows.py",):
            continue
        txt = open(f, encoding="utf-8", errors="ignore").read().lower()
        for w in brands:
            if w in txt:
                ok_ctx = ("blocklist" in txt and w in ("paragon", "ekco")) or os.path.basename(f) in ("hw_models.py", "NOTES.md", "REVIEW-v1-street.md", "REVIEW-v1-close.md")          # the notes and the two try 1 reviews name the television's maker only to say its mark is painted out
                if not ok_ctx:
                    hits.append((os.path.basename(f), w))
    # glb node and material names
    for k, p in GLB.items():
        if os.path.exists(p):
            g = GL.Glb(p)
            for n in g.nodes:
                for w in brands + ["child", "toy"]:
                    if w in n.lower():
                        hits.append((k, n))
    row("CONTENT-01", not hits, "the content rule: no real firm's name (the target's blocklist), no drink, gambling, child or toy in the kit's scripts, notes, node names or room records; no person in any render (the review's eyes); hits: %s" % (hits or "none"))


def coplanar_pairs(g):
    """Pairs of different joinery parts with street-facing (normal -y) triangles on one plane, overlapping in area: {(part, part, axis, facing, plane): mm2}."""
    import itertools
    from collections import defaultdict
    tris = []
    for n, nd in g.nodes.items():
        if not n.startswith("paint_joinery"):
            continue
        pos = nd["pos"]
        for t in nd["tri"].reshape(-1, 3):
            p = pos[t]
            nrm = np.cross(p[1] - p[0], p[2] - p[0])
            ln = np.linalg.norm(nrm)
            if ln < 1e-9:
                continue
            nrm = nrm / ln
            ax = int(np.argmax(abs(nrm)))
            if abs(nrm[ax]) < 0.9999 or np.ptp(p[:, ax]) > 0.01:
                continue
            sg = int(np.sign(nrm[ax]))
            if not (ax == 1 and sg < 0):
                continue                      # only the faces that look at the street (normal -y): the others lie inside the brick (the linings' ends and tops) or behind the sash
            o = [i for i in range(3) if i != ax]
            tris.append((n, ax, sg, round(float(p[:, ax].mean()), 2), p[:, o].min(axis=0), p[:, o].max(axis=0)))
    grp = defaultdict(list)
    for t in tris:
        grp[(t[1], t[2], t[3])].append(t)
    found = {}
    for k, lst in grp.items():
        for a, b in itertools.combinations(lst, 2):
            if a[0] == b[0]:
                continue
            ov = np.minimum(a[5], b[5]) - np.maximum(a[4], b[4])
            if (ov > 0.05).all():
                key = tuple(sorted((a[0], b[0]))) + (k[0], k[1], k[2])
                found[key] = found.get(key, 0.0) + float(ov[0] * ov[1])
    return found


def extras(G):
    # KIT-16 normal maps are real, every textured primitive has UVs, no bump
    if not G:
        for rid, nm in (("KIT-16", "export: real normal maps, UVs, no bump"), ("KIT-17", "nothing floats in a kit piece")):
            not_run(rid, "kit glbs not built", name=nm)
        return
    bad = []
    for k, g in G.items():
        for m in g.j["materials"]:
            if "normalTexture" in m:
                ti = m["normalTexture"]["index"]
                im = np.asarray(g.image(g.j["textures"][ti]["source"]).convert("RGB")).astype(np.float64) / 255.0
                if im[..., 2].mean() < 0.7 or abs(im[..., 0].mean() - 0.5) > 0.1:
                    bad.append((k, m["name"], "blue %.2f" % im[..., 2].mean()))
            if "bump" in json.dumps(m).lower():
                bad.append((k, m["name"], "bump"))
        for n, nd in g.nodes.items():
            mi = [g.j["materials"][mm] if mm is not None else None for mm in [None]]
            for mat in nd["mat"]:
                mj = g.material(mat) if mat else {}
                textured = "baseColorTexture" in mj.get("pbrMetallicRoughness", {}) or "normalTexture" in mj
                if textured and np.isnan(nd["uv"]).any():
                    bad.append((k, n, "textured without UVs"))
                for t in (mj.get("pbrMetallicRoughness", {}).get("baseColorTexture"), mj.get("normalTexture")):
                    if t and t.get("texCoord", 0) < 0:
                        bad.append((k, n, "negative texCoord"))
    row("KIT-16", not bad, "every normalTexture in the four glbs is a real RGB normal map (blue over 0.7, red and green about 0.5), no bump in any exported material, every textured primitive has TEXCOORD_0 and no texCoord is negative; bad: %s" % (bad or "none"), name="export: real normal maps, UVs, no bump")
    # KIT-17 nothing floats: every net hangs from its rod, every rod from two brackets, every bracket on the lining or the wall
    fl = []
    for k, g in G.items():
        plane = 235.0 if k in ("RC", "RC2") else 254.0
        back = 250.8 if k in ("S22", "S11") else 215.0
        for nm, ztop in (("N1", 880), ("N2", 1630), ("N3", 500)):
            nlo, nhi = g.bbox("net__" + nm)
            rlo, rhi = g.bbox("net_rod__" + nm)
            if not (nhi[2] - 20.0 <= rlo[2] and rhi[2] <= nhi[2] and rlo[0] <= nlo[0] + 0.01 and rhi[0] >= nhi[0] - 0.01 and rlo[1] <= plane <= rhi[1]):
                fl.append((k, nm, "the rod is not in the net's head casing"))
            for side in ("L", "R"):
                blo, bhi = g.bbox("net_bracket__%s_%s" % (nm, side))
                touch_rod = blo[0] <= rhi[0] + 0.01 and bhi[0] >= rlo[0] - 0.01 and blo[2] <= rhi[2] and bhi[2] >= rlo[2]
                on_wall = abs(blo[1] - back) <= 0.5
                if not (touch_rod and on_wall):
                    fl.append((k, nm, side, "bracket"))
        plo, phi = g.bbox("curtain_pole")
        for nm in ("curtain__C1_drawn",):
            clo, chi = g.bbox(nm)
            if not (plo[2] <= chi[2] <= phi[2] + 0.01):
                fl.append((k, nm, "not on the pole"))
        for side in ("L", "R"):
            blo, bhi = g.bbox("curtain_bracket__" + side)
            if not (abs(blo[1] - 215.0) <= 0.5 and blo[2] <= phi[2] and bhi[2] >= plo[2] and blo[1] <= plo[1]):
                fl.append((k, "curtain bracket", side))
        for nm, hr, key in (("blind__B1", "blind_headrail__B1", 1650), ("blind__B3", "blind_headrail__B3", 1640)):
            clo, chi = g.bbox(nm)
            hlo, hhi = g.bbox(hr)
            if not (hlo[2] <= chi[2] <= hhi[2] + 0.01):
                fl.append((k, nm, "not on its headrail"))
        clo, chi = g.bbox("blind__B2")
        rlo, rhi = g.bbox("blind_roller__B2")
        if not (rlo[2] <= chi[2] <= rhi[2]):
            fl.append((k, "B2", "not on its roller"))
    row("KIT-17", not fl, "nothing floats in a kit piece: every net card's 20 mm head casing carries its rod (the rod ends in two brackets that stand on the lining's back or the wall's inner face), the curtain cards hang from the pole (brackets on the wall's inner face), each blind from its headrail or roller; loose: %s" % (fl or "none"), name="nothing floats in a kit piece")
    # KIT-19 no two parts share a street-side plane over an area
    big = []
    small = []
    for k, g in G.items():
        f = coplanar_pairs(g)
        for key, area in sorted(f.items(), key=lambda x: -x[1]):
            (big if area > 2000.0 else small).append((k, key[0].replace("paint_joinery__", ""), key[1].replace("paint_joinery__", ""), "%s%s %.1f" % ("-+"[key[3] > 0], "xyz"[key[2]], key[4]), round(area)))
    row("KIT-19", not big, "no two joinery parts of a kit piece have street-facing faces (normal -y) on one plane over an overlapping area above 2,000 mm2 (two faces on one plane shadow each other black in a path tracer: the first build's head lining on the side linings, 20,300 mm2, and bottom rail on the oak sill's riser, 26,500 mm2, made the black notch at the head of the far jamb); over: %s; the smaller ones left in the lab's sash (stile feet on the sill riser 1,569 mm2 and a bar on a rail 328 mm2, none seen black in any frame): %s" % (big or "none", small[:6] or "none"), name="no two parts share a plane")
    # NEG-02: the negative control of KIT-19: the first build's S22 (kept in the scratch folder, outside git) must fail it
    old_glb = os.path.join(T.SCRATCH, "kit_try1_glb", "hw_S22.glb")
    if os.path.exists(old_glb):
        f0 = coplanar_pairs(GL.Glb(old_glb))
        mx = max(f0.values()) if f0 else 0.0
        row("NEG-02", mx > 2000.0, "negative control: the first build's S22 (kit_try1_glb/hw_S22.glb) must FAIL KIT-19: its largest shared-plane overlap is %.0f mm2 (over 2,000)" % mx, name="negative control: the first build's shared planes fail KIT-19")
    else:
        not_run("NEG-02", "the first build's glb (scratch kit_try1_glb) is not there", name="negative control: the first build's shared planes fail KIT-19")
    # KIT-18 cloth folds irregular
    st = json.load(open(os.path.join(T.KITWORK, "cloth", "stats.json"))) if os.path.exists(os.path.join(T.KITWORK, "cloth", "stats.json")) else None
    if st:
        ok = True
        res = []
        for k, v in st.items():
            ok &= v["pitch_min"] >= v["rng"][0] - 1e-6 and v["pitch_max"] <= v["rng"][1] + 1e-6 and v["pitch_std"] >= 5.0 and v["depth_std"] > 0.5
            res.append("%s pitch %.0f to %.0f mm (sd %.1f), depth sd %.1f" % (k, v["pitch_min"], v["pitch_max"], v["pitch_std"], v["depth_std"]))
        row("KIT-18", ok, "folds are not a regular corrugation: " + "; ".join(res), name="net and curtain folds vary")
    else:
        not_run("KIT-18", "cloth stats not written", name="net and curtain folds vary")


def preview_rows():
    files = sorted(glob.glob(os.path.join(T.PREVIEWS, "hw-*-%s.jpg" % T.DATE2)))
    v1 = sorted(glob.glob(os.path.join(T.PREVIEWS, "hw-*-%s.jpg" % T.DATE)))
    bad = []
    for f in files + v1:
        im = Image.open(f)
        if im.width > 1600 or os.path.getsize(f) > 500 * 1024:
            bad.append((os.path.basename(f), im.size, os.path.getsize(f) // 1024))
    row("PRV-01", bool(files) and not bad, "%d review previews of try 2 (JPEG, at most 1600 px wide, under 500 KB): %s; the %d try 1 pictures stay beside them; bad: %s" % (len(files), ", ".join(os.path.basename(f) for f in files), len(v1), bad or "none"), name="the review set is in production/previews", status=None if files else "not_run")


def main():
    t0 = time.time()
    G = glbs()
    kit_rows(G)
    mat_rows(G)
    frames = frames_index()
    meas = measure_all(frames) if frames else {}
    wb_rows(frames, meas)
    night_rows(frames, meas)
    gls04(frames)
    lamp_row(frames)
    slot_row(frames)
    jnr_row(frames)
    acc_rows(meas)
    glass_rows()
    pic_rows()
    site_rows(frames)
    content_rows()
    extras(G)
    preview_rows()
    n_pass = sum(1 for r in ROWS if r["status"] == "pass")
    n_fail = [r for r in ROWS if r["status"] == "fail"]
    n_not = [r for r in ROWS if r["status"] == "not_run"]
    got = {r["id"] for r in ROWS}
    missing = [c for c in CHECK_IDS if c not in got]
    print("\n%d of %d rows pass (%d fail, %d not run; the target's own %d rows: %d pass)" % (n_pass, len(ROWS), len(n_fail), len(n_not), len(CHECK_IDS), sum(1 for r in ROWS if r["id"] in CHECK_IDS and r["status"] == "pass")))
    if missing:
        print("rows of the target never produced:", missing)
    if DRY:
        return 0
    os.makedirs(T.CHECKS, exist_ok=True)
    out = {"made": time.strftime("%Y-%m-%d %H:%M:%S"), "pass": n_pass, "total": len(ROWS), "fail": [r["id"] for r in n_fail], "not_run": [r["id"] for r in n_not], "target_rows": len(CHECK_IDS), "rows": ROWS,
           "seconds": round(time.time() - t0, 1), "measurements": {t: {s: {k: v for k, v in st.items() if k != "bbox"} for s, st in ws.items()} for t, ws in meas.items()}}
    json.dump(out, open(os.path.join(T.CHECKS, "check_windows_v2.json"), "w"), indent=1, default=float)
    return 0 if not n_fail and not n_not else 1


if __name__ == "__main__":
    main()
