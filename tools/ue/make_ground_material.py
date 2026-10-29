"""Make /Game/Ledger/M_LedgerGround, the street ground's copy of M_LedgerSurface with its water as a clear coat.

    UnrealEditor-Cmd ue-probe/LedgerProbe.uproject -run=pythonscript -script=C:/Users/Jafar/ledger-local/tools/ue/make_ground_material.py
    python tools/ue/make_ground_material.py --selftest    # runs without Unreal

WHY, 29 October 2026 (his order D11, the look; production/research/street-wear/WET-GROUND-METHOD-2026-10-29.md, step 3
and "Step 3's build, planned"): wet ground is rough saturated stone with water over part of it, two lobes, where the
game's one material drew the road as one lobe of mixed roughness, which on real-albedo ground read as a milky sheet
and polished tile. The ground alone takes the coat (asphalt, flags, kerb), so the walls and fronts keep the cheaper
default-lit shading. The graph is make_base_material.py's own, built again under this name with its GROUND block on:
reuse, not a second copy of the graph.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_base_material as mbm  # noqa: E402

ASSET = "M_LedgerGround"


def configure():
    mbm.GROUND = True
    mbm.ASSET = ASSET
    mbm.ASSET_PATH = mbm.PACKAGE + "/" + ASSET
    return mbm


def selftest():
    m = configure()
    ok = [m.GROUND, m.ASSET_PATH == "/Game/Ledger/M_LedgerGround", 0.0 < m.GROUND_COAT_ROUGHNESS <= 0.05,
          "ground-water-to-coat" in open(m.__file__, encoding="utf-8").read()]
    print("make_ground_material selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    configure()
    # no sys.exit inside the editor (make_base_material.py's own rule: SystemExit through the embedded interpreter turns
    # a script that worked into a failing process); the verdict travels in ue-material.txt
    _code = mbm.main()
    if not mbm._inside_unreal():
        sys.exit(_code)
