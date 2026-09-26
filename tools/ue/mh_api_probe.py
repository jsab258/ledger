"""What a built cast member's hair materials hold, and what its blueprint puts on the hair: why the recoloured hair renders unchanged (26 September).

    set LEDGER_MH_SCRIPT=mh_api_probe
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

Reads only. Writes mh-api.json beside the project.
"""
import json
import os
import time

WHO = os.environ.get("LEDGER_PROBE_WHO", "MH_RoccoN1")


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "mh-api.json")

    def run():
        facts = {"mi": {}, "components": []}
        root = "/Game/Ledger/MetaHumans/" + WHO
        for path in unreal.EditorAssetLibrary.list_assets(root + "/Grooms", recursive=True, include_folder=False):
            name = path.split("/")[-1].split(".")[0]
            if not name.startswith("MI_") or "Hair" not in name:
                continue
            mi = unreal.load_asset(path)
            row = {"parent": mi.get_editor_property("parent").get_path_name() if mi.get_editor_property("parent") else None}
            try:
                row["scalars"] = {str(p.parameter_info.name): round(p.parameter_value, 3) for p in mi.get_editor_property("scalar_parameter_values")}
            except Exception as ex:
                row["scalars"] = "raised %r" % ex
            try:
                row["parentScalars"] = [str(n) for n in unreal.MaterialEditingLibrary.get_scalar_parameter_names(mi)][:60]
            except Exception as ex:
                row["parentScalars"] = "raised %r" % ex
            facts["mi"][name] = row
        # the blueprint's hair components and the materials they are given
        bp = unreal.load_asset(root + "/BP_" + WHO + ".BP_" + WHO)
        try:
            sub = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
            handles = sub.k2_gather_subobject_data_for_blueprint(bp)
            for h in handles:
                data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h)
                obj = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
                if obj is None:
                    continue
                row = {"name": obj.get_name(), "class": obj.get_class().get_name()}
                if isinstance(obj, unreal.PrimitiveComponent):
                    try:
                        row["materials"] = [m.get_path_name() if m else None for m in obj.get_editor_property("override_materials")]
                    except Exception:
                        pass
                if "Groom" in row["class"]:
                    for prop in ("groom_asset", "binding_asset"):
                        try:
                            v = obj.get_editor_property(prop)
                            row[prop] = v.get_path_name() if v else None
                        except Exception:
                            pass
                facts["components"].append(row)
        except Exception as ex:
            facts["components"] = "raised %r" % ex
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(facts, fh, indent=1)

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            with open(out, "w", encoding="utf-8") as fh:
                json.dump({"raised": repr(e)}, fh)
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
