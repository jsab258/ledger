"""Solve one plain video into a body animation with Epic's markerless plugin (n09-8).

Run inside the Unreal editor (commandlet or -ExecutePythonScript) with the plugins
PythonScriptPlugin, MetaHuman (Animator), CaptureManagerEditor, MetaHumanBodyTracker.
Arguments come from the environment so the commandlet line stays short:
  MOCAP_VIDEO   absolute path of an .mp4 (24 fps constant)
  MOCAP_NAME    short name for the slate and assets (letters, digits, _)
  MOCAP_FPS     expected frame rate (default 24)
  MOCAP_OUT     content folder (default /Game/MocapSolve)
  MOCAP_LOG     absolute path of a JSON result file written at every stage
Steps (production/research/ai-video-motion/PLUGIN-SOLVE-ROUTE-2026-11-09.md section 6):
ingest, frame-rate check, Performance (mono, body on, face off), blocking pipeline,
export to the performer skeleton (no retarget, so no target mesh is needed).
Every stage writes its outcome; anything but an explicit success stops the run.
"""
import json
import os
import time
import traceback

import unreal

VIDEO = os.environ.get("MOCAP_VIDEO", "")
NAME = os.environ.get("MOCAP_NAME", "solve")
FPS = float(os.environ.get("MOCAP_FPS", "24"))
OUT = os.environ.get("MOCAP_OUT", "/Game/MocapSolve")
LOG = os.environ.get("MOCAP_LOG", "")
result = {"video": VIDEO, "name": NAME, "stages": [], "ok": False}


def note(stage, ok, **kw):
    entry = {"stage": stage, "ok": bool(ok), "t": time.strftime("%H:%M:%S")}
    entry.update({k: (v if isinstance(v, (int, float, str, bool, type(None), list, dict)) else str(v)) for k, v in kw.items()})
    result["stages"].append(entry)
    unreal.log("MOCAPSOLVE " + json.dumps(entry))
    if LOG:
        with open(LOG, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=1)
    return ok


def run():
    if not os.path.isfile(VIDEO):
        return note("input", False, error="video not found")
    note("input", True, size=os.path.getsize(VIDEO))

    for plugin_class in ("CaptureManagerIngestBlueprintLibrary", "MetaHumanPerformance", "MetaHumanPerformanceExportUtils"):
        if not hasattr(unreal, plugin_class):
            return note("plugins", False, missing=plugin_class)
    note("plugins", True)

    # 1. Ingest
    params = unreal.CaptureManagerConversionParams()
    lib = unreal.CaptureManagerIngestBlueprintLibrary
    got = lib.ingest_mono_video_sync(VIDEO, "", NAME, 1, params)
    capture, err = (got if isinstance(got, tuple) else (got, ""))
    if capture is None:
        return note("ingest", False, error=err)
    note("ingest", True, asset=capture.get_path_name())

    # 2. Frame rate: the ingest leaves the image sequence at 0/1000 (the forum's
    # "0 fps" fault; the Performance then rejects the capture). Set the sequence's
    # override and the capture's metadata to the clip's rate, both, then save.
    rates = []
    want = unreal.FrameRate(int(round(FPS)), 1)
    for seq in capture.get_editor_property("image_sequences"):
        if not seq:
            continue
        before = seq.get_editor_property("frame_rate_override")
        seq.set_editor_property("frame_rate_override", want)
        after = seq.get_editor_property("frame_rate_override")
        unreal.EditorAssetLibrary.save_loaded_asset(seq)
        rates.append({"seq": seq.get_name(), "before": "%d/%d" % (before.numerator, before.denominator),
                      "after": "%d/%d" % (after.numerator, after.denominator)})
    try:
        meta = capture.get_editor_property("metadata")
        meta.set_editor_property("frame_rate", FPS)
        capture.set_editor_property("metadata", meta)
        rates.append({"metadata_frame_rate": capture.get_editor_property("metadata").get_editor_property("frame_rate")})
    except Exception as e:
        rates.append({"metadata_error": str(e)[:300]})
    unreal.EditorAssetLibrary.save_loaded_asset(capture)
    good = all(r.get("after", "%d/1" % int(FPS)) == "%d/1" % int(round(FPS)) for r in rates if "after" in r) and any("after" in r for r in rates)
    if not note("frame_rate", good, read=rates, expected=FPS):
        return False

    # 3. Performance: mono footage, body tracking on, face off
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    perf = tools.create_asset(asset_name=NAME + "_Performance", package_path=OUT,
                              asset_class=unreal.MetaHumanPerformance,
                              factory=unreal.MetaHumanPerformanceFactoryNew())
    if perf is None:
        return note("performance", False, error="create_asset returned None")
    perf.set_editor_property("input_type", unreal.DataInputType.MONO_FOOTAGE)
    perf.set_editor_property("footage_capture_data", capture)
    if perf.get_editor_property("footage_capture_data") is None:
        return note("performance", False, error="capture rejected (frame rate?)")
    # SetBodyTracking is a BlueprintSetter, not exposed as a method; set_editor_property calls it
    perf.set_editor_property("body_tracking", True)
    perf.set_editor_property("face_tracking", False)
    note("performance", True, asset=perf.get_path_name(),
         body=perf.get_editor_property("body_tracking"),
         face=perf.get_editor_property("face_tracking"),
         foot_locking=perf.get_editor_property("enable_foot_locking"))

    # 4. Blocking pipeline. StartPipeline answers DISABLED when CanProcess() is false
    # and says no more (no .cpp ships), so record what the asset holds first.
    diag = {}
    for prop in ("camera", "focal_length", "start_frame_to_process", "end_frame_to_process", "input_type"):
        try:
            diag[prop] = str(perf.get_editor_property(prop))
        except Exception as e:
            diag[prop] = "unread: %s" % str(e)[:120]
    diag["can_process_before"] = perf.can_process()
    if not diag.get("camera") or diag["camera"] in ("", "None"):
        try:
            views = [str(v) for v in capture.get_editor_property("image_sequences") if v]
            diag["views"] = views
        except Exception as e:
            diag["views"] = "unread: %s" % str(e)[:120]
    try:
        perf.set_processing_range(0, 81)
    except Exception as e:
        diag["range_error"] = str(e)[:200]
    diag["can_process_after_range"] = perf.can_process()
    note("diagnostics", True, **diag)
    perf.set_blocking_processing(True)
    t0 = time.time()
    perr = perf.start_pipeline()
    secs = round(time.time() - t0, 1)
    frames = None
    try:
        frames = perf.get_number_of_processed_frames()
    except Exception as e:
        frames = "unread: %s" % e
    if perr != unreal.StartPipelineErrorType.NONE:
        return note("pipeline", False, error=str(perr), seconds=secs, frames=frames)
    note("pipeline", True, seconds=secs, frames=frames)

    # 5. Export onto the performer skeleton
    settings = unreal.MetaHumanPerformanceExportAnimationSettings()
    settings.set_editor_property("show_export_dialog", False)
    settings.set_editor_property("export_face", False)
    settings.set_editor_property("export_body", True)
    settings.set_editor_property("export_skeleton", unreal.PerformanceExportSkeleton.PERFORMER_SKELETON)
    settings.set_editor_property("package_path", OUT)
    settings.set_editor_property("asset_name", NAME + "_Body")
    anim = unreal.MetaHumanPerformanceExportUtils.export_animation_sequence(perf, settings)
    if not anim:
        return note("export", False, error="export_animation_sequence returned None")
    info = {"asset": anim.get_path_name()}
    try:
        info["length_s"] = anim.get_editor_property("sequence_length")
    except Exception:
        pass
    unreal.EditorAssetLibrary.save_directory(OUT)
    note("export", True, **info)
    result["ok"] = True
    note("done", True)


try:
    run()
except Exception:
    note("exception", False, error=traceback.format_exc()[-1500:])
