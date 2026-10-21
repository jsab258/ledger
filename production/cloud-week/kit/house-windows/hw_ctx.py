"""The street's numbers for the gate of the house windows: where each window stands, the review cameras, the angles. Read from target.json (and the scene file for the two street views).

Written 14 October from the shop kit's sw_ctx.py (copied that day; the shop context's Ctx class stays there, this one is the street's): same conventions, no shop in it.

Frames. STREET: x along (0 at the south end, + north), y across (east +), z above the road's crown; the footway is crown + 0.10; the eye is 1.60 above the footway = 1.70 above the crown. BLENDER: the street
as Unreal draws it is left-handed (the viewer on the west footway has the HIGH street x on his left), Blender is right-handed, so the gate's scene is the street with x negated: X_b = -x, Y_b = y, Z_b = z.
A kit piece's own x is the viewer's right (target 8); on an east wall the viewer looks along +y, his right is +X_b, so the piece goes on with no turn; on a west wall it is turned 180 degrees about z.
"""
import math

import hw_t as T

WALL_E = 5.125                 # the east frontage's brick face (y)
WALL_W = -5.125
WALL_T = 0.215
EYE_Z = 1.70                   # above the crown
FOOT = 0.10
KERB_Y = 3.505                 # the far pavement's kerb edge (the review cameras stand here)
CARD_BEHIND = 0.270


def blender_pt(p):
    return (-p[0], p[1], p[2])


def side_of(site):
    return site["side"]        # +1 east, -1 west


def wall_y(site):
    return WALL_E if site["side"] > 0 else WALL_W


def placement(site):
    """(X_b, Y_b, Z_b, turn_deg) of the kit piece: the opening's bottom-edge centre on the brick face."""
    return (-site["x_centre"], wall_y(site), site["sill_z_above_crown"], 0.0 if site["side"] > 0 else 180.0)


def eye_in_front(site, eye):
    """True when the eye is on the street side of the window's wall."""
    return (eye[1] < wall_y(site)) if site["side"] > 0 else (eye[1] > wall_y(site))


def angle_from_wall_deg(site, eye):
    """The angle at which the window's centre is seen from the wall's plane (degrees): 90 square on, small along the wall. From the scene's geometry."""
    cx = site["x_centre"]
    cz = site["sill_z_above_crown"] + 0.838
    dx = cx - eye[0]
    dy = abs(wall_y(site) - eye[1])
    dz = cz - eye[2]
    # the angle between the line of sight and the wall plane (the wall plane contains x and z)
    horiz = math.hypot(dx, dz)
    return math.degrees(math.atan2(dy, horiz)) if horiz > 1e-9 else 90.0


def card_plane_y(site):
    return wall_y(site) + site["side"] * CARD_BEHIND


# ------------------------------------------------------------------------------------------------------------------ the cameras
def view_cameras():
    """The review views of the street: the Hook sheet's camera (cam_hook), the scene file's cam_A (the brief's 'Hook view': it stands on the east footway at x 4 and looks along the street, 1.1 m from the
    parade's wall), and the reverse view. Eyes in the street frame; yaw (degrees from +x toward the east), pitch (degrees, positive DOWN), the vertical field."""
    return {
        "cam_hook": {"eye": (-3.0, -1.6, 2.2), "yaw": 20.4, "pitch": -3.4, "vfov": 46.0, "note": "vignette-scene.json cam_hook: the approved Hook sheet's camera (west carriageway, 20.4 degrees to its right, 3.4 degrees up)"},
        "cam_A": {"eye": (4.0, 4.0, FOOT + 1.6), "yaw": 0.0, "pitch": 4.0, "vfov": 60.0, "note": "vignette-scene.json cam_A: the east footway, 0.875 m back from the kerb, looking up the street (the target review's 'Hook camera')"},
        "cam_reverse": {"eye": (38.0, 1.6, 1.7), "yaw": 200.4, "pitch": -3.4, "vfov": 46.0, "note": "vignette-scene.json cam_reverse: the far end of the level street, east carriageway, looking back toward the quay, the parade on its left"},
    }


def h_camera(name, site):
    """A target review camera (section 3.3 / 9) for a window: eye 1.60 above the footway, the window's centre as the aim; the along cameras stand on the quay-end side of the window."""
    g = T.target()["gate"]["cameras"][name]
    kind, ang, dist = g["spec"]
    s = site["side"]
    wy = wall_y(site)
    cx, cz = site["x_centre"], site["sill_z_above_crown"] + 0.838
    if kind == "across":
        ey = -s * KERB_Y
        d = abs(wy - ey)
        ex = cx - (math.tan(math.radians(ang)) * d if ang else 0.0)
    elif kind == "along":
        ey = wy - s * dist
        ex = cx - dist / math.tan(math.radians(ang))
    else:                                      # under
        ey = wy - s * dist
        ex = cx
    return {"eye": (ex, ey, EYE_Z), "aim": (cx, wy, cz), "vfov": g["vfov_deg"], "note": g["what"]}
