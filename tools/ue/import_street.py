"""Import the street's geometry from Blender into Unreal static meshes, in CI.

    Called from tools/ue/make_base_material.py main(), in the editor run the
    probe step already starts, exactly as tools/ue/import_figure.py is.
    python tools/ue/import_street.py --selftest    # runs without Unreal

THE CROSSING, 23 September. Jafar's ruling of the morning: Blender is for
shapes and layout, all look-development happens in Unreal against the sheet,
and the mirror is fixed once where Blender work crosses into Unreal.
tools/art-recipes/terrace-front.py --export-glb writes
production/assets/street/quay-street.glb, already reflected the right way
round, and quay-street.json beside it. This makes the GLB into static meshes
under /Game/Ledger/Street, which DefaultGame.ini already cooks with the rest
of /Game/Ledger, and the probe's VignetteShot places them.

WHERE THEY LAND WAS MEASURED, NOT ASSUMED: a throwaway import on UE 5.8 on 23
September put all 52 meshes at /Game/Ledger/Street/quay-street/StaticMeshes/
<mesh name>, and Mickey's sign at (600, 500, 322) uu - x along the street, the
east side at +Y, which is the right-hand side looking north. This script reads
the sign back on every run and says so, so an importer that one day turns the
file round goes red on the line rather than in a picture.

IT CANNOT TAKE THE MATERIAL RUN DOWN. It writes one key=value line to
ue-material.txt, which the step already reads whole, and its caller catches
anything it raises.
"""
import json
import os
import sys
import time

GLB_REL = "production/assets/street/quay-street.glb"
SIDECAR_REL = "production/assets/street/quay-street.json"
PACKAGE_ROOT = "/Game/Ledger/Street"
PACKAGE_DIR = PACKAGE_ROOT + "/quay-street/StaticMeshes"

#: THE SIGN READ BACK, in uu, and how far it may be from where the export put
#: it. The export's own bounds for the sign are x 3.2..8.8, the east frontage
#: at 5.0, z 3.0..3.5 in metres; 5 cm is a real move, not rounding.
SIGN_MESH = "street_sign_fascia_mickeys_plain"
SIGN_WANT_UU = (600.0, 500.0, 322.0)
SIGN_TOLERANCE_UU = 5.0


def repo_root():
    # A THROWAWAY PROJECT OUTSIDE THE CHECKOUT names the checkout here; the
    # probe project sits inside it and never needs to.
    if os.environ.get("LEDGER_REPO_ROOT"):
        return os.environ["LEDGER_REPO_ROOT"]
    try:
        import unreal
        return os.path.abspath(os.path.join(unreal.Paths.project_dir(), ".."))
    except Exception:
        return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def object_path(mesh):
    return "%s/%s.%s" % (PACKAGE_DIR, mesh, mesh)


def mesh_names(sidecar):
    return [m.get("mesh") for m in sidecar.get("meshes", []) if m.get("mesh")]


def sign_verdict(origin_uu):
    """AGREES, or MOVED with the distance, or NOT-READ."""
    if origin_uu is None:
        return "NOT-READ"
    d = sum((a - b) ** 2 for a, b in zip(origin_uu, SIGN_WANT_UU)) ** 0.5
    return "AGREES" if d <= SIGN_TOLERANCE_UU else "MOVED/%.0fuu" % d


def street_line(status, asked, found, sign, seconds, note):
    return ("streetImportStatus=%s streetImportMeshes=%d/%d streetImportSign=%s "
            "streetImportSeconds=%.1f streetImportNote=%s"
            % (status, found, asked, sign, seconds, (note or "none").replace(" ", "~")[:160]))


def selftest():
    passed = failed = 0

    def ok(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("FAILED - %s : %s" % (name, detail))

    root = repo_root()
    with open(os.path.join(root, SIDECAR_REL), encoding="utf-8") as fh:
        side = json.load(fh)
    names = mesh_names(side)
    ok("the sidecar names the meshes", len(names) >= 40, len(names))
    ok("the sign this script reads back is one of them", SIGN_MESH in names, names[:5])
    ok("every name is one Unreal can make an asset of",
       all(n.replace("_", "").isalnum() and len(n) <= 60 for n in names))
    ok("the GLB is beside it", os.path.getsize(os.path.join(root, GLB_REL)) > 100000)
    ok("the object path is the measured one",
       object_path("street_slate") == "/Game/Ledger/Street/quay-street/StaticMeshes/street_slate.street_slate")
    ok("the sign where the export put it AGREES", sign_verdict((600.0, 500.0, 322.0)) == "AGREES")
    ok("the sign on the other side of the street is MOVED",
       sign_verdict((600.0, -500.0, 322.0)).startswith("MOVED/"), sign_verdict((600.0, -500.0, 322.0)))
    ok("a sign never read says so", sign_verdict(None) == "NOT-READ")
    ok("the line carries its denominator",
       "streetImportMeshes=52/52" in street_line("OK", 52, 52, "AGREES", 1.0, ""))
    print("import_street selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


def _complex_as_simple(unreal, mesh):
    """Collide with the mesh's own triangles, 23 September, and say whether
    it READ BACK. The street is exported one mesh per material across the
    whole street, so a simple collision - a box or hull round each mesh -
    would be one shape the size of the town. The crime's sight lines are
    simple-collision traces, and complex-as-simple is what lets them, and a
    walking pawn, meet these meshes' real faces. Whether the game uses it is
    the look file's street_collision; this only makes it possible."""
    bs = mesh.get_editor_property("body_setup")
    if bs is None:
        return False
    want = unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE
    bs.set_editor_property("collision_trace_flag", want)
    return bs.get_editor_property("collision_trace_flag") == want


def _nanite_off(unreal, sub, mesh):
    """Switch Nanite off on one mesh and say whether it READ BACK off."""
    ns = mesh.get_editor_property("nanite_settings")
    ns.enabled = False
    try:
        sub.set_nanite_settings(mesh, ns, apply_changes=True)
    except Exception:
        mesh.set_editor_property("nanite_settings", ns)
    return not mesh.get_editor_property("nanite_settings").enabled


def main():
    import unreal
    t0 = time.time()
    root = repo_root()
    glb = os.path.join(root, GLB_REL)
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    note = []
    asked = found = nanite_off = complex_ok = 0
    sign = "NOT-READ"
    status = "NOTHING"
    try:
        with open(os.path.join(root, SIDECAR_REL), encoding="utf-8") as fh:
            names = mesh_names(json.load(fh))
        asked = len(names)
        if not os.path.exists(glb):
            status = "NO-GLB"
        else:
            # CLEARED FIRST: a mesh the export no longer makes must not
            # survive from an older run and be cooked as if it were current.
            lib = unreal.EditorAssetLibrary
            if lib.does_directory_exist(PACKAGE_ROOT):
                lib.delete_directory(PACKAGE_ROOT)
            task = unreal.AssetImportTask()
            task.set_editor_property("filename", glb)
            task.set_editor_property("destination_path", PACKAGE_ROOT)
            task.set_editor_property("automated", True)
            task.set_editor_property("replace_existing", True)
            task.set_editor_property("save", True)
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
            sub = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
            for n in names:
                m = lib.load_asset(object_path(n)) if lib.does_asset_exist(object_path(n)) else None
                if m is None:
                    note.append("missing/" + n)
                    continue
                found += 1
                # NANITE OFF, 23 September, and read back. The importer turns
                # it on, and the first street frame drew the SIMPLIFIED
                # fallback it keeps beside a Nanite mesh (relative error 1.0):
                # big triangles across the windows, and the parade's brick
                # fronts dropped so the dark room boxes behind showed through.
                # These meshes are a few thousand faces each; the full mesh
                # is what should draw.
                if _nanite_off(unreal, sub, m):
                    nanite_off += 1
                try:
                    if _complex_as_simple(unreal, m):
                        complex_ok += 1
                except Exception as e:
                    note.append("complex/" + str(e).splitlines()[0][:60] if str(e) else "complex/raised")
                lib.save_asset(object_path(n), False)
                if n == SIGN_MESH:
                    b = m.get_bounds()
                    sign = sign_verdict((b.origin.x, b.origin.y, b.origin.z))
            status = ("OK" if found == asked and sign == "AGREES" and nanite_off == found
                      else "PARTIAL")
    except Exception as e:
        status = "RAISED"
        note.append(str(e).split("\n")[0][:100])
    line = street_line(status, asked, found, sign, time.time() - t0, "/".join(note[:3]))
    line += " streetImportNaniteOff=%d/%d" % (nanite_off, found)
    line += " streetImportComplexAsSimple=%d/%d" % (complex_ok, found)
    with open(out, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print("import_street: " + line)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
