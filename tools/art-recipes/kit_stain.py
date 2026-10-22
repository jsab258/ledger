"""A kit piece's named stains baked onto its own unwrap, for the kit's shared material to lay over.

    F:/LedgerTools/bpyenv/Scripts/python.exe tools/art-recipes/kit_stain.py production/specs/kit-wear/lamp_post_C.json
    python tools/art-recipes/kit_stain.py --selftest      # the drawing, without Blender

WHY, 22 October 2026 (his ruling of 21 October: the concrete columns "weathered"; his message of 22
October: "then the lamp's staining"). Two tries drew rain streaks in the kit's master material as a
world-aligned map of runs; both read as an even grain with no source. The design names its stains
and where they come from (lime under the arm, rust under the plate's screws and the spigot, algae
on the shaded face), so they are drawn there, once, in the piece's own picture
(production/research/street-wear/LAMP-STAINING-BAKE-2026-10-22.md).

THE METHOD:
  * the slot's faces get their own unwrap in the piece's first UV (nothing else on them reads it:
    the kit material's detail and streaks are world-aligned);
  * Cycles bakes each texel's position and facing in the piece's own frame into float pictures;
  * the stains are drawn on those in numpy: seeded runs (a position across the face, a width, a
    length, a slight meander, fading downward from their source) and patches by a value noise;
  * one RGBA picture is written: the stain's colour and, in alpha, how much of it; the kit material
    lays it over the slot's own colour by StainStrength (tools/ue/make_kit_materials.py);
  * the piece's game copy is written again with only that unwrap changed.
"""
import json
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def vnoise(np, p, cell, seed):
    """Value noise in [0, 1] at points p (N x 3, metres), lattice spacing cell metres, two octaves."""
    out = np.zeros(len(p))
    amp, total = 1.0, 0.0
    for octave in range(2):
        c = cell / (2 ** octave)
        q = p / c
        i = np.floor(q).astype(np.int64)
        f = q - i
        f = f * f * (3 - 2 * f)

        def h(dx, dy, dz):
            k = (i[:, 0] + dx) * 73856093 ^ (i[:, 1] + dy) * 19349663 ^ (i[:, 2] + dz) * 83492791 ^ (seed + octave) * 2654435761
            return ((k * 1103515245 + 12345) & 0x7FFFFFFF) / float(0x7FFFFFFF)

        v = 0.0
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    w = ((f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1])
                         * (f[:, 2] if dz else 1 - f[:, 2]))
                    v = v + w * h(dx, dy, dz)
        out += amp * v
        total += amp
        amp *= 0.5
    return out / total


def runs(spec, rng):
    """The design's runs as rows: (face, u0, width, z_top, length, kind). face is the outward
    direction of the face the run is on ('+x', '-x', '+y', '-y', 'arm+x', 'arm-x', 'arm+y')."""
    out = []
    h = spec["shaft_half_m"]
    top, arm = spec["shaft_top_m"], spec["arm"]
    faces = ["+x", "-x", "-y", "+y"]
    R = spec.get("runoff")
    if R:
        # broad dark run-off: below the arm on +y, and from the top on the other faces near the arm's side
        for k in range(R["count"]):
            under = k < R["under_arm"]
            face = "+y" if under else ["+x", "-x", "-y"][k % 3]
            if face in ("+x", "-x"):
                u0 = rng.uniform(0.0, h * 0.7)          # toward the arm's side of the face
            elif under:
                # spread across the face under the arm, a little jitter each
                u0 = -h * 0.7 + (k + 0.5) * (1.4 * h / R["under_arm"]) + rng.uniform(-0.015, 0.015)
            else:
                u0 = rng.uniform(-h * 0.6, h * 0.6)
            out.append((face, u0, rng.uniform(*R["width_m"]), arm["z0"] if under else top,
                        rng.uniform(*R["length_m"]), "runoff"))
    L = spec["lime"]
    for k in range(L["count"]):
        under = k < L["under_arm"]
        face = "+y" if under else faces[k % 4]
        u0 = rng.uniform(-h * 0.8, h * 0.8)
        z0 = arm["z0"] if under else top
        out.append((face, u0, rng.uniform(*L["width_m"]), z0, rng.uniform(*L["length_m"]) * (1.3 if under else 1.0), "lime"))
    A = spec["arm_lime"]
    for k in range(A["count"]):
        face = ["arm+y", "arm+x", "arm-x"][k % 3]
        u0 = rng.uniform(-h * 0.7, h * 0.7) if face == "arm+y" else rng.uniform(arm["y0"] + 0.03, arm["y1"] - 0.02)
        out.append((face, u0, rng.uniform(*A["width_m"]), arm["z1"], rng.uniform(*A["length_m"]), "lime"))
    D = spec["door_rust"]
    for x in D["x"]:
        out.append(("-y", x + rng.uniform(-0.004, 0.004), rng.uniform(*D["width_m"]), D["from_z"], rng.uniform(*D["length_m"]), "rust"))
    S = spec["spigot_rust"]
    out.append(("arm+y", rng.uniform(-0.01, 0.01), S["width_m"], arm["z1"], rng.uniform(*S["length_m"]), "rust"))
    return out


def face_of(np, n, p, spec):
    """Each texel's face name, and its across-the-face coordinate u (metres)."""
    arm = spec["arm"]
    on_arm = (p[:, 1] > spec["shaft_half_m"] + 0.005) & (p[:, 2] > arm["z0"] - 0.01)
    ax, ay = np.abs(n[:, 0]), np.abs(n[:, 1])
    name = np.full(len(n), "", dtype=object)
    side_x = (ax > 0.7)
    side_y = (ay > 0.7)
    name[side_x & (n[:, 0] > 0)] = "+x"
    name[side_x & (n[:, 0] < 0)] = "-x"
    name[side_y & (n[:, 1] > 0)] = "+y"
    name[side_y & (n[:, 1] < 0)] = "-y"
    for a in ("+x", "-x", "+y"):
        sel = on_arm & (name == a)
        name[sel] = "arm" + a
    u = np.where(side_x, p[:, 1], p[:, 0])
    return name, u


def draw(np, p, n, spec):
    """The stain's colour (N x 3, linear) and amount (N) at texels of position p and facing n."""
    import random
    rng = random.Random(spec["seed"])
    N = len(p)
    C = np.zeros((N, 3))
    A = np.zeros(N)

    def over(colour, amount):
        # each new stain painted on top of those before it (premultiplied colour)
        nonlocal C, A
        a = np.clip(amount, 0.0, 1.0)
        C = C * (1 - a)[:, None] + a[:, None] * np.asarray(colour)[None, :]
        A = A * (1 - a) + a

    name, u = face_of(np, n, p, spec)
    z = p[:, 2]
    G = spec["algae"]
    patch = vnoise(np, p, G["patch_m"], spec["seed"])
    vertical = np.abs(n[:, 2]) < 0.5
    shaded = (name == "-y")
    ramp = np.clip(1 - z / G["shaded_to_m"], 0, 1) * np.where(z < G["strong_below_m"], 1.0, 0.6)
    a_sh = shaded * ramp * np.clip((patch - 0.35) * 3.0, 0, 1) * G["shaded_strength"]
    a_ot = (vertical & ~shaded) * np.clip(1 - z / G["others_to_m"], 0, 1) * np.clip((patch - 0.45) * 3.0, 0, 1) * G["others_strength"]
    over(G["colour"], a_sh + a_ot)
    arm = spec["arm"]
    arm_top = (n[:, 2] > 0.7) & (p[:, 1] > spec["shaft_half_m"]) & (z > arm["z0"])
    over(G["colour"], arm_top * np.clip((patch - 0.3) * 2.5, 0, 1) * spec["arm_algae"]["strength"])
    wobble = (vnoise(np, np.stack([p[:, 0] * 0, p[:, 1] * 0, z], 1), 0.12, spec["seed"] + 7) - 0.5)
    for face, u0, w, ztop, length, kind in sorted(runs(spec, rng), key=lambda r: ("runoff", "lime", "rust").index(r[5])):
        on = (name == face)
        d = np.abs(u - (u0 + wobble * w * 0.8))
        below = ztop - z
        fade = np.clip(1 - below / length, 0, 1) * (below > -0.002)
        width = w * (0.55 + 0.45 * fade)
        edge = np.clip((width / 2 - d) / max(w * 0.25, 0.001), 0, 1)
        grain = 0.75 + 0.25 * vnoise(np, p, 0.01, spec["seed"] + 3)
        if kind == "runoff":
            # water runs: striations stretched down the face
            grain = 0.45 + 0.55 * vnoise(np, np.stack([p[:, 0], p[:, 1], p[:, 2] * 0.05], 1), 0.008, spec["seed"] + 11)
        row = {"lime": spec["lime"], "rust": spec["rust"], "runoff": spec.get("runoff")}[kind]
        amount = on * edge * (fade ** row.get("fade_power", 0.7)) * grain
        over(row["colour"], amount * row["strength"])
    rgb = np.where(A[:, None] > 1e-6, C / np.maximum(A, 1e-6)[:, None], 0.0)
    return rgb, A


def srgb8(np, lin):
    lin = np.clip(lin, 0, 1)
    s = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * np.power(lin, 1 / 2.4) - 0.055)
    return np.round(s * 255).astype(np.uint8)


def main(spec_path):
    import bpy
    import bmesh
    import numpy as np
    spec = json.load(open(spec_path, encoding="utf-8"))
    glb = os.path.join(REPO, spec["glb"])
    px = int(os.environ.get("LEDGER_STAIN_PX", spec["px"]))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    piece = [o for o in bpy.context.scene.objects if o.type == "MESH"][0]
    bpy.context.view_layer.objects.active = piece
    piece.select_set(True)
    slot_index = [i for i, s in enumerate(piece.material_slots) if s.material and s.material.name == spec["slot"]]
    if not slot_index:
        raise SystemExit("kit_stain: %s has no slot %s" % (glb, spec["slot"]))
    original = piece.material_slots[slot_index[0]].material

    # The slot's faces, unwrapped in the first UV, then separated for the bake.
    bpy.context.scene.tool_settings.use_uv_select_sync = True
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(piece.data)
    for f in bm.faces:
        f.select = f.material_index == slot_index[0]
    bmesh.update_edit_mesh(piece.data)
    bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=0.004, scale_to_bounds=False)
    bpy.ops.uv.pack_islands(rotate=True, scale=True, margin=0.004)
    bpy.ops.mesh.separate(type="SELECTED")
    bpy.ops.object.mode_set(mode="OBJECT")
    part = [o for o in bpy.context.scene.objects if o.type == "MESH" and o is not piece][0]
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = part
    part.select_set(True)
    bpy.ops.object.material_slot_remove_unused()
    temp = original.copy()
    part.material_slots[0].material = temp

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 1
    scene.render.bake.margin = int(spec["margin_px"])
    pos_img = bpy.data.images.new("stain-pos", px, px, alpha=False, float_buffer=True)
    nor_img = bpy.data.images.new("stain-nor", px, px, alpha=False, float_buffer=True)
    for im in (pos_img, nor_img):
        im.colorspace_settings.name = "Non-Color"
    nt = temp.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    enc = nt.nodes.new("ShaderNodeVectorMath")
    enc.operation = "MULTIPLY_ADD"
    emit = nt.nodes.new("ShaderNodeEmission")
    outn = nt.nodes.new("ShaderNodeOutputMaterial")
    img = nt.nodes.new("ShaderNodeTexImage")
    nt.links.new(enc.outputs[0], emit.inputs["Color"])
    nt.links.new(emit.outputs[0], outn.inputs["Surface"])
    # positions and normals encoded into [0, 1]: (v + 1) / 6 and (n + 1) / 2
    for image, socket, scale in ((pos_img, "Position", 1.0 / 6.0), (nor_img, "Normal", 0.5)):
        for l in list(enc.inputs[0].links):
            nt.links.remove(l)
        nt.links.new(geo.outputs[socket], enc.inputs[0])
        enc.inputs[1].default_value = (scale, scale, scale)
        enc.inputs[2].default_value = (scale, scale, scale) if socket == "Position" else (0.5, 0.5, 0.5)
        img.image = image
        for node in nt.nodes:
            node.select = False
        img.select = True
        nt.nodes.active = img
        bpy.ops.object.bake(type="EMIT", margin=int(spec["margin_px"]), use_clear=True)

    def read(image):
        buf = np.empty(px * px * 4, dtype=np.float32)
        image.pixels.foreach_get(buf)
        return buf.reshape(-1, 4)[:, :3].astype(np.float64)

    pe, ne = read(pos_img), read(nor_img)
    covered = pe.sum(axis=1) > 0
    p = pe[covered] * 6.0 - 1.0
    n = ne[covered] * 2.0 - 1.0
    n = n / np.maximum(np.linalg.norm(n, axis=1), 1e-6)[:, None]
    rgb, a = draw(np, p, n, spec)
    out = np.zeros((px * px, 4), dtype=np.uint8)
    grey = srgb8(np, np.array([0.3, 0.3, 0.3]))
    out[:, :3] = grey
    out[covered, :3] = srgb8(np, rgb)
    out[covered, :3] = np.where(a[:, None] > 1e-4, out[covered, :3], grey)
    out[covered, 3] = np.round(np.clip(a, 0, 1) * 255).astype(np.uint8)
    out = out.reshape(px, px, 4)[::-1]          # Blender's rows run bottom up
    os.makedirs(os.path.dirname(spec["stain"]), exist_ok=True)
    from PIL import Image
    Image.fromarray(out, "RGBA").save(spec["stain"])

    # The piece again, its slot's own material back, written over its game copy.
    part.material_slots[0].material = original
    bpy.ops.object.select_all(action="DESELECT")
    piece.select_set(True)
    part.select_set(True)
    bpy.context.view_layer.objects.active = piece
    bpy.ops.object.join()
    bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_selection=True, export_apply=True,
                              export_materials="EXPORT", export_yup=True)
    stained = int((out[..., 3] > 25).sum())
    print("kit_stain: %s slot=%s px=%d texels=%d stained=%d runs=%d stain=%s"
          % (spec["piece"], spec["slot"], px, int(covered.sum()), stained,
             len(runs(spec, __import__("random").Random(spec["seed"]))), spec["stain"]))


def selftest():
    import numpy as np
    spec = json.load(open(os.path.join(REPO, "production", "specs", "kit-wear", "lamp_post_C.json"), encoding="utf-8"))
    ok = []

    def check(name, cond):
        ok.append(bool(cond))
        if not cond:
            print("kit_stain selftest FAIL %s" % name)

    import random
    r = runs(spec, random.Random(spec["seed"]))
    check("the design's run counts", sum(1 for x in r if x[5] == "lime") == spec["lime"]["count"] + spec["arm_lime"]["count"]
          and sum(1 for x in r if x[5] == "rust") == 3 and sum(1 for x in r if x[5] == "runoff") == spec["runoff"]["count"])
    # a run under the arm on +y: stained just below its source, clean far below
    face, u0, w, ztop, length, kind = [x for x in r if x[0] == "+y" and x[5] == "lime"][0]
    lowest = min(x[3] - x[4] for x in r if x[0] == "+y")     # the end of the longest run on that face
    pts = np.array([[u0, 0.11, ztop - 0.01], [u0, 0.11, lowest - 0.05], [u0 + 0.05, 0.11, ztop - 0.01]])
    nor = np.array([[0, 1.0, 0]] * 3)
    rgb, a = draw(np, pts, nor, spec)
    check("a run stains just below its source", a[0] > 0.3)
    check("and nothing below its length", a[1] < 0.05)
    # lime shows paler than the dark run-off it may lie on
    check("lime is paler than the run-off", rgb[0].mean() > np.mean(spec["runoff"]["colour"]) + 0.05)
    # the shaded face's foot carries algae somewhere, the sunny face's high shaft none
    zs = np.linspace(0.02, 0.25, 60)
    foot = np.stack([np.linspace(-0.1, 0.1, 60), np.full(60, -0.11), zs], 1)
    _, a2 = draw(np, foot, np.array([[0, -1.0, 0]] * 60), spec)
    check("algae on the shaded foot", a2.max() > 0.2)
    high = np.stack([np.linspace(-0.1, 0.1, 60), np.full(60, 0.11), np.full(60, 2.5)], 1)
    _, a3 = draw(np, high, np.array([[0, 1.0, 0]] * 60), spec)
    check("the mid shaft clean", a3.max() < 0.05)
    print("kit_stain selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[-1])
