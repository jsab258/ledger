"""A quick look from the hook camera at an exported street, for composition only.

    blender --background --factory-startup --python tools/art-recipes/hook-preview.py \
        -- --glb production/assets/street/quay-street.glb --out PREVIEW.png [--res 1280x720]

WHY, 3 October (the proof view, step 2.1, composition). Judging the street's masses (what stands
where, how high, what closes the view, where the hill sits) needs a frame from the hook camera,
and the Unreal editor cannot run on this PC while the build machine builds. This imports the
street exactly as Unreal receives it and renders it in Blender's Workbench (flat shading, no
graphics-card render worth the name): the masses and their outline against the sky, not the
look. The look is judged in the game's own camera, never here (CLAUDE.md).

THE CAMERA is the scene file's cam_hook (production/specs/vignette-scene.json), read, not typed:
along the street x_m, across it z_m (east positive), eye_height_m over the crown, yaw_deg toward
the east, pitch_deg negative looking up (the frame's horizon sits below its middle), and
fov_vertical_deg. The glb arrives in Blender with east at -Y (the export's reflection and glTF's
axes together), so the camera stands at y = -z_m and turns toward -Y.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def args_after_dashes(argv):
    a = argv[argv.index("--") + 1:] if "--" in argv else []
    out = {"glb": os.path.join(ROOT, "production", "assets", "street", "quay-street.glb"),
           "out": "", "res": "1280x720", "camera": "cam_hook", "plan": "", "cull": ""}
    i = 0
    while i < len(a):
        if a[i] in ("--glb", "--out", "--res", "--camera", "--plan", "--cull") and i + 1 < len(a):
            out[a[i][2:]] = a[i + 1]
            i += 2
        else:
            i += 1
    return out


def camera_spec(name):
    spec = json.load(open(os.path.join(ROOT, "production", "specs", "vignette-scene.json"), encoding="utf-8"))
    for c in spec["cameras"]:
        if c["id"] == name:
            return c
    raise KeyError(name)


def main():
    import bpy
    a = args_after_dashes(sys.argv)
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.import_scene.gltf(filepath=a["glb"])
    c = camera_spec(a["camera"])
    cam_data = bpy.data.cameras.new("hook")
    cam_data.sensor_fit = "VERTICAL"
    cam_data.angle_y = math.radians(c["fov_vertical_deg"])
    cam_data.clip_end = 2000.0
    cam = bpy.data.objects.new("hook", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    # looking north (+X): rotation (90, 0, -90); east is -Y here, so a yaw toward the east turns
    # the view clockwise seen from above (more negative about Z); pitch_deg negative looks up.
    cam.location = (c["x_m"], -c["z_m"], c["eye_height_m"] + c.get("declared_ground", {}).get("y_m", 0.0))
    cam.rotation_euler = (math.radians(90.0 - c["pitch_deg"]), 0.0, math.radians(-90.0 - c["yaw_deg"]))
    if a["plan"]:
        # --plan X0,X1,Y0,Y1: looking straight down on the street (x north up the picture,
        # east to the right), to see what stands where; the hook camera is marked by a post.
        x0, x1, y0, y1 = (float(v) for v in a["plan"].split(","))
        cam_data.type = "ORTHO"
        cam_data.ortho_scale = max(x1 - x0, y1 - y0)
        cam.location = ((x0 + x1) / 2.0, -(y0 + y1) / 2.0, 300.0)
        cam.rotation_euler = (0.0, 0.0, math.radians(90.0))
        bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=60.0, location=(c["x_m"], -c["z_m"], 30.0))
    sc = bpy.context.scene
    sc.camera = cam
    w, h = (int(v) for v in a["res"].split("x"))
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.engine = "BLENDER_WORKBENCH"
    shading = sc.display.shading
    shading.light = "STUDIO"
    shading.color_type = "MATERIAL"
    shading.show_shadows = True
    shading.show_cavity = True
    # --cull 1: back faces hidden, as Unreal draws one-sided surfaces, to catch a face wound inwards
    shading.show_backface_culling = a["cull"] == "1"
    sc.display.shadow_focus = 0.6
    # the sky as the sheet's: a pale overcast grey
    sc.world = sc.world or bpy.data.worlds.new("w")
    sc.world.color = (0.80, 0.81, 0.82)
    shading.background_type = "VIEWPORT"
    shading.background_color = (0.80, 0.81, 0.82)
    sc.render.filepath = a["out"]
    bpy.ops.render.render(write_still=True)
    print("hookPreview out=%s camera=%s at=(%.2f,%.2f,%.2f) yaw=%.1f pitch=%.1f fovV=%.1f" % (
        a["out"], a["camera"], cam.location.x, cam.location.y, cam.location.z,
        c["yaw_deg"], c["pitch_deg"], c["fov_vertical_deg"]))


if __name__ == "__main__":
    main()
