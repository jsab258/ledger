"""WHAT A GIVEN-OUT COPY OF THE GAME MUST DROP, AND WHICH LIBRARIES NEED A LICENCE BESIDE THEM.

Reads a list of the files in a package (one path per line; a manifest line's first tab-separated
field is the path, as in Unreal's Manifest_*_Win64.txt) and reports:

  drop     files that must come out before a copy leaves his PC (debug-only files)
  licence  third-party libraries shipped, the licence file each wants beside it, whether that
           file is in the list, and whether the library's terms have been read
  unknown  .dll files this table does not know (each needs its licence looked up)

Research behind the table: production/research/lane/SHIPPED-LIBRARIES-LICENCES-2026-11-18.md
and production/research/engine-notices/NOTE.md (5 October 2026).

    python tools/lane/release_libs.py MANIFEST.txt      (or the list on standard input)
    python tools/lane/release_libs.py --json MANIFEST.txt

Exit code 0 when nothing must be dropped, every known library's terms are read and its licence
file is in the list, and no unknown .dll is shipped; 1 otherwise.
"""
import json
import sys

# Debug-only files: never in a copy given out.
DROP = {
    "d3d12sdklayers.dll": "the Direct3D 12 debug layer; Microsoft's Agility SDK guide (20 April 2021) says to "
                          "remove it from a game's installer, and the redistributable spec says it should not "
                          "be installed on end user machines",
    "d3dconfig.exe": "the Agility SDK's debug-layer settings tool, a developer tool beside the debug layer, "
                     "not needed by a player",
}

# Each shipped third-party library: the licence file wanted beside it (in production/licences/engine,
# staged into the package), and whether its terms have been read ("read" / "not read").
LIBRARIES = {
    "libogg_64.dll": ("ogg-LICENSE.txt", "read", "BSD 3-clause: notice in the documentation"),
    "libvorbis_64.dll": ("vorbis-LICENSE.txt", "read", "BSD 3-clause: notice in the documentation"),
    "libvorbisfile_64.dll": ("vorbis-LICENSE.txt", "read", "BSD 3-clause: notice in the documentation"),
    "msquic.dll": ("msquic-LICENSE.txt", "read", "MIT: notice with all copies"),
    "tbb12.dll": ("onetbb-LICENSE.txt", "read", "Apache 2.0: licence and NOTICE with the work"),
    "tbbmalloc.dll": ("onetbb-LICENSE.txt", "read", "Apache 2.0: licence and NOTICE with the work"),
    "onnxruntime.dll": ("onnxruntime-LICENSE.txt", "read", "licence and its third-party notices"),
    "directml.dll": ("directml-LICENSE.txt", "read", "Microsoft terms: end-user terms as protective, notices kept"),
    "d3d12core.dll": ("d3d12-agility-sdk-LICENSE.txt", "read",
                      "Microsoft DirectX terms: distributable as listed in the SDK; end-user terms as protective"),
    "xaudio2_9redist.dll": ("xaudio2-redist-LICENSE.txt", "read",
                            "Microsoft XAudio 2.9 Redistributable terms (NuGet 1.2.13, read 18 Nov 2026): add "
                            "significant function, end users agree to terms as protective, indemnify Microsoft; "
                            "no credit line asked"),
    "gfsdk_aftermath_lib.x64.dll": ("nvidia-aftermath-LICENSE.txt", "not read",
                                    "NVIDIA's current Aftermath terms (v2026.3 docs) read 18 Nov 2026; the text "
                                    "for SDK 2025.5, the version shipped, not read"),
    "dbghelp.dll": ("dbghelp-LICENSE.txt", "not read",
                    "only Debugging Tools for Windows copies are redistributable; which copy 10.0.25291 is, "
                    "and its terms, not read"),
}


def paths_from(lines):
    """The file paths in a list or manifest: first tab field, forward slashes, blanks skipped."""
    out = []
    for line in lines:
        p = line.split("\t")[0].strip().replace("\\", "/")
        if p:
            out.append(p)
    return out


def base(path):
    return path.rsplit("/", 1)[-1].lower()


def report(lines):
    """A dict: drop (path, reason), licence (path, library, file, present, status, note), unknown (path)."""
    files = paths_from(lines)
    names = {base(f) for f in files}
    drop, licence, unknown = [], [], []
    for f in files:
        b = base(f)
        if b in DROP:
            drop.append({"path": f, "reason": DROP[b]})
        elif b in LIBRARIES:
            wanted, status, note = LIBRARIES[b]
            licence.append({"path": f, "library": b, "licence_file": wanted,
                            "licence_present": wanted.lower() in names, "status": status, "note": note})
        elif b.endswith(".dll"):
            unknown.append({"path": f})
    clean = (not drop and not unknown
             and all(x["status"] == "read" and x["licence_present"] for x in licence))
    return {"drop": drop, "licence": licence, "unknown": unknown, "clean": clean}


def text(r):
    out = []
    out.append(f"Drop before giving a copy out: {len(r['drop'])}")
    for d in r["drop"]:
        out.append(f"  DROP  {d['path']}  ({d['reason']})")
    out.append(f"Libraries needing a licence beside them: {len(r['licence'])}")
    for x in r["licence"]:
        have = "present" if x["licence_present"] else "MISSING"
        out.append(f"  {x['status'].upper():8}  {x['path']}  wants {x['licence_file']} ({have})  {x['note']}")
    out.append(f"Unknown libraries: {len(r['unknown'])}")
    for u in r["unknown"]:
        out.append(f"  UNKNOWN  {u['path']}")
    out.append("clean" if r["clean"] else "not clean")
    return "\n".join(out)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if argv:
        with open(argv[0], encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    else:
        lines = sys.stdin.read().splitlines()
    r = report(lines)
    print(json.dumps(r, indent=2) if as_json else text(r))
    return 0 if r["clean"] else 1


if __name__ == "__main__":
    sys.exit(main())
