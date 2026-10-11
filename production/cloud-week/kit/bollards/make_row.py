"""A review aid: the five street kinds side by side in one scene, written to the scratch folder (never to git): K1, K2, K3, K4 and K6, then K5, 0.7 m apart."""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.abspath(os.path.join(HERE, "..", "..", "..", "assets", "cloud-week", "bollards"))
OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/kit-bollards/bollards_row.glb"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
for i, k in enumerate(("K1", "K2", "K3", "K4", "K6", "K5")):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(ASSET, "bollard_%s.glb" % k))
    for ob in set(bpy.data.objects) - before:
        if ob.parent is None:
            ob.location.x += 0.75 * (i - 2.5)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_apply=True, export_cameras=False, export_lights=False, export_yup=True)
print("row", OUT, os.path.getsize(OUT))
