"""phone-box: the measurements on photograph P1 (Geograph 5269043), made the way the gate measures: each edge is the
strongest grey-level step inside a recorded window, averaged over a recorded band of the object's own face."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sd_lib as L

SCRATCH = os.environ.get("SD_SCRATCH", "/home/user/ledger-scratch/street-dressing/phone-box")
OBJECT_BOX = [405, 60, 670, 715]      # the kiosk's own extent in the 1024 px image: x0 y0 x1 y1
# axis y: rows, band = columns [c0, c1] of the face; axis x: columns, band = rows [r0, r1]
FEATURES = [
    dict(id="roof_top", axis="y", band=[525, 555], win=[60, 76], pol="any"),
    dict(id="cap_bottom", axis="y", band=[525, 555], win=[88, 104], pol="any"),
    dict(id="header_bottom", axis="y", band=[560, 600], win=[168, 190], pol="any"),
    dict(id="band_top", axis="y", band=[470, 500], win=[392, 410], pol="any"),
    dict(id="band_bottom", axis="y", band=[470, 500], win=[436, 452], pol="any"),
    dict(id="rail_top", axis="y", band=[470, 500], win=[628, 644], pol="any"),
    dict(id="rail_bottom", axis="y", band=[470, 500], win=[650, 664], pol="any"),
    dict(id="post_l_outer", axis="x", band=[250, 330], win=[404, 416], pol="any"),
    dict(id="frame_l_outer", axis="x", band=[250, 330], win=[416, 428], pol="any"),
    dict(id="glass_l", axis="x", band=[250, 330], win=[430, 444], pol="any"),
    dict(id="glass_r", axis="x", band=[250, 330], win=[630, 645], pol="any"),
    dict(id="frame_r_outer", axis="x", band=[250, 330], win=[646, 660], pol="any"),
    dict(id="post_r_outer", axis="x", band=[250, 330], win=[660, 672], pol="any"),
]

if __name__ == "__main__":
    os.makedirs(SCRATCH, exist_ok=True)
    pg, path = L.sampled_photo("5269043", "P1", SCRATCH)
    print(pg)
    g = L.load_gray(path)
    out = {}
    for f in FEATURES:
        p, c, sp = L.edge_pos(g, f["axis"], f["band"], f["win"], f["pol"])
        out[f["id"]] = dict(px=round(p, 2), contrast=round(c, 1), spread=round(sp, 2), **f)
        print("%-14s %7.2f  contrast %5.1f  spread %4.2f" % (f["id"], p, c, sp))
    json.dump({"photo": "P1", "gid": "5269043", "size": list(g.shape[::-1]), "object_box": OBJECT_BOX, "features": out}, open(os.path.join(os.path.dirname(__file__), "photo_measurements.json"), "w"), indent=1)
