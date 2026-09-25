"""A face animation for each character's spoken line, from the audio alone.

    set LEDGER_MH_SCRIPT=speech_faces
    set LEDGER_SPEECH_WAVS=F:/LedgerTools/tmp/speech/sheila-dunn.wav,...
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY, 25 September. Jafar's ruling: each MetaHuman candidate is shown front,
profile AND SPEAKING in the game's light, because one image cannot define a
head. Nothing in the project moved a mouth (asset-coverage research: "no lip
sync exists anywhere"). UE 5.8's MetaHuman Animator makes a face animation
from audio alone (a MetaHumanPerformance with audio input, processed on this
PC), the same way its own example process_audio_performance.py does.

Each wav becomes a SoundWave, a performance, and an animation sequence on
the face skeleton the built cast use (the one Epic's face idle plays on), at
/Game/Ledger/MetaHumans/Speech/AS_<name>. Head movement is off: the body's own idle
moves the head. Writes speech-faces.txt beside the project.

THE MOOD, 25 September, afternoon: Jafar asked why Sheila looked high. The
first solve let the mood be detected from the voice, and a calm voice was
read as low: the lids drooped and the eyes drifted. LEDGER_SPEECH_MOOD picks
the mood (NEUTRAL by default), LEDGER_SPEECH_OUTPUT the controls solved
(FULL_FACE, or MOUTH_ONLY, which leaves the eyes at rest, open and ahead),
and LEDGER_SPEECH_SUFFIX names the variant (AS_<name><suffix>).
"""
import os
import time

DEST = "/Game/Ledger/MetaHumans/Speech"   # with the cast, outside the public repository
MOOD, OUTPUT, SUFFIX = "NEUTRAL", "FULL_FACE", ""
FACE_IDLE = "/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/mhc_mh001_fmn_f_idle.mhc_mh001_fmn_f_idle"


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "speech-faces.txt")
    wavs = [w for w in os.environ.get("LEDGER_SPEECH_WAVS", "").split(",") if w]
    global MOOD, OUTPUT, SUFFIX
    MOOD = os.environ.get("LEDGER_SPEECH_MOOD", "NEUTRAL")
    OUTPUT = os.environ.get("LEDGER_SPEECH_OUTPUT", "FULL_FACE")
    SUFFIX = os.environ.get("LEDGER_SPEECH_SUFFIX", "")

    def log(lines, l):
        lines.append(l)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def one(wav, lines):
        name = os.path.splitext(os.path.basename(wav))[0].replace("-", "_")
        t0 = time.time()
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", wav)
        task.set_editor_property("destination_path", DEST)
        task.set_editor_property("destination_name", "SW_" + name)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        sound = unreal.load_asset(DEST + "/SW_" + name)
        if sound is None:
            log(lines, "%s NO-SOUND" % name)
            return
        tools = unreal.AssetToolsHelpers.get_asset_tools()
        perf = tools.create_asset(asset_name="PF_" + name + SUFFIX, package_path=DEST,
                                  asset_class=unreal.MetaHumanPerformance, factory=unreal.MetaHumanPerformanceFactoryNew())
        perf.set_editor_property("input_type", unreal.DataInputType.AUDIO)
        perf.set_editor_property("audio", sound)
        over = unreal.AudioDrivenAnimationSolveOverrides()
        over.mood = getattr(unreal.AudioDrivenAnimationMood, MOOD)
        over.mood_intensity = 1.0
        perf.set_editor_property("audio_driven_animation_solve_overrides", over)
        perf.set_editor_property("audio_driven_animation_output_controls", getattr(unreal.AudioDrivenAnimationOutputControls, OUTPUT))
        perf.set_editor_property("head_movement_mode", unreal.PerformanceHeadMovementMode.DISABLED)
        perf.set_blocking_processing(True)
        err = perf.start_pipeline()
        log(lines, "%s processed err=%s in %.0f s" % (name, err, time.time() - t0))
        idle = unreal.load_asset(FACE_IDLE)
        skel = idle.get_editor_property("skeleton") if idle else None
        es = unreal.MetaHumanPerformanceExportAnimationSettings()
        es.show_export_dialog = False
        es.package_path = DEST
        es.asset_name = "AS_" + name + SUFFIX
        if skel is not None:
            es.target_skeleton_or_skeletal_mesh = skel
        es.enable_head_movement = False
        es.export_range = unreal.PerformanceExportRange.PROCESSING_RANGE
        anim = unreal.MetaHumanPerformanceExportUtils.export_animation_sequence(perf, es)
        if anim is None:
            log(lines, "%s NO-ANIMATION" % name)
            return
        unreal.EditorAssetLibrary.save_directory(DEST, only_if_is_dirty=False, recursive=True)
        log(lines, "%s AS_%s%s mood=%s output=%s length=%.2fs skeleton=%s sound=%.2fs total %.0f s" % (
            name, name, SUFFIX, MOOD, OUTPUT, anim.get_play_length(), skel.get_path_name() if skel else "none",
            sound.get_editor_property("duration"), time.time() - t0))

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        lines = []
        try:
            for w in wavs:
                try:
                    one(w, lines)
                except Exception as e:
                    log(lines, "%s RAISED %r" % (w, e))
            log(lines, "done")
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
