"""The face-model coefficients of Epic's 29 MetaHuman presets, and one preset's face landmarks.

    set LEDGER_MH_SCRIPT=face_coeffs
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY, 28 September (Jafar's list, item 3; production/research/character-pipeline/
faces-and-hair-2026-09-28.md). Sheila's and Darren's faces, blended from the
presets, still leaned East Asian from the front after two attempts. The 5.8
API gets and sets a face's model coefficients (MetaHumanCharacterEditorSubsystem
get_face_model_coefficients / set_face_model_coefficients) and moves its
landmarks (translate_face_landmarks), so the difference between the presets
whose own pictures read white European and the rest is a direction a face can
be moved along, and landmarks name where the nose bridge, eyelids and lips are.
Reads only: each preset is opened for editing, read, and closed unsaved.
Writes preset-coeffs.json beside the project.
"""
import json
import os
import time

PRESET_DIR = "/MetaHumanCharacter/Optional/Presets/"
NAMES = ["Ada", "Aera", "Aoi", "Asha", "Bo", "Bruce", "Cameron", "Celeste", "Dominic", "Etta", "Grace", "Isaiah", "Jelena",
         "Jorge", "Kelvin", "Lani", "Lorenzo", "Mateo", "Mikel", "Omari", "Orlando", "Sook-ja", "Sunita", "Trey", "Tuya",
         "Victor", "Vivian", "Walter", "Zuri"]


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "preset-coeffs.json")

    def run():
        sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
        facts = {"coefficients": {}, "errors": {}}
        for n in NAMES:
            ch = unreal.load_asset(PRESET_DIR + n + "." + n)
            if ch is None:
                facts["errors"][n] = "missing"
                continue
            if not sub.try_add_object_to_edit(ch):
                facts["errors"][n] = "could not open for edit"
                continue
            try:
                facts["coefficients"][n] = [round(float(c), 6) for c in sub.get_face_model_coefficients(ch)]
                if n == "Jelena":
                    facts["landmarksJelena"] = [[round(v.x, 3), round(v.y, 3), round(v.z, 3)] for v in sub.get_face_landmarks(ch)]
            except Exception as e:
                facts["errors"][n] = repr(e)
            finally:
                sub.remove_object_to_edit(ch)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(facts, fh)

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
