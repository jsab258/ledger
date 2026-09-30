# Fitting a tailored jacket without the body printing through (research note, 30 September 2026)

A separate helper, about thirty minutes, web only, given the blind reviewer's findings rather than a theory. **D** means documented, with the source number. **I** means the helper's own inference.

## The route for us

1. **Fit the jacket to a smooth "jacket form", not to the skin.** Make one form per man from his MetaHuman torso: smoothed hard, with the hollows filled (under the chest, between chest and belly, below the collarbones, down the spine) and the front falling straight from the fullest point of the chest. Professionals fit to such stand-ins. Roblox uses a body "cage" that "tells the clothing the shape of the character without all the fine details" [7], Marvelous a simulated "fitting suit" [5], Daz simple "projection templates" [10] (D). Filling hollows slice by slice, as taut cloth bridges them: **I**.
2. **Build the tailoring into the form.** A shoulder pad 1 to 2 cm thick at the shoulder point, thinning to nothing at the neck, and a firm, rounded chest (**I**). Chest ease 15 to 20 cm round for a classic or British cut [13] (D).
3. **Carry the change with a coarse, smooth warp.** Epic's resizer moves garment points and normals from about 1,500 sampled body points (1,000 to 2,500 advised) [1, 2] (D). Fewer points, or a low-resolution cage, carry only broad shape; Wrap's "Smoothness" and Lattice "Neighbours" work likewise [6] (D).
4. **Pull the jacket back towards its own designed shape.** Blender's Smooth Corrective modifier, rest state "Original Coordinates", smooths the distortion a deformation added [11] (D); the lapel roll and pockets survive because they are in the rest shape (**I**). Daz's "Base Shape Matching" smoothing does this for clothing and smooths muscle morphs out [10] (D, search summary).
5. **Move stacked parts as one.** Lapels, collar, facings and breast pocket take exactly the displacement of the panel beneath. Epic's resizer has "custom regions" for this: a marked group moves inside a box tied to a local frame, not by the general warp [3] (D). Push only the innermost layer out of the body and give every layer above it the same shift (**I**).
6. **Delete what cannot be seen:** the shirt under the jacket (keep the V, cuffs and collar band) and the body under both. MakeHuman's format does it with "delete_verts" and a stacking order, "z_depth" [12]; Roblox has "Hidden Surface Removal" [8]; Cyberpunk 2077 squashes lower layers [15] (D).
7. **Treat the two collars as one pair.** About 1.3 cm (half an inch) of shirt collar shows above the jacket collar at the back [16] (D). Fit them together with a fixed 2 to 4 mm gap, or merge the visible shirt collar into the jacket (**I**).
8. **Collide last, only where needed.** Push out only points inside the body, with a margin: Character Creator's "Margin" [9] (D); in Daz collision "should not affect any areas that are not cutting into" the body [10] (D, search summary).

## 1. How professionals transfer a garment

- **Unreal.** The resizer samples the source body ("the more points ... the more accurate to the body shape") [1], stores RBF weights, and moves positions, and optionally normals and tangent frames, from the target body's matching points [2] (D). Custom regions use trilinear interpolation in a box [3] (D). The module also has edge, bending and shear constraints, use unpublished [4] (D). At 1,500 points over about 2 m² the samples lie 3.5 to 4 cm apart, so some muscle still passes (**I**); Epic's answer is several source bodies near the targets (earlier note PIPELINE).
- **Character Creator.** "Close-fitting" smooths "the entire shape"; "Smooth" keeps "its general shape"; "Margin" sets the offset; conform weights stop seams twisting [9] (D).
- **Marvelous and CLO** re-simulate the pattern on the new avatar, resized ("Auto Fitting") or at "its original size" ("Re-Drape") [5] (D). Cloth keeping its own size cannot sink into hollows (**I**).
- **Wrap** fits coarse to fine; a coarse "Sampling Final" and high "Smoothness" keep only broad shape, then its Lattice node carries the garment [6] (D), leaving "buckling issues and sharp edges" to fix [6] (D).
- **Our fault (I).** We draw the base body onto the skin round after round, so the change we carry *is* the muscle. More smoothing afterwards treats the symptom; the target is wrong.

## 2. A tailored jacket's structure

- A horsehair canvas and felt chest piece shape a rounded chest [18] (D). CLO ships shoulder pads as separate trim; one practitioner found pads built into the avatar stop a simulated shoulder lifting off it [21] (D, search summaries). Our jacket is skinned there, not simulated, so a padded form suits us (**I**).
- Ease round the chest: slim 10 to 13 cm, classic 15 to 18, British 18 to 20 [13] (D); modern slim jackets in a 2019 study, 5 to 8 [14] (D). No game source on modelling over a padded dummy was found; Epic's "Clothing Construction Presets" are plain bodies [22] (D, search summary).

## 3. Layers close together

- MakeHuman's z_depth runs from 0 (skin) to 100 (accessories) [12]; Roblox takes each layer's outer cage as the next one's reference [7]; Cyberpunk ranks garments and squashes the lower [15] (D).
- Deleting hidden geometry is standard for fixed outfits [8, 12] (D); Epic's techwear outfit is one mesh (earlier note TAILORED-ROUTES) (D).

## 4. British suits, 1988 to 1992 (brief)

- Broad, extended, padded shoulders, a fuller draped chest and low button stances, under Armani's influence [19, 20, 24] (D, partly search summaries).
- The double-breasted 6x1, buttoned "extra-low", was fashionable "from the mid-1980s through the early 1990s" [19] (D).
- Lapels mid-width to wide, with a low gorge; no reliable dated width found [24].

## Not found

- The kernel and smoothing of Epic's RBF (only signatures are published).
- A studio talk on tailored game jackets; a figure for the gap between clothing layers.
- Dated lapel widths for British high-street suits of 1990.
- Wrap's default values (its pages list none; r3ds.com refused the connection).

## Sources

1. Building an Outfit Asset in Unreal Engine (UE 5.7). Epic Games. Undated. https://dev.epicgames.com/documentation/unreal-engine/building-an-outfit-asset-in-unreal-engine?application_version=5.7 (read in full)
2. GenerateRBFResizingWeights and ApplyRBFResizing node pages; FRBFInterpolation API (UE 5.8). Epic Games. Undated. https://dev.epicgames.com/documentation/unreal-engine/node-reference/Dataflow/ApplyRBFResizing (read in full)
3. CustomRegionResizing node; FCustomRegionResizing and EMeshResizingCustomRegionType API (UE 5.8). Epic Games. Undated. https://dev.epicgames.com/documentation/unreal-engine/node-reference/Dataflow/CustomRegionResizing (read in full)
4. MeshResizingCore API index (UE 5.8). Epic Games. Undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/MeshResizingCore (fetched summary)
5. Auto Fitting (5 January 2026), and Change Pose by OBJ Morphing (29 May 2025). Marvelous Designer. https://support.marvelousdesigner.com/hc/en-us/articles/47358335130649-Auto-Fitting (both read in full)
6. Wrapping and Lattice nodes. Faceform Wrap documentation. Undated. https://docs.faceform.com/Wrap/Nodes/Lattice/Lattice.html (fetched summaries). Also J. Versluis, "Converting Clothing with Faceform Wrap", 30 January 2024, https://www.versluis.com/2024/01/converting-clothing-with-faceform-wrap/ (fetched summary)
7. Clothing specifications. Roblox Creator Hub. Undated. https://create.roblox.com/docs/art/accessories/clothing-specifications (fetched summary). Also B. Book-Larsson, "Layers of Genius Behind Layered Clothing", 4 April 2022 (fetched summary)
8. Layered clothing example. Roblox Creator Hub. Undated. https://create.roblox.com/docs/resources/beyond-the-dark/layered-clothing (fetched summary)
9. Conforming Clothing, and Setting Conforming Weight. Reallusion, Character Creator 4 manual. Undated. https://manual.reallusion.com/Character-Creator-4/Content/ENU/4.0/08_Cloth/Conforming_Clothing.htm (fetched summaries)
10. Daz 3D forums on the Smoothing modifier (Base Shape Matching; collision against smoothing iterations). Undated. https://www.daz3d.com/forums/discussion/232011/about-applying-the-smoothing-modifyer (search summary only). Also Daz Transfer Utility tutorial, undated (fetched summary)
11. Smooth Corrective Modifier. Blender 4.5 LTS Manual. Undated. https://docs.blender.org/manual/en/4.5/modeling/modifiers/deform/corrective_smooth.html (read in full)
12. File formats and extensions (mhclo). MakeHuman Community. Undated. https://static.makehumancommunity.org/oldsite/documentation/file_formats_and_extensions.html (search summary only)
13. How to Measure Chest for a Suit Jacket. Nathan Tailors. Updated 4 May 2026. https://www.nathantailors.com/guides/how-to-measure-chest-for-suit-jacket (fetched summary)
14. A quantification of the preferred ease allowance for the men's formal jacket patterns. Fashion and Textiles. 8 May 2019. https://link.springer.com/article/10.1186/s40691-018-0165-x (abstract read in full)
15. Garment Support: How does it work? Cyberpunk 2077 Modding wiki. Undated. https://wiki.redmodding.org/cyberpunk-2077-modding/for-mod-creators-theory/3d-modelling/garment-support-how-does-it-work (fetched summary)
16. How much of my shirt collar should show when I wear a suit jacket? Christopher's Custom. 8 May 2010. https://christopherscustom.com/how-much-of-my-shirt-collar-should-show-when-i-wear-a-suit-jacket/ (fetched summary)
17. R. Brouet, A. Sheffer, L. Boissieux and M.-P. Cani, "Design Preserving Garment Transfer", ACM Transactions on Graphics 31(4). July 2012. https://history.siggraph.org/learning/design-preserving-garment-transfer-by-brouet-sheffer-boissieux-and-cani/ (abstract only; background)
18. R. Munro, "What Half Canvas Construction Actually Means in a Tailored Jacket". Rampley and Co. 9 July 2026. https://www.rampleyandco.com/blogs/the-journal/what-half-canvas-construction-actually-means-in-a-tailored-jacket (fetched summary)
19. M. Spaiser, "Variations on the Double-Breasted Jacket". Bond Suits. 29 May 2018. https://www.bondsuits.com/variations-double-breasted-jacket-buttons-wrap-lapels-width/ (fetched summary)
20. T. Sylvester, "How relevant is 80s Armani?". Permanent Style. 2 July 2021. https://www.permanentstyle.com/2021/07/how-relevant-is-80s-armani.html (first half read)
21. Refining a Jacket: Adding Shoulder Pads (CLO help; sign-in wall), and Polycount, "marvelous designer - padded, layered clothes?" (blocked). Both undated. https://polycount.com/discussion/162105/marvelous-designer-padded-layered-clothes (search summaries only)
22. MetaHuman Clothing Construction Presets, sets of 2 and 4. Epic Games on Fab. Undated. https://www.fab.com/listings/3c0c4df1-ce96-44cf-8a30-c47d744d2a0c (search summary only)
23. M. Zhang and others, "LoBoFit: Flexible Garment Refitting via Local Bone Mapping Blending". arXiv. 8 May 2026. https://arxiv.org/abs/2605.07450 (abstract only; background)
24. 1980s power suits: shoulders and lapels. Designherkit and Gentleman's Gazette. Undated. https://designherkit.com/80s-formal-wear-men/ (search summaries only; weak, and their 4 to 5 inch peak-lapel figure is not trusted)
