"""Which colour settings a built MetaHuman's hair materials really have.

    set LEDGER_MH_SCRIPT=probe_hair_materials
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject

WHY, 24 September. Take T3 set Melanin and Whiteness on Lena's and Rocco's
built hair materials and nothing visible changed. This lists, for every
material instance under each cast take's Grooms folder, its parent and its
scalar parameters with their values, to mh-hair-materials.txt in the scratch
project folder.
"""
import os
import time

ROOT = "/Game/Ledger/MetaHumans/"
TAKES = ("MH_LenaT3", "MH_RoccoT3", "MH_LenaT2")


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "mh-hair-materials.txt")

    def run():
        mel = unreal.MaterialEditingLibrary
        lines = []
        for take in TAKES:
            for path in unreal.EditorAssetLibrary.list_assets(ROOT + take + "/Grooms", recursive=True, include_folder=False):
                a = unreal.load_asset(path)
                if not isinstance(a, unreal.MaterialInstance):
                    continue
                parent = a.get_editor_property("parent")
                lines.append("%s parent=%s" % (path.split(".")[0], parent.get_path_name() if parent else "none"))
                for n in mel.get_scalar_parameter_names(a):
                    lines.append("    scalar %s = %.3f" % (n, mel.get_material_instance_scalar_parameter_value(a, n)))
                for n in mel.get_vector_parameter_names(a):
                    lines.append("    vector %s" % n)
                for n in mel.get_texture_parameter_names(a):
                    tex = mel.get_material_instance_texture_parameter_value(a, n)
                    lines.append("    texture %s = %s" % (n, tex.get_name() if tex else "none"))
        # WHICH MATERIAL THE BUILT GROOM COMPONENTS DRAW WITH: the blueprint's
        # own overrides, if it has any, are what the game shows.
        for take in TAKES:
            bp = unreal.load_asset(ROOT + take + "/BP_" + take)
            lines.append("%s blueprint loaded=%s" % (take, bp is not None))
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
