"""Street furniture check for Quay Street (lane, 17 Nov 2026).

Reads what the street really emits and what the built models really measure,
and checks both against the street furniture target
(production/research/phase2-plan/TARGET-STREET-FURNITURE-2026-11-17.md, rows S1 to S13).
Pure Python, no Blender, no Unreal: a screen for the main session before any
furniture rebuild, never a pass on its own (pieces pass only in the packaged walk).

Inputs (read only):
  production/specs/vignette-pieces.json   every emitted piece, centre and size
  production/assets/street/clutter/*.glb   the script-built furniture models
Frame: x along the street 0 to 48 m, z across (east +), kerb faces at +-3.0 m,
footway 2.0 m, so the building line is at +-5.0 m; y up.

Usage: python tools/lane/furniture_check.py [--root REPO] [--json]
Exit 0 when nothing FAILs (MISSING, DIFFERS, INFO and UNMEASURED do not fail), 1 otherwise.
Also imports tools/art-recipes/terrace-front.py read-only for clutter_placements and NAME_PLATE_AT.
"""
import argparse
import json
import math
import os
import struct
import sys

KERB_FACE_M = 3.0
FOOTWAY_M = 2.0
BUILDING_LINE_M = KERB_FACE_M + FOOTWAY_M
# A walking person's width, the AI tester's own figure (vignette-scene.json E8 note, 29 Sep).
WALK_CLEAR_M = 0.68

# The target's numbers, each with its row. Where the lane's research of 17 Nov
# corrects the target, the correction is a separate key so the main session can
# choose (production/research/lane/FURNITURE-SPECS-2026-11-17.md).
TARGET = {
    "lamps": {"row": "S1", "x_side": [(8.0, "east"), (18.0, "west"), (28.0, "east"), (38.0, "west")],
              "axis_from_centre_m": 3.725, "tol_m": 0.02},
    "bollard": {"row": "S6", "height_m": 1.082, "tol_frac": 0.05, "x": [20.7, 24.3], "side": "west",
                "centre_from_kerb_m": 0.5},
    "kiosk": {"row": "S7", "plan_m": 0.890, "height_m": 2.192, "tol_m": 0.03, "x": 16.5, "side": "east",
              "centre_from_centreline_m": 3.675},
    "pillar_box": {"row": "S8", "height_m": 1.500, "body_m": 0.489, "tol_frac": 0.05, "x": 27.0, "side": "east"},
    "pillar_box_research": {"row": "S8 (lane research)", "height_m": 1.346, "body_m_type_b": 0.381,
                            "body_m_type_k": 0.483},
    "litter_bin": {"row": "S5", "max_count": 3, "rim_m": 1.050, "post_m": 0.0761, "tol_frac": 0.08},
    "guard_rail": {"row": "S11", "panels": 1, "height_m": 1.0, "min_infill_bars": 17,
                   "post_axis_from_kerb_m": 0.375, "tol_m": 0.03},
    "gully": {"row": "S12", "plan_m": (0.440, 0.290), "tol_m": 0.02, "x": 12.0, "side": "east"},
    "name_plate": {"row": "S9", "count": 1, "size_m": (0.980, 0.200)},
    "bus_stop": {"row": "S10", "count": 1, "x": 46.0, "side": "west"},
}

# Which held asset the street recipe swaps for which script-built model
# (tools/art-recipes/terrace-front.py CLUTTER_FOR_HELD, read 17 Nov).
CLUTTER_FOR_HELD = {"decorative_bollard_02": "bollard", "swing_bin": "litter-bin",
                    "outdoor_bin": "litter-bin", "pavement_sign": "a-board"}
# The recipe's own column clearance for bins (terrace-front.py CLUTTER_CLEAR_OF_COLUMN_M).
CLEAR_OF_COLUMN_M = 0.9


# ---------------------------------------------------------------- glb bounds
def _quat_rotate(q, v):
    x, y, z, w = q
    vx, vy, vz = v
    # v' = v + 2w(q x v) + 2 q x (q x v)
    cx, cy, cz = y * vz - z * vy, z * vx - x * vz, x * vy - y * vx
    cx2, cy2, cz2 = y * cz - z * cy, z * cx - x * cz, x * cy - y * cx
    return (vx + 2 * (w * cx + cx2), vy + 2 * (w * cy + cy2), vz + 2 * (w * cz + cz2))


def _node_matrix(node):
    """4x4 row-major matrix of a glTF node (matrix, or T*R*S)."""
    if "matrix" in node:
        m = node["matrix"]  # column-major
        return [[m[c * 4 + r] for c in range(4)] for r in range(4)]
    t = node.get("translation", [0, 0, 0])
    q = node.get("rotation", [0, 0, 0, 1])
    s = node.get("scale", [1, 1, 1])
    cols = []
    for i, axis in enumerate(((1, 0, 0), (0, 1, 0), (0, 0, 1))):
        r = _quat_rotate(q, axis)
        cols.append([r[0] * s[i], r[1] * s[i], r[2] * s[i]])
    return [[cols[0][0], cols[1][0], cols[2][0], t[0]],
            [cols[0][1], cols[1][1], cols[2][1], t[1]],
            [cols[0][2], cols[1][2], cols[2][2], t[2]],
            [0, 0, 0, 1]]


def _mul(a, b):
    return [[sum(a[r][k] * b[k][c] for k in range(4)) for c in range(4)] for r in range(4)]


def _apply(m, p):
    return tuple(m[r][0] * p[0] + m[r][1] * p[1] + m[r][2] * p[2] + m[r][3] for r in range(3))


def read_glb_json(path):
    with open(path, "rb") as fh:
        head = fh.read(12)
        magic, _ver, _length = struct.unpack("<4sII", head)
        if magic != b"glTF":
            raise ValueError("not a glb: %s" % path)
        clen, ctype = struct.unpack("<II", fh.read(8))
        if ctype != 0x4E4F534A:
            raise ValueError("first chunk is not JSON: %s" % path)
        return json.loads(fh.read(clen).decode("utf-8"))


def gltf_bounds(gltf, mesh_filter=None):
    """World-space (min, max) of every POSITION accessor's box corners under the
    default scene's node tree. Uses accessor min/max (required by glTF 2.0 for
    POSITION), so no buffer is read. mesh_filter(name) may exclude meshes."""
    lo = [math.inf] * 3
    hi = [-math.inf] * 3
    nodes = gltf.get("nodes", [])
    scenes = gltf.get("scenes", [{"nodes": list(range(len(nodes)))}])
    roots = scenes[gltf.get("scene", 0)].get("nodes", [])
    ident = [[1 if r == c else 0 for c in range(4)] for r in range(4)]
    stack = [(i, ident) for i in roots]
    while stack:
        i, parent = stack.pop()
        node = nodes[i]
        m = _mul(parent, _node_matrix(node))
        if "mesh" in node:
            mesh = gltf["meshes"][node["mesh"]]
            if mesh_filter is None or mesh_filter(mesh.get("name", "")):
                for prim in mesh.get("primitives", []):
                    acc = gltf["accessors"][prim["attributes"]["POSITION"]]
                    a, b = acc["min"], acc["max"]
                    for cx in (a[0], b[0]):
                        for cy in (a[1], b[1]):
                            for cz in (a[2], b[2]):
                                p = _apply(m, (cx, cy, cz))
                                for k in range(3):
                                    lo[k] = min(lo[k], p[k])
                                    hi[k] = max(hi[k], p[k])
        for c in node.get("children", []):
            stack.append((c, m))
    if lo[0] == math.inf:
        return None
    return tuple(lo), tuple(hi)


def model_size(path):
    """(x, y_up, z) size in metres of a glb, or None if it cannot be read."""
    try:
        b = gltf_bounds(read_glb_json(path))
    except (OSError, ValueError, KeyError, IndexError, struct.error):
        return None
    if b is None:
        return None
    lo, hi = b
    return tuple(round(hi[k] - lo[k], 4) for k in range(3))


# ---------------------------------------------------------------- checks
def _side(z):
    return "east" if z > 0 else "west"


def _line(row, what, verdict, found, want, note=""):
    return {"row": row, "what": what, "verdict": verdict, "found": found, "want": want, "note": note}


def clear_walk_m(z_centre, depth):
    """The wider of the two gaps a walker has past a piece on the footway."""
    near = abs(z_centre) - depth / 2.0
    front = near - KERB_FACE_M
    back = BUILDING_LINE_M - (abs(z_centre) + depth / 2.0)
    return round(max(front, back), 3)



# Pieces that stand on the footway but are swapped or removed by the recipe.
HELD_PROPS_OFF_STREET = ("traffic_cone_01", "traffic_cone_02")
# A model the recipe turns a quarter (terrace-front.py CLUTTER_EXTRA_TURN): its x size runs across the street.
QUARTER_TURNED = ("a-board",)


def footed(pieces, drawn, models):
    """[(label, x0, x1, z0, z1)] of every footed thing on a footway: the
    street's own emitted pieces (column bases, kiosk plinth, pillar box, rail
    posts, dustbins), held props the recipe keeps, and the recipe's drawn
    clutter at its model's measured size. Across-street depth of a drawn model
    is its z size (x size when quarter-turned): an approximation of its yaw."""
    out = []
    replaced = set(CLUTTER_FOR_HELD) | set(HELD_PROPS_OFF_STREET)
    drawn_names = {d[0] for d in drawn}
    for p in pieces:
        n = p["name"]
        if n.endswith("_lid"):
            continue
        own = n.startswith("column") and n.endswith("_base") or n in ("kiosk_plinth", "pillarbox_body") \
            or n.startswith(("rail_post", "dustbin"))
        held = n.startswith("prop_") and p.get("asset") not in replaced \
            and (p["y_m"] - p["sy_m"] / 2.0) < 0.3 and p.get("bom") != "A7_gully_grate"
        if drawn and n.startswith("dustbin") and "dustbin" in drawn_names:
            continue  # drawn below at the model's size
        if drawn and n in ("kiosk_plinth", "pillarbox_body"):
            continue
        if not (own or held):
            continue
        if not (KERB_FACE_M <= abs(p["z_m"]) <= BUILDING_LINE_M):
            continue
        out.append((n, p["x_m"] - p["sx_m"] / 2, p["x_m"] + p["sx_m"] / 2,
                    p["z_m"] - p["sz_m"] / 2, p["z_m"] + p["sz_m"] / 2))
    for model, x, z, _note in drawn:
        size = models.get(model)
        if size is None or not (KERB_FACE_M <= abs(z) <= BUILDING_LINE_M):
            continue
        along, across = (size[2], size[0]) if model in QUARTER_TURNED else (size[0], size[2])
        out.append(("%s (drawn)" % model, x - along / 2, x + along / 2, z - across / 2, z + across / 2))
    return out


def walker_gaps(items):
    """For each footed thing, the widest free band across the footway left by
    it and everything overlapping it along the street on the same side."""
    rows = []
    for label, x0, x1, z0, z1 in items:
        sign = 1 if (z0 + z1) > 0 else -1
        group = [(a0, a1, b0, b1) for _l, a0, a1, b0, b1 in items
                 if a0 < x1 and a1 > x0 and ((b0 + b1) > 0) == (sign > 0)]
        spans = sorted((max(KERB_FACE_M, min(abs(b0), abs(b1))), min(BUILDING_LINE_M, max(abs(b0), abs(b1))))
                       for _a0, _a1, b0, b1 in group)
        best, edge = 0.0, KERB_FACE_M
        for lo, hi in spans:
            best = max(best, lo - edge)
            edge = max(edge, hi)
        best = round(max(best, BUILDING_LINE_M - edge), 3)
        rows.append(_line("W", "walker's gap at %s, x %.2f" % (label, (x0 + x1) / 2),
                          "PASS" if best >= WALK_CLEAR_M else "FAIL", best, ">= %.2f" % WALK_CLEAR_M,
                          "with %d overlapping" % (len(group) - 1) if len(group) > 1 else ""))
    return rows


def check(pieces, models, drawn=(), name_plate=None):
    """pieces: list of piece dicts (vignette-pieces.json 'pieces');
    models: {name: (sx, sy_up, sz) or None} of the clutter glbs;
    drawn: [(model, x, z, note)] from the recipe's clutter_placements (what the
    street really draws in place of the held props); name_plate: the recipe's
    NAME_PLATE_AT (x0, x1, y0, y1) or None.
    Returns a list of result lines."""
    out = []
    by_name = {p["name"]: p for p in pieces}

    # S1 lamps
    t = TARGET["lamps"]
    cols = sorted((p for p in pieces if p["name"].startswith("column") and p["name"].endswith("_base")),
                  key=lambda p: p["x_m"])
    found = [(p["x_m"], _side(p["z_m"]), abs(p["z_m"])) for p in cols]
    ok = (len(found) == len(t["x_side"]) and
          all(abs(f[0] - w[0]) < 1e-6 and f[1] == w[1] and abs(f[2] - t["axis_from_centre_m"]) <= t["tol_m"]
              for f, w in zip(found, t["x_side"])))
    out.append(_line(t["row"], "lamp columns: four, 10 m staggered, axis 3.725 m", "PASS" if ok else "FAIL",
                     found, t["x_side"]))

    # the walker's gap: every footed thing the street draws on a footway, pieces
    # that overlap along the street taken together
    for row in walker_gaps(footed(pieces, drawn, models)):
        out.append(row)

    # S5 litter bins (held bins the recipe swaps for the litter-bin model)
    t = TARGET["litter_bin"]
    bins = [p for p in pieces if p.get("asset") in ("swing_bin", "outdoor_bin")]
    drawn_bins = [d for d in drawn if d[0] == "litter-bin"]
    places = ", ".join("%.1f %s" % (d[1], _side(d[2])) for d in drawn_bins) if drawn_bins else \
        ", ".join("%.1f %s" % (p["x_m"], _side(p["z_m"])) for p in bins)
    out.append(_line(t["row"], "public litter bins on 48 m", "PASS" if len(bins) <= t["max_count"] else "FAIL",
                     len(bins), "<= %d" % t["max_count"],
                     "places as drawn: " + places + "; the litter-bins target asks 6.6 E and 35.2 E (open question 1)"))
    size = models.get("litter-bin")
    if size is None:
        out.append(_line(t["row"], "litter bin model height (post top)", "UNMEASURED", None, 1.255))
    else:
        out.append(_line(t["row"], "litter bin model overall height (target post 1.255 m, rim 1.050 m)",
                         "PASS" if abs(size[1] - 1.255) <= 1.255 * t["tol_frac"] else "FAIL", size[1], 1.255,
                         "rim height needs the mesh itself; overall height only"))

    # S6 bollards
    t = TARGET["bollard"]
    bol = [p for p in pieces if p.get("asset") == "decorative_bollard_02"]
    pos_ok = sorted(round(p["x_m"], 2) for p in bol) == t["x"] and all(_side(p["z_m"]) == t["side"] for p in bol)
    out.append(_line(t["row"], "bollards at the yard mouth only", "PASS" if pos_ok else "FAIL",
                     [(p["x_m"], _side(p["z_m"])) for p in bol], (t["x"], t["side"])))
    size = models.get("bollard")
    if size is None:
        out.append(_line(t["row"], "bollard model height", "UNMEASURED", None, t["height_m"]))
    else:
        h = size[1]
        out.append(_line(t["row"], "bollard model height", "PASS" if abs(h - t["height_m"]) <= t["height_m"] * t["tol_frac"]
                         else "FAIL", h, t["height_m"], "the scene's held stand-in is 1.008 m; the street draws bollard.glb"))

    # S7 kiosk
    t = TARGET["kiosk"]
    k = by_name.get("kiosk_plinth")
    if k is None:
        out.append(_line(t["row"], "kiosk place", "MISSING", None, (t["x"], t["side"])))
    else:
        ok = abs(k["x_m"] - t["x"]) < 1e-6 and _side(k["z_m"]) == t["side"] and \
            abs(abs(k["z_m"]) - t["centre_from_centreline_m"]) <= 0.01
        out.append(_line(t["row"], "kiosk place", "PASS" if ok else "FAIL", (k["x_m"], k["z_m"]),
                         (t["x"], t["centre_from_centreline_m"])))
    size = models.get("kx100-kiosk")
    if size is None:
        out.append(_line(t["row"], "kiosk model size", "UNMEASURED", None, (t["plan_m"], t["height_m"])))
    else:
        plan = max(size[0], size[2])
        ok = abs(plan - t["plan_m"]) <= t["tol_m"] and abs(size[1] - t["height_m"]) <= t["tol_m"]
        out.append(_line(t["row"], "kiosk model plan and height", "PASS" if ok else "FAIL",
                         (round(plan, 3), size[1]), (t["plan_m"], t["height_m"]),
                         "plan is the widest of x and z; a lid skirt can add a few mm"))

    # S8 pillar box
    t = TARGET["pillar_box"]
    r = TARGET["pillar_box_research"]
    size = models.get("pillar-box")
    if size is None:
        out.append(_line(t["row"], "pillar box model", "UNMEASURED", None, (t["height_m"], t["body_m"])))
    else:
        h, body = size[1], min(size[0], size[2])
        ok_t = abs(h - t["height_m"]) <= t["height_m"] * t["tol_frac"]
        out.append(_line(t["row"], "pillar box model height against the target", "PASS" if ok_t else "FAIL",
                         h, t["height_m"]))
        ok_r = abs(h - r["height_m"]) <= r["height_m"] * t["tol_frac"]
        out.append(_line(r["row"], "pillar box model height against the Type B or K research (about 1.346 m)",
                         "PASS" if ok_r else "DIFFERS", h, r["height_m"],
                         "advisory: the target and the research disagree; the main session picks one"))
        out.append(_line(t["row"], "pillar box model footprint, cap included (body itself needs the mesh)", "INFO", body,
                         {"target": t["body_m"], "type_b": r["body_m_type_b"], "type_k": r["body_m_type_k"]}))

    # S11 guard rail
    t = TARGET["guard_rail"]
    posts = sorted((p for p in pieces if p["name"].startswith("rail_post")), key=lambda p: p["x_m"])
    infill = [p for p in pieces if p["name"].startswith("rail_inf")]
    if not posts:
        out.append(_line(t["row"], "guard rail", "MISSING", None, "1 panel"))
    else:
        panels = len(posts) - 1
        axis = abs(posts[0]["z_m"]) - KERB_FACE_M
        out.append(_line(t["row"], "guard rail panels", "PASS" if panels == t["panels"] else "FAIL", panels, t["panels"]))
        out.append(_line(t["row"], "guard rail post axis from the kerb face",
                         "PASS" if abs(axis - t["post_axis_from_kerb_m"]) <= t["tol_m"] else "FAIL",
                         round(axis, 3), t["post_axis_from_kerb_m"]))
        per_panel = len(infill) / max(panels, 1)
        out.append(_line(t["row"], "guard rail infill bars per panel (tube rail to be replaced)",
                         "PASS" if per_panel >= t["min_infill_bars"] else "FAIL", per_panel, t["min_infill_bars"]))

    # S12 gully grate
    t = TARGET["gully"]
    g = [p for p in pieces if p.get("bom") == "A7_gully_grate"]
    if not g:
        out.append(_line(t["row"], "gully grate", "MISSING", None, t["plan_m"]))
    else:
        p = g[0]
        plan = tuple(sorted((p["sx_m"], p["sz_m"]), reverse=True))
        ok = abs(plan[0] - t["plan_m"][0]) <= t["tol_m"] and abs(plan[1] - t["plan_m"][1]) <= t["tol_m"]
        out.append(_line(t["row"], "gully grate plan", "PASS" if ok else "FAIL", tuple(round(v, 3) for v in plan),
                         t["plan_m"], "lane research: 440 x 290 matches no UK size found; 430 x 370 or 450 x 450 are common"))

    # S9, S10: not yet in the street
    t = TARGET["name_plate"]
    if name_plate is not None:
        x0, x1, z0, z1 = name_plate
        w, h = round(x1 - x0, 3), round(z1 - z0, 3)
        ok = abs(w - t["size_m"][0]) <= 0.02 and abs(h - t["size_m"][1]) <= 0.02
        out.append(_line(t["row"], "street name plate (drawn by the recipe, NAME_PLATE_AT)", "PASS" if ok else "DIFFERS",
                         (w, h, round((z0 + z1) / 2, 3)), (t["size_m"][0], t["size_m"][1], 2.63),
                         "advisory: present; size differs from the target, the main session picks one"))
    for key, what in (("name_plate", "street name plate"), ("bus_stop", "bus stop")):
        if key == "name_plate" and name_plate is not None:
            continue
        t = TARGET[key]
        hits = [p for p in pieces if key.replace("_", "") in p["name"].replace("_", "")]
        out.append(_line(t["row"], what, "PASS" if len(hits) == t["count"] else "MISSING", len(hits), t["count"]))
    return out


def load(root):
    with open(os.path.join(root, "production/specs/vignette-pieces.json"), encoding="utf-8") as fh:
        pieces = json.load(fh)["pieces"]
    cdir = os.path.join(root, "production/assets/street/clutter")
    models = {}
    for name in ("bollard", "litter-bin", "kx100-kiosk", "pillar-box", "grit-bin", "dustbin", "a-board",
                 "milk-crates"):
        models[name] = model_size(os.path.join(cdir, name + ".glb"))
    drawn, name_plate = [], None
    recipe = recipe_module(root)
    if recipe is not None:
        drawn, _notes = recipe.clutter_placements(root)
        name_plate = getattr(recipe, "NAME_PLATE_AT", None)
    return pieces, models, drawn, name_plate


def recipe_module(root):
    """The street recipe, imported read-only for its pure placement function;
    None when it cannot be imported here."""
    import importlib.util
    path = os.path.join(root, "tools/art-recipes/terrace-front.py")
    try:
        spec = importlib.util.spec_from_file_location("terrace_front_readonly", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:  # noqa: BLE001 - any import failure just means 'no recipe view'
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    pieces, models, drawn, name_plate = load(a.root)
    lines = check(pieces, models, drawn, name_plate)
    if a.json:
        print(json.dumps({"models": models, "lines": lines}, indent=1))
    else:
        for name, s in models.items():
            print("model %-12s %s" % (name, s))
        for l in lines:
            print("%-5s %-10s %s | found %s | want %s%s" % (l["row"], l["verdict"], l["what"], l["found"], l["want"],
                                                       (" | " + l["note"]) if l["note"] else ""))
    return 1 if any(l["verdict"] == "FAIL" for l in lines) else 0


if __name__ == "__main__":
    sys.exit(main())
