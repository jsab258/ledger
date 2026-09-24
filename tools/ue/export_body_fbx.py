"""Export MetaHuman bodies to FBX for Blender, in the full editor.

    set LEDGER_MH_SCRIPT=export_body_fbx
    set LEDGER_EXPORT_DIR=F:/LedgerTools/tmp/bodies
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -unattended
    (LEDGER_EXPORT_ONLY=/path/one,/path/two exports just those)

WHY, 25 September. The Blender route for the donkey jacket stopped at "the
engine's FBX export of a MetaHuman body crashes" (clothing-pipeline
TRIED-2026-09-24.md). The crash reports say why: the export ran in the
command-line editor (UnrealEditor-Cmd, -run=pythonscript), and exporting a
skinned mesh goes through a skinned mesh component whose render object
exists only where there is a renderer: "Assertion failed: MeshObject"
(SkinnedMeshComponent.cpp), twice, from Exporter.RunAssetExportTask. So this
runs in the full editor, after it has settled, as the other probes here do.

It exports the bare built body (MH_RoccoBare, no garment added) and the
plugin's own template bodies (PLUGIN_BODIES), and writes what it did to export-bodies.txt
beside the files.
"""
import os
import time

BUILT = [p for p in os.environ.get("LEDGER_EXPORT_ONLY", "/Game/Ledger/MetaHumans/MH_RoccoBare/Body/SKM_MH_RoccoBare_BodyMesh").split(",") if p]
PLUGIN_ROOT = "/MetaHumanCharacter/"
# The plugin's own bodies. NOT its garment meshes (ClothAssets/*_CombinedSkelMesh):
# the FBX exporter dies on those ("Array index out of bounds: 1 into an array
# of size 1", 25 September), and a garment is not a body to fit to.
# The garment's source bodies (archetype_SkelMesh, m_srt_unw_SkelMesh) crash
# the exporter as well; the identity template is the one that exports whole.
PLUGIN_BODIES = ["/MetaHumanCharacter/Body/IdentityTemplate/SKM_Body"]


def main_after_idle(seconds=25.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out_dir = os.environ.get("LEDGER_EXPORT_DIR", os.path.join(unreal.Paths.project_dir(), "export-bodies"))
    os.makedirs(out_dir, exist_ok=True)
    report = os.path.join(out_dir, "export-bodies.txt")

    def plugin_bodies(lines):
        reg = unreal.AssetRegistryHelpers.get_asset_registry()
        flt = unreal.ARFilter(package_paths=[PLUGIN_ROOT.rstrip("/")], recursive_paths=True,
                              class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "SkeletalMesh")])
        for ad in reg.get_assets(flt):
            lines.append("candidate %s" % ad.package_name)
        return list(PLUGIN_BODIES)

    def export(path, lines):
        a = unreal.load_asset(path)
        if a is None:
            lines.append("MISSING %s" % path)
            return
        dst = os.path.join(out_dir, path.rsplit("/", 1)[-1] + ".fbx")
        task = unreal.AssetExportTask()
        task.set_editor_property("object", a)
        task.set_editor_property("filename", dst)
        task.set_editor_property("exporter", unreal.SkeletalMeshExporterFBX())
        task.set_editor_property("automated", True)
        task.set_editor_property("prompt", False)
        task.set_editor_property("replace_identical", True)
        task.set_editor_property("options", unreal.FbxExportOption())
        lines.append("exporting %s" % path)
        with open(report, "w", encoding="utf-8") as fh:   # written before, so a crash still names the asset
            fh.write("\n".join(lines) + "\n")
        ok = unreal.Exporter.run_asset_export_task(task)
        size = os.path.getsize(dst) if os.path.exists(dst) else 0
        lines.append("  ok=%s bytes=%d -> %s" % (ok, size, dst))

    def run():
        lines = []
        targets = list(BUILT) + ([] if os.environ.get("LEDGER_EXPORT_ONLY") else plugin_bodies(lines))
        for p in targets:
            try:
                export(p, lines)
            except Exception as e:
                lines.append("  RAISED %r" % e)
        lines.append("done")
        with open(report, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            with open(report, "a", encoding="utf-8") as fh:
                fh.write("RAISED %r\n" % e)
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
