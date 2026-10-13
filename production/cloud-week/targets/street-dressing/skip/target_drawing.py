"""skip: draws the target from target.json alone: elevations, plan and sections as filled polygons in millimetres
(target_drawing.json) and, with a folder on the command line, as pictures; and the end marking plates flat, with their stripes
(skip-marking-plates.png and the stripes' polygons in target_drawing.json under "marking_plates").
Usage: python target_drawing.py [PICTURE_DIR]"""
import json
import math
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L


def plate_stripes(T):
    """The red stripes of ONE plate, in its own frame (u across from the plate's INNER edge outward, v down from its upper edge),
    as polygons clipped to the plate: red where ((v - d tan(angle)) - breadth/2) mod period lies within breadth/2 of zero (the stripes
    fall toward the outer edge, as Schedule 1 shows)."""
    ch = T["marking"]["chosen"]
    w, ln = ch["plate_width_mm"], ch["plate_length_mm"]
    t = math.tan(math.radians(ch["stripe_angle_deg"]))
    b, per = ch["stripe_breadth_mm"], ch["stripe_period_mm"]
    from shapely.geometry import Polygon, box
    plate = box(0.0, 0.0, w, ln)
    out = []
    k = -4
    while k * per < ln + w * t + per:
        # the stripe's upper edge at the inner edge (d = 0): v = k * per; it falls t per mm toward the outer edge (d = w)
        poly = Polygon([(0.0, k * per), (w, k * per + w * t), (w, k * per + w * t + b), (0.0, k * per + b)])
        g = poly.intersection(plate)
        if not g.is_empty and g.area > 1.0:
            for q in ([g] if g.geom_type == "Polygon" else list(g.geoms)):
                out.append([[round(x, 2), round(y, 2)] for x, y in q.exterior.coords])
        k += 1
    return plate, out


def draw_plates(T, outdir=None):
    ch = T["marking"]["chosen"]
    plate, stripes = plate_stripes(T)
    res = {"plate_mm": [ch["plate_width_mm"], ch["plate_length_mm"]], "frame": "u from the inner edge outward, v down from the upper edge", "red_stripes": stripes,
           "red_srgb": T["materials"]["marking_red_yellow"]["stripe_srgb"], "yellow_srgb": T["materials"]["marking_red_yellow"]["srgb"]}
    if outdir:
        from PIL import Image, ImageDraw
        os.makedirs(outdir, exist_ok=True)
        s, pad = 1.2, 40
        w, ln = ch["plate_width_mm"], ch["plate_length_mm"]
        W = int(2 * w * s + 3 * pad)
        H = int(ln * s + 2 * pad)
        im = Image.new("RGB", (W, H), (250, 250, 248))
        d = ImageDraw.Draw(im)
        # the two plates of an end as seen from outside: the left plate's inner edge on its right, the right plate's on its left
        for k, inner_right in enumerate((True, False)):
            x0 = pad + k * (w * s + pad)
            d.rectangle([x0, pad, x0 + w * s, pad + ln * s], fill=tuple(res["yellow_srgb"]), outline=(30, 30, 30))
            for poly in stripes:
                pts = []
                for u, v in poly:
                    xx = (w - u) if inner_right else u          # inner edge on the right for the left plate
                    pts.append((x0 + xx * s, pad + v * s))
                d.polygon(pts, fill=tuple(res["red_srgb"]))
            d.rectangle([x0, pad, x0 + w * s, pad + ln * s], outline=(30, 30, 30))
        d.text((6, 4), "skip end marking plates, flat (mm: %d x %d; stripes %d degrees, %d broad, rising toward the inner edges)" % (w, ln, ch["stripe_angle_deg"], ch["stripe_breadth_mm"]), fill=(0, 0, 0))
        p = os.path.join(outdir, "skip-marking-plates.png")
        im.save(p)
        res["picture"] = p
    return res


if __name__ == "__main__":
    out = L.drawing_main(HERE, sys.argv[1:])
    T = json.load(open(os.path.join(HERE, "target.json")))
    mp = draw_plates(T, sys.argv[1] if len(sys.argv) > 1 else None)
    out["marking_plates"] = {k: v for k, v in mp.items() if k != "picture"}
    json.dump(out, open(os.path.join(HERE, "target_drawing.json"), "w"))
    print("skip: the marking plates drawn flat (%d red stripe polygons)%s" % (len(mp["red_stripes"]), "; " + mp["picture"] if mp.get("picture") else ""))
