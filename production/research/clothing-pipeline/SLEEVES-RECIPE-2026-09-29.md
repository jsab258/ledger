# Sewing and draping jacket sleeves by script: what professional tools, research and Blender add-ons do (research note, 29 September 2026)

The clothing session's item 1 (CLOTHES.md): the sleeve problem researched again, given to a separate helper as the problem stood after the builder's three failed attempts (production/art/clothing/donkey-jacket-pattern/README.md), not as a theory; about thirty minutes; every source read 29 September 2026. It adds to SLEEVES-2026-09-29.md beside it. **D** documented, with a source; **I** the helper's inference. Saved by the clothing session (the helper does not write files); the session's own finding on the pattern is at the end.

## In short

- Every working pipeline found closes the seams at low or zero gravity, welds them into shared points, then settles at full gravity: Houdini's Vellum Drape, the OpenSew-2 Blender add-on, GarmentCode (which welds before it simulates at all). None keeps sewing springs on through the drape. (D)
- The pieces start wrapped round the body on shapes that unroll flat (cylinders, cones), so the seams begin close. (D)
- Blender takes both spring lengths and bending rest angles from the rest shape (D, source). A flat rest shape key makes every tube want to unroll; a piece bent into place (the builder's 15 cm blend into the armhole) stores strain that pulls it back; and a capped Max Sewing Force stops pulling harder once a gap passes a few millimetres (D, code). All three are likely reasons why the seams closed at frame 1 and reopened by frame 20. (I)
- No drop-in simulator better than Blender runs on the processor or an AMD card under a licence allowing commercial use: GarmentCode's simulator is research-only. The best free option is OpenSew-2's recipe (GPL-3.0), copied into our own script.

## 1. How professional tools and research do it

- **GarmentCodeData** (D): panels placed from the neck down, sleeves rotated to the arm's angle; A-pose bodies, arm angle varied ±15°; stitches merged before simulating, the original edge lengths as rest lengths so stretched edges pull the seam shut; gravity off for the first frames; collisions filtered by body part; cloth inside the body pulled out to the nearest surface; about 72% of samples succeed.
- **Fuhrmann et al. 2003** (D): pieces placed on cylinders and cones round the body, then sewn by physics.
- **Houdini Vellum Drape** (D): soft springs pull the points together with no gravity; after a welding frame delay the points are welded, then gravity comes on; optional bending stiffness across the welds.
- **CLO** (D, search summary): place sleeves as close to the arms as possible; if they misbehave, sew only the first 10 to 15 cm of the underarm, let it settle, then the rest; skin offset 0; check sleeve and armhole lengths match.
- **Marvelous Designer** (D): sleeves wrapped round an arm's bounding volume; pose changes by morphing the avatar over many frames.
- **Browzwear** (D): dressed in an A-pose; pose changes through an intermediate pose.
- **Bolt** (NVIDIA, 2025) (D): drapes one layer at a time; pushes cloth away from pinch points "such as under the armpits"; transfers skin weights using the garment's normals.
- None drapes in a relaxed arms-down pose: A-pose or arms more raised, then the avatar is animated to the target pose. (I)

## 2. Sleeve cap height and arm angle

- Cap height sets the angle a sleeve naturally hangs at (D): a high narrow cap hangs down (tailored jackets), a low wide cap points out and lets the arm lift (shirts, workwear); a cap drafted for one arm position shows drag lines in another (ikat bag, 2014; Sewing with Numbers, 2026).
- In 3D a garment whose rest shape suits raised arms stretches over the shoulder and bunches in the armpit when the arms come down; fit is judged in an A-pose, then other poses (Wolff et al., Computer Graphics Forum, 2023) (D).
- No published formula links cap height to an angle in degrees; the evidence is thin.

## 3. Blender by script

From Blender 4.5's source (D):
- Sewing springs are loose edges with rest length 0; their stiffness is the tension stiffness over the mean spring length; their pull grows with the gap until Max Sewing Force, then stays constant.
- Bending rest angles come from the rest positions (the Rest Shape Key when one is set).
- Self-collision skips only triangles sharing a point or joined directly by a sewing edge; one row further in they still push apart (why the cap and armhole repelled, I).
- `collision_settings.vertex_group_self_collisions` and `vertex_group_object_collisions` exclude a group's triangles from self and object collision.
- The collider's Single Sided option pushes cloth inside the body out along its normals.
- At 10 mm edges and tension 15 to 25, a sewing cap of 5 to 15 is reached at a gap of about 2 to 10 mm (I): the builder's cap of 10 made the seams weak.

**OpenSew-2** (GPL-3.0-or-later, free, Python-driven, Blender 5.2, August 2026) (D): pieces wrapped on the measured body, sleeves on the arm's axis at the arm's radius plus ease; quality 12 to 14, collision quality 6, distance 4 mm, self-collision on at 2 mm; sewing force unlimited (0), shrink 0, the collar band pinned (stiffness 25) while stitching; the body collider 2 mm outside, 20 mm inside, friction 60; stitch 25 frames at 0.15 gravity; weld stitches up to 4.5 cm apart at their midpoints, delete the loose edges, push points inside the body out 3 mm, a fresh cloth modifier so the welded shape is the new rest; settle 50 frames at full gravity, then a 3 to 6% take-in and a relax; its "Stiff" fabric: tension 25, compression 200, shear 15, bending 60, mass 0.45. Its author warns sleeves "gather at the armhole" on bodies whose arms hang against the ribs.

Paid add-ons (D): Garment Tool (from US$54; Blender's own solver; bends sleeves round the arms, ramps gravity, animates sewing force and shrink); Simply Cloth Studio 2.0 (US$36 to 170 by source; seams merge during the simulation; Python not verified).

## 4. Open-source simulators on the processor or AMD

| Option | Licence | Verdict |
|---|---|---|
| GarmentCode's simulator (NvidiaWarp-GarmentCode) | NVIDIA Source Code License, research or evaluation only | Out: non-commercial |
| NVIDIA Warp | Apache-2.0 since 1.6.2 (7 March 2025); runs on the CPU on Windows | A toolkit; porting GarmentCode's changes would be large |
| Newton | Apache-2.0; its VBD cloth solver runs on the CPU | Possible later, with our own stitching; speed unknown |
| Codim-IPC | Apache-2.0; Ubuntu and macOS only, last updated January 2023 | Out |
| libuipc | CUDA only | Out |
| HOOD, ContourCraft | code MIT; built on SMPL (non-commercial, I) | Out |
| Houdini Vellum Drape | Houdini Indie US$299 a year | Paid: Jafar's decision |
| Marvelous Designer | US$39 a month, US$280 a year; Python only inside the open app | Paid: Jafar's decision |

## 5. Routes that avoid the problem

- **Weld before simulating** (GarmentCode) (D; I for Blender): wrap every piece, merge each seam pair at its midpoint, simulate only a settle; acceptable only if the wrapped gaps are about 2 cm or less.
- **Build in 3D and flatten afterwards** (Marvelous Designer, CLO) (D); in Blender "Seams to Sewing Pattern" (GPL-2.0-or-later, May 2026). A check against the Brian draft, not a replacement.

## The helper's recipe for the next attempt

1. Diagnose: one run with gravity 0, Max Sewing Force 0, bending 0.1, collisions off, seam gaps logged each frame.
2. Pick the drape angle by geometry: the arm angle whose wrapped sleeve cap lies nearest its armhole.
3. Place every piece at once, in one mesh, unstretched; stop if any seam pair is more than about 4 cm apart.
4. Cloth: sewing springs on, Max Sewing Force 0, shrink 0, gravity 0 to 0.15; quality 12 to 15, collision quality 6, distance 3 to 4 mm; self-collision on with two or three rows either side of every seam excluded; the collar band pinned; the body collider Single Sided, 2 mm outside, 20 mm inside, friction about 60.
5. Stitch 20 to 30 frames, until every seam is within about 5 mm.
6. Weld at the midpoints; delete the loose edges; push points inside the body out 3 mm; a fresh cloth modifier.
7. Settle about 50 frames at full gravity.
8. Lower the arms: weights from the body, Armature above Cloth, Dynamic Mesh on, the body animated to MetaHuman's reference pose over 40 to 60 frames, through an intermediate pose if the armpit catches; hold 30 frames.
9. Weights again in the reference pose; export.

## The clothing session's own finding (29 September, before the helper reported)

The pattern the builder drafted was cut for the wrong body, which the helper could not know. body_measurements.py took the armpit as 9 cm under the arm's joint, in MetaHuman's reference pose whose arms are raised: 15 cm under Ron's shoulder, where a man's is 23 to 30 (FreeSewing's own standard man of his chest: 30). So Brian drew a 17 cm armhole whose foot sat above Ron's real armpit, inside the root of his arm, and to match that short armhole a sleeve 54 cm wide with a 4 cm cap, a shirt's. Measured on the body (a ray from the torso out towards the arm, the highest level where it meets air before the arm: 22 cm under the shoulder) and with shoulder to shoulder taken round the back as FreeSewing takes it (520 mm, not 446 straight across), Brian gives a 26 cm armhole and, with armholeDepth 12% and bicepsEase 12%, an 11.5 cm cap on a 51 cm sleeve: a work jacket's. The first failure (the side seams pushed 19 cm open with the arms in the rest pose) follows from the armhole's foot inside the arm.

## Sources (all read 29 September 2026)

- GarmentCodeData, arXiv 2405.17609 (May 2024; ECCV 2024): https://arxiv.org/html/2405.17609
- NvidiaWarp-GarmentCode, README and LICENSE (last push 2 September 2024): https://github.com/maria-korosteleva/NvidiaWarp-GarmentCode
- GarmentCode (MIT; last push 29 June 2025): https://github.com/maria-korosteleva/GarmentCode
- NVIDIA Warp CHANGELOG, 1.6.2 (7 March 2025): https://github.com/NVIDIA/warp
- Newton (Apache-2.0): https://github.com/newton-physics/newton; issue #4280 (22 September 2026)
- OpenSew-2, README, sim.py and props.py (GPL-3.0; August 2026): https://github.com/MarcelloMorettoni/opensew-2
- Blender 4.5 source (blender-v4.5-release): cloth.cc, SIM_mass_spring.cc, implicit_blender.cc, collision.cc, rna_cloth.cc: https://github.com/blender/blender
- Blender manual, cloth Shape and Collision settings (current): https://docs.blender.org/manual/en/latest/physics/cloth/settings/shape.html
- Houdini Vellum Drape SOP (Houdini 22.0 docs): https://www.sidefx.com/docs/houdini/nodes/sop/vellumdrape.html; Houdini Indie: https://www.sidefx.com/products/houdini-indie/
- CLO, "Correcting Improper Sleeve Simulation" (undated; search summary): https://support.clo3d.com/hc/en-us/articles/115013366587
- Browzwear, "Preparing the Garment on the Avatar" (updated 24 December 2025): help.browzwear.com
- Bolt, arXiv 2504.17614 (24 April 2025): https://arxiv.org/html/2504.17614
- Fuhrmann et al., Computers & Graphics 27(1), 2003: https://www.sciencedirect.com/science/article/abs/pii/S0097849302002455
- ikat bag, "Subtleties in Drafting: Sleeves" (3 March 2014); Sewing with Numbers, "How to draft t-shirt sleeves" (10 August 2026); Wolff et al., Computer Graphics Forum 2023 (search summary)
- Garment Tool docs (undated): https://joseconseco.github.io/GarmentToolDocs/quick_guide/
- Simply Cloth Studio 2.0, CG Channel (19 January 2026)
- Seams to Sewing Pattern (GPL-2.0-or-later; 27 May 2026): https://gitlab.com/thomaskole/blender-seams-to-sewing-pattern
- Codim-IPC (Apache-2.0; 29 January 2023); HOOD (MIT; 20 May 2025); ContourCraft (MIT; 2 August 2025)
- FreeSewing's standard adult male measurements, @freesewing/models 4.10.2 (MIT), read from the package on this PC
