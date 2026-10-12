"""The gate stage: bake the card for each review camera and state, render, write the review set to the previews. See sw_gate.py for the method."""
import json
import os
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sw_assets as A  # noqa: E402
import sw_gate as G  # noqa: E402

DATE = "2026-10-13"
CAMS = ["STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"]
STATES = ["day", "night_lit"]
REVIEW = [("STREET_SQUARE", "day"), ("STREET_SQUARE", "night_lit"), ("CLOSE_35", "day"), ("CLOSE_35", "night_lit")]
HDRI = "/home/user/cache/hdri/bethnal_green_entrance_2k.hdr"


def jpeg_under(im, path, kb=480, width=1600):
    im = im.convert("RGB")
    if im.width > width:
        im = im.resize((width, int(round(im.height * width / im.width))), Image.LANCZOS)
    q = 90
    while q >= 40:
        im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(path) <= kb * 1024:
            break
        q -= 5
    return os.path.getsize(path)


def bake_all(work, log=print):
    T = A.load_target()
    R = A.ritas(T)
    rooms = os.path.join(work, "rooms")
    gate = os.path.join(work, "gate")
    os.makedirs(gate, exist_ok=True)
    stats = {}
    for cam in CAMS:
        eye = R["cameras"][cam]["eye_street_m"]
        t0 = time.time()
        uvp = os.path.join(gate, "uv_%s.npy" % cam)
        if os.path.exists(uvp):
            uv = np.load(uvp)
        else:
            uv = G.uv_map(eye)
            np.save(uvp, uv)
        stats[cam] = {"uv_s": round(time.time() - t0, 1)}
        for st in STATES:
            pic = os.path.join(rooms, "pawnbroker_%s.png" % st)
            out = os.path.join(gate, "card_%s_%s.png" % (cam, st))
            _, lin_img = G.bake_card(eye, pic, G.BRIGHTNESS[st], out, uv=uv)
            stats[cam][st] = {"card": out}
        log("baked %s in %.0f s" % (cam, time.time() - t0))
    json.dump(stats, open(os.path.join(gate, "bake_stats.json"), "w"), indent=1)
    return stats


def run(work, assets, previews, samples, views=None, log=print):
    T = A.load_target()
    R = A.ritas(T)
    gate = os.path.join(work, "gate")
    os.makedirs(gate, exist_ok=True)
    os.makedirs(previews, exist_ok=True)
    stats = bake_all(work, log)
    front = os.path.join(assets, "ritas_front.glb")
    disp = os.path.join(assets, "ritas_display.glb")
    grille = os.path.join(assets, "ritas_grille_night.glb")
    extra = json.load(open(os.path.join(gate, "gate_lights.json"))) if os.path.exists(os.path.join(gate, "gate_lights.json")) else {}
    times = {}
    todo = views or [(c, s) for c in CAMS for s in STATES]
    for cam, st in todo:
        out = os.path.join(gate, "%s_%s.png" % (cam, st))
        t = G.render_view(cam, R["cameras"][cam], st, os.path.join(gate, "card_%s_%s.png" % (cam, st)), out, front, grille, disp, HDRI, samples=samples, extra=extra)
        times["%s_%s" % (cam, st)] = t
        log("render %s %s: %.0f s" % (cam, st, t))
        json.dump(times, open(os.path.join(gate, "render_times.json"), "w"), indent=1)
    # the review set: STREET_SQUARE and CLOSE_35, day and night_lit
    for cam, st in REVIEW:
        p = os.path.join(gate, "%s_%s.png" % (cam, st))
        if os.path.exists(p):
            nm = "ritas-%s-%s-%s.jpg" % (cam.lower().replace("_", "-"), st.replace("_", "-"), DATE)
            jpeg_under(Image.open(p), os.path.join(previews, nm))
    # the three pictures reduced, and the before-and-after for Jafar (the approved day picture beside the new one)
    rooms = os.path.join(work, "rooms")
    for st in ("day", "night_lit", "night_dark"):
        p = os.path.join(rooms, "pawnbroker_%s.png" % st)
        if os.path.exists(p):
            jpeg_under(Image.open(p), os.path.join(previews, "ritas-room-%s-%s.jpg" % (st.replace("_", "-"), DATE)))
    new = os.path.join(rooms, "pawnbroker_day.png")
    old = os.path.join(A.REPO, "production", "art", "shop-rooms", "pawnbroker_day.png")
    if os.path.exists(new) and os.path.exists(old):
        a = Image.open(old).convert("RGB").resize((1400, 634), Image.LANCZOS)
        b = Image.open(new).convert("RGB").resize((1400, 634), Image.LANCZOS)
        sheet = Image.new("RGB", (1400, 634 * 2 + 12), (20, 20, 20))
        sheet.paste(a, (0, 0))
        sheet.paste(b, (0, 634 + 12))
        jpeg_under(sheet, os.path.join(previews, "ritas-room-before-after-%s.jpg" % DATE), width=1400)
    return times
