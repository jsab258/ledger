#!/usr/bin/env python3
"""Unpack conda-forge packages (.conda files) into a folder, without conda.

  python -I conda_unpack.py PYLIB DEST FILE.conda [FILE.conda ...]

A .conda file is a zip that holds pkg-<name>.tar.zst (the files) and info-<name>.tar.zst
(the recipe and licences). PYLIB is a folder holding the zstandard module from PyPI
(one-sim.sh setup installs it there). Only the pkg part is unpacked, into DEST.
"""
import sys
import tarfile
import zipfile


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    sys.path.insert(0, sys.argv[1])
    import zstandard
    dest = sys.argv[2]
    for path in sys.argv[3:]:
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if name.startswith("pkg-") and name.endswith(".tar.zst"):
                    with z.open(name) as f:
                        reader = zstandard.ZstdDecompressor().stream_reader(f)
                        with tarfile.open(fileobj=reader, mode="r|") as t:
                            t.extractall(dest, filter="tar")
                    print("unpacked", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
