# The set-aside donkey jacket, bound the game way and tested moving in Unreal (30 September)

Jafar, 30 September: "Game clothes are not simulated cloth. A garment is a skeletal mesh skinned to the MetaHuman skeleton, with skin weights transferred from the body mesh and fixes at the shoulders, elbows and hips so it bends cleanly; only loose parts, a coat's hem or a skirt, are cloth-simulated. [...] take the set-aside jacket, bound this way on Ron, and test it walking, sitting and with arms raised in Unreal." Not for his page: a method test, reported to the clothing session (NOW.md, Handovers to clothing), whose own skinned remake of the jacket is under way.

## What was tested

The clothing session's last simulated-cloth jacket (its 29 September finish, 521,044 triangles) cut to 40,000 triangles and skinned to Ron's own skeleton (MH_RoccoP2) by `tools/meshgen/blender/bind_garment.py`, imported onto his body skeleton with the old jacket's wool, yoke and button materials (`tools/ue/import_garments.py`), worn over his boots and trousers with Epic's jumper hidden (`LedgerGarments.h`, `-WearHeld`), and filmed in the street by the portrait tool standing in the open road (`-PortraitGarments -PortraitStand=14,0,-90 -PortraitMotion=... -PortraitMotionViews=...`): Epic's walk loop, Epic's 28-second body range-of-motion loop (arms overhead, arms out, twists, a deep squat) and the sit made on 28 September.

## Three bindings

1. **Nearest body point** (the weights of the body point nearest each jacket point, the armpits filled in from their neighbours): with the arms raised the jacket's sides rose with them in wings down to the hip (`blender-nearest.jpg`, second row): the side panels had taken the arm's bones. 14% of its edges stretched past 1.35 times in Blender against 1% of Ron's own skin. Rejected.
2. **A, panel by panel**: the jacket's sewing pattern (its "pattern" UV layer, one island a panel) says which points are sleeve and which are the jacket's body; sleeves copy only the arm's weights, the body only the trunk's with every bone under the upper arm removed, and the armhole seams take both, smoothed over a few centimetres. Stretch fell to 2.5% arms raised, 0.9% walking (`blender-panels.jpg`).
3. **B, as A, but the trunk keeps Epic's shoulder correctives** (the bones under upperarm_correctiveRoot, which Unreal drives from the arm's pose).

Blender cannot judge the shoulders: it turns the correctives rigidly with the arm, so in Blender Ron's chest came through A's front with the arms up. In Unreal, where they are driven, it does not.

## In Unreal

- **Walking** (`walking.jpg`, front and back): follows him cleanly, no tearing, sleeves and back right.
- **Arms raised and out** (`arms-A-B.jpg`: A front, B front, A back, B back; seconds 16, 18, 20, 22): no wings, no body through, both A and B. B lifts the shoulders with the arms a little more; A's front collar is a little neater.
- **Sitting** (`sitting-A-B.jpg`: A front, B front, A side, A back, B back): from the side the front lies over the lap; from the front the lower front follows each thigh and splits between them, reading as shorts; from behind the back hangs straight down through where a seat would be. A shows skin at the top of the yoke as he leans forward; B does not. **B is the better binding.**

## What is still wrong

1. The skirt of the jacket (below the hips) must be cloth, as Jafar said: skinned, it follows the thighs (sitting, the deep squat).
2. Epic's trousers come up to 118 cm and show through the jacket's lower front as dark patches when he walks: the jacket needs about a centimetre more room at the belly and hips, or the trousers' top hidden under it.
3. His throat is bare in the collar's opening: the jacket is worn with nothing under it (Epic's jumper is hidden); a shirt collar is needed.
4. A crease across the chest, in the garment's own shape.

The files: F:/LedgerTools/bound/RonJacket (A) and RonJacketB (B), each with the skinned FBX, its .blend and bind.json; the films in F:/LedgerTools/tmp/jacket-test.
