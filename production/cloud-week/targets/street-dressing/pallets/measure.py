"""pallets: pixel measurements on photograph P1 (Geograph 2660949, the 1024 px copy): a timber pallet leaning on a wall, deck boards seen from the front.
Each board's left and right edges are measured on a band of rows across all the boards; the ratio board width to pitch is the invariant used."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sd_family as SF
import sd_lib as L

OBJECT_BOX = [95, 205, 285, 400]
BAND = [296, 304]
# approximate edge positions read from the grid (left edge '+', right edge '-'): board k from left to right
LEFT = [103, 133, 165, 199, 235]
RIGHT = [120, 150, 183, 218, 255]
FEATURES = []
for k, (a, b) in enumerate(zip(LEFT, RIGHT), 1):
    FEATURES.append(dict(id="board%d_left" % k, axis="x", band=BAND, win=[a - 4, a + 4], pol="+"))
    FEATURES.append(dict(id="board%d_right" % k, axis="x", band=BAND, win=[b - 4, b + 4], pol="-"))
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    res = SF.measure_main(here, "pallets", "2660949", "P1", OBJECT_BOX, FEATURES)
    F = res["features"]
    w = [F["board%d_right" % k]["px"] - F["board%d_left" % k]["px"] for k in range(1, 6)]
    gaps = [F["board%d_left" % (k + 1)]["px"] - F["board%d_right" % k]["px"] for k in range(1, 5)]
    pitch = [F["board%d_left" % (k + 1)]["px"] - F["board%d_left" % k]["px"] for k in range(1, 5)]
    frac = [w[k] / pitch[k] for k in range(4)]
    out = {"board_px": w, "gap_px": gaps, "pitch_px": pitch, "board_over_pitch": frac, "mean": sum(frac) / 4.0, "spread": max(frac) - min(frac)}
    print(out)
    pm = json.load(open(os.path.join(here, "photo_measurements.json")))
    pm["P1"]["ratio"] = out
    json.dump(pm, open(os.path.join(here, "photo_measurements.json"), "w"), indent=1)
