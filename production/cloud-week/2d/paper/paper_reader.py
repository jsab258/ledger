"""paper_reader.py: the independent half of the check: an item's RGB picture back into the ink masks the target's reader takes (unit 4.2 to 4.4, cloud week 42).

Nothing here imports the maker's drawing code. The flat reference is drawn again from target.json alone with PIL (the stock, the art's nominal colour, every shape in its aged colour,
the scrims); a pixel belongs to a block's ink when its nearest colour, among every colour the item can show (CIE76), is the block's aged ink and not the ground the flat reference
puts there. That is the target's own definition of the ink mask ("nearer the block's aged ink than its aged ground").
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import paper_common as pc


def flat_reference(sc, P, item, cls, tau=1.0):
    """(rgb float (h, w, 3), alpha bool): the item with no lettering, flat colours, drawn from the target alone."""
    ppm = float(item["px_per_mm"])
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    w, h = int(round(W * ppm)), int(round(H * ppm))
    rgb = np.zeros((h, w, 3), np.float32)
    if item["stock"]:
        rgb[:] = np.asarray(P.stock(item["stock"], cls, tau), np.float32)
    for a in item["art"]:
        x0, y0, x1, y1 = a["box_mm"]
        rgb[int((H - y1) * ppm):int((H - y0) * ppm), int(x0 * ppm):int(x1 * ppm)] = np.asarray(P.paint_rgb(a["nominal_rgb"], cls), np.float32)
    for b in item["blocks"]:                      # the target's guarantee: the picture is the block's `on art:` colour in a zone 10 mm round the line
        if b.get("ghost") or not str(b["on"]).startswith("art:"):
            continue
        zc = tuple(int(v) for v in b["on"].split(":", 1)[1].split(","))
        x0, y0, x1, y1 = b["ink_box_mm"]
        rgb[int((H - y1 - 10) * ppm):int((H - y0 + 10) * ppm), int((x0 - 10) * ppm):int((x1 + 10) * ppm)] = np.asarray(P.paint_rgb(zc, cls), np.float32)
    alpha = np.ones((h, w), bool)

    def X(x):
        return x * ppm

    def Y(y):
        return (H - y) * ppm

    def col_of(s):
        k, f = s.get("fill_kind"), s.get("fill")
        if k == "ink":
            return P.ink(f, item["stock"], cls, tau)
        if k == "paint":
            return P.paint(f, cls)
        if k == "stock" or f == "paper":
            return P.stock(item["stock"], cls, tau) if item["stock"] else None
        return {"black": P.ink("black", item["stock"], cls, tau), "white": P.stock("white_card", cls, tau), "buff_card": P.stock("buff_card", cls, tau), "brass": P.paint("brass", cls)}.get(f)
    for s in item["shapes"]:
        kind = s["kind"]
        if kind == "star":
            im = Image.new("L", (w, h), 0)
            ImageDraw.Draw(im).polygon([(X(px), Y(py)) for px, py in s["pts_mm"]], fill=255)
            alpha &= np.asarray(im) > 127
            continue
        if kind == "scrim":
            x0, y0, x1, y1 = s["box_mm"]
            r0, r1 = int((H - y1) * ppm), int((H - y0) * ppm)
            c0, c1 = int(x0 * ppm), int(x1 * ppm)
            n = r1 - r0
            t = np.linspace(0, 1, n)[:, None, None]
            a_ = (s["alpha_top"] + (s["alpha_bottom"] - s["alpha_top"]) * t)
            rgb[r0:r1, c0:c1] = rgb[r0:r1, c0:c1] * (1 - a_) + np.asarray(s["rgb"], np.float32) * a_
            continue
        if kind == "roundel" and s["id"] == "hole":
            im = Image.new("L", (w, h), 0)
            bx = s["box_mm"]
            ImageDraw.Draw(im).ellipse([X(bx[0]), Y(bx[3]), X(bx[2]), Y(bx[1])], fill=255)
            alpha &= ~(np.asarray(im) > 127)
            continue
        col = col_of(s)
        if col is None:
            continue
        im = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(im)
        bx = s.get("box_mm")
        if kind in ("rect", "rule") and bx:
            d.rectangle([X(bx[0]), Y(bx[3]), X(bx[2]) - 1, Y(bx[1]) - 1], fill=255)
        elif kind == "frame":
            wd = max(1, int(round(s.get("width_mm", 3) * ppm)))
            d.rectangle([X(bx[0]), Y(bx[3]), X(bx[2]) - 1, Y(bx[1]) - 1], outline=255, width=wd)
        elif kind == "roundel" and bx:
            d.ellipse([X(bx[0]), Y(bx[3]), X(bx[2]), Y(bx[1])], fill=255)
        elif kind == "ring":
            cx, cy = s["centre_mm"]
            ro, ri = s["r_outer_mm"], s["r_inner_mm"]
            d.ellipse([X(cx - ro), Y(cy + ro), X(cx + ro), Y(cy - ro)], fill=255)
            d.ellipse([X(cx - ri), Y(cy + ri), X(cx + ri), Y(cy - ri)], fill=0)
        elif kind == "poly" and s.get("pts_mm"):
            d.polygon([(X(px), Y(py)) for px, py in s["pts_mm"]], fill=255)
        elif kind == "ticks":
            for sg in s["segments_mm"]:
                d.line([(X(sg["p0"][0]), Y(sg["p0"][1])), (X(sg["p1"][0]), Y(sg["p1"][1]))], fill=255, width=max(1, int(round(s.get("width_mm", 2) * ppm))))
        elif kind == "hand":
            cx, cy = s["centre_mm"]
            ang = s.get("angle_deg")
            if ang is None:
                ang = 60.0 if s.get("pointing") == "by variant" else 0.0
            a = math.radians(ang)
            ex, ey = cx + s["length_mm"] * math.sin(a), cy + s["length_mm"] * math.cos(a)
            d.line([(X(cx), Y(cy)), (X(ex), Y(ey))], fill=255, width=max(1, int(round(s["width_mm"] * ppm))))
            r = s["width_mm"] * ppm / 2          # the target's "rounded end" (the reference drew a square one, and the tip of K02's hour hand read as stray ink)
            for px, py in ((X(cx), Y(cy)), (X(ex), Y(ey))):
                d.ellipse([px - r, py - r, px + r, py + r], fill=255)
        m = np.asarray(im) > 127
        if kind == "rule":          # the compositor's rule: a rule that runs through a line of lettering is cut 2 mm round it (the maker does the same; NOTES.md)
            for b in item["blocks"]:
                if b.get("ghost"):
                    continue
                x0, y0, x1, y1 = b["ink_box_mm"]
                m[int((H - y1 - 2.0) * ppm):int((H - y0 + 2.0) * ppm), int((x0 - 2.0) * ppm):int((x1 + 2.0) * ppm)] = False
        rgb[m] = np.asarray(col, np.float32)
    return rgb, alpha


def item_palette(P, item, cls, tau=1.0):
    """Every colour the item can show: {name: rgb} (ink keys, ground colours, the stock)."""
    q = {}
    if item["stock"]:
        q["stock"] = np.asarray(P.stock(item["stock"], cls, tau), float)
    for b in item["blocks"]:
        if b.get("ghost"):
            continue
        q["ink:" + b["ink"]] = np.asarray(P.ink(b["ink"], item["stock"], cls, tau), float)
        q["on:" + str(b["on"])] = np.asarray(P.ground(item, b["on"], cls, tau), float)
    for s in item["shapes"]:
        k, f = s.get("fill_kind"), s.get("fill")
        if k == "ink":
            q["shape:" + f] = np.asarray(P.ink(f, item["stock"], cls, tau), float)
        elif k == "paint":
            q["shape:" + f] = np.asarray(P.paint(f, cls), float)
    return q


def tape_region(sc, P, item, cls, tau=1.0):
    """(mask, filter) of the tabs of yellowed tape the item carries, drawn from the target's own tab spec: a tab is a translucent filter, so a pixel under it is read after dividing by the
    filter (the filter is what turns bare stock into the target's tape colour at the target's opacity). None when the item has no tab."""
    ppm = float(item["px_per_mm"])
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    tabs = pc.tab_layout(sc.T, item, cls)
    if not tabs:
        return None
    polys = [pc.tape_polygon(c, ppm, H, spec, fxx, fyy) for c, fxx, fyy, spec in tabs]
    spec = tabs[0][3]
    w, h = int(round(W * ppm)), int(round(H * ppm))
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    for p in polys:
        d.polygon(p, fill=255)
    stock = np.asarray(P.stock(item["stock"], cls, tau), np.float32)
    tape = np.asarray(spec["rgb"], np.float32)
    f = (spec["opacity"] * tape + (1 - spec["opacity"]) * stock) / np.maximum(stock, 1.0)
    return np.asarray(im) > 127, f


def block_masks(sc, P, item, rgb, cls, ref, tau=1.0, alpha=None, tape=True, despeckle=False):
    """{block id: bool mask in the block's glyph window}: the pixels whose nearest colour among the item's is the block's ink and which the flat reference says are ground."""
    ppm = float(item["px_per_mm"])
    tape = tape_region(sc, P, item, cls, tau) if tape else None
    q = item_palette(P, item, cls, tau)
    names = list(q)
    cols = np.stack([q[n] for n in names])
    out = {}
    lab_q = pc.lab_of(cols)
    h, w = rgb.shape[:2]
    for b in item["blocks"]:
        if b.get("ghost"):
            continue
        x0, x1, y0, y1 = sc.glyph_window(item, b, (h, w), ppm)
        sub = rgb[y0:y1, x0:x1]
        if tape is not None:
            tm = tape[0][y0:y1, x0:x1]
            if tm.any():
                sub = sub.copy()
                sub[tm] = np.clip(sub[tm] / tape[1][None, :], 0, 255)
        lab = pc.lab_of(sub).astype(np.float32)
        ink_col = q["ink:" + b["ink"]]
        d_ink = np.full(lab.shape[:2], 1e9, np.float32)
        d_other = np.full(lab.shape[:2], 1e9, np.float32)
        ink_lab = pc.lab_of(ink_col)
        for i, c in enumerate(cols):
            dq = np.sqrt(((lab - lab_q[i].astype(np.float32)) ** 2).sum(-1))
            if np.sqrt(((lab_q[i] - ink_lab) ** 2).sum()) < 12.0:        # two inks of one item that a person cannot tell apart (felt black, ballpoint black) are one colour here
                d_ink = np.minimum(d_ink, dq)
            else:
                d_other = np.minimum(d_other, dq)
        m = d_ink <= d_other
        # the pixels where the flat reference already shows this colour (a shape of the same ink) are the shape's, not the lettering's
        m &= (np.abs(ref[y0:y1, x0:x1] - ink_col[None, None, :]).max(-1) > 8)
        if alpha is not None:
            m &= alpha[y0:y1, x0:x1]
        if despeckle and m.any():
            # a copier's toner speckle (the target: 0.15 to 0.4 mm across, i.e. under 0.13 mm2) is not lettering: components under 0.12 mm2 (and at least 3 pixels) are dropped before reading
            lab_, n_ = ndi.label(m, structure=np.ones((3, 3)))
            area = np.bincount(lab_.ravel())
            small = area < max(3.5, 0.12 * ppm * ppm)
            small[0] = False
            m &= ~small[lab_]
        full = np.zeros((h, w), bool)
        full[y0:y1, x0:x1] = m
        out[b["id"]] = full
    return out


def union_mask(masks, shape=None):
    """The union of the blocks' masks; an item with no legible block (F02: only ghosts) gives an empty mask of `shape` (a StopIteration here once ended the check's pool early)."""
    vals = list(masks.values())
    if not vals:
        return np.zeros(shape, bool) if shape is not None else None
    u = vals[0].copy()
    for m in vals[1:]:
        u |= m
    return u
