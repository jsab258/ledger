"""The ten fascia boards (unit 4.1, cloud week 42): every board is drawn from target.json (amended) and a seed.

render_fascia(T, shop, seed) -> (Board, info). `info` holds what the manifest and the checks need: the blocks as drawn (ink boxes read
off the drawn alphas), the wear layers, the ghost record, the emissive planes, the geometry rows. Nothing is invented: every size, colour,
position, count and font is the target's. What the target leaves to the builder is marked JUDGEMENT in a comment and listed in NOTES.md.
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import fascia_common as fc
import fascia_paint as fp
import fascia_wear as fw
from fascia_common import H_MM, W_MM

LINE_ROLES = {"rule", "rule_outer", "rule_inner", "corner_block", "keyline", "rope", "speed_line", "slab_joint", "slab_edge", "box_frame", "vinyl_panel"}
CONTAINER_ROLES = {"old_board", "box_face", "slab_face"}


# ------------------------------------------------------------------ small drawing helpers
def wobbly_rect_alpha(B, win, x0, y0, x1, y1, amp=0.35, rng=None):
    """a hand-painted band: the two long edges wander by a fraction of a millimetre"""
    r0, r1, c0, c1 = win
    cols = np.arange(c0, c1, dtype=np.float32)
    ys_top = H_MM - np.arange(r0, r1, dtype=np.float32)
    n1 = fc.fnoise((1, c1 - c0 + 8), 40.0, 0.01, rng)[0, :c1 - c0] * amp
    n2 = fc.fnoise((1, c1 - c0 + 8), 40.0, 0.01, rng)[0, :c1 - c0] * amp
    cx = np.clip(np.minimum(cols + 1, x1) - np.maximum(cols, x0), 0, 1)
    top = (y1 + n1)[None, :]
    bot = (y0 + n2)[None, :]
    cy = np.clip(np.minimum(ys_top[:, None], top) - np.maximum(ys_top[:, None] - 1, bot), 0, 1)
    return cy * cx[None, :]


def rope_alpha_and_pattern(win, pts, width, pitch, H=H_MM):
    """a laid rope along a polyline: the outline alpha and a twist pattern (-1..1) across it"""
    r0, r1, c0, c1 = win
    a = fp.poly_alpha(win, pts, width, H=H)
    S = fp.SS
    img = Image.new("L", ((c1 - c0) * S, (r1 - r0) * S), 128)
    d = ImageDraw.Draw(img)
    P = np.array([((x - c0) * S, (H - y - r0) * S) for x, y in pts])
    seg = np.diff(P, axis=0)
    lens = np.hypot(seg[:, 0], seg[:, 1])
    cum = np.concatenate([[0], np.cumsum(lens)])
    total = cum[-1]
    step = pitch * S / 2.0
    n = int(total / step)
    for k in range(n):
        s = k * step + step / 2
        i = int(np.searchsorted(cum, s) - 1)
        i = max(0, min(i, len(seg) - 1))
        t = (s - cum[i]) / max(lens[i], 1e-6)
        p = P[i] + seg[i] * t
        u = seg[i] / max(lens[i], 1e-6)
        nrm = np.array([-u[1], u[0]])
        half = width * S / 2.0
        shade_ = 40 if k % 2 == 0 else 215
        a_ = p - nrm * half - u * pitch * S * 0.18
        b_ = p + nrm * half + u * pitch * S * 0.18
        d.line([tuple(a_), tuple(b_)], fill=shade_, width=int(pitch * S * 0.34))
    pat = (np.asarray(img.resize((c1 - c0, r1 - r0), Image.BOX), np.float32) - 128.0) / 128.0
    return a, pat


def lab_shift(rgb, dL, da, db):
    L = fc.lab(np.asarray(rgb, float))
    return np.clip(fc.unlab(L + np.array([dL, da, db], float)), 0, 255)


def dilate_box(mask, box_mm, pad, H=H_MM, W=W_MM):
    x0, y0, x1, y1 = box_mm
    c0, c1 = max(0, int(x0 - pad)), min(W, int(x1 + pad) + 1)
    r0, r1 = max(0, H - int(y1 + pad) - 1), min(H, H - int(y0 - pad))
    mask[r0:r1, c0:c1] = True


def is_light(rgb):
    return float(fc.lab(np.asarray(rgb, float))[0]) >= 48.0


# ------------------------------------------------------------------ the ground
def paint_ground_fill(B, s, colour, grain, rough, amp_override=None):
    T = B.T
    win = (0, H_MM, 0, W_MM)
    amp = amp_override if amp_override is not None else grain.get("amp_L", 1.2)
    if grain.get("direction") == "along":
        kinds = (("streak", 0.38), ("grain", 0.45), ("blot", 0.65), ("iso", 0.3), ("fine", 0.22))
    else:
        kinds = (("blot", 0.55), ("iso", 0.4), ("fine", 0.25))
    rgb = B.mottle(win, colour, amp, kinds=kinds)
    B.rgb[:] = rgb
    rn = B.noise("blot") * 0.03 + B.noise("fine") * 0.012
    B.rough[:] = np.clip(rough + rn, 0.02, 1.0)
    B.metal[:] = 0.0
    B.height[:] = (B.noise("streak") * 0.012 + B.noise("fine") * 0.006).astype(np.float32) if grain.get("direction") == "along" else (B.noise("fine") * 0.004).astype(np.float32)


def grime(B, s):
    """a grime film heavier along the top and bottom edges (the soot under the cornice, the road spray), zero-mean on the board, so the ground's
    aged median (the target's palette, which already holds the grime film) is kept"""
    age = s["age"]
    rows = np.arange(H_MM, dtype=np.float32)
    d_top, d_bot = rows, H_MM - 1 - rows
    prof = np.exp(-d_bot / 70.0) * 1.0 + np.exp(-d_top / 45.0) * 0.8
    prof = prof - prof.mean()
    delta = (age["grime_film"] * 0.9) * prof[:, None]                       # +: toward grime
    tint = np.where(delta[..., None] > 0, GRIME_BLEND_DARK, GRIME_BLEND_LIGHT)
    B.rgb += (tint - B.rgb) * delta[..., None] * 0.5


def chalk(B, s):
    """the chalk bloom of old gloss (each shop's `chalk_dL`): L* lifted in patches over EVERYTHING on the surface, zero-mean on the board"""
    age = s["age"]
    if not age.get("chalk_dL"):
        return
    lift = np.clip(B.noise("blot") * 0.5 + 0.35, 0, 1.2) * age["chalk_dL"]
    lift = lift - float(lift.mean())
    luma = (0.2126 * B.rgb[..., 0] + 0.7152 * B.rgb[..., 1] + 0.0722 * B.rgb[..., 2]) / 255.0
    L_approx = 100.0 * np.power(np.maximum(luma, 1e-4), 0.45)
    B.rgb *= (1.0 + 1.36 * lift / np.maximum(L_approx, 15.0))[..., None]
    np.clip(B.rgb, 0, 255, out=B.rgb)


GRIME_BLEND_DARK = np.array([88.0, 82.0, 74.0], np.float32)
GRIME_BLEND_LIGHT = np.array([200.0, 198.0, 190.0], np.float32)


# ------------------------------------------------------------------ the board
def render_fascia(T, s, seed, wrong_font=None, with_text=True):
    B = fp.Board(T, s, seed)
    info = dict(shop=s["id"], seed=int(seed), blocks=[], ghosts=[], wear={}, geometry=[], notes=[])
    sid = s["id"]
    kind = s["construction_kind"]
    shapes = s["shapes"]
    roles = [sh["role"] for sh in shapes]
    g = s["ground"]
    gcol = fc.pal(T, g["colour"])

    # ---- 0. what the whole board is under everything
    if "old_board" in roles:
        ob = [sh for sh in shapes if sh["role"] == "old_board"][0]
        paint_ground_fill(B, s, fc.pal(T, ob["colour"]), dict(direction="along", amp_L=1.6, scale_mm=[30, 300]), 0.65)
    elif "slab_edge" in roles:
        paint_ground_fill(B, s, fc.pal(T, "mastic"), dict(direction="along", amp_L=1.0, scale_mm=[40, 400]), 0.55, amp_override=1.0)
    else:
        paint_ground_fill(B, s, gcol, g["grain"], g["roughness"])
    B.metal[:] = g.get("metallic", 0.0) if not ("old_board" in roles or "slab_edge" in roles) else 0.0
    grime(B, s)

    # ---- 1. the shapes, in the target's order
    shape_alpha = np.zeros((H_MM, W_MM), np.float32)          # lines and frames (for the free-zone maths)
    hand_kind = kind in ("signwritten", "gilded")
    srng = B.rng("shapes")
    for sh in shapes:
        role = sh["role"]
        if role == "old_board":
            continue
        col = fc.pal(T, sh["colour"])
        if sh["kind"] == "rect":
            x0, y0, x1, y1 = sh["box"]
            win = B.win(x0, y0, x1, y1, pad=2)
            if role in ("rule",) and hand_kind:
                a = wobbly_rect_alpha(B, win, x0, y0, x1, y1, amp=0.35, rng=srng)
            else:
                a = fp.rect_alpha(win, x0, y0, x1, y1)
            rgb_i, rough, metal, hgt = col, 0.5, 0.0, 0.0
            if role == "box_frame":
                if sh["colour"] == "bronze_anodised":
                    rough, metal = 0.35, 1.0
                elif sh["colour"] == "powder_black":
                    rough, metal = 0.50, 0.0
                else:
                    rough, metal = 0.55, 0.0
                rgb_i = B.mottle(win, col, 1.0, kinds=(("streak", 0.8), ("fine", 0.3)))
            elif role == "box_face":
                rough, metal = 0.35, 0.0
                rgb_i = B.mottle(win, col, 0.9, kinds=(("blot", 0.6), ("iso", 0.4), ("fine", 0.3)))
            elif role == "vinyl_panel":
                rough, metal, hgt = 0.45, 0.0, 0.08
                rgb_i = B.mottle(win, col, 0.5, kinds=(("blot", 0.6), ("fine", 0.3)))
            elif role == "rule":
                if hand_kind:
                    rough, hgt = max(0.35, g["roughness"] - 0.10), 0.20
                    rgb_i = B.mottle(win, col, 1.2, kinds=(("blot", 0.7), ("streak", 0.4), ("fine", 0.3)))
                else:
                    rough, hgt = 0.45, 0.08
                    rgb_i = B.mottle(win, col, 0.4, kinds=(("blot", 0.6), ("fine", 0.3)))
            elif role == "corner_block":
                rough, hgt = 0.45, 0.20
                rgb_i = B.mottle(win, col, 1.0, kinds=(("blot", 0.6), ("fine", 0.3)))
            elif role == "slab_edge":
                rough, metal, hgt = 0.15, 1.0, 0.80
                rgb_i = B.mottle(win, col, 2.0, kinds=(("streak", 0.8), ("fine", 0.6), ("iso", 0.3)))
            elif role == "slab_face":
                rough, metal = 0.08, 0.0
                rgb_i = B.mottle(win, col, 0.8, kinds=(("blot", 0.7), ("iso", 0.4), ("fine", 0.15)))
            elif role == "slab_joint":
                rough, hgt = 0.55, None
                rgb_i = col
            elif role == "speed_line":
                rough, metal, hgt = 0.15, 1.0, 0.80
                rgb_i = B.mottle(win, col, 1.5, kinds=(("streak", 0.8), ("fine", 0.5)))
            if role == "slab_joint":
                B.paint(win, a, rgb_i, rough=rough, metal=0.0, height=-0.50, hmode="set")
            elif role == "slab_face":
                B.paint(win, a, rgb_i, rough=rough, metal=metal, height=0.0, hmode="set")
            else:
                B.paint(win, a, rgb_i, rough=rough, metal=metal, height=hgt)
            if role in LINE_ROLES:
                a_occ = a
                if role in ("box_frame", "slab_edge"):
                    fr_mm = (s["border"].get("frame_mm") if role == "box_frame" else s["border"].get("edge_mm")) or 12
                    a_occ = np.clip(a - fp.rect_alpha(win, x0 + fr_mm, y0 + fr_mm, x1 - fr_mm, y1 - fr_mm), 0, 1)
                if role == "vinyl_panel":
                    a_occ = np.zeros_like(a)
                shape_alpha[win[0]:win[1], win[2]:win[3]] = np.maximum(shape_alpha[win[0]:win[1], win[2]:win[3]], a_occ)
            info.setdefault("shapes_drawn", []).append(dict(role=role, kind="rect", box=[x0, y0, x1, y1], colour=sh["colour"]))
        else:                                              # polyline
            pts = sh["pts"]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            w = sh["width_mm"]
            win = B.win(min(xs) - w, min(ys) - w, max(xs) + w, max(ys) + w, pad=3)
            if role == "rope":
                a, pat = rope_alpha_and_pattern(win, pts, w, sh["twist_pitch_mm"])
                base = B.mottle(win, col, 1.4, kinds=(("fine", 0.6), ("blot", 0.4)))
                rgb_i = np.clip(base * (1.0 + 0.16 * pat[..., None]), 0, 255)
                B.paint(win, a, rgb_i, rough=0.80, metal=0.0, height=0.15)
            elif role == "keyline":
                a = fp.poly_alpha(win, pts, w)
                rgb_i = B.mottle(win, col, 2.0, kinds=(("blot", 0.7), ("fine", 0.4), ("iso", 0.4)))
                B.paint(win, a, rgb_i, rough=0.30, metal=1.0, height=0.15)
            else:                                           # rule_outer, rule_inner: sign-written lines
                a = fp.poly_alpha(win, pts, w)
                rgb_i = B.mottle(win, col, 1.0, kinds=(("blot", 0.7), ("fine", 0.3)))
                B.paint(win, a, rgb_i, rough=max(0.35, g["roughness"] - 0.10), metal=0.0, height=0.15 if role == "rule_inner" else 0.20)
            shape_alpha[win[0]:win[1], win[2]:win[3]] = np.maximum(shape_alpha[win[0]:win[1], win[2]:win[3]], a)
            info.setdefault("shapes_drawn", []).append(dict(role=role, kind="polyline", n=len(pts), width=w, colour=sh["colour"]))

    # glass slabs: a 2 mm polished bevel round every slab edge (the target: a ramp to -0.30 mm)
    if "slab_face" in roles:
        sf = [sh for sh in shapes if sh["role"] == "slab_face"][0]["box"]
        joints = [sh["box"] for sh in shapes if sh["role"] == "slab_joint"]
        xs = [sf[0]] + sorted([j[2] for j in joints]) + []
        slab_edges = []
        cuts = sorted([sf[0], sf[2]] + [j[0] for j in joints] + [j[2] for j in joints])
        spans = [(cuts[0], cuts[1]), (cuts[2], cuts[3]), (cuts[4], cuts[5])]
        for (xa, xb) in spans:
            slab_edges.append((xa, sf[1], xb, sf[3]))
        bev = np.zeros((H_MM, W_MM), np.float32)
        for (xa, ya, xb, yb) in slab_edges:
            win = B.win(xa, ya, xb, yb, pad=0)
            r0, r1, c0, c1 = win
            cols = np.arange(c0, c1, dtype=np.float32) + 0.5
            rws = H_MM - (np.arange(r0, r1, dtype=np.float32) + 0.5)
            dxe = np.minimum(cols - xa, xb - cols)[None, :]
            dye = np.minimum(rws - ya, yb - rws)[:, None]
            de = np.minimum(dxe + 0 * dye, dye + 0 * dxe)
            ramp = np.clip(1.0 - de / 2.0, 0, 1)
            B.height[r0:r1, c0:c1] += (-0.30 * ramp).astype(np.float32)
            B.rough[r0:r1, c0:c1] = np.where(ramp > 0, 0.05, B.rough[r0:r1, c0:c1])
    info["shape_alpha_sum"] = float(shape_alpha.sum())

    # ---- 2. ghosts
    blocks = s["blocks"]
    blocked = np.zeros((H_MM, W_MM), bool)
    for b in blocks:
        if b["in_texture"] or b["ghost"]:
            dilate_box(blocked, b["effects_box_mm"], 12)
    blocked |= ndi.binary_dilation(shape_alpha > 0.03, iterations=6)
    loss_block = np.zeros((H_MM, W_MM), bool)
    gh = s.get("ghost")
    grng = B.rng("ghost")
    hole_pts = []
    if gh and gh["kind"] == "older_lettering":
        gb = [b for b in blocks if b["ghost"]][0]
        face, _, win = fp.text_layers(T, gb, None, hand=False, shade=False)
        share = gb["broken_fraction"]
        # the part of the old lettering still in view: not under the newer letters or their shade (the same draws the painter will make)
        r0v, r1v, c0v, c1v = win
        under = np.zeros(face.shape, bool)
        for ob in blocks:
            if ob["ghost"] or not ob["in_texture"]:
                continue
            ox0, oy0, ox1, oy1 = ob["effects_box_mm"]
            if ox1 < c0v or ox0 > c1v or H_MM - oy1 > r1v or H_MM - oy0 < r0v:
                continue
            f_o, s_o, w_o = fp.text_layers(T, ob, B.rng("block", ob["id"]), hand=True)
            u = np.zeros(face.shape, bool)
            ra, rb, ca, cb = w_o
            rr0, rr1 = max(ra, r0v), min(rb, r1v)
            cc0, cc1 = max(ca, c0v), min(cb, c1v)
            if rr1 > rr0 and cc1 > cc0:
                m_o = (f_o > 0.3) | ((s_o if s_o is not None else 0) > 0.3)
                u[rr0 - r0v:rr1 - r0v, cc0 - c0v:cc1 - c0v] = m_o[rr0 - ra:rr1 - ra, cc0 - ca:cc1 - ca]
            under |= ndi.binary_dilation(u, iterations=2)
        visible = np.where(under, 0.0, face)
        rep = fp.repaint_mask(B, win, visible, share, grng) if share > 0 else np.zeros_like(face)
        info["ghost_visible_px"] = int((visible > 0.5).sum())
        a = face * (1.0 - rep)
        gcol_rgb = np.array(gb["face_rgb"], np.float32)
        wcol = B.mottle(win, gcol_rgb, 0.5, kinds=(("blot", 0.7), ("fine", 0.3)))
        B.paint(win, a, wcol, rough=max(0.3, g["roughness"] - 0.05))
        m = face > 0.5
        ridge = (m & ~ndi.binary_erosion(m, iterations=1)) & (rep < 0.5)
        r0, r1, c0, c1 = win
        B.height[r0:r1, c0:c1] += 0.10 * ndi.gaussian_filter(ridge.astype(np.float32), 0.5)
        # the repaint's own brush edge shows as a faint ridge
        rm = rep > 0.5
        redge = rm & ~ndi.binary_erosion(rm, iterations=1) & (face > 0.3)
        B.height[r0:r1, c0:c1] += 0.06 * redge
        info["ghosts"].append(dict(id=gb["id"], string=gb["text"], font=gb["font"], cap_mm=gb["cap_mm"], baseline_mm=gb["baseline_mm"],
                                   centre_x_mm=gb["x_mm"], rgb=gb["face_rgb"], broken_fraction_target=share,
                                   broken_fraction_drawn=round(float(((visible > 0.5) & (rep > 0.5)).sum() / max(1.0, (visible > 0.5).sum())), 3),
                                   pinholes=gh.get("pinholes", 0), win=list(win)))
        if gh.get("pinholes"):
            hole_pts = [tuple(p) for p in gh["pinhole_positions_mm"]]
    elif gh and gh["kind"] == "repaint_patch":
        x0, y0, x1, y1 = gh["box_mm"]
        win = B.win(x0, y0, x1, y1, pad=10)
        a = fp.rect_alpha(win, x0, y0, x1, y1)
        r0, r1, c0, c1 = win
        n = fc.fnoise(a.shape, 3.0, 3.0, grng)
        a = np.clip((ndi.gaussian_filter(a, 1.5) - 0.5) * 5.0 + 0.5 + 0.33 * n, 0, 1)
        pc = lab_shift(gcol, 2.1, -0.7, -2.0)
        d0 = float(fc.dE(pc, gcol))
        pc = lab_shift(gcol, 2.1 * gh["dE"] / d0, -0.7 * gh["dE"] / d0, -2.0 * gh["dE"] / d0)
        brush = fc.fnoise(a.shape, 38.0, 1.0, grng)
        pimg = np.clip(B.rgb[r0:r1, c0:c1] * 0 + pc[None, None, :] * (1.0 + 0.012 * brush[..., None]), 0, 255)
        # the patch keeps the board's grain: it is paint on the same boards
        pimg = np.clip(pimg * (B.rgb[r0:r1, c0:c1] / np.maximum(gcol[None, None, :], 1.0)), 0, 255)
        B.paint(win, a, pimg)
        m = a > 0.5
        ridge = m & ~ndi.binary_erosion(m, iterations=1)
        B.height[r0:r1, c0:c1] += 0.15 * ndi.gaussian_filter(ridge.astype(np.float32), 0.5)
        info["ghosts"].append(dict(id="repaint_patch", string=None, box_mm=gh["box_mm"], dE=gh["dE"], win=list(win)))
        dilate_box(blocked, gh["box_mm"], 6)
    elif gh and gh["kind"] == "painted_out_patch":
        x0, y0, x1, y1 = gh["box_mm"]
        win = B.win(x0, y0, x1, y1, pad=10)
        a = fp.rect_alpha(win, x0, y0, x1, y1)
        r0, r1, c0, c1 = win
        n = fc.fnoise(a.shape, 5.0, 3.0, grng)
        a = np.clip((ndi.gaussian_filter(a, 2.0) - 0.5) * 4.0 + 0.5 + 0.45 * n, 0, 1)
        pcol = fc.pal(T, "painted_out")
        img = B.mottle(win, pcol, 2.6, kinds=(("streak", 0.9), ("grain", 0.5), ("blot", 0.4), ("fine", 0.3)))
        B.paint(win, a, img, rough=0.75, metal=0.0)
        m = a > 0.5
        ridge = m & ~ndi.binary_erosion(m, iterations=1)
        B.height[r0:r1, c0:c1] += 0.40 * ndi.gaussian_filter(ridge.astype(np.float32), 0.6) * (0.5 + 0.5 * np.clip(fc.fnoise(a.shape, 6.0, 6.0, grng), -1, 1))
        info["ghosts"].append(dict(id="painted_out_patch", string=None, box_mm=gh["box_mm"], win=list(win)))
        dilate_box(loss_block, gh["box_mm"], 8)
        # six nail holes, 3 to 4 mm, the heads of the removed lettering's fixings
        n_ = gh["pinholes"]
        tops = [(1450.0, 398.0), (2705.0, 404.0), (3960.0, 396.0)]
        bots = [(1520.0, 152.0), (2812.0, 146.0), (4012.0, 154.0)]
        for (hx, hy) in tops + bots:
            hole_pts.append((float(hx + grng.uniform(-14, 14)), float(hy + grng.uniform(-4, 4))))
        info["nail_heads_top"] = hole_pts[:3]
        # the unit's own free zone is not blocked by the patch (runs and marks may cross buff paint)
    info["blocked_frac"] = float(blocked.mean())

    # ---- 3. paint loss
    loss_frac = s["age"]["loss_fraction"]
    ob_frac = s["age"].get("old_board", {}).get("loss_fraction", 0.0) if "old_board" in s["age"] else 0.0
    free_loss = fw.gather_free(B, blocked.copy(), margin=24) & ~loss_block
    if "box_frame" in roles:
        bf = [sh for sh in shapes if sh["role"] == "box_frame"][0]["box"]
        inside = np.zeros((H_MM, W_MM), bool)
        dilate_box(inside, bf, 8)
        free_loss &= ~inside                          # the ring of old board only
        ring_px = float(free_loss.sum())
        frac = ob_frac * ring_px / float(W_MM * H_MM)
        info["old_board_loss_target"] = ob_frac
    elif "slab_edge" in roles:
        frac = 0.0
    else:
        frac = loss_frac
    if sid == "mickeys":
        for gb in blocks:
            if not gb["in_texture"]:
                dilate_box(blocked, gb["effects_box_mm"], 34)
        free_loss &= ~blocked
        sh_zone = np.zeros((H_MM, W_MM), bool)
        dilate_box(sh_zone, [2996.0, 90.0, 5114.0, 439.0], 34)
        free_loss &= ~sh_zone
    lrng = B.rng("loss")
    # flaking is not even: it gathers where the board is damp (the foot, under the cornice) and in patches
    rr_ = np.arange(H_MM, dtype=np.float32)[:, None]
    bands = fc.fnoise((H_MM, W_MM), 260.0, 16.0, B.rng("lossbands"))          # long damp bands along the board, where the paint lets go
    wgt = np.exp(1.5 * bands + 0.9 * B.noise("blot") + 0.5 * B.noise("iso")) * (0.35 + 1.8 * np.exp(-(H_MM - 1 - rr_) / 60.0) + 0.9 * np.exp(-rr_ / 35.0))
    la, lsub = fp.loss_patches(B, free_loss, frac, lrng, gcol, weight=wgt, gap=(2 if frac < 0.1 else 1), big_prob=(0.022 if frac < 0.1 else 0.09))
    ground_lab = float(fc.lab(gcol)[0])
    if "old_board" in roles:
        ground_lab = float(fc.lab(fc.pal(T, [sh for sh in shapes if sh["role"] == "old_board"][0]["colour"]))[0])
    if sid == "empty_unit":
        prim, wood = np.array([104.0, 92.0, 78.0]), np.array([104.0, 92.0, 78.0])             # the silvered timber under the soot film
    elif ground_lab >= 55:
        prim, wood = np.array([138.0, 134.0, 124.0]), np.array([104.0, 90.0, 76.0])
    else:
        prim, wood = np.array([142.0, 138.0, 130.0]), np.array([116.0, 102.0, 86.0])
    if la.any():
        for code, colr, hgt in ((1, prim, -0.30), (2, wood, -0.50)):
            m = (lsub == code)
            if not m.any():
                continue
            a = la * m
            sel = a > 0.002
            B.rgb[sel] = B.rgb[sel] + (colr[None, :] * (1.0 + 0.035 * B.noise("fine")[sel][:, None] + 0.04 * B.noise("iso")[sel][:, None]) - B.rgb[sel]) * a[sel][:, None]
            B.rough[sel] = B.rough[sel] + (0.85 - B.rough[sel]) * a[sel]
            B.metal[sel] = B.metal[sel] * (1 - a[sel])
            B.height[sel] = B.height[sel] + (hgt - B.height[sel]) * a[sel]
    B.layers["loss"] = la
    B.layers["loss_sub"] = lsub
    info["loss"] = dict(target_fraction=frac, drawn_fraction=round(float((la > 0.5).sum() / (W_MM * H_MM)), 4),
                        substrate_primer=[int(v) for v in prim], substrate_wood=[int(v) for v in wood])

    # ---- 4. the letters
    if with_text:
        for b in blocks:
            if b["ghost"] or not b["in_texture"]:
                continue
            fk = None
            if wrong_font and b["id"] == wrong_font[0]:
                fk = wrong_font[1]
            drawn = fp.paint_block(B, b, ground_rough=g["roughness"], font_key=fk)
            m = drawn["face"] > 0.5
            rows = np.where(m.any(axis=1))[0]
            cols = np.where(m.any(axis=0))[0]
            r0, r1, c0, c1 = drawn["win"]
            if len(rows):
                ink = [float(c0 + cols.min()), float(H_MM - (r0 + rows.max() + 1)), float(c0 + cols.max() + 1), float(H_MM - (r0 + rows.min()))]
            else:
                ink = None
            info["blocks"].append(dict(id=b["id"], string=b["text"], font=b["font"], weight=b["weight"], cap_mm=b["cap_mm"],
                                       size_px_per_em=b["size_px_per_em"], tracking_em=b["tracking_em"], anchor=b["anchor"], x_mm=b["x_mm"],
                                       baseline_mm=b["baseline_mm"], face=b["face"], shade=b.get("shade"), technique=b["technique"],
                                       hand_jitter=bool(b.get("jitter")), ink_box_drawn_mm=ink, role=b["role"]))
    for b in blocks:
        if not b["in_texture"] and not b["ghost"]:
            info["blocks"].append(dict(id=b["id"], string=b["text"], font=b["font"], weight=b["weight"], cap_mm=b["cap_mm"], in_texture=False,
                                       geometry=True, role=b["role"], technique=b["technique"], baseline_mm=b["baseline_mm"], x_mm=b["x_mm"],
                                       ink_box_mm=b["ink_box_mm"]))
    for gd in info["ghosts"]:
        if gd.get("string"):
            gb = [b for b in blocks if b["id"] == gd["id"]][0]
            info["blocks"].append(dict(id=gb["id"], string=gb["text"], font=gb["font"], weight=gb["weight"], cap_mm=gb["cap_mm"], role="ghost",
                                       technique=gb["technique"], baseline_mm=gb["baseline_mm"], x_mm=gb["x_mm"], ink_box_mm=gb["ink_box_mm"]))

    # ---- 5. specials: Mickey's contact shadow, nail and pin holes, the lifting vinyl rule
    if sid == "mickeys":
        geo = s["geometry"][0]
        letters = [b for b in blocks if not b["in_texture"]][0]
        foot, _, wn = fp.text_layers(T, dict(letters, jitter=None), None, hand=False, shade=False, extra_pad=40)
        emb = geo["embolden_m"] * 1000.0
        foot_d = ndi.gaussian_filter(foot, 0.7)
        foot_m = foot > 0.5
        if emb > 0:
            foot_m = ndi.binary_dilation(foot_m, iterations=int(round(emb / 2.0)))
        cs = geo["contact_shadow_in_texture"]
        sh = np.zeros_like(foot)
        sh_src = foot_m.astype(np.float32)
        dx, dy = cs["offset_mm"]
        sh = np.roll(np.roll(sh_src, int(round(dx)), axis=1), int(round(-dy)), axis=0)
        sh = ndi.gaussian_filter(sh, cs["blur_mm"] / 2.0)
        r0, r1, c0, c1 = wn
        k = cs["opacity"] * np.clip(sh, 0, 1)
        shadow_col = np.array([14.0, 18.0, 24.0], np.float32)
        B.rgb[r0:r1, c0:c1] = B.rgb[r0:r1, c0:c1] + (shadow_col[None, None, :] - B.rgb[r0:r1, c0:c1]) * k[..., None]
        info["shadow"] = dict(win=list(wn), opacity=cs["opacity"], blur_mm=cs["blur_mm"], offset_mm=cs["offset_mm"], footprint_px=int(foot_m.sum()))
        B.layers["footprint"] = (wn, foot_m)
    hole_alpha = None
    if hole_pts:
        holes_layer = np.zeros((H_MM, W_MM), np.float32)
        dia = 3.5
        for hx, hy in hole_pts:
            win = B.win(hx - 6, hy - 6, hx + 6, hy + 6)
            a = fp.disc_alpha(win, hx, hy, dia / 2.0)
            B.paint(win, a, np.array([6.0, 6.0, 6.0]), rough=0.9, metal=0.0, height=-0.4, hmode="add")
            r0, r1, c0, c1 = win
            holes_layer[r0:r1, c0:c1] = np.maximum(holes_layer[r0:r1, c0:c1], a)
        B.layers["holes"] = holes_layer
        info["holes"] = [[round(x, 1), round(y, 1)] for x, y in hole_pts]

    # ---- 6. wear: rain runs, gull marks, rust runs
    age = s["age"]
    free = fw.gather_free(B, blocked.copy(), margin=14)
    for b in blocks:
        if b["in_texture"] and not b["ghost"]:
            dilate_box(blocked, b["effects_box_mm"], 14)
    text_only = np.zeros((H_MM, W_MM), bool)
    for b in blocks:
        if b["in_texture"] or b["ghost"]:
            dilate_box(text_only, b["effects_box_mm"], 10)
    wrng = B.rng("wear")
    face_free = free.copy()
    if "box_frame" in roles:
        # the old board's ring takes the runs of a box sign too, and so does the box face: the frame itself does not
        fr = [sh for sh in shapes if sh["role"] == "box_frame"][0]["box"]
        fa = [sh for sh in shapes if sh["role"] == "box_face"][0]["box"]
        ring = np.zeros((H_MM, W_MM), bool)
        dilate_box(ring, fr, 8)
        inner = np.zeros((H_MM, W_MM), bool)
        dilate_box(inner, [fa[0] + 6, fa[1] + 6, fa[2] - 6, fa[3] - 6], 0)
        face_free = free & (inner | ~ring) & ~ndi.binary_dilation(shape_alpha > 0.03, iterations=8)
        # keep the frame band itself out
        band = np.zeros((H_MM, W_MM), bool)
        dilate_box(band, fr, 4)
        inband = np.zeros((H_MM, W_MM), bool)
        dilate_box(inband, [fr[0] + 22, fr[1] + 22, fr[2] - 22, fr[3] - 22], 0)
        face_free &= ~(band & ~inband)
    if "slab_face" in roles:
        sf = [sh for sh in shapes if sh["role"] == "slab_face"][0]["box"]
        inner = np.zeros((H_MM, W_MM), bool)
        dilate_box(inner, [sf[0] + 8, sf[1] + 8, sf[2] - 8, sf[3] - 8], 0)
        face_free = free & inner & ~ndi.binary_dilation(shape_alpha > 0.03, iterations=8)
    light = is_light(gcol) if "old_board" not in roles else True
    runs_layer, runs_pl = fw.place_runs(B, face_free, age["runs"]["count"], age["runs"]["len_mm"], wrng, light)
    gfree = face_free & ~ndi.binary_dilation(runs_layer > 0.02, iterations=12)
    core, halo, gull_pl = fw.place_gull(B, gfree, age["gull"]["count"], age["gull"]["size_mm"], wrng)
    # rust: where the fixings are
    rn = age["rust"]["count"]
    heads, lens = [], []
    if rn:
        if sid == "mickeys":
            heads = [(32.0, 519.0), (W_MM - 32.0, 519.0)]
        elif sid == "ironmonger":
            heads = [(38.0 + wrng.uniform(-3, 3), 446.0 + wrng.uniform(-6, 6)), (40.0 + wrng.uniform(-3, 3), 186.0 + wrng.uniform(-6, 6))]
        elif sid == "chandler":
            heads = [(190.0 + wrng.uniform(-30, 30), 506.0), (2705.0 + wrng.uniform(-200, 200), 508.0), (5230.0 + wrng.uniform(-30, 30), 506.0)]
        elif sid == "empty_unit":
            heads = [tuple(p) for p in info.get("nail_heads_top", [])][:rn]
        heads = heads[:rn]
        lens = [float(wrng.uniform(28, 70)) for _ in heads]
    rust_layer = fw.place_rust(B, heads, lens, wrng, light) if heads else np.zeros((H_MM, W_MM), np.float32)
    fw.apply_runs(B, runs_layer, light)
    fw.apply_gull(B, core, halo)
    fw.apply_rust(B, rust_layer)
    B.layers["runs"], B.layers["gull"], B.layers["rust"] = runs_layer, core, rust_layer
    info["wear"] = dict(runs=len(runs_pl), gull=len(gull_pl), rust=len(heads), runs_at=[[int(x), int(y), int(l)] for x, y, l, _ in runs_pl],
                        gull_at=[[int(x), int(y), round(float(sz), 1)] for x, y, sz in gull_pl], rust_at=[[round(float(x), 1), round(float(y), 1)] for x, y in heads])

    # the newsagent's lower vinyl rule lifts 30 mm at its right end
    if sid == "newsagent":
        x1, y0, y1 = 5190.0, 90.0, 104.0
        win = B.win(x1 - 32, y0 - 6, x1 + 2, y1 + 4)
        a = fp.rect_alpha(win, x1 - 30, y0, x1, y1)
        r0, r1, c0, c1 = win
        B.rgb[r0:r1, c0:c1] = B.rgb[r0:r1, c0:c1] + (B.rgb[r0:r1, c0:c1] * 1.07 - B.rgb[r0:r1, c0:c1]) * a[..., None]
        sa = fp.rect_alpha(win, x1 - 30, y0 - 3.0, x1, y0)
        B.rgb[r0:r1, c0:c1] = B.rgb[r0:r1, c0:c1] * (1 - 0.35 * sa[..., None])
        B.height[r0:r1, c0:c1] += 0.35 * a
        info["vinyl_lift"] = dict(rule="lower", x_mm=[x1 - 30, x1])

    # the chandler's lower edge: salt bloom, the board whiter near the foot
    if sid == "chandler":
        prof = np.exp(-np.arange(H_MM)[::-1] / 28.0).astype(np.float32)[:, None] * (0.6 + 0.4 * np.clip(B.noise("blot"), -1, 1))
        B.rgb += (np.array([190.0, 194.0, 200.0])[None, None, :] - B.rgb) * (0.10 * np.clip(prof, 0, 1))[..., None]

    chalk(B, s)

    # ---- 7. the planted moulding, in the height map only (the outer 24 mm, +0.6 mm, a 4 mm chamfer)
    if s.get("moulding"):
        mo = s["moulding"]
        cols = np.arange(W_MM, dtype=np.float32) + 0.5
        rws = np.arange(H_MM, dtype=np.float32) + 0.5
        d = np.minimum(np.minimum(cols[None, :], W_MM - cols[None, :]), np.minimum(rws[:, None], H_MM - rws[:, None]))
        w, ch = mo["width_mm"], mo["chamfer_mm"]
        ring = np.clip((w - d) / ch, 0.0, 1.0)            # 1 up to w - chamfer from the edge, falling to 0 at w
        B.height += (mo["height_mm"] * ring).astype(np.float32)
        info["moulding"] = dict(width_mm=w, height_mm=mo["height_mm"], chamfer_mm=ch)

    # ---- 8. light: the box signs' emissive plane
    if s.get("lit") == "tubes":
        info["emissive"] = build_emissive(B, s, info)
    return B, info


def build_emissive(B, s, info):
    """The lit face of a box sign: face colour x level. level = 0.85 base, +6 per cent in a band round each tube row, the tube-end shadows
    (60 mm wide, 10 per cent dimmer) at every joint in both rows, the dead tube (laundry: upper row, x 3300 to 4800, to 60 per cent).
    JUDGEMENT (review note 5): the lengths beyond the first and last joint are lit by short end tubes at the same level, without an end shadow
    at the box's own ends."""
    em = [g for g in s["geometry"] if g.get("emissive")][0]["emissive"]
    x0, y0, x1, y1 = em["face_mm"]
    cols = np.arange(W_MM, dtype=np.float32) + 0.5
    ys = H_MM - (np.arange(H_MM, dtype=np.float32) + 0.5)
    X, Y = np.meshgrid(cols, ys)
    inside = (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)
    level = np.full((H_MM, W_MM), 0.85, np.float32)
    bandw = 40.0
    for ry in em["tube_rows_y_mm"]:
        level *= (1.0 + (em["row_band_pct"] / 100.0) * np.exp(-((Y - ry) / bandw) ** 2))
    for ry in em["tube_rows_y_mm"]:
        row_w = np.exp(-((Y - ry) / bandw) ** 2)
        for xj in em["tube_joints_x_mm"]:
            hw = em["tube_end_shadow"]["width_mm"] / 2.0
            edge = np.clip(1.0 - (np.abs(X - xj) - hw + 10.0) / 10.0, 0, 1)
            level *= (1.0 - (em["tube_end_shadow"]["dim_pct"] / 100.0) * row_w * edge)
    dead = em.get("dead_tube")
    if dead:
        up = max(em["tube_rows_y_mm"])
        dx0, dx1 = dead["x_mm"]
        hx = np.clip(np.minimum((X - dx0) / 12.0, (dx1 - X) / 12.0) + 0.5, 0, 1)
        vy = np.clip((Y - (up - 90.0)) / 60.0, 0, 1)             # the upper zone of the face; the lower row still lights it
        k = 1.0 - (1.0 - dead["level_pct"] / 100.0) * hx * vy
        level *= k
    level = np.where(inside, level, 0.0).astype(np.float32)
    B.layers["level"] = level
    emis = np.clip(B.rgb * level[..., None], 0, 255)
    # only the lit face glows: the frame and the old board do not
    B.emis = emis.astype(np.float32)
    return dict(face_mm=em["face_mm"], base_level=0.85, tube_rows_y_mm=em["tube_rows_y_mm"], tube_joints_x_mm=em["tube_joints_x_mm"],
                dead_tube=dead, ends="lit by short end tubes at the same level (judgement, review note 5)")
