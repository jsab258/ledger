# The donkey jacket's fit and stiffness (research note, 29 September 2026)

The clothing session's research after two blind reviews failed the pattern-sewn jacket (production/art/clothing/donkey-jacket-sewn/review-1.md, review-2.md): a separate helper given the problem (a roll across the upper back, the cloth clinging to the chest and belly, the back standing off like a cape, a sail under raised arms), not a theory; about thirty minutes; every source read 29 September 2026. **D** documented with its source; **I** the helper's inference. Saved by the clothing session.

## In short

- **The cloth's weight, first (I, from Blender's source [S1]).** Blender's vertex mass is per vertex. At 12 mm edges a jacket of about 1.9 m² has 13,000 to 15,000 vertices; at 0.006 kg each the simulated jacket weighed **80 to 90 kg**. Melton weighs about 0.7 kg/m² [U1], about 0.09 g a vertex at 12 mm. With tension 40 that load stretches the upper jacket about 10% under its own weight (real melton about 0.2%). One fault that fits all four failures: sagging, wrapping the belly, stretching into a sail instead of lifting the hem, the back hanging out.
- **The pattern (D, tailoring sources).** A big belly takes up front length; a front too short kicks the back hem out (the "tent"). A horizontal fold between the shoulders means the upper back is too long; the standard fix is to shorten the back above the armhole. Brian has no belly option: front length is added by hand.
- **Unreal.** A backstop of distance about 0 stops cloth moving inward past its draped shape, Chaos's answer to clinging; 0.7 kg/m² is Epic's own figure for melton; the yoke should be render geometry driven by the same simulation triangles.

## 1. Pattern and fit

- Balance is the front length against the back from the neck point; right, the hem hangs level; set at the pattern [P1] (D). A stooped back needs more back length; an erect posture "a longer front and commensurately decreased back" [P2] (D).
- A large stomach lacks front material and spoils the hang [P1] (D); a front too short makes the back hang higher and tent at the hem [P9] (D, search summary). The fix: slash and spread the front, adding length and width at the centre front [P3], the back largely unchanged [P4] (D).
- A horizontal fold between the shoulders: the upper back too long; cut across the upper back and rotate the piece down at the armhole, taking out the excess [P5] (D).
- Shoulders: square ones wrinkle at the collar's base (let out the shoulder seam); sloped ones below the shoulder and at the underarm [P5] (D). A rounded back needs added length and a dart, movable into a yoke seam [P6] (D).
- For us (I): diagnose from the hem's heights (centre front, sides, centre back), not theory; any back shaping can hide under the PVC yoke. A low armhole joins much of the body to the sleeve, so lifting the arm should lift the jacket [P7] (D); a sail means the cloth is too stretchy for its weight or its skin weights are wrong (I).

## 2. Making heavy wool look stiff

- Blender (D, source [S1]): stretch force = (tension / average edge length) x the change in length; angular bending k = bending x rest length x 0.1; mass the same on every vertex; bending rest angles from the rest shape.
- So (I): at the same numbers a coarser mesh is stiffer (about in proportion to the edge) and lighter per area (with the square of the edge); every setting rescales with the resolution.
- Stiffness is bending against weight: the Peirce "bending length", c³ = G / (w g) (ASTM D1388) [T1] (D, search summary). The helper's estimate for our settings: about 3 to 4.5 cm. No published figure for melton found.
- Blender's presets (4.5.13): Denim mass 1, tension 40, bending 10, quality 12; Leather 0.4, 80, 150, 15; Cotton 0.3, 15, 0.5, 5; not tied to resolution or physical units [S2] (D).
- Chaos (D, engine source [U1-U3]): density's tooltip lists "Melton Wool: 0.7" kg/m²; the default fabric bending 100, buckling ratio 0.5, buckling stiffness 50, friction 0.8, collision thickness 1 cm; 3D rest angles by default ("any creases and folds ... baked"), FlatnessRatio (0 to 1) blends them towards flat. So a crease in the Blender drape stays in Unreal unless fixed or flattened (I).

## 3. Stopping the cape and the cling in Unreal

- Max distance: how far each vertex may move from its skinned place [U4] (D). Backstop: a particle cannot go more than "distance" inward past its skinned, draped place [U5] (D). Anim drive: a pull towards the skinned pose, 0 to 1. Tethers from pinned vertices, scale 1 to 1.1. Velocity scale 0.75 by default [U2] (D). Remedy's Alan Wake passed on 10 to 30% of world movement [G1] (D, 2010).
- Suggested for a hip-length jacket (I): max distance 0 at the yoke and shoulders, 0.5 to 1.5 cm at the chest and upper back, 2 to 4 cm at the belly and lower back, 5 to 8 cm at the hem; backstop 0 to 0.5 cm, radius 20 cm or more on the torso; anim drive 0.02 to 0.1; tethers from the yoke, scale 1.0 to 1.03; velocity scale 0.3 to 0.5; friction 0.2 to 0.4. Skin weights: torso panels on the spine and clavicles, sleeves on the arms (copied from the body, the side panels get upper-arm weights, which makes the sail).

## 4. The yoke on the render mesh

- Each render vertex is stored on a simulation triangle with a distance along its normal [U6] (D), so a raised layer keeps its offset; the proxy deformer's multiple influences (radius 5 cm by default) and selection sets tie chosen render vertices to chosen triangles [U3] (D). Thin decorative pieces stay out of the simulation [G2] (D). One wool layer, stiffer in the yoke, the yoke render geometry about 2 mm proud (I).

## What to change (the helper's steps)

1. Print the unit scale and the total simulated mass; set each vertex's mass from 0.7 kg/m² x its area.
2. Lower bending by about the same factor as the mass, then tune on a test square; keep tension and compression; quality 12 to 15; choose the resolution first.
3. The level-hem test at the sewing pose; if the centre front is higher, add front length at the belly (slash from the side seam to the centre front, spread at the centre front).
4. Look for the roll before and after the carry to the rest pose; if present when sewn, take its depth out of the back above the armhole, under the yoke.
5. Match Brian's shoulder slope to the body's in the sewing pose.
6. In Unreal: density 0.7, FlatnessRatio on the torso, the section 3 values, torso skin weights.
7. The yoke render-only.
8. Film arms raised, walking and a turn beside the photographs.

## Sources (all read 29 September 2026)

- [S1] Blender 4.5 release branch source: SIM_mass_spring.cc, implicit_blender.cc, cloth.cc (projects.blender.org).
- [S2] Blender 4.5.13 bundled cloth presets (the local install).
- [U1] UE 5.8 source: SimulationMassConfigNode.h, CollectionClothFabricFacade.h, XPBDBendingConstraints.h.
- [U2] UE 5.8 source: SimulationBendingConfigNode.h, SimulationAnimDriveConfigNode.h, SimulationLongRangeAttachmentConfigNode.h, SimulationVelocityScaleConfigNode.h.
- [U3] UE 5.8 source: ProxyDeformerNode.h. [U5] PBDSphericalConstraint.h. [U6] SkeletalMeshTypes.h.
- [U4] Epic, "Clothing Tool in Unreal Engine" (5.8 docs, undated): https://dev.epicgames.com/documentation/en-us/unreal-engine/clothing-tool-in-unreal-engine
- [P1] Derek Guy, "What Is Balance?", Put This On, 29 May 2013: https://putthison.com/what-is-balance-if-youve-ever-participated-in/
- [P2] King & Allen, "How we tailor for different postures", 8 September 2022: https://kingandallen.co.uk/journal/tips-advice/how-we-tailor-for-different-postures/
- [P3] Haley Glenn, "Common pattern adjustments for men", Seamwork, 30 September 2015: https://seamwork.com/issues/2015/10/adjustments-for-men
- [P4] The Pragmatic Costumer, full belly adjustment, 7 December 2015: https://thepragmaticcostumer.wordpress.com/2015/12/07/full-belly-adjustment-for-a-3xl-gentleman-altering-a-vest-pattern-for-the-fuller-male-figure/
- [P5] Heather Lou, blazer fitting, Closet Core, 15 March 2019: https://blog.closetcorepatterns.com/how-to-fit-a-tailored-jacket-or-blazer-fit-adjustments-for-the-jasika-blazer/
- [P6] Diane, "Fit notes for shoulder darts and yokes", Dream Cut Sew, 14 March 2025: https://www.dreamcutsew.com/fit-notes-for-shoulder-darts-and-yokes/
- [P7] Nathan Tailors, "Why your suit pulls when you raise your arms", 7 September 2026: https://www.nathantailors.com/en/blog/why-your-suit-pulls-when-you-raise-your-arms
- [P9] Search summaries only: Caprice Bespoke (undated); Styleforum and Ask Andy threads on the lump below the collar; Laura Mae Designs, upper back adjustments (June 2021).
- [F1] FreeSewing Brian options (undated): https://freesewing.eu/docs/designs/brian/options
- [T1] Peirce bending length, via a search summary of arXiv 1312.3796 (December 2013).
- [G1] Henrik Enqvist, "The Secrets of Cloth Simulation in Alan Wake", 29 April 2010: https://www.gamedeveloper.com/programming/the-secrets-of-cloth-simulation-in-i-alan-wake-i-
- [G2] Leaf et al., "Bolt: Clothing Virtual Characters at Scale", arXiv, 24 April 2025: https://arxiv.org/html/2504.17614
