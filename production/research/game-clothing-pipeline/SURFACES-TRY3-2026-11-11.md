# Tom's surfaces, try 3: the garment's own colour map (11 November 2026)

The one researched different method after two failed tries (RULINGS 7 Nov). Written 09:45 before the import.

**Questions.** 1. Why did tries 1 and 2 fail? 2. Where does a game garment's fabric read come from at 3 to 8 m? 3. What did Mafia do, as far as its files show? 4. What can be made today without new code in the material?

**Answers.**
1. The shared tiles: a weave normal averages flat past arm's length; cloth sheen (MSM_Cloth fuzz) adds light on top and turned navy violet and indigo chalky; one roughness tile over every boot slot made the matte sole glossy (review: F:/LedgerTools/gate/new/tom-surfaces-2026-11-11/review.json).
2. From colour structure, not relief: denim is an indigo warp over a pale weft, so rubbed places shift hue toward pale grey-blue as well as lighten (FADE-REFERENCE.md beside Tom's jeans: Sirlin 2026, Heddels 2011, read 30 Oct), with vertical slub streaks along the grain and stonewash mottle. The garment material draws Tint x ColourMap, and our maps were neutral grey: every pixel one hue (import_garments.py, the cloth multiply). That is why the jeans read as plain blue.
3. Mafia: every garment carries its own MacroDiffuse (DAO, 2048 to 4096) beside the fabric layers' tiling atlas (MAFIA-CLOTH-SURFACES-2026-11-11.md). The DAO's pixels were not read: the textures are not exported, and the export ran through FModel's window, which a helper may not click and computer use may not open (RULINGS 29 Oct). Unverified whether its denim streaks live in the DAO or the atlas.
4. Paint the colour in each garment's own map, in true millimetres along each pattern piece's grain (the bake chain's raster_flat.npz holds per-pixel pattern coordinates for the jeans), tint to white, the average kept at the colour he judged. Boots: the polish written only where the packed map's part is the upper (sole is part 0.5 at roughness 0.81 already). No material change.

**Made.** tools/meshgen/paint_fabric_colour.py; maps, specs and records in F:/LedgerTools/garments/tom/surfaces-2026-11-11/painted/. Jeans mean sRGB 66, 81, 102; jacket 41, 47, 71 (old 41, 47, 71 judged colour kept); boots upper roughness 0.30, sole 0.81.

**Not reached.** Mafia's DAO pixels; a dated 1990 stonewash garment measured; the jacket's per-island grain (no raster for it: its map's axes stand in; the cotton noise is nearly isotropic so the error is small).
