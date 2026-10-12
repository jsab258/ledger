#!/bin/sh
# Rebuild everything in order (about 4 minutes): target.json, its self-check (live), the controls, the previews, TARGET.md.
set -e
PY=/home/user/.bpyenv/bin/python
cd "$(dirname "$0")"
$PY -I make_target.py
$PY -I self_check.py --live
$PY -I controls.py
$PY -I make_previews.py
$PY -I make_doc.py
