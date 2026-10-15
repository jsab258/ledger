#!/usr/bin/env python3
"""Rita's shop (the pawnbroker, east_parade bay 2): the whole thing, rebuilt exactly by one command.

    python3 build_ritas.py                 # every stage, in order
    python3 build_ritas.py front display   # some stages
    python3 build_ritas.py --list

Since 13 October (batch A) this is a wrapper: the one command for every shop is build_shop.py (`python3 build_shop.py --shop ritas ...`), which reads the shop's numbers from target.json. Rita's output is
unchanged by the move (the front's glb, the display, the room's placed.json and the gate's STREET_SQUARE picture were compared with the stored ones, see NOTES.md).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    sys.exit(subprocess.run([sys.executable, os.path.join(HERE, "build_shop.py"), "--shop", "ritas"] + sys.argv[1:]).returncode)
