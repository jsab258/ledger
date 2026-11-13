"""Seamshift round 2 (advisor 119/120): its refitted jumpers into Unreal, scratch only.

    set LEDGER_MH_SCRIPT=seamshift_scratch_import
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -unattended

WHY, 13 November 2026. Round 1 (production/research/tool-tests-2026-11/SEAMSHIFT-ROUND1-2026-11-12.md)
checked the refits outside Unreal only; its point 7 left the import, the skeleton match and the
90-degree turn its own notes report for Darren to round 2. This imports each refitted jumper_skinned.fbx
onto its wearer's body skeleton under /Game/Scratch/Seamshift (never the game's Garments folder),
then, with a garment and its body each spawned at the origin in the unsaved level, compares every
shared bone's reference-pose position (the bind pose) and the two meshes' bounds (a turn shows as the
width and depth swapped or the centre off the body). Writes seamshift-scratch.txt beside the project.
The scratch folder is deleted at the end, so nothing stays in the project.
"""
import os
import time

SRC = "F:/LedgerTools/tool-tests-2026-11/seamshift-r1/out/tom-jumper-to-cast"
WEARERS = {"Sheila": "MH_LenaS4", "Ron": "MH_RoccoP2", "Darren": "MH_SamS6"}
DEST = "/Game/Scratch/Seamshift"


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "seamshift-scratch.txt")

    def bones(mesh):
        a = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0, 0, 0))
        c = a.get_editor_property("skeletal_mesh_component")
        c.set_skinned_asset_and_update(mesh) if hasattr(c, "set_skinned_asset_and_update") else c.set_skeletal_mesh(mesh)
        res = {}
        for i in range(c.get_num_bones()):
            n = c.get_bone_name(i)
            res[str(n)] = c.get_socket_location(n)
        unreal.EditorLevelLibrary.destroy_actor(a)
        return res

    def size(mesh):
        b = mesh.get_bounds()
        return ([round(2 * x, 1) for x in (b.box_extent.x, b.box_extent.y, b.box_extent.z)],
                [round(x, 1) for x in (b.origin.x, b.origin.y, b.origin.z)])

    def one(who, mh, lines):
        fbx = "%s/%s/jumper_skinned.fbx" % (SRC, who)
        body = unreal.load_asset("/Game/Ledger/MetaHumans/%s/Body/SKM_%s_BodyMesh" % (mh, mh))
        skel = body.get_editor_property("skeleton") if body else None
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_mesh", True)
        ui.set_editor_property("import_as_skeletal", True)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
        ui.set_editor_property("import_materials", False)
        ui.set_editor_property("import_textures", False)
        ui.set_editor_property("import_animations", False)
        ui.set_editor_property("create_physics_asset", False)
        if skel is not None:
            ui.set_editor_property("skeleton", skel)
        sk = ui.get_editor_property("skeletal_mesh_import_data")
        sk.set_editor_property("import_morph_targets", False)
        sk.set_editor_property("convert_scene", True)
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", fbx)
        task.set_editor_property("destination_path", DEST + "/" + who)
        task.set_editor_property("destination_name", "SKM_Jumper_" + who)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", False)
        task.set_editor_property("options", ui)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        mesh = unreal.load_asset("%s/%s/SKM_Jumper_%s" % (DEST, who, who))
        lines.append("%s (%s) from %s" % (who, mh, fbx))
        if mesh is None:
            lines.append("  IMPORT FAILED: no mesh made (bone names or hierarchy refused by the body skeleton?)")
            return
        ms = mesh.get_editor_property("skeleton")
        lines.append("  skeleton: %s; body's %s; same=%s" % (
            ms.get_path_name() if ms else "none", skel.get_path_name() if skel else "none",
            bool(ms and skel and ms.get_path_name() == skel.get_path_name())))
        gs, gc = size(mesh)
        bs, bc = size(body)
        lines.append("  garment size cm %s centre %s; body size %s centre %s" % (gs, gc, bs, bc))
        lines.append("  turn check: garment wider (x) than deep (y)=%s, body=%s" % (gs[0] > gs[1], bs[0] > bs[1]))
        gb, bb = bones(mesh), bones(body)
        shared = [n for n in gb if n in bb]
        missing = [n for n in gb if n not in bb]
        lines.append("  bones: garment %d, body %d, shared %d, garment-only %s" % (len(gb), len(bb), len(shared), missing[:10]))
        d = sorted(((gb[n] - bb[n]).length(), n) for n in shared)
        if d:
            over = [n for x, n in d if x > 0.1]
            lines.append("  bind pose: worst %.3f cm at %s; median %.3f cm; bones over 0.1 cm: %d %s" % (
                d[-1][0], d[-1][1], d[len(d) // 2][0], len(over), over[:8]))

    def run():
        lines = []
        for who, mh in WEARERS.items():
            try:
                one(who, mh, lines)
            except Exception as e:
                lines.append("%s RAISED %r" % (who, e))
        try:
            unreal.EditorAssetLibrary.delete_directory(DEST)
            lines.append("scratch folder deleted: %s" % (not unreal.EditorAssetLibrary.does_directory_exist(DEST)))
        except Exception as e:
            lines.append("scratch delete RAISED %r" % e)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("RAISED %r\n" % e)
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
