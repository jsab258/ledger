"""The hours on a shop's door (14 October 2026, try 2; the ironmonger's close review, narrow 7; the brief's step 0 k).

Rita's approved front carries its hours on the shop door's lower pane: 4.1's glass row 24 (old standard bold, cap 34 mm, gold leaf with a 3 mm black shade, three lines MON-SAT / WED / SUN CLOSED).
4.1 drew an hours sign for some shops (the launderette's engraved plate, the cafe's card: small panels the front places under the OPEN card), a glass row for the newsagent, and none for the ironmonger.
`ensure(ctx)` makes the ironmonger's: Rita's row re-lettered with the shop's own hours (target `hours`), by 4.1's own renderer (imported, nothing in 4.1's folders is written or changed), written into the
shop's own copy of the 4.1 outputs (SCRATCH/shop-windows/<shop>/fascias, glass/<shop>/) and added to that copy's manifest as a glass row marked `hours_like_ritas`, which sw_front places where Rita's stands (the
door's lower pane, z base 1040 plus the baseline, d 39). Idempotent. The row's number (90) is a row of the shop's copy only.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FASC = os.path.join(REPO, "production", "cloud-week", "2d", "fascias")
ROW_ID = 90


def _t(h):
    h12 = h if h <= 12 else h - 12
    whole = int(h12)
    frac = int(round((h12 - whole) * 60))
    return "%d" % whole if frac == 0 else "%d.%02d" % (whole, frac)


def hours_lines(R):
    """MON-SAT, the early-closing day and Sunday, in 4.1's own format (8.30-5.30; the afternoon hour as 12 hour figures)."""
    hrs = R["hours"]
    mon = hrs["mon"]
    lines = ["MON-SAT %s-%s" % (_t(mon[0]), _t(mon[1]))]
    for d_, nm in (("wed", "WED"), ("thu", "THU"), ("sat", "SAT")):
        h = hrs.get(d_)
        if h and h != mon:
            lines.append("%s %s-%s" % (nm, _t(h[0]), _t(h[1])))
    sun = hrs.get("sun")
    lines.append("SUN CLOSED" if not sun else "SUN %s-%s" % (_t(sun[0]), _t(sun[1])))
    return lines


def ensure(ctx, log=print):
    """Make the shop's hours row if the shop has no hours sign and no hours glass row; returns the manifest row or None."""
    man_p = os.path.join(ctx.fascias, "manifest.json")
    man = json.load(open(man_p))
    if any(g["shop"] == ctx.id and g.get("hours") for g in man["glass_lettering"]):
        return None
    if any(p.get("id") == "hours_plate." + ctx.id for p in man.get("small_panels", [])):
        return None
    if not ctx.R.get("hours"):
        return None
    sys.path.insert(0, FASC)
    import numpy as np
    from PIL import Image
    import fascia_common as fc
    import fascia_small as fs
    import make_fascias as mf
    T = fc.load_target()
    g = dict(T["glass_lettering"][24])
    assert g["shop"] == "ritas" and g.get("hours")
    lines = hours_lines(ctx.R)
    g.update(shop=ctx.id, hours=False, lines=lines, text=" | ".join(lines), x_street_m=float(ctx.R["front"]["centres_street_x_m"]["shop_door"]), surface="shop-door glass (hours; Rita's row 24 re-lettered, try 2)",
             source="14 Oct, try 2 (ironmonger close review, narrow 7): the hours on the shop door like Rita's approved front", kind="Judgement")
    seed = fc.seed_for("glass", 1, "hours", ctx.id)
    S, A, face_alpha, rec = fs.render_glass_row(T, g, ROW_ID, seed)
    W, H = rec["size_mm"]
    base = np.dstack([mf.u8(S.B.rgb), mf.u8(A * 255.0)])
    stem = "%02d_hours-%s" % (ROW_ID, ctx.id)
    files = {"rgba": mf.save(ctx.fascias, "glass/%s/%s_rgba.png" % (ctx.id, stem), base, "sRGB 8-bit + straight alpha (seen from the street)", (W, H)),
             "orm": mf.save(ctx.fascias, "glass/%s/%s_orm.png" % (ctx.id, stem), mf.orm8(S.B.rough, S.B.metal), "linear 8-bit: R=255, G=roughness, B=metal", (W, H))}
    ink = rec["face_alpha_ink_box_in_tile_mm"]
    cx_in_tile = (ink[0] + ink[2]) / 2.0
    place = dict(x_street_m_of_ink_centre=g["x_street_m"], z_baseline_m=g["z_m"], tile_left_street_offset_mm=round(-cx_in_tile, 1), tile_baseline_from_tile_bottom_mm=rec["baseline_row_from_bottom_mm"],
                 note="u runs from the viewer's left to right; placed by sw_front like Rita's hours row (the door's lower pane)")
    row = dict(kind="glass_row", id="%s.glass.%d" % (ctx.id, ROW_ID), row=ROW_ID, shop=ctx.id, surface=g["surface"], string=" | ".join(lines), lines=rec["lines"], line_pitch_mm=rec["line_pitch_mm"], hours=True, hours_like_ritas=True,
               font=g["font"], weight=g["weight"], cap_mm=g["cap_mm"], technique=g["technique"], style=rec["style"], tracking_em=rec["tracking_em"], seed=int(seed), size_px=[W, H], size_mm=[W, H], files=files, place=place,
               ink_box_in_tile_mm=ink, source=g["source"], kind_of_number="Judgement", proposed=True, brush=bool(rec.get("brush")))
    man["glass_lettering"].append(row)
    json.dump(man, open(man_p, "w"), indent=1)
    log("hours row for %s: %s (%d x %d mm)" % (ctx.id, " | ".join(lines), W, H))
    return row
