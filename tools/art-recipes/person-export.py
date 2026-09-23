"""One person for Unreal: a Mixamo character with one looping clip, as a glb.

    blender -b --factory-startup --python tools/art-recipes/person-export.py -- \
        --body "ledger/Assets/Characters/Kate.fbx" \
        --clip "ledger/Assets/Characters/B/idle_2__Standing Idle 01_....fbx" \
        --out production/assets/people/kate-idle.glb [--tex 1024]

WHY THIS EXISTS, 23 September. Jafar's presentable checklist asks for "a
handful of people [who] stand or walk in the street, even if they only
idle". The bodies and the clips are already here, in the Unity project,
downloaded under D46 (Mixamo characters and animations are allowed, bodies as
animations are). Unreal takes the street as glb, and a glb carries a skin and
its animation together, so each person crosses the same way the street does:
one file, imported on the runner.

WHAT IT DOES. Imports the body, imports the clip (a Mixamo clip is its own
skeleton with the same bone names, `mixamorig:*`), hands the clip's action to
the body's skeleton, throws the clip's skeleton away, shrinks every texture
to --tex pixels (a body's 4k maps are 50 MB and a person at fifteen metres is
a few hundred pixels tall), and exports the body alone, skinned, with the one
action. Prints one line saying what it wrote.
"""
import os
import sys


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = {"body": "", "clip": "", "out": "", "tex": 1024, "preview": "", "frame": 60,
           "from": 0, "to": 0, "also": []}
    i = 0
    while i < len(a):
        if a[i] == "--also" and i + 1 < len(a) and "=" in a[i + 1]:
            out["also"].append(tuple(a[i + 1].split("=", 1))); i += 2
        elif a[i] in ("--body", "--clip", "--out", "--preview") and i + 1 < len(a):
            out[a[i][2:]] = a[i + 1]; i += 2
        elif a[i] in ("--tex", "--frame", "--from", "--to") and i + 1 < len(a):
            out[a[i][2:]] = int(a[i + 1]); i += 2
        else:
            i += 1
    return out


def preview(bpy, path, frame):
    """The body as the action drives it HERE, before export, at one frame: the
    other half of a comparison with the exported file re-imported."""
    import math
    sc = bpy.context.scene
    sc.frame_set(frame)
    cam = bpy.data.objects.new("pcam", bpy.data.cameras.new("pcam"))
    sc.collection.objects.link(cam)
    cam.location = (0.0, -3.2, 1.0)
    cam.rotation_euler = (math.radians(88), 0, 0)
    sc.camera = cam
    sun = bpy.data.objects.new("psun", bpy.data.lights.new("psun", "SUN"))
    sc.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))
    sun.data.energy = 3
    if sc.world is None:
        sc.world = bpy.data.worlds.new("w")
    r = sc.render
    r.engine = "BLENDER_EEVEE_NEXT"
    r.resolution_x, r.resolution_y = 300, 450
    r.filepath = os.path.abspath(path)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    bpy.data.objects.remove(sun)


def main():
    import bpy
    o = args()
    if not (o["body"] and o["clip"] and o["out"]):
        print("person-export refused: need --body --clip --out"); return 2
    bpy.ops.wm.read_factory_settings(use_empty=True)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=o["body"], automatic_bone_orientation=False)
    body = [ob for ob in bpy.data.objects if ob not in before]
    body_arm = [ob for ob in body if ob.type == "ARMATURE"]
    if not body_arm:
        print("person-export refused: no skeleton in the body"); return 2
    body_arm = body_arm[0]
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=o["clip"], automatic_bone_orientation=False)
    clip = [ob for ob in bpy.data.objects if ob not in before]
    clip_arm = [ob for ob in clip if ob.type == "ARMATURE"]
    act = clip_arm[0].animation_data.action if clip_arm and clip_arm[0].animation_data else None
    if act is None:
        print("person-export refused: no action in the clip"); return 2
    # THE CLIP'S BONES MUST BE THE BODY'S, or the action drives nothing.
    names = set(b.name.split(":")[-1] for b in body_arm.data.bones)
    driven = set()
    for fc in act.fcurves:
        p = fc.data_path
        if p.startswith('pose.bones["'):
            driven.add(p.split('"')[1].split(":")[-1])
    shared = len(driven & names)
    # ONLY THE CLIP'S OWN ACTION BESIDES: the body arrives with a one-frame
    # action of its own, and it must not ride along as a second clip.
    for other in list(bpy.data.actions):
        if other != act:
            bpy.data.actions.remove(other)
    if shared == 0:
        print("person-export refused: the clip drives none of the body's bones"); return 2
    # THE CLIP'S NUMBERS, WITH THE BODY'S BONE NAMES. Mixamo bodies and
    # clips share a rest convention, so the clip's local rotations hold on
    # any body (checked by eye, four bodies by five clips, 23 September);
    # but the prefix before the colon ("mixamorig:", "mixamorig7:") varies by
    # download, so every channel is renamed to the body's own bone. SOME
    # CLIPS ARE WRONG FOR A STREET ALL BY THEMSELVES, whatever the body: the
    # talk bows double through frames 40-80, the old-man idle coughs and
    # stretches its head back in the middle, the laugh turns upside down, the
    # look over the shoulder walks off. Choose by eye; see --from and --to.
    full = {b.name.split(":")[-1]: b.name for b in body_arm.data.bones}
    # ROTATIONS ONLY, BUT FOR THE HIPS' TRAVEL. A Mixamo clip keys every
    # bone's position as well, in its own skeleton's proportions; on a body
    # of other proportions those keys shove each bone off its joint, and Joe
    # came out bent double where Kate, the clips' own skeleton, stood up.
    for fc in list(act.fcurves):
        p = fc.data_path
        if p.startswith('pose.bones["') and (p.endswith(".location") or p.endswith(".scale")):
            if p.endswith(".scale") or p.split('"')[1].split(":")[-1] != "Hips":
                act.fcurves.remove(fc)
    for fc in act.fcurves:
        p = fc.data_path
        if p.startswith('pose.bones["'):
            old = p.split('"')[1]
            new = full.get(old.split(":")[-1])
            if new and new != old:
                fc.data_path = p.replace('"%s"' % old, '"%s"' % new, 1)
    for ob in clip:
        bpy.data.objects.remove(ob, do_unlink=True)
    if body_arm.animation_data is None:
        body_arm.animation_data_create()
    act.name = os.path.splitext(os.path.basename(o["out"]))[0]
    body_arm.animation_data.action = act
    # BLENDER 4.4 AND LATER DRIVE AN OBJECT FROM ONE SLOT OF AN ACTION; without
    # the slot the body stays in its T-pose and no animation is exported.
    if hasattr(act, "slots") and len(act.slots) and hasattr(body_arm.animation_data, "action_slot"):
        body_arm.animation_data.action_slot = act.slots[0]
    # THE SKELETON IN METRES, ITS OWN TURN AND SCALE APPLIED. A Mixamo body
    # arrives with its skeleton at 1:100 and a quarter turn, bones in
    # centimetres, and Unreal's importer drops that scale on a skinned mesh:
    # the first five came in 1.7 cm tall (23 September). Applied here, the
    # file is in metres with nothing to drop. The hips' travel goes too,
    # since its keys are in the old centimetres; in place, as these clips
    # are, only a little bob is lost.
    for fc in list(act.fcurves):
        if fc.data_path.endswith(".location"):
            act.fcurves.remove(fc)
    # AND THE POSITION THOSE KEYS LEFT BEHIND: a bone with no curve keeps the
    # last value one set, and the hips kept theirs in centimetres - the first
    # export in metres stood every person 2 m back and 0.4 m in the air.
    for pb in body_arm.pose.bones:
        pb.location = (0.0, 0.0, 0.0)
    for ob in bpy.data.objects:
        ob.select_set(ob in body)
    bpy.context.view_layer.objects.active = body_arm
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    # ONE MESH, NOT NINE. A Mixamo body is its parts - body, hair, belt,
    # shoes, eyelashes - each its own skinned mesh, and Unreal's importer
    # makes a skeletal mesh of each; the import took the first it found, which
    # could be a belt. Joined here, the file holds one skinned mesh with all
    # the materials, and a person is one thing on both sides.
    parts = [ob for ob in body if ob.type == "MESH"]
    joined = len(parts)
    if len(parts) > 1:
        keep = [ob for ob in body if ob.type != "MESH"]
        for ob in bpy.data.objects:
            ob.select_set(ob in parts)
        bpy.context.view_layer.objects.active = parts[0]
        bpy.ops.object.join()
        body = keep + [bpy.context.view_layer.objects.active]
    # MORE CLIPS ON THE SAME BODY, 23 September, for the slice's player: a
    # body that stands, walks and runs is one skeleton with three actions,
    # not three people. Each --also name=path clip is adopted exactly as the
    # main one was - the body's bone names, rotations only - and named
    # <out>__<name>; each keeps its own length in the file.
    extra = []
    for label, path in o["also"]:
        before = set(bpy.data.objects)
        bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=False)
        got = [ob for ob in bpy.data.objects if ob not in before]
        arms = [ob for ob in got if ob.type == "ARMATURE"]
        a2 = arms[0].animation_data.action if arms and arms[0].animation_data else None
        for ob in got:
            bpy.data.objects.remove(ob, do_unlink=True)
        if a2 is None:
            print("person-export: --also %s has no action; left out" % label)
            continue
        for fc in list(a2.fcurves):
            if fc.data_path.endswith(".location") or fc.data_path.endswith(".scale"):
                a2.fcurves.remove(fc)
        for fc in a2.fcurves:
            p = fc.data_path
            if p.startswith('pose.bones["'):
                old = p.split('"')[1]
                new = full.get(old.split(":")[-1])
                if new and new != old:
                    fc.data_path = p.replace('"%s"' % old, '"%s"' % new, 1)
        a2.name = act.name + "__" + label
        a2.use_fake_user = True
        extra.append(a2)
    f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])
    # A CALM STRETCH OF A CLIP, when the whole of it is not: the old-man idle
    # coughs and stretches its head back in the middle and stands quietly at
    # both ends, so --from and --to export only the quiet part as the loop.
    if o["from"] and o["to"] and o["from"] < o["to"]:
        f0, f1 = max(f0, o["from"]), min(f1, o["to"])
        # WITH MORE CLIPS the file keeps each action's own range, so the calm
        # stretch is set on the main action itself rather than the scene.
        if extra and hasattr(act, "use_frame_range"):
            act.use_frame_range = True
            act.frame_start, act.frame_end = f0, f1
    # ONE ANIMATION IN THE FILE: the clip's own action goes with its skeleton.
    for other in list(bpy.data.actions):
        if other != act and other not in extra:
            bpy.data.actions.remove(other)
    bpy.context.scene.frame_start, bpy.context.scene.frame_end = int(f0), int(f1)
    # CLOTH AND SKIN ARE NOT METAL. The FBX importer turns Mixamo's
    # specular materials into half-metallic ones, and in Unreal's light a
    # coat half metal is a plastic coat.
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        for n in m.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED":
                n.inputs["Metallic"].default_value = 0.0
                # FORCED, gloss map or not: a Mixamo body's gloss maps read as
                # wet leather in any light (the first file's shirt did).
                for l in list(n.inputs["Roughness"].links):
                    m.node_tree.links.remove(l)
                n.inputs["Roughness"].default_value = 0.55 if "hair" in m.name.lower() else 0.75
    shrunk = 0
    for im in bpy.data.images:
        if im.size[0] > o["tex"] or im.size[1] > o["tex"]:
            w, h = im.size[0], im.size[1]
            k = o["tex"] / float(max(w, h))
            im.scale(max(1, int(w * k)), max(1, int(h * k)))
            im.pack()
            shrunk += 1
    for ob in bpy.data.objects:
        ob.select_set(False)
    for ob in body:
        if ob.name in bpy.data.objects:
            ob.select_set(True)
    if o["preview"]:
        preview(bpy, o["preview"], o["frame"])
    os.makedirs(os.path.dirname(os.path.abspath(o["out"])), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=os.path.abspath(o["out"]), export_format="GLB",
                              use_selection=True, export_skins=True, export_animations=True,
                              export_animation_mode="ACTIONS", export_yup=True,
                              export_frame_range=not extra, export_anim_slide_to_zero=True,
                              export_image_format="JPEG")
    size = os.path.getsize(o["out"]) if os.path.exists(o["out"]) else 0
    print("personExport out=%s bytes=%d bones=%d clipBonesShared=%d/%d frames=%d-%d texturesShrunk=%d partsJoined=%d clips=%d"
          % (o["out"], size, len(names), shared, len(driven), int(f0), int(f1), shrunk, joined, 1 + len(extra)))
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as e:
        print("person-export raised: %s" % str(e).splitlines()[0][:200]); rc = 3
    sys.exit(rc)
