"""Tom's retarget from the Game Animation Sample's mannequin: an IK rig for Tom's body and a
retargeter from the sample's UEFN mannequin to it, made by Unreal's own auto-characterisation.

    UnrealEditor-Cmd.exe ue-probe/LedgerProbe.uproject -run=pythonscript -script=tools/ue/make_tom_retarget.py -EnablePlugins=PythonScriptPlugin -unattended -nopause -nosplash -nullrhi -stdout
    python tools/ue/make_tom_retarget.py --selftest

WHY, 22 October 2026 (his order of 21 October, item 7: "Tom's walk rebuilt on Epic's Game Animation
Sample with motion matching"). The sample's motion matching runs on its own UEFN mannequin (the
sample's databases are built on that skeleton); the game runs it on a hidden mannequin beside Tom
and copies the pose onto Tom's own body each frame through this retargeter (Unreal's IK retargeting,
the way the sample itself dresses its other characters: its RetargetedCharacters, RTG_UEFN_to_*).

WHAT IT MAKES, under /Game/Ledger/People/tom-player: IK_TomPlayer (Tom's chains, found by Unreal's
auto-characterisation of his skeleton) and RTG_UEFN_to_TomPlayer (source the sample's
IK_UEFN_Mannequin, target IK_TomPlayer, chains mapped and the bones aligned automatically); and the
motion-matching graph the hidden mannequin runs, ABP_TomMotion (with the sample's Offset Root
Bone) and ABP_TomMotionPlain (without, for a comparison): animation blueprints on the mannequin's
skeleton whose parent is the game's ULedgerMotionMatchAnim, their nodes laid out and compiled by
the game's own ULedgerMotionMatchTools.wire_motion_match_blueprint (MotionMatchAnim.h says why a
blueprint). Nothing here is made by hand.
ONE LINE, appended to ue-material.txt.
"""
import os
import sys

TOM_MESH = "/Game/Ledger/People/tom-player/SK_tom-player"
SOURCE_RIG = "/Game/Characters/UEFN_Mannequin/Rigs/IK_UEFN_Mannequin"
MANNEQUIN = "/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin"
GRAPHS = (("ABP_TomMotion", True), ("ABP_TomMotionPlain", False))
DEST = "/Game/Ledger/People/tom-player"
RIG_NAME = "IK_TomPlayer"
RTG_NAME = "RTG_UEFN_to_TomPlayer"


def main():
    import unreal
    lib = unreal.EditorAssetLibrary
    notes = []
    at = unreal.AssetToolsHelpers.get_asset_tools()
    clear_old(unreal)
    mesh = lib.load_asset(TOM_MESH)
    src = lib.load_asset(SOURCE_RIG)
    if mesh is None or src is None:
        line = "tomRetargetStatus=NO-INPUT mesh=%s sourceRig=%s" % (mesh is not None, src is not None)
    else:
        rig = at.create_asset(RIG_NAME, DEST, unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
        rc = unreal.IKRigController.get_controller(rig)
        rc.set_skeletal_mesh(mesh)
        try:
            rc.apply_auto_generated_retarget_definition()
            notes.append("auto-retarget-definition")
        except Exception as e:
            notes.append("auto-def-failed:%s" % str(e)[:60])
        chains = []
        try:
            chains = [str(c.get_editor_property("chain_name")) for c in rc.get_retarget_chains()]
        except Exception as e:
            notes.append("chains?:%s" % str(e)[:40])
        try:
            notes.append("root=%s" % rc.get_retarget_root())
        except Exception:
            pass
        rtg = at.create_asset(RTG_NAME, DEST, unreal.IKRetargeter, unreal.IKRetargetFactory())
        tc = unreal.IKRetargeterController.get_controller(rtg)
        tc.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, src)
        tc.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, rig)
        for step, fn in (("default-ops", lambda: tc.add_default_ops()),
                         ("map-chains", lambda: tc.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)),
                         ("align-bones", lambda: tc.auto_align_all_bones(unreal.RetargetSourceOrTarget.TARGET))):
            try:
                fn()
                notes.append(step)
            except Exception as e:
                notes.append("%s-failed:%s" % (step, str(e)[:60]))
        lib.save_loaded_asset(rig)
        lib.save_loaded_asset(rtg)
        line = "tomRetargetStatus=OK chains=%d %s notes=%s" % (len(chains), ",".join(chains)[:200], "/".join(notes))
        line += " " + make_graphs(unreal, lib, at)
    with open(os.path.join(unreal.Paths.project_dir(), "ue-material.txt"), "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print("make_tom_retarget: " + line)
    return 0


def clear_old(unreal):
    """THIS SCRIPT'S OWN EARLIER OUTPUTS, removed before anything loads them: in a commandlet the
    library's delete reports success and leaves the file (22 October), and the remake then finds
    the old asset in its way. Only the five assets this script makes, never anything else."""
    folder = os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_content_dir()),
                          DEST.replace("/Game/", "", 1))
    for name in (RIG_NAME, RTG_NAME) + tuple(n for n, _ in GRAPHS):
        f = os.path.join(folder, name + ".uasset")
        if os.path.isfile(f):
            os.remove(f)
    unreal.AssetRegistryHelpers.get_asset_registry().scan_paths_synchronous([DEST], True)


def make_graphs(unreal, lib, at):
    """The two motion-matching graphs; one key per graph, then the wiring's own line."""
    mannequin = lib.load_asset(MANNEQUIN)
    if mannequin is None:
        return "tomMotionGraph=NO-MANNEQUIN"
    skeleton = mannequin.get_editor_property("skeleton")
    parent = getattr(unreal, "LedgerMotionMatchAnim", None)
    tools = getattr(unreal, "LedgerMotionMatchTools", None)
    if skeleton is None or parent is None or tools is None:
        return "tomMotionGraph=NO-TOOL skeleton=%s parent=%s tools=%s" % (skeleton is not None, parent is not None, tools is not None)
    out = []
    for name, offset in GRAPHS:
        f = unreal.AnimBlueprintFactory()
        f.set_editor_property("target_skeleton", skeleton)
        f.set_editor_property("parent_class", parent)
        f.set_editor_property("preview_skeletal_mesh", mannequin)
        abp = at.create_asset(name, DEST, unreal.AnimBlueprint, f)
        if abp is None:
            out.append("%s=NOT-MADE" % name)
            continue
        wired = tools.wire_motion_match_blueprint(abp, offset)
        lib.save_loaded_asset(abp)
        out.append("%s:%s" % (name, wired.replace(" ", ",")))
    return "tomMotionGraph=" + ";".join(out)


def selftest():
    ok = all(p.startswith("/Game/") for p in (TOM_MESH, SOURCE_RIG, DEST, MANNEQUIN)) and RTG_NAME.startswith("RTG_") and RIG_NAME.startswith("IK_") \
        and all(n.startswith("ABP_") for n, _ in GRAPHS) and [o for _, o in GRAPHS] == [True, False]
    print("make_tom_retarget selftest: passed=%d/1 failed=%d" % (1 if ok else 0, 0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
