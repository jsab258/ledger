"""The gate stage: bake the card for each review camera and state, render, write the review set to the previews. See sw_gate.py for the method.

Try 2 (13 October): the review pictures are named `...-v2-2026-10-13.jpg` (the try 1 files stay as the record); the room picture's side-wall front columns are baked for the gate's
reveals and the display's return walls; and the checks' own renders are made here (a no-reflection beauty and a glass mask for every camera and state, at 1280 x 720)."""
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
TAG = "-v2"
CAMS = ["STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"]
STATES = ["day", "night_lit"]
REVIEW = [("STREET_SQUARE", "day"), ("STREET_SQUARE", "night_lit"), ("CLOSE_35", "day"), ("CLOSE_35", "night_lit")]
HDRI = "/home/user/cache/hdri/bethnal_green_entrance_2k.hdr"
CHECK_RES = (1280, 720)
CHECK_SAMPLES = 16


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


def side_columns(picture_png, out_l, out_r, w=8):
    """The room picture's own side-wall front columns (u 0 to 8 px for the left wall, 4088 to 4096 for the right), one value a row, as 16-px-wide 8-bit sRGB strips: the gate's reveals
    and the display's return walls take them as emission at the same height (close review fault 3: the wall meets the card without a step)."""
    a = np.asarray(Image.open(picture_png).convert("RGB")).astype(np.float32)
    for sl, path in ((slice(0, w), out_l), (slice(a.shape[1] - w, a.shape[1]), out_r)):
        col = a[:, sl, :].mean(axis=1)                      # (rows, 3) in sRGB levels
        strip = np.repeat(col[:, None, :], 16, axis=1)
        Image.fromarray(np.clip(strip + 0.5, 0, 255).astype(np.uint8)).save(path)


def bake_all(work, log=print):
    T = A.load_target()
    R = A.ritas(T)
    rooms = os.path.join(work, "rooms")
    gate = os.path.join(work, "gate")
    os.makedirs(gate, exist_ok=True)
    stats = {}
    for st in STATES:
        pic = os.path.join(rooms, "pawnbroker_%s.png" % st)
        side_columns(pic, os.path.join(gate, "col_l_%s.png" % st), os.path.join(gate, "col_r_%s.png" % st))
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


def run(work, assets, previews, samples, views=None, log=print, check_renders=True):
    T = A.load_target()
    R = A.ritas(T)
    gate = os.path.join(work, "gate")
    os.makedirs(gate, exist_ok=True)
    os.makedirs(previews, exist_ok=True)
    stats = bake_all(work, log)
    front = os.path.join(assets, "ritas_front.glb")
    disp = os.path.join(assets, "ritas_display.glb")
    grille = os.path.join(assets, "ritas_grille_night.glb")
    lp = os.path.join(gate, "gate_lights.json")
    if not os.path.exists(lp):
        json.dump({"lamp_w": 50000, "spill_w": 175}, open(lp, "w"))      # Blender watts, set by eye (see NOTES.md)
    extra = json.load(open(lp))

    def cols(st):
        return {"l": os.path.join(gate, "col_l_%s.png" % st), "r": os.path.join(gate, "col_r_%s.png" % st)}
    times = {}
    todo = views or [(c, s) for c in CAMS for s in STATES]
    for cam, st in todo:
        out = os.path.join(gate, "%s_%s.png" % (cam, st))
        t = G.render_view(cam, R["cameras"][cam], st, os.path.join(gate, "card_%s_%s.png" % (cam, st)), out, front, grille, disp, HDRI, samples=samples, extra=extra, column_pngs=cols(st))
        times["%s_%s" % (cam, st)] = t
        log("render %s %s: %.0f s" % (cam, st, t))
        json.dump(times, open(os.path.join(gate, "render_times.json"), "w"), indent=1)
    if check_renders:
        # the checks' own renders: LIT-02 on the rendered frames with the glass's reflection off, and the glass mask (the window's glass pixels without frame, mullions, beads, lattice)
        for cam in CAMS:
            for st in STATES:
                t = G.render_view(cam, R["cameras"][cam], st, os.path.join(gate, "card_%s_%s.png" % (cam, st)), os.path.join(gate, "check_%s_%s_norefl.png" % (cam, st)), front, grille, disp, HDRI,
                                  samples=CHECK_SAMPLES, extra=extra, res=CHECK_RES, glass_refl=0.0, column_pngs=cols(st))
                times["check_%s_%s_norefl" % (cam, st)] = t
                t = G.render_view(cam, R["cameras"][cam], st, os.path.join(gate, "card_%s_%s.png" % (cam, st)), os.path.join(gate, "check_%s_%s_mask.png" % (cam, st)), front, grille, disp, HDRI,
                                  samples=1, extra=extra, res=CHECK_RES, mode="mask_glass", column_pngs=cols(st))
                times["check_%s_%s_mask" % (cam, st)] = t
                if st != "day":
                    t = G.render_view(cam, R["cameras"][cam], st, os.path.join(gate, "card_%s_%s.png" % (cam, st)), os.path.join(gate, "check_%s_%s_maskopen.png" % (cam, st)), front, grille, disp, HDRI,
                                      samples=1, extra=extra, res=CHECK_RES, mode="mask_glass_open", column_pngs=cols(st))
                log("check renders %s %s done" % (cam, st))
        json.dump(times, open(os.path.join(gate, "render_times.json"), "w"), indent=1)
    # the review set: STREET_SQUARE and CLOSE_35, day and night_lit
    for cam, st in REVIEW:
        p = os.path.join(gate, "%s_%s.png" % (cam, st))
        if os.path.exists(p):
            nm = "ritas-%s-%s%s-%s.jpg" % (cam.lower().replace("_", "-"), st.replace("_", "-"), TAG, DATE)
            jpeg_under(Image.open(p), os.path.join(previews, nm))
    # the three pictures reduced, and the before-and-after for Jafar (the approved day picture beside the new one)
    rooms = os.path.join(work, "rooms")
    for st in ("day", "night_lit", "night_dark"):
        p = os.path.join(rooms, "pawnbroker_%s.png" % st)
        if os.path.exists(p):
            jpeg_under(Image.open(p), os.path.join(previews, "ritas-room-%s%s-%s.jpg" % (st.replace("_", "-"), TAG, DATE)))
    new = os.path.join(rooms, "pawnbroker_day.png")
    old = os.path.join(A.REPO, "production", "art", "shop-rooms", "pawnbroker_day.png")
    if os.path.exists(new) and os.path.exists(old):
        a = Image.open(old).convert("RGB").resize((1400, 634), Image.LANCZOS)
        b = Image.open(new).convert("RGB").resize((1400, 634), Image.LANCZOS)
        sheet = Image.new("RGB", (1400, 634 * 2 + 12), (20, 20, 20))
        sheet.paste(a, (0, 0))
        sheet.paste(b, (0, 634 + 12))
        jpeg_under(sheet, os.path.join(previews, "ritas-room-before-after%s-%s.jpg" % (TAG, DATE)), width=1400)
    return times
