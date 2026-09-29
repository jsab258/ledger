# Testing a skirt seated (research note, 29 September 2026)

The clothing session asked for this after Sheila's pleated skirt failed its sitting test five ways. A separate helper was given the problem, not a theory, and worked for about thirty minutes, read only. Every source was read on 29 September 2026. **D** means documented, with its source; **I** means the helper's inference. "Search summary" means only a search engine's summary was seen.

## In short

- **Recommended test (I): two stages.** *Stage 1, skinned only:* pose seated in one step and count cone and render points inside the body. Pass: none. *Stage 2, cloth:* Dynamic Mesh on, pins as now (1 at the hip, 0.35 at the hem, stiffness 1). Rest to frame 10, sit by frame 100, slide a box seat in from behind by 120, hold to 150. Settings: quality 12, collision quality 5, impulse clamp 30, distance 5 mm, body outer thickness 5 mm, no self-collision. Pass: nothing inside the body or seat at frames 100 and 150. Run Stage 2 only once Stage 1 passes, and re-run the walk on the new weights.
- **All five runs pulled the cloth towards a target inside the body (I).** Test 3 showed the skinned seated shape, which the pins aim at, had 339 points inside the thighs. Chaos measures max distance and backstop from the skinned position too (D [E1]), and MagicaCloth's backstop fails unless the skirt is skinned to the legs (D [G1]). Sitting is a skinning problem first.
- **Weights for sitting (I):** band and hip on the pelvis. Below the buttock fold the whole ring follows the thighs, back included (it is sat on): each half to its own thigh, centre front and back shared 50/50 over 8 to 10 cm.
- **The lampshade is normal for skinning (I);** in the game gravity lays it on the lap within max distance. A thigh-driven morph is possible (D [E4]) but unproven through the outfit route [L1].
- **Blender (D [B1]):** reach the pose from the bind pose over several frames. Single Sided pushes intersecting cloth out along the collider's normal, so a tangled start shreds (I). Dynamic Mesh re-takes the rest shape each frame, ending the fight between pins and springs behind the spikes (I).
- **Unreal (D [E1][E2]):** the anim drive and max distance can be changed at runtime, so a seated Sheila can be held tighter.
- **Epic gives no advice on skirts for MetaHumans or for seated characters,** and no studio's account of seated skirts was found.

## A. Testing seated cloth in a DCC

- **Blender manual (D [B1]).**
  - "Very fast movements and teleport jumps" break the sim.
  - For clipping: more Distance, then more Quality (smaller steps catch fast collisions).
  - The body's Collision modifier must sit below its Armature.
  - Animating a pin weight up from 0 is unsupported; a Rest Shape Key starts the cloth pre-draped.
- **Marvelous Designer (D [M1][M2]).** The seated body loads as a morph target reached over a set frame count while the garment simulates; big changes need an interim pose. One user loads the chair with the body and raises the steps from 30 to 45 or 60.
- **Daz dForce (D [M3]):**
  - Pull the chair back, then slide it in so it pushes the skirt ahead.
  - "Leave some space between the legs and the seat."
  - Do not squeeze the motion into 30 frames; use more frames or substeps.
- **Stills in Blender (D [B3]):** final pose at frame 150, run to 175–200, impulse clamp 25–55, a box in place of a chair.
- **Coarse cloth (D).** A low-poly skirt misbehaves on lifted legs until subdivided [B4]; cloth can pass a collider whose faces differ in size from its own (search summary [B6]).
- **Our pose (I).** Rotating the thighs with the pelvis still sweeps them through the seat's place, so lower the pelvis onto the seat or slide the seat in afterwards.

## B. How games handle seated skirts

- **Skinning carries it (D [G1][G2]).** MagicaCloth's backstop works from the animated pose; its skirt must be weighted to the legs, or "the legs will pass through the skirt". A 2025 forum answer blames missing weights for MetaHuman legs clipping cloth [E6].
- **Chaos (D [E1][E2]):**
  - At 0 max distance a point is kinematic. Backstop is a sphere offset along the normal from the skinned position, optionally from a separate accessory mesh.
  - The anim drive pulls towards the skinned mesh, "for cinematics or animation-driven scenes"; it and max distance are settable at runtime. ClothBlendWeight blends skinned (0) against simulated (1).
  - Colliders: capsules, tapered capsules (cloth only), skinned level sets or skinned triangle meshes; CCD and substeps help against fast limbs. Chairs need Collide with Environment [E3].
- **Correctives (D [E4][M4]).** Bone Driven Controller drives a morph from a bone "to avoid geometry intersections". Daz skirts ship "sitting" morphs, good "if both legs are bent equally".
- **I:** when Sheila sits, the builder can raise the anim drive or lower max distance and leave chairs out of the cloth, so the skirt shows its skinned seated shape. Hence Stage 1 matters most.

## C. The cheapest honest test

Stage 1 (minutes, no simulation, I): re-weight as above; pose fully seated; test every cone and render point against the body (closest point, signed by its normal); record the gap on the lap. It fails if any point is inside the body, or hangs more than about 1 cm below the thighs, where a seat would cut it.

Stage 2 only checks that gravity settles the lap and nothing tunnels at a walking pace.

If Stage 1 cannot pass, more cloth settings will not help; that is the point to stop and tell Jafar (I).

## Sources (all read 29 September 2026)

- [B1] Blender manual and API, bundled with the Blender MCP on F:: cloth/examples.rst, settings/collisions.rst, settings/shape.rst, physics/collision.rst; CollisionSettings.use_culling (undated).
- [B3] Nabesaka, "Using Blender Cloth Simulation For Stills", 20 April 2023, updated 1 April 2024.
- [B4] Blender Artists, "Creating a skirt rig with cloth sim…", 17–30 January 2018.
- [B6] Search summary: projects.blender.org #47195 (undated; the page's bot check was not passed).
- [M1] Marvelous Designer, "Change Pose by OBJ Morphing", 29 May 2025.
- [M2] Daz forums, "Posing and draping in Marvelous Designer", August 2016.
- [M3] Daz forums, "dForce simulation: how to avoid exploding skirt while sitting?", November 2019.
- [M4] Daz forums, "G2F Skirt Rigging", October 2014; "Problems with dresses and seated poses", July 2013.
- [E1] UE 5.8 source on this PC: the cloth asset's MaxDistance, Backstop, AnimDrive, Collision and Solver config nodes; ClothAssetInteractor.h; SkeletalMeshComponent.h; TaperedCapsuleElem.h.
- [E2] Epic, "Clothing Tool", UE 5.8 docs (undated).
- [E3] T. Brakensiek (Epic), "Cloth Collision with World", 7 June 2022, updated 3 March 2026.
- [E4] Epic, "Bone Driven Controller", UE 5.8 docs (undated).
- [E6] Epic forum, "No collision clipping in cloth asset but clipping when playing", reply of 4 June 2025.
- [E7] Checked, no skirt advice: Claire_puiling, "Chaos Cloth Simulation on puffy skirt", 28 December 2024; "MetaHuman Fashion Kit" listing, 21 April 2026.
- [G1] Magica Soft, MagicaCloth 2 "Backstop" (undated).
- [G2] Magica Soft, "Preventing penetration" (undated).
- [L1] Our notes: SHEILA-CLOTHES-2026-09-29.md, SKINNING-TROUSERS-2026-09-29.md.
