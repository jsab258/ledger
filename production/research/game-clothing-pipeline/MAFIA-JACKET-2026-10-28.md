# One Mafia jacket at the wrist, collar and hem (28 October 2026)

Jafar's order of 28 October: pieces, how the cuff joins the sleeve, and how the mesh is built and weighted to bend at the wrist and elbow. Method only, never assets. Revised after review (see the end).

## Sources

Untagged figures come from the kept jacket folder, F:\LedgerTools\aaa-study\mafia\jacket-2026-10-28 (four LOD meshes and the normal map), read on 28 October. Tagged figures come from Study 6's property exports of 25 October, read on 28 October.

| Tag | File |
|---|---|
| S1 | Characters\Male\Clothing\Top\VestJacket_004\SK_Ma_VestJacket_004.json |
| S2 | its Materials\MI_Ma_VestJacket_004.json, plus 14 sibling instances |
| S3 | its Textures\*.json |
| S4 | Characters\Male\Skeleton\ABP_Male_PostProcess.json |
| S5 | Characters\Male\Skeleton\PHYS_Male_Clothing.json |
| S6 | F:\LedgerTools\aaa-study\mafia\study-6\presets.csv and outfit_datatable_rows.csv |

S1 to S5 sit under F:\LedgerTools\aaa-study\mafia\exports\MafiaTheOldCountry\Content\Nero\.

## The jacket, and why

**SK_Ma_VestJacket_004** (Male/Clothing/Top): a lounge jacket over a waistcoat, shirt front and bow tie.
- **Common and plain:** 26 presets and 16 outfit rows name it [S6]; one material, 15 colourways [S2].
- **Skinning only:** it sits on the shared male skeleton, with no garment animation blueprint, cloth or morphs [S1; no morph chunk in the meshes], so the wrist and elbow come from skinning alone.
- **Study 6's anchor jacket.**

## How it was read

- **Reader:** our own reader, in Python and numpy; joints were checked against the weighted vertices, within 1 to 4 cm.
- **Methods:** section (a plane cut); ray (wall thickness by an inward ray); crossings (edges cut by a plane, about 2 per quad); shares (weight-sum per bone).
- **Units:** "t" is cm from the elbow joint along the forearm; the hand joint is at 27.25.

## 1. Pieces

| | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| Triangles | 19,131 | 8,509 | 4,781 | 1,505 |
| Vertices | 12,226 | 6,109 | 3,758 | 1,467 |
| Screen size [S1] | 1.0 | 0.4 | 0.15 | 0.08 |
| Most influences | 8 | 8 | 4 | 4 |

- **One section and one material slot at every level of detail (LOD).** LOD1 to LOD3 are flagged as reduced in the engine [S1]; LOD2 is 25.0% of LOD0.
- **37 separate pieces at LOD0:**
  - **The main shell** (7,172 positions, 14,312 triangles): jacket, waistcoat, shirt front and collars as one nearly closed surface. It has 10 small holes (49 open edges) and one non-manifold edge. None of them is at a sleeve end, the hem or the neck.
  - The bow tie, in two pieces: 1,266 and 64 triangles.
  - **Two shirt cuffs:** closed bands of 578 and 532 triangles.
  - A chain, in two pieces: 336 and 30 triangles. By shape and place it is a watch chain (unverified).
  - 21 buttons, all separate pieces: 8 sleeve (4 per sleeve, 112 triangles each), 6 waistcoat, 3 jacket front, 4 shirt.
  - A small pocket-square-like piece.
  - 8 scraps of 1 or 2 triangles, filling small holes in the shell.
- **Cuff, collar and hem bands are part of the main shell, not separate pieces.**
- **Textures:** 2048 shipped, 4096 imported [S3]. The material reads colour with occlusion, normal, and one packed map [S2].
- **The material** [S2]: a layered master's child, cloth shading, six layer IDs and a "WpoPhysics" switch.

## 2. The wrist

**The cuff is geometrically continuous with the sleeve** (section, both sleeves):
- The outer sleeve runs to a rounded lip at t = 28.73 (left) and 28.96 (right): 1.48 and 1.71 cm past the hand joint.
- It folds inward as a turned-in facing.
- A **nearly flat cap** closes the sleeve 9.3 to 9.5 cm inside the opening. Plane-fit error is 0.19 cm on the left; on the right it is 0.36 cm, with the cap tilted 10°.
- **No break in the surface.** The only seams are UV cuts, at the lip and at the cap.
- The facing uses the jacket's own fabric ID, so no lining is modelled.

**Its size:**
- **Lip-zone wall:** 0.45 to 0.46 cm on the left (ray; p10 to p90: 0.38 to 0.60) and 0.46 cm on the right (0.36 to 0.73).

**The shirt cuff:**
- A separate closed band, 10.3 to 10.4 cm long, wall 0.29 to 0.30 cm (ray), radius 2.5 to 5.1 cm.
- It starts at the jacket's cap and shows **1.0 cm (left) and 0.8 cm (right)** beyond the lip.

**Loops:**
- **About 24 to 29 quads round the forearm** (crossings: 47 to 59).
- **Rings 2.2 to 2.4 cm apart mid-forearm,** closing to about 1.0 to 1.2 cm in the last 2.5 to 5 cm (measured on edges running along the arm).
- The facing has 5 loops about 2 cm apart.
- Last 10 cm: 167 outer and 106 turned-in vertices (left), 170 and 143 (right).
- **A triangulated quad layout:** 54% of edges lie within 10° of along or round the arm.

**Rib: none on this jacket.**
- **The edge is geometry** (the lip). The normal map adds an edge band: tilt (the length of its red-green vector) about 0.2 to 0.25 at the edge, fading over 0.5 to 0.75 cm, against 0.08 to 0.12 on plain cloth.
- **No topstitch row** within 6 cm of the lip.
- **The vent is not modelled** (no inward faces before t = 19). The sleeve's back seam is a drawn line in the normal map (tilt 0.4, against 0.07 beside it) and also the UV island's cut. Four buttons sit beside it, 11 to 14° away, at t = 16.6, 19.1, 21.7 and 23.8; the last is 4.9 cm from the lip.
- **Fine wrinkles above the cuff are baked** into the normal map.

**Lower LODs:**
- Facing and cap last to LOD2.
- At LOD1 sleeve buttons become 4- or 8-vertex pieces; by LOD2 they are gone.

## 3. The collar and the hem

**The collar is part of the main shell:**
- The jacket collar folds over (about 161.5 cm); its inner side runs into the fused shirt collar, which tops out at 162.9.
- The inner neck surface slopes to a flat cap at about 153 to 153.5 cm.
- **Walls (ray):** 0.93 to 1.05 cm median at the back collar (p10 to p90: about 0.7 to 1.4); lapels 0.54 to 0.55 cm.
- The roll line and lapel edges are drawn in the normal map.

**The hem:**
- **A closed U-fold.** Below the waistcoat the skirt has a second, offset wall 0.61 to 0.62 cm in (ray; p10 to p90: about 0.45 to 0.69), its loop heights matching the outer wall's (median difference 0.08 cm).
- That inner wall is a lining rising about 38 cm, to where it turns into the waistcoat's back.
- Above it the torso is one surface, sealed by hidden caps: the waist cap at about 105 to 108 cm, and the neck cap.
- **Loops:** rings 1.05 to 1.7 cm apart in the bottom 5 cm and 2.6 to 2.8 above; 40 to 48 quads round each wall.
- **Drawn, not modelled:** a line peaking 0.75 to 1.0 cm above the fold (median tilt 0.28), the panel seams and the pocket flaps.
- **Modelled:** the centre-back vent, as two overlapping walls.

## 4. Weights

**The skeleton:** 272 bones (the file shows 297, of which 25 are sockets), with helper joints under "correctiveRoot" and offset parents (MetaHuman-like names; unverified). The jacket weights 96.

**Twist joints:** lowerarm_twist_02 at t = 9.1 and lowerarm_twist_01 at t = 18.2.

**upperarm, lowerarm and upperarm_twist themselves carry exactly zero weight.**

**Influences:**
- At most 8 per vertex, a mean of 5.13; 2,061 of 9,884 positions use 8.
- Stored in exact 1/255 steps; 4 at LOD2 and LOD3.

**Bone shares along the left forearm** (the right matches within a few points):

| cm from elbow | Shares |
|---|---|
| 0 to 3 | twist_02 36 to 40%, upperarm_twistCor_02 29 to 31%, elbow helpers 4 to 9% each |
| 3 to 6 | twist_02 76%, lowerarm_fwd 8% |
| 6 to 9 | twist_02 87%, twist_01 9% |
| 15 to 18 | twist_02 52%, twist_01 48% |
| 21 to 24 | twist_01 75%, twist_02 22% |
| 24 to 27 | twist_01 57%, hand 20%, wrist_outer 9%, twist_02 8%, wrist_inner 4% |
| 27 to 30 | hand 59%, twist_01 15%, thumb_01 13%, wrist_outer 10% |

**The cuff:**
- **Jacket cuff, last 2 cm of the shell:** hand 59%, twist_01 13 to 15%, thumb_01 13 to 18%, wrist_outer 7 to 10%.
- **Shirt cuff:** twist_01 41 to 45%, hand 30 to 34%, twist_02 11 to 12%, thumb_01 6 to 8%, wrist_outer 5%.
- **Buttons:** 18 of 21 have one weight row on every vertex (exactly rigid); the other 3 are near-rigid.

**The elbow** (bent 38° in the bind pose):
- **Inner crook (±5 cm):** upperarm_twistCor_02 39 to 43%, twist_02 28 to 34%, **lowerarm_fwd 14 to 15%**, upperarm_bicep 4 to 12% (depending on the region).
- **Elbow point:** twist_02 30 to 43%, twistCor_02 25 to 35%, **lowerarm_bck 16 to 26%**. (These depend on the wedge chosen.)
- **The blend is not wider at the crook.** The forearm side's share goes from 10% to 90% over **about 4 to 6 cm at the crook**, against **5 to 8 cm at the point**. These are the review's figures, from four methods; the crook is the narrowest of 12 directions.
- **The crook's density is real:** vertices 0.35 to 0.53 cm apart along it, against 0.67 to 1.29 cm at the point. That is modelled fold geometry.

**What the files show of the drivers** (from property files only; how the game uses them was not read):
- **The male skeleton's post-process graph [S4]:**
  - 15 RBF pose drivers posing helper joints from pose assets: lowerarm drives the elbow helpers, bicep and tricep; hand drives the wrist helpers; upperarm drives its twistCor joints and helpers.
  - One Control Rig node (Rig_Male).
  - Two rigid-body nodes, using S5 and a weapons asset.
  - None of them names the forearm twist joints.
- **Not read:** which mesh runs it.
- **S5:** 30 bodies (18 flap bones plus 2 flap offsets simulated, 10 kinematic colliders) and 28 constraints.
- **This jacket's own physics asset** is the shared PHYS_Male [S1].

**Hem and collar weights:**
- 20 flap bones carry weight on this jacket. At the lowest 3 cm, 12 carry more than 1%. The flap share is 88% at the global lowest 3 cm and 69% along the hem line, with a mean of 7.0 influences.
- The collar: neck_twist_01 76%, spine_04 20%.

## 5. How it was made, from the files

- **No tool names or import paths survive** [S1 to S3].
- **A retopologised quad layout,** triangulated; the skirt lining is an offset copy of the outer wall.
- **Vertex colours:** one channel holds eight IDs, one per sub-garment, fitting the material's layer IDs (inferred). A second channel is set only on the chain (purpose unverified).
- **UVs:** 176 islands, median 11.9 px/cm at 2048 (p10 to p90: 10.4 to 13.3). Neck and torso caps get 2.8 to 3.9 px/cm, sleeve caps 6 to 9. A second UV set (79 cm per unit) is probably for tiling fabric (unverified).

## What LEDGER should copy (method only)

1. **Close every visible edge.** Sleeve end: outer sleeve, a rounded lip about 0.45 cm, a turned-in facing about 9.5 cm, then a cap. Close the neck and torso with hidden caps.
2. **The under-garment's cuff is a separate thin closed band** (0.3 cm wall, about 10 cm long), showing about 1 cm.
3. **A second, offset wall wherever the inside can be seen:** the sleeve facing for about 9.5 cm, and the skirt lining for about 38 cm up to the waistcoat. Edges about 0.45 to 0.6 cm thick; lapels 0.55, collar about 1. Elsewhere one surface, closed by hidden caps.
4. **Loops:**
   - about 26 quads round the forearm;
   - rings about 2 cm apart, closing to about 1 cm in the last 2.5 to 5 cm before an edge;
   - denser vertices in a crook (about 0.4 cm apart) for its folds;
   - quads, triangulated at export.
5. **Skin to twist and helper joints, not the main limb joints.**
   - Two forearm twist joints in three zones, with the hand taking over in the last 2 to 3 cm.
   - A short elbow blend of about 4 to 8 cm, no wider at the crook.
   - Front helper about 15% at the crook, back helper about 15 to 25% at the point.
   - Up to 8 influences at the top two LODs, 4 below; rigid buttons.
6. **The helpers carry the bend's corrections,** and something must drive them. Mafia's skeleton graph holds RBF pose drivers for this [S4], read from its file only. Check how LEDGER's MetaHumans drive theirs in the packaged game.
7. **Hem and skirt weighted to about 20 flap bones** (69 to 88% at the hem), named as simulated bodies in a clothing physics asset [S5]; not cloth.
8. **Geometry for** edges, buttons, vent overlaps and big folds. **The normal map for** seams, the hem line about 1 cm up, pocket flaps, wrinkles and an edge band of 0.5 to 0.75 cm.
9. **One material with per-part IDs in vertex colour.** Even density of about 12 px/cm at 2048 (author at 4096). Hidden caps get less texture space. Cut UVs at the lip, at the cap and along the sleeve's back seam.
10. **LODs:** keep the facing and cap to LOD2, drop sleeve buttons by LOD2, use 4 influences from LOD2.

## What could not be read

Motion (nothing was posed); the pose assets' targets and the Control Rig, including what sets the twist joints; which mesh runs S4; the material graph (which UV tiles, how IDs pick layers); the vertex-colour byte order; the body under this outfit and whether it is cut; the source tools; the colour and packed textures.

## Record

- **Disk:** 8.7 MB in the jacket folder (meshes 2.8 MB, normal map 4.1 MB, pictures 1.8 MB), kept for review.
- **The key:** put into FModel's settings by script for four runs, blanked after each, confirmed blank.

## Review applied (fresh reviewer, 28 October; pass with fixes, 16 faults)

- **F1:** elbow blend restated and copy item 5 changed; my 10.4 cm crook figure is withdrawn (its distance measure fails on the crook side).
- **F2:** drivers and physics sourced to S4, S5 and S1, read from files only; item 6 is now a check.
- **F3:** "body cut" dropped.
- **F4:** item 3 reworded.
- **F5:** sleeve caps 6 to 9 px/cm.
- **F6:** second bow-tie and chain pieces added.
- **F7 to F15:** shell "nearly closed", LOD1 buttons, 18 of 21 rigid, ring spacing, band tilt, cuff region, point shares, per-side figures and about 20 flap bones corrected.
- **F16:** Study 6 files named.
