"""A sewn garment pressed: its crinkles smoothed out, its size kept, nothing inside its wearer (tailor.press).

    blender -b -P tools/meshgen/blender/press_garment.py -- IN.blend OUT_DIR [--garment Jacket] [--rounds 40]

WHY, 29 September (the clothing session): see tailor.press. Run on the
garment sew_donkey.py leaves in the body's rest pose, before finish_donkey.py.
OUT_DIR gets pressed.blend (the same scene, the garment pressed),
pressed-front.png and pressed-back.png, and press.json.
"""
import json
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[0], argv[1]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=BLEND)
garment = bpy.data.objects[opt("--garment", "Jacket", str)]
body = next(o for o in bpy.data.objects if o.type == "MESH" and o is not garment and not o.hide_render)
bev = tailor.evaluated_copy(body, "BodyNow")
bvh = tailor.bvh_of(bev)
bpy.data.objects.remove(bev, do_unlink=True)
report = tailor.press(garment, bvh, rounds=opt("--rounds", 40, int), smooth=opt("--smooth", 0.25), lengths=opt("--lengths", 10, int))
# BY PIECE, from the flat pattern's layout (brian.LAYOUT): the back at u 0,
# the fronts at u +-1, the sleeves at u +-2
uvl = garment.data.uv_layers["pattern"]
u_of = {lp.vertex_index: uvl.data[lp.index].uv[0] for lp in garment.data.loops}
sleeves = [i for i, u in u_of.items() if abs(u) >= 1.5]
fronts = [i for i, u in u_of.items() if 0.5 <= abs(u) < 1.5]
backs = [i for i, u in u_of.items() if abs(u) < 0.5]
# THE SLEEVES PRESSED AGAIN (the first blind review: 'both forearms have
# dense, small, papery crinkles'): a second pass on them alone
report["sleeves"] = tailor.press(garment, bvh, rounds=opt("--sleeve-rounds", 60, int), smooth=0.35, lengths=opt("--lengths", 10, int),
                                 only=sleeves)
# THE HOLLOWS SPANNED (the same review: 'the chest moulds to the body')
if "--no-span" not in argv:
    # below the armpits (the body's own measure, else 25 cm under the top of the cloth)
    top = max((garment.matrix_world @ v.co).z for v in garment.data.vertices)
    report["spanned"] = tailor.span_hollows(garment, fronts + backs, fronts, backs, z_max=opt("--span-below", top - 0.17), deepest=opt("--span-deepest", 0.04))
    # and clear of the body again, where spanning a slope brought a point near it
    report["afterSpan"] = tailor.press(garment, bvh, rounds=2, smooth=0.0, lengths=0)
print("PRESS", json.dumps(report), flush=True)
co = tailor.coords(garment, evaluated=False)
mid = Vector((0.0, float(co[:, 1].mean()), float(co[:, 2].min() + co[:, 2].max()) / 2))
tailor.pictures(os.path.join(OUT, "pressed"), mid, views=(("front", (0, -3.4, 0.1)), ("back", (0, 3.4, 0.1))))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "pressed.blend"))
json.dump({"in": BLEND, "body": body.name, **report}, open(os.path.join(OUT, "press.json"), "w"), indent=1)
