"""HumanMotionCraft's clips onto two MetaHuman bodies with Unreal's own retargeter, in a scratch project (no game).

    UnrealEditor-Cmd.exe F:/LedgerTools/humanmotioncraft/ue_check/HmcCheck.uproject -run=pythonscript
        -script=<full path to this file>   with HMC_GLB_DIR, HMC_BODIES (";"-separated FBX), HMC_OUT set

Advisor 132 (13 Nov 2026, his typed approval 14:12): export to glb, retarget onto a MetaHuman in Unreal, then the leg
and foot measures beside Motionsmith. Method: production/research/ai-video-motion/CMU-RETARGET-METHOD-2026-11-12.md
(the IK Rig route) and tools/ue/retarget_sitting.py (the calls that worked on 7 Oct). Each glb is imported by
Interchange as its own skeletal mesh and clip; each body FBX by the classic importer as a skeletal mesh on the
MetaHuman skeleton; the source IK rig is tried by the engine's auto-generation first, and when that finds no legs, made
by hand from the tool's bone names (MakeHuman-style), each chain named as the MetaHuman plugin's IK_MH_IKRig names it;
one retargeter per clip and body, auto-mapped, auto-aligned, batch-retargeted and exported to FBX for measuring.
Writes HMC_OUT/ue_result.json; every step's outcome is recorded, never assumed.
"""
import json
import os
import time
import traceback

import unreal

GLB_DIR = os.environ.get("HMC_GLB_DIR", "")
BODIES = [b for b in os.environ.get("HMC_BODIES", "").split(";") if b]
OUT = os.environ.get("HMC_OUT", "")
CLIPS = ["a_sit_stand_game_ai", "b_counter_lean_game_ai", "c_busstop_smoke_game_ai"]
TARGET_RIG = "/MetaHumanCharacter/Animation/Retargeting/IK_MH_IKRig"
WORK = "/Game/HMC"

# The tool's bones by role (rig-info.json, game profile): role -> (start, end, goal bone or None).
HMC_ROLES = {
    "spine": ("spine05", "spine01", None),
    "neck": ("neck01", "neck03", None),
    "head": ("head", "head", None),
    "clavicle_l": ("clavicle.L", "shoulder01.L", None),
    "clavicle_r": ("clavicle.R", "shoulder01.R", None),
    "arm_l": ("upperarm01.L", "wrist.L", "wrist.L"),
    "arm_r": ("upperarm01.R", "wrist.R", "wrist.R"),
    # IK_MH_IKRig's leg chain runs thigh to ball with its goal on the foot: the tool's runs thigh to toe3-1 the same way.
    "leg_l": ("upperleg01.L", "toe3-1.L", "foot.L"),
    "leg_r": ("upperleg01.R", "toe3-1.R", "foot.R"),
    "thumb_l": ("finger1-1.L", "finger1-3.L", None),
    "index_l": ("finger2-1.L", "finger2-3.L", None),
    "middle_l": ("finger3-1.L", "finger3-3.L", None),
    "ring_l": ("finger4-1.L", "finger4-3.L", None),
    "pinky_l": ("finger5-1.L", "finger5-3.L", None),
    "thumb_r": ("finger1-1.R", "finger1-3.R", None),
    "index_r": ("finger2-1.R", "finger2-3.R", None),
    "middle_r": ("finger3-1.R", "finger3-3.R", None),
    "ring_r": ("finger4-1.R", "finger4-3.R", None),
    "pinky_r": ("finger5-1.R", "finger5-3.R", None),
}
# The MetaHuman's bone that starts each role: used to find IK_MH_IKRig's own chain name for the role.
MH_START = {
    "spine": "spine_01", "neck": "neck_01", "head": "head", "clavicle_l": "clavicle_l", "clavicle_r": "clavicle_r",
    "arm_l": "upperarm_l", "arm_r": "upperarm_r", "leg_l": "thigh_l", "leg_r": "thigh_r", "thumb_l": "thumb_01_l", "index_l": "index_01_l", "middle_l": "middle_01_l",
    "ring_l": "ring_01_l", "pinky_l": "pinky_01_l", "thumb_r": "thumb_01_r", "index_r": "index_01_r",
    "middle_r": "middle_01_r", "ring_r": "ring_01_r", "pinky_r": "pinky_01_r",
}

res = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "notes": [], "clips": {}, "bodies": {}, "outputs": []}


def note(s):
    res["notes"].append(s)
    unreal.log("hmc_ue_retarget: " + s)


def chains_of(rc):
    """Each chain's name, start, end and goal, read through the controller (5.8's BoneChain hides its bones)."""
    out = []
    for c in rc.get_retarget_chains():
        try:
            name = str(c.get_editor_property("chain_name"))
        except Exception:
            name = str(getattr(c, "chain_name", c))
        row = {"chain": name}
        for key, fn in (("start", "get_retarget_chain_start_bone"), ("end", "get_retarget_chain_end_bone"),
                        ("goal", "get_retarget_chain_goal")):
            try:
                row[key] = str(getattr(rc, fn)(name))
            except Exception as e:
                row[key] = "?" + str(e)[:40]
        out.append(row)
    return out


def import_task(path, dest, name, options=None):
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", path)
    t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    if options is not None:
        t.set_editor_property("options", options)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
    return [unreal.load_asset(p) for p in t.get_editor_property("imported_object_paths")]


def body_fbx(path, name):
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_mesh", True)
    ui.set_editor_property("import_as_skeletal", True)
    ui.set_editor_property("import_animations", False)
    ui.set_editor_property("import_materials", False)
    ui.set_editor_property("import_textures", False)
    ui.set_editor_property("create_physics_asset", False)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    got = import_task(path, WORK + "/Bodies", name, ui)
    return next((a for a in got if isinstance(a, unreal.SkeletalMesh)), None)


def export_fbx(seq, path):
    ex = unreal.AssetExportTask()
    ex.set_editor_property("object", seq)
    ex.set_editor_property("filename", path)
    ex.set_editor_property("automated", True)
    ex.set_editor_property("prompt", False)
    ex.set_editor_property("replace_identical", True)
    ex.set_editor_property("exporter", unreal.AnimSequenceExporterFBX())
    return bool(unreal.Exporter.run_asset_export_task(ex))


def export_mesh_fbx(mesh, path):
    ex = unreal.AssetExportTask()
    ex.set_editor_property("object", mesh)
    ex.set_editor_property("filename", path)
    ex.set_editor_property("automated", True)
    ex.set_editor_property("prompt", False)
    ex.set_editor_property("replace_identical", True)
    ex.set_editor_property("exporter", unreal.SkeletalMeshExporterFBX())
    return bool(unreal.Exporter.run_asset_export_task(ex))


def main():
    lib = unreal.EditorAssetLibrary
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    os.makedirs(os.path.join(OUT, "fbx"), exist_ok=True)
    if lib.does_directory_exist(WORK):  # the scratch project's own folder: a fresh start every run
        res["cleared"] = bool(lib.delete_directory(WORK))
    unreal.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")
    target_rig = unreal.load_asset(TARGET_RIG)
    tc = unreal.IKRigController.get_controller(target_rig)
    res["target_chains"] = chains_of(tc)
    role_name = {}
    for role, mh in MH_START.items():
        hit = next((c["chain"] for c in res["target_chains"] if c["start"] == mh), None)
        role_name[role] = hit
    res["role_to_target_chain"] = role_name

    bodies = {}
    for b in BODIES:
        name = os.path.splitext(os.path.basename(b))[0]
        m = body_fbx(b, name)
        res["bodies"][name] = {"file": b, "mesh": m.get_path_name() if m else None}
        if m:
            # The mesh is not exported back: SkeletalMeshExporterFBX asserts in a commandlet (MeshObject, no render
            # resources; 13 Nov 15:04). The film takes the body's own FBX, the file this mesh came from.
            bodies[name] = m

    for clip in CLIPS:
        row = {"glb": os.path.join(GLB_DIR, clip + ".glb")}
        res["clips"][clip] = row
        got = import_task(row["glb"], WORK + "/Src/" + clip, clip)
        row["imported"] = [a.get_path_name() for a in got if a is not None]
        mesh = next((a for a in got if isinstance(a, unreal.SkeletalMesh)), None)
        seqs = [a for a in got if isinstance(a, unreal.AnimSequence)]
        if mesh is None:  # Interchange may report only the top asset: look in the folder
            for p in lib.list_assets(WORK + "/Src/" + clip, recursive=True):
                a = unreal.load_asset(p)
                if isinstance(a, unreal.SkeletalMesh) and mesh is None:
                    mesh = a
                if isinstance(a, unreal.AnimSequence) and a not in seqs:
                    seqs.append(a)
            row["imported_folder"] = [str(p) for p in lib.list_assets(WORK + "/Src/" + clip, recursive=True)]
        if mesh is None or not seqs:
            row["error"] = "no skeletal mesh or no clip after import"
            continue
        seq = max(seqs, key=lambda a: a.get_play_length())
        row["mesh"], row["seq"] = mesh.get_path_name(), seq.get_path_name()
        row["frames"] = unreal.AnimationLibrary.get_num_frames(seq)
        row["length_s"] = seq.get_play_length()

        rig = tools.create_asset("IK_" + clip, WORK + "/Rigs", unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
        rc = unreal.IKRigController.get_controller(rig)
        rc.set_skeletal_mesh(mesh)
        try:
            row["auto_ok"] = bool(rc.apply_auto_generated_retarget_definition())
        except Exception as e:
            row["auto_ok"] = "raised " + str(e)[:120]
        row["auto_chains"] = chains_of(rc)
        # The bones as Unreal named them: Interchange turns "foot.L" into "foot_L" (13 Nov 15:05, the auto rig's chains).
        try:  # IKRigController has no skeleton reader in 5.8; the clip's own pose names every bone
            opts = unreal.AnimPoseEvaluationOptions()
            opts.set_editor_property("evaluation_type", unreal.AnimDataEvalType.RAW)
            opts.set_editor_property("should_retarget", False)
            pose = unreal.AnimPoseExtensions.get_anim_pose_at_frame(seq, 0, opts)
            bones = [str(n) for n in unreal.AnimPoseExtensions.get_bone_names(pose)]
        except Exception as e:
            bones = []
            row["bones_read"] = "refused: " + str(e)[:80]
        row["bones"] = bones
        norm = {b.replace(".", "_").replace("-", "_").lower(): b for b in bones}

        def bone(n):
            if n in bones or not bones:
                return n
            return norm.get(n.replace(".", "_").replace("-", "_").lower(), n)

        legs = [c for c in row["auto_chains"] if c["start"].lower().startswith("upperleg01") and c["end"].lower().startswith(("foot", "toe"))]
        if len(legs) < 2:
            # BY HAND: the engine's templates do not know this naming; every chain named as IK_MH_IKRig names it.
            for c in list(row["auto_chains"]):
                try:
                    rc.remove_retarget_chain(c["chain"])
                except Exception:
                    pass
            rc.set_retarget_root(bone("root"))
            for role, (start, end, goal_bone) in HMC_ROLES.items():
                name = role_name.get(role) or role
                goal = ""
                if goal_bone:
                    goal = str(rc.add_new_goal(name + "_goal", bone(goal_bone)))
                rc.add_retarget_chain(name, bone(start), bone(end), goal)
            row["rig"] = "by hand"
        else:
            row["rig"] = "auto"
        row["chains"] = chains_of(rc)
        try:
            row["root"] = str(rc.get_retarget_root())
        except Exception:
            pass
        # THE HIPS' REST HEIGHT (try 1 on this fault, 13 Nov 15:12): the tool writes its hip bone's rest at 5 cm
        # above the file's origin while its clip stands him at 85 cm, so Unreal took the source as 6 cm tall and
        # scaled the hips' motion about 16 times (pelvis 15 m up). The source's retarget pose is raised by the gap
        # between the clip's first frame (standing) and the rest, measured here, never typed in.
        root_dz = None
        try:
            ref = unreal.AnimPoseExtensions.get_reference_pose(mesh.get_editor_property("skeleton"))
            r0 = unreal.AnimPoseExtensions.get_bone_pose(ref, bone("root"), unreal.AnimPoseSpaces.WORLD).translation
            f0 = unreal.AnimPoseExtensions.get_bone_pose(pose, bone("root"), unreal.AnimPoseSpaces.WORLD).translation
            root_dz = float(f0.z - r0.z)
            row["root_rest_cm"], row["root_frame0_cm"] = [round(r0.x, 2), round(r0.y, 2), round(r0.z, 2)], [round(f0.x, 2), round(f0.y, 2), round(f0.z, 2)]
        except Exception as e:
            row["root_offset_read"] = "refused: " + str(e)[:100]
        row["root_dz_cm"] = root_dz

        for bname, bmesh in bodies.items():
            rtg = tools.create_asset("RTG_%s_to_%s" % (clip, bname), WORK + "/Rigs", unreal.IKRetargeter, unreal.IKRetargetFactory())
            ctrl = unreal.IKRetargeterController.get_controller(rtg)
            ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, rig)
            ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_rig)
            o = {"clip": clip, "body": bname, "steps": []}
            for side, m in ((unreal.RetargetSourceOrTarget.SOURCE, mesh), (unreal.RetargetSourceOrTarget.TARGET, bmesh)):
                try:
                    ctrl.set_preview_mesh(side, m)
                except Exception as e:
                    o["steps"].append("preview-mesh refused: " + str(e)[:80])
            try:
                ctrl.add_default_ops()
                ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.SOURCE, rig)
                ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.TARGET, target_rig)
                o["steps"].append("default ops")
            except Exception as e:
                o["steps"].append("ops refused: " + str(e)[:80])
            # THE ROOT MOTION STEP OFF (try 2 on the pelvis fault, 13 Nov 15:20; engine source RootMotionGeneratorOp.cpp,
            # default CopyFromSourceRoot): the source rig's root bone is the tool's hip bone, named "root", so that
            # step copied the hips' height onto the MetaHuman's floor bone and the pelvis came out at the source's
            # unscaled height, detached from its own thighs and spine. These clips stay in place: no root motion.
            if os.environ.get("HMC_ROOT_MOTION_OFF", "1") == "1":
                try:
                    names = [str(ctrl.get_op_name(i)) for i in range(ctrl.get_num_retarget_ops())]
                    o["ops"] = names
                    for i, n in enumerate(names):
                        if "root" in n.lower() and "motion" in n.lower():
                            ctrl.set_retarget_op_enabled(i, False)
                            o["steps"].append("op off: " + n)
                except Exception as e:
                    o["steps"].append("op switch refused: " + str(e)[:100])
            try:
                ctrl.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)
                o["steps"].append("chains auto-mapped")
            except Exception as e:
                o["steps"].append("auto-map refused: " + str(e)[:80])
            try:
                ctrl.auto_align_all_bones(unreal.RetargetSourceOrTarget.SOURCE)
                o["steps"].append("source aligned to target")
            except Exception as e:
                o["steps"].append("auto-align refused: " + str(e)[:80])
            if root_dz is not None and os.environ.get("HMC_ROOT_OFFSET", "1") == "1":
                try:
                    ctrl.set_root_offset_in_retarget_pose(unreal.Vector(0.0, 0.0, root_dz), unreal.RetargetSourceOrTarget.SOURCE)
                    o["steps"].append("source root raised %.2f cm" % root_dz)
                except Exception as e:
                    o["steps"].append("root offset refused: " + str(e)[:100])
            inputs = unreal.IKRetargetBatchOperationInputs()
            inputs.set_editor_property("assets_to_retarget", [unreal.AssetRegistryHelpers.create_asset_data(seq)])
            inputs.set_editor_property("source_mesh", mesh)
            inputs.set_editor_property("target_mesh", bmesh)
            inputs.set_editor_property("ik_retarget_asset", rtg)
            inputs.set_editor_property("suffix", "_" + bname)
            inputs.set_editor_property("target_path", WORK + "/Out")
            inputs.set_editor_property("include_referenced_assets", False)
            inputs.set_editor_property("overwrite_existing_files", True)
            t0 = time.time()
            result = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
            o["seconds"] = round(time.time() - t0, 2)
            names = [str(a.package_name) for a in result] if result else []
            o["made"] = names
            done = None
            for n in names:
                a = unreal.load_asset(n)
                if isinstance(a, unreal.AnimSequence):
                    done = a
            if done is None:
                o["error"] = "batch made no clip"
            else:
                o["frames"] = unreal.AnimationLibrary.get_num_frames(done)
                o["skeleton"] = done.get_editor_property("skeleton").get_path_name()
                o["fbx"] = os.path.join(OUT, "fbx", "%s__%s.fbx" % (clip, bname))
                o["exported"] = export_fbx(done, o["fbx"])
            res["outputs"].append(o)
    lib.save_directory(WORK, only_if_is_dirty=False, recursive=True)


try:
    main()
    res["status"] = "DONE"
except Exception:
    res["status"] = "RAISED"
    res["traceback"] = traceback.format_exc()
res["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
with open(os.path.join(OUT, "ue_result.json"), "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
unreal.log("hmc_ue_retarget: " + res["status"])
