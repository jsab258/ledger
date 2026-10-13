"""The gate stage: bake the card for each review camera and state, render, write the review set to the previews. See sw_gate.py for the method.

13 October, batch A: written for any shop (sw_ctx.Ctx): the room pictures are <picture name>_<state>.png, the frames and checks' renders go under the shop's own gate folder, the previews are named
<shop>-<view>-<state>-2026-10-13.jpg (Rita's keep the `-v3` of her third build). A shop that is dark at night (the ironmonger) is also rendered from STREET_SQUARE in night_dark, as an extra review picture.
A shop with no room (Mickey's, whose real room is already walked; the empty unit) is rendered over a stand-in card: a flat dim picture for Mickey's (the real room is owed to the PC), no card for the empty unit.

Try 3 (13 October, from the try 2 reviews): the review pictures are named `...-v3-2026-10-13.jpg` (v1 and v2 stay as the record); the night glass is reflection only; the footway is on the
spill's channel; two strip lights light the display's tiers at night (`strip_w` in gate_lights.json); two more check renders: the front's mask by day (FRN-10's pixel test) and the display
pieces' object-index mask at night from the two close cameras (LIT-08).

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
import sw_ctx  # noqa: E402

DATE = "2026-10-13"
TAG = "-v3"                  # Rita's third build's tag; the other shops' previews carry none
CAMS = ["STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"]
STATES = ["day", "night_lit"]
REVIEW = [("STREET_SQUARE", "day"), ("STREET_SQUARE", "night_lit"), ("CLOSE_35", "day"), ("CLOSE_35", "night_lit")]
HDRI = "/home/user/cache/hdri/bethnal_green_entrance_2k.hdr"
CHECK_RES = (1280, 720)
RES_FRAME = (2560, 1440)
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


def room_picture(ctx, state):
    return os.path.join(ctx.rooms, "%s_%s.png" % (ctx.picture_name, state))


def bake_all(work, log=print, ctx=None, states=None):
    ctx = ctx or sw_ctx.rita()
    R = ctx.R
    rooms = ctx.rooms
    gate = ctx.gate
    states = states or STATES
    os.makedirs(gate, exist_ok=True)
    stats = {}
    for st in states:
        pic = room_picture(ctx, st)
        side_columns(pic, os.path.join(gate, "col_l_%s.png" % st), os.path.join(gate, "col_r_%s.png" % st))
    for cam in CAMS:
        eye = R["cameras"][cam]["eye_street_m"]
        t0 = time.time()
        uvp = os.path.join(gate, "uv_%s.npy" % cam)
        if os.path.exists(uvp):
            uv = np.load(uvp)
        else:
            uv = G.uv_map(eye, ctx=ctx)
            np.save(uvp, uv)
        stats[cam] = {"uv_s": round(time.time() - t0, 1)}
        for st in states:
            if st == "night_dark" and cam != "STREET_SQUARE":
                continue                      # a dark shop's own night picture is one extra view, from STREET_SQUARE
            pic = room_picture(ctx, st)
            out = os.path.join(gate, "card_%s_%s.png" % (cam, st))
            _, lin_img = G.bake_card(eye, pic, G.BRIGHTNESS[st], out, uv=uv, ctx=ctx)
            stats[cam][st] = {"card": out}
        log("baked %s in %.0f s" % (cam, time.time() - t0))
    json.dump(stats, open(os.path.join(gate, "bake_stats.json"), "w"), indent=1)
    return stats


def standin_card_pictures(ctx, log=print):
    """Mickey's (front only; its real room is already built and walked): the card behind the glass is a flat dim picture, so that the gate shows the front and its glass over something and no more. The
    three states' pictures are one dim warm grey (day 118, night_lit 80, night_dark 18: the means the approved rooms' pictures are held to); they are written to the shop's rooms folder as
    <picture name>_<state>.png at 4096 x 1855 and are NOT a room: the real one is owed to the PC."""
    os.makedirs(ctx.rooms, exist_ok=True)
    out = {}
    for st, v in (("day", 118), ("night_lit", 80), ("night_dark", 18)):
        p = room_picture(ctx, st)
        Image.fromarray(np.full((1855, 4096, 3), (v, int(v * 0.93), int(v * 0.82)), np.uint8)).save(p)
        out[st] = p
    return out


def run(work, assets, previews, samples, views=None, log=print, check_renders=True, ctx=None):
    ctx = ctx or sw_ctx.rita()
    R = ctx.R
    gate = ctx.gate
    os.makedirs(gate, exist_ok=True)
    os.makedirs(previews, exist_ok=True)
    tag = TAG if ctx.id == "ritas" else ""
    states = list(STATES)
    stats = bake_all(work, log, ctx=ctx, states=states + (["night_dark"] if not ctx.lit else []))
    front = os.path.join(assets, ctx.front_glb)
    disp = os.path.join(assets, ctx.display_glb)
    grille = os.path.join(assets, ctx.grille_glb) if ctx.has_grille else None
    lp = os.path.join(gate, "gate_lights.json")
    if not os.path.exists(lp):
        json.dump({"lamp_w": 50000, "spill_w": 175, "strip_w": 0.0}, open(lp, "w"))      # Blender watts, set by eye (see NOTES.md)
    extra = json.load(open(lp))

    def cols(st):
        return {"l": os.path.join(gate, "col_l_%s.png" % st), "r": os.path.join(gate, "col_r_%s.png" % st)}
    times = {}
    todo = views or [(c, s) for c in CAMS for s in states]
    if not ctx.lit and not views:
        todo = todo + [("STREET_SQUARE", "night_dark")]            # a shop that is dark at night: the street's own night picture, one view, as an extra
    for cam, st in todo:
        out = os.path.join(gate, "%s_%s.png" % (cam, st))
        t = G.render_view(cam, R["cameras"][cam], st, os.path.join(gate, "card_%s_%s.png" % (cam, st)), out, front, grille, disp, HDRI, samples=samples, extra=extra, column_pngs=cols(st), ctx=ctx)
        times["%s_%s" % (cam, st)] = t
        log("render %s %s: %.0f s" % (cam, st, t))
        json.dump(times, open(os.path.join(gate, "render_times.json"), "w"), indent=1)
    if check_renders:
        # the checks' own renders: LIT-02 on the rendered frames with the glass's reflection off, and the glass mask (the window's glass pixels without frame, mullions, beads, lattice)
        for cam in CAMS:
            for st in states:
                card = os.path.join(gate, "card_%s_%s.png" % (cam, st))
                t = G.render_view(cam, R["cameras"][cam], st, card, os.path.join(gate, "check_%s_%s_norefl.png" % (cam, st)), front, grille, disp, HDRI,
                                  samples=CHECK_SAMPLES, extra=extra, res=CHECK_RES, glass_refl=0.0, column_pngs=cols(st), ctx=ctx)
                times["check_%s_%s_norefl" % (cam, st)] = t
                if st != "day":
                    # GLS-03: the same frame (same size, same samples, same seed) with the glass's reflection off, so that the difference is the glass and nothing else
                    t = G.render_view(cam, R["cameras"][cam], st, card, os.path.join(gate, "check_%s_%s_norefl_full.png" % (cam, st)), front, grille, disp, HDRI,
                                      samples=samples, extra=extra, res=RES_FRAME, glass_refl=0.0, column_pngs=cols(st), ctx=ctx)
                    times["check_%s_%s_norefl_full" % (cam, st)] = t
                t = G.render_view(cam, R["cameras"][cam], st, card, os.path.join(gate, "check_%s_%s_mask.png" % (cam, st)), front, grille, disp, HDRI,
                                  samples=1, extra=extra, res=CHECK_RES, mode="mask_glass", column_pngs=cols(st), ctx=ctx)
                times["check_%s_%s_mask" % (cam, st)] = t
                t = G.render_view(cam, R["cameras"][cam], st, card, os.path.join(gate, "check_%s_%s_room.png" % (cam, st)), front, grille, disp, HDRI,
                                  samples=1, extra=extra, res=CHECK_RES, mode="mask_room", column_pngs=cols(st), ctx=ctx)
                if st != "day":
                    if grille:
                        t = G.render_view(cam, R["cameras"][cam], st, card, os.path.join(gate, "check_%s_%s_maskopen.png" % (cam, st)), front, grille, disp, HDRI,
                                          samples=1, extra=extra, res=CHECK_RES, mode="mask_glass_open", column_pngs=cols(st), ctx=ctx)
                else:
                    # FRN-10's pixel test: the front's opaque parts, white, at the frames' own size
                    G.render_view(cam, R["cameras"][cam], st, card, os.path.join(gate, "check_%s_%s_frontmask.png" % (cam, st)), front, grille, disp, HDRI,
                                  samples=1, extra=extra, res=RES_FRAME, mode="mask_front", column_pngs=cols(st), ctx=ctx)
                if st != "day" and cam in ("CLOSE_35", "CLOSE_35_B"):
                    # LIT-08: one colour a display piece, the room white, the lattice drawn (black)
                    di = json.load(open(os.path.join(ctx.display_work, "display_items.json")))
                    groups = {nm: gi for gi, g in enumerate(di["groups"]) for nm in g["objs"]}
                    G.render_view(cam, R["cameras"][cam], st, card, os.path.join(gate, "check_%s_%s_pieces.png" % (cam, st)), front, grille, disp, HDRI,
                                  samples=1, extra=extra, res=RES_FRAME, mode="mask_pieces", column_pngs=cols(st), groups=groups, ctx=ctx)
                log("check renders %s %s done" % (cam, st))
        json.dump(times, open(os.path.join(gate, "render_times.json"), "w"), indent=1)
    # the review set: STREET_SQUARE and CLOSE_35, day and night_lit
    for cam, st in REVIEW:
        p = os.path.join(gate, "%s_%s.png" % (cam, st))
        if os.path.exists(p):
            nm = "%s-%s-%s%s-%s.jpg" % (ctx.id, cam.lower().replace("_", "-"), st.replace("_", "-"), tag, DATE)
            jpeg_under(Image.open(p), os.path.join(previews, nm))
    if not ctx.lit:
        p = os.path.join(gate, "STREET_SQUARE_night_dark.png")
        if os.path.exists(p):
            jpeg_under(Image.open(p), os.path.join(previews, "%s-street-square-night-dark%s-%s.jpg" % (ctx.id, tag, DATE)))
    # the three pictures reduced, and (Rita's only: an approved room exists) the before-and-after for Jafar
    for st in ("day", "night_lit", "night_dark"):
        p = room_picture(ctx, st)
        if os.path.exists(p):
            jpeg_under(Image.open(p), os.path.join(previews, "%s-room-%s%s-%s.jpg" % (ctx.id, st.replace("_", "-"), tag, DATE)))
    new = room_picture(ctx, "day")
    old = os.path.join(A.REPO, "production", "art", "shop-rooms", "pawnbroker_day.png") if ctx.id == "ritas" else None
    if old and os.path.exists(new) and os.path.exists(old):
        a = Image.open(old).convert("RGB").resize((1400, 634), Image.LANCZOS)
        b = Image.open(new).convert("RGB").resize((1400, 634), Image.LANCZOS)
        sheet = Image.new("RGB", (1400, 634 * 2 + 12), (20, 20, 20))
        sheet.paste(a, (0, 0))
        sheet.paste(b, (0, 634 + 12))
        jpeg_under(sheet, os.path.join(previews, "ritas-room-before-after%s-%s.jpg" % (tag, DATE)), width=1400)
    return times
