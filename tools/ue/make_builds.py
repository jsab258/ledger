"""Three plain male builds for the clothing session, made and exported by script.

    set LEDGER_MH_SCRIPT=make_builds
    set LEDGER_BUILDS_OUT=F:/LedgerTools/bodies
    set LEDGER_BUILDS_STEP=make      (sets, re-rigs and exports; =export only exports)
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY, 29 September (Jafar: the clothing session sews and drapes in Blender on
"Ron, Darren and Sheila, plus one slim, one average and one heavy male build").
Each build is the Walter preset duplicated into /Game/Builds/ with only its
body set, through the same body constraints the cast uses (Height, Fat,
Muscularity; tools/ue/make_cast_metahumans.py), at 178 cm, the British adult
male average of the period; the face does not matter, the body does. Each is
then exported as the cast's bodies are (tools/ue/export_dcc.py, geometry: the
body and the full body as FBX with the skeleton, in the reference pose) into
LEDGER_BUILDS_OUT/<name>/, and what it did goes to make-builds.txt there.

SET ASIDE, 29 September (the two-tries rule): three attempts, the third
re-rigged by Epic's service with blocking True and exported while still open
(production/research/character-pipeline/metahuman-builds-2026-09-29.md); the
rigging finished each time, yet all three bodies still measure the same
(chest 923, waist 941 mm): the constraints never reach the Walter copy's body.
"""
import os
import time

PRESET = "/MetaHumanCharacter/Optional/Presets/Walter.Walter"
DEST_DIR = "/Game/Builds/"
BUILDS = {
    "MH_BuildSlim": {"Height": 178.0, "Fat": -1.0, "Muscularity": -0.5},
    "MH_BuildAverage": {"Height": 178.0, "Fat": 0.0, "Muscularity": 0.0},
    "MH_BuildHeavy": {"Height": 178.0, "Fat": 1.3, "Muscularity": 0.2},
}


def make(unreal, name, body):
    dest = DEST_DIR + name
    if not unreal.EditorAssetLibrary.does_asset_exist(dest):
        made = unreal.EditorAssetLibrary.duplicate_asset(PRESET, dest)
        if made is None:
            return None, "%s NOT DUPLICATED from %s" % (name, PRESET)
        unreal.EditorAssetLibrary.save_loaded_asset(made, only_if_is_dirty=False)
    ch = unreal.load_asset(dest)
    if ch is None:
        return None, "%s NOT LOADED" % dest
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    opened = not sub.is_object_added_for_editing(ch) and sub.try_add_object_to_edit(ch)
    held = []
    exported = "not exported"
    try:
        cons = sub.get_body_constraints(ch, False)
        for con in cons:
            n = str(con.get_editor_property("name"))
            if n in body:
                con.set_editor_property("target_measurement", body[n])
                con.set_editor_property("is_active", True)
                held.append(n)
        sub.set_body_constraints(ch, cons)
        sub.commit_body_state(ch)
        # THE THIRD AND LAST ATTEMPT (the two-tries rule), 29 September
        # (production/research/character-pipeline/metahuman-builds-2026-09-29.md):
        # a copied preset keeps its old body rig, and reopening the character
        # reloads the body from that rig, so the new body is re-rigged here,
        # as the cast is (blocking, so it returns when the cloud has answered),
        # and exported while still open.
        rp = unreal.MetaHumanCharacterAutoRiggingRequestParams()
        try:
            rp.set_editor_property("blocking", True)
            rp.set_editor_property("report_progress", False)
        except Exception as e:
            held.append("no-blocking:%r" % e)
        sub.request_auto_rigging(ch, rp)
        import export_dcc
        exported = export_dcc.geometry(unreal, ch, name, os.path.join(os.environ.get("LEDGER_BUILDS_OUT", "F:/LedgerTools/bodies"), name))
    finally:
        if opened:
            sub.remove_object_to_edit(ch)
    unreal.EditorAssetLibrary.save_loaded_asset(ch, only_if_is_dirty=False)
    return ch, "%s body %s (set: %s); %s" % (name, body, ",".join(held) or "NONE", exported)


def main_after_idle(seconds=20.0):
    import unreal
    import export_dcc
    st = {"t0": time.time(), "h": None, "done": False}
    root = os.environ.get("LEDGER_BUILDS_OUT", "F:/LedgerTools/bodies")
    os.makedirs(root, exist_ok=True)
    report = os.path.join(root, "make-builds.txt")

    def run():
        lines = []
        for name, body in BUILDS.items():
            try:
                if os.environ.get("LEDGER_BUILDS_STEP", "make") == "make":
                    ch, note = make(unreal, name, body)
                    lines.append(note)
                else:
                    # A SECOND EDITOR RUN EXPORTS (29 September): made and
                    # exported in the same instant, all three came out the
                    # preset's own body, the settings not yet solved into it.
                    ch = unreal.load_asset(DEST_DIR + name)
                    lines.append(export_dcc.geometry(unreal, ch, name, os.path.join(root, name)) if ch is not None
                                 else "%s NOT FOUND" % name)
            except Exception as e:
                lines.append("%s RAISED %r" % (name, e))
            with open(report, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines) + "\n")
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
