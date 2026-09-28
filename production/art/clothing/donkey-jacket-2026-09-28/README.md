# The donkey jacket, hung on Ron's own body: first pass (28 September)

Not for approval yet: a proof that the route works, on the way to one jacket, simulated, on one body (Jafar's list, item 5).

- Ron's whole body (the build's body has no torso: a build drops the skin under clothes) came out of Unreal through MetaHumanCharacterExportBlueprintLibrary.export_geometry (tools/ue/export_dcc.py, LEDGER_DCC_MODE=geometry): 982 vertices within 15 cm of the middle at the waist, where the built body had none.
- tools/meshgen/blender/drape_jacket.py cuts a shell from his torso and arms, stands it off 3 cm, smooths away the muscle, hangs it straight down from the fullest point between armpit and hip, lets the hem down to the top of the thigh, and lets Blender's cloth settle it on his body for 90 frames, held at the shoulders. That is the simulation mesh (2,516 vertices); the render mesh adds thickness, the black yoke, a collar, four buttons and patch pockets. Both carry his skin weights.
- Still to do: the sleeves still creep down his lowered arms at the last frame (2 cm); the cloth wants a wool material in Unreal; the collar is plain; then the import into Unreal's cloth graph (production/research/character-pipeline/cloth-graph-python-2026-09-28.md), the simulation, and the checks walking, sitting and arms up; and 1990 photographs to check it against.

## Into Unreal's cloth, same night

tools/ue/make_cloth_jacket.py imports the two meshes and fills a copy of Epic's static-mesh cloth template (its nodes StaticMesh_Render, StaticMesh_SIM and TransferSkinWeights, whose names were read from the template file, since Python cannot list a graph) and regenerates the cloth asset: done, CA_ron_donkey in the dressing project (cloth-asset-2026-09-28.txt). Ron's whole body is kept in that project for the weights (tools/ue/export_dcc.py, geometry mode, now saved). Next: the jacket on Ron in the game on a cloth component, simulated, and checked walking, sitting and with arms up.
