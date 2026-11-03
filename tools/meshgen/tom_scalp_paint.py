"""Tom's scalp painted in his hair's colour, so the gaps in his hair never show pale skin (his ruling of 3 November, hair, 3).

    python -I tools/meshgen/tom_scalp_paint.py [--inputs DIR] [--out PATH]
    python -I tools/meshgen/tom_scalp_paint.py --selftest

WHY. His crown read bleached since 2 November, when the hair's voxel shadow on surfaces went to 0 to clear a black
"ponytail" from the office wall: that pass also shaded his scalp under his hair, so with it off the scalp's skin shows
through the strands, lit as if bare. Three tries at the shadow failed (DECISIONS 3 November); his fourth: leave the
shadow at 0 and paint the scalp itself in the hair's colour. Epic's MetaHuman heads are drawn this way at a distance
too (the plugin bakes a groom into the far heads' colour; its T_BakedGroomDefault).

WHAT IT PAINTS. His near head's baked base colour (T_Head_LOD1_BC, 2048 square, the head's own layout), through the
MetaHuman Character plugin's own scalp region (T_SkinAccentRegions_002, fourth channel: white over the top, back and
sides, black over the face, a soft edge round the hairline), toward his hair's dark brown (the cast maker's
TOM_DARK_BROWN: melanin 0.8, redness 0.03), keeping a little of the skin's own variation so the paint is not flat.
Both inputs are exported by tools/ue/export_head_scalp_inputs.py and kept in F:/LedgerTools/bodies/MH_TomL1/scalp-inputs;
the result goes to the game inputs on F: (a new picture stays out of git), where the game and its staging look.
"""
import os
import sys

import numpy as np
from PIL import Image

INPUTS = r"F:\LedgerTools\bodies\MH_TomL1\scalp-inputs"
REL = "production/assets/people/tom/T_Head_LOD1_BC_scalp.png"
OUT = os.path.join(os.environ.get("LEDGER_GAME_INPUTS", r"F:\LedgerTools\game-inputs"), *REL.split("/"))
HAIR_SRGB = (52, 38, 30)    # dark brown at melanin 0.8, a little warm: the roots' colour, under the strands
STRENGTH = 0.85             # at the scalp's core; the skin's own variation keeps the rest
EDGE = (0.25, 0.85)         # the mask's soft edge mapped to 0..1, so the hairline's skin stays skin


def paint(bc, mask):
    """bc: HxWx3 uint8 base colour; mask: HxW float 0..1 (the scalp region). Returns HxWx3 uint8."""
    a = bc.astype(float)
    s = np.clip((mask - EDGE[0]) / (EDGE[1] - EDGE[0]), 0.0, 1.0) ** 1.2 * STRENGTH
    lum = a.mean(axis=2, keepdims=True)
    # the skin's own light and dark, a tenth of it, carried into the paint
    vary = 1.0 + 0.1 * (lum / max(1.0, float(lum.mean())) - 1.0)
    hair = np.array(HAIR_SRGB, dtype=float)[None, None, :] * vary
    out = a * (1.0 - s[:, :, None]) + hair * s[:, :, None]
    return np.clip(out, 0, 255).astype(np.uint8)


def run(inputs=INPUTS, out=OUT):
    bc = np.asarray(Image.open(os.path.join(inputs, "T_Head_LOD1_BC.tga")).convert("RGB"))
    regions = Image.open(os.path.join(inputs, "T_SkinAccentRegions_002.tga"))
    mask = np.asarray(regions.split()[3].resize((bc.shape[1], bc.shape[0]), Image.BILINEAR)).astype(float) / 255.0
    res = paint(bc, mask)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    Image.fromarray(res).save(out, optimize=True)
    covered = float((mask > EDGE[1]).mean())
    return out, covered


def selftest():
    bc = np.full((8, 8, 3), 200, np.uint8)
    mask = np.zeros((8, 8)); mask[:4, :] = 1.0
    res = paint(bc, mask)
    ok = abs(int(res[7, 0, 0]) - 200) <= 1 and res[0, 0, 0] < 100 and res[0, 0, 0] > 40
    print("tom_scalp_paint selftest: %s face=%d scalp=%d" % ("passed" if ok else "FAILED", res[7, 0, 0], res[0, 0, 0]))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    a = sys.argv[1:]
    out, covered = run(a[a.index("--inputs") + 1] if "--inputs" in a else INPUTS, a[a.index("--out") + 1] if "--out" in a else OUT)
    print("tomScalpPaint out=%s scalpCore=%.3f" % (out, covered))
