"""Fetch a MetaHuman Character's texture sources from Epic's service, then assemble it.

    UnrealEditor.exe <project> -ExecutePythonScript="tools/ue/request_metahuman_textures.py"

WHY IT EXISTS, 24 September. tools/ue/assemble_metahuman.py ran MH_Test as far
as "The Character is missing textures, use Download Texture Sources to create
them before assembling". That button is the editor subsystem's
RequestTextureSources, a request to Epic's MetaHuman service under Jafar's Epic
account, and he said yes to it in chat ("yes, download the textures").

IT RUNS IN THE FULL EDITOR, NOT AS A COMMANDLET: the request is answered over
the network while the editor ticks, and a commandlet does not tick while a
script runs. So this asks, then returns; a tick callback checks every few
seconds whether the character can now be built, builds it with the Optimized
pipeline (the same call and settings as assemble_metahuman.py), saves, writes
one line to ue-material.txt in the project folder, and closes the editor. It
gives up after TIMEOUT_S and says so rather than waiting for ever.
"""
import os
import time

import unreal

CHARACTER = "/Game/MH_Test"
BUILD_ROOT = "/Game/Ledger/MetaHumans"
TIMEOUT_S = 20 * 60
POLL_S = 5.0

_state = {"t0": time.time(), "last": 0.0, "handle": None, "sub": None, "ch": None, "asked": False}


def _write(status, note):
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    line = "metahumanTextures=%s metahumanTexturesSeconds=%.0f metahumanTexturesNote=%s" % (
        status, time.time() - _state["t0"], (note or "none").replace(" ", "~")[:200])
    with open(out, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print("request_metahuman_textures: " + line)


def _finish(status, note):
    _write(status, note)
    if _state["handle"] is not None:
        unreal.unregister_slate_post_tick_callback(_state["handle"])
        _state["handle"] = None
    try:
        if _state["sub"] is not None and _state["ch"] is not None:
            _state["sub"].remove_object_to_edit(_state["ch"])
    except Exception:
        pass
    unreal.SystemLibrary.quit_editor()


def _tick(delta):
    now = time.time()
    if now - _state["last"] < POLL_S:
        return
    _state["last"] = now
    sub, ch = _state["sub"], _state["ch"]
    try:
        if sub.can_build_meta_human(ch, True):
            p = unreal.MetaHumanCharacterEditorBuildParameters()
            p.set_editor_property("pipeline_type", unreal.MetaHumanDefaultPipelineType.OPTIMIZED)
            p.set_editor_property("pipeline_quality", unreal.MetaHumanQualityLevel.HIGH)
            p.set_editor_property("absolute_build_path", BUILD_ROOT)
            unreal.EditorAssetLibrary.save_loaded_asset(ch, only_if_is_dirty=False)
            sub.build_meta_human(ch, p)
            unreal.EditorAssetLibrary.save_directory(BUILD_ROOT, only_if_is_dirty=False, recursive=True)
            made = unreal.EditorAssetLibrary.list_assets(BUILD_ROOT, recursive=True, include_folder=False)
            _finish("BUILT" if made else "BUILT-NOTHING", "%d assets in %s; %s" % (
                len(made), BUILD_ROOT, ",".join(a.split("/")[-1] for a in made if "BP_" in a)[:120] or "no-blueprint"))
            return
    except Exception as e:
        _finish("ERROR", repr(e))
        return
    if now - _state["t0"] > TIMEOUT_S:
        _finish("TIMED-OUT", "the textures had not arrived after %d minutes" % (TIMEOUT_S // 60))


def main():
    ch = unreal.load_asset(CHARACTER)
    if ch is None:
        _finish("NO-CHARACTER", CHARACTER + " did not load")
        return
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    if sub is None or not sub.try_add_object_to_edit(ch):
        _finish("NOT-EDITABLE", "no subsystem, or try_add_object_to_edit refused")
        return
    _state["sub"], _state["ch"] = sub, ch
    sub.request_texture_sources(ch, unreal.MetaHumanCharacterTextureRequestParams())
    _state["asked"] = True
    _write("ASKED", "request_texture_sources sent; waiting while the editor ticks")
    _state["handle"] = unreal.register_slate_post_tick_callback(_tick)


main()
