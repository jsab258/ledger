# The suit jacket in the game, its skirt as cloth (1 October)

The builder's list, item 7: the clothing session's set-aside suit jacket (F:/LedgerTools/garments/suit_jacket_test, its README of 30 September: MakeHuman's CC0 Men's Suit 3 by Margaret Toigo, fitted to MH_RoccoP2 and MH_SamC5 as exported 29 September 17:33) filmed in Unreal with cloth on, walking, through Epic's range-of-motion loop (arms overhead and out, twists, a deep squat) and sitting. A method test, not for Jafar's page: the jacket was set aside at the gate.

## How it was made

`tools/ue/make_cloth_garment.py`, in the dressing project, makes one Chaos cloth asset per man from Epic's static-mesh cloth template:

- the render and simulation mesh: `*_suit_jacket_static.fbx`;
- the skin weights: copied from the clothing session's own `*_suit_jacket_skinned.fbx` (closest point on the same shape), so its panel binding is kept;
- the colour and normal maps: its own `*_basecolor.png` and `*_normal.png` (green flipped);
- how far each point may leave its skinned place: 0 above `simMaxDistance.below` and rising to 4 cm at the hem (`garment.json`: Ron 97.2 to 86.9 cm, Darren 92.5 to 84.5 cm), written by a height gradient inside the cloth graph into the template's own MaxDistance map, after its paint node.

The game wears it on a cloth component following the body (`LedgerJacket.h`, `WearCloth`), Epic's jumper hidden under it, his boots on; the portrait tool films it (`-PortraitCloth=... -PortraitClothHidesTop -PortraitMotion=...`).

Two ways to set that map failed before this one, and the third works:
1. A weight layer written onto the simulation mesh by Geometry Script, named by the max-distance setting: the skirt never moved, even with 30 cm allowed.
2. The same values made in the graph under another name (LedgerMaxDistance): nothing moved, even at a constant 1. The setting's weight-map name is also an input pin, wired in Epic's template from the paint node's "MaxDistance", which wins over any name set on it.
3. The values written into "MaxDistance" itself, after the paint node: the cloth follows them. `proof-free-lower-half-30cm.jpg` frees everything below 130 cm by up to 30 cm, and the lower front opens and swings as he walks.

## What it shows

- **Walking** (`ron-walk.jpg`, `darren-walk.jpg`, front and back): the jacket follows both men cleanly, in its colours, the shirt front and tie in place; no tearing, no body through.
- **Arms and the squat** (`*-arms-and-squat.jpg`): arms overhead lift the whole jacket with them, the squat holds; nothing breaks.
- **Sitting** (`*-sit.jpg`, front and back): at 4 cm the skirt still follows the thighs: from the front the lower front wraps between them like shorts, and from behind it hangs straight down in a column where a seat would be (there is no seat in the film). 4 cm is too little for the skirt to leave the thighs.
- **The whole jacket as cloth** (`proof-whole-jacket-free-30cm.jpg`): it collapses and tears apart walking, the chest bare. The shirt front, tie and buttons are in the same mesh and simulate with it; a simulated garment needs a simulation mesh of the shell alone (Epic's route: a single-sided sim mesh driving the render mesh).

## For the clothing session

The skinned binding holds in the game walking and through the range of motion. Sitting needs the skirt to move more than 4 cm below the hips (or the skirt skinned to the pelvis, not the thighs, as its README intended), and anything that simulates must leave the shirt front, tie and buttons out of the simulated part. The two side and three-quarter views of the sit were blocked by the shopfront at the stand used, so the side of the sit is not filmed.

Films (raw pictures): F:/LedgerTools/tmp/suit-test (final-Rocco-*, final-Sam-*, and the proofs).
