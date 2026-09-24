#!/usr/bin/env python3
"""Put the files the game reads at run time inside the game, so a packaged copy needs no project folder.

    python tools/ue/stage_game_data.py            # copies into ue-probe/Content/LedgerData (gitignored)
    python tools/ue/stage_game_data.py --list     # prints what it would copy, copies nothing
    python tools/ue/stage_game_data.py --selftest

WHY, 24 September (overnight). The production pipeline audit: "the launcher
still requires checkout files". The packaged game found its street, its look,
its people, its sounds and its drawn textures only through the repository
(-LedgerRepo, or a checkout four folders up), because the game reads them at
run time from the repository's own paths. This copies exactly those files
into Content/LedgerData, keeping each one's repository path below it, and
DefaultGame.ini stages that folder beside the game's content as plain files
(DirectoriesToAlwaysStageAsNonUFS). The game looks there when no checkout
answers (VignetteShot.cpp FindStreetSidecar, FindSpec; CrimeProbe.cpp).

THE LIST IS COMPUTED, NOT KEPT: from the street's sidecar (its decals and
drawn maps), the piece list (its scanned surfaces) and the sound list (its
clips and ambience), the same way the game resolves them.
"""
import json
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEST = os.path.join(REPO, "ue-probe", "Content", "LedgerData")

FIXED = [
    "production/assets/street/quay-street.json",
    "production/specs/vignette-pieces.json",
    "production/specs/unreal-look.json",
    "production/specs/street-vehicles.json",
    "production/specs/street-people.json",
    "production/specs/street-sounds.json",
    "content/dialogue/crime-witness-v1.json",
]
DECAL_ROOT = "ledger/Assets/StreamingAssets/Decals"
# WHOLE FOLDERS TOO, 25 September: the sky photograph, the photographed
# surfaces and the decals. The build machine copies these beside its own test
# copy, so its frames looked right, but the steady copy Jafar plays never had
# them: its sky dome and surfaces fell back to plain colours and the street
# played three times darker than the editor (measured, mean luminance 17
# against 55 at the window). The game's finders look under LedgerData too.
DIRS = [
    "ledger/Assets/Resources/Sky",
    "ledger/Assets/StreamingAssets/CityPack/textures",
    DECAL_ROOT,
]
VOICE_ROOT = "ledger/Assets/StreamingAssets/Audio/Voice"
SOUND_ROOT = "production/assets/sounds"
MAP_SUFFIXES = ("", "_n", "_r")          # SurfaceBind.h MapSuffix


def _load(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return json.load(fh)


def decal_path(decal):
    """StreetMeshes.h PictureLeaf: under production/ from the repository root, else under the decal root."""
    if not decal:
        return None
    return (decal if decal.startswith("production/") else DECAL_ROOT + "/" + decal) + ".png"


def wanted():
    files = list(FIXED)
    side = _load("production/assets/street/quay-street.json")
    for row in side.get("meshes", []):
        d = decal_path(row.get("decal"))
        if d:
            files.append(d)
        dm = row.get("drawn_map")
        if dm:
            files += [dm + s + ".png" for s in MAP_SUFFIXES]
    pieces = _load("production/specs/vignette-pieces.json")
    for sc in pieces.get("scanned", []) or []:
        for f in sc.get("files", []) or []:
            if isinstance(f, str) and f:
                files.append(f)
    sounds = _load("production/specs/street-sounds.json")
    for v in sounds.get("voices", []) or []:
        for c in v.get("clips", []) or []:
            files.append(VOICE_ROOT + "/" + c)
    for a in sounds.get("ambience", []) or []:
        w = a.get("wav")
        if w:
            files.append(SOUND_ROOT + "/" + (w if w.endswith(".wav") else w + ".wav"))
    for d in DIRS:
        root = os.path.join(REPO, d)
        for dirpath, _dirs, names in os.walk(root):
            for n in names:
                if n.endswith(".meta"):
                    continue
                files.append(os.path.relpath(os.path.join(dirpath, n), REPO).replace("\\", "/"))
    seen, out = set(), []
    for f in files:
        f = f.replace("\\", "/")
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def stage(copy=True):
    files = wanted()
    have = [f for f in files if os.path.isfile(os.path.join(REPO, f))]
    missing = [f for f in files if f not in have]
    size = sum(os.path.getsize(os.path.join(REPO, f)) for f in have)
    if copy:
        for f in have:
            dst = os.path.join(DEST, f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(REPO, f), dst)
    print("stage_game_data: %s %d files, %.1f MB, missing=%d%s -> ue-probe/Content/LedgerData"
          % ("copied" if copy else "would copy", len(have), size / 1e6, len(missing),
             (" (" + ", ".join(missing[:6]) + ")") if missing else ""))
    return have, missing


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("stage_game_data selftest FAIL " + name)
    check("a production decal is read from the repository", decal_path("production/a/b") == "production/a/b.png")
    check("any other decal is under the decal root", decal_path("generated/x") == DECAL_ROOT + "/generated/x.png")
    check("no decal, no file", decal_path(None) is None)
    files = wanted()
    check("the street's sidecar is staged", "production/assets/street/quay-street.json" in files)
    check("the witness lines are staged", "content/dialogue/crime-witness-v1.json" in files)
    check("each drawn map comes with its normal and roughness", any(f.endswith("_n.png") for f in files) and any(f.endswith("_r.png") for f in files))
    check("the street's voices are staged", any(f.startswith(VOICE_ROOT) for f in files))
    check("nothing is listed twice", len(files) == len(set(files)))
    check("the sky photograph is staged", any(f.startswith("ledger/Assets/Resources/Sky/") and f.endswith(".png") for f in files))
    check("the photographed surfaces are staged", any(f.startswith("ledger/Assets/StreamingAssets/CityPack/textures/") for f in files))
    check("the staging folder is inside the game's content", DEST.replace("\\", "/").endswith("ue-probe/Content/LedgerData"))
    print("stage_game_data selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    _, missing = stage(copy="--list" not in sys.argv)
    sys.exit(1 if missing else 0)
