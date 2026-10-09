"""Glyph kernels shared by make_target.py (to choose each item's pixel scale) and self_check.py (to read pixels).

Nothing here reads target.json. A caller passes `font_fn(key, weight, px)` (a PIL ImageFont at px pixels per em).

THE PROBLEM THIS ANSWERS (TARGET-REVIEW fault 1). The first try compared whole lines against their font re-render with a
1 mm (print) or 2.5 mm (hand) tolerance: a changed date, TEA for ALE or LUNCH for BINGO scored F 0.94 to 1.00 and passed. A
single glyph is a small part of a line, so the line score cannot see it. The check below reads ONE GLYPH AT A TIME.

Three numbers, all in pixels of the item's own render:

  F       mean of recall and precision of the read ink against the glyph re-rendered from the manifest, each against the
          other dilated 0.5 mm (TARGET-REVIEW's figure). A true glyph scores 0.85 or more.
  SEP     a pairwise score of the read ink between the claimed glyph and ONE alternative glyph. A = pixels only the claimed
          glyph inks (not within the tolerance of the alternative); B = pixels only the alternative inks. SEP is the share of
          the A and B pixels together on which the read ink sides with the claimed glyph (an A pixel it covers, a B pixel it
          leaves bare). 1.0: the read ink is the claimed glyph. 0.0: it is the alternative. The claimed glyph "out-scores" the alternative by 2 x SEP - 1; the gate is
          SEP 0.70, i.e. a margin of 0.40 where TARGET-REVIEW asked for 0.05.
  N       |A| + |B|. Below N_MIN (8 pixels) the two glyphs cannot be told apart at that scale, and the item's scale is raised.

WHY NOT THE F MARGIN THE REVIEW WORDED. F is a mean over the whole glyph, so two glyphs that share most of their ink score alike:
O against D in Oswald 700 at 34 mm capitals scores 0.987 against the true glyph's 1.000, a margin of 0.013, and 6 against 8
0.036 (glyph_table() in self_check.py prints the table). A margin of 0.05 on F cannot be met by 11 of 36 capitals and digits
even at that size, and by most of them at 8 mm. SEP looks only at the pixels where the two glyphs differ, which is where the
decision is made.
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

GLYPHS = ([chr(c) for c in range(65, 91)] + [chr(c) for c in range(97, 123)] + list("0123456789") +
          list("£.,'’-—–&·?:!"))
N_MIN = 8           # pixels: fewer and two glyphs are not told apart
TOL_PX = 1          # alignment tolerance of the separation score, in pixels (never more than 1)
F_MIN = 0.85        # TARGET-REVIEW: F at 0.5 mm dilation
SEP_GATE = 0.70     # the claimed glyph's pairwise score
TWIN_MM2 = 0.03     # two glyphs that differ by less than this area at 24 px/mm are shape twins (I and l, ' and ’ at small sizes)
EXPLICIT_TWINS = {("I", "l"), ("l", "I"), ("'", "’"), ("’", "'")}   # capital I and small L are one shape in the sans faces; a straight and a curly apostrophe differ by under 0.1 mm
BIG_EM_PX = 150.0   # glyphs bigger than this are compared at a reduced scale (differences are large there)
_ST8 = ndi.generate_binary_structure(2, 2)


def disk(r):
    r = int(r)
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r + 0.5


def dil(a, n):
    """Dilation by n pixels with the 3 x 3 square (what ndi.binary_dilation(a, 3x3, iterations=n) gives), by shifts: the same pixels, several times faster on the small arrays the glyph reader works on."""
    n = int(n)
    if n <= 0 or not a.any():
        return a
    d = a
    for _ in range(n):
        e = d.copy()
        e[:, 1:] |= d[:, :-1]
        e[:, :-1] |= d[:, 1:]
        f = e.copy()
        f[1:, :] |= e[:-1, :]
        f[:-1, :] |= e[1:, :]
        d = f
    return d


def ero(a, n=1):
    """Erosion by n pixels with the 3 x 3 square (the dilation of the background)."""
    return ~dil(~a, n)


def sliver_only(A, B, n=1):
    """True when the pixels in which a glyph and its mirror differ are slivers (nothing thicker than 2n pixels survives an erosion by n and fewer than N_MIN pixels remain): such a glyph is its
    own mirror for any viewer (an M or an A whose two diagonals differ by an edge) and its mirror is not scored."""
    return int(ero(A, n).sum()) + int(ero(B, n).sum()) < N_MIN


def glyph_patch(font_fn, key, weight, ch, em_mm, ppm, rot_deg=0.0, emb_mm=0.0, tight=False):
    """The glyph as a boolean patch. Returns (patch, ox, base): the pen origin and the baseline in patch pixels (ox from the left, base from the top).
    em_mm: the em in millimetres. rot_deg: counter-clockwise about (origin + half the advance, baseline). emb_mm: radius of added stroke.
    tight: cut the patch to the ink (plus what a turn and a stroke add) BEFORE turning it, which gives the same pixels much faster; ox and base are then relative to the cut patch
    (every caller that places a patch by ox and base is unaffected; family() needs the common frame and does not ask for it)."""
    em = em_mm * ppm
    f = font_fn(key, weight, em)
    pad = int(em * 0.35) + 4
    adv = f.getlength(ch)
    W = int(adv + 1.0 * em + 2 * pad)
    H = int(em * 1.9) + 2 * pad
    asc = int(em * 1.25) + pad
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).text((pad + em * 0.1, asc), ch, font=f, fill=255, anchor="ls")
    ox = pad + em * 0.1
    cx0 = cy0 = 0
    r = int(round(emb_mm * ppm))
    if tight:
        bb = im.getbbox()
        if bb is None:
            return np.zeros((1, 1), bool), 0.0, 0
        m = int(math.ceil(max(bb[2] - bb[0], bb[3] - bb[1]) * math.sin(math.radians(min(abs(rot_deg), 30.0))))) + 3 + max(0, r) + 2
        cx0, cy0 = max(0, bb[0] - m), max(0, bb[1] - m)
        im = im.crop((cx0, cy0, min(W, bb[2] + m), min(H, bb[3] + m)))
        # the cut must not clip what the turn moves: bring the rotation centre along
    if abs(rot_deg) > 1e-9:
        im = im.rotate(rot_deg, center=(ox + adv / 2.0 - cx0, asc - cy0), resample=Image.BILINEAR)
    a = np.asarray(im) > 100
    if r >= 1:
        a = ndi.binary_dilation(a, disk(r))
    return a, ox - cx0, asc - cy0


def place_patch(patch, ox, base, x_px, y_px, win):
    """Paste patch (pen origin at ox, base) so that its origin falls at canvas pixel (x_px, y_px); return the window (x0, x1, y0, y1) of the canvas as an array."""
    x0, x1, y0, y1 = win
    out = np.zeros((y1 - y0, x1 - x0), bool)
    px0 = int(round(x_px - ox))
    py0 = int(round(y_px - base))
    h, w = patch.shape
    sx0, sy0 = max(0, x0 - px0), max(0, y0 - py0)
    sx1, sy1 = min(w, x1 - px0), min(h, y1 - py0)
    if sx1 > sx0 and sy1 > sy0:
        out[py0 + sy0 - y0:py0 + sy1 - y0, px0 + sx0 - x0:px0 + sx1 - x0] = patch[sy0:sy1, sx0:sx1]
    return out


def ink_cols(a):
    c = np.where(a.any(axis=0))[0]
    return (int(c.min()), int(c.max())) if len(c) else None


def mirror_in_place(a):
    """The array's ink flipped left-right about its own ink centre line."""
    c = ink_cols(a)
    if c is None:
        return a
    m = np.zeros_like(a)
    m[:, c[0]:c[1] + 1] = a[:, c[0]:c[1] + 1][:, ::-1]
    return m


def fscore(read, ref, tol_px):
    """Mean of recall and precision, each against the other dilated tol_px."""
    if not ref.any():
        return 0.0
    rd = dil(read, tol_px)
    fd = dil(ref, tol_px)
    recall = (ref & rd).sum() / max(1, ref.sum())
    prec = (read & fd).sum() / max(1, read.sum()) if read.any() else 0.0
    return float((recall + prec) / 2.0)


def sep_sets(ref_c, ref_a, tol_px=TOL_PX):
    dc, da = dil(ref_c, tol_px), dil(ref_a, tol_px)
    return ref_c & ~da, ref_a & ~dc


def sep_score(read, A, B, tol_px=TOL_PX, read_d=None):
    """1.0 when the read ink is the claimed glyph, 0.0 when it is the alternative; None when A and B hold fewer than N_MIN pixels.
    The share of the differing pixels (A and B together) on which the read ink sides with the claimed glyph: a pixel of A counts when the read ink (dilated tol_px) covers it,
    a pixel of B when the read ink leaves it bare. read_d: the read ink already dilated by tol_px (the same for every alternative of one glyph)."""
    na, nb = int(A.sum()), int(B.sum())
    if na + nb < N_MIN:
        return None
    dr = dil(read, tol_px) if read_d is None else read_d
    good = int((A & dr).sum()) + nb - int((B & read).sum())
    return float(good / (na + nb))


def family(font_fn, key, weight, em_mm, ppm, chars, rot_deg=0.0, emb_mm=0.0):
    """Patches of every glyph in `chars` (that the font really has) on one common canvas with one common origin, so that they can be compared pixel to pixel."""
    pats = {}
    nd, _, _ = glyph_patch(font_fn, key, weight, "\ue000", em_mm, ppm, rot_deg, emb_mm)
    for c in chars:
        p, o, b = glyph_patch(font_fn, key, weight, c, em_mm, ppm, rot_deg, emb_mm)
        if p.shape == nd.shape and np.array_equal(p, nd) and c != " ":
            continue                      # the font has no glyph for c: its notdef box is not an alternative
        pats[c] = (p, o, b)
    Hh = max(v[0].shape[0] for v in pats.values())
    Ww = max(v[0].shape[1] for v in pats.values())
    out = {}
    for c, (p, o, b) in pats.items():
        z = np.zeros((Hh, Ww), bool)
        z[:p.shape[0], :p.shape[1]] = p
        out[c] = z
    return out


def _corners(jit):
    """The jitter extremes a hand style reaches (3.5 sd of its size, 3.5 sd of its rotation, all four combinations) and the unjittered glyph."""
    if not jit:
        return [(1.0, 0.0)]
    s, r = 3.5 * jit.get("size_sd", 0.0), 3.5 * jit.get("rotation_sd_deg", 0.0)
    return [(1.0, 0.0), (1.0 + s, r), (1.0 + s, -r), (1.0 - s, r), (1.0 - s, -r)]


def separation_table(font_fn, key, weight, cap_mm, cap_ratio, ppm, chars, glyphs=GLYPHS, emb_mm=0.0, jit=None):
    """For each used char, the worst (smallest) |A|+|B| against any alternative that is not a shape twin, plus the twins found, and the same against its mirror.
    With jit (a hand style's size_sd and rotation_sd_deg) every pair is measured at the unjittered glyph and at the four corners of the jitter at 3.5 sd (the claimed glyph and
    the alternative are drawn alike: the checker draws both from the same manifest entry) and the smallest count stands.
    Returns dict(worst={char: (n, alt)}, twins=[(c, a)...], mirror={char: n}, ppm_eval=...)."""
    em0 = cap_mm / cap_ratio
    ppm_eval = ppm
    if em0 * ppm > BIG_EM_PX:
        ppm_eval = ppm * BIG_EM_PX / (em0 * ppm)
    allc = sorted(set(glyphs) | (set(chars) - {" "}))
    worst, twins, mirror = {}, [], {}
    for sc_, rot in _corners(jit):
        em_mm = em0 * sc_
        pats = family(font_fn, key, weight, em_mm, ppm_eval, allc, rot_deg=rot, emb_mm=emb_mm)
        dpat = {c: dil(p, TOL_PX) for c, p in pats.items()}
        tw_p = tw_d = None
        for c in sorted(set(chars) - {" "}):
            if c not in pats:
                continue
            best = None
            for a in allc:
                if a == c or a not in pats:
                    continue
                if (c, a) in EXPLICIT_TWINS:
                    twins.append((c, a))
                    continue
                n = int((pats[c] & ~dpat[a]).sum() + (pats[a] & ~dpat[c]).sum())
                if n < N_MIN:
                    if em_mm * 24.0 <= 400:
                        if tw_p is None:
                            tw_p = family(font_fn, key, weight, em_mm, 24.0, allc)
                            tw_d = {k: dil(v, 2) for k, v in tw_p.items()}
                        n2 = ((tw_p[c] & ~tw_d[a]).sum() + (tw_p[a] & ~tw_d[c]).sum()) / (24.0 * 24.0)
                    else:
                        n2 = 1e9
                    if n2 < TWIN_MM2:
                        twins.append((c, a))
                        continue
                if best is None or n < best[0]:
                    best = (n, a)
            if best is not None and (c not in worst or worst[c] is None or best[0] < worst[c][0]):
                worst[c] = best
            elif c not in worst:
                worst[c] = best
            m = mirror_in_place(pats[c])
            mn = int((pats[c] & ~dil(m, TOL_PX)).sum() + (m & ~dpat[c]).sum())
            mirror[c] = min(mirror.get(c, mn), mn)
    return dict(worst=worst, twins=sorted(set(twins)), mirror=mirror, ppm_eval=ppm_eval)


def needed_ppm(font_fn, key, weight, cap_mm, cap_ratio, chars, cands=(2, 3, 4, 6, 8, 12, 16), emb_mm=0.0, jit=None):
    """The smallest candidate scale at which every used char is told from every non-twin alternative by at least N_MIN pixels. For a hand style pass jit
    (size_sd, rotation_sd_deg): each pair is then measured over glyphs jittered to 3.5 sd of that style (separation_table), and the scale rises until the worst corner holds."""
    last = None
    for ppm in cands:
        t = separation_table(font_fn, key, weight, cap_mm, cap_ratio, ppm, chars, emb_mm=emb_mm, jit=jit)
        ok = all(v is None or v[0] >= N_MIN for v in t["worst"].values())
        last = (ppm, t)
        if ok:
            return ppm, t
    return None, last[1]


def paste_or(canvas, patch, ox, base, x_px, y_px):
    """OR the patch into canvas (row 0 = top) so that its pen origin falls at (x_px, y_px)."""
    px0 = int(round(x_px - ox))
    py0 = int(round(y_px - base))
    h, w = patch.shape
    H, W = canvas.shape
    sx0, sy0 = max(0, -px0), max(0, -py0)
    sx1, sy1 = min(w, W - px0), min(h, H - py0)
    if sx1 > sx0 and sy1 > sy0:
        canvas[py0 + sy0:py0 + sy1, px0 + sx0:px0 + sx1] |= patch[sy0:sy1, sx0:sx1]


def shrink_cov(a, k, thr=0.4):
    """Area reduction by an integer factor: a reduced pixel is ink when at least `thr` of its k x k block is ink. This is how a glyph drawn straight at the reduced scale looks
    (the glyph reader's reference is drawn straight at the reduced scale), where shrink() fattens every edge by up to a reduced pixel."""
    if k <= 1:
        return a
    h, w = a.shape
    h2, w2 = h // k * k, w // k * k
    if h2 == 0 or w2 == 0:
        return a[:1, :1]
    return a[:h2, :w2].reshape(h2 // k, k, w2 // k, k).mean(axis=(1, 3)) >= thr


def shrink(a, k):
    """Block-max reduction by an integer factor (any ink in the block)."""
    if k <= 1:
        return a
    h, w = a.shape
    h2, w2 = h // k * k, w // k * k
    if h2 == 0 or w2 == 0:
        return a[:1, :1]
    return a[:h2, :w2].reshape(h2 // k, k, w2 // k, k).any(axis=(1, 3))
