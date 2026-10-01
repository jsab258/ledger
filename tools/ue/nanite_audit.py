"""Every static mesh under /Game/Ledger with Nanite still on, listed, and with
--fix switched off, rebuilt and saved (import_vehicles.nanite_off_and_rebuilt).

    UnrealEditor-Cmd.exe <project> -run=pythonscript -script=tools/ue/nanite_audit.py -EnablePlugins=PythonScriptPlugin
    (set LEDGER_NANITE_FIX=1 to fix; the cook step runs it as a check)
    python tools/ue/nanite_audit.py --selftest     # runs without Unreal

WHY, 1 October. This game draws no Nanite: every mesh is meant to draw its full
triangles (the street's since 23 September). A mesh left with Nanite on draws
the coarse stand-in Nanite keeps beside it, and on 1 October twenty did: both
parked cars at a quarter of their triangles, and eighteen street props, the
skip at 278 of its 928 (the import's "off" had never been saved). Jafar had
called the cars crude boxes and the skip and pallets placeholders that morning.
This finds any such mesh, by count, so it cannot come back unseen.

ONE LINE, appended to ue-material.txt: naniteAuditOn=<n> naniteAuditFixed=<n> and the worst.
"""
import os
import sys

ROOTS = ("/Game/Ledger",)


def audit_line(on, fixed, worst):
    return "naniteAuditStatus=%s naniteAuditOn=%d naniteAuditFixed=%d naniteAuditWorst=%s" % (
        "CLEAN" if on == fixed else "NANITE-LEFT-ON", on, fixed,
        ("/".join("%s:%d/%d" % w for w in worst[:6]) or "none"))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("nanite_audit selftest FAIL " + name)
    check("clean when all fixed", audit_line(2, 2, []).startswith("naniteAuditStatus=CLEAN"))
    check("names what is left on", "NANITE-LEFT-ON" in audit_line(2, 0, [("SM_skip", 278, 928)]))
    check("gives drawn of full", "SM_skip:278/928" in audit_line(1, 0, [("SM_skip", 278, 928)]))
    print("nanite_audit selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main():
    import unreal
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import import_vehicles
    fix = os.environ.get("LEDGER_NANITE_FIX") == "1"
    lib = unreal.EditorAssetLibrary
    on = fixed = 0
    worst = []
    for root in ROOTS:
        for p in lib.list_assets(root, recursive=True, include_folder=False):
            a = lib.load_asset(p)
            if not isinstance(a, unreal.StaticMesh) or not a.get_editor_property("nanite_settings").enabled:
                continue
            on += 1
            name = p.split("/")[-1].split(".")[0]
            drawn, full = a.get_num_triangles(0), a.get_num_nanite_triangles()
            if fix and import_vehicles.nanite_off_and_rebuilt(unreal, a):
                fixed += 1
                unreal.log("nanite_audit: %s off, %d triangles drawn (was %d of %d)" % (name, a.get_num_triangles(0), drawn, full))
            else:
                worst.append((name, drawn, full))
    worst.sort(key=lambda w: w[2] - w[1], reverse=True)
    line = audit_line(on, fixed, worst)
    with open(os.path.join(unreal.Paths.project_dir(), "ue-material.txt"), "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    unreal.log("nanite_audit: " + line)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
