"""sd_photo: crops, masks and the target-on-photo overlay, for the previews of a family (JPEG, 1200 px at most, under 300 KB)."""
import io
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import sd_lib as L
import sd_check as K


def save_limited(im, path, max_side=1200, max_kb=290):
    im = im.convert("RGB")
    if max(im.size) > max_side:
        f = max_side / float(max(im.size))
        im = im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS)
    for q in (88, 82, 76, 70, 62, 55, 48):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True)
        if len(buf.getvalue()) / 1024 < max_kb:
            break
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(buf.getvalue())
    return im.size, len(buf.getvalue()) / 1024


def blur_boxes(im, boxes, radius=9):
    im = im.copy()
    for b in boxes:
        reg = im.crop(b).filter(ImageFilter.GaussianBlur(radius))
        im.paste(reg, b)
    return im


def fill_boxes(im, boxes, colour=None):
    im = im.copy()
    d = ImageDraw.Draw(im)
    for b in boxes:
        c = colour
        if c is None:
            reg = np.asarray(im.crop((max(b[0] - 6, 0), max(b[1] - 6, 0), b[2] + 6, b[3] + 6)).convert("RGB"), float)
            c = tuple(int(v) for v in np.median(reg.reshape(-1, 3), axis=0))
        d.rectangle(b, fill=c)
    return im


def overlay(im, T, ph, outlines=True, features=True):
    """Draw the variant's projected parts (view of the photograph) on the photograph, at the fitted scale."""
    V = ph.get("variant", T["sample"])
    ps = K._ps_cache(L.variant_parts(T, V))
    fit = ph["fit"]
    lo_ref, hi_ref = ps.bbox(only=fit.get("parts"))
    s = (fit["y_bottom_px"] - fit["y_top_px"]) / (hi_ref[2] - lo_ref[2])
    view = ph.get("view", "front")
    ax, sign = L.view_axes(view)
    cx = sign * (lo_ref[ax] + hi_ref[ax]) / 2.0
    d = ImageDraw.Draw(im)
    r, u, f = [np.array(a, float) for a in L.VIEWS[view]]
    polys = []
    for p in ps.parts:
        g = L.project_part(ps, p["id"], view)
        if g is None:
            continue
        for q in ([g] if g.geom_type == "Polygon" else list(g.geoms)):
            pts = []
            for x, z in q.exterior.coords:
                pts.append((fit["x_centre_px"] + (x - cx) * s, fit["y_bottom_px"] - (z - lo_ref[2]) * s))
            polys.append((p, pts))
    if outlines:
        for p, pts in polys:
            col = (255, 150, 0) if p.get("transparent") else (255, 30, 30)
            d.line(pts + [pts[0]], fill=col, width=1)
    if features:
        for ft in ph["features"]:
            col = (0, 230, 60)
            if ft["axis"] == "y":
                d.line([(ph["object_box"][0] - 12, ft["px"]), (ph["object_box"][0] - 2, ft["px"])], fill=col, width=1)
                d.line([(ph["object_box"][2] + 2, ft["px"]), (ph["object_box"][2] + 12, ft["px"])], fill=col, width=1)
            else:
                d.line([(ft["px"], ph["object_box"][1] - 12), (ft["px"], ph["object_box"][1] - 2)], fill=col, width=1)
                d.line([(ft["px"], ph["object_box"][3] + 2), (ft["px"], ph["object_box"][3] + 12)], fill=col, width=1)
    return im
