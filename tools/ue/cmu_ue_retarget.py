"""CMU moves onto the cast with Unreal's own retargeter: step 4 of
production/research/ai-video-motion/CMU-RETARGET-METHOD-2026-11-12.md (review 17 Nov, fixes taken).

    UnrealEditor-Cmd.exe <ue-probe>/LedgerProbe.uproject -run=pythonscript -script=<FULL path to this file>
        -EnablePlugins=PythonScriptPlugin -unattended -nop4 -nosplash
    env: CMU_IN (default F:/LedgerTools/game-inputs/cmu-2026-11-17), CMU_OUT (a folder under F:/LedgerTools),
         CMU_BODIES (";"-separated body mesh paths; default Ron's and Rocco's)

Inputs are cmu_clips.py's files: one T-pose FBX per source subject (rest = cgspeed's frame 0, stand-in cube on the
hips) and each clip as that skeleton's motion only (first two 30 fps steps trimmed, no limb flips). As
retarget_sitting.py (7 Oct): the T-pose imported as a skeletal mesh, its clips onto its skeleton; as
tools/tool-tests/hmc_ue_retarget.py (13 Nov): the engine's auto rig first, by hand when it finds no legs, every hand
chain named as IK_MH_IKRig names it; one retargeter per subject and body, default ops, chains auto-mapped, the source
auto-aligned to the MetaHuman's A-pose, batch-retargeted and exported to FBX for the measured check.
The method's guards: leg chains LeftUpLeg to LeftFoot (never from LHipJoint); no finger or thumb chain (the set has no
finger data); the retarget root is Hips; the root-motion op is off (these clips sit and rise in place; the exit's
root motion from the target pelvis is a later step). The rest is real standing height, so no root offset is set
(hmc's 5 cm rest fault does not arise; the rest heights are recorded). Any BadPelvisHeight line in the editor log is a
stop: the caller reads the log after the run. Writes CMU_OUT/ue_result.json; every step's outcome recorded.

Feet (try 1 of 2 on the fault "CMU feet", 17 Nov; diagnosis F:/LedgerTools/tool-dev/reports/
CMU-RETARGET-FEET-DIAGNOSIS-2026-11-17.md, 5.8.2 source cited there):
- Target: a copy of IK_MH_IKRig made in WORK each run (Epic's asset never edited) with the leg chains ending at foot_l/r,
  the foot goals on foot_l/r and one-bone chains LeftFoot/RightFoot on ball_l/r, so the source and target leg chains
  end at the same joint (the ankle) and the toes ride on their own FK chain (Run IK Rig places a goal from the chain
  END's length and rotation: RunIKRigOp.cpp 64-80, 110-154).
- FK Chains: leg chains One to One (Interpolated blends shin and foot with FastLerp, whose sign flip twists the foot
  for one frame: IKRetargetProcessor.cpp 705, Quat.h 1374-1376).
- Source retarget pose: after auto-align, the source foot and toe are turned back to their own T-pose orientation
  (auto-align turns the up-leg about 26 degrees and the feet inherit it; the target then stood toe-down 15-28 degrees).
- Scale Source (factor = the body's reference pelvis height over the source Hips height) and Blend to Source under
  Run IK Rig on the leg chains, horizontal only (per axis 1, 1, 0): planted feet stay on the scaled source's ground
  marks; height stays chain-relative, so each body keeps its own ankle height (CMU ankles sit 2.6-6 cm up, the
  MetaHuman's 9.5-9.8: a full blend sank the feet 4-14 cm in the diagnosis).
- Each body's reference pose of the measured roles goes into ue_result.json (body_ref) for cmu_bone_dump.py's rest.
"""
import json
import os
import time
import traceback

import unreal

IN = os.environ.get("CMU_IN", "F:/LedgerTools/game-inputs/cmu-2026-11-17")
OUT = os.environ.get("CMU_OUT", "F:/LedgerTools/game-inputs/cmu-2026-11-17/ue")
BODIES = [b for b in os.environ.get("CMU_BODIES", "/Game/Ledger/MetaHumans/MH_RoccoP2/Body/SKM_MH_RoccoP2_BodyMesh;"
                                    "/Game/Ledger/MetaHumans/MH_Rocco/Body/SKM_MH_Rocco_BodyMesh").split(";") if b]
SUBJECTS = {"143_18": ["sit_get_up_143_18"], "113_15": ["sit_get_up_113_15"], "131_01": ["start_walk_stop_131_01"]}
TARGET_RIG = "/MetaHumanCharacter/Animation/Retargeting/IK_MH_IKRig"  # Epic's: read and copied, never edited
WORK = "/Game/Retarget/CMU"
ANKLE_RIG = WORK + "/IK_MH_IKRig_ankle"  # the copy with ankle goals, remade every run (WORK is cleared first)
BLEND_AXES = (1.0, 1.0, 0.0)  # Blend to Source per axis: horizontal from the scaled source, height chain-relative
MH_ROLES = ("pelvis", "thigh_l", "calf_l", "foot_l", "ball_l", "thigh_r", "calf_r", "foot_r", "ball_r")
CMU_FOOT_PARENTS = ("CmuRig", "Hips", "{s}HipJoint", "{s}UpLeg", "{s}Leg")  # root down to the foot's parent (cgspeed)

# CMU (cgspeed, MotionBuilder naming) bones by role: role -> (start, end, goal bone or None). No finger chains.
CMU_ROLES = {
    "spine": ("LowerBack", "Spine1", None),
    "neck": ("Neck", "Neck1", None),
    "head": ("Head", "Head", None),
    "clavicle_l": ("LeftShoulder", "LeftShoulder", None),
    "clavicle_r": ("RightShoulder", "RightShoulder", None),
    "arm_l": ("LeftArm", "LeftHand", "LeftHand"),
    "arm_r": ("RightArm", "RightHand", "RightHand"),
    "leg_l": ("LeftUpLeg", "LeftFoot", "LeftFoot"),
    "leg_r": ("RightUpLeg", "RightFoot", "RightFoot"),
    "toe_l": ("LeftToeBase", "LeftToeBase", None),
    "toe_r": ("RightToeBase", "RightToeBase", None),
}
MH_START = {"spine": "spine_01", "neck": "neck_01", "head": "head", "clavicle_l": "clavicle_l",
            "clavicle_r": "clavicle_r", "arm_l": "upperarm_l", "arm_r": "upperarm_r", "leg_l": "thigh_l", "leg_r": "thigh_r",
            "toe_l": "ball_l", "toe_r": "ball_r"}
FINGERS = ("thumb", "index", "middle", "ring", "pinky", "finger")

res = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "notes": [], "subjects": {}, "outputs": []}


def note(s):
    res["notes"].append(s)
    unreal.log("cmu_ue_retarget: " + s)


def chains_of(rc):
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


def fbx(path, dest, name, skeleton):
    """The FBX as a skeletal mesh (skeleton None) or as an animation on skeleton (retarget_sitting.py's way)."""
    lib = unreal.EditorAssetLibrary
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_mesh", skeleton is None)
    ui.set_editor_property("import_as_skeletal", True)
    ui.set_editor_property("import_animations", skeleton is not None)
    ui.set_editor_property("import_materials", False)
    ui.set_editor_property("import_textures", False)
    ui.set_editor_property("create_physics_asset", False)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH
                           if skeleton is None else unreal.FBXImportType.FBXIT_ANIMATION)
    if skeleton is not None:
        ui.set_editor_property("skeleton", skeleton)
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", path)
    t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    t.set_editor_property("options", ui)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
    return [lib.load_asset(q) for q in lib.list_assets(dest, recursive=True, include_folder=False)]


def export_fbx(seq, path):
    ex = unreal.AssetExportTask()
    ex.set_editor_property("object", seq)
    ex.set_editor_property("filename", path)
    ex.set_editor_property("automated", True)
    ex.set_editor_property("prompt", False)
    ex.set_editor_property("replace_identical", True)
    ex.set_editor_property("exporter", unreal.AnimSequenceExporterFBX())
    return bool(unreal.Exporter.run_asset_export_task(ex))


def qmul(a, b):
    """Hamilton product of (w, x, y, z) tuples, as FQuat's operator*: a * b applies b first."""
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (aw * bw - ax * bx - ay * by - az * bz, aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx, aw * bz + ax * by - ay * bx + az * bw)


def qinv(a):
    return (a[0], -a[1], -a[2], -a[3])


def wxyz(q):
    return (q.w, q.x, q.y, q.z)


def make_ankle_rig(lib):
    """The copy of Epic's IK_MH_IKRig with ankle goals and toe chains; returns (rig, record) or raises with the reason."""
    if lib.does_asset_exist(ANKLE_RIG):  # a leftover of this script's own work folder: remade from Epic's every run
        lib.delete_asset(ANKLE_RIG)
    rig = lib.duplicate_asset(TARGET_RIG, ANKLE_RIG)
    if rig is None:
        raise RuntimeError("could not copy %s to %s" % (TARGET_RIG, ANKLE_RIG))
    ac = unreal.IKRigController.get_controller(rig)
    for side, sfx in (("Left", "l"), ("Right", "r")):
        leg = next((c["chain"] for c in chains_of(ac) if c["start"] == "thigh_" + sfx), None)
        if not leg:
            raise RuntimeError("the copy has no leg chain from thigh_" + sfx)
        goal = str(ac.get_retarget_chain_goal(leg))
        ok = [bool(ac.set_retarget_chain_end_bone(leg, "foot_" + sfx)), bool(ac.set_goal_bone(goal, "foot_" + sfx))]
        name = str(ac.add_retarget_chain(side + "Foot", "ball_" + sfx, "ball_" + sfx, "None"))
        if not all(ok) or name in ("", "None"):
            raise RuntimeError("ankle edit refused on %s (end/goal %s, toe chain %s)" % (side, ok, name))
    rec = dict(chains=[c for c in chains_of(ac) if "Leg" in c["chain"] or "Foot" in c["chain"]],
               goals={str(g.get_editor_property("goal_name")): str(g.get_editor_property("bone_name")) for g in ac.get_all_goals()})
    bad = [c["chain"] for c in rec["chains"] if c["start"].startswith("thigh_") and not c["end"].startswith("foot_")]
    bad += [g for g, b in rec["goals"].items() if "Foot" in g and not b.startswith("foot_")]
    if bad or len([c for c in rec["chains"] if c["start"].startswith("ball_")]) != 2:
        raise RuntimeError("ankle rig reads back wrong: %s" % rec)
    return rig, rec


def ref_roles(mesh, name, dest):
    """A mesh's own reference pose (component space, cm) of the measured roles, read through a scratch IK rig."""
    rig = unreal.AssetToolsHelpers.get_asset_tools().create_asset(name, dest, unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
    if rig is None:  # a leftover the folder delete could not remove (seen 17 Nov): reuse it, its mesh is set again below
        rig = unreal.load_asset("%s/%s" % (dest, name))
    if rig is None:
        raise RuntimeError("no reference rig %s/%s" % (dest, name))
    rc = unreal.IKRigController.get_controller(rig)
    rc.set_skeletal_mesh(mesh)
    out = {}
    for r in MH_ROLES:
        t = rc.get_ref_pose_transform_of_bone(r).translation
        out[r] = [round(t.x, 4), round(t.y, 4), round(t.z, 4)]
    return out


def restore_source_feet(ctrl, src_rc):
    """Turn the source foot and toe back to their T-pose orientation after auto-align. E = accumulated global turn of
    the retarget pose over the reference: E(b) = E(parent) * Qg(b) * D(b) * Qg(b)^-1 (IKRetargetProcessor.cpp 77: local
    = ref local * delta). The foot's delta D = Qg(foot)^-1 * E(parent)^-1 * Qg(foot) makes E(foot) identity; the toe's
    delta is then reset to identity. Returns the angle of the turn removed per side, in degrees."""
    import math
    SRC = unreal.RetargetSourceOrTarget.SOURCE
    out = {}
    for side in ("Left", "Right"):
        e = (1.0, 0.0, 0.0, 0.0)
        for name in CMU_FOOT_PARENTS:
            b = name.format(s=side)
            qg = wxyz(src_rc.get_ref_pose_transform_of_bone(b).rotation)
            d = wxyz(ctrl.get_rotation_offset_for_retarget_pose_bone(b, SRC))
            e = qmul(e, qmul(qg, qmul(d, qinv(qg))))
        foot, toe = side + "Foot", side + "ToeBase"
        qf = wxyz(src_rc.get_ref_pose_transform_of_bone(foot).rotation)
        d = qmul(qinv(qf), qmul(qinv(e), qf))
        ctrl.set_rotation_offset_for_retarget_pose_bone(foot, unreal.Quat(d[1], d[2], d[3], d[0]), SRC)
        ctrl.set_rotation_offset_for_retarget_pose_bone(toe, unreal.Quat(0.0, 0.0, 0.0, 1.0), SRC)
        back = wxyz(ctrl.get_rotation_offset_for_retarget_pose_bone(foot, SRC))
        out[side] = dict(removed_deg=round(math.degrees(2.0 * math.acos(min(1.0, abs(e[0])))), 2),
                         readback_ok=abs(abs(sum(x * y for x, y in zip(back, d))) - 1.0) < 1e-4)
    return out


def op_idx(ctrl, name):
    return next((i for i in range(ctrl.get_num_retarget_ops()) if str(ctrl.get_op_name(i)) == name), -1)


def set_fk_one_to_one(ctrl, leg_chains):
    """One to One on the leg chains of the FK Chains op; returns the modes read back."""
    def idx(name):
        return op_idx(ctrl, name)
    rec = {}
    oc = ctrl.get_op_controller(idx("FK Chains"))
    st = oc.get_settings()
    new = []
    for c in st.get_editor_property("chains_to_retarget"):
        if str(c.get_editor_property("target_chain_name")) in leg_chains:
            c.set_editor_property("rotation_mode", unreal.FKChainRotationMode.ONE_TO_ONE)
        new.append(c)
    st.set_editor_property("chains_to_retarget", new)
    oc.set_settings(st)
    rec["fk_legs"] = {str(c.get_editor_property("target_chain_name")): str(c.get_editor_property("rotation_mode"))
                      for c in ctrl.get_op_controller(idx("FK Chains")).get_settings().get_editor_property("chains_to_retarget")
                      if str(c.get_editor_property("target_chain_name")) in leg_chains}
    return rec["fk_legs"]


def add_leg_ops(ctrl, factor):
    """Scale Source first in the stack (factor set), Blend to Source added under Run IK Rig; returns (record, blend name)."""
    def idx(name):
        return op_idx(ctrl, name)
    rec = {}
    i = ctrl.add_retarget_op("/Script/IKRig.IKRetargetScaleSourceOp")
    scale_name = str(ctrl.get_op_name(i))
    oc = ctrl.get_op_controller(i)
    st = oc.get_settings()
    st.set_editor_property("source_scale_factor", factor)
    oc.set_settings(st)
    ctrl.move_retarget_op_in_stack(idx(scale_name), 0)
    rec["scale"] = dict(name=scale_name, index=idx(scale_name),
                        factor=round(ctrl.get_op_controller(idx(scale_name)).get_settings().get_editor_property("source_scale_factor"), 5))
    i = ctrl.add_retarget_op("/Script/IKRig.IKRetargetBlendToSourceOp")
    blend_name = str(ctrl.get_op_name(i))
    rec["blend_parent_set"] = bool(ctrl.set_parent_op_by_name(blend_name, "Run IK Rig"))
    return rec, blend_name


def set_blend(ctrl, blend_name, leg_chains):
    def idx(name):
        return op_idx(ctrl, name)
    oc = ctrl.get_op_controller(idx(blend_name))
    st = oc.get_settings()
    new = []
    for c in st.get_editor_property("chains"):
        if str(c.get_editor_property("target_chain_name")) in leg_chains:
            c.set_editor_property("blend_to_source", 1.0)
            c.set_editor_property("translation_alpha", 1.0)
            c.set_editor_property("rotation_alpha", 0.0)
            c.set_editor_property("translation_per_axis_alpha", unreal.Vector(*BLEND_AXES))
        new.append(c)
    st.set_editor_property("chains", new)
    oc.set_settings(st)
    back = {}
    for c in ctrl.get_op_controller(idx(blend_name)).get_settings().get_editor_property("chains"):
        n = str(c.get_editor_property("target_chain_name"))
        if n in leg_chains:
            v = c.get_editor_property("translation_per_axis_alpha")
            back[n] = dict(blend=round(c.get_editor_property("blend_to_source"), 3), t=round(c.get_editor_property("translation_alpha"), 3),
                           r=round(c.get_editor_property("rotation_alpha"), 3), axes=[round(v.x, 3), round(v.y, 3), round(v.z, 3)])
    return back


def main():
    lib = unreal.EditorAssetLibrary
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    os.makedirs(os.path.join(OUT, "fbx"), exist_ok=True)
    if lib.does_directory_exist(WORK):  # this script's own work folder: a fresh start every run
        res["cleared"] = bool(lib.delete_directory(WORK))
    unreal.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")
    if unreal.load_asset(TARGET_RIG) is None:
        raise RuntimeError("no target rig " + TARGET_RIG)
    target_rig, res["ankle_rig"] = make_ankle_rig(lib)
    res["target_rig"] = ANKLE_RIG
    tc = unreal.IKRigController.get_controller(target_rig)
    res["target_chains"] = chains_of(tc)
    role_name = {role: next((c["chain"] for c in res["target_chains"] if c["start"] == mh), None)
                 for role, mh in MH_START.items()}
    res["role_to_target_chain"] = role_name
    bodies = {}
    for b in BODIES:
        m = unreal.load_asset(b)
        res.setdefault("bodies", {})[b] = bool(m)
        if isinstance(m, unreal.SkeletalMesh):
            bodies[b.split("/")[-1].replace("SKM_MH_", "").replace("_BodyMesh", "")] = m
    if not bodies:
        raise RuntimeError("no body mesh loaded")
    res["body_ref"] = {bn: ref_roles(bm, "IK_Ref_" + bn, WORK + "/ref") for bn, bm in bodies.items()}

    for subj, clips in SUBJECTS.items():
        row = {"clips": {}}
        res["subjects"][subj] = row
        dest = WORK + "/" + subj
        got = fbx(os.path.join(IN, "tpose_%s.fbx" % subj), dest, "tpose", None)
        mesh = next((a for a in got if isinstance(a, unreal.SkeletalMesh)), None)
        if mesh is None:
            row["error"] = "no T-pose mesh"
            continue
        skel = mesh.get_editor_property("skeleton")
        anims = []
        for clip in clips:
            before = set(str(a.get_path_name()) for a in got if a is not None)
            got = fbx(os.path.join(IN, clip + ".fbx"), dest, clip, skel)
            seqs = [a for a in got if isinstance(a, unreal.AnimSequence) and str(a.get_path_name()) not in before]
            if not seqs:
                row["clips"][clip] = {"error": "no clip after import"}
                continue
            seq = max(seqs, key=lambda a: a.get_play_length())
            row["clips"][clip] = {"seq": seq.get_path_name(), "frames": unreal.AnimationLibrary.get_num_frames(seq),
                                  "length_s": round(seq.get_play_length(), 3)}
            anims.append((clip, seq))
        if not anims:
            continue
        # Rest heights, recorded (the retargeter scales the pelvis by them).
        try:
            ref = unreal.AnimPoseExtensions.get_reference_pose(skel)
            h = unreal.AnimPoseExtensions.get_bone_pose(ref, "Hips", unreal.AnimPoseSpaces.WORLD).translation
            row["rest_hips_cm"] = [round(h.x, 2), round(h.y, 2), round(h.z, 2)]
        except Exception as e:
            row["rest_hips_read"] = "refused: " + str(e)[:100]

        rig = tools.create_asset("IK_CMU_" + subj, dest, unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
        rc = unreal.IKRigController.get_controller(rig)
        rc.set_skeletal_mesh(mesh)
        try:
            row["auto_ok"] = bool(rc.apply_auto_generated_retarget_definition())
        except Exception as e:
            row["auto_ok"] = "raised " + str(e)[:120]
        row["auto_chains"] = chains_of(rc)
        legs_ok = [c for c in row["auto_chains"] if c["start"] in ("LeftUpLeg", "RightUpLeg")]
        if len(legs_ok) < 2:
            # BY HAND: legs from the up-leg (the method: never from LHipJoint), every chain named as IK_MH_IKRig names it.
            for c in list(row["auto_chains"]):
                try:
                    rc.remove_retarget_chain(c["chain"])
                except Exception:
                    pass
            for role, (start, end, goal_bone) in CMU_ROLES.items():
                name = role_name.get(role) or role
                goal = str(rc.add_new_goal(name + "_goal", goal_bone)) if goal_bone else ""
                rc.add_retarget_chain(name, start, end, goal)
            row["rig"] = "by hand"
        else:
            # The auto rig kept, but no finger or thumb chain (placeholders in the set, flips 17 Nov).
            for c in row["auto_chains"]:
                if any(f in c["chain"].lower() for f in FINGERS):
                    try:
                        rc.remove_retarget_chain(c["chain"])
                    except Exception:
                        pass
            row["rig"] = "auto"
        try:
            rc.set_retarget_root("Hips")
        except Exception as e:
            row["root_set"] = "refused: " + str(e)[:80]
        row["chains"] = chains_of(rc)
        try:
            row["root"] = str(rc.get_retarget_root())
        except Exception as e:
            row["root"] = "unread: " + str(e)[:80]
        # The method's guards read back, a stop for this subject when any fails (review 17 Nov, fix 2).
        bad = []
        if row["root"] != "Hips":
            bad.append("retarget root reads %s, not Hips" % row["root"])
        starts = [c["start"] for c in row["chains"]]
        for leg in ("LeftUpLeg", "RightUpLeg"):
            if leg not in starts:
                bad.append("no leg chain from " + leg)
        for toe in ("LeftToeBase", "RightToeBase"):
            if toe not in starts:
                bad.append("no toe chain from " + toe)
        for c in row["chains"]:
            if c["start"] in ("LeftUpLeg", "RightUpLeg") and not c["end"].endswith("Foot"):
                bad.append("leg chain %s ends at %s, not the ankle" % (c["chain"], c["end"]))
        if any(any(f in c["chain"].lower() for f in FINGERS) for c in row["chains"]):
            bad.append("a finger or thumb chain is left")
        if row["rig"] == "by hand":
            want = set(role_name.get(r) or r for r in CMU_ROLES)
            missing = sorted(want - set(c["chain"] for c in row["chains"]))
            if missing:
                bad.append("hand-built rig lacks " + ", ".join(missing))
        if bad:
            row["error"] = "; ".join(bad)
            note("%s stopped: %s" % (subj, row["error"]))
            continue

        for bname, bmesh in bodies.items():
            rtg = tools.create_asset("RTG_CMU_%s_to_%s" % (subj, bname), dest, unreal.IKRetargeter, unreal.IKRetargetFactory())
            ctrl = unreal.IKRetargeterController.get_controller(rtg)
            ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, rig)
            ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_rig)
            o = {"subject": subj, "body": bname, "body_mesh": bmesh.get_path_name(), "steps": []}
            stop = []  # a refused op, auto-map or auto-align step: no batch, no export (review fix 3)
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
                stop.append("ops refused: " + str(e)[:80])
            try:  # the root-motion op off: in place (method step 4; hmc's try 2 found its default copies the hips' height)
                names = [str(ctrl.get_op_name(i)) for i in range(ctrl.get_num_retarget_ops())]
                o["ops"] = names
                off = 0
                for i, n in enumerate(names):
                    if "root" in n.lower() and "motion" in n.lower():
                        ctrl.set_retarget_op_enabled(i, False)
                        o["steps"].append("op off: " + n)
                        off += 1
                if not off:
                    stop.append("no root-motion op found by name among %s" % names)  # review fix 1
            except Exception as e:
                stop.append("op switch refused: " + str(e)[:100])
            try:
                ctrl.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)
                o["steps"].append("chains auto-mapped")
            except Exception as e:
                stop.append("auto-map refused: " + str(e)[:80])
            try:
                ctrl.auto_align_all_bones(unreal.RetargetSourceOrTarget.SOURCE)
                o["steps"].append("source aligned to target")
            except Exception as e:
                stop.append("auto-align refused: " + str(e)[:80])
            legs = [role_name["leg_l"], role_name["leg_r"]]
            try:
                hips = rc.get_ref_pose_transform_of_bone("Hips").translation.z
                factor = res["body_ref"][bname]["pelvis"][2] / hips
                o["leg_ops"], blend_name = add_leg_ops(ctrl, factor)
                ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.SOURCE, rig)
                ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.TARGET, target_rig)
                o["leg_ops"]["fk_legs"] = set_fk_one_to_one(ctrl, legs)
                o["blend"] = set_blend(ctrl, blend_name, legs)
                lo = o["leg_ops"]
                lo["fk_legs"] = {str(c.get_editor_property("target_chain_name")): str(c.get_editor_property("rotation_mode"))
                                 for c in ctrl.get_op_controller(op_idx(ctrl, "FK Chains")).get_settings().get_editor_property("chains_to_retarget")
                                 if str(c.get_editor_property("target_chain_name")) in legs}
                lo["scale"]["index"] = op_idx(ctrl, lo["scale"]["name"])
                if any(v != str(unreal.FKChainRotationMode.ONE_TO_ONE) for v in lo["fk_legs"].values()) or len(lo["fk_legs"]) != 2:
                    stop.append("leg chains not One to One: %s" % lo["fk_legs"])
                if lo["scale"]["index"] != 0 or abs(lo["scale"]["factor"] - factor) > 1e-3:
                    stop.append("Scale Source not first or factor wrong: %s (want %.4f)" % (lo["scale"], factor))
                if not lo["blend_parent_set"] or str(ctrl.get_parent_op_by_name(blend_name)) != "Run IK Rig":
                    stop.append("Blend to Source is not under Run IK Rig")
                if sorted(o["blend"]) != sorted(legs) or any(v["blend"] != 1.0 or v["axes"] != list(BLEND_AXES) for v in o["blend"].values()):
                    stop.append("Blend to Source leg settings read back wrong: %s" % o["blend"])
                o["steps"].append("legs One to One, Scale Source %.4f, Blend to Source (horizontal)" % factor)
            except Exception as e:
                stop.append("leg ops refused: " + str(e)[:160])
            try:
                o["feet_restored"] = restore_source_feet(ctrl, rc)
                if not all(v["readback_ok"] for v in o["feet_restored"].values()):
                    stop.append("source foot pose offsets read back wrong: %s" % o["feet_restored"])
                o["steps"].append("source feet back to their T-pose orientation")
            except Exception as e:
                stop.append("foot restore refused: " + str(e)[:120])
            try:
                o["mapping"] = {op: {t: str(ctrl.get_source_chain(t, op)) for t in legs + [role_name["toe_l"], role_name["toe_r"]]}
                                for op in ("FK Chains", "Run IK Rig")}
                toe_src = {c["chain"] for c in row["chains"] if c["start"] in ("LeftToeBase", "RightToeBase")}
                if not {o["mapping"]["FK Chains"][role_name["toe_l"]], o["mapping"]["FK Chains"][role_name["toe_r"]]} <= toe_src:
                    stop.append("the ball chains are not mapped to the source toe chains: %s" % o["mapping"]["FK Chains"])
            except Exception as e:
                stop.append("mapping read refused: " + str(e)[:100])
            o["ops"] = [dict(name=str(ctrl.get_op_name(i)), enabled=bool(ctrl.get_retarget_op_enabled(i)),
                             parent=str(ctrl.get_parent_op_by_name(ctrl.get_op_name(i)))) for i in range(ctrl.get_num_retarget_ops())]
            if stop:
                o["error"] = "; ".join(stop)
                note("%s to %s stopped before the batch: %s" % (subj, bname, o["error"]))
                res["outputs"].append(o)
                continue
            inputs = unreal.IKRetargetBatchOperationInputs()
            inputs.set_editor_property("assets_to_retarget", [unreal.AssetRegistryHelpers.create_asset_data(a) for _, a in anims])
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
            made = [str(a.package_name) for a in result] if result else []
            o["made"] = made
            o["clips"] = {}
            for clip, _ in anims:
                hit = next((n for n in made if clip in n.split("/")[-1]), None)
                done = unreal.load_asset(hit) if hit else None
                if not isinstance(done, unreal.AnimSequence):
                    o["clips"][clip] = {"error": "batch made no clip"}
                    continue
                path = os.path.join(OUT, "fbx", "%s__%s.fbx" % (clip, bname))
                o["clips"][clip] = {"asset": hit, "frames": unreal.AnimationLibrary.get_num_frames(done),
                                    "skeleton": done.get_editor_property("skeleton").get_path_name(),
                                    "fbx": path, "exported": export_fbx(done, path)}
            res["outputs"].append(o)
    lib.save_directory(WORK, only_if_is_dirty=False, recursive=True)


res["deferred"] = ("131_01 (start, walk, stop) runs in place with the root-motion op off; the exit's root motion "
                   "generated from the target pelvis is put off to a later step (method step 4, review fix 5)")
EXPECTED = sum(len(c) for c in SUBJECTS.values()) * len(BODIES)
try:
    main()
    res["status"] = "DONE"
except Exception:
    res["status"] = "RAISED"
    res["traceback"] = traceback.format_exc()
n_ok = sum(1 for o in res["outputs"] for c in o.get("clips", {}).values() if c.get("exported"))
if res["status"] == "DONE" and n_ok < EXPECTED:  # DONE only when every export succeeded (review fix 4)
    res["status"] = "INCOMPLETE"
res["exported"], res["expected"] = n_ok, EXPECTED
res["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "ue_result.json"), "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print("cmuRetarget=%s exported=%d result=%s" % (res["status"], n_ok, os.path.join(OUT, "ue_result.json").replace(" ", "~")))
unreal.log("cmu_ue_retarget: " + res["status"])
