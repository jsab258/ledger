"""Export one animation sequence to FBX with its skeleton (no mesh: a commandlet cannot export the preview mesh), so it can be filmed outside Unreal.

Run as a commandlet: -run=pythonscript -script=<full path> with
  ANIM_PATH  asset path of the AnimSequence (e.g. /Game/MocapSolve/m2s1101e_Body)
  ANIM_FBX   absolute path of the .fbx to write
  ANIM_OUT   absolute path of a JSON result file
Writes {"ok": true, ...} only when the export task reports success and the file exists.
"""
import json
import os

import unreal

PATH = os.environ.get("ANIM_PATH", "")
FBX = os.environ.get("ANIM_FBX", "")
OUT = os.environ.get("ANIM_OUT", "")
res = {"anim": PATH, "fbx": FBX, "ok": False}
anim = unreal.load_asset(PATH)
if anim is None:
    res["error"] = "anim not found"
else:
    skel = anim.get_editor_property("skeleton")
    res["skeleton"] = skel.get_path_name() if skel else None
    opts = unreal.FbxExportOption()
    opts.set_editor_property("export_preview_mesh", False)  # True asserts in a commandlet (no render: SkinnedMeshComponent MeshObject)
    opts.set_editor_property("collision", False)
    task = unreal.AssetExportTask()
    task.set_editor_property("object", anim)
    task.set_editor_property("filename", FBX)
    task.set_editor_property("automated", True)
    task.set_editor_property("prompt", False)
    task.set_editor_property("replace_identical", True)
    task.set_editor_property("options", opts)
    ok = unreal.Exporter.run_asset_export_task(task)
    res["task_ok"] = bool(ok)
    res["ok"] = bool(ok) and os.path.isfile(FBX)
    if os.path.isfile(FBX):
        res["bytes"] = os.path.getsize(FBX)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
unreal.log("ANIMEXPORT " + json.dumps(res))
