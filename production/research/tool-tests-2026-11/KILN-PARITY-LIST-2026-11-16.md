# Kiln against Marvelous: the parity list (16 November 2026)

For n16-1 (advisor 166, his pick A: Kiln's parity list beside M7's count in every round report). Each line: what Marvelous does for us today, where Kiln stands, the evidence, and the milestone that closes it. Updated at every round report.

Method researched: KILN-EVALUATION-2026-11-16.md (the judge's numbers, rounds 1 to 9) and TOOLCHAIN-CORE-DESIGN-2026-11-13.md (M5 to M7).

**M7 count: 0 garments of the Hook's list passed through Kiln; total not yet counted** (the list's rows mix new pieces, refits and variants; counted when the breadth set is costed).

| What Marvelous gives us | Kiln today | Evidence | Closed by |
|---|---|---|---|
| Layering (one garment over another) | jacket over jumper met, 0 seen through; margins thin (through over 3 mm 124 of 133, worst edge 2.88 of 3) | round 9, M4 | M5 on the cast |
| Sewing (seams, bands, cuffs, zips) | seams close inside each step; zip line wavy, collar ripple, armhole puckers named by reviewers | rounds 3, 6, 9 | shortfall work inside M5 |
| Fabrics (presets per cloth) | nine presets (cotton, jersey, wool, denim, leather, silk, linen, nylon, stretch); per-fabric numbers only from presets | cloth/src/fabrics.rs | breadth set's wool, nylon, cotton jobs |
| Poses and sitting | walk, sit, arms up tested on refits only; no drape in a sitting pose yet | job test_poses | M5 (the heavy body sitting), the skirt |
| Pressing and pleats | none: no pleat tacking or pressed crease | not built | the breadth set's pleated skirt |
| Women's garments and bodies | refits to women's bodies only (Sheila's blouse and cardigan); no woman's garment draped from a pattern | sheila-layers-to-cast job | the skirt; a held-back job |
| Long loose parts (coat tails, skirts) handed to Unreal's cloth | none | not built | M6 |
| Export to Unreal (skinned mesh on the MetaHuman skeleton) | rigged refits exported; no Kiln drape walked packaged yet | M5 not started | M6 (one outfit walked packaged) |
| Speed | 66 to 144 s per job, within 1.2x of Marvelous; processor only | evaluation table; FoldCraft read | the card path port (FoldCraft read) |
| Close-up look | counts beat Marvelous everywhere; by eye Marvelous still better close up | milestone reviews | M5 and M6 reviews |
