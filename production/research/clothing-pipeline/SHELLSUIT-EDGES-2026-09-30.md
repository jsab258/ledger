# Clean openings, collars and trims on a scripted garment (research note, 30 September 2026)

The clothing session asked for this after the shell-suit jacket failed its second review with the same edge faults as the cardigan and jumper. A separate helper was given the problem, not a theory, and worked read only for about twenty-five minutes. Every source was read on 30 September 2026. **D** means documented, with its source; **I** means the helper's inference. "Search summary" means only a search engine's summary was seen. It does not repeat CARDIGAN-BUILD or JUMPER. Polycount, PatternReview, Hey June and the ACM paper page refused; the Genies page was gone.

## In short

- **Third and last attempt (I, from A to C).** Build edges first, never cut:
  1. Keep the passing shell only as a hidden shape target.
  2. On it, draw every edge as a curve: hem, cuffs, neckline (base of neck, 1.5–2 cm lower at the front), each front's zip edge (straight to the zip end, then opening into the V), and the side and raglan seams.
  3. Make each panel (two fronts, back, two sleeves, the raglan panels) a quad patch between its own four curves, with equal point counts on shared curves (`grid_fill`, or your own blend of the four sides). Weld shared curves. Colour panels are then whole patches with straight joins.
  4. Project the inner points onto the target (Shrinkwrap, Target Normal Project, plus ease). Relax inner points only; borders stay on their curves.
  5. Grow every trim from its border row with `extrude_edge_only`: collar up from the neckline; zip strip and facing from each front edge; waistband and cuffs from the hem and cuff rows, drawn in and turned 1.5 cm inside.
  6. Weight this single-sided mesh (section C), then Solidify, 2 mm inward, with Rim Fill, so every edge closes and the layers share weights.
  7. Test with Preserve Volume off and no Corrective Smooth.
- **The collar's front edge is the top of the zip edge (D [P3], I).** The zip's top is "tucked into the collar", so edge and collar end are one line. The corner where zip edge, neckline and collar meet must be one shared point.
- **A stand collar follows the neckline (D [P1][P2]).** Its lower edge curves up about 2 cm towards the centre front, and its front end rises vertically. Built as a ring round the neck, it reads as a hood with square side corners (I).
- **Height:** about 4.5 cm for a stand (search summary [P4]); a shirt stand is 3.2 cm [P1].
- **Game practice (D [G1], search summary [G2]).** Model visible hems, cuffs and open edges, extruding one row at collar and sleeves to fake thickness. Put loops round the shoulders and elbows.
- **Weights (D [W1][W2]).** Copy them only where body and garment are close and face the same way. Fill the rest smoothly across the garment's own mesh.
- **The game skins linearly (D [U1]).** Blender previews must do the same.

## A. Clean openings from the start

- **Cutting makes the ragged edge (I).** `bisect_plane` puts new points wherever the plane crosses existing edges [S2]. On a smoothed offset skin that gives slivers and a zigzag border, which every trim copies.
- **Voxel Remesh is ruled out (D [S1]).** It "should *not* be used" for meshes that will deform. QuadriFlow is suggested instead, but it neither cleans intersections [S1] nor puts borders where we choose (I).
- **Grid Fill makes patches (D [S1][S2]).** It "generates a grid" inside a rough rectangle of edges. It works best when opposite sides have equal point counts. This matches sewing, where each panel is its own cut piece (I).
- **Target Normal Project (D [S1])** gives "a much smoother projection" than nearest point. **I:** use it, not a copy of the body's own points.
- **Relaxing (D [S2]).** `smooth_laplacian_vert` has a separate border factor. **I:** set that to 0.
- **The stand collar (D):**
  - Its lower edge rises 3/4 in to a vertical front of 3/4 in, from a gentle curve. The top corner can be square or rounded [P1].
  - For stand collars, the neckline is lowered up to 2 cm at the centre front [P2].
- **Collar build (I).** Use 4–5 rows, leaning 10° inward with the inner face 5–10 mm off the neck. Roll the top over a 2–3 mm radius and return down the inside to the neckline. With the zip open, each half stands on its own front and parts with it.

## B. Trims that share points with the shell

- **Game practice (D).** "Model visible hems, cuffs and open edges", without a double shell where the inside is never seen [G1]. Genies extrudes one row at collar, sleeves and trouser edges, under 90° (search summary [G2]).
- **Tools (D [S1][S2]).** `extrude_edge_only` turns border edges into faces, joined to the shell. Solidify's Rim Fill makes faces "between the inner and outer surfaces" at open edges. Its Shell output group lets later steps touch only the shell.
- **Order (I).** Make the shell and all trims one mesh first, then give it thickness once. A separate strip laid on top can always part; an extruded row cannot. Solidify grown inward keeps the outside where the reviewer passed it.
- **Zip (I).** Extrude each front edge outward 5–6 mm as the tape (zip material), then inward 2.5 cm as the facing. Nothing lies between them for the background to show through.

## C. Honest skinned behaviour

- **Robust transfer (D).** The authors' code [W1] matches within 5% of the garment's bounding-box diagonal and 30° of normal. It fills the unmatched points over the garment's own points and faces, then smooths 10 times at 0.2. A GPL add-on exists but needs outside libraries [W2]; that is a licence question for Jafar. **I:** a plain numpy version (fixed matched weights, repeated neighbour averaging) is enough.
- **Fins (I).** They are weights jumping across the underarm. A transfer onto the finished mesh, filled along its edges, cannot jump, and it gives nothing to the hidden inner points. Then apply the jumper note's zones and `vertex_group_smooth` [S2] along rows.
- **Seated sawtooth (I).** Shell, band and facing each had their own copied weights, so they slid through one another. On one welded mesh, weight constant down each column through the waistband and its turn-in. Solidify then gives inner, outer and rim the same weights; check this in the script.
- **Corrective Smooth (D [S1]).** It reduces distortion after the Armature modifier. **I:** the game does not run it, so use it only as a check: where it changes a pose much, the weights are wrong.
- **Preserve Volume (D [S1][U1]).** In Blender it uses quaternions. UE5 skins linearly; dual quaternion needs a Deformer Graph, shown only in Epic's Content Examples. Keep it off.
- **Chaos cloth (I).** The builder's Chaos cloth may move the hem in the game; the Blender test judges skinning alone.

## Sources (all read 30 September 2026)

- [S1] Blender manual bundled with the Blender MCP: Solidify, Grid Fill, Remeshing, Shrinkwrap, Smooth Corrective, Armature, weight Smooth (undated).
- [S2] Blender Python API bundled with the Blender MCP: `bmesh.ops` (`grid_fill`, `extrude_edge_only`, `bisect_plane`, `smooth_laplacian_vert`), `bpy.ops.object.vertex_group_smooth` (undated).
- [G1] VK GameDev, "Clothing retopology for game assets", vkgamedev.com (1 September 2026).
- [G2] Search summary: Genies Tech Docs, "3D Modeling" (undated; page 404).
- [W1] R. Abdrashitov, K. Raichstat, J. Monsen, D. Hill, "Robust Skin Weights Transfer via Weight Inpainting", SIGGRAPH Asia 2023 Technical Communications (December 2023). Read: the authors' code, github.com/rin-23/RobustSkinWeightsTransferCode, `src/sphere_to_plane_transfer.py`, MIT (undated).
- [W2] SentFromSpaceVR, robust-weight-transfer README, GitHub, GPL-3.0 (undated); plus a search summary of how it works.
- [U1] Laura, "UE5 has dual quaternion skinning", landelare.github.io (10 October 2023).
- [P1] Cloning Couture, "Drafting a Stand Collar" (21 February 2022).
- [P2] Müller & Sohn, "Pattern construction for stand-up collar" (6 March 2023).
- [P3] Threads Monthly, "How to neatly sew a separating zip with a facing or lining" (21 February 2024).
- [P4] Search summary: Müller & Sohn, "Pattern construction for collar with stand" (undated).

Every source above was read by the helper itself, except [G2], [P4] and the part of [W2] marked as a search summary.
