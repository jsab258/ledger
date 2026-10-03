#!/usr/bin/env python3
"""THE HOOK CAMERA'S PROFILE, read off the engine's own CSV (P1, 3 October).

    python tools/perf-hook.py CSV [--label NAME]      # one JSON line: frame, GPU, passes, draws, memory
    python tools/perf-hook.py --table A.json B.json   # the runs side by side, as text
    python tools/perf-hook.py --selftest

WHY. Jafar's order of 3 October (P1): "profile the hook camera, standing and walking,
with the voice speaking, with Nanite and virtual shadows on and off, and tell me plainly
what the proof view can add within 60 frames a second on this card, and what would make
room: the voice on the processor, the settings, or both." The game's -PerfHook=stand|walk
holds the scene file's cam_hook (or walks it up the street) and starts the engine's CSV
profiler once the street has settled, with -csvGpuStats for the time of every pass; this
reads that file. The verdict is the ruling's (tools/slice-perf.py): MEETS when the median
frame is at or under 16.7 ms and the slowest 1% at or under 33.3 ms. The planning line of
the pre-production review is kept beside it: a GPU median of 14.0 ms (4-BUDGETS.md, 4.1).
"""
import csv
import json
import os
import statistics
import sys

GPU_LINE_MS = 14.0                 # the review's planning line for the GPU median (4-BUDGETS.md)
PASS_GROUPS = {                    # the per-pass columns, summed into the budget's own shares
    "lumen": ("LumenSceneUpdate", "LumenScreenProbeGather", "LumenReflections", "UpdateLumenSceneBuffers",
              "DistanceFields", "GlobalDistanceFieldUpdate", "DistanceFieldShadows"),
    "base pass and prepass": ("Basepass", "Prepass", "CompositionBeforeBasePass", "RenderVelocities", "HZB"),
    "shadows": ("ShadowDepths", "ShadowProjection"),
    "lights and lighting": ("RenderDeferredLighting", "Lights", "LightGrid", "TranslucentLighting", "LightFunctionAtlasGeneration"),
    "translucency and glass": ("Translucency", "FrontLayerTranslucencyGBuffer", "Distortion"),
    "fog and sky": ("Fog", "LocalFogVolumeVolumes", "SkyAtmosphere", "SkyAtmosphereLUTs", "CaptureConvolveSkyEnvMap", "VolumetricFog"),
    "upscale and post": ("TemporalSuperResolution", "Postprocessing", "PostRenderOpsFX"),
    "people (hair and skin)": ("HairGuideInterpolation", "HairCardsInterpolation", "HairStrands", "SubsurfaceScattering"),
}


def read(path, drop=0):
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        rows = list(csv.reader(fh))
    header = rows[0]
    body = [r for r in rows[1:] if len(r) == len(header)][drop:]
    return header, body


def column(header, body, name):
    if name not in header:
        return []
    i = header.index(name)
    out = []
    for r in body:
        try:
            out.append(float(r[i]))
        except ValueError:
            pass
    return out


def slowest_1pct(xs):
    s = sorted(xs)
    return statistics.mean(s[-max(1, len(s) // 100):]) if s else None


def med(xs):
    return round(statistics.median(xs), 2) if xs else None


def summarise(header, body, label=""):
    frame = column(header, body, "FrameTime")
    gpu = column(header, body, "GPUTime")
    passes = {}
    for h in header:
        if h.startswith("GPU/"):
            m = med(column(header, body, h))
            if m:
                passes[h[4:]] = m
    groups = {g: round(sum(passes.get(n, 0.0) for n in names), 2) for g, names in PASS_GROUPS.items()}
    named = {n for names in PASS_GROUPS.values() for n in names}
    groups["other"] = round(sum(v for k, v in passes.items() if k not in named and k != "Total"), 2)
    f50, f1 = med(frame), slowest_1pct(frame)
    verdict = None
    if f50 is not None and f1 is not None:
        verdict = "MEETS" if f50 <= 16.7 and f1 <= 33.3 else ("BELOW-60" if f1 <= 33.3 else "BELOW-30")
    return {
        "label": label, "frames": len(frame),
        "frameMedianMs": f50, "frameSlowest1pctMs": round(f1, 2) if f1 is not None else None,
        "gpuMedianMs": med(gpu), "gpuLineMs": GPU_LINE_MS,
        "gpuRoomMs": round(GPU_LINE_MS - med(gpu), 2) if gpu else None,
        "verdict": verdict,
        "groups": groups,
        "topPasses": sorted(passes.items(), key=lambda kv: -kv[1])[:8],
        "drawCalls": med(column(header, body, "RHI/DrawCalls")),
        "primitives": med(column(header, body, "RHI/PrimitivesDrawn")),
        "gpuMemMB": med(column(header, body, "GPUMem/LocalUsedMB")),
        "systemMemMB": med(column(header, body, "PhysicalUsedMB")),
        "walkedM": round(max(column(header, body, "View/PosX") or [0]) / 100.0 - min(column(header, body, "View/PosX") or [0]) / 100.0, 1),
    }


def table(rows):
    keys = ["label", "frameMedianMs", "frameSlowest1pctMs", "gpuMedianMs", "gpuRoomMs", "verdict", "drawCalls", "primitives", "gpuMemMB"]
    out = [" | ".join(keys)]
    for r in rows:
        out.append(" | ".join(str(r.get(k)) for k in keys))
    groups = list(rows[0]["groups"].keys()) if rows else []
    out.append("")
    out.append("pass group | " + " | ".join(r["label"] for r in rows))
    for g in groups:
        out.append(g + " | " + " | ".join(str(r["groups"].get(g)) for r in rows))
    return "\n".join(out)


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("perf-hook selftest FAIL " + name)
    header = ["FrameTime", "GPUTime", "GPU/Basepass", "GPU/ShadowDepths", "GPU/LumenReflections", "GPU/Mystery", "RHI/DrawCalls", "View/PosX"]
    body = [[str(14 + (k % 3)), str(12 + (k % 2)), "3", "2", "1.5", "0.5", "900", str(k * 10)] for k in range(200)]
    s = summarise(header, body, "t")
    check("the median frame and GPU are read", s["frameMedianMs"] == 15.0 and s["gpuMedianMs"] == 12.5)
    check("the room under the planning line", s["gpuRoomMs"] == 1.5)
    check("the ruling's verdict", s["verdict"] == "MEETS")
    check("passes fall into their budget groups, the rest into other",
          s["groups"]["base pass and prepass"] == 3.0 and s["groups"]["shadows"] == 2.0 and s["groups"]["lumen"] == 1.5 and s["groups"]["other"] == 0.5)
    check("the walk's distance is read from the view", s["walkedM"] == 19.9)
    slow = [[str(40), "38", "3", "2", "1.5", "0.5", "900", "0"] for _ in range(200)]
    check("a frame of 40 ms is below 30", summarise(header, slow)["verdict"] == "BELOW-30")
    print("perf-hook selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--table" in argv:
        rows = [json.load(open(p, encoding="utf-8")) for p in argv[argv.index("--table") + 1:]]
        print(table(rows))
        return 0
    path = argv[0]
    label = argv[argv.index("--label") + 1] if "--label" in argv else os.path.basename(path)
    header, body = read(path)
    print(json.dumps(summarise(header, body, label)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
