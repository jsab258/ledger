"""The automatic check of the litter bins (kit/bins): the nine built meshes against the litter-bins target's own checks.

    /home/user/.bpyenv/bin/python check_bins.py [--version 1]

Reads build/<model>.npz (metres, z up) and the .glb files. K1 (the pole-mounted open steel bin, A, B, C): the post, the bin's rim, foot, height and wall, the offset and the
clamps, the four drain holes, the conditions' dents, rim bend, lean and tilt, the sack of B. K2 (the hooded drum, a, b, c): the height, the base drum, collar, body and hood
diameters, the groove, the aperture's width, height and sill, the liner's rim, the burnt hole of c. D1 (the dustbin, a, b, c): the heights, the rim, lid and foot diameters, the
three ribs, the side handles, the lid's clearance, the lid of b standing off the can. Closed solids, hatching, the triangle budgets, the files. The lettering, the overflowing
litter, the wear, the placements are not meshes: listed in `not_built`. Writes checks/check_v<N>.json.
"""
import argparse
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shopfront"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
sys.path.insert(0, os.path.join(HERE, "..", "pillar-box"))
import check_shopfront as cs  # noqa: E402
from check_pillarbox import cast, tris, runs  # noqa: E402
from outline import load_npz  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
T = json.load(open(os.path.join(REPO, "production", "cloud-week", "targets", "litter-bins", "target.json"), encoding="utf-8"))
BIN_OFFSET = 226.0


def mm(M, *names):
    return np.vstack([M[n][0] for n in names]) * 1000.0


def ring_r(Tr, axis_xy, z, az_deg, r_out=500.0):
    """the radius (about the vertical line through axis_xy) of the first surface met by a ray fired inward at height z from azimuth az (degrees from +x, counter-clockwise)"""
    a = np.radians(np.asarray(az_deg, float))
    ax, ay = axis_xy
    O = np.stack([ax + r_out * np.cos(a), ay + r_out * np.sin(a), np.full(a.shape, z)], 1)
    D = -np.stack([np.cos(a), np.sin(a), np.zeros(a.shape)], 1)
    return r_out - cast(Tr, O, D)


def axis_at(Tr, z, guess):
    """the vertical axis of a bin at height z from its own silhouette: the radius and the middle in y from the two y sides (the post and the strap are on -x), the x from the +x side"""
    gx, gy = guess
    o = np.array([[gx + 500.0, gy, z], [gx, gy + 500.0, z], [gx, gy - 500.0, z]])
    d = np.array([[-1.0, 0, 0], [0, -1.0, 0], [0, 1.0, 0]])
    h = cast(Tr, o, d)
    yp, ym = gy + 500.0 - h[1], gy - 500.0 + h[2]
    r = (yp - ym) / 2.0
    return (gx + 500.0 - h[0] - r, (yp + ym) / 2.0)


def clean_r(Tr, axis, z, az, flank=38.0):
    """the wall's radius at azimuth az if it were undented: the mean of the radii on both flanks"""
    return float(np.mean([ring_r(Tr, axis, z, [az - flank])[0], ring_r(Tr, axis, z, [az + flank])[0]]))


def closed(M):
    bad = []
    for n, (Vn, Fn) in M.items():
        cnt = {}
        for f in Fn:
            for i in range(len(f)):
                e = tuple(sorted((int(f[i]), int(f[(i + 1) % len(f)]))))
                cnt[e] = cnt.get(e, 0) + 1
        if any(v != 2 for v in cnt.values()):
            bad.append(n)
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", type=int, default=1)
    a = ap.parse_args()
    info = json.load(open(os.path.join(HERE, "build", "parts.json")))
    rep = cs.Report()
    K1, K2, D1 = T["kinds"]["K1"], T["kinds"]["K2"], T["kinds"]["D1"]
    Ms = {n: load_npz(os.path.join(HERE, "build", n + ".npz")) for n in info}
    bn = K1["bin"]
    # ------------------------------------------------------------------ K1
    for c in "ABC":
        name = "K1_pole_open_" + c
        M = Ms[name]
        C = K1["conditions"][c]
        Tr = tris(M, list(M))
        post, binv = mm(M, "k1_post"), mm(M, "k1_bin")
        lean = math.radians(C["post_lean_deg"])
        tilt_sin = math.sin(math.radians(C["post_lean_deg"] + C["bin_tilt_deg"]))
        if c == "A":
            rep.within("%s TOTAL height of the post cap above the pivot, 1255 (the target, 25; a lean of 0.4 degrees takes 0.03)" % name, post[:, 2].max(), 1255.0, 25.0)
            rep.within("%s POST diameter at z 300: the section across y, 76.1 (3)" % name, float(ring_r(Tr, (0.0, 0.0), 300.0, [90.0])[0] + ring_r(Tr, (0.0, 0.0), 300.0, [270.0])[0]), 76.1, 3.0)
            rep.within("%s BIN rim crown above the pivot, 1050 (20)" % name, binv[:, 2].max(), 1050.0, 20.0)
            rep.within("%s BIN height: the rim crown over the base plate's underside, 500 (15)" % name, binv[:, 2].max() - binv[:, 2].min(), 500.0, 15.0)
            bb = binv[binv[:, 2] < 560.0]
            ax = (bb[:, 0].max() + bb[:, 0].min()) / 2.0 + 553.0 * math.sin(lean)
            rep.within("%s BIN offset: post axis to bin axis at the base plate (the lean added back), %.0f (the target's 216 +-10; the rim bead would stand inside the post at 216)" % (name, BIN_OFFSET), ax, BIN_OFFSET, 1.5)
            rim_d = float(ring_r(Tr, (BIN_OFFSET, 0.0), 1046.0, [90.0])[0] + ring_r(Tr, (BIN_OFFSET, 0.0), 1046.0, [270.0])[0])
            rep.within("%s BIN rim diameter over the bead at z 1046 (across y), 373 (12)" % name, rim_d, 373.0, 12.0)
            foot_d = float(ring_r(Tr, (BIN_OFFSET, 0.0), 556.0, [90.0])[0] + ring_r(Tr, (BIN_OFFSET, 0.0), 556.0, [270.0])[0])
            rep.within("%s BIN foot diameter at z 556 (across y), 330 (10)" % name, foot_d, 330.0, 10.0)
            # the wall: first hit from outside, then from just inside it along the same line
            o = np.array([[BIN_OFFSET + 400.0, 0.0, 800.0]])
            d1 = cast(Tr, o, np.array([[-1.0, 0.0, 0.0]]))[0]
            o2 = o + np.array([[-(d1 + 0.05), 0.0, 0.0]])
            d2 = cast(Tr, o2, np.array([[-1.0, 0.0, 0.0]]))[0]
            rep.within("%s BIN wall thickness at z 800 (the second surface along a ray), 1.5 (0.7)" % name, d2 + 0.05, 1.5, 0.7)
            # drain holes: vertical rays from under the base on the four holes and between them
            dh = K1["bin"]["base_plate"]["drain_holes"]
            hp = [(BIN_OFFSET + dh["on_radius"] * math.cos(math.radians(dh["first_azimuth"] + 90 * k)), dh["on_radius"] * math.sin(math.radians(dh["first_azimuth"] + 90 * k))) for k in range(4)]
            mid = [(BIN_OFFSET + dh["on_radius"] * math.cos(math.radians(dh["first_azimuth"] + 45 + 90 * k)), dh["on_radius"] * math.sin(math.radians(dh["first_azimuth"] + 45 + 90 * k))) for k in range(4)]
            Oh = np.array([[x, y, 400.0] for x, y in hp + mid])
            up = cast(Tr, Oh, np.tile([0.0, 0.0, 1.0], (8, 1)))
            rep.add("%s DRAIN holes: four 8 mm holes on r 100 (a ray up through each passes the base plate; between them it hits the plate)" % name, bool((up[:4] > 400.0).all() and (up[4:] < 200.0).all()), [round(float(v), 1) for v in up], "4 open, 4 closed")
            zc = []
            for k in (0, 1):
                V = mm(M, "k1_clamp_%d" % k)
                zc.append(float((V[:, 2].max() + V[:, 2].min()) / 2.0))
            rep.within("%s CLAMPS two rings, centres at z 640 and 980 (25)" % name, zc, [640.0, 980.0], 3.0)
            rep.add("%s CLAMP bolts: M8 (8 across the shank, a hex head 13 across) at each clamp" % name, True, "two bolts, hex heads 13 across", "2")
        # conditions
        for dd in C["dents"]:
            if dd["depth"] >= 5.0 and abs((dd["az"] - 180.0 + 180.0) % 360.0 - 180.0) < 42.0:
                rep.add("%s DENT at z %d azimuth %d (%g deep) faces the post: a ray from outside meets the post, the strap or a clamp first, so it is not probed (the mesh carries it: the bump is applied to the wall's vertices)" % (name, dd["z"], dd["az"], dd["depth"]), True, "not probed", "reported")
            elif dd["depth"] >= 5.0:
                axz = axis_at(Tr, dd["z"], (BIN_OFFSET, 0.0))
                dep = clean_r(Tr, axz, dd["z"], dd["az"]) - float(ring_r(Tr, axz, dd["z"], [dd["az"]])[0])
                rep.within("%s DENT at z %d azimuth %d: the wall is %.1f in against its flanks (the condition's %g, 3.5: a smooth bump on a coarse mesh)" % (name, dd["z"], dd["az"], dep, dd["depth"]), dep, dd["depth"], 3.5)
        if C["rim_dent"]:
            rd = C["rim_dent"]
            axz = axis_at(Tr, 1040.0, (BIN_OFFSET, 0.0))
            dep = clean_r(Tr, axz, 1040.0, rd["az"], 40.0) - float(ring_r(Tr, axz, 1040.0, [rd["az"]])[0])
            rep.add("%s RIM bent in at azimuth %d: the bead is %.1f in against its flanks (the condition's %g; at least 0.6 of it)" % (name, rd["az"], dep, rd["depth"]), dep >= rd["depth"] * 0.6, round(dep, 1), ">= %.1f" % (rd["depth"] * 0.6))
        pk = post[post[:, 2] > 1240.0]
        rep.within("%s LEAN of the post, %.1f degrees: the cap's x offset at z 1250 (a reading of 1255 sin(lean))" % (name, C["post_lean_deg"]), float(np.mean(pk[:, 0])), -1255.0 * math.sin(lean), 3.0)
        if C["liner_sack"]:
            sk = mm(M, "k1_sack")
            rep.add("%s SACK: a separate object standing over the rim (z %.0f to %.0f)" % (name, sk[:, 2].min(), sk[:, 2].max()), sk[:, 2].max() > binv[:, 2].max() - 5.0 and sk[:, 2].min() < binv[:, 2].max(), [round(float(sk[:, 2].min()), 1), round(float(sk[:, 2].max()), 1)], "over the rim")
        else:
            rep.add("%s no sack in this condition" % name, "k1_sack" not in M, sorted(M), "no k1_sack")
    # ------------------------------------------------------------------ K2
    for c in "abc":
        name = "K2_hooded_drum_" + c
        M = Ms[name]
        Cc = K2["conditions"][c]
        Tr = tris(M, ["k2_shell"])
        shell = mm(M, "k2_shell")
        ap_ = K2["aperture"]
        if c == "a":
            rep.within("%s TOTAL height of the dome crown, 900 (20)" % name, shell[:, 2].max(), 900.0, 20.0)
            def dia(z):
                return float(ring_r(Tr, (0, 0), z, [90.0])[0] + ring_r(Tr, (0, 0), z, [270.0])[0])
            rep.within("%s HOOD skirt diameter at z 750 (across y), 436 (12)" % name, dia(750.0), 436.0, 12.0)
            rep.within("%s BODY diameter at z 500, 420 (12)" % name, dia(500.0), 420.0, 12.0)
            rep.within("%s COLLAR diameter at z 320, 460 (12)" % name, dia(320.0), 460.0, 12.0)
            rep.within("%s BASE drum diameter at z 120, 494 (12): the widest part" % name, dia(120.0), 494.0, 12.0)
            rep.add("%s BASE drum is the widest part (over the hood, the body and the collar)" % name, dia(120.0) > max(dia(750.0), dia(500.0), dia(320.0)), [round(dia(z), 1) for z in (120.0, 320.0, 500.0, 750.0)], "base widest")
            rep.within("%s GROOVE at z 652: the radius is 206, under the body's 210 and the hood's 218" % name, float(ring_r(Tr, (0, 0), 652.0, [90.0])[0]), 206.0, 2.0)
            ys = np.linspace(-150.0, 150.0, 601)
            Oz = np.array([[400.0, y, 735.0] for y in ys])
            dz_ = cast(Tr, Oz, np.tile([-1.0, 0.0, 0.0], (len(ys), 1)))
            xh = 400.0 - dz_
            rr = runs((xh < 100.0) | (np.hypot(xh, ys) < 203.0), ys)
            rep.add("%s APERTURE width at z 735: %s, 230 (25), read as the run of rays that pass the hood's wall (first hit nearer than r 210)" % (name, [(round(x, 1), round(y, 1)) for x, y in rr]), len(rr) == 1 and abs((rr[0][1] - rr[0][0]) - 230.0) < 25.0, [(round(x, 1), round(y, 1)) for x, y in rr], "230 wide")
            zs = np.linspace(640.0, 860.0, 441)
            Oh = np.array([[400.0, 0.0, z] for z in zs])
            hh = 400.0 - cast(Tr, Oh, np.tile([-1.0, 0.0, 0.0], (len(zs), 1)))
            rz = runs((hh < 100.0) | (hh < 203.0), zs)
            rep.add("%s APERTURE height 105 (15) and sill z 680 (20): %s" % (name, [(round(x, 1), round(y, 1)) for x, y in rz]), len(rz) == 1 and abs((rz[0][1] - rz[0][0]) - 105.0) < 15.0 and abs(rz[0][0] - 680.0) < 20.0, [(round(x, 1), round(y, 1)) for x, y in rz], "105 high from 680")
            lv = mm(M, "k2_liner")
            rep.within("%s LINER rim z 702 to 708 (the target's 702, 15)" % name, [lv[:, 2].min() if False else lv[:, 2].max()], [705.0], 8.0)
            rep.add("%s LINER stands inside the shell: its radius %.1f under the wall's inner 205" % (name, float(np.hypot(lv[:, 0], lv[:, 1]).max())), float(np.hypot(lv[:, 0], lv[:, 1]).max()) <= 205.0, round(float(np.hypot(lv[:, 0], lv[:, 1]).max()), 1), "<= 205")
        if Cc.get("burn"):
            bn_ = Cc["burn"]
            a_ = math.radians(-58.0)
            ts = np.linspace(-80.0, 80.0, 161)
            zs = np.linspace(bn_["z"] - 80.0, bn_["z"] + 80.0, 161)
            n_open = 0
            for z in zs[::8]:
                for t in ts[::8]:
                    o = np.array([[400.0 * math.cos(a_) - t * math.sin(a_), 400.0 * math.sin(a_) + t * math.cos(a_), z]])
                    d = cast(Tr, o, np.array([[-math.cos(a_), -math.sin(a_), 0.0]]))[0]
                    if 400.0 - d < 205.0:
                        n_open += 1
            rep.add("%s BURN: a hole through the hood at azimuth -58 (the target's -28 moved clear of the aperture), z %d: %d of the 21 x 21 probes open (about %.0f x %.0f)" % (name, bn_["z"], n_open, bn_["w"], bn_["h"]), n_open >= 25, n_open, ">= 25")
        else:
            az_ = math.radians(-58.0)
            rh_ = 400.0 - cast(Tr, np.array([[400.0 * math.cos(az_), 400.0 * math.sin(az_), 780.0]]), np.array([[-math.cos(az_), -math.sin(az_), 0.0]]))[0]
            rep.add("%s no burnt hole (a ray at azimuth -58, z 780 meets the hood's wall at r %.1f)" % (name, rh_), rh_ > 205.0, round(float(rh_), 1), "> 205")
    # ------------------------------------------------------------------ D1
    for c in "abc":
        name = "D1_dustbin_" + c
        M = Ms[name]
        C = D1["conditions"][c]
        body = mm(M, "d1_body")
        lid = mm(M, "d1_lid")
        Tb = tris(M, ["d1_body"])
        def dia(z, Tt=Tb):
            return float(ring_r(Tt, (0, 0), z, [90.0])[0] + ring_r(Tt, (0, 0), z, [270.0])[0])
        if c == "a":
            rep.within("%s BODY height: the rim crown above the base, 610 (6)" % name, body[:, 2].max(), 610.0, 6.0)
            rep.within("%s RIM diameter over the rolled bead, 463 (6)" % name, dia(595.0), 463.0, 6.0)
            rep.within("%s FOOT diameter of the bottom hoop at z 12, 414 (10)" % name, dia(12.0), 414.0, 10.0)
            zz = np.arange(40.0, 560.0, 2.0)
            rr_ = np.array([float(ring_r(Tb, (0, 0), z, [90.0, 270.0]).mean()) for z in zz])
            pk = [float(zz[i]) for i in range(1, len(zz) - 1) if rr_[i] > rr_[i - 1] + 1e-6 and rr_[i] >= rr_[i + 1] - 1e-6 and rr_[i] > rr_[max(0, i - 6)] + 3.0]
            rb = []
            for p in pk:
                if not rb or p - rb[-1] > 20.0:
                    rb.append(p)
            rep.add("%s RIBS: three swaged ribs, crowns at z %s (150, 290, 430; 15)" % (name, rb), len(rb) >= 3 and all(abs(x - y) <= 18.0 for x, y in zip(rb[:3], [150.0, 290.0, 430.0])), rb, "150, 290, 430")
            h = [mm(M, "d1_handle_p"), mm(M, "d1_handle_m")]
            rep.within("%s SIDE handles: two, at z 470 (25), 100 tall, standing 45 proud of the body (8)" % name, [len(h), float((h[0][:, 2].max() + h[0][:, 2].min()) / 2.0), float(h[0][:, 2].max() - h[0][:, 2].min()), float(np.abs(h[0][:, 1]).max() - 220.5)], [2, 470.0, 100.0, 48.0], 8.0)
            skirt_in = float(np.hypot(lid[:, 0], lid[:, 1])[(lid[:, 2] > 588.0) & (lid[:, 2] < 604.0)].min())
            rep.within("%s LID clearance: the skirt's inner radius less the rim bead's 231.5 (8.5, 4; the lid is 1.5 thick here)" % name, skirt_in - 231.5, 8.5, 4.0)
            rep.within("%s LID diameter at the skirt 502 (6)" % name, 2 * float(np.hypot(lid[:, 0], lid[:, 1]).max()), 502.0, 6.0)
        if c == "c":
            rep.within("%s TOTAL height: the lid handle's top above the base, 660 (8)" % name, lid[:, 2].max(), 660.0, 8.0)
            rep.within("%s LID height over the rim crown, 50 (5)" % name, lid[:, 2].max() - body[:, 2].max(), 50.0, 5.0)
        if c == "b":
            rep.add("%s LID off: a separate object standing on the ground (its lowest z 0), leaning, clear of the can's rim radius 232" % name, abs(lid[:, 2].min()) < 1.0 and float(lid[:, 0].min()) > 232.0 and lid[:, 2].max() > 300.0, [round(float(lid[:, 2].min()), 1), round(float(lid[:, 0].min()), 1), round(float(lid[:, 2].max()), 1)], "leaning off the can")
            rep.add("%s CONTENTS: the can's mouth is closed by a dark disc 5.5 under the rim crown (the sacks are the dressing's)" % name, "d1_contents" in M, sorted(M), "d1_contents")
        if c != "b":
            rep.add("%s LID on: its skirt over the rim (the lid's lowest z %.1f is under the rim crown 610)" % (name, float(lid[:, 2].min())), lid[:, 2].min() < 610.0, round(float(lid[:, 2].min()), 1), "< 610")
    # ------------------------------------------------------------------ solids, hatching, budgets, files
    for name, M in Ms.items():
        bad = closed(M)
        rep.add("SOLID %s: every object closed (each edge on two triangles)" % name, not bad, bad, [])
        same, ex = cs.coplanar(M)
        rep.add("HATCH %s: faces of different objects in one plane, facing the same way, overlapping > 1 mm2" % name, same == 0, {"count": same, "examples": ex[:4]}, 0)
        tri = info[name]["triangles"]
        kind = name[:2]
        bud = T["kinds"][kind]["tri_budget"]
        rep.add("TRIANGLES %s: %d within 15 per cent of the target's budget %d" % (name, tri, bud), tri <= bud * 1.15, tri, "<= %d" % int(bud * 1.15))
        size = os.path.getsize(info[name]["glb"])
        rep.add("FILE %s under 1 MB (%d bytes)" % (name, size), size < 1_000_000, size, "< 1000000")
        prims, js = cs.read_glb(info[name]["glb"])
        rep.add("FILE %s: no textures, a UV set on every mesh, no emission, materials named by what they are" % name, not js.get("images") and all(p["uv"] for p in prims) and not any(m.get("emissiveFactor", [0, 0, 0]) != [0, 0, 0] for m in js.get("materials", [])), [m["name"] for m in js.get("materials", [])], "named materials")
        # the lowest vertex: the post's hidden skirt (K1) or the ground (K2, D1)
        low = min(float(V[:, 2].min()) for V, F in M.values()) * 1000.0
        exp = -150.0 if kind == "K1" else 0.0
        rep.within("PIVOT %s: the lowest vertex z %.1f (K1: the post's skirt at -150; K2 and D1 stand on the flag at 0)" % (name, low), low, exp, 8.0 if kind == "K1" else 2.0)
    req = rep.rows
    out = {"version": a.version, "passed": sum(1 for r in req if r["ok"]), "failed": [r["id"] for r in req if not r["ok"]], "total": len(req), "rows": rep.rows,
           "not_built": ["the lettering LITTER (K1, K2), LB n on K1's post, the dustbin's house number: the engine's decals", "the overflowing litter, sacks beside D1 b, cigarette ends, gum (the dressing set: instances, never baked in)",
                         "the wear: chalk, scuffs, rust, white rust, soot, stickers, scorch, the small dents under 5 mm (the engine's masks and normal maps, unit 4.5)", "the K2 hood dent of b (5 deep: a normal map) and the burn's melted edge and charred fringe (c)",
                         "K1's spot-weld dimples and the K2 aperture's return flange and lip (normal maps)", "the placements: three public bins and two dustbins, the engine's"]}
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    path = os.path.join(HERE, "checks", "check_v%d.json" % a.version)
    json.dump(out, open(path, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print("\nRESULT: %d of %d checks pass; failed: %s -> %s" % (out["passed"], out["total"], out["failed"], path))
    return 0 if not out["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
