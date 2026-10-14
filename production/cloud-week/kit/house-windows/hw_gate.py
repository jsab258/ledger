"""The gate in the cloud for the house windows (target section 9): what the game will show from a review camera, without Unreal.

Rewritten 14 October for the house windows from the shop kit's sw_gate.py (copied that day, shop-windows/sw_gate.py, md5 08e00d19...): what is kept is the method (the room picture baked for the camera through
tools/ue/make_interior_material.py's `trace`, imported and never rewritten; the card as an emission quad; the night glass as reflection only; the stand-in lamps hidden from the camera and from glossy
rays) and the baking code (uv_map, mips, sample_mips, bake_card); what is new is the street, the houses with the kit pieces in the wall, and the measuring masks.

For each camera and state: (1) every window seen at 11 degrees or more from its wall gets its card baked through `trace` from this eye (a window under that sees the reveal and the frame only: no ray reaches
the card); (2) the street, the two rows, the twenty kit pieces and the cards are built in Blender and rendered with Cycles at 2560 x 1440; (3) a flat-colour mask render says, per pixel, what it is
(R: 1 glass, 2 joinery, 3 net or curtain or blind, 4 brick, 5 card; G: the window's number) for the measurements of target 9.

The pane (target 5.1, GLASS.pane.cloud_stand_in): Cycles Principled, not a Glass BSDF: here a Mix of a Transparent BSDF and a Glossy GGX (roughness 0.03) weighted by the dielectric Fresnel of
F0 0.08 (IOR 1.789: Unreal's Specular 1.0), 1.0 by day and 0.2 at night (unreal-look.json glass_specular_night); the room card, the nets, the curtains and the blinds are seen through it as the room is seen
through a pane (1 - Fresnel); its roughness is raised to 0.35 in the 6 mm dirt band and the lowest 25 mm (the pane's COLOR_0). The game's own glass (Lumen, the street cube) is owed on the PC.
"""
import importlib.util
import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
import hw_t as T  # noqa: E402
import hw_ctx as C  # noqa: E402

_spec = importlib.util.spec_from_file_location("make_interior_material", os.path.join(REPO, "tools", "ue", "make_interior_material.py"))
MIM = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MIM)
trace = MIM.trace

BRIGHTNESS = {"day": 0.12, "night_lit": 1.0, "night_dark": 0.7}       # the game's emissive scale for the card (target 7.1 and 9; 14 Oct, from the try 1 reviews: a lit room's card is the night_lit picture x 1.0, no longer x 0.7 x 0.4 = 0.28, which put the room seen through clear glass at a quarter of its own net)
WARM = (1.0, 0.714, 0.344)
SODIUM = (1.0, 0.25, 0.0)
RES = tuple(int(v) for v in os.environ.get("LEDGER_GATE_RES", "2560x1440").split("x"))
MIN_BAKE_ANGLE = 11.0
COTTAGE_LAMP_SCALE = 0.5        # 14 Oct, from the try 1 reviews (N3): the two lamps in front of the west cottages (x 8 and 18) burnt 11.2 per cent of west_south_bay2_gf_w1's joinery to flat orange; cut until no window's joinery is over 2 per cent
COTTAGE_LAMPS = (8.0, 18.0)
OPENING_GAP = 0.002             # the stand-in wall's openings are cut 2 mm larger each side and at the head than the kit's linings (the close review's narrow point 1: faces sharing the brick's planes left a black notch at the far jamb's head)
GRIME_BAND_M = 0.030            # target 4.2: a grime band 30 mm high along the sill on grimy windows ...
GRIME_BAND_FACTOR = 0.75        # ... at x 0.75 (the close review's number, a Judgement within the box shade, above KIT-09's floor of 0.25)
CAT = {"glass": 1, "joinery": 2, "cloth": 3, "brick": 4, "card": 5}


def lin(c):
    c = np.asarray(c, np.float32)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def srgb(l):
    l = np.clip(l, 0, 1)
    return np.where(l <= 0.0031308, l * 12.92, 1.055 * l ** (1 / 2.4) - 0.055)


# ------------------------------------------------------------------------------------------------------------- the bake (the shop gate's, generalised)
def _bake_rows(args):
    j0, j1, ex, ey, ez, W, H, D, camd, side, nw, nh = args
    out = np.empty((j1 - j0, nw, 2), np.float32)
    for j in range(j0, j1):
        zc = H - (j + 0.5) / nh * H
        for i in range(nw):
            xc = (i + 0.5) / nw * W if side < 0 else W - (i + 0.5) / nw * W         # column 0 is the viewer's LEFT: the card's HIGH x on an east card, its LOW x on a west one
            u, v = trace((xc, 0.0, zc), (ex, ey, ez), (W, H, D), camd, side)
            out[j - j0, i, 0] = u
            out[j - j0, i, 1] = v
    return j0, out


def uv_map(eye_card, size, camd, side, nw, nh, jobs=3):
    """(u, v) of the room picture for every card pixel, through the game's `trace` (the Python function, called per pixel)."""
    from multiprocessing import Pool
    W, H, D = size
    step = 16
    chunks = [(j, min(nh, j + step), eye_card[0], eye_card[1], eye_card[2], W, H, D, camd, side, nw, nh) for j in range(0, nh, step)]
    uv = np.empty((nh, nw, 2), np.float32)
    with Pool(jobs) as p:
        for j0, o in p.imap_unordered(_bake_rows, chunks):
            uv[j0:j0 + o.shape[0]] = o
    return uv


def mips(img):
    chain = [img]
    while min(chain[-1].shape[:2]) > 8:
        a = chain[-1]
        h2, w2 = a.shape[0] // 2 * 2, a.shape[1] // 2 * 2
        a = a[:h2, :w2]
        chain.append((a[0::2, 0::2] + a[1::2, 0::2] + a[0::2, 1::2] + a[1::2, 1::2]) / 4.0)
    return chain


def sample_mips(chain, uv, base_wh):
    pw, ph = base_wh
    du_dx = np.gradient(uv[..., 0], axis=1) * pw
    dv_dx = np.gradient(uv[..., 1], axis=1) * ph
    du_dy = np.gradient(uv[..., 0], axis=0) * pw
    dv_dy = np.gradient(uv[..., 1], axis=0) * ph
    foot = np.maximum(np.hypot(du_dx, dv_dx), np.hypot(du_dy, dv_dy))
    lod = np.clip(np.log2(np.maximum(foot, 1.0)), 0, len(chain) - 1.001)
    lo = np.floor(lod).astype(int)
    fr = (lod - lo)[..., None]
    out = np.zeros(uv.shape[:2] + (3,), np.float32)
    for lv in range(len(chain)):
        m_lo, m_hi = lo == lv, lo == lv - 1
        if not (m_lo.any() or m_hi.any()):
            continue
        h, w = chain[lv].shape[:2]
        x = np.clip(uv[..., 0] * w - 0.5, 0, w - 1)
        y = np.clip(uv[..., 1] * h - 0.5, 0, h - 1)
        samp = np.stack([ndimage.map_coordinates(chain[lv][..., c], [y, x], order=1, mode="nearest") for c in range(3)], axis=-1)
        out += np.where(m_lo[..., None], samp * (1 - fr), 0) + np.where(m_hi[..., None], samp * fr, 0)
    return out


def bake_card(eye_card, size, camd, side, picture_png, out_png, nw, nh, jobs=3):
    """The card's emission picture for one eye: the room picture (sRGB) sampled through trace with mips, written as 8-bit sRGB WITHOUT the brightness (the card's emission strength carries it)."""
    uv = uv_map(eye_card, size, camd, side, nw, nh, jobs)
    pic = np.asarray(Image.open(picture_png).convert("RGB")).astype(np.float32) / 255.0
    chain = mips(lin(pic))
    lin_img = sample_mips(chain, uv, (pic.shape[1], pic.shape[0]))
    Image.fromarray((srgb(lin_img) * 255.0 + 0.5).astype(np.uint8)).save(out_png)
    return lin_img


def card_state(site, night, lit_names):
    """Which picture a window's card shows (PIC-08): day by day; at night the lit windows their night_lit picture, the others night_dark; an unlet (empty) room is never lit."""
    if not night:
        return "day"
    st = "night_lit" if site["id"] in lit_names else "night_dark"
    if site["room"].startswith("up_empty") and st == "night_lit":
        st = "night_dark"
    return st


def eye_in_card_frame(site, eye):
    """The eye in the card frame `trace` takes: x from the card's low-x edge, y out from the card plane (negative for the east viewer), z above the card's bottom."""
    c = site["card"]
    return (eye[0] - c["x_low"], eye[1] - site["side"] * abs(c["y_card_plane"]), eye[2] - c["z_bottom_above_crown"])


GLASS_IOR = 1.789          # F0 = ((n - 1) / (n + 1))^2 = 0.08: Unreal's Specular 1.0


def make_glass_gate(bpy, refl, old_fault=False, backface_fix=True):
    """The pane of the cloud gate (target 5.1): a Mix of a Transparent BSDF and a Glossy GGX, weighted by the dielectric Fresnel of F0 0.08 (IOR 1.789) x `refl` (1.0 by day, 0.2 at night) x (1 - Backfacing); the roughness rises
    from 0.03 to 0.35 where the pane's COLOR_0 says dirt (R 0.8: the 6 mm band and the lowest 25 mm). `old_fault`: the first build's pane for WB-08: a lit pale card (flat emission, no reflection), no lines.
    `backface_fix` (14 Oct, from the try 1 reviews, fault 1): the kit's panes are closed slabs 2.5 mm thick (a front face and a back face); Cycles' Fresnel node inverts the IOR on a back face, so past the critical angle (34 degrees from
    the normal, any view under 56 degrees from the wall) the back face was a total mirror and nothing passed the pane. The back face is now fully transparent and the front face stands for both, as the target's 5.1 says (F0 0.08
    for both faces of a single pane). `backface_fix=False` is the negative control of GLS-06 and MAT-04 (it must fail both)."""
    glass_gate = bpy.data.materials.new("glass_gate")
    glass_gate.use_nodes = True
    gnt = glass_gate.node_tree
    for n in list(gnt.nodes):
        gnt.nodes.remove(n)
    gout = gnt.nodes.new("ShaderNodeOutputMaterial")
    if old_fault:
        # a lit pale card: its own light (emission), flat; a first try with a diffuse card and only the box shade removed still read D/L 0.52 because Cycles shades the reveal itself
        dif = gnt.nodes.new("ShaderNodeEmission")
        dif.inputs["Color"].default_value = (0.60, 0.60, 0.58, 1.0)
        dif.inputs["Strength"].default_value = 1.0
        gnt.links.new(dif.outputs[0], gout.inputs[0])
        return glass_gate
    gmix = gnt.nodes.new("ShaderNodeMixShader")
    gtr = gnt.nodes.new("ShaderNodeBsdfTransparent")
    ggl = gnt.nodes.new("ShaderNodeBsdfGlossy")
    ggl.distribution = "GGX"
    ggl.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    gfr = gnt.nodes.new("ShaderNodeFresnel")
    gfr.inputs["IOR"].default_value = GLASS_IOR
    gmul = gnt.nodes.new("ShaderNodeMath")
    gmul.operation = "MULTIPLY"
    gmul.inputs[1].default_value = refl
    gat = gnt.nodes.new("ShaderNodeAttribute")
    gat.attribute_name = "Color"
    gsep = gnt.nodes.new("ShaderNodeSeparateColor")
    gdirt = gnt.nodes.new("ShaderNodeMapRange")
    gdirt.inputs["From Min"].default_value = 1.0
    gdirt.inputs["From Max"].default_value = 0.8
    gdirt.inputs["To Min"].default_value = 0.03
    gdirt.inputs["To Max"].default_value = 0.35
    gdirt.clamp = True
    gnt.links.new(gat.outputs["Color"], gsep.inputs["Color"])
    gnt.links.new(gsep.outputs["Red"], gdirt.inputs["Value"])
    gnt.links.new(gdirt.outputs["Result"], ggl.inputs["Roughness"])
    gnt.links.new(gfr.outputs["Fac"], gmul.inputs[0])
    if backface_fix:
        ggeo = gnt.nodes.new("ShaderNodeNewGeometry")
        ginv = gnt.nodes.new("ShaderNodeMath")                 # 1 - Backfacing: 1 on the front face, 0 on the back face
        ginv.operation = "SUBTRACT"
        ginv.inputs[0].default_value = 1.0
        gfac = gnt.nodes.new("ShaderNodeMath")                 # Fresnel x refl x (1 - Backfacing)
        gfac.operation = "MULTIPLY"
        gnt.links.new(ggeo.outputs["Backfacing"], ginv.inputs[1])
        gnt.links.new(gmul.outputs["Value"], gfac.inputs[0])
        gnt.links.new(ginv.outputs["Value"], gfac.inputs[1])
        gnt.links.new(gfac.outputs["Value"], gmix.inputs["Fac"])
    else:
        gnt.links.new(gmul.outputs["Value"], gmix.inputs["Fac"])
    gnt.links.new(gtr.outputs[0], gmix.inputs[1])
    gnt.links.new(ggl.outputs[0], gmix.inputs[2])
    gnt.links.new(gmix.outputs[0], gout.inputs[0])
    return glass_gate


# ------------------------------------------------------------------------------------------------------------- the scene
def build_and_render(view_name, cam, state, out_png, bake_dir, samples=48, res=None, mode="beauty", glass_refl=None, extra=None, log=print):
    """Build the street with the twenty windows and render one view. `cam`: {eye (street), yaw/pitch or aim, vfov}. state: 'day' or 'night' (20:30: the lit windows by the table, the rest dark).
    mode: 'beauty' (the render), 'mask' (flat colours: glass 1, joinery 2, cloth 3, brick 4, card 5 in R, the window's number in G). Returns the seconds and the record (windows in view, angles)."""
    import bpy
    from mathutils import Vector, Matrix, Euler
    res = res or RES
    extra = extra or {}
    maskT = mode == "maskT"          # the mask with the glass clear: what lies BEHIND each pane pixel (3 net, curtain or blind; 5 the room card; 2 joinery): the clear glass and the cloth told apart (NIGHT-07)
    if maskT:
        mode = "mask"
    night = state != "day"
    t0 = time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    lit_names = set(T.lit_at("20:30")) if night else set()
    sites = T.sites()
    rec = {"view": view_name, "state": state, "windows": {}}

    # ---------------------------------------------------------------- materials
    def new_mat(name, rgb, rough=0.8, emit=None, emit_strength=0.0):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        p = m.node_tree.nodes["Principled BSDF"]
        p.inputs["Base Color"].default_value = (*rgb, 1.0)
        p.inputs["Roughness"].default_value = rough
        if emit is not None:
            p.inputs["Emission Color"].default_value = (*emit, 1.0)
            p.inputs["Emission Strength"].default_value = emit_strength
        return m

    def flat(name, rgb):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        t = m.node_tree
        for n in list(t.nodes):
            t.nodes.remove(n)
        e = t.nodes.new("ShaderNodeEmission")
        e.inputs["Color"].default_value = (*rgb, 1.0)
        o = t.nodes.new("ShaderNodeOutputMaterial")
        t.links.new(e.outputs[0], o.inputs[0])
        return m

    P_SOFFIT = list(T.paints()["white_grimy"]["lin"])
    brick = new_mat("brick", (0.5, 0.3, 0.22), 0.92)
    nt = brick.node_tree
    bp = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    cb = nt.nodes.new("ShaderNodeCombineXYZ")
    br = nt.nodes.new("ShaderNodeTexBrick")
    nt.links.new(tc.outputs["Object"], sp.inputs["Vector"])
    nt.links.new(sp.outputs["X"], cb.inputs["X"])
    nt.links.new(sp.outputs["Z"], cb.inputs["Y"])
    nt.links.new(cb.outputs["Vector"], br.inputs["Vector"])
    br.offset = 0.5
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = 0.215
    br.inputs["Row Height"].default_value = 0.075
    br.inputs["Mortar Size"].default_value = 0.010
    br.inputs["Mortar Smooth"].default_value = 0.2
    br.inputs["Color1"].default_value = (*lin([0.50, 0.30, 0.22]), 1.0)
    br.inputs["Color2"].default_value = (*lin([0.43, 0.25, 0.18]), 1.0)
    br.inputs["Mortar"].default_value = (*lin([0.58, 0.55, 0.50]), 1.0)
    nt.links.new(br.outputs["Color"], bp.inputs["Base Color"])
    paving = new_mat("paving", tuple(lin([0.50, 0.50, 0.48])), 0.85)
    road = new_mat("road", tuple(lin([0.22, 0.22, 0.22])), 0.9)
    stone = new_mat("stone", tuple(lin([0.72, 0.70, 0.64])), 0.85)
    roof = new_mat("roof", tuple(lin([0.2, 0.2, 0.22])), 0.7)
    dark = new_mat("carcass", (0.015, 0.015, 0.015), 1.0)
    shopfront = new_mat("shopfront", tuple(lin([0.08, 0.1, 0.09])), 0.5)
    post = new_mat("lamp_post", tuple(lin([0.05, 0.05, 0.06])), 0.6)
    if mode == "mask":
        mk = {k: flat("mk_" + k, (v / 255.0, 0, 0)) for k, v in CAT.items()}
        clear_glass = bpy.data.materials.new("clear_glass_mask")
        clear_glass.use_nodes = True
        for n_ in list(clear_glass.node_tree.nodes):
            clear_glass.node_tree.nodes.remove(n_)
        ct_ = clear_glass.node_tree.nodes.new("ShaderNodeBsdfTransparent")
        co_ = clear_glass.node_tree.nodes.new("ShaderNodeOutputMaterial")
        clear_glass.node_tree.links.new(ct_.outputs[0], co_.inputs[0])

    # ---------------------------------------------------------------- helpers
    def bl(p):
        return (-p[0], p[1], p[2])

    def blk(name, x0, x1, y0, y1, z0, z1, m):
        """A closed box in STREET coordinates (x0 < x1 in the street's x), built in Blender's (x negated)."""
        xa, xb = -x1, -x0
        v = [(xa, y0, z0), (xb, y0, z0), (xb, y1, z0), (xa, y1, z0), (xa, y0, z1), (xb, y0, z1), (xb, y1, z1), (xa, y1, z1)]
        f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        me = bpy.data.meshes.new(name)
        me.from_pydata(v, [], f)
        o = bpy.data.objects.new(name, me)
        sc.collection.objects.link(o)
        o.data.materials.append(m)
        return o

    def wedge(name, x0, x1, y_eave, y_back, z_eave, z_ridge, m):
        """A roof: a prism from the eaves to the ridge (street x, y)."""
        xa, xb = -x1, -x0
        v = [(xa, y_eave, z_eave), (xb, y_eave, z_eave), (xb, y_back, z_eave), (xa, y_back, z_eave), (xa, (y_eave + y_back) / 2, z_ridge), (xb, (y_eave + y_back) / 2, z_ridge)]
        f = [(0, 3, 2, 1), (0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5)[::-1], (3, 0, 4), (2, 3, 4, 5)]
        me = bpy.data.meshes.new(name)
        me.from_pydata(v, [], [(0, 3, 2, 1), (0, 1, 5, 4), (1, 2, 5), (3, 4, 5, 2), (0, 4, 3)])
        o = bpy.data.objects.new(name, me)
        sc.collection.objects.link(o)
        o.data.materials.append(m)
        return o

    def cat(o, key, m_real):
        o.data.materials.clear()
        o.data.materials.append(mk[key] if mode == "mask" else m_real)

    X0, X1 = -3.0, 50.0

    # ---------------------------------------------------------------- the street
    g = blk("road", X0, X1, -3.38, 3.38, -0.6, 0.0, road)
    cat(g, "brick", road)
    for nm, ya, yb in (("footway_E", 3.38, 12.0), ("footway_W", -12.0, -3.38)):
        o = blk(nm, X0, X1, ya, yb, -0.6, 0.10, paving)
        cat(o, "brick", paving)
    # ---------------------------------------------------------------- the east parade: one slab a floor, piers between the openings
    ups = [s for s in sites if s["side"] > 0]
    gfs = [s for s in sites if s["side"] < 0]
    yo, yi = C.WALL_E, C.WALL_E + C.WALL_T
    z_gf_top, z_sill, z_head, z_eave = 3.65, ups[0]["sill_z_above_crown"], ups[0]["head_z_above_crown"], 6.3
    # the ground floor (the shops' own, the wall kit's and unit 7's: stand-ins): stallriser, window, door, pilasters and a fascia a bay
    fascia_m = new_mat("fascia", tuple(lin([0.62, 0.58, 0.48])), 0.6)
    glass_dark = new_mat("shop_glass", (0.01, 0.012, 0.014), 0.05)
    o = blk("e_ground_back", 3.0, 46.0, yo + 0.06, yi, 0.1, z_gf_top, shopfront)
    cat(o, "brick", shopfront)
    bx = 3.0
    while bx < 45.9:
        be = min(bx + 6.0, 46.0)
        for nm, a, b, z0_, z1_, yy, m_ in (("stall", bx + 0.3, be - 0.3, 0.1, 0.62, yo - 0.02, shopfront), ("win", bx + 0.55, bx + 4.2, 0.62, 2.75, yo + 0.03, glass_dark),
                                           ("door", bx + 4.45, bx + 5.45, 0.1, 2.55, yo + 0.03, glass_dark), ("pil_l", bx, bx + 0.3, 0.1, 2.8, yo - 0.05, shopfront), ("pil_r", be - 0.3, be, 0.1, 2.8, yo - 0.05, shopfront),
                                           ("fascia", bx, be, 2.8, 3.5, yo - 0.06, fascia_m)):
            o = blk("e_%s_%g" % (nm, bx), a, b, yy, yo + 0.07, z0_, z1_, m_)
            cat(o, "brick", m_)
        bx += 6.0
    o = blk("e_stringcourse", 3.0, 46.0, yo - 0.03, yi, 3.5, 3.65, stone)
    cat(o, "brick", stone)
    xs = sorted(s["x_centre"] for s in ups)
    cuts = [3.0]
    for x in xs:
        cuts += [x - (0.425 + OPENING_GAP), x + (0.425 + OPENING_GAP)]
    cuts.append(46.0)
    for k in range(0, len(cuts), 2):
        a, b = cuts[k], cuts[k + 1]
        if b - a > 1e-6:
            o = blk("e_pier_%d" % k, a, b, yo, yi, z_gf_top, z_eave, brick)
            cat(o, "brick", brick)
    for x in xs:
        o = blk("e_under_sill_%g" % x, x - (0.425 + OPENING_GAP), x + (0.425 + OPENING_GAP), yo, yi, z_gf_top, z_sill - 0.127, brick)
        cat(o, "brick", brick)
        o = blk("e_stone_sill_%g" % x, x - 0.5012, x + 0.5012, yo - 0.0508, yi, z_sill - 0.127, z_sill, stone)
        cat(o, "brick", stone)
        o = blk("e_head_%g" % x, x - (0.425 + OPENING_GAP), x + (0.425 + OPENING_GAP), yo, yi, z_head + OPENING_GAP, z_eave, brick)
        cat(o, "brick", brick)
    o = wedge("e_roof", 2.7, 46.3, yo - 0.3, yo + 8.0, z_eave, z_eave + 0.5 * 8.0 * math.tan(math.radians(35.0)), roof)
    cat(o, "brick", roof)
    # the eaves' underside (the close review's narrow point 2): the stand-in's 0.3 m overhang was roofing in shade and showed pure black in the top of the upper panes by day; a soffit board in the house's grimy white
    # (linear 0.66, roughness 0.48), lit by the street as a painted soffit is; its top 5 mm stands inside the roof's prism so that no two faces share a plane
    soffit = new_mat("soffit", tuple(P_SOFFIT), 0.48)
    o = blk("e_soffit", 2.7, 46.3, yo - 0.3, yo, z_eave - 0.025, z_eave + 0.005, soffit)
    cat(o, "brick", soffit)
    # ---------------------------------------------------------------- the west cottages (x 3 to 21), the west_north shops beyond (stand-ins)
    wy_o, wy_i = C.WALL_W, C.WALL_W - C.WALL_T
    gz_sill, gz_head, gz_eave = gfs[0]["sill_z_above_crown"], gfs[0]["head_z_above_crown"], 3.1
    o = blk("w_below", 3.0, 21.0, wy_i, wy_o, 0.1, gz_sill - 0.127, brick)
    cat(o, "brick", brick)
    o = blk("w_above", 3.0, 21.0, wy_i, wy_o, gz_head + OPENING_GAP, gz_eave, brick)
    cat(o, "brick", brick)
    wx = sorted(s["x_centre"] for s in gfs)
    cuts = [3.0]
    doors = [4.5, 13.5, 19.5]
    for x in sorted(wx + doors):
        hw = 0.45 if x in doors else 0.425 + OPENING_GAP
        cuts += [x - hw, x + hw]
    cuts.append(21.0)
    for k in range(0, len(cuts), 2):
        a, b = cuts[k], cuts[k + 1]
        if b - a > 1e-6:
            o = blk("w_pier_%d" % k, a, b, wy_i, wy_o, gz_sill - 0.127, gz_head + OPENING_GAP, brick)
            cat(o, "brick", brick)
    for x in doors:
        o = blk("w_door_%g" % x, x - 0.45, x + 0.45, wy_i, wy_o + 0.02, 0.1, 2.0, shopfront)
        cat(o, "brick", shopfront)
        o = blk("w_door_head_%g" % x, x - 0.45, x + 0.45, wy_i, wy_o, 2.0, gz_sill + 1.68, brick)
        cat(o, "brick", brick)
    for x in wx:
        # the stone sill stands 50.8 mm proud of the face toward the street (the east row's is yo - 0.0508; here the street is at larger y). A first version put it 50.8 mm INTO the wall and its top shared the plane of the
        # wall's own top face under the window: a black strip along every cottage sill (shadow on coplanar faces). The wall under the windows stops at the sill's underside and the stone sill is its own block.
        o = blk("w_stone_sill_%g" % x, x - 0.5012, x + 0.5012, wy_i, wy_o + 0.0508, gz_sill - 0.127, gz_sill, stone)
        cat(o, "brick", stone)
    o = wedge("w_roof", 2.7, 21.3, wy_o + 0.3, wy_o - 5.0, gz_eave, gz_eave + 0.5 * 5.0 * math.tan(math.radians(40.0)), roof)
    cat(o, "brick", roof)
    o = blk("w_soffit", 2.7, 21.3, wy_o, wy_o + 0.3, gz_eave - 0.025, gz_eave + 0.005, soffit)
    cat(o, "brick", soffit)
    o = blk("wn_shops", 21.0, 46.0, wy_i - 8.0, wy_o, 0.1, 3.5, brick)
    cat(o, "brick", brick)
    o = blk("far_end_e", 46.0, 48.0, yo, yi + 8.0, 0.1, 7.0, brick)
    cat(o, "brick", brick)
    # ---------------------------------------------------------------- the lamp columns (stand-ins): dark posts, the light itself hidden from the camera and from glossy rays
    lamps = []
    for lx in (8.0, 18.0, 28.0, 38.0):
        o = blk("lamp_post_%g" % lx, lx - 0.06, lx + 0.06, -3.84, -3.72, 0.1, 4.55, post)
        cat(o, "brick", post)
        o = blk("lamp_head_%g" % lx, lx - 0.18, lx + 0.18, -3.96, -3.60, 4.55, 4.85, post)
        cat(o, "brick", post)
        lamps.append(lx)

    # ---------------------------------------------------------------- the kit pieces in the walls
    def load_kit(kind):
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.join(T.ASSETS, {"S22": "hw_S22.glb", "S11": "hw_S11.glb", "RC": "hw_RC.glb", "RC2": "hw_RC2.glb"}[kind]))
        new = [o for o in bpy.data.objects if o not in before]
        for o in new:
            o.hide_render = True
            o.hide_viewport = True
        return [o for o in new if o.type == "MESH"]
    templates = {}
    P = T.paints()
    refl = (0.2 if night else 1.0) if glass_refl is None else glass_refl
    glass_gate = make_glass_gate(bpy, refl, old_fault=bool(extra.get("old_fault")))

    cam_eye = cam["eye"]
    window_ids = {s["id"]: i + 1 for i, s in enumerate(sites)}
    baked = {}

    def bake_for(site):
        """The baked card of a window (or of a cottage house) for this eye and state; None when the window is seen too near the wall's plane to see the room."""
        ang = C.angle_from_wall_deg(site, cam_eye)
        key = site["card"].get("shared_by") and tuple(site["card"]["shared_by"]) or (site["id"],)
        if key in baked:
            return baked[key]
        res_ = None
        if ang >= MIN_BAKE_ANGLE and C.eye_in_front(site, cam_eye):
            lit = site["id"] in lit_names
            st = card_state(site, night, lit_names)
            pic = os.path.join(T.ROOMS, "%s_%s.png" % (site["room"], st))
            if os.path.exists(pic):
                c = site["card"]
                W_, H_, D_, camd = c["w"], c["h"], c["d"], c["camd"]
                nw = 768 if c["room_family"] == "UP" else 1024
                nh = int(round(nw * H_ / W_))
                out = os.path.join(bake_dir, "card_%s_%s_%s.png" % (view_name, st, site["id"] if len(key) == 1 else key[0]))
                if not os.path.exists(out):
                    os.makedirs(bake_dir, exist_ok=True)
                    bake_card(eye_in_card_frame(site, cam_eye), (W_, H_, D_), camd, c["side"], pic, out, nw, nh)
                res_ = (out, st)
        baked[key] = res_
        return res_
    kit_cache = {}
    for site in sites:
        kind = site["kind"]
        if kind not in kit_cache:
            kit_cache[kind] = load_kit(kind)
        tmpl = kit_cache[kind]
        wid = window_ids[site["id"]]
        X, Y, Z, turn = C.placement(site)
        root = bpy.data.objects.new("win_" + site["id"], None)
        sc.collection.objects.link(root)
        root.location = (X, Y, Z)
        root.rotation_euler = (0.0, 0.0, math.radians(turn))
        ang = C.angle_from_wall_deg(site, cam_eye)
        rec["windows"][site["id"]] = {"id": wid, "angle_deg": round(ang, 2), "in_front": C.eye_in_front(site, cam_eye), "kind": kind, "room": site["room"]}
        net = site["net"]["kind"]
        extra_k = (site.get("extra") or {}).get("kind")
        torn = site["net"].get("torn")
        paint = P[site["paint"]]
        lit = site["id"] in lit_names
        show = {"net__" + net} if net != "N0" else set()
        if torn:
            show = {"net__N1_torn", "net_rod__N1", "net_bracket__N1_L", "net_bracket__N1_R"}
        elif net != "N0":
            show |= {"net_rod__" + net, "net_bracket__%s_L" % net, "net_bracket__%s_R" % net}
        if extra_k in ("C1",):
            show |= {"curtain__C1_drawn", "curtain_pole", "curtain_finial__L", "curtain_finial__R", "curtain_bracket__L", "curtain_bracket__R"}
        if extra_k in ("C2",):
            show |= {"curtain__C2_open_L", "curtain__C2_open_R", "curtain_pole", "curtain_finial__L", "curtain_finial__R", "curtain_bracket__L", "curtain_bracket__R"}
        if extra_k == "B1":
            show |= {"blind__B1", "blind_headrail__B1"}
        if extra_k == "B2":
            show |= {"blind__B2", "blind_roller__B2"}
        if extra_k == "B3":
            show |= {"blind__B3", "blind_headrail__B3"}
        room = T.room(site["room"])
        if site["card"]["room_family"] == "UP" and room["pendant"]:
            show.add("pendant__shade")
        mats_w = {}
        for o in tmpl:
            nm = o.name
            base = nm.split(".")[0]
            is_dress = base.startswith(("net__", "net_rod__", "net_bracket__", "curtain", "blind", "pendant__"))
            if is_dress and base not in show:
                continue
            if base == "room__card" or base == "pendant__shade_gf":
                continue
            c = o.copy()
            sc.collection.objects.link(c)
            c.parent = root
            c.matrix_parent_inverse = Matrix.Identity(4)
            c.hide_render = False
            c.hide_viewport = False
            c.pass_index = wid
            c.name = "%s|%s" % (site["id"], base)
            rec["windows"][site["id"]].setdefault("objects", []).append(base)
            for i, sl in enumerate(c.material_slots):
                m0 = sl.material
                if m0 is None:
                    continue
                sl.link = "OBJECT"                     # the meshes are shared by every window of a kind: each window's materials are its own, on its object
                sl.material = m0
                mn = m0.name.split(".")[0]
                if mode == "mask":
                    key = "glass" if mn.startswith("glass") else ("joinery" if mn.startswith("paint_") or base.startswith(("net_rod", "net_bracket", "curtain_pole", "curtain_finial", "curtain_bracket")) else "cloth")
                    sl.material = clear_glass if (maskT and key == "glass") else mk[key]
                    continue
                if mn.startswith("glass"):
                    sl.material = glass_gate
                elif mn.startswith("paint_"):
                    grime = site["condition"] == "grimy" and base in GRIME_PARTS
                    key = ("paint", site["paint"], site["condition"], base in ("paint_joinery__lower_bottom_rail", "paint_joinery__oak_sill", "paint_joinery__frame_sill_rail"), m0.name, (site["id"], base) if grime else None)
                    if key not in mats_w:
                        m = m0.copy()
                        pb = m.node_tree.nodes["Principled BSDF"]
                        col = list(paint["lin"])
                        if site["condition"] == "grimy" and key[3]:
                            col = [v * 0.85 for v in col]
                        mixn = next((n for n in m.node_tree.nodes if n.type == "MIX"), None)
                        if mixn is not None:
                            mixn.inputs[7].default_value = (*col, 1.0)
                            if extra.get("old_fault"):               # WB-08: the first build's flat joinery: no box shade and no shading of the reveal (its own light, the paint's colour)
                                for lk in list(mixn.inputs[6].links):
                                    m.node_tree.links.remove(lk)
                                mixn.inputs[6].default_value = (1.0, 1.0, 1.0, 1.0)
                                for lk in list(pb.inputs["Base Color"].links):
                                    m.node_tree.links.remove(lk)
                                pb.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
                                pb.inputs["Specular IOR Level"].default_value = 0.0
                                pb.inputs["Emission Color"].default_value = (*col, 1.0)
                                pb.inputs["Emission Strength"].default_value = 0.6
                        else:
                            pb.inputs["Base Color"].default_value = (*col, 1.0)
                        pb.inputs["Roughness"].default_value = paint["rough"]
                        if site["condition"] == "flaking":
                            flake_paint(m, col)
                        if grime:
                            zmin = min((o.matrix_world @ v.co).z for v in o.data.vertices)
                            grime_band(m, base, zmin, Z)
                        mats_w[key] = m
                    sl.material = mats_w[key]
                elif mn in ("net_voile", "curtain", "blind"):
                    kk = (mn, base, lit)
                    if kk not in mats_w:
                        m = m0.copy()
                        pb = m.node_tree.nodes["Principled BSDF"]
                        if mn == "net_voile":
                            col = {"white": (238, 238, 232), "greyed": (208, 208, 200), "yellowed": (222, 206, 158)}[site["net"]["colour"] or "white"]
                        elif mn == "curtain":
                            cname = (site["extra"] or {}).get("colour", "cream")
                            col = tuple(T.target()["curtains"][extra_k if extra_k in ("C1", "C2") else "C1"]["colours"][cname])
                        else:
                            col = tuple(T.target()["blinds"][extra_k]["colour"]) if extra_k else (226, 224, 214)
                        cl = [float(v) for v in T.srgb_to_lin(col)]
                        # the colour factor: the glTF importer's Mix node holds it; set it by finding the Mix node's constant
                        for nd in m.node_tree.nodes:
                            if nd.type == "MIX" and nd.data_type == "RGBA":
                                try:
                                    nd.inputs[7].default_value = (*cl, 1.0)
                                    nd.inputs[6].default_value = nd.inputs[6].default_value
                                except Exception:
                                    pass
                        if night:
                            if lit:
                                if mn == "net_voile":
                                    em, sv = tuple(WARM[k_] * cl[k_] for k_ in range(3)), 0.48 * 1.0
                                    em = tuple(cl[k_] * WARM[k_] for k_ in range(3))
                                    sv = 0.48
                                elif mn == "curtain":
                                    cname = (site["extra"] or {}).get("colour", "cream")
                                    em = tuple(T.target()["curtains"][extra_k if extra_k in ("C1", "C2") else "C1"]["night_lit_emission_linear"][cname])
                                    sv = 1.0
                                else:
                                    em = tuple(T.target()["blinds"][extra_k]["night_lit_emission_linear"])
                                    sv = 1.0
                            else:
                                em, sv = tuple(cl[k_] * SODIUM[k_] for k_ in range(3)), 0.02
                            pb.inputs["Emission Color"].default_value = (*em, 1.0)
                            pb.inputs["Emission Strength"].default_value = sv
                        mats_w[kk] = m
                    sl.material = mats_w[kk]
                elif mn == "pendant_shade":
                    m = m0.copy()
                    pb = m.node_tree.nodes["Principled BSDF"]
                    if night and lit:
                        pb.inputs["Emission Color"].default_value = (*WARM, 1.0)
                        pb.inputs["Emission Strength"].default_value = 3.0
                    sl.material = m
        # the room card of this window: the kit's own room__card for an upper window; a cottage house's card is built once below
        if site["card"]["room_family"] == "UP":
            cardo = None
            for o in tmpl:
                if o.name.split(".")[0] == "room__card":
                    cardo = o.copy()
                    sc.collection.objects.link(cardo)
                    cardo.parent = root
                    cardo.matrix_parent_inverse = Matrix.Identity(4)
                    cardo.hide_render = False
                    cardo.hide_viewport = False
                    cardo.pass_index = wid
                    cardo.name = site["id"] + "|room__card"
            bk = bake_for(site)
            if cardo is not None:
                cardo.data = cardo.data.copy()
                cardo.data.materials.clear()
                if mode == "mask":
                    cardo.data.materials.append(mk["card"])
                else:
                    cardo.data.materials.append(card_material(bpy, bk, site, lit, night))
                cardo.visible_diffuse = False
                cardo.visible_glossy = False
                cardo.visible_shadow = False
        # the shared cottage cards are made after the loop

    # the cottages' shared room cards (one a house)
    done = set()
    for site in gfs:
        key = tuple(site["card"]["shared_by"])
        if key in done:
            continue
        done.add(key)
        mates = [s for s in gfs if s["id"] in key]
        bk = bake_for(site)
        lit = any(s["id"] in lit_names for s in mates)
        c = site["card"]
        W_, H_ = c["w"], c["h"]
        xl, xh = c["x_low"], c["x_low"] + W_
        zb, zt = c["z_bottom_above_crown"], c["z_bottom_above_crown"] + H_
        ypl = c["y_card_plane"]
        ypl = -abs(ypl)
        v = [(-xh, ypl, zb), (-xl, ypl, zb), (-xl, ypl, zt), (-xh, ypl, zt)]
        # west card: the viewer (east) looks along -y; his left is the HIGH Blender x... the picture's column 0 (viewer's left) is at the high street x = the low Blender x here: u increases from -xh to -xl
        me = bpy.data.meshes.new("card_" + key[0])
        me.from_pydata(v, [], [(0, 1, 2, 3)])
        uvl = me.uv_layers.new(name="UVMap")
        uvs = ((1, 0), (0, 0), (0, 1), (1, 1))
        for li, vi in zip(me.loops, range(4)):
            uvl.data[li.index].uv = uvs[vi]
        o = bpy.data.objects.new("card_" + key[0], me)
        sc.collection.objects.link(o)
        o.pass_index = window_ids[key[0]]
        me.materials.append(mk["card"] if mode == "mask" else card_material(bpy, bk, site, lit, night))
        o.visible_diffuse = False
        o.visible_glossy = False
        o.visible_shadow = False
        # the pendant in the cottage's front room, at the room's centre
        if T.room(site["room"])["pendant"]:
            pm = new_mat("pendant_gf", tuple(lin([0.93, 0.89, 0.77])), 0.9, emit=WARM if (night and lit) else None, emit_strength=3.0 if (night and lit) else 0.0)
            xcm = (xl + xh) / 2
            n = 24
            verts, faces = [], []
            z0p, z1p = c["z_bottom_above_crown"] + 1.686 + 0.3736 - 0.3736, c["z_bottom_above_crown"] + 1.926 + 0.3736 - 0.3736
            z0p, z1p = zt - 0.30 - 0.24, zt - 0.30
            yc = ypl - 0.55
            for i in range(n):
                a = 2 * math.pi * i / n
                verts.append((-xcm + 0.17 * math.cos(a), yc + 0.17 * math.sin(a), z0p))
                verts.append((-xcm + 0.105 * math.cos(a), yc + 0.105 * math.sin(a), z1p))
            for i in range(n):
                j = (i + 1) % n
                faces.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
            me2 = bpy.data.meshes.new("pendant_gf_" + key[0])
            me2.from_pydata(verts, [], faces)
            op = bpy.data.objects.new("pendant_gf_" + key[0], me2)
            sc.collection.objects.link(op)
            me2.materials.append(mk["cloth"] if mode == "mask" else pm)

    # ---------------------------------------------------------------- world and lights
    world = bpy.data.worlds.new("w")
    sc.world = world
    world.use_nodes = True
    wn = world.node_tree
    bg = wn.nodes["Background"]
    sky_s = float(extra.get("sky_strength", 1.0))
    env = wn.nodes.new("ShaderNodeTexEnvironment")
    if os.path.exists(T.SKY_HDRI):
        env.image = bpy.data.images.load(T.SKY_HDRI, check_existing=True)
        wn.links.new(env.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = sky_s * (0.15 if night else 1.0)
    if mode == "mask":
        bg.inputs["Strength"].default_value = 0.0
        wn.links.remove(bg.inputs["Color"].links[0]) if bg.inputs["Color"].links else None
        bg.inputs["Color"].default_value = (0, 0, 0, 1)
    if night and mode != "mask":
        for lx in lamps:
            spl = bpy.data.lights.new("lamp_%g" % lx, "SPOT")
            spl.color = SODIUM
            spl.energy = float(extra.get("lamp_w", 4000.0)) * (float(extra.get("cottage_lamp_scale", COTTAGE_LAMP_SCALE)) if lx in COTTAGE_LAMPS else 1.0)
            spl.spot_size = math.radians(92)
            spl.spot_blend = 0.5
            spl.shadow_soft_size = 0.15
            lo = bpy.data.objects.new("lamp_light_%g" % lx, spl)
            sc.collection.objects.link(lo)
            lo.location = (-lx, -3.78, 4.52)
            lo.rotation_euler = Euler((0.0, 0.0, 0.0))
            lo.visible_camera = False          # no lit stand-in lamp is ever seen (unit 7's night fault)
            lo.visible_glossy = False
            lo.visible_transmission = False
        # the stand-in street's pools must not be reflected in the night glass as a burnt bar (unit 7's close reviews: the lamps' pool on the far footway and the road): road and both footways are out of glossy rays at night
        for nm in ("road", "footway_E", "footway_W"):
            bpy.data.objects[nm].visible_glossy = False
        for nm in [x for x in os.environ.get("LEDGER_GATE_NOGLOSSY", "").split(",") if x]:
            if nm in bpy.data.objects:
                bpy.data.objects[nm].visible_glossy = False

    # ---------------------------------------------------------------- the camera
    camd = bpy.data.cameras.new("cam")
    camd.sensor_fit = "VERTICAL"
    camd.angle_y = math.radians(cam["vfov"])
    camd.clip_start, camd.clip_end = 0.05, 300.0
    co = bpy.data.objects.new("cam", camd)
    sc.collection.objects.link(co)
    eye_b = Vector(bl(cam["eye"]))
    if "aim" in cam:
        d_b = Vector(bl(cam["aim"])) - eye_b
    else:
        yaw, pitch = math.radians(cam["yaw"]), math.radians(cam["pitch"])
        d_s = (math.cos(yaw) * math.cos(pitch), math.sin(yaw) * math.cos(pitch), -math.sin(pitch))
        d_b = Vector((-d_s[0], d_s[1], d_s[2]))
    co.location = eye_b
    co.rotation_euler = d_b.to_track_quat("-Z", "Y").to_euler()
    sc.camera = co
    json.dump({"view": view_name, "state": state, "eye_street_m": list(cam["eye"]), "vfov_deg": cam["vfov"], "resolution": list(res), "direction_blender": list(d_b.normalized())},
              open(os.path.splitext(out_png)[0] + ".camera.json", "w"), indent=1)
    # ---------------------------------------------------------------- render
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.image_settings.color_depth = "8"
    sc.render.filepath = out_png
    if mode == "mask":
        sc.cycles.samples = 1
        sc.cycles.use_denoising = False
        sc.cycles.use_adaptive_sampling = False
        sc.cycles.filter_width = 0.01
        sc.render.dither_intensity = 0.0
        sc.view_settings.view_transform = "Raw"
        sc.view_settings.look = "None"
        # window number into G: every object of a window carries it as its pass index: the mask render writes it through the emission colour of a per-window material
        for o in list(bpy.data.objects):
            if o.type == "MESH" and o.pass_index > 0:
                for i, sl in enumerate(o.material_slots):
                    m0 = sl.material
                    if m0 is None or not m0.name.startswith("mk_"):
                        continue
                    sl.link = "OBJECT"
                    key = (m0.name, o.pass_index)
                    nm = "%s_w%d" % (m0.name, o.pass_index)
                    m2 = bpy.data.materials.get(nm)
                    if m2 is None:
                        m2 = m0.copy()
                        m2.name = nm
                        e = next(n for n in m2.node_tree.nodes if n.type == "EMISSION")
                        col = list(e.inputs["Color"].default_value)
                        col[1] = o.pass_index / 255.0
                        e.inputs["Color"].default_value = col
                    sl.material = m2
    else:
        sc.cycles.samples = samples
        sc.cycles.use_denoising = True
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
        sc.cycles.use_adaptive_sampling = True
        sc.cycles.adaptive_threshold = 0.02
        sc.cycles.max_bounces = 8
        sc.cycles.transmission_bounces = 8
        sc.cycles.transparent_max_bounces = 24
        sc.cycles.sample_clamp_indirect = 10.0
        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
    if extra.get("post"):                       # an experiment's hook (the builder's own tests): a function of bpy called before the render
        extra["post"](bpy)
    t1 = time.time()
    bpy.ops.render.render(write_still=True)
    return round(time.time() - t1, 1), rec


GRIME_PARTS = ("paint_joinery__lower_bottom_rail", "paint_joinery__oak_sill")


def grime_band(m, base, z_lo_kit, root_z):
    """Target 4.2's grime band (the close review's narrow point 3): on a grimy window the lowest 30 mm of the bottom rail (the kit's own z from the part's lowest point; `root_z` is the window's sill height in the street) and the oak
    sill's top faces are x 0.75 of the paint, on top of the x 0.85 the lower rail and sill already carry. Only grimy windows: a sound house's bottom rail is clean (the glb carries the default paint of every house of its kind,
    so the band is the gate's, by the house's condition, and is listed in hw_manifest.json for the PC)."""
    import bpy
    nt = m.node_tree
    pb = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    msk = nt.nodes.new("ShaderNodeMath")
    if base == "paint_joinery__oak_sill":
        nt.links.new(geo.outputs["Normal"], sep.inputs["Vector"])
        msk.operation = "GREATER_THAN"
        msk.inputs[1].default_value = 0.5
    else:
        nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
        msk.operation = "LESS_THAN"
        msk.inputs[1].default_value = root_z + z_lo_kit + GRIME_BAND_M
    nt.links.new(sep.outputs["Z"], msk.inputs[0])
    fac = nt.nodes.new("ShaderNodeMath")                    # 1 - (1 - 0.75) x mask
    fac.operation = "MULTIPLY_ADD"
    fac.inputs[1].default_value = -(1.0 - GRIME_BAND_FACTOR)
    fac.inputs[2].default_value = 1.0
    nt.links.new(msk.outputs["Value"], fac.inputs[0])
    grey = nt.nodes.new("ShaderNodeCombineColor")
    for nm in ("Red", "Green", "Blue"):
        nt.links.new(fac.outputs["Value"], grey.inputs[nm])
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs[0].default_value = 1.0
    cur = pb.inputs["Base Color"].links[0].from_socket if pb.inputs["Base Color"].links else None
    if cur is not None:
        nt.links.new(cur, mul.inputs[6])
    else:
        mul.inputs[6].default_value = pb.inputs["Base Color"].default_value
    nt.links.new(grey.outputs["Color"], mul.inputs[7])
    nt.links.new(mul.outputs[2], pb.inputs["Base Color"])


def flake_paint(m, col):
    """white_flaking (target 4.2): about 12 per cent of the area of the lower 250 mm of the frame (the lower rails, the sill, the stiles' feet) flaked to grey primer (66, 60, 54) or bare timber (96, 66, 40)."""
    nt = m.node_tree
    pb = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 38.0
    nz.inputs["Detail"].default_value = 4.0
    rmp = nt.nodes.new("ShaderNodeMapRange")
    rmp.inputs["From Min"].default_value = 0.56
    rmp.inputs["From Max"].default_value = 0.60
    low = nt.nodes.new("ShaderNodeMath")
    low.operation = "LESS_THAN"
    low.inputs[1].default_value = 0.25
    both = nt.nodes.new("ShaderNodeMath")
    both.operation = "MULTIPLY"
    kind = nt.nodes.new("ShaderNodeTexNoise")
    kind.inputs["Scale"].default_value = 9.0
    krp = nt.nodes.new("ShaderNodeMapRange")
    krp.inputs["From Min"].default_value = 0.45
    krp.inputs["From Max"].default_value = 0.55
    primer = nt.nodes.new("ShaderNodeMix")
    primer.data_type = "RGBA"
    primer.inputs[6].default_value = (*T.srgb_to_lin((66, 60, 54)), 1.0)
    primer.inputs[7].default_value = (*T.srgb_to_lin((96, 66, 40)), 1.0)
    cur = pb.inputs["Base Color"].links[0].from_socket if pb.inputs["Base Color"].links else None
    fl = nt.nodes.new("ShaderNodeMix")
    fl.data_type = "RGBA"
    nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
    nt.links.new(geo.outputs["Position"], nz.inputs["Vector"])
    nt.links.new(geo.outputs["Position"], kind.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], rmp.inputs["Value"])
    nt.links.new(sep.outputs["Z"], low.inputs[0])
    nt.links.new(rmp.outputs["Result"], both.inputs[0])
    nt.links.new(low.outputs["Value"], both.inputs[1])
    nt.links.new(kind.outputs["Fac"], krp.inputs["Value"])
    nt.links.new(krp.outputs["Result"], primer.inputs[0])
    nt.links.new(both.outputs["Value"], fl.inputs[0])
    if cur is not None:
        nt.links.new(cur, fl.inputs[6])
    else:
        fl.inputs[6].default_value = (*col, 1.0)
    nt.links.new(primer.outputs[2], fl.inputs[7])
    nt.links.new(fl.outputs[2], pb.inputs["Base Color"])


def card_material(bpy, bk, site, lit, night):
    """The card's emission: the baked picture (sRGB) x the state's brightness; a lit landing never emits less than the target's floor (landing_bulb); no bake (the window is seen under 11 degrees from its
    wall: no ray reaches the card): a plain dark matt."""
    m = bpy.data.materials.new("card_" + site["id"])
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(em.outputs[0], out.inputs[0])
    if bk is None:
        em.inputs["Color"].default_value = (0.02, 0.02, 0.02, 1.0)
        em.inputs["Strength"].default_value = 1.0
        return m
    path, st = bk
    ti = nt.nodes.new("ShaderNodeTexImage")
    ti.image = bpy.data.images.load(path, check_existing=True)
    ti.image.colorspace_settings.name = "sRGB"
    ti.interpolation = "Linear"
    ti.extension = "EXTEND"
    nt.links.new(ti.outputs["Color"], em.inputs["Color"])
    em.inputs["Strength"].default_value = BRIGHTNESS[st]
    if st == "night_lit" and T.room(site["room"])["type"] == "landing":
        fl = T.target()["rooms"]["lights_by_state"]["landing_bulb"]["card_emission_floor_linear"]
        mx = nt.nodes.new("ShaderNodeVectorMath")
        mx.operation = "MAXIMUM"
        mu = nt.nodes.new("ShaderNodeVectorMath")
        mu.operation = "SCALE"
        mu.inputs["Scale"].default_value = BRIGHTNESS[st]
        mx.inputs[1].default_value = fl
        nt.links.new(ti.outputs["Color"], mu.inputs[0])
        nt.links.new(mu.outputs["Vector"], mx.inputs[0])
        nt.links.new(mx.outputs["Vector"], em.inputs["Color"])
        em.inputs["Strength"].default_value = 1.0
    return m
