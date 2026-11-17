"""The loft generator for the fictional 1990 small family hatch (n16-9), pure Python.

Written by the lane session, 17 November 2026. It needs no Blender: it works out
the car's twelve cross-sections ("stations") along its length from a handful of
numbers, checks them against the class ranges measured from real cars of the
class (dimensions only), and can draw flat outline views (side, front, rear,
three-quarter) as SVG for a cheap first look before the real P9 renders.

The Blender side (tools/lane/car_loft_blender.py) bridges these stations into
one mesh. That file is UNTESTED: it needs the main session's run on the PC.

Method: production/research/asset-plan/2-VEHICLES.md section 3.3 ("Loft, not
bevelled boxes": about 12 stations, each a half cross-section with shoulder,
inward lean of the glass and sill tuck; one fixed topology so shape keys and
UVs survive every variant). Class ranges: production/research/lane/
HATCH-CLASS-AND-PLATES-2026-11-17.md (eight real cars, read 17 Nov 2026).

Axes: x from the nose (0) to the tail (L), y across (+ is the car's left),
z up from the ground. Metres.
"""
import json
import math
import sys
from dataclasses import dataclass, asdict, field

# Points in every half cross-section, bottom centre to roof centre. Fixed, so
# every station has the same topology (bridge_loops and shape keys need it).
SECTION_POINTS = (
    "keel",        # bottom centreline
    "floor_edge",  # the floor's edge, tucked in from the sill
    "sill",        # sill's outer face
    "flank",       # widest point of the lower body
    "shoulder",    # top of the flank, just below the belt
    "belt",        # the belt line: bottom of the side glass
    "cant",        # top of the side glass (cant rail)
    "roof_edge",   # the roof's outer edge
    "crown",       # roof (or bonnet, or deck) centreline
)

# Class ranges for a 1990 British small family hatch, measured from eight real
# cars (dimensions only; see the research file named in the docstring).
CLASS_RANGES = {
    "length": (3.950, 4.250),
    "width": (1.630, 1.700),
    "height": (1.370, 1.450),
    "wheelbase": (2.430, 2.550),
    "height_over_length": (0.329, 0.370),
    "wheelbase_over_length": (0.600, 0.645),
    # Not measured from the eight cars; the asset plan's own reading (UNVERIFIED).
    "belt_over_height": (0.60, 0.66),
    "glass_over_height": (0.33, 0.40),
}

TRIANGLE_BUDGET = 40000   # production/specs/asset-budgets.json "car"


@dataclass
class HatchParams:
    length: float = 4.08
    width: float = 1.66
    height: float = 1.40
    wheelbase: float = 2.50
    front_overhang: float = 0.80      # nose to front axle
    wheel_radius: float = 0.289       # 175/70 R13
    tyre_width: float = 0.175
    track: float = 1.40
    belt_ratio: float = 0.625         # belt height over overall height
    sill_z: float = 0.30              # bottom of the body at the sills
    keel_z: float = 0.22              # bottom of the floor pan
    nose_top_z: float = 0.70          # bonnet height at the nose
    tail_top_z: float = 0.86          # top of the tail panel under the hatch glass
    screen_base_x: float = 1.22       # foot of the windscreen, from the nose
    screen_rake_deg: float = 34.0     # windscreen angle from horizontal
    hatch_base_from_tail: float = 0.10
    hatch_angle_deg: float = 56.0     # hatch glass angle from horizontal
    glass_inset: float = 0.12         # inward lean of the side glass, each side
    shoulder_in: float = 0.03         # belt set in from the flank
    sill_tuck: float = 0.06           # floor edge tucked in from the sill
    nose_taper: float = 0.86          # half width at the nose tip over full
    tail_taper: float = 0.92          # half width at the tail tip over full
    roof_crown: float = 0.02          # rise of the roof centre over its edge
    deck_crown: float = 0.015         # bonnet and tail deck crown
    arch_clearance: float = 0.045     # arch radius minus wheel radius
    roof_drop: float = 0.0            # the roof falls this much from its front to its back
    subdivision_levels: int = 2

    @property
    def belt_z(self):
        return self.belt_ratio * self.height

    def derived(self):
        """The x positions the outline turns at, from the numbers above."""
        rise = self.height - self.belt_z
        roof_front = self.screen_base_x + rise / math.tan(math.radians(self.screen_rake_deg))
        hatch_base = self.length - self.hatch_base_from_tail
        hatch_rise = self.height - self.roof_drop - self.tail_top_z
        roof_back = hatch_base - hatch_rise / math.tan(math.radians(self.hatch_angle_deg))
        return {
            "front_axle": self.front_overhang,
            "rear_axle": self.front_overhang + self.wheelbase,
            "screen_base": self.screen_base_x,
            "roof_front": roof_front,
            "roof_back": roof_back,
            "hatch_base": hatch_base,
        }


# Not tried in a blind round: the shape the two outline rounds point to (round 1
# read as a saloon, round 2 as an estate; production/lane/P9-OUTLINE-ROUNDS-2026-11-17.md).
# The roof falls toward a more raked hatch that still ends near the tail.
ROUND3_PROPOSAL = {"roof_drop": 0.06, "hatch_angle_deg": 40.0, "hatch_base_from_tail": 0.14,
                   "tail_top_z": 0.84, "nose_top_z": 0.72, "screen_base_x": 1.16}


def top_z(p, x):
    """The side outline's top line at x: bonnet, windscreen, roof, hatch, tail."""
    d = p.derived()
    cowl = p.belt_z
    if x <= d["screen_base"]:
        t = x / d["screen_base"] if d["screen_base"] > 0 else 1.0
        # the bonnet rises from the nose with a slight convex curve
        return p.nose_top_z + (cowl - p.nose_top_z) * math.sin(t * math.pi / 2)
    if x <= d["roof_front"]:
        t = (x - d["screen_base"]) / (d["roof_front"] - d["screen_base"])
        return cowl + (p.height - p.roof_crown - cowl) * t
    roof_top = p.height - p.roof_crown
    if x <= d["roof_back"]:
        t = (x - d["roof_front"]) / max(d["roof_back"] - d["roof_front"], 1e-6)
        return roof_top - p.roof_drop * t * t
    if x <= d["hatch_base"]:
        t = (x - d["roof_back"]) / (d["hatch_base"] - d["roof_back"])
        start = roof_top - p.roof_drop
        return start + (p.tail_top_z - start) * t
    # the short tail deck falls a little to the tail
    t = (x - d["hatch_base"]) / max(p.length - d["hatch_base"], 1e-6)
    return p.tail_top_z - 0.04 * t


def station_list(p):
    """Twelve named stations, sorted along the car (2-VEHICLES.md 3.3)."""
    d = p.derived()
    st = [
        ("nose_tip", 0.0),
        ("bumper_face", 0.06),
        ("headlamp", 0.28),
        ("front_axle", d["front_axle"]),
        ("screen_base", d["screen_base"]),
        ("roof_front", d["roof_front"]),
        ("b_pillar", (d["roof_front"] + d["roof_back"]) / 2),
        ("roof_back", d["roof_back"]),
        ("rear_axle", d["rear_axle"]),
        ("hatch_base", d["hatch_base"]),
        ("tail", p.length - 0.06),
        ("tail_tip", p.length),
    ]
    return sorted(st, key=lambda s: s[1])


def half_width_at(p, x):
    """Plan-view taper: full width in the middle, rounded in at nose and tail."""
    hw = p.width / 2
    nose_len, tail_len = 0.55, 0.45
    if x < nose_len:
        t = x / nose_len
        return hw * (p.nose_taper + (1 - p.nose_taper) * math.sin(t * math.pi / 2))
    if x > p.length - tail_len:
        t = (p.length - x) / tail_len
        return hw * (p.tail_taper + (1 - p.tail_taper) * math.sin(t * math.pi / 2))
    return hw


def section(p, name, x):
    """One half cross-section: 9 (y, z) points, keel to crown, y >= 0."""
    hw = half_width_at(p, x)
    tz = top_z(p, x)
    belt = p.belt_z
    end = name in ("nose_tip", "tail_tip")
    keel = p.keel_z + (0.08 if end else 0.0)
    sill = p.sill_z + (0.06 if end else 0.0)
    glass = tz > belt + 1e-6
    shoulder_z = min(belt - 0.05, tz - 0.05)
    flank_z = sill + 0.55 * (shoulder_z - sill)
    pts = {
        "keel": (0.0, keel),
        "floor_edge": (hw - p.sill_tuck - 0.04, keel),
        "sill": (hw - 0.01, sill),
        "flank": (hw, flank_z),
        "shoulder": (hw - 0.008, shoulder_z),
    }
    if glass:
        frac = (tz - belt) / max(p.height - p.roof_crown - belt, 1e-6)
        belt_y = hw - p.shoulder_in
        cant_y = belt_y - p.glass_inset * frac
        pts["belt"] = (belt_y, belt)
        pts["cant"] = (cant_y, tz - 0.035 * frac)
        pts["roof_edge"] = (cant_y - 0.03 * frac, tz)
        pts["crown"] = (0.0, tz + p.roof_crown * frac)
    else:
        # no glass here: the belt points lie on the bonnet or deck, same count
        deck = min(tz, belt)
        y0 = hw - p.shoulder_in
        pts["belt"] = (y0, deck - 0.01)
        pts["cant"] = (y0 * 0.70, deck)
        pts["roof_edge"] = (y0 * 0.35, deck + p.deck_crown * 0.7)
        pts["crown"] = (0.0, deck + p.deck_crown)
    return [pts[k] for k in SECTION_POINTS], glass


def build(p):
    """All stations with their half sections; the data the Blender side bridges."""
    out = []
    for name, x in station_list(p):
        pts, glass = section(p, name, x)
        out.append({"name": name, "x": round(x, 5), "glass": glass,
                    "half_section": [(round(y, 5), round(z, 5)) for y, z in pts]})
    return out


def full_loop(st):
    """A station's closed loop, mirrored: right side bottom to top, then left
    side top to bottom, without doubling the centreline points."""
    half = st["half_section"]
    right = [(st["x"], -y, z) for y, z in half]
    left = [(st["x"], y, z) for y, z in reversed(half[1:-1])]
    return right + left


def triangle_estimate(p, n_stations=12):
    """Body triangles after subdivision (quads x 4 per level x 2 triangles),
    plus the two end caps, plus wheels and details at a fixed allowance."""
    loop = 2 * (len(SECTION_POINTS) - 1)
    quads = (n_stations - 1) * loop + 2 * (loop // 2)
    body = quads * (4 ** p.subdivision_levels) * 2
    wheels_and_details = 4 * 1800 + 3500
    return body + wheels_and_details


def measure(p, stations=None):
    stations = stations or build(p)
    ys = [y for s in stations for y, _ in s["half_section"]]
    zs = [z for s in stations for _, z in s["half_section"]]
    xs = [s["x"] for s in stations]
    length = max(xs) - min(xs)
    width = 2 * max(ys)
    height = max(max(zs), 0.0)
    return {
        "length": round(length, 4),
        "width": round(width, 4),
        "height": round(height, 4),
        "wheelbase": round(p.wheelbase, 4),
        "height_over_length": round(height / length, 4),
        "wheelbase_over_length": round(p.wheelbase / length, 4),
        "belt_over_height": round(p.belt_z / height, 4),
        "glass_over_height": round((height - p.belt_z) / height, 4),
        "triangles_estimate": triangle_estimate(p, len(stations)),
    }


def check(p):
    """Every failure as a plain sentence; an empty list means it passes."""
    fails = []
    st = build(p)
    m = measure(p, st)
    for key, (lo, hi) in CLASS_RANGES.items():
        if not (lo - 1e-9 <= m[key] <= hi + 1e-9):
            fails.append("%s %.3f outside the class range %.3f to %.3f" % (key, m[key], lo, hi))
    xs = [s["x"] for s in st]
    if any(b <= a for a, b in zip(xs, xs[1:])):
        fails.append("stations not in order along the car: %s" % [s["name"] for s in st])
    d = p.derived()
    if not d["screen_base"] < d["roof_front"] < d["roof_back"] < d["hatch_base"]:
        fails.append("glasshouse turns out of order: %s" % d)
    arch = p.wheel_radius + p.arch_clearance
    if d["front_axle"] - arch < 0.12:
        fails.append("front arch cuts into the bumper face")
    if p.length - d["rear_axle"] - arch < 0.12:
        fails.append("rear arch cuts into the tail")
    if 2 * p.wheel_radius + 0.0 > p.belt_z:
        fails.append("wheels taller than the belt")
    if arch * 2 > p.belt_z - 0.02 + p.wheel_radius:
        fails.append("arch reaches the belt line")
    if p.track / 2 + p.tyre_width / 2 > p.width / 2 + 0.005:
        fails.append("tyres stick out of the body")
    if p.track / 2 + p.tyre_width / 2 < p.width / 2 - 0.10:
        fails.append("wheels tucked too far in (looks narrow-tracked)")
    for s in st:
        hs = s["half_section"]
        if any(y < -1e-9 for y, _ in hs):
            fails.append("%s: a point crosses the centreline" % s["name"])
        if hs[0][0] != 0.0 or hs[-1][0] != 0.0:
            fails.append("%s: keel or crown off the centreline" % s["name"])
        if not all(b[1] >= a[1] - 1e-9 for a, b in zip(hs, hs[1:])):
            fails.append("%s: section folds back on itself (z falls)" % s["name"])
    if m["triangles_estimate"] > TRIANGLE_BUDGET:
        fails.append("triangle estimate %d over the budget %d" % (m["triangles_estimate"], TRIANGLE_BUDGET))
    return fails


# ---------- flat outline views for a first look (not the P9 renders) ----------

def _svg(paths, w, h, title):
    body = "\n".join(paths)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
            '<title>%s</title><rect width="100%%" height="100%%" fill="#ffffff"/>\n%s\n</svg>\n'
            % (w, h, w, h, title, body))


def _poly(pts, fill, stroke="none"):
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (
        " ".join("%.1f,%.1f" % q for q in pts), fill, stroke)


def side_view(p, scale=200):
    st = build(p)
    w, h = int(p.length * scale) + 80, int(p.height * scale) + 80
    X = lambda x: 40 + x * scale
    Z = lambda z: h - 40 - z * scale
    top = [(X(s["x"]), Z(s["half_section"][-1][1])) for s in st]
    # densify the top line between stations
    dense = [(X(x / 100 * p.length), Z(top_z(p, x / 100 * p.length))) for x in range(101)]
    bottom = [(X(s["x"]), Z(s["half_section"][2][1])) for s in reversed(st)]
    paths = [_poly(dense + bottom, "#000000")]
    d = p.derived()
    arch = p.wheel_radius + p.arch_clearance
    for ax in (d["front_axle"], d["rear_axle"]):
        paths.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff"/>' % (X(ax), Z(p.wheel_radius), arch * scale))
        paths.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#000000"/>' % (X(ax), Z(p.wheel_radius), p.wheel_radius * scale))
    paths.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="#888" stroke-width="2"/>' % (Z(0), w, Z(0)))
    return _svg(paths, w, h, "side")


def end_view(p, which="front", scale=200):
    st = build(p)
    w, h = int(p.width * scale) + 80, int(p.height * scale) + 80
    Y = lambda y: w / 2 + y * scale
    Z = lambda z: h - 40 - z * scale
    paths = []
    for s in st:
        loop = full_loop(s)
        paths.append(_poly([(Y(y), Z(z)) for _, y, z in loop], "#000000"))
    for side in (-1, 1):
        yc = side * p.track / 2
        paths.append(_poly([(Y(yc - p.tyre_width / 2), Z(0)), (Y(yc + p.tyre_width / 2), Z(0)),
                            (Y(yc + p.tyre_width / 2), Z(2 * p.wheel_radius)),
                            (Y(yc - p.tyre_width / 2), Z(2 * p.wheel_radius))], "#000000"))
    paths.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="#888" stroke-width="2"/>' % (Z(0), w, Z(0)))
    return _svg(paths, w, h, which)


def quads(p):
    """The body's quads, mirrored, as (x, y, z) corner lists, with a glass flag."""
    st = build(p)
    loops = [full_loop(s) for s in st]
    n = len(loops[0])
    out = []
    for i in range(len(loops) - 1):
        a, b = loops[i], loops[i + 1]
        glass_pair = st[i]["glass"] and st[i + 1]["glass"]
        for j in range(n):
            k = (j + 1) % n
            # point indices 5..7 on either side are the glass band (belt to roof edge)
            jj = j if j < len(SECTION_POINTS) else n - j
            kk = k if k < len(SECTION_POINTS) else n - k
            # side glass: the belt-to-cant band where both stations have glass
            g = glass_pair and {jj, kk} == {5, 6}
            # windscreen and hatch glass: the top faces where the outline is steep
            dz = abs(st[i + 1]["half_section"][-1][1] - st[i]["half_section"][-1][1])
            dx = max(st[i + 1]["x"] - st[i]["x"], 1e-6)
            if dz / dx > 0.4 and min(jj, kk) >= 6 and (st[i]["glass"] or st[i + 1]["glass"]):
                g = True
            out.append(([a[j], a[k], b[k], b[j]], g))
    return out


def three_quarter_view(p, scale=150, yaw_deg=35.0, pitch_deg=-12.0):
    """Flat-shaded three-quarter view (front left), painter's order, no texture."""
    yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
    cx = p.length / 2

    def proj(v):
        x, y, z = v[0] - cx, v[1], v[2]
        # turn about z so the front-left corner faces the viewer, then tilt
        u = x * math.cos(yaw) + y * math.sin(yaw)
        dpt = -x * math.sin(yaw) + y * math.cos(yaw)
        vz = z * math.cos(pitch) - dpt * math.sin(pitch)
        depth = dpt * math.cos(pitch) + z * math.sin(pitch)
        return u, vz, depth
    light = (-0.5, -0.4, 0.75)
    ln = math.sqrt(sum(c * c for c in light))
    light = tuple(c / ln for c in light)
    faces = []
    for corners, g in quads(p):
        pr = [proj(c) for c in corners]
        a, b, c = corners[0], corners[1], corners[2]
        u = [b[i] - a[i] for i in range(3)]
        v = [c[i] - a[i] for i in range(3)]
        nrm = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
        nl = math.sqrt(sum(q * q for q in nrm)) or 1.0
        nrm = [q / nl for q in nrm]
        shade = abs(sum(nrm[i] * light[i] for i in range(3)))
        base = 40 if g else 150
        val = int(base * (0.35 + 0.65 * shade))
        faces.append((sum(q[2] for q in pr) / 4, [(q[0], q[1]) for q in pr], val))
    faces.sort(key=lambda f: -f[0])
    us = [q[0] for f in faces for q in f[1]]
    vs = [q[1] for f in faces for q in f[1]]
    w = int((max(us) - min(us)) * scale) + 80
    h = int((max(vs) - min(vs) + 0.3) * scale) + 80
    U = lambda u: 40 + (u - min(us)) * scale
    V = lambda v: h - 40 - (v - min(vs) + 0.3) * scale
    far, near = [], []
    d = p.derived()
    for ax in (d["front_axle"], d["rear_axle"]):
        for side in (-1, 1):
            u, vz, dep = proj((ax, side * p.track / 2, p.wheel_radius))
            e = '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#111"/>' % (
                U(u), V(vz), p.wheel_radius * scale * abs(math.sin(yaw)) + 4, p.wheel_radius * scale)
            # smaller depth is nearer the viewer (faces are drawn largest depth first)
            (near if dep < 0 else far).append(e)
    paths = list(far)
    for _, pts, val in faces:
        col = "#%02x%02x%02x" % (val, val, val)
        paths.append(_poly([(U(a), V(b)) for a, b in pts], col, col))
    paths += near
    return _svg(paths, w, h, "three-quarter")


def write_views(p, folder):
    import os
    os.makedirs(folder, exist_ok=True)
    views = {"side": side_view(p), "front": end_view(p, "front"), "rear": end_view(p, "rear"),
             "three-quarter": three_quarter_view(p)}
    for k, svg in views.items():
        with open(os.path.join(folder, "hatch-%s.svg" % k), "w") as f:
            f.write(svg)
    return sorted(views)


def main(argv):
    p = HatchParams()
    if "--round3" in argv:
        p = HatchParams(**ROUND3_PROPOSAL)
    if "--json" in argv:
        print(json.dumps({"params": asdict(p), "stations": build(p)}, indent=1))
        return 0
    if "--views" in argv:
        folder = argv[argv.index("--views") + 1]
        print("views:", write_views(p, folder))
    m = measure(p)
    fails = check(p)
    print(json.dumps(m, indent=1))
    print("PASS" if not fails else "FAIL:\n- " + "\n- ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
