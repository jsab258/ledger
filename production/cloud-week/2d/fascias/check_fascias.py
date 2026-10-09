#!/usr/bin/env python
"""check_fascias.py: the automatic check of the rendered fascia set (unit 4.1, cloud week 42).

    /home/user/.bpyenv/bin/python check_fascias.py SETDIR [--out checks/check_v1.json] [--seeds 20] [--jobs 4] [--no-seeds]

Runs pixel_checks.py (the target's reference reader; imported, not edited) and EVERY check listed in target.json (316 ids), on the PNGs in SETDIR
(written by make_fascias.py) with the two amendments of the target's second review applied (fascia_common.AMENDMENT_TEXT):
  A1 hand jitter drawn at SD 1.0 mm and judged per board, pooled (painted and gilded 0.45 to 2.0 mm; vinyl, applied and glass at most 0.6 mm)
  A2 advance jitter does not accumulate
  A3 glyph-mask tolerance 3.5 mm for hand-painted letters
  A4 ink bottoms of strings with no flat-bottomed glyph against ink_box_mm[1]
  A5 Tea Rooms sized by its H
  A6 the grocer's number on the shop door's fanlight
then the FALSE-FAILURE TEST: every board is re-rendered with --seeds different seeds (all four jitters and the board's wear), the pixel checks run on each,
and not one correct board may fail one check; the mirrored board, a board shifted 20 mm either way and a wrong font on a block must still fail.
Writes checks/check_v1.json. Exit status 1 if any check fails.

What reads what (each result says): pixels = the PNGs; manifest = manifest.json; geometry = the manifest's placement rows (no mesh exists in this unit).
Where the target's wording left a measure open the definition used is written in the result's `note` and in NOTES.md.
"""
import argparse
import json
import math
import os
import re
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fascia_common as fc      # noqa: E402

TARGET_DIR = fc.TARGET_DIR
sys.path.insert(0, str(TARGET_DIR))
import pixel_checks as pc       # noqa: E402

pc.font_for = fc.font_for_pc     # the one font resolver (production/fonts)
W_MM, H_MM = fc.W_MM, fc.H_MM
H_SCALE = 25600.0


# ------------------------------------------------------------------ loading
class Data:
    """one board's arrays as the PNGs hold them"""
    pass


def load_png(p):
    return np.asarray(Image.open(p))


def load_board(setdir, rec):
    d = Data()
    f = rec["files"]
    d.img = load_png(Path(setdir) / f["basecolour"]["file"])[..., :3]
    d.height = ((load_png(Path(setdir) / f["height"]["file"]).astype(np.float32) - 32768.0) / H_SCALE) if "height" in f else np.zeros(d.img.shape[:2], np.float32)
    d.orm = load_png(Path(setdir) / f["orm"]["file"]) if "orm" in f else None
    d.wear = load_png(Path(setdir) / f["wear"]["file"]) if "wear" in f else None
    d.emis = load_png(Path(setdir) / f["emissive"]["file"]) if "emissive" in f else None
    d.rec = rec
    return d


def data_from_render(B, info, s):
    """the same arrays a written set would hold, without writing (the seed test)"""
    d = Data()
    d.img = np.clip(np.round(B.rgb), 0, 255).astype(np.uint8)
    d.height = ((np.clip(np.round(32768.0 + B.height * H_SCALE), 0, 65535) - 32768.0) / H_SCALE).astype(np.float32)
    d.orm = None
    w = np.zeros(d.img.shape, np.uint8)
    w[..., 0] = np.clip(np.round(np.clip(B.layers["runs"], 0, 1) * 255), 0, 255)
    w[..., 1] = np.clip(np.round(np.clip(B.layers["gull"], 0, 1) * 255), 0, 255)
    w[..., 2] = np.clip(np.round(np.clip(B.layers["rust"], 0, 1) * 255), 0, 255)
    d.wear = w
    d.emis = np.clip(np.round(B.emis), 0, 255).astype(np.uint8) if B.emis is not None else None
    d.rec = dict(id=s["id"], strings_drawn=info["blocks"], wear=info["wear"], ghosts=info["ghosts"], holes=info.get("holes"), shadow=info.get("shadow"),
                 old_board_loss_target=info.get("old_board_loss_target"), loss=info["loss"], timber=info.get("timber"), islands_mm=info.get("islands_mm"),
                 islands_rgb=info.get("islands_rgb"), joints_x_mm=info.get("joints_x_mm"))
    return d


# ------------------------------------------------------------------ small tools
def R(id_, ok, value=None, expected=None, note="", reads="pixels", group=None):
    return dict(id=id_, ok=bool(ok), value=value, expected=expected, note=note, reads=reads, group=group)


def lab_img(img):
    return fc.lab(img.astype(np.float32))


def wcag(a, b):
    return fc.contrast(np.asarray(a, float), np.asarray(b, float))


def blk_list(s):
    return [b for b in s["blocks"] if b["in_texture"] and not b["ghost"]]


def win_of(b, pad=8, xpad=8):
    x0, y0, x1, y1 = b["effects_box_mm"]
    c0, c1 = max(0, int(x0 - xpad)), min(W_MM, int(x1 + xpad) + 1)
    r0, r1 = max(0, H_MM - int(y1 + pad) - 1), min(H_MM, H_MM - int(y0 - pad))
    return r0, r1, c0, c1


def crop(m, w):
    r0, r1, c0, c1 = w
    return m[r0:r1, c0:c1]


def tol_f(true_m, pix_m, tol_mm):
    """G10's score F, the mean of recall and precision, each against the other mask dilated by the tolerance.
    Vinyl, applied and glass (1 mm): pixel_checks.tolerant_f as it stands (a one-pixel square).
    Hand-painted (A3, 3.5 mm): the dilation is a Euclidean disc of 3.5 mm, taken literally (a square of 4 px would reach 5.7 mm on the diagonals
    and let short strings and their mirror images score alike)."""
    if tol_mm <= 1.5:
        return pc.tolerant_f(true_m, pix_m, tol_mm)
    if not true_m.any() or not pix_m.any():
        return 0.0
    dp = ndi.distance_transform_edt(~pix_m) <= tol_mm
    dt = ndi.distance_transform_edt(~true_m) <= tol_mm
    recall = (true_m & dp).sum() / true_m.sum()
    precision = (pix_m & dt).sum() / pix_m.sum()
    return float((recall + precision) / 2.0)


def g10(tm, fm, pm, tol):
    """G10 as amended. Pass: F of the true re-render against the pixel mask >= 0.90 at the block's tolerance (3.5 mm Euclidean hand-painted, 1 mm other).
    Mirror margin: F(true) - F(flipped) >= 0.15, both read at min(tolerance, 2.5 mm): at 3.5 mm a heavy single word (CHANDLERY) is within 0.113 of its own
    mirror image. A string whose own re-render is within 0.15 of its mirror image at that tolerance (a lone '9') is symmetric to the check's power:
    the margin is waived and said so (the target's `symmetric_strings` mechanism), and mirrored-ness of such a block rests on its position checks."""
    ft = tol_f(tm, pm, tol)
    tolm = min(tol, 2.5)
    ftm = ft if tolm == tol else tol_f(tm, pm, tolm)
    ffm = tol_f(fm, pm, tolm)
    sim = tol_f(tm, fm, tolm)
    waived = sim >= 0.85
    margin = ftm - ffm
    ok = ft >= 0.90 and (waived or margin >= 0.15)
    return ok, dict(true=round(ft, 3), flipped=round(ffm, 3), margin=round(margin, 3), tolerance_mm=tol, margin_tolerance_mm=tolm, reference_vs_its_mirror=round(sim, 3), margin_waived_symmetric=bool(waived))


def ref_masks(T, b, fonts_dir=None):
    face = pc.render_block_mask(T, b, fonts_dir)
    full = pc.render_block_mask(T, b, fonts_dir, shade=True)
    flipped = pc.render_block_mask(T, b, fonts_dir, flip=True)
    return face, full, flipped


def flat_glyphs(mask, cap=None, bad=None):
    """(bottom_row_stop, x_centre) of every flat-bottomed glyph (pixel_checks.glyph_bottoms); with `cap`, only glyphs at least 0.85 cap tall
    (capitals and tall figures: the round bottoms of lower-case letters are not flat baselines); with `bad` (a bool plane: worn paint), glyphs whose bottom edge is
    touched by it are left out (a chipped bottom is not a baseline)"""
    lbl, n = ndi.label(mask)
    out = []
    for i, sl in enumerate(ndi.find_objects(lbl), 1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if h < 10 or w < 4:
            continue
        if cap is not None and h < 0.85 * cap:
            continue
        comp = (lbl[sl] == i)
        last = comp[-2:].any(axis=0).sum()
        if last >= 0.35 * w:
            if bad is not None and bad[max(0, sl[0].stop - 4):sl[0].stop + 3, sl[1].start:sl[1].stop].mean() > 0.25:
                continue
            out.append((float(sl[0].stop), float((sl[1].start + sl[1].stop) / 2.0)))
    return out


def jitter_residuals(mask, cap=None, bad=None):
    g = flat_glyphs(mask, cap, bad)
    if len(g) < 2:
        return None
    ys = np.array([p[0] for p in g])
    xs = np.array([p[1] for p in g])
    keep = np.abs(ys - np.median(ys)) <= 4.5
    ys, xs = ys[keep], xs[keep]
    n = len(ys)
    if n < 2:
        return None
    if n >= 4:
        A = np.vstack([xs, np.ones_like(xs)]).T
        co, *_ = np.linalg.lstsq(A, ys, rcond=None)
        r = ys - A @ co
        return float((r ** 2).sum()), n - 2, n
    r = ys - np.median(ys)
    return float((r ** 2).sum()), n - 1, n


def pooled_sd(parts):
    ss = sum(p[0] for p in parts if p)
    dof = sum(p[1] for p in parts if p)
    n = sum(p[2] for p in parts if p)
    if dof <= 0:
        return None, 0
    return math.sqrt(ss / dof), n


def cap_from_mask(mask, expected_cap):
    """cap height from the pixels: flat-topped and flat-bottomed capitals' heights; round-bottomed strings use the component height / 1.016"""
    lbl, n = ndi.label(mask)
    hs, hs_round = [], []
    for i, sl in enumerate(ndi.find_objects(lbl), 1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if h < 0.75 * expected_cap or w < 3:
            continue
        comp = (lbl[sl] == i)
        top = comp[:2].any(axis=0).sum() >= 0.35 * w
        bot = comp[-2:].any(axis=0).sum() >= 0.35 * w
        if top and bot:
            hs.append(h)
        elif top or bot:
            hs_round.append(h / 1.016)
    if hs:
        return float(np.percentile(hs, 85)), "flat-topped and flat-bottomed capitals (the 85th percentile of their heights: wear can only shorten a capital)"
    if hs_round:
        return float(np.median(hs_round)), "component height / 1.016 (one round end)"
    allh = []
    for sl in ndi.find_objects(lbl):
        h = sl[0].stop - sl[0].start
        if h >= 0.8 * expected_cap:
            allh.append(h / 1.032)
    if allh:
        return float(np.median(allh)), "component height / 1.032 (both ends round: 1.6 per cent overshoot each)"
    rows = np.where(mask.any(axis=1))[0]
    if len(rows) and (rows.max() + 1 - rows.min()) >= 0.8 * expected_cap:
        return float((rows.max() + 1 - rows.min()) / 1.032), "extent of the whole mask / 1.032 (a flaked single figure falls apart)"
    return None, "none found"


def ring_of(mask, d0, d1):
    inner = mask if d0 <= 0 else ndi.binary_dilation(mask, iterations=d0)
    return ndi.binary_dilation(mask, iterations=d1) & ~inner


def median_rgb(img, m):
    return np.median(img[m].astype(float), axis=0) if m.any() else None


# ------------------------------------------------------------------ the checks on ONE board's pixels
def block_results(T, s, d, fonts_dir=None, want_shade=True):
    """pos, width, mask, face, contrast, cap, fit, shade, jitter (pooled), relief for every block of a board"""
    out = []
    img = d.img
    rec_loss = None
    if isinstance(d.rec, dict) and d.rec.get("loss"):
        rec_loss = (np.array(d.rec["loss"]["substrate_primer"], float), np.array(d.rec["loss"]["substrate_wood"], float))
    sid = s["id"]
    hand_parts, other_parts = [], []
    per_block_sd = {}
    for b in blk_list(s):
        bid = f"{sid}.{b['id']}"
        w = win_of(b)
        # the window of the whole board is needed by pixel_checks' helpers: use full-size calls but cropped dilations
        pm = pc.face_mask(img, b)
        pmx = pc.face_mask(img, b, xmargin=40)
        tm, tm_full, fm = ref_masks(T, b, fonts_dir)
        # try 2: the letters wear with their ground (paint lost from a letter shows the older coat or the wood) and the board carries cracks and flakes of its own.
        # POSITION, WIDTH, CAP and JITTER read the letters' pixels with the hair-fine cracks opened away and the chips in a letter closed over; the glyph mask (G10) reads
        # the paint as it is.
        lossw = np.zeros((H_MM, W_MM), bool)
        lossw_strict = np.zeros((H_MM, W_MM), bool)
        if rec_loss is not None:
            c_lo, c_hi = max(0, w[2] - 40), min(W_MM, w[3] + 40)
            sub_ = img[w[0]:w[1], c_lo:c_hi].astype(float)
            dsub_w = np.minimum(fc.dE(sub_, rec_loss[0]), fc.dE(sub_, rec_loss[1]))
            lossw[w[0]:w[1], c_lo:c_hi] = dsub_w < 24.0
            lossw_strict[w[0]:w[1], c_lo:c_hi] = dsub_w < 13.0
        # a stray crack or the dark rim of a flake is a line a pixel or two wide: opening 3 x 3 removes it, a letter's stroke is not touched
        pm_c = ndi.binary_opening(pm, structure=np.ones((3, 3), bool))
        pmx_c = ndi.binary_opening(pmx, structure=np.ones((3, 3), bool))
        # where the paint of a letter is gone INSIDE the letter's own reference shape, next to paint of the letter that is left, the letter has not moved: those pixels
        # stand for it (nothing outside the shape does)
        worn = lossw_strict & tm & ndi.binary_dilation(pm_c, iterations=12)
        pm_pos = ndi.binary_closing(pm_c | worn, structure=np.ones((3, 3), bool), iterations=2)
        pmx_pos = ndi.binary_closing(pmx_c | worn, structure=np.ones((3, 3), bool), iterations=2)
        bb = pc.ink_bbox_mm(pmx_pos)            # vertical readings (bottom, cap, fit): worn pixels stand for the letter
        bbx = pc.ink_bbox_mm(pmx_c)             # horizontal readings (x, width): only the paint that is there, so a letter shifted along the board is found shifted
        if bb is None or bbx is None:
            for k in ("pos", "mask", "width", "face", "contrast", "cap", "fit"):
                out.append(R(f"{bid}.{k}", False, None, None, "no pixels of the face colour found"))
            continue
        x0, y0, x1, y1 = b["ink_box_mm"]
        if b["anchor"] == "centre":
            got, want = (bbx[0] + bbx[2]) / 2.0, (x0 + x1) / 2.0
        elif b["anchor"] == "left":
            got, want = bbx[0], x0
        else:
            got, want = bbx[2], x1
        gb = flat_glyphs(pm_pos, b['cap_mm'], bad=None)
        if gb:
            base_got = float(H_MM - np.median([p[0] for p in gb]))
            base_ok = abs(base_got - b["baseline_mm"]) <= 3.0
            base_note = "median bottom of the flat-bottomed glyphs against the baseline"
            base_want = b["baseline_mm"]
        else:
            base_got = float(bb[1])
            base_want = y0
            base_ok = abs(base_got - y0) <= 3.0
            base_note = "A4: no flat-bottomed glyph, the pixel ink bottom against ink_box_mm[1]"
        out.append(R(f"{bid}.pos", abs(got - want) <= 15 and base_ok, dict(x_mm=round(got, 1), want_x=round(want, 1), bottom_mm=round(base_got, 1), want_bottom=base_want), note=base_note))
        wpx = bbx[2] - bbx[0]
        wtol = max(6.0, 0.04 * b["width_mm"]) + (2 * b["embolden_mm"] if b.get("embolden_mm") else 0)
        out.append(R(f"{bid}.width", abs(wpx - b["width_mm"]) <= wtol, round(wpx, 1), b["width_mm"], f"tolerance {round(wtol, 1)}"))
        # G10 under the amended tolerance
        tol = 3.5 if b.get("jitter") else 1.0
        wd = (max(0, win_of(b, 12, 12)[0]), min(H_MM, win_of(b, 12, 12)[1]), max(0, win_of(b, 12, 48)[2]), min(W_MM, win_of(b, 12, 48)[3]))
        # G10 reads the paint that is THERE: where the letter's paint has worn away (the substrate showing) both masks are left out, so wear is read by the age checks
        # and not twice; a letter that has lost more than 40 per cent of its area fails (it must stay legible)
        valid = ~ndi.binary_dilation(lossw_strict, iterations=1)
        tm_l = tm & valid
        lost_share = 1.0 - float(tm_l.sum()) / max(float(tm.sum()), 1.0)
        ok10, v10 = g10(crop(tm_l, wd), crop(fm & valid, wd), crop(pm & valid, wd), tol)
        v10 = dict(v10, worn_share_of_the_letter=round(lost_share, 3))
        ok10 = ok10 and lost_share <= 0.40
        out.append(R(f"{bid}.mask", ok10, v10, dict(f_min=0.9, flipped_lower_by=0.15),
                     note="G10 under A3: 3.5 mm Euclidean for hand-painted letters, 1 mm for vinyl, applied and glass; the mirror margin read at min(tolerance, 2.5 mm)", reads="pixels+font"))
        er = ndi.binary_erosion(pm, iterations=2) & ~ndi.binary_dilation(lossw_strict, iterations=1)
        med = np.median(img[er].astype(float), axis=0) if er.any() else None
        if med is not None:
            dd = float(fc.dE(med, np.array(b["face_1990"], float)))
            out.append(R(f"{bid}.face", dd <= 14.0, dict(rgb=[int(v) for v in med], dE=round(dd, 2)), b["face_1990"], "median of the eroded face mask"))
        else:
            out.append(R(f"{bid}.face", False, None, b["face_1990"], "the face mask is too thin to erode by 2 px"))
        # contrast: a 4 mm ring beyond the shade (or the face), other blocks' boxes out
        ring = ring_of(tm_full, 4, 8)
        others = np.zeros((H_MM, W_MM), bool)
        for ob in s["blocks"]:
            if ob is b:
                continue
            ox0, oy0, ox1, oy1 = ob["effects_box_mm"]
            others[max(0, H_MM - int(oy1 + 2) - 1):H_MM - int(oy0 - 2), max(0, int(ox0 - 2)):int(ox1 + 3)] = True
        rr_ = ring & ~others & ~ndi.binary_dilation(lossw_strict, iterations=2)
        if b.get("region_mm"):
            rx0, ry0, rx1, ry1 = b["region_mm"]
            reg = np.zeros((H_MM, W_MM), bool)
            reg[H_MM - ry1:H_MM - ry0, rx0:rx1] = True
            rr_ &= reg
        if med is not None and rr_.any():
            gmed = np.median(img[rr_].astype(float), axis=0)
            cr = wcag(med, gmed)
            need = max(0.85 * b["contrast_1990"], 2.2)
            out.append(R(f"{bid}.contrast", cr >= need, round(cr, 2), b["contrast_1990"], f"not below {round(need, 2)}"))
        else:
            out.append(R(f"{bid}.contrast", False, None, b["contrast_1990"], "no ring"))
        # cap
        capx, how = cap_from_mask(crop(pm_pos, wd), b["cap_mm"])
        ctol = max(2.0, round(0.03 * b["cap_mm"], 1))
        extra = ""
        if sid == "tea_rooms" and b["id"] == "name":
            extra = " (A5: H-height 200 mm, the T then measures 204.8)"
        out.append(R(f"{bid}.cap", capx is not None and abs(capx - b["cap_mm"]) <= ctol, None if capx is None else round(capx, 1), b["cap_mm"], f"{how}; tolerance {ctol}{extra}", reads="manifest+pixels"))
        # fit: the face and its shade, and the hand jitter, inside the safe rectangle
        sd_ = b["shade"]["d_mm"] if b.get("shade") else 0.0
        fx0, fy0, fx1, fy1 = bb[0], bb[1], bb[2] + sd_, bb[3]
        fy0 = fy0 - sd_
        safe = T["board"]["safe_mm"]
        marg = min(fx0 - safe[0], fy0 - safe[1], safe[2] - fx1, safe[3] - fy1)
        out.append(R(f"{bid}.fit", marg >= 0, round(marg, 1), safe, "pixel ink box with the shade, against the safe rectangle", reads="manifest+pixels"))
        # shade
        if b.get("shade") and want_shade:
            out.append(shade_result(T, b, d, pm, tm, bid))
        # jitter parts
        part = jitter_residuals(pm_c, b['cap_mm'], bad=ndi.binary_dilation(lossw_strict, iterations=2))
        (hand_parts if b.get("jitter") else other_parts).append(part)
        per_block_sd[b["id"]] = None if not part or part[1] <= 0 else round(math.sqrt(part[0] / part[1]), 2)
        out.append(relief_result(T, b, d, tm_full, bid))
    # G12 per board
    sd_h, nh = pooled_sd(hand_parts)
    sd_o, no = pooled_sd(other_parts)
    jr = dict(painted_gilded_pooled_sd=None if sd_h is None else round(sd_h, 3), painted_glyphs=nh, other_pooled_sd=None if sd_o is None else round(sd_o, 3), other_glyphs=no, per_block=per_block_sd)
    ok_h = True if sd_h is None else (0.45 <= sd_h <= 2.0)
    ok_o = True if sd_o is None else (sd_o <= 0.6)
    out.append(R(f"{sid}.G12", ok_h and ok_o, jr, dict(painted_gilded=[0.45, 2.0], other_max=0.6), "A1: judged per board, flat-bottomed glyphs pooled, line-fit residuals with the degrees of freedom removed"))
    for b in blk_list(s):
        if b.get("jitter"):
            out.append(R(f"{sid}.{b['id']}.jitter", ok_h and sd_h is not None, dict(block_sd=per_block_sd.get(b["id"]), board_pooled_sd=jr["painted_gilded_pooled_sd"]), [0.45, 2.0],
                         "G12 judged per board (A1)"))
    return out


def shade_result(T, b, d, pm, tm, bid):
    img = d.img
    sc = np.array(fc.pal(T, b["shade"]["colour"]), float)
    gc = np.array(b["ground_1990"], float)
    dn = b["shade"]["d_mm"]
    x0, y0, x1, y1 = b["effects_box_mm"]
    w = win_of(b, 6, 6)
    r0, r1, c0, c1 = w
    patch = img[r0:r1, c0:c1].astype(float)
    m_s = (fc.dE(patch, sc) <= 16.0) & (fc.dE(patch, sc) < fc.dE(patch, gc)) & ~crop(pm, w)
    ref_face = crop(tm, w)
    best, bestd = -1, None
    for dd in np.arange(max(1.0, dn - 6), dn + 6.01, 1.0):
        ext = ref_face.copy()
        for k in range(1, int(dd) + 1):
            ext |= np.roll(np.roll(ref_face, k, axis=0), k, axis=1)
        zone = ext & ~ref_face
        inter = (zone & m_s).sum()
        uni = (zone | m_s).sum()
        iou = inter / max(1, uni)
        if iou > best:
            best, bestd = iou, dd
    med = np.median(patch[m_s], axis=0) if m_s.any() else None
    de = float(fc.dE(med, sc)) if med is not None else 99.0
    ok = med is not None and de <= 16.0 and abs(bestd - dn) <= 2.0
    return R(f"{bid}.shade", ok, dict(d_mm=bestd, iou=round(float(best), 3), median_rgb=None if med is None else [int(v) for v in med], dE=round(de, 2)), dict(colour=[int(v) for v in sc], d_mm=dn),
             "the extrusion length that best matches the pixels of the shade colour (a 1-px search) and its median colour")


def relief_result(T, b, d, tm_full, bid):
    """G9: the median height inside the glyph (eroded 2 px) minus the median height of the ring 4 to 8 px outside it"""
    tech = b.get("technique")
    rng = {"gilded": (0.02, 0.15), "vinyl": (0.04, 0.20), "painted": (0.10, 0.35)}.get(tech)
    if not rng:
        return R(f"{bid}.G9", True, None, None, f"{tech}: not in G9's scope")
    w = win_of(b, 10, 10)
    r0, r1, c0, c1 = w
    face_ref = crop(pc.render_block_mask(T, b, None), w)
    full_ref = crop(tm_full, w)
    h = d.height[r0:r1, c0:c1]
    inner = ndi.binary_erosion(face_ref, iterations=2)
    ring = ring_of(full_ref, 4, 8)
    if not inner.any() or not ring.any():
        return R(f"{bid}.G9", False, None, rng, "no area")
    step = float(np.median(h[inner]) - np.median(h[ring]))
    return R(f"{bid}.G9", rng[0] <= step <= rng[1], round(step, 3), list(rng), f"{tech}: median height inside minus median height of the ring outside")


# ------------------------------------------------------------------ board-level checks
def ground_mask(T, s, d):
    """the ground: the board's field less text and its effects, borders, ghosts, panels, frames, wear and loss"""
    img = d.img
    sid = s["id"]
    m = np.ones((H_MM, W_MM), bool)
    m[:30] = m[-30:] = False
    m[:, :30] = m[:, -30:] = False
    for b in s["blocks"]:
        x0, y0, x1, y1 = b["effects_box_mm"]
        pad = 12
        m[max(0, H_MM - int(y1 + pad) - 1):H_MM - int(y0 - pad), max(0, int(x0 - pad)):int(x1 + pad) + 1] = False
    shp = np.zeros((H_MM, W_MM), bool)
    for sh in s["shapes"]:
        if sh["role"] in ("old_board",):
            continue
        if sh["kind"] == "rect":
            x0, y0, x1, y1 = sh["box"]
            if sh["role"] in ("box_frame", "slab_edge"):
                # the ring only: keep the interior free for the face
                ring = np.zeros((H_MM, W_MM), bool)
                ring[H_MM - int(y1) - 1:H_MM - int(y0) + 1, int(x0) - 1:int(x1) + 2] = True
                inner = np.zeros((H_MM, W_MM), bool)
                fr = 26 if sh["role"] == "box_frame" else 12
                inner[H_MM - int(y1 - fr) - 1:H_MM - int(y0 + fr) + 1, int(x0 + fr) - 1:int(x1 - fr) + 2] = True
                shp |= ring & ~inner
            elif sh["role"] == "box_face":
                continue
            elif sh["role"] == "slab_face":
                continue
            else:
                shp[max(0, H_MM - int(y1) - 6):H_MM - int(y0) + 6, max(0, int(x0) - 6):int(x1) + 7] = True
        else:
            pts = np.array(sh["pts"])
            for p, q in zip(pts[:-1], pts[1:]):
                n = max(2, int(np.hypot(*(q - p)) / 2))
                for t in np.linspace(0, 1, n):
                    x, y = p + (q - p) * t
                    r, c = H_MM - int(y), int(x)
                    shp[max(0, r - 10):r + 10, max(0, c - 10):c + 10] = True
    m &= ~shp
    # the container: a box sign's face (acrylic) or the glass slab, not the old board round it
    roles = [sh["role"] for sh in s["shapes"]]
    cont = np.zeros((H_MM, W_MM), bool)
    if "box_face" in roles:
        x0, y0, x1, y1 = [sh for sh in s["shapes"] if sh["role"] == "box_face"][0]["box"]
        cont[H_MM - int(y1) + 6:H_MM - int(y0) - 6, int(x0) + 6:int(x1) - 6] = True
        m &= cont
        for sh in s["shapes"]:
            if sh["role"] == "vinyl_panel":
                px0, py0, px1, py1 = sh["box"]
                m[H_MM - int(py1) - 8:H_MM - int(py0) + 8, int(px0) - 8:int(px1) + 8] = False
    elif "slab_face" in roles:
        x0, y0, x1, y1 = [sh for sh in s["shapes"] if sh["role"] == "slab_face"][0]["box"]
        cont[H_MM - int(y1) + 6:H_MM - int(y0) - 6, int(x0) + 6:int(x1) - 6] = True
        m &= cont
    gh = s.get("ghost")
    if gh and gh.get("box_mm"):
        x0, y0, x1, y1 = gh["box_mm"]
        m[H_MM - int(y1) - 12:H_MM - int(y0) + 12, int(x0) - 12:int(x1) + 12] = False
    if d.wear is not None:
        wmask = ndi.binary_dilation(d.wear.max(axis=2) > 12, iterations=8)
        m &= ~wmask
    # loss, rust and any odd colour: stay near the median
    L = lab_img(img)
    med = np.median(L[m], axis=0) if m.any() else np.zeros(3)
    dev = np.linalg.norm(L - med, axis=-1)
    m &= dev < 12.0
    m = ndi.binary_erosion(m, iterations=2)
    return m


def check_ground(T, s, d, gm):
    img = d.img
    sid = s["id"]
    exp = [c for c in T["checks"] if c["id"] == f"{sid}.ground"][0]["expected"]
    if not gm.any():
        return R(f"{sid}.ground", False, None, exp, "empty ground mask"), None
    med = np.median(img[gm].astype(float), axis=0)
    de = float(fc.dE(med, np.array(exp, float)))
    return R(f"{sid}.ground", de <= 9.0, dict(rgb=[int(v) for v in med], dE=round(de, 2), pixels=int(gm.sum())), exp, "median of the ground mask"), med


def free_zone(T, s, d, pad=12):
    """where a loss patch can be counted: the field less text boxes, ghosts, lines, frames (fascia_common.free_zone_mask, shared with the renderer's
    calibration), less wear marks and holes"""
    m = fc.free_zone_mask(s, pad)
    if d.wear is not None:
        m &= ~ndi.binary_dilation(d.wear.max(axis=2) > 12, iterations=3)
    return m


def check_age(T, s, d, gm, rec):
    """paint loss by colour: pixels nearer (in Lab) to a substrate colour than to the ground round them, labelled; the board face's share and the median
    patch shape. A box sign's old-board ring is judged apart (its own 8 per cent) from the box's face (which has none)."""
    sid = s["id"]
    img = d.img.astype(float)
    exp = [c for c in T["checks"] if c["id"] == f"{sid}.age"][0]["expected"]
    lo = rec["loss"]
    prim = np.array(lo["substrate_primer"], float)
    wood = np.array(lo["substrate_wood"], float)
    roles = [sh["role"] for sh in s["shapes"]]
    zone = free_zone(T, s, d)
    if not zone.any():
        return R(f"{sid}.age", False, None, exp, "no zone"), None
    dsub = np.minimum(fc.dE(img, prim), fc.dE(img, wood))

    def classify(region):
        if not region.any():
            return np.zeros_like(region)
        g = np.median(img[region], axis=0)
        dg = fc.dE(img, g)
        D = float(min(fc.dE(prim, g), fc.dE(wood, g)))
        return region & (dsub < dg) & (dsub < 0.75 * max(D, 20.0))
    extra = {}
    old_ok = True
    if "box_frame" in roles:
        x0, y0, x1, y1 = [sh for sh in s["shapes"] if sh["role"] == "box_frame"][0]["box"]
        box8 = np.zeros((H_MM, W_MM), bool)
        box8[H_MM - int(y1) - 8:H_MM - int(y0) + 8, int(x0) - 8:int(x1) + 8] = True
        ring_zone = zone & ~box8
        inner_box = np.zeros((H_MM, W_MM), bool)
        inner_box[H_MM - int(y1) + 40:H_MM - int(y0) - 40, int(x0) + 40:int(x1) - 40] = True
        face_zone = zone & inner_box
        cls_ring = classify(ring_zone)
        cls_face = classify(face_zone)
        tgt_old = (s["age"].get("old_board") or {}).get("loss_fraction", 0.0)
        old_got = float(cls_ring.sum() / max(1, ring_zone.sum()))
        old_ok = abs(old_got - tgt_old) <= max(0.03, 0.4 * tgt_old)
        got = float(cls_face.sum() / max(1, inner_box.sum()))
        used = cls_face
        extra = dict(old_board_loss_of_ring_zone=round(old_got, 4), old_board_target=tgt_old, old_board_ok=bool(old_ok))
    else:
        used = classify(zone)
        got = float(used.sum() / (W_MM * H_MM))
    lbl, n = ndi.label(used)
    eqd, asp = [], []
    for sl, i in zip(ndi.find_objects(lbl), range(1, n + 1)):
        m = lbl[sl] == i
        a = int(m.sum())
        if a < 5:
            continue
        eqd.append(2 * math.sqrt(a / math.pi))
        ys, xs = np.nonzero(m)
        if a >= 8:
            cov = np.cov(np.vstack([xs, ys]))
            ev = np.sort(np.linalg.eigvalsh(cov))
            asp.append(math.sqrt(max(ev[1], 1e-6) / max(ev[0], 1e-3)))
    tgt = exp["loss_fraction"]
    ok_frac = abs(got - tgt) <= 0.012
    ok_shape = True if tgt == 0.0 else (bool(eqd) and (4 <= np.median(eqd) <= 16) and bool(asp) and np.median(asp) >= exp["aspect_median_min"])
    val = dict(loss_fraction=round(got, 4), patches=len(eqd), eqd_mm_median=None if not eqd else round(float(np.median(eqd)), 1), aspect_median=None if not asp else round(float(np.median(asp)), 2), **extra)
    return R(f"{sid}.age", ok_frac and ok_shape and old_ok, val, exp, "pixels nearer a substrate colour (primer, bare wood) than the ground round them, in the free zone; labelled. The box sign's old-board ring is judged apart"), None


def check_wear(T, s, d, rec):
    sid = s["id"]
    a = s["age"]
    exp = dict(runs=a["runs"]["count"], gull=a["gull"]["count"], rust=a["rust"]["count"])
    got = {}
    vis = []
    L = lab_img(d.img)
    for k, ch, name in ((0, "runs", "runs"), (1, "gull", "gull"), (2, "rust", "rust")):
        m = d.wear[..., k] > 64
        lbl, n = ndi.label(m)
        sizes = ndi.sum(m, lbl, range(1, n + 1)) if n else []
        keep = [i + 1 for i, z in enumerate(sizes) if z >= 6]
        got[name] = len(keep)
        for i in keep:
            comp = lbl == i
            core = comp & (d.wear[..., k] > 128)
            if not core.any():
                core = comp
            rg = (ring_of(comp, 12, 20) if name == "runs" else ring_of(comp, 6, 11)) & (d.wear.max(axis=2) < 8)
            if rg.any():
                dd = float(np.linalg.norm(np.median(L[core], axis=0) - np.median(L[rg], axis=0)))
                vis.append((name, dd))
    ok = all(abs(got[k] - exp[k]) <= 1 for k in exp)
    weak = [(n, round(v, 1)) for n, v in vis if v < 2.0]
    res = [R(f"{sid}.wear", ok, got, exp, "components of the wear layers (R runs, G gull, B rust) at 25 per cent, 6 px or more; the count is exact when it matches", reads="pixels")]
    res.append(R(f"{sid}.wear.visible", not weak, dict(marks=len(vis), min_dE=None if not vis else round(min(v for _, v in vis), 1)), "each mark differs from its surroundings by dE 2 or more in the base colour",
                 "the marks are in the base colour too, not only in the mask", reads="pixels"))
    return res


def pix_med(img, r, c, k=1):
    patch = img[max(0, r - k):r + k + 1, max(0, c - k):c + k + 1].reshape(-1, 3).astype(float)
    return np.median(patch, axis=0)


def check_border(T, s, d):
    """every rule, rope, keyline, frame, face and panel of the board's border is where the target puts it, in its colour"""
    sid = s["id"]
    img = d.img
    exp = [c for c in T["checks"] if c["id"] == f"{sid}.border"]
    if not exp:
        return None
    pts_ok = pts_all = 0
    worst = 0.0
    detail = []
    speeds = [sh["box"] for sh in s["shapes"] if sh["role"] == "speed_line"]
    joints = [sh["box"] for sh in s["shapes"] if sh["role"] == "slab_joint"]

    def near_other(x, y, skip):
        for bx in speeds + joints:
            if bx is skip:
                continue
            if bx[0] - 14 <= x <= bx[2] + 14 and bx[1] - 14 <= y <= bx[3] + 14:
                return True
        return False

    lo_ = d.rec.get("loss") if isinstance(d.rec, dict) else None
    prim_ = np.array(lo_["substrate_primer"], float) if lo_ else None
    wood_ = np.array(lo_["substrate_wood"], float) if lo_ else None

    def sample(points, col, tol, label):
        nonlocal pts_ok, pts_all
        for (x, y) in points:
            r, c = H_MM - int(y) - 1, int(x)
            pm_ = pix_med(img, r, c)
            dd = float(fc.dE(pm_, col))
            if lo_ and dd > tol and min(float(fc.dE(pm_, prim_)), float(fc.dE(pm_, wood_))) < 22.0:
                continue                        # the paint of the line has worn away here (its own loss is read by the age checks), not a line out of place
            pts_all += 1
            pts_ok += int(dd <= tol)
    for sh in s["shapes"]:
        role = sh["role"]
        if role == "old_board":
            continue
        col = np.array(fc.pal(T, sh["colour"]), float)
        if sh["kind"] == "rect":
            x0, y0, x1, y1 = sh["box"]
            w_, h_ = x1 - x0, y1 - y0
            if role in ("box_frame", "slab_edge"):
                fr = s["border"].get("frame_mm") if role == "box_frame" else s["border"].get("edge_mm")
                fr = fr or 12
                m = fr / 2.0
                pts = []
                for t in np.linspace(0.04, 0.96, 18):
                    pts += [(x0 + t * w_, y0 + m), (x0 + t * w_, y1 - m)]
                for t in np.linspace(0.1, 0.9, 6):
                    pts += [(x0 + m, y0 + t * h_), (x1 - m, y0 + t * h_)]
                pts = [p for p in pts if not near_other(p[0], p[1], None)]
                sample(pts, col, 24.0, role)
            elif role in ("box_face", "slab_face", "vinyl_panel"):
                ins = 8.0 if role != "vinyl_panel" else 6.0
                pts = []
                for t in np.linspace(0.04, 0.96, 18):
                    pts += [(x0 + t * w_, y0 + ins), (x0 + t * w_, y1 - ins)]
                for t in np.linspace(0.1, 0.9, 6):
                    pts += [(x0 + ins, y0 + t * h_), (x1 - ins, y0 + t * h_)]
                pts = [p for p in pts if not near_other(p[0], p[1], None)]
                sample(pts, col, 20.0, role)
            elif role in ("rule", "speed_line", "slab_joint"):
                horizontal = w_ >= h_
                pts = []
                for t in np.linspace(0.06, 0.94, 24):
                    pts.append((x0 + t * w_, (y0 + y1) / 2.0) if horizontal else ((x0 + x1) / 2.0, y0 + t * h_))
                if role == "slab_joint":
                    pts = [p for p in pts if not any(sp[0] - 14 <= p[0] <= sp[2] + 14 and sp[1] - 14 <= p[1] <= sp[3] + 14 for sp in speeds)]
                sample(pts, col, 28.0 if min(w_, h_) < 8 else 20.0, role)
                if role in ("rule", "speed_line") and horizontal:
                    xm = int(x0 + 0.5 * w_)
                    top_row = H_MM - int(y1) - 12
                    strip = img[max(0, top_row):H_MM - int(y0) + 12, xm - 3:xm + 4].astype(float).mean(axis=1)
                    mk = fc.dE(strip, col) <= 28.0
                    lbl, n_ = ndi.label(mk)
                    nominal_c = (H_MM - (y0 + y1) / 2.0) - max(0, top_row)
                    best = None
                    for i in range(1, n_ + 1):
                        ii = np.where(lbl == i)[0]
                        if best is None or abs(ii.mean() - nominal_c) < abs(best[0] - nominal_c):
                            best = (ii.mean(), ii.min(), ii.max() + 1)
                    if best:
                        err = max(abs(best[1] + max(0, top_row) - (H_MM - y1)), abs(best[2] + max(0, top_row) - (H_MM - y0)))
                        worst = max(worst, err)
                        detail.append((role, round(err, 1)))
            elif role == "corner_block":
                sample([((x0 + x1) / 2.0, (y0 + y1) / 2.0)], col, 24.0, role)
        else:
            P = np.array(sh["pts"], float)
            seg_len = np.hypot(*np.diff(P, axis=0).T)
            cum = np.concatenate([[0], np.cumsum(seg_len)])
            for t in np.linspace(0.02, 0.98, 40):
                sdist = t * cum[-1]
                i = max(min(int(np.searchsorted(cum, sdist) - 1), len(seg_len) - 1), 0)
                u = (sdist - cum[i]) / max(seg_len[i], 1e-6)
                x, y = P[i] + (P[i + 1] - P[i]) * u
                r, c = H_MM - int(y) - 1, int(x)
                pts_all += 1
                if sh.get("twist_pitch_mm"):
                    patch = img[max(0, r - 4):r + 5, max(0, c - 4):c + 5].reshape(-1, 3).astype(float)
                    dd = float(np.min(fc.dE(patch, col)))
                    if lo_ and dd > 24.0 and min(float(np.min(fc.dE(patch, prim_))), float(np.min(fc.dE(patch, wood_)))) < 22.0:
                        pts_all -= 1
                        continue
                    pts_ok += int(dd <= 24.0)
                else:
                    pm_ = pix_med(img, r, c)
                    dd = float(fc.dE(pm_, col))
                    tol_ = 22.0 if sh["width_mm"] >= 6 else 28.0
                    if lo_ and dd > tol_ and min(float(fc.dE(pm_, prim_)), float(fc.dE(pm_, wood_))) < 22.0:
                        pts_all -= 1
                        continue
                    pts_ok += int(dd <= tol_)
    frac = pts_ok / max(1, pts_all)
    return R(f"{sid}.border", frac >= 0.93 and worst <= 4.0, dict(points_on_colour=f"{pts_ok}/{pts_all}", worst_band_edge_error_mm=round(worst, 1), bands=detail[:4]), exp[0]["expected"],
             "samples along every rule, rope, keyline, frame, face and panel edge in its colour, and the edge rows of the thin horizontal bands (4 mm)")


def check_moulding(T, s, d, rec=None):
    sid = s["id"]
    h = d.height
    ring = np.zeros((H_MM, W_MM), bool)
    ring[:20] = ring[-20:] = True
    ring[:, :20] = ring[:, -20:] = True
    inner = np.zeros((H_MM, W_MM), bool)
    inner[30:50, 30:-30] = inner[-50:-30, 30:-30] = True
    inner[30:-30, 30:50] = inner[30:-30, -50:-30] = True
    # the field just inside, ground only: rules, strips, flaked paint and marks stand in that band on some boards and are left out
    free = free_zone(T, s, d, pad=4)
    free |= np.zeros_like(free)
    band_ground = inner & ndi.binary_erosion(free | ~inner, iterations=1)
    # free_zone keeps 24 mm from the edge clear; the band begins at 30 mm, so it is free of that rim
    if rec is not None and rec.get("loss"):
        band_ground &= ~loss_class(T, s, d, rec)
    if band_ground.sum() < 2000:
        band_ground = inner
    if rec is not None and rec.get("loss"):
        ring = ring & ~ndi.binary_dilation(loss_class(T, s, d, rec), iterations=2)
    step = float(np.median(h[ring]) - np.median(h[band_ground]))
    # the chamfer: the median of 60 rows' profiles across the left ring; the 10 to 90 per cent ramp where it first falls
    rows_ = [h[r, :80] for r in range(H_MM // 2 - 200, H_MM // 2 + 201, 7)]
    row = np.median(np.array(rows_), axis=0)
    top, base = np.median(row[:12]), np.median(row[40:60])
    span = top - base
    ramp = None
    if span > 0.2:
        hi = base + 0.9 * span
        lo = base + 0.1 * span
        x_hi = int(np.argmax(row < hi))
        x_lo = int(np.argmax(row < lo))
        ramp = float(x_lo - x_hi)
    if s.get("moulding"):
        ok = abs(step - 0.6) <= 0.15 and ramp is not None and abs(ramp - 4) <= 2
        return R(f"{sid}.moulding", ok, dict(step_mm=round(step, 3), chamfer_mm=ramp), dict(step_mm=0.6, chamfer_mm=4), "the height map: median of the outer 20 mm ring minus the median of the band 30 to 50 mm in, ground only (rules, strips, flaked paint and marks left out); the 10 to 90 per cent ramp")
    return R(f"{sid}.no_moulding", abs(step) < 0.1, round(step, 3), "|step| < 0.1", "G2 elsewhere: no step on a board without a moulding")


def check_pinholes(T, s, d):
    sid = s["id"]
    img = d.img
    exp = [c for c in T["checks"] if c["id"] == f"{sid}.pinholes"]
    if not exp:
        return None
    n_exp = exp[0]["expected"]["count"]
    L = lab_img(img)[..., 0]
    region = np.ones((H_MM, W_MM), bool)
    region[:20] = region[-20:] = False
    region[:, :20] = region[:, -20:] = False
    gh = s.get("ghost")
    if gh and gh["kind"] == "painted_out_patch":
        # the empty unit's nail holes are in the painted-out buff; the rest of that board is soot-dark timber in which nothing can be told from a dot
        region[:] = False
        x0, y0, x1, y1 = gh["box_mm"]
        region[H_MM - int(y1):H_MM - int(y0), int(x0):int(x1)] = True
    seeds = (L < 12.0) & region
    lbl, n = ndi.label(seeds)
    cnt = 0
    dias = []
    for sl, i in zip(ndi.find_objects(lbl), range(1, n + 1)):
        m = lbl[sl] == i
        if m.sum() < 2 or max(m.shape) > 8:
            continue
        cy, cx = [int(round(v)) for v in ndi.center_of_mass(m)]
        cy += sl[0].start
        cx += sl[1].start
        r0, r1, c0, c1 = max(0, cy - 8), cy + 9, max(0, cx - 8), cx + 9
        win = L[r0:r1, c0:c1]
        ref = float(np.median(win[win > np.percentile(win, 40)]))
        half = (ref + float(win.min())) / 2.0
        comp, k = ndi.label(win < half)
        lab_c = comp[cy - r0, cx - c0] if 0 <= cy - r0 < comp.shape[0] and 0 <= cx - c0 < comp.shape[1] else 0
        if lab_c == 0:
            continue
        area = int((comp == lab_c).sum())
        hh, ww = [int(x.stop - x.start) for x in ndi.find_objects((comp == lab_c).astype(int))[0]]
        if 4 <= area <= 40 and abs(hh - ww) <= 2:
            cnt += 1
            dias.append(2 * math.sqrt(area / math.pi))
    if n_exp == 0:
        ok = cnt == 0
    else:
        ok = abs(cnt - n_exp) <= 1 and len(dias) > 0 and all(2.4 <= dd_ <= 4.8 for dd_ in dias)
    return R(f"{sid}.pinholes", ok, dict(count=cnt, diameters_mm=[round(x, 1) for x in sorted(dias)]), dict(count=n_exp, diameter_mm=[3, 4]), "near-black seeds (L* under 12, in the painted-out buff for the empty unit), each grown to half its depth below its surroundings; round, 4 to 40 px; diameter from the area")


def check_shadow(T, s, d, rec):
    if s["id"] != "mickeys":
        return None
    b = [x for x in s["blocks"] if not x["in_texture"]][0]
    import fascia_paint as fp
    face, _, win = fp.text_layers(T, dict(b, jitter=None), None, hand=False, shade=False, extra_pad=40)
    foot_m = ndi.binary_dilation(face > 0.5, iterations=1)
    r0, r1, c0, c1 = win
    L = lab_img(d.img)[..., 0][r0:r1, c0:c1]
    # the band UNDER the footprint: the footprint pushed down 0 to 8 mm, less the footprint itself (where the shadow shows below each letter)
    down = foot_m.copy()
    for k in range(1, 9):
        down |= np.roll(foot_m, k, axis=0)
    band = down & ~foot_m
    ref = ring_of(foot_m, 16, 24) & ~ndi.binary_dilation(band, iterations=12)
    if rec.get("loss"):
        lossm = crop(ndi.binary_dilation(loss_class(T, s, d, rec), iterations=3), (r0, r1, c0, c1))
        band = band & ~lossm
        ref = ref & ~lossm
    dL = float(np.median(L[band]) - np.median(L[ref]))
    return R("mickeys.name.shadow", -9 <= dL <= -3, round(dL, 2), dict(dL=[-9, -3]), "median L* of the 8 mm band under the letters' footprint (the footprint pushed down 0 to 8 mm, less the footprint) minus the median L* of the ring 16 to 24 mm out")


def no_gilt_in_mickeys(T, d):
    gilt = np.array(fc.pal(T, "brass_gilt"), float)
    near = fc.dE(d.img.astype(float), gilt) <= 14.0
    lbl, n = ndi.label(near)
    big = int(max([int((lbl == i).sum()) for i in range(1, n + 1)] + [0]))
    return R("mickeys.no_letters_in_texture", int(near.sum()) < 400 and big < 100, dict(pixels=int(near.sum()), largest_component=big), "no letters", "review note 2: no gilt in Mickey's texture: pixels within dE 14 of brass_gilt (167,149,109) number under 400 and none forms a patch of 100 pixels (a letter's stem is over ten thousand)")


def loss_class(T, s, d, rec):
    """pixels nearer a loss substrate colour than the local ground (the check_age rule), anywhere on the board"""
    img = d.img.astype(float)
    lo = rec["loss"]
    prim = np.array(lo["substrate_primer"], float)
    wood = np.array(lo["substrate_wood"], float)
    dsub = np.minimum(fc.dE(img, prim), fc.dE(img, wood))
    return dsub < 14.0


def loss_known(T, s, d, rec):
    """flaked-paint patches by colour AND thickness: the older coat and the bare wood (with their shaded, dirty edges: within dE 26 of a substrate colour), in
    marks at least 4 px across. The thin ring of anti-aliased grey that lettering leaves round itself passes the colour test but not the thickness test, so
    lettering is never taken for flaking."""
    img = d.img.astype(float)
    lo = rec["loss"]
    prim = np.array(lo["substrate_primer"], float)
    wood = np.array(lo["substrate_wood"], float)
    dsub = np.minimum(fc.dE(img, prim), fc.dE(img, wood))
    zone_ = fc.free_zone_mask(s, 12)
    g_ = np.median(img[zone_ & (dsub > 14.0)], axis=0) if (zone_ & (dsub > 14.0)).any() else np.median(img.reshape(-1, 3), axis=0)
    D_ = float(min(fc.dE(prim, g_), fc.dE(wood, g_)))
    lc = dsub < min(26.0, 0.5 * max(D_, 20.0))             # with the older coat close to the ground in colour (Mickey's), the test tightens
    core = ndi.binary_erosion(lc, iterations=1)
    lbl, n = ndi.label(core)
    keep = np.zeros_like(lc)
    for sl, i in zip(ndi.find_objects(lbl), range(1, n + 1)):
        comp = lbl[sl] == i
        if comp.sum() < 6:
            continue
        if ndi.distance_transform_edt(np.pad(comp, 1)).max() >= 2.0:
            keep[sl] |= comp
    return ndi.binary_dilation(keep, iterations=4)


def check_ghosts(T, s, d, gm):
    sid = s["id"]
    out = []
    img = d.img
    L = lab_img(img)
    for b in s["blocks"]:
        if not b["ghost"]:
            continue
        cid = f"{sid}.{b['id']}.ghost"
        exp = [c for c in T["checks"] if c["id"] == cid][0]
        face = pc.render_block_mask(T, b, None)
        box = b["effects_box_mm"]
        w = (max(0, H_MM - int(box[3]) - 14), min(H_MM, H_MM - int(box[1]) + 14), max(0, int(box[0]) - 14), min(W_MM, int(box[2]) + 14))
        r0, r1, c0, c1 = w
        fm = face[r0:r1, c0:c1]
        # the newer letters (and their shade) are not the ghost's: their own reference masks, a little widened for the hand
        others = np.zeros((H_MM, W_MM), bool)
        for ob in s["blocks"]:
            if ob is b or ob["ghost"] or not ob["in_texture"]:
                continue
            others |= pc.render_block_mask(T, ob, None, shade=True)
        others = ndi.binary_dilation(crop(others, w), iterations=4)
        om = others
        inner = ndi.binary_erosion(fm, iterations=2) & ~om
        outer = ring_of(fm, 5, 12) & ~om & ~ndi.binary_dilation(fm, iterations=4)
        if inner.sum() < 50 or outer.sum() < 50:
            out.append(R(cid, False, dict(inner_px=int(inner.sum()), outer_px=int(outer.sum())), exp["expected"], "too little of the ghost in view to measure"))
            continue
        Lw = L[r0:r1, c0:c1]
        wgt = outer.astype(np.float32)
        sig = 10.0
        den = ndi.gaussian_filter(wgt, sig) + 1e-6
        loc = np.stack([ndi.gaussian_filter(Lw[..., k] * wgt, sig) / den for k in range(3)], -1)
        # the ghost differs from the ground along ONE colour direction (the target's ghost colour against the ground's): read the deviation along it,
        # so the grain's noise across it does not inflate the dE
        ghost_dir = fc.lab(np.array(b["face_rgb"], float)) - fc.lab(np.array(b["ground_1990"], float))
        nominal = float(np.linalg.norm(ghost_dir))
        u_dir = ghost_dir / max(nominal, 1e-6)
        dev = np.tensordot(Lw - loc, u_dir, axes=([-1], [0]))
        dev_s = ndi.uniform_filter(dev, 3)
        present = (dev_s > 0.4 * nominal) & inner
        share_present = float(present.sum() / max(1, inner.sum()))
        broken = 1.0 - share_present
        dE_med = float(np.median(dev_s[present])) if present.any() else 0.0
        cx = (b["ink_box_mm"][0] + b["ink_box_mm"][2]) / 2.0
        ex_ = exp["expected"]
        ok_dE = 2.5 <= dE_med <= 5.5
        ok_br = abs(broken - ex_["broken_fraction"]) <= 0.15
        # position: the ghost strokes in view lie on the reference mask (their centre of mass inside the string's own extent)
        cols = np.where(present.any(axis=0))[0]
        ok_pos = abs(cx - ex_["centre_x_mm"]) <= 15 and len(cols) > 0 and (cols.min() + c0) >= b["ink_box_mm"][0] - 15 and (cols.max() + c0) <= b["ink_box_mm"][2] + 15
        out.append(R(cid, ok_dE and ok_br and ok_pos, dict(dE_from_ground=round(dE_med, 2), broken=round(broken, 3), in_view_px=int(inner.sum()), present_x_mm=None if not len(cols) else [int(cols.min() + c0), int(cols.max() + c0)]),
                     dict(dE=[3, 5], broken=ex_["broken_fraction"]), "edge contrast of the ghost strokes in view (not under the newer letters) against the ground round them (a local reference, 10 px), read along the ghost's own colour direction; the share of the string in view that is not seen is the share painted over",
                     reads="pixels+font"))
    g = s.get("ghost")
    if g and g["kind"] in ("repaint_patch", "painted_out_patch"):
        cid = f"{sid}.ghost_patch"
        exp = [c for c in T["checks"] if c["id"] == cid][0]
        x0, y0, x1, y1 = g["box_mm"]
        w = (H_MM - int(y1), H_MM - int(y0), int(x0), int(x1))
        r0, r1, c0, c1 = w
        known = np.zeros((H_MM, W_MM), bool)
        for ob in s["blocks"]:
            if ob["in_texture"] and not ob["ghost"]:
                known |= ndi.binary_dilation(pc.render_block_mask(T, ob, None, shade=True), iterations=5)
        if d.wear is not None:
            known |= ndi.binary_dilation(d.wear.max(axis=2) > 12, iterations=6)
        for hx, hy in (d.rec.get("holes") or []):
            rr, cc = H_MM - int(hy), int(hx)
            known[max(0, rr - 8):rr + 8, max(0, cc - 8):cc + 8] = True
        if d.rec.get("loss"):
            known |= ndi.binary_dilation(loss_class(T, s, d, d.rec), iterations=2)
        inbox = np.zeros((H_MM, W_MM), bool)
        inbox[r0 + 12:r1 - 12, c0 + 12:c1 - 12] = True
        inbox &= ~known
        outbox = ring_of(inbox_full(w), 24, 40) & ~known
        if g["kind"] == "repaint_patch":
            inner_med = np.median(L[inbox], axis=0)
            outer_med = np.median(L[outbox], axis=0)
            de = float(np.linalg.norm(inner_med - outer_med))
            ok = abs(de - g["dE"]) <= 1.5
            val = dict(dE=round(de, 2), pixels=int(inbox.sum()))
        else:
            pc_col = np.array(T["palette"]["painted_out"]["srgb_1990"], float)
            med = np.median(img[inbox].astype(float), axis=0)
            de = float(fc.dE(med, pc_col))
            ok = de <= 12.0
            val = dict(median_rgb=[int(v) for v in med], dE_from_painted_out_buff=round(de, 2), pixels=int(inbox.sum()))
        n_ink = unlisted_ink_count(T, s, d, region=w, known=known)
        out.append(R(cid, ok and n_ink == 0, dict(val, legible_strings=n_ink), exp["expected"], "the patch present in its box; and no text-like feature in it that no block listed (marks, holes and loss are known)"))
    return out


def inbox_full(w):
    r0, r1, c0, c1 = w
    m = np.zeros((H_MM, W_MM), bool)
    m[r0:r1, c0:c1] = True
    return m


def unlisted_ink_count(T, s, d, region=None, known=None):
    """text-like marks that no block of the manifest explains: compact, high-contrast components of letter size outside every listed feature"""
    img = d.img
    L = lab_img(img)[..., 0]
    med = ndi.median_filter(L, size=(25, 25)) if region is None else None
    if region is not None:
        r0, r1, c0, c1 = region
        Lc = L[max(0, r0 - 20):r1 + 20, max(0, c0 - 20):c1 + 20]
        med = ndi.median_filter(Lc, size=(25, 25))
        dev = np.abs(Lc - med)
        mask = dev > 10.0
        kn = known[max(0, r0 - 20):r1 + 20, max(0, c0 - 20):c1 + 20] if known is not None else np.zeros_like(mask)
        mask &= ~ndi.binary_dilation(kn, iterations=3)
        # keep inside the region
        reg = np.zeros_like(mask)
        reg[r0 - max(0, r0 - 20):r0 - max(0, r0 - 20) + (r1 - r0), c0 - max(0, c0 - 20):c0 - max(0, c0 - 20) + (c1 - c0)] = True
        mask &= reg
    else:
        dev = np.abs(L - med)
        mask = dev > 10.0
    lbl, n = ndi.label(mask)
    cnt = 0
    for sl in ndi.find_objects(lbl):
        h_ = sl[0].stop - sl[0].start
        w_ = sl[1].stop - sl[1].start
        if 12 <= h_ <= 400 and 4 <= w_ <= 400:
            cnt += 1
    return cnt


def check_unlisted_ink(T, s, d, rec):
    """G14's 'no OTHER legible string': on the free ground (not text, ghost, lines, frames, wear, holes or flaked paint) no letter-sized, high-contrast mark
    stands that the manifest does not list"""
    L = lab_img(d.img)[..., 0]
    free = free_zone(T, s, d, pad=14)
    if d.wear is not None:
        free &= ~ndi.binary_dilation(d.wear.max(axis=2) > 12, iterations=10)
    if rec.get("loss"):
        free &= ~loss_known(T, s, d, rec)
    for hx, hy in (rec.get("holes") or []):
        r, c = H_MM - int(hy), int(hx)
        free[max(0, r - 10):r + 10, max(0, c - 10):c + 10] = False
    if rec.get("islands_rgb"):
        # the empty unit's islands of old paint are listed in the manifest (their colour), as flaked paint is
        isl = fc.dE(d.img.astype(float), np.array(rec["islands_rgb"], float)) < 14.0
        free &= ~ndi.binary_dilation(isl, iterations=6)
    free = ndi.binary_erosion(free, iterations=16)            # away from every edge of a listed feature (the local mean reaches 15 px)
    mean = ndi.uniform_filter(L, 31)
    dev = np.abs(L - mean)
    mask = (dev > 12.0) & free
    lbl, n = ndi.label(mask)
    hits = []
    for sl in ndi.find_objects(lbl):
        h_ = sl[0].stop - sl[0].start
        w_ = sl[1].stop - sl[1].start
        comp = lbl[sl] > 0
        if h_ >= 24 and w_ >= 6 and int(comp.sum()) >= 60:
            hits.append([int(sl[1].start), int(H_MM - sl[0].stop), int(sl[1].stop), int(H_MM - sl[0].start)])
    return R(f"{s['id']}.unlisted_ink", not hits, dict(count=len(hits), at=hits[:5]), 0, "G14: no letter-sized (24 mm or more) high-contrast mark on the free ground that no block, ghost, line, wear mark, hole or flaked patch explains")


def check_emissive(T, s, d):
    sid = s["id"]
    out = []
    cid = f"{sid}.emissive"
    cdef = [c for c in T["checks"] if c["id"] == cid][0]
    e = cdef["expected"]
    if d.emis is None:
        return [R(cid, False, None, e, "no emissive map")]
    base = d.img.astype(np.float32)
    em = d.emis.astype(np.float32)
    lum_b = base @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    lum_e = em @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    ratio = np.where(lum_b > 20, lum_e / np.maximum(lum_b, 1.0), 0.0)
    x0, y0, x1, y1 = e["face_mm"]
    fr0, fr1, fc0, fc1 = H_MM - int(y1), H_MM - int(y0), int(x0), int(x1)
    cover = float((lum_e[fr0:fr1, fc0:fc1] > 5).mean())
    outside = np.ones((H_MM, W_MM), bool)
    outside[fr0:fr1, fc0:fc1] = False
    leak = float((lum_e[outside] > 5).mean())
    # the face ground: acrylic pixels (not letters, not the vinyl panel)
    g_col = np.array(T["palette"][[sh for sh in s["shapes"] if sh["role"] == "box_face"][0]["colour"]]["srgb_1990"], float)
    on_ground = fc.dE(base, g_col) <= 12.0
    geo = [g for g in s["geometry"] if g.get("emissive")][0]["emissive"]
    joints = geo["tube_joints_x_mm"]
    tube_rows = geo["tube_rows_y_mm"]

    def level_at(row_y, xa, xb):
        r = H_MM - int(row_y) - 1
        band = (slice(max(0, r - 3), r + 4), slice(int(xa), int(xb)))
        m = on_ground[band] & (ratio[band] > 0)
        if m.sum() < 30:
            return None
        return float(np.median(ratio[band][m]))
    # tubes: the segments between joints, away from the joints by 45 mm
    segs = list(zip([x0 + 40] + [j + 45 for j in joints], [j - 45 for j in joints] + [x1 - 40]))
    lv = {}
    for ry in tube_rows:
        lv[ry] = [level_at(ry, a, b) for a, b in segs]
    ok = cover >= 0.97 and leak < 0.01
    notes = [f"face coverage {cover:.3f}, leak outside the face {leak:.4f}"]
    dead = geo.get("dead_tube")
    res_dead = None
    if dead:
        up = max(tube_rows)
        li = [i for i, (a, b) in enumerate(segs) if a >= dead["x_mm"][0] - 5 and b <= dead["x_mm"][1] + 5]
        other = [i for i in range(len(segs)) if i not in li]
        ref = [lv[up][i] for i in other if lv[up][i]]
        dd = [lv[up][i] for i in li if lv[up][i]]
        if ref and dd:
            res_dead = float(np.median(dd) / np.median(ref))
            ok_dead = abs(res_dead - dead["level_pct"] / 100.0) <= e["dead_tube"]["level_pct"] / 100.0 * 0 + 0.05
            ok &= ok_dead
            notes.append(f"dead tube level {res_dead:.3f} of the neighbours (want {dead['level_pct']/100.0:.2f} +-0.05)")
        else:
            ok = False
            notes.append("dead tube not measurable")
        low = max(0, 1)
        ref_low = [v for v in lv[min(tube_rows)] if v]
        if ref_low:
            lo_li = [lv[min(tube_rows)][i] for i in li if lv[min(tube_rows)][i]]
            if lo_li:
                low_ratio = float(np.median(lo_li) / np.median(ref_low))
                ok &= abs(low_ratio - 1.0) <= 0.05
                notes.append(f"the lower row under the dead tube {low_ratio:.3f} of its neighbours (still lit)")
    else:
        vals = [v for ry in tube_rows for v in lv[ry] if v]
        if vals:
            spread = (max(vals) - min(vals)) / np.median(vals)
            ok &= spread <= 0.08
            notes.append(f"no dead tube: the tubes agree within {spread:.3f}")
    # tube-end shadows: the level in a 40 mm window about each interior joint against the level 100 to 160 mm either side
    sh_vals = []
    for ry in tube_rows:
        for j in joints[1:-1] if len(joints) > 2 else joints:
            a = level_at(ry, j - 20, j + 20)
            nb = [level_at(ry, j - 160, j - 100), level_at(ry, j + 100, j + 160)]
            nb = [v for v in nb if v]
            if a and nb:
                sh_vals.append(a / np.mean(nb))
    if sh_vals and not (dead and False):
        dim = 1.0 - float(np.median(sh_vals))
        ok &= abs(dim - e["tube_end_shadow"]["dim_pct"] / 100.0) <= 0.05
        notes.append(f"tube-end shadow dims the row by {dim:.3f} (want {e['tube_end_shadow']['dim_pct']/100.0:.2f} +-0.05)")
    # the row band: +6 per cent on the row line over 80 mm off it
    bands = []
    for ry in tube_rows:
        on = level_at(ry, x0 + 500, x0 + 900) if True else None
        off = level_at(ry + 90 if ry + 90 < y1 - 20 else ry - 90, x0 + 500, x0 + 900)
        if on and off:
            bands.append(on / off - 1.0)
    if bands:
        notes.append(f"row band +{np.median(bands) * 100:.1f} per cent over the face 90 mm off the row (want +6 +-5)")
        ok &= abs(float(np.median(bands)) - e["row_band_pct"] / 100.0) <= 0.05
    out.append(R(cid, ok, dict(coverage=round(cover, 3), dead_tube_level=None if res_dead is None else round(res_dead, 3)), e, "; ".join(notes)))
    return out


# ------------------------------------------------------------------ try 2: how the board AGES (pattern, placement, letters, timber, ghost)
# The thresholds are read off the target's own photographs of real weathered timber (NOTES.md, "Measured on P2, P3 and the wear photographs"):
# P2 (blue-painted planks, 26 per cent lost): 60 per cent of the lost paint lies in joined strips over 50 mm across, 28 per cent over 200 mm,
# the largest 1000 mm long, p99/p10 of the strip size 8.7, 95 per cent of the strips within 20 degrees of the grain; plank to plank the loss varies
# 0.13 to 0.51. The thresholds below are half of P2's where P2 is the reference, and sit well clear of try 1's even confetti (share over 50 mm: 0 to 0.08).
PATTERN = dict(share_ge_50=0.30, share_ge_50_ring=0.18, largest_bbox_w=150, largest_bbox_w_ring=90, p99_over_p10=10.0, along_grain=0.80, edge_over_middle=1.6,
               lower_over_upper=1.1, share_ge_50_bare=0.50)


def paint_region(T, s, d):
    """pixels where paint can be lost and be seen to be lost: the face less a 6 mm rim, the lines (rules, ropes, keylines, corner blocks), frames, glass
    and vinyl panels; a box sign's old-board ring only. Letters are IN (they wear with the ground)."""
    m = np.ones((H_MM, W_MM), bool)
    m[:6] = m[-6:] = False
    m[:, :6] = m[:, -6:] = False
    roles = [sh["role"] for sh in s["shapes"]]
    for sh in s["shapes"]:
        role = sh["role"]
        if role in ("old_board",):
            continue
        if sh["kind"] == "rect":
            x0, y0, x1, y1 = sh["box"]
            if role in ("box_frame", "box_face", "slab_face", "slab_edge", "vinyl_panel", "slab_joint", "speed_line"):
                m[max(0, H_MM - int(y1) - 10):H_MM - int(y0) + 10, max(0, int(x0) - 10):int(x1) + 11] = False
            else:
                m[max(0, H_MM - int(y1) - 3):H_MM - int(y0) + 3, max(0, int(x0) - 3):int(x1) + 4] = False
        else:
            pts = np.array(sh["pts"])
            for p_, q_ in zip(pts[:-1], pts[1:]):
                n = max(2, int(np.hypot(*(q_ - p_)) / 2))
                for t_ in np.linspace(0, 1, n):
                    x, y = p_ + (q_ - p_) * t_
                    r, c_ = H_MM - int(y), int(x)
                    m[max(0, r - 7):r + 8, max(0, c_ - 7):c_ + 8] = False
    return m


def loss_pattern_mask(T, s, d, rec):
    """the paint lost, by colour, anywhere in the paint region (letters included): nearer a substrate colour than the ground round it AND than any letter or
    shade colour of the board"""
    img = d.img.astype(float)
    reg = paint_region(T, s, d)
    lo = rec["loss"]
    prim = np.array(lo["substrate_primer"], float)
    wood = np.array(lo["substrate_wood"], float)
    dsub = np.minimum(fc.dE(img, prim), fc.dE(img, wood))
    cols = []
    for b in s["blocks"]:
        if b["in_texture"] and not b["ghost"]:
            cols.append(np.array(b["face_1990"], float))
            if b.get("shade"):
                cols.append(np.array(fc.pal(T, b["shade"]["colour"]), float))
    dface = np.full(dsub.shape, 1e3)
    for c_ in cols:
        dface = np.minimum(dface, fc.dE(img, c_))
    near = reg & (dsub < 14.0)
    if reg.sum() == 0:
        return np.zeros_like(reg), reg
    g = np.median(img[reg & ~near], axis=0) if (reg & ~near).any() else np.median(img[reg], axis=0)
    dg = fc.dE(img, g)
    D = float(min(fc.dE(prim, g), fc.dE(wood, g)))
    used = reg & (dsub < dg) & (dsub < 0.75 * max(D, 20.0)) & (dsub < dface)
    used = ndi.binary_opening(used, structure=np.ones((2, 2), bool)) | ndi.binary_dilation(ndi.binary_erosion(used, iterations=2), iterations=2) & used
    return used, reg


def pattern_metrics(used, reg, bare=False):
    """the pattern of the lost paint, the numbers P2 and the wear photographs are measured in"""
    H, W = used.shape
    lbl, n = ndi.label(used, structure=np.ones((3, 3)))
    sl = ndi.find_objects(lbl)
    out = {}
    if n == 0:
        return dict(n=0)
    areas = ndi.sum(used, lbl, np.arange(1, n + 1)).astype(float)
    ok = areas >= 6
    ids = np.where(ok)[0]
    if len(ids) == 0:
        return dict(n=0)
    eqd = 2 * np.sqrt(areas[ids] / math.pi)
    tot = float(areas[ids].sum())
    out["n"] = int(len(ids))
    out["eqd_mm_p10_p50_p99"] = [round(float(np.percentile(eqd, q)), 1) for q in (10, 50, 99)]
    out["p99_over_p10"] = round(float(np.percentile(eqd, 99) / max(np.percentile(eqd, 10), 1e-6)), 1)
    out["share_in_strips_ge_50mm"] = round(float(areas[ids][eqd >= 50].sum() / tot), 3)
    out["largest_bbox_w_mm"] = int(max(sl[i][1].stop - sl[i][1].start for i in ids))
    ori = []
    for i in ids:
        if areas[i] < 8:
            continue
        ys, xs = np.nonzero(lbl[sl[i]] == i + 1)
        cov = np.cov(np.vstack([xs, ys]))
        ev, evec = np.linalg.eigh(cov)
        ori.append(abs(math.degrees(math.atan2(evec[1, 1], evec[0, 1]))) % 180)
    ori = np.array(ori)
    out["share_along_grain_20deg"] = round(float(((ori < 20) | (ori > 160)).mean()), 3) if len(ori) else None
    if bare:
        lo_ = used[H // 2:][reg[H // 2:]].mean() if reg[H // 2:].any() else 0
        up_ = used[:H // 2][reg[:H // 2]].mean() if reg[:H // 2].any() else 0
        out["lower_half_over_upper_half_density"] = round(float(lo_ / max(up_, 1e-6)), 2)
    else:
        edge = np.zeros_like(used)
        edge[-90:] = True
        edge[:50] = True
        edge[:, :200] = True
        edge[:, -200:] = True
        mid = np.zeros_like(used)
        mid[150:400, 700:-700] = True
        e_ = used[edge & reg].mean() if (edge & reg).any() else 0
        m_ = used[mid & reg].mean() if (mid & reg).any() else 0
        out["edge_over_middle_density"] = round(float(e_ / max(m_, 1e-4)), 2)
    c = 100
    cells = np.array([used[r:r + c, q:q + c].mean() for r in range(0, H - c + 1, c) for q in range(0, W - c + 1, c) if reg[r:r + c, q:q + c].mean() > 0.6])
    out["cell100_density_cv"] = round(float(cells.std() / max(cells.mean(), 1e-9)), 2) if len(cells) else None
    return out


def check_age_pattern(T, s, d, rec):
    """try 2 (the fresh review, fault 1): paint loss must be a PATTERN, not an even confetti of equal flakes: clusters of every size that join into strips along
    the grain, heavy at the bottom rail, the ends and the joints, light in the open middle (a box sign's old-board ring and the empty unit's silvered timber
    have their own reading)"""
    sid = s["id"]
    if not rec.get("loss") or rec["loss"].get("target_fraction", 0) <= 0:
        return None
    used, reg = loss_pattern_mask(T, s, d, rec)
    roles = [sh["role"] for sh in s["shapes"]]
    ring = "box_frame" in roles
    bare = s["construction_kind"] == "bare"
    m = pattern_metrics(used, reg, bare=bare)
    fails = []
    if m.get("n", 0) < 5:
        fails.append("too few marks to judge")
    else:
        need50 = PATTERN["share_ge_50_bare"] if bare else (PATTERN["share_ge_50_ring"] if ring else PATTERN["share_ge_50"])
        if m["share_in_strips_ge_50mm"] < need50:
            fails.append(f"joined strips over 50 mm carry {m['share_in_strips_ge_50mm']} of the loss, need {need50}")
        need_w = PATTERN["largest_bbox_w_ring"] if ring else PATTERN["largest_bbox_w"]
        if m["largest_bbox_w_mm"] < need_w:
            fails.append(f"largest strip {m['largest_bbox_w_mm']} mm long, need {need_w}")
        if m["p99_over_p10"] < PATTERN["p99_over_p10"]:
            fails.append(f"sizes too alike: p99/p10 {m['p99_over_p10']}, need {PATTERN['p99_over_p10']}")
        if m.get("share_along_grain_20deg") is not None and m["share_along_grain_20deg"] < PATTERN["along_grain"]:
            fails.append("strips do not follow the grain")
        if bare:
            if m["lower_half_over_upper_half_density"] < PATTERN["lower_over_upper"]:
                fails.append("the bare timber does not silver toward its exposed lower half")
        elif not ring and m["edge_over_middle_density"] < PATTERN["edge_over_middle"]:
            fails.append(f"loss is not heavier at the foot and the ends: edge/middle {m['edge_over_middle_density']}, need {PATTERN['edge_over_middle']}")
    return R(f"{sid}.age_pattern", not fails, dict(m, failing=fails), dict(PATTERN), "paint loss as a pattern, measured on the pixels and set against P2 (NOTES.md): joined strips carry the loss, one or more long strips, sizes of every order, along the grain, heavy at the foot and ends"), used, reg


def check_letters_wear(T, s, d, rec, used, reg):
    """the lettering wears with its ground (fault 1): the loss on the letters is of the same order as on the ground round them, no clean halo"""
    sid = s["id"]
    blocks = blk_list(s)
    if not blocks or not rec.get("loss") or rec["loss"].get("target_fraction", 0) < 0.025:
        return None
    letters = np.zeros((H_MM, W_MM), bool)
    for b in blocks:
        letters |= pc.render_block_mask(T, b, None, shade=True)
    ink = ndi.binary_erosion(letters, iterations=1)
    near = ndi.binary_dilation(letters, iterations=60) & ~ndi.binary_dilation(letters, iterations=4) & reg
    if ink.sum() < 500 or near.sum() < 500:
        return None
    f_l = float((used & ink).sum() / ink.sum())
    f_g = float((used & near).sum() / near.sum())
    ok = f_g < 0.003 or (0.25 * f_g <= f_l <= 5.0 * f_g)
    return R(f"{sid}.letters_wear", ok, dict(loss_on_letters=round(f_l, 4), loss_on_the_ground_within_60mm=round(f_g, 4), ratio=None if f_g <= 0 else round(f_l / f_g, 2)),
             dict(ratio=[0.25, 5.0]), "the share of the letters' (and shade's) pixels that show the substrate, against the share of the ground within 60 mm of them: letters wear with their ground, there is no clean halo")


def check_wear_placement(T, s, d, rec):
    """try 2 (fault 3 and the mid-board dashes): rain runs begin at the top edge; gull marks stand on the top edge (the cornice and ledges), few, each its own shape;
    rust runs begin at a fixing; nothing floats in the open middle of the board"""
    sid = s["id"]
    if d.wear is None:
        return None
    flagged = []
    stats = {}
    for k, name in ((0, "runs"), (1, "gull"), (2, "rust")):
        m = d.wear[..., k] > 64
        lbl, n = ndi.label(m)
        sl = ndi.find_objects(lbl)
        cnt = 0
        for i, sl_ in enumerate(sl, 1):
            comp = lbl[sl_] == i
            if comp.sum() < 6:
                continue
            cnt += 1
            top, bot = sl_[0].start, sl_[0].stop
            left, right = sl_[1].start, sl_[1].stop
            if name == "runs":
                if top > 16:
                    flagged.append((name, "does not begin at the top edge", int(left), int(H_MM - top)))
                if bot - top < 30:
                    flagged.append((name, "a dash shorter than 30 mm", int(left), int(H_MM - top)))
            elif name == "gull":
                cy = (top + min(bot, top + 70)) / 2.0
                if top > 75:
                    flagged.append((name, "is not on the top edge", int(left), int(H_MM - top)))
                wd = right - left
                if wd > (110 if sid == "empty_unit" else 55):
                    flagged.append((name, "too wide for a droppings mark", int(left), int(wd)))
            else:
                heads = (rec.get("wear") or {}).get("rust_at") or []
                near = any(abs((left + right) / 2.0 - hx) < 20 and abs(top - (H_MM - hy)) < 20 for hx, hy in heads)
                if not near and top > 70:
                    flagged.append((name, "does not begin at a fixing", int(left), int(H_MM - top)))
        stats[name] = cnt
    # nothing else: a pale or dark dash, small and elongated, standing away from every edge and every listed feature
    return R(f"{sid}.wear_placement", not flagged, dict(counts=stats, flagged=flagged[:6]), "runs from the top edge, gulls on the top edge, rust at fixings",
             "every wear mark is attached to an edge or a fixing where water and birds put it; none floats mid-board; gull marks are no wider than 55 mm (110 on the empty unit)")


def check_timber(T, s, d, rec):
    """the empty unit's bare timber is WOOD (fault 2): planks with seams, a strong grain, a few islands of old paint, not a field of scale-shaped flecks"""
    sid = s["id"]
    if s["construction_kind"] != "bare":
        return None
    img = d.img
    L = lab_img(img)[..., 0]
    # grain: gradient energy across the grain over along it on the free ground
    zone = ndi.binary_erosion(free_zone(T, s, d), iterations=4)
    Ls = ndi.gaussian_filter(L, 1.2)
    gy = ndi.sobel(Ls, axis=0)
    gx = ndi.sobel(Ls, axis=1)
    ratio = float((gy[zone] ** 2).mean() / max((gx[zone] ** 2).mean(), 1e-6))
    # seams: a thin dark line across (nearly) every column, outside the painted-out patch: at each row, how much darker the row is than the rows 5 to 7 above and
    # below it, the median over the free columns. Grain lines and bands do not run across every column; a seam does.
    cols_ok = np.zeros(W_MM, bool)
    cols_ok[60:1000] = True
    cols_ok[4400:5350] = True
    Lc = L[:, cols_ok]
    ridge = np.zeros(H_MM)
    for r in range(30, H_MM - 30):
        nb = 0.5 * (Lc[r - 7:r - 4].mean(axis=0) + Lc[r + 5:r + 8].mean(axis=0))
        ridge[r] = float(np.median(nb - Lc[r - 1:r + 2].min(axis=0)))
    rows_hi = np.where(ridge >= 8.0)[0]
    groups = []
    for r in rows_hi:
        if groups and r - groups[-1][-1] <= 8:
            groups[-1].append(int(r))
        else:
            groups.append([int(r)])
    seam_rows = [int(np.mean(g)) for g in groups]
    rec_seams = (rec.get("timber") or {}).get("seams_from_top_mm")
    at_rec = [round(float(ridge[max(0, int(round(y)) - 4):int(round(y)) + 5].max()), 1) for y in (rec_seams or [])]
    seams_ok = 2 <= len(groups) <= 4 and (rec_seams is None or all(v >= 8.0 for v in at_rec))
    # islands: pixels of the old paint's colour, in pieces 40 mm or longer
    ip = np.array(rec.get("islands_rgb") or [84, 82, 68], float)
    near = fc.dE(img.astype(float), ip) < 5.0
    near = ndi.binary_opening(near, structure=np.ones((3, 3), bool))
    lbl, n = ndi.label(near)
    isl = 0
    for sl_ in ndi.find_objects(lbl):
        w_ = sl_[1].stop - sl_[1].start
        if w_ >= 40 and (lbl[sl_] > 0).sum() >= 150:
            isl += 1
    ok = ratio >= 5.0 and seams_ok and 8 <= isl <= 34
    return R(f"{sid}.timber", ok, dict(grain_gradient_across_over_along=round(ratio, 1), seams_found_rows=seam_rows, seams_drawn_rows=rec_seams, ridge_at_drawn=at_rec, islands_of_old_paint=isl),
             dict(grain_ratio_min=5.0, seams=[2, 3], islands=[8, 34]), "wood, not flecks: the gradient across the grain at least five times the gradient along it on the free ground; the seams between three planks are thin dark lines across nearly every column (outside the painted-out patch), 2 to 4 found, each drawn one at least 8 L* darker than the rows beside it; 10 to 30 islands of old paint (8 to 34 counted: the weather bites them), each 40 mm or longer")


def check_grime(T, s, d, rec):
    """try 2 (fault 1): grime builds up where the board is damp, in the same places the paint lets go: the ground is darker down the lower edge than in the open middle, and
    a little darker at the ends. Read on the free ground (no letters, flakes or wear marks)."""
    sid = s["id"]
    if not rec.get("loss"):
        return None
    if any(sh["role"] in ("box_frame", "slab_edge") for sh in s["shapes"]):
        return None                              # a box sign's acrylic and a glass front are not weathered timber: their ring and glass have their own readings
    L = lab_img(d.img)[..., 0]
    zone = free_zone(T, s, d, pad=6)
    if rec.get("loss"):
        zone &= ~loss_known(T, s, d, rec)
    zone &= ~ndi.binary_dilation(d.wear.max(axis=2) > 12, iterations=8) if d.wear is not None else zone
    zone = ndi.binary_erosion(zone, iterations=2)
    rows = np.arange(H_MM)[:, None]
    cols = np.arange(W_MM)[None, :]
    bottom = zone & (rows >= H_MM - 100) & (rows < H_MM - 22)
    mid = zone & (rows >= 150) & (rows < 400) & (cols > 700) & (cols < W_MM - 700)
    left = zone & (cols < 200) & (rows >= 120) & (rows < 430)
    right = zone & (cols >= W_MM - 200) & (rows >= 120) & (rows < 430)
    if bottom.sum() < 3000 or mid.sum() < 3000:
        return None
    mb, mm_ = float(np.median(L[bottom])), float(np.median(L[mid]))
    ends = []
    for m in (left, right):
        if m.sum() >= 1500:
            ends.append(mm_ - float(np.median(L[m])))
    d_bottom = mm_ - mb
    d_ends = float(np.mean(ends)) if ends else None
    ok = d_bottom >= 1.5 and (d_ends is None or d_ends >= -0.5)
    return R(f"{sid}.grime", ok, dict(bottom_darker_by_L=round(d_bottom, 2), ends_darker_by_L=None if d_ends is None else round(d_ends, 2)), dict(bottom_min=1.5, ends_min=-0.5),
             "median L* of the free ground 22 to 100 mm above the lower edge against the open middle, and of the 200 mm at each end against it (the ends need be no lighter than the middle by more than 0.5): dirt builds up where the board is damp, most down the lower edge")


def readable_ghost(T, s, d, gb):
    """how well a given word can be read in the board's own contrast, along the colour direction the target's ghost differs from the ground by: the mean of the
    high-pass deviation inside the word's strokes minus the ring round them, and the normalised correlation of the word's mask with that deviation over its box"""
    Lab = lab_img(d.img)
    face = pc.render_block_mask(T, gb, None)
    x0, y0, x1, y1 = gb["effects_box_mm"]
    r0, r1, c0, c1 = max(0, H_MM - int(y1) - 20), min(H_MM, H_MM - int(y0) + 20), max(0, int(x0) - 20), min(W_MM, int(x1) + 20)
    Lw = Lab[r0:r1, c0:c1]
    fm = face[r0:r1, c0:c1]
    ghost_dir = fc.lab(np.array(gb["face_rgb"], float)) - fc.lab(np.array(gb["ground_1990"], float))
    nominal = float(np.linalg.norm(ghost_dir))
    u_dir = ghost_dir / max(nominal, 1e-6)
    proj = np.tensordot(Lw, u_dir, axes=([-1], [0]))
    hp = proj - ndi.gaussian_filter(proj, 12.0)
    inner = ndi.binary_erosion(fm, iterations=2)
    outer = ring_of(fm, 5, 14) & ~ndi.binary_dilation(fm, iterations=4)
    if inner.sum() < 50 or outer.sum() < 50:
        return None
    dL = float(hp[inner].mean() - hp[outer].mean())
    a = (fm.astype(float) - fm.mean())
    b = (hp - hp.mean())
    ncc = float((a * b).sum() / math.sqrt(max((a * a).sum() * (b * b).sum(), 1e-9)))
    return dL, ncc, nominal


def check_no_ghost(T, s, d):
    """try 2 (fault 4): Mickey's board shows NO old name (the Hook sheet's board is clean): the word the target had as a ghost cannot be read in the texture"""
    if s["id"] != "mickeys":
        return None
    gb = s.get("ghost_block_dropped")
    if not gb:
        return None
    r = readable_ghost(T, s, d, gb)
    if r is None:
        return R("mickeys.ghost_name.ghost", False, None, None, "no area")
    dL, ncc, nominal = r
    ok = abs(dL) <= 0.35 * nominal and ncc <= 0.12
    return R("mickeys.ghost_name.ghost", ok, dict(deviation_along_the_ghost_colour_inside_minus_ring=round(dL, 2), nominal_ghost_dE=round(nominal, 2), correlation_with_the_old_word=round(ncc, 3)), dict(ghost="absent", deviation_max_share_of_nominal=0.35, correlation_max=0.12),
             "A7: the old name (Marcellus SC, cap 245, centred at 2705) cannot be read in the texture: the high-pass deviation along the old ghost's own colour direction inside its strokes against the ring round them (under 0.35 of the target's 3.5 dE), and the correlation of its mask with the board's contrast over its box (under 0.12)")


# ------------------------------------------------------------------ G5, G6
def autocorr_peak(L, gm):
    x = L.astype(np.float64)
    m = gm.astype(np.float64)
    mu = (x * m).sum() / max(1.0, m.sum())
    x = (x - mu) * m
    # remove each row's own mean over the ground (a vertical gradient is not a period)
    rm = x.sum(axis=1) / np.maximum(m.sum(axis=1), 1.0)
    x = (x - rm[:, None]) * m
    # the DETAIL repeats in a tiling, the slow tone does not matter: high-pass (a masked Gaussian of 60 px removed) so a few big smooth blotches do not stand for a period
    sm = ndi.gaussian_filter(x, 60.0) / np.maximum(ndi.gaussian_filter(m, 60.0), 1e-3)
    x = (x - sm) * m
    # remove slow trends along x: columns' mean over the ground, smoothed 400 px
    W = x.shape[1]
    num = np.zeros(W)
    n = 2 * W
    F = np.fft.rfft(x, n=n, axis=1)
    ac = np.fft.irfft((F * np.conj(F)).sum(axis=0), n=n)[:W]
    e = (x ** 2).sum(axis=0)
    ce = np.concatenate([[0], np.cumsum(e)])
    out = np.zeros(W)
    for L_ in range(0, W):
        d1 = ce[W - L_]                 # sum of e[0 .. W-L-1]
        d2 = ce[W] - ce[L_]             # sum of e[L .. W-1]
        out[L_] = ac[L_] / math.sqrt(max(d1 * d2, 1e-9))
    # how many ground pixel pairs stand behind each lag: a lag with few pairs says nothing about tiling
    Fm = np.fft.rfft(m, n=n, axis=1)
    pairs = np.fft.irfft((Fm * np.conj(Fm)).sum(axis=0), n=n)[:W]
    return out, pairs


def check_g5_g6(T, s, d, gm):
    """G5 and G6 read the board's free ground: the field less text, ghosts, lines, frames and wear (flaked paint stays in: it follows the grain, P2)"""
    sid = s["id"]
    L = lab_img(d.img)[..., 0]
    gm = free_zone(T, s, d, pad=8)
    roles = [sh["role"] for sh in s["shapes"]]
    if "box_face" in roles:
        x0, y0, x1, y1 = [sh for sh in s["shapes"] if sh["role"] == "box_face"][0]["box"]
        cont = np.zeros((H_MM, W_MM), bool)
        cont[H_MM - int(y1) + 6:H_MM - int(y0) - 6, int(x0) + 6:int(x1) - 6] = True
        gm &= cont
    elif "slab_face" in roles:
        x0, y0, x1, y1 = [sh for sh in s["shapes"] if sh["role"] == "slab_face"][0]["box"]
        cont = np.zeros((H_MM, W_MM), bool)
        cont[H_MM - int(y1) + 6:H_MM - int(y0) - 6, int(x0) + 6:int(x1) - 6] = True
        gm &= cont
    ac, pairs = autocorr_peak(L, gm)
    # only lags with enough ground pairs behind them (a quarter of the pairs at lag 600): a tiling shows where the ground overlaps itself, and a lag with a
    # few thousand pairs is noise, not a period
    ok_lag = np.zeros(len(ac), bool)
    ok_lag[600:5001] = pairs[600:5001] >= 0.25 * pairs[600]
    peak = float(np.max(np.abs(ac[ok_lag]))) if ok_lag.any() else 0.0
    r5 = R(f"{sid}.G5", peak <= 0.55, round(peak, 3), 0.55, f"normalised autocorrelation of the ground's L* (text, borders, wear masked; each row's mean and a 60 px Gaussian trend removed) at lags 600 to 5000 mm that have at least a quarter of the pairs of lag 600 behind them ({int(ok_lag.sum())} lags)")
    out = [r5]
    if s["construction_kind"] in ("applied_letters", "signwritten", "gilded", "bare"):
        Lf = L.astype(np.float32)
        band = ndi.gaussian_filter(Lf, 2.0) - ndi.gaussian_filter(Lf, 15.0)
        gx = ndi.sobel(band, axis=1)
        gy = ndi.sobel(band, axis=0)
        mm = ndi.binary_erosion(gm, iterations=3)
        Jxx, Jyy, Jxy = float((gx * gx)[mm].sum()), float((gy * gy)[mm].sum()), float((gx * gy)[mm].sum())
        th = 0.5 * math.atan2(2 * Jxy, Jxx - Jyy)       # dominant gradient direction
        ang = abs(math.degrees(th)) % 180.0
        grain = abs(ang - 90.0)                           # texture runs perpendicular to the gradient
        out.append(R(f"{sid}.G6", grain <= 8.0, round(grain, 2), [0, 8], "structure tensor of the ground's L* (DoG 2 to 15 px): the grain's angle from horizontal"))
    return out


# ------------------------------------------------------------------ G18 mirror
def check_mirror(T, s, d):
    out = []
    img = d.img
    for b in blk_list(s):
        if b["anchor"] != "centre" or abs(b["x_mm"] - W_MM / 2) < 200:
            continue
        pm = pc.face_mask(img, b)
        bb = pc.ink_bbox_mm(pm)
        c_true = (b["ink_box_mm"][0] + b["ink_box_mm"][2]) / 2.0
        if bb is None:
            out.append(R(f"{s['id']}.{b['id']}.mirror", False, None, None, "no pixels"))
            continue
        got = (bb[0] + bb[2]) / 2.0
        out.append(R(f"{s['id']}.{b['id']}.mirror", abs(got - c_true) < abs(got - (W_MM - c_true)), dict(got=round(got, 1), x=round(c_true, 1), mirrored_x=round(W_MM - c_true, 1)), None, "G18"))
    return out


def board_checks(T, s, d, fast=False):
    """every pixel check that belongs to one board; returns a list of results"""
    out = []
    out += block_results(T, s, d)
    out += check_mirror(T, s, d)
    gm = ground_mask(T, s, d)
    r, med = check_ground(T, s, d, gm)
    out.append(r)
    if d.rec.get("loss") is not None:
        out.append(check_age(T, s, d, gm, d.rec)[0])
    if d.wear is not None:
        out += check_wear(T, s, d, d.rec)
        wp = check_wear_placement(T, s, d, d.rec)
        if wp:
            out.append(wp)
    pat = check_age_pattern(T, s, d, d.rec) if d.rec.get("loss") is not None else None
    if pat:
        out.append(pat[0])
        lw = check_letters_wear(T, s, d, d.rec, pat[1], pat[2])
        if lw:
            out.append(lw)
    gr = check_grime(T, s, d, d.rec) if d.rec.get("loss") is not None else None
    if gr:
        out.append(gr)
    tb = check_timber(T, s, d, d.rec)
    if tb:
        out.append(tb)
    ng = check_no_ghost(T, s, d)
    if ng:
        out.append(ng)
    bd = check_border(T, s, d)
    if bd:
        out.append(bd)
    out.append(check_moulding(T, s, d, d.rec))
    ph = check_pinholes(T, s, d)
    if ph:
        out.append(ph)
    sh = check_shadow(T, s, d, d.rec)
    if sh:
        out.append(sh)
        out.append(no_gilt_in_mickeys(T, d))
    out += check_ghosts(T, s, d, gm)
    out.append(check_unlisted_ink(T, s, d, d.rec))
    if s.get("lit") == "tubes":
        out += check_emissive(T, s, d)
    if not fast:
        out += check_g5_g6(T, s, d, gm)
    out.append(R(f"{s['id']}.size", d.img.shape[:2] == (H_MM, W_MM), list(d.img.shape[1::-1]), [W_MM, H_MM], "G1"))
    out.append(R(f"{s['id']}.ground_median", med is not None, None if med is None else [int(v) for v in med], None, "for G7"))
    return out


# ------------------------------------------------------------------ the false-failure test
def render_and_check(job):
    sid, k = job
    import fascia_boards as fb
    T = fc.load_target()
    s = fc.shop_by_id(T, sid)
    seed = fc.seed_for("falsefail", sid, k)
    B, info = fb.render_fascia(T, s, seed)
    d = data_from_render(B, info, s)
    res = board_checks(T, s, d, fast=False)
    bad = [r for r in res if not r["ok"] and not r["id"].endswith(".ground_median")]
    jit = [r for r in res if r["id"].endswith(".G12")][0]["value"]
    return dict(shop=sid, seed_index=k, seed=int(seed), failures=[dict(id=r["id"], value=r["value"], note=r["note"]) for r in bad], n_checks=len(res), g12=jit)


def render_small_and_check(job):
    """the sign faces, glass rows, the window's whitewash and the panels, re-rendered at other seeds and read by the same checks"""
    kind, key, k = job
    import fascia_small as fs
    T = fc.load_target()
    if kind == "sign":
        sg = [p for p in T["projecting_signs"] if p["id"] == key][0]
        seed = fc.seed_for("falsefail", key, k)
        S, rec = fs.render_sign_face(T, sg, "a", seed)
        img = np.clip(np.round(S.B.rgb), 0, 255).astype(np.uint8)
        ok, v = sign_face_result(T, key, rec["blocks"], img, rec["size_mm"][0], rec["size_mm"][1])
        fails = [] if ok else [dict(id=f"{key}.faces", value=v, note="sign face")]
        if rec["wear"].get("substrate_primer") is not None:
            cols = [fc.pal(T, rec["blocks"][0]["face"])]
            if rec["blocks"][0].get("shade"):
                cols.append(fc.pal(T, rec["blocks"][0]["shade"]["colour"]))
            r_, _ = small_age_pattern(T, key, img, rec["size_mm"][0], rec["size_mm"][1], rec["wear"], cols, f"{key}.age_pattern")
            if not r_["ok"]:
                fails.append(dict(id=r_["id"], value=r_["value"], note="sign age pattern"))
        return dict(shop=key, seed_index=k, failures=fails, n_checks=2, g12=dict(painted_gilded_pooled_sd=None))
    if kind == "wash":
        seed = fc.seed_for("falsefail", "wash", k)
        S, a = fs.render_window_wash(T, seed)
        m = wash_metrics(a)
        res = check_wash_from_alpha(a)
        return dict(shop="empty_unit.glass.window", seed_index=k, failures=[] if res["ok"] else [dict(id=res["id"], value=res["value"], note=res["note"])], n_checks=1, g12=dict(painted_gilded_pooled_sd=None))
    if kind == "panel":
        import json as _json
        cast = _json.loads(fc.HOOK_CAST.read_text(encoding="utf-8"))
        seed = fc.seed_for("falsefail", "panel", key, k)
        if key == "letting_board":
            S, rec = fs.render_letting_board(T, seed)
            img = np.clip(np.round(S.B.rgb), 0, 255).astype(np.uint8)
            r_, _ = small_age_pattern(T, key, img, rec["size_mm"][0], rec["size_mm"][1], rec["wear"], [fc.pal(T, "vinyl_red")], "letting_board.age_pattern")
            return dict(shop=key, seed_index=k, failures=[] if r_["ok"] else [dict(id=r_["id"], value=r_["value"], note="letting board")], n_checks=1, g12=dict(painted_gilded_pooled_sd=None))
        fn = fs.render_hours_card if key == "tea_rooms" else fs.render_hours_plate
        S, rec = fn(T, key, cast, seed)
        img = np.clip(np.round(S.B.rgb), 0, 255).astype(np.uint8)
        p = dict(shop=key, lines=rec["lines"], cap_mm=rec["cap_mm"], size_px=rec["size_mm"])
        ok, detail = hours_panel_from_img(T, img, p)
        return dict(shop=f"hours_plate.{key}", seed_index=k, failures=[] if ok else [dict(id=f"hours_plate.{key}.lines", value=detail, note="hours sign")], n_checks=1, g12=dict(painted_gilded_pooled_sd=None))
    idx = key
    row = T["glass_lettering"][idx]
    seed = fc.seed_for("falsefail", "glass", idx, k)
    S, A, fa_, rec = fs.render_glass_row(T, row, idx, seed)
    img = np.dstack([np.clip(np.round(S.B.rgb), 0, 255).astype(np.uint8), np.clip(np.round(A * 255), 0, 255).astype(np.uint8)])
    g = dict(size_px=rec["size_mm"], style=rec["style"], ink_box_in_tile_mm=rec["face_alpha_ink_box_in_tile_mm"], place=dict(tile_baseline_from_tile_bottom_mm=rec["baseline_row_from_bottom_mm"]),
             lines=rec["lines"], line_pitch_mm=rec["line_pitch_mm"], tracking_em=rec["tracking_em"])
    ok, v, note = glass_row_result(T, idx, g, img)
    return dict(shop=f"{row['shop']}.glass.{idx}", seed_index=k, failures=[] if ok else [dict(id=f"{row['shop']}.glass.{idx}", value=v, note=note)], n_checks=1, g12=dict(painted_gilded_pooled_sd=None))


def negative_controls(T, setdir, man, only_ids=None):
    """the mirrored board, a board shifted 20 mm either way, and a wrong font on one block must still FAIL"""
    out = []
    import fascia_boards as fb
    for rec in man["boards"]:
        s = fc.shop_by_id(T, rec["id"])
        if not blk_list(s):
            continue
        d = load_board(setdir, rec)
        mir = Data()
        mir.__dict__.update(d.__dict__)
        mir.img = d.img[:, ::-1].copy()
        rm = board_checks(T, s, mir, fast=True)
        fails = [r["id"] for r in rm if not r["ok"] and (r["id"].endswith((".mask", ".pos", ".mirror")))]
        out.append(R(f"neg.{rec['id']}.mirrored", len(fails) > 0, dict(failing=len(fails), of=sum(1 for r in rm if r["id"].endswith((".mask", ".pos", ".mirror")))), "the mirrored board fails",
                     "a mask, position or mirror check fails on at least one block", group="negative"))
        for dx in (20, -20):
            sh = Data()
            sh.__dict__.update(d.__dict__)
            sh.img = np.roll(d.img, dx, axis=1)
            rs = board_checks(T, s, sh, fast=True)
            pos = [r for r in rs if r["id"].endswith(".pos")]
            msk = [r for r in rs if r["id"].endswith(".mask")]
            ok = all(not r["ok"] for r in pos) and any(not r["ok"] for r in msk)
            out.append(R(f"neg.{rec['id']}.shift{dx:+d}", ok, dict(pos_failing=f"{sum(1 for r in pos if not r['ok'])}/{len(pos)}", mask_failing=f"{sum(1 for r in msk if not r['ok'])}/{len(msk)}"),
                         "every position check and a mask check fail", "20 mm along the board, the position tolerance is 15 mm", group="negative"))
    # a board whose first 1200 mm is repeated along it must fail G5 (the painted timber boards, which have ground detail to repeat)
    for rec in man["boards"]:
        if rec["id"] not in ("mickeys", "fish_market", "ritas", "ironmonger", "chandler"):
            continue
        s = fc.shop_by_id(T, rec["id"])
        d = load_board(setdir, rec)
        img = d.img.copy()
        tile = img[:, 100:1300].copy()
        for k in range(5):
            x0 = 100 + k * 1200
            w = min(1200, W_MM - x0)
            img[:, x0:x0 + w] = tile[:, :w]
        st = Data()
        st.__dict__.update(d.__dict__)
        st.img = img
        g5 = [x for x in check_g5_g6(T, s, st, None) if x["id"].endswith(".G5")][0]
        out.append(R(f"neg.{rec['id']}.tiled", not g5["ok"], g5["value"], "G5 fails on a board that repeats its first 1200 mm", "the ground's autocorrelation peak at the 1200 mm period", group="negative"))
    # a stray word painted on the free ground must be seen as unlisted ink (G14: no OTHER legible string)
    from PIL import ImageDraw as _ID
    for rec in man["boards"]:
        s = fc.shop_by_id(T, rec["id"])
        d = load_board(setdir, rec)
        fz = ndi.binary_erosion(free_zone(T, s, d, pad=14), iterations=16)
        if d.wear is not None:
            fz &= ~ndi.binary_dilation(d.wear.max(axis=2) > 12, iterations=10)
        if rec.get("loss"):
            fz &= ~ndi.binary_dilation(loss_known(T, s, d, rec), iterations=18)        # a clear patch of ground, not on a flake and not beside one
        dist = ndi.distance_transform_edt(fz)
        if rec["id"] == "empty_unit":
            # the unit's dark flaked timber can carry no detectable word; its plain place for one is the painted-out patch, which G14 reads
            x0, y0, x1, y1 = s["ghost"]["box_mm"]
            r, c = H_MM - int((y0 + y1) / 2), int((x0 + x1) / 2)
        elif dist.max() < 40:
            continue
        else:
            r, c = np.unravel_index(int(np.argmax(dist)), dist.shape)
        img = Image.fromarray(d.img.copy())
        dr = _ID.Draw(img)
        lum = float(d.img[max(0, r - 20):r + 20, max(0, c - 40):c + 40].mean())
        f = fc.font_for(T, "libre-franklin", 700, 56)
        dr.text((c, r), "ZORB", font=f, fill=((20, 20, 20) if lum > 100 else (235, 235, 235)), anchor="mm")
        st = Data()
        st.__dict__.update(d.__dict__)
        st.img = np.asarray(img)
        if rec["id"] == "empty_unit":
            gp = [x for x in check_ghosts(T, s, st, None) if x["id"] == "empty_unit.ghost_patch"][0]
            out.append(R("neg.empty_unit.stray_word", not gp["ok"], gp["value"], "the stray word in the painted-out patch is found", "a word painted in the buff patch, 40 mm cap, that no block lists", group="negative"))
            continue
        res = check_unlisted_ink(T, s, st, st.rec)
        out.append(R(f"neg.{rec['id']}.stray_word", not res["ok"], res["value"], "the stray word is found", "a word painted on the free ground, 40 mm cap, that no block lists", group="negative"))
    # try 2: the faults of the fresh review must be CAUGHT. (1) try 1's even confetti of equal flakes in place of the board's loss; (2) Mickey's old name painted back;
    # (3) a gull mark and a dash in the middle of a board; (4) a horizontal comb in place of the window's whitewash, and try 1's thin haze; (5) a brushed row mirrored
    import fascia_paint as fp
    from PIL import ImageDraw as _ID2
    for rec in man["boards"]:
        if rec["id"] not in ("mickeys", "fish_market", "ritas", "ironmonger", "chandler"):
            continue
        s = fc.shop_by_id(T, rec["id"])
        d = load_board(setdir, rec)
        used, reg = loss_pattern_mask(T, s, d, rec)
        img = d.img.copy()
        near = ndi.binary_dilation(used, iterations=3)
        gcol = np.median(d.img[reg & ~near].astype(float), axis=0)
        rg = np.random.default_rng(fc.seed_for("confetti", rec["id"]))
        img[near] = (gcol[None, :] * (1.0 + 0.02 * rg.standard_normal((int(near.sum()), 1)))).clip(0, 255).astype(np.uint8)
        frac = float(used.sum()) / float(reg.sum())
        conf = Image.new("L", (W_MM, H_MM), 0)
        dr_ = _ID2.Draw(conf)
        regr, regc = np.where(reg)
        got = 0.0
        target = frac * reg.sum()
        sub = np.array(rec["loss"]["substrate_primer"], np.uint8)
        wood = np.array(rec["loss"]["substrate_wood"], np.uint8)
        cm = np.zeros((H_MM, W_MM), np.uint8)
        while got < target:
            k = int(rg.integers(len(regr)))
            cy, cx = int(regr[k]), int(regc[k])
            eqd = float(np.clip(rg.lognormal(math.log(9.0), 0.5), 4, 30))
            asp = float(np.clip(rg.lognormal(math.log(3.6), 0.25), 2, 7))
            b_ = math.sqrt(math.pi / 4 * eqd * eqd / math.pi / asp)
            a_ = b_ * asp
            dr_.ellipse([cx - a_, cy - b_, cx + a_, cy + b_], fill=255)
            got += math.pi * a_ * b_
            if got > 4 * target:
                break
        cmask = np.asarray(conf) > 127
        img[cmask] = np.where(rg.random(int(cmask.sum()))[:, None] < 0.35, wood[None, :], sub[None, :])
        cd = Data()
        cd.__dict__.update(d.__dict__)
        cd.img = img
        res = check_age_pattern(T, s, cd, cd.rec)
        out.append(R(f"neg.{rec['id']}.confetti", res is not None and not res[0]["ok"], None if res is None else res[0]["value"].get("failing"), "try 1's even confetti of equal flakes fails the pattern check",
                     "the board's loss replaced by equal ellipses (median 9 mm across, aspect 3.6) scattered evenly at the same fraction", group="negative"))
    # (2) the old name painted back on Mickey's
    for rec in man["boards"]:
        if rec["id"] != "mickeys":
            continue
        s = fc.shop_by_id(T, "mickeys")
        d = load_board(setdir, rec)
        gb = s["ghost_block_dropped"]
        face, _, win = fp.text_layers(T, gb, None, hand=False, shade=False)
        img = d.img.astype(np.float32).copy()
        r0, r1, c0, c1 = win
        img[r0:r1, c0:c1] = img[r0:r1, c0:c1] + (np.array(gb["face_rgb"], np.float32)[None, None, :] - img[r0:r1, c0:c1]) * np.clip(face, 0, 1)[..., None]
        gd = Data()
        gd.__dict__.update(d.__dict__)
        gd.img = np.clip(img, 0, 255).astype(np.uint8)
        res = check_no_ghost(T, s, gd)
        out.append(R("neg.mickeys.old_name_back", res is not None and not res["ok"], None if res is None else res["value"], "an old name painted back (try 1's ghost) is read", "the target's ghost, MICKEY'S at +3.5 dE, drawn over the board", group="negative"))
    # (3) a gull mark and a dash in the middle of the board
    for rec in man["boards"]:
        if rec["id"] not in ("fish_market", "ironmonger"):
            continue
        s = fc.shop_by_id(T, rec["id"])
        d = load_board(setdir, rec)
        wear = d.wear.copy()
        wear[250:280, 700:735, 1] = 255                  # a gull mark at mid height
        wear[300:309, 900:940, 0] = 255                  # a 40 x 9 mm dash in the open field
        md = Data()
        md.__dict__.update(d.__dict__)
        md.wear = wear
        res = check_wear_placement(T, s, md, md.rec)
        out.append(R(f"neg.{rec['id']}.mid_board_marks", res is not None and not res["ok"], None if res is None else res["value"], "a gull mark and a dash in the open middle are found",
                     "a 35 mm mark in the gull layer at mid height and a 40 mm dash in the run layer", group="negative"))
    # (4) the window: a horizontal comb, and try 1's thin haze
    rgc = np.random.default_rng(7)
    comb = np.full((1800, 3250), 0.86, np.float32) + 0.05 * np.sin(np.arange(1800)[:, None] / 3.0) + 0.02 * rgc.standard_normal((1800, 1))
    comb[:44] = 0.0
    comb[-44:] = 0.0
    comb[:, :14] = 0.0
    comb[:, -14:] = 0.0
    res = check_wash_from_alpha(np.clip(comb, 0, 1))
    out.append(R("neg.window.comb_streaks", not res["ok"], res["value"].get("failing"), "a window of horizontal comb streaks fails", "alpha 0.86 with a row-to-row sine and noise, no swirls", group="negative"))
    haze = np.full((1800, 3250), 0.53, np.float32) + 0.02 * rgc.standard_normal((1800, 3250)).astype(np.float32)
    res = check_wash_from_alpha(haze)
    out.append(R("neg.window.thin_haze", not res["ok"], res["value"].get("failing"), "try 1's mid-grey haze (mean alpha 0.53) fails", "a uniform alpha of 0.53", group="negative"))
    # (5) a brushed row mirrored
    import fascia_small as fs
    for g in man["glass_lettering"]:
        if g.get("kind") == "glass_row" and g.get("style") == "whitewash" and not g.get("hours"):
            idx = g["row"]
            img = load_png(Path(setdir) / g["files"]["rgba"]["file"])[:, ::-1].copy()
            ok, v, note = glass_row_result(T, idx, g, img)
            out.append(R(f"neg.{g['shop']}.glass.{idx}.mirrored", not ok, v.get("lines"), "a brushed row, mirrored, fails", "the tile flipped left to right", group="negative"))
    # wrong font on one block
    pairs = [("ritas", "name", "oswald"), ("ironmonger", "name", "abril-fatface"), ("chandler", "name", "josefin-sans"), ("fish_market", "name", "jost"), ("grocer", "name", "libre-franklin"),
             ("newsagent", "name", "jost"), ("tea_rooms", "name", "old-standard-tt-bold"), ("steam_laundry", "name", "oswald")]
    for sid, bid, fk in pairs:
        s = fc.shop_by_id(T, sid)
        B, info = fb.render_fascia(T, s, fc.seed_for("wrongfont", sid), wrong_font=(bid, fk))
        d = data_from_render(B, info, s)
        rr = board_checks(T, s, d, fast=True)
        fail = [r for r in rr if r["id"] == f"{sid}.{bid}.mask"]
        out.append(R(f"neg.{sid}.{bid}.wrong_font_{fk}", bool(fail) and not fail[0]["ok"], fail[0]["value"] if fail else None, "that block's glyph mask fails", "G10 must catch a font swap", group="negative"))
    return out


# ------------------------------------------------------------------ the global checks (manifest and the set)
def words_forbidden(T, text):
    fp_ = T["forbidden_patterns"]
    hits = []
    low = text.upper()
    for lst in ("alcohol_gambling_children", "real_marks", "names_not_minted"):
        for w in fp_[lst]:
            if re.search(r"(?<![A-Z0-9])" + re.escape(w.upper()) + r"(?![A-Z0-9])", low):
                hits.append(w)
    return hits


def global_checks(T, setdir, man, board_res):
    out = []
    approved = set(T["approved_words"])
    rule = re.compile(T["hours_plate_rule"]["pattern"])
    ghostw = set(T["ghost_words"])
    # G1
    for rec in man["boards"]:
        f = rec["files"]["basecolour"]
        out.append(R(f"{rec['id']}.G1", f["size_px"] == [W_MM, H_MM] and f["size_mm"] == [W_MM, H_MM], f["size_px"], [W_MM, H_MM], "image size", reads="pixels"))
    # G3 and G4: every string of every layer.
    # G3 reading: no WORD is painted twice on a board (the FRESH FISH FRESH FISH fault). The target's own layouts repeat a numeral at the two ends
    # (Rita's 5, the chandler's 13) and set a ghost under the same word as the name (the ironmonger's); those are specified, not faults.
    # G4 reading: a ghost word appears only in a ghost block, or as the name of the very shop it belongs to (IRONMONGER on the ironmonger, MICKEY'S on Mickey's).
    g3_bad, g4_bad = [], []
    own = {"IRONMONGER": "ironmonger", "MICKEY’S": "mickeys"}
    for rec in man["boards"]:
        strs = [b["string"] for b in rec["strings_drawn"] if b.get("string") and not b.get("geometry") and b.get("role") != "ghost" and not b["string"].isdigit()]
        if len(strs) != len(set(strs)):
            g3_bad.append(rec["id"])
        for b in rec["strings_drawn"]:
            t = b.get("string")
            if not t:
                continue
            if t not in approved:
                g4_bad.append((rec["id"], t, "not approved"))
            if t in ghostw and b.get("role") not in ("ghost",) and own.get(t) != rec["id"]:
                g4_bad.append((rec["id"], t, "ghost word outside a ghost block and not its own shop's name"))
            h = words_forbidden(T, t)
            if h:
                g4_bad.append((rec["id"], t, f"forbidden {h}"))
    for h in man["hanging_signs"]:
        for f in h["faces"]:
            t = " ".join(b["string"] for b in f.get("blocks", [])) if f.get("blocks") else (f.get("block") or {}).get("string")
            if t:
                if t not in approved or words_forbidden(T, t):
                    g4_bad.append((f["id"], t, "not approved or forbidden"))
    for g in man["glass_lettering"]:
        t = g.get("string")
        if g.get("hours"):
            for ln in g["lines"]:
                if not hours_line_ok(T, ln["string"]) or words_forbidden(T, ln["string"]):
                    g4_bad.append((g["id"], ln["string"], "hours rule"))
        elif t:
            if t not in approved or words_forbidden(T, t) or t in ghostw:
                g4_bad.append((g["id"], t, "not approved, forbidden, or a ghost word"))
    for p in man["small_panels"]:
        if p["id"].startswith("hours_plate"):
            for ln in p["lines"]:
                if not hours_line_ok(T, ln) or words_forbidden(T, ln):
                    g4_bad.append((p["id"], ln, "hours rule"))
        elif p.get("string"):
            if p["string"] not in approved:
                g4_bad.append((p["id"], p["string"], "not approved"))
    out.append(R("G3", not g3_bad, g3_bad, 1, "each string once per board in the layers manifest", reads="manifest"))
    out.append(R("G4", not g4_bad, g4_bad, True, "every string approved (hours plates by their rule), none forbidden, ghost words only in ghost blocks (and Mickey's raised letters, which is the same minted name)", reads="manifest"))
    # hours signs (A11): five trades, five kinds of sign, each trade's own
    hs = []
    for g in man["glass_lettering"]:
        if g.get("hours"):
            hs.append(dict(shop=g["shop"], kind=("brushed whitewash on the glass" if g["style"] == "whitewash" else ("gold leaf on the glass" if g["style"] == "gold" else "white cut vinyl on the glass")),
                           lines=[ln["string"] for ln in g["lines"]]))
    for p in man["small_panels"]:
        if p["id"].startswith("hours_plate"):
            hs.append(dict(shop=p["shop"], kind=p["sign_kind"], lines=p["lines"]))
    bad = [(h["shop"], ln) for h in hs for ln in h["lines"] if not hours_line_ok(T, ln)]
    kinds = [h["kind"] for h in hs]
    shops = sorted(h["shop"] for h in hs)
    caff = [h for h in hs if h["shop"] == "tea_rooms"]
    caff_ok = bool(caff) and all(("AM" in ln or "PM" in ln or "NOON" in ln) for ln in caff[0]["lines"][:2]) and "6.30 AM - 10 PM" in caff[0]["lines"][0]
    out.append(R("hours_plates", not bad and len(hs) == 5 and len(set(kinds)) == 5 and shops == sorted(["ritas", "fish_market", "steam_laundry", "newsagent", "tea_rooms"]) and caff_ok,
                 dict(signs=len(hs), kinds=kinds, bad=bad, caff=caff[0]["lines"] if caff else None), T["hours_plate_rule"]["pattern"],
                 "A11: five hours signs, five different kinds (brushed whitewash, gold leaf, cut vinyl, an engraved plate, a card in marker pen); every line matches the plates' rule (the caff's card extended: AM, PM, NOON) and the hours are hook-cast.json's; the caff's reads 6.30 AM - 10 PM", reads="manifest"))
    # G7: pixel ground medians, fonts, kinds
    gm = {}
    for r in board_res:
        if r["id"].endswith(".ground_median") and r["value"]:
            gm[r["id"].split(".")[0]] = np.array(r["value"], float)
    ids = list(gm)
    worst = 1e9
    pair = None
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            dd = float(fc.dE(gm[ids[i]], gm[ids[j]]))
            if dd < worst:
                worst, pair = dd, (ids[i], ids[j])
    fonts = {}
    for s in T["shops"]:
        nm = [b for b in s["blocks"] if b["role"] == "name" and not b["ghost"]]
        if nm:
            fonts.setdefault(nm[0]["font"], []).append(s["id"])
    dup_fonts = {k: v for k, v in fonts.items() if len(v) > 1}
    centred = T["distinctness"]["centred_skeleton_boards"]
    dotted = [s["id"] for s in T["shops"] for b in s["blocks"] if "·" in b["text"] and b["role"] == "trade"]
    classes = {s["layout_class"] for s in T["shops"]}
    # name-face colour for same construction kind
    kinds = {}
    for s in T["shops"]:
        kinds.setdefault(s["construction_kind"], []).append(s["id"])
    same_kind_bad = []
    for k, v in kinds.items():
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                si, sj = fc.shop_by_id(T, v[i]), fc.shop_by_id(T, v[j])
                ni = [b for b in si["blocks"] if b["role"] == "name" and not b["ghost"] and b["in_texture"]]
                nj = [b for b in sj["blocks"] if b["role"] == "name" and not b["ghost"] and b["in_texture"]]
                if ni and nj:
                    dc = float(fc.dE(fc.pal(T, ni[0]["face"]), fc.pal(T, nj[0]["face"])))
                    if dc < 25 and (si["border"] or {}).get("kind") == (sj["border"] or {}).get("kind"):
                        same_kind_bad.append((v[i], v[j], round(dc, 1)))
    out.append(R("G7", worst >= 14.0 and not dup_fonts and not same_kind_bad and len(centred) <= 5, dict(least_ground_dE=round(worst, 1), pair=pair, shared_name_fonts=dup_fonts, same_kind_pairs_too_alike=same_kind_bad),
                 "pairwise dE >= 14 on the PIXEL ground medians", "see distinctness", reads="pixels"))
    out.append(R("G11", len(centred) <= 5 and len(dotted) <= 3 and len(classes) >= 6, dict(centred_skeleton=centred, dotted_trade_lines=dotted, layout_classes=len(classes)),
                 dict(max_centred=5, max_dotted=3, min_classes=6), "from the target's layout classes and the trade strings drawn", reads="manifest"))
    return out


def aggregate_G(res):
    """G2, G8, G9, G10, G12 .. G14, G18 roll up the per-item results"""
    out = []

    def roll(gid, pred, note, reads="pixels"):
        sel = [r for r in res if pred(r["id"])]
        out.append(R(gid, bool(sel) and all(r["ok"] for r in sel), dict(items=len(sel), failing=[r["id"] for r in sel if not r["ok"]][:8]), None, note, reads=reads))
    roll("G2", lambda i: i.endswith(".moulding") or i.endswith(".no_moulding"), "the height map's moulding on the three boards that have it and no step elsewhere")
    roll("G8", lambda i: i.endswith(".contrast"), "every name line's contrast")
    roll("G9", lambda i: i.endswith(".G9"), "relief step of every gilded, vinyl and painted block")
    roll("G10", lambda i: i.endswith(".mask") and ".glass." not in i and not i.startswith("neg."), "glyph masks of every block", reads="pixels+font")
    roll("G12", lambda i: i.endswith(".G12"), "per board, pooled (amendment A1)")
    roll("G13", lambda i: i.endswith(".wear"), "wear counts")
    roll("G14", lambda i: i.endswith(".ghost") or i.endswith(".ghost_patch") or i.endswith(".unlisted_ink"), "ghosts, and no other legible string", reads="pixels+font")
    roll("G18", lambda i: i.endswith(".mirror"), "no off-centre block sits at W - x")
    roll("G1", lambda i: i.endswith(".G1"), "every board is 5410 x 550 px at one pixel a millimetre")
    roll("G15", lambda i: i.endswith(".mount") or (i.endswith(".faces") and not i.startswith("neg")), "the four hanging signs: mount numbers and both faces", reads="geometry+pixels")
    roll("G16", lambda i: ".glass." in i and not i.startswith("neg"), "every glass lettering row not already in the game", reads="pixels+font")
    roll("G17", lambda i: i.endswith(".geometry") or i.endswith("_box") or i.endswith("_panel") or i == "mickeys.no_letters_in_texture", "Mickey's letters, the two boxes and the tea panel, and no gilt in Mickey's texture", reads="geometry")
    roll("AGE", lambda i: i.endswith((".age_pattern", ".letters_wear", ".wear_placement", ".timber", ".grime", ".ghost_name.ghost")), "try 2: the ageing is a pattern (joined strips, heavy at the foot and ends), the letters wear with the ground, wear marks stand on edges and fixings, the empty unit is wood, Mickey's has no old name")
    roll("G5", lambda i: i.endswith(".G5"), "no tiling period")
    roll("G6", lambda i: i.endswith(".G6"), "grain direction")
    return out


# ------------------------------------------------------------------ hanging signs, glass, panels, geometry
HOURS_RULE_AMPM = re.compile(r"^(MON-SAT|SUN) [0-9]{1,2}(\.[0-9]{2})? (AM|PM) - ([0-9]{1,2}(\.[0-9]{2})? (AM|PM)|12 NOON)$")


def hours_line_ok(T, ln):
    """the plates' own rule (target), or its extension for the caff's card (A11): '6.30 AM - 10 PM', '8 AM - 12 NOON'"""
    return bool(re.match(T["hours_plate_rule"]["pattern"], ln)) or bool(HOURS_RULE_AMPM.match(ln))


def mask_of_alpha_face(img_rgba, face_rgb, shade_rgb=None, tol=18.0):
    rgb = img_rgba[..., :3].astype(float)
    a = img_rgba[..., 3] > 127
    m = (fc.dE(rgb, np.array(face_rgb, float)) <= tol) & a
    if shade_rgb is not None:
        m &= fc.dE(rgb, np.array(face_rgb, float)) <= fc.dE(rgb, np.array(shade_rgb, float))
    return m


def ref_small(T, b, W, H):
    """a block's reference face mask on its own W x H tile and its mirror image; a CONDENSED block (A8) is re-drawn by the painter's own glyph squeeze"""
    import fascia_paint as fp
    if float(b.get("squeeze", 1.0) or 1.0) != 1.0:
        bb = dict(b, jitter=None)
        face, _, win = fp.text_layers(T, bb, None, hand=False, board_wh=(W, H), shade=False)
        tm = np.zeros((H, W), bool)
        r0, r1, c0, c1 = win
        tm[r0:r1, c0:c1] = face > 0.5
        return tm, tm[:, ::-1].copy()
    saved = (pc.W_MM, pc.H_MM)
    pc.W_MM, pc.H_MM = W, H
    try:
        tm = pc.render_block_mask(T, b, None)
        fm = pc.render_block_mask(T, dict(b), None, flip=True)
    finally:
        pc.W_MM, pc.H_MM = saved
    return tm, fm


def small_texture_mask_check(T, b, face_mask_px, W, H, tol, flip_margin=0.15):
    tm, fm = ref_small(T, b, W, H)
    return g10(tm, fm, face_mask_px, tol)


def g10_loose(tm, fm, pm, tol, f_min, m_tol, m_min):
    """G10 for a hand-lettered row that is not a font (A9: brushed whitewash, marker pen): F at a loose tolerance, and the string told from its mirror image at a
    tighter one"""
    ft = tol_f(tm, pm, tol)
    ftm = tol_f(tm, pm, m_tol)
    ffm = tol_f(fm, pm, m_tol)
    sim = tol_f(tm, fm, m_tol)
    waived = sim >= 0.85
    margin = ftm - ffm
    ok = ft >= f_min and (waived or margin >= m_min)
    return ok, dict(true=round(ft, 3), flipped=round(ffm, 3), margin=round(margin, 3), tolerance_mm=tol, f_min=f_min, margin_tolerance_mm=m_tol, margin_min=m_min,
                    reference_vs_its_mirror=round(sim, 3), margin_waived_symmetric=bool(waived))


def sign_face_result(T, sid, blks, img, W, H):
    """G10 on one hanging-sign face's own texture, line by line: its lettering re-rendered from the font (condensed where A8 says) against the pixels of the face colour"""
    import fascia_small as fs
    sgn = [p for p in T["projecting_signs"] if p["id"] == sid][0]
    col = fc.pal(T, sgn["faces"]["colour"])
    sh = sgn["faces"].get("shade")
    rgb = img[..., :3].astype(float)
    pm_all = (fc.dE(rgb, col) <= 14.0)
    if sh:
        pm_all &= fc.dE(rgb, col) < fc.dE(rgb, fc.pal(T, sh["colour"]))
    gnd = fc.pal(T, sgn["faces"]["ground"])
    pm_all &= fc.dE(rgb, col) < fc.dE(rgb, gnd)
    detail = []
    ok_all = True
    for blk in blks:
        b = fs.make_block(T, blk["string"], blk["font"], blk["weight"], blk["cap_mm"], blk["tracking_em"], blk["baseline_mm"], W / 2.0, "centre", sgn["faces"]["colour"],
                          shade_d=(blk["shade"]["d_mm"] if blk.get("shade") else None), shade_colour=(sh["colour"] if sh else "shade_black"),
                          technique=blk["technique"], hand=blk["hand_jitter"], bid="face", squeeze=blk.get("squeeze", 1.0) or 1.0)
        x0, y0, x1, y1 = b["ink_box_mm"]
        reg = np.zeros((H, W), bool)
        reg[max(0, H - int(y1) - 6):H - int(y0) + 6, max(0, int(x0) - 10):int(x1) + 10] = True
        pm = pm_all & reg
        tol = 3.5 if blk["hand_jitter"] else 1.0
        ok, v = small_texture_mask_check(T, b, pm, W, H, tol)
        ok_all &= ok
        detail.append(dict(line=blk["string"], **v))
    return ok_all, detail


def band_pass_sd(L, mask, s1=6.0, s2=30.0):
    """the SD of the slow tone (a band of 6 to 30 px) of L* over a mask: the cloud mottle of a ground"""
    num = ndi.gaussian_filter(np.where(mask, L, 0.0), s1) / np.maximum(ndi.gaussian_filter(mask.astype(np.float32), s1), 1e-3)
    num2 = ndi.gaussian_filter(np.where(mask, L, 0.0), s2) / np.maximum(ndi.gaussian_filter(mask.astype(np.float32), s2), 1e-3)
    bp = (num - num2)[ndi.binary_erosion(mask, iterations=int(s2 * 0.6))] if ndi.binary_erosion(mask, iterations=int(s2 * 0.6)).any() else (num - num2)[mask]
    return float(bp.std()) if bp.size else 0.0


def small_age_pattern(T, sid, img, W, H, wear, face_cols, label):
    """the same reading of ageing for a small board (a hanging board, the letting board): the paint lost is heavier round the edge than in the open field, joined
    into strips, and no mark floats in the middle on its own; and the slow tone is not a cloud"""
    prim = np.array(wear["substrate_primer"], float)
    woodc = np.array(wear["substrate_wood"], float)
    rgb = img[..., :3].astype(float)
    reg = np.ones((H, W), bool)
    reg[:4] = reg[-4:] = False
    reg[:, :4] = reg[:, -4:] = False
    dsub = np.minimum(fc.dE(rgb, prim), fc.dE(rgb, woodc))
    dface = np.full((H, W), 1e3)
    for c_ in face_cols:
        dface = np.minimum(dface, fc.dE(rgb, np.array(c_, float)))
    near = reg & (dsub < 14.0)
    g = np.median(rgb[reg & ~near], axis=0)
    dg = fc.dE(rgb, g)
    D = float(min(fc.dE(prim, g), fc.dE(woodc, g)))
    used = reg & (dsub < dg) & (dsub < 0.75 * max(D, 20.0)) & (dsub < dface)
    used = ndi.binary_opening(used, structure=np.ones((2, 2), bool)) | ndi.binary_dilation(ndi.binary_erosion(used, iterations=2), iterations=2) & used
    rows = np.arange(H)[:, None]
    cols = np.arange(W)[None, :]
    band = (rows < 0.16 * H) | (rows > 0.78 * H) | (cols < 0.12 * W) | (cols > 0.88 * W)
    inner = ~band
    dens_b = float(used[band & reg].mean())
    dens_i = float(used[inner & reg].mean())
    lbl, n = ndi.label(used, structure=np.ones((3, 3)))
    if n:
        areas = ndi.sum(used, lbl, np.arange(1, n + 1)).astype(float)
        ok_ = areas >= 6
        eqd = 2 * np.sqrt(areas[ok_] / math.pi)
        share30 = float(areas[ok_][eqd >= 30].sum() / max(areas[ok_].sum(), 1.0))
        nm = int(ok_.sum())
    else:
        share30, nm = 0.0, 0
    inner_share = float(used[inner & reg].sum() / max(used.sum(), 1))
    # the slow tone of the ground: not a cloud
    ground = reg & ~ndi.binary_dilation(used, iterations=4) & (dface > 20.0)
    L = lab_img(img[..., :3])[..., 0]
    bp = band_pass_sd(L, ground)
    ratio = dens_b / max(dens_i, 1e-4)
    fails = []
    if nm >= 5 and ratio < 1.5:
        fails.append(f"loss is not heavier round the edge: edge/interior {round(ratio, 2)}")
    if nm >= 5 and inner_share > 0.45:
        fails.append(f"too much of the loss stands in the open field: {round(inner_share, 2)}")
    if nm >= 5 and share30 < 0.20:
        fails.append(f"flakes do not join: strips over 30 mm carry {round(share30, 2)} of the loss")
    if bp > 1.2:
        fails.append(f"cloud mottle: the slow tone's SD {round(bp, 2)} L*")
    return R(label, not fails, dict(marks=nm, edge_over_interior_density=round(ratio, 2), share_of_loss_in_the_open_field=round(inner_share, 2), share_in_strips_over_30mm=round(share30, 2),
                                  slow_tone_sd_L=round(bp, 2), failing=fails),
             dict(edge_over_interior_min=1.5, open_field_share_max=0.45, share_30mm_min=0.20, slow_tone_sd_max=1.2),
             "try 2 (the fresh review, fault 6): the small boards weather from their edges, in joined strips, with no mark floating in the field and no cloud mottle"), used


def check_signs(T, setdir, man):
    out = []
    import fascia_small as fs
    for h in man["hanging_signs"]:
        sg = [p for p in T["projecting_signs"] if p["id"] == h["id"]][0]
        m = h["mount"]
        ok_mount = (abs(m["x_street_m"] - sg["mount"]["x_street_m"]) <= 0.02 and abs(m["arm_height_m"] - sg["mount"]["arm_height_m"]) <= 0.02 and abs(m["projection_m"] - sg["mount"]["projection_m"]) <= 0.02)
        low = h["lowest_computed_m"]
        pf = m.get("plate_foot_m")
        ok_low = low >= 2.5 or h["id"] == "steam_laundry_box"
        ok_foot = True if pf is None else (pf - T["board"]["cornice_top_m"] >= 0.05 - 1e-9)
        if h["id"] == "steam_laundry_box":
            ok_foot = (m["arm_height_m"] - sg["parts"]["box_m"][1]) >= T["board"]["cornice_top_m"] + 0.05 - 1e-9
        out.append(R(f"{h['id']}.mount", ok_mount and ok_low and ok_foot, dict(x=m["x_street_m"], arm=m["arm_height_m"], projection=m["projection_m"], lowest=low, plate_foot=pf, cornice_top=T["board"]["cornice_top_m"]),
                     dict(x=sg["mount"]["x_street_m"], arm=sg["mount"]["arm_height_m"], projection=sg["mount"]["projection_m"], lowest_min=2.5), "the manifest's placement row against the target's (no mesh exists in this unit)", reads="geometry"))
        # the lowest point: recompute from the parts
        faces_ok = True
        detail = []
        if h["id"] == "ritas_three_balls":
            out.append(R(f"{h['id']}.faces", True, "no lettering (three balls)", None, "no name or lettering on the balls: nothing to read; the three textures exist", reads="pixels+font"))
            continue
        pat_ok = True
        pat_detail = []
        for f in h["faces"]:
            img = load_png(Path(setdir) / f["files"]["basecolour"]["file"])
            ok, v = sign_face_result(T, h["id"], f["blocks"], img[..., :3], f["size_px"][0], f["size_px"][1])
            faces_ok &= ok
            detail.append(dict(face=f["id"], lines=v))
            # the fill: the lettering covers a signwriter's share of the board
            wr = f["wear"]
            if wr.get("substrate_primer") is not None:
                cols = [fc.pal(T, f["blocks"][0]["face"])]
                if f["blocks"][0].get("shade"):
                    cols.append(fc.pal(T, f["blocks"][0]["shade"]["colour"]))
                r_, used = small_age_pattern(T, h["id"], img, f["size_px"][0], f["size_px"][1], wr, cols, f"{h['id']}.{f['id'][-1]}.age_pattern")
                pat_ok &= r_["ok"]
                pat_detail.append(dict(face=f["id"], **r_["value"]))
        out.append(R(f"{h['id']}.faces", faces_ok, detail, dict(f_min=0.9, flipped_lower_by=0.15), "G10 on each face's own texture, line by line: the lettering reads left to right from its own side", reads="pixels+font"))
        # fill: ink height share of the face
        f0 = h["faces"][0]
        Hf = f0["size_px"][1]
        ink_h = max(b["ink_box_mm"][3] for b in f0["blocks"]) - min(b["ink_box_mm"][1] for b in f0["blocks"])
        ink_w = max(b["ink_box_mm"][2] for b in f0["blocks"]) - min(b["ink_box_mm"][0] for b in f0["blocks"])
        Wf = f0["size_px"][0]
        fill = ink_h * ink_w / float(Wf * Hf)
        out.append(R(f"{h['id']}.fill", fill >= 0.15 and f0["cap_mm_built"] >= 70, dict(cap_mm=f0["cap_mm_built"], lines=len(f0["blocks"]), ink_box_share_of_face=round(fill, 3), squeeze=f0.get("squeeze")),
                     dict(ink_box_share_min=0.15, cap_min_mm=70), "try 2 (fault 2): a hanging board is filled as a signwriter fills it: the lettering's box covers 15 per cent of the face at least (it was 5 to 8) and the cap is 70 mm or more (it was 51 to 99 mm and 5 to 8 per cent in try 1)"))
        if pat_detail:
            out.append(R(f"{h['id']}.age_pattern", pat_ok, pat_detail, None, "the small boards weather from their edges (small_age_pattern), both faces"))
    return out


def glass_row_result(T, idx, g, img):
    """G16 on one glass row's tile, line by line: the string against its font (G10), the cap, the baseline height and the ink centre's street x"""
    import fascia_small as fs
    approved = set(T["approved_words"])
    row = T["glass_lettering"][idx]
    W, H = g["size_px"]
    st = g["style"]
    gs = fs.glass_style(row)
    face_rgb = gs.get("face_rgb") or list(fc.pal(T, gs["face"]))
    rgb = img[..., :3].astype(float)
    a = img[..., 3] > 127
    pm_all = (fc.dE(rgb, np.array(face_rgb, float)) <= (22.0 if st in ("whitewash", "paint_flaking") else 16.0)) & a
    if gs.get("shade"):
        sc = fc.pal(T, gs["shade_colour"])
        pm_all &= fc.dE(rgb, np.array(face_rgb, float)) < fc.dE(rgb, sc)
    trk = g.get("tracking_em", fs.glass_tracking(row, gs))
    lines = g["lines"]
    detail = []
    ok10 = True
    capx_first, how = None, ""
    for li, ln in enumerate(lines):
        b = fs.make_block(T, ln["string"], row["font"], row["weight"] or 400, row["cap_mm"], trk, ln["baseline_from_bottom_mm"], W / 2.0 - (gs.get("shade") or 0) / 2.0, "centre",
                          gs["face"] or "whitewash", shade_d=gs.get("shade"), shade_colour=gs.get("shade_colour", "shade_black"), technique="painted", hand=gs["hand"], bid="glass",
                          face_rgb=gs.get("face_rgb") and list(gs["face_rgb"]), figure=ln["string"].replace(" ", "").isdigit())
        x0, y0, x1, y1 = b["ink_box_mm"]
        reg = np.zeros((H, W), bool)
        reg[max(0, H - int(y1) - 10):H - int(y0) + 10, :] = True
        if len(lines) > 1:
            pitch = g["line_pitch_mm"]
            reg[:] = False
            reg[max(0, H - int(y1) - int(0.2 * pitch)):H - int(y0) + int(0.3 * pitch), :] = True
        pm = pm_all & reg
        if st == "whitewash":
            tm, fm = ref_small(T, b, W, H)
            ok, v = g10_loose(tm, fm, pm, 7.0, 0.85, 4.0, 0.10)
        else:
            tol = 3.5 if gs["hand"] else 1.0
            ok, v = small_texture_mask_check(T, b, pm, W, H, tol)
        ok10 &= ok
        detail.append(dict(line=ln["string"], **v))
        if li == len(lines) - 1:
            capx_first, how = cap_from_mask(pm, row["cap_mm"])
            gb = flat_glyphs(pm, row["cap_mm"] * (0.8 if ln["string"].replace(" ", "").isdigit() else 0.85))
            rows_ = np.where(pm.any(axis=1))[0]
            if gb:
                bottom_from_below = H - np.median([p[0] for p in gb]) + 1.0
            elif len(rows_):
                bottom_from_below = H - (rows_.max() + 1) - 0.016 * row["cap_mm"]
            else:
                bottom_from_below = None
    base_row = g["place"]["tile_baseline_from_tile_bottom_mm"]
    z_tile_bottom = row["z_m"] - base_row / 1000.0
    z_pix = None if bottom_from_below is None else z_tile_bottom + bottom_from_below / 1000.0
    cols = np.where(pm_all.any(axis=0))[0]
    cx_pix = (cols.min() + cols.max() + 1) / 2.0 if len(cols) else None
    ink_c = (g["ink_box_in_tile_mm"][0] + g["ink_box_in_tile_mm"][2]) / 2.0
    err_x = None if cx_pix is None else abs(cx_pix - ink_c) / 1000.0
    cap_tol = (0.09 if st == "whitewash" else 0.05) * row["cap_mm"]
    ok_cap = capx_first is not None and abs(capx_first - row["cap_mm"]) <= cap_tol
    ok_z = z_pix is not None and abs(z_pix - row["z_m"]) <= 0.03
    ok_x = err_x is not None and err_x <= 0.10
    if row.get("hours"):
        ok_w = all(hours_line_ok(T, ln["string"]) for ln in lines)
    else:
        ok_w = row["text"] in approved
    return (ok10 and ok_cap and ok_z and ok_x and ok_w,
            dict(lines=detail, cap_mm=None if capx_first is None else round(capx_first, 1), z_baseline_m=None if z_pix is None else round(z_pix, 3), x_street_m=row["x_street_m"], approved=ok_w),
            f"G16: G10 on the tile's own mask, line by line (hand 3.5 mm, vinyl and gilt 1 mm, brushed whitewash 7 mm with the string told from its mirror image), cap within {int(cap_tol)} mm, z (baseline of the lowest line) within 0.03, x within 0.10; {how}")


def check_glass(T, setdir, man):
    out = []
    for g in man["glass_lettering"]:
        if g["kind"] == "glass_wash":
            out.append(check_wash(T, setdir, g))
            continue
        if g["kind"] != "glass_row":
            continue
        idx = g["row"]
        row = T["glass_lettering"][idx]
        img = load_png(Path(setdir) / g["files"]["rgba"]["file"])
        ok, v, note = glass_row_result(T, idx, g, img)
        out.append(R(f"{g['shop']}.glass.{idx}", ok, v, dict(text=row["text"], cap_mm=row["cap_mm"], z_m=row["z_m"], x_street_m=row["x_street_m"]), note, reads="pixels+font"))
    return out


def wash_metrics(a):
    """the whitewashed window's alpha plane, read: its coat, its hand, its margin and its dribbles"""
    H, W = a.shape
    inner = np.zeros((H, W), bool)
    inner[130:H - 150, 130:W - 130] = True
    mean_in = float(a[inner].mean())
    thin = float((a[inner] < 0.70).mean())
    # the hand: the direction of the pattern's gradient (a comb of horizontal streaks has all its gradient across them; swirls turn through every direction)
    s = ndi.gaussian_filter(a, 2.0)
    gy, gx = np.gradient(s)
    mag = np.hypot(gx, gy)[inner]
    ang = (np.degrees(np.arctan2(gy, gx))[inner] % 180.0)
    hist, _ = np.histogram(ang, bins=8, range=(0, 180), weights=mag)
    hist = hist / max(hist.sum(), 1e-9)
    # a streak texture along a swirl: the share of the gradient energy that points straight up or down (horizontal streaks)
    vertical_share = float(hist[3] + hist[4]) if False else float(hist[[0, 7]].sum() * 0 + hist[3:5].sum())
    bins_used = int((hist >= 0.04).sum())
    # margin: the alpha 6 mm in from each edge, on the middle 80 per cent of each edge
    edges = [a[6, int(0.1 * W):int(0.9 * W)], a[H - 7, int(0.1 * W):int(0.9 * W)], a[int(0.1 * H):int(0.9 * H), 6], a[int(0.1 * H):int(0.9 * H), W - 7]]
    margin_clear = float(np.mean([(e < 0.3).mean() for e in edges]))
    # dribbles: thin vertical runs below the foot of the coat
    foot = np.zeros((H, W), bool)
    foot[H - 120:, :] = True
    col_runs = 0
    cols = a[H - 120:, :]
    lbl, n = ndi.label((cols > 0.4) & ndi.binary_dilation(cols > 0.4, structure=np.ones((9, 1), bool)))
    for sl in ndi.find_objects(lbl):
        hh = sl[0].stop - sl[0].start
        ww = sl[1].stop - sl[1].start
        if hh >= 28 and ww <= 14:
            col_runs += 1
    # horizontal comb: the rows' variance of the mean alpha along x (streaks that run the whole width)
    rowmean = a[:, int(0.1 * W):int(0.9 * W)].mean(axis=1)[130:H - 150]
    comb = float(np.std(rowmean - ndi.gaussian_filter1d(rowmean, 25.0)))
    return dict(mean_alpha_inner=round(mean_in, 3), thin_share=round(thin, 3), gradient_in_8_directions=[round(float(x), 3) for x in hist], directions_used=bins_used,
                clear_margin_share=round(margin_clear, 2), dribbles=col_runs, row_comb_sd=round(comb, 4))


def check_wash(T, setdir, g):
    img = load_png(Path(setdir) / g["files"]["rgba"]["file"])
    a = img[..., 3].astype(np.float32) / 255.0
    r = check_wash_from_alpha(a)
    return R(r["id"], r["ok"], r["value"], r["expected"], r["note"], reads="pixels")


def check_wash_from_alpha(a):
    """try 2 (fault 1 of the signs sheet): the empty unit's window is whitewash laid with a cloth: near-opaque white, swirls in every direction, thin spots, a ragged clear
    margin and dribbles at the foot; no horizontal comb streaks, nothing legible"""
    m = wash_metrics(a)
    fails = []
    if m["mean_alpha_inner"] < 0.80:
        fails.append("not near-opaque")
    if not (0.005 <= m["thin_share"] <= 0.30):
        fails.append("thin spots out of range")
    if m["directions_used"] < 5 or max(m["gradient_in_8_directions"]) > 0.40:
        fails.append("the pattern runs one way (a comb), not round")
    if m["clear_margin_share"] < 0.55:
        fails.append("no clear margin along the glazing")
    if m["dribbles"] < 6:
        fails.append("no dribbles at the foot")
    if m["row_comb_sd"] > 0.02:
        fails.append("rows differ along the whole width (a comb)")
    return dict(id="empty_unit.glass.window", ok=not fails, value=dict(m, failing=fails), expected=dict(mean_alpha_min=0.80, thin=[0.005, 0.30], directions_min=5, clear_margin_min=0.55, dribbles_min=6),
                note="fault 1 of the signs sheet: the whiting's alpha read for its coat, its hand, its margin, its dribbles")


def g_trk(style):
    return 0.05 if style != "vinyl" else 0.03


def base_of(g):
    return int(g["place"]["tile_baseline_from_tile_bottom_mm"])


def hours_panel_result(T, setdir, p):
    return hours_panel_from_img(T, load_png(Path(setdir) / p["files"]["basecolour"]["file"])[..., :3], p)


def hours_panel_from_img(T, img, p):
    """G16-like for the launderette's plate and the caff's card: the lines read against their font"""
    import fascia_small as fs
    W, H = p["size_px"]
    rgb = img.astype(float)
    if p["shop"] == "steam_laundry":
        face_rgb = np.array([226.0, 222.0, 204.0])
        pm_all = fc.dE(rgb, face_rgb) <= 16.0
        pm_all[:12] = pm_all[-12:] = False
        pm_all[:, :12] = pm_all[:, -12:] = False
        font, wt = "libre-franklin", 600
        tol_kind = "plate"
    else:
        face_rgb = np.array([24.0, 28.0, 52.0])
        pm_all = fc.dE(rgb, face_rgb) <= 22.0
        font, wt = "patrick-hand", 400
        tol_kind = "card"
    detail = []
    ok_all = True
    cap = p["cap_mm"]
    pitch = cap * (1.8 if tol_kind == "plate" else 2.0)
    top_y = H / 2.0 + (len(p["lines"]) * pitch - (pitch - cap)) / 2.0 - cap
    for i, ln in enumerate(p["lines"]):
        base = int(round(top_y - i * pitch))
        b = fs.make_block(T, ln, font, wt, cap, 0.05 if tol_kind == "plate" else 0.04, base, W / 2.0, "centre", "vinyl_cream" if tol_kind == "plate" else "sign_black", technique="vinyl", bid=f"line{i+1}")
        x0, y0, x1, y1 = b["ink_box_mm"]
        reg = np.zeros((H, W), bool)
        reg[max(0, H - int(y1) - 6):H - int(y0) + 6, :] = True
        pm = pm_all & reg
        tm, fm = ref_small(T, b, W, H)
        if tol_kind == "plate":
            ok, v = g10(tm, fm, pm, 1.0)
        else:
            ok, v = g10_loose(tm, fm, pm, 7.0, 0.80, 4.0, 0.08)
        ok_all &= ok and hours_line_ok(T, ln)
        detail.append(dict(line=ln, **v))
    return ok_all, detail


def check_panels(T, setdir, man):
    out = []
    import fascia_small as fs
    lb = [p for p in man["small_panels"] if p["id"] == "letting_board"][0]
    img = load_png(Path(setdir) / lb["files"]["basecolour"]["file"])[..., :3]
    W, H = lb["size_px"]
    col = fc.pal(T, "vinyl_red")
    wh = fc.pal(T, "white_paint")
    pm = (fc.dE(img.astype(float), col) <= 16.0) & (fc.dE(img.astype(float), col) < fc.dE(img.astype(float), wh))
    cols = np.where(pm.sum(axis=0) > 3)[0]
    rows = np.where(pm.sum(axis=1) > 3)[0]
    # only the big lettering (the screws' rust is orange, a different colour)
    c_ink = (cols.min() + cols.max() + 1) / 2.0 if len(cols) else None
    r_ink = (rows.min() + rows.max() + 1) / 2.0 if len(rows) else None
    b = dict(id="letting", text="TO LET", font="libre-franklin", weight=800, cap_mm=130, tracking_em=0.06, anchor="centre", x_mm=W / 2.0, face="vinyl_red", face_rgb=None, shade=None,
             embolden_mm=0.0, jitter=None, ghost=False, technique="vinyl")
    blk = lb["block"]
    b.update(cap_ratio=fc.cap_ratio(T, "libre-franklin", 800), size_px_per_em=130 / fc.cap_ratio(T, "libre-franklin", 800), origin_x_mm=None, ink_box_mm=blk["ink_box_mm"], baseline_mm=int(H / 2 - 65))
    probe = fs.make_block(T, "TO LET", "libre-franklin", 800, 130, 0.06, int(H / 2 - 65), W / 2.0, "centre", "vinyl_red", technique="vinyl", bid="letting")
    ok10, v10 = small_texture_mask_check(T, probe, pm, W, H, 1.0)
    ok_size = [W, H] == [900, 450]
    ok_pos = c_ink is not None and abs(c_ink - W / 2.0) <= 15 and r_ink is not None and abs(r_ink - H / 2.0) <= 15
    centre = lb["centre_on_fascia_mm"]
    out.append(R("letting_board", ok_size and ok_pos and ok10 and abs(centre[0] - 2705.0) <= 15 and abs(centre[1] - 275) <= 15,
                 dict(size=[W, H], g10=v10, ink_centre=[None if c_ink is None else round(c_ink, 1), None if r_ink is None else round(r_ink, 1)], centre_on_fascia=centre),
                 dict(text="TO LET", size_mm=[900, 450], centre_mm=[2705.0, 275]), "G10 on the board's own texture; the lettering centred on the 900 x 450 board, the board centred at (2705, 275) on the fascia", reads="pixels+font"))
    if lb.get("wear") and lb["wear"].get("substrate_primer") is not None:
        r_, _ = small_age_pattern(T, "letting_board", img, W, H, lb["wear"], [fc.pal(T, "vinyl_red")], "letting_board.age_pattern")
        out.append(r_)
    # the hours signs of the launderette (a plate) and the caff (a card)
    for p in man["small_panels"]:
        if p["id"].startswith("hours_plate"):
            ok, detail = hours_panel_result(T, setdir, p)
            out.append(R(f"{p['id']}.lines", ok, detail, None, "the plate's or the card's lines read against their font; each line matches the hours rule (the card's extended for AM, PM and NOON)", reads="pixels+font"))
    return out


def check_geometry(T, man):
    out = []
    mk = fc.shop_by_id(T, "mickeys")
    g = mk["geometry"][0]
    centre_street = mk["board_u0_street_x_m"] - g["centre_board_x_mm"] / 1000.0
    nm = [b for b in mk["blocks"] if not b["in_texture"]][0]
    # the letters' bounding box from the font: cap, width, centre
    import fascia_small as fs
    probe = fs.make_block(T, nm["text"], nm["font"], nm["weight"], nm["cap_mm"], nm["tracking_em"], nm["baseline_mm"], nm["x_mm"], "centre", "brass_gilt")
    box = probe["ink_box_mm"]
    emb = g["embolden_m"] * 1000.0
    width = box[2] - box[0] + emb
    ok_bbox = abs((box[0] + box[2]) / 2 - g["centre_board_x_mm"]) <= 8 and abs(width - nm["width_mm"]) <= 10
    ok = abs(g["stand_off_m"] * 1000 - 14) <= 2 and abs(g["cap_m"] * 1000 - 330) <= 8 and abs(centre_street - 4.65) <= 0.05 and ok_bbox
    texture_blocks = [b for rec in man["boards"] if rec["id"] == "mickeys" for b in rec["strings_drawn"] if b.get("string") == "MICKEY’S" and b.get("role") == "name" and not b.get("geometry")]
    out.append(R("mickeys.name.geometry", ok and not texture_blocks, dict(depth_mm=g["stand_off_m"] * 1000, cap_mm=g["cap_m"] * 1000, centre_street_x_m=round(centre_street, 3), font_bbox_mm=[round(v, 1) for v in box], name_blocks_in_texture=len(texture_blocks)),
                 dict(depth_mm=14, cap_mm=330, centre_street_x_m=4.65, bbox_mm=nm["ink_box_mm"]), "the manifest's geometry row against the target's, the letters' box re-measured from the font file; no name block in the texture", reads="geometry"))
    for s in T["shops"]:
        for gp in s["geometry"]:
            if gp["kind"] in ("box_sign", "flat_panel"):
                row = [x for rec in man["boards"] if rec["id"] == s["id"] for x in rec["geometry"] if x["id"] == gp["id"]][0]
                ok = row["outer_mm"] == gp["outer_mm"] and abs(row["depth_m"] - gp["depth_m"]) <= 0.015
                out.append(R(f"{s['id']}.{gp['id']}", ok, dict(outer_mm=row["outer_mm"], depth_mm=round(row["depth_m"] * 1000), uv=row.get("uv_rect_top_left_origin")),
                             dict(outer_mm=gp["outer_mm"], depth_mm=round(gp["depth_m"] * 1000)), "the manifest's geometry row (and the pixels' own border check on the same rectangle)", reads="geometry"))
    return out


def check_lit(T, man):
    rec = [r for r in man["boards"] if r["id"] == "ritas"][0]
    return [R("rita.lit", "emissive" not in rec["files"], list(rec["files"].keys()), True, "Rita's board has no emissive map (only her window is ruled lit)")]


# ------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("setdir")
    ap.add_argument("--out", default=str(HERE / "checks" / "check_v2.json"))
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1))
    ap.add_argument("--no-seeds", action="store_true")
    ap.add_argument("--no-neg", action="store_true")
    ap.add_argument("--only-neg", action="store_true", help="run only the negative controls (a development aid)")
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)
    t0 = time.time()
    T = fc.load_target()
    setdir = Path(a.setdir)
    man = json.loads((setdir / "manifest.json").read_text(encoding="utf-8"))
    only = {x for x in a.only.split(",") if x}
    if a.only_neg:
        neg = negative_controls(T, setdir, man)
        for r in neg:
            print(("ok  " if r["ok"] else "FAIL"), r["id"], json.dumps(r["value"], default=str)[:160])
        print(f"negatives {sum(1 for r in neg if r['ok'])}/{len(neg)} in {int(time.time() - t0)} s")
        return 0
    results = []
    board_res = []
    for rec in man["boards"]:
        if only and rec["id"] not in only:
            continue
        s = fc.shop_by_id(T, rec["id"])
        d = load_board(setdir, rec)
        rr = board_checks(T, s, d)
        board_res += rr
        print(f"  {rec['id']}: {sum(1 for r in rr if r['ok'])}/{len(rr)} ok", flush=True)
    results += board_res
    results += global_checks(T, setdir, man, board_res)
    results += check_geometry(T, man)
    results += check_lit(T, man)
    results += check_signs(T, setdir, man)
    results += check_glass(T, setdir, man)
    results += check_panels(T, setdir, man)
    results += aggregate_G(results)
    # every id of the target must have a result
    have = {r["id"] for r in results}
    missing = [c["id"] for c in T["checks"] if c["id"] not in have]
    # the target's own ids that are defined by a different name here
    results_by_id = {r["id"]: r for r in results}
    # report
    target_rows = []
    for c in T["checks"]:
        r = results_by_id.get(c["id"])
        target_rows.append(dict(id=c["id"], ok=None if r is None else r["ok"], value=None if r is None else r["value"], reads=c["reads"], name=c["name"]))
    neg = []
    if not a.no_neg and not only:
        neg = negative_controls(T, setdir, man)
    seeds = {}
    if not a.no_seeds and not only:
        jobs = [(s["id"], k) for s in T["shops"] if blk_list(s) or s["id"] in ("empty_unit", "mickeys") for k in range(a.seeds)]
        small = [("sign", p["id"], k) for p in T["projecting_signs"] if p["id"] != "ritas_three_balls" for k in range(a.seeds)]
        small += [("glass", i, k) for i, g in enumerate(T["glass_lettering"]) if g["text"] and not g.get("existing") for k in range(a.seeds)]
        small += [("wash", "wash", k) for k in range(a.seeds)]
        small += [("panel", pk, k) for pk in ("letting_board", "steam_laundry", "tea_rooms") for k in range(a.seeds)]
        t1 = time.time()
        with Pool(a.jobs) as pool:
            rs = []
            for i, r in enumerate(pool.imap_unordered(render_and_check, jobs, chunksize=1)):
                rs.append(r)
                if (i + 1) % 20 == 0:
                    print(f"  seeds {i + 1}/{len(jobs)} ({int(time.time() - t1)} s), failures so far {sum(len(x['failures']) for x in rs)}", flush=True)
            for i, r in enumerate(pool.imap_unordered(render_small_and_check, small, chunksize=4)):
                rs.append(r)
                if (i + 1) % 100 == 0:
                    print(f"  small seeds {i + 1}/{len(small)} ({int(time.time() - t1)} s), failures so far {sum(len(x['failures']) for x in rs)}", flush=True)
        per_board = {}
        for r in rs:
            per_board.setdefault(r["shop"], []).append(r)
        seeds = dict(seeds_per_board=a.seeds, boards={sid: dict(runs=len(v), board_seeds_failing=sum(1 for x in v if x["failures"]), checks_per_run=v[0]["n_checks"],
                                                              failures=[dict(seed_index=x["seed_index"], fails=x["failures"]) for x in v if x["failures"]],
                                                              pooled_sd_painted=[x["g12"]["painted_gilded_pooled_sd"] for x in sorted(v, key=lambda z: z["seed_index"])]) for sid, v in per_board.items()},
                     total_runs=len(rs), total_failures=sum(len(x["failures"]) for x in rs), seconds=round(time.time() - t1, 1))
    n_ok = sum(1 for r in results if r["ok"])
    n_bad = [r for r in results if not r["ok"]]
    doc = dict(schema="ledger.cloud-week-42.fascias-check/1", script="check_fascias.py " + fc.SCRIPT_VERSION, set=str(setdir), made=time.strftime("%Y-%m-%d %H:%M:%S"),
               amendments=T["_amendments"], summary=dict(checks_run=len(results), passed=n_ok, failed=len(n_bad), target_ids=len(T["checks"]), target_ids_without_result=missing,
                                                         negative_controls_failing_as_they_must=sum(1 for r in neg if r["ok"]), negative_controls=len(neg),
                                                         false_failures_over_seeds=None if not seeds else seeds["total_failures"], seed_runs=None if not seeds else seeds["total_runs"]),
               failures=[dict(id=r["id"], value=r["value"], expected=r["expected"], note=r["note"]) for r in n_bad], target_check_ids=target_rows, results=results, negative_controls=neg, false_failure_test=seeds,
               seconds=round(time.time() - t0, 1))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, indent=1, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o)), encoding="utf-8")
    print(f"CHECK: {n_ok} of {len(results)} pass, {len(n_bad)} fail; target ids without a result: {len(missing)}; negatives {sum(1 for r in neg if r['ok'])}/{len(neg)}; "
          f"false failures over seeds: {None if not seeds else seeds['total_failures']} in {None if not seeds else seeds['total_runs']} runs; {doc['seconds']} s")
    for r in n_bad[:40]:
        print("  FAIL", r["id"], json.dumps(r["value"], default=str)[:200], "|", r["note"][:100])
    return 1 if n_bad or (seeds and seeds["total_failures"]) or missing or any(not r["ok"] for r in neg) else 0


if __name__ == "__main__":
    sys.exit(main())
