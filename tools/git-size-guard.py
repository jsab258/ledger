"""Only text and small files go into git: the check every session's commit runs.

    python tools/git-size-guard.py              # checks what is staged; tools/hooks/pre-commit runs it
    python tools/git-size-guard.py --selftest   # runs without git

WHY, 3 October (Jafar: "only text and small files go into git; renders, approval pictures,
audio, models and builds live on the drives and in the Dropbox backup"). The project's history
on GitHub had reached 32 GB, 30.6 GB of it the build machine's test pictures, committed on every
run from 22 September (that machine no longer commits them: .github/workflows/
ledger-probe-unreal.yml). A picture committed to git is kept for ever and never compresses against
the last one, so the rule is enforced where a commit is made, for all three sessions at once: the
hook lives in the shared git folder, which the builder's checkout, the town's and the clothing's
worktrees all use.

WHAT IT REFUSES, in every staged file that is added or changed:
- a picture, sound, film, AI model, build or archive (by its kind), anywhere outside the places
  the game's build reads from git;
- any file over 1 MB outside those places;
- in those places, any file over its cap;
- any text that holds one of the keys kept beside the LEDGER key (%LOCALAPPDATA%\\LEDGER\\*.txt),
  compared only, never printed.

THE PLACES THE BUILD READS FROM GIT (GAME_INPUTS): the build machine checks the game out of git
and imports the street, the people, the props, the sounds and the fonts from there, so those stay
in git under a cap a file; everything else large lives on the drives (F:\\LedgerTools, by
CLAUDE.md's retention rule) and in the Dropbox backup. A new place goes here with its reason.
"""
import glob
import os
import subprocess
import sys

LIMIT = 1_000_000                      # any file outside GAME_INPUTS: 1 MB
# HAND-WRITTEN CODE (3 October: the Core tests' one file is 2 MB): git keeps each change to a
# source file as a small difference against the last, so the history does not grow by its size;
# generated text (logs, verdicts, tables) keeps the 1 MB limit.
CODE_KINDS = {".cs", ".cpp", ".h", ".hpp", ".c", ".py", ".ps1", ".sh"}
CODE_LIMIT = 5_000_000
GAME_INPUTS = {                        # prefix: cap a file, in bytes
    "production/assets/": 25_000_000,  # meshes, textures, sounds the editor run imports
    "ue-probe/Content/": 25_000_000,   # the Unreal content the build makes and cooks
    "production/fonts/": 5_000_000,    # the game's own typefaces
    "production/reference/": 5_000_000,  # the bar every visual is judged against (the Hook sheet)
}
BIG_KINDS = {
    # pictures and renders
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tga", ".tif", ".tiff", ".exr", ".hdr", ".psd",
    # sound and film
    ".wav", ".mp3", ".ogg", ".flac", ".m4a", ".aac", ".mp4", ".webm", ".mov", ".avi", ".mkv",
    # models: AI weights and 3D source files
    ".safetensors", ".ckpt", ".pt", ".pth", ".onnx", ".gguf", ".bin", ".npz",
    ".blend", ".blend1", ".fbx", ".glb", ".gltf", ".obj", ".usd", ".usdz", ".abc", ".uasset", ".umap",
    # builds and archives
    ".exe", ".dll", ".pdb", ".pak", ".ucas", ".utoc", ".zip", ".7z", ".rar", ".tar", ".gz",
}
KEYS_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), "LEDGER")


def place_cap(path):
    for prefix, cap in GAME_INPUTS.items():
        if path.startswith(prefix):
            return cap
    return None


def verdict(path, size, head=b"", keys=()):
    """Why this staged file may not go into git, or None when it may."""
    path = path.replace("\\", "/")
    kind = os.path.splitext(path)[1].lower()
    cap = place_cap(path)
    if cap is None:
        if kind in BIG_KINDS:
            return "a %s file outside the places the build reads from git: it lives on the drives" % kind
        if kind in CODE_KINDS:
            if size > CODE_LIMIT:
                return "%.1f MB of code, over the %d MB a source file may be" % (size / 1e6, CODE_LIMIT // 1_000_000)
        elif size > LIMIT:
            return "%.1f MB, over the 1 MB a file outside the build's places may be" % (size / 1e6)
    elif size > cap:
        return "%.1f MB, over the %d MB a file in %s may be" % (size / 1e6, cap // 1_000_000, path.split("/")[0] + "/" + path.split("/")[1])
    if head and b"\0" not in head[:8000]:
        for k in keys:
            if k and k in head:
                return "holds one of the keys kept outside the project"
    return None


def load_keys():
    out = []
    for f in glob.glob(os.path.join(KEYS_DIR, "*.txt")):
        try:
            k = open(f, "rb").read().strip()
        except OSError:
            continue
        if len(k) >= 16:
            out.append(k)
    return out


def staged():
    raw = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
                         capture_output=True, check=True).stdout
    return [p for p in raw.decode("utf-8", "replace").split("\0") if p]


def main():
    keys = load_keys()
    bad = []
    for p in staged():
        size = int(subprocess.run(["git", "cat-file", "-s", ":" + p], capture_output=True, text=True).stdout.strip() or 0)
        head = b""
        if size <= LIMIT:
            head = subprocess.run(["git", "cat-file", "blob", ":" + p], capture_output=True).stdout
        why = verdict(p, size, head, keys)
        if why:
            bad.append((p, why))
    if bad:
        print("git-size-guard: this commit is refused. Only text and small files go into git; "
              "renders, approval pictures, audio, models and builds live on the drives (F:\\LedgerTools) "
              "and in the Dropbox backup (CLAUDE.md, Jafar 3 October).")
        for p, why in bad[:40]:
            print("  %s: %s" % (p, why))
        if len(bad) > 40:
            print("  ... and %d more" % (len(bad) - 40))
        print("Unstage them (git restore --staged <path>) and keep them on F:. Never commit with --no-verify.")
        return 1
    return 0


def selftest():
    passed = failed = 0

    def ok(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("git-size-guard selftest FAIL: " + name)
    ok("a build machine's picture is refused", verdict("production/d1-probe/ue-vign_hook_day.png", 1_800_000))
    ok("an approval picture is refused however small", verdict("production/approvals/ron/face.jpg", 40_000))
    ok("a voice take is refused", verdict("game-design/voice-live/take.wav", 300_000))
    ok("a render under production/art is refused", verdict("production/art/shop-rooms/grocer_day.png", 900_000))
    ok("a Blender file is refused", verdict("tools/art-recipes/scene.blend", 200_000))
    ok("text over 1 MB is refused", verdict("production/d1-probe/ue-build.txt", 1_500_000))
    ok("code is let through", verdict("tools/retention.py", 60_000, b"import os\n") is None)
    ok("hand-written code over 1 MB is let through: git keeps each change as a small difference",
       verdict("ledger/CoreTests/Program.cs", 2_000_000, b"using System;\n") is None)
    ok("but not past its own cap", verdict("ledger/CoreTests/Program.cs", 6_000_000, b"using System;\n"))
    ok("the street the build imports is let through", verdict("production/assets/street/quay-street.glb", 16_200_000) is None)
    ok("a game input over its cap is refused", verdict("production/assets/street/quay-street.glb", 30_000_000))
    ok("the Hook sheet is let through", verdict("production/reference/hook-sheet.png", 4_834_247) is None)
    ok("Windows paths are read the same", verdict("production\\d1-probe\\x.png", 10))
    ok("a key in text is refused", verdict("notes.md", 100, b"token 0123456789abcdef0123 here", [b"0123456789abcdef0123"]))
    ok("a key is not looked for in a binary file", verdict("production/assets/x.glb", 100, b"\0" + b"0123456789abcdef0123", [b"0123456789abcdef0123"]) is None)
    hook = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hooks", "pre-commit")
    ok("the hook runs this file from the shared checkout", os.path.isfile(hook) and "git-size-guard.py" in open(hook, encoding="utf-8").read())
    print("git-size-guard selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
