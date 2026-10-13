"""a-board: pixel measurements on two photographs.
P1 = Geograph 3671864 (a painted plywood A-board, front leaf seen square on; the 480 x 640 copy, turned 2.6 degrees about (265, 335) because the board's
vertical edges ran 2 to 3 degrees off the picture's vertical): left and right edges at two heights, the top, the two feet's lower edges, the top of the foot arch.
P2 = Geograph 6913397 (a framed notice board beside a bus, 4 August 1978; the 1024 px copy): the board's four edges, used for the width to height ratio only."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sd_family as SF
import sd_lib as L
from PIL import Image

ROT_DEG, ROT_CENTRE = 2.6, (265, 335)
OBJECT_BOX_P1 = [70, 36, 436, 640]
FEATURES_P1 = [
    dict(id="left_top", axis="x", band=[100, 140], win=[62, 80], pol="-"),
    dict(id="left_bot", axis="x", band=[500, 540], win=[62, 78], pol="-"),
    dict(id="right_top", axis="x", band=[100, 140], win=[430, 439], pol="-"),
    dict(id="right_bot", axis="x", band=[500, 540], win=[430, 441], pol="-"),
    dict(id="top_y", axis="y", band=[200, 300], win=[30, 48], pol="+"),
    dict(id="foot_left_y", axis="y", band=[75, 115], win=[620, 640], pol="-"),
    dict(id="foot_right_y", axis="y", band=[385, 425], win=[620, 640], pol="-"),
    dict(id="arch_top_y", axis="y", band=[200, 290], win=[588, 606], pol="-"),
]
# the foot arch's width at its base, measured at a fixed row (its ratio to the leaf's width is the invariant)
FEATURES_ARCH = [
    dict(id="arch_base_left_x", axis="x", band=[620, 628], win=[128, 152], pol="any"),
    dict(id="arch_base_right_x", axis="x", band=[620, 628], win=[352, 378], pol="any"),
]
OBJECT_BOX_P2 = [484, 466, 560, 562]
FEATURES_P2 = [
    dict(id="left_x", axis="x", band=[500, 520], win=[482, 500], pol="+"),
    dict(id="right_x", axis="x", band=[500, 520], win=[540, 560], pol="-"),
    dict(id="top_y", axis="y", band=[505, 535], win=[464, 471], pol="+"),
    dict(id="bottom_y", axis="y", band=[505, 535], win=[552, 566], pol="-"),
]


def run(g, feats):
    out = {}
    for f in feats:
        p, c, sp = L.edge_pos(g, f["axis"], f["band"], f["win"], f.get("pol", "any"))
        out[f["id"]] = dict(px=round(p, 2), contrast=round(c, 1), spread=round(sp, 2), **f)
        print("%-18s %7.2f contrast %5.1f spread %4.2f" % (f["id"], p, c, sp))
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    scr = SF.scratch("a-board")
    pg, path = L.sampled_photo("3671864", "P1", scr)
    Image.open(path).convert("RGB").rotate(ROT_DEG, resample=Image.BICUBIC, center=ROT_CENTRE, fillcolor=(128, 128, 128)).save(os.path.join(scr, "P1rot.jpg"), quality=95)
    g = L.load_gray(os.path.join(scr, "P1rot.jpg"))
    print(pg)
    res = {"P1": {"photo": "P1rot", "gid": "3671864", "size": list(g.shape[::-1]), "object_box": OBJECT_BOX_P1,
                  "rotated": {"deg": ROT_DEG, "centre": list(ROT_CENTRE)}, "features": run(g, FEATURES_P1), "arch_features": run(g, FEATURES_ARCH), "page": pg}}
    pg2, path2 = L.sampled_photo("6913397", "P2", scr)
    g2 = L.load_gray(path2)
    print(pg2)
    res["P2"] = {"photo": "P2", "gid": "6913397", "size": list(g2.shape[::-1]), "object_box": OBJECT_BOX_P2, "features": run(g2, FEATURES_P2), "page": pg2}
    json.dump(res, open(os.path.join(here, "photo_measurements.json"), "w"), indent=1)
