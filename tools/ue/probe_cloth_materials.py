"""Which colour settings a built cast member's clothing materials expose.

    set LEDGER_MH_SCRIPT=probe_cloth_materials
    UnrealEditor.exe <the dressing project>

WHY, 24 September (overnight): Epic's free garments come in grey with bright
blue trim, too loud for plain 1990 clothes. This lists, for every material
instance in each take's built Clothing folder, its parent and its vector and
scalar parameters with values, to mh-cloth-materials.txt in the project folder.
"""
import os
import time

ROOT = "/Game/Ledger/MetaHumans/"
TAKES = ("MH_LenaT2", "MH_RoccoT2", "MH_SamT2")


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "mh-cloth-materials.txt")

    def run():
        mel = unreal.MaterialEditingLibrary
        lines = []
        for take in TAKES:
            for path in unreal.EditorAssetLibrary.list_assets(ROOT + take, recursive=True, include_folder=False):
                if "/Clothing/" not in path and "/Outfit" not in path:
                    continue
                a = unreal.load_asset(path)
                if not isinstance(a, unreal.MaterialInstance):
                    continue
                parent = a.get_editor_property("parent")
                lines.append("%s parent=%s" % (path.split(".")[0], parent.get_path_name() if parent else "none"))
                for n in mel.get_vector_parameter_names(a):
                    c = mel.get_material_instance_vector_parameter_value(a, n)
                    lines.append("    vector %s = %.3f %.3f %.3f" % (n, c.r, c.g, c.b))
                for n in mel.get_scalar_parameter_names(a):
                    lines.append("    scalar %s = %.3f" % (n, mel.get_material_instance_scalar_parameter_value(a, n)))
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            with open(out, "w", encoding="utf-8") as fh:
                fh.write("RAISED %r\n" % e)
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
