"""The gate in the cloud (target section 3, last paragraph): what the game will show from each review camera, without Unreal.

Used by build_ritas.py (stage `gate`). For each camera and state:
  1. the card picture is baked through tools/ue/make_interior_material.py's `trace` (imported, not rewritten): for every pixel of the card the card point and the eye go
     through `trace`, and the room picture is sampled at the returned (u, v), bilinear with mips; the card's emission is that picture times the state's brightness
     (day 0.15, night 0.7);
  2. the front (ritas_front.glb, with the night lattice at night), the display (ritas_display.glb) and the glass are rendered in Blender at 2560 x 1440 from the camera;
     the card is a flat quad behind them whose emission is the baked picture. The glass is a plain transmissive surface (a mix of a clear pane and a transparent one:
     all of the pane's reflectance by day, 0.2 of it at night: the look file's glass_specular_night); the game's own glass is the game's.
Frames: the front model's (x_m = 18 - street x, y_m = street y - 5.295, z_m = street z - 0.10), the card at y_m 0.58, x_m -2.65..2.65, z_m 0.55..2.95.
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

# the game's rule, imported
_spec = importlib.util.spec_from_file_location("make_interior_material", os.path.join(REPO, "tools", "ue", "make_interior_material.py"))
MIM = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MIM)
trace = MIM.trace

W, H, D = 5.3, 2.4, 4.5
CAMD = 5.3
# the spill's receivers: the window frame and the door frame stand OUT of the display's light channel, as the game has it (shop-interiors.json lit_note: "the window bars are not on that
# channel, so they no longer flare"; try 1 read "the window bars" as the night lattice only, 13 Oct, close review fault 4)
SPILL_OFF = ("win_", "frame_", "door_jamb_", "door_frame_head", "band_", "sil_sill")
SPILL_POS = (0.975, 0.10, 2.30)        # the stand-in rect light, model frame: 0.10 behind the wall face, z 2.30 (street review N1): the whole rect stands 50 mm or more behind the glass
PIERS = {"x": ((-3.0, -2.65), (2.65, 3.0)), "y": (0.0, 0.30), "z": (0.0, 3.56)}     # the brick piers behind the pilasters (sw_front.PIERS_X; street review N2)
CARD_X0, CARD_Y, CARD_BOTTOM = 15.35, 5.875, 0.65
CARD_BOTTOM_M = CARD_BOTTOM - 0.10          # the card's bottom in the front model's z (above the footway)
BAY_MID_X = 18.0
Y_WALL = 5.295
FOOT = 0.10
BRIGHTNESS = {"day": 0.15, "night_lit": 0.7, "night_dark": 0.7}
VFOV = {"STREET_SQUARE": 39.0, "STREET_30": 39.0, "CLOSE_35": 60.0, "CLOSE_35_B": 60.0}
RES = tuple(int(v) for v in os.environ.get("LEDGER_GATE_RES", "2560x1440").split("x"))
CARD_PX = (2560, 1161)           # the card is 5.3 x 2.4 m: 483 px a metre


def lin(c):
    c = np.asarray(c, np.float32)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def srgb(l):
    l = np.clip(l, 0, 1)
    return np.where(l <= 0.0031308, l * 12.92, 1.055 * l ** (1 / 2.4) - 0.055)


def eye_card(eye_street):
    return (eye_street[0] - CARD_X0, eye_street[1] - CARD_Y, eye_street[2] - CARD_BOTTOM)


def to_model(p):
    """street (x, y, z above the crown) -> the front model's frame (x_m to the viewer's right, y_m out from the wall toward -y, z_m above the footway)."""
    return (BAY_MID_X - p[0], p[1] - Y_WALL, p[2] - FOOT)


# ------------------------------------------------------------------------------------------------------------- the bake
def _bake_rows(args):
    j0, j1, ex, ey, ez = args
    nw, nh = CARD_PX
    out = np.empty((j1 - j0, nw, 2), np.float32)
    for j in range(j0, j1):
        zc = H - (j + 0.5) / nh * H
        for i in range(nw):
            xc = W - (i + 0.5) / nw * W            # column 0 is the card's HIGH x: the viewer's left on an east card
            u, v = trace((xc, 0.0, zc), (ex, ey, ez), (W, H, D), CAMD, 1)
            out[j - j0, i, 0] = u
            out[j - j0, i, 1] = v
    return j0, out


def uv_map(eye_street, jobs=4):
    """(u, v) of the room picture for every card pixel, through the game's `trace` (the Python function, called per pixel)."""
    from multiprocessing import Pool
    ex, ey, ez = eye_card(eye_street)
    nh = CARD_PX[1]
    step = 24
    chunks = [(j, min(nh, j + step), ex, ey, ez) for j in range(0, nh, step)]
    uv = np.empty((nh, CARD_PX[0], 2), np.float32)
    with Pool(jobs) as p:
        for j0, o in p.imap_unordered(_bake_rows, chunks):
            uv[j0:j0 + o.shape[0]] = o
    return uv


def mips(img):
    """A box-filtered mip chain of a float image (h, w, 3)."""
    chain = [img]
    while min(chain[-1].shape[:2]) > 8:
        a = chain[-1]
        h2, w2 = a.shape[0] // 2 * 2, a.shape[1] // 2 * 2
        a = a[:h2, :w2]
        chain.append((a[0::2, 0::2] + a[1::2, 0::2] + a[0::2, 1::2] + a[1::2, 1::2]) / 4.0)
    return chain


def sample_mips(chain, uv, base_wh):
    """Bilinear sample with mips (trilinear between two levels by the per-pixel footprint). uv in 0..1 (v down)."""
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


def bake_card(eye_street, picture_png, brightness, out_png, uv=None, jobs=4):
    """The card's emission picture for one camera and state: the room picture (sRGB) sampled through trace with mips; written as 8-bit sRGB WITHOUT the brightness
    (the render's emission strength carries it) and returned together with the linear-light composite (picture x brightness)."""
    if uv is None:
        uv = uv_map(eye_street, jobs)
    pic = np.asarray(Image.open(picture_png).convert("RGB")).astype(np.float32) / 255.0
    chain = mips(lin(pic))
    lin_img = sample_mips(chain, uv, (pic.shape[1], pic.shape[0]))
    srgb8 = (srgb(lin_img) * 255.0 + 0.5).astype(np.uint8)
    Image.fromarray(srgb8).save(out_png)
    return uv, lin_img


def composite_luma(lin_img, brightness):
    """Rec.709 luma (0..255) of the card picture x brightness, tone-mapped Standard (the sRGB curve), glass reflection off."""
    c = srgb(np.clip(lin_img * brightness, 0, 1)) * 255.0
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


# ------------------------------------------------------------------------------------------------------------- the render
def render_view(cam_name, cam_def, state, card_png, out_png, front_glb, grille_glb, display_glb, hdri, samples=64, log=print, extra=None, res=None, glass_refl=None, mode="beauty", column_pngs=None):
    import bpy
    from mathutils import Vector, Matrix
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    night = state != "day"
    # --- the front, the display, the lattice
    def load(path):
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=path)
        return [o for o in bpy.data.objects if o not in before]
    front = load(front_glb)
    disp = load(display_glb)
    for o in disp:
        if o.parent is None:
            o.location += Vector((BAY_MID_X - 17.025 + 0.0, 0.0, 0.0)) if False else Vector((0.975, -0.025, 0.600))
    lattice = load(grille_glb) if night else []
    # empties from the importer carry the Y-up conversion; apply the display's offset on the roots only
    # glass: a mix of a clear pane (all the glass's reflectance) and a transparent one, 1.0 by day and 0.2 at night
    refl = (0.2 if night else 1.0) if glass_refl is None else glass_refl
    res = res or RES
    gm = bpy.data.materials.new("gate_glass")
    gm.use_nodes = True
    nt = gm.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mixn = nt.nodes.new("ShaderNodeMixShader")
    mixn.inputs[0].default_value = refl
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    gl = nt.nodes.new("ShaderNodeBsdfGlass")
    gl.inputs["IOR"].default_value = 1.5
    gl.inputs["Roughness"].default_value = 0.02
    gl.inputs["Color"].default_value = (0.97, 0.99, 0.98, 1.0)
    nt.links.new(tr.outputs[0], mixn.inputs[1])
    nt.links.new(gl.outputs[0], mixn.inputs[2])
    if not night:
        # by day Cycles' glass stops the sky's shadow rays, so the display got no direct sky light (close review, narrow 1, tested there): for a shadow ray the pane is clear, as real
        # glass is to the sky's light. Camera, reflection and refraction rays still meet the glass as before
        lpn = nt.nodes.new("ShaderNodeLightPath")
        tr2 = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix2 = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(lpn.outputs["Is Shadow Ray"], mix2.inputs[0])
        nt.links.new(mixn.outputs[0], mix2.inputs[1])
        nt.links.new(tr2.outputs[0], mix2.inputs[2])
        nt.links.new(mix2.outputs[0], out.inputs[0])
    else:
        nt.links.new(mixn.outputs[0], out.inputs[0])
    for o in front + disp:
        if o.type == "MESH":
            for slot in o.material_slots:
                if slot.material and slot.material.name.lower().startswith("glass") and "row" not in slot.material.name.lower():
                    slot.material = gm
    # the door's OPEN sign by day, CLOSED at night (the card is turned over)
    for o in front:
        if o.type == "MESH" and o.name.startswith("door_sign"):
            for slot in o.material_slots:
                m = slot.material
                if m and night:
                    for n in m.node_tree.nodes:
                        if n.type == "TEX_IMAGE":
                            n.image = bpy.data.images.load(os.path.join(os.path.dirname(os.path.dirname(card_png)), "paper", "K03b", "K03b_A_basecolour.png"), check_existing=True)
    # --- the card: emission = the baked picture x the state's brightness; it does not light the scene (the game's card is unlit; Lumen's light is owed on the PC)
    me = bpy.data.meshes.new("card")
    x0, x1, z0, z1, yc = -W / 2, W / 2, 0.55, 2.95, CARD_Y - Y_WALL
    me.from_pydata([(x0, yc, z0), (x1, yc, z0), (x1, yc, z1), (x0, yc, z1)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for loop, (a, b) in zip(me.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        uv.data[loop.index].uv = (a, b)
    card = bpy.data.objects.new("card", me)
    sc.collection.objects.link(card)
    cm = bpy.data.materials.new("card_emission")
    cm.use_nodes = True
    cnt = cm.node_tree
    for n in list(cnt.nodes):
        cnt.nodes.remove(n)
    ti = cnt.nodes.new("ShaderNodeTexImage")
    ti.image = bpy.data.images.load(card_png, check_existing=True)
    ti.image.colorspace_settings.name = "sRGB"
    ti.interpolation = "Linear"
    em = cnt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = BRIGHTNESS[state]
    co = cnt.nodes.new("ShaderNodeOutputMaterial")
    cnt.links.new(ti.outputs["Color"], em.inputs["Color"])
    cnt.links.new(em.outputs[0], co.inputs[0])
    me.materials.append(cm)
    card.visible_diffuse = False
    card.visible_glossy = False
    card.visible_shadow = False
    # --- reveals between the wall and the card so a grazing ray finds a surface: top and under the bed are dark and matt; the SIDES (and the display's two return walls) are an emission of
    # the room picture's own side-wall front column (picture u 0 to 8 px for the left wall, 4088 to 4096 for the right) at the same height, times the state's brightness, so the wall
    # meets the card without a step (13 Oct, close review fault 3: from CLOSE_35_B a third of the window was a black slab, the 0.61 m gap beside the card's edge)
    dark = bpy.data.materials.new("reveal")
    dark.use_nodes = True
    dark.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)

    def wall_material(side):
        m = bpy.data.materials.new("side_wall_" + side)
        m.use_nodes = True
        t = m.node_tree
        for n in list(t.nodes):
            t.nodes.remove(n)
        if not column_pngs:
            return dark
        geo = t.nodes.new("ShaderNodeNewGeometry")
        sep = t.nodes.new("ShaderNodeSeparateXYZ")
        mth = t.nodes.new("ShaderNodeMath")          # v = (z - card bottom) / card height
        mth.operation = "MULTIPLY_ADD"
        mth.inputs[1].default_value = 1.0 / H
        mth.inputs[2].default_value = -CARD_BOTTOM_M / H
        com = t.nodes.new("ShaderNodeCombineXYZ")
        com.inputs["X"].default_value = 0.5
        tex = t.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(column_pngs[side], check_existing=True)
        tex.image.colorspace_settings.name = "sRGB"
        tex.interpolation = "Linear"
        tex.extension = "EXTEND"
        emn = t.nodes.new("ShaderNodeEmission")
        emn.inputs["Strength"].default_value = BRIGHTNESS[state]
        outn = t.nodes.new("ShaderNodeOutputMaterial")
        t.links.new(geo.outputs["Position"], sep.inputs["Vector"])
        t.links.new(sep.outputs["Z"], mth.inputs[0])
        t.links.new(mth.outputs[0], com.inputs["Y"])
        t.links.new(com.outputs["Vector"], tex.inputs["Vector"])
        t.links.new(tex.outputs["Color"], emn.inputs["Color"])
        t.links.new(emn.outputs[0], outn.inputs[0])
        return m
    wall_l, wall_r = wall_material("l"), wall_material("r")

    def slab(name, a0, a1, b0, b1, c0, c1, mat=None):
        bpy.ops.mesh.primitive_cube_add(size=1, location=((a0 + a1) / 2, (b0 + b1) / 2, (c0 + c1) / 2))
        o = bpy.context.object
        o.name = name
        o.scale = (a1 - a0, b1 - b0, c1 - c0)
        o.data.materials.append(mat or dark)
        return o
    ycard = yc
    slab("reveal_l", -W / 2 - 0.012, -W / 2, 0.0, ycard + 0.02, 0.0, 2.97, wall_l)
    slab("reveal_r", W / 2, W / 2 + 0.012, 0.0, ycard + 0.02, 0.0, 2.97, wall_r)
    slab("reveal_top", -W / 2, W / 2, 0.0, ycard + 0.02, 2.95, 2.97)
    slab("reveal_floor", -W / 2, W / 2, 0.02, ycard + 0.02, 0.0, 0.55)
    for o in disp:
        if o.type == "MESH" and o.name.startswith("return_wall_"):
            o.data.materials.clear()
            o.data.materials.append(wall_l if o.name.startswith("return_wall_l") else wall_r)
    # --- the street: wall, footway, road, far footway
    brick = bpy.data.materials.new("brick")
    brick.use_nodes = True
    bn = brick.node_tree
    bp = bn.nodes["Principled BSDF"]
    tc = bn.nodes.new("ShaderNodeTexCoord")
    sp = bn.nodes.new("ShaderNodeSeparateXYZ")
    cb = bn.nodes.new("ShaderNodeCombineXYZ")
    br = bn.nodes.new("ShaderNodeTexBrick")
    bn.links.new(tc.outputs["Object"], sp.inputs["Vector"])
    bn.links.new(sp.outputs["X"], cb.inputs["X"])
    bn.links.new(sp.outputs["Z"], cb.inputs["Y"])
    bn.links.new(cb.outputs["Vector"], br.inputs["Vector"])
    br.offset = 0.5
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = 0.215
    br.inputs["Row Height"].default_value = 0.075
    br.inputs["Mortar Size"].default_value = 0.010
    br.inputs["Mortar Smooth"].default_value = 0.2
    br.inputs["Color1"].default_value = (*lin(np.array([0.50, 0.30, 0.22])), 1.0)
    br.inputs["Color2"].default_value = (*lin(np.array([0.43, 0.25, 0.18])), 1.0)
    br.inputs["Mortar"].default_value = (*lin(np.array([0.58, 0.55, 0.50])), 1.0)
    bn.links.new(br.outputs["Color"], bp.inputs["Base Color"])
    bp.inputs["Roughness"].default_value = 0.92
    paving = bpy.data.materials.new("paving")
    paving.use_nodes = True
    paving.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*lin(np.array([0.50, 0.50, 0.48])), 1.0)
    paving.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.85
    road = bpy.data.materials.new("road")
    road.use_nodes = True
    road.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*lin(np.array([0.22, 0.22, 0.22])), 1.0)
    road.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
    def plane(name, v, m):
        me2 = bpy.data.meshes.new(name)
        me2.from_pydata(v, [], [(0, 1, 2, 3)])
        o = bpy.data.objects.new(name, me2)
        sc.collection.objects.link(o)
        o.data.materials.append(m)
        return o
    xs = 14.0
    # wall face at y 0: left and right of the bay (viewer's left = -x_m), above the cornice; the shop's own opening stays open behind the front
    plane("wall_l", [(-xs, 0.0, 0.0), (-3.0, 0.0, 0.0), (-3.0, 0.0, 12.0), (-xs, 0.0, 12.0)], brick)
    plane("wall_r", [(3.0, 0.0, 0.0), (xs, 0.0, 0.0), (xs, 0.0, 12.0), (3.0, 0.0, 12.0)], brick)
    plane("wall_top", [(-3.0, 0.0, 3.56), (3.0, 0.0, 3.56), (3.0, 0.0, 12.0), (-3.0, 0.0, 12.0)], brick)
    kerb_y = 3.63 - Y_WALL
    plane("footway", [(-xs, kerb_y, 0.0), (xs, kerb_y, 0.0), (xs, 0.0, 0.0), (-xs, 0.0, 0.0)], paving)
    plane("road", [(-xs, -3.0 - Y_WALL, -FOOT), (xs, -3.0 - Y_WALL, -FOOT), (xs, kerb_y, -FOOT), (-xs, kerb_y, -FOOT)], road)
    plane("far_footway", [(-xs, -9.0 - Y_WALL, 0.0), (xs, -9.0 - Y_WALL, 0.0), (xs, -3.0 - Y_WALL, 0.0), (-xs, -3.0 - Y_WALL, 0.0)], paving)

    def block(name, x0, x1, y0, y1, z0, z1, m):
        """A closed box in the model frame (vertices in world coordinates, so the brick shader's object coordinates are the wall's own)."""
        v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        me2 = bpy.data.meshes.new(name)
        me2.from_pydata(v, [], f)
        o = bpy.data.objects.new(name, me2)
        sc.collection.objects.link(o)
        o.data.materials.append(m)
        return o
    # a brick pier behind each pilaster (13 Oct, street review N2): the pilaster's shaft and core stop at x 2.970 and the street model's wall opening is the whole bay, so the outer
    # 30 to 54 mm of the bay was open to the sky at STREET_30; the game's street facade has to close the same gap (owed on the PC)
    for k, (xa, xb) in enumerate(PIERS["x"]):
        block("pier_%d" % k, xa, xb, PIERS["y"][0], PIERS["y"][1], PIERS["z"][0], PIERS["z"][1], brick)
    # --- the camera
    eye = to_model(cam_def["eye_street_m"])
    aim = to_model(cam_def["aim_street_m"])
    cam = bpy.data.cameras.new("cam")
    cam.sensor_fit = "VERTICAL"
    cam.angle_y = math.radians(VFOV[cam_name])
    cam.clip_start, cam.clip_end = 0.05, 100.0
    co_ = bpy.data.objects.new("cam", cam)
    sc.collection.objects.link(co_)
    co_.location = Vector(eye)
    co_.rotation_euler = (Vector(aim) - Vector(eye)).to_track_quat("-Z", "Y").to_euler()
    sc.camera = co_
    bpy.context.view_layer.update()
    fwd = co_.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
    to_aim = (Vector(aim) - Vector(eye)).normalized()
    cam_rec = {"camera": cam_name, "state": state, "eye_street_m": [BAY_MID_X - co_.location.x, co_.location.y + Y_WALL, co_.location.z + FOOT],
               "defined_eye_street_m": list(cam_def["eye_street_m"]), "aim_street_m": list(cam_def["aim_street_m"]),
               "aim_error_deg": round(math.degrees(fwd.angle(to_aim)), 4), "vfov_deg": round(math.degrees(cam.angle_y), 4), "defined_vfov_deg": VFOV[cam_name],
               "resolution": list(res)}
    json.dump(cam_rec, open(os.path.splitext(out_png)[0] + ".camera.json", "w"), indent=1)
    # --- light: day = an overcast sky; night = sodium lamps (linear 1.0, 0.25, 0.0) and the display's spill (a rect light in the window head, tipped 62 degrees down)
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    wn = w.node_tree
    bg = wn.nodes["Background"]
    if not night and hdri and os.path.exists(hdri):
        env = wn.nodes.new("ShaderNodeTexEnvironment")
        env.image = bpy.data.images.load(hdri, check_existing=True)
        wn.links.new(env.outputs["Color"], bg.inputs["Color"])
        bg.inputs["Strength"].default_value = 1.0
    elif not night:
        bg.inputs["Color"].default_value = (0.62, 0.68, 0.78, 1)
        bg.inputs["Strength"].default_value = 1.0
    else:
        bg.inputs["Color"].default_value = (0.004, 0.005, 0.009, 1)
        bg.inputs["Strength"].default_value = 1.0
    if night:
        for lx in (8.0, 28.0):
            sp = bpy.data.lights.new("lamp_%g" % lx, "SPOT")
            sp.color = (1.0, 0.25, 0.0)
            sp.energy = (extra or {}).get("lamp_w", 4000.0)
            sp.spot_size = math.radians(92)
            sp.spot_blend = 0.5
            sp.shadow_soft_size = 0.15
            lo = bpy.data.objects.new("lamp", sp)
            sc.collection.objects.link(lo)
            lo.location = Vector(to_model((lx, -4.1, 4.78)))
            lo.rotation_euler = (Vector(to_model((lx, -4.1, 0.0))) - lo.location).to_track_quat("-Z", "Y").to_euler()
        # the display's spill: 350 lm rect light in the window head, tipped 62 degrees down (lighting channel 1: the window bars are not on it; here it lights the display and what is in front)
        rl = bpy.data.lights.new("spill", "AREA")
        rl.shape = "RECTANGLE"
        rl.size, rl.size_y = 3.2, 0.18
        rl.color = (1.0, 0.97, 0.92)
        rl.energy = (extra or {}).get("spill_w", 60.0)
        ro = bpy.data.objects.new("spill", rl)
        sc.collection.objects.link(ro)
        # centred at y 0.10 behind the wall face and z 2.30 (13 Oct, street review N1; try 1 had it at y -0.02, z 2.36, so its front edge stood 63 mm IN FRONT of the glass, its emitting face
        # was seen from the street and it lit the window frame from in front: the burnt bar, the glowing mullions, the bright pavement). Now the whole rect, tipped as before, stands 50 mm or
        # more behind the glass's inner face, and the light itself is invisible to the camera, to glossy rays and to transmission rays
        ro.location = SPILL_POS
        ro.visible_camera = False
        ro.visible_glossy = False
        ro.visible_transmission = False
        # an area light shines along its own -Z; tipped about x by -28 degrees it shines down and out toward the street: 62 degrees below the horizontal, as the spec's rect light
        ro.rotation_euler = (math.radians(-28.0), 0.0, 0.0)
        # lighting channel 1 (the game's): the spill lights the display, the front and the street but not the night grille's lattice (the bars would flare)
        recv = bpy.data.collections.new("spill_receivers")
        sc.collection.children.link(recv)
        for o in list(bpy.data.objects):
            if o.type == "MESH" and o not in lattice and o.name != "card" and not o.name.startswith(SPILL_OFF):
                recv.objects.link(o)          # the window frame, the door frame and the band stand out of the spill's channel, with the lattice (the game's lighting channel)
        ro.light_linking.receiver_collection = recv
    # --- the glass mask (a check's render, 13 Oct): every pixel where the window's glass is the first thing the camera sees white, everything else (frame, mullions, beads, lattice, display,
    # wall) black: the window-glass pixels without the frame
    if mode in ("mask_glass", "mask_glass_open"):
        def flat(c):
            m = bpy.data.materials.new("flat")
            m.use_nodes = True
            t = m.node_tree
            for n in list(t.nodes):
                t.nodes.remove(n)
            e = t.nodes.new("ShaderNodeEmission")
            e.inputs["Color"].default_value = (*c, 1.0)
            o2 = t.nodes.new("ShaderNodeOutputMaterial")
            t.links.new(e.outputs[0], o2.inputs[0])
            return m
        white, black = flat((1, 1, 1)), flat((0, 0, 0))
        for o in bpy.data.objects:
            if o.type == "MESH":
                o.data.materials.clear()
                o.data.materials.append(white if o.name.startswith("win_glass_lower") else black)
                if mode == "mask_glass_open" and o in lattice:
                    o.hide_render = True          # the glass as it is where the lattice's gaps are: the lattice left out
            elif o.type == "LIGHT":
                o.hide_render = True
        sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
        sc.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 1
        sc.cycles.use_denoising = False
        sc.cycles.use_adaptive_sampling = False
        sc.cycles.filter_width = 0.01
        sc.view_settings.view_transform = "Standard"
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.resolution_percentage = 100
        sc.render.image_settings.file_format = "PNG"
        sc.render.image_settings.color_mode = "RGB"
        sc.render.filepath = out_png
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        return round(time.time() - t0, 1)
    # --- render
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.02
    sc.cycles.max_bounces = 8
    sc.cycles.transmission_bounces = 8
    sc.cycles.sample_clamp_indirect = 10.0
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.filepath = out_png
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    return round(time.time() - t0, 1)
