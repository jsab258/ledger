# Review: JACKET-2026-10-28.md (one Mafia jacket at the wrist, collar and hem)

Fresh, independent review, 28 October 2026, about 16:00 to 17:15.

**What I used:** only the kept files in F:\LedgerTools\aaa-study\mafia\jacket-2026-10-28: the four LOD .psk files and T_Ma_VestJacket_004_N.png. Nothing new was extracted. FModel and the key were not touched. I did not read the author's scripts in the scratchpad.

**How I measured:**
- My own ActorX reader, written in Python 3.12 with numpy, scipy and PIL and run from stdin (no script files saved). It reads these chunks: PNTS, VTXW, FACE0000, RAWWEIGHTS, VTXNORMS, VERTEXCOLOR, EXTRAUVS0 and REFSKELT.
- Joints were rebuilt with non-root quaternions conjugated. That convention places hand_l at 27.25 cm from lowerarm_l; the other convention misses the weighted vertices by about 59 cm.
- Face winding is reversed against the stored normals (99.5% of faces), so face normals were flipped.

**Methods:**
- **Pieces:** connected components on the point graph.
- **Wall:** Möller-Trumbore rays cast along the negative stored normal.
- **Ring spacing:** axial length of edges that run within 15° of the arm.
- **Tilt:** the length of (2R-1, 2G-1), sampled at random points on each face through UV0.
- **Weight shares:** weight-sum per bone over a region.

**My renders** (for me only; they stay in the jacket folder): review_sections_neck_hem.png, review_hem_horizontal.png and review_vertical_sections.png, 0.23 MB in all.

## Faults

### F1. The elbow blend widths do not reproduce. The crook is not wider. (Major)
**Document:**
- §4: "The blend is wider on the crook: the forearm side goes from 10% to 90% over 10.4 to 10.6 cm there, against 5.8 to 6.5 cm at the point."
- Copy item 5: "A crook blend of about 10 cm against about 6 cm at the elbow point."

**Measure:** I defined the crook as the bisector of the two rays from the elbow (towards the shoulder, along -upperarm, and along the forearm), and the point as its opposite. My crook region gives the same shares as the document's crook (twistCor_02 39 to 43%, twist_02 28 to 34%, lowerarm_fwd 14 to 15%), so it is the same place.

The 10% to 90% width of the forearm-side weight, in cm:

| Variant | Crook L | Crook R | Point L | Point R |
|---|---|---|---|---|
| Lowerarm chain, ±15°, mean-axis bins | 5.3 | 4.8 | 8.0 | 7.6 |
| Twist joints only, same | 5.4 | 5.3 | 7.7 | 7.9 |
| First >10% to last <90%, ±15°/±30° | 4.7 / 5.7 | 4.1 / 4.5 | 6.5 / 6.6 | 5.4 / 5.6 |
| Along mesh edges (Dijkstra) | 8.7 | 6.5 | 7.7 | 6.2 |

- I swept 12 azimuths round the elbow. The crook is the narrowest sector, at 4.8 to 5.4 cm. No sector, on any variant, reaches 10 cm; the widest is 9.1.
- The point's 5.8 to 6.5 cm does reproduce on the "first >10% to last <90%" variant.

**Correction:**
- "The blend at the crook is about 4 to 6 cm, narrower than or equal to the point's 5 to 8 cm. The crook is not wider; it has denser geometry."
- Remove "a crook blend of about 10 cm against about 6" from copy item 5, or redo the measure with its definition written down: which bones count as "forearm side", and along what path.
- The crook's density claim does stand: vertex spacing along the crook strip has a median of 0.35 to 0.53 cm, against 0.67 to 1.29 cm at the point.

### F2. The pose drivers, Control Rig, rigid-body nodes and physics asset are stated as fact, with no source in the kept files. (Major)
**Document:** §4, under "What drives the helpers": "15 RBF pose drivers (Gaussian, swing angle)…", which joint drives which helpers, "One Control Rig node", "Two rigid-body nodes", "The clothing physics asset has 30 bodies (20 simulated flaps, 10 kinematic colliders)", and "whose pose every garment copies". Copy items 6 and 7 rest on these.

**Measure:** the kept files cannot show any of this. A .psk carries no animation blueprint, pose asset or physics asset.

What the files do show is consistent with these claims but does not prove them:
- The skeleton has helper joints under `*_correctiveRoot` and `*Off` parents.
- The main upperarm, lowerarm and upperarm_twist joints carry exactly zero weight.
- There are 20 `flapDyn_*` joints, and all 20 are weighted on this jacket.

"How it was read" names only "the mesh and material property files from Study 6". It does not name the post-process graph or the physics asset.

**Correction:**
- Name the source file of each claim, with its path and the date it was read, or mark the claims "unverified here".
- Reword copy item 6 as a hypothesis: "the helpers are weighted, and something must drive them; check how in our packaged game".

### F3. Copy item 2 states something that was not measured. (Moderate)
**Document:**
- Copy item 2: "…showing about 1 cm, with the body cut under it."
- "What could not be read": "The body under this outfit and its cuts."

**Measure:** none is possible. No body mesh is in the kept set.

**Correction:** remove "with the body cut under it", or mark it as the usual practice, unverified for this outfit.

### F4. "Thickness only at seen edges… Elsewhere one layer" does not fit the hem's own numbers. (Moderate)
**Document:** copy item 3.

**Measure:**
- The skirt's inner wall runs from the hem fold (z about 86) up to z about 124, where it turns into the waistcoat back (vertex ID 16). That is 38 cm, which the document itself states in §3.
- Ray wall 0.62 cm (p10 to p90: 0.44 to 0.69). Loop heights match the outer wall: median difference 0.08 cm, p90 0.17.
- Above that, the torso is one closed surface sealed by hidden caps: the neck cap at z about 153.5 and the waist cap at z 105 to 108. It is not open single cloth.

**Correction:** "A second, offset wall wherever the inside can be seen: the sleeve facing for about 9.5 cm, and the skirt's lining for about 38 cm up to the waistcoat. Elsewhere one surface, closed by hidden caps."

### F5. "Hidden caps get 2.8 to 3.9 px/cm" is true only of the neck and torso caps. (Moderate)
**Document:**
- §5: "Hidden caps get 2.8 to 3.9 px/cm."
- Copy item 9: "Caps get a corner of the UV space."

**Measure:** texel density at 2048, area-weighted per UV island:

| Cap | Faces | Area | Density |
|---|---|---|---|
| Neck cap (island 175) | 25 | 164 cm² | 3.92 px/cm |
| Torso cap (island 112) | 43 | 688 cm² | 2.79 px/cm |
| Left sleeve cap (island 174) | 21 | 82 cm² | 6.09 px/cm |
| Right sleeve cap (island 173) | 21 | 92 cm² | 9.38 px/cm |

**Correction:** "The big neck and torso caps get 2.8 to 3.9 px/cm; the small sleeve caps 6 to 9."

### F6. The piece list adds up to 35, not 37. (Minor)
**Document:** "37 separate pieces at LOD0", then the list.

**Measure:**
- There are 37 components, which is correct. The list counts 1 + 1 + 2 + 1 + 21 + 1 + 8 = 35.
- The two missing pieces are both closed by vertex-colour ID:
  - a 64-triangle piece at the neck centre, at (6.2, -0.1, 153.2), with ID 112, the bow tie's;
  - a 30-triangle piece at (13.9, 8.8, 113.6), with ID 145, the chain's.
- The 8 scraps are shell triangles sitting in holes of the main shell. 12 of the coincident-vertex groups pair a 3-vertex scrap with the shell.
- The button counts are confirmed by size and place: sleeve 8 (112 triangles each), waistcoat 6 (78), jacket front 3 (80), shirt 4 (84).

**Correction:** add "a second bow-tie piece (64 triangles) and a second chain piece (30 triangles)", and say that the scraps fill small holes in the shell.

### F7. "One closed surface" is contradicted by its own open edges, and "no seam" by its own UV cuts. (Minor)
**Document:**
- §1: "fused into one closed surface. None of its open edges is at a sleeve end…"
- §2: "Outer surface, lip, facing and cap are one shell: no seam, no overlap, no open edge."

**Measure:**
- The main shell has 49 open edges in 10 small holes and one non-manifold edge, at (13.4, 0.3, 139.0). None is at a sleeve end, the hem or the neck. The largest holes, of 10 and 12 vertices, are at the torso side (z 123) and the left front (z 137).
- At the wrist the surface is geometrically continuous, but UV islands are cut at the lip (just inside the apex) and at the cap.

**Correction:** "Nearly closed (10 small holes, none at an edge that shows). At the cuff, no geometric break; the only seams are UV cuts at the lip and the cap."

### F8. Buttons at LOD1 are not all 4-vertex cards. (Minor)
**Document:** "Buttons become 4-vertex cards at LOD1 and are gone at LOD2."

**Measure:** at LOD1, pieces within 1 cm of each LOD0 button:

| Button | At LOD1 |
|---|---|
| Left sleeve, all 4 | 4 vertices / 2 triangles |
| Right sleeve, 3 of 4 | 8 vertices / 9 triangles |
| Right sleeve, the 4th | 4 vertices / 2 triangles |
| The other 13 buttons | 5 to 14 vertices (one gone) |

- At LOD2, all sleeve buttons are gone. Small pieces of 3 to 8 vertices remain at four non-sleeve buttons.

**Correction:** "Sleeve buttons fall to 4- or 8-vertex pieces at LOD1 and are gone at LOD2."

### F9. "Each button has one weight row" holds for 18 of 21. (Minor)
**Measure:** 18 buttons have one identical row on every vertex. The other three are:
- a right-sleeve button with two rows, swapping 127/128 against 128/127 out of 255;
- two jacket-front buttons with 3 and 2 rows: 4 or 5 vertices add spine_03 and spine_04 at 3 to 25/255.

**Correction:** "18 of 21 exactly rigid, the rest near-rigid." Copy item 5's "rigid buttons" stands.

### F10. The ring spacing quoted is too low. (Minor)
**Document:** "Rings every 1.7 to 2.3 cm mid-forearm, closing to 0.7 to 1.3 cm in the last 5 cm."

**Measure:** the axial length of near-longitudinal outer edges, for t 8 to 18:
- left median 2.34 to 2.35 (p10 to p90: 1.67 to 2.65);
- right median 2.24 (2.0 to 2.5).

In the last 2.5 cm the medians are 1.17 (left) and 1.05 (right). On the right, the 2.5 to 5 cm band is still 2.03.

**Correction:** "Rings about 2.2 to 2.4 cm apart mid-forearm, closing to about 1 to 1.2 cm in the last 2.5 to 5 cm." Copy item 4's "about 2 cm" stands.

### F11. The edge band's tilt reads as upper-quartile values. (Minor)
**Document:** "Baked edge band about 0.75 cm wide…: tilt 0.25 to 0.35, against 0.07 to 0.09 on plain cloth."

**Measure:** tilt against the 3D distance from the lip apex, on the outer island including the lip roll:

| Distance from apex | Median tilt | p75 |
|---|---|---|
| 0 to 0.25 cm | 0.22 to 0.25 | 0.37 |
| 0.25 to 0.5 cm | 0.16 | |
| 0.5 to 0.75 cm | 0.11 to 0.14 | |
| Plain cloth, 1 to 3 cm | 0.08 left; 0.11 to 0.12 right | |

The width, about 0.5 to 0.75 cm, is confirmed.

**Correction:** "Tilt about 0.2 to 0.25 at the edge, fading over 0.5 to 0.75 cm, against about 0.08 to 0.12 on plain cloth."

### F12. The jacket cuff's weight shares depend on a region that is not stated. (Minor)
**Document:** "Jacket cuff: hand 42 to 45%, twist_01 28 to 33%…"

**Measure:**

| Region | Hand | twist_01 | thumb_01 | wrist_outer |
|---|---|---|---|---|
| Last 2 cm of the shell | 59% | 13 to 15% | 13 to 18% | 7 to 10% |
| Last 3 cm | 49 to 54% | 18 to 25% | | |

The document's figures fit a region about 4 cm long. The shirt cuff reproduces exactly: twist_01 45/41%, hand 30/34%, twist_02 12/11%, thumb 6/8%, wrist_outer 5%.

**Correction:** state the region, or quote the last 2 cm.

### F13. The elbow point's shares, and "back helper at about 15%". (Minor)
**Document:**
- "Elbow point: twist_02 42 to 43%, twistCor_02 27 to 28%, lowerarm_bck 16 to 19%."
- Copy item 5: "Front and back helpers at about 15%."

**Measure:** a ±25° wedge, ±5 cm along the arm:
- left: twistCor_02 35%, twist_02 30%, bck 26%;
- right: twist_02 43%, twistCor_02 25%, bck 24%.

The crook's lowerarm_fwd, at 14 to 15%, matches. The crook also carries upperarm_bicep at 10 to 12%, which the document leaves out.

**Correction:** "Front helper about 15% at the crook; back helper about 15 to 25% at the point (depends on region)."

### F14. Small figures that are slightly off, or one side only. (Minor)
| Document | Measured |
|---|---|
| Lip "1.5 cm past the hand joint" | 1.48 left, 1.71 right |
| "Right sleeve 0.42" lip wall | 0.46 median (p10 to p90: 0.36 to 0.73) |
| Back collar wall "1.05 (0.69 to 1.41)" | 0.93 median (0.72 to 1.41) |
| 0 to 3 cm row: "twist_02 36%, twistCor_02 31%, four helpers 8% each" | 40/29; helpers 9, 9, 6, 4 to 5 |
| "Last 10 cm: about 160 outer and 106 turned-in" | left 167/106; right 170/143 (the right facing is denser: 233 faces against 173) |
| "Flat cap" | Left: plane fit rms 0.19 cm, max 0.43. Right: rms 0.36, max 0.94, tilted 10° to the axis |
| Hem "about 47 quads round each wall" | outer 40 to 48, inner 41 to 44 |
| Hem rings "about 2.6 above" | 2.8 |

None changes a conclusion. Each should be quoted per side, or as a range.

### F15. "Skirts swing on a few rigid-body flap bones" (Minor)
**Measure:**
- The skeleton has 20 `flapDyn` joints, and all 20 carry weight on this jacket.
- In the bottom 3 cm (z < 86.8), 16 carry weight and 12 carry more than 1%. The 88% share and the mean of 7.0 influences reproduce exactly (7.02).
- "Rigid-body" comes from the unkept graph (see F2). The bone names only suggest it.
- Measured per azimuth along the real hem line, not the global lowest 3 cm, the flap share is 69%.

**Correction:** "about 20 flap bones (12 at the hem's lowest edge)". Source the rigid-body claim.

### F16. Facts from Study 6 files are not in the kept set. (Note)
These cannot be re-measured here:
- screen sizes 1.0/0.4/0.15/0.08;
- "reduced in the engine";
- "imported at 4096";
- all material details (layered master, masked, cloth shading, layer IDs, tiling, WpoPhysics);
- 26 presets and 16 outfit rows;
- 15 colourways;
- "normals and tangents recomputed in the engine";
- empty import source paths;
- no tool names;
- no Chaos cloth or clothing data;
- "the physics asset is the shared body one".

The PNG is 2048², which is consistent with "shipped at 2048". There is no morph chunk in any .psk, which is consistent with "no morphs".

**Correction:** name the Study 6 files, with path and read date, beside these claims.

## Re-measured and confirmed
**Triangles, vertices and influences per LOD:**

| | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| Triangles | 19,131 | 8,509 | 4,781 | 1,505 |
| Vertices | 12,226 | 6,109 | 3,758 | 1,467 |
| Most influences | 8 | 8 | 4 | 4 |

- LOD2 is 25.0% of LOD0.
- Mean influences 5.134; 2,061 of 9,884 positions use 8.
- Weights are in exact 1/255 steps (residual 1.5e-5).
- 96 bones carry weight.
- 297 bones in the file, 25 of them sockets, leaving 272.

**Pieces:**
- The main shell has 7,172 positions and 14,312 triangles. The bow tie has 1,266 triangles.
- The shirt cuffs are closed tori: 578 and 532 triangles, 289 and 266 positions, Euler characteristic 0.
- Sleeve buttons are 112 triangles each, 4 per sleeve.

**Wrist:**
- Forearm 27.25 cm; elbow bent 37.9° in the bind pose.
- Twist joints at t = 9.1 and 18.2.
- Lip at t = 28.73 and 28.96.
- Cap centroid at t = 19.19 and 19.68: 9.54 and 9.28 cm inside the opening.
- Lip-zone wall 0.46 cm (p10 to p90: 0.38 to 0.60) on the left.
- The facing is its own UV island with ID 0 (jacket); the cap is its own island too.
- Shirt cuff: 10.32 and 10.41 cm long, wall 0.30 (ray), radius 2.48 to 5.10 on the left, showing 1.02 and 0.81 cm. On the right, 9 vertices sit up to 0.18 cm behind the cap plane, which is hidden.
- Crossings of 47 to 59 give about 24 to 29 quads round the forearm.
- Edge angles: 54% fall at 0 to 10° or 80 to 90°.
- The facing has 5 loops about 2 cm apart.
- No vent geometry: no inward faces before t = 19.
- The sleeve's UV seam runs at a fixed azimuth, with a drawn line on it (tilt 0.4, against 0.07 off it).
- Buttons sit at t = 16.6, 19.1, 21.7 and 23.8, 11 to 14° from the seam; the last is 4.9 cm from the lip.
- The facing and cap last to LOD2 and are gone at LOD3.
- Shirt cuff positions: 289, then 157, then 108.

**Collar and hem:**
- Shell top 162.90, the fused shirt collar. Jacket collar about 161.5. Neck cap at z 153 to 153.5. Lapel wall 0.54.
- The hem is a U-fold: wall 0.62, loop heights matched, the inner wall joining the waistcoat at about z 124 (38 cm up).
- Torso cap at z 105 to 108.
- Hem rings 1.05 to 1.7 cm in the bottom 5 cm.
- The hem's drawn line peaks 0.75 to 1.0 cm from the fold, at median tilt 0.28.
- The centre-back vent overlap is seen in horizontal sections at z 88, 95 and 102.

**Weights:** the forearm share table matches within 0 to 2 points in every row from 3 to 30 cm.

**Vertex colours and UVs:**
- One channel holds eight IDs: 0, 16, 32, 64, 80, 112, 128 and 145. The shell uses 0/16/32, the cuffs 32, the bow tie 112, the chain 145, and buttons 64/80/128.
- A second channel is non-zero only on the two chain pieces. The other two channels are constant.
- 176 UV islands.
- Texel density: median 11.9 px/cm at 2048 (p10 to p90: 10.4 to 13.3).
- UV1: 79.1 cm per unit, area-weighted (the main shell 85). 2,010 faces have zero UV1 area.
- Normal-map mean RGB: 0.501, 0.500, 0.975.

**Record:** 2.82 MB of meshes, 4.10 MB of normal map and 1.79 MB of pictures, 8.7 MB in all.

## The copy list: does it follow from the numbers?
| Item | Verdict |
|---|---|
| 1. Close every edge | Yes |
| 2. Under-cuff band | Yes, except "with the body cut under it" (F3) |
| 3. Thickness only at seen edges | No as worded (F4) |
| 4. Loops | Yes (F10 is a detail) |
| 5. Skinning | Mostly. Remove the crook 10 cm against 6 cm (F1); the back helper reads 15 to 25% (F13) |
| 6. RBF correctives | Not shown by the kept files (F2); keep only as "check ours" |
| 7. Flap bones | Weights yes; "a few" is about 20; "rigid-body" is unsourced (F15) |
| 8. Geometry against normal map | Yes |
| 9. One material, IDs, density | Yes; caps partly (F5) |
| 10. LODs | Yes |

Everything stays method-only. No asset is copied.

## Verdict
**Pass with fixes.** About 75 figures were re-measured from the kept files, and most hold within measuring noise. There are 16 faults:
- **2 major:** F1, the elbow blend widths, which do not reproduce and point the wrong way, and F2, the pose-driver and physics claims, with no source in the kept files.
- **3 moderate:** F3 to F5.
- **10 minor:** F6 to F15.
- **1 note:** F16.

The fixes needed before this becomes a target: correct F1, then copy item 5; source F2, then items 6 and 7; reword items 2, 3 and 9.
