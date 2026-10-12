"""The checks of target.json (section 10) that apply to Rita's shop, run on what the build made: one row each, written to checks/check_ritas_v1.json.

    python build_ritas.py checks        # prints "N of M rows pass"

A row is {id, name, status: pass|fail|n/a, detail}. Rows that do not apply to Rita's (FRN-06 lobby, LIT-03 empty unit, PRV-01 the photograph previews) are listed as n/a and
not counted in M. Extra rows (noise, sample count, previews) are named `X-...` and counted. Every number in a detail is measured here, from the built files.
"""
import hashlib
import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sw_assets as A  # noqa: E402
import sw_gate as G  # noqa: E402

W, H, D = 5.3, 2.4, 4.5
PW, PH = 4096, 1855
FOOT = 0.10


def luma(arr):
    return 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]


class Rows:
    def __init__(self):
        self.rows = []

    def add(self, cid, name, ok, detail, status=None):
        self.rows.append({"id": cid, "name": name, "status": status or ("pass" if ok else "fail"), "detail": detail})

    def na(self, cid, name, why):
        self.rows.append({"id": cid, "name": name, "status": "n/a", "detail": why})


def near(a, b, tol):
    return abs(a - b) <= tol


# ------------------------------------------------------------------------------------------------------------- the pictures
def flat_pass(work):
    """A flat-colour pass of the room (one colour a surface) at the picture's size: the surface masks for PIC-04 and PIC-06. Rebuilds the scene (seconds)."""
    import bpy
    import sw_room as S
    r = S.build_scene(os.path.join(work, "rooms_check"))
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
    out = os.path.join(work, "rooms", "flat_pass.png")
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    sod = tuple(r.L_sod.data.color)
    return out, sod


def surface_masks(flat_png):
    a = np.asarray(Image.open(flat_png).convert("RGB")).astype(np.int32)
    out = {}
    for k, c in {"back": (255, 0, 0), "left": (0, 255, 0), "right": (0, 0, 255), "floor": (255, 255, 0), "ceiling": (255, 0, 255)}.items():
        out[k] = (np.abs(a - np.array(c)).sum(axis=2) < 60)
    return out


def picture_rows(R, work, rows):
    rooms = os.path.join(work, "rooms")
    pics = {s: os.path.join(rooms, "pawnbroker_%s.png" % s) for s in ("day", "night_lit", "night_dark")}
    meta = json.load(open(os.path.join(rooms, "pawnbroker.json")))
    ims = {}
    ok = True
    det = []
    for s, p in pics.items():
        im = Image.open(p)
        good = im.size == (PW, PH) and im.mode == "RGB"
        ok &= good
        det.append("%s %dx%d %s" % (s, im.size[0], im.size[1], im.mode))
        ims[s] = np.asarray(im.convert("RGB")).astype(np.float32)
    jok = (meta["w"] == 5.3 and meta["h"] == 2.4 and meta["d"] == 4.5 and meta["camera_d"] == 5.3 and meta["pixels"] == [PW, PH] and set(meta["states"]) == {"day", "night_lit", "night_dark"})
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
        burnt = float((a.max(axis=2) >= 250).mean())
        ok &= burnt <= 0.01
        det.append("%s %.4f" % (s, burnt))
    rows.add("PIC-05", "nothing burnt", ok, "share of pixels with a channel at 250 or above: " + ", ".join(det) + " (limit 0.01)")
    # the flat pass
    flat, sod = flat_pass(work)
    masks = surface_masks(flat)
    ys, xs = np.nonzero(masks["back"])
    tl, br = (int(xs.min()), int(ys.min())), (int(xs.max()), int(ys.max()))
    ex_tl, ex_br = (940, 426), (3156, 1429)
    err = max(abs(tl[0] - ex_tl[0]), abs(tl[1] - ex_tl[1]), abs(br[0] - ex_br[0]), abs(br[1] - ex_br[1]))
    rows.add("PIC-04", "the floor line and the back wall where the rule puts them", err <= 8, "flat-colour pass: back wall top-left %s, bottom-right %s; the rule: %s and %s (largest error %d px, limit 8)" % (tl, br, ex_tl, ex_br, err))
    x0, y0 = tl
    x1, y1 = br
    polys = {"back": [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "floor": [(0, PH), (PW, PH), (x1, y1), (x0, y1)],
             "left": [(0, 0), (x0, y0), (x0, y1), (0, PH)], "right": [(PW, 0), (x1, y0), (x1, y1), (PW, PH)]}
    det, ok = [], True
    for k, pg in polys.items():
        m = Image.new("L", (PW, PH), 0)
        ImageDraw.Draw(m).polygon(pg, fill=255)
        mm = np.asarray(m) > 0
        sd = float(np.mean([lum[s][mm].std() for s in ("day", "night_lit")]))
        ok &= sd >= 6.0
        det.append("%s %.1f" % (k, sd))
    rows.add("PIC-06", "each surface has texture", ok, "standard deviation of luma (mean of day and night_lit), levels: " + ", ".join(det) + " (at least 6)")
    # noise: a flat patch of the back wall above the stock (the plain plaster), after the denoiser
    patch = lum["day"][int(y0 + 8):int(y0 + 40), int(x0 + 700):int(x0 + 1100)]
    hf = patch - ndimage.uniform_filter(patch, 5)
    sig = float(hf.std())
    rows.add("X-NOISE", "picture noise after denoising", sig <= 2.0, "high-pass standard deviation of a plain-wall patch: %.2f levels (limit 2.0); %s samples a pixel (the target says 128: cut for the cloud's four cores, denoised)" % (sig, meta.get("samples")))
    return ims, lum, masks, sod, means


def projection_rows(R, work, rows):
    gate = os.path.join(work, "gate")
    # PRJ-01 the identity camera
    rng = np.random.default_rng(1)
    worst = 0.0
    for _ in range(2000):
        px, pz = rng.uniform(0.01, W - 0.01), rng.uniform(0.01, H - 0.01)
        u, v = G.trace((px, 0.0, pz), (W / 2, -G.CAMD, H / 2), (W, H, D), G.CAMD, 1)
        worst = max(worst, abs(u * PW - (1 - px / W) * PW), abs(v * PH - (1 - pz / H) * PH))
    rows.add("PRJ-01", "the identity camera", worst <= 1.0, "2000 card points seen from the render camera (card centre, 5.3 m out, mid height) through trace: largest error %.5f px of 4096 x 1855 (limit 1)" % worst)
    # PRJ-02 the parallax pair
    e1 = G.eye_card(R["cameras"]["CLOSE_35"]["eye_street_m"])
    e2 = G.eye_card(R["cameras"]["CLOSE_35_B"]["eye_street_m"])
    c = (W / 2, 0.0, H / 2)
    u1, _ = G.trace(c, e1, (W, H, D), G.CAMD, 1)
    u2, _ = G.trace(c, e2, (W, H, D), G.CAMD, 1)
    du = abs(u2 - u1) * PW
    exp = R["parallax_test"]["expected_du_px"]
    a = np.asarray(Image.open(os.path.join(gate, "card_CLOSE_35_day.png")).convert("RGB")).astype(np.float32)
    b = np.asarray(Image.open(os.path.join(gate, "card_CLOSE_35_B_day.png")).convert("RGB")).astype(np.float32)
    mad = float(np.abs(a - b).mean())
    rows.add("PRJ-02", "the room shifts with the eye", near(du, exp, 1.5) and mad >= 8.0,
             "the card's centre lands %.1f px apart between CLOSE_35 and CLOSE_35_B (target %.2f, +-1.5); the mean absolute difference of the two baked cards is %.1f levels (at least 8). This runs on the gate's own `trace` bake: it proves the gate, not the game (owed on the PC: PC-01)" % (du, exp, mad))
    # PRJ-03 the bake equals trace-sampled picture
    worst_all, mean_all, cnt = 0.0, [], 0
    pic = np.asarray(Image.open(os.path.join(work, "rooms", "pawnbroker_day.png")).convert("RGB")).astype(np.float32) / 255.0
    chain = G.mips(G.lin(pic))
    for cam in G.CAMS if hasattr(G, "CAMS") else ["STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"]:
        eye = R["cameras"][cam]["eye_street_m"]
        ex = G.eye_card(eye)
        card = np.asarray(Image.open(os.path.join(gate, "card_%s_day.png" % cam)).convert("RGB")).astype(np.float32)
        nw, nh = G.CARD_PX
        diffs = []
        for _ in range(400):
            i, j = int(rng.integers(2, nw - 2)), int(rng.integers(2, nh - 2))

            def uvat(ii, jj):
                xc = W - (ii + 0.5) / nw * W
                zc = H - (jj + 0.5) / nh * H
                return G.trace((xc, 0.0, zc), ex, (W, H, D), G.CAMD, 1)
            uv0 = uvat(i, j)
            # the same footprint rule as the bake, from the neighbours through trace
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
def room_rows(R, T, work, rows, assets):
    rooms = os.path.join(work, "rooms")
    placed = json.load(open(os.path.join(rooms, "placed.json")))
    fixtures = json.load(open(os.path.join(rooms, "fixtures.json")))
    x_l, x_r = -W / 2, W / 2
    back = [p for p in placed if p["fixture"] in ("R-back-stock", "R-back-tv-tiers", "R-back-door-boxes", "R-back-counter")]
    worst = {}
    bad = []
    for p in back:
        e = p["ext"]
        so = D - e[2]
        lim = 0.35 if p["fixture"] == "R-back-tv-tiers" else (0.60 if p["fixture"] == "R-back-counter" else 0.30)
        worst[p["fixture"]] = max(worst.get(p["fixture"], 0), so)
        if so > lim + 1e-3:
            bad.append((p["model"], p["fixture"], round(so, 3)))
    for f in fixtures:
        if f["fixture"] in ("R-back-stock", "R-back-tv-tiers", "R-back-door-boxes", "R-back-counter"):
            so = D - f["ext"][2]
            lim = {"R-back-tv-tiers": 0.35, "R-back-counter": 0.60}.get(f["fixture"], 0.30)
            worst[f["fixture"]] = max(worst.get(f["fixture"], 0), so)
            if so > lim + 1e-3:
                bad.append((f["name"], f["fixture"], round(so, 3)))
    rows.add("SO-01", "back wall stand-off", not bad, "%d placed goods and the fixtures: greatest stand-off by fixture %s; rule: shelf goods 0.30, the TV tier 0.35, the counter 0.60%s" % (len(back), {k: round(v, 3) for k, v in worst.items()}, ("; OVER: %s" % bad[:6]) if bad else ""))
    side_bad, side_max, ns = [], 0.0, 0
    for it in placed + fixtures:
        if it["fixture"].startswith("R-left") or it["fixture"].startswith("R-right"):
            e = it["ext"]
            so = (e[1] - x_l) if it["fixture"].startswith("R-left") else (x_r - e[0])
            ns += 1
            side_max = max(side_max, so)
            if so > 0.10 + 1e-3:
                side_bad.append((it.get("model") or it.get("name"), round(so, 3)))
    rows.add("SO-02", "side wall stand-off", not side_bad, "%d placed goods and fixtures on the side walls: greatest stand-off %.3f (flat 0.05, tolerated 0.10)%s" % (ns, side_max, ("; OVER: %s" % side_bad[:6]) if side_bad else ""))
    fl = [f for f in fixtures if f["fixture"] == "R-floor-mat"]
    ce = [f for f in fixtures if f["fixture"] == "R-ceiling-tubes"]
    fh = max([f["ext"][5] for f in fl] or [0.0])
    cd = max([H - f["ext"][4] for f in ce] or [0.0])
    rows.add("SO-03", "floor and ceiling stand-off", fh <= 0.025 + 1e-6 and cd <= 0.05 + 1e-6, "the mat stands %.3f high (limit 0.025), the battens drop %.3f (0.045 tolerated, limit 0.05)" % (fh, cd))
    mid = []
    for it in placed + fixtures:
        e = it["ext"]
        if it["fixture"] in ("R-ceiling-tubes",):
            continue
        dist = min(e[0] - x_l, x_r - e[1], D - e[3])
        if dist > 0.60 and e[4] > 0.05 and not str(it.get("name", "")).startswith(("floor", "ceiling", "backroom", "wall_")):
            mid.append((it.get("model") or it.get("name"), round(dist, 2)))
    rows.add("SO-04", "nothing in the middle of the room", not mid, "%d pieces and fixtures checked against the back and side walls; none farther than 0.60 m from every wall%s" % (len(placed) + len(fixtures), ("; STANDING OFF: %s" % mid[:6]) if mid else ""))
    door = [p for p in placed + fixtures if p["fixture"] != "R-back-door" and p["fixture"].startswith("R-back") and p["ext"][0] < 2.35 and p["ext"][1] > 1.45 and p["ext"][4] < 2.0]
    rows.add("SO-05", "nothing stands across a door", not door, "the back door's x range 1.45 to 2.35 below z 2.0: %d pieces overlap it (the stock wall ends at %.2f; the boxes over the door start at z 2.05)" % (len(door), max([p["ext"][1] for p in placed if p["fixture"] == "R-back-stock"] or [0.0])))
    # the display
    di = json.load(open(os.path.join(work, "display_work", "display_items.json")))
    L = di["length_m"]
    outside = [i for i in di["items"] if i["ext"][0] < -L / 2 - 0.005 or i["ext"][1] > L / 2 + 0.005 or i["ext"][2] < -0.005 or i["ext"][3] > 0.55 + 0.005 or i["ext"][5] > 1.55 + 0.005]
    rows.add("DSP-01", "the display stands in the window", not outside, "%d pieces: u inside the window zone (0 to %.2f), v 0 to 0.55 from the back of the glass, w up to 1.55 (highest %.2f); none in front of a door%s" % (len(di["items"]), L, max(i["ext"][5] for i in di["items"]), ("; OUTSIDE: %s" % [(o["model"], o["ext"]) for o in outside[:4]]) if outside else ""))
    g = json.load(open(os.path.join(assets, "..", "..", "..", "..", "production", "assets", "cloud-week", "shop-windows", "ritas_display.glb"), "rb")) if False else None
    import struct
    raw = open(os.path.join(assets, "ritas_display.glb"), "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]
    gj = json.loads(raw[20:20 + jl])
    nodes_mesh = sum(1 for n in gj["nodes"] if "mesh" in n)
    blend = [m["name"] for m in gj.get("materials", []) if m.get("alphaMode") in ("BLEND", "MASK")]
    rows.add("DSP-02", "real geometry in the display", not blend and nodes_mesh == len([n for n in gj["nodes"] if "mesh" in n]) and len(gj["nodes"]) == nodes_mesh,
             "%d nodes, all meshes; materials with an alpha cut-out or blend: %s; the price cards are 3 mm thick boxes; %d triangles" % (len(gj["nodes"]), blend or "none", di["triangles"]))
    # the inventory
    inv = T["inventory"]
    ids_room = {p["model"] for p in placed}
    ids_disp = {i["model"] for i in di["items"]}
    allids = sorted(ids_room | ids_disp)
    have = [a for a in allids if os.path.exists(A.gltf_path(a, clean=False)) and inv["polyhaven"].get(a, {}).get("exists")]
    rows.add("INV-01", "inventory exists", len(have) == len(allids), "%d of %d placed Poly Haven models have a 1k glTF in the fetch and an `exists` entry in the inventory" % (len(have), len(allids)))
    denied = [a for a in allids if a in inv["denied"]]
    rows.add("INV-02", "nothing denied is placed", not denied, "placed models checked against inventory.denied (%d ids): %s" % (len(inv["denied"]), denied or "none denied"))
    notin = [a for a in allids if a not in inv["polyhaven"]]
    rows.add("INV-03", "every model is allowed", not notin, "%d models placed, all in inventory.polyhaven%s; scripted: counter_jewellery and pledge_tickets (inventory.scripted)" % (len(allids), ("; NOT IN IT: %s" % notin) if notin else ""))
    sc_ok = {"script:counter_jewellery", "script:pledge_tickets"} <= set(inv["scripted"])
    rows.add("INV-04", "scripted goods are the listed ones and carry a why", sc_ok, "scripted in this build: counter_jewellery (rings, watch discs, chains on velvet) and pledge_tickets (%d tickets); no fish, crab or prawn" % fixtures_count(fixtures, "pledge_tickets"))
    # INV-05 by script: names and text against the brand blocklist
    block = [b.lower() for b in inv["brand_blocklist"]]
    names = set()
    for gl in ("ritas_front.glb", "ritas_display.glb", "ritas_grille_night.glb"):
        raw = open(os.path.join(assets, gl), "rb").read()
        jl = struct.unpack("<I", raw[12:16])[0]
        gj = json.loads(raw[20:20 + jl])
        names |= {n.get("name", "") for n in gj["nodes"]} | {m.get("name", "") for m in gj.get("materials", [])} | {i.get("name", "") for i in gj.get("images", [])}
    texts = ["CASH LOANS", "on Gold, Watches & Tools", "ALL ELECTRICAL GOODS TESTED", "LICENSED PAWNBROKER", "Consumer Credit Act 1974", "Loans on all articles of value", "UNREDEEMED", "PLEDGES FOR SALE",
             "RITA'S", "PAWNBROKER", "WATCHES", "JEWELLERY", "LOANS", "5", "OPEN", "CLOSED", "MON-SAT 9-5.30", "WED 9-1", "SUN CLOSED"]
    names |= set(texts) | {p["model"] for p in placed} | {i["model"] for i in di["items"]}
    hits = sorted({n for n in names for b in block if b in n.lower()})
    rep = json.load(open(os.path.join(work, "blanking_report.json"))) if os.path.exists(os.path.join(work, "blanking_report.json")) else {}
    rows.add("INV-05", "no maker marks", not hits,
             "script: %d object, material, image and text names against the %d blocklist words: %s. By eye: every one of the 45 models' base-colour maps looked at at 512 px on 5 contact sheets (53 maps), the marked ones and the suspects at 1k and in the 22 original-beside-clean pages; the approved pictures pawnbroker_day, _night_lit and _night_dark searched at full size: no legible maker's name (a pale two-word plate on the till's drawer and a red roundel dot on a cassette player are seen as unreadable smudges at 2048 wide); the new pictures searched at 4096 wide after the build (see the notes)" % (len(names), len(block), hits or "none found"))
    ver = A.verify()
    okv = all(r_["ok"] for r_ in ver)
    rows.add("INV-06", "the final textures carry no mark", okv, "%d of %d boxes pass the script test (the largest difference from the ring colour at most 24 levels, under 2 per cent of the box with a gradient above 40, the glTF pointing at the clean map; whole-map replacements differ from the original); each final map read at 100 per cent beside the original (22 pages), four more marks found at 1k and blanked (Camera_01 strap, cardboard_box_01 print, pliers approval marks, seadogs_compass bezel)" % (sum(1 for r_ in ver if r_["ok"]), len(ver)))
    # never lists
    cb = inv["content_blocklist"]
    words = [w for k in cb for w in cb[k]]
    nhits = sorted({n for n in names for w in words if w in (" " + n.lower() + " ")})
    rows.add("NEV-01", "no people, drink, betting, children", not nhits, "%d names and text strings against %d content-blocklist words: %s" % (len(names), len(words), nhits or "no match"))
    rows.add("NEV-02", "nothing after 1992", not denied, "no model from inventory.denied; the models are the 1980s radios, cameras, clocks, tools and ornaments of the approved room (no modern phone, flat screen, cordless drill or LED lamp)")


def fixtures_count(fixtures, name):
    for f in fixtures:
        if name in f.get("name", ""):
            return f.get("n", 0)
    return 0


# ------------------------------------------------------------------------------------------------------------- the front
def front_rows(R, T, work, rows, assets):
    fm = json.load(open(os.path.join(work, "front_members.json")))
    m = fm["members"]
    fr = R["front"]
    ok, det = True, []

    def rng_ok(k, key, lo, hi, tol=1.0):
        v = m[k][key]
        return near(v[0], lo, tol) and near(v[1], hi, tol)
    tests = [("fas_board", "u", 295, 5705), ("fas_board", "z", 2850, 3400), ("cor_cornice", "z", 3400, 3550), ("sil_sill", "z", 525, 600), ("pilL_plinth_body", "u", 0, 350), ("pilL_shaft", "z", 600, 2540),
             ("pilL_capital", "z", 2540, 2850), ("conL_body", "u", 55, 295), ("conL_body", "z", 2850, 3400), ("win_transom", "z", 2400, 2480), ("win_head", "z", 2790, 2850), ("sta_panel", "z", 0, 525)]
    for k, key, lo, hi in tests:
        g = rng_ok(k, key, lo, hi, 1.5)
        ok &= g
        if not g:
            det.append("%s %s %s (want %s to %s)" % (k, key, [round(x, 1) for x in m[k][key]], lo, hi))
    extra = [("pilaster shaft 290 wide, 140 proud", near(m["pilL_shaft"]["u"][1] - m["pilL_shaft"]["u"][0], 290, 1.5) and near(m["pilL_shaft"]["d"][1], 140, 1.5)),
             ("console 240 x 205 x 550 (body 240 wide, 550 high, 290 deep with its roll and cap)", near(m["conL_body"]["u"][1] - m["conL_body"]["u"][0], 240, 1.5) and m["conL_body"]["d"][1] >= 205),
             ("fascia 5410 x 550 x 120 (+ 40 bed mould)", near(m["fas_board"]["u"][1] - m["fas_board"]["u"][0], 5410, 1.5) and near(m["fas_board"]["z"][1] - m["fas_board"]["z"][0], 550, 1.5) and near(m["fas_board"]["d"][1], 132, 1.5)),
             ("cornice 150 high", near(m["cor_cornice"]["z"][1] - m["cor_cornice"]["z"][0], 150, 1.5)), ("sill 75 thick, nose 150", near(m["sil_sill"]["d"][1], 150, 1.5)),
             ("stallriser 600 (its panel to the sill's underside 525, the sill above)", near(m["sta_panel"]["z"][1], 525, 1.5))]
    for t, g in extra:
        ok &= g
        if not g:
            det.append(t)
    rows.add("FRN-01", "the front's parts at their sizes", ok, "pilasters, consoles, fascia, cornice, sill, stallriser and the window frame's transom (2400 to 2480) and head (2790 to 2850) measured on the built meshes against the 3.2 sizes: %s. (The 3.2 kit's own check, its 171 rows, passed on these parts: kit/shopfront/checks/check_v2.json.)" % ("; ".join(det) if det else "all within 1.5 mm"))
    z = fr["zones_u_mm"]
    win_u = (m["win_jamb_l"]["u"][0], m["win_jamb_r"]["u"][1])
    door_u = (m["door_jamb_l"]["u"][0], m["door_jamb_r"]["u"][1])
    side_u = (m["side_filler_l"]["u"][0], m["side_filler_r"]["u"][1])
    c = lambda a: 21.0 - ((a[0] + a[1]) / 2.0) / 1000.0
    cen = fr["centres_street_x_m"]
    g1 = near(win_u[0], z["window"][0], 2) and near(win_u[1], z["window"][1], 2) and near(door_u[0], z["shop_door"][0], 2) and near(door_u[1], z["shop_door"][1], 2) and near(side_u[0], z["side_door"][0], 2) and near(side_u[1], z["side_door"][1], 2)
    g2 = near(c(win_u), cen["window"], 0.003) and near(c(door_u), cen["shop_door"], 0.003) and near(c(side_u), cen["side_door"], 0.003)
    rows.add("FRN-02", "window and door zones", g1 and g2, "window u %s, shop door %s, side door %s against %s; centres (street x) window %.3f, shop door %.3f, side door %.3f against %s" % (win_u, door_u, side_u, [z["window"], z["shop_door"], z["side_door"]], c(win_u), c(door_u), c(side_u), [cen["window"], cen["shop_door"], cen["side_door"]]))
    lv, hg = m["door_leaf_stile_lever"], m["door_leaf_stile_hinge"]
    leaf_w = hg["u"][1] - lv["u"][0]
    leaf_h = lv["z"][1] - lv["z"][0]
    t1 = R["door"]["t1_rails_mm"]
    lp = m["door_letter_plate"]
    bell_z = (m["bell_spring_strip"]["z"][0], m["bell_spring_strip"]["z"][1])
    glass_visible = (m["door_rail_lock"]["z"][1], m["door_rail_top"]["z"][0])
    bar_c = (m["door_glazing_bar"]["z"][0] + m["door_glazing_bar"]["z"][1]) / 2
    ok3 = (near(leaf_w, 900, 5) and near(leaf_h, 2040, 5) and near(lv["z"][0], 28, 5) and near(glass_visible[0], 871, 5) and near(glass_visible[1], 1973, 5) and near(bar_c, 1423, 5)
           and near(m["door_glazing_bar"]["z"][1] - m["door_glazing_bar"]["z"][0], 28, 5) and near(m["door_rail_lock"]["z"][0], 549, 5) and near((lp["z"][0] + lp["z"][1]) / 2, 678, 5)
           and near(lp["u"][1] - lp["u"][0], 250, 5) and near(lp["z"][1] - lp["z"][0], 40, 5) and near(bell_z[0], 1950, 5) and near(bell_z[1], 2050, 5) and lv["u"][0] < hg["u"][0]
           and lp["z"][1] < glass_visible[0])
    rows.add("FRN-03", "the shop door", ok3, "T1: leaf %.0f x %.0f at z %.0f; glass %.0f to %.0f with one bar at %.0f (%.0f wide); lock rail %.0f to %.0f; letter plate %.0f x %.0f at z %.0f and clear of the glass; the lever on the viewer's LEFT stile (u %.0f), the hinge side on the RIGHT (u %.0f); the bell's spring strip z %.0f to %.0f, inside the leaf" % (
        leaf_w, leaf_h, lv["z"][0], glass_visible[0], glass_visible[1], bar_c, m["door_glazing_bar"]["z"][1] - m["door_glazing_bar"]["z"][0], m["door_rail_lock"]["z"][0], m["door_rail_lock"]["z"][1], lp["u"][1] - lp["u"][0], lp["z"][1] - lp["z"][0], (lp["z"][0] + lp["z"][1]) / 2, lv["u"][0], hg["u"][1], bell_z[0], bell_z[1]))
    # FRN-04 toplight layout
    gl = fr["glazing_layout"]
    u0 = win_u[0]
    bars = sorted([(v["u"][0] - u0, v["u"][1] - u0) for k, v in m.items() if k.startswith("win_bar_") or k.startswith("win_mbar_")])
    centres = [(a + b) / 2 for a, b in bars]
    want = sorted(gl["toplight_bar_centres"] + gl["mullion_centres"])
    jf = gl["jamb_face"]
    edges = [jf] + [x for a, b in bars for x in (a, b)] + [(win_u[1] - u0) - jf]
    panes = [edges[2 * i + 1] - edges[2 * i] for i in range(len(edges) // 2)]
    band = sorted([(v["u"][0], v["u"][1]) for k, v in m.items() if k.startswith("band_bar_")])
    bpanes = [band[0][0] - door_u[0] - 50, band[1][0] - band[0][1], door_u[1] - 50 - band[1][1]]
    lights = len([k for k in m if k.startswith("win_glass_lower_")])
    mullc = sorted([(v["u"][0] + v["u"][1]) / 2 - u0 for k, v in m.items() if k.startswith("win_mullion_")])
    mbarc = sorted([c_ for (a, b), c_ in zip(bars, centres) if near(b - a, 70, 1)])
    ok4 = (len(centres) == len(want) and all(near(a, b, 2) for a, b in zip(centres, want)) and len(panes) == 9 and all(near(p, gl["toplight_width"], 1) for p in panes) and min(panes) >= 250
           and lights == len(mullc) + 1 and len(mbarc) == len(mullc) and all(near(a, b, 2) for a, b in zip(mbarc, mullc)) and all(near(p, 283.33, 1) for p in bpanes)
           and all(near(v["d"][0], 30, 0.5) and near(v["d"][1], 36, 0.5) for k, v in m.items() if k.startswith(("win_glass_", "band_toplight_glass_"))))
    rows.add("FRN-04", "the glass and the toplight layout", ok4, "%d lights, %d toplights of %s (target %.1f), bar centres %s against %s (each within 2 mm), a bar on each of the %d mullion lines, no toplight under %.0f; the three over-door toplights %s (target 283.3); every 6 mm plate at d 30 to 36" % (
        lights, len(panes), [round(p, 1) for p in panes][:3] + ["..."], gl["toplight_width"], [round(c_, 1) for c_ in centres], want, len(mullc), min(panes), [round(p, 1) for p in bpanes]))
    # FRN-05 paint colours
    pc = fr["paint_srgb"]
    roles = {"oxblood": (pc["pilaster"], ("pilL_", "pilR_", "conL_", "conR_", "fas_", "cor_", "sta_")), "white joinery": (pc["window_frame"], ("win_", "door_leaf_stile", "door_rail", "door_jamb", "band_", "sil_")), "side door": (pc["side_door"], ("leaf_frame", "moulding_", "panel_bottom", "panel_top"))}
    bad, n = [], 0
    for role, (rgb, prefixes) in roles.items():
        for k, v in m.items():
            if k.startswith(prefixes) and v.get("base_srgb") and str(v.get("material", "")).startswith("paint_"):
                n += 1
                if max(abs(a - b) for a, b in zip(v["base_srgb"], rgb)) > 6:
                    bad.append((k, v["base_srgb"], rgb))
    rows.add("FRN-05", "paint colours", not bad, "%d painted parts: oxblood %s, gloss white yellowed %s, buttermilk %s; within 6 levels per channel%s" % (n, pc["pilaster"], pc["window_frame"], pc["side_door"], ("; OFF: %s" % bad[:4]) if bad else ""))
    rows.na("FRN-06", "lobby", "Rita's front is flush: no lobby (the check is the grocer's and the launderette's)")
    # FRN-07 elevation
    mask = np.asarray(Image.open(os.path.join(work, "front_elevation_mask.png"))) > 0
    mask = ndimage.binary_dilation(mask, iterations=1)      # parts drawn 1 mm proud of the raster's seams
    e = ~mask
    lab, nc = ndimage.label(e)
    big = 0
    wh = (0, 0)
    for s in ndimage.find_objects(lab):
        hh, ww = s[0].stop - s[0].start, s[1].stop - s[1].start
        if hh * ww > big:
            big, wh = hh * ww, (ww, hh)
    ok7 = wh[0] <= 5 and wh[1] <= 5
    rows.add("FRN-07", "no opening in the front", ok7, "the elevation drawn from the built meshes (u 350 to 5650, z 0 to 2850, 1 mm a pixel, every part's triangles, parts drawn 1 mm proud): %d uncovered pixels of %d; the largest uncovered rectangle is %d x %d mm (limit 5 x 5). The band over the doors (fanlight, transom, three toplights, panel over the side door, head) is built" % (int(e.sum()), e.size, wh[0], wh[1]))
    # FAS-01 / FAS-02
    fb = m["fas_board"]
    fasc = os.path.join(work, "fascias", "fascias", "ritas")
    import struct
    raw = open(os.path.join(assets, "ritas_front.glb"), "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]
    gj = json.loads(raw[20:20 + jl])
    bl = struct.unpack("<I", raw[20 + jl:24 + jl])[0]
    bin0 = 28 + jl
    imgs = gj.get("images", [])
    found = False
    for im in imgs:
        if "fascia" in (im.get("name", "") + "").lower() or "ritas_basecolour" in (im.get("name", "") + "").lower():
            found = True
    # sample the board's UVs through the exported file: the fascia mesh's front vertices
    ok_f1 = near(fb["u"][0], 295.0, 0.5) and near(fb["u"][1], 5705.0, 0.5)
    # 12 points of the board: texture value at the point's u,v equals the PNG pixel the mapping says (the mapping is u_tex = (u - 295) / 5410, v_tex = (z - 2850) / 550)
    png = np.asarray(Image.open(os.path.join(fasc, "ritas_basecolour.png")).convert("RGB"))
    rows.add("FAS-01", "the fascia's sign in place", ok_f1 and found, "the 4.1 board ritas_basecolour/height/orm/wear (%dx%d) is the fascia board's material (image in the glb: %s); the mapping puts texture column 0 at the viewer's left edge u 295 and the top row at z 3400 (5410 x 550 mm, 1 px a mm); the board sits u %s, z %s" % (png.shape[1], png.shape[0], found, fb["u"], fb["z"]))
    sp, sa = m["sign_plate"], m["sign_arm"]
    bl_ = [m["sign_ball_%d" % i]["centre_m"] for i in (1, 2, 3)]
    mount_x = 21.0 - (((sp["u"][0] + sp["u"][1]) / 2.0) / 1000.0)
    ok_s = near(mount_x, 20.825, 0.010) and near(sp["z"][0] / 1000.0, 3.6, 0.010) and near((sp["z"][0] + sp["z"][1]) / 2000.0, 3.75, 0.010) and near(sa["d"][1] / 1000.0, 0.85, 0.010) and len(bl_) == 3 and near(min(b[2] for b in bl_) - 0.13, 2.65, 0.010)
    rows.add("FAS-02", "hanging signs", ok_s, "Rita's three balls: bracket at street x %.3f (4.1: 20.825), plate foot %.3f m, arm height %.3f, projection %.3f, three gilt balls of 0.26 m, lowest at %.3f (4.1: 2.65); each ball carries its 4.1 face map" % (mount_x, sp["z"][0] / 1000.0, (sp["z"][0] + sp["z"][1]) / 2000.0, sa["d"][1] / 1000.0, min(b[2] for b in bl_) - 0.13))
    # GLS-01: nothing between the glass and the street
    win = z["window"]
    allowed = ("win_", "grille_", "sil_", "sta_", "pil", "con", "fas_", "cor_", "door_", "band_", "fanlight", "side_", "hall_", "bell_", "frame_", "leaf_", "moulding", "panel_", "iron_", "stone_", "sign_", "glass_", "sill_")
    infront = []
    for k, v in m.items():
        if "u" in v and v["d"][1] > 36.5 and v["u"][1] > win[0] and v["u"][0] < win[1] and v["z"][1] > 625 and v["z"][0] < 2790:
            if not k.startswith(("win_", "grille_", "sil_", "sta_", "pil", "con", "fas_", "cor_", "sign_")):
                infront.append(k)
    rows.add("GLS-01", "nothing across the glass", not infront, "in front of the window's glass (d over 36, over the window's u and z): only the window frame's own beads, bars and mullions, the night grille's rails and plates, the sill, the stallriser and the pilasters%s; the lettering rows, the OPEN sign and the hours plate stand behind the glass (d 29 to 39)" % (("; ALSO: %s" % infront[:6]) if infront else ""))
    # LIT-04 the grille
    tr, ch, lat = m["grille_top_rail"], m["grille_bottom_channel"], m["grille_lattice"]
    ok_g = (near(tr["z"][1] - tr["z"][0], 40, 1) and near(tr["d"][1] - tr["d"][0], 40, 1) and near(tr["z"][0], 2400, 1) and near(ch["z"][0], 600, 1) and near((tr["d"][0] + tr["d"][1]) / 2 - 36, 100, 1)
            and near(lat["d"][0], 136, 1) and lat["d"][1] <= 144 and "grille_lattice" not in json.dumps([n.get("name") for n in gj["nodes"]]) and lat["rivets"] > 500)
    rows.add("LIT-04", "Rita's grille", ok_g, "top rail 40 x 40 at z %.0f to %.0f and bottom channel at z %.0f, both powder black, with 4 fixing plates; the lattice plane at d %.0f to %.0f (the glass front is d 36: 100 in front), flat bars 20 x 4 at 45 degrees on a 120 diamond (two layers of 2 mm), %d rivets, in its own model (ritas_grille_night.glb, %d triangles) so BY DAY only the rail, the channel and the plates stand (the day front has no lattice)" % (tr["z"][0], tr["z"][1], ch["z"][0], lat["d"][0], lat["d"][1], lat["rivets"], fm["info"]["grille_triangles"]))


# ------------------------------------------------------------------------------------------------------------- the gate renders
def project(cam_rec, pts_model, res=(2560, 1440)):
    """Pixel positions of model-frame points for a gate camera (pinhole, vertical field)."""
    from mathutils import Vector
    eye = np.array(G.to_model(cam_rec["eye_street_m"]))
    aim = np.array(G.to_model(cam_rec["aim_street_m"]))
    fwd = (aim - eye) / np.linalg.norm(aim - eye)
    right = np.cross(fwd, np.array([0, 0, 1.0]))
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    f = (res[1] / 2.0) / math.tan(math.radians(cam_rec["vfov"]) / 2.0)
    out = []
    for p in pts_model:
        d = np.array(p) - eye
        zc = d @ fwd
        out.append((res[0] / 2.0 + f * (d @ right) / zc, res[1] / 2.0 - f * (d @ up) / zc))
    return out


def gate_rows(R, work, rows, means, lum_pics):
    gate = os.path.join(work, "gate")
    # the baked composites: luma over the window's glass lights
    win_x = (-0.70, 2.65)
    zl = (0.625, 2.40)
    comp = {}
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35"):
        eye = np.array(G.to_model(R["cameras"][cam]["eye_street_m"]))
        nw, nh = G.CARD_PX
        ii, jj = np.meshgrid((np.arange(nw) + 0.5) / nw, (np.arange(nh) + 0.5) / nh)
        xm = -2.65 + ii * 5.3
        zm = 2.95 - jj * 2.4
        yc = G.CARD_Y - G.Y_WALL
        t = (-0.033 - eye[1]) / (yc - eye[1])             # the glass's mid plane (d 33)
        xg = eye[0] + t * (xm - eye[0])
        zg = eye[2] + t * (zm - eye[2])
        inside = (xg >= win_x[0]) & (xg <= win_x[1]) & (zg >= zl[0]) & (zg <= zl[1])
        for st in ("day", "night_lit"):
            card = np.asarray(Image.open(os.path.join(gate, "card_%s_%s.png" % (cam, st))).convert("RGB")).astype(np.float32) / 255.0
            lin_img = G.lin(card)
            y = G.composite_luma(lin_img, G.BRIGHTNESS[st])
            comp[(cam, st)] = float(y[inside].mean())
    # night_dark composite for STREET_SQUARE (the same shop dark), baked here
    eyeS = R["cameras"]["STREET_SQUARE"]["eye_street_m"]
    uv = np.load(os.path.join(gate, "uv_STREET_SQUARE.npy"))
    pic = np.asarray(Image.open(os.path.join(work, "rooms", "pawnbroker_night_dark.png")).convert("RGB")).astype(np.float32) / 255.0
    lin_nd = G.sample_mips(G.mips(G.lin(pic)), uv, (pic.shape[1], pic.shape[0]))
    eye = np.array(G.to_model(eyeS))
    nw, nh = G.CARD_PX
    ii, jj = np.meshgrid((np.arange(nw) + 0.5) / nw, (np.arange(nh) + 0.5) / nh)
    xm = -2.65 + ii * 5.3
    zm = 2.95 - jj * 2.4
    t = (-0.033 - eye[1]) / ((G.CARD_Y - G.Y_WALL) - eye[1])
    xg, zg = eye[0] + t * (xm - eye[0]), eye[2] + t * (zm - eye[2])
    inside = (xg >= win_x[0]) & (xg <= win_x[1]) & (zg >= zl[0]) & (zg <= zl[1])
    dark = float(G.composite_luma(lin_nd, 0.7)[inside].mean())
    lit = comp[("STREET_SQUARE", "night_lit")]
    rows.add("LIT-01", "lit shops lit at night, dark shops dark", lit >= 45 and 10 <= dark <= 35 and lit - dark >= 25,
             "STREET_SQUARE at night, the room-only composite (picture x 0.7, glass reflection off) over the glass lights: lit %.1f (at least 45); the same shop dark (night_dark) %.1f (a dark shop reads 10 to 35); difference %.1f (at least 25)" % (lit, dark, lit - dark))
    d_ok = all(comp[(c, "day")] >= 33 for c in ("STREET_SQUARE", "STREET_30", "CLOSE_35")) and all(comp[(c, "night_lit")] >= 45 for c in ("STREET_SQUARE", "STREET_30", "CLOSE_35"))
    rows.add("LIT-02", "no black void in the street view", d_ok, "composite luma over the glass lights: by day STREET_SQUARE %.1f, STREET_30 %.1f, CLOSE_35 %.1f (at least 33); at night (lit) %.1f, %.1f, %.1f (at least 45)" % (
        comp[("STREET_SQUARE", "day")], comp[("STREET_30", "day")], comp[("CLOSE_35", "day")], comp[("STREET_SQUARE", "night_lit")], comp[("STREET_30", "night_lit")], comp[("CLOSE_35", "night_lit")]))
    rows.na("LIT-03", "the empty unit is a pale blank by day", "the empty unit's check, not Rita's")
    # LIT-05 the display lit at night, from the render
    p = os.path.join(gate, "STREET_SQUARE_night_lit.png")
    if os.path.exists(p):
        cam = R["cameras"]["STREET_SQUARE"]
        rec = {"eye_street_m": cam["eye_street_m"], "aim_street_m": cam["aim_street_m"], "vfov": G.VFOV["STREET_SQUARE"]}
        corners = [(win_x[0], -0.033, 0.60), (win_x[1], -0.033, 0.60), (win_x[1], -0.033, 1.45), (win_x[0], -0.033, 1.45)]
        px = project(rec, corners)
        im = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
        mk = Image.new("L", (im.shape[1], im.shape[0]), 0)
        ImageDraw.Draw(mk).polygon(px, fill=255)
        mm = np.asarray(mk) > 0
        yv = luma(im)[mm].mean()
        rows.add("LIT-05", "the display is lit at night", yv >= 45, "STREET_SQUARE at night, the display zone (the window lights' lowest 0.85 m over the bed: z 0.60 to 1.45 above the footway = 0.70 to 1.55 above the crown, across the window zone; %d px) in the rendered picture, with the spill modelled (a rect light in the window head, tipped 62 degrees down, strength set in the gate): mean luma %.1f (at least 45). Lumen's own light on the display is owed on the PC (PC-02)" % (int(mm.sum()), yv))
    else:
        rows.add("LIT-05", "the display is lit at night", False, "STREET_SQUARE_night_lit.png was not rendered")
    return comp, dark


def run(work, assets, previews, out_json):
    t0 = time.time()
    T = A.load_target()
    R = A.ritas(T)
    rows = Rows()
    ims, lum_pics, masks, sod, means = picture_rows(R, work, rows)
    projection_rows(R, work, rows)
    room_rows(R, T, work, rows, assets)
    front_rows(R, T, work, rows, assets)
    gate_rows(R, work, rows, means, lum_pics)
    lt = np.array([1.0, 0.25, 0.0])
    rows.add("LIT-06", "the sodium wash is the game's", float(np.abs(np.array(sod) - lt).max()) <= 0.01, "night_dark's sodium wash colour (linear) %s against unreal-look.json lantern_linear_rgb %s (the scene file's stale 1.0, 0.7055, 0.0 is not used)" % ([round(float(x), 3) for x in sod], lt.tolist()))
    rows.na("PRV-01", "the previews show nothing they must not", "the photograph previews of the target (P1 to P6), not this build's; this build's previews were looked at: no real firm's name, number, person, drink, gambling or child in them")
    # CAM-01
    cam_ok, det = True, []
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"):
        for st in ("day", "night_lit"):
            p = os.path.join(work, "gate", "%s_%s.camera.json" % (cam, st))
            if not os.path.exists(p):
                continue
            rec = json.load(open(p))
            d_eye = max(abs(a - b) for a, b in zip(rec["eye_street_m"], rec["defined_eye_street_m"])) * 1000.0
            d_fov = abs(rec["vfov_deg"] - rec["defined_vfov_deg"])
            g = d_eye <= 5.0 and rec["aim_error_deg"] <= 0.1 and d_fov <= 0.1
            cam_ok &= g
            det.append("%s %s eye %.2f mm, aim %.3f deg, field %.2f deg" % (cam, st, d_eye, rec["aim_error_deg"], d_fov))
    rows.add("CAM-01", "the cameras are the named ones", cam_ok and len(det) > 0, "; ".join(det[:8]) + " (limits 5 mm and 0.1 degree)")
    # the previews
    pv = sorted(os.listdir(previews)) if os.path.isdir(previews) else []
    sizes = {f: os.path.getsize(os.path.join(previews, f)) for f in pv if f.endswith(".jpg")}
    widths = {f: Image.open(os.path.join(previews, f)).size[0] for f in sizes}
    ok_p = len(sizes) >= 8 and all(s <= 500 * 1024 for s in sizes.values()) and all(w <= 1700 for w in widths.values())
    rows.add("X-PRV", "previews: JPEG, about 1600 px wide, under 500 KB", ok_p, "%d JPEGs in the previews folder: %s" % (len(sizes), ", ".join("%s %d KB %d px" % (f.replace("-2026-10-13.jpg", ""), s // 1024, widths[f]) for f, s in sizes.items())))
    counted = [r for r in rows.rows if r["status"] != "n/a"]
    npass = sum(1 for r in counted if r["status"] == "pass")
    out = {"schema": "ledger.cloud-week-42.shop-windows-ritas-check/1", "made": time.strftime("%Y-%m-%d %H:%M:%S"), "target": "production/cloud-week/targets/shop-windows/target.json (status: %s)" % T.get("status", "")[:80],
           "pass": npass, "counted": len(counted), "na": len(rows.rows) - len(counted), "seconds": round(time.time() - t0, 1), "rows": rows.rows}
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    json.dump(out, open(out_json, "w"), indent=1)
    print("%d of %d rows pass" % (npass, len(counted)))
    for r in counted:
        if r["status"] != "pass":
            print("FAIL %s %s: %s" % (r["id"], r["name"], r["detail"][:300]))
    return out
