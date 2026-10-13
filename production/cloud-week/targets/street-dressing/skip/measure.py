"""skip: pixel measurements on photograph P1 (Geograph 6875634, the 1024 px copy), first turned 7.2 degrees about (730, 270) because the skip stands tilted on a slope.
The skip is seen square on from its long side; the features are its silhouette's lines."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sd_family as SF
import sd_lib as L
from PIL import Image

ROT_DEG, ROT_CENTRE = 7.2, (730, 270)
OBJECT_BOX = [540, 190, 912, 345]
FEATURES = [
    dict(id="top_y", axis="y", band=[650, 780], win=[190, 206], pol="any"),
    dict(id="rim_line_y", axis="y", band=[650, 700], win=[222, 242], pol="any"),
    dict(id="bottom_y", axis="y", band=[670, 740], win=[326, 345], pol="any"),
    dict(id="tip_left_x", axis="x", band=[238, 246], win=[536, 562], pol="any"),
    dict(id="tip_right_x", axis="x", band=[236, 244], win=[894, 914], pol="any"),
    dict(id="top_left_x", axis="x", band=[203, 209], win=[584, 614], pol="any"),
    dict(id="top_right_x", axis="x", band=[203, 209], win=[834, 866], pol="any"),
    dict(id="bottom_left_x", axis="x", band=[326, 332], win=[606, 640], pol="any"),
    dict(id="bottom_right_x", axis="x", band=[326, 332], win=[774, 806], pol="any"),
]
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    scr = SF.scratch("skip")
    pg, path = L.sampled_photo("6875634", "P1", scr)
    Image.open(path).convert("RGB").rotate(ROT_DEG, resample=Image.BICUBIC, center=ROT_CENTRE).save(os.path.join(scr, "P1rot.jpg"), quality=95)
    g = L.load_gray(os.path.join(scr, "P1rot.jpg"))
    out = {}
    for f in FEATURES:
        p, c, sp = L.edge_pos(g, f["axis"], f["band"], f["win"], f.get("pol", "any"))
        out[f["id"]] = dict(px=round(p, 2), contrast=round(c, 1), spread=round(sp, 2), **f)
        print("%-16s %7.2f contrast %5.1f spread %4.2f" % (f["id"], p, c, sp))
    json.dump({"P1": {"photo": "P1rot", "gid": "6875634", "size": list(g.shape[::-1]), "object_box": OBJECT_BOX, "rotated": {"deg": ROT_DEG, "centre": list(ROT_CENTRE)}, "features": out, "page": pg}}, open(os.path.join(here, "photo_measurements.json"), "w"), indent=1)
