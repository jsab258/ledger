"""Derives the street's window sites from tools/art-recipes/terrace-front.py (the one home of what the street draws):
every opening of a house (not a shop's own glazing), its kind, its centre, sill and head, and the wall it is in.
Used by make_target.py (to write them into target.json) and self_check.py (to re-derive them live and compare).
Run with /home/user/.bpyenv/bin/python (terrace-front.py needs nothing from bpy at import)."""
import importlib.util, os, re, sys, collections, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def load_tf():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("tf_hw", os.path.join(ROOT, "tools", "art-recipes", "terrace-front.py"))
    tf = importlib.util.module_from_spec(spec)
    sys.modules["tf_hw"] = tf
    spec.loader.exec_module(tf)
    return tf


def _xz(q):
    if q.get("kind") == "mesh":
        xs = [v[0] for v in q["verts"]]; zs = [v[2] for v in q["verts"]]; ys = [v[1] for v in q["verts"]]
        return min(xs), max(xs), min(zs), max(zs), min(ys), max(ys)
    return q["x0"], q["x1"], q["z0"], q["z1"], q.get("y0"), q.get("y1")


def derive():
    tf = load_tf()
    parts, err = tf.plan_street(ROOT)
    if err:
        raise RuntimeError(err)
    pats = [
        (re.compile(r"^(east_parade)_upper_sash(?:kit)?_(?:[a-z]+_)*?(\d+)(?:_\d+)?_bay(\d+)$"), "upper"),
        (re.compile(r"^(east_chandler)_upper_sash(?:kit)?_(?:[a-z]+_)*?(\d+)(?:_\d+)?_bay(\d+)$"), "upper"),
        (re.compile(r"^(west_south)_gf_sash(?:kit)?_(?:[a-z]+_)*?(\d+)(?:_\d+)?_bay(\d+)$"), "gf"),
    ]
    groups = collections.defaultdict(list)
    for q in parts:
        for rx, floor in pats:
            m = rx.match(q["id"])
            if m:
                groups[(m.group(1), int(m.group(3)), floor, int(m.group(2)))].append(q)
    sites = []
    for (blk, bay, floor, idx), qs in sorted(groups.items()):
        ext = [_xz(q) for q in qs]
        x0 = min(e[0] for e in ext); x1 = max(e[1] for e in ext)
        z0 = min(e[2] for e in ext); z1 = max(e[3] for e in ext)
        mats = sorted({q.get("material") for q in qs})
        kitnodes = any("sashkit" in q["id"] for q in qs)
        sites.append({"block": blk, "bay": bay, "floor": floor, "index": idx, "x_min": round(x0, 4), "x_max": round(x1, 4),
                      "z_min": round(z0, 4), "z_max": round(z1, 4), "materials": mats, "kit_nodes": kitnodes})
    return sites, tf


def kind_of(tf, block, bay):
    return tf._window_kind(block, bay)


if __name__ == "__main__":
    sites, tf = derive()
    for s in sites:
        print(s["block"], s["bay"], s["floor"], s["index"], round((s["x_min"] + s["x_max"]) / 2, 3), round(s["x_max"] - s["x_min"], 3), s["z_min"], s["z_max"], kind_of(tf, s["block"], s["bay"]), s["materials"], s["kit_nodes"])
