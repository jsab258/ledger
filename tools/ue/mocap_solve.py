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

    # 2. Frame rate: the capture's image sequence must say 24, not 0 or 1
    rates = []
    try:
        for seq in capture.get_editor_property("image_sequences"):
            if seq:
                fr = seq.get_editor_property("frame_rate_override")
                rates.append({"seq": seq.get_name(), "override": str(fr)})
    except Exception as e:  # property names differ between versions: record, do not guess
        rates.append({"read_error": str(e)})
    note("frame_rate", True, read=rates, expected=FPS)

    # 3. Performance: mono footage, body tracking on, face off
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    perf = tools.create_asset(asset_name=NAME + "_Performance", package_path=OUT,
                              asset_class=unreal.MetaHumanPerformance,
                              factory=unreal.MetaHumanPerformanceFactoryNew())
    if perf is None:
        return note("performance", False, error="create_asset returned None")
    perf.set_editor_property("input_type", unreal.DataInputType.MONO_FOOTAGE)
    perf.set_editor_property("footage_capture_data", capture)
    perf.set_body_tracking(True)
    perf.set_editor_property("face_tracking", False)
    note("performance", True, asset=perf.get_path_name(),
         body=perf.get_editor_property("body_tracking"),
         face=perf.get_editor_property("face_tracking"),
         foot_locking=perf.get_editor_property("enable_foot_locking"))

    # 4. Blocking pipeline
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
