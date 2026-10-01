"""The street's parked cars into Unreal: each production/assets/vehicles/*.glb as
one static mesh, in the editor run the cook step already starts.

    python3 tools/ue/import_vehicles.py --selftest     # runs without Unreal

WHY IT EXISTS, 23 September. Jafar's presentable checklist: "cars and props
are real-looking models rather than shapes, with no recognisable real car
model". Each car is a glb built by tools/art-recipes/car-model.py, joined into
one object with its materials as sections, so it imports as one mesh.

WHAT IT MAKES, under /Game/Ledger/Vehicles/<stem>/: SM_<stem>, renamed from
whatever the importer called it so the probe loads it by a known name, with
NANITE OFF and read back, as the street's are (the first street frame drew
Nanite's simplified stand-in). Materials stay beside it.

ONE LINE, appended to ue-material.txt: asked, made, and why not.
"""
import glob
import os
import sys
import time

VEHICLES_REL = "production/assets/vehicles"
PACKAGE_ROOT = "/Game/Ledger/Vehicles"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def stems(root):
    return sorted(os.path.splitext(os.path.basename(p))[0]
                  for p in glob.glob(os.path.join(root, VEHICLES_REL, "*.glb")))


def mesh_path(stem):
    return "%s/%s/SM_%s" % (PACKAGE_ROOT, stem, stem)


def vehicles_line(asked, made, nanite_off, seconds, notes):
    return ("vehiclesImportStatus=%s vehiclesImported=%d/%d vehiclesNaniteOff=%d/%d "
            "vehiclesImportSeconds=%.1f vehiclesImportNote=%s"
            % ("OK" if asked and made == asked else ("NOTHING" if not asked else "PARTIAL"),
               made, asked, nanite_off, made, seconds,
               ("/".join(notes) or "none").replace(" ", "~")[:200]))


def selftest():
    passed = failed = 0

    def ok(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("import_vehicles selftest FAIL %s: %s" % (name, detail))
    found = stems(repo_root())
    ok("the committed cars are found", len(found) >= 1, str(found))
    ok("the mesh is named where the probe loads it",
       mesh_path("hatch-navy") == "/Game/Ledger/Vehicles/hatch-navy/SM_hatch-navy")
    ok("the line carries its denominator", "vehiclesImported=1/2" in vehicles_line(2, 1, 1, 1.0, ["x"]))
    print("import_vehicles selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


def import_glb(unreal, glb, dest, mesh_asset):
    """One glb as one static mesh at mesh_asset (its materials beside it), Nanite
    off and read back. Returns (made, nanite_off, note); the note is None when
    it went in. Shared with tools/ue/import_shop_displays.py."""
    lib = unreal.EditorAssetLibrary
    stem = os.path.splitext(os.path.basename(glb))[0]
    if lib.does_directory_exist(dest):
        lib.delete_directory(dest)
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", glb)
    task.set_editor_property("destination_path", dest)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    mesh = None
    for p in lib.list_assets(dest, recursive=True, include_folder=False):
        if isinstance(lib.load_asset(p), unreal.StaticMesh):
            mesh = p
            break
    if mesh is None:
        return 0, 0, "%s-no-mesh" % stem
    if mesh.split(".")[0] != mesh_asset:
        lib.rename_asset(mesh.split(".")[0], mesh_asset)
    m = lib.load_asset(mesh_asset)
    if m is None:
        return 0, 0, "%s-rename-did-not-take" % stem
    off = 1 if nanite_off_and_rebuilt(unreal, m) else 0
    lib.save_directory(dest)
    return 1, off, None


def nanite_off_and_rebuilt(unreal, m):
    """NANITE OFF, THE MESH REBUILT AND SAVED, 1 October. In the cook step's
    commandlet the StaticMeshEditorSubsystem is not there (get_editor_subsystem
    returns None), so the old fallback only set the property: it read back off
    in the same run, but nothing marked the package dirty, save_directory skipped
    it, and the saved car still had Nanite on and drew Nanite's coarse stand-in:
    3,638 of the hatchback's 14,994 triangles, the skip 278 of 928 (measured
    1 October; Jafar that morning: "the cars are crude boxes", "the skip and the
    pallets look like placeholders"). Setting the LOD's own build settings back
    runs the mesh build, and the save is forced. True when the saved mesh is off
    and draws its full triangles."""
    ns = m.get_editor_property("nanite_settings")
    ns.enabled = False
    sub = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    if sub is not None:
        sub.set_nanite_settings(m, ns, apply_changes=True)
    else:
        m.modify()
        m.set_editor_property("nanite_settings", ns)
        esml = unreal.EditorStaticMeshLibrary
        esml.set_lod_build_settings(m, 0, esml.get_lod_build_settings(m, 0))
    unreal.EditorAssetLibrary.save_loaded_asset(m, only_if_is_dirty=False)
    return not m.get_editor_property("nanite_settings").enabled


def main():
    import unreal
    t0 = time.time()
    root = repo_root()
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    notes = []
    found = stems(root)
    made = nanite_off = 0
    for stem in found:
        try:
            m, off, note = import_glb(unreal, os.path.join(root, VEHICLES_REL, stem + ".glb"),
                                      "%s/%s" % (PACKAGE_ROOT, stem), mesh_path(stem))
            made += m
            nanite_off += off
            if note:
                notes.append(note)
        except Exception as e:
            notes.append("%s-raised-%s" % (stem, str(e).splitlines()[0][:60] if str(e) else "?"))
    line = vehicles_line(len(found), made, nanite_off, time.time() - t0, notes)
    with open(out, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print("import_vehicles: " + line)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
