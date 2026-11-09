# Review of CROWN-FIX-PLAN-2026-11-09 (n09-7), 9 November 2026

Verdict: PASS WITH FIXES.

## Checked and holding

- HairStrandsEnvironment.cpp: SkyLighting at 38, IntegrationType 63-64 (0 AdHoc, 1 Uniform, 2 SH, default 2) and its switch at 336-340, ScreenTraceOcclusion 66-67 (default 0) and 393, ScatterSceneLighting 34-35 and 499-521 (adds light only). All as cited.
- HairStrandsDeepTransmittanceCommon.ush 13-19 (count 0, visibility 1): holds.
- HairStrandsVoxelization.cpp: the Environment scale falls back to the global scale when it is -1 (line 56), so DensityScale.Shadow=0 does not zero it. Holds. Citation fix: the static is at line 43, not 45 (the cvar is at 49).
- VirtualShadowMapArray.cpp 160-162 (default 0); GroomComponent.cpp 1786-1795 SetHairRootScale (public, not editor-only, clamps 0-10); HairStrandsVoxelRasterCompute.usf 727-730 coverage by radius.
- DefaultEngine.ini: line 104 is Shadow=0; 105-106 is only a comment that type 1 was refused, so the sky light is at the default. Holds.
- Forum links all reached (200). 2709070: Epic's Tim Stullich, 24 Feb 2026, UE 5.7.2, "no good solution", probes leak indoors; holds. 1852498: type 0, "Problem solved", 5.3, no Epic reply; holds. 2660465: the 0.08 multiply, confirmed by the poster; holds. 2533751: no cvar named; holds. Epic doc pages were not fetched by this review.
- TRIED-ARCHIVE.md has no "crown" line. The earlier tries are in DECISIONS (3 Nov 10:39, 11:41, 11:59), HAIR-TEST-RESULT (cards) and HAIR-NEAR-DARK (type 1). All match the plan's list.

## Fixes

1. **Step 0 cannot tell the causes apart.** The cited thread says SkyLighting 0 leaves hair "broken and very dark". A crown at or under 99 is then near-certain whatever the cause, so the rule "at or under 99 means cause 1" decides nothing. Add a second reading, for example the side hair or a hair-free skin patch, or require the street-to-office gap to close in proportion. State what a "not cause 1" result would look like.
2. **Misattribution.** "Broken and very dark" is the original poster's words, not Epic's (the plan's Rejected list implies a finding).
3. **Same lever as a tried one.** Try 1 is the same cvar as 7 Nov's try, at another value. It is not the same method (voxel hair count against a uniform sample), and HAIR-NEAR-DARK had listed "1 or 0". But 2709070's own users advise type 1, and type 1 failed on the cast. Name type 0's risk of the same cast fault, and note that the cast bar (10 levels) is unsourced.
4. **Counting.** The plan itself notes these are tries five and six. Both need his yes, or one ask, before any build. Step 0 should be said to need that too if it costs a package run.

## Measurement step

The step runs the packaged copy with -dpcvars and -OfficeLook. It edits no project file, ini or asset, so it changes nothing in the game. Caveats: the pictures go to Saved/OfficeLook, and the packaged copy must be a current build.

## Try 2

New method, not tried before. The values 1.5, 2 and 3 are unsourced. The plan marks them so.
