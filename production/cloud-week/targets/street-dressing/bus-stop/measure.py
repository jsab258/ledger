"""bus-stop: pixel measurements on photograph P1 (Geograph 5668101, the 640 px copy)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sd_family as SF

OBJECT_BOX = [500, 62, 610, 458]
FEATURES = [
    dict(id="flag_top", axis="y", band=[535, 565], win=[60, 80]),
    dict(id="flag_bottom", axis="y", band=[535, 565], win=[100, 120]),
    dict(id="band1_top", axis="y", band=[538, 546], win=[196, 216]),
    dict(id="case_top", axis="y", band=[530, 570], win=[226, 246]),
    dict(id="case_bottom", axis="y", band=[530, 570], win=[364, 386]),
    dict(id="band2_bottom", axis="y", band=[538, 546], win=[430, 456]),
    dict(id="flag_left", axis="x", band=[78, 98], win=[515, 535]),
    dict(id="flag_right", axis="x", band=[78, 98], win=[565, 590]),
    dict(id="case_left", axis="x", band=[300, 340], win=[505, 525]),
    dict(id="case_right", axis="x", band=[300, 340], win=[582, 606]),
    # the review of 13 October: the pole's own width (13 to 14 px, not 7 to 8), where the white length begins and the black ring under the case ends
    dict(id="pole_l", axis="x", band=[200, 225], win=[536, 550]),
    dict(id="pole_r", axis="x", band=[200, 225], win=[550, 564]),
    dict(id="white_top", axis="y", band=[540, 560], win=[165, 185]),
    dict(id="ring_bottom", axis="y", band=[540, 560], win=[384, 400]),
    dict(id="ring_top", axis="y", band=[540, 560], win=[368, 384]),
    dict(id="pole_l2", axis="x", band=[395, 410], win=[536, 550]),
    dict(id="pole_r2", axis="x", band=[395, 410], win=[550, 566]),
    dict(id="mid_bar", axis="y", band=[540, 566], win=[276, 292]),
    dict(id="card_top", axis="y", band=[540, 566], win=[293, 305]),
]
if __name__ == "__main__":
    SF.measure_main(os.path.dirname(os.path.abspath(__file__)), "bus-stop", "5668101", "P1", OBJECT_BOX, FEATURES)
