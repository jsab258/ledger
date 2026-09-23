"""Assemble a MetaHuman Character into a usable character, in the editor, with no hands.

    UnrealEditor-Cmd.exe ue-probe/LedgerProbe.uproject -run=pythonscript \
        -script="tools/ue/assemble_metahuman.py" -unattended -nosplash
    python3 tools/ue/assemble_metahuman.py --selftest     # runs without Unreal

WHY IT EXISTS, 24 September. Jafar's order for the PS5 corner: "one MetaHuman
standing in it", and tonight "assemble MH_Test into a usable character ... if
you can do it without my hands". He made MH_Test in MetaHuman Creator and had
it rigged by Epic's service (it needs his Epic sign-in, which is done). What
the Creator's Assembly button does is script-callable on the editor subsystem
the plugin ships: open the character for edit, build it with the Optimized
pipeline into a folder of ordinary assets (skeletal meshes, materials,
grooms) that a packaged game can draw, then close it. This does exactly that.

MEMORY FIRST: MetaHuman Creator asks for 10 GB free to open a rigged face, and
another session on this PC may hold several. The script refuses below 10 GB
rather than risk the editor, and says so.

ONE LINE, appended to ue-material.txt in the project folder: asked, built,
where, and why not.
"""
import os
import sys
import time

CHARACTER = "/Game/MH_Test"
BUILD_ROOT = "/Game/Ledger/MetaHumans"
NEED_FREE_GB = 10.0


def free_gb():
    """Free physical memory in GB, or None if it cannot be read."""
    try:
        import ctypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        m = MEMORYSTATUSEX()
        m.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            return None
        return m.ullAvailPhys / (1024.0 ** 3)
    except Exception:
        return None


def line(status, built, where, seconds, note):
    return ("metahumanStatus=%s metahumanBuilt=%s metahumanWhere=%s metahumanSeconds=%.1f metahumanNote=%s"
            % (status, built, where, seconds, (note or "none").replace(" ", "~")[:200]))


def selftest():
    ok = 0
    bad = 0
    f = free_gb()
    if f is None or f > 0:
        ok += 1
    else:
        bad += 1
        print("assemble_metahuman selftest FAIL free memory read as %r" % f)
    s = line("REFUSED", "no", "none", 0.0, "free 6.8 GB under 10")
    if "metahumanNote=free~6.8~GB~under~10" in s:
        ok += 1
    else:
        bad += 1
        print("assemble_metahuman selftest FAIL line: " + s)
    print("assemble_metahuman selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main():
    import unreal
    t0 = time.time()
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")

    def write(l):
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(l + "\n")
        print("assemble_metahuman: " + l)

    f = free_gb()
    if f is not None and f < NEED_FREE_GB:
        write(line("REFUSED", "no", "none", time.time() - t0, "free %.1f GB under %.0f" % (f, NEED_FREE_GB)))
        return
    ch = unreal.load_asset(CHARACTER)
    if ch is None:
        write(line("NO-CHARACTER", "no", "none", time.time() - t0, CHARACTER + " did not load"))
        return
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    if sub is None:
        write(line("NO-SUBSYSTEM", "no", "none", time.time() - t0, "MetaHuman Creator plugin not loaded"))
        return
    if not sub.try_add_object_to_edit(ch):
        write(line("NOT-EDITABLE", "no", "none", time.time() - t0, "try_add_object_to_edit refused"))
        return
    try:
        if not sub.can_build_meta_human(ch, True):
            write(line("CANNOT-BUILD", "no", "none", time.time() - t0, "can_build_meta_human said no; see the log"))
            return
        p = unreal.MetaHumanCharacterEditorBuildParameters()
        p.set_editor_property("pipeline_type", unreal.MetaHumanDefaultPipelineType.OPTIMIZED)
        p.set_editor_property("pipeline_quality", unreal.MetaHumanQualityLevel.HIGH)
        p.set_editor_property("absolute_build_path", BUILD_ROOT)
        sub.build_meta_human(ch, p)
        unreal.EditorAssetLibrary.save_directory(BUILD_ROOT, only_if_is_dirty=False, recursive=True)
        made = unreal.EditorAssetLibrary.list_assets(BUILD_ROOT, recursive=True, include_folder=False)
        write(line("BUILT" if made else "BUILT-NOTHING", "%d-assets" % len(made), BUILD_ROOT,
                   time.time() - t0, "optimized-high"))
    finally:
        sub.remove_object_to_edit(ch)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
