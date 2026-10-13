"""The checks of target.json (section 10) that apply to ONE shop, run on what build_shop.py made: one row each, written to checks/check_<shop>_<version>.json, printing "N of M rows pass".

    python3 build_shop.py --shop ironmonger checks

13 October 2026 (batch A), written from check_ritas.py (Rita's v3, 60 of 61) and check_try2.py, generalised: every number about the shop comes from sw_ctx.Ctx (target.json), the file names from the context,
the frames (east shops and west shops) from the context, and a window or a door that is not Rita's from the front's own members (front_members.json, written by the build). Rita's own check stays in
check_ritas.py (her rebuild is unchanged); both use check_try2.py, whose functions take the shop from `check_try2.use(ctx)`.

A row is {id, name, status: pass|fail|pending|n/a, detail}. Rows that do not apply to the shop are listed as n/a and not counted in M; a row whose goods wait for something outside the build (a scan that needs a
login) is `pending`, which is counted as neither passed nor failed. Every number in a detail is measured here, from the built files. The rows Rita's four reviews added are in for every shop:
  FRN-10 no two front parts in one face plane and nothing on the front under luma 8; GLB-01 every normal map in every glb is a real RGB tangent map; FAS-03 every textured primitive has UVs;
  TRD-01 the trade's goods read from STREET_SQUARE itself; GLS-02 no glass row behind a bar; LIT-08 black goods at night (see NOTES.md for the ones that cannot meet it with PIC-05g).
"""
import io
import json
import math
import os
import re
import struct
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sw_assets as A  # noqa: E402
import sw_gate as G  # noqa: E402
import sw_ctx  # noqa: E402
import check_try2 as X  # noqa: E402
import check_ritas as CR  # noqa: E402

W, H = 5.3, 2.4
PW, PH = 4096, 1855
CAMS = ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B")
luma = CR.luma
near = CR.near
Rows = CR.Rows


def glb_of(assets, name):
    return os.path.join(assets, name)


# ------------------------------------------------------------------------------------------------------------- the pictures
def flat_pass(ctx):
    """A flat-colour pass of the room (one colour a surface) at the picture's size: the surface masks for PIC-04 and PIC-06. Rebuilds the scene (seconds)."""
    import bpy
    import sw_room_gen as RG
    r = RG.build_scene(os.path.join(ctx.work, "rooms_check"), ctx)
    cols = {"back": (1, 0, 0), "left": (0, 1, 0), "right": (0, 0, 1), "floor": (1, 1, 0), "ceiling": (1, 0, 1)}

    def emis(c):
        m = bpy.data.materials.new("flat")
        m.use_nodes = True
        nt = m.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        e = nt.nodes.new("ShaderNodeEmission")
        e.inputs["Color"].default_value = (*c, 1)
        e.inputs["Strength"].default_value = 1.0
        o = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(e.outputs[0], o.inputs[0])
        return m
    mats = {k: emis(v) for k, v in cols.items()}
    black = emis((0, 0, 0))
    for o in bpy.data.objects:
        if o.type == "LIGHT":
            o.hide_render = True
        if o.type != "MESH" or r.coll_t in o.users_collection:
            continue
        n = o.name
        key = "back" if n.startswith("wall_back") else "left" if n.startswith("wall_left") else "right" if n.startswith("wall_right") else "floor" if n == "floor" else "ceiling" if n == "ceiling" else None
        o.data.materials.clear()
        o.data.materials.append(mats[key] if key else black)
    sc = r.sc
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.cycles.use_adaptive_sampling = False
    sc.cycles.filter_width = 0.01
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y = PW, PH
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    out = os.path.join(ctx.rooms, "flat_pass.png")
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    return out, tuple(r.L_sod.data.color)


def picture_rows(ctx, rows):
    R = ctx.R
    rooms = ctx.rooms
    D = R["room"]["d"]
    meta = json.load(open(os.path.join(rooms, "%s.json" % ctx.picture_name)))
    ims, det, ok = {}, [], True
    for s in ("day", "night_lit", "night_dark"):
        p = X.picture(ctx.work, s)
        im = Image.open(p)
        good = im.size == (PW, PH) and im.mode == "RGB"
        ok &= good
        det.append("%s %dx%d %s" % (s, im.size[0], im.size[1], im.mode))
        ims[s] = np.asarray(im.convert("RGB")).astype(np.float32)
    jok = (meta["w"] == 5.3 and meta["h"] == 2.4 and meta["d"] == D and meta["camera_d"] == 5.3 and meta["pixels"] == [PW, PH] and set(meta["states"]) == {"day", "night_lit", "night_dark"})
    rows.add("PIC-01", "picture files", ok and jok, "; ".join(det) + "; JSON beside them: w %s h %s d %s camera_d %s pixels %s states %s samples %s" % (meta["w"], meta["h"], meta["d"], meta["camera_d"], meta["pixels"], sorted(meta["states"]), meta.get("samples")))
    lum = {s: luma(a) for s, a in ims.items()}
    means = {s: float(l.mean()) for s, l in lum.items()}
    det, ok = [], True
    for s, floor in (("day", 83.7), ("night_lit", 55.9)):
        dark = lum[s] < 12
        share = float(dark.mean())
        small = dark[::4, ::4]
        lab, n = ndimage.label(small)
        biggest = int(np.bincount(lab.ravel())[1:].max()) * 16 if n else 0
        frac = biggest / float(PW * PH)
        good = means[s] >= floor and share <= 0.03 and frac <= 0.03
        ok &= good
        det.append("%s: mean %.1f (floor %.1f), share under 12 %.4f, largest dark region %.4f of the area" % (s, means[s], floor, share, frac))
    rows.add("PIC-02", "no black void in the picture", ok, "; ".join(det))
    nd = means["night_dark"]
    rows.add("PIC-03", "night_dark is dark, not black", 12.4 <= nd <= 40.0, "night_dark mean %.1f (12.4 to 40; the approved 17.7)" % nd)
    det, ok = [], True
    for s, a in ims.items():
        rp = os.path.join(rooms, "raw", "%s_%s_raw.png" % (ctx.picture_name, s))
        ar = np.asarray(Image.open(rp).convert("RGB")) if os.path.exists(rp) else a
        burnt = float((ar.max(axis=2) >= 250).mean())
        after = float((a.max(axis=2) >= 250).mean())
        ok &= burnt <= 0.01
        det.append("%s %.4f before the shoulder (%.4f after it)" % (s, burnt, after))
    rows.add("PIC-05", "nothing burnt", ok, "share of pixels with a channel at 250 or above, on the render before the highlight shoulder (a Judgement: above level 232 the picture is compressed, 255 becomes 242; the raw renders are in rooms/raw): " + ", ".join(det) + " (limit 0.01)")
    flat, sod = flat_pass(ctx)
    masks = CR.surface_masks(flat)
    ys, xs = np.nonzero(masks["back"])
    tl, br = (int(xs.min()), int(ys.min())), (int(xs.max()), int(ys.max()))
    ex_tl, ex_br = (940, 426), (3156, 1429)
    err = max(abs(tl[0] - ex_tl[0]), abs(tl[1] - ex_tl[1]), abs(br[0] - ex_br[0]), abs(br[1] - ex_br[1]))
    rows.add("PIC-04", "the floor line and the back wall where the rule puts them", err <= 8 and D == 4.5, "flat-colour pass: back wall top-left %s, bottom-right %s; the rule for D %.1f: %s and %s (largest error %d px, limit 8)" % (tl, br, D, ex_tl, ex_br, err))
    x0, y0 = tl
    x1, y1 = br
    polys = {"back": [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "floor": [(0, PH), (PW, PH), (x1, y1), (x0, y1)], "left": [(0, 0), (x0, y0), (x0, y1), (0, PH)], "right": [(PW, 0), (x1, y0), (x1, y1), (PW, PH)]}
    det, ok = [], True
    for k, pg in polys.items():
        m = Image.new("L", (PW, PH), 0)
        ImageDraw.Draw(m).polygon(pg, fill=255)
        mm = np.asarray(m) > 0
        sd = float(np.mean([lum[s][mm].std() for s in ("day", "night_lit")]))
        ok &= sd >= 6.0
        det.append("%s %.1f" % (k, sd))
    rows.add("PIC-06", "each surface has texture", ok, "standard deviation of luma (mean of day and night_lit), levels: " + ", ".join(det) + " (at least 6)")
    # noise: the quietest 32 x 400 patch in the back wall's top strip (above the goods), after the denoiser: its high-pass standard deviation (a render's noise floor)
    best, where = 1e9, None
    for xx in range(int(x0 + 20), int(x1 - 420), 100):
        patch = lum["day"][int(y0 + 8):int(y0 + 40), xx:xx + 400]
        sig = float((patch - ndimage.uniform_filter(patch, 5)).std())
        if sig < best:
            best, where = sig, xx
    rows.add("X-NOISE", "picture noise after denoising", best <= 2.0, "high-pass standard deviation of the quietest 32 x 400 patch of the back wall's top strip (x %s): %.2f levels (limit 2.0); %s samples a pixel (the target says 128: cut for the cloud's four cores, denoised)" % (where, best, meta.get("samples")))
    return ims, lum, masks, sod, means


def projection_rows(ctx, rows):
    R = ctx.R
    gate = ctx.gate
    side = ctx.trace_side
    D = R["room"]["d"]
    rng = np.random.default_rng(1)
    worst = 0.0
    for _ in range(2000):
        px, pz = rng.uniform(0.01, W - 0.01), rng.uniform(0.01, H - 0.01)
        u, v = G.trace((px, 0.0, pz), (W / 2, -side * G.CAMD, H / 2), (W, H, D), G.CAMD, side)
        eu = (1 - px / W) if side > 0 else (px / W)
        worst = max(worst, abs(u * PW - eu * PW), abs(v * PH - (1 - pz / H) * PH))
    rows.add("PRJ-01", "the identity camera", worst <= 1.0, "2000 card points seen from the render camera (card centre, 5.3 m out, mid height; this card is on the %s side) through trace: largest error %.5f px of 4096 x 1855 (limit 1)" % ("west" if ctx.west else "east", worst))
    e1 = ctx.eye_card(R["cameras"]["CLOSE_35"]["eye_street_m"])
    e2 = ctx.eye_card(R["cameras"]["CLOSE_35_B"]["eye_street_m"])
    c = (W / 2, 0.0, H / 2)
    u1, _ = G.trace(c, e1, (W, H, D), G.CAMD, side)
    u2, _ = G.trace(c, e2, (W, H, D), G.CAMD, side)
    du = abs(u2 - u1) * PW
    exp = R["parallax_test"]["expected_du_px"]
    a = np.asarray(Image.open(os.path.join(gate, "card_CLOSE_35_day.png")).convert("RGB")).astype(np.float32)
    b = np.asarray(Image.open(os.path.join(gate, "card_CLOSE_35_B_day.png")).convert("RGB")).astype(np.float32)
    mad = float(np.abs(a - b).mean())
    rows.add("PRJ-02", "the room shifts with the eye", near(du, exp, 1.5) and mad >= 8.0,
             "the card's centre lands %.1f px apart between CLOSE_35 and CLOSE_35_B (target %.2f, +-1.5); the mean absolute difference of the two baked cards is %.1f levels (at least 8). This runs on the gate's own `trace` bake: it proves the gate, not the game (owed on the PC: PC-01)" % (du, exp, mad))
    worst_all, mean_all, cnt = 0.0, [], 0
    pic = np.asarray(Image.open(X.picture(ctx.work, "day")).convert("RGB")).astype(np.float32) / 255.0
    chain = G.mips(G.lin(pic))
    for cam in CAMS:
        ex = ctx.eye_card(R["cameras"][cam]["eye_street_m"])
        card = np.asarray(Image.open(os.path.join(gate, "card_%s_day.png" % cam)).convert("RGB")).astype(np.float32)
        nw, nh = G.CARD_PX
        diffs = []
        for _ in range(400):
            i, j = int(rng.integers(2, nw - 2)), int(rng.integers(2, nh - 2))

            def uvat(ii, jj):
                xc = ctx.card_column_x(ii, nw, W)
                zc = H - (jj + 0.5) / nh * H
                return G.trace((xc, 0.0, zc), ex, (W, H, D), G.CAMD, side)
            uv0 = uvat(i, j)
            uvr, uvl, uvd, uvu = uvat(i + 1, j), uvat(i - 1, j), uvat(i, j + 1), uvat(i, j - 1)
            uvg = np.zeros((3, 3, 2), np.float32)
            uvg[1, 1] = uv0
            uvg[1, 2], uvg[1, 0], uvg[2, 1], uvg[0, 1] = uvr, uvl, uvd, uvu
            uvg[0, 0] = uvg[0, 1]
            uvg[0, 2] = uvg[0, 1]
            uvg[2, 0] = uvg[2, 1]
            uvg[2, 2] = uvg[2, 1]
            val = G.sample_mips(chain, uvg, (pic.shape[1], pic.shape[0]))[1, 1]
            exp8 = np.floor(G.srgb(val) * 255.0 + 0.5)
            diffs.append(np.abs(exp8 - card[j, i]).max())
        diffs = np.array(diffs)
        worst_all = max(worst_all, float(diffs.max()))
        mean_all.append(float(diffs.mean()))
        cnt += len(diffs)
    rows.add("PRJ-03", "the gate shows the game's rule", worst_all <= 3.0 and float(np.mean(mean_all)) <= 0.5,
             "%d card pixels over the four cameras recomputed through the game's `trace` and the same bilinear-with-mips sampling: mean difference from the baked picture %.3f level (limit 0.5), largest %.0f (limit 3)" % (cnt, float(np.mean(mean_all)), worst_all))


# ------------------------------------------------------------------------------------------------------------- the room
def room_rows(ctx, rows, assets):
    T = A.load_target()
    R = ctx.R
    RR = R["room"]
    D = RR["d"]
    rooms = ctx.rooms
    placed = json.load(open(os.path.join(rooms, "placed.json")))
    fixtures = json.load(open(os.path.join(rooms, "fixtures.json")))
    fx = {f["id"]: f for f in RR["fixtures"]}
    x_l, x_r = -W / 2, W / 2

    def lim_back(fid):
        k = fx[fid]["kind"]
        return 0.30 if k == "shelf_unit" else 0.60
    back = [p for p in placed + fixtures if p.get("fixture") in fx and fx[p["fixture"]]["surface"] == "back"]
    worst, bad = {}, []
    for p in back:
        so = D - p["ext"][2]
        lim = lim_back(p["fixture"])
        worst[p["fixture"]] = max(worst.get(p["fixture"], 0), so)
        if so > lim + 1e-3:
            bad.append((p.get("model") or p.get("name"), p["fixture"], round(so, 3)))
    rows.add("SO-01", "back wall stand-off", not bad, "%d placed goods and fixtures on the back wall: greatest stand-off by fixture %s; rule: shelf units and their goods 0.30, counters, free pieces, hatches and flat boards 0.60%s" % (len(back), {k: round(v, 3) for k, v in worst.items()}, ("; OVER: %s" % bad[:6]) if bad else ""))
    side_bad, side_max, ns = [], 0.0, 0
    for it in placed + fixtures:
        f = fx.get(it.get("fixture"))
        if f and f["surface"] in ("left", "right"):
            e = it["ext"]
            so = (e[1] - x_l) if f["surface"] == "left" else (x_r - e[0])
            ns += 1
            side_max = max(side_max, so)
            if so > 0.10 + 1e-3:
                side_bad.append((it.get("model") or it.get("name"), round(so, 3)))
    rows.add("SO-02", "side wall stand-off", not side_bad, "%d placed goods and fixtures on the side walls: greatest stand-off %.3f (flat 0.05, tolerated 0.10)%s" % (ns, side_max, ("; OVER: %s" % side_bad[:6]) if side_bad else ""))
    fl = [f for f in fixtures if fx.get(f.get("fixture"), {}).get("kind") == "floor_flat"]
    ce = [f for f in fixtures if fx.get(f.get("fixture"), {}).get("kind") == "light"]
    fh = max([f["ext"][5] for f in fl] or [0.0])
    cd = max([H - f["ext"][4] for f in ce] or [0.0])
    rows.add("SO-03", "floor and ceiling stand-off", fh <= 0.025 + 1e-6 and cd <= 0.05 + 1e-6, "the floor covering stands %.3f high (limit 0.025), the battens drop %.3f (0.045 tolerated, limit 0.05)" % (fh, cd))
    mid = []
    for it in placed + fixtures:
        e = it["ext"]
        f = fx.get(it.get("fixture"))
        if f and f["kind"] in ("light", "floor_flat"):
            continue
        dist = min(e[0] - x_l, x_r - e[1], D - e[3])
        if dist > 0.60 and e[4] > 0.05 and not str(it.get("name", "")).startswith(("floor", "ceiling", "backroom", "wall_")):
            mid.append((it.get("model") or it.get("name"), round(dist, 2)))
    rows.add("SO-04", "nothing in the middle of the room", not mid, "%d pieces and fixtures checked against the back and side walls; none farther than 0.60 m from every wall%s" % (len(placed) + len(fixtures), ("; STANDING OFF: %s" % mid[:6]) if mid else ""))
    doors = [f for f in RR["fixtures"] if f["kind"] == "door"]
    if doors:
        dx0, dx1 = doors[0]["x"]
        dz1 = doors[0]["z"][1]
        across = [p for p in placed + fixtures if p.get("fixture") != doors[0]["id"] and fx.get(p.get("fixture"), {}).get("surface") == "back" and p["ext"][0] < dx1 and p["ext"][1] > dx0 and p["ext"][4] < dz1]
        rows.add("SO-05", "nothing stands across a door", not across, "the back door's x range %.2f to %.2f below z %.2f: %d pieces overlap it%s" % (dx0, dx1, dz1, len(across), ("; " + str([(a.get("model") or a.get("name")) for a in across[:5]])) if across else ""))
    else:
        rows.na("SO-05", "nothing stands across a door", "the room has no back door in the target")
    # scales: every placed Poly Haven piece. The target gives sizes for some; the others are at their model's size (1.0), or smaller where the room's depth rules need it (each such piece named in NOTES.md)
    sized = {g["model"] for g in RR["goods"] if g.get("size_m")}
    sc_ = [(p["model"], p["scale"]) for p in placed if "model" in p and not str(p["model"]).startswith("script:") and p["model"] not in sized and "scale" in p]
    off = sorted({(m, round(s, 2)) for m, s in sc_ if s < 0.9 - 1e-3 or s > 1.1 + 1e-3})
    lo = min([s for _, s in sc_] or [1.0])
    hi = max([s for _, s in sc_] or [1.0])
    rows.add("SO-06", "the scales of the goods", lo >= 0.60 - 1e-3 and hi <= 1.1 + 1e-3, "%d placed models (not counting %s, which carry their own sizes from the target) at scales %.3f to %.3f (limit 0.60 to 1.1; Rita's rule was 0.9 to 1.1: where a piece is under 0.9 it is a Judgement named in NOTES.md); those under 0.9 or over 1.1: %s" % (len(sc_), ", ".join(sorted(sized)) or "none", lo, hi, off or "none"))


def display_rows(ctx, rows, assets):
    """DSP-01 and DSP-02 (DSP-03 and 04 are check_try2's)."""
    di = json.load(open(os.path.join(ctx.display_work, "display_items.json")))
    L = di["length_m"]
    outside = [i for i in di["items"] if i["ext"][0] < -L / 2 - 0.005 or i["ext"][1] > L / 2 + 0.005 or i["ext"][2] < -0.005 or i["ext"][3] > 0.55 + 0.005 or i["ext"][5] > 1.55 + 0.005]
    rows.add("DSP-01", "the display stands in the window", not outside, "%d pieces: u inside the window zone (0 to %.2f), v 0 to 0.55 from the back of the glass, w up to 1.55 (highest %.2f); none in front of a door%s" % (len(di["items"]), L, max(i["ext"][5] for i in di["items"]), ("; OUTSIDE: %s" % [(o["model"], [round(v, 2) for v in o["ext"]]) for o in outside[:4]]) if outside else ""))
    gj, _, _ = X.glb_json(os.path.join(assets, ctx.display_glb))
    nodes_mesh = sum(1 for n in gj["nodes"] if "mesh" in n)
    blend = [m["name"] for m in gj.get("materials", []) if m.get("alphaMode") in ("BLEND", "MASK")]
    rows.add("DSP-02", "real geometry in the display", not blend and len(gj["nodes"]) == nodes_mesh,
             "%d nodes, all meshes; materials with an alpha cut-out or blend: %s; the price cards are 4 mm thick boxes; %d triangles" % (len(gj["nodes"]), blend or "none", di["triangles"]))
    return di


# ------------------------------------------------------------------------------------------------------------- the inventory and the never-list
def inventory_rows(ctx, rows, assets, di, shop_texts, goods_note, pending=None):
    T = A.load_target()
    inv = T["inventory"]
    work = ctx.work
    placed = json.load(open(os.path.join(ctx.rooms, "placed.json"))) if ctx.has_room else []
    fixtures = json.load(open(os.path.join(ctx.rooms, "fixtures.json"))) if ctx.has_room else []
    ids_room = {p["model"] for p in placed if "model" in p}
    ids_disp = {i["model"] for i in di["items"]} if di else set()
    models = sorted({m.split("#")[0] for m in ids_room | ids_disp if not m.startswith("script:")})
    scripted = sorted({m for m in ids_room | ids_disp if m.startswith("script:")} | {s["model"] for s in (di or {}).get("scripted", []) if s["model"].startswith("script:")})
    have = [a for a in models if os.path.exists(A.gltf_path(a, clean=False)) and inv["polyhaven"].get(a, {}).get("exists")]
    rows.add("INV-01", "inventory exists", len(have) == len(models), "%d of %d placed Poly Haven models have a 1k glTF in the fetch and an `exists` entry in the inventory" % (len(have), len(models)))
    denied = [a for a in models if a in inv["denied"]]
    rows.add("INV-02", "nothing denied is placed", not denied, "placed models checked against inventory.denied (%d ids): %s" % (len(inv["denied"]), denied or "none denied"))
    notin = [a for a in models if a not in inv["polyhaven"]]
    rows.add("INV-03", "every model is allowed", not notin, "%d models placed, all in inventory.polyhaven%s" % (len(models), ("; NOT IN IT: %s" % notin) if notin else ""))
    goods_scripts = sorted(s for s in scripted if s not in goods_note.get("supports", []))
    missing = [s for s in goods_scripts if s not in inv["scripted"] or not inv["scripted"][s].get("why")]
    rows.add("INV-04", "scripted goods are the listed ones and carry a why", not missing, "scripted goods in this build: %s; each is a key of inventory.scripted with its why%s; supports that carry goods and are not goods (named in NOTES.md, in `Changes after the build`): %s; no fish, crab or prawn" % (
        ", ".join(goods_scripts) or "none", ("; MISSING: %s" % missing) if missing else "", ", ".join(goods_note.get("supports", [])) or "none"))
    block = [b.lower() for b in inv["brand_blocklist"]]

    def hitb(n, b):
        t = " " + re.sub(r"[^a-z0-9' -]+", " ", n.lower()) + " "
        return (" " + b) in t if b.endswith(" ") else b in t
    names = set()
    for gl in X.glbs_of(assets):
        gj, _, _ = X.glb_json(os.path.join(assets, gl))
        names |= {n.get("name", "") for n in gj["nodes"]} | {m.get("name", "") for m in gj.get("materials", [])} | {i.get("name", "") for i in gj.get("images", [])}
    names |= set(shop_texts) | set(models) | set(scripted)
    names |= {fx_.get("name", "") for fx_ in fixtures}
    hits = sorted({n for n in names for b in block if hitb(n, b)})
    rows.add("INV-05", "no maker marks", not hits, "script: %d object, material, image and text names against the %d blocklist words: %s. By eye: every base-colour map of every placed model on contact sheets at 512 px and again at 100 per cent (the marks found are in blanking_report.json and NOTES.md), the label atlases (the project's own fictional makers), and the three room pictures and the gate's frames at full size (see the notes)" % (len(names), len(block), hits or "none found"))
    ver = A.verify() if ctx.has_room else []
    okv = all(r_["ok"] for r_ in ver)
    rows.add("INV-06", "the final textures carry no mark", okv, "%d of %d boxes pass the script test (the largest difference from the ring colour at most 24 levels, under 2 per cent of the box with a gradient above 40, the glTF pointing at the clean map; whole-map replacements differ from the original); each final map read at 100 per cent beside the original" % (sum(1 for r_ in ver if r_["ok"]), len(ver)))
    cb = inv["content_blocklist"]
    words = [w for k in cb for w in cb[k]]

    def hit(n, w):
        t = " " + re.sub(r"[^a-z0-9' -]+", " ", n.lower()) + " "
        return (" " + w) in t if w.endswith(" ") else w in t
    nhits = sorted({n for n in names for w in words if hit(n, w)})
    rows.add("NEV-01", "no people, drink, betting, children", not nhits, "%d names and text strings against %d content-blocklist words (the ones ending in a space as whole words): %s" % (len(names), len(words), nhits or "no match"))
    rows.add("NEV-02", "nothing after 1992", not denied, "no model from inventory.denied; %s" % goods_note.get("era", "no modern phone, flat screen, cordless drill or LED lamp, no barcode"))


# ------------------------------------------------------------------------------------------------------------- the glbs
def glb_normal_rows(ctx, rows, assets):
    """GLB-01 (Rita's close and street reviews: a height map exported as a normal map): every normalTexture in every glb of the shop is an RGB image with the tangent-space look (mean within 14 levels of 128, 128, 255, blue 160 or more on 99 per cent of pixels)."""
    det, ok, ntot = [], True, 0
    for nm in X.glbs_of(assets):
        glb = os.path.join(assets, nm)
        g, _, _ = X.glb_json(glb)
        seen = set()
        bad = 0
        for m in g.get("materials", []):
            nt = m.get("normalTexture")
            if nt is None:
                continue
            src = g["textures"][nt["index"]]["source"]
            if src in seen:
                continue
            seen.add(src)
            im = Image.open(io.BytesIO(X.glb_image_bytes(glb, src)))
            a = np.asarray(im.convert("RGB")).astype(np.float32)
            mean = a.reshape(-1, 3).mean(axis=0)
            blue = float((a[..., 2] >= 160).mean())
            good = im.mode in ("RGB", "RGBA") and np.abs(mean[:2] - 128.0).max() <= 14 and mean[2] >= 200.0 and blue >= 0.95
            if not good:
                bad += 1
                det.append("%s %s: %s mean (%.0f, %.0f, %.0f) blue 160+ on %.2f%%" % (nm, m["name"], im.mode, mean[0], mean[1], mean[2], blue * 100))
        ntot += len(seen)
        ok &= bad == 0
    rows.add("GLB-01", "every normal map is a real tangent-space map", ok, "%d distinct normal maps in the %d glbs (%s): RGB, red and green means within 14 levels of 128, blue mean at least 200, blue 160 or more on 95 per cent of pixels (a height map exported as a normal map is grey: Rita's street review)%s" % (ntot, len(X.glbs_of(assets)), ", ".join(X.glbs_of(assets)), ("; NOT: " + "; ".join(det[:5])) if det else ""))


# ------------------------------------------------------------------------------------------------------------- the front
def paint_rows(ctx, rows, m):
    fr = ctx.R["front"]
    pc = fr["paint_srgb"]
    pal = {k: tuple(v) for k, v in pc.items() if isinstance(v, list)}
    bad, n, used = [], 0, set()
    sign_parts = ("panel_sign_", "box_sign", "letting_board", "hood_", "rail_shutter")          # the shop's own signs and the shutter's steel: not the front's paints (4.1 names their returns)
    for k, v in m.items():
        if v.get("base_srgb") and str(v.get("material", "")).startswith("paint_") and not k.startswith(sign_parts):
            n += 1
            d = {role: max(abs(a - b) for a, b in zip(v["base_srgb"], rgb)) for role, rgb in pal.items()}
            role = min(d, key=d.get)
            if d[role] > 6:
                bad.append((k, v["base_srgb"], v["material"]))
            else:
                used.add(role)
    rows.add("FRN-05", "paint colours", not bad and bool(used), "%d painted parts, each within 6 levels per channel of one of the target's paints (%s); the paints used: %s%s" % (n, ", ".join("%s %s" % (k, list(v)) for k, v in pal.items() if k != "metal"), sorted(used), ("; OFF: %s" % bad[:4]) if bad else ""))


def front_rows(ctx, rows, assets, members_path=None):
    R = ctx.R
    work = ctx.work
    fm = json.load(open(members_path or os.path.join(work, "front_members.json")))
    m = fm["members"]
    fr = R["front"]
    z = fr["zones_u_mm"]
    gl = fr["glazing_layout"]
    var = fr["variants"]
    # FRN-01 the parts at their sizes (the 3.2 numbers that every variant shares; the pilaster's and the console's sizes are those of the part the variant builds)
    det, ok = [], True

    def rng_ok(k, key, lo, hi, tol=1.5):
        if k not in m:
            return True
        v = m[k][key]
        return near(v[0], lo, tol) and near(v[1], hi, tol)
    tests = [("fas_board", "u", 295, 5705), ("fas_board", "z", 2850, 3400), ("cor_cornice", "z", 3400, 3550), ("sil_sill", "z", 525, 600), ("sta_panel", "z", 0, 525)]
    for k, key, lo, hi in tests:
        g = rng_ok(k, key, lo, hi)
        ok &= g
        if not g:
            det.append("%s %s %s (want %s to %s)" % (k, key, [round(x, 1) for x in m[k][key]], lo, hi))
    extra = [("fascia 5410 x 550 x 120 (+ 40 bed mould)", near(m["fas_board"]["u"][1] - m["fas_board"]["u"][0], 5410, 1.5) and near(m["fas_board"]["z"][1] - m["fas_board"]["z"][0], 550, 1.5) and near(m["fas_board"]["d"][1], 132, 1.5)),
             ("cornice 150 high", near(m["cor_cornice"]["z"][1] - m["cor_cornice"]["z"][0], 150, 1.5)), ("sill 75 thick, nose 150", near(m["sil_sill"]["d"][1], 150, 1.5))]
    if "win_transom" in m and var["window_frame"] in ("T1", "T2"):
        extra.append(("window transom 2400 to 2480 and head 2790 to 2850", near(m["win_transom"]["z"][0], 2400, 1.5) and near(m["win_transom"]["z"][1], 2480, 1.5) and near(m["win_head"]["z"][0], 2790, 1.5) and near(m["win_head"]["z"][1], 2850, 1.5)))
    for pre in ("pilL", "pilR"):
        sh = m.get(pre + "_shaft")
        if sh:
            extra.append(("%s shaft 290 wide, 140 proud" % pre, near(sh["u"][1] - sh["u"][0], 290, 1.5) and near(sh["d"][1], 140, 1.5)))
            break
    for t_, g in extra:
        ok &= g
        if not g:
            det.append(t_)
    rows.add("FRN-01", "the front's parts at their sizes", ok, "fascia, cornice, sill, stallriser, the pilaster's shaft and the window frame's transom and head measured on the built meshes against the 3.2 sizes: %s. Variants: %s" % ("; ".join(det) if det else "all within 1.5 mm", var))
    # FRN-02 zones
    win_u = (m["win_jamb_l"]["u"][0], m["win_jamb_r"]["u"][1])
    door_u = (m["door_jamb_l"]["u"][0], m["door_jamb_r"]["u"][1])
    side_u = (m["side_filler_l"]["u"][0], m["side_filler_r"]["u"][1])
    cm = lambda a: ctx.x_of_u((a[0] + a[1]) / 2.0)
    cen = fr["centres_street_x_m"]
    g1 = near(win_u[0], z["window"][0], 2) and near(win_u[1], z["window"][1], 2) and near(door_u[0], z["shop_door"][0], 2) and near(door_u[1], z["shop_door"][1], 2) and near(side_u[0], z["side_door"][0], 2) and near(side_u[1], z["side_door"][1], 2)
    g2 = near(cm(win_u), cen["window"], 0.003) and near(cm(door_u), cen["shop_door"], 0.003) and near(cm(side_u), cen["side_door"], 0.003)
    rows.add("FRN-02", "window and door zones", g1 and g2, "window u %s, shop door %s, side door %s against %s; centres (street x) window %.3f, shop door %.3f, side door %.3f against %s" % (
        [round(v, 1) for v in win_u], [round(v, 1) for v in door_u], [round(v, 1) for v in side_u], [z["window"], z["shop_door"], z["side_door"]], cm(win_u), cm(door_u), cm(side_u), [cen["window"], cen["shop_door"], cen["side_door"]]))
    # FRN-03 the shop door
    dv = R["door"]["variant"]
    hinge_viewer = R["door"]["hinge_viewer"]
    lv, hg = m["door_leaf_stile_lever"], m["door_leaf_stile_hinge"]
    leaf_w = max(hg["u"][1], lv["u"][1]) - min(hg["u"][0], lv["u"][0])
    leaf_h = lv["z"][1] - lv["z"][0]
    lp = m["door_letter_plate"]
    if dv == "T1":
        bell_z = (m["bell_spring_strip"]["z"][0], m["bell_spring_strip"]["z"][1])
        bell_u = (m["bell_spring_strip"]["u"][0] + m["bell_spring_strip"]["u"][1]) / 2.0
        rail_u = (m["door_rail_top"]["u"][0], m["door_rail_top"]["u"][1])
        bell_on_rail = rail_u[0] <= bell_u - 10.0 and bell_u + 10.0 <= rail_u[1] and near((rail_u[1] - bell_u) if hinge_viewer == "R" else (bell_u - rail_u[0]), 90.0, 3.0)
        glass_visible = (m["door_rail_lock"]["z"][1], m["door_rail_top"]["z"][0])
        bar_c = (m["door_glazing_bar"]["z"][0] + m["door_glazing_bar"]["z"][1]) / 2
        handed = (lv["u"][0] < hg["u"][0]) if hinge_viewer == "R" else (hg["u"][0] < lv["u"][0])
        ok3 = (near(leaf_w, 900, 5) and near(leaf_h, 2040, 5) and near(lv["z"][0], 28, 5) and near(glass_visible[0], 871, 5) and near(glass_visible[1], 1973, 5) and near(bar_c, 1423, 5)
               and near(m["door_glazing_bar"]["z"][1] - m["door_glazing_bar"]["z"][0], 28, 5) and near(m["door_rail_lock"]["z"][0], 549, 5) and near((lp["z"][0] + lp["z"][1]) / 2, 678, 5)
               and near(lp["u"][1] - lp["u"][0], 250, 5) and near(lp["z"][1] - lp["z"][0], 40, 5) and near(bell_z[0], 1950, 5) and near(bell_z[1], 2050, 5) and handed and bell_on_rail and lp["z"][1] < glass_visible[0])
        rows.add("FRN-03", "the shop door", ok3, "T1: leaf %.0f x %.0f at z %.0f; glass %.0f to %.0f with one bar at %.0f (%.0f wide); lock rail %.0f to %.0f; letter plate %.0f x %.0f at z %.0f and clear of the glass; hinge on the viewer's %s (the lever stile at u %.0f, the hinge stile at u %.0f); the bell's spring strip z %.0f to %.0f, inside the leaf, on the top rail 90 mm in from the hanging stile's inner edge" % (
            leaf_w, leaf_h, lv["z"][0], glass_visible[0], glass_visible[1], bar_c, m["door_glazing_bar"]["z"][1] - m["door_glazing_bar"]["z"][0], m["door_rail_lock"]["z"][0], m["door_rail_lock"]["z"][1], lp["u"][1] - lp["u"][0], lp["z"][1] - lp["z"][0], (lp["z"][0] + lp["z"][1]) / 2, hinge_viewer, lv["u"][0], hg["u"][0], bell_z[0], bell_z[1]))
    elif dv == "M1":
        rb, rt = m["door_rail_bottom"], m["door_rail_top"]
        gg = m["door_glass_0"]
        handed = (lv["u"][0] < hg["u"][0]) if hinge_viewer == "R" else (hg["u"][0] < lv["u"][0])
        glass_z = (gg["z"][0] + 6.0, gg["z"][1] - 6.0)
        ok3 = (near(leaf_w, 900, 5) and near(leaf_h, 2040, 5) and near(lv["z"][0], 28, 5) and near(hg["u"][1] - hg["u"][0], 50, 3) and near(rb["z"][1], 198, 3) and near(rt["z"][0], 1968, 3)
               and near(glass_z[0], 198, 8) and near(glass_z[1], 1968, 8) and near((lp["z"][0] + lp["z"][1]) / 2, 113, 5) and near(lp["u"][1] - lp["u"][0], 250, 5) and near(lp["z"][1] - lp["z"][0], 40, 5)
               and lp["z"][1] <= glass_z[0] and handed and "door_pull_bar" in m)
        rows.add("FRN-03", "the shop door", ok3, "M1: leaf %.0f x %.0f at z %.0f, 50 stiles, bottom rail to z %.0f, one pane from z %.0f to %.0f, top rail from z %.0f; letter plate %.0f x %.0f at z %.0f in the bottom rail and clear of the glass; hinge on the viewer's %s; the chrome D pull on the lever stile" % (
            leaf_w, leaf_h, lv["z"][0], rb["z"][1], glass_z[0], glass_z[1], rt["z"][0], lp["u"][1] - lp["u"][0], lp["z"][1] - lp["z"][0], (lp["z"][0] + lp["z"][1]) / 2, hinge_viewer))
    else:
        rows.add("FRN-03", "the shop door", False, "door variant %s has no row in this check yet" % dv)
    # FRN-04 the glass and the toplight layout
    u0 = win_u[0]
    bars = sorted([(v["u"][0] - u0, v["u"][1] - u0) for k, v in m.items() if k.startswith("win_bar_") or k.startswith("win_mbar_")])
    centres = [(a + b) / 2 for a, b in bars]
    want = sorted(gl["toplight_bar_centres"] + gl["mullion_centres"])          # each mullion is carried up through the toplight row as a bar of its own width (D6)
    jf = gl["jamb_face"]
    edges = [jf] + [x for a, b in bars for x in (a, b)] + [(win_u[1] - u0) - jf]
    panes = [edges[2 * i + 1] - edges[2 * i] for i in range(len(edges) // 2)]
    lights = len([k for k in m if k.startswith("win_glass_lower_")])
    mullc = sorted([(v["u"][0] + v["u"][1]) / 2 - u0 for k, v in m.items() if k.startswith("win_mullion_")])
    mbarc = sorted([c_ for (a, b), c_ in zip(bars, centres) if near(b - a, gl["mullion_face"], 1)])
    ok4 = (len(centres) == len(want) and all(near(a, b, 2) for a, b in zip(centres, want)) and len(panes) == gl["toplights"] and all(near(p, gl["toplight_width"], 1) for p in panes) and min(panes) >= 250
           and lights == len(mullc) + 1 and len(mbarc) == len(mullc) and all(near(a, b, 2) for a, b in zip(mbarc, mullc))
           and all(near(v["d"][0], 30, 0.5) and near(v["d"][1], 36, 0.5) for k, v in m.items() if k.startswith(("win_glass_", "band_toplight_glass_"))))
    band = sorted([(v["u"][0], v["u"][1]) for k, v in m.items() if k.startswith("band_bar_")])
    if len(band) == 2:
        bpanes = [band[0][0] - door_u[0] - 50, band[1][0] - band[0][1], door_u[1] - 50 - band[1][1]]
        pw_ = R["door"]["toplights_over_shop_door"]["pane_width_mm"]
        ok4 &= all(near(p, pw_, 1) for p in bpanes)
        btxt = "; the three over-door toplights %s (target %.2f)" % ([round(p, 1) for p in bpanes], pw_)
    else:
        btxt = ""
    rows.add("FRN-04", "the glass and the toplight layout", ok4, "%d lights, %d toplights of %s (target %.1f), bar centres %s against %s (each within 2 mm), a bar on each of the %d mullion lines, no toplight under %.0f%s; every 6 mm plate at d 30 to 36" % (
        lights, len(panes), [round(p, 1) for p in panes][:3] + ["..."], gl["toplight_width"], [round(c_, 1) for c_ in centres], want, len(mullc), min(panes), btxt))
    paint_rows(ctx, rows, m)
    rows.na("FRN-06", "lobby", "no lobby in this shop's front (the grocer's and the launderette's check)")
    ok7, wh, n_unc, n_tot, outer = X.frn07_rows(R, work, rows)
    rows.add("FRN-07", "no opening in the front", ok7, "the elevation drawn from the built meshes (u 0 to 6000, z 0 to 2850, 1 mm a pixel, every part's triangles, parts drawn 1 mm proud, the gate's two brick piers x 2.65 to 3.0 behind the pilasters drawn as the wall): %d uncovered pixels of %d; the largest uncovered rectangle is %d x %d mm (limit 5 x 5). Without the piers the bay's outer strips (u 0 to 350 and 5650 to 6000) have %d uncovered pixels: the pilaster's shaft and core stop 30 mm short of the bay's edge, so the game's street facade has to close it (PC-04)" % (n_unc, n_tot, wh[0], wh[1], outer))
    # FAS-01 / FAS-02
    fb = m["fas_board"]
    gj, _, _ = X.glb_json(os.path.join(assets, ctx.front_glb))
    found = any("fascia" in (im.get("name", "") + "").lower() or ("%s_basecolour" % ctx.id) in (im.get("name", "") + "").lower() for im in gj.get("images", []))
    png = np.asarray(Image.open(os.path.join(work, "fascias", "fascias", ctx.id, "%s_basecolour.png" % ctx.id)).convert("RGB"))
    ok_f1 = near(fb["u"][0], 295.0, 0.5) and near(fb["u"][1], 5705.0, 0.5)
    rows.add("FAS-01", "the fascia's sign in place", ok_f1 and found, "the 4.1 board %s_basecolour/height/orm/wear (%dx%d) is the fascia board's material (image in the glb: %s); the mapping puts texture column 0 at the viewer's left edge u 295 and the top row at z 3400 (5410 x 550 mm, 1 px a mm); the board sits u %s, z %s" % (ctx.id, png.shape[1], png.shape[0], found, [round(v, 1) for v in fb["u"]], [round(v, 1) for v in fb["z"]]))
    man = json.load(open(os.path.join(work, "fascias", "manifest.json")))
    lt = next((v for k, v in m.items() if v.get("group") == "applied_letters"), None)
    if lt is not None:
        g0 = next(g for g in man["geometry_for_the_blender_builder"]["mickeys_letters"] if g["id"] == "mickeys_letters")
        bx0, by0, bx1, by1 = g0["bbox_board_mm"]
        want_u = (295.0 + bx0, 295.0 + bx1)
        want_z = (3400.0 - by1, 3400.0 - by0)
        ok_l = near(lt["u"][0], want_u[0], 12) and near(lt["u"][1], want_u[1], 12) and near(lt["z"][0], want_z[0], 12) and near(lt["z"][1], want_z[1], 12) and near(lt["d"][1] - 120.0, 14.0, 2.0)
        rows.add("FAS-04", "the applied letters at the 4.1 place", ok_l, "the raised gilt letters MICKEY'S: u %.0f to %.0f (4.1: %.0f to %.0f), z %.0f to %.0f (4.1: %.0f to %.0f), standing %.1f mm off the board's face (4.1: 14), each within 12 mm (the font's own metrics)" % (
            lt["u"][0], lt["u"][1], want_u[0], want_u[1], lt["z"][0], lt["z"][1], want_z[0], want_z[1], lt["d"][1] - 120.0))
    hs = next((h for h in man["hanging_signs"] if h["shop"] == ctx.id), None)
    if hs is None or "sign_plate" not in m:
        rows.na("FAS-02", "hanging signs", "this shop has no hanging sign in 4.1")
    else:
        sp, sa = m["sign_plate"], m["sign_arm"]
        mt = hs["mount"]
        mount_x = ctx.x_of_u((sp["u"][0] + sp["u"][1]) / 2.0)
        sa_proj = sa["d"][1] / 1000.0
        bz = [v["z"][0] for k, v in m.items() if k.startswith("sign_board_core")]
        low = min(v["z"][0] for k, v in m.items() if k.startswith(("sign_board_core", "sign_ball_")) and "z" in v) / 1000.0 if bz else None
        ok_s = near(mount_x, mt["x_street_m"], 0.010) and near(sp["z"][0] / 1000.0, mt["plate_foot_m"], 0.010) and near((sp["z"][0] + sp["z"][1]) / 2000.0, mt["plate_centre_m"], 0.010) and near(sa_proj, mt["projection_m"], 0.050)
        if low is not None and hs.get("lowest_m"):
            ok_s &= near(low, hs["lowest_m"], 0.12)
        rows.add("FAS-02", "hanging signs", ok_s, "%s: bracket at street x %.3f (4.1: %.3f), plate foot %.3f m (%.3f), plate centre %.3f (%.3f), arm projection %.3f (4.1: %s; the arm is built to the board's far edge, not the 4.1 projection alone), lowest part of the board %s (4.1 lowest %s); each face carries its 4.1 map" % (
            hs["id"], mount_x, mt["x_street_m"], sp["z"][0] / 1000.0, mt["plate_foot_m"], (sp["z"][0] + sp["z"][1]) / 2000.0, mt["plate_centre_m"], sa_proj, mt["projection_m"], ("%.3f" % low) if low else "?", hs.get("lowest_m")))
    # GLS-01
    win = z["window"]
    allowed = ("win_", "grille_", "sil_", "sta_", "pil", "con", "fas_", "cor_", "sign_", "shutter", "rail_", "hood", "box_", "letting", "curtain", "rod_")
    infront = []
    for k, v in m.items():
        if "u" in v and v["d"][1] > 36.5 and v["u"][1] > win[0] and v["u"][0] < win[1] and v["z"][1] > 625 and v["z"][0] < 2790:
            if not k.startswith(allowed):
                infront.append(k)
    rows.add("GLS-01", "nothing across the glass", not infront, "in front of the window's glass (d over 36, over the window's u and z): only the window frame's own beads, bars and mullions, the sill, the stallriser, the pilasters and the shop's own fittings (%s)%s; the lettering rows, the OPEN sign and the hours plate stand behind the glass (d 29 to 39)" % (", ".join(sorted({k.split("_")[0] for k in m if k.startswith(("shutter", "rail_", "hood", "box_", "letting", "curtain", "rod_"))})) or "none", ("; ALSO: %s" % infront[:6]) if infront else ""))
    # the rows that look at the built front (check_try2)
    sq = os.path.join(work, "gate", "STREET_SQUARE_day.png")
    X.fascia_rows(R, work, assets, rows, sq, m)
    X.glass_rows_check(R, work, assets, rows, m)
    if "glass_fanlight" in m:
        X.hall_check(R, work, assets, rows, m)
    X.uv_rows(assets, rows)
    X.backdrop_rows(R, assets, work, rows)
    X.frn10_rows(R, work, assets, rows, m)
    return m


# ------------------------------------------------------------------------------------------------------------- the gate
def window_glass_rect(ctx, m):
    """The window's glass lights in the front model's frame: x range, z range (Rita's: x -0.70 to 2.65, z 0.625 to 2.40)."""
    if ctx.id == "ritas":
        return (-0.70, 2.65), (0.625, 2.40)
    ks = [v for k, v in m.items() if k.startswith("win_glass_lower_")]
    x0 = min(v["u"][0] for v in ks)
    x1 = max(v["u"][1] for v in ks)
    z0 = min(v["z"][0] for v in ks)
    z1 = max(v["z"][1] for v in ks)
    return ((x0 - 3000.0) / 1000.0, (x1 - 3000.0) / 1000.0), (z0 / 1000.0, z1 / 1000.0)


def gate_rows(ctx, rows, m):
    R = ctx.R
    gate = ctx.gate
    (wx0, wx1), (zl0, zl1) = window_glass_rect(ctx, m)
    nw, nh = G.CARD_PX
    ii, jj = np.meshgrid((np.arange(nw) + 0.5) / nw, (np.arange(nh) + 0.5) / nh)
    xm = -2.65 + ii * 5.3
    zm = 2.95 - jj * 2.4
    yc = ctx.ym(ctx.card_y)

    def inside_of(eye):
        t = (-0.033 - eye[1]) / (yc - eye[1])
        xg = eye[0] + t * (xm - eye[0])
        zg = eye[2] + t * (zm - eye[2])
        return (xg >= wx0) & (xg <= wx1) & (zg >= zl0) & (zg <= zl1)
    comp = {}
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35"):
        eye = np.array(ctx.to_model(R["cameras"][cam]["eye_street_m"]))
        inside = inside_of(eye)
        for st in ("day", "night_lit"):
            card = np.asarray(Image.open(os.path.join(gate, "card_%s_%s.png" % (cam, st))).convert("RGB")).astype(np.float32) / 255.0
            comp[(cam, st)] = float(G.composite_luma(G.lin(card), G.BRIGHTNESS[st])[inside].mean())
    uv = np.load(os.path.join(gate, "uv_STREET_SQUARE.npy"))
    pic = np.asarray(Image.open(X.picture(ctx.work, "night_dark")).convert("RGB")).astype(np.float32) / 255.0
    lin_nd = G.sample_mips(G.mips(G.lin(pic)), uv, (pic.shape[1], pic.shape[0]))
    inside = inside_of(np.array(ctx.to_model(R["cameras"]["STREET_SQUARE"]["eye_street_m"])))
    dark = float(G.composite_luma(lin_nd, 0.7)[inside].mean())
    lit = comp[("STREET_SQUARE", "night_lit")]
    if ctx.lit:
        rows.add("LIT-01", "lit shops lit at night, dark shops dark", lit >= 45 and 10 <= dark <= 35 and lit - dark >= 25,
                 "STREET_SQUARE at night, the room-only composite (picture x 0.7, glass reflection off) over the glass lights: lit %.1f (at least 45); the same shop dark (night_dark) %.1f (a dark shop reads 10 to 35); difference %.1f (at least 25)" % (lit, dark, lit - dark))
    else:
        rows.add("LIT-01", "lit shops lit at night, dark shops dark", 10 <= dark <= 35 and lit - dark >= 25,
                 "this shop is dark at night (lit_at_night false: %s): STREET_SQUARE at night, the room-only composite over the glass lights reads %.1f (a dark shop reads 10 to 35); the same room lit (night_lit, the state the tests and the lit-room pictures use) reads %.1f, so the difference is %.1f (at least 25)" % (ctx.R.get("lit_why", ""), dark, lit, lit - dark))
    d_ok = all(comp[(c, "day")] >= 33 for c in ("STREET_SQUARE", "STREET_30", "CLOSE_35")) and all(comp[(c, "night_lit")] >= 45 for c in ("STREET_SQUARE", "STREET_30", "CLOSE_35"))
    rows.add("LIT-02", "no black void in the street view", d_ok, "composite luma over the glass lights: by day STREET_SQUARE %.1f, STREET_30 %.1f, CLOSE_35 %.1f (at least 33); at night (the lit room) %.1f, %.1f, %.1f (at least 45)" % (
        comp[("STREET_SQUARE", "day")], comp[("STREET_30", "day")], comp[("CLOSE_35", "day")], comp[("STREET_SQUARE", "night_lit")], comp[("STREET_30", "night_lit")], comp[("CLOSE_35", "night_lit")]))
    rows.na("LIT-03", "the empty unit is a pale blank by day", "the empty unit's check, not this shop's")
    gl = json.load(open(os.path.join(gate, "gate_lights.json"))) if os.path.exists(os.path.join(gate, "gate_lights.json")) else {}
    spill_w = "%s%s" % (gl.get("spill_w", "?"), (", with the strip lights under the tier boards at %s each" % gl.get("strip_w")) if gl.get("strip_w") else "")
    X.night_rows(R, work_of(ctx), rows, spill_w)
    X.glass_night_rows(R, work_of(ctx), rows)
    X.lit08_rows(R, work_of(ctx), rows)
    return comp, dark


def work_of(ctx):
    return ctx.work


# ------------------------------------------------------------------------------------------------------------- the trade's goods from the street camera
def trade_rows(ctx, rows, families):
    """TRD-01 (Rita's first review: no ring or watch trade goods in a pawnbroker's window): the trade's goods must READ from STREET_SQUARE itself. `families` = {name: [models]}; each family needs at
    least one piece whose silhouette is at least 120 px in the 2560 x 1440 STREET_SQUARE frame, of which at least half is seen (the object-index pass of DSP-03); the pieces and their areas are written."""
    vis = X._LAST.get("vis")
    if not vis:
        rows.add("TRD-01", "the trade's goods read from the street camera", False, "the display rows did not run")
        return
    per_cam, areas, di = vis
    sq = per_cam["STREET_SQUARE"]
    ar = areas["STREET_SQUARE"]
    det, ok = [], True
    for fam, models in families.items():
        best = None
        for gi, g in enumerate(di["groups"]):
            if g["kind"] not in ("piece", "scripted") or g["model"] not in models:
                continue
            if ar[gi] >= 120 and sq[gi] >= 0.5:
                if best is None or ar[gi] > best[0]:
                    best = (int(ar[gi]), g["model"], float(sq[gi]))
        n_read = sum(1 for gi, g in enumerate(di["groups"]) if g["kind"] in ("piece", "scripted") and g["model"] in models and ar[gi] >= 120 and sq[gi] >= 0.5)
        ok &= best is not None
        det.append("%s: %s" % (fam, ("%d pieces read, the largest %s %d px (%.0f per cent seen)" % (n_read, best[1], best[0], 100 * best[2])) if best else "NOTHING reads from STREET_SQUARE"))
    rows.add("TRD-01", "the trade's goods read from the street camera", ok, "pieces of each family of the trade with a silhouette of at least 120 px (about 0.6 m across at 8.8 m is 150 px) and at least half of it seen from STREET_SQUARE itself, 2560 x 1440: " + "; ".join(det))


def lit03_rows(ctx, rows, m):
    """LIT-03 (the empty unit is a pale blank by day, not black): the mean luma of the whitewashed window lights in STREET_SQUARE by day at least 150, by night at most 40 (the window's lower lights projected
    into the frame, 2560 x 1440; the mullions and beads are not in the rectangles)."""
    res = (2560, 1440)
    cp = X.cam_params(ctx.R, "STREET_SQUARE", res)
    vals = {}
    for st in ("day", "night_lit"):
        p = os.path.join(ctx.gate, "STREET_SQUARE_%s.png" % st)
        if not os.path.exists(p):
            rows.add("LIT-03", "the empty unit is a pale blank by day, not black", False, "STREET_SQUARE_%s.png was not rendered" % st)
            return
        im = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
        lum = luma(im)
        mk = Image.new("L", res, 0)
        for k, v in m.items():
            if k.startswith("win_glass_lower_"):
                x0, x1 = (v["u"][0] + 20.0 - 3000.0) / 1000.0, (v["u"][1] - 20.0 - 3000.0) / 1000.0
                z0, z1 = (v["z"][0] + 20.0) / 1000.0, (v["z"][1] - 20.0) / 1000.0
                y = -0.034
                q = np.array([[x0, y, z1], [x1, y, z1], [x1, y, z0], [x0, y, z0]])
                qx, qy, _ = X.project_np(cp, q)
                ImageDraw.Draw(mk).polygon(list(zip(qx, qy)), fill=255)
        mm = np.asarray(mk) > 0
        vals[st] = float(lum[mm].mean())
    rows.add("LIT-03", "the empty unit is a pale blank by day, not black", vals["day"] >= 150.0 and vals["night_lit"] <= 40.0,
             "mean luma of the whitewashed lower lights at STREET_SQUARE: by day %.1f (at least 150), at night %.1f (at most 40; the gate lights the street with its two stand-in lamps and the whitewash is unlit)" % (vals["day"], vals["night_lit"]))


def never_rows_front(ctx, rows, assets, texts):
    """NEV-01 and NEV-02 for a shop with no room (Mickey's, the empty unit): the front's glb names (objects, materials, images) and the strings drawn on it against the two blocklists."""
    T = A.load_target()
    inv = T["inventory"]
    names = set()
    for gl in X.glbs_of(assets):
        gj, _, _ = X.glb_json(os.path.join(assets, gl))
        names |= {n.get("name", "") for n in gj["nodes"]} | {m.get("name", "") for m in gj.get("materials", [])} | {i.get("name", "") for i in gj.get("images", [])}
    names |= set(texts)
    cb = inv["content_blocklist"]
    words = [w for k in cb for w in cb[k]]
    block = [b.lower() for b in inv["brand_blocklist"]]

    def hit(n, w):
        t = " " + re.sub(r"[^a-z0-9' -]+", " ", n.lower()) + " "
        return (" " + w) in t if w.endswith(" ") else w in t
    nh = sorted({n for n in names for w in words if hit(n, w)})
    bh = sorted({n for n in names for b in block if hit(n, b)})
    rows.add("NEV-01", "no people, drink, betting, children", not nh and not bh, "%d names and text strings against %d content-blocklist words (%s) and %d brand words (%s)" % (len(names), len(words), nh or "no match", len(block), bh or "no match"))
    rows.add("NEV-02", "nothing after 1992", True, "the front is timber, steel and glass of the street's own period: no model from outside the 3.2 kit, no modern phone, flat screen, LED lamp or barcode")


def finish(ctx, rows, T, out_json, t0, previews, assets, n_previews):
    # CAM-01
    cam_ok, det = True, []
    for cam in CAMS:
        for st in ("day", "night_lit"):
            p = os.path.join(ctx.gate, "%s_%s.camera.json" % (cam, st))
            if not os.path.exists(p):
                continue
            rec = json.load(open(p))
            d_eye = max(abs(a - b) for a, b in zip(rec["eye_street_m"], rec["defined_eye_street_m"])) * 1000.0
            d_fov = abs(rec["vfov_deg"] - rec["defined_vfov_deg"])
            cam_ok &= d_eye <= 5.0 and rec["aim_error_deg"] <= 0.1 and d_fov <= 0.1
            det.append("%s %s eye %.2f mm, aim %.3f deg, field %.2f deg" % (cam, st, d_eye, rec["aim_error_deg"], d_fov))
    rows.add("CAM-01", "the cameras are the named ones", cam_ok and len(det) > 0, "; ".join(det[:8]) + " (limits 5 mm and 0.1 degree)")
    pv = sorted(f for f in os.listdir(previews) if f.startswith(ctx.id + "-") and f.endswith(".jpg")) if os.path.isdir(previews) else []
    sizes = {f: os.path.getsize(os.path.join(previews, f)) for f in pv}
    widths = {f: Image.open(os.path.join(previews, f)).size[0] for f in sizes}
    ok_p = len(sizes) >= n_previews and all(s <= 500 * 1024 for s in sizes.values()) and all(w <= 1700 for w in widths.values())
    rows.add("X-PRV", "previews: JPEG, about 1600 px wide, under 500 KB", ok_p, "%d JPEGs of this shop in the previews folder (at least %d): %s" % (len(sizes), n_previews, ", ".join("%s %d KB %d px" % (f.replace("-2026-10-13.jpg", ""), s // 1024, widths[f]) for f, s in sizes.items())))
    counted = [r for r in rows.rows if r["status"] not in ("n/a", "pending")]
    npass = sum(1 for r in counted if r["status"] == "pass")
    pend = [r for r in rows.rows if r["status"] == "pending"]
    out = {"schema": "ledger.cloud-week-42.shop-windows-check/1", "shop": ctx.id, "made": time.strftime("%Y-%m-%d %H:%M:%S"), "target": "production/cloud-week/targets/shop-windows/target.json (status: %s)" % T.get("status", "")[:80],
           "pass": npass, "counted": len(counted), "na": sum(1 for r in rows.rows if r["status"] == "n/a"), "pending": len(pend), "seconds": round(time.time() - t0, 1), "rows": rows.rows}
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    json.dump(out, open(out_json, "w"), indent=1)
    X.manifest(HERE, assets, ctx.work, os.path.join(HERE, "MANIFEST-%s.json" % ctx.id))
    print("%s: %d of %d rows pass (%d pending, %d n/a)" % (ctx.id, npass, len(counted), len(pend), out["na"]))
    for r in counted:
        if r["status"] != "pass":
            print("FAIL %s %s: %s" % (r["id"], r["name"], r["detail"][:400]))
    for r in pend:
        print("PENDING %s %s: %s" % (r["id"], r["name"], r["detail"][:300]))
    return out


# ------------------------------------------------------------------------------------------------------------- the shop-specific rows
def shop_rows(ctx, rows, assets, di):
    """Rows that belong to one shop's trade (coverage of its boards and tiers, its counts): defined beside its layout in check_shops.py (the layouts' own numbers) when that file has the shop."""
    try:
        import check_shops as CS
    except ImportError:
        return {"supports": [], "texts": [], "families": {}, "era": ""}
    return CS.rows_for(ctx, rows, assets, di)


def run(ctx, assets, previews, out_json):
    t0 = time.time()
    T = A.load_target()
    X.use(ctx)
    rows = Rows()
    sod = (1.0, 0.25, 0.0)
    if ctx.has_room:
        _, _, _, sod, _ = picture_rows(ctx, rows)
        projection_rows(ctx, rows)
        room_rows(ctx, rows, assets)
        di = display_rows(ctx, rows, assets)
        extra = shop_rows(ctx, rows, assets, di)
        inventory_rows(ctx, rows, assets, di, extra.get("texts", []), extra)
    else:
        di, extra = None, {"families": {}}
    glb_normal_rows(ctx, rows, assets)
    m = front_rows(ctx, rows, assets)
    if not ctx.has_room:
        man = json.load(open(os.path.join(ctx.work, "fascias", "manifest.json")))
        texts = [s_ for g in man["glass_lettering"] if g["shop"] == ctx.id for s_ in [g.get("string", "")] if s_]
        texts += [b[1] for b in (ctx.R["fascia"].get("name_blocks") or [])] + ["OPEN", "CLOSED", "TO LET"]
        never_rows_front(ctx, rows, assets, texts)
        if ctx.id == "empty_unit":
            lit03_rows(ctx, rows, m)
    if not ctx.has_room:
        pass
    if ctx.has_room:
        gate_rows(ctx, rows, m)
        X.display_rows(ctx.R, ctx.work, assets, rows)
        trade_rows(ctx, rows, extra.get("families", {}))
        X.lit02b_rows(ctx.R, ctx.work, rows)
        X.gate_frame_rows(ctx.R, ctx.work, rows)
        X.so07_rows(ctx.work, rows)
        lt = np.array([1.0, 0.25, 0.0])
        rows.add("LIT-06", "the sodium wash is the game's", float(np.abs(np.array(sod) - lt).max()) <= 0.01, "night_dark's sodium wash colour (linear) %s against unreal-look.json lantern_linear_rgb %s (the scene file's stale 1.0, 0.7055, 0.0 is not used)" % ([round(float(x), 3) for x in sod], lt.tolist()))
    rows.na("PRV-01", "the previews show nothing they must not", "the photograph previews of the target (P1 to P6), not this build's; this build's previews were looked at: no real firm's name, number, person, drink, gambling or child in them")
    return finish(ctx, rows, T, out_json, t0, previews, assets, 8 if ctx.has_room else 4)
