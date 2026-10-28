# Review of KIT-2026-10-28.md (fresh reviewer, 28 October 2026)

**What was read.** The document. The kept folder F:/LedgerTools/aaa-study/mafia/kit-2026-10-28 (export 1,554 files, scripts, summary, logs). The 25 October street-group exports it names (BPP_PLA_Palermo_Buildings_01_MainStreet/BackStreet.json and the cell that places them). The game's name index (index/*.txt). Unreal 5.8's install, read only: the PCG plugin source and sample content, the PCGPrimitives plugin, and the PCG toolset's shape-grammar skill text. Epic's shape-grammar page (fetched 28 October). LEDGER's RULINGS.md, PLAN.md, the order ledger (production/orders/2026-10-25.md), P5, Studies 4 and 5, vignette-scene.json, kit-materials.json, street-wear.json, 4-BUDGETS.md, and the reviewed wear study (scratchpad mafia-wear/WEAR-2026-10-28.md). Nothing was extracted, FModel was not opened, no key file was read, and nothing was written except this file. All measuring was done with my own inline Python, run on those files.

**Unreachable.** F:/LedgerTools/aaa-study/mafia/wear-2026-10-28 is gone; it was deleted after its review, under the 28 October extract rule. That folder held palermo_decals.csv, masters.json and the wear export. 611 of the 1,611 meshes and 242 of the 2,247 material instances in kit_main.json came from it, and those are the ArchB elements, the street's commonest pieces. For those, the derived kit_main.json was checked rather than the raw files. The decal claims could not be re-run at all.

## Reproduced (my own scripts give the same answer)

- **Placements.** 33,983 placements of 432 meshes, plus 3 with no mesh. Back street 19,429 of 280. Bounds read for 380 meshes, which hold 32,798 placements (96.5%). 1,554 export files; 45 MB.
- **Shells.** 299 placements of 26 facade meshes, 154 of them floor shells. House 03 is placed 31, 28 and 32 times, with floor shells 4.5 and 5.5 m. Floor shells run 3.9 to 5.9 m and widths 7.8 to 17.2 m. The Elements folder holds 29,900 placements.
- **Family table.** Exact for balcony 35/10,110, window 77/7,579, corbel 7/2,977, pillar 19/2,020, ground 12/513, corner 3/176 and plaster patches 10/643. The other rows differ only by how names are sorted into families.
- **Grid.** My own wall grouping, independent of the study's, gives a storey step of 4.08 m (middle half 3.69 to 4.26, 336 steps) and a pitch of 3.99 m (3.35 to 4.33, 264 steps). The study's files give 4.08 m and 3.69 to 4.26 m from 344 steps, and 3.99 m and 3.34 to 4.33 m from 244 steps. Back street: 4.13 to 4.17 m and 4.05 m.
- **Scale.** 61.7% at scale 1, 6.2% within 5%, 6.8% at 5 to 10%, 25.3% beyond. Windows and doors 64% at scale 1 plus 24% within 10%. Ledges 35% at scale 1. Pivot on the bottom face: 57.2%.
- **Names.** Within the study's own pattern: 396 dimensions, 96/72/60%, 120 (82), 240 (74), 60 (57); name against bounds 90/91/36.
- **Per front.** Median width 9.8 m, 32 pieces, 15 meshes, 12 families. House families 62 to 94 meshes. Plaster patches on 27.8% of fronts. Overlays median 1, p90 9, 0.72 per 10 m.
- **Plaster.** The ArchB plaster covers 45 meshes and 8,852 slot placements, with 13 variants. 141 instances are named "ovrd". The balcony beam appears 510 and 224 times.
- **Trim sheets.** 35 trim sets in the index. Trim library 3,792 of 35,423 slot placements: wood 21 meshes and 3,513, blinds 171, paving 108.
- **Texel density.** 34,291 slot placements; authored 1,131 (965 to 3,569); cooked 575 (487 to 1,785). By kind, cooked: shells 552, windows 507, style 641, wear 690. Wood window and shutter pieces sit at 204.9 to 209.2 cm per UV unit, 82% of placements. Of 1,945 textures, 60% half, 18% quarter, 22% full.
- **Wear.** Vertex colour 90% of placements read; vertex-blend master 54.5%. Shutters 186 brown, 46 grey, 36 unset.
- **Decals.** 8 decals on one building; none on the back street.
- **Unreal 5.8.** The grammar syntax ([ ], count, *, +, {A:2}, < >), PCGGrammar.h:54-58, the parser's tokens, the submodule fields Symbol, Size and bScalable, the seed attribute, bAcceptIncompleteSubdivision (PCGSubdivideSegment.h:51), the core data table element, Export Selected Attributes (binary or JSON, editor platforms only), and PCGPrimitives marked IsExperimentalVersion true. The demo strings "L1, L2*, L3" and "C,W,Win*, D, Win*, W, C-". The skill text on slots, "is corner" and the cascading corner grammar C90* to C2*.
- **LEDGER values.** brick_course_m 0.075, brick_length_m 0.215, storeys 3.4 and 2.8 m, window 0.85 m. street-wear.json carries a seed, brick set, tint and wear per bay.

## Faults

**F1. Variant swap share (§2, §5.2).**
- Words: "274 of 726 instance groups, holding 8,591 placements (25%), draw their mesh with a sibling variant of its material"; §5.2 "as Mafia's 25%".
- Measure (read OverrideMaterials in the street-group export, compared with each mesh's own slot materials):
  - 274 groups carry an override, and they hold 12,010 placements (35%).
  - 8,591 is the override *slot*-placements count. Divided by 33,983 placements, it mixes two units.
  - 45 of the 274 groups (4,564 placements) "override" with the mesh's own default material.
  - Real swaps: 229 groups, 7,446 placements (22%).
  - Swaps to a same-name or same-parent sibling: 136 groups, 5,229 placements (15%). The rest go to unrelated materials: green plaster patches on another master, ArchD plaster on Opera ornaments.
- Correction: "229 groups (7,446 placements, 22%) draw a different material from the mesh's own; 15% a sibling variant." Use that in §5.2.

**F2. "15 meshes a front" is per shell piece, not per building front (§1, §5.1, §5.5.3).**
- Measure: overlays_per_front.py treats each shell instance (a base or one stacked floor) as a "building", over 271 shell instances.
- I grouped stacked shells by position (within 50 cm) into about 96 buildings and re-ran the same assignment rule. A whole building front, median, carries 110 pieces, 28 distinct meshes and 24 families (p90 49 meshes). Per shell front: 33, 15 and 12, which reproduces the document.
- Correction: say "per storey band (shell piece)". State Mafia's whole-front median as 28 meshes. Re-base §5.1 ("25 or fewer per family" sits below Mafia's single-front median) and give §5.5.3 a threshold.

**F3. Floor shells (§1).**
- Words: "plus up to two floor shells that stack on it".
- Measure: grouped shell stacks. ArchD House 07 stacks a base, Floor_a2, Floor_a2 and Floor_b (15 times). ArchB House 03 stacks a base, Floor_a, Floor_a and Floor_b (7 times). House 04 is the same.
- Correction: "one to three floor shells, the middle type repeated", which is Epic's "L1, L2*, L3" exactly. That strengthens §4's fit.

**F4. Size-named share (§1).**
- Words: "217 of 457 element meshes (47%)".
- Measure: names_pivots.py's pattern "_(\d{2,3})cm" needs an underscore, so it misses names such as BalconyRailing120cm and LedgePlaster160cm (29 meshes).
- Corrected: 246 of 457 (54%); 425 dimensions; 96% multiples of 10 cm, 72% of 30 cm, 60% of 60 cm. Commonest: 120 (89), 240 (74), 60 (59), 90 (29), 180 (24), 140 (20).

**F5. Ledges "stretched" (§4).**
- Words: "stretches 64% of ledges".
- Measure: scale on each ledge's long axis, from the bounds. Of 4,660 ledge placements: 35% unscaled, 25% longer, 23% shorter, 17% scaled only across their section.
- Correction: "scales 64% of ledges: a quarter lengthened, a quarter shortened".

**F6. Wall-library slots per shell (§2).**
- Words: "Shells take three to six slots of that library each".
- Measure: slot lists of the 26 shell meshes. 1 to 4 slots are wall-library (MI_Wall*), 3 being the commonest; 1 to 9 slots in all.
- Correction: "one to four wall-library slots (most often three), one to nine slots in all".

**F7. Trim coverage leaves out the ironwork trim (§2).**
- Words: "cover 3,792 of 35,423 slot placements (11%)"; "an ironwork trim material serves door grilles and window gratings".
- Measure: texel_main.json. MI_Trim_IronWork_* (texture T_Trim_IronWork_01_a_D, 2048 authored, 1024 cooked) serves 26 meshes and 5,321 slot placements: the ArchD 60 cm balcony railing (2,886), ArchA railings, wall ties, ironwork arches, corbels and gratings.
- Correction: "11% from the trim library, plus 15% from the ironwork trim, 26% in all"; the ironwork trim mainly serves balcony railings.

**F8. Decal bottom-edge bands contradict the reviewed wear study (§3, §5.3).**
- Words: "42% start at the wall's foot (30 cm or less), 25% at 0.3 to 1.5 m, 18% at 1.5 to 4 m, 15% higher"; §5.3 "one foot band ... (Mafia: 42% of wall decals start there)".
- Measure: the CSV is deleted, so this cannot be re-run. The reviewed WEAR-2026-10-28.md, after its fix F2, gives 30%, 18%, 21% and 32% on 595 street wall decals that have a street level. It adds that boxes at the base are mostly full-height leak stains, not foot bands.
- Correction: use the reviewed figures. Drop "foot band" as Mafia's practice; if it stays in §5.3, mark it as ours (I).

**F9. Trim budget (§5.2).**
- Words: "two sheets of 4096 × 2048 at 512 px/m ... This is the existing budget (4-BUDGETS.md)".
- Read: 4-BUDGETS.md line 158 says "three shared 4096×2048 trim sheets at 512 px/m".
- Correction: say three, or record in DECISIONS why it is two.

**F10. The advanced template misread (§4).**
- Words: "The advanced template stacks priority lists of wall and window widths, XL to S".
- Read: the strings in SGD_Bldg_Advance_Template use "[Column,Wall_XL,Wall_L,Wall_M,Wall_S]". In the skill's own syntax table, [ ] means "place A and B together, once", and priority is "< >".
- Correction: "groups the four widths in [ ]". How the Primitives code applies them is not read (U).

**F11. The optional container is answerable (§2).**
- Words: "Whether the full size ships in an optional container was not checked (U), so the in-game median lies between 575 and 1,131 px/m."
- Read: the kept index lists one .uptnl file in the whole game (a world map). The trim sheets ship .uasset plus .ubulk only.
- Correction: the cooked size is what ships, so the in-game median is about 575 px/m. Mark this R.

**F12. Decal layers per house type (§3).**
- Words: "Three ArchB house types have their own decal layers by name".
- Measure: the index holds "Decals_HLODLayer" for 14 level instances: ArchB 08, 09 and 10; ArchC 02, 04, 06, 09, 10, 11, 12, 15 and 17; a Moorish ruin; a Porto house.
- Correction: "14 level instances, including three ArchB types".

**F13. Measured (M) figures with no script in the kept folder.**
- Figures: the family table, scale shares, variant swap, trim coverage, vertex-colour and world-noise shares, "15 within 3 m", wall-decal size and fade.
- None of the 14 kept scripts computes them, and the grid's 2.5 to 6 m step filter is written nowhere. I reproduced most of them, but "15 decals within 3 m", "1,854 wall decals" (decals_main.json says 1,849), "3.0 × 3.1 m, 24 cm deep" and "Opera 135" cannot be checked now.
- Correction: add the scripts, or tag those figures "M (script not kept)". Write the step filter into the grid line. Point the decal claims at the reviewed wear study, or mark them unverifiable since its folder was deleted.

**F14. World-position noise (§3).**
- Words: "36% of placements use the plaster whose switch ... is on".
- Measure: 35.6% of read placements have a slot with the switch on. Plaster accounts for 30.5% and other materials 5.1% (stone, door frames; 97 instances carry the switch).
- Correction: "31% plaster, 5% other materials".

**F15. Cut volume and hidden pieces (§1).**
- Measure: SM_CutVolume_01a's group is bHiddenInGame and bVisible false. In all, 1,347 placements never render: the cut volume, collision shells and distance (HLOD) proxies.
- Correction: say the cut volume is a hidden generator helper (its use is still U). Note that 32,636 placements render.

**F16. Small errors.**
- House 03 is 1,484.6 cm high, so 14.8 m, not 14.9.
- About half of ledge placements (2,410 of 4,660) pivot at one end; the rest are centred, mostly corner pieces. Ledge lengths also include 50, 110, 150, 160, 200 and 250 cm.
- In the wood sheet, the window wing 60×240_01 (318 placements, 152.5 cm per UV unit) is a window leaf, not a door or small shutter.
- Trim sizes: besides the newspaper sheet, sets are 1024 (including the blinds sheet used on the street), 2048×1024, 1024×2048 and 1024×512.
- Primitive Cross-Section sits under "in core PCG", but Epic's page says it needs the Geometry Script Interop plugin.

**F17. Fit with his rulings (§5, §5.6).**
- RULINGS.md line 20 (25 Oct): phase 5's "design is written during phase 2; until then only its research". Line 17: phase 2 waits on phase 1; 28 Oct: "no new shops".
- Section 5 is a design with a first use on "the block beside Quay Street", and that includes a shop house with a shopfront bay. The document never says when that first use runs.
- Correction: label §5 a proposal for phase 2's design. State that the first use waits for phase 2, or goes to him as a deliberate scope change naming what it displaces. Drop the shop variant, or ask him.

**F18. Fit with P5 (§5.4).**
- P5 step 5: "saved static, streamed by cell", with "a new saved, partitioned level" a scope item for phase 5's design.
- §5.4's "instanced at load" keeps run-time spawning and does not mention that open item.
- Correction: name the choice and send it to the design.

**F19. Core reference missed (§4, §5.4).**
- The core, non-experimental PCG plugin ships a grammar building sample (PCG/Content/SampleContent/Grammar: GrammarSample.umap, PCG_BuildingSample, PCG_Wall/Window/HoleWindow/Column).
- Duplicate Cross-Section is the core node that stacks floors by a grammar along an extrude vector. §5.4 needs it before "Subdivide Segment per floor slot" but does not name it.
- Correction: name both. Copy structure from the core sample, under the same licence caveat as for the Primitives.

**F20. Reuse first.**
- kit-materials.json already has a "brick" kind, so only "render" is new.
- D13's asset checks (asset-budgets.json, asset_checks.py) exist and §5 does not use them.

**F21. Missing numeric checks (§5.2, §5.5).**
- No budgets: 4-BUDGETS gives a module ≤ 8,000 triangles and ≤ 4 materials, a frontage ≤ 150,000 triangles and ≤ 12 materials. P5 gives a packaged walk of 16.7 ms median and a 6 GB card.
- No tolerances for "overlaps, floating, buried, blocked door" (for example 1 cm, 2 cm, a 0.9 m clear door).
- "Counted against Mafia's 15" has no pass line (and see F2).
- The per-house variety swap has no target.
- The wall master's tiling scale has no check.
- The fade size is set by eye.

**F22. The decal rule against the findings (§5.3).**
- At most one leak per upper sill, one per downpipe, one foot band and one or two patches comes to roughly 5 to 8 decals per 6 m front.
- The document's own finding is that generated fronts carry almost none, and the wear study gives a median of 1 per street wall.
- Correction: state the expected total, and justify it as authored density for the walked path, or cap it.

**F23. Hours (§5.6).**
- "33, ceiling 40" is not plausible.
- The order ledger's own record is a median of 9 gate rounds and 26 reviews per piece over ten gates (D13). Yet six judged views (three variants, day and night) get 3 hours.
- Two new 4096×2048 trim sheets plus a wall master get 6 hours, and about 25 modules re-gridded and re-UV'd get 8.
- Missing: the packaged build and AI tester walk, the period-target reviewer against photographs (8 Oct rule), D13 asset checks, LODs and collision, his page, timelog and RECIPE.
- Correction: about 50 to 70 hours (I), or keep 33 as "build only" and add the gate rounds separately.

## Verdict

Verdict: pass with fixes. About 85 numbers re-measured or re-read; about 66 reproduce, 11 are wrong (F1, F3 to F7, F9, F12, F14, F16) and 8 cannot be checked since the wear folder was deleted (F13). 23 faults; the ones that bear on the method are F1, F2, F8, F17, F21 and F23.
