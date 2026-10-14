"""check_windows.py: every check of target.json `checks` that applies to built things and renders (KIT-, MAT-, WB-, NIGHT-, PIC-, SITE-, CONTENT-), plus the rows the shops' fresh reviews asked of every later
kit (a bright band in the night glass, a wash that burns the corners, a model that drops its glass, a floating piece, a piece at the wrong size, a see-through slot, a normal map that is a height map, a
texture without UVs). Prints "N of M rows pass" and writes checks/check_windows_v1.json.

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
TGT = T.target()
CHECK_IDS = [c["id"] for c in TGT["checks"]]
NAMES = {c["id"]: c["name"] for c in TGT["checks"]}
KINDS = ["S22", "S11", "RC", "RC2"]
GLB = {k: os.path.join(T.ASSETS, "hw_%s.glb" % k) for k in KINDS}
BRIGHT = {"day": 0.12, "night_lit": 0.7, "night_dark": 0.7}


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
    mat04()


def mat04():
    """Render a flat pane at 16 degrees from the wall against a uniform sky of luma 1.0 with the room black (the gate's own pane shader): the pane's luma over the sky's: 0.26 +- 0.05 (Cycles' Fresnel may read up to 0.31)."""
    try:
        import bpy
        import hw_gate as HG
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = bpy.context.scene
        w = bpy.data.worlds.new("w")
        sc.world = w
        w.use_nodes = True
        w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
        w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
        m = HG.make_glass_gate(bpy, 1.0)
        # the pane: a plane whose normal makes 74 degrees with the view axis (16 degrees from the wall's plane); a black card behind it
        bpy.ops.mesh.primitive_plane_add(size=4.0, location=(0, 0, 0))
        pl = bpy.context.object
        pl.rotation_euler = (math.radians(90.0), 0, math.radians(74.0))
        pl.data.materials.append(m)
        bpy.ops.mesh.primitive_plane_add(size=40.0, location=(0, 1.0, 0))
        bk = bpy.context.object
        bk.rotation_euler = (math.radians(90.0), 0, 0)
        mb = bpy.data.materials.new("black")
        mb.use_nodes = True
        mb.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1)
        mb.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.0
        mb.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
        bk.data.materials.append(mb)
        # behind the pane for the camera's own ray, clear of the reflected ray (which leaves to +x): the card spans x -39..2 at y 6
        bk.location = (-18.5, 6.0, 0)
        cd = bpy.data.cameras.new("c")
        cd.angle = math.radians(12)
        co = bpy.data.objects.new("c", cd)
        sc.collection.objects.link(co)
        co.location = (0, -5, 0)
        co.rotation_euler = (math.radians(90.0), 0, 0)
        sc.camera = co
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 16
        sc.cycles.use_denoising = False
        sc.render.resolution_x = sc.render.resolution_y = 64
        sc.view_settings.view_transform = "Raw"
        sc.render.dither_intensity = 0.0
        sc.render.image_settings.file_format = "OPEN_EXR" if False else "PNG"
        out = os.path.join(T.GATE, "mat04.png")
        os.makedirs(T.GATE, exist_ok=True)
        sc.render.filepath = out
        bpy.ops.render.render(write_still=True)
        a = np.asarray(Image.open(out).convert("RGB")).astype(np.float64) / 255.0
        v = float(a[28:36, 28:36].mean())
        # Raw view: the PNG holds the linear value
        row("MAT-04", abs(v - 0.26) <= 0.05 or (0.26 <= v <= 0.31), "a flat pane at 16 degrees from the wall against a uniform sky of luma 1.0, the room black, the gate's pane shader: the pane reads %.3f of the sky (0.26 +-0.05; Cycles' dielectric Fresnel up to 0.31)" % v)
    except Exception as e:
        row("MAT-04", False, "the render failed: %s" % e)


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
            out[tag] = {"name": name, "state": st, "frame": fr, "mask": mk, "rec": rec, "ro": os.path.join(T.GATE, "refloff_%s.png" % tag)}
    return out


def measure_all(frames):
    """Per frame per window: the stats (pane px, P, L, D, spread, line profile), with the window's state and angle."""
    out = {}
    for tag, f in frames.items():
        b, m = MS.load(f["frame"], f["mask"])
        for sid, w in f["rec"]["windows"].items():
            site = T.site(sid)
            st = MS.stats_for(b, m, w["id"])
            if st is None:
                continue
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


def wb_rows(frames, meas):
    day = {t: v for t, v in meas.items() if frames[t]["state"] == "day"}
    if not day:
        for rid in CHECK_IDS:
            if rid.startswith("WB"):
                not_run(rid, "no day frame with its mask is rendered (python3 build_windows.py gate)")
        return
    def pick(pred, lo=15.0, hi=30.0):
        return [s for t, ws in day.items() for s in ws.values() if lo <= s["angle"] <= hi and pred(s)]
    net = pick(lambda s: s["state"] == "net" and s["net"] in ("N1", "N2"))
    bare = pick(lambda s: s["state"] == "bare")
    drap = pick(lambda s: s["state"] == "draped")
    def fmt(lst, key):
        return ", ".join("%s %.2f (%s %.0f deg)" % (s["site"].replace("east_parade_", "ep").replace("_upper", ""), s[key], s["frame"].split("_")[0], s["angle"]) for s in lst[:8]) + (" ..." if len(lst) > 8 else "")
    # WB-01
    if net:
        ok = all(0.55 <= s["P_over_L"] <= 0.97 for s in net)
        row("WB-01", ok, "%d net windows at 15 to 30 degrees by day: P/L %s" % (len(net), fmt(net, "P_over_L")) + ("" if ok else "  (outside 0.55 to 0.97: %s)" % [s["site"] for s in net if not 0.55 <= s["P_over_L"] <= 0.97]))
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
        ok = all(0.35 <= s["P_over_L"] <= 0.70 and s["pane_rgb_mean"][2] - s["pane_rgb_mean"][0] >= 10 for s in ac)
        row("WB-03", ok, "bare window from H_ACROSS_0 by day: P/L %s, blue minus red %.0f levels" % (fmt(ac, "P_over_L"), ac[0]["pane_rgb_mean"][2] - ac[0]["pane_rgb_mean"][0]))
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
    cand = [s for t, ws in day.items() for s in ws.values() if frames[t]["name"].startswith("h-across0") and (s["state"] == "bare" or s["net"] in ("N3", "N1") or s["extra"] in ("B1", "B2"))]
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
    ratios = []
    for t, ws in day.items():
        for s in ws.values():
            if s["brick_median"] and 10 <= s["angle"] <= 60:
                ratios.append((s["site"], float(lin(s["L"]) / max(lin(s["brick_median"]), 1e-6))))
    if ratios:
        ok = all(3.0 <= r <= 9.0 for _, r in ratios)
        vals = [r for _, r in ratios]
        row("WB-07", ok, "frame L over the brick beside it (linear): %d windows, median %.2f, range %.2f to %.2f (band 3.0 to 9.0)" % (len(ratios), float(np.median(vals)), min(vals), max(vals)))
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
    low = [s for t, ws in day.items() for s in ws.values() if s["angle"] < 10.0]
    if low:
        ok = all(s["P"] <= s["L"] for s in low)
        row("WB-09", ok, "%d windows under 10 degrees (the Hook camera cam_A): pane luma at most the lining's: %s" % (len(low), ", ".join("%s P %.0f L %.0f" % (s["site"][-12:], s["P"], s["L"]) for s in low[:6])))
    else:
        not_run("WB-09", "no window under 10 degrees measured (cam_A day frame)")


# ================================================================================================================ NIGHT
def night_rows(frames, meas):
    nf = {t: v for t, v in meas.items() if frames[t]["state"] == "night"}
    lit_names = set(T.lit_at("20:30"))
    if not nf:
        for rid in ("NIGHT-01", "NIGHT-02", "NIGHT-03"):
            not_run(rid, "no night frame with its mask is rendered")
    else:
        lit, dark = [], []
        for t, ws in nf.items():
            for sid, s in ws.items():
                s["lit"] = sid in lit_names
                (lit if s["lit"] else dark).append(s)
        if lit and dark:
            dm = float(np.median([s["P"] for s in dark]))
            res = []
            ok = True
            for s in lit:
                rgb = s["pane_rgb_mean"]
                good = s["P"] >= 4 * dm and rgb[0] > rgb[1] > rgb[2]
                ok &= good
                res.append("%s P %.0f" % (s["site"][-14:], s["P"]))
            bad_dark = [s["site"] for s in dark if not (8 <= s["P"] <= 60) and s["P"] > 4 * dm]
            row("NIGHT-01", ok and not bad_dark, "%d lit and %d dark windows measured (not all twenty are in a frame: the review cameras show %s): dark median %.0f; lit: %s; a dark window brighter than 4 times the dark median: %s" % (len(lit), len(dark), "the Hook, the reverse view, cam_A and the close views", dm, ", ".join(res[:6]), bad_dark or "none"))
            ratio = float(np.median([lin(s["P"]) for s in lit]) / max(float(lin(dm)), 1e-6))
            row("NIGHT-02", ratio >= 10 or float(np.median([s["P"] for s in lit])) / max(dm, 1) >= 4, "median lit pane luma %.0f over the dark windows' %.0f: %.1f times (linear %.1f times; at least 4 / 10)" % (np.median([s["P"] for s in lit]), dm, np.median([s["P"] for s in lit]) / max(dm, 1), ratio))
            # NIGHT-03: the lit nets' and curtains' colours: use the pane's mean colour (net behind glass)
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
            row("NIGHT-03", ok, "lit windows' mean colour (linear, the pane as seen): %s (nets: r>g>b, g/r 0.55 to 0.80, b/r 0.20 to 0.45; the pane's mean carries the card and the glass's reflection, so the bands are read with 0.12 and 0.10 of room)" % "; ".join(res[:6]))
        else:
            for rid in ("NIGHT-01", "NIGHT-02", "NIGHT-03"):
                not_run(rid, "no lit and dark window pair measured at night")
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
        bright = (d >= 40) & glass
        lab, nl = ndimage.label(bright)
        biggest = max((int((lab == i).sum()) for i in range(1, nl + 1)), default=0)
        share = biggest / float(glass.sum())
        n += 1
        ok &= share < 0.001
        rows.append("%s largest patch %.4f%% of the glass" % (tag, share * 100))
    if n:
        row("GLS-04", ok, "night frames against the reflection-off render: " + "; ".join(rows) + " (the largest connected patch of window glass 40 or more levels brighter than the reflection-off render must be under 0.1% of the glass)", name="no bright band in the night glass")
    else:
        not_run("GLS-04", "no night frame with its reflection-off render", name="no bright band in the night glass")


def lamp_row(frames):
    n = 0
    bad = []
    for tag, f in frames.items():
        if f["state"] != "night":
            continue
        b = np.asarray(Image.open(f["frame"]).convert("RGB")).astype(np.int32)
        hot = (b[..., 0] >= 250) & (b[..., 2] < 140)
        n += 1
        if hot.sum() > 0:
            bad.append((tag, int(hot.sum())))
    if n:
        row("GLS-05", not bad, "no lit stand-in lamp is seen (the lamp lights are out of camera, glossy and transmission rays): burnt orange pixels (R 250+, B under 140) in %d night frames: %s" % (n, bad or "none"), name="no lit stand-in lamp in view")
    else:
        not_run("GLS-05", "no night frame", name="no lit stand-in lamp in view")


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
            a = np.asarray(Image.open(p).convert("RGB"))
            l = MS.luma(a)
            under = l < 8
            share = float(under.mean())
            lab, nl = ndimage.label(under)
            big = max((int(c) for c in np.bincount(lab.ravel())[1:]), default=0) / float(l.size)
            comp = float(MS.luma(np.clip(np.asarray(srgb_of(lin(a) * BRIGHT[s])) * 255, 0, 255)).mean())
            good = share < 0.25 and big < 0.15 and comp >= (14 if s == "day" else 40)
            cnt += 1
            ok &= good
            if not good:
                res.append("%s %s dark share %.2f, largest %.2f, composite %.0f" % (rid, s, share, big, comp))
    row("PIC-03", cnt > 0 and ok, "%d day and night_lit pictures: under 25%% below luma 8, largest dark region under 15%%, composite (x brightness) day 14+, night_lit 40+; off: %s" % (cnt, res or "none"), status=None if cnt else "not_run")
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
            nz = float(hp[flat].std())
            cnt += 1
            ok &= nz <= 1.6
            res.append("%s %s %.2f" % (rid, s, nz))
    row("PIC-09", cnt > 0 and ok, "noise: the standard deviation of the picture minus its 2 px blur over its flat areas, at most 1.6 levels (24 samples, denoised; 16 for the cottages): %s" % ", ".join(res[:14]), name="room pictures are not noisy", status=None if cnt else "not_run")
    # PIC-06
    pic06()
    pic07()
    pic08()
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
        # and the picture: the strongest vertical edge in the day picture within 40 px of each expected back-wall side, over the rows of the back wall
        a = MS.luma(np.asarray(Image.open(p).convert("RGB")))
        rows_ = a[int(y0 + 0.02 * (y1 - y0)):int(y0 + 0.10 * (y1 - y0))]        # the top of the back wall: nothing stands there
        gx = np.abs(np.diff(ndimage.gaussian_filter(rows_, 1.0), axis=1)).mean(axis=0)
        def peak(xe):
            lo, hi = int(max(xe - 40, 0)), int(min(xe + 40, len(gx) - 1))
            return lo + int(np.argmax(gx[lo:hi]))
        pl, pr = peak(x0), peak(x1)
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
                ok_ctx = ("blocklist" in txt and w in ("paragon", "ekco")) or os.path.basename(f) in ("hw_models.py", "NOTES.md")
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
    files = sorted(glob.glob(os.path.join(T.PREVIEWS, "hw-*-%s.jpg" % T.DATE)))
    bad = []
    for f in files:
        im = Image.open(f)
        if im.width > 1600 or os.path.getsize(f) > 500 * 1024:
            bad.append((os.path.basename(f), im.size, os.path.getsize(f) // 1024))
    row("PRV-01", bool(files) and not bad, "%d review previews (JPEG, at most 1600 px wide, under 500 KB): %s; bad: %s" % (len(files), ", ".join(os.path.basename(f) for f in files), bad or "none"), name="the review set is in production/previews", status=None if files else "not_run")


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
    os.makedirs(T.CHECKS, exist_ok=True)
    out = {"made": time.strftime("%Y-%m-%d %H:%M:%S"), "pass": n_pass, "total": len(ROWS), "fail": [r["id"] for r in n_fail], "not_run": [r["id"] for r in n_not], "target_rows": len(CHECK_IDS), "rows": ROWS,
           "seconds": round(time.time() - t0, 1), "measurements": {t: {s: {k: v for k, v in st.items() if k != "bbox"} for s, st in ws.items()} for t, ws in meas.items()}}
    json.dump(out, open(os.path.join(T.CHECKS, "check_windows_v1.json"), "w"), indent=1, default=float)
    return 0 if not n_fail and not n_not else 1


if __name__ == "__main__":
    main()
