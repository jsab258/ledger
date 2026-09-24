"""What each of the MetaHuman plugin's 29 people is made of, for casting.

    set LEDGER_MH_SCRIPT=probe_mh_presets
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject

WHY, 24 September. Jafar: "Why is Lena a middle aged chinese woman? Need a
proper casting for faces and bodies." The cast were taken whole from the
nearest shipped person. Casting to a brief means mixing them: a face shape
from some, a skin tone and a skin texture (which carries age) from others, a
height and build, a haircut. This writes, for every shipped person, the skin
settings the creator keeps, and for a few opened for edit, the body
measurements and the length of the face model's coefficients, one JSON file
to the scratch project folder (mh-presets.json).
"""
import json
import os
import time

PRESET_DIR = "/MetaHumanCharacter/Optional/Presets/"
OPEN_FOR_EDIT = ("Vivian", "Walter", "Jorge")


def plain(v):
    """A property value as JSON: numbers, strings, and the fields of structs, two levels deep."""
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    try:
        import unreal
        if isinstance(v, unreal.StructBase):
            out = {}
            for name in dir(v):
                if name.startswith("_") or name in ("cast", "copy", "assign", "static_struct", "get_editor_property",
                                                    "set_editor_property", "set_editor_properties", "export_text",
                                                    "import_text", "to_tuple"):
                    continue
                try:
                    x = getattr(v, name)
                except Exception:
                    continue
                if callable(x):
                    continue
                out[name] = plain(x) if not isinstance(x, unreal.StructBase) else {k: (y if isinstance(y, (int, float, str, bool)) else str(y)) for k, y in plain_shallow(x).items()}
            return out
    except Exception:
        pass
    return str(v)


def plain_shallow(v):
    out = {}
    for name in dir(v):
        if name.startswith("_"):
            continue
        try:
            x = getattr(v, name)
        except Exception:
            continue
        if not callable(x):
            out[name] = x
    return out


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "mh-presets.json")

    def run():
        sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
        names = sorted(a.split("/")[-1].split(".")[0] for a in unreal.EditorAssetLibrary.list_assets(PRESET_DIR, recursive=False, include_folder=False))
        data = {"presets": {}, "errors": []}
        for n in names:
            ch = unreal.load_asset(PRESET_DIR + n + "." + n)
            if ch is None:
                data["errors"].append("no load " + n)
                continue
            row = {}
            for prop in ("skin_settings", "eyes_settings", "makeup_settings", "head_model_settings"):
                try:
                    row[prop] = plain(ch.get_editor_property(prop))
                except Exception as e:
                    row[prop] = "unreadable: %r" % e
            try:
                col = ch.internal_collection
                row["wardrobe"] = [str(s.selected_item) + "@" + str(s.slot_name) for s in col.default_instance.get_editor_property("slot_selections")]
            except Exception as e:
                row["wardrobe"] = "unreadable: %r" % e
            data["presets"][n] = row
        for n in OPEN_FOR_EDIT:
            ch = unreal.load_asset(PRESET_DIR + n + "." + n)
            try:
                if not sub.try_add_object_to_edit(ch):
                    data["errors"].append("not editable " + n)
                    continue
                cons = sub.get_body_constraints(ch, False)
                data["presets"][n]["body_constraints"] = [plain(c) for c in cons]
                coeffs = sub.get_face_model_coefficients(ch)
                data["presets"][n]["face_coefficients"] = {"count": len(coeffs), "first": [round(float(c), 4) for c in list(coeffs)[:8]]}
                sub.remove_object_to_edit(ch)
            except Exception as e:
                data["errors"].append("%s: %r" % (n, e))
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, default=str)
        print("probe_mh_presets: wrote %s, %d presets, %d errors" % (out, len(data["presets"]), len(data["errors"])))

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
