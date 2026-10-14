"""The gate stage: calibrate the stand-in sky and lamps, render the review views and the measuring frames, the masks, the reflection-off night frames, the review previews.

Written 14 October for the house windows from the shop kit's sw_gate_run.py (copied that day, md5 75b34a4d...): what is kept is the shape (bake, render, previews, the check renders beside the frames); the views,
the calibration and the masks are the house windows'. One render at a time (the machine is shared): `python3 build_windows.py gate [name ...]` renders what is missing.

Frames (GATE folder, outside git): frame_<name>_<state>.png (2560 x 1440 beauty), mask_<name>_<state>.png (flat colours: R 1 glass, 2 joinery, 3 cloth, 4 brick, 5 card; G the window's number), and for
the night frames refloff_<name>_night.png (1280 x 720, the glass's reflection off: the check for a band the lamps' pools put in the night glass, unit 7's close review) and the camera JSON beside each.
The review set goes to production/previews/cloud-week/house-windows/hw-<view>-<state>-2026-10-13.jpg (about 1600 px, under 500 KB).
"""
import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hw_t as T  # noqa: E402
import hw_ctx as C  # noqa: E402
import hw_gate as G  # noqa: E402

CLOSE_SITE = "east_parade_bay0_upper_w1"
# name -> (camera key or (H name, site id), states)
FRAMES = [
    ("hook", "cam_hook", ("day", "night")),
    ("reverse", "cam_reverse", ("day", "night")),
    ("cam-a", "cam_A", ("day", "night")),
    ("close", ("H_ALONG_30_NEAR", CLOSE_SITE), ("day", "night")),
    ("h-across0-bay3w1", ("H_ACROSS_0", "east_parade_bay3_upper_w1"), ("day",)),
    ("h-along15-bay3w1", ("H_ALONG_15_NEAR", "east_parade_bay3_upper_w1"), ("day",)),
    ("h-along30-bay1w1", ("H_ALONG_30_NEAR", "east_parade_bay1_upper_w1"), ("day",)),
    ("h-across0-bay2w0", ("H_ACROSS_0", "east_parade_bay2_upper_w0"), ("day", "night")),
    ("h-along30-gf2w1", ("H_ALONG_30_NEAR", "west_south_bay2_gf_w1"), ("day", "night")),
    ("h-under-bay1w0", ("H_UNDER", "east_parade_bay1_upper_w0"), ("day",)),
]
# WB-08: the first build's pane (an opaque pale card, F0 0.04, no box shade) in the same view as the bare window at 15 degrees; its mask is that frame's own
OLD_FAULT = ("old-fault", "h-along15-bay3w1", "east_parade_bay3_upper_w1")
SAMPLES = int(os.environ.get("LEDGER_GATE_SAMPLES", "40"))


def camera_of(key):
    if isinstance(key, str):
        return C.view_cameras()[key]
    name, sid = key
    return C.h_camera(name, T.site(sid))


def lights_path():
    return os.path.join(T.GATE, "gate_lights.json")


def calibrate(log=print):
    """sky_strength: a Lambertian grey card (albedo 0.18) facing the street reads linear 0.18 +- 0.01 in the render's own pixels (target 9); lamp_w: the paving under the near lamp reads sRGB 150 +- 20."""
    import bpy
    from mathutils import Vector
    os.makedirs(T.GATE, exist_ok=True)
    lp = lights_path()
    if os.path.exists(lp):
        return json.load(open(lp))

    def scene(night, strength, lamp_w=0.0):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = bpy.context.scene
        w = bpy.data.worlds.new("w")
        sc.world = w
        w.use_nodes = True
        wn = w.node_tree
        env = wn.nodes.new("ShaderNodeTexEnvironment")
        env.image = bpy.data.images.load(T.SKY_HDRI, check_existing=True)
        wn.links.new(env.outputs["Color"], wn.nodes["Background"].inputs["Color"])
        wn.nodes["Background"].inputs["Strength"].default_value = strength * (0.15 if night else 1.0)
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 24
        sc.cycles.use_denoising = False
        sc.render.resolution_x = sc.render.resolution_y = 64
        sc.view_settings.view_transform = "Standard"
        sc.render.image_settings.file_format = "PNG"
        return sc

    def read(path):
        a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32) / 255.0
        c = a[24:40, 24:40].mean(axis=(0, 1))
        return float(np.mean(G.lin(c))), float(np.mean(c) * 255.0)

    s = 1.0
    out = os.path.join(T.GATE, "cal.png")
    for it in range(3):
        rs = []
        for ny in (-1.0, 1.0):
            sc = scene(False, s)
            m = bpy.data.materials.new("grey")
            m.use_nodes = True
            m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.18, 0.18, 0.18, 1)
            m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
            bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, 0), rotation=(math.radians(90.0 * (-ny)), 0, 0))
            pl = bpy.context.object
            pl.data.materials.append(m)
            cd = bpy.data.cameras.new("c")
            cd.angle = math.radians(20)
            co = bpy.data.objects.new("c", cd)
            sc.collection.objects.link(co)
            co.location = (0, 3.0 * ny, 0)
            co.rotation_euler = (math.radians(90.0), 0, math.radians(0 if ny < 0 else 180.0))
            sc.camera = co
            sc.render.filepath = out
            bpy.ops.render.render(write_still=True)
            rs.append(read(out)[0])
        r = float(np.mean(rs))
        log("   sky strength %.3f: grey card reads %.4f linear" % (s, r))
        if abs(r - 0.18) < 0.006:
            break
        s *= 0.18 / max(r, 1e-4)
    # lamps
    lamp_w = 4000.0
    for it in range(4):
        sc = scene(True, s)
        m = bpy.data.materials.new("pav")
        m.use_nodes = True
        m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*G.lin([0.5, 0.5, 0.48]), 1)
        m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.85
        bpy.ops.mesh.primitive_plane_add(size=14.0, location=(0, 0, 0.10))
        bpy.context.object.data.materials.append(m)
        sp = bpy.data.lights.new("l", "SPOT")
        sp.color = (1.0, 0.25, 0.0)
        sp.energy = lamp_w
        sp.spot_size = math.radians(92)
        sp.spot_blend = 0.5
        sp.shadow_soft_size = 0.15
        lo = bpy.data.objects.new("l", sp)
        sc.collection.objects.link(lo)
        lo.location = (0, 0, 4.52)
        cd = bpy.data.cameras.new("c")
        cd.angle = math.radians(8)
        co = bpy.data.objects.new("c", cd)
        sc.collection.objects.link(co)
        co.location = (0, 0, 9.0)
        co.rotation_euler = (0, 0, 0)
        sc.camera = co
        sc.render.filepath = out
        bpy.ops.render.render(write_still=True)
        a = np.asarray(Image.open(out).convert("RGB")).astype(np.float32)
        c = a[24:40, 24:40].mean(axis=(0, 1))
        luma = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
        log("   lamp %.0f W: the paving under the lamp reads sRGB luma %.0f (colour %s)" % (lamp_w, luma, [round(float(v)) for v in c]))
        if abs(luma - 150.0) < 8:
            break
        lamp_w *= (G.lin(np.array([150.0 / 255.0]))[0] / max(float(G.lin(np.array([luma / 255.0]))[0]), 1e-5))
    res = {"sky_strength": round(float(s), 4), "lamp_w": round(float(lamp_w), 1), "lamp_height_m": 4.52, "note": "calibrated by hw_gate_run.calibrate (grey card 0.18; paving under the lamp sRGB luma 150)"}
    json.dump(res, open(lp, "w"), indent=1)
    return res


def jpeg_under(im, path, kb=480, width=1600):
    im = im.convert("RGB")
    if im.width > width:
        im = im.resize((width, int(round(im.height * width / im.width))), Image.LANCZOS)
    q = 90
    while q >= 40:
        im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(path) <= kb * 1024:
            break
        q -= 5
    return os.path.getsize(path)


def run(names=None, samples=None, log=print):
    cal = calibrate(log)
    extra = {"sky_strength": cal["sky_strength"], "lamp_w": cal["lamp_w"]}
    os.makedirs(T.GATE, exist_ok=True)
    os.makedirs(T.PREVIEWS, exist_ok=True)
    cards = os.path.join(T.GATE, "cards")
    tp = os.path.join(T.GATE, "render_times.json")
    times = json.load(open(tp)) if os.path.exists(tp) else {}
    recs_p = os.path.join(T.GATE, "gate_frames.json")
    recs = json.load(open(recs_p)) if os.path.exists(recs_p) else {}
    for name, key, states in FRAMES:
        if names and name not in names:
            continue
        cam = camera_of(key)
        for st in states:
            fr = os.path.join(T.GATE, "frame_%s_%s.png" % (name, st))
            mk = os.path.join(T.GATE, "mask_%s_%s.png" % (name, st))
            ro = os.path.join(T.GATE, "refloff_%s_%s.png" % (name, st))
            tag = "%s_%s" % (name, st)
            if not os.path.exists(fr):
                t, rec = G.build_and_render(name, cam, st, fr, cards, samples=samples or SAMPLES, extra=extra, log=log)
                times[tag] = t
                recs[tag] = rec
                log("frame %s: %.0f s" % (tag, t))
                json.dump(times, open(tp, "w"), indent=1)
                json.dump(recs, open(recs_p, "w"), indent=1)
            if not os.path.exists(mk):
                t, rec = G.build_and_render(name, cam, st, mk, cards, mode="mask", extra=extra, log=log)
                times["mask_" + tag] = t
                json.dump(times, open(tp, "w"), indent=1)
            if st == "night" and not os.path.exists(ro):
                t, rec = G.build_and_render(name, cam, st, ro, cards, samples=16, res=(1280, 720), glass_refl=0.0, extra=extra, log=log)
                times["refloff_" + tag] = t
                json.dump(times, open(tp, "w"), indent=1)
            if name in ("hook", "reverse", "cam-a", "close"):
                pst = "night_lit" if st == "night" else st
                jp = os.path.join(T.PREVIEWS, "hw-%s-%s-%s.jpg" % (name, pst, T.DATE))
                if not os.path.exists(jp):
                    sz = jpeg_under(Image.open(fr), jp)
                    log("preview %s: %d KB" % (os.path.basename(jp), sz // 1024))
    if not names or "old-fault" in names:
        old_fault(cal, extra, cards, times, tp, samples, log)
    return times


def old_fault(cal, extra, cards, times, tp, samples, log=print):
    """WB-08: render the view of the bare window at 15 degrees with the old pane (no reflection, pale and opaque, no box shade) and measure it by the same mask; writes old_fault.json beside the frames."""
    import hw_measure as MS
    name, base, sid = OLD_FAULT
    key = next(k for n, k, st in FRAMES if n == base)
    mk = os.path.join(T.GATE, "mask_%s_day.png" % base)
    op = os.path.join(T.GATE, "old_fault.json")
    fr = os.path.join(T.GATE, "frame_%s_day.png" % name)
    if os.path.exists(op):
        return
    if not os.path.exists(mk):
        log("old fault: the mask of %s is not rendered yet (python3 build_windows.py gate %s)" % (base, base))
        return
    ex = dict(extra)
    ex["old_fault"] = True
    if not os.path.exists(fr):
        t, rec = G.build_and_render(name, camera_of(key), "day", fr, cards, samples=min(samples or SAMPLES, 24), extra=ex, log=log)
        times["old_fault_day"] = t
        json.dump(times, open(tp, "w"), indent=1)
        log("frame old_fault_day: %.0f s" % t)
    b, m = MS.load(fr, mk)
    recs = json.load(open(os.path.join(T.GATE, "gate_frames.json")))
    w = recs["%s_day" % base]["windows"]
    out = {"view": base, "site": sid, "windows": {}}
    for s_id, wi in w.items():
        st = MS.stats_for(b, m, wi["id"])
        if st is None:
            continue
        st["line"] = MS.line_profile(b, m, wi["id"], st["L"])
        st["angle"] = wi["angle_deg"]
        out["windows"][s_id] = {k: st[k] for k in ("P", "L", "D", "spread", "P_over_L", "D_over_L", "line", "angle")}
    if sid not in out["windows"]:
        log("old fault: the window %s is not measured in the frame" % sid)
        return
    t = out["windows"][sid]
    out.update({k: t[k] for k in ("P_over_L", "D_over_L", "spread", "line")})
    json.dump(out, open(op, "w"), indent=1)
    log("old fault: P/L %.2f D/L %.2f spread %.0f line %s" % (t["P_over_L"], t["D_over_L"], t["spread"], t["line"]))


if __name__ == "__main__":
    run(sys.argv[1:] or None)
