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


BARE = os.environ.get("LEDGER_MH_BARE", "") == "1"
# A SECOND TAKE BESIDE THE FIRST (24 September): LEDGER_MH_TAKE=T2 makes
# MH_LenaT2 and so on, cast to the brief below, and leaves the stand-ins be.
TAKE = os.environ.get("LEDGER_MH_TAKE", "")


def asset_name(who, bare=False, take=None):
    return "MH_" + who.capitalize() + ("Bare" if bare else "") + (TAKE if take is None else take)


# CAST TO A BRIEF, 24 September. Jafar: "Why is Lena a middle aged chinese
# woman? Need a proper casting for faces and bodies." Canon says only "Rocco
# (old muscle), Lena (older bookkeeper)"; the voice cards make Sam a fast-
# talking Scot. The brief (his to strike, FOR-JAFAR 24 September): Lena
# British, about sixty, small and neat; Rocco British with an Italian name,
# late fifties, big and heavy; Sam Scottish, late twenties, wiry. Each is
# the base preset (its eyes, brows, wardrobe) with its face shape a weighted
# mix of shipped faces, its skin tone and skin texture set (the texture
# carries age: 121 is the aged set Walter and Grace share), its body held to
# measurements, and a haircut from the plugin's grooms. Skin U runs light
# (0.2, Vivian) to dark (0.95, Zuri); measurements are centimetres, and Fat,
# Muscularity and Masculine/Feminine the creator's own sliders.
GROOMS = "/MetaHumanCharacter/Optional/Grooms/Bindings/Hair/"
CASTING = {
    "lena": {"base": "Vivian", "face": {"Vivian": 0.55, "Celeste": 0.25, "Walter": 0.2},
             "skin": {"u": 0.24, "v": 0.45, "face_texture_index": 121},
             "body": {"Height": 160.0, "Fat": 0.6, "Muscularity": -0.8},
             "hair": "WI_Hair_M_BobCurly"},
    "rocco": {"base": "Jorge", "face": {"Jorge": 0.35, "Walter": 0.35, "Bruce": 0.3},
              "skin": {"u": 0.34, "v": 0.5, "face_texture_index": 121},
              "body": {"Height": 186.0, "Fat": 1.3, "Muscularity": 0.6},
              "hair": "WI_Hair_S_HairLoss"},
    "sam": {"base": "Orlando", "face": {"Orlando": 0.45, "Victor": 0.55},
            "skin": {"u": 0.2, "v": 0.45, "face_texture_index": 28},
            "body": {"Height": 173.0, "Fat": -1.0, "Muscularity": -0.3},
            "hair": "WI_Hair_S_Messy"},
}


def blend(vectors_and_weights):
    """The weighted mean of equal-length coefficient lists."""
    total = sum(w for _, w in vectors_and_weights)
    n = len(vectors_and_weights[0][0])
    out = [0.0] * n
    for vec, w in vectors_and_weights:
        for i in range(n):
            out[i] += float(vec[i]) * w / total
    return out


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
        if TAKE and who in CASTING:
            preset = CASTING[who]["base"]
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

    def apply_casting(ch, who):
        c = CASTING[who]
        notes = []
        vw = []
        for name, w in c["face"].items():
            src = unreal.load_asset(PRESET_DIR + name + "." + name)
            if src is None:
                notes.append("no-" + name)
                continue
            opened_here = not sub.is_object_added_for_editing(src)
            if opened_here and not sub.try_add_object_to_edit(src):
                notes.append("closed-" + name)
                continue
            vw.append((list(sub.get_face_model_coefficients(src)), w))
            if opened_here:
                sub.remove_object_to_edit(src)
        if vw and all(len(v) == len(vw[0][0]) for v, _ in vw):
            sub.set_face_model_coefficients(ch, blend(vw))
            sub.commit_face_state(ch)
            # The base preset's rig fits the base preset's face, not this one.
            sub.remove_face_rig(ch)
            notes.append("face-of-%d" % len(vw))
        ss = ch.get_editor_property("skin_settings")
        skin = ss.get_editor_property("skin")
        for k, v in c["skin"].items():
            skin.set_editor_property(k, v)
        ss.set_editor_property("skin", skin)
        # 4K FACE TEXTURES, not the default 2K: the close-up shows the difference.
        res = ss.get_editor_property("desired_texture_sources_resolutions")
        for k in ("face_albedo", "face_normal", "face_cavity"):
            try:
                res.set_editor_property(k, unreal.RequestTextureResolution.RES4K)
            except Exception:
                notes.append("no-4k-" + k)
        ss.set_editor_property("desired_texture_sources_resolutions", res)
        sub.commit_skin_settings(ch, ss)
        notes.append("skin")
        cons = sub.get_body_constraints(ch, False)
        held = 0
        for con in cons:
            n = str(con.get_editor_property("name"))
            if n in c["body"]:
                con.set_editor_property("target_measurement", c["body"][n])
                con.set_editor_property("is_active", True)
                held += 1
        sub.set_body_constraints(ch, cons)
        sub.commit_body_state(ch)
        notes.append("body-%d" % held)
        hair = unreal.load_asset(GROOMS + c["hair"] + "." + c["hair"])
        if hair is not None:
            col = ch.internal_collection
            item = col.try_add_item_from_wardrobe_item("Hair", hair)
            col.default_instance.try_add_slot_selection(
                unreal.MetaHumanPipelineSlotSelection(slot_name="Hair", selected_item=item))
            notes.append("hair")
        return notes

    def ask_cloud():
        ch = st["ch"]
        notes = []
        if TAKE and st["who"] in CASTING:
            notes += apply_casting(ch, st["who"])
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
        # A cast take's duplicate may still say "textured" from its base
        # preset before the service answers: the service took 30 s at least.
        early = TAKE and st["who"] in CASTING and now - st["asked"] < 30.0
        if rigged and textured and not early:
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
                # A CAST TAKE IS ALWAYS ASKED: its duplicate carries the base
                # preset's rig and textures, which the casting then changes.
                if not (TAKE and st["who"] in CASTING) and sub.can_build_meta_human(st["ch"], False) and st["ch"].get_editor_property("has_high_resolution_textures"):
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
    check("a take sits beside the first", asset_name("lena", take="T2") == "MH_LenaT2")
    check("each of the cast has a brief", sorted(CASTING) == ["lena", "rocco", "sam"])
    check("each brief blends shipped faces and is based on one of them",
          all(c["base"] in c["face"] and abs(sum(c["face"].values()) - 1.0) < 1e-6 for c in CASTING.values()))
    check("the blend is a weighted mean", blend([([0.0, 2.0], 1.0), ([2.0, 4.0], 3.0)]) == [1.5, 3.5])
    check("skin tone inside the picker", all(0.0 <= c["skin"]["u"] <= 1.0 and 0.0 <= c["skin"]["v"] <= 1.0 for c in CASTING.values()))
    print("make_cast_metahumans selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("make_cast_metahumans runs inside the editor; see the header")
