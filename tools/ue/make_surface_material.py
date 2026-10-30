"""Make /Game/Ledger/M_LedgerSurface alone, with none of the steps make_base_material.py chains after it.

    UnrealEditor-Cmd ue-probe/LedgerProbe.uproject -run=pythonscript -script=C:/Users/Jafar/ledger-local/tools/ue/make_surface_material.py
    python tools/ue/make_surface_material.py --selftest    # runs without Unreal

WHY, 30 October 2026 (his order D11, the chandler's S3, the brick's streaks): run as a script, make_base_material.py builds
the surface material and then, in the same editor, the sky, the figure, the interior, glass, grime, wet and stain
decals, the ground's copy, the street's import, the walk clips and the sitting retarget, which a change to the surface
graph alone does not need and which touch assets other work is using. This builds the one material by the same
main() (reuse, not a copy of the graph), and writes its line to ue-material.txt as that script does. The ground's copy
(make_ground_material.py) keeps its own run.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_base_material as mbm  # noqa: E402


def selftest():
    ok = [not mbm.GROUND, mbm.ASSET_PATH == "/Game/Ledger/M_LedgerSurface", callable(mbm.main)]
    print("make_surface_material selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    # no sys.exit inside the editor (make_base_material.py's own rule); the verdict travels in ue-material.txt
    _code = mbm.main()
    if not mbm._inside_unreal():
        sys.exit(_code)
