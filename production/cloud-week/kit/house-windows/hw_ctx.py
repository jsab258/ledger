"""The shop context: everything about WHICH shop is being built that the code needs, read from target.json (production/cloud-week/targets/shop-windows/).

Used by build_shop.py and every sw_*.py / check_*.py. One `Ctx(shop_id)` per run. Nothing in the kit holds a shop's own numbers: the front's zones, paints, door end, the card, the cameras and the file names come from here,
and a number the target lacks is a named Judgement in NOTES.md. Rita's context reproduces the constants the kit was written with (bay middle street x 18, wall face y 5.295, card at y 5.875, the pictures called pawnbroker_*).

Frames (the kit's):
  front model   x_m = (u - 3000) / 1000, u in millimetres across the bay from the viewer's LEFT; y_m = -d (d out from the wall face toward the street), z_m above the footway (the crown + 0.10)
  street        east shops (east_parade, east_chandler): the front is at street y +5.295, the viewer on the far pavement at y -3.505; the viewer's left is the HIGH street x (Unreal is left-handed)
                west shops (west_north): the front is at y -5.295, the viewer at y +3.505; the viewer's left is the LOW street x
  Y             the distance from the street's centreline toward the shops (always positive): wall face 5.295, glass 5.245 to 5.265, card 5.875, kerb 3.63, the far pavement -3.505
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SCRATCH = os.environ.get("LEDGER_SW_SCRATCH", "/home/user/ledger-scratch")
WORK_ROOT = os.path.join(SCRATCH, "shop-windows")
ASSETS = os.path.join(REPO, "production", "assets", "cloud-week", "shop-windows")
PREVIEWS = os.path.join(REPO, "production", "previews", "cloud-week", "shop-windows")
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "shop-windows", "target.json")
BAY_MID_U = 3000.0
WALL_Y = 5.295            # |street y| of the wall face (d 0): the kit's glass back face (d 30) stands at the street model's 5.265
FOOT = 0.10               # the footway is the crown + 0.10
DATE = "2026-10-13"

_T = None


def load_target():
    global _T
    if _T is None:
        _T = json.load(open(TARGET_JSON, encoding="utf-8"))
    return _T


class Ctx:
    def __init__(self, shop_id, T=None):
        self.T = T or load_target()
        self.id = shop_id
        self.R = next(s for s in self.T["shops"] if s["id"] == shop_id)
        R = self.R
        self.west = R["side"] == "west"
        self.sgn = -1 if self.west else 1                 # the sign of the shop side's street y
        self.trace_side = -1 if self.west else 1          # make_interior_material.trace's `side`
        self.bay0, self.bay1 = R["street_x_m"]
        self.mid_x = (self.bay0 + self.bay1) / 2.0         # the street x of u 3000
        self.wall_y = WALL_Y
        self.zones = R["front"]["zones_u_mm"]
        self.door_end = R["front"]["door_end_viewer"]       # "L" or "R": which end of the bay the doors are at, seen from the street
        self.variants = R["front"]["variants"]
        lob = R["front"].get("lobby") or {}
        self.lobby_depth = float(lob["depth"]) if lob.get("kind") == "recessed" else 0.0     # a recessed lobby (the launderette 300, the grocer 600): the door frame stands that far behind the frame line
        self.has_room = bool(R.get("needs_room"))
        self.card = R.get("card")
        if self.card:
            self.card_x0, self.card_x1 = self.card["x0"], self.card["x1"]
            self.card_y = abs(self.card["z"])                # |y|: 5.875
            self.card_bottom, self.card_top = self.card["bottom"], self.card["top"]
        else:
            # the empty unit has no card in the street (bay 3 of 6 is skipped): the gate stands one in (the rule's: bay start + 0.35 to bay end - 0.35, z 0.65 to 3.05, 5.875 out) behind the whitewash
            self.card_x0, self.card_x1 = self.bay0 + 0.35, self.bay1 - 0.35
            self.card_y = 5.875
            self.card_bottom, self.card_top = 0.65, 3.05
        # pictures: the spec name is the file stem (pawnbroker for Rita's, tea_room for the tea rooms)
        self.picture_name = None
        if R.get("pictures"):
            self.picture_name = R["pictures"]["states"]["day"][:-len("_day.png")]
        elif not self.has_room:
            self.picture_name = "%s_standin" % shop_id             # Mickey's (its real room is owed to the PC) and the empty unit: a flat stand-in card for the gate (sw_gate_run.standin_card_pictures)
        self.lit = bool(R.get("lit_at_night"))
        # file names
        self.front_glb = "%s_front.glb" % shop_id
        self.display_glb = "%s_display.glb" % shop_id
        self.grille_glb = "%s_grille_night.glb" % shop_id
        self.work = WORK_ROOT if shop_id == "ritas" else os.path.join(WORK_ROOT, shop_id)       # Rita's keeps the places the earlier tries used
        self.fascias = os.path.join(self.work, "fascias")
        self.paper = os.path.join(WORK_ROOT, "paper")        # the OPEN / CLOSED sign (4.2) is the same for every shop
        self.rooms = os.path.join(self.work, "rooms")
        self.gate = os.path.join(self.work, "gate")
        self.display_work = os.path.join(self.work, "display_work")
        nf = (R.get("night_furniture") or "").lower()
        self.has_grille = "lattice" in nf
        w = self.zones["window"]
        self.window_u = (float(w[0]), float(w[1]))
        self.window_cx_m = ((w[0] + w[1]) / 2.0 - BAY_MID_U) / 1000.0     # the window zone's centre in the front model's x (Rita's 0.975)
        self.window_len = (w[1] - w[0]) / 1000.0

    # ---- frames
    def u_of_x(self, x):
        """u (mm, from the viewer's left) of a street x."""
        return BAY_MID_U + ((x - self.mid_x) if self.west else (self.mid_x - x)) * 1000.0

    def x_of_u(self, u):
        d = (u - BAY_MID_U) / 1000.0
        return self.mid_x + (d if self.west else -d)

    def ym(self, Y):
        """The front model's y for a distance Y from the centreline toward the shops (wall face 5.295 -> 0; the card 5.875 -> +0.58; the kerb 3.63 -> -1.665)."""
        return Y - WALL_Y

    def to_model(self, p):
        """street (x, y, z above the crown) -> the front model's frame (x_m to the viewer's right, y_m = -d, z_m above the footway)."""
        return ((self.u_of_x(p[0]) - BAY_MID_U) / 1000.0, self.sgn * p[1] - WALL_Y, p[2] - FOOT)

    def eye_card(self, eye_street):
        """The eye in the card frame `trace` takes: x from the card's low-x edge, y out from the card (negative for the east viewer, positive for the west one), z above the card's bottom."""
        return (eye_street[0] - self.card_x0, eye_street[1] - self.sgn * self.card_y, eye_street[2] - self.card_bottom)

    def card_column_x(self, i, nw, W):
        """The card-frame x of baked column i: column 0 is the viewer's LEFT (the high x on an east card, the low x on a west one)."""
        t = (i + 0.5) / nw * W
        return t if self.west else W - t

    def lamp_xs(self):
        """The two assumed street lamps' x (the gate's stand-ins): 10 m either side of the bay's middle."""
        return (self.mid_x - 10.0, self.mid_x + 10.0)

    def path(self, *a):
        return os.path.join(self.work, *a)


def rita():
    return Ctx("ritas")
