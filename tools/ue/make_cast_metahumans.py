"""Make the slice's cast as MetaHumans, by script, in the full editor.

    set LEDGER_MH_STEP=prepare   (or build)
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject
        with Content/Python/init_unreal.py calling main_after_idle()
    python tools/ue/make_cast_metahumans.py --selftest     # runs without Unreal

WHY, 24 September. Jafar: "MetaHumans replace the Mixamo stand-ins for the
slice's cast, starting with Rocco, Lena and Sam, in plain clothes for now."
Each starts from the nearest of the 29 people the MetaHuman plugin ships,
chosen from their preview pictures against the cards: Rocco, twenty years on
the door, big and slow, from Jorge; Lena, thirty-one years on the books, from
Grace; Sam, the fast talker who walks the street, from Orlando. A choice of
look, not canon, and his to overrule.

TWO STEPS, TWO EDITOR RUNS, because the preview holds several GB and a build
beside it runs out of memory (assemble_metahuman.py's own finding):

  prepare  duplicate the preset into /Game/Cast/MH_<name>, open it for edit,
           put it in the plugin's one plain garment, ask Epic's service to
           rig it and to send its textures, and wait until it can be built;
           one character at a time, never re-entered.
  build    build each with the Optimized pipeline at High into
           /Game/Ledger/MetaHumans, where the probe's build step copies from.

THE FILES STAY OUT OF THE REPOSITORY: they are made in the scratch project
outside it, and backed up to Dropbox (DECISIONS, 24 September).

ONE LINE PER CHARACTER PER STEP, appended to ue-material.txt in the project
folder: who, from which preset, what happened, how long.
"""
import os
import sys
import time

CAST = [("rocco", "Jorge"), ("lena", "Grace"), ("sam", "Orlando")]
PRESET_DIR = "/MetaHumanCharacter/Optional/Presets/"
CAST_DIR = "/Game/Cast/"
BUILD_ROOT = "/Game/Ledger/MetaHumans"
GARMENT = "/MetaHumanCharacter/Optional/Clothing/WI_DefaultGarment.WI_DefaultGarment"
NEED_FREE_GB = 10.0
CLOUD_TIMEOUT_S = 15 * 60


def asset_name(who, bare=False):
    return "MH_" + who.capitalize() + ("Bare" if bare else "")


BARE = os.environ.get("LEDGER_MH_BARE", "") == "1"


def status_line(step, who, preset, status, seconds, note):
    return ("castMetahuman step=%s who=%s preset=%s status=%s seconds=%.0f note=%s"
            % (step, who, preset, status, seconds, (note or "none").replace(" ", "~")[:220]))


def free_gb():
    try:
        import ctypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        m = MEMORYSTATUSEX()
        m.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            return None
        return m.ullAvailPhys / (1024.0 ** 3)
    except Exception:
        return None


def main_after_idle(seconds=20.0, settle=15.0):
    import unreal
    step_name = os.environ.get("LEDGER_MH_STEP", "prepare")
    only = [w.strip() for w in os.environ.get("LEDGER_MH_ONLY", "").split(",") if w.strip()]
    cast = [c for c in CAST if not only or c[0] in only]
    st = {"t0": time.time(), "h": None, "i": 0, "phase": "wait", "busy": False}
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)

    def write(l):
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(l + "\n")
        print("make_cast_metahumans: " + l)

    def close_current():
        ch = st.get("ch")
        if ch is not None and sub.is_object_added_for_editing(ch):
            sub.remove_object_to_edit(ch)
        if ch is not None:
            unreal.EditorAssetLibrary.save_loaded_asset(ch, only_if_is_dirty=False)
        st["ch"] = None

    def next_character():
        close_current()
        st["i"] += 1
        st["phase"] = "open" if st["i"] < len(cast) else "quit"

    def open_character():
        who, preset = cast[st["i"]]
        dest = CAST_DIR + asset_name(who, BARE)
        st["who"], st["preset"], st["tc"] = who, preset, time.time()
        if not unreal.EditorAssetLibrary.does_asset_exist(dest):
            if step_name != "prepare":
                write(status_line(step_name, who, preset, "NOT-PREPARED", 0, dest + " does not exist"))
                return False
            made = unreal.EditorAssetLibrary.duplicate_asset(PRESET_DIR + preset + "." + preset, dest)
            if made is None:
                write(status_line(step_name, who, preset, "NO-DUPLICATE", 0, "duplicate_asset refused " + preset))
                return False
            unreal.EditorAssetLibrary.save_loaded_asset(made, only_if_is_dirty=False)
        ch = unreal.load_asset(dest)
        if ch is None:
            write(status_line(step_name, who, preset, "NO-LOAD", 0, dest))
            return False
        if step_name == "build":
            f = free_gb()
            if f is not None and f < NEED_FREE_GB:
                write(status_line(step_name, who, preset, "REFUSED", 0, "free %.1f GB under %.0f" % (f, NEED_FREE_GB)))
                return False
        if not sub.try_add_object_to_edit(ch):
            write(status_line(step_name, who, preset, "NOT-EDITABLE", 0, "try_add_object_to_edit refused"))
            return False
        st["ch"] = ch
        st["opened"] = time.time()
        return True

    def ask_cloud():
        ch = st["ch"]
        notes = []
        # THE PLAIN GARMENT, added after the character is open (with it
        # already in the collection, opening crashed: dress_metahuman.py).
        # BARE, FOR FITTING (24 September): the same preset with no garment,
        # because a built body has its skin removed wherever clothes cover it,
        # and a jacket needs the torso to be fitted to.
        garment = None if BARE else unreal.load_asset(GARMENT)
        if BARE:
            notes.append("bare")
        elif garment is not None:
            col = ch.internal_collection
            item = col.try_add_item_from_wardrobe_item("Outfits", garment)
            col.default_instance.try_add_slot_selection(
                unreal.MetaHumanPipelineSlotSelection(slot_name="Outfits", selected_item=item))
            notes.append("garment")
        else:
            notes.append("no-garment")
        sub.request_auto_rigging(ch, unreal.MetaHumanCharacterAutoRiggingRequestParams())
        sub.request_texture_sources(ch, unreal.MetaHumanCharacterTextureRequestParams())
        st["asked"] = time.time()
        st["last"] = 0.0
        write(status_line(step_name, st["who"], st["preset"], "ASKED", time.time() - st["tc"],
                          "+".join(notes) + ";rig-and-textures-requested"))

    def poll_cloud():
        ch = st["ch"]
        now = time.time()
        if now - st["last"] < 3.0:
            return
        st["last"] = now
        rigged = sub.can_build_meta_human(ch, False)
        textured = bool(ch.get_editor_property("has_high_resolution_textures"))
        if rigged and textured:
            write(status_line(step_name, st["who"], st["preset"], "READY", now - st["tc"],
                              "rigged-and-textured-after-%.0fs" % (now - st["asked"])))
            next_character()
        elif now - st["asked"] > CLOUD_TIMEOUT_S:
            write(status_line(step_name, st["who"], st["preset"], "TIMED-OUT", now - st["tc"],
                              "rigged=%s textured=%s after %d min" % (rigged, textured, CLOUD_TIMEOUT_S // 60)))
            next_character()

    def build():
        ch = st["ch"]
        if not sub.can_build_meta_human(ch, True):
            write(status_line(step_name, st["who"], st["preset"], "CANNOT-BUILD", time.time() - st["tc"], "see the log"))
            return
        p = unreal.MetaHumanCharacterEditorBuildParameters()
        p.set_editor_property("pipeline_type", unreal.MetaHumanDefaultPipelineType.OPTIMIZED)
        p.set_editor_property("pipeline_quality", unreal.MetaHumanQualityLevel.HIGH)
        p.set_editor_property("absolute_build_path", BUILD_ROOT)
        sub.build_meta_human(ch, p)
        unreal.EditorAssetLibrary.save_directory(BUILD_ROOT, only_if_is_dirty=False, recursive=True)
        made = unreal.EditorAssetLibrary.list_assets(BUILD_ROOT + "/" + asset_name(st["who"], BARE), recursive=True, include_folder=False)
        write(status_line(step_name, st["who"], st["preset"], "BUILT", time.time() - st["tc"],
                          "%d-assets-optimized-high" % len(made)))

    def step():
        now = time.time()
        ph = st["phase"]
        if ph == "wait":
            if now - st["t0"] >= seconds:
                st["phase"] = "open" if cast else "quit"
        elif ph == "open":
            if open_character():
                st["phase"] = "settle"
            else:
                next_character()
        elif ph == "settle":
            if now - st["opened"] < settle:
                return
            if step_name == "prepare":
                if sub.can_build_meta_human(st["ch"], False) and st["ch"].get_editor_property("has_high_resolution_textures"):
                    write(status_line(step_name, st["who"], st["preset"], "ALREADY-READY", now - st["tc"], "nothing asked"))
                    next_character()
                    return
                ask_cloud()
                st["phase"] = "poll"
            else:
                build()
                next_character()
        elif ph == "poll":
            poll_cloud()
        if st["phase"] == "quit":
            unreal.unregister_slate_post_tick_callback(st["h"])
            unreal.SystemLibrary.quit_editor()

    def tick(delta):
        # NEVER RE-ENTERED: opening for edit and saving both pump the editor's
        # ticks (dress_metahuman.py and request_metahuman_textures.py).
        if st["busy"]:
            return
        st["busy"] = True
        try:
            step()
        except Exception as e:
            write(status_line(step_name, st.get("who", "none"), st.get("preset", "none"), "RAISED",
                              time.time() - st["t0"], repr(e)))
            try:
                next_character()
            except Exception:
                st["phase"] = "quit"
            if st["phase"] == "quit":
                unreal.unregister_slate_post_tick_callback(st["h"])
                unreal.SystemLibrary.quit_editor()
        finally:
            st["busy"] = False

    st["h"] = unreal.register_slate_post_tick_callback(tick)


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("make_cast_metahumans selftest FAIL " + name)
    check("three of the slice's cast", [w for w, _ in CAST] == ["rocco", "lena", "sam"])
    check("each from a shipped preset", all(p for _, p in CAST))
    check("the asset name is the MetaHuman convention", asset_name("rocco") == "MH_Rocco")
    check("the build lands where the probe copies from", BUILD_ROOT == "/Game/Ledger/MetaHumans")
    check("the line names who and what", "who=lena" in status_line("prepare", "lena", "Grace", "READY", 1, "x")
          and "status=READY" in status_line("prepare", "lena", "Grace", "READY", 1, "x"))
    check("a note keeps no spaces", " " not in status_line("p", "w", "p", "S", 1, "a b c").split("note=")[1])
    print("make_cast_metahumans selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("make_cast_metahumans runs inside the editor; see the header")
