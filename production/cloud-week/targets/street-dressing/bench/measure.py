"""bench: pixel measurements on photograph P1 (Geograph 2693537, the 640 px copy): the back of a slatted bench seen against the light."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sd_family as SF

OBJECT_BOX = [148, 178, 512, 372]
FEATURES = [
    dict(id="back_top", axis="y", band=[200, 300], win=[176, 192], pol="-"),
    dict(id="gap1_top", axis="y", band=[200, 290], win=[194, 206], pol="+"),
    dict(id="gap1_bottom", axis="y", band=[200, 290], win=[198, 212], pol="-"),
    dict(id="gap2_top", axis="y", band=[200, 290], win=[210, 222], pol="+"),
    dict(id="gap2_bottom", axis="y", band=[200, 290], win=[216, 228], pol="-"),
    dict(id="gap3_top", axis="y", band=[200, 290], win=[226, 238], pol="+"),
    dict(id="gap3_bottom", axis="y", band=[200, 290], win=[232, 244], pol="-"),
    dict(id="gap4_top", axis="y", band=[200, 290], win=[242, 254], pol="+"),
    dict(id="gap4_bottom", axis="y", band=[200, 290], win=[246, 258], pol="-"),
    dict(id="left_end", axis="x", band=[186, 196], win=[140, 160], pol="-"),
    dict(id="mid_left", axis="x", band=[217, 221], win=[316, 334], pol="-"),
    dict(id="mid_right", axis="x", band=[217, 221], win=[328, 346], pol="+"),
    dict(id="right_end", axis="x", band=[186, 196], win=[494, 516], pol="+"),
]
if __name__ == "__main__":
    SF.measure_main(os.path.dirname(os.path.abspath(__file__)), "bench", "2693537", "P1", OBJECT_BOX, FEATURES)
