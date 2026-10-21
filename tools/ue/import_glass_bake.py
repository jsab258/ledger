"""The shop glass's baked street into Unreal: each window's day and night cube, made by
tools/glass_bake.py, as a compressed cube the game only looks up.

    python tools/ue/import_glass_bake.py --selftest     # runs without Unreal

WHY IT EXISTS, 21 October 2026 (his order, item 6: the packaged build's worst frame at or under
33.3 ms on the walk). Research note production/cloud-week/research/1d-shop-glass-without-frame-cost.md
found the slow frames were the game re-photographing every shop window's six-sided picture of the
street with full Lumen at load and at each change of light, and recommended what shipped games do
(route A): take each picture once per light at build time and only look it up in play.

WHAT IT MAKES, under /Game/Ledger/GlassBake/<light>/: TC_<mesh> for every <mesh>.hdr under
F:/LedgerTools/game-inputs/glass-bake/<light>/ (a long-lat picture 2N x N, which the engine takes
back as an N cube: TextureBuildUtilities.cpp ComputeLongLatCubemapExtents), HDR compressed (BC6H),
mips from the texture group, never streamed. The game finds them by name (VignetteShot.cpp
LoadGlassBake); a window with no cube for both lights is caught live, as before.

THE STAMP (the note's step 4: "a stale bake cannot ship"): the bake's manifest.json holds the sha256
of the files the street was built from; if any differs from the checkout now, nothing is imported
and the folder is emptied, so every window is caught live (right to look at, its slow frames back),
and the status line says STALE with the files that changed. Re-bake: python tools/glass_bake.py.

ONE LINE, appended to ue-material.txt.
"""
import glob
import hashlib
import json
import os
import sys
import time

BAKE_ROOT = os.environ.get("LEDGER_GLASS_BAKE", r"F:\LedgerTools\game-inputs\glass-bake")
PACKAGE = "/Game/Ledger/GlassBake"
LIGHTS = ("day", "night")
# What the street in the glass is made from: the street's export, its look, the shops behind its
# glass and the scene's placed pieces (lamps, people's places, props).
STAMPED = [
    "production/assets/street/quay-street.json",
    "production/specs/unreal-look.json",
    "production/specs/shop-interiors.json",
    "production/specs/vignette-scene.json",
]


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def stamp(root, files=STAMPED):
    out = {}
    for rel in files:
        p = os.path.join(root, rel)
        if os.path.isfile(p):
            # LINE ENDINGS IGNORED (21 October: the build machine's checkout keeps CRLF where this PC's
            # working copy keeps LF, and its first import called a fresh bake STALE on that alone)
            with open(p, "rb") as f:
                out[rel] = hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()
        else:
            out[rel] = None
    return out


def changed(made, now):
    """The stamped files whose hash differs between the bake and the checkout now."""
    return sorted(k for k in set(made) | set(now) if made.get(k) != now.get(k))


def asset_name(mesh):
    return "TC_" + mesh


def status_line(status, made, asked, seconds, notes):
    return ("glassBakeStatus=%s glassBakeImported=%d/%d glassBakeSeconds=%.1f glassBakeNote=%s"
            % (status, made, asked, seconds, ("/".join(notes) or "none").replace(" ", "~")[:220]))


def main():
    import unreal
    t0 = time.time()
    root = repo_root()
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    lib = unreal.EditorAssetLibrary
    notes = []
    man_path = os.path.join(BAKE_ROOT, "manifest.json")
    hdrs = {light: sorted(glob.glob(os.path.join(BAKE_ROOT, light, "*.hdr"))) for light in LIGHTS}
    asked = sum(len(v) for v in hdrs.values())
    made = 0
    if not os.path.isfile(man_path) or asked == 0:
        status = "NOBAKE"
        notes.append("no-bake-in-%s" % BAKE_ROOT)
    else:
        man = json.load(open(man_path, encoding="utf-8"))
        diff = changed(man.get("stamp", {}), stamp(root))
        if diff:
            status = "STALE"
            notes.append("changed:" + ",".join(os.path.basename(d) for d in diff))
            if lib.does_directory_exist(PACKAGE):
                lib.delete_directory(PACKAGE)
        else:
            tools = unreal.AssetToolsHelpers.get_asset_tools()
            for light in LIGHTS:
                dest = "%s/%s" % (PACKAGE, light)
                if lib.does_directory_exist(dest):
                    lib.delete_directory(dest)
                for hdr in hdrs[light]:
                    mesh = os.path.splitext(os.path.basename(hdr))[0]
                    task = unreal.AssetImportTask()
                    task.set_editor_property("filename", hdr)
                    task.set_editor_property("destination_path", dest)
                    task.set_editor_property("destination_name", asset_name(mesh))
                    task.set_editor_property("automated", True)
                    task.set_editor_property("replace_existing", True)
                    task.set_editor_property("save", True)
                    tools.import_asset_tasks([task])
                    path = "%s/%s" % (dest, asset_name(mesh))
                    tex = lib.load_asset(path)
                    if not isinstance(tex, unreal.TextureCube):
                        notes.append("%s/%s-not-a-cube(%s)" % (light, mesh, type(tex).__name__))
                        continue
                    tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_HDR_COMPRESSED)
                    tex.set_editor_property("srgb", False)
                    tex.set_editor_property("never_stream", True)
                    tex.set_editor_property("mip_gen_settings", unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP)
                    lib.save_loaded_asset(tex, only_if_is_dirty=False)
                    made += 1
            status = "OK" if made == asked else "PARTIAL"
    line = status_line(status, made, asked, time.time() - t0, notes)
    with open(out, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print("import_glass_bake: " + line)
    return 0


def selftest():
    import tempfile
    passed = failed = 0

    def ok(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("import_glass_bake selftest FAIL " + name)
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "production", "specs"))
    p = os.path.join(d, "production", "specs", "unreal-look.json")
    open(p, "w").write("{}")
    a = stamp(d, ["production/specs/unreal-look.json", "production/specs/missing.json"])
    ok("a missing file stamps as None", a["production/specs/missing.json"] is None)
    ok("an unchanged street is not stale", changed(a, stamp(d, list(a))) == [])
    open(p, "w").write('{"glass": 1}')
    ok("a changed look is stale, by name", changed(a, stamp(d, list(a))) == ["production/specs/unreal-look.json"])
    open(p, "wb").write(b'{\r\n "glass": 1\r\n}\r\n')
    crlf = stamp(d, list(a))
    open(p, "wb").write(b'{\n "glass": 1\n}\n')
    ok("line endings alone do not make a bake stale", changed(crlf, stamp(d, list(a))) == [])
    ok("the asset is named as the game looks it up", asset_name("street_glass_eg_bay2") == "TC_street_glass_eg_bay2")
    ok("the stamp covers the street's export and look", all(f in STAMPED for f in
       ("production/assets/street/quay-street.json", "production/specs/unreal-look.json")))
    src = open(os.path.join(repo_root(), "ue-probe", "Source", "LedgerProbe", "Private", "VignetteShot.cpp"), encoding="utf-8").read()
    ok("the game looks under the same package", "/Game/Ledger/GlassBake/%s/TC_%s.TC_%s" in src and PACKAGE == "/Game/Ledger/GlassBake")
    print("import_glass_bake selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
