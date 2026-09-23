"""Fetch a MetaHuman Character's texture sources from Epic's service and save them into it.

    UnrealEditor.exe <project>      with Content/Python/init_unreal.py exec'ing this file

WHY IT EXISTS, 24 September. tools/ue/assemble_metahuman.py ran MH_Test as far
as "The Character is missing textures, use Download Texture Sources to create
them before assembling". That button is the editor subsystem's
RequestTextureSources, a request to Epic's MetaHuman service under Jafar's Epic
account, and he said yes to it in chat ("yes, download the textures").

IT RUNS IN THE FULL EDITOR, NOT AS A COMMANDLET, AND AS THE PROJECT'S
START-UP SCRIPT (Content/Python/init_unreal.py calling this), NOT BY
-ExecutePythonScript: the request is answered over the network while the
editor ticks, a commandlet does not tick while a script runs, and
-ExecutePythonScript closes the editor the moment its script returns, which
cut the first download off. So this asks, then returns; a tick callback checks
every few seconds whether the character can now be built, saves it with its
textures, writes one line to ue-material.txt in the project folder, and closes
the editor. Assembling is then assemble_metahuman.py's, as a commandlet. It
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
            # NOT RE-ENTERED: saving pumps the editor's ticks, and the first
            # run (24 September) came back into this callback from inside its
            # own save six times, then crashed in the build. The callback goes
            # before anything that can tick, and assembling is left to
            # assemble_metahuman.py as a commandlet, which does not tick.
            unreal.unregister_slate_post_tick_callback(_state["handle"])
            _state["handle"] = None
            unreal.EditorAssetLibrary.save_loaded_asset(ch, only_if_is_dirty=False)
            _finish("TEXTURES-IN", "texture sources downloaded and saved into %s; assemble with assemble_metahuman.py" % CHARACTER)
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
    if sub.can_build_meta_human(ch, True):
        _finish("ALREADY-IN", "the character already has its texture sources")
        return
    sub.request_texture_sources(ch, unreal.MetaHumanCharacterTextureRequestParams())
    _state["asked"] = True
    _write("ASKED", "request_texture_sources sent; waiting while the editor ticks")
    _state["handle"] = unreal.register_slate_post_tick_callback(_tick)


main()
