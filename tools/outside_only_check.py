#!/usr/bin/env python3
"""OTHER GAMES ARE STUDIED FROM THE OUTSIDE ONLY: NO DECOMPILER, NO EXTRACTOR, NO ANOTHER GAME'S FILES.

    python tools/outside_only_check.py              # one line: outsideOnly found=N outcome=PASS|FAIL, each hit above it
    python tools/outside_only_check.py --selftest

WHY, 17 November 2026 (his ruling 22:33 through the advisor, 214; RULINGS' line "17 Nov (replaces 11, 25, 28 Oct):
other games are studied from the outside only"): other games are never decompiled, their files never opened or
extracted. Until then studies had used FModel on Mafia and KCD2, and its copies stayed on F: after the ruling ended
them. A ruling held by memory alone fails the first time a helper reaches for the old tool, so this fails the build.

WHAT FAILS, each printed as one line "outsideOnly HIT <kind> <path> <size>":
  tool      a decompiler or game-file extractor (the TOOLS table below) found by name: a folder so named, or a program
            or archive file so named (.exe .dll .jar .zip .7z ...). Writing ABOUT a tool (a research note named
            UE4SS-READING.md) is allowed: notes, tables and pictures are not the tool. In tools/ a script that calls
            one by its executable name (FModel.exe, quickbms.exe) fails too.
  archive   another game's packed files: .pak .utoc .ucas .sig
  asset     extracted asset files: .uasset .uexp .umap outside our own Unreal projects' Content (a folder holding a
            .uproject, its Content/ and Plugins/*/Content/; ue-probe in the repository and the projects named in
            OWN_PROJECTS below)
  uses      C# source or project (.cs .csproj .sln) built on an extractor library (CUE4Parse, UAssetAPI, UE4SS):
            a home-made extractor carries no tool's name (study-b-sh2's reader, 6 Nov, did not)
  extract   a folder whose name says it holds an extract ("extract", "fmodel-export")
WHERE IT LOOKS (CPU kept light, never a whole drive):
  - git's tracked files (git ls-files) and everything under tools/
  - on F:, only the named folders that exist, two levels down: F:/LedgerTools/study, studies, tools, tool-dev
  - and every folder production/storage-map.json lists whose shelf or path mentions study, extract or FModel, three
    levels down (FModel's CUE4Parse libraries sat at the third level of aaa-study when this was written)
A matched folder is reported once and not entered. Nothing is deleted: the session decides what to do with a hit
(retention rules, or his yes for anything of his).
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL_MESSAGE = "outsideOnly FAIL another game's decompiler, extractor or files are present"

# ONE DATA TABLE: name -> pattern matched against a file or folder name, lower case.
TOOLS = {
    "FModel": r"fmodel",
    "UE4SS": r"ue4ss",
    "umodel / UEViewer": r"umodel|ueviewer|ue-viewer",
    "QuickBMS": r"quickbms|\.bms$",
    "CUE4Parse": r"cue4parse",
    "repak": r"(^|[^a-z])repak",
    "UnrealPak (copied out of the engine)": r"unrealpak",
    "retoc / ZenTools (IoStore unpackers)": r"(^|[^a-z])retoc|zentools",
    "UAssetGUI / UAssetAPI": r"uassetgui|uassetapi",
    "Ghidra": r"ghidra",
    "IDA": r"^ida(64|t|t64|w|q)?(\.exe)?$|idapro|hex-?rays",
    "dnSpy": r"dnspy",
    "ILSpy": r"ilspy",
    "AssetRipper / AssetStudio": r"assetripper|assetstudio",
    "x64dbg / Cheat Engine": r"x64dbg|x32dbg|cheatengine|cheat engine",
}
PROGRAM_EXT = (".exe", ".dll", ".jar", ".zip", ".7z", ".rar", ".msi", ".bat", ".cmd", ".ps1", ".lua", ".bms", ".so", ".py", "")
ARCHIVE_EXT = (".pak", ".utoc", ".ucas", ".sig")
ASSET_EXT = (".uasset", ".uexp", ".umap")
EXTRACT_DIR = r"extract|fmodel-?export"
USES_LIBRARY = r"cue4parse|uassetapi|ue4ss"  # a home-made extractor: C# source or project built on one
USES_EXT = (".cs", ".csproj", ".sln")
CALL_IN_TOOLS = r"\b(fmodel|ue4ss|umodel|quickbms|cue4parse|repak|retoc|uassetgui|ghidra(run)?|ida64|dnspy|ilspy(cmd)?)\.(exe|dll|jar)\b"
# Our own Unreal projects outside the repository (their Content is ours).
OWN_PROJECTS = (
    "C:/LedgerTools/mh-assemble", "C:/LedgerTools/mh-assemble-before-dressing-2026-09-24", "C:/LedgerTools/mocap-solve",
    "F:/LedgerTools/mh-dress", "F:/LedgerTools/game-inputs/fab-check", "F:/LedgerTools/game-inputs/gasp",
)
NAMED_F = ("F:/LedgerTools/study", "F:/LedgerTools/studies", "F:/LedgerTools/tools", "F:/LedgerTools/tool-dev")
MAP_WORDS = ("study", "extract", "fmodel")


def norm(p):
    return p.replace("\\", "/").rstrip("/")


def tool_of(name, is_dir):
    low = name.lower()
    if not is_dir and os.path.splitext(low)[1] not in PROGRAM_EXT:
        return None
    for label, pat in TOOLS.items():
        if re.search(pat, low):
            return label
    return None


def own_content_roots(root, tracked):
    roots = [norm(os.path.join(root, os.path.dirname(t))) for t in tracked if t.lower().endswith(".uproject")]
    roots += [norm(p) for p in OWN_PROJECTS]
    return [r.lower() for r in roots]


def is_own_asset(path, roots):
    p = norm(path).lower()
    for r in roots:
        if p.startswith(r + "/content/") or re.match(re.escape(r) + r"/plugins/[^/]+/content/", p):
            return True
    return False


def classify(path, is_dir, roots):
    name = os.path.basename(norm(path))
    t = tool_of(name, is_dir)
    if t:
        return "tool(%s)" % t
    if is_dir:
        return "extract" if re.search(EXTRACT_DIR, name.lower()) else None
    ext = os.path.splitext(name.lower())[1]
    if ext in ARCHIVE_EXT:
        return "archive"
    if ext in ASSET_EXT and not is_own_asset(path, roots):
        return "asset"
    return None


def uses_of(path):
    if not path.lower().endswith(USES_EXT):
        return None
    try:
        m = re.search(USES_LIBRARY, open(path, encoding="utf-8", errors="replace").read(), re.I)
    except OSError:
        return None
    return "uses(%s)" % m.group(0) if m else None


def size_of(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    total = 0
    for d, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(d, f))
            except OSError:
                pass
    return total


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return "%.0f%s" % (n, unit) if unit == "B" else "%.1f%s" % (n, unit)
        n /= 1024.0


def walk_limited(top, depth, roots, hits):
    """Each entry down to `depth` levels below top; a matched folder is reported and not entered."""
    try:
        entries = sorted(os.scandir(top), key=lambda e: e.name)
    except OSError:
        return
    for e in entries:
        is_dir = e.is_dir(follow_symlinks=False)
        kind = classify(e.path, is_dir, roots) or (None if is_dir else uses_of(e.path))
        if kind:
            hits.append((kind, norm(e.path)))
        elif is_dir and depth > 1 and e.name != "__pycache__":
            walk_limited(e.path, depth - 1, roots, hits)


def map_folders(root):
    path = os.path.join(root, "production", "storage-map.json")
    try:
        folders = json.load(open(path, encoding="utf-8")).get("folders", [])
    except (OSError, ValueError):
        return []
    out = []
    for f in folders:
        text = ("%s %s" % (f.get("shelf", ""), f.get("path", ""))).lower()
        if any(w in text for w in MAP_WORDS):
            out.append(f["path"])
    return out


def git_tracked(root):
    r = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True)
    if r.returncode != 0:
        return None
    return [t for t in r.stdout.decode("utf-8", "replace").split("\0") if t]


# PROTECTED FOLDERS AWAITING HIS YES (17 Nov 22:55): retention.py refuses deleting these study folders (protected), so
# their old extractors wait on his page item study-tools-delete-2026-11-17; listed, not failing, until he answers.
# Remove each line once its folder is gone or he says keep.
AWAITING = ("F:/LedgerTools/aaa-study/study-a-inzoi-extract", "F:/LedgerTools/aaa-study/study-b-sh2",
            "F:/LedgerTools/aaa-study/tools/FModel-aug-2026.zip", "F:/LedgerTools/aaa-study/tools/fmodel-aug-2026")


def check(root=ROOT, tracked=None, named=NAMED_F, mapped=None, out=sys.stdout):
    if tracked is None:
        tracked = git_tracked(root)
        if tracked is None:
            print("outsideOnly found=0 outcome=FAIL git ls-files failed: nothing measured must never read as clean", file=out)
            return 1
    if mapped is None:
        mapped = map_folders(root)
    roots = own_content_roots(root, tracked)
    hits = []
    seen_dirs = set()
    for t in tracked:
        parts = t.split("/")
        for i in range(len(parts) - 1):  # folder components, each once
            d = "/".join(parts[: i + 1])
            if d in seen_dirs:
                continue
            seen_dirs.add(d)
            kind = classify(os.path.join(root, d), True, roots)
            if kind:
                hits.append((kind, norm(os.path.join(root, d))))
        full = norm(os.path.join(root, t))
        if any(full.startswith(h + "/") for _, h in hits):
            continue  # inside a folder already reported
        kind = classify(os.path.join(root, t), False, roots)
        if kind:
            hits.append((kind, norm(os.path.join(root, t))))
    tools_dir = os.path.join(root, "tools")
    tracked_set = set(norm(os.path.join(root, t)) for t in tracked)
    for d, dirs, files in os.walk(tools_dir):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for x in list(dirs):
            p = norm(os.path.join(d, x))
            kind = classify(p, True, roots)
            if kind:
                dirs.remove(x)
                if p not in [h[1] for h in hits]:
                    hits.append((kind, p))
        for f in files:
            p = norm(os.path.join(d, f))
            kind = classify(p, False, roots)
            if not kind and p not in tracked_set:
                kind = uses_of(p)
            if kind and p not in tracked_set:
                hits.append((kind, p))
            if f.endswith((".py", ".ps1", ".sh", ".bat", ".cmd")) and os.path.abspath(p) != os.path.abspath(__file__):
                try:
                    text = open(p, encoding="utf-8", errors="replace").read()
                except OSError:
                    continue
                m = re.search(CALL_IN_TOOLS, text, re.I)
                if m:
                    hits.append(("calls(%s)" % m.group(0), p))
    looked = 0
    for top, depth in [(n, 2) for n in named] + [(m, 3) for m in mapped]:
        if os.path.isdir(top):
            looked += 1
            walk_limited(top, depth, roots, hits)
    waiting = [(k, p) for k, p in hits if out is sys.stdout and any(p == a or p.startswith(a + "/") for a in AWAITING)]
    hits = [h for h in hits if h not in waiting]
    for kind, p in waiting:
        print("outsideOnly WAITING HIS YES %s %s %s" % (kind, p, human(size_of(p))), file=out)
    for kind, p in hits:
        print("outsideOnly HIT %s %s %s" % (kind, p, human(size_of(p))), file=out)
    if hits:
        print(FAIL_MESSAGE + " (delete nothing here: the session decides)", file=out)
    print("outsideOnly found=%d tracked=%d folders=%d outcome=%s" % (len(hits), len(tracked), looked, "FAIL" if hits else "PASS"), file=out)
    return 1 if hits else 0


def selftest():
    import io
    ok = True

    def t(cond, what):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + what)
        ok = ok and cond

    def mk(base, rel, body="x"):
        p = os.path.join(base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(body)

    d = tempfile.mkdtemp()
    repo, fdrive = os.path.join(d, "repo"), os.path.join(d, "F")
    tracked = ["ue-probe/LedgerProbe.uproject", "ue-probe/Content/Ledger/Kit/Wall.uasset",
               "production/research/UE4SS-READING-2026-11-12.md", "tools/catalogue.py"]
    for rel in tracked:
        mk(repo, rel)
    os.makedirs(os.path.join(fdrive, "study"))
    mapped_dir = os.path.join(fdrive, "aaa-study")
    mk(mapped_dir, "study-5/mafia_numbers.csv")
    mk(mapped_dir, "public/study-2-sources.md")

    def run(tr=None, mapped=(mapped_dir,)):
        s = io.StringIO()
        rc = check(repo, tracked if tr is None else tr, (os.path.join(fdrive, "study"), os.path.join(fdrive, "missing")), list(mapped), s)
        return rc, s.getvalue()

    rc, txt = run()
    t(rc == 0, "our own uassets, a research note about UE4SS and recorded numbers pass")
    t("outcome=PASS" in txt.splitlines()[-1], "the last line carries outcome=PASS")

    mk(mapped_dir, "tools/FModel-aug-2026.zip")
    rc, txt = run()
    t(rc == 1 and "tool(FModel)" in txt and FAIL_MESSAGE in txt, "an FModel zip in a mapped study folder fails")
    os.remove(os.path.join(mapped_dir, "tools/FModel-aug-2026.zip"))

    mk(mapped_dir, "study-b/bin/CUE4Parse.dll")
    rc, txt = run()
    t(rc == 1 and "tool(CUE4Parse)" in txt, "an extractor's library three levels down in a mapped folder fails")
    os.remove(os.path.join(mapped_dir, "study-b/bin/CUE4Parse.dll"))

    mk(fdrive, "study/x/y/deep/FModel.exe")
    rc, _ = run()
    t(rc == 0, "a named F: folder is read two levels down only (CPU kept light)")
    mk(fdrive, "study/fmodel-1/FModel.exe")
    rc, txt = run()
    t(rc == 1 and txt.count("outsideOnly HIT") == 1, "a matched folder is one hit, not entered")

    mk(repo, "production/mafia/Content/Palermo/Car.uasset")
    rc, txt = run(tracked + ["production/mafia/Content/Palermo/Car.uasset"])
    t(rc == 1 and "asset " in txt, "a tracked uasset outside our projects fails (an extract)")

    mk(repo, "game/pakchunk0-Windows.utoc")
    rc, txt = run(tracked + ["game/pakchunk0-Windows.utoc"])
    t(rc == 1 and "archive" in txt, "another game's IoStore archive in git fails")

    mk(repo, "tools/vendor/quickbms/quickbms.exe")
    rc, txt = run()
    t(rc == 1 and "tool(QuickBMS)" in txt, "an extractor dropped under tools/ (untracked) fails")
    import shutil
    shutil.rmtree(os.path.join(repo, "tools/vendor"))

    mk(repo, "tools/read_study.py", "subprocess.run(['C:/x/FModel.exe', '--export'])\n")
    rc, txt = run()
    t(rc == 1 and "calls(FModel.exe)" in txt, "a script in tools/ calling an extractor by executable fails")
    os.remove(os.path.join(repo, "tools/read_study.py"))

    mk(mapped_dir, "study-c/tool/tool.csproj", '<Reference Include="CUE4Parse"/>')
    rc, txt = run()
    t(rc == 1 and "uses(CUE4Parse)" in txt, "a home-made reader built on CUE4Parse fails though named 'tool'")
    os.remove(os.path.join(mapped_dir, "study-c/tool/tool.csproj"))

    os.makedirs(os.path.join(mapped_dir, "study-a-inzoi-extract"))
    rc, txt = run()
    t(rc == 1 and "extract " in txt, "an extract folder fails even empty")

    t(tool_of("UE4SS-METHOD-LICENCE.md", False) is None and tool_of("UE4SS.dll", False), "a note is not the tool; the dll is")
    t(tool_of("prepak.py", False) is None and tool_of("repak.exe", False), "repak matches only as its own word")
    print("outsideOnly selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else check())
