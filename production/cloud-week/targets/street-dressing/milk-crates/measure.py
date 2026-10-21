"""milk-crates: pixel measurements on photograph P1 (Geograph 6898849, the 640 px copy): two blue crates stacked, seen obliquely from above."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sd_family as SF

OBJECT_BOX = [474, 595, 720, 906]    # in the 1024 px copy (768 x 1024)
FEATURES = [
    dict(id="top_rim_top", axis="y", band=[608, 640], win=[704, 728], pol="any"),
    dict(id="top_rim_bottom", axis="y", band=[608, 640], win=[728, 749], pol="any"),
    dict(id="lower_rim_top", axis="y", band=[608, 640], win=[803, 829], pol="any"),
    dict(id="stack_bottom", axis="y", band=[608, 640], win=[864, 896], pol="any"),
    dict(id="front_left", axis="x", band=[832, 872], win=[515, 544], pol="any"),
    dict(id="front_right", axis="x", band=[832, 872], win=[646, 672], pol="any"),
]
if __name__ == "__main__":
    SF.measure_main(os.path.dirname(os.path.abspath(__file__)), "milk-crates", "6898849", "P1", OBJECT_BOX, FEATURES)
