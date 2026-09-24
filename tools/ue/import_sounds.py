"""The street's sounds into Unreal: every clip production/specs/street-sounds.json
names, as a SoundWave, in the editor run the cook step already starts.

    python3 tools/ue/import_sounds.py --selftest     # runs without Unreal

WHY IT EXISTS, 23 September. Jafar's presentable checklist: "sound is
positional: a voice or a noise comes from where its source is and changes as
you move" - and the street made no sound at all. The probe places each sound
with an Unreal audio component and the engine's own attenuation; a packaged
game can only play a SoundWave that exists as an asset, so the wavs become
assets here, as the street's meshes do.

WHAT IT MAKES: /Game/Ledger/Sounds/Voice/<voice>/<clip> for each person's
pre-voiced lines (ledger/Assets/StreamingAssets/Audio/Voice) and
/Game/Ledger/Sounds/Ambience/<name> for each ambience bed
(production/assets/sounds), the beds set to loop.

ONE LINE, appended to ue-material.txt: asked, made, and why not.
"""
import json
import os
import sys
import time

SPEC_REL = "production/specs/street-sounds.json"
VOICE_REL = "ledger/Assets/StreamingAssets/Audio/Voice"
AMBIENCE_REL = "production/assets/sounds"
PACKAGE_ROOT = "/Game/Ledger/Sounds"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def wanted(root):
    """[(source path, destination folder, asset name, loops)] from the spec."""
    with open(os.path.join(root, SPEC_REL), encoding="utf-8") as fh:
        spec = json.load(fh)
    out = []
    for a in spec.get("ambience", []):
        out.append((os.path.join(root, AMBIENCE_REL, a["wav"] + ".wav"),
                    PACKAGE_ROOT + "/Ambience", a["wav"], True))
    seen = set()
    for v in spec.get("voices", []):
        for c in v.get("clips", []):
            if c in seen:
                continue
            seen.add(c)
            voice, leaf = c.split("/", 1)
            out.append((os.path.join(root, VOICE_REL, c), PACKAGE_ROOT + "/Voice/" + voice,
                        os.path.splitext(leaf)[0], False))
    # ONE-OFF CUES, 24 September: a clip the game plays on an event (the
    # encounter's shout), imported like a voice line and never looped.
    for q in spec.get("cues", []):
        c = q["clip"]
        if c in seen:
            continue
        seen.add(c)
        voice, leaf = c.split("/", 1)
        out.append((os.path.join(root, VOICE_REL, c), PACKAGE_ROOT + "/Voice/" + voice,
                    os.path.splitext(leaf)[0], False))
    return out


def asset_path(folder, name):
    return "%s/%s" % (folder, name)


def sounds_line(asked, made, loops, seconds, notes):
    return ("soundsImportStatus=%s soundsImported=%d/%d soundsLooping=%d "
            "soundsImportSeconds=%.1f soundsImportNote=%s"
            % ("OK" if asked and made == asked else ("NOTHING" if not asked else "PARTIAL"),
               made, asked, loops, seconds, ("/".join(notes) or "none").replace(" ", "~")[:200]))


def selftest():
    passed = failed = 0

    def ok(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("import_sounds selftest FAIL %s: %s" % (name, detail))
    w = wanted(repo_root())
    ok("the spec names sounds", len(w) >= 2, str(len(w)))
    ok("every named sound is on disk", all(os.path.exists(p) for p, _, _, _ in w),
       str([p for p, _, _, _ in w if not os.path.exists(p)][:3]))
    ok("the ambience loops and the voices do not",
       any(l for _, _, _, l in w) and any(not l for _, _, _, l in w))
    ok("the line carries its denominator", "soundsImported=1/2" in sounds_line(2, 1, 0, 1.0, ["x"]))
    print("import_sounds selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


def main():
    import unreal
    t0 = time.time()
    root = repo_root()
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    lib = unreal.EditorAssetLibrary
    notes = []
    try:
        todo = wanted(root)
    except Exception as e:
        todo = []
        notes.append("spec-" + (str(e).splitlines()[0][:60] if str(e) else "unreadable"))
    made = loops = 0
    if lib.does_directory_exist(PACKAGE_ROOT):
        lib.delete_directory(PACKAGE_ROOT)
    for src, folder, name, loop in todo:
        try:
            task = unreal.AssetImportTask()
            task.set_editor_property("filename", src)
            task.set_editor_property("destination_path", folder)
            task.set_editor_property("destination_name", name)
            task.set_editor_property("automated", True)
            task.set_editor_property("replace_existing", True)
            task.set_editor_property("save", True)
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
            a = lib.load_asset(asset_path(folder, name))
            if not isinstance(a, unreal.SoundWave):
                notes.append("%s-not-a-soundwave" % name)
                continue
            if loop:
                a.set_editor_property("looping", True)
                if a.get_editor_property("looping"):
                    loops += 1
            lib.save_asset(asset_path(folder, name), False)
            made += 1
        except Exception as e:
            notes.append("%s-raised-%s" % (name, str(e).splitlines()[0][:60] if str(e) else "?"))
    line = sounds_line(len(todo), made, loops, time.time() - t0, notes)
    with open(out, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print("import_sounds: " + line)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
