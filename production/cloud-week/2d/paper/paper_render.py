"""paper_render.py: an item's elements, a class and a seed in; colour, alpha, height, roughness and metal out (unit 4.2 to 4.4, cloud week 42).

render(P, geo, cls, seed, wear) composites paper_ink's elements over the aged stock in the colours the target's own formulas give for the class, then, if wear is on, lets
paper_wear age the sheet (the table the item names). wear=False is the clean render the check reads for ITEM.clean: the class's colours and the process's look, no weather,
no fixings and none of the copier's speckle.
"""
import math

import numpy as np
from scipy import ndimage as ndi

import paper_common as pc
import paper_ink as pi
import paper_wear as pw

PAPER_ROUGH = {"white_card": 0.80, "buff_card": 0.80, "index_white": 0.80}
H_UNITS_DEFAULT = 25600.0          # 16-bit height units per mm (the fascia maps' own scale)
H_UNITS_RELIEF = 8192.0            # for the cast and pressed plates: 3 mm of relief needs more than the 1.28 mm the default scale holds


def resolve(P, item, spec, cls, tau):
    t, key = spec
    if t == "rgb":
        return np.asarray(key, np.float32)
    if t == "ink":
        col = P.ink(key, item["stock"], cls, tau)
    elif t == "paint":
        col = P.paint(key, cls)
    elif t == "stockkey":
        col = P.stock(key, cls, tau)
    else:
        raise ValueError(spec)
    if item["wear"].get("table") == "letting_board" and key in ("agent_red", "vinyl_red"):
        col = pc.mix(col, (196, 128, 118), 0.30 * pc.AGE[cls]["yellow"])             # the target's red_fade: towards chalk-pink by 0.3 at class D
    return np.asarray(col, np.float32)


def render(P, geo, cls, seed, wear=True):
    it = geo.item
    h, w = geo.shape
    ppm = geo.ppm
    iid = it["id"]
    table = it["wear"].get("table")
    tau = 0.7 if table == "glass_bill" else 1.0
    rng = pc.rng_for(seed, iid, "render", cls)
    rgb = np.zeros((h, w, 3), np.float32)
    if it["stock"]:
        rgb[:] = np.asarray(P.stock(it["stock"], cls, tau), np.float32)
        low = pc.value_noise((h, w), 6.0 * ppm, rng, octaves=2)
        fine = rng.standard_normal((h, w)).astype(np.float32)
        rgb *= (1.0 + (low - 0.5) * 0.024 + fine * 0.004)[..., None]
    height = np.zeros((h, w), np.float32)
    base_rough = PAPER_ROUGH.get(it["stock"], 0.85) if it["stock"] else geo.look["rough"]
    rough = np.full((h, w), base_rough, np.float32)
    metal = np.zeros((h, w), np.float32)
    # the art slots: a flat stand-in in the target's nominal colour, aged as a printed colour; behind every line the target says is set "on art:r,g,b" the picture is that colour (the
    # target's guarantee, in a zone 10 mm round the line and feathered over 25 mm), so a title on sky and a tag on sand each stand on what the target says
    for a in geo.art:
        wx0, wx1, wy0, wy1 = a["win"]
        col = np.asarray(P.paint_rgb(a["rgb"], cls), np.float32)
        n = pc.value_noise((wy1 - wy0, wx1 - wx0), 60 * ppm, pc.rng_for(seed, iid, "art"), octaves=2)
        rgb[wy0:wy1, wx0:wx1] = col * (1.0 + (n[..., None] - 0.5) * 0.05)
        for b in it["blocks"]:
            if b.get("ghost") or not str(b["on"]).startswith("art:"):
                continue
            zc = tuple(int(v) for v in b["on"].split(":", 1)[1].split(","))
            if zc == tuple(a["rgb"]):
                continue
            x0, y0, x1, y1 = b["ink_box_mm"]
            H_ = it["format"]["h_mm"]
            zb = ((x0 - 10) * ppm, (H_ - y1 - 10) * ppm, (x1 + 10) * ppm, (H_ - y0 + 10) * ppm)
            zwin = pi.window_around(zb, geo.shape, 25 * ppm)
            core = pi.rect_cov(zb, zwin)
            m = np.maximum(core, np.clip(pc.smooth(core, 9 * ppm) * 2.0, 0, 1))
            zcol = np.asarray(P.paint_rgb(zc, cls), np.float32)
            sub = rgb[zwin[2]:zwin[3], zwin[0]:zwin[1]]
            sub[:] = sub * (1 - m[..., None]) + zcol * m[..., None]
    for e in geo.elems:
        wx0, wx1, wy0, wy1 = e.win
        col = resolve(P, it, e.spec, cls, tau)
        a = e.cov if e.dens is None else e.cov * e.dens
        sub = rgb[wy0:wy1, wx0:wx1]
        if e.rim is not None:
            colarr = col[None, None, :] * (1.0 - np.clip(e.rim, 0, 0.35))[..., None]
        else:
            colarr = col
        sub[:] = sub * (1 - a[..., None]) + colarr * a[..., None]
        if e.film and e.kind != "scrim":
            height[wy0:wy1, wx0:wx1] += e.cov * e.film
        if e.rough is not None and e.kind != "scrim":
            rough[wy0:wy1, wx0:wx1] = rough[wy0:wy1, wx0:wx1] * (1 - a) + e.rough * a
    alpha = geo.alpha.copy()
    for win, hole in geo.holes:
        wx0, wx1, wy0, wy1 = win
        alpha[wy0:wy1, wx0:wx1] *= (1 - hole)
    units = H_UNITS_DEFAULT
    if it.get("relief") and it["relief"].get("raised_mm"):
        units = H_UNITS_RELIEF
        height += relief_height(it, geo, alpha)
    if it["kind"] in ("plate", "board"):
        rolled_edge(it, geo, alpha, rgb, height)
    log = {}
    if wear:
        S = pw.Surf(geo, P, cls, rgb, alpha, height, rough, metal, pc.rng_for(seed, iid, "wear", cls), tau)
        pw.apply(S, table, cls)
        log = S.log
        rgb, alpha, height, rough, metal = S.rgb, S.alpha, S.height, S.rough, S.metal
    units = height_units(height)
    return dict(rgb=rgb, alpha=alpha, height=height, rough=rough, metal=metal, units=units, log=log, tau=tau)


def height_units(height):
    """16-bit units per mm, chosen per picture so that no pixel clips (the second close review: 86 of 129 maps hit +-1.28 mm at 25600): 25600 to 1.27 mm, 8192 to 3.99 mm, else 4096."""
    hm = float(np.abs(height).max()) if height.size else 0.0
    return 25600.0 if hm <= 1.27 else (8192.0 if hm <= 3.99 else 4096.0)


def relief_height(it, geo, alpha):
    """The raised letters and border of a cast or pressed plate: raised_mm high, ten degrees of draft on each wall and a rounded top edge."""
    r = it["relief"]
    rm = np.zeros(geo.shape, np.float32)
    for e in geo.elems:
        if e.raised:
            wx0, wx1, wy0, wy1 = e.win
            rm[wy0:wy1, wx0:wx1] = np.maximum(rm[wy0:wy1, wx0:wx1], e.cov)
    inside = ndi.distance_transform_edt(rm > 0.5).astype(np.float32) / geo.ppm            # mm from the wall
    ramp = r["raised_mm"] * math.tan(math.radians(r["draft_deg"])) + r["top_radius_mm"]
    t = np.clip(inside / max(ramp, 0.2), 0, 1)
    prof = 1 - (1 - t) ** 2                                                              # a rounded shoulder
    return (r["raised_mm"] * prof * (rm > 0.5)).astype(np.float32)


def rolled_edge(it, geo, alpha, rgb, height):
    """The rolled or radiused edge of a plate or board: the height rolls over the last few millimetres and the colour shades with it."""
    roll = 6.0
    if it.get("relief"):
        txt = it["relief"].get("edge", "")
        roll = 3.0 if "radius 3" in txt else (2.0 if "2 mm arris" in txt else 4.0)          # S01: the target's 2 mm arris
    if it["process"] in ("enamel", "vitreous_enamel_steel"):
        roll = 6.0
    if it["process"] == "agent_board":
        roll = 2.0
    d = ndi.distance_transform_edt(np.pad(alpha > 0.5, 1))[1:-1, 1:-1].astype(np.float32) / geo.ppm      # padded: the picture's own border is the plate's edge (the close review's finding 2)
    t = np.clip(d / roll, 0, 1)
    drop = roll * (1 - np.sqrt(np.clip(1 - (1 - t) ** 2, 0, 1)))
    height -= (drop * (1.0 if it["process"] in ("enamel", "vitreous_enamel_steel") else 0.35)).astype(np.float32)      # H01, H02: the target's true 6 mm radius
    k = (1 - t)
    gy, gx = np.gradient(drop)
    rgb *= (1 - 0.10 * k + (-gx * 0.5 - gy * 0.5) * geo.ppm * 0.05)[..., None]


def to_rgba8(r):
    rgb = np.clip(np.round(r["rgb"]), 0, 255).astype(np.uint8)
    a = np.clip(np.round(r["alpha"] * 255), 0, 255).astype(np.uint8)
    return rgb, a


def height16(r):
    return np.clip(np.round(32768 + r["height"] * r["units"]), 0, 65535).astype(np.uint16)


def orm8(r):
    o = np.empty(r["rgb"].shape, np.uint8)
    o[..., 0] = 255
    o[..., 1] = np.clip(np.round(r["rough"] * 255), 0, 255).astype(np.uint8)
    o[..., 2] = np.clip(np.round(r["metal"] * 255), 0, 255).astype(np.uint8)
    return o
