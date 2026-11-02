"""Export skeletal or static meshes from a MetaHuman project to FBX, in the full editor.

    set LEDGER_MH_SCRIPT=export_mesh_fbx
    set LEDGER_EXPORT_ASSETS=/Game/Fab/oa_boots/Boots/meshes/m_med_nrw_CombinedSkelMesh[,...]
    set LEDGER_EXPORT_DIR=F:/LedgerTools/garments/tom/boots/epic-ref
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended
    python tools/ue/export_mesh_fbx.py --selftest

WHY, 2 November 2026 (Epic's boots, his yes of 31 October, for Tom's toe shape): exporting a skeletal mesh from a
commandlet asserts in the engine (SkinnedMeshComponent.cpp, MeshObject: a skinned mesh needs the renderer), so the
export runs in the full editor after it has settled, as tools/ue/hidden_faces.py's records do, and the editor quits.
Every asset at LOD 0 only; one line a file to export.txt in LEDGER_EXPORT_DIR (EXPORTED or FAILED or MISSING).
"""
import os
import sys
import time


def wanted(env=None):
    env = os.environ if env is None else env
    return [a.strip() for a in env.get("LEDGER_EXPORT_ASSETS", "").split(",") if a.strip()]


def out_name(asset):
    return asset.rstrip("/").split("/")[-1].split(".")[0] + ".fbx"


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None}
    out = os.environ.get("LEDGER_EXPORT_DIR", "")

    def run():
        lines = []
        os.makedirs(out, exist_ok=True)
        for asset in wanted():
            m = unreal.load_asset(asset)
            if m is None:
                lines.append("MISSING " + asset)
                continue
            t = unreal.AssetExportTask()
            t.set_editor_property("object", m)
            t.set_editor_property("filename", os.path.join(out, out_name(asset)))
            skeletal = isinstance(m, unreal.SkeletalMesh)
            t.set_editor_property("exporter", unreal.SkeletalMeshExporterFBX() if skeletal else unreal.StaticMeshExporterFBX())
            t.set_editor_property("automated", True)
            t.set_editor_property("prompt", False)
            t.set_editor_property("replace_identical", True)
            o = unreal.FbxExportOption()
            o.set_editor_property("level_of_detail", False)
            o.set_editor_property("collision", False)
            t.set_editor_property("options", o)
            ok = unreal.Exporter.run_asset_export_task(t)
            lines.append("%s %s" % ("EXPORTED" if ok else "FAILED", os.path.join(out, out_name(asset))))
        with open(os.path.join(out, "export.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def tick(delta):
        if time.time() - st["t0"] < seconds:
            return
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            if out:
                run()
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)


def selftest():
    ok = [wanted({"LEDGER_EXPORT_ASSETS": " /Game/A/B , /Game/C.C "}) == ["/Game/A/B", "/Game/C.C"],
          out_name("/Game/Fab/oa_boots/Boots/meshes/m_med_nrw_CombinedSkelMesh") == "m_med_nrw_CombinedSkelMesh.fbx",
          out_name("/Game/C.C") == "C.fbx", wanted({}) == []]
    print("export_mesh_fbx selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__" and "--selftest" in sys.argv:
    sys.exit(selftest())
