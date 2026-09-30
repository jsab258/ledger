"""The clothing session's garments onto the cast, in the MetaHuman project.

    set LEDGER_MH_SCRIPT=import_garments
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -unattended
    python tools/ue/import_garments.py --selftest        # the list, without Unreal

WHY, 30 September. The clothing session (CLAUDE.md, three sessions) makes
each garment in Blender on the body the builder exported, skinned to that
body's own bones, and hands it over (NOW.md, Handovers); the builder fits
it in Unreal. production/specs/garments.json lists them. Each skinned FBX
becomes a skeletal mesh on its wearer's body skeleton, keeping the weights
it came with (the boots' README: re-transferring them would send the toe
box to the toe bones), at /Game/Ledger/MetaHumans/Garments/<Name>/SKM_<Name>.
That folder sits with the cast's MetaHumans, outside the public repository,
and the build machine mirrors it with them (ledger-probe-unreal.yml). The
game wears each by following the body's pose (LedgerGarments.h).

Writes import-garments.txt beside the project: each asset, its skeleton,
its size and its material slots.

LEDGER_GARMENTS=RonJacket,... imports only those. A garment's "materials"
maps its FBX slot names to material instances already in the project (the
bound jacket takes the donkey jacket's wool, yoke and buttons), set on the
mesh after the import.
"""
import json
import os
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = os.path.join(REPO, "production", "specs", "garments.json")
DEST = "/Game/Ledger/MetaHumans/Garments"
# Each wearer's approved MetaHuman, whose body the garments were made on
# (the face take changes the face, never the body: F:/LedgerTools/bodies/README.md).
BODY = {"Rocco": "MH_RoccoP2", "Lena": "MH_LenaS4", "Sam": "MH_SamC5"}


def garments(path=SPEC):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)["garments"]


def selftest():
    failed = 0
    g = garments()
    checks = [
        ("the list names garments", len(g) >= 1, str(len(g))),
        ("every wearer has an approved body", all(x["who"] in BODY for x in g), str([x["who"] for x in g])),
        ("every name is one word", all(x["name"].isalnum() for x in g), ""),
        ("every garment's file is where it says", all(os.path.isfile(x["fbx"]) for x in g) or not os.path.isdir("F:/LedgerTools"),
         str([x["fbx"] for x in g if not os.path.isfile(x["fbx"])])),
    ]
    for name, ok, detail in checks:
        if not ok:
            failed += 1
            print("import_garments selftest FAIL %s: %s" % (name, detail))
    print("import_garments selftest: passed=%d/%d failed=%d" % (len(checks) - failed, len(checks), failed))
    return 1 if failed else 0


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "import-garments.txt")

    def body_skeleton(who):
        mh = BODY[who]
        mesh = unreal.load_asset("/Game/Ledger/MetaHumans/%s/Body/SKM_%s_BodyMesh" % (mh, mh))
        return mesh.get_editor_property("skeleton") if mesh else None

    def one(g, lines):
        name = "SKM_" + g["name"]
        folder = DEST + "/" + g["name"]
        skel = body_skeleton(g["who"])
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_mesh", True)
        ui.set_editor_property("import_as_skeletal", True)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
        ui.set_editor_property("import_materials", True)
        ui.set_editor_property("import_textures", False)
        ui.set_editor_property("import_animations", False)
        ui.set_editor_property("create_physics_asset", False)
        if skel is not None:
            ui.set_editor_property("skeleton", skel)
        sk = ui.get_editor_property("skeletal_mesh_import_data")
        sk.set_editor_property("import_morph_targets", False)
        sk.set_editor_property("convert_scene", True)
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", g["fbx"])
        task.set_editor_property("destination_path", folder)
        task.set_editor_property("destination_name", name)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        task.set_editor_property("options", ui)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        mesh = unreal.load_asset(folder + "/" + name)
        if mesh is None:
            lines.append("MISSING %s/%s (from %s)" % (folder, name, g["fbx"]))
            return
        b = mesh.get_bounds()
        lines.append("%s: %s/%s" % (g["who"], folder, name))
        lines.append("  on the skeleton %s (the body's: %s)" % (
            mesh.get_editor_property("skeleton").get_path_name() if mesh.get_editor_property("skeleton") else "none",
            skel.get_path_name() if skel else "none"))
        lines.append("  size cm %s, centre %s" % ([round(2 * x, 1) for x in (b.box_extent.x, b.box_extent.y, b.box_extent.z)],
                                                 [round(x, 1) for x in (b.origin.x, b.origin.y, b.origin.z)]))
        lines.append("  material slots: %s" % [str(m.get_editor_property("material_slot_name")) for m in mesh.get_editor_property("materials")])
        mats = g.get("materials", {})
        if mats:
            slots = list(mesh.get_editor_property("materials"))
            for i, s in enumerate(slots):
                want = mats.get(str(s.get_editor_property("material_slot_name")))
                mi = unreal.load_asset(want) if want else None
                if mi is not None:
                    s.set_editor_property("material_interface", mi)
                    slots[i] = s
            mesh.set_editor_property("materials", slots)
            lines.append("  materials set: %s" % [str(s.get_editor_property("material_interface").get_name()) if s.get_editor_property("material_interface") else "none" for s in slots])
        unreal.EditorAssetLibrary.save_directory(folder)

    def run():
        lines = []
        only = [x for x in os.environ.get("LEDGER_GARMENTS", "").split(",") if x]
        for g in garments():
            if only and g["name"] not in only:
                continue
            try:
                one(g, lines)
            except Exception as e:
                lines.append("%s RAISED %r" % (g["name"], e))
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


if __name__ == "__main__" and "--selftest" in sys.argv:
    sys.exit(selftest())
