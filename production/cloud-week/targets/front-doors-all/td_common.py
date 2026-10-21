"""Shared paths and small helpers for the front-doors-all target (cloud week 42, unit 9).
Python: /home/user/.bpyenv/bin/python. Nothing here touches the network."""
import json
import os
import re
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DOOR31 = os.path.join(ROOT, "production", "cloud-week", "targets", "front-door", "target.json")
WINDOWS_T = os.path.join(ROOT, "production", "cloud-week", "targets", "house-windows", "target.json")
WEAR_T = os.path.join(ROOT, "production", "cloud-week", "targets", "wear", "target.json")
SCENE = os.path.join(ROOT, "production", "specs", "vignette-scene.json")
TERRACE_FRONT = os.path.join(ROOT, "tools", "art-recipes", "terrace-front.py")
VIEWS_T1 = os.path.join(ROOT, "production", "cloud-week", "kit", "door", "views_T1.json")
VIEWS_F1 = os.path.join(ROOT, "production", "cloud-week", "kit", "door", "views_F1.json")
PREVIEWS = os.path.join(ROOT, "production", "previews", "cloud-week", "refs", "front-doors-all")
TARGET_JSON = os.path.join(HERE, "target.json")

# Whole-word blocklist: real makers, firms and marks. The target says "rim night latch" for the lock.
BLOCKLIST = ["yale", "chubb", "ingersoll", "banham", "ebco", "hoppe", "paragon", "dixons", "everest", "anglian",
             "crittall", "pilkington", "masonite", "hormann", "union jack", "rolex"]
STALE_NIGHT = "(1, 0.7055, 0)"
LANTERN_LINEAR = [1.0, 0.25, 0.0]


def load_json(p):
    with open(p) as f:
        return json.load(f)


def strings(o, path=""):
    """Every string in a nested object with its path."""
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, path + "/" + str(k))
    elif isinstance(o, (list, tuple)):
        for i, v in enumerate(o):
            yield from strings(v, path + "[%d]" % i)


def words(s):
    return set(re.findall(r"[a-z0-9']+", s.lower()))


def blocklist_hits(o, skip_paths=()):
    hits = []
    for p, s in strings(o):
        if any(p.startswith(k) for k in skip_paths):
            continue
        low = s.lower()
        for b in BLOCKLIST:
            if re.search(r"(?<![a-z0-9'])" + re.escape(b) + r"(?![a-z0-9'])", low):
                hits.append((p, b))
    return hits


def r(x, n=1):
    return round(float(x), n)
