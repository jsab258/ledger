"""The target's numbers for the house windows, read from target.json (production/cloud-week/targets/house-windows/): the one place the kit scripts get them.

Nothing here needs Blender. Frames (target section 0): windows in millimetres in the KIT frame (x across, 0 at the window's middle, + to the viewer's right; y INTO the wall from the brick face;
z UP from the opening's bottom edge); rooms in metres in the ROOM frame (x across from the room's centre, + toward the picture's right; y back from the card plane; z up from the floor);
the street in metres as the scene file has it (x along, y across, east +, z above the road crown; the footway is crown + 0.10).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_DIR = os.path.join(REPO, "production", "cloud-week", "targets", "house-windows")
TARGET_JSON = os.path.join(TARGET_DIR, "target.json")
SCRATCH = os.environ.get("LEDGER_HW_SCRATCH", "/home/user/ledger-scratch/house-windows")
POLY = os.path.join(SCRATCH, "polyhaven")
ROOMS = os.path.join(SCRATCH, "rooms")
GATE = os.path.join(SCRATCH, "gate")
KITWORK = os.path.join(SCRATCH, "kit")
ASSETS = os.path.join(REPO, "production", "assets", "cloud-week", "house-windows")
PREVIEWS = os.path.join(REPO, "production", "previews", "cloud-week", "house-windows")
CHECKS = os.path.join(HERE, "checks")
LAB_GLB = {"S22": os.path.join(REPO, "production", "assets", "sash-window", "sash_window.glb"),
           "S11": os.path.join(REPO, "production", "assets", "sash-window", "sash_window_1over1.glb")}
SHARED_HDRI = "/home/user/ledger-scratch/polyhaven/_hdri"       # read only: another builder's cache of Poly Haven HDRIs (CC0); never written here
SKY_HDRI = os.path.join(REPO, "ledger", "Assets", "Resources", "Sky", "polyhaven", "belfast_open_field_2k.hdr")
DATE = "2026-10-13"          # the date the brief gives for the try 1 preview names (they stay)
DATE2 = "2026-10-14-v2"      # the try 2 previews (14 October, after the try 1 reviews): hw-<view>-<state>-2026-10-14-v2.jpg
MM = 0.001

_T = None


def target():
    global _T
    if _T is None:
        _T = json.load(open(TARGET_JSON, encoding="utf-8"))
    return _T


def sites():
    return target()["sites"]


def site(sid):
    return next(s for s in sites() if s["id"] == sid)


def rooms():
    return target()["rooms"]["rooms"]


def room(rid):
    return rooms()[rid]


def families():
    return target()["rooms"]["families"]


def paints():
    return target()["paints"]


def lit_at(hour="20:30"):
    return list(target()["rooms"]["lit_share"]["lit_by_hour"][hour]["windows"])


def srgb_to_lin(c):
    c = [v / 255.0 for v in c]
    return [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]


def room_for_site(s):
    return room(s["room"])


def ensure(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)
