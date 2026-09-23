"""The street's people into Unreal: each production/assets/people/*.glb as a
skeletal mesh and its looping animation, in the editor run the cook step
already starts.

    python3 tools/ue/import_people.py --selftest     # runs without Unreal

WHY IT EXISTS, 23 September. Jafar's presentable checklist: "a handful of
people stand or walk in the street, even if they only idle". Each person is a
glb made by tools/art-recipes/person-export.py - a Mixamo body with one clip,
the bone names put right and the loop trimmed in Blender - so this imports
files that are already correct, the way tools/ue/import_street.py imports the
street.

WHAT IT MAKES, under /Game/Ledger/People/<stem>/ (DefaultGame.ini already
cooks /Game/Ledger): SK_<stem>, the skeletal mesh, and A_<stem>, its
animation, renamed from whatever the importer called them so the probe loads
them by a name it can know. Whatever else the importer makes (the skeleton,
the physics asset, materials, textures) stays beside them.

ONE LINE, appended to ue-material.txt as the street's is: how many people
were asked, how many came back with both a mesh and an animation, and why
not for any that did not.
"""
import glob
import os
import sys
import time

PEOPLE_REL = "production/assets/people"
PACKAGE_ROOT = "/Game/Ledger/People"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def stems(root):
    return sorted(os.path.splitext(os.path.basename(p))[0]
                  for p in glob.glob(os.path.join(root, PEOPLE_REL, "*.glb")))


def mesh_path(stem):
    return "%s/%s/SK_%s" % (PACKAGE_ROOT, stem, stem)


def anim_path(stem):
    return "%s/%s/A_%s" % (PACKAGE_ROOT, stem, stem)


def people_line(asked, made, seconds, notes, sizes=None):
    # peopleSizes, 23 September: each person's height in centimetres as the
    # imported mesh has it, and how many skeletal meshes the importer made of
    # the file. Five people imported "5/5" and stood nowhere to be seen, and
    # the line could not say whether they were 2 cm tall or a belt apiece.
    return ("peopleImportStatus=%s peopleImported=%d/%d peopleImportSeconds=%.1f peopleImportNote=%s"
            " peopleSizes=%s"
            % ("OK" if asked and made == asked else ("NOTHING" if not asked else "PARTIAL"),
               made, asked, seconds, ("/".join(notes) or "none").replace(" ", "~")[:200],
               ("/".join(sizes or []) or "none").replace(" ", "~")[:300]))


def selftest():
    passed = failed = 0

    def ok(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("import_people selftest FAIL %s: %s" % (name, detail))
    root = repo_root()
    found = stems(root)
    ok("the committed people are found", len(found) >= 3, str(found))
    ok("the mesh is named where the probe loads it",
       mesh_path("joe-pockets") == "/Game/Ledger/People/joe-pockets/SK_joe-pockets")
    ok("and the animation", anim_path("joe-pockets") == "/Game/Ledger/People/joe-pockets/A_joe-pockets")
    ok("the line carries its denominator", "peopleImported=4/5" in people_line(5, 4, 1.0, ["x"]))
    ok("nothing asked says NOTHING, not OK", people_line(0, 0, 0.0, []).startswith("peopleImportStatus=NOTHING"))
    ok("the sizes ride the line", "peopleSizes=joe:178cm:1mesh" in people_line(1, 1, 1.0, [], ["joe:178cm:1mesh"]))
    print("import_people selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


def main():
    import unreal
    t0 = time.time()
    root = repo_root()
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    lib = unreal.EditorAssetLibrary
    notes = []
    found = stems(root)
    made = 0
    sizes = []
    for stem in found:
        dest = "%s/%s" % (PACKAGE_ROOT, stem)
        try:
            # CLEARED FIRST, as the street's folder is: nothing from an older
            # run may be cooked as if it were current.
            if lib.does_directory_exist(dest):
                lib.delete_directory(dest)
            task = unreal.AssetImportTask()
            task.set_editor_property("filename", os.path.join(root, PEOPLE_REL, stem + ".glb"))
            task.set_editor_property("destination_path", dest)
            task.set_editor_property("automated", True)
            task.set_editor_property("replace_existing", True)
            task.set_editor_property("save", True)
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
            mesh = anim = None
            meshes = 0
            tall = -1.0
            for p in lib.list_assets(dest, recursive=True, include_folder=False):
                a = lib.load_asset(p)
                if isinstance(a, unreal.SkeletalMesh):
                    meshes += 1
                    try:
                        ext = a.get_bounds().box_extent
                        tall = max(tall, 2.0 * float(ext.z))
                    except Exception:
                        pass
                if isinstance(a, unreal.SkeletalMesh) and mesh is None:
                    mesh = p
                elif isinstance(a, unreal.AnimSequence):
                    # THE LONGEST, if the importer made more than one: the
                    # loop is the clip; a one-frame pose is not.
                    if anim is None or a.get_play_length() > lib.load_asset(anim).get_play_length():
                        anim = p
            sizes.append("%s:%dcm:%dmesh" % (stem.split("-")[0], int(round(tall)), meshes))
            if mesh is None or anim is None:
                notes.append("%s-%s" % (stem, "no-mesh" if mesh is None else "no-anim"))
                continue
            if mesh.split(".")[0] != mesh_path(stem):
                lib.rename_asset(mesh.split(".")[0], mesh_path(stem))
            if anim.split(".")[0] != anim_path(stem):
                lib.rename_asset(anim.split(".")[0], anim_path(stem))
            if lib.does_asset_exist(mesh_path(stem)) and lib.does_asset_exist(anim_path(stem)):
                lib.save_directory(dest)
                made += 1
            else:
                notes.append("%s-rename-did-not-take" % stem)
        except Exception as e:
            notes.append("%s-raised-%s" % (stem, str(e).splitlines()[0][:60] if str(e) else "?"))
    line = people_line(len(found), made, time.time() - t0, notes, sizes)
    with open(out, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print("import_people: " + line)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
